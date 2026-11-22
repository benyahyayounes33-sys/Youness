import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Suspense } from "react";
import { ShopBrowser } from "@/components/product/ShopBrowser";
import { VibeHeader } from "@/components/pages/Headers";
import { VIBES, vibeBySlug } from "@/lib/products";

export function generateStaticParams() {
  return VIBES.map((v) => ({ slug: v.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const v = vibeBySlug(slug);
  return v ? { title: v.name.fr, description: v.line.fr } : {};
}

export default async function CollectionPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const v = vibeBySlug(slug);
  if (!v) notFound();
  return (
    <>
      <VibeHeader slug={v.slug} />
      <Suspense fallback={<div className="min-h-[60svh]" />}>
        <ShopBrowser lockedVibe={v.slug} />
      </Suspense>
    </>
  );
}
