const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const MEMOS_DIR = path.resolve(__dirname, '../pages/memos');
const OUTPUT_DIR = path.resolve(__dirname, '../dist_pdf');

// List of the 12 main countries from the index.html homepage
const MAIN_COUNTRIES = [
    'egypt.html',
    'maldives.html',
    'turkey.html',
    'vietnam.html',
    'china.html',
    'mauritius.html',
    'thailand.html',
    'seychelles.html',
    'indonesia.html',
    'sri-lanka.html',
    'tanzania.html',
    'tunisia.html'
];

if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

(async () => {
  console.log('--- Emoji Tours PDF Generator (12 main countries) ---');
  
  let browser;
  try {
    browser = await chromium.launch();
    const page = await browser.newPage();

    // Filter to only include the main countries
    const files = fs.readdirSync(MEMOS_DIR).filter(f => MAIN_COUNTRIES.includes(f.toLowerCase()));

    console.log(`Processing ${files.length} documents...`);

    for (const file of files) {
      // Normalize naming (e.g. sri-lanka.html -> Memo_SriLanka.pdf)
      const baseName = file.replace('.html', '').replace('-', '_');
      const parts = baseName.split('_');
      const prettyName = parts.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join('');
      
      const filePath = `file://${path.join(MEMOS_DIR, file)}`;
      const outputPath = path.join(OUTPUT_DIR, `Memo_${prettyName}.pdf`);

      console.log(`[Processing] ${prettyName}...`);
      
      try {
        await page.goto(filePath, { waitUntil: 'networkidle', timeout: 45000 });
        await page.waitForTimeout(2000);

        await page.pdf({
          path: outputPath,
          format: 'A4',
          printBackground: true,
          margin: { top: '0', bottom: '0', left: '0', right: '0' }
        });
        
        console.log(`  ✓ Generated: Memo_${prettyName}.pdf`);
      } catch (err) {
        console.error(`  ✕ Error in ${file}:`, err.message);
      }
    }

    console.log('Finished.');

  } catch (error) {
    console.error('Critical Error:', error);
  } finally {
    if (browser) await browser.close();
  }
})();
