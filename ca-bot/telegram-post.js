#!/usr/bin/env node
/* ============================================================================
   ca-bot/telegram-post.js  —  TSSC-TELEGRAM-V4

   Posts TrickySSC's daily current affairs to the Telegram channel. It reads a
   page the CA bot has ALREADY written (ca-archive/DD-MM-YYYY.html), so it
   never calls Gemini or PIB and costs nothing to run.

     node ca-bot/telegram-post.js digest   the "Today at a glance" lines + link
     node ca-bot/telegram-post.js quiz     5 of the page's MCQs as quiz polls
     node ca-bot/telegram-post.js trick    the next Trick of the Day (ca-bot/tricks.json)
     node ca-bot/telegram-post.js mock     the Sunday free-mock challenge
     node ca-bot/telegram-post.js noon     Sunday → mock, any other day → trick
     node ca-bot/telegram-post.js pyq      PYQ of the Day: one real question as a quiz poll

   The trick and mock posts need no page and no network read: the tricks are a
   fixed list that is walked through one a day and then starts again.

   PYQ of the Day reads its questions from the CSV files named
   ca-bot/pyq-*.csv — ordinary "questions-EN" CSVs, the same ones the batch
   uploader takes. It makes NO database read (the site's security rules keep
   the question bank for logged-in users, and this bot does not log in).
   To give it more questions, upload another questions-EN CSV into ca-bot/
   with a name that starts with "pyq-". Best is the paper's own ID, e.g.
       pyq-ssc-chsl_2024_tier1_shift-1_2024-07-02_en.csv
   so the post can link to that exact paper; any other name still works and
   links to the paper named in the CSV's "concept" column, or to the PYQ page.
   Questions with a figure, formula markup or a passage are skipped. Subjects
   follow the weekday (PYQ_DAYS); SSC CGL and SSC CHSL alternate by day when
   the CSVs cover both. Each question is used once before any repeats.

   Needs two repo secrets (Settings → Secrets and variables → Actions):
     TELEGRAM_BOT_TOKEN   the token @BotFather gave you
     TELEGRAM_CHAT_ID     the channel, written as @yourchannel
   The bot must be an ADMIN of the channel with "Post messages" allowed.
   If either secret is missing the script logs a line and exits cleanly, so
   the workflows are safe to upload before the channel exists.

   Optional environment:
     TG_FILE     page to post, e.g. 03-10-2026.html (default: the newest page)
     DRY_RUN     "true" prints what would be sent and sends nothing
     TG_MANUAL   "true" (a hand-run) skips the "is the page fresh?" check
============================================================================ */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT    = path.join(__dirname, '..');
const ARCHIVE = path.join(ROOT, 'ca-archive');
const SITE    = 'https://trickyssc.com';
const MOCKS   = SITE + '/ssc-cgl-mock-test';

/* ---- SETTINGS ------------------------------------------------------------ */
const QUIZ_COUNT = 5;                        // MCQs posted as polls each morning
const TRICKS_FILE = path.join(__dirname, 'tricks.json');
const TRICK_START = '2026-10-05';            // the day trick no. 1 is posted (IST)
const FREE_MOCKS  = 4;                       // Mock 1..4 are free; Sunday rotates through them
/* PYQ of the Day */
const PYQ_PREFIX = 'pyq-';                   // ca-bot/pyq-*.csv are the question files
const PYQ_START  = '2026-10-05';             // counting starts here, so no question repeats early
const PYQ_PAGES  = [                         // exams alternate day by day, in this order
  { exam: 'SSC CGL',  key: 'ssc-cgl',  file: 'ssc-cgl-pyq.html',  hub: SITE + '/ssc-cgl-pyq.html' },
  { exam: 'SSC CHSL', key: 'ssc-chsl', file: 'ssc-chsl-pyq.html', hub: SITE + '/ssc-chsl-pyq.html' },
];
const PYQ_DAYS   = ['gk', 'quant', 'reasoning', 'english', 'gk', 'quant', 'english'];   // Sunday … Saturday
const PYQ_LABEL  = { quant: 'Maths', reasoning: 'Reasoning', english: 'English', gk: 'GK' };
const PRACTICE = {                           // where each trick sends people to practise
  Maths:     SITE + '/ssc-cgl-quant-chapter-wise-test.html',
  Reasoning: SITE + '/ssc-cgl-reasoning-chapter-wise-test.html',
};
/* Launch-price line, shown under the digest until the switch. Keep these the
   same as the SETTINGS in /tssc-launch-price.js. */
