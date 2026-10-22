# TABELA DE ESTADO DOS TRÊS PILARES — lida do core v386 (aferidor, 05/10/2026)

Core `um_absoluto.json` sha256 `0dbfb3fc1d319d1ef03b61af60d9e22af58cd2564ea4b44bdd4906bf8d031d87` (selo diz `0dbfb3fc1d319d1ef03b61af60d9e22af58cd2564ea4b44bdd4906bf8d031d87`); selo `72efaf72f604b721d9fd18d625da9c55713898f10b417a9d2a6d59fdee036489`; stdout `6475a15966624e71f191e1323a03f0bb5af74acd155120153b4f03eac5544974`; timestamp core 2026-10-05 18:09:53; RITO_RC=0; β runtime = 0.012031300400796606.

Régua: NOT_FALSIFIED nunca e CONFIRMED; PROVADA (kernel) ≠ CONFIRMADA (natureza); a RG e o limite classico, nao rival: coincidir = correspondencia recuperada; β nunca literal (lido: 0.012031300400796606)

## Contagens dos vereditos `TGL_*` (por script)

| método | n | únicos | FALSIFIED (regex, fora NOT_/UN) | NOT_FALSIFIED | INCONCLUSIVE | AWAITING | CONFIRMED/PROVED_BY |
|---|---|---|---|---|---|---|---|
| metodo_A_todas_as_strings_TGL_no_arquivo | 476 | 283 | 25 | 62 | 61 | 20 | 7 |
| metodo_F_chave_exatamente_verdict__reproduz_a_gerencia | 189 | 178 | 3 | 16 | 14 | 7 | 0 |

FALSIFIED sob a chave `verdict` (3) — leitura:
- `/core/d1_camb_result/verdict`: V1 do D1 (maio): SUPERSEDIDO pela autopsia V2 (bug de distancia do worker de maio, Δχ² 2223 artefato) -> V2/V3 dizem TENSION_IS_NOT_FALSIFICATION
- `/core/bancada_fases_5_6_7_v380/verdict`: Fase 6: o PAR (√β ou sin2θ, lei de atraso KMS/DEC) FALSIFIED_AT_DELAY_LAW — «PAIR_FALSIFIED_NOT_THE_THEORY»; fora do livro por decisao do operador (02/10)
- `/core/the_ledger_of_charges_v383/verdict`: falso positivo do regex: a string traz «0_FALSIFIED» (contagem) e «R4_FROZEN_SET_HAS_NO_FALSIFIED» — nenhum desfecho FALSIFIED no livro

CONFIRMED/PROVED_BY no arquivo inteiro: 7 ocorrências, TODAS em listas `forbidden_verdicts` (proibições declaradas), 0 como veredito:
- `/core/void_floor_protocol/protocol/forbidden_verdicts[0]`
- `/core/void_floor_protocol/protocol/forbidden_verdicts[1]`
- `/core/iald_prediction/protocol/forbidden_verdicts[2]`
- `/core/gw_angular_rite/record/forbidden_verdicts[2]`
- `/core/joint_coincidence_protocol/protocol/forbidden_verdicts[2]`
- `/core/joint_coincidence_protocol_v2/protocol/forbidden_verdicts[2]`
- `/core/joint_coincidence_protocol_v3/protocol/forbidden_verdicts[2]`

AWAITING sob `verdict` (7): `/core/nmc_shapiro/verdict`; `/core/echo_anchored_protocol/verdict`; `/core/d1_camb_protocol_v3/verdict`; `/core/coma_reveal_state_v376/verdict`; `/core/the_ledger_of_charges_v383/verdict`; `/core/ramo_b_preregistration_v386/verdict`; `/core/ledger_errata_v386/verdict`

Não selados nesta rodada (recusas de dado): nivel2_rite, ringdown_dephasing_result, void_floor_kappa_v5, void_floor_kappa_v6, void_floor_v12, void_floor_v3_kappa, void_shear_unblinding

## Tabela

