import "@fontsource-variable/bodoni-moda/opsz.css";
import "@fontsource-variable/bodoni-moda/opsz-italic.css";
import "@fontsource-variable/jost";
import "./style.css";
import * as THREE from "three";
import { SITES, siteUrl } from "./sites.js";
import { World } from "./world.js";
import { createPost } from "./post.js";
import { Kinetic } from "./kinetic.js";
import { SoundEngine, renderOffline } from "./audio.js";

const $ = (s) => document.querySelector(s);
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const params = new URLSearchParams(location.search);
const CAPTURE = params.has("capture");

/* ---------------------------------------------------------------- accessible list / fallback */
$("#sites-list").innerHTML = SITES.map((s, i) => {
  const url = siteUrl(s);
  const inner = `<img src="sites/${s.slug}-thumb.jpg" alt="" loading="lazy"/><span>${String(i + 1).padStart(2, "0")} — ${s.name}<br><small>${s.line}</small></span>`;
  return url ? `<a href="${url}">${inner}</a>` : `<div>${inner}</div>`;
}).join("");

function webglOK() {
  try { const c = document.createElement("canvas"); return !!(c.getContext("webgl2") || c.getContext("webgl")); } catch { return false; }
}

/* ---------------------------------------------------------------- type */
const gateTitle = new Kinetic($(".gate-title"));
const chapters = [...document.querySelectorAll(".chapter")].map((el) => ({
  el, from: parseFloat(el.dataset.from), to: parseFloat(el.dataset.to), kin: [...el.querySelectorAll(".kin")].map((k) => new Kinetic(k)),
  body: [...el.querySelectorAll(".eyebrow, .body")],
}));
const focusTitle = new Kinetic($("#focus-title"), "");

if (!webglOK()) {
  document.body.classList.add("no-gl");
  $(".gate-actions").remove();
  $("#gate-load").textContent = "WebGL is not available on this device — here are the nine walls.";
  gateTitle.show(0);
  const tick = (now) => { gateTitle.update(now / 1000); requestAnimationFrame(tick); };
  requestAnimationFrame(tick);
} else {
  boot();
}

