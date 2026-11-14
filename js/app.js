/* ==========================================================
   ONELINE — storefront logic (no dependencies)
   ========================================================== */
(() => {
  "use strict";

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  const money = (n) => {
    const v = (Math.round(n * 100) / 100).toFixed(2);
    return STORE.currencyAfter ? `${v} ${STORE.currency.trim()}` : `${STORE.currency}${v}`;
  };
  const byId = Object.fromEntries(PRODUCTS.map((p) => [p.id, p]));
  const sizeById = Object.fromEntries(SIZES.map((s) => [s.id, s]));
  const frameById = Object.fromEntries(FRAMES.map((f) => [f.id, f]));
  const catLabel = (id) => (CATEGORIES.find((c) => c.id === id) || {}).label || id;
  const minPrice = Math.min(...SIZES.map((s) => s.price));

  /* ---------- Persistent state ---------- */
  const load = (k, d) => { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch { return d; } };
  const save = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} };

  let cart = load("oneline_cart", []).filter((i) => byId[i.id] && sizeById[i.size] && frameById[i.frame]);
  let wish = new Set(load("oneline_wish", []).filter((id) => byId[id]));

  const state = { cat: "all", q: "", sort: "featured" };

  /* ---------- Static bits ---------- */
  $$("[data-free-ship]").forEach((el) => (el.textContent = money(STORE.freeShippingFrom)));
  $("[data-year]").textContent = new Date().getFullYear();
  $("[data-mail]").href = `mailto:${STORE.email}`;
  $("[data-insta]").href = STORE.instagram;
  $$("[data-cat-count]").forEach((el) => {
    const n = PRODUCTS.filter((p) => p.cat === el.dataset.catCount).length;
    el.textContent = `${n} poster${n === 1 ? "" : "s"}`;
  });

  /* ---------- Filters ---------- */
  const filtersEl = $("[data-filters]");
  function renderFilters() {
    const chips = CATEGORIES.map((c) => {
      const n = c.id === "all" ? PRODUCTS.length : PRODUCTS.filter((p) => p.cat === c.id).length;
      return `<button class="chip ${state.cat === c.id ? "active" : ""}" role="tab" aria-selected="${state.cat === c.id}" data-cat="${c.id}">${c.label}<small>${n}</small></button>`;
    });
    if (wish.size) {
      chips.push(`<button class="chip ${state.cat === "wish" ? "active" : ""}" role="tab" aria-selected="${state.cat === "wish"}" data-cat="wish">♥ Wishlist<small>${wish.size}</small></button>`);
    }
    filtersEl.innerHTML = chips.join("");
  }
  filtersEl.addEventListener("click", (e) => {
    const b = e.target.closest("[data-cat]");
    if (!b) return;
    state.cat = b.dataset.cat;
    renderFilters();
    renderGrid();
  });

  /* ---------- Grid ---------- */
  const gridEl = $("[data-grid]");
  const heart = `<svg viewBox="0 0 24 24"><path d="M12 21s-7.5-4.6-9.5-9.3C1 8.2 3.3 4.5 7 4.5c2 0 3.6 1.1 5 3 1.4-1.9 3-3 5-3 3.7 0 6 3.7 4.5 7.2C19.5 16.4 12 21 12 21z"/></svg>`;
  const badgeText = { new: "New", best: "Bestseller", limited: "Limited" };

  function visibleProducts() {
    const q = state.q.trim().toLowerCase();
    let list = PRODUCTS.filter((p) => {
      if (state.cat === "wish") { if (!wish.has(p.id)) return false; }
      else if (state.cat !== "all" && p.cat !== state.cat) return false;
      if (!q) return true;
      return (p.name + " " + p.desc + " " + catLabel(p.cat)).toLowerCase().includes(q);
    });
    const order = PRODUCTS.map((p) => p.id);
    if (state.sort === "az") list.sort((a, b) => a.name.localeCompare(b.name));
    else if (state.sort === "za") list.sort((a, b) => b.name.localeCompare(a.name));
    else if (state.sort === "new") list.sort((a, b) => (b.badge === "new") - (a.badge === "new") || order.indexOf(a.id) - order.indexOf(b.id));
    else if (state.sort === "featured") list.sort((a, b) => (b.badge === "best") - (a.badge === "best") || order.indexOf(a.id) - order.indexOf(b.id));
    return list;
  }

  function renderGrid() {
    const list = visibleProducts();
    gridEl.innerHTML = list.map((p, i) => `
      <article class="card" style="animation-delay:${Math.min(i, 12) * 40}ms">
        <div class="card__media" data-open-product="${p.id}">
          ${p.badge ? `<span class="card__badge card__badge--${p.badge}">${badgeText[p.badge]}</span>` : ""}
          <button class="card__wish ${wish.has(p.id) ? "on" : ""}" data-wish="${p.id}" aria-label="${wish.has(p.id) ? "Remove from" : "Add to"} wishlist">${heart}</button>
          <img src="${p.img}" alt="${p.name} poster" loading="lazy" />
          <button class="card__quick" data-quick-add="${p.id}">Quick add — A3</button>
        </div>
        <div class="card__body">
          <div>
            <div class="card__cat">${catLabel(p.cat)}</div>
            <h3 class="card__name" data-open-product="${p.id}">${p.name}</h3>
          </div>
          <div class="card__price"><small>from</small>${money(minPrice)}</div>
        </div>
      </article>`).join("");

    const total = list.length;
    $("[data-results]").textContent = `${total} poster${total === 1 ? "" : "s"}${state.q ? ` for “${state.q}”` : ""}`;
    $("[data-empty]").hidden = total > 0;
  }

  gridEl.addEventListener("click", (e) => {
    const w = e.target.closest("[data-wish]");
    if (w) { e.stopPropagation(); toggleWish(w.dataset.wish); return; }
    const q = e.target.closest("[data-quick-add]");
    if (q) { e.stopPropagation(); addToCart(q.dataset.quickAdd, "a3", "none", 1); return; }
    const o = e.target.closest("[data-open-product]");
    if (o) openProduct(o.dataset.openProduct);
  });

  $("[data-sort]").addEventListener("change", (e) => { state.sort = e.target.value; renderGrid(); });
  $("[data-reset]").addEventListener("click", () => {
    state.cat = "all"; state.q = ""; $("[data-search-input]").value = "";
    renderFilters(); renderGrid();
  });

  // Collection tiles / footer links jump to a category
  $$("[data-go-cat]").forEach((a) => a.addEventListener("click", () => {
    state.cat = a.dataset.goCat;
    renderFilters(); renderGrid();
    closeAll();
  }));

  /* ---------- Search ---------- */
  const searchEl = $("[data-search]");
  const searchInput = $("[data-search-input]");
  $("[data-open-search]").addEventListener("click", () => {
    searchEl.classList.toggle("open");
    if (searchEl.classList.contains("open")) setTimeout(() => searchInput.focus(), 150);
  });
  $("[data-close-search]").addEventListener("click", () => searchEl.classList.remove("open"));
  let searchT;
  searchInput.addEventListener("input", () => {
    clearTimeout(searchT);
    searchT = setTimeout(() => {
      state.q = searchInput.value;
      if (state.q && state.cat === "wish") state.cat = "all";
      renderFilters(); renderGrid();
      if (state.q) $("#shop").scrollIntoView({ behavior: "smooth" });
    }, 220);
  });

  /* ---------- Wishlist ---------- */
  function toggleWish(id) {
    wish.has(id) ? wish.delete(id) : wish.add(id);
    save("oneline_wish", [...wish]);
    toast(wish.has(id) ? "Added to wishlist ♥" : "Removed from wishlist");
    if (state.cat === "wish" && !wish.size) state.cat = "all";
    updateWishCount(); renderFilters(); renderGrid();
  }
  function updateWishCount() {
    const el = $("[data-wish-count]");
    el.textContent = wish.size; el.hidden = !wish.size;
  }
  $("[data-filter-wish]").addEventListener("click", () => {
    if (!wish.size) { toast("Your wishlist is empty — tap ♥ on a poster"); return; }
    state.cat = "wish"; renderFilters(); renderGrid();
    $("#shop").scrollIntoView({ behavior: "smooth" });
  });

  /* ---------- Overlay / drawers / modals ---------- */
  const overlay = $("[data-overlay]");
  const panels = { cart: $("[data-cart]"), menu: $("[data-menu]"), modal: $("[data-modal]"), checkout: $("[data-checkout-modal]") };

  function open(name) {
    closeAll(true);
    panels[name].classList.add("open");
    panels[name].setAttribute("aria-hidden", "false");
    overlay.classList.add("show");
    document.body.classList.add("locked");
  }
  function closeAll(silent) {
    Object.values(panels).forEach((p) => { p.classList.remove("open"); p.setAttribute("aria-hidden", "true"); });
    if (!silent) { overlay.classList.remove("show"); document.body.classList.remove("locked"); }
  }
  overlay.addEventListener("click", () => closeAll());
  $$("[data-close]").forEach((b) => b.addEventListener("click", () => closeAll()));
  $$(".modal").forEach((m) => m.addEventListener("click", (e) => { if (e.target === m) closeAll(); }));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") { closeAll(); searchEl.classList.remove("open"); } });
  $("[data-open-cart]").addEventListener("click", () => open("cart"));
  $("[data-open-menu]").addEventListener("click", () => open("menu"));
  $$(".mobile-nav a").forEach((a) => a.addEventListener("click", () => closeAll()));

  /* ---------- Product modal ---------- */
  const pm = { id: null, size: "a3", frame: "none", qty: 1 };
  function pmPrice() { return sizeById[pm.size].price + frameById[pm.frame].price; }

  function renderPm() {
    const p = byId[pm.id];
    $("[data-pm-img]").src = p.img;
    $("[data-pm-img]").alt = `${p.name} poster`;
    $("[data-pm-cat]").textContent = catLabel(p.cat);
    $("[data-pm-title]").textContent = p.name;
    $("[data-pm-desc]").textContent = p.desc;
    $("[data-pm-price]").textContent = money(pmPrice() * pm.qty);
    $("[data-pm-qty]").textContent = pm.qty;
    $("[data-pm-frame]").className = `pm__frame${pm.frame !== "none" ? ` pm__frame--${pm.frame}` : ""}`;
    $("[data-pm-sizes]").innerHTML = SIZES.map((s) =>
      `<button class="opt__choice ${pm.size === s.id ? "active" : ""}" data-size="${s.id}"><b>${s.label} · ${money(s.price)}</b><span>${s.dims}</span></button>`).join("");
    $("[data-pm-frames]").innerHTML = FRAMES.map((f) =>
      `<button class="opt__choice ${pm.frame === f.id ? "active" : ""}" data-frame="${f.id}"><b>${f.label}</b><span>${f.price ? "+" + money(f.price) : "Included"}</span></button>`).join("");
  }
  function openProduct(id) {
    Object.assign(pm, { id, size: "a3", frame: "none", qty: 1 });
    renderPm();
    open("modal");
  }
  $("[data-pm-sizes]").addEventListener("click", (e) => { const b = e.target.closest("[data-size]"); if (b) { pm.size = b.dataset.size; renderPm(); } });
  $("[data-pm-frames]").addEventListener("click", (e) => { const b = e.target.closest("[data-frame]"); if (b) { pm.frame = b.dataset.frame; renderPm(); } });
  $("[data-pm-minus]").addEventListener("click", () => { pm.qty = Math.max(1, pm.qty - 1); renderPm(); });
  $("[data-pm-plus]").addEventListener("click", () => { pm.qty = Math.min(20, pm.qty + 1); renderPm(); });
  $("[data-pm-add]").addEventListener("click", () => {
    addToCart(pm.id, pm.size, pm.frame, pm.qty);
    open("cart");
  });

  /* ---------- Cart ---------- */
  const unitPrice = (i) => sizeById[i.size].price + frameById[i.frame].price;

  function totals() {
    const subtotal = cart.reduce((s, i) => s + unitPrice(i) * i.qty, 0);
    // Buy 3 get 1 free: cheapest unit in every group of 4 is free
    const units = cart.flatMap((i) => Array(i.qty).fill(unitPrice(i))).sort((a, b) => a - b);
    const free = Math.floor(units.length / 4);
    const discount = units.slice(0, free).reduce((s, v) => s + v, 0);
    const afterDiscount = subtotal - discount;
    const shipping = !cart.length || afterDiscount >= STORE.freeShippingFrom ? 0 : STORE.shippingCost;
    const count = units.length;
    return { subtotal, discount, shipping, total: afterDiscount + shipping, count, afterDiscount };
  }

  function addToCart(id, size, frame, qty) {
    const ex = cart.find((i) => i.id === id && i.size === size && i.frame === frame);
    ex ? (ex.qty = Math.min(50, ex.qty + qty)) : cart.push({ id, size, frame, qty });
    persistCart();
    toast(`Added “${byId[id].name}” (${sizeById[size].label}) to cart`);
    const c = $("[data-cart-count]");
    c.classList.remove("bump"); void c.offsetWidth; c.classList.add("bump");
  }
  function persistCart() { save("oneline_cart", cart); renderCart(); }

  function renderCart() {
    const t = totals();
    const countEl = $("[data-cart-count]");
    countEl.textContent = t.count; countEl.hidden = !t.count;
    $("[data-cart-count-text]").textContent = t.count ? `(${t.count})` : "";

    const itemsEl = $("[data-cart-items]");
    if (!cart.length) {
      itemsEl.innerHTML = `<div class="cart__empty">
        <svg viewBox="0 0 24 24"><path d="M5 7h14l-1.2 12.2a2 2 0 0 1-2 1.8H8.2a2 2 0 0 1-2-1.8L5 7z"/><path d="M9 7V6a3 3 0 0 1 6 0v1"/></svg>
        <p>Your cart is empty.</p>
        <a href="#shop" class="btn btn--primary" data-empty-shop>Start shopping</a></div>`;
      $("[data-empty-shop]").addEventListener("click", () => closeAll());
    } else {
      itemsEl.innerHTML = cart.map((i, idx) => {
        const p = byId[i.id];
        return `<div class="ci">
          <img src="${p.img}" alt="${p.name}" />
          <div>
            <p class="ci__name">${p.name}</p>
            <p class="ci__meta">${sizeById[i.size].label} · ${frameById[i.frame].label}</p>
            <div class="qty">
              <button aria-label="Decrease" data-ci-minus="${idx}">−</button>
              <span>${i.qty}</span>
              <button aria-label="Increase" data-ci-plus="${idx}">+</button>
            </div>
          </div>
          <div>
            <div class="ci__price">${money(unitPrice(i) * i.qty)}</div>
            <button class="ci__remove" data-ci-remove="${idx}">Remove</button>
          </div>
        </div>`;
      }).join("");
    }

    $("[data-cart-foot]").hidden = !cart.length;
    $("[data-subtotal]").textContent = money(t.subtotal);
    $("[data-discount-row]").hidden = !t.discount;
    $("[data-discount]").textContent = "−" + money(t.discount);
    $("[data-shipping]").textContent = t.shipping ? money(t.shipping) : "Free";
    $("[data-total]").textContent = money(t.total);

    const left = STORE.freeShippingFrom - t.afterDiscount;
    const pct = Math.min(100, (t.afterDiscount / STORE.freeShippingFrom) * 100);
    const fill = $("[data-ship-fill]");
    fill.style.width = pct + "%";
    fill.classList.toggle("full", left <= 0);
    $("[data-ship-msg]").innerHTML = left > 0
      ? `You’re <b>${money(left)}</b> away from <b>free shipping</b>`
      : `🎉 You’ve unlocked <b>free shipping</b>`;

    const wa = $("[data-whatsapp]");
    if (STORE.whatsapp && cart.length) {
      wa.hidden = false;
      const lines = cart.map((i) => `• ${byId[i.id].name} — ${sizeById[i.size].label}, ${frameById[i.frame].label} × ${i.qty}`);
      const msg = `Hi ${STORE.name}! I'd like to order:\n${lines.join("\n")}\n\nTotal: ${money(t.total)}`;
      wa.href = `https://wa.me/${STORE.whatsapp}?text=${encodeURIComponent(msg)}`;
    } else wa.hidden = true;
  }

  $("[data-cart-items]").addEventListener("click", (e) => {
    const t = e.target.closest("button");
    if (!t) return;
    if (t.dataset.ciPlus != null) cart[+t.dataset.ciPlus].qty = Math.min(50, cart[+t.dataset.ciPlus].qty + 1);
    else if (t.dataset.ciMinus != null) {
      const i = +t.dataset.ciMinus;
      cart[i].qty -= 1;
      if (cart[i].qty < 1) cart.splice(i, 1);
    } else if (t.dataset.ciRemove != null) cart.splice(+t.dataset.ciRemove, 1);
    else return;
    persistCart();
  });

  /* ---------- Checkout ---------- */
  $("[data-checkout]").addEventListener("click", () => {
    const t = totals();
    $("[data-co-summary]").innerHTML = `
      <div class="cart__row"><span>${t.count} poster${t.count === 1 ? "" : "s"}</span><span>${money(t.subtotal)}</span></div>
      ${t.discount ? `<div class="cart__row cart__row--discount"><span>Buy 3 get 1 free</span><span>−${money(t.discount)}</span></div>` : ""}
      <div class="cart__row"><span>Shipping</span><span>${t.shipping ? money(t.shipping) : "Free"}</span></div>
      <div class="cart__row"><span>Total</span><span>${money(t.total)}</span></div>`;
    $("[data-co-form-wrap]").hidden = false;
    $("[data-co-done]").hidden = true;
    open("checkout");
  });

  $("[data-co-form]").addEventListener("submit", (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target));
    const number = "OL-" + Date.now().toString(36).toUpperCase().slice(-6);
    // TODO: send `data` + `cart` to your backend / payment provider here.
    const orders = load("oneline_orders", []);
    orders.push({ number, date: new Date().toISOString(), customer: data, items: cart, totals: totals() });
    save("oneline_orders", orders);

    $("[data-co-number]").textContent = number;
    $("[data-co-email]").textContent = data.email;
    $("[data-co-form-wrap]").hidden = true;
    $("[data-co-done]").hidden = false;
    cart = []; persistCart(); e.target.reset();
  });

  /* ---------- Newsletter ---------- */
  $("[data-newsletter]").addEventListener("submit", (e) => {
    e.preventDefault();
    e.target.reset();
    toast("You’re in! Use code ONELINE10 for 10% off.");
  });

  /* ---------- Toast ---------- */
  let toastT;
  function toast(msg) {
    const el = $("[data-toast]");
    el.textContent = msg;
    el.classList.add("show");
    clearTimeout(toastT);
    toastT = setTimeout(() => el.classList.remove("show"), 2400);
  }

  /* ---------- Header shadow & reveal ---------- */
  const header = $(".header");
  const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 10);
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
    }), { threshold: 0.12 });
    $$(".section__head, .collection, .feature, .review, .faq details, .newsletter__inner").forEach((el) => { el.classList.add("reveal"); io.observe(el); });
  }

  /* ---------- Init ---------- */
  renderFilters();
  renderGrid();
  renderCart();
  updateWishCount();
})();
