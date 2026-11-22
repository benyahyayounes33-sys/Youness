"use client";

import { Banknote, Lock, ShieldCheck } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useMemo, useState } from "react";
import clsx from "clsx";
import { ALL_CITIES, DELIVERY_ZONES } from "@/lib/config";
import { useMounted } from "@/lib/hooks";
import { useLang } from "@/lib/i18n";
import { buildOrder, saveLocalOrder, totals, validate, type CheckoutForm } from "@/lib/order";
import { imageOf } from "@/lib/products";
import { useStore } from "@/lib/store";
import { PageHeader, QtyStepper, WhatsAppIcon } from "../ui/bits";
import { Magnetic } from "../ui/motion";

const EMPTY: CheckoutForm = { name: "", phone: "", city: "", otherCity: "", address: "", note: "" };

function Field({ label, error, children, hint, id }: { label: string; error?: string; children: React.ReactNode; hint?: string; id: string }) {
  return (
    <div>
      <label htmlFor={id} className="mb-2 block text-sm font-semibold">{label}</label>
      {children}
      {error ? <p id={`${id}-err`} className="mt-1.5 text-sm text-accent" role="alert">{error}</p>
        : hint ? <p className="mt-1.5 text-xs text-ink/50">{hint}</p> : null}
    </div>
  );
}

const input = (bad?: boolean) =>
  clsx("w-full rounded-xl border bg-white px-4 py-3.5 text-base text-ink outline-none transition-colors placeholder:text-ink/35 focus:border-ink",
    bad ? "border-accent" : "border-ink/15");

