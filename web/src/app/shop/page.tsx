import type { Metadata } from "next";
import { Suspense } from "react";
import { ShopBrowser } from "@/components/product/ShopBrowser";
import { ShopHeader } from "@/components/pages/Headers";

export const metadata: Metadata = { title: "Boutique", description: "Tous les posters A4 adhésifs et stickers ONELINE, par vibe." };

export default function ShopPage() {
  return (
    <>
      <ShopHeader />
      <Suspense fallback={<div className="min-h-[60svh]" />}>
        <ShopBrowser />
      </Suspense>
    </>
  );
}
