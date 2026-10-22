// Offline Node tests: real controller/validators and bundled KaTeX; DOM fixtures
// exercise the modal and sanitizer. No network, browser or model calls occur.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
function loadBundled(path) {
  const module = { exports: {} };
  vm.runInNewContext(readFileSync(path, 'utf8'), { module, exports: module.exports });
  return module.exports;
}
const moduleSource = readFileSync(new URL('./artifact_access.js', import.meta.url), 'utf8');
const api = await import('data:text/javascript;base64,' + Buffer.from(moduleSource).toString('base64'));
const { artifactIdFromURL, artifactIdFromSearch, normalizeArtifactLinks, validateArtifactMetadata,
  validateArtifactAccess, sanitizeArtifactPreview, artifactPreviewDocument, createArtifactAccessController, mountArtifactAccess } = api;
const ID = '12345678-1234-4234-8234-123456789012', ID2 = '12345678-1234-4234-8234-123456789013';
const A = 'a'.repeat(64), B = 'b'.repeat(64), TOKEN = 'x'.repeat(43), BASE = api.ARTIFACT_ORIGIN;
const NOW = Date.UTC(2026, 9, 1, 12);
const metadata = (id = ID, extra = {}) => ({ id, filename: 'Arquivo.html', kind: 'website', bytes: 42, sha256: 'c'.repeat(64), preview_html: '<h1>Preview</h1>', ...extra });
const access = (id = ID, time = NOW, token = TOKEN) => ({ id, download_url: BASE + '/task-download/' + id + '/' + token,
  preview_url: BASE + '/task-view/' + id + '/' + token, expires_at: (time + 900000) / 1000 });
const response = (value, status = 200) => ({ ok: status >= 200 && status < 300, status, json: async () => value });
const deferred = () => { let resolve; const promise = new Promise((r) => { resolve = r; }); return { promise, resolve }; };
const tick = () => new Promise(setImmediate);
function harness(handler, { search = '', account = A, timeout = 20000 } = {}) {
  let identity = { account, token: '' }, time = NOW, lost = 0;
  const calls = [], states = [];
  const request = async (path, options) => {
    calls.push({ path, options });
    if (handler) return handler(path, options, calls);
    const id = path.split('/')[3];
    return response(path.endsWith('/view') ? metadata(id) : access(id, time));
  };
  const controller = createArtifactAccessController({ request, identity: () => identity,
    render: (state) => states.push(state), onAuthLost: () => lost++, now: () => time, initialSearch: search, requestTimeout: timeout });
  return { controller, calls, states, lost: () => lost, owner: (value, token = '') => { identity = { account: value, token }; }, time: (value) => { time = value; } };
}

test('identifies stable, authenticated and historical ticket links by canonical UUID only', () => {
  for (const value of [BASE + '/api/task-artifacts/' + ID, '/api/task-artifacts/' + ID,
    BASE + '/task-download/' + ID + '/' + TOKEN, '/task-download/' + ID + '/' + TOKEN,
    BASE + '/app/index.html?artifact=' + ID, '/app/index.html?artifact=' + ID.toUpperCase()]) assert.equal(artifactIdFromURL(value), ID);
});

test('rejects hostile origins, credentials, schemes, encoded paths, traversal and malformed tickets', () => {
  const path = '/api/task-artifacts/' + ID;
  for (const value of ['https://evil.example' + path, BASE + '.evil.example' + path, 'http://demo.iald.ia.br' + path,
    'https://user:pass@demo.iald.ia.br' + path, BASE + ':444' + path, '//demo.iald.ia.br' + path,
    BASE + '/x/..' + path, BASE + '/%61pi/task-artifacts/' + ID, BASE + '\\api\\task-artifacts\\' + ID,
    BASE + path + '/more', BASE + path + '?owner=other', BASE + path + '#x', BASE + '/api/task-artifacts/not-a-uuid',
    '/task-download/' + ID + '/' + TOKEN.slice(1), '/task-download/' + ID + '/' + TOKEN + 'x',
    'javascript:alert(1)', '\n' + BASE + path, BASE + '/app/index.html?artifact=' + ID + '&artifact=' + ID2]) {
    assert.equal(artifactIdFromURL(value), null, value);
  }
});

