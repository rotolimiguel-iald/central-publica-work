// Offline tests. The request boundary is always a mock; no provider is called.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { webcrypto } from 'node:crypto';

const source = readFileSync(new URL('./chat_jobs.js', import.meta.url), 'utf8');
const { createDurableChatJobs, applyChatJobDelivery } = await import('data:text/javascript;base64,' + Buffer.from(source).toString('base64'));
const A = 'a'.repeat(64), B = 'b'.repeat(64);
const ID = '12345678-1234-4234-8234-123456789012';
const ID2 = '12345678-1234-4234-8234-123456789013';
const body = () => ({ model: 'qwen3', messages: [{ role: 'user', content: 'Pergunta' }],
  stream: true, iald_conv: 'c_test', iald_mode: 'think', iald_surface: 'app', iald_selo_prev: 'c'.repeat(64) });
const response = (data, status = 200) => ({ ok: status >= 200 && status < 300, status, json: async () => data });
const job = (status = 'running', extra = {}) => ({ id: ID, status, conversation_id: 'c_test', ...extra });
const event = (seq, data) => ({ seq, data: typeof data === 'string' ? data : JSON.stringify(data) });
const delta = (text) => ({ choices: [{ delta: { content: text } }] });
const page = (status, events, extra = {}) => job(status, { events, cursor: events.at(-1)?.seq || 0, has_more: false, ...extra });
const donePage = () => page('completed', [event(1, delta('Resposta')), event(2, '[DONE]')]);
const collect = async (iterator) => { const lines = []; for await (const line of iterator) lines.push(line); return lines; };
class Storage {
  values = new Map(); fail = false;
  getItem(key) { return this.values.get(key) ?? null; }
  setItem(key, value) { if (this.fail) throw new Error('Quota'); this.values.set(key, String(value)); }
  removeItem(key) { this.values.delete(key); }
}
function setup(handler = () => response(donePage()), options = {}) {
  const storage = options.storage || new Storage(), calls = [], sleeps = [];
  let account = A;
  const request = async (path, opts = {}) => {
    calls.push({ path, opts });
    if (path.endsWith('/session')) return response({ account });
    if (path === '/api/chat-jobs' && opts.method === 'POST') return response(job(), 202);
    if (path.endsWith('/ack')) return response({ ok: true });
    return handler(path, opts);
  };
  const client = createDurableChatJobs({ request, storage, randomUUID: () => ID,
    sleep: async (ms) => { sleeps.push(ms); }, ...options });
  client.setOwner(A);
  return { client, storage, calls, sleeps, changeAccount: (value) => { account = value; } };
}

test('persists immutable UUID, authenticated account and legacy body before submit', async () => {
  const storage = new Storage(); let submitted;
  const h = setup(null, { storage, request: async (path, opts) => {
    if (path.endsWith('/session')) return response({ account: A });
    if (opts.method === 'POST') {
      submitted = JSON.parse(opts.body);
      const stored = JSON.parse(storage.getItem('iald_chat_jobs_v1:' + A))[0];
      assert.equal(stored.attempted, true); assert.deepEqual(stored.payload, submitted);
      return response(job(), 202);
    }
    return response(donePage());
  } });
  const payload = body(), r = await h.client.begin(payload);
  payload.messages[0].content = 'Changed later';
  await collect(h.client.stream(r));
  assert.deepEqual(submitted, { ...body(), request_id: ID, account: A });
});

test('storage failure prevents POST', async () => {
  const h = setup(); h.storage.fail = true;
  await assert.rejects(h.client.begin(body()), /Sem espaço/);
  assert.equal(h.calls.filter((c) => c.opts.method === 'POST').length, 0);
});

test('lost submit response restarts with the same persisted request and body', async () => {
  const storage = new Storage(), posts = [];
  const request = async (path, opts) => {
    if (path.endsWith('/session')) return response({ account: A });
    if (opts.method === 'POST') {
      posts.push(opts.body);
      if (posts.length === 1) throw new Error('Response lost');
      return response(job(), 202);
    }
    return response(donePage());
  };
  const first = setup(null, { storage, request });
  await assert.rejects(collect(first.client.stream(await first.client.begin(body()))), { pending: true });
  const restart = setup(null, { storage, request, randomUUID: () => { throw new Error('Must not generate another ID'); } });
  await collect(restart.client.stream(restart.client.pending()[0]));
  assert.equal(posts.length, 2); assert.equal(posts[0], posts[1]);
});

