/**
 * Store settings — edit this file before going live.
 * Everything marked DEMO is a placeholder and must be replaced with real values.
 */
export const STORE = {
  name: "ONELINE",
  tagline: "Walls that say something.",
  /** DEMO — WhatsApp Business number in international format, digits only (e.g. 2126XXXXXXXX). */
  whatsappNumber: "212600000000",
  /** DEMO */
  phoneDisplay: "+212 6 00 00 00 00",
  /** DEMO */
  email: "contact@oneline.ma",
  instagram: "https://www.instagram.com/",
  tiktok: "https://www.tiktok.com/",
  baseCity: "Casablanca",
  /** Order subtotal (MAD) from which delivery is free. DEMO value. */
  freeShippingFrom: 250,
  /** Shown in the announcement bar while the catalogue is demo data. */
  isDemo: true,
} as const;

export type Zone = { id: string; fee: number; eta: { fr: string; ar: string }; cities: string[] };

/** Delivery fees per city (MAD). DEMO values — align them with your delivery company. */
export const DELIVERY_ZONES: Zone[] = [
  { id: "casablanca", fee: 20, eta: { fr: "24–48 h", ar: "24–48 ساعة" }, cities: ["Casablanca"] },
  {
    id: "axe",
    fee: 30,
    eta: { fr: "24–72 h", ar: "24–72 ساعة" },
    cities: ["Rabat", "Salé", "Témara", "Mohammédia", "Kénitra", "El Jadida", "Settat", "Berrechid"],
  },
  {
    id: "national",
    fee: 35,
    eta: { fr: "2–4 jours", ar: "2–4 أيام" },
    cities: ["Marrakech", "Fès", "Meknès", "Tanger", "Tétouan", "Agadir", "Oujda", "Safi", "Béni Mellal", "Nador",
      "Khouribga", "Essaouira", "Errachidia", "Ouarzazate", "Taza", "Larache", "Al Hoceïma", "Khémisset"],
  },
  { id: "sud", fee: 45, eta: { fr: "3–6 jours", ar: "3–6 أيام" }, cities: ["Laâyoune", "Dakhla", "Guelmim", "Tan-Tan"] },
];

/** Used when the customer types a city that is not in the list. */
export const OTHER_ZONE: Zone = { id: "autre", fee: 40, eta: { fr: "2–6 jours", ar: "2–6 أيام" }, cities: [] };

export const ALL_CITIES = DELIVERY_ZONES.flatMap((z) => z.cities);
