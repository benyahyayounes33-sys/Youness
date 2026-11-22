"use client";

import { Check, Copy, PackageSearch } from "lucide-react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import clsx from "clsx";
import { useLang } from "@/lib/i18n";
import { findLocalOrder, getLocalOrders, whatsappMessage, whatsappUrl, type Order } from "@/lib/order";
import { PageHeader, WhatsAppIcon } from "../ui/bits";
import { Magnetic, Reveal } from "../ui/motion";

function Summary({ o }: { o: Order }) {
  const { t, mad } = useLang();
  return (
    <dl className="space-y-2 text-sm">
      {o.lines.map((l) => (
        <div key={l.slug} className="flex justify-between gap-4"><dt dir="auto">{l.name} × {l.qty}</dt><dd className="tabular-nums">{mad(l.total)}</dd></div>
      ))}
      <div className="flex justify-between border-t border-ink/10 pt-2 text-ink/60"><dt>{t.checkout.deliveryFee} · {o.customer.city}</dt><dd className="tabular-nums">{o.delivery === 0 ? t.checkout.free : mad(o.delivery)}</dd></div>
      <div className="flex justify-between text-base font-semibold"><dt>{t.checkout.total}</dt><dd className="tabular-nums">{mad(o.total)}</dd></div>
    </dl>
  );
}

export function OrderConfirmation() {
  const { t } = useLang();
  const sp = useSearchParams();
  const [order, setOrder] = useState<Order | null | undefined>(undefined);
  const [copied, setCopied] = useState(false);
  useEffect(() => setOrder(findLocalOrder(sp.get("ref") ?? "") ?? null), [sp]);

  if (order === undefined) return <div className="min-h-[70svh]" />;
  if (!order) {
    return (
      <>
        <PageHeader eyebrow={t.order.ref} title={t.order.missing} />
        <div className="mx-auto max-w-[1440px] px-5 pb-28 md:px-10"><Magnetic href="/shop">{t.order.backShop}</Magnetic></div>
      </>
    );
  }
  const msg = whatsappMessage(order);
  return (
    <>
      <PageHeader eyebrow={`${t.order.ref} · ${order.ref}`} title={t.order.title} sub={t.order.lead} />
      <section className="mx-auto grid max-w-[1440px] gap-8 px-5 pb-28 md:px-10 lg:grid-cols-12">
        <Reveal className="lg:col-span-7">
          <div className="rounded-2xl bg-paper p-6 text-ink md:p-8">
            <span className="inline-flex items-center gap-2 rounded-full bg-accent/10 px-3 py-1 text-xs font-semibold text-accent">
              <span className="h-2 w-2 animate-pulse rounded-full bg-accent motion-reduce:animate-none" /> {t.order.status}
            </span>
            <a href={whatsappUrl(msg)} target="_blank" rel="noreferrer"
              className="mt-6 flex w-full items-center justify-center gap-3 rounded-full bg-[#25d366] py-5 text-base font-bold text-ink hover:bg-[#3ee07b]">
              <WhatsAppIcon size={22} /> {t.order.send}
            </a>
            <button onClick={async () => { await navigator.clipboard.writeText(msg); setCopied(true); setTimeout(() => setCopied(false), 1800); }}
              className="mt-3 flex w-full items-center justify-center gap-2 rounded-full border border-ink/15 py-3.5 text-sm font-semibold hover:bg-ink hover:text-paper">
              {copied ? <Check size={16} /> : <Copy size={16} />} {copied ? t.order.copied : t.order.copy}
            </button>
            <p className="mt-5 text-xs text-ink/55">{t.order.local}</p>
          </div>
          <div className="mt-6 rounded-2xl border border-paper/12 p-6 md:p-8">
            <h2 className="text-[11px] font-semibold uppercase tracking-[0.22em] text-silver">{t.order.preview}</h2>
            <pre className="mt-4 whitespace-pre-wrap break-words font-sans text-sm leading-relaxed text-paper/80" dir="ltr">{msg}</pre>
          </div>
        </Reveal>
        <Reveal delay={0.1} className="lg:col-span-5">
          <div className="rounded-2xl bg-paper p-6 text-ink md:p-8 lg:sticky lg:top-28">
            <h2 className="font-display text-2xl uppercase">{t.order.details}</h2>
            <p className="mt-4 text-sm">{order.customer.name} · <span dir="ltr">{order.customer.phone}</span></p>
            <p className="mt-1 text-sm text-ink/60">{order.customer.address}, {order.customer.city}</p>
            <div className="mt-6"><Summary o={order} /></div>
            <Link href="/shop" className="mt-8 block text-center text-sm underline underline-offset-4">{t.order.backShop}</Link>
          </div>
        </Reveal>
      </section>
    </>
  );
}

