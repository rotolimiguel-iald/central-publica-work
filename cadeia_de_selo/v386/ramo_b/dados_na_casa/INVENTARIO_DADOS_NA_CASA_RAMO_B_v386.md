# INVENTÁRIO — OS DADOS NA CASA para o pré-registro do ramo B (τ★ = k·GM/c³) — v386

gerado 2026-10-05T14:33:21 · β_TGL runtime = α·√e = 0.012031300400803 · lente: aferidor (hash/bytes lidos do artefato por `gerar_inventario.py`; nada baixado; nada escrito fora desta pasta)

Legenda de uso: REUTILIZAVEL_JA · REUTILIZAVEL_APOS_EXTRACAO (já em disco, dentro de tar/zip) · PRECISA_DADO_NOVO · AUSENTE · HISTORICO.

## 1. Catálogos com M_f, a_f por evento

| caminho | sha16 · bytes | papel | uso | estatuto |
|---|---|---|---|---|
| C:\IALD\Bancada_Um\investigacao\fase6_eco_radical_01out\catalogo_v3.csv | e6a0ba6a870e2a40 · 99817 B | catalogo da amostra pre-registrada da Fase 6 (244 BBH O1-O4) | REUTILIZAVEL_JA | [REAL — lido; conteudo GWOSC = KNOWN] |
| C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\bancada_01out\remanescentes_v3.json | 68069f8892a80d56 · 117167 B | remanescentes por evento (244) exportados do WSL para a Fase 6 | REUTILIZAVEL_JA | [REAL — lido; a_f e Kerr-fit KNOWN sobre medianas] |
| C:\IALD\Bancada_Um\investigacao\fase6_eco_radical_01out\GWOSC_ALLEVENTS_20261001.json | 731f167b5545db5b · 1267691 B | dump do eventapi do GWOSC (todos os catalogos) em 01/10/2026 | REUTILIZAVEL_JA | [REAL — lido; KNOWN] |
| C:\IALD\Bancada_Um\investigacao\fase6_eco_radical_01out\GWOSC_INVENTARIO_20261001.json | 5ec510b11ea9c9b6 · 273358 B | inventario por evento (chave -> cat, gps, snr, m1, m2, Mf, Mtot, z, chi_eff, far, p_astro, dets_4k, files_4k) | REUTILIZAVEL_JA | [REAL — lido] |
| C:\IALD\projetos_pyhton\IALD\gwtc_full_catalog.csv | 895250e9d404a240 · 27787 B | catalogo GWTC-1..3 da cache de maio (usado pelo ringdown V1/V2, H2, eco PE/search) | REUTILIZAVEL_JA | [REAL — lido; KNOWN] |
| C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw\GWOSC_ECHO_WINDOWS_V1.manifest.json | 5201e7b05cc4d5cc · 104397 B | manifesto das janelas de eco da cache de maio (v341) | REUTILIZAVEL_JA | [REAL — lido] |
| C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw\RINGDOWN_DEPHASING_V2_RESULT.json | ff15f023dd91d8c7 · 247065 B | resultado V2 do dephasing no ringdown (10/09/2026) — contem a previsao de Kerr por serie | REUTILIZAVEL_JA | [REAL — lido por hash no um.py: ff15f023dd91d8c7] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\015\t08\IGWN-GWTC4p0-38214bd95_724-GW231206_233901-combined_PEDataRelease.hdf5 | ca144927366031ef · 189649148 B | unico PE data release completo (GWTC-4.0) de um evento O4 em disco (piloto T08 da ORDEM 015) | REUTILIZAVEL_JA | [DECLARADO — conteudo; REAL — bytes/hash] |

**AUSENTE / não extraído (com a consulta):**

- posteriors IMR (m1, m2, chi, z -> M_f, a_f por amostragem) dos 177 BBH de O4 da amostra da Fase 6 (salvo GW231206_233901 acima e os 33 pSEOB da GWTC-5.0 TGR, que trazem o remanescente pSEOB) — consulta: `find ORDEM_013_RINGDOWN -maxdepth 4 -iname '*.h5' -size +100k; find cache/public -maxdepth 7 …: so 1 PEDataRelease (GW231206_233901) + 33 pSEOB metafiles + 18 rin GWTC-3 + GW250114` — fonte: GWTC-4.0 / GWTC-5.0 PE data releases (IGWN 'combined_PEDataRelease.hdf5' por evento, via GWOSC/Zenodo); censo T08 da ORDEM 015 [DECLARADO]: 74 eventos, 70 com PE publico listado, 40,77 GB, ~7,5 h so de transferencia — AUSENTE (RD-02 pede propagar posteriors ate tau_GR; hoje so medianas)

