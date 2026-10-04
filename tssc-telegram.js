/* ============================================================================
   tssc-telegram.js  —  TSSC-TGJOIN-V4 (floating corner button)

   Shows a small "Join us on Telegram" button fixed to the bottom-left corner of
   the screen, on phones, tablets and computers. A soft ring pulses round the
   icon to catch the eye. It appears on every page that loads this file.

     x            shrinks it to just the round icon for the rest of the visit
     a tap on it  opens the channel, and the button then stays away for 14 days

   The in-page cards (<div data-tg-join="…">) are hidden while INLINE_CARDS is
   false. Set it to true to show them again as well.

   To change the channel, the wording or the corner, edit SETTINGS below — one
   place for every page.

   No network call, no Firestore read. Storage: one sessionStorage flag (shrunk)
   and one localStorage timestamp (tapped).
============================================================================ */
(function () {
  'use strict';

  /* ---- SETTINGS ---------------------------------------------------------- */
  var CHANNEL      = 'trickyssc';                   // t.me/<CHANNEL>
  var FLOATING     = true;                          // the corner button
  var INLINE_CARDS = false;                         // the cards inside the page
  var CORNER       = 'left';                        // 'left' or 'right' (back-to-top sits on the right)
  var FLOAT_TITLE  = 'Join us on Telegram';
  var FLOAT_TITLE_PHONE = 'Join Telegram';
  var FLOAT_SUB    = 'Daily quiz, PYQ and tricks. Free.';
  var SHOW_AFTER_MS = 1200;                         // wait this long after the page opens
  var QUIET_DAYS    = 14;                           // after a tap, stay away this many days
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

  /* ------------------------------------------------------------ corner button */
  var FCSS =
    '.tgf{position:fixed;' + (CORNER === 'right' ? 'right' : 'left') + ':16px;' +
      'bottom:calc(16px + env(safe-area-inset-bottom, 0px));z-index:990;' +
      "font-family:'Rajdhani',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;" +
      'opacity:0;transform:translateY(18px);transition:opacity .35s ease,transform .35s ease;pointer-events:none;}' +
    '.tgf.on{opacity:1;transform:none;pointer-events:auto;}' +
    '.tgf-a{position:relative;display:flex;align-items:center;gap:.6rem;background:#fff;border:1px solid #BAE6FD;' +
      'border-radius:999px;padding:6px 18px 6px 6px;box-shadow:0 8px 24px rgba(13,27,42,.20);' +
      'text-decoration:none !important;color:#0D1B2A;-webkit-tap-highlight-color:transparent;' +
      'animation:tgfNudge 7s ease-in-out 4s infinite;}' +
    '.tgf-a *{text-decoration:none !important;}' +
    '.tgf-a:hover{border-color:#229ED9;}' +
    '.tgf-a:focus-visible,.tgf-x:focus-visible{outline:3px solid #0D1B2A;outline-offset:2px;}' +
    '.tgf-ic{position:relative;flex:0 0 44px;width:44px;height:44px;border-radius:50%;background:#229ED9;' +
      'display:flex;align-items:center;justify-content:center;}' +
    '.tgf-ic svg{position:relative;z-index:1;width:22px;height:22px;fill:#fff;display:block;}' +
    /* the pulse: two rings that grow and fade, one second apart */
    ".tgf-ic:before,.tgf-ic:after{content:'';position:absolute;top:0;right:0;bottom:0;left:0;border-radius:50%;" +
      'border:2px solid #229ED9;opacity:0;animation:tgfPing 2.2s cubic-bezier(0,0,.2,1) infinite;pointer-events:none;}' +
    '.tgf-ic:after{animation-delay:1.1s;}' +
    '.tgf-tx{position:relative;z-index:1;display:flex;flex-direction:column;line-height:1.15;}' +
    '.tgf-t{font-weight:700;font-size:1.02rem;color:#0D1B2A;white-space:nowrap;}' +
    '.tgf-tp{display:none;}' +
    '.tgf-s{font-weight:600;font-size:.82rem;color:#4A5568;white-space:nowrap;margin-top:1px;}' +
    '.tgf-x{position:absolute;top:-9px;' + (CORNER === 'right' ? 'left' : 'right') + ':-6px;width:24px;height:24px;' +
      'border-radius:50%;border:2px solid #fff;padding:0;background:#0D1B2A;color:#fff;font:700 14px/1 Arial,sans-serif;' +
      'cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,.25);}' +
    /* a bigger invisible target round the small x, for thumbs */
    ".tgf-x:after{content:'';position:absolute;top:-10px;right:-10px;bottom:-10px;left:-10px;}" +
    /* shrunk: just the round icon */
    '.tgf.min .tgf-tx,.tgf.min .tgf-x{display:none;}' +
    '.tgf.min .tgf-a{padding:6px;animation:none;}' +
    '@keyframes tgfPing{0%{transform:scale(1);opacity:.7;}75%,100%{transform:scale(1.85);opacity:0;}}' +
    '@keyframes tgfNudge{0%,88%,100%{transform:translateY(0);}92%{transform:translateY(-6px);}' +
      '95%{transform:translateY(0);}97.5%{transform:translateY(-3px);}}' +
    '@media(max-width:520px){' +
      '.tgf{' + (CORNER === 'right' ? 'right' : 'left') + ':12px;bottom:calc(12px + env(safe-area-inset-bottom, 0px));}' +
      '.tgf-a{padding:5px 15px 5px 5px;gap:.5rem;}' +
      '.tgf-ic{flex-basis:42px;width:42px;height:42px;}' +
      '.tgf-td,.tgf-s{display:none;}' +
      '.tgf-tp{display:inline;}' +
      '.tgf.min .tgf-a{padding:5px;}' +
    '}' +
    '@media(prefers-reduced-motion:reduce){.tgf,.tgf-a,.tgf-ic:before,.tgf-ic:after{animation:none !important;transition:none !important;}}' +
    '@media print{.tgf{display:none !important;}}';

  function quiet() {
    try {
      var t = parseInt(localStorage.getItem('tsscTgTapped') || '0', 10);
      return t > 0 && (Date.now() - t) < QUIET_DAYS * 86400000;
    } catch (e) { return false; }
  }
  function shrunk() { try { return sessionStorage.getItem('tsscTgMin') === '1'; } catch (e) { return false; } }

  function floatButton() {
    if (!FLOATING || document.getElementById('tsscTgFloat') || quiet() || !document.body) return;
    var st = document.createElement('style');
    st.id = 'tsscTgFloatCSS'; st.textContent = FCSS;
    (document.head || document.documentElement).appendChild(st);

    var wrap = el('div', 'tgf' + (shrunk() ? ' min' : ''));
    wrap.id = 'tsscTgFloat';

    var a = el('a', 'tgf-a');
    a.href = URL; a.target = '_blank'; a.rel = 'noopener';
    a.setAttribute('aria-label', FLOAT_TITLE + '. ' + FLOAT_SUB);

    var ic = el('span', 'tgf-ic');
    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('aria-hidden', 'true');
    var p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    p.setAttribute('d', PLANE);
    svg.appendChild(p); ic.appendChild(svg);

    var tx = el('span', 'tgf-tx');
    var t = el('span', 'tgf-t');
    t.appendChild(el('span', 'tgf-td', FLOAT_TITLE));          // tablets and computers
    t.appendChild(el('span', 'tgf-tp', FLOAT_TITLE_PHONE));    // phones
    tx.appendChild(t);
    tx.appendChild(el('span', 'tgf-s', FLOAT_SUB));
    a.appendChild(ic); a.appendChild(tx);

    var x = el('button', 'tgf-x', '\u00D7');
    x.type = 'button';
    x.setAttribute('aria-label', 'Make this smaller');

    a.addEventListener('click', function () {
      try { localStorage.setItem('tsscTgTapped', String(Date.now())); } catch (e) {}
      try { if (typeof window.gtag === 'function') window.gtag('event', 'telegram_join_click', { place: 'float' }); } catch (e) {}
      setTimeout(function () { if (wrap.parentNode) wrap.parentNode.removeChild(wrap); }, 400);
    });
    x.addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      wrap.className = 'tgf on min';
      try { sessionStorage.setItem('tsscTgMin', '1'); } catch (err) {}
    });

    wrap.appendChild(a); wrap.appendChild(x);
    document.body.appendChild(wrap);
    setTimeout(function () { wrap.className += ' on'; }, SHOW_AFTER_MS);
  }

  function run() {
    var slots = document.querySelectorAll('[data-tg-join]');
    if (INLINE_CARDS) {
      if (!document.getElementById('tsscTgJoinCSS')) {
        var st = document.createElement('style');
        st.id = 'tsscTgJoinCSS'; st.textContent = CSS;
        (document.head || document.documentElement).appendChild(st);
      }
      for (var i = 0; i < slots.length; i++) draw(slots[i]);
    } else {
      for (var j = 0; j < slots.length; j++) slots[j].style.display = 'none';
    }
    floatButton();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();
