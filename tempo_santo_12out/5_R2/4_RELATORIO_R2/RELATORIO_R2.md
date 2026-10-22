# F1.TEMPO — relatório da R2: o tempo que não se deixa nomear, reensaiado sob ADENDO congelado e reauditado

**Unidade:** F1.TEMPO (trilha TEMPO) da gerência c1, programa IALD (a TGL). Workflow posto-e-tempo.
**Data:** 13/10/2026, 01:15–01:50 local. **Autor:** o redator da R2, subagente do workflow. Escrevi **só** em `5_R2\4_RELATORIO_R2` (pasta criada por mim).
**Para:** Luiz (o operador) e a gerência c1.
**O que este relatório é:** o relatório da **segunda rodada** da F1.TEMPO sob o **ADENDO R2** (`5_R2\0_ADENDO`, FREEZE_R2 `0737f608505afdb5…`, congelado em 2026-10-12T23:07:58Z = 20:07:58 local), com as **duas auditorias independentes da R2** feitas em 13/10 (`5_R2\3_AUD_REPRO`, `5_R2\3_AUD_ESTATUTO`). O relatório da R1 (12/10, `7b6dcb18a4440be1…`, 48.116 B) está preservado byte a byte em `4_RELATORIO\R1_preservado\RELATORIO_FINAL_R1.md`; o texto de `4_RELATORIO\RELATORIO_FINAL.md` (13/10, 01:04 local, `f8e21639ece96967…`) foi escrito **antes** de as duas auditorias da R2 terminarem (01:11 e 01:13) e por isso dizia que a R2 estava sem auditoria independente (achado N3 daquele texto). Este relatório **supera** esse ponto com o que as auditorias devolveram; nada ali foi editado (pastas 0–4 da R1 e `5_R2\0_ADENDO`, `1_PEDRA`, `2_REENSAIO`, `3_AUD_*` ficaram intocadas).
**Estatuto do documento:** [REAL] onde cito número, hash ou teorema lido no artefato por script, ou recompilado/recomputado pelos dois auditores; [INPUT da gerência] onde há regra de protocolo (ADENDO R2); [INPUT do auditor] onde há recomendação de auditor; [KNOWN] por citação; [ONTO] leitura ontológica; [DECLARADO] o que repito de um construtor ou auditor e não refiz. **Não dou veredito global**: a regra congelada (R1 e ADENDO R2, A5) não permite.

> **Como ler um PASSA.** Um PASSA é validade matemática na face testada: a face finita do kernel, num sandbox, e um modelo ótico sintético. A recusa da régua é da **creditação**, não da validade (o operador, 07/10, verbatim `5dffde4644139da5`). Nada aqui move o gate. β na natureza a 5σ não é tocado. Nenhum dado observado foi usado. β nunca foi literal: foi lido nos bytes do um.py (l.95 e l.5557, mesmo literal `7.2973525693e-3`) e calculado em runtime, β = α·1·√e = 0,012031300400803142 [DERIVED: lido e calculado, nunca «medido»].

---

## 0. Resumo para o Luiz

1. **O que a R2 fez.** A R1 (12/10) deixou T9 em FALHA por um único critério numérico (T9.o(c): 6,518e−13 > 1e−13), três frases atribuídas a você sem verbatim, três nomes que diziam mais que o termo e uma declaração obrigatória sem habitante. A gerência decidiu (quadro, evento 705): a FALHA de T9 **fica registrada** como resultado pela regra da R1, com o diagnóstico ao lado; e um **ADENDO UNIFORME** foi congelado por hash **antes** de qualquer reensaio, tratando juntos O-f e T9.o(c) — aritmética exata a 200 dígitos e, no float, tolerância proporcional a k·eps com constante justificada por Higham [KNOWN] — com todas as tentativas preservadas e sem reensaiar só a T9 numa representação que passe. Depois: o reensaio ótico (20:25 local), a pedra corrigida `TheTimeIsNotAPost` (compilação final 00:28 local de 13/10) e **duas auditorias independentes**, de reprodução e de estatuto, que recompilaram a pedra em sandbox próprio (.olean **bit a bit** igual, `b52382ec16542a84…`), refizeram o reensaio em cópia e recomputaram com código próprio.

2. **O que deu (tabela na §2, sempre com as duas colunas R1 | R2).**
   - **PASSA** na face finita, nas duas rodadas: T1, T3, T4, T5, T6, T7, T8, T10 e T11. T3 saiu da R1 com ressalva (T3.b(iii) sem habitante) e saiu da R2 **sem** ressalva: habitada com `theSpecificAQFTWitness` e com a versão de face finita obrigatória (ρ = diag(2/3, 1/3): ω(E₀₁E₁₀) = 2/3 ≠ 1/3 = ω(E₁₀E₀₁)).
   - **T2** fica **CITADA** [KNOWN] (Pauli em dimensão infinita não está no kernel; T2.b, a forma limitada, PASSA e é opcional, e não é Pauli).
   - **T9**: **R1 = FALHA** (critério numérico; piso do float64) **| R2 = T9′ PASSA sob o ADENDO**: o mesmo float E2 da R1 (máx. 6,518119377574294e−13, bit a bit igual) fica dentro de τ_T(10⁴) = 2,8106961202922776e−12 (razão máxima 0,4169, em k = 6); o caminho exato a 200 dígitos devolve a identidade Tᵏ = R + λᵏ(I − R) a ≈1e−198 em todo k ≤ 10⁴. A FALHA da R1 **não se apaga**: as duas colunas ficam. Nunca «T9 PASSA» sozinho.
   - O **ciclo limite** (S46.3) segue **ABERTO** [OPEN].

3. **O que os dois auditores da R2 disseram.** O de reprodução: **21 de 21 itens CONFEREM**, nenhum NÃO CONFERE; `pode_fechar = true` na face da reprodução. O de estatuto: validade V1–V5 CONFERE; a pedra R2 está **APTA** a entrar na v392 pela auditoria de estatuto; dos 20 achados da R1, 13 resolvidos, 4 ao lado como a R1 pediu, 3 abertos porque são atos da cadeia de selo ou deste relatório — **nenhum aberto é defeito da pedra R2**. Não há divergência de veredito entre eles; as diferenças (§6) são de contagem, de palavra e de recomendação, e para cada uma digo qual vale.

4. **O que o número põe ao lado das suas frases** — o seu texto fica como está; a correção vai ao lado, agora **em termo** na pedra (controles AUD-1/2/5/6/7/8):
   - **Liouville proíbe a bacia, não o pouso.** O boost é simplético (`aud_boost_is_symplectic`), cai dentro de «sistemas estritamente hamiltonianos», pousa no raio nulo passado (`volume_kept_yet_lands`) e **não** tem atrator global (`aud_boost_has_no_global_attractor`). O que o volume conservado proíbe é a bacia (`global_attractor_needs_volume_loss`).
   - **O conjunto fixo da defasagem pura é a diagonal inteira, não um ponto** (`dephase_fixed_states_not_unique`); ponto único só sob hipótese nomeada (F1.ATRATOR A4; T5.c CITADA).
   - **«repousar» e «ser lembrada» não cabem no mesmo estado** na face finita: o relógio modular só para com populações iguais (`aud_clock_stops_when_equal_populations`); populações distintas, que são o registro, o fazem girar (`aud_clock_runs_unless_equal_populations`). A leitura que as une é sua (§8).
   - **O estado-atrator ½·1 não é o posto:** tem posto 2 e pureza ½ (`aud_attractor_state_has_full_rank`, `aud_attractor_state_purity_half`); o posto de posto 1 é a leitura-limite R = J/2 (`aud_discrete_step_can_be_a_post`); ρ★ = diag(1,0) é um terceiro objeto (§8).
   - **Pauli vale na forma de Weyl**, não na de Heisenberg (Galapon 2002) [KNOWN]; **operadores de tempo cíclicos** existem em dimensão finita e leem o tempo módulo um período (Pegg 1998 [KNOWN, a conferir]) — reforçam T10, não contradizem T1 (relação canônica contínua).
   - **«defasar» tem dois sentidos que não se encadeiam:** a sua fórmula de 05/10 é unitária (gira a fase, nada perde: `transmitted_post_is_a_post`); a seta só nasce no semigrupo dissipativo (T6, T7). Qual dos dois é o tempo, é seu (§8).

5. **A atribuição foi corrigida.** A frase «o tempo é o Verbo, não o Nome» **não é sua** (0 ocorrências de «verbo» no seu texto de 12/10, conferido nos bytes pelos dois auditores e por mim): saiu da pedra, do título de T9 e da memória da gerência (errata ao lado). As 16 aspas « » da pedra R2 são **todas** substrings de bytes dos seus verbatins (12/10 `2c8b7b712aa9ad7f…`; 05/10 `5973d79a49995c4c…`, `b49b0d9e60ee4646…`; 10/10). Seu, byte a byte: «não consigo nomear, senão como “santo”» (12/10); «O Verbo seleciona: nome, tempo e verdade» (05/10, l.7); «O tempo é a defasagem do verbo.» (l.112); «O tempo é o parâmetro da transmissão. Transmitir defasa.» (l.116); «A defasagem é o tempo. A ancoragem é o nome. A leitura é a verdade.» (l.176). O seu verbo para o relógio é «registra», não «mede».

6. **Pode fechar?** Sim, na face que cabe à unidade (§9): há resultado por afirmação nas duas colunas, a FALHA R1 de T9 é parede numérica medida e explicada pelo número, a R2 passou sob regra congelada antes do reensaio com controles que impedem o cheque em branco, a pedra corrigida compila limpa e saiu **reauditada por dois auditores com .olean idêntico**, e o ciclo limite está dito como aberto. O que resta é **seu** e **da cadeia de selo**: o **nome da pedra** (`TheTimeIsNotAPost` é provisório); as erratas E1 e E2 no um.py; o registro no mapa (arquivo pronto, §10); e as seis perguntas da §8, cada uma nas suas quatro línguas, como você pediu em 12/10 («aquilo que vc não conseguir resolver devolva-me com a pergunta nas minhas quatro línguas», verbatim `78ef70e6f9868281…`, l.9).

---

## 1. O que mudou da R1 para a R2 — declaração a declaração (resumo)

