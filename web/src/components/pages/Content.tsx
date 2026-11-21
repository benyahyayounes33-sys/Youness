"use client";

import { AnimatePresence, motion } from "framer-motion";
import { Mail, Plus } from "lucide-react";
import Image from "next/image";
import { useState } from "react";
import { DELIVERY_ZONES, OTHER_ZONE, STORE } from "@/lib/config";
import { useLang } from "@/lib/i18n";
import { whatsappUrl } from "@/lib/order";
import { InstagramIcon, PageHeader, TikTokIcon, WhatsAppIcon } from "../ui/bits";
import { EASE, Reveal } from "../ui/motion";

export function AboutView() {
  const { t } = useLang();
  const a = t.pages.about;
  return (
    <>
      <PageHeader eyebrow={a.eyebrow} title={a.title} />
      <section className="mx-auto grid max-w-[1440px] gap-12 px-5 pb-24 md:px-10 lg:grid-cols-12">
        <Reveal className="relative aspect-[16/11] overflow-hidden rounded-md lg:col-span-7">
          <Image src="/scenes/room-after.jpg" alt="" fill sizes="(min-width:1024px) 60vw, 100vw" className="object-cover" />
        </Reveal>
        <div className="space-y-6 text-lg leading-relaxed text-paper/80 lg:col-span-5">
          {a.paras.map((p, i) => <Reveal key={i} delay={i * 0.08}><p>{p}</p></Reveal>)}
        </div>
      </section>
      <section className="border-t border-paper/10">
        <div className="mx-auto grid max-w-[1440px] px-5 md:grid-cols-3 md:px-10">
          {a.values.map((v, i) => (
            <Reveal key={v.t} delay={i * 0.08} className="border-b border-paper/10 py-12 md:border-b-0 md:border-e md:px-8 md:last:border-e-0">
              <span dir="ltr" className="font-display text-6xl text-paper/10">0{i + 1}</span>
              <h2 className="mt-3 font-display text-4xl uppercase">{v.t}</h2>
              <p className="mt-2 text-silver">{v.d}</p>
            </Reveal>
          ))}
        </div>
      </section>
    </>
  );
}

export function ContactView() {
  const { t } = useLang();
  const c = t.pages.contact;
  const [name, setName] = useState("");
  const [msg, setMsg] = useState("");
  return (
    <>
      <PageHeader eyebrow={c.eyebrow} title={c.title} sub={c.sub} />
      <section className="mx-auto grid max-w-[1440px] gap-8 px-5 pb-28 md:px-10 lg:grid-cols-12">
        <div className="space-y-4 lg:col-span-5">
          <a href={whatsappUrl(`Bonjour ${STORE.name} !`)} target="_blank" rel="noreferrer"
            className="flex items-center justify-between rounded-2xl bg-[#25d366] p-7 text-ink transition-transform hover:-translate-y-1">
            <span className="font-display text-3xl uppercase">{c.whatsapp}</span><WhatsAppIcon size={30} />
          </a>
          <a href={`mailto:${STORE.email}`} className="flex items-center justify-between rounded-2xl border border-paper/12 p-7 hover:border-paper/40">
            <span><span className="block text-[11px] font-semibold uppercase tracking-[0.22em] text-silver">{c.email}</span><span className="mt-1 block text-lg">{STORE.email}</span></span><Mail />
          </a>
          <div className="flex gap-3 rounded-2xl border border-paper/12 p-7">
            <span className="me-auto text-[11px] font-semibold uppercase tracking-[0.22em] text-silver">{c.social}</span>
            <a href={STORE.instagram} target="_blank" rel="noreferrer" aria-label="Instagram"><InstagramIcon size={24} /></a>
            <a href={STORE.tiktok} target="_blank" rel="noreferrer" aria-label="TikTok"><TikTokIcon size={24} /></a>
          </div>
        </div>
        <form className="rounded-2xl bg-paper p-6 text-ink md:p-8 lg:col-span-7"
          onSubmit={(e) => { e.preventDefault(); window.open(whatsappUrl(`${name ? `${name} — ` : ""}${msg}`), "_blank", "noopener"); }}>
          <h2 className="font-display text-3xl uppercase">{c.formTitle}</h2>
          <label htmlFor="cname" className="mb-2 mt-6 block text-sm font-semibold">{c.name}</label>
          <input id="cname" value={name} onChange={(e) => setName(e.target.value)} className="w-full rounded-xl border border-ink/15 bg-white px-4 py-3.5 outline-none focus:border-ink" />
          <label htmlFor="cmsg" className="mb-2 mt-5 block text-sm font-semibold">{c.message}</label>
          <textarea id="cmsg" required rows={5} value={msg} onChange={(e) => setMsg(e.target.value)} className="w-full resize-none rounded-xl border border-ink/15 bg-white px-4 py-3.5 outline-none focus:border-ink" />
          <button className="mt-6 flex items-center gap-2 rounded-full bg-ink px-7 py-4 text-sm font-semibold text-paper hover:bg-accent"><WhatsAppIcon /> {c.send}</button>
          <p className="mt-4 text-xs text-ink/55">{c.honest}</p>
        </form>
      </section>
    </>
  );
}

