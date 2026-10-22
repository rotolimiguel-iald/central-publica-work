# O que e REUTILIZAVEL para o pre-registro do ramo B (caminho + sha16, lidos por script em 05/10/2026)

Regua: nada aqui e veredito; sha16 = 16 primeiros hex do sha256 calculado no disco hoje. Nada foi baixado.

## Codigo (leitores / estimadores)

| item | caminho | sha16 | bytes | o que faz / limite |
|---|---|---|---|---|
| pipeline V1 do dephasing | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\eco_ancorado_v1\ringdown_dephasing_v1.py` | 31a9f41da1b72321 | 14086 | seno amortecido branqueado, grade (f, tau), pico por argmax (defeito: borda) |
| pipeline V2 do dephasing | `...\Nós\eco_ancorado_v1\ringdown_dephasing_v2.py` | 0793c58d6995194b | 18415 | ancoragem IMRPhenomXAS (SNR>=8), exclusao de borda, corte |df|<=0.3; previsao `delta_B = -0.5*BETA*gm*w_gr**2*tau_gr` (k=1, M=M_f,det) l.141; nulos = seno amortecido puro (NAO calibra difusao de fase, CT-02); roda no WSL /opt/lal_env |
| leitor/juiz no um.py | `...\Nós\um.py` v385: `prove_ringdown_dephasing_protocol` l.209231; `_result` l.209273; `_amendment_v2` l.209324; `_result_v2` l.209374-209420; `prove_ringdown_scope_v376` l.195121-195186 | um.py 33,386,720 B (nao rodar) | — | le por hash e aplica a matriz pre-registrada (exclude_z 5, power_min 5, bias 0.2, syst 1 sigma, chi2/dof 3; vereditos permitidos BRANCH_B_EXCLUDED / GR_TENSION_REPORTED / NOT_FALSIFIED_POWERED / _UNDERPOWERED / INCONCLUSIVE_SYSTEMATICS / AWAITING_RESULT_FILE; proibidos CONFIRMED/PROVED) |
| banco de GW residente (Bancada Um) | `C:\IALD\Bancada_Um\bancada\gw.py` | ea7c849c7f2c10b8 | 19614 | por evento: Mf_det, a_f_HBR2016, f_qnm_220_hz, tau_d_220_ms, lag; `gw_empilhar(versao=...)` |
| empilhador | `C:\IALD\Bancada_Um\bancada\gw_stack.py` | 0a636d439a03f016 | 7697 | empilhamento com poder gravado antes de abrir |
| estimador ancorado do eco (V5) | `C:\IALD\Bancada_Um\investigacao\fase6_eco_radical_01out\echo_anchored_v5.py` | efa2d774bd7b79c4 | 24477 | `delay_laws()` l.58: MAY 2ln(1/beta)·GM/c^3, KMS 4pi(1+sq)/sq·GM/c^3, DEC 2/beta·GM/c^3; `qnm()` BCW l.61; a_f HBR2016, M_f UIB2016 |
| reproducao independente do C6 | `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C7_INDEPENDENT_v3_3\reproduce_c6.py` | c9477017041da663 | 7093 | reproduziu o C6 com diferenca 0.0 (auditoria 013-bis) |
| grade de QNM (220+440; sem 221) | `...\ORDEM_013_RINGDOWN\QNM_GRID.json` | 4f34367a09060238 | 169231 | usada por bancada e auditoria (spline + brentq) |
| codigo E2 do 5 sigma (pinado no registro) | `...\ORDEM_013_RINGDOWN\bis\e2_code\` (blinding, null_campaign, pe_runner, pseob_source, registration_guard, remnant_conversion, route_iv_null, run_controlled, strain_io, synthetic_null, temporal_contract) e `bis\e2_code_v1_1\` | sha256 de cada um em `ENTREGA_013BIS_E2_REGISTRO_V1.md` | — | pSEOBNRv4HM_PA (DTau220/DTau440) + bilby/dynesty; a guarda da V1 expirou em 2026-09-24T11:06:33Z; toda continuacao sob V1.1 |
| diagnostico de posto espectral (T-10 A') | `...\ORDEM_013_RINGDOWN\bis\015\t10\t10_aprime_rank.py` | sha256 e986e401c498d959... (do recibo) | — | so-220 com (M_f, a_f) livres NAO identifica delta_tau (Jacobiano 2x3 posto 2); com 440 posto local 3 |

## Pre-registros ja escritos (modelos de forma)

| item | caminho | sha16 | bytes |
|---|---|---|---|
| protocolo V1 do dephasing (no core) | `core.ringdown_dephasing_protocol.protocol` | protocol_hash a3d941e56d3d33c5 | — |
| emenda V2 (no core) | `core.ringdown_dephasing_amendment_v2.protocol` | protocol_hash 3449885389a2529a | — |
| RINGDOWN_5SIGMA_V1 | `...\ORDEM_013_RINGDOWN\RINGDOWN_5SIGMA_V1.json` | e1be6b0409720c68 | 183005 |
| RINGDOWN_5SIGMA_V1_1 (arvore irma, relogio proprio) | `...\ORDEM_013_RINGDOWN\RINGDOWN_5SIGMA_V1_1.json` (+ V1_1_1 75b1884d18240ddb, V1_1_2 a02c4224b0c832a8, V1_1_3 74a2c8b656244ff4) | 96571187bec3c1d7 | 228439 |
| pre-registro da Fase 6 (3 leituras x leis) | `C:\IALD\Bancada_Um\investigacao\fase6_eco_radical_01out\PREREGISTRO_FASE6_ECO_RADICAL_20261001.json` | 47457358d72dd9dc | 89280 |
| pre-registro dos dois lados V1.4 (livro) | `C:\IALD\Bancada_Um\investigacao\preregistro_dois_lados_02out\PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.json` | 4a0019a3db649e01 | 60772 |
| ORDEM 015 (13 decisoes do operador na §9) | `...\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md` | c903681d01eec5ed | 135319 |

## Dados EM DISCO (nada a baixar para um V1 de dephasing)

| item | caminho | sha16 / contagem | nota |
|---|---|---|---|
| cache de maio (O1-O3) | `C:\IALD\projetos_pyhton\IALD\strain_cache\*.npz` | 170 npz | 32 s @ 4096 Hz, H1/L1; os 169 sha256 estao no V2_RESULT |
| catalogo GWTC (massas, z, chi_eff, GPS) | `C:\IALD\projetos_pyhton\IALD\gwtc_full_catalog.csv` | 895250e9d404a240 (27787 B) | medianas; sem intervalos propagados (RD-02) |
| strain O4 (GWOSC) | `C:\IALD\Bancada_Um\fontes_externas\gwosc_o4\` | 703 arquivos (354 x 4096 s + manifesto) | 177 eventos O4 ja janelados a 32 s (Fase 6) |
| amostra/catalogo da Fase 6 (244 BBH) | `...\fase6_eco_radical_01out\catalogo_v3.csv` / `AMOSTRA_FASE6.json` | e6a0ba6a870e2a40 / 2f6424f3adf57e76 | M_f, a_f, f_220, tau_220 por evento |
| posteriores pSEOBNR do GW250114 (Zenodo 17018009) | `...\ORDEM_013_RINGDOWN\cache\public\17018009\extracted\TGR_companion_S250114ax_results\gw250114_pseobnr\posterior_samples.h5` | b9971bcd7d72fdd4 (59,249,916 B) | + controle de injecao `controls_extracted\...\pseobnr_injection\posterior_samples.h5` e2373f81973401ad (64,331,592 B); licenca MIT (errata 013) |
| catalogo dtau220 GWTC-5.0 (31/33 eventos) | `...\ORDEM_013_RINGDOWN\C4_CATALOG_220.json` + `C4_CATALOG_COMBINATION.json` | 93bdc413130d294a / f3d8c1959ded3efd | NAO-CEGO; R-B ln B -1.81 (31) / -2.48 (33), INCONCLUSIVE_SYSTEMATICS; deformacao comum +0.072 [+0.015,+0.134] |
| catalogo dtau220 GWTC-3 (18 produtos; 10 publicados) | `...\ORDEM_013_RINGDOWN\C4_GWTC3_220.json` + `C4_GWTC3_COMBINATION.json` + `C4_GWTC3_PUBLISHED_COMBINATION.json` | d9dc9b09a8d91dc7 / f88c2aa84f988917 / f6dbd853223b8039 | uniao distinta 39 eventos |
| leituras do relogio (10, sem escolha) | `...\ORDEM_013_RINGDOWN\C1_LEITURAS.md` (+ C1_TABLES.json) | a640e0c9ab336dab | R-B: tau*,src = G M_src/c^3, tau*,det = t_M |
| C6 (GW250114, strain na fonte) | `...\cache\gw\C6_RESULTS_GW250114.json` | 781a3741a68875eb | INCONCLUSIVE_SYSTEMATICS; ln B(R-B) -0.0026 primario |
| T05 (440: sigma_equiv, prior) | `...\Chatgpt\TGL_BANCADA_OFICIAL\state\investigation_20260928\gw\assessment.json` | 920076efbebf912b | rho440 proxy 1.763 [INPUT] |
| Fisher (poder por cenario O4/O5/ET/CE) | `...\ORDEM_013_RINGDOWN\C5_FISHER_v3.json` | ef7a800369ba0732 | N90, z esperado condicional |
| strain do GW250114 (t07) | `...\ORDEM_013_RINGDOWN\bis\015\t07\` (metadata, results_rho) | c5415c5a3498150c (frames) | covariancia H1 offsource 0.955% acima de 1e12 (T15) |

## Numeros ja fixados que o pre-registro deve CITAR (nao recalcular)

- beta_runtime = 0.012031300400803142; t_P = 5.391125282640084e-44 s; delta_pred_A(V2) = -2.153e-42.
- delta_B por serie = -beta·Q·(M omega) (k=1, M=M_f,det): x = 0.0211559 (a=0.7); empilhado V2 -0.019367; fracao por realizacao (difusao de fase) 0.247-0.273.
- sigma(V2) = 0.1089 (15 series); para poder 5 precisaria sigma <= 0.00387 (~790x a informacao atual).
- C6 ln B(R-B/RG) = -0.0026 (10 t_M, 1e-20); correcao/sigma = 0.34; ramo B imitado por Kerr 1.25% mais leve, delta a ~ -0.016/-0.019.
- Catalogo GWTC-5.0: z_comb R-B 0.654 (39 posteriores); N90(5 sigma, R-B) = 335 GW250114-like ou ~3300 O4; largura de delta_f: N90 = 59/38/21.
- Sistematica de familia SEOB x Phenom 0.029 = 7x o piso 0.0040 (VERMELHA); offset fixo em 0 proibido como teste.
- Se o ramo B agisse na PROPAGACAO: Gamma_B·t = 2.26e17 e-folds (excluido trivialmente) — o ramo B so e testavel como efeito LOCAL na fonte.
- Relogios v369: GM/c^3 com M = Terra EXCLUIDO; M = atomo invisivel; tau* <= 4.8e12 t_P (95%).
- Eco (Fase 6): as leis k·GM_f/c^3 com k = 8.84 (MAY), 29.9 (KMS, a=0.69), 166.2 (DEC) estao FALSIFIED_AT_DELAY_LAW para amplitude sqrt(beta) e sin 2theta (z_excl 8.9-19.4; MAY sqrt(beta) inconclusiva) — fora do livro por decisao do operador; nao e teste do dephasing.
