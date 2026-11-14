# ONELINE — Poster Store

A fast, responsive storefront for selling posters. Pure HTML/CSS/JS — no build step.

## Run locally
Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Features
- Hero, collections, marquee, reviews (hidden until you have real ones), FAQ, newsletter, footer
- Product grid with category filters, search, sort and wishlist
- Product view with size (A4 / A3 / A2), frame options and live frame preview
- Cart drawer (saved in the browser), free-shipping progress bar, automatic "Buy 3 get 1 free"
- Discount codes (e.g. newsletter welcome code, one code per creator/influencer)
- Checkout that sends orders to a Google Sheet (free) and/or WhatsApp
- Fully responsive (desktop, tablet, mobile)

> **Launching the brand?** Read [`LAUNCH_PLAN.md`](LAUNCH_PLAN.md) — strategy, pricing,
> production, marketing, a 30-day timeline and a go-live checklist.

## Customise
Everything is in **`js/products.js`**:
- `STORE` — currency, free-shipping threshold, shipping cost, WhatsApp number, email, Instagram
- `STORE.orderEndpoint` — where orders go (see below). **Set this or `whatsapp`, or you won't receive orders.**
- `STORE.payments` — payment methods shown at checkout (only list what you really accept)
- `STORE.codes` / `STORE.welcomeCode` — discount codes and the newsletter welcome code
- `SIZES` / `FRAMES` — prices
- `PRODUCTS` — add a poster by dropping an image in `images/` and adding one line

## Receiving orders
- **Google Sheet (free):** follow the steps at the top of `tools/google-sheet-orders.gs`, then paste
  the web-app URL into `STORE.orderEndpoint`. Every order (and newsletter sign-up) becomes a row,
  with a STATUS column to track New → Confirmed → Shipped → Delivered. Optional email alert per order.
- **Formspree:** paste a Formspree form URL into `STORE.orderEndpoint` instead.
- **WhatsApp:** set `STORE.whatsapp`. Customers get a "Confirm my order on WhatsApp" button with the
  full order and address pre-filled. Works on its own or alongside the Sheet.

## Going live
- Host for free on GitHub Pages (repo Settings → Pages → deploy from `main`), Netlify or Vercel.
- To take card payments later, connect Stripe / PayPal / a Shopify Buy Button and add the method
  to `STORE.payments`.
