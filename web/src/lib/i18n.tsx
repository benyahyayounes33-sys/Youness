"use client";

import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";
import { DICTS, type Dict } from "./dict";
import type { L10n, Lang } from "./products";

type Ctx = { lang: Lang; t: Dict; setLang: (l: Lang) => void; l: (v: L10n) => string; mad: (n: number) => string };

const LangCtx = createContext<Ctx | null>(null);
const KEY = "oneline-lang";

export function LangProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>("fr");

  useEffect(() => {
    const saved = localStorage.getItem(KEY);
    if (saved === "ar" || saved === "fr") setLangState(saved);
  }, []);

  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dir = DICTS[lang].dir;
  }, [lang]);

  const setLang = useCallback((l: Lang) => {
    setLangState(l);
    localStorage.setItem(KEY, l);
  }, []);

  const value: Ctx = {
    lang,
    t: DICTS[lang],
    setLang,
    l: (v) => v[lang],
    mad: (n) => (lang === "ar" ? `${n.toLocaleString("fr-FR")} درهم` : `${n.toLocaleString("fr-FR")} MAD`),
  };
  return <LangCtx.Provider value={value}>{children}</LangCtx.Provider>;
}

export function useLang() {
  const c = useContext(LangCtx);
  if (!c) throw new Error("useLang outside LangProvider");
  return c;
}
