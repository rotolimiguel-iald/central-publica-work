# Lições da release v406 do app (03/11/2026) — para a próxima release

Números lidos dos artefatos desta pasta. A próxima release parte desta pasta (copiar só as ferramentas, como em `COPIA_DA_V405.json`).
Estado ao escrever: pacote **construído, validado e aceito por revisor independente (rodada 1)**; **NÃO instalado**. A instalação exige a janela de manutenção do filho web (porta 8082), que a ORDEM_004 reserva ao operador.

## O que mudou no pipeline (e foi medido)

1. **R3-1 aplicada:** `KEEP_FLAG = r'H[123]|discharg|condition|verif'` com `re.I` (`app/build/haiku_codec.py`). Na v406: 12.104 bandeiras TRUE na fonte; catalogáveis com a regra velha 11.637, com a nova **11.621**; **16 nomes** voltam ao literal (~905 B): 6 por `H[123]` sem delimitador e 10 por `verif` (`…name_verifies…`). Dois dos 6 são `ext_th2_dense…` e `ext_th2_omega_norm…`: «th2» é de teorema, e o `re.I` casa «h2» dentro de «th2» (sobrecaptura inofensiva: ficam literais, nenhum par se perde). Para eliminá-la, `(?<![A-Za-z])H[123]` sem `re.I`; não foi feito porque a ordem fixa a expressão.
2. **R3-2 aplicada:** a receita de leitura do `kernel_formalization` diz `max_chars 4500`. Busca exercitada pelo construtor (semente 20261103): **700/700**, 0 falhas (v405: 699/700). O revisor, com semente própria (40640406): 524/525; a única falha é artefato de medição (nome com «σ», guardado como `σ` no selado; re-medidos 4/4 recuperados).
3. **Janela P2 deslizada (decisão da gerência, ORDEM_004):** `SHARED_P2_SUFFIXES` = `_v402.._v406` (saiu `_v401`). Os tópicos que saíram (3: `falsidade_da_inercia_v401`, `cunhagens_v401`, `kh_n1_cobertura_v401`) viram cápsula compacta **mas mantêm `limites`/`diz`/`nao_diz`** (patch `fit_memory.compact(..., literal_suffixes)` + `P2_RETIRED_LITERAL_SUFFIXES` em `release_cfg.py`, lido por `prepare.py`). Medido: `shared` 812.335 B; folga mínima com a reserva declarada de 148.656 B = **41.975 B** (DeepSeek; Kimi 45.364; MiMo 41.992); `_v402` **não** precisou sair. O revisor recomputou 105 literais `limites/diz/nao_diz` iguais ao selado no `shared` e no `sonnet_public`, 474/474 tópicos presentes.
4. **Haiku55:** sufixos expandidos `_v405,_v406`; 1.575.137 B; 841.257 tokens permanentes; folga **139.788** tokens (v405: 172.998; v404: 28.640). Mínimo de runtime: 10.000.
5. **Tamanho da release:** a v406 trouxe só 3 tópicos novos (`fechamento_v406`, `cunhagens_v406`, `kh_n1_cobertura_v406`; 80.663 B de fonte) contra 13 da v405 (283.684 B). O `shared` cresceu 31,8 KB (780.493 → 812.335 B). A premissa «uma v406 do mesmo porte não cabe» não se aplicou ao tamanho real; a janela deslizou mesmo assim, por decisão da gerência.
6. **Contrato JEV:** `jev_control_v406.json` gerado por `prepare.py` em `app/science/memory_stage/`, destino `canonical_releases\v406_a381c4d14709\jev_control_v406.json`, sha256 `226c0b18a3d2751742b092f9b971c55575e05098f37972e6bff4fa929df52564`, `source_sha256` = pino do `um.py` (`ddcb91930982d6143f47127d43020ab97cb9f5275331f470f2d0e4caaffd1fc0`). O revisor conferiu que só campos de versão diferem do contrato instalado. A Torre só o enxerga depois da instalação (`torre.py gerar` procura em `canonical_releases/v406_*/`).
7. **Plano de instalação:** 1.773 arquivos; 1.765 sob `canonical_releases\v406_a381c4d14709` (diretório novo), 1 `core_packet_v406_bound.txt`, 3 + 3 pacotes em `.iald_runtime/haiku55` e `.iald_runtime/haiku`, e o manifesto ativo `iald_nucleo_fixo.json` por último. 0 `.py` de runtime substituído.
8. **Contagem nativa:** 6 pedidos de contagem (3 pacotes × 2), 0 geração, `max_retries=0`, sem contexto do operador, sem atlas privado. Usa a chave do próprio app (`count_final_public.py` lê `IALD_CLAUDE_API_KEY` do `.env` do app; o conteúdo da chave não foi lido por mim).

