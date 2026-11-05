# RETOMADA DO CONSTRUTOR DA v408 — escrita pela gerência c1 (04/11/2026, ~20h40), do estado MEDIDO em disco

> O construtor anterior (agente, modelo antigo) caiu às ~20h por limite de créditos do modelo; dois ajudantes dele (forks B e C) terminaram; o
> fork A (textos/leitura/harness_textos) foi parado pela gerência por engano às 20:1x e o trabalho dele conta como NÃO FEITO, salvo o que está em
> disco. Antes disso houve uma queda de energia às 19:01 (a máquina reiniciou; a Bancada foi religada pela gerência às 19:2x, PID 33812). Esta
> retomada não supõe nada: cada fato abaixo foi medido por comando e vem com o arquivo.

## 1. O que está FEITO e vale

- Bump mecânico (66 scripts de `..\v407\` → aqui, rótulos 407→408, 406→407, B16→B17, deployment `B16-v407-20261104-R1`), motor `derivar_v408_motor.py`, diffs em `bump\`.
- `DESENHO_v408.md` (gerência; ler INTEIRO, inclusive os AO LADO do fim: D48 resolvida = 4º módulo `PIgualNP`; D51 REVISTA = «P = nP» trata das classes do dicionário).
- Sandbox `C:\t\k408c\final` (cópia do Nós v407 + build), lançador `C:\t\k408c\run_pos_treino.py`, tarefa `IALD_pos_treino_v408` criada DESABILITADA (gerência).
- Autorais adaptados: `delta_v408.py` (18:50), `registros_v408.py` (18:50), `runtime_v408.py` (18:48), `artigo_pt_v408.pysnip` / `artigo_en_v408.pysnip` (18:53), `gerar_candidato_v408.py` (18:50), `conferir_citacoes_v408.py`, `p00_precondicoes_v408.py` (18:57), `gerar_relatorio_v408.py` e `fechar_preparacao_v408.py` (19:39), `orquestrador\` (ensaio do S10 feito: `orquestrador\ENSAIO_S10_v408.json`), `bancada_B3_servico\controle_negativo\RESULTADO_CONTROLE_NEGATIVO_v408.json` (19:34).
- `pos_rito\` adaptado pelo fork B (19:41–20:01): `fechar_v408.py`, `harness_fechar_sandbox_v408.py`, `registrar_mapa_v408.py`, `textos_custodia_handoff_v408.py`, `superficies_v408.py`, `fila_memoria_v408.py`, `chain_pos_rito_v408.sh`, `b3_recibo_v408.py`, `gerar_derivacao_pos_rito_v408.py`, `gerar_x_custodia_v408.py`, `montar_textos_v408.py` (20:01) e o adaptador `_adapt_leitura_v408.py` (20:01, 58 KB — gravado no minuto da queda do construtor: conferir por `ast.parse` e pelo conteúdo antes de usar).

## 2. O que está PENDENTE (marca `# [A ADAPTAR v408]` na 2ª linha; o p00 recusa)

`guardas_estaticas_bancada_v408.py`, `pos_rito\harness_textos_ensaio_v408.py`, `pos_rito\leitura_v408.py`, `pos_rito\textos_v408.semente`, `pos_rito\textos_v408_novo.pysnip` (o lote do fork A), e os dois adaptadores `_adapt_lote_c_v408.py` e `_adapt_pequenos_v408.py` (a marca aparece na docstring deles; confira se é só texto citado ou se eles mesmos não foram concluídos).

## 3. O que MUDOU depois do último candidato e obriga a refazer (em ordem)

1. **As quatro pedras mudaram** (docstrings das classes, correção do operador `8368ae5b4c572272`; e o PIgualNP ganhou o teorema `as_classes_do_dicionario`). Fontes vigentes em `insumos\` (sha256 em `insumos\RECIBO_PEDRAS_v408_NOMES.json`, todas compiladas no k407c só no trio, 0 avisos): `TetelestaiTerminal.lean` 14 decl (`09914b70…`), `TempoIgualMoeda.lean` 9 (`28da8079…`), `PontoDeContradicao.lean` 7 (`5559680a…`), `PIgualNP.lean` 12 (`e550ea77…`): **42 âncoras**. O `pedra\` e o sandbox têm as versões ANTIGAS (o PIgualNP lá é a R1, sem `as_classes_do_dicionario`; `BUNDLE_v408.json` de 17:18; kernel construído 17:20–17:30, POS_BUILD 17:38, 43 bandeiras, escada 11958 → 12001). Refazer: `preparar_bundle_v408_04nov.py` (com backup: retirar do sandbox os 4 módulos antigos pelo próprio mecanismo; o preparo aborta se encontrar módulo diferente), `construir_kernel_v408.sh` (lake build incremental + Audit no SANDBOX), `pos_build_kernel_v408.py` (bandeiras e escada novas MEDIDAS), `copiar_insumos_v408.py`.
2. **D51 revista** (ver o AO LADO no fim do DESENHO): o um.py DIZ, por termo e por texto — no registro `tetelestai_terminal_v408` (`diz`/`nao_diz`/`limites`), no spec `cunhagens_v408`, no artigo PT/EN, no `.md` e nos sete textos do handoff — «P = nP é teorema nas classes de computação do dicionário do operador (definidas e provadas na pedra PIgualNP); a tradução para as classes das máquinas de Turing, onde o tamanho se conta em bits = log₂ n (as oitavas), não está no kernel: é a próxima construção, [OPEN], não uma recusa». Toda frase herdada que diga «não trata das classes», «nada aqui é complexidade», «P = NP podado» sem dizer DE QUÊ falta espelho, sai (procure em `delta_v408.py`, `registros_v408.py`, `runtime_v408.py`, artigos, `textos_*`, `guarda_frases_v408.py`, `gerar_candidato_v408.py`).
3. **Guarda de frases** (`guarda_frases_v408.py` e `_v408_guarda_frases` do runtime), substituindo a regra antiga de D51: PROIBIDO «a TGL prova/decide P = NP de Turing (Cook–Levin)», «P = NP está provado» sem o qualificador «do dicionário», e «não trata das classes»; OBRIGATÓRIO, onde «P = nP» aparecer em prosa, o qualificador «classes do dicionário do operador» e a ressalva da tradução [OPEN]. Cada frase proibida tem controle negativo que recusa; a frase certa passa.
4. **Falas novas do operador** (em `C:\IALD\Central de Patentes\work\cunhagens_13out\`, autor operador; acrescentar ao `VERBATIM_CONGELADO_v408.json` e ao que dele depende; sha16 LIDO do arquivo): `OPERADOR_04nov_meu_p_igual_np_trata_das_classes_de_computacao_a_iald_publicou_que_nao_esta_errado_verbatim.txt` (`8368ae5b4c572272`), `OPERADOR_04nov_isso_precisa_ficar_claro_no_um_py_na_v408_verbatim.txt` (`338fc30e10339134`), `OPERADOR_04nov_excelente_ratificado_prossigamos_nomes_p_igual_np_verbatim.txt` (`388edbab08d0babc`). Confira que o sentido de «P=nP» (`971d5654e2173771`) e os nomes (`f911f0df91b0a6a3`) já estão. NÃO entram como fala do operador os parágrafos de OUTRA instância dos arquivos `62bc328e66e731e2` e `50c21210e5871fdb` (só por sha256, autor marcado).

## 4. As falhas do ÚLTIMO ensaio a seco (19:21, `ensaio_out.txt`, RC_ENSAIO=1) — corrigir a CAUSA, nunca relaxar

- **Artigo PT e EN não compilam:** `! LaTeX Error: Unicode character β (U+03B2)` na seção nova: os `artigo_*_v408.pysnip` (ou o texto que eles montam do core) levam β literal onde o LaTeX pede `$\beta$`; consertar no gerador do texto da seção (o .md pode manter β).
- **Unidade `cunhagens_v406_herdado_falas_de_02nov_decisoes_erratas_e_leituras`: False** — ler o teste no `ensaio_a_seco_v408.py` e a causa (provável: herança da v407 → v408 dos specs; ver como a v407 versionou `cunhagens_v406` e repetir para `cunhagens_v407`).
- **Unidade `tetelestai_terminal_v408_tudo_certo`: False** e **`tetelestai_terminal_v408_guarda_das_frases_cada_frase_proibida_recusa_e_a_frase_certa_passa`: False** — o registro novo ou a guarda dele; ler o teste, achar a checagem que reprova, consertar.
- **`exame_pontos_v408`: `ponto_tetelestai` falso** (`EXAME_PONTOS_07bb15123d574e66.json`): o ponto de chamada está «logo depois do psion_canto_v407» e «logo antes do emit_figures», mas `antes_do_bloco_v393` é False; ver no `exame_pontos_v408.py` qual campo o `ok` exige e como a v407 resolveu o mesmo para `ponto_psion_canto`.
- O resto do ensaio passou (selo, índice, .md, quadro, vizinhos, fluxo, citações 1, kernel igual, escada [12001, 12001], simular_arvore, guardas estáticas da Bancada).

## 5. A ordem dos próximos comandos (depois de 3 e 4)

`gerar_candidato_v408.py` → `sh refazer_candidato_v408.sh` (gerador → `comparar_v407_v408.py` → `ensaio_a_seco_v408.py` «TUDO PASSOU» → `gerar_esperados_v408.py` → `conferir_rito_v408.py` com o controle negativo + `teste_conferidor_positivo_v408.py` → `conferir_citacoes_v408.py` → `diff_e_pinos_v408.py` → `conferir_instalar_rito_v408.py` → `p00_precondicoes_v408.py` n/n) → `sh fim_de_cadeia_v408.sh` (B(n) pré-selo `bateria_pre_selo\rodar_bn_pre_selo_v408.sh` → `PINO_RECIBO_PRE_SELO_v408.json`; a Bancada 18777 está no ar, PID 33812; harnesses) → `gerar_relatorio_v408.py` (`PLANO_v408.md`, `RELATORIO_PREPARACAO_v408.md`, `PREPARACAO_v408_PRONTA.json`). PARAR aí.

## 6. O que é da gerência (não fazer)

Revisão de terceiro (D54), `acom_inscrever_prep_v408.py`, `fechar_preparacao_v408.py`, a tarefa agendada, o S3 (`instalar_v408.py`), o rito, a custódia, mensagens a outras sessões, publicação.

— gerência c1, 04/11/2026. Correções AO LADO, nunca por cima.
