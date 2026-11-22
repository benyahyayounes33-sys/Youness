import * as THREE from "three";
import { screenGeometry, siteMaterial, zoeMaterial } from "./screens.js";
import { SITES } from "./sites.js";

const RINGS = 10;
const BONE = new THREE.Color("#f2ede4");
const smooth = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
const easeIO = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
const wrap = (a) => Math.atan2(Math.sin(a), Math.cos(a));

export class World {
  constructor(renderer, textures, stripHeights) {
    this.renderer = renderer;
    this.textures = textures;
    this.stripHeights = stripHeights;
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color("#050404");
    this.scene.fog = new THREE.FogExp2(0x050404, 0.03);
    this.camera = new THREE.PerspectiveCamera(52, 1, 0.05, 260);
    this.raycaster = new THREE.Raycaster();
    this.screens = [];
    this.rings = [];
    this.events = [];
    this.pick = { frame: 0, watched: null };
    this.focus = null;
    this.zoe = { idx: 0, next: 1, timer: 0, hold: 2.3, crank: 1.6, lastSlit: -1 };
    this.figYaw = 0;
    this.headYaw = 0;
    this.lookOff = new THREE.Vector2();
    this.build();
  }

  win(slug, aspect) { return Math.min(1, (512 / aspect) / this.stripHeights[slug]); }

