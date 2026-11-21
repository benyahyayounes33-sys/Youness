/**
 * DEMO CATALOGUE — sample products and prices for the prototype.
 * Replace with your real products (or load them from a database / CMS) before going live.
 */
export type Lang = "fr" | "ar";
export type L10n = { fr: string; ar: string };
export type VibeSlug =
  | "jdm-luxury-cars"
  | "music-artists"
  | "movies-series"
  | "football-sports"
  | "anime-gaming"
  | "minimal-aesthetic"
  | "motivational";

export type Vibe = { slug: VibeSlug; index: string; name: L10n; line: L10n; cover: string[] };

export type Product = {
  slug: string;
  name: string;
  vibe: VibeSlug;
  type: "poster" | "sticker";
  price: number;
  badge?: "best" | "new" | "limited";
  original?: boolean;
  popularity: number;
  added: number;
  desc: L10n;
};

export const VIBES: Vibe[] = [
  { slug: "jdm-luxury-cars", index: "01", name: { fr: "JDM & Voitures de luxe", ar: "سيارات JDM والفخامة" },
    line: { fr: "Lignes de course, chrome et adrénaline.", ar: "خطوط السباق والكروم والأدرينالين." },
    cover: ["911-gt3-shark-blue", "992-gt3-rs-argent", "911-gt3-noir-mat"] },
  { slug: "music-artists", index: "02", name: { fr: "Musique & Artistes", ar: "الموسيقى والفنانون" },
    line: { fr: "La bande-son de ta chambre.", ar: "الموسيقى التصويرية لغرفتك." },
    cover: ["happier-than-ever", "now-playing", "sound-of-the-city"] },
  { slug: "movies-series", index: "03", name: { fr: "Films & Séries", ar: "أفلام ومسلسلات" },
    line: { fr: "Tes scènes cultes, en grand.", ar: "مشاهدك المفضلة بحجم كبير." },
    cover: ["the-dark-knight", "queens-gambit", "baby-driver"] },
  { slug: "football-sports", index: "04", name: { fr: "Football & Sport", ar: "كرة القدم والرياضة" },
    line: { fr: "Jusqu'à la 90e et au-delà.", ar: "حتى الدقيقة 90 وما بعدها." },
    cover: ["dima-maghrib", "ninety-plus-four", "no-days-off"] },
  { slug: "anime-gaming", index: "05", name: { fr: "Anime & Gaming", ar: "أنمي وألعاب" },
    line: { fr: "Primes, héros et légendes.", ar: "مكافآت وأبطال وأساطير." },
    cover: ["wanted-luffy-gear5", "wanted-shanks", "zoro-daily-world"] },
  { slug: "minimal-aesthetic", index: "06", name: { fr: "Minimal & Esthétique", ar: "بسيط وجمالي" },
    line: { fr: "Doux, épuré, toujours élégant.", ar: "ناعم وأنيق دائماً." },
    cover: ["love-yourself-first", "belle-lettres", "blur-vol-03"] },
  { slug: "motivational", index: "07", name: { fr: "Motivation", ar: "تحفيز" },
    line: { fr: "Des mots qui te poussent chaque matin.", ar: "كلمات تدفعك كل صباح." },
    cover: ["discipline-over-motivation", "work-in-silence", "day-one"] },
];

const P = (slug: string, name: string, vibe: VibeSlug, price: number, popularity: number, added: number,
  fr: string, ar: string, extra: Partial<Product> = {}): Product =>
  ({ slug, name, vibe, type: "poster", price, popularity, added, desc: { fr, ar }, ...extra });

