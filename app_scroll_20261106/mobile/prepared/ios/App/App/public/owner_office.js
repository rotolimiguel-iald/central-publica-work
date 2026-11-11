// Bundled source: private_chat_controller.mjs
/* Staging candidate. Transport is injected only after its independent review.
 * This controller owns no public history, storage, model, wallet or export API.
 */
export class PrivateChatRefused extends Error {
  constructor(code) { super(code); this.name = 'PrivateChatRefused'; this.code = code; }
}

// The same terminal representation is used by polling and history recovery.
// Server/model error text is not injected; only a local status and safe copy.
export function privateTerminalMessage(result) {
  if (result.status === 'completed' && typeof result.answer === 'string' && result.answer.trim()) {
    return { role: 'assistant', content: result.answer, status: 'completed', job_id: result.job_id || result.id };
  }
  const labels = {
    failed: 'A consulta privada não concluiu.', interrupted: 'A consulta privada foi interrompida.',
    cancelled: 'A consulta privada foi cancelada.', expired: 'A consulta privada expirou.',
    completed: 'A consulta terminou sem uma resposta legível.'
  };
  const partial = typeof result.answer === 'string' && result.answer.trim()
    ? '\n\nResposta parcial preservada (não concluída):\n' + result.answer : '';
  return { role: 'assistant', status: result.status, job_id: result.job_id || result.id, failed: true,
    content: (labels[result.status] || 'Não foi possível confirmar a resposta privada.') +
      ' O pedido foi preservado; nenhum reenvio foi feito.' + partial };
}

