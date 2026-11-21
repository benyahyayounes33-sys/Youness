"use client";

import { AnimatePresence, motion } from "framer-motion";
import { ArrowRight, Heart, Search, ShoppingBag, Trash2, X } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import clsx from "clsx";
import { STORE } from "@/lib/config";
import { useEscape, useMounted, useScrollLock } from "@/lib/hooks";
import { useLang } from "@/lib/i18n";
import { totals } from "@/lib/order";
import { imageOf, PRODUCTS, productBySlug, vibeBySlug } from "@/lib/products";
import { useStore } from "@/lib/store";
import { QtyStepper } from "../ui/bits";
import { EASE, Magnetic } from "../ui/motion";

/* ------------------------------------------------------------------ cart drawer */
export function CartDrawer() {
  const { t, mad, lang } = useLang();
  const open = useStore((s) => s.cartOpen);
  const setOpen = useStore((s) => s.setCartOpen);
  const items = useStore((s) => s.items);
  const setQty = useStore((s) => s.setQty);
  const remove = useStore((s) => s.remove);
  const mounted = useMounted();
  const close = useCallback(() => setOpen(false), [setOpen]);
  useScrollLock(open);
  useEscape(close, open);
  const tt = totals(mounted ? items : []);
  const progress = Math.min(1, tt.subtotal / STORE.freeShippingFrom);
  const side = lang === "ar" ? "-100%" : "100%";

  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-[80]" role="dialog" aria-modal="true" aria-label={t.cart.title}>
          <motion.div className="absolute inset-0 bg-ink/70 backdrop-blur-sm" onClick={close}
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} />
          <motion.aside
            className="absolute inset-y-0 end-0 flex w-full max-w-md flex-col bg-paper text-ink"
            initial={{ x: side }} animate={{ x: 0 }} exit={{ x: side }} transition={{ duration: 0.6, ease: EASE }}
          >
            <div className="flex items-center justify-between border-b border-ink/10 px-6 py-5">
              <h2 className="font-display text-3xl uppercase">{t.cart.title}</h2>
              <button onClick={close} className="grid h-10 w-10 place-items-center rounded-full hover:bg-ink/5" aria-label={t.nav.close} autoFocus>
                <X size={20} />
              </button>
            </div>
            {tt.lines.length === 0 ? (
              <div className="flex flex-1 flex-col items-center justify-center gap-6 px-8 text-center">
                <ShoppingBag size={40} strokeWidth={1.2} className="text-ink/30" />
                <p className="font-serif text-3xl italic">{t.cart.empty}</p>
                <Link href="/shop" onClick={close} className="rounded-full bg-ink px-7 py-3.5 text-sm font-semibold text-paper hover:bg-accent">{t.cart.emptyCta}</Link>
              </div>
            ) : (
              <>
                <div className="px-6 pt-5">
                  <p className="text-xs font-medium text-ink/70">{tt.free ? t.cart.freeReached : t.cart.freeLeft(mad(tt.missingForFree))}</p>
                  <div className="mt-2 h-1 overflow-hidden rounded-full bg-ink/10">
                    <motion.div className="h-full bg-accent" initial={false} animate={{ width: `${progress * 100}%` }} transition={{ duration: 0.6, ease: EASE }} />
                  </div>
                </div>
                <ul className="flex-1 space-y-5 overflow-y-auto px-6 py-6">
                  {tt.lines.map((ln) => (
                    <li key={ln.slug} className="flex gap-4">
                      <Link href={`/product/${ln.slug}`} onClick={close} className="relative aspect-[1/1.414] w-20 shrink-0 overflow-hidden rounded-[2px] bg-bone">
                        <Image src={imageOf(ln.slug)} alt={ln.name} fill sizes="80px" className="object-cover" />
                      </Link>
                      <div className="flex min-w-0 flex-1 flex-col">
                        <div className="flex items-start justify-between gap-2">
                          <p className="truncate text-sm font-semibold" dir="auto">{ln.name}</p>
                          <p className="shrink-0 text-sm font-semibold tabular-nums">{mad(ln.total)}</p>
                        </div>
                        <p className="text-xs text-ink/55">{ln.type === "poster" ? t.product.poster1 : t.product.sticker1} · {mad(ln.unit)}</p>
                        <div className="mt-auto flex items-center justify-between pt-2">
                          <QtyStepper size="sm" value={ln.qty} onChange={(v) => setQty(ln.slug, v)} label={t.product.qty} />
                          <button onClick={() => remove(ln.slug)} className="flex items-center gap-1 text-xs text-ink/55 hover:text-accent">
                            <Trash2 size={13} /> {t.cart.remove}
                          </button>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
                <div className="border-t border-ink/10 px-6 py-6">
                  <div className="flex items-center justify-between text-lg font-semibold">
                    <span>{t.cart.subtotal}</span><span className="tabular-nums">{mad(tt.subtotal)}</span>
                  </div>
                  <p className="mt-1 text-xs text-ink/55">{t.cart.deliveryNote}</p>
                  <Link href="/checkout" onClick={close}
                    className="mt-5 flex w-full items-center justify-center gap-2 rounded-full bg-accent py-4 text-sm font-semibold text-white hover:bg-[#ff5247]">
                    {t.cart.checkout} <ArrowRight size={16} className="rtl:rotate-180" />
                  </Link>
                  <Link href="/cart" onClick={close} className="mt-3 block text-center text-sm font-medium underline-offset-4 hover:underline">{t.cart.view}</Link>
                </div>
              </>
            )}
          </motion.aside>
        </div>
      )}
    </AnimatePresence>
  );
}