function boot() {
  const canvas = $("#gl");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: "high-performance" });
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  const maxAniso = renderer.capabilities.getMaxAnisotropy();

  /* ---- load the nine recordings */
  const manager = new THREE.LoadingManager();
  const loader = new THREE.TextureLoader(manager);
  const textures = {}, heights = {};
  manager.onProgress = (_u, done, total) => { $("#load-pct").textContent = Math.round((done / total) * 100); };
  SITES.forEach((s) => {
    textures[s.slug] = loader.load(`sites/${s.slug}.jpg`, (tex) => { heights[s.slug] = tex.image.height; });
    textures[s.slug].colorSpace = THREE.SRGBColorSpace;
    textures[s.slug].anisotropy = maxAniso;
    textures[s.slug].minFilter = THREE.LinearMipmapLinearFilter;
  });
  const buttons = [$("#enter-sound"), $("#enter-quiet")];
  buttons.forEach((b) => (b.disabled = true));
  gateTitle.show(0.2);

  let world, post;
  manager.onLoad = () => {
    world = new World(renderer, textures, heights);
    post = createPost(renderer, world.scene, world.camera);
    resize();
    $("#gate-load").style.visibility = "hidden";
    buttons.forEach((b) => (b.disabled = false));
    if (CAPTURE) setupCapture();
  };

  /* ---- sound */
  let audio = null, engine = null, soundOn = false;
  function ensureAudio() {
    if (audio) return;
    audio = new (window.AudioContext || window.webkitAudioContext)();
    engine = new SoundEngine(audio, audio.destination);
    engine.build();
    engine.start(audio.currentTime + 0.05, 2.5);
  }
  function setSound(on) {
    soundOn = on;
    if (on) { ensureAudio(); audio.resume(); engine.setMaster(0.9); } else if (engine) engine.setMaster(0, audio.currentTime, 0.25);
    const b = $("#sound-toggle");
    b.textContent = on ? "sound on" : "sound off";
    b.setAttribute("aria-pressed", String(on));
  }
  $("#sound-toggle").addEventListener("click", () => setSound(!soundOn));

  /* ---- gate */
  let entered = false, enterT = 0;
  function enter(withSound) {
    if (entered || !world) return;
    entered = true;
    enterT = clock;
    window.scrollTo(0, 0);
    if (withSound) setSound(true);
    $("#gate").style.pointerEvents = "none";
    document.body.classList.add("entered");
    document.body.classList.remove("locked");
  }
  document.body.classList.add("locked");
  $("#enter-sound").addEventListener("click", () => enter(true));
  $("#enter-quiet").addEventListener("click", () => enter(false));

  /* ---- input */
  const pointer = new THREE.Vector2();
  let pointerActive = false, down = null;
  addEventListener("pointermove", (e) => {
    if (e.pointerType !== "mouse") return;
    pointer.set((e.clientX / innerWidth) * 2 - 1, -(e.clientY / innerHeight) * 2 + 1);
    pointerActive = true;
  });
  addEventListener("pointerdown", (e) => { down = { x: e.clientX, y: e.clientY, t: performance.now() }; });
  addEventListener("pointerup", (e) => {
    if (!entered || !world || !down || e.target.closest("a, button")) return;
    const moved = Math.hypot(e.clientX - down.x, e.clientY - down.y);
    down = null;
    if (moved > 8) return;
    if (world.focus) { closeFocus(); return; }
    const ndc = new THREE.Vector2((e.clientX / innerWidth) * 2 - 1, -(e.clientY / innerHeight) * 2 + 1);
    const hit = world.pickAt(ndc, world.screens);
    if (hit) openFocus(hit);
  });
  addEventListener("keydown", (e) => { if (e.key === "Escape" && world?.focus) closeFocus(); });
  addEventListener("wheel", (e) => { if (world?.focus) { e.preventDefault(); world.scrub(e.deltaY * 0.0005); } }, { passive: false });
  let touchY = null;
  addEventListener("touchstart", (e) => { touchY = e.touches[0].clientY; }, { passive: true });
  addEventListener("touchmove", (e) => {
    if (!world?.focus || touchY == null) return;
    e.preventDefault();
    world.scrub((touchY - e.touches[0].clientY) * 0.0012);
    touchY = e.touches[0].clientY;
  }, { passive: false });

  function openFocus(mesh) {
    if (!world.focusOn(mesh)) return;
    const s = mesh.userData.site;
    const i = SITES.indexOf(s);
    document.body.classList.add("locked");
    const f = $("#focus");
    f.hidden = false;
    f.__o = 0;
    $("#focus-index").textContent = `${String(i + 1).padStart(2, "0")} / 09 — ${s.line}`;
    $("#focus-desc").textContent = s.desc;
    focusTitle.set(s.name);
    focusTitle.show(clock, 0.35);
    const url = siteUrl(s);
    const link = $("#focus-link");
    link.hidden = !url;
    if (url) link.href = url;
    world.events.push({ type: "crank", t: clock, s: 0.8 });
  }
  function closeFocus() {
    world.unfocus();
    focusTitle.hide(clock);
    document.body.classList.remove("locked");
    world.events.push({ type: "crank", t: clock, s: 0.5 });
  }

  /* ---- sizing */
  function resize() {
    const w = innerWidth, h = innerHeight;
    const pr = Math.min(devicePixelRatio, w < 800 ? 1.5 : 1.75);
    renderer.setPixelRatio(pr);
    renderer.setSize(w, h, false);
    if (world) { world.camera.aspect = w / h; world.camera.updateProjectionMatrix(); post.setSize(w, h, pr); }
  }
  addEventListener("resize", resize);

  /* ---- frame */
  let clock = 0, p = 0, last = performance.now(), prevP = 0, vel = 0;
  const hud = { depth: $("#depth-val"), mark: $("#depth-mark"), watching: $("#watching-name"), zoe: $("#zoe-caption"), hint: $("#hint") };
  let lastWatched = null, lastZoe = -1;
  const gateEl = $("#gate"), hudEl = $("#hud");
  const fadeTo = (el, target, dt, speed = 1) => {
    if (el.__o == null) el.__o = parseFloat(getComputedStyle(el).opacity) || 0;
    el.__o += (target - el.__o) * (1 - Math.exp(-dt * speed * 2.4));
    if (Math.abs(el.__o - target) < 0.002) el.__o = target;
    el.style.opacity = el.__o.toFixed(3);
    return el.__o;
  };

  function step(t, dt, target) {
    if (!world) return null;
    p = target;
    vel = THREE.MathUtils.lerp(vel, (p - prevP) / Math.max(dt, 1e-4), 1 - Math.exp(-dt * 10));
    prevP = p;
    const info = world.update({ t, dt, p, vel, pointer, pointerActive, reduced });
    const speed = Math.min(1, Math.abs(vel) * 5);
    post.lens.uniforms.uStreak.value = reduced ? 0 : Math.min(1.4, Math.max(0, Math.abs(vel) * 6 - 0.04));
    post.lens.uniforms.uDir.value.set(0, Math.sign(vel) || 1);
    post.lens.uniforms.uTime.value = t;
    post.bloom.strength = 0.55 + speed * 0.3 + (p > 0.93 ? 0.45 * Math.min(1, (p - 0.93) / 0.05) : 0);
    post.lens.uniforms.uFade.value = entered ? Math.min(1, (t - enterT) / 1.6 + 0.25) : 0.25;
    post.composer.render(dt);

    // type
    gateTitle.update(t);
    for (const c of chapters) {
      const on = entered && p >= c.from && p < c.to && !world.focus;
      c.kin.forEach((k, i) => (on ? k.show(t, i * 0.25) : k.hide(t)));
      c.kin.forEach((k) => k.update(t));
      const vis = c.kin.some((k) => k.visible);
      c.el.classList.toggle("vis", vis);
      c.body.forEach((b, i) => fadeTo(b, on && t - (b.__on ?? (b.__on = t)) > 0.25 + i * 0.15 ? 1 : 0, dt, 1.2));
      if (!on) c.body.forEach((b) => (b.__on = null));
    }
    focusTitle.update(t);
    const fEl = $("#focus");
    if (!fEl.hidden) { const fo = fadeTo(fEl, world.focus && world.focus.dir === 1 ? 1 : 0, dt, 1.6); if (fo === 0 && !world.focus) fEl.hidden = true; }

    // HUD
    hud.depth.textContent = `−${(info.depth * 64).toFixed(1).padStart(4, "0")} m`;
    hud.mark.style.top = `${info.depth * 100}%`;
    const w = info.watched;
    const name = w ? (w.userData.zoe ? `the zoetrope — ${SITES[info.zoeIdx].name}` : `${String(SITES.indexOf(w.userData.site) + 1).padStart(2, "0")} ${w.userData.site.name}`) : "—";
    if (name !== lastWatched) { hud.watching.textContent = name; lastWatched = name; }
    const atBottom = p > 0.75 && p < 0.9 && !world.focus;
    fadeTo(hud.zoe, atBottom ? 1 : 0, dt, 1.2);
    const g = fadeTo(gateEl, entered ? 0 : 1, dt, 1.1);
    gateEl.style.visibility = g < 0.01 ? "hidden" : "visible";
    fadeTo(hudEl, entered && t - enterT > 0.6 ? 1 : 0, dt, 0.9);
    if (info.zoeIdx !== lastZoe) { hud.zoe.textContent = `№ ${String(info.zoeIdx + 1).padStart(2, "0")} — ${SITES[info.zoeIdx].name}`; lastZoe = info.zoeIdx; }
    hud.hint.textContent = p < 0.05 ? "scroll ↓" : p > 0.97 ? "scroll ↑ to go back down" : "click a screen";

    // sound
    const ev = world.drainEvents();
    if (soundOn && engine) {
      const now = audio.currentTime;
      engine.setSpeed(Math.abs(vel) * 6, info.depth, now);
      for (const e of ev) { if (e.type === "ratchet") engine.ratchet(now + Math.random() * 0.01, e.s, e.pan); else engine.crank(now, e.s); }
    }
    return { info, ev, speed: Math.abs(vel) * 6 };
  }

  function loop(now) {
    const dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    clock += dt;
    const max = document.documentElement.scrollHeight - innerHeight;
    const target = entered ? Math.min(1, Math.max(0, scrollY / Math.max(1, max))) : 0;
    const smoothP = p + (target - p) * (1 - Math.exp(-dt * (reduced ? 12 : 4.5)));
    step(clock, dt, smoothP);
    requestAnimationFrame(loop);
  }
  if (!CAPTURE) requestAnimationFrame(loop);

  /* ---- deterministic capture API (used to record the review video) */
  function setupCapture() {
    const log = { samples: [], events: [] };
    window.__world = world;
    window.__cap = {
      ready: true,
      size(w, h) { renderer.setPixelRatio(1); renderer.setSize(w, h, false); canvas.style.width = w + "px"; canvas.style.height = h + "px";
        world.camera.aspect = w / h; world.camera.updateProjectionMatrix(); post.setSize(w, h, 1); },
      enter(t) { clock = t; enter(false); enterT = t; },
      gate(t) { clock = t; gateTitle.update(t); post.lens.uniforms.uFade.value = 0.25; world.update({ t, dt: 1 / 30, p: 0, vel: 0, pointer, pointerActive: false, reduced }); post.composer.render(); },
      frame(t, dt, target, cmd = {}) {
        clock = t;
        if (cmd.pointer) { pointer.set(cmd.pointer[0], cmd.pointer[1]); pointerActive = true; } else pointerActive = false;
        if (cmd.focus != null) { const m = world.screens[cmd.focus]; openFocus(m); }
        if (cmd.unfocus) closeFocus();
        if (cmd.scrub) world.scrub(cmd.scrub);
        const r = step(t, dt, target);
        log.samples.push({ t, speed: r.speed, depth: r.info.depth });
        for (const e of r.ev) log.events.push({ ...e, t: e.t ?? t });
        return { watched: r.info.watched ? r.info.watched.userData.site?.slug || "zoe" : null };
      },
      screenIndexNear(ndcX, ndcY) { const m = world.pickAt(new THREE.Vector2(ndcX, ndcY), world.screens); return m ? world.screens.indexOf(m) : -1; },
      async audio(duration, startAt) { return renderOffline({ duration, startAt, ...log }); },
      eventCount() { return log.events.length; },
    };
  }
}
