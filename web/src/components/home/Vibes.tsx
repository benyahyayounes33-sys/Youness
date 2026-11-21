"use client";

import { ArrowUpRight } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import clsx from "clsx";
import { useLang } from "@/lib/i18n";
import { imageOf, productsByVibe, VIBES, type Vibe, type VibeSlug } from "@/lib/products";
import { Eyebrow, MaskLines, Reveal } from "../ui/motion";

const CLASS: Record<VibeSlug, string> = {
  "jdm-luxury-cars": "vibe-cars text-paper",
  "music-artists": "vibe-music text-paper",
  "movies-series": "vibe-movies text-paper",
  "football-sports": "vibe-football text-paper",
  "anime-gaming": "vibe-anime",
  "minimal-aesthetic": "vibe-minimal",
  motivational: "vibe-motivational",
};

const TITLE: Record<VibeSlug, string> = {
  "jdm-luxury-cars": "font-display uppercase italic -skew-x-6 tracking-tight",
  "music-artists": "font-serif italic normal-case",
  "movies-series": "font-display uppercase tracking-[0.02em]",
  "football-sports": "font-display uppercase",
  "anime-gaming": "font-display uppercase",
  "minimal-aesthetic": "font-serif italic normal-case",
  motivational: "font-display uppercase",
};

/** Decorative layer that gives each vibe its own personality. */
export function VibeDecor({ slug }: { slug: VibeSlug }) {
  switch (slug) {
    case "jdm-luxury-cars":
      return (
        <>
          <span className="absolute inset-y-0 end-[34%] w-3 -skew-x-[20deg] bg-accent/90" aria-hidden />
          <span className="absolute inset-y-0 end-[calc(34%-18px)] w-1 -skew-x-[20deg] bg-accent/50" aria-hidden />
          <span dir="ltr" className="absolute -bottom-6 end-4 font-display text-[9rem] italic leading-none text-paper/[0.06]" aria-hidden>RS</span>
        </>
      );
    case "music-artists":
      return (
        <span className="absolute -end-16 top-1/2 h-72 w-72 -translate-y-1/2 rounded-full bg-[repeating-radial-gradient(circle,#232027_0_1px,#16141a_1px_4px)] shadow-2xl motion-safe:animate-[spin_14s_linear_infinite] motion-safe:[animation-play-state:paused] group-hover:[animation-play-state:running]" aria-hidden>
          <span className="absolute inset-[38%] rounded-full bg-accent" /><span className="absolute inset-[48%] rounded-full bg-ink" />
        </span>
      );
    case "football-sports":
      return (
        <>
          <span className="absolute inset-4 rounded-sm border border-paper/15" aria-hidden />
          <span className="absolute start-1/2 top-1/2 h-28 w-28 -translate-x-1/2 -translate-y-1/2 rounded-full border border-paper/15 rtl:translate-x-1/2" aria-hidden />
          <span className="absolute inset-x-4 top-1/2 h-px bg-paper/15" aria-hidden />
        </>
      );
    case "anime-gaming":
      return (
        <span className="absolute end-5 top-14" aria-hidden>
          <span className="block font-display text-5xl leading-[0.95] text-ink/85 [writing-mode:vertical-rl]">アニメ</span>
        </span>
      );
    case "motivational":
      return (
        <span dir="ltr" className="absolute inset-0 flex flex-col justify-center overflow-hidden font-display text-[3.6rem] uppercase leading-[0.85] text-outline-thin text-ink/15 md:text-[5.5rem] md:text-ink/25" aria-hidden>
          <span>no excuses</span><span className="ms-16">no excuses</span><span>no excuses</span>
        </span>
      );
    default:
      return null;
  }
}

