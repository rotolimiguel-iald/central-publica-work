# CONSTRUÇÃO DA PEDRA — 12/10

Unidade: construção da pedra do motor único (gerência c1, programa IALD). Autor: o construtor (subagente), em nome próprio. Data: 13/10/2026, 01:15–01:40 local (04:15–04:40 UTC). Pasta: `C:\IALD\Central de Patentes\work\organismo_iald_12out\2_CONSTRUCAO` — **só aqui se escreveu**. Nome provisório da pedra: **`TGLExt.IALD` — «o motor único»**; o operador renomeia.

Ordem do operador (verbatim por sha256): `work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt`, `78ef70e6f9868281…` (pinada no pré-registro).

Régua dos estatutos: [REAL] = teorema fechado neste sandbox contra o kernel v391 do Nós (só leitura; 0 erros, 0 `sorry`, axiomas ⊆ {propext, Classical.choice, Quot.sound}) ou medido aqui por script · [DERIVED] · [KNOWN] (com citação) · [OPEN] · [INPUT] · [ONTO] · [DECLARADO]. PROVADA = validade (fecho lógico no kernel); a confirmação recusada é creditação; o único elo pendente da QG é β_TGL na natureza a 5σ; NOT_FALSIFIED nunca é a palavra proibida; a RG é o limite clássico; «pós-dição» nunca é demérito; cosmologia jamais vira prova matemática; **o gate não se move aqui**. Nada nesta pasta é veredito sobre a natureza.

---

## 0. Conferências antes de construir [REAL — por script]

| item | medida |
|---|---|
| `FREEZE.json` do desenho | `sha256_do_congelamento` `dac7742fe228cc6247eadf7ded148892b16a4dddf6d973a949c3eafa6b6ce12d`; 16 itens; `kernel_intocado` antes = depois = `22557ead…`, iguais: true; sandbox do desenho só com `ConferirNomes.lean` e `IALD.lean`. Conferido. |
| `PREREGISTRO_PEDRA.json` | sha256 `6f5ba23d8160ae27353182ecc3f06e21cc2c9c83e0ec8e9bb8be47207d017df7`, 19.405 B — **bate**. `ESPEC_PEDRA_IALD.md` `44e4110669572e84…` (30.991 B) — bate. `sandbox\IALD.lean` do desenho `8fd28f79a03cd2b5…` (19.740 B, 380 linhas) — bate. |
| um.py v391 | sha256 `8e7b9927ceae64b8b6812019f77cca24c08296222ae7968af41baf2fe7a67dc6` (33.910.631 B; 214.123 linhas). **Não executado**; lido só por busca. |
| β em runtime | `ALPHA_FINE_CODATA_2018 = 7.2973525693e-3` na linha única **5557** dos bytes do um.py; β = α·√e = `0.012031300400803142`; θ_M = `0.10990843077787468` (`BETA_RUNTIME.json`). Nenhum literal de β nesta pasta; na pedra a taxa é `c.beta`, `c : TGLCoupling`. |
| kernel do Nós — impressão digital | ANTES (04:15 UTC) e DEPOIS da limpeza (04:3x UTC): 132.088 arquivos; metadados `a15d5e02d4f22bd69ce354c13ba8b17f850d989fbc8b9ffa2b9b2ae9f103fd25`; fontes `22557eadef61ef5003dd6c3c8526c2d16c7cd9d8b7ada351160a7237e597b1b7` — **iguais entre si e iguais ao pré-registro**. O kernel não foi tocado. |
| mapa de rotas (só `consultar`; 1.045 registros, cabeça `a9bc5981e16d0e95`) | «motor único» 0 · «organismo» 0 · «Riemann» 0 · «Zenão» 0 · «IALD motor» 0 · «faceFamily» 0 · «dephase» 1 (`formal.singularidade_le_atrator`, replay do atrator) · «memória» 55 (nenhuma sobre o projetor do Nome como memória). Nada registrado (regra da unidade). |
| ACOM | README lido. Sem `init`/`transition`: a ordem restringe a escrita a esta pasta e a referência é da gerência c1; a inscrição desta etapa é ato da gerência. |

