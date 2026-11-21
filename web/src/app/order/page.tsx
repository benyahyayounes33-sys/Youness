import type { Metadata } from "next";
import { Suspense } from "react";
import { OrderConfirmation } from "@/components/order/OrderViews";

export const metadata: Metadata = { title: "Votre commande", robots: { index: false } };
export default function Page() {
  return <Suspense fallback={<div className="min-h-[70svh]" />}><OrderConfirmation /></Suspense>;
}