test('another pending request cannot allocate a new request in the same conversation', async () => {
  const h = setup(); await h.client.begin(body());
  await assert.rejects(h.client.begin(body()), /já tem uma resposta pendente/);
  assert.equal(h.client.pending().length, 1);
});

test('drains has_more, waits after DONE while running, emits DONE only at terminal', async () => {
  const pages = [page('running', [event(1, delta('A'))], { has_more: true }),
    page('running', [event(2, '[DONE]')]), page('completed', [], { cursor: 2 })];
  const h = setup(() => response(pages.shift()));
  const lines = await collect(h.client.stream(await h.client.begin(body())));
  assert.deepEqual(lines, ['data: ' + JSON.stringify(delta('A')), 'data: [DONE]']);
  assert.deepEqual(h.sleeps, [1000]);
  assert.deepEqual(h.calls.filter((c) => c.path.includes('?after')).map((c) => c.path.split('after=')[1]), ['0', '1', '2']);
});

test('ordinary sequence gap stays pending and never emits DONE', async () => {
  const h = setup(() => response(page('completed', [event(3, delta('Missing')), event(4, '[DONE]')])));
  await assert.rejects(collect(h.client.stream(await h.client.begin(body()))), /Faltam eventos/);
});

test('only an explicit withdrawal bridges a monotonic gap (including first replay page)', async () => {
  for (const prior of [false, true]) {
    const pages = prior ? [page('running', [event(1, delta('Withdrawn'))], { has_more: true })] : [];
    pages.push(page('completed', [event(9, { iald_aviso: { retirar_resposta: true, tipo: 'moderacao_resposta' } }), event(10, '[DONE]')]));
    const h = setup(() => response(pages.shift()));
    const lines = await collect(h.client.stream(await h.client.begin(body())));
    assert.equal(lines.at(-1), 'data: [DONE]');
    assert.ok(lines.some((line) => line.includes('retirar_resposta')));
  }
});

test('notice without boolean true does not authorize sequence gap', async () => {
  for (const flag of [undefined, false, 'true', 1]) {
    const h = setup(() => response(page('completed', [event(5, { iald_aviso: { retirar_resposta: flag } })])));
    await assert.rejects(collect(h.client.stream(await h.client.begin(body()))), /Faltam eventos/);
  }
});

for (const status of ['failed', 'cancelled', 'interrupted']) {
  test(status + ' cannot turn partial text and DONE into a normal completed answer', async () => {
    const h = setup(() => response(page(status, [event(1, delta('Partial')), event(2, '[DONE]')])));
    const lines = [];
    await assert.rejects((async () => { for await (const line of h.client.stream(await h.client.begin(body()))) lines.push(line); })(), { terminal: true, status });
    assert.ok(!lines.includes('data: [DONE]'));
  });
}

test('error event wins over completed status and DONE', async () => {
  const h = setup(() => response(page('completed', [event(1, { error: 'Falha segura' }), event(2, '[DONE]')])));
  await assert.rejects(collect(h.client.stream(await h.client.begin(body()))), { terminal: true, status: 'failed' });
});

test('completed without DONE, invalid JSON, and bad cursor fail closed', async () => {
  for (const result of [page('completed', [event(1, delta('A'))]), page('completed', [event(1, '{broken')]),
    page('completed', [event(1, '[DONE]')], { cursor: 8 })]) {
    const h = setup(() => response(result));
    await assert.rejects(collect(h.client.stream(await h.client.begin(body()))), { pending: true });
  }
});