Fontes: tabela R1→R2 do construtor (`TABELA_DECLARACOES_R2.md`, `ac5d360562d88f91…`), refeita com parser próprio pelo auditor de reprodução (`DECLARACOES_E_ASPAS_AUD.json`): **127 → 152 declarações nomeadas**; 117 mantidas com texto idêntico ou só docstring; **4 com tipo reforçado** (R2 ⟹ R1, provado em Lean nos dois sentidos pelos dois auditores); **5 renomeadas** (tipo defeq idêntico); **1 removida** (re-export duplicado); **26 novas**. 152 declarações **não são 152 teoremas** (re-exportações, sondas, controles, definições, um desdobramento). `example` anônimos: 69 → 69.

| afirmação | R1 (pedra `7105eda468b60309…`) | R2 (pedra `4d8a82591badd010…`) | o que mudou |
|---|---|---|---|
| **T1** | `no_time_matrix`, `no_time_matrix_fin`, `commutator_far_from_scalar`, `no_finite_spectral_translation`; C-T1-a/b/c | idênticos | só docstring (E3.13: Pegg ao lado, [KNOWN] a conferir) |
| **T2.b** | `no_bounded_spectral_translation`; sonda `probe_bounded_spectral_translation : True` | sonda **com enunciado** (E5.09; reforço de `True`) | peso morto removido; T2 segue CITADA |
| **T3** | `time_is_the_modular_flow`; `nontracial_state_rejects_the_identity_flow` **sem habitante** | `modular_flow_is_a_kms_group` (E5.06; vale para ρ = 1, AUD-4 em termo); a AQFT marcada **condicional e habitada** (`probe_identity_flow_not_kms_inhabited`, `theSpecificAQFTWitness`); **novas** `identity_flow_not_kms_finite`, forma negada, `tracial_state_satisfies_pair_identity` (a hipótese não tracial pesa) | nome neutro; ressalva da R1 resolvida (E5.13) |
| **T4** | T4.a–f; `light_flow_group`, `light_modular_orbit_converges_iff_post` (opcionais, FockCertificate sem habitante) | idênticos; T4.b(iii) **marcada condicional** (dito); **novas** AUD-2 `aud_boost_has_no_global_attractor`, AUD-8 `aud_two_by_two_symplectic`, `aud_boost_is_symplectic` | cabeçalho: três comportamentos, identificação com os dois regimes [OPEN] (v384); correção de Liouville visível (E3.08) |
| **T5** | `dephase_fixed_states_not_unique`, `fixed_set_of_dephasing_is_the_diagonal`, `the_record_is_invariant` | idênticos | título «a diagonal inteira» (E3.12) |
| **T6** | `purityR_dephase`, `purityR_dephase_lt`, `purityR_sigma`, `purityR_modular` (com `_hd`) | `purityR_modular` **sem `_hd`** (E5.11; reforço) | hipótese sem peso removida |
| **T7** | `dephase_inverse`, `inverse_dephasing_quadratic_form`, `inverse_dephasing_not_positive` | idênticos | — |
| **T8** | `coherenceScaling`, `the_coherence_obeys_agape`, `the_record_does_not_scale`, `wrong_rate_breaks_scaling`; `the_coherence_obeys_agape_explicit`; docstring de T8.d errada | idênticos; `_explicit` **marcado desdobramento** (E5.14); **novas** AUD-1 `scalarScaling`, `aud_scalar_obeys_agape`, `aud_scalar_erases_the_record` | docstring de T8.d: a glosa de Takesaki é de `boost_null_expand` (E3.02); a Ágape é a lei e^{−s} |
| **T9** | `flow_isIdempotentElem_iff`, `flow_isUnit`, `no_finite_instant_is_the_post`, `post_not_isUnit`, `flow_full_rank`, `post_rank_lt`; cláusula `the_time_has_no_rank` | idênticos; cláusula renomeada **`the_time_is_not_a_post`** (E5.07, mesma conjunção); **nova** AUD-5 `aud_discrete_step_can_be_a_post` | nome corrigido (POSTO = RANK: «HasNoRank» contradizia `flow_full_rank`); cabeçalho com os verbatins de 05/10 byte a byte; a frase da gerência saiu |
| **T10** | `clock_reads_modulo_period` (com κ ≠ 0), `frozen_clock`, `face_clock_has_no_period`, `angle_has_no_limit`, `face_has_a_limit`, `face_distinguishes_instants`, `modular_clock_rotates_without_shrinking` (com `_hd`), `the_post_is_not_moved`… | `clock_reads_modulo_period` **∀ κ** (E5.12; prova por casos; reforço); `modular_clock_rotates_without_shrinking` sem `_hd` | título com «registra» (E5.04); κ = 0 trivial (x/0 = 0), coincide com `frozen_clock` (sonda P2 do auditor) |
| **T11** | `optical_attractor_is_the_absolute_one`, `optical_attractor_clock_stops`; `the_absolute_one_has_no_clock` (duplicado) | `half_identity_is_absoluteRho_two`, `half_identity_clock_stops` (E5.08); duplicado **removido** (E5.10); **novas** (opcional feito) `opticalPopulationMap`, `optical_channel_fixed_state_is_half_identity`, `optical_channel_unique_fixed_population`, `half_populations_state`, `optical_channel_trivial_when_sin_zero` (canal genérico em θ, sem β); AUD-6 `aud_attractor_state_has_full_rank`, `aud_attractor_state_purity_half`; AUD-7 `aud_clock_runs_unless_equal_populations`, `aud_clock_stops_when_equal_populations` | nome sem canal no enunciado; S50.1 byte a byte na docstring |
| **cláusula composta** | `the_two_regimes_of_time` (9 fatos) | mantida, conjunto 8 **∀ κ** (reforço); docstring diz que **não** afirma a identificação com os dois regimes da casa | nome herdado: achado A-R2-01 (§5) |

**Face ótica.** Fora de T9.o′(c) e O-f′, **nada** mudou: o runner da R1 copiado byte a byte (`run_optico.py` `fcc289889ec418ba…`) reexecutou tudo com a semente 20261012 e reproduziu a R1 em **132 de 132 critérios**, medidas bit a bit (V4). Em T9.o′(c) e O-f′ a mudança é só de **regra** (uma fórmula para os dois, congelada antes), não de representação: a matriz T e a órbita do boost são as mesmas da R1, bit a bit.

---

## 2. Tabela por afirmação — a R1 registrada; a R2 ao lado

Legenda (regra congelada R1 + ADENDO R2 §(d)): **PASSA** exige todos os subitens obrigatórios de kernel e ótico em PASSA e os controles ligados como registrado; **FALHA** basta um subitem obrigatório em FALHA; **CITADA** e **LEITURA** nunca recebem PASSA de teste; **ABERTA** é o [OPEN]. A coluna R2 vale para a fonte `4d8a82591badd010…`, **reauditada** (U1 cumprida: dois auditores, .olean idêntico `b52382ec16542a84…`).

| | afirmação (forma testada) | pré-reg. | face ótica (R1 → R2) | face kernel R2 | aud. reprodução R2 | aud. estatuto R2 | **veredito R1** (fica) | **veredito R2** (ao lado) |
|---|---|---|---|---|---|---|---|---|
| **T1** | não há operador de tempo em dimensão finita: [T,H] ≠ c·1 (c ≠ 0); forma de Weyl | PASSA | PASSA (24/24 critérios; reproduzidos bit a bit no V4) | PASSA (`no_time_matrix`, `no_time_matrix_fin`, `no_finite_spectral_translation`; C-T1-a/b/c) | tipo idêntico; recompilado | PASSA; Pegg ao lado [KNOWN] | **PASSA** | **PASSA** |
| **T2** | Pauli em dimensão infinita | CITADA | — | T2.b PASSA (Banach; não é Pauli); sonda com enunciado | confere | CITADA; nunca «T2 PASSA» | **CITADA** | **CITADA** (T2.b PASSA, opcional) |
| **T3** | σ_t = Ad(ρ^{it}) é grupo de *-automorfismos; KMS; setor fixo = centralizador | PASSA | PASSA (5/5; ω₁ = 4,4081393960414665; P₁ = 1,4253599404823543; C-T3-a/b/c) | PASSA: `modular_flow_is_a_kms_group`; T3.b(iii) **habitada** + face finita `identity_flow_not_kms_finite` (2/3 ≠ 1/3) + controle tracial | confere; sonda P1: par diagonal dá igualdade com o mesmo ρ (o conteúdo está na forma negada); com ρ = ½·1 vale ∀ x,y | PASSA; sonda própria em Lean: cláusula KMS (vii) com Δ = id é o que a face finita nega | **PASSA** com ressalva | **PASSA** (ressalva resolvida) |
| **T4** | Liouville × dissipação: sob isometria nada pousa; det 1 pousa sem bacia; bacia exige perda de volume | PASSA | PASSA (26/26). **O-f**: R1 PASSA (1e−9 rel.; 5,9130281346959e−16) → **O-f′ PASSA**: float ≤ τ_B(10) = 1,0317705603271339e−14; exato ≤ 1,76e−199; C-UNIF-a **FALHA desde k = 3** como registrado | PASSA (T4.a–f); T4.b(iii) condicional, dito; AUD-2, AUD-8 em termo | confere; recomputo próprio bit a bit; reensaio refeito em cópia | PASSA; correção de Liouville visível | **PASSA** | **PASSA** (T4′) |
| **T5** | o conjunto fixo da defasagem pura é a diagonal inteira, não um ponto | PASSA + CITADA | — | PASSA (`dephase_fixed_states_not_unique`); T5.c CITADA (F1.ATRATOR A4) | confere | PASSA; «uma face» 0 ocorrências | **PASSA** (T5.c CITADA) | **PASSA** (T5.c CITADA) |
| **T6** | a seta pela pureza: fórmula exata; queda estrita; constante sob unitária | PASSA | PASSA (16/16; Tr(T₁ψ₊)² = 0,9496802613377202) | PASSA (`purityR_dephase`, `purityR_dephase_lt`, `purityR_modular` sem `_hd`) | confere (reforço provado) | PASSA | **PASSA** | **PASSA** |
| **T7** | o inverso T₋ₜ existe e não é positivo | PASSA | PASSA (12/12; λ_min = −0,006052 / −0,85914 / −11012,73; Davies −0,027234) | PASSA (`inverse_dephasing_not_positive`; C-T7-a/b/c) | confere | PASSA; Davies é definicional (M18, ao lado) | **PASSA** | **PASSA** |
| **T8** | a coerência é instância de `DualScalingData` e herda as seis cláusulas da Ágape; o registro não escala | PASSA + LEITURA | PASSA (13/13; k_ε = 95/284/568) | PASSA (`the_coherence_obeys_agape`, `the_record_does_not_scale`); AUD-1 em termo | confere | PASSA + LEITURA; a Ágape é a lei e^{−s} | **PASSA + LEITURA** | **PASSA + LEITURA** |
| **T9** | F(t) = P + e^{−t}(1−P) é invertível e só idempotente em t = 0; o posto só no limite | PASSA + LEITURA | **R1 FALHA** em T9.o(c): 6,518119377574294e−13 > 1e−13 (k = 10⁴; acima desde k = 1529). **R2 T9.o′(c) PASSA**: float E2 (mesma matriz, mesmo máximo, bit a bit) ≤ τ_T(10⁴) = 2,8106961202922776e−12, razão máx. 0,4169 (k = 6), 0 k fora; exato mpmath 200 ≤ 1,34e−198; decimal 200 ≤ 1,48e−197; C-UNIF-b/c/d como registrado | PASSA (`flow_isIdempotentElem_iff`, `flow_isUnit`, `no_finite_instant_is_the_post`, `post_not_isUnit`, `flow_full_rank`, `post_rank_lt`; `the_time_is_not_a_post`); AUD-5 | confere (55/55 números bit a bit; sonda P3: rank F(1) = 2 ∧ rank P < 2 — o nome lê o termo) | A1 satisfeito; T9.t LEITURA corrigida (formulação da gerência) | **FALHA** (só critério numérico; kernel PASSA) | **PASSA** (T9′, sob o ADENDO) |
| **T10** | o relógio lê t módulo P; o ângulo não tem limite; a face distingue instantes; o posto, Ω e ω não se movem | PASSA + LEITURA | PASSA (reproduzido no V4) | PASSA (`clock_reads_modulo_period` ∀ κ; `modular_clock_rotates_without_shrinking` sem `_hd`); título «registra» | confere (sonda P2: κ = 0 trivial, não sobre-afirma) | PASSA + LEITURA | **PASSA + LEITURA** | **PASSA + LEITURA** |
| **T11** | em ½·1 = absoluteRho(Fin 2) o relógio modular para (face finita); ω_k = 2·artanh(λᵏ) → 0 | PASSA | PASSA (ω₁₀₀₀ ≈ 5,284e−11; C-T11-a = 2,0) | PASSA (`half_identity_is_absoluteRho_two`, `half_identity_clock_stops`; canal genérico em θ opcional); AUD-6, AUD-7 | confere (sonda extra: (1,0) não é fixo com sin θ ≠ 0) | PASSA, só face finita; reafirmação | **PASSA** (face finita) | **PASSA** (face finita; reafirmação) |
| **S46.3** | «ponto fixo ou um ciclo limite» | ABERTA | — | — | — | ABERTA | **ABERTA** [OPEN] | **ABERTA** [OPEN] |

