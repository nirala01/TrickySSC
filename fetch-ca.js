// GitHub Action — Daily Current Affairs fetcher
// Sources: PIB RSS + Jina AI Search + Groq formatting

const https = require('https');
const fs    = require('fs');

const GROQ_KEY = process.env.GROQ_API_KEY;
if (!GROQ_KEY) { console.error('No GROQ_API_KEY'); process.exit(1); }

// ── Date helpers ──────────────────────────────────────────────────────────────
function getIST() {
  return new Date(Date.now() + 5.5 * 60 * 60 * 1000);
}
function fmtDate(d) {
  const dd = String(d.getUTCDate()).padStart(2,'0');
  const mm = String(d.getUTCMonth()+1).padStart(2,'0');
  return `${dd}-${mm}-${d.getUTCFullYear()}`;
}
function dispDate(d) {
  const days   = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  return `${days[d.getUTCDay()]}, ${d.getUTCDate()} ${months[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
}

// ── HTTP helpers ──────────────────────────────────────────────────────────────
function httpGet(url) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? require('https') : require('http');
    const req = mod.get(url, { headers: { 'User-Agent': 'Mozilla/5.0', 'Accept': '*/*' } }, res => {
      // Follow redirects
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return httpGet(res.headers.location).then(resolve).catch(reject);
      }
      let buf = '';
      res.on('data', c => buf += c);
      res.on('end', () => resolve(buf));
    });
    req.on('error', reject);
    req.setTimeout(20000, () => { req.destroy(); reject(new Error('Timeout')); });
  });
}

function httpsPost(url, headers, body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const u    = new URL(url);
    const req  = https.request({
      hostname: u.hostname, port: 443, path: u.pathname + u.search,
      method: 'POST',
      headers: { 'Content-Type':'application/json', 'Content-Length':Buffer.byteLength(data), ...headers }
    }, res => {
      let buf = '';
      res.on('data', c => buf += c);
      res.on('end', () => {
        try { resolve(JSON.parse(buf)); }
        catch(e) { reject(new Error('JSON parse: ' + buf.slice(0,200))); }
      });
    });
    req.on('error', reject);
    req.setTimeout(30000, () => { req.destroy(); reject(new Error('Timeout')); });
    req.write(data); req.end();
  });
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

// ── Source 1: PIB RSS ─────────────────────────────────────────────────────────
async function fetchPIB() {
  try {
    console.log('Fetching PIB RSS...');
    const xml = await httpGet('https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3');
    // Extract titles and descriptions from RSS
    const items = [];
    const titleRe  = /<title><!\[CDATA\[(.*?)\]\]><\/title>/g;
    const descRe   = /<description><!\[CDATA\[(.*?)\]\]><\/description>/g;
    const linkRe   = /<link>(.*?)<\/link>/g;
    let tm, dm, lm;
    const titles = []; const descs = []; const links = [];
    while ((tm = titleRe.exec(xml)) !== null)  titles.push(tm[1]);
    while ((dm = descRe.exec(xml))  !== null)  descs.push(dm[1]);
    while ((lm = linkRe.exec(xml))  !== null)  links.push(lm[1]);
    // Skip first (channel title)
    for (let i = 1; i < Math.min(titles.length, 20); i++) {
      const title = titles[i]?.trim();
      const desc  = descs[i]?.replace(/<[^>]+>/g,'').trim();
      if (title && title.length > 10) {
        items.push(`PIB: ${title}${desc ? ' — ' + desc.slice(0,300) : ''}`);
      }
    }
    console.log(`PIB: ${items.length} items`);
    return items;
  } catch(e) {
    console.warn('PIB fetch failed:', e.message);
    return [];
  }
}

// ── Source 2: Jina AI Search ──────────────────────────────────────────────────
async function fetchJinaSearch(query) {
  try {
    console.log(`Jina search: "${query}"`);
    const encoded = encodeURIComponent(query);
    const text = await httpGet(`https://s.jina.ai/${encoded}`);
    // Take first 3000 chars of results
    return text.slice(0, 3000);
  } catch(e) {
    console.warn(`Jina search failed for "${query}":`, e.message);
    return '';
  }
}