test('launch parameter requires one UUID; no owner or historical token is consumed', () => {
  assert.equal(artifactIdFromSearch('?artifact=' + ID + '&owner=untrusted'), ID);
  for (const value of ['', '?artifact=bad', '?artifact=' + ID + '&artifact=' + ID2]) assert.equal(artifactIdFromSearch(value), null);
});

test('fresh capabilities require matching ID, exact production routes and future expiration', () => {
  const grant = validateArtifactAccess(access(), ID, NOW);
  assert.equal(grant.expires_at, NOW + 900000);
  assert.equal(validateArtifactAccess({ ...access(), expires_at: new Date(NOW + 900000).toISOString() }, ID, NOW).expires_at, grant.expires_at);
  for (const delta of [{ id: ID2 }, { download_url: access(ID2).download_url }, { download_url: access().download_url + '?owner=x' },
    { download_url: access().download_url.replace(BASE, 'https://evil.example') }, { preview_url: access().preview_url.replace('/task-view/', '/task-preview/') },
    { preview_url: access().download_url }, { expires_at: NOW / 1000 }, { expires_at: 'tomorrow' }, { expires_at: '2026-10-01 12:15:00' }]) {
    assert.throws(() => validateArtifactAccess({ ...access(), ...delta }, ID, NOW));
  }
});

test('metadata validates owner-scoped response identity and limits preview to websites', () => {
  for (const delta of [{ id: ID2 }, { filename: '' }, { bytes: -1 }, { sha256: 'wrong' }, { preview_html: 123 }]) {
    assert.throws(() => validateArtifactMetadata(metadata(ID, delta), ID));
  }
  assert.equal(validateArtifactMetadata(metadata(ID, { kind: 'spreadsheet' }), ID).preview_html, null);
  assert.equal(validateArtifactMetadata(metadata(ID, { preview_html: 'a'.repeat(2 * 1024 * 1024 + 1) }), ID).preview_html, null);
});

test('opening only calls authenticated view and POST access with JSON empty body', async () => {
  const h = harness(); await h.controller.open(ID);
  assert.deepEqual(h.calls.map((c) => c.path), ['/api/task-artifacts/' + ID + '/view', '/api/task-artifacts/' + ID + '/access']);
  assert.equal(h.calls[0].options.method, 'GET'); assert.equal(h.calls[1].options.method, 'POST');
  assert.equal(h.calls[1].options.body, '{}'); assert.deepEqual(h.calls[1].options.headers, { 'Content-Type': 'application/json' });
  assert.equal(h.calls[1].options.cache, 'no-store'); assert.equal(h.controller.snapshot().phase, 'ready');
});

test('no artifact API requests occur before authentication; launch opens only once afterward', async () => {
  const h = harness(null, { account: '', search: '?artifact=' + ID });
  await h.controller.authenticated(); assert.equal(h.calls.length, 0);
  h.owner(A); await h.controller.authenticated(); await h.controller.authenticated();
  assert.equal(h.calls.length, 2); assert.equal(h.controller.snapshot().id, ID);
  const manual = harness(null, { account: '' }); await manual.controller.open(ID);
  assert.equal(manual.calls.length, 0); assert.match(manual.controller.snapshot().error, /Entre/);
});

test('close or logout cancels a pending launch before login', async () => {
  for (const method of ['close', 'reset']) {
    const h = harness(null, { account: '', search: '?artifact=' + ID }); h.controller[method]();
    h.owner(A); await h.controller.authenticated(); assert.equal(h.calls.length, 0);
  }
});

test('each fresh modal entry issues a new capability, never uses a historical token', async () => {
  const h = harness(); const id = artifactIdFromURL(BASE + '/task-download/' + ID + '/' + 'h'.repeat(43));
  await h.controller.open(id); h.controller.close(); await h.controller.open(id);
  assert.equal(h.calls.filter((c) => c.path.endsWith('/access')).length, 2);
  assert.ok(h.calls.every((c) => !c.path.includes('h'.repeat(43)) && !c.path.startsWith('/task-download/')));
});

