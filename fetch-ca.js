// GitHub Action script — runs daily, fetches CA via Groq, saves JSON

const https = require('https');
const fs    = require('fs');

const GROQ_KEY = process.env.GROQ_API_KEY;
if (!GROQ_KEY) { console.error('No GROQ_API_KEY'); process.exit(1); }

// ── Date helpers ─────────────────────────────────────────────────────────────
function getIST() {
  const now = new Date();
  return new Date(now.getTime() + 5.5 * 60 * 60 * 1000);
}
function formatDate(d) {
  const dd = String(d.getUTCDate()).padStart(2,'0');
  const mm = String(d.getUTCMonth()+1).padStart(2,'0');
  return `${dd}-${mm}-${d.getUTCFullYear()}`;
}
function displayDate(d) {
  const days   = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const months = ['January','February','March','April','May','June','July',
                  'August','September','October','November','December'];
  return `${days[d.getUTCDay()]}, ${d.getUTCDate()} ${months[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
}

// ── HTTPS helper ──────────────────────────────────────────────────────────────
function httpsPost(url, headers, body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const u    = new URL(url);
    const opts = {
      hostname: u.hostname, port: 443, path: u.pathname + u.search,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data), ...headers }
    };
    const req = https.request(opts, res => {
      let buf = '';
      res.on('data', c => buf += c);
      res.on('end', () => {
        try { resolve(JSON.parse(buf)); }
        catch(e) { reject(new Error('JSON parse failed: ' + buf.slice(0,300))); }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

// ── Groq call ─────────────────────────────────────────────────────────────────
async function callGroq(prompt) {
  const MODELS = ['llama-3.3-70b-versatile', 'llama3-70b-8192', 'mixtral-8x7b-32768'];

  for (const model of MODELS) {
    for (let attempt = 1; attempt <= 3; attempt++) {
      try {
        console.log(`Trying ${model} attempt ${attempt}...`);
        const resp = await httpsPost(
          'https://api.groq.com/openai/v1/chat/completions',
          { 'Authorization': 'Bearer ' + GROQ_KEY },
          {
            model,
            messages: [{ role: 'user', content: prompt }],
            temperature: 0.3,
            max_tokens: 8000,
            response_format: { type: 'json_object' }
          }
        );
        if (resp.error) throw new Error(resp.error.message || JSON.stringify(resp.error));
        const text = resp.choices[0].message.content;
        const parsed = JSON.parse(text);
        console.log(`✅ Got response from ${model}`);
        return parsed;
      } catch(err) {
        console.warn(`⚠️  ${model} attempt ${attempt}: ${err.message}`);
        const isRetry = err.message.includes('rate') || err.message.includes('429') || err.message.includes('503') || err.message.includes('overload');
        const isSkip  = err.message.includes('not found') || err.message.includes('404');
        if (isSkip) break;
        if (isRetry && attempt < 3) { console.log('Waiting 15s...'); await sleep(15000); }
        else if (!isRetry) break;
      }
    }
  }
  throw new Error('All Groq models failed');
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function fetchCA() {
  const ist      = getIST();
  const dateStr  = formatDate(ist);
  const dispDate = displayDate(ist);

  console.log(`Fetching CA for ${dispDate}`);

  const prompt = `You are a current affairs expert for SSC and competitive exam preparation in India.

Today is ${dispDate}.

Provide 20-25 important current affairs items for India from today or the past 1-2 days, relevant for SSC CGL, CHSL, and other competitive exams.

Draw content from reliable Indian news sources covering government, economy, science, sports, awards, and international affairs.

Return ONLY a valid JSON object — no markdown, no explanation:

{
  "date": "${dispDate}",
  "dateKey": "${dateStr}",
  "generatedAt": "${new Date().toISOString()}",
  "sources": [],
  "items": [
    {
      "title": "Clear headline with key name/place/number",
      "whyInNews": "1-2 sentences — what specifically happened, with full names, dates, places, numbers",
      "summary": "2-3 sentences with full proper names, exact numbers, specific places",
      "keyPoints": ["Specific fact with name/number", "Specific fact with date/place", "Specific fact with data"],
      "importantPoints": ["Point 1 for exam", "Point 2 for exam", "Point 3 for exam", "Point 4 for exam"],
      "category": "polity|economy|science|intl|environ|society|defence|sports|awards|general",
      "examRelevance": "Which SSC topic/subject and why it matters",
      "tags": ["tag1", "tag2", "tag3"]
    }
  ]
}

STRICT RULES:
- ALWAYS use full proper names — never "a minister", "an author", always the actual name
- ALWAYS include specific numbers — ranks, amounts, dates, percentages
- ALWAYS include place names — cities, states, countries
- Write content clearly and accurately based on the facts
- If award: full name + category + awarding body
- If scheme: scheme name + ministry + budget + beneficiaries
- If report/index: India rank + total countries + publishing org
- If sports: winner + venue + opponent + score
- Include all categories: Polity, Economy, Science & Tech, International, Environment, Society, Defence, Sports, Awards
- "whyInNews": triggering event with full facts
- "importantPoints": 4-5 memory points — founding year, HQ, full form, related article, historical context
- Return exactly the JSON structure above with items array`;

  try {
    const data = await callGroq(prompt);

    // Extract items — handle both {items:[]} and direct array
    let items = data.items || data.current_affairs || data.news || [];
    if (!Array.isArray(items) || !items.length) {
      throw new Error('No items array in response');
    }

    const result = {
      date:        data.date        || dispDate,
      dateKey:     data.dateKey     || dateStr,
      generatedAt: data.generatedAt || new Date().toISOString(),
      sources:     [],
      items
    };

    fs.writeFileSync('current-affairs-data.json', JSON.stringify(result, null, 2), 'utf8');
    console.log(`✅ Saved ${items.length} items to current-affairs-data.json`);
    console.log(`Categories: ${[...new Set(items.map(i=>i.category))].join(', ')}`);

  } catch(err) {
    console.error('❌ Error:', err.message);
    const fallback = {
      date: dispDate, dateKey: dateStr,
      generatedAt: new Date().toISOString(),
      error: err.message, sources: [], items: []
    };
    fs.writeFileSync('current-affairs-data.json', JSON.stringify(fallback, null, 2), 'utf8');
    process.exit(1);
  }
}

fetchCA();
