"use client";

import { motion, useMotionValue, useReducedMotion, useScroll, useSpring, useTransform, type MotionValue } from "framer-motion";
import { ArrowDown, ArrowRight } from "lucide-react";
import Image from "next/image";
import { useRef } from "react";
import { useLang } from "@/lib/i18n";
import { imageOf, PRODUCTS } from "@/lib/products";
import { EASE, Eyebrow, Magnetic, MaskLines } from "../ui/motion";

const CARDS = [
  { slug: "wanted-luffy-gear5", x: 31, y: 9, w: 39, r: -2, z: 90, depth: 0.25 },
  { slug: "911-gt3-shark-blue", x: 1, y: 21, w: 31, r: -8, z: 30, depth: 0.55 },
  { slug: "love-yourself-first", x: 67, y: 0, w: 30, r: 7, z: 50, depth: 0.4 },
  { slug: "dima-maghrib", x: 69, y: 52, w: 28, r: -5, z: 20, depth: 0.75 },
  { slug: "discipline-over-motivation", x: 9, y: 66, w: 25, r: 6, z: 10, depth: 0.9 },
];

function Card({ c, i, progress }: { c: (typeof CARDS)[number]; i: number; progress: MotionValue<number> }) {
  const reduce = useReducedMotion();
  const y = useTransform(progress, [0, 1], [0, reduce ? 0 : -260 * c.depth]);
  const name = PRODUCTS.find((p) => p.slug === c.slug)?.name ?? "";
  return (
    <motion.div
      className="absolute"
      style={{ left: `${c.x}%`, top: `${c.y}%`, width: `${c.w}%`, y, zIndex: c.z, transformStyle: "preserve-3d" }}
    >
      <motion.div
        style={{ transformStyle: "preserve-3d" }}
        initial={{ opacity: 0, y: 80, rotate: c.r * 2.5 }}
        animate={{ opacity: 1, y: 0, rotate: c.r }}
        transition={{ duration: 1.4, ease: EASE, delay: 0.35 + i * 0.1 }}
      >
        <div className="relative aspect-[1/1.414] overflow-hidden rounded-[3px] shadow-[0_40px_80px_-20px_rgba(0,0,0,0.75)] ring-1 ring-white/10"
          style={{ transform: `translateZ(${c.z}px)` }}>
          <Image src={imageOf(c.slug)} alt={name} fill priority={i < 3} sizes="(min-width:1024px) 22vw, 40vw" className="object-cover" />
          <div className="pointer-events-none absolute inset-0 bg-gradient-to-tr from-transparent via-white/0 to-white/15" />
        </div>
      </motion.div>
    </motion.div>
  );
}

