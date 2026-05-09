// Renders my pages to PNG using the bundled Chromium.
// Usage: node screenshot.js
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const repo = "/home/user/blisniukamanov";
const outDir = path.join(repo, "_compare");
fs.mkdirSync(outDir, { recursive: true });

const pages = [
  { name: "01-home-desktop",       file: "index.html",        width: 1280, full: true  },
  { name: "02-destinations-desktop", file: "destinations.html", width: 1280, full: true },
  { name: "03-journeys-desktop",   file: "journeys.html",     width: 1280, full: true  },
  { name: "04-home-mobile",        file: "index.html",        width: 414,  full: true  },
];

(async () => {
  const browser = await chromium.launch({
    executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });
  const ctx = await browser.newContext({ deviceScaleFactor: 1 });

  for (const p of pages) {
    const url = "file://" + path.join(repo, p.file);
    const page = await ctx.newPage();
    await page.setViewportSize({ width: p.width, height: 900 });
    console.log("→", p.name, url);
    await page.goto(url, { waitUntil: "networkidle", timeout: 45000 }).catch((e) => {
      console.warn("  networkidle timeout, falling back:", e.message);
    });
    // Force scroll-reveal animations to show + scroll once to trigger lazy bits
    await page.evaluate(() => {
      document.querySelectorAll(".reveal").forEach((el) => el.classList.add("in"));
      window.scrollTo(0, document.body.scrollHeight);
    });
    await page.waitForTimeout(400);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(800);
    const out = path.join(outDir, p.name + ".png");
    await page.screenshot({ path: out, fullPage: p.full });
    console.log("  saved", out);
    await page.close();
  }

  await browser.close();
  console.log("Done.");
})();