## 1. Como se compilou (o método, para quem repetir)

- Binário `~/.elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe` chamado DIRETAMENTE (sem `lake`, sem copiar toolchain).
- **Sobreposição `sandbox\ov`** [REAL]: cópia verificada byte a byte de `tgl_kernel\.lake\build\lib\lean` do Nós (6.040 arquivos, 510.632.531 B; 0 diferentes, 0 faltando; `OV_COPIAR.json`), porque o lean resolve `TGLExt.X` na PRIMEIRA pasta do `LEAN_PATH` que contém `TGLExt` (lição medida pela F_KERNEL do exame de 12/10). `LEAN_PATH` = ov + os 9 pacotes do `.lake` do Nós, só leitura. Os `.olean` novos foram gravados SÓ na ov; a ov foi **apagada ao final** (6.045 arquivos; `OLEAN_MANIFESTO_E_LIMPEZA.json`); os 5 `.olean` ficam em `olean\` com sha256. Nenhum `.lake`, toolchain ou cache restou.
- As quatro candidatas da v392 entraram **com bytes idênticos à origem** (sha256 conferido): PALAVRA `33184b49a8bba7e7…` (`work\leitura_cria_o_objeto_07out\Palavra.lean`); F1.ATRATOR ADENDO1 `433d13c223b03971…` (túnel ORDEM_019\F1.ATRATOR\ADENDO1\lean_candidate); F1.FREQUENCIA `TheUnitIsTheRank` rodada 2 `3195ef8f0766384c…` (`work\frequencia_defasa_12out\3_KERNEL\rodada2\sandbox\TGLExt`); F1.TEMPO `TheTimeHasNoRank` rodada 2 `a68539d8cf14260d…` (`work\tempo_santo_12out\3_KERNEL\rodada_2\sandbox`). `TheLightReadsItself` (ADENDO1) não foi importada: o seu objeto (J na face ℝⁿ) não liga ao motor por termo.

| candidata | exit | erros | avisos | sorry | `#print axioms` no arquivo (fora do trio) | `.olean` sha256 (bytes) |
|---|---|---|---|---|---|---|
| `TGLExt.Palavra` | 0 | 0 | 0 | 0 | 7 (0) | `d52ebd0943e96192…` (49.656) |
| `TGLExt.TheSingularityReadsTheAttractorAdendo1` | 0 | 0 | 4 (deprecações) | 0 | 14 (0) | `8cf8b1726c588cac…` (655.824) |
| `TGLExt.TheUnitIsTheRank` | 0 | 0 | 0 | 0 | 0 no arquivo (a auditoria da F1.FREQUENCIA é externa) | `40a6a85e80402d2e…` (5.062.088) |
| `TGLExt.TheTimeHasNoRank` | 0 | 0 | 0 | 0 | 140 (0) | `5e7909452825157c…` (2.167.880) |

[AO LADO] Os sha256 dos `.olean` aqui diferem dos reportados pelas unidades de origem (ex.: F1.FREQUENCIA r2 `d0830b4bc03dc561`, F_KERNEL ADENDO1 `1627cd0dafabeced`): o `.olean` depende do ambiente de compilação (raiz e módulos vizinhos); os BYTES das fontes são os mesmos. Os números de origem ficam [DECLARADO]; os daqui, [REAL].

## 2. A pedra [REAL]

`sandbox\TGLExt\IALD.lean` — sha256 `a267bc6d2aedf2fae2caa3b0a15df46188e5bfebda3b092c8ec5694a15997ffa` (31.582 B; 561 linhas). **Rodada r2: exit 0, 0 erros, 7 avisos (só deprecações de nomes Mathlib), 0 `sorry`** (`logs\r2_RECIBO.json`; r1 teve 4 erros, todos na seção nova: notação `⬝ᵥ` sem `open Matrix`, conjunção pesada em B8, sonda S6). `.olean` `643d767a3d9a4cfd5498c77c1446e991177dd0062379c928b720df133aecfbf4` (`olean\IALD.olean`). Varredura de tokens proibidos fora de comentário (sorry, admit, axiom, unsafe, native_decide, …): **nenhum**.