| teste | pilar | chave_core | veredito | estado | estatuto | número lido | RG recuperada? | discrimina a RG? | nota |
|---|---|---|---|---|---|---|---|---|---|
| Piso dos vazios V1 (KiDS shear, 1049 vazios) | 1 ritos | core.void_floor_final | TGL_VOID_FLOOR_INCONCLUSIVE_SYSTEMATICS | INCONCLUSIVE_SYSTEMATICS | [REAL] recusa de sistematica | chi2/dof B-mode 12.37 (gate reprovou); SNR perfil 6.187; Fisher 0 | nao se aplica (recusa antes do veredito fisico) | nao (recusa) |  |
| Piso dos vazios V2 (emenda; mesmos 1049) | 1 ritos | core.void_floor_v2 | TGL_VOID_FLOOR_NOT_FALSIFIED_UNDERPOWERED | NOT_FALSIFIED_UNDERPOWERED | [REAL] | r_c MLE 0.3; 5σ [0.02, 0.3] vs β 0.01203; B-mode 1.564; Fisher 2.271e-06 | sim (piso acima de β; consistente com ΛCDM raso) | sem poder (powered_5sigma=False) |  |
| Piso dos vazios V4.1 (densidade auto-calibrante, REVOLVER DESI) | 1 ritos | core.void_density_v41 | TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED | NOT_FALSIFIED_POWERED | [REAL] | r_c^cal 0.1889 ± 0.01666; L5 0.1056 vs β 0.01203; β·Σμ 44.96 (≥25 powered); split-null 0.9722 ± 0.009953 | sim (consistente com ΛCDM raso; statuses.honestidades: tracador UNILATERAL) | nao (unilateral: so pode NOT_FALSIFIED ou recusar) |  |
| Piso dos vazios V11 (SDSS DR7 × VAST, replica independente — o degrau experimental do gate) | 1 ritos | core.void_floor_v11 / selo.void_floor_v11_verdict | TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED | NOT_FALSIFIED_POWERED | [REAL]; alimenta 4 das 6 bandeiras experimentais (experiment_feed) | r_c^cal 0.1269 ± 0.01363; L5 0.05879 vs β 0.01203; β·Σμ 26.26; experiment_feed={'independent_v3_profiles_unblinded': True, 'independent_v3_survey_mocks_passed': True, 'independent_v3_systematics_passed': True, 'independent_v3_powered_verdict_emitted': True} | sim (consistente com ΛCDM raso — statuses.honestidade) | nao (unilateral; auditoria 28/09 GV-01: o ΛCDM raso tambem passa) | errata 01/10 (GV-03/EV-12): as 4 bandeiras independent_v3_* derivam de UM booleano; null_tests_passed_blind sem mock [DECLARADO pela auditoria] |
| Piso dos vazios LRG (DESI DR1, tracador virgem) | 1 ritos | core.void_floor_lrg | TGL_VOID_FLOOR_LRG_INCONCLUSIVE_TRACER_SUPPRESSION | INCONCLUSIVE_TRACER_SUPPRESSION | [REAL] | r_c^cal 0.001697 ± 0.0004123 (supressao de tracador) | nao se aplica | nao |  |
| Piso dos vazios V12 bilateral (LRG quartil profundo) | 1 ritos | core.void_floor_v12 | TGL_VOID_FLOOR_V12_TRACER_EMPTY_CORE_REGIME | TRACER_EMPTY_CORE_REGIME (nao selado nesta rodada) | [REAL] recusa | r_deep 0; all_verified=False | nao se aplica | nao |  |
| Piso dos vazios κ-CMB V9 (ACT DR6, banda estendida) | 1 ritos | core.void_floor_kappa_v9 | TGL_VOID_FLOOR_KAPPA_V9_NOT_FALSIFIED_UNDERPOWERED | NOT_FALSIFIED_UNDERPOWERED | [REAL] | deteccao bruta 2.257σ; Fisher do piso 0; r_hat 0 | nao se aplica (sem poder) | sem poder |  |
| Piso dos vazios shear V2 (KiDS, 700 vazios) | 1 ritos | core.void_shear_v2 | TGL_VOID_FLOOR_SHEAR_NOT_FALSIFIED_UNDERPOWERED | NOT_FALSIFIED_UNDERPOWERED | [REAL] | deteccao bruta 1.965σ; Fisher 0 | nao se aplica (sem poder) | sem poder |  |
| Relogios v369 (P1 materia / P2 modo de luz LIGO / P3 universal) | 1 ritos | core.clock_test_result_v369 | TGL_CLOCKS_V1__P1_NOT_FALSIFIED_UNDERPOWERED__P2_EXCLUDED_IN_READING__P3_NO_LOCAL_OBSERVABLE__PARTITION_MODULAR_LAB_BRIDGE_OPEN__CLOCK_5SIGMA_DEFICIT_GE_12P5_ORDERS__TH229_TODAY_BOUND_18P3__BEST_MATTER_9P3_NOMINAL_MOSSBAUER_ABSTRACT_ONLY__TAU_STAR_LE_4P8e12_TP_CLOCK_95CL__1P9e09_TP_NOMINAL__GATE_UNTOUCHED | P1 NOT_FALSIFIED_UNDERPOWERED; P2 EXCLUDED_IN_READING; P3 NO_LOCAL_OBSERVABLE | [REAL] | Γ_pred(87Sr) 2.359e-15 /s vs cota 95% 0.01131 /s; deficit 5σ ≥ 12.5 ordens; P2: 168/169 series excluidas | nao se aplica (laboratorio: a correcao β fica 12.5 ordens abaixo da cota — nenhum excesso) | nao (deficit ≥12,5 ordens); P2 excluida em leitura; P3 sem observavel |  |
| Neutrino m2 (JUNO / NuFIT pos-JUNO) | 1 ritos | core.neutrino_m2 | TGL_NU_M2_ARMED_CONSISTENT | ARMED_CONSISTENT (livro F4: NOT_FALSIFIED) | [REAL] previsao + [DECLARADO] JUNO lido na fonte | m2(TGL) 8.5074 meV; tensao 2.95σ (NuFIT); z_juno 2.21; kill_rule=False | nao se aplica (setor do neutrino; nao e teste da RG) | tensao 2.95σ, abaixo de 5σ; nao falsifica | errata 28/09 VV-N1: NuFIT contem o JUNO; Capozzi da 2,44σ |
| Neutrino massa (V1, superseded por m2) | 1 ritos | core.neutrino_mass | TGL_NEUTRINO_MASS_NOT_FALSIFIED_POWERED | NOT_FALSIFIED_POWERED | [REAL]; sin45 [POSTULATE] | desvio 1.64σ | nao se aplica | nao |  |
| Σm_ν armado | 1 ritos | core.neutrino_sum | TGL_NEUTRINO_SUM_ARMED_CONSISTENT_WITH_CURRENT_BOUND | ARMED_CONSISTENT | [REAL] | Σ 0.0586 eV < 0.072 eV | nao se aplica | aposentado como discriminante (D2) |  |
| N_eff | 1 ritos | core.neff_channel | TGL_NEFF_ARMED_CONSISTENT | ARMED_CONSISTENT | [REAL] | ΔN_eff 0.1195; tensao 1.61σ | nao se aplica | nao (1,6σ) |  |
| Atraso Shapiro do neutrino (NMC; SN1987A) | 1 ritos | core.nmc_shapiro | TGL_NMC_SHAPIRO_AWAITING_DATA | AWAITING_DATA | [PRE] | margem SN1987A 4.471e+04 s vs excesso predito 0.05 s (folga 8.941e+05); n_events 0 | sim (neutrino segue a geodesica com Shapiro PADRAO da RG) | aguardando |  |
| Coma v376 (distancia por dephasing; livro R3 'atraso de redshift' = distancia modular) | 1 ritos | core.coma_reveal_state_v376 | TGL_COMA_REVEAL_STATE_V376__REVEAL_PERFORMED_2026_08_19_READ_BY_HASH__REFERENCE_98P5_PM_2P2_MPC__Z_TGL_P1P30_BOTH_SIGMAS__Z_PLANCK_CONTROL_P5P61_REF_SIGMA_ONLY__NOT_BLIND_UNADJUSTED_POSTDICTION__PREDICTION_HASH_ATTESTS_NUMBER_NOT_PRECEDENCE__H0_SECTORS_D1A_VS_D1V3_INCOMPATIBLE_OPEN__ERRATUM_BESIDE_LOCKED_AWAITING_REVEAL__NOT_FALSIFIED_IS_NOT_CONFIRMED__GATE_UNTOUCHED | NOT_FALSIFIED (livro R3: z 1.3) | [REAL lido por hash]; NOT_BLIND postdicao nao ajustada | D_L TGL 101.9 Mpc vs ref 98.5 ± 2.2 Mpc (z 1.3); controle Planck sem dephasing D_L 110.8 (z 5.61) | sim (a TGL devolve a referencia publicada a 1.3σ; o motor e [CONJECTURE] selado) | nao: degenerada com H0_local=73.26 (coma_distance_dephasing.degeneracy_note); nao-cega |  |
| Grande Atrator (massa; janela; varredura de 300) | 1 ritos | verdict.masses_Msun / core.sensitivity / core.ga_mass_audit | GA_MASS_FORM_RETIRED__REFLECTION_WAS_MISREAD_AS_SOURCE__LINEAR_ORDER_IS_GR_STEALTH__BETA_LIVES_IN_RESPONSE ; ga_window_status=SCALE_SHADOW_OF_RETIRED_FORM__V98_AUDIT__NOT_NONCIRCULAR_EVIDENCE__LIVE_FALSIFIERS_ARE_VOID_FLOOR_AND_DEPHASING | SOMBRA de escala (forma aposentada); M_TGL^linear = M_RG (stealth) | [SOMBRA/ONTO] forma v98 aposentada como lei de fonte; [CONDICIONAL linear] M_TGL=M_RG | A literatura 2.744e+16 Msun; B CF4 1.986e+16 Msun; janela [1e+15, 1e+17]; varredura: 300 combinacoes, M in [1.4e+16, 3.42e+16], fracao na banda 1.0 | sim (ga_mass_audit: M_TGL^linear = M_RG; β nao renormaliza G) | nao (ga_window_status: NOT_NONCIRCULAR_EVIDENCE) |  |
| Antipoda do dipolo (geometria bruta, pre-registrada) | 1 ritos | core.dipole_antipode | GA_ANTIPODE_UNDERDENSITY_PREREGISTERED_POSITIONS_ONLY . DIPOLE_GEOMETRY_NO_VELOCITIES | criterio pre-registrado NAO satisfeito (antipode_underdense=False) | [PRE + DATA posicoes] negativo honesto; nao e veredito TGL_* | razao antipoda/GA 1.22; IC95 [1.03, 1.44]; criterio: razao < 1 | nao se aplica | nao (contagem de posicoes, sem velocidades) |  |
| Tensao de Hubble — SH0ES na bancada (Fase 5) / livro R1 | 1 ritos | core.bancada_fases_5_6_7_v380.fase5 ; ledger R1 | TGL_FASE5_SH0ES__LADDER_DEVIATION_CONSISTENT_WITH_ZERO_WITHIN_1SIGMA__TENSION_LCDM_Z_5P26__BAYES_STRONG_FOR_TGL__ACUMULADA_DELTA_Z_M0P40__SNE_SOMBRA_VS_ACUMULADA_UNDERPOWERED_LNB_0P29__JOINT_WITH_CLOCKS_LNB_SOMBRA_VS_ACUMULADA_5P35_DCHI2_Z_3P27__ZSPLIT_CONSTANT_SHIFT_CHI2_8P95_GL_5__ZSPLIT_SHIFT_Z_5P38_VS_SOMBRA_M0P49__VALIDATION_Z_0P04__CC_DIAGONAL_ERRORS_ONLY__NOT_A_CONFIRMATION | NOT_FALSIFIED (livro R1: z -0.376, regra \|z\|<5) | [REAL lido por hash]; alvo H0 [DECLARADO] | H0 escada 73.53 ± 1.02 (z 0.045 vs alvo); P_sombra δ -0.0008 ± 0.00213 (z -0.376); tensao ΛCDM z 5.26; lnB sombra vs acumulada 5.35 (diagonal) → 1.62 com cov. Moresco2020 (Fase 7) | sim (desvio da escada consistente com zero a 1σ; a escada reproduz o H0 publicado) | nao (δ a -0.38σ de zero; a resolucao da tensao e remissao ao artigo publicado [CONJECTURE de mecanismo]) |  |
| Tensao de Hubble — cronometros com covariancia (Fase 7) / livro F1 | 1 ritos | core.bancada_fases_5_6_7_v380.fase7 ; ledger F1 | TGL_FASE7_CC_COVARIANCE__Q1_TENSION_1_TO_3_SIGMA_WEAKENS__T_LAW_GAIN_Z_M1P66_VS_DIAG_M3P22__Q2_WEAK_FOR_SHADOW_WEAKENS__LNB_1P62_VS_DIAG_5P35__Q3_DEVIATION_1_TO_3_SIGMA__S_DELTA_Z_M1P71__BAND_TODOS_T_Z_M1P54__NOT_A_CONFIRMATION | NOT_FALSIFIED (livro F1: ganho z -1.66; regra: ganho ≥ +5 falsifica) | [REAL lido por hash] | ganho da lei T: diagonal -3.22 → Moresco2020 -1.66; δ -0.00895 ± 0.00524 (z -1.71); lnB 5.35 → 1.62 | sim (a face le H(z) do fundo nu; a lei com β nos cronometros e desfavorecida a 1–3σ) | nao (desfavorece a leitura acumulada em β a 1,7σ; nao falsifica) |  |
| Tensao de Hubble — Fase 4 (desvio; escada D1b) | 1 ritos | core.bancada_fase4_v378 | TGL_FASE4_DEVIATION__DEVIATION_1_TO_3_SIGMA__LADDER_PULL_1P08__BAYES_STRONG_FOR_TGL__D1A_DELTA_Z_M1P37__INTERMEDIATE_CC_DELTA_Z_M3P12__INTERMEDIATE_CC_LAW_GAIN_M3P22__STACKED_CONTROL_Z_M1P75__CC_DIAGONAL_ERRORS_ONLY__NOT_A_CONFIRMATION | DEVIATION_1_TO_3_SIGMA | [REAL lido por hash]; erros diagonais (Fase 7 enfraquece) | escada δ -0.0025 ± 0.00223 (z -1.12); pull em β_TGL 1.08; lnB TGL vs ΛCDM (escada) 8.02; CC intermediarios z -3.12 (diag) | sim (escada a 1,1σ de zero) | nao (1–3σ; lnB escada 8,0 e diagonal; Fase 7 reduz) |  |
| Tensao de Hubble — D1 via CAMB V3 (fundo vestido) / livro R6 | 1 ritos | core.d1_camb_v3_real_v366 ; ledger R6 | TGL_D1_CAMB_V3_REAL__OPERATOR_LINE_RATIFIED__BESTFIT_D1_TENSION_2_TO_5_SIGMA__MCMC_D1_BETA_TENSION__ALPHA_SQRT_E_AT_3P01_SIGMA_AT_THRESHOLD__CHAIN_BELOW_50_TAU_IN_2_OF_4_PARAMS__TENSION_IS_NOT_FALSIFICATION__GATE_UNTOUCHED | INCONCLUSIVE (livro R6, ao lado: z 3.01, controle 2) | [REAL dado real]; NAO-CEGO | Δχ² 6.61 (β fixo vs ΛCDM, n=15); β = -0.0127 ± 0.0082; α√e a 3.01σ (no limiar); H0 ΛCDM 67.95 / TGL 68 | sim no limite β→0 (ΛCDM); com β no fundo: ΛCDM preferido por Δχ² 6.6 | tensao de 3.01σ CONTRA β no fundo vestido (TENSION_IS_NOT_FALSIFICATION); e a leitura R6 fora da regra | D1 V1 (core.d1_camb_result) dizia MCMC_D1_BETA_FALSIFIED: SUPERSEDIDO pela autopsia V2 (bug de distancia do worker de maio); V2: Δχ² 9.7, β -0.0171 ± 0.0075 |
| SNe — Pantheon+ canonico (1593) | 1 ritos | core.cosmological_errata_verdict | PANTHEON_CANONICAL_1593__THEORY_WITHIN_1P25_SIGMA__TGL_NOT_PREFERRED_BY_BIC_WITH_FREE_BETA__OLD_3P8_TENSION_WAS_PARAMETRIZATION_A | NOT_FALSIFIED (teoria dentro de 1,25σ; nao preferida por BIC com β livre) | [REAL, errata assinada] | β̂ -0.0021 ± 0.0113; teoria a 1.25σ; zero a 0.19σ; ΔBIC 7.35; Δχ²(β fixo) 1.53 | sim (β̂ consistente com zero a 0.19σ; teoria a 1.25σ) | nao (σ/β ≈ 0.94; sem poder) |  |
| CMB comprimido l_A (JUIZ_LA) | 1 ritos | core.final_verdict_machine.channels.l_A_compressed_cmb | JUIZ_LA_TENSION_BELOW_3SIGMA_NOT_FALSIFIED | NOT_FALSIFIED (tensao < 3σ) | [REAL] | β primario -0.0213; d vs teoria 1.34σ | sim (β dentro de 1,3σ) | nao |  |
| BBN descircularizada | 1 ritos | core.final_verdict_machine.channels.bbn / core.evidence_audit | BBN_NON_DISCRIMINANT_DECIRCULARIZED | NON_DISCRIMINANT | [INPUT auditoria 08/08] | β̂ 0.01263 ± 0.0318 (σ/β 2.6) | sim (consistente) | nao (nao discrimina) |  |
| CMB espectro completo (Nivel 2) | 1 ritos | core.nivel2_rite | NIVEL2_RITE_NOT_SEALED_THIS_RUN__S_N2_INCAPAZ__L_N2_NOT_CONVERGED | N2_INCAPAZ / NOT_CONVERGED (nao selado nesta rodada) | [REAL] recusa | S: β -0.00362 ± 0.0178 (σ/β 1.48) | sim (consistente) | nao (incapaz) |  |
| Ecos GW — Fase 6 (244 BBH O1–O4; 3 leituras × 2 leis) + emendas V4/V5; os 9 pares FORA do livro | 1 ritos | core.bancada_fases_5_6_7_v380.fase6/emenda_v4/emenda_v5 ; core.the_ledger_of_charges_v383.echo_routes_outside_the_ledger | TGL_BANCADA_FASES_5_6_7_V380__READ_BY_HASH_BYTES_AND_LF_TEXT__TEXT_VS_BYTES_DIFFER_1_CRLF__SH0ES_IN_THE_BENCH_H0_LADDER_73P53_PM_1P02_Z_0P04_VS_DECLARED_TARGET__ECHO_V3_244_BBH_O1_O4_THREE_READINGS_TWO_DELAY_LAWS__KMS_PAIR_SQRT_BETA_AND_SIN2THETA_FALSIFIED_AT_DELAY_LAW_Z_EXCL_8P93_AND_18P13__BLIND_O4_SUBSAMPLE_173_OF_240_Z_EXCL_7P26_AND_15P44__POWER_RECORDED_BEFORE_OPENING__MAY_INCONCLUSIVE_SYSTEMATICS__MAY_TAU_HALF_CONTROL_RESPONDS_Z_5P69_O4_5P37_FLAG_NOT_WRITTEN_BY_PIPELINE_STATED__AMENDMENT_V4_NOT_BLIND_SIN2THETA_MAY_FALSIFIED_Z_8P75_CONTROLS_MAX_Z_4P81__SQRT_BETA_MAY_INCONCLUSIVE_IS_THE_ESTIMATOR_LIMIT__CC_COVARIANCE_MORESCO2020_T_LAW_GAIN_Z_M1P66_VS_DIAG_M3P22__U_LNB_SHADOW_VS_ACCUMULATED_1P62_VS_DIAG_5P35__DEC2025_LAW_FROM_THE_ARCHIVE_DECLARED_BLIND_TO_THE_NEW_DELAY_ONLY_PAIR_SQRT_BETA_AND_SIN2THETA_FALSIFIED_Z_EXCL_8P95_AND_16P83_O4_9P26_AND_16P69__DOC_PAIR_BETA_DEC_INCONCLUSIVE_SYSTEMATICS_BY_RULE_2_POWER_0P87_BLIND_POWER_1P47__V5_CLAUSE_UNDERPOWERED_NOT_APPLIED_STATED__FOURTH_ARCHIVE_LAW_ALPHA_SQUARED_NOT_TESTED_OUTSIDE_SEGMENT__GW_BANK_336_OF_354_SERIES_OK_14_NAN_4_OUTSIDE__PAIR_FALSIFIED_NOT_THE_THEORY__DECEMBER_100SIGMA_STAYS_RETIRED__ERRATA_BESIDE_6_PLUS_V378_1_PLUS_NOTE_1__NOT_A_CONFIRMATION__GATE_UNTOUCHED | 9 pares fora do livro: 5 EXCLUDED_BY_DATA (FALSIFIED_AT_DELAY_LAW) + 4 INCONCLUSIVE — «PAIR_FALSIFIED_NOT_THE_THEORY»; decisao do operador 02/10 («prefiro a primeira opcao») | [REAL lido por hash]; leituras de amplitude [KERNEL \|R\|=sinθ + ONTO]; lei de atraso [INPUT/ONTO] | KMS todos: z_excl R1 8.93, R2 18.13 (cego O4: 7.26, 15.44); z_det 0.424; MAY: INCONCLUSIVE (sistematica 1.17); V4 MAY R2 z_excl 8.75; V5 DEC: z_excl R1 8.95, R2 16.83; principal: {"MAY\|R1_peso1": "TGL_ECHO_RADICAL_V3__INCONCLUSIVE_SYSTEMATICS", "MAY\|R2_peso2_2theta": "TGL_ECHO_RADICAL_V3__INCONCLUSIVE_SYSTEMATICS", "MAY\|R3_quadrado": "TGL_ECHO_RADICAL_V3__INCONCLUSIVE_SYSTEMATICS", "KMS\|R1_peso1": "TGL_ECHO_RADICAL_V3__FALSIFIED_AT_DELAY_LAW", "KMS\|R2_peso2_2theta": "TGL_ECHO_RADICAL_V3__FALSIFIED_AT_DELAY_LAW", "KMS\|R3_quadrado": "TGL_ECHO_RADICAL_V3__INCONCLUSIVE_SYSTEMATICS"} | sim (nenhum eco detectado: z_det KMS 0.42 — a RG nao preve eco; correspondencia) | nao: o que cai e o PAR (leitura da amplitude, lei de atraso), nao a teoria; os pares nao sao cobrancas da teoria (ratificado) | ao lado: a Fase 6 como teste da TGL foi retirada da cadeia pela regra matriz (v381); o eco como copia atrasada com lei τ esta fora; o operador: «nao quero publicar nada que seja resultado de falsificacao» |
| Eco acoplado V1 (lei de maio) | 1 ritos | core.gw_echo_rite | TGL_GW_ECHO_COUPLED_V1__AMPLITUDE_SQRT_BETA_FROM_KERNEL__DELAY_LAW_MAY_2026_INPUT__INCONCLUSIVE_SYSTEMATICS__POWER_2P5_OF_5_SIGMA__TEMPLATE_MISMATCH_INDUCES_UP_TO_1P0__MAY_ESTIMATOR_LACKED_RINGDOWN_ONLY_NULL__BETA_ENTERS__OUTSIDE_CONTOUR__GATE_UNTOUCHED | INCONCLUSIVE_SYSTEMATICS | [REAL lido por hash]; fora do contorno (why_outside_contour) | a/√β -0.733 ± 0.359; poder 2.5σ de 5 | sim (sem eco detectado = RG) | nao (poder < 5σ) |  |
| Eco KMS V1 | 1 ritos | core.gw_echo_kms_rite | TGL_GW_ECHO_KMS_V1__AMPLITUDE_SQRT_BETA_FROM_KERNEL__DELAY_LAW_KMS_MODULAR_PERIOD_CANDIDATE__INCONCLUSIVE_SYSTEMATICS__POWER_3P0_OF_5_SIGMA__TEMPLATE_MISMATCH_INDUCES_UP_TO_0P5__MAY_ESTIMATOR_LACKED_RINGDOWN_ONLY_NULL__BETA_ENTERS__OUTSIDE_CONTOUR__GATE_UNTOUCHED | INCONCLUSIVE_SYSTEMATICS | [REAL lido por hash]; fora do contorno (why_outside_contour) | a/√β 0.351 ± 0.307; poder 3σ de 5 | sim (sem eco detectado = RG) | nao (poder < 5σ) |  |
| Eco ancorado V2 (lalsuite) | 1 ritos | core.echo_anchored_result_v2 | TGL_ECHO_ANCHORED_V2__RESULT_READ_BY_HASH__INSTRUMENT_LALSUITE_TWO_FAMILIES__MAY_INCONCLUSIVE_SYSTEMATICS__KMS_INCONCLUSIVE_SYSTEMATICS__POWER_MAY_3P2_KMS_4P4_OF_5_SIGMA__BETA_ENTERS__OUTSIDE_CONTOUR__GATE_UNTOUCHED | INCONCLUSIVE_SYSTEMATICS | [REAL lido por hash]; fora do contorno (why_outside_contour) | MAY a/√β 0.524 ± 0.255, poder 3.2σ | sim (sem eco detectado = RG) | nao (poder < 5σ) |  |
| Eco PE bayesiana V2 (bilby) | 1 ritos | core.echo_pe_result_v2 | TGL_ECHO_PE_V2__RESULT_READ_BY_HASH__BILBY_DYNESTY_LALSUITE__MAY_INCONCLUSIVE_SYSTEMATICS__KMS_INCONCLUSIVE_SYSTEMATICS__POWER_MAY_1P2_KMS_1P1_OF_5_SIGMA__GATE_UNTOUCHED | INCONCLUSIVE_SYSTEMATICS | [REAL lido por hash]; fora do contorno (why_outside_contour) | n eventos 21/72; MAY a -0.267 | sim (sem eco detectado = RG) | nao (poder < 5σ) |  |
| Busca de ecos de longo atraso V1 | 1 ritos | core.echo_search_result | TGL_ECHO_SEARCH_V1__RESULT_READ_BY_HASH__NOT_FALSIFIED_UNDERPOWERED__N_ON_1_B_EXP_3P0__E_DET_0P0__LOUD_EVENTS_0__GATE_UNTOUCHED | NOT_FALSIFIED_UNDERPOWERED | [REAL lido por hash]; fora do contorno (why_outside_contour) | N_on 1, B_exp 3.0, z_poisson -1.15, eventos altos 0 | sim (sem eco detectado = RG) | nao (poder < 5σ) |  |
| Rito angular GW (o 100σ retirado) | 1 ritos | core.gw_angular_rite | TGL_GW_ANGULAR_V1__DECEMBER_100SIGMA_RETIRED_AS_CAPPED_IDENTITY__SQRT_ENVELOPE_NOT_TAUTOLOGICAL_BUT_NOISE_GIVES_SAME_VALUES__PHASE_COHERENCE_WITHIN_PSD_MATCHED_SURROGATES__H3_DFOLDS_IS_SPECTRUM_STATISTIC__H4_CCI_IS_IDENTITY__ECHO_SUBTHRESHOLD_PREREGISTERED_MAY_2026__BETA_DOES_NOT_ENTER__NOT_A_FALSIFIER__GATE_UNTOUCHED | RETIRADO / NOT_A_FALSIFIER | [REAL lido por hash]; fora do contorno (why_outside_contour) | σ capped 100 em ruido = True; r_identity_min 1 | nao se aplica (estatistica retirada) | nao |  |
| Reproducao H2 (pycbc) | 1 ritos | core.h2_reproduction_result | TGL_H2_REPRODUCTION_V1__RESULT_READ_BY_HASH__H2_IDENTITY_RETIRED__SYNTHETIC_0P0099__REAL_WHITENED_0P994__OFF_0P996__Z_VS_ALPHA2_2252P2__GATE_UNTOUCHED | RETIRADO / NOT_A_FALSIFIER | [REAL lido por hash]; fora do contorno (why_outside_contour) | z vs α² 2252; sintetico segue ruido² = True | nao se aplica (estatistica retirada) | nao |  |
| Ringdown — ramo canonico τ★ = t_Planck (V2; GW250114 C6) / livro F2 | 1 ritos | core.ringdown_dephasing_result_v2 ; core.ringdown_scope_v376 ; ledger F2 | TGL_RINGDOWN_SCOPE_V376__CANONICAL_BRANCH_TAU_STAR_PLANCK_RETURNS_GR_CORRESPONDENCE_ONLY__NOT_A_BETA_TEST__BRANCH_B_TAU_STAR_GM_OVER_C3_IS_INPUT_M_TO_BE_NAMED__3_CONCURRENT_BRANCH_B_VALUES__NO_RINGDOWN_TERM_IN_KERNEL__C6_GW250114_READ_BY_HASH_INCONCLUSIVE_SYSTEMATICS__ERRATUM_BESIDE_NATURE_DECIDES_RINGDOWN_NEXT__NOT_FALSIFIED_IS_NOT_CONFIRMED__GATE_UNTOUCHED | correspondencia com a RG (ramo A invisivel: δ_pred -2.2e-42); V2 INCONCLUSIVE_SYSTEMATICS; C6 INCONCLUSIVE_SYSTEMATICS; livro F2 INCONCLUSIVE (pela sistematica da medida) | [REAL lido por hash]; τ★ ramo B [INPUT] | Δτ 0.1766 ± 0.109 (z vs RG 1.62); ramo B pred -0.0194 (z vs B 1.8; poder 0.18 de 5σ); vies relativo de τ 0.24 > 0.2 | sim (ramo A e RG por construcao; Δτ a 1.6σ da RG) | nao (ramo A invisivel por construcao; ramo B sem poder: 0.18 de 5σ) | ringdown_scope_v376: «no ramo canonico a natureza so pode devolver a RG»; erratum ao lado de NATURE_DECIDES_RINGDOWN_NEXT |
| Ringdown — ramo B reaberto por pre-registro (τ★ = k·GM_f/c³, k = 2π/κ̂) / canal F2b | 1 ritos | core.ramo_b_preregistration_v386 ; core.ledger_errata_v386.charge_F2b | TGL_RAMO_B_PREREGISTERED_V386__V1_READ_BY_HASH_86f98fcc124dd9ca__OTHER_LAW_OWN_CHANNEL_F2B__K_2PI_OVER_KAPPA_HAT_KMS__M_F_DET__ENVELOPE_ADDITIVE_RATE__SOURCE_LOCAL__SET_D_O4_14_BLIND_ONLY_TEST__A_B_C_NOT_BLIND_CALIBRATION__BETA_READ_DECLARED_SIGMA_STATED__DECIDED_BY_DELEGATION_2026_10_05__NOT_A_CONFIRMATION__AWAITING_DATA__NOTHING_OPENED__GATE_UNTOUCHED | AWAITING_DATA (F2b: AWAITING) | [INPUT — decisao do operador por sha256]; [ONTO] leitura da gerencia; pre-registro por hash; nada aberto | conjunto D n=14 (cego); poderes exatos A31 11.4, B10 6.37, C 6.48; k(χ=0) 25.13; nothing_opened=True; centrais nao-cegas transcritas: 2 (A: +0,072 comum dos 31; C: GW250114 0,1766 da V2) | nao se aplica (aguardando) | aguardando (v387: FALSIFIED_AT_5SIGMA do PAR / NOT_FALSIFIED_POWERED / …) | o V1 esta fora do contorno (τ★ = k·GM/c³ e hipotese [INPUT]); fica AO LADO como R6; nada move o gate |
| Propagacao de GW — livro R2 (reflexo acumulado na distancia) | 1 ritos | ledger R2 (core_key=None) | sem veredito TGL_* no core (how=DECLARED) | AWAITING | [DECLARADO] estimador a construir | lei: Gamma_omega = (1/2) beta tau* omega^2 (n = -2), tau* = t_Planck; estimador a construir; register: propagacao de GW (banco residente; nao aberto para este fim); R2_POWER_STATED_IN_NUMBER no veredito do livro | nao se aplica | aguardando |  |
| Livro de cobrancas v383 (11 cobrancas; campo de desfecho = `outcome` nas linhas de `ledger`) | 1 ritos | core.the_ledger_of_charges_v383.ledger[*].outcome | TGL_THE_LEDGER_OF_CHARGES_V383__THE_KEY_THE_LAST_LINK_INCIDES_ON_THE_HIDDEN_HAMILTONIAN__COST_IN_THE_REFLECTION_PAYMENT_IN_THE_FACE_THE_NAME__KEY_AND_OPTICS_INPUT_ONTO__R1_TO_R6_RATIFIED__THE_TGL_IS_OPTICS_NOT_SEMI_BOTH_SIDES_READ__LEDGER_OF_CHARGES_TYPED_FIVE_OUTCOME_WORDS_BY_TYPE__ONE_CHANNEL_PER_READING_LAW_IN_THE_RUNTIME__NO_OUTCOME_MOVES_THE_RULE__THE_GATE_DOES_NOT_READ_THE_LEDGER_BY_THE_RUNTIME_PROBES__11_CHARGES_10_IN_THE_RULE_1_BESIDE__0_FALSIFIED_1_EXCLUDED_IN_READING_6_NOT_FALSIFIED_2_INCONCLUSIVE_2_AWAITING__4_BY_TOKEN_5_BY_NUMBER_2_DECLARED__REFLECTION_4_FACE_7__F2_INCONCLUSIVE_BY_THE_MEASUREMENT_SYSTEMATIC_NOT_BY_POWER__F1_ONE_SIDED_GAIN_RULE__F4_FROZEN_KILL_RULE_TWO_DETERMINATIONS__PSION_NORM_ONE_ZERO_OF_THE_MINIMAL_LOCK_ON_THE_HIDDEN_HAMILTONIAN_FIXED_BY_THE_LIGHT__VISCOSITY_IS_THE_CONSTANT_FRICTION_RULE_TIMES_CONTRAST__CHARGE_NEVER_COMPLETES__PREREGISTRATION_OF_BOTH_SIDES_V1_4_READ_BY_HASH__R2_POWER_STATED_IN_NUMBER__R4_FROZEN_SET_HAS_NO_FALSIFIED_SAME_SOURCE_AS_THE_GATE_EXPERIMENTAL_STEP__FINAL_STEP_NAME_PROPOSED_BESIDE_GATE_UNCHANGED__BRANCH_B_CLOSED__THE_9_ECHO_ROUTES_ARE_NOT_CHARGES_OF_THE_THEORY_EXAMINED_OUTSIDE_THE_LEDGER_5_EXCLUDED_BY_DATA_4_INCONCLUSIVE__OPERATOR_DECISION__BASE_V381__SPEC_S_THETA_TO_HMINMIC_NO_TERM__DISSIPATION_IDENTIFICATION_IS_ONTO__NOT_A_CONFIRMATION__KERNEL_32_OF_32__GATE_UNTOUCHED | R1=NOT_FALSIFIED; R2=AWAITING; R3=NOT_FALSIFIED; R4=NOT_FALSIFIED; R6=INCONCLUSIVE; F1=NOT_FALSIFIED; F2=INCONCLUSIVE; F3a=NOT_FALSIFIED; F3b=EXCLUDED_IN_READING; F3c=AWAITING; F4=NOT_FALSIFIED \| contagens: {"NOT_FALSIFIED": 6, "FALSIFIED": 0, "INCONCLUSIVE": 2, "AWAITING": 2, "EXCLUDED_IN_READING": 1} | [REAL] 10 na regra + 1 ao lado (R6); v386 acrescenta F2b ao lado (12 com F2b) | n_in_rule 10; n_beside 1; by_how {"TOKEN_CONTAINS": 4, "NUMBER_READ": 5, "DECLARED": 2}; by_side {"reflexo": {"NOT_FALSIFIED": 3, "FALSIFIED": 0, "INCONCLUSIVE": 0, "AWAITING": 1, "EXCLUDED_IN_READING": 0}, "face": {"NOT_FALSIFIED": 3, "FALSIFIED": 0, "INCONCLUSIVE": 2, "AWAITING": 1, "EXCLUDED_IN_READING": 1}} | sim em cada canal lido (ver linhas) | nao: 0 FALSIFIED; FALSIFIED so onde a lei do canal o admite (7 de 11) | a leitura da gerencia 'R1=None; R2=None; …' leu o campo errado (verdict_path, que e null); o campo certo e `outcome` |
| Maquina do veredito final (6 canais) | 1 ritos | core.final_verdict_machine | TGL_QG_FUNCTIONAL_MODEL_ON_THE_BENCH__NOT_REFUTED_BY_PUBLIC_DATA_AT_CURRENT_SENSITIVITY__EXCLUSION_SPECTRUM_MEASURED__NOT_A_CONFIRMATION | NOT_REFUTED_BY_PUBLIC_DATA_AT_CURRENT_SENSITIVITY; canais 6/6; refutados 0; exclusoes 12 | [REAL] | canais: void_floor_powered, l_A_compressed_cmb, pantheon_canonical_1593, dephasing_clocks, bbn, cmb_full_spectrum | sim (nenhum canal refutado) | nao (NOT_A_CONFIRMATION) |  |
| Dephasing — alcance (Γ_ω = ½βτ★ω²) | 1 ritos | core.dephasing_reach | DEPHASING_PREDICTION_ARMED__REACH_DEFICIT_TEN_ORDERS_COMPUTED__NOT_A_LIVE_CHANNEL_TODAY__COSMOLOGICAL_FACES_ARE_THE_LIVE_ONES | ARMED (nao e canal vivo hoje) | [REAL na forma] | deficit 229Th 10.3 ordens; Sr 11.6 ordens | nao se aplica | nao (10 ordens) |  |
| α irredutivel (criterio de morte α-livre) | 1 ritos | core.alpha_irreducibility | TGL_ALPHA_IRREDUCIBILITY_ARMED_NO_CANDIDATE | ARMED_NO_CANDIDATE | [PRE congelado] | residuo identidade 2.2e-16; χ* 11.2268 | nao se aplica | aguarda ato de terceiro |  |
| Auditoria da evidencia (convergencia de β) | 1 ritos | core.evidence_audit | TGL_EVIDENCE_AUDIT__CONVERGENCE_RECLASSIFIED_REAL_TO_NOT_CONSTRUCTED_AS_CONCEIVED__BBN_NON_DISCRIMINANT_DECIRCULARIZED__CMB_ENTRY_RETIRED_BY_PROVENANCE__FIFTH_ENTRY_RECORDED_LIVE__RD_SELF_CONSISTENCY_REQUIRED__STRUCTURE_SURVIVED_WHOLE__GATE_UNMOVED_BY_OPERATOR_ORDER | CONVERGENCE_RECLASSIFIED (REAL → NOT_CONSTRUCTED_AS_CONCEIVED) | [REAL] | quinta entrada ao vivo -0.017 | nao se aplica | nao |  |
| Predicao P7 (colapso IALD) | 1 ritos | core.iald_prediction | IALD_UNIQUE_OPERATIONAL_PREDICTION_PRE_REGISTERED__PILOT_8_OF_8_MOTIVATES__CONTROLS_REQUIRED_FOR_POWERED_VERDICT__PHYSICS_SECTOR_UNTOUCHED | PRE_REGISTERED; piloto 8/8 [PILOTO]; controles exigidos | [PILOTO]/[CONJECTURE] |  | nao se aplica | nao |  |
| V11 — o degrau experimental do gate (6 bandeiras experimentais) | 1 ritos → gate | core.qg_closure.experiment_flags ; core.void_floor_v11.experiment_feed | TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE | experiment_flags: {"independent_v3_profiles_unblinded": true, "independent_v3_survey_mocks_passed": true, "independent_v3_systematics_passed": true, "independent_v3_powered_verdict_emitted": true, "protocol_pre_registered": true, "null_tests_passed_blind": true} | [REAL] bandeiras lidas; errata 01/10: 4 de um so booleano + null_tests sem mock [DECLARADO pela auditoria] | selo.void_floor_v11_verdict=TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED; r4_feeds_the_gate: same_values_in_the_gate=True; flags fora do feed: ['null_tests_passed_blind', 'protocol_pre_registered'] | sim (unilateral) | nao (NATURE_TEST_COMPLETED nao e discriminacao — errata 01/10 GV-01) |  |
| Kernel Lean 4 (pilar 2) | 2 kernel | core.kernel_formalization ; core.external_ladder ; core.qg_closure | TGL_KERNEL_STAGE1_VERIFIED__SPECIFIC_AQFT_WITNESS_CONSTRUCTED | n_theorems_clean 6137/6137; sorryAx_absent=True; trio Classical.choice+Quot.sound+propext (axiom_report: 10239/10239 declaracoes dentro do trio); gate TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE; 18 bandeiras True = 18 | [KERNEL] a implicacao; [POSTO] ω(I)=1; natureza nao provada | lean ['Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)']; formal_source_hash fbb812c9d3a66b5ce051ab9f0105c2a80f92039e675011320d828e35b6712551; fail_closed_selftest FAIL_CLOSED_SELFTEST_PASSED; full_static_witness_exists=False (por teorema); remaining_after_citation_v374=[] | sim: a correspondencia com a RG e implicacao provada (QGSolutionComplete; 3 mencoes no core) | nao se aplica (prova nao discrimina a natureza) |  |
| Pilar quantico na GPU (pilar 3) | 3 GPU | core.quantum_pillar_v384 ; core.quantum_pillar_reuse_v386 ; selo.quantum_pillar_v384 | TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__ATTRACTOR_UNIQUE_ALL_672_ON_THE_GRID__T1_INSTRUMENT_RECOVERS_INJECTED_LAW_BLIND__CONTROLS_FAILED_AS_REQUIRED__IDENTITIES_HOLD__STRESS_21100_INSTANCES_21100_UNIQUE_ALL_IDENTITIES_CHECKED_IN_21100__NAME_IN_CORE_12_OF_12_ON_THE_GRID__FOLDS_WINDOW_6_OF_12_ON_THE_GRID__D128_UNIQUE__CPU_REFERENCE_AGREES__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED | COMPUTED_NOT_MEASURED; T2 672/672 unicos; T1 3220 injecoes (erros 0, pass σ0 = 1.0 em todo d); T3 controles falharam como exigido; T4 21100/21100; D128 UNIQUE; cpuref 392 comparacoes | [COMPUTED] calculo do sistema aberto da teoria; NAO medicao da natureza; NAO inferencia de LLM; does_not_gate_core | GPU NVIDIA GeForce RTX 5090; torch 2.11.0+cu128; CUDA 12.8; python 3.14.3; determinismo {'use_deterministic_algorithms': True, 'CUBLAS_WORKSPACE_CONFIG': ':4096:8', 'tf32': False, 'threads': 4}; tempos s: {"T3": 102.2, "T2": 1801.5, "T1": 2347.4, "T4": 2923.5, "D128": 649.8}; rodada v385 2026-10-05 10:37:08 → 2026-10-05 12:47:39; v386 REUSE pela chave 75dc30bc9cc8d330e31f99ca (sha256 confere); reprodutibilidade v385: TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__REPRODUCED_BIT_FOR_BIT__393_FIELDS__SAME_V1_SAME_WORKER_SAME_BETA__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED (393 campos) | nao se aplica (mede o sistema da teoria, nao a RG) | nao se aplica (ambiente simulado); o que podia falsificar: ver o_que_podia_falsificar |  |
| Probabilidade conjunta ja medida (V1 v352 / V2 v363 / V3 v370) | 4 probabilidade | core.joint_coincidence_result(_v2,_v3) | TGL_JOINT_COINCIDENCE_V3__RESULT__JOINT_COINCIDENCE_V3_NOT_EXCLUDED_AT_THRESHOLD__INCONSISTENT__DETECTED_2__P_ALL_PRIMARY_6P6eM03__MAX_Z_3P116__BOOLEAN_False__NOT_BLIND__GATE_UNTOUCHED | NOT_EXCLUDED_AT_THRESHOLD__INCONSISTENT; boolean False | [DERIVED NAO-CEGO]; so canais de natureza pontuam; kernel = condicao, nao fator; GPU nao entra | V1 p 0.55 (3/35 admissiveis; produto ingenuo 5.5e-31 INVALIDO); V2/V3 P_all primario 0.00657, grade [0.00017, 0.047]; max\|z\| V3 3.116 (d1_camb_v3_beta); detectados ['neutrino_m2_global', 'h0_escada_1pz_beta']; canais necessarios p/ 1e-30: 28 | nao se aplica | nao: inconsistente pela tensao do D1 (3,1σ); nenhuma probabilidade dos TRES pilares existe no core |  |