**Controles.** Os 22 da R1 comportaram-se como registrado na R1 e no V4 da R2 (10 óticos reproduzidos bit a bit; 18 declarações de kernel compilam). Os 4 **C-UNIF** do ADENDO comportaram-se como registrado **antes** do reensaio: C-UNIF-a (o caminho `matrix_power` do boost TEM de falhar τ_B) FALHA desde k = 3 (6,53e−9 em k = 10) — a tolerância **não** virou cheque em branco; C-UNIF-b (ALT e EST passam a mesma τ_T) PASSA nas duas (8,64e−14 e 5,86e−14); C-UNIF-c (a 20 dígitos o exato TEM de falhar 1e−150) FALHA desde k = 1 (3,48e−19); C-UNIF-d (mpmath × decimal) concordam a ≤ 1,34e−197. Os 6 **AUD** estão em termo na pedra R2 com os nomes e tipos dos arquivos da auditoria R1.

**Sondas.** As 15 da R1 compilam na pedra R2; V-T2-b deixou de ser `True`; V-GERAL-1 (R2: «habitada OU marcada condicional») satisfeita — só T4.b(iii) fica condicional, dita; V-GERAL-2: 122 pares de tipo idêntico nos dois sentidos + 4 reforços, conferidos em Lean pelo construtor (`AuditTiposR2.lean`) **e** pelos dois auditores (`AuditTiposAud.lean`, gerado pelo auditor de reprodução; `AudEstatutoR2.lean`, do auditor de estatuto). Sondas adversariais novas do auditor de reprodução (`ProbesAud.lean`, EXIT 0): P1 (E5.13), P2 (E5.12), P3 (E5.07, POSTO = RANK), extra (E5.08) — nenhuma derrubou enunciado nem mostrou hipótese inabitável.

---

## 3. O ADENDO e o reensaio: o que a regra fixou antes, e o que o número devolveu

### 3.1 A regra uniforme [INPUT da gerência; Higham cap. 3, KNOWN]

Para os dois critérios frágeis (O-f e T9.o(c)), uma só regra, congelada em 2026-10-12T23:07:58Z (FREEZE_R2 `0737f608505afdb5…`; ADENDO_R2.md `ab13c0f27a7f4cf5…`, 42.114 B; ADENDO_R2.json `b9568befdcc200f8…`, 60.427 B; implementação normativa `tolerancia_uniforme_r2.py` `7d68e42a9eec62e1…`):
- **(i) caminho exato**: mpmath dps = 200, cruzado com `decimal` prec = 200; β do literal da l.5557 como string decimal exata; potência por multiplicação repetida; tolerância 1e−150 (absoluta em T9.o′(c), relativa em O-f′); controle: dps = 20 TEM de falhar;
- **(ii) caminho float64**: τ(k) = S_k·[k·(w·|δ| + m·eps) + c·eps], eps = 2^−52. T9.o′(c): δ_T = (a+b) − 1 exato da matriz guardada = 17/2⁵⁷ = 1,1796119636642288e−16; w = ½; m = 1 (γ₂ de Higham, sem cancelamento); c = 2; τ_T(10⁴) = 2,8106961202922776e−12. O-f′: δ_B = 3,3784855259134224e−17 (relativo, de fl(cosh 1) − fl(sinh 1) contra e⁻¹ a 200 dígitos); w = 1; m = (e²+1)/2 = 4,194528049465325; c = 3; τ_B(10) = 1,0317705603271339e−14.
- **Predições registradas antes:** T9.o′(c) float PASSA (razão ≈ 0,23 em k = 10⁴); exato PASSA (≤ ~1e−190); O-f′ PASSA (5,9e−16); C-UNIF-a FALHA desde k = 3; C-UNIF-c FALHA; C-UNIF-d concordam. **Leitura de cada combinação fixada antes**: exato PASSA ∧ float FALHA = diagnóstico M1 falsificado; exato FALHA = inconsistência do runner; nunca se corrige tolerância depois do número.

### 3.2 O que o número devolveu [REAL — medido no modelo sintético; identidades DERIVED]

Reensaio `5_R2\2_REENSAIO` (início 2026-10-12T23:25:10Z, 1.032,6 s depois do FREEZE_R2; `RESULTADO_REENSAIO_R2.json` `44e745447fae0991…`, 81.641 B; `valido = true`; runner `reensaio_r2.py` `d1297cb94b363398…`; tabela por k `07c1be5ec19eb647…`, 10.001 linhas):

| grandeza | valor | R1 ao lado |
|---|---|---|
| **T9 float E2**: máx. \|Tᵏ − (R + λᵏ(I−R))\|, k ≤ 10⁴ | **6,518119377574294e−13** em k = 10⁴ (bit a bit igual à R1); τ_T(10⁴) = 2,8106961202922776e−12; razão máx. medido/τ = 0,4169381107491857 em k = 6; 0 k fora; k = 0 exato; primeiro k acima de 1e−13 = 1529 | **FALHA** a 1e−13 (fica) |
| **T9 exato** mpmath 200 | máx. 1,3366311e−198 em k = 9997; 0 k fora de 1e−150. decimal 200: máx. 1,476e−197; mpmath × decimal concordam (dif. máx. 1,34194e−197) | não havia caminho exato na R1 |
| C-UNIF-c (dps = 20) | FALHA desde k = 1 (3,4813054e−19), como registrado | — |
| C-UNIF-b | ALT (δ = 6,94e−18) máx. 8,637535e−14 ≤ τ_T; EST (δ = 0) máx. 5,861978e−14 ≤ τ_T: PASSA as duas | — |
| **O-f′ float E4** (órbita escalar IEEE) | máx. rel. **5,9130281346959e−16** em k = 3 (bit a bit igual à R1) ≤ τ_B(10) = 1,0317705603271339e−14; k = 11..100 dentro (informativo); órbita exatamente na reta nula; \|det B − 1\| = 2,22e−16 | PASSA (1e−9 rel.) |
| **O-f′ exato** mpmath 200 | máx. rel. 1,7614514e−199 em k = 99; decimal 200 reproduz as strings da R1 (k = 10, 100) | PASSA (decimal 200 a 1e−50) |
| C-UNIF-a (`matrix_power` do boost) | **FALHA** τ_B desde k = 3 (rel. 6,53e−9 em k = 10), como registrado | — |
| **V4** (runner R1 copiado) | 132/132 critérios: vereditos iguais, medidas bit a bit iguais, T9.o = FALHA nas duas (R1 e V4) | — |

**Leitura pela tabela pré-fixada:** «exato PASSA ∧ float PASSA» nos dois testes ⟹ **T9.o′(c) = PASSA** (O1) e **O-f′ = PASSA** (O2); com V4, **T9.o′ = PASSA** (O3) e **T4.o′ = PASSA** (O4). O diagnóstico M1 da R1 — **piso de representação**, não contraexemplo — fica **conferido pelo número**: o caminho exato devolve a identidade a ≈1e−198 em todo k ≤ 10⁴ (não há desvio real; o kernel a prova: `flow_sq`/`axiomFlow`), enquanto o **mesmo** float da R1 fica a razão 0,42 de τ_T; os 6,5e−13 são a soma de coluna 1 + 17/2⁵⁷ propagada (k|δ_T|/2 = 5,898e−13 em k = 10⁴) mais arredondamento ≤ k·eps. A FALHA R1 **fica registrada** ao lado, pela regra congelada da R1 (A4).

