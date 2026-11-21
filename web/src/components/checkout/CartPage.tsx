"use client";

import { ArrowRight, Trash2 } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { STORE } from "@/lib/config";
import { useMounted } from "@/lib/hooks";
import { useLang } from "@/lib/i18n";
import { totals } from "@/lib/order";
import { imageOf } from "@/lib/products";
import { useStore } from "@/lib/store";
import { PageHeader, QtyStepper } from "../ui/bits";
import { Magnetic } from "../ui/motion";

export function CartPage() {
  const { t, mad } = useLang();
  const items = useStore((s) => s.items);
  const setQty = useStore((s) => s.setQty);
  const remove = useStore((s) => s.remove);
  const mounted = useMounted();
  const tt = totals(mounted ? items : []);

  return (
    <>
      <PageHeader eyebrow={t.nav.cart} title={t.cart.title} sub={mounted && tt.count ? t.cart.items(tt.count) : undefined} />
      <section className="mx-auto max-w-[1440px] px-5 pb-28 md:px-10">
        {!mounted ? <div className="min-h-[30svh]" /> : tt.lines.length === 0 ? (
          <div className="rounded-md border border-dashed border-paper/20 py-24 text-center">
            <p className="font-serif text-3xl italic">{t.cart.empty}</p>
            <div className="mt-8"><Magnetic href="/shop">{t.cart.emptyCta}</Magnetic></div>
          </div>
        ) : (
          <div className="grid gap-12 lg:grid-cols-12">
            <ul className="divide-y divide-paper/10 border-y border-paper/10 lg:col-span-8">
              {tt.lines.map((ln) => (
                <li key={ln.slug} className="flex gap-5 py-6">
                  <Link href={`/product/${ln.slug}`} className="relative aspect-[1/1.414] w-24 shrink-0 overflow-hidden rounded-[2px] bg-graphite md:w-28">
                    <Image src={imageOf(ln.slug)} alt={ln.name} fill sizes="112px" className="object-cover" />
                  </Link>
                  <div className="flex flex-1 flex-col">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <Link href={`/product/${ln.slug}`} className="font-semibold hover:text-accent" dir="auto">{ln.name}</Link>
                        <p className="mt-1 text-sm text-silver">{ln.type === "poster" ? t.product.poster : t.product.sticker}</p>
                      </div>
                      <p className="font-semibold tabular-nums">{mad(ln.total)}</p>
                    </div>
                    <div className="mt-auto flex items-center justify-between pt-4">
                      <QtyStepper value={ln.qty} onChange={(v) => setQty(ln.slug, v)} size="sm" label={t.product.qty} />
                      <button onClick={() => remove(ln.slug)} className="flex items-center gap-1.5 text-sm text-silver hover:text-accent"><Trash2 size={14} /> {t.cart.remove}</button>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
            <aside className="h-fit rounded-md bg-paper p-7 text-ink lg:col-span-4 lg:sticky lg:top-28">
              <div className="flex justify-between text-lg font-semibold"><span>{t.cart.subtotal}</span><span className="tabular-nums">{mad(tt.subtotal)}</span></div>
              <p className="mt-2 text-sm text-ink/60">{t.cart.deliveryNote}</p>
              <p className="mt-4 text-sm font-medium">{tt.free ? t.cart.freeReached : t.cart.freeLeft(mad(tt.missingForFree))}</p>
              <div className="mt-2 h-1 overflow-hidden rounded-full bg-ink/10"><div className="h-full bg-accent transition-all" style={{ width: `${Math.min(100, (tt.subtotal / STORE.freeShippingFrom) * 100)}%` }} /></div>
              <Link href="/checkout" className="mt-7 flex items-center justify-center gap-2 rounded-full bg-accent py-4 text-sm font-semibold text-white hover:bg-[#ff5247]">
                {t.cart.checkout} <ArrowRight size={16} className="rtl:rotate-180" />
              </Link>
              <Link href="/shop" className="mt-3 block text-center text-sm underline-offset-4 hover:underline">{t.cart.continue}</Link>
            </aside>
          </div>
        )}
      </section>
    </>
  );
}
