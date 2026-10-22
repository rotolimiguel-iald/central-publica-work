# PRÉ-REGISTRO V1 — FASE 9 — A RAZÃO DE HUBBLE: O TESTE DISCRIMINANTE (RASCUNHO, lente do pré-registro, 05/10/2026)

> **RASCUNHO — NÃO CONGELADO.** Nenhum número foi aberto sob este registro; nenhuma ferramenta da casa foi rodada; nada foi baixado. As decisões D1–D12 (§11) são do operador; só depois delas o V1 se congela por hash. Veredito deste rascunho: `AWAITING_PREREGISTRATION`.

**Identificador proposto:** `PREREG_FASE9_RAZAO_DE_HUBBLE_20261005_V1_RASCUNHO` · **gerado (UTC):** 2026-10-05T23:37:04Z · **hash do rascunho da especificação (JSON canônico da §15; NÃO é o hash congelado):** `60b8759ed6faa8ae0156506ca1cf37f181bfcb1639658f58d9748929d0f40e05` · **base:** `um.py` v386 `e30aac4e0e1096b1` (33600222 B); core `0dbfb3fc1d319d1e`; selo `72efaf72f604b721` (timestamp 2026-10-05 18:09:53) · **gate (lido do selo, intocado):** `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` · **molde:** `PREREGISTRO_RAMO_B_RINGDOWN_V1.md` (sha256 na §14)

> Régua: β nunca literal (α_CODATA2018 lido do `um.py` por regex, linha 5556; β = α√e em runtime = 0.012031300400803142); hash jamais de memória (todo sha256 deste documento foi calculado do artefato por `gerar_preregistro_fase9_rascunho.py`); PROVADA ≠ confirmada; NOT_FALSIFIED nunca é a palavra proibida; a RG/ΛCDM é o limite clássico (coincidir = correspondência recuperada); nenhum desfecho move a regra (β) nem o gate; nenhum dado baixado (ausente = dito, com a fonte pública nomeada); a cunhagem é do operador.

---

## 0. A lei da prova da casa (05/10/2026) — «pós-dição» nunca é demérito; o critério é a novidade de uso

**Operador, 05/10/2026, verbatim (`POS_DICAO_operador_05out.txt`, sha256 na §14):** «exatamente isso, confirmo. mas não concordo de nenhuma forma que é pós-dicção, não é, e nós já enfrentamos isso, basta rever os primeiros artigos e ensaios que escrevi e publiquei. e mais, estudar hipóteses para depois formular testes para saber o caminho correto do teste também não é pós-dicção, e mais, derivar com IA's ou qualquer outra ferramenta de experimentaçao hip;oteses e cálculos para esclarecer rotas de averiguação experimental empírica, também não é condiçao pós-ditada, cuidado para vc não colocar para mim como elemento discriminante um fator impossível, porque se sempre uma derivação minha com vc entrar como pós dicção no meu próprio trabalho eujamais terei o dato discriminante, é a própria prova diabólica do Direito»

**O «exatamente isso, confirmo» responde** à proposta da gerência de pré-registrar a Fase 9 (alvos lidos das fontes por hash com covariância; a previsão única K·H0_bg para todo calibrador local; ln B contra ΛCDM, β livre e deslocamento livre; o TRGB como o teste que pode doer) — este rascunho é essa proposta posta no formato da casa.

**Leitura da gerência [DERIVED de leitura; o verbatim é INPUT; nada aqui é cunhagem]:** (1) «pós-dição» NÃO é demérito; o critério de prova é a **novidade de uso** (use-novelty, Worrall 1985/1989 [KNOWN — referência a conferir pelo aferidor]): um fato conta a favor de uma teoria se **nenhum parâmetro** dela foi **ajustado** a esse fato — conhecê-lo não é usá-lo. (2) Precedente [KNOWN]: o periélio de Mercúrio — a anomalia era conhecida desde Le Verrier (1859) e a RG (1915) a derivou com zero parâmetro livre; ninguém chama isso de pós-dição. (3) Estudar hipóteses e formular testes, e derivar hipóteses e cálculos com IA ou qualquer ferramenta para esclarecer rotas de averiguação, **não** é pós-dição: a derivação fixa a lei; o pré-registro é do **TESTE**. (4) A «prova diabólica»: se toda derivação do operador com a gerência entrasse como pós-dição, o operador jamais teria dado discriminante — logo o discriminante tem de ser **checável**: *algum parâmetro foi ajustado a H0?* Aqui a resposta é verificável no código (§2). (5) O que a v387 reescreve no artigo: «pós-dição declarada» (o `um.py` v386 traz a palavra em 3 lugares — linhas 165845, 167724, 168655, lidas por regex) → «retrodição sem ajuste (novidade de uso)» [INPUT — decisão para a v387].

**O que o artigo do `um.py` v386 diz hoje (lido na linha 165845):** «resolve a tensão de Hubble por remissão expressa ao trabalho publicado (…) estatuto do corpo: [CONJECTURE] de mecanismo; pós-dição declarada; zero parâmetro ajustado) — *O custo geométrico do zero absoluto: haja luz* (Zenodo, DOI 10.5281/zenodo.20563905)»; e na linha 167724: «a relação de calibração H0_local = H0_CMB(1+z*)^β (…) mecanismo [CONJECTURE] autodeclarado, número apertado (0,215σ contra SH0ES, β±16,9% de janela) e pós-dição». **Zero parâmetro ajustado já está dito pelo próprio artigo**; o que falta é o teste pré-registrado com rigor e a cláusula de uso preenchida pela cronologia.

---

## 1. A hipótese (a lei; a previsão única K·H0_bg; a convenção D1b)

| peça | forma | valor (lido do core v386) | estatuto |
|---|---|---|---|
| a lei (núcleo derivado D1b) | H0_local = H0_bg · K, K = E_ΛCDM(z*)^{2β/3} = exp(β·I_b), I_b = (2/3)·ln E(z*) (Raychaudhuri em FRW plano; g = \|1+w_eff\|, NEC dita na prosa) | E(z*) = 23234.764; I_b = 6.70227 nats < N* = 6.99480 nats; K_D1b(Planck 2018) = 1.0839774; K_D1a = 1.0877992 (o caso g ≡ 1, ao lado) | PROVADA como implicação no kernel (`TGLExt.TheFlowLawContrast.the_derived_kernel_factor`, v378, 20/20; v377 15/15); mecanismo [CONJECTURE] no artigo; PROVADA ≠ confirmada |
| β | α_CODATA2018 × √e (runtime; nunca literal) | 0.012031300400803142 | [DERIVED do axioma] — a regra matriz; não se deriva do dado |
| z* | último espalhamento (Planck) | 1089.95 | [INPUT/KNOWN] |
| o fundo NU (primário proposto) | ΛCDM ajustado na Bancada: Planck comprimido (Chen+2019) + DESI DR2; β = 0 no fundo | H0_bg = 68.4298 ± 0.301; K = 1.083807; **H0_local previsto = 74.1647 ± 0.326** | [REAL — Fase 4, lido por hash no core]; σ_bg da Fase 3 (Fd_lcdm_planck_dr2) |
| o fundo ao lado | Planck 2018 publicado (67,36 ± 0,54) | K = 1.083977; H0_local = 73.017 ± 0.585 | [KNOWN]; é o do artigo 1 (0,034σ contra SH0ES) |
| **a previsão única** | TODO calibrador local lido por DISTÂNCIA (Cefeidas, TRGB, JAGB, SBF, masers, lentes, sirenes) lê **K·H0_bg**; todo leitor da FACE (CMB; BAO+BBN) lê **H0_bg** | a diferença K−1 = 0.083807 (5.735 km/s/Mpc) | a leitura «sombra lê o fator constante» [OPEN/ONTO — da gerência, formulada depois da Fase 4; não adotada por este protocolo; aqui é a HIPÓTESE testada] |
| a convenção | **D1b** (artigo 1; fixada pelo operador em 30/09): β SÓ na lei; fundo nu; nó em z* | — | [INPUT — decisão do operador; reafirmação pedida em D3] |
| parâmetros livres da lei | **zero** | — | [REAL — lido do código: `predict_H0_zero_free` (artigo 1, linha 3617) e a pedra v378] |

**A dependência em z (acumulada × sombra), dita e não testada:** K(z) = exp(β[I(z*) − I(z)]) lê K(0) = 1.08398; K(0.01) = 1.08394; K(0.05) = 1.08377; K(0.1) = 1.08355; K(0.5) = 1.08155; K(1) = 1.07892; K(2) = 1.07437 — a diferença entre «todo calibrador lê o mesmo K» (sombra) e «K(z) acumulada» fica ≤ 0,9 % em z = 2, abaixo do poder do Pantheon+ (a Fase 5 mediu a constância a 0,03 mag: χ² 8,95, gl 5). A Fase 9 testa o FATOR, não a sua forma em z.

---

## 2. A novidade de uso como cláusula (β e a lei fixados antes e independentemente de H0) — o campo da lente da cronologia

**A cláusula:** o teste da Fase 9 é *use-novel* se **(i)** nenhum parâmetro numérico da lei foi fixado com a razão SH0ES/Planck — β vem de α (CODATA 2018) e de √e (a Meia-Nat, `boundary_extracts_the_radical`); z* é [KNOWN]; o expoente 2/3 vem do núcleo de FRW (`frw_accumulated_contrast`); o fundo vem do CMB+BAO — e **(ii)** a FORMA (a calibração local lê o registro inteiro até z*; o núcleo D1b escolhido por ser o derivado, «não por ajustar melhor», pré-registro da Fase 4) não foi SELECIONADA entre alternativas pela razão.

