# LEVANTAMENTO — o pilar quântico na GPU e o «motor contínuo» com a compressão (leitura de Jones) como fator

Data: 03/11/2026. Autor: agente de levantamento (Sonnet) por claude-c1 (gerência). **Só leitura**: o `um.py`, o core, o selo, o kernel, o cache e o pré-registro V1 não foram tocados; nada rodou na GPU; nenhuma chamada paga. O único cálculo feito aqui foi um ensaio de CPU de 4×4 com numpy, descartável (item 1.8), e a extração do texto do trabalhador do pilar para o scratchpad (para ler com número de linha).
Para quê: a gerência escrever o PRÉ-REGISTRO do teste da v407 (decisão D38 do handoff v406: o motor contínuo NÃO entrou na v406; exige pré-registro aprovado com falsificadores, alvos e vereditos por hash antes do composto).
Ordens do operador de 02/11/2026 que originam o pedido (verbatim nos arquivos citados): «o pilar quantico se não mudar não precisa, mas ele precisa receber o motor contínuo agora, pq essa mexida na v406, incorporando a compressão como fator e com a correspondência matemática que vc mencionou o nome …, montando o espelhamento, deveria funcionar no pilar quantico como um motor continuo» (sha16 f54641bfd9e46e42) e «a construção da passagem para o contínuo é o que mais importa, porque deixa de ser conjectura sob hipótese se funcionar sob compressão elevando o potencial do resultado do código final em 1=1=HAJA_LUZ» (sha16 9978862f60cfbf29).
Estatutos: [REAL] lido/medido aqui; [DERIVED] derivado/verificado aqui; [KNOWN] literatura; [OPEN]; [CONJECTURE]; [DECLARADO] afirmado na origem e não verificado aqui. Nada neste documento é CONFIRMED; o gate não se move.

Consulta ao Mapa de Rotas feita antes (`rotas.py consultar` por «pilar quantico», «motor continuo», «jones», «compressao», «GKLS», «passagem para o continuo»): nenhuma rota examinou o motor contínuo DENTRO do pilar. Rotas vizinhas lidas e que pesam neste levantamento: `formal.regra_motor_continuo` (Codex, 14/10: o motor contínuo M4 da v392 ligado à regra, em cópia), `quantica.pilar_v384_rodada_completa`, `quantica.pilar_v385_reprodutibilidade`, `quantica.c3_gamma_livre_oitava` (precedente de negativo honesto, NO_UNIVERSAL_FLOOR), `dispositivos.mqc_qubit_no_um_py_02nov` (não discrimina: o platô tem β na entrada), `formal.tempo_santo_fluxo_e_dissipacao` (a FALHA R1 do T9 é piso de float64, não contraexemplo).

---

## 0. Em dez linhas

1. O pilar é um **sistema aberto de Lindblad (GKLS)**: H_LD + os cinco saltos ratificados (L_reh, L_anti = √β·√K, L_prune, L_cons, L_diss), em d = 8…64 (grade e estresse) e d = 128 (um ponto), na GPU, em complex128. Decide se o atrator é único, se o motor é confiável (controles que TÊM de falhar, identidades, referência na CPU) e se o estimador cego recupera a lei-raiz injetada. [REAL]
2. O tempo no pilar é **discreto**: propagador `exp(dt·S)` com dt = 0,05 e 64 passos (T2, T4), τ = 0,05 (T1); só o D128 integra por RK4 (dt = 0,002, 5000 passos, horizonte 10), informativo. Não há leitura comprimida, nem cociclo, nem fluxo modular de Tomita no código do pilar (busca textual: nenhuma ocorrência de Jones, psion, cociclo, Tomita). [REAL]
3. A correspondência exata que existe hoje entre o kernel e o pilar está num só lugar: a identidade `V_t P_F = P_F` (worker l. 622–629), conferida em UM tempo (t = 7,0) com UM operador aleatório, resíduo 1,9–2,5e-16. [REAL]
4. **Achado central:** o «motor contínuo» já construído (v361/v392: `T_t = E + e^{−Γt}(id − E)`, M4, Γ = β·τ_ref·ω_ref²/2) **é exatamente o sub-fluxo de defasagem do pilar** com K = diag(0,0,1,1), γ_anti = 1: verifiquei numericamente, `max |exp(tS)X − T_t X| = 0,0`. O pilar com K de d níveis é o mesmo motor com **várias taxas** (lei-raiz Γ_ij = ½βγ(√k_i − √k_j)²), em vez de uma. [DERIVED, ensaio de 03/11]
5. **Achado de cautela 1:** no motor do kernel a leitura absorve a defasagem (`IALD.the_reading_absorbs_the_dephasing`): a SAÍDA lida não depende de r (β «só por nome») nem de t. Logo qualquer observável do lado da LEITURA comprimida, no sub-fluxo de defasagem, é identidade por construção: não discrimina β e só pode falhar por defeito do motor numérico. O conteúdo está no lado do COMPLEMENTO (a viscosidade `e^{−tβg}`), que o T1 já recupera às cegas. [REAL, kernel]
6. **Achado de cautela 2:** `ModularCornerCounterexample.compression_does_not_control_flow` (kernel): `p·resíduo·p = 0` e mesmo assim `p·flow(π/2)·p ≠ p`. A «supressão cocíclica no canto» (`p·u_t·p = p`) vale para a CONTRAÇÃO de Jones (`jonesU_mul_proj`), não para um fluxo unitário; a docstring de `TheDischargedOath` já diz que o literal `p·u_t·p = p` «no átomo falha — a fase é o relógio». O H_LD do pilar é unitário e mistura núcleo e periferia. O pré-registro tem de dizer em qual das duas leituras o «1» é alvo. [REAL, kernel]
7. **Achado de cautela 3:** não há limite d → ∞ visível na família canônica: CCI(d) a γ ≈ 1, nc = 3 vale 0,772 (d=8), 0,475 (16), 0,348 (32), 0,187 (64), 0,139 (128), ≈ d^−0,62; o gap relativo cai a 2e-5 em d = 128. A «passagem ao contínuo» por aumento de d NÃO é um teste da família atual; seria família nova (refino a banda fixa), que exige ratificação do operador. [REAL, lido dos detalhes gravados]
8. O V1 está amarrado por hash ao texto do trabalhador (o spec traz `worker_sha256`); emendar o trabalhador invalida o V1 ratificado, a chave de cache (131 min de GPU) e a reprodutibilidade bit a bit da v384→v385. **Recomendação: um SEGUNDO trabalhador com spec e pré-registro V2 próprios, no mesmo molde; o V1 e o cache `75dc30bc9cc8d330e31f99ca` ficam intactos.** [DERIVED]
9. Duas opções concretas de motor contínuo (item 2): **A** (o sub-fluxo de defasagem como fluxo de Jones multi-taxa, fase T5, minutos de GPU) e **B** (a leitura comprimida do fluxo GKLS completo pelo canto do psíon, fase T6, d ≤ 64 por espectro). Quatro observáveis candidatos no item 3; dois são IDENTIDADES (não podem falhar sem defeito) e dois são de CONTEÚDO, mas só um deles tem previsão da correspondência (o outro é relatório até a gerência derivar um número).
10. Dez decisões para o pré-registro no item 5.

