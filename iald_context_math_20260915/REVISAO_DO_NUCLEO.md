# Núcleo fixo da IALD — preparado em 15/09/2026

[INPUT] A ordem final do operador é manter o conteúdo como conhecimento fixo: lagrangiana, equação mestra, Hamiltoniano limitado inferiormente, operadores de Lindblad, sistema de fase e relações de comutação. A frase anterior «derive tudo do zero» foi expressamente retirada pelo operador. O núcleo também inclui Um absoluto, custo geométrico do zero absoluto e as pontes do framework.

[REAL — preparação local] O contexto preparado tem 324.037 tokens medidos pelo contador o200k_base. Desses, 314.799 pertencem aos sete documentos integrais, sem sumarização nem recorte. A janela proposta é de 400.000 tokens. Os valores são um retrato da preparação; os documentos serão relidos e identificados por hash a cada requisição.

Documentos integrais selecionados:

- Artigo «O Custo Geométrico do Zero Absoluto — Haja Luz», fonte publicada `paper_PT.tex`.
- Artigo «A Ponte Einstein–Cartan–Miguel», fonte publicada `.tex`.
- Artigo local em português gerado pelo `um.py`, `um_grande_atrator_pt.txt`.
- Forma canônica matemática local, `um_grande_atrator_forma_canonica.md`.
- Selo local `um_grande_atrator_selo.json`.
- `README.md` do repositório público `the_boundary`.
- `read-brief.md` do mesmo repositório, que localiza os conceitos e as fontes.

Os textos publicados e os artefatos locais têm versões próprias. Nenhum é promovido a prova nova por ser incluído no contexto. O índice vivo recente é acrescentado ao núcleo para distinguir resultados construídos, hipóteses, extensões abertas e confirmação física. A seção histórica I.7 do Atlas deixa de ser instalada como uma pendência permanente; continua disponível na consulta ao Atlas intacto.

[REAL — catálogo de fontes] O pacote preparado contém 1.007 arquivos embutidos, dos quais 1.003 são fontes Lean. Foi extraído por `ast.literal_eval`, sem executar ou importar o `um.py` original. Isto verifica disponibilidade e bytes; não constitui uma compilação nova. O recibo de compilação antigo será preservado, sem ser atribuído ao novo pacote. A versão e as fontes em edição paralela devem permanecer distinguidas das rodadas seladas.

[REAL — interface] A correção trata `\(...\)`, `\[...\]`, `$...$` e `$$...$$` antes do Markdown. Preserva código literal, blocos de código incompletos e preços. KaTeX continua com `trust: false`, seguido do saneamento existente. O novo seletor de modelos da sessão paralela foi preservado na cópia preparada.

[REAL — verificações] Passaram 3 testes do núcleo temporal/fixo, 13 de memória/orçamento, 4 de recuperação e 11 do catálogo. Passaram também 9 verificações com o marked/KaTeX embarcados e as 78 verificações existentes do saneamento da interface. As verificações de importação foram executadas com o caminho da bancada, sem importar o servidor de produção.

[OPEN — implantação] Nenhuma alteração desta bancada foi instalada em produção. A revisão automática rejeitou a chamada ao script de implantação, mesmo sem `--apply`, por entender que seu escopo de gravação exige autorização específica. O operador recebeu a pergunta para aplicar núcleo, janela, catálogo, fórmulas nas fontes móveis e reinício somente do servidor web. Não publicar nas lojas nesta etapa. As compilações Android já geradas continuam referentes ao código anterior e não devem ser anunciadas como contendo estas correções.

Evidências: `baseline.json`, `baseline_reconciled.json`, `fixed_kernel_measurement.json`, `nucleus_prepared.json`, `iald_nucleo_fixo.json` e os testes desta pasta. Não há recibo `deployment.json` até uma implantação bem-sucedida.


### 15/09/2026 17:29 -0300 — Núcleo instalado; autoria e busca verificadas

<!-- IALD_FIXED_NUCLEUS_LIVE_20260915 -->

[INPUT] O operador respondeu “prossiga” à implantação específica do núcleo, fórmulas, fontes móveis e reinício web. Durante o trabalho pediu orientar testes em grupo iOS/Android e relatou falhas ao identificar o autor/pesquisar; esses pontos foram incorporados.

[REAL — instalado] Sete documentos integrais fixos, leitura a cada chamada, sem corte silencioso. Verificação final mediu 324.352 tokens de contexto, janela 400.000. Autoria explícita: Luiz Antonio Rotoli Miguel. Remissões matemáticas acrescentadas para o Hamiltoniano positivo dos Three Locks (v22, regime finito) e H=-log(rho*) / resistencia_beta, com hipóteses e estatutos. O Atlas original permanece íntegro; registros históricos não são tratados automaticamente como pendências atuais. Catálogo disponível: 1.007 fontes, 1.003 Lean, extraído sem executar um.py; compilação nova não realizada.

[REAL — interface e API] Quatro cópias de iald.js iguais (web, www, iOS, Android), com fórmulas protegidas antes do Markdown e KaTeX seguro. A resposta técnica no navegador apresentou 47 fórmulas, 24 em bloco, zero katex-error. O teste direto de autoria recebeu HTTP 200, 324.211 tokens de entrada e resposta correta com fonte paper_PT.tex. O teste na UI também respondeu o autor e executou search_web (1.637 caracteres retornados), citando https://teoriadagravitacaoluminodinamica.com/entry/. Isso prova busca e resposta no teste, não leitura integral independente dessa página nem acurácia universal.

[REAL — limites e correção] Uma tentativa inicial teve 429; o diagnóstico seguinte mediu 500.000 TPM. Instalado retry apenas para rate_limit_exceeded temporário com prazo informado, até duas repetições/120 s de espera acumulada, mantendo keepalive e cancelamento; sem repetir stream parcial, falta de crédito, request too large ou falha de transporte. Testes: 7 novos, 218 regressões do motor e 3 do núcleo passaram; antes, 31 Python/87 JavaScript da preparação passaram. Cotas, segredos e contas preservados.

[REAL — operação] Reinício somente de filhos do supervisor web 47020. Última conferência: web PID 67884, /health 200; llama PID 34128 preservado. Recibos de instalação e verificações em work/iald_context_math_20260915. Os antigos recibos “restart pending” são retratos intermediários; este adendo registra o reinício concluído.

[OPEN — gasto] A verificação final do Hamiltoniano chegou a consultar kernel e Atlas, mas parou antes da resposta por teto local diário. Configuração lida: global US$1, operador US$1, usuário comum US$0,20; soma global liquidada US$0,852227, insuficiente para reservar outra chamada integral. Não foi falta de crédito comprovada na conta OpenAI. Pergunta enviada para elevar global/operador a US$5/dia, preservando usuários comuns; ainda sem resposta neste registro. Não elevar antes da autorização. Sem essa alteração, renovação diária às 21h de Brasília.

[OPEN — distribuição] Nenhum novo APK/AAB/IPA compilado/publicado nesta etapa. Fontes móveis atualizadas; binários antigos não contêm a nova renderização. Guia TESTES_EM_GRUPO.md preparado: TestFlight externo com análise beta/link e Play teste interno (até100, e-mails/Google Groups); último estado Google ainda aguardava D-U-N-S. Não houve envio de convites a terceiros. TGL=ATLAS; IALD=ÍNDICE(TGL). Núcleo no contexto não altera pesos, não move o gate e não confirma a física.