// ── Source 3: Jina Read specific pages ───────────────────────────────────────
async function fetchJinaRead(url) {
  try {
    console.log(`Jina read: ${url}`);
    const text = await httpGet(`https://r.jina.ai/${url}`);
    return text.slice(0, 3000);
  } catch(e) {
    console.warn(`Jina read failed for ${url}:`, e.message);
    return '';
  }
}

// ── Groq call ─────────────────────────────────────────────────────────────────
async function callGroq(prompt) {
  const MODELS = ['llama-3.3-70b-versatile', 'llama3-70b-8192', 'mixtral-8x7b-32768'];
  for (const model of MODELS) {
    for (let attempt = 1; attempt <= 3; attempt++) {
      try {
        console.log(`Groq: ${model} attempt ${attempt}`);
        const resp = await httpsPost(
          'https://api.groq.com/openai/v1/chat/completions',
          { 'Authorization': 'Bearer ' + GROQ_KEY },
          { model, messages:[{role:'user',content:prompt}], temperature:0.3, max_tokens:8000, response_format:{type:'json_object'} }
        );
        if (resp.error) throw new Error(resp.error.message);
        return JSON.parse(resp.choices[0].message.content);
      } catch(e) {
        console.warn(`${model} attempt ${attempt}: ${e.message.slice(0,80)}`);
        const retry = e.message.includes('rate') || e.message.includes('429') || e.message.includes('503');
        const skip  = e.message.includes('not found') || e.message.includes('404');
        if (skip) break;
        if (retry && attempt < 3) { console.log('Waiting 15s...'); await sleep(15000); }
        else if (!retry) break;
      }
    }
  }
  throw new Error('All Groq models failed');
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  const ist      = getIST();
  const dateKey  = fmtDate(ist);
  const dateDisp = dispDate(ist);

  console.log(`\n=== Fetching CA for ${dateDisp} ===\n`);

  // Fetch from multiple sources in parallel
  const [pibItems, jinaGK, jinaDrishti, jinaIndia, jinaIntl, jinaSports, jinaAppoint] = await Promise.all([
    fetchPIB(),
    fetchJinaSearch(`India current affairs today ${dateDisp} SSC exam government`),
    fetchJinaSearch(`India government news today ${dateDisp} PIB ministry scheme`),
    fetchJinaRead('https://www.gktoday.in/current-affairs/'),
    fetchJinaSearch(`international news today ${dateDisp} world summit UN treaty agreement`),
    fetchJinaSearch(`sports news today ${dateDisp} India cricket Olympics championship winner`),
    fetchJinaSearch(`appointments awards rankings India ${dateDisp} index report 2026`),
  ]);

  // Combine all sources
  const combinedSources = [
    pibItems.length ? `=== PIB GOVERNMENT NEWS ===\n${pibItems.join('\n')}` : '',
    jinaGK          ? `=== INDIA CURRENT AFFAIRS ===\n${jinaGK}` : '',
    jinaDrishti     ? `=== GOVERNMENT SCHEMES & POLICY ===\n${jinaDrishti}` : '',
    jinaIndia       ? `=== GKTODAY ===\n${jinaIndia}` : '',
    jinaIntl        ? `=== INTERNATIONAL NEWS ===\n${jinaIntl}` : '',
    jinaSports      ? `=== SPORTS NEWS ===\n${jinaSports}` : '',
    jinaAppoint     ? `=== APPOINTMENTS AWARDS RANKINGS ===\n${jinaAppoint}` : '',
  ].filter(Boolean).join('\n\n').slice(0, 15000);

  if (!combinedSources) {
    throw new Error('All sources returned empty — check network');
  }

  console.log(`\nTotal source content: ${combinedSources.length} chars`);

  // Format with Groq
  const prompt = `You are a current affairs expert for SSC and competitive exam preparation in India.

Today is ${dateDisp}.

Below is raw content from multiple Indian news sources (PIB, GKToday, web search).

Extract and format 18-22 important current affairs items for SSC exam preparation.

RAW SOURCE CONTENT:
${combinedSources}

Return ONLY a valid JSON object — no markdown:
{
  "date": "${dateDisp}",
  "dateKey": "${dateKey}",
  "generatedAt": "${new Date().toISOString()}",
  "sources": [],
  "items": [
    {
      "title": "Clear headline with full name/place/number",
      "whyInNews": "1-2 sentences — what happened, full names, exact date, place, numbers",
      "summary": "2-3 sentences with full proper names, numbers, places",
      "keyPoints": ["Fact 1", "Fact 2", "Fact 3", "Fact 4"],
      "importantPoints": ["Memory point 1 — HQ/founding year/full form", "Related act/article", "Historical context", "Key statistic", "Why it matters"],
      "category": "polity|economy|science|intl|environ|society|defence|sports|awards|general",
      "examRelevance": "Which SSC subject and why students must remember this",
      "tags": ["tag1", "tag2", "tag3"]
    }
  ]
}

RULES:
- Use ONLY information from the source content above
- Full proper names always — never vague references
- Specific numbers, ranks, amounts, dates
- MUST include items from ALL these categories:
  * Polity & Governance (India govt, schemes, bills, appointments)
  * Economy (budget, trade, GDP, RBI, markets)
  * Science & Tech (ISRO, DRDO, new technology, health)
  * International (UN, summits, treaties, foreign relations, world events)
  * Environment (climate, wildlife, pollution, green energy)
  * Defence (armed forces, exercises, weapons, borders)
  * Sports (cricket, Olympics, championships — include winner names, venues, scores)
  * Awards & Rankings (India's rank in global indices, who won what award)
  * Society & Education (NEP, social schemes, census)
- importantPoints: founding year, HQ, full form, related articles, historical facts
- For international news: include country names, leader names, organization names, treaty details
- For sports: always include winner name + country/team + venue + opponent + score/result
- For appointments: full name + designation + organization + who they replaced
- For awards: full award name + recipient full name + category + awarding body
- Return 20-25 items covering a good mix of all categories`;

  console.log('\nCalling Groq to format...');
  const data = await callGroq(prompt);

  // Validate
  const items = data.items || [];
  if (!items.length) throw new Error('No items in Groq response');

  const result = {
    date:        data.date        || dateDisp,
    dateKey:     data.dateKey     || dateKey,
    generatedAt: data.generatedAt || new Date().toISOString(),
    sources:     [],
    items
  };

  // Save main file
  fs.writeFileSync('current-affairs-data.json', JSON.stringify(result, null, 2), 'utf8');
  console.log(`\n✅ Saved ${items.length} items to current-affairs-data.json`);

  // Save archive
  const archiveDir = 'ca-archive';
  if (!fs.existsSync(archiveDir)) fs.mkdirSync(archiveDir);
  const archiveFile = `${archiveDir}/ca-${dateKey}.json`;
  fs.writeFileSync(archiveFile, JSON.stringify(result, null, 2), 'utf8');
  console.log(`✅ Archive: ${archiveFile}`);

  // Update index
  const indexFile = `${archiveDir}/index.json`;
  let index = [];
  try { index = JSON.parse(fs.readFileSync(indexFile, 'utf8')); } catch(e) {}
  const ei = index.findIndex(e => e.dateKey === dateKey);
  const entry = { date: result.date, dateKey, file: `ca-${dateKey}.json`, count: items.length };
  if (ei >= 0) index[ei] = entry; else index.unshift(entry);
  index.sort((a,b) => b.dateKey.split('-').reverse().join('').localeCompare(a.dateKey.split('-').reverse().join('')));
  if (index.length > 365) index = index.slice(0, 365);
  fs.writeFileSync(indexFile, JSON.stringify(index, null, 2), 'utf8');
  console.log(`✅ Index updated (${index.length} dates)`);
  console.log(`\nCategories: ${[...new Set(items.map(i=>i.category))].join(', ')}`);
}

main().catch(err => {
  console.error('\n❌ Fatal error:', err.message);
  process.exit(1);
});