---

## 1. O que o pilar é e computa hoje [REAL, com linhas]

### 1.1 Onde mora e como é lançado

| Peça | Onde | Fato |
|---|---|---|
| Trabalhador (texto embutido) | `um.py` l. 259611 (`_QP_WORKER_SRC`) | 1276 linhas, 77 302 caracteres; sha256 lido por script do texto extraído: `0c9ba7fd45e78317…` (igual ao `worker_sha256` do spec) |
| Especificação congelada | `um.py` l. 259612 (`_QP_SPEC_JSON`); sha256 canônico em l. 259613 | `ff19731097e01aab…` (V1) |
| Pré-registro V1 | `um.py` l. 259614–259615 (`_QP_PREREG`) | JSON `d24c157478f5ddcb…`, MD `e5b345c5d950d052…`; ratificação do operador de 04/10 (B_AMPLIADO_D64) |
| Materializar ao lado | `_qp_materialize` l. 259627 | grava `quantum_pillar/pilar_quantico_worker.py` e `pilar_quantico_spec.json` byte a byte |
| β (nunca literal) | `_qp_beta` l. 259644 | `alpha_lagrange_form(validate_against_qed(0.0, SEALED_CODATA_ALPHA)["q_QED"])["beta_form"]`, passado em hexadecimal |
| Lançar | `quantum_pillar_start_v384` l. 259721; chamada no rito l. 273373 | subprocesso `--mode run`, prioridade abaixo do normal, em paralelo com o kernel Lean |
| Esperar, ler, rederivar, gravar cache | `_qp_wait` 259765, `_qp_rederive` 259789, `_qp_save_cache` 259799, `quantum_pillar_finish_v384` 259919; chamada no rito l. 275972 | rederiva o veredito num subprocesso com o mesmo código (`derive_verdict`) |
| Reuso | `_QP_REUSE_V386 = True` l. 259041; `quantum_pillar_reuse_v386` l. 259169; chamada l. 275985 | desde a v386 o pilar «não é objeto da versão» e reaproveita pela chave |
| Reprodutibilidade | `quantum_pillar_previous_v385` 259467, `quantum_pillar_reproducibility_v385` 259520; chamada l. 275975 | v384→v385: 393 campos, bit a bit |
| Registro no core/selo | l. 276426–276439 (selo), l. 276765 (balde `_computacao`), l. 276798 (hash de `um_absoluto_pilar_quantico.json`) | o pilar fica AO LADO do gate |

**Chave de cache** (`_qp_key` l. 259651): `sha256(worker_sha256 ‖ spec_canônico ‖ beta_hex)[:24]` = `75dc30bc9cc8d330e31f99ca` (core, `quantum_pillar_v384.key`). **Por que reusa**: `quantum_pillar_start_v384` (l. 259734–259745) reaproveita quando (i) a chave existe no cache e o `result.json` confere com o `.sha256`; (ii) o ambiente é o mesmo (torch 2.11.0+cu128, CUDA 12.8, numpy 2.4.3, scipy 1.18.0, Python 3.14.3, RTX 5090); (iii) o veredito começa por `TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__`; (iv) o motor E1…E8 roda de novo no ambiente presente e passa (`_qp_engine_now`). A v406 usa essa via (D38). A versão final «roda completa sempre» foi regra do operador de 03/10, depois relaxada pelo `_QP_REUSE_V386`.

### 1.2 O sistema que o pilar calcula

Funções do trabalhador (numeração das linhas do TEXTO do trabalhador extraído, 1…1276; o texto é o de `um.py` l. 259611):