export function createPrivateChatController({ api, onState = () => {}, uuid = () => crypto.randomUUID(), getConversationId }) {
  const refuse = code => { throw new PrivateChatRefused(code); };
  const privateUuid = value => typeof value === 'string' && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value);
  let epoch = 0, revision = 0, destroyed = false, refreshing = null;
  let abort = new AbortController();
  let privateHandle = null, viewId = uuid(), uncertainRequestId = null;
  let promptView = null, restoreUnverified = false, neutralRevision = 0;
  const activeView = () => getConversationId ? getConversationId() : viewId;
  const pollRecoveryAttempted = new Set();
  let state = blank();
  function blank() {
    return { mode: 'undetermined', available: false, reauthenticate: false,
      busy: false, checking: false, following: true, conversationId: null, jobId: null, jobStatus: null, pendingJobs: [], failureCode: '', historyRequired: false, uncertain: false,
      messages: [], notice: '', privacy: false };
  }
  function snapshot() { return { ...state, messages: state.messages.map(x => ({ ...x })), revision }; }
  function emit() { revision++; onState(snapshot()); }
  function current(ticket) { if (destroyed || ticket !== epoch) refuse('STALE_IDENTITY_OR_VIEW'); }
  function begin() { if (destroyed) refuse('DESTROYED'); return { ticket: epoch, signal: abort.signal }; }
  function safeNotice(code) {
    state.notice = code; emit();
    return { route: 'blocked', code };
  }
  function clearPrivateAccess(notice, askOwner = false) {
    epoch++; abort.abort(); abort = new AbortController(); refreshing = null;
    api.resetIdentity?.(); privateHandle = null;
    promptView = askOwner ? activeView() : null;
    state.available = false; state.reauthenticate = askOwner; state.messages = [];
    state.following = false; state.busy = false; state.checking = false;
    state.mode = state.privacy ? 'private-locked' : 'undetermined';
    state.notice = notice; state.failureCode = '';
    // Opaque receipts allow read-only reconciliation. Never replay a start.
    emit();
  }
  function routeFailure() {
    clearPrivateAccess('LOCAL_PREFLIGHT_REFUSED');
    return { route: 'blocked', code: state.notice };
  }
  function lockAuthorization(error, ticket) {
    if (error?.code !== 'PRIVATE_AUTHORIZATION_DENIED' || ticket !== epoch || destroyed) return false;
    const askOwner = error.reason === 'owner-proof';
    const notice = askOwner ? 'REAUTHENTICATE' : error.reason === 'session' ? 'SESSION_UNAVAILABLE' : 'PRIVATE_UNAVAILABLE';
    clearPrivateAccess(notice, askOwner);
    return true;
  }
  async function refresh() {
    if (destroyed) return false;
    if (refreshing) return refreshing;
    const { ticket, signal } = begin(), view = activeView();
    const operation = (async () => {
      try {
        const result = await api.capability({ signal }); current(ticket);
        if (activeView() !== view) return false;
        const available = result?.available === true;
        if (!available && result?.reauthenticate !== true) neutralRevision++;
        // Capability alone never initiates an invitation. Retain a scoped decision,
        // or recover one from server-side context for an already private conversation.
        let askOwner = !available && result?.reauthenticate === true && promptView === view && view != null;
        if (!available && result?.reauthenticate === true && state.privacy && !askOwner) {
          const context = await api.preflight({conversation_id: view}, {signal, intent: 'restore'});
          current(ticket);
          if (activeView() !== view) return false;
          askOwner = context.route === 'reauthenticate';
        }
        if (!available && state.privacy && state.mode !== 'private-locked') {
          clearPrivateAccess(askOwner ? 'REAUTHENTICATE' : 'PRIVATE_UNAVAILABLE', askOwner);
        } else {
          state.available = available; state.reauthenticate = askOwner;
          promptView = askOwner ? view : null;
          if (askOwner) state.notice = 'REAUTHENTICATE';
          else if (state.notice === 'REAUTHENTICATE') state.notice = state.privacy ? 'PRIVATE_UNAVAILABLE' : '';
          emit();
        }
        return true;
      } catch (error) {
        if (ticket !== epoch || destroyed || activeView() !== view) return false;
        if (!lockAuthorization(error, ticket)) clearPrivateAccess(state.privacy ? 'PRIVATE_UNAVAILABLE' : '');
        return false;
      }
    })();
    refreshing = operation;
    try { return await operation; } finally { if (refreshing === operation) refreshing = null; }
  }
  async function identityChanged() {
    // Synchronous erasure before the capability await, including a same-token login.
    epoch++; abort.abort(); abort = new AbortController(); refreshing = null;
    privateHandle = null; viewId = uuid(); uncertainRequestId = null;
    promptView = null; restoreUnverified = false; pollRecoveryAttempted.clear();
    api.resetIdentity?.();
    state = blank(); emit();
    await refresh();
  }
  function logout() {
    epoch++; abort.abort(); abort = new AbortController(); refreshing = null;
    privateHandle = null; viewId = uuid(); uncertainRequestId = null;
    promptView = null; restoreUnverified = false; pollRecoveryAttempted.clear();
    api.resetIdentity?.();
    state = blank(); emit();
  }
  function newConversation() {
    // Explicit user navigation creates an independent conversation; no private-to-public conversion.
    logout();
  }
  async function classify(message, routingMessages = null, intent = 'send') {
    const { ticket, signal } = begin();
    const conversationId = getConversationId ? getConversationId() : viewId;
    if (typeof conversationId !== 'string' || !/^[A-Za-z0-9_-]{1,128}$/.test(conversationId)) refuse('INVALID_VIEW_ID');
    const request = { conversation_id: conversationId, messages: routingMessages || [{ role: 'user', content: message }] };
    if (privateHandle) request.private_handle = privateHandle;
    const observed = neutralRevision;
    let result;
    try {
      result = await api.preflight(request, { signal, intent });
    } catch (error) {
      if (error?.reason === 'owner-proof' && observed !== neutralRevision) throw new PrivateAuthorizationDenied();
      throw error;
    }
    current(ticket);
    // A newer neutral capability supersedes a delayed private decision on the
    // same view. An explicitly public result still follows the usual guards.
    if (observed !== neutralRevision && ['private', 'reauthenticate'].includes(result?.route)) {
      throw new PrivateAuthorizationDenied();
    }
    if (getConversationId && getConversationId() !== conversationId) refuse('STALE_IDENTITY_OR_VIEW');
    if (!result || !['public', 'private', 'reauthenticate', 'unavailable'].includes(result.route)) {
      refuse('INVALID_PREFLIGHT');
    }
    if (result.route === 'reauthenticate') throw new PrivateAuthorizationDenied('owner-proof');
    promptView = null; state.reauthenticate = false;
    if (state.notice === 'REAUTHENTICATE') { state.notice = ''; emit(); }
    if (result.route === 'unavailable' && state.privacy) throw new PrivateAuthorizationDenied();
    if (result.route === 'public' && state.privacy) refuse('PRIVATE_DOWNGRADE_REFUSED');
    if (result.route === 'private' && !privateUuid(result.private_handle)) refuse('PRIVATE_HANDLE_REQUIRED');
    if (result.route === 'private') privateHandle = result.private_handle;
    if (result.route === 'public' || result.route === 'private') restoreUnverified = false;
    return { ...result, publicViewId: conversationId };
  }
  async function submit({ message, attachmentCount = 0, routingMessages = null }) {
    if (typeof message !== 'string' || !message.trim()) refuse('INVALID_MESSAGE');
    if (!Number.isSafeInteger(attachmentCount) || attachmentCount < 0) refuse('INVALID_ATTACHMENTS');
    if (state.mode === 'private-locked' && state.reauthenticate) return safeNotice('REAUTHENTICATE');
    if (state.historyRequired) return safeNotice('PRIVATE_HISTORY_RECOVERY_REQUIRED');
    if (state.checking || state.jobId || state.uncertain) return safeNotice('PRIVATE_WORK_PENDING_RECOVER_FIRST');
    const { ticket, signal } = begin();
    state.checking = true; state.notice = ''; state.failureCode = ''; emit();
    let startAttempted = false;
    try {
      // First operation carrying the human message: exclusively the local preflight.
      const decision = await classify(message, routingMessages); current(ticket);
      if (decision.route === 'unavailable') return safeNotice('PRIVATE_UNAVAILABLE');
      if (decision.route === 'public') {
        // Caller may continue the original public path only for this explicit result.
        // Opaque context must never be saved in public history or model messages.
        return { route: 'public', epoch: ticket, publicViewId: decision.publicViewId };
      }
      state.privacy = true; state.mode = 'private'; emit();
      if ([...message].length > 12000) return safeNotice('PRIVATE_MESSAGE_TOO_LONG');
      if (attachmentCount) return safeNotice('PRIVATE_ATTACHMENTS_NOT_IN_REVIEWED_CONTRACT');
      const requestId = uuid();
      uncertainRequestId = requestId;
      startAttempted = true;
      const result = await api.start({ message, private_handle: privateHandle,
        private_conversation_id: state.conversationId, request_id: requestId }, { signal });
      current(ticket);
      if (typeof result?.job_id !== 'string' || !result.job_id ||
          !privateUuid(result?.private_conversation_id) || result.private_conversation_id !== privateHandle ||
          (state.conversationId && state.conversationId !== result.private_conversation_id)) {
        refuse('INVALID_PRIVATE_RECEIPT');
      }
      state.conversationId = result.private_conversation_id; state.jobId = result.job_id;
      state.jobStatus = result.status;
      uncertainRequestId = null;
      state.following = true;
      state.messages.push({ role: 'user', content: message });
      state.notice = 'PRIVATE_RUNNING'; emit();
      if (!['queued','running'].includes(result.status)) await poll();
      return { route: 'private', accepted: true };
    } catch (error) {
      if (ticket !== epoch || destroyed) return { route: 'blocked', code: 'STALE_IDENTITY_OR_VIEW' };
      if (error?.code === 'PRIVATE_AUTHORIZATION_DENIED') {
        if (startAttempted) state.uncertain = true;
        lockAuthorization(error, ticket); return { route: 'blocked', code: state.notice };
      }
      if (startAttempted) state.uncertain = true;
      return startAttempted ? safeNotice('PRIVATE_RECEIPT_UNCERTAIN_RECOVER_NO_RESEND') : routeFailure();
    } finally {
      if (ticket === epoch && !destroyed) { state.checking = false; state.busy = !!state.jobId && state.following && ['queued','running'].includes(state.jobStatus); emit(); }
    }
  }
  async function poll() {
    if (!state.privacy || !state.following || !state.jobId || state.mode === 'private-locked') return;
    const { ticket, signal } = begin(), jobId = state.jobId;
    try {
      const result = await api.get({ job_id: jobId }, { signal }); current(ticket);
      if (state.jobId !== jobId) return;
      if (result?.status === 'queued' || result?.status === 'running') {
        state.jobStatus = result.status; state.busy = true; emit(); return;
      }
      if (!['completed', 'failed', 'interrupted', 'cancelled', 'expired'].includes(result?.status)) refuse('INVALID_JOB_STATUS');
      if (result.status === 'completed' && typeof result.answer !== 'string') refuse('INVALID_PRIVATE_ANSWER');
      state.messages.push(privateTerminalMessage({ ...result, job_id: jobId }));
      const next = state.pendingJobs.shift();
      state.jobId = next?.id || null; state.jobStatus = next?.status || result.status;
      state.busy = !!next; state.notice = 'PRIVATE_' + result.status.toUpperCase(); emit();
    } catch (error) {
      if (ticket !== epoch || destroyed) return;
      if (lockAuthorization(error, ticket)) return;
      if (state.jobId !== jobId) return;
      // A failed observer is not evidence that a job is still running or cancelled.
      state.busy = false; state.following = false; state.historyRequired = true;
      if (!pollRecoveryAttempted.has(jobId)) {
        // One readonly recovery per job/view. Never replay start or loop on failure.
        pollRecoveryAttempted.add(jobId);
        const recovery = recover(privateHandle, { fromPoll: true }), recoveryTicket = epoch;
        await recovery;
        if (error?.code === 'PRIVATE_NOT_FOUND' && epoch === recoveryTicket && !destroyed && state.privacy && !state.jobId && !state.uncertain && state.notice === 'PRIVATE_RECOVERED') {
          state.notice = 'PRIVATE_JOB_NOT_FOUND'; emit();
        }
        return;
      }
      state.failureCode = error?.httpStatus ? 'HTTP_' + error.httpStatus : error?.code === 'PRIVATE_TRANSPORT_UNCERTAIN' ? 'NETWORK_OR_TIMEOUT' : 'INVALID_RESPONSE';
      state.notice = 'PRIVATE_STATUS_UNAVAILABLE_RECOVER_NO_RESEND';
      emit();
    }
  }
  async function recover(privateConversationId = privateHandle, { fromPoll = false } = {}) {
    if (state.mode === 'private-locked' && state.reauthenticate) return safeNotice('REAUTHENTICATE');
    if (privateConversationId !== null && !privateUuid(privateConversationId)) refuse('INVALID_CONVERSATION');
    if (state.checking && !fromPoll) return { route: 'blocked', code: 'PRIVATE_RECOVERY_IN_PROGRESS' };
    // History becomes authoritative for this view; older polls cannot resurrect a job.
    epoch++; abort.abort(); abort = new AbortController(); refreshing = null;
    const { ticket, signal } = begin();
    state.privacy = true; state.mode = 'private'; state.historyRequired = true; state.checking = true;
    state.busy = false; state.following = false; state.failureCode = ''; emit();
    try {
      const args = { private_conversation_id: privateConversationId };
      if (state.uncertain && uncertainRequestId) args.uncertain_request_id = uncertainRequestId;
      const result = await api.history(args, { signal }); current(ticket);
      if (!privateUuid(result?.private_conversation_id) ||
          (privateConversationId && privateConversationId !== result.private_conversation_id) || !Array.isArray(result.items)) refuse('INVALID_PRIVATE_HISTORY');
      const messages = result.items.map(item => {
        if (!['user', 'assistant'].includes(item.role) || typeof item.content !== 'string') refuse('INVALID_PRIVATE_HISTORY');
        return { role: item.role, content: item.content, status: item.status, failed: item.failed === true, job_id: item.job_id };
      });
      if (result.job_id != null && (typeof result.job_id !== 'string' || !result.job_id)) refuse('INVALID_PRIVATE_HISTORY');
      state.conversationId = result.private_conversation_id; state.messages = messages;
      privateHandle = result.private_conversation_id;
      state.following = true;
      uncertainRequestId = null;
      state.jobId = result.job_id || null; state.jobStatus = result.job_status || (state.jobId ? 'running' : null);
      state.pendingJobs = (result.pending_jobs || []).slice(1);
      state.historyRequired = false; state.uncertain = false; state.notice = 'PRIVATE_RECOVERED'; emit();
      return { route: 'private', recovered: true };
    } catch (error) {
      if (ticket !== epoch || destroyed) return;
      if (lockAuthorization(error, ticket)) return { route: 'blocked', code: state.notice };
      state.busy = false; state.following = false;
      // Failed history (including 404) cannot confirm absence or release an uncertain start.
      state.failureCode = error?.code === 'PRIVATE_NOT_FOUND' ? 'HTTP_404' : error?.httpStatus ? 'HTTP_' + error.httpStatus : error?.code === 'PRIVATE_TRANSPORT_UNCERTAIN' ? 'NETWORK_OR_TIMEOUT' : 'INVALID_RESPONSE';
      state.notice = 'PRIVATE_HISTORY_UNAVAILABLE';
      emit();
      return { route: 'blocked' };
    } finally { if (ticket === epoch && !destroyed) { state.checking = false; state.busy = !!state.jobId && state.following && ['queued','running'].includes(state.jobStatus); emit(); } }
  }
  async function restoreCurrent() {
    if (state.checking || ((state.jobId || state.uncertain) && state.mode !== 'private-locked')) return;
    restoreUnverified = true;
    const ticket = epoch;
    try {
      // Context is authoritative even when capability is neutral or unavailable.
      // This read carries no prompt, starts no work and grants no send permit.
      const decision = await classify('', [], 'restore');
      if (state.checking || ((state.jobId || state.uncertain) && state.mode !== 'private-locked')) return;
      if (decision.route === 'private') { state.available = true; return recover(privateHandle); }
      if (decision.route !== 'public') return safeNotice('PRIVATE_UNAVAILABLE');
      return { route: 'public' };
    } catch (error) {
      if (ticket !== epoch || destroyed) return;
      if (lockAuthorization(error, ticket)) return { route: 'blocked', code: state.notice };
      return routeFailure();
    }
  }
  async function recheckDraft(message) {
    if (typeof message !== 'string' || !message.trim()) return;
    const ticket = epoch;
    try {
      const decision = await classify(message);
      if (decision.route === 'private') { state.privacy = true; state.mode = 'private'; state.notice = ''; emit(); }
      else if (decision.route !== 'public') return safeNotice('PRIVATE_UNAVAILABLE');
      return { route: decision.route };
    } catch (error) {
      if (ticket !== epoch || destroyed) return;
      if (lockAuthorization(error, ticket)) return { route: 'blocked', code: state.notice };
      return routeFailure();
    }
  }
  async function beforeAttachment(message = '') {
    // No filenames, bytes, extraction, file input processing or public store access here.
    // Caller retains File objects in RAM until this explicit local decision.
    if (state.checking || state.jobId || state.uncertain) return safeNotice('PRIVATE_WORK_PENDING_RECOVER_FIRST');
    if (state.privacy) return safeNotice('PRIVATE_ATTACHMENTS_NOT_IN_REVIEWED_CONTRACT');
    if (typeof message !== 'string') refuse('INVALID_MESSAGE');
    const ticket = epoch;
    try {
      const result = await classify(message, null, 'attachment');
      if (result.route === 'private') { state.privacy = true; state.mode = 'private'; }
      if (result.route === 'public') return { route: 'public', epoch, publicViewId: result.publicViewId };
      return safeNotice('PRIVATE_ATTACHMENTS_NOT_IN_REVIEWED_CONTRACT');
    } catch (error) {
      if (ticket !== epoch || destroyed) return;
      if (lockAuthorization(error, ticket)) return { route: 'blocked', code: state.notice };
      return routeFailure();
    }
  }
  function allowPublicExport() { return !restoreUnverified && !state.reauthenticate && !state.privacy && !state.busy && !state.uncertain; }
  function stopFollowing() {
    if (!state.privacy) return { handled: false };
    // Abort only this UI observer; there is no backend cancellation contract.
    epoch++; abort.abort(); abort = new AbortController();
    state.following = false; state.busy = false; state.checking = false; state.notice = 'PRIVATE_FOLLOWING_STOPPED_JOB_PRESERVED'; emit();
    return { handled: true, cancelled: false, jobPreserved: true };
  }
  function allowPublicEdit() { return !restoreUnverified && !state.reauthenticate && !state.privacy && !state.busy && !state.uncertain; }
  function isCurrentPublicPermit(permit) { return !destroyed && permit?.route === 'public' && permit.epoch === epoch && !restoreUnverified && !state.reauthenticate && !state.privacy && (!getConversationId || permit.publicViewId === getConversationId()); }
  function destroy() { logout(); destroyed = true; abort.abort(); }
  return { submit, poll, recover, refresh, identityChanged, logout, newConversation,
    denyCurrentAccess: error => lockAuthorization(error, epoch),
    beforeAttachment, restoreCurrent, recheckDraft, allowPublicExport, allowPublicEdit, stopFollowing, isCurrentPublicPermit, snapshot, destroy };
}

