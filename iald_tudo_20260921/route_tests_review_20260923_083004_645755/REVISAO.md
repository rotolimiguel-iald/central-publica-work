# Testes de rotas — staged, 23/09/2026

**Claude:128 passaram,2 falharam(exit1). Acesso nativo:62 passaram,0 falharam(exit0).** Os15casos novos Haiku passaram. Nenhum teste foi marcado xfail/skip nem removido para esconder a regressão.

## Achado real R1 — disponibilidade Sonnet incoerente(P2)

Sem SDK Anthropic e, separadamente, com memória atlas_integral, /api/motor informa indisponibilidade do modelo selecionado, mas a linha claude-sonnet em opcoes continua disponivel=true. _opcoes_de_motor anexa diretamente as linhas de CLAUDE_ROUTES.options; flags considera configuração, enquanto option_rows fixa true. O envio faz a verificação real e recusa corretamente, sem fallback nem geração. As duas asserções antigas, atualizadas apenas para o ID claude-sonnet, continuam falhando. Diagnóstico explícito em final_claude.log.

Correção sugerida ao pai: compor elegibilidade de conta com prontidão efetiva de SDK/memória na construção das opções e conferir a recusa na seleção. Não trocar a expectativa desses dois testes para true. Não foi alterado servidor.

## Razão de cada grupo de mudanças

1. Isolamento comum: REAIS agora contém somente fontes públicas; removida a leitura de .env/usuários/razões para hash. Importação passa por offline_bootstrap: fonte atual do servidor, AST com apenas _segredo substituído por configuração sintética, __file__ em runtimeW. Rede, SQLite e gravações externas bloqueados; engines opcionais com estado privado desabilitados. Fonte e lógica das rotas preservadas. Tokenizer usa somente cache local existente. Node é permitido apenas com --check.
2. Claude fixture: recriar RouteBridge depois de substituir CLAUDE_CFG. O bridge captura base_config no construtor; o mock antigo deixava referência à configuração anterior. enabled=True e budgets públicos None explícitos. Pacote mínimo é fixture sintética para política, não simulação de memória medida válida. SDK falso registra contagens e contrato max_retries=0.
3. IDs: seletor atual retorna claude-sonnet, mantendo motor/provedor claude. Alias claude continua testado para compatibilidade; novas escolhas explícitas exercitadas.
4. Erros: modelo inválido responde400/Modelo inválido; seleção Claude não autorizada responde409. Mantida exigência de nenhuma gravação ao negar. Não alteradas asserções de consentimento ou envio.
5. Opções: conta comum recebe opção OpenAI, não lista vazia; permanece sem acesso nativo/Claude. É a única expectativa funcional ajustada em test_acesso_nativa.py.
6. Registro Claude antigo/forjado: _motor_efetivo preserva seleção para recusa explícita, conforme comentário do fonte; deixou de cair automaticamente na OpenAI/nativa. Testes agora exigem ausência de qualquer envio e recusa visível, inclusive para caio listado mas não Luiz. Painel acompanha o motor gravado indisponível.
7. Quinze checagens novas: flag1/flag0; cliente antigo sem Haiku; sessão/Bearer com X-IALD-Context; escolha/contexto426; chat antigo recusado antes de count/send/reserva; consentimentos intactos; retorno Sonnet; quatro contas públicas não autorizadas mesmo com capability e sem budgets. Nenhuma geração Haiku testada.

Diff exato em test_claude_rotas.py.diff e test_acesso_nativa.py.diff. O cabeçalho histórico dos testes originais permanece como linhagem; este parecer descreve o escopo atual.

## Reprodução

Executar em processos separados, com o diretório deste pacote como cwd:

    C:\Python314\python.exe -B -X utf8 test_claude_rotas.py
    C:\Python314\python.exe -B -X utf8 test_acesso_nativa.py

Manter offline_bootstrap.py ao lado das cópias; não copiar isoladamente os testes para ROOT. PROJETO permanece fixado na fonte real C:\IALD\projetos_pyhton\IALD. Para ler dependências do perfil do operador foi necessária execução elevada nesta auditoria; nenhuma biblioteca foi instalada. Logs finais e receipt.json pinam fontes/resultados. Nenhuma chave, usuário ou razão real foi lido; nenhum arquivo ROOT, Selo, ferramenta, app ou memória foi editado.

As primeiras execuções diagnósticas registraram a fixture antiga e ajustes do próprio isolamento; não usar seus totais como resultado final. Conclusão restrita a rotas/política sob fixtures: não aprova produção, pacote Haiku real, inferência paga, Selo ou build21/20. As duas falhas reais permanecem pendentes para o pai.
