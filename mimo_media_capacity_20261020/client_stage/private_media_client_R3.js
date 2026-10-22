// Embedded private-media integration. No upload is performed by the file picker.
const MEDIA_RAW_MAX = 37_499_904;
const MEDIA_BASE64_MAX = 50_000_000;
const MEDIA_LIMIT_TEXT = 'Áudio/vídeo: até 50 MB em base64 (aproximadamente 37,5 MB de arquivo). O servidor verifica o contexto preservando a memória TGL; não há limite fixo de duração.';
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
  if (!conversation || !backgroundOwner || conversation.background_owner !== backgroundOwner) return;
  const owner = backgroundOwner, id = conversation.id;
  const records = await mediaLocal('readonly', store => store.index('conversation').getAll([mediaStorageScope(), owner, id]));
  if (owner !== backgroundOwner || S.ativaId !== id) return;
  const drafts = records.filter(r => r.selected === true);
  S.anexos = S.anexos.filter(a => !a.localDraftId).concat(drafts.map(r => ({ name: r.name, media: mediaURL(r), mediaKind: r.kind, mime: r.mime,
    localDraftId: r.id, mediaOwner: owner, mediaConversation: id, kb: Math.round(r.blob.size / 1024) })));
  desenharAnexos(); atualizarBotaoEnviar();
}
async function lerMidiaLocal(f, tipo) {
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
  if (anexos.filter(a => a.localDraftId).length > 1) throw Error('Uma mídia de áudio/vídeo por mensagem.');
  const owner = backgroundOwner; mediaScope(owner, conversation);
  const response = await fetchIALD('/api/motor', { cache: 'no-store' });
  if (!response.ok) throw Error('Não foi possível conferir as autorizações. Nenhuma mídia foi enviada.');
  const motor = await response.json(); mediaScope(owner, conversation);
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
async function mediaUpload(anexo, owner, conversation) {
  mediaScope(owner, conversation);
  if (anexo.mediaOwner !== owner || anexo.mediaConversation !== conversation) throw Error('O anexo pertence a outra conversa.');
  const uploadKey = mediaKey(owner, conversation, anexo.localDraftId);
  if (mediaUploadsInFlight.has(uploadKey)) throw Error('O mesmo anexo já está em envio. O pedido não foi repetido.');
  mediaUploadsInFlight.add(uploadKey);
  try {
  const record = await mediaLoad(owner, conversation, anexo.localDraftId);
  if (record.part) return canonicalMediaPart(record.part);
  if (record.state !== 'local') throw Error('Envio anterior da mídia sem conclusão confirmada. Não foi repetido; confira a situação antes de reenviar.');
  mediaValidateSize(record.blob.size, mediaLimits(record.kind)); mediaScope(owner, conversation);
  // Persist intent BEFORE the one upload. Lost responses never auto-retry.
  record.state = 'uncertain'; await mediaLocal('readwrite', store => store.put(record));
  mediaScope(owner, conversation); avisar('Enviando mídia privada…');
  const response = await fetchIALD('/api/private-media?conversation_id=' + encodeURIComponent(conversation), {
    method: 'POST', headers: { 'Content-Type': record.mime }, body: record.blob,
  });
  if (!response.ok) throw Error('O servidor recusou a mídia (HTTP ' + response.status + '). O histórico foi preservado; o envio não foi repetido.');
  const part = canonicalMediaPart(await response.json());
  if (part.kind !== record.kind || part.mime !== record.mime || part.bytes !== record.blob.size) throw Error('Metadados da mídia não correspondem ao arquivo enviado.');
  record.part = part; record.state = 'stored'; await mediaLocal('readwrite', store => store.put(record));
  mediaScope(owner, conversation); return part;
  } finally { mediaUploadsInFlight.delete(uploadKey); }
}
async function mediaMigrateLegacy(conversations, owner) {
  let changed = false;
  for (const c of conversations) {
    for (const message of c.mensagens || []) {
      if (!Array.isArray(message.content)) continue;
      for (let i = 0; i < message.content.length; i++) {
        const part = message.content[i];
        const data = part?.type === 'input_audio' ? part.input_audio?.data : part?.type === 'video_url' ? part.video_url?.url : null;
        if (typeof data !== 'string' || !/^data:(audio|video)\//.test(data)) continue;
        if (!mediaStorageScope()) throw Error('O histórico antigo contém mídia. Aguarde o escopo seguro do servidor; o original não foi sobrescrito.');
        const match = /^data:((audio|video)\/[a-z0-9.+-]+);base64,([A-Za-z0-9+/=\r\n]+)$/i.exec(data);
        if (!match) throw Error('Mídia antiga ilegível; o histórico original não foi sobrescrito.');
        const binary = atob(match[3]); mediaValidateSize(binary.length, { raw: MEDIA_RAW_MAX, encoded: MEDIA_BASE64_MAX });
        const blob = new Blob([Uint8Array.from(binary, c => c.charCodeAt(0))], { type: match[1] });
        const id = crypto.randomUUID(), key = mediaKey(owner, c.id, id);
        const record = { key, storageScope: mediaStorageScope(), owner, conversation: c.id, id, blob, kind: match[2], mime: match[1], name: 'Mídia do histórico', selected: false, state: 'local' };
        await mediaLocal('readwrite', store => store.put(record));
        message.content[i] = { type: 'iald_local_media', localDraftId: id, kind: record.kind, mime: record.mime, bytes: blob.size };
        changed = true;
      }
    }
  }
  return changed;
}
function mediaAssertHistory(conversations) {
  for (const c of conversations) for (const message of c.mensagens || []) if (Array.isArray(message.content)) for (const p of message.content) {
    if (p?.type === 'input_audio' || p?.type === 'video_url') throw Error('Mídia antiga precisa ser recuperada localmente antes de salvar. O histórico não foi apagado.');
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
        const r = await fetchIALD('/api/private-media/' + p.media_ref + '?conversation_id=' + encodeURIComponent(conversation), { cache: 'no-store' });
        if (!r.ok) throw Error('Anexo indisponível nesta conta/conversa.');
        const actual = canonicalMediaPart(await r.json()); mediaScope(owner, conversation);
        if (actual.media_ref !== p.media_ref || actual.sha256 !== p.sha256) throw Error('Referência de mídia alterada.');
        info.textContent = 'Mídia privada conferida · ' + actual.kind + ' · ' + actual.duration_seconds.toFixed(1) + ' s · preservada até exclusão da conversa/conta.';
      } catch (error) { avisar(error.message); }
    });
  }
}
