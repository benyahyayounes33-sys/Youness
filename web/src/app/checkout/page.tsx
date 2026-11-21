import type { Metadata } from "next";
import { Checkout } from "@/components/checkout/Checkout";

export const metadata: Metadata = { title: "Commande", robots: { index: false } };
export default function Page() { return <Checkout />; }