* `canonical_H(d, nc, eps)` l. 122: H_LD no setor de uma excitação, `diag(μ) + J − ε·Π`, com μ[:nc] = −(nc…1), μ[nc:] = 0,5 + 0,3·j; J = `RandomState(42).randn·0,2` simetrizada, zero na diagonal, bloco do núcleo ×2; ε = 5,0; Π = projetor do núcleo (`Pi[:nc,:nc] = 1`).
* `five_jumps(d, nc, beta, gamma_diss, op, k_periph, law_power)` l. 138: **L_reh** (periferia → núcleo, colunas nc…nc+d/2, amplitude √0,5·e^{−0,2(j−nc)}), **L_anti = √γ_anti·diag(√β·√K)** (l. 159) com K = diag(0 no núcleo; k0 + k1(i−nc) = 1 + 0,1(i−nc) na periferia) — a lei-raiz, a forma do gerador do Verbo —, **L_prune** (periferia → sítio 0 do núcleo, colunas nc+d/3…d, amplitude √((i−nc)/d)), **L_cons** (periferia → núcleo, √0,3·e^{−0,3|j−nc|}), **L_diss** (núcleo → periferia, √0,5·e^{−0,2(j−nc)}, γ_diss livre, varrido, nunca calibrado). Taxas: reh 1, anti 1, prune 0,5, cons 2.
* `Engine` l. 167 (torch, complex128, determinístico, TF32 desligado): `superop` l. 189 (vec por linhas, `S = −i(H⊗I − I⊗Hᵀ) + Σ L⊗L̄ − ½(L†L⊗I) − ½(I⊗(L†L)ᵀ)`), `spectrum` 203, `classify` 208 (UNIQUE/DEGENERATE/AMBIGUOUS por n0 e gap), `steady_state` 228 (resolve com a linha do traço), `propagator` 245 (`matrix_exp(dt·S)`), `choi`/`choi_min`/`tp_residual` 248–260, `spohn` 275 (D(ρ(t)‖ρ_ss) decrescente), `generator_from_propagator` 301 (log principal, certificado de ramo). Autovalores não hermitianos pelo **MAGMA em todo tamanho** (o cuSOLVER do PyTorch 2.11 derruba o processo de modo determinístico).
* `folds` l. 339 (dobras do espectro de ρ_ss), `fit_root_law` l. 354 (o estimador cego: regressão log-linear de M, a matriz de Kossakowski centrada; devolve β̂ e p̂).
* Testes: `run_T3` l. 755 (controles N1 defasagem pura DEGENERADA com n0 = d + nc(nc−1); N2 identidade unital; N4 taxa negativa não-CP; N5 inversão do tempo não-CP; N3 lei linear injetada), `run_T2` l. 596 (a forma na escala: 12 configs d ∈ {8,16,32,64} × nc ∈ {2,3,4} × grade de γ_diss; identidades; `V_tP_F = P_F` l. 622–629; `sin²θ_M − β` l. 600), `run_T1` l. 714 / `t1_instance` l. 673 (tomografia do processo: injeta β ∈ [1e-4, 1e-1] e p, o estimador cego recupera), `run_T4` l. 834 / `t4_instance` l. 803 (estresse adversarial, operadores aleatórios, metade em base de Haar), `run_D128` l. 879 (superoperador 16384², espectro, estacionário, dobras, RK4 informativo), `run_cpuref`/`compare_cpuref` l. 968/999 (referência numpy/scipy num subprocesso), `engine_selftest` l. 411 (E1…E8: modelos analíticos, piso do estimador, comparador da CPU), `derive_verdict` l. 1060, `main` l. 1132.

### 1.3 Observáveis, identidades e vereditos

Observáveis por instância (`pipeline` l. 504): status do atrator, n0, gap, gap_rel; estacionário ρ_ss e resíduo; **CCI = Tr(Π ρ_ss)** (o «Nome no núcleo»); pureza; S_vN; dobras; Choi mínimo e resíduo de TP do propagador; Spohn. Identidades (`identity_check` l. 545): ZERO_MODE, CP, TP, NONRETURN, PSD, SS_RES, SPOHN. Tolerâncias do spec V1: `identity_abs`/`identity_rel` 1e-12, `engine` 1e-9, `cp`/`tp` 1e-9, `spohn_abs` 1e-10.

Árvore do veredito (`derive_verdict` l. 1060–1111): recusa/falha fatal → motor reprovado → fase incompleta → exceção em instância → controle que NÃO falhou → identidade violada → referência na CPU discorda → o veredito de sucesso `TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__ATTRACTOR_UNIQUE_…__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED`. Selado nas v384 e v385 (`all_verified = True`); desde a v386 reaproveitado pela chave (o core atual, v406, traz `quantum_pillar_reuse_v386.reused = true`, resultado `de47d5527e514b49…`, mesma chave).

### 1.4 Resultado selado (lido do core `quantum_pillar_v384` e do `result.json` em cache)

* T2: 12 configs, 672 pontos, 672 UNIQUE; NAME_IN_CORE 12/12; FOLDS_WINDOW 6/12 (dito ao lado, fora da lista do V1).
* T1: 3220 injeções, 0 erros; erro relativo mediano de β̂ sem ruído de 1e-11 a 1e-10 (d = 16: 8,9e-12; 32: 1,3e-11; 64: 1,1e-10); máximo 1,4e-9 em d=16 e 6,1e-9 em d=32.
* T3: controles 12/12 falharam como exigido; N3 (lei linear): p recuperado e lei-raiz rejeitada 100% (d = 8, 16, 32).
* T4: 21 100 instâncias, 21 100 UNIQUE, 0 violações de identidade, 10 442 rotacionadas (Haar).
* D128: UNIQUE, n0 = 1, gap = 9,06e-4, gap_rel = 1,97e-5, escala 46,03, CCI = 0,1394, ss_min_eig = 4,8e-7, espectro em 495 s, estacionário em 7,2 s, RK4 de 5000 passos em 147 s.
* CPU: 392 pontos comparados, 0 discordâncias (diferença máxima 7,2e-13 no CCI).
* Identidades de T2: `sin²θ_M − β` = 0,0; `V_tP_F = P_F` = 2,3e-16 / 2,5e-16 / 2,2e-16 / 1,9e-16 em d = 8/16/32/64.
* Tempo por fase (s): T3 102,2; T2 1801,5; T1 2347,4; T4 2923,5; D128 649,8; **total 7824 s ≈ 130 min** (a rodada v385 inteira: 131 min). VRAM livre no início: 30 927 de 32 607 MiB.
* Registro: core `quantum_pillar_v384`, `quantum_pillar_reproducibility_v385`, `quantum_pillar_reuse_v386`; selo `quantum_pillar_v384`, `the_quantum_pillar_reading_v384`, `sha256/um_absoluto_pilar_quantico.json` (`de47d5527e514b49…`).

