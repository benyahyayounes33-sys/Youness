/**
 * Synthesized sound for the well — no audio files.
 * room tone (brown noise + mains hum through a stone-well reverb), wind driven by scroll speed,
 * ratchet clatter on ring detents and a crank clunk for the zoetrope.
 * Works with a live AudioContext or an OfflineAudioContext (used to render the review video).
 */
function noiseBuffer(ctx, seconds, type, seed = 1) {
  const len = Math.floor(ctx.sampleRate * seconds);
  const buf = ctx.createBuffer(2, len, ctx.sampleRate);
  let s = seed;
  const rnd = () => ((s = (s * 16807) % 2147483647) / 2147483647) * 2 - 1;
  for (let c = 0; c < 2; c++) {
    const d = buf.getChannelData(c);
    let last = 0;
    for (let i = 0; i < len; i++) {
      const w = rnd();
      if (type === "brown") { last = (last + 0.02 * w) / 1.02; d[i] = last * 3.5; } else d[i] = w * 0.5;
    }
    const fade = Math.floor(ctx.sampleRate * 0.05); // seamless loop
    for (let i = 0; i < fade; i++) { const k = i / fade; d[i] = d[i] * k + d[len - fade + i] * (1 - k); }
  }
  return buf;
}

function impulse(ctx, seconds, decay) {
  const len = Math.floor(ctx.sampleRate * seconds);
  const buf = ctx.createBuffer(2, len, ctx.sampleRate);
  let s = 7;
  const rnd = () => ((s = (s * 48271) % 2147483647) / 2147483647) * 2 - 1;
  for (let c = 0; c < 2; c++) {
    const d = buf.getChannelData(c);
    for (let i = 0; i < len; i++) {
      const t = i / ctx.sampleRate;
      d[i] = rnd() * Math.pow(1 - i / len, decay) * (t < 0.012 ? 0 : 1) * (1 - 0.55 * Math.min(1, t * 1.6)); // darker tail
    }
  }
  return buf;
}

function clickBuffer(ctx) {
  const len = Math.floor(ctx.sampleRate * 0.045);
  const buf = ctx.createBuffer(1, len, ctx.sampleRate);
  const d = buf.getChannelData(0);
  let s = 3;
  for (let i = 0; i < len; i++) {
    s = (s * 16807) % 2147483647;
    const t = i / ctx.sampleRate;
    d[i] = ((s / 2147483647) * 2 - 1) * Math.exp(-t / 0.0045) + Math.sin(2 * Math.PI * 3150 * t) * Math.exp(-t / 0.009) * 0.6;
  }
  return buf;
}

export class SoundEngine {
  constructor(ctx, destination) {
    this.ctx = ctx;
    this.master = ctx.createGain();
    this.master.gain.value = 0;
    this.comp = ctx.createDynamicsCompressor();
    this.comp.threshold.value = -26; this.comp.knee.value = 12; this.comp.ratio.value = 4;
    this.comp.attack.value = 0.004; this.comp.release.value = 0.25;
    this.makeup = ctx.createGain();
    this.makeup.gain.value = 2.2;
    this.master.connect(this.comp).connect(this.makeup).connect(destination);
    this.lastClick = -1;
  }

