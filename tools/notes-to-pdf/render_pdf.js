// Print HTML files to PDF with Chromium. Usage: node render_pdf.js jobs.json
// jobs.json: [{"html": "/abs/in.html", "pdf": "/abs/out.pdf"}, ...]
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  for (const job of jobs) {
    const page = await browser.newPage();
    await page.goto('file://' + job.html, { waitUntil: 'load', timeout: 0 });
    await page.evaluate(async () => {
      await document.fonts.ready;
      await Promise.all([...document.images].map(i => i.decode().catch(() => null)));
    });
    await page.pdf({ path: job.pdf, preferCSSPageSize: true, printBackground: true,
                     outline: false, tagged: true, timeout: 0 });  // bookmarks are added by build.py
    await page.close();
    console.log('pdf', job.pdf);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
