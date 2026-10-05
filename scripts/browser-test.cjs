const { chromium } = require('playwright');
const fs = require('node:fs');
const { sessionCount, testUrl, isPageView } = require('./browser-test-config.cjs');
const sessions = sessionCount(process.env.TEST_SESSIONS || '3');
const report = {
  run: process.env.GITHUB_RUN_ID || `local-${Date.now()}`,
  synthetic: true, sessionsRequested: sessions, sessionsCompleted: 0,
  pageLoads: 0, collectionResponses: 0, ga4ReportedViews: null,
  note: 'Collection responses do not prove GA4 reported views or active users.',
  visits: [], failures: [], startedAt: new Date().toISOString()
};
(async () => {
  fs.mkdirSync('test-results', { recursive: true });
  const browser = await chromium.launch({ headless: true });
  try {
    for (let i = 0; i < sessions; i++) {
      const context = await browser.newContext();
      try {
        const page = await context.newPage();
        for (const path of ['/', '/articles/chinese-labor-transcontinental-railroad.html', '/articles/chinese-labor-transcontinental-railroad-citations.html']) {
          const visit = { session: i + 1, path, collected: false };
          const collected = page.waitForResponse(r => isPageView(r.url(), r.request().postData()), { timeout: 15000 })
            .then(r => r.ok()).catch(() => false);
          try {
            const response = await page.goto(testUrl(path, `${report.run}-${i + 1}`), { waitUntil: 'load', timeout: 30000 });
            if (!response || !response.ok()) throw new Error(`Page failed: ${path}`);
            report.pageLoads++;
            await page.locator('h1').waitFor({ state: 'visible' });
            // Check reading/navigation UI, without concealing automation or spoofing identity.
            await page.keyboard.press('PageDown');
            await page.waitForTimeout(3000);
            visit.collected = await collected;
            if (visit.collected) report.collectionResponses++;
            else report.failures.push(`No collection response: session ${i + 1}, ${path}`);
          } finally {
            await collected;
            report.visits.push(visit);
          }
        }
        await page.screenshot({ path: `test-results/session-${i + 1}.png` });
        report.sessionsCompleted++;
      } catch (error) {
        report.failures.push(error.message);
      } finally { await context.close(); }
      if (report.failures.length) break;
    }
  } finally {
    await browser.close();
    report.finishedAt = new Date().toISOString();
    fs.writeFileSync('test-results/report.json', JSON.stringify(report, null, 2));
    console.log(JSON.stringify(report, null, 2));
  }
  if (report.failures.length) process.exitCode = 1;
})().catch(error => { console.error(error); process.exitCode = 1; });
