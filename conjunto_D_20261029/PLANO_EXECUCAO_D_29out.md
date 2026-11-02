# PLANO DE EXECUÇÃO — conjunto D (ramo B do ringdown, pré-registro V1) — 29/10/2026

Autoria: estudo técnico pedido pela gerência c1 (subagente, só leitura + pasta nova). **Não executei a PE real, não abri dado real de D (nenhum posterior, nenhuma amostra de strain), não modifiquei nenhum arquivo existente.** Tudo o que está aqui foi escrito em `C:\IALD\Central de Patentes\work\conjunto_D_20261029\`.

Estatutos: **[REAL]** medido por mim hoje (script, hash do disco, execução); **[DECLARADO]** lido de recibo/documento da bancada ChatGPT/Codex, não reproduzido; **[DERIVED]** cálculo meu sobre entradas declaradas; **[INFERENCE]** raciocínio; **[OPEN]** decisão ou medida que falta. NOT_FALSIFIED nunca é CONFIRMED.

---

## 0. Em uma tela

1. **O que existe e roda:** V1 congelado e lido por hash [REAL]; os 10 eventos têm strain H1+L1 em disco, com sha256 igual ao manifesto (20 HDF5 + 20 NPZ) [REAL]; janela de 32 s ao redor de cada evento tem DQ limpa nas duas estações [REAL]; a forma de onda `pSEOBNRv4HM_PA` com `dtau220 ≠ 0` sai do `pseob_source` de 015 em **0,065 s por chamada** (1,02 s na primeira) [REAL, §3]; código de PE controlada (bilby + dynesty `rwalk`, 24 workers) existe e já rodou em GW250114 [DECLARADO].
2. **O que NÃO roda como está:** toda a cadeia de guardas 013-bis/015 (`registration_guard`) está **vencida e fechada**: prazo `hard_deadline` 2026-10-03T15:36:46Z, recibo de auditoria gerencial `RECIBO_015_V1_1_AUDITADA.md` **ausente**, pasta `Chatgpt` só leitura, caminhos de strain fora da raiz permitida [REAL, §2.g]. É preciso um **guarda novo, pinado ao V1 do ramo B** (código a escrever, §6).
3. **A PE nunca convergiu na casa:** 2 de 2 PE reais de GW250114 pararam em `maxcall` com Δlogz = 425 e 177 (alvo 0,1) e ESS ≈ 1; a PE sintética INIT003 também (Δlogz 57) [DECLARADO, recibos lidos hoje]. O custo até convergir em D é **desconhecido**; meus cenários dão **170 CPU-h por PE (central)**, com faixa 51–517 [DERIVED/OPEN, §7].
4. **O poder de planejamento de D é < 5σ:** 3,7–3,9σ (10 eventos) e 4,4–4,6σ (14, com os 4 holds) [DERIVED, §4.3]. Se confirmado na PE, o veredito pela regra 2 da Fase 6 é `NOT_FALSIFIED_UNDERPOWERED` **qualquer que seja o valor central de δ̂** (a regra 3 vem antes da 5), salvo `INSUFFICIENT_SAMPLE` ou `INCONCLUSIVE_SYSTEMATICS` (C1–C9, χ²/dof > 3, rótulo), que vêm antes. Com n = 10 exato no mínimo (`min_eventos=10`), uma só PE não convergida dá `INSUFFICIENT_SAMPLE`.
5. **Tempo** (2 PE de 24 workers em paralelo nos 48 núcleos): D10 sozinha, central: 55–63 h; cadeia completa (F4.1 + D10 + C2 mínima), central: 121–140 h (5–6 dias); otimista 36–42 h; pessimista 15–17 dias [DERIVED, §7].
6. **Autorização:** a gerência já registrou hoje (Mapa, `ringdown.ramo_b_preregistro_v386`, seq 1545, 14:40) a ordem verbatim do operador «autorizo a realização do teste do conjunto D» (sha256 `9e54b477…bdbc9`, lido do disco) e fixou o alcance: D decide **só o par** do ramo B, com o canal F2b retirado ao lado na v404 [REAL]. Não resta contradição de registro; resta o **orçamento de CPU** (dias de máquina inteira), que a ordem não fixa [OPEN, §6-D2].
7. **Correção ao `defeito` registrado no seq 1545:** a frase «se D se comportar como a calibração A (+0,072 ± 0,034) … FALSIFIED_AT_5SIGMA do par (z_excl ≈ 7 com 10 eventos)» supõe a informação média do A31 (σ_comb ≈ 0,059 para 10 eventos). Com o **SNR de D** (12–17) a projeção é σ_comb ≈ 0,10: z_excl ≈ 4,4–4,6 < 5 e, antes disso, **poder < 5 ⇒ `NOT_FALSIFIED_UNDERPOWERED`** (regra 3 antes da 5). O ajuste que gera a projeção, aplicado ao próprio A31, dá σ_comb = 0,0355 contra 0,0336 declarado (erro de 6 %) [REAL, §4.3].

---

## 1. Mapa de Rotas — o que li e o que não refaço

Consulta feita antes de qualquer trabalho: `rotas.py consultar "ringdown"` (27 rotas) e `consultar "PE"` (337, truncado), depois `rotas.py ver ringdown.ramo_b_preregistro_v386` e `ver ringdown.dephasing`; ainda `ver ringdown.modo_unico.degenerescencia` e `ver discriminante.ordem_018_chatgpt_codex`; e `NOS_VIVO\consultar.py --unidade F4.1/F4.2/F4.3`.

| rota (seq) | o que diz | consequência para este plano |
|---|---|---|
| `ringdown.ramo_b_preregistro_v386` (365: V1 lido por hash, F2b AWAITING) | V1 congelado por hash; vereditos permitidos na ordem; conjunto D cego, 14 elegíveis, 10 sem hold | base do plano |
| mesma rota (1508 e 1526, 28/10; E8 da v404) | calibração A (NOT_BLIND) deu +0,072 [+0,015; +0,134] contra a previsão do par −0,382; canal F2b passa a `WITHDRAWN_BEFORE_DATA__ROUTE_CORRECTED_BY_NOT_BLIND_CALIBRATION_AND_AUTHOR_READING_2026_10_28`; **«proximo_passo: o ramo B (par fonte) deixa de ser a leitura; … nada a abrir em D»**; `nao_refazer`: «Não repetir INIT003/imports 5e391d57/4a0 … Não executar A/B, ler/hash arrays externos, contornar d72 …» | tensão com a ordem de hoje, **já tratada** pela gerência no seq 1545 (abaixo) |
| mesma rota (433–687, 05–06/10) | INIT003: 9738 chamadas, 857,9 s, Δlogz 57,28, ESS null, STOPPED_NOT_CONVERGED; RB interrompido; proposta A (100 000 chamadas por caso, 14 400 s) preparada e revista, **não executada** (F4.1 AGUARDA_OPERADOR) | não refazer INIT003; o custo real por convergência é maior que o envelope A (§7) |
| `ringdown.dephasing` | V2 do dephasing: poder 0,2σ (ramo A invisível); «a PE só-220 do conjunto D fica para a v387 (custos [DECLARADO] 63–78 / 58–390 CPU-h)» | custos declarados reaparecem em §7, reinterpretados por PE |
| `ringdown.modo_unico.degenerescencia` (F4.3, seq 957–969) | F4.3 (220+440) AUDITADA; «poder NÃO medido; pedido ao operador SUSPENSO» | o 440 não entra; F4.3 é outra unidade |
| NOS_VIVO F4.1 / F4.2 | F4.1 «P3 qualificado (A02)» e F4.2 «PE solo-220 de D» no grafo: **AGUARDA_OPERADOR**; F4.2 critério: «veredito da função pré-registrada sobre o conjunto D» | a autorização do operador de hoje (já registrada, seq 1545) destrava os dois |

**Estado do registro [REAL, lido do disco durante o estudo]:** `work\cunhagens_13out\OPERADOR_29out_autoriza_conjunto_D_verbatim.txt` (sha256 `9e54b47780dab1010785726f2fb55d0675b6c59d5d7118ad0f77be8c650bdbc9`) = «autorizo a realização do teste do conjunto D»; `rotas.py` seq 1545 (RESULTADO, EM_CURSO, 29/10 14:40): «AUTORIZADO e em preparação … nenhum dado aberto»; veredito `TGL_RAMO_B_SET_D__AUTHORIZED_BY_OPERATOR_20261029__EXECUTION_IN_PREPARATION__NOTHING_OPENED__GATE_UNTOUCHED`; `defeito`: D decide só o PAR (canal F2b retirado ao lado na v404). A retirada do canal não revoga o V1 (E8: «segue congelado por hash»). **Pontos que o registro ainda não cobre [OPEN]:** (i) a ordem não fixa o orçamento de CPU/parede (§7: de 1,5 a mais de 40 dias de máquina conforme o cenário); (ii) `nao_refazer` da rota proíbe «contornar d72» e «ler/hash arrays externos»: o plano abaixo **não repete INIT003**, usa guarda novo e não usa o pacote P3 do Codex; o hash de bytes do strain (que fiz hoje, §4.2) é só confirmação do manifesto — se a gerência entende que isso é «ler/hash arrays externos», declare errata ao lado.

---

## 2. O que o código faz (respostas (a)–(g), com linhas)

Árvores: `e2_code` (013-bis, 27/09), `e2_code_v1_1` e **`e2_code_v1_1_2`** (015; a última, com grade de geração 8192 Hz; é a que o Codex descreve em `NOTA_CONJUNTO_D.md`). Linhas abaixo: `v1` = `e2_code`; `v112` = `e2_code_v1_1_2` quando difere. Hashes na tabela do §4.

### (a) Como se lança a PE

- **Único lançador:** `run_controlled.py --job <nome>` (v1 l.37: o único argumento). Ele chama `checked_registration()` e `load_jobs()` (l.39), `authorize_event(reg, evento, modo)` (l.41), recusa `workers > 28` (l.43) e, em calibração, `wall > 10 h` (l.45); exige `privacy_mode == 'procedural_same_host'` (l.46); `stop = min(time_guard(reg), agora + wall)` (l.47); cria `BASE/'cache'/<output_directory_name>` (l.49; `output_path` em `registration_guard.py` l.133–135), grava `LAUNCH_CONTEXT.json` (l.50–55) e lança `pe_runner.py --job … --launch-context …` com `start_new_session=True`, stdout/stderr no `PRIVATE.log` e 1 thread de BLAS (l.56–68); mata o grupo no prazo (l.70–73, `cleanup_group` l.14–33); grava `CONTROLLER.json` (l.87–95).
- **«Direct CLI is rejected» (g):** `pe_runner.py` l.1 e `main` (v1 l.173–179) chamam `validate_launch` (`registration_guard.py` v1 l.232–252; v112 l.357–386): o contexto de lançamento tem de existir e bater com o hash da configuração; `controller_pid == os.getppid()`, o processo tem de ser líder de sessão e de grupo (`os.getsid(0)==os.getpid()`), os *start ticks* do controlador em `/proc` conferem (anti-reuso de PID), `stop_utc` dentro do prazo, e **stdout e stderr têm de ser o arquivo regular `PRIVATE.log`** (não tty). Logo só o `run_controlled` satisfaz a guarda.
- **Registro exigido:** v1 `ORDEM_013_RINGDOWN/RINGDOWN_5SIGMA_V1.json`; v112 a cadeia `RINGDOWN_5SIGMA_V1_1*.json` (`load_registration_chain_v1_1`, l.425; a última é `…_V1_1_3.json`). O guarda confere: testemunha com `registro_sha256` em `TUNEL/DO_CHATGPT/` (v1 l.36–39, 157–167), recibo de ativação e **quatro revisões** (v1 l.71–110), **árvore de código** igual à registrada (l.41–42), pinos de entrada (l.47–48), manifesto do runtime `/opt/lal_env` e módulos ativos (l.49–66), e o relógio (`time_guard`, v1 l.112–118; v112 l.135–186).
- **Autorização por evento:** `authorize_event` (v1 l.120–131; v112 l.189–201): modo `blind_test` exige evento **fora** de `calibration_event_ids`, entrada em `test_candidates` com `eligible=True`, `published_deformation_at_registration=False` e `publication_census_scope`; `validate_job_reviews` (v1 l.169–185) exige revisão de metadados de publicação e, se `data_quality_hold`, resolução de DQ com hash. **v112 acrescenta** `check_blind_activation` (l.121–132): exige o recibo gerencial `TUNEL/PARA_CHATGPT/RECIBO_015_V1_1_AUDITADA.md` — **ausente em disco** (só existe `RECIBO_015_MAQUINA_LIVRE.md`) [REAL].
- **Janela temporal:** `temporal_contract.validate_time_contract` (l.5–27), chamado a cada waveform: calcula limites conservadores de LAL (`SimInspiralChirpTimeBound`, `MergeTimeBound`, `RingdownTimeBound × max(1, 1+dtau)`) e aborta se `geocent_time − 0,022 − inspiral − merger < start + roll` ou `geocent_time + 0,022 + tail > start + dur − roll` (`WINDOW_BOUND_VIOLATION_ABORT_NOT_PRIOR_REJECTION`). **[REAL, medido hoje com LAL 6.2.1]** nos cantos do prior (15+10 M☉, χ=±0,99, dtau ∈ [−0,8; 2]) o pior caso exige 5,72 s antes do pico e 1,31 s depois: **janela de 16 s com o evento a ~12 s serve** (como no piloto de GW250114: início = GPS − 12,2).
- **Relógio vencido [REAL]:** `PART_015_BUDGET_START.json`: `hard_deadline_utc = 2026-10-03T15:36:46Z`; hoje é 2026-10-29. `time_guard` levanta `TimeoutError('Part 015 hard deadline reached')` (v112 l.184), e `checked_registration()` chama `time_guard` (v112 l.61). Reabrir a cadeia exigiria novo orçamento testemunhado **dentro de `Chatgpt/TUNEL`** (pasta só leitura para nós). **Conclusão: o guarda da casa não pode ser reaproveitado; copiar o código e trocar o guarda.**

### (b) `blinding.py`

- v1 l.14–35: exige as quatro colunas `dtau220, dtau440, domega220, domega440` pareadas (l.15–17); lê a semente de `registration['blinding']['seed_relative_to_Chatgpt']` (l.18; `…/cache/E2_PRIVATE/BLIND_SEED_V1.bin`, que **não li**), confere o compromisso SHA256 (l.19) e 32 bytes (l.21); `scale = offset_half_range` (= 1,0 no registro). Para cada (evento, campo): `u = (int(HMAC-SHA256(semente, '013BIS:'+evento+':'+campo)[:8]) + 0,5)/2⁶⁴`; **soma `scale·(2u−1) ∈ (−1, 1)` a TODAS as amostras do campo** (l.29–31). Devolve `blinded_<campo>` + o compromisso + aviso «offset-censored; médias e sinais sem interpretação física» (l.33–35).
- **Como se lê só σ:** qualquer estatística invariante a deslocamento (desvio padrão ddof=1, largura W90, razão W90/3,29÷σ do C9) passa intacta; média, mediana e sinal ficam sob offset de até ±1, contra |δ_pred| ≈ 0,4. `pe_runner` só emite esses números em `ANALYST_OUTPUT.json` (v1 l.262–265; v112 l.289–291) e **só em modo `blind_test` e só se a PE convergiu** (`accepted_for_analysis`, l.246–249). O posterior bruto fica no `*_result.hdf5`, no pickle do dynesty e no `PRIVATE.log` do diretório de saída — **privados só por procedimento** («PROCEDURAL_SAME_HOST_NOT_SEPARATE_CUSTODIAN», `run_controlled` l.54): quem roda a pipeline não deve abrir esses arquivos até a abertura.
- `unblinding_allowed` (v1 l.37–49; v112 l.38–60) é um **teste de permissão por leitura (reading) com recibo** — nunca decisão implícita. Ele serve à cadeia 013-bis (leituras R-A…R-GLOBAL, informação mínima 95 215,98), **não ao V1 do ramo B**, que não define esse gate: a regra de abertura do V1 está na ordem de fluxo (linha 382 do `.md`); a autorização ligada ao hash do estágio cego é código/ato a criar (§6).
- A semente da 013-bis (`BLIND_SEED_V1.bin`, compromisso `b83d64c7…`) pertence a outro registro e à pasta do Codex: **não reaproveitar**; criar semente nova (§5, passo 2).

### (c) `injection_design.py`, `synthetic_null.py` e como se roda C2

- `injection_design.inject_into_ifos` (l.42–102): só modo `calibration` e só eventos de `calibration_event_ids` (l.44); família `pSEOBNRv4HM_PA` ou `IMRPhenomXPHM` (l.45–46); `noise_kind='REAL_OFFSOURCE'` (l.47); o GPS tem de coincidir com `reg['event_reference_GPS']`, que no registro só tem **GW250114** (l.48–50); a janela de análise não pode tocar o intervalo protegido do evento real (l.51–56); `parameters` completos incl. as quatro deformações (l.57–63, `validate_truth_support` l.26–39); reescala a distância para o SNR ótimo de rede-alvo (l.84–95) e injeta via `ifo.inject_signal` (l.96). A família XPHM só aceita deformações nulas (l.62–63). A análise tem de apontar os **mesmos bytes** de off-source (l.71–74).
- `synthetic_null.py` (l.11–58) **não injeta**: é a calibração escalar do falso-positivo (z>5) para o filtro casado; `null_runner.py`/`null_campaign.py` (receitas das células da 013-bis) idem. **Não servem a C2 do V1.**
- **C2 do V1** = «injeções só-RG e com `dtau220 = δ_pred(k)` na PE da casa (|viés| ≤ 0,2·|δ_pred|, cobertura)». Mecanismo existente: um job `mode='calibration'` com bloco `injection` `{family:'pSEOBNRv4HM_PA', noise_kind:'REAL_OFFSOURCE', target_network_optimal_SNR, parameters:{… dtau220: 0 ou δ_pred}}`; a PE recupera com a mesma fonte. **Falta:** adaptação para ruído off-source **dos eventos de D** (hoje só GW250114 passa as guardas) — ver §6.

### (d) De onde `pe_runner` lê o strain

- v1 l.195–205 (v112 l.216–226): por detector, `offsource_psd(contained(data['offsource_path']), data['offsource_sha256'], cfg)` e `window(contained(data['onsource_path']), data['onsource_sha256'], segment_start, duration, DQ, INJ)` em `strain_io.py` (l.45–73, l.29–43): HDF5 GWOSC de 4096 s a 4 kHz; confere sha256 do arquivo; máscara DQ de 1 Hz (`quality_mask` l.15–27); PSD de Welch (Hann, 50 %, mediana) do **primeiro bloco** de `psd_duration_s` segundos que passa DQ+finitude antes de `min(GPS − exclusão, início da janela)`; recusa início fracionário.
- `contained()` (guard l.26–29) rejeita qualquer caminho fora de `Chatgpt/`. Os HDF5 de D estão em `C:\IALD\Bancada_Um\fontes_externas\gwosc_o4\hdf5\` — **fora da raiz permitida** → o guarda novo precisa aceitar essa raiz com sha256 pinado.
- **Os 10 eventos têm strain nos caminhos da Bancada [REAL]:** 20/20 HDF5 e 20/20 NPZ existem, tamanho e sha256 **iguais ao manifesto** `GWOSC_O4_32S_V1.manifest.json` (§4.2). DQ dos arquivos (só metadados `quality/…`, sem abrir o strain) [REAL]: nos 10 eventos × 2 detectores os 32 s centrais passam `DATA, CBC_CAT1-3` e `NO_CBC/BURST/DETCHAR_HW_INJ`; `NO_STOCH_HW_INJ` também não falha; `NO_CW_HW_INJ` vale 0 em quase todo o arquivo (injeção contínua de CW — não deve ser exigida). Maior bloco limpo antes do evento: **mínimo 451 s (L1 de GW241130)** e 477 s (GW250118) → `psd_duration_s = 256` serve para todos; **512 s não serviria** para 2 eventos.

### (e) `remnant_conversion`: M_f,det e χ_f

- `derive` (l.11–47): por linha do posterior, `ls.SimIMREOBFinalMassSpin(m1·M☉, m2·M☉, [0,0,χ1], [0,0,χ2], SEOBNRv4)` → (status, fração de massa, spin) (l.33–36); **M_f,det = fração × (m1 + m2)** com massas **de detector** (l.40); **χ_f = spin do ajuste NR alinhado** (preserva sinal); `z` por inversão de D_L com Planck18 pinado (l.38). Saídas pareadas e na mesma ordem: `final_mass_detector, final_spin, redshift`. Estatuto: «ajuste GR aplicado ao posterior livre, não é medida independente do remanescente» (l.46). O V1 usa só a **mediana de χ_f** (`a_i`) para k(a_i), N(a_i) (M e (1+z) cancelam em x = β·k·N).

### (f) Parâmetros de amostragem e tempos medidos

- **Fixados** nos jobs registrados da GW250114 (`RINGDOWN_5SIGMA_V1_1_3.json` → `pe_jobs`; `bis/015/E2_PE_JOBS_ALLOCATION_015_V4.json`) [DECLARADO]: bilby `Dynesty` com `sample='rwalk'` (v1 l.225–228), `nlive=512` (C1) ou `1024` (H1), `walks=50`, `dlogz=0,1`, `maxcall` 3,0 M / 5,74 M / 6,45 M, `workers (npool)=24` (≤ 28), ESS mínimo 100, ≥ 1000 amostras de posterior, sementes 15260302/303/404, `wall_budget_seconds=28800`; janela 16 s, 4096 Hz, geração 8192 Hz, banda 20–1024 Hz, referência 20 Hz, PSD 256 s com segmentos de 8 s, exclusão 16 s, roll-off 0,2 s; priors `m1∈[15,100]`, `m2∈[10,100]`, `q≥0,125`, `χ∈±0,99`, **`d_L ∈ [100, 2000] Mpc`**, `dtau220∈[−0,8; 2,0]`; só `dtau220` livre (`dtau440=domega440=0` fixos).
- **Tempos medidos (recibos, GW250114, calibração NOT_BLIND, SNR ≈ 78)** [DECLARADO; lidos e recomputados por mim em `estimativa_tempo.py`]:

| job | chamadas | parede | CPU (usuário+sistema) | CPU/chamada | núcleos efetivos (de 24) | Δlogz final | ESS | status |
|---|---|---|---|---|---|---|---|---|
| `…_S220` (nlive 512) | 3 000 506 | 13 557 s (3,77 h) | 184 084 s (51,1 h) | 0,0614 s | 13,6 (57 %) | **425,3** | 1,0 | `PARTIAL_MAXCALL_NOT_ACCEPTED` |
| `…_S220_C1` (nlive 512) | 5 739 196 | 23 072 s (6,41 h) | 356 147 s (98,9 h) | 0,0621 s | 15,4 (64 %) | **177,0** | 1,0 | `PARTIAL_MAXCALL_NOT_ACCEPTED` |
| `…_S220_H1` (nlive 1024) | — | 145 s | — | — | — | — | — | morto (SIGKILL/RuntimeError) |

  [REAL, lido hoje do `…_result.hdf5` só pela contagem de linhas de `nested_samples`, sem abrir colunas]: S220 fez ≈ 9 500 iterações a ≈ **300 chamadas/iteração**; C1 ≈ 11 700 iterações a ≈ **470–490 chamadas/iteração**. A INIT003 sintética (SNR 20, nlive 256, walks 25, 1 worker): 9738 chamadas, 857,9 s, Δlogz 57,3 [DECLARADO]. **Nenhuma PE de modelo completo convergiu na casa.**

### (g) Guardas e contratos (resumo)

(1) `run_controlled` + `validate_launch` (acima); (2) `checked_registration` encadeada (testemunha, ativação, 4 revisões, árvore de código, runtime pinado, relógio) — **vencida**; (3) `check_blind_activation` — recibo ausente; (4) `temporal_contract` — satisfeito com `analysis_time_contract={start_GPS, duration_s, roll_off_s}` e `geocent_time` (janela de 16 s basta); (5) `pseob_source` (v112 l.88–122) recusa se `1+dtau440 > 2·max(1, 1+dtau220)` e exige `generation_maximum_frequency_hz` e `generation_sample_rate_hz` com `fmax = fs/2` e grade zero-origem compatível (`generation_grid` l.36–50); EDOM (waveform `None`) é registrado em `EDOM_LOG.jsonl`, nunca vira rejeição silenciosa (l.52–61 e 116–118); (6) `pe_runner.validate_config` (v1 l.51–85; v112 l.75–78): priors exatos, classes `Uniform/Sine/Cosine/Constraint`, sem checkpoint, sem plots; (7) conversão e cosmologia pinadas (`remnant_conversion` l.16–23).

---

## 3. Teste de fumaça (WSL, sem dado real) — [REAL]

`/opt/lal_env/bin/python` 3.12.3, bilby 2.8.2, dynesty 3.1.0, lalsimulation 6.2.1, numpy 2.5.3, scipy 1.18.1, h5py 3.16.0; 48 núcleos, 125 GB. Importei **cópias byte-idênticas** (sha256 conferido) de `pseob_source.py` e `temporal_contract.py` da árvore v1_1_2 e gerei formas de onda com `pseob_frequency_domain` (grade 0–2048 Hz, Δf = 1/32 Hz, 65 537 bins; geração 8192 Hz; banda 20–1024 Hz; M = (35, 30) M☉, χ = (0,3; 0,1), D_L = 500 Mpc, `analysis_time_contract` = 32 s com roll-off 0,2 s):

| chamada | dtau220 | tempo (parede) | norma² de h₊ |
|---|---|---|---|
| 1 (inclui carga preguiçosa de LAL) | 0 | **1,021 s** | 1,5585e−42 |
| 2 | −0,40 | **0,0647 s** | 1,5366e−42 |
| 3 (repetição) | −0,40 | 0,0663 s | idêntica |
| 4 | +0,30 | 0,0696 s | 1,5738e−42 |

CPU total do teste: 0,86 s. A norma varia com `dtau220` (razão 0,986 entre −0,40 e GR): a deformação chega ao `pSEOBNRv4HM_PA`. **`pSEOBNRv4HM_PA` está disponível e funcional; não é parede.** O custo por forma de onda (0,065 s) bate com o recibo da R5 (0,0848 s CPU/fonte, DECLARADO) e com o piloto (0,0653 s/chamada). Arquivos: `smoke\smoke_pseob.py`, `smoke\smoke_pseob_saida.txt`.

---

## 4. Inventário (hashes lidos do disco por script)

Gerado por `inventario_D_29out.py` (hash do próprio script no JSON). Completo em `INVENTARIO_D_29out.json`; abaixo a tabela inteira (113 arquivos).

### 4.1 Eventos do conjunto D10 — metadados (nenhum valor de deformação)

Fontes: catálogo residente (GPS, z), V1 (SNR, M_f,det, χ_f, k, δ_pred = informação cega), `dq_meta_D_v2.json` (DQ), `PROJECAO_PODER_D_planejamento.json`. D_L: Planck18 plano, integração numérica minha. **[REAL] 5 de 10 eventos têm D_L > 2000 Mpc** (2241, 2576, 3347, 4009, 4852): o prior de distância dos jobs da GW250114 (`[100, 2000]`) **truncaria metade do conjunto**.

| evento | GPS (catalogo) | SNR rede | z | D_L (Mpc, Planck18 plano) | M_f,det (V1) | chi_f (V1) | k(chi_f) | delta_pred (V1) | sigma_i proj. | H1: pre-run OK (s) | L1: pre-run OK (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| GW230919_215712 | 1379195850.0 | 16.8 | 0.25 | 1301 | 58.4 | 0.75 | 31.56 | -0.4282 | 0.287 | 1773 | 3010 |
| GW240513_183302 | 1399660400.9 | 14.5 | 0.40 | 2241 | 54.8 | 0.74 | 31.25 | -0.4197 | 0.329 | 3944 | 3944 |
| GW240920_073424 | 1410852882.5 | 14.0 | 0.27 | 1421 | 46.6 | 0.64 | 28.92 | -0.3527 | 0.341 | 2058 | 2058 |
| GW240923_204006 | 1411159224.1 | 13.6 | 0.65 | 4009 | 126.0 | 0.70 | 30.16 | -0.3895 | 0.350 | 1200 | 1200 |
| GW241111_111552 | 1415358970.6 | 16.3 | 0.29 | 1542 | 55.6 | 0.72 | 30.67 | -0.4040 | 0.295 | 568 | 2546 |
| GW241130_034908 | 1416973766.6 | 13.8 | 0.36 | 1981 | 70.1 | 0.71 | 30.41 | -0.3966 | 0.345 | 3518 | 451 |
| GW241210_060606 | 1417845984.8 | 13.4 | 0.45 | 2576 | 69.3 | 0.70 | 30.16 | -0.3895 | 0.355 | 3288 | 3288 |
| GW250104_015122 | 1419990700.3 | 12.1 | 0.76 | 4852 | 133.0 | 0.73 | 30.95 | -0.4117 | 0.391 | 1700 | 1700 |
| GW250109_010541 | 1420419959.5 | 13.1 | 0.56 | 3347 | 97.4 | 0.66 | 29.29 | -0.3640 | 0.363 | 879 | 879 |
| GW250118_170523 | 1421255141.2 | 13.9 | 0.35 | 1917 | 86.8 | 0.73 | 30.95 | -0.4117 | 0.343 | 477 | 477 |


### 4.2 Strain dos 10 eventos (sha256 dos bytes; amostras não abertas)

| evento | det | hdf5 bytes | hdf5 sha16 (confere manifesto) | npz sha16 (confere manifesto) |
|---|---|---|---|---|
| GW230919_215712 | H1 | 90326907 | `3b705f5c7725fa86` (sim) | `f76ea5f0bdccdfcc` (sim) |
| GW230919_215712 | L1 | 128720937 | `a21f860838440ec5` (sim) | `dda38ae09bec4104` (sim) |
| GW240513_183302 | H1 | 128614253 | `8614ec94882c37d4` (sim) | `b23135e4176fb87b` (sim) |
| GW240513_183302 | L1 | 128669990 | `1b21deafa7b8f6f9` (sim) | `0673a469df995a2c` (sim) |
| GW240920_073424 | H1 | 129025218 | `858adc4e70653a31` (sim) | `67ca88fe6a141f2f` (sim) |
| GW240920_073424 | L1 | 128703893 | `43a4eed73d668be5` (sim) | `767035c8e86d780d` (sim) |
| GW240923_204006 | H1 | 109155373 | `140901292e9e5f7e` (sim) | `453e77ec6245a03c` (sim) |
| GW240923_204006 | L1 | 128720271 | `7a73e0ce19bbc4dc` (sim) | `aa7fd607183c4932` (sim) |
| GW241111_111552 | H1 | 67405696 | `af9c6f5b7395d5fc` (sim) | `70ee1caab4b13310` (sim) |
| GW241111_111552 | L1 | 128728116 | `f2f139ce0054c3f8` (sim) | `84746ffcc0c333a7` (sim) |
| GW241130_034908 | H1 | 128626946 | `fa34aebfeeea9f1b` (sim) | `142ffcd3147f27e8` (sim) |
| GW241130_034908 | L1 | 32996556 | `4d2c44617b42aab3` (sim) | `e7bd502ed4cbfa10` (sim) |
| GW241210_060606 | H1 | 128617259 | `e48561bb566df5ff` (sim) | `82835c6bd17e7cc4` (sim) |
| GW241210_060606 | L1 | 128708250 | `19847f5cb52d8825` (sim) | `af9b46d6112d9da6` (sim) |
| GW250104_015122 | H1 | 98250146 | `56235463402d777d` (sim) | `e2c4c2444c5e1325` (sim) |
| GW250104_015122 | L1 | 85181762 | `93ceeb394ed9d2cd` (sim) | `e3497e43509a90f6` (sim) |
| GW250109_010541 | H1 | 128628251 | `a7cc36373822d55e` (sim) | `d7672fb556b15f4c` (sim) |
| GW250109_010541 | L1 | 128717741 | `2f7dfe282b3921a3` (sim) | `c5293bfa3ffac88e` (sim) |
| GW250118_170523 | H1 | 128623707 | `e2cfc656b499fb73` (sim) | `a07a0f9b64d24f17` (sim) |
| GW250118_170523 | L1 | 128726427 | `9d475654fd2ed79d` (sim) | `078c5bb4d9ff12c1` (sim) |


### 4.3 Projeção de poder de PLANEJAMENTO de D — [DERIVED]

Entradas: SNR de rede GWOSC e δ_pred por evento (já no V1), ajuste σ_τ(SNR) da bancada para os 31 do GWTC-5.0 (`ln σ = 1,4166 − 0,9450 ln ρ`, resíduo ln 0,2177; NOT_BLIND, planejamento), σ_sys ∈ {0; 0,029; 0,038} do V1. **Não inclui** jackknife (σ_usado = max(σ_comb, σ_jack) só pode piorar) nem a diferença v4HM-PA × v5PHM, e usa SNR de **rede**, não de ringdown. Não lê nem imprime nenhum valor central de deformação.

| conjunto | sigma_sys | informacao | n | delta_pred ponderado | sigma_comb | poder = abs(delta_pred)/sigma_comb |
|---|---|---|---|---|---|---|
| D10_sem_hold | 0.000 | mediana | 10 | -0.3985 | 0.1062 | 3.75 |
| D10_sem_hold | 0.000 | esperada | 10 | -0.3985 | 0.1013 | 3.93 |
| D10_sem_hold | 0.029 | mediana | 10 | -0.3985 | 0.1066 | 3.74 |
| D10_sem_hold | 0.029 | esperada | 10 | -0.3985 | 0.1017 | 3.92 |
| D10_sem_hold | 0.038 | mediana | 10 | -0.3985 | 0.1069 | 3.73 |
| D10_sem_hold | 0.038 | esperada | 10 | -0.3985 | 0.1020 | 3.91 |
| D14_com_holds | 0.000 | mediana | 14 | -0.4005 | 0.0906 | 4.42 |
| D14_com_holds | 0.000 | esperada | 14 | -0.4005 | 0.0864 | 4.64 |
| D14_com_holds | 0.029 | mediana | 14 | -0.4005 | 0.0909 | 4.41 |
| D14_com_holds | 0.029 | esperada | 14 | -0.4005 | 0.0867 | 4.62 |
| D14_com_holds | 0.038 | mediana | 14 | -0.4005 | 0.0911 | 4.39 |
| D14_com_holds | 0.038 | esperada | 14 | -0.4005 | 0.0870 | 4.60 |


**Calibração do modelo [REAL]:** aplicado aos 31 eventos do A31 (SNR do próprio ajuste), o mesmo `σ(ρ)` dá σ_comb = **0,0355** (mediana) contra **0,0336** do V1/`sigma_comb_A31` — erro de 6 %. **Cenário «D se comporta como a calibração A»** (δ̄ = +0,072 contra δ̄_pred = −0,3985): z_excl = 0,4705/σ_comb ≈ **4,4–4,6** (D10) e 5,2–5,5 (D14), e em ambos o poder fica < 5, logo a regra 3 devolve `NOT_FALSIFIED_UNDERPOWERED` antes que a regra 5 possa dar `FALSIFIED_AT_5SIGMA`. σ_comb máximo para poder ≥ 5 (D10): 0,0797; o fator de informação que falta é **1,78×** sobre a projeção central. Para comparação, o V1 declara para A (31 eventos) 11,4σ, B 6,4σ, C 6,5σ.

### 4.4 Tabela de arquivos

| sha16 | bytes | estatuto do conteudo | papel | caminho |
|---|---|---|---|---|
| `86f98fcc124dd9ca` | 138727 | REAL | pre-registro V1 congelado (JSON) | `I/Bancada_Um/investigacao/preregistro_ramo_b_05out/PREREGISTRO_RAMO_B_RINGDOWN_V1.json` |
| `294b88a3632c1cea` | 102303 | REAL | pre-registro V1 congelado (MD) | `I/Bancada_Um/investigacao/preregistro_ramo_b_05out/PREREGISTRO_RAMO_B_RINGDOWN_V1.md` |
| `16a3df7a77f439b5` | 1708 | REAL | hashes do V1 | `I/Bancada_Um/investigacao/preregistro_ramo_b_05out/V1_RAMO_B_HASHES.json` |
| `126adc100753c2ca` | 360514 | REAL | poder cego (so sigma e spin) do A/B/C | `I/Bancada_Um/investigacao/preregistro_ramo_b_05out/PODER_CEGO_RAMO_B_v2.json` |
| `e4c99ccc1d8a506e` | 16812 | REAL | script do poder cego | `I/Bancada_Um/investigacao/preregistro_ramo_b_05out/poder_cego_ramo_b_v2.py` |
| `48bf6267047acdd5` | 93848 | REAL | gerador do V1 | `I/Bancada_Um/investigacao/preregistro_ramo_b_05out/gerar_preregistro_ramo_b_05out.py` |
| `0a636d439a03f016` | 7697 | REAL | funcao de veredito da Fase 6 (ECO V3): empilhar() + veredito() | `I/Bancada_Um/bancada/gw_stack.py` |
| `741103f99a7adccc` | 8607 | REAL | constantes CR da Fase 6 (min_eventos=10, poder_min=5, z_excl=5, sist_max=0.3) | `I/Bancada_Um/investigacao/fase6_eco_radical_01out/preregistro_fase6.py` |
| `7d4407fde07c6692` | 3121 | REAL | e2_code :: 013-bis v1 (27/09) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/blinding.py` |
| `a6066c933d29f13f` | 7979 | REAL | e2_code :: 013-bis v1 (27/09) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/fetch_registered.py` |
| `12017563c123df76` | 7907 | REAL | e2_code :: 013-bis v1 (27/09) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/injection_design.py` |
| `9fa748e79ba55312` | 3269 | REAL | e2_code :: 013-bis v1 (27/09) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/null_campaign.py` |
| `1b6bf00beced255d` | 5544 | REAL | e2_code :: 013-bis v1 (27/09) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/null_runner.py` |
| `6712610a0392abe6` | 19622 | REAL | e2_code :: 013-bis v1 (27/09) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/pe_runner.py` |
| `2c9a053177bd2671` | 4358 | REAL | e2_code :: 013-bis v1 (27/09) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/pseob_source.py` |
| `3cb2d9ef0672ccdf` | 15710 | REAL | e2_code :: 013-bis v1 (27/09) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/registration_guard.py` |
| `87604de5c8fa7139` | 3406 | REAL | e2_code :: 013-bis v1 (27/09) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/remnant_conversion.py` |
| `dfcf9491ab98f9d3` | 2206 | REAL | e2_code :: 013-bis v1 (27/09) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/route_iv_null.py` |
| `7b5dd6484014942e` | 5991 | REAL | e2_code :: 013-bis v1 (27/09) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/run_controlled.py` |
| `a52faf32e8808832` | 4560 | REAL | e2_code :: 013-bis v1 (27/09) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/strain_io.py` |
| `be0fa6d4b678993e` | 4074 | REAL | e2_code :: 013-bis v1 (27/09) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/synthetic_null.py` |
| `c8f4ecbc28d4312e` | 1859 | REAL | e2_code :: 013-bis v1 (27/09) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code/temporal_contract.py` |
| `9ea5f9b65fba907d` | 5147 | REAL | e2_code_v1_1 :: 015 v1.1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1/blinding.py` |
| `a6066c933d29f13f` | 7979 | REAL | e2_code_v1_1 :: 015 v1.1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1/fetch_registered.py` |
| `12017563c123df76` | 7907 | REAL | e2_code_v1_1 :: 015 v1.1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1/injection_design.py` |
| `4dfac23c0f926178` | 3282 | REAL | e2_code_v1_1 :: 015 v1.1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1/null_campaign.py` |
| `e29c37ab15ec720d` | 6248 | REAL | e2_code_v1_1 :: 015 v1.1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1/null_runner.py` |
| `11c5588fabf5ae0e` | 22293 | REAL | e2_code_v1_1 :: 015 v1.1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1/pe_runner.py` |
| `58cb22bbe37f9207` | 7505 | REAL | e2_code_v1_1 :: 015 v1.1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1/pseob_source.py` |
| `ce3db9a0073c18ba` | 31436 | REAL | e2_code_v1_1 :: 015 v1.1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1/registration_guard.py` |
| `87604de5c8fa7139` | 3406 | REAL | e2_code_v1_1 :: 015 v1.1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1/remnant_conversion.py` |
| `dfcf9491ab98f9d3` | 2206 | REAL | e2_code_v1_1 :: 015 v1.1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1/route_iv_null.py` |
| `7b5dd6484014942e` | 5991 | REAL | e2_code_v1_1 :: 015 v1.1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1/run_controlled.py` |
| `a52faf32e8808832` | 4560 | REAL | e2_code_v1_1 :: 015 v1.1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1/strain_io.py` |
| `be0fa6d4b678993e` | 4074 | REAL | e2_code_v1_1 :: 015 v1.1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1/synthetic_null.py` |
| `c8f4ecbc28d4312e` | 1859 | REAL | e2_code_v1_1 :: 015 v1.1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1/temporal_contract.py` |
| `9ea5f9b65fba907d` | 5147 | REAL | e2_code_v1_1_2 :: 015 v1.1.2 (ultima) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1_2/blinding.py` |
| `a6066c933d29f13f` | 7979 | REAL | e2_code_v1_1_2 :: 015 v1.1.2 (ultima) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1_2/fetch_registered.py` |
| `12017563c123df76` | 7907 | REAL | e2_code_v1_1_2 :: 015 v1.1.2 (ultima) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1_2/injection_design.py` |
| `4dfac23c0f926178` | 3282 | REAL | e2_code_v1_1_2 :: 015 v1.1.2 (ultima) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1_2/null_campaign.py` |
| `e29c37ab15ec720d` | 6248 | REAL | e2_code_v1_1_2 :: 015 v1.1.2 (ultima) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1_2/null_runner.py` |
| `11c5588fabf5ae0e` | 22293 | REAL | e2_code_v1_1_2 :: 015 v1.1.2 (ultima) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1_2/pe_runner.py` |
| `58cb22bbe37f9207` | 7505 | REAL | e2_code_v1_1_2 :: 015 v1.1.2 (ultima) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1_2/pseob_source.py` |
| `4dd3005ed34b30a2` | 31781 | REAL | e2_code_v1_1_2 :: 015 v1.1.2 (ultima) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1_2/registration_guard.py` |
| `87604de5c8fa7139` | 3406 | REAL | e2_code_v1_1_2 :: 015 v1.1.2 (ultima) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1_2/remnant_conversion.py` |
| `dfcf9491ab98f9d3` | 2206 | REAL | e2_code_v1_1_2 :: 015 v1.1.2 (ultima) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1_2/route_iv_null.py` |
| `7b5dd6484014942e` | 5991 | REAL | e2_code_v1_1_2 :: 015 v1.1.2 (ultima) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1_2/run_controlled.py` |
| `a52faf32e8808832` | 4560 | REAL | e2_code_v1_1_2 :: 015 v1.1.2 (ultima) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1_2/strain_io.py` |
| `be0fa6d4b678993e` | 4074 | REAL | e2_code_v1_1_2 :: 015 v1.1.2 (ultima) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1_2/synthetic_null.py` |
| `c8f4ecbc28d4312e` | 1859 | REAL | e2_code_v1_1_2 :: 015 v1.1.2 (ultima) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code_v1_1_2/temporal_contract.py` |
| `7cdfe269fd93958d` | 9020 | REAL | emenda 015 do source/runner (grade de geracao, EDOM) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/015/amend_source_runner.py` |
| `91b3197c5af3cbd4` | 7557 | REAL | emenda 015 relogio/nulos | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/015/amend_clock_and_nulls.py` |
| `66be75bee3d995c2` | 6491 | REAL | emenda 015 leitura/falha | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/015/amend_reading_and_failure.py` |
| `4f54400b10653cc0` | 10565 | REAL | T05 diagnosticos NAO-CEGOS | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/015/t05/measure.py` |
| `3d959ac7ce751bc6` | 273438 | REAL | T05 resultado | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/015/t05/RESULT.json` |
| `93f7ee3fcd840b36` | 3318 | REAL | R5 manifesto de entradas da qualificacao de fonte | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/015/t03/R5/INPUT_MANIFEST.json` |
| `d4a94b0dbcbcf534` | 964 | REAL | R5 qualificacao de fonte (1015 waveforms) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/015/t03/R5/generation_4096/RESULT.json` |
| `4ff0d4e17fac4ccc` | 11864 | REAL | alocacao de jobs 015 V4 (GW250114) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/015/E2_PE_JOBS_ALLOCATION_015_V4.json` |
| `e1be6b0409720c68` | 183005 | REAL | registro/orcamento da cadeia 013-bis/015 | `CP/Chatgpt/ORDEM_013_RINGDOWN/RINGDOWN_5SIGMA_V1.json` |
| `96571187bec3c1d7` | 228439 | REAL | registro/orcamento da cadeia 013-bis/015 | `CP/Chatgpt/ORDEM_013_RINGDOWN/RINGDOWN_5SIGMA_V1_1.json` |
| `75b1884d18240ddb` | 230799 | REAL | registro/orcamento da cadeia 013-bis/015 | `CP/Chatgpt/ORDEM_013_RINGDOWN/RINGDOWN_5SIGMA_V1_1_1.json` |
| `a02c4224b0c832a8` | 231927 | REAL | registro/orcamento da cadeia 013-bis/015 | `CP/Chatgpt/ORDEM_013_RINGDOWN/RINGDOWN_5SIGMA_V1_1_2.json` |
| `74a2c8b656244ff4` | 233331 | REAL | registro/orcamento da cadeia 013-bis/015 | `CP/Chatgpt/ORDEM_013_RINGDOWN/RINGDOWN_5SIGMA_V1_1_3.json` |
| `892e416585062eef` | 126793 | REAL | registro/orcamento da cadeia 013-bis/015 | `CP/Chatgpt/ORDEM_013_RINGDOWN/ORCAMENTO_40H.json` |
| `2b3cfefd17cb8f3d` | 1536 | REAL | recibo/manifesto da bancada | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/PART_B_BUDGET_START.json` |
| `087ede2068e14d70` | 452 | REAL | recibo/manifesto da bancada | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/PART_015_BUDGET_START.json` |
| `840d3087a0c3ad1f` | 1546 | REAL | recibo/manifesto da bancada | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/FINAL_DELIVERY_RECEIPT.json` |
| `2611d2d895d37645` | 2358 | REAL | recibo/manifesto da bancada | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/E3_PILOT_FAILURE_AUDIT_V1.json` |
| `56906841f9202098` | 5148 | REAL | recibo/manifesto da bancada | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/C3_C6_TIMING_013BIS.json` |
| `98bc0408e7fec14a` | 48947 | REAL | recibo/manifesto da bancada | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/E0_SNR_INFORMATION_FIT.json` |
| `df95b7567c2f07df` | 5727 | REAL | recibo/manifesto da bancada | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/E0_SNR_FIT_REVIEW.md` |
| `ef3d21edfd3a9258` | 614 | REAL | recibo/manifesto da bancada | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/B1_DELIVERY_MANIFEST.json` |
| `5e40faf24890b5cb` | 4386 | REAL | recibo/manifesto da bancada | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/B2_DELIVERY_MANIFEST.json` |
| `1ceeafc2987088a3` | 2568 | REAL | recibo/manifesto da bancada | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/B3_DELIVERY_MANIFEST.json` |
| `a431926241035a2a` | 2756 | REAL | recibo/manifesto da bancada | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/B4_TEST_DELIVERY_MANIFEST.json` |
| `985275ce9928f487` | 3339 | REAL | recibo/manifesto da bancada | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/B5_DELIVERY_MANIFEST.json` |
| `f28f4acc9e1c6b06` | 29329 | REAL | custo/sistematica E0 (escalar) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e0_core/COST_RECEIPT.json` |
| `6d70759dbfa8bbef` | 4188 | REAL | custo/sistematica E0 (escalar) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e0_core/SYSTEMATICS_COST.json` |
| `e3ff1ff9f8201714` | 2728 | REAL | custo/sistematica E0 (escalar) | `CP/Chatgpt/ORDEM_013_RINGDOWN/bis/e0_core/SYSTEMATICS_ADENDO.md` |
| `8536ecf82cad76ad` | 829 | REAL | piloto GW250114 (calibracao NOT_BLIND; nao e evento de D): E3_PSEOB_PILOT_V2_S220 | `CP/Chatgpt/ORDEM_013_RINGDOWN/cache/E3_PSEOB_PILOT_V2_S220/CONTROLLER.json` |
| `3d51335d5ee9fdfd` | 3217 | REAL | piloto GW250114 (calibracao NOT_BLIND; nao e evento de D): E3_PSEOB_PILOT_V2_S220 | `CP/Chatgpt/ORDEM_013_RINGDOWN/cache/E3_PSEOB_PILOT_V2_S220/PRIVATE_CONVERGENCE.json` |
| `26ed3aedd10d0d39` | 832 | REAL | piloto GW250114 (calibracao NOT_BLIND; nao e evento de D): E3_PSEOB_PILOT_V2_S220_C1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/cache/E3_PSEOB_PILOT_V2_S220_C1/CONTROLLER.json` |
| `c1d291f30c44212e` | 3231 | REAL | piloto GW250114 (calibracao NOT_BLIND; nao e evento de D): E3_PSEOB_PILOT_V2_S220_C1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/cache/E3_PSEOB_PILOT_V2_S220_C1/PRIVATE_CONVERGENCE.json` |
| `e288aad2d4ad8d9c` | 877 | REAL | piloto GW250114 (calibracao NOT_BLIND; nao e evento de D): E3_PSEOB_PILOT_V2_S220_H1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/cache/E3_PSEOB_PILOT_V2_S220_H1/CONTROLLER.json` |
| `47c8438f89094ee7` | 867 | REAL | piloto GW250114 (calibracao NOT_BLIND; nao e evento de D): E3_PSEOB_PILOT_V2_S220_H1 | `CP/Chatgpt/ORDEM_013_RINGDOWN/cache/E3_PSEOB_PILOT_V2_S220_H1/FAILURE.json` |
| `192d72c068a83c9c` | 2962 | DECLARADO | preparacao Codex ORDEM 018 | `CP/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/MANIFESTO_CONJUNTO_D.json` |
| `946e0a64d6c8a8d4` | 79557 | DECLARADO | preparacao Codex ORDEM 018 | `CP/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/PROPOSTA_MANIFESTO_METADATA_D.json` |
| `631429ead39df3c5` | 9322 | DECLARADO | preparacao Codex ORDEM 018 | `CP/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/NOTA_CONJUNTO_D.md` |
| `7d42ad140e895211` | 13457 | DECLARADO | preparacao Codex ORDEM 018 | `CP/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/PLANO_PILOTO_SINTETICO_SO220.json` |
| `05455249436c0376` | 14656 | DECLARADO | preparacao Codex ORDEM 018 | `CP/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/AUDITORIA_INSTRUMENTO_SO220.json` |
| `12f50519559994fd` | 14878 | DECLARADO | preparacao Codex ORDEM 018 | `CP/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/p3_scientific_design_proposal/PROPOSTA_CONTINUACAO.md` |
| `10db03e08226a820` | 16014 | DECLARADO | preparacao Codex ORDEM 018 | `CP/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/p3_startup_pin_preparation/driver_p3.py` |
| `19c7f7cde449470a` | 5022 | DECLARADO | preparacao Codex ORDEM 018 | `CP/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/p3_startup_pin_preparation/launch_p3.py` |
| `5e696af0f8d669e4` | 365 | DECLARADO | preparacao Codex ORDEM 018 | `CP/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/p3_startup_pin_preparation/ROOT_DECISION.json` |
| `d8c457a2c78bb067` | 1297 | DECLARADO | preparacao Codex ORDEM 018 | `CP/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/p3_startup_pin_preparation/COMANDO_CANDIDATO.json` |
| `3b8192167a561d91` | 1721 | DECLARADO | preparacao F4.2 (07/10) | `CP/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F4.2/PREPARACAO_GATE.md` |
| `98512f36002a848a` | 1326 | DECLARADO | preparacao F4.2 (07/10) | `CP/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F4.2/RESULTADO.json` |
| `9e54b47780dab101` | 47 | INPUT | autorizacao verbatim do operador, 29/10 (registrada pela gerencia, Mapa seq 1545) | `CP/work/cunhagens_13out/OPERADOR_29out_autoriza_conjunto_D_verbatim.txt` |
| `52635ea9d1324f10` | 4135 | DECLARADO | registro da autorizacao no Mapa (gerencia c1, 29/10) | `CP/work/conjunto_D_20261029/rota_mapa_autorizacao_D_29out.json` |
| `a795cf04ca3b2f6a` | 253528 | REAL | manifesto de strain 32s/4096s (336 OK) | `I/Bancada_Um/fontes_externas/gwosc_o4/GWOSC_O4_32S_V1.manifest.json` |
| `e6a0ba6a870e2a40` | 99817 | REAL | catalogo residente (GPS) | `I/Bancada_Um/investigacao/fase6_eco_radical_01out/catalogo_v3.csv` |
| `55be29abac26d1d0` | 6048 | REAL | reconciliacao 44/14/10 | `CP/work/cadeia_de_selo/v386/ramo_b/pre_registro/RECONCILIACAO_CONJUNTO_D.json` |
| `21adcceb7d5c4be5` | 54494 | REAL | inventario de dados na casa | `CP/work/cadeia_de_selo/v386/ramo_b/dados_na_casa/INVENTARIO_DADOS_NA_CASA_RAMO_B_v386.json` |
| `5a9805a9d3b43740` | 1866 | REAL | artefato desta sessao (29/10) | `CP/work/conjunto_D_20261029/smoke/smoke_pseob.py` |
| `57833952b8b7ca60` | 946 | REAL | artefato desta sessao (29/10) | `CP/work/conjunto_D_20261029/smoke/smoke_pseob_saida.txt` |
| `5a8375936ce46d25` | 3221 | REAL | artefato desta sessao (29/10) | `CP/work/conjunto_D_20261029/smoke/dq_meta.py` |
| `d4b8d141888f92fe` | 2066 | REAL | artefato desta sessao (29/10) | `CP/work/conjunto_D_20261029/smoke/dq_meta2.py` |
| `a0e4250f69b671b9` | 5925 | REAL | artefato desta sessao (29/10) | `CP/work/conjunto_D_20261029/smoke/dq_meta_D_v2.json` |
| `423f82273ae00096` | 1009 | REAL | artefato desta sessao (29/10) | `CP/work/conjunto_D_20261029/smoke/bounds_corners.py` |
| `1ea886c58707ddfe` | 4120 | REAL | artefato desta sessao (29/10) | `CP/work/conjunto_D_20261029/projecao_poder_D.py` |
| `89958dd17baa513d` | 5638 | REAL | artefato desta sessao (29/10) | `CP/work/conjunto_D_20261029/PROJECAO_PODER_D_planejamento.json` |
| `58cb22bbe37f9207` | 7505 | REAL | artefato desta sessao (29/10) | `CP/work/conjunto_D_20261029/copias_somente_leitura_v1_1_2/pseob_source.py` |
| `c8f4ecbc28d4312e` | 1859 | REAL | artefato desta sessao (29/10) | `CP/work/conjunto_D_20261029/copias_somente_leitura_v1_1_2/temporal_contract.py` |