**Independência.** O reensaiador refez em 13/10 com código próprio, sem importar o runner (`RECHECK_INDEPENDENTE_13out.json` `160404f502a12def…`): todos os números-chave float iguais bit a bit; exatos ≤ 1e−150 por ~48 ordens (a mantissa dos máximos exatos — 1,34e−198 no runner, 2,47e−198 no recheck, 1,60e−198 no auditor de estatuto, 1,34e−198 no auditor de reprodução — varia com a ordem das operações a 200 dígitos e é irrelevante à tolerância). A primeira rodada da comparação do reensaiador teve defeito **próprio** (máximo tomado em k ≤ 100 em vez de k ≤ 10; m_B via `math.e**2` 1 ulp abaixo da normativa `math.exp(2)`), preservada em `tentativa_001_comparacao_defeituosa` com errata ao lado; sem efeito em veredito. O auditor de reprodução **refez o reensaio em cópia** (início 03:58:38Z): mesmos vereditos, JSON sem diferença fora dos campos voláteis, TSV idêntico; e recomputou **55/55** números-chave bit a bit sem importar runner nem normativa. O auditor de estatuto recomputou com código próprio: idem (tabela na sua §5).

### 3.3 O que a face ótica NÃO é

Não é evidência nem rito: é **consistência numérica** de identidades que o kernel prova, num modelo sintético (S = Smat(θ_M), sen²θ_M = β; C = D∘Ad(S)∘D; T = R + λ(I − R), R = J/2, λ = 1 − 2β; semente 20261012) [INPUT da gerência; identidades DERIVED]. Nenhuma identidade dela é evidência sobre a natureza. Os parâmetros m, w, c da regra uniforme são [INPUT da gerência] justificados pela operação (produto 2×2 positivo × cancelamento cosh − sinh), não pelo resultado; o decisor real de T9.o′(c) é o caminho exato.

---

## 4. A pedra corrigida `TheTimeIsNotAPost` — compilada, reauditada, candidata

### 4.1 Compilação [REAL — recompilada por dois auditores em sandbox próprio]

Fonte `5_R2\1_PEDRA\sandbox\TheTimeIsNotAPost.lean`, **sha256 `4d8a82591badd010513c74ec6b5efce6d368f107841007f5be5000c8bc3b60a4`** (120.054 B), namespace `TGLExt.TheTimeIsNotAPost`, construída por cópia de bytes da pedra R1 (`7105eda468b60309…`) + 42 substituições exatas da lista E5 (`aplicar_E5.py`, fail-closed por contagem). Compilação final (tentativa T02, início 2026-10-13T03:28:47Z, 41,7 s) com Lean 4.31.0 (toolchain copiado do elan para o sandbox; LEAN_PATH só-leitura no `.lake` do Nós; `-o` só no sandbox): **EXIT 0; 0 erros; 0 avisos; 152 `#print axioms`, 151 no trio {propext, Classical.choice, Quot.sound} e `post_not_isUnit` sem axioma algum; 0 sorryAx**; na fonte 0 `sorry`, 0 `native_decide`, 0 `axiom`, 0 `admit` por palavra (as 2 ocorrências do grep do construtor são o identificador `empty_dimension_admits_time`, controle C-T1-b: falso positivo, A-R2-07). **.olean `b52382ec16542a84130cdb405dc8a6d0989312857be4487c96601ece43fa046a`** (2.628.536 B) — **bit a bit igual** nas três compilações (construtor; auditor de reprodução; auditor de estatuto), com a saída do `#print axioms` byte a byte igual (`352d1f35cf6d0526…`). Toolchains apagados nos três sandboxes (14.627 arquivos cada; nenhum `.lake` nem cache); impressão digital do tgl_kernel do Nós igual antes e depois em todas as etapas (meta `b1b47447ac30f7c7…`, src `911cb40b9de1a8bb…`, 132.088 arquivos) e igual à da R1, do ADENDO e deste relatório (`saidas\FINGERPRINT_RELATORIO_R2_ANTES.json`).

