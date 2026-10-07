// ═══════════════════════════════════════════════════════════════════════════
//  fetch-ca.js — TrickySSC daily current affairs bot (PIB only + Gemini Flash)
//
//  1. Reads today's English press releases from PIB (RSS, with allRel.aspx as
//     a fallback).
//  2. Gemini call #1 — picks the SSC-worthy releases from the titles
//     (schemes, cabinet, appointments, awards, sci-tech, defence, economy,
//     international relations, environment, sports/culture/important days).
//  3. Opens only those releases on pib.gov.in and reads their full text.
//  4. Gemini call #2 — writes the page content as JSON (topics, glance lines,
//     important-facts slips, 10 MCQs, FAQs, meta).
//  5. Renders ca-archive/DD-MM-YYYY.html from ca-bot/page-template.html and
//     updates current-affairs.html (list, latest card, ItemList JSON-LD),
//     ca-archive/index.json and sitemap.xml.
//
//  Never overwrites an existing day page (your hand-written pages are safe)
//  unless FORCE=true. Only 2 Gemini requests per run — fits the free tier.
//
//  Env: GEMINI_API_KEY (required) · GEMINI_MODEL (optional, pins a model)
//       CA_DATE=DD-MM-YYYY (optional, default = today in IST) · FORCE=true
//  Node 20+, no npm packages.
// ═══════════════════════════════════════════════════════════════════════════
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const ARCHIVE = path.join(ROOT, 'ca-archive');
const TEMPLATE = path.join(ROOT, 'ca-bot', 'page-template.html');
const HUB = path.join(ROOT, 'current-affairs.html');
const SITEMAP = path.join(ROOT, 'sitemap.xml');
const SITE = 'https://trickyssc.com';

const KEY = process.env.GEMINI_API_KEY;
const FORCE = String(process.env.FORCE || '').toLowerCase() === 'true';
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36';

const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
const DAYS = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
const WORDS = ['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten'];

// SSC bucket → [tone CSS var, tag label]
const BUCKETS = {
  'Schemes':                ['--c-scheme', 'Government Schemes'],
  'Cabinet Decisions':      ['--c-scheme', 'Cabinet Decisions'],
  'Appointments':           ['--c-appt',   'Appointments'],
  'Awards':                 ['--c-award',  'Awards & Honours'],
  'Science & Technology':   ['--c-tech',   'Science & Technology'],
  'Defence':                ['--c-def',    'Defence'],
  'Economy':                ['--c-eco',    'Economy & Banking'],
  'International Relations':['--c-ir',     'International Relations'],
  'Environment':            ['--c-env',    'Environment & Ecology'],
  'Sports & Culture':       ['--c-sport',  'Sports, Culture & Days'],
};

const log = (...a) => console.log('[ca-bot]', ...a);
const die = (msg) => { console.error('[ca-bot] ERROR:', msg); process.exit(1); };
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

// ─────────────────────────── date ───────────────────────────
function targetDate() {
  const env = (process.env.CA_DATE || '').trim();
  if (env) {
    const m = env.match(/^(\d{2})-(\d{2})-(\d{4})$/);
    if (!m) die('CA_DATE must be DD-MM-YYYY, got ' + env);
    return { d: +m[1], m: +m[2], y: +m[3] };
  }
  const ist = new Date(Date.now() + 5.5 * 3600 * 1000); // shift to IST, read UTC fields
  return { d: ist.getUTCDate(), m: ist.getUTCMonth() + 1, y: ist.getUTCFullYear() };
}
const pad = (n) => String(n).padStart(2, '0');

// ─────────────────────────── http ───────────────────────────
async function get(url, tries = 3) {
  let last;
  for (let i = 0; i < tries; i++) {
    try {
      const ctl = new AbortController();
      const t = setTimeout(() => ctl.abort(), 25000);
      const r = await fetch(url, { headers: { 'User-Agent': UA, 'Accept': 'text/html,application/xml,*/*' }, signal: ctl.signal });
      clearTimeout(t);
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return await r.text();
    } catch (e) { last = e; await sleep(1500 * (i + 1)); }
  }
  throw new Error(url + ' → ' + (last && last.message));
}

function decode(s) {
  return String(s || '')
    .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1')
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n))
    .replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16)))
    .replace(/&nbsp;/g, ' ').replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'")
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&')
    .replace(/\s+/g, ' ').trim();
}
function stripTags(html) {
  return decode(String(html)
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<(br|\/p|\/li|\/tr|\/h\d|\/div)[^>]*>/gi, '\n')
    .replace(/<[^>]+>/g, ' '));
}

// ─────────────────────────── PIB ───────────────────────────
const RSS_URLS = [
  'https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3',
  'https://www.pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3',
];
const PRID_RE = /PRID=(\d+)/i;

function sameDay(dateObj, T) {
  if (!dateObj || isNaN(dateObj)) return null; // unknown
  const ist = new Date(dateObj.getTime() + 5.5 * 3600 * 1000);
  return ist.getUTCDate() === T.d && ist.getUTCMonth() + 1 === T.m && ist.getUTCFullYear() === T.y;
}

async function pibFromRss(T) {
  for (const u of RSS_URLS) {
    try {
      const xml = await get(u);
      const items = [...xml.matchAll(/<item>([\s\S]*?)<\/item>/gi)].map(m => {
        const it = m[1];
        const pick = (tag) => { const x = it.match(new RegExp('<' + tag + '[^>]*>([\\s\\S]*?)</' + tag + '>', 'i')); return x ? decode(x[1]) : ''; };
        const link = pick('link');
        const pr = link.match(PRID_RE);
        return { prid: pr ? pr[1] : '', title: pick('title'), link, when: pick('pubDate') ? new Date(pick('pubDate')) : null };
      }).filter(x => x.prid && x.title);
      log(`RSS ${u} → ${items.length} items`);
      if (!items.length) continue;
      const dated = items.filter(x => sameDay(x.when, T) !== false); // keep same-day or undated
      return dated;
    } catch (e) { log('RSS failed:', e.message); }
  }
  return [];
}

