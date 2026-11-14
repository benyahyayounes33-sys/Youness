# ONELINE: Brand Launch Plan

A practical plan for taking ONELINE from a finished website to a real poster brand that sells.
The work is split into a 30-day timeline (section 7) with a go-live checklist at the end.

---

## 0. Decide this first: what you're allowed to sell

Nearly all of the 20 designs in the shop right now use other people's intellectual property:
One Piece (Luffy, Zoro, Nami, Shanks and the Wanted set), Naruto (Itachi), Solo Leveling,
Porsche (the crest and the "911" name), Dodge Viper, Messi's face, The Dark Knight and 007.
Selling prints of these without a licence is copyright and/or trademark infringement. In practice
that means:

- **Social accounts.** Instagram, TikTok and Meta ads take posts and ads down when rights-holders
  report them. Repeated reports can lose you the account your whole brand depends on.
- **Payments.** Stripe, PayPal and Shopify Payments all forbid infringing goods, and they can
  freeze your balance.
- **Marketplaces.** Etsy and Amazon remove listings and suspend shops.
- **You can't scale it.** You can't safely run ads, work with bigger creators, or sell to shops
  if the products aren't yours.

| Path | Risk | What it looks like |
|---|---|---|
| **A. Original designs** (recommended core) | Low | You own the art, so you can advertise anywhere and build a real brand. |
| **B. Licensed designs** | Low | Official licences from rights-holders or agencies. Costly, so it's a later-stage move. |
| **C. Fan art** | High | Strong demand, but it can be shut down at any time on any channel. |

**Recommendation:** build ONELINE around original work, and turn the name into the concept.

> **Every ONELINE poster carries one line.** That means one statement, printed small at the bottom
> in the brand typeface, next to the red line mark.

You can own this, it's easy to recognise in a feed, and it gives each design a caption people
quote and share. Original directions that fit what already sells for you:

- **Typographic statement posters.** Bold Anton type with a single line, like the hero
  ("Walls that say something.").
- **Car culture without brands.** Your own photos or illustrations of cars with no logos, badges
  or model names. Sell the mood (JDM night, track day, garage) rather than the manufacturer.
- **Anime-inspired originals.** Your own characters and worlds in the same graphic, streetwear
  style, with no existing characters.
- **Editorial "magazine cover" posters** like *BLUR Vol.03*, with your own models and photos.
- **City and local pride.** Your city's skyline, streets or slang as clean graphic posters.

*Not legal advice. If you plan to keep any fan art, talk to a local IP lawyer first.*

---

## 1. Brand identity (already built into the site)

| | |
|---|---|
| **Name** | ONELINE |
| **Promise** | Walls that say something. |
| **Logo** | `ONE — LINE` with the red line as the mark. The line can be used on its own as an icon. |
| **Colours** | Ink `#0b0b0c` · Paper `#f6f4ef` · Signal Red `#ff3b30` |
| **Type** | Anton (headlines, always uppercase) · Inter (everything else) |
| **Voice** | Short, confident, a little cheeky. One sentence beats three. |

**Protect the name before you spend money on it:**
- Search for existing "ONELINE" trademarks in poster or print classes (class 16) in your country,
  and in the WIPO Global Brand Database. If there's a clash, change the name now, not later.
- Claim the same handle everywhere (Instagram, TikTok, Pinterest, WhatsApp Business), for example
  `@oneline.posters`, and buy a matching domain.

---

## 2. Product & pricing

**Start focused:** 12–20 designs across 3–4 collections, with **A3 as the hero size** (best mix of
price and wall impact). Add designs in "drops" of 4–6 so you always have something new to post.

**Know your numbers for each size before launch:**

```
Cost per poster = print + packaging (tube or rigid mailer) + payment/COD fee
                + share of shipping you absorb + allowance for refused/damaged orders
Target: unframed price ≈ 3 × cost  (≈ 60–65% gross margin)
```

| Size | Print | Packaging | Fees | Shipping share | **Total cost** | Price now | Margin |
|---|---|---|---|---|---|---|---|
| A4 |  |  |  |  |  | 14.99 |  |
| A3 |  |  |  |  |  | 19.99 |  |
| A2 |  |  |  |  |  | 29.99 |  |
| Frame |  |  |  |  |  | +15 |  |

Fill this in with real supplier quotes, then set prices in `js/products.js`.
**Stress-test your offers:** "Buy 3 get 1 free" plus the 10% code makes 4 × A3 cost the customer
about 13.49 each, with free shipping. Make sure that worst case is still profitable.

**Cash on delivery:** a refused parcel costs you shipping both ways plus the print. So confirm
every order by phone or WhatsApp before printing, and track the refusal rate (section 9).

---

## 3. Production

| | Local print shop | Print-on-demand (Gelato, Printful, Prodigi) |
|---|---|---|
| Cost per poster | Lowest | Higher |
| Inventory and packing | You handle it | None, they ship |
| Best for | Local sales, COD, fast delivery | Selling abroad, testing designs |

- **Get samples from at least 2 suppliers**, in every size, on 2–3 papers. Pick by colour,
  blacks and paper feel. Then photograph the samples: they become your product photos.
- **The site makes promises your supplier has to meet:** 250gsm matte paper, fade-resistant
  pigment inks, dispatch within 48h, and a 30-day reprint or refund guarantee. If a promise isn't
  true, change the copy in `index.html`.
- **Print files:** every A size has the same proportions, so design once at A2 and scale down.

