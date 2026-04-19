// GitHub Action — Daily Current Affairs
// Sources: PIB RSS + Jina Search (International, Sports, Appointments, India news)

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

// ── HTTP GET with redirect follow ─────────────────────────────────────────────
function httpGet(url, maxRedirects = 5) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : http;
    const req = mod.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; TrickySSC-Bot/1.0)',
        'Accept': 'text/html,application/xhtml+xml,*/*',
        'Accept-Language': 'en-US,en;q=0.9',
      }
    }, res => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location && maxRedirects > 0) {
        const next = res.headers.location.startsWith('http') ? res.headers.location : new URL(res.headers.location, url).href;
        return httpGet(next, maxRedirects - 1).then(resolve).catch(reject);
      }
      let buf = '';
      res.on('data', c => buf += c);
      res.on('end', () => resolve(buf));
    });
    req.on('error', reject);
    req.setTimeout(25000, () => { req.destroy(); reject(new Error('Timeout: ' + url)); });
  });
}

// ── Groq call ─────────────────────────────────────────────────────────────────
function httpsPost(url, headers, body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const u    = new URL(url);
    const req  = https.request({
      hostname: u.hostname, port: 443, path: u.pathname,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data), ...headers }
    }, res => {
      let buf = '';
      res.on('data', c => buf += c);
      res.on('end', () => { try { resolve(JSON.parse(buf)); } catch(e) { reject(new Error('Parse fail: ' + buf.slice(0,200))); } });
    });
    req.on('error', reject);
    req.setTimeout(30000, () => { req.destroy(); reject(new Error('Groq timeout')); });
    req.write(data); req.end();
  });
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

// ── Fetch PIB RSS ─────────────────────────────────────────────────────────────
async function fetchPIB() {
  try {
    const xml = await httpGet('https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3');
    const items = [];
    const re = /<item>[\s\S]*?<title><!\[CDATA\[(.*?)\]\]><\/title>[\s\S]*?<description><!\[CDATA\[(.*?)\]\]><\/description>[\s\S]*?<\/item>/g;
    let m;
    while ((m = re.exec(xml)) !== null && items.length < 15) {
      const title = m[1]?.trim();
      const desc  = m[2]?.replace(/<[^>]+>/g,'').replace(/\s+/g,' ').trim().slice(0,250);
      if (title && title.length > 5) items.push(`• ${title}: ${desc}`);
    }
    console.log(`PIB: ${items.length} items`);
    return items.join('\n');
  } catch(e) {
    console.warn('PIB failed:', e.message);
    return '';
  }
}

