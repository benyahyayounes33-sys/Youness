"use client";

import { AnimatePresence, motion } from "framer-motion";
import { Heart, Menu, Search, ShoppingBag, X } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import clsx from "clsx";
import { STORE } from "@/lib/config";
import { useCartCount, useMounted, useScrollLock } from "@/lib/hooks";
import { useLang } from "@/lib/i18n";
import { useStore } from "@/lib/store";
import { EASE } from "../ui/motion";
import { Wordmark } from "../ui/bits";

export function Header() {
  const { t, lang, setLang } = useLang();
  const pathname = usePathname();
  const [scrolled, setScrolled] = useState(false);
  const [menu, setMenu] = useState(false);
  const count = useCartCount();
  const favs = useStore((s) => s.favorites.length);
  const mounted = useMounted();
  const setCartOpen = useStore((s) => s.setCartOpen);
  const setSearchOpen = useStore((s) => s.setSearchOpen);
  useScrollLock(menu);

  useEffect(() => {
    const on = () => setScrolled(window.scrollY > 24);
    on();
    window.addEventListener("scroll", on, { passive: true });
    return () => window.removeEventListener("scroll", on);
  }, []);
  useEffect(() => setMenu(false), [pathname]);
  useEffect(() => {
    const k = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setSearchOpen(true);
      }
    };
    window.addEventListener("keydown", k);
    return () => window.removeEventListener("keydown", k);
  }, [setSearchOpen]);

  const links = [
    { href: "/shop", label: t.nav.shop },
    { href: "/#vibes", label: t.nav.vibes },
    { href: "/shop?sort=popular", label: t.nav.best },
    { href: "/about", label: t.nav.about },
  ];

  return (
    <>
      {STORE.isDemo && (
        <div className="relative z-50 bg-accent px-4 py-2 text-center text-[11px] font-semibold tracking-wide text-white">
          {t.announce}
        </div>
      )}
      <header
        className={clsx(
          "sticky top-0 z-40 transition-[background-color,backdrop-filter,border-color] duration-500",
          scrolled || pathname !== "/" ? "border-b border-paper/10 bg-ink/75 backdrop-blur-xl" : "border-b border-transparent",
        )}
      >
        <div className="mx-auto flex h-16 max-w-[1440px] items-center justify-between gap-4 px-5 md:h-20 md:px-10">
          <Link href="/" aria-label={`${STORE.name} — accueil`} className="shrink-0">
            <Wordmark className="text-[26px] md:text-[30px]" />
          </Link>
          <nav className="hidden items-center gap-9 lg:flex" aria-label="Principale">
            {links.map((l) => (
              <Link key={l.href} href={l.href}
                className="group relative text-[13px] font-medium uppercase tracking-[0.16em] text-paper/80 transition-colors hover:text-paper">
                {l.label}
                <span className="absolute -bottom-1.5 start-0 h-px w-0 bg-accent transition-all duration-500 group-hover:w-full" />
              </Link>
            ))}
          </nav>
          <div className="flex items-center gap-1 md:gap-2">
            <button onClick={() => setSearchOpen(true)} className="grid h-10 w-10 place-items-center rounded-full hover:bg-paper/10" aria-label={t.nav.search}>
              <Search size={19} />
            </button>
            <button
              onClick={() => setLang(lang === "fr" ? "ar" : "fr")}
              className="hidden h-10 min-w-10 place-items-center rounded-full px-2 text-[13px] font-semibold hover:bg-paper/10 sm:grid"
              aria-label={t.nav.switchTo} lang={lang === "fr" ? "ar" : "fr"}
            >
              {t.nav.switchShort}
            </button>
            <Link href="/shop?fav=1" className="relative hidden h-10 w-10 place-items-center rounded-full hover:bg-paper/10 sm:grid" aria-label={t.nav.favorites}>
              <Heart size={19} />
              {mounted && favs > 0 && <span className="absolute end-1 top-1 h-2 w-2 rounded-full bg-accent" />}
            </Link>
            <button onClick={() => setCartOpen(true)} className="relative grid h-10 w-10 place-items-center rounded-full hover:bg-paper/10" aria-label={`${t.nav.cart} (${count})`}>
              <ShoppingBag size={19} />
              <AnimatePresence>
                {count > 0 && (
                  <motion.span key={count} initial={{ scale: 0.4, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.4, opacity: 0 }}
                    className="absolute -end-0.5 -top-0.5 grid h-[18px] min-w-[18px] place-items-center rounded-full bg-accent px-1 text-[10px] font-bold text-white tabular-nums">
                    {count}
                  </motion.span>
                )}
              </AnimatePresence>
            </button>
            <button onClick={() => setMenu(true)} className="grid h-10 w-10 place-items-center rounded-full hover:bg-paper/10 lg:hidden" aria-label={t.nav.menu} aria-expanded={menu}>
              <Menu size={21} />
            </button>
          </div>
        </div>
      </header>

      <AnimatePresence>
        {menu && (
          <motion.div className="fixed inset-0 z-[70] flex flex-col bg-ink px-6 pb-10 pt-5" role="dialog" aria-modal="true" aria-label={t.nav.menu}
            initial={{ clipPath: "inset(0 0 100% 0)" }} animate={{ clipPath: "inset(0 0 0% 0)" }} exit={{ clipPath: "inset(0 0 100% 0)" }}
            transition={{ duration: 0.7, ease: EASE }}>
            <div className="flex items-center justify-between">
              <Wordmark className="text-[26px]" />
              <button onClick={() => setMenu(false)} className="grid h-11 w-11 place-items-center rounded-full border border-paper/20" aria-label={t.nav.close}>
                <X size={20} />
              </button>
            </div>
            <nav className="mt-14 flex flex-col gap-2" aria-label={t.nav.menu}>
              {[...links, { href: "/track", label: t.nav.track }, { href: "/contact", label: t.nav.contact }].map((l, i) => (
                <motion.div key={l.href} initial={{ y: 40, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.15 + i * 0.06, duration: 0.7, ease: EASE }}>
                  <Link href={l.href} onClick={() => setMenu(false)} className="block font-display text-5xl uppercase leading-[1.08] hover:text-accent">
                    {l.label}
                  </Link>
                </motion.div>
              ))}
            </nav>
            <div className="mt-auto flex items-center gap-3">
              <button onClick={() => setLang(lang === "fr" ? "ar" : "fr")} className="rounded-full border border-paper/20 px-5 py-3 text-sm font-semibold" lang={lang === "fr" ? "ar" : "fr"}>
                {t.nav.switchTo}
              </button>
              <Link href="/shop?fav=1" onClick={() => setMenu(false)} className="flex items-center gap-2 rounded-full border border-paper/20 px-5 py-3 text-sm font-semibold">
                <Heart size={16} /> {t.nav.favorites}
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