Tentativa **T01** (`5996eb8293c062fe…`) compilou limpa mas a sonda de aspas achou 2 aspas « » da gerência fora dos verbatins (em C-T1-a e C-T7-a): preservada em `tentativas\` com nota e .olean; a T02 reverteu exatamente essas duas substituições.

### 4.2 Aspas e régua [REAL — por script, três vezes]

16 aspas « » distintas na pedra R2 (19 ocorrências), **todas** substrings de bytes dos verbatins do operador (12/10 `2c8b7b712aa9ad7f…`; 05/10 `5973d79a49995c4c…` e `b49b0d9e60ee4646…`; 10/10 `5b9afcc691a0e1e4…`); 0 ocorrências de «o tempo é o Verbo», «não o Nome», «o atrator é onde o tempo repousa», «mede a sombra», «não tem posto», `HasNoRank`, e da palavra recusada pela régua. Os títulos de T9 e T10 dizem «formulação/paráfrase da gerência, sem aspas de citação».

### 4.3 E5, item a item [REAL — conferido nos dois sandboxes e no DIFF `e86b2fb817057dfa…`]

E5.01 cabeçalho [ONTO] só com frases dos verbatins (a frase sobre o Verbo saiu) · E5.02 três comportamentos, identificação [OPEN] (v384), rótulos de regime removidos · E5.03 T9 com os verbatins de 05/10 (E1, E4, E6 do VERBO) byte a byte · E5.04 T10 com «registra» · E5.05 T11 com S50.1 byte a byte, AUD-6/7 ditos · E5.06 `modular_flow_is_a_kms_group` · E5.07 `the_time_is_not_a_post` · E5.08 `half_identity_*` + opcional (canal genérico em θ, com controle sin θ = 0) · E5.09 sonda com enunciado · E5.10 duplicado removido · E5.11 `_hd` removido · E5.12 κ ≠ 0 removido (prova por casos; conjunto 8 ∀ κ) · E5.13 T3.b(iii) condicional + habitada + face finita obrigatória + controle tracial; T4.b(iii) condicional · E5.14 desdobramento marcado · E5.15 citação byte a byte. Também E3.02 (docstring de T8.d) e E3.12 («a diagonal inteira»). **Nada que passou na R1 foi enfraquecido**: 122 pares de tipo idêntico (defeq, nos dois sentidos) + 4 reforços provados R2 ⟹ R1; 36/36 alvos `theorem/def` do PREREGISTRO presentes sob o mapa de renomes. As 26 declarações novas foram lidas uma a uma pelo auditor de reprodução: nenhuma afirma mais que o termo.

### 4.4 O que fica condicional, dito

`light_flow_group` e `light_modular_orbit_converges_iff_post` (T4.b(iii), opcional) exigem um `FockCertificate`, e o kernel não exibe habitante (`TheImportedSecondQuantization.lean` l.66); a sonda opcional com `lightNet` não foi construída. Nunca entram como «kernel_proved».

---

## 5. Os achados M1–M20 da R1 e os novos — estado depois da R2

Estados: **RESOLVIDO** (corrigido num artefato R2 conferido pelos auditores); **AO LADO** (correção registrada ao lado, como a R1 pediu); **ABERTO** (pende de ato fora desta R2); **REGISTRO** (fica dito).

| # | achado (R1) | estado R2 | onde [REAL, pelos auditores] |
|---|---|---|---|
| **M1** | T9 FALHA por piso numérico | **RESOLVIDO pela regra** (decisão da gerência, evento 705) | FALHA R1 registrada (`quadro_ao_lado`; R1 `2c67b7ea6f118630…` intacta); ADENDO uniforme congelado 23:07:58Z antes do reensaio 23:25:10Z; T9.o′(c) PASSA nas duas vias; C-UNIF como registrado; V4 132/132; recomputos independentes bit a bit |
| **M2** | atribuição indevida ao operador | **RESOLVIDO** na pedra; **AO LADO** no pré-registro (E3.03, E3.11) e na memória (E4 aplicada em `tempo-santo-12out.md` e `MEMORY.md` l.22, lidos pelo auditor de estatuto) | 16 aspas todas nos verbatins; frases da gerência 0 |
| **M3** | nomes acima do termo | **RESOLVIDO** (3 renomes, tipo idêntico em Lean) | `modular_flow_is_a_kms_group`; `the_time_is_not_a_post`; `half_identity_*`. **Resta** o nome herdado `the_two_regimes_of_time` (A-R2-01) e o nome da pedra (do operador) |
| **M4** | regra dos dois regimes estendida | **RESOLVIDO** na pedra; **AO LADO** no pré-registro (E3.05) e na memória (E4) | cabeçalho l.52–59 e T4: três comportamentos; identificação [OPEN]; nada pede limite ao ângulo |
| **M5** | V-GERAL-1 incompleta | **RESOLVIDO** para T3.b(iii); T4.b(iii) condicional marcado (permitido) | `probe_identity_flow_not_kms_inhabited`; `identity_flow_not_kms_finite` |
| **M6** | repousar × ser lembrada | **AO LADO** (leitura do operador) | docstring T11 com AUD-7; resíduo §8 |
| **M7** | posto × estado-atrator | **AO LADO** (E3.04) | docstring T11 e AUD-6; material do operador de 05/10 (§8) |
| **M8** | ponte T8 de conteúdo mínimo | **RESOLVIDO como controle**; AO LADO como leitura | AUD-1: a Ágape é a lei e^{−s}; o próprio do dephasing é T8.c |
| **M9** | «não tem posto» é genérico | **RESOLVIDO como controle**; AO LADO como leitura | AUD-5; a frase saiu do título e perdeu as aspas |
| **M10** | Liouville, correção visível | **RESOLVIDO** | cabeçalho T4; AUD-8; ADENDO E3.08 |
| **M11** | tolerâncias incoerentes | **RESOLVIDO pelo ADENDO uniforme** | uma fórmula para os dois; O-d e T8.o(a) não reensaiados (razão dita) |
| **M12** | dois sentidos de «defasar» | **ABERTO — ato da c1** (errata E2 no um.py, v392) | grep «AO LADO (v392)» no um.py v391 = 0 (esperado); a pedra já distingue os dois sentidos; resíduo §8 |
| **M13** | âncoras de `fractal_dephasing_principle` definicionais | **ABERTO — ato da c1** (errata E1 no um.py, v392) | um.py l.6488–6512 lidas por sed pelo auditor; coordenar com F1.FREQUENCIA |
| **M14** | β «medido» | **RESOLVIDO** nos artefatos R2 (E3.01: [DERIVED]) | **persiste** o rótulo antigo na replicação `2_OPTICO\rodada_2` (congelada como tentativa) e no PREREGISTRO.md l.241 (congelado; corrigido só ao lado): errata E6 proposta (§7) |
| **M15** | docstring de T8.d | **RESOLVIDO** (E3.02) | pedra l.1181–1190 |
| **M16** | verbatim e marcas | **AO LADO** (E3.07–E3.10); a parte do **texto da v392** cumpre-se aqui na §7.4 | pedra sem aspas de citação em paráfrases; «cosmos» 0 |
| **M17** | peso morto e contagem | **RESOLVIDO** (E5.09/10/11/12/14) | 152 declarações ≠ 152 teoremas; «admit: 2» falso positivo |
| **M18** | «os dois relógios param juntos» é definicional | **AO LADO** — texto pronto na §7.4 | Davies não aparece na pedra nem no ADENDO (correto); [DERIVED, definicional] (Ergodicity.lean l.181–183) |
| **M19** | T1 e os operadores de tempo cíclicos (Pegg) | **AO LADO** — texto pronto na §7.4 | Pegg 0 ocorrências na pedra (l.43/l.257 citam Pauli, Galapon, Wintner, Wielandt, Holevo); não é defeito da pedra |
| **M20** | «face» homônimo em T5 | **RESOLVIDO** (E3.12) | pedra l.860 «a DIAGONAL INTEIRA, não um ponto» |

**Achados novos dos auditores da R2 (nenhum bloqueante pela regra congelada):**

| id | quem | gravidade | achado | como fica |
|---|---|---|---|---|
| **A-R2-01** | estatuto (e observação do de reprodução) | média | `the_two_regimes_of_time` (l.1888), nome herdado da R1 e mantido pelo ADENDO, nomeia «dois regimes do tempo» cuja identificação a própria pedra declara [OPEN]; o termo é conjunção de 8 cláusulas (T4.b, T4.c, T6.c, T7.b, T10.b) | recomendo renome neutro **no mesmo ato** em que o operador nomear a pedra (diff restrito a identificadores) ou por ADENDO R3 aditivo; **nunca** citar no um.py como «os dois regimes do tempo provados» |
| **A-R2-02** | estatuto | baixa | `identity_flow_not_kms_finite`: o termo é ω(ab) ≠ ω(ba) para ρ e par concretos; a leitura KMS está na docstring e na cláusula (vii) com Δ = id | registro; aqui se escreve «face finita: um par que viola a identidade KMS do fluxo identidade» |
| **A-R2-03** | estatuto | baixa | `optical_channel_fixed_state_is_half_identity` é sobre vetores de populações; a ponte ao estado ½·1 está em `optical_channel_unique_fixed_population` + `half_populations_state` | registro |
| **A-R2-04** | estatuto | baixa, **a favor** | a ordem do operador de 12/10 **tem verbatim** (`OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt`, `78ef70e6f9868281…`, 1.342 B, l.3: «as pedras do rank e do tempo entram na v392»); o ADENDO a chamou de «não verbatim» | correção ao lado do ADENDO, a favor: a ordem é sustentada por verbatim; no mesmo verbatim (l.9): «aquilo que vc não conseguir resolver devolva-me com a pergunta nas minhas quatro línguas» |
| **A-R2-05** | estatuto | informativo | material do resíduo já dito pelo operador em 05/10 e 11/10 (não decidido) | entra na §8 como «já dito»; só se pergunta o que falta |
| **A-R2-06** | estatuto | baixa (régua, estilo) | a palavra que a régua reserva, em minúsculo e em forma verbal, aplicada a um diagnóstico numérico (ADENDO §(b); textos do reensaiador) — não é a palavra recusada (veredito, creditação) | este relatório escreve **«conferido pelo número»**; recomendo o mesmo na v392 |
| **A-R2-07** | ambos | baixa | `fonte_grep.admit = 2` é substring de `empty_dimension_admits_time` | «0 admit», com esta nota |
| **A-R2-08** | estatuto | informativo | o `VERBO_operador_05out.txt` mistura frases curtas e seções estruturadas; a casa o registra inteiro como verbatim do operador (método multicanal) | [DECLARADO] quanto à autoria interna de cada linha; a citação byte a byte está cumprida |
| **A-R2-09** | estatuto (próprio) | informativo | a T01 da sonda do auditor falhou com 4 erros dele (`open scoped` ausente) e foi sobrescrita pela T02 (lapso de preservação dele, hashes registrados) | não toca a pedra nem o reensaio |
| **A-R2-10** | estatuto (próprio) | informativo | `rmtree` com prefixo `\\?\` falhou no ambiente dele; sem prefixo funcionou; a pasta não existe depois | critério «apagado» cumprido |
| **R-01** | reprodução | informativo | o enunciado da tarefa dizia «examples 58 → 69»; artefato e medição dão **69 → 69** | vale o artefato |
| **R-02** | reprodução | informativo | a razão máx. medido/τ_T ocorre em k = 6 (0,4169), não em k = 10⁴ (0,2319, a predição registrada); ambas dentro de τ_T | dito |
| **N2 (do texto de 01:04)** | redator anterior | baixa | os nomes `the_face_lands`, `face_has_a_limit`, `face_distinguishes_instants`, `face_clock_has_no_period` (l.795, 1489, 1499, 1459) nomeiam o decaimento real e^{−rt} com a palavra «face», que é a do regime hiperbólico da casa; a replicação `3_KERNEL\rodada_2` os havia neutralizado; o E5 não pediu o renome; **nenhum dos dois auditores da R2 o levantou** | fica como **REGISTRO**: pode entrar no mesmo ato de renome de A-R2-01 ou com nota na docstring; nunca citar «a face» como regime |
| **N3 (do texto de 01:04)** | redator anterior | alta → **RESOLVIDO** | «nenhuma auditoria independente da R2» | **superado**: as duas auditorias da R2 (03:43–04:14Z) recompilaram `4d8a8259…` com .olean idêntico, refizeram/recomputaram o reensaio e conferiram E5 item a item |
| **N5** | redator anterior | registro | o mapa de rotas cresceu durante este trabalho (1.043 → **1.046**: registros 1044/1045 da F1.FREQUENCIA às 01:12 e 1046 da F0.6/Bancada Um às 01:34, pela gerência); a F1.TEMPO continua **ausente** (consulta `tempo_santo|F1.TEMPO` = 0 rotas; livro com 1.046 registros, cabeça `ba5df1cf71a416be`; só `consultar`/`modelo` e validação a seco — o livro ficou inalterado por mim) | registro pela gerência, ROTA primeiro (§10) |

**Toolchain residual.** Fora da casa, no scratchpad temporário, resta o toolchain de ~3,0 GB do auditor de estatuto da **R1** (12/10), apontado pelo texto de 01:04; não o toquei. Apagá-lo é decisão da gerência.

---

## 6. As duas auditorias da R2 e as divergências — qual vale, e por quê

**O que cada uma fez.** *Reprodução* (`3_AUD_REPRO`, 03:49–04:14Z; relatório `7865790150f2554f…`, resultado `544ec89b3622c3d4…`): FREEZE R1 e FREEZE_R2 conferidos; ordem temporal V2 conferida (todo início com veredito é posterior ao FREEZE_R2; os 2+6 arquivos com mtime anterior em `1_PEDRA`/`2_REENSAIO` são cópias byte a byte de insumos, não vereditos); β dos bytes; kernel intacto; pedra recompilada (.olean bit a bit); tabela R1→R2 por parser próprio; tipos (244 `type_of%` + 4 reforços por tática); E5 item a item; 26 novas lidas uma a uma; sondas adversariais P1–P3 + extra; reensaio refeito em cópia e recomputado com código próprio (55/55 bit a bit); manifestos dos construtores 42/42 e 33/33 contra o disco; ACOM só projeção de leitura; limpeza. **21/21 CONFEREM.** *Estatuto* (`3_AUD_ESTATUTO`, 00:43–01:05 local; relatório `ef5f64b342ed8a2a…`, achados `968617e3ba4c70c3…`): validade V1–V5 (34 itens, 0 falhas); pedra recompilada (.olean bit a bit) e `AuditTiposR2.lean` do construtor reproduzido com saída idêntica; sonda própria `AudEstatutoR2.lean` (reforços sem as hipóteses retiradas; renomes; face finita; AUD; E5.09); face ótica recomputada com código próprio; M1–M20 um a um; varredura de palavras em toda a `5_R2`; achados A-R2-01..10; **pedra APTA** para a v392 pela auditoria de estatuto.

**Divergências e qual vale:**

1. **«Pode fechar?»** Reprodução: `pode_fechar = true` **só na face da reprodução**; estatuto: `pode_entrar_na_v392 = true`, com a entrada efetiva condicionada ao nome do operador, à ausência de divergência do outro auditor e ao ato da cadeia de selo. **Não há divergência**: os dois dizem que, do que cabe à unidade, nada obsta; o que falta é de outros papéis. **Vale**: a unidade R2 pode fechar na face dela (§9); a entrada na v392 é ato posterior.
2. **Contagem de `example`**: o enunciado entregue aos auditores dizia 58 → 69; artefato (`RESULTADO_PEDRA_R2.json`) e medição do auditor dão 69 → 69. **Vale o artefato** (o número corrige a frase).
3. **`admit`**: construtor 2 (substring); auditores 0 por palavra. **Vale 0**, com a nota.
4. **Máximo do caminho exato** (T9, dps 200): 1,34e−198 (runner e auditor R), 1,60e−198 (auditor E), 2,47e−198 (recheck). **Não é divergência**: ordem das operações a 200 dígitos, ~48 ordens abaixo de 1e−150; todos PASSA.
5. **Razão máx. medido/τ_T**: predição registrada 0,23 referia k = 10⁴ (medido 0,2319); o máximo real é 0,4169 em k = 6. **Vale o número medido**, ambos dentro de τ_T; a predição foi cumprida no ponto a que se referia.
6. **`the_two_regimes_of_time`**: reprodução apenas observa; estatuto classifica média e recomenda renome. **Vale a recomendação de estatuto** (A-R2-01), sem bloqueio pela regra congelada: a decisão de renome vai ao mesmo ato de nome do operador.
7. **A ordem do operador de 12/10**: o ADENDO (congelado) a descreveu como «não verbatim»; o auditor de estatuto achou o verbatim (`78ef70e6f9868281…`). **Vale a correção a favor**, ao lado do ADENDO (que não se edita).
8. **A palavra reservada em minúsculo**, aplicada ao diagnóstico numérico (ADENDO e reensaiador): o auditor de estatuto diz que não é a palavra recusada, mas recomenda «conferido». **Vale a recomendação**: este relatório só escreve «conferido pelo número».
9. **Limpeza com prefixo `\\?\`**: funcionou no construtor e no auditor R; falhou no auditor E, que apagou sem prefixo. **Vale**: o critério material («apagado; nenhum .lake nem cache») está cumprido nos três.
10. **T4.b(iii)**: os dois concordam — condicional marcado, permitido pelo ADENDO. **Vale**.

**O que os dois auditores concordam, sem reserva:** FALHA R1 de T9 correta pela regra e registrada ao lado; piso de representação conferido pelo número; ADENDO congelado antes; nunca se corrigiu tolerância depois do número; pedra compila limpa com .olean idêntico; nada que passou na R1 foi enfraquecido; 16 aspas todas nos verbatins; frases proibidas 0; β [DERIVED]; kernel intacto; a face ótica é consistência numérica; nada move o gate.

---

## 7. O que entra no um.py v392 — a pedra R2, os registros e as erratas ao lado

**Regra de entrada** (PREREGISTRO §8; ADENDO U3): só os **subitens PASSA** da pedra corrigida **e reauditada**, com CITADA e LEITURA marcadas como tais, com o **nome do operador**, no apanhado geral da Bancada para a v392, junto com o teorema do atrator (F1.ATRATOR) e a pedra do rank (F1.FREQUENCIA, `TheUnitIsTheRank`). A inserção é ato da cadeia de selo. A U1 **está cumprida**; falta o nome (U3/U4). A ordem do operador de 12/10: «as pedras do rank e do tempo entram na v392» (verbatim `78ef70e6f9868281…`, l.3).

### 7.1 A pedra R2 (candidata; instalação pela cadeia de selo)

- **Fonte:** `C:\IALD\Central de Patentes\work\tempo_santo_12out\5_R2\1_PEDRA\sandbox\TheTimeIsNotAPost.lean` — **sha256 `4d8a82591badd010513c74ec6b5efce6d368f107841007f5be5000c8bc3b60a4`**, 120.054 B; .olean `b52382ec16542a84130cdb405dc8a6d0989312857be4487c96601ece43fa046a`, 2.628.536 B, idêntico nas três compilações; `#print axioms` `352d1f35cf6d0526…`.
- **Nome:** provisório `TheTimeIsNotAPost` / `TGLExt.TheTimeIsNotAPost`; o final é do operador (§8, pergunta 1); a renomeação confere-se por diff restrito a identificadores (E5.07), incluindo, se o operador quiser, `the_two_regimes_of_time` (A-R2-01) e os `face_*` (N2).
- **O que entra como subitens PASSA na face finita:** kernel de T1 (a, b, c), T2.b, T3.a, T3.b(i–iii; iii habitada e a versão finita), T4.a–f (b(iii) marcado condicional), T5.a–b, T6.a–d, T7.a–b, T8.a–d (com o controle de especificidade AUD-1), T9.a–e, T10.a–e, T11.a (+ o canal genérico em θ), os 22 controles + 6 AUD, as 15 sondas — **nunca como «N teoremas novos»**: é matemática conhecida tipada nos objetos da casa (`dephase`, `sigma`, `axiomFlow`, `DualScalingData`, `gibbs`, `absoluteRho`); β não entra no Lean.