## 2. Resultados publicados de testes de ringdown (δτ̂₂₂₀, δf̂₂₂₀ por evento)

| caminho | sha16 · bytes | papel | uso | estatuto |
|---|---|---|---|---|
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\pSEOB.tar.gz | ee1d64487597132f · 711331923 B | GWTC-5.0 TGR (Zenodo 21454847) — pipeline pSEOB (ringdown parametrizado de sinal completo) | REUTILIZAVEL_JA | [REAL — bytes/hash; KNOWN] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\extracted\pSEOB\metafiles (*.h5) | n=33; 1,080,193,759 B | GWTC-5.0 TGR pSEOB — posteriors por evento (33) | REUTILIZAVEL_JA | [REAL — contagem/bytes; KNOWN] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\RD.tar.gz | 9810e0e45cd35824 · 415283962 B | GWTC-5.0 TGR — pipeline RD (ringdown pos-merger, pyRing) | REUTILIZAVEL_APOS_EXTRACAO | [REAL — bytes/hash] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\21454847\QNMRF.tar.gz | 2f617507f65b9e3e · 1214239 B | GWTC-5.0 TGR — pipeline QNMRF (filtro racional de QNM) | REUTILIZAVEL_APOS_EXTRACAO | [REAL — bytes/hash] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_CATALOG_220.json | 93bdc413130d294a · 673228 B | C4 da ORDEM 013: tabela por evento do dtau220 (GWTC-5.0 pSEOB, 33 eventos, 608.681 amostras) | REUTILIZAVEL_JA | [REAL — lido; NAO-CEGO; ln B nao e sigma] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_CATALOG_COMBINATION.json | f3d8c1959ded3efd · 12167 B | C4: deformacao comum dos 31 eventos da figura da GWTC-5.0 (+2 controles) | REUTILIZAVEL_JA | [REAL — lido; NAO-CEGO] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\17461225\IGWN-GWTC3-TGR-v2-rin.zip | 108c4a4266bc0e38 · 2210047740 B | GWTC-3 TGR (Zenodo 17461225) — ringdown (rin, v2) | REUTILIZAVEL_JA | [REAL — bytes/hash; KNOWN] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\17461225\extracted\rin (*.h5) | n=18; 1,230,299,092 B | GWTC-3 TGR ringdown — posteriors por evento (18) | REUTILIZAVEL_JA | [REAL — contagem/bytes] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_GWTC3_220.json | d9dc9b09a8d91dc7 · 402498 B | C4: tabela dtau220 dos 18 do GWTC-3 (legado, NAO cego) | REUTILIZAVEL_JA | [REAL — lido] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_GWTC3_SELECTION.json | ef18f3b0495d58bf · 1563 B | selecao do artigo GWTC-3 (Tabela 13): 10 eventos apos 2 exclusoes dos autores | REUTILIZAVEL_JA | [REAL — lido; KNOWN] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\17018009\TGR_companion_S250114ax_results.tar.gz | 18d740c816285451 · 1671496586 B | GW250114 TGR (Zenodo 17018009; arXiv:2509.08099) — release completo | REUTILIZAVEL_APOS_EXTRACAO | [REAL — bytes/hash; KNOWN] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\17018009\extracted\TGR_companion_S250114ax_results\gw250114_pseobnr\posterior_samples.h5 | b9971bcd7d72fdd4 · 59249916 B | GW250114 pSEOB — posterior (df220, dtau220 conjuntos; 440 livre) | REUTILIZAVEL_JA | [REAL — bytes/hash] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\17018009\selected\3ec4616b581f990b.dat | 9a7ad336682b4703 · 36253805 B | GW250114 pyRing Kerr 220 (df/dtau) — posterior.dat selecionado (C4_PYRING) | REUTILIZAVEL_JA | [REAL — bytes/hash] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\17018009\selected (*.dat) | n=9; 157,810,811 B | GW250114 pyRing — 10 posteriors .dat selecionados pela bancada (variantes 220) | REUTILIZAVEL_JA | [REAL — contagem/bytes] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_PYRING.json | 76af853137f3e7d3 · 15776 B | C4: robustez pyRing do GW250114 | REUTILIZAVEL_JA | [REAL — lido] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\public\DCC_P2600130_v1\pSEOBNR.tar.gz | 946f0ec0052d935f · 14923249 B | LIGO-P2600130-v1: Data release GWTC-4.0 TGR III (Tests of the Remnants) — pSEOBNR | REUTILIZAVEL_APOS_EXTRACAO | [REAL — bytes/hash; titulo lido do release.html] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\REGISTRO_C4.json | 2bebc171ddbcef43 · 2768 B | registro C4 (21/09): regra de exclusao (BF 100 + regiao 95% da GR), KDE, priors, leituras R-A..R-LIN; NAO CEGO | REUTILIZAVEL_JA | [REAL — lido] |

