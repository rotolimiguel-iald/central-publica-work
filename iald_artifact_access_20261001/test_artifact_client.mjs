// Offline extraction of the current production sanitizer and request adapter.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
const source = readFileSync('C:/IALD/projetos_pyhton/IALD/app/iald.js', 'utf8');
const start = source.indexOf('// ── SANEAMENTO (início)');
const end = source.indexOf('// ── SANEAMENTO (fim)', start);
assert(start >= 0 && end > start);
const sanitize = vm.createContext({ URL });
vm.runInContext(source.slice(start, end), sanitize);
class Anchor {
  localName = 'a'; values = new Map();
  constructor(href) { this.values.set('href', href); }
  get attributes() { return [...this.values].map(([name, value]) => ({ name, value })); }
  setAttribute(k, v) { this.values.set(k, v); }
  getAttribute(k) { return this.values.get(k) ?? null; }
  removeAttribute(k) { this.values.delete(k); }
  remove() { throw Error('Valid artifact link unexpectedly removed'); }
}
test('artifact link stays a plain target blank link without an authenticated click action', () => {
  const href = 'https://demo.iald.ia.br/api/task-artifacts/12345678-1234-4234-8234-123456789012';
  const a = new Anchor(href);
  sanitize.sanear({ querySelectorAll: () => [a] });
  assert.equal(a.getAttribute('href'), href);
  assert.equal(a.getAttribute('target'), '_blank');
  assert.equal(a.getAttribute('rel'), 'noopener noreferrer');
  assert.equal(source.includes('/api/task-artifacts/'), false);
  assert.equal(source.includes('/task-download/'), false);
});
test('ordinary relative artifact URL resolves to the native local origin', () => {
  assert.equal(new URL('/api/task-artifacts/id', 'capacitor://localhost/app/index.html').origin, 'null');
  assert.equal(new URL('/api/task-artifacts/id', 'https://localhost/app/index.html').host, 'localhost');
});
const fnStart = source.indexOf('async function fetchIALD(');
const fnEnd = source.indexOf('\n}', fnStart) + 2;
assert(fnStart >= 0 && fnEnd > fnStart);
for (const surface of ['app', 'web']) {
  test(`request adapter supplies correct authentication for ${surface}`, async () => {
    let sent;
    const context = vm.createContext({ SUPERFICIE: surface, BASE: surface === 'app' ? 'https://demo.iald.ia.br' : '',
      tokenApp: () => surface === 'app' ? 'synthetic-token' : '',
      fetch: async (url, options) => { sent = { url, options }; return { status: 200 }; } });
    vm.runInContext(source.slice(fnStart, fnEnd), context);
    await context.fetchIALD('/api/task-artifacts/synthetic-id');
    assert.equal(sent.options.credentials, surface === 'app' ? 'omit' : 'same-origin');
    assert.equal(sent.options.headers.Authorization, surface === 'app' ? 'Bearer synthetic-token' : undefined);
  });
}
