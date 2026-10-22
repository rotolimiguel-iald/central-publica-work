# Fase 9 (a razão de Hubble) — lente «OS DADOS NA CASA» — inventário aferido (05/10/2026)

Aferidor, não cético cego: tudo abaixo foi LIDO por script (`medir.py`, `ler_core.py` nesta pasta; `inventario_medido.json`, `inventario_medido_extra.json`), sem download. Estatutos marcados. NOT_FALSIFIED nunca é CONFIRMED; a RG/ΛCDM é o limite clássico. β nunca literal: `ALPHA_FINE_CODATA_2018 = 0.0072973525693` lido do `um.py` por regex ⟹ β = α·√e = 0,012031300400803142 (= `beta_tgl` do RESULTADO da Fase 5).

Consultas feitas antes (ordem da casa): `rotas.py consultar "Hubble" | "SH0ES" | "escada" | "D1b"`; `rotas.py ver` de `d1.fase1_eff_30set`, `d1.fase2_dois_setores_30set`, `d1.fase3_leitores_h0`, `d1.fase3bis_d1b_convencao_artigo`, `d1.fase4_desvio_30set`, `d1.fase5_sh0es_01out`, `d1.fase7_cc_covariancia_01out`, `d1.camb.v3_real`, `um_py.v380.fases_5_6_7_por_hash` (registros inteiros gravados em `rota_*.json` aqui); `buscar.py` (13.608 docs, índice de 03/09/2026) para TRGB, Freedman, JAGB, escada inversa, TDCOSMO, JWST, Riess 2024/CCHP, Pantheon+SH0ES, cadeias Planck, DESI DR2, ids arXiv, 72,6/70,4/68,5, Anand, pós-dição; memórias `fase5-sh0es-01out.md`, `fase7-cc-covariancia-01out.md`, `relatorio-consolidado-01out.md`, `beta-e-a-regra-matriz-02out.md`, `rg-limite-classico-nao-rival.md`; a lei da prova da casa `POS_DICAO_operador_05out.txt` (775 B, sha16 cf82d9e55757a7f2).

Versão corrente lida do selo: `um_absoluto_selo.json` → `um_version = v386` (86.148 B, sha16 72efaf72f604b721); `um.py` 33.600.222 B, sha16 e30aac4e0e1096b1; `um_absoluto.json` 4.947.109 B, sha16 0dbfb3fc1d319d1e.

---

## 1. REUTILIZÁVEL JÁ (em disco, hash lido hoje)

### 1.1 A escada SH0ES reproduzida na Bancada (Fase 5, 01/10) — Pantheon+ com calibradores + covariância