// Bundled source: private_api.mjs
/* Scoped JEV/Office HTTP adapter. All content routes remain on the authenticated app origin. */
export class PrivateAuthorizationDenied extends Error {
  constructor(reason = 'private') {
    super('PRIVATE_AUTHORIZATION_DENIED');
    this.name = 'PrivateAuthorizationDenied'; this.code = 'PRIVATE_AUTHORIZATION_DENIED'; this.reason = reason;
  }
}

export function createOwnerChatApi({ request, getConversationId, preflightTransport = null, requestTimeout = 15000 }) {
  const validUuid = value => typeof value === 'string' && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(value);
  const reject = () => { throw Error('PRIVATE_REQUEST_REFUSED'); };
  let generation = 0, scope = null, proofDecisionRevision = 0;
  const viewId = () => { const id=getConversationId?.(); if(typeof id!=='string'||!/^[A-Za-z0-9_-]{1,128}$/.test(id))reject();return id; };
  async function timed(action, signal) {
    const controller = new AbortController();
    if(signal?.aborted)throw Object.assign(Error('PRIVATE_TRANSPORT_UNCERTAIN'),{code:'PRIVATE_TRANSPORT_UNCERTAIN'});
    let timer,rejectAbort;
    const interrupted=new Promise((_,reject)=>{rejectAbort=reject;});
    const abort = () => {clearTimeout(timer);controller.abort();rejectAbort(Object.assign(Error('PRIVATE_TRANSPORT_UNCERTAIN'),{code:'PRIVATE_TRANSPORT_UNCERTAIN'}));};
    signal?.addEventListener('abort',abort,{once:true});
    try {
      return await Promise.race([interrupted,action(controller.signal),new Promise((_,reject)=>{
        timer=setTimeout(()=>{controller.abort();reject(Object.assign(Error('PRIVATE_TRANSPORT_UNCERTAIN'),{code:'PRIVATE_TRANSPORT_UNCERTAIN'}));},requestTimeout);
      })]);
    } finally { clearTimeout(timer);signal?.removeEventListener('abort',abort); }
  }
  async function post(path, body, { signal } = {}, routing = false) {
    return timed(async signal => {
    const epoch=generation,view=body.conversation_id, observedProof=proofDecisionRevision;
    // A renewed session in another tab can obsolete the server's earlier denial.
    // Keep denying the old operation; only a current signal may invite Apple.
    const proofDenied = () => new PrivateAuthorizationDenied(observedProof === proofDecisionRevision ? 'owner-proof' : 'private');
    let response;
    try { response = await request(path,{method:'POST',signal,headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}); }
    catch (_) { throw Object.assign(Error('PRIVATE_TRANSPORT_UNCERTAIN'),{code:'PRIVATE_TRANSPORT_UNCERTAIN'}); }
    // Check request identity before acting on denial from an obsolete response.
    if(epoch!==generation||view!==viewId())reject();
    if (response.status === 401) throw new PrivateAuthorizationDenied('session');
    if (response.status === 403) {
      let denial;
      try { denial = await response.json(); } catch { /* An unreadable denial grants nothing. */ }
      if (epoch !== generation || view !== viewId()) reject();
      if (denial?.bloqueado === true || denial?.status === 'blocked') throw new PrivateAuthorizationDenied('session');
      if (routing ? denial?.route === 'reauthenticate' : denial?.error === 'owner_apple_required') {
        throw proofDenied();
      }
      throw new PrivateAuthorizationDenied();
    }
    if(response.status===404)throw Object.assign(Error('PRIVATE_NOT_FOUND'),{code:'PRIVATE_NOT_FOUND'});
    if(!response.ok)throw Object.assign(Error('PRIVATE_HTTP_REFUSED'),{code:'PRIVATE_HTTP_REFUSED',httpStatus:response.status});
    const result=await response.json();
    if(epoch!==generation||view!==viewId())reject();
    if (routing ? result?.route === 'reauthenticate' : result?.error === 'owner_apple_required') {
      throw proofDenied();
    }
    if(result?.route==='reauthenticate'||result?.authorized===false||result?.not_authorized===true||
       ['owner_apple_required','not_authorized','unauthorized','owner_private_required','private_access_denied'].includes(result?.error)) {
      throw new PrivateAuthorizationDenied();
    }
    if(routing && result && ['public','private','reauthenticate','unavailable'].includes(result.route))return result;
    if(!result||result.error)reject();
    return result;
    }, signal);
  }
  function privateScope(handle = scope?.private_handle) {
    const id=viewId();if(!validUuid(handle)||!scope||scope.conversation_id!==id||scope.private_handle!==handle)reject();
    return {conversation_id:id,private_handle:handle};
  }
  return {
    resetIdentity() {generation++;scope=null;},
    async capability({signal}={}) {
      return timed(async signal => {
      const epoch=generation;
      const response=await request('/api/owner-office/capability',{signal});
      if(epoch!==generation)reject();
      if(response.status===401||response.status===403)throw new PrivateAuthorizationDenied('session');
      if(!response.ok)reject();
      const result=await response.json();
      if(epoch!==generation)reject();
      if (result?.available === true || result?.reauthenticate !== true) proofDecisionRevision++;
      return {available:result?.available===true,reauthenticate:result?.reauthenticate===true};
      },signal);
    },
    async preflight(body, options={}) {
      let result;
      if(preflightTransport)result=await preflightTransport(body,options);
      else if(options.intent==='restore')result=await post('/api/owner-chat/context',{conversation_id:body.conversation_id},options,true);
      else result=await post('/api/owner-chat/preflight',body,options,true);
      if(result.route==='public' && (result.domain!=='public'||result.context_profile!=='existing_public'))reject();
      if(result.route==='private' && (result.domain!=='office_private'||result.context_profile!=='office_minimal'))reject();
      if(result.route==='private') {
        if(!validUuid(result.private_handle)||body.conversation_id!==viewId())reject();
        scope={conversation_id:body.conversation_id,private_handle:result.private_handle};
      }
      return result;
    },
    async start(input, options) {
      if(!validUuid(input.request_id)||typeof input.message!=='string'||!input.message.trim()||[...input.message].length>12000)reject();
      const target=privateScope(input.private_handle);
      const result=await post('/api/owner-chat/start',{...target,request_id:input.request_id,query:input.message},options);
      if(result.job_id!==input.request_id||result.private_conversation_id!==target.private_handle)reject();
      return result;
    },
    async get(args,options) {
      if(!validUuid(args.job_id))reject();
      const result=await post('/api/owner-chat/get',{...privateScope(),job_id:args.job_id},options);
      if(result.job_id!==args.job_id)reject();return result;
    },
    async exportDocument(args,options) {
      const target=privateScope();
      if (!validUuid(args?.job_id) || !['txt','md','pdf','docx'].includes(args?.format)) reject();
      return post('/api/owner-chat/export',{...target,job_id:args.job_id,format:args.format},options);
    },
    async history(args,options) {
      const target=privateScope(args.private_conversation_id||undefined);
      const result=await post('/api/owner-chat/history',target,options);
      if(!Array.isArray(result.items))reject();
      const items=[],pendingJobs=[];let jobId=null,jobStatus=null;
      for(const record of result.items) {
        if(!validUuid(record.id)||typeof record.query!=='string'||!['queued','running','completed','failed','interrupted','cancelled','expired'].includes(record.status))reject();
        items.push({role:'user',content:record.query});
        if(record.status==='queued'||record.status==='running'){pendingJobs.push({id:record.id,status:record.status});if(!jobId){jobId=record.id;jobStatus=record.status;}}
        else items.push(privateTerminalMessage(record));
      }
      if(args.uncertain_request_id&&!result.items.some(record=>record.id===args.uncertain_request_id))reject();
      return {private_conversation_id:target.private_handle,items,job_id:jobId,job_status:jobStatus,pending_jobs:pendingJobs};
    },
  };
}