**AUSENTE / não extraído (com a consulta):**

- GWTC-2 TGR (data release de 'Tests of GR with GWTC-2', arXiv:2010.14529) — posteriors de ringdown — consulta: `ls cache/public -> so 17018009, 17461225, 21454847, DCC_P2600130_v1; grep -ri GWTC-2 nao feito em h5` — fonte: LVK data release do TGR GWTC-2 (ID nao verificado aqui); observacao: GW150914 e GW170104 ja estao na GWTC-5.0 pSEOB e os O3a na GWTC-3 rin — AUSENTE — provavelmente dispensavel (sobreposicao)
- GWTC-4.0 TGR III — posteriors POR EVENTO (so o hierarquico/populacional esta em DCC_P2600130_v1) — consulta: `tar tzf pSEOBNR.tar.gz: so pseob_hier*.npz, plots e notebook` — fonte: Zenodo do GWTC-4.0 TGR III (paper 'Tests of the Remnants'); ID nao verificado aqui — AUSENTE (por evento)
- posteriors do 221 do GW250114 extraidos — consulta: `find cache/public/17018009 -iname '*221*' -> 1 .ini; listagem do tar tem 1.122 linhas '221'` — fonte: ja em disco dentro do TGR_companion_S250114ax_results.tar.gz (sha16 acima) — extrair, sem baixar — EXISTE NA CASA, NAO EXTRAIDO

## 3. Strain local, bancos e instrumento