| item | caminho | bytes | sha16 | estatuto |
|---|---|---|---|---|
| Pantheon+SH0ES.dat (1701 SNe, 47 colunas: zHD, zHEL, m_b_corr, MU_SH0ES, CEPH_DIST, IS_CALIBRATOR, USED_IN_SH0ES_HF …) | `C:\IALD\observaveis_tgl\tgl_data_cache\pantheon\Pantheon+SH0ES.dat` | 579.283 | 1cb0fc379ef066af | [REAL] hash; origem raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease (`frente_alpha\download_pantheon.py`, 1.406 B, sha16 24fa8194f683ca29) [DECLARADO]; **sem registro de identidade byte a byte com o oficial** (só a cov tem) |
| Pantheon+SH0ES_STAT+SYS.cov (1701×1701) | `C:\IALD\projetos_pyhton\acom\tgl_data_cache\pantheon_covariance.dat` | 33.284.960 | abf806d966485e64 | [REAL] byte-idêntica ao oficial (`Bancada_Um\estado\identidade_pantheon_cov.json`, 916 B, sha16 bf334f7b0067ca92, 30/09) |
| cache .npy da cov | `C:\IALD\Bancada_Um\tabelas\pantheon_cov_v1.npy` (+ `.npy.json` 299 B com o sha256 da fonte) | 23.147.336 | — | [REAL] regenerável |
| amostra de H0 usada | 1657 = 1580 (zHD > 0,01) + 77 calibradores Cefeida (μ = CEPH_DIST) em 37 hospedeiras; M profilado analiticamente (Brout+22/Riess+22) | — | — | gravado em `RESULTADO_FASE5…json → pantheon_sh0es` (sha256 do .dat 1cb0fc37…98cf8 dentro) |
| PREREGISTRO_FASE5_SH0ES_20261001.json | `C:\IALD\Bancada_Um\investigacao\fase5_sh0es_01out\` (cópia idêntica em `A Ponte e o Um\cache\bancada_01out\`) | 8.733 | f9fbf497c90c0a66 | [REAL] |
| RESULTADO_FASE5_SH0ES_20261001.json | idem (cópia idêntica no cache do rito) | 45.862 | 851d1076b85f12f6 | [REAL] |
| RELATORIO_FASE5_SH0ES_20261001.md | idem | 6.628 | 5b3274356126ef0f | [REAL] |
| SMOKE_SH0ES.json (poder prévio: sombra vs acumulada 0,19σ) | idem | 813 | 7a09b86bda582f08 | [REAL] |
| rodar_fase5.py (runner; `validar_sh0es` l.103, `bloco` l.76) | idem | 20.309 | 6e0981e3c6da1b7d | [REAL] |
| relatorio_fase5.py · preregistro_fase5.py · registrar_fase5.py · smoke_sh0es.py | idem | 7.364 · 11.604 · 10.997 · 5.216 | bec0029991883445 · — · — · — | [REAL] |
| rodar_fase5.log (+ `_tentativa1.log`, `_tentativa2.log`: o desvio de protocolo da validação V, dito) | idem | 4.592 | 200108b4f524f6c3 | [REAL] |

Números da Fase 5 lidos do core v386 (`core.core.bancada_fases_5_6_7_v380.fase5`): validação H0 = 73,53294 ± 1,01698, Ω_m = 0,33168, z_vs_alvo = 0,04476 (alvo «73,6 ± 1,1 (Brout et al. 2022) [DECLARADO: valor de memória da gerência, não lido da fonte]»); P_sombra δ = −0,0008 ± 0,00213 (z −0,3758), z_tensão 5,26015; ln B(sombra/acumulada) S = 5,35167; n = 1657. Do RESULTADO: P·sombra·tgl: H0_fundo 68,393 → K 1,083814 → H0_local 74,125; z* = 1089,95; rodada 646 s (01/10 12:59–13:10).

### 1.2 O leitor da Fase 4/5 no `um.py` v386 (funções e linhas) — o um.py NÃO calcula a escada: lê os artefatos da Bancada por hash

| função / bloco | linha | o que faz |
|---|---|---|
| `_V380_FILES` | 195215 | mapa dos 18 artefatos lidos de `CACHE\bancada_01out` e `CACHE\gw` (f5_pre, f5_res, f7_pre, f7_res, cc_cov …) |
| `prove_bancada_fases_5_6_7_v380(ONE, core)` | 195257 | lê por hash (bytes e texto LF), confere β = α√e do core, hash do pré-registro gravado no resultado, guarda de palavra proibida; devolve `fase5` (validação, P_sombra, lnB) |
| `_V378_BANCADA_FILES` | 195616 | PREREGISTRO/RESULTADO/SMOKE da Fase 4 + reanálise D1b + cronômetros |
| `prove_bancada_fase4_v378(ONE, core)` | 195822 | lê `CACHE\bancada_30set` por hash; devolve `P_ladder_d1b` (δ, σ, z_δ, K, H0_bg, H0_local, pull, lnB, χ²), `Q_pantheon_d1b`, `R_dr1_d1b`, `S_joint_d1b`, `T_intermediate_d1b`, `stacked_control`, posteriores |
| `prove_bancada_fases_v377(ONE, core)` | 196126 | Fases 1–3 por hash |
| conferência runtime `K_b = E(z*)^{2β/3}` a 1e-12 | 195708 | o núcleo D1b avaliado no runtime |
| pedra v378 (dissipação com contraste; D1b) | 199783 | `TGLExt/TheFlowLawContrast.lean` (fonte embutido em 127728) |
| livro de cobranças R1 («reflexo», escada; K = E(z*)^{2β/3} sobre o fundo nu; nó fixo em z*) | 194590, 194663 | a cobrança R1 lê `fase5.validacao.H0` e `P_ladder_d1b.z_delta` (194592) |
| artigo PT: «resolve a tensão de Hubble por remissão expressa … pós-dição declarada; zero parâmetro ajustado» | 165845 (contexto 165840–165850) | a frase que a v387 reescreve |
| artigo PT/EN: Fase 3 (leitores de H0: sombra = escada, TRGB, SBF, masers, lentes, sirenes) | 168624 / 172411 | — |
| artigo: Anand et al. 2025 TRGB-JWST (Coma 101,2 ± 6,4 Mpc) | 167631 / 171411 | única citação TRGB-JWST no um.py (é distância de Coma, não H0) |

Números da Fase 4 lidos do core v386 (`core.core.bancada_fase4_v378.P_ladder_d1b`): δ = −0,0025 ± 0,00223, z_δ = −1,12441, z_perfil = 1,13242, z_ganho_da_lei = 4,00641, β livre = 0,00953, custo/nat 0,00911, H0_bg = 68,4298, K = 1,083807, H0_local = 74,1647, pull = 1,0814; ln B tgl/ΛCDM 8,0204, livre/ΛCDM 5,7744, tgl/livre 2,2460; χ² ΛCDM 31,627 / TGL 15,576 / livre 14,293; `DIAGONAL_ERRORS_ONLY` no veredito. **Confere com o que a gerência citou (todos os dígitos).** Hashes gravados no core batem com os arquivos medidos hoje (22b4c440d8ad844d, 10683b334d28d84a, 5fb33c410edc6eea, 3d5c6afe85cc3064).

### 1.3 O computador da escada: a Bancada Um (scripts)

| script | caminho | bytes | sha16 | papel |
|---|---|---|---|---|
| motor.py | `C:\IALD\Bancada_Um\bancada\motor.py` | 19.991 | 49f304fd41afc8e4 | `OPCOES_ARTIGO` (l.40: planck_cov chen2019, dr1 correlacionada, lei d1b, beta_no_fundo nao); `_predizer_bloco` l.156; `I_lei = (2/3)·ln E_ΛCDM` l.190–191 (D1b); `lei_sn` sombra/acumulada l.202–211; `chi2` l.240; `residuos` l.269 |
| fundo_gpu.py | `…\bancada\fundo_gpu.py` | 8.477 | dc3920c2445c256f | `FundoV3Lote`; `DM_com_boost` l.141 (K(z) dentro da integral) |
| pantheon_cov.py | `…\bancada\pantheon_cov.py` | 6.341 | 386aee0980df5d65 | χ²_prof com M profilado; calibradores μ = CEPH_DIST |
| fontes.py | `…\bancada\fontes.py` | 12.724 | 6bc0d220f0fb7904 | caminhos de todos os dados (l.15–22, 120–123, 139); `planck_chen2019` l.163; `DR1_CORRELACOES` l.160; `desi_dr2` l.95 (exige as 3 cópias idênticas); `pantheon_plus` l.196 (docstring com a errata de 28/09) |
| evidencia.py | `…\bancada\evidencia.py` | 13.633 | 92b0c9eeb6370bd8 | ln Z por quadratura; ln B |
| patch_sh0es_calibradores.py | `…\ferramentas\patch_sh0es_calibradores.py` | 17.822 | 59c24d2b63cc45dc | o patch que ligou o conjunto `pantheon_sh0es` (01/10) |
| um_bancada.py (HTTP :18777) | `C:\IALD\Bancada_Um\um_bancada.py` | 20.339 | 13a393654139bc9f | `/api/ajustar`, `/api/comparar`, `/api/amostrar`, `/api/dados`, `/api/livro`, `/api/validacao` |
| mcp_um.py (MCP `bancada-um`) | `C:\IALD\Bancada_Um\mcp_um.py` | 14.480 | 95ee0e3ce3afb7ac | `ajustar`, `comparar`, `amostrar_posterior`, `listar_dados`, `livro` |
| importar_cronometros_do_artigo.py · importar_covariancia_moresco2020.py · patch_cc_covariancia.py | `…\ferramentas\` | 2.411 · 6.231 · 7.243 | d79cb413b36f57eb · 9d1e737ac1915842 · f5149134402a44ad | proveniência dos cronômetros e da covariância |

### 1.4 O fundo: DESI DR2 BAO (Fase 1), DESI DR1, Planck comprimido, cronômetros, tabela CAMB

| item | caminho | bytes | sha16 | estatuto |
|---|---|---|---|---|
| DESI DR2 BAO média (13 medidas) | `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\_originais\desi_gaussian_bao_ALL_GCcomb_mean.txt` (read-only) | 472 | 9ac154ab583ce759 | [REAL] 3 cópias idênticas (também `frente_alpha\` e `A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\data\cosmology\`); a Bancada recusa se divergirem |
| DESI DR2 BAO covariância 13×13 | idem `…_cov.txt` | 2.547 | 252a143274c8a07c | [REAL]; origem CobayaSampler/bao_data `desi_bao_dr2` (`download_desi_dr2.py`, 22/05/2026; sha16 363d55b1e00d3d54); `ORIGINS.md` (1.202 B, 24db0abed7e09775): «a remote release commit was not independently verified» [DECLARADO] |
| PROVENIENCIA.json (teste acústico) | `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\PROVENIENCIA.json` | 3.679 | 65362c4dbd8045c8 | [REAL] |
| DESI DR1 BAO (12 linhas, σ) | literal `DESI_ROWS` em `A Ponte e o Um\cache\d1_camb\v3\d1_v3_pipeline.py` l.34 | 24.068 | 4e8f9dc33e28db79 | [REAL] literal do pipeline selado; correlações D_M–D_H em `fontes.py` l.160 (lidas do HTML do arXiv 2404.03002 em 28/09) [KNOWN] |
| Planck 2018 comprimido (R, ℓ_A, ω_b): média + `PLANCK_COV` | `d1_v3_pipeline.py` l.33 (literal) | — | — | [REAL] literal; a cov do pipeline tinha correlações mal transcritas (D1F-03) |
| Chen, Huang & Wang 2019 (arXiv:1808.05724) PDF — Tabela I (σ e correlações 0,46/−0,66/−0,33) | `C:\IALD\Bancada_Um\fontes_externas\chen_huang_wang_2019_1808.05724.pdf` | 6.273.047 | 09effe1d0d8caa01 | [KNOWN — PDF em disco]; é a cov usada por `planck_cov = chen2019` |
| MANIFESTO_D1_V3.json · D1_CAMB_V3_REAL_RESULT.json | `…\cache\d1_camb\v3\` | 1.294 · 6.655 | 6e31e7f07db757e3 · f048b17f12674f33 | [REAL] |
| Cronômetros Moresco+2022 (32 pontos) | `C:\IALD\Bancada_Um\fontes_externas\moresco_2022_cc.json` | 1.892 | 530db89807c02723 | [REAL] importado por AST do artigo 1 (`tgl_paper_unified.py` 1.216.423 B, sha16 29c92b66b2fd6b4d, l.1181–1197) |
| Covariância Moresco+2020 (IMF+SPS; 15 pontos de Moresco) | `…\fontes_externas\moresco_2020_cov.json` (cópia idêntica no cache do rito `bancada_01out`) | 35.984 | 1c22a3a3f101834f | [REAL] arquivos do gitlab CCcovariance por sha256 dentro do json |
| Tabela CAMB ΛCDM | `C:\IALD\Bancada_Um\tabelas\camb_lcdm_v1.npz` (+ `.json` 590 B) | 223.602 | 6bc4dd4a09232500 | [REAL] |
| Fase 1 PREREG · RESULTADO · RELATORIO | `C:\IALD\Bancada_Um\investigacao\fase1_eff_30set\` | 4.449 · 28.781 · 9.934 | f0133c95a32d2dff · 165e3715d8c5d58f · 3a6839d67f15c411 | [REAL] |
| Fase 2 PREREG · RESULTADO · RELATORIO | `…\fase2_dois_setores_30set\` | 5.364 · 24.879 · 8.876 | 1f103573f28bc0f3 · 80735aa770c8c7c5 · ed80d3d3152d73be | [REAL] |
| Fase 4 PREREG · RESULTADO · SMOKE · RELATORIO | `…\fase4_desvio_30set\` (cópias idênticas no cache `bancada_30set`) | 9.812 · 44.444 · 1.355 · 7.682 | 22b4c440d8ad844d · 10683b334d28d84a · 5fb33c410edc6eea · 8cb9c8b208cd5c32 | [REAL] |
| Fase 7 PREREG · RESULTADO · RELATORIO | `…\fase7_cc_covariancia_01out\` (cópias no cache `bancada_01out`) | 7.183 · 44.122 · 4.834 | 36e354d547895d1d · 4f2671cbce7576f6 · 50f89754f73bdac9 | [REAL] |

### 1.5 Os valores publicados JÁ NA CASA (Fase 3, 30/09 — gravados por hash no pré-registro; os abstracts foram lidos na fonte em 30/09 mas NÃO foram guardados)

`C:\IALD\Bancada_Um\investigacao\fase3_leitores_h0\PREREGISTRO_FASE3_LEITORES_20260930.json` (7.966 B, sha16 6bf24b350e088350) → `leitores_de_sombra` / `fundos`:

| leitor | H0 ± σ | fonte (como a casa gravou) | estatuto |
|---|---|---|---|
| S1 SH0ES-JWST Cefeidas | 73,49 ± 0,93 | Riess et al. 2025, arXiv:2509.01667 (abstract lido 30/09) | [KNOWN]; «MOTIVOU a forma da lei» (não é incidência nova) |
| S2 CCHP TRGB | 70,39 ± 1,936 | Freedman et al. 2025, arXiv:2408.06153v3 (abstract lido 30/09); stat, sys e σ_SN em quadratura | [KNOWN] — é o «70,4 ± 1,9» da gerência |
| S3 SBF-TRGB-JWST | 73,8 ± 2,404 | Jensen et al. 2025, arXiv:2502.15935 | [KNOWN] |
| S4 masers | 73,9 ± 3,0 | Pesce et al. 2020, arXiv:2001.09213 | [KNOWN] |
| S5 TDCOSMO lentes | 71,6 ± 3,6 (+3,9/−3,3 simetrizado) | TDCOSMO 2025, arXiv:2506.03023 | [KNOWN] |
| S6 sirenes LVK O4a | 76,6 ± 11,25 (+13,0/−9,5) | LVK O4a cosmology summary (PDF lido 30/09) | [KNOWN]; vetável |
| fundo Fc Planck 2018 | 67,36 ± 0,54 | Planck 2018 VI, TT,TE,EE+lowE+lensing | [KNOWN] |
| fundo Fa TGL Planck+DR2 · Fb Planck só · Fd ΛCDM Planck+DR2 | 69,200 ± 0,304 · 68,19 ± 0,618 · 68,531 ± 0,301 | Bancada (30/09) | [REAL] |
| R22 SH0ES | 73,04 ± 1,04 | literal `sh0es_mean=73.04`, `SH0ES_SIGMA = 1.04` em `d1_v3_pipeline.py` l.37/44 | [KNOWN] |
| Brout+22 (alvo da validação da Fase 5) | 73,6 ± 1,1; Ω_m 0,334 ± 0,018 | memória da gerência | [DECLARADO — não lido da fonte] |
| TRGB CCHP (artigo multiprobe, maio/2026) | 69,80 ± 1,70 | `Manuscrito\tgl_multiprobe_paper_v1.tex` l.636 (cita Freedman2024 «Status Report on the CCHP, ApJ in press (2024)») | [KNOWN — versão anterior do mesmo programa] |
| Megamasers MCP (idem) | 73,90 ± 3,00 | idem l.635 | [KNOWN] |

Resultados da Fase 3 com esses leitores (RESULTADO 14.451 B, sha16 e91f019bd98e5a59): família A (fundo TGL 69,2) r̄ = 1,0548 ± 0,0112; z vs lei −2,94; S2 (TRGB) z −2,49; família D (fundo Planck 2018) S2 z −1,43; família E (fundo ΛCDM 68,531) S2 z −2,12. Independência: «S1, S2 e S3 partilham a amostra de SNe do fluxo de Hubble (σ_SN ≈ 0,7 comum)» — declarada, **não modelada**. Fator da lei na Fase 3 = K_D1a = 1,087799 (não o D1b).

[DERIVED dos números da casa, aritmética simples] Sob D1b (H0_bg 68,4298 × K 1,083807 = 74,1647), o TRGB da casa (70,39 ± 1,936) fica a (70,39 − 74,1647)/1,936 = −1,95σ — é o «1,9σ abaixo» da gerência; o SH0ES-JWST 2025 (73,49 ± 0,93) a −0,73σ; TDCOSMO (71,6 ± 3,6) a −0,71σ; SBF (73,8 ± 2,40) a −0,15σ; masers (73,9 ± 3,0) a −0,09σ. Nada disto é veredito; é leitura dos números já em disco.

---

## 2. A LER DA FONTE (nomeada; o valor existe na casa só como literal/abstract lido; sem PDF em disco)

| fonte | o que a casa tem | o que falta |
|---|---|---|
| Brout et al. 2022, ApJ 938, 110 (arXiv:2202.04077) | alvo 73,6 ± 1,1 [DECLARADO] | ler o valor e a convenção (amostra, calibradores) na fonte: o alvo da validação da Fase 5 precisa deixar de ser [DECLARADO] |
| Riess et al. 2022, ApJL 934, L7 (arXiv:2112.04510) | 73,04 ± 1,04 literal | PDF/tabela com a covariância da escada (se a Fase 9 quiser o SH0ES completo dos ancoradouros) |
| Riess et al. 2025, arXiv:2509.01667 (SH0ES-JWST) | 73,49 ± 0,93 (abstract) | PDF; o «JWST 2024 Riess 72,6 ± 2,0» citado pela gerência **não está na casa** (0 hits; seria arXiv:2408.11770, a nomear e ler) |
| Freedman et al. 2024/25, arXiv:2408.06153v3 (CCHP) | 70,39 ± 1,94 (abstract; stat+sys+σ_SN) | PDF; a separação TRGB / JAGB / Cefeidas (a casa gravou só o combinado) |
| Jensen et al. 2025, arXiv:2502.15935 (SBF-TRGB-JWST) | 73,8 ± 2,40 (abstract) | PDF |
| Pesce et al. 2020, arXiv:2001.09213 (masers) | 73,9 ± 3,0 (abstract) | PDF |
| TDCOSMO 2025, arXiv:2506.03023 | 71,6 +3,9/−3,3 (abstract) | PDF; o erro assimétrico (foi simetrizado) |
| Planck 2018 VI (arXiv:1807.06209) | 67,36 ± 0,54 [KNOWN]; o comprimido (R, ℓ_A, ω_b) via Chen+2019 (PDF em disco) | PDF do Planck; **cadeias/posteriores (PLA) ausentes** |
| DESI 2024 VI (arXiv:2404.03002) DR1 | 12 linhas literais + correlações lidas do HTML em 28/09 | PDF |
| DESI DR2 2025 (arXiv:2503.14738) | dados mean/cov (CobayaSampler) em disco | PDF; a «escada inversa DESI DR2 + BBN 68,5 ± 0,6» **não está na casa** (0 hits) — a nomear e ler |
| LVK O4a cosmology summary | 76,6 +13,0/−9,5 (PDF lido 30/09, não guardado) | PDF |
| Moresco et al. 2022 LRR | 32 pontos via artigo 1 | PDF (a tabela foi importada do artigo 1, não da fonte) |

Regra de leitura para a Fase 9 (herdada do pré-registro da Fase 5): o alvo entra com hash da fonte, não de memória; «[DECLARADO]» fica dito onde ainda for memória.

---

## 3. AUSENTE (consulta citada)

1. **Cadeias/posteriores do Planck 2018 (PLA) em disco: AUSENTE.** Glob `**/*{plikHM,paramnames,CosmoParams,planck_2018,base_plikHM}*` sob `C:\IALD` → só `tgl_pycbc_env\Lib\site-packages\getdist\styles\planck.paramnames` (estilo do getdist, não cadeia); `buscar.py "plikHM|COM_CosmoParams|base_plikHM_TTTEEE"` → 0 arquivos de dado (só índices e tool-results); `observaveis_tgl\tgl_data_cache\cmb\` e `\desi\` VAZIOS. O que a casa tem do CMB: o comprimido (R, ℓ_A, ω_b) e, no Nível 2 de agosto, a plik_lite dentro do Boltzmann (um.py l.204686) — cujas cadeias são PRÓPRIAS: `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\13_nivel2_chains.h5` (51.839.136 B, sha16 af118c94a693ac3c; resultado 13_nivel2_resultado.json 4.205 B, sha16 d3c09d15dfe65a53).
2. **Covariância entre os calibradores locais (S1–S3, σ_SN ≈ 0,7 comum): AUSENTE** — declarada no pré-registro da Fase 3 (`independencia`), tratada como independente. A Fase 9 «com covariância completa» precisa construí-la ou lê-la da fonte (R22/Brout+22/CCHP partilham o Pantheon+).
3. **Escada inversa publicada (BBN + BAO, sem CMB): AUSENTE.** O mais próximo na casa é o fundo ΛCDM da Bancada Planck-comprimido + DR2 = 68,531 ± 0,301 [REAL] — que USA o Planck comprimido, logo não é a escada inversa independente do CMB. A prior BBN de ω_b não foi inventariada nesta lente (o Nível 2 cita «BBN and τ priors»).
4. **Riess JWST 2024 «72,6 ± 2,0»: AUSENTE** (`buscar.py "72[.,]6 ?(±|\\pm) ?2[.,]0"` → 0 arquivos). **«70,4 ± 1,9»: 0 hits literais**, mas o valor está na casa como 70,39 ± 1,936 (Fase 3). **«68,5 ± 0,6»: 0 hits.**
5. **PDFs das fontes da Fase 3: AUSENTES** (abstracts «lidos 30/09» sem cópia). Os três PDFs de webfetch que o índice do acervo lista para «escada inversa», «JAGB» e «CCHP» (`d554e796…\tool-results\webfetch-1787147312149-1p62wp.pdf`, `da691dac…\webfetch-1786232688537-204ufu.pdf`, `…1786232977500-1ebkf4.pdf`) **não existem mais em disco** (`ls`: No such file); o único webfetch sobrevivente naquela pasta é Cadamuro–Fröb–Minz, arXiv:2312.04629 (Hamiltoniano modular de férmions massivos), 17/09 — nada de H0.
6. **O índice do acervo está velho para esta lente**: `INDICE_DO_ACERVO.json` é de 03/09/2026 (2.026.744 B, sha16 5d66b0db4a05b367) — não cobre `C:\IALD\Bancada_Um` (28/09+), as Fases 1–7, nem a v386. Tudo da Bancada foi achado pelo MAPA DE ROTAS, não pelo `buscar.py`.
7. **Registro de identidade do `Pantheon+SH0ES.dat` com o oficial: AUSENTE** (só a covariância tem `identidade_pantheon_cov.json`). O sha256 do .dat está gravado nos resultados (1cb0fc37…); a conferência contra o raw oficial é ato da gerência (exige rede).

---

## 4. Achados do aferidor (classificação: EXISTE E ESTÁ LIGADO → EXISTE MAS NÃO LIGADO → MEDIDA → AUSENTE)

- **A1 [REAL]** Todos os números da Fase 4 e da Fase 5 citados pela gerência batem dígito a dígito com o core v386 lido por script (ver §1.2 e §1.1). Hashes do core = hashes dos arquivos em disco hoje.
- **A2 [REAL]** O alvo da validação da Fase 5 (73,6 ± 1,1) é [DECLARADO] no pré-registro, no resultado, no core e no veredito (`…VS_DECLARED_TARGET…`); Brout+22 não está em disco. EXISTE NA CASA (o número) MAS NÃO ESTÁ LIGADO À FONTE.
- **A3 [REAL]** Três K diferentes vivem na casa: K_D1a = (1+z*)^β = 1,087799 (Fase 3), K_D1b = E(z*)^{2β/3} = 1,083807 (Fase 4, fundo nu 68,4298) e 1,083814 (Fase 5, P·sombra, fundo 68,393), 1,083977 (SMOKE da Fase 5, θ de Planck+DR2 sem SNe, H0 68,53). A convenção vigente (30/09) é D1b; a Fase 9 precisa fixar o fundo que define K (decisão do operador: «qual fundo é o fundo», ainda aberta no relatório consolidado de 01/10).
- **A4 [REAL]** Os seis leitores publicados (TRGB inclusive) já estão pré-registrados por hash na Fase 3 com fontes nomeadas — a Fase 9 não parte do zero; falta a covariância entre eles e o PDF das fontes.
- **A5 [REAL]** `DIAGONAL_ERRORS_ONLY` da Fase 4 refere-se aos cronômetros; a escada (Pantheon+SH0ES) já entrou com a covariância STAT+SYS completa na Fase 5. A covariância da Fase 7 (Moresco+2020) cobre só os 15 pontos de Moresco; os 17 outros seguem diagonais (dito).
- **A6 [REAL]** A validação V da Fase 5 foi rodada três vezes (desvio de protocolo dito nos logs `_tentativa1/2`); o estimador de V não estava fixado no pré-registro além de «ΛCDM». Para a Fase 9, fixar o estimador da validação antes de abrir.
- **A7 [REAL]** A lei da prova da casa (05/10): «pós-dição» nunca é demérito; o critério é a novidade de uso. O artigo v386 (l.165845) ainda diz «pós-dição declarada; zero parâmetro ajustado» — a v387 reescreve; o `fator_lei` e β não foram ajustados a nenhum leitor (β = α√e em runtime; K fixado pelo fundo).

## 5. Decisões do operador (não tomadas aqui)

1. Qual fundo define K na Fase 9 (ΛCDM nu Planck-comp + DR2, como na Fase 4; ou Planck 2018 publicado; ou Planck só) — «qual fundo é o fundo».
2. Se o S6 (sirenes LVK O4a, ± 11) entra ou é vetado; se o S1 (SH0ES, que motivou a lei) entra na família primária ou só na réplica (novidade de uso: Worrall).
3. Se as fontes (PDFs) devem ser baixadas e guardadas por hash pela gerência (esta lente não baixa) antes de abrir — em especial Brout+22, Freedman 2024/25, Riess 2024 e 2025, TDCOSMO 2025, DESI DR2 (escada inversa).
4. Se a correlação S1–S3 (σ_SN comum) entra modelada ou como faixa.
5. Registrar a identidade byte a byte do `Pantheon+SH0ES.dat` com o raw oficial (ato da gerência; exige rede).