// Bundled source: owner_main_view.mjs
/* Candidate same-canvas view. No dialog, case picker, public message object or persistence. */

const NOTICES = {
  REAUTHENTICATE: 'Revalide sua identidade Apple para consultar o Escritório.',
  SESSION_UNAVAILABLE: 'Não foi possível continuar com esta sessão.',
  PRIVATE_UNAVAILABLE: 'A consulta privada está indisponível. Sua mensagem não foi enviada ao chat público.',
  LOCAL_PREFLIGHT_REFUSED: 'Não foi possível verificar a rota local. Sua mensagem não foi enviada.',
  PRIVATE_RUNNING: '',
  PRIVATE_JOB_NOT_FOUND: 'O pedido não foi localizado. Nenhum reenvio foi feito.',
  PRIVATE_CANCELLED: 'A consulta terminou cancelada. Nenhum reenvio foi feito.',
  PRIVATE_EXPIRED: 'A consulta expirou. Nenhum reenvio foi feito.',
  PRIVATE_COMPLETED: '',
  PRIVATE_FAILED: 'A consulta não concluiu. Nenhum reenvio foi feito.',
  PRIVATE_INTERRUPTED: 'A consulta foi interrompida. Nenhum reenvio foi feito.',
  PRIVATE_RECOVERED: '',
  PRIVATE_HISTORY_UNAVAILABLE: 'Não foi possível recuperar a conversa privada. Recupere o histórico antes de enviar outra mensagem.',
  PRIVATE_HISTORY_RECOVERY_REQUIRED: 'Recupere o histórico privado antes de enviar outra mensagem. Nenhum pedido foi reenviado.',
  PRIVATE_RECEIPT_UNCERTAIN_RECOVER_NO_RESEND: 'O recebimento ainda não foi confirmado. Recupere a conversa antes de enviar outra mensagem.',
  PRIVATE_STATUS_UNAVAILABLE_RECOVER_NO_RESEND: 'Não foi possível acompanhar a consulta. O pedido permanece no Escritório.',
  PRIVATE_WORK_PENDING_RECOVER_FIRST: 'Há um pedido privado pendente. Aguarde ou recupere a conversa.',
  PRIVATE_ATTACHMENTS_NOT_IN_REVIEWED_CONTRACT: 'Anexos privados ainda não estão disponíveis nesta integração.',
  ATTACHMENT_ROUTE_CONTRACT_PENDING: 'O encaminhamento de anexos aguarda a revisão do contrato local.',
  PRIVATE_FOLLOWING_STOPPED_JOB_PRESERVED: 'Acompanhamento interrompido nesta tela. O pedido permanece no Escritório; nenhuma ordem pendente foi apagada ou cancelada.',
  PRIVATE_MESSAGE_TOO_LONG: 'A consulta privada aceita até 12.000 caracteres. Reduza a mensagem para continuar.',
};

