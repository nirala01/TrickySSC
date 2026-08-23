/* ============================================================================
   tssc-pricing.js — reads the live pricing catalog from Firestore.

   PRICES ARE DATA, NOT CODE. Everything below is loaded from the single
   Firestore document `config/pricing`, which you edit in admin-pricing.html.
   Changing a price, adding a combo or launching a new module needs no file
   edit, no commit and no deploy.

   ── The two concepts, and why they are separate ─────────────────────────
   ENTITLEMENT KEY   an atomic unlockable thing. "ssc-cgl-mocks".
                     Written into entitlements/{uid}.modules[key].
                     Pages ask "does this user hold key X?".
                     NEVER rename one once it has been sold — that orphans
                     every entitlement already granted under the old name.

   PRODUCT           something a buyer can pay for. Has a price, and GRANTS
                     one or more entitlement keys.

   A combo is just a product that grants several keys — no special case
   anywhere in the code:

       product p-mocks    ₹49  grants [ssc-cgl-mocks]
       product p-chapter  ₹49  grants [ssc-cgl-chapter]
       product p-combo    ₹79  grants [ssc-cgl-mocks, ssc-cgl-chapter]

   Selling quant and reasoning separately later is the same move: add keys
   ssc-cgl-chapter-quant / -reasoning, add a ₹29 product for each, and
   optionally a combo granting both. No code changes.

   ── Who reads this ──────────────────────────────────────────────────────
   The browser reads it to DISPLAY prices. The trickyssc-pay Worker reads the
   SAME document server-side to decide what to CHARGE. One source of truth,
   so the two can never drift. A price sent up from a browser is ignored.

   Cost note: one Firestore read per user per 10 minutes (sessionStorage
   cached), not one per page view.
============================================================================ */
(function (root) {
  'use strict';

  var PROJECT = 'trickyssc-17bb3';
  var API_KEY = 'AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA';   // public web key
  var DOC = 'config/pricing';
  var CACHE_KEY = 'tssc_pricing_v1';
  var CACHE_TTL = 10 * 60 * 1000;

  /* Last-resort catalog, used only if Firestore is unreachable AND nothing is
     cached. Keeps the page from rendering a priceless card. The Worker still
     charges from Firestore, so a stale fallback can never mis-charge. */
  var FALLBACK = {
    version: 0,
    fallback: true,
    entitlements: {
      'ssc-cgl-mocks': { label: 'SSC CGL Mock Tests', exam: 'ssc-cgl' }
    },
    products: [
      { id: 'p-ssc-cgl-mocks', label: 'SSC CGL Mock Test Series', exam: 'ssc-cgl',
        grants: ['ssc-cgl-mocks'], price: 49, mrp: 199, durationDays: 365,
        live: true, order: 1,
        blurb: 'All 50 Tier I + all 50 Tier II mocks, including every mock released during the year.' }
    ]
  };

  /* ---- Firestore REST returns typed values; flatten them to plain JS ---- */
  function decode(v) {
    if (v == null) return null;
    if ('stringValue'    in v) return v.stringValue;
    if ('integerValue'   in v) return parseInt(v.integerValue, 10);
    if ('doubleValue'    in v) return Number(v.doubleValue);
    if ('booleanValue'   in v) return v.booleanValue;
    if ('timestampValue' in v) return v.timestampValue;
    if ('nullValue'      in v) return null;
    if ('arrayValue'     in v) return (v.arrayValue.values || []).map(decode);
    if ('mapValue'       in v) return decodeFields(v.mapValue.fields || {});
    return null;
  }
  function decodeFields(f) {
    var out = {};
    for (var k in f) if (Object.prototype.hasOwnProperty.call(f, k)) out[k] = decode(f[k]);
    return out;
  }

  function readCache() {
    try {
      var o = JSON.parse(sessionStorage.getItem(CACHE_KEY) || 'null');
      if (o && Date.now() - o.ts < CACHE_TTL && o.data) return o.data;
    } catch (e) {}
    return null;
  }
  function writeCache(data) {
    try { sessionStorage.setItem(CACHE_KEY, JSON.stringify({ ts: Date.now(), data: data })); }
    catch (e) {}
  }

  /** Force the next read to hit Firestore. Call after editing prices. */
  function bust() {
    try { sessionStorage.removeItem(CACHE_KEY); } catch (e) {}
  }

  function normalise(raw) {
    var cat = raw || {};
    cat.payApi = cat.payApi || '';        // payment server address
    cat.entitlements = cat.entitlements || {};
    cat.products = (cat.products || []).map(function (p, i) {
      p.grants = p.grants || [];
      p.price = Number(p.price) || 0;
      p.mrp = p.mrp ? Number(p.mrp) : null;
      p.durationDays = Number(p.durationDays) || 365;
      p.order = (p.order == null ? i + 1 : Number(p.order));
      return p;
    });
    return cat;
  }

  function fetchCatalog() {
    var url = 'https://firestore.googleapis.com/v1/projects/' + PROJECT +
              '/databases/(default)/documents/' + DOC + '?key=' + API_KEY;
    return fetch(url)
      .then(function (r) {
        if (!r.ok) throw new Error('pricing HTTP ' + r.status);
        return r.json();
      })
      .then(function (j) {
        if (!j.fields) throw new Error('config/pricing has no fields');
        var cat = normalise(decodeFields(j.fields));
        if (!cat.products.length) throw new Error('config/pricing has no products');
        writeCache(cat);
        return cat;
      });
  }

  var _promise = null;

  /** Resolves to the catalog. Cached; safe to call repeatedly. */
  function load(force) {
    if (force) { bust(); _promise = null; }
    if (_promise) return _promise;
    var cached = readCache();
    if (cached) { _promise = Promise.resolve(normalise(cached)); return _promise; }
    _promise = fetchCatalog().catch(function (e) {
      console.warn('[pricing] falling back to baked catalog:', e.message);
      return normalise(JSON.parse(JSON.stringify(FALLBACK)));
    });
    return _promise;
  }

  // ---- query helpers, all taking the resolved catalog ----

  /** Live products for an exam, in display order. */
  function productsFor(cat, exam) {
    return cat.products
      .filter(function (p) { return p.live !== false && (!exam || p.exam === exam); })
      .sort(function (a, b) { return a.order - b.order; });
  }

  /** Live products that unlock a given entitlement key (singles AND combos). */
  function productsGranting(cat, key) {
    return cat.products
      .filter(function (p) { return p.live !== false && p.grants.indexOf(key) !== -1; })
      .sort(function (a, b) { return a.order - b.order; });
  }

  /** The product to lead with for a key: cheapest that grants it. */
  function bestFor(cat, key) {
    var all = productsGranting(cat, key);
    if (!all.length) return null;
    return all.slice().sort(function (a, b) { return a.price - b.price; })[0];
  }

  /** Combos = products granting this key plus something else. */
  function combosFor(cat, key) {
    return productsGranting(cat, key).filter(function (p) { return p.grants.length > 1; });
  }

  function product(cat, id) {
    return cat.products.filter(function (p) { return p.id === id; })[0] || null;
  }

  root.TSSC_PRICING = {
    load: load,
    bust: bust,
    decodeFields: decodeFields,
    normalise: normalise,
    FALLBACK: FALLBACK,
    productsFor: productsFor,
    productsGranting: productsGranting,
    bestFor: bestFor,
    combosFor: combosFor,
    product: product
  };
})(window);
