const { chromium } = require('playwright');
const [,, inFile, outFile] = process.argv;
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + inFile, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: outFile, format: 'Letter', printBackground: true, preferCSSPageSize: true,
                   margin: { top: 0, bottom: 0, left: 0, right: 0 } });
  await browser.close();
  console.log('pdf written', outFile);
})().catch(e => { console.error(e); process.exit(1); });
