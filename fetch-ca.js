// GitHub Action — Daily Current Affairs (TrickySSC)
// Source: PIB (Press Information Bureau) RSS ONLY
// Model : Google Gemini, called through a Cloudflare Worker that holds the API key
//
// Required env : GEMINI_WORKER_URL   e.g. https://ca-gemini.<you>.workers.dev
//                                    (a full ...:generateContent URL also works)
// Optional env : GEMINI_WORKER_TOKEN sent as "Authorization: Bearer <token>"
//                GEMINI_MODEL        overrides the first model in the chain

const https = require('https');
const http  = require('http');
const fs    = require('fs');

const WORKER_URL   = (process.env.GEMINI_WORKER_URL || '').trim().replace(/\/+$/, '');
const WORKER_TOKEN = (process.env.GEMINI_WORKER_TOKEN || '').trim();
if (!WORKER_URL) { console.error('No GEMINI_WORKER_URL'); process.exit(1); }

// Preferred order. Flash is fast + generous free quota; lite is the cheaper
// fallback; 2.0-flash is the last resort if both 2.5 models are rate-limited.
const MODELS = [
  process.env.GEMINI_MODEL || 'gemini-2.5-flash',
  'gemini-2.5-flash-lite',
  'gemini-2.0-flash',
].filter((m, i, a) => a.indexOf(m) === i);

