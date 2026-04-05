const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Читаем чистые HTML, подготовленные build_pdf.py
const MEMOS_DIR = path.resolve(__dirname, '../tmp/pdf_ready/memos');
const OUTPUT_DIR = path.resolve(__dirname, '../dist_pdf');

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
  console.log('--- Туроператора PDF Generator ---');

  let browser;
  try {
    browser = await chromium.launch();
    const page = await browser.newPage();

    const files = fs.readdirSync(MEMOS_DIR).filter(f => MAIN_COUNTRIES.includes(f.toLowerCase()));
    console.log(`Генерируем ${files.length} PDF...`);

    for (const file of files) {
      const baseName = file.replace('.html', '').replace(/-/g, '_');
      const parts = baseName.split('_');
      const prettyName = parts.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join('');

      const filePath = `file://${path.join(MEMOS_DIR, file)}`;
      const outputPath = path.join(OUTPUT_DIR, `Memo_${prettyName}.pdf`);

      console.log(`  [→] ${prettyName}...`);
      try {
        await page.goto(filePath, { waitUntil: 'networkidle', timeout: 45000 });
        await page.waitForTimeout(1000);

        await page.pdf({
          path: outputPath,
          format: 'A4',
          printBackground: true,
          margin: { top: '15mm', bottom: '30mm', left: '15mm', right: '15mm' }
        });

        console.log(`  ✓ Memo_${prettyName}.pdf`);
      } catch (err) {
        console.error(`  ✕ Ошибка в ${file}:`, err.message);
      }
    }

    console.log('\nГотово.');
  } catch (error) {
    console.error('Критическая ошибка:', error);
  } finally {
    if (browser) await browser.close();
  }
})();