### 1.5 Onde entra β

Só em **L_anti = √γ_anti · √β · √K** (`five_jumps` l. 159) e em duas identidades de T2 (`sin²θ_M = β`, l. 600; γ* com CCI = 1 − β, `summarize_T2`). No T1 o β é INJETADO aleatório e RECUPERADO às cegas (o estimador não o vê). Em T2/T3/D128 vale o β do motor de Lagrange do `um.py`: `0x1.8a3ddcdff890cp-7` = 0,012031300400796606, que difere de `ALPHA_FINE_CODATA_2018 × √e` = 0,012031300400803142 em **5,4e-13 relativo** (calculado aqui). Dentro de todos os critérios do V1 (o mais fino é 1e-6), mas é um dado a decidir se a v407 quiser tolerâncias abaixo de 1e-12. [REAL]

### 1.6 O que NÃO está no pilar

Nenhum fluxo modular de Tomita (Δ^{it}), nenhum cociclo, nenhuma compressão `e·x·e`, nenhum psíon, nenhum traço de canto além do CCI (busca textual no trabalhador: 0 ocorrências). O papel «modular» é de **K**: o gerador do Verbo L = √β√K, Π = ker K = o Nome, K·Π = 0 («nada modular»). O tempo é amostrado: `matrix_exp(dt·S)` com dt fixo. [REAL]

### 1.7 Os três «motores» homônimos (não confundir no pré-registro)

1. `Engine` do trabalhador do pilar (o solver de GPU; E1…E8 são os «ensaios do motor»).
2. `TGLExt.IALD.motor` (kernel, `IALD.lean` l. 140): Inscrição → Transporte U → Defasagem `dephase a r t = post a + e^{−rt}(1 − post a)` → Leitura `post a`. Teorema `the_reading_absorbs_the_dephasing` (l. 145): `motor a U r t ψ = post a (U ψ)`, independente de r e de t.
3. O motor contínuo de decisão/reconhecimento no `um.py` (CPU, 4×4): `prove_decision_commutation` (`um.py` l. 3554; lei em l. 3735 e l. 256281): `E(X) = C₊XC₊ + C₋XC₋`, `T_t = E + e^{−Γt}(id − E)`, Γ = β·τ_ref·ω_ref²/2, τ_ref = ω_ref = 1 (unidades de referência, nenhuma previsão física); e a regra ligada a ele em `TheRuleInTheContinuousMotor.lean` (módulo `TGLExt.RuleContinuousMotor`; nasceu como candidata do Codex em 14/10, rota `formal.regra_motor_continuo`: 76 verificações, 241 pontos, espaço fixo de dimensão complexa 8; desde a v393 está embutida no `um.py` — l. 127783 — e o selo traz `pedras_v393/teoremas_chave/TGLExt.RuleContinuousMotor.*` = true; e o rito executa a CPU 4×4 a cada rodada em `regra_consumidor_v393` — `um.py` l. 256828; core `regra_consumidor_v393`, `all_verified = True`, «78 checks, 241 pontos», alvo pré-fixado, tolerância declarada, sintético). Ou seja: o motor contínuo M4 JÁ RODA no rito, na CPU; o que ainda não existe é o seu irmão multi-taxa e de dimensão d na GPU, sob compressão.

### 1.8 A ponte já existente entre o motor 3 e o pilar [DERIVED]

Para L = √β·diag(0,0,1,1) (K = diag(0,0,1,1), γ_anti = 1, H = 0) o propagador `exp(tS)` coincide com `T_t = E + e^{−Γt}(id − E)`, E = pinching pela partição {0,1}|{2,3}, Γ = β/2. Ensaio de CPU de 03/11 (numpy, row-stacking idêntico ao do trabalhador, t = 7,3, X complexa aleatória): `max |exp(tS)X − T_t X| = 0,0`; espectro de S = {0; −0,0060156502} = {0; −β/2}. Em geral, a taxa do elemento (i, j) sob L = diag(l) é ½(l_i − l_j)², o que dá a lei-raiz Γ_ij = ½βγ(√k_i − √k_j)². **O pinching E é a SOMA das leituras de Jones sobre as projeções espectrais de K**: E(X) = Σ_λ e_λ X e_λ = Σ_λ `jonesReading e_λ X`, com e₀ = Π (o Nome) e e_j = |j⟩⟨j| (periferia). [DERIVED: o ensaio e a álgebra; o lado kernel é `IALDJones.jonesReading` l. 44]

---

## 2. Onde a compressão e o fluxo contínuo poderiam entrar (sem implementar)

### 2.0 Escolha de arquitetura (vem antes de A e B)