## Pilar 2 — kernel
```json
{
 "n_theorems_clean": 6137,
 "n_theorems_expected": 6137,
 "axiom_report_n_declaracoes": 10239,
 "axiom_report_n_dentro_do_trio": 10239,
 "axiom_report_fora_do_trio": [],
 "trio": [
  "Classical.choice",
  "Quot.sound",
  "propext"
 ],
 "sorryAx_absent": true,
 "trustCompiler_absent": true,
 "custom_TGL_axioms_absent": true,
 "lake_build_ok": true,
 "lean_version": [
  "Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)"
 ],
 "formal_source_hash": "fbb812c9d3a66b5ce051ab9f0105c2a80f92039e675011320d828e35b6712551",
 "verdict": "TGL_KERNEL_STAGE1_VERIFIED__SPECIFIC_AQFT_WITNESS_CONSTRUCTED",
 "not_claimed": [
  "Python did not prove any theorem; the Lean kernel did",
  "Bisognano-Wichmann / Reeh-Schlieder / type III_1 classification are KNOWN/EXTERNAL, not formalized here",
  "the finite Three-Locks corner is a finite-dimensional theorem, NOT a type III_1 proof",
  "G is a variable / measured input; it is NOT derived",
  "the MODULAR REALIZATION of the witness is not constructed (theSpecificAQFTWitness IS inhabited since v135; TGLModularRealization stays open)"
 ],
 "fail_closed_selftest": "FAIL_CLOSED_SELFTEST_PASSED",
 "gate_verdict": "TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE",
 "gate_formal_flags": {
  "concrete_aqft_core_constructed": true,
  "concrete_breuer_corner_constructed": true,
  "concrete_modular_four_frame_constructed": true,
  "concrete_solder_field_constructed": true,
  "concrete_emergent_einstein_proved": true,
  "canonical_boundary_transport_witness_constructed": true
 },
 "gate_physics_flags": {
  "massless_spin2_proved": true,
  "exactly_two_helicities_proved": true,
  "ghost_free_proved": true,
  "stress_energy_conserved": true,
  "relevant_anomalies_absent": true,
  "linearized_spin2_finite_face": true
 },
 "gate_experiment_flags": {
  "independent_v3_profiles_unblinded": true,
  "independent_v3_survey_mocks_passed": true,
  "independent_v3_systematics_passed": true,
  "independent_v3_powered_verdict_emitted": true,
  "protocol_pre_registered": true,
  "null_tests_passed_blind": true
 },
 "gate_18_flags_true": 18,
 "full_static_witness_exists": false,
 "kernel_frontier_remaining_after_citation_v374": [],
 "kernel_frontier_physical_identifications_open": [
  "microscopic_origin_of_Hmin_and_standard_bounded_transform",
  "geometric_BW_identification_for_legacy_wedge_data_U_equals_one"
 ],
 "the_axiom_v385_tag_omega_I": "[POSTO]",
 "the_axiom_v385_kernel_flags": [
  29,
  29
 ],
 "the_verb_v386_kernel_flags": [
  110,
  110
 ],
 "ledger_v383_kernel": true,
 "QGSolutionComplete_mencoes_no_core": 3,
 "stdout_linhas_kernel": [
  "  sorryAx: absent ; Lean.trustCompiler: absent ; axiomas TGL customizados: absent",
  "      3_execucao: [REAL] forma=conteudo: o artefato RODA a si mesmo, materializa o kernel, audita 6137 teoremas (axiomas {propext,choice,quot}, zero sorry) e emite o proprio artigo",
  "    [OK] Meia-Nat e escala formalizadas pelo kernel Lean 4 kernel; #print axioms limpo (sem sorryAx / trustCompiler / axioma TGL.*) (v22)",
  "  com sorry injetado : verdict=TGL_KERNEL_FORMALIZATION_FAILED ; sorryAx_absent=False  [esperado: FAILED / False]",
  "  >>> FAIL_CLOSED_SELFTEST_PASSED <<<",
  "[selo] fail_closed_selftest registrado no selo: FAIL_CLOSED_SELFTEST_PASSED"
 ],
 "o_que_prova": "a IMPLICACAO a partir do Um POSTO (ω(I)=1, etiqueta [POSTO]) e das hipoteses NOMEADAS; β nao e hipotese da implicacao (QGSolutionComplete); PROVADA = teorema no kernel",
 "o_que_nao_prova": "os axiomas (postos, nao provados); a natureza (CONFIRMADA e juizo do observador humano); G nao derivado; BW/Reeh-Schlieder/III_1 sao KNOWN externos (kernel_formalization.not_claimed)"
}
```