export function Hero() {
  const { t } = useLang();
  const ref = useRef<HTMLElement>(null);
  const reduce = useReducedMotion();
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end start"] });
  const textY = useTransform(scrollYProgress, [0, 1], [0, reduce ? 0 : 140]);
  const fade = useTransform(scrollYProgress, [0, 0.75], [1, 0]);
  const mx = useMotionValue(0);
  const my = useMotionValue(0);
  const spring = { stiffness: 90, damping: 20, mass: 0.6 };
  const rotY = useSpring(useTransform(mx, [-0.5, 0.5], [-9, 9]), spring);
  const rotX = useSpring(useTransform(my, [-0.5, 0.5], [7, -7]), spring);

  const onMove = (e: React.PointerEvent) => {
    if (reduce || e.pointerType !== "mouse") return;
    const r = e.currentTarget.getBoundingClientRect();
    mx.set((e.clientX - r.left) / r.width - 0.5);
    my.set((e.clientY - r.top) / r.height - 0.5);
  };

  return (
    <section ref={ref} onPointerMove={onMove} className="relative -mt-16 overflow-hidden md:-mt-20" aria-label="ONELINE">
      <div aria-hidden className="pointer-events-none absolute inset-0">
        <div className="absolute -top-1/4 end-[-10%] h-[90vh] w-[90vh] rounded-full bg-[radial-gradient(circle,rgba(255,59,48,0.16),transparent_62%)]" />
        <div className="absolute bottom-0 start-[-20%] h-[70vh] w-[70vh] rounded-full bg-[radial-gradient(circle,rgba(168,170,174,0.10),transparent_65%)]" />
        <div className="absolute inset-0 bg-[linear-gradient(90deg,rgba(242,239,233,0.045)_1px,transparent_1px)] bg-[size:calc(100%/6)_100%]" />
      </div>

      <div className="relative mx-auto grid min-h-[100svh] max-w-[1440px] items-center gap-10 px-5 pb-28 pt-28 md:px-10 lg:grid-cols-12 lg:pt-24">
        <motion.div style={{ y: textY, opacity: fade }} className="relative z-10 lg:col-span-6">
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1, duration: 0.8 }}>
            <Eyebrow>{t.hero.eyebrow}</Eyebrow>
          </motion.div>
          <h1 dir="ltr" className="mt-7 text-start font-display uppercase leading-[0.86] tracking-[-0.01em] whitespace-nowrap text-[clamp(3.3rem,8.3vw,8.6rem)] rtl:text-end">
            <MaskLines
              lines={[<>YOUR WALLS<span className="text-accent">.</span></>, <>YOUR WORLD<span className="text-accent">.</span></>]}
              lineClassName={["", "text-outline"]}
              delay={0.15}
            />
          </h1>
          <motion.p className="mt-7 max-w-md font-serif text-[clamp(1.4rem,2.2vw,2rem)] italic leading-snug text-paper/85"
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.75, duration: 1, ease: EASE }}>
            {t.hero.subtitle}
          </motion.p>
          <motion.div className="mt-10 flex flex-wrap items-center gap-3"
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.95, duration: 1, ease: EASE }}>
            <Magnetic href="/shop">{t.hero.cta1} <ArrowRight size={16} className="rtl:rotate-180" /></Magnetic>
            <Magnetic href="/shop?sort=popular" variant="ghost">{t.hero.cta2}</Magnetic>
          </motion.div>
          <motion.dl className="mt-12 flex flex-wrap gap-x-8 gap-y-3 text-[11px] font-semibold uppercase tracking-[0.2em] text-silver"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.2, duration: 1 }}>
            <div className="flex gap-2"><dt className="text-paper tabular-nums">{PRODUCTS.length}</dt><dd>{t.hero.stats[0]}</dd></div>
            <div><dd>{t.hero.stats[1]}</dd></div>
            <div className="flex items-center gap-2"><span className="h-1.5 w-1.5 rounded-full bg-accent" /><dd>{t.hero.stats[2]}</dd></div>
          </motion.dl>
        </motion.div>

        <div className="relative lg:col-span-6" style={{ perspective: 1400 }}>
          <motion.div className="relative mx-auto aspect-[1/1.02] w-full max-w-[660px]"
            style={{ rotateX: rotX, rotateY: rotY, transformStyle: "preserve-3d" }}>
            {CARDS.map((c, i) => <Card key={c.slug} c={c} i={i} progress={scrollYProgress} />)}
          </motion.div>
        </div>
      </div>

      <motion.a href="#vibes" className="absolute bottom-24 start-1/2 z-10 hidden -translate-x-1/2 flex-col items-center gap-2 text-[10px] uppercase tracking-[0.3em] text-silver md:flex rtl:translate-x-1/2"
        initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.6 }}>
        {t.hero.scroll}
        <motion.span animate={reduce ? {} : { y: [0, 6, 0] }} transition={{ repeat: Infinity, duration: 1.8 }}><ArrowDown size={14} /></motion.span>
      </motion.a>

      <div className="absolute inset-x-0 bottom-0 z-10 overflow-hidden border-y border-paper/10 bg-ink/80 py-4 backdrop-blur" aria-hidden>
        <div className="marquee">
          {[0, 1].map((k) => (
            <div key={k} className="flex shrink-0 items-center">
              {[...t.marquee, ...t.marquee].map((m, i) => (
                <span key={i} className="flex items-center gap-8 px-8 font-display text-xl uppercase tracking-[0.06em] text-paper/80">
                  {m}<span className="text-accent">✦</span>
                </span>
              ))}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