export function FaqView() {
  const { t } = useLang();
  const f = t.pages.faq;
  const [open, setOpen] = useState<number | null>(0);
  return (
    <>
      <PageHeader eyebrow={f.eyebrow} title={f.title} />
      <section className="mx-auto max-w-4xl px-5 pb-28 md:px-10">
        <ul className="border-t border-paper/12">
          {f.items.map((it, i) => (
            <li key={it.q} className="border-b border-paper/12">
              <button onClick={() => setOpen(open === i ? null : i)} aria-expanded={open === i} className="flex w-full items-center justify-between gap-6 py-6 text-start text-lg font-semibold md:text-xl">
                {it.q}
                <Plus size={20} className={`shrink-0 transition-transform duration-500 ${open === i ? "rotate-45 text-accent" : ""}`} />
              </button>
              <AnimatePresence initial={false}>
                {open === i && (
                  <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.45, ease: EASE }} className="overflow-hidden">
                    <p className="max-w-2xl pb-7 leading-relaxed text-paper/75">{it.a}</p>
                  </motion.div>
                )}
              </AnimatePresence>
            </li>
          ))}
        </ul>
      </section>
    </>
  );
}

export function ShippingView() {
  const { t, lang, mad } = useLang();
  const s = t.pages.shipping;
  return (
    <>
      <PageHeader eyebrow={s.eyebrow} title={s.title} sub={s.free} />
      <section className="mx-auto max-w-[1440px] px-5 pb-28 md:px-10">
        <div className="overflow-x-auto rounded-2xl border border-paper/12">
          <table className="w-full min-w-[560px] text-start text-sm">
            <thead className="bg-paper/[0.04] text-[11px] uppercase tracking-[0.2em] text-silver">
              <tr><th className="p-5 text-start">{s.tableCity}</th><th className="p-5 text-start">{s.tableFee}</th><th className="p-5 text-start">{s.tableEta}</th></tr>
            </thead>
            <tbody className="divide-y divide-paper/10">
              {[...DELIVERY_ZONES, { ...OTHER_ZONE, cities: [s.other] }].map((z) => (
                <tr key={z.id}>
                  <td className="p-5 leading-relaxed">{z.cities.join(", ")}</td>
                  <td className="whitespace-nowrap p-5 font-semibold tabular-nums">{mad(z.fee)}</td>
                  <td className="whitespace-nowrap p-5 text-silver">{z.eta[lang]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <h2 className="mt-20 font-display text-4xl uppercase">{s.returnsTitle}</h2>
        <ul className="mt-6 max-w-3xl space-y-4">
          {s.returns.map((r) => <li key={r} className="flex gap-4 leading-relaxed text-paper/80"><span className="mt-2.5 h-1.5 w-1.5 shrink-0 rounded-full bg-accent" />{r}</li>)}
        </ul>
      </section>
    </>
  );
}

export function LegalView({ which }: { which: "privacy" | "terms" }) {
  const { t } = useLang();
  const d = t.pages[which];
  return (
    <>
      <PageHeader eyebrow={d.eyebrow} title={d.title} />
      <section className="mx-auto max-w-3xl px-5 pb-28 md:px-10">
        {d.sections.map((s, i) => (
          <div key={s.h} className="border-t border-paper/12 py-8">
            <h2 className="flex gap-4 font-display text-2xl uppercase"><span dir="ltr" className="text-accent">{String(i + 1).padStart(2, "0")}</span>{s.h}</h2>
            <p className="mt-3 leading-relaxed text-paper/75">{s.p}</p>
          </div>
        ))}
      </section>
    </>
  );
}