const INTRO = 49, REGULAR = 99;
const SWITCH_AT = Date.parse('2026-10-11T00:00:00+05:30');
const FIRST_DAY = '11 Oct';
/* -------------------------------------------------------------------------- */

const TOKEN  = (process.env.TELEGRAM_BOT_TOKEN || '').trim();
const CHAT   = (process.env.TELEGRAM_CHAT_ID || '').trim();
const DRY    = /^(1|true|yes)$/i.test(process.env.DRY_RUN || '');
const MANUAL = /^(1|true|yes)$/i.test(process.env.TG_MANUAL || '');
const API    = (process.env.TELEGRAM_API_BASE || 'https://api.telegram.org').replace(/\/+$/, '');
const MODE   = String(process.argv[2] || process.env.TG_MODE || 'digest').trim().toLowerCase();

const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
const log = (...a) => console.log('[telegram]', ...a);
const sleep = ms => new Promise(r => setTimeout(r, ms));

/* ---------------------------------------------------------------- the page */
const FILE_RE = /^(\d{2})-(\d{2})-(\d{4})\.html$/;

function pageInfo(name) {
  const m = FILE_RE.exec(name);
  if (!m) return null;
  const d = +m[1], mo = +m[2], y = +m[3];
  return { name, d, mo, y, key: y * 10000 + mo * 100 + d, long: `${d} ${MONTHS[mo - 1]} ${y}` };
}

function pickPage() {
  const asked = path.basename(String(process.env.TG_FILE || '').trim());
  if (asked) {
    const p = pageInfo(asked);
    if (!p) throw new Error(`TG_FILE "${asked}" is not a DD-MM-YYYY.html name`);
    if (!fs.existsSync(path.join(ARCHIVE, asked))) throw new Error(`ca-archive/${asked} does not exist`);
    return p;
  }
  const all = fs.readdirSync(ARCHIVE).map(pageInfo).filter(Boolean).sort((a, b) => b.key - a.key);
  if (!all.length) throw new Error('no daily pages found in ca-archive/');
  return all[0];
}

/* How many days old the page is, counted in IST calendar days. */
function ageInDays(p) {
  const nowIst = new Date(Date.now() + 5.5 * 3600 * 1000);
  const today = Date.UTC(nowIst.getUTCFullYear(), nowIst.getUTCMonth(), nowIst.getUTCDate());
  return Math.round((today - Date.UTC(p.y, p.mo - 1, p.d)) / 86400000);
}

const ENT = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', rsquo: '\u2019', lsquo: '\u2018',
              rdquo: '\u201D', ldquo: '\u201C', ndash: '\u2013', mdash: '\u2014', hellip: '\u2026' };
