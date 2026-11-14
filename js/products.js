/* ==========================================================
   ONELINE — product catalogue & store settings
   Edit this file to add posters, change prices or currency.
   ========================================================== */

const STORE = {
  name: "ONELINE",
  currency: "$",            // e.g. "$", "€", "MAD "
  currencyAfter: false,     // true → "149 MAD" style
  freeShippingFrom: 50,     // order total that unlocks free shipping
  shippingCost: 4.99,
  // WhatsApp number for "Order on WhatsApp" (international format, digits only).
  // Leave empty to hide the WhatsApp button.
  whatsapp: "",
  email: "hello@oneline.store",
  instagram: "https://instagram.com/",

  // Where orders and newsletter sign-ups are sent. Without this (or a WhatsApp
  // number) you will NOT receive orders. Paste a Google Apps Script web-app URL
  // (see tools/google-sheet-orders.gs → orders land in a Google Sheet) or a
  // Formspree form URL (https://formspree.io/f/xxxxxx).
  orderEndpoint: "",

  // Payment options shown at checkout and in the footer. Only list what you can
  // actually accept — add "Card" / "PayPal" once they are really connected.
  payments: ["Cash on delivery"],

  // Discount codes → percent off. Give each creator/influencer their own code
  // so you can see who drives sales.
  codes: {
    ONELINE10: 10,          // newsletter welcome code
  },
  welcomeCode: "ONELINE10", // shown after newsletter sign-up ("" to show none)
};

/* Size / format options — price is added to nothing, it IS the price. */
const SIZES = [
  { id: "a4", label: "A4", dims: "21 × 29.7 cm", price: 14.99 },
  { id: "a3", label: "A3", dims: "29.7 × 42 cm", price: 19.99 },
  { id: "a2", label: "A2", dims: "42 × 59.4 cm", price: 29.99 },
];

const FRAMES = [
  { id: "none",  label: "No frame",     price: 0 },
  { id: "black", label: "Black frame",  price: 15 },
  { id: "white", label: "White frame",  price: 15 },
];

const CATEGORIES = [
  { id: "all",    label: "All posters" },
  { id: "anime",  label: "Anime" },
  { id: "wanted", label: "Wanted" },
  { id: "cars",   label: "Cars" },
  { id: "sport",  label: "Sport" },
  { id: "film",   label: "Film" },
  { id: "art",    label: "Art & Fashion" },
];

/* badge: "new" | "best" | "limited" | "" */
const PRODUCTS = [
  { id: "shadow-monarch",      name: "Shadow Monarch",          cat: "anime",  img: "images/shadow-monarch.jpg",       badge: "new",     desc: "Split-line composition with violet shadow soldiers and the line “The system uses me, and I use the system.” Minimal white background, perfect for clean walls." },
  { id: "luffy-gear5-street",  name: "Gear 5 — Streetwear",     cat: "anime",  img: "images/luffy-gear5-street.jpg",   badge: "best",    desc: "Bold black type meets an all-white streetwear Gear 5. Gold accents and a mid-air pose full of energy." },
  { id: "gear5-emblem",        name: "Gear 5 Emblem",           cat: "anime",  img: "images/gear5-emblem.jpg",         badge: "",        desc: "Graphic typographic poster with the giant “5” and the Jolly Roger worked into the lettering." },
  { id: "zoro-newspaper",      name: "The Pirate Hunter — Daily World", cat: "anime", img: "images/zoro-newspaper.jpg", badge: "best",  desc: "A full newspaper front page dedicated to the swordsman: profile, quotes, bounty and vintage paper texture." },

  { id: "wanted-luffy-gear5",  name: "Wanted — Luffy (Gear 5)", cat: "wanted", img: "images/wanted-luffy-gear5.jpg",   badge: "best",    desc: "Classic bounty poster on aged parchment. 3,000,000,000 berries." },
  { id: "wanted-luffy-classic",name: "Wanted — Luffy (First Bounty)", cat: "wanted", img: "images/wanted-luffy-classic.jpg", badge: "", desc: "Where it all began — the very first 30,000,000 bounty, in the original art style." },
  { id: "wanted-zoro",         name: "Wanted — Zoro",           cat: "wanted", img: "images/wanted-zoro.jpg",          badge: "",        desc: "Bounty poster with the intense bandana look. 1,111,000,000 berries." },
  { id: "wanted-nami",         name: "Wanted — Nami",           cat: "wanted", img: "images/wanted-nami.jpg",          badge: "",        desc: "The navigator’s bounty poster on textured parchment. 366,000,000 berries." },
  { id: "wanted-shanks",       name: "Wanted — Shanks",         cat: "wanted", img: "images/wanted-shanks.jpg",        badge: "limited", desc: "The red-haired Emperor. 4,048,900,000 berries." },
  { id: "wanted-dragon",       name: "Wanted — Dragon",         cat: "wanted", img: "images/wanted-dragon.jpg",        badge: "limited", desc: "The most wanted man in the world. 6,000,000,000 berries." },
  { id: "wanted-crocodile",    name: "Wanted — Crocodile",      cat: "wanted", img: "images/wanted-crocodile.jpg",     badge: "",        desc: "Golden hook, fur coat and a cigar. 1,965,000,000 berries." },
  { id: "wanted-hancock",      name: "Wanted — Boa Hancock",    cat: "wanted", img: "images/wanted-hancock.jpg",       badge: "",        desc: "The Pirate Empress. 1,659,000,000 berries." },
  { id: "wanted-itachi",       name: "Wanted — Itachi",         cat: "wanted", img: "images/wanted-itachi.jpg",        badge: "new",     desc: "A crossover bounty poster with crows and a red-eyed stare. 5,000,000,000." },

  { id: "porsche-911-gt3-blue",name: "911 GT3 — Shark Blue",    cat: "cars",   img: "images/porsche-911-gt3-blue.jpg", badge: "best",    desc: "Electric blue GT3 shot from two angles over giant glitch typography. Loud, glossy, motorsport." },
  { id: "porsche-gt3rs-koi",   name: "911 GT3 RS — Koi & Lily", cat: "cars",   img: "images/porsche-gt3rs-koi.jpg",    badge: "new",     desc: "White GT3 RS framed by violet spider lilies and koi fish, with Japanese calligraphy. Japan-meets-Stuttgart." },
  { id: "viper-gt",            name: "Viper GT — Data Sheet",   cat: "cars",   img: "images/viper-gt.jpg",             badge: "",        desc: "Purple American muscle in a technical collage — graphs, specs, wheel close-up and hand-drawn scribbles." },

  { id: "messi-smoke",         name: "The GOAT — Smoke",        cat: "sport",  img: "images/messi-smoke.jpg",          badge: "best",    desc: "Black & white portrait dissolving into smoke and particles behind huge stencil lettering." },

  { id: "dark-knight",         name: "The Dark Knight",         cat: "film",   img: "images/dark-knight.jpg",          badge: "",        desc: "Editorial movie poster in black, cream and red with the iconic “Some men just want to watch the world burn.”" },

  { id: "unseen-007",          name: "Unseen 007",              cat: "art",    img: "images/unseen-007.jpg",           badge: "",        desc: "Surreal wrapped-face figure with red butterflies and neon 007. “Life, is always up.”" },
  { id: "blur-magazine",       name: "BLUR — Vol.03",           cat: "art",    img: "images/blur-magazine.jpg",        badge: "new",     desc: "Subculture magazine cover in cobalt blue with motion-blur portrait. “Everything moves. Nothing stays.”" },
];