export function mountOwnerMainChat({ api, root = document, onBusy = () => {}, uuid, getConversationId,
  schedule = setTimeout, cancel = clearTimeout, onPrivateClear = () => {}, reauthenticate,
  renderPrivateMarkdown, createPrivateWait, onExport, onContentChanged }) {
  const publicCanvas = root.querySelector('#conversa-interna');
  if (!publicCanvas) throw Error('MAIN_CANVAS_REQUIRED');
  const host = root.createElement('section'); host.hidden = true;
  host.dataset.ownerPrivateCanvas = '1'; host.className = 'conversa-interna owner-main-private';
  host.setAttribute('aria-label', 'Conversa privada do Escritório');
  const log = root.createElement('div'); log.setAttribute('role', 'log'); log.setAttribute('aria-live', 'polite');
  const notice = root.createElement('p'); notice.setAttribute('role', 'status');
  host.append(log, notice); publicCanvas.insertAdjacentElement('afterend', host);
  const header = root.createElement('div'); header.hidden = true; header.className = 'cab-estado owner-local-domain';
  header.textContent = 'JEV · Escritório privado';
  header.title = 'Consulta privada do titular; análise pelo MiMo autorizado, com ferramentas de leitura no servidor.';
  root.querySelector('#cab-estado')?.insertAdjacentElement('afterend', header);
  const status = root.createElement('p'); status.setAttribute('role', 'status');
  status.className = 'owner-main-route-status'; publicCanvas.insertAdjacentElement('afterend', status);
  const style = root.createElement('style');
  style.textContent = `.owner-main-private{font-size:14px;overflow-wrap:anywhere}
    .owner-main-private [role="log"]{display:flex;flex-direction:column;gap:18px}
    .owner-main-private .owner-plain-text{white-space:pre-wrap}
    .owner-main-route-status{font-size:13px}
    .owner-main-private[hidden],.owner-main-route-status[hidden],.owner-main-private [hidden]{display:none}`;
  style.textContent += `:root[data-owner-private-active="1"] #cab-estado,:root[data-owner-private-active="1"] #dica-janela,:root[data-owner-private-active="1"] #medidor{display:none!important}
    .owner-local-domain[hidden]{display:none}`;
  root.head.append(style);
  let timer = null, wasPrivate = false, disposed = false;
  let renderedConversation = null, noticeKey = null, waiting = null;
  const rows = [];
  let actionEpoch = 0, actionAbort = new AbortController(), exportHandler = onExport;
  function invalidateActions() {
    actionEpoch++; actionAbort.abort(); actionAbort = new AbortController();
  }
  function actionContext(message, row) {
    const ticket = actionEpoch, state = controller.snapshot(), conversationId = state.conversationId;
    const isCurrent = () => {
      const now = controller.snapshot();
      return !disposed && ticket === actionEpoch && row.isConnected && rows.some(item => item.row === row)
        && now.privacy && now.available && !now.reauthenticate && now.mode !== 'private-locked'
        && !now.checking && !now.historyRequired && !now.uncertain && now.conversationId === conversationId;
    };
    return { conversationId, signal: actionAbort.signal, isCurrent };
  }
  async function copyPrivateText(text, context) {
    if (!context.isCurrent()) return false;
    try { await root.defaultView.navigator.clipboard.writeText(text); return context.isCurrent(); }
    catch {
      if (!context.isCurrent()) return false;
      // Synchronous fallback only during this human action. No persistent buffer.
      const previous = root.activeElement, selection = root.defaultView?.getSelection?.();
      const ranges = selection ? Array.from({length: selection.rangeCount}, (_, i) => selection.getRangeAt(i).cloneRange()) : [];
      const inputSelection = previous && typeof previous.selectionStart === 'number'
        ? [previous.selectionStart, previous.selectionEnd, previous.selectionDirection] : null;
      const area = root.createElement('textarea'); area.value = text; area.readOnly = true;
      area.style.cssText = 'position:fixed;left:-9999px;top:0'; root.body.append(area);
      try { area.select(); return root.execCommand('copy') === true; }
      finally {
        area.remove();
        if (context.isCurrent()) {
          previous?.focus?.({preventScroll:true});
          if (inputSelection) previous.setSelectionRange(...inputSelection);
          if (selection) { selection.removeAllRanges(); for (const range of ranges) selection.addRange(range); }
        }
      }
    }
  }
  function appendActions(row, body, message) {
    if (message.role !== 'assistant' || message.status !== 'completed' || message.failed) return;
    const actions = root.createElement('div'); actions.className = 'msg-acoes';
    const feedback = root.createElement('span'); feedback.setAttribute('role', 'status');
    const copy = root.createElement('button'); copy.type = 'button'; copy.className = 'btn-acao';
    copy.textContent = 'Copiar'; copy.dataset.ownerAction = 'copy';
    copy.onclick = async () => {
      const context = actionContext(message, row); if (!context.isCurrent()) return;
      try {
        const ok = await copyPrivateText(message.content, context);
        if (context.isCurrent()) feedback.textContent = ok ? 'Copiado' : 'Não foi possível copiar.';
      } catch { if (context.isCurrent()) feedback.textContent = 'Não foi possível copiar.'; }
    };
    actions.append(copy);
    if (typeof exportHandler === 'function' && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(message.job_id || '')) {
      const button = root.createElement('button'); button.type = 'button'; button.className = 'btn-acao';
      button.textContent = 'Exportar'; button.dataset.ownerAction = 'export';
      button.onclick = async () => {
        const context = actionContext(message, row); if (!context.isCurrent() || button.disabled) return;
        button.disabled = true;
        try { await exportHandler(Object.freeze({...message}), context); }
        catch { if (context.isCurrent()) feedback.textContent = 'Não foi possível exportar a resposta privada.'; }
        finally { if (!disposed && row.isConnected && rows.some(item => item.row === row)) button.disabled = false; }
      };
      actions.append(button);
    }
    actions.append(feedback); body.append(actions);
  }
  const stopTimer = () => { if (timer !== null) cancel(timer); timer = null; };
  function clearRows() {
    invalidateActions();
    for (const item of rows) item.row.remove();
    rows.length = 0;
    waiting?.stop(); waiting = null;
  }
  function render(state) {
    stopTimer();
    if (state.mode === 'private-locked' || !state.available || state.reauthenticate) invalidateActions();
    if (state.mode === 'private-locked') onPrivateClear();
    host.hidden = !state.privacy; publicCanvas.hidden = state.privacy;
    header.hidden = !state.privacy;
    if (root.documentElement) {
      if (state.privacy) root.documentElement.dataset.ownerPrivateActive = '1';
      else delete root.documentElement.dataset.ownerPrivateActive;
    }
    status.hidden = state.privacy || !state.notice;
    const nextNotice = JSON.stringify([state.notice, state.failureCode, state.reauthenticate, state.privacy,
      state.checking, state.historyRequired, state.uncertain, state.following, state.jobId]);
    if (noticeKey !== nextNotice) {
    noticeKey = nextNotice;
    status.textContent = NOTICES[state.notice] || '';
    notice.textContent = (NOTICES[state.notice] || '') + (state.failureCode ? ' [' + state.failureCode + ']' : '');
    notice.hidden = !notice.textContent;
    if (state.reauthenticate && reauthenticate) {
      const login = root.createElement('button'); login.type = 'button'; login.textContent = 'Revalidar Apple';
      const view = getConversationId?.();
      login.onclick = () => { if (controller.snapshot().reauthenticate && view === getConversationId?.()) reauthenticate(); };
      (state.privacy ? notice : status).append(login);
    }
    if (state.privacy && !state.reauthenticate && !state.checking && (state.historyRequired || state.uncertain || (!state.following && state.jobId) || state.notice === 'PRIVATE_HISTORY_UNAVAILABLE')) {
      const resume = root.createElement('button'); resume.type = 'button'; resume.textContent = 'Retomar acompanhamento';
      resume.onclick = () => controller.recover(); notice.append(resume);
      notice.hidden = false;
    }
    }
    if (wasPrivate && !state.privacy) onPrivateClear();
    wasPrivate = state.privacy;
    const conversation = state.privacy ? state.conversationId || getConversationId?.() || '' : null;
    if (conversation !== renderedConversation || !state.privacy) {
      clearRows(); renderedConversation = conversation;
    }
    const scroll = root.querySelector('#conversa');
    const followBottom = scroll && scroll.scrollHeight - scroll.clientHeight - scroll.scrollTop < 48;
    const selected = root.defaultView?.getSelection?.();
    const preserveSelection = selected && !selected.isCollapsed;
    let changed = false;
    for (let index = 0; index < state.messages.length; index++) {
      const message = state.messages[index];
      const signature = JSON.stringify([message.role, message.content, message.failed === true, message.status, message.job_id]);
      if (rows[index]?.signature === signature) continue;
      changed = true;
      const previous = rows[index];
      const row = root.createElement('div'); row.className = 'msg ' + (message.role === 'user' ? 'msg-user' : 'msg-ai');
      row.dataset.role = message.role; row.dataset.papel = message.role === 'user' ? 'user' : 'ai';
      // Use only the injected private-safe renderer. Never pass private text to the public path.
      const body = root.createElement('div'); body.className = 'msg-corpo';
      const content = root.createElement('div'); content.className = 'conteudo';
      if (message.failed) {
        row.dataset.aviso = 'private-terminal';
        const title = root.createElement('strong'); title.textContent = 'Consulta não concluída';
        body.append(title);
      }
      if (message.role !== 'user' && renderPrivateMarkdown) {
        try { content.append(renderPrivateMarkdown(message.content)); }
        catch { content.classList.add('owner-plain-text'); content.textContent = message.content; }
      } else { content.classList.add('owner-plain-text'); content.textContent = message.content; }
      body.append(content); appendActions(row, body, message); row.append(body);
      if (previous) previous.row.replaceWith(row);
      else if (waiting) log.insertBefore(row, waiting.node);
      else log.append(row);
      rows[index] = { row, signature };
    }
    while (rows.length > state.messages.length) { rows.pop().row.remove(); changed = true; }
    const showWait = state.busy && state.jobId && state.following && state.privacy;
    if (showWait && !waiting) {
      if (createPrivateWait) waiting = createPrivateWait();
      else {
        const node = root.createElement('div'); node.className = 'beta-wait';
        node.setAttribute('role', 'status'); node.setAttribute('aria-label', 'Consulta privada em andamento');
        const orbit = root.createElement('span'); orbit.className = 'beta-wait__orbit';
        const icon = root.createElement('span'); icon.className = 'beta-wait__icon'; icon.textContent = 'β';
        icon.setAttribute('aria-hidden', 'true'); orbit.append(icon); node.append(orbit);
        waiting = { node, stop: () => node.remove() };
      }
      log.append(waiting.node); changed = true;
    } else if (!showWait && waiting) {
      waiting.stop(); waiting = null; changed = true;
    }
    if (changed && !preserveSelection) {
      if (onContentChanged) onContentChanged();
      else if (followBottom) scroll.scrollTop = scroll.scrollHeight;
    }
    onBusy(state.busy, state.privacy, state);
    if (state.jobId && state.following && state.mode !== 'private-locked') timer = schedule(async () => {
      timer = null; await controller.poll();
      if (!disposed && controller.snapshot().following && controller.snapshot().jobId && controller.snapshot().mode !== 'private-locked' && timer === null) timer = schedule(tick, 2000);
    }, 2000);
  }
  async function tick() {
    timer = null; if (disposed) return; await controller.poll();
    if (!disposed && controller.snapshot().following && controller.snapshot().jobId && controller.snapshot().mode !== 'private-locked' && timer === null) timer = schedule(tick, 2000);
  }
  const controller = createPrivateChatController({ api, uuid, getConversationId, onState: render });
  const visible = () => { if (!root.hidden && !disposed) controller.refresh(); };
  const page = () => { if (!disposed) controller.refresh(); };
  root.addEventListener('visibilitychange', visible);
  root.defaultView?.addEventListener('pageshow', page);
  root.defaultView?.addEventListener('focus', page);
  root.defaultView?.addEventListener('pagehide', invalidateActions);
  // Mount can precede login; explicit onLogin is required even when the token is unchanged.
  controller.refresh();
  return { controller, setExportHandler(handler) {
      invalidateActions(); exportHandler = typeof handler === 'function' ? handler : undefined;
      for (const item of rows) item.signature = null;
      render(controller.snapshot());
    }, onLogin: () => { onPrivateClear(); return controller.identityChanged(); },
    revalidate: () => { if (controller.snapshot().reauthenticate) return reauthenticate?.(); },
    reset: () => { onPrivateClear(); controller.logout(); },
    newConversation: () => { onPrivateClear(); controller.newConversation(); }, refresh: () => controller.refresh(),
    destroy() {
      disposed = true; stopTimer(); controller.destroy(); clearRows();
      root.removeEventListener('visibilitychange', visible);
      root.defaultView?.removeEventListener('pageshow', page);
      root.defaultView?.removeEventListener('focus', page);
      root.defaultView?.removeEventListener('pagehide', invalidateActions);
      host.remove(); status.remove(); style.remove(); header.remove();
    } };
}