function decode(s) {
  return String(s)
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n))
    .replace(/&([a-z]+);/gi, (m, n) => (n.toLowerCase() in ENT ? ENT[n.toLowerCase()] : m));
}
const plain = html => decode(String(html).replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const clip = (s, n) => (s.length <= n ? s : s.slice(0, n - 1).trimEnd() + '\u2026');

function readGlance(html) {
  const ul = /<ul class="glist">([\s\S]*?)<\/ul>/.exec(html);
  if (!ul) return [];
  const out = [];
  const re = /<li[^>]*>([\s\S]*?)<\/li>/g;
  let m;
  while ((m = re.exec(ul[1]))) { const t = plain(m[1]); if (t) out.push(t); }
  return out;
}

/* Puts quotes round bare q / o / a / e keys, leaving everything inside strings alone. */
function quoteKeys(js) {
  let out = '', inStr = false, escNext = false, last = '';
  for (let i = 0; i < js.length; i++) {
    const c = js[i];
    if (inStr) {
      out += c;
      if (escNext) escNext = false;
      else if (c === '\\') escNext = true;
      else if (c === '"') inStr = false;
      continue;
    }
    if (c === '"') { inStr = true; out += c; last = c; continue; }
    if ((last === '{' || last === ',') && /[qoae]/.test(c) && /^\s*:/.test(js.slice(i + 1, i + 6))) {
      out += '"' + c + '"'; last = c; continue;
    }
    out += c;
    if (!/\s/.test(c)) last = c;
  }
  return out;
}

/* The page keeps its MCQs as a JSON array:  var QS=[ {q, o:[..], a:index, e}, ... ]; */
function readQuiz(html) {
  const at = html.indexOf('var QS=');
  if (at < 0) return [];
  const start = html.indexOf('[', at);
  let depth = 0, inStr = false, escNext = false, end = -1;
  for (let i = start; i < html.length; i++) {
    const c = html[i];
    if (inStr) {
      if (escNext) escNext = false;
      else if (c === '\\') escNext = true;
      else if (c === '"') inStr = false;
    } else if (c === '"') inStr = true;
    else if (c === '[') depth++;
    else if (c === ']') { depth--; if (depth === 0) { end = i; break; } }
  }
  if (start < 0 || end < 0) return [];
  const raw = html.slice(start, end + 1);
  let arr;
  try { arr = JSON.parse(raw); }
  catch (e1) {
    /* a hand-written page may use bare keys ({q:"..", o:[..], a:1, e:".."}) */
    try { arr = JSON.parse(quoteKeys(raw)); }
    catch (e2) { log('could not read the MCQs:', e2.message); return []; }
  }
  return (Array.isArray(arr) ? arr : []).map(x => ({
    q: plain(x && x.q || ''),
    o: (x && Array.isArray(x.o) ? x.o : []).map(plain),
    a: x && Number.isInteger(x.a) ? x.a : -1,
    e: plain(x && x.e || ''),
  }));
}

/* Telegram's limits for a quiz poll: question 300, 2-10 options of 100, explanation 200. */
function pollable(x) {
  return x.q && x.q.length <= 290 && x.o.length >= 2 && x.o.length <= 10 &&
         x.o.every(t => t && t.length <= 100) && x.a >= 0 && x.a < x.o.length;
}

/* -------------------------------------------------------------- the texts */
function promoLine() {
  const left = SWITCH_AT - Date.now();
  if (left > 0) {
    const days = Math.ceil(left / 86400000);
    const head = days <= 1 ? `\u23F3 <b>Last day at \u20B9${INTRO}</b>` : `\u23F3 <b>${days} days left at \u20B9${INTRO}</b>`;
    return `${head} \u2014 100 SSC CGL mock tests, \u20B9${REGULAR} from ${days <= 1 ? 'tomorrow' : FIRST_DAY}\n${MOCKS}`;
  }
  return `\uD83C\uDFAF 100 SSC CGL mock tests in real exam timing, Mock 1\u20134 free\n${MOCKS}`;
}

function digestText(p, lines, quizCount) {
  const url = `${SITE}/ca-archive/${p.name}`;
  const head = `\uD83D\uDDDE <b>Current Affairs \u00B7 ${esc(p.long)}</b>\n` +
               `<i>${lines.length} one-liners for SSC CGL, CHSL, MTS</i>\n\n`;
  const tail = `\n\n\uD83D\uDCDD Full notes${quizCount ? ` + ${quizCount} MCQs` : ''}:\n${url}\n\n${promoLine()}`;
  /* Telegram allows 4096 characters; drop lines from the end if a long day would overflow. */
  let body = lines.map(t => '\uD83D\uDD39 ' + esc(t));
  while (body.length > 1 && (head + body.join('\n\n') + tail).length > 3900) body.pop();
  return head + body.join('\n\n') + tail;
}

function quizHeader(p, n, total) {
  const url = `${SITE}/ca-archive/${p.name}#quiz`;
  const more = total > n ? `${total - n} more questions and the full notes:` : 'Full notes for these questions:';
  return `\u2600\uFE0F <b>Morning Quiz \u00B7 ${esc(p.long)}</b>\n` +
         `${n} current-affairs questions below. Tap an option to check your answer.\n\n${more}\n${url}`;
}

/* ------------------------------------------------- trick of the day, mock */
/* Today's date in IST as {y, mo, d, dow}; dow 0 = Sunday. */
function todayIst() {
  const forced = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(process.env.TG_DATE || '').trim());   // testing / back-posting
  const t = forced ? new Date(Date.UTC(+forced[1], +forced[2] - 1, +forced[3]))
                   : new Date(Date.now() + 5.5 * 3600 * 1000);
  return { y: t.getUTCFullYear(), mo: t.getUTCMonth() + 1, d: t.getUTCDate(), dow: t.getUTCDay(),
           utc: Date.UTC(t.getUTCFullYear(), t.getUTCMonth(), t.getUTCDate()) };
}