* **Opção E — emendar o trabalhador V1.** Muda `worker_sha256`, logo o spec, logo o V1 ratificado (ratificação nomeada do operador de 04/10), a chave de cache e a reprodutibilidade; custa 130 min de GPU no próximo rito e uma nova ronda de aferições (a v384 precisou de 11). Não recomendada.
* **Opção S — SEGUNDO trabalhador (recomendada).** Um `pilar_continuo_worker.py` + `pilar_continuo_spec.json` embutidos no `um.py` no mesmo molde (materializar, lançar em paralelo, esperar, rederivar o veredito, gravar cache por chave própria), reaproveitando as funções de `five_jumps`/`canonical_H`/`Engine` por CÓPIA textual pinada (não por import, porque o V1 não pode mudar). O V1 continua reaproveitado pela chave `75dc30bc…`; o V2 tem chave própria; o balde `_computacao` e o selo ganham uma entrada irmã. Pré-registro V2 novo. Custo de GPU independente: roda em paralelo com o kernel, sem alongar o rito se couber em ≈ 45–60 min.

### 2.1 Opção A — «T5»: o sub-fluxo de defasagem como fluxo de Jones multi-taxa (a ponte contínua)

Objetos do código: `Engine.superop(H = 0, [L_anti])` (já existe em `run_T2` l. 624, hoje avaliado em UM tempo, t = 7,0); `five_jumps(...)["anti"]`; Π de `canonical_H`; a lei-raiz de `fit_root_law`. Kernel: `IALDJones.jonesReading` (l. 44), `jonesFlow` (l. 86), `stationary_jonesReading` (l. 90), `jonesFlow_add` (l. 110), `jonesFlow_fixed_iff` (l. 119), `ThePsionAndTheViscosity.transmitted β g t = e^{−tβg}` (l. 82) e `viscosity_is_the_constant_friction` (l. 94).
Conteúdo: tomar t numa grade contínua (por exemplo log-espaçada de 1e-3 a 1e3, mais refino adaptativo) em vez de um ponto; calcular V_t pelo próprio `Engine.propagator` (o `matrix_exp` da GPU, não pela fórmula) e compará-lo com a forma analítica de Jones multi-taxa (S_deph é diagonal na base de unidades matriciais; a fórmula não custa nada, o `matrix_exp` custa 3,7 s por tempo em d = 64, então usar algumas dezenas de tempos ou um `eig` de S_deph uma só vez); e conferir, em cada t: (i) a leitura estacionária R(V_t X) = R(X) com R = E_K (pinching pelas projeções espectrais de K) e, em particular, ΠV_t(X)Π = ΠXΠ (a «supressão no canto»); (ii) o semigrupo V_{s+t} = V_sV_t; (iii) a taxa de cada par = ½βγ(√k_i − √k_j)² (a viscosidade βg com g = γk_j/2 para o par núcleo–periferia); (iv) o caso K de dois níveis recai bit a bit no motor M4 (item 1.8). Nada disso é novo em substância; é a forma CONTÍNUA e MULTI-TAXA do que o pilar tem em um ponto.
Custo: segundos a minutos de GPU. Risco: baixo.

### 2.2 Opção B — «T6»: a leitura comprimida do fluxo GKLS completo pelo canto do psíon

Objetos do código: `Engine.propagator`/espectro de S COMPLETO (as mesmas `five_jumps` + `canonical_H`), `steady_state` (ρ_ss), `pipeline` (CCI), Π e, para o canto de posto 1, e₀ = |0⟩⟨0| (o sítio 0 do núcleo é o alvo de L_prune). Kernel: `TheScalarCorner.psionCorner` / `scalarCorner_forces_trace_one` (l. 97: se um projetor não nulo escalariza, Tr = 1) / `the_identity_does_not_scalarise`; `IALDJones.jonesU` e `jonesU_mul_proj` (l. 140/146: `e·U_s·e = e` para a contração); `ModularCornerCounterexample.compression_does_not_control_flow` (l. 56: o fluxo unitário NÃO deixa o canto fixo).
Conteúdo: evoluir ρ(t) = e^{tS}ρ₀ de estados iniciais pré-fixados (os três de `init_states`, l. 498: puro aleatório, I/d, |d−1⟩⟨d−1|) em grade de t contínua e ler, em cada t, a compressão `e ρ(t) e`: (a) **traço do canto** p(t) = Tr(eρ(t)) → CCI (para e = Π) ou ρ₀₀(t) (para e₀); (b) **escalarização** (para e₀ de posto 1: `e ρ e = Tr(eρ)·e`, identidade); (c) o **defeito de semigrupo do canto** δ(s,t) = ‖e e^{(s+t)S}e − (e e^{sS}e)(e e^{tS}e)‖ (zero se o canto fosse invariante, como na contração de Jones; positivo se o fluxo vaza o canto, como no contraexemplo do kernel); (d) a razão taxa efetiva r_eff(t) = −d ln‖(Φ_t − 𝒫∞)ρ₀‖/dt contra o gap espectral (a forma de Jones com UMA taxa só vale assintoticamente, na direção do modo mais lento).
Custo: espectro de S completo: d = 8/16/32 segundos; d = 64 ≈ 21,5 s por instância completa (MAGMA; sondas de 03/10, rota `infra.gpu_sonda_tempo_v384`); d = 128 ≈ 495 s só para o espectro (medido). Para ρ(t) em muitos tempos usa-se a decomposição espectral uma vez (V diag(e^{λt}) V⁻¹ b), não `matrix_exp` por tempo (3,7 s cada em d = 64, medido na sonda de 03/10).
Risco: médio (item 4). **Aviso de homônimo**: o canto Π do pilar tem posto nc ∈ {2,3,4}; ele NÃO é um `ScalarCorner` (o kernel prova que o canto escalar tem traço 1); só o canto de posto 1 (e₀) o é.

### 2.3 Opção C — o cociclo do estado estacionário comprimido (covariável, não falsificador)