test('ack waits for durable history; 409 retains saved phase for ack-only retry', async () => {
  let saved = false, ack = 0;
  const h = setup(null, { request: async (path, opts) => {
    if (path.endsWith('/session')) return response({ account: A });
    if (path.endsWith('/ack')) { assert.ok(saved); return response({ ok: true }, ++ack === 1 ? 409 : 200); }
    if (opts.method === 'POST') return response(job(), 202);
    return response(donePage());
  } });
  const r = await h.client.begin(body()); await collect(h.client.stream(r));
  await assert.rejects(h.client.delivered(r, () => { throw new Error('Disk full'); }), /Disk full/);
  assert.equal(ack, 0);
  await assert.rejects(h.client.delivered(r, () => { saved = true; }), { httpStatus: 409 });
  assert.equal(h.client.pending()[0].phase, 'saved'); assert.equal(h.client.pending()[0].payload, null);
  await h.client.acknowledge(h.client.pending()[0]);
  assert.equal(h.client.pending().length, 0); assert.equal(ack, 2);
});

test('delivery transaction deduplicates a replay after saved history but lost outbox', () => {
  const c = { id: 'c_test', mensagens: [] }, r = { ...job(), request_id: ID };
  assert.equal(applyChatJobDelivery(c, r, { answer: { role: 'assistant', content: 'Once' } }), true);
  assert.equal(applyChatJobDelivery(c, r, { answer: { role: 'assistant', content: 'Once' } }), false);
  assert.equal(c.mensagens.length, 1); assert.equal(c.mensagens[0].chat_job_id, ID);
});

test('server discovery restores only existing conversations, from zero without a POST', async () => {
  const h = setup((path) => path === '/api/chat-jobs'
    ? response({ account: A, jobs: [job('completed'), job('running', { id: ID2, conversation_id: 'c_missing' })] }) : response(donePage()));
  const records = await h.client.discover((id) => id === 'c_test');
  assert.equal(records.length, 1); assert.equal(records[0].payload, null);
  await collect(h.client.stream(records[0]));
  assert.equal(h.calls.filter((c) => c.opts.method === 'POST').length, 0);
});

test('pending payloads are isolated by authenticated account', async () => {
  const h = setup(); const r = await h.client.begin(body());
  h.client.setOwner(B); h.changeAccount(B);
  assert.deepEqual(h.client.pending(), []);
  await assert.rejects(collect(h.client.stream(r)), { detached: true });
  h.client.setOwner(A); assert.equal(h.client.pending()[0].payload.account, A);
});

test('session mismatch before begin clears owner and never sends payload', async () => {
  const h = setup(); h.changeAccount(B);
  await assert.rejects(h.client.begin(body()), { detached: true });
  assert.equal(h.client.owner(), ''); assert.equal(h.calls.filter((c) => c.opts.method === 'POST').length, 0);
});

test('list account mismatch refuses recovery even if session check just succeeded', async () => {
  const h = setup(() => response({ account: B, jobs: [job()] }));
  await assert.rejects(h.client.discover(() => true), { detached: true });
  assert.equal(h.client.owner(), ''); assert.equal(h.storage.values.size, 0);
});

test('cookie change between session check and POST keeps ORIGINAL account and UUID', async () => {
  const posts = [];
  const h = setup(null, { request: async (path, opts) => {
    if (path.endsWith('/session')) return response({ account: A });
    posts.push(JSON.parse(opts.body)); return response({ error: 'A conta mudou.' }, 409);
  } });
  const r = await h.client.begin(body());
  await assert.rejects(collect(h.client.stream(r)), { httpStatus: 409 });
  assert.equal(posts[0].account, A); assert.equal(posts[0].request_id, ID);
  assert.equal(h.client.pending().length, 1);
});

test('HTTP 401 clears scope; display names never become owners', async () => {
  let lost = 0;
  const h = setup(null, { onScopeLost: () => lost++, request: async () => response({}, 401) });
  await assert.rejects(h.client.begin(body()), { detached: true });
  assert.equal(h.client.owner(), ''); assert.equal(lost, 1);
  h.client.setOwner('sessao-web'); assert.equal(h.client.owner(), '');
});

test('pause/logout abort observation without cancel; late old-account response is ignored', async () => {
  let release, requested;
  const ready = new Promise((resolve) => { requested = resolve; });
  const h = setup(() => new Promise((resolve) => { release = resolve; requested(); }));
  const r = await h.client.begin(body()), observing = collect(h.client.stream(r));
  await ready; h.client.setOwner(B); release(response(donePage()));
  await assert.rejects(observing, { detached: true });
  assert.equal(h.calls.filter((c) => c.path.endsWith('/cancel')).length, 0);
  assert.equal(h.client.pending().length, 0);
});

