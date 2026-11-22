"use client";

import { useLang } from "@/lib/i18n";
import { Magnetic } from "@/components/ui/motion";

export default function NotFound() {
  const { t } = useLang();
  return (
    <section className="mx-auto grid min-h-[75svh] max-w-[1440px] place-items-center px-5 text-center">
      <div>
        <p dir="ltr" className="font-display text-[28vw] leading-none text-paper/[0.07] md:text-[16vw]">404</p>
        <h1 className="-mt-[8vw] font-display text-5xl uppercase md:text-7xl">{t.common.notFoundTitle}</h1>
        <p className="mt-4 text-silver">{t.common.notFoundSub}</p>
        <div className="mt-10"><Magnetic href="/">{t.common.backHome}</Magnetic></div>
      </div>
    </section>
  );
}
