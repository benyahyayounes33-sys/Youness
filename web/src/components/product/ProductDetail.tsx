"use client";

import { AnimatePresence, motion } from "framer-motion";
import { ArrowLeft, Check, ChevronDown, Heart, ShoppingBag } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import clsx from "clsx";
import { useMounted } from "@/lib/hooks";
import { useLang } from "@/lib/i18n";
import { imageOf, PRODUCTS, vibeBySlug, type Product } from "@/lib/products";
import { useStore } from "@/lib/store";
import { QtyStepper } from "../ui/bits";
import { EASE, MaskLines, Reveal } from "../ui/motion";
import { ProductCard } from "./ProductCard";

function Accordion({ title, children, open: initial = false }: { title: string; children: React.ReactNode; open?: boolean }) {
  const [open, setOpen] = useState(initial);
  return (
    <div className="border-b border-paper/12">
      <button onClick={() => setOpen(!open)} aria-expanded={open} className="flex w-full items-center justify-between py-5 text-start font-semibold">
        {title}
        <ChevronDown size={18} className={clsx("transition-transform duration-500", open && "rotate-180")} />
      </button>
      <AnimatePresence initial={false}>
        {open && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.45, ease: EASE }} className="overflow-hidden">
            <div className="pb-6 leading-relaxed text-paper/75">{children}</div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export function ProductDetail({ p }: { p: Product }) {
  const { t, l, mad } = useLang();
  const router = useRouter();
  const add = useStore((s) => s.add);
  const setCartOpen = useStore((s) => s.setCartOpen);
  const toggleFav = useStore((s) => s.toggleFav);
  const fav = useStore((s) => s.favorites.includes(p.slug));
  const mounted = useMounted();
  const [qty, setQty] = useState(1);
  const [added, setAdded] = useState(false);
  const [zoom, setZoom] = useState<{ x: number; y: number } | null>(null);
  const vibe = vibeBySlug(p.vibe)!;
  const related = PRODUCTS.filter((x) => x.vibe === p.vibe && x.slug !== p.slug).sort((a, b) => b.popularity - a.popularity).slice(0, 4);
  const isFav = mounted && fav;

  return (
    <>
      <section className="mx-auto grid max-w-[1440px] gap-10 px-5 pb-24 pt-8 md:px-10 lg:grid-cols-12 lg:gap-16 lg:pt-12">
        <div className="lg:col-span-7">
          <Link href="/shop" className="mb-6 inline-flex items-center gap-2 text-sm text-silver hover:text-paper">
            <ArrowLeft size={15} className="rtl:rotate-180" /> {t.product.back}
          </Link>
          <motion.div
            className="relative mx-auto aspect-[1/1.414] max-w-[640px] cursor-zoom-in overflow-hidden rounded-[3px] bg-graphite shadow-[0_50px_100px_-40px_rgba(0,0,0,0.8)]"
            initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 1, ease: EASE }}
            onPointerMove={(e) => {
              if (e.pointerType !== "mouse") return;
              const r = e.currentTarget.getBoundingClientRect();
              setZoom({ x: ((e.clientX - r.left) / r.width) * 100, y: ((e.clientY - r.top) / r.height) * 100 });
            }}
            onPointerLeave={() => setZoom(null)}
          >
            <Image src={imageOf(p.slug)} alt={p.name} fill priority sizes="(min-width:1024px) 640px, 92vw"
              className="object-cover transition-transform duration-300"
              style={zoom ? { transform: "scale(1.9)", transformOrigin: `${zoom.x}% ${zoom.y}%` } : undefined} />
          </motion.div>
        </div>

        <div className="lg:col-span-5 lg:pt-12">
          <div className="lg:sticky lg:top-28">
            <Link href={`/collections/${vibe.slug}`} className="text-[11px] font-semibold uppercase tracking-[0.24em] text-silver hover:text-accent">
              <span dir="ltr">N°{vibe.index}</span> · {l(vibe.name)}
            </Link>
            <h1 className="mt-4 font-display text-[clamp(2.6rem,5vw,4.6rem)] uppercase leading-[0.92]" dir="auto">
              <MaskLines lines={[p.name]} />
            </h1>
            <div className="mt-5 flex flex-wrap items-center gap-3">
              <p className="text-3xl font-semibold tabular-nums">{mad(p.price)}</p>
              {p.badge && <span className="rounded-full border border-paper/20 px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.16em]">{t.product.badge[p.badge]}</span>}
              {p.original && <span className="rounded-full bg-accent/15 px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.16em] text-accent">{t.product.original}</span>}
            </div>
            <p className="mt-6 text-lg leading-relaxed text-paper/80">{l(p.desc)}</p>
            <p className="mt-6 text-sm text-silver"><span className="font-semibold text-paper">{t.product.format} :</span> {p.type === "poster" ? t.product.poster : t.product.sticker}</p>

            <div className="mt-8 flex flex-wrap items-center gap-3">
              <QtyStepper value={qty} onChange={(v) => setQty(Math.max(1, v))} label={t.product.qty} />
              <button onClick={() => { add(p.slug, qty); setAdded(true); setCartOpen(true); setTimeout(() => setAdded(false), 1500); }}
                className="flex min-w-48 flex-1 items-center justify-center gap-2 rounded-full bg-accent px-6 py-4 text-sm font-semibold text-white transition-colors hover:bg-[#ff5247]">
                {added ? <Check size={16} /> : <ShoppingBag size={16} />} {added ? t.product.added : t.product.add}
              </button>
              <button onClick={() => toggleFav(p.slug)} aria-pressed={isFav} aria-label={isFav ? t.product.unfav : t.product.fav}
                className={clsx("grid h-[52px] w-[52px] place-items-center rounded-full border transition-colors", isFav ? "border-accent bg-accent text-white" : "border-paper/20 hover:border-paper")}>
                <Heart size={18} fill={isFav ? "currentColor" : "none"} />
              </button>
            </div>
            <button onClick={() => { add(p.slug, qty); router.push("/checkout"); }}
              className="mt-3 w-full rounded-full border border-paper/25 py-4 text-sm font-semibold transition-colors hover:bg-paper hover:text-ink">
              {t.product.orderNow}
            </button>
            <p className="mt-3 text-center text-xs text-silver">{t.checkout.cod}</p>

            <div className="mt-10 border-t border-paper/12">
              <Accordion title={t.product.details} open>
                <dl className="grid grid-cols-[auto_1fr] gap-x-6 gap-y-2 text-sm">
                  <dt className="text-silver">{t.product.format}</dt><dd>{p.type === "poster" ? t.product.poster : t.product.sticker}</dd>
                  <dt className="text-silver">{t.product.collection}</dt><dd><Link href={`/collections/${vibe.slug}`} className="underline underline-offset-2 hover:text-accent">{l(vibe.name)}</Link></dd>
                  {p.original && (<><dt className="text-silver">Design</dt><dd>{t.product.original}</dd></>)}
                </dl>
                <p className="mt-4 text-xs text-silver">{t.product.demo}</p>
              </Accordion>
              <Accordion title={t.product.apply}>{t.product.applyText}</Accordion>
              <Accordion title={t.product.delivery}>{t.product.deliveryText}</Accordion>
            </div>
          </div>
        </div>
      </section>

      {related.length > 0 && (
        <section className="border-t border-paper/10 bg-coal py-20 md:py-28">
          <div className="mx-auto max-w-[1440px] px-5 md:px-10">
            <Reveal><h2 className="font-display text-[clamp(2.2rem,5vw,4rem)] uppercase">{t.product.related}</h2></Reveal>
            <div className="mt-10 grid grid-cols-2 gap-x-4 gap-y-10 md:grid-cols-4 md:gap-x-6">
              {related.map((r, i) => <ProductCard key={r.slug} p={r} index={i} />)}
            </div>
          </div>
        </section>
      )}
    </>
  );
}
