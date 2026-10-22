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
function persistirConversasBackground() {
  if (!backgroundOwner) throw new PendingChatJobError('A conta precisa ser identificada antes de salvar.');
  mediaAssertHistory(S.conversas);
  const key = backgroundHistoryKey(backgroundOwner);
  const raw = JSON.stringify({ conversas: S.conversas, ativa: S.ativaId });
  try {
    localStorage.setItem(key, raw);
    if (localStorage.getItem(key) !== raw) throw new Error();
  } catch (_) { throw new PendingChatJobError('Não foi possível salvar a resposta neste aparelho. A entrega continua pendente.'); }
}
function salvarConversas() {
  try {
  if (!DEMO && backgroundOwner) { persistirConversasBackground(); return; }
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
function limitesDoPlano() {
  const l = S.motor && S.motor.limites;
  return (l && typeof l === 'object') ? l : null;
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
  const legacy = S.conversas.some(c => (c.mensagens || []).some(m => Array.isArray(m.content) && m.content.some(p =>
    (p?.type === 'input_audio' && typeof p.input_audio?.data === 'string' && p.input_audio.data.startsWith('data:audio/')) ||
    (p?.type === 'video_url' && typeof p.video_url?.url === 'string' && p.video_url.url.startsWith('data:video/')))));
  if (!legacy) return;
  await mediaAwaitBoundMotor(owner);
  const epoch = backgroundEpoch, scope = mediaStorageScope(), snapshot = JSON.stringify(S.conversas);
  const recovered = JSON.parse(snapshot);
  await mediaMigrateLegacy(recovered, owner);
  if (owner !== backgroundOwner || epoch !== backgroundEpoch || scope !== mediaStorageScope()) throw detached();
  if (snapshot !== JSON.stringify(S.conversas)) throw new PendingChatJobError('O histórico mudou durante a recuperação; as alterações foram preservadas e a recuperação será retomada.');
  S.conversas = recovered;
  persistirConversasBackground();
}