test('expired click prepares one new link and requires another real user click', async () => {
  const refresh = deferred(); let grants = 0;
  const h = harness((path) => response(path.endsWith('/view') ? metadata() : ++grants === 1 ? access() : null));
  await h.controller.open(ID); h.time(NOW + 900000);
  // The renewal itself is asynchronous; neither click may navigate while it runs.
  let prevented = 0; const event = { preventDefault: () => prevented++ };
  assert.equal(h.controller.activate('download', event), false);
  assert.equal(h.controller.activate('download', event), false);
  await tick(); assert.equal(prevented, 2); assert.equal(grants, 2);
  assert.equal(h.controller.snapshot().access, null); // Null/invalid renewal cannot produce a link.
  const valid = harness(); await valid.controller.open(ID); valid.time(NOW + 900001);
  assert.equal(valid.controller.activate('preview', event), false); await tick();
  assert.equal(valid.controller.activate('preview', event), true);
  assert.equal(valid.calls.filter((c) => c.path.endsWith('/access')).length, 2);
});

test('double click shares an in-flight modal request', async () => {
  const pending = deferred();
  const h = harness((path) => path.endsWith('/view') ? pending.promise : response(access()));
  const first = h.controller.open(ID), second = h.controller.open(ID);
  assert.equal(h.calls.length, 1); pending.resolve(response(metadata())); await Promise.all([first, second]);
  assert.equal(h.calls.length, 2);
});

test('closing aborts the request and ignores a late uncooperative response', async () => {
  const pending = deferred(); const h = harness(() => pending.promise);
  const opened = h.controller.open(ID); h.controller.close();
  assert.equal(h.calls[0].options.signal.aborted, true);
  pending.resolve(response(metadata())); await opened;
  assert.equal(h.controller.snapshot().open, false); assert.equal(h.calls.length, 1);
});

test('switching artifacts rejects old responses without clearing the new modal', async () => {
  const old = deferred();
  const h = harness((path) => path.includes(ID + '/view') ? old.promise
    : response(path.endsWith('/view') ? metadata(ID2) : access(ID2)));
  const first = h.controller.open(ID); await h.controller.open(ID2); old.resolve(response(metadata())); await first;
  assert.equal(h.controller.snapshot().id, ID2); assert.equal(h.controller.snapshot().metadata.id, ID2);
  assert.equal(h.calls.filter((c) => c.path.endsWith(ID + '/access')).length, 0);
});

test('account/token changes during response decoding cannot show another account preview or capability', async () => {
  for (const tokenChange of [false, true]) {
    const body = deferred();
    const h = harness(() => ({ ok: true, status: 200, json: () => body.promise }));
    const opened = h.controller.open(ID); await tick();
    h.owner(tokenChange ? A : B, tokenChange ? 'new-session' : ''); body.resolve(metadata()); await opened;
    assert.equal(h.controller.snapshot().open, false); assert.equal(h.calls.length, 1);
  }
});

test('ready links and preview clear on logout or a detected identity change', async () => {
  const h = harness(); await h.controller.open(ID); h.owner(''); h.controller.checkIdentity();
  assert.equal(h.controller.snapshot().open, false); assert.equal(h.controller.snapshot().access, null);
  let prevented = false; assert.equal(h.controller.activate('download', { preventDefault: () => { prevented = true; } }), false);
  assert.equal(prevented, true);
});

for (const status of [401, 403, 404, 500]) {
  test('HTTP ' + status + ' cannot expose preview or actionable links', async () => {
    const h = harness(() => response({ error: '<script>private</script>' }, status)); await h.controller.open(ID);
    assert.equal(h.controller.snapshot().access, null); assert.equal(h.controller.snapshot().metadata, null);
    assert.ok(!h.controller.snapshot().error.includes('<script>'));
    if (status === 401) { assert.equal(h.controller.snapshot().open, false); assert.equal(h.lost(), 1); }
    else assert.equal(h.controller.snapshot().phase, 'error');
  });
}

