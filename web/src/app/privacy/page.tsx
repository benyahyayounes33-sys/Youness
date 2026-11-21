import type { Metadata } from "next";
import { LegalView } from "@/components/pages/Content";

export const metadata: Metadata = { title: "Confidentialité" };
export default function Page() { return <LegalView which="privacy" />; }