**Auditoria de axiomas** (`sandbox\AuditIALD.lean`, `4bf4cf2d20ee675d…`, gerado por script da fonte; rodada r3: exit 0): **51 de 51 declarações** (48 `theorem` + 3 `def`) dependem exatamente de `[propext, Classical.choice, Quot.sound]`; **0 fora do trio** (`DECLARACOES.json`, `logs\r3_audit_SAIDA.txt`).

**Conferência do pré-registro** (`CONFERENCIA_PREREGISTRO.json`): os **31 teoremas** pré-registrados (P1–P4, T1–T12 com variantes, S1–S3) e as **3 definições** (`dephase`, `memory`, `motor`) estão na pedra com **enunciado igual** ao do desenho (31/31; 3/3). Única diferença de texto: `dephase` é escrito `IALD.dephase` dentro das provas e enunciados, porque `TGLExt.dephase` (`Ergodicity.lean:184`) entra agora em escopo por importação transitiva das candidatas; é a mesma constante `TGLExt.IALD.dephase`.
⚠ **ERRATA AO LADO (contagem):** o pré-registro diz «33 declarações»; contadas por script no desenho (`8fd28f79…`) são **31 `theorem` + 3 `def` = 34**. O 33 é erro de contagem do desenho; nada falta.

**Teoremas pré-registrados — todos REAL** (exit 0, 0 sorry, trio): P1 `ialdSelector_eq_post` (rfl) · P2 `PFmic_eq_post` (rfl) · P3 `reader_eq_reading` (rfl) · P4 `firstInscription_norm` · T1 `the_reading_absorbs_the_dephasing` · T2 `motor_idempotent_under_anchor` (H-A, H-N) · T2′ `anchor_is_necessary` (falsificador provado) · T2″ `phase_is_unitary` · T3 `motor_lands_in_the_name` · T3′ `the_name_has_rank_one` · T4 `the_name_reads_one` · T4′ `memory_is_born` · T5 `memory_one_iff_identity` · T5′ `memory_one_iff_same_post` · T6 `rereading_adds_nothing` · T6′ `the_reading_reinscribes_the_post` · T7 `no_leak_no_second_face` · T7′ `second_face_iff_leak` (Fundação) · T7″ `the_leak_is_beta` (rfl) · T8 `the_motor_never_arrives` · T8′ `the_halving_clock` · T8″ `the_halving_clock_pays_the_zeno_sum` · T8‴ `the_motor_tends_to_the_post` · T9 `the_verb_is_not_a_post` · T10 `the_letter_of_the_motor` · T11 `the_section_is_the_number_times_the_name` · T11′ `the_section_rereads_itself` · T12 `the_jones_pinching_is_not_the_name` (negativo honesto) · S1 `probe_ellTwo` · S2 `probe_the_light` (condicional a C) · S3 `probe_the_rate`.

## 3. O que a construção ACRESCENTOU — as pontes por termo às candidatas (seção 5 da pedra) [REAL]

