import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

/** Speed-streak lens + chromatic fringe + vignette + film grain (runs in linear space before OutputPass). */
const LensShader = {
  uniforms: {
    tDiffuse: { value: null },
    uTime: { value: 0 },
    uStreak: { value: 0 },
    uDir: { value: new THREE.Vector2(0, 1) },
    uGrain: { value: 0.075 },
    uAberr: { value: 0.006 },
    uVig: { value: 0.9 },
    uRes: { value: new THREE.Vector2(1, 1) },
    uFade: { value: 1 },
  },
  vertexShader: /* glsl */ `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
  fragmentShader: /* glsl */ `
    uniform sampler2D tDiffuse; uniform float uTime, uStreak, uGrain, uAberr, uVig, uFade; uniform vec2 uRes, uDir;
    varying vec2 vUv;
    float hash(vec2 p){ p = fract(p * vec2(443.897, 441.423)); p += dot(p, p.yx + 19.19); return fract((p.x + p.y) * p.x); }
    vec3 tap(vec2 uv, vec2 c, float ab){
      return vec3(texture2D(tDiffuse, uv + c * ab).r, texture2D(tDiffuse, uv).g, texture2D(tDiffuse, uv - c * ab).b);
    }
    void main(){
      vec2 uv = vUv; vec2 c = uv - 0.5;
      float r = length(c);
      float ab = uAberr * (0.35 + 2.2 * r) * (1.0 + uStreak * 2.0);
      vec3 col;
      if (uStreak < 0.004) {
        col = tap(uv, c, ab);
      } else {
        vec2 dir = normalize(normalize(c + 1e-5) * 0.45 + uDir * 0.75);
        float len = uStreak * 0.09 * (0.35 + r * 1.8);
        vec3 acc = vec3(0.0); float tot = 0.0;
        for (int i = 0; i < 14; i++) {
          float k = float(i) / 13.0 - 0.5;
          float w = 1.0 - abs(k) * 1.4;
          acc += tap(uv + dir * k * len, c, ab) * w; tot += w;
        }
        col = acc / tot;
      }
      col *= 1.0 - uVig * pow(r, 2.2) * 1.6;
      float g = hash(uv * uRes + fract(uTime * 7.31) * 513.0) - 0.5;
      col += g * uGrain * (0.55 + 0.45 * (1.0 - dot(col, vec3(0.33))));
      gl_FragColor = vec4(max(col, 0.0) * uFade, 1.0);
    }`,
};

export function createPost(renderer, scene, camera) {
  const size = renderer.getSize(new THREE.Vector2());
  const rt = new THREE.WebGLRenderTarget(size.x, size.y, { type: THREE.HalfFloatType, samples: 4 });
  const composer = new EffectComposer(renderer, rt);
  composer.addPass(new RenderPass(scene, camera));
  const bloom = new UnrealBloomPass(new THREE.Vector2(size.x / 2, size.y / 2), 0.55, 0.45, 0.72);
  composer.addPass(bloom);
  const lens = new ShaderPass(LensShader);
  composer.addPass(lens);
  composer.addPass(new OutputPass());
  const setSize = (w, h, pr) => {
    composer.setPixelRatio(pr);
    composer.setSize(w, h);
    bloom.resolution.set(w / 2, h / 2);
    lens.uniforms.uRes.value.set(w * pr, h * pr);
  };
  return { composer, bloom, lens, setSize };
}