test('explicit stop after uncertain submission cancels same ID without new inference', async () => {
  let posts = 0, cancels = 0;
  const h = setup(null, { request: async (path, opts) => {
    if (path.endsWith('/session')) return response({ account: A });
    if (path.endsWith('/cancel')) { cancels++; assert.ok(path.includes(ID)); return response(job('cancelled')); }
    if (opts.method === 'POST') { posts++; throw new Error('Lost response'); }
  } });
  const r = await h.client.begin(body()); await assert.rejects(collect(h.client.stream(r)));
  await h.client.cancel(r); assert.equal(posts, 1); assert.equal(cancels, 1);
});

test('explicit stop before attempted submission remains local and never submits', async () => {
  const h = setup(), r = await h.client.begin(body()); await h.client.cancel(r);
  await assert.rejects(collect(h.client.stream(r)), { terminal: true, status: 'cancelled' });
  assert.equal(h.calls.filter((c) => c.opts.method === 'POST').length, 0);
  await h.client.delivered(r, () => {}); assert.equal(h.client.pending().length, 0);
});

test('privacy purge uses dedicated route and preserves local outbox on remote failure', async () => {
  let success = false;
  const h = setup((path, opts) => {
    assert.equal(path, '/api/chat-jobs/conversations/c_test/delete');
    assert.equal(opts.body, '{}'); return response({ ok: true }, success ? 200 : 503);
  });
  await h.client.begin(body());
  await assert.rejects(h.client.purgeConversation('c_test')); assert.equal(h.client.pending().length, 1);
  success = true; await h.client.purgeConversation('c_test'); assert.equal(h.client.pending().length, 0);
});

