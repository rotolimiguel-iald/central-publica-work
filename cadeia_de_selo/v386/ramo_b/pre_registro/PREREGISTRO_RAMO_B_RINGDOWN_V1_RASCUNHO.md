# PRÉ-REGISTRO V1 DO RAMO B DO RINGDOWN — τ★ emparelhado à gravidade (τ★ = k·GM/c³) — RASCUNHO (05/10/2026)

**Identificador (proposto):** `PREREG_RAMO_B_RINGDOWN_20261005_V1` · **estado:** RASCUNHO — NÃO congelado; o hash de congelamento só existe depois das decisões do operador (§2) e da gravação na Bancada (`C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_ringdown_05out\`, lugar permanente, como o pilar quântico) · **autor:** aferidor da lente `pre_registro` (claude-code/central-de-patentes, sessão 6da8f00d), por ordem da gerência; correção sempre AO LADO, em nome próprio · **base:** `um.py` v385 sha16 `d406ae5725105145` (lido: `d406ae57251051456b8ee49220e117bc086cedc164b6e9d15e85b516467c4760`, 33.386.720 B); core `um_absoluto.json` `475ac8d218b3a5c8`; selo `um_absoluto_selo.json` `ad5c1ac7affc3949` · **formato herdado:** `PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.md` (`fc132b8f3e2d531b`) e `PREREGISTRO_PILAR_QUANTICO_20261003_V1.md` (`e5b345c5d950d052`).

**Mapa de rotas consultado antes (régua):** `rotas.py consultar "ringdown"` (16 rotas), `consultar "ramo B"` (4 rotas), `ver ringdown.dephasing` (15 registros lidos, seq 24–352). O próximo passo registrado na rota (seq 352, 05/10 14:15) é exatamente este documento: «pre-registro V1 do ramo B ANTES de abrir dado: a lei (…), k e qual M (…) fixados por principio (…), o observavel (…), o estimador, o poder com a sigma publicada, os controles (ramo canonico; injecoes so-RG) e os vereditos permitidos (sem CONFIRMED); RD-01/CT-02 (propagacao x fonte; ensemble x realizacao) decididos no pre-registro».

> Régua: β nunca literal (β_TGL = α_CODATA2018·√e = 0,012031300400803142, α lido do `um.py` por script); PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED; a RG é o limite clássico, não rival — coincidir com a RG = correspondência recuperada; nenhum desfecho move a regra (β) nem o gate; a cosmologia/natureza jamais vira prova matemática.

---

## 1. A hipótese do ramo B

### 1.1 Nas palavras do operador (verbatim, `DECISAO_OPERADOR_RAMO_B_05out.json`, sha256 `a5d548235522c1129ddd683887ac43d7fc2aec36095b7171af08c3ab076060f3`, 2.719 B, 2026-10-05T17:11:36.866Z)

> «eu não havia proibido o ramo B, acontece que naquela ocasião ainda não tínhamos todos os críterios para prosseguir. há pouco tempo eu ainda disse que a TGL pode ler das duas formas, e eu penso que podemos investigar a explorar o ramo B porque faz sentido examinar se a constante de acoplamento de fato emerge da relação do tempo emparelhado à gravidade sobre a constante da luz ao cubo, a mim faz todo sentido que assim seja, porque desde antes sustentei que o regime gravitônico é o da constante da luz ao cubo, e se o tempo é emergente da fluxo modular relativo, a mim, encontro correspondência direta com a proposta. de resto concordo com tudo»

**Âncoras no acervo (lidas por script; `buscar.py "constante da luz ao cubo"`, 20 arquivos):** o mais antigo é de 28/07/2025 (`IMac LA\Física - TGL\Provas\3\TGL_Cap_L_O_Instante_Lucifer_Faisca_Sem_Permanencia.docx`: «c³ = luz elevada à permanência»); o verbatim «o regime gravitônico é o regime da constante da luz ao cubo, é esse o fechamento» está em `BANCADA_TOE\MEMORIA_DA_BANCADA.md:2879`; a pedra 84_ (17/08/2026): «a dobra é aquilo que eu chamei vulgarmente de constante da luz ao cubo (c³)», medido G·m_P/c³ = t_Planck; o próprio programa diz (um.py:168040): «c³ sozinho não é velocidade; com G é tempo por massa, Gm/c³: com a massa de Planck dá t_Planck — o ramo A da lei de dephasing —, e com a massa do remanescente dá GM/c³ — o ramo B do ringdown» [REAL — texto do programa]. A expressão «tempo emparelhado à gravidade» tem **0 ocorrências** no acervo indexado (`buscar.py "tempo emparelhado|emparelhad[oa] [àa] gravidade"`): é cunhagem nova de 05/10 [INPUT]. «Tempo emergente do fluxo modular relativo» = tempo térmico de Connes–Rovelli [KNOWN]; no kernel, a ponte KMS/Unruh existe como `TGLExt.ContratoQGv31.ContratoH2.unruh_is_kms` e `unruh_is_kms_temperature` (Audit.lean:9545–9546; `kmsStrip` em ContratoQG_v31.lean:150) — β·κ = 2π —, mas **nenhum termo liga τ★ a GM/c³**: toda menção a ringdown no kernel é comentário/docstring (8 menções, 0 declarações, `ringdown_scope_v376.kernel_ringdown_mentions`; grep hoje: Audit.lean:9618/9760, LightOneParticleByTerm.lean:12, QGSolutionComplete.lean:14/39, TetelestaiOneObject.lean:17/39, TheImportedSecondQuantization.lean:18), e a própria lei Γ_ω = ½βτ★ω² «NÃO tem termo no kernel (a lei em ω² vive só em docstring e no runtime) — é leitura [ONTO]» (TheMatrixRule.lean:46).

### 1.2 A tradução operacional

| peça | forma | estatuto |
|---|---|---|
| a lei | Γ_ω = ½·β·τ★·ω² (GKSL energia-preservante; o custo entra como taxa ADITIVA ao amortecimento do modo) | [REAL na forma; ONTO — sem termo no kernel] |
| o relógio do ramo B | τ★ = k·G·M/c³ (k adimensional; M a nomear — §2) | [INPUT — decisão do operador; k com origem física dita em §2.1] |
| o observável | fração do tempo de amortecimento do modo (ℓ,m,n) = (2,2,0): δτ̂₂₂₀ ≡ τ_obs/τ_GR − 1 (a convenção `dtau220` do pSEOB: τ = τ_GR·(1 + dtau220)) | [KNOWN — convenção do catálogo] |
| a previsão (linear) | δτ₂₂₀/τ₂₂₀ = −x, x = Γ·τ_GR = ½βk(GM/c³)(2πf)²·Q/(πf) = **β·k·(GMω/c³)·Q₂₂₀ = β·k·N(a_f)**, com N(a_f) ≡ (Mω̂₂₂₀)(a_f)·Q₂₂₀(a_f) | [DERIVED das entradas] |
| a previsão (exata, taxas somam) | τ_obs = 1/(1/τ_GR + Γ) ⟹ δτ/τ = −x/(1+x) | [DERIVED] |
| Kerr | Mω̂₂₂₀(a) = 1,5251 − 1,1568(1−a)^0,1292; Q₂₂₀(a) = 0,7000 + 1,4187(1−a)^(−0,4990) (Berti–Cardoso–Will 2006; os mesmos coeficientes do um.py:155704) | [KNOWN] |
| δf₂₂₀ | 0 em primeira ordem (dephasing não desloca a frequência; as duas leituras de Γ preveem δf̂ ≈ 0 — RD-02, verificador) | [DERIVED] |

**Fato estrutural que decide o M (e o frame):** com M = M_f (a massa do remanescente), o M **cancela** — x depende só do spin a_f e de k: x = β·k·N(a_f); e como GMω/c³ é invariante de frame (M e ω escalam inversamente com 1+z), a previsão é a mesma no detector e na fonte. Para a_f = 0,6785 (a mediana do spin do GW250114 no release da descoberta): Mω̂ = 0,5261, Q = 3,199, N = 1,683 ⟹ x(k = 1) = 0,02025 ⟹ δτ/τ = −2,0 % (linear) / −1,98 % (exata); em a_f = 0,68: N = 1,688, x = 0,02031. Com outro M (total inicial, chirp), x ganha o fator M_outro/M_f (≈ 1,05 para M_tot, pois E_rad ≈ 5 % [KNOWN]; ≈ 0,44·(M_tot/M_f) para a massa chirp a q ≈ 1) — e deixa de ser função só do spin.

**O que o teste pergunta (reformulado como pergunta falsificável):** fixados β (a regra, [DERIVED] do axioma, v376), k e M ANTES do dado, o amortecimento do 220 publicado pelos catálogos se desvia da RG na fração −β·k·N(a_f)·(M/M_f)? Não se «deriva β do dado» (a regra matriz, 02/10: «β não se deriva DO DADO»): o que se testa é o PAR (k, M) sob a identificação dita em §2.3–2.4.

### 1.3 O que o registro já diz (lido por hash; nada aqui é novo)

| item | número lido | fonte |
|---|---|---|
| ramo canônico τ★ = t_Planck | δ_pred_A = −2,153e−42 (V2 selada, ensemble); recomputado hoje para 250 Hz/4 ms: −3,20e−42 (t_P = 5,391125282640084e−44 s das constantes do um.py) | `core.ringdown_dephasing_result_v2.stacks.3.0.delta_pred_A`; `poder_cego_ramo_b.py` |
| ramo B (k = 1, M = M_f) na V2 | δ_pred_B = −0,019367 (média do ensemble, 15 séries a 3 ms); medido δτ̂ = 0,1766 ± 0,1089 (z vs RG 1,62; z vs B 1,80); poder 0,178 de 5σ; **INCONCLUSIVE_SYSTEMATICS** («vies relativo de tau 0.240 > 0.2»); V1 hash `a3d941e56d3d33c5`, V2 hash `3449885389a2529a`, resultado `ff15f023dd91d8c7` | `core.ringdown_dephasing_result_v2`; veredito `TGL_RINGDOWN_DEPHASING_V2__…__BRANCH_B_PRED_M0P0194__POWER_0P2_OF_5_SIGMA__…` |
| 3 valores concorrentes do ramo B | −0,019367 (V2, ensemble) · −0,010 (CT-02) · −0,005 (CTV-02, por realização) | `core.ringdown_scope_v376.branch_B_concurrent_values` |
| C6 GW250114 (bancada, strain na fonte) | INCONCLUSIVE_SYSTEMATICS; ln B(R-B/RG) no início primário = −0,0026; R-MOD −0,25; R-LIN −0,09 | `core.ringdown_scope_v376.c6_*` (sha256 `781a3741a68875eb…`) |
| relógio livre do GW250114 (C4) | ln evidência (relógio livre entre t_P e GM/c³ / RG) = +0,026 — nenhuma preferência | `C4_FREE_CLOCK.json` (`cbf6332771937278…`) |
| relógios v369 | GM_⊕/c³ como relógio universal: EXCLUÍDO; G·m_átomo/c³: invisível — «a source-dependent mass clock is not one universal constant» | `core.clock_test_result_v369.tau_star_alternatives`; `C1_LEITURAS_v4.json` R-B |
| propagação (CT-02, verificador) | Γ_B = 4,9965 s⁻¹; Γ_B·t_prop = 2,263e17 e-folds ⟹ como propagação o ramo B é excluído trivialmente; só é testável como efeito LOCAL na fonte | mapa `ringdown.dephasing` seq 132 |
| realização × ensemble (CTV-02/RD-01) | sob difusão de fase, o δτ̂ por realização é 0,273 ± 0,06 do deslocamento do ensemble; o resto vira tremor de ~2 % em δf̂ | mapa seq 85/141 [DECLARADO pelo verificador] |
| não identificabilidade do 220 único | com (M, a) livres num só 220, a deformação de τ está no espaço gerado por massa/spin (determinante −Q′/Q = −1,2188 em χ = 0,68; z identificável = 0); o ramo B é imitado por um Kerr ~1,25 % mais leve com Δχ ≈ −0,016 | `bis/F4_POWER_GATE_REVIEW.md` (`35b02b3d0a4d45ec…`); ORDEM 013 (22/09) |
| livro de cobranças v383 | F2 (ringdown, face): INCONCLUSIVE pela sistemática da MEDIDA; R6 «ENCERRADO» de 02/10 era leitura da gerência — ERRATA AO LADO de 05/10: REABERTO POR PRÉ-REGISTRO | `core.the_ledger_of_charges_v383`; memória `ramo-b-reaberto-05out.md` |

---

## 2. As DECISÕES do operador a fixar ANTES do dado (nenhuma tomada aqui; cada uma com o custo dito)

### 2.1 D1 — o k de τ★ = k·GM/c³ (um só k, ou a lista com Šidák)

| k | τ★ | origem física | estatuto | x = βkN (a_f = 0,6785) | δτ/τ exata |
|---|---|---|---|---|---|
| **1** | GM/c³ | «a dobra em c³» (pedra 84_): a mesma dobra G·m/c³ em duas massas — m_P dá t_P (ramo A), M_f dá o ramo B; o k da V2 (v346) | [ONTO/INPUT — o k que o registro já testou] | 0,02025 | −1,98 % |
| **2** | 2GM/c³ = r_s/c | tempo de travessia do raio de Schwarzschild à velocidade da luz (o prefator das leis de atraso MAY/DEC) | [KNOWN geometria; INPUT como relógio] | 0,0405 | −3,9 % |
| **4π** | 2π·r_s/c | a circunferência do horizonte percorrida à luz | [KNOWN geometria; INPUT] | 0,2545 | −20,3 % |
| **8π** | ħ/(k_B T_H) = 8πGM/c³ (a = 0) | o PERÍODO KMS/térmico de Hawking: «tempo emergente do fluxo modular relativo» (Connes–Rovelli; no kernel β·κ = 2π, `unruh_is_kms`); é a leitura literal da frase do operador | [KNOWN período; ONTO identificação τ★ = período modular] | 0,509 | −33,7 % |
| **2π/κ(a_f)** | 4π(1+√(1−a²))/√(1−a²) · GM/c³ (Kerr; a = 0 → 8π; a = 0,68 → 29,7) | o mesmo período KMS, com a gravidade superficial de Kerr por evento (a lei que a Fase 6 usou como ATRASO e a auditoria GWECO-05 corrigiu: 2π/κ é largura em tempo imaginário; aqui entra como ESCALA DE TAXA, uso distinto, dito) | [KNOWN κ; ONTO] | 0,601 | −37,5 % |
| (R-MOD) | 2π/κ com ω → ω − mΩ_H | hipótese da gerência na ORDEM 013; Kay–Wald 1991: não há estado Hadamard estacionário em Kerr | [CONJECTURE — fora deste V1 salvo ordem] | — | — |

Observações para a decisão: (i) o pSEOB tem prior `dtau220 ~ Uniform(−0,8; 2,0)`: todas as previsões acima cabem no prior (a de 2π/κ fica a 0,2 da borda inferior — dito); (ii) o poder e a cláusula de sistemática dependem de k linearmente (§4); (iii) se o operador quiser **mais de um k**, cada k é uma cobrança e a significância global entra com Šidák sobre o número de k fixados (como no livro); (iv) **não** se ajusta k ao dado — «a lei do pagamento é fixada antes da cobrança».

### 2.2 D2 — qual M

| M | efeito na previsão | nota |
|---|---|---|
| **M_f** (massa do remanescente, a do catálogo: `final_mass`/`final_mass_non_evolved`) | x = βkN(a_f): o M cancela; função só do spin; invariante de frame | o Nome M_f entregue (R5/R6: «onde a massa aparece»); é o M da V2 (v346) |
| M_tot = m₁ + m₂ (inicial) | × M_tot/M_f ≈ 1,03–1,05 (E_rad ≈ 3–5 %), lido por evento do catálogo se escolhido | perde a invariância «só spin» |
| M_chirp | × M_c/M_f ≈ 0,44 (q ≈ 1), menor para q < 1; por evento | idem |

### 2.3 D3 — propagação × fonte (RD-01/CT-02)

A lei do ramo B age **durante o ringdown, no relógio do próprio remanescente** (τ★,src = GM_src/c³; τ★,det = GM_det/c³; «no independent D dependence in local rate», C1 R-B). Como propagação ao longo de D o efeito seria 10¹⁷ e-folds (excluído por construção, não por teste). A frase do operador de 16/09 («betatgl está de fato na propagação da onda») lê o ramo canônico; o ramo B é OUTRO relógio/lei. **Proposta:** FONTE (local). Decisão do operador.

### 2.4 D4 — ensemble × realização (a identificação [ONTO] do que Γ faz ao modo)

| identificação | o que o 220 mostra | previsão efetiva | poder (×) |
|---|---|---|---|
| **envoltória / taxa aditiva** (a docstring do protocolo V1: «somada à taxa de decaimento do modo dominante»; `ENSEMBLE_ADDITIVE_RATE` da C1) | δτ̂ = −x em CADA evento | −β·k·N(a_f) | 1,00 |
| difusão de fase (desdobramento unitário aleatório) | δτ̂ por realização ≈ 0,273 do ensemble + tremor de ~2 % em δf̂; o observável adequado passa a ser a LARGURA populacional de δf̂ | −0,273·β·k·N(a_f) em δτ̂ | 0,273 |

**Proposta:** envoltória como observável PRIMÁRIO (é o que o catálogo publica) e a largura de δf̂ como SECUNDÁRIO declarado (N₉₀ = 59/38/21 eventos GW250114-like para σ_jit 0,019/0,0228/0,030, limiar do LRT 25,0 — 013-bis, [DECLARADO pela bancada, condicional ao desenrolamento browniano [INPUT] e à transferência ao pSEOB [OPEN]]). Decisão do operador.

### 2.5 D5 — o observável

Primário: **δτ̂₂₂₀ fracional** (convenção `dtau220`). Alternativa Q: δQ/Q = δτ/τ + δf/f — a previsão é a mesma (δf ≈ 0), mas Q soma o ruído de δf̂; só como diagnóstico. Alternativa largura de δf̂: §2.4.

### 2.6 D6 — o estimador (§3) · D7 — os conjuntos de dados e a cegueira (§3.3) · D8 — a sistemática de família (§5) · D9 — o lado no livro de cobranças (face: o remanescente, com o custo lido nele pela ótica de 02/10; a cobrança seria **F2b**, ao lado de F2, uma por lei) · D10 — os nomes dos vereditos (§6) · D11 — o piloto de PE na casa (§5, custo) · D12 — a ratificação deste V1 (verbatim + carimbo + hash do transcrito, como no pilar).

---

## 3. O estimador

### 3.1 Primário — média ponderada por 1/σ² dos δτ̂₂₂₀ publicados, RELATIVA À RG, com nuisance

1. Para cada evento i do conjunto fixado (§3.3): a_i (mediana do spin do remanescente do posterior), σ_i (desvio-padrão completo, ddof = 1, do posterior de `dtau220`; o posterior é aproximado por gaussiana — a largura 90 %/3,29 confere com σ_std em 31/31, §4), e o centro δ̂_i (lido SÓ na abertura).
2. Previsão por evento: δ_i^pred = −x_i/(1+x_i), x_i = β·k·N(a_i)·(M/M_f)_i; a incerteza de Kerr entra propagando os quantis 05/95 do spin em N(a) (correlacionada entre H1/L1 por construção, pois o posterior é da rede — RD-02 resolvido pelo uso do posterior publicado).
3. Nuisance da REFERÊNCIA: c(σ) = c₀ + k_c·σ (o «viés» da LVK: offset fixo em 0 é PROIBIDO como teste — `E0_CORE.json`: `offset_zero_status = PROIBIDA_COMO_TESTE_CALIBRATION_ONLY`; com offset 0 e o viés da LVK haveria 5σ espúrios contra o R-B em ~115 eventos e contra a própria RG em ~191). c₀ e k_c ajustados em conjunto sob as duas hipóteses (RG: δ̂_i = c(σ_i) + ε; B: δ̂_i = c(σ_i) + δ_i^pred + ε).
4. Estatística: δ̄ = Σw_i(δ̂_i − c(σ_i))/Σw_i, w_i = 1/(σ_i² + σ_sys²), σ_comb = 1/√Σw_i; z_RG = δ̄/σ_comb; z_B = (δ̄ − δ̄^pred)/σ_comb; **poder = |δ̄^pred|/σ_comb** (fixado ANTES, §4); fração máxima de informação por evento reportada (hoje 0,337 — o GW250114).
5. χ²/dof do empilhamento e jackknife por evento (σ_usado = max(σ_comb, σ_jackknife), fail-closed como na Fase 6).

### 3.2 Secundário — verossimilhança conjunta por KDE dos posteriores (o método C4 da bancada)

Produto sobre eventos da densidade posterior (KDE, largura de banda 0,7/1,0/1,4) avaliada em δ_i^pred (hipótese B) e em 0 (RG), com o mesmo nuisance; devolve ln B(B/RG). Entra como consistência; **o primário decide**. Se os dois discordarem no rótulo, o resultado lê INCONCLUSIVE_SYSTEMATICS com o motivo dito.

### 3.3 Conjuntos de dados (D7) e cegueira

| conjunto | n | fonte em disco (sha256) | cegueira |
|---|---|---|---|
| A — GWTC-5.0 TGR, seleção da figura do release (pSEOBNRv5PHM-reweighted; GW250114 com o 440 livre, os demais 440 fixos na RG; GW250114 uma só vez) | 31 (+2 controles dos autores: GW191109_010717, GW200208_130117) | `C4_CATALOG_220.json` `93bdc413130d294acde91ec03f8392b8d9c5ec5b33fdc97274371656503d8e17`; seleção `C4_CATALOG_COMBINATION.json` `f3d8c1959ded3efd…`; Zenodo 21454847 | **NÃO CEGO quanto ao dado** (§8) |
| B — GWTC-3 TGR (pSEOBNRv4HM; 10 selecionados pelos autores) | 10 (de 18) | `C4_GWTC3_220.json` `d9dc9b09a8d91dc7…`; `C4_GWTC3_SELECTION.json` `ef18f3b0495d58bf…`; Zenodo 17461225 | NÃO CEGO; réplica de instrumento (família v4) |
| C — GW250114, release da descoberta | 1 | `C4_220_INITIAL.json` `f5550b7b1f129e83…`; Zenodo 17018009 | NÃO CEGO; cruza com A |
| D — os eventos O4 com strain público e SEM δτ̂ publicado (31 dos 45, 013-bis) | até 31 | banco de GW residente da Bancada (336/354 janelas O4 OK) + PE na casa (WSL `/opt/lal_env`, pSEOBNRv4HM_PA, bilby+dynesty; piloto só-220 da ORDEM 015: 0/120 quedas, 63–78 CPU-h ≈ 2,6–3,3 h) | **CEGO** — AWAITING_DATA até a PE rodar sob este registro |
| E — futuros (GWTC-5 final; O5) | — | — | CEGO; réplica |

**Regra:** o veredito PRINCIPAL é o do conjunto A (dito NÃO CEGO); B e C são réplicas de instrumento; D é a réplica CEGA — a única que pode dar a palavra «cega» a este V1; E fica registrado.

---

## 4. O PODER, calculado ÀS CEGAS (só σ e spin; nenhum valor central lido pelo script)

Script `poder_cego_ramo_b.py` (nesta pasta; saída `PODER_CEGO_RAMO_B.json`). σ_i = desvio-padrão completo (ddof = 1) do posterior de `dtau220` (`bis/E0_ROUTE_IV_POWER_v2.json` `ae457e82c8c18b5cccf47d60c785d82b3ec3888db7975f2184666c558e4ddd93`); controle: largura 90 %/3,29 dos quantis 05/95 do catálogo (`catalog_220_readout.py:108`, `np.quantile(v,[.05,.5,.95])`). β = α√e em runtime; a_i = mediana do spin; N(a_i) por BCW.

### 4.1 As σ por evento (conjunto A; só σ e spin)

| evento | σ (std) | w90/3,29 | a_f | N(a_f) | k_KMS(a_f) |
|---|---|---|---|---|---|
| GW150914_095045 | 0,1955 | 0,1928 | 0,675 | 1,670 | 29,59 |
| GW170104_101158 | 0,5011 | 0,4885 | 0,661 | 1,626 | 29,30 |
| GW190519_153544 | 0,3064 | 0,2884 | 0,668 | 1,647 | 29,44 |
| GW190521_074359 | 0,2081 | 0,1968 | 0,721 | 1,839 | 30,69 |
| GW190630_185205 | 0,3320 | 0,3288 | 0,693 | 1,734 | 30,00 |
| GW190828_063405 | 0,3162 | 0,3161 | 0,807 | 2,313 | 33,83 |
| GW190910_112807 | 0,3423 | 0,3431 | 0,669 | 1,654 | 29,48 |
| GW200129_065458 | 0,2058 | 0,2013 | 0,734 | 1,895 | 31,06 |
| GW200224_222234 | 0,2542 | 0,2489 | 0,719 | 1,831 | 30,64 |
| GW200311_115853 | 0,6013 | 0,5954 | 0,689 | 1,720 | 29,91 |
| GW230628_231200 | 0,2696 | 0,2596 | 0,705 | 1,776 | 30,27 |
| GW230914_111401 | 0,2686 | 0,2639 | 0,664 | 1,636 | 29,37 |
| GW230927_153832 | 0,2645 | 0,2667 | 0,687 | 1,712 | 29,86 |
| GW231028_153006 | 0,1827 | 0,1823 | 0,787 | 2,180 | 32,95 |
| GW231102_071736 | 0,2564 | 0,2399 | 0,731 | 1,885 | 30,99 |
| GW231206_233901 | 0,2017 | 0,1955 | 0,661 | 1,627 | 29,31 |
| GW231226_101520 | 0,1369 | 0,1354 | 0,671 | 1,659 | 29,52 |
| GW240511_031507 | 0,2293 | 0,2251 | 0,709 | 1,793 | 30,39 |
| GW240514_121713 | 0,2106 | 0,2064 | 0,689 | 1,717 | 29,89 |
| GW240615_113620 | 0,1588 | 0,1576 | 0,629 | 1,537 | 28,74 |
| GW240621_195059 | 0,1649 | 0,1653 | 0,661 | 1,628 | 29,32 |
| GW240705_053215 | 0,2121 | 0,2064 | 0,714 | 1,811 | 30,50 |
| GW240716_034900 | 0,3036 | 0,2921 | 0,643 | 1,575 | 28,98 |
| GW240919_061559 | 0,2462 | 0,2427 | 0,670 | 1,656 | 29,50 |
| GW240920_124024 | 0,1377 | 0,1368 | 0,689 | 1,718 | 29,90 |
| GW241006_015333 | 0,2763 | 0,2669 | 0,734 | 1,897 | 31,07 |
| GW241127_061008 | 0,2371 | 0,2368 | 0,629 | 1,536 | 28,73 |
| GW241129_021832 | 0,2459 | 0,2414 | 0,723 | 1,850 | 30,76 |
| GW241225_082815 | 0,2807 | 0,2805 | 0,607 | 1,479 | 28,37 |
| GW250114_082203 | 0,0578 | 0,0580 | 0,678 | 1,683 | 29,67 |
| GW250119_025138 | 0,3347 | 0,3333 | 0,760 | 2,021 | 31,89 |

σ_comb(31, 1/σ²) = **0,03357** (idêntico ao `sigma_combined` do `E0_CORE.json` `ce5fa2f3bfc98513…`, R-B, std_ddof1); fração máxima de informação = 0,337 (GW250114).

### 4.2 Poder por candidato (|δ̄^pred|/σ_comb; envoltória; M = M_f) — e o número honesto

| k | A: 31 (std) | A: 33 | B: GWTC-3 (10) | C: GW250114 só | ×0,273 (difusão de fase, A) | leitura |
|---|---|---|---|---|---|---|
| 1 | **0,62σ** (δ̄^pred −0,0207) | 0,63 | 0,35 | 0,35 | 0,17 | **UNDERPOWERED** — N₉₀ para 5σ ≈ 3.327 eventos de mistura O4 ou ≈ 320 equivalentes GW250114 (`E0_CORE.json` R-B: N50 2.108, N90 3.327, `GW250114_equivalents_target90` 320); 013-bis: O5 inteiro 2,2–3,1σ; 3G ~207 eventos com SNR_RD ≥ 50 |
| 2 | **1,23σ** (−0,0414) | 1,25 | 0,69 | 0,70 | 0,34 | UNDERPOWERED (N₉₀ ≈ 830) |
| 4π | **7,75σ** (−0,260) | 7,86 | 4,36 | 4,39 | 2,12 | POWERED no A (não em B nem C sozinhos; não sob difusão de fase) |
| 8π | **15,5σ** (−0,521) | 15,7 | 8,71 | 8,78 | 4,23 | POWERED em A, B e C; sob difusão de fase 4,2 (UNDERPOWERED) |
| 2π/κ(a_f) | **18,5σ** (−0,622) | 18,8 | 10,5 | 10,4 | 5,05 | POWERED em A, B e C; sob difusão de fase 5,05 (no limiar) |

**Os números honestos, ditos antes:** (a) com o k que o registro já testou (k = 1), o conjunto publicado inteiro dá 0,62σ — o teste é UNDERPOWERED por fator 8 e NENHUM desfecho pode ser FALSIFIED nem NOT_FALSIFIED_POWERED; o rótulo esperado é NOT_FALSIFIED_UNDERPOWERED ou INCONCLUSIVE_SYSTEMATICS; (b) só a partir de k ≳ 4,8 (k·0,62 ≥ 5 ⟹ k ≥ 8,1 para 5σ no A; e §5: k ≥ 4,7–6,1 para passar a cláusula de sistemática) o conjunto A tem poder; (c) k = 8π e 2π/κ (a leitura literal «tempo = período do fluxo modular») são POWERED a 15–19σ: nesses k o dado publicado **decide** — o que quer que decida, é decisão do dado, não deste documento; (d) o poder é do PAR (k, M, identificação): sob difusão de fase (×0,273) só 2π/κ fica no limiar.

### 4.3 O que NÃO entrou no poder (dito)

σ_sys de família (§5) ainda não somada em quadratura (reduz o poder; para k = 1 a soma com 0,029 dá σ_comb,tot ≈ 0,044 e poder 0,47σ); a incerteza de Kerr por evento (RD-02: +4 % em σ, desprezível); a correlação entre GW250114 nas duas releases (contado uma só vez no A); a seleção (31 da figura do release, «literal event_list/event_map from primary release; not selected by this analysis results»).

---

## 5. Os CONTROLES (todos ditos antes; qualquer um reprovado ⟹ INCONCLUSIVE_SYSTEMATICS)

| id | controle | regra | estado hoje |
|---|---|---|---|
| C1 | **ramo canônico como controle nulo**: τ★ = t_Planck ⟹ δ_pred_A = −3,2e−42 (250 Hz, 4 ms; selada −2,15e−42) ⟹ z ~ 1e−40 | o estimador, rodado com τ★ = t_P, tem de devolver exatamente «correspondência com a RG» (|z_A − z_RG| < 1e−30): é a calibração de que o ramo B não é o canônico | computável sem dado novo |
| C2 | **injeções só-RG** | (a) a calibração de injeção do próprio pSEOB da LVK [KNOWN/DECLARADO]; (b) na casa: injeções GR (dtau220 = 0) e injeções com dtau220 = δ_pred(k) na PE só-220 do WSL — viés recuperado |viés| ≤ 0,2·|δ_pred| e cobertura; custo 63–78 CPU-h por lote | (a) existe; (b) AWAITING (piloto da ORDEM 015 nunca rodou: zero posterior) |
| C3 | **degenerescência spin/massa** | só posteriores de IMR COMPLETO com deformação do 220 (pSEOB): (M_f, a_f) vêm da inspiral+merger; ringdown-only com (M, a) livres (V2 da casa; pyRing 220-only) é DIAGNÓSTICO, nunca o teste (F4: z identificável = 0) | o catálogo A/B/C cumpre |
| C4 | **sistemática do início t₀** | no pSEOB não há t₀ (a deformação é do modelo IMR); nos diagnósticos ringdown-only, a diferença 3 ms × 6 ms (ou 10 t_M × 12 t_M) medida nas MESMAS séries com injeções pareadas e σ da DIFERENÇA — sem soma em quadratura (RD-05/RDV-01) | regra fixada |
| C5 | **família de forma de onda** (SEOB × Phenom) | σ_sys,fam entra em w_i e na cláusula 2: sist_rel = σ_sys/|δ̄^pred| > 0,3 ⟹ INCONCLUSIVE. Número lido (`bis/e0_core/SYSTEMATICS_ADENDO.md` `e3ff1ff9f8201714…`, R-B, O4, SNR 40, início 10 t_M, 206 ruídos): recuperação cruzada Phenom→SEOB −0,0376 ± 0,0030 (sem ruído −0,0328); SEOB→Phenom +0,0382 ± 0,0035 (sem ruído +0,0267); mesma família ≈ 0 (−0,0029 ± 0,0031; +0,0159 ± 0,0039) ⟹ σ_sys,fam ≈ 0,027–0,038 [REAL — NÃO-CEGO; DECLARADO pela bancada]. **Consequência fixada antes:** k_min para sist_rel ≤ 0,3 = 4,67 (σ_sys 0,029) a 6,11 (σ_sys 0,038): para k ∈ {1, 2} o rótulo INCONCLUSIVE_SYSTEMATICS está predeterminado por esta cláusula, salvo redução de σ_sys por réplica publicada (pyRing × pSEOB nos mesmos eventos) ou pela PE da casa | número existe; decisão D8 |
| C6 | **nuisance da referência** c(σ) = c₀ + k_c·σ | ajustado sob as duas hipóteses; offset fixo em 0 proibido; reportar c₀, k_c; valores da 013-bis (c₀ = −0,061 ± 0,068; k_c = +0,79 ± 0,37) são NÃO-CEGOS [DECLARADO] e NÃO são usados como prior | forma fixada |
| C7 | **H1/L1 um bloco por evento**; GW250114 uma vez (release única); sem multiplicar releases sobrepostas | regra do catálogo (`duplicate_policy`) | cumprido |
| C8 | **look-elsewhere** | um k e um M: nenhum fator de tentativas; lista de k: Šidák sobre a lista fixada; os 8 «relógios» da C1 (R-A…R-GLOBAL) NÃO são tentativas deste V1 | regra fixada |
| C9 | **convergência/forma** | χ²/dof ≤ 3; jackknife; fração de informação máxima reportada; a gaussianidade conferida pela razão w90/3,29 ÷ σ_std ∈ [0,9; 1,1] (hoje 31/31) | cumprido |

---

## 6. Os VEREDITOS permitidos (na ORDEM; a primeira regra que se aplica decide; CONFIRMED proibido)

Tokens: `TGL_RAMO_B_RINGDOWN_V1__<k>__<M>__<identificação>__<conjunto>__<desfecho>__…__GATE_UNTOUCHED`.

0. sem estimador selado por hash, sem dado, ou n < 10 ⟹ **`AWAITING_DATA`** (sufixo `INSUFFICIENT_SAMPLE` quando n < 10);
1. C1–C9 reprovado, ou sist_rel = max(|σ_sys,fam|, |σ_sys,t₀|)/|δ̄^pred| > 0,3, ou χ²/dof > 3, ou primário × secundário discordam ⟹ **`INCONCLUSIVE_SYSTEMATICS`** (com o motivo);
2. poder = |δ̄^pred|/σ_usado < 5 ⟹ **`NOT_FALSIFIED_UNDERPOWERED`** (sufixo `POWER_<x>_OF_5_SIGMA`);
3. z_excl = |δ̄ − δ̄^pred|/σ_usado ≥ 5 (com c(σ) profilado; FWER) ⟹ **`FALSIFIED_AT_5SIGMA`** — falsifica o PAR (k, M, identificação) sob a lei; NÃO falsifica β, nem a lei na forma, nem a TGL; a regra não se move (`TheLedgerOfCharges.falsified_extinguishes_the_charge_not_the_rule`);
4. senão ⟹ **`NOT_FALSIFIED_POWERED`**; se além disso |z_RG| ≥ 5, acrescenta-se `__GR_TENSION_REPORTED` — a tensão com a RG é RELATADA, não é da TGL, e **não** vira CONFIRMED (a confirmação é ato do observador humano).

**«Coincidir com a RG» = correspondência recuperada:** se o dado ficar na RG (δ̄ ≈ c(σ)) com poder ≥ 5 para o k fixado, o par cai (FALSIFIED do par) e a correspondência com a RG é o pagamento (a parada, R5/D5): o ramo canônico fica como está; nada disso é derrota da teoria. Se o dado ficar na RG SEM poder (k pequeno), é NOT_FALSIFIED_UNDERPOWERED — e NÃO se lê como «a natureza decidiu».

---

## 7. O que o resultado NÃO decide (dito antes)

- **O gate**: as 18 bandeiras formais são função só do formal (probes negativos do runtime; `the_gate_ignores_the_ledger`); nenhum desfecho aqui move bandeira — nem o degrau experimental (que lê o V11, outra fonte).
- **H2/H3** (o four-frame suave; o equilíbrio local do horizonte): hipóteses nomeadas do teorema mestre; este teste não as toca.
- **β**: a regra matriz; «a lei precede a cobrança» (`the_law_precedes_the_charge`); FALSIFIED extingue a cobrança (o par), não a norma.
- **A implicação da QG** (`QGSolutionComplete.lean:36`: β não entra como hipótese) e a correspondência com a RG no ramo canônico (`ringdown_scope_v376`).
- **A cobrança R2** (propagação, τ★ = t_Planck): outra lei/relógio; segue AWAITING.
- **A lei na forma** Γ_ω = ½βτ★ω²: o que se testa é a escala τ★ = k·GM/c³ (e M, e a identificação), «não a lei de dephasing nem a TGL» (`why_outside_contour`, V2).
- Nenhum NOT_FALSIFIED de ringdown lê como «a natureza decidiu a formulação da QG» (errata ao lado de `NATURE_DECIDES_RINGDOWN_NEXT`, v376).

---

## 8. Cegueira (declaração honesta, canal a canal)

- **Quanto ao ESTIMADOR:** CEGO — nenhum estimador com k, M e identificação fixados rodou sob registro; o script desta pasta leu SÓ σ e spin.
- **Quanto ao DADO (conjuntos A/B/C): NÃO CEGO.** Está no registro da casa desde 22–23/09 (ORDEM 013/013-bis, NÃO-CEGO, [DECLARADO pela bancada]): a deformação comum dos 31 do GWTC-5.0 (+0,072 [+0,015; +0,134] a 90 %; centro ponderado +0,0668 ± 0,0336), o ln B(R-B/RG) do GW250114 (0,029; correção/σ 0,34), e os ln B por leitura do C4 (31: R-B −1,81; R-MOD −3,56; R-LIN −8,22; todos INCONCLUSIVE_SYSTEMATICS pela bancada). **Em nome próprio deste aferidor:** ao inspecionar o ESQUEMA dos catálogos, o script de inspeção imprimiu os três quantis de `dtau220` da primeira linha de cada arquivo (GW150914_095045 no A; a primeira linha do B; o GW250114 no C) e, ao ler o estado da combinação, os ln B por leitura — não era a intenção; fica dito; nenhum desses números entrou no poder nem neste texto além desta declaração.
- **Quanto ao DADO (conjunto D):** CEGO — 31 eventos O4 com strain público sem δτ̂ publicado; só a PE da casa os abre, e só depois do hash deste V1.
- Consequência: o veredito do conjunto A é um veredito **não cego quanto ao dado** e será rotulado assim no token (`__NOT_BLIND_TO_DATA_STATED`), como a casa fez na Fase 6 (V4) e no livro V1.4; a palavra «cego» só cabe ao conjunto D.

---

## 9. A disciplina (ordem de execução; fail-closed)

1. As decisões D1–D12 do operador, verbatim, com carimbo e hash do transcrito (o método do pilar: linha do `.jsonl` sem o fim de linha, sha256).
2. Este rascunho vira `PREREGISTRO_RAMO_B_RINGDOWN_20261005_V1.json` + `.md` na Bancada (`C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_ringdown_05out\`), com o hash congelado da especificação = `sha256(json.dumps(spec, sort_keys=True, ensure_ascii=False, separators=(",",":")))`; backup imediato de bytes antes de tocar qualquer arquivo já existente; registro no mapa (`rotas.py registrar`, rota `ringdown.dephasing`, com os sha256 dos artefatos).
3. O `um.py` (v386 ou a versão que o receber) lê o pré-registro POR HASH antes de qualquer estimador (`prove_ramo_b_preregistration_*`: confere JSON e MD byte a byte; devolve `PRE_REGISTERED_BEFORE_DATA_READ`); é a testemunha no stdout do rito (`rodada_vNNN_stdout.txt` no Nós).
4. A Bancada roda: (i) estágio CEGO — σ_i, a_i, N(a_i), δ^pred, poder, C1 e C5 — grava `PODER_RAMO_B_ANTES_DE_ABRIR.json` com hash; (ii) só então ABRIR o conjunto A (e B, C): δ̂_i, c(σ), δ̄, z_RG, z_B, χ², jackknife, o secundário KDE — grava `RESULTADO_RAMO_B_V1.json` com hash e com a regra do §6 aplicada pela MESMA função (como `gw_stack.py`); (iii) conjunto D: PE só-220 na casa sob o mesmo registro, injeções C2(b), abertura só depois do seu próprio `PODER_ANTES_DE_ABRIR`.
5. O `um.py` lê o resultado por hash e aplica a matriz do §6 sem recalcular; o Nós sela; a custódia leva a pasta inteira.
6. Nenhuma emenda depois de abrir sem estimador NOVO (cláusula V4 da Fase 6); toda correção vai AO LADO, em nome próprio; vereditos proibidos: CONFIRMED, PROVED_BY, «QG confirmada».
7. Todas as superfícies de memória na mesma sessão (regra da linhagem completa): Atlas (verbete «ramo B», append datado), MEMORIA_DA_LINHAGEM, DESENHO_DO_FECHAMENTO (adendo), MEMORY.md/MEMORY_2.md, mapa.

---

## 10. Estatutos (resumo)

| objeto | estatuto |
|---|---|
| a palavra do operador (05/10) | [INPUT] — decisão; «tempo emparelhado à gravidade» cunhagem nova (0 ocorrências antes) |
| «regime gravitônico = c³» (28/07/2025; 17/08/2026; 16/09/2026) | [ONTO — cunhagem do operador; âncoras REAL no acervo] |
| Γ_ω = ½βτ★ω² | [REAL na forma; ONTO — sem termo no kernel (TheMatrixRule.lean:46)] |
| τ★ = k·GM/c³; k; M; fonte × propagação; ensemble × realização | [INPUT] — decisões do operador; as origens de 8π e 2π/κ são [KNOWN] (Hawking/KMS; `unruh_is_kms`), a identificação τ★ = período modular é [ONTO] |
| BCW 2006; pSEOB; os catálogos | [KNOWN]; dados [REAL — lidos por hash] |
| β = α√e | [DERIVED do axioma, v376] — a regra; nunca literal |
| a previsão δ = −x/(1+x), x = βkN(a_f)(M/M_f) | [DERIVED] das entradas |
| o poder do §4 | [REAL — computado às cegas, só σ e spin] |
| σ_sys de família; nuisance c₀, k_c; N₉₀; rota da largura de δf̂ | [REAL — NÃO-CEGO; DECLARADO pela bancada (013-bis)] |
| 0,273 (fração por realização) | [DECLARADO pelo verificador de 28/09] |
| os 3 valores concorrentes (−0,0194/−0,010/−0,005) | [REAL core; DECLARADO] — este V1 os substitui por UMA previsão fixada por (k, M, identificação) |
| o desfecho | a vir; nunca CONFIRMED |

---

## 11. Fontes lidas (caminho · sha256) — nenhuma digitada de memória

- `…\scratchpad\v386\ramo_b\DECISAO_OPERADOR_RAMO_B_05out.json` · `a5d548235522c1129ddd683887ac43d7fc2aec36095b7171af08c3ab076060f3`
- `Nós\um.py` (v385) · `d406ae57251051456b8ee49220e117bc086cedc164b6e9d15e85b516467c4760`
- `Nós\um_absoluto.json` · `475ac8d218b3a5c83c9c032b5ff1cca93db19066236f2de211fa58da8263a9b5` (chaves: `ringdown_scope_v376`, `ringdown_dephasing_protocol/_result/_amendment_v2/_result_v2`, `the_ledger_of_charges_v383`, `clock_test_result_v369`, `dephasing_reach`, `the_matrix_rule_v381.consequences_ratified_20261002.ringdown`)
- `Nós\um_absoluto_selo.json` · `ad5c1ac7affc3949acbf71f84449df746d93c98d0941b63ee45c48e903b8c364`
- `cache\gw\RINGDOWN_DEPHASING_V2_RESULT.json` · `ff15f023dd91d8c77fb003b2efd10c91b22d5bcb5047dc2101885fbb634e15c5` · `cache\gw\C6_RESULTS_GW250114.json` · `781a3741a68875eba0fcef02d596dab7d36103d9e926edc6bec18fb485a055e8`
- `Chatgpt\ORDEM_013_RINGDOWN\C4_CATALOG_220.json` · `93bdc413130d294acde91ec03f8392b8d9c5ec5b33fdc97274371656503d8e17` · `C4_CATALOG_COMBINATION.json` · `f3d8c1959ded3efd15045923ce0cbafe7356ec888ced1934d8d0c183046d0d01` · `C4_GWTC3_220.json` · `d9dc9b09a8d91dc7f85c5e849091db619b1c22a633b09c97d82bcf434e9c6053` · `C4_GWTC3_SELECTION.json` · `ef18f3b0495d58bffc5f968f86ca860eefd3becb570cd75bfc9f88fa8fee5dd3` · `C4_220_INITIAL.json` · `f5550b7b1f129e83b4874f95b223e82ca973e0812bd98c150a6c04cd37747edc` · `C4_FREE_CLOCK.json` · `cbf63327719372780ec3b3c89376360e78828c45198ee5cfd5bf04cd5ea328b1` · `C1_LEITURAS_v4.json` · `126270a896d8589870954b209155f26a8b08295839b31e0e9a6e28e512621980`
- `…\bis\E0_ROUTE_IV_POWER_v2.json` · `ae457e82c8c18b5cccf47d60c785d82b3ec3888db7975f2184666c558e4ddd93` · `bis\e0_core\E0_CORE.json` · `ce5fa2f3bfc985138e5c3a20116b93791a84f8034df3c42ce3ce2781fb7e26be` · `bis\e0_core\SYSTEMATICS_ADENDO.md` · `e3ff1ff9f8201714b60f10ba82562924b2e242d91c710a86976bd70a44f8b973` · `bis\F4_POWER_GATE_REVIEW.md` · `35b02b3d0a4d45ecfbacc156f73c909eeab10f9e12bf07a6ca169b37b6d4d914` · `C7_GWTC3_REPRODUCTION\assets\ORDEM_013_RINGDOWN\catalog_220_readout.py` · `c2b43d633b39195a086a7961cdcc9842ec90fb4d5b25cf5114641b33191707de`
- Bancada: `PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.md` · `fc132b8f3e2d531b438027f00115df5be91856d4506e10385279ae58993892be` · `PREREGISTRO_PILAR_QUANTICO_20261003_V1.md` · `e5b345c5d950d05286f1e0293a314297dc30506f9d424eaea11e489c592275a6`
- Memórias: `ramo-b-reaberto-05out.md`, `ordem-013-confrontacao-ringdown.md`, `beta-e-a-regra-matriz-02out.md` (R1–R6 e a errata de R6 de 05/10), `fase6-eco-radical-01out.md`, `psi-nome-da-luz-graviton-verbo-vivo-16set.md`, `onda-e-eco-definicao-16set.md`, `auditoria-testes-passados-28set.md`, `relatorio-consolidado-01out.md`; Atlas: verbetes Γ_ω (l. 644), ²²⁹Th/τ★ ≲ 1,8e−33 s (l. 778), Dephasing (l. 1101), Eco reclassificado (l. 1149), τ★ (l. 2239).
- Mapa de rotas: `ringdown.dephasing` (seq 24, 25, 26, 27, 44, 85, 86, 88, 89, 90, 92, 132, 141, 249, 352), `kernel.livro_de_cobrancas.otica`, `auditoria.testes_passados_28set`; cabeça do livro `b43d3d46d596671a` (353 registros).

PROVADA ≠ CONFIRMADA. NOT_FALSIFIED nunca é CONFIRMED. Este é um RASCUNHO: o hash que vale é o do V1 congelado depois das decisões do operador.