---

## 5. Pipeline passo a passo

Convenções: `WSLPY` = `wsl.exe -d Ubuntu-24.04 -- bash -lc "cd '/mnt/c/IALD/Central de Patentes/work/conjunto_D_20261029/codigo_D' && /opt/lal_env/bin/python -B …"`. Saídas privadas de PE: `C:\Users\rotol\.iald_privado\conjunto_D_20261029\pe\<job>\` (fora do git e fora de `work\`, que é público). «EXISTE» = já está em disco e foi lido; «A ESCREVER» = não existe (§6).

**Passo 0 — Pré-condições (gerência/operador).** (0.1) Ordem de 29/10 verbatim + sha256 e alcance (só o par; F2b retirado ao lado) [JÁ REGISTRADO, seq 1545]; falta fixar o orçamento de CPU/parede (D2). (0.2) Conferir o V1 por hash antes de tudo [EXISTE]:
`sha256sum "/c/IALD/Bancada_Um/investigacao/preregistro_ramo_b_05out/PREREGISTRO_RAMO_B_RINGDOWN_V1.json"` deve dar `86f98fcc124dd9cae04fdb06bd10c14175893253d5b139496bd4c05f109feee0` (e o `.md` `294b88a3…`). (0.3) Consultar o Mapa: `C:\Python314\python.exe -X utf8 C:\IALD\MAPA_DE_ROTAS\rotas.py consultar "ringdown"`.

**Passo 1 — Congelar os 10 eventos (antes de qualquer PE).** `WSLPY congelar_D.py --gerar` [A ESCREVER]. Escreve `00_congelamento\MANIFESTO_D_CONGELADO.json` + `JOBS_D_V1.json` e imprime os sha256. Conteúdo (é a lista do contrato F4.2 de 07/10): sha256 do V1 (JSON+MD); os 10 eventos, GPS, `segment_start = GPS − 12,0`, duração 16 s; caminho + sha256 dos 20 HDF5 (valores da tabela 4.2); DQ exigido `DATA, CBC_CAT1..3` e `NO_CBC/BURST/DETCHAR/STOCH_HW_INJ`; PSD = primeiro bloco OK de 256 s (Welch 8 s, Hann 50 %, mediana), exclusão 16 s; priors (com `d_L` até ≥ 10 000 Mpc, §6-D1); sampler, sementes, tetos de chamadas e parede; regra de repetição (§6-D5); hash da árvore `codigo_D`; hash de `estimador_ramo_b_v1.py` e `veredito_ramo_b.py`; compromisso da semente (passo 2); `σ_sys` (0,029 e 0,038, V1) e as constantes CR de `preregistro_fase6.py` l.42 (`min_eventos=10, poder_min=5, z_excl=5, sistematica_max_relativa=0,3`). **Registrar o sha256 do manifesto no Mapa** (`rotas.py registrar`, livro encadeado = carimbo de tempo) **e** num arquivo de testemunho. Holds (GW240515, GW240615, GW240930, GW241102) e os 8 pendentes **ficam fora** (V1 l.153); só entram com método de resolução de DQ fixado por hash — não neste plano.

**Passo 2 — Semente de cegueira.** `WSLPY blind_seed_D.py --criar` [A ESCREVER]: 32 bytes de `os.urandom` em `~/.iald_privado/conjunto_D_20261029/BLIND_SEED_D.bin` (modo 0600), imprime **só** o sha256 (o compromisso, que vai ao manifesto); etiqueta do HMAC `'RAMOB_V1_D:'` no lugar de `'013BIS:'`. Ninguém imprime nem põe a semente em work/túnel/log.

**Passo 3 — Qualificação F4.1 do instrumento (sem dado de D).** (3.1) já feito: fumaça (§3). (3.2) `WSLPY run_controlled_D.py --job F41_SYN_GR` e `--job F41_SYN_RB` [A ESCREVER o runner; reaproveita `pe_runner` v112]: 2 PE sintéticas (injeção GR e injeção com `dtau220 = −0,39`) em ruído gaussiano de PSD analítica, SNR de rede 14, parâmetros no centro de D (35+30 M☉ de fonte, z≈0,4, χ_eff 0,1), **com a mesma configuração de amostragem de D**. Mede `chamadas até convergir`, `s/chamada`, eficiência de núcleos e **dimensiona o orçamento de D**. Critérios herdados da proposta A02 (`PROPOSTA_CONTINUACAO.md`): Δlogz < 0,1 antes de somar os pontos vivos, ESS ≥ 100, sem EDOM dentro da região do posterior, verdade em [q05; q95] com W90 < 2,52. **Porta:** só lança D se F4.1 convergir dentro do teto; se não, parar e decidir orçamento/sampler (nenhum olhar em D). Pode começar com 1 PE (GR) para medir a escala.

**Passo 4 — PE cega dos 10 eventos.** `WSLPY lancar_fila_D.py --conjunto D10 --concorrentes 2 --workers 24` [A ESCREVER], que chama `run_controlled_D.py --job D_<evento>` (modo `blind_test`) em fila, mantendo 2 PE × 24 workers nos 48 núcleos. Cada job grava `LAUNCH_CONTEXT/CLAIM`, `PRIVATE.log`, `EDOM_LOG.jsonl`, `PRIVATE_CONVERGENCE.json` e, **se convergiu**, `ANALYST_OUTPUT.json` (colunas deslocadas + `final_mass_detector, final_spin, redshift`); senão `ANALYST_STATUS.json` com `PARTIAL_*`. Política de repetição fixada **antes** (§6-D5; decidida só por flags de convergência, nunca por dtau). Quem opera lê só `CONTROLLER.json`, `ANALYST_STATUS.json`, `PRIVATE_CONVERGENCE.json` e `ANALYST_OUTPUT.json`.
Porta: **10/10 convergidas**; com 9 o V1 dá `INSUFFICIENT_SAMPLE`.

**Passo 5 — Estágio cego.** `WSLPY estagio_cego_D.py` [A ESCREVER]. Lê **somente** os `ANALYST_OUTPUT.json`: σ_i = std ddof=1 de `blinded_dtau220` (invariante ao offset) e W90/3,29 (C9); `a_i` = mediana de `final_spin`; `N(a_i)`, `κ̂(a_i)` e `k = 4π(1+s)/s` com as funções `bcw220/kerr_kappa_hat/k_kms` **copiadas verbatim** de `poder_cego_ramo_b_v2.py` l.45–70 (aquele script executa no import; copiar as funções); β = `ALPHA_FINE_CODATA_2018 × √e` em runtime (α lido de `um.py` por regex, como no script); `x_i = β·k·N`, `δ_i^pred = −x/(1+x)`; pesos `w = 1/(σ² + σ_sys²)`; `δ̄^pred`, `σ_comb`, **poder = |δ̄^pred|/σ_comb** (o jackknife não é calculável cego; `σ_usado ≥ σ_comb`); C1 (controle canônico τ★ = t_P: |z_A − z_RG| < 1e−30, V1 poder_cego `controle_ramo_canonico_delta` ≈ −3e−42); C5 (σ_sys família 0,029–0,038 DECLARADO; sist_rel = σ_sys/|δ̄^pred| ≤ 0,3). Escreve `PODER_RAMO_B_ANTES_DE_ABRIR.json`, imprime o sha256 e **registra-o no Mapa** antes do passo 6.

**Passo 6 — Injeções C2(b).** `WSLPY run_controlled_D.py --job C2_<evento>_{GR,RB}` [A ESCREVER a adaptação de `injection_design`]: para cada evento, uma injeção com `dtau220 = 0` e outra com `dtau220 = δ_pred,i`, em **ruído off-source real do próprio evento** (bloco pré-evento fora do intervalo protegido, longe da janela do PSD), parâmetros no centro do posterior GR do catálogo (m₁, m₂ de fonte × (1+z); χ = χ_eff alinhado), distância reescalada ao **SNR de rede do catálogo** (alvo `target_network_optimal_SNR`). Recuperação com a mesma PE. Critérios do V1: |viés| ≤ 0,2·|δ_pred| (≈ 0,08) e cobertura nominal; deduz-se `c(σ) = c₀ + k_c·σ` (V1: «valores da 013-bis NÃO são prior»). Três tamanhos (§7): mínima 10 PE (5 eventos × 2), média 20 (10 × 2), ampla 50. **Honestidade estatística:** com 1 injeção por classe e evento, a incerteza do viés combinado é ≈ σ_comb ≈ 0,10 — maior que a tolerância 0,08; C2 mínima/média só exclui vieses grandes, não certifica |viés| ≤ 0,2·|δ_pred| (§8-R6).

**Passo 7 — Autorização de abertura e abertura.** (7.1) Registro da autorização do operador ligada ao sha256 do passo 5 e à lista de gates (F4.1 ok, 10/10 convergidas, C1/C5/C2 ok) [A ESCREVER o ato]. (7.2) `WSLPY abrir_D.py` [A ESCREVER]: confere a árvore de código = a do manifesto; lê o `dtau220` **bruto** dos `*_result.hdf5` (sem offset); verifica que σ_i bruto == σ_i do estágio cego (1e−12); roda `estimador_ramo_b_v1.py` **uma vez**.

**Passo 8 — Estimador do V1** (`estimador_ramo_b_v1.py` [A ESCREVER]), exatamente a seção `estimador` do V1: `δ̂_i` e σ_i por evento; `w_i = 1/(σ_i²+σ_sys²)`; `δ̄ = Σw(δ̂−c(σ))/Σw`; `σ_comb = 1/√Σw`; `σ_usado = max(σ_comb, σ_jackknife)`; `z_RG = δ̄/σ_comb`; `z_B = (δ̄ − δ̄^pred)/σ_comb`; `poder = |δ̄^pred|/σ_usado`; `χ²/dof`; jackknife por evento; fração máxima de informação por evento (≤ 0,2 na 013-bis; aqui ≈ 0,14 projetado); secundário por KDE (larguras 0,7/1,0/1,4) e `ln B`. **«Offset fixo em 0 PROIBIDO como teste.»**

**Passo 9 — Função de veredito e `RESULTADO_RAMO_B_V1.json`.** `veredito_ramo_b.py` [A ESCREVER]: `gw_stack.veredito` (l.69–81) **não é chamável aqui**: consome `cego/aberto` do rito do **eco** (leis MAY/KMS/DEC, `recovery_R1/R2`, `a_on`, controles ×0,5/×2) e o prefixo `TGL_ECHO_RADICAL_V3__`, e pode devolver `DETECTED_AT_DELAY_LAW`, que **não está** nos vereditos permitidos do V1. A «mesma função» é a **ordem da regra 2** (`n<10 → INSUFFICIENT_SAMPLE`; `sist_rel>0,3 → INCONCLUSIVE_SYSTEMATICS`; `poder<5 → NOT_FALSIFIED_UNDERPOWERED`; `z_excl≥5 → FALSIFIED_AT_5SIGMA`; senão `NOT_FALSIFIED_POWERED`, com sufixo `__GR_TENSION_REPORTED` se |z_RG| ≥ 5) com as constantes de `preregistro_fase6.py` l.42; o V1 acrescenta `χ²/dof>3`, C1–C9 reprovado e discordância primário × secundário a `INCONCLUSIVE_SYSTEMATICS`. Token: `TGL_RAMO_B_RINGDOWN_V1__K_2PI_OVER_KAPPA_HAT_KMS__M_F_DET__ENVELOPE_ADDITIVE_RATE__SET_D_O4_BLIND__<desfecho>__GATE_UNTOUCHED`. Proibidos: `CONFIRMED`, `PROVED`, `PROVED_BY`, «QG confirmada». Falsificação = do **par**, nunca de β, da lei na forma ou da TGL. O próprio `veredito_ramo_b.py` entra no manifesto do passo 1 (hash antes de abrir).

**Passo 10 — Registros.** Mapa de Rotas (`rotas.py registrar`, artefatos com sha256), memória da casa por depósito (regra da fila), cofre; nenhum movimento de gate.

---

## 6. O que FALTA (separado do que existe)

**A. Código a escrever** (todo em `work\conjunto_D_20261029\codigo_D\`, cópias **byte-idênticas** de `pseob_source`, `temporal_contract`, `strain_io`, `remnant_conversion` da v112, pinadas por hash no manifesto):
1. `guard_D.py` (substitui `registration_guard`): confere V1 por hash, manifesto congelado + testemunho, árvore de código, runtime `/opt/lal_env` e módulos ativos, relógio **novo** definido pelo operador (autorização de 29/10), autorização por evento (só os 10), caminhos de strain na raiz da Bancada com sha256 pinado, `validate_launch` mantido (anti-CLI direto).
2. `pe_runner_D.py` e `run_controlled_D.py`: cópias de v112 com `import guard_D`, diretório de saída fora do git e `contained()` trocado.
3. `blinding_D.py` + `blind_seed_D.py`: semente nova, etiqueta HMAC própria, o V1 do ramo B tem **só `dtau220` livre**; `dtau440`, `domega220`, `domega440` saem do posterior como colunas constantes (fixas em 0), então `shifted_samples` ainda funciona (as constantes recebem offset inofensivo); só `dtau220` é lido.
4. `injection_D.py`: injeção em off-source dos eventos de D (o original só aceita GW250114), com PSD/janela fora do intervalo protegido e `validate_truth_support` ajustado a priors com parâmetros fixos (impedimento 2 da `NOTA_CONJUNTO_D.md`).
5. `congelar_D.py`, `lancar_fila_D.py`, `estagio_cego_D.py`, `abrir_D.py`, `estimador_ramo_b_v1.py`, `veredito_ramo_b.py`.
6. Testes sem dado de D para o estimador e o veredito (sintético com resposta conhecida, incluindo o caso n = 9 → `INSUFFICIENT_SAMPLE`).

**B. Arquivos de registro a criar:** (a ordem do operador já existe: seq 1545); `MANIFESTO_D_CONGELADO.json` e `JOBS_D_V1.json` (+ testemunho, + registro no Mapa); compromisso da semente; autorização de abertura ligada ao hash do estágio cego; relatório de F4.1.

**C. Decisões [OPEN] — da gerência/operador, antes do congelamento:**
- **D1 priors:** `d_L` até ≥ 10 000 Mpc (5/10 eventos > 2000 Mpc); manter `m₁∈[15,100]`, `m₂∈[10,100]` (todas as massas de detector de D ficam dentro); `dtau220∈[−0,8; 2,0]`; prior de tempo em torno do GPS do catálogo (largura ±0,1 s a fixar).
- **D2 amostrador e orçamento:** `nlive`, `walks`, `maxcall` e **parede por job** (a cadeia 015 limitava a 28 800 s = 8 h; o cenário central dá 11–13 h por PE com 24 workers). Decidir pelo resultado de F4.1.
- **D3 estimador:** o V1 não fixa o valor central de `δ̂_i` (média? mediana?). Proposta: **média posterior** (consistente com σ por ddof=1), mediana como controle; congelar antes.
- **D4 nuisance `c(σ)`:** o V1 diz «c(σ) = c₀ + k_c·σ profilado sob as duas hipóteses». Com `c₀` livre e sem âncora, `c₀` absorve a média comum e o poder colapsa. A leitura funcional é **calibrar `c` nas injeções GR de C2 e propagar a incerteza como covariância de nuisance** (o poder cai por √(1 + σ_c²/σ_comb²); com 10 injeções σ_c ≈ σ_comb → poder ≈ 2,7–2,8σ). Isso torna C2 grande parte do custo. Decidir antes.
- **D5 repetição:** uma repetição por evento com `maxcall × 2`, nova semente de sampler, decidida **só** por flags de convergência (como a 015 fez para GW250114); depois disso o evento falha → n < 10.
- **D6 janela do PSD:** `psd_duration_s = 256` (todos os eventos têm ≥ 451 s limpos antes); registrar em vez de 512.
- **D7 abertura:** quem abre e como (cegueira é **procedural, no mesmo host**; o V1 já registra «certificação de cegueira é deste V1»). Se o operador quiser custódia separada, o seed e os brutos teriam de ir a outra conta/máquina.
- **D8 holds e pendentes:** continuam fora; se D10 sair com n < 10 por convergência, o plano **não** os promove.
- **D9 C2:** tamanho (10 / 20 / 50 PE) e se o ruído é off-source dos eventos de D (proposto) ou outro.

---

## 7. Estimativa de tempo e CPU

Base **medida** [DECLARADO, recibos GW250114; recomputada por `estimativa_tempo.py`]: 0,0614–0,0621 CPU-s por chamada de verossimilhança; 13,6–15,4 núcleos efetivos de 24 workers (57–64 %); logo **2 PE de 24 workers** ≈ 27–31 núcleos efetivos nos 48. Pior que isso: 3 PE de 16 workers ou 4 de 12 podem render mais por núcleo (**[OPEN]**, medir em F4.1).

**Número de chamadas até convergir — a incógnita [OPEN].** Argumento [INFERENCE]: nested sampling gasta `iterações ≈ nlive × H` (H = informação em nats; para ρ ≈ 14 em 12 dimensões, H ≈ 50–70) e `chamadas/iteração` medido nos pilotos de GW250114 = 300–490 (cresce com a compressão). Com nlive = 512: 26 000–36 000 iterações × 300–500 ≈ **8–18 milhões de chamadas** por PE de D. Escolhi cenários: **otimista 3·10⁶** (nlive 256, aceitação alta), **central 10⁷**, **pessimista 3·10⁷**. Coerência: «58–390 CPU-h» do V1/013-bis [DECLARADO] corresponde a 3,4·10⁶–2,3·10⁷ chamadas — leio como **por PE**, não como total de D.

| cenario | CPU-h por PE | wall de 1 PE (24 workers) | F4.1 (2 PE sinteticas) | D10 PE cega (10 PE) | C2 minima (10 PE) | C2 media (20 PE) | C2 ampla (50 PE) |
|---|---|---|---|---|---|---|---|
| otimista (3e6 chamadas) | 51-52 | 3.3-3.8 h | 102-103 CPU-h; 3.3-3.8 h | 511-517 CPU-h; 16.6-19.0 h | 511-517 CPU-h; 16.6-19.0 h | 1023-1034 CPU-h; 33.1-38.1 h | 2556-2586 CPU-h; 82.8-95.2 h |
| central (1e7 chamadas) | 170-172 | 11.0-12.7 h | 341-345 CPU-h; 11.0-12.7 h | 1704-1724 CPU-h; 55.2-63.5 h | 1704-1724 CPU-h; 55.2-63.5 h | 3408-3448 CPU-h; 110.4-126.9 h | 8521-8619 CPU-h; 276.0-317.4 h |
| pessimista (3e7 chamadas) | 511-517 | 33.1-38.1 h | 1023-1034 CPU-h; 33.1-38.1 h | 5113-5171 CPU-h; 165.6-190.4 h | 5113-5171 CPU-h; 165.6-190.4 h | 10225-10343 CPU-h; 331.2-380.8 h | 25563-25856 CPU-h; 828.0-952.1 h |

Totais:

| cenario | F4.1 + D10 + C2 minima (22 PE) | F4.1 + D10 + C2 media (32 PE) | F4.1 + D10 + C2 ampla (62 PE) |
|---|---|---|---|
| otimista (3e6 chamadas) | 1125-1138 CPU-h; 36-42 h (1.5-1.7 dias) | 1636-1655 CPU-h; 53-61 h (2.2-2.5 dias) | 3170-3206 CPU-h; 103-118 h (4.3-4.9 dias) |
| central (1e7 chamadas) | 3749-3792 CPU-h; 121-140 h (5.1-5.8 dias) | 5453-5516 CPU-h; 177-203 h (7.4-8.5 dias) | 10566-10687 CPU-h; 342-394 h (14.3-16.4 dias) |
| pessimista (3e7 chamadas) | 11248-11377 CPU-h; 364-419 h (15.2-17.5 dias) | 16360-16548 CPU-h; 530-609 h (22.1-25.4 dias) | 31698-32062 CPU-h; 1027-1181 h (42.8-49.2 dias) |


Leituras: (i) **D10 sozinha**, central: ~1 700 CPU-h → 55–63 h de parede (2,3–2,6 dias). (ii) O que mais pesa não é D, é **C2**: cada injeção custa uma PE inteira. (iii) F4.1 com uma só PE (GR) já mede a escala: 170 CPU-h (central), 11–12,7 h de parede com 24 workers (menos se 48 workers escalarem: [OPEN], medir); a decisão de orçar o resto sai daí. (iv) Por evento, no cenário central, 11–13 h de parede com 24 workers — acima do teto de 8 h da cadeia antiga.
Comparação com o declarado pela bancada: T09 da ORDEM 015: 2,6–3,3 h (outro objeto: 220+440); proposta A02 do Codex: 8 h 00 min 20 s nominais para dois casos **de 100 000 chamadas** (dynesty estático, nlive 256, walks 25, 1 worker) — por contagem, 100 000 chamadas ≈ 4 000 iterações ≈ 15,6 nats de compressão do volume do prior, contra H ≈ 50–80 nats necessários em 12 dimensões a SNR 14–20: **não convergem** [INFERENCE] (a INIT003 chegou a Δlogz 57 com 9 738 chamadas).

---

## 8. Riscos e paredes (em ordem de probabilidade × dano)

| # | risco | evidência | efeito | mitigação |
|---|---|---|---|---|
| R1 | **Convergência da PE** (custo desconhecido, nunca atingida na casa) | 2/2 PE reais e 1 sintética pararam por teto com Δlogz 425 / 177 / 57 | n < 10 ⇒ `INSUFFICIENT_SAMPLE`; ou semanas de CPU | F4.1 antes de D; teto e parede dimensionados pela medida; repetição pré-registrada (D5) |
| R2 | **Guardas/registro** (cadeia 013-bis/015 vencida e fechada; `Chatgpt` só leitura; recibo `…_AUDITADA.md` ausente; caminhos fora da raiz); a autorização já está registrada, falta o orçamento | prazo 2026-10-03; ausência do recibo; `contained()` | nada roda | guarda novo pinado ao V1 + manifesto novo (§6); orçamento de CPU dito ao operador |
| R3 | **Poder < 5σ e n = 10 no mínimo** | projeção 3,7–3,9σ (D10), 4,4–4,6σ (D14); `min_eventos=10` | veredito quase certo `NOT_FALSIFIED_UNDERPOWERED`; uma PE falha ⇒ `INSUFFICIENT_SAMPLE` | dizer ao operador **antes**; avaliar parar no estágio cego (passo 5): ali o poder já é conhecido |
| R4 | prior de distância dos jobs existentes | 5/10 eventos > 2000 Mpc | posterior truncado/enviesado | D1 |
| R5 | `c(σ)` ambíguo (D4) e C2 pequeno | V1 `estimador` | poder cai ou C2 não certifica o viés | decidir D4/D9; reportar a limitação |
| R6 | estatística de C2: σ do viés combinado ≈ 0,10 > tolerância 0,08 com 1 injeção por classe | cálculo acima | C2 só exclui vieses grandes | tamanho «ampla» (50 PE) ou aceitar a limitação dita |
| R7 | PSD de 512 s inviável em 2 eventos; DQ de H1 (GW241111) com só 568 s limpos antes do evento | tabela 4.1 | falha de `offsource_psd` | 256 s (D6) |
| R8 | cegueira procedural, mesmo host; brutos legíveis por quem opera | `run_controlled` l.54 | vazamento acidental | disciplina de leitura (§5-4), sem abrir `*_result.hdf5` antes do passo 7 |
| R9 | `gw_stack.veredito` não aplicável; `DETECTED_AT_DELAY_LAW` fora do V1 | §5-9 | veredito errado | `veredito_ramo_b.py` com a mesma ordem, em manifesto |
| R10 | pSEOBNRv4HM_PA indisponível | **não ocorre**: gera em 0,065 s (§3) | — | — |
| R11 | strain ausente | **não ocorre**: 20/20 com sha256 do manifesto | — | — |
| R12 | A calibração A (+0,072 vs −0,382) já contradiz o par fora da cegueira | rota, 28/10 | D pode apenas repetir o que A sugeriu (não cega) | D continua o único teste cego; dizer isso no relatório |

As **3 paredes mais prováveis**: (1) R1 convergência/custo; (2) R2 guardas + autorização; (3) R3 poder < 5σ com n no mínimo.

---

## 9. Para registro no Mapa de Rotas (devolução do que foi examinado)

Examinado hoje (sem abrir D): código `e2_code`, `e2_code_v1_1`, `e2_code_v1_1_2` e emendas 015; `gw_stack.py` e `preregistro_fase6.py`; recibos de custo e pilotos de GW250114; preparação F3/F4.2 do Codex; manifesto de strain; DQ dos 10 eventos; fumaça pSEOB; limites temporais de LAL; projeção de poder de D; estimativa de tempo. Resultado em uma linha: *a cadeia de guardas da 013-bis/015 está fechada (prazo vencido, recibo ausente); a PE completa nunca convergiu na casa; D10 tem poder de planejamento 3,7–3,9σ < 5; pSEOBNRv4HM_PA e o strain de D estão disponíveis; 5 de 10 eventos exigem d_L > 2000 Mpc; custo central 170 CPU-h por PE.* Artefatos desta pasta com sha256 em `INVENTARIO_D_29out.json`. Não refazer: INIT003; o 100 000 chamadas da proposta A02 (não converge por contagem); o `gw_stack.veredito` para o ramo B.