export const PRODUCTS: Product[] = [
  P("911-gt3-noir-mat", "911 GT3 — Noir Mat", "jdm-luxury-cars", 45, 92, 20,
    "Une GT3 noir mat posée sous un « 911 » géant en dégradé. Sobre, puissant, parfait pour un bureau.",
    "‏GT3 بالأسود المطفي تحت رقم 911 عملاق بتدرّج لوني. بسيط وقوي ومثالي للمكتب.", { badge: "best" }),
  P("992-gt3-rs-argent", "992 GT3 RS — Argent", "jdm-luxury-cars", 45, 80, 18,
    "La RS argentée sur fond graphite, bandes centrales et fiche technique minimaliste.",
    "‏RS الفضية على خلفية رمادية مع خطوط وسطية وبطاقة تقنية بسيطة."),
  P("911-gt3-shark-blue", "911 GT3 — Shark Blue", "jdm-luxury-cars", 45, 77, 30,
    "Bleu électrique, typographie glitch et deux angles de la même voiture. Bruyant, brillant, motorsport.",
    "أزرق كهربائي وخط «غليتش» وزاويتان لنفس السيارة. جريء ولامع وروح السباقات.", { badge: "new" }),
  P("gt3-rs-koi", "GT3 RS — Koi & Lys", "jdm-luxury-cars", 45, 64, 12,
    "La GT3 RS blanche entourée de lys violets et de calligraphie japonaise : Japon × Stuttgart.",
    "‏GT3 RS البيضاء محاطة بزنابق بنفسجية وخط ياباني: اليابان × شتوتغارت."),
  P("happier-than-ever", "Happier Than Ever", "music-artists", 39, 83, 16,
    "Tons crème et typographie géante autour d'un portrait doux. Pour les fans de pop mélancolique.",
    "ألوان كريمية وخط ضخم حول بورتريه ناعم. لعشاق البوب الهادئ.", { badge: "best" }),
  P("selena-polaroid", "Selena — Polaroid", "music-artists", 35, 58, 14,
    "Format polaroid minimal avec fiche d'identité façon carte de collection.",
    "تصميم بولارويد بسيط مع بطاقة تعريف كبطاقات التجميع."),
  P("now-playing", "Now Playing", "music-artists", 35, 61, 34,
    "Vinyle rouge, barre de lecture et titre en serif. Un design ONELINE pour les mélomanes.",
    "أسطوانة حمراء وشريط تشغيل وعنوان أنيق. تصميم ONELINE لعشاق الموسيقى.", { badge: "new", original: true }),
  P("sound-of-the-city", "Sound of the City", "music-artists", 35, 66, 33,
    "Une onde sonore et les coordonnées de Casablanca. Le bruit de la ville, en noir et rouge.",
    "موجة صوتية وإحداثيات الدار البيضاء. صوت المدينة بالأسود والأحمر.", { original: true }),
  P("the-dark-knight", "The Dark Knight", "movies-series", 39, 88, 15,
    "Composition éditoriale rouge et noire, citation culte en bas de page. Un classique du mur cinéphile.",
    "تكوين تحريري بالأحمر والأسود مع اقتباس شهير. كلاسيكي لكل محب للسينما.", { badge: "best" }),
  P("lucy-2014", "Lucy (2014)", "movies-series", 35, 52, 10,
    "Affiche minimaliste façon carte de film : photo, année, réalisateur et casting.",
    "ملصق بسيط على شكل بطاقة فيلم: صورة وسنة ومخرج وممثلون."),
  P("baby-driver", "Baby Driver", "movies-series", 35, 57, 9,
    "Lunettes noires, écouteurs et fiche minimaliste. Pour ceux qui conduisent en rythme.",
    "نظارات سوداء وسماعات وبطاقة بسيطة. لمن يقود على الإيقاع."),
  P("venom-2018", "Venom", "movies-series", 35, 55, 8,
    "Moitié homme, moitié symbiote, sur fond crème. Contraste maximal.",
    "نصف إنسان ونصف سيمبيوت على خلفية كريمية. تباين قوي."),
  P("queens-gambit", "The Queen's Gambit", "movies-series", 35, 60, 31,
    "Échiquier, regard concentré et typographie condensée. Élégance stratégique.",
    "رقعة شطرنج ونظرة مركّزة وخط مكثف. أناقة استراتيجية.", { badge: "new" }),
  P("dima-maghrib", "Dima Maghrib", "football-sports", 39, 95, 32,
    "Rouge profond, étoile verte et « ديما مغرب ». Un design ONELINE pour les jours de match.",
    "أحمر عميق ونجمة خضراء و«ديما مغرب». تصميم ONELINE لأيام المباريات.", { badge: "best", original: true }),
  P("ninety-plus-four", "90+4'", "football-sports", 35, 63, 29,
    "Un terrain dessiné au trait et la minute qui change tout. « It's never over. »",
    "ملعب مرسوم بخطوط رفيعة والدقيقة التي تغيّر كل شيء. «لم ينتهِ بعد».", { original: true }),
  P("no-days-off", "No Days Off", "football-sports", 35, 59, 28,
    "Typographie empilée, contours et rouge vif. Pour la salle, le terrain ou le bureau.",
    "خط متراكب وحدود وأحمر قوي. للصالة أو الملعب أو المكتب.", { original: true }),
  P("wanted-luffy-gear5", "Wanted — Luffy (Gear 5)", "anime-gaming", 39, 99, 26,
    "L'avis de recherche du Dieu Soleil sur parchemin vieilli. 3 000 000 000 de berries.",
    "إعلان مطلوب لإله الشمس على ورق قديم. 3,000,000,000 بيري.", { badge: "best" }),
  P("wanted-luffy-30m", "Wanted — Luffy (première prime)", "anime-gaming", 39, 74, 21,
    "Là où tout a commencé : la toute première prime de 30 000 000.",
    "حيث بدأ كل شيء: أول مكافأة بقيمة 30,000,000."),
  P("wanted-shanks", "Wanted — Shanks", "anime-gaming", 39, 90, 22,
    "L'Empereur aux cheveux rouges. 4 048 900 000 berries.",
    "الإمبراطور ذو الشعر الأحمر. 4,048,900,000 بيري.", { badge: "limited" }),
  P("wanted-dragon", "Wanted — Dragon", "anime-gaming", 39, 81, 23,
    "L'homme le plus recherché du monde. 6 000 000 000 berries.",
    "الرجل الأكثر طلباً في العالم. 6,000,000,000 بيري.", { badge: "limited" }),
  P("wanted-nami", "Wanted — Nami", "anime-gaming", 39, 70, 19,
    "La navigatrice sur parchemin texturé. 366 000 000 berries.",
    "الملاحة على ورق قديم. 366,000,000 بيري."),
  P("wanted-crocodile", "Wanted — Crocodile", "anime-gaming", 39, 62, 17,
    "Crochet doré, manteau de fourrure et cigare. 1 965 000 000 berries.",
    "خطاف ذهبي ومعطف فرو وسيجار. 1,965,000,000 بيري."),
  P("wanted-itachi", "Wanted — Itachi", "anime-gaming", 39, 76, 27,
    "Un avis de recherche crossover, corbeaux et regard rouge. 5 000 000 000.",
    "إعلان مطلوب مزدوج العوالم، غربان ونظرة حمراء. 5,000,000,000.", { badge: "new" }),
  P("zoro-daily-world", "Zoro — Daily World", "anime-gaming", 45, 86, 24,
    "Une une de journal complète : profil, citations, prime et papier vintage.",
    "صفحة جريدة كاملة: ملف شخصي واقتباسات ومكافأة وورق عتيق.", { badge: "best" }),
  P("gear5-streetwear", "Gear 5 — Streetwear", "anime-gaming", 39, 79, 13,
    "Typographie noire massive et un Gear 5 tout en blanc, accents dorés.",
    "خط أسود ضخم وGear 5 بالأبيض مع لمسات ذهبية."),
  P("gear5-emblem", "Gear 5 — Emblème", "anime-gaming", 39, 54, 11,
    "Le « 5 » géant et le Jolly Roger intégrés dans le lettrage.",
    "الرقم 5 العملاق وعلم القراصنة داخل الحروف."),
  P("shadow-monarch", "Shadow Monarch", "anime-gaming", 39, 68, 35,
    "Composition fendue, soldats de l'ombre violets et fond blanc minimal.",
    "تكوين مقسوم وجنود ظل بنفسجيون على خلفية بيضاء.", { badge: "new" }),
  P("jolly-roger-sticker", "Sticker — Jolly Roger", "anime-gaming", 15, 72, 25,
    "Le drapeau du chapeau de paille en sticker découpé, contour blanc.",
    "علم قبعة القش كملصق مقصوص بحافة بيضاء.", { type: "sticker" }),
  P("love-yourself-first", "Love Yourself First", "minimal-aesthetic", 35, 91, 30,
    "Baisers de rouge à lèvres et une phrase douce en serif. Le favori des chambres aesthetic.",
    "قبلات أحمر شفاه وعبارة ناعمة. المفضل لغرف الـ aesthetic.", { badge: "best" }),
  P("belle-lettres", "Belle — Lettres", "minimal-aesthetic", 35, 65, 7,
    "Robe dorée, roses gravées et manuscrit ancien en fond.",
    "فستان ذهبي وورود منقوشة ومخطوطة قديمة في الخلفية."),
  P("belle-fleurs", "Belle — Fleurs", "minimal-aesthetic", 35, 61, 6,
    "Bouquet de fleurs, lanterne chaude et feuillage d'automne.",
    "باقة زهور وفانوس دافئ وأوراق خريفية."),
  P("bubbles", "Bubbles", "minimal-aesthetic", 29, 56, 5,
    "Bleu ciel et bonne humeur : le poster le plus mignon du catalogue.",
    "أزرق سماوي ومزاج جميل: أكثر ملصق لطافة في المتجر."),
  P("blur-vol-03", "BLUR — Vol. 03", "minimal-aesthetic", 39, 69, 4,
    "Couverture éditoriale bleue, mouvement et grain : « Everything moves. Nothing stays. »",
    "غلاف تحريري أزرق وحركة وحبيبات: «كل شيء يتحرك، لا شيء يبقى»."),
  P("discipline-over-motivation", "Discipline > Motivation", "motivational", 35, 89, 36,
    "Le rappel quotidien en typographie massive. Un design ONELINE.",
    "تذكير يومي بخط ضخم. تصميم ONELINE.", { badge: "best", original: true }),
  P("work-in-silence", "Work in Silence — خدم وسكت", "motivational", 35, 84, 36,
    "Noir profond, darija en rouge et une promesse : « let success make the noise ».",
    "أسود عميق ودارجة بالأحمر ووعد: «دع النجاح يتكلم».", { badge: "new", original: true }),
  P("day-one", "Day One", "motivational", 35, 71, 36,
    "« One day » barré, « Day one » affirmé. À toi de choisir, dès maintenant.",
    "«يوماً ما» مشطوبة و«اليوم الأول» واضحة. القرار لك من الآن.", { original: true }),
];

export const productBySlug = (slug: string) => PRODUCTS.find((p) => p.slug === slug);
export const vibeBySlug = (slug: string) => VIBES.find((v) => v.slug === slug);
export const productsByVibe = (slug: VibeSlug) => PRODUCTS.filter((p) => p.vibe === slug);
export const imageOf = (slug: string) => `/products/${slug}.jpg`;