test('network, malformed JSON, invalid metadata and access errors keep an actionable retry state', async () => {
  for (const handler of [() => { throw new TypeError('Network failed'); },
    () => ({ ok: true, status: 200, json: async () => { throw new Error('bad json'); } }),
    () => response(metadata(ID2))]) {
    const h = harness(handler); await h.controller.open(ID); assert.equal(h.controller.snapshot().phase, 'error');
    assert.equal(h.controller.snapshot().access, null); assert.equal(h.calls.length, 1);
  }
  const h = harness((path) => response(path.endsWith('/view') ? metadata() : { error: 'unavailable' }, path.endsWith('/view') ? 200 : 500));
  await h.controller.open(ID); assert.equal(h.controller.snapshot().metadata.id, ID);
  assert.equal(h.controller.snapshot().access, null); assert.ok(h.controller.snapshot().error);
});

test('request timeout exits loading and permits retry', async () => {
  const h = harness((path, options) => new Promise((resolve, reject) => options.signal.addEventListener('abort', () => reject(new DOMException('abort', 'AbortError')))), { timeout: 5 });
  await h.controller.open(ID); assert.equal(h.controller.snapshot().phase, 'error'); assert.match(h.controller.snapshot().error, /demorou/);
});

// Minimal DOM fixtures model parsed nodes, not a substitute for browser parser QA.
class Element {
  constructor(tag, attrs = {}, children = []) {
    this.localName = tag; this.tagName = tag.toUpperCase(); this.namespaceURI = 'http://www.w3.org/1999/xhtml';
    this.attrs = new Map(Object.entries(attrs)); this.children = []; this.parentNode = null; this.listeners = new Map(); this.hidden = false; this.text = '';
    children.forEach((child) => this.appendChild(child));
  }
  get attributes() { return [...this.attrs].map(([name, value]) => ({ name, value })); }
  getAttribute(name) { return this.attrs.get(name) ?? null; }
  setAttribute(name, value) { this.attrs.set(name, String(value)); }
  hasAttribute(name) { return this.attrs.has(name); }
  removeAttribute(name) { this.attrs.delete(name); }
  get id() { return this.getAttribute('id'); } set id(value) { this.setAttribute('id', value); }
  get className() { return this.getAttribute('class'); } set className(value) { this.setAttribute('class', value); }
  appendChild(child) { this.children.push(child); child.parentNode = this; child.ownerDocument = this.ownerDocument; return child; }
  remove() { if (this.parentNode) this.parentNode.children = this.parentNode.children.filter((c) => c !== this); this.parentNode = null; }
  get isConnected() { return !!this.parentNode; }
  get textContent() { return this.text + this.children.map((c) => c.textContent).join(''); }
  set textContent(value) { this.text = String(value); this.children.forEach((c) => { c.parentNode = null; }); this.children = []; }
  get innerHTML() { return this.children.map((c) => c.serialize()).join(''); }
  serialize() { return '<' + this.localName + [...this.attrs].map(([k, v]) => ' ' + k + '="' + v.replaceAll('"', '&quot;') + '"').join('') + '>' + this.text + this.innerHTML + '</' + this.localName + '>'; }
  querySelectorAll(selector) {
    const all = this.children.flatMap((c) => [c, ...c.querySelectorAll('*')]);
    return selector === '*' ? all : all.filter((n) => selector === 'a[href]' ? n.localName === 'a' && n.hasAttribute('href') : n.localName === selector);
  }
  closest(selector) { if (selector === 'a[href]' && this.localName === 'a' && this.hasAttribute('href')) return this; return this.parentNode?.closest(selector) || null; }
  contains(node) { return node === this || this.querySelectorAll('*').includes(node); }
  addEventListener(name, callback) { this.listeners.set(name, callback); }
  focus() { if (this.ownerDocument) this.ownerDocument.activeElement = this; }
}
function dom() {
  const listeners = new Map(), document = { activeElement: null, templateInputs: [],
    addEventListener: (name, callback) => listeners.set(name, callback),
    createElement(tag) {
      const result = new Element(tag); result.ownerDocument = document;
      if (tag === 'template') {
        result.content = new Element('fragment', {}, [new Element('h1')]); result.content.children[0].textContent = 'Preview';
        Object.defineProperty(result, 'innerHTML', { set: (html) => document.templateInputs.push(html), get: () => result.content.innerHTML });
      }
      return result;
    },
    getElementById(id) { return [document.head, document.body].flatMap((n) => n.querySelectorAll('*')).find((n) => n.id === id) || null; },
  };
  document.head = document.createElement('head'); document.body = document.createElement('body');
  const messages = document.createElement('div'); messages.id = 'conversa-interna'; document.body.appendChild(messages);
  return { document, messages, window: { addEventListener: (name, callback) => listeners.set(name, callback) } };
}
const generated = readFileSync(new URL('./iald.js', import.meta.url), 'utf8');
const baseline = readFileSync(new URL('./iald.base.js', import.meta.url), 'utf8').replaceAll('\r\n', '\n');
const sanitizerStart = '// ── SANEAMENTO (início) ──', sanitizerEnd = '// ── SANEAMENTO (fim) ──';
const sanitizerBlock = (text) => text.slice(text.indexOf(sanitizerStart), text.indexOf(sanitizerEnd));
const styleContext = vm.createContext({ URL }); vm.runInContext(sanitizerBlock(generated), styleContext);
const unsafeStyle = styleContext.estiloPerigoso;

