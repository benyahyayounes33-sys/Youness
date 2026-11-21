"use client";

import { MotionConfig } from "framer-motion";
import { useEffect, type ReactNode } from "react";
import { LangProvider } from "@/lib/i18n";
import { useStore } from "@/lib/store";

export function Providers({ children }: { children: ReactNode }) {
  useEffect(() => {
    useStore.persist.rehydrate();
  }, []);
  return (
    <MotionConfig reducedMotion="user">
      <LangProvider>{children}</LangProvider>
    </MotionConfig>
  );
}
