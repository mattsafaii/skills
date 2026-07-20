// Fetch Google Search Console data for a property using a service account.
// Outputs one JSON object on stdout:
//   {
//     property, window: {start, end}, prev_window: {start, end} | null,
//     totals: {clicks, impressions, ctr, position},
//     prev_totals: {...} | null,
//     top_queries: [{query, clicks, impressions, position}],
//     top_pages: [{page, clicks, impressions, position}],
//     inspections: [{url, verdict, coverage_state, last_crawl, error?}]
//   }
//
// Usage:
//   node gsc-fetch.mjs --key <service-account.json> --property <sc-domain:example.com|https://example.com/> \
//     --start YYYY-MM-DD --end YYYY-MM-DD [--prev-start YYYY-MM-DD --prev-end YYYY-MM-DD] \
//     [--inspect "https://example.com/,https://example.com/about"]

import { readFileSync } from "node:fs";
import { JWT } from "google-auth-library";

function arg(name) {
  const i = process.argv.indexOf(`--${name}`);
  return i === -1 ? undefined : process.argv[i + 1];
}

const keyPath = arg("key");
const property = arg("property");
const start = arg("start");
const end = arg("end");
const prevStart = arg("prev-start");
const prevEnd = arg("prev-end");
const inspect = (arg("inspect") ?? "").split(",").map((s) => s.trim()).filter(Boolean);

if (!keyPath || !property || !start || !end) {
  console.error("required: --key --property --start --end");
  process.exit(2);
}

const key = JSON.parse(readFileSync(keyPath.replace(/^~/, process.env.HOME), "utf8"));
const client = new JWT({
  email: key.client_email,
  key: key.private_key,
  scopes: ["https://www.googleapis.com/auth/webmasters.readonly"],
});

const API = "https://searchconsole.googleapis.com";
const encProp = encodeURIComponent(property);

async function post(path, body) {
  const res = await client.request({
    url: `${API}${path}`,
    method: "POST",
    data: body,
  });
  return res.data;
}

async function analytics(startDate, endDate, dimensions, rowLimit = 10) {
  const data = await post(`/webmasters/v3/sites/${encProp}/searchAnalytics/query`, {
    startDate,
    endDate,
    dimensions,
    rowLimit,
  });
  return data.rows ?? [];
}

async function totalsFor(startDate, endDate) {
  const rows = await analytics(startDate, endDate, [], 1);
  const r = rows[0];
  return r
    ? { clicks: r.clicks, impressions: r.impressions, ctr: r.ctr, position: r.position }
    : { clicks: 0, impressions: 0, ctr: 0, position: null };
}

async function inspection(url) {
  try {
    const data = await post(`/v1/urlInspection/index:inspect`, {
      inspectionUrl: url,
      siteUrl: property,
    });
    const r = data.inspectionResult?.indexStatusResult ?? {};
    return {
      url,
      verdict: r.verdict ?? "UNKNOWN",
      coverage_state: r.coverageState ?? null,
      last_crawl: r.lastCrawlTime ?? null,
    };
  } catch (e) {
    return { url, verdict: "ERROR", coverage_state: null, last_crawl: null, error: String(e.message ?? e) };
  }
}

const out = {
  property,
  window: { start, end },
  prev_window: prevStart && prevEnd ? { start: prevStart, end: prevEnd } : null,
  totals: await totalsFor(start, end),
  prev_totals: prevStart && prevEnd ? await totalsFor(prevStart, prevEnd) : null,
  top_queries: (await analytics(start, end, ["query"])).map((r) => ({
    query: r.keys[0],
    clicks: r.clicks,
    impressions: r.impressions,
    position: r.position,
  })),
  top_pages: (await analytics(start, end, ["page"])).map((r) => ({
    page: r.keys[0],
    clicks: r.clicks,
    impressions: r.impressions,
    position: r.position,
  })),
  inspections: [],
};

for (const url of inspect.slice(0, 10)) {
  out.inspections.push(await inspection(url));
}

console.log(JSON.stringify(out, null, 2));