  build() {
    const ctx = this.ctx;
    this.brown = noiseBuffer(ctx, 7, "brown", 11);
    this.white = noiseBuffer(ctx, 5, "white", 23);
    this.clickBuf = clickBuffer(ctx);

    this.verb = ctx.createConvolver();
    this.verb.buffer = impulse(ctx, 3.6, 2.4);
    this.verbOut = ctx.createGain();
    this.verbOut.gain.value = 0.55;
    this.verb.connect(this.verbOut).connect(this.master);

    // room tone
    this.room = ctx.createBufferSource();
    this.room.buffer = this.brown;
    this.room.loop = true;
    this.roomLp = ctx.createBiquadFilter();
    this.roomLp.type = "lowpass";
    this.roomLp.frequency.value = 260;
    this.roomHp = ctx.createBiquadFilter();
    this.roomHp.type = "highpass";
    this.roomHp.frequency.value = 38;
    this.roomGain = ctx.createGain();
    this.roomGain.gain.value = 0.26;
    this.room.connect(this.roomHp).connect(this.roomLp).connect(this.roomGain).connect(this.master);
    // air: the faint hiss of a big stone room
    this.air = ctx.createBufferSource();
    this.air.buffer = this.white;
    this.air.loop = true;
    this.airHp = ctx.createBiquadFilter();
    this.airHp.type = "highpass";
    this.airHp.frequency.value = 3800;
    this.airGain = ctx.createGain();
    this.airGain.gain.value = 0.012;
    this.air.connect(this.airHp).connect(this.airGain).connect(this.verb);
    this.hum = [50, 100, 150].map((f, i) => {
      const o = ctx.createOscillator();
      o.frequency.value = f;
      const g = ctx.createGain();
      g.gain.value = [0.022, 0.012, 0.005][i];
      o.connect(g).connect(this.roomGain);
      return o;
    });

    // wind
    this.wind = ctx.createBufferSource();
    this.wind.buffer = this.white;
    this.wind.loop = true;
    this.windBp = ctx.createBiquadFilter();
    this.windBp.type = "bandpass";
    this.windBp.frequency.value = 520;
    this.windBp.Q.value = 0.7;
    this.windGain = ctx.createGain();
    this.windGain.gain.value = 0.0;
    this.windPan = ctx.createStereoPanner();
    this.wind.connect(this.windBp).connect(this.windGain).connect(this.windPan);
    this.windPan.connect(this.master);
    this.windPan.connect(this.verb);
    this.gust = ctx.createOscillator();
    this.gust.frequency.value = 0.11;
    const gustAmt = ctx.createGain();
    gustAmt.gain.value = 0.35;
    this.gust.connect(gustAmt).connect(this.windPan.pan);
    // whistle layer
    this.whistle = ctx.createBufferSource();
    this.whistle.buffer = this.white;
    this.whistle.loop = true;
    this.whistleBp = ctx.createBiquadFilter();
    this.whistleBp.type = "bandpass";
    this.whistleBp.frequency.value = 1800;
    this.whistleBp.Q.value = 9;
    this.whistleGain = ctx.createGain();
    this.whistleGain.gain.value = 0;
    this.whistle.connect(this.whistleBp).connect(this.whistleGain).connect(this.windPan);
  }

  start(t = this.ctx.currentTime, fade = 2.5) {
    [this.room, this.air, this.wind, this.whistle, this.gust, ...this.hum].forEach((n) => n.start(t));
    this.master.gain.setValueAtTime(0, t);
    this.master.gain.linearRampToValueAtTime(0.9, t + fade);
  }

  setMaster(v, t = this.ctx.currentTime, tc = 0.4) {
    this.master.gain.cancelScheduledValues(t);
    this.master.gain.setTargetAtTime(v, t, tc);
  }

  /** speed: 0..~3 (normalized scroll speed), depth: 0 (top) .. 1 (bottom) */
  setSpeed(speed, depth, t = this.ctx.currentTime, tc = 0.18) {
    const s = Math.min(1.6, speed);
    this.windGain.gain.setTargetAtTime(0.07 + 0.42 * s, t, tc);
    this.windBp.frequency.setTargetAtTime(450 + 1200 * s + 250 * depth, t, tc);
    this.whistleGain.gain.setTargetAtTime(0.004 + 0.02 * Math.max(0, s - 0.35), t, tc);
    this.whistleBp.frequency.setTargetAtTime(1500 + 1400 * s, t, tc);
    this.roomLp.frequency.setTargetAtTime(280 - 120 * depth, t, 0.8);
    this.roomGain.gain.setTargetAtTime(0.22 + 0.12 * depth, t, 0.8);
  }

