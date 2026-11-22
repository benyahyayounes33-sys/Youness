import type { Metadata, Viewport } from "next";
import "@fontsource/anton/400.css";
import "@fontsource-variable/inter";
import "@fontsource/instrument-serif/400.css";
import "@fontsource/instrument-serif/400-italic.css";
import "@fontsource/ibm-plex-sans-arabic/400.css";
import "@fontsource/ibm-plex-sans-arabic/600.css";
import "@fontsource/ibm-plex-sans-arabic/700.css";
import "./globals.css";
import { Providers } from "@/components/layout/Providers";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { CartDrawer, QuickView, SearchOverlay } from "@/components/product/Overlays";

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000"),
  title: { default: "ONELINE — Posters A4 adhésifs · Maroc", template: "%s · ONELINE" },
  description: "Posters A4 adhésifs et stickers pour personnaliser ta chambre. Voitures, anime, films, musique, football, minimal, motivation. Paiement à la livraison au Maroc.",
  openGraph: { title: "ONELINE — YOUR WALLS. YOUR WORLD.", description: "Posters A4 adhésifs · Paiement à la livraison au Maroc", images: ["/scenes/room-after.jpg"], locale: "fr_MA", type: "website" },
};

export const viewport: Viewport = { themeColor: "#0b0b0d", width: "device-width", initialScale: 1 };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr" dir="ltr" suppressHydrationWarning>
      <body className="grain min-h-svh bg-ink text-paper">
        <Providers>
          <a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:start-4 focus:top-4 focus:z-[100] focus:rounded-full focus:bg-paper focus:px-4 focus:py-2 focus:text-ink">
            Aller au contenu
          </a>
          <Header />
          <main id="main">{children}</main>
          <Footer />
          <CartDrawer />
          <QuickView />
          <SearchOverlay />
        </Providers>
      </body>
    </html>
  );
}
