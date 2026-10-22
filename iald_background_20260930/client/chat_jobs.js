// Durable transport only. All HTTP uses the app's authenticated request function.
export const TERMINAL_JOB_STATUSES = new Set(['completed', 'failed', 'cancelled', 'interrupted', 'expired']);
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
const ACCOUNT = /^[0-9a-f]{64}$/;
const STATUSES = new Set(['queued', 'running', ...TERMINAL_JOB_STATUSES]);
const copy = (value) => JSON.parse(JSON.stringify(value));

export class PendingChatJobError extends Error {
  constructor(message, extra = {}) {
    super(message); this.name = 'PendingChatJobError'; this.pending = true;
    Object.assign(this, extra);
  }
}
export class TerminalChatJobError extends Error {
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

export function createDurableChatJobs({ request, storage, randomUUID = () => crypto.randomUUID(),
  sleep = defaultSleep, onPending = () => {}, onSubmitted = () => {}, onScopeLost = () => {}, requestTimeout = 20000 }) {
  let owner = '', generation = 0;
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
      const raw = JSON.stringify(records);
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
  async function http(path, options, scope, signal) {
    check(scope);
    const controller = new AbortController();
    const abort = () => controller.abort();
    if (signal?.aborted) throw detached();
    signal?.addEventListener('abort', abort, { once: true });
    active.add(controller);
    const timer = setTimeout(abort, requestTimeout);
    try {
      const response = await request(path, { ...options, cache: 'no-store', signal: controller.signal });
      check(scope);
      if (response.status === 401) loseScope();
      if (response.status === 410 && (!options.method || options.method === 'GET') &&
          /^\/api\/chat-jobs\/[0-9a-f-]{36}(?:\?after=\d+)?$/.test(path)) {
        throw new TerminalChatJobError('expired', 'Esta resposta temporária expirou. Nenhum novo pedido foi enviado.');
      }
      let body;
      try { body = await response.json(); } catch (_) { throw new PendingChatJobError('Resposta do servidor ilegível; o pedido continua pendente.'); }
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
    write([...records, record], scope); // Mandatory verified write BEFORE any submit.
    return record;
  }
  async function submit(record, scope, signal) {
    assertRecord(record, scope);
    if (record.id) return;
    if (!record.payload) throw new PendingChatJobError('Pedido sem corpo local; recupere-o pela lista do servidor.');
    if (record.payload.account !== scope.owner || record.payload.request_id !== record.request_id) throw detached();
    await verifyAccount(scope, signal);
    update(record, scope, { attempted: true });
    const response = await post('/api/chat-jobs', record.payload, scope, signal);
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
    else await submit(record, scope, signal);
    if (record.local_cancel) throw new TerminalChatJobError('cancelled', 'Pedido cancelado antes do envio.');
    let cursor = 0, sawDone = false, sawError = false;
    // Every resumed observer replays from zero into a fresh UI buffer. No partial
    // answer is persisted as final and no replay appends to an earlier draft.
    while (true) {
      check(scope);
      let page;
      try { page = await http('/api/chat-jobs/' + record.id + '?after=' + cursor, {}, scope, signal); }
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
export function applyChatJobDelivery(conversation, job, { answer = null, notice = null, status = 'completed' }) {
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