function VibeCard({ v, className, index }: { v: Vibe; className: string; index: number }) {
  const { t, l } = useLang();
  const count = productsByVibe(v.slug).length;
  const light = ["anime-gaming", "minimal-aesthetic", "motivational"].includes(v.slug);
  return (
    <Reveal delay={(index % 3) * 0.08} className={className}>
      <Link href={`/collections/${v.slug}`}
        className={clsx("group relative flex h-full min-h-[300px] flex-col overflow-hidden rounded-md p-6 md:p-8", CLASS[v.slug])}>
        <VibeDecor slug={v.slug} />
        <div className="relative z-[2] flex items-center justify-between text-[11px] font-semibold uppercase tracking-[0.22em] opacity-70">
          <span dir="ltr">N°{v.index}</span>
          <span>{t.vibes.designs(count)}</span>
        </div>
        <h3 className={clsx("relative z-[2] mt-4 max-w-[62%] text-[clamp(2rem,3.2vw,3.2rem)] leading-[0.95]", TITLE[v.slug])}>
          {l(v.name)}
        </h3>
        <p className="relative z-[2] mt-3 max-w-[52%] text-sm opacity-75">{l(v.line)}</p>
        <span className={clsx("relative z-[2] mt-auto inline-flex w-fit items-center gap-2 rounded-full px-4 py-2 text-xs font-semibold transition-colors",
          light ? "bg-ink text-paper group-hover:bg-paper group-hover:text-ink" : "bg-paper text-ink group-hover:bg-accent group-hover:text-white")}>
          {t.vibes.explore} <ArrowUpRight size={14} className="rtl:-scale-x-100" />
        </span>
        <div className="pointer-events-none absolute bottom-[-6%] end-[5%] z-[1] aspect-[1/0.95] w-[44%] max-w-[300px]" aria-hidden>
          {v.cover.map((slug, i) => (
            <span key={slug}
              className="absolute bottom-0 aspect-[1/1.414] w-[58%] overflow-hidden rounded-[2px] shadow-[0_24px_40px_-14px_rgba(0,0,0,0.7)] transition-transform duration-700 ease-[cubic-bezier(.16,1,.3,1)]"
              style={{ insetInlineEnd: `${i * 19}%`, zIndex: 3 - i, transform: `rotate(${(i - 1) * 7}deg) translateY(${i * 6}%)` }}>
              <Image src={imageOf(slug)} alt="" fill sizes="(min-width:1024px) 14vw, 30vw" className="object-cover" />
            </span>
          ))}
        </div>
      </Link>
    </Reveal>
  );
}

const LAYOUT = [
  "lg:col-span-7 lg:row-span-2",
  "lg:col-span-5",
  "lg:col-span-5",
  "lg:col-span-4",
  "lg:col-span-4",
  "lg:col-span-4",
  "lg:col-span-12",
];

export function Vibes() {
  const { t } = useLang();
  const order: VibeSlug[] = ["anime-gaming", "jdm-luxury-cars", "movies-series", "music-artists", "minimal-aesthetic", "football-sports", "motivational"];
  return (
    <section id="vibes" className="mx-auto max-w-[1440px] scroll-mt-24 px-5 py-24 md:px-10 md:py-36">
      <div className="flex flex-col justify-between gap-6 md:flex-row md:items-end">
        <div>
          <Eyebrow>{t.vibes.eyebrow}</Eyebrow>
          <h2 className="mt-6 font-display text-[clamp(3rem,8vw,7.5rem)] uppercase leading-[0.9]"><MaskLines inView lines={[t.vibes.title]} /></h2>
        </div>
        <Reveal><p className="max-w-sm text-silver">{t.vibes.sub}</p></Reveal>
      </div>
      <div className="mt-14 grid grid-cols-1 gap-4 md:grid-cols-2 lg:auto-rows-[300px] lg:grid-cols-12">
        {order.map((slug, i) => (
          <VibeCard key={slug} v={VIBES.find((v) => v.slug === slug)!} index={i} className={clsx(LAYOUT[i], i === 6 && "md:col-span-2")} />
        ))}
      </div>
    </section>
  );
}
