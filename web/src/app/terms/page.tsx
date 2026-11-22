import type { Metadata } from "next";
import { LegalView } from "@/components/pages/Content";

export const metadata: Metadata = { title: "Conditions générales" };
export default function Page() { return <LegalView which="terms" />; }