| Size | Pixels at 300 DPI | Add bleed |
|---|---|---|
| A2 | 4961 × 7016 | 3 mm per side, if your printer asks for it |
| A3 | 3508 × 4961 | |
| A4 | 2480 × 3508 | |

---

## 4. Photos & content bank (ready before launch day)

For each hero poster, shoot:
1. **On a real wall, framed**, in a styled room (bedroom, desk setup, living room).
2. **Close-up** of the paper texture and print detail.
3. **In hand**, to show scale.
4. **Size line-up**, with A4, A3 and A2 side by side.

Mockups are fine for day one, but real photos sell better, so swap them in as you go.
Before launch, have **30+ short videos** filmed and edited so you're never posting in a panic.

---

## 5. Where you sell

- **Website (this repo).** Host it free on GitHub Pages: repo **Settings → Pages → Deploy from a
  branch → `main` / root**. Add your own domain once you've bought it.
- **Instagram + TikTok.** This is where people will discover you.
- **WhatsApp Business.** Use the catalogue, quick replies for prices and delivery times, and labels
  for order status.
- **Pinterest.** Posters and room decor get steady, long-lasting traffic there. Pin every design.
- **In person.** Anime conventions, car meets, markets and pop-ups. Bring framed samples and a QR
  code to the site.

---

## 6. Marketing playbook

**Content that works for posters:**
1. **Wall transformations.** An empty wall, then the finished wall.
2. **"Pick one."** Three posters, and viewers comment their choice (great for engagement).
3. **Packing orders.** Rolling, tubing and sealing, with satisfying sound.
4. **Design process.** A timelapse from sketch to final print.
5. **Size and frame comparisons.** A4 vs A3 vs A2, framed vs unframed.
6. **The line.** Close-up on the one line of each poster, then "Which line is yours?"

**Cadence for the first 30 days:** 1 short video a day plus 3+ stories a day. Use the same visual
style every time (ink, paper and red, Anton captions).

**Creators:** send free posters to 10–20 micro-creators (5k–50k followers) in room decor, desk
setups, cars or streetwear. Give each one a personal discount code in `STORE.codes`, so the Google
Sheet's `CODE` column shows who actually drives sales.

**Launch mechanics:**
- **Numbered first drop**, for example 50 of each design, marked "Limited". Scarcity gives people a
  reason to buy now.
- **Waitlist.** The newsletter form offers 10% off (`ONELINE10`). Push it hard in the pre-launch
  weeks.
- **Bundles.** "Buy 3 get 1 free" is already automatic. Use it in every launch post.

---

## 7. 30-day launch timeline

**Week 1: Foundation**
- [ ] Make the IP decision (section 0) and choose the first 12–20 designs
- [ ] Do the trademark search, then claim the handles and domain
- [ ] Request samples from 2 suppliers
- [ ] Set up WhatsApp Business

**Week 2: Product & site**
- [ ] Choose the supplier, fill in the cost table, set prices
- [ ] Choose packaging (tubes or rigid mailers, branded sticker)
- [ ] Photograph the samples and replace the images in `images/`
- [ ] Set up the Google Sheet order inbox (`tools/google-sheet-orders.gs`)
- [ ] Deploy the site and place a test order from your phone

**Week 3: Pre-launch**
- [ ] Post daily teasers and push the waitlist
- [ ] Ship posters to creators, timed so they post during launch week
- [ ] Soft launch to friends and family: aim for the first 10 real orders, then ask for photos
      and reviews

**Week 4: Launch**
- [ ] Launch day: feed post, stories every few hours, message everyone on the waitlist
- [ ] Creator posts go live
- [ ] Turn real reviews into the Reviews section (see the checklist)
- [ ] End-of-week review: what sold, what didn't, what's next

---

## 8. Go-live checklist (website)

All settings are in **`js/products.js`**.

- [ ] `currency`, `SIZES` prices, `FRAMES` prices, `shippingCost`, `freeShippingFrom`
- [ ] `whatsapp`: your number, digits only with country code
- [ ] `orderEndpoint`: your Google Sheet web-app URL. **Without this or WhatsApp, you get no orders.**
- [ ] `payments`: only methods you can really accept (currently just cash on delivery)
- [ ] `email`: a real inbox (`hello@oneline.store` is a placeholder)
- [ ] `instagram`, plus the TikTok and Pinterest links in the `index.html` footer (currently `#`)
- [ ] `PRODUCTS`: final designs and photos, per your IP decision
- [ ] Reviews: the section is **hidden** because the old quotes were placeholders. Once you have real
      reviews, put them in, remove `hidden`, and add the nav links back
- [ ] Hero numbers ("20+ designs", "48h dispatch", "30-day guarantee") match what you can deliver
- [ ] Add a short Shipping, Returns & Privacy page. You collect names, phone numbers and
      addresses, so say how you use them
- [ ] Once you have a domain, make the `og:image` URL absolute so link previews show your poster
- [ ] Place a full test order on your phone and check it reaches the Sheet or WhatsApp

---

## 9. Numbers to check every week

| Metric | Why it matters |
|---|---|
| Orders & revenue | Is it growing week over week? |
| Average order value | Are bundles and frames working? |
| Conversion rate (orders ÷ visitors) | Is the site and the offer convincing? |
| COD confirmed / refused % | Refusals eat your margin. Confirm before printing. |
| Best sellers | Make more like these and drop what doesn't sell |
| Sales per creator code | Which creators to work with again |
