/* Local-only preparation. No network endpoint or backend reference contract here. */
'use strict';
(function (scope) {
  const LIMIT_TEXT = 'Áudio/vídeo: até 50 MB em base64 (aproximadamente 37,5 MB de arquivo). O servidor valida o tamanho e a admissão do contexto, preservando a memória TGL.';
  function encodedBytes(bytes) {
    if (!Number.isSafeInteger(bytes) || bytes < 0) throw new TypeError('Tamanho de arquivo inválido.');
    return 4 * Math.ceil(bytes / 3);
  }
  function validateLocalBlob(blob, kind, maxEncodedBytes) {
    if (!(blob instanceof Blob) || !blob.size || !['audio', 'video'].includes(kind))
      throw new TypeError('Arquivo local de áudio/vídeo inválido.');
    if (!Number.isSafeInteger(maxEncodedBytes) || maxEncodedBytes <= 0)
      throw new TypeError('Limite oficial ainda não vinculado ao contrato.');
    if (encodedBytes(blob.size) > maxEncodedBytes)
      throw new RangeError('A mídia ultrapassa 50 MB em base64 (aproximadamente 37,5 MB de arquivo).');
    // Duration is not a transport-size limit. MIME/content/context validation is server-owned.
    return { kind, bytes: blob.size, encodedBytes: encodedBytes(blob.size) };
  }
  function partition(owner, conversation, id) {
    if ([owner, conversation, id].some(x => typeof x !== 'string' || !x || x.length > 512))
      throw new TypeError('Conta, conversa e identificador local são obrigatórios.');
    return JSON.stringify([owner, conversation, id]);
  }
  class BlobDrafts {
    constructor(indexedDB, maxEncodedBytes) {
      this.indexedDB = indexedDB;
      this.maxEncodedBytes = maxEncodedBytes;
      this.opening = null;
    }
    open() {
      if (!this.indexedDB || typeof this.indexedDB.open !== 'function')
        return Promise.reject(new Error('Armazenamento local indisponível. O arquivo não foi enviado.'));
      if (this.opening) return this.opening;
      this.opening = new Promise((resolve, reject) => {
        const request = this.indexedDB.open('iald-local-media-drafts-v1', 1);
        request.onupgradeneeded = () => request.result.createObjectStore('drafts', { keyPath: 'key' });
        request.onerror = () => reject(new Error('Falha ao abrir a mídia local. O arquivo não foi enviado.'));
        request.onblocked = () => reject(new Error('Armazenamento local bloqueado por outra janela.'));
        request.onsuccess = () => {
          const database = request.result;
          database.onversionchange = () => { database.close(); this.opening = null; };
          resolve(database);
        };
      }).catch(error => { this.opening = null; throw error; });
      return this.opening;
    }
    async transaction(mode, action) {
      const database = await this.open();
      return new Promise((resolve, reject) => {
        const tx = database.transaction('drafts', mode);
        let value;
        tx.oncomplete = () => resolve(value);
        tx.onerror = tx.onabort = () => reject(new Error('Falha ao guardar ou recuperar mídia local. O arquivo não foi enviado.'));
        try {
          const request = action(tx.objectStore('drafts'));
          request.onsuccess = () => { value = request.result; };
        } catch (error) { tx.abort(); reject(error); }
      });
    }
    async put(owner, conversation, id, blob, kind, name) {
      const key = partition(owner, conversation, id);
      const metadata = validateLocalBlob(blob, kind, this.maxEncodedBytes);
      const record = { key, owner, conversation, id, blob, name: String(name || 'mídia'), ...metadata };
      await this.transaction('readwrite', store => store.put(record));
      // Only this local pointer belongs in UI metadata; never serialize the Blob or a data URL.
      return { localDraftId: id, kind, name: record.name, bytes: metadata.bytes };
    }
    async get(owner, conversation, id) {
      const key = partition(owner, conversation, id);
      const record = await this.transaction('readonly', store => store.get(key));
      if (!record) throw new Error('Mídia local não encontrada. Selecione o arquivo novamente.');
      if (record.owner !== owner || record.conversation !== conversation || record.id !== id)
        throw new Error('A mídia local pertence a outra conta ou conversa.');
      validateLocalBlob(record.blob, record.kind, this.maxEncodedBytes);
      return record;
    }
    async remove(owner, conversation, id) {
      const key = partition(owner, conversation, id);
      return this.transaction('readwrite', store => store.delete(key));
    }
  }
  const api = { LIMIT_TEXT, encodedBytes, validateLocalBlob, partition, BlobDrafts };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else scope.IALDLocalMediaDrafts = api;
})(globalThis);
