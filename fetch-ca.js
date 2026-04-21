// GitHub Action — Daily Current Affairs
// Sources: PIB RSS + Indian Express RSS + Hindu RSS + Groq formatting

const https = require('https');
const http  = require('http');
const fs    = require('fs');

const GROQ_KEY = process.env.GROQ_API_KEY;
if (!GROQ_KEY) { console.error('No GROQ_API_KEY'); process.exit(1); }

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
function parseRSS(xml, sourceName, maxItems = 20) {
  const items = [];
  // Match <item> blocks
  const itemRe = /<item>([\s\S]*?)<\/item>/g;
  let m;
  while ((m = itemRe.exec(xml)) !== null && items.length < maxItems) {
    const block = m[1];
    const title = (block.match(/<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?<\/title>/) || [])[1]?.trim();
    const desc  = (block.match(/<description>(?:<!\[CDATA\[)?([\s\S]*?)(?:\]\]>)?<\/description>/) || [])[1]
                    ?.replace(/<[^>]+>/g, '').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/\s+/g,' ').trim().slice(0, 300);
    if (title && title.length > 5) {
      items.push(`[${sourceName}] ${title}${desc ? ': ' + desc : ''}`);
    }
  }
  return items;
}

// ── Fetch RSS sources ─────────────────────────────────────────────────────────
async function fetchRSS(url, name, max = 20) {
  try {
    console.log(`Fetching RSS: ${name}`);
    const xml   = await httpGet(url);
    const items = parseRSS(xml, name, max);
    console.log(`  ${name}: ${items.length} items`);
    return items;
  } catch(e) {
    console.warn(`  ${name} failed: ${e.message}`);
    return [];
  }
}

