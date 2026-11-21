"use client";

import Link from "next/link";
import { Mail, Phone } from "lucide-react";
import { STORE } from "@/lib/config";
import { whatsappUrl } from "@/lib/order";
import { useLang } from "@/lib/i18n";
import { InstagramIcon, TikTokIcon, WhatsAppIcon } from "../ui/bits";

export function Footer() {
  const { t } = useLang();
  const f = t.footer;
  const cols = [
    { h: f.shop, links: [["/shop", f.links.all], ["/shop?sort=popular", f.links.best], ["/shop?type=sticker", f.links.stickers], ["/about", f.links.about]] },
    { h: f.help, links: [["/faq", f.links.faq], ["/shipping", f.links.shipping], ["/track", f.links.track], ["/contact", f.links.contact]] },
    { h: f.legal, links: [["/privacy", f.links.privacy], ["/terms", f.links.terms]] },
  ];
  return (
    <footer className="relative overflow-hidden border-t border-paper/10 bg-ink pt-20">
      <div className="mx-auto grid max-w-[1440px] gap-12 px-5 md:grid-cols-12 md:px-10">
        <div className="md:col-span-4">
          <p className="max-w-xs font-serif text-3xl italic leading-tight text-paper/90">{STORE.tagline}</p>
          <div className="mt-8 flex gap-2">
            <a href={STORE.instagram} target="_blank" rel="noreferrer" aria-label="Instagram" className="grid h-11 w-11 place-items-center rounded-full border border-paper/15 hover:border-paper hover:bg-paper hover:text-ink"><InstagramIcon /></a>
            <a href={STORE.tiktok} target="_blank" rel="noreferrer" aria-label="TikTok" className="grid h-11 w-11 place-items-center rounded-full border border-paper/15 hover:border-paper hover:bg-paper hover:text-ink"><TikTokIcon /></a>
            <a href={whatsappUrl("Bonjour ONELINE !")} target="_blank" rel="noreferrer" aria-label="WhatsApp" className="grid h-11 w-11 place-items-center rounded-full border border-paper/15 hover:border-[#25d366] hover:bg-[#25d366] hover:text-ink"><WhatsAppIcon /></a>
          </div>
          <ul className="mt-8 space-y-2 text-sm text-silver">
            <li className="flex items-center gap-2"><Phone size={14} /> <span dir="ltr">{STORE.phoneDisplay}</span></li>
            <li className="flex items-center gap-2"><Mail size={14} /> {STORE.email}</li>
          </ul>
        </div>
        {cols.map((c) => (
          <div key={c.h} className="md:col-span-2">
            <h3 className="text-[11px] font-semibold uppercase tracking-[0.24em] text-silver">{c.h}</h3>
            <ul className="mt-5 space-y-3">
              {c.links.map(([href, label]) => (
                <li key={href}><Link href={href} className="text-sm text-paper/80 transition-colors hover:text-accent">{label}</Link></li>
              ))}
            </ul>
          </div>
        ))}
        <div className="md:col-span-2">
          <h3 className="text-[11px] font-semibold uppercase tracking-[0.24em] text-silver">COD</h3>
          <p className="mt-5 text-sm leading-relaxed text-paper/70">{f.delivery}</p>
        </div>
      </div>
      <div className="mx-auto mt-16 max-w-[1440px] px-5 md:px-10">
        <p dir="ltr" aria-hidden className="select-none font-display text-[22vw] leading-[0.78] tracking-tight text-paper/[0.06] md:text-[19vw]">
          ONELINE<span className="text-accent/40">.</span>
        </p>
      </div>
      <div className="mx-auto flex max-w-[1440px] flex-col gap-2 border-t border-paper/10 px-5 py-6 text-xs text-silver md:flex-row md:justify-between md:px-10">
        <p>© {new Date().getFullYear()} {STORE.name}. {f.rights}</p>
        {STORE.isDemo && <p>{f.demo}</p>}
      </div>
    </footer>
  );
}
