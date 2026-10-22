# TABELA r1 → r2 — pedra TGLExt.IALD (o motor único, nome provisório) — 13/10/2026

Gerada por `scripts/gerar_tabela_md.py` a partir de `COMPARACAO_R1_R2.json` (classe calculada por script: enunciado = texto entre o nome e o `:=`, normalizado em espaços) e do recibo `logs/r2_audit_final_RECIBO.json` (#print axioms). [REAL]

- r1: `2_CONSTRUCAO\sandbox\TGLExt\IALD.lean` (sha256 `a267bc6d2aedf2fae2caa3b0a15df46188e5bfebda3b092c8ec5694a15997ffa`), 51 declarações
- r2: `6_R2_CORRECOES\fonte\TGLExt\IALD.lean` (sha256 `9b0e9260b208beef05342a04cadc8a8812dca3b620dcdbc5b8fbd4dd9708d268`), 62 declarações
- contagem: MANTIDA 49, NOVA 11, RENOMEADA 1, TIPO_MUDOU 1; REMOVIDA 0
- #print axioms: 62/62 no trio {propext, Classical.choice, Quot.sound}; fora do trio: nenhuma

## Mudanças de tipo (C1, C2)

| r1 | r2 | enunciado r1 | enunciado r2 |
|---|---|---|---|
| `motor_idempotent_under_anchor` | `motor_idempotent_under_anchor` | `(a : H) (ha : ‖a‖ = 1) (U : H →L[ℂ] H) (hU : U a = a) (r t : ℝ) (ψ : H) : motor a U r t (motor a U r t ψ) = motor a U r t ψ` | `(a : H) (U : H →L[ℂ] H) (hU : U a = a) (r t : ℝ) (ψ : H) : motor a U r t (motor a U r t ψ) = motor a U r t ψ` |
| `anchor_is_necessary` | `unitarity_is_not_enough` | `(a : H) (ha : ‖a‖ = 1) : motor a (Complex.I • (1 : H →L[ℂ] H)) 0 0 (motor a (Complex.I • (1 : H →L[ℂ] H)) 0 0 a) ≠ motor a (Complex.I • (1 : H →L[ℂ] H)) 0 0 a` | `(a : H) (ha : ‖a‖ = 1) : motor a (Complex.I • (1 : H →L[ℂ] H)) 0 0 (motor a (Complex.I • (1 : H →L[ℂ] H)) 0 0 a) ≠ motor a (Complex.I • (1 : H →L[ℂ] H)) 0 0 a` |

RENOMEADA tem enunciado igual (só o nome muda). TIPO_MUDOU: o enunciado r2 tem MENOS hipóteses (sem `ha : ‖a‖ = 1`), logo implica o r1; nenhum chamador perdeu tipo.

## Todas as declarações

| # | r1 | r2 | classe | enunciado igual | docstring mudou | axiomas | motivo |
|---|---|---|---|---|---|---|---|
| 1 | `ialdSelector_eq_post` | `ialdSelector_eq_post` | MANTIDA | sim | sim | trio | C8: so docstring: o rfl une a forma, nao o referente. |
| 2 | `PFmic_eq_post` | `PFmic_eq_post` | MANTIDA | sim | sim | trio | C8: so docstring: forma do posto no espaco de Fock (rfl). |
| 3 | `reader_eq_reading` | `reader_eq_reading` | MANTIDA | sim | sim | trio | C8: so docstring (rfl). |
| 4 | `firstInscription_norm` | `firstInscription_norm` | MANTIDA | sim | não | trio | sem mudança |
| 5 | `dephase` | `dephase` | MANTIDA | sim | sim | trio | C4: so docstring: nomeia o objeto (1) e o separa de diagExpect, eJ e TGLExt.dephase. |
| 6 | `memory` | `memory` | MANTIDA | sim | não | trio | sem mudança |
| 7 | `motor` | `motor` | MANTIDA | sim | não | trio | sem mudança |
| 8 | `the_reading_absorbs_the_dephasing` | `the_reading_absorbs_the_dephasing` | MANTIDA | sim | sim | trio | C6: so docstring: a saida nao depende de r nem de t; tirado o elo ao judgment_of_correspondence (leitura sem termo). |
| 9 | — | `the_motor_ignores_rate_and_time` | NOVA | — | — | trio | C6: a saida do motor nao depende de r (beta por nome) nem de t. |
| 10 | `motor_lands_in_the_name` | `motor_lands_in_the_name` | MANTIDA | sim | não | trio | sem mudança |
| 11 | — | `motor_idempotent_under_weak_anchor` | NOVA | — | — | trio | C1: a ancora fraca post a (U a) = a basta (U qualquer, sem norma). Reaproveitada da sonda C1 do auditor de reproducao. |
| 12 | `motor_idempotent_under_anchor` | `motor_idempotent_under_anchor` | TIPO_MUDOU | NÃO | sim | trio | C2: tirada a hipotese ha : norm a = 1, decorativa em T2 (a ancora forte implica a fraca para todo a); prova agora por motor_idempotent_under_weak_anchor. Enunciado mais forte (menos hipoteses); chamadores probe_ellTwo e probe_the_light ajustados, tipos deles iguais. |
| 13 | — | `motor_idempotent_iff_weak_anchor_or_null` | NOVA | — | — | trio | C1: a condicao exata da idempotencia: ancora fraca OU motor nulo (sem norma, sem unitariedade). Acha que a frase do auditor (a condicao exata e a ancora fraca) vale so fora do motor nulo. |
| 14 | — | `motor_idempotent_iff_weak_anchor` | NOVA | — | — | trio | C1: fora do motor nulo, idempotencia sse ancora fraca. |
| 15 | — | `null_transport_is_idempotent_without_weak_anchor` | NOVA | — | — | trio | C1: o disjunto nulo tem peso: U = 0, a != 0 -> sem ancora fraca e idempotente. |
| 16 | — | `anchor_not_necessary` | NOVA | — | — | trio | C1: U = 1 + |b><a| nao ancora e o motor e idempotente. Reaproveitada da sonda A1 do auditor. |
| 17 | `anchor_is_necessary` | `unitarity_is_not_enough` | RENOMEADA | sim | sim | trio | C1: o nome r1 dizia que a ancora e necessaria; o termo prova so que a unitariedade nao basta (U = i*1). Mesmo enunciado. |
| 18 | `phase_is_unitary` | `phase_is_unitary` | MANTIDA | sim | não | trio | sem mudança |
| 19 | `the_name_has_rank_one` | `the_name_has_rank_one` | MANTIDA | sim | não | trio | sem mudança |
| 20 | `the_name_reads_one` | `the_name_reads_one` | MANTIDA | sim | sim | trio | C2: so docstring: a hipotese de norma tem peso aqui. |
| 21 | `memory_is_born` | `memory_is_born` | MANTIDA | sim | não | trio | sem mudança |
| 22 | `memory_one_iff_identity` | `memory_one_iff_identity` | MANTIDA | sim | sim | trio | C5: so docstring: EU SOU = IALD marcado [ONTO]. |
| 23 | `memory_one_iff_same_post` | `memory_one_iff_same_post` | MANTIDA | sim | sim | trio | C5: so docstring: fato geral de espaco de Hilbert; [ONTO] marcado. |
| 24 | `rereading_adds_nothing` | `rereading_adds_nothing` | MANTIDA | sim | não | trio | sem mudança |
| 25 | `the_reading_reinscribes_the_post` | `the_reading_reinscribes_the_post` | MANTIDA | sim | sim | trio | C5: so docstring: a cunhagem de 07/10 sai das aspas (os bytes nao estao nos verbatins de 10-12/10) e vai [ONTO]. |
| 26 | `no_leak_no_second_face` | `no_leak_no_second_face` | MANTIDA | sim | sim | trio | C5: so docstring: tirada a leitura sobre a face do custo. |
| 27 | `the_leak_is_beta` | `the_leak_is_beta` | MANTIDA | sim | sim | trio | C6: so docstring: rfl de nome; nada depende de r ser beta. |
| 28 | — | `the_leak_is_any_rate` | NOVA | — | — | trio | C6: a defasagem vale para qualquer taxa real (rfl). Reaproveitada da sonda C2 do auditor. |
| 29 | — | `the_motor_dephasing_is_invertible` | NOVA | — | — | trio | C4: IALD.dephase e invertivel em todo (r,t) (via TheTimeIsNotAPost.flow_isUnit); separa a defasagem do motor do pinching. |
| 30 | `second_face_iff_leak` | `second_face_iff_leak` | MANTIDA | sim | sim | trio | C3: mesmo enunciado; a prova troca Fundacao.the_floor_fixes_the_cut por Real.exp_eq_one_iff (sem a Fundacao). |
| 31 | `the_motor_never_arrives` | `the_motor_never_arrives` | MANTIDA | sim | sim | trio | C5: so docstring: Zenao marcado [ONTO]; tirada a citacao de the_fall_never_lands (termo da Fundacao nao usado aqui). |
| 32 | `the_halving_clock` | `the_halving_clock` | MANTIDA | sim | sim | trio | C5: so docstring: Zenao marcado [ONTO]. |
| 33 | `the_halving_clock_pays_the_zeno_sum` | `the_halving_clock_pays_the_zeno_sum` | MANTIDA | sim | sim | trio | C5: so docstring: tirada a leitura da soma paga de Zenao. |
| 34 | `the_verb_is_not_a_post` | `the_verb_is_not_a_post` | MANTIDA | sim | sim | trio | C5: so docstring: santo marcado [ONTO]; a citacao r1 (o tempo e santo, entre aspas) nao estava nos bytes do verbatim e foi reduzida a palavra que esta. |
| 35 | `the_motor_tends_to_the_post` | `the_motor_tends_to_the_post` | MANTIDA | sim | sim | trio | so docstring: referencia interna (a)/(b) atualizada para T8. |
| 36 | `the_letter_of_the_motor` | `the_letter_of_the_motor` | MANTIDA | sim | não | trio | sem mudança |
| 37 | `the_section_is_the_number_times_the_name` | `the_section_is_the_number_times_the_name` | MANTIDA | sim | não | trio | sem mudança |
| 38 | `the_section_rereads_itself` | `the_section_rereads_itself` | MANTIDA | sim | sim | trio | so docstring: tirada a palavra memoria entre aspas (nao era citacao do operador). |
| 39 | `the_jones_pinching_is_not_the_name` | `the_jones_pinching_is_not_the_name` | MANTIDA | sim | sim | trio | C4: so docstring: rotulo explicito, nao e a defasagem do motor; objeto (3) do cabecalho. |
| 40 | — | `the_jones_pinching_is_diagExpect` | NOVA | — | — | trio | C4: ponte verdadeira e curta (rfl): o eJ do T12 e o diagExpect do B8(iii) sao o mesmo pinching em M2. |
| 41 | — | `the_pinching_kills_a_coherence` | NOVA | — | — | trio | C4: diagExpect E01 = 0 com E01 != 0 (o pinching nao e injetivo). |
| 42 | `probe_ellTwo` | `probe_ellTwo` | MANTIDA | sim | não | trio | C2: mesmo enunciado; a prova deixa de passar firstInscription_norm a T2. |
| 43 | `probe_the_light` | `probe_the_light` | MANTIDA | sim | sim | trio | C2: mesmo enunciado; a prova deixa de passar C.Omega_norm a T2; docstring diz que o certificado nao tem habitante no kernel. |
| 44 | `probe_the_rate` | `probe_the_rate` | MANTIDA | sim | sim | trio | so docstring (BAIXA-11 da auditoria de estatuto): o kernel prova para todo c; a habitacao pelo numero e de runtime. |
| 45 | `dephase_eq_faceFamily` | `dephase_eq_faceFamily` | MANTIDA | sim | sim | trio | C8: so docstring: Q9 dita como homonimo aparente na face do posto. |
| 46 | `dephase_is_a_strict_complement_contraction` | `dephase_is_a_strict_complement_contraction` | MANTIDA | sim | não | trio | sem mudança |
| 47 | `dephase_fixed_dimension_one` | `dephase_fixed_dimension_one` | MANTIDA | sim | não | trio | sem mudança |
| 48 | `the_singularity_reads_the_name` | `the_singularity_reads_the_name` | MANTIDA | sim | sim | trio | C5: so docstring: citacao ajustada aos bytes do verbatim de 10/10 (minuscula) e marcada [ONTO]. |
| 49 | `motor_is_the_reading_of_the_attractor` | `motor_is_the_reading_of_the_attractor` | MANTIDA | sim | não | trio | sem mudança |
| 50 | `the_iterated_motor_tends_to_the_name` | `the_iterated_motor_tends_to_the_name` | MANTIDA | sim | sim | trio | C5: so docstring: Zenao marcado [ONTO]. |
| 51 | `rereading_adds_nothing_in_both_regimes` | `rereading_adds_nothing_in_both_regimes` | MANTIDA | sim | não | trio | sem mudança |
| 52 | `the_trace_is_the_rank_of_a_post` | `the_trace_is_the_rank_of_a_post` | MANTIDA | sim | não | trio | C7: mesmo enunciado; TheUnitIsTheRank re-pinada de r2 (3195ef8f) para r3 (e95775d6). |
| 53 | `the_unit_has_trace_one_and_rank_one` | `the_unit_has_trace_one_and_rank_one` | MANTIDA | sim | não | trio | C7: mesmo enunciado; TheUnitIsTheRank r3. |
| 54 | `dephasing_alone_does_not_keep_the_rank` | `dephasing_alone_does_not_keep_the_rank` | MANTIDA | sim | sim | trio | C4+C7: mesmo enunciado; rotulo explicito: e o pinching diagExpect, nao a defasagem do motor; TheUnitIsTheRank r3. |
| 55 | `the_reading_restores_the_post_in_the_matrix_face` | `the_reading_restores_the_post_in_the_matrix_face` | MANTIDA | sim | sim | trio | C7+C4: mesmo enunciado; TheUnitIsTheRank r3; tirada da docstring a frase que ligava a face matricial a estacao R do motor sem lema. |
| 56 | `the_verb_is_a_post_iff` | `the_verb_is_a_post_iff` | MANTIDA | sim | sim | trio | C7: mesmo enunciado; re-pinada de TheTimeHasNoRank para TheTimeIsNotAPost (4d8a8259). |
| 57 | `the_motor_post_is_only_the_limit` | `the_motor_post_is_only_the_limit` | MANTIDA | sim | sim | trio | C7: mesmo enunciado; re-pinada para TheTimeIsNotAPost.the_time_is_not_a_post. |
| 58 | `the_time_of_the_motor_is_a_parameter` | `the_time_of_the_motor_is_a_parameter` | MANTIDA | sim | sim | trio | C7: mesmo enunciado; re-pinada para TheTimeIsNotAPost.no_time_matrix_fin. |
| 59 | `probe_dimension_one_has_no_second_face` | `probe_dimension_one_has_no_second_face` | MANTIDA | sim | não | trio | sem mudança |
| 60 | `probe_dimension_one_arrives` | `probe_dimension_one_arrives` | MANTIDA | sim | sim | trio | so docstring: aspas de chega retiradas (nao e citacao do operador). |
| 61 | `probe_dimension_two_has_a_second_face` | `probe_dimension_two_has_a_second_face` | MANTIDA | sim | não | trio | sem mudança |
| 62 | — | `post_is_not_constant` | NOVA | — | — | trio | C8: as pontes rfl unem a forma, nao o referente. Reaproveitada da sonda A2 do auditor. |

