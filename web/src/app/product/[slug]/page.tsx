import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ProductDetail } from "@/components/product/ProductDetail";
import { imageOf, PRODUCTS, productBySlug } from "@/lib/products";

export function generateStaticParams() {
  return PRODUCTS.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const p = productBySlug(slug);
  if (!p) return {};
  return { title: p.name, description: p.desc.fr, openGraph: { title: `${p.name} · ONELINE`, description: p.desc.fr, images: [imageOf(p.slug)] } };
}

export default async function ProductPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const p = productBySlug(slug);
  if (!p) notFound();
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Product",
    name: p.name,
    image: imageOf(p.slug),
    description: p.desc.fr,
    brand: { "@type": "Brand", name: "ONELINE" },
    offers: { "@type": "Offer", priceCurrency: "MAD", price: p.price, availability: "https://schema.org/InStock" },
  };
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <ProductDetail p={p} />
    </>
  );
}