/* How many trick days (Monday to Saturday) have gone by since TRICK_START, today included. */
function trickNumber() {
  const start = Date.parse(TRICK_START + 'T00:00:00Z');
  const today = todayIst().utc;
  if (!(today >= start)) return 1;
  let n = 0;
  for (let t = start; t <= today; t += 86400000) if (new Date(t).getUTCDay() !== 0) n++;
  return Math.max(n, 1);
}

function loadTricks() {
  const arr = JSON.parse(fs.readFileSync(TRICKS_FILE, 'utf8'));
  const ok = (Array.isArray(arr) ? arr : []).filter(t => t && t.title && Array.isArray(t.lines) && t.lines.length && t.q && t.a);
  if (!ok.length) throw new Error('ca-bot/tricks.json has no usable tricks');
  return ok;
}

function trickText(t, no) {
  const link = PRACTICE[t.sub] || PRACTICE.Maths;
  return `\uD83E\uDDE0 <b>Trick of the Day #${no}</b> \u00B7 ${esc(t.topic || t.sub || 'SSC')}\n` +
         `<b>${esc(t.title)}</b>\n\n` +
         t.lines.map(esc).join('\n') +
         `\n\n\u270D\uFE0F <b>Try it:</b> ${esc(t.q)}\n` +
         `Answer (tap to reveal): <tg-spoiler>${esc(t.a)}</tg-spoiler>\n\n` +
         `Practise this chapter free:\n${link}`;
}

function mockText() {
  const week = Math.floor(todayIst().utc / (7 * 86400000));
  const n = (week % FREE_MOCKS) + 1;
  return `\uD83C\uDFAF <b>Sunday Mock Challenge</b>\n\n` +
         `Sit one full SSC CGL Tier I mock today, start to finish.\n` +
         `This week: <b>Mock ${n}</b>, free.\n\n` +
         `\uD83D\uDD39 100 questions, 60 minutes\n` +
         `\uD83D\uDD39 Real sectional timing, like the exam\n` +
         `\uD83D\uDD39 Score, rank and solutions at the end\n\n` +
         `Start here:\n${MOCKS}`;
}

/* ---------------------------------------------------------- PYQ of the day */
/* Small repeatable random generator, so a given date always picks the same question. */
function seeded(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
  let a = h >>> 0;
  return () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
                 t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}
function shuffled(arr, rnd) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}

/* English Tier I papers, read from the links the PYQ page builder already printed. */
function readPapers(file) {
  const html = fs.readFileSync(path.join(ROOT, file), 'utf8');
  const seen = new Set(), out = [];
  const re = /href="([^"]*(?:[?&]|&amp;)paperId=([^"&]+)[^"]*)"/g;
  let m;
  while ((m = re.exec(html))) {
    const url = decode(m[1]), pid = decodeURIComponent(m[2]);
    /* English, Tier I, and a real dated paper (…_2025-09-26_en) */
    if (!/_\d{4}-\d{2}-\d{2}_en$/.test(pid) || !/tier1/.test(pid) || seen.has(pid)) continue;
    seen.add(pid);
    const q = new URL(url, SITE).searchParams;
    out.push({ pid, url: new URL(url, SITE).href, year: q.get('year') || '', heldOn: q.get('heldOn') || '', shift: q.get('shift') || '' });
  }
  return out.sort((a, b) => (a.pid < b.pid ? -1 : 1));
}

