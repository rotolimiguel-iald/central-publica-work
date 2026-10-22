import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = resolve(fileURLToPath(new URL('..', import.meta.url)));
const config = JSON.parse(readFileSync(join(root, 'capacitor.config.json'), 'utf8'));
function check(ok, message) { if (!ok) throw new Error(message); }
check(config.appId === 'br.ia.IALD', 'Unexpected bundle identifier');
check(!config.server?.url, 'Release must use embedded assets');
const web = join(root, config.webDir);
for (const name of ['index.html', 'iald.js', 'iald.css', 'kernel_prompt.js', 'kernel_prompt_loja.js', 'icon.png',
  'img/iald_logo_header.png', 'img/iald_logo_transparent_final.png', 'img/iald_logo_dark_transparent_final.png',
  'vendor/marked.min.js', 'vendor/katex/katex.min.js', 'vendor/katex/katex.min.css']) {
  check(existsSync(join(web, name)), `Missing embedded asset: ${name}`);
}

// 13/09/2026: build 4.1 (13) shipped with the logo pointing at "/iald_logo_header.png",
// a root-absolute path that does not exist inside the app bundle (the image failed
// silently). Every local src/href must be relative AND present in the webDir.
const html = readFileSync(join(web, 'index.html'), 'utf8');
const js = readFileSync(join(web, 'iald.js'), 'utf8');
const refs = new Set();
for (const m of html.matchAll(/(?:src|href)="([^"#?]+)"/g)) refs.add(m[1]);
for (const m of js.matchAll(/['"](\.\/(?:img|vendor)\/[^'"]+)['"]/g)) refs.add(m[1]);
for (const ref of refs) {
  if (/^(https?:|mailto:|data:)/.test(ref)) continue;
  check(!ref.startsWith('/'), `Root-absolute asset path is not bundled: ${ref}`);
  check(existsSync(join(web, ref.replace(/^\.\//, ''))), `Referenced asset missing from ${config.webDir}: ${ref}`);
}
const katexCss = readFileSync(join(web, 'vendor/katex/katex.min.css'), 'utf8');
for (const m of katexCss.matchAll(/url\((fonts\/KaTeX_[A-Za-z0-9_-]+\.woff2)\)/g)) {
  check(existsSync(join(web, 'vendor/katex', m[1])), `KaTeX font missing: ${m[1]}`);
}

const blocked = [/Licenciamento:/i, /Sovereign/i, /Efficiency 1\.2/i, /ROI R\$/i,
  /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/, /\bAIza[0-9A-Za-z_-]{30,}/,
  /\bgh[pousr]_[0-9A-Za-z]{20,}/];
function scan(dir) {
  for (const item of readdirSync(dir, { withFileTypes: true })) {
    const path = join(dir, item.name);
    if (item.isDirectory()) scan(path);
    else if (/\.(js|html|css|json)$/.test(item.name)) {
      const text = readFileSync(path, 'utf8');
      check(!blocked.some(pattern => pattern.test(text)), `Restricted content in ${path}`);
    }
  }
}
scan(web);
console.log(`Release validation passed: embedded assets (${refs.size} local refs), app ID and content guard.`);
