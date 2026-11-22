/**
 * Letter-by-letter kinetic type driven by the scene clock (not CSS transitions),
 * so it animates identically live and in frame-by-frame capture.
 */
const ease = (x) => 1 - Math.pow(1 - Math.min(1, Math.max(0, x)), 4);

export class Kinetic {
  constructor(el, text = el.dataset.text || "") {
    this.el = el;
    this.letters = [];
    this.state = 0; // 0 hidden, 1 shown
    this.t0 = -99;
    this.reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
    this.set(text);
  }

  set(text) {
    this.el.textContent = "";
    this.el.setAttribute("aria-label", text);
    this.letters = [];
    text.split(" ").forEach((word, wi, arr) => {
      const w = document.createElement("span");
      w.className = "w";
      w.setAttribute("aria-hidden", "true");
      for (const ch of word) {
        const l = document.createElement("span");
        l.className = "l";
        l.textContent = ch;
        w.appendChild(l);
        this.letters.push(l);
      }
      this.el.appendChild(w);
      if (wi < arr.length - 1) this.el.appendChild(document.createTextNode(" "));
    });
    this.apply(this.state ? 1 : 0, true);
  }

  show(t, delay = 0) { if (this.state !== 1) { this.state = 1; this.t0 = t + delay; } }
  hide(t) { if (this.state !== 0) { this.state = 0; this.t0 = t; } }

  update(t) {
    const n = this.letters.length;
    const stagger = this.state ? 0.034 : 0.012;
    const dur = this.state ? 0.85 : 0.35;
    const total = (n - 1) * stagger + dur;
    if (t - this.t0 > total + 0.05 && this.settled === this.state) return;
    this.letters.forEach((l, i) => {
      const k = ease((t - this.t0 - i * stagger) / dur);
      const q = this.state ? k : 1 - k;
      if (this.reduce) { l.style.opacity = q.toFixed(3); l.style.transform = ""; return; }
      const y = (1 - q) * 0.62;
      const r = (1 - q) * (i % 2 ? 9 : -7);
      l.style.opacity = q.toFixed(3);
      l.style.transform = `translate3d(0, ${y.toFixed(3)}em, 0) rotate(${r.toFixed(2)}deg) scale(${(0.85 + 0.15 * q).toFixed(3)})`;
      l.style.filter = q < 0.99 ? `blur(${((1 - q) * 6).toFixed(2)}px)` : "";
    });
    this.settled = t - this.t0 > total ? this.state : -1;
  }

  apply(q) {
    this.letters.forEach((l) => { l.style.opacity = q; l.style.transform = q ? "" : "translate3d(0,0.62em,0)"; });
  }

  get visible() { return this.state === 1 || this.letters.some((l) => parseFloat(l.style.opacity || "0") > 0.01); }
}