function paperLabel(exam, p) {
  const d = /^(\d{4})-(\d{2})-(\d{2})$/.exec(p.heldOn);
  /* day and month only: the exam-cycle year is already in front, and some papers of a cycle
     were held in the following calendar year */
  const when = d ? `${+d[3]} ${MONTHS[+d[2] - 1].slice(0, 3)}` : '';
  const shift = p.shift ? p.shift.replace(/-/g, ' ') : '';
  return [`${exam} ${p.year}`.trim(), [when, shift].filter(Boolean).join(', ')].filter(Boolean).join(' \u00B7 ');
}

function canonSubject(s) {
  const t = String(s || '').toLowerCase();
  if (/reason|intelligence/.test(t)) return 'reasoning';
  if (/quant|math|numer|arith/.test(t)) return 'quant';
  if (/english|comprehension|language/.test(t)) return 'english';
  if (/aware|gk|knowledge|studies|science/.test(t)) return 'gk';
  return '';
}

/* The uploader's own line-break markers become real line breaks. */
function tidy(s) {
  return decode(String(s == null ? '' : s))
    .replace(/\[BR\]/gi, '\n').replace(/\|\|/g, '\n')
    .replace(/[ \t]+/g, ' ').replace(/ ?\n ?/g, '\n').replace(/\n{2,}/g, '\n').trim();
}