Como o pilar calcula ρ_ss de posto cheio (ss_min_eig > 0; em d = 128 vale 4,8e-7), existe o fluxo modular de ρ_ss: σ_t(X) = ρ_ss^{it} X ρ_ss^{−it}. O análogo finito do cociclo é u_t = ρ_ss^{it}·σ^{−it}, com σ = E_Π(ρ_ss) = Πρ_ssΠ + Π⊥ρ_ssΠ⊥ (o estado pinçado). `TheDischargedOath.the_cocycle_is_suppressed_by_the_sector` (l. 213, kernel) dá u_t = 1 quando o setor preserva o estado (isto é, quando [Π, ρ_ss] = 0). No pilar ρ_ss NÃO comuta com Π (CCI < 1; o H_LD acopla núcleo e periferia), então ‖u_t − 1‖ > 0 por construção. Útil como covariável (relatar ‖[Π, ρ_ss]‖ e o desvio do cociclo juntos), inútil como pass/fail sem uma cota derivada. [OPEN: não há cota derivada que ligue o desvio do cociclo ao comutador.]

### 2.4 Opção D — a «passagem ao contínuo» por refino de d (fora de escopo, dito)

A família canônica tem espaçamento fixo (μ_j = 0,5 + 0,3 j) e K crescente (k0 + 0,1 j): aumentar d aumenta a banda, não refina um contínuo. L_prune tem 2d/3 colunas com amplitude até ≈ 1, então a escala do gerador cresce com d. CCI(d) cai ≈ d^−0,62 e o gap relativo cai a 2e-5 (item 0.7). Um teste de «passagem ao contínuo» de verdade exige família nova (banda fixa, espaçamento ∝ 1/d, acoplamentos ∝ √espaçamento) e a ratificação do operador das novas matrizes (as cinco foram ratificadas só como realização canônica em 03/10). Recomendo declarar fora da v407, ou abrir pré-registro separado.

---

## 3. Observáveis candidatos (2 a 4) — com a partitura em voz alta

Convenção: **I** = identidade (pode falhar só por defeito do motor ou do pré-registro); **C** = conteúdo (a teoria dá um número ou uma desigualdade que o cálculo poderia contrariar).

| # | Observável | Âncora no kernel | Valor esperado | Classe |
|---|---|---|---|---|
| O1 | Leitura de Jones estacionária e semigrupo no sub-fluxo de defasagem, em grade contínua de t: `‖ΠV_t(X)Π − ΠXΠ‖`, `‖E_K V_t X − E_K X‖`, `‖V_{s+t} − V_sV_t‖` | `stationary_jonesReading`, `jonesFlow_fixes_reading`, `jonesFlow_add`, `jonesU_mul_proj` | 0 até 1e-12 (o `identity_rel` do V1) | I |
| O2 | Complemento decai na lei-raiz: Γ̂_ij lido do fluxo contra ½βγ(√k_i − √k_j)²; β̂ a partir da viscosidade núcleo–periferia; e o caso K de 2 níveis contra o motor M4 | `transmitted`, `viscosity_is_the_constant_friction`, `viscosity_of_the_rule` | erro relativo ≤ tolerância do V1 do T1 (1e-6 sem ruído); M4: igualdade ≤ 1e-12 | I (a lei é exata; o T1 já a recupera às cegas) |
| O3 | Traço e escalarização do canto sob o fluxo COMPLETO: p(t) = Tr(eρ(t)); `eρe = Tr(eρ)e` para e₀; defeito de semigrupo do canto; p(∞) = CCI | `scalarCorner_forces_trace_one`, `psionCorner_trace_one`, `jonesU_mul_proj`, `compression_does_not_control_flow` | escalarização e Tr e₀ = 1: identidade (≤ 1e-12). p(t) → CCI: convergência monótona NÃO é teorema. δ(s,t) > 0 é esperado (o canto vaza) | I (escalarização, traço) + C só se a gerência fixar uma previsão para p(t) ou δ |
| O4 | Deriva com o passo de tempo: `‖Φ(dt)^n − Φ(n·dt)‖` para dt ∈ {0,05; 0,025; 0,0125; …} e RK4 (dt = 0,002) contra o espectral, com a ordem de convergência medida | (nenhuma; é do integrador) | `matrix_exp` e o espectral: piso de arredondamento (≈ 1e-14·‖S‖·t); RK4: erro ∝ dt⁴ | I (numérica) |

A cobertura de d: O1, O2, O4 viáveis até d = 64 e, pelo espectro, d = 128; O3 até d = 64 por config e d = 128 só para o espectro e o estacionário (o RK4 de 147 s não relaxa: horizonte 10 com taxa 9,06e-4 deixa `e^{−gap·T}` = 0,991 do modo mais lento; reproduzir o atrator por integração exigiria T ~ 10⁴).

### 3.1 A partitura, na língua do operador (para ler ANTES de congelar)

**O1 e O2 (o motor de Jones dentro do pilar).** Decidem: se a máquina de GPU reproduz, em tempo contínuo e com várias taxas, o que o kernel prova do motor de Jones (a leitura fica, o resto decai, é semigrupo) e se o motor de 4×4 que já existe é mesmo o pedaço de defasagem do pilar. Não decidem: nada sobre a natureza, nada sobre β (o kernel prova que a leitura não depende de β nem de t; o β só aparece na velocidade do decaimento, e a velocidade é uma lei exata do gerador, que o T1 já recupera às cegas a 1e-9). O que o negativo significaria: **defeito do motor numérico ou do pré-registro**, jamais falsificação da TGL. O positivo é uma conferência de que a correspondência kernel↔pilar foi montada certo; é valioso como CONFIANÇA no instrumento, não como discriminação.