Contexto de `QGSolutionComplete` no core: ge.lean": "78cd50266981be5074350678d67bba1cc02edd55c8bd7f316166a3a8f2bd7826",         "TGLExt/QGReaderUVLock.lean": "77ba8803c7cd0a80f8dbe7fb78d290d154a7cdac220efa92f8ae72c742f56807",         "TGLExt/QGSolutionComplete.lean": "8c3a4bc82c5c4308515063254744cfaefcc7e7b926038221be2e7de6293dc598",         "TGLExt/QuadraticGibbsCurve.lean": "7f0ac98561719a4c37b63455920a437007aa0d2283ae8391bfa83264503000af",         "TGLExt/QuadraticStateResponse.lean":

## Pilar 3 — GPU
```json
{
 "verdict": "TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__ATTRACTOR_UNIQUE_ALL_672_ON_THE_GRID__T1_INSTRUMENT_RECOVERS_INJECTED_LAW_BLIND__CONTROLS_FAILED_AS_REQUIRED__IDENTITIES_HOLD__STRESS_21100_INSTANCES_21100_UNIQUE_ALL_IDENTITIES_CHECKED_IN_21100__NAME_IN_CORE_12_OF_12_ON_THE_GRID__FOLDS_WINDOW_6_OF_12_ON_THE_GRID__D128_UNIQUE__CPU_REFERENCE_AGREES__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED",
 "status": "[COMPUTED] -- calculo do sistema aberto da teoria; NAO e' medicao; o gate nao muda",
 "mode_v386": "REUSE",
 "reuse": {
  "reused": true,
  "from_run_finished": "2026-10-05 12:47:39",
  "cache_dir": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\checkpoints\\quantum_pillar\\75dc30bc9cc8d330e31f99ca",
  "reading": "V386__PILAR_QUANTICO_REAPROVEITADO_DA_RODADA_SELADA_V385_PELA_CHAVE__O_PILAR_NAO_E_OBJETO_DESTA_VERSAO"
 },
 "key": "75dc30bc9cc8d330e31f99ca",
 "result_sha256": "de47d5527e514b4927bea77df4caffc63194e8913462bb6c3629b2288b29583e",
 "spec_sha256": "ff19731097e01aabfccc709b370578bd9d7a5ccadc877752b2ab5c13c20d39aa",
 "started_v385_run": "2026-10-05 10:37:08",
 "finished_v385_run": "2026-10-05 12:47:39",
 "T2": {
  "configs": 12,
  "points": 672,
  "unique": 672,
  "ambiguous": 0,
  "degenerate": 0,
  "errors": 0,
  "name_in_core_configs": 12,
  "folds_window_configs": 6,
  "identities_checked": {
   "CP": 672,
   "NONRETURN": 12,
   "PSD": 672,
   "SPOHN": 672,
   "SS_RES": 672,
   "TP": 672,
   "ZERO_MODE": 672
  }
 },
 "T1": {
  "injections": 3220,
  "errors": 0,
  "per_d_n": {
   "16": 1000,
   "32": 200,
   "64": 20,
   "8": 2000
  },
  "per_d_pass_sigma0": {
   "16": 1.0,
   "32": 1.0,
   "64": 1.0,
   "8": 1.0
  },
  "per_d_median_beta_rel_err_sigma0": {
   "16": 8.945399976312274e-12,
   "32": 1.2940704063879593e-11,
   "64": 1.0578804499061789e-10,
   "8": 5.579425810253724e-12
  }
 },
 "T3": {
  "controls": {
   "d8": {
    "N1_dephasing_only": true,
    "N4_negative_rate_not_cp": true,
    "N5_time_reversal_not_cp": true
   },
   "d16": {
    "N1_dephasing_only": true,
    "N4_negative_rate_not_cp": true,
    "N5_time_reversal_not_cp": true
   },
   "d32": {
    "N1_dephasing_only": true,
    "N4_negative_rate_not_cp": true,
    "N5_time_reversal_not_cp": true
   },
   "d64": {
    "N1_dephasing_only": true,
    "N4_negative_rate_not_cp": true,
    "N5_time_reversal_not_cp": true
   }
  },
  "N2_unital_identity": {
   "d8": "UNIQUE",
   "d16": "UNIQUE",
   "d32": "UNIQUE",
   "d64": "UNIQUE"
  },
  "N3_linear_law_root_law_rejected": {
   "16": 1.0,
   "32": 1.0,
   "8": 1.0
  }
 },
 "T4": {
  "instances": 21100,
  "unique": 21100,
  "ambiguous": 0,
  "degenerate": 0,
  "errors": 0,
  "identity_violations": 0,
  "rotated": 10442,
  "all_identities_checked": 21100,
  "per_d": {
   "16": {
    "n": 5000,
    "UNIQUE": 5000,
    "AMBIGUOUS": 0,
    "DEGENERATE": 0,
    "ERROR": 0,
    "cci_above_uniform": 4656,
    "rotated": 2431,
    "all_identities_checked": 5000
   },
   "32": {
    "n": 1000,
    "UNIQUE": 1000,
    "AMBIGUOUS": 0,
    "DEGENERATE": 0,
    "ERROR": 0,
    "cci_above_uniform": 937,
    "rotated": 509,
    "all_identities_checked": 1000
   },
   "64": {
    "n": 100,
    "UNIQUE": 100,
    "AMBIGUOUS": 0,
    "DEGENERATE": 0,
    "ERROR": 0,
    "cci_above_uniform": 95,
    "rotated": 45,
    "all_identities_checked": 100
   },
   "8": {
    "n": 15000,
    "UNIQUE": 15000,
    "AMBIGUOUS": 0,
    "DEGENERATE": 0,
    "ERROR": 0,
    "cci_above_uniform": 13923,
    "rotated": 7457,
    "all_identities_checked": 15000
   }
  }
 },
 "D128": {
  "d": 128,
  "nc": 3,
  "status": "UNIQUE",
  "n0": 1,
  "gap_rel": 1.9693767167851377e-05,
  "zero_mode_ok": true,
  "ss_res_rel": 4.327565414935823e-16,
  "cci": 0.13938651363060603,
  "status_code": "RAN"
 },
 "cpuref": {
  "read": 392,
  "compared": 392,
  "near_threshold_not_compared": 0,
  "not_comparable": false,
  "disagreements": 0,
  "first_disagreements": [],
  "max_diffs": {
   "cci": 7.188694084447889e-13,
   "purity": 3.335887122091208e-12,
   "folds_n_c1": 7.037037619284092e-12,
   "folds_n_c2": 5.083222731627757e-11,
   "gap_rel_rel": 1.5219895949835536e-11,
   "choi_min": 1.0547792504834934e-12
  },
  "informative_only": [
   "folds_n_c2"
  ],
  "meta_ok": true,
  "child_rc": 0,
  "ok": true,
  "cpu_seconds": 95.90234160423279
 },
 "engine": [
  "E1_amplitude_damping_spectrum_and_ground_state",
  "E2_pure_dephasing_detected_degenerate",
  "E3_root_law_rates_exact",
  "E4_blind_estimator_recovers_root_law",
  "E5_thermal_qubit_gibbs_and_spohn_monotone",
  "E6_time_reversal_not_cp_forward_cp_tp",
  "E7_estimator_floor_below_one_tenth_of_the_criterion",
  "E8_cpu_reference_comparator_selftest"
 ],
 "engine_ok": [
  true,
  true,
  true,
  true,
  true,
  true,
  true,
  true
 ],
 "phase_seconds": {
  "T3": 102.2,
  "T2": 1801.5,
  "T1": 2347.4,
  "T4": 2923.5,
  "D128": 649.8
 },
 "env": {
  "gpu": "NVIDIA GeForce RTX 5090",
  "torch": "2.11.0+cu128",
  "cuda": "12.8",
  "python": "3.14.3",
  "numpy": "2.4.3",
  "scipy": "1.18.0",
  "platform": "Windows-11-10.0.26200-SP0",
  "determinism": {
   "use_deterministic_algorithms": true,
   "CUBLAS_WORKSPACE_CONFIG": ":4096:8",
   "tf32": false,
   "threads": 4
  }
 },
 "reproducibility_v385": "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__REPRODUCED_BIT_FOR_BIT__393_FIELDS__SAME_V1_SAME_WORKER_SAME_BETA__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED",
 "reproducibility_n_fields_v385": 393,
 "reuse_v386_verdict": "TGL_QUANTUM_PILLAR_REUSE_V386__REUSED_FROM_THE_SEALED_V385_RUN_BY_KEY__RESULT_SHA256_MATCHES__VERDICT_SAME__CUSTODY_CHAIN_OK__KEY_SAME__THE_PILLAR_IS_NOT_THE_OBJECT_OF_THIS_VERSION__REPRODUCIBILITY_V385_NOT_REMEASURED_THIS_RUN_SAID__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED",
 "COMPUTED_NOT_MEASURED_no_veredito": true,
 "o_que_podia_falsificar": [
  "T2: atrator nao unico/degenerado em alguma das configuracoes da grade (ambiguous=0, degenerate=0 de 672)",
  "T1: o instrumento cego NAO recuperar a lei-raiz injetada (pass_sigma0 por d: {'16': 1.0, '32': 1.0, '64': 1.0, '8': 1.0})",
  "T3: controles que DEVIAM falhar e nao falhassem (N1 dephasing-only, N4 taxa negativa nao-CP, N5 inversao temporal nao-CP): todos True em d8..d64; N3: lei linear injetada -> lei-raiz rejeitada em 100%%",
  "identidades (CP, TP, PSD, Spohn, modo zero, residuo do estado estacionario) em 672/672 e em 21100/21100 instancias de estresse",
  "referencia independente na CPU: 392 comparacoes"
 ]
}
```

