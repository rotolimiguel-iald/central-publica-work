from pathlib import Path
p=Path(r'C:/IALD/Central de Patentes/work/app_attachments_beta_wait_20261021/repair');(p/'stage/app').mkdir(parents=True,exist_ok=True)
s=(p/'baseline/app/iald.js').read_text(encoding='utf-8')
helper=r'''// Account-scoped durable JSON. No media permission changes or provider calls.
// IndexedDB owns atomic full snapshots; WebStorage stores only small pointers.
function createChatLocalStore({ indexedDB = globalThis.indexedDB, crypto = globalThis.crypto } = {}) {
  let opening;
  const failure = () => new PendingChatJobError('Armazenamento local indisponível. O conteúdo foi preservado nesta aba; o envio não foi iniciado.');
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
  return { put, get, remove };
}

'''
s=s.replace('function createDurableChatJobs({ request, storage, randomUUID',helper+'function createDurableChatJobs({ request, storage, payloadStore = null, randomUUID',1)
s=s.replace('const raw = JSON.stringify(records);','const raw = JSON.stringify(records.map(r => r.payload_ref ? { ...r, payload: null } : r));',1)
s=s.replace("    write([...records, record], scope); // Mandatory verified write BEFORE any submit.","    if (payloadStore) {\n      record.payload_ref = await payloadStore.put(scope.owner, 'payload', JSON.stringify(record.payload));\n      check(scope);\n    }\n    write([...records, record], scope); // Mandatory verified write BEFORE any submit.",1)
s=s.replace("    if (!record.payload) throw new PendingChatJobError('Pedido sem corpo local; recupere-o pela lista do servidor.');\n    if (record.payload.account !== scope.owner || record.payload.request_id !== record.request_id) throw detached();\n",'',1)
s=s.replace('    const fullJSON = JSON.stringify(record.payload);',"    if (record.payload_ref) {\n      if (!payloadStore) throw new PendingChatJobError('Armazenamento do pedido indisponível.');\n      record.payload = JSON.parse(await payloadStore.get(scope.owner, 'payload', record.payload_ref));\n      check(scope);\n    }\n    if (!record.payload) throw new PendingChatJobError('Pedido sem corpo local; recupere-o pela lista do servidor.');\n    if (record.payload.account !== scope.owner || record.payload.request_id !== record.request_id) throw detached();\n    const fullJSON = JSON.stringify(record.payload);",1)
# Drop a payload only after ack AND local outbox removal. Failure leaves a harmless orphan.
s=s.replace("    write(read().filter((r) => r.request_id !== record.request_id), scope);\n  }\n  async function delivered", "    write(read().filter((r) => r.request_id !== record.request_id), scope);\n    if (payloadStore && record.payload_ref) {\n      try { await payloadStore.remove(scope.owner, 'payload', record.payload_ref); }\n      catch (_) { onPending('Entrega confirmada; limpeza local do corpo ainda pendente.'); }\n    }\n  }\n  async function delivered",1)
s=s.replace('const backgroundJobs = createDurableChatJobs({','const chatLocalStore = createChatLocalStore();\nlet backgroundHistoryWrites = Promise.resolve();\nconst backgroundJobs = createDurableChatJobs({',1)
s=s.replace('  request: fetchIALD, storage: localStorage,','  request: fetchIALD, storage: localStorage, payloadStore: chatLocalStore,',1)
a=s.index('function persistirConversasBackground()');b=s.index('function desanexarRespostasBackground(',a)
s=s[:a]+'''function persistirConversasBackground() {
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
''' +s[b:]
s=s.replace("      history = JSON.parse(raw);\n      if (!history", "      history = JSON.parse(raw);\n      if (history?.chat_local_history_v1) {\n        history = JSON.parse(await chatLocalStore.get(account, 'history', history.chat_local_history_v1));\n        if (token !== tokenApp() || (backgroundOwner && backgroundOwner !== account)) throw detached();\n      }\n      if (!history",1)
s=s.replace('    if (backgroundOwner) desanexarRespostasBackground(true);\n    const raw', '    if (backgroundOwner) desanexarRespostasBackground(true);\n    const loadEpoch = backgroundEpoch;\n    const raw',1)
s=s.replace('if (token !== tokenApp() || (backgroundOwner && backgroundOwner !== account)) throw detached();','if (loadEpoch !== backgroundEpoch || token !== tokenApp()) throw detached();',1)
s=s.replace('    persistirConversasBackground(); // Mandatory verified history write before ack.','    return persistirConversasBackground(); // Mandatory verified history write before ack.',1)
s=s.replace('if (!DEMO && backgroundOwner) { persistirConversasBackground(); return; }',"if (!DEMO && backgroundOwner) {\n    const saved = persistirConversasBackground();\n    saved.catch(error => avisarBackground('Alteração preservada nesta aba, mas ainda não salva: ' + error.message));\n    return saved;\n  }",1)
s=s.replace('  mediaAssertHistory(S.conversas);\n  salvarConversas();\n  if (hasMedia)', '  mediaAssertHistory(S.conversas);\n  await salvarConversas();\n  if (hasMedia)',1)
s=s.replace('      persistirConversasBackground();\n      job ||=', '      await persistirConversasBackground();\n      job ||=',1)
s=s.replace("    failure = error;", "    failure = error;\n    if (!job && !error.detached) error.notSubmitted = true;",1)
s=s.replace("      } : null;\n      pintarAviso(corpo.parentElement, conteudo, deliveryNotice", "      } : failure?.notSubmitted ? {\n        tipo: 'envio_local_bloqueado', retirar_resposta: true,\n        texto: 'Mensagem não enviada. ' + failure.message + ' Nenhuma entrega pelo servidor foi iniciada.',\n      } : null;\n      pintarAviso(corpo.parentElement, conteudo, deliveryNotice",1)
s=s.replace("  em_andamento: ['Resposta em andamento'", "  envio_local_bloqueado: ['Mensagem não enviada', ICONE.ampulheta, ''],\n  em_andamento: ['Resposta em andamento'",1)
(p/'stage/app/iald.js').write_bytes(s.replace('\n','\r\n').encode())
import difflib
(p/'PATCH.diff').write_text(''.join(difflib.unified_diff((p/'baseline/app/iald.js').read_text(encoding='utf-8').splitlines(True),s.splitlines(True),fromfile='baseline/app/iald.js',tofile='stage/app/iald.js')),encoding='utf-8')
print('stage created')