export function Checkout() {
  const { t, mad, lang } = useLang();
  const router = useRouter();
  const items = useStore((s) => s.items);
  const setQty = useStore((s) => s.setQty);
  const clear = useStore((s) => s.clear);
  const mounted = useMounted();
  const [f, setF] = useState<CheckoutForm>(EMPTY);
  const [submitted, setSubmitted] = useState(false);
  const [busy, setBusy] = useState(false);

  const cityName = f.city === "__other" ? (f.otherCity.trim() || "__other") : f.city;
  const tt = totals(mounted ? items : [], cityName || undefined);
  const errors = useMemo(() => validate(f, tt.count), [f, tt.count]);
  const show = (k: keyof typeof errors) => (submitted && errors[k] ? t.checkout.errors[errors[k]!] : undefined);
  const up = (k: keyof CheckoutForm) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) =>
    setF((s) => ({ ...s, [k]: e.target.value }));

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    if (Object.keys(errors).length) {
      const first = document.querySelector<HTMLElement>("[aria-invalid='true']");
      first?.focus();
      return;
    }
    setBusy(true);
    const order = buildOrder(f, items);
    saveLocalOrder(order);
    clear();
    router.push(`/order?ref=${order.ref}`);
  };

  if (mounted && tt.count === 0 && !busy) {
    return (
      <>
        <PageHeader eyebrow={t.checkout.title} title={t.cart.empty} />
        <div className="mx-auto max-w-[1440px] px-5 pb-28 md:px-10"><Magnetic href="/shop">{t.cart.emptyCta}</Magnetic></div>
      </>
    );
  }

  return (
    <>
      <PageHeader eyebrow={t.checkout.title} title={t.checkout.title} sub={t.checkout.sub} />
      <form onSubmit={submit} noValidate className="mx-auto grid max-w-[1440px] gap-8 px-5 pb-28 md:px-10 lg:grid-cols-12">
        <div className="space-y-6 lg:col-span-7">
          <fieldset className="rounded-2xl bg-paper p-6 text-ink md:p-8">
            <legend className="sr-only">{t.checkout.contact}</legend>
            <h2 className="flex items-baseline gap-3 font-display text-2xl uppercase"><span className="text-accent" dir="ltr">01</span>{t.checkout.contact}</h2>
            <div className="mt-6 grid gap-5 md:grid-cols-2">
              <Field id="name" label={t.checkout.name} error={show("name")}>
                <input id="name" autoComplete="name" value={f.name} onChange={up("name")} className={input(!!show("name"))} aria-invalid={!!show("name")} />
              </Field>
              <Field id="phone" label={t.checkout.phone} error={show("phone")} hint={t.checkout.phoneHint}>
                <input id="phone" type="tel" inputMode="tel" autoComplete="tel" dir="ltr" placeholder="06 12 34 56 78" value={f.phone} onChange={up("phone")}
                  className={clsx(input(!!show("phone")), lang === "ar" && "text-end")} aria-invalid={!!show("phone")} />
              </Field>
            </div>
          </fieldset>

          <fieldset className="rounded-2xl bg-paper p-6 text-ink md:p-8">
            <legend className="sr-only">{t.checkout.delivery}</legend>
            <h2 className="flex items-baseline gap-3 font-display text-2xl uppercase"><span className="text-accent" dir="ltr">02</span>{t.checkout.delivery}</h2>
            <div className="mt-6 grid gap-5">
              <Field id="city" label={t.checkout.city} error={show("city")}>
                <select id="city" value={f.city} onChange={up("city")} className={input(!!show("city"))} aria-invalid={!!show("city")}>
                  <option value="">{t.checkout.chooseCity}</option>
                  {DELIVERY_ZONES.map((z) => (
                    <optgroup key={z.id} label={`${mad(z.fee)} · ${z.eta[lang]}`}>
                      {z.cities.map((c) => <option key={c} value={c}>{c}</option>)}
                    </optgroup>
                  ))}
                  <option value="__other">{t.checkout.otherCity}</option>
                </select>
              </Field>
              {f.city === "__other" && (
                <Field id="otherCity" label={t.checkout.otherCityName} error={show("city")}>
                  <input id="otherCity" value={f.otherCity} onChange={up("otherCity")} className={input(!!show("city"))} list="cities" />
                  <datalist id="cities">{ALL_CITIES.map((c) => <option key={c} value={c} />)}</datalist>
                </Field>
              )}
              <Field id="address" label={t.checkout.address} error={show("address")} hint={t.checkout.addressHint}>
                <textarea id="address" rows={3} autoComplete="street-address" value={f.address} onChange={up("address")}
                  className={clsx(input(!!show("address")), "resize-none")} aria-invalid={!!show("address")} />
              </Field>
              <Field id="note" label={t.checkout.note}>
                <input id="note" value={f.note} onChange={up("note")} placeholder={t.checkout.notePh} className={input()} />
              </Field>
            </div>
          </fieldset>

          <fieldset className="rounded-2xl bg-paper p-6 text-ink md:p-8">
            <legend className="sr-only">{t.checkout.payment}</legend>
            <h2 className="flex items-baseline gap-3 font-display text-2xl uppercase"><span className="text-accent" dir="ltr">03</span>{t.checkout.payment}</h2>
            <label className="mt-6 flex cursor-pointer items-start gap-4 rounded-xl border-2 border-ink p-5">
              <input type="radio" name="payment" checked readOnly className="mt-1 accent-[#ff3b30]" />
              <span>
                <span className="flex items-center gap-2 font-semibold"><Banknote size={18} /> {t.checkout.cod}</span>
                <span className="mt-1 block text-sm text-ink/60">{t.checkout.codHint}</span>
              </span>
            </label>
          </fieldset>
        </div>

        <aside className="lg:col-span-5">
          <div className="rounded-2xl border border-paper/12 bg-coal p-6 md:p-8 lg:sticky lg:top-28">
            <h2 className="font-display text-2xl uppercase">{t.checkout.summary}</h2>
            <ul className="mt-6 max-h-[38svh] space-y-4 overflow-y-auto pe-1">
              {tt.lines.map((ln) => (
                <li key={ln.slug} className="flex items-center gap-4">
                  <span className="relative aspect-[1/1.414] w-14 shrink-0 overflow-hidden rounded-[2px] bg-graphite">
                    <Image src={imageOf(ln.slug)} alt="" fill sizes="56px" className="object-cover" />
                  </span>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-semibold" dir="auto">{ln.name}</p>
                    <div className="mt-1.5"><QtyStepper size="sm" value={ln.qty} onChange={(v) => setQty(ln.slug, v)} label={t.product.qty} /></div>
                  </div>
                  <p className="text-sm font-semibold tabular-nums">{mad(ln.total)}</p>
                </li>
              ))}
            </ul>
            <dl className="mt-6 space-y-3 border-t border-paper/10 pt-6 text-sm">
              <div className="flex justify-between"><dt className="text-silver">{t.checkout.subtotal}</dt><dd className="tabular-nums">{mad(tt.subtotal)}</dd></div>
              <div className="flex justify-between">
                <dt className="text-silver">{t.checkout.deliveryFee}{tt.zone && cityName !== "__other" ? ` · ${cityName}` : ""}</dt>
                <dd className="tabular-nums">{!f.city ? t.checkout.chooseCityFirst : tt.free ? t.checkout.free : mad(tt.delivery)}</dd>
              </div>
              {tt.zone && <p className="text-xs text-silver">{t.checkout.eta(tt.zone.eta[lang])}</p>}
              {!tt.free && <p className="text-xs text-silver">{t.cart.freeLeft(mad(tt.missingForFree))}</p>}
              <div className="flex items-end justify-between border-t border-paper/10 pt-4">
                <dt className="font-semibold">{t.checkout.total}</dt>
                <dd className="font-display text-4xl tabular-nums">{mad(tt.total)}</dd>
              </div>
            </dl>
            {submitted && errors.cart && <p className="mt-3 text-sm text-accent" role="alert">{t.checkout.errors.empty}</p>}
            <button type="submit" disabled={busy}
              className="mt-7 flex w-full items-center justify-center gap-3 rounded-full bg-[#25d366] py-4 text-sm font-bold text-ink transition-colors hover:bg-[#3ee07b] disabled:opacity-60">
              <WhatsAppIcon size={20} /> {t.checkout.submit}
            </button>
            <p className="mt-4 flex gap-2 text-xs leading-relaxed text-silver"><ShieldCheck size={16} className="shrink-0" /> {t.checkout.honest}</p>
            <p className="mt-2 flex items-center gap-2 text-xs text-silver"><Lock size={14} /> <Link href="/privacy" className="underline underline-offset-2">{t.footer.links.privacy}</Link></p>
          </div>
        </aside>
      </form>
    </>
  );
}
