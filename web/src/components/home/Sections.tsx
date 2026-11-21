"use client";

import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { ArrowRight, Banknote, Camera, MessageCircle, Ruler, Sparkles, Star, Sticker, Truck } from "lucide-react";
import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import clsx from "clsx";
import { useLang } from "@/lib/i18n";
import { imageOf, PRODUCTS } from "@/lib/products";
import { ProductCard } from "../product/ProductCard";
import { EASE, Eyebrow, Magnetic, MaskLines, Reveal } from "../ui/motion";

/* ------------------------------------------------------------ featured */
export function Featured() {
  const { t } = useLang();
  const [tab, setTab] = useState<"best" | "new" | "limited">("best");
  const list = PRODUCTS.filter((p) => (tab === "new" ? p.badge === "new" : tab === "limited" ? p.badge === "limited" || p.original : p.badge === "best"))
    .sort((a, b) => b.popularity - a.popularity).slice(0, 8);
  return (
    <section className="bg-coal py-24 md:py-36">
      <div className="mx-auto max-w-[1440px] px-5 md:px-10">
        <div className="flex flex-col justify-between gap-8 md:flex-row md:items-end">
          <div>
            <Eyebrow>{t.featured.eyebrow}</Eyebrow>
            <h2 className="mt-6 max-w-3xl font-display text-[clamp(2.8rem,7vw,6.5rem)] uppercase leading-[0.9]"><MaskLines inView lines={[t.featured.title]} /></h2>
          </div>
          <div role="tablist" aria-label={t.featured.eyebrow} className="flex gap-1 rounded-full border border-paper/15 p-1">
            {(["best", "new", "limited"] as const).map((k) => (
              <button key={k} role="tab" aria-selected={tab === k} onClick={() => setTab(k)}
                className={clsx("relative rounded-full px-4 py-2 text-xs font-semibold transition-colors md:px-5", tab === k ? "text-ink" : "text-paper/70 hover:text-paper")}>
                {tab === k && <motion.span layoutId="tab-pill" className="absolute inset-0 rounded-full bg-paper" transition={{ duration: 0.5, ease: EASE }} />}
                <span className="relative">{t.featured.tabs[k]}</span>
              </button>
            ))}
          </div>
        </div>
        <AnimatePresence mode="wait">
          <motion.div key={tab} className="mt-14 grid grid-cols-2 gap-x-4 gap-y-10 md:grid-cols-3 md:gap-x-6 xl:grid-cols-4"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.35 }}>
            {list.map((p, i) => <ProductCard key={p.slug} p={p} index={i} />)}
          </motion.div>
        </AnimatePresence>
        <div className="mt-16 flex justify-center">
          <Magnetic href="/shop" variant="ghost">{t.featured.viewAll} <ArrowRight size={16} className="rtl:rotate-180" /></Magnetic>
        </div>
      </div>
    </section>
  );
}

