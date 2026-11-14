/**
 * ONELINE — receive website orders & newsletter sign-ups in a Google Sheet.
 * Free, no server needed.
 *
 * SETUP (about 5 minutes)
 * 1. Create a new Google Sheet (go to sheets.new) and name it "ONELINE Orders".
 * 2. In the sheet: Extensions → Apps Script. Delete the sample code, paste this
 *    whole file, and click Save.
 * 3. Click Deploy → New deployment → gear icon → "Web app".
 *      Execute as:      Me
 *      Who has access:  Anyone
 *    Click Deploy, allow the permissions, and copy the Web app URL (it ends in /exec).
 * 4. Paste that URL into  orderEndpoint  in js/products.js.
 * 5. Place a test order on your site. A row should appear in the "Orders" tab.
 *
 * Optional: put your email in NOTIFY_EMAIL to get an email for every new order.
 * After editing this script: Deploy → Manage deployments → Edit (pencil) →
 * Version: "New version" → Deploy. The URL stays the same.
 *
 * Use the STATUS column to track each order: New → Confirmed → Shipped →
 * Delivered (or Refused / Returned). For cash-on-delivery, confirm every order
 * by phone or WhatsApp before you print it.
 */
const NOTIFY_EMAIL = ""; // e.g. "you@example.com"

const SHEETS = {
  order: {
    name: "Orders",
    columns: ["date", "order", "status", "name", "phone", "email", "address", "city", "zip",
              "payment", "items", "posters", "subtotal", "discount", "code", "shipping", "total"],
  },
  newsletter: {
    name: "Subscribers",
    columns: ["date", "email"],
  },
};

function doPost(e) {
  const p = (e && e.parameter) || {};
  const conf = SHEETS[p.type];
  if (!conf) return ContentService.createTextOutput("ignored");

  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(conf.name) || ss.insertSheet(conf.name);
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(conf.columns.map((c) => c.toUpperCase()));
      sheet.setFrozenRows(1);
    }
    sheet.appendRow(conf.columns.map((c) => {
      if (c === "date") return new Date();
      if (c === "status") return "New";
      return clean(p[c]);
    }));
  } finally {
    lock.releaseLock();
  }

  if (p.type === "order" && NOTIFY_EMAIL) {
    MailApp.sendEmail(
      NOTIFY_EMAIL,
      `New order ${clean(p.order)} — ${clean(p.total)}`,
      [
        `Order: ${p.order}`,
        `Customer: ${p.name} · ${p.phone} · ${p.email}`,
        `Address: ${p.address}, ${p.city} ${p.zip || ""}`,
        `Payment: ${p.payment}`,
        "",
        p.items,
        "",
        `Subtotal ${p.subtotal} · Discount ${p.discount}${p.code ? " (" + p.code + ")" : ""} · Shipping ${p.shipping}`,
        `TOTAL ${p.total}`,
      ].join("\n")
    );
  }
  return ContentService.createTextOutput("ok");
}

// Open the /exec URL in a browser to check the endpoint is live.
function doGet() {
  return ContentService.createTextOutput("ONELINE order endpoint is running.");
}

// Keep values as plain text: stops anything starting with = + - @ being run as a
// spreadsheet formula, and keeps phone numbers like +212… intact.
function clean(v) {
  v = v == null ? "" : String(v).slice(0, 2000);
  return /^[=+\-@]/.test(v) ? "'" + v : v;
}
