/**
 * The nine walls: scroll recordings of the ONELINE store (home, shop and the seven vibes).
 * Each recording is a full-page capture played back top-to-bottom on the screens.
 * Set STORE_URL to the live store to make "Open the wall" link to the real pages.
 */
export const STORE_URL = "";

export const SITES = [
  { slug: "home", name: "ONELINE", line: "Your walls. Your world.", path: "/", desc: "The flagship: a cinematic poster store for Morocco — 3D poster wall, seven vibes, cash on delivery." },
  { slug: "shop", name: "La Boutique", line: "Thirty-six designs, one grid.", path: "/shop", desc: "Search, filter by vibe, sort, favourite — every A4 adhesive poster in one place." },
  { slug: "anime", name: "Anime & Gaming", line: "Bounties, heroes, legends.", path: "/collections/anime-gaming", desc: "Wanted posters, Gear 5, the Pirate Hunter — halftone dots and vertical katakana." },
  { slug: "cars", name: "JDM & Luxe", line: "Racing lines and chrome.", path: "/collections/jdm-luxury-cars", desc: "GT3, RS, Shark Blue — speed stripes and carbon-black grids." },
  { slug: "movies", name: "Films & Séries", line: "Cult scenes, full size.", path: "/collections/movies-series", desc: "Polaroid film cards and editorial one-sheets, framed by film perforations." },
  { slug: "music", name: "Musique", line: "The soundtrack of a room.", path: "/collections/music-artists", desc: "Vinyl, waveforms and portraits — the wall that plays." },
  { slug: "football", name: "Football & Sport", line: "To the 90th and beyond.", path: "/collections/football-sports", desc: "Dima Maghrib, 90+4', No Days Off — original ONELINE designs on pitch lines." },
  { slug: "minimal", name: "Minimal & Esthétique", line: "Soft, clean, always elegant.", path: "/collections/minimal-aesthetic", desc: "Lipstick kisses, gilded letters and blue editorial covers on a hairline grid." },
  { slug: "motivation", name: "Motivation", line: "Words that push every morning.", path: "/collections/motivational", desc: "Discipline > Motivation, خدم وسكت, Day One — red, loud, original." },
];

export const siteUrl = (s) => (STORE_URL ? STORE_URL.replace(/\/$/, "") + s.path : "");