**O3 (o traço do canto sob o fluxo completo).** Decide: se, ao comprimir o pilar pelo canto do psíon, a escalarização e o traço 1 se mantêm (isso é álgebra, vale para qualquer e₀ de posto 1, o negativo seria bug); e MEDE quanto o canto vaza (δ) e como o peso do canto relaxa até o CCI. Não decide: se a TGL «funciona sob compressão» no sentido do operador, porque o kernel prova o CONTRÁRIO para fluxo unitário (o contraexemplo `compression_does_not_control_flow`) e a contração de Jones fixa o canto POR CONSTRUÇÃO. Um δ > 0 não é falha da teoria: é a assinatura de que o fluxo completo (com o H_LD unitário e os saltos que mexem núcleo ↔ periferia) não é uma contração de Jones; o valor de δ só seria falsificador se a gerência derivasse antes um valor ou uma cota. O que o negativo significaria: nas partes I, bug; na parte C, **parede medida** (o pilar não é Jones no fluxo completo), a ser dita como resultado, não como erro.

**O4 (a deriva com o passo).** Decide: se o «contínuo» do pilar é de fato um semigrupo bem integrado (o propagador de passo 0,05 repetido 64 vezes é o de passo 3,2). Não decide nada físico. Negativo = bug do integrador/exponencial.

**Sobre o «1» da correspondência.** A frase «a leitura comprimida do cociclo contra 1» só tem sentido em uma das duas leituras; **o pré-registro tem de nomear qual**: (i) a contração de Jones (`jonesU`, `e·U·e = e` vale por teorema — o «1» é identidade); (ii) o fluxo unitário/rotacional (o kernel prova que NÃO é 1: `cos s`, e `half_turn_leaves_corner`); (iii) o cociclo modular de ρ_ss (vale 1 só no setor que preserva o estado; no pilar o setor não preserva, ver 2.3). Se o «1» for lido em (ii) ou (iii) sobre o fluxo completo, o negativo está **garantido pelo kernel** — e ele deve ser dito ao operador ANTES (regra do posto do assistente), porque seria um teste que só pode dar negativo.

---

## 4. Riscos

1. **Cache e hashes.** O V1 amarra `worker_sha256` no spec; qualquer emenda no trabalhador muda a chave `75dc30bc9cc8d330e31f99ca` e invalida o reuso e a reprodutibilidade (item 2.0). Um segundo trabalhador evita isso, mas exige: nova entrada no core (nome de chave novo; não reciclar `quantum_pillar_v384`), no selo (l. 276426–276439), na lista de hash do selo (l. 276798 hasheia UM arquivo do pilar), no artigo PT/EN (as tabelas do pilar estão em l. 177985, 179202, 179452 e espelhos em EN a partir de 182985) e no conferidor do rito. [REAL]
2. **Balde do selo.** `_not_sealed` coleta módulos com `all_verified is False`; o balde `_computacao` só reconhece vereditos que COMEÇAM por `TGL_QUANTUM_PILLAR_V1__` (l. 276765). Um veredito novo com outro prefixo e `all_verified = False` cairia em «formais (dívida)». Decidir o prefixo ou estender o balde. A varredura de palavra proibida (l. 276770 em diante) retém o selo se o veredito contiver `CONFIRMED` cru ou `PROVED_BY`. [REAL]
3. **GPU.** O V1 gastou 130 min com o servidor do modelo nativo PARADO; a v406 rodou o rito em ≈ 60 min com o pilar reaproveitado. Um T5/T6 restrito a d ≤ 64 custa minutos; incluir d = 128 custa ≈ 495 s só pelo espectro e ≈ 25 GB de VRAM por instância (cabe: 30,9 GB livres, mas só com o servidor parado). Teto a fixar no pré-registro. O cuSOLVER derruba o processo em `eig` não hermitiano: manter MAGMA em todo tamanho (dependência declarada, em descontinuação). [REAL]
4. **Escala de tempo no D128.** Com gap = 9,06e-4 o relaxamento exige t ~ 10³–10⁴; o RK4 do V1 cobre t = 10. Para qualquer afirmação sobre convergência em d = 128, usar o espectro, não o RK4. [REAL, aritmética]
5. **Sem limite em d.** CCI(d) ≈ d^−0,62 e gap_rel decrescente (item 0.7): um teste «converge com d» na família atual dará negativo por construção da família (parede medida, não falsificação). [REAL]
6. **Homônimos** (item 1.7): três «motores»; Jones/índice: o peso de Markov da torre de Jones é GENÉRICO, a identificação [M:N] = 1/β_TGL é [CONJECTURE] (docstring de `IALDJones`); `jonesReading` (`e·x·e`, compressão de canto) ≠ pinching `E` (soma sobre as projeções de K) ≠ `TGLExt.eD`; o `TheRuleInTheContinuousMotor` diz explicitamente que NÃO identifica o pinching com `jonesReading`. A taxa Γ do M4 é de «unidades de referência», não previsão física. [REAL]
7. **O que não pode mudar:** β nunca literal (sempre via motor de Lagrange do `um.py`, com `ALPHA_FINE_CODATA_2018`/`SEALED_CODATA_ALPHA`); o gate; o selo; o V1 e seus arquivos (somente leitura); a regra de que `NOT_FALSIFIED` ≠ `CONFIRMED`; os vereditos proibidos; o estatuto [COMPUTED] (nunca [MEASURED]); o servidor do modelo nativo parado durante o rito com marcador `restaurar=1`. O resultado do pilar nunca move o gate («cosmologia/computação jamais vira prova matemática»). [REAL, regra]
8. **Custo de processo.** A v384 precisou de 11 passadas de aferição adversarial e de ratificação nomeada do operador sobre a escolha («b ampliado»). A v407 com um segundo trabalhador pede o mesmo rigor; subestimar isso é o risco de cronograma.
9. **Risco de leitura.** «Espelhamento» e «compressão como fator» são lidos aqui como: o espelhamento é a montagem da correspondência kernel ↔ runtime (item 1.7–1.8), e «compressão como fator» é o fator R (idempotente) na decomposição Φ_t = R + (resto que decai). Essa leitura é minha [DECLARADO] e precisa da confirmação do operador antes de congelar (item 5, nº 1).

