"use client";

import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

export type CartItem = { slug: string; qty: number };

type State = {
  items: CartItem[];
  favorites: string[];
  cartOpen: boolean;
  searchOpen: boolean;
  quickView: string | null;
  add: (slug: string, qty?: number) => void;
  setQty: (slug: string, qty: number) => void;
  remove: (slug: string) => void;
  clear: () => void;
  toggleFav: (slug: string) => void;
  setCartOpen: (open: boolean) => void;
  setSearchOpen: (open: boolean) => void;
  setQuickView: (slug: string | null) => void;
};

export const MAX_QTY = 20;

export const useStore = create<State>()(
  persist(
    (set) => ({
      items: [],
      favorites: [],
      cartOpen: false,
      searchOpen: false,
      quickView: null,
      add: (slug, qty = 1) =>
        set((s) => {
          const found = s.items.find((i) => i.slug === slug);
          const items = found
            ? s.items.map((i) => (i.slug === slug ? { ...i, qty: Math.min(MAX_QTY, i.qty + qty) } : i))
            : [...s.items, { slug, qty: Math.min(MAX_QTY, qty) }];
          return { items };
        }),
      setQty: (slug, qty) =>
        set((s) => ({
          items: qty <= 0 ? s.items.filter((i) => i.slug !== slug)
            : s.items.map((i) => (i.slug === slug ? { ...i, qty: Math.min(MAX_QTY, qty) } : i)),
        })),
      remove: (slug) => set((s) => ({ items: s.items.filter((i) => i.slug !== slug) })),
      clear: () => set({ items: [] }),
      toggleFav: (slug) =>
        set((s) => ({
          favorites: s.favorites.includes(slug) ? s.favorites.filter((f) => f !== slug) : [...s.favorites, slug],
        })),
      setCartOpen: (cartOpen) => set({ cartOpen }),
      setSearchOpen: (searchOpen) => set({ searchOpen }),
      setQuickView: (quickView) => set({ quickView }),
    }),
    {
      name: "oneline-store",
      storage: createJSONStorage(() => localStorage),
      partialize: (s) => ({ items: s.items, favorites: s.favorites }),
      skipHydration: true,
    },
  ),
);