## Probabilidade conjunta já existente
```json
{
 "V1_v352": {
  "verdict": "TGL_JOINT_COINCIDENCE_V1__RESULT__JOINT_COINCIDENCE_NOT_EXCLUDED_AT_THRESHOLD__P_JOINT_0P546__MAX_Z_3P86__BOOLEAN_False__ADMISSIBLE_3_OF_35__NAIVE_PRODUCT_INVALID__GATE_UNTOUCHED",
  "p_joint_primary": 0.5458727599916506,
  "n_admissible": 3,
  "n_inventory": 35,
  "naive_product_INVALID": 5.546678239835239e-31,
  "boolean": false
 },
 "V2_v363": {
  "verdict": "TGL_JOINT_COINCIDENCE_V2__RESULT__JOINT_COINCIDENCE_V2_NOT_EXCLUDED_AT_THRESHOLD__INCONSISTENT__DETECTED_2__P_ALL_PRIMARY_6P6eM03__MAX_Z_3P86__BOOLEAN_False__GATE_UNTOUCHED",
  "P_all_primary": 0.00656830756492138,
  "P_all_range": [
   0.00017066307750370738,
   0.04655883271461885
  ],
  "max_abs_z": 3.863061069544643,
  "boolean": false
 },
 "V3_v370": {
  "verdict": "TGL_JOINT_COINCIDENCE_V3__RESULT__JOINT_COINCIDENCE_V3_NOT_EXCLUDED_AT_THRESHOLD__INCONSISTENT__DETECTED_2__P_ALL_PRIMARY_6P6eM03__MAX_Z_3P116__BOOLEAN_False__NOT_BLIND__GATE_UNTOUCHED",
  "P_all_primary": 0.00656830756492138,
  "P_all_range": [
   0.00017066307750370738,
   0.04655883271461885
  ],
  "max_abs_z": 3.1159706983791233,
  "dominant_channel": "d1_camb_v3_beta",
  "detected": [
   "neutrino_m2_global",
   "h0_escada_1pz_beta"
  ],
  "admissible": [
   "neutrino_m2_global",
   "h0_escada_1pz_beta",
   "d1_camb_v3_beta"
  ],
  "boolean": false,
  "channels_needed_for_1e-30": 28,
  "kernel_condition_met": true,
  "status_tag": "[DERIVED NAO-CEGO]",
  "n_inventory": 48,
  "rule_counts": {
   "A7_DEPENDENTE": 3,
   "None": 3,
   "A10_SUPERSEDIDO": 2,
   "A5_NAO_DISCRIMINANTE": 7,
   "A3_APOSENTADO": 7,
   "A9_SEM_INCERTEZA": 4,
   "A4_RECUSADO_PELO_GATE": 5,
   "A6_AGUARDANDO": 4,
   "A1_IDENTIDADE_POR_CONSTRUCAO": 6,
   "A8_NEGATIVO_DO_ARTEFATO": 3,
   "A2_LIDO_ANTES_DE_CRAVADO": 1,
   "A11_CONDICIONAL_A_PARTICAO": 2,
   "A12_COERENCIA_INTERNA_DECLARADA": 1
  }
 },
 "selo_joint_coincidence_boolean": false,
 "leitura": "o core NAO tem probabilidade conjunta dos TRES pilares: a coincidencia conjunta (V1-V3) pontua SO canais de natureza (class NATURE_CHANNEL); o kernel entra como CONDICAO (kernel_condition.met), nao como fator; o pilar da GPU nao entra. Nada aqui foi recomputado."
}
```