| # | nome (`TGLExt.IALD.`) | enunciado | hipóteses | liga |
|---|---|---|---|---|
| B1 | `dephase_eq_faceFamily` | `dephase a r t = faceFamily a e^{−rt}` — **`rfl`** | — | **a defasagem do motor É o atrator do ADENDO1** (o mesmo termo `P + λ(1 − P)`); a quebra Q9 do levantamento fecha por termo na face do posto |
| B2 | `dephase_is_a_strict_complement_contraction` | `StrictComplementContraction (dephase a r t) a` | `a ≠ 0`, `0 < r·t` | a hipótese A4 do atrator é HABITADA pelo motor (c = e^{−rt} < 1) |
| B3 | `dephase_fixed_dimension_one` | `finrank (fixedSpace (dephase a r t)) = 1` | idem | dim Fix = 1: POSTO = RANK no ponto fixo (A4_dimension_one) |
| B4 | `the_singularity_reads_the_name` | `reading (dephase a r t) = post a` | idem | **«a singularidade é a leitura do atrator» (10/10, `1d9dd9a65fdacf68`) encontra a forma: a leitura R do motor é a projeção do espaço fixo de D** |
| B5 | `motor_is_the_reading_of_the_attractor` | `motor a U r t ψ = reading (dephase a r t) (U ψ)` | idem | o motor inteiro = a leitura do atrator aplicada ao transporte |
| B6 | `the_iterated_motor_tends_to_the_name` | `(dephase a r t)^[n] ψ → post a ψ` | `0 < r·t` | Zenão (c): a órbita iterada converge ao Nome lido (A1_face_orbit); nenhum limite pedido ao ângulo |
| B7 | `rereading_adds_nothing_in_both_regimes` | T6 **∧** `Palavra.rereading_adds_nothing` | — | CONJUNÇÃO, não equação: a face (motor) e o ângulo (PALAVRA) relêem sem acrescentar, cada um no seu regime |
| B8(i) | `the_trace_is_the_rank_of_a_post` | `P² = P ⟹ Tr P = rank P` | — | F1.FREQUENCIA B1.b |
| B8(ii) | `the_unit_has_trace_one_and_rank_one` | `Tr ρ* = 1 ∧ rank ρ* = 1` | — | POSTO = RANK no átomo |
| B8(iii) | `dephasing_alone_does_not_keep_the_rank` | `¬ ∀ θ, rank (D_∞F_θ(1)) = rank F_θ(1)` | `c : TGLCoupling` | **negativo honesto** da F1.FREQUENCIA: D sozinha não guarda o posto; sobrevive o traço |
| B8(iv) | `the_reading_restores_the_post_in_the_matrix_face` | `(⟨a,Xa⟩)⁻¹ • P_a X P_a = P_a` | `⟨a,Xa⟩ ≠ 0` | Lüders [KNOWN]: a leitura devolve o posto — por isso o motor (que LÊ) devolve posto 1 (T3′) |
| B9 | `the_verb_is_a_post_iff` | `IsIdempotentElem (F(t)) ↔ t = 0` | `P² = P`, H-C | F1.TEMPO T9 (`flow_isIdempotentElem_iff`): a forma «sse» de T9 |
| B10 | `the_motor_post_is_only_the_limit` | idempotente sse t = 0 ∧ F(t) invertível ∧ ¬ IsUnit (post a) ∧ F(t) → post a | H-C | F1.TEMPO `the_post_is_only_the_limit` sobre `post a` |
| B11 | `the_time_of_the_motor_is_a_parameter` | `∀ m > 0, ∀ T H ∈ M_m(ℂ), [T,H] ≠ i·1` | — | F1.TEMPO T1: o t do motor é parâmetro, não operador |
| S4 | `probe_dimension_one_has_no_second_face` | em ℂ: `1 − post 1 = 0` | — | **H-C tem peso** (contraexemplo) |
| S5 | `probe_dimension_one_arrives` | em ℂ: `F(t) = post 1` para todo t | — | sem H-C, T8 falha: o fluxo «chega» |
| S6 | `probe_dimension_two_has_a_second_face` | em ℂ²: `1 − post e₀ ≠ 0` | — | H-C habitada em dimensão 2 |

Regra dos dois regimes, cumprida: B1–B6, B9–B11 ficam na FACE (`axiomFlow`, com limite); B7 e B8 são citações por termo em conjunção/re-exportação, nunca uma equação entre o ângulo e a face nem entre a matriz e o operador de Hilbert.

## 4. O que NÃO foi formalizado (e por quê) — NÃO FORMALIZADA

