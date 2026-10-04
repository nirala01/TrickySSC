/* ============================================================================
   tssc-telegram.js  —  TSSC-TGJOIN-V1

   Draws the "Join us on Telegram" card wherever a page has

       <div data-tg-join="home | ca | pyq"> … </div>

   The plain link inside that div is what shows if this script does not load.
   To change the channel or the wording, edit the SETTINGS below — one place
   for every page.

   No network call, no storage, no Firestore read.
============================================================================ */
(function () {
  'use strict';

  /* ---- SETTINGS ---------------------------------------------------------- */
  var CHANNEL = 'trickyssc';                        // t.me/<CHANNEL>
  var TEXT = {
    home: ['Daily SSC practice on Telegram',
           'Morning quiz, a trick, one PYQ and current affairs. Free.'],
    ca:   ['Get this on Telegram every day',
           '8 PM: the day\u2019s one-liners. 7 AM: a 5-question quiz. Free.'],
    pyq:  ['One PYQ a day, as a quiz on Telegram',
           'Plus a daily trick, current affairs and a morning quiz. Free.']
  };
  /* ------------------------------------------------------------------------ */

  var URL = 'https://t.me/' + CHANNEL;
  var CSS =
    '.tgj{box-sizing:border-box;margin-bottom:1.1rem;}' +
    '.tgj-in{box-sizing:border-box;display:flex;align-items:center;gap:.85rem;background:#fff;' +
      'border:1px solid #BAE6FD;border-left:5px solid #229ED9;border-radius:14px;padding:.8rem 1rem;' +
      'box-shadow:0 2px 10px rgba(34,158,217,.12);font-family:inherit;text-align:left;}' +
    '.tgj-ic{flex:0 0 42px;width:42px;height:42px;border-radius:50%;background:#229ED9;display:flex;' +
      'align-items:center;justify-content:center;}' +
    '.tgj-ic svg{width:22px;height:22px;fill:#fff;display:block;}' +
    '.tgj-tx{flex:1 1 0;min-width:0;}' +
    '.tgj-h{font-weight:700;font-size:1.06rem;line-height:1.25;color:#0D1B2A;margin:0;}' +
    '.tgj-s{font-weight:500;font-size:.9rem;line-height:1.35;color:#4A5568;margin:.15rem 0 0;}' +
    '.tgj-b{flex:0 0 auto;display:inline-block;background:#229ED9;color:#fff !important;' +
      'text-decoration:none !important;font-weight:700;font-size:.98rem;line-height:1.2;padding:.6rem 1rem;' +
      'border-radius:10px;white-space:nowrap;}' +
    '.tgj-b:hover{background:#1B8AC0;}' +
    '.tgj-b:focus-visible{outline:3px solid #0D1B2A;outline-offset:2px;}' +
    '@media(max-width:520px){.tgj-in{flex-wrap:wrap;}.tgj-b{flex:1 1 100%;text-align:center;}}';

  var PLANE = 'M9.04 15.6l-.37 5.2c.53 0 .76-.23 1.04-.5l2.5-2.4 5.17 3.8c.95.52 1.62.25 1.88-.87' +
              'l3.4-15.98c.3-1.4-.5-1.95-1.43-1.6L1.2 9.6c-1.37.53-1.35 1.3-.23 1.64l5.14 1.6L18.06 5.3' +
              'c.56-.37 1.07-.17.65.2z';

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function draw(slot) {
    if (slot.__tgj) return;
    slot.__tgj = 1;
    var kind = slot.getAttribute('data-tg-join');
    var t = TEXT[kind] || TEXT.home;

    var card = el('div', 'tgj-in');
    var ic = el('div', 'tgj-ic');
    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('aria-hidden', 'true');
    var p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    p.setAttribute('d', PLANE);
    svg.appendChild(p); ic.appendChild(svg);

    var tx = el('div', 'tgj-tx');
    tx.appendChild(el('p', 'tgj-h', t[0]));
    tx.appendChild(el('p', 'tgj-s', t[1]));

    var a = el('a', 'tgj-b', 'Join @' + CHANNEL);
    a.href = URL; a.target = '_blank'; a.rel = 'noopener';
    a.addEventListener('click', function () {
      try { if (typeof window.gtag === 'function') window.gtag('event', 'telegram_join_click', { place: kind || 'home' }); } catch (e) {}
    });

    card.appendChild(ic); card.appendChild(tx); card.appendChild(a);
    slot.textContent = '';
    slot.className = (slot.className ? slot.className + ' ' : '') + 'tgj';
    slot.appendChild(card);
  }

  function run() {
    if (!document.getElementById('tsscTgJoinCSS')) {
      var st = document.createElement('style');
      st.id = 'tsscTgJoinCSS'; st.textContent = CSS;
      (document.head || document.documentElement).appendChild(st);
    }
    var slots = document.querySelectorAll('[data-tg-join]');
    for (var i = 0; i < slots.length; i++) draw(slots[i]);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();