// ── Jina Search ───────────────────────────────────────────────────────────────
async function jinaSearch(query, label) {
  try {
    const url = `https://s.jina.ai/${encodeURIComponent(query)}`;
    const raw = await httpGet(url);
    // Extract just text content, remove URLs and junk
    const clean = raw
      .replace(/https?:\/\/\S+/g, '')
      .replace(/#{1,6}\s/g, '')
      .replace(/\[.*?\]\(.*?\)/g, '')
      .replace(/\s{3,}/g, '\n\n')
      .trim()
      .slice(0, 2500);
    console.log(`Jina [${label}]: ${clean.length} chars`);
    return clean;
  } catch(e) {
    console.warn(`Jina [${label}] failed:`, e.message);
    return '';
  }
}

// ── Groq format ───────────────────────────────────────────────────────────────
async function groqFormat(prompt) {
  const MODELS = ['llama-3.3-70b-versatile', 'llama3-70b-8192'];
  let lastErr;
  for (const model of MODELS) {
    for (let i = 1; i <= 3; i++) {
      try {
        const resp = await httpsPost(
          'https://api.groq.com/openai/v1/chat/completions',
          { 'Authorization': 'Bearer ' + GROQ_KEY },
          { model, messages:[{role:'user',content:prompt}], temperature:0.25, max_tokens:8000, response_format:{type:'json_object'} }
        );
        if (resp.error) throw new Error(resp.error.message);
        const parsed = JSON.parse(resp.choices[0].message.content);
        console.log(`Groq success: ${model}`);
        return parsed;
      } catch(e) {
        lastErr = e;
        console.warn(`${model} attempt ${i}: ${e.message.slice(0,80)}`);
        const retry = /rate|429|503|overload|demand/i.test(e.message);
        if (!retry) break;
        if (i < 3) { console.log('Waiting 15s...'); await sleep(15000); }
      }
    }
  }
  throw lastErr;
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  const ist     = getIST();
  const dateKey = fmtKey(ist);
  const dateTxt = fmtDisp(ist);
  console.log(`\n=== CA Fetch: ${dateTxt} ===\n`);

  // Fetch all sources in parallel
  console.log('Fetching all sources in parallel...');
  const [
    pib,
    indiaNews,
    intlNews,
    sportsNews,
    appointAwards,
    scienceEnv,
  ] = await Promise.all([
    fetchPIB(),
    jinaSearch(`India current affairs ${dateTxt} government scheme policy economy`, 'India'),
    jinaSearch(`international news today ${dateTxt} UN summit treaty world leaders`, 'International'),
    jinaSearch(`sports results today ${dateTxt} India cricket football chess winner medal`, 'Sports'),
    jinaSearch(`India appointments awards rankings index ${dateTxt} 2026`, 'Appoint/Awards'),
    jinaSearch(`India science technology space ISRO environment climate ${dateTxt}`, 'Science/Env'),
  ]);

  console.log('\nAll sources fetched. Sending to Groq...\n');

  const prompt = `You are a current affairs expert for SSC and competitive exam preparation in India.
Today is ${dateTxt}.

Below are news items from MULTIPLE distinct sources. You MUST extract items from EACH source section.

=== SOURCE A: PIB (Government Press Releases) ===
${pib || 'No data'}

=== SOURCE B: India News (Government, Economy, Schemes) ===
${indiaNews || 'No data'}

=== SOURCE C: International News (World Events, UN, Summits) ===
${intlNews || 'No data'}

=== SOURCE D: Sports News (Results, Champions, Medals) ===
${sportsNews || 'No data'}

=== SOURCE E: Appointments, Awards & Rankings ===
${appointAwards || 'No data'}

=== SOURCE F: Science, Technology & Environment ===
${scienceEnv || 'No data'}

TASK: Extract 20-25 current affairs items. You MUST include items from EVERY source section above.
Minimum coverage required:
- At least 4 items from SOURCE A (PIB)
- At least 3 items from SOURCE B (India news)
- At least 3 items from SOURCE C (International)
- At least 3 items from SOURCE D (Sports)
- At least 3 items from SOURCE E (Appointments/Awards)
- At least 2 items from SOURCE F (Science/Environment)

Return ONLY valid JSON — no markdown:
{
  "date": "${dateTxt}",
  "dateKey": "${dateKey}",
  "generatedAt": "${new Date().toISOString()}",
  "sources": [],
  "items": [
    {
      "title": "Headline with full name/place/number",
      "whyInNews": "What happened — full names, date, place, numbers",
      "summary": "2-3 sentences with proper names, numbers, places",
      "keyPoints": ["Specific fact 1", "Fact 2", "Fact 3", "Fact 4"],
      "importantPoints": ["HQ/founding year/full form", "Related act/article", "Historical context", "Key stat", "Why it matters"],
      "category": "polity|economy|science|intl|environ|society|defence|sports|awards|general",
      "examRelevance": "SSC subject and why to remember",
      "tags": ["tag1","tag2","tag3"]
    }
  ]
}

STRICT RULES:
- Full proper names always
- Specific numbers, ranks, amounts, dates
- Sports: winner + country/team + venue + opponent + score
- Appointments: full name + designation + organization
- International: country + leader name + organization + what happened
- Awards: recipient + full award name + category + awarding body
- Rankings: India rank + total countries + publishing organization`;

  const data  = await groqFormat(prompt);
  const items = data.items || [];
  if (!items.length) throw new Error('No items returned');

  const result = {
    date: data.date || dateTxt,
    dateKey: data.dateKey || dateKey,
    generatedAt: data.generatedAt || new Date().toISOString(),
    sources: [],
    items
  };

  // Save files
  fs.writeFileSync('current-affairs-data.json', JSON.stringify(result, null, 2));
  console.log(`✅ Saved ${items.length} items`);

  const dir = 'ca-archive';
  if (!fs.existsSync(dir)) fs.mkdirSync(dir);
  fs.writeFileSync(`${dir}/ca-${dateKey}.json`, JSON.stringify(result, null, 2));
  console.log(`✅ Archive: ${dir}/ca-${dateKey}.json`);

  // Update index
  let index = [];
  try { index = JSON.parse(fs.readFileSync(`${dir}/index.json`, 'utf8')); } catch(e) {}
  const ei = index.findIndex(e => e.dateKey === dateKey);
  const entry = { date: result.date, dateKey, file: `ca-${dateKey}.json`, count: items.length };
  if (ei >= 0) index[ei] = entry; else index.unshift(entry);
  index.sort((a,b) => b.dateKey.split('-').reverse().join('').localeCompare(a.dateKey.split('-').reverse().join('')));
  if (index.length > 365) index = index.slice(0,365);
  fs.writeFileSync(`${dir}/index.json`, JSON.stringify(index, null, 2));
  console.log(`✅ Index: ${index.length} dates`);

  // Log category breakdown
  const cats = {};
  items.forEach(i => { cats[i.category] = (cats[i.category]||0)+1; });
  console.log('\nCategory breakdown:');
  Object.entries(cats).forEach(([k,v]) => console.log(`  ${k}: ${v}`));
}

main().catch(err => {
  console.error('\n❌ Fatal:', err.message);
  process.exit(1);
});