// Bundled source: owner_office_entry.mjs
/* App entry. JEV preflight transport is installed only after the parent pins its reviewed recap. */

export const OWNER_ROUTER_CONTRACT_READY = true; // Contract wired; backend acceptance/install remain parent gates.

export function mountOwnerOffice({ request, root = document, reauthenticate, getConversationId,
  onBusy, onPrivateClear, readDraft, writeDraft, preflightTransport = null, renderPrivateMarkdown, createPrivateWait, onExport, onContentChanged }) {
  const api = createOwnerChatApi({ request, getConversationId, preflightTransport });
  let documentExporter = null;
  const view = mountOwnerMainChat({ api, root, reauthenticate, getConversationId,
    onBusy: (busy, privacy, state) => { documentExporter?.sync(state); onBusy?.(busy, privacy, state); }, onPrivateClear,
    renderPrivateMarkdown, createPrivateWait, onExport, onContentChanged });
  documentExporter = createPrivateDocumentExporter({api, root, getState: () => view.controller.snapshot(),
    onDenied: error => view.controller.denyCurrentAccess(error)});
  if (!onExport) view.setExportHandler((message, context) => documentExporter.open(message, context));
  let heldDraft = null, loginGeneration = 0;
  return { ...view,
    beforeAuthentication() {
      loginGeneration++;
      heldDraft = view.controller.snapshot().reauthenticate ? {view: getConversationId?.(), text: readDraft?.()} : null;
      view.reset();
    },
    reset() { loginGeneration++; heldDraft = null; view.reset(); },
    newConversation() { loginGeneration++; heldDraft = null; view.newConversation(); },
    beforeText: args => view.controller.submit(args),
    beforeAttachment: message => view.controller.beforeAttachment(message),
    restoreCurrent: () => view.controller.restoreCurrent(),
    async refresh() {
      await view.controller.refresh();
      const state = view.controller.snapshot();
      if (state.privacy && state.available && !state.checking && state.following && state.mode !== 'private-locked') {
        return view.controller.recover(state.conversationId || undefined);
      }
    },
    async onLogin() {
      const generation = ++loginGeneration, draft = heldDraft; heldDraft = null;
      await view.onLogin();
      if (generation !== loginGeneration) return;
      if (draft?.text && draft.view === getConversationId?.() && view.controller.snapshot().available) {
        const decision = await view.controller.recheckDraft(draft.text);
        if (decision?.route === 'private' && generation === loginGeneration && draft.view === getConversationId?.()) writeDraft?.(draft.text);
        return decision; // Only preflight, never replay a submitted operation.
      }
      return view.controller.restoreCurrent();
    },
  };
}