test('preview sanitizer removes executable tags, foreign namespaces, navigation and remote loaders', () => {
  const svg = new Element('svg'); svg.namespaceURI = 'http://www.w3.org/2000/svg';
  const unsafe = ['script', 'iframe', 'object', 'embed', 'form', 'meta', 'base', 'link', 'template', 'input', 'noscript'].map((tag) => new Element(tag));
  const anchor = new Element('a', { href: 'https://evil.example/', target: '_top', ping: 'https://evil.example', onclick: 'alert(1)' });
  const image = new Element('img', { src: 'https://evil.example', srcset: 'evil 1x', onerror: 'alert(1)' });
  const raster = new Element('img', { src: 'data:image/png;base64,AA==' });
  const vector = new Element('img', { src: 'data:image/svg+xml;base64,AA==' });
  const span = new Element('span', { 'xlink:href': 'javascript:alert(1)', style: 'color:red', title: 'Plain text' });
  const style = new Element('style'); style.textContent = 'body { color: red }';
  const cssAttack = new Element('style'); cssAttack.textContent = String.raw`@\69mport 'https://evil.example/x';`;
  const root = new Element('fragment', {}, [...unsafe, svg, anchor, image, raster, vector, span, style, cssAttack]);
  sanitizeArtifactPreview(root, unsafeStyle);
  assert.equal(root.querySelectorAll('script').length, 0); assert.equal(root.children.includes(svg), false);
  unsafe.forEach((node) => assert.equal(root.children.includes(node), false));
  assert.equal(anchor.attributes.length, 0); assert.equal(image.attributes.length, 0);
  assert.equal(raster.getAttribute('src'), 'data:image/png;base64,AA=='); assert.equal(vector.getAttribute('src'), null);
  assert.equal(span.getAttribute('xlink:href'), null); assert.equal(span.getAttribute('style'), 'color:red');
  assert.equal(root.children.includes(style), true); assert.equal(root.children.includes(cssAttack), false);
});

test('preview document places restrictive CSP before sanitized content', () => {
  const { document } = dom(); const html = '<h1>Original preview</h1>';
  const srcdoc = artifactPreviewDocument(html, document, unsafeStyle);
  assert.equal(document.templateInputs[0], html);
  assert.ok(srcdoc.indexOf('Content-Security-Policy') < srcdoc.indexOf('<body>'));
  for (const directive of ["default-src 'none'", "style-src 'unsafe-inline'", 'img-src data:', "base-uri 'none'", "form-action 'none'"]) assert.ok(srcdoc.includes(directive));
  assert.ok(!srcdoc.includes('allow-scripts')); assert.ok(!srcdoc.includes('allow-same-origin'));
});

