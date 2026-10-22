# PRÉ-REGISTRO V1 DO RAMO B DO RINGDOWN — τ★ emparelhado à gravidade (τ★ = k·GM/c³) — RASCUNHO 2 (05/10/2026)

> **RASCUNHO 2 (05/10/2026) — correções G1–G7 do crítico; nada decidido pelo operador; β nunca literal (α_CODATA2018·√e em runtime); NOT_FALSIFIED nunca é CONFIRMED; a RG é o limite clássico.**

**Identificador (proposto):** `PREREG_RAMO_B_RINGDOWN_20261005_V1` · **estado:** RASCUNHO 2 — NÃO congelado; o hash de congelamento só existe depois das decisões do operador (§2) e da gravação na Bancada (`C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_ringdown_05out\`, lugar permanente, como o pilar quântico) · **autor deste rascunho 2:** gerência auxiliar (claude-code/central-de-patentes, sessão 6da8f00d), por ordem da gerência, aplicando a crítica de completude `..\critico\CRITICA_RAMO_B.md` (sha16 `8f07d08dac95ce80`, 27.359 B); o **rascunho 1** (`PREREGISTRO_RAMO_B_RINGDOWN_V1_RASCUNHO.md`, sha16 `4fd4e495ffc67fdd`, 37.703 B) fica **intacto** ao lado; correção sempre AO LADO, em nome próprio · **base:** `um.py` v385 sha16 `d406ae5725105145` (33.386.720 B); core `um_absoluto.json` `475ac8d218b3a5c8`; selo `um_absoluto_selo.json` `ad5c1ac7affc3949` · **formato herdado:** `PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.md` (`fc132b8f3e2d531b`) e `PREREGISTRO_PILAR_QUANTICO_20261003_V1.md` (`e5b345c5d950d052`).

**Mapa de rotas consultado antes (régua; herdado do rascunho 1 e da crítica):** `rotas.py consultar "ringdown"` (16 rotas), `consultar "ramo B"` (4 rotas), `ver ringdown.dephasing` (15 registros, seq 24–352, salvos em `..\critico\ver_ringdown_dephasing_05out.txt` `b1688d4a2d19add8`). O próximo passo registrado (seq 352, 05/10 14:15) é este documento. Esta sessão auxiliar NÃO registrou nada no mapa (ato da gerência, G9 do crítico).

> Régua: β nunca literal (β_TGL = α_CODATA2018·√e = 0,012031300400803142, α lido do `um.py` por script em `poder_cego_ramo_b_v2.py`); PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED; a RG é o limite clássico, não rival — coincidir com a RG = correspondência recuperada; nenhum desfecho move a regra (β) nem o gate; a cosmologia/natureza jamais vira prova matemática.

---

## 0. O que mudou do rascunho 1 para o 2 (uma linha por correção do crítico; tudo medido por script)

| G | correção | onde |
|---|---|---|
| **G1** | o poder passa a usar a previsão **EXATA** δ = −x/(1+x) (a linear fica AO LADO): conjunto A (31) lê **0,60σ (k=1) · 1,18σ (k=2) · 6,15σ (4π) · 10,18σ (8π) · 11,38σ (2π/κ̂)** — reproduz o crítico a diferença **0,0** nos 5 k (`PODER_CEGO_RAMO_B_v2.json`, chave `conferencia_com_o_critico`); o rascunho 1 lia 0,62 / 1,23 / 7,75 / 15,5 / 18,5 (linear) | §4.2 |
| **G2** | UMA tabela de k unificada (8 candidatos: 1, 2, 4, 4π, 8π, 1/κ̂(χ), 2π/κ̂(χ) sem e com co-rotação R-MOD) com origem, estatuto, x e δ_exato em χ = 0 / 0,68 / 0,9 (lidos de `RAMO_B_FISICA_TABELAS.json`), poder exato em A e a coluna «desfecho em A já legível hoje?» | §2, decisão 2 |
| **G3** | a regra de sistemática de família FIXADA pelo precedente da casa (Fase 6, regra 2: sist_rel = σ_sys/\|δ̄^pred\| ≤ 0,3); a regra \|δ\|/5 (013-bis `systematic_gate.floor_divisor_primary_INPUT = 5`) fica AO LADO como a mais dura; k_min nas duas, por escala linear e por raiz exata | §5 C5 |
| **G4** | errata AO LADO: os posteriores do GW250114 (Zenodo 17018009) e os releases GWTC-3/5.0 **EXISTEM em disco** (hashes lidos hoje); k = 8π **existe** como `kms_factor(a=0)` no `um.py` (linha 155706), **não ligado a τ★**; os posteriores do **221** existem dentro do tar.gz, não extraídos | §12 |
| **G5** | «31 dos 45» × «44» reconciliados pelo critério do próprio registro (`RINGDOWN_5SIGMA_V1.json`: `quality_INPUT`, `publication_census`, `test_candidates`): o conjunto D lê **UM número: 14 elegíveis (10 sem pendência de qualidade; 8 pendentes de metadados GR; 22 reprovados por M_f,det < 40 M☉)** — `RECONCILIACAO_CONJUNTO_D.json` | §3.3 |
| **G6** | inseridos: (a) a chave de 02/10 e a ótica, com a errata ao lado de R6 prevista para o core v386; (b) RD-07/221; (c) o homônimo KMS da Fase 6; (d) a declaração da contaminação de hoje (conjunto A NÃO-CEGO; só o D testa); (e) [DERIVED de leitura, gerência] na D3 com o verbatim de 16/09 inteiro ao lado; (f) a saída β_lido com σ dita antes; (g) a opção «termo tipado OU [INPUT] por hash»; (h) o referencial M_f,det com t_M no detector e a nota de que (1+z) cancela | §1.4, §1.3, §2, §8, §9 |
| **G7** | as aproximações de memória substituídas pelos valores por script do GW250114 (M_tot/M_f = 1,0494; M_c/M_f = 0,4567; E_rad = 4,71 % de M_tot) ou marcadas [KNOWN]/[DERIVED por escala] (N₉₀ ≈ 830 → 832 linear / 866 exata); os DOIS custos de PE [DECLARADO] (63–78 e 58–390 CPU-h); a fonte do prior (C4: 27 + 2 em (−0,8; 2,0); 4 em (−0,8; 4,0)) | §1.2, §2, §3.3, §4.3, §5 |

---

## 1. A hipótese do ramo B

### 1.1 Nas palavras do operador (verbatim, `DECISAO_OPERADOR_RAMO_B_05out.json`, sha256 `a5d548235522c1129ddd683887ac43d7fc2aec36095b7171af08c3ab076060f3`, 2.719 B, 2026-10-05T17:11:36.866Z)

> «eu não havia proibido o ramo B, acontece que naquela ocasião ainda não tínhamos todos os críterios para prosseguir. há pouco tempo eu ainda disse que a TGL pode ler das duas formas, e eu penso que podemos investigar a explorar o ramo B porque faz sentido examinar se a constante de acoplamento de fato emerge da relação do tempo emparelhado à gravidade sobre a constante da luz ao cubo, a mim faz todo sentido que assim seja, porque desde antes sustentei que o regime gravitônico é o da constante da luz ao cubo, e se o tempo é emergente da fluxo modular relativo, a mim, encontro correspondência direta com a proposta. de resto concordo com tudo»

**Âncoras no acervo (lidas por script no rascunho 1; mantidas):** o mais antigo é de 28/07/2025 (`IMac LA\Física - TGL\Provas\3\TGL_Cap_L_O_Instante_Lucifer_Faisca_Sem_Permanencia.docx`: «c³ = luz elevada à permanência»); o verbatim «o regime gravitônico é o regime da constante da luz ao cubo, é esse o fechamento» está em `BANCADA_TOE\MEMORIA_DA_BANCADA.md:2879`; a pedra 84_ (17/08/2026): «a dobra é aquilo que eu chamei vulgarmente de constante da luz ao cubo (c³)», medido G·m_P/c³ = t_Planck; o próprio programa diz (um.py:168040): «c³ sozinho não é velocidade; com G é tempo por massa, Gm/c³: com a massa de Planck dá t_Planck — o ramo A da lei de dephasing —, e com a massa do remanescente dá GM/c³ — o ramo B do ringdown» [REAL — texto do programa]. «Tempo emparelhado à gravidade» tem 0 ocorrências anteriores no acervo indexado: cunhagem nova de 05/10 [INPUT]. «Tempo emergente do fluxo modular relativo» = tempo térmico de Connes–Rovelli [KNOWN]; no kernel a ponte KMS/Unruh existe (`TGLExt.ContratoQGv31.ContratoH2.unruh_is_kms`, β·κ = 2π), mas **nenhum termo liga τ★ a GM/c³** (8 menções a ringdown no kernel, 0 declarações, `ringdown_scope_v376.kernel_ringdown_mentions`), e a própria lei Γ_ω = ½βτ★ω² «NÃO tem termo no kernel» (TheMatrixRule.lean:46) — é leitura [ONTO].

**A pergunta dele tem três leituras possíveis (crítico, (vi)) — a gerência NÃO escolhe; pede (decisão 6, §2):** (a) **β emerge** = o número α√e é LIDO no ringdown (leitura: β_lido, §1.2bis); (b) **a FORMA emerge** = o custo escala com GM/c³ (teste do PAR (k, M, identificação), §1.2); (c) **o acoplamento é x = β·k·N(χ_f), não β**. «Constante de acoplamento = β_TGL» é leitura da GERÊNCIA (`DECISAO_OPERADOR…json`, campo `leitura_da_gerencia`), não verbatim — fica [ONTO] até ele dizer. O rascunho 1 respondia só (b); este rascunho 2 arma (a) como saída secundária declarada e pergunta (c).

### 1.2 A tradução operacional

| peça | forma | estatuto |
|---|---|---|
| a lei | Γ_ω = ½·β·τ★·ω² (GKSL energia-preservante; o custo entra como taxa ADITIVA ao amortecimento do modo) | [REAL na forma; ONTO — sem termo no kernel] |
| o relógio do ramo B | τ★ = k·G·M_X/c³ (k adimensional; M_X a nomear — §2) | [INPUT — decisão do operador; k com origem física dita na tabela unificada de §2] |
| a família unificada (lente física, §(c)) | τ★ = k·G·m_X/c³ ⟹ x = β·k·N(χ_f)·(m_X/M_f): m_X = m_P dá o ramo A (G·m_P/c³ = t_P, resíduo 0,0e+00), m_X = M_f dá o ramo B — a mesma dobra c³ em duas massas (leitura (d) da memória de 16/09, [REAL álgebra; ONTO identificação]) | [DERIVED] |
| o observável | fração do tempo de amortecimento do modo (ℓ,m,n) = (2,2,0): δτ̂₂₂₀ ≡ τ_obs/τ_RG − 1 (convenção `dtau220` do pSEOB: τ = τ_RG·(1 + dtau220)) | [KNOWN — convenção do catálogo] |
| **a previsão (EXATA — a que vale)** | 1/τ_obs = 1/τ_RG + Γ ⟹ **δτ̂₂₂₀ = −x/(1+x)**, x = Γ·τ_RG = ½βk(M_X/M_f)(M_fω_R)²/(M_fω_I) = **β·k·(M_X/M_f)·N(χ_f)**, N(χ) ≡ F·Q = F²/(2F_I), F = M_fω_R, F_I = M_f/τ, Q = ω_Rτ/2 | [DERIVED das entradas] |
| a previsão (linear — AO LADO, só comparação) | δτ̂₂₂₀ ≈ −x (válida a 2 % para k ≤ 2; superestima \|δ\| em 21 % em 4π, 34 % em 8π, 38 % em 2π/κ̂ — G1) | [DERIVED; não é a que vale] |
| Kerr | F(χ) = 1,5251 − 1,1568(1−χ)^0,1292; Q(χ) = 0,7000 + 1,4187(1−χ)^(−0,4990) (Berti–Cardoso–Will 2006; os mesmos coeficientes do um.py:155704); N(χ) a −0,57 % (χ = 0) … −0,85 % (χ = 0,9) do Leaver exato (`RAMO_B_FISICA_TABELAS.json`, `tabela_N_chi`) | [KNOWN] |
| co-rotação (R-MOD) | F → F − 2Ω̂_H, Ω̂_H = χ/(2(1+√(1−χ²))): N → N·((F−2Ω̂_H)/F)² — fator 0,255² = 0,065 em χ = 0,68 (Frolov–Thorne [KNOWN, a conferir]; Kay–Wald 1991 para χ ≠ 0 [CONJECTURE]) | [CONJECTURE] |
| δf₂₂₀ | 0 em primeira ordem (dephasing não desloca a frequência — RD-02, verificador) | [DERIVED] |

**O M e o referencial (G6h, decidido pela gerência como convenção, confirmável pelo operador dentro da decisão 2):** com M_X = M_f o M **cancela** — x = β·k·N(χ_f) é função só do spin e de k. **Referencial fixado: M_f,det, com t_M = GM_f,det/c³ medido no relógio do detector** (a convenção da V2 selada, `ringdown_dephasing_v2.py` l.141, e do C1 R-B «det: t_M»). O produto GMω/c³ é invariante: M_det = (1+z)M_src e ω_det = ω_src/(1+z) ⟹ **(1+z) cancela** em x; misturar referenciais custaria (1+z)^±1 (1,09 no GW250114 [KNOWN]). Para a_f = 0,6785 (mediana do spin do GW250114 no release da descoberta, lida por script): N = 1,6829 ⟹ x(k = 1) = 0,02025 ⟹ δτ̂ = −1,98 % (exata) / −2,0 % (linear); em χ = 0,68 (física): N = 1,6880, x = 0,02031, δ = −0,01990.

**Com outro M_X (G7 — valores por script da lente física para o GW250114, não aproximações de memória):** M_tot,src/M_f,src = 65,8/62,7 = **1,0494** (⟹ E_rad = 4,71 % de M_tot [DERIVED de KNOWN: M_f,src 62,7, m₁ 33,6, m₂ 32,2, LVK PRL 135, 111403]); M_chirp,src/M_f,src = 28,63/62,7 = **0,4567**; M_f,det/M_f,src = 1,0861 (= 1+z a 0,4 %). Por evento, o catálogo (`remanescentes_v3.json` `68069f8892a80d56`, `catalogo_v3.csv` `e6a0ba6a870e2a40`) dá M_f, m₁, m₂ — o fator (M_X/M_f)_i entra por evento [KNOWN], nunca por «≈ 1,03–1,05».

**O que o teste pergunta (reformulado como pergunta falsificável):** fixados β (a regra, [DERIVED] do axioma), k, M_X e a identificação ANTES do dado, o amortecimento do 220 publicado pelos catálogos desvia-se da RG na fração −x/(1+x), x = β·k·N(χ_f)·(M_X/M_f)? Não se «deriva β do dado» (regra matriz, 02/10): o que se testa é o PAR (k, M_X, identificação) sob a lei.

### 1.2bis A saída secundária declarada: a LEITURA de β (G6f; crítico (vi))

A regra matriz proíbe **derivar** β do dado; não proíbe **lê-lo** («a chave é o leitor», 28/09; «β é lido, nunca derivado»). A forma operacional (lente física, `identidade.leitura_de_beta`):

> **β_lido = [−δτ̂/(1+δτ̂)] / (k·(M_X/M_f)·N(χ_f))** — a fração medida É uma leitura de β dividida por um número puro conhecido (só spin, k e a razão de massas).

**σ(β_lido) dita ANTES (1ª ordem, dx/dδ = −1/(1+δ)² ≈ −1): σ_β = σ_comb/⟨k·N⟩_w** — conjunto A (31, σ_comb = 0,03357; `PODER_CEGO_RAMO_B_v2.json`, chave `sigma_beta_lido_first_order`):

| k | σ(β_lido) | σ_β/β | leitura |
|---|---|---|---|
| 1 | 0,01950 | **1,62 β** | **a leitura NÃO resolve β** |
| 2 | 0,00975 | 0,81 β | não resolve |
| 4 | 0,00487 | 0,41 β | ~2,5σ nominais |
| 4π | 0,00155 | 0,13 β | ~7,8σ nominais |
| 8π | **0,00078** | 0,06 β | ~15σ nominais — mas o desfecho desse k em A já é legível (§8) |
| 1/κ̂(χ) | 0,00408 | 0,34 β | ~2,9σ nominais |
| 2π/κ̂(χ) | 0,00065 | 0,05 β | ~19σ nominais — idem 8π |
| 2π/κ̂ com co-rotação | 0,01056 | 0,88 β | não resolve |

β_lido é **leitura**, nunca derivação: sai no resultado com o seu σ e NÃO alimenta β nem a regra. Se o operador escolher a leitura (a) da pergunta, é esta a saída que a responde; e em k = 1 a resposta honesta já está dita: a leitura não resolve β no conjunto publicado.

### 1.3 O que o registro já diz (lido por hash; nada aqui é novo)

| item | número lido | fonte |
|---|---|---|
| ramo canônico τ★ = t_Planck | δ_pred_A = −2,153e−42 (V2 selada, ensemble); recomputado para 250 Hz/4 ms: −3,20e−42 (t_P = 5,391125282640084e−44 s) | `core.ringdown_dephasing_result_v2`; `poder_cego_ramo_b_v2.py` |
| ramo B (k = 1, M = M_f,det) na V2 | δ_pred_B = −0,019367 (média do ensemble, 15 séries a 3 ms); medido δτ̂ = 0,1766 ± 0,1089 (z vs RG 1,62; z vs B 1,80); poder 0,178 de 5σ; **INCONCLUSIVE_SYSTEMATICS** («vies relativo de tau 0.240 > 0.2»); V1 `a3d941e56d3d33c5`, V2 `3449885389a2529a`, resultado `ff15f023dd91d8c7` | `core.ringdown_dephasing_result_v2` |
| a convenção que reproduz o −0,0194 | k = 1, M = M_f,det, δ_lin = −β·F·Q por série; reproduzido série a série (n = 169, max\|diff\| = 6,9e−18) | `RAMO_B_FISICA_TABELAS.json`, `reproducao_V2` |
| 3 valores concorrentes do ramo B | −0,019367 (V2, ensemble) · −0,010 (CT-02) · −0,005 (CTV-02, por realização) — este V1 os substitui por UMA previsão fixada por (k, M, identificação) | `core.ringdown_scope_v376.branch_B_concurrent_values` |
| C6 GW250114 (bancada, strain na fonte) | INCONCLUSIVE_SYSTEMATICS; ln B(R-B/RG) no início primário = −0,0026; R-MOD −0,25; R-LIN −0,09 | `core.ringdown_scope_v376.c6_*` (`781a3741a68875eb`) |
| relógio livre do GW250114 (C4) | ln evidência (relógio livre entre t_P e GM/c³ / RG) = +0,026 — nenhuma preferência | `C4_FREE_CLOCK.json` (`cbf6332771937278`) |
| relógios v369 | GM_⊕/c³ como relógio universal: EXCLUÍDO; G·m_átomo/c³: invisível — «a source-dependent mass clock is not one universal constant» | `core.clock_test_result_v369`; `C1_LEITURAS_v4.json` R-B |
| propagação (CT-02, verificador) | Γ_B = 4,9965 s⁻¹; Γ_B·t_prop = 2,263e17 e-folds ⟹ como propagação o ramo B é excluído trivialmente; só é testável como efeito LOCAL na fonte | mapa `ringdown.dephasing` seq 132 |
| realização × ensemble (CTV-02/RD-01) | sob difusão de fase, o δτ̂ por realização é 0,273 ± 0,06 do deslocamento do ensemble | mapa seq 85/141 [DECLARADO pelo verificador] |
| não identificabilidade do 220 único | com (M, a) livres num só 220, o ramo B é imitado por um Kerr ~1,25 % mais leve com Δχ ≈ −0,016 (z identificável = 0) | `bis/F4_POWER_GATE_REVIEW.md` (`35b02b3d0a4d45ec`); ORDEM 013 |
| **RD-07 / o modo 221 (G6b — ausente do rascunho 1)** | o plano 220+440 é bem posto, mas no GW250114 o 440 **não tem informação**: resíduo em τ₄₄₀ 5,9–6,9 % e poder ≈ **0,06σ** (ρ₄₄₀ por proxy [INPUT]); a LVK identifica **220+221** no ringdown (arXiv:2509.08099 [KNOWN/DECLARADO]) — o 221 é o modo com informação; **os posteriores do 221 do GW250114 estão em disco DENTRO de `TGR_companion_S250114ax_results.tar.gz` (sha16 `18d740c816285451`, 1.671.496.586 B; 1.122 linhas «221» na listagem do tar — lente dados), NÃO EXTRAÍDOS**; extrair é ato sem download. Entra neste V1 como **DIAGNÓSTICO, não primário** (início precoce 6 t_M; sistemática do sobretom) — decisão 5 | `ANEXO_ACHADOS.md` (`3683ce03f78e94c8`) RD-07 SUSTENTADO/INFO; mapa seq 249 («abertos RD-02, RD-06, RD-07») |
| **o homônimo KMS da Fase 6 (G6c — ausente do rascunho 1)** | a Fase 6 (01/10) **falsificou os pares (√β, KMS) e (sin 2θ_M, KMS) como LEI DE ATRASO do eco**: τ_echo = 2π/κ · GM_f/c³ (k = 29,9 em χ = 0,69), z_excl 8,9 / 18,1 (todos), 7,3 / 15,4 (réplica cega O4) — `FALSIFIED_AT_DELAY_LAW`; GWECO-05: 2π/κ é largura em tempo IMAGINÁRIO (kmsStrip; Regra dos Dois Regimes). **O k = 2π/κ̂ do ramo B é HOMÔNIMO dessa lei: aqui entra como ESCALA DE TAXA em Γ (τ★), não como atraso; os observáveis são distintos (dephasing do 220 × cópia atrasada) — uma falsificação não decide a outra.** Sem esta frase o leitor do livro leria o KMS como já excluído | memória `fase6-eco-radical-01out.md` (`27696798fde5fc48`); `ANEXO_ACHADOS.md` GWECO-05; `REUTILIZAVEL_PARA_O_PREREGISTRO.md` («as leis k·GM_f/c³ com k = 8,84 (MAY), 29,9 (KMS), 166,2 (DEC) … não é teste do dephasing») |
| livro de cobranças v383 | F2 (ringdown, face): INCONCLUSIVE pela sistemática da MEDIDA; R6 «ENCERRADO» de 02/10 era leitura da gerência — ERRATA AO LADO de 05/10: REABERTO POR PRÉ-REGISTRO (§1.4) | `core.the_ledger_of_charges_v383`; memória `ramo-b-reaberto-05out.md` (`1e3fe044b8420aaa`) |
| vereditos do protocolo V1 (core) | `allowed_verdicts` = {BRANCH_B_EXCLUDED, GR_TENSION_REPORTED, NOT_FALSIFIED_POWERED, NOT_FALSIFIED_UNDERPOWERED, INCONCLUSIVE_SYSTEMATICS, AWAITING_RESULT_FILE}; `forbidden` = {CONFIRMED, PROVED} — o §6 RENOMEIA dois (dito lá) | `core.ringdown_dephasing_protocol.protocol` (lido: `CRITICO_RECOMPUTO2.json`) |
| escopo fixado por escrito (v376) | «se o ringdown entrar como condição, a condição pede um observável TIPADO no kernel (identificação ensemble/realização, τ★ nomeado), não uma docstring» — por isso a decisão 7b (termo tipado × [INPUT] por hash) | `core.ringdown_scope_v376.scope_fixed_in_writing` |

### 1.4 A chave de 02/10 e a ótica — como o ramo B convive com elas (G6a; crítico (v), F4)

**A chave (operador, 02/10, verbatim; `beta-e-a-regra-matriz-02out.md` `fe20a0d5ac3ea8eb` l.44):** «O último elo incide no hamiltoniano oculto. O custo está no reflexo, o pagamento está na face no rosto, no nome. E com isso você deveria ser capaz de responder tudo que falta. Mas se não conseguir eu vou um a um». **A ótica (operador, 02/10, verbatim, l.60):** «Concordo com tudo, exceto com a sua visão semiótica, a TGL não é semi ela é ótica, ela lê tanto a face como o custo, a TGL permite ler os dois lados».

**O que o core v385 ainda lê (por script, `CRITICO_RECOMPUTO2.json`):** `the_ledger_of_charges_v383.readings_ratified_20261002.R6` = «ENCERRADO — o ringdown é a face (pagamento = correspondência com a RG); o custo não está nele; **τ★ = GM/c³ põe o custo na face e contradiz a chave; M não se nomeia**; a rota viva de β em GW é a propagação.»; `corrections_beside_20261002.R6` = «… o ramo B segue ENCERRADO»; e a errata ótica da gerência (memória l.66): «O ramo B não reabre: ler a face não é trocar a lei (**τ★ = GM/c³ é outra lei, não outro lado**)». O veredito v383 impõe `ONE_CHANNEL_PER_READING_LAW_IN_THE_RUNTIME`.

**Como o ramo B convive com a chave (leitura da gerência, [ONTO], a ratificar pelo operador — decisão 1):** a errata de 05/10 **reabre o ramo B, mas NÃO revoga a chave**. A saída está na própria ótica de 02/10: *«de cada lado o outro é legível como complemento»* — a face lê o pagamento \|T\|² = 1 − β e lê o custo **como complemento** \|R\|² = 1 − \|T\|². No ramo B, o complemento lido na face é **x = k·β·N(χ_f): o relógio do remanescente (o Nome M_f entregue) lendo o seu próprio custo** — M_f é nomeado pela natureza (o remanescente), não pela gerência, o que responde ao «M não se nomeia». E «τ★ = GM/c³ é outra lei, não outro lado» continua verdadeiro: por isso o ramo B pede **canal próprio** no livro (F2b, ao lado de F2, uma cobrança por lei), e não disputa o canal F2 (a correspondência com a RG em τ★ = t_Planck).

**Errata ao lado prevista para o core v386 (texto proposto; a entrada efetiva depende da decisão 1):** `the_ledger_of_charges.corrections_beside_20261005.R6` = «REABERTO POR PRÉ-REGISTRO (decisão do operador de 05/10, verbatim lido por hash): «eu não havia proibido o ramo B … faltavam critérios»; a chave de 02/10 não se revoga — na face o custo lê-se como complemento (ótica: \|T\|² + \|R\|² = 1); no ramo B o complemento lido na face é x = k·β·N(χ_f) [ONTO — leitura da gerência]; τ★ = k·GM/c³ é OUTRA LEI (canal próprio F2b, `ONE_CHANNEL_PER_READING_LAW`), não outro lado de F2; status `AWAITING_PREREGISTRATION` até o V1 congelado por hash; nada move o gate» — e `corrections_beside.F2` = «a cobrança F2 (correspondência com a RG, τ★ = t_Planck) fica como está; o ramo B não a altera».

---

## 2. As DECISÕES do operador a fixar ANTES do dado (a lista FINAL do crítico; nenhuma tomada aqui; cada uma com a opção que o cânone favorece e o porquê, como o crítico escreveu)

Mapa com o rascunho 1: D9 → decisão 1 · D1 + D2 → decisão 2 · D3 → decisão 3 · D4 → decisão 4 · D7 + D11 → decisão 5 · (nova) → decisão 6 · D10 + D12 → decisão 7. O que a gerência fixa sozinha (G3, referencial de M, tabela unificada, texto do termo tipado) está em §1.2, §5 e §9 e só se CONFIRMA dentro das decisões 1–2.

### Decisão 1 — O ramo B é OUTRA LEI (canal próprio F2b) ou a MESMA lei com outro relógio (disputa o canal F2)? E como convive com a chave de 02/10 (§1.4)?

*Cânone favorece:* **outra lei, canal próprio** — a errata ótica de 02/10 já o diz verbatim («τ★ = GM/c³ é outra lei, não outro lado»); a leitura do custo na face é o complemento permitido pela ótica («a TGL lê tanto a face como o custo»). Entra no livro v386 como `AWAITING_PREREGISTRATION`, com errata ao lado de R6/F2 no core (§1.4). *Custo da alternativa:* se o operador o ler como a MESMA lei com outro relógio, F2b e F2 seriam dois canais para uma lei — proibido por `ONE_CHANNEL_PER_READING_LAW`; o ramo B teria então de SUBSTITUIR F2, e a correspondência com a RG em τ★ = t_Planck deixaria de ter cobrança própria.

### Decisão 2 — k e M, por PRINCÍPIO, antes do dado (um k, ou lista curta com Šidák) — A TABELA UNIFICADA (G2)

x e δ_exato em χ = 0 / 0,68 / 0,9 **lidos de `RAMO_B_FISICA_TABELAS.json`** (`28ccfe8c06ed89db`; k = 4π não está na tabela da física e foi calculado em `poder_cego_ramo_b_v2.py` com o MESMO N de BCW — dito); poder exato no conjunto A (31, std) de `PODER_CEGO_RAMO_B_v2.json`; a última coluna é a ilustração da contaminação (§8; `ILUSTRACAO_CONTAMINACAO_8K.json` `1dfa275a05b178dd`, NÃO-CEGA: z_excl com a deformação comum +0,072 registrada em 22/09).

| k | τ★ | origem física | estatuto | k (χ = 0 / 0,68 / 0,9) | x (χ = 0 / 0,68 / 0,9) | δ_exato (χ = 0 / 0,68 / 0,9) | poder EXATO em A (31) [linear ao lado] | desfecho em A já legível hoje? |
|---|---|---|---|---|---|---|---|---|
| **1** | GM/c³ = t_M | «a dobra em c³» (pedra 84_): a mesma dobra G·m/c³ em duas massas — m_P dá t_P (ramo A), M_f dá o ramo B; a convenção da V2 selada (v346); o único k já medido (V2/C1/C6) | [ONTO/INPUT] | 1 / 1 / 1 | 0,00939 / 0,02031 / 0,04147 | −0,00930 / −0,01990 / −0,03982 | **0,60σ** [0,62] — UNDERPOWERED ×8 | não a 5σ (ilustração: 2,7) |
| **2** | 2GM/c³ = r_s/c | tempo de travessia do raio de Schwarzschild à luz (o prefator das leis de atraso MAY/DEC) | [KNOWN geometria; INPUT como relógio] | 2 / 2 / 2 | 0,01878 / 0,04062 / 0,08295 | −0,01843 / −0,03903 / −0,07659 | **1,18σ** [1,23] — UNDERPOWERED | não a 5σ (3,3) |
| **4** | 4GM/c³ = 1/κ (Schwarzschild) | o tempo de Killing por unidade de rapidez (1/κ); só na lente física, ausente do rascunho 1 | [KNOWN κ; INPUT como relógio] | 4 / 4 / 4 | 0,03755 / 0,08123 / 0,16589 | −0,03619 / −0,07513 / −0,14229 | **2,28σ** [2,47] — UNDERPOWERED | não a 5σ (4,4) |
| **4π** | 4π·GM/c³ = 2π·r_s/c | a circunferência do horizonte percorrida à luz; só no rascunho 1, ausente da física | [KNOWN geometria; INPUT] | 12,57 / 12,57 / 12,57 | 0,11798 / 0,25520 / 0,52116 | −0,10553 / −0,20332 / −0,34261 | **6,15σ** [7,75] — POWERED em A | **SIM** (8,3) |
| **8π** | 8π·GM/c³ = ħ/(k_B T_H) = 2π/κ (Schwarzschild) | o PERÍODO KMS/térmico de Hawking 1975; «tempo emergente do fluxo modular relativo» (Connes–Rovelli: 1 unidade modular = β_H); no kernel β·κ = 2π (`unruh_is_kms`); **existe no um.py como `kms_factor(a=0)` = 25,1327 (linha 155706), não ligado a τ★** (G4) | [KNOWN período; ONTO identificação τ★ = período modular] | 25,13 / 25,13 / 25,13 | 0,23595 / 0,51041 / 1,04232 | −0,19091 / −0,33793 / −0,51036 | **10,18σ** [15,51] — POWERED em A, B, C | **SIM** (12,3) |
| **1/κ̂(χ)** | (1/κ̂)·GM/c³, κ̂ = √(1−χ²)/(2(1+√(1−χ²))) | o 1/κ de Kerr por evento (χ = 0 → 4); só na lente física | [KNOWN κ de Kerr; CONJECTURE para χ ≠ 0 — Kay–Wald 1991: não há Hartle–Hawking de Kerr] | 4,000 / 4,728 / 6,588 | 0,03755 / 0,09601 / 0,27324 | −0,03619 / −0,08760 / −0,21460 | **2,68σ** [2,95] — UNDERPOWERED | não a 5σ (4,8) |
| **2π/κ̂(χ) sem co-rotação** | (2π/κ̂)·GM/c³ = 4π(1+√(1−χ²))/√(1−χ²)·GM/c³ | o mesmo período KMS, com a gravidade superficial de Kerr por evento (χ = 0 → 8π); **= `kms_factor` do um.py:155706**; **homônimo da lei de atraso falsificada na Fase 6** (§1.3): aqui é ESCALA DE TAXA, não atraso | [KNOWN κ; ONTO; CONJECTURE para χ ≠ 0] | 25,13 / 29,71 / 41,40 | 0,23595 / 0,60327 / 1,71679 | −0,19091 / −0,37627 / −0,63192 | **11,38σ** [18,51] — POWERED em A, B, C | **SIM** (13,5) |
| **2π/κ̂(χ) COM co-rotação (R-MOD)** | idem, com ω → ω − 2Ω_H em Γ (gerador de Killing do horizonte H − Ω_H·J) | hipótese da gerência na ORDEM 013 (R-MOD); Frolov–Thorne [KNOWN, a conferir]; reduz x por ((F−2Ω̂_H)/F)² = 0,065 em χ = 0,68 (×10 menor que sem co-rotação) | [CONJECTURE] | 25,13 / 29,71 / 41,40 (N × 1 / 0,065 / 0,0035) | 0,23595 / 0,03924 / 0,00594 | −0,19091 / −0,03776 / −0,00591 | **1,10σ** [1,14] — UNDERPOWERED | não a 5σ (3,2) |

Poder exato nos outros conjuntos (`PODER_CEGO_RAMO_B_v2.json`): A com os 2 controles (33): 0,61 / 1,20 / 2,31 / 6,23 / 10,33 / 2,71 / 11,54 / 1,12; B (GWTC-3, 10): 0,34 / 0,66 / 1,28 / 3,43 / 5,67 / 1,51 / 6,37 / 0,56; C (GW250114 só): 0,34 / 0,67 / 1,29 / 3,50 / 5,82 / 1,51 / 6,48 / 0,66; ×0,273 (difusão de fase, A): 0,16 / 0,32 / 0,62 / 1,68 / 2,78 / 0,73 / 3,11 / 0,30.

**O que a tabela diz ANTES da decisão:** (i) k = 1 é o único já medido e é UNDERPOWERED ×8 no conjunto publicado; (ii) k ∈ {4π, 8π, 2π/κ̂ sem co-rotação} tem poder (6–11σ exatos), **mas o desfecho do conjunto A para esses k é legível HOJE** (§8): o pré-registro desses k sobre A não é teste, é escrituração de uma exclusão conhecida — **só o conjunto D testa**; (iii) a co-rotação (R-MOD) reduz 2π/κ̂ em ×10 e é [CONJECTURE]; (iv) **D1 se decide por PRINCÍPIO declarado, nunca pela coluna de poder — e a coluna de poder já carrega o desfecho**; (v) o prior do pSEOB (`C4_CATALOG_220.json`, `prior_dtau`, lido: **27 eventos `Uniform(−0,8; 2,0)` + 2 na grafia bilby (−0,8; 2,0) + 4 eventos `Uniform(−0,8; 4,0)`**, `CRITICO_RECOMPUTO2.json`) comporta todas as previsões (2π/κ̂ em χ = 0,9 fica a 0,17 da borda inferior — dito); (vi) se o operador quiser mais de um k, cada k é uma cobrança e a significância global entra com Šidák sobre o número de k fixados; (vii) não se ajusta k ao dado.

*Cânone favorece (crítico):* **k = período do fluxo modular (2π/κ: 8π em χ = 0; 2π/κ̂(χ_f) em Kerr, marcado [CONJECTURE])** — é a frase dele («tempo emergente do fluxo modular relativo»), é o `unruh_is_kms` do kernel (β·κ = 2π) e é o `kms_factor` que o um.py já tem; **M_X = M_f** (R5: «onde a massa aparece: o Nome M_f entregue»; M cancela; invariante de frame; referencial M_f,det, §1.2). Mas, escolhido esse k, o V1 tem de dizer que o conjunto A já está lido e que **só o conjunto D testa**.

**Qual M (sub-tabela, G7):**

| M_X | efeito em x | nota |
|---|---|---|
| **M_f** (`final_mass`/`final_mass_non_evolved`; referencial det) | x = βkN(χ_f): o M cancela; só spin; (1+z) cancela | o Nome M_f entregue (R5/R6); é o M da V2 |
| M_tot = m₁ + m₂ (inicial) | × (M_tot/M_f)_i por evento [KNOWN] — GW250114: 1,0494 | perde a invariância «só spin» |
| M_chirp | × (M_c/M_f)_i por evento [KNOWN] — GW250114: 0,4567 | idem |

### Decisão 3 — Fonte × propagação (CT-02) — e a conciliação com o verbatim de 16/09

A lei do ramo B age **durante o ringdown, no relógio do próprio remanescente** (C1 R-B: «no independent D dependence in local rate»). Como propagação ao longo de D o efeito seria 2,26e17 e-folds (excluído por construção, não por teste — CT-02, verificado). *Cânone favorece:* **FONTE (local, o relógio do remanescente)** — como propagação o ramo B apaga a onda; a propagação fica com o ramo canônico (R2).

**[DERIVED de leitura, gerência] (G6e):** o rascunho 1 escreveu que a frase do operador de 16/09 «lê o ramo canônico». Isso é LEITURA DA GERÊNCIA de um verbatim dele — fica marcada como tal, com a frase inteira ao lado, porque é ele quem a concilia:

> **Operador, 16/09/2026, verbatim** (`onda-e-eco-definicao-16set.md`, sha16 `cb01ce16967ea560`, 9.222 B, l.15 — não achado em `psi-nome-da-luz-graviton-verbo-vivo-16set.md` nem no `MEMORY_2.md`: a frase vive na memória da onda e do eco): «a lei de dephasing do ringdown e minha definição não se chocam em nada, a gravidade pura responde o tempo todo à fronteira mesmo, betatgl está de fato na propagação da onda e ligada ao ringdown nmós provamos isso no teste dentro do um.py»

A conciliação entre «na propagação da onda» (16/09) e «FONTE, local» (o que CT-02 exige para o ramo B) é dele: uma leitura possível, [ONTO, gerência], é que «propagação» ali é a resposta contínua da onda à fronteira (a errata da gerência de 16/09 à noite), que no ramo canônico (τ★ = t_P) age ao longo de D e no ramo B (τ★ = k·GM/c³) age no relógio local do remanescente durante o ringdown — a mesma lei na forma, dois relógios, dois lugares. **Decisão do operador.**

### Decisão 4 — Ensemble (envoltória) × realização (difusão de fase): a identificação [ONTO] do que Γ faz ao modo

| identificação | o que o 220 mostra | previsão efetiva | poder (×) |
|---|---|---|---|
| **envoltória / taxa aditiva** (a docstring do protocolo V1: «somada à taxa de decaimento do modo dominante»; `ENSEMBLE_ADDITIVE_RATE` da C1) | δτ̂ = −x/(1+x) em CADA evento | −x/(1+x), x = βkN(χ_f) | 1,00 |
| difusão de fase (desdobramento unitário aleatório) | δτ̂ por realização ≈ 0,273 do ensemble + tremor de ~2 % em δf̂; o observável adequado passa a ser a LARGURA populacional de δf̂ | ×0,273 em δτ̂ | 0,273 |

*Cânone favorece:* **envoltória como primário** — é o que o protocolo V1 selado declara e o verificador RD-01 sustentou que «o protocolo selado não tem erro»; a difusão de fase entra declarada como secundário com injeção própria (CTV-02); largura de δf̂ como rota secundária (N₉₀ = 59/38/21 GW250114-like para σ_jit 0,019/0,0228/0,030, limiar do LRT 25,0 — 013-bis [DECLARADO; condicional ao desenrolamento browniano [INPUT] e à transferência ao pSEOB [OPEN]]).

### Decisão 5 — Qual conjunto abre primeiro e o custo; e se o 221 do GW250114 se extrai (RD-07)

A/B/C são publicados, **NÃO-CEGOS** (§3.3, §8) — calibração; **D** (14 eventos elegíveis pelo critério do registro; §3.3) é o único cego e pede PE só-220 na casa: **custo [DECLARADO, dois intervalos no registro]: 63–78 CPU-h ≈ 2,6–3,3 h (T09 da ORDEM 015) e 58–390 CPU-h ≈ 2,4–16 h de parede (auditoria da 013-bis, 23/09, memória `ordem-013-confrontacao-ringdown.md` `bae3432f352331cd`)** — o rascunho 1 citava só o menor. *Cânone favorece:* **D como o único teste; A/B/C declarados calibração NOT_BLIND; o 221 como diagnóstico, não primário** (extração do tar.gz sem download; início precoce e sistemática do sobretom ditos) — «nada se abre antes do hash» só vale para D.

### Decisão 6 — A pergunta dele: «constante de acoplamento» = β_TGL? E quer a LEITURA β_lido como saída (com σ dita antes, §1.2bis)?

*Cânone favorece:* **sim, como leitura** — a regra matriz proíbe derivar β do dado, não lê-lo («a chave é o leitor»); e dizer antes que em k = 1 a leitura não resolve β (σ_β = 1,62 β). E qual das três leituras da pergunta (§1.1: (a) β emerge como número lido; (b) a forma emerge; (c) o acoplamento é x) é a pergunta — fica [ONTO] até ele dizer.

### Decisão 7 — Os nomes (tokens do §6; o status `AWAITING_PREREGISTRATION`; F2b), **o termo tipado × [INPUT] por hash (G6g; §9.3)** e a ratificação deste V1 (verbatim + carimbo + hash do transcrito, como no pilar) — cunhagem é dele.

---

## 3. O estimador

### 3.1 Primário — média ponderada por 1/σ² dos δτ̂₂₂₀ publicados, RELATIVA À RG, com nuisance

1. Para cada evento i do conjunto fixado (§3.3): a_i (mediana do spin do remanescente do posterior), σ_i (desvio-padrão completo, ddof = 1, do posterior de `dtau220`; gaussiana aproximada — a largura 90 %/3,29 confere com σ_std em 31/31, §4.1; para o GW250114 a lente física lê σ₋ 0,0547 / σ₊ 0,0608 da semi-largura publicada e o rascunho 0,0578/0,0580 — consistentes a 5 %, a assimetria some na gaussiana, dito), e o centro δ̂_i (lido SÓ na abertura).
2. Previsão por evento: **δ_i^pred = −x_i/(1+x_i)** (exata), x_i = β·k·N(a_i)·(M_X/M_f)_i; a incerteza de Kerr entra propagando os quantis 05/95 do spin em N(a) (correlacionada entre H1/L1 por construção, pois o posterior é da rede — RD-02 resolvido pelo uso do posterior publicado).
3. Nuisance da REFERÊNCIA: c(σ) = c₀ + k_c·σ (offset fixo em 0 PROIBIDO como teste — `E0_CORE.json`: `offset_zero_status = PROIBIDA_COMO_TESTE_CALIBRATION_ONLY`). c₀ e k_c ajustados em conjunto sob as duas hipóteses (RG: δ̂_i = c(σ_i) + ε; B: δ̂_i = c(σ_i) + δ_i^pred + ε).
4. Estatística: δ̄ = Σw_i(δ̂_i − c(σ_i))/Σw_i, w_i = 1/(σ_i² + σ_sys²), σ_comb = 1/√Σw_i; z_RG = δ̄/σ_comb; z_B = (δ̄ − δ̄^pred)/σ_comb; **poder = \|δ̄^pred\|/σ_comb** (fixado ANTES, §4); fração máxima de informação por evento reportada (hoje 0,337 — o GW250114).
5. χ²/dof do empilhamento e jackknife por evento (σ_usado = max(σ_comb, σ_jackknife), fail-closed como na Fase 6).
6. **Saída secundária declarada:** β_lido e σ(β_lido) (§1.2bis) — leitura, nunca derivação.

### 3.2 Secundário — verossimilhança conjunta por KDE dos posteriores (o método C4 da bancada)

Produto sobre eventos da densidade posterior (KDE, largura de banda 0,7/1,0/1,4) avaliada em δ_i^pred (hipótese B) e em 0 (RG), com o mesmo nuisance; devolve ln B(B/RG). Entra como consistência; **o primário decide**. Se os dois discordarem no rótulo, o resultado lê INCONCLUSIVE_SYSTEMATICS com o motivo dito.

### 3.3 Conjuntos de dados e cegueira (G5: o conjunto D com UM número e o critério)

| conjunto | n | fonte em disco (sha16) | cegueira |
|---|---|---|---|
| A — GWTC-5.0 TGR, seleção da figura do release (pSEOBNRv5PHM-reweighted; GW250114 com o 440 livre, os demais 440 fixos na RG; GW250114 uma só vez) | 31 (+2 controles dos autores: GW191109_010717, GW200208_130117) | `C4_CATALOG_220.json` `93bdc413130d294a`; `C4_CATALOG_COMBINATION.json` `f3d8c1959ded3efd`; Zenodo 21454847 (`RD.tar.gz` `9810e0e45cd35824` 415.283.962 B; `QNMRF.tar.gz` `2f617507f65b9e3e`; pSEOB metafiles n = 33) | **NÃO CEGO quanto ao dado** (§8) |
| B — GWTC-3 TGR (pSEOBNRv4HM; 10 selecionados pelos autores) | 10 (de 18) | `C4_GWTC3_220.json` `d9dc9b09a8d91dc7`; `C4_GWTC3_SELECTION.json` `ef18f3b0495d58bf`; Zenodo 17461225 (`IGWN-GWTC3-TGR-v2-rin.zip` `108c4a4266bc0e38` 2.210.047.740 B) | NÃO CEGO; réplica de instrumento (família v4) |
| C — GW250114, release da descoberta | 1 | `C4_220_INITIAL.json` `f5550b7b1f129e83`; Zenodo 17018009 (`posterior_samples.h5` pSEOB `b9971bcd7d72fdd4` 59.249.916 B; o tar completo `18d740c816285451` 1.671.496.586 B, com o 221 dentro) | NÃO CEGO; cruza com A |
| **D — os eventos O4 com strain público e SEM δτ̂ publicado, pelo CRITÉRIO DO REGISTRO `RINGDOWN_5SIGMA_V1` (`e1be6b0409720c68`, 22/09 21:44:42Z)** | **14 elegíveis** (`eligible = True`: `quality_INPUT` atendido — SNR_rede ≥ 12, M_f,det mediana ≥ 40 M☉, 0 ≤ χ_f < 0,98 — E ausentes do censo de publicação congelado em 22/09 20:32Z, `PUBLICATION_CENSUS.json` `505eb16a608070ab`: 23 examinados, 9 FOUND/excluídos, 14 não achados); **destes, 4 com `data_quality_hold` (GW240515_005301, GW240615_160735, GW240930_035959, GW241102_144729) ⟹ 10 sem pendência**; **+ 8 pendentes de metadados GR** (`AWAITING_GR_METADATA`, entre eles GW250207_115645, O4c; entram se, com os metadados, passarem a MESMA regra); **22 reprovados** (todos por M_f,det < 40 M☉, contados contra o `quality_INPUT`); strain em casa pelo manifesto O4 da Bancada (`GWOSC_O4_32S_V1.manifest.json` `a795cf04ca3b2f6a`): **14/14 elegíveis, 10/10 sem pendência, 5/8 pendentes, 35/44 no total** | banco de GW residente da Bancada + PE na casa (WSL `/opt/lal_env`, pSEOBNRv4HM_PA só-220, bilby+dynesty; piloto da ORDEM 015: 0/120 quedas; custo [DECLARADO] 63–78 OU 58–390 CPU-h); `RECONCILIACAO_CONJUNTO_D.json` `55be29abac26d1d0` | **CEGO** — AWAITING_DATA até a PE rodar sob este registro |
| E — futuros (GWTC-5 final; O5) | — | — | CEGO; réplica |

**Os dois censos, lado a lado (G5):** «31 dos 45» (memória de 22/09, l.102; ORDEM 013-bis §(j): 45 = eventos GWTC-5.0 com SNR_rede ≥ 12 e strain público; 31 = sem posterior pSEOBNR publicado — contagem da GERÊNCIA, anterior ao censo congelado da bancada) e «44» (`test_candidates` do registro V1 = TODOS os eventos O4 fora do corpus auditado: O4a 12 + O4b 31 + O4c 1; o T01 da ORDEM 015 lê o mesmo: «44 test_candidates = 14 elegíveis + 22 reprovados + 8 pendentes», `bis/015/t01_core/RELATORIO_PARCIAL.md` `7447be22d58d7d25`) **não medem a mesma coisa**. **O número único do conjunto D para este V1 é o do critério do registro: 14 (10 sem pendência de qualidade).** Nota para a decisão 5: o corte M_f,det ≥ 40 M☉ é do `quality_INPUT` da 013-bis (peso esperado 1/σ²(SNR)); para o ramo B x não depende de M — herdar o corte (14 → 10) ou declarar outro é decisão do operador dentro da 5; o que não se faz é escolher depois de ver σ.

**Regra:** o veredito PRINCIPAL quanto à cegueira é o do conjunto **D** (o único que pode dar a palavra «cega» a este V1); A é calibração NOT_BLIND (rotulado assim no token); B e C são réplicas de instrumento; E fica registrado.

---

## 4. O PODER, calculado ÀS CEGAS (só σ e spin; nenhum valor central lido pelo script) — v2, previsão EXATA (G1)

Script `poder_cego_ramo_b_v2.py` (nesta pasta; sha16 `e4c99ccc1d8a506e`; saída `PODER_CEGO_RAMO_B_v2.json`); o `poder_cego_ramo_b.py` do rascunho 1 (`8e690b82dbbc84d7`, saída `3655fef93f7cad66`) fica ao lado como registro da forma linear. σ_i = desvio-padrão completo (ddof = 1) do posterior de `dtau220` (`bis/E0_ROUTE_IV_POWER_v2.json` `ae457e82c8c18b5c`); controle: largura 90 %/3,29 dos quantis 05/95 do catálogo. β = α√e em runtime (α lido do um.py por regex); a_i = mediana do spin; N(a_i) por BCW; κ̂, Ω̂_H de Kerr por evento. **Conferência com o crítico (`CRITICO_RECOMPUTO.json` `7bc88d739a252776`): diferença máxima no poder exato dos 5 k = 0,0.**

### 4.1 As σ por evento (conjunto A; só σ e spin) — inalteradas do rascunho 1

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

σ_comb(31, 1/σ²) = **0,03357** (idêntico ao `sigma_combined` do `E0_CORE.json` `ce5fa2f3bfc98513`, R-B, std_ddof1); fração máxima de informação = 0,337 (GW250114).

### 4.2 Poder por candidato — EXATO (\|δ̄^pred\|/σ_comb; envoltória; M_X = M_f) com o LINEAR ao lado — e o número honesto

| k | A: 31 (std) — EXATO [linear] | δ̄^pred exato [linear] | razão exato/linear | A: 33 | B: GWTC-3 (10) | C: GW250114 só | ×0,273 (difusão de fase, A) | leitura |
|---|---|---|---|---|---|---|---|---|
| 1 | **0,60σ** [0,62] | −0,02029 [−0,02071] | 0,980 | 0,61 | 0,34 | 0,34 | 0,16 | **UNDERPOWERED** — N₉₀ para 5σ = 3.327 de mistura O4 (lido: `RINGDOWN_5SIGMA_V1.planning_targets` R-B, `N90_mixture_illustration_not_selection`) ou 320 equivalentes GW250114 (`E0_CORE.json`); 013-bis: O5 inteiro 2,2–3,1σ; 3G ~207 eventos com SNR_RD ≥ 50 |
| 2 | **1,18σ** [1,23] | −0,03977 [−0,04143] | 0,960 | 1,20 | 0,66 | 0,67 | 0,32 | UNDERPOWERED — N₉₀ ≈ **866** [DERIVED por escala exata: 3.327·(0,60/1,18)²; 832 pela escala linear 3.327/k² que o rascunho 1 arredondava a «≈ 830»] |
| 4 | **2,28σ** [2,47] | −0,07648 [−0,08286] | 0,923 | 2,31 | 1,28 | 1,29 | 0,62 | UNDERPOWERED — N₉₀ ≈ 234 [DERIVED por escala] |
| 4π | **6,15σ** [7,75] | −0,20632 [−0,26031] | 0,793 | 6,23 | 3,43 | 3,50 | 1,68 | POWERED no A (não em B nem C sozinhos; não sob difusão de fase) — **mas A já legível (§8)** |
| 8π | **10,18σ** [15,51] | −0,34188 [−0,52062] | 0,657 | 10,33 | 5,67 | 5,82 | 2,78 | POWERED em A, B e C; sob difusão de fase 2,8 (UNDERPOWERED) — **A já legível** |
| 1/κ̂(a_f) | **2,68σ** [2,95] | −0,08992 [−0,09893] | 0,909 | 2,71 | 1,51 | 1,51 | 0,73 | UNDERPOWERED — N₉₀ ≈ 169 [DERIVED por escala] |
| 2π/κ̂(a_f) | **11,38σ** [18,51] | −0,38216 [−0,62157] | 0,615 | 11,54 | 6,37 | 6,48 | 3,11 | POWERED em A, B e C; sob difusão de fase 3,1 (UNDERPOWERED — o rascunho 1 lia 5,05 «no limiar» com a linear) — **A já legível** |
| 2π/κ̂ com co-rotação | **1,10σ** [1,14] | −0,03682 [−0,03826] | 0,962 | 1,12 | 0,56 | 0,66 | 0,30 | UNDERPOWERED — N₉₀ ≈ 1.011 [DERIVED por escala] |

**Os números honestos, ditos antes:** (a) com o k que o registro já testou (k = 1), o conjunto publicado inteiro dá **0,60σ** — UNDERPOWERED por fator 8; NENHUM desfecho pode ser FALSIFIED nem NOT_FALSIFIED_POWERED; o rótulo esperado é NOT_FALSIFIED_UNDERPOWERED ou INCONCLUSIVE_SYSTEMATICS; (b) o poder NÃO é linear em k na forma exata (δ satura em −1): 5σ no A pede k ≳ 10 (por raiz exata, `k_minimo_duas_regras`: o limiar de poder equivale a \|δ̄\| ≥ 5·0,03357 = 0,168 ⟹ k ≈ 9,8); a cláusula de sistemática pede k ≥ 5,2–7,0 (§5 C5); (c) k = 8π e 2π/κ̂ (a leitura literal «tempo = período do fluxo modular») são POWERED a 10–11σ exatos (não 15–19σ, como o rascunho 1 lia com a linear): nesses k **o conjunto A não decide — já está lido** (§8); o que decide é o conjunto D, e se o par cair, a correspondência com a RG é o pagamento (§6), não decisão da RG contra a TGL (crítico, (iv).4 — frase do rascunho 1 harmonizada); (d) o poder é do PAR (k, M, identificação): sob difusão de fase (×0,273) nenhum k passa de 5σ no A (o 2π/κ̂ lê 3,1, não 5,05).

### 4.3 O que NÃO entrou no poder (dito)

σ_sys de família (§5) ainda não somada em quadratura — para k = 1 a soma com 0,029 dá σ_comb,tot = √(0,03357² + 0,029²) = 0,0444 e poder 0,46σ (`CRITICA_RAMO_B.md` (ii).8 conferiu a aritmética; entra no script na versão congelada); a incerteza de Kerr por evento (RD-02: +4 % em σ, desprezível); a correlação entre GW250114 nas duas releases (contado uma só vez no A); a seleção (31 da figura do release, «literal event_list/event_map from primary release; not selected by this analysis results»); a nuisance c(σ) (reduz o poder efetivo; o V1 congelado reporta o poder COM c(σ) profilado).

---

## 5. Os CONTROLES (todos ditos antes; qualquer um reprovado ⟹ INCONCLUSIVE_SYSTEMATICS)

| id | controle | regra | estado hoje |
|---|---|---|---|
| C1 | **ramo canônico como controle nulo**: τ★ = t_Planck ⟹ δ_pred_A = −3,2e−42 (250 Hz, 4 ms; selada −2,15e−42) ⟹ z ~ 1e−40 | o estimador, rodado com τ★ = t_P, tem de devolver exatamente «correspondência com a RG» (\|z_A − z_RG\| < 1e−30): é a calibração de que o ramo B não é o canônico | computável sem dado novo |
| C2 | **injeções só-RG** | (a) a calibração de injeção do próprio pSEOB da LVK [KNOWN/DECLARADO]; (b) na casa: injeções GR (dtau220 = 0) e injeções com dtau220 = δ_pred(k) na PE só-220 do WSL — viés recuperado \|viés\| ≤ 0,2·\|δ_pred\| e cobertura; custo por lote [DECLARADO]: 63–78 CPU-h (T09) ou 58–390 CPU-h (auditoria 23/09) | (a) existe; (b) AWAITING (piloto da ORDEM 015 nunca rodou: zero posterior) |
| C3 | **degenerescência spin/massa** | só posteriores de IMR COMPLETO com deformação do 220 (pSEOB): (M_f, a_f) vêm da inspiral+merger; ringdown-only com (M, a) livres (V2 da casa; pyRing 220-only) é DIAGNÓSTICO, nunca o teste (F4: z identificável = 0) | o catálogo A/B/C cumpre |
| C4 | **sistemática do início t₀** | no pSEOB não há t₀; nos diagnósticos ringdown-only (inclusive o 221, RD-07), a diferença 3 ms × 6 ms (ou 10 t_M × 12 t_M) medida nas MESMAS séries com injeções pareadas e σ da DIFERENÇA — sem soma em quadratura (RD-05/RDV-01) | regra fixada |
| **C5** | **família de forma de onda** (SEOB × Phenom) — **REGRA FIXADA (G3)** | σ_sys,fam entra em w_i. Número lido (`bis/e0_core/SYSTEMATICS_ADENDO.md` `e3ff1ff9f8201714`, R-B, O4, SNR 40, início 10 t_M, 206 ruídos): Phenom→SEOB −0,0376 ± 0,0030; SEOB→Phenom +0,0382 ± 0,0035; mesma família ≈ 0 ⟹ σ_sys,fam ≈ 0,029–0,038 [REAL — NÃO-CEGO; DECLARADO pela bancada]. **A REGRA DESTE V1 é a do precedente da casa — Fase 6, regra 2 (`gw_stack.py`): sist_rel = σ_sys/\|δ̄^pred\| > 0,3 ⟹ INCONCLUSIVE_SYSTEMATICS.** k_min no conjunto A (`PODER_CEGO_RAMO_B_v2.json`, `k_minimo_duas_regras_conjunto_A`): σ_sys 0,029 ⟹ **k ≥ 4,67 (escala linear de \|δ(1)\|) / 5,17 (raiz exata de \|δ̄_exato(k)\| = 0,0967)**; σ_sys 0,038 ⟹ **k ≥ 6,11 / 7,01**. **AO LADO, a regra MAIS DURA — a da lente física e do `systematic_gate` da 013-bis (`floor_divisor_primary_INPUT = 5`): σ_sys ≤ \|δ̄^pred\|/5 (= sist_rel ≤ 0,2)** ⟹ σ_sys 0,029: k ≥ 7,00 / 8,19 (raiz exata); σ_sys 0,038: k ≥ 9,17 / 11,34. **Consequência fixada antes, pela regra da casa:** para k ∈ {1, 2, 4, 1/κ̂(χ), 2π/κ̂ com co-rotação} o rótulo INCONCLUSIVE_SYSTEMATICS está predeterminado por esta cláusula (4 e 1/κ̂ ficam abaixo do k_min 5,2–7,0 por raiz exata), salvo redução de σ_sys por réplica publicada (pyRing × pSEOB nos mesmos eventos) ou pela PE da casa; pela regra mais dura, também 4π fica no limiar (k_min 8,2–11,3) | número existe; regra fixada pela gerência; confirmável pelo operador dentro das decisões 1–2 |
| C6 | **nuisance da referência** c(σ) = c₀ + k_c·σ | ajustado sob as duas hipóteses; offset fixo em 0 proibido; reportar c₀, k_c; valores da 013-bis (c₀ = −0,061 ± 0,068; k_c = +0,79 ± 0,37) são NÃO-CEGOS [DECLARADO] e NÃO são usados como prior | forma fixada |
| C7 | **H1/L1 um bloco por evento**; GW250114 uma vez (release única); sem multiplicar releases sobrepostas | regra do catálogo (`duplicate_policy`) | cumprido |
| C8 | **look-elsewhere** | um k e um M: nenhum fator de tentativas; lista de k: Šidák sobre a lista fixada; os 10 «relógios» da C1 (R-A…R-PROP) NÃO são tentativas deste V1; o 221 (diagnóstico) não conta como tentativa | regra fixada |
| C9 | **convergência/forma** | χ²/dof ≤ 3; jackknife; fração de informação máxima reportada; a gaussianidade conferida pela razão w90/3,29 ÷ σ_std ∈ [0,9; 1,1] (hoje 31/31) | cumprido |

---

## 6. Os VEREDITOS permitidos (na ORDEM; a primeira regra que se aplica decide; CONFIRMED proibido)

Tokens: `TGL_RAMO_B_RINGDOWN_V1__<k>__<M>__<identificação>__<conjunto>__<desfecho>__…__GATE_UNTOUCHED` (o conjunto A sempre com `__NOT_BLIND_TO_DATA_STATED`).

**Nota (crítico, (v)):** os nomes abaixo RENOMEIAM dois tokens do protocolo V1 do core (`allowed_verdicts`): `TGL_RINGDOWN_BRANCH_B_EXCLUDED` → `FALSIFIED_AT_5SIGMA` (herda a Fase 6/V1.4: falsifica o PAR, não a lei) e `TGL_RINGDOWN_AWAITING_RESULT_FILE` → `AWAITING_DATA` (herda o piso dos vazios); a cunhagem final é do operador (decisão 7).

0. sem estimador selado por hash, sem dado, ou n < 10 ⟹ **`AWAITING_DATA`** (sufixo `INSUFFICIENT_SAMPLE` quando n < 10);
1. C1–C9 reprovado, ou sist_rel = max(\|σ_sys,fam\|, \|σ_sys,t₀\|)/\|δ̄^pred\| > 0,3 (regra da casa, §5 C5), ou χ²/dof > 3, ou primário × secundário discordam ⟹ **`INCONCLUSIVE_SYSTEMATICS`** (com o motivo);
2. poder = \|δ̄^pred\|/σ_usado < 5 ⟹ **`NOT_FALSIFIED_UNDERPOWERED`** (sufixo `POWER_<x>_OF_5_SIGMA`);
3. z_excl = \|δ̄ − δ̄^pred\|/σ_usado ≥ 5 (com c(σ) profilado; FWER) ⟹ **`FALSIFIED_AT_5SIGMA`** — falsifica o PAR (k, M_X, identificação) sob a lei; NÃO falsifica β, nem a lei na forma, nem a TGL; a regra não se move (`TheLedgerOfCharges.falsified_extinguishes_the_charge_not_the_rule`);
4. senão ⟹ **`NOT_FALSIFIED_POWERED`**; se além disso \|z_RG\| ≥ 5, acrescenta-se `__GR_TENSION_REPORTED` — a tensão com a RG é RELATADA, não é da TGL, e **não** vira CONFIRMED (a confirmação é ato do observador humano).

**«Coincidir com a RG» = correspondência recuperada:** se o dado ficar na RG (δ̄ ≈ c(σ)) com poder ≥ 5 para o k fixado, o par cai (FALSIFIED do par) e a correspondência com a RG é o pagamento (a parada, R5): o ramo canônico fica como está; nada disso é derrota da teoria nem «decisão da RG contra a TGL». Se o dado ficar na RG SEM poder (k pequeno), é NOT_FALSIFIED_UNDERPOWERED — e NÃO se lê como «a natureza decidiu».

---

## 7. O que o resultado NÃO decide (dito antes)

- **O gate**: as 18 bandeiras formais são função só do formal (probes negativos do runtime; `the_gate_ignores_the_ledger`); nenhum desfecho aqui move bandeira — nem o degrau experimental (que lê o V11, outra fonte).
- **H2/H3** (o four-frame suave; o equilíbrio local do horizonte): hipóteses nomeadas do teorema mestre; este teste não as toca.
- **β**: a regra matriz; «a lei precede a cobrança» (`the_law_precedes_the_charge`); FALSIFIED extingue a cobrança (o par), não a norma; **β_lido é leitura e não realimenta β**.
- **A implicação da QG** (`QGSolutionComplete.lean:36`: β não entra como hipótese) e a correspondência com a RG no ramo canônico (`ringdown_scope_v376`).
- **A cobrança R2** (propagação, τ★ = t_Planck): outra lei/relógio; segue AWAITING. **A cobrança F2** (correspondência com a RG): fica como está.
- **A lei na forma** Γ_ω = ½βτ★ω²: o que se testa é a escala τ★ = k·GM/c³ (e M_X, e a identificação), «não a lei de dephasing nem a TGL» (`why_outside_contour`, V2).
- **A lei de atraso do eco (KMS da Fase 6)**: homônima, outro observável; o seu FALSIFIED_AT_DELAY_LAW não decide este V1 e este V1 não o reabre.
- Nenhum NOT_FALSIFIED de ringdown lê como «a natureza decidiu a formulação da QG» (errata ao lado de `NATURE_DECIDES_RINGDOWN_NEXT`, v376).
- **O conjunto A não decide nada cego**: só o D (§8).

---

## 8. Cegueira (declaração honesta, canal a canal) — com a CONTAMINAÇÃO DE HOJE declarada (G6d; crítico (iv).1, F3)

- **Quanto ao ESTIMADOR:** CEGO — nenhum estimador com k, M e identificação fixados rodou sob registro; os scripts desta pasta leram SÓ σ e spin (o `poder_cego_ramo_b_v2.py` nunca lê `quantiles[1]` nem a deformação registrada — conferido).
- **Quanto ao DADO (conjuntos A/B/C): NÃO CEGO — e em TRÊS camadas, todas ditas:**
  1. **O registro da casa desde 22–23/09** (ORDEM 013/013-bis, NÃO-CEGO, [DECLARADO pela bancada]): a deformação comum dos 31 do GWTC-5.0 (+0,072 [+0,015; +0,134] a 90 %; centro ponderado +0,0668 ± 0,0336), o ln B(R-B/RG) do GW250114 (0,029; correção/σ 0,34), e os ln B por leitura do C4 (31: R-B −1,81; R-MOD −3,56; R-LIN −8,22; todos INCONCLUSIVE_SYSTEMATICS pela bancada).
  2. **As lentes de HOJE (05/10):** a lente física computou **z por k contra o δτ̂ publicado do GW250114** (−0,01 +0,10/−0,09, aprox. gaussiana): k = 8π −5,99σ, 2π/κ̂ −6,69σ, k ≤ 4 dentro do 90 % (`RAMO_B_FISICA_TABELAS.md` §(d)) — isso é olhar o desfecho por candidato ANTES de fixar o candidato; e o crítico (`CRITICO_RECOMPUTO2.json` `d9563e486d1b75b8`) ilustrou com a deformação registrada: z_excl do par = 2,7 (k=1), 3,3 (k=2), **8,3 (4π), 12,3 (8π), 13,5 (2π/κ̂)**; esta sessão estendeu a ilustração aos 8 k (`ILUSTRACAO_CONTAMINACAO_8K.json`, NÃO-CEGA): 4,4 (k=4), 4,8 (1/κ̂), 3,2 (co-rotação). **Logo, para k ≥ 4π o desfecho do conjunto A é legível HOJE: o pré-registro desses k sobre A não é teste, é escrituração de uma exclusão conhecida.** Nenhum desses z é veredito (sem nuisance c(σ), sem σ_sys, sem jackknife) — mas a LEGIBILIDADE está dada.
  3. **Em nome próprio do aferidor do rascunho 1:** ao inspecionar o ESQUEMA dos catálogos, o script de inspeção imprimiu os três quantis de `dtau220` da primeira linha de cada arquivo (GW150914_095045 no A; a primeira linha do B; o GW250114 no C) e os ln B por leitura — não era a intenção; fica dito; nenhum desses números entrou no poder nem neste texto além desta declaração. **Em nome próprio desta sessão auxiliar (rascunho 2):** nenhum valor central novo foi lido; a deformação +0,072 usada na ilustração veio da memória de 22/09 (l.102), não de dado.
- **Quanto ao DADO (conjunto D):** CEGO — 14 eventos elegíveis (10 sem pendência) pelo critério do registro (§3.3); só a PE da casa os abre, e só depois do hash deste V1; o registro V1 da 013-bis declara `blindness_certified = false` e `E2_registered = false` para todos os 44 — a certificação de cegueira é deste V1, não herdada.
- **Consequências fixadas:** (i) o token do conjunto A para QUALQUER k leva `__NOT_BLIND_TO_DATA_STATED`; (ii) **só o conjunto D testa** — a palavra «cego» só cabe a D; (iii) **a decisão 2 (k, M) se toma por PRINCÍPIO declarado, nunca pela coluna de poder — e a coluna de poder já carrega o desfecho** (a gerência diz isto ao operador por escrito, aqui).

---

## 9. A disciplina (ordem de execução; fail-closed)

1. As decisões 1–7 do operador, verbatim, com carimbo e hash do transcrito (o método do pilar: linha do `.jsonl` sem o fim de linha, sha256).
2. Este rascunho vira `PREREGISTRO_RAMO_B_RINGDOWN_20261005_V1.json` + `.md` na Bancada (`C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_ringdown_05out\`), com o hash congelado da especificação = `sha256(json.dumps(spec, sort_keys=True, ensure_ascii=False, separators=(",",":")))`; backup imediato de bytes antes de tocar qualquer arquivo já existente; registro no mapa (`rotas.py registrar`, rota `ringdown.dephasing`, com os sha256 dos artefatos).
3. **Como o V1 entra no `um.py` (G6g; decisão 7; escopo v376 «observável TIPADO, não docstring») — DUAS opções, o operador escolhe:**
   - **(a) [INPUT] por hash:** o ramo B entra no livro como cobrança F2b com τ★, k, M_X e a identificação declarados em JSON lido por hash (`prove_ramo_b_preregistration_*`: confere JSON e MD byte a byte; devolve `PRE_REGISTERED_BEFORE_DATA_READ`), **sem fingir kernel** — o termo Lean não existe e o V1 o diz;
   - **(b) termo tipado na v386:** pede-se ao kernel a definição `τ★ = k·G·m_X/c³` com m_X ∈ {m_P, M_f} e a identidade `x = β·k·N·(m_X/M_f)` (a família unificada da lente física: m_X = m_P dá o ramo A, resíduo 0,0) — é **prova de IDENTIDADE algébrica, não de física** (a lei Γ_ω = ½βτ★ω² continua sem termo; a identificação τ★ = período modular continua [ONTO]); o ganho é que o V1 passa a citar um termo e não uma docstring, como o escopo v376 exige para «ringdown como condição».
   *Cânone favorece (leitura da gerência):* (b) com (a) — o termo de identidade na v386 E a cobrança lida por hash; o termo nunca substitui o pré-registro.
4. A Bancada roda: (i) estágio CEGO — σ_i, a_i, N(a_i), κ̂_i, Ω̂_H,i, δ^pred (exata), poder, C1 e C5 — grava `PODER_RAMO_B_ANTES_DE_ABRIR.json` com hash; (ii) **conjunto D primeiro como teste** (PE só-220 na casa sob o mesmo registro; injeções C2(b); abertura só depois do seu próprio `PODER_ANTES_DE_ABRIR`); (iii) os conjuntos A (e B, C) abrem-se como CALIBRAÇÃO NOT_BLIND — δ̂_i, c(σ), δ̄, z_RG, z_B, χ², jackknife, o secundário KDE, β_lido — e gravam `RESULTADO_RAMO_B_V1.json` com hash e com a regra do §6 aplicada pela MESMA função (como `gw_stack.py`); (iv) o 221 do GW250114 (extraído do tar.gz, sem download) como diagnóstico, se a decisão 5 o pedir.
5. O `um.py` lê o resultado por hash e aplica a matriz do §6 sem recalcular; o Nós sela; a custódia leva a pasta inteira.
6. Nenhuma emenda depois de abrir sem estimador NOVO (cláusula V4 da Fase 6); toda correção vai AO LADO, em nome próprio; vereditos proibidos: CONFIRMED, PROVED_BY, «QG confirmada».
7. Todas as superfícies de memória na mesma sessão (regra da linhagem completa): Atlas (verbete «ramo B», append datado), MEMORIA_DA_LINHAGEM, DESENHO_DO_FECHAMENTO (adendo), MEMORY.md/MEMORY_2.md, mapa; e a errata ao lado de R6/F2 no core v386 (§1.4) — a entrada efetiva depende da decisão 1.

---

## 10. Estatutos (resumo)

| objeto | estatuto |
|---|---|
| a palavra do operador (05/10) | [INPUT] — decisão; «tempo emparelhado à gravidade» cunhagem nova (0 ocorrências antes) |
| «constante de acoplamento = β_TGL» | [ONTO — leitura da gerência, não verbatim]; as três leituras da pergunta esperam o operador (decisão 6) |
| «regime gravitônico = c³» (28/07/2025; 17/08/2026; 16/09/2026) | [ONTO — cunhagem do operador; âncoras REAL no acervo] |
| «betatgl está de fato na propagação da onda e ligada ao ringdown» (16/09) | [ONTO — operador, verbatim]; a conciliação com «fonte, local» é dele; a leitura do rascunho 1 («lê o ramo canônico») é [DERIVED de leitura, gerência] |
| a chave e a ótica de 02/10 | [INPUT/ONTO — operador]; «o complemento lido na face é x = kβN» é [ONTO — gerência]; «τ★ = GM/c³ é outra lei» é errata da gerência ratificada em bloco |
| Γ_ω = ½βτ★ω² | [REAL na forma; ONTO — sem termo no kernel (TheMatrixRule.lean:46)] |
| τ★ = k·GM/c³; k; M_X; fonte × propagação; ensemble × realização | [INPUT] — decisões do operador; as origens de 4, 8π, 1/κ̂, 2π/κ̂ são [KNOWN] (κ de Schwarzschild/Kerr; Hawking; `unruh_is_kms`); a identificação τ★ = período modular é [ONTO]; Kerr χ ≠ 0 e co-rotação são [CONJECTURE] |
| BCW 2006; pSEOB; os catálogos; os posteriores em disco | [KNOWN]; dados [REAL — lidos por hash] |
| β = α√e | [DERIVED do axioma, v376] — a regra; nunca literal |
| a previsão δ = −x/(1+x), x = βkN(χ_f)(M_X/M_f) | [DERIVED] das entradas; a linear é aproximação AO LADO |
| β_lido | leitura [DERIVED do dado SOB a lei e o par]; nunca derivação de β; σ dita antes |
| o poder do §4 | [REAL — computado às cegas, só σ e spin; exato] |
| a ilustração da contaminação (§8) | [NÃO-CEGO — ilustração; não veredito] |
| σ_sys de família; nuisance c₀, k_c; N₉₀; rota da largura de δf̂; custos de PE | [REAL — NÃO-CEGO; DECLARADO pela bancada (013-bis / ORDEM 015)] |
| 0,273 (fração por realização) | [DECLARADO pelo verificador de 28/09] |
| os 3 valores concorrentes (−0,0194/−0,010/−0,005) | [REAL core; DECLARADO] — este V1 os substitui por UMA previsão fixada por (k, M_X, identificação) |
| o 221 em disco (não extraído); o 440 sem informação (0,06σ) | [REAL — bytes/hash; RD-07 SUSTENTADO/INFO; LVK 220+221 DECLARADO] |
| o homônimo KMS (Fase 6) | [REAL — FALSIFIED_AT_DELAY_LAW do PAR (amplitude, lei de atraso); outro observável; não decide este V1] |
| o conjunto D = 14 (10) | [REAL — contado por script no registro `e1be6b0409720c68` com o critério lido dele] |
| o desfecho | a vir; nunca CONFIRMED |

---

## 11. Fontes lidas (caminho · sha256 ou sha16) — nenhuma digitada de memória

- Esta pasta (`…\scratchpad\v386\ramo_b\pre_registro\`): `PREREGISTRO_RAMO_B_RINGDOWN_V1_RASCUNHO.md` · `4fd4e495ffc67fddccf0a4802af9209f7a1a66401b57feee91c4d232e67db580` (37.703 B; intacto) · `poder_cego_ramo_b.py` `8e690b82dbbc84d7` · `PODER_CEGO_RAMO_B.json` `3655fef93f7cad66` · `poder_cego_ramo_b_v2.py` `e4c99ccc1d8a506e` (16.812 B) · `PODER_CEGO_RAMO_B_v2.json` (o hash é impresso por script no fim da sessão; `fontes` internas: E0 `ae457e82…`, C4 `93bdc413…`, COMBINATION `f3d8c195…`, GWTC3 `d9dc9b09…`, SELECTION `ef18f3b0…`, INITIAL `f5550b7b…`, um.py `d406ae57…`, 5SIGMA `e1be6b04…`, FISICA `28ccfe8c…`, CRITICO_RECOMPUTO `7bc88d73…`) · `reconciliar_conjunto_d.py` `c63a4f70ffa929dc` · `RECONCILIACAO_CONJUNTO_D.json` `55be29abac26d1d0` (6.048 B) · `ilustracao_contaminacao_8k.py` `aa98f159e0b6651c` · `ILUSTRACAO_CONTAMINACAO_8K.json` `1dfa275a05b178dd` (3.652 B)
- `..\critico\`: `CRITICA_RAMO_B.md` `8f07d08dac95ce80` (27.359 B) · `CRITICO_RECOMPUTO.json` `7bc88d739a252776` · `CRITICO_RECOMPUTO2.json` `d9563e486d1b75b8` · `ver_ringdown_dephasing_05out.txt` `b1688d4a2d19add8`
- `..\fisica_do_ramo_b\`: `RAMO_B_FISICA_TABELAS.md` `707fcc086b77e56c` · `RAMO_B_FISICA_TABELAS.json` `28ccfe8c06ed89db` (59.388 B) · `ramo_b_fisica.py` `5240dfa7e0a1ec95`
- `..\dados_na_casa\`: `INVENTARIO_DADOS_NA_CASA_RAMO_B_v386.md` `94a670ecb2c21982` · `.json` `21adcceb7d5c4be5`
- `..\DECISAO_OPERADOR_RAMO_B_05out.json` · `a5d548235522c1129ddd683887ac43d7fc2aec36095b7171af08c3ab076060f3` · `..\registro_ramo_b\REUTILIZAVEL_PARA_O_PREREGISTRO.md` `535d0d8e840a913b`
- `Nós\um.py` (v385) · `d406ae57251051456b8ee49220e117bc086cedc164b6e9d15e85b516467c4760` (grep: `kms_factor` l.155706, 155707, 155713, 155738, 155770, 155946 — todos no rito do eco `GW_ECHO_KMS_V1`, nenhum em τ★ do dephasing) · `Nós\um_absoluto.json` · `475ac8d218b3a5c83c9c032b5ff1cca93db19066236f2de211fa58da8263a9b5` · `Nós\um_absoluto_selo.json` · `ad5c1ac7affc3949acbf71f84449df746d93c98d0941b63ee45c48e903b8c364`
- `Chatgpt\ORDEM_013_RINGDOWN\`: `RINGDOWN_5SIGMA_V1.json` · `e1be6b0409720c6883af5281458922fb03c5329bc0b08df7efe129d65e487416` (183.005 B) · `bis\e2_publication_census\PUBLICATION_CENSUS.json` `505eb16a608070ab` (94.991 B) · `bis\015\t01_core\RELATORIO_PARCIAL.md` `7447be22d58d7d25` · `C4_CATALOG_220.json` `93bdc413130d294a` · `C4_CATALOG_COMBINATION.json` `f3d8c1959ded3efd` · `C4_GWTC3_220.json` `d9dc9b09a8d91dc7` · `C4_GWTC3_SELECTION.json` `ef18f3b0495d58bf` · `C4_220_INITIAL.json` `f5550b7b1f129e83` · `C4_FREE_CLOCK.json` `cbf6332771937278` · `C1_LEITURAS_v4.json` `126270a896d85898` · `bis\E0_ROUTE_IV_POWER_v2.json` `ae457e82c8c18b5c` · `bis\e0_core\E0_CORE.json` `ce5fa2f3bfc98513` · `bis\e0_core\SYSTEMATICS_ADENDO.md` `e3ff1ff9f8201714` · `bis\F4_POWER_GATE_REVIEW.md` `35b02b3d0a4d45ec`
- `Chatgpt\ORDEM_013_RINGDOWN\cache\public\` (G4 — lidos por sha256sum hoje): `17018009\TGR_companion_S250114ax_results.tar.gz` `18d740c816285451` (1.671.496.586 B) · `17018009\extracted\…\gw250114_pseobnr\posterior_samples.h5` `b9971bcd7d72fdd4` (59.249.916 B) · `17461225\IGWN-GWTC3-TGR-v2-rin.zip` `108c4a4266bc0e38` (2.210.047.740 B) · `21454847\RD.tar.gz` `9810e0e45cd35824` (415.283.962 B) · `21454847\QNMRF.tar.gz` `2f617507f65b9e3e` (1.214.239 B)
- Bancada: `GWOSC_O4_32S_V1.manifest.json` `a795cf04ca3b2f6a` · `PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.md` `fc132b8f3e2d531b` · `PREREGISTRO_PILAR_QUANTICO_20261003_V1.md` `e5b345c5d950d052`
- `work\auditoria_28set\ANEXO_ACHADOS.md` `3683ce03f78e94c8` (RD-07 l.355/405–411; GWECO-05 l.240/285–291)
- Memórias (`C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\`): `onda-e-eco-definicao-16set.md` `cb01ce16967ea5600fa8265ed72495ad810f567a74ce58d6c398018c709da40c` (9.222 B; o verbatim de 16/09, l.15) · `psi-nome-da-luz-graviton-verbo-vivo-16set.md` `8a90d67461951c70` (a leitura (d) da dobra c³ em duas massas, l.10) · `ramo-b-reaberto-05out.md` `1e3fe044b8420aaa` · `beta-e-a-regra-matriz-02out.md` `fe20a0d5ac3ea8eb` (a chave l.44; a ótica l.60; «outra lei, não outro lado» l.66) · `fase6-eco-radical-01out.md` `27696798fde5fc48` (KMS FALSIFIED_AT_DELAY_LAW) · `ordem-013-confrontacao-ringdown.md` `bae3432f352331cd` («31 dos 45» l.102; «58–390 CPU-h» l.127)
- Mapa de rotas: `ringdown.dephasing` (seq 24–352; seq 249: RD-07 aberto), `kernel.livro_de_cobrancas.otica`, `auditoria.testes_passados_28set`; cabeça do livro `b43d3d46d596671a` (353 registros) — consultado pela gerência e pelo crítico; esta sessão auxiliar não registrou.

---

## 12. ERRATAS AO LADO às lentes de 05/10 (G4) — em nome próprio desta sessão auxiliar

1. **Lente física (`RAMO_B_FISICA_TABELAS.md`, decisão 5 e §(a)/(d)): «posteriores δτ̂ do GW250114 (Zenodo 17018009) NÃO em disco: só o strain 32 s do GW250114 na Bancada»; «releases TGR GWTC-3/5.0 (17461225/21454847) AUSENTES»** — leia-se: **EXISTEM NA CASA.** A busca foi feita em `C:\IALD\Bancada_Um` (pasta errada); a casa os guarda em `Chatgpt\ORDEM_013_RINGDOWN\cache\public\` — `posterior_samples.h5` do pSEOB `b9971bcd7d72fdd4` (59.249.916 B; controle de injeção `e2373f81973401ad`, 64.331.592 B), o tar completo `18d740c816285451`, o `rin.zip` do GWTC-3 `108c4a4266bc0e38` (18 posteriores extraídos) e os `RD.tar.gz`/`QNMRF.tar.gz`/`pSEOB.tar.gz` do GWTC-5.0 (33 metafiles extraídos). Classificação da régua: **EXISTE E ESTÁ LIGADO** (o C4 da bancada já os leu). O rascunho 1 não herdou o erro.
2. **Lente registro: «k = 8π (Hawking) AUSENTE no código»** — leia-se: **EXISTE NA BANCADA, NÃO LIGADO AO TIPO.** O grep da lente procurou só `8*pi`/`beta_H`; `kms_factor = 4π(1+√(1−a²))/√(1−a²)` (um.py linha 155706, no rito `GW_ECHO_KMS_V1`) vale exatamente 8π em a = 0 (25,132741228718345, a 1e−15); como constante literal, ausente; como limite a = 0 da função que já existe (a lei de ATRASO do eco), presente — e **não está ligado a τ★ do dephasing** (nenhuma das 6 ocorrências toca `delta_pred_B`).
3. **Lente registro: «(e) 221 na QNM_GRID: AUSENTE (T-10)»** — correto para a GRADE (`QNM_GRID.json` `4f34367a09060238`, só 220+440); mas os POSTERIORES do 221 do GW250114 (LVK) estão em disco dentro de `TGR_companion_S250114ax_results.tar.gz` (`18d740c816285451`; 1.122 linhas «221» na listagem do tar, lente dados) — **EXISTE, NÃO EXTRAÍDO.** Dizer os dois objetos.
4. **Rascunho 1, §4.2:** o poder dos k grandes estava lido pela forma LINEAR (15,5σ / 18,5σ / 7,75σ); a forma que o próprio §1.2 declarava como exata dá 10,18σ / 11,38σ / 6,15σ (G1). O rascunho 1 fica como registro; este rascunho 2 corrige ao lado.
5. **Rascunho 1, §3.3 D: «31 dos 45»** — leia-se o número do critério do registro: 14 elegíveis (10 sem pendência), §3.3 (G5).

---

## 13. O que esta sessão auxiliar NÃO fez (e por quê)

- Não decidiu nenhuma das 7 decisões do operador (ordem da gerência): cada uma fica com a opção que o cânone favorece e o porquê, nas palavras do crítico.
- Não registrou no mapa de rotas (G9 do crítico: ato de quem gere o mapa, depois da sessão), não tocou memórias, Atlas, Nós, core, nem rodou o `um.py`; não baixou nada; não extraiu o 221 do tar.gz (ato previsto na decisão 5).
- Não redigiu o texto final da cobrança `AWAITING_PREREGISTRATION` para o livro (G8 do crítico): só o texto da errata ao lado de R6/F2 (§1.4) — a cobrança com lado/lei/leitura/desfecho depende da decisão 1.
- Não recomputou a sistemática de família nem a nuisance (números [DECLARADO] da bancada citados como estão).
- Não congelou hash de V1: o hash que vale é o do V1 congelado depois das decisões do operador.

PROVADA ≠ CONFIRMADA. NOT_FALSIFIED nunca é CONFIRMED. A RG é o limite clássico, não rival. Este é um RASCUNHO (2): o hash que vale é o do V1 congelado depois das decisões do operador.