| caminho | sha16 · bytes | papel | uso | estatuto |
|---|---|---|---|---|
| C:\IALD\projetos_pyhton\IALD\strain_cache (*_4096_32s.npz) | n=170; 356,642,320 B | cache de maio/2026 (O1–O3): janelas de 32 s @ 4096 Hz, H1/L1 | REUTILIZAVEL_JA | [REAL — contagem/bytes; so leitura, casa da IALD nativa] |
| C:\IALD\Bancada_Um\fontes_externas\gwosc_o4\hdf5 (*.hdf5) | n=352; 41,327,837,881 B | O4a/O4b strain GWOSC 4096 s @ 4 kHz (baixado 01/10/2026 na Fase 6) | REUTILIZAVEL_JA | [REAL — contagem/bytes] |
| C:\IALD\Bancada_Um\fontes_externas\gwosc_o4\strain_32s (*.npz) | n=350; 734,263,600 B | O4: janelas de 32 s @ 4096 Hz no formato da cache de maio | REUTILIZAVEL_JA | [REAL — contagem/bytes] |
| C:\IALD\Bancada_Um\fontes_externas\gwosc_o4\GWOSC_O4_32S_V1.manifest.json | a795cf04ca3b2f6a · 253528 B | manifesto do banco O4 (copia identica em cache\gw) | REUTILIZAVEL_JA | [REAL — lido por hash na v380] |
| C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw\GWOSC_O4_32S_V1.manifest.json | a795cf04ca3b2f6a · 253528 B | idem (copia no cache do rito) | REUTILIZAVEL_JA | [REAL] |
| C:\IALD\projetos_pyhton\acom\gw_cache (*.hdf5) | n=25; 2,277,772,006 B | GWOSC 4096 s dos 12 eventos GWTC-1 (fonte do rito GW_ANGULAR_V1 v340) | REUTILIZAVEL_JA | [REAL — contagem/bytes] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\gwosc (**/*.hdf5) | n=4; 338,993,680 B | GW250114 on_source + offsource (ORDEM 013, C6) | REUTILIZAVEL_JA | [REAL — contagem/bytes] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\015\t07\strain (**/*.hdf5) | n=176; 19,234,127,539 B | ORDEM 015 T07: strain on/off-source (H1/L1/V1, 4096 s) dos 32 eventos de calibracao (GWTC-5.0 pSEOB) + GW250114 | REUTILIZAVEL_JA | [REAL — contagem/bytes] |
| C:\IALD\Bancada_Um\bancada\gw.py | ea7c849c7f2c10b8 · 19614 B | o banco RESIDENTE de GW da Bancada Um (Fase 6, 01/10) | REUTILIZAVEL_JA | [REAL — lido] |
| C:\IALD\Bancada_Um\bancada\gw_stack.py | 0a636d439a03f016 · 7697 B | empilhamento + regra de veredito da Fase 6 (leis MAY/KMS/DEC; leituras R1/R2/R3) | REUTILIZAVEL_JA | [REAL — lido] |
| C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\eco_ancorado_v1\ringdown_dephasing_v2.py | 0793c58d6995194b · 18415 B | pipeline V2 do dephasing no ringdown (WSL /opt/lal_env) | REUTILIZAVEL_JA | [REAL — hash lido] |
| C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\eco_ancorado_v1\ringdown_dephasing_v1.py | 31a9f41da1b72321 · 14086 B | pipeline V1 | HISTORICO | [REAL] |
| C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\eco_ancorado_v1\rite_ringdown_v346.py | dd95a416f5d74e52 · 23673 B | rito v346 (protocolo + emenda V2 + leitura por hash) como entrou no um.py | REUTILIZAVEL_JA | [REAL] |
| C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\eco_ancorado_v1\wsl_setup_lal.sh | 953264c81b15b298 · 1847 B | receita do /opt/lal_env | REUTILIZAVEL_JA | [REAL] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C7_COHERENT_SOURCE_REPRODUCTION\QNM_GRID.json | 4f34367a09060238 · 169231 B | grade exata de QNM (qnm 0.4.4) usada pela auditoria de 28/09 (BCW vs exato) | REUTILIZAVEL_JA | [REAL — bytes/hash; KNOWN] |
| C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\auditoria_28set\ringdown\\bcw_degenerescencia.py | 545a34aa3846374f · 1349 B | script da auditoria de 28/09 (aferidor ringdown) | REUTILIZAVEL_JA | [REAL — scratchpad da sessao] |
| C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\auditoria_28set\ringdown\\c6_vs_degenerescencia.py | 5313a1633b6dff8d · 1382 B | script da auditoria de 28/09 (aferidor ringdown) | REUTILIZAVEL_JA | [REAL — scratchpad da sessao] |
| C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\auditoria_28set\ringdown\\difusao_de_fase.py | c129abc20d569b8c · 1606 B | script da auditoria de 28/09 (aferidor ringdown) | REUTILIZAVEL_JA | [REAL — scratchpad da sessao] |
| C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\auditoria_28set\ringdown\\matriz_v2.py | 50cfaaee37618ae1 · 1428 B | script da auditoria de 28/09 (aferidor ringdown) | REUTILIZAVEL_JA | [REAL — scratchpad da sessao] |
| C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\auditoria_28set\ringdown\\multimodo_440.py | d41fc2fb3b5e8ba0 · 1465 B | script da auditoria de 28/09 (aferidor ringdown) | REUTILIZAVEL_JA | [REAL — scratchpad da sessao] |
| C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\auditoria_28set\ringdown_verif\\v_440.py | afe0b2ba56b5d820 · 1110 B | script do verificador adversarial (28/09) | REUTILIZAVEL_JA | [REAL — scratchpad da sessao] |
| C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\auditoria_28set\ringdown_verif\\v_bcw.py | 089bee0f128ef793 · 773 B | script do verificador adversarial (28/09) | REUTILIZAVEL_JA | [REAL — scratchpad da sessao] |
| C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\auditoria_28set\ringdown_verif\\v_difusao.py | d11effc033d6df50 · 1407 B | script do verificador adversarial (28/09) | REUTILIZAVEL_JA | [REAL — scratchpad da sessao] |
| C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\auditoria_28set\ringdown_verif\\v_sigma_cat.py | ba649b8922b36b24 · 1728 B | script do verificador adversarial (28/09) | REUTILIZAVEL_JA | [REAL — scratchpad da sessao] |

