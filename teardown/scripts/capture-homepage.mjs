// Usage: node capture-homepage.mjs <url> <desktop-png-path> <mobile-png-path>
// Prints { title, metaDescription, text } as JSON to stdout.
import { chromium } from "playwright";

const [, , url, desktopPath, mobilePath] = process.argv;
if (!url || !desktopPath || !mobilePath) {
  console.error("Usage: node capture-homepage.mjs <url> <desktop-png-path> <mobile-png-path>");
  process.exit(1);
}

const browser = await chromium.launch();

const desktopPage = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await desktopPage.goto(url, { waitUntil: "networkidle", timeout: 30000 });
await desktopPage.screenshot({ path: desktopPath, fullPage: true });

const content = await desktopPage.evaluate(() => ({
  title: document.title,
  metaDescription: document.querySelector('meta[name="description"]')?.content ?? null,
  text: document.body.innerText,
}));

const mobilePage = await browser.newPage({ viewport: { width: 390, height: 844 } });
await mobilePage.goto(url, { waitUntil: "networkidle", timeout: 30000 });
await mobilePage.screenshot({ path: mobilePath, fullPage: true });

await browser.close();

console.log(JSON.stringify(content));