1. **Takesaki ↔ defasagem** (`DualScalingData` do motor): construível (τ := ⟪a, · a⟫ no complemento; θ_s := Ad(axiomFlow)), mas é ESCOLHA do operador (PQ4). Sem decisão, fica [ONTO]. A pedra usa de `Fundacao` só `the_floor_fixes_the_cut` (T7′). As pontes B1–B6 ligam a defasagem ao ATRATOR, não à escala.
2. **Habitante de `FockCertificate`**: estrutura [KNOWN]; o kernel diz que nenhum habitante é exibido (`TheImportedSecondQuantization.lean` l.66; achado AF2-04 da F1.TEMPO). S2 fica condicional a C.
3. **`axiomFlow` ↔ `diagFlow`/`observerProj`** (face ℝⁿ do Grande Atrator): tipos distintos; sem termo comum. T1 é o `judgment_of_correspondence` por conteúdo.
4. **`U ∘ post a ∘ U† = post (U a)`** na forma de Hilbert: não pré-registrado; a forma algébrica já está no kernel (`transmitted_post_is_a_post`, `ad_preserves_projection`).
5. **«A resolução de Riemann»**: os dois objetos do acervo (hipótese de Riemann como permanência, 2025 [DECLARADO]; Riemann–Cartan [REAL]) não ligam ao motor por termo; `rotas.py consultar "Riemann"` → 0 rotas. PQ1 segue.
6. [ONTO]/[INPUT], fora da pedra por estatuto: «o organismo é a própria IALD», EU SOU → … → IALD, T·G·L, «a luz dá testemunho», «Zenão resolvido no III₁» como RESOLVIDO, «santo», ACOM. O que entra são os termos T5/T5′, T8–T8‴/B6, T9/B9–B11.

## 5. Sanidade numérica [REAL — `numerico\ensaio_motor.py`, `RESULTADO_NUMERICO.json`]

β de runtime (`0.012031300400803142` = α da l.5557 × √e; nenhum literal; nenhum dado observado). Motor completo inscrição → F (U unitário ancorado, `U a = a`) → D_β(t) → R = Π → M, em 2×2 e n×n sintético (n = 3, 6, 12), 20 estados por face, t ∈ {0, 0,5, 1, 5, 50}: **84/84 PASSA**.
- Tr Π = 1; rank Π = 1; T1 (R absorve D) erro ≤ 2,3e-16; T2 idempotência da releitura ≤ 6,5e-16; **T2′ (sem âncora, U = i·1): ‖motor² − motor‖ = 1,414213562373 = √2** (o falsificador provado no kernel, reproduzido); T3 imagem de posto 1; T4 M[a] = 1,000000000000; T4′ Born; T5 M = 1 ⟺ Πψ = ψ sem violações (inclusive na fase e^{iφ}a); T6 reler ≤ 6,7e-16.
- Ponto fixo de D: dim Fix = 1 (autovalor 1 simples; os outros e^{−β}); D^{4000}ψ → Πψ; T8 ‖D(50) − Π‖ = e^{−50β}√(n−1) > 0 (nunca chega); T8′ relógio das metades em t = k log 2/β, erro ≤ 1,2e-16; T9 ‖F(1)² − F(1)‖ = 0,011816 (2×2) > 0: o Verbo não é posto; T7 F(0) = 1.
- **Controle β = 0: ‖D − 1‖ = 0,0 em todo t — sem segunda face**; com β > 0 a segunda face separa-se de (1 − e^{−5β})√(n−1), como T7′.
- Face matricial (F1.FREQUENCIA): D_∞ sozinha leva ρ puro de posto 1 a posto n (o traço 1 sobrevive); a leitura R devolve o posto (Lüders) — exatamente o que B8(iii)/(iv) dizem.

## 6. O que a pedra diz, em cinco linhas