/* ------------------------------------------------------------ before / after */
export function RoomCompare() {
  const { t } = useLang();
  const [pos, setPos] = useState(50);
  const [touched, setTouched] = useState(false);
  const reduce = useReducedMotion();
  const box = useRef<HTMLDivElement>(null);
  const dragging = useRef(false);

  useEffect(() => {
    if (reduce || touched || !box.current) return;
    const el = box.current;
    let raf = 0;
    const io = new IntersectionObserver(([e]) => {
      if (!e.isIntersecting) return;
      io.disconnect();
      const start = performance.now();
      const step = (now: number) => {
        const k = Math.min(1, (now - start) / 2200);
        setPos(50 + Math.sin(k * Math.PI * 2) * 22 * (1 - k));
        if (k < 1) raf = requestAnimationFrame(step);
      };
      raf = requestAnimationFrame(step);
    }, { threshold: 0.6 });
    io.observe(el);
    return () => { io.disconnect(); cancelAnimationFrame(raf); };
  }, [reduce, touched]);

  const setFromPointer = (clientX: number) => {
    const r = box.current!.getBoundingClientRect();
    setPos(Math.max(0, Math.min(100, ((clientX - r.left) / r.width) * 100)));
  };

  return (
    <section className="mx-auto max-w-[1440px] px-5 py-24 md:px-10 md:py-36">
      <div className="grid gap-10 lg:grid-cols-12 lg:items-end">
        <div className="lg:col-span-5">
          <Eyebrow>{t.room.eyebrow}</Eyebrow>
          <h2 className="mt-6 font-display text-[clamp(2.6rem,5.5vw,5.2rem)] uppercase leading-[0.92]"><MaskLines inView lines={[t.room.title]} /></h2>
        </div>
        <Reveal className="lg:col-span-5 lg:col-start-8"><p className="text-silver">{t.room.sub}</p></Reveal>
      </div>
      <Reveal className="mt-14">
        <div ref={box} dir="ltr"
          className="relative aspect-[4/5] select-none overflow-hidden rounded-md bg-graphite sm:aspect-[16/10]"
          onPointerDown={(e) => { dragging.current = true; setTouched(true); setFromPointer(e.clientX); }}
          onPointerMove={(e) => dragging.current && setFromPointer(e.clientX)}
          onPointerUp={() => (dragging.current = false)} onPointerLeave={() => (dragging.current = false)}>
          <Image src="/scenes/room-after.jpg" alt={t.room.after} fill sizes="(min-width:1440px) 1360px, 100vw" className="object-cover object-[60%_50%]" />
          <div className="absolute inset-0" style={{ clipPath: `inset(0 ${100 - pos}% 0 0)` }}>
            <Image src="/scenes/room-before.jpg" alt={t.room.before} fill sizes="(min-width:1440px) 1360px, 100vw" className="object-cover object-[60%_50%]" />
          </div>
          <span className="absolute start-4 top-4 rounded-full bg-ink/80 px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.2em] backdrop-blur">{t.room.before}</span>
          <span className="absolute end-4 top-4 rounded-full bg-accent px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.2em]">{t.room.after}</span>
          <div className="pointer-events-none absolute inset-y-0 w-px bg-paper" style={{ left: `${pos}%` }}>
            <span className="absolute top-1/2 grid h-14 w-14 -translate-x-1/2 -translate-y-1/2 place-items-center rounded-full bg-paper text-ink shadow-2xl">
              <ArrowRight size={16} className="absolute -translate-x-2.5 rotate-180" /><ArrowRight size={16} className="absolute translate-x-2.5" />
            </span>
          </div>
          <input type="range" min={0} max={100} value={Math.round(pos)} className="sr-range" aria-label={t.room.label}
            onChange={(e) => { setTouched(true); setPos(Number(e.target.value)); }} />
          <span className="pointer-events-none absolute bottom-4 start-1/2 -translate-x-1/2 rounded-full bg-ink/70 px-4 py-2 text-xs text-paper/80 backdrop-blur">{t.room.hint}</span>
        </div>
      </Reveal>
    </section>
  );
}

/* ------------------------------------------------------------ why */
const WHY_ICONS = [Ruler, Sticker, Banknote, MessageCircle, Truck, Sparkles];

export function WhyUs() {
  const { t } = useLang();
  return (
    <section className="bg-paper py-24 text-ink md:py-36">
      <div className="mx-auto max-w-[1440px] px-5 md:px-10">
        <Eyebrow className="!text-ink/50">{t.why.eyebrow}</Eyebrow>
        <h2 className="mt-6 max-w-4xl font-display text-[clamp(2.4rem,5vw,4.8rem)] uppercase leading-[0.95]"><MaskLines inView lines={[t.why.title]} /></h2>
        <div className="mt-16 grid border-t border-ink/15 sm:grid-cols-2 lg:grid-cols-3">
          {t.why.items.map((it, i) => {
            const Icon = WHY_ICONS[i];
            return (
              <Reveal key={it.t} delay={(i % 3) * 0.08} className="group border-b border-ink/15 py-10 sm:pe-10 lg:[&:nth-child(3n+2)]:border-x lg:[&:nth-child(3n+2)]:px-10 lg:[&:nth-child(3n)]:ps-10">
                <div className="flex items-center justify-between">
                  <Icon size={28} strokeWidth={1.4} className="transition-transform duration-500 group-hover:-rotate-6 group-hover:text-accent" />
                  <span className="font-display text-sm text-ink/30" dir="ltr">0{i + 1}</span>
                </div>
                <h3 className="mt-8 font-display text-3xl uppercase">{it.t}</h3>
                <p className="mt-3 max-w-xs text-ink/70">{it.d}</p>
              </Reveal>
            );
          })}
        </div>
      </div>
    </section>
  );
}