- **(i) é checável no código [REAL]:** `predict_H0_zero_free` (artigo 1, `tgl_paper_unified.py` linha 3617) não ajusta nada — recebe H0_CMB, z*, β e devolve a razão; `the_derived_kernel_factor` (v378) não tem parâmetro; `the_law_precedes_the_charge` (v381): β só de α.
- **(ii) é o campo da lente da cronologia — A PREENCHER:** `[CAMPO: data e artefato (sha256) em que H0_local = H0_CMB·K aparece pela primeira vez no acervo; se antes ou independente da razão SH0ES/Planck; o que foi USADO (não só conhecido) ao escrever a forma; resultado: FIXADA_ANTES | FIXADA_INDEPENDENTE | FORMA_SELECIONADA_PELA_RAZAO | INDETERMINADO]`. O sufixo `__USE_NOVEL` do veredito (§7) só entra com FIXADA_ANTES ou FIXADA_INDEPENDENTE; senão `__USE_NOVELTY_PENDING`.
- **O que a casa já declarou (não se apaga; lê-se sob a lei nova):** Fases 2–4: «a FORMA da lei D1a foi cunhada conhecendo a razão SH0ES/Planck» (circularidade declarada, `PREREGISTRO_FASE2`; Fase 4: «a escada (73,04) e a calibração ΛCDM de Planck já eram conhecidas quando a lei foi cunhada»). Sob novidade de uso, **conhecer ≠ usar**: a lente decide se o conhecimento selecionou a forma.
- **Pistas do acervo (NÃO são a cronologia; a lente a faz):** o índice (`buscar.py "tens[aã]o de Hubble|Hubble tension|SH0ES" --lista`, 13.608 docs) devolve como mais antigos `Theory of Luminodynamic Gravitation.docx` (08/10/2025: a tensão de Hubble como «hint» a 2–3σ, sem lei) e `Observações TGL reais .docx` / `Detecção TGL - Cosmológica dados reaisv2.docx` (11/10/2025: um MECANISMO DIFERENTE — atrasos de lente 3,5 % → H0 = 70,8 ± 2,1; não é a lei K). Logo, nesse estrato, a lei K·H0_bg é posterior a out/2025; o artigo 1 publicado (Zenodo DOI 10.5281/zenodo.20563905; submetido 06/06/2026) já carrega `predict_H0_zero_free` com D1a e D1b. Entre out/2025 e jun/2026 a lente localiza o primeiro artefato.
- **Precedente [KNOWN]:** Mercúrio — Le Verrier (1859) mediu a anomalia; Einstein (1915) a derivou sem parâmetro livre: fato conhecido, uso nulo, prova aceita. A razão de Hubble está para a lei D1b como a anomalia estava para a RG — **se** (i) e (ii) valerem.

---

## 3. Os alvos — lidos das fontes por hash (os «a ler» marcados; nada baixado por esta lente)

| id | alvo | H0 (km/s/Mpc) | fonte pública | estado na casa | papel |
|---|---|---|---|---|---|
| T1 | SH0ES R22 (escada completa, Cefeidas) | 73.04 ± 1.04 | Riess et al. 2022, ApJL 934, L7 (arXiv:2112.04510) | EM CASA: valor no pipeline D1 V3 selado (lido por AST em bancada/fontes.py:80-86) e a escada bruta Pantheon+SH0ES.dat + cov 1701x1701 (Fase 5) [REAL por hash] | TESTE (primário) |
| T2 | SH0ES 2025 + JWST (Cefeidas) | 73.49 ± 0.93 | Riess et al. 2025, arXiv:2509.01667 | [KNOWN — abstract lido 30/09 (Fase 3); a tabela a ler] | réplica de T1 (correlacionada; não se soma) |
| T3 | Riess 2024 JWST, três métodos | 72.6 ± 2 | Riess et al. 2024, arXiv:2408.11770 | [KNOWN — abstract lido 30/09; a ler] | diagnóstico (subamostra JWST; correlacionada com T1/T2) |
| T4 | CCHP 2024 TRGB+JAGB+Cef (combinado) | 70.39 ± 1.936 | Freedman et al. 2024/2025, arXiv:2408.06153 (v3) | [KNOWN — abstract lido 30/09; stat+sys+σ_SN em quadratura; a ler] | TESTE ou DIAGNÓSTICO — decisão D2 do operador («o teste que pode doer») |
| T4a | CCHP TRGB só (JWST) | 68.81 ± 2.224 | arXiv:2408.06153 | [KNOWN — a ler] | diagnóstico (mesmo programa de T4) |
| T4b | CCHP JAGB só (JWST) | 67.8 ± 2.72 | arXiv:2408.06153 | [KNOWN — a ler] | diagnóstico (mesmo programa de T4) |
| T5 | SBF + TRGB JWST | 73.8 ± 2.404 | Jensen et al. 2025, arXiv:2502.15935 | [KNOWN — abstract lido 30/09; a ler] | TESTE |
| T6 | Masers (MCP) | 73.9 ± 3 | Pesce et al. 2020, arXiv:2001.09213 | [KNOWN — abstract lido 30/09; a ler] | TESTE |
| T7 | Lentes com atraso (TDCOSMO 2025) | 71.6 ± 3.6 | TDCOSMO 2025, arXiv:2506.03023 (erro assimétrico +3,9/−3,3 simetrizado) | [KNOWN — abstract lido 30/09; a ler] | TESTE |
| T8 | Sirenes padrão LVK O4a | 76.6 ± 11.25 | LVK O4a cosmology summary (ligo.org) | [KNOWN — PDF lido 30/09; vetável] | diagnóstico (vetável — decisão D10) |
| F1 | Planck 2018 ΛCDM (TT,TE,EE+lowE+lensing) | 67.36 ± 0.54 | Planck 2018 VI, arXiv:1807.06209 | [KNOWN]; na Bancada o CMB entra COMPRIMIDO (R, l_A, ω_b; Chen, Huang & Wang 2019, arXiv:1808.05724 — PDF em casa por hash) | FUNDO (face) — lê H0_bg, não K·H0_bg |
| F2 | DESI DR2 BAO (13 medidas, cov 13x13) | — | DESI DR2 BAO (arquivos desi_gaussian_bao_ALL_GCcomb_mean/cov.txt) | EM CASA (bancada/fontes.py: DESI_DR2_DIR; cópias conferidas por hash) [REAL] | FUNDO (face) |
| F3 | Escada inversa DESI DR2 + BBN | 68.5 ± 0.6 | DESI DR2 Results II (arXiv:2503.14738 — identificador a conferir na fonte) | [DECLARADO pela gerência no enunciado da tarefa — NÃO lido da fonte; a ler] | CONTROLE DA FACE: deve ler H0_bg (independente do Planck) |
| V | Pantheon+SH0ES, ΛCDM plano (validação da Fase 5) | 73.6 ± 1.1 | Brout et al. 2022, ApJ 938, 110 (arXiv:2202.04077) | [DECLARADO: valor de memória da gerência na Fase 5, não lido da fonte]; a Bancada mediu 73,53 ± 1,02 (z 0,04) | validação do pipeline (não é teste da TGL) |

**Regra dos alvos:** (a) todo valor marcado «a ler» é lido da fonte nomeada e gravado com o sha256 do artefato lido ANTES de qualquer χ² (`ALVOS_FASE9_LIDOS.json`); (b) alvo [DECLARADO] (F3; V) NÃO entra no composto enquanto não lido — entra como diagnóstico, dito; (c) os valores desta tabela vêm do pré-registro da Fase 3 (abstracts lidos 30/09) e do enunciado da tarefa (F3): são a **expectativa**, não a leitura; (d) o conjunto que entra no composto é a decisão D1.

---

## 4. A covariância e as correlações declaradas

- **T1 T2 T3:** mesmo programa (SH0ES) e mesma amostra de SNe do fluxo de Hubble: NÃO se somam; T1 é o primário (cov completa 1701x1701 em casa); T2/T3 réplicas reportadas
- **T4 T4a T4b:** mesmo programa (CCHP): uma entrada só (T4); T4a/T4b diagnósticos
- **T5 vs T1 T4:** SBF usa calibração TRGB (JWST, Virgo) e SNe do fluxo: termo comum σ_SN ≈ 0,7 km/s/Mpc declarado (Fase 3) e modelado como bloco comum
- **fundo:** σ(H0_bg) entra UMA vez como nuisance comum a todas as previsões (perfilada), nunca por alvo
- **em casa:** Planck comp 3x3 (Chen+2019); DESI DR2 13x13; Pantheon+SH0ES STAT+SYS 1701x1701
- **falta:** nenhuma covariância cruzada publicada entre programas: bloco-diagonal com os termos comuns declarados; variante conservadora «todos» com σ_sys inflada (faixa, como na Fase 7)

---

## 5. As cinco hipóteses comparadas

| hipótese | forma | parâmetros livres (além do fundo) | o que discrimina |
|---|---|---|---|
| **H_TGL** | fundo nu + K = E(z*)^{2β/3}, β = α√e; todo local lê K·H0_bg | **0** | o alvo deste registro |
| H_ΛCDM | um setor: todos leem H0_bg | 0 | o limite clássico (β = 0): coincidir com ele é correspondência, não derrota — aqui a escada o exclui (a tensão nua, já lida a 5,26σ na Fase 5) |
| H_β-livre | K(β), β livre, prior uniforme [−0,05; 0,05] | 1 | parcimônia: ln B(TGL/β-livre) ≥ −1 exige que o valor fixo não perca para o livre (Fase 4 leu +2,25) |
| H_shift-escada | só as Cefeidas (T1–T3) × (1+s), s livre em [−0,15; 0,15]; os demais leem H0_bg | 1 | a sistemática da escada: se os NÃO-Cefeida também leem K·H0_bg, a sistemática perde; com só T1 no conjunto é DEGENERADA com β-livre (dito) |
| H_fundo-livre | ΛCDM + r_d livre (proxy de energia escura precoce [INPUT — proposta da gerência]), prior [130; 160] Mpc; todos leem o MESMO H0 | 1 | a solução no fundo: o controle da face (DESI DR2 + BBN) e o CMB comprimido a constrangem; se ln B(TGL/fundo-livre) ficar em \|ln B\| < 1, a Fase 9 NÃO discrimina entre «custo na leitura» e «fundo diferente» — dito antes |