export function TrackOrder() {
  const { t } = useLang();
  const [ref, setRef] = useState("");
  const [phone, setPhone] = useState("");
  const [result, setResult] = useState<Order | null | undefined>(undefined);
  const [mine, setMine] = useState<Order[]>([]);
  useEffect(() => setMine(getLocalOrders()), []);

  return (
    <>
      <PageHeader eyebrow={t.nav.track} title={t.track.title} sub={t.track.sub} />
      <section className="mx-auto grid max-w-[1440px] gap-8 px-5 pb-28 md:px-10 lg:grid-cols-12">
        <div className="lg:col-span-6">
          <form onSubmit={(e) => { e.preventDefault(); setResult(findLocalOrder(ref, phone) ?? null); }} className="rounded-2xl bg-paper p-6 text-ink md:p-8">
            <label htmlFor="ref" className="mb-2 block text-sm font-semibold">{t.track.ref}</label>
            <input id="ref" value={ref} onChange={(e) => setRef(e.target.value)} placeholder="OL-261121-AB12" dir="ltr"
              className="w-full rounded-xl border border-ink/15 bg-white px-4 py-3.5 uppercase outline-none focus:border-ink" required />
            <label htmlFor="tphone" className="mb-2 mt-5 block text-sm font-semibold">{t.track.phone}</label>
            <input id="tphone" type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="06 12 34 56 78" dir="ltr"
              className="w-full rounded-xl border border-ink/15 bg-white px-4 py-3.5 outline-none focus:border-ink" required />
            <button className="mt-6 flex w-full items-center justify-center gap-2 rounded-full bg-ink py-4 text-sm font-semibold text-paper hover:bg-accent">
              <PackageSearch size={17} /> {t.track.search}
            </button>
            <p className="mt-4 text-xs leading-relaxed text-ink/55">{t.track.honest}</p>
          </form>
        </div>
        <div className="lg:col-span-6">
          {result === null && <p className="rounded-2xl border border-dashed border-paper/25 p-6 text-silver" role="status">{t.track.notFound}</p>}
          {result && (
            <div className="rounded-2xl border border-paper/12 p-6 md:p-8" role="status">
              <p className="text-[11px] font-semibold uppercase tracking-[0.22em] text-silver">{t.track.ref} · <span dir="ltr">{result.ref}</span></p>
              <ol className="mt-6 space-y-4">
                {t.track.steps.map((s, i) => (
                  <li key={s} className="flex items-center gap-4">
                    <span className={clsx("grid h-8 w-8 place-items-center rounded-full border text-xs", i === 0 ? "border-accent bg-accent text-white" : "border-paper/20 text-silver")}>
                      {i === 0 ? <Check size={14} /> : i + 1}
                    </span>
                    <span className={i === 0 ? "font-semibold" : "text-silver"}>{s}</span>
                  </li>
                ))}
              </ol>
              <p className="mt-6 text-sm text-silver">{t.track.unknown}</p>
              <a href={whatsappUrl(t.track.askMsg(result.ref))} target="_blank" rel="noreferrer"
                className="mt-5 inline-flex items-center gap-2 rounded-full bg-[#25d366] px-6 py-3.5 text-sm font-bold text-ink hover:bg-[#3ee07b]">
                <WhatsAppIcon /> {t.track.ask}
              </a>
            </div>
          )}
          {mine.length > 0 && (
            <div className="mt-8">
              <h2 className="text-[11px] font-semibold uppercase tracking-[0.22em] text-silver">{t.track.device}</h2>
              <ul className="mt-4 divide-y divide-paper/10 border-y border-paper/10">
                {mine.map((o) => (
                  <li key={o.ref}>
                    <Link href={`/order?ref=${o.ref}`} className="flex justify-between py-4 text-sm hover:text-accent">
                      <span dir="ltr">{o.ref}</span><span>{new Date(o.createdAt).toLocaleDateString("fr-MA")}</span>
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </section>
    </>
  );
}
