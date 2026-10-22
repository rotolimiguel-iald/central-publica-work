  } catch (error) {
    failure = error;
    if (currentTurn() && !error.detached) {
      avisarBackground(error.message || 'Resposta pendente. Retomaremos o mesmo pedido quando a conexão voltar.');
    }
  } finally {
    if (paintTimer !== null) clearTimeout(paintTimer);
    if (!currentTurn()) { corpo.parentElement.remove(); return; }
    streamFinished = doneReceived;
    tirarDigitando();
    congelarTrilha(trilha);
    const complete = doneReceived && !failure;
    texto = complete ? splitThinking(bruto, true).text : '';
    const limpo = complete ? aplicarPtbr(texto) : '';
    let answer = null, deliveryNotice = null;
    if (complete) {
      delete corpo.parentElement.dataset.backgroundPending;
      pintarAgora();
      if (aviso) {
        const linha = corpo.parentElement;
        deliveryNotice = retirada ? Object.assign({}, aviso, { retirar_resposta: true }) : aviso;
        pintarAviso(linha, conteudo, deliveryNotice, texto);
        if (origem.id === S.ativaId && aviso.tipo === 'consentimento_ia') {
          S.avisoConsentimento = linha;
          const f = folhaDoAviso(aviso);
          abrirConsentimento(f.texto, f.provedor, f.versao);
        } else if (origem.id === S.ativaId && aviso.tipo === 'limite') abrirCreditos(aviso);
      } else if (limpo) {
        answer = { role: 'assistant', content: limpo };
        if (modeloRespondente) answer.modelo = modeloRespondente;
        if (selo && /^[0-9a-f]{64}$/.test(selo.link)) {
          answer.selo = selo;
          if (bruto !== limpo) answer.bruto = bruto;
        }
        corpo.parentElement._bruto = limpo;
      } else {
        deliveryNotice = { tipo: 'falha_motor', texto: 'A resposta terminou sem conteúdo.' };
        pintarAviso(corpo.parentElement, conteudo, deliveryNotice, '');
      }
    } else {
      // Interrupted network delivery is never a normal answer, sealed or otherwise.
      bruto = ''; selo = null; pensamento = ''; texto = '';
      corpo.parentElement._bruto = '';
      deliveryNotice = failure?.terminal ? {
        tipo: failure.status === 'cancelled' ? 'resposta_interrompida' : 'falha_motor',
        texto: failure.message, retirar_resposta: true,
      } : null;
      pintarAviso(corpo.parentElement, conteudo, deliveryNotice || failure?.aviso || {
        tipo: 'em_andamento', retirar_resposta: true,
        texto: controller.signal.reason?.type === 'user_cancel'
          ? 'Pedido de parada registrado. A confirmação será recuperada do servidor.'
          : 'Resposta pendente. Você pode sair e voltar; o pedido não será enviado com outro identificador.',
      }, '');
    }
    try {
      if (DEMO && answer) {
        origem.mensagens.push(answer); salvarConversas();
      } else if (job && (complete || failure?.terminal)) {
        await salvarEntregaBackground(job, answer, deliveryNotice, complete ? 'completed' : failure.status);
      }
      if (currentTurn()) listarConversas();
    } catch (error) {
      if (currentTurn()) avisarBackground(error.message || 'Resposta aguardando confirmação de gravação.');
    }
    if (currentTurn()) {
      S.gerando = false; S.aborto = null; S.backgroundTurn = null;
      activeBackgroundJob = null;
      atualizarBotaoEnviar(); atualizarDica();
      if (!document.hidden && !document.querySelector('[data-folha][data-aberta="1"]')) $('#entrada').focus();
      if (!DEMO && !(aviso && aviso.tipo === 'limite')) setTimeout(() => { carregarMotor(); }, 1500);
      agendarRecuperacaoBackground();
    }
  }