// ── Date helpers ──────────────────────────────────────────────────────────────
function getIST() { return new Date(Date.now() + 5.5 * 60 * 60 * 1000); }
function fmtKey(d) {
  return `${String(d.getUTCDate()).padStart(2,'0')}-${String(d.getUTCMonth()+1).padStart(2,'0')}-${d.getUTCFullYear()}`;
}
function fmtDisp(d) {
  const days   = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  return `${days[d.getUTCDay()]}, ${d.getUTCDate()} ${months[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
}

// ── HTTP GET ──────────────────────────────────────────────────────────────────
function httpGet(url, maxRedirects = 5) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : http;
    const req = mod.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; RSS-Reader/1.0)',
        'Accept': 'application/rss+xml, application/xml, text/xml, */*',
      }
    }, res => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location && maxRedirects > 0) {
        const next = res.headers.location.startsWith('http')
          ? res.headers.location
          : new URL(res.headers.location, url).href;
        return httpGet(next, maxRedirects - 1).then(resolve).catch(reject);
      }
      let buf = '';
      res.setEncoding('utf8');
      res.on('data', c => buf += c);
      res.on('end', () => resolve(buf));
    });
    req.on('error', reject);
    req.setTimeout(20000, () => { req.destroy(); reject(new Error('Timeout')); });
  });
}

// ── Parse RSS XML ─────────────────────────────────────────────────────────────
function decode(s) {
  return s.replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>')
          .replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/&nbsp;/g,' ');
}
function parseRSS(xml, maxItems = 80) {
  const items = [];
  const itemRe = /<item>([\s\S]*?)<\/item>/g;
  let m;
  while ((m = itemRe.exec(xml)) !== null && items.length < maxItems) {
    const block = m[1];
    const title = (block.match(/<title>(?:<!\[CDATA\[)?([\s\S]*?)(?:\]\]>)?<\/title>/) || [])[1]
                    ?.replace(/<[^>]+>/g,'').replace(/\s+/g,' ').trim();
    const desc  = (block.match(/<description>(?:<!\[CDATA\[)?([\s\S]*?)(?:\]\]>)?<\/description>/) || [])[1]
                    ?.replace(/<[^>]+>/g, '').replace(/\s+/g,' ').trim().slice(0, 350);
    const link  = (block.match(/<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?<\/link>/) || [])[1]?.trim();
    if (title && title.length > 5) {
      items.push({ title: decode(title), desc: desc ? decode(desc) : '', link: link || '' });
    }
  }
  return items;
}

async function fetchRSS(url, name, max = 80) {
  try {
    console.log(`Fetching RSS: ${name}`);
    const xml   = await httpGet(url);
    const items = parseRSS(xml, max);
    console.log(`  ${name}: ${items.length} items`);
    return items;
  } catch(e) {
    console.warn(`  ${name} failed: ${e.message}`);
    return [];
  }
}

// Pre-filter: PIB publishes a lot of routine noise. Drop the obvious junk
// before it ever reaches the model so the prompt stays focused.
const NOISE = [
  /weather|rainfall|heat ?wave|cold ?wave|cyclone alert|imd (bulletin|warning)/i,
  /lok sabha (question|reply)|rajya sabha (question|reply)|reply to (a |an )?(unstarred|starred)/i,
  /tender|vacancy|recruitment|walk[- ]in|corrigendum|advertisement/i,
  /media (advisory|invitation)|photo release|press conference to be held/i,
  /shri .{3,60} (to visit|visits|will visit|inaugurate|inaugurates|addresses|chairs|reviews|holds? meeting)/i,
  /(review|reviews|reviewed) (the )?(progress|meeting|status|preparedness)/i,
  /condole|condolence|pays? (homage|tribute)|birth anniversary|death anniversary/i,
  /greets|greetings|extends (his |her )?(best )?wishes|felicitat/i,
  /price of (petrol|diesel|onion|tomato)|mandi price/i,
];
function isNoise(t) { return NOISE.some(re => re.test(t)); }

// ── Gemini call (via Cloudflare Worker) ───────────────────────────────────────
function httpsPost(url, headers, body, timeoutMs = 120000) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const u    = new URL(url);
    const mod  = u.protocol === 'http:' ? http : https;
    const req  = mod.request({
      hostname: u.hostname, port: u.port || (u.protocol === 'http:' ? 80 : 443),
      path: u.pathname + u.search, method: 'POST',
      headers: { 'Content-Type':'application/json', 'Content-Length':Buffer.byteLength(data), ...headers }
    }, res => {
      let buf = '';
      res.on('data', c => buf += c);
      res.on('end', () => {
        try { resolve({ status: res.statusCode, json: JSON.parse(buf) }); }
        catch(e) { resolve({ status: res.statusCode, json: null, raw: buf }); }
      });
    });
    req.on('error', reject);
    req.setTimeout(timeoutMs, () => { req.destroy(); reject(new Error('Worker timeout')); });
    req.write(data); req.end();
  });
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

function endpointFor(model) {
  // If the secret already points at a ...:generateContent URL, use it verbatim
  // (the Worker decides the model). Otherwise append the standard Gemini path.
  if (/:generateContent/i.test(WORKER_URL)) return WORKER_URL;
  return `${WORKER_URL}/v1beta/models/${model}:generateContent`;
}

// Pull the model's text out of whatever the Worker returned — a raw Gemini
// response, or a simplified {text}/{output}/{result} wrapper.
function extractText(j) {
  if (!j) return null;
  if (typeof j === 'string') return j;
  if (typeof j.text === 'string') return j.text;
  if (typeof j.output === 'string') return j.output;
  if (typeof j.result === 'string') return j.result;
  const parts = j.candidates?.[0]?.content?.parts;
  if (Array.isArray(parts)) return parts.map(p => p.text || '').join('');
  return null;
}

function parseJSON(text) {
  let t = text.trim().replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/, '');
  const a = t.indexOf('{'), b = t.lastIndexOf('}');
  if (a > 0 || b < t.length - 1) t = t.slice(a, b + 1);
  return JSON.parse(t);
}

async function geminiCall(prompt) {
  let lastErr;
  const headers = WORKER_TOKEN ? { 'Authorization': 'Bearer ' + WORKER_TOKEN } : {};
  for (const model of MODELS) {
    for (let i = 1; i <= 3; i++) {
      try {
        console.log(`  Gemini [${model}] attempt ${i}`);
        const { status, json, raw } = await httpsPost(endpointFor(model), headers, {
          contents: [{ role: 'user', parts: [{ text: prompt }] }],
          generationConfig: {
            temperature: 0.3,
            maxOutputTokens: 16000,
            responseMimeType: 'application/json',
          },
        });
        if (status >= 400 || json?.error) {
          const msg = json?.error?.message || json?.error || raw || `HTTP ${status}`;
          throw new Error(`HTTP ${status}: ${String(msg).slice(0, 300)}`);
        }
        const finish = json?.candidates?.[0]?.finishReason;
        if (finish && !/STOP|MAX_TOKENS/i.test(finish)) throw new Error(`finishReason ${finish}`);
        const text = extractText(json);
        if (!text) throw new Error('Empty response: ' + (raw || JSON.stringify(json)).slice(0, 200));
        const parsed = parseJSON(text);
        console.log(`  Success: ${model}`);
        return parsed;
      } catch(e) {
        lastErr = e;
        const msg   = e.message;
        const skip  = /not found|does not exist|not supported|deprecated|404/i.test(msg);
        const retry = /429|quota|rate|503|overload|unavailable|timeout|Unexpected token|JSON/i.test(msg);
        console.warn(`  ${model} attempt ${i}: ${msg.slice(0,160)}`);
        if (skip) { console.log(`  Skipping ${model}`); break; }
        if (retry && i < 3) { console.log('  Waiting 20s before retry...'); await sleep(20000); }
        else if (!retry) break;
      }
    }
  }
  throw lastErr || new Error('All Gemini models failed');
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  const ist     = getIST();
  const dateKey = fmtKey(ist);
  const dateTxt = fmtDisp(ist);
  console.log(`\n=== CA Fetch (PIB → Gemini): ${dateTxt} ===\n`);

  // Skip if already successfully ran today (archive file exists with items)
  try {
    const existing = fs.readFileSync(`ca-archive/ca-${dateKey}.json`, 'utf8');
    const parsed   = JSON.parse(existing);
    if (parsed.items && parsed.items.length >= 8) {
      console.log(`✅ Already have ${parsed.items.length} items for ${dateKey} — skipping duplicate run`);
      return;
    }
  } catch(e) { /* file doesn't exist yet — proceed */ }

  // PIB publishes ONE national RSS feed (all ministries). ModId=6 = press
  // releases, Lang=1 = English, Regid=3 = National (PIB Delhi).
  const raw = await fetchRSS('https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3', 'PIB-National', 100);

  // Dedupe by title (PIB often posts the same release twice, once per region)
  const seen = new Set();
  const uniq = raw.filter(r => {
    const k = r.title.toLowerCase().replace(/[^a-z0-9]/g,'');
    if (seen.has(k)) return false;
    seen.add(k); return true;
  });
  const kept = uniq.filter(r => !isNoise(r.title));
  console.log(`\nPIB releases: ${raw.length} fetched → ${uniq.length} unique → ${kept.length} after noise filter`);

  if (kept.length < 3) throw new Error('Too few PIB items — check the PIB RSS feed / network');

  const lines = kept.map((r, i) => `${i+1}. ${r.title}${r.desc ? ' — ' + r.desc : ''}`);

  const prompt = `You are a current affairs editor for SSC (CGL/CHSL/MTS) exam preparation in India, working ONLY from today's official Press Information Bureau (PIB) press releases.
Today: ${dateTxt}.

PIB publishes far more than SSC needs. Your job is to FILTER, not summarise everything.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TODAY'S PIB RELEASES (title — first lines):
${lines.join('\n')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEEP a release ONLY if it fits one of these 10 SSC buckets (use the exact category code):

HIGHEST PRIORITY
 1. "schemes"      — NEW scheme/programme launched, or an existing scheme expanded/renamed/changed. Capture: implementing ministry, objective, target group, financial outlay, period.
 2. "cabinet"      — Cabinet / CCEA / CCS decisions: schemes approved, bills/acts approved, major policy decisions, financial outlays, new initiatives.
 3. "appointments" — Important appointments: heads/chairpersons of major organisations, constitutional posts, ambassadors, Indian appointees to international bodies.
 4. "awards"       — National / government / major sports / cultural / scientific awards and honours announced or conferred.
 5. "science"      — Space missions, AI, quantum, semiconductors, biotech, defence-tech, indigenous technologies, ISRO/DRDO/CSIR achievements.

VERY USEFUL
 6. "defence"      — New missiles/weapons/platforms, military exercises (name + countries + venue), defence agreements, indigenous systems, notable operations.
 7. "economy"      — Major economic policies, RBI/SEBI/GST decisions, GDP or other indicators highlighted by government, financial inclusion, digital payments (UPI etc.), Budget/Economic Survey facts.
 8. "intl"         — India + country agreements/MoUs, summits, BRICS/G20/SCO/ASEAN/QUAD/UN, international organisations, official visits by PM/President/EAM with a concrete outcome.
 9. "environ"      — National parks/wildlife, tiger/elephant/cheetah conservation, climate initiatives, environmental reports, international environmental agreements.
10. "agri"         — MSP announcements, new agricultural schemes/missions, crop production figures, farmer welfare, GI-tag developments in agri produce.
11. "culture"      — UNESCO developments, GI tags, festivals with a factual hook, archaeological discoveries, monuments/heritage projects.
12. "sports"       — Major Indian achievements, tournaments hosted by India, Khelo India, National Sports Awards, government sports schemes.

(12 codes cover the 10 buckets: Sports/Culture and Economy/Agriculture are split so the site can filter them.)

STRICTLY DROP — never include:
- Routine minister speeches, visits, inaugurations, meetings, reviews, "addresses gathering"
- Ordinary departmental/administrative announcements and detailed statistics with no exam hook
- Parliamentary questions/replies unless they reveal ONE very important new fact
- Highly technical research papers, weather/IMD bulletins, condolences, greetings, tenders
- Anything already covered by another kept item (merge duplicates into one)

Return ONLY valid JSON — no markdown, no code fences:
{
  "items": [
    {
      "title": "Clear headline with the key name/scheme/place/number — never vague",
      "whyInNews": "1-2 sentences — what specifically happened per PIB: full names of people/organisations/ministries, exact date, place, exact numbers/amounts",
      "summary": "Exactly 3 sentences. Every sentence must contain full proper names, exact figures, specific locations. No vague words like recently, some, various, officials.",
      "keyPoints": [
        "Specific fact with full name and number",
        "Specific fact with exact date and place",
        "Specific fact with data, outlay or statistic",
        "Another standalone important detail"
      ],
      "importantPoints": [
        "Full form AND founding year AND headquarters of the key organisation/ministry mentioned",
        "Related constitutional article OR act OR amendment OR parent scheme with year",
        "Historical context — first time, previous version, previous record holder, or background",
        "Key statistic — outlay in crore, beneficiaries, rank, target year",
        "Why this matters for India / policy implication"
      ],
      "mcq": {
        "question": "One SSC-style one-liner MCQ on the single most testable fact",
        "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
        "answer": "A"
      },
      "category": "schemes|cabinet|appointments|awards|science|defence|economy|intl|environ|agri|culture|sports",
      "ministry": "Full name of the ministry/department that issued the release",
      "examRelevance": "Exact SSC subject and chapter — e.g. GK: Government Schemes, Economy: RBI Monetary Policy, Science: Space",
      "tags": ["tag1","tag2","tag3"]
    }
  ]
}

STRICT RULES — violations make the content useless for students:
- Use ONLY facts present in the PIB text above. Do NOT invent dates, outlays, names or numbers. If a figure is not in the release, omit it rather than guess.
- NEVER use vague words: recently, some, various, certain, officials, a country, a minister — always full proper names
- Full name on first use for every person, organisation, ministry, place, scheme
- Schemes: scheme full name + ministry + objective + target group + outlay/period (whatever PIB gives)
- Cabinet: exact decision + outlay + duration + beneficiaries
- Appointments: appointee full name + exact designation + full organisation name + predecessor if given
- Awards: recipient + award full name + category + awarding body + year award was instituted (if known reliably)
- Defence: system/exercise full name + agency (DRDO/HAL etc.) + countries + venue
- International: country + leader full name + organisation full name + concrete outcome
- importantPoints item 1 MUST have full form + founding year + HQ city of the main organisation/ministry
- importantPoints item 2 MUST cite a specific article number, act name with year, or parent scheme with year
- importantPoints item 3 MUST give a historical fact — year, previous record, or context
- keyPoints: exactly 4 items, each a crisp standalone fact a student can memorise
- mcq: exactly 4 options, answer is a single letter A-D
- Order items by priority: schemes/cabinet first, then appointments/awards/science, then the rest
- Return 8-12 items if the day is rich; fewer is fine on a thin day. Quality over quantity — a strong 6 beats a padded 12.`;

  console.log(`\nCalling Gemini with ${kept.length} PIB releases (${Buffer.byteLength(prompt)} bytes prompt)...`);
  const r = await geminiCall(prompt);

  const VALID = new Set(['schemes','cabinet','appointments','awards','science','defence','economy','intl','environ','agri','culture','sports']);
  const items = (r.items || []).filter(i => i && i.title).map(i => ({
    ...i,
    category: VALID.has(i.category) ? i.category : 'general',
  }));

  console.log(`\nTotal items: ${items.length}`);
  if (!items.length) throw new Error('No items from Gemini');

  const result = {
    date:        dateTxt,
    dateKey,
    generatedAt: new Date().toISOString(),
    sources:     ['PIB'],
    model:       'gemini',
    items
  };

  // Save files
  fs.writeFileSync('current-affairs-data.json', JSON.stringify(result, null, 2));
  console.log(`✅ Saved ${items.length} items → current-affairs-data.json`);

  const dir = 'ca-archive';
  if (!fs.existsSync(dir)) fs.mkdirSync(dir);
  fs.writeFileSync(`${dir}/ca-${dateKey}.json`, JSON.stringify(result, null, 2));
  console.log(`✅ Archive → ${dir}/ca-${dateKey}.json`);

  // Update index
  let index = [];
  try { index = JSON.parse(fs.readFileSync(`${dir}/index.json`, 'utf8')); } catch(e) {}
  const ei    = index.findIndex(e => e.dateKey === dateKey);
  const entry = { date: dateTxt, dateKey, file: `ca-${dateKey}.json`, count: items.length };
  if (ei >= 0) index[ei] = entry; else index.unshift(entry);
  index.sort((a,b) => b.dateKey.split('-').reverse().join('').localeCompare(a.dateKey.split('-').reverse().join('')));
  if (index.length > 365) index = index.slice(0,365);
  fs.writeFileSync(`${dir}/index.json`, JSON.stringify(index, null, 2));
  console.log(`✅ Index updated: ${index.length} dates`);

  // Category breakdown
  const cats = {};
  items.forEach(i => { cats[i.category] = (cats[i.category]||0)+1; });
  console.log('\nCategory breakdown:');
  Object.entries(cats).sort((a,b)=>b[1]-a[1]).forEach(([k,v]) => console.log(`  ${k}: ${v}`));
}

main().catch(err => {
  console.error('\n❌ Fatal:', err.message);
  process.exit(1);
});