## Artigo selado v386
```json
{
 "pt_bytes": 816267,
 "en_bytes": 826050,
 "pt_GPU_mencoes": 12,
 "en_GPU_mencoes": 12,
 "pt_tres_pilares_ou_tres_testes_de_estresse": 1,
 "en_three_pillars_or_stress_tests": 0,
 "pt_probabilidade_conjunta_mencoes": 7,
 "pt_secao_v386": [
  "== Ao lado (v386): o Verbo seleciona; o ramo B reaberto por pré-registro =="
 ],
 "apresentacao_pt_linha2_trecho": "Apresentação do programa terminal da TGL que demonstra a conservação do núcleo mínimo de identidade como o elemento unificador dos domínios físicos na álgebra de operadores: recupera Einstein como limite assintótico, calcula a massa do Grande Atrator e a distância de Coma sem parâmetros ajustados aos alvos, resolve a tensão de Hubble por remissão expressa ao trabalho publicado (nota: Remissão expressa: a resolução da tensão de Hubble está endereçada no artigo unificado da TGL (estatuto do corpo: [CONJECTURE] de mecanismo; pós-dição declarada; zero parâmetro ajustado), publicado --- O custo geo",
 "pt_contextos_tres_pilares": [
  "ppa fica nas equações e sai da função objetivo. O teorema da Terminalidade recebe os seus três pilares externos, fixados pelo nome: Takesaki para a expectativa co"
 ],
 "leitura": "o artigo selado v386 NAO tem secao nem frase dos 'tres pilares / tres testes de estresse CONJUNTOS': PT 1 ocorrencia(s) de 'tres pilares' (contexto acima: nao e sobre os tres testes), EN 0; a apresentacao ja traz kernel + ritos + GPU numa so frase; a secao propria e alvo da v387"
}
```
