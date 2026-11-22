"use client";

import { motion } from "framer-motion";
import { Check, Eye, Heart, Plus } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import clsx from "clsx";
import { useMounted } from "@/lib/hooks";
import { useLang } from "@/lib/i18n";
import { imageOf, vibeBySlug, type Product } from "@/lib/products";
import { useStore } from "@/lib/store";
import { EASE } from "../ui/motion";

export function ProductCard({ p, index = 0, priority = false, tone = "dark" }: {
  p: Product; index?: number; priority?: boolean; tone?: "dark" | "light";
}) {
  const { t, l, mad } = useLang();
  const add = useStore((s) => s.add);
  const setQuickView = useStore((s) => s.setQuickView);
  const toggleFav = useStore((s) => s.toggleFav);
  const fav = useStore((s) => s.favorites.includes(p.slug));
  const mounted = useMounted();
  const [added, setAdded] = useState(false);
  const isFav = mounted && fav;

  const onAdd = () => {
    add(p.slug);
    setAdded(true);
    setTimeout(() => setAdded(false), 1400);
  };

  return (
    <motion.article
      className="group relative"
      initial={{ opacity: 0, y: 36 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "0px 0px -8% 0px" }}
      transition={{ duration: 0.9, ease: EASE, delay: (index % 4) * 0.07 }}
    >
      <div className={clsx("relative aspect-[1/1.414] overflow-hidden rounded-[3px]", tone === "dark" ? "bg-graphite" : "bg-bone")}>
        <Link href={`/product/${p.slug}`} aria-label={p.name} className="absolute inset-0 z-[1]">
          <Image
            src={imageOf(p.slug)} alt={p.name} fill priority={priority}
            sizes="(min-width:1280px) 22vw, (min-width:768px) 30vw, 46vw"
            className="object-cover transition-transform duration-[1.2s] ease-[cubic-bezier(.16,1,.3,1)] group-hover:scale-[1.045]"
          />
        </Link>
        <div className="peel" aria-hidden />
        {p.badge && (
          <span className="pointer-events-none absolute start-3 top-3 z-[2] rounded-full bg-ink/85 px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.14em] text-paper backdrop-blur">
            {p.badge === "limited" && <span className="me-1.5 inline-block h-1.5 w-1.5 rounded-full bg-accent align-middle" />}
            {t.product.badge[p.badge]}
          </span>
        )}
        <button
          onClick={() => toggleFav(p.slug)}
          className={clsx("absolute end-3 top-3 z-[2] grid h-9 w-9 place-items-center rounded-full backdrop-blur transition-colors",
            isFav ? "bg-accent text-white" : "bg-ink/60 text-paper hover:bg-ink")}
          aria-label={isFav ? t.product.unfav : t.product.fav} aria-pressed={isFav}
        >
          <Heart size={16} fill={isFav ? "currentColor" : "none"} />
        </button>
        <div className="absolute inset-x-3 bottom-3 z-[2] hidden gap-2 opacity-0 transition-all duration-500 group-hover:translate-y-0 group-hover:opacity-100 group-focus-within:opacity-100 md:flex md:translate-y-3">
          <button onClick={() => setQuickView(p.slug)} className="flex flex-1 items-center justify-center gap-2 rounded-full bg-paper/90 py-2.5 text-xs font-semibold text-ink backdrop-blur hover:bg-paper">
            <Eye size={14} /> {t.product.quick}
          </button>
          <button onClick={onAdd} className="grid h-10 w-10 place-items-center rounded-full bg-accent text-white hover:bg-[#ff5247]" aria-label={t.product.add}>
            {added ? <Check size={16} /> : <Plus size={16} />}
          </button>
        </div>
        <button onClick={onAdd} className="absolute bottom-3 end-3 z-[2] grid h-10 w-10 place-items-center rounded-full bg-accent text-white shadow-lg md:hidden" aria-label={t.product.add}>
          {added ? <Check size={16} /> : <Plus size={16} />}
        </button>
      </div>
      <div className={clsx("mt-3 flex flex-col gap-1 md:mt-4 md:flex-row md:items-start md:justify-between md:gap-3", tone === "dark" ? "text-paper" : "text-ink")}>
        <div className="min-w-0">
          <p className={clsx("truncate text-[10px] font-semibold uppercase tracking-[0.18em]", tone === "dark" ? "text-silver" : "text-ink/50")}>
            {p.type === "sticker" ? t.product.sticker1 : l(vibeBySlug(p.vibe)!.name)}
          </p>
          <h3 className="mt-1 line-clamp-2 text-[14px] font-semibold leading-snug md:mt-1.5 md:text-[15px]" dir="auto">
            <Link href={`/product/${p.slug}`} className="hover:text-accent">{p.name}</Link>
          </h3>
        </div>
        <p className="shrink-0 text-[14px] font-semibold tabular-nums md:text-[15px]">{mad(p.price)}</p>
      </div>
    </motion.article>
  );
}
