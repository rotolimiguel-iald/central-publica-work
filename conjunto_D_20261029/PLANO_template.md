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

{{TAB_EVENTOS}}

### 4.2 Strain dos 10 eventos (sha256 dos bytes; amostras não abertas)

{{TAB_STRAIN}}

### 4.3 Projeção de poder de PLANEJAMENTO de D — [DERIVED]

Entradas: SNR de rede GWOSC e δ_pred por evento (já no V1), ajuste σ_τ(SNR) da bancada para os 31 do GWTC-5.0 (`ln σ = 1,4166 − 0,9450 ln ρ`, resíduo ln 0,2177; NOT_BLIND, planejamento), σ_sys ∈ {0; 0,029; 0,038} do V1. **Não inclui** jackknife (σ_usado = max(σ_comb, σ_jack) só pode piorar) nem a diferença v4HM-PA × v5PHM, e usa SNR de **rede**, não de ringdown. Não lê nem imprime nenhum valor central de deformação.

{{TAB_PROJ}}

**Calibração do modelo [REAL]:** aplicado aos 31 eventos do A31 (SNR do próprio ajuste), o mesmo `σ(ρ)` dá σ_comb = **0,0355** (mediana) contra **0,0336** do V1/`sigma_comb_A31` — erro de 6 %. **Cenário «D se comporta como a calibração A»** (δ̄ = +0,072 contra δ̄_pred = −0,3985): z_excl = 0,4705/σ_comb ≈ **4,4–4,6** (D10) e 5,2–5,5 (D14), e em ambos o poder fica < 5, logo a regra 3 devolve `NOT_FALSIFIED_UNDERPOWERED` antes que a regra 5 possa dar `FALSIFIED_AT_5SIGMA`. σ_comb máximo para poder ≥ 5 (D10): 0,0797; o fator de informação que falta é **1,78×** sobre a projeção central. Para comparação, o V1 declara para A (31 eventos) 11,4σ, B 6,4σ, C 6,5σ.

### 4.4 Tabela de arquivos

{{TAB_INV}}

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

{{TAB_TEMPO}}

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