async function pibFromAllRel() {
  for (const u of ['https://pib.gov.in/allRel.aspx', 'https://www.pib.gov.in/allRel.aspx']) {
    try {
      const html = await get(u);
      const out = [];
      const seen = new Set();
      for (const m of html.matchAll(/<a[^>]+href=["']([^"']*PRID=(\d+)[^"']*)["'][^>]*>([\s\S]*?)<\/a>/gi)) {
        const title = stripTags(m[3]);
        if (!title || title.length < 12 || seen.has(m[2])) continue;
        seen.add(m[2]);
        out.push({ prid: m[2], title, link: 'https://pib.gov.in/PressReleasePage.aspx?PRID=' + m[2], when: null });
      }
      log(`allRel ${u} → ${out.length} items`);
      if (out.length) return out;
    } catch (e) { log('allRel failed:', e.message); }
  }
  return [];
}

// obvious non-exam noise — Gemini filters the rest
const NOISE = /\b(condolence|condoles|tender|recruitment|walk-in|english rendering|text of (the )?(pm|prime minister|president|vice)|curtain raiser|media accreditation|photo feature|press conference schedule|weekly roundup)\b/i;

const MON3 = { JAN:1,FEB:2,MAR:3,APR:4,MAY:5,JUN:6,JUL:7,AUG:8,SEP:9,OCT:10,NOV:11,DEC:12 };

async function readRelease(prid) {
  if (AIR_ITEMS.has(String(prid))) return airRead(String(prid));
  const urls = [
    'https://pib.gov.in/PressReleaseIframePage.aspx?PRID=' + prid,
    'https://pib.gov.in/PressReleasePage.aspx?PRID=' + prid,
  ];
  for (const u of urls) {
    try {
      const html = await get(u, 2);
      let text = stripTags(html);
      // posted-on date + ministry, if visible
      const po = text.match(/Posted On:?\s*(\d{1,2})\s+([A-Za-z]{3})[a-z]*\s+(\d{4})/i);
      const posted = po ? { d: +po[1], m: MON3[po[2].toUpperCase()], y: +po[3] } : null;
      const mi = html.match(/<div[^>]*class=["'][^"']*MinistryNameSubhead[^"']*["'][^>]*>([\s\S]*?)<\/div>/i);
      const ministry = mi ? stripTags(mi[1]) : '';
      // trim site chrome: start near "Posted On" if present
      const k = text.search(/Posted On/i);
      if (k > 0) text = text.slice(Math.max(0, k - 400));
      text = text.replace(/\n\s*\n+/g, '\n').slice(0, 7000);
      if (text.length > 300) return { text, posted, ministry, url: 'https://pib.gov.in/PressReleasePage.aspx?PRID=' + prid };
    } catch (e) { /* try next */ }
  }
  return null;
}

async function pool(items, n, fn) {
  const out = new Array(items.length); let i = 0;
  await Promise.all(Array.from({ length: n }, async () => {
    while (i < items.length) { const k = i++; out[k] = await fn(items[k], k); }
  }));
  return out;
}

// ─────────────────── News On AIR (All India Radio) — second source ───────────────────
// TSSC-CA-AIR-V1 (2026-10-06). Adds International / Business / Sports items that PIB does not carry.
// Fail-safe: any problem here is logged and the run simply continues with PIB only.
// Switch off with repo variable CA_NEWSONAIR=off. NOTE: News On AIR's copyright page restricts
// reproduction without written permission, so the writer prompt below tells the model to use these
// items only as a source of FACTS, never to copy sentences, and every topic links back to the source.
const AIR_ENABLED = String(process.env.CA_NEWSONAIR || '').trim().toLowerCase() !== 'off';
const AIR_BASE = 'https://newsonair.gov.in';
const AIR_CATEGORIES = ['national', 'international', 'business', 'sports', ''];   // '' = the site's main feed (latest stories)
const AIR_ITEMS = new Map();          // numeric id -> { title, link, when, text }
let AIR_USED = false;                 // set once an AIR item is part of the final corpus
let PIB_USED = false;
function sourcesPhrase() {
  const p = [];
  if (AIR_USED) p.push('All India Radio (News On AIR) reports');
  if (PIB_USED) p.push('official Press Information Bureau (PIB) releases');
  return p.join(' and ') || 'official sources';
}

function airId(link) {                // numeric-only id (the pipeline strips non-digits), starts with 99 so it never clashes with a PRID
  let h = 5381;
  for (const ch of String(link)) h = ((h * 33) ^ ch.charCodeAt(0)) >>> 0;
  return '99' + String(h).padStart(10, '0');
}
function airDayOk(when, T) {          // same IST day, or yesterday evening (after 6 pm IST)
  if (!when || isNaN(when)) return false;
  const ist = new Date(when.getTime() + 5.5 * 3600 * 1000);
  const d = ist.getUTCDate(), m = ist.getUTCMonth() + 1, y = ist.getUTCFullYear();
  if (d === T.d && m === T.m && y === T.y) return true;
  const prev = new Date(Date.UTC(T.y, T.m - 1, T.d - 1));
  return d === prev.getUTCDate() && m === prev.getUTCMonth() + 1 && y === prev.getUTCFullYear() && ist.getUTCHours() >= 18;
}
function airArticleText(html) {       // the story body sits between the date line and "Most Read"
  let t = stripTags(html);
  const end = t.search(/Most Read/i);
  if (end > 0) t = t.slice(0, end);
  const dm = t.match(/(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\s+\d{1,2}:\d{2}\s*[AP]M/);
  if (dm) t = t.slice(t.indexOf(dm[0]) + dm[0].length);
  t = t.replace(/Share\s+\S*/g, ' ').replace(/\n\s*\n+/g, '\n').trim();
  return t.slice(0, 3500);
}
function airParseWhen(html) {
  const dm = stripTags(html).match(/(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})\s+(\d{1,2}):(\d{2})\s*([AP])M/);
  if (!dm) return null;
  const mon = ['January','February','March','April','May','June','July','August','September','October','November','December'].indexOf(dm[1]);
  let hh = +dm[4] % 12; if (dm[6] === 'P') hh += 12;
  return new Date(Date.UTC(+dm[3], mon, +dm[2], hh, +dm[5]) - 5.5 * 3600 * 1000);   // site shows IST
}
async function airFromFeed(cat, T) {
  const xml = await get(cat ? `${AIR_BASE}/category/${cat}/feed/` : `${AIR_BASE}/feed/`, 1);
  const items = [...xml.matchAll(/<item>([\s\S]*?)<\/item>/gi)].map(m => {
    const it = m[1];
    const pick = (tag) => { const x = it.match(new RegExp('<' + tag + '[^>]*>([\\s\\S]*?)</' + tag + '>', 'i')); return x ? x[1] : ''; };
    const link = decode(pick('link'));
    const when = pick('pubDate') ? new Date(decode(pick('pubDate'))) : null;
    const body = pick('content:encoded') || pick('description');
    return { title: decode(pick('title')), link, when, text: stripTags(body).slice(0, 3500) };
  }).filter(x => x.title && /^https?:\/\/(www\.)?newsonair\.gov\.in\//.test(x.link));
  return items.filter(x => airDayOk(x.when, T));
}
async function airFromCategoryPage(cat, T) {          // fallback if the feed is unavailable
  const html = await get(cat ? `${AIR_BASE}/category/${cat}/` : `${AIR_BASE}/`, 1);
  const seen = new Set(), links = [];
  for (const m of html.matchAll(/href=["'](https:\/\/(?:www\.)?newsonair\.gov\.in\/([a-z0-9][a-z0-9-]{25,})\/)["']/gi)) {
    if (/^(category|wp-|hi|author|tag|page)/i.test(m[2]) || seen.has(m[1])) continue;
    seen.add(m[1]); links.push(m[1]);
  }
  const out = [];
  await pool(links.slice(0, 12), 4, async (link) => {
    try {
      const h = await get(link, 2);
      const when = airParseWhen(h);
      if (!airDayOk(when, T)) return;
      const tm = h.match(/<title>([\s\S]*?)<\/title>/i);
      const title = decode(tm ? tm[1] : '').replace(/\s*\|\s*Akashvani News.*$/i, '');
      const text = airArticleText(h);
      if (title && text.length > 150) out.push({ title, link, when, text });
    } catch (e) { /* skip this article */ }
  });
  return out;
}
async function airCandidates(T) {
  if (!AIR_ENABLED) { log('News On AIR: switched off (CA_NEWSONAIR=off)'); return []; }
  const all = [];
  for (const cat of AIR_CATEGORIES) {
    let items = [];
    const nm = cat || 'main';
    try { items = await airFromFeed(cat, T); log(`News On AIR ${nm} feed → ${items.length} items for the day`); }
    catch (e) {
      log(`News On AIR ${nm} feed unavailable (${e.message.slice(0, 80)}) — trying the page`);
      try { items = await airFromCategoryPage(cat, T); log(`News On AIR ${nm} page → ${items.length} items for the day`); }
      catch (e2) { log(`News On AIR ${nm} unavailable: ${e2.message.slice(0, 100)}`); }
    }
    for (const x of items.slice(0, 12)) {
      const id = airId(x.link);
      if (AIR_ITEMS.has(id)) continue;
      AIR_ITEMS.set(id, x);
      all.push({ prid: id, title: '[AIR] ' + x.title, link: x.link, when: x.when });
    }
  }
  return all;
}
async function airRead(id) {
  const x = AIR_ITEMS.get(id);
  if (!x) return null;
  let text = x.text;
  if (!text || text.length < 200) {
    try { text = airArticleText(await get(x.link, 2)); } catch (e) { return null; }
  }
  if (!text || text.length < 150) return null;
  return { text, posted: null, ministry: 'News On AIR (All India Radio)', url: x.link };
}

// ─────────────────── Web research (Gemini + Google Search) ───────────────────
// TSSC-CA-RESEARCH-V1 (2026-10-06). After the headlines are picked and their official text is read, each
// one is researched on the web for extra detail (background, numbers, previous editions...). The research
// call is plain text (tools on, JSON off) so it cannot clash with the JSON writer call. If the key does not
// allow search, the run logs it once and carries on with the official text only.
// Switch off with repo variable CA_WEB_SEARCH=off. Needs GEMINI_API_KEY (also when OpenAI writes the page).
const WEB_RESEARCH = String(process.env.CA_WEB_SEARCH || '').trim().toLowerCase() !== 'off';
let WEB_RESEARCH_DEAD = false;
let WEB_RESEARCH_FAILS = 0;
const WEB_TITLES = new Map();         // url -> short site name for the "Source:" line

async function webResearch(headline, official, dateLong) {
  if (!WEB_RESEARCH || WEB_RESEARCH_DEAD || !KEY) return null;
  const models = (await modelChain()).slice(0, 2);
  const prompt = `You are a research assistant for an editor of SSC (Staff Selection Commission) exam-preparation current affairs. Date: ${dateLong}.
Headline: ${headline}
What the official source already says (may be partial):
${String(official).slice(0, 1500)}

Use Google Search to find reliable, up-to-date information about this news. Prefer government and official sources (PIB, ministries, RBI, ISRO, the UN, sports federations) and reputable news agencies. Ignore exam-preparation and coaching websites.
Write a FACT SHEET of 12 to 20 short bullet facts for a General Awareness candidate: what happened, who / where / when, key numbers, the organisation or ministry involved, the purpose, background, previous editions / winners / records, and related static facts (headquarters, founding year, full forms).
RULES: facts only, no opinions. State each fact in your own words — do not copy sentences. Leave out anything you could not confirm. If sources disagree, say so. Never invent. Start directly with the bullets.`;
  for (const model of models) {
    for (let attempt = 0; attempt < 2; attempt++) {
      try {
        const r = await fetch(`${API}/models/${model}:generateContent`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'x-goog-api-key': KEY },
          body: JSON.stringify({ contents: [{ role: 'user', parts: [{ text: prompt }] }], tools: [{ google_search: {} }], generationConfig: { temperature: 0.2, maxOutputTokens: 4096 } }),
        });
        const body = await r.text();
        if (r.status === 400 || r.status === 401 || r.status === 403) {
          log(`Web search is not available on this key (${model}: HTTP ${r.status} ${body.slice(0, 120).replace(/\s+/g, ' ')}) — continuing without it`);
          WEB_RESEARCH_DEAD = true; return null;
        }
        if (r.status === 404) break;                    // try the next model
        if (!r.ok) { log(`Web research ${model}: HTTP ${r.status}`); await sleep(4000 * (attempt + 1)); continue; }
        const j = JSON.parse(body);
        const cand = (j.candidates || [])[0] || {};
        const text = ((cand.content && cand.content.parts) || []).filter(p => !p.thought && p.text).map(p => p.text).join('').trim();
        const chunks = ((cand.groundingMetadata && cand.groundingMetadata.groundingChunks) || []).map(c => c.web).filter(w => w && w.uri);
        if (text.length < 200) { log(`Web research ${model}: empty reply (${cand.finishReason || 'no text'})`); break; }
        const seen = new Set(), sources = [];
        for (const w of chunks) { if (seen.has(w.uri)) continue; seen.add(w.uri); sources.push({ uri: w.uri, title: String(w.title || '').replace(/^www\./, '') }); }
        sources.slice(0, 2).forEach(w => WEB_TITLES.set(w.uri, w.title || 'web source'));
        WEB_RESEARCH_FAILS = 0;
        return { notes: text.slice(0, 6000), sources: sources.slice(0, 2).map(w => w.uri) };
      } catch (e) { log(`Web research ${model}: ${e.message.slice(0, 100)}`); await sleep(2000); }
    }
  }
  if (++WEB_RESEARCH_FAILS >= 3) { WEB_RESEARCH_DEAD = true; log('Web research failed for 3 headlines in a row — skipping it for the rest of this run'); }
  return null;
}

// ─────────────────────────── Gemini ───────────────────────────
const API = 'https://generativelanguage.googleapis.com/v1beta';
let MODEL_CHAIN = null;

function versionScore(name) {
  const m = name.match(/gemini-(\d+(?:\.\d+)?)/);
  return m ? parseFloat(m[1]) : 0;
}
async function modelChain() {
  if (MODEL_CHAIN) return MODEL_CHAIN;
  const chain = [];
  if (process.env.GEMINI_MODEL) chain.push(process.env.GEMINI_MODEL.replace(/^models\//, ''));
  try {
    const r = await fetch(API + '/models?pageSize=1000', { headers: { 'x-goog-api-key': KEY } });
    const j = await r.json();
    const found = (j.models || [])
      .filter(m => (m.supportedGenerationMethods || []).includes('generateContent'))
      .map(m => m.name.replace(/^models\//, ''))
      .filter(n => /flash/i.test(n) && !/lite|image|tts|audio|live|embed|8b|exp|thinking|native|robotics|computer/i.test(n));
    found.sort((a, b) => {
      const pa = /preview/.test(a) ? 1 : 0, pb = /preview/.test(b) ? 1 : 0;
      return (versionScore(b) - versionScore(a)) || (pa - pb) || a.length - b.length;
    });
    log('Flash models on this key:', found.slice(0, 6).join(', ') || '(none listed)');
    chain.push(...found.slice(0, 4));
  } catch (e) { log('ListModels failed:', e.message); }
  chain.push('gemini-flash-latest', 'gemini-2.5-flash');
  MODEL_CHAIN = [...new Set(chain)];
  return MODEL_CHAIN;
}

function parseJson(text) {
  let t = String(text || '').trim().replace(/^```(?:json)?\s*/i, '').replace(/```\s*$/, '').trim();
  try { return JSON.parse(t); } catch (e) {
    const a = t.indexOf('{'), b = t.lastIndexOf('}');
    if (a >= 0 && b > a) return JSON.parse(t.slice(a, b + 1));
    throw e;
  }
}

async function geminiTry(system, user, maxTokens) {
  if (!KEY) return null;
  const models = await modelChain();
  let lastErr = '';
  // TSSC-CA-RETRY-V1 (2026-10-06): HTTP 503 ("model overloaded") is temporary and common on the
  // free tier. The old loop tried every model twice within ~40 s and gave up. Now, if a whole pass
  // failed ONLY for temporary reasons (503/500/429/empty reply), wait and run another pass.
  const ROUNDS = 4;
  for (let round = 0; round < ROUNDS; round++) {
    let transient = false;
    for (const model of models) {
      for (let attempt = 0; attempt < 2; attempt++) {
        try {
          const r = await fetch(`${API}/models/${model}:generateContent`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'x-goog-api-key': KEY },
            body: JSON.stringify({
              systemInstruction: { parts: [{ text: system }] },
              contents: [{ role: 'user', parts: [{ text: user }] }],
              generationConfig: { temperature: 0.3, maxOutputTokens: maxTokens, responseMimeType: 'application/json' },
            }),
          });
          const body = await r.text();
          if (r.status === 429) {
            const w = body.match(/"retryDelay":\s*"(\d+)/);
            const secs = w ? Math.min(+w[1] + 2, 70) : 40;
            lastErr = `${model}: 429 rate limit`;
            transient = true;
            log(`${lastErr} — waiting ${secs}s`);
            if (attempt === 0) { await sleep(secs * 1000); continue; }
            break;
          }
          if (r.status === 404 || r.status === 400 || r.status === 403) { lastErr = `${model}: HTTP ${r.status} ${body.slice(0, 200)}`; log(lastErr); break; }
          if (!r.ok) { lastErr = `${model}: HTTP ${r.status}`; transient = true; log(lastErr); await sleep(5000); continue; }
          const j = JSON.parse(body);
          const cand = (j.candidates || [])[0];
          const text = cand && cand.content && (cand.content.parts || []).filter(p => !p.thought && p.text).map(p => p.text).join('');
          if (!text) { lastErr = `${model}: empty reply (${cand && cand.finishReason})`; transient = true; log(lastErr); continue; }
          const data = parseJson(text);
          log(`Gemini OK — ${model}`);
          return data;
        } catch (e) { lastErr = `${model}: ${e.message}`; transient = true; log(lastErr); }
      }
    }
    if (!transient || round === ROUNDS - 1) break;
    const wait = 30 * (round + 1);
    log(`All models busy (temporary errors) — waiting ${wait}s, then trying again (pass ${round + 2}/${ROUNDS})`);
    await sleep(wait * 1000);
  }
  log('All Gemini models failed. Last error: ' + lastErr);
  return null;
}

// ───────────────── OpenAI (optional second provider) ─────────────────
// TSSC-CA-OPENAI-V1 (2026-10-06). Used when OPENAI_API_KEY is set. Gemini stays first unless
// CA_PROVIDER=openai. Repo variable OPENAI_MODEL picks the model (default below).
const OPENAI_KEY = process.env.OPENAI_API_KEY;
const OPENAI_MODEL = (process.env.OPENAI_MODEL || 'gpt-5-mini').trim();

async function openaiTry(system, user, maxTokens) {
  if (!OPENAI_KEY) return null;
  let tokenParam = 'max_completion_tokens';
  let lastErr = '';
  for (let attempt = 0; attempt < 4; attempt++) {
    try {
      const body = {
        model: OPENAI_MODEL,
        messages: [{ role: 'system', content: system }, { role: 'user', content: user }],
        response_format: { type: 'json_object' },
      };
      // reasoning models spend part of this budget on thinking, so give it room
      body[tokenParam] = Math.min(Math.max(maxTokens * 2, 8192), 32768);
      const r = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + OPENAI_KEY },
        body: JSON.stringify(body),
      });
      const text = await r.text();
      if (r.status === 400 && tokenParam === 'max_completion_tokens' && /max_completion_tokens/.test(text)) {
        tokenParam = 'max_tokens'; log('OpenAI: switching to max_tokens'); continue;
      }
      if (r.status === 401 || r.status === 403 || r.status === 404 || r.status === 400) {
        lastErr = `${OPENAI_MODEL}: HTTP ${r.status} ${text.slice(0, 220)}`; log('OpenAI ' + lastErr); return null;
      }
      if (r.status === 402 || (r.status === 429 && /insufficient_quota|billing/i.test(text))) {
        lastErr = `${OPENAI_MODEL}: HTTP ${r.status} (no credit / quota — top up the OpenAI balance)`; log('OpenAI ' + lastErr); return null;
      }
      if (!r.ok) { lastErr = `${OPENAI_MODEL}: HTTP ${r.status}`; log('OpenAI ' + lastErr); await sleep(15000 * (attempt + 1)); continue; }
      const j = JSON.parse(text);
      const choice = (j.choices || [])[0];
      const content = choice && choice.message && choice.message.content;
      if (!content) { lastErr = `${OPENAI_MODEL}: empty reply (${choice && choice.finish_reason})`; log('OpenAI ' + lastErr); continue; }
      const data = parseJson(content);
      log(`OpenAI OK — ${OPENAI_MODEL}`);
      return data;
    } catch (e) { lastErr = `${OPENAI_MODEL}: ${e.message}`; log('OpenAI ' + lastErr); await sleep(5000); }
  }
  log('OpenAI failed. Last error: ' + lastErr);
  return null;
}

// Every caller still uses gemini(); it now walks the providers in order.
let OPENAI_TAKEOVER = false;   // set once Gemini has failed a whole call and OpenAI answered: skip Gemini's long waits for the rest of the run
async function gemini(system, user, maxTokens) {
  const preferOpenAI = OPENAI_TAKEOVER || String(process.env.CA_PROVIDER || '').toLowerCase() === 'openai';
  const order = preferOpenAI ? [['OpenAI', openaiTry], ['Gemini', geminiTry]] : [['Gemini', geminiTry], ['OpenAI', openaiTry]];
  const tried = [];
  for (const [name, fn] of order) {
    if (name === 'Gemini' && !KEY) continue;
    if (name === 'OpenAI' && !OPENAI_KEY) continue;
    tried.push(name);
    const data = await fn(system, user, maxTokens);
    if (data) { if (name === 'OpenAI' && tried.length > 1) OPENAI_TAKEOVER = true; return data; }
    if (tried.length < order.length && (name === 'Gemini' ? OPENAI_KEY : KEY)) log(`${name} failed — trying the other provider`);
  }
  die(`All providers failed (${tried.join(', ') || 'none configured'}) — see the lines above.`);
}

// ─────────────────────────── prompts ───────────────────────────
const BUCKET_LIST = Object.keys(BUCKETS).join(', ');

const SELECT_SYS = `You are the current-affairs editor for TrickySSC, an SSC CGL/CHSL/MTS exam prep site. Readers are exam candidates with little time: a page full of minor news wastes their day.
From a list of All India Radio (News On AIR) item titles (tagged [AIR]) and Press Information Bureau (PIB) release titles, pick ONLY the releases an SSC General Awareness paper could realistically ask about. News On AIR is the primary source of headlines: when an [AIR] item and a PIB release are equally important, prefer the [AIR] item. Use PIB to add what AIR does not carry — Cabinet decisions, new schemes and portals, appointments, defence and space milestones, official reports and indices.

TIER 1 — always pick: Union Cabinet decisions; new schemes, missions, portals, laws and policies (with ministry); appointments to top posts (President, CJI, Governors, Chiefs, Secretaries, heads of commissions/banks/PSUs); awards, honours and rankings with named winners; major reports and indices with a rank or headline number; space, science and defence milestones (launches, inductions, exercises with partner country and venue); international agreements, summits and hosting decisions (who hosts, where, which edition); major sports results (tournament winners, first-ever or record achievements, hosts); important days with their themes; national parks, sanctuaries, Ramsar and heritage-site declarations; big economy and banking news (RBI, GDP, trade figures, budget-linked decisions).
TIER 2 — pick only if the day is thin: bilateral visits that produced a concrete outcome; MoUs between well-known bodies with a named, askable outcome; named exhibitions, fairs and festivals.
SKIP always: curtain raisers, workshops, conferences, seminars and review meetings; minister travel, speeches, inaugurations of ordinary projects; joint-working-group and routine bilateral talks; state-level and district-level events; training, capacity-building and awareness drives; individual bronze or silver medallists and routine participation lists; statistics bulletins without a headline number; press-release follow-ups and duplicates.

HEADLINES ONLY: the page carries at most 6 topics, and every pick will then be researched in depth and written up as a full explainer. So rank strictly and pick the 4 to 6 most important headlines of the day (fewer only if the day truly has fewer). Never pad the list with Tier-2 items just to reach a number.
Reply ONLY with JSON: {"picks":[{"prid":"<id>","why":"<5 words>"}]} ordered most important first.`;

function writeSys(dateLong) {
  return `You write the daily current-affairs page for TrickySSC (SSC CGL, CHSL, MTS, CPO, GD aspirants) for ${dateLong}.
SOURCE RULE: every news fact must come from the official text supplied (a PIB release or News On AIR report) or from the RESEARCH NOTES attached to that item; if they disagree, the official text wins. Facts in the research notes are web-sourced: state them in your own words and never copy sentences.  Items from News On AIR (ministry line "News On AIR (All India Radio)") are copyrighted news text: use them ONLY as a source of facts (who, what, where, when, numbers), state each fact in your own short exam-style words, and never copy or closely paraphrase their sentences. You MAY add standard static background that is certain and exam-relevant (ministry of a scheme, headquarters, founding year, full forms, capital of a country, who a day commemorates) — never invent numbers, dates, names or outcomes. If unsure, leave it out.
STYLE: short one-line factual bullets, the way SSC asks — dates, full forms, ministries, venues, outlays, first/largest, edition numbers, themes. No opinion, no filler, no "the government said it is committed to". Indian English. Use **double asterisks** to bold the key term in each bullet (1–2 per bullet). Plain text otherwise — no HTML, no markdown links.
TARGETING: write exactly ONE topic for each supplied headline (at most 6 topics in all) — each a full, detailed explainer a candidate can revise from, not a news snippet. Do not add, merge or drop topics. Cover everything askable about the story: what happened, who / where / when, numbers, the ministry or organisation involved, the purpose, and relevant background and static facts. For sports, keep the result, winners, venue, records and edition details.
Each topic:
- "bucket": exactly one of: ${BUCKET_LIST}
- "tag2": a short secondary label (e.g. "Important Days", "Summits", "MoU", "Space")
- "id": short kebab-case slug, unique
- "emoji": one emoji
- "rail": 2–4 word label for the jump menu
- "title": exam-style headline (max ~12 words)
- "bullets": 8–12 one-line facts about the news itself — detailed and specific, no filler and no repetition
- "sections": 1–3 sub-sections (for example Background, Key Details as a table, Related facts), each {"heading": "...", "bullets": [...]} OR {"heading": "...", "table": [["Field","Value"], ...]} (tables of 4–8 key/value rows are great for schemes, summits, appointments)
- "facts": 6–8 "Important Facts for Exams" — only lines an SSC paper could ask, question-answer shaped
- "likely": the most likely exam question angle, 3–8 words
- "prids": the PRID numbers used
Also:
- "glance": one line per topic (same order), the single most askable fact
- "mcqs": 8 to 10 MCQs across all topics — ONLY questions a real SSC GA paper could ask (who / which / where / when / first / host / winner / ministry / theme / full form / rank). Fewer, better MCQs beat filler: if only 7 askable questions exist, write 7. NEVER ask: project costs or amounts down to the last digit, counts of minor measures or participants, names of committee members, speakers or minor officials, individual bronze or silver medallists, numbers of languages or districts, or any trivia that only matters inside one press release. Each MCQ: {"q":"...","o":["A","B","C","D"],"a":<0-3 index of correct>,"e":"one-line explanation"} — plausible distractors, answers spread across A–D, no "all of the above"
- "faqs": 6 FAQs {"q","a"} a searcher would type about today's topics; answers 2–3 sentences, plain text
- "metaDescription": ≤155 characters, starts "Daily Current Affairs ${dateLong} for SSC CGL, CHSL & MTS —" then 3–4 topic names, ends "with practice MCQs."
- "keywords": 8–10 lowercase search keywords
- "cardLine": one line for the archive card, like "Topic A, Topic B, Topic C and more, with practice MCQs."
- "seoTopicsSentence": one flowing sentence naming every topic, starting "The topics covered today are"
Reply ONLY with JSON: {"topics":[...],"glance":[...],"mcqs":[...],"faqs":[...],"metaDescription":"","keywords":[],"cardLine":"","seoTopicsSentence":""}`;
}

// ─────────────────────────── render helpers ───────────────────────────
const esc = (s) => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const rich = (s) => esc(String(s || '').replace(/\*\*\s*\*\*/g, '')).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/\*\*/g, '');
const plain = (s) => String(s || '').replace(/\*\*/g, '');
const slug = (s) => String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40) || 'topic';

function srcLabel(u, urls) {          // "PIB release", "News On AIR report" or the web site's name
  const off = urls.filter(x => /pib\.gov\.in|newsonair\.gov\.in/.test(x));
  const n = off.length > 1 ? ' ' + (off.indexOf(u) + 1) : '';
  if (/newsonair\.gov\.in/.test(u)) return 'News On AIR report' + n;
  if (/pib\.gov\.in/.test(u)) return 'PIB release' + n;
  return esc(WEB_TITLES.get(u) || 'web source');
}

function renderStory(t, i, T, dateLong, sourceUrls) {
  const [tone, label] = BUCKETS[t.bucket] || ['--orange', t.bucket || 'Current Affairs'];
  let s = `<!-- ---------- ${i + 1}. ${esc(plain(t.title)).toUpperCase().slice(0, 50)} ---------- -->
<article class="story reveal" id="${t.id}" style="--tone:var(${tone})">
  <div class="story-head">
    <div class="tagrow">
      <span class="tag">${esc(label)}</span>
${t.tag2 ? `      <span class="tag ghost">${esc(t.tag2)}</span>\n` : ''}      <span class="tag ghost">${esc(dateLong)}</span>
    </div>
    <h2>${esc(plain(t.title))}</h2>
  </div>
  <div class="story-body">
    <ul>
${(t.bullets || []).map(b => `      <li>${rich(b)}</li>`).join('\n')}
    </ul>
`;
  for (const sec of (t.sections || [])) {
    if (!sec || !sec.heading) continue;
    s += `\n    <h3>${esc(plain(sec.heading))}</h3>\n`;
    if (Array.isArray(sec.table) && sec.table.length) {
      s += `    <div class="scroller">\n      <table class="tbl">\n`;
      for (const row of sec.table) {
        if (!Array.isArray(row) || row.length < 2) continue;
        s += `        <tr><td>${rich(row[0])}</td><td>${rich(row.slice(1).join(' — '))}</td></tr>\n`;
      }
      s += `      </table>\n    </div>\n`;
    }
    if (Array.isArray(sec.bullets) && sec.bullets.length) {
      s += `    <ul>\n${sec.bullets.map(b => `      <li>${rich(b)}</li>`).join('\n')}\n    </ul>\n`;
    }
  }
  s += `
    <div class="slip">
      <h4><span class="omr"><i class="f"></i><i></i><i></i><i></i></span> Important Facts for Exams</h4>
      <ul>
${(t.facts || []).map(f => `        <li>${rich(f)}</li>`).join('\n')}
      </ul>
    </div>
`;
  if (sourceUrls.length) {
    s += `    <p class="src">Source: ${sourceUrls.map((u, k) => `<a href="${esc(u)}" target="_blank" rel="noopener nofollow">${srcLabel(u, sourceUrls)}</a>`).join(' · ')}</p>\n`;
  }
  s += `  </div>\n</article>\n`;
  return s;
}

function jsonLd(obj) { return '<script type="application/ld+json">\n' + JSON.stringify(obj, null, 2) + '\n</script>'; }

// ─────────────────────────── hub / index / sitemap ───────────────────────────
function listDays() {
  return fs.readdirSync(ARCHIVE)
    .map(f => { const m = f.match(/^(\d{2})-(\d{2})-(\d{4})\.html$/); return m ? { f, d: +m[1], m: +m[2], y: +m[3] } : null; })
    .filter(Boolean)
    .sort((a, b) => (b.y - a.y) || (b.m - a.m) || (b.d - a.d));
}

function updateIndexJson(days) {
  const dated = days.map(x => x.f);
  const other = fs.readdirSync(ARCHIVE).filter(f => /\.html?$/i.test(f) && f !== 'index.html' && !dated.includes(f)).sort().reverse();
  const all = dated.concat(other);
  fs.writeFileSync(path.join(ARCHIVE, 'index.json'), JSON.stringify(all, null, 2) + '\n');
}

function replaceBetween(html, start, end, inner) {
  const a = html.indexOf(start), b = html.indexOf(end);
  if (a < 0 || b < a) return null;
  return html.slice(0, a + start.length) + '\n' + inner + '\n    ' + html.slice(b);
}

function updateHub(days, latest) {
  if (!fs.existsSync(HUB)) { log('current-affairs.html not found — skipped'); return; }
  let h = fs.readFileSync(HUB, 'utf8');

  // 1. static month-grouped list
  const groups = [];
  for (const x of days) {
    const key = x.y + '-' + x.m;
    let g = groups.find(g => g.key === key);
    if (!g) { g = { key, label: MONTHS[x.m - 1] + ' ' + x.y, items: [] }; groups.push(g); }
    g.items.push(x);
  }
  const list = groups.map((g, gi) => `    <div class="month">
      <h3>${g.label} <span>${g.items.length} day${g.items.length > 1 ? 's' : ''}</span></h3>
      <div class="grid">
${g.items.map((x, i) => {
    const wd = DAYS[new Date(Date.UTC(x.y, x.m - 1, x.d)).getUTCDay()];
    return `        <a class="day${gi === 0 && i === 0 ? ' new' : ''}" href="ca-archive/${x.f}">
          <div class="dnum">${pad(x.d)}</div>
          <div class="dtxt">
            <div class="dlabel">${x.d} ${MONTHS[x.m - 1]} ${x.y}</div>
            <div class="dsub">${wd}</div>
          </div>
          <span class="arrow">➜</span>
        </a>`;
  }).join('\n')}
      </div>
    </div>`).join('\n');
  const h1 = replaceBetween(h, '<!-- CA-LIST:START -->', '<!-- CA-LIST:END -->', list);
  if (h1) h = h1; else log('CA-LIST markers missing — list not updated');

  // 2. featured latest card (only when this run created the newest day)
  const top = days[0];
  if (latest && top && top.f === latest.file) {
    const card = `  <a class="feat" id="latestCard" href="ca-archive/${latest.file}">
    <div class="cal"><div class="m" id="latM">${MONTHS[top.m - 1].slice(0, 3)}</div><div class="d" id="latD">${pad(top.d)}</div></div>
    <div class="txt">
      <div class="k">⚡ Latest current affairs</div>
      <h2 id="latH">Current Affairs — ${latest.dateLong}</h2>
      <p id="latP">${esc(latest.cardLine)}</p>
    </div>
    <span class="go">Read Today's CA →</span>
  </a>`;
    const h2 = replaceBetween(h, '<!-- CA-LATEST:START -->', '<!-- CA-LATEST:END -->', card);
    if (h2) h = h2; else log('CA-LATEST markers missing — card not updated');
  }

  // 3. ItemList JSON-LD
  const items = days.slice(0, 60).map((x, i) => `      {"@type":"ListItem","position":${i + 1},"name":"Current Affairs ${x.d} ${MONTHS[x.m - 1]} ${x.y}","url":"${SITE}/ca-archive/${x.f}"}`).join(',\n');
  h = h.replace(/"numberOfItems":\d+,\s*"itemListElement":\[[\s\S]*?\n\s*\]/, `"numberOfItems":${Math.min(days.length, 60)},\n    "itemListElement":[\n${items}\n    ]`);

  fs.writeFileSync(HUB, h);
  log('current-affairs.html updated');
}

// card text for the newest day, read from that page's own meta tags
function latestInfo(x) {
  const html = fs.readFileSync(path.join(ARCHIVE, x.f), 'utf8');
  const og = html.match(/<meta property="og:description" content="([^"]*)"/i) || html.match(/<meta name="description" content="([^"]*)"/i);
  let line = og ? decode(og[1]) : '';
  line = line.replace(/^Daily Current Affairs[^—]*—\s*/i, '');
  return { file: x.f, dateLong: `${x.d} ${MONTHS[x.m - 1]} ${x.y}`, cardLine: line || 'Exam-ready topics with practice MCQs.' };
}

function refreshArchive(iso, file) {
  const days = listDays();
  updateIndexJson(days);
  if (days.length) updateHub(days, latestInfo(days[0]));
  for (const x of days) updateSitemap(x.f, `${x.y}-${pad(x.m)}-${pad(x.d)}`, x.f === file ? iso : null);
}

function updateSitemap(file, iso, bumpHub) {
  if (!fs.existsSync(SITEMAP)) return;
  let s = fs.readFileSync(SITEMAP, 'utf8');
  if (bumpHub) s = s.replace(/(<loc>https:\/\/trickyssc\.com\/current-affairs\.html<\/loc>\s*<lastmod>)[^<]*(<\/lastmod>)/, `$1${bumpHub}$2`);
  const loc = `${SITE}/ca-archive/${file}`;
  if (!s.includes(`<loc>${loc}</loc>`)) {
    const entry = `  <url>\n    <loc>${loc}</loc>\n    <lastmod>${iso}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n`;
    // insert right after the current-affairs.html entry so all CA urls stay together
    const m = s.match(/  <url>\s*<loc>https:\/\/trickyssc\.com\/current-affairs\.html<\/loc>[\s\S]*?<\/url>\n/);
    s = m ? s.replace(m[0], m[0] + entry) : s.replace('</urlset>', entry + '</urlset>');
  }
  fs.writeFileSync(SITEMAP, s);
}

// TSSC-CA-NODUP-V1: headlines already published on the previous two days' pages (read from their "rail" links)
function recentCovered(T) {
  const out = [];
  for (let k = 1; k <= 2; k++) {
    const dt = new Date(Date.UTC(T.y, T.m - 1, T.d - k));
    const f = path.join(ARCHIVE, `${pad(dt.getUTCDate())}-${pad(dt.getUTCMonth() + 1)}-${dt.getUTCFullYear()}.html`);
    if (!fs.existsSync(f)) continue;
    const h = fs.readFileSync(f, 'utf8');
    const rail = (h.match(/<a href="#[^"]+">[^<]{6,140}<\/a>/g) || []).slice(0, 8)
      .map(x => x.replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').trim());
    rail.forEach(t => out.push(t));
  }
  return [...new Set(out)];
}

// ─────────────────────────── main ───────────────────────────
(async () => {
  if (!KEY && !OPENAI_KEY) die('Neither GEMINI_API_KEY nor OPENAI_API_KEY secret is set');
  const T = targetDate();
  const file = `${pad(T.d)}-${pad(T.m)}-${T.y}.html`;
  const iso = `${T.y}-${pad(T.m)}-${pad(T.d)}`;
  const dateLong = `${T.d} ${MONTHS[T.m - 1]} ${T.y}`;
  const weekday = DAYS[new Date(Date.UTC(T.y, T.m - 1, T.d)).getUTCDay()];
  const outPath = path.join(ARCHIVE, file);
  log('Target date:', dateLong, '→', 'ca-archive/' + file);

  if (!fs.existsSync(ARCHIVE)) fs.mkdirSync(ARCHIVE);
  if (fs.existsSync(outPath) && !FORCE) {
    log('Page already exists — not rewriting it (set FORCE=true to rebuild). Refreshing the archive list only.');
    refreshArchive(iso, file);
    return;
  }
  if (!fs.existsSync(TEMPLATE)) die('ca-bot/page-template.html is missing');

  // 1. PIB list
  let rel = await pibFromRss(T);
  if (rel.length < 5) {
    const extra = await pibFromAllRel();
    const seen = new Set(rel.map(r => r.prid));
    rel = rel.concat(extra.filter(r => !seen.has(r.prid)));
  }
  rel = rel.filter(r => !NOISE.test(r.title));
  let airRel = [];
  try { airRel = (await airCandidates(T)).filter(r => !NOISE.test(r.title)); } catch (e) { log('News On AIR skipped:', e.message); }
  if (!rel.length && !airRel.length) die('No PIB releases found for today (PIB unreachable from the runner, or nothing published yet).');
  if (!rel.length) log('PIB returned nothing — continuing with News On AIR items only');
  rel = airRel.concat(rel);                      // News On AIR first: it is the primary source for headlines
  log(`${rel.length} candidate releases (${airRel.length} from News On AIR)`);

  // 2. pick
  const titles = rel.slice(0, 260).map(r => `${r.prid} | ${r.title}`).join('\n');
  const covered = recentCovered(T);
  if (covered.length) log('Already covered on the previous two days:', covered.join(' | '));
  const coveredTxt = covered.length ? `\n\nALREADY PUBLISHED on the previous two days' pages (do NOT pick these again, or any item that is only a follow-up of them; pick a repeat only if there is a genuinely NEW major development today):\n- ${covered.join('\n- ')}` : '';
  const sel = await gemini(SELECT_SYS, `Date: ${dateLong}${coveredTxt}\nAll India Radio items first ([AIR] = News On AIR), then PIB releases (id | title):\n${titles}`, 4096);
  const byId = new Map(rel.map(r => [r.prid, r]));
  let picks = (sel.picks || []).map(p => String(p.prid).replace(/\D/g, '')).filter(id => byId.has(id));
  picks = [...new Set(picks)];
  // TSSC-CA-AIRCAP-V1: keep PIB (the official source) as the backbone — at most CA_AIR_MAX News On AIR items (default: no cap, best-ranked first)
  { const v = parseInt(process.env.CA_AIR_MAX, 10); const AIR_MAX = Number.isFinite(v) ? Math.max(0, v) : 99;
    let n = 0; const before = picks.length;
    picks = picks.filter(id => !AIR_ITEMS.has(id) || ++n <= AIR_MAX);
    if (picks.length < before) log(`News On AIR items capped at ${AIR_MAX}: ${before - picks.length} dropped`); }
  { const v = parseInt(process.env.CA_MAX_TOPICS, 10); const MAXT = Number.isFinite(v) ? Math.min(8, Math.max(3, v)) : 6;
    if (picks.length > MAXT) log(`Keeping the ${MAXT} most important headlines (of ${picks.length} picked)`);
    picks = picks.slice(0, MAXT); }
  if (picks.length < 3) die('Gemini picked fewer than 3 usable releases: ' + JSON.stringify(sel).slice(0, 300));
  log('Picked PRIDs:', picks.join(', '));

  // 3. read full text
  const texts = await pool(picks, 4, async (id) => ({ id, r: await readRelease(id) }));
  const good = texts.filter(x => x.r).filter(x => {
    const p = x.r.posted;
    if (p && !(p.d === T.d && p.m === T.m && p.y === T.y)) {
      // allow the previous day too (evening releases land on the next morning's run)
      const prev = new Date(Date.UTC(T.y, T.m - 1, T.d - 1));
      const ok = p.d === prev.getUTCDate() && p.m === prev.getUTCMonth() + 1 && p.y === prev.getUTCFullYear();
      if (!ok) log(`PRID ${x.id} posted ${p.d}-${p.m}-${p.y} — dropped (old)`);
      return ok;
    }
    return true;
  });
  if (good.length < 3) die(`Only ${good.length} release texts could be read from pib.gov.in`);
  const urlOf = new Map(good.map(x => [x.id, x.r.url]));
  AIR_USED = good.some(x => AIR_ITEMS.has(String(x.id)));
  PIB_USED = good.some(x => !AIR_ITEMS.has(String(x.id)));
  if (AIR_USED) log(`News On AIR items in the final corpus: ${good.filter(x => AIR_ITEMS.has(String(x.id))).length}`);
  // 3b. research each headline on the web (extra detail); optional and fail-safe
  const research = new Map();
  if (WEB_RESEARCH && KEY) {
    log(`Researching ${good.length} headlines on the web...`);
    const res = await pool(good, 2, async (x) => ({ id: x.id, r: await webResearch(String(byId.get(x.id).title).replace(/^\[AIR\]\s*/, ''), x.r.text, dateLong) }));
    res.forEach(o => { if (o && o.r) research.set(o.id, o.r); });
    log(`Web research found notes for ${research.size} of ${good.length} headlines`);
  }
  const webOf = new Map([...research].map(([id, o]) => [id, o.sources]));
  const corpus = good.map(x => `=== PRID ${x.id} | ${byId.get(x.id).title}${x.r.ministry ? ' | ' + x.r.ministry : ''}\n${x.r.text}`
    + (research.has(x.id) ? `\n--- RESEARCH NOTES for this item (extra detail from web search; the official text above wins if they disagree) ---\n${research.get(x.id).notes}` : '')).join('\n\n');
  log(`Read ${good.length} releases (${corpus.length} chars)`);

  // 4. write
  const data = await gemini(writeSys(dateLong), `PIB releases for ${dateLong}:\n\n${corpus}`, 32768);
  let topics = (data.topics || []).filter(t => t && t.title && Array.isArray(t.bullets) && t.bullets.length);
  if (topics.length < 3) die('Gemini returned fewer than 3 topics');
  topics = topics.slice(0, 8);
  const used = new Set();
  topics.forEach(t => { let id = slug(t.id || t.title); while (used.has(id)) id += '-2'; used.add(id); t.id = id; if (!BUCKETS[t.bucket]) t.bucket = 'Schemes'; });
  const mcqs = (data.mcqs || []).filter(q => q && q.q && Array.isArray(q.o) && q.o.length === 4 && Number.isInteger(q.a) && q.a >= 0 && q.a < 4).slice(0, 10);
  const faqs = (data.faqs || []).filter(f => f && f.q && f.a).slice(0, 6);
  const glance = (data.glance || []).slice(0, topics.length);

  // 5. render
  const nFacts = topics.reduce((n, t) => n + (t.facts || []).length + (t.bullets || []).length, 0);
  const words = topics.reduce((n, t) => n + JSON.stringify(t).split(/\s+/).length, 0);
  const readMin = Math.max(4, Math.round(words / 180));
  const kw = (data.keywords || []).map(plain).join(', ');
  const meta = plain(data.metaDescription || `Daily Current Affairs ${dateLong} for SSC CGL, CHSL & MTS with practice MCQs.`);
  const cardLine = plain(data.cardLine || topics.slice(0, 3).map(t => plain(t.title)).join(', ') + ' and more.');
  const canon = `${SITE}/ca-archive/${file}`;

  const headMeta = `<title>Current Affairs ${dateLong} for SSC CGL | TrickySSC</title>
<meta name="description" content="${esc(meta)}">
<meta name="keywords" content="${esc('current affairs ' + dateLong.toLowerCase() + ', daily current affairs, ssc cgl current affairs' + (kw ? ', ' + kw : ''))}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="TrickySSC">
<link rel="canonical" href="${canon}">
<link rel="icon" href="${SITE}/favicon.png">

<meta property="og:type" content="article">
<meta property="og:site_name" content="Tricky SSC">
<meta property="og:title" content="Daily Current Affairs ${dateLong} — SSC CGL, CHSL, MTS">
<meta property="og:description" content="${esc(cardLine)}">
<meta property="og:url" content="${canon}">
<meta property="og:image" content="${SITE}/favicon.png">
<meta property="article:published_time" content="${iso}T20:00:00+05:30">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Current Affairs ${dateLong} for SSC CGL &amp; CHSL">
<meta name="twitter:description" content="${topics.length} exam-ready topics + ${mcqs.length} practice MCQs from the news of ${dateLong}.">`;

  const rail = topics.map(t => `      <a href="#${t.id}">${esc(t.emoji || '📌')} ${esc(plain(t.rail || t.title))}</a>`).join('\n')
    + (mcqs.length ? `\n      <a href="#quiz">📝 Practice MCQs</a>` : '');
  const glanceHtml = glance.map(g => `      <li><b></b><span>${rich(g)}</span></li>`).join('\n');
  const stories = topics.map((t, i) => renderStory(t, i, T, dateLong,
    (t.prids || []).flatMap(p => { const id = String(p).replace(/\D/g, ''); return [urlOf.get(id), ...(webOf.get(id) || [])]; }).filter(Boolean).filter((u, k, a) => a.indexOf(u) === k))).join('\n');

  const seoIntro = `<h2>Daily Current Affairs ${dateLong} for SSC CGL, CHSL, MTS and CPO</h2>
    <p>This page carries the complete <strong>current affairs of ${dateLong}</strong>, prepared specifically for candidates preparing for SSC CGL, SSC CHSL, SSC MTS, SSC CPO, SSC GD Constable and other competitive examinations. Every topic on this page is compiled from ${sourcesPhrase()} and written in the short, factual, one-line style that the General Awareness section of SSC papers actually tests — dates, full forms, ministries, venues, appointments and numbers — rather than long news reporting.</p>
    <p>${esc(plain(data.seoTopicsSentence || ''))} Each topic ends with an <strong>Important Facts for Exams</strong> box, and the page closes with ${mcqs.length} practice MCQs with answers.</p>`;

  const topicTable = `<h2>Topics covered on ${dateLong} and the sections they belong to</h2>
    <div class="scroller">
      <table class="tbl">
        <tr><th>Topic</th><th>Category</th><th>Most likely question</th></tr>
${topics.map(t => `        <tr><td>${esc(plain(t.rail || t.title))}</td><td>${esc(BUCKETS[t.bucket][1])}</td><td>${esc(plain(t.likely || ''))}</td></tr>`).join('\n')}
      </table>
    </div>`;

  const generic = [
    { q: 'Is current affairs enough to score well in SSC General Awareness?', a: 'No. Current affairs are important but static GK — History, Geography, Polity, Economics and Science — still carries the larger share of the General Awareness section. The most reliable approach is to read current affairs daily for about ten minutes and revise static GK chapter-wise alongside, using chapter-wise tests to check retention.' },
    { q: 'Are these daily current affairs pages free on TrickySSC?', a: 'Yes. All daily current affairs pages and the complete date-wise archive are free to read, with no login required. SSC CGL and SSC CHSL previous year papers are also free; the full 100-mock test series is available on the paid plan, with Mocks 1–4 free for everyone.' },
  ];
  const allFaqs = faqs.map(f => ({ q: plain(f.q), a: plain(f.a) })).concat(generic);
  const faqHtml = allFaqs.map(f => `    <details class="faq"><summary>${esc(f.q)}</summary><div class="fa">${esc(f.a)}</div></details>`).join('\n\n')
    + `\n\n    <p style="margin-top:26px;font-size:.92rem;color:var(--muted)">Last updated: ${dateLong} · Published by TrickySSC · Compiled from ${sourcesPhrase()} and presented for examination preparation purposes only.</p>`;

  const ld = [
    jsonLd({ '@context': 'https://schema.org', '@type': 'NewsArticle',
      headline: `Daily Current Affairs ${dateLong} for SSC CGL, CHSL, MTS and CPO`, description: meta,
      datePublished: `${iso}T20:00:00+05:30`, dateModified: `${iso}T20:00:00+05:30`, inLanguage: 'en-IN',
      mainEntityOfPage: { '@type': 'WebPage', '@id': canon },
      author: { '@type': 'Organization', name: 'TrickySSC', url: SITE + '/' },
      publisher: { '@type': 'Organization', name: 'TrickySSC', url: SITE + '/', logo: { '@type': 'ImageObject', url: SITE + '/favicon.png' } },
      image: [SITE + '/favicon.png'], articleSection: 'Current Affairs', keywords: `current affairs ${dateLong}, SSC CGL current affairs${kw ? ', ' + kw : ''}`,
      about: topics.slice(0, 5).map(t => ({ '@type': 'Thing', name: plain(t.rail || t.title) })) }),
    jsonLd({ '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: SITE + '/' },
      { '@type': 'ListItem', position: 2, name: 'Current Affairs', item: SITE + '/current-affairs.html' },
      { '@type': 'ListItem', position: 3, name: `Current Affairs ${dateLong}`, item: canon }] }),
    jsonLd({ '@context': 'https://schema.org', '@type': 'FAQPage',
      mainEntity: allFaqs.map(f => ({ '@type': 'Question', name: f.q, acceptedAnswer: { '@type': 'Answer', text: f.a } })) }),
  ].join('\n\n');

  const qs = JSON.stringify(mcqs.map(q => ({ q: plain(q.q), o: q.o.map(plain), a: q.a, e: plain(q.e) })), null, 1)
    .replace(/</g, '\\u003c');

  const tok = {
    HEAD_META: headMeta, DATE_LONG: dateLong, DD: pad(T.d), MON3: MONTHS[T.m - 1].slice(0, 3), WEEKDAY: weekday, YEAR: String(T.y),
    N_WORD: WORDS[topics.length] || String(topics.length), N_TOPICS2: pad(topics.length), N_MCQ: String(mcqs.length),
    N_FACTS: (Math.floor(nFacts / 10) * 10) + '+', READ_MIN: String(readMin),
    RAIL: rail, GLANCE: glanceHtml, STORIES: stories, SEO_INTRO: seoIntro, TOPIC_TABLE: topicTable,
    FAQ_HTML: faqHtml, JSONLD: ld, QS_JSON: qs,
  };
  let page = fs.readFileSync(TEMPLATE, 'utf8').replace(/\{\{([A-Z0-9_]+)\}\}/g, (m, k) => (k in tok ? tok[k] : m));
  if (!mcqs.length) page = page.replace(/<!-- ---------- QUIZ ---------- -->[\s\S]*?<\/section>/, '');
  fs.writeFileSync(outPath, page);
  log(`Wrote ca-archive/${file} — ${topics.length} topics, ${mcqs.length} MCQs`);

  // 6. hub + index + sitemap
  refreshArchive(iso, file);
  log('Done.');
})().catch(e => die(e.stack || e.message));