const MARKUP  = /<[a-z\/!][^>]*>|\\[a-zA-Z]+|\\\(|\\\[|\$\$|\^\{|_\{/i;             // HTML tags or formula markup
const NEEDS_MORE = /^\s*(passage|directions?)\b|\(\s*Q\.?\s*\d+\s*[\u2013\u2014-]\s*Q?\.?\s*\d+\s*\)|\b(passage|cloze)\b|read the following|study the following|\b(figure|diagram|venn|mirror image|water image|paper is folded|embedded|pie[- ]?chart|bar[- ]?graph|histogram|line[- ]?graph)\b|\b(given|following|above|below) (table|graph|chart|image|picture)\b|\b(table|graph|chart|image|picture) (given|below|above)\b|underlined|highlighted|in bold|bracketed|\b(as|is|are) shown\b|\bshown (below|above|in)\b|\bgiven (matrix|grid|dice|cube|shape|map)\b/i;

/* Returns a poll-ready question, or a short reason why this one cannot be shown as plain text. */
function pollFromDoc(d) {
  if (!d) return { skip: 'missing' };
  if (d.imageUrl) return { skip: 'has a figure' };
  const oi = d.optionImages;
  if (oi && typeof oi === 'object' && Object.keys(oi).some(k => oi[k])) return { skip: 'options are images' };
  const rawQ = String(d.text || d.question || '');
  const o = d.options && typeof d.options === 'object' ? d.options : {};
  const rawOpts = ['A', 'B', 'C', 'D'].map(k => String(o[k] != null ? o[k] : (d['option_' + k] != null ? d['option_' + k] : (d['option' + k] || ''))));
  if (MARKUP.test(rawQ) || rawOpts.some(x => MARKUP.test(x))) return { skip: 'formula or HTML markup' };
  if (NEEDS_MORE.test(rawQ)) return { skip: 'needs a passage, figure or highlighted text' };
  const q = tidy(rawQ), opts = rawOpts.map(x => tidy(x).replace(/\n/g, ' '));
  if (q.length < 12 || q.length > 290) return { skip: `question length ${q.length}` };
  if (q.split('\n').length > 8) return { skip: 'too many lines' };
  if (opts.some(x => !x || x.length > 100)) return { skip: 'an option is empty or too long' };
  if (new Set(opts.map(x => x.toLowerCase())).size !== 4) return { skip: 'duplicate options' };
  let c = String(d.correct == null ? '' : d.correct).trim().toUpperCase();
  if (/^[1-4]$/.test(c)) c = 'ABCD'[+c - 1];
  const idx = 'ABCD'.indexOf(c);
  if (c.length !== 1 || idx < 0) return { skip: 'no answer key' };
  /* explanation: plain text, whole sentences only, within Telegram's 200 characters */
  let e = '';
  const rawE = String(d.explanation || '');
  if (rawE && !/\\[a-zA-Z]+|\\\(|\\\[|\$\$/.test(rawE)) {
    const flat = tidy(rawE.replace(/<[^>]+>/g, ' ')).replace(/\n/g, ' ');
    if (flat.length <= 200) e = flat;
    else {
      const parts = flat.match(/[^.!?]+[.!?]+(\s|$)/g) || [];
      for (const s of parts) { if ((e + s).trim().length > 200) break; e += s; }
      e = e.trim();
    }
  }
  return { q, opts, idx, e, qNum: d.qNum };
}

/* A small CSV reader (quoted fields, doubled quotes, line breaks inside quotes). */
function parseCsv(text) {
  const t = String(text).replace(/^\uFEFF/, '');
  const rows = []; let row = [], f = '', q = false;
  for (let i = 0; i < t.length; i++) {
    const c = t[i];
    if (q) { if (c === '"') { if (t[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += c; }
    else if (c === '"') q = true;
    else if (c === ',') { row.push(f); f = ''; }
    else if (c === '\n') { row.push(f); rows.push(row); row = []; f = ''; }
    else if (c !== '\r') f += c;
  }
  if (f.length || row.length) { row.push(f); rows.push(row); }
  if (!rows.length) return [];
  const head = rows[0].map(h => h.trim());
  return rows.slice(1).filter(r => r.some(v => v && v.trim()))
             .map(r => { const o = {}; head.forEach((k, i) => { o[k] = r[i] || ''; }); return o; });
}

const MON3 = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'];

/* Works out which paper a CSV belongs to: from its file name if that is a paper ID, otherwise
   from the tail of the "concept" column ("… — SSC CGL 2025 Sep 26 Shift 1"). */
function findPaper(name, rows, papers) {
  const id = name.slice(PYQ_PREFIX.length).replace(/\.csv$/i, '').toLowerCase();
  let hit = papers.find(p => p.pid === id);
  if (hit) return hit;
  for (const r of rows.slice(0, 5)) {
    const m = /SSC\s+(CGL|CHSL)\s+(\d{4})\s+([A-Za-z]{3})[a-z]*\s+(\d{1,2})\s+Shift\s*(\d)/i.exec(r.concept || '');
    if (!m) continue;
    const mo = MON3.indexOf(m[3].toLowerCase()) + 1;
    if (!mo) continue;
    const re = new RegExp(`^ssc-${m[1].toLowerCase()}_${m[2]}_tier1_shift-${m[5]}_\\d{4}-${String(mo).padStart(2, '0')}-${String(m[4]).padStart(2, '0')}_en$`);
    hit = papers.find(p => re.test(p.pid));
    if (hit) return hit;
  }
  return null;
}

/* Every question in ca-bot/pyq-*.csv that is safe to show as plain text. */
function loadPool() {
  const files = fs.readdirSync(__dirname).filter(n => n.toLowerCase().startsWith(PYQ_PREFIX) && /\.csv$/i.test(n)).sort();
  const pool = [];
  for (const name of files) {
    const rows = parseCsv(fs.readFileSync(path.join(__dirname, name), 'utf8'));
    if (!rows.length) { log(`${name}: no rows, skipped`); continue; }
    const examKey = /chsl/i.test(name + ' ' + (rows[0].exam || '') + ' ' + (rows[0].concept || '')) ? 'ssc-chsl' : 'ssc-cgl';
    const src = PYQ_PAGES.find(x => x.key === examKey);
    const paper = findPaper(name, rows, readPapers(src.file));
    let n = 0;
    for (const r of rows) {
      const poll = pollFromDoc({
        qNum: parseInt(r.qNum, 10) || 0, subject: r.subject, text: r.text, explanation: r.explanation,
        options: { A: r.option_A, B: r.option_B, C: r.option_C, D: r.option_D }, correct: r.correct,
        imageUrl: r.imageUrl || r.image || '',
      });
      const subject = canonSubject(r.subject);
      if (poll.skip || !subject) continue;
      pool.push({ id: `${name}#${poll.qNum}`, src, subject, paper, year: String(r.year || '').trim(), poll });
      n++;
    }
    log(`${name}: ${n} of ${rows.length} questions usable${paper ? '' : ' (paper not matched: posts will link to the PYQ page)'}`);
  }
  return pool;
}

/* Finds today's question. Returns { exam, subject, paper, hub, year, poll } or throws. */
function pickPyq() {
  const pool = loadPool();
  if (!pool.length) throw new Error(`no usable questions: upload a questions-EN CSV into ca-bot/ named ${PYQ_PREFIX}….csv`);
  const day = todayIst();
  const subject = PYQ_DAYS[day.dow];
  let cands = pool.filter(x => x.subject === subject);
  if (!cands.length) throw new Error(`no usable ${PYQ_LABEL[subject]} question in the CSVs`);
  /* Which exam a given day uses: the one whose turn it is, or the other one if the CSVs
     hold no question of this subject for it. */
  const has = {};
  for (const pg of PYQ_PAGES) has[pg.key] = cands.some(x => x.src.key === pg.key);
  const examOn = utc => {
    const alt = PYQ_PAGES[Math.floor(utc / 86400000) % PYQ_PAGES.length];
    return has[alt.key] ? alt.key : (PYQ_PAGES.find(pg => has[pg.key]) || alt).key;
  };
  const key = examOn(day.utc);
  cands = cands.filter(x => x.src.key === key);
  /* a fixed shuffle of the candidates, then one step forward each day this subject and exam come up */
  cands = shuffled(cands.slice().sort((a, b) => (a.id < b.id ? -1 : 1)), seeded(`pyq|${subject}|${key}`));
  const start = Date.parse(PYQ_START + 'T00:00:00Z');
  let turn = 0;
  for (let t = start; t < day.utc; t += 86400000) {
    if (PYQ_DAYS[new Date(t).getUTCDay()] === subject && examOn(t) === key) turn++;
  }
  const x = cands[turn % cands.length];
  return { exam: x.src.exam, subject, paper: x.paper, hub: x.src.hub, year: x.year, poll: x.poll };
}

function pyqHeader(x) {
  const qn = x.poll.qNum ? ` \u00B7 Q${x.poll.qNum}` : '';
  const label = x.paper ? paperLabel(x.exam, x.paper) : `${x.exam} ${x.year}`.trim();
  const link = x.paper
    ? `Answer the poll below \uD83D\uDC47 then take this full paper, free, with solutions:\n<a href="${esc(x.paper.url)}">Attempt ${esc(label)}</a>`
    : `Answer the poll below \uD83D\uDC47 then practise full papers, free, with solutions:\n${x.hub}`;
  return `\uD83D\uDCDA <b>PYQ of the Day</b> \u00B7 ${PYQ_LABEL[x.subject]}\n${esc(label)}${qn}\n\n${link}`;
}

/* -------------------------------------------------------------- Telegram */
async function call(method, payload) {
  if (DRY) { log(`DRY RUN ${method}:\n` + JSON.stringify(payload, null, 2)); return { ok: true }; }
  for (let attempt = 1; attempt <= 3; attempt++) {
    let res, data;
    try {
      res = await fetch(`${API}/bot${TOKEN}/${method}`, {
        method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(payload),
      });
      data = await res.json();
    } catch (e) {
      if (attempt === 3) throw new Error(`${method}: network error — ${e.message}`);
      await sleep(2000 * attempt);
      continue;
    }
    if (data && data.ok) return data;
    const wait = data && data.parameters && data.parameters.retry_after;
    if (res.status === 429 && wait && attempt < 3) { log(`rate limited, waiting ${wait}s`); await sleep((wait + 1) * 1000); continue; }
    throw new Error(`${method}: ${res.status} ${data && data.description || 'unknown error'}`);
  }
}

async function postDigest(p, html) {
  const lines = readGlance(html);
  if (lines.length < 2) throw new Error(`"Today at a glance" not found in ${p.name}`);
  const quiz = readQuiz(html);
  await call('sendMessage', {
    chat_id: CHAT, text: digestText(p, lines, quiz.length), parse_mode: 'HTML',
    link_preview_options: { is_disabled: true },
  });
  log(`digest posted for ${p.long} (${lines.length} lines)`);
}

async function postQuiz(p, html) {
  const all = readQuiz(html);
  const pick = all.filter(pollable).slice(0, QUIZ_COUNT);
  if (pick.length < 2) throw new Error(`fewer than 2 usable MCQs in ${p.name}`);
  await call('sendMessage', {
    chat_id: CHAT, text: quizHeader(p, pick.length, all.length), parse_mode: 'HTML',
    link_preview_options: { is_disabled: true },
  });
  for (let i = 0; i < pick.length; i++) {
    const x = pick[i];
    await sleep(DRY ? 0 : 1500);                       // stay well inside Telegram's rate limit
    const payload = {
      chat_id: CHAT, question: clip(`Q${i + 1}. ${x.q}`, 300), options: x.o,
      type: 'quiz', correct_option_id: x.a, is_anonymous: true, disable_notification: true,
    };
    if (x.e) payload.explanation = clip(x.e, 200);
    await call('sendPoll', payload);
  }
  log(`quiz posted for ${p.long} (${pick.length} polls)`);
}

async function postTrick() {
  const tricks = loadTricks();
  const no = trickNumber();
  const t = tricks[(no - 1) % tricks.length];
  await call('sendMessage', {
    chat_id: CHAT, text: trickText(t, no), parse_mode: 'HTML',
    link_preview_options: { is_disabled: true },
  });
  log(`trick #${no} posted: ${t.title}`);
}

async function postMock() {
  await call('sendMessage', {
    chat_id: CHAT, text: mockText(), parse_mode: 'HTML',
    link_preview_options: { is_disabled: true },
  });
  log('Sunday mock challenge posted');
}

async function postPyq() {
  const x = pickPyq();
  await call('sendMessage', {
    chat_id: CHAT, text: pyqHeader(x), parse_mode: 'HTML',
    link_preview_options: { is_disabled: true },
  });
  await sleep(DRY ? 0 : 1500);
  const payload = {
    chat_id: CHAT, question: clip(x.poll.q, 300), options: x.poll.opts,
    type: 'quiz', correct_option_id: x.poll.idx, is_anonymous: true, disable_notification: true,
  };
  if (x.poll.e) payload.explanation = x.poll.e;
  await call('sendPoll', payload);
  log(`PYQ of the Day posted: ${x.exam} ${PYQ_LABEL[x.subject]}, Q${x.poll.qNum}${x.paper ? ' of ' + x.paper.pid : ''}`);
}

/* ------------------------------------------------------------------ main */
(async () => {
  let mode = MODE;
  if (mode === 'noon') mode = todayIst().dow === 0 ? 'mock' : 'trick';
  if (!['digest', 'quiz', 'trick', 'mock', 'pyq'].includes(mode)) {
    log(`unknown mode "${MODE}" — use digest, quiz, trick, mock, noon or pyq`); process.exit(1);
  }
  if (!DRY && (!TOKEN || !CHAT)) {
    log('TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID are not set — nothing posted. Add the two repo secrets to switch this on.');
    return;
  }
  if (mode === 'trick') { await postTrick(); return; }
  if (mode === 'mock')  { await postMock();  return; }
  if (mode === 'pyq')   { await postPyq();   return; }
  const p = pickPage();
  const asked = !!String(process.env.TG_FILE || '').trim();
  if (mode === 'quiz' && !asked && !MANUAL) {
    const age = ageInDays(p);
    if (age > 1) { log(`newest page is ${p.long}, ${age} days old — no quiz today (yesterday's page was not built).`); return; }
  }
  const html = fs.readFileSync(path.join(ARCHIVE, p.name), 'utf8');
  if (mode === 'digest') await postDigest(p, html);
  else await postQuiz(p, html);
})().catch(e => { console.error('[telegram] FAILED:', e.message); process.exit(1); });