// Evaluate the generated application itself with a minimal DOM and mocked fetch.
// Rendering libraries, native bridges and background OS scheduling are not tested.
class Node {
  constructor(cls = '') { this.className = cls; this.dataset = {}; this.style = {}; this.childNodes = []; this._text = ''; this.parentElement = null; this.isConnected = false; this.classList = { add() {}, remove() {}, toggle() {} }; }
  appendChild(n) { this.childNodes.push(n); n.parentElement = this; n.isConnected = true; return n; }
  remove() { if (this.parentElement) this.parentElement.childNodes = this.parentElement.childNodes.filter((n) => n !== this); this.isConnected = false; }
  replaceChild(n, old) { this.childNodes[this.childNodes.indexOf(old)] = n; n.parentElement = this; }
  isEqualNode(n) { return this.textContent === n.textContent; }
  querySelector(sel) { return this.childNodes.find((n) => '.' + n.className === sel) || this.childNodes.map((n) => n.querySelector(sel)).find(Boolean) || null; }
  querySelectorAll() { return []; }
  get textContent() { return this._text + this.childNodes.map((n) => n.textContent).join(''); }
  set textContent(v) { this._text = String(v); this.childNodes = []; }
  set innerHTML(v) { this._text = ''; this.childNodes = []; }
  get innerHTML() { return this._text; }
  addEventListener() {} focus() {} setAttribute() {}
}
function appHarness(handler, { nativeApp = null } = {}) {
  const storage = new Storage(), calls = [], notices = [], rendered = [], timers = new Map();
  const input = new Node(), root = new Node(), listeners = new Map(); let nextTimer = 0;
  const document = { readyState: 'loading', hidden: false, createElement: () => new Node(),
    addEventListener: (name, fn) => listeners.set(name, fn),
    querySelector: (sel) => sel === '#entrada' ? input : sel === '#conversa-interna' ? root : null,
    querySelectorAll: () => [] };
  const sandbox = { document, localStorage: storage, location: { search: '', protocol: 'https:', origin: 'https://offline.invalid', hash: '' },
    navigator: {}, URLSearchParams, URL, AbortController, AbortSignal, DOMException, crypto: webcrypto,
    console, TextEncoder, TextDecoder, SYSTEM_PROMPT: 'System', SYSTEM_PROMPT_LOJA: 'System', PTBR_FIXES: [],
    setTimeout: (fn, ms) => { timers.set(++nextTimer, { fn, ms }); return nextTimer; }, clearTimeout: (id) => timers.delete(id),
    setInterval: () => 0, clearInterval() {}, Node, notices, rendered,
    fetch: async (path, opts) => {
      const address = new URL(path, 'https://offline.invalid');
      path = address.pathname + address.search;
      calls.push({ path, opts });
      if (path.endsWith('/session')) return response({ account: A });
      if (path === '/api/chat-jobs' && opts.method === 'POST') return response(job('running', { id: JSON.parse(opts.body).request_id }), 202);
      return handler(path, opts, calls);
    } };
  sandbox.window = { addEventListener: (name, fn) => listeners.set(name, fn), matchMedia: () => ({ matches: false }), location: sandbox.location };
  if (nativeApp) sandbox.window.Capacitor = { Plugins: { App: nativeApp } };
  const context = vm.createContext(sandbox);
  const application = readFileSync(new URL('./iald.js', import.meta.url), 'utf8').replace(/^import .*;\r?\n/gm, '').replace(/\bexport /g, '');
  vm.runInContext(application, context, { filename: 'staged/iald.js' });
  vm.runInContext(`
    portaoNecessario = () => false;
    avisar = (text) => notices.push(text);
    listarConversas = atualizarBotaoEnviar = atualizarDica = rolarSePerto = congelarTrilha = passoTrilha = pintarModeloResposta = carregarMotor = () => {};
    aplicarPtbr = (text) => text;
    abrirConversa = () => {};
    abrirConsentimento = (...args) => notices.push({ consent: args });
    abrirCreditos = (aviso) => notices.push({ credits: aviso });
    desenharMensagem = () => {
      const row = new Node('msg'), body = row.appendChild(new Node('msg-corpo'));
      body.appendChild(new Node('trilha')); body.appendChild(new Node('conteudo')); rendered.push(row); return body;
    };
    renderMarkdown = (text) => { const node = new Node(); const textNode = node.appendChild(new Node()); textNode.textContent = text; return node; };
    const originalNoticeRenderer = pintarAviso;
    pintarAviso = (...args) => { notices.push(args[2]); return originalNoticeRenderer(...args); };
    backgroundOwner = '${A}'; backgroundJobs.setOwner(backgroundOwner);
    S.conversas = [{ id: 'c_test', background_owner: backgroundOwner, mensagens: [{ role: 'user', content: 'Pergunta' }] }]; S.ativaId = 'c_test';
    globalThis.app = { S, backgroundJobs, transmitir, parar, desanexarRespostasBackground, recuperarRespostasBackground,
      identificarContaBackground, apagarJobsDaConversa, ligarRespostasBackground, respostaPendenteBackground, persistirConversasBackground };
  `, context);
  return { context, app: sandbox.app, storage, calls, notices, rendered, timers, listeners, document,
    evaluate: (text) => vm.runInContext(text, context) };
}
function appPage(path, calls, result) {
  const post = calls.find((call) => call.path === '/api/chat-jobs' && call.opts.method === 'POST');
  const id = post ? JSON.parse(post.opts.body).request_id : ID;
  return response({ ...result, id });
}

test('generated client preserves model, seal, thinking split and exact legacy request fields', async () => {
  const seal = { link: 'c'.repeat(64), conv: 'c_test' };
  const h = appHarness((path, opts, calls) => path.endsWith('/ack') ? response({ ok: true }) : appPage(path, calls,
    page('completed', [event(1, { iald_modelo: { rotulo: 'Motor', id: 'provider-model', motor: 'anthropic' } }), event(2, delta('<think>Private thought</think>Answer')),
      event(3, { iald_selo: seal }), event(4, '[DONE]')])));
  await h.app.transmitir(body().messages);
  const answers = h.app.S.conversas[0].mensagens.filter((m) => m.role === 'assistant');
  assert.equal(answers.length, 1); assert.equal(answers[0].content, 'Answer');
  assert.equal(answers[0].selo.link, seal.link); assert.ok(answers[0].bruto.includes('<think>'));
  assert.equal(answers[0].modelo.id, 'provider-model'); assert.equal(answers[0].modelo.rotulo, 'Motor');
  const payload = JSON.parse(h.calls.find((c) => c.opts.method === 'POST' && c.path === '/api/chat-jobs').opts.body);
  assert.equal(payload.account, A); assert.equal(payload.iald_surface, 'web'); assert.equal(payload.stream, true);
  assert.equal(payload.model, 'qwen3'); assert.equal(payload.temperature, 0.7); assert.equal(payload.max_tokens, 4096);
  assert.equal(h.calls.filter((c) => c.path.endsWith('/ack')).length, 1);
  assert.ok(h.notices.includes('A resposta continua no servidor. Você pode sair e voltar.'));
});

