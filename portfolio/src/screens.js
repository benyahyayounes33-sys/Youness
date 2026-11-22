import * as THREE from "three";

/**
 * Curved screen geometry lying on the inside of a cylinder of radius R.
 * Local frame: origin on the wall, +Z points to the well's axis. `aFlat` holds the unrolled shape.
 */
export function screenGeometry(w, h, R, seg = 36) {
  const g = new THREE.PlaneGeometry(w, h, seg, 1);
  const pos = g.attributes.position;
  const flat = new Float32Array(pos.array);
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), y = pos.getY(i);
    const a = x / R;
    pos.setXYZ(i, R * Math.sin(a), y, R * (1 - Math.cos(a)));
  }
  g.setAttribute("aFlat", new THREE.BufferAttribute(flat, 3));
  g.computeVertexNormals();
  g.computeBoundingSphere();
  return g;
}

const common = /* glsl */ `
  uniform float uTime, uDim, uHover, uBright, uFog, uUnroll;
  uniform vec2 uSize;
  varying vec2 vUv; varying vec3 vN; varying vec3 vV; varying float vDepth;
  float sdRB(vec2 p, vec2 b, float r){ vec2 q = abs(p) - b + vec2(r); return length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - r; }
  vec3 glassFrame(vec3 content, float d, float bevel){
    float inner = 1.0 - smoothstep(-bevel - 0.006, -bevel, d);
    float fres = pow(1.0 - clamp(abs(dot(normalize(vN), normalize(vV))), 0.0, 1.0), 2.2);
    vec3 glass = vec3(0.09, 0.11, 0.13) + fres * vec3(0.35, 0.55, 0.65);
    vec3 col = mix(glass, content, inner);
    float rim = smoothstep(-0.018 * uSize.y, 0.0, d);                 // bright outer edge
    float bev = smoothstep(-bevel, -bevel + 0.01, d) * (1.0 - smoothstep(-bevel + 0.01, -bevel + 0.025, d)); // inner bevel line
    col += rim * mix(vec3(0.75, 0.92, 1.0), vec3(1.0, 0.86, 0.72), vUv.x) * (0.55 + 1.2 * fres);
    col += bev * vec3(0.5, 0.62, 0.7) * 0.6;
    return col;
  }
  vec3 finish(vec3 col){
    col *= uDim;
    col += uHover * vec3(0.06, 0.07, 0.08);
    float f = 1.0 - exp(-uFog * uFog * vDepth * vDepth);
    return mix(col, vec3(0.0196, 0.0157, 0.0157), clamp(f, 0.0, 1.0));
  }
`;

const vertex = /* glsl */ `
  attribute vec3 aFlat;
  uniform float uUnroll;
  varying vec2 vUv; varying vec3 vN; varying vec3 vV; varying float vDepth;
  void main(){
    vUv = uv;
    vec3 p = mix(position, aFlat, uUnroll);
    vec3 n = normalize(mix(normal, vec3(0.0, 0.0, 1.0), uUnroll));
    vec4 wp = modelMatrix * vec4(p, 1.0);
    vN = normalize(mat3(modelMatrix) * n);
    vV = cameraPosition - wp.xyz;
    vec4 mv = viewMatrix * wp;
    vDepth = -mv.z;
    gl_Position = projectionMatrix * mv;
  }
`;

const siteFragment = /* glsl */ `
  uniform sampler2D map; uniform float uOffset, uWin, uLoop;
  ${common}
  vec3 site(vec2 uv){
    float f = uOffset * (1.0 - uWin) + (1.0 - uv.y) * uWin;
    return texture2D(map, vec2(uv.x, 1.0 - f)).rgb;
  }
  void main(){
    vec2 p = (vUv - 0.5) * uSize;
    float d = sdRB(p, uSize * 0.5, 0.075 * uSize.y);
    if (d > 0.0) discard;
    float bevel = 0.05 * uSize.y;
    vec2 c = vUv - 0.5;
    float ca = 0.0016 + 0.012 * dot(c, c);
    vec3 col = vec3(site(vUv + vec2(ca, 0.0)).r, site(vUv).g, site(vUv - vec2(ca, 0.0)).b);
    col = col * 1.08 + vec3(0.035, 0.037, 0.04);   // a lit display never reads as pure black
    col = col / (1.0 + 0.55 * max(max(col.r, col.g), col.b));   // soft highlight roll-off: white pages glow, never blow out
    col *= 1.25;
    col *= 0.93 + 0.07 * sin(vUv.y * uSize.y * 190.0 - uTime * 4.0);
    col *= 1.0 - 0.45 * dot(c * 1.5, c * 1.5);
    float loop = smoothstep(0.0, 0.02, uOffset) * smoothstep(1.0, 0.98, uOffset);
    col *= mix(1.0, mix(0.12, 1.0, loop), uLoop) * uBright;
    gl_FragColor = vec4(finish(glassFrame(col, d, bevel)), 1.0);
  }
`;