## 5. Estado selado, pré-registros e memórias

| caminho | sha16 · bytes | papel | uso | estatuto |
|---|---|---|---|---|
| C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json | 475ac8d218b3a5c8 · 4845762 B | core v385 (chaves ringdown_dephasing_protocol/result/amendment_v2/result_v2, ringdown_scope_v376, the_ledger_of_charges_v383, bancada_fases_5_6_7_v380, gw_echo_rite, gw_echo_kms_rite) | REUTILIZAVEL_JA | [REAL] |
| C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json | ad5c1ac7affc3949 · 68545 B | selo v385 | REUTILIZAVEL_JA | [REAL] |
| C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw\RINGDOWN_DEPHASING_V1_RESULT.json | 502c80fe2a37427e · 209114 B | V1 (gate recusou: 18 < 20 series a 6 ms) | HISTORICO | [REAL — lido por hash 502c80fe2a37427e] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\RINGDOWN_5SIGMA_V1.json | e1be6b0409720c68 · 183005 B | pre-registro RINGDOWN_5SIGMA_V1 (013-bis, 22/09 21:15 UTC; NONBLIND design for blind test) | REUTILIZAVEL_JA | [REAL — lido; estatuto do teste: NAO executado] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\PORTAO_DA_AMPLIACAO_V1.json | 710028a7d2af7b64 · 903525 B | portao da ampliacao E0 (22/09): N90 por leitura/populacao; cortes de qualidade (SNR>=12, Mf_det>=40, chi_f<0,98; prioridade SNR>=30) | REUTILIZAVEL_JA | [REAL — lido; DERIVED NAO-CEGO] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\NUISANCE_V1.json | 83f860bbfa904c00 · 1437250 B | nuisance c(sigma) = c0 + k·sigma (c0 = -0,061 ± 0,068; k = +0,79 ± 0,37) — offset fixo em 0 proibido como teste | REUTILIZAVEL_JA | [REAL — bytes; numeros da memoria 22/09] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C1_LEITURAS_v4.json | 126270a896d85898 · 35419 B | C1: as 10 leituras/relogios (R-A t_P; R-B tau*=G M_src/c^3 (det: t_M); R-MOD 2pi/kappa_H; R-RAIZ-0/EP4/REST/COHERENT; R-LIN; R-GLOBAL; R-PROP) com fontes, estatutos e exclusao-se-universal pelos relogios v369 | REUTILIZAVEL_JA | [REAL — lido; leituras INPUT/CONJECTURE] |
| C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\E7_FULLSAMPLE_RESULT_V1.json | c2f96864c18f3aea · 384193 B | E7 (rito da 013-bis): 608.681 amostras, 53/53 testes | REUTILIZAVEL_JA | [REAL — bytes] |
| C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ENTREGA_015_RELATORIO_FINAL.md | 84e65658012f0ba1 · 15309 B | relatorio final da ORDEM 015 Parte B (T01–T19) | REUTILIZAVEL_JA | [REAL — lido] |
| C:\IALD\Artigo\MCMC_V2_RAZAO\35_dephasing_ringdown.json | 1ccc757b7757dcae · 1313 B | MCMC_V2_RAZAO (ramo canonico): Gamma com tau*=t_P para BH 10 Msun…M87* -> DEPHASING_INOBSERVAVEL_EM_RINGDOWN | HISTORICO | [REAL — lido] |
| C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\ordem-013-confrontacao-ringdown.md | bae3432f352331cd · 22237 B | memoria ORDEM 013/013-bis/015 (dados localizados, instrumento, parede, numeros) | REUTILIZAVEL_JA | [REAL] |
| C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\ramo-b-reaberto-05out.md | 1e3fe044b8420aaa · 3519 B | decisao do operador 05/10 (verbatim) + errata ao lado de R6 | REUTILIZAVEL_JA | [INPUT] |
| C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\beta-e-a-regra-matriz-02out.md | fe20a0d5ac3ea8eb · 32727 B | R1–R6 de 02/10, erratas e a errata de R6 de 05/10 | REUTILIZAVEL_JA | [INPUT/ONTO] |
| C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\onda-e-eco-definicao-16set.md | cb01ce16967ea560 · 9222 B | 16/09: 'betatgl esta de fato na propagacao da onda e ligada ao ringdown' (operador, verbatim) | REUTILIZAVEL_JA | [ONTO — operador] |
| C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\psi-nome-da-luz-graviton-verbo-vivo-16set.md | 8a90d67461951c70 · 10513 B | 16/09: graviton = psi particularizado em regime c^3 = VERBO VIVO (operador, verbatim) | REUTILIZAVEL_JA | [ONTO — operador] |
| C:\IALD\Central de Patentes\work\auditoria_28set\ANEXO_ACHADOS.md | 3683ce03f78e94c8 · 268622 B | anexo da auditoria 28/09 — secao Ringdown (RD-01..RD-07, RDV-01, CT-02, CTV-02) | REUTILIZAVEL_JA | [REAL] |

