import { DELIVERY_ZONES, OTHER_ZONE, STORE, type Zone } from "./config";
import { productBySlug } from "./products";
import type { CartItem } from "./store";

export type Line = { slug: string; name: string; type: "poster" | "sticker"; unit: number; qty: number; total: number };

export function lines(items: CartItem[]): Line[] {
  return items.flatMap((i) => {
    const p = productBySlug(i.slug);
    if (!p || i.qty < 1) return [];
    return [{ slug: p.slug, name: p.name, type: p.type, unit: p.price, qty: i.qty, total: p.price * i.qty }];
  });
}

export function zoneFor(city: string): Zone {
  return DELIVERY_ZONES.find((z) => z.cities.includes(city)) ?? OTHER_ZONE;
}

export function totals(items: CartItem[], city?: string) {
  const ls = lines(items);
  const subtotal = ls.reduce((s, l) => s + l.total, 0);
  const count = ls.reduce((s, l) => s + l.qty, 0);
  const free = subtotal >= STORE.freeShippingFrom;
  const zone = city ? zoneFor(city) : null;
  const delivery = !city || subtotal === 0 ? 0 : free ? 0 : zone!.fee;
  return { lines: ls, subtotal, count, free, zone, delivery, total: subtotal + delivery, missingForFree: Math.max(0, STORE.freeShippingFrom - subtotal) };
}

/** Moroccan mobile/landline: 06/07/05 + 8 digits, also +212 / 00212 prefixes. Returns +212XXXXXXXXX or null. */
export function normalizePhone(raw: string): string | null {
  const s = raw.replace(/[\s.\-()]/g, "");
  const m = s.match(/^(?:\+212|00212|212|0)([5-7]\d{8})$/);
  return m ? `+212${m[1]}` : null;
}

export type CheckoutForm = { name: string; phone: string; city: string; otherCity: string; address: string; note: string };
export type FieldError = "name" | "phone" | "city" | "address" | "empty";

export function validate(f: CheckoutForm, itemCount: number): Partial<Record<keyof CheckoutForm | "cart", FieldError>> {
  const e: Partial<Record<keyof CheckoutForm | "cart", FieldError>> = {};
  if (f.name.trim().length < 3) e.name = "name";
  if (!normalizePhone(f.phone)) e.phone = "phone";
  if (!f.city || (f.city === "__other" && f.otherCity.trim().length < 2)) e.city = "city";
  if (f.address.trim().length < 10) e.address = "address";
  if (itemCount < 1) e.cart = "empty";
  return e;
}

export type Order = {
  ref: string;
  createdAt: string;
  customer: { name: string; phone: string; city: string; address: string; note: string };
  lines: Line[];
  subtotal: number;
  delivery: number;
  total: number;
};

export function makeRef(d = new Date()): string {
  const p = (n: number) => String(n).padStart(2, "0");
  const rnd = Math.random().toString(36).slice(2, 6).toUpperCase();
  return `OL-${String(d.getFullYear()).slice(2)}${p(d.getMonth() + 1)}${p(d.getDate())}-${rnd}`;
}

export function buildOrder(f: CheckoutForm, items: CartItem[]): Order {
  const city = f.city === "__other" ? f.otherCity.trim() : f.city;
  const t = totals(items, city || "__other");
  return {
    ref: makeRef(),
    createdAt: new Date().toISOString(),
    customer: { name: f.name.trim(), phone: normalizePhone(f.phone)!, city, address: f.address.trim(), note: f.note.trim() },
    lines: t.lines,
    subtotal: t.subtotal,
    delivery: t.delivery,
    total: t.total,
  };
}

const mad = (n: number) => `${n.toLocaleString("fr-FR")} MAD`;

/** Message sent to the shop on WhatsApp (French, so the team always reads the same format). */
export function whatsappMessage(o: Order): string {
  const items = o.lines.map((l) => `• ${l.name} (${l.type === "poster" ? "A4 adhésif" : "sticker"}) × ${l.qty} = ${mad(l.total)}`);
  return [
    `🧾 *Nouvelle commande ${STORE.name}*`,
    `Réf : ${o.ref}`,
    "",
    `👤 Nom : ${o.customer.name}`,
    `📞 Téléphone : ${o.customer.phone}`,
    `🏙️ Ville : ${o.customer.city}`,
    `📍 Adresse : ${o.customer.address}`,
    ...(o.customer.note ? [`📝 Note : ${o.customer.note}`] : []),
    "",
    "*Articles*",
    ...items,
    "",
    `Sous-total : ${mad(o.subtotal)}`,
    `Livraison : ${o.delivery === 0 ? "offerte" : mad(o.delivery)}`,
    `*Total à payer à la livraison : ${mad(o.total)}*`,
    "💵 Paiement : à la livraison (cash)",
    "",
    "Merci de confirmer ma commande 🙏",
  ].join("\n");
}

export const whatsappUrl = (text: string) => `https://wa.me/${STORE.whatsappNumber}?text=${encodeURIComponent(text)}`;

/* ---- orders prepared on this device (no server: nothing is recorded by the shop until WhatsApp) ---- */
const KEY = "oneline-orders";

export function saveLocalOrder(o: Order) {
  const all = getLocalOrders().filter((x) => x.ref !== o.ref);
  localStorage.setItem(KEY, JSON.stringify([o, ...all].slice(0, 20)));
}

export function getLocalOrders(): Order[] {
  if (typeof window === "undefined") return [];
  try {
    return JSON.parse(localStorage.getItem(KEY) || "[]");
  } catch {
    return [];
  }
}

export function findLocalOrder(ref: string, phone?: string): Order | undefined {
  const r = ref.trim().toUpperCase();
  const ph = phone ? normalizePhone(phone) : null;
  return getLocalOrders().find((o) => o.ref === r && (!phone || o.customer.phone === ph));
}
