"use client";

import clsx from "clsx";
import { useLang } from "@/lib/i18n";
import { productsByVibe, vibeBySlug, type VibeSlug } from "@/lib/products";
import { PageHeader } from "../ui/bits";
import { MaskLines, Reveal } from "../ui/motion";
import { VibeDecor } from "../home/Vibes";

export function ShopHeader() {
  const { t } = useLang();
  return <PageHeader eyebrow={t.nav.shop} title={t.shop.title} sub={t.shop.sub} />;
}

const CLASS: Record<VibeSlug, string> = {
  "jdm-luxury-cars": "vibe-cars text-paper", "music-artists": "vibe-music text-paper", "movies-series": "vibe-movies text-paper",
  "football-sports": "vibe-football text-paper", "anime-gaming": "vibe-anime", "minimal-aesthetic": "vibe-minimal", motivational: "vibe-motivational",
};

export function VibeHeader({ slug }: { slug: VibeSlug }) {
  const { t, l } = useLang();
  const v = vibeBySlug(slug)!;
  return (
    <header className="px-5 pb-10 pt-6 md:px-10 md:pt-10">
      <div className={clsx("relative mx-auto flex min-h-[46svh] max-w-[1440px] flex-col justify-end overflow-hidden rounded-md p-7 md:p-12", CLASS[slug])}>
        <VibeDecor slug={slug} />
        <p className="relative z-[2] text-[11px] font-semibold uppercase tracking-[0.24em] opacity-70">
          <span dir="ltr">N°{v.index}</span> · {t.vibes.designs(productsByVibe(slug).length)}
        </p>
        <h1 className="relative z-[2] mt-4 max-w-4xl font-display text-[clamp(2.8rem,8vw,7.5rem)] uppercase leading-[0.9]">
          <MaskLines lines={[l(v.name)]} />
        </h1>
        <Reveal delay={0.2}><p className="relative z-[2] mt-4 max-w-xl font-serif text-2xl italic opacity-85">{l(v.line)}</p></Reveal>
      </div>
    </header>
  );
}