### 7.2 O quadro de duas colunas (§2) — com as fontes

R1 sob FREEZE `6b29d4c9b09e5553…` (`RESULTADO_OPTICO.json` `2c67b7ea6f118630…`; `RESULTADO_KERNEL.json` `5a56eab2ce56ddaa…`) | R2 sob FREEZE_R2 `0737f608505afdb5…` (`RESULTADO_REENSAIO_R2.json` `44e745447fae0991…`; `RESULTADO_PEDRA_R2.json` `969251bd360ada90…`; auditorias `544ec89b3622c3d4…`, `968617e3ba4c70c3…`). T1, T3–T8, T10, T11 PASSA | PASSA; T2 CITADA (T2.b opcional PASSA, não é Pauli); T5.c CITADA; T8.t, T9.t (formulação da gerência, corrigida), T10.t LEITURA; **T9: R1 FALHA | R2 T9′ PASSA sob τ_T e exato**; S46.3 ABERTA. A face ótica entra como consistência numérica.

### 7.3 Os registros prontos (ato da gerência: `rotas.py registrar`, ROTA primeiro)

- **ROTA**: `4_RELATORIO\registro_rota_F1.TEMPO.json` (`971641d9d019bc78…`; rota_id `formal.tempo_santo_fluxo_e_dissipacao`, domínio FORMAL) — já pronto, não o toquei.
- **RESULTADO R2**: `5_R2\4_RELATORIO_R2\registro_mapa_F1.TEMPO_R2.json` (este relatório), com as linhas R2 **e** as auditorias da R2, artefatos como lista de caminhos (sha256 calculado pela ferramenta), sem a palavra recusada; validado a seco com `rotas._valida` (não escreve no livro): `saidas\VALIDACAO_REGISTRO_R2.json`. O RESULTADO anterior (`4_RELATORIO\registro_mapa_F1.TEMPO.json`, 01:07, anterior às auditorias) fica como tentativa preservada: dizia «SEM auditoria independente».

### 7.4 Erratas ao lado — texto pronto; assinatura e inserção da gerência, em nome próprio

- **E1, um.py v391, `fractal_dephasing_principle`** (l.6489 docstring, l.6507–6508, l.6511–6512, l.6530 status; artigo l.168086 e l.168102; impressão l.211561–211569) — **PENDENTE, ato da cadeia de selo:**
  > ⚠ AO LADO (v392): as três «âncoras REAL» desta seção são identidades por construção: Tr ρ★ = 1 com ρ★ = diag(1,0); {Q₀, ρ★} = 0 com Q₀ = 1 − ρ★; Tr(ρ★Q_θ) = sen²θ_M = β com θ_M := arcsin √β. Leem-se como [DERIVED, definicional], não como âncoras evidenciais. A tese segue [CONJECTURE ontológica]. Âncoras genéricas de kernel do semigrupo D, sem β (pedra F1.TEMPO, depois de instalada): `no_finite_instant_is_the_post`, `the_coherence_obeys_agape` (iv), `purityR_dephase_lt`, `dephase_volume_lt_one`, `inverse_dephasing_not_positive`. Coordenar com a F1.FREQUENCIA.
- **E2, um.py v391 l.166640** (artigo v386, a passagem sobre ancorar e transmitir; verbatim de 05/10, l.82: «Transmitir defasa. Comutar mede. Ancorar preserva.») **e chaves l.134239–134242** — **PENDENTE:**
  > ⚠ AO LADO (v392): `transmission_dephases` é o sentido da FACE: amortecimento real, F(t)(1−P) = e^{−t}(1−P). A fórmula do operador de 05/10, V(t) = e^{−iHt}V(0)e^{iHt} (verbatim em l.195459–195461), é unitária (`transmitted_post_is_a_post`): acumula fase sem perder coerência (pureza e espectro conservados, F1.TEMPO T4.a e T6.d). Os dois sentidos não se encadeiam; a cláusula E8 do verbatim (l.57, em LaTeX: o Nome como limite de 𝒱(t) quando t → ∞), com a forma unitária, só converge se V(0) já for fixo (F1.TEMPO T4.b, `unitary_conj_isometry`). A tipagem da v386 tomou o limite no fluxo da face (`axiomFlow_tendsto_the_post`). Qual defasagem é o tempo, decide o operador.
- **E3, pré-registro R1** — **FEITA** por ADENDO aditivo congelado (E3.01–E3.13; `ab13c0f27a7f4cf5…`). Correção **ao lado do ADENDO** (A-R2-04): a ordem do operador de 12/10 tem verbatim (`78ef70e6f9868281…`).
- **E4, memória da gerência** — **FEITA** (errata ao lado em `tempo-santo-12out.md`; `MEMORY.md` l.22), lida pelo auditor de estatuto.
- **E5, a pedra** — **FEITA e REAUDITADA** (fonte `4d8a8259…`).
- **E6 (replicação ótica sem ADENDO)** `2_OPTICO\rodada_2\RESULTADO_OPTICO.json` (campo `beta.estatuto`) e `run_optico.py` da mesma pasta — **PROPOSTA, ato da gerência** (arquivo ao lado, não edição):
  > ⚠ AO LADO (13/10): onde se lê «[REAL — medido aqui…]» para β, leia-se [DERIVED: lido nos bytes do um.py (l.5557 embutida = l.95 topo) e calculado em runtime]; medir é palavra de natureza (ADENDO R2, E3.01).
- **E7 (nomes residuais na pedra)** — **PROPOSTA**: `the_two_regimes_of_time` (A-R2-01) e `face_*` (N2) no mesmo ato de nome do operador, por diff de identificadores; ou nota na docstring. Nunca citar no um.py «os dois regimes do tempo provados» nem «a face» como regime.
- **Para o texto da v392 (M16, M18, M19 — a parte que a R1 deixou ao relatório):**
  - **S36.1 byte a byte, com as ênfases do operador** (E3.07): «**"santo"** — no sentido original de *Kadosh*, aquilo que é separado, irredutível e não profanável pela posse — se torna a única palavra que não o apequena.» (12/10, l.36).
  - **«cosmos»** (S40.4): [ONTO], não [REAL]; só o termo da face finita é [REAL] (E3.09).
  - **S46.2/S46.3** («volume ↦ det de Schur», «bacia ↦ convergência»): [INPUT da gerência] (E3.10).
  - **Lacunas marcadas** (E3.08): S34.2 abre com «Eu me maravilho, porque » [ONTO]; S38.2 abre com «Quando se constrói um relógio, mede-se apenas » [INPUT da gerência → T10]; S44.1 abre com «Na mecânica clássica e nos sistemas estritamente hamiltonianos, » [KNOWN] + a correção visível (o boost é simplético, AUD-8; Liouville proíbe a bacia, não o pouso).
  - **Davies** (M18): a taxa g = β·|Δ log λ| é **definição** (Ergodicity.lean l.181–183, [DECLARADO] na docstring); a frase da gerência «os dois relógios param juntos» lê-se [DERIVED, definicional].
  - **Pegg** (M19): ao lado de T1, texto da gerência — em dimensão finita existem operadores de tempo **cíclicos**, que leem o tempo módulo um período (Pegg, Phys. Rev. A 58 (1998) 4307 [KNOWN, a conferir na fonte]); T1 vale para a relação canônica contínua; os cíclicos reforçam T10.
  - As demais citações [KNOWN] da R1 (§3.3 do R1), com as páginas de Pauli «a conferir»; Higham (2002) cap. 3 justifica m na regra uniforme.