// ── Groq call ─────────────────────────────────────────────────────────────────
function httpsPost(url, headers, body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const u    = new URL(url);
    const req  = https.request({
      hostname: u.hostname, port: 443, path: u.pathname,
      method: 'POST',
      headers: { 'Content-Type':'application/json', 'Content-Length':Buffer.byteLength(data), ...headers }
    }, res => {
      let buf = '';
      res.on('data', c => buf += c);
      res.on('end', () => { try { resolve(JSON.parse(buf)); } catch(e) { reject(new Error('Parse: '+buf.slice(0,200))); } });
    });
    req.on('error', reject);
    req.setTimeout(60000, () => { req.destroy(); reject(new Error('Groq timeout')); });
    req.write(data); req.end();
  });
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function groqCall(prompt) {
  const MODELS = [
    'llama-3.3-70b-versatile',
    'llama-3.3-70b-specdec',
    'llama3-groq-70b-8192-tool-use-preview',
  ];
  let lastErr;
  for (const model of MODELS) {
    for (let i = 1; i <= 3; i++) {
      try {
        console.log(`  Groq [${model}] attempt ${i}`);
        const resp = await httpsPost(
          'https://api.groq.com/openai/v1/chat/completions',
          { 'Authorization': 'Bearer ' + GROQ_KEY },
          { model, messages:[{role:'user',content:prompt}], temperature:0.25, max_tokens:6000, response_format:{type:'json_object'} }
        );
        if (resp.error) throw new Error(resp.error.message);
        const parsed = JSON.parse(resp.choices[0].message.content);
        console.log(`  Success: ${model}`);
        return parsed;
      } catch(e) {
        lastErr = e;
        const retry = /rate|429|503|overload|demand/i.test(e.message);
        const skip  = /decommission|no longer support|not found|404/i.test(e.message);
        console.warn(`  ${model} attempt ${i}: ${e.message.slice(0,100)}`);
        if (skip) { console.log(`  Skipping ${model} (decommissioned)`); break; }
        if (retry && i < 3) { console.log(`  Rate limit — waiting 30s...`); await sleep(30000); }
        else if (!retry) break;
      }
    }
  }
  throw lastErr || new Error('All Groq models failed');
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  const ist     = getIST();
  const dateKey = fmtKey(ist);
  const dateTxt = fmtDisp(ist);
  console.log(`\n=== CA Fetch: ${dateTxt} ===\n`);

  // Skip if already successfully ran today (archive file exists with items)
  try {
    const existing = fs.readFileSync(`ca-archive/ca-${dateKey}.json`, 'utf8');
    const parsed   = JSON.parse(existing);
    if (parsed.items && parsed.items.length >= 10) {
      console.log(`✅ Already have ${parsed.items.length} items for ${dateKey} — skipping duplicate run`);
      return;
    }
  } catch(e) { /* file doesn't exist yet — proceed */ }

  // Fetch multiple RSS feeds in parallel — all free, no auth needed
  const [
    pibItems,
    indianExpressItems,
    hinduItems,
    hinduSportsItems,
    pibScienceItems,
    pib2Items,
  ] = await Promise.all([
    fetchRSS('https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3',   'PIB-National',    20),
    fetchRSS('https://indianexpress.com/section/india/feed/',              'IndianExpress',   15),
    fetchRSS('https://www.thehindu.com/news/national/?service=rss',       'TheHindu',        15),
    fetchRSS('https://www.thehindu.com/sport/?service=rss',               'Hindu-Sports',    10),
    fetchRSS('https://pib.gov.in/RssMain.aspx?ModId=23&Lang=1&Regid=3',  'PIB-Science',     10),
    fetchRSS('https://pib.gov.in/RssMain.aspx?ModId=7&Lang=1&Regid=3',   'PIB-Finance',     10),
  ]);

  const allItems = [
    ...pibItems,
    ...pib2Items,
    ...pibScienceItems,
    ...indianExpressItems,
    ...hinduItems,
    ...hinduSportsItems,
  ];

  console.log(`\nTotal RSS items collected: ${allItems.length}`);

  if (allItems.length < 5) {
    throw new Error('Too few RSS items — check network connectivity');
  }

  // Split into two batches for two separate Groq calls
  const half    = Math.ceil(allItems.length / 2);
  const batch1  = allItems.slice(0, half);
  const batch2  = allItems.slice(half);

  const makePrompt = (items, focus) => `You are a current affairs expert for SSC competitive exam prep in India.
Today: ${dateTxt}.

Extract important current affairs from these news headlines:
${items.join('\n')}

Focus on: ${focus}

STRICTLY EXCLUDE — do NOT include these types of news:
- Crime, murder, rape, assault, accidents, deaths of individuals
- Political party fights, blame games, election rhetoric, party controversies
- Celebrity/film/TV/entertainment news
- Religious disputes, communal incidents, riots
- Personal tragedies, domestic violence, suicides
- Sensational or tabloid-style news
- Petty state-level political squabbles

ONLY include SSC-exam-relevant news:
- Government schemes, policies, bills, acts, budgets
- International relations, treaties, summits, UN/global events
- Science, space, technology, defence achievements
- Economy — RBI, GDP, trade, markets, indices
- Sports championships, medals, records (not personal life)
- Awards, appointments to key positions, global rankings
- Environment — climate agreements, wildlife, conservation
- Constitutional/judicial matters of national importance

Return ONLY valid JSON — no markdown:
{
  "items": [
    {
      "title": "Clear headline — full names, place, number",
      "whyInNews": "1-2 sentences — what happened, who, where, when, numbers",
      "summary": "2-3 detailed sentences with full proper names, exact numbers, specific places, background context",
      "keyPoints": ["Specific fact with name/number", "Specific fact with date/place", "Specific fact with data", "Another important detail"],
      "importantPoints": ["Full form / HQ / founding year of key organization", "Related constitutional article / act / amendment", "Historical background or previous context", "Key statistics or data points", "Why it matters for India / global significance"],
      "category": "polity|economy|science|intl|environ|society|defence|sports|awards|general",
      "examRelevance": "SSC subject/topic and specific reason why students must remember this",
      "tags": ["tag1","tag2","tag3"]
    }
  ]
}

RULES:
- Extract 10-12 items — only SSC-relevant news, skip everything else
- Full proper names always — never vague like "a minister", "a country"
- If headline is brief, USE YOUR KNOWLEDGE to fill full details
- Sports: winner+team+venue+score. Appointments: name+designation+org
- International: country+leader+event+outcome. Awards: recipient+award+body
- importantPoints MUST have 5 points — founding year, HQ, full form, related act, historical fact
- summary MUST be 3 detailed sentences`;

  console.log('\nCalling Groq Batch 1 (India/PIB/Economy)...');
  const r1 = await groqCall(makePrompt(
    batch1,
    'Polity, Economy, Science & Tech, Environment, Defence, Society — India-focused news'
  ));

  console.log('Waiting 40s before Batch 2 to avoid rate limit...');
  await sleep(40000);

  console.log('Calling Groq Batch 2 (International/Sports/Awards)...');
  const r2 = await groqCall(makePrompt(
    batch2,
    'International Affairs, Sports results, Awards, Appointments, Global Rankings'
  ));

  const items = [...(r1.items||[]), ...(r2.items||[])];
  console.log(`\nTotal items: ${items.length} (B1:${r1.items?.length||0} B2:${r2.items?.length||0})`);

  if (!items.length) throw new Error('No items from Groq');

  const result = {
    date:        dateTxt,
    dateKey,
    generatedAt: new Date().toISOString(),
    sources:     ['PIB', 'The Hindu', 'Indian Express'],
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
