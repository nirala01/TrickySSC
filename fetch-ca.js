// GitHub Action script — runs daily, fetches CA via Gemini, saves JSON

const https = require('https');
const fs    = require('fs');

const GEMINI_KEY = process.env.GEMINI_API_KEY;
if (!GEMINI_KEY) { console.error('No GEMINI_API_KEY'); process.exit(1); }

// ── Date helpers ────────────────────────────────────────────────────────────
function getIST() {
  // IST = UTC+5:30
  const now = new Date();
  const ist = new Date(now.getTime() + 5.5 * 60 * 60 * 1000);
  return ist;
}
function drishtiDate(d) {
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

function httpsPost(url, body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const u    = new URL(url);
    const opts = {
      hostname: u.hostname, port: 443, path: u.pathname + u.search,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) }
    };
    const req = https.request(opts, res => {
      let buf = '';
      res.on('data', c => buf += c);
      res.on('end', () => {
        try { resolve(JSON.parse(buf)); }
        catch(e) { reject(new Error('JSON parse failed: ' + buf.slice(0,200))); }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function fetchCA() {
  const ist      = getIST();
  const dateStr  = drishtiDate(ist);
  const dispDate = displayDate(ist);

  console.log(`Fetching CA for ${dispDate} (Drishti date: ${dateStr})`);

  const prompt = `You are a current affairs expert for SSC and competitive exam preparation in India.

Today is ${dispDate}.

Search and find today's important current affairs from:
1. Drishti IAS daily news: https://www.drishtiias.com/current-affairs-news-analysis-editorials/news-analysis/${dateStr}
2. Adda247 current affairs: https://currentaffairs.adda247.com/

Based on your knowledge of current events in India around this date, provide 18-22 important current affairs items relevant for SSC CGL, CHSL, and other competitive exams.

Return ONLY a valid JSON object with this exact structure — no markdown, no explanation, no code blocks:

{
  "date": "${dispDate}",
  "dateKey": "${dateStr}",
  "generatedAt": "${new Date().toISOString()}",
  "sources": [
    "https://www.drishtiias.com/current-affairs-news-analysis-editorials/news-analysis/${dateStr}",
    "https://currentaffairs.adda247.com/"
  ],
  "items": [
    {
      "title": "Rephrased headline with key name/place/number included",
      "summary": "2-3 sentences. MUST include: full names of people/organizations, exact dates, specific places, numbers/amounts/ranks. No vague language.",
      "keyPoints": ["Specific fact with name/number", "Specific fact with date/place", "Specific fact with data"],
      "category": "polity|economy|science|intl|environ|society|defence|sports|awards|general",
      "examRelevance": "Which SSC topic/subject this falls under and why it matters",
      "tags": ["tag1", "tag2", "tag3"]
    }
  ]
}

STRICT CONTENT RULES:
- ALWAYS include full proper names — never say "an author", "a minister", "a company" — always use the actual name
- ALWAYS include specific numbers — ranks, amounts, dates, percentages, distances, years
- ALWAYS include place names — cities, states, countries, rivers, mountains
- ALWAYS include the appointing/awarding body name when relevant
- Rephrase all content — do not copy verbatim from source
- If a person won an award: include their full name, award name, category, and who gave it
- If a scheme was launched: include scheme name, ministry, target beneficiaries, budget amount
- If a report/index was released: include rank of India, total countries, publishing organization
- If a sports event: include winner name, venue, opponent, score if available
- Keep language simple and direct — suitable for SSC exam prep
- Include items from all categories: Polity, Economy, Science & Tech, International Affairs, Environment, Society, Defence, Sports, Awards & Rankings
- Each item must have ALL fields filled with specific factual content — no placeholder text`;

  const body = {
    contents: [{ parts: [{ text: prompt }] }],
    generationConfig: {
      temperature: 0.3,
      maxOutputTokens: 8192,
      responseMimeType: 'application/json'
    }
  };

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${GEMINI_KEY}`;

  try {
    const resp = await httpsPost(url, body);

    if (resp.error) throw new Error(resp.error.message);
    if (!resp.candidates || !resp.candidates[0]) throw new Error('No candidates in response');

    const text = resp.candidates[0].content.parts[0].text;
    let parsed;
    try {
      parsed = JSON.parse(text);
    } catch(e) {
      // Try to extract JSON if wrapped
      const m = text.match(/\{[\s\S]*\}/);
      if (!m) throw new Error('No JSON object in response');
      parsed = JSON.parse(m[0]);
    }

    if (!parsed.items || !Array.isArray(parsed.items)) {
      throw new Error('Invalid response structure — no items array');
    }

    // Ensure required fields
    parsed.date        = parsed.date        || dispDate;
    parsed.dateKey     = parsed.dateKey     || dateStr;
    parsed.generatedAt = parsed.generatedAt || new Date().toISOString();
    parsed.sources     = parsed.sources     || [];

    // Write to file
    fs.writeFileSync('current-affairs-data.json', JSON.stringify(parsed, null, 2), 'utf8');
    console.log(`✅ Saved ${parsed.items.length} items to current-affairs-data.json`);
    console.log(`Categories: ${[...new Set(parsed.items.map(i=>i.category))].join(', ')}`);

  } catch(err) {
    console.error('❌ Error:', err.message);

    // Write error state so page can show fallback
    const fallback = {
      date: dispDate,
      dateKey: dateStr,
      generatedAt: new Date().toISOString(),
      error: err.message,
      sources: [
        `https://www.drishtiias.com/current-affairs-news-analysis-editorials/news-analysis/${dateStr}`,
        'https://currentaffairs.adda247.com/'
      ],
      items: []
    };
    fs.writeFileSync('current-affairs-data.json', JSON.stringify(fallback, null, 2), 'utf8');
    process.exit(1);
  }
}

fetchCA();
