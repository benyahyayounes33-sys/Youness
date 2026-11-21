import type { Metadata } from "next";
import { ShippingView } from "@/components/pages/Content";

export const metadata: Metadata = { title: "Livraison & retours" };
export default function Page() { return <ShippingView />; }