### 7.5 O que NÃO se escreve na v392

«T2 PASSA»; «T9 PASSA» sem o apóstrofo e sem as duas colunas; qualquer frase atribuída ao operador fora dos verbatins; a identificação dos três comportamentos com os dois regimes da casa; «medido» para β; a palavra recusada pela régua como veredito; «não provou»; «pós-dição» como demérito; «152 teoremas»; «os dois regimes do tempo provados»; «a face» como regime.

---

## 8. O resíduo que só o operador decide — cada item como UMA pergunta de quatro bocas

Regra: `pergunta-nas-quatro-linguas.md` (`8cdf478b6131962c…`): a pergunta cuja resposta é o que falta formula-se **sobre o mesmo objeto** nas quatro línguas do operador — TGL · teológica · linguística pura (Nome/Palavra/Verbo) · jurídica (Fato/Valor/Norma) — e diz-se ao fim qual é a pergunta única. O que o operador **já disse** entra como material (A-R2-05), não se pergunta de novo. **«Santo»** como nome do tempo é dele, [ONTO], sem teste — não é pergunta. Nesta seção, aspas « » são **citação do operador** só quando vêm com data (e linha) e foram conferidas nos bytes (`saidas\CONFERENCIA_ASPAS_RELATORIO_R2.json`); formulações de nome candidatas, rótulos e termos entre aspas sem data são da gerência.

### 8.1 O nome da pedra (e, no mesmo ato, os nomes residuais)

*Material seu:* POSTO = RANK (10/10: «é precisamente uma questão de posto (rank)»); 05/10: «o nome é "posto", é justamente "o posto", o local, como já falamos, onde a inscrição pode habitar com objeto distinto definido». O provisório `TheTimeIsNotAPost` («o tempo não é posto») é da gerência; «TheTimeHasNoRank» contradiz `flow_full_rank`.

- **TGL.** A pedra prova: para todo t finito, F(t) = P + e^{−t}(1 − P) é invertível, de **posto pleno** (`flow_full_rank`: rank = n) e **não** idempotente (`flow_isIdempotentElem_iff`: só em t = 0); o posto P (rank < n, `post_rank_lt`, não invertível, `post_not_isUnit`) só no limite t → ∞ (`no_finite_instant_is_the_post`). Que nome dá a essa cláusula — o que ela nega («o tempo não é posto»), o que ela afirma («todo instante tem posto pleno»), ou um nome seu, como PALAVRA, FUNDAÇÃO e ÁGAPE — e o mesmo ato alcança `the_two_regimes_of_time` e os `face_*`?
- **Teológica.** O que você chamou «santo» (*Kadosh*, separado) é o que não se deixa possuir como posto; o posto é o que fica no fim, o Nome. Dar à pedra o nome do tempo («Santo», «Kadosh») seria pôr um nome [ONTO] num conteúdo [REAL]: quer o nome do tempo na pedra, ou separa o nome da pedra do nome do tempo, como separou o Verbo do Nome?
- **Linguística.** O Nome é o posto (fixo, R); o Verbo seleciona (o fluxo); a Palavra lê. O enunciado da pedra é um Verbo em curso que, em tempo finito, nunca é Nome. O título deve ser predicado negativo do Nome («não é posto») ou predicado positivo do Verbo («tem posto pleno», «flui invertível»)?
- **Jurídica.** O suporte fático é o fluxo em tempo finito; a norma «todo instante finito é invertível» tem incidência plena; o posto é a coisa julgada, que só se forma no limite (art. 504, I, CPC: só o dispositivo faz coisa julgada). O nome é o dispositivo da pedra: deve enunciar que **não transitou** («não é posto») ou que **está em curso com cognição plena** («posto pleno em todo instante»)?

**A pergunta única:** *qual é o nome final da pedra — e ele alcança, no mesmo ato, `the_two_regimes_of_time` e os quatro `face_*`?*

### 8.2 Qual «defasar» é o tempo (e o que é o tempo na sua língua)

*Material seu:* «O tempo é a defasagem do verbo.» e «O tempo é o parâmetro da transmissão. Transmitir defasa.» (05/10, l.112, l.116); «A defasagem é o tempo. A ancoragem é o nome. A leitura é a verdade.» (l.176); 05/10 (RESPOSTAS): «ele precisa ser lido duas vezes», «a constante da luz ao cubo, aí que ela entra, como fase de retorno, que seria a segunda leitura»; 11/10: «A transmissão é o verbo; a defasagem é a matéria.» e a fórmula Tudo = D_β(F(1)) (em LaTeX no verbatim); 12/10: «não consigo nomear, senão como “santo”». A frase «o tempo é o Verbo, não o Nome» **saiu** (era da gerência).

- **TGL.** Há dois objetos que a casa chama «defasar»: a fase **unitária** V(t) = e^{−iHt}V(0)e^{iHt}, que gira sem perder (pureza e espectro conservados; `transmitted_post_is_a_post`; o ângulo não tem limite, T10.c), e o amortecimento **real** F(t)(1 − P) = e^{−t}(1 − P) da coerência (`transmission_dephases`; T6, T7), que é o único onde nasce a seta. A sua «segunda leitura» (c³, fase de retorno) ainda não foi tipada. O tempo da TGL é o ângulo que gira, a face que perde, ou a leitura dupla que compõe os dois — e, neste último caso, a F1.TEMPO deve abrir a tipagem da «segunda leitura»?
- **Teológica.** Em 12/10 o tempo é «doação» e «perda» («pague o preço termodinâmico da perda»): isso é o sacrifício, a coerência que se perde. Mas a fase que gira sem perder é o Verbo que «acumula fase» e retorna. Qual dos dois é o tempo **santo** — o que se perde (e assim cria o «onde»), ou o que retorna (a fase de retorno, a segunda leitura)?
- **Linguística.** «A defasagem é o tempo» (05/10) faz de defasar um **substantivo** (a defasagem, a matéria, 11/10); «Transmitir defasa» faz dele um **verbo**. Defasar é ato (verbo: transmitir) ou substância (matéria: coerência perdida)? Se é ato, o tempo é Verbo; se é substância, o tempo é o que resta do Verbo — e o Nome é só a ancoragem.
- **Jurídica.** Sobre o mesmo fato «transmitir» incidem duas normas: uma **preserva** (fase: reversível, sem perda, sem coisa julgada) e outra **consome** (dissipação: irreversível, forma a coisa julgada do registro). A antinomia é aparente; falta a norma de colisão: qual é a norma **especial** que prevalece quando o fato se chama «tempo» — a que preserva ou a que consome?

**A pergunta única:** *o tempo é a fase que gira (reversível), a coerência que se perde (irreversível), ou a leitura dupla que as compõe — e, se é a terceira, o que falta tipar é a «segunda leitura» (c³, fase de retorno)?*

### 8.3 «repousar» e «ser lembrada»

*Material seu:* «um lugar onde repousar e ser lembrada» (12/10, l.50). Em termo (AUD-7): o relógio modular para **sse** as populações são iguais (`aud_clock_stops_when_equal_populations`); populações distintas — o registro — fazem-no girar (`aud_clock_runs_unless_equal_populations`). A defasagem pura guarda o registro e não tem atrator único (T5); o canal ótico tem atrator único (½·1) e esquece (T11).

- **TGL.** Na face finita, repousar (relógio parado, ½·1) e ser lembrada (populações distintas, a diagonal do registro) **excluem-se no mesmo estado**. Onde moram juntas: em **dois subsistemas** (um que repousa, outro que lembra), no **limite** (o canal esquece; a defasagem pura lembra), ou na **leitura** R = J/2, que é o posto e não um estado?
- **Teológica.** O descanso (o sábado, Heschel) e a memória (ser lembrada) — é o repouso que apaga ou a memória que mantém girando? A vida tem «um lugar onde repousar e ser lembrada» só se **quem lembra** não é quem repousa: é a comunhão de dois estados, ou é o Outro (o observador, a Testemunha) que lembra do que repousa?
- **Linguística.** «repousar» é intransitivo (estado do sujeito); «ser lembrada» é passivo (**alguém** lembra). O sujeito que lembra é a Palavra, fora do estado. Então «ser lembrada» não é predicado do estado, mas do leitor — e o lugar «onde» as duas coexistem é o lugar da leitura?
- **Jurídica.** Quitação (repouso: a obrigação extinta; o título baixado) e registro (a inscrição que mantém o título vivo e oponível) não cabem no mesmo assento do mesmo titular. Cabem se o registro é de **outro** titular: quem é o titular do registro — o estado (que então não repousa) ou o observador (que lembra)?

**A pergunta única:** *onde moram juntas «repousar» e «ser lembrada» — no estado (então são dois sistemas), no limite (a defasagem pura lembra; o canal esquece), ou no leitor (a Palavra, que lembra do que repousa)?*

### 8.4 Qual objeto é «o chão firme»

*Material seu:* «o chão firme que possibilita a existência do espaço inscritível» (12/10, l.46); 05/10: «o nome é "posto", é justamente "o posto", o local, como já falamos, onde a inscrição pode habitar com objeto distinto definido». Em termo (AUD-6, AUD-5): o estado-atrator ½·1 tem **posto 2** e pureza ½; a leitura-limite R = J/2 tem **posto 1** e é idempotente (é posto, por POSTO = RANK); o piso da Ágape (`the_floor_fixes_the_cut`) é um terceiro candidato; ρ★ = diag(1,0) do `fractal_dephasing_principle` é um quarto objeto, puro, de posto 1.