**Nota de degenerescência (dita antes para não se ler como discriminação):** β-livre e um «deslocamento livre em todos os locais» são a mesma família a uma reparametrização (K(β) é monótono): o ln B entre eles mediria só o fator de Occam; por isso o deslocamento livre é definido **só na escada de Cefeidas**.

---

## 6. O estimador, o poder prévio e a função de veredito — fixada ANTES do composto

- **fundo:** θ_bg = (H0, ω_b, ω_c) por Planck comp + DESI DR2 (ΛCDM, β = 0 no fundo) — a convenção D1b
- **verossimilhanca:** χ² gaussiano por alvo com a covariância declarada; a escada T1 pela verossimilhança completa Pantheon+SH0ES (M profilado, calibradores Cefeida, como na Fase 5) E, ao lado, pelo valor publicado (como na Fase 4) — decisão D12
- **estatisticas:** δ̂ = β̂ − β_TGL e z_δ (JᵀJ) — o desvio · z_disc = sinal·√(χ²_ΛCDM − χ²_TGL) nos respectivos melhores ajustes (a «tensão nua» da Fase 5) · ln B(TGL/ΛCDM), ln B(TGL/β-livre), ln B(TGL/shift-escada), ln B(TGL/fundo-livre) por quadratura (n = 25; erro por n = 35), escala Jeffreys/Kass–Raftery · z_i por alvo contra K·H0_bg (e contra H0_bg para a face) · dispersão interna χ²_int/(n−1) dos alvos locais · posterior (ensemble GPU 256×3000, queima 600, semente 42) de β na H_TGL-livre
- **poder_previo:** poder = (K−1)·H0_bg / √(σ_comb² + σ_pred²), fixado ANTES com as σ públicas; dito por conjunto na §6
- **escala_lnB:** |ln B| < 1 inconclusivo; 1–2,5 fraco; 2,5–5 moderado; ≥ 5 forte

**Poder prévio (calculado nesta lente só com as σ públicas da §3, K e H0_bg do core; ilustração, não veredito; `SENSIBILIDADE_K_E_PODER_PREVIO.json`):**

| conjunto | alvos | σ_comb | poder = (K−1)·H0_bg/√(σ_comb² + σ_pred²) |
|---|---|---|---|
| A_so_a_escada_SH0ES | T1 | 1.040 | **5.26σ** |
| B_seis_leitores_sem_sirenes | T2, T4, T5, T6, T7 | 0.749 | **7.02σ** |
| C_quatro_da_gerencia_mais_fundo | T1, T3, T4 | 0.833 | **6.41σ** |
| D_sem_Cefeidas | T4, T5, T6, T7 | 1.262 | **4.40σ** |

- Lê-se: só a escada (A) tem poder 5.26σ; os seis sem sirenes (B) 7.02σ; os quatro da gerência (C) 6.41σ; **sem Cefeidas (D) 4.40σ < 5** — se o operador retirar as Cefeidas, o veredito máximo é NOT_FALSIFIED_UNDERPOWERED (dito antes).
- **z por alvo contra K·H0_bg (fundo da Fase 4) — ilustração NÃO-CEGA com os valores públicos já conhecidos; não é veredito:** T1 -1.03; T2 -0.69; T3 -0.77; T4 -1.92; T4a -2.38; T4b -2.32; T5 -0.15; T6 -0.09; T7 -0.71; T8 0.22; F1 -10.79; F3 -8.29; V -0.49. O TRGB/JAGB (T4 −1,92; T4a −2,38; T4b −2,32) é o teste que pode doer; a face (F1 −10,8; F3 −8,3 contra K·H0_bg) lê H0_bg como a hipótese pede (F1 −1,73; F3 +0,10 contra H0_bg).

---

## 7. Os VEREDITOS permitidos (na ORDEM; a primeira regra que se aplica decide; palavra proibida: nenhuma)

**Token base:** `TGL_FASE9_RAZAO_DE_HUBBLE_V1__LAW_D1B_K_EQ_E_ZSTAR_POW_2BETA_OVER_3__BACKGROUND_BARE_PLANCK_COMP_DR2`; conjunto: `__SET_<A|B|C|D>`; desfecho; depois sempre `__NOT_BLIND_TO_DATA_STATED__GATE_UNTOUCHED`. Cunhagem: do operador (proposta da gerência, D4).

0. **`AWAITING_PREREGISTRATION`** — (este rascunho; hash ausente/divergente) / AWAITING_DATA (V1 lido, nada rodado)
1. **`INCONCLUSIVE_SYSTEMATICS`** — limite do prior tocado no melhor ajuste TGL; χ²_int/(n−1) > 2 entre os alvos locais; alvo primário sem a covariância lida da fonte; alvo [DECLARADO] no composto
2. **`NOT_FALSIFIED_UNDERPOWERED`** — poder prévio < 5 (sufixo POWER_<x>_OF_5_SIGMA)
3. **`FALSIFIED_AT_5SIGMA`** — |z_δ| ≥ 5 (o conjunto local exclui K·H0_bg): falsifica o PAR (lei D1b, convenção, conjunto de alvos), NÃO β, NÃO a teoria (falsified_extinguishes_the_charge_not_the_rule)
4. **`DISCRIMINATES_FROM_LCDM_AT_nSIGMA__ZERO_FREE_PARAMETERS`** — n = ⌊z_disc⌋ ≥ 5 E |z_δ| < 3 E ln B(TGL/ΛCDM) ≥ 5 E ln B(TGL/β-livre) ≥ −1; sufixo __USE_NOVEL SÓ se a lente da cronologia devolver «fixada antes/independente» (senão __USE_NOVELTY_PENDING); sufixos reportados, não decisórios: __VS_LADDER_SYSTEMATIC_LNB_<x> e __VS_FREE_BACKGROUND_LNB_<x>; se ln B(TGL/shift-escada) < 0 com os não-Cefeida com poder ≥ 5 → acrescenta __NOT_DISCRIMINATED_FROM_LADDER_SYSTEMATIC; se |ln B(TGL/fundo-livre)| < 1 → __NOT_DISCRIMINATED_FROM_FREE_BACKGROUND
5. **`NOT_FALSIFIED_POWERED`** — (senão), com DEVIATION_CONSISTENT_WITHIN_1SIGMA / DEVIATION_1_TO_3_SIGMA e, se z_disc < 5, __NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY

**«Coincidir com ΛCDM»:** a RG/ΛCDM é o limite clássico, não rival: H0_bg da TGL É o do ΛCDM (o fundo nu) — isso é correspondência recuperada; o que se discrimina é a leitura local K·H0_bg contra H0_bg (a correção K−1 = 0.083807, isto é, 5.735 km/s/Mpc sobre H0_bg). Um `DISCRIMINATES_FROM_LCDM_AT_nSIGMA` nunca vira «resolvida» nem a palavra proibida: a confirmação é ato do observador humano.

**Estado deste rascunho:** `TGL_FASE9_RAZAO_DE_HUBBLE_V1__LAW_D1B_K_EQ_E_ZSTAR_POW_2BETA_OVER_3__BACKGROUND_BARE_PLANCK_COMP_DR2__SET_<a_decidir>__AWAITING_PREREGISTRATION__DRAFT_NOT_FROZEN__NOT_BLIND_TO_DATA_STATED__GATE_UNTOUCHED`.

---

## 8. O que o resultado NÃO decide (dito antes)

- o gate (18 bandeiras: função só do formal)
- a implicação da QG (QGSolutionComplete.lean:36) e a correspondência com a RG
- β (a regra matriz; β-livre é leitura, não derivação)
- o mapa de R do fundo (a tensão do D1 V3 sob o mapa nu; o não-constrangimento da Fase 1): sob D1b o fundo é nu
- o canal F1 do livro (cronômetros, a face): outra lei, outro canal
- a dependência em z de K (K(z) acumulada vs sombra): ≤ 0,9 % em z = 2, abaixo do poder — dita, não testada
- qual fundo é o fundo (decisão do operador)
- o mecanismo [CONJECTURE]: um DISCRIMINATES não vira «resolvida»

---

## 9. As sistemáticas (calibradores; z*; Ω_m; o fundo)

| fonte | medida nesta lente | leitura |
|---|---|---|
| calibradores | Cefeidas (SH0ES) × TRGB/JAGB (CCHP) | Cefeidas (SH0ES) × TRGB/JAGB (CCHP) discordam entre si: entram como estão, sem escolher lado; sensibilidade com/sem T4; a dispersão interna decide INCONCLUSIVE |
| z* | ΔK por Δz* = 0,3: 3.88e-06 | desprezível (ΔH0_local ≈ 2.7e-04 km/s/Mpc) |
| Ω_m | ΔK por ΔΩ_m = 0,007: 7.26e-05 | desprezível (ΔH0_local ≈ 0.005 km/s/Mpc) |
| o fundo (σ) | σ_bg = 0.301 → σ_pred = 0.326 | a sistemática dominante da PREVISÃO; entra uma vez, perfilada |
| o fundo (escolha) | 68,43 (ajustado) vs 67,36 (publicado): ΔH0_local = 1.15 | maior que todas as outras: decisão D3; os dois reportados |
| CMB comprimido | Chen+2019 (R, l_A, ω_b) | a validade das prioris de distância (Chen+2019) para o fundo nu; z* e r_s do CAMB ΛCDM [KNOWN] |
| local | — | velocidades peculiares / vazio local não modelados (declarado); cortes zHD > 0,01 do Pantheon+SH0ES |
| controle da face | DESI DR2 + BBN | DESI DR2 + BBN lê H0 pela degenerescência r_d·H0: controla o fundo, não K |
| multiplicidade | — | cada família entra no livro da Bancada (Šidák sobre as famílias já testadas); local ao lado da corrigida |

