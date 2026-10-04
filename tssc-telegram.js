/* ============================================================================
   tssc-telegram.js  —  TSSC-TGJOIN-V3 (phone and tablet layouts; whole card is the link)

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
  /* each: [ title, line shown on tablets and computers, shorter line shown on phones ] */
  var TEXT = {
    home: ['Daily SSC practice on Telegram',
           'Morning quiz, a trick, one PYQ and current affairs. Free.',
           'Quiz, trick, PYQ and news. Free.'],
    ca:   ['Get this on Telegram every day',
           '8 PM: the day\u2019s one-liners. 7 AM: a 5-question quiz. Free.',
           '8 PM one-liners, 7 AM quiz. Free.'],
    pyq:  ['One PYQ a day, as a quiz on Telegram',
           'Plus a daily trick, current affairs and a morning quiz. Free.',
           'Plus quiz, tricks and news. Free.']
  };
  /* ------------------------------------------------------------------------ */

  var URL = 'https://t.me/' + CHANNEL;
  var CSS =
    '.tgj{box-sizing:border-box;margin-bottom:1.1rem;}' +
    /* the whole card is one link, so it is an easy target for a thumb */
    '.tgj-in{box-sizing:border-box;display:flex;align-items:center;gap:.85rem;background:#fff;' +
      'border:1px solid #BAE6FD;border-left:5px solid #229ED9;border-radius:14px;padding:.8rem 1rem;' +
      'box-shadow:0 2px 10px rgba(34,158,217,.12);font-family:inherit;text-align:left;' +
      'text-decoration:none !important;color:inherit;cursor:pointer;-webkit-tap-highlight-color:transparent;}' +
    '.tgj-in *{text-decoration:none !important;}' +
    '.tgj-in:focus-visible{outline:3px solid #0D1B2A;outline-offset:2px;}' +
    '.tgj-ic{flex:0 0 42px;width:42px;height:42px;border-radius:50%;background:#229ED9;display:flex;' +
      'align-items:center;justify-content:center;}' +
    '.tgj-ic svg{width:22px;height:22px;fill:#fff;display:block;}' +
    '.tgj-tx{flex:1 1 0;min-width:0;}' +
    '.tgj-h{font-weight:700;font-size:1.06rem;line-height:1.25;color:#0D1B2A;margin:0;padding:0;max-width:none;}' +
    '.tgj-s{display:block;}' +
    '.tgj-s,.tgj-sm{font-weight:500;font-size:.9rem;line-height:1.35;color:#4A5568;margin:.15rem 0 0;padding:0;max-width:none;}' +
    '.tgj-sm{display:none;}' +
    '.tgj-b{flex:0 0 auto;box-sizing:border-box;display:inline-flex;align-items:center;justify-content:center;' +
      'min-height:44px;background:#229ED9;color:#fff !important;font-weight:700;font-size:.98rem;line-height:1.2;' +
      'padding:.55rem 1rem;border-radius:10px;white-space:nowrap;}' +
    '.tgj-in:hover .tgj-b{background:#1B8AC0;}' +
    /* homepage: line up with the chapter-wise card above it once the hero stacks */
    '@media(max-width:1024px){.hero [data-tg-join]{max-width:560px;}}' +
    /* phones: one compact row — icon, two short lines, a "Join" button */
    '@media(max-width:520px){' +
      '.tgj-in{gap:.65rem;padding:.65rem .75rem;border-radius:12px;}' +
      '.tgj-ic{flex-basis:38px;width:38px;height:38px;}' +
      '.tgj-ic svg{width:20px;height:20px;}' +
      '.tgj-h{font-size:1rem;}' +
      '.tgj-s{display:none;}' +
      '.tgj-sm{display:block;font-size:.84rem;}' +
      '.tgj-bh{display:none;}' +
      '.tgj-b{padding:.5rem .95rem;font-size:1rem;}' +
    '}' +
    '@media(max-width:360px){.tgj-h{font-size:.95rem;}.tgj-in{gap:.55rem;padding:.6rem .65rem;}}';

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

    var card = el('a', 'tgj-in');
    card.href = URL; card.target = '_blank'; card.rel = 'noopener';
    card.setAttribute('aria-label', t[0] + '. Join @' + CHANNEL + ' on Telegram');
    card.addEventListener('click', function () {
      try { if (typeof window.gtag === 'function') window.gtag('event', 'telegram_join_click', { place: kind || 'home' }); } catch (e) {}
    });

    var ic = el('span', 'tgj-ic');
    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('aria-hidden', 'true');
    var p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    p.setAttribute('d', PLANE);
    svg.appendChild(p); ic.appendChild(svg);

    /* spans, not <p>: some pages style every <p> inside their hero */
    var tx = el('span', 'tgj-tx');
    var h = el('span', 'tgj-h', t[0]);          h.style.display = 'block';
    var s1 = el('span', 'tgj-s', t[1]);
    var s2 = el('span', 'tgj-sm', t[2] || t[1]);
    tx.appendChild(h); tx.appendChild(s1); tx.appendChild(s2);

    var btn = el('span', 'tgj-b');
    btn.appendChild(document.createTextNode('Join'));
    btn.appendChild(el('span', 'tgj-bh', '\u00A0@' + CHANNEL));

    card.appendChild(ic); card.appendChild(tx); card.appendChild(btn);
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
