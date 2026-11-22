#!/usr/bin/env python3
"""
4x AI upscaler for poster art (Real-ESRGAN x4plus anime 6B) that runs on CPU without PyTorch.

The official .pth weights are read with a small torch-free unpickler, the RRDBNet network is
rebuilt as an ONNX graph and executed with onnxruntime, tile by tile.

    python3 tools/esrgan_upscale.py IN.jpg [IN2.png ...] --out DIR [--model PATH.pth]

The model is downloaded from the official Real-ESRGAN GitHub release if --model is missing.
"""
import argparse
import collections
import os
import pickle
import time
import urllib.request
import zipfile

import numpy as np
import onnx
import onnxruntime as ort
from onnx import helper, numpy_helper, TensorProto
from PIL import Image

MODEL_URL = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth"
DTYPES = {"FloatStorage": np.float32, "HalfStorage": np.float16, "DoubleStorage": np.float64,
          "LongStorage": np.int64, "IntStorage": np.int32, "ByteStorage": np.uint8, "BoolStorage": np.bool_}


def load_pth(path):
    """Read a zip-format PyTorch checkpoint into numpy arrays (no torch needed)."""
    z = zipfile.ZipFile(path)
    prefix = z.namelist()[0].split("/")[0]

    def rebuild(storage, offset, size, stride, *_):
        it = storage.itemsize
        return np.lib.stride_tricks.as_strided(storage[offset:], shape=tuple(size),
                                               strides=tuple(s * it for s in stride)).copy()

    class U(pickle.Unpickler):
        def find_class(self, mod, name):
            if mod == "torch._utils" and name == "_rebuild_tensor_v2":
                return rebuild
            if mod == "torch._utils" and name == "_rebuild_parameter":
                return lambda data, *_: data
            if mod == "torch" and name in DTYPES:
                return DTYPES[name]
            if mod == "collections" and name == "OrderedDict":
                return collections.OrderedDict
            raise pickle.UnpicklingError(f"blocked: {mod}.{name}")

        def persistent_load(self, pid):
            _, dtype, key, _loc, _n = pid
            return np.frombuffer(z.read(f"{prefix}/data/{key}"), dtype=dtype)

    ck = U(z.open(f"{prefix}/data.pkl")).load()
    return ck.get("params_ema", ck.get("params", ck))


def build_onnx(Wt, num_block=6):
    nodes, inits = [], []
    cnt = [0]

    def name(p):
        cnt[0] += 1
        return f"{p}_{cnt[0]}"

    def conv(x, key):
        w, b = Wt[key + ".weight"].astype(np.float32), Wt[key + ".bias"].astype(np.float32)
        inits.extend([numpy_helper.from_array(w, key + ".w"), numpy_helper.from_array(b, key + ".b")])
        out = name(key)
        nodes.append(helper.make_node("Conv", [x, key + ".w", key + ".b"], [out], pads=[1, 1, 1, 1],
                                      kernel_shape=[3, 3]))
        return out

    def lrelu(x):
        out = name("lr")
        nodes.append(helper.make_node("LeakyRelu", [x], [out], alpha=0.2))
        return out

    def cat(xs):
        out = name("cat")
        nodes.append(helper.make_node("Concat", xs, [out], axis=1))
        return out

    def res(x, skip):  # x * 0.2 + skip
        m, out = name("mul"), name("add")
        nodes.append(helper.make_node("Mul", [x, "c02"], [m]))
        nodes.append(helper.make_node("Add", [m, skip], [out]))
        return out

    def up(x):
        out = name("up")
        nodes.append(helper.make_node("Resize", [x, "", "scales2"], [out], mode="nearest",
                                      coordinate_transformation_mode="asymmetric", nearest_mode="floor"))
        return out

    inits.append(numpy_helper.from_array(np.array(0.2, np.float32), "c02"))
    inits.append(numpy_helper.from_array(np.array([1, 1, 2, 2], np.float32), "scales2"))
    feat = conv("x", "conv_first")
    h = feat
    for i in range(num_block):
        blk_in = h
        for r in (1, 2, 3):
            p = f"body.{i}.rdb{r}"
            x0 = h
            x1 = lrelu(conv(x0, p + ".conv1"))
            x2 = lrelu(conv(cat([x0, x1]), p + ".conv2"))
            x3 = lrelu(conv(cat([x0, x1, x2]), p + ".conv3"))
            x4 = lrelu(conv(cat([x0, x1, x2, x3]), p + ".conv4"))
            x5 = conv(cat([x0, x1, x2, x3, x4]), p + ".conv5")
            h = res(x5, x0)
        h = res(h, blk_in)
    body = conv(h, "conv_body")
    f = name("feat")
    nodes.append(helper.make_node("Add", [feat, body], [f]))
    f = lrelu(conv(up(f), "conv_up1"))
    f = lrelu(conv(up(f), "conv_up2"))
    out = conv(lrelu(conv(f, "conv_hr")), "conv_last")
    nodes.append(helper.make_node("Identity", [out], ["y"]))
    g = helper.make_graph(nodes, "rrdbnet",
                          [helper.make_tensor_value_info("x", TensorProto.FLOAT, [1, 3, "h", "w"])],
                          [helper.make_tensor_value_info("y", TensorProto.FLOAT, [1, 3, "H", "W"])], inits)
    m = helper.make_model(g, opset_imports=[helper.make_opsetid("", 17)])
    m.ir_version = 8
    onnx.checker.check_model(m)
    return m


class Upscaler:
    def __init__(self, model_path, threads=None):
        if not os.path.exists(model_path):
            print("downloading model ...", flush=True)
            urllib.request.urlretrieve(MODEL_URL, model_path)
        m = build_onnx(load_pth(model_path))
        so = ort.SessionOptions()
        so.intra_op_num_threads = threads or os.cpu_count()
        so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.sess = ort.InferenceSession(m.SerializeToString(), so, providers=["CPUExecutionProvider"])

    def run(self, img, tile=192, pad=16):
        a = np.asarray(img.convert("RGB")).astype(np.float32) / 255
        h, w, _ = a.shape
        out = np.zeros((h * 4, w * 4, 3), np.float32)
        for y0 in range(0, h, tile):
            for x0 in range(0, w, tile):
                y1, x1 = min(h, y0 + tile), min(w, x0 + tile)
                ya, yb, xa, xb = max(0, y0 - pad), min(h, y1 + pad), max(0, x0 - pad), min(w, x1 + pad)
                inp = a[ya:yb, xa:xb].transpose(2, 0, 1)[None]
                y = self.sess.run(None, {"x": np.ascontiguousarray(inp)})[0][0].transpose(1, 2, 0)
                out[y0 * 4:y1 * 4, x0 * 4:x1 * 4] = y[(y0 - ya) * 4:(y0 - ya + y1 - y0) * 4,
                                                      (x0 - xa) * 4:(x0 - xa + x1 - x0) * 4]
        return Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "RealESRGAN_x4plus_anime_6B.pth"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    up = Upscaler(args.model)
    for p in args.inputs:
        t = time.time()
        im = Image.open(p)
        res = up.run(im)
        dst = os.path.join(args.out, os.path.splitext(os.path.basename(p))[0] + "_x4.png")
        res.save(dst)
        print(f"{os.path.basename(p)} {im.size} -> {res.size}  {time.time() - t:.1f}s", flush=True)


if __name__ == "__main__":
    main()
