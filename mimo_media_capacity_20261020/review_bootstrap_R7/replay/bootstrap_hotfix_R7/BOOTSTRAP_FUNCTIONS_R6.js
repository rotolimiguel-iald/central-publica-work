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
    await carregarMotor();
    await mediaMigrateLegacy(S.conversas, account);
    persistirConversasBackground();
    if (!S.conversas.length) novaConversa({ semFoco: true });
    else { listarConversas(); abrirConversa(); }
  }
  if (await mediaMigrateLegacy(S.conversas, account)) persistirConversasBackground();
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
  if (!DEMO && backgroundOwner) { persistirConversasBackground(); return; }
  mediaAssertHistory(S.conversas);
  guardar(K.conversas, S.conversas);
  guardar(K.ativa, S.ativaId || '');
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