  build() {
    const { scene } = this;
    let y = 0;
    const wallPts = [];
    const R0 = 8.6;
    wallPts.push(new THREE.Vector2(R0 + 0.7, 4.2));
    for (let i = 0; i < RINGS; i++) {
      const R = R0 * Math.pow(0.905, i);
      const w = 2.5 * Math.pow(R / R0, 0.55);
      const h = w * 0.625;
      const n = Math.max(9, Math.floor((2 * Math.PI * R) / (w * 1.1)));
      y -= h / 2;
      const group = new THREE.Group();
      group.position.y = y;
      const ring = { group, R, w, h, n, y, i, speed: 0.085 * Math.pow(1.27, i) * (i % 2 ? -1 : 1), angle: i * 0.7, detent: 0, lastClick: -1 };
      ring.detentSize = (2 * Math.PI) / (n * 3);
      group.rotation.y = ring.angle;
      const geo = screenGeometry(w, h, R);
      for (let k = 0; k < n; k++) {
        const site = SITES[(k * 4 + i * 3) % SITES.length];
        const mat = siteMaterial(this.textures[site.slug], this.win(site.slug, w / h), w, h);
        mat.uniforms.uOffset.value = (k * 0.137 + i * 0.29) % 1;
        const m = new THREE.Mesh(geo, mat);
        const phi = (k / n) * Math.PI * 2;
        m.position.set(R * Math.sin(phi), 0, R * Math.cos(phi));
        m.rotation.y = phi + Math.PI;
        m.userData = { site, ring, rate: 0.05 + ((k * 7 + i * 3) % 10) * 0.004, slotPos: m.position.clone(), slotQuat: m.quaternion.clone() };
        group.add(m);
        this.screens.push(m);
      }
      const rail = new THREE.Mesh(new THREE.TorusGeometry(R + 0.12, 0.014, 6, 220), new THREE.MeshBasicMaterial({ color: BONE.clone().multiplyScalar(1.2) }));
      rail.rotation.x = Math.PI / 2;
      rail.position.y = y - h / 2 - 0.16;
      scene.add(rail);
      scene.add(group);
      this.rings.push(ring);
      wallPts.push(new THREE.Vector2(R + 0.55, y + h / 2 + 0.32), new THREE.Vector2(R + 0.55, y - h / 2 - 0.32));
      y -= h / 2 + 0.62;
    }
    const last = this.rings[this.rings.length - 1];
    this.lastRingY = last.y;
    const lastBottom = last.y - last.h / 2 - 0.32;
    this.floorY = lastBottom - 6.2;
    const fy = this.floorY;
    wallPts.push(new THREE.Vector2(last.R + 0.9, lastBottom - 0.35), new THREE.Vector2(7.7, lastBottom - 1.1), new THREE.Vector2(7.7, fy - 0.2));
    wallPts.sort((a, b) => b.y - a.y);
    const wall = new THREE.Mesh(new THREE.LatheGeometry(wallPts.reverse(), 120),
      new THREE.MeshStandardMaterial({ color: 0x0d0c0b, roughness: 0.93, metalness: 0.06, side: THREE.BackSide }));
    scene.add(wall);
    this.mouthMat = new THREE.MeshBasicMaterial({ color: BONE.clone().multiplyScalar(1.6) });
    const mouth = new THREE.Mesh(new THREE.TorusGeometry(R0 + 0.7, 0.05, 8, 260), this.mouthMat);
    mouth.rotation.x = Math.PI / 2;
    mouth.position.y = 4.2;
    scene.add(mouth);

    scene.add(new THREE.HemisphereLight(0x22303c, 0x050404, 0.5));
    this.camLight = new THREE.PointLight(0xf2ede4, 7, 10, 2);
    scene.add(this.camLight);

    // ---- bottom chamber: floor, Prussian-blue pool, light shaft, the figure
    const floor = new THREE.Mesh(new THREE.CircleGeometry(7.7, 120), new THREE.MeshStandardMaterial({ color: 0x07080a, roughness: 0.38, metalness: 0.55 }));
    floor.rotation.x = -Math.PI / 2;
    floor.position.y = fy;
    scene.add(floor);
    this.poolMat = new THREE.ShaderMaterial({
      transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, uniforms: { uTime: { value: 0 } },
      vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
      fragmentShader: `varying vec2 vUv; uniform float uTime;
        void main(){ vec2 c = vUv - 0.5; float r = length(c) * 2.0; float a = pow(1.0 - clamp(r, 0.0, 1.0), 2.0);
          float rip = 0.88 + 0.12 * sin(r * 26.0 - uTime * 1.3);
          vec3 col = vec3(0.0, 0.192, 0.325) * 1.7 * a * rip + vec3(0.30, 0.55, 0.85) * pow(a, 7.0) * 0.45;
          gl_FragColor = vec4(col, 1.0); }`,
    });
    const pool = new THREE.Mesh(new THREE.CircleGeometry(2.8, 96), this.poolMat);
    pool.rotation.x = -Math.PI / 2;
    pool.position.y = fy + 0.01;
    scene.add(pool);
    const shaftH = 11;
    const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 2.5, shaftH, 64, 1, true), new THREE.ShaderMaterial({
      transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
      vertexShader: `varying vec2 vUv; varying vec3 vN; varying vec3 vV; void main(){ vUv = uv; vec4 wp = modelMatrix * vec4(position, 1.0);
        vN = normalize(mat3(modelMatrix) * normal); vV = normalize(cameraPosition - wp.xyz); gl_Position = projectionMatrix * viewMatrix * wp; }`,
      fragmentShader: `varying vec2 vUv; varying vec3 vN; varying vec3 vV;
        void main(){ float edge = pow(abs(dot(vN, vV)), 2.0); float fade = smoothstep(1.0, 0.0, vUv.y) * smoothstep(0.0, 0.08, vUv.y);
          gl_FragColor = vec4(vec3(0.05, 0.26, 0.45) * edge * fade * 0.2, 1.0); }`,
    }));
    shaft.position.y = fy + shaftH / 2;
    scene.add(shaft);
    const spot = new THREE.SpotLight(0x2a77c0, 48, 22, 0.42, 0.7, 1.3);
    spot.position.set(0, fy + 10, 0);
    spot.target.position.set(0, fy, 0);
    scene.add(spot, spot.target);
    const bounce = new THREE.PointLight(0x0d4a7a, 2.5, 6, 1.5);
    bounce.position.set(0, fy + 0.4, 0);
    scene.add(bounce);

    const rim = new THREE.PointLight(0xbcd6ff, 3.5, 5, 1.8);
    rim.position.set(0, fy + 2.3, -1.6);
    scene.add(rim);
    this.figure = this.makeFigure();
    this.figure.position.set(0, fy, 0);
    scene.add(this.figure);

    // ---- the zoetrope screen
    const zw = 9.8, zh = 5.5, zR = 7.15;
    this.zw = zw; this.zh = zh;
    this.zoeMat = zoeMaterial(this.textures[SITES[0].slug], this.textures[SITES[1].slug],
      this.win(SITES[0].slug, zw / zh), this.win(SITES[1].slug, zw / zh), zw, zh);
    this.zoeMat.uniforms.uBright.value = 1.15;
    this.zoeMesh = new THREE.Mesh(screenGeometry(zw, zh, zR, 64), this.zoeMat);
    this.zoeMesh.position.set(0, fy + 3.05, -zR);
    this.zoeMesh.userData = { zoe: true };
    scene.add(this.zoeMesh);
    const zLight = new THREE.PointLight(0xf2ede4, 9, 10, 1.6);
    zLight.position.set(0, fy + 2.6, -5.2);
    scene.add(zLight);
    for (const dy of [zh / 2 + 0.14, -zh / 2 - 0.14]) {
      const rail = new THREE.Mesh(new THREE.TorusGeometry(zR, 0.012, 6, 64, zw / zR), new THREE.MeshBasicMaterial({ color: BONE.clone().multiplyScalar(1.3) }));
      rail.rotation.set(Math.PI / 2, 0, Math.PI / 2 - zw / zR / 2);
      rail.position.y = fy + 3.05 + dy;
      scene.add(rail);
    }
    this.pickables = [...this.screens, this.zoeMesh];
    this.topY = 4.2;
  }

  makeFigure() {
    const g = new THREE.Group();
    const mat = new THREE.MeshStandardMaterial({ color: 0x101318, roughness: 0.55, metalness: 0.15 });
    const coatPts = [[0.001, 0.42], [0.29, 0.4], [0.31, 0.5], [0.27, 0.95], [0.235, 1.2], [0.225, 1.32], [0.255, 1.42], [0.245, 1.48], [0.15, 1.53], [0.07, 1.56], [0.001, 1.57]]
      .map(([r, y]) => new THREE.Vector2(r, y));
    const coat = new THREE.Mesh(new THREE.LatheGeometry(coatPts, 40), mat);
    coat.scale.z = 0.72;
    g.add(coat);
    for (const s of [-1, 1]) {
      const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.05, 0.46, 12), mat);
      leg.position.set(0.09 * s, 0.23, 0);
      g.add(leg);
      const shoe = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.05, 0.2), mat);
      shoe.position.set(0.09 * s, 0.025, 0.04);
      g.add(shoe);
      const arm = new THREE.Mesh(new THREE.CapsuleGeometry(0.055, 0.58, 4, 10), mat);
      arm.position.set(0.265 * s, 1.1, 0);
      arm.rotation.z = 0.07 * s;
      g.add(arm);
    }
    const head = new THREE.Group();
    head.position.y = 1.58;
    const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.05, 0.1, 10), mat);
    neck.position.y = 0.04;
    const skull = new THREE.Mesh(new THREE.SphereGeometry(0.112, 24, 18), mat);
    skull.scale.set(0.92, 1.12, 1.0);
    skull.position.y = 0.17;
    head.add(neck, skull);
    g.add(head);
    g.userData.head = head;
    return g;
  }

  /* ------------------------------------------------------------------ camera path */
  poseAt(p) {
    const fy = this.floorY;
    const q = new THREE.Quaternion();
    const m = new THREE.Matrix4();
    const look = (eye, target, up = new THREE.Vector3(0, 1, 0)) => { m.lookAt(eye, target, up); return new THREE.Quaternion().setFromRotationMatrix(m); };
    // A — above the mouth, looking straight down
    const uA = clamp(p / 0.07, 0, 1);
    const spin = uA * 0.7;
    const posA = new THREE.Vector3(0, THREE.MathUtils.lerp(13, 3.2, easeIO(uA)), 0);
    const qA = look(posA, new THREE.Vector3(0, -60, 0), new THREE.Vector3(Math.sin(spin), 0, -Math.cos(spin)));
    // B — the descent: spiral down the axis, looking out at the walls
    const uB = clamp((p - 0.055) / (0.74 - 0.055), 0, 1);
    const yaw = Math.PI + uB * Math.PI * 2.3;
    const pitch = THREE.MathUtils.lerp(-1.35, -0.4, smooth(0, 0.14, uB)) + 0.07 * Math.sin(uB * 9) + 0.12 * smooth(0.85, 1, uB);
    const yB = THREE.MathUtils.lerp(2.4, this.lastRingY - 0.4, uB * uB * (1.6 - 0.6 * uB));
    const posB = new THREE.Vector3(-Math.sin(yaw) * 0.55, yB, -Math.cos(yaw) * 0.55);
    const dirB = new THREE.Vector3(Math.cos(pitch) * Math.sin(yaw), Math.sin(pitch), Math.cos(pitch) * Math.cos(yaw));
    const qB = look(posB, posB.clone().add(dirB));
    // C — the bottom: the watcher and the zoetrope
    const uC = clamp((p - 0.72) / (0.9 - 0.72), 0, 1);
    const orbit = 0.62 - 0.18 * uC;
    const posC = new THREE.Vector3(Math.sin(orbit) * 5.4, fy + 1.7 + 0.25 * (1 - uC), Math.cos(orbit) * 5.4);
    const tgtC = new THREE.Vector3(-2.7, fy + 2.75, -6.4);
    const qC = look(posC, tgtC);
    // D — finale: rise out until the well is a ring of light
    const uD = clamp((p - 0.9) / 0.1, 0, 1);
    const eD = easeIO(uD);
    const kD = smooth(0, 0.35, uD);
    const posD = new THREE.Vector3(posC.x * (1 - kD), THREE.MathUtils.lerp(fy + 1.75, 27, eD), THREE.MathUtils.lerp(posC.z, 9.5, kD));
    const qTop = look(new THREE.Vector3(0, 27, 9.5), new THREE.Vector3(0, fy * 0.2 - 2.5, 0), new THREE.Vector3(0, 0, -1));
    const qD = qC.clone().slerp(qTop, smooth(0.05, 0.6, uD));

    let pos, quat;
    if (p < 0.72) {
      const k = smooth(0.05, 0.1, p);
      pos = posA.clone().lerp(posB, k);
      quat = qA.clone().slerp(qB, k);
    } else if (p < 0.9) {
      const endB = new THREE.Vector3(-Math.sin(Math.PI + Math.PI * 2.3) * 0.55, this.lastRingY - 0.4, -Math.cos(Math.PI + Math.PI * 2.3) * 0.55);
      const k = easeIO(smooth(0.72, 0.8, p));
      pos = (p < 0.74 ? posB : endB).clone().lerp(posC, k);
      quat = qB.clone().slerp(qC, k);
    } else {
      pos = posD;
      quat = qD;
    }
    return { pos, quat };
  }

  /* ------------------------------------------------------------------ interaction */
  pickAt(ndc, list = this.pickables) {
    this.raycaster.setFromCamera(ndc, this.camera);
    const hit = this.raycaster.intersectObjects(list, false)[0];
    return hit ? hit.object : null;
  }

  focusOn(mesh) {
    if (this.focus || !mesh || mesh.userData.zoe) return false;
    const parent = mesh.parent;
    this.scene.attach(mesh);
    this.focus = { mesh, parent, t: 0, dir: 1, startPos: mesh.position.clone(), startQuat: mesh.quaternion.clone(), prevOffset: mesh.material.uniforms.uOffset.value };
    mesh.material.uniforms.uOffset.value = 0.0;
    mesh.material.uniforms.uLoop.value = 0;
    return true;
  }

  unfocus() { if (this.focus && this.focus.dir === 1) this.focus.dir = -1; }

  scrub(delta) { if (this.focus) { const u = this.focus.mesh.material.uniforms.uOffset; u.value = clamp(u.value + delta, 0, 1); } }

  updateFocus(dt) {
    const f = this.focus;
    if (!f) return;
    f.t = clamp(f.t + (dt / 1.15) * f.dir, 0, 1);
    const e = easeIO(f.t);
    const { mesh, parent } = f;
    const ud = mesh.userData;
    const slotWorld = new THREE.Matrix4().multiplyMatrices(parent.matrixWorld, new THREE.Matrix4().compose(ud.slotPos, ud.slotQuat, new THREE.Vector3(1, 1, 1)));
    const sPos = new THREE.Vector3(), sQuat = new THREE.Quaternion(), sScl = new THREE.Vector3();
    slotWorld.decompose(sPos, sQuat, sScl);
    const cam = this.camera;
    const d = 2.6;
    const visH = 2 * d * Math.tan(THREE.MathUtils.degToRad(cam.fov / 2));
    const visW = visH * cam.aspect;
    const scale = Math.min((visW * 0.6) / ud.ring.w, (visH * 0.62) / ud.ring.h);
    const fwd = new THREE.Vector3(0, 0, -1).applyQuaternion(cam.quaternion);
    const right = new THREE.Vector3(1, 0, 0).applyQuaternion(cam.quaternion);
    const tPos = cam.position.clone().addScaledVector(fwd, d).addScaledVector(right, cam.aspect > 1 ? visW * 0.12 : 0);
    const arc = new THREE.Vector3(0, Math.sin(Math.PI * e) * 0.6, 0);
    mesh.position.copy(sPos).lerp(tPos, e).add(arc);
    mesh.quaternion.copy(sQuat).slerp(cam.quaternion, e);
    mesh.scale.setScalar(THREE.MathUtils.lerp(1, scale, e));
    mesh.material.uniforms.uUnroll.value = smooth(0.2, 0.85, f.t);
    for (const s of this.screens) if (s !== mesh) s.material.uniforms.uDim.value = THREE.MathUtils.lerp(1, 0.22, e);
    this.zoeMat.uniforms.uDim.value = THREE.MathUtils.lerp(1, 0.3, e);
    if (f.dir === -1 && f.t === 0) {
      parent.attach(mesh);
      mesh.position.copy(ud.slotPos);
      mesh.quaternion.copy(ud.slotQuat);
      mesh.scale.setScalar(1);
      mesh.material.uniforms.uUnroll.value = 0;
      mesh.material.uniforms.uLoop.value = 1;
      mesh.material.uniforms.uOffset.value = Math.max(0.03, Math.min(0.97, mesh.material.uniforms.uOffset.value));
      this.focus = null;
    }
  }

  /* ------------------------------------------------------------------ frame */
  update({ t, dt, p, vel, pointer, pointerActive, reduced }) {
    const ev = this.events;
    const sv = clamp(vel * 7, -4, 4);
    const motion = reduced ? 0.35 : 1;
    const pose = this.poseAt(p);
    const cam = this.camera;
    cam.position.copy(pose.pos);
    const tl = reduced || !pointerActive ? 0 : 1;
    const bottomK = smooth(0.74, 0.8, p) * (1 - smooth(0.88, 0.92, p));
    const yawR = THREE.MathUtils.lerp(0.22, 0.34, bottomK), pitR = THREE.MathUtils.lerp(0.12, 0.26, bottomK);
    this.lookOff.lerp(new THREE.Vector2(-pointer.x * yawR * tl, (pointer.y > 0 ? pointer.y * pitR : pointer.y * 0.12) * tl), 1 - Math.exp(-dt * 2.2));
    if (this.focus) this.lookOff.multiplyScalar(0.9);
    cam.quaternion.copy(pose.quat).multiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(this.lookOff.y, this.lookOff.x, 0, "YXZ")));
    cam.updateMatrixWorld();
    this.camLight.position.copy(cam.position);

    // fog thins as we rise for the finale so the whole well can glow
    const fogK = p > 0.9 ? THREE.MathUtils.lerp(0.03, 0.004, smooth(0.9, 0.97, p)) : p < 0.07 ? THREE.MathUtils.lerp(0.012, 0.03, smooth(0.0, 0.07, p)) : 0.03;
    this.scene.fog.density = fogK;
    this.mouthMat.color.copy(BONE).multiplyScalar(1.6 + 3.2 * smooth(0.92, 1, p));

    // rings turn and screens play, both driven by scroll velocity (scrolling up runs them backwards)
    const drive = (0.32 + 3.6 * sv) * motion;
    for (const r of this.rings) {
      r.angle += r.speed * drive * dt;
      r.group.rotation.y = r.angle;
      const det = Math.floor(r.angle / r.detentSize);
      if (det !== r.detent) {
        r.detent = det;
        const dist = Math.abs(r.y - cam.position.y);
        const s = Math.exp(-(dist * dist) / 40) * (0.45 + 0.55 * Math.min(1, Math.abs(sv) * 2));
        if (s > 0.05 && t - r.lastClick > 0.03 && !this.focus) { ev.push({ type: "ratchet", t, s, pan: Math.sin(r.angle * 3.1 + r.i) * 0.6 }); r.lastClick = t; }
      }
    }
    const play = (0.1 + 1.7 * sv) * motion;
    for (const s of this.screens) {
      const u = s.material.uniforms;
      if (this.focus && this.focus.mesh === s) { u.uOffset.value = clamp(u.uOffset.value + dt * 0.03, 0, 1); }
      else { u.uOffset.value = ((u.uOffset.value + dt * s.userData.rate * play) % 1 + 1) % 1; }
      u.uTime.value = t;
      u.uFog.value = fogK;
      u.uHover.value += ((this.pick.watched === s ? 1 : 0) - u.uHover.value) * Math.min(1, dt * 6);
    }

    // zoetrope: holds a site, then cranks the next one open slit by slit
    const z = this.zoe, zu = this.zoeMat.uniforms;
    const near = p > 0.64;
    z.timer += dt * (1 + Math.min(2, Math.abs(sv) * 1.5));
    if (z.timer > z.hold) {
      const tt = (z.timer - z.hold) / z.crank;
      if (z.lastSlit === -1 && near) ev.push({ type: "crank", t, s: 1 });
      const slit = Math.floor(clamp(tt, 0, 1) * (zu.uSlits.value + 5) - 2.5);
      if (slit !== z.lastSlit) { if (near && slit >= 0 && slit < zu.uSlits.value) ev.push({ type: "ratchet", t, s: 0.7, pan: (slit / zu.uSlits.value - 0.5) * 1.4 }); z.lastSlit = slit; }
      zu.uT.value = clamp(tt, 0, 1);
      if (tt >= 1) {
        z.idx = z.next; z.next = (z.next + 1) % SITES.length; z.timer = 0; z.lastSlit = -1;
        const A = SITES[z.idx], B = SITES[z.next];
        zu.mapA.value = this.textures[A.slug]; zu.mapB.value = this.textures[B.slug];
        zu.uWinA.value = this.win(A.slug, this.zw / this.zh); zu.uWinB.value = this.win(B.slug, this.zw / this.zh);
        zu.uOffA.value = zu.uOffB.value; zu.uOffB.value = 0; zu.uT.value = 0;
        if (near) ev.push({ type: "crank", t, s: 0.6 });
      }
    }
    zu.uOffA.value = Math.min(0.999, zu.uOffA.value + dt * 0.045);
    zu.uOffB.value = Math.min(0.999, zu.uOffB.value + dt * 0.045 * zu.uT.value);
    zu.uFlicker.value = Math.floor(t * 12) % 2;
    zu.uTime.value = t; zu.uFog.value = fogK;
    this.poolMat.uniforms.uTime.value = t;

    // what is the visitor looking at? (pointer on desktop, view centre otherwise)
    if (++this.pick.frame % 3 === 0) this.pick.watched = this.pickAt(pointerActive ? pointer : new THREE.Vector2(0, 0));
    const w = this.pick.watched;
    const target = new THREE.Vector3();
    (w || this.zoeMesh).getWorldPosition(target);
    if (this.focus) this.focus.mesh.getWorldPosition(target);
    const fig = this.figure.position;
    const want = Math.atan2(target.x - fig.x, target.z - fig.z);
    this.figYaw += wrap(want - this.figYaw) * Math.min(1, dt * 1.4);
    const headWant = clamp(wrap(want - this.figYaw), -1.1, 1.1);
    this.headYaw += (headWant - this.headYaw) * Math.min(1, dt * 4);
    this.figure.rotation.y = this.figYaw;
    const head = this.figure.userData.head;
    head.rotation.y = this.headYaw;
    const up = Math.atan2(target.y - (fig.y + 1.7), Math.hypot(target.x - fig.x, target.z - fig.z));
    head.rotation.x = clamp(-up * 0.6, -0.5, 0.35);

    this.updateFocus(dt);
    return { watched: w, zoeIdx: zu.uT.value > 0.5 ? z.next : z.idx, depth: clamp((this.topY - cam.position.y) / (this.topY - this.floorY), 0, 1) };
  }

  drainEvents() { const e = this.events; this.events = []; return e; }
}