test('render-only normalization removes historical token without replacing formula nodes or stored text', () => {
  const raw = BASE + '/task-download/' + ID + '/' + TOKEN;
  const formula = new Element('span', { class: 'katex' }), anchor = new Element('a', { href: raw }, [formula]);
  const root = new Element('div', {}, [anchor]), history = { content: '[Arquivo](' + raw + ')' };
  normalizeArtifactLinks(root);
  assert.equal(anchor.getAttribute('href'), BASE + '/app/index.html?artifact=' + ID);
  assert.equal(anchor.children[0], formula); assert.equal(history.content, '[Arquivo](' + raw + ')');
});

test('modal intercepts message click, builds empty sandbox and fresh touchable anchors, clears on close', async () => {
  const d = dom(), calls = [];
  const controller = mountArtifactAccess({ ...d, identity: () => ({ account: A, token: '' }), unsafeStyle,
    request: async (path, options) => { calls.push({ path, options }); return response(path.endsWith('/view') ? metadata() : access(ID, Date.now())); } });
  const anchor = new Element('a', { href: '/task-download/' + ID + '/' + 'h'.repeat(43) }); d.messages.appendChild(anchor);
  const event = { target: anchor, prevented: false, preventDefault() { this.prevented = true; }, stopPropagation() {} };
  d.messages.listeners.get('click')(event); await tick();
  assert.equal(event.prevented, true); assert.equal(calls.length, 2);
  const frame = d.document.body.querySelectorAll('iframe')[0];
  assert.equal(frame.getAttribute('sandbox'), ''); assert.equal(frame.getAttribute('src'), null);
  assert.equal(frame.getAttribute('allow-scripts'), null); assert.equal(frame.getAttribute('allow-same-origin'), null);
  assert.match(frame.getAttribute('srcdoc'), /Content-Security-Policy/);
  const links = d.document.body.querySelectorAll('a[href]').filter((a) => a !== anchor);
  assert.equal(links.length, 2); assert.equal(links[0].target, '_blank'); assert.equal(links[0].rel, 'noopener noreferrer');
  controller.close(); assert.equal(frame.getAttribute('srcdoc'), null);
  links.forEach((link) => assert.equal(link.getAttribute('href'), null));
});

test('metadata-only files create no iframe and unrelated message links are untouched', async () => {
  const d = dom(); let count = 0;
  const controller = mountArtifactAccess({ ...d, identity: () => ({ account: A }), unsafeStyle,
    request: async (path) => { count++; return response(path.endsWith('/view') ? metadata(ID, { kind: 'spreadsheet', preview_html: null }) : { ...access(ID, Date.now()), preview_url: null }); } });
  const anchor = new Element('a', { href: 'https://example.org/article' }); d.messages.appendChild(anchor);
  d.messages.listeners.get('click')({ target: anchor, preventDefault() { assert.fail('Unrelated link intercepted'); } });
  assert.equal(count, 0); await controller.open(ID);
  assert.equal(d.document.body.querySelectorAll('iframe').length, 0);
  assert.equal(d.document.body.querySelectorAll('a[href]').length, 2); // Ordinary link plus download.
});

test('generated source preserves sanitizer and renders formulas with actual bundled marked/KaTeX', () => {
  assert.equal(sanitizerBlock(generated), sanitizerBlock(baseline));
  const mathBlock = (text) => text.slice(text.indexOf('function protectMath('), text.indexOf('function renderMarkdown('));
  assert.equal(mathBlock(generated), mathBlock(baseline));
  const protect = vm.runInNewContext(mathBlock(generated) + '\nprotectMath');
  const marked = loadBundled('C:/IALD/projetos_pyhton/IALD/app/vendor/marked.min.js');
  const katex = loadBundled('C:/IALD/projetos_pyhton/IALD/app/vendor/katex/katex.min.js');
  const input = String.raw`\[2+2=4\]` + '\n[Arquivo](' + BASE + '/app/index.html?artifact=' + ID + ')';
  const result = protect(input);
  const rendered = marked.parse(result.text).replace(result.pattern, (_, i) => katex.renderToString(result.formulas[+i].eq, { displayMode: result.formulas[+i].bloco, throwOnError: true, trust: false, output: 'html' }));
  assert.match(rendered, /class="katex"/); assert.doesNotMatch(rendered, /katex-error/);
  assert.ok(rendered.includes('/app/index.html?artifact=' + ID));
});

