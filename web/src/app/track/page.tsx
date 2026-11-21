import type { Metadata } from "next";
import { TrackOrder } from "@/components/order/OrderViews";

export const metadata: Metadata = { title: "Suivi de commande" };
export default function Page() { return <TrackOrder />; }