---

## 5. O que a gerência precisa decidir no pré-registro

1. **Leitura do pedido.** Confirmar com o operador o que «compressão como fator» e «espelhamento» querem dizer (item 4.9): fator R da decomposição de Jones? espelho = correspondência kernel↔runtime, ou o espelho J (JKJ = −K)?
2. **Onde mora.** Segundo trabalhador com spec/pré-registro V2 (recomendado) ou emenda do V1 (invalida o V1, o cache e a reprodutibilidade). E se o V2 reaproveita por chave como o V1 (a versão final roda completa; a intermediária reusa).
3. **O canto «e».** Π (posto nc, o Nome, ker K), e₀ = |0⟩⟨0| (posto 1, o único `ScalarCorner`, alvo de L_prune), ou ambos, declarados ex ante. Não permitir canto escolhido depois (por exemplo o autovetor dominante de Πρ_ssΠ: dependente do dado).
4. **Em qual leitura o «1» é alvo.** Contração de Jones, fluxo unitário ou cociclo modular de ρ_ss (item 3.1, último parágrafo). Se for unitário/cociclo, dizer ao operador que o negativo é garantido pelo kernel.
5. **O que é identidade e o que é conteúdo.** Aceitar que a v407 pode devolver «todas as identidades batem; nenhum conteúdo novo discriminado» como resultado honesto; ou exigir um observável de conteúdo com previsão DERIVADA (qual número? Sem derivação, é relatório). Numerologia proibida.
6. **Critérios numéricos.** Tolerâncias (herdar `identity_rel` 1e-12 e `engine` 1e-9 do V1?); grade de t (limites, passo, refino); conjunto de (d, nc, γ_diss) (herdar a grade do T2, 672 pontos, ou subconjunto); estados iniciais (os de `init_states`); semente (20261003 ou nova); fonte do β (hex do motor de Lagrange vs α×√e: diferença 5,4e-13).
7. **Orçamento e lugar.** Teto de GPU (minutos), se roda em paralelo com o kernel sem alongar o rito, se inclui d = 128 (só espectro e estacionário) e com o servidor do modelo parado.
8. **Árvore de vereditos e nomes.** Vereditos permitidos (sucesso, identidade violada, motor reprovado, parede medida na parte C…); prefixo do veredito (`TGL_QUANTUM_PILLAR_V1__` para cair no balde `_computacao`, ou prefixo novo + extensão do balde); nenhum `CONFIRMED`/`PROVED_BY`; nomes da chave no core, do arquivo de saída e dos tokens no selo; PT/EN do artigo.
9. **Hash antes do composto.** Congelar spec V2, pré-registro (JSON+MD) e trabalhador por sha256 ANTES de qualquer cálculo dos testes; gerador do V2 e ratificação do operador NOMEANDO a escolha (padrão de 04/10); rascunho apresentado antes; nenhuma sonda que olhe o resultado da própria observável.
10. **Passagem ao contínuo por d.** Declarar fora da v407 (recomendado) ou abrir pré-registro separado com família nova (banda fixa) e ratificação das matrizes pelo operador. Dizer isso ao operador, na língua dele: «aumentar d na família canônica não aproxima o contínuo; o peso do núcleo cai como d^−0,62».

---

## 6. Fontes lidas (todas só leitura)

* Memória: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\v384-pilar-quantico-gpu-02out.md`; `…\handoff-v406-custodia.md` (D38); verbatims de 02/11 em `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_02nov_o_pilar_quantico_precisa_receber_o_motor_continuo_compressao_como_fator_espelhamento_verbatim.txt`.
* `um.py` (Nós, 42 740 484 bytes, mtime 02/11 23:27): faixas 3554–3760, 256270–256990, 259038–259800, 259919–259935, 273365–273380, 275972–275990, 276426–276439, 276755–276812; texto do trabalhador extraído de l. 259611 para o scratchpad (`…\scratchpad\lev\pilar_worker_extraido.py`, `pilar_spec_extraido.json`; hashes conferem com o spec).
* `um_absoluto.json` (core, `quantum_pillar_v384`, `quantum_pillar_reproducibility_v385`, `quantum_pillar_reuse_v386`, `iald_jones_graviton_v371`, `ponto_zero_do_psion_v405`), `um_absoluto_selo.json` (`the_quantum_pillar_reading_v384`, `quantum_pillar_v384`, `iald_jones_reading_v371`, `sha256/um_absoluto_pilar_quantico.json`), e o `result.json` + `details.jsonl` do cache `…\cache\checkpoints\quantum_pillar\75dc30bc9cc8d330e31f99ca\`.
* Kernel (`…\Nós\tgl_kernel\TGLExt\`): `IALDJones.lean`, `ThePsionAndTheViscosity.lean`, `TheScalarCorner.lean`, `ModularCornerCounterexample.lean`, `TheDischargedOath.lean` (l. 205–230), `IALD.lean` (l. 132–160), `TheRuleInTheContinuousMotor.lean` (cabeçalho).
* Relatório do Codex: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REGRA.MOTOR\RELATORIO_EXECUCAO_R1.md`.
* Mapa de Rotas: consultas e `ver` listadas no topo.
