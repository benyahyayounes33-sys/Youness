"use client";

import { motion, useMotionValue, useReducedMotion, useSpring, type HTMLMotionProps } from "framer-motion";
import Link from "next/link";
import { useRef, type ReactNode } from "react";
import clsx from "clsx";

export const EASE = [0.16, 1, 0.3, 1] as const;

/** Fade/rise into view once. */
export function Reveal({ children, delay = 0, y = 28, className, as = "div" }: {
  children: ReactNode; delay?: number; y?: number; className?: string; as?: "div" | "section" | "li" | "article";
}) {
  const reduce = useReducedMotion();
  const M = motion[as];
  return (
    <M
      className={className}
      initial={reduce ? { opacity: 0 } : { opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "0px 0px -10% 0px" }}
      transition={{ duration: reduce ? 0.2 : 0.9, ease: EASE, delay }}
    >
      {children}
    </M>
  );
}

/** Headline that rises line by line out of a mask. */
export function MaskLines({ lines, className, lineClassName, delay = 0, inView = false }: {
  lines: ReactNode[]; className?: string; lineClassName?: string | string[]; delay?: number; inView?: boolean;
}) {
  const reduce = useReducedMotion();
  const line = {
    hidden: reduce ? { opacity: 0 } : { y: "105%" },
    show: (i: number) => ({
      ...(reduce ? { opacity: 1 } : { y: "0%" }),
      transition: { duration: reduce ? 0.2 : 1.1, ease: EASE, delay: delay + i * 0.12 },
    }),
  };
  return (
    <motion.span
      className={clsx("block", className)}
      initial="hidden"
      {...(inView ? { whileInView: "show", viewport: { once: true, margin: "0px 0px -8% 0px" } } : { animate: "show" })}
    >
      {lines.map((ln, i) => (
        <span key={i} className="-mt-[0.16em] block overflow-hidden pb-[0.06em] pt-[0.16em]">
          <motion.span className={clsx("block", Array.isArray(lineClassName) ? lineClassName[i] : lineClassName)} variants={line} custom={i}>
            {ln}
          </motion.span>
        </span>
      ))}
    </motion.span>
  );
}

/** Button/link that leans toward the pointer (disabled with reduced motion / touch). */
export function Magnetic({ children, href, onClick, className, variant = "solid", type = "button", ariaLabel, disabled }: {
  children: ReactNode; href?: string; onClick?: () => void; className?: string; variant?: "solid" | "ghost" | "light";
  type?: "button" | "submit"; ariaLabel?: string; disabled?: boolean;
}) {
  const reduce = useReducedMotion();
  const ref = useRef<HTMLElement | null>(null);
  const x = useSpring(useMotionValue(0), { stiffness: 260, damping: 18, mass: 0.4 });
  const y = useSpring(useMotionValue(0), { stiffness: 260, damping: 18, mass: 0.4 });
  const move = (e: React.PointerEvent) => {
    if (reduce || e.pointerType !== "mouse" || !ref.current) return;
    const r = ref.current.getBoundingClientRect();
    x.set((e.clientX - (r.left + r.width / 2)) * 0.28);
    y.set((e.clientY - (r.top + r.height / 2)) * 0.38);
  };
  const leave = () => { x.set(0); y.set(0); };
  const cls = clsx(
    "relative inline-flex items-center justify-center gap-3 rounded-full px-7 py-4 text-sm font-semibold tracking-wide transition-colors duration-300 select-none disabled:opacity-50 disabled:cursor-not-allowed",
    variant === "solid" && "bg-accent text-white hover:bg-[#ff5247]",
    variant === "ghost" && "border border-paper/25 text-paper hover:border-paper hover:bg-paper hover:text-ink",
    variant === "light" && "bg-paper text-ink hover:bg-white",
    className,
  );
  const common = {
    onPointerMove: move, onPointerLeave: leave, style: { x, y },
  } satisfies HTMLMotionProps<"a">;
  if (href) {
    return (
      <motion.span {...common} className="inline-flex" ref={ref as React.Ref<HTMLSpanElement>}>
        <Link href={href} className={cls} aria-label={ariaLabel} onClick={onClick}>{children}</Link>
      </motion.span>
    );
  }
  return (
    <motion.button {...common} ref={ref as React.Ref<HTMLButtonElement>} type={type} onClick={onClick}
      className={cls} aria-label={ariaLabel} disabled={disabled}>
      {children}
    </motion.button>
  );
}

export function Eyebrow({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <p className={clsx("flex items-center gap-3 text-[11px] font-semibold uppercase tracking-[0.28em] text-silver", className)}>
      <span className="h-px w-8 bg-accent" aria-hidden />
      {children}
    </p>
  );
}