const zoeFragment = /* glsl */ `
  uniform sampler2D mapA; uniform sampler2D mapB; uniform float uOffA, uOffB, uWinA, uWinB, uT, uSlits, uFlicker;
  ${common}
  vec3 siteA(vec2 uv){ float f = uOffA * (1.0 - uWinA) + (1.0 - uv.y) * uWinA; return texture2D(mapA, vec2(uv.x, 1.0 - f)).rgb; }
  vec3 siteB(vec2 uv){ float f = uOffB * (1.0 - uWinB) + (1.0 - uv.y) * uWinB; return texture2D(mapB, vec2(uv.x, 1.0 - f)).rgb; }
  void main(){
    vec2 p = (vUv - 0.5) * uSize;
    float d = sdRB(p, uSize * 0.5, 0.04 * uSize.y);
    if (d > 0.0) discard;
    float bevel = 0.035 * uSize.y;
    float sx = vUv.x * uSlits;
    float k = floor(sx);
    float lx = fract(sx);
    float open = clamp((uT * (uSlits + 5.0) - k) / 5.0, 0.0, 1.0);        // slits open one after another
    float reveal = step(abs(lx - 0.5), open * 0.5 + 0.0001) * step(0.0001, open);
    vec2 c = vUv - 0.5;
    float ca = 0.0012 + 0.008 * dot(c, c);
    vec3 a = vec3(siteA(vUv + vec2(ca, 0.0)).r, siteA(vUv).g, siteA(vUv - vec2(ca, 0.0)).b);
    vec3 b = vec3(siteB(vUv + vec2(ca, 0.0)).r, siteB(vUv).g, siteB(vUv - vec2(ca, 0.0)).b);
    vec3 col = mix(a, b, reveal);
    col = col * 1.06 + vec3(0.03);
    col = col / (1.0 + 0.55 * max(max(col.r, col.g), col.b)) * 1.25;
    float shutter = sin(3.14159 * clamp(uT, 0.0, 1.0));                 // slats only while cranking
    float slat = smoothstep(0.0, 0.07, lx) * smoothstep(1.0, 0.93, lx);
    col *= mix(1.0, mix(0.18, 1.0, slat), shutter);
    col *= 1.0 - shutter * 0.22 * uFlicker;
    col *= 0.94 + 0.06 * sin(vUv.y * uSize.y * 120.0 - uTime * 5.0);
    col *= (1.0 - 0.4 * dot(c * 1.4, c * 1.4)) * uBright;
    gl_FragColor = vec4(finish(glassFrame(col, d, bevel)), 1.0);
  }
`;

const baseUniforms = (w, h) => ({
  uTime: { value: 0 }, uDim: { value: 1 }, uHover: { value: 0 }, uBright: { value: 1.0 },
  uFog: { value: 0.04 }, uUnroll: { value: 0 }, uSize: { value: new THREE.Vector2(w, h) },
});

export function siteMaterial(tex, win, w, h) {
  return new THREE.ShaderMaterial({
    uniforms: { ...baseUniforms(w, h), map: { value: tex }, uOffset: { value: Math.random() }, uWin: { value: win }, uLoop: { value: 1 } },
    vertexShader: vertex,
    fragmentShader: siteFragment,
  });
}

export function zoeMaterial(texA, texB, winA, winB, w, h) {
  return new THREE.ShaderMaterial({
    uniforms: {
      ...baseUniforms(w, h), mapA: { value: texA }, mapB: { value: texB }, uOffA: { value: 0 }, uOffB: { value: 0 },
      uWinA: { value: winA }, uWinB: { value: winB }, uT: { value: 0 }, uSlits: { value: 26 }, uFlicker: { value: 0 },
    },
    vertexShader: vertex,
    fragmentShader: zoeFragment,
  });
}
