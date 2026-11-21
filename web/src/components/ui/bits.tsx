"use client";

import { Minus, Plus } from "lucide-react";
import clsx from "clsx";
import type { ReactNode } from "react";
import { MAX_QTY } from "@/lib/store";
import { Eyebrow, MaskLines, Reveal } from "./motion";

export function Wordmark({ className }: { className?: string }) {
  return (
    <span dir="ltr" className={clsx("font-display text-2xl leading-none tracking-[0.04em]", className)}>
      ONELINE<span className="text-accent">.</span>
    </span>
  );
}

export function QtyStepper({ value, onChange, size = "md", label }: {
  value: number; onChange: (v: number) => void; size?: "sm" | "md"; label: string;
}) {
  const b = size === "sm" ? "h-8 w-8" : "h-11 w-11";
  return (
    <div className="inline-flex items-center rounded-full border border-current/20" role="group" aria-label={label}>
      <button type="button" className={clsx(b, "grid place-items-center rounded-full hover:bg-current/10")}
        onClick={() => onChange(value - 1)} aria-label="−">
        <Minus size={14} />
      </button>
      <span className={clsx("min-w-8 text-center tabular-nums font-semibold", size === "sm" ? "text-sm" : "")} aria-live="polite">{value}</span>
      <button type="button" className={clsx(b, "grid place-items-center rounded-full hover:bg-current/10 disabled:opacity-30")}
        onClick={() => onChange(value + 1)} disabled={value >= MAX_QTY} aria-label="+">
        <Plus size={14} />
      </button>
    </div>
  );
}

export function PageHeader({ eyebrow, title, sub, children }: { eyebrow: string; title: string; sub?: string; children?: ReactNode }) {
  return (
    <header className="mx-auto max-w-[1440px] px-5 pb-10 pt-14 md:px-10 md:pb-14 md:pt-20">
      <Eyebrow>{eyebrow}</Eyebrow>
      <h1 className="mt-6 max-w-5xl font-display text-[clamp(2.6rem,7vw,6.5rem)] uppercase leading-[0.92]">
        <MaskLines lines={[title]} />
      </h1>
      {sub && <Reveal delay={0.2}><p className="mt-6 max-w-2xl text-lg text-silver">{sub}</p></Reveal>}
      {children}
    </header>
  );
}

/* brand icons (lucide no longer ships brand marks) */
export function InstagramIcon({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden>
      <rect x="3" y="3" width="18" height="18" rx="5" /><circle cx="12" cy="12" r="4.2" /><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none" />
    </svg>
  );
}
export function TikTokIcon({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" aria-hidden>
      <path d="M16.6 3c.4 2.1 1.7 3.6 3.9 3.8v3.1c-1.4.1-2.7-.3-3.9-1v6.3c0 3.4-2.6 5.8-5.9 5.8-3.2 0-5.7-2.5-5.7-5.6 0-3.4 2.9-6 6.4-5.5v3.2c-1.5-.4-3.1.6-3.1 2.3 0 1.4 1.1 2.4 2.4 2.4 1.5 0 2.6-1 2.6-2.8V3h3.3z" />
    </svg>
  );
}
export function WhatsAppIcon({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" aria-hidden>
      <path d="M12 2.2a9.7 9.7 0 0 0-8.4 14.6L2.3 21.8l5.1-1.3A9.7 9.7 0 1 0 12 2.2zm0 17.7c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 19.9zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8.9c-.1.2-.3.2-.5.1-.7-.3-1.4-.7-2-1.3-.6-.5-1-1.1-1.4-1.8-.1-.2 0-.4.1-.5l.4-.4.2-.4v-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5c-.2 0-.5.1-.7.3-.6.6-.9 1.4-.9 2.2.1 1 .4 1.9 1 2.7 1.1 1.6 2.5 2.9 4.2 3.7.5.2 1 .4 1.5.5.6.2 1.1.1 1.6 0 .6-.1 1.3-.6 1.5-1.1.2-.4.2-.9.1-1.3l-.3-.3z" />
    </svg>
  );
}
