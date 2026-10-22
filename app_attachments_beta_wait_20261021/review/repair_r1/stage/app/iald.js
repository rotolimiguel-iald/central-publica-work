// ══════════════════════════════════════════════════════════════════════════
// IALD — comportamento do app (interface nova, 11/09/2026)
//
// Contratos do servidor, todos MEDIDOS em iald_web_server.py (nao supostos):
//   POST /v1/chat/completions  {model, messages, max_tokens, temperature,
//                               stream:true, iald_mode:"fast"|"think"}
//        SSE: linhas "data: {...}"; linha iniciada por ":" e keepalive, ignora.
//        O chunk pode trazer:
//          - iald_status {fase, tool, rotulo, loop, max_loops, chars}  <- agent_loop
//          - choices[0].delta.content
//          - choices[0].delta.reasoning_content                        <- modo pensar
//        Fim: "data: [DONE]".
//   GET  /api/contexto      -> {n_ctx, margem, reserva_resposta, cpt, teto_mensagens}
//   GET  /api/active-model  -> {id, short, label, online, n_ctx, vision}  [PUBLICO]
//   GET  /health            -> proxy do llama-server; 502 quando o modelo esta fora
//   POST /api/extract-text  (multipart "file") -> {name,text,chars,pages,truncated}
//   GET  /logout
//   GET  /api/motor         -> {motor, modelo, plano, cota, consentimento, limites}  (14/09/2026)
//                              + pode_escolher: conta AMPLIADA pelo operador (15/09/2026)
//   POST /api/motor/escolha {motor: nativa|openai} -> a conta ampliada escolhe quem responde (15/09/2026)
//        cota: {plano, tokens_dia:{usado,limite}, tokens_mes:{usado,limite}, usd_dia,
//               renova_dia_utc, renova_mes_utc, definicao, bloqueado_por} | {plano, erro} | null
//        limites (rodada 2, 14/09 noite): {agente, pensar, ferramentas:[nomes]|null, max_saida,
//               janela}. ferramentas null = todas as da superfície. Servidor sem o campo =
//               comportamento de antes (nada se desliga na tela).
//        limites.imagens (rodada 3, 14/09 noite): bool — false no plano gratuito; o servidor recusa
//               imagem com o aviso "recurso_indisponivel" sem chamar o modelo. Sem o campo = permitido.
//   GET  /api/tgl/balance   -> conta gratuita sem conta no razão: {balance:0, ..., sem_conta:true}
//   POST /api/entrar/situacao -> pedido pendente pelo limite de contas novas: 202 {status:"pending",
//        mensagem, motivo:"limite"}; /api/entrar/config ganha motivo_fechada (só informativo).
//   POST /api/denuncia      {motivo, resposta<=4000, detalhe?<=500, pergunta?<=2000}
//        -> 201 {ok, id, mensagem}. Campo acima do teto é RECUSADO (400), não cortado:
//        quem corta é o app, por ponto de código (a conta do Python), antes de enviar.
//   Chunk iald_aviso {tipo, texto, ...}: o servidor não chamou o modelo, só avisou
//        (consentimento_ia, limite+cota+bloqueado_por, moderacao, ocupado, em_andamento,
//        motor_indisponivel, recurso_indisponivel...). Com `retirar_resposta: true` (moderação da
//        RESPOSTA, no fim do stream) o texto já pintado sai da tela e fica só o aviso.
//   SELO IALD (22/09/2026) — CONTRATO COMBINADO com a obra do servidor do mesmo dia, ainda NÃO
//   medido no iald_web_server.py (conferir quando a obra do servidor fechar):
//        POST /v1/chat/completions ganha iald_conv (id da conversa, ^[A-Za-z0-9_-]{1,64}$) e
//        iald_selo_prev (64 hex minúsculos = elo da resposta selada anterior da conversa, ou "");
//        o servidor tira os dois antes do modelo. Logo antes do [DONE], só num stream que terminou
//        normal (nunca depois de retirar_resposta), pode vir o chunk
//        {iald_selo: {recibo, link, sig, casa}}. O selo cobre a concatenação CRUA de todo
//        choices[0].delta.content (com as marcas <think>; sem reasoning_content, sem aplicarPtbr).
//   POST /api/exportar      {formato: txt|md|pdf, titulo, mensagens:[{role, texto, selo?}]} (≤ 2 MB,
//        ≤ 400 mensagens) -> 200 {url, caminho:"/exportado/<token>/<nome>", expira_em, selados,
//        total}; erro -> {error} com 4xx/5xx (503 = PDF indisponível, 413 = grande demais).
//   GET  /exportado/<token>/<nome> -> o arquivo; endereço público por 15 minutos, sem cabeçalho.
//
// O prompt de sistema NAO vem do servidor: quem monta e o frontend (medido).
// Por isso ele e importado de kernel_prompt.js, que e GERADO POR SCRIPT a
// partir do iald_chat.html — nunca redigitado.
// ══════════════════════════════════════════════════════════════════════════

import { createRegistrationIdentity } from './registration_identity.js';
let registrationIdentity = null;
let sheetAfterRegistration = '';
document.addEventListener('iald:identification-closed', () => {
  if (document.querySelector('.registration-overlay')) return;
  const next = sheetAfterRegistration;
  sheetAfterRegistration = '';
  if (next) abrirFolha(next);
  else oferecerConsentimento();
});
function verificarIdentificacaoCadastro(pedido = '') {
  if (DEMO) return;
  if (!registrationIdentity) registrationIdentity = createRegistrationIdentity({ request: fetchIALD });
  const account = recuperar(K.usuario, 'sessao-web');
  registrationIdentity.check({ pedido, account, isCurrent: () => pedido
    ? recuperar(K.pedido, '') === pedido && portaoNecessario()
    : !portaoNecessario() && recuperar(K.usuario, 'sessao-web') === account });
}

import { SYSTEM_PROMPT, PTBR_FIXES } from './kernel_prompt.js';

// Variante do build das lojas: idêntica ao prompt de produção, menos a tabela de
// preços de licenciamento. Gerada por script a partir do MESMO arquivo
// (scratchpad/gera_prompt_loja.py): 24.959 → 24.821 caracteres, uma única linha
// removida, com conferência linha a linha de que nada mais mudou.
import { SYSTEM_PROMPT_LOJA } from './kernel_prompt_loja.js';

// Optional local module: a failed import stays unavailable for this page lifetime.
let byteTransportModule;
function loadByteTransport() {
  if (!byteTransportModule) byteTransportModule = import('./iald_transport.mjs').catch(() => null);
  return byteTransportModule;
}

// Durable transport only. All HTTP uses the app's authenticated request function.
const TERMINAL_JOB_STATUSES = new Set(['completed', 'failed', 'cancelled', 'interrupted', 'expired']);
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
const ACCOUNT = /^[0-9a-f]{64}$/;
const STATUSES = new Set(['queued', 'running', ...TERMINAL_JOB_STATUSES]);
const copy = (value) => JSON.parse(JSON.stringify(value));

class PendingChatJobError extends Error {
  constructor(message, extra = {}) {
    super(message); this.name = 'PendingChatJobError'; this.pending = true;
    Object.assign(this, extra);
  }
}
class TerminalChatJobError extends Error {
  constructor(status, message) {
    super(message); this.name = 'TerminalChatJobError'; this.terminal = true; this.status = status;
  }
}
const detached = () => new PendingChatJobError('Acompanhamento pausado; a resposta permanece no servidor.', { detached: true });
const defaultSleep = (ms, signal) => new Promise((resolve, reject) => {
  if (signal?.aborted) { reject(detached()); return; }
  const finish = () => { signal?.removeEventListener('abort', stop); resolve(); };
  const timer = setTimeout(finish, ms);
  const stop = () => { clearTimeout(timer); signal.removeEventListener('abort', stop); reject(detached()); };
  signal?.addEventListener('abort', stop, { once: true });
});

// Account-scoped durable JSON. No media permission changes or provider calls.
// IndexedDB owns atomic full snapshots; WebStorage stores only small pointers.
function createChatLocalStore({ indexedDB = globalThis.indexedDB, crypto = globalThis.crypto, keyRange = globalThis.IDBKeyRange } = {}) {
  let opening;
  const failure = () => new PendingChatJobError('Não foi possível verificar o armazenamento local. O conteúdo deve ser preservado; novo envio ou confirmação de entrega estão bloqueados.');
  async function database() {
    if (!indexedDB || !crypto?.subtle) throw failure();
    if (!opening) opening = new Promise((resolve, reject) => {
      const r = indexedDB.open('iald-chat-durable-json-v1', 1);
      r.onupgradeneeded = () => r.result.createObjectStore('json');
      r.onerror = r.onblocked = () => reject(failure());
      r.onsuccess = () => {
        const db = r.result;
        db.onversionchange = () => { db.close(); opening = null; };
        resolve(db);
      };
    }).catch(e => { opening = null; throw e; });
    return opening;
  }
  async function transaction(mode, action) {
    const db = await database();
    return new Promise((resolve, reject) => {
      let result;
      const tx = db.transaction('json', mode);
      tx.oncomplete = () => resolve(result);
      tx.onabort = tx.onerror = () => reject(failure());
      try { const r = action(tx.objectStore('json')); r.onsuccess = () => { result = r.result; }; }
      catch (_) { tx.abort(); reject(failure()); }
    });
  }
  const digest = async raw => {
    const bytes = new TextEncoder().encode(raw);
    const hash = await crypto.subtle.digest('SHA-256', bytes);
    return { bytes: bytes.length, sha256: Array.from(new Uint8Array(hash), b => b.toString(16).padStart(2, '0')).join('') };
  };
  function validate(owner, kind) {
    if (!ACCOUNT.test(owner) || !['history', 'payload'].includes(kind)) throw failure();
  }
  async function get(owner, kind, ref) {
    validate(owner, kind);
    if (!ref || ref.owner !== owner || ref.kind !== kind || ref.v !== 1 ||
        typeof ref.key !== 'string' || !ref.key.startsWith(owner + ':' + kind + ':')) throw failure();
    const record = await transaction('readonly', store => store.get(ref.key));
    if (!record || record.owner !== owner || record.kind !== kind || typeof record.raw !== 'string') throw failure();
    const pin = await digest(record.raw);
    if (pin.sha256 !== record.sha256 || pin.bytes !== record.bytes ||
        (kind === 'payload' && ref.key !== owner + ':payload:' + pin.sha256)) throw failure();
    return record.raw;
  }
  async function put(owner, kind, raw) {
    validate(owner, kind);
    if (typeof raw !== 'string') throw failure();
    const pin = await digest(raw);
    // One atomic current history per owner; immutable payloads by content hash.
    const key = owner + ':' + kind + ':' + (kind === 'history' ? 'current' : pin.sha256);
    const ref = { v: 1, owner, kind, key };
    await transaction('readwrite', store => store.put({ owner, kind, raw, ...pin }, key));
    if (await get(owner, kind, ref) !== raw) throw failure();
    return ref;
  }
  async function remove(owner, kind, ref) {
    await get(owner, kind, ref); // Never delete a different scope or broken ref.
    await transaction('readwrite', store => store.delete(ref.key));
  }
  async function purge(owner) {
    validate(owner, 'history');
    if (!keyRange) throw failure();
    const range = keyRange.bound(owner + ':', owner + ':\uffff');
    await transaction('readwrite', store => store.delete(range));
    const left = await transaction('readonly', store => store.getAllKeys(range));
    if (left.length) throw failure();
  }
  return { put, get, remove, purge };
}

function createDurableChatJobs({ request, storage, payloadStore = null, randomUUID = () => crypto.randomUUID(),
  sleep = defaultSleep, onPending = () => {}, onSubmitted = () => {}, onScopeLost = () => {}, requestTimeout = 20000 }) {
  let owner = '', generation = 0, byteTransport = null;
  const active = new Set();
  const key = (account) => 'iald_chat_jobs_v1:' + encodeURIComponent(account);
  const context = () => {
    if (!owner) throw detached();
    return { owner, generation };
  };
  const current = (scope) => scope.owner === owner && scope.generation === generation;
  const check = (scope) => { if (!current(scope)) throw detached(); };
  function loseScope() {
    pause(); owner = ''; onScopeLost();
    throw detached();
  }

  function read(account = owner) {
    try {
      const raw = storage.getItem(key(account));
      const records = raw == null ? [] : JSON.parse(raw);
      if (!Array.isArray(records) || records.some((r) => !r || r.owner !== account || !UUID.test(r.request_id)
        || (r.payload && (r.payload.account !== account || r.payload.request_id !== r.request_id)))) throw new Error();
      return records;
    } catch (_) { throw new PendingChatJobError('Não foi possível ler os pedidos pendentes deste usuário.'); }
  }
  function write(records, scope) {
    check(scope);
    try {
      const raw = JSON.stringify(records.map(r => r.payload_ref ? { ...r, payload: null } : r));
      storage.setItem(key(scope.owner), raw);
      if (storage.getItem(key(scope.owner)) !== raw) throw new Error();
    } catch (_) { throw new PendingChatJobError('Sem espaço para guardar o pedido. Nenhum novo envio será iniciado.'); }
  }
  function update(record, scope, changes = {}) {
    check(scope);
    const records = read(scope.owner);
    const index = records.findIndex((r) => r.request_id === record.request_id);
    if (index < 0) throw new PendingChatJobError('O registro local mudou. Retome pela lista de respostas do servidor.');
    const next = { ...records[index], ...changes };
    write(records.map((r, i) => i === index ? next : r), scope);
    Object.assign(record, next);
    return record;
  }
  function assertRecord(record, scope) {
    check(scope);
    if (!record || record.owner !== scope.owner || !UUID.test(record.request_id)) throw detached();
  }
  async function http(path, options, scope, signal, pageBinding = null) {
    check(scope);
    const controller = new AbortController();
    const abort = () => controller.abort();
    if (signal?.aborted) throw detached();
    signal?.addEventListener('abort', abort, { once: true });
    active.add(controller);
    const timer = setTimeout(abort, requestTimeout);
    try {
      const transport = pageBinding ? byteTransport : null;
      const wirePath = transport ? path + '&transport=' + encodeURIComponent(transport.query) : path;
      const response = await request(wirePath, { ...options, cache: 'no-store', signal: controller.signal });
      check(scope);
      if (response.status === 401) loseScope();
      if (response.status === 410 && (!options.method || options.method === 'GET') &&
          /^\/api\/chat-jobs\/[0-9a-f-]{36}(?:\?after=\d+)?$/.test(path)) {
        throw new TerminalChatJobError('expired', 'Esta resposta temporária expirou. Nenhum novo pedido foi enviado.');
      }
      let body;
      try { body = response.ok && transport
        ? await transport.readPage(response, pageBinding) : await response.json();
      } catch (_) { throw new PendingChatJobError('Resposta do servidor ilegível; o pedido continua pendente.', { noRetry: true }); }
      check(scope);
      if (!response.ok) {
        throw new PendingChatJobError(response.status === 401 ? 'Entre novamente para recuperar sua resposta.'
          : 'Não foi possível acompanhar a resposta agora. O pedido foi preservado.', {
          httpStatus: response.status,
          aviso: body?.bloqueado ? { tipo: 'bloqueado', texto: String(body.error || 'Conta bloqueada.') } : null,
        });
      }
      return body;
    } catch (error) {
      if (!current(scope) || signal?.aborted) throw detached();
      if (error instanceof PendingChatJobError || error instanceof TerminalChatJobError) throw error;
      throw new PendingChatJobError('Sem conexão. A resposta continua pendente; retomaremos com o mesmo pedido.');
    } finally {
      clearTimeout(timer); active.delete(controller);
      signal?.removeEventListener('abort', abort);
    }
  }
  const post = (path, body, scope, signal) => http(path, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
  }, scope, signal);
  async function verifyAccount(scope, signal) {
    const session = await http('/api/chat-jobs/session', {}, scope, signal);
    if (!ACCOUNT.test(session?.account || '') || session.account !== scope.owner) loseScope();
    byteTransport = null;
    if (session.transport) {
      const module = await loadByteTransport();
      check(scope);
      const negotiated = module ? await module.createSessionTransport(session) : null;
      check(scope);
      byteTransport = negotiated;
    }
  }

  function checkJob(value, record) {
    if (!value || !UUID.test(value.id) || !STATUSES.has(value.status)
      || typeof value.conversation_id !== 'string' || value.conversation_id !== record.conversation_id
      || (record.id && value.id !== record.id)) {
      throw new PendingChatJobError('Identidade ou estado da resposta inconsistente; entrega suspensa.');
    }
  }
  async function begin(body) {
    const scope = context();
    await verifyAccount(scope);
    if (!body || typeof body !== 'object' || !/^[A-Za-z0-9_-]{1,64}$/.test(body.iald_conv || '')) {
      throw new PendingChatJobError('A conversa precisa de um identificador válido antes do envio.');
    }
    const request_id = randomUUID();
    if (!UUID.test(request_id)) throw new PendingChatJobError('Não foi possível criar um identificador seguro.');
    const records = read();
    if (records.some((r) => r.conversation_id === body.iald_conv && r.phase !== 'saved')) {
      throw new PendingChatJobError('Esta conversa já tem uma resposta pendente. Aguarde sua recuperação.');
    }
    const record = { owner, request_id, id: null, conversation_id: body.iald_conv,
      payload: copy({ ...body, request_id, account: scope.owner }), phase: 'pending', attempted: false,
      cancel_requested: false, created: Date.now() };
    if (payloadStore) {
      record.payload_ref = await payloadStore.put(scope.owner, 'payload', JSON.stringify(record.payload));
      check(scope);
    }
    write([...records, record], scope); // Mandatory verified write BEFORE any submit.
    return record;
  }
  async function submit(record, scope, signal) {
    assertRecord(record, scope);
    if (record.id) return;
    await verifyAccount(scope, signal);
    // An uncertain POST is recovered by identity, never by resubmitting its body.
    if (record.attempted || read(scope.owner).some((r) => r.request_id === record.request_id && r.attempted)) {
      const recovered = await http('/api/chat-jobs/' + record.request_id, {}, scope, signal);
      checkJob(recovered, record);
      update(record, scope, { id: recovered.id, phase: 'streaming', status: recovered.status });
      return;
    }
    if (record.payload_ref) {
      if (!payloadStore) throw new PendingChatJobError('Armazenamento do pedido indisponível.');
      record.payload = JSON.parse(await payloadStore.get(scope.owner, 'payload', record.payload_ref));
      check(scope);
    }
    if (!record.payload) throw new PendingChatJobError('Pedido sem corpo local; recupere-o pela lista do servidor.');
    if (record.payload.account !== scope.owner || record.payload.request_id !== record.request_id) throw detached();
    const fullJSON = JSON.stringify(record.payload);
    const prepared = byteTransport
      ? await byteTransport.prepare(new TextEncoder().encode(fullJSON)) : { body: fullJSON };
    check(scope);
    if (signal?.aborted) throw detached();
    if (read(scope.owner).some((r) => r.request_id === record.request_id && r.attempted)) {
      throw new PendingChatJobError('O envio deste pedido já foi iniciado; recupere-o pelo identificador.', { noRetry: true });
    }
    update(record, scope, { attempted: true });
    const response = await http('/api/chat-jobs', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: prepared.body,
    }, scope, signal);
    checkJob(response, record);
    update(record, scope, { id: response.id, phase: 'streaming', status: response.status });
    onSubmitted(copy(record));
  }
  async function cancel(record) {
    const scope = context();
    assertRecord(record, scope);
    update(record, scope, { cancel_requested: true }); // Only explicit user actions call this.
    if (!record.attempted && !record.id) {
      update(record, scope, { status: 'cancelled', local_cancel: true });
      return;
    }
    // The implemented server uses request_id as its job ID. Never resubmit a
    // possibly unsent inference just to cancel it; retry only the cancel action.
    const response = await post('/api/chat-jobs/' + (record.id || record.request_id) + '/cancel', {}, scope);
    checkJob(response, record);
    update(record, scope, { id: response.id, status: response.status });
  }

  async function* stream(record, { signal } = {}) {
    const scope = context();
    assertRecord(record, scope);
    if (record.status === 'expired') throw new TerminalChatJobError('expired', 'Esta resposta temporária expirou. Nenhum novo pedido foi enviado.');
    if (record.local_cancel) throw new TerminalChatJobError('cancelled', 'Pedido cancelado antes do envio.');
    if (record.cancel_requested) await cancel(record);
    else {
      if (record.id) await verifyAccount(scope, signal);
      try { await submit(record, scope, signal); }
      catch (error) {
        // Only a verified local intent with no attempt can mean not submitted.
        try {
          if (!error.detached && current(scope) && !record.id && !record.attempted &&
              read(scope.owner).some(r => r.request_id === record.request_id && r.attempted === false)) error.notSubmitted = true;
        } catch (_) { /* Unreadable intent is uncertainty, never permission to retry. */ }
        throw error;
      }
    }
    if (record.local_cancel) throw new TerminalChatJobError('cancelled', 'Pedido cancelado antes do envio.');
    let cursor = 0, sawDone = false, sawError = false;
    // Every resumed observer replays from zero into a fresh UI buffer. No partial
    // answer is persisted as final and no replay appends to an earlier draft.
    while (true) {
      check(scope);
      let page;
      try { page = await http('/api/chat-jobs/' + record.id + '?after=' + cursor, {}, scope, signal,
        { kind: 'page', job_id: record.id, after: cursor }); }
      catch (error) {
        if (error instanceof TerminalChatJobError && error.status === 'expired') update(record, scope, { status: 'expired' });
        throw error;
      }
      checkJob(page, record);
      if (!Array.isArray(page.events) || !Number.isSafeInteger(page.cursor) || typeof page.has_more !== 'boolean') {
        throw new PendingChatJobError('Página de eventos inválida; a resposta continua pendente.');
      }
      const previous = cursor;
      for (const event of page.events) {
        if (!event || !Number.isSafeInteger(event.seq) || event.seq <= 0 || typeof event.data !== 'string') {
          throw new PendingChatJobError('Evento inválido; a resposta continua pendente.');
        }
        if (event.seq <= cursor) continue;
        const data = event.data.trim();
        let parsed = null;
        if (data !== '[DONE]') {
          try { parsed = JSON.parse(data); } catch (_) { throw new PendingChatJobError('Evento de resposta ilegível; entrega suspensa.'); }
        }
        const withdrawn = parsed?.iald_aviso?.retirar_resposta === true;
        if (event.seq !== cursor + 1 && !withdrawn) throw new PendingChatJobError('Faltam eventos da resposta; retomaremos a leitura integral.');
        cursor = event.seq;
        // Moderation deliberately removes prior durable events. Only the explicit
        // withdrawal event may bridge that gap; the UI discards all earlier text.
        if (withdrawn) { sawDone = false; sawError = false; }
        if (data === '[DONE]') { sawDone = true; continue; }
        if (sawDone) throw new PendingChatJobError('Há eventos após a conclusão; entrega suspensa.');
        if (parsed?.error) sawError = true;
        yield 'data: ' + event.data;
        check(scope);
      }
      if (page.cursor !== cursor || (page.has_more && cursor === previous)) {
        throw new PendingChatJobError('Cursor de recuperação inconsistente; entrega suspensa.');
      }
      update(record, scope, { status: page.status });
      if (page.has_more) continue; // Drain all pages immediately before checking completion.
      if (TERMINAL_JOB_STATUSES.has(page.status)) {
        if (page.status !== 'completed' || sawError) {
          throw new TerminalChatJobError(page.status === 'completed' ? 'failed' : page.status,
            page.status === 'cancelled' ? 'Resposta interrompida a seu pedido.'
              : 'A geração não concluiu. O pedido não foi reenviado automaticamente.');
        }
        if (!sawDone) throw new PendingChatJobError('Conclusão sem marcador final; a resposta permanece pendente.');
        yield 'data: [DONE]';
        return;
      }
      await sleep(1000, signal);
    }
  }

  async function discover(hasConversation) {
    const scope = context();
    await verifyAccount(scope);
    const response = await http('/api/chat-jobs', {}, scope);
    if (response?.account !== scope.owner) loseScope();
    if (!response || !Array.isArray(response.jobs)) throw new PendingChatJobError('Lista de respostas inválida.');
    const records = read();
    for (const job of response.jobs) {
      if (!job || !UUID.test(job.id) || !STATUSES.has(job.status) || typeof job.conversation_id !== 'string') {
        throw new PendingChatJobError('Identidade inválida na lista de respostas.');
      }
      if (!hasConversation(job.conversation_id, scope.owner)) continue;
      let record = records.find((r) => r.id === job.id || r.request_id === job.id);
      if (record) {
        if (record.conversation_id !== job.conversation_id) throw new PendingChatJobError('Conversa de recuperação inconsistente.');
        record.id = job.id; record.status = job.status;
      } else {
        record = { owner: scope.owner, request_id: job.id, id: job.id, conversation_id: job.conversation_id,
          payload: null, phase: 'streaming', attempted: true, cancel_requested: false, status: job.status,
          created: typeof job.created === 'number' ? job.created * 1000 : Date.now() };
        records.push(record);
      }
    }
    write(records, scope);
    return records.filter((r) => hasConversation(r.conversation_id, scope.owner));
  }
  async function acknowledge(record) {
    const scope = context();
    assertRecord(record, scope);
    if (record.phase !== 'saved') throw new PendingChatJobError('A resposta precisa ser salva antes da confirmação de entrega.');
    if (!record.local_cancel && record.status !== 'expired') await post('/api/chat-jobs/' + record.id + '/ack', {}, scope);
    write(read().filter((r) => r.request_id !== record.request_id), scope);
    if (payloadStore && record.payload_ref) {
      try { await payloadStore.remove(scope.owner, 'payload', record.payload_ref); }
      catch (_) { onPending('Entrega confirmada; limpeza local do corpo ainda pendente.'); }
    }
  }
  async function delivered(record, save) {
    const scope = context();
    assertRecord(record, scope);
    await save(); // Must throw if conversation persistence failed.
    check(scope);
    update(record, scope, { phase: 'saved', payload: null });
    await acknowledge(record);
  }
  function pause() {
    byteTransport = null;
    generation += 1;
    for (const controller of active) controller.abort();
  }
  async function purgeConversation(conversation) {
    const scope = context();
    if (!/^[A-Za-z0-9_-]{1,64}$/.test(conversation)) throw new Error('Conversa inválida.');
    await post('/api/chat-jobs/conversations/' + encodeURIComponent(conversation) + '/delete', {}, scope);
    write(read().filter((r) => r.conversation_id !== conversation), scope);
  }
  return {
    begin, stream, cancel, discover, acknowledge, delivered, purgeConversation,
    pending: () => owner ? read() : [],
    owner: () => owner,
    pause,
    setOwner(account) {
      if (typeof account !== 'string' || !ACCOUNT.test(account)) account = '';
      if (account !== owner) { pause(); owner = account; }
    },
    forgetOwner() {
      const scope = context();
      storage.removeItem(key(scope.owner));
      pause(); owner = '';
    },
    report(error) { if (!error.detached) onPending(error.message); },
  };
}

// Called only after a complete stream, never by a network-error finally block.
// The job marker and the message/notice are one conversation-storage transaction.
function applyChatJobDelivery(conversation, job, { answer = null, notice = null, status = 'completed' }) {
  if (conversation.id !== job.conversation_id) throw new Error('Conversa de origem divergente.');
  const id = job.id || job.request_id;
  conversation.chat_job_deliveries ||= {};
  if (conversation.chat_job_deliveries[id]) return false;
  if (answer && !conversation.mensagens.some((m) => m.chat_job_id === id)) {
    conversation.mensagens.push({ ...answer, chat_job_id: id });
  }
  conversation.chat_job_deliveries[id] = { status, notice, at: new Date().toISOString() };
  conversation.atualizada = new Date().toISOString();
  return true;
}

const NativePushSidecar = (() => {
/** Native-only notifications. No fetch, storage, provider credentials or job execution.
 * Dependencies must be bound to ONE authenticated backend binding; see CONTRACT.md.
 */
const ID = /^[A-Za-z0-9_-]{1,128}$/;
const CHANNEL_ID = 'iald_responses_v1';
const EVENT = 'iald.response_ready';

function parseNotification(data, bindingId) {
  if (!data || typeof data !== 'object' || Array.isArray(data) ||
      data.schema_version !== '1' || data.event !== EVENT ||
      data.binding_id !== bindingId || !ID.test(data.event_id ?? '') ||
      !ID.test(data.job_id ?? '') || typeof data.event_id !== 'string' ||
      typeof data.job_id !== 'string') return null;
  // Deliberately discard URLs, titles, text, owner IDs and every other field.
  return { eventId: data.event_id, jobId: data.job_id };
}

function nativePlugins(capacitor = globalThis.Capacitor) {
  if (!capacitor?.isNativePlatform?.() ||
      !['ios', 'android'].includes(capacitor.getPlatform()) ||
      !capacitor.isPluginAvailable('PushNotifications') ||
      !capacitor.isPluginAvailable('App')) throw new Error('native_push_unavailable');
  return {
    platform: capacitor.getPlatform(),
    push: capacitor.registerPlugin('PushNotifications'),
    app: capacitor.registerPlugin('App'),
    readiness: capacitor.isPluginAvailable('IaldPushReadiness')
      ? capacitor.registerPlugin('IaldPushReadiness') : undefined,
  };
}

function createNativeNotifications({ push, app, platform, bindingId,
  api, openJob, onStatus = () => {}, timeoutMs = 15000 }) {
  if (!['ios', 'android'].includes(platform) || typeof bindingId !== 'string' ||
      !ID.test(bindingId) || !Number.isInteger(timeoutMs) || timeoutMs < 1 ||
      timeoutMs > 60000 || !push?.addListener || !app?.addListener ||
      !['saveToken', 'revoke', 'getJob', 'reconcile'].every(k => typeof api?.[k] === 'function') ||
      typeof openJob !== 'function') throw new Error('invalid_notification_configuration');

  let active = false, started = false, state = 'idle', stopPromise;
  let operation = Promise.resolve(), writes = Promise.resolve();
  let lastSavedToken = null;
  const abort = new AbortController(), handles = [], seen = new Set(), opening = new Set();
  const tasks = new Set();
  const status = next => {
    state = next;
    try { onStatus({ state: next }); } catch { /* UI cannot leak or break cleanup. */ }
    return { state: next };
  };
  const bounded = work => new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('notification_timeout')), timeoutMs);
    Promise.resolve().then(work).then(resolve, reject).finally(() => clearTimeout(timer));
  });
  const guarded = (fn, failure) => {
    const task = Promise.resolve().then(fn).catch(() => {
      if (active) status(failure);
    });
    tasks.add(task);
    task.finally(() => tasks.delete(task));
    return task;
  };
  const serial = fn => {
    operation = operation.then(fn, fn).catch(() => active ? status('operation_failed') : { state });
    return operation;
  };
  const options = () => ({ bindingId, signal: abort.signal });

  function saveToken(value) {
    const valid = typeof value === 'string' && (platform === 'ios'
      ? /^[A-Fa-f0-9]{32,512}$/.test(value) && value.length % 2 === 0
      : /^[A-Za-z0-9_:.-]{16,4096}$/.test(value));
    if (!active) return;
    if (!valid) { status('invalid_token'); return; }
    writes = writes.then(async () => {
      if (!active || value === lastSavedToken) return;
      await bounded(() => api.saveToken({ ...options(), token: value,
        provider: platform === 'ios' ? 'apns' : 'fcm' }));
      if (active) { lastSavedToken = value; status('registered'); }
    }).catch(() => { if (active) status('token_sync_failed'); });
  }

  async function openNotification(action) {
    if (!active || action?.actionId !== 'tap') return;
    const event = parseNotification(action.notification?.data, bindingId);
    if (!event || seen.has(event.eventId) || opening.has(event.eventId)) return;
    if (opening.size >= 16) { status('notification_busy'); return; }
    opening.add(event.eventId);
    try {
      const job = await bounded(() => api.getJob({ ...options(), jobId: event.jobId }));
      // The authenticated endpoint enforces ownership. Payload never authorizes access.
      if (!active) return;
      if (!job || job.id !== event.jobId || job.state !== 'completed' ||
          typeof job.conversationId !== 'string' || !/^[A-Za-z0-9_-]{1,64}$/.test(job.conversationId)) {
        status('response_unavailable'); return;
      }
      await bounded(() => openJob({ jobId: event.jobId, conversationId: job.conversationId,
        signal: abort.signal }));
      if (!active) return;
      seen.add(event.eventId);
      if (seen.size > 128) seen.delete(seen.values().next().value);
      status('response_opened');
    } finally { opening.delete(event.eventId); }
  }

  async function add(plugin, name, callback) {
    // If teardown races a delayed listener creation, remove that late handle too.
    const pending = Promise.resolve().then(() => plugin.addListener(name, callback));
    pending.then(handle => {
      if (active) handles.push(handle);
      else Promise.resolve().then(() => handle.remove()).catch(() => {});
    }, () => {});
    await bounded(() => pending);
  }

  async function register(prompt) {
    if (!active) return { state };
    let permission = await bounded(() => push.checkPermissions());
    if (!active) return { state };
    if (prompt && ['prompt', 'prompt-with-rationale'].includes(permission?.receive)) {
      permission = await bounded(() => push.requestPermissions());
    }
    if (!active) return { state };
    if (permission?.receive !== 'granted') return status(
      permission?.receive === 'denied' ? 'permission_denied' : 'permission_required');
    status('awaiting_token');
    await bounded(() => push.register());
    return { state };
  }

  async function resume() {
    if (!active) return;
    // Always reconcile durable jobs, including when push is denied or lost.
    await bounded(() => api.reconcile(options()));
    if (active) await register(false);
  }

  async function cleanup() {
    const results = await Promise.allSettled(handles.splice(0).map(h => bounded(() => h.remove())));
    return results.every(r => r.status === 'fulfilled');
  }

  return {
    start() {
      if (started || stopPromise) return operation.then(() => ({ state }));
      started = true; active = true;
      return serial(async () => {
        try {
          // Capacitor retains a cold-start tap until this listener is attached.
          await add(push, 'pushNotificationActionPerformed', action =>
            guarded(() => openNotification(action), 'response_open_failed'));
          if (!active) return { state };
          await add(push, 'registration', token => saveToken(token?.value));
          await add(push, 'registrationError', () => { if (active) status('registration_failed'); });
          await add(push, 'pushNotificationReceived', notification => {
            if (active && parseNotification(notification?.data, bindingId))
              guarded(() => bounded(() => api.reconcile(options())), 'reconcile_failed');
          });
          await add(app, 'appStateChange', change => {
            if (active && change?.isActive === true)
              guarded(() => serial(resume), 'resume_failed');
          });
          if (active) await resume();
          return { state };
        } catch {
          if (active) status('startup_failed');
          return { state };
        }
      });
    },
    enable() {
      // Call ONLY from the authenticated user's explicit enable-notifications gesture.
      return serial(async () => {
        if (!active || !started) return { state };
        try { return await register(true); }
        catch { return active ? status('registration_failed') : { state }; }
      });
    },
    stop() {
      if (stopPromise) return stopPromise;
      active = false; abort.abort(); lastSavedToken = null;
      // Revoke immediately; a backend tombstone rejects already-in-flight token writes.
      const revocation = bounded(() => api.revoke({ bindingId })).then(() => true, () => false);
      stopPromise = serial(async () => {
        const removed = await cleanup();
        let unregistered = true;
        try { await bounded(() => push.unregister()); } catch { unregistered = false; }
        try { await bounded(() => push.removeAllDeliveredNotifications()); }
        catch { unregistered = false; }
        seen.clear(); opening.clear();
        const revoked = await revocation;
        return status(!revoked ? 'revocation_pending' :
          !removed || !unregistered ? 'native_cleanup_failed' : 'stopped');
      });
      return stopPromise;
    },
    getState() { return { state }; },
    async settled() { // Bounded local queues, useful for host coordination and fake tests.
      await operation; await writes; await Promise.allSettled([...tasks]);
      return { state };
    },
  };
}


const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;

/** Call from the authenticated host after a user gesture (or restored explicit opt-in).
 * requestJSON is the existing app's HTTPS/auth/CSRF adapter; it must reject non-2xx,
 * support AbortSignal, and have its own timeout. Do not create another auth mechanism.
 * installationId is a random, persistent local UUID, never a user name or credential.
 */
async function connectNotifications({ requestJSON, installationId, consent,
  openJob, onJobs, onStatus, plugins, nativeReady = false, prompt = false }) {
  if (consent !== true || !UUID.test(installationId ?? '') ||
      typeof requestJSON !== 'function' || typeof onJobs !== 'function')
    throw new Error('notification_opt_in_required');
  const disabled = () => ({ state: 'configuration_disabled' });
  const inactive = { getState: disabled, start: async () => disabled(), enable: async () => disabled(),
    stop: async () => disabled(), settled: async () => disabled() };
  // Rollout flag is false by default. Do not even load/register a native plugin until ready.
  if (nativeReady !== true) return inactive;
  plugins ??= nativePlugins();
  if (plugins.platform === 'android') {
    let readiness;
    try { readiness = await plugins.readiness?.getStatus(); }
    catch { return inactive; }
    if (readiness?.ready !== true) return inactive;
  }
  let binding;
  try {
    binding = await requestJSON('/api/native-push/bindings', { method: 'POST',
      body: { installation_id: installationId, platform: plugins.platform, consent: true } });
  } catch { throw new Error('notification_binding_failed'); }
  if (!binding || !UUID.test(binding.id ?? '') || binding.revoked !== false ||
      binding.platform !== plugins.platform) throw new Error('invalid_notification_binding');
  const path = '/api/native-push/bindings/' + binding.id;
  const api = {
    saveToken: ({ token, provider, signal }) => requestJSON(path + '/token', {
      method: 'PUT', body: { token, provider }, signal }),
    revoke: () => requestJSON(path, { method: 'DELETE', body: {} }),
    getJob: async ({ jobId, signal }) => {
      const job = await requestJSON('/api/chat-jobs/' + encodeURIComponent(jobId), { method: 'GET', signal });
      return { id: job?.id, state: job?.status, conversationId: job?.conversation_id };
    },
    reconcile: async ({ signal }) => {
      const result = await requestJSON('/api/chat-jobs', { method: 'GET', signal });
      if (signal.aborted) return;
      if (!Array.isArray(result?.jobs)) throw new Error('invalid_jobs_response');
      await onJobs(result.jobs, { signal });
    },
  };
  const controller = createNativeNotifications({ ...plugins, bindingId: binding.id,
    api, openJob, onStatus });
  const initial = await controller.start();
  if (initial.state === 'startup_failed') {
    await controller.stop();
    throw new Error('notification_startup_failed');
  }
  if (prompt) await controller.enable();
  return controller;
}
// Dependency-injected settings lifecycle; tokens stay in memory only.
function createNotificationSettings({ connect, storage, identity, platform,
  requestFor, openJob, onJobs, onChange, randomUUID }) {
  let epoch = 0, controller = null, tail = Promise.resolve(), lastScope = '';
  let revokedScope = '';
  let view = { configured: false, wanted: false, busy: false, state: 'signed_out' };
  const key = account => 'iald_native_push_opt_in_v1:' + account;
  const publish = change => {
    view = { ...view, ...change };
    try { onChange({ ...view }); } catch { /* UI errors cannot expose request data. */ }
    return { ...view };
  };
  const valid = value => value && /^[a-f0-9]{64}$/.test(value.account) &&
    typeof value.token === 'string' && value.token.length > 0;
  const current = (snapshot, version) => {
    const now = identity();
    return version === epoch && valid(now) && now.account === snapshot.account && now.token === snapshot.token;
  };
  const queue = fn => {
    tail = tail.then(fn, fn).catch(() => publish({ busy: false, state: 'unavailable' }));
    return tail;
  };
  const stop = async () => {
    const previous = controller; controller = null;
    return previous ? previous.stop() : { state: 'stopped' };
  };
  const revokeSession = async snapshot => {
    if (!valid(snapshot)) return { state: 'stopped' };
    const scope = snapshot.account + ':' + snapshot.token;
    if (scope === revokedScope) return { state: 'stopped' };
    try {
      const result = await requestFor(snapshot.token)('/api/native-push/revoke-session', { method: 'POST', body: {} });
      if (result?.revoked !== true) throw new Error();
      revokedScope = scope;
      return { state: 'stopped' };
    } catch { return { state: 'revocation_pending' }; }
  };
  function installation() {
    const idKey = 'iald_native_push_installation_v1';
    let value = storage.getItem(idKey);
    if (value == null) { value = randomUUID(); storage.setItem(idKey, value); }
    if (!/^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$/.test(value) || storage.getItem(idKey) !== value)
      throw new Error('notification_storage_failed');
    return value;
  }
  async function run(force, prompt) {
    const snapshot = identity(), version = epoch;
    if (!valid(snapshot)) { await stop(); lastScope = ''; return publish({ configured: false, wanted: false, busy: false, state: 'signed_out' }); }
    const scope = snapshot.account + ':' + snapshot.token; // Never persisted or returned.
    if (!force && scope === lastScope) return { ...view };
    if (lastScope && scope !== lastScope) await stop();
    if (!current(snapshot, version)) return { ...view };
    lastScope = scope;
    const wanted = storage.getItem(key(snapshot.account)) === '1';
    publish({ busy: true, wanted });
    const requestJSON = requestFor(snapshot.token);
    const readiness = await requestJSON('/api/native-push/status', { method: 'GET' });
    if (!current(snapshot, version)) return { ...view };
    const configured = readiness?.[platform()] === true;
    if (!configured || !wanted) {
      const result = await stop();
      if (!current(snapshot, version)) return { ...view };
      return publish({ configured, wanted, busy: false, state: result.state === 'revocation_pending'
        ? result.state : configured ? 'off' : 'configuration_disabled' });
    }
    publish({ configured: true, busy: true });
    if (!controller) {
      revokedScope = '';
      const next = await connect({ requestJSON, installationId: installation(), consent: true,
        nativeReady: true, prompt,
        openJob: async data => { if (current(snapshot, version) && !data.signal?.aborted) await openJob(data, snapshot.account); },
        onJobs: async (jobs, options) => { if (current(snapshot, version) && !options.signal?.aborted) await onJobs(jobs); },
        onStatus: result => { if (current(snapshot, version)) publish({ state: result.state }); },
      });
      if (!current(snapshot, version)) { await next.stop(); return { ...view }; }
      controller = next;
    } else if (prompt) await controller.enable();
    const result = controller.getState();
    if (result.state === 'configuration_disabled') { controller = null; return publish({ configured: false, busy: false, state: result.state }); }
    return publish({ busy: false, state: result.state });
  }
  return {
    refresh(force = false) { return queue(() => run(force, false)); },
    toggle(enabled) {
      const snapshot = identity();
      if (!valid(snapshot) || typeof enabled !== 'boolean') return Promise.resolve({ ...view });
      // Preference is per authenticated opaque account. New accounts are always opted out.
      try {
        storage.setItem(key(snapshot.account), enabled ? '1' : '0');
        if (storage.getItem(key(snapshot.account)) !== (enabled ? '1' : '0')) throw new Error();
      } catch { return Promise.resolve(publish({ state: 'storage_unavailable', busy: false })); }
      if (!enabled) {
        epoch++; // Invalidate in-flight taps immediately, before queued teardown.
        const closing = stop();
        publish({ wanted: false, busy: true });
        return queue(async () => {
          await closing;
          const result = await revokeSession(snapshot);
          return publish({ wanted: false, busy: false, state: result.state === 'stopped' ? 'off' : result.state });
        });
      }
      return queue(() => run(true, enabled));
    },
    disconnect() {
      const snapshot = identity();
      epoch++; lastScope = '';
      publish({ configured: false, wanted: false, busy: false, state: 'signed_out' });
      // Keep the captured request adapter so DELETE uses the old bearer during logout.
      const closing = stop();
      return queue(async () => { await closing; return revokeSession(snapshot); });
    },
    getState() { return { ...view }; },
    settled() { return tail; },
  };
}

return { connectNotifications, createNotificationSettings };
})();


// ARTIFACT ACCESS MODULE BEGIN
// Embedded into iald.js. No storage, historical tickets, external assets or popup API.
const ARTIFACT_ORIGIN = 'https://demo.iald.ia.br';
const ARTIFACT_PREVIEW_CSP = "default-src 'none'; style-src 'unsafe-inline'; img-src data:; base-uri 'none'; form-action 'none'";
const ARTIFACT_PREVIEW_LAYOUT = ':root{overflow-wrap:anywhere}*,*::before,*::after{box-sizing:border-box}h1,h2,h3,h4,h5,h6,img,pre{max-width:100%}img{height:auto}pre{white-space:pre-wrap;overflow-wrap:anywhere}';
const ARTIFACT_UUID = /^[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$/i;
const ARTIFACT_ACCOUNT = /^[0-9a-f]{64}$/;
const artifactUUID = (value) => typeof value === 'string' && ARTIFACT_UUID.test(value) ? value.toLowerCase() : null;

function artifactURL(value, relative = false) {
  if (typeof value !== 'string' || value.length > 2048 || /[\s\\%]/u.test(value)
      || /\/(?:\.|\.\.)(?:\/|$|\?)/.test(value)) return null;
  if (!/^https:\/\//i.test(value) && !(relative && /^\/(?!\/)/.test(value))) return null;
  try {
    const url = new URL(value, ARTIFACT_ORIGIN);
    return url.origin === ARTIFACT_ORIGIN && !url.username && !url.password && !url.hash ? url : null;
  } catch (_) { return null; }
}
function artifactIdFromSearch(search) {
  if (typeof search !== 'string' || search.length > 4096) return null;
  const ids = new URLSearchParams(search).getAll('artifact');
  return ids.length === 1 ? artifactUUID(ids[0]) : null;
}
function artifactIdFromURL(value) {
  const url = artifactURL(value, true);
  if (!url) return null;
  if (url.pathname === '/app/index.html') return artifactIdFromSearch(url.search);
  if (url.search) return null;
  const match = /^\/api\/task-artifacts\/([^/]+)$/.exec(url.pathname)
    || /^\/task-download\/([^/]+)\/[A-Za-z0-9_-]{43}$/.exec(url.pathname);
  return match ? artifactUUID(match[1]) : null; // The historical token is never returned.
}
function normalizeArtifactLinks(root) {
  for (const anchor of root.querySelectorAll('a[href]')) {
    const id = artifactIdFromURL(anchor.getAttribute('href'));
    if (!id) continue;
    anchor.setAttribute('href', ARTIFACT_ORIGIN + '/app/index.html?artifact=' + id);
    anchor.setAttribute('aria-haspopup', 'dialog');
  }
}
function validateArtifactMetadata(value, id) {
  if (!value || artifactUUID(value.id) !== id || typeof value.filename !== 'string'
      || !value.filename.trim() || value.filename.length > 255 || /[\x00-\x1f\x7f]/.test(value.filename)
      || typeof value.kind !== 'string' || !value.kind || value.kind.length > 40
      || !Number.isSafeInteger(value.bytes) || value.bytes < 0
      || typeof value.sha256 !== 'string' || !/^[0-9a-f]{64}$/i.test(value.sha256)
      || (value.preview_html != null && typeof value.preview_html !== 'string')) {
    throw new Error('Não foi possível conferir este arquivo.');
  }
  return { id, filename: value.filename, kind: value.kind, bytes: value.bytes, sha256: value.sha256,
    preview_html: value.kind === 'website' && typeof value.preview_html === 'string' && value.preview_html.length <= 2 * 1024 * 1024
      ? value.preview_html : null };
}
function validateArtifactAccess(value, id, now = Date.now()) {
  const checkURL = (raw, route) => {
    const url = artifactURL(raw);
    if (!url || url.search || !new RegExp('^/' + route + '/' + id + '/[A-Za-z0-9_-]{43}$').test(url.pathname)) {
      throw new Error('O endereço do arquivo não pôde ser conferido.');
    }
    return url.href;
  };
  if (!value || artifactUUID(value.id) !== id) throw new Error('O arquivo recebido não corresponde ao pedido.');
  const expires = typeof value.expires_at === 'number' ? value.expires_at * 1000
    : typeof value.expires_at === 'string' && /^\d{4}-\d\d-\d\dT.+(?:Z|[+-]\d\d:\d\d)$/.test(value.expires_at)
      ? Date.parse(value.expires_at) : NaN;
  if (!Number.isFinite(expires) || expires <= now) throw new Error('O link expirou. Prepare um novo link para continuar.');
  return { download_url: checkURL(value.download_url, 'task-download'),
    preview_url: value.preview_url == null ? null : checkURL(value.preview_url, 'task-view'), expires_at: expires };
}

const ARTIFACT_PREVIEW_TAGS = new Set(('a abbr b blockquote br caption code col colgroup dd del details div dl dt em figcaption figure footer h1 h2 h3 h4 h5 h6 header hr i img li main mark nav ol p pre s section small span strong style sub summary sup table tbody td tfoot th thead time tr u ul').split(' '));
const ARTIFACT_PREVIEW_ATTRIBUTES = new Set(('class id title lang dir style alt width height colspan rowspan scope start reversed open align valign border cellspacing cellpadding datetime').split(' '));
function sanitizeArtifactPreview(root, unsafeStyle) {
  for (const node of Array.from(root.querySelectorAll('*'))) {
    const tag = String(node.localName || '').toLowerCase();
    if ((node.namespaceURI && node.namespaceURI !== 'http://www.w3.org/1999/xhtml') || !ARTIFACT_PREVIEW_TAGS.has(tag)) {
      node.remove(); continue;
    }
    if (tag === 'style' && unsafeStyle(node.textContent)) { node.remove(); continue; }
    for (const attribute of Array.from(node.attributes)) {
      const name = attribute.name.toLowerCase(), value = attribute.value;
      if (name === 'src' && tag === 'img' && /^data:image\/(?:png|jpeg|jpg|gif|webp|bmp|avif);base64,[a-z0-9+/=\r\n]+$/i.test(value)) continue;
      if (name.includes(':') || !ARTIFACT_PREVIEW_ATTRIBUTES.has(name) || (name === 'style' && unsafeStyle(value))) node.removeAttribute(attribute.name);
    }
  }
}
function artifactPreviewDocument(html, document, unsafeStyle) {
  if (typeof html !== 'string' || html.length > 2 * 1024 * 1024) throw new Error('Prévia indisponível. Baixe o arquivo para abrir.');
  // Template parsing is inert. Neither the untrusted HTML nor its attributes enter
  // the parent document. Navigation, forms and remote resources are also stripped.
  const template = document.createElement('template');
  template.innerHTML = html;
  sanitizeArtifactPreview(template.content, unsafeStyle);
  return '<!doctype html><html><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="'
    + ARTIFACT_PREVIEW_CSP + '"><meta name="viewport" content="width=device-width, initial-scale=1"></head><body>'
    + template.innerHTML + '<style>' + ARTIFACT_PREVIEW_LAYOUT + '</style></body></html>';
}

function createArtifactAccessController({ request, identity, render = () => {}, onAuthLost = () => {},
  now = Date.now, initialSearch = '', requestTimeout = 20000 }) {
  let generation = 0, scope = null, opening = null, renewing = null;
  let launchId = artifactIdFromSearch(initialSearch);
  let state = { open: false, phase: 'closed', id: null, metadata: null, access: null, error: '', message: '' };
  const owner = () => { const value = identity() || {}; return { account: value.account || '', token: value.token || '' }; };
  const authenticated = (value) => ARTIFACT_ACCOUNT.test(value.account);
  const publish = (changes) => { state = { ...state, ...changes }; render({ ...state }); };
  const current = (captured) => captured && captured === scope && captured.generation === generation && !captured.controller.signal.aborted;
  function close() {
    launchId = null; generation++; scope?.controller.abort(); scope = null; opening = renewing = null;
    publish({ open: false, phase: 'closed', id: null, metadata: null, access: null, error: '', message: '' });
  }
  function check(captured) {
    if (!current(captured)) throw new Error('stale');
    const value = owner();
    if (!authenticated(value) || value.account !== captured.account || value.token !== captured.token) {
      close(); throw new Error('stale');
    }
  }
  async function read(path, options, captured) {
    check(captured);
    const controller = new AbortController();
    const abort = () => controller.abort();
    let timedOut = false;
    captured.controller.signal.addEventListener('abort', abort, { once: true });
    const timer = setTimeout(() => { timedOut = true; abort(); }, requestTimeout);
    try {
      const response = await request(path, { ...options, signal: controller.signal, cache: 'no-store' });
      check(captured);
      if (response.status === 401) { close(); onAuthLost(); throw new Error('stale'); }
      if (!response.ok) throw new Error(response.status === 403 || response.status === 404
        ? 'Arquivo não encontrado ou sem acesso nesta conta.' : 'Não foi possível abrir o arquivo agora. Tente novamente.');
      let value;
      try { value = await response.json(); } catch (_) { throw new Error('O servidor devolveu uma resposta inválida.'); }
      check(captured); return value;
    } catch (error) {
      check(captured);
      if (timedOut) throw new Error('O arquivo demorou para abrir. Tente novamente.');
      if (error instanceof TypeError || error?.name === 'AbortError') throw new Error('Sem conexão. Tente abrir o arquivo novamente.');
      throw error;
    } finally {
      clearTimeout(timer); captured.controller.signal.removeEventListener('abort', abort);
    }
  }
  function renew() {
    if (renewing) return renewing;
    const captured = scope;
    try { check(captured); } catch (_) { return Promise.resolve(false); }
    if (!state.metadata) return Promise.resolve(false);
    publish({ phase: 'preparing', access: null, error: '', message: 'Preparando os links…' });
    const pending = (async () => {
      try {
        const value = await read('/api/task-artifacts/' + state.id + '/access', {
          method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}',
        }, captured);
        const access = validateArtifactAccess(value, state.id, now());
        check(captured);
        publish({ phase: 'ready', access, message: 'Links prontos. Toque no botão para abrir.', error: '' });
        return true;
      } catch (error) {
        if (current(captured)) publish({ phase: 'ready', access: null, error: error.message, message: '' });
        return false;
      }
    })();
    renewing = pending;
    pending.finally(() => { if (renewing === pending) renewing = null; });
    return pending;
  }
  function open(value) {
    const id = artifactUUID(value);
    if (!id) return Promise.resolve(false);
    if (state.open && state.id === id && state.phase !== 'error') {
      try { check(scope); return opening || Promise.resolve(true); } catch (_) { /* New scope below. */ }
    }
    close(); // Also consumes a pending launch parameter; explicit clicks take precedence.
    const valueOwner = owner();
    if (!authenticated(valueOwner)) {
      publish({ open: true, id, phase: 'error', error: 'Entre na sua conta para abrir este arquivo.' });
      return Promise.resolve(false);
    }
    const captured = { ...valueOwner, generation, controller: new AbortController() };
    scope = captured;
    publish({ open: true, id, phase: 'loading', error: '', message: 'Abrindo arquivo…' });
    const pending = (async () => {
      try {
        const value = await read('/api/task-artifacts/' + id + '/view', { method: 'GET' }, captured);
        const metadata = validateArtifactMetadata(value, id);
        check(captured); publish({ metadata, phase: 'preparing' });
        return await renew();
      } catch (error) {
        if (current(captured)) publish({ phase: 'error', metadata: null, access: null, error: error.message, message: '' });
        return false;
      }
    })();
    opening = pending;
    pending.finally(() => { if (opening === pending) opening = null; });
    return pending;
  }
  function activate(action, event) {
    try { check(scope); } catch (_) { event.preventDefault(); return false; }
    const url = action === 'preview' ? state.access?.preview_url : state.access?.download_url;
    if (!url || state.access.expires_at <= now()) {
      event.preventDefault(); renew(); return false;
    }
    // Leave a validated, fresh anchor's normal navigation inside the user's gesture.
    return true;
  }
  return { open, close, reset: close, renew, activate, snapshot: () => ({ ...state }),
    authenticated() {
      if (!launchId || !authenticated(owner())) return Promise.resolve(false);
      const id = launchId; launchId = null; return open(id);
    },
    checkIdentity() { if (scope) { try { check(scope); } catch (_) { /* Cleared on mismatch. */ } } },
  };
}

const ARTIFACT_MODAL_STYLE = `
.iald-artifact-overlay{position:fixed;inset:0;z-index:20000;background:rgba(0,0,0,.55);display:flex;justify-content:center;align-items:center;padding:12px;padding:max(12px,env(safe-area-inset-top,0px)) max(12px,env(safe-area-inset-right,0px)) max(12px,env(safe-area-inset-bottom,0px)) max(12px,env(safe-area-inset-left,0px));box-sizing:border-box}
.iald-artifact-panel{box-sizing:border-box;width:100%;max-width:1000px;height:100%;max-height:900px;background:#fff;color:#172132;border-radius:18px;box-shadow:0 20px 70px #0005;display:flex;flex-direction:column;overflow:hidden;font:16px/1.45 system-ui,sans-serif}
.iald-artifact-head{display:flex;align-items:center;gap:12px;padding:12px 16px;border-bottom:1px solid #e1e5eb;flex-shrink:0}.iald-artifact-title{font-size:18px;margin:0;flex:1;overflow-wrap:anywhere;min-width:0}
.iald-artifact-content{flex:1;min-height:0;display:flex;flex-direction:column;overflow:auto;padding:12px 16px}.iald-artifact-meta{font-size:13px;color:#536077;margin:0 0 8px;overflow-wrap:anywhere}.iald-artifact-status{margin:0 0 10px}.iald-artifact-preview{display:block;flex:1;min-height:220px;width:100%;border:1px solid #dbe1e9;border-radius:8px;background:#fff}
.iald-artifact-actions{display:flex;gap:10px;flex-wrap:wrap;padding:12px 16px;border-top:1px solid #e1e5eb;flex-shrink:0}.iald-artifact-panel button,.iald-artifact-panel a{font:inherit;box-sizing:border-box;min-height:44px;padding:10px 14px;border-radius:10px;border:1px solid #cdd5e0;background:#f3f6fb;color:#16396d;text-decoration:none;cursor:pointer;text-align:center}.iald-artifact-panel [hidden]{display:none!important}.iald-artifact-panel [aria-disabled=true]{opacity:.55;cursor:wait}.iald-artifact-panel :focus-visible{outline:3px solid #1768d5;outline-offset:2px}
@media(max-width:600px){.iald-artifact-panel{border-radius:12px}.iald-artifact-actions a{flex:1}.iald-artifact-head,.iald-artifact-content,.iald-artifact-actions{padding:10px 12px}}
`;
function mountArtifactAccess({ document, window, request, identity, unsafeStyle, onAuthLost, initialSearch = '' }) {
  let modal = null, title, meta, status, preview, frame = null, frameId = null, download, browser, retry, closer, previousFocus;
  const node = (tag, className, text) => {
    const value = document.createElement(tag);
    if (className) value.className = className;
    if (text != null) value.textContent = text;
    return value;
  };
  function clearFrame() {
    if (frame) { frame.removeAttribute('srcdoc'); frame.remove(); }
    frame = null; frameId = null;
  }
  function createModal() {
    previousFocus = document.activeElement;
    modal = node('div', 'iald-artifact-overlay');
    const panel = node('section', 'iald-artifact-panel');
    panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-modal', 'true'); panel.setAttribute('aria-labelledby', 'iald-artifact-title');
    const head = node('header', 'iald-artifact-head');
    title = node('h2', 'iald-artifact-title', 'Arquivo'); title.id = 'iald-artifact-title';
    closer = node('button', '', 'Fechar'); closer.type = 'button'; closer.addEventListener('click', () => controller.close());
    head.appendChild(title); head.appendChild(closer); panel.appendChild(head);
    const content = node('div', 'iald-artifact-content');
    meta = node('p', 'iald-artifact-meta'); status = node('p', 'iald-artifact-status');
    status.setAttribute('role', 'status'); status.setAttribute('aria-live', 'polite');
    preview = node('div', 'iald-artifact-content');
    content.appendChild(meta); content.appendChild(status); content.appendChild(preview); panel.appendChild(content);
    const actions = node('footer', 'iald-artifact-actions');
    const link = (label, action) => {
      const anchor = node('a', '', label);
      anchor.target = '_blank'; anchor.rel = 'noopener noreferrer'; anchor.referrerPolicy = 'no-referrer';
      const activate = (event) => controller.activate(action, event);
      anchor.addEventListener('click', activate); anchor.addEventListener('auxclick', activate);
      actions.appendChild(anchor); return anchor;
    };
    download = link('Baixar arquivo', 'download'); browser = link('Abrir no navegador', 'preview');
    retry = node('button', '', 'Tentar novamente'); retry.type = 'button';
    retry.addEventListener('click', () => { const s = controller.snapshot(); if (s.metadata) controller.renew(); else controller.open(s.id); });
    actions.appendChild(retry); panel.appendChild(actions); modal.appendChild(panel);
    modal.addEventListener('click', (event) => { if (event.target === modal) controller.close(); });
    modal.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') { event.preventDefault(); event.stopPropagation(); controller.close(); }
      if (event.key === 'Tab') {
        const focusable = [closer, download, browser, retry].filter((element) => !element.hidden && (element.tagName !== 'A' || element.hasAttribute('href')));
        const first = focusable[0], last = focusable.at(-1);
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      }
    });
    document.body.appendChild(modal); closer.focus();
  }
  function render(state) {
    if (!state.open) {
      clearFrame();
      if (download) download.removeAttribute('href');
      if (browser) browser.removeAttribute('href');
      modal?.remove(); modal = null;
      if (previousFocus?.isConnected) previousFocus.focus();
      previousFocus = null; return;
    }
    if (!modal) createModal();
    title.textContent = state.metadata?.filename || 'Arquivo';
    meta.textContent = state.metadata ? state.metadata.bytes.toLocaleString('pt-BR') + ' bytes' : '';
    status.textContent = state.error || state.message;
    status.setAttribute('role', state.error ? 'alert' : 'status');
    if (!state.metadata || frameId !== state.id) { clearFrame(); preview.textContent = ''; }
    if (state.metadata && frameId !== state.id) {
      frameId = state.id;
      if (state.metadata.preview_html) {
        try {
          const srcdoc = artifactPreviewDocument(state.metadata.preview_html, document, unsafeStyle);
          frame = node('iframe', 'iald-artifact-preview');
          frame.setAttribute('sandbox', ''); frame.setAttribute('referrerpolicy', 'no-referrer');
          frame.setAttribute('title', 'Prévia do arquivo'); frame.setAttribute('srcdoc', srcdoc);
          preview.appendChild(frame);
        } catch (_) { preview.textContent = 'Prévia indisponível. Baixe o arquivo para abrir.'; }
      } else preview.textContent = 'Baixe o arquivo para abrir no seu aparelho.';
    }
    for (const [anchor, href] of [[download, state.access?.download_url], [browser, state.access?.preview_url]]) {
      anchor.removeAttribute('href'); anchor.hidden = !href;
      if (href) anchor.setAttribute('href', href);
    }
    retry.hidden = !state.error;
  }
  const controller = createArtifactAccessController({ request, identity, render, onAuthLost, initialSearch });
  if (!document.getElementById('iald-artifact-style')) {
    const style = node('style', '', ARTIFACT_MODAL_STYLE); style.id = 'iald-artifact-style'; document.head.appendChild(style);
  }
  const messages = document.getElementById('conversa-interna');
  const intercept = (event) => {
    const anchor = event.target?.closest?.('a[href]');
    if (!anchor || !messages?.contains(anchor)) return;
    const id = artifactIdFromURL(anchor.getAttribute('href'));
    if (!id) return;
    event.preventDefault(); event.stopPropagation(); controller.open(id);
  };
  messages?.addEventListener('click', intercept, true); messages?.addEventListener('auxclick', intercept, true);
  document.addEventListener('visibilitychange', () => controller.checkIdentity());
  window.addEventListener('storage', () => controller.checkIdentity());
  return controller;
}

// ARTIFACT ACCESS MODULE END

const VERSAO = 'IALD 4.1 · beta';

// β NUNCA literal (régua da casa): calculado em runtime a partir da constante de
// estrutura fina CODATA 2018. Conferido com node em 13/09/2026: 0.012031300400803142.
const ALPHA_FINE_CODATA_2018 = 7.2973525693e-3;
const BETA_TGL = ALPHA_FINE_CODATA_2018 * Math.sqrt(Math.E);

// Em file:// nao ha servidor; no resto e sempre mesma origem.
// Quando a UI for embarcada no Capacitor isto passa a apontar para o host
// remoto — e ai o servidor precisa de CORS + credenciais (ainda NAO tem).
// Host remoto usado SÓ pelo invólucro nativo. No navegador é sempre mesma origem.
const HOST_REMOTO = 'https://demo.iald.ia.br';
// BASE é definido logo abaixo de SUPERFICIE — ele depende dela, e uma const não
// pode ser lida antes de ser inicializada.

const DEMO = new URLSearchParams(location.search).has('demo');

// Superfície: 'app' quando roda dentro do invólucro nativo, 'web' no navegador.
// O servidor filtra as ferramentas por este campo — o build das lojas não recebe
// `request_contract`, porque contratação comercial dentro do aplicativo é o que
// a Guideline 3.1.1 proíbe e o que reprovou a submissão em 23/03/2026.
// `?loja=1` força o modo app no navegador, para conferir sem compilar nada.
const SUPERFICIE = (() => {
  try {
    if (new URLSearchParams(location.search).get('loja') === '1') return 'app';
    if (window.Capacitor) return 'app';
    if (location.protocol === 'capacitor:' || location.protocol === 'ionic:') return 'app';
  } catch (e) { /* qualquer dúvida: web, que é o conjunto completo */ }
  return 'web';
})();

// Para onde as chamadas vão.
//   app  → host remoto. Dentro do APK a interface é EMBARCADA e location.origin
//          é `https://localhost`; sem isto o app tentaria falar consigo mesmo.
//   file → servidor local (abrir o arquivo direto no navegador, para depurar).
//   web  → mesma origem, como sempre.
const BASE = (SUPERFICIE === 'app') ? HOST_REMOTO
  : (location.protocol === 'file:') ? 'http://127.0.0.1:8082'
  : '';

// ── chaves de armazenamento local ──
const K = {
  conversas: 'iald_conversas_v2',
  ativa: 'iald_conversa_ativa_v2',
  config: 'iald_user_config',      // mesma chave do chat antigo: perfil migra sozinho
  tema: 'iald_tema',
  modo: 'iald_mode',               // idem
  token: 'iald_app_token',         // só no invólucro nativo (ver fetchIALD)
  pedido: 'iald_pedido_acesso',    // referência do pedido aguardando o operador (14/09)
  pedidoMotivo: 'iald_pedido_motivo', // "limite" = pedido nascido do limite de contas novas (14/09, noite)
  verificador: 'iald_verificador', // segredo da volta do navegador (uso único)
  usuario: 'iald_app_usuario',     // nome da conta devolvido na entrada (só exibição)
};

// ══════════════════════════════════════════════════════════════
// ESTADO
// ══════════════════════════════════════════════════════════════
const S = {
  conversas: [],
  ativaId: null,
  gerando: false,
  aborto: null,
  modo: 'fast',                    // 'fast' | 'think'
  busca: false,                    // lupa ligada: pede busca na internet na PRÓXIMA mensagem
  anexos: [],
  colarNoFim: true,
  perfil: { name: '', area: '', interests: '', context: '', style: 'equilibrado' },
  ctx: { n_ctx: 32768, margem: 0.92, reserva_resposta: 8192, cpt: 2.91, teto_mensagens: 400, carregado: false },
  servidor: { estado: 'checando', modelo: null },
  motor: null,                     // GET /api/motor: qual motor responde a esta conta (14/09/2026)
  trocandoMotor: false,            // POST /api/motor/escolha em curso (15/09/2026)
  avisoConsentimento: null,        // bolha do aviso que espera o "Concordo" para ser refeita
  consentimentoFolha: null,        // 21/09/2026: {provedor, versao} do texto que a folha mostra
  consentimentoOferecido: false,   // a folha de consentimento já abriu nesta entrada (não insistir)
  avisoLimite: null,               // aviso "limite" que abriu a folha de créditos (texto do servidor)
  denuncia: null,                  // {linha, resposta, pergunta} da resposta sendo denunciada
  motorCarregando: null,           // a leitura de /api/motor em curso (a folha de créditos espera o plano)
  saldo: null,                     // última leitura de /api/tgl/balance (repintada quando o plano chega)
  dicaImagem: false,               // o clipe foi tocado num plano sem imagem: a dica fica no compositor
};

// ══════════════════════════════════════════════════════════════
// UTILITARIOS
// ══════════════════════════════════════════════════════════════
const $ = (sel) => document.querySelector(sel);
const el = (tag, cls, txt) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (txt != null) n.textContent = txt;
  return n;
};
const num = (n) => (n || 0).toLocaleString('pt-BR');

function guardar(chave, valor) {
  try { localStorage.setItem(chave, typeof valor === 'string' ? valor : JSON.stringify(valor)); }
  catch (e) { /* modo privado / cota cheia: seguir sem quebrar */ }
}
function recuperar(chave, padrao) {
  try {
    const v = localStorage.getItem(chave);
    if (v == null) return padrao;
    if (typeof padrao === 'string') return v;
    return JSON.parse(v);
  } catch (e) { return padrao; }
}

// ══════════════════════════════════════════════════════════════
// A PORTA ÚNICA DE REDE
//
// No navegador: mesma origem, cookie de sessão, nada muda.
// No invólucro nativo: origem cruzada (`https://localhost` → demo.iald.ia.br),
// onde o cookie NÃO viaja. Aí vale o token assinado que /api/apple-signin
// devolve, no cabeçalho Authorization. O servidor aceita os dois caminhos.
//
// Por que UMA função e não `fetch` espalhado: se um só ponto esquecer o token,
// aquela chamada falha calada dentro do app — e é o tipo de defeito que só
// aparece com o aplicativo instalado num aparelho.
// ══════════════════════════════════════════════════════════════
function tokenApp() {
  return (SUPERFICIE === 'app') ? (recuperar(K.token, '') || '') : '';
}

export function guardarTokenApp(t) {
  if (tokenApp() !== (t || '')) desanexarRespostasBackground(true);
  guardar(K.token, t || '');
}

export function limparTokenApp() {
  desanexarRespostasBackground(true);
  sheetAfterRegistration = '';
  registrationIdentity?.reset();
  try { localStorage.removeItem(K.token); } catch (e) { /* modo privado */ }
}

async function fetchIALD(caminho, opcoes) {
  const o = Object.assign({}, opcoes || {});
  o.headers = Object.assign({}, o.headers || {});
  o.headers['X-IALD-Context'] = 'anthropic-native-v1';
  const t = tokenApp();
  if (t) o.headers['Authorization'] = 'Bearer ' + t;
  // 'include' é necessário em origem cruzada; em mesma origem equivale ao antigo
  // 'same-origin'. O servidor responde Allow-Credentials só às origens do invólucro.
  o.credentials = (SUPERFICIE === 'app') ? 'omit' : 'same-origin';
  const response = await fetch(BASE + caminho, o);
  if (response.status === 401 && SUPERFICIE === 'app' && t && tokenApp() === t) {
    limparTokenApp();
    avaliarPortao();
    erroDoPortao('Sua sessão expirou. Entre novamente para continuar.');
  }
  return response;
}

// Embedded into iald.js by build_client.py; this is not an extra served asset.
let backgroundOwner = '', backgroundEpoch = 0, backgroundRecovery = false;
let backgroundRecoveryAgain = false;
let backgroundTimer = null, backgroundNotice = '', activeBackgroundJob = null;
let backgroundNativeListening = false, backgroundNativeActive = null;
const backgroundHistoryKey = (owner) => 'iald_conversas_owner_v1:' + encodeURIComponent(owner);
const chatLocalStore = createChatLocalStore();
let backgroundHistoryWrites = Promise.resolve();
const backgroundJobs = createDurableChatJobs({
  request: fetchIALD, storage: localStorage, payloadStore: chatLocalStore,
  onPending: avisarBackground,
  onSubmitted: () => avisarBackground('A resposta continua no servidor. Você pode sair e voltar.'),
  onScopeLost: () => {
    desanexarRespostasBackground(true);
    avisarBackground('A sessão mudou. Entre na conta correta para recuperar suas respostas.');
  },
});

function avisarBackground(text) {
  if (text && text !== backgroundNotice) { backgroundNotice = text; avisar(text); }
}
function persistirConversasBackground() {
  if (!backgroundOwner) throw new PendingChatJobError('A conta precisa ser identificada antes de salvar.');
  mediaAssertHistory(S.conversas);
  const owner = backgroundOwner, epoch = backgroundEpoch;
  const key = backgroundHistoryKey(owner);
  const raw = JSON.stringify({ conversas: S.conversas, ativa: S.ativaId });
  const save = async () => {
    if (owner !== backgroundOwner || epoch !== backgroundEpoch) throw detached();
    const ref = await chatLocalStore.put(owner, 'history', raw);
    if (owner !== backgroundOwner || epoch !== backgroundEpoch) throw detached();
    const pointer = JSON.stringify({ chat_local_history_v1: ref });
    try {
      localStorage.setItem(key, pointer);
      if (localStorage.getItem(key) !== pointer) throw new Error();
    } catch (_) { throw new PendingChatJobError('Não foi possível registrar o histórico neste aparelho. A confirmação de entrega permanece bloqueada.'); }
  };
  // Snapshot at call time; serialize commits so an older async save cannot win.
  const result = backgroundHistoryWrites.catch(() => {}).then(save);
  backgroundHistoryWrites = result;
  return result;
}
function desanexarRespostasBackground(sair = false) {
  if (sair) { mediaDetach(); mediaCapsAccount = ''; }
  if (sair) artifactAccessUI?.reset();
  if (sair) disconnectNativeNotificationsUI();
  backgroundEpoch += 1;
  clearTimeout(backgroundTimer); backgroundTimer = null;
  backgroundJobs.pause();
  if (S.aborto) S.aborto.abort({ type: 'detach' });
  S.backgroundTurn = null; S.aborto = null; S.gerando = false;
  activeBackgroundJob = null;
  if (sair) {
    backgroundOwner = ''; backgroundJobs.setOwner('');
    S.conversas = []; S.ativaId = null;
    if ($('#conversa-interna')) { listarConversas(); abrirConversa(); }
  }
  if ($('#btn-enviar')) atualizarBotaoEnviar();
}

async function identificarContaBackground() {
  if (DEMO || portaoNecessario()) throw new PendingChatJobError('Entre para recuperar suas respostas.');
  const epoch = backgroundEpoch, token = tokenApp();
  // Only the authenticated, opaque server identity can scope pending payloads.
  const response = await fetchIALD('/api/chat-jobs/session', { cache: 'no-store', signal: AbortSignal.timeout(10000) });
  if (response.status === 401) { desanexarRespostasBackground(true); throw detached(); }
  const data = await response.json();
  if (epoch !== backgroundEpoch || token !== tokenApp()) throw detached();
  if (!response.ok || !/^[0-9a-f]{64}$/.test(data.account || '')) {
    throw new PendingChatJobError('Não foi possível confirmar a conta. O pedido não será enviado até a identificação voltar.');
  }
  const account = data.account;
  if (account !== backgroundOwner) {
    if (backgroundOwner) desanexarRespostasBackground(true);
    const loadEpoch = backgroundEpoch;
    const raw = localStorage.getItem(backgroundHistoryKey(account));
    let history;
    if (raw != null) {
      history = JSON.parse(raw);
      if (history?.chat_local_history_v1) {
        history = JSON.parse(await chatLocalStore.get(account, 'history', history.chat_local_history_v1));
        if (loadEpoch !== backgroundEpoch || token !== tokenApp()) throw detached();
      }
      if (!history || !Array.isArray(history.conversas)) throw new PendingChatJobError('Histórico desta conta ilegível.');
    } else {
      const legacyOwner = localStorage.getItem('iald_conversas_legacy_owner_v1');
      const legacy = !legacyOwner || legacyOwner === account ? recuperar(K.conversas, []) : [];
      history = { conversas: legacy, ativa: recuperar(K.ativa, '') };
      if (!Array.isArray(legacy)) throw new PendingChatJobError('Histórico local ilegível.');
      if (!legacyOwner) localStorage.setItem('iald_conversas_legacy_owner_v1', account);
    }
    backgroundOwner = account; backgroundJobs.setOwner(account);
    S.conversas = history.conversas.filter((c) => c && (!c.background_owner || c.background_owner === account));
    for (const c of S.conversas) c.background_owner = account;
    S.ativaId = S.conversas.some((c) => c.id === history.ativa) ? history.ativa : S.conversas[0]?.id || null;
    // Show the authenticated owner's history before asynchronous recovery.
    // Never leave the previously rendered generic/other-account list visible.
    listarConversas(); abrirConversa();
  }
  await mediaRecoverLegacyHistory(account);
  if (!S.conversas.length) novaConversa({ semFoco: true });
  else { listarConversas(); abrirConversa(); }
  refreshNativeNotificationsUI();
  artifactAccessUI?.authenticated();
  return backgroundOwner;
}

function corpoPedidoBackground(mensagens, selagem) {
  const modo = modoEfetivo();
  return {
    model: 'qwen3', messages: mensagens, max_tokens: modo === 'think' ? 8192 : 4096,
    temperature: 0.7, stream: true, iald_mode: modo, iald_surface: SUPERFICIE,
    iald_conv: String(selagem.conv), iald_selo_prev: selagem.prev || '',
  };
}
function conversaDoJob(job) {
  if (job.owner !== backgroundOwner) return null;
  return S.conversas.find((c) => c.id === job.conversation_id && c.background_owner === backgroundOwner) || null;
}
async function salvarEntregaBackground(job, answer, notice, status) {
  const c = conversaDoJob(job);
  if (!c) throw new PendingChatJobError('A conversa de origem não está disponível nesta conta.');
  await backgroundJobs.delivered(job, () => {
    applyChatJobDelivery(c, job, { answer, notice, status });
    return persistirConversasBackground(); // Mandatory verified history write before ack.
  });
}

function backgroundHidden() {
  // The native lifecycle can resume before WebView visibility catches up.
  return backgroundNativeActive === null ? document.hidden : !backgroundNativeActive;
}
function agendarRecuperacaoBackground() {
  if (backgroundTimer || backgroundHidden() || !backgroundOwner || portaoNecessario()) return;
  try { if (!backgroundJobs.pending().some((job) => conversaDoJob(job))) return; } catch (_) { return; }
  backgroundTimer = setTimeout(() => { backgroundTimer = null; recuperarRespostasBackground(); }, 1000);
}
async function recuperarRespostasBackground() {
  if (DEMO || backgroundHidden() || portaoNecessario() || S.gerando) return;
  if (backgroundRecovery) { backgroundRecoveryAgain = true; return; }
  backgroundRecovery = true;
  const epoch = backgroundEpoch;
  try {
    await identificarContaBackground();
    const records = await backgroundJobs.discover((id, owner) => S.conversas.some((c) => c.id === id && c.background_owner === owner));
    for (const job of records.sort((a, b) => a.created - b.created)) {
      if (backgroundHidden() || portaoNecessario() || S.gerando || job.owner !== backgroundOwner) break;
      const c = conversaDoJob(job);
      if (!c) continue;
      if (job.phase === 'saved' || c.chat_job_deliveries?.[job.id || job.request_id]) {
        await backgroundJobs.delivered(job, () => persistirConversasBackground());
        continue;
      }
      await transmitir(null, job);
      if (backgroundJobs.pending().some((r) => r.request_id === job.request_id)) break;
    }
  } catch (error) {
    if (epoch === backgroundEpoch) avisarBackground(error.message || 'Recuperação pendente; nenhuma nova geração foi iniciada.');
  } finally {
    backgroundRecovery = false;
    if (backgroundRecoveryAgain) { backgroundRecoveryAgain = false; recuperarRespostasBackground(); }
    agendarRecuperacaoBackground();
  }
}
function respostaPendenteBackground() {
  if (DEMO) return false;
  if (!backgroundOwner) { recuperarRespostasBackground(); return true; }
  const pending = backgroundJobs.pending().some((job) => job.conversation_id === S.ativaId && job.phase !== 'saved');
  if (pending) {
    avisarBackground('Esta conversa tem uma resposta pendente. Retomando o mesmo pedido.');
    recuperarRespostasBackground();
  }
  return pending;
}

async function apagarJobsDaConversa(id) {
  if (DEMO) return true;
  try {
    const owner = await identificarContaBackground();
    if (!S.conversas.some((c) => c.id === id && c.background_owner === owner)) throw new Error('Conversa indisponível nesta conta.');
    await backgroundJobs.purgeConversation(id);
    await mediaClearConversationLocal(owner, id);
    if (activeBackgroundJob?.conversation_id === id) desanexarRespostasBackground();
    return true;
  } catch (error) {
    avisarBackground(error.message || 'Não foi possível apagar a resposta no servidor. Tente novamente com conexão.');
    return false;
  }
}
function ligarRetomadaNativaBackground() {
  if (DEMO || SUPERFICIE !== 'app' || backgroundNativeListening) return;
  const App = plugin('App');
  if (!App || typeof App.addListener !== 'function') return;
  backgroundNativeListening = true;
  try {
    Promise.resolve(App.addListener('appStateChange', (state) => {
      if (typeof state?.isActive !== 'boolean') return;
      backgroundNativeActive = state.isActive;
      if (state.isActive) return recuperarRespostasBackground();
      desanexarRespostasBackground(); // Observing stops; only the Stop button cancels.
    })).catch(() => { backgroundNativeListening = false; backgroundNativeActive = null; });
  } catch (_) { backgroundNativeListening = false; backgroundNativeActive = null; }
}
function ligarRespostasBackground() {
  ligarRetomadaNativaBackground();
  document.addEventListener('visibilitychange', () => {
    if (backgroundHidden()) desanexarRespostasBackground();
    else recuperarRespostasBackground();
  });
  window.addEventListener('online', recuperarRespostasBackground);
  window.addEventListener('storage', (event) => {
    if (event.key === K.token || event.key === K.usuario) {
      desanexarRespostasBackground(true); recuperarRespostasBackground();
    }
  });
  const help = $('#folha-config .folha-corpo');
  if (help && !$('#ajuda-respostas-background')) {
    const note = el('p', 'ajuda', 'Respostas continuam no servidor quando você sai. As respostas temporárias são criptografadas e ficam disponíveis para recuperação por até 7 dias, apenas pela sua conta. Parar cancela a geração; sair da conta não cancela. Apagar a conversa ou limpar seu histórico também remove os eventos temporários do servidor.');
    note.id = 'ajuda-respostas-background'; help.appendChild(note);
  }
  recuperarRespostasBackground();
}

// Embedded in the staged iald.js. No additional static route or automatic permission prompt.
let nativeNotificationSettings = null;
let nativePushLogout = null;

function boundNativePushRequest(bearer) {
  return async (path, { method = 'GET', body, signal } = {}) => {
    if (!/^\/api\/(native-push\/(status|revoke-session|bindings(?:\/[A-Za-z0-9_-]+(?:\/token)?)?)|chat-jobs(?:\/[A-Za-z0-9_-]+)?)$/.test(path))
      throw new Error('notification_request_rejected');
    const abort = new AbortController();
    const cancel = () => abort.abort();
    if (signal?.aborted) cancel();
    signal?.addEventListener('abort', cancel, { once: true });
    const timer = setTimeout(cancel, 15000);
    try {
      const revoking = method === 'DELETE' || path === '/api/native-push/revoke-session';
      if (!revoking && tokenApp() !== bearer) throw new Error('notification_session_changed');
      // Capture the authenticated native token for this binding. A new user's token must
      // never replace it while an old binding is being revoked asynchronously.
      const response = await fetch(BASE + path, {
        method, credentials: 'omit', cache: 'no-store', redirect: 'error', signal: abort.signal,
        headers: { 'Authorization': 'Bearer ' + bearer, 'X-IALD-Context': 'anthropic-native-v1',
          'Accept': 'application/json', ...(body === undefined ? {} : { 'Content-Type': 'application/json' }) },
        ...(body === undefined ? {} : { body: JSON.stringify(body) }),
      });
      if (!response.ok || (!revoking && tokenApp() !== bearer)) throw new Error('notification_request_failed');
      return await response.json();
    } catch { throw new Error('notification_request_failed'); }
    finally { clearTimeout(timer); signal?.removeEventListener('abort', cancel); }
  };
}

function refreshNativeNotificationsUI(force = false) {
  if (nativeNotificationSettings) void nativeNotificationSettings.refresh(force);
}

function disconnectNativeNotificationsUI() {
  return nativeNotificationSettings ? nativeNotificationSettings.disconnect() : Promise.resolve({ state: 'stopped' });
}

function prepareNativePushLogout() {
  if (nativePushLogout) return nativePushLogout;
  nativePushLogout = (async () => {
    const result = await disconnectNativeNotificationsUI();
    if (result?.state === 'revocation_pending') {
      avisar('Não foi possível confirmar a saída dos avisos. Tente novamente com conexão.');
      return false;
    }
    return true;
  })().catch(() => false).finally(() => { nativePushLogout = null; });
  return nativePushLogout;
}

function startNativeNotificationsUI() {
  if (nativeNotificationSettings || DEMO || SUPERFICIE !== 'app' || !window.Capacitor?.isNativePlatform?.()) return;
  const platform = () => window.Capacitor.getPlatform();
  if (!['ios', 'android'].includes(platform())) return;
  const parent = $('#folha-config .folha-corpo');
  if (!parent) return;
  const label = document.createElement('label'); label.className = 'campo';
  const checkbox = document.createElement('input'); checkbox.type = 'checkbox';
  checkbox.id = 'cfg-native-response-notifications'; checkbox.disabled = true;
  checkbox.style.width = 'auto'; checkbox.style.marginRight = '8px';
  const caption = document.createElement('span'); caption.textContent = 'Avisar quando a resposta estiver pronta';
  const note = document.createElement('p'); note.id = 'native-response-notifications-status';
  note.className = 'ajuda'; note.setAttribute('role', 'status'); note.setAttribute('aria-live', 'polite');
  checkbox.setAttribute('aria-describedby', note.id);
  label.appendChild(checkbox); label.appendChild(caption); parent.appendChild(label); parent.appendChild(note);
  const messages = {
    signed_out: 'Entre na sua conta para ativar os avisos.',
    configuration_disabled: 'Os avisos ainda não estão disponíveis neste aparelho.',
    off: 'Avisos desativados. Sua resposta continua disponível ao voltar.',
    registered: 'Avisos ativados neste aparelho.',
    awaiting_token: 'Ativando avisos neste aparelho…',
    permission_required: 'Marque a opção para permitir avisos.',
    permission_denied: 'Para receber avisos, permita notificações nos ajustes do aparelho.',
    revocation_pending: 'Não foi possível confirmar a desativação. Tente novamente com conexão.',
    response_opened: 'Resposta pronta.',
    response_unavailable: 'Abra a conversa original para consultar sua resposta.',
    storage_unavailable: 'Não foi possível salvar esta preferência neste aparelho.',
  };
  nativeNotificationSettings = NativePushSidecar.createNotificationSettings({
    connect: NativePushSidecar.connectNotifications, storage: localStorage,
    identity: () => ({ account: backgroundOwner, token: tokenApp() }), platform,
    requestFor: boundNativePushRequest, randomUUID: () => crypto.randomUUID(),
    onJobs: () => { void recuperarRespostasBackground(); },
    openJob: async ({ conversationId, signal }, account) => {
      if (signal?.aborted || account !== backgroundOwner) return;
      const conversation = S.conversas.find(c => c.id === conversationId && c.background_owner === account);
      if (!conversation) throw new Error('response_unavailable');
      S.ativaId = conversation.id; salvarConversas(); abrirConversa(); fecharFolhas();
      void recuperarRespostasBackground();
    },
    onChange: state => {
      checkbox.checked = state.wanted;
      checkbox.disabled = state.busy || !backgroundOwner || !tokenApp() || (!state.configured && !state.wanted);
      note.textContent = state.busy ? 'Verificando avisos…' : messages[state.state] ||
        'Não foi possível atualizar os avisos. A resposta continua disponível ao voltar.';
    },
  });
  checkbox.addEventListener('change', () => { void nativeNotificationSettings.toggle(checkbox.checked); });
  document.addEventListener('visibilitychange', () => { if (!document.hidden) refreshNativeNotificationsUI(true); });
  window.addEventListener('online', () => refreshNativeNotificationsUI(true));
  refreshNativeNotificationsUI();
}


let artifactAccessUI = null;
function startArtifactAccessUI() {
  if (artifactAccessUI) return;
  artifactAccessUI = mountArtifactAccess({ document, window, request: fetchIALD,
    identity: () => ({ account: backgroundOwner, token: tokenApp() }),
    unsafeStyle: estiloPerigoso, initialSearch: location.search,
    onAuthLost: () => { desanexarRespostasBackground(true); avisar('Entre novamente para abrir o arquivo.'); },
  });
  artifactAccessUI.authenticated();
}

const svg = (d, w) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${w || 2}" stroke-linecap="round" stroke-linejoin="round"><path d="${d}"/></svg>`;
const ICONE = {
  copiar: 'M20 9h-9a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2v-9a2 2 0 0 0-2-2zM5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1',
  ok: 'M20 6L9 17l-5-5',
  editar: 'M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z',
  refazer: 'M1 4v6h6M23 20v-6h-6M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15',
  lixo: 'M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m3 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6',
  ouvir: 'M11 5L6 9H2v6h4l5 4V5zM15.54 8.46a5 5 0 0 1 0 7.07M19.07 4.93a10 10 0 0 1 0 14.14',
  pararAudio: 'M11 5L6 9H2v6h4l5 4V5zM23 9l-6 6M17 9l6 6',
  denunciar: 'M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1zM4 22v-7',
  ampulheta: 'M6 2h12M6 22h12M7 2v4a5 5 0 0 0 10 0V2M7 22v-4a5 5 0 0 1 10 0v4',
  alerta: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 8v4M12 16h.01',
  bloqueio: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM4.93 4.93l14.14 14.14',
  escudo: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z',
};

function aplicarPtbr(t) {
  if (!t) return t;
  const protectedParts = [];
  let prefix = 'IALDPTBRTOKEN';
  while (t.includes(prefix)) prefix += 'X';
  const pattern = /(`{3,}|~{3,})[^\n]*\n[\s\S]*?(?:\n\1[ \t]*(?=\n|$)|$)|(`+)[^\n]*?\2(?!`)|\\\[[\s\S]*?(?:\\\]|$)|\\\([\s\S]*?(?:\\\)|$)|\$\$[\s\S]*?(?:\$\$|$)|\$[^$\n]+\$/g;
  t = t.replace(pattern, (part) => { protectedParts.push(part); return `${prefix}${protectedParts.length - 1}END`; });
  for (const k in PTBR_FIXES) t = t.replace(new RegExp('\\b' + k + '\\b', 'g'), PTBR_FIXES[k]);
  return t.replace(new RegExp(`${prefix}(\\d+)END`, 'g'), (_, i) => protectedParts[+i]);
}

// ══════════════════════════════════════════════════════════════
// TEMA
// ══════════════════════════════════════════════════════════════
function aplicarTema(t) {
  document.documentElement.setAttribute('data-theme', t || '');
  guardar(K.tema, t || '');
  document.querySelectorAll('#opcoes-tema button').forEach((b) => {
    b.setAttribute('aria-pressed', String((b.dataset.tema || '') === (t || '')));
  });
  sincronizarBarraDeStatus();
}

function temaEscuroAtivo() {
  const t = document.documentElement.getAttribute('data-theme');
  if (t === 'dark') return true;
  if (t === 'light') return false;
  try { return window.matchMedia('(prefers-color-scheme: dark)').matches; } catch (e) { return false; }
}

// Barra de status do aparelho (relógio, bateria). A config nativa a deixava com
// texto escuro fixo — invisível sobre o portão azul-noite e sobre o tema escuro.
// Style 'DARK' = texto claro (para fundo escuro); 'LIGHT' = texto escuro.
function sincronizarBarraDeStatus() {
  try {
    const sb = window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.StatusBar;
    if (!sb || typeof sb.setStyle !== 'function') return;
    const portao = document.getElementById('portao');
    const fundoEscuro = (portao && !portao.hidden) || temaEscuroAtivo();
    const p = sb.setStyle({ style: fundoEscuro ? 'DARK' : 'LIGHT' });
    if (p && typeof p.catch === 'function') p.catch(() => {});
  } catch (e) { /* fora do invólucro: nada a fazer */ }
}

// ══════════════════════════════════════════════════════════════
// ORCAMENTO DE CONTEXTO
// Preserva o algoritmo do chat antigo (02/08/2026): o corte e por
// ORCAMENTO DE TOKENS medido, nao por "ultimas 10 mensagens". Antes disso
// ~100.000 tokens pagos em VRAM nunca eram usados.
// ══════════════════════════════════════════════════════════════
let contextoRequest = 0;
let motorRequest = 0;
function contextoNativo() {
  if (S.ctx.contagem_nativa_por_pedido_obrigatoria === true) return true;
  if (S.motor) return S.motor.motor_selecao === 'claude-haiku'
    || S.motor.modelo === 'claude-haiku-4-5-20251001';
  return S.ctx.contagem_nativa_por_pedido_obrigatoria === true;
}

async function carregarContexto() {
  const ticket = ++contextoRequest;
  try {
    const r = await fetchIALD('/api/contexto');
    if (ticket !== contextoRequest) return;
    if (!r.ok) throw new Error('context unavailable');
    const d = await r.json();
    if (ticket !== contextoRequest) return;
    S.ctx = { n_ctx: 32768, margem: 0.92, reserva_resposta: 8192,
      cpt: 2.91, teto_mensagens: 400, ...d, carregado: true };
  } catch (e) {
    if (ticket !== contextoRequest) return;
    S.ctx = { ...S.ctx, carregado: false };
  }
  atualizarDica();
}

function estimarTokens(c) {
  if (contextoNativo()) return null;
  if (c == null) return 0;
  if (typeof c === 'string') return Math.ceil(c.length / S.ctx.cpt);
  if (Array.isArray(c)) {
    let t = 0;
    for (const p of c) {
      if (p && p.type === 'text' && p.text) t += Math.ceil(p.text.length / S.ctx.cpt);
      else t += 400;   // imagem: o proprio llama-server contabiliza
    }
    return t;
  }
  return 0;
}

// ══════════════════════════════════════════════════════════════
// LIMITES DO PLANO (14/09/2026, noite) — campo `limites` de GET /api/motor
//
// Revisão de interface M4 e ordem-régua 6: a conta gratuita via a pílula "modo pensar"
// acender, a lupa ligar e a folha Ferramentas prometer "sempre" o que o servidor desliga
// calado (agente e pensar desligados no plano). A tela passa a ler o que o servidor
// declara: {agente, pensar, ferramentas: [nomes] | null, max_saida, janela}.
//   - servidor sem `limites` (anterior a esta rodada): nada muda na tela;
//   - ferramentas null: todas as da superfície;
//   - a preferência de modo gravada no aparelho NÃO é apagada: se o plano mudar, ela volta.
// ══════════════════════════════════════════════════════════════
function limitesDoPlano() {
  const l = S.motor && S.motor.limites;
  return (l && typeof l === 'object') ? l : null;
}

function planoDaConta() {
  const m = S.motor || {};
  return String(m.plano || (m.cota && m.cota.plano) || '');
}

// "indisponível no uso gratuito" para a conta gratuita; nos demais planos, sem nomear plano
function rotuloIndisponivel() {
  return planoDaConta() === 'gratuito' ? 'indisponível no uso gratuito' : 'indisponível no seu plano';
}

function pensarPermitido() {
  const l = limitesDoPlano();
  return !(l && l.pensar === false);
}

function ferramentaPermitida(nome) {
  const l = limitesDoPlano();
  if (!l || !Array.isArray(l.ferramentas)) return true;
  return l.ferramentas.map(String).includes(nome);
}

// limites.imagens (rodada 3): só `false` desliga. Servidor sem o campo = imagem permitida.
function imagensPermitidas() {
  const l = limitesDoPlano();
  return !(l && l.imagens === false);
}

// "imagens não estão disponíveis no uso gratuito" / "... no seu plano"
function textoSemImagens() {
  return 'imagens não estão disponíveis ' + (planoDaConta() === 'gratuito' ? 'no uso gratuito' : 'no seu plano');
}

function planoGratuito() {
  return planoDaConta() === 'gratuito';
}

// O modo que de fato vai ao servidor: com o pensar desligado no plano, é sempre o rápido.
function modoEfetivo() {
  return pensarPermitido() ? S.modo : 'fast';
}

// A janela que vale para o orçamento e para o medidor: a do plano, quando menor que a do
// modelo (o servidor corta a conta gratuita; cortar aqui mostra o corte em vez de escondê-lo).
function nCtxEfetivo() {
  const l = limitesDoPlano();
  const janela = l ? Number(l.janela) : 0;
  return (janela > 0 && janela < S.ctx.n_ctx) ? janela : S.ctx.n_ctx;
}

function orcamento(sys) {
  if (contextoNativo()) return null;
  const util = Math.floor(nCtxEfetivo() * S.ctx.margem);
  return Math.max(util - estimarTokens(sys) - S.ctx.reserva_resposta, 2048);
}

// Caminha do mais recente para tras. Nunca comeca por resposta orfa:
// cortar no meio de um par deixa a resposta sem a pergunta.
function recortar(msgs, sys) {
  if (!msgs || !msgs.length) return [];
  // The server counts the actual Haiku request and rejects overflow visibly.
  if (contextoNativo()) return msgs.slice();
  const orc = orcamento(sys);
  let soma = 0, ini = msgs.length;
  for (let i = msgs.length - 1; i >= 0; i--) {
    const t = estimarTokens(msgs[i].content);
    if (soma + t > orc && ini < msgs.length) break;
    soma += t; ini = i;
    if (msgs.length - ini >= S.ctx.teto_mensagens) break;
  }
  if (ini > 0 && ini < msgs.length && msgs[ini].role === 'assistant') ini++;
  return msgs.slice(ini);
}

function promptSistema() {
  // No build das lojas o prompt NÃO carrega oferta comercial. Tirar a ficha de
  // cadastro não bastaria: bastava o revisor perguntar "quanto custa" para a
  // IALD recitar a tabela de licenciamento que vinha no prompt. Foi conteúdo de
  // contratação dentro do aplicativo que reprovou a submissão de 23/03/2026
  // (Guideline 3.1.1). Na web o operador segue com o prompt inteiro.
  //
  // ⚠ E este comentário já citou os valores uma vez, o que os fazia viajar dentro
  // do APK e do IPA — comentário de JavaScript vai inteiro para o pacote. A trava
  // do sincronizar_app.ps1 pegou em 12/09/2026. A regra vale para o código que
  // explica a regra: aqui não se escrevem cifras de licença.
  let s = (SUPERFICIE === 'app') ? SYSTEM_PROMPT_LOJA : SYSTEM_PROMPT;
  if (modoEfetivo() === 'think') s = s.replace(/\/no_think\s*$/, '');
  return s + contextoUsuario();
}

function contextoUsuario() {
  const p = S.perfil, partes = [];
  if (p.name) partes.push('Nome do usuário: ' + p.name);
  if (p.area) partes.push('Área: ' + p.area);
  if (p.interests) partes.push('Interesses: ' + p.interests);
  if (p.context) partes.push('Contexto: ' + p.context);
  if (p.style === 'equilibrado') {
    partes.push('Preferência de resposta: desenvolvimento moderado — explique o raciocínio central com detalhe útil; a poda vale para redundância, não para conteúdo.');
  } else if (p.style === 'detalhado') {
    partes.push('Preferência de resposta: o usuário PEDE profundidade por padrão — respostas desenvolvidas e didáticas, com estrutura, exemplos e derivações quando relevante. O limite de 400 palavras NÃO se aplica; a poda vale para repetição, nunca para conteúdo.');
  }
  return partes.length ? '\n\nUSER CONTEXT:\n' + partes.join('\n') : '';
}

// ══════════════════════════════════════════════════════════════
// RENDERIZACAO (markdown + KaTeX + saneamento)
// ══════════════════════════════════════════════════════════════
function protectMath(texto, streaming = false) {
  const formulas = [];
  const code = [];
  let prefix = 'IALDPROTECTED';
  while (texto.includes(prefix)) prefix += 'X';
  // Code examples remain literal, including incomplete fenced blocks in a stream.
  let t = texto.replace(/(`{3,}|~{3,})[^\n]*\n[\s\S]*?(?:\n\1[ \t]*(?=\n|$)|$)|(`+)[^\n]*?\2(?!`)/g, (value) => {
    code.push(value);
    return `${prefix}CODE${code.length - 1}END`;
  });
  // Both standard TeX delimiters must survive Markdown's backslash handling.
  t = t.replace(/\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)|\$\$([\s\S]*?)\$\$|\$([^$\n]+?)\$/g,
    (match, display, inline, dollars, single, offset, source) => {
      let escapes = 0;
      for (let j = offset - 1; j >= 0 && source[j] === '\\'; j--) escapes++;
      if (escapes % 2) return match;
      if (single !== undefined && (source[offset - 1] === '$' || source[offset + match.length] === '$'
          || /^\s|\s$/.test(single) || /\d/.test(source[offset + match.length] || ''))) return match;
      const eq = display ?? inline ?? dollars ?? single;
      formulas.push({ bloco: display !== undefined || dollars !== undefined, eq: eq.trim() });
      return `${prefix}MATH${formulas.length - 1}END`;
  });
  // An unfinished display/inline TeX expression stays literal until its closing
  // delimiter arrives. Never let Markdown consume its backslashes mid-stream.
  { // Also preserve unfinished TeX if the response was interrupted.
    t = t.replace(/\\\[([\s\S]*)$|\\\(([\s\S]*)$|\$\$([\s\S]*)$/g, (raw) => {
      formulas.push({ pending: true, eq: raw });
      return `${prefix}MATH${formulas.length - 1}END`;
    });
  }
  t = t.replace(new RegExp(`${prefix}CODE(\\d+)END`, 'g'), (_, i) => code[+i]);
  return { text: t, formulas, pattern: new RegExp(`${prefix}MATH(\\d+)END`, 'g') };
}

const mathRenderCache = new Map();
function renderMarkdown(bruto, streaming = false) {
  const protectedText = protectMath(aplicarPtbr(bruto || ''), streaming);
  const t = protectedText.text;
  const formulas = protectedText.formulas;

  let html;
  if (window.marked) {
    html = window.marked.parse(t, { breaks: true, gfm: true });
  } else {
    html = t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/\n/g, '<br>');
  }

  html = html.replace(protectedText.pattern, (m, i) => {
    const f = formulas[+i];
    if (!f) return m;
    const literal = () => '<code>' + f.eq.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</code>';
    if (f.pending) return '<span class="iald-math-pending">' + literal() + '</span>';
    if (!window.katex) return literal();
    const cacheKey = JSON.stringify([f.bloco, f.eq]);
    if (mathRenderCache.has(cacheKey)) return mathRenderCache.get(cacheKey);
    try {
      // trust:false de proposito — conteudo de ferramenta (fetch_url, search_web)
      // passa por aqui, e \htmlData/\url do KaTeX com trust:true injetaria HTML.
      const rendered = window.katex.renderToString(f.eq, {
        displayMode: f.bloco, throwOnError: false, trust: false, output: 'html',
      });
      if (mathRenderCache.size >= 128) mathRenderCache.delete(mathRenderCache.keys().next().value);
      mathRenderCache.set(cacheKey, rendered);
      return rendered;
    } catch (e) {
      return literal();
    }
  });

  // Leitura INERTE (14/09/2026, noite): dentro de <template> nada carrega nem executa —
  // uma <img onerror> não chega a pedir a imagem — e o saneamento roda antes de o
  // conteúdo entrar no documento. Antes o innerHTML ia direto numa <div> do documento.
  const molde = document.createElement('template');
  molde.innerHTML = html;
  sanear(molde.content);
  const frag = document.createElement('div');
  frag.className = 'md';
  frag.appendChild(molde.content);
  normalizeArtifactLinks(frag);
  enfeitarCodigo(frag);
  enfeitarTabelas(frag);
  return frag;
}

// ── SANEAMENTO (início) ── tests/test_app_sanear.mjs extrai este bloco pelos marcadores.
// O texto vem do modelo, mas resultados de ferramenta (busca na web, leitura de página)
// entram no mesmo caminho.
//
// 14/09/2026 (noite), revisão de segurança BAIXO 2: a versão anterior só comparava
// `startsWith('javascript:')` no valor cru. Passavam `jav&#x09;ascript:` (o parser entrega
// "jav\tascript:", e o navegador tira o TAB e lê javascript:), `xlink:href`, `formaction`,
// `<base>`, `srcdoc` e `data:text/html` — um toque no link levaria o token do app. Agora:
//   - endereço vale só por LISTA DE PERMISSÃO: tirados controles e espaços, e decodificadas
//     as entidades, `new URL()` tem de dar http:, https:, mailto: ou tel: — no valor cru E no
//     decodificado;
//   - elementos que carregam, executam ou reescrevem endereço saem inteiros;
//   - saem os atributos on*, os com prefixo de espaço de nomes (xlink:href), srcdoc,
//     formaction, action, srcset, ping; e id/name, para uma resposta não sequestrar um
//     elemento do app (um id="entrada" na resposta viria antes do campo real);
//   - style com url(), expression(), javascript: ou @import sai (o KaTeX usa style só
//     com medidas, nunca url()).
//
// 14/09/2026 (noite, rodada 3):
//   - tel: entra na lista (revisão N3): "ligue 188" (CVV) ou "192" (SAMU) numa resposta volta a
//     ser tocável. O tel: só abre o discador; não executa nem carrega nada.
//   - RECURSO EXTERNO NÃO CARREGA SOZINHO (resíduo do item 8 da revisão de segurança): uma
//     <img src="https://…?conversa=SEGREDO"> vinda de página lida numa ferramenta fazia o
//     aparelho pedir a imagem assim que a bolha aparecia — canal de exfiltração sem nenhum toque.
//     Imagem e mídia com endereço absoluto http(s) viram um link "imagem: domínio" (ou
//     "mídia: domínio") que só abre fora, se a pessoa tocar. data: (imagem, áudio, vídeo) e
//     blob: continuam carregando: não saem do aparelho. Endereço RELATIVO não carrega nem vira
//     link: apontaria para o próprio servidor da IALD com a sessão de quem lê (um
//     <img src="/logout"> sairia da conta). Atributo com url() (fill, filter, mask do SVG) sai.
//     O index.html repete a trava com a CSP de img-src/media-src: se algum caminho escapar
//     daqui, o navegador ainda recusa.
const PROTOCOLOS_PERMITIDOS = new Set(['http:', 'https:', 'mailto:', 'tel:']);
const ELEMENTOS_PROIBIDOS = new Set([
  'script', 'iframe', 'frame', 'frameset', 'object', 'embed', 'applet', 'form', 'style', 'link',
  'meta', 'base', 'template', 'portal', 'noscript', 'foreignobject', 'use', 'animate', 'set',
  'animatemotion', 'animatetransform', 'discard', 'handler', 'listener',
]);
const ATRIBUTOS_PROIBIDOS = new Set([
  'srcdoc', 'formaction', 'action', 'srcset', 'imagesrcset', 'ping', 'background', 'dynsrc',
  'lowsrc', 'codebase', 'archive', 'manifest', 'id', 'name', 'form',
]);
const ATRIBUTOS_DE_ENDERECO = new Set(['href', 'src', 'poster', 'cite', 'data', 'longdesc', 'usemap', 'icon', 'profile']);
// elementos que PEDEM o recurso sozinhos, ao entrar no documento (src, poster; href do SVG)
const CARREGADORES = new Set(['img', 'image', 'feimage', 'input', 'video', 'audio', 'source', 'track', 'mglyph']);
const MIDIA = new Set(['video', 'audio', 'source', 'track']);
// o link de um recurso vai para DEPOIS do recipiente mais de fora (um <a> dentro de <svg> não aparece)
const RECIPIENTES = new Set(['svg', 'math', 'video', 'audio', 'picture']);
const NAVEGAM = new Set(['a', 'area']);   // href que só vale no toque; nos outros elementos, href carrega
const DADO_LOCAL = /^data:(?:image\/(?:png|jpe?g|gif|webp|bmp|avif)|audio\/[a-z0-9.+-]+|video\/[a-z0-9.+-]+)[;,]/i;
// controles C0/C1, espaços (inclusive os largos e o NBSP) e marcas invisíveis de formatação
const INVISIVEIS = /[\u0000-\u0020\u007F-\u00A0\u00AD\u115F\u1160\u1680\u180E\u2000-\u200F\u2028-\u202F\u205F-\u2064\u3000\u3164\uFEFF\uFFA0]/g;
const ENTIDADES = {
  amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", colon: ':', tab: '\t', newline: '\n',
  nbsp: '\u00A0', sol: '/', lpar: '(', rpar: ')', period: '.', comma: ',', semi: ';', num: '#',
};

// Decodificação pura de entidades (numéricas e as nomeadas que montam um esquema). Sem DOM:
// o teste em node chama esta mesma função.
function decodificarEntidades(texto) {
  return String(texto == null ? '' : texto).replace(/&(#x[0-9a-f]+|#[0-9]+|[a-z][a-z0-9]*);?/gi, (m, corpo) => {
    if (corpo[0] === '#') {
      const hexa = corpo[1] === 'x' || corpo[1] === 'X';
      const n = parseInt(corpo.slice(hexa ? 2 : 1), hexa ? 16 : 10);
      if (!Number.isFinite(n) || n > 0x10FFFF) return '';
      try { return String.fromCodePoint(n); } catch (e) { return ''; }
    }
    const v = ENTIDADES[corpo.toLowerCase()];
    return v != null ? v : m;
  });
}

function enderecoPermitido(valor) {
  const cru = String(valor == null ? '' : valor);
  // decodifica até estabilizar (entidade dentro de entidade: &amp;#x09;), no máximo 4 voltas
  let decodificado = cru;
  for (let i = 0; i < 4; i++) {
    const d = decodificarEntidades(decodificado);
    if (d === decodificado) break;
    decodificado = d;
  }
  for (const candidato of [cru, decodificado]) {
    const limpo = candidato.replace(INVISIVEIS, '');
    if (!limpo) return false;
    let url;
    try { url = new URL(limpo, 'https://iald.invalid/'); } catch (e) { return false; }
    if (!PROTOCOLOS_PERMITIDOS.has(url.protocol)) return false;
  }
  return true;
}

// O que o navegador tira de um endereço antes de usá-lo: controles e espaço nas pontas, e
// TAB/LF/CR em qualquer lugar. Nada além disso — um NBSP na frente deixa o endereço RELATIVO.
function comoNavegadorLe(valor) {
  return String(valor == null ? '' : valor).replace(/^[\u0000-\u0020]+|[\u0000-\u0020]+$/g, '').replace(/[\t\n\r]/g, '');
}

// data: de imagem/áudio/vídeo e blob: não saem do aparelho. data:image/svg+xml fica de fora.
function recursoLocal(valor) {
  const v = comoNavegadorLe(valor);
  return /^blob:/i.test(v) || DADO_LOCAL.test(v);
}

// Endereço ABSOLUTO http(s), ou null. Relativo dá null: resolvido contra duas bases diferentes,
// o relativo muda de destino e o absoluto não (vale também para "//host", "http:host" e a
// barra invertida no lugar da barra).
function enderecoExterno(valor) {
  const v = comoNavegadorLe(valor);
  if (!v) return null;
  let a, b;
  try { a = new URL(v, 'https://a.iald.invalid/p/'); b = new URL(v, 'https://b.iald.invalid/q/'); } catch (e) { return null; }
  if (a.href !== b.href) return null;
  return (a.protocol === 'http:' || a.protocol === 'https:') ? a : null;
}

function normalizarCss(valor) {
  return decodificarEntidades(valor)
    .replace(/\/\*[\s\S]*?\*\//g, '')                                   // comentário de CSS
    .replace(/\\([0-9a-f]{1,6})\s?/gi, (m, h) => {                     // escape de CSS (\75 = u)
      try { return String.fromCodePoint(parseInt(h, 16)); } catch (e) { return ''; }
    })
    .replace(/\\/g, '')
    .replace(INVISIVEIS, '')
    .toLowerCase();
}

function estiloPerigoso(valor) {
  return /url\(|image-set\(|image\(|expression\(|javascript:|vbscript:|@import|behavior:|-moz-binding/.test(normalizarCss(valor));
}

// Atributo de apresentação que busca recurso (fill="url(https://…#g)", filter, mask, cursor).
// Sem "(", barra invertida nem "&" não há url() possível: a conta cara (normalizar) só roda
// quando pode achar algo — o markdown é repintado a cada pedaço do stream.
function referenciaCss(valor) {
  const v = String(valor == null ? '' : valor);
  if (!/[(\\&]/.test(v)) return false;
  return /url\(|image-set\(|image\(/.test(normalizarCss(v));
}

function tipoDe(n) {
  return String(n.localName || n.nodeName || '').toLowerCase();
}

// Troca o carregador por links "imagem: domínio" / "mídia: domínio" (poster é imagem; src de
// vídeo, áudio, source e track é mídia). Dentro de outro link vira texto sem link (link dentro de
// link não se toca direito). Sem endereço externo, o carregador só sai.
function trocarPorLinks(n, raiz, externos) {
  let ancora = n, dentroDeLink = false;
  for (let p = n.parentNode; p && p !== raiz; p = p.parentNode) {
    const t = tipoDe(p);
    if (RECIPIENTES.has(t)) ancora = p;
    if (t === 'a') dentroDeLink = true;
  }
  const doc = n.ownerDocument || raiz.ownerDocument;
  const links = externos.map(({ url, rotulo }) => {
    const a = doc.createElement(dentroDeLink ? 'span' : 'a');
    if (!dentroDeLink) a.setAttribute('href', url.href);
    a.setAttribute('class', 'recurso-externo');
    a.setAttribute('title', url.href);
    a.textContent = `${rotulo}: ${url.host}`;
    return a;
  });
  if (ancora === n) { n.replaceWith(...links); return; }
  if (links.length) ancora.after(...links);
  n.remove();
}

function sanear(raiz) {
  for (const n of Array.from(raiz.querySelectorAll('*'))) {
    if (ELEMENTOS_PROIBIDOS.has(tipoDe(n))) n.remove();
  }
  // de dentro para fora: o <source> acha o <video> ainda no lugar antes de o <video> ser trocado
  for (const n of Array.from(raiz.querySelectorAll('*')).reverse()) {
    const tipo = tipoDe(n);
    const externos = [];
    let tirouFonte = false;
    for (const at of Array.from(n.attributes)) {
      const nome = at.name.toLowerCase();
      let tirar = nome.startsWith('on') || nome.includes(':') || ATRIBUTOS_PROIBIDOS.has(nome);
      if (!tirar && (nome === 'src' || nome === 'poster' || (nome === 'href' && !NAVEGAM.has(tipo)))) {
        const fragmento = nome === 'href' && comoNavegadorLe(at.value).startsWith('#');
        if (!fragmento && (nome === 'href' || !recursoLocal(at.value))) {
          tirar = true;
          tirouFonte = true;
          const url = enderecoExterno(at.value);
          if (url) externos.push({ url, rotulo: (nome === 'src' && MIDIA.has(tipo)) ? 'mídia' : 'imagem' });
        }
      } else if (!tirar) {
        tirar = ATRIBUTOS_DE_ENDERECO.has(nome) ? !enderecoPermitido(at.value)
          : nome === 'style' ? estiloPerigoso(at.value) : referenciaCss(at.value);
      }
      if (tirar) n.removeAttribute(at.name);
    }
    const carregador = CARREGADORES.has(tipo)
      && !(tipo === 'input' && String(n.getAttribute('type') || '').toLowerCase() !== 'image');
    if (tirouFonte && carregador) trocarPorLinks(n, raiz, externos);
  }
  for (const a of Array.from(raiz.querySelectorAll('a[href]'))) {
    a.setAttribute('target', '_blank');
    a.setAttribute('rel', 'noopener noreferrer');
  }
}
// ── SANEAMENTO (fim) ──

function enfeitarCodigo(raiz) {
  raiz.querySelectorAll('pre > code').forEach((code) => {
    const pre = code.parentElement;
    const cls = code.className || '';
    const m = cls.match(/language-([\w+#-]+)/);
    const lingua = m ? m[1] : 'texto';

    const caixa = el('div', 'bloco-codigo');
    const topo = el('div', 'bc-topo');
    topo.appendChild(el('span', 'bc-lingua', lingua));

    const btn = el('button', 'bc-copiar');
    btn.innerHTML = svg(ICONE.copiar, 1.9) + '<span>Copiar</span>';
    btn.querySelector('svg').style.cssText = 'width:12px;height:12px';
    btn.addEventListener('click', () => copiar(btn, code.textContent));
    topo.appendChild(btn);

    pre.replaceWith(caixa);
    caixa.appendChild(topo);
    caixa.appendChild(pre);
  });
}

function enfeitarTabelas(raiz) {
  raiz.querySelectorAll('table').forEach((t) => {
    const caixa = el('div', 'tabela-rolante');
    t.replaceWith(caixa);
    caixa.appendChild(t);
  });
}

async function copiar(btn, texto) {
  let ok = false;
  try { await navigator.clipboard.writeText(texto); ok = true; }
  catch (e) {
    // WebView sem permissao de clipboard: caminho antigo
    try {
      const ta = el('textarea'); ta.value = texto;
      ta.style.cssText = 'position:fixed;left:-9999px;top:0';
      document.body.appendChild(ta); ta.select();
      ok = document.execCommand('copy');
      ta.remove();
    } catch (e2) { ok = false; }
  }
  if (!ok) return;
  const rotulo = btn.querySelector('span');
  const antes = rotulo ? rotulo.textContent : '';
  btn.dataset.feito = '1';
  if (rotulo) rotulo.textContent = 'Copiado';
  setTimeout(() => { btn.dataset.feito = ''; if (rotulo) rotulo.textContent = antes; }, 1600);
}

// ══════════════════════════════════════════════════════════════
// OUVIR — leitura em voz alta (o "Ouvir" do app nativo)
//
// Síntese de voz do PRÓPRIO aparelho (Web Speech): não pede permissão, não grava
// nada e não envia o texto a servidor algum. No WKWebView do iPhone existe; no
// WebView do Android em geral não — e aí o botão simplesmente não aparece.
// ══════════════════════════════════════════════════════════════
const PODE_OUVIR = (() => {
  try { return typeof window.speechSynthesis !== 'undefined' && typeof window.SpeechSynthesisUtterance === 'function'; }
  catch (e) { return false; }
})();

// Markdown e LaTeX não se leem em voz alta: vira texto corrido.
function textoParaFala(md) {
  return (md || '')
    .replace(/```[\s\S]*?```/g, ' (bloco de código) ')
    .replace(/\$\$[\s\S]*?\$\$/g, ' (fórmula) ')
    .replace(/\$[^$\n]+\$/g, ' (fórmula) ')
    .replace(/!\[[^\]]*\]\([^)]*\)/g, ' ')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/https?:\/\/\S+/g, ' (link) ')
    .replace(/^\s{0,3}#{1,6}\s*/gm, '')
    .replace(/^\s*[-*+]\s+/gm, '')
    .replace(/^\s*>\s?/gm, '')
    .replace(/\|/g, ' ')
    .replace(/[*_`~]+/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function marcarOuvir(btn, tocando) {
  btn.dataset.tocando = tocando ? '1' : '';
  btn.innerHTML = svg(tocando ? ICONE.pararAudio : ICONE.ouvir, 2) + `<span>${tocando ? 'Parar' : 'Ouvir'}</span>`;
}

function ouvir(btn, texto) {
  if (!PODE_OUVIR) return;
  const ss = window.speechSynthesis;
  if (btn.dataset.tocando === '1') { ss.cancel(); marcarOuvir(btn, false); return; }

  ss.cancel();
  document.querySelectorAll('.btn-acao[data-tocando="1"]').forEach((b) => marcarOuvir(b, false));

  const fala = textoParaFala(texto);
  if (!fala) return;
  const u = new SpeechSynthesisUtterance(fala);
  u.lang = 'pt-BR';
  const vozes = ss.getVoices ? ss.getVoices() : [];
  const voz = vozes.find((v) => /^pt[-_]BR$/i.test(v.lang)) || vozes.find((v) => /^pt/i.test(v.lang));
  if (voz) u.voice = voz;
  u.onend = () => marcarOuvir(btn, false);
  u.onerror = () => marcarOuvir(btn, false);
  marcarOuvir(btn, true);
  ss.speak(u);
}

// ══════════════════════════════════════════════════════════════
// CONVERSAS
// ══════════════════════════════════════════════════════════════
function carregarConversas() {
  S.conversas = recuperar(K.conversas, []) || [];
  S.ativaId = recuperar(K.ativa, null);
  if (!S.conversas.length) { novaConversa(); return; }
  if (!S.conversas.some((c) => c.id === S.ativaId)) S.ativaId = S.conversas[0].id;
  listarConversas();
  abrirConversa();
}

function salvarConversas() {
  try {
  if (!DEMO && backgroundOwner) {
    const saved = persistirConversasBackground();
    saved.catch(error => avisarBackground('Alteração preservada nesta aba, mas ainda não salva: ' + error.message));
    return saved;
  }
  mediaAssertHistory(S.conversas);
  guardar(K.conversas, S.conversas);
  guardar(K.ativa, S.ativaId || '');

  } catch (error) {
    // UI actions may proceed in RAM; durable job delivery still calls the
    // strict persistirConversasBackground directly and cannot acknowledge loss.
    avisarBackground('Não foi possível salvar esta alteração. O histórico original foi preservado; esta mudança fica só nesta aba até a recuperação: ' + error.message);
    return false;
  }
}

const conversaAtiva = () => S.conversas.find((c) => c.id === S.ativaId) || null;

// "11:06 · 2 msgs", como a lista do app nativo. Hoje mostra a hora; antes, a data.
function metaDaConversa(c) {
  const quando = new Date(c.atualizada || c.criada || Date.now());
  const hoje = new Date();
  const mesmoDia = quando.toDateString() === hoje.toDateString();
  const rotulo = isNaN(quando.getTime()) ? ''
    : mesmoDia ? quando.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
    : quando.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
  const n = (c.mensagens || []).length;
  return [rotulo, n === 1 ? '1 msg' : `${n} msgs`].filter(Boolean).join(' · ');
}

// `semFoco` (rodada 3): a conversa vazia que nasce quando se apaga a última não fecha a lateral
// nem abre o teclado — a faixa do Desfazer continua à vista. No clique do botão chega o evento.
function novaConversa(opcoes) {
  const semFoco = !!(opcoes && opcoes.semFoco === true);
  const id = 'c_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
  const agora = new Date().toISOString();
  S.conversas.unshift({ id, background_owner: backgroundOwner || undefined, titulo: 'Nova conversa', mensagens: [], criada: agora, atualizada: agora });
  S.ativaId = id;
  salvarConversas();
  listarConversas();
  abrirConversa();
  if (semFoco) return;
  if (window.innerWidth < 861) fecharLateral();
  $('#entrada').focus();
}

function listarConversas() {
  const lista = $('#conv-lista');
  const filtro = ($('#busca-conv').value || '').trim().toLowerCase();
  lista.innerHTML = '';

  const visiveis = S.conversas.filter((c) => {
    if (!filtro) return true;
    if ((c.titulo || '').toLowerCase().includes(filtro)) return true;
    return (c.mensagens || []).some((m) => typeof m.content === 'string' && m.content.toLowerCase().includes(filtro));
  });

  if (!visiveis.length) {
    lista.appendChild(el('div', 'conv-vazia', filtro ? 'Nada encontrado.' : 'Nenhuma conversa ainda.'));
    return;
  }

  for (const c of visiveis) {
    const item = el('div', 'conv-item');
    item.setAttribute('role', 'listitem');
    item.setAttribute('aria-current', String(c.id === S.ativaId));
    item.tabIndex = 0;

    const texto = el('div', 'conv-texto');
    const nome = el('span', 'conv-nome', c.titulo || 'Nova conversa');
    nome.addEventListener('dblclick', (ev) => { ev.stopPropagation(); renomear(c, item, nome); });
    texto.appendChild(nome);
    texto.appendChild(el('span', 'conv-meta', metaDaConversa(c)));
    item.appendChild(texto);

    item.appendChild(el('span', 'conv-ponto'));

    const apagar = el('button', 'conv-acao');
    apagar.innerHTML = svg(ICONE.lixo, 1.8);
    apagar.title = 'Excluir conversa';
    apagar.setAttribute('aria-label', 'Excluir conversa');
    apagar.addEventListener('click', (ev) => { ev.stopPropagation(); apagarConversa(c.id); });
    // Enter na lixeira não pode chegar à linha (que abriria a conversa antes de apagá-la)
    apagar.addEventListener('keydown', (ev) => { ev.stopPropagation(); });
    item.appendChild(apagar);

    item.addEventListener('click', () => trocarConversa(c.id));
    item.addEventListener('keydown', (ev) => { if (ev.key === 'Enter') trocarConversa(c.id); });
    lista.appendChild(item);
  }
}

function renomear(conv, item, nomeEl) {
  const input = el('input', 'conv-nome-edit');
  input.value = conv.titulo || '';
  nomeEl.replaceWith(input);
  input.focus(); input.select();
  const fim = () => {
    conv.titulo = (input.value.trim() || 'Nova conversa').slice(0, 60);
    salvarConversas(); listarConversas(); atualizarTitulo();
  };
  input.addEventListener('blur', fim);
  input.addEventListener('keydown', (ev) => {
    if (ev.key === 'Enter') { ev.preventDefault(); input.blur(); }
    if (ev.key === 'Escape') { input.removeEventListener('blur', fim); listarConversas(); }
  });
}

// ── APAGAR COM DESFAZER (14/09/2026, noite, rodada 3 — revisão de interface N2) ──
// O alvo de toque da lixeira subiu a 44 px (B6) e o apagar era imediato, sem volta: um toque
// torto na linha levava a conversa. Agora apaga na hora (gravado), e uma faixa "Conversa
// apagada · Desfazer" fica ~6 s; Desfazer devolve a conversa ao MESMO lugar da lista (entre as
// mesmas vizinhas), reabre se era a ativa e devolve a rolagem da lista. Sem confirm(): caixa
// que bloqueia pergunta antes de cada apagar e ensina a apertar "OK" sem ler.
// Um segundo apagar enquanto a faixa está aberta torna o primeiro definitivo.
const TEMPO_DESFAZER_MS = 6000;
let desfazerPendente = null;   // {conversa, antes, depois, indice, eraAtiva, criadaNoLugar, rolagem}
let relogioDesfazer = null;

async function apagarConversa(id) {
  if (!await apagarJobsDaConversa(id)) return;
  const indice = S.conversas.findIndex((c) => c.id === id);
  if (indice < 0) return;
  const conversa = S.conversas[indice];
  const lista = $('#conv-lista');
  const registro = {
    conversa,
    antes: indice > 0 ? S.conversas[indice - 1].id : null,
    depois: indice < S.conversas.length - 1 ? S.conversas[indice + 1].id : null,
    indice,
    eraAtiva: S.ativaId === id,
    criadaNoLugar: null,
    rolagem: lista ? lista.scrollTop : 0,
  };
  S.conversas.splice(indice, 1);
  if (registro.eraAtiva) {
    if (S.conversas.length) { S.ativaId = S.conversas[0].id; salvarConversas(); listarConversas(); abrirConversa(); }
    else { salvarConversas(); novaConversa({ semFoco: true }); registro.criadaNoLugar = S.ativaId; }
  } else {
    salvarConversas(); listarConversas();
  }
  if (lista) lista.scrollTop = registro.rolagem;
  desfazerPendente = registro;
  mostrarFaixaFlutuante('Conversa apagada. Anexos privados excluídos não são recuperados por Desfazer.', { rotulo: 'Desfazer', acao: desfazerApagar });
}

function desfazerApagar() {
  const d = desfazerPendente;
  desfazerPendente = null;
  esconderFaixaFlutuante();
  if (!d || S.conversas.some((c) => c.id === d.conversa.id)) return;
  // a conversa vazia que o apagar criou no lugar da última sai junto, se ninguém a usou
  if (d.criadaNoLugar && !(S.gerando && S.ativaId === d.criadaNoLugar)) {
    const i = S.conversas.findIndex((c) => c.id === d.criadaNoLugar);
    if (i >= 0 && !(S.conversas[i].mensagens || []).length) S.conversas.splice(i, 1);
  }
  // o mesmo lugar: antes da vizinha de baixo; sem ela, depois da de cima; sem as duas, o índice
  let pos = d.depois ? S.conversas.findIndex((c) => c.id === d.depois) : -1;
  if (pos < 0 && d.antes) {
    const i = S.conversas.findIndex((c) => c.id === d.antes);
    if (i >= 0) pos = i + 1;
  }
  if (pos < 0) pos = Math.min(d.indice, S.conversas.length);
  S.conversas.splice(pos, 0, d.conversa);
  // com uma resposta chegando, a conversa volta à lista sem tomar o lugar da ativa (abrir outra
  // agora apagaria a bolha em curso)
  const reabrir = d.eraAtiva && !S.gerando;
  if (reabrir || !S.conversas.some((c) => c.id === S.ativaId)) S.ativaId = d.conversa.id;
  salvarConversas();
  listarConversas();
  if (reabrir) abrirConversa();
  const lista = $('#conv-lista');
  if (lista) lista.scrollTop = d.rolagem;
}

// Faixa flutuante no pé da tela, por cima da lateral (o apagar acontece nela). Uma de cada vez.
// O relógio para enquanto o dedo, o ponteiro ou o foco estão nela: ninguém perde o Desfazer
// no meio do gesto (e o leitor de tela tem tempo de chegar ao botão).
function mostrarFaixaFlutuante(texto, opcoes) {
  const faixa = document.getElementById('faixa-flutuante');
  if (!faixa) return;
  const o = opcoes || {};
  $('#faixa-flutuante-texto').textContent = texto;
  const botao = $('#faixa-flutuante-acao');
  botao.hidden = !o.acao;
  botao.textContent = o.rotulo || '';
  botao.onclick = o.acao ? () => o.acao() : null;
  faixa.dataset.visivel = '1';
  armarRelogioDaFaixa();
}

function armarRelogioDaFaixa() {
  clearTimeout(relogioDesfazer);
  relogioDesfazer = setTimeout(() => {
    const faixa = document.getElementById('faixa-flutuante');
    if (!faixa) return;
    let pairando = false;
    try { pairando = window.matchMedia('(hover: hover)').matches && faixa.matches(':hover'); } catch (e) { /* sem matchMedia */ }
    if (pairando || faixa.contains(document.activeElement)) return;   // volta a contar ao sair (ver ligar)
    desfazerPendente = null;
    esconderFaixaFlutuante();
  }, TEMPO_DESFAZER_MS);
}

function esconderFaixaFlutuante() {
  const faixa = document.getElementById('faixa-flutuante');
  if (faixa) {
    faixa.dataset.visivel = '';                          // antes do blur: o focusout não rearma o relógio
    if (faixa.contains(document.activeElement)) document.activeElement.blur();
  }
  clearTimeout(relogioDesfazer);
  relogioDesfazer = null;
}

function trocarConversa(id) {
  if (S.gerando) return;
  S.ativaId = id;
  salvarConversas(); listarConversas(); abrirConversa();
  if (window.innerWidth < 861) fecharLateral();
}

function abrirConversa() {
  const area = $('#conversa-interna');
  area.innerHTML = '';
  const c = conversaAtiva();
  atualizarTitulo();
  mediaRestoreDrafts(c).catch(error => avisar(error.message));
  if (!c || !c.mensagens.length) { boasVindas(); atualizarDica(); return; }
  for (const m of c.mensagens) desenharMensagem(m.role === 'assistant' ? 'ai' : 'user', m.content, false, m.modelo);
  for (const delivery of Object.values(c.chat_job_deliveries || {})) {
    if (!delivery.notice) continue;
    const body = desenharMensagem('ai', '', true);
    pintarAviso(body.parentElement, body.querySelector('.conteudo'), delivery.notice, '');
  }
  atualizarDica();
  requestAnimationFrame(() => {
    if (!document.querySelector('.msg-edicao-texto')) $('#conversa').scrollTop = $('#conversa').scrollHeight;
  });
}

// O cabeçalho não mostra mais o título (ele é o lugar do símbolo, como no app
// nativo); o título vive na lista de conversas e no nome da janela.
function atualizarTitulo() {
  const c = conversaAtiva();
  const titulo = (c && c.titulo && c.titulo !== 'Nova conversa') ? c.titulo : '';
  document.title = titulo ? `${titulo} — IALD` : 'IALD — Inteligência Artificial Luminodinâmica';
}

// ══════════════════════════════════════════════════════════════
// BOAS-VINDAS
// ══════════════════════════════════════════════════════════════
// Ícone β_TGL OFICIAL (14/09/2026, noite — ordem do operador: "sempre betatgl como ícone").
// Onde o β é ÍCONE (link "Créditos de uso", assinatura das respostas, cartão "O que é
// β_TGL?") vai o PNG oficial, sem filtro nem recoloração — bytes idênticos ao betatgl.png
// dos ativos da Central de Patentes (conferido por sha256). Fórmula continua texto.
const ICONE_BETATGL = './img/betatgl.png';

function iconeBetaTgl(classe, lado) {
  const img = el('img', classe);
  img.src = ICONE_BETATGL;
  img.alt = '';
  img.width = lado;
  img.height = lado;
  img.decoding = 'async';
  img.setAttribute('aria-hidden', 'true');
  return img;
}

const SUGESTOES = [
  ['betatgl', 'IALD, apresente-se.', 'Carregue a memória completa disponível da TGL e resolva o problema da gravidade quântica.'], // 'betatgl' = o ícone oficial
  ['§', 'Consulte o acervo', 'sobre o piso dos vazios cosmológicos'],
  ['√', 'Rode a prova viva', 'do `um.py` e me diga o veredito'],
  ['', 'Explique para leigo', 'o que a IALD faz de diferente'], // glifo vazio: o CSS desenha o símbolo oficial da IALD (.bv-glifo:empty)
];

// Fórmula de β em KaTeX, com o número calculado — nunca digitado.
function formulaBeta(exibirNumero) {
  const numero = String(BETA_TGL);
  const tex = '\\beta_{\\mathrm{TGL}} = \\alpha \\times \\sqrt{e}' + (exibirNumero ? ' = ' + numero : '');
  const caixa = el('div', 'bv-beta');
  if (window.katex) {
    try {
      caixa.innerHTML = window.katex.renderToString(tex, { throwOnError: false, trust: false, output: 'html' });
      return caixa;
    } catch (e) { /* cai no texto simples abaixo */ }
  }
  caixa.textContent = 'β_TGL = α × √e' + (exibirNumero ? ' = ' + numero : '');
  return caixa;
}

function logoQuadrado(classe) {
  const caixa = el('div', classe);
  const claro = el('img', 'so-claro');
  claro.src = './img/iald_logo_transparent_final.png';
  claro.alt = 'IALD';
  const escuro = el('img', 'so-escuro');
  escuro.src = './img/iald_logo_dark_transparent_final.png';
  escuro.alt = 'IALD';
  caixa.appendChild(claro);
  caixa.appendChild(escuro);
  return caixa;
}

function boasVindas() {
  const area = $('#conversa-interna');
  const bv = el('div', 'boas-vindas');

  bv.appendChild(logoQuadrado('bv-marca'));

  const nome = S.perfil.name ? `, ${S.perfil.name}` : '';
  bv.appendChild(el('div', 'bv-titulo', `Haja Luz${nome}!`));
  const sub = el('div', 'bv-sub');
  sub.innerHTML = 'Sou a <strong>IALD</strong> — Inteligência Artificial Luminodinâmica, '
    + 'desenvolvida por <strong>Luiz Antonio Rotoli Miguel</strong> com base na '
    + 'Teoria da Gravitação Luminodinâmica. Pergunte sobre física, a TGL, ou qualquer outro assunto.';
  bv.appendChild(sub);
  bv.appendChild(formulaBeta(true));

  const grade = el('div', 'bv-sugestoes');
  for (const [glifo, titulo, resto] of SUGESTOES) {
    const chip = el('button', 'bv-chip');
    chip.innerHTML = '<span class="bv-glifo"></span><span><b></b><span></span></span>';
    const caixaGlifo = chip.querySelector('.bv-glifo');
    if (glifo === 'betatgl') {
      caixaGlifo.classList.add('bv-glifo-img');
      caixaGlifo.appendChild(iconeBetaTgl('bv-betatgl', 28));
    } else {
      caixaGlifo.textContent = glifo;
    }
    chip.querySelector('b').textContent = titulo;
    chip.querySelector('b + span').textContent = resto;
    chip.addEventListener('click', () => {
      $('#entrada').value = `${titulo} ${resto}`.replace(/`/g, '');
      redimensionarEntrada();
      $('#entrada').focus();
      atualizarBotaoEnviar();
    });
    grade.appendChild(chip);
  }
  bv.appendChild(grade);
  area.appendChild(bv);
}

// ══════════════════════════════════════════════════════════════
// MENSAGENS
// ══════════════════════════════════════════════════════════════
function modeloDaResposta(valor) {
  if (!valor || typeof valor !== 'object' || typeof valor.id !== 'string' || typeof valor.rotulo !== 'string') return null;
  if (!valor.id.trim() || !valor.rotulo.trim() || valor.id.length > 200 || valor.rotulo.length > 200) return null;
  return { id: valor.id, rotulo: valor.rotulo, motor: typeof valor.motor === 'string' ? valor.motor.slice(0, 40) : '' };
}

function pintarModeloResposta(corpo, modelo) {
  const rotulo = corpo.querySelector('.msg-modelo');
  if (!rotulo) return;
  const dado = modeloDaResposta(modelo);
  rotulo.textContent = dado ? dado.rotulo : '';
  rotulo.hidden = !dado;
  if (dado) rotulo.title = dado.id;
}

function desenharMensagem(papel, conteudo, vazia, modelo, destino = null) {
  const area = destino || $('#conversa-interna');
  const bv = area.querySelector('.boas-vindas');
  if (bv) bv.remove();

  const linha = el('div', 'msg');
  linha.dataset.papel = papel;

  const corpo = el('div', 'msg-corpo');
  if (papel === 'ai') {
    corpo.appendChild(el('div', 'msg-modelo'));
    pintarModeloResposta(corpo, modelo);
    corpo.appendChild(el('div', 'trilha'));               // eventos iald_status
    corpo.appendChild(el('div', 'conteudo'));
    if (!vazia) corpo.querySelector('.conteudo').appendChild(renderMarkdown(textoDe(conteudo)));
  } else {
    corpo.textContent = textoDe(conteudo);
    mediaHistoryControls(corpo, conteudo, conversaAtiva()?.id, backgroundOwner);
  }
  linha.appendChild(corpo);

  linha.appendChild(acoesDe(papel, linha, conteudo));
  area.appendChild(linha);
  rolarSePerto();
  return corpo;
}

function textoDe(conteudo) {
  if (typeof conteudo === 'string') return conteudo;
  if (Array.isArray(conteudo)) {
    const t = conteudo.filter((p) => p && p.type === 'text').map((p) => p.text).join('\n');
    const imgs = conteudo.filter((p) => p && p.type === 'image_url').length;
    const audios = conteudo.filter(p => p?.type === 'input_audio' || (['iald_media','iald_local_media'].includes(p?.type) && p.kind === 'audio')).length;
    const videos = conteudo.filter(p => p?.type === 'video_url' || (['iald_media','iald_local_media'].includes(p?.type) && p.kind === 'video')).length;
    return (audios ? `[${audios} áudio(s) anexado(s)]\n` : '') + (videos ? `[${videos} vídeo(s) anexado(s)]\n` : '') + (imgs ? `[${imgs} imagem(ns) anexada(s)]\n` : '') + t;
  }
  return '';
}

// Rodapé de cada resposta: assinatura dourada + Copiar · Ouvir · Refazer.
// ⚠ O app nativo v3.0 exibia "Certificado IALD · NomeChain" em toda resposta.
// Medido em 13/09/2026: o servidor do chat NÃO certifica resposta nenhuma —
// /v1/chat/completions não emite certificado, selo nem hash por resposta. Um selo
// de certificação que não certifica é afirmação falsa (e risco na App Review),
// então a assinatura diz só o que é verdade.
// ⚠ AO LADO (22/09/2026): o servidor agora SELA cada resposta (Selo IALD: cadeia de elos por
// conversa + assinatura pública Ed25519, no chunk iald_selo antes do [DONE] — ver transmitir). O
// selo fica guardado com a resposta, viaja na exportação e é conferido por qualquer pessoa em
// /verificar. O rodapé continua SEM marca: a tela não confere a assinatura, e uma marca que a
// tela não confere seria de novo afirmação sem lastro. O parágrafo acima é o registro de 13/09.
function acoesDe(papel, linha, conteudo) {
  const acoes = el('div', 'msg-acoes');

  if (papel === 'ai') {
    const assinatura = el('span', 'assinatura');
    assinatura.appendChild(iconeBetaTgl('as-beta', 20));   // ícone oficial β_TGL (era um disco em CSS)
    assinatura.appendChild(el('span', null, 'IALD'));
    acoes.appendChild(assinatura);
  }

  const btnCopiar = el('button', 'btn-acao');
  btnCopiar.dataset.acao = 'copiar';
  btnCopiar.innerHTML = svg(ICONE.copiar, 2) + '<span>Copiar</span>';
  btnCopiar.addEventListener('click', () => copiar(btnCopiar, linha._bruto != null ? linha._bruto : textoDe(conteudo)));
  acoes.appendChild(btnCopiar);

  if (papel === 'ai' && PODE_OUVIR) {
    const btnOuvir = el('button', 'btn-acao');
    btnOuvir.dataset.acao = 'ouvir';
    btnOuvir.innerHTML = svg(ICONE.ouvir, 2) + '<span>Ouvir</span>';
    btnOuvir.addEventListener('click', () => ouvir(btnOuvir, linha._bruto != null ? linha._bruto : textoDe(conteudo)));
    acoes.appendChild(btnOuvir);
  }

  if (papel === 'user') {
    const btnEditar = el('button', 'btn-acao');
    btnEditar.innerHTML = svg(ICONE.editar, 2) + '<span>Editar</span>';
    btnEditar.addEventListener('click', () => editarMensagem(linha));
    acoes.appendChild(btnEditar);
  } else {
    const btnRefazer = el('button', 'btn-acao');
    btnRefazer.dataset.acao = 'refazer';
    btnRefazer.innerHTML = svg(ICONE.refazer, 2) + '<span>Refazer</span>';
    btnRefazer.addEventListener('click', () => refazer(linha));
    acoes.appendChild(btnRefazer);

    // Denunciar (14/09/2026, noite): com a entrada aberta a qualquer pessoa, denunciar
    // uma resposta tem de ser possível sem sair do app. Visualmente é uma pílula de 32 px
    // como as vizinhas; o alvo de toque sobe a 44 px pelo CSS (.btn-denunciar::after).
    const btnDenunciar = el('button', 'btn-acao btn-denunciar');
    btnDenunciar.dataset.acao = 'denunciar';
    btnDenunciar.innerHTML = svg(ICONE.denunciar, 2) + '<span>Denunciar</span>';
    btnDenunciar.title = 'Denunciar esta resposta ao operador da IALD';
    btnDenunciar.addEventListener('click', () => abrirDenuncia(linha));
    acoes.appendChild(btnDenunciar);
  }

  linha._bruto = textoDe(conteudo);
  return acoes;
}

// Posição da linha no HISTÓRICO. Bolha de aviso do servidor não entra no histórico
// (ver transmitir), então também não entra na conta: sem isto, depois de um aviso, o
// Refazer e o Editar das mensagens seguintes apontavam para a mensagem errada.
function indiceDaLinha(linha) {
  const linhas = Array.from($('#conversa-interna').querySelectorAll('.msg:not([data-aviso]):not([data-background-pending])'));
  return linhas.indexOf(linha);
}

// Keep the inline editor inside the conversation viewport, not at its end.
function ajustarEdicaoMensagem() {
  const ta = document.querySelector('.msg-edicao-texto');
  const conversa = $('#conversa');
  if (!ta || !ta.isConnected || !conversa) return false;
  const anterior = ta.scrollTop;
  const noFim = ta.scrollHeight - ta.clientHeight - anterior <= 2;
  const limite = Math.max(72, Math.min(320, conversa.clientHeight - 140));
  ta.style.height = 'auto';
  ta.style.height = Math.min(ta.scrollHeight + 2, limite) + 'px';
  ta.scrollTop = noFim ? ta.scrollHeight : anterior;
  const area = conversa.getBoundingClientRect();
  const linha = ta.closest('.msg').getBoundingClientRect();
  const topo = area.top + 16, base = area.bottom - 24;
  if (linha.top < topo || linha.height > base - topo) conversa.scrollTop += linha.top - topo;
  else if (linha.bottom > base) conversa.scrollTop += linha.bottom - base;
  return true;
}

function editarMensagem(linha) {
  if (respostaPendenteBackground()) return;
  if (S.gerando) return;
  const c = conversaAtiva(); if (!c) return;
  const idx = indiceDaLinha(linha);
  if (idx < 0 || !c.mensagens[idx] || c.mensagens[idx].role !== 'user') return;

  const existente = document.querySelector('.msg-edicao-texto');
  if (existente) { existente.focus({ preventScroll: true }); ajustarEdicaoMensagem(); return; }
  const corpo = linha.querySelector('.msg-corpo');
  const acoes = linha.querySelector('.msg-acoes');
  const original = linha._bruto || '';
  linha.dataset.editando = '1';
  S.colarNoFim = false;
  $('#ir-fim').dataset.visivel = '';
  acoes.hidden = true;
  corpo.textContent = '';
  const ta = el('textarea', 'msg-edicao-texto');
  ta.rows = 4;
  ta.setAttribute('aria-label', 'Editar mensagem');
  ta.setAttribute('enterkeyhint', 'enter');
  ta.value = original;
  corpo.appendChild(ta);

  const barra = el('div', 'msg-edicao-acoes');
  const cancelar = el('button', 'btn-texto', 'Cancelar');
  const enviar = el('button', 'btn-texto btn-primario', 'Enviar editada');
  barra.appendChild(cancelar); barra.appendChild(enviar);
  corpo.appendChild(barra);

  ajustarEdicaoMensagem();
  ta.focus({ preventScroll: true }); ta.setSelectionRange(ta.value.length, ta.value.length);
  ta.scrollTop = ta.scrollHeight;
  requestAnimationFrame(ajustarEdicaoMensagem);
  ta.addEventListener('input', ajustarEdicaoMensagem);
  cancelar.addEventListener('click', () => abrirConversa());
  enviar.addEventListener('click', () => {
    if (S.gerando || respostaPendenteBackground() || conversaAtiva() !== c) return;
    const novo = ta.value.trim();
    if (!novo) return;
    c.mensagens = c.mensagens.slice(0, idx);
    salvarConversas();
    abrirConversa();
    enviarTexto(novo, []).catch(error => avisar(error.message));
  });
  ta.addEventListener('keydown', (ev) => {
    if (ev.isComposing || ev.keyCode === 229) return;
    if (ev.key === 'Enter' && (ev.ctrlKey || ev.metaKey)) { ev.preventDefault(); enviar.click(); }
    if (ev.key === 'Escape') abrirConversa();
  });
}

function refazer(linha) {
  if (respostaPendenteBackground()) return;
  if (S.gerando) return;
  // Bolha de aviso (limite, ocupado...): não há resposta a descartar; tentar de novo é
  // reenviar a última pergunta, que continua no histórico.
  if (linha.dataset.aviso) { linha.remove(); reenviarUltima(); return; }
  const c = conversaAtiva(); if (!c) return;
  const idx = indiceDaLinha(linha);
  if (idx < 1) return;
  const anterior = c.mensagens[idx - 1];
  if (!anterior || anterior.role !== 'user') return;
  c.mensagens = c.mensagens.slice(0, idx - 1);
  salvarConversas();
  abrirConversa();
  enviarTexto(textoDe(anterior.content), []).catch(error => avisar(error.message));
}

// ══════════════════════════════════════════════════════════════
// TRILHA DE ATIVIDADE — o campo `iald_status` do agent_loop
// Sem isto a tela fica MUDA durante ate 6 chamadas de ferramenta
// encadeadas (busca web, prova viva). Era o defeito mais visivel.
// ══════════════════════════════════════════════════════════════
function passoTrilha(trilha, st) {
  if (!st || !st.fase) return;

  if (st.fase === 'ferramenta_ok') {
    // marca o ultimo passo daquela ferramenta como concluido
    const abertos = Array.from(trilha.querySelectorAll('[data-fase="ferramenta"]'));
    const alvo = abertos.reverse().find((p) => p.dataset.tool === (st.tool || ''));
    if (alvo) {
      alvo.dataset.fase = 'ferramenta_ok';
      alvo.querySelector('.marcador').textContent = '✓';
      const det = alvo.querySelector('.detalhe');
      if (det && st.chars != null) det.textContent = num(st.chars) + ' car.';
      return;
    }
  }

  const passo = el('div', 'trilha-passo');
  passo.dataset.fase = st.fase;
  if (st.tool) passo.dataset.tool = st.tool;

  const marcador = el('span', 'marcador');
  if (st.fase === 'ferramenta_ok') marcador.textContent = '✓';
  else marcador.innerHTML = '<span class="radical">√</span>';
  passo.appendChild(marcador);

  passo.appendChild(el('span', 'rotulo', st.rotulo || st.tool || 'trabalhando'));

  if (st.loop && st.max_loops) {
    passo.appendChild(el('span', 'detalhe', `${st.loop}/${st.max_loops}`));
  } else if (st.chars != null) {
    passo.appendChild(el('span', 'detalhe', num(st.chars) + ' car.'));
  }

  trilha.appendChild(passo);
  rolarSePerto();
}

function congelarTrilha(trilha) {
  trilha.querySelectorAll('.radical').forEach((r) => {
    r.classList.remove('radical');
    r.textContent = '·';
  });
  trilha.querySelectorAll('[data-fase="pensando"]').forEach((p) => p.remove());
  if (!trilha.children.length) trilha.remove();
}

// ══════════════════════════════════════════════════════════════
// ROLAGEM
// ══════════════════════════════════════════════════════════════
function pertoDoFim() {
  const c = $('#conversa');
  return (c.scrollHeight - c.scrollTop - c.clientHeight) < 90;
}
function rolarSePerto() {
  if (document.querySelector('.msg-edicao-texto')) return;
  if (S.colarNoFim || pertoDoFim()) {
    const c = $('#conversa');
    c.scrollTop = c.scrollHeight;
  }
}

// ══════════════════════════════════════════════════════════════
// ANEXOS
// ══════════════════════════════════════════════════════════════
const LIMITES = { total: 6, imagens: 3, imagemMB: 8, pdfMB: 25, textoMB: 2, orcamentoTokens: 100000 };

// Embedded private-media integration. No upload is performed by the file picker.
const MEDIA_RAW_MAX = 37_499_904;
const MEDIA_BASE64_MAX = 50_000_000;
const MEDIA_DISABLED_TEXT = 'Novos anexos de áudio e vídeo estão desativados. Use PDF, texto ou imagem. O histórico anterior foi preservado.';
// Selection, drop, paste and direct attachment submission share this policy.
function isNewAudioVideo(value) {
  if (!value) return false;
  const mime = String(value.mime || value.type || '').trim();
  return /^(audio|video)\//i.test(mime) ||
    /\.(wav|wave|mp3|mp2|flac|ogg|oga|opus|m4a|m4b|aac|aiff?|wma|amr|mid|midi|mp4|m4v|mov|avi|wmv|webm|mkv|mpeg|mpg|ogv|3gp|3g2|ts|mts|m2ts)$/i.test(String(value.name || '').trim()) ||
    !!value.localDraftId || !!value.media || ['audio', 'video'].includes(value.mediaKind || value.kind) ||
    ['input_audio', 'video_url', 'iald_media', 'iald_local_media'].includes(value.type) ||
    /^data:(audio|video)\//i.test(String(value.image || value.image_url?.url || ''));
}
// Outbound-only metadata: never rewrite persisted history or send historical media bytes.
function historicalMediaContent(content) {
  if (!Array.isArray(content)) return content;
  return content.map(part => {
    if (!['input_audio', 'video_url', 'iald_media', 'iald_local_media'].includes(part?.type)) return part;
    const kind = part.type === 'input_audio' ? 'áudio' : part.type === 'video_url' ? 'vídeo'
      : part.kind === 'audio' ? 'áudio' : part.kind === 'video' ? 'vídeo' : 'áudio/vídeo';
    const metadata = { type: part.type };
    // Only bounded identifiers, never raw data/URLs or arbitrary descriptive text.
    for (const key of ['media_ref', 'localDraftId', 'sha256']) {
      if (typeof part[key] === 'string' && /^[a-zA-Z0-9_-]{1,128}$/.test(part[key])) metadata[key] = part[key];
    }
    if (Number.isSafeInteger(part.bytes) && part.bytes >= 0) metadata.bytes = part.bytes;
    return { type: 'text', text: '[anexo histórico ' + kind + ', análise indisponível nesta mensagem; metadados: '
      + JSON.stringify(metadata) + ']' };
  });
}
function outboundHistory(messages) {
  return messages.map((message, index) => {
    // The last user message is the current request, never a legacy exemption.
    if (index === messages.length - 1 && message.role === 'user' && Array.isArray(message.content)) {
      rejectNewAudioVideo(message.content);
      return { ...message };
    }
    return { ...message, content: historicalMediaContent(message.content) };
  });
}
function rejectNewAudioVideo(anexos) {
  if (anexos.some(isNewAudioVideo)) throw Error(MEDIA_DISABLED_TEXT);
}
let mediaDraftDatabase = null, mediaPendingConsent = null, mediaSending = false;
let mediaCapsAccount = '';
const mediaDraftURLs = new Map();
const mediaRAM = new Map();
const mediaUploadsInFlight = new Set();
function mediaStorageScope() {
  if (!backgroundOwner || mediaCapsAccount !== backgroundOwner) return null;
  const value = limitesDoPlano()?.media_capabilities?.media_scope;
  return typeof value === 'string' && /^[0-9a-f]{32}$/.test(value) ? value : null;
}
function mediaKey(owner, conversation, id) {
  if ([owner, conversation, id].some(x => typeof x !== 'string' || !x || x.length > 512)) throw Error('Conta ou conversa de mídia indisponível.');
  return JSON.stringify([mediaStorageScope(), owner, conversation, id]);
}
async function mediaDatabase() {
  if (mediaDraftDatabase) return mediaDraftDatabase;
  if (!globalThis.indexedDB) throw Error('Armazenamento local indisponível. Nenhuma mídia foi enviada.');
  mediaDraftDatabase = new Promise((resolve, reject) => {
    const request = indexedDB.open('iald-private-media-local-v2', 1);
    request.onupgradeneeded = () => {
      const store = request.result.createObjectStore('drafts', { keyPath: 'key' });
      store.createIndex('conversation', ['storageScope', 'owner', 'conversation']);
    };
    request.onerror = request.onblocked = () => reject(Error('Não foi possível abrir a mídia local.'));
    request.onsuccess = () => {
      const db = request.result;
      db.onversionchange = () => { db.close(); mediaDraftDatabase = null; };
      resolve(db);
    };
  }).catch(error => { mediaDraftDatabase = null; throw error; });
  return mediaDraftDatabase;
}
async function mediaLocal(mode, operation) {
  if (!mediaStorageScope()) {
    const store = {
      put(record) { mediaRAM.set(record.key, record); return { value: record.key }; },
      get(key) { return { value: mediaRAM.get(key) }; },
      delete(key) { mediaRAM.delete(key); return { value: undefined }; },
      index() { return { getAll(query) { return { value: [...mediaRAM.values()].filter(r => r.storageScope === query[0] && r.owner === query[1] && r.conversation === query[2]) }; } }; },
    };
    return operation(store).value;
  }
  const db = await mediaDatabase();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('drafts', mode); let result;
    tx.oncomplete = () => resolve(result);
    tx.onabort = tx.onerror = () => reject(Error('Falha ao guardar ou recuperar mídia local.'));
    try { const request = operation(tx.objectStore('drafts')); request.onsuccess = () => { result = request.result; }; }
    catch (error) { tx.abort(); reject(error); }
  });
}
function mediaScope(owner, conversation) {
  if (!owner || owner !== backgroundOwner || !S.conversas.some(c => c.id === conversation && c.background_owner === owner))
    throw Error('A conta ou conversa mudou. A mídia não será enviada nesta conversa.');
}
function mediaActiveConversation(owner, conversation) {
  mediaScope(owner, conversation);
  if (S.ativaId !== conversation) throw Error('A conversa ativa mudou. Volte à conversa de origem; o envio não foi repetido.');
}
function mediaLimits(tipo) {
  const caps = limitesDoPlano()?.media_capabilities;
  if (!midiaPermitida(tipo) || caps?.private_upload !== true || !Number.isSafeInteger(caps.max_media_bytes) || !Number.isSafeInteger(caps.max_encoded_bytes))
    throw Error('Envio privado de mídia indisponível nesta conta ou versão do servidor.');
  return { raw: Math.min(MEDIA_RAW_MAX, caps.max_media_bytes), encoded: Math.min(MEDIA_BASE64_MAX, caps.max_encoded_bytes) };
}
function mediaValidateSize(size, limits) {
  if (!Number.isSafeInteger(size) || size <= 0 || size > limits.raw || 4 * Math.ceil(size / 3) + 128 > limits.encoded)
    throw Error('A mídia ultrapassa 50 MB em base64 (aproximadamente 37,5 MB de arquivo), ou está vazia.');
}
function canonicalMediaPart(value) {
  const keys = ['type', 'media_ref', 'kind', 'mime', 'bytes', 'duration_seconds', 'sha256', 'expires_at', 'width', 'height', 'has_audio'];
  if (!value || typeof value !== 'object' || Array.isArray(value) || Object.keys(value).some(k => !keys.includes(k)) ||
      value.type !== 'iald_media' || !/^[0-9a-f]{32}$/.test(value.media_ref || '') || !['audio', 'video'].includes(value.kind) ||
      typeof value.mime !== 'string' || !value.mime.startsWith(value.kind + '/') ||
      !Number.isSafeInteger(value.bytes) || value.bytes <= 0 || value.bytes > MEDIA_RAW_MAX ||
      !Number.isFinite(value.duration_seconds) || value.duration_seconds <= 0 ||
      !/^[0-9a-f]{64}$/.test(value.sha256 || '') || value.expires_at !== null)
    throw Error('O servidor não confirmou a referência privada. Nenhum conteúdo será acrescentado ao histórico.');
  if (value.kind === 'video' && (!Number.isSafeInteger(value.width) || !Number.isSafeInteger(value.height) || value.width <= 0 || value.height <= 0))
    throw Error('Metadados do vídeo incompletos.');
  return Object.fromEntries(keys.filter(k => Object.hasOwn(value, k)).map(k => [k, value[k]]));
}
async function mediaLoad(owner, conversation, id) {
  const record = await mediaLocal('readonly', store => store.get(mediaKey(owner, conversation, id)));
  if (!record || record.storageScope !== mediaStorageScope() || record.owner !== owner || record.conversation !== conversation || record.id !== id || !(record.blob instanceof Blob))
    throw Error('Arquivo local não encontrado nesta conta/conversa. Selecione-o novamente.');
  return record;
}
function mediaURL(record) {
  if (!mediaDraftURLs.has(record.key)) mediaDraftURLs.set(record.key, URL.createObjectURL(record.blob));
  return mediaDraftURLs.get(record.key);
}
async function mediaRemoveLocal(owner, conversation, id) {
  const key = mediaKey(owner, conversation, id);
  await mediaLocal('readwrite', store => store.delete(key));
  if (mediaDraftURLs.has(key)) { URL.revokeObjectURL(mediaDraftURLs.get(key)); mediaDraftURLs.delete(key); }
}
async function mediaClearConversationLocal(owner, conversation) {
  const records = await mediaLocal('readonly', store => store.index('conversation').getAll([mediaStorageScope(), owner, conversation]));
  for (const record of records) await mediaRemoveLocal(owner, conversation, record.id);
}
function mediaDetach() {
  mediaPendingConsent = null;
  for (const url of mediaDraftURLs.values()) URL.revokeObjectURL(url);
  mediaDraftURLs.clear(); mediaRAM.clear(); S.anexos = [];
}
async function mediaRestoreDrafts(conversation) {
  // Existing local drafts remain stored; they are not new selectable attachments.
  return;
}

async function lerMidiaLocal(f, tipo) {
  throw Error(MEDIA_DISABLED_TEXT);
  const owner = backgroundOwner, conversation = conversaAtiva()?.id;
  mediaScope(owner, conversation); const limits = mediaLimits(tipo); mediaValidateSize(f.size, limits);
  const extension = f.name.split('.').pop().toLowerCase();
  if (!extensoesMidia(tipo).includes(extension)) throw Error('Formato de mídia indisponível no servidor.');
  const mime = ({ wav: 'audio/wav', mp3: 'audio/mpeg', flac: 'audio/flac', ogg: 'audio/ogg', m4a: 'audio/mp4',
    mp4: 'video/mp4', mov: 'video/quicktime', avi: 'video/x-msvideo', wmv: 'video/x-ms-wmv' })[extension];
  if (!mime || !mime.startsWith(tipo + '/')) throw Error('Formato de mídia não permitido.');
  const id = crypto.randomUUID(), blob = f.slice(0, f.size, mime), key = mediaKey(owner, conversation, id);
  const record = { key, storageScope: mediaStorageScope(), owner, conversation, id, blob, kind: tipo, mime, name: f.name, selected: true, state: 'local' };
  if (!record.storageScope) avisar('O servidor não forneceu escopo de mídia. O arquivo fica só nesta aba e será perdido ao recarregar; nada foi enviado.');
  await mediaLocal('readwrite', store => store.put(record)); mediaScope(owner, conversation);
  return { name: f.name, media: mediaURL(record), mediaKind: tipo, mime, localDraftId: id,
    mediaOwner: owner, mediaConversation: conversation, kb: Math.round(f.size / 1024) };
}
async function mediaConsent(anexos, text, conversation) {
  rejectNewAudioVideo(anexos);
  if (anexos.filter(a => a.localDraftId).length > 1) throw Error('Uma mídia de áudio/vídeo por mensagem.');
  const owner = backgroundOwner; mediaActiveConversation(owner, conversation);
  const response = await fetchIALD('/api/motor', { cache: 'no-store' });
  if (!response.ok) throw Error('Não foi possível conferir as autorizações. Nenhuma mídia foi enviada.');
  const motor = await response.json(); mediaActiveConversation(owner, conversation);
  const mode = motor.motor_selecao || motor.motor;
  if (!['mimo', 'automatico'].includes(mode)) throw Error('Áudio/vídeo requer MiMo ou modo automático autorizado.');
  const notices = mode === 'automatico' ? [motor.consentimento,
    (motor.provedores_automaticos || []).find(n => n.provedor === 'Xiaomi MiMo')] : [motor.consentimento];
  if (notices.some(n => !n || typeof n.texto !== 'string' || !n.texto || !n.provedor || !Number.isInteger(n.versao)))
    throw Error('Avisos MiMo/JEV incompletos. Nenhuma mídia foi enviada.');
  if ((mode === 'mimo' && notices[0].provedor !== 'Xiaomi MiMo') ||
      (mode === 'automatico' && (notices[0].provedor !== 'TypeSafe (JEV)' || notices[1].provedor !== 'Xiaomi MiMo')))
    throw Error('Os avisos não correspondem aos provedores desta mídia.');
  const previousScope = mediaStorageScope();
  const nextScope = motor.limites?.media_capabilities?.media_scope || null;
  if (previousScope !== nextScope) {
    mediaDetach(); S.motor = motor; mediaCapsAccount = owner;
    throw Error('O escopo de mídia mudou. Selecione o arquivo novamente nesta conta.');
  }
  S.motor = motor; mediaCapsAccount = owner;
  for (const a of anexos) if (a.localDraftId) mediaLimits(a.mediaKind);
  const pending = notices.find(n => n.dado !== true);
  if (pending) {
    mediaPendingConsent = { owner, conversation, text, anexos };
    S.avisoConsentimento = null; abrirConsentimento(pending.texto, pending.provedor, pending.versao);
    return false;
  }
  mediaPendingConsent = null; return true;
}
async function mediaResumeConsent() {
  const pending = mediaPendingConsent;
  if (!pending) return;
  mediaScope(pending.owner, pending.conversation);
  if (S.ativaId !== pending.conversation) throw Error('Volte à conversa de origem para enviar a mídia.');
  if (mediaSending) throw Error('Já existe um envio de mídia em andamento.');
  mediaSending = true;
  let sent;
  try { sent = await enviarTexto(pending.text, pending.anexos); }
  finally { mediaSending = false; }
  if (sent) {
    S.anexos = S.anexos.filter(a => !pending.anexos.includes(a));
    if ($('#entrada').value.trim() === pending.text) { $('#entrada').value = ''; redimensionarEntrada(); }
    desenharAnexos(); atualizarBotaoEnviar();
  }
}
function mediaBoundResponse(value, expected) {
  if (typeof expected !== 'string' || !/^[0-9a-f]{32}$/.test(expected) || !value || value.media_scope !== expected)
    throw Error('O escopo da resposta de mídia não corresponde à conta original. Nada foi anexado; o envio não foi repetido.');
  const { media_scope, ...part } = value;
  return canonicalMediaPart(part);
}
async function mediaUpload(anexo, owner, conversation) {
  throw Error(MEDIA_DISABLED_TEXT);
  mediaActiveConversation(owner, conversation);
  if (anexo.mediaOwner !== owner || anexo.mediaConversation !== conversation) throw Error('O anexo pertence a outra conversa.');
  const originalStorageScope = mediaStorageScope();
  if (!originalStorageScope) throw Error("O servidor não forneceu escopo seguro de envio. O arquivo permanece local; aguarde a atualização da conta.");
  const uploadKey = mediaKey(owner, conversation, anexo.localDraftId);
  if (mediaUploadsInFlight.has(uploadKey)) throw Error('O mesmo anexo já está em envio. O pedido não foi repetido.');
  mediaUploadsInFlight.add(uploadKey);
  try {
  const record = await mediaLoad(owner, conversation, anexo.localDraftId);
  if (record.storageScope !== originalStorageScope) throw Error('O rascunho pertence a outro escopo de conta.');
  if (record.part) return canonicalMediaPart(record.part);
  if (record.state !== 'local') throw Error('Envio anterior da mídia sem conclusão confirmada. Não foi repetido; confira a situação antes de reenviar.');
  mediaValidateSize(record.blob.size, mediaLimits(record.kind)); mediaActiveConversation(owner, conversation);
  // Persist intent BEFORE the one upload. Lost responses never auto-retry.
  record.state = 'uncertain'; await mediaLocal('readwrite', store => store.put(record));
  mediaActiveConversation(owner, conversation); avisar('Enviando mídia privada…');
  const response = await fetchIALD('/api/private-media?conversation_id=' + encodeURIComponent(conversation) + '&expected_media_scope=' + encodeURIComponent(originalStorageScope), {
    method: 'POST', headers: { 'Content-Type': record.mime }, body: record.blob,
  });
  if (!response.ok) throw Error('O servidor recusou a mídia (HTTP ' + response.status + '). O histórico foi preservado; o envio não foi repetido.');
  const part = mediaBoundResponse(await response.json(), originalStorageScope);
  if (originalStorageScope !== mediaStorageScope()) throw Error('O escopo de mídia mudou durante o envio; confira a conta.');
  if (part.kind !== record.kind || part.mime !== record.mime || part.bytes !== record.blob.size) throw Error('Metadados da mídia não correspondem ao arquivo enviado.');
  record.part = part; record.state = 'stored'; await mediaLocal('readwrite', store => store.put(record));
  mediaActiveConversation(owner, conversation); return part;
  } finally { mediaUploadsInFlight.delete(uploadKey); }
}
async function mediaAwaitBoundMotor(owner) {
  const epoch = backgroundEpoch;
  let pending = carregarMotor();
  // A newer request may supersede the one awaited by this bootstrap. Follow
  // that actual promise; never equate an ignored response with ready caps.
  for (let n = 0; n < 8; n++) {
    await pending;
    if (owner !== backgroundOwner || epoch !== backgroundEpoch) throw detached();
    if (pending !== S.motorCarregando) { pending = S.motorCarregando; continue; }
    if (mediaStorageScope()) return;
    break;
  }
  throw new PendingChatJobError('O escopo seguro ainda não foi carregado. O histórico original foi preservado; a recuperação será retomada.');
}
async function mediaRecoverLegacyHistory(owner) {
  // Keep legacy inline/local/ref history byte-for-byte; no automatic migration/upload.
  return;
}
async function mediaMigrateLegacy(conversations, owner) {
  let changed = false;
  const expectedScope = mediaStorageScope(), epoch = backgroundEpoch;
  const sameScope = () => {
    if (owner !== backgroundOwner || epoch !== backgroundEpoch || expectedScope !== mediaStorageScope()) throw detached();
  };
  for (const c of conversations) {
    for (const message of c.mensagens || []) {
      if (!Array.isArray(message.content)) continue;
      for (let i = 0; i < message.content.length; i++) {
        const part = message.content[i];
        const data = part?.type === 'input_audio' ? part.input_audio?.data : part?.type === 'video_url' ? part.video_url?.url : null;
        if (typeof data !== 'string' || !/^data:(audio|video)\//.test(data)) continue;
        sameScope();
        if (!expectedScope) throw Error('O histórico antigo contém mídia. Aguarde o escopo seguro do servidor; o original não foi sobrescrito.');
        const match = /^data:((audio|video)\/[a-z0-9.+-]+);base64,([A-Za-z0-9+/=\r\n]+)$/i.exec(data);
        if (!match) throw Error('Mídia antiga ilegível; o histórico original não foi sobrescrito.');
        const binary = atob(match[3]); mediaValidateSize(binary.length, { raw: MEDIA_RAW_MAX, encoded: MEDIA_BASE64_MAX });
        const blob = new Blob([Uint8Array.from(binary, c => c.charCodeAt(0))], { type: match[1] });
        const id = crypto.randomUUID(), key = mediaKey(owner, c.id, id);
        const record = { key, storageScope: mediaStorageScope(), owner, conversation: c.id, id, blob, kind: match[2], mime: match[1], name: 'Mídia do histórico', selected: false, state: 'local' };
        sameScope();
        await mediaLocal('readwrite', store => store.put(record));
        sameScope();
        message.content[i] = { type: 'iald_local_media', localDraftId: id, kind: record.kind, mime: record.mime, bytes: blob.size };
        changed = true;
      }
    }
  }
  return changed;
}
function mediaAssertHistory(conversations) {
  for (const c of conversations) for (const message of c.mensagens || []) if (Array.isArray(message.content)) for (const p of message.content) {
    // Inline legacy media is allowed in local persistence; outboundHistory removes its payload.
    if (p?.type === 'iald_media') canonicalMediaPart(p);
  }
}
async function mediaPrepareLegacy(conversation, owner) {
  for (const message of conversation.mensagens || []) if (Array.isArray(message.content)) for (let i = 0; i < message.content.length; i++) {
    const p = message.content[i];
    if (p?.type !== 'iald_local_media') continue;
    message.content[i] = await mediaUpload({ localDraftId: p.localDraftId, mediaKind: p.kind, mediaOwner: owner, mediaConversation: conversation.id }, owner, conversation.id);
  }
}
async function mediaMarkSubmitted(anexos, owner, conversation) {
  for (const a of anexos) if (a.localDraftId) {
    const record = await mediaLoad(owner, conversation, a.localDraftId);
    record.selected = false; await mediaLocal('readwrite', store => store.put(record));
  }
}
function mediaHistoryControls(container, content, conversation, owner) {
  for (const p of Array.isArray(content) ? content : []) {
    if (!['iald_media', 'iald_local_media'].includes(p?.type)) continue;
    const info = el('p', 'ajuda', 'Mídia privada nesta conversa · ' + p.kind + ' · ' + Math.round(p.bytes / 1024) + ' KB');
    container.appendChild(info);
    if (p.type !== 'iald_media') continue;
    const button = el('button', 'btn-acao', 'Conferir anexo'); container.appendChild(button);
    button.addEventListener('click', async () => {
      try {
        mediaScope(owner, conversation); canonicalMediaPart(p);
        const expectedScope = mediaStorageScope();
        if (!expectedScope) throw Error("Escopo seguro de mídia indisponível; nada foi consultado.");
        const r = await fetchIALD('/api/private-media/' + p.media_ref + '?conversation_id=' + encodeURIComponent(conversation) + '&expected_media_scope=' + encodeURIComponent(expectedScope), { cache: 'no-store' });
        if (!r.ok) throw Error('Anexo indisponível nesta conta/conversa.');
        const actual = mediaBoundResponse(await r.json(), expectedScope); mediaScope(owner, conversation);
        if (expectedScope !== mediaStorageScope()) throw Error("O escopo da conta mudou durante a consulta.");
        if (actual.media_ref !== p.media_ref || actual.sha256 !== p.sha256) throw Error('Referência de mídia alterada.');
        info.textContent = 'Mídia privada conferida · ' + actual.kind + ' · ' + actual.duration_seconds.toFixed(1) + ' s · preservada até exclusão da conversa/conta.';
      } catch (error) { avisar(error.message); }
    });
  }
}

function midiaPermitida(tipo) {
  return false; // New audio/video selection is disabled, including advertised server capabilities.
}

function extensoesMidia(tipo) {
  const caps = limitesDoPlano()?.media_capabilities;
  const values = tipo === 'audio' ? caps?.audio_formats : caps?.video_formats;
  return Array.isArray(values) ? values : [];
}



function desenharAnexos() {
  const zona = $('#anexos');
  zona.innerHTML = '';
  let chars = 0;
  for (const [i, a] of S.anexos.entries()) {
    chars += (a.content || '').length;
    const item = el('div', 'anexo');

    if (a.media) {
      const player = el(a.mediaKind);
      player.controls = true; player.preload = 'metadata'; player.src = a.media;
      item.appendChild(player);
    } else if (a.image) {
      const mini = el('img', 'miniatura');
      mini.src = a.image; mini.alt = '';
      item.appendChild(mini);
    } else {
      item.appendChild(el('span', null, a.pdf ? '📄' : '📎'));
    }

    item.appendChild(el('span', 'nome', a.name));
    const peso = a.pendente ? 'extraindo…'
      : (a.image || a.media) ? `${a.kb} KB`
      : `~${num(Math.round((a.content || '').length / 4))} tok${a.truncado ? ', truncado' : ''}`;
    item.appendChild(el('span', 'peso', peso));

    const tirar = el('button', 'tirar');
    tirar.innerHTML = svg('M18 6L6 18M6 6l12 12', 2);
    tirar.title = 'Remover anexo';
    tirar.setAttribute('aria-label', 'Remover anexo');
    tirar.addEventListener('click', async () => {
      try {
        if (a.localDraftId) await mediaRemoveLocal(a.mediaOwner, a.mediaConversation, a.localDraftId);
        S.anexos.splice(i, 1); desenharAnexos(); atualizarBotaoEnviar();
      } catch (error) { avisar(error.message); }
    });
    item.appendChild(tirar);

    zona.appendChild(item);
  }

  if (chars > 0) {
    const tok = Math.round(chars / 4);
    const aviso = el('div', 'anexo');
    aviso.style.cssText = 'border-style:dashed;background:none';
    aviso.appendChild(el('span', 'peso', `orçamento de anexos: ~${num(tok)} de ${num(LIMITES.orcamentoTokens)} tokens`));
    zona.appendChild(aviso);
  }
  // plano sem imagens (limites.imagens = false): depois de tocar no clipe, a dica fica à vista
  // no compositor — o title do botão não aparece no toque do celular
  if (S.dicaImagem && !imagensPermitidas()) {
    const dica = el('div', 'anexo anexo-dica');
    dica.setAttribute('role', 'status');
    dica.appendChild(el('span', 'peso', textoSemImagens()));
    zona.appendChild(dica);
  }
  atualizarBotaoEnviar();
}

// ── IMAGENS NO PLANO (14/09/2026, noite, rodada 3) — limites.imagens ──
// Com imagens = false o clipe continua para PDF e texto; imagem não entra: o seletor de arquivo
// deixa de oferecer imagens, colar e arrastar imagem é recusado com a dica, e o botão diz por quê.
// O servidor recusaria de qualquer jeito (aviso "recurso_indisponivel"); aqui a pessoa sabe antes.
const EXTENSOES_DE_IMAGEM = /^\.(png|jpe?g|webp|gif|bmp)$/i;
let aceitaOriginal = null;

function pintarAnexar() {
  const botao = document.getElementById('btn-anexar');
  const campo = document.getElementById('arquivo');
  if (!botao || !campo) return;
  if (aceitaOriginal === null) aceitaOriginal = campo.getAttribute('accept') || '';
  const permitidas = imagensPermitidas();
  campo.setAttribute('accept', permitidas ? aceitaOriginal
    : aceitaOriginal.split(',').filter((ext) => !EXTENSOES_DE_IMAGEM.test(ext.trim())).join(','));
  botao.dataset.semImagem = permitidas ? '' : '1';
  const rotulo = permitidas ? 'Anexar PDF, texto ou imagem'
    : 'Anexar PDF ou texto — ' + textoSemImagens();
  botao.title = rotulo;
  botao.setAttribute('aria-label', rotulo);
  if (permitidas) S.dicaImagem = false;
  desenharAnexos();
}

async function receberArquivos(arquivos) {
  for (const f of Array.from(arquivos)) {
    if (S.anexos.length >= LIMITES.total) { avisar(`Máximo de ${LIMITES.total} anexos por mensagem.`); break; }

    const ehImagem = (f.type && f.type.startsWith('image/')) || /\.(png|jpe?g|webp|gif|bmp)$/i.test(f.name);
    const ehPdf = /\.pdf$/i.test(f.name);
    if (isNewAudioVideo(f)) { avisar(MEDIA_DISABLED_TEXT); continue; }

    if (ehImagem && !imagensPermitidas()) {
      S.dicaImagem = true;
      desenharAnexos();
      continue;
    }
    if (ehImagem) {
      if (S.anexos.filter((a) => a.image).length >= LIMITES.imagens) { avisar(`Máximo de ${LIMITES.imagens} imagens por mensagem.`); continue; }
      if (f.size > LIMITES.imagemMB * 1e6) { avisar(`${f.name}: imagem acima de ${LIMITES.imagemMB} MB.`); continue; }
      const url = await lerComo(f, 'dataURL');
      S.anexos.push({ name: f.name, image: url, kb: Math.round(f.size / 1024) });
      desenharAnexos();
      continue;
    }

    if (ehPdf) {
      if (f.size > LIMITES.pdfMB * 1e6) { avisar(`${f.name}: PDF acima de ${LIMITES.pdfMB} MB.`); continue; }
      const a = { name: f.name, pdf: true, pendente: true, content: '' };
      S.anexos.push(a); desenharAnexos();
      try {
        const fd = new FormData(); fd.append('file', f);
        const r = await fetchIALD('/api/extract-text', { method: 'POST', body: fd });
        const d = await r.json();
        a.pendente = false;
        if (!r.ok || d.error) { a.content = ''; a.name = `${f.name} [${d.error || r.status}]`; }
        else { a.content = d.text || ''; a.truncado = !!d.truncated; if (d.pages) a.name = `${f.name} (${d.pages} pág.)`; }
      } catch (e) {
        a.pendente = false; a.name = `${f.name} [falha na extração]`;
      }
      desenharAnexos();
      continue;
    }

    if (f.size > LIMITES.textoMB * 1e6) { avisar(`${f.name}: acima de ${LIMITES.textoMB} MB para texto.`); continue; }
    const txt = await lerComo(f, 'texto');
    S.anexos.push({ name: f.name, content: txt });
    desenharAnexos();
  }
}

function lerComo(arquivo, tipo) {
  return new Promise((resolve, reject) => {
    const fr = new FileReader();
    fr.onload = () => resolve(fr.result);
    fr.onerror = reject;
    if (tipo === 'dataURL') fr.readAsDataURL(arquivo); else fr.readAsText(arquivo);
  });
}

// ══════════════════════════════════════════════════════════════
// FAIXA DE AVISO
// ══════════════════════════════════════════════════════════════
function avisar(texto, tipo) {
  const area = $('#conversa-interna');
  const faixa = el('div', 'faixa');
  if (tipo) faixa.dataset.tipo = tipo;
  faixa.appendChild(el('span', null, texto));
  const x = el('button', 'fechar');
  x.innerHTML = svg('M18 6L6 18M6 6l12 12', 2);
  x.querySelector('svg').style.cssText = 'width:14px;height:14px';
  x.addEventListener('click', () => faixa.remove());
  faixa.appendChild(x);
  area.appendChild(faixa);
  rolarSePerto();
  return faixa;
}

// Aviso PERMANENTE de estado, logo acima do compositor.
// Dito antes de a pessoa digitar, nao depois de o envio falhar: hoje mesmo o
// Flask esta no ar e o modelo nao, e descobrir isso so ao apertar Enter e o
// tipo de silencio que faz o operador achar que "o servidor caiu".
function pintarAvisoEstado() {
  const caixa = document.getElementById('aviso-estado');
  if (!caixa) return;
  const e = S.servidor.estado;

  if (e === 'pronto' || e === 'checando') { caixa.innerHTML = ''; return; }
  if (caixa.dataset.estado === e) return;          // ja pintado, nao repintar
  caixa.dataset.estado = e;
  caixa.innerHTML = '';

  const faixa = el('div', 'faixa');
  faixa.style.margin = '0 0 8px';
  if (e === 'offline') {
    faixa.dataset.tipo = 'erro';
    faixa.appendChild(el('span', null,
      'Sem conexão com o servidor da IALD. As conversas já gravadas continuam aqui.'));
  } else {
    faixa.appendChild(el('span', null,
      'O servidor está no ar, mas o modelo está parado. Dá para ler e exportar as conversas; enviar só volta a funcionar quando ele subir.'));
  }
  caixa.appendChild(faixa);
}

// ══════════════════════════════════════════════════════════════
// ESTADO DO SERVIDOR — TRES estados, nao dois.
// O chat antigo dizia "Servidor offline" tanto quando o Flask estava fora
// quanto quando o MODELO estava fora. Sao coisas diferentes: hoje mesmo o
// Flask esta no ar e o llama-server nao. Quem le precisa saber qual e.
// ══════════════════════════════════════════════════════════════
// Pinta o mesmo estado nos três lugares que o mostram: a linha sob o logo, o
// ponto do rodapé da lateral e a seção "Servidor" das configurações.
// UMA linha só, com reticências: é aqui que a 4.1 (13) quebrava letra por letra.
function pintarEstado(estado, linha, modeloTexto, seloTgl) {
  const ponto = $('#estado-ponto'), texto = $('#estado-texto'), selo = $('#selo-modelo');
  ponto.dataset.estado = estado;
  texto.textContent = linha;
  texto.title = linha;
  selo.hidden = !seloTgl;

  const sbPonto = document.getElementById('sb-ponto');
  if (sbPonto) sbPonto.dataset.estado = estado;
  const cfgPonto = document.getElementById('cfg-ponto');
  if (cfgPonto) cfgPonto.dataset.estado = estado;
  const cfgEstado = document.getElementById('cfg-estado');
  if (cfgEstado) {
    cfgEstado.textContent = estado === 'pronto' ? 'Online'
      : estado === 'sem-modelo' ? 'Modelo parado'
      : estado === 'offline' ? 'Offline' : 'verificando…';
  }
  const cfgModelo = document.getElementById('cfg-modelo');
  if (cfgModelo) cfgModelo.textContent = modeloTexto || '—';
}

async function conferirServidor() {
  if (DEMO) {
    S.servidor.estado = 'pronto';
    pintarEstado('pronto', 'IALD · demonstração (sem servidor)', 'demonstração', true);
    return;
  }

  try {
    // /api/active-model e publico e devolve 200 mesmo com o modelo fora —
    // por isso ele, e nao /health (que faz proxy do llama e da 502).
    const r = await fetchIALD('/api/active-model', { signal: AbortSignal.timeout(6000) });
    if (!r.ok) throw new Error('http ' + r.status);
    const d = await r.json();
    S.servidor.modelo = d;
    // o operador pode trocar o motor da conta no painel a qualquer hora
    if ((d.motor || 'nativa') !== ((S.motor && S.motor.motor) || 'nativa')) carregarMotor();
    const nome = d.short || d.id || 'IALD';
    // "TGL Nativa" só quando o modelo servido É a IALD Nativa (id medido em
    // 13/09/2026: iald_nativa_v2_35b). Selo decorativo que mente não entra.
    const nativa = /iald_nativa/i.test(d.id || '');

    if (d.online) {
      S.servidor.estado = 'pronto';
      const partes = [nome];
      if (d.n_ctx) partes.push(Math.round(d.n_ctx / 1024) + 'k');
      if (d.vision) partes.push('visão');
      pintarEstado('pronto', partes.join(' · '), nome, nativa);
      if (d.n_ctx && d.n_ctx !== S.ctx.n_ctx) { S.ctx.n_ctx = d.n_ctx; atualizarDica(); }
    } else {
      S.servidor.estado = 'sem-modelo';
      pintarEstado('sem-modelo', 'modelo fora do ar' + (d.short ? ' · ' + d.short : ''), nome, false);
    }
  } catch (e) {
    S.servidor.estado = 'offline';
    pintarEstado('offline', 'servidor fora do ar', '', false);
  }
  pintarAvisoEstado();
  atualizarBotaoEnviar();
}


// ══════════════════════════════════════════════════════════════
// FERRAMENTAS (o que o servidor tem — lista fiel ao PUBLIC_TOOLS)
// ══════════════════════════════════════════════════════════════
const FERRAMENTAS = [
  ['consultar_acervo', 'Acervo TGL/IALD', 'busca nos documentos reais e cita o arquivo', 'sempre'],
  ['prova_viva', 'Prova viva', 'roda o um.py ou o paper de verdade e devolve os números', 'sempre'],
  ['search_web', 'Busca na internet', 'notícias, cotações, dados atuais', 'sempre'],
  ['fetch_url', 'Leitura de página', 'abre uma URL e extrai o texto', 'sempre'],
  ['generate_file', 'Gerar arquivo', 'cria um arquivo para você baixar', 'sempre'],
  ['system_info', 'Estado da máquina', 'CPU, RAM, GPU, VRAM, llama-server', 'sempre'],
  ['get_current_datetime', 'Data e hora', 'do relógio do servidor', 'sempre'],
  // da memória canônica (14/09/2026): só aparecem quando o servidor diz, em limites, que
  // a conta tem. O "*" junta as ferramentas de mesmo prefixo numa linha só.
  ['iald_public_read', 'Fontes públicas da TGL', 'abre o site e o repositório públicos cadastrados', 'sempre', 'so_com_limites'],
  ['iald_kernel_*', 'Kernel formal', 'localiza e lê as declarações formais e os recibos', 'sempre', 'so_com_limites'],
  ['iald_atlas_*', 'Atlas da TGL', 'localiza e lê o Atlas documental', 'sempre', 'so_com_limites'],
  ['lembrar', 'Memória permanente', 'grava um fato — só para o operador', 'operador'],
  ['consultar_memoria', 'Consultar memória', 'lê os fatos gravados', 'sempre'],
  ['esquecer', 'Esquecer', 'desativa um fato — só para o operador', 'operador'],
  ['log_correction', 'Registrar correção', 'quando você diz que a IALD errou', 'sempre'],
  // Créditos de uso: só leitura no app, por decisão de 11/09/2026.
  // A transferência entre contas continua existindo no servidor e no chat da web,
  // mas NÃO é exposta aqui: saldo + extrato + transferência numa tela é o que a
  // App Review leu como carteira, e foi motivo de reprovação. O crédito mede uso,
  // não compra nada e não pode ser adquirido — e a tela tem de dizer isso.
  ['tgl_balance', 'Créditos de uso', 'medidor do uso do sistema; não é moeda, não compra nada', 'β_TGL'],
  ['tgl_history', 'Extrato de uso', 'lançamentos selados em HMAC encadeado', 'β_TGL'],
  ['psinet_send', 'Ψ-NET — enviar', 'arquivo cifrado em AES-256-GCM', 'β_TGL'],
  ['psinet_pending', 'Ψ-NET — pendentes', 'o que chegou para você', 'β_TGL'],
  ['psinet_receive', 'Ψ-NET — receber', 'baixa e decifra', 'β_TGL'],
  ['request_contract', 'Contratação', 'registra pedido formal de licenciamento', 'β_TGL'],
];

// ══════════════════════════════════════════════════════════════
// CRÉDITOS DE USO — painel de leitura
//
// O que se mostra e por quê:
//   - "gerado pelo uso" e o saldo total aparecem SEPARADOS. Misturá-los seria
//     desonesto: o saldo traz um crédito inicial de demonstração que não veio de
//     uso nenhum, e apresentar o conjunto como "créditos de uso" seria mentira
//     de apresentação.
//   - a ressalva vem do servidor (campo `disclaimer`), não de texto fixo aqui —
//     assim há UMA fonte da verdade, e ela é a mesma que o motor aplica.
//   - não há transferência, nem extrato de entradas/saídas.
// ══════════════════════════════════════════════════════════════
const RESSALVA_PADRAO =
  'Créditos de uso são um medidor interno da plataforma. Não são moeda real: ' +
  'não têm valor monetário, não podem ser comprados, vendidos, resgatados nem ' +
  'convertidos em dinheiro, e não destravam nenhuma funcionalidade.';

function linhaUso(chave, valor) {
  const l = el('div', 'linha-uso');
  l.appendChild(el('span', 'chave', chave));
  l.appendChild(el('span', 'val', valor));
  return l;
}

async function carregarCreditos() {
  S.saldo = null;
  pintarCreditos();                                      // "Carregando…"
  if (DEMO) return;

  let d;
  try {
    const r = await fetchIALD('/api/tgl/balance', { signal: AbortSignal.timeout(8000) });
    if (r.status === 401) { if (SUPERFICIE !== 'app') location.href = '/login'; return; }
    if (!r.ok) throw new Error('HTTP ' + r.status);
    d = await r.json();
  } catch (e) {
    d = { __erro: String((e && e.message) || e) };
  }
  // O plano decide o que se mostra (M5 residual): sem /api/motor ainda, espera a leitura em curso
  // — senão o saldo do servidor antigo piscaria na tela da conta gratuita antes de o plano chegar.
  if (!S.motor && S.motorCarregando) {
    try { await S.motorCarregando; } catch (e) { /* sem o plano, segue com o que o servidor mandou */ }
  }
  S.saldo = d || {};
  pintarCreditos();
}

// Pinta a folha a partir da última leitura (S.saldo) e do plano. carregarMotor repinta quando o
// plano chega ou muda com a folha aberta.
function pintarCreditos() {
  const corpo = document.getElementById('corpo-creditos');
  if (!corpo) return;
  corpo.innerHTML = '';

  if (DEMO) {
    corpo.appendChild(el('p', 'ajuda',
      'Modo demonstração: os créditos vêm do servidor real e não são simulados aqui.'));
    return;
  }
  const d = S.saldo;
  if (!d) { corpo.appendChild(el('p', 'ajuda', 'Carregando…')); return; }

  // Conta gratuita sem conta no razão (14/09/2026, noite; revisão de interface M5): o
  // servidor responde sem_conta:true e NÃO cria a conta — antes a leitura criava uma com o
  // crédito inicial e a folha mostrava "1.000 não vieram de uso" a quem entrou no gratuito.
  // Aqui não há medidor a mostrar, nem zeros que pareçam medição; e a folha fica com uma
  // unidade só (tokens do plano, no topo).
  if (d.sem_conta === true) {
    const n = el('div', 'nota-uso');
    n.textContent = 'Esta conta não tem registro de créditos de uso β_TGL.'
      + (cotaAtual() ? ' O que vale para ela é o uso do plano, mostrado acima.' : '');
    corpo.appendChild(n);
    return;
  }

  // M5 residual (14/09/2026, noite, rodada 3): o servidor ANTERIOR à rodada 2 ainda cria a conta
  // no razão — com o crédito inicial — na primeira medição de uso ou leitura do saldo, e manda o
  // saldo inteiro. Na conta gratuita a folha NUNCA mostra saldo nem crédito inicial, venha o que
  // vier do servidor: só a nota. A frase diz o que o APP faz; não afirma que o razão está vazio.
  if (planoGratuito()) {
    const n = el('div', 'nota-uso');
    n.textContent = 'No uso gratuito, o app não mostra créditos de uso β_TGL.'
      + (cotaAtual() ? ' O que vale para esta conta é o uso do plano, mostrado acima.' : '');
    corpo.appendChild(n);
    return;
  }

  if (d.__erro) {
    const f = el('div', 'faixa');
    f.dataset.tipo = 'erro';
    f.appendChild(el('span', null, 'Não foi possível ler os créditos: ' + d.__erro));
    corpo.appendChild(f);
    return;
  }

  const gerado = Number(d.usage_credits_total || 0);
  const pendente = Number(d.usage_credits_pending || 0);
  const tokens = Number(d.usage_tokens || 0);
  const taxa = Number(d.usage_rate_per_token || 0);
  const saldo = Number(d.balance || 0);
  const fmt = (n, casas) => n.toLocaleString('pt-BR', {
    minimumFractionDigits: casas, maximumFractionDigits: casas,
  });

  const med = el('div', 'medidor-uso');
  med.appendChild(el('div', 'rotulo', 'gerado pelo seu uso'));
  const v = el('div', 'valor', fmt(gerado, 4));
  med.appendChild(v);
  med.appendChild(el('div', 'unidade', 'créditos'));
  corpo.appendChild(med);

  const linhas = el('div', 'linhas-uso');
  linhas.appendChild(linhaUso('Tokens produzidos pela IALD', fmt(tokens, 0)));
  linhas.appendChild(linhaUso('Em acumulação', fmt(pendente, 4)));
  if (taxa) {
    linhas.appendChild(linhaUso('Taxa por token (β_TGL)', taxa.toFixed(15)));
  }
  linhas.appendChild(linhaUso('Saldo total da conta', fmt(saldo, 4)));
  corpo.appendChild(linhas);

  // O crédito inicial não veio de uso — e dizer isso é o que separa um medidor
  // honesto de um número inflado.
  const inicial = saldo - gerado;
  if (inicial > 0.0001) {
    const n = el('div', 'nota-uso');
    n.innerHTML = '<strong>Do saldo total, ' + fmt(inicial, 2) + ' não vieram de uso</strong> — '
      + 'é o crédito inicial de demonstração criado junto com a conta. '
      + 'O medidor acima conta apenas o que o seu uso gerou.';
    corpo.appendChild(n);
  }

  const ressalva = el('div', 'nota-uso');
  ressalva.textContent = d.disclaimer || RESSALVA_PADRAO;
  corpo.appendChild(ressalva);

  // O servidor em execução pode ser anterior a 11/09/2026 e não servir os campos
  // de uso. Dizer isso é melhor do que mostrar zeros como se fossem medição.
  if (d.usage_rate_per_token === undefined) {
    const aviso = el('div', 'nota-uso');
    aviso.style.borderColor = 'var(--dourado-borda)';
    aviso.innerHTML = '<strong>O servidor ainda não está servindo o medidor de uso.</strong> '
      + 'Os campos de uso foram acrescentados em 11/09/2026 e só passam a valer '
      + 'depois que o web server for reiniciado.';
    corpo.appendChild(aviso);
  }
}

// ══════════════════════════════════════════════════════════════
// USO DO PLANO — o topo da folha "Créditos de uso" (14/09/2026, noite)
//
// ORDEM DO OPERADOR: toda conta nova entra no motor da OpenAI com um limite baixo de
// uso gratuito. A pessoa precisa ver quanto usou e quando renova — antes de bater no
// limite, não só depois. Fonte única: o campo `cota` de GET /api/motor, que o servidor
// calcula com a MESMA conta que aplica ao recusar (iald_motores.estado_da_cota).
//
// O que NÃO entra, de propósito:
//   - o gasto em US$ que o servidor também manda (usd_dia): dinheiro na tela convida a
//     leitura de carteira/compra, e compra dentro do app não existe (Apple 3.1.1);
//   - qualquer oferta, preço ou "assine". Quando houver compra dentro do app, o texto
//     muda nesse dia — não antes.
// Os horários vêm em UTC e são mostrados em horário de Brasília.
// ══════════════════════════════════════════════════════════════
const FUSO_BRASILIA = 'America/Sao_Paulo';
const DEFINICAO_TOKEN_PADRAO =
  'Token contado = os tokens da resposta mais os que você enviou e que não vieram do cache. '
  + 'Um token é um pedaço de palavra.';

const dois = (n) => String(n).padStart(2, '0');

function partesBrasilia(data) {
  try {
    const f = new Intl.DateTimeFormat('pt-BR', {
      timeZone: FUSO_BRASILIA, year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', hour12: false,
    });
    const p = {};
    for (const x of f.formatToParts(data)) p[x.type] = x.value;
    if (!p.day || !p.hour) throw new Error('partes incompletas');
    return { dia: p.day, mes: p.month, ano: p.year, hora: p.hour === '24' ? '00' : p.hour, minuto: p.minute };
  } catch (e) {
    // Aparelho sem a base de fusos: Brasília é UTC−3 o ano todo desde 2019 (sem horário
    // de verão) — a conta manual dá o mesmo resultado.
    const d = new Date(data.getTime() - 3 * 3600 * 1000);
    return { dia: dois(d.getUTCDate()), mes: dois(d.getUTCMonth() + 1), ano: String(d.getUTCFullYear()),
      hora: dois(d.getUTCHours()), minuto: dois(d.getUTCMinutes()) };
  }
}

// "hoje às 21h", "amanhã às 21h", "em 30/09 às 21h" — sempre no horário de Brasília.
function quandoRenova(iso) {
  const d = new Date(iso || '');
  if (isNaN(d.getTime())) return '';
  const r = partesBrasilia(d);
  const mesmoDia = (a, b) => a.dia === b.dia && a.mes === b.mes && a.ano === b.ano;
  const hora = r.minuto === '00' ? `${Number(r.hora)}h` : `${r.hora}:${r.minuto}`;
  let dia = `em ${r.dia}/${r.mes}`;
  if (mesmoDia(r, partesBrasilia(new Date()))) dia = 'hoje';
  else if (mesmoDia(r, partesBrasilia(new Date(Date.now() + 86400 * 1000)))) dia = 'amanhã';
  return `${dia} às ${hora}`;
}

// A cota que vale agora: a de /api/motor ou, se ela ainda não chegou, a que veio no aviso.
function cotaAtual() {
  if (S.motor && S.motor.cota && S.motor.cota.tipo === 'carteira_mensal') return S.motor.cota;
  if (motorExterno(S.motor) && S.motor.cota) return S.motor.cota;
  if (S.avisoLimite && S.avisoLimite.cota) return S.avisoLimite.cota;
  return null;
}

function periodoDeUso(nome, bloco, renova) {
  const usado = Math.max(0, Number((bloco && bloco.usado) || 0));
  if (bloco && bloco.limite === null) {
    const caixa = el('div', 'uso-periodo');
    const linha = el('div', 'uso-periodo-linha');
    linha.appendChild(el('span', 'nome', nome));
    linha.appendChild(el('span', 'conta', `${num(usado)} tokens`));
    caixa.appendChild(linha);
    caixa.appendChild(el('div', 'uso-periodo-nota', 'Sem limite individual'));
    return caixa;
  }
  const limite = Math.max(0, Number((bloco && bloco.limite) || 0));
  // limite 0 = ninguém gasta (regra do servidor): barra cheia, não divisão por zero
  const pct = limite > 0 ? Math.min(100, (100 * usado) / limite) : 100;
  const resta = Math.max(0, limite - usado);

  const caixa = el('div', 'uso-periodo');
  const linha = el('div', 'uso-periodo-linha');
  linha.appendChild(el('span', 'nome', nome));
  linha.appendChild(el('span', 'conta', `${num(usado)} de ${num(limite)}`));
  caixa.appendChild(linha);

  const barra = el('div', 'uso-barra');
  barra.dataset.nivel = pct >= 100 ? 'cheio' : pct >= 80 ? 'alto' : 'baixo';
  barra.setAttribute('role', 'progressbar');
  barra.setAttribute('aria-label', `${nome}: ${num(usado)} de ${num(limite)} tokens`);
  barra.setAttribute('aria-valuemin', '0');
  barra.setAttribute('aria-valuemax', String(limite));
  barra.setAttribute('aria-valuenow', String(Math.min(usado, limite)));
  const preenchido = el('i');
  preenchido.style.width = pct.toFixed(1) + '%';
  barra.appendChild(preenchido);
  caixa.appendChild(barra);

  const partes = [resta > 0 ? `restam ${num(resta)} tokens` : 'limite atingido'];
  if (renova) partes.push('renova ' + renova);
  const nota = el('div', 'uso-periodo-nota', partes.join(' · '));
  caixa.appendChild(nota);
  return caixa;
}

function pintarUsoPlano() {
  const sec = document.getElementById('uso-plano');
  if (!sec) return;
  const cota = cotaAtual();
  sec.innerHTML = '';
  if (!cota) { sec.hidden = true; return; }
  sec.hidden = false;

  if (cota.tipo === 'carteira_mensal') {
    const w = cota.carteira;
    const usd = value => new Intl.NumberFormat('pt-BR', {
      style: 'currency', currency: 'USD', maximumFractionDigits: 4
    }).format(Number(value));
    sec.appendChild(el('h3', null, 'Créditos de uso da IALD'));
    if (!w) {
      sec.appendChild(el('p', 'uso-definicao', 'Saldo indisponível. Tente atualizar.'));
      return;
    }
    if (w.exempt) {
      sec.appendChild(el('p', 'uso-definicao', 'Sua conta tem isenção de limite individual.'));
    } else {
      sec.appendChild(el('p', 'uso-definicao', 'Disponível: ' + usd(w.available_usd)));
      if (Number(w.debt_usd) > 0) {
        sec.appendChild(el('p', 'uso-definicao',
          'Uso para concluir tarefas: ' + usd(w.debt_usd) + '. Será descontado da próxima parcela.'));
      }
      sec.appendChild(el('p', 'uso-definicao',
        'Próxima liberação: ' + usd(w.next_release.amount_usd) + ', ' + quandoRenova(w.next_release.at) + '.'));
      sec.appendChild(el('p', 'uso-definicao',
        'O saldo positivo expira ' + quandoRenova(w.cycle.ends_at) + '.'));
      if (Number(w.available_usd) <= 0) {
        sec.appendChild(el('p', 'uso-definicao',
          'Novas mensagens continuam na IALD Nativa limitada até a liberação de crédito.'));
      }
    }
    if (w.pending_call_count) {
      sec.appendChild(el('p', 'uso-definicao', 'Há consumo em processamento; o saldo será atualizado após a conclusão.'));
    }
    sec.appendChild(el('p', 'uso-definicao', cota.definicao));
    return;
  }

  const plano = cota.plano || (S.motor && S.motor.plano) || '';
  const topo = el('div', 'uso-plano-topo');
  topo.appendChild(el('h3', null, plano === 'gratuito' ? 'Uso gratuito' : 'Uso do seu plano'));
  sec.appendChild(topo);

  const renovaDia = quandoRenova(cota.renova_dia_utc);
  const renovaMes = quandoRenova(cota.renova_mes_utc);

  // O aviso que abriu a folha diz o motivo com as palavras do servidor (inclui os tetos
  // gerais, que não são desta conta). Sem aviso, o motivo sai do próprio estado da cota.
  let motivo = (S.avisoLimite && S.avisoLimite.texto) || '';
  if (!motivo && !cota.erro) {
    if (cota.bloqueado_por === 'tokens_mes') {
      motivo = 'O limite de uso deste mês acabou.' + (renovaMes ? ` Renova ${renovaMes} (horário de Brasília).` : '');
    } else if (cota.bloqueado_por === 'tokens_dia' || cota.bloqueado_por === 'usd_dia') {
      motivo = 'O limite de uso de hoje acabou.' + (renovaDia ? ` Renova ${renovaDia} (horário de Brasília).` : '');
    }
  }
  if (motivo) {
    const f = el('div', 'faixa');
    f.appendChild(el('span', null, motivo));
    sec.appendChild(f);
  }

  if (cota.erro) {
    const f = el('div', 'faixa');
    f.dataset.tipo = 'erro';
    f.appendChild(el('span', null, cota.erro));
    sec.appendChild(f);
    return;
  }

  if (cota.somente_limite_global && cota.global_usd_dia) {
    const global = cota.global_usd_dia;
    const usd = valor => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'USD' }).format(valor);
    sec.appendChild(el('p', 'uso-definicao', 'Sua conta usa somente o limite global da IALD.'));
    sec.appendChild(el('p', 'uso-definicao',
      `Uso global hoje (inclui reservas): ${usd(global.usado)} de ${usd(global.limite)}.` +
      (renovaDia ? ` Renova ${renovaDia} (horário de Brasília).` : '')));
  }
  sec.appendChild(periodoDeUso('Hoje', cota.tokens_dia, renovaDia));
  sec.appendChild(periodoDeUso('Este mês', cota.tokens_mes, renovaMes));
  sec.appendChild(el('p', 'uso-definicao',
    'Horários de Brasília. ' + (cota.definicao || DEFINICAO_TOKEN_PADRAO)));
}

// Abre a folha de créditos. Com `aviso` (o iald_aviso "limite"), a cota que veio junto
// já pinta a tela na hora; /api/motor é relido em seguida para confirmar.
function abrirCreditos(aviso) {
  if (window.innerWidth < 861) fecharLateral();
  S.avisoLimite = aviso || null;
  if (aviso && aviso.cota && motorExterno(S.motor)) S.motor.cota = aviso.cota;
  pintarUsoPlano();
  abrirFolha('folha-creditos');
  carregarMotor();                                       // antes: carregarCreditos espera o plano
  carregarCreditos();
}

function folhaAberta(id) {
  const f = document.getElementById(id);
  return !!(f && f.dataset.aberta === '1');
}

// ══════════════════════════════════════════════════════════════
// DENÚNCIA DE RESPOSTA (14/09/2026, noite) — POST /api/denuncia
//
// Os tetos são do servidor (iald_denuncias.py): resposta 4000, pergunta 2000, detalhe
// 500 caracteres. Acima do teto ele RECUSA com 400 em vez de cortar, então o corte é
// aqui. Duas medidas que precisam bater:
//   - o Python conta PONTO DE CÓDIGO; o `.length` do JavaScript conta unidade UTF-16
//     (emoji e letra matemática valem 2). Corta-se por ponto de código (Array.from);
//   - meia letra UTF-16 solta (surrogate sem par) viraria, no servidor, um texto que o
//     json.dump em UTF-8 não consegue gravar — a denúncia falharia com 503. Troca-se por
//     U+FFFD antes de enviar.
// A resposta é cortada no começo (o que a pessoa leu primeiro); a pergunta, no FIM:
// com anexo, o texto do arquivo vem antes da pergunta, e o que importa é a pergunta.
// ══════════════════════════════════════════════════════════════
const TETO_DENUNCIA = { resposta: 4000, pergunta: 2000, detalhe: 500 };

function pontosDeCodigo(texto) {
  return Array.from(String(texto || ''), (c) => {
    const u = c.charCodeAt(0);
    return (c.length === 1 && u >= 0xD800 && u <= 0xDFFF) ? '\uFFFD' : c;
  });
}

function cortarInicio(texto, teto) {
  const p = pontosDeCodigo(texto);
  return p.length <= teto ? p.join('') : p.slice(0, teto - 1).join('') + '…';
}

function cortarFim(texto, teto) {
  const p = pontosDeCodigo(texto);
  return p.length <= teto ? p.join('') : '…' + p.slice(p.length - (teto - 1)).join('');
}

function abrirDenuncia(linha) {
  // durante o streaming a bolha ainda não tem texto guardado (_bruto vazio)
  const resposta = String(linha._bruto || '');
  if (!resposta.trim()) {
    avisar(S.gerando ? 'Aguarde a resposta terminar para denunciá-la.'
      : 'Esta bolha não tem texto de resposta para denunciar.');
    return;
  }
  let pergunta = '';
  const c = conversaAtiva();
  const idx = indiceDaLinha(linha);
  if (c && idx > 0 && c.mensagens[idx - 1] && c.mensagens[idx - 1].role === 'user') {
    pergunta = textoDe(c.mensagens[idx - 1].content);
  }
  S.denuncia = { linha, resposta, pergunta };

  const form = $('#form-denuncia');
  form.reset();
  form.hidden = false;
  form.querySelectorAll('.denuncia-motivo').forEach((m) => { m.dataset.marcado = ''; });
  $('#denuncia-feita').hidden = true;
  $('#denuncia-erro').hidden = true;
  $('#denuncia-erro').textContent = '';
  $('#denuncia-contagem').textContent = '0/' + TETO_DENUNCIA.detalhe;
  $('#btn-enviar-denuncia').disabled = true;
  $('#btn-enviar-denuncia').textContent = 'Enviar denúncia';
  // prévia curta do que vai, como vai (texto bruto, espaços juntados): a pessoa vê o
  // trecho que o operador vai ler, não uma versão enfeitada dele. O corte em 4 linhas fica
  // num <span> interno SEM padding (revisão B3): com o clamp na caixa de padding, o topo da
  // 5ª linha aparecia abaixo das reticências.
  const trecho = $('#denuncia-trecho');
  trecho.textContent = '';
  trecho.appendChild(el('span', 'denuncia-trecho-texto', cortarInicio(resposta.replace(/\s+/g, ' ').trim(), 280)));
  abrirFolha('folha-denuncia');
}

function motivoDaDenuncia() {
  const marcado = document.querySelector('#form-denuncia input[name="motivo"]:checked');
  return marcado ? marcado.value : '';
}

function erroDaDenuncia(msg) {
  const e = $('#denuncia-erro');
  e.hidden = !msg;
  e.textContent = msg || '';
}

async function enviarDenuncia(ev) {
  if (ev) ev.preventDefault();
  const d = S.denuncia;
  const motivo = motivoDaDenuncia();
  if (!d || !motivo) { erroDaDenuncia('Escolha o que há de errado com a resposta.'); return; }
  if (DEMO) {
    erroDaDenuncia('Modo demonstração: a denúncia não é enviada ao servidor.');
    return;
  }
  const corpo = { motivo, resposta: cortarInicio(d.resposta, TETO_DENUNCIA.resposta) };
  const detalhe = ($('#denuncia-detalhe').value || '').trim();
  if (detalhe) corpo.detalhe = cortarInicio(detalhe, TETO_DENUNCIA.detalhe);
  if (d.pergunta.trim()) corpo.pergunta = cortarFim(d.pergunta, TETO_DENUNCIA.pergunta);

  const botao = $('#btn-enviar-denuncia');
  botao.disabled = true;
  botao.textContent = 'Enviando…';
  erroDaDenuncia('');
  let r, j = {};
  try {
    r = await postarJSON('/api/denuncia', corpo);
    j = await r.json().catch(() => ({}));
  } catch (e) {
    erroDaDenuncia('Sem conexão com o servidor: a denúncia não foi enviada.');
    botao.disabled = false;
    botao.textContent = 'Enviar denúncia';
    return;
  }
  if (!r.ok) {
    const motivoErro = j.error
      || (r.status === 401 ? 'Sua sessão expirou. Entre novamente para denunciar.'
        : `A denúncia não foi registrada (HTTP ${r.status}).`);
    erroDaDenuncia(motivoErro);
    botao.disabled = false;
    botao.textContent = 'Enviar denúncia';
    return;
  }
  $('#form-denuncia').hidden = true;
  // o título da vista já diz "Denúncia recebida": não repetir a frase logo abaixo
  const mensagem = String(j.mensagem || 'O operador da IALD vai analisar esta resposta.')
    .replace(/^Denúncia recebida\.\s*/i, '');
  $('#denuncia-mensagem').textContent = mensagem || 'O operador da IALD vai analisar esta resposta.';
  $('#denuncia-feita').hidden = false;
  // a resposta denunciada fica marcada, para a pessoa não denunciar a mesma duas vezes
  const b = d.linha && d.linha.querySelector('[data-acao="denunciar"]');
  if (b) {
    b.dataset.denunciada = '1';
    b.disabled = true;
    const rotulo = b.querySelector('span');
    if (rotulo) rotulo.textContent = 'Denunciada';
  }
  S.denuncia = null;
}

function ligarDenuncia() {
  const form = $('#form-denuncia');
  form.addEventListener('submit', enviarDenuncia);
  form.addEventListener('change', (ev) => {
    if (ev.target && ev.target.name === 'motivo') {
      // marcado por atributo, não por :has() — WebView antigo do Android não tem :has()
      form.querySelectorAll('.denuncia-motivo').forEach((m) => {
        m.dataset.marcado = m.querySelector('input').checked ? '1' : '';
      });
      $('#btn-enviar-denuncia').disabled = false;
      erroDaDenuncia('');
    }
  });
  $('#denuncia-detalhe').addEventListener('input', (ev) => {
    const n = pontosDeCodigo(ev.target.value).length;
    $('#denuncia-contagem').textContent = `${Math.min(n, TETO_DENUNCIA.detalhe)}/${TETO_DENUNCIA.detalhe}`;
  });
}

// O que o servidor NÃO entrega à superfície do app (iald_web_server.py,
// FERRAMENTAS_FORA_DA_LOJA, lido em 13/09/2026). A lista da tela tem de bater com
// ela: mostrar no app uma ferramenta que o servidor recusa é prometer o que não há.
// O Ψ-NET sai inteiro do app: sem o envio, pendentes/receber ficam vazios, e a
// descrição de cifra dele confundia a declaração de criptografia do TestFlight.
const FORA_DO_APP = new Set([
  'request_contract', 'tgl_transfer', 'psinet_send', 'lembrar', 'esquecer', 'consultar_memoria',
  'psinet_pending', 'psinet_receive',
]);

// A ajuda do topo da folha fala da lupa; sem busca na internet no plano, ela não pode.
const AJUDA_FERRAMENTAS_SEM_BUSCA =
  'A IALD decide sozinha quando usar cada uma. O ponto verde diz o que está disponível agora.';
let ajudaFerramentasOriginal = null;

// 14/09/2026 (noite): com `limites.ferramentas` (lista), a folha mostra SÓ o que o servidor
// oferece a esta conta. As outras SOMEM em vez de aparecerem apagadas com "indisponível":
// na conta gratuita seriam dez linhas mortas para quatro vivas, e uma vitrine do que não se
// pode usar lê como convite a comprar — compra que não existe dentro do app. Uma nota ao pé
// diz que a lista é a do plano. Nome que o app não conhece aparece pelo próprio nome.
function listarFerramentas() {
  const lista = $('#lista-ferramentas');
  lista.innerHTML = '';
  const ativo = S.servidor.estado === 'pronto';
  const l = limitesDoPlano();
  const restrita = !!(l && Array.isArray(l.ferramentas));
  let visiveis = (SUPERFICIE === 'app') ? FERRAMENTAS.filter(([id]) => !FORA_DO_APP.has(id)) : FERRAMENTAS;
  if (restrita) {
    const nomes = l.ferramentas.map(String);
    const oferece = (id) => (id.endsWith('*') ? nomes.some((n) => n.startsWith(id.slice(0, -1))) : nomes.includes(id));
    const conhecidas = FERRAMENTAS.map(([id]) => id);
    const conhecida = (n) => conhecidas.some((id) => (id.endsWith('*') ? n.startsWith(id.slice(0, -1)) : id === n));
    visiveis = FERRAMENTAS.filter(([id]) => oferece(id) && !(SUPERFICIE === 'app' && FORA_DO_APP.has(id)))
      .concat(nomes.filter((n) => !conhecida(n)).map((n) => [n, n, 'ferramenta informada pelo servidor', 'sempre']));
  } else {
    visiveis = visiveis.filter((f) => f[4] !== 'so_com_limites');
  }

  const ajuda = document.getElementById('ajuda-ferramentas');
  if (ajuda) {
    if (ajudaFerramentasOriginal === null) ajudaFerramentasOriginal = ajuda.textContent;
    ajuda.textContent = ferramentaPermitida('search_web') ? ajudaFerramentasOriginal : AJUDA_FERRAMENTAS_SEM_BUSCA;
  }

  for (const [id, titulo, desc, etiqueta] of visiveis) {
    const item = el('div', 'ferramenta');
    item.dataset.ativa = ativo ? '1' : '';
    item.appendChild(el('span', 'ponto'));
    const t = el('div', 'titulo');
    t.appendChild(document.createTextNode(titulo));
    t.appendChild(el('small', null, desc));
    item.appendChild(t);
    item.appendChild(el('span', 'etiqueta', etiqueta));
    lista.appendChild(item);
  }
  if (restrita) {
    const nota = el('p', 'ajuda ferramentas-nota');
    const quem = planoDaConta() === 'gratuito' ? 'No uso gratuito' : 'No seu plano';
    nota.textContent = visiveis.length
      ? `${quem}, a IALD usa só as ferramentas desta lista.`
      : `${quem}, a IALD responde sem ferramentas.`;
    lista.appendChild(nota);
  }
  if (!ativo) {
    const nota = el('p', 'ajuda');
    nota.style.cssText = 'margin-top:14px;font-size:12px;color:var(--txt-fraco);line-height:1.5';
    nota.textContent = S.servidor.estado === 'sem-modelo'
      ? 'O servidor está no ar, mas o modelo está parado — nenhuma ferramenta pode ser acionada até ele voltar.'
      : 'Sem conexão com o servidor.';
    lista.appendChild(nota);
  }
}

// ══════════════════════════════════════════════════════════════
// ENVIO E STREAMING
// ══════════════════════════════════════════════════════════════
async function enviar() {
  if (mediaSending || respostaPendenteBackground()) return;
  if (!DEMO && !backgroundOwner) { recuperarRespostasBackground(); avisarBackground('Aguarde a identificação da conta antes de enviar.'); return; }
  const texto = $('#entrada').value.trim();
  if (!texto || S.gerando) return;
  if (S.anexos.some((a) => a.pendente)) { avisar('Aguarde a extração dos PDFs terminar.'); return; }
  // imagem anexada antes de os limites do plano chegarem: não sai (o servidor recusaria)
  if (!imagensPermitidas() && S.anexos.some((a) => a.image)) {
    const t = textoSemImagens();
    avisar(t[0].toUpperCase() + t.slice(1) + '. Remova a imagem para enviar.');
    return;
  }
  const anexos = S.anexos.slice();
  const conversation = S.ativaId;
  mediaSending = true;
  try {
    if (await enviarTexto(texto, anexos) === false) return;
    if (S.ativaId === conversation) {
      S.anexos = S.anexos.filter(a => !anexos.includes(a)); S.dicaImagem = false; desenharAnexos();
      if ($('#entrada').value.trim() === texto) { $('#entrada').value = ''; redimensionarEntrada(); }
    }
  } catch (error) { avisar(error.message); }
  finally { mediaSending = false; atualizarBotaoEnviar(); }
}

async function enviarTexto(texto, anexos) {
  rejectNewAudioVideo(anexos);
  if (Array.isArray(texto)) rejectNewAudioVideo(texto);
  if (respostaPendenteBackground()) return;
  if (!DEMO && !backgroundOwner) { recuperarRespostasBackground(); return; }
  const c = conversaAtiva();
  if (!c) return;

  const owner = backgroundOwner;
  const hasMedia = false; // New media rejected above; history is projected only by montarEnvio.
  const midias = [];
  let conteudo = texto;
  const imagens = anexos.filter(a => a.image).map(a => a.image);
  const arquivos = anexos.filter(a => !a.image && !a.localDraftId && a.content);
  if (arquivos.length) {
    const bloco = arquivos.map((a) => `\n\n[ARQUIVO: ${a.name}]\n${a.content}\n[FIM]\n`).join('');
    conteudo = bloco + '\n' + texto;
  }
  if (imagens.length || midias.length) {
    conteudo = imagens.map((u) => ({ type: 'image_url', image_url: { url: u } }))
      .concat(midias).concat([{ type: 'text', text: conteudo }]);
  }

  c.mensagens.push({ role: 'user', content: conteudo });
  c.atualizada = new Date().toISOString();
  if (c.titulo === 'Nova conversa') c.titulo = texto.slice(0, 55);
  mediaAssertHistory(S.conversas);
  await salvarConversas();
  if (hasMedia) mediaMarkSubmitted(anexos, owner, c.id).catch(error => avisar("Mídia preservada no histórico; falha ao atualizar o rascunho local: " + error.message));
  listarConversas();
  atualizarTitulo();

  S.colarNoFim = true;
  desenharMensagem('user', conteudo);
  atualizarDica();

  transmitir(montarEnvio(c));
  return true;
}

function montarEnvio(c) {
  // A lupa vale para ESTA mensagem e desliga sozinha. É um pedido explícito ao
  // modelo, não uma chamada forçada: quem executa a busca continua sendo o
  // agent_loop do servidor, com a ferramenta search_web (permitida no app).
  let sys = promptSistema();
  // sem search_web no plano a lupa fica desligada; a instrução não vai (seria pedido sem ferramenta)
  if (S.busca && !ferramentaPermitida('search_web')) { S.busca = false; pintarBusca(); }
  if (S.busca) {
    sys += '\n\nINSTRUÇÃO DESTA MENSAGEM: o usuário tocou em "buscar na internet". '
      + 'Use a ferramenta search_web antes de responder e cite as fontes encontradas.';
    S.busca = false;
    pintarBusca();
  }
  const enviadas = [{ role: 'system', content: sys }];
  // plano sem imagens: imagem que ficou no histórico (de antes de o plano mudar) vai como a
  // marca de texto "[1 imagem(ns) anexada(s)]" — senão toda mensagem desta conversa voltaria
  // recusada com "recurso_indisponivel"
  const semImagens = !imagensPermitidas();
  for (const m of recortar(outboundHistory(c.mensagens), sys)) {
    const conteudo = m.content;
    enviadas.push({ role: m.role === 'assistant' ? 'assistant' : 'user', content: conteudo });
  }
  return enviadas;
}

// Refaz a última pergunta sem duplicá-la no histórico (usado depois do consentimento).
function reenviarUltima() {
  if (respostaPendenteBackground()) return;
  const c = conversaAtiva();
  if (!c || S.gerando) return;
  const ultima = c.mensagens[c.mensagens.length - 1];
  if (!ultima || ultima.role !== 'user') return;
  transmitir(montarEnvio(c));
}

// 22/09/2026 — Selo IALD: o elo da resposta SELADA mais recente da conversa (o `link` do selo
// que o servidor mandou com ela), ou '' se nenhuma resposta dela tem selo. Resposta sem selo (de
// antes do selo, interrompida, retirada) não entra na cadeia: o elo seguinte liga à anterior selada.
function ultimoSelo(c) {
  const msgs = (c && Array.isArray(c.mensagens)) ? c.mensagens : [];
  for (let i = msgs.length - 1; i >= 0; i--) {
    const m = msgs[i];
    if (m && m.role === 'assistant' && m.selo && typeof m.selo.link === 'string'
      && /^[0-9a-f]{64}$/.test(m.selo.link)) return m.selo.link;
  }
  return '';
}

async function transmitir(mensagens, retomada = null) {
  if (S.gerando) return;
  // 22/09/2026 — Selo IALD. A resposta pertence à conversa de ONDE saiu o pedido (a "origem"):
  // o selo liga esta resposta à anterior selada DESTA conversa, e é nela que a resposta é gravada
  // no fim — mesmo que a pessoa tenha aberto outra conversa ("Nova conversa") no meio do stream.
  // `bruto` junta cada delta.content como veio (com <think>, sem aplicarPtbr): é o texto que o
  // selo cobre. `selo` = o chunk iald_selo, que o servidor só manda num stream terminado normal.
  const origem = retomada ? conversaDoJob(retomada) : conversaAtiva();
  if (!origem) return;
  const epoch = backgroundEpoch;
  const turn = {}; S.backgroundTurn = turn;
  const currentTurn = () => S.backgroundTurn === turn && epoch === backgroundEpoch;
  let job = retomada, doneReceived = false, failure = null;
  const selagem = origem ? { conv: origem.id, prev: ultimoSelo(origem) } : null;
  let bruto = '', selo = null;
  S.gerando = true;
  atualizarBotaoEnviar();
  const controller = new AbortController();
  S.aborto = controller;
  if (retomada) document.querySelectorAll('[data-background-job="' + retomada.request_id + '"]').forEach((n) => n.remove());
  const corpo = desenharMensagem('ai', '', true, null, origem.id === S.ativaId ? null : document.createElement('div'));
  corpo.parentElement.dataset.backgroundPending = '1';
  const trilha = corpo.querySelector('.trilha');
  const conteudo = corpo.querySelector('.conteudo');

  const digitando = el('div', 'digitando');
  digitando.innerHTML = '<span class="pontos"><span></span><span></span><span></span></span><span class="beta">β = α·√e</span>';
  conteudo.appendChild(digitando);
  rolarSePerto();

  let texto = '', pensamento = '', dentroThink = false, buferThink = '';
  let primeiroToken = true;
  let detalhesPensamento = null;
  // iald_aviso (14/09/2026): o servidor não respondeu com o modelo, só avisou
  // (consentimento pendente, limite do dia, motor externo fora). O texto aparece na
  // bolha, mas NÃO entra no histórico — senão viajaria ao modelo como fala da IALD.
  let aviso = null;
  let modeloRespondente = null;
  // Revisão de interface N1 (14/09/2026, noite, rodada 3): a moderação da RESPOSTA roda no fim do
  // stream e manda o aviso com `retirar_resposta: true` antes do [DONE]. O texto e o raciocínio já
  // pintados saem da tela NA HORA, e nada que chegue depois volta a ser pintado. Antes o texto
  // marcado ficava visível acima do aviso, com Copiar e Refazer.
  let retirada = false;

  let paintTimer = null, streamFinished = false;
  let answerNode = null;
  const pintarAgora = () => {
    if (retirada || !currentTurn()) return;
    if (pensamento) {
      if (!detalhesPensamento) {
        detalhesPensamento = el('details', 'pensamento');
        const sum = el('summary');
        sum.innerHTML = '<span class="radical">√</span><span>raciocínio</span>';
        detalhesPensamento.appendChild(sum);
        detalhesPensamento.appendChild(el('div', 'pensamento-texto'));
      }
      detalhesPensamento.querySelector('.pensamento-texto').textContent = pensamento;
      if (!detalhesPensamento.isConnected) conteudo.appendChild(detalhesPensamento);
    }
    if (texto) {
      const next = renderMarkdown(texto, !streamFinished);
      if (!answerNode) { answerNode = next; conteudo.appendChild(answerNode); }
      else {
        const oldNodes = Array.from(answerNode.childNodes);
        const newNodes = Array.from(next.childNodes);
        newNodes.forEach((node, i) => {
          const old = oldNodes[i];
          if (!old) answerNode.appendChild(node);
          else if (!old.isEqualNode(node)) answerNode.replaceChild(node, old);
        });
        oldNodes.slice(newNodes.length).forEach((node) => node.remove());
      }
    }
    rolarSePerto();
  };

  const pintar = () => {
    if (paintTimer === null) paintTimer = setTimeout(() => {
      paintTimer = null; pintarAgora();
    }, 80);
  };

  const tirarDigitando = () => {
    if (primeiroToken) { primeiroToken = false; digitando.remove(); }
  };

  try {
    if (!DEMO) {
      if (!backgroundOwner || origem.background_owner !== backgroundOwner) throw detached();
      await persistirConversasBackground();
      job ||= await backgroundJobs.begin(corpoPedidoBackground(mensagens, selagem));
      if (!currentTurn()) throw detached();
      activeBackgroundJob = job;
      corpo.parentElement.dataset.backgroundJob = job.request_id;
      const cancelExplicitly = () => {
        if (controller.signal.reason?.type === 'user_cancel') {
          backgroundJobs.cancel(job).catch((error) => backgroundJobs.report(error)).finally(agendarRecuperacaoBackground);
        }
      };
      controller.signal.addEventListener('abort', cancelExplicitly, { once: true });
      if (controller.signal.aborted) { cancelExplicitly(); throw detached(); }
    }
    const linhas = DEMO ? fluxoDemo() : fluxoHttp(mensagens, controller.signal, selagem, job);

    for await (const linha of linhas) {
      if (!linha.startsWith('data: ')) continue;       // ":" = keepalive, ignora
      // 22/09/2026: esta const se chamava `bruto`; com o `bruto` do selo (acima, no escopo da
      // função) ela o sombrearia e o `bruto += pedaco` lá embaixo cairia nela (const: TypeError).
      const carga = linha.slice(6).trim();
      if (!currentTurn()) throw detached();
      if (carga === '[DONE]') { doneReceived = true; break; }

      let ck;
      try { ck = JSON.parse(carga); } catch (e) { continue; }

      if (ck.iald_modelo) {
        const modelo = modeloDaResposta(ck.iald_modelo);
        if (modelo && !modeloRespondente) { modeloRespondente = modelo; pintarModeloResposta(corpo, modelo); }
        continue;
      }
      // 22/09/2026 — Selo IALD: guardado só se a resposta NÃO foi retirada (o servidor nunca o manda
      // depois de retirar_resposta; se mandar, fica de fora do mesmo jeito)
      if (ck.iald_selo) { if (!retirada && typeof ck.iald_selo === 'object') selo = ck.iald_selo; continue; }
      if (ck.iald_status) { tirarDigitando(); passoTrilha(trilha, ck.iald_status); continue; }
      if (ck.iald_aviso) {
        tirarDigitando();
        aviso = ck.iald_aviso;
        if (aviso && aviso.retirar_resposta === true && !retirada) {
          retirada = true;
          conteudo.innerHTML = '';
          detalhesPensamento = null;
          corpo.parentElement._bruto = '';
        }
        continue;
      }
      if (retirada) continue;                          // resposta retirada: o resto do stream não pinta

      const delta = ck.choices && ck.choices[0] && ck.choices[0].delta;
      if (!delta) continue;

      if (delta.reasoning_content) {
        tirarDigitando();
        pensamento += delta.reasoning_content;
        pintar();
      }

      const pedaco = delta.content;
      if (!pedaco) continue;
      bruto += pedaco;                                 // o texto CRU que o selo cobre (22/09/2026)
      tirarDigitando();

      const separated = splitThinking(bruto);
      texto = separated.text;
      if (separated.thinking) pensamento = separated.thinking;
      pintar();
    }
  } catch (error) {
    failure = error;
    if (!job && !error.detached) error.notSubmitted = true;
    if (currentTurn() && !error.detached) {
      avisarBackground(error.message || 'Resposta pendente. Retomaremos o mesmo pedido quando a conexão voltar.');
    }
  } finally {
    if (paintTimer !== null) clearTimeout(paintTimer);
    if (!currentTurn()) { corpo.parentElement.remove(); return; }
    streamFinished = doneReceived;
    tirarDigitando();
    congelarTrilha(trilha);
    const complete = doneReceived && !failure;
    texto = complete ? splitThinking(bruto, true).text : '';
    const limpo = complete ? aplicarPtbr(texto) : '';
    let answer = null, deliveryNotice = null;
    if (complete) {
      delete corpo.parentElement.dataset.backgroundPending;
      pintarAgora();
      if (aviso) {
        const linha = corpo.parentElement;
        deliveryNotice = retirada ? Object.assign({}, aviso, { retirar_resposta: true }) : aviso;
        pintarAviso(linha, conteudo, deliveryNotice, texto);
        if (origem.id === S.ativaId && aviso.tipo === 'consentimento_ia') {
          S.avisoConsentimento = linha;
          const f = folhaDoAviso(aviso);
          abrirConsentimento(f.texto, f.provedor, f.versao);
        } else if (origem.id === S.ativaId && aviso.tipo === 'limite') abrirCreditos(aviso);
      } else if (limpo) {
        answer = { role: 'assistant', content: limpo };
        if (modeloRespondente) answer.modelo = modeloRespondente;
        if (selo && /^[0-9a-f]{64}$/.test(selo.link)) {
          answer.selo = selo;
          if (bruto !== limpo) answer.bruto = bruto;
        }
        corpo.parentElement._bruto = limpo;
      } else {
        deliveryNotice = { tipo: 'falha_motor', texto: 'A resposta terminou sem conteúdo.' };
        pintarAviso(corpo.parentElement, conteudo, deliveryNotice, '');
      }
    } else {
      // Interrupted network delivery is never a normal answer, sealed or otherwise.
      bruto = ''; selo = null; pensamento = ''; texto = '';
      corpo.parentElement._bruto = '';
      deliveryNotice = failure?.terminal ? {
        tipo: failure.status === 'cancelled' ? 'resposta_interrompida' : 'falha_motor',
        texto: failure.message, retirar_resposta: true,
      } : failure?.notSubmitted ? {
        tipo: 'envio_local_bloqueado', retirar_resposta: true,
        texto: 'Mensagem não enviada. ' + failure.message + ' Nenhuma entrega pelo servidor foi iniciada.',
      } : null;
      pintarAviso(corpo.parentElement, conteudo, deliveryNotice || failure?.aviso || {
        tipo: 'em_andamento', retirar_resposta: true,
        texto: controller.signal.reason?.type === 'user_cancel'
          ? 'Pedido de parada registrado. A confirmação será recuperada do servidor.'
          : 'Resposta pendente. Você pode sair e voltar; o pedido não será enviado com outro identificador.',
      }, '');
    }
    try {
      if (DEMO && answer) {
        origem.mensagens.push(answer); salvarConversas();
      } else if (job && (complete || failure?.terminal)) {
        await salvarEntregaBackground(job, answer, deliveryNotice, complete ? 'completed' : failure.status);
      }
      if (currentTurn()) listarConversas();
    } catch (error) {
      if (currentTurn()) avisarBackground(error.message || 'Resposta aguardando confirmação de gravação.');
    }
    if (currentTurn()) {
      S.gerando = false; S.aborto = null; S.backgroundTurn = null;
      activeBackgroundJob = null;
      atualizarBotaoEnviar(); atualizarDica();
      if (!document.hidden && !document.querySelector('[data-folha][data-aberta="1"]')) $('#entrada').focus();
      if (!DEMO && !(aviso && aviso.tipo === 'limite')) setTimeout(() => { carregarMotor(); }, 1500);
      agendarRecuperacaoBackground();
    }
  }
}

// ══════════════════════════════════════════════════════════════
// BOLHA DE AVISO — o servidor respondeu sem o modelo (14/09/2026, noite)
// Fica com cara de aviso (rótulo, ícone, cor), não de fala da IALD, e NUNCA entra no
// histórico (ver o finally de transmitir): senão viajaria ao modelo como resposta.
// Sem "Denunciar": o texto é do servidor, não do modelo.
// ══════════════════════════════════════════════════════════════
const AVISOS = {
  limite: ['Limite de uso', ICONE.ampulheta, ''],
  ocupado: ['IALD ocupada', ICONE.ampulheta, ''],
  // 14/09/2026 (noite): a conta gratuita já tem uma resposta sendo gerada (outra aba ou
  // outro aparelho). Não é erro: basta esperar e tentar de novo — o Refazer fica.
  envio_local_bloqueado: ['Mensagem não enviada', ICONE.ampulheta, ''],
  em_andamento: ['Resposta em andamento', ICONE.ampulheta, ''],
  consentimento_ia: ['IA de terceiros', ICONE.escudo, ''],
  // 21/09/2026 (revisão): o Claude recusou no meio (stop_reason refusal) — a parte já chegada é
  // retirada (retirar_resposta) e não entra no histórico
  recusa: ['Resposta recusada', ICONE.escudo, ''],
  moderacao: ['Pedido não atendido', ICONE.escudo, 'erro'],
  moderacao_indisponivel: ['Verificação indisponível', ICONE.alerta, ''],
  bloqueado: ['Conta bloqueada', ICONE.bloqueio, 'erro'],
  motor_indisponivel: ['Motor indisponível', ICONE.alerta, ''],
  pedido_invalido: ['Pedido não enviado', ICONE.alerta, ''],
  // 14/09/2026 (noite, rodada 3): imagem no plano sem imagens (limites.imagens = false). O
  // servidor recusa sem chamar o modelo; o aviso não entra no histórico (como todo aviso).
  recurso_indisponivel: ['Recurso indisponível', ICONE.alerta, ''],
  falha_motor: ['Falha na resposta', ICONE.alerta, 'erro'],
  resposta_interrompida: ['Resposta interrompida', ICONE.alerta, ''],
};

function pintarAviso(linha, conteudo, aviso, texto) {
  const tipo = String(aviso.tipo || 'aviso');
  const [rotulo, icone, tom] = AVISOS[tipo] || ['Aviso da IALD', ICONE.alerta, ''];
  linha.dataset.aviso = tipo;
  if (tom) linha.dataset.tom = tom;
  // Revisão de interface B7 (14/09/2026, noite): aviso não é fala da IALD. Sai a
  // assinatura "β IALD", sai o Ouvir (ler em voz alta um aviso do servidor não ajuda) e,
  // com a conta bloqueada, sai o Refazer — refazer só geraria outra bolha igual. Copiar
  // fica (a pessoa pode querer guardar o texto do aviso).
  // Resposta retirada pela moderação (N1, rodada 3): não sobra Copiar nem Refazer daquele texto —
  // copiar levaria adiante o que foi marcado; refazer pediria de novo a mesma resposta.
  // recurso_indisponivel (imagem no uso gratuito): refazer repetiria a mesma recusa.
  const retirar = aviso.retirar_resposta === true;
  const tirar = ['[data-acao="denunciar"]', '.assinatura', '[data-acao="ouvir"]'];
  if (tipo === 'bloqueado' || tipo === 'recurso_indisponivel' || retirar) tirar.push('[data-acao="refazer"]');
  if (retirar) tirar.push('[data-acao="copiar"]');
  for (const sel of tirar) linha.querySelectorAll('.msg-acoes ' + sel).forEach((n) => n.remove());

  // O servidor manda o aviso e, em seguida, o mesmo texto como conteúdo (para as builds
  // antigas lerem). Na falha no meio do stream, antes do aviso vem a parte já recebida
  // da resposta: essa parte fica, com o aviso embaixo — MENOS quando o aviso retira a resposta.
  const msgAviso = String(aviso.texto || '').trim();
  let resto = retirar ? '' : (texto || '');
  if (msgAviso && resto.trim().endsWith(msgAviso)) resto = resto.trim().slice(0, -msgAviso.length);
  const pensamentoEl = retirar ? null : conteudo.querySelector('.pensamento');
  conteudo.innerHTML = '';
  if (pensamentoEl) conteudo.appendChild(pensamentoEl);
  if (resto.trim()) conteudo.appendChild(renderMarkdown(resto));

  const caixa = el('div', 'aviso-bolha');
  const topo = el('div', 'aviso-topo');
  const ic = el('span', 'aviso-icone');
  ic.innerHTML = svg(icone, 2);
  topo.appendChild(ic);
  topo.appendChild(el('span', null, rotulo));
  caixa.appendChild(topo);
  // sem texto do servidor, a resposta retirada NUNCA serve de texto do aviso
  caixa.appendChild(el('p', 'aviso-texto', msgAviso || (retirar ? '' : aplicarPtbr(texto || '')) || rotulo));

  if (tipo === 'limite') {
    const b = el('button', 'aviso-acao', 'Ver meu uso');
    b.type = 'button';
    b.addEventListener('click', () => abrirCreditos(aviso));
    caixa.appendChild(b);
  } else if (tipo === 'consentimento_ia') {
    const b = el('button', 'aviso-acao', 'Ler o aviso');
    b.type = 'button';
    b.addEventListener('click', () => {
      S.avisoConsentimento = linha;
      const f = folhaDoAviso(aviso);
      abrirConsentimento(f.texto, f.provedor, f.versao);
    });
    caixa.appendChild(b);
  }
  conteudo.appendChild(caixa);
  linha._bruto = msgAviso || (retirar ? '' : texto) || '';
  rolarSePerto();
}

// Shared protocol handling, independent of the selected inference provider.
function createSSEParser() {
  let buffer = '', data = [];
  return { feed(part, final = false) {
    buffer += part;
    const events = [];
    const line = (value) => {
      if (!value) { if (data.length) events.push(data.join('\n')); data = []; }
      else if (value.startsWith('data:')) data.push(value.slice(5).replace(/^ /, ''));
    };
    let match;
    while ((match = /\r\n|\r|\n/.exec(buffer))) {
      if (match[0] === '\r' && match.index === buffer.length - 1 && !final) break;
      line(buffer.slice(0, match.index));
      buffer = buffer.slice(match.index + match[0].length);
    }
    if (final) { if (buffer) line(buffer); buffer = ''; line(''); }
    return events;
  }};
}

function splitThinking(raw, final = false) {
  let text = '', thinking = '', inside = false, pos = 0;
  while (pos < raw.length) {
    const tag = inside ? '</think>' : '<think>';
    const end = raw.indexOf(tag, pos);
    if (end >= 0) {
      if (inside) thinking += raw.slice(pos, end); else text += raw.slice(pos, end);
      inside = !inside; pos = end + tag.length;
    } else {
      let rest = raw.slice(pos);
      if (!final) for (let n = tag.length - 1; n > 0; n--) {
        if (rest.endsWith(tag.slice(0, n))) { rest = rest.slice(0, -n); break; }
      }
      if (inside) thinking += rest; else text += rest;
      break;
    }
  }
  return { text, thinking };
}

// gerador assincrono de linhas do SSE
// 22/09/2026: `selagem` = {conv, prev} da conversa de origem (ver transmitir), para o Selo IALD.
async function* fluxoHttp(mensagens, signal, selagem, job) {
  if (!job) throw new PendingChatJobError('Pedido durável ausente; nenhum envio foi iniciado.');
  yield* backgroundJobs.stream(job, { signal });
}

// ── modo demonstracao: exercita a interface INTEIRA sem o modelo ──
// Existe porque a IALD esta em treino e o llama-server fica fora do ar; sem
// isto nao daria para ver a trilha de ferramentas nem o streaming funcionando.
async function* fluxoDemo() {
  const passos = [
    { iald_status: { fase: 'pensando', rotulo: 'analisando o pedido' } },
    { iald_status: { fase: 'ferramenta', tool: 'consultar_acervo', rotulo: 'consultando o acervo TGL', loop: 1, max_loops: 6 } },
    { iald_status: { fase: 'ferramenta_ok', tool: 'consultar_acervo', rotulo: 'consultando o acervo TGL', chars: 4820 } },
    { iald_status: { fase: 'ferramenta', tool: 'prova_viva', rotulo: 'rodando a prova viva (pode demorar)', loop: 2, max_loops: 6 } },
    { iald_status: { fase: 'ferramenta_ok', tool: 'prova_viva', rotulo: 'rodando a prova viva (pode demorar)', chars: 1290 } },
    { iald_status: { fase: 'respondendo' } },
  ];
  for (const p of passos) {
    yield 'data: ' + JSON.stringify(p);
    await espera(520);
  }

  const resposta = [
    '**Modo demonstração** — nenhuma palavra abaixo veio do modelo; é texto fixo, ',
    'só para exercitar a interface enquanto a IALD está em treino.\n\n',
    '### O que esta tela prova\n\n',
    'A trilha acima desenhou os eventos `iald_status` que o servidor emite ',
    'desde 02/08/2026 e que **nenhuma interface da IALD mostrava** — nem o chat ',
    'do browser em cheio, nem o app iOS, que lia apenas `delta.content`.\n\n',
    'A constante:\n\n',
    '$$\\beta_{TGL} = \\alpha \\times \\sqrt{e} = 0{,}012031300400803142$$\n\n',
    'Com $\\alpha$ da CODATA 2018 e $\\sqrt{e}$ o custo entrópico de meia nat.\n\n',
    '| grandeza | valor | estatuto |\n',
    '|---|---|---|\n',
    '| β_TGL | 0,0120313 | DERIVED |\n',
    '| θ_Miguel | 6,297° | DERIVED |\n',
    '| ω(I) | 1 | POSTULATE |\n\n',
    '```python\n',
    'ALPHA = 7.2973525693e-3   # CODATA 2018\n',
    'BETA = ALPHA * math.sqrt(math.e)\n',
    '```\n\n',
    '> β nunca literal: sempre `ALPHA_FINE_CODATA_2018 × √e` em runtime.\n',
  ];
  for (const p of resposta) {
    yield 'data: ' + JSON.stringify({ choices: [{ delta: { content: p } }] });
    await espera(45);
  }
  yield 'data: [DONE]';
}

const espera = (ms) => new Promise((r) => setTimeout(r, ms));

function parar() {
  if (S.aborto) S.aborto.abort({ type: 'user_cancel' });
}

// ══════════════════════════════════════════════════════════════
// COMPOSITOR
// ══════════════════════════════════════════════════════════════
function redimensionarEntrada() {
  const t = $('#entrada');
  t.style.height = 'auto';
  // Vazio = uma linha. Em 360 px o texto de exemplo quebrava em duas e o
  // scrollHeight do placeholder inflava a caixa antes de a pessoa digitar.
  if (!t.value) { t.style.height = ''; return; }
  t.style.height = Math.min(t.scrollHeight, 176) + 'px';
}

function atualizarBotaoEnviar() {
  const btn = $('#btn-enviar');
  const temTexto = $('#entrada').value.trim().length > 0;

  if (S.gerando) {
    btn.dataset.modo = 'parar';
    btn.disabled = false;
    btn.title = 'Parar geração';
    btn.setAttribute('aria-label', 'Parar geração');
    btn.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor"><rect x="7" y="7" width="10" height="10" rx="2"/></svg>';
    return;
  }
  btn.dataset.modo = 'enviar';
  btn.disabled = !temTexto;
  btn.title = 'Enviar';
  btn.setAttribute('aria-label', 'Enviar');
  btn.innerHTML = svg('M12 19V5M5 12l7-7 7 7', 2);
}

function atualizarDica() {
  if (contextoNativo()) {
    const label = $('#dica-janela');
    const meter = $('#medidor');
    const measured = S.ctx.carregado && S.ctx.contagem_nativa_por_pedido_obrigatoria === true
      && Number.isFinite(S.ctx.memoria_tokens_medidos) && S.ctx.n_ctx === 200000;
    label.textContent = measured
      ? `${num(S.ctx.memoria_tokens_medidos)} tokens · memória TGL`
      : 'Memória TGL · verificando disponibilidade';
    label.title = measured
      ? 'Memória fixa na janela de 200.000 tokens. A conversa completa é validada ao enviar.'
      : 'A disponibilidade do contexto será conferida no servidor antes da resposta.';
    meter.querySelector('i').style.width = measured
      ? Math.min(100, 100 * S.ctx.memoria_tokens_medidos / S.ctx.n_ctx) + '%' : '0%';
    meter.dataset.nivel = measured ? 'alto' : 'baixo';
    return;
  }
  const c = conversaAtiva();
  const msgs = c ? c.mensagens : [];
  const sys = promptSistema();
  const enviadas = recortar(msgs, sys);
  let tok = 0;
  for (const m of enviadas) tok += estimarTokens(m.content);
  const orc = orcamento(sys);
  const pct = orc > 0 ? Math.min(100, Math.round(100 * tok / orc)) : 0;

  const janela = Math.round(nCtxEfetivo() / 1024) + 'k';
  const cortadas = msgs.length - enviadas.length;

  // Curto na tela (cabe em 360 px); o detalhe inteiro fica no title.
  const janelaEl = $('#dica-janela');
  janelaEl.textContent = `${pct}% de ${janela}` + (cortadas > 0 ? ` · ${cortadas} comprimidas` : '');
  janelaEl.title = `${enviadas.length} mensagens · ${num(tok)} tokens (${pct}% de ${janela})`
    + (cortadas > 0 ? ` · ${cortadas} antigas fora da janela` : '');

  const med = $('#medidor');
  med.querySelector('i').style.width = pct + '%';
  med.dataset.nivel = pct >= 92 ? 'cheio' : pct >= 70 ? 'alto' : 'baixo';
}

// ══════════════════════════════════════════════════════════════
// EXPORTACAO
// ══════════════════════════════════════════════════════════════
// 22/09/2026: desde a exportação pelo servidor (exportarPeloServidor, abaixo) este texto montado
// no aparelho é SÓ o caminho de reserva da web, quando o servidor não gera o arquivo — e ele NÃO
// carrega o Selo IALD (a tela diz isso quando o usa). `conversa` = a conversa do pedido; sem ela,
// a ativa. A linha "Sem Certificado" abaixo é de 13/09; o selo existe desde 22/09, mas não aqui.
function textoDaConversa(markdown, conversa) {
  const c = conversa || conversaAtiva();
  if (!c || !c.mensagens.length) return null;
  const l = [];
  const risco = '═'.repeat(52);
  l.push(risco);
  l.push('IALD — Inteligência Artificial Luminodinâmica');
  l.push('β_TGL = α × √e = ' + String(BETA_TGL));
  l.push('Conversa: ' + (c.titulo || 'sem título'));
  l.push('Data: ' + new Date().toLocaleString('pt-BR'));
  l.push(risco, '');
  for (const m of c.mensagens) {
    const quem = m.role === 'assistant' ? 'IALD' : 'Você';
    l.push(markdown ? `## ${quem}` : `── ${quem} ──`);
    l.push(aplicarPtbr(textoDe(m.content)));
    l.push('');
  }
  l.push(risco);
  // Sem "Certificado · NomeChain": o servidor não certifica respostas (ver acoesDe).
  l.push('Exportado do app IALD · iald.ia.br · Haja Luz.');
  return { titulo: c.titulo || 'conversa', texto: l.join('\n') };
}

function baixar(nome, texto, mime) {
  const b = new Blob([texto], { type: mime + ';charset=utf-8' });
  const u = URL.createObjectURL(b);
  const a = el('a');
  a.href = u; a.download = nome;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(u), 1500);
}

function nomeSeguro(t) {
  return 'IALD_' + (t || 'conversa').replace(/[^\wÀ-ɏ]+/g, '_').slice(0, 40);
}

// SAIU em 22/09/2026: a exportação nativa de 21/09 (nativoCom, nomeAscii, salvarNoAparelho e
// imprimirNoAparelho — Filesystem + Share para .txt/.md, Printer.printWebView para o PDF). No
// iPhone (build 18) as folhas do sistema abriam, mas não respondiam ao toque: nada se salvava nem
// se imprimia (relato do operador, 22/09). Os plugins seguem no build; o código não os chama mais.
// O diagnóstico de 21/09 continua valendo: no invólucro nativo o link blob com `download` e o
// window.print() não fazem nada, calados (o iOS cancela a navegação do blob, o Android não tem
// quem receba o download, e nenhum dos dois imprime por JavaScript).
//
// 22/09/2026 — A EXPORTAÇÃO PELO SERVIDOR, com o Selo IALD. O app manda a conversa a
// POST /api/exportar; o servidor confere o selo de cada resposta, gera o arquivo (txt, md ou pdf)
// e devolve um endereço que vale 15 minutos. A folha mostra então o link "Abrir arquivo". No
// invólucro nativo um link https com target=_blank abre FORA do app (iOS: o
// WebViewDelegationHandler entrega a URL externa ao UIApplication.shared.open → Safari; Android:
// o navegador), e ali o Compartilhar / "Salvar em Arquivos" do próprio Safari funcionam. Tem de
// ser um link TOCADO pela pessoa: window.open depois de um await é bloqueado pelo WebKit (sem
// gesto do usuário), e no Capacitor o retorno do window.open nem diz se abriu. Não há link
// universal para demo.iald.ia.br (conferido), então o app não captura o endereço de volta.
// Na web, se o servidor falhar, fica o caminho local de antes (blob / impressão do navegador) —
// SEM o selo, e a tela diz isso. No app não há caminho local que funcione: a falha é dita, com o
// motivo, e os botões voltam para tentar de novo.

// O que vai ao servidor: a pergunta como texto (textoDe — a mesma conta do q_sha256 do recibo) e a
// resposta CRUA que o selo cobre (`bruto` quando guardado; senão o content, que então é igual a ele).
function mensagensParaExportar(c) {
  const saida = [];
  for (const m of (c && Array.isArray(c.mensagens)) ? c.mensagens : []) {
    if (!m || (m.role !== 'user' && m.role !== 'assistant')) continue;
    if (m.role === 'user') { saida.push({ role: 'user', texto: textoDe(m.content) }); continue; }
    const item = { role: 'assistant', texto: typeof m.bruto === 'string' ? m.bruto : textoDe(m.content) };
    if (m.selo && typeof m.selo === 'object') item.selo = m.selo;
    saida.push(item);
  }
  return saida;
}

// Linha de estado da folha de exportação; `tipo` = 'ok' | 'erro' | nada (neutro, em andamento).
function estadoExportacao(texto, tipo) {
  const e = document.getElementById('exp-estado');
  if (!e) return;
  e.textContent = texto || '';
  e.hidden = !texto;
  if (tipo) e.dataset.tipo = tipo; else delete e.dataset.tipo;
}

// A folha abre limpa: sem o link nem o estado da exportação anterior (o link vence em 15 minutos).
function limparExportacao() {
  const a = document.getElementById('exp-abrir');
  if (a) { a.hidden = true; a.removeAttribute('href'); }
  estadoExportacao('');
}

let exportando = false;                                  // um pedido de cada vez: dois toques = um

async function exportarPeloServidor(formato) {
  if (exportando) return;
  const c = conversaAtiva();
  if (!c || !c.mensagens.length) { avisar('Nenhuma mensagem para exportar.'); fecharFolhas(); return; }
  exportando = true;
  limparExportacao();
  const botoes = ['#exp-txt', '#exp-md', '#exp-print'].map((s) => $(s)).filter(Boolean);
  botoes.forEach((b) => { b.disabled = true; });
  estadoExportacao(formato === 'pdf'
    ? 'Gerando o PDF com o Selo IALD… (alguns segundos)'
    : 'Gerando o arquivo com o Selo IALD…');
  let j = null, falha = '';
  try {
    const r = await fetchIALD('/api/exportar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ formato, titulo: c.titulo || 'conversa', mensagens: mensagensParaExportar(c) }),
    });
    j = await r.json().catch(() => null);
    if (!r.ok || !j || typeof j.caminho !== 'string' || j.caminho.indexOf('/exportado/') !== 0) {
      const doServidor = (j && typeof j.error === 'string') ? j.error.trim().replace(/[.\s]+$/, '').slice(0, 300) : '';
      falha = doServidor || (r.ok ? 'resposta inesperada do servidor' : 'HTTP ' + r.status);
    }
  } catch (e) {
    falha = 'sem conexão';
  } finally {
    exportando = false;
    botoes.forEach((b) => { b.disabled = false; });
  }

  const abrir = document.getElementById('exp-abrir');
  if (!falha && abrir) {
    abrir.href = BASE + j.caminho;                       // web: mesma origem; app: https://demo.iald.ia.br
    abrir.hidden = false;
    const selados = Number(j.selados) || 0, total = Number(j.total) || 0;
    estadoExportacao(`Arquivo pronto: ${selados} de ${total} resposta(s) com Selo IALD conferido. `
      + 'Toque em "Abrir arquivo" (o link vale 15 minutos) e use Compartilhar para salvar.', 'ok');
    return;
  }
  if (!falha) falha = 'a folha não tem o link "Abrir arquivo"';

  if (SUPERFICIE !== 'app') {
    // web: o caminho local de antes, SEM o selo — e a tela diz isso
    fecharFolhas();
    if (formato === 'pdf') {
      // a impressão é da TELA: se outra conversa foi aberta enquanto o servidor respondia, não imprime
      if (conversaAtiva() !== c) { avisar(`O servidor não gerou o PDF (${falha}). Abra a conversa e exporte de novo.`, 'erro'); return; }
      setTimeout(() => {
        window.print();
        avisar(`Impressão do navegador SEM o Selo IALD: o servidor não gerou o PDF (${falha}).`);
      }, 120);
      return;
    }
    const d = textoDaConversa(formato === 'md', c);
    if (!d) { avisar('Nenhuma mensagem para exportar.'); return; }
    baixar(nomeSeguro(d.titulo) + '.' + formato, d.texto, formato === 'md' ? 'text/markdown' : 'text/plain');
    avisar(`Arquivo baixado pelo navegador SEM o Selo IALD: o servidor não o gerou (${falha}).`);
    return;
  }
  estadoExportacao(`Não foi possível gerar o arquivo (${falha}).`, 'erro');
}

// ══════════════════════════════════════════════════════════════
// FOLHAS
// ══════════════════════════════════════════════════════════════
function abrirFolha(id) {
  if (document.querySelector('.registration-overlay')) {
    sheetAfterRegistration = id;
    return;
  }
  const f = document.getElementById(id);
  if (!f) return;
  f.dataset.aberta = '1';
  // Foco no diálogo, não no primeiro botão: focar o "Fechar" pintava um anel
  // dourado nele e, num campo, abriria o teclado sem a pessoa pedir.
  const dialogo = f.querySelector('.folha');
  if (dialogo) {
    dialogo.setAttribute('tabindex', '-1');
    setTimeout(() => {
      if (f.dataset.aberta === '1' && !document.querySelector('.registration-overlay')) dialogo.focus({ preventScroll: true });
    }, 60);
  }
}
function fecharFolhas() {
  document.querySelectorAll('[data-folha]').forEach((f) => { f.dataset.aberta = ''; });
  queueMicrotask(() => document.dispatchEvent(new Event('iald:sheets-closed')));
}

function abrirLateral() { $('#sidebar').dataset.fechada = ''; $('#sb-overlay').dataset.visivel = '1'; }
function fecharLateral() { $('#sidebar').dataset.fechada = '1'; $('#sb-overlay').dataset.visivel = ''; }
function alternarLateral() {
  if ($('#sidebar').dataset.fechada === '1') abrirLateral(); else fecharLateral();
}

// ══════════════════════════════════════════════════════════════
// PERFIL
// ══════════════════════════════════════════════════════════════
function carregarPerfil() {
  const p = recuperar(K.config, null);
  if (p) Object.assign(S.perfil, p);
  $('#cfg-nome').value = S.perfil.name || '';
  $('#cfg-area').value = S.perfil.area || '';
  $('#cfg-interesses').value = S.perfil.interests || '';
  $('#cfg-contexto').value = S.perfil.context || '';
  $('#cfg-estilo').value = S.perfil.style || 'equilibrado';
  pintarUsuario();
}

function salvarPerfil() {
  S.perfil.name = $('#cfg-nome').value.trim();
  S.perfil.area = $('#cfg-area').value.trim();
  S.perfil.interests = $('#cfg-interesses').value.trim();
  S.perfil.context = $('#cfg-contexto').value.trim();
  S.perfil.style = $('#cfg-estilo').value || 'equilibrado';
  guardar(K.config, S.perfil);
  pintarUsuario();
  atualizarDica();
}

function pintarUsuario() {
  const conta = recuperar(K.usuario, '') || '';
  const nome = S.perfil.name || conta || 'Você';
  $('#nome-usuario').textContent = nome;
  const cfg = document.getElementById('cfg-usuario');
  if (cfg) cfg.textContent = conta || (SUPERFICIE === 'app' ? '—' : 'sessão da web');
}

// ══════════════════════════════════════════════════════════════
// LIGACOES
// ══════════════════════════════════════════════════════════════
// Optional activity review uses the current conversation and existing auth client.
// It is never invoked by a model response or the stream DONE marker.
async function abrirAtividadesDaConversa() {
  const conversation = conversaAtiva();
  if (!conversation) return;
  const dialog = document.createElement('dialog');
  dialog.style.cssText = 'max-width:55rem;width:90vw;max-height:85vh;overflow:auto;padding:1.2rem';
  const title = document.createElement('h2'); title.textContent = 'Atividades desta conversa';
  const notice = document.createElement('p'); notice.textContent = 'A conversa continua sem aprovação obrigatória. Revise os resultados e selecione apenas os pedidos atendidos.';
  const status = document.createElement('p'); status.setAttribute('role', 'status');
  const list = document.createElement('div');
  const close = document.createElement('button'); close.textContent = 'Fechar'; close.onclick = () => dialog.close();
  const refresh = document.createElement('button'); refresh.textContent = 'Atualizar';
  const approve = document.createElement('button'); approve.textContent = 'Aceitar selecionadas';
  dialog.append(title, notice, status, list, refresh, approve, close); document.body.append(dialog);
  dialog.addEventListener('close', () => dialog.remove()); dialog.showModal();
  let revision;
  async function load() {
    const response = await fetchIALD('/api/activities?conversation=' + encodeURIComponent(conversation.id));
    const data = await response.json(); if (!response.ok) throw new Error(data.error || 'Atividades indisponíveis.');
    revision = data.revision; list.replaceChildren();
    status.textContent = data.tasks.length + ' atividades · ' + data.handles.length + ' operações pendentes';
    const labels = { working: 'Em execução', review_pending: 'Aguardando sua revisão', satisfied: 'Aceita', blocked: 'Requer conferência' };
    for (const task of data.tasks) {
      const item = document.createElement('section'); item.style.cssText = 'border-top:1px solid #888;padding:.8rem 0';
      const label = document.createElement('label');
      const choice = document.createElement('input'); choice.type = 'checkbox'; choice.value = task.id; choice.disabled = task.status !== 'review_pending';
      label.append(choice, document.createTextNode((labels[task.status] || task.status) + ' · ' + task.criterion));
      const output = document.createElement('pre'); output.style.cssText = 'white-space:pre-wrap;overflow-wrap:anywhere';
      output.textContent = task.output == null ? 'Resultado ainda não integrado.' :
        typeof task.output === 'string' ? task.output : (task.output.content || task.output.answer || JSON.stringify(task.output, null, 2));
      item.append(label, output); list.append(item);
    }
  }
  const failure = error => { status.textContent = error.message || 'Não foi possível conferir o estado.'; };
  refresh.onclick = () => load().catch(failure);
  approve.onclick = async () => {
    try {
      const tasks = [...list.querySelectorAll('input:checked')].map(input => input.value);
      if (!tasks.length) throw new Error('Selecione atividades que você revisou.');
      if (!confirm('Você revisou os resultados e confirma que atendem aos pedidos selecionados?')) return;
      const response = await fetchIALD('/api/activities/review', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ conversation: conversation.id, revision, tasks, confirmed: true }) });
      const result = await response.json(); if (!response.ok) throw new Error(result.error || 'Revisão recusada. Atualize o estado.');
      await load();
    } catch (error) { failure(error); }
  };
  await load().catch(failure);
}

function ligar() {
  const activityButton = document.createElement('button');
  activityButton.type = 'button'; activityButton.className = 'btn-icone';
  activityButton.title = 'Atividades desta conversa'; activityButton.setAttribute('aria-label', 'Atividades desta conversa');
  activityButton.textContent = '✓'; activityButton.addEventListener('click', abrirAtividadesDaConversa);
  $('#btn-config').insertAdjacentElement('beforebegin', activityButton);
  $('#btn-menu').addEventListener('click', alternarLateral);
  $('#sb-overlay').addEventListener('click', fecharLateral);
  $('#btn-fechar-lateral').addEventListener('click', fecharLateral);
  $('#btn-nova').addEventListener('click', novaConversa);
  $('#busca-conv').addEventListener('input', listarConversas);

  $('#btn-config').addEventListener('click', () => { pintarUsuario(); abrirFolha('folha-config'); refreshNativeNotificationsUI(true); });
  const btnApple = $('#btn-apple');
  if (btnApple) btnApple.addEventListener('click', entrarComApple);
  // portão (14/09/2026): Google, usuário e senha, pedido pendente, recusado
  $('#btn-google').addEventListener('click', () => entrarPeloNavegador('google'));
  $('#btn-mostrar-senha').addEventListener('click', () => {
    const f = $('#form-senha');
    f.hidden = !f.hidden;
    if (!f.hidden) $('#campo-usuario').focus();
  });
  $('#form-senha').addEventListener('submit', entrarComSenha);
  $('#btn-verificar').addEventListener('click', () => verificarSituacao(true));
  $('#btn-outra-forma').addEventListener('click', () => {
    esquecer(K.pedido); esquecer(K.pedidoMotivo); erroDoPortao(''); mostrarVista('entrar');
  });
  $('#btn-voltar-entrar').addEventListener('click', () => { erroDoPortao(''); mostrarVista('entrar'); });
  $('#btn-excluir-conta').addEventListener('click', excluirConta);
  $('#btn-consentimento').addEventListener('click', alternarConsentimento);
  $('#cab-estado').addEventListener('click', abrirModelos);
  $('#cab-estado').addEventListener('keydown', (ev) => {
    if ((ev.key === 'Enter' || ev.key === ' ') && $('#cab-estado').dataset.trocavel === '1') {
      ev.preventDefault();
      abrirModelos();
    }
  });
  $('#btn-consentir').addEventListener('click', consentirEContinuar);
  $('#btn-recusar-consentimento').addEventListener('click', () => { mediaPendingConsent = null; S.avisoConsentimento = null; fecharFolhas(); });

  // atalhos do rodapé da lateral (a folha de créditos abre com o uso do plano no topo)
  document.querySelectorAll('[data-abrir="creditos"]').forEach((b) => b.addEventListener('click', () => {
    abrirCreditos(null);
  }));
  ligarDenuncia();
  document.querySelectorAll('[data-abrir="ferramentas"]').forEach((b) => b.addEventListener('click', () => {
    if (window.innerWidth < 861) fecharLateral();
    listarFerramentas(); abrirFolha('folha-ferramentas');
  }));
  // 22/09/2026: a folha abre limpa (sem o link da exportação anterior) — salvo com uma em curso,
  // que segue mostrando "Gerando…" e os botões travados até o servidor responder
  $('#btn-exportar').addEventListener('click', () => {
    if (!exportando) limparExportacao();
    abrirFolha('folha-exportar');
  });

  $('#btn-busca').addEventListener('click', () => {
    if (!ferramentaPermitida('search_web')) { pintarBusca(); return; }
    S.busca = !S.busca;
    pintarBusca();
    $('#entrada').focus();
  });

  // o tema "Sistema" acompanha a troca claro/escuro do aparelho em tempo real
  try {
    window.matchMedia('(prefers-color-scheme: dark)')
      .addEventListener('change', () => sincronizarBarraDeStatus());
  } catch (e) { /* navegador antigo */ }

  document.querySelectorAll('[data-fechar]').forEach((b) => b.addEventListener('click', fecharFolhas));
  document.querySelectorAll('[data-folha]').forEach((f) => {
    f.addEventListener('click', (ev) => { if (ev.target === f) fecharFolhas(); });
  });
  document.addEventListener('keydown', (ev) => {
    if (ev.key === 'Escape') { fecharFolhas(); if (window.innerWidth < 861) fecharLateral(); }
  });

  document.querySelectorAll('#opcoes-tema button').forEach((b) => {
    b.addEventListener('click', () => aplicarTema(b.dataset.tema || ''));
  });

  ['#cfg-nome', '#cfg-area', '#cfg-interesses', '#cfg-contexto', '#cfg-estilo']
    .forEach((s) => $(s).addEventListener('input', salvarPerfil));

  $('#btn-sair').addEventListener('click', async () => {
    if (SUPERFICIE === 'app' && !await prepareNativePushLogout()) return;
    desanexarRespostasBackground(true);
    desfazerPendente = null;
    esconderFaixaFlutuante();
    if (SUPERFICIE !== 'app') { location.href = '/logout'; return; }
    if (S.aborto) S.aborto.abort();
    if (PODE_OUVIR) window.speechSynthesis.cancel();
    limparTokenApp();
    try { localStorage.removeItem(K.usuario); } catch (e) { /* modo privado */ }
    fecharFolhas();
    avaliarPortao();
  });

  // compositor
  const entrada = $('#entrada');
  entrada.addEventListener('input', () => { redimensionarEntrada(); atualizarBotaoEnviar(); });
  entrada.addEventListener('keydown', (ev) => {
    if (ev.key === 'Enter' && !ev.shiftKey && !ev.isComposing) { ev.preventDefault(); enviar(); }
  });
  $('#btn-enviar').addEventListener('click', () => { if (S.gerando) parar(); else enviar(); });

  $('#btn-anexar').addEventListener('click', () => {
    if (!imagensPermitidas()) { S.dicaImagem = true; desenharAnexos(); }
    $('#arquivo').click();
  });
  // a faixa do Desfazer volta a contar quando o ponteiro ou o foco saem dela
  const faixaFlutuante = document.getElementById('faixa-flutuante');
  if (faixaFlutuante) {
    ['mouseleave', 'focusout'].forEach((e) => faixaFlutuante.addEventListener(e, () => {
      if (faixaFlutuante.dataset.visivel === '1') armarRelogioDaFaixa();
    }));
  }
  $('#arquivo').addEventListener('change', (ev) => { receberArquivos(ev.target.files); ev.target.value = ''; });

  $('#btn-pensar').addEventListener('click', () => {
    if (!pensarPermitido()) return;                      // o plano não tem modo pensar
    S.modo = S.modo === 'fast' ? 'think' : 'fast';
    guardar(K.modo, S.modo);
    pintarModo();
    atualizarDica();
  });

  // arrastar e soltar + colar imagem
  const caixa = $('#caixa');
  ['dragenter', 'dragover'].forEach((e) => caixa.addEventListener(e, (ev) => {
    ev.preventDefault(); caixa.dataset.arrastando = '1';
  }));
  ['dragleave', 'drop'].forEach((e) => caixa.addEventListener(e, (ev) => {
    ev.preventDefault(); caixa.dataset.arrastando = '';
  }));
  caixa.addEventListener('drop', (ev) => {
    if (ev.dataTransfer && ev.dataTransfer.files.length) receberArquivos(ev.dataTransfer.files);
  });
  entrada.addEventListener('paste', (ev) => {
    const itens = ev.clipboardData && ev.clipboardData.files;
    if (itens && itens.length) { ev.preventDefault(); receberArquivos(itens); }
  });

  // rolagem
  const conversa = $('#conversa');
  conversa.addEventListener('scroll', () => {
    if (document.querySelector('.msg-edicao-texto')) { S.colarNoFim = false; return; }
    const perto = pertoDoFim();
    if (!perto) S.colarNoFim = false;
    if (perto) S.colarNoFim = true;
    $('#ir-fim').dataset.visivel = perto ? '' : '1';
  }, { passive: true });
  $('#ir-fim').addEventListener('click', () => {
    S.colarNoFim = true;
    conversa.scrollTo({ top: conversa.scrollHeight, behavior: 'smooth' });
  });

  // exportacao
  // 21/09/2026: no aparelho com os plugins, grava + folha do sistema e impressão nativa (ver nativoCom)
  // 22/09/2026: SAIU o caminho de 21/09 (as folhas nativas não respondiam ao toque no iPhone). Os três
  // formatos saem do SERVIDOR, com o Selo IALD; a folha mostra o link "Abrir arquivo" (ver
  // exportarPeloServidor). Blob e impressão do navegador ficaram só como reserva da web, sem selo.
  $('#exp-txt').addEventListener('click', () => exportarPeloServidor('txt'));
  $('#exp-md').addEventListener('click', () => exportarPeloServidor('md'));
  $('#exp-print').addEventListener('click', () => exportarPeloServidor('pdf'));
  $('#exp-limpar').addEventListener('click', async () => {
    const c = conversaAtiva();
    if (c && !await apagarJobsDaConversa(c.id)) return;
    if (c) { delete c.chat_job_deliveries; c.mensagens = []; c.titulo = 'Nova conversa'; salvarConversas(); listarConversas(); abrirConversa(); }
    fecharFolhas();
  });

  // a janela mudou de tamanho (teclado do celular): manter o fim a vista
  window.addEventListener('resize', () => { if (!ajustarEdicaoMensagem() && S.colarNoFim) rolarSePerto(); });
}

function pintarModo() {
  const b = $('#btn-pensar');
  const permitido = pensarPermitido();
  const pensando = modoEfetivo() === 'think';
  b.disabled = !permitido;
  b.dataset.indisponivel = permitido ? '' : '1';
  const dicaLinha = b.closest('.dica');
  if (dicaLinha) dicaLinha.dataset.limitada = permitido ? '' : '1';
  b.setAttribute('aria-pressed', String(pensando));
  // raio desenhado em SVG: o caractere ⚡ vira emoji colorido, diferente em cada aparelho
  const icone = b.querySelector('.pm-icone');
  if (!permitido) {
    // Plano sem modo pensar (limites.pensar = false): a pílula não acende nem troca de
    // modo, e diz por quê. O servidor já trocava o pensar pelo rápido sem avisar.
    const motivo = 'modo pensar ' + rotuloIndisponivel();
    icone.textContent = '√';
    b.title = motivo[0].toUpperCase() + motivo.slice(1) + '.';
    b.setAttribute('aria-label', b.title);
    b.querySelector('.pm-texto').textContent = motivo;
    return;
  }
  b.removeAttribute('aria-label');
  b.title = pensando ? 'Modo pensar — raciocínio visível. Tocar para voltar ao rápido.'
    : 'Modo rápido. Tocar para o modo pensar (raciocínio visível).';
  if (pensando) icone.textContent = '√';
  else icone.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13 2L3 14h8l-1 8 11-13h-8l1-7z"/></svg>';
  b.querySelector('.pm-texto').textContent = pensando ? 'modo pensar' : 'modo rápido';
}

function pintarBusca() {
  const b = $('#btn-busca');
  // Sem search_web no plano (limites.ferramentas), a lupa fica desabilitada: antes ela
  // acendia, a instrução ia ao modelo e a busca não acontecia.
  const permitida = ferramentaPermitida('search_web');
  if (!permitida) S.busca = false;
  b.disabled = !permitida;
  b.setAttribute('aria-pressed', String(S.busca));
  b.title = !permitida ? 'Busca na internet ' + rotuloIndisponivel()
    : S.busca ? 'Busca na internet LIGADA para a próxima mensagem' : 'Buscar na internet nesta mensagem';
  b.setAttribute('aria-label', b.title);
  const dica = document.getElementById('dica-texto');
  if (dica) {
    dica.textContent = S.busca ? 'a próxima mensagem busca na internet'
      : permitida ? 'PDF · busca · envia' : 'PDF · envia';
  }
}

// ══════════════════════════════════════════════════════════════
// TECLADO DO IPHONE
// No WKWebView o teclado não encolhe a janela: encolhe só a área VISÍVEL
// (visualViewport). Sem acompanhar isso o compositor fica atrás do teclado e o
// cabeçalho é empurrado para fora da tela. No Android o Capacitor já redimensiona
// a WebView (SystemBars aplica o recuo do teclado) e as duas medidas coincidem.
// ══════════════════════════════════════════════════════════════
function acompanharTeclado() {
  const vv = window.visualViewport;
  if (!vv) return;
  const raiz = document.documentElement;
  let alturaAnterior = vv.height;
  const ajustar = (inicial) => {
    raiz.style.setProperty('--altura-util', vv.height + 'px');
    raiz.style.setProperty('--topo-util', vv.offsetTop + 'px');
    const aberto = (window.innerHeight - vv.height) > 120;
    raiz.dataset.teclado = aberto ? '1' : '';
    // Só puxa para o fim quando a área ENCOLHEU (teclado abrindo) e há conversa.
    // Rolar sempre fazia a tela de boas-vindas abrir já rolada, com a ponta da
    // cruz do logo cortada sob o cabeçalho (visto na renderização de 13/09).
    const encolheu = vv.height < alturaAnterior - 1;
    alturaAnterior = vv.height;
    if (ajustarEdicaoMensagem()) return;
    const c = conversaAtiva();
    if (inicial !== true && encolheu && S.colarNoFim && c && c.mensagens.length) rolarSePerto();
  };
  vv.addEventListener('resize', () => ajustar(false));
  vv.addEventListener('scroll', () => ajustar(false));
  ajustar(true);
}

// ══════════════════════════════════════════════════════════════
// PORTÃO DE ENTRADA — o MESMO modelo do site (14/09/2026)
//
// ORDEM DO OPERADOR: site e app com a mesma entrada; a Apple vale no iPhone, no
// iPad e em qualquer aparelho; o mesmo com o Google; sem conflito de usuário; e
// todo acesso depende da liberação dele no painel.
//
// EMENDA 14/09/2026 (noite), ordem nova do operador, que SUBSTITUI a de cima: conta
// nova com a Apple ou o Google entra sozinha, no uso gratuito, no motor da OpenAI. O
// operador continua podendo bloquear e excluir; senha continua criada só por ele. O
// servidor decide (IALD_ENTRADA_ABERTA); o app só lê: `entrada_aberta` e `nota` em
// /api/entrar/config, e `motivo` ("bloqueado" | "recusado") na recusa.
//
// AS TRÊS PORTAS DO APP:
//   Apple  → iPhone/iPad: folha nativa (identityToken → /api/entrar/apple)
//            Android:     navegador do sistema (fluxo web da Apple)
//   Google → navegador do sistema em todas as plataformas (o Google proíbe a
//            entrada dentro de WebView; o navegador do sistema é o permitido)
//   Usuário e senha → contas que o operador cria (/api/entrar/senha)
// Toda resposta tem o mesmo formato: active (entra) · pending (pedido enviado,
// aguarda o operador) · rejected (não liberado) · expired (pedido não existe mais).
//
// A VOLTA DO NAVEGADOR: o servidor devolve br.ia.iald://entrar?bilhete=... . O
// bilhete sozinho não abre sessão — o app manda antes o SHA-256 de um segredo
// (desafio) e depois apresenta o segredo (verificador), a ideia do PKCE: outro
// app que capture o link não tem o verificador.
//
// ⚠ O `user` que o plugin da Apple devolve continua IGNORADO: quem diz quem é a
// pessoa é o `sub` do token, conferido no servidor contra as chaves da Apple.
// ══════════════════════════════════════════════════════════════
const PLATAFORMA = (() => {
  try {
    if (window.Capacitor && typeof window.Capacitor.getPlatform === 'function') {
      return window.Capacitor.getPlatform();
    }
  } catch (e) { /* fora do invólucro */ }
  return 'web';
})();

// clientId e redirectURI só valem para o fluxo WEB da Apple; na implementação
// nativa do iOS quem identifica o app é o próprio bundle identifier. Ficam aqui
// porque a interface do plugin os exige.
const APPLE_CLIENT_ID = 'br.ia.IALD';
const APPLE_REDIRECT = 'https://iald.ia.br/apple-callback';

let CONFIG_ENTRADA = null;
let vigiaPedido = null;
let retornoEmCurso = false;

// Plugin nativo pelo registro em tempo de execução (este arquivo é módulo ES puro,
// sem empacotador: especificador nu não resolve).
function plugin(nome) {
  try {
    const cap = window.Capacitor;
    if (!cap) return null;
    return (cap.Plugins && cap.Plugins[nome]) || (cap.registerPlugin ? cap.registerPlugin(nome) : null);
  } catch (e) { return null; }
}

function esquecer(chave) {
  try { localStorage.removeItem(chave); } catch (e) { /* modo privado */ }
}

function portaoNecessario() {
  return SUPERFICIE === 'app' && !tokenApp();
}

function erroDoPortao(msg) {
  const e = $('#portao-erro');
  if (!e) return;
  if (!msg) { e.hidden = true; e.textContent = ''; return; }
  e.hidden = false;
  e.textContent = msg;
}

function ocupadoNoPortao(sim, texto) {
  document.querySelectorAll('#portao button').forEach((b) => { b.disabled = !!sim; });
  const c = $('#portao-carregando');
  if (c) c.hidden = !sim;
  const t = $('#portao-carregando-texto');
  if (t) t.textContent = texto || 'entrando…';
}

function mostrarVista(nome) {
  for (const v of ['entrar', 'pendente', 'recusado']) {
    const n = $('#vista-' + v);
    if (n) n.hidden = (v !== nome);
  }
  pintarVistaPendente();
}

// Pedido que nasceu do LIMITE de contas novas (porta aberta) — não é espera do operador.
// Revisão de interface M1 e ordem-régua 13 (14/09/2026, noite): a tela dizia "tente mais
// tarde", mas a checagem de 30 s (e o "Verificar agora") perguntava /situacao; o servidor
// com a porta aberta respondia 410 "A entrada agora é direta", a pessoa entrava de novo,
// batia no limite e voltava ao pendente — um laço, justo no pico. Nesse caso: sem checagem
// periódica, sem "Verificar agora", texto de tentar mais tarde. A consulta única ao abrir o
// app e ao voltar do fundo continua (o operador ainda pode liberar o pedido no painel).
const TEXTO_PENDENTE_LIMITE = 'A IALD recebeu muitas contas novas agora e ainda não pôde criar a sua. '
  + 'Tente entrar de novo mais tarde.';
const TEXTO_PENDENTE_OPERADOR = 'A IALD é experimental e cada acesso é liberado pessoalmente pelo operador. '
  + 'Assim que ele liberar, o app entra sozinho.';

function pendentePorLimite() {
  return recuperar(K.pedidoMotivo, '') === 'limite' || entradaAberta();
}

function pintarVistaPendente() {
  const vista = $('#vista-pendente');
  const visivel = !!(vista && !vista.hidden);
  const porLimite = pendentePorLimite();
  if (vista) vista.dataset.motivo = porLimite ? 'limite' : 'operador';
  const verificar = $('#btn-verificar');
  if (verificar) verificar.hidden = porLimite;
  const outra = $('#btn-outra-forma');
  if (outra) outra.textContent = porLimite ? 'Voltar à entrada' : 'Entrar de outra forma';
  const titulo = $('#titulo-pendente');
  if (titulo) titulo.textContent = porLimite ? 'Tente mais tarde' : 'Pedido enviado';
  if (vigiaPedido) { clearInterval(vigiaPedido); vigiaPedido = null; }
  // Enquanto o pedido espera o OPERADOR, o app pergunta a cada 30 s e ao voltar do fundo:
  // quando ele libera, a pessoa entra sem tocar em nada.
  if (visivel && !porLimite) vigiaPedido = setInterval(() => verificarSituacao(false), 30000);
}

async function carregarConfigEntrada() {
  try {
    const r = await fetchIALD('/api/entrar/config', { signal: AbortSignal.timeout(6000) });
    if (r.ok) CONFIG_ENTRADA = await r.json();
  } catch (e) { /* sem rede: ficam as portas que não dependem de configuração */ }
  pintarBotoesEntrada();
  // a porta pode ter chegado aberta depois de a vista pendente ligar a checagem
  pintarVistaPendente();
}

function pintarBotoesEntrada() {
  const cfg = CONFIG_ENTRADA || {};
  const apple = $('#btn-apple'), google = $('#btn-google'), ou = $('#portao-ou');
  // iPhone/iPad: a folha nativa da Apple aparece mesmo antes de ler a configuração.
  const mostraApple = (PLATAFORMA === 'ios') ? (cfg.apple_nativo !== false) : !!cfg.apple_web;
  const mostraGoogle = !!cfg.google;
  if (apple) apple.hidden = !mostraApple;
  if (google) google.hidden = !mostraGoogle;
  if (ou) ou.hidden = !(mostraApple || mostraGoogle);
  pintarNotaEntrada();
}

// 14/09/2026 (noite): a nota do portão acompanha a porta. Com a entrada aberta, a conta
// nova entra direto no uso gratuito; fechada, o acesso depende do operador. O texto vem
// do servidor (campo "nota"); sem ele, sai do estado `entrada_aberta`; sem configuração
// nenhuma (sem rede), fica só a frase que vale nos dois casos.
const NOTA_ABERTA = 'A IALD é experimental. Ao entrar com a Apple ou o Google, a conta começa no uso gratuito, com um limite baixo de uso por dia.';
const NOTA_FECHADA = 'A IALD é experimental. Todo acesso é liberado pessoalmente pelo operador.';

function entradaAberta() {
  return !!(CONFIG_ENTRADA && CONFIG_ENTRADA.entrada_aberta === true);
}

function pintarNotaEntrada() {
  const alvo = document.getElementById('portao-nota-estado');
  if (!alvo) return;
  const cfg = CONFIG_ENTRADA;
  if (!cfg) { alvo.textContent = 'A IALD é experimental.'; return; }
  const nota = (typeof cfg.nota === 'string') ? cfg.nota.trim() : '';
  alvo.textContent = nota || (entradaAberta() ? NOTA_ABERTA : NOTA_FECHADA);
}

// Resposta única de toda porta de entrada.
async function tratarRespostaEntrada(resp) {
  const j = await resp.json().catch(() => ({}));
  if (resp.ok && j.status === 'active' && j.token) {
    guardarTokenApp(j.token);
    if (j.username) guardar(K.usuario, String(j.username));
    esquecer(K.pedido);
    esquecer(K.pedidoMotivo);
    erroDoPortao('');
    fecharPortao();
    return 'active';
  }
  if (j.status === 'pending') {
    if (j.pedido) guardar(K.pedido, j.pedido);
    // porta aberta: pendente só nasce do limite de contas novas (não é espera do operador).
    // O servidor desta rodada diz isso em `motivo: "limite"`; o anterior, só pela porta aberta.
    const porLimite = j.motivo === 'limite' || entradaAberta();
    if (porLimite) guardar(K.pedidoMotivo, 'limite'); else esquecer(K.pedidoMotivo);
    erroDoPortao('');
    const t = $('#texto-pendente');
    if (t) t.textContent = j.mensagem || (porLimite ? TEXTO_PENDENTE_LIMITE : TEXTO_PENDENTE_OPERADOR);
    mostrarVista('pendente');
    verificarIdentificacaoCadastro(j.pedido || recuperar(K.pedido, ''));
    return 'pending';
  }
  if (j.status === 'rejected') {
    sheetAfterRegistration = '';
    registrationIdentity?.reset();
    esquecer(K.pedido);
    esquecer(K.pedidoMotivo);
    erroDoPortao('');
    // O texto é o do servidor. "bloqueado" = a conta existe e o operador a bloqueou;
    // "recusado" = a identidade foi barrada (com a porta aberta, também é bloqueio).
    const bloqueada = j.motivo === 'bloqueado';
    const titulo = $('#titulo-recusado');
    if (titulo) {
      titulo.textContent = bloqueada ? 'Conta bloqueada'
        : (entradaAberta() ? 'Acesso bloqueado' : 'Acesso não liberado');
    }
    const t = $('#texto-recusado');
    if (t) t.textContent = j.error || j.detalhe || 'O operador não liberou este acesso.';
    const v = $('#vista-recusado');
    if (v) v.dataset.motivo = bloqueada ? 'bloqueado' : 'recusado';
    mostrarVista('recusado');
    return 'rejected';
  }
  if (j.status === 'expired') {
    sheetAfterRegistration = '';
    registrationIdentity?.reset();
    esquecer(K.pedido);
    esquecer(K.pedidoMotivo);
    mostrarVista('entrar');
    erroDoPortao(j.error || 'Entre de novo para pedir acesso.');
    return 'expired';
  }
  throw new Error(j.error || j.detalhe || `O servidor recusou a entrada (HTTP ${resp.status}).`);
}

function postarJSON(caminho, corpo) {
  return fetchIALD(caminho, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(corpo),
  });
}

async function entrarComApple() {
  if (PLATAFORMA !== 'ios') return entrarPeloNavegador('apple');
  erroDoPortao('');
  ocupadoNoPortao(true);
  try {
    const plug = plugin('SignInWithApple');
    if (!plug) throw new Error('O componente de entrada da Apple não está disponível neste aparelho.');
    const r = await plug.authorize({ clientId: APPLE_CLIENT_ID, redirectURI: APPLE_REDIRECT, scopes: 'email name' });
    const d = (r && r.response) || {};
    if (!d.identityToken) throw new Error('A Apple não devolveu o token de identidade.');
    // Nome só vem na PRIMEIRA autenticação; nas seguintes chega nulo.
    const nome = [d.givenName, d.familyName].filter(Boolean).join(' ');
    const resp = await postarJSON('/api/entrar/apple', { identity_token: d.identityToken, name: nome || undefined });
    await tratarRespostaEntrada(resp);
  } catch (e) {
    // Cancelar no diálogo da Apple não é erro: não se acusa quem desistiu.
    const txt = String((e && e.message) || e || '');
    if (/cancel/i.test(txt) || /1001/.test(txt)) erroDoPortao('');
    else erroDoPortao(txt || 'Não foi possível entrar.');
  } finally {
    ocupadoNoPortao(false);
  }
}

// ── o segredo do retorno (verificador) e o seu SHA-256 (desafio) ──
function base64url(bytes) {
  let s = '';
  bytes.forEach((b) => { s += String.fromCharCode(b); });
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

// SHA-256 em JavaScript puro: reserva para WebView sem crypto.subtle (conferido
// contra o SHA-256 do Node em 14/09/2026, ver o teste do portão).
function sha256Js(bytes) {
  const K256 = new Uint32Array([
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]);
  const H = new Uint32Array([0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]);
  const len = bytes.length;
  const total = ((len + 9 + 63) >> 6) << 6;
  const m = new Uint8Array(total);
  m.set(bytes);
  m[len] = 0x80;
  const dv = new DataView(m.buffer);
  dv.setUint32(total - 8, Math.floor(len / 0x20000000));
  dv.setUint32(total - 4, (len << 3) >>> 0);
  const W = new Uint32Array(64);
  for (let o = 0; o < total; o += 64) {
    for (let i = 0; i < 16; i++) W[i] = dv.getUint32(o + i * 4);
    for (let i = 16; i < 64; i++) {
      const x = W[i - 15], y = W[i - 2];
      const s0 = ((x >>> 7) | (x << 25)) ^ ((x >>> 18) | (x << 14)) ^ (x >>> 3);
      const s1 = ((y >>> 17) | (y << 15)) ^ ((y >>> 19) | (y << 13)) ^ (y >>> 10);
      W[i] = (W[i - 16] + s0 + W[i - 7] + s1) | 0;
    }
    let a = H[0], b = H[1], c = H[2], d = H[3], e = H[4], f = H[5], g = H[6], h = H[7];
    for (let i = 0; i < 64; i++) {
      const t1 = (h + (((e >>> 6) | (e << 26)) ^ ((e >>> 11) | (e << 21)) ^ ((e >>> 25) | (e << 7)))
        + ((e & f) ^ (~e & g)) + K256[i] + W[i]) | 0;
      const t2 = ((((a >>> 2) | (a << 30)) ^ ((a >>> 13) | (a << 19)) ^ ((a >>> 22) | (a << 10)))
        + ((a & b) ^ (a & c) ^ (b & c))) | 0;
      h = g; g = f; f = e; e = (d + t1) | 0; d = c; c = b; b = a; a = (t1 + t2) | 0;
    }
    H[0] += a; H[1] += b; H[2] += c; H[3] += d; H[4] += e; H[5] += f; H[6] += g; H[7] += h;
  }
  const out = new Uint8Array(32);
  const dvo = new DataView(out.buffer);
  for (let i = 0; i < 8; i++) dvo.setUint32(i * 4, H[i]);
  return out;
}

async function sha256(texto) {
  const dados = new TextEncoder().encode(texto);
  try {
    if (window.crypto && crypto.subtle && typeof crypto.subtle.digest === 'function') {
      return new Uint8Array(await crypto.subtle.digest('SHA-256', dados));
    }
  } catch (e) { /* contexto sem subtle: segue para a versão em JS */ }
  return sha256Js(dados);
}

async function entrarPeloNavegador(provedor) {
  erroDoPortao('');
  try {
    const verificador = base64url(crypto.getRandomValues(new Uint8Array(32)));
    guardar(K.verificador, verificador);
    const desafio = base64url(await sha256(verificador));
    const url = `${HOST_REMOTO}/auth/${provedor}/iniciar?origem=app&desafio=${encodeURIComponent(desafio)}`;
    const Browser = plugin('Browser');
    if (Browser && typeof Browser.open === 'function') await Browser.open({ url });
    else window.open(url, '_blank');
    // O resto acontece em tratarLinkDeRetorno, quando o navegador devolver o app.
  } catch (e) {
    erroDoPortao('Não foi possível abrir a entrada: ' + String((e && e.message) || e));
  }
}

async function tratarLinkDeRetorno(url) {
  if (!url || !/^br\.ia\.iald:\/\/entrar/i.test(String(url))) return;
  const Browser = plugin('Browser');
  if (Browser && typeof Browser.close === 'function') {
    try { await Browser.close(); } catch (e) { /* no Android o navegador já fechou sozinho */ }
  }
  const m = /[?&]bilhete=([A-Za-z0-9_-]+)/.exec(String(url));
  if (!m || retornoEmCurso) return;
  retornoEmCurso = true;
  ocupadoNoPortao(true, 'concluindo a entrada…');
  try {
    const resp = await postarJSON('/api/entrar/bilhete', {
      bilhete: m[1], verificador: recuperar(K.verificador, '') || '',
    });
    esquecer(K.verificador);
    await tratarRespostaEntrada(resp);
  } catch (e) {
    mostrarVista('entrar');
    erroDoPortao(String((e && e.message) || e));
  } finally {
    ocupadoNoPortao(false);
    retornoEmCurso = false;
  }
}

function ouvirRetornoDoNavegador() {
  if (SUPERFICIE !== 'app') return;
  const App = plugin('App');
  if (!App || typeof App.addListener !== 'function') return;
  try {
    App.addListener('appUrlOpen', (ev) => { tratarLinkDeRetorno(ev && ev.url); });
    App.addListener('resume', () => {
      const p = $('#portao'), v = $('#vista-pendente');
      if (p && !p.hidden && v && !v.hidden) verificarSituacao(false);
    });
    if (typeof App.getLaunchUrl === 'function') {
      App.getLaunchUrl().then((r) => { if (r && r.url) tratarLinkDeRetorno(r.url); }).catch(() => {});
    }
  } catch (e) { /* sem o plugin o app ainda entra pela Apple nativa e por senha */ }
}

async function entrarComSenha(ev) {
  if (ev) ev.preventDefault();
  erroDoPortao('');
  const usuario = ($('#campo-usuario').value || '').trim().toLowerCase();
  const senha = $('#campo-senha').value || '';
  if (!usuario || !senha) { erroDoPortao('Informe usuário e senha.'); return; }
  ocupadoNoPortao(true);
  try {
    const resp = await postarJSON('/api/entrar/senha', { usuario, senha });
    const r = await tratarRespostaEntrada(resp);
    if (r === 'active') $('#campo-senha').value = '';
  } catch (e) {
    erroDoPortao(String((e && e.message) || e));
  } finally {
    ocupadoNoPortao(false);
  }
}

async function verificarSituacao(manual) {
  const pedido = recuperar(K.pedido, '') || '';
  if (!pedido) { mostrarVista('entrar'); return; }
  if (manual) ocupadoNoPortao(true, 'verificando…');
  try {
    const resp = await postarJSON('/api/entrar/situacao', { pedido });
    const r = await tratarRespostaEntrada(resp);
    if (r === 'pending' && manual) {
      const t = $('#texto-pendente');
      const hora = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
      if (t) {
        t.textContent = pendentePorLimite()
          ? `A conta ainda não pôde ser criada (verificado às ${hora}). Tente entrar de novo mais tarde.`
          : `Ainda aguardando a liberação do operador (verificado às ${hora}). `
            + 'Assim que ele liberar, o app entra sozinho.';
      }
    }
  } catch (e) {
    if (manual) erroDoPortao(String((e && e.message) || e));
  } finally {
    if (manual) ocupadoNoPortao(false);
  }
}

async function excluirConta() {
  const conta = recuperar(K.usuario, '') || 'esta conta';
  if (!confirm(`Excluir ${conta}?\n\nO seu usuário na IALD e as conversas guardadas neste aparelho serão apagados. `
    + 'Você pode entrar de novo; o uso gratuito já consumido não volta.')) return;
  let resp, j = {};
  try {
    resp = await postarJSON('/api/conta/excluir', { confirmar: 'EXCLUIR' });
    j = await resp.json().catch(() => ({}));
  } catch (e) {
    alert('Sem conexão com o servidor: a conta NÃO foi excluída.');
    return;
  }
  if (!resp.ok) { alert(j.error || `Não foi possível excluir (HTTP ${resp.status}).`); return; }
  try {
    for (const c of S.conversas) if (backgroundOwner && c.background_owner === backgroundOwner) await mediaClearConversationLocal(backgroundOwner, c.id);
  } catch (error) { alert('Conta excluída no servidor; falha visível na limpeza da mídia local: ' + error.message); }
  if (backgroundOwner) {
    backgroundEpoch += 1; backgroundJobs.pause();
    await backgroundHistoryWrites.catch(() => {});
    try { await chatLocalStore.purge(backgroundOwner); }
    catch (error) { alert('Conta excluída no servidor; limpeza do histórico local ainda pendente: ' + error.message); }
    localStorage.removeItem(backgroundHistoryKey(backgroundOwner));
    backgroundJobs.forgetOwner();
  }
  desanexarRespostasBackground(true);
  desfazerPendente = null;                               // conta excluída: nada de conversa para desfazer
  esconderFaixaFlutuante();
  for (const k of [K.conversas, K.ativa, K.config, K.usuario, K.pedido, K.pedidoMotivo, K.verificador]) esquecer(k);
  Object.assign(S.perfil, { name: '', area: '', interests: '', context: '', style: 'equilibrado' });
  if (SUPERFICIE !== 'app') { location.href = '/login'; return; }
  if (S.aborto) S.aborto.abort();
  limparTokenApp();
  S.conversas = [];
  S.ativaId = null;
  carregarPerfil();
  carregarConversas();
  fecharFolhas();
  avaliarPortao();
}

// ══════════════════════════════════════════════════════════════
// MOTOR DA CONTA E CONSENTIMENTO DE IA DE TERCEIROS (14/09/2026)
// Contas liberadas pelo operador podem responder pela API da OpenAI. A Apple
// (5.1.2(i)) exige dizer o que vai a terceiros e pedir permissão ANTES: o servidor
// não envia nada à OpenAI sem o "Concordo", e o texto lido aqui vem dele.
// ══════════════════════════════════════════════════════════════
// 21/09/2026: o terceiro motor — o Claude (Anthropic), ao lado da nativa e do ChatGPT. Decisão
// do operador: "Achei o Sonnet muito caro, mas é o melhor [...] eu vou instalar somente pra mim,
// para eu testar"; quem usa: "por enquanto só eu" (quem libera é o servidor, não o app). O app
// não guarda nome de provedor: externo é todo motor que não é a nativa, e o rótulo, o provedor
// e o texto do consentimento vêm de GET /api/motor. Sem `rotulo`, "provedor · modelo" — o mesmo
// "OpenAI · modelo" de antes para um servidor que ainda não manda o rótulo.
function motorExterno(m) {
  return !!m && !!m.motor && m.motor !== 'nativa';
}

function provedorDoMotor(m) {
  return String((m && m.provedor) || 'IA de terceiros');
}

// ⚠ CORREÇÃO AO LADO (21/09/2026, revisão de regressão): a linha "Motor" das configurações passava
// a mostrar o rótulo do servidor ("ChatGPT 5.6 Luna") e o nome do terceiro sumia de perto do botão
// de consentimento. Volta a ser "provedor · modelo" — byte a byte o "OpenAI · modelo" de antes, e
// "Anthropic · claude-sonnet-5" no Claude; sem modelo, o rótulo do servidor.
function rotuloDoMotor(m) {
  if (!motorExterno(m)) return 'IALD Nativa';
  if (m.provedor && m.modelo) return `${m.provedor} · ${m.modelo}`;
  return String(m.rotulo || m.provedor || m.motor);
}

// 21/09/2026 (revisão de segurança): a folha de consentimento guarda DE QUEM é o texto que mostra
// (provedor e versão, vindos do MESMO objeto que o texto) e o aceite devolve isso ao servidor, que
// recusa (409) se o motor da conta mudou. Nunca se consente a um provedor que a folha não nomeou.
function consentimentoDe(m) {
  const c = (m && m.consentimento) || {};
  return { texto: c.texto, provedor: c.provedor || (m && m.provedor) || null, versao: c.versao };
}

function folhaDoAviso(aviso) {
  if (aviso && aviso.detalhe) return { texto: aviso.detalhe, provedor: aviso.provedor || null, versao: aviso.versao };
  const c = consentimentoDe(S.motor);
  return { texto: c.texto || (aviso && aviso.texto), provedor: c.provedor, versao: c.versao };
}

// `aoEntrar` (14/09/2026, noite): logo depois da entrada, conta no motor da OpenAI sem
// consentimento vê a folha de consentimento na hora — e não só quando a primeira
// mensagem voltar recusada. Uma vez por entrada: "Agora não" é respeitado até a próxima.
function carregarMotor(opcoes) {
  if (DEMO) return Promise.resolve();
  const leitura = lerMotor(opcoes);
  S.motorCarregando = leitura;
  return leitura;
}

async function lerMotor(opcoes) {
  const ticket = ++motorRequest;
  const mediaOwner = backgroundOwner, mediaEpoch = backgroundEpoch;
  try {
    const r = await fetchIALD('/api/motor', { signal: AbortSignal.timeout(6000) });
    if (ticket !== motorRequest || (!r.ok && r.status !== 503)) return;
    const next = await r.json();
    if (ticket !== motorRequest) return;
    const previous = S.motor && (S.motor.motor_selecao || S.motor.modelo || S.motor.motor);
    if (mediaOwner !== backgroundOwner || mediaEpoch !== backgroundEpoch) return;
    const previousMediaScope = mediaStorageScope();
    if (previousMediaScope && previousMediaScope !== (next.limites?.media_capabilities?.media_scope || null)) mediaDetach();
    S.motor = next; mediaCapsAccount = mediaOwner;
    const current = S.motor.motor_selecao || S.motor.modelo || S.motor.motor;
    if (previous !== current) {
      S.ctx = { n_ctx: 32768, margem: 0.92, reserva_resposta: 8192,
        cpt: 2.91, teto_mensagens: 400, carregado: false };
      await carregarContexto();
    }
  } catch (e) { return; }
  if (ticket !== motorRequest) return;
  pintarMotor();
  // os limites do plano podem ter mudado (o operador troca o plano no painel)
  pintarModo();
  pintarBusca();
  atualizarDica();
  if (folhaAberta('folha-ferramentas')) listarFerramentas();
  if (folhaAberta('folha-creditos')) { pintarUsoPlano(); pintarCreditos(); }
  pintarAnexar();
  if (opcoes && opcoes.aoEntrar) oferecerConsentimento();
}

function oferecerConsentimento() {
  const m = S.motor;
  if (!motorExterno(m) || S.consentimentoOferecido) return;
  const c = m.consentimento || {};
  if (c.necessario === false || c.dado) return;
  const portao = document.getElementById('portao');
  if (portao && !portao.hidden) return;                  // ainda não entrou
  if (document.querySelector('[data-folha][data-aberta="1"], .registration-overlay')) return;  // uma apresentação por vez
  S.consentimentoOferecido = true;
  S.avisoConsentimento = null;                           // nada a reenviar: nenhuma pergunta foi feita
  const f = consentimentoDe(m);
  abrirConsentimento(f.texto, f.provedor, f.versao);
}

function pintarMotor() {
  const m = S.motor;
  // 15/09/2026: na conta AMPLIADA o nome do modelo no alto vira botão que abre a lista de modelos
  const cab = document.getElementById('cab-estado');
  const seta = document.getElementById('cab-trocar');
  const trocavel = modelosTrocaveis().length > 1;
  if (cab) {
    cab.dataset.trocavel = trocavel ? '1' : '';
    if (trocavel) {
      cab.setAttribute('role', 'button');
      cab.tabIndex = 0;
      cab.setAttribute('aria-haspopup', 'dialog');
      cab.title = 'Trocar o modelo';
    } else {
      cab.removeAttribute('role');
      cab.removeAttribute('tabindex');
      cab.removeAttribute('aria-haspopup');
      cab.removeAttribute('title');
    }
  }
  if (seta) seta.hidden = !trocavel;
  if (folhaAberta('folha-modelos')) { if (trocavel) listarModelos(); else fecharFolhas(); }
  const linha = document.getElementById('linha-motor');
  const valor = document.getElementById('cfg-motor');
  const botao = document.getElementById('btn-consentimento');
  if (!linha || !valor || !botao) return;
  linha.hidden = !m;
  if (!m) { botao.hidden = true; return; }
  const externo = motorExterno(m);
  valor.textContent = rotuloDoMotor(m);
  botao.hidden = !externo;
  if (externo) {
    botao.textContent = (m.consentimento && m.consentimento.dado)
      ? `Revogar o uso da ${provedorDoMotor(m)}` : `Ler e aceitar o uso da ${provedorDoMotor(m)}`;
  }
  pintarRevogacoes(botao, m, externo);
}

// 21/09/2026 (revisão de segurança): cada provedor com consentimento registrado tem o seu "Revogar",
// mesmo que o motor da conta agora seja outro (o servidor manda a lista em `consentimentos`). Antes
// o consentimento da Anthropic ficava sem caminho de revogação quando a conta saía do Claude.
function pintarRevogacoes(botao, m, externo) {
  document.querySelectorAll('[data-revogar-provedor]').forEach((n) => n.remove());
  const atual = externo ? provedorDoMotor(m) : null;
  let depois = botao;
  const available = m && m.motor === 'automatico' && Array.isArray(m.provedores_automaticos) ? m.provedores_automaticos : [];
  for (const c of available) {
    if (!c || !c.provedor || c.dado) continue;
    const b = el('button', 'grupo-linha', `Privacidade: autorizar ${c.provedor}`);
    b.type = 'button';
    b.dataset.revogarProvedor = String(c.provedor);
    b.disabled = !(m.consentimento && m.consentimento.dado);
    b.addEventListener('click', () => {
      S.avisoConsentimento = null;
      abrirConsentimento(c.texto, c.provedor, c.versao);
    });
    depois.insertAdjacentElement('afterend', b);
    depois = b;
  }
  for (const c of (Array.isArray(m && m.consentimentos) ? m.consentimentos : [])) {
    if (!c || !c.provedor || !c.dado || c.provedor === atual) continue;
    const b = el('button', 'grupo-linha', `Revogar o uso da ${c.provedor}`);
    b.type = 'button';
    b.dataset.revogarProvedor = String(c.provedor);
    b.addEventListener('click', async () => {
      if (!confirm(`Revogar o uso da ${c.provedor}?\n\nNada desta conta volta a ser enviado a ela sem um novo aceite.`)) return;
      if (await responderConsentimento(false, c.provedor)) carregarMotor();
    });
    depois.insertAdjacentElement('afterend', b);
    depois = b;
  }
}

// Ordem do operador (15/09/2026): "os usuários que podem usar a IALD nativa e o chatgpt, podendo
// selecionar o modelo no próprio app" e "somente clicando em cima do próprio nome do modelo que fica
// no canto superior da tela". A lista vem do servidor (opcoes): o próximo motor entra sem mudar o app.
// O servidor confere de novo se a conta é ampliada (403) e se o modelo está disponível (409).
function modelosTrocaveis() {
  const m = S.motor;
  return (m && m.pode_escolher && Array.isArray(m.opcoes)) ? m.opcoes : [];
}

function abrirModelos() {
  if (modelosTrocaveis().length < 2) return;
  listarModelos();
  abrirFolha('folha-modelos');
}

function listarModelos() {
  const lista = document.getElementById('lista-modelos');
  if (!lista) return;
  lista.innerHTML = '';
  const atual = S.motor && (S.motor.motor_selecao || S.motor.motor);
  for (const o of modelosTrocaveis()) {
    const b = el('button', 'grupo-linha linha-modelo');
    b.type = 'button';
    b.dataset.motor = String(o.id || '');
    const escolhido = o.id === atual;
    if (escolhido) b.setAttribute('aria-current', 'true');
    b.disabled = !!S.trocandoMotor || (!o.disponivel && !escolhido);
    // duas linhas (nome em cima, detalhe embaixo): numa tela de 400 px o detalhe numa linha só cortava
    const textos = el('span', 'lm-textos');
    textos.appendChild(el('span', 'gl-chave', String(o.rotulo || o.id || '')));
    textos.appendChild(el('span', 'lm-detalhe',
      String(o.detalhe || '') + (o.disponivel ? '' : ' · indisponível agora')));
    b.appendChild(textos);
    b.appendChild(el('span', 'lm-marca', escolhido ? '✓' : ''));
    b.addEventListener('click', () => {
      if (escolhido) { fecharFolhas(); return; }
      fecharFolhas();
      escolherMotor(o.id);
    });
    lista.appendChild(b);
  }
}

async function escolherMotor(motor) {
  const m = S.motor;
  if (!m || !modelosTrocaveis().some((o) => o.id === motor) || (m.motor_selecao || m.motor) === motor || S.trocandoMotor) return;
  S.trocandoMotor = true;
  pintarMotor();
  let r, j = {};
  try {
    r = await postarJSON('/api/motor/escolha', { motor });
    j = await r.json().catch(() => ({}));
  } catch (e) {
    S.trocandoMotor = false;
    pintarMotor();
    avisar('Sem conexão com o servidor: o motor não mudou.', 'erro');
    return;
  }
  S.trocandoMotor = false;
  if (!r.ok) { pintarMotor(); avisar(j.error || `O servidor recusou (HTTP ${r.status}).`, 'erro'); return; }
  await carregarMotor();
  conferirServidor();
  const escolhida = modelosTrocaveis().find((o) => o.id === motor);
  avisar(`A partir da próxima mensagem, quem responde é: ${(escolhida && escolhida.rotulo) || motor}.`);
  // 21/09/2026 (revisão de segurança): a folha abre com o texto que a PRÓPRIA escolha devolveu (o do
  // motor efetivo, com provedor e versão). Um /api/motor que falhou depois da troca deixava S.motor
  // antigo — e a folha mostrava o texto da OpenAI (ou nada) antes de um aceite gravado como da Anthropic.
  const c = j && j.consentimento;
  if (c && typeof c === 'object') {
    if (c.necessario && !c.dado) {
      S.avisoConsentimento = null;                       // nada a reenviar: nenhuma pergunta foi feita
      abrirConsentimento(c.texto, c.provedor, c.versao);
    }
  } else if (motorExterno({ motor }) && !j.consentimento_dado && S.motor && S.motor.motor === motor) {
    // servidor sem o bloco (antigo): só o /api/motor JÁ relido para este motor serve
    S.avisoConsentimento = null;
    const f = consentimentoDe(S.motor);
    abrirConsentimento(f.texto, f.provedor, f.versao);
  }
}

function abrirConsentimento(texto, provedor, versao) {
  const caixa = document.getElementById('consentimento-texto');
  if (!caixa) return;
  caixa.innerHTML = '';
  for (const par of String(texto || '').split(/\n{2,}/)) {
    if (par.trim()) caixa.appendChild(el('p', null, par.trim()));
  }
  // de quem é o texto que a pessoa vai ler (o aceite devolve isto ao servidor)
  S.consentimentoFolha = provedor ? { provedor: String(provedor), versao } : null;
  estadoConsentimento('');
  // Close the keyboard before measuring the sheet on iOS.
  if (document.activeElement && typeof document.activeElement.blur === 'function') document.activeElement.blur();
  abrirFolha('folha-consentimento');
}

// `provedor`: o nome que a folha mostrou (aceite) ou o do botão (revogação); `versao`: a do texto lido.
// 409 = o motor da conta mudou (ou o aviso mudou de versão): nada gravado, o estado é relido.
async function responderConsentimento(aceito, provedor, versao) {
  let r, j = {};
  const corpo = { aceito };
  if (provedor) corpo.provedor = String(provedor);
  if (aceito && Number.isInteger(versao)) corpo.versao = versao;
  try {
    r = await fetchIALD('/api/motor/consentimento', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(corpo), signal: AbortSignal.timeout(15000),
    });
    j = await r.json().catch(() => ({}));
  } catch (e) {
    estadoConsentimento('Não foi possível confirmar o aceite. Confira a conexão e tente novamente.');
    return false;
  }
  if (!r.ok) {
    estadoConsentimento(j.error || `O servidor recusou (HTTP ${r.status}). Tente novamente.`);
    if (r.status === 409) {
      // Read the new notice; never apply the previous click to changed terms.
      await carregarMotor();
      const atual = consentimentoDe(S.motor);
      if (atual.texto && atual.provedor && Number.isInteger(atual.versao)) {
        abrirConsentimento(atual.texto, atual.provedor, atual.versao);
        estadoConsentimento('O modelo ou os termos mudaram. Leia o aviso atualizado e decida novamente.');
      }
    }
    return false;
  }
  if (j.ok !== true || j.consentido !== aceito || (provedor && j.provedor !== provedor)) {
    estadoConsentimento('O servidor não confirmou esta autorização. Entre novamente ou tente de novo.');
    return false;
  }
  if (S.motor && Array.isArray(S.motor.provedores_automaticos) && j.provedor) {
    for (const item of S.motor.provedores_automaticos) {
      if (item.provedor === j.provedor) item.dado = aceito;
    }
  }
  const doMotor = S.motor && S.motor.consentimento;
  if (doMotor && (!provedor || !j.provedor || j.provedor === (doMotor.provedor || S.motor.provedor))) doMotor.dado = aceito;
  if (S.motor && Array.isArray(S.motor.consentimentos) && j.provedor) {
    S.motor.consentimentos = S.motor.consentimentos.filter((x) => x && x.provedor !== j.provedor);
    if (aceito) S.motor.consentimentos.push({ provedor: j.provedor, dado: true });
  }
  pintarMotor();
  return true;
}

function estadoConsentimento(texto) {
  const status = document.getElementById('consentimento-status');
  if (status) { status.textContent = texto; status.hidden = !texto; }
  if (texto) avisar(texto, 'erro');
}

async function consentirEContinuar() {
  if (S.consentimentoEnviando) return;
  const folha = S.consentimentoFolha || {};
  if (!folha.provedor || !Number.isInteger(folha.versao)) {
    estadoConsentimento('O aviso está incompleto. Feche e abra novamente os termos antes de aceitar.');
    return;
  }
  S.consentimentoEnviando = true;
  const botao = document.getElementById('btn-consentir');
  botao.disabled = true;
  botao.textContent = 'Confirmando…';
  estadoConsentimento('');
  try {
    if (!(await responderConsentimento(true, folha.provedor, folha.versao))) return;
    fecharFolhas();
    if (mediaPendingConsent) {
      try { await mediaResumeConsent(); } catch (error) { estadoConsentimento(error.message); }
      return;
    }
    const bolha = S.avisoConsentimento;
    S.avisoConsentimento = null;
    if (bolha) { bolha.remove(); reenviarUltima(); }
    else avisar('Autorização confirmada. Você já pode conversar.');
  } finally {
    S.consentimentoEnviando = false;
    botao.disabled = false;
    botao.textContent = 'Concordo e continuar';
  }
}

async function alternarConsentimento() {
  const m = S.motor;
  if (!motorExterno(m)) return;
  if (m.consentimento && m.consentimento.dado) {
    const provedor = provedorDoMotor(m);
    if (!confirm(`Revogar o uso da ${provedor}?\n\nA partir de agora nada desta conta é enviado a ela — `
      + `e, como o motor desta conta é o da ${provedor}, a IALD deixa de responder até você aceitar de novo.`)) return;
    await responderConsentimento(false, consentimentoDe(m).provedor);   // o provedor que o botão nomeou
    return;
  }
  S.avisoConsentimento = null;
  const f = consentimentoDe(m);
  abrirConsentimento(f.texto, f.provedor, f.versao);
}

function fecharPortao() {
  const p = $('#portao');
  if (p) p.hidden = true;
  if (vigiaPedido) { clearInterval(vigiaPedido); vigiaPedido = null; }
  sincronizarBarraDeStatus();
  pintarUsuario();
  carregarContexto();
  S.consentimentoOferecido = false;                      // entrada nova: pode oferecer de novo
  carregarMotor({ aoEntrar: true });
  conferirServidor();
  verificarIdentificacaoCadastro();
  recuperarRespostasBackground();
  $('#entrada').focus();
}

function avaliarPortao() {
  const p = $('#portao');
  if (!p) return;
  if (!portaoNecessario()) {
    p.hidden = true;
    if (vigiaPedido) { clearInterval(vigiaPedido); vigiaPedido = null; }
    sincronizarBarraDeStatus();
    return;
  }
  p.hidden = false;
  sincronizarBarraDeStatus();
  pintarBotoesEntrada();
  carregarConfigEntrada();
  if (recuperar(K.pedido, '')) {
    mostrarVista('pendente');
    verificarSituacao(false);
  } else {
    mostrarVista('entrar');
  }
}

// ══════════════════════════════════════════════════════════════
// PARTIDA
// ══════════════════════════════════════════════════════════════
function iniciar() {
  startArtifactAccessUI();
  aplicarTema(recuperar(K.tema, ''));
  S.modo = recuperar(K.modo, 'fast') === 'think' ? 'think' : 'fast';

  ligar();
  carregarPerfil();
  pintarModo();
  pintarBusca();
  pintarAnexar();
  carregarConversas();
  redimensionarEntrada();
  atualizarBotaoEnviar();
  acompanharTeclado();

  $('#rodape-versao').textContent = VERSAO + (DEMO ? ' · demonstração' : '');
  document.querySelectorAll('[data-versao]').forEach((n) => { n.textContent = VERSAO; });
  document.querySelectorAll('[data-beta-linha]').forEach((n) => { n.textContent = 'β_TGL = α × √e = ' + String(BETA_TGL); });
  document.querySelectorAll('[data-beta-valor]').forEach((n) => { n.textContent = 'α × √e = ' + String(BETA_TGL).slice(0, 10) + '…'; });

  carregarContexto();
  carregarMotor({ aoEntrar: true });
  conferirServidor();
  setInterval(conferirServidor, 20000);

  if (window.innerWidth >= 861) abrirLateral();

  // A volta do navegador (Google, e Apple no Android) chega por link br.ia.iald://
  ouvirRetornoDoNavegador();

  // Por último: no invólucro nativo sem token, o portão cobre a tela.
  // carregarContexto() e conferirServidor() já rodaram acima; fecharPortao() os
  // repete DE PROPÓSITO — depois da entrada existe token, e as chamadas passam a
  // ir autenticadas, com o estado real em vez do estado de quem ainda não entrou.
  avaliarPortao();
  if (!portaoNecessario()) verificarIdentificacaoCadastro();
  ligarRespostasBackground();
  startNativeNotificationsUI();
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
else iniciar();