test('generated client never persists or seals a partial answer on network failure', async () => {
  let reads = 0;
  const h = appHarness((path, opts, calls) => {
    if (++reads > 1) throw new Error('Offline');
    return appPage(path, calls, page('running', [event(1, delta('Partial')), event(2, { iald_selo: { link: 'c'.repeat(64) } })], { has_more: true }));
  });
  await h.app.transmitir(body().messages);
  assert.equal(h.app.S.conversas[0].mensagens.length, 1);
  assert.equal(h.app.backgroundJobs.pending().length, 1);
  assert.equal(h.calls.filter((c) => c.path.endsWith('/ack')).length, 0);
  assert.ok(!h.rendered.at(-1).textContent.includes('Partial'));
  assert.equal(h.app.respostaPendenteBackground(), true);
});

test('generated client handles moderation reset gap, clears old text, and saves only notice', async () => {
  let reads = 0;
  const h = appHarness((path, opts, calls) => {
    if (path.endsWith('/ack')) return response({ ok: true });
    return appPage(path, calls, ++reads === 1 ? page('running', [event(1, delta('Withdrawn text'))], { has_more: true })
      : page('completed', [event(7, { iald_aviso: { tipo: 'moderacao_resposta', texto: 'Resposta retirada.', retirar_resposta: true } }),
        event(8, { iald_selo: { link: 'c'.repeat(64) } }), event(9, delta('Forbidden late text')), event(10, '[DONE]')]));
  });
  await h.app.transmitir(body().messages);
  assert.equal(h.app.S.conversas[0].mensagens.length, 1);
  const delivery = Object.values(h.app.S.conversas[0].chat_job_deliveries)[0];
  assert.equal(delivery.notice.retirar_resposta, true);
  assert.ok(!h.rendered.at(-1).textContent.includes('Withdrawn'));
  assert.ok(!h.rendered.at(-1).textContent.includes('Forbidden'));
});

test('generated client persists failed terminal notice without assistant or seal', async () => {
  const h = appHarness((path, opts, calls) => path.endsWith('/ack') ? response({ ok: true }) : appPage(path, calls,
    page('interrupted', [event(1, delta('Partial')), event(2, { iald_selo: { link: 'c'.repeat(64) } }), event(3, '[DONE]')])));
  await h.app.transmitir(body().messages);
  assert.equal(h.app.S.conversas[0].mensagens.length, 1);
  assert.equal(Object.values(h.app.S.conversas[0].chat_job_deliveries)[0].status, 'interrupted');
  assert.equal(h.app.backgroundJobs.pending().length, 0);
});

test('generated client keeps ack pending and retries without replaying assistant', async () => {
  let ack = 0, reads = 0;
  const h = appHarness((path, opts, calls) => {
    if (path.endsWith('/ack')) return response({ ok: true }, ++ack === 1 ? 409 : 200);
    if (path === '/api/chat-jobs') {
      const id = h.app.backgroundJobs.pending()[0].id;
      return response({ account: A, jobs: [job('completed', { id })] });
    }
    reads++; return appPage(path, calls, donePage());
  });
  await h.app.transmitir(body().messages);
  assert.equal(h.app.backgroundJobs.pending()[0].phase, 'saved');
  await h.app.recuperarRespostasBackground();
  assert.equal(h.app.S.conversas[0].mensagens.length, 2); assert.equal(reads, 1); assert.equal(ack, 2);
});

