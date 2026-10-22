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