/* ------------------------------------------------------------ how it works */
export function HowItWorks() {
  const { t } = useLang();
  return (
    <section className="mx-auto max-w-[1440px] px-5 py-24 md:px-10 md:py-36">
      <Eyebrow>{t.how.eyebrow}</Eyebrow>
      <h2 className="mt-6 font-display text-[clamp(2.6rem,6vw,5.6rem)] uppercase leading-[0.92]"><MaskLines inView lines={[t.how.title]} /></h2>
      <ol className="mt-16 grid gap-10 md:grid-cols-3">
        {t.how.steps.map((s, i) => (
          <Reveal as="li" key={s.t} delay={i * 0.12} className="relative border-t border-paper/15 pt-8">
            <span className="absolute -top-px start-0 h-px w-16 bg-accent" />
            <span dir="ltr" className="font-display text-7xl leading-none text-paper/10">0{i + 1}</span>
            <h3 className="mt-4 font-display text-3xl uppercase">{s.t}</h3>
            <p className="mt-3 max-w-xs text-silver">{s.d}</p>
          </Reveal>
        ))}
      </ol>
    </section>
  );
}

/* ------------------------------------------------------------ social proof (placeholders) */
export function Social() {
  const { t } = useLang();
  const tiles = ["/scenes/room-after.jpg", imageOf("wanted-shanks"), imageOf("love-yourself-first"), imageOf("911-gt3-noir-mat"), "/scenes/room-before.jpg", imageOf("dima-maghrib")];
  return (
    <section className="bg-coal py-24 md:py-36">
      <div className="mx-auto max-w-[1440px] px-5 md:px-10">
        <div className="flex flex-col justify-between gap-6 md:flex-row md:items-end">
          <div>
            <Eyebrow><span dir="ltr">{t.social.eyebrow}</span></Eyebrow>
            <h2 className="mt-6 font-display text-[clamp(2.8rem,7vw,6.5rem)] uppercase leading-[0.9]"><MaskLines inView lines={[t.social.title]} /></h2>
          </div>
          <Reveal><p className="max-w-sm text-silver">{t.social.sub}</p></Reveal>
        </div>
        <div className="mt-14 grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-6">
          {tiles.map((src, i) => (
            <Reveal key={i} delay={i * 0.05} className="group relative aspect-square overflow-hidden rounded-[3px] bg-graphite">
              <Image src={src} alt="" fill sizes="(min-width:1024px) 16vw, 45vw" className="object-cover opacity-45 grayscale transition-all duration-700 group-hover:scale-105 group-hover:opacity-70" />
              <div className="absolute inset-0 flex flex-col items-center justify-center gap-2 p-3 text-center">
                <Camera size={22} strokeWidth={1.4} />
                <span className="text-[10px] font-semibold uppercase tracking-[0.18em] text-paper/80">{t.social.placeholder}</span>
              </div>
            </Reveal>
          ))}
        </div>
        <h3 className="mt-24 font-display text-4xl uppercase">{t.social.reviewsTitle}</h3>
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {t.social.reviews.map((r, i) => (
            <Reveal key={i} delay={i * 0.08} className="flex flex-col rounded-md border border-dashed border-paper/25 p-7">
              <span className="w-fit rounded-full bg-paper/10 px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.16em] text-silver">{t.social.reviewExample}</span>
              <div className="mt-6 flex gap-1 text-paper/25" aria-hidden>{[0, 1, 2, 3, 4].map((k) => <Star key={k} size={16} />)}</div>
              <p className="mt-4 font-serif text-xl italic leading-snug text-paper/70">“{r.text}”</p>
              <p className="mt-auto pt-6 text-xs text-silver">{r.who}</p>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ------------------------------------------------------------ closing CTA */
export function ClosingCta() {
  const { t } = useLang();
  return (
    <section className="relative overflow-hidden bg-accent text-ink">
      <div className="mx-auto flex max-w-[1440px] flex-col items-start gap-10 px-5 py-24 md:flex-row md:items-end md:justify-between md:px-10 md:py-32">
        <div>
          <h2 className="font-display text-[clamp(3.6rem,12vw,11rem)] uppercase leading-[0.85]"><MaskLines inView lines={[t.cta.title]} /></h2>
          <Reveal><p className="mt-6 max-w-md font-serif text-2xl italic">{t.cta.sub}</p></Reveal>
        </div>
        <Magnetic href="/shop" variant="light" className="shrink-0">{t.cta.button} <ArrowRight size={16} className="rtl:rotate-180" /></Magnetic>
      </div>
    </section>
  );
}
