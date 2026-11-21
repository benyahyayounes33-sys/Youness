import type { Metadata } from "next";
import { AboutView } from "@/components/pages/Content";

export const metadata: Metadata = { title: "La marque" };
export default function Page() { return <AboutView />; }
