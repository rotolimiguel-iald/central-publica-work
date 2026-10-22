// Embedded into iald.js by build_client.py; this is not an extra served asset.
let backgroundOwner = '', backgroundEpoch = 0, backgroundRecovery = false;
let backgroundRecoveryAgain = false;
let backgroundTimer = null, backgroundNotice = '', activeBackgroundJob = null;
let backgroundNativeListening = false, backgroundNativeActive = null;
const backgroundHistoryKey = (owner) => 'iald_conversas_owner_v1:' + encodeURIComponent(owner);
const backgroundJobs = createDurableChatJobs({
  request: fetchIALD, storage: localStorage,
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
  const key = backgroundHistoryKey(backgroundOwner);
  const raw = JSON.stringify({ conversas: S.conversas, ativa: S.ativaId });
  try {
    localStorage.setItem(key, raw);
    if (localStorage.getItem(key) !== raw) throw new Error();
  } catch (_) { throw new PendingChatJobError('Não foi possível salvar a resposta neste aparelho. A entrega continua pendente.'); }
}
function desanexarRespostasBackground(sair = false) {
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
    const raw = localStorage.getItem(backgroundHistoryKey(account));
    let history;
    if (raw != null) {
      history = JSON.parse(raw);
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
    persistirConversasBackground();
    if (!S.conversas.length) novaConversa({ semFoco: true });
    else { listarConversas(); abrirConversa(); }
  }
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
    persistirConversasBackground(); // Mandatory verified history write before ack.
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