/* ------------------------------------------------------------------ quick view */
export function QuickView() {
  const { t, l, mad } = useLang();
  const slug = useStore((s) => s.quickView);
  const setQuickView = useStore((s) => s.setQuickView);
  const add = useStore((s) => s.add);
  const setCartOpen = useStore((s) => s.setCartOpen);
  const toggleFav = useStore((s) => s.toggleFav);
  const favs = useStore((s) => s.favorites);
  const [qty, setQty] = useState(1);
  const close = useCallback(() => setQuickView(null), [setQuickView]);
  useScrollLock(!!slug);
  useEscape(close, !!slug);
  useEffect(() => setQty(1), [slug]);
  const p = slug ? productBySlug(slug) : undefined;

  return (
    <AnimatePresence>
      {p && (
        <div className="fixed inset-0 z-[80] grid place-items-center p-4" role="dialog" aria-modal="true" aria-label={p.name}>
          <motion.div className="absolute inset-0 bg-ink/80 backdrop-blur-sm" onClick={close} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} />
          <motion.div
            className="relative grid max-h-[92svh] w-full max-w-4xl overflow-y-auto rounded-md bg-paper text-ink md:grid-cols-2"
            initial={{ opacity: 0, y: 40, scale: 0.97 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: 30, scale: 0.98 }}
            transition={{ duration: 0.55, ease: EASE }}
          >
            <div className="relative aspect-[1/1.414] bg-bone md:aspect-auto md:min-h-[560px]">
              <Image src={imageOf(p.slug)} alt={p.name} fill sizes="(min-width:768px) 450px, 90vw" className="object-cover" />
            </div>
            <div className="flex flex-col p-7 md:p-9">
              <button onClick={close} className="absolute end-4 top-4 z-10 grid h-10 w-10 place-items-center rounded-full bg-paper/90 hover:bg-ink hover:text-paper" aria-label={t.nav.close} autoFocus>
                <X size={18} />
              </button>
              <p className="text-[11px] font-semibold uppercase tracking-[0.22em] text-ink/50">{l(vibeBySlug(p.vibe)!.name)}</p>
              <h2 className="mt-3 font-display text-4xl uppercase leading-none" dir="auto">{p.name}</h2>
              <p className="mt-4 text-2xl font-semibold tabular-nums">{mad(p.price)}</p>
              <p className="mt-5 leading-relaxed text-ink/75">{l(p.desc)}</p>
              <p className="mt-5 text-sm"><span className="font-semibold">{t.product.format} :</span> {p.type === "poster" ? t.product.poster : t.product.sticker}</p>
              {p.original && <p className="mt-2 text-sm font-semibold text-accent">{t.product.original}</p>}
              <div className="mt-auto flex flex-wrap items-center gap-3 pt-8">
                <QtyStepper value={qty} onChange={(v) => setQty(Math.max(1, v))} label={t.product.qty} />
                <button onClick={() => { add(p.slug, qty); close(); setCartOpen(true); }}
                  className="flex flex-1 items-center justify-center gap-2 rounded-full bg-accent px-6 py-3.5 text-sm font-semibold text-white hover:bg-[#ff5247]">
                  <ShoppingBag size={16} /> {t.product.add}
                </button>
                <button onClick={() => toggleFav(p.slug)} className={clsx("grid h-11 w-11 place-items-center rounded-full border", favs.includes(p.slug) ? "border-accent bg-accent text-white" : "border-ink/20")}
                  aria-label={favs.includes(p.slug) ? t.product.unfav : t.product.fav} aria-pressed={favs.includes(p.slug)}>
                  <Heart size={16} fill={favs.includes(p.slug) ? "currentColor" : "none"} />
                </button>
              </div>
              <Link href={`/product/${p.slug}`} onClick={close} className="mt-5 text-sm font-medium underline underline-offset-4 hover:text-accent">{t.product.viewFull}</Link>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

/* ------------------------------------------------------------------ search */
const norm = (s: string) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");

export function SearchOverlay() {
  const { t, l, mad } = useLang();
  const open = useStore((s) => s.searchOpen);
  const setOpen = useStore((s) => s.setSearchOpen);
  const [q, setQ] = useState("");
  const router = useRouter();
  const input = useRef<HTMLInputElement>(null);
  const close = useCallback(() => { setOpen(false); setQ(""); }, [setOpen]);
  useScrollLock(open);
  useEscape(close, open);
  useEffect(() => { if (open) setTimeout(() => input.current?.focus(), 50); }, [open]);
  const results = useMemo(() => {
    const n = norm(q.trim());
    if (!n) return PRODUCTS.filter((p) => p.badge === "best").slice(0, 6);
    return PRODUCTS.filter((p) => norm(`${p.name} ${l(vibeBySlug(p.vibe)!.name)} ${p.desc.fr}`).includes(n)).slice(0, 8);
  }, [q, l]);

  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-[85]" role="dialog" aria-modal="true" aria-label={t.nav.search}>
          <motion.div className="absolute inset-0 bg-ink/85 backdrop-blur-md" onClick={close} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} />
          <motion.div className="relative mx-auto mt-[10svh] w-[min(720px,92vw)]"
            initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -12 }} transition={{ duration: 0.45, ease: EASE }}>
            <form onSubmit={(e) => { e.preventDefault(); close(); router.push(`/shop?q=${encodeURIComponent(q)}`); }}
              className="flex items-center gap-3 border-b border-paper/30 pb-4">
              <Search size={22} className="text-silver" />
              <input ref={input} value={q} onChange={(e) => setQ(e.target.value)} placeholder={t.shop.search}
                className="w-full bg-transparent font-display text-3xl uppercase tracking-wide outline-none placeholder:text-paper/25 md:text-4xl" aria-label={t.nav.search} />
              <button type="button" onClick={close} className="grid h-10 w-10 shrink-0 place-items-center rounded-full border border-paper/20" aria-label={t.nav.close}><X size={18} /></button>
            </form>
            <ul className="mt-6 grid gap-2">
              {results.map((p) => (
                <li key={p.slug}>
                  <Link href={`/product/${p.slug}`} onClick={close} className="group flex items-center gap-4 rounded-md p-2 hover:bg-paper/5">
                    <span className="relative aspect-[1/1.414] w-12 shrink-0 overflow-hidden rounded-[2px] bg-graphite">
                      <Image src={imageOf(p.slug)} alt="" fill sizes="48px" className="object-cover" />
                    </span>
                    <span className="min-w-0 flex-1">
                      <span className="block truncate font-semibold" dir="auto">{p.name}</span>
                      <span className="block text-xs text-silver">{l(vibeBySlug(p.vibe)!.name)}</span>
                    </span>
                    <span className="text-sm font-semibold tabular-nums">{mad(p.price)}</span>
                  </Link>
                </li>
              ))}
              {results.length === 0 && <li className="py-6 text-center text-silver">{t.shop.empty}</li>}
            </ul>
            <div className="mt-6 flex justify-center">
              <Magnetic href={`/shop${q ? `?q=${encodeURIComponent(q)}` : ""}`} onClick={close} variant="ghost" className="!py-3 text-xs">{t.featured.viewAll}</Magnetic>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