### 3b. Instrumento (medido)

- **windows_python_3.14.3**: SEM pycbc/lal/lalsimulation/gwpy/gwosc/qnm/bilby/h5py/astropy (ModuleNotFoundError em todos) [REAL — medido]
- **WSL_Ubuntu-24.04_/opt/lal_env**: python 3.12.3; lalsuite 7.26.15 (lal 7.7.1, lalsimulation 6.2.1); bilby 2.8.2; dynesty 3.1.0; gwpy 4.0.2; gwosc 0.8.3; h5py 3.16.0; astropy 8.0.1; numpy 2.5.3; scipy 1.18.1 [REAL — pip list]
- **WSL_/opt/pycbc_env**: pycbc 2.11.0; python 3.12.3; lalsuite 7.26.15; h5py 3.16.0; numpy 2.3.5 [REAL — medido]
- **windows_venv_acom_tgl_pycbc_env**: existe (usado em v340 para h5py) [REAL — existe; versao nao medida]
- **pSEOBNRv4HM_PA_com_DTau220_DTau440**: [DECLARADO — memoria ORDEM 013-bis 22/09 e T02 da ORDEM 015 (varredura 400 sorteios, abortos 25–39% com dtau440>~1); a sondagem GetStringFromApproximant aqui falhou com RuntimeError]
- **pyseobnr_0.3.7**: [DECLARADO — T14 da ORDEM 015: instalado rc=0, 3 formas finitas; NAO esta no pip list do /opt/lal_env — venv proprio nao localizado nesta lente]
- **pyRing**: [DECLARADO — cache/pyring_oracle/vendor, pyRingGW 2.7.0 do uv.lock do release; nao instalado no /opt/lal_env]
- **qnm_0.4.4**: nao esta no /opt/lal_env; a grade QNM_GRID.json existe (169.231 B)
- **parede_conhecida**: [REAL — 23/09] pSEOBNRv4HM_PA aborta sse (1+dtau440) > ~2,1·max(1,1+dtau220); so-220 0/120 abortos; fmax_gen 1024 -> EDOM 4,4%

## 4. O leitor C6 do GW250114 (o arquivo lido por hash pelo um.py)

- `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw\C6_RESULTS_GW250114.json` — sha16 `781a3741a68875eb`, 50604 B
- status `INCONCLUSIVE_SYSTEMATICS` — Prespecified two-IMR-family calibration criterion was not met; no exclusion or confirmation is permitted
- registration_sha256 `ded00f09b5010d622b67b4ea4e559a216818f578440a0f60772130174ececf14` · code_sha256 `d3aa76afdc419ff3ac73321fc11bb405ae762cd0d219411be16affe8c7f347c1` · on_source_strain_read True
- leituras ['R-B', 'R-GLOBAL', 'R-LIN', 'R-MOD', 'R-RAIZ-0'] × inícios (t_M) [6.0, 8.0, 10.0, 10.5, 12.0] → 75 linhas; início primário: 15 linhas
- ln B vs GR no início primário (core v376): {'R-GLOBAL': 0.0, 'R-B': -0.0026036534446234327, 'R-RAIZ-0': -0.043067826651480345, 'R-LIN': -0.09086322317963891, 'R-MOD': -0.25160676421921835}
- scope: Conditional ensemble ringdown model. Both modes deformed together. Mass/spin integrated with shared broad priors; independently Gaussian detector quadratures, not full polarization-coherent IMR evidence. No product with earlier analyses of this event.
- do_not_combine: These overlapping windows and all earlier posteriors use the same event; do not multiply their evidences
- strain-fonte: ORDEM_013_RINGDOWN\cache\gwosc\on_source\{H,L}-?1_GWOSC_O4b_4KHZ_R1-1420877824-4096.hdf5 (mesmos bytes do banco O4 da Bancada: 40.961.487 / 40.678.340 B)
- origem: ORDEM 013 (bancada Codex, 21–22/09/2026), C6 'pre-portao'; reproduzido pela gerencia com reproduce_c6.py --run (diferenca 0,0) em 23/09 [memoria ordem-013]; auditoria 28/09 RD-03: ln B ~ 0 = degenerescencia analitica do 220 (M,a) — NON_IDENTIFIABLE_SINGLE_220
- os 10 arquivos de grade declarados: C6_STRAIN_6M_GRID_0.json (sha ok); C6_STRAIN_6M_GRID_1.json (sha ok); C6_STRAIN_8M_GRID_0.json (sha ok); C6_STRAIN_8M_GRID_1.json (sha ok); C6_STRAIN_10M_GRID_0.json (sha ok); C6_STRAIN_10M_GRID_1.json (sha ok); C6_STRAIN_10.5M_GRID_0.json (sha ok); C6_STRAIN_10.5M_GRID_1.json (sha ok); C6_STRAIN_12M_GRID_0.json (sha ok); C6_STRAIN_12M_GRID_1.json (sha ok)