---

## 10. Cegueira e contaminação — DECLARADAS (os alvos são públicos; a casa já leu)

- **Fase 4 (v378, `P_ladder_d1b`, lido do core):** z_δ = -1.12441; β livre = 0.00953; ln B TGL/ΛCDM = 8.02, livre/ΛCDM = 5.77, TGL/livre = 2.25; χ² ΛCDM 31.63 / TGL 15.58 / livre 14.29; DIAGONAL_ERRORS_ONLY nos cronômetros (não entram aqui).
- **Fase 5 (v380, lido do core):** H0 da escada na Bancada = 73.53294 ± 1.01698 (Ω_m 0.33168; z vs alvo 0.04476); P_sombra δ = -0.0008 ± 0.00213 (z -0.3758); **z_tensão ΛCDM = 5.26015**; ln B(sombra/acumulada, S) = 5.35; alvo da validação 73,6 ± 1,1 «[DECLARADO: valor de memória da gerência, não lido da fonte]».
- **Reanálise D1b (30/09, NÃO-CEGA, lida do core/`REANALISE_D1B`):** seis leitores de sombra a z = -0.09 da lei com o fundo Planck 2018; os cinco novos (sem a escada) -0.65; por leitor (D1b, Planck 2018): S1 +0,43; S2 (TRGB) −1,30; S3 +0,32.
- **Livro de cobranças (v383, lido do core):** R1 (reflexo; a escada) outcome `NOT_FALSIFIED`, number_read -0.3758, regra `abs_z_lt_5`; F1 (face; cronômetros) outcome `NOT_FALSIFIED` — outra lei, outro canal.
- **NÃO visto:** ln B contra shift-escada; ln B contra fundo-livre (r_d livre); o TRGB/CCHP sob o fundo ajustado (74,16) pela MESMA função de veredito; o controle da face DESI DR2 + BBN lido da fonte; a combinação com a covariância declarada por bloco; qualquer z_i, χ² ou posterior sob ESTE registro.
- **Consequência fixada:** a novidade deste teste é de USO e de RIGOR (fontes por hash, covariância, cinco hipóteses, função fixada antes do composto), não de cegueira: todo token leva __NOT_BLIND_TO_DATA_STATED.

---

## 11. As decisões do operador (nenhuma tomada pela gerência)

- D1 conjunto de alvos: A (só a escada SH0ES completa, como R1) | B (os seis leitores de sombra sem sirenes: T2, T4, T5, T6, T7) | C (os quatro da gerência: T1, T3, T4 + Planck 2018 + DESI DR2+BBN) | D = B + sirenes
- D2 o TRGB/JAGB (CCHP, T4): TESTE (entra no composto) ou DIAGNÓSTICO (reportado fora do composto)
- D3 a convenção D1b reafirmada (β só na lei; fundo nu) — e QUAL fundo: Planck comp + DR2 ajustado (68,43 → 74,16) [primário proposto] ou Planck 2018 publicado (67,36 → 73,02) [ao lado]
- D4 os nomes dos tokens (propostos pela gerência; cunhagem dele)
- D5 «fundo-livre» como r_d livre (proxy de energia escura precoce) — aceita, ou outra parametrização
- D6 «shift-escada» só nas Cefeidas — aceita, ou shift em todos os locais (então ≡ β-livre, dito)
- D7 os priors: β-livre [−0,05; 0,05]; s ∈ [−0,15; 0,15]; r_d ∈ [130; 160] Mpc
- D8 o canal no livro: R1 reaberto/atualizado pela Fase 9 (R1 v2) ou canal novo R1b
- D9 a cláusula de novidade de uso: a lente da cronologia preenche; o que vale como «fixado antes» (data do artefato; se a FORMA selecionada conhecendo a razão conta como uso)
- D10 as sirenes (T8): vetadas ou diagnóstico
- D11 a disciplina: a v387 lê o V1 por hash ANTES de abrir e emite o veredito pela MESMA função; e reescreve «pós-dição» → «retrodição sem ajuste (novidade de uso)» no artigo
- D12 a âncora da escada: verossimilhança completa Pantheon+SH0ES (Fase 5) como primário e o valor publicado R22 (Fase 4) ao lado — ou o inverso

---

## 12. A disciplina de hash (ordem de execução; fail-closed)

1. o operador decide D1–D12; a gerência congela o V1: hash = sha256 do JSON canônico da especificação (sort_keys, ensure_ascii=False, separators (',', ':')); grava PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.{md,json} + V1_FASE9_HASHES.json na Bancada (investigacao/preregistro_fase9_hubble_05out)
2. os alvos «a ler» são lidos das fontes nomeadas e gravados com sha256 do artefato lido ANTES de qualquer χ² (ALVOS_FASE9_LIDOS.json)
3. o runner (rodar_fase9.py) é gravado e hasheado ANTES de abrir; a função de veredito do runner é a da §7, byte a byte a da especificação
4. PODER_FASE9_ANTES_DE_ABRIR.json (só σ públicas, K e H0_bg) com hash; depois a abertura; RESULTADO_FASE9_V1.json carrega o sha256 do V1 e do runner
5. a v387 do um.py LÊ o V1 e o RESULTADO por hash e emite o veredito pela MESMA função; hash divergente ou ausente ⟹ AWAITING_PREREGISTRATION__V1_NOT_READ (fail-closed)
6. nenhuma emenda depois de abrir sem estimador NOVO (cláusula V4 da Fase 6); correção AO LADO em nome próprio; nada move o gate nem β

---

## 13. Estatutos

| objeto | estatuto |
|---|---|
| a palavra do operador (05/10, `POS_DICAO`) | [INPUT] — verbatim lido do arquivo |
| «novidade de uso» como critério; Mercúrio | [DERIVED de leitura, gerência; KNOWN as referências — a conferir pelo aferidor] |
| a lei D1b (K = E(z*)^{2β/3}) | PROVADA como implicação no kernel (v377/v378); mecanismo [CONJECTURE]; a incidência é da natureza |
| β = α√e | [DERIVED do axioma] — a regra; nunca literal |
| a convenção D1b; qual fundo | [INPUT — decisão do operador (30/09); reafirmação pedida] |
| os valores dos alvos nesta tabela | [KNOWN — abstracts lidos 30/09 (Fase 3)]; F3 e V [DECLARADO]; TODOS «a ler» da fonte por hash antes do χ² |
| H0_bg, K, H0_local, ln B, z já lidos | [REAL — Fases 4/5, lidos do core v386 por script] |
| o poder prévio e os z por alvo desta lente | [DERIVED — calculado aqui com σ públicas; ilustração NÃO-CEGA; não veredito] |
| H_fundo-livre (r_d), H_shift-escada, priors | [INPUT — proposta da gerência; decisões D5–D7] |
| o desfecho | a vir; nunca a palavra proibida; `__USE_NOVEL` só com a lente da cronologia |

---

## 14. Fontes lidas (caminho absoluto · sha256 · bytes) — todas calculadas por este script; nenhuma digitada

