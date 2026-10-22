import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = fs.readFileSync(path.join(root, 'app/iald.js'), 'utf8');
const fn = source.slice(source.indexOf('function protectMath('), source.indexOf('function renderMarkdown('));
const protect = vm.runInNewContext(fn + '\nprotectMath');
const require = createRequire(import.meta.url);
const marked = require(path.join(root, 'app/vendor/marked.min.js'));
const katex = require(path.join(root, 'app/vendor/katex/katex.min.js'));
const formula = String.raw`\[
\text{hipóteses}\rightarrow\text{prova formal}\rightarrow\text{construção concreta}
\]`;
let checks = 0;
function check(text, expected) {
  const result = protect(text);
  assert.equal(result.formulas.length, expected, text);
  const html = marked.parse(result.text).replace(result.pattern, (_, i) =>
    katex.renderToString(result.formulas[+i].eq, { displayMode: result.formulas[+i].bloco, throwOnError: true, trust: false, output: 'html' }));
  assert.equal((html.match(/class="katex"/g) || []).length, expected);
  checks++;
  return html;
}
assert.match(check(formula, 1), /katex-display/);
check(String.raw`O custo \(\beta=\alpha\sqrt e\), $x_i^2$ e $$H\ge E_0 I$$.`, 3);
check('`$x$` e `\\(x\\)`; exemplo:\n```tex\n\\[x\\]\n$$y$$\n```\n\\(z\\)', 1);
check('~~~tex\n$$x$$\n~~~\n$y$', 1);
check('```tex\n$$x$$\n', 0);
check(String.raw`Preço: R$10 e R$20; escapado \$30.`, 0);
check(String.raw`\[x`, 0);
check('IALDPROTECTEDMATH0END $x$', 1);
const unsafe = protect(String.raw`\(\href{javascript:alert(1)}{x}\)`);
const blocked = katex.renderToString(unsafe.formulas[0].eq, { trust: false, throwOnError: false, output: 'html' });
assert.doesNotMatch(blocked, /href="javascript:/);
checks++;
console.log(JSON.stringify({ checks, status: 'PASS', engine: 'actual bundled marked + KaTeX', display_formula: true }));