test('generated client logout detaches but does not cancel or save a partial', async () => {
  let release, started;
  const ready = new Promise((resolve) => { started = resolve; });
  const h = appHarness(() => new Promise((resolve) => { release = resolve; started(); }));
  const turn = h.app.transmitir(body().messages); await ready;
  h.app.desanexarRespostasBackground(true); release(response(donePage())); await turn;
  assert.equal(h.app.S.conversas.length, 0); assert.equal(h.app.backgroundJobs.owner(), '');
  assert.equal(h.calls.filter((c) => c.path.endsWith('/cancel') || c.path.endsWith('/ack')).length, 0);
});

test('generated client Stop sends cancel; ordinary observation abort does not', async () => {
  let started;
  const ready = new Promise((resolve) => { started = resolve; });
  const h = appHarness((path, opts, calls) => {
    if (path.endsWith('/cancel')) return appPage(path, calls, job('cancelled'));
    return new Promise((resolve, reject) => { opts.signal.addEventListener('abort', () => reject(new Error('Aborted'))); started(); });
  });
  const turn = h.app.transmitir(body().messages); await ready; h.app.parar(); await turn;
  await Promise.resolve();
  assert.equal(h.calls.filter((c) => c.path.endsWith('/cancel')).length, 1);
  assert.equal(h.app.S.conversas[0].mensagens.length, 1);
});

test('generated client binds startup, visibility and online recovery and documents retention', () => {
  const h = appHarness(() => response({ account: A, jobs: [] }));
  h.document.hidden = true; h.app.ligarRespostasBackground();
  assert.equal(typeof h.listeners.get('visibilitychange'), 'function');
  assert.equal(typeof h.listeners.get('online'), 'function');
  const generated = readFileSync(new URL('./iald.js', import.meta.url), 'utf8');
  assert.ok(generated.includes('criptografadas e ficam disponíveis para recuperação por até 7 dias'));
  assert.ok(generated.includes("if (c && !await apagarJobsDaConversa(c.id)) return;"));
  assert.ok(generated.includes("async function apagarConversa(id) {\n  if (!await apagarJobsDaConversa(id)) return;"));
});

test('generated recovery replays server-only jobs and does not duplicate a saved delivery', async () => {
  let reads = 0, acks = 0;
  const h = appHarness((path) => {
    if (path === '/api/chat-jobs') return response({ account: A, jobs: [job('completed')] });
    if (path.endsWith('/ack')) { acks++; return response({ ok: true }); }
    reads++; return response(donePage());
  });
  await h.app.recuperarRespostasBackground();
  assert.equal(h.app.S.conversas[0].mensagens.length, 2);
  // Simulate the server's list remaining visible after a lost ack response/outbox.
  await h.app.recuperarRespostasBackground();
  assert.equal(h.app.S.conversas[0].mensagens.length, 2);
  assert.equal(reads, 1); assert.equal(acks, 2);
  assert.equal(h.calls.filter((c) => c.path === '/api/chat-jobs' && c.opts.method === 'POST').length, 0);
});

test('generated client preserves consent notice and excludes it from assistant history', async () => {
  const notice = { tipo: 'consentimento_ia', texto: 'Autorize o provedor.', provedor: 'anthropic', versao: 'test-v1' };
  const h = appHarness((path, opts, calls) => path.endsWith('/ack') ? response({ ok: true }) : appPage(path, calls,
    page('completed', [event(1, { iald_aviso: notice }), event(2, delta(notice.texto)), event(3, '[DONE]')])));
  await h.app.transmitir(body().messages);
  assert.equal(h.app.S.conversas[0].mensagens.length, 1);
  assert.equal(Object.values(h.app.S.conversas[0].chat_job_deliveries)[0].notice.tipo, 'consentimento_ia');
  assert.ok(h.notices.some((item) => item?.consent));
});