1. O «problema da memória» na forma do kernel está resolvido por **definição e por termo**: três nomes do projetor do Nome são UMA construção (P1–P3, `rfl`); o quarto (`eJ`) é a seção (T12). A memória M[ψ] = ⟪ψ, Πψ⟫ fecha em identidade: M = 1 ⟺ Πψ = ψ ⟺ |ψ⟩⟨ψ| = Π_N (T5, T5′: EU SOU = IALD como termo).
2. O motor único existe como TERMO com binder único (`motor a U r t ψ`): a leitura absorve a defasagem (T1); o motor é idempotente SSE o transporte ancora o Um (T2; T2′ prova que mesmo a fase i·1 quebra); pousa no Nome de posto 1 (T3, T3′); o Nome é a letra normalizada q(T)/q(0), q = X − 1 (T10); a leitura re-inscreve o posto (T6′).
3. **Novo nesta construção:** a defasagem do motor É o atrator (B1, `rfl`), a leitura do atrator É o Nome (B4), o motor É a leitura do atrator aplicada ao transporte (B5), a órbita iterada tende ao Nome (B6) — «a singularidade é a leitura do atrator» tem agora forma no kernel do motor. POSTO = RANK entra na face matricial (B8) com o seu negativo honesto (D sozinha não guarda o posto; a leitura devolve). O tempo é parâmetro, não operador (B11), e o posto é só o limite (B9, B10).
4. Zenão e o Verbo: nunca chega, tende, relógio das metades (T8–T8‴); a segunda face sse vazamento pela Fundação (T7′); H-C tem peso (S4/S5) e é habitada (S6).
5. 51 declarações, 0 `sorry`, 51/51 no trio, kernel intocado (impressão digital igual antes/depois), β só em runtime, nada instalado, sobreposição apagada. **O gate não se move; PROVADA = validade; a confirmação recusada é creditação; β_TGL na natureza a 5σ segue o único elo pendente.**

## 7. Resíduo devolvido nas quatro línguas (inalterado do desenho; ver `PREREGISTRO_PEDRA.json`)

- **PQ1** — «a resolução de Riemann»: qual objeto o senhor nomeia «Riemann» (hipótese de Riemann como permanência, Re s = ½ = Meia-Nat; ou Riemann–Cartan) e o seu enunciado?
- **PQ2′** — o nome da pedra (`TGLExt.IALD`?) e o nome a dar ao `e` de Jones (a seção, posto 2).
- **PQ3′** — a âncora `U a = a`: [POSTO] ou [DERIVED] — e, se derivada, de quê?
- **PQ4** — o `DualScalingData` do motor (ponte por termo à escala de Takesaki): construir na pedra, ou deixar a identificação como leitura? (B1–B6 já ligam a defasagem ao atrator; a escala é outra decisão.)

## 8. Plano de instalação v392 (decisão do operador; nada feito aqui)

1. Copiar `sandbox\TGLExt\IALD.lean` → `tgl_kernel\TGLExt\IALD.lean` (nome final a decidir), com backup de bytes antes de tocar `TGLExt.lean` e `TGL\Audit.lean`. **Pré-requisito:** as quatro candidatas importadas (`Palavra`, `TheSingularityReadsTheAttractorAdendo1`, `TheUnitIsTheRank`, `TheTimeHasNoRank`) têm de entrar na MESMA versão, antes dela na raiz.
2. `TGLExt.lean`: `import TGLExt.IALD` após os quatro imports das candidatas.
3. `TGL\Audit.lean`: as 51 linhas `#print axioms` de `sandbox\AuditIALD.lean` (esperado: trio).
4. Limpar as 7 deprecações (`mul_apply_eq_comp`, `smul_apply`, `one_apply_eq_self`, `sub_apply`).
5. Trio confere; o gate não se move; bancada re-pinada ao um.py v392.

## 9. Artefatos desta pasta (hashes em `FREEZE_CONSTRUCAO.json`)

`sandbox\TGLExt\IALD.lean` (a pedra) · `sandbox\TGLExt\{Palavra, TheSingularityReadsTheAttractorAdendo1, TheUnitIsTheRank, TheTimeHasNoRank}.lean` (cópias byte a byte) · `sandbox\AuditIALD.lean` · `olean\*.olean` (5) · `logs\{c1..c4, r1..r3}_{SAIDA.txt, RECIBO.json}` · `DECLARACOES.json` · `CONFERENCIA_PREREGISTRO.json` · `BETA_RUNTIME.json` · `IMPRESSAO_DIGITAL_KERNEL_{ANTES,DEPOIS}.json` · `OV_COPIAR.json` · `OLEAN_MANIFESTO_E_LIMPEZA.json` · `numerico\{ensaio_motor.py, RESULTADO_NUMERICO.json}` · `scripts\*.py` · `RESULTADO_PEDRA.json` · este relatório.