for (const surface of ['web', 'app']) {
  test('generated authenticated adapter preserves ' + surface + ' credentials and browser-managed Origin', async () => {
    const start = generated.indexOf('async function fetchIALD('), end = generated.indexOf('\n}', start) + 2;
    let sent;
    const context = vm.createContext({ SUPERFICIE: surface, BASE: surface === 'app' ? BASE : '', tokenApp: () => surface === 'app' ? 'test-only-session' : '',
      fetch: async (path, options) => { sent = { path, options }; return { status: 200 }; } });
    vm.runInContext(generated.slice(start, end), context);
    await context.fetchIALD('/api/task-artifacts/' + ID + '/access', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
    assert.equal(sent.options.credentials, surface === 'app' ? 'omit' : 'same-origin');
    assert.equal(sent.options.headers.Authorization, surface === 'app' ? 'Bearer test-only-session' : undefined);
    assert.equal(sent.options.headers.Origin, undefined);
  });
}


test('generated login hook opens only after authenticated account response', async () => {
  let opened = 0;
  const start = generated.indexOf('async function identificarContaBackground(');
  const end = generated.indexOf('function corpoPedidoBackground(', start);
  const context = vm.createContext({ DEMO: false, portaoNecessario: () => false, backgroundEpoch: 1,
    backgroundOwner: A, tokenApp: () => '', AbortSignal, refreshNativeNotificationsUI() {},
    artifactAccessUI: { authenticated() { opened++; } },
    fetchIALD: async (path) => { assert.equal(opened, 0); assert.equal(path, '/api/chat-jobs/session'); return response({ account: A }); } });
  vm.runInContext(generated.slice(start, end), context);
  await context.identificarContaBackground();
  assert.equal(opened, 1);
});

test('generated logout hook clears modal and pending launch, ordinary background pause does not', () => {
  let cleared = 0;
  const start = generated.indexOf('function desanexarRespostasBackground(');
  const end = generated.indexOf('async function identificarContaBackground(', start);
  const context = vm.createContext({ artifactAccessUI: { reset() { cleared++; } }, disconnectNativeNotificationsUI() {},
    backgroundEpoch: 0, backgroundTimer: null, clearTimeout() {}, backgroundJobs: { pause() {}, setOwner() {} },
    backgroundOwner: A, activeBackgroundJob: null, S: { aborto: null }, $: () => null });
  vm.runInContext(generated.slice(start, end), context);
  context.desanexarRespostasBackground(false); assert.equal(cleared, 0);
  context.desanexarRespostasBackground(true); assert.equal(cleared, 1);
});


test('preview-only responsive rules follow source styles and viewport belongs to generated head', () => {
  const { document } = dom();
  const create = document.createElement;
  document.createElement = (tag) => {
    const element = create(tag);
    if (tag === 'template') {
      const style = new Element('style'); style.textContent = 'h1{font-size:36px}';
      const heading = new Element('h1'); heading.textContent = 'Luminodinâmica';
      element.content = new Element('fragment', {}, [style, heading]);
    }
    return element;
  };
  const original = '<style>h1{font-size:36px}</style><h1>Luminodinâmica</h1>';
  const record = metadata(ID, { preview_html: original });
  const srcdoc = artifactPreviewDocument(record.preview_html, document, unsafeStyle);
  assert.equal(record.preview_html, original);
  assert.ok(srcdoc.indexOf('name="viewport"') < srcdoc.indexOf('</head>'));
  assert.ok(srcdoc.includes('content="width=device-width, initial-scale=1"'));
  assert.ok(srcdoc.indexOf(':root{overflow-wrap:anywhere}') > srcdoc.indexOf('h1{font-size:36px}'));
  assert.ok(srcdoc.includes('*,*::before,*::after{box-sizing:border-box}'));
  assert.ok(srcdoc.includes('h1,h2,h3,h4,h5,h6,img,pre{max-width:100%}'));
  assert.ok(srcdoc.includes('pre{white-space:pre-wrap;overflow-wrap:anywhere}'));
});