  ratchet(t = this.ctx.currentTime, strength = 1, pan = 0) {
    if (t - this.lastClick < 0.018) return;
    this.lastClick = t;
    const ctx = this.ctx;
    const src = ctx.createBufferSource();
    src.buffer = this.clickBuf;
    src.playbackRate.value = 0.85 + Math.random() * 0.35;
    const bp = ctx.createBiquadFilter();
    bp.type = "bandpass";
    bp.frequency.value = 1900 + Math.random() * 1400;
    bp.Q.value = 3.5;
    const g = ctx.createGain();
    g.gain.value = 0.85 * strength;
    const p = ctx.createStereoPanner();
    p.pan.value = Math.max(-1, Math.min(1, pan));
    src.connect(bp).connect(g).connect(p);
    p.connect(this.master);
    p.connect(this.verb);
    src.start(t);
  }

  crank(t = this.ctx.currentTime, strength = 1) {
    const ctx = this.ctx;
    const o = ctx.createOscillator();
    o.frequency.setValueAtTime(120, t);
    o.frequency.exponentialRampToValueAtTime(48, t + 0.16);
    const g = ctx.createGain();
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(0.5 * strength, t + 0.006);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.28);
    const n = ctx.createBufferSource();
    n.buffer = this.clickBuf;
    n.playbackRate.value = 0.45;
    const lp = ctx.createBiquadFilter();
    lp.type = "lowpass";
    lp.frequency.value = 900;
    const ng = ctx.createGain();
    ng.gain.value = 0.5 * strength;
    o.connect(g).connect(this.master);
    g.connect(this.verb);
    n.connect(lp).connect(ng).connect(this.master);
    o.start(t);
    o.stop(t + 0.32);
    n.start(t);
  }
}

/** Render the soundtrack for a captured timeline (review video). Returns a 16-bit WAV as base64. */
export async function renderOffline({ duration, startAt, samples, events }) {
  const sr = 44100;
  const off = new OfflineAudioContext(2, Math.ceil(duration * sr), sr);
  const eng = new SoundEngine(off, off.destination);
  eng.build();
  eng.start(startAt, 2.5);
  for (let i = 0; i < samples.length; i += 2) eng.setSpeed(samples[i].speed, samples[i].depth, samples[i].t, 0.16);
  for (const e of events) {
    if (e.type === "ratchet") eng.ratchet(e.t, e.s, e.pan);
    else if (e.type === "crank") eng.crank(e.t, e.s);
  }
  eng.master.gain.setTargetAtTime(0, Math.max(0, duration - 1.6), 0.4);
  const buf = await off.startRendering();
  const L = buf.getChannelData(0), R = buf.getChannelData(1);
  let peak = 1e-6;
  for (let i = 0; i < L.length; i++) peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i]));
  const gain = Math.min(6, 0.89 / peak);
  const out = new DataView(new ArrayBuffer(44 + L.length * 4));
  const w = (o, s) => [...s].forEach((c, i) => out.setUint8(o + i, c.charCodeAt(0)));
  w(0, "RIFF"); out.setUint32(4, 36 + L.length * 4, true); w(8, "WAVE"); w(12, "fmt ");
  out.setUint32(16, 16, true); out.setUint16(20, 1, true); out.setUint16(22, 2, true); out.setUint32(24, sr, true);
  out.setUint32(28, sr * 4, true); out.setUint16(32, 4, true); out.setUint16(34, 16, true); w(36, "data"); out.setUint32(40, L.length * 4, true);
  for (let i = 0; i < L.length; i++) {
    out.setInt16(44 + i * 4, Math.max(-1, Math.min(1, L[i] * gain)) * 32767, true);
    out.setInt16(46 + i * 4, Math.max(-1, Math.min(1, R[i] * gain)) * 32767, true);
  }
  let bin = "";
  const bytes = new Uint8Array(out.buffer);
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(bin);
}
