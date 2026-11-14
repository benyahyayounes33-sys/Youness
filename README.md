# ONELINE — Poster Store

A fast, responsive storefront for selling posters. Pure HTML/CSS/JS — no build step.

## Run locally
Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Features
- Hero, collections, marquee, reviews, FAQ, newsletter, footer
- Product grid with category filters, search, sort and wishlist
- Product view with size (A4 / A3 / A2), frame options and live frame preview
- Cart drawer (saved in the browser), free-shipping progress bar, automatic "Buy 3 get 1 free"
- Checkout form (cash on delivery / card / PayPal) and optional "Order on WhatsApp"
- Fully responsive (desktop, tablet, mobile)

## Customise
Everything is in **`js/products.js`**:
- `STORE` — currency, free-shipping threshold, shipping cost, WhatsApp number, email, Instagram
- `SIZES` / `FRAMES` — prices
- `PRODUCTS` — add a poster by dropping an image in `images/` and adding one line

## Going live
- Host for free on GitHub Pages, Netlify or Vercel (just upload the folder).
- The checkout currently saves orders in the browser only. To take real payments,
  connect Stripe / PayPal / Shopify Buy Button, or use the WhatsApp ordering option
  (see the `TODO` in `js/app.js`).
