import type { Metadata } from "next";
import { FaqView } from "@/components/pages/Content";

export const metadata: Metadata = { title: "FAQ" };
export default function Page() { return <FaqView />; }