test('generated client authenticates account from session and isolates history on switch', async () => {
  const h = appHarness(() => response({ account: A, jobs: [] }));
  await h.app.backgroundJobs.begin(body());
  h.app.persistirConversasBackground();
  h.storage.setItem('iald_conversas_owner_v1:' + B, JSON.stringify({ conversas: [{ id: 'c_b', background_owner: B, mensagens: [] }], ativa: 'c_b' }));
  h.context.fetch = async (path) => { assert.equal(path, '/api/chat-jobs/session'); return response({ account: B }); };
  await h.app.identificarContaBackground();
  assert.equal(h.app.backgroundJobs.owner(), B); assert.equal(h.app.backgroundJobs.pending().length, 0);
  assert.equal(h.app.S.conversas[0].id, 'c_b');
  const old = JSON.parse(h.storage.getItem('iald_chat_jobs_v1:' + A));
  assert.equal(old[0].payload.account, A); assert.equal(old[0].attempted, false);
});

test('generated client HTTP 401 clears account without fallback or cancelling jobs', async () => {
  const h = appHarness(() => response({}, 401));
  await h.app.transmitir(body().messages);
  assert.equal(h.app.backgroundJobs.owner(), ''); assert.equal(h.app.S.conversas.length, 0);
  assert.equal(h.calls.filter((call) => call.path.endsWith('/cancel') || call.path.endsWith('/ack')).length, 0);
});

test('native appStateChange registers once, pauses without cancel and recovers despite stale hidden WebView', async () => {
  const registrations = [];
  const h = appHarness((path) => {
    if (path === '/api/chat-jobs') return response({ account: A, jobs: [job('completed')] });
    if (path.endsWith('/ack')) return response({ ok: true });
    return response(donePage());
  }, { nativeApp: { addListener: (name, callback) => { registrations.push({ name, callback }); return Promise.resolve({ remove() {} }); } } });
  h.document.hidden = true;
  h.app.ligarRespostasBackground(); h.app.ligarRespostasBackground();
  assert.equal(registrations.length, 1); assert.equal(registrations[0].name, 'appStateChange');
  const controller = new AbortController(); h.app.S.aborto = controller; h.app.S.gerando = true;
  await registrations[0].callback({ isActive: false });
  assert.equal(controller.signal.reason.type, 'detach'); assert.equal(h.app.backgroundJobs.owner(), A);
  await registrations[0].callback({ isActive: true });
  assert.equal(h.app.S.conversas[0].mensagens.length, 2);
  assert.equal(h.calls.filter((call) => call.path.endsWith('/cancel')).length, 0);
  assert.equal(h.calls.filter((call) => call.path === '/api/chat-jobs' && call.opts.method === 'POST').length, 0);
  await registrations[0].callback({ isActive: true });
  assert.equal(h.app.S.conversas[0].mensagens.length, 2);
});

test('unavailable native lifecycle listener leaves visibility recovery usable', async () => {
  let attempts = 0;
  const h = appHarness(() => response({ account: A, jobs: [] }), {
    nativeApp: { addListener: () => { attempts++; return Promise.reject(new Error('Plugin unavailable')); } },
  });
  h.document.hidden = true; h.app.ligarRespostasBackground();
  await new Promise(setImmediate); // Flush cross-realm promise adoption and rejection.
  h.app.ligarRespostasBackground(); await new Promise(setImmediate);
  assert.equal(attempts, 2); assert.equal(typeof h.listeners.get('visibilitychange'), 'function');
  assert.equal(h.calls.length, 0);
});

test('voluntary cancellation persists a dedicated interruption notice instead of failure', async () => {
  const h = appHarness((path, opts, calls) => path.endsWith('/ack') ? response({ ok: true }) : appPage(path, calls,
    page('cancelled', [event(1, delta('Partial')), event(2, '[DONE]')])));
  await h.app.transmitir(body().messages);
  const saved = JSON.parse(h.storage.getItem('iald_conversas_owner_v1:' + A));
  const delivery = Object.values(saved.conversas[0].chat_job_deliveries)[0];
  assert.equal(delivery.status, 'cancelled'); assert.equal(delivery.notice.tipo, 'resposta_interrompida');
  assert.equal(saved.conversas[0].mensagens.length, 1);
  assert.ok(h.rendered.at(-1).textContent.includes('Resposta interrompida'));
  assert.ok(!h.rendered.at(-1).textContent.includes('Falha na resposta'));
  assert.equal(h.app.backgroundJobs.pending().length, 0);
});