## Resíduos BAIXOS declarados (parecer r1; não valem nova rodada)

- **F1 — o único com sabor epistêmico:** no haiku55, `projecao_transversal_v404/name_status` (`estado: PROVISORIO`, «aceito_pelo_operador: até ele dar outro») virou só ponteiro. Causa: a janela expandida do haiku55 deslizou para `_v405/_v406` e `protected_fields()` só protege valor ESCALAR sob chave ESSENTIAL; `name_status` é um dict. No `shared` e no `sonnet_public` está literal; 1 de 208 chaves de qualificador no haiku55; recuperável pelo ponteiro. **Para a v407:** estender `protected_fields` a dicts de status (ou manter `_v404` expandido).
- **F2** — nomes catalogados com «σ/Δ» (4) ficam escapados no selado; a receita os recupera (consulta literal e escapada).
- **F3** — `shared` e `sonnet_public` trazem `kernel_formalization` só como contagem (12.104 TRUE / 4 FALSE sem nome); herdado da v405.
- **F4** — DeepSeek: folga real de 106 B com o output reservado pelo runtime (adaptativo); 41.975 B com a reserva declarada. Por desenho, igual à v405; com histórico longo o runtime recusa de forma visível.
- **F5** — em `falsidade_da_inercia_v401` o registro `unconditional` (registro de teorema) ficou só ponteiro; `estatuto`, `limites`, `nao_diz`, `verdict` e `scope` ficaram literais.

## Para a v407

- **Deslizar a janela de novo:** a folga mínima declarada é 41.975 B; uma release de ~30 KB no `shared` consome três quartos dela. Sai `_v402` (27,1 KB no `shared`): acrescentar `'_v402'` a `P2_RETIRED_LITERAL_SUFFIXES` e tirá-lo de `SHARED_P2_SUFFIXES`. Se a release for do porte da v405 (104 KB), saem `_v402` e `_v403`.
- **Promover o check da janela a ferramenta do pipeline:** o construtor adaptou o `q3_window_topics.py` do revisor v405 (`review/revisor_sonnet-app-v405-revisor/`); o revisor v406 refez o seu. Vale um `check_janela_p2.py` único, na pasta de ferramentas. [recomendação]
- **`builder_measurements.py` foi reescrito** sem literais de versão (lê `app/RELEASE.json` e `BUILT.json`): na v407 não precisa de edição. `task.py` ainda traz o texto da «consulta» da unidade escrito à mão por versão, e `release_cfg.py` os rótulos `OWNER`/`BUILDER`: editar na cópia.
- **`deploy_controlled.py` acopla instalação e reinício** do filho web (suspende o supervisor, encerra o filho, escreve, retoma): não há modo «instalar sem reiniciar», e `assert_quiesced` impede escrita com o web de pé. Por regra da ORDEM_004 o reinício é do operador.
- **Caminho do destino:** o real é `v406_a381c4d14709` (12 hex, convenção da v405). O briefing que eu dei ao revisor abreviou para 10 hex; erro meu de escrita, sem efeito (o plano e o `release_cfg.py` usam os 12 hex; o revisor anotou como INFO I2).

## Processo

- Copiar só as ferramentas (24 arquivos), não os resultados da v405: `COPIA_DA_V405.json` lista origem, destino e hash; `deploy_controlled.py` recusaria `deployment.json` existente e os recibos antigos se confundiriam com os novos.
- Tempo: etapa 1 (claims, fontes, prepare, finalize) ≈ 1 min; etapa 2 (contagem, validação, medidas, busca) ≈ 3 min; revisão ≈ 15 min.
- **Custo do revisor:** o revisor da v406 (sonnet, estreito, lista Q1–Q8 e reaproveitamento dos scripts do revisor v405) gastou ~287 mil tokens em 36 chamadas, contra 666 e 825 mil das duas rodadas da v405.
- **Ordem na missão:** `submit sources` e `submit app` → revisor `accept sources` e `accept app` (feito, revisões 4–7) → **pendente:** `claim deploy` → `deploy_controlled.py` (reinício do filho web: operador) → `submit deploy` → `accept` → `claim verify` → `verify_installed.py` → `submit verify` → `accept`.
- **Confidencialidade e redação:** 0 nomes/chaves vedados nos 3 prefixos; os 5 contextos de «CONFIRMED» foram lidos à mão (todos negados ou lista de vereditos proibidos).
