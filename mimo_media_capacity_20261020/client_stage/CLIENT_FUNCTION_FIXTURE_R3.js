async function enviarTexto(texto, anexos) {
  if (respostaPendenteBackground()) return;
  if (!DEMO && !backgroundOwner) { recuperarRespostasBackground(); return; }
  const c = conversaAtiva();
  if (!c) return;

  const owner = backgroundOwner;
  const hasMedia = anexos.some(a => a.localDraftId) || c.mensagens.some(m => Array.isArray(m.content) && m.content.some(p => ['iald_media','iald_local_media'].includes(p?.type)));
  const midias = [];
  if (hasMedia) {
    if (!await mediaConsent(anexos, texto, c.id)) return false;
    await mediaPrepareLegacy(c, owner);
    for (const a of anexos) if (a.localDraftId) midias.push(await mediaUpload(a, owner, c.id));
    mediaScope(owner, c.id);
  }
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
  salvarConversas();
  if (hasMedia) await mediaMarkSubmitted(anexos, owner, c.id);
  listarConversas();
  atualizarTitulo();

  S.colarNoFim = true;
  desenharMensagem('user', conteudo);
  atualizarDica();

  transmitir(montarEnvio(c));
  return true;
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
  for (const m of recortar(c.mensagens, sys)) {
    const conteudo = m.content;
    if (Array.isArray(conteudo) && conteudo.some(p => p?.type === 'iald_local_media')) throw Error('Mídia local ainda não foi enviada com autorização; histórico preservado.');
    enviadas.push({ role: m.role === 'assistant' ? 'assistant' : 'user', content: conteudo });
  }
  return enviadas;
}