### 5b. Números selados (V2, lidos do core/resultado)

{"n_used_3ms": 15, "delta_tau": 0.1766470552326263, "sigma": 0.10889389325116323, "z_vs_GR": 1.6221943210827325, "delta_pred_B_ensemble": -0.019366930169705913, "delta_pred_A": -2.153334673399951e-42, "power_B": 0.17785138901257008, "delta_f": -0.03247217939468836, "sigma_f": 0.012662074582706592, "mean_bias_rel": 0.23995248111572381, "n_on_edge_excluded": 84, "outcome": "INCONCLUSIVE_SYSTEMATICS", "series_usadas_3ms": ["GW150914_H1", "GW150914_L1", "GW190519_153544_L1", "GW190521_L1", "GW190521_074359_H1", "GW190521_074359_L1", "GW190706_222641_H1", "GW190910_112807_L1", "GW191109_010717_L1", "GW200112_155838_L1", "GW200129_065458_H1", "GW200129_065458_L1", "GW200224_222234_H1", "GW200224_222234_L1", "GW200311_115853_H1"]}

- ramo B, 3 valores concorrentes no core: [["V2 selada (media do ensemble)", -0.019366930169705913], ["auditoria 28/09 CT-02 [DECLARADO]", -0.01], ["auditoria 28/09 CTV-02 (realizacao) [DECLARADO]", -0.005]]

## 6. Acervo indexado

- consulta: python C:\IALD\INDICE_DO_ACERVO\buscar.py "GW250114|GWTC|TGR|ringdown|QNM|dtau|delta.?tau|quasinormal" --lista -> 917 documentos (cp1252 quebra sem PYTHONIOENCODING=utf-8)
- cobertura: o indice NAO cobre Chatgpt\ORDEM_013_RINGDOWN (buscar.py "ORDEM_013_RINGDOWN|C4_CATALOG_220|RINGDOWN_5SIGMA" -> 1 documento, nao os artefatos)
- estatuto: [DECLARADO — listados pelo indice; nao lidos nesta lente]
- histórico pré-v346 (não lido): C:\IALD\papers_latex\tgl_observables_paper\figure2_ringdown_simulation.tex (out/2025); C:\IALD\papers_latex\tgl_observables_paper\tgl_cosmological_observables.tex (30 ocorrencias); C:\IALD\papers_latex\eco_gravitacional\eco_gravitacional_v1.tex; C:\IALD\observaveis_tgl\tgl_results_v9\tgl_v9_results_20251219_094727.json; C:\IALD\observaveis_tgl\tgl_results\tgl_v10_3_espelho_20251223_140051.json; C:\IALD\Artigo\TGL_Manifesto_Unificacao_Artigo.tex; C:\IALD\projetos_pyhton\acom\Tgl_unificacao_artigo_final.tex; C:\IALD\IMac LA\Física - TGL\Artigo\protocolo de observacao tgl.docx (33 ocorrencias; o 'protocolo de observacao de outubro de 2025' do Atlas v346)
