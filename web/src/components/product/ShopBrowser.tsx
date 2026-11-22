"use client";

import { Heart, Search, X } from "lucide-react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import clsx from "clsx";
import { useMounted } from "@/lib/hooks";
import { useLang } from "@/lib/i18n";
import { PRODUCTS, VIBES, vibeBySlug, type VibeSlug } from "@/lib/products";
import { useStore } from "@/lib/store";
import { ProductCard } from "./ProductCard";

const norm = (s: string) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
type Sort = "popular" | "priceAsc" | "priceDesc" | "newest" | "name";

export function ShopBrowser({ lockedVibe }: { lockedVibe?: VibeSlug }) {
  const { t, l } = useLang();
  const router = useRouter();
  const pathname = usePathname();
  const sp = useSearchParams();
  const favorites = useStore((s) => s.favorites);
  const mounted = useMounted();

  const q = sp.get("q") ?? "";
  const vibe = (lockedVibe ?? sp.get("vibe") ?? "") as VibeSlug | "";
  const type = (sp.get("type") ?? "") as "" | "poster" | "sticker";
  const sort = (sp.get("sort") ?? "popular") as Sort;
  const fav = sp.get("fav") === "1";

  const set = (k: string, v: string) => {
    const next = new URLSearchParams(sp.toString());
    if (v) next.set(k, v);
    else next.delete(k);
    router.replace(`${pathname}${next.toString() ? `?${next}` : ""}`, { scroll: false });
  };

  const [query, setQuery] = useState(q);
  useEffect(() => setQuery(q), [q]);
  useEffect(() => {
    if (query === q) return;
    const id = setTimeout(() => set("q", query), 250);
    return () => clearTimeout(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [query]);

  const list = useMemo(() => {
    const n = norm(query.trim());
    const out = PRODUCTS.filter((p) =>
      (!vibe || p.vibe === vibe) && (!type || p.type === type) && (!fav || (mounted && favorites.includes(p.slug))) &&
      (!n || norm(`${p.name} ${l(vibeBySlug(p.vibe)!.name)} ${p.desc.fr} ${p.desc.ar}`).includes(n)));
    const by: Record<Sort, (a: (typeof out)[number], b: (typeof out)[number]) => number> = {
      popular: (a, b) => b.popularity - a.popularity,
      priceAsc: (a, b) => a.price - b.price || b.popularity - a.popularity,
      priceDesc: (a, b) => b.price - a.price || b.popularity - a.popularity,
      newest: (a, b) => b.added - a.added,
      name: (a, b) => a.name.localeCompare(b.name, "fr"),
    };
    return out.sort(by[sort] ?? by.popular);
  }, [query, vibe, type, fav, sort, favorites, mounted, l]);

  const filtered = !!(query || (!lockedVibe && vibe) || type || fav);

  return (
    <div className="mx-auto max-w-[1440px] px-5 pb-28 md:px-10">
      <div className="sticky top-16 z-20 -mx-5 border-y border-paper/10 bg-ink/85 px-5 py-4 backdrop-blur-xl md:top-20 md:-mx-10 md:px-10">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center">
          <label className="flex flex-1 items-center gap-3 rounded-full border border-paper/15 px-4 py-2.5 focus-within:border-paper/50">
            <Search size={16} className="text-silver" />
            <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder={t.shop.search} aria-label={t.shop.search}
              className="w-full bg-transparent text-sm outline-none placeholder:text-paper/35" />
            {query && <button onClick={() => { setQuery(""); set("q", ""); }} aria-label={t.shop.reset}><X size={15} /></button>}
          </label>
          <div className="flex flex-wrap items-center gap-2">
            <select value={type} onChange={(e) => set("type", e.target.value)} aria-label={t.shop.type.label}
              className="rounded-full border border-paper/15 bg-ink px-4 py-2.5 text-sm outline-none focus:border-paper/50">
              <option value="">{t.shop.type.label} · {t.shop.type.all}</option>
              <option value="poster">{t.shop.type.poster}</option>
              <option value="sticker">{t.shop.type.sticker}</option>
            </select>
            <select value={sort} onChange={(e) => set("sort", e.target.value === "popular" ? "" : e.target.value)} aria-label={t.shop.sort.label}
              className="rounded-full border border-paper/15 bg-ink px-4 py-2.5 text-sm outline-none focus:border-paper/50">
              {(["popular", "newest", "priceAsc", "priceDesc", "name"] as Sort[]).map((k) => <option key={k} value={k}>{t.shop.sort.label} · {t.shop.sort[k]}</option>)}
            </select>
            <button onClick={() => set("fav", fav ? "" : "1")} aria-pressed={fav}
              className={clsx("flex items-center gap-2 rounded-full border px-4 py-2.5 text-sm transition-colors", fav ? "border-accent bg-accent text-white" : "border-paper/15 hover:border-paper/50")}>
              <Heart size={14} fill={fav ? "currentColor" : "none"} /> {t.shop.favOnly}
            </button>
          </div>
        </div>
        {!lockedVibe && (
          <div className="no-scrollbar -mx-5 mt-4 flex gap-2 overflow-x-auto px-5 md:mx-0 md:px-0">
            {[{ slug: "", label: t.shop.all }, ...VIBES.map((v) => ({ slug: v.slug, label: l(v.name) }))].map((c) => (
              <button key={c.slug || "all"} onClick={() => set("vibe", c.slug)} aria-pressed={vibe === c.slug}
                className={clsx("shrink-0 rounded-full px-4 py-2 text-xs font-semibold transition-colors",
                  vibe === c.slug ? "bg-paper text-ink" : "bg-paper/[0.06] text-paper/75 hover:bg-paper/15")}>
                {c.label}
              </button>
            ))}
          </div>
        )}
      </div>
      <div className="mt-8 flex items-center justify-between text-sm text-silver">
        <p aria-live="polite">{t.shop.results(list.length)}</p>
        {filtered && <button onClick={() => router.replace(pathname, { scroll: false })} className="underline underline-offset-4 hover:text-paper">{t.shop.reset}</button>}
      </div>
      {list.length > 0 ? (
        <div className="mt-8 grid grid-cols-2 gap-x-4 gap-y-10 md:grid-cols-3 md:gap-x-6 xl:grid-cols-4">
          {list.map((p, i) => <ProductCard key={p.slug} p={p} index={i} priority={i < 4} />)}
        </div>
      ) : (
        <div className="py-28 text-center">
          <p className="font-serif text-3xl italic">{t.shop.empty}</p>
          <button onClick={() => router.replace(pathname, { scroll: false })} className="mt-6 rounded-full border border-paper/25 px-6 py-3 text-sm font-semibold hover:bg-paper hover:text-ink">{t.shop.reset}</button>
        </div>
      )}
    </div>
  );
}