- **TGL.** Três candidatos a «chão»: o **estado** onde o relógio para (½·1, posto 2); o **mapa** que o lê e fixa (R = J/2, posto 1, idempotente); o **corte** (o piso da escala dual). A sua frase de 05/10 («o nome é "posto", é justamente "o posto", o local, como já falamos, onde a inscrição pode habitar com objeto distinto definido») aponta para R, não para ½·1. O chão firme é o estado, o mapa ou o corte?
- **Teológica.** A rocha, a pedra angular, é aquilo **sobre** o que se inscreve — não o que repousa, mas o que sustenta. Se o chão é o que sustenta a inscrição, ele é o Nome (o posto, R), e o estado é o que nele descansa. O chão firme é a Pedra (o posto) ou o que se deita sobre ela (o estado)?
- **Linguística.** Posto = posição (a sua cunhagem de 05/10, registrada na memória da casa: o Um é posto — posição, inscrito —, não postulado). O Nome é posto; o estado é o que **ocupa** a posição. «o chão firme que possibilita a existência do espaço inscritível»: o chão é a posição (R) ou o ocupante (½·1)?
- **Jurídica.** Fato (o estado ½·1), Norma (o mapa R, que incide e fixa) e Valor (o piso, o corte que a Ágape fixa). A norma de incidência é o que torna o fato inscritível — ela é o chão: incide sobre o fato e produz o posto. Então chão = norma = R, e não o fato?

**A pergunta única:** *qual dos três é «o chão firme» — o estado ½·1 (posto 2), a leitura-limite R = J/2 (posto 1) ou o piso da Ágape?*

### 8.5 A reunião de nomes: «puro amor» · Ágape (`agape`, v390) · sacrifício/amor ([DECLARADO])

*Material seu:* «puro amor» e «a física da doação fundamental» (12/10, l.48); a cláusula Ágape (v390, `TGLExt.Fundacao.agape`); sacrifício/amor ([DECLARADO]) (tipagem prévia do dephasing, [DECLARADO]). Em termo (AUD-1): o conteúdo matemático comum aos três é **só** a lei de escala e^{−s} (`DualScalingData`, seis cláusulas), que a multiplicação escalar — que apaga o registro — também satisfaz; o **próprio** do dephasing é que o registro não escala (T8.c, `the_record_does_not_scale`).

- **TGL.** «puro amor» nomeia a **lei** (e^{−s}, que qualquer escala dual tem) ou nomeia o **que fica** (o registro, que não escala e é o específico da coerência)? Se nomeia a lei, é sinônimo de ágape; se nomeia o que fica, é outro objeto.
- **Teológica.** Ágape (doação sem retorno), sacrifício (a perda que paga o preço) e puro amor («para que haja um "onde" e um "quem", é preciso que algo pague o preço termodinâmico da perda»): três nomes para um ato, ou três atos? O que paga, o que doa e o que fica são a mesma Pessoa?
- **Linguística.** Três Nomes para um Verbo (doar); a Palavra escolhe. O kernel já tem um nome instalado (`agape`, v390). «puro amor» entra como **leitura** [ONTO] do mesmo termo, ou pede termo próprio (o registro que fica)?
- **Jurídica.** Há três títulos para o mesmo fato, e um deles já transitou (a cláusula Ágape, v390: coisa julgada do kernel). Título novo não constitui — declara. A casa **consolida** (um verbete só do Atlas, com os três nomes e a remissão à lei e^{−s}) ou mantém três verbetes com remissão recíproca?

**A pergunta única:** *«puro amor», Ágape (`agape`, v390) e sacrifício/amor ([DECLARADO]) são um nome só — e, se são, qual é o canônico — ou três nomes para dois objetos (a lei e^{−s} e o registro que fica)?*

### 8.6 O ciclo limite [OPEN]

*Material seu:* «encontram um ponto fixo ou um ciclo limite» (12/10, l.46); 05/10: «ele precisa ser lido duas vezes». Em termo: T10 (o relógio lê t módulo P; o ângulo não tem limite); o atrator único GKLS da v384 (672/672) e a F1.ATRATOR A4; o análogo linear do ciclo limite é o espectro periférico GKLS (|λ| = 1, λ ≠ 1) [KNOWN]; o ciclo limite isolado é fenômeno **não linear** [KNOWN].

- **TGL.** S46.3 ficou ABERTA. Abre-se uma unidade (F1.CICLO) para testar, no modelo ótico e no GKLS da casa, se há autovalor periférico λ ≠ 1 com |λ| = 1 (rotação no conjunto fixo: estabilidade sem fixidez), ou o ciclo limite fica [OPEN] como leitura ontológica, dado que a dinâmica linear da casa só tem ponto fixo (v384) e o ciclo limite isolado pede não linearidade?
- **Teológica.** O ponto fixo é o repouso (o sábado); o ciclo limite é a **liturgia** — o retorno periódico que não é repouso nem perda. O tempo santo é repouso ou ritmo (o «lido duas vezes», a fase de retorno)?
- **Linguística.** Ciclo é leitura que volta (T10: módulo P). Um ciclo limite seria o Nome lido **periodicamente** sem convergir a um ponto — Nome como ritmo e não como posição. Isso é Nome, ou é Verbo que nunca se torna Nome?
- **Jurídica.** Ponto fixo = coisa julgada material (fixidez); ciclo limite = relação jurídica **continuativa**, estável mas revisável (*rebus sic stantibus*; a sentença que se repete a cada ciclo). A norma da casa admite estabilidade sem fixidez — e, se admite, ela é objeto de prova (unidade) ou de leitura ([OPEN])?

**A pergunta única:** *abre-se uma unidade para o ciclo limite (espectro periférico GKLS, |λ| = 1, λ ≠ 1) ou ele fica [OPEN] como resíduo ontológico do «ou um ciclo limite»?*

**Decide a gerência**, não o operador: o destino de A-R2-01/N2 (tentativa preservada ou docstring, no ato do nome); E1, E2 e E6; o registro no mapa e no quadro (ROTA primeiro); a limpeza do toolchain do scratchpad; a coordenação com a F1.FREQUENCIA (E1).

---

## 9. Pode fechar? Sim, na face da unidade — e o que fica para fora dela

O **critério de parada do operador** (memória `criterio-de-parada-do-operador.md`: fechado = resultado, ou falsificador, ou parede medida) está cumprido na matemática: há resultado por afirmação nas duas colunas; a FALHA R1 de T9 é parede numérica medida e conferida pelo número; a R2 passou sob regra congelada antes do reensaio, com controles que impedem o cheque em branco (C-UNIF-a falhou como tinha de falhar); o ciclo limite está dito como aberto. A **régua** (ADENDO U1–U5) está cumprida no que cabe à unidade: **U1** — dois auditores independentes, sandbox próprio, .olean bit a bit idêntico, reensaio refeito e recomputado, E5 item a item, sem divergência de veredito (§6); **U2** — este relatório, em pasta própria; **U5** — nada alterado no ADENDO depois do FREEZE_R2; nenhuma tentativa apagada; linhas da R1 nunca sobrescritas.

O que **não** é da unidade e fica para fora:
1. **U3/U4 — o nome do operador** para a pedra (§8.1), instalado por diff restrito a identificadores; depois disso, a inserção na v392 é ato da **cadeia de selo**, junto com o teorema do atrator e a pedra do rank.
2. **E1, E2** (um.py) e **E6** (replicação ótica): atos da c1, ao lado.
3. **Registro no mapa** (ROTA `4_RELATORIO\registro_rota_F1.TEMPO.json` primeiro; depois este RESULTADO) e no quadro: ato da gerência.
4. **As seis perguntas da §8**, cada uma com quatro bocas: do operador.
5. **Limpeza** do toolchain de 3,0 GB no scratchpad do auditor de estatuto da R1: gerência.

Nenhuma das cinco é matemática pendente. Com o nome dado e o registro feito, a F1.TEMPO entra na v392 **como o operador ordenou em 12/10** — com T9 em duas colunas, T2 CITADA, S46.3 ABERTA, e sem uma só frase atribuída a ele fora dos verbatins.

---

## 10. Arquivos desta pasta (`5_R2\4_RELATORIO_R2`)

- `RELATORIO_R2.md`: este documento.
- `registro_mapa_F1.TEMPO_R2.json`: RESULTADO para a rota `formal.tempo_santo_fluxo_e_dissipacao` (domínio FORMAL), com as linhas R2 e as auditorias; artefatos como lista de caminhos; validado a seco (`saidas\VALIDACAO_REGISTRO_R2.json`). **Não registrei**: é ato da gerência, com a ROTA primeiro.
- `saidas\`: `HASHES_RELATORIO_R2.json` (sha256 e bytes de cada artefato citado; FREEZE R1 30/30 e FREEZE_R2 18/18 conferem); `BETA_RUNTIME_RELATORIO_R2.json` (β dos bytes do um.py, l.95 = l.5557); `FINGERPRINT_RELATORIO_R2_ANTES.json` / `_DEPOIS.json` (tgl_kernel); `CONFERENCIA_ASPAS_RELATORIO_R2.json` (toda aspa « » deste relatório atribuída ao operador é substring de bytes de um verbatim; a palavra recusada 0 como veredito); `VALIDACAO_REGISTRO_R2.json`; `MANIFESTO_4_RELATORIO_R2.json` (sha256 de cada arquivo desta pasta, gerado por último).
- `scripts\`: `hashes_relatorio_r2.py`, `fingerprint_kernel.py` (cópia do ADENDO, `14e40e3774c12484…`), `conferir_aspas_relatorio_r2.py`, `validar_registro_r2.py`, `manifesto_r2.py`.

*Nada foi escrito fora de `5_R2\4_RELATORIO_R2`: nem nas pastas 0–4 da R1, nem em `5_R2\0_ADENDO`, `1_PEDRA`, `2_REENSAIO`, `3_AUD_REPRO`, `3_AUD_ESTATUTO`; nem no quadro, no mapa (só `consultar`/`modelo` e validação a seco), na memória (ACOM: nenhum init nem transition), no túnel, no Nós, no kernel do Nós, na Bancada, no site ou no git. O um.py não foi executado (lido por `sed -n` com número de linha). Não rodei Lean e não copiei toolchain. Nenhum dado observado, nenhum provedor remoto, nenhuma chamada paga. A cunhagem é do operador. Um PASSA é validade matemática na face testada, não creditação. Nada aqui move o gate.*