// Explicit owner download only. Never invokes public export, artifact URLs or a model.
export function createPrivateDocumentExporter({ api, getState, onDenied, root = document, capacitor = globalThis.Capacitor }) {
  const types = { txt: 'text/plain', md: 'text/markdown', pdf: 'application/pdf',
    docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' };
  let epoch = 0, sheet = null, prepared = null, cachePath = null, sharing = false, contextCleanup = null, requestAbort = null, cleanupNotice = null;
  const pendingCleanup = new Set(), writing = new Set(), deleting = new Map();
  const fs = capacitor?.Plugins?.Filesystem, share = capacitor?.Plugins?.Share;
  const native = capacitor?.isNativePlatform?.() === true;
  if (!root.getElementById('owner-private-export-style')) {
    const style = root.createElement('style'); style.id = 'owner-private-export-style';
    style.textContent = `.owner-private-export{position:fixed;inset:0;z-index:10000;background:#0006;display:grid;place-items:center;padding:20px;font-size:14px}.owner-private-export-panel{width:min(100%,420px);max-height:80dvh;overflow:auto;background:var(--bg-elevado,#fff);color:var(--txt,#182536);padding:24px;border-radius:22px;box-shadow:0 16px 60px #0003;display:flex;flex-direction:column;gap:16px}.owner-private-export-panel h3,.owner-private-export-panel p{margin:0}.owner-private-export-formats{display:flex;flex-wrap:wrap;gap:10px}.owner-private-export button{min-height:44px;padding:9px 14px;border:1px solid var(--borda,#d9dee5);border-radius:14px;font:inherit;color:inherit;background:var(--bg-campo,#f3f5f8)}.owner-private-export [hidden]{display:none!important}`;
    root.head.append(style);
  }
  const hash = async bytes => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)), n => n.toString(16).padStart(2, '0')).join('');
  const uuid = value => typeof value === 'string' && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value);
  function valid(state, conversation, job) {
    return state?.privacy === true && state.available === true && !state.reauthenticate &&
      !state.checking && !state.historyRequired && !state.uncertain &&
      state.mode === 'private' && state.conversationId === conversation &&
      state.messages.some(m => m.job_id === job && m.status === 'completed' && !m.failed);
  }
  function showCleanupNotice() {
    if (!pendingCleanup.size) { cleanupNotice?.remove(); cleanupNotice = null; return; }
    if (cleanupNotice) return;
    cleanupNotice = root.createElement('div');
    cleanupNotice.setAttribute('role', 'status');
    cleanupNotice.setAttribute('style', 'position:fixed;bottom:12px;left:12px;right:12px;z-index:10001;padding:14px;border-radius:14px;background:var(--bg-elevado,#fff);color:var(--txt,#182536);font-size:14px;box-shadow:0 2px 20px #0003');
    const text = root.createElement('p');
    text.textContent = 'Não foi possível limpar um arquivo temporário deste app.';
    const retry = root.createElement('button'); retry.type = 'button'; retry.textContent = 'Tentar limpar arquivo temporário';
    retry.onclick = async () => { retry.disabled = true; await reconcileCleanup(); retry.disabled = false; };
    cleanupNotice.append(text, retry); root.body.append(cleanupNotice);
  }
  async function erase(path) {
    if (!path || !pendingCleanup.has(path) || writing.has(path)) return;
    if (deleting.has(path)) return deleting.get(path);
    const pending = Promise.resolve().then(async () => {
      try {
        if (!fs?.deleteFile) throw new Error('CLEANUP_UNAVAILABLE');
        await fs.deleteFile({ path, directory: 'CACHE' });
        pendingCleanup.delete(path);
        if (!pendingCleanup.size) { cleanupNotice?.remove(); cleanupNotice = null; }
      } catch { showCleanupNotice(); }
      finally { deleting.delete(path); }
    });
    deleting.set(path, pending); return pending;
  }
  async function reconcileCleanup() {
    if (!sharing) await Promise.all([...pendingCleanup].map(erase));
  }
  function reset() {
    contextCleanup?.(); contextCleanup = null;
    requestAbort?.abort(); requestAbort = null;
    epoch++; prepared = null;
    if (sheet) { sheet.remove(); sheet = null; }
    const path = cachePath; cachePath = null;
    if (!sharing) void reconcileCleanup();
  }
  function sync(state) {
    if (prepared && !valid(state, prepared.conversation, prepared.job)) reset();
    if (sheet && !valid(state, sheet.dataset.conversation, sheet.dataset.job)) reset();
  }
  async function validate(data, message, format) {
    if (!data || data.schema !== 'owner-private-document/v1' || data.job_id !== message.job_id || data.format !== format ||
        data.mime !== types[format] || data.filename !== `IALD_Minuta_${message.job_id.slice(0, 8)}.${format}` ||
        !Number.isSafeInteger(data.bytes) || data.bytes < 1 || data.bytes > 8388608 ||
        typeof data.data_base64 !== 'string' || data.data_base64.length > 11184812 ||
        !/^[A-Za-z0-9+/]*={0,2}$/.test(data.data_base64) ||
        typeof data.sha256 !== 'string' || !/^[a-f0-9]{64}$/.test(data.sha256)) throw new Error('DOCUMENT_INVALID');
    const binary = atob(data.data_base64), bytes = Uint8Array.from(binary, c => c.charCodeAt(0));
    if (bytes.length !== data.bytes || await hash(bytes) !== data.sha256 ||
        await hash(new TextEncoder().encode(message.content)) !== data.source_sha256) throw new Error('DOCUMENT_CHANGED');
    return bytes;
  }
  function open(message, context = null) {
    const state = getState(), conversation = state?.conversationId;
    if (!uuid(message?.job_id) || !valid(state, conversation, message.job_id) ||
        (context && (context.signal?.aborted || !context.isCurrent()))) return false;
    reset(); const ticket = epoch;
    const actionAbort = new AbortController(); requestAbort = actionAbort;
    if (context?.signal) {
      context.signal.addEventListener('abort', reset, { once: true });
      contextCleanup = () => context.signal.removeEventListener('abort', reset);
    }
    const overlay = root.createElement('div'); sheet = overlay;
    overlay.dataset.conversation = conversation; overlay.dataset.job = message.job_id;
    overlay.className = 'owner-private-export'; overlay.setAttribute('role', 'dialog'); overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Salvar resposta');
    const panel = root.createElement('div'); panel.className = 'owner-private-export-panel';
    const title = root.createElement('h3'); title.textContent = 'Salvar resposta';
    const close = root.createElement('button'); close.type = 'button'; close.textContent = 'Fechar'; close.className = 'btn-quiet';
    close.onclick = reset;
    const status = root.createElement('p'); status.setAttribute('role', 'status'); status.textContent = 'Escolha o formato da minuta.';
    const actions = root.createElement('div'); actions.className = 'owner-private-export-formats';
    const save = root.createElement('button'); save.type = 'button'; save.className = 'btn-primario'; save.hidden = true;
    save.textContent = native ? 'Salvar ou compartilhar' : 'Baixar arquivo';
    panel.append(title, actions, status, save, close); overlay.append(panel); root.body.append(overlay);
    let busy = false;
    const current = () => ticket === epoch && valid(getState(), conversation, message.job_id) &&
      (!context || (!context.signal?.aborted && context.isCurrent()));
    for (const [format, label] of [['docx', 'Word'], ['pdf', 'PDF'], ['md', 'Markdown'], ['txt', 'Texto']]) {
      const button = root.createElement('button'); button.type = 'button'; button.className = 'btn-quiet'; button.textContent = label;
      actions.append(button);
      button.onclick = async () => {
        if (busy || !current()) return;
        busy = true; save.hidden = true; actions.querySelectorAll('button').forEach(b => b.disabled = true);
        status.textContent = 'Preparando arquivo…';
        let path = null;
        try {
          const oldPath = cachePath; cachePath = null; prepared = null; await erase(oldPath);
          if (!current()) return;
          const data = await api.exportDocument({ job_id: message.job_id, format }, { signal: actionAbort.signal });
          const bytes = await validate(data, message, format);
          if (!current()) return;
          let uri = null;
          if (native) {
            if (!fs?.writeFile || !share?.share) throw new Error('NATIVE_SAVE_UNAVAILABLE');
            path = `iald-private-exports/${crypto.randomUUID()}_${data.filename}`;
            pendingCleanup.add(path); writing.add(path);
            let file;
            try { file = await fs.writeFile({ path, directory: 'CACHE', data: data.data_base64, recursive: true }); }
            finally { writing.delete(path); }
            if (!current()) { await erase(path); return; }
            if (typeof file.uri !== 'string' || !file.uri.startsWith('file://')) { await erase(path); throw new Error('NATIVE_SAVE_INVALID'); }
            cachePath = path; uri = file.uri;
          }
          prepared = { conversation, job: message.job_id, bytes, mime: data.mime, filename: data.filename, uri, path };
          status.textContent = 'Arquivo pronto. Revise a minuta antes de utilizá-la.'; save.hidden = false;
        } catch (error) {
          if (current()) {
            status.textContent = 'Não foi possível preparar o arquivo. Tente novamente.';
            if (error?.code === 'PRIVATE_AUTHORIZATION_DENIED') onDenied?.(error);
          }
          if (path) await erase(path);
        } finally {
          busy = false; if (current()) actions.querySelectorAll('button').forEach(b => b.disabled = false);
        }
      };
    }
    save.onclick = async () => {
      if (busy || !prepared || !current()) return;
      const file = prepared; busy = true; save.disabled = true;
      try {
        // Revalidate immediately before the explicit transfer to the device/user.
        const capability = await api.capability({ signal: actionAbort.signal });
        if (!current()) return;
        if (!capability?.available) { onDenied?.(new PrivateAuthorizationDenied()); reset(); return; }
        if (native) {
          sharing = true;
          overlay.remove(); sheet = null; // No app modal can intercept the native share sheet.
          await share.share({ title: 'Minuta IALD', files: [file.uri], dialogTitle: 'Salvar minuta' });
        } else {
          const url = URL.createObjectURL(new Blob([file.bytes], { type: file.mime }));
          const link = root.createElement('a'); link.href = url; link.download = file.filename;
          root.body.append(link); link.click(); link.remove();
          setTimeout(() => URL.revokeObjectURL(url), 1500);
        }
        reset();
      } catch (error) {
        if (current() && error?.code === 'PRIVATE_AUTHORIZATION_DENIED') onDenied?.(error);
        if (current()) {
          prepared = null; save.hidden = true; save.disabled = false;
          if (!sheet) { root.body.append(overlay); sheet = overlay; }
          status.textContent = 'Salvamento não concluído. Escolha o formato novamente para tentar salvar.';
          close.focus();
        }
      } finally {
        sharing = false; await erase(file.path); if (cachePath === file.path) cachePath = null;
        if (native && !sheet) reset(); busy = false;
      }
    };
    overlay.addEventListener('keydown', event => {
      if (event.key === 'Escape') { event.preventDefault(); reset(); }
      if (event.key === 'Tab') {
        const controls = [...panel.querySelectorAll('button')].filter(b => !b.hidden && !b.disabled);
        const index = controls.indexOf(root.activeElement);
        if (event.shiftKey && index <= 0) { event.preventDefault(); controls.at(-1)?.focus(); }
        else if (!event.shiftKey && index === controls.length - 1) { event.preventDefault(); controls[0]?.focus(); }
      }
    });
    close.focus();
    return true;
  }
  return { open, sync, reset, validate, reconcileCleanup };
}