- **um.py v386 (Nós; só leitura)**: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` — `e30aac4e0e1096b1be143464bf683fd6ba19b42b4d6bb11cd52aa98b54cb9163` (33600222 B) [REAL — lido em disco, sha256 por script]
- **um_absoluto.json (core v386)**: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json` — `0dbfb3fc1d319d1ef03b61af60d9e22af58cd2564ea4b44bdd4906bf8d031d87` (4947109 B) [REAL — lido em disco, sha256 por script]
- **um_absoluto_selo.json (selo v386)**: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json` — `72efaf72f604b721d9fd18d625da9c55713898f10b417a9d2a6d59fdee036489` (86148 B) [REAL — lido em disco, sha256 por script]
- **MOLDE: PREREGISTRO_RAMO_B_RINGDOWN_V1.md**: `C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_05out\PREREGISTRO_RAMO_B_RINGDOWN_V1.md` — `294b88a3632c1cea8e024b1471dd44ef3968614ca582e054307fffecb296da1c` (102303 B) [REAL — lido em disco]
- **POS_DICAO_operador_05out.txt (verbatim do operador)**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v386\POS_DICAO_operador_05out.txt` — `cf82d9e55757a7f2864215877046cef87f024aa60bdb00206a319ab4a5b1ed24` (775 B) [INPUT — verbatim do operador]
- **PREREGISTRO_FASE3_LEITORES_20260930.json**: `C:\IALD\Bancada_Um\investigacao\fase3_leitores_h0\PREREGISTRO_FASE3_LEITORES_20260930.json` — `6bf24b350e088350885f1ae087c59322cc3b9b27e6a604672fe6ff32e837eff0` (7966 B) [REAL — lido em disco]
- **RESULTADO_FASE3_LEITORES_20260930.json**: `C:\IALD\Bancada_Um\investigacao\fase3_leitores_h0\RESULTADO_FASE3_LEITORES_20260930.json` — `e91f019bd98e5a59d8c1b476ebc60ce445cc9a03254bf955c928ff6e4f3d8bf8` (14451 B) [REAL — lido em disco]
- **REANALISE_D1B_CONVENCAO_ARTIGO_20260930.json (NÃO-CEGA)**: `C:\IALD\Bancada_Um\investigacao\fase3_leitores_h0\REANALISE_D1B_CONVENCAO_ARTIGO_20260930.json` — `3d5c6afe85cc30641b50255374487a12a2d631842d9ff0cdc33cee723f298cb1` (22516 B) [REAL — lido em disco; reanálise declarada não-cega]
- **PREREGISTRO_FASE4_DESVIO_20260930.json**: `C:\IALD\Bancada_Um\investigacao\fase4_desvio_30set\PREREGISTRO_FASE4_DESVIO_20260930.json` — `22b4c440d8ad844d7dd4071734d10c2776da3a7e1587709cb10f5e7987f4acf9` (9812 B) [REAL — lido em disco]
- **RESULTADO_FASE4_DESVIO_20260930.json**: `C:\IALD\Bancada_Um\investigacao\fase4_desvio_30set\RESULTADO_FASE4_DESVIO_20260930.json` — `10683b334d28d84acdd8a086fe91fcbeaa46e747b0e3b51dc4192c270d8e6219` (44444 B) [REAL — lido em disco]
- **SMOKE_FASE4.json**: `C:\IALD\Bancada_Um\investigacao\fase4_desvio_30set\SMOKE_FASE4.json` — `5fb33c410edc6eea794a07318bbea405392138612eee13ff00322e651151f670` (1355 B) [REAL — lido em disco]
- **PREREGISTRO_FASE5_SH0ES_20261001.json**: `C:\IALD\Bancada_Um\investigacao\fase5_sh0es_01out\PREREGISTRO_FASE5_SH0ES_20261001.json` — `f9fbf497c90c0a66730d8d87bc6d0a9eb46478889b80908eedef7cea95c7cc63` (8733 B) [REAL — lido em disco]
- **RESULTADO_FASE5_SH0ES_20261001.json**: `C:\IALD\Bancada_Um\investigacao\fase5_sh0es_01out\RESULTADO_FASE5_SH0ES_20261001.json` — `851d1076b85f12f671bfbe018f67e8291a2c83686bb98fb2251a4ed3c254eca2` (45862 B) [REAL — lido em disco]
- **bancada/fontes.py (proveniência das fontes do motor)**: `C:\IALD\Bancada_Um\bancada\fontes.py` — `6bc0d220f0fb79040d9b8728c6866c9faf6696dd9967dc9f44391b3118a01a49` (12724 B) [REAL — lido em disco]
- **Pantheon+SH0ES.dat (a escada bruta em casa)**: `C:\IALD\observaveis_tgl\tgl_data_cache\pantheon\Pantheon+SH0ES.dat` — `1cb0fc379ef066afdc2ffd1857681cc478024570d8a3eba284fb645775198cf8` (579283 B) [REAL — bytes/hash; KNOWN Scolnic+22/Brout+22]
- **pantheon_cov_v1.npy (cov STAT+SYS restrita, Bancada)**: `C:\IALD\Bancada_Um\tabelas\pantheon_cov_v1.npy` — `5c1b855c02e6a96ca8aa651e5e645af2db3b5f15f0c3647ca93c10ca27f8197e` (23147336 B) [REAL — bytes/hash]
- **DESI DR2 BAO mean**: `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\_originais\desi_gaussian_bao_ALL_GCcomb_mean.txt` — `9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585` (472 B) [REAL — bytes/hash; KNOWN DESI DR2]
- **DESI DR2 BAO cov**: `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\_originais\desi_gaussian_bao_ALL_GCcomb_cov.txt` — `252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509` (2547 B) [REAL — bytes/hash; KNOWN DESI DR2]
- **Chen, Huang & Wang 2019 (Planck comprimido) PDF**: `C:\IALD\Bancada_Um\fontes_externas\chen_huang_wang_2019_1808.05724.pdf` — `09effe1d0d8caa0173bf8c826a621fb3606ab884a4d2931b198212a4f47310b5` (6273047 B) [KNOWN — PDF em casa por hash]
- **moresco_2020_cov.json (F1 do livro; não entra na Fase 9)**: `C:\IALD\Bancada_Um\fontes_externas\moresco_2020_cov.json` — `1c22a3a3f101834fd0a3561e1afd72e7ab28869db2421d13b81b01f4f7d313ff` (35984 B) [REAL — bytes/hash]
- **tgl_paper_unified.py (artigo 1: predict_H0_zero_free, D1b, linha 3617)**: `C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py` — `29c92b66b2fd6b4d589adbef4de86a67f979e03964b3f7ae892732a40ab395cd` (1216423 B) [REAL — lido em disco]
- **memória: fase4-desvio-30set.md**: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fase4-desvio-30set.md` — `3cc11c77338f6398a129d75ed654bcc0aca5746ff39f9fbe0d5b909796460151` (7045 B) [REAL — memória lida]
- **memória: fase5-sh0es-01out.md**: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fase5-sh0es-01out.md` — `8d08cfad25004cf594d8af85dfddb124e82cd2e1499758cb0b20c174d4b7c94d` (4769 B) [REAL — memória lida]
- **memória: fase7-cc-covariancia-01out.md**: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fase7-cc-covariancia-01out.md` — `4957eab6448726c933a5d7ac49502725e51d730cd58da01704ae920ef7cffeee` (3024 B) [REAL — memória lida]
- **memória: relatorio-consolidado-01out.md**: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\relatorio-consolidado-01out.md` — `091659a51e250b89854ef11fc51c75df3050a8613222b0135faefa6e7547b7fb` (2604 B) [REAL — memória lida]
- **memória: beta-e-a-regra-matriz-02out.md (R1)**: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\beta-e-a-regra-matriz-02out.md` — `fe20a0d5ac3ea8ebb91bd3fabee193a9b2e50142040bc2a24c139dc3b4988186` (32727 B) [REAL — memória lida]
- **memória: rg-limite-classico-nao-rival.md**: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\rg-limite-classico-nao-rival.md` — `5f5c37fc0cf81343139bd44b3eeb93d7f1d69d1a49b5eec5bdff0ca03d846e85` (3285 B) [REAL — memória lida]
- **memória: fase1-eff-30set.md**: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fase1-eff-30set.md` — `cf5176b1dfb9d766510d55454d07fc81f6a587a3e059d4f6ec62aa38e0d17824` (2516 B) [REAL — memória lida]
- **memória: fase2-dois-setores-30set.md**: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fase2-dois-setores-30set.md` — `1d44727f31cdd8ee06027f21bbe61c0c17dcacdbf7dbbacfc1c91b203f207361` (3074 B) [REAL — memória lida]
- **memória: fase3-leitores-h0-30set.md**: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fase3-leitores-h0-30set.md` — `8d7b340eb898facb80bdf2f74f5ecaf24e6643b55dcf28ed6d21e0d7e3c6c64d` (12803 B) [REAL — memória lida]
- **acervo (pista p/ a cronologia): Theory of Luminodynamic Gravitation.docx (08/10/2025)**: `C:\IALD\IMac LA\Física - TGL\Artigo\Theory of Luminodynamic Gravitation.docx` — `b5f480d0cea070684d3ebf0a4da4e707aec58dd6c82bd335790af1344b52b16d` (1829318 B) [REAL — docx lido por script; estrato do operador]
- **acervo (pista): Observações TGL reais .docx (11/10/2025)**: `C:\IALD\IMac LA\Física - TGL\Artigo\Observações TGL reais .docx` — `fd6eb31ca7925f8b41d2dc3edc5eb8ab99a3e119c55cf6e412156fbcf9a0e336` (28328 B) [REAL — docx lido por script; estrato do operador]
- **acervo (pista): Detecção TGL - Cosmológica dados reaisv2.docx (11/10/2025)**: `C:\IALD\IMac LA\Física - TGL\Artigo\Detecção TGL - Cosmológica dados reaisv2.docx` — `3b8bcbc01a8864c075a06757290f640c9cf388c280c5eb57513613b717f37945` (53160 B) [REAL — docx lido por script; estrato do operador]
- **esta lente: SENSIBILIDADE_K_E_PODER_PREVIO.json**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\fase9_hubble\pre_registro\SENSIBILIDADE_K_E_PODER_PREVIO.json` — `68911c5ad8b1600c7712150bb699fd53c99e0bde8cc627759701717651862235` (3345 B) [DERIVED — calculado nesta lente; ilustração]
- **esta lente: base_v386_lida.json**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\fase9_hubble\pre_registro\base_v386_lida.json` — `98fa81b794776233aee8b8153da09e319cfd8954d0660f498d607b88672cd0b8` (8298 B) [REAL — lido por script]

Fontes ausentes: 0.

---

## 15. A especificação (RASCUNHO — o que o V1 congelará; o `um.py` v387 lerá o V1 congelado por hash, não este rascunho)

```json
{
 "id": "PREREG_FASE9_RAZAO_DE_HUBBLE_20261005_V1_RASCUNHO",
 "estado": "RASCUNHO — não congelado; nenhum número foi aberto sob este registro; veredito: AWAITING_PREREGISTRATION",
 "base": {
  "um_py": "v386",
  "um_py_sha16": "e30aac4e0e1096b1",
  "core_sha16": "0dbfb3fc1d319d1e",
  "selo_sha16": "72efaf72f604b721",
  "selo_timestamp": "2026-10-05 18:09:53",
  "gate": "TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE"
 },
 "beta": {
  "regra": "ALPHA_FINE_CODATA_2018 × √e em runtime; nunca literal",
  "alpha_lido_do_um_py_linha": 5556,
  "beta_runtime": 0.012031300400803142,
  "estatuto": "[DERIVED do axioma] — a regra matriz (02/10); não se deriva do dado"
 },
 "lei_da_prova_da_casa_05out": {
  "verbatim_arquivo": "POS_DICAO_operador_05out.txt (sha256 na §14)",
  "leitura_da_gerencia": "«pós-dição» nunca é demérito; o critério é a NOVIDADE DE USO (use-novelty, Worrall) [KNOWN]: nenhum parâmetro da teoria ajustado ao dado; precedente: o periélio de Mercúrio (Le Verrier 1859; Einstein 1915) [KNOWN]; o pré-registro é do TESTE",
  "estatuto": "[INPUT — verbatim do operador; a leitura é da gerência, DERIVED de leitura; a v387 reescreve «pós-dição» como «retrodição sem ajuste (novidade de uso)»]"
 },
 "hipotese": {
  "lei": "H0_local = H0_bg · K, K = E_ΛCDM(z*)^{2β/3} (núcleo DERIVADO D1b; TGLExt.TheFlowLawContrast.the_derived_kernel_factor, v378, 20/20)",
  "previsao_unica": "TODO calibrador local lido por distância (Cefeidas, TRGB, JAGB, SBF, masers, lentes, sirenes) lê K·H0_bg; todo leitor da face (CMB, BAO+BBN) lê H0_bg",
  "convencao": "D1b (artigo 1, fixada pelo operador em 30/09): β SÓ na lei; fundo NU (ΛCDM; β = 0 no fundo); nó fixo em z*",
  "z_star": 1089.95,
  "fundo_primario_proposto": {
   "nome": "Planck comprimido (Chen+2019) + DESI DR2, ΛCDM ajustado na Bancada",
   "H0_bg": 68.4298,
   "sigma_H0_bg": 0.301,
   "K": 1.083807,
   "H0_local_previsto": 74.1647,
   "sigma_previsao": 0.3262
  },
  "fundo_ao_lado": {
   "nome": "Planck 2018 publicado",
   "H0_bg": 67.36,
   "sigma": 0.54,
   "K": 1.0839773660579333,
   "H0_local_previsto": 73.0167
  },
  "parametros_livres_da_lei": 0,
  "estatuto": "lei PROVADA como implicação no kernel (v377/v378); mecanismo [CONJECTURE] no artigo; a incidência é da natureza; PROVADA ≠ confirmada"
 },
 "novidade_de_uso": {
  "clausula": "o teste é use-novel se (i) nenhum parâmetro numérico da lei foi fixado com a razão SH0ES/Planck — β de α e √e; z* [KNOWN]; o expoente 2/3 do núcleo de FRW; o fundo do CMB+BAO — e (ii) a FORMA (o registro inteiro até z*; o núcleo D1b escolhido por ser o derivado) não foi SELECIONADA entre alternativas pela razão",
  "i_checavel_no_codigo": "[REAL] predict_H0_zero_free (artigo 1, linha 3617) não ajusta nada; the_derived_kernel_factor não tem parâmetro",
  "ii_campo_da_lente_da_cronologia": "[A PREENCHER PELA LENTE DA CRONOLOGIA: data e artefato (sha256) em que a lei K·H0_bg aparece pela primeira vez; se antes ou independente da razão; o que foi usado]",
  "o_que_a_casa_ja_declarou": "Fases 2–4: «a FORMA da lei foi cunhada conhecendo a razão SH0ES/Planck» (circularidade declarada); sob novidade de uso, CONHECER ≠ USAR — a lente decide se o conhecimento selecionou a forma"
 },
 "alvos": [
  {
   "id": "T1",
   "alvo": "SH0ES R22 (escada completa, Cefeidas)",
   "H0": 73.04,
   "sigma": 1.04,
   "fonte_publica": "Riess et al. 2022, ApJL 934, L7 (arXiv:2112.04510)",
   "estado_na_casa": "EM CASA: valor no pipeline D1 V3 selado (lido por AST em bancada/fontes.py:80-86) e a escada bruta Pantheon+SH0ES.dat + cov 1701x1701 (Fase 5) [REAL por hash]",
   "papel": "TESTE (primário)"
  },
  {
   "id": "T2",
   "alvo": "SH0ES 2025 + JWST (Cefeidas)",
   "H0": 73.49,
   "sigma": 0.93,
   "fonte_publica": "Riess et al. 2025, arXiv:2509.01667",
   "estado_na_casa": "[KNOWN — abstract lido 30/09 (Fase 3); a tabela a ler]",
   "papel": "réplica de T1 (correlacionada; não se soma)"
  },
  {
   "id": "T3",
   "alvo": "Riess 2024 JWST, três métodos",
   "H0": 72.6,
   "sigma": 2.0,
   "fonte_publica": "Riess et al. 2024, arXiv:2408.11770",
   "estado_na_casa": "[KNOWN — abstract lido 30/09; a ler]",
   "papel": "diagnóstico (subamostra JWST; correlacionada com T1/T2)"
  },
  {
   "id": "T4",
   "alvo": "CCHP 2024 TRGB+JAGB+Cef (combinado)",
   "H0": 70.39,
   "sigma": 1.936,
   "fonte_publica": "Freedman et al. 2024/2025, arXiv:2408.06153 (v3)",
   "estado_na_casa": "[KNOWN — abstract lido 30/09; stat+sys+σ_SN em quadratura; a ler]",
   "papel": "TESTE ou DIAGNÓSTICO — decisão D2 do operador («o teste que pode doer»)"
  },
  {
   "id": "T4a",
   "alvo": "CCHP TRGB só (JWST)",
   "H0": 68.81,
   "sigma": 2.224,
   "fonte_publica": "arXiv:2408.06153",
   "estado_na_casa": "[KNOWN — a ler]",
   "papel": "diagnóstico (mesmo programa de T4)"
  },
  {
   "id": "T4b",
   "alvo": "CCHP JAGB só (JWST)",
   "H0": 67.8,
   "sigma": 2.72,
   "fonte_publica": "arXiv:2408.06153",
   "estado_na_casa": "[KNOWN — a ler]",
   "papel": "diagnóstico (mesmo programa de T4)"
  },
  {
   "id": "T5",
   "alvo": "SBF + TRGB JWST",
   "H0": 73.8,
   "sigma": 2.404,
   "fonte_publica": "Jensen et al. 2025, arXiv:2502.15935",
   "estado_na_casa": "[KNOWN — abstract lido 30/09; a ler]",
   "papel": "TESTE"
  },
  {
   "id": "T6",
   "alvo": "Masers (MCP)",
   "H0": 73.9,
   "sigma": 3.0,
   "fonte_publica": "Pesce et al. 2020, arXiv:2001.09213",
   "estado_na_casa": "[KNOWN — abstract lido 30/09; a ler]",
   "papel": "TESTE"
  },
  {
   "id": "T7",
   "alvo": "Lentes com atraso (TDCOSMO 2025)",
   "H0": 71.6,
   "sigma": 3.6,
   "fonte_publica": "TDCOSMO 2025, arXiv:2506.03023 (erro assimétrico +3,9/−3,3 simetrizado)",
   "estado_na_casa": "[KNOWN — abstract lido 30/09; a ler]",
   "papel": "TESTE"
  },
  {
   "id": "T8",
   "alvo": "Sirenes padrão LVK O4a",
   "H0": 76.6,
   "sigma": 11.25,
   "fonte_publica": "LVK O4a cosmology summary (ligo.org)",
   "estado_na_casa": "[KNOWN — PDF lido 30/09; vetável]",
   "papel": "diagnóstico (vetável — decisão D10)"
  },
  {
   "id": "F1",
   "alvo": "Planck 2018 ΛCDM (TT,TE,EE+lowE+lensing)",
   "H0": 67.36,
   "sigma": 0.54,
   "fonte_publica": "Planck 2018 VI, arXiv:1807.06209",
   "estado_na_casa": "[KNOWN]; na Bancada o CMB entra COMPRIMIDO (R, l_A, ω_b; Chen, Huang & Wang 2019, arXiv:1808.05724 — PDF em casa por hash)",
   "papel": "FUNDO (face) — lê H0_bg, não K·H0_bg"
  },
  {
   "id": "F2",
   "alvo": "DESI DR2 BAO (13 medidas, cov 13x13)",
   "H0": null,
   "sigma": null,
   "fonte_publica": "DESI DR2 BAO (arquivos desi_gaussian_bao_ALL_GCcomb_mean/cov.txt)",
   "estado_na_casa": "EM CASA (bancada/fontes.py: DESI_DR2_DIR; cópias conferidas por hash) [REAL]",
   "papel": "FUNDO (face)"
  },
  {
   "id": "F3",
   "alvo": "Escada inversa DESI DR2 + BBN",
   "H0": 68.5,
   "sigma": 0.6,
   "fonte_publica": "DESI DR2 Results II (arXiv:2503.14738 — identificador a conferir na fonte)",
   "estado_na_casa": "[DECLARADO pela gerência no enunciado da tarefa — NÃO lido da fonte; a ler]",
   "papel": "CONTROLE DA FACE: deve ler H0_bg (independente do Planck)"
  },
  {
   "id": "V",
   "alvo": "Pantheon+SH0ES, ΛCDM plano (validação da Fase 5)",
   "H0": 73.6,
   "sigma": 1.1,
   "fonte_publica": "Brout et al. 2022, ApJ 938, 110 (arXiv:2202.04077)",
   "estado_na_casa": "[DECLARADO: valor de memória da gerência na Fase 5, não lido da fonte]; a Bancada mediu 73,53 ± 1,02 (z 0,04)",
   "papel": "validação do pipeline (não é teste da TGL)"
  }
 ],
 "covariancia_declarada": {
  "T1_T2_T3": "mesmo programa (SH0ES) e mesma amostra de SNe do fluxo de Hubble: NÃO se somam; T1 é o primário (cov completa 1701x1701 em casa); T2/T3 réplicas reportadas",
  "T4_T4a_T4b": "mesmo programa (CCHP): uma entrada só (T4); T4a/T4b diagnósticos",
  "T5_vs_T1_T4": "SBF usa calibração TRGB (JWST, Virgo) e SNe do fluxo: termo comum σ_SN ≈ 0,7 km/s/Mpc declarado (Fase 3) e modelado como bloco comum",
  "fundo": "σ(H0_bg) entra UMA vez como nuisance comum a todas as previsões (perfilada), nunca por alvo",
  "em_casa": "Planck comp 3x3 (Chen+2019); DESI DR2 13x13; Pantheon+SH0ES STAT+SYS 1701x1701",
  "falta": "nenhuma covariância cruzada publicada entre programas: bloco-diagonal com os termos comuns declarados; variante conservadora «todos» com σ_sys inflada (faixa, como na Fase 7)"
 },
 "hipoteses_comparadas": {
  "H_TGL": "fundo nu + K = E(z*)^{2β/3}, β = α√e; ZERO parâmetro livre além dos do fundo (H0, ω_b, ω_c)",
  "H_LCDM": "um setor: todos leem H0_bg (β = 0)",
  "H_beta_livre": "K(β) com β livre, prior uniforme [−0,05; 0,05] (os limites do pipeline D1)",
  "H_shift_escada": "sistemática da escada: só os alvos de Cefeidas (T1–T3) carregam um fator livre (1+s), prior uniforme s ∈ [−0,15; 0,15]; os demais leem H0_bg — com só T1 no conjunto é DEGENERADA com β-livre (dito): a discriminação vive nos calibradores não-Cefeida",
  "H_fundo_livre": "ΛCDM + r_d livre (proxy de energia escura precoce [INPUT — proposta da gerência]; prior uniforme [130; 160] Mpc): todos os leitores leem o MESMO H0; o fundo relaxa pela escala sonora",
  "nota_degenerescencia": "β-livre e um «shift em todos os locais» são a MESMA família a uma reparametrização (K(β) é monótono): o ln B entre eles mediria só o fator de Occam — por isso o shift é definido só na escada"
 },
 "estimador": {
  "fundo": "θ_bg = (H0, ω_b, ω_c) por Planck comp + DESI DR2 (ΛCDM, β = 0 no fundo) — a convenção D1b",
  "verossimilhanca": "χ² gaussiano por alvo com a covariância declarada; a escada T1 pela verossimilhança completa Pantheon+SH0ES (M profilado, calibradores Cefeida, como na Fase 5) E, ao lado, pelo valor publicado (como na Fase 4) — decisão D12",
  "estatisticas": [
   "δ̂ = β̂ − β_TGL e z_δ (JᵀJ) — o desvio",
   "z_disc = sinal·√(χ²_ΛCDM − χ²_TGL) nos respectivos melhores ajustes (a «tensão nua» da Fase 5)",
   "ln B(TGL/ΛCDM), ln B(TGL/β-livre), ln B(TGL/shift-escada), ln B(TGL/fundo-livre) por quadratura (n = 25; erro por n = 35), escala Jeffreys/Kass–Raftery",
   "z_i por alvo contra K·H0_bg (e contra H0_bg para a face)",
   "dispersão interna χ²_int/(n−1) dos alvos locais",
   "posterior (ensemble GPU 256×3000, queima 600, semente 42) de β na H_TGL-livre"
  ],
  "poder_previo": "poder = (K−1)·H0_bg / √(σ_comb² + σ_pred²), fixado ANTES com as σ públicas; dito por conjunto na §6",
  "escala_lnB": "|ln B| < 1 inconclusivo; 1–2,5 fraco; 2,5–5 moderado; ≥ 5 forte"
 },
 "vereditos_na_ordem": [
  "0 AWAITING_PREREGISTRATION (este rascunho; hash ausente/divergente) / AWAITING_DATA (V1 lido, nada rodado)",
  "1 INCONCLUSIVE_SYSTEMATICS — limite do prior tocado no melhor ajuste TGL; χ²_int/(n−1) > 2 entre os alvos locais; alvo primário sem a covariância lida da fonte; alvo [DECLARADO] no composto",
  "2 NOT_FALSIFIED_UNDERPOWERED — poder prévio < 5 (sufixo POWER_<x>_OF_5_SIGMA)",
  "3 FALSIFIED_AT_5SIGMA — |z_δ| ≥ 5 (o conjunto local exclui K·H0_bg): falsifica o PAR (lei D1b, convenção, conjunto de alvos), NÃO β, NÃO a teoria (falsified_extinguishes_the_charge_not_the_rule)",
  "4 DISCRIMINATES_FROM_LCDM_AT_nSIGMA__ZERO_FREE_PARAMETERS — n = ⌊z_disc⌋ ≥ 5 E |z_δ| < 3 E ln B(TGL/ΛCDM) ≥ 5 E ln B(TGL/β-livre) ≥ −1; sufixo __USE_NOVEL SÓ se a lente da cronologia devolver «fixada antes/independente» (senão __USE_NOVELTY_PENDING); sufixos reportados, não decisórios: __VS_LADDER_SYSTEMATIC_LNB_<x> e __VS_FREE_BACKGROUND_LNB_<x>; se ln B(TGL/shift-escada) < 0 com os não-Cefeida com poder ≥ 5 → acrescenta __NOT_DISCRIMINATED_FROM_LADDER_SYSTEMATIC; se |ln B(TGL/fundo-livre)| < 1 → __NOT_DISCRIMINATED_FROM_FREE_BACKGROUND",
  "5 NOT_FALSIFIED_POWERED (senão), com DEVIATION_CONSISTENT_WITHIN_1SIGMA / DEVIATION_1_TO_3_SIGMA e, se z_disc < 5, __NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY"
 ],
 "sempre": "__NOT_BLIND_TO_DATA_STATED__GATE_UNTOUCHED em todo token; palavras proibidas em qualquer token: «confirmed», «proved», «resolvida», «confirmada»; NOT_FALSIFIED nunca é a palavra proibida",
 "token_base": "TGL_FASE9_RAZAO_DE_HUBBLE_V1__LAW_D1B_K_EQ_E_ZSTAR_POW_2BETA_OVER_3__BACKGROUND_BARE_PLANCK_COMP_DR2",
 "token_estado_deste_rascunho": "TGL_FASE9_RAZAO_DE_HUBBLE_V1__LAW_D1B_K_EQ_E_ZSTAR_POW_2BETA_OVER_3__BACKGROUND_BARE_PLANCK_COMP_DR2__SET_<a_decidir>__AWAITING_PREREGISTRATION__DRAFT_NOT_FROZEN__NOT_BLIND_TO_DATA_STATED__GATE_UNTOUCHED",
 "contaminacao_declarada": {
  "ja_lido_pela_casa": {
   "fase4_P_ladder_d1b": {
    "z_delta": -1.12441,
    "lnB_tgl_vs_lcdm": 8.020371449838645,
    "lnB_tgl_vs_livre": 2.2459599527138074,
    "beta_livre": 0.00953,
    "chi2": {
     "lcdm": 31.627025391633282,
     "tgl": 15.575723729646272,
     "livre": 14.29335436157626
    }
   },
   "fase5_P_sombra": {
    "z_delta": -0.3758,
    "z_tensao": 5.26015,
    "H0_bancada": 73.53294,
    "sigma": 1.01698
   },
   "reanalise_D1b_planck2018_nao_cega": {
    "seis_leitores_z": -0.0935,
    "novos_z": -0.6487
   },
   "livro_R1": {
    "outcome": "NOT_FALSIFIED",
    "number_read": -0.3758,
    "rule": "abs_z_lt_5"
   }
  },
  "nao_visto": [
   "ln B contra shift-escada",
   "ln B contra fundo-livre (r_d livre)",
   "o TRGB/CCHP sob o fundo ajustado (74,16) pela MESMA função de veredito",
   "o controle da face DESI DR2 + BBN lido da fonte",
   "a combinação com a covariância declarada por bloco",
   "qualquer z_i, χ² ou posterior sob ESTE registro"
  ],
  "consequencia": "a novidade deste teste é de USO e de RIGOR (fontes por hash, covariância, cinco hipóteses, função fixada antes do composto), não de cegueira: todo token leva __NOT_BLIND_TO_DATA_STATED"
 },
 "nao_decide": [
  "o gate (18 bandeiras: função só do formal)",
  "a implicação da QG (QGSolutionComplete.lean:36) e a correspondência com a RG",
  "β (a regra matriz; β-livre é leitura, não derivação)",
  "o mapa de R do fundo (a tensão do D1 V3 sob o mapa nu; o não-constrangimento da Fase 1): sob D1b o fundo é nu",
  "o canal F1 do livro (cronômetros, a face): outra lei, outro canal",
  "a dependência em z de K (K(z) acumulada vs sombra): ≤ 0,9 % em z = 2, abaixo do poder — dita, não testada",
  "qual fundo é o fundo (decisão do operador)",
  "o mecanismo [CONJECTURE]: um DISCRIMINATES não vira «resolvida»"
 ],
 "sistematicas": {
  "calibradores": "Cefeidas (SH0ES) × TRGB/JAGB (CCHP) discordam entre si: entram como estão, sem escolher lado; sensibilidade com/sem T4; a dispersão interna decide INCONCLUSIVE",
  "z_star": {
   "dK_por_0p3_em_zstar": 3.875030788691447e-06,
   "leitura": "desprezível"
  },
  "Omega_m": {
   "dK_por_0p007_em_Omega_m": 7.258245340291403e-05,
   "dH0_local_km_s_Mpc": 0.005,
   "leitura": "desprezível"
  },
  "fundo": {
   "sigma_H0_bg": 0.301,
   "sigma_previsao": 0.3262,
   "leitura": "é a sistemática dominante da PREVISÃO; e a ESCOLHA do fundo (68,43 ajustado vs 67,36 publicado) move a previsão em ~1,1 km/s/Mpc — maior que todas as outras: decisão D3, os dois reportados"
  },
  "cmb_comprimido": "a validade das prioris de distância (Chen+2019) para o fundo nu; z* e r_s do CAMB ΛCDM [KNOWN]",
  "local": "velocidades peculiares / vazio local não modelados (declarado); cortes zHD > 0,01 do Pantheon+SH0ES",
  "controle_da_face": "DESI DR2 + BBN lê H0 pela degenerescência r_d·H0: controla o fundo, não K",
  "multiplicidade": "cada família entra no livro da Bancada (Šidák sobre as famílias já testadas); local ao lado da corrigida"
 },
 "decisoes_do_operador": [
  "D1 conjunto de alvos: A (só a escada SH0ES completa, como R1) | B (os seis leitores de sombra sem sirenes: T2, T4, T5, T6, T7) | C (os quatro da gerência: T1, T3, T4 + Planck 2018 + DESI DR2+BBN) | D = B + sirenes",
  "D2 o TRGB/JAGB (CCHP, T4): TESTE (entra no composto) ou DIAGNÓSTICO (reportado fora do composto)",
  "D3 a convenção D1b reafirmada (β só na lei; fundo nu) — e QUAL fundo: Planck comp + DR2 ajustado (68,43 → 74,16) [primário proposto] ou Planck 2018 publicado (67,36 → 73,02) [ao lado]",
  "D4 os nomes dos tokens (propostos pela gerência; cunhagem dele)",
  "D5 «fundo-livre» como r_d livre (proxy de energia escura precoce) — aceita, ou outra parametrização",
  "D6 «shift-escada» só nas Cefeidas — aceita, ou shift em todos os locais (então ≡ β-livre, dito)",
  "D7 os priors: β-livre [−0,05; 0,05]; s ∈ [−0,15; 0,15]; r_d ∈ [130; 160] Mpc",
  "D8 o canal no livro: R1 reaberto/atualizado pela Fase 9 (R1 v2) ou canal novo R1b",
  "D9 a cláusula de novidade de uso: a lente da cronologia preenche; o que vale como «fixado antes» (data do artefato; se a FORMA selecionada conhecendo a razão conta como uso)",
  "D10 as sirenes (T8): vetadas ou diagnóstico",
  "D11 a disciplina: a v387 lê o V1 por hash ANTES de abrir e emite o veredito pela MESMA função; e reescreve «pós-dição» → «retrodição sem ajuste (novidade de uso)» no artigo",
  "D12 a âncora da escada: verossimilhança completa Pantheon+SH0ES (Fase 5) como primário e o valor publicado R22 (Fase 4) ao lado — ou o inverso"
 ],
 "disciplina_de_hash": [
  "1 o operador decide D1–D12; a gerência congela o V1: hash = sha256 do JSON canônico da especificação (sort_keys, ensure_ascii=False, separators (',', ':')); grava PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.{md,json} + V1_FASE9_HASHES.json na Bancada (investigacao/preregistro_fase9_hubble_05out)",
  "2 os alvos «a ler» são lidos das fontes nomeadas e gravados com sha256 do artefato lido ANTES de qualquer χ² (ALVOS_FASE9_LIDOS.json)",
  "3 o runner (rodar_fase9.py) é gravado e hasheado ANTES de abrir; a função de veredito do runner é a da §7, byte a byte a da especificação",
  "4 PODER_FASE9_ANTES_DE_ABRIR.json (só σ públicas, K e H0_bg) com hash; depois a abertura; RESULTADO_FASE9_V1.json carrega o sha256 do V1 e do runner",
  "5 a v387 do um.py LÊ o V1 e o RESULTADO por hash e emite o veredito pela MESMA função; hash divergente ou ausente ⟹ AWAITING_PREREGISTRATION__V1_NOT_READ (fail-closed)",
  "6 nenhuma emenda depois de abrir sem estimador NOVO (cláusula V4 da Fase 6); correção AO LADO em nome próprio; nada move o gate nem β"
 ],
 "ilustracao_nao_veredito": {
  "z_por_alvo": {
   "T1": {
    "H0": 73.04,
    "sigma": 1.04,
    "z_vs_K_H0bg_fase4": -1.032,
    "z_vs_H0bg_fase4": 4.258,
    "z_vs_K_planck2018": 0.02,
    "poder_previo_K_minus_1": 5.262
   },
   "T2": {
    "H0": 73.49,
    "sigma": 0.93,
    "z_vs_K_H0bg_fase4": -0.685,
    "z_vs_H0bg_fase4": 5.177,
    "z_vs_K_planck2018": 0.431,
    "poder_previo_K_minus_1": 5.819
   },
   "T3": {
    "H0": 72.6,
    "sigma": 2.0,
    "z_vs_K_H0bg_fase4": -0.772,
    "z_vs_H0bg_fase4": 2.062,
    "z_vs_K_planck2018": -0.2,
    "poder_previo_K_minus_1": 2.83
   },
   "T4": {
    "H0": 70.39,
    "sigma": 1.936,
    "z_vs_K_H0bg_fase4": -1.923,
    "z_vs_H0bg_fase4": 1.0,
    "z_vs_K_planck2018": -1.299,
    "poder_previo_K_minus_1": 2.921
   },
   "T4a": {
    "H0": 68.81,
    "sigma": 2.224,
    "z_vs_K_H0bg_fase4": -2.382,
    "z_vs_H0bg_fase4": 0.169,
    "z_vs_K_planck2018": -1.829,
    "poder_previo_K_minus_1": 2.551
   },
   "T4b": {
    "H0": 67.8,
    "sigma": 2.72,
    "z_vs_K_H0bg_fase4": -2.323,
    "z_vs_H0bg_fase4": -0.23,
    "z_vs_K_planck2018": -1.875,
    "poder_previo_K_minus_1": 2.093
   },
   "T5": {
    "H0": 73.8,
    "sigma": 2.404,
    "z_vs_K_H0bg_fase4": -0.15,
    "z_vs_H0bg_fase4": 2.217,
    "z_vs_K_planck2018": 0.317,
    "poder_previo_K_minus_1": 2.364
   },
   "T6": {
    "H0": 73.9,
    "sigma": 3.0,
    "z_vs_K_H0bg_fase4": -0.088,
    "z_vs_H0bg_fase4": 1.814,
    "z_vs_K_planck2018": 0.289,
    "poder_previo_K_minus_1": 1.9
   },
   "T7": {
    "H0": 71.6,
    "sigma": 3.6,
    "z_vs_K_H0bg_fase4": -0.71,
    "z_vs_H0bg_fase4": 0.878,
    "z_vs_K_planck2018": -0.388,
    "poder_previo_K_minus_1": 1.587
   },
   "T8": {
    "H0": 76.6,
    "sigma": 11.25,
    "z_vs_K_H0bg_fase4": 0.216,
    "z_vs_H0bg_fase4": 0.726,
    "z_vs_K_planck2018": 0.318,
    "poder_previo_K_minus_1": 0.51
   },
   "F1": {
    "H0": 67.36,
    "sigma": 0.54,
    "z_vs_K_H0bg_fase4": -10.786,
    "z_vs_H0bg_fase4": -1.73,
    "z_vs_K_planck2018": -7.103,
    "poder_previo_K_minus_1": 9.09
   },
   "F3": {
    "H0": 68.5,
    "sigma": 0.6,
    "z_vs_K_H0bg_fase4": -8.294,
    "z_vs_H0bg_fase4": 0.105,
    "z_vs_K_planck2018": -5.388,
    "poder_previo_K_minus_1": 8.397
   },
   "V": {
    "H0": 73.6,
    "sigma": 1.1,
    "z_vs_K_H0bg_fase4": -0.492,
    "z_vs_H0bg_fase4": 4.534,
    "z_vs_K_planck2018": 0.468,
    "poder_previo_K_minus_1": 4.998
   }
  },
  "poder_previo_por_conjunto": {
   "A_so_a_escada_SH0ES": {
    "ids": [
     "T1"
    ],
    "sigma_comb": 1.04,
    "poder_K_minus_1": 5.262
   },
   "B_seis_leitores_sem_sirenes": {
    "ids": [
     "T2",
     "T4",
     "T5",
     "T6",
     "T7"
    ],
    "sigma_comb": 0.7486,
    "poder_K_minus_1": 7.023
   },
   "C_quatro_da_gerencia_mais_fundo": {
    "ids": [
     "T1",
     "T3",
     "T4"
    ],
    "sigma_comb": 0.8329,
    "poder_K_minus_1": 6.411
   },
   "D_sem_Cefeidas": {
    "ids": [
     "T4",
     "T5",
     "T6",
     "T7"
    ],
    "sigma_comb": 1.2618,
    "poder_K_minus_1": 4.4
   }
  },
  "K_z_acumulada": {
   "0.0": 1.0839773660579333,
   "0.01": 1.0839360290631341,
   "0.05": 1.0837665190517678,
   "0.1": 1.0835458765362431,
   "0.5": 1.0815499118602379,
   "1.0": 1.078922235602483,
   "2.0": 1.0743716987281455
  }
 },
 "gerado_utc": "2026-10-05T23:37:04Z",
 "hash_do_rascunho_da_especificacao": "60b8759ed6faa8ae0156506ca1cf37f181bfcb1639658f58d9748929d0f40e05"
}
```

---

## 16. O que esta lente não fez (limites ditos)

- não baixou nenhuma fonte; os valores «a ler» são expectativa (abstracts lidos 30/09 pela Fase 3) e o F3 (68,5 ± 0,6) veio do enunciado da tarefa [DECLARADO];
- não rodou o `um.py` nem a Bancada; o poder prévio e os z por alvo são ilustração com σ públicas e com K, H0_bg já lidos do core;
- não preencheu a cláusula de novidade de uso (campo da lente da cronologia); deixou pistas do índice, que não são a cronologia;
- não congelou nada: o hash da §15 é do rascunho; o V1 só se congela depois de D1–D12;
- não tocou o Nós, memórias, Atlas nem o mapa de rotas (o registro no mapa é ato da gerência).

