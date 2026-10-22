# README — a seção «Os três testes de estresse, conjuntos» (v387): o que o runtime precisa

Lente `redacao`, 05/10/2026. Entrega: `artigo_pt_v387_tres_testes.pysnip`, `artigo_en_v387_tres_testes.pysnip`, `APRESENTACAO_RESUMO_v387.md`
(frases curtas PT/EN como pares `old → new`) e este README. Os pysnip foram EXECUTADOS pelo arnês desta lente (`_arnes_exec.py`) contra o core
SELADO v386 (`um_absoluto.json` sha256 `0dbfb3fc1d319d1e…`, somente leitura), como corpo de `build_pt(core, verdict, data_path)` /
`build_en(...)`: PT 9 parágrafos, 22.398 B de LaTeX; EN 9 parágrafos, 24.023 B; **0 acertos da regex proibida** no texto emitido; **0 «n/d»/«n/a»
por número ausente** (os 22 «n/a» que restam em cada língua são a coluna «RG?»/«discrimina?» quando o canal não lê a RG); a guarda interna
(`[GUARDA]`/`[GUARD]`) não disparou na versão entregue. O LaTeX emitido está em `render_pt_v387.tex` / `render_en_v387.tex` para leitura.
**Nada do um.py foi rodado; nada fora desta lente foi tocado.**

Registro honesto do arnês: na primeira execução do EN a guarda interna DISPAROU — a frase da régua trazia «PROVED … CONFIRMED» em maiúsculas,
e o token `CONFIRMED` é exatamente o que a regex proíbe (no PT estava «CONFIRMADA», que não bate). Corrigido para `\emph{proved}`/`\emph{confirmed}`;
a guarda fez o que devia (seção não emitida, linha visível). Lição para o runtime: a mesma guarda deve correr sobre o texto GERADO, não só sobre os tokens.

## 1. Onde a seção entra

Proposta (decisão da gerência/operador — pergunta 2 abaixo): logo DEPOIS da `\subsection*{Nota: o que se calcula na GPU e como}` (PT, linha
~166136 na v386; EN, a «Note: what is computed on the GPU and how»), porque é ali que os três já estão apresentados («Uma rodada … faz três
coisas»); alternativa: como primeira seção «Ao lado (v387)», antes da «Ao lado (v386)». O pysnip já emite a sua `\addcontentsline` (sumário).
O pysnip usa `\bTGL` (macro já definida no preâmbulo do artigo), `longtable` (já carregado) e `\allowbreak` (núcleo do LaTeX).

## 2. O que a seção LÊ do core (tudo por caminho, com `_g3s`, nunca levanta; ausência imprime «n/d»/«n/a»)

Escopo disponível em `build_pt`: `core`, `verdict` (= raiz `verdict`), `data_path`. **O selo NÃO está no escopo** (por isso nada do selo é citado).

| bloco | caminhos lidos |
|---|---|
| `core.the_ledger_of_charges_v383` | `ledger[*].id/outcome/number_read/numbers_read`, `counts`, `echo_routes_outside_the_ledger.{n,excluded_by_data,inconclusive}` |
| `core.void_floor_v11 / void_density_v41` | `verdict`, `primary.{rhat_cal,sigma,L5,powered_beta_mu}`, `beta_floor`, `split_null.{ratio,sigma}` |
| `core.void_floor_v2 / void_floor_final / void_floor_kappa_v9 / void_shear_v2 / void_floor_lrg` | `verdict`, `rc_mle`, `rc_interval_5sigma[0,1]`, `systematics.chi2_dof_bmode`, `powered_5sigma`, `snr_profile`, `values.{detection_sigma_raw,fisher_floor}`, `primary.{rhat_cal,sigma}` |
| `core.clock_test_result_v369` | `verdict`, `P1.platforms[0].{Gamma_pred_per_s,Gamma_ub_per_s}`, `P2.{n_excluded,n_series}` (+ `ledger F3a.numbers_read.deficit_ordens_5sigma`) |
| `core.neutrino_m2 / neutrino_sum / neff_channel / nmc_shapiro` | `verdict`, `values.{m2_pred_meV,tensao_atual_sigma,kill_rule_satisfeita,sum_pred_eV,current_bound_eV,Delta_Neff,tensao_atual_best}`, `margin_s`, `nmc_dt_s`, `n_events` |
| `core.coma_reveal_state_v376` | `D_L_TGL_median_Mpc`, `reference_Mpc`, `reference_sigma_Mpc`, `z_TGL_both_sigmas`, `control_D_L_planck_median_Mpc`, `z_planck_control_ref_sigma_only`, `H0_local_D1a` |
| `verdict` (raiz) + `core.sensitivity` + `core.ga_mass_audit` | `masses_Msun.{A_literature,B_cf4_positions}`, `in_accepted_window.{A_literature,B_cf4_positions}`, `n_combinations`, `fraction_in_band`, `ga_mass_audit.verdict` |
| `core.dipole_antipode` | `antipode_underdense`, `density_ratio_antipode_over_GA`, `bootstrap.ci95[0,1]` |
| `core.bancada_fases_5_6_7_v380` | `fase5.validacao.{H0,sigma_H0,z_vs_alvo}`, `fase5.P_sombra.{delta,sigma_delta,z_delta}`, `fase5.lnB_sombra_vs_acumulada_S`, `fase7.T_z_ganho.{diagonal,moresco2020}`, `fase7.T_delta_moresco2020.{delta,sigma,z}`, `fase7.U_lnB_sombra_vs_acumulada.{diagonal,moresco2020}`, `fase6.todos_KMS.{z_det,z_excl_R1,z_excl_R2}`, `emenda_v5.todos_DEC.{z_excl_R1,z_excl_R2}` |
| `core.bancada_fase4_v378` | `veredito_fase4`, `P_ladder_d1b.{delta,sigma_delta,z_delta,pull,lnB.tgl_vs_lcdm}` |
| `core.d1_camb_v3_real_v366` | `delta_chi2`, `n_data`, `beta_posterior.{median,sigma}`, `z_alpha_sqrt_e` |
| `core.cosmological_errata_verdict` + `core.final_verdict_machine.channels.pantheon_canonical_1593` | `source_INPUT.{beta_hat,sigma,delta_BIC}`, `d_theory_sigma`, `d_zero_sigma`, `verdict`; `core.beta` (σ/β) |
| `core.final_verdict_machine` | `verdict`, `channels_emitted`, `channels_total`, `refuted_channels`, `exclusions_count`, `channels.l_A_compressed_cmb.{verdict,primary_beta,d_vs_theory_sigma}`, `channels.bbn.verdict`; `core.evidence_audit.values.bbn_decirc.{beta_hat,sigma}`, `values.fifth_entry_live`, `verdict` |
| `core.nivel2_rite` | `verdict`, `values.variantes.S.{mediana,sigma}` |
| `core.gw_echo_rite / gw_echo_kms_rite / echo_anchored_result_v2 / echo_pe_result_v2 / echo_search_result` | `verdict`, `stack.{a_over_sqrt_beta,sigma,power_sigma}`, `summary.{N_on,B_exp}` |
| `core.ringdown_dephasing_result_v2 / ringdown_scope_v376 / ramo_b_preregistration_v386` | `stacks["3.0"].{delta_tau,sigma}`, `z_vs_GR`, `power_B`, `delta_pred_A_v2`, `verdict`, `F2b_status`, `conjunto_D_n`, `pins.{poder_exato_A31,poder_exato_B10,poder_exato_C}.read`, `nothing_opened` |
| `core.dephasing_reach` | `verdict`, `deficit_orders_Th229`, `deficit_orders_Sr` |
| `core.kernel_formalization / external_ladder / qg_closure / the_axiom_v385 / the_verb_v386` | `verdict`, `axiom_report` (contado em runtime: declarações dentro do trio), `sorryAx_absent`, `custom_TGL_axioms_absent`, `lean_version` (regex `version X`), `n_theorems_clean`, `n_theorems_expected`, `formal_flags/physics_flags/experiment_flags` (contadas), `gate.verdict`, `gate.full_static_witness_exists`, `tag_for_omega_I`, `kernel_flags_ok/total` |
| `core.quantum_pillar_v384 / quantum_pillar_reuse_v386 / quantum_pillar_reproducibility_v385` | `verdict`, `mode`, `summary.T2.{points,unique,ambiguous,degenerate,identities_checked.CP}`, `summary.T1.{injections,errors,per_d[d].pass_sigma0}`, `summary.T3.{controls[d].N1/N4/N5,N3_linear_law[d].root_law_rejected}`, `summary.T4.{instances,unique,all_identities_checked}`, `summary.D128.status`, `summary.cpuref.{compared,disagreements}`, `summary.engine[*].ok`, `summary.phase_seconds`, `summary.env.{gpu,torch,cuda,determinism.use_deterministic_algorithms}`, `result_sha256_matches_v385_sealed`, `reproducibility.verdict` (segmento 1) |
| `core.joint_coincidence_result / _v3` | `primary.p_joint`, `n_admissible`, `n_inventory`, `naive_product_INVALID.value`, `primary.P_all`, `max_abs_z`, `dominant_channel`, `boolean_v3`, `channels_needed_for_threshold_at_primary_quality`, `kernel_condition.met`, `verdict` |
| `core.three_stress_tests_v387` (NOVO, opcional) | ver §3 |

## 3. O que FALTA no core para render sem contar sozinha: o registro `three_stress_tests_v387`

Hoje a seção **conta sozinha** (walk do core por chave `== "verdict"` que começa com `TGL_`, pela mesma regex) e DIZ que contou sozinha; o
veredito central sai como `TGL_THREE_STRESS_TESTS_V387__NOT_RECORDED_THIS_RUN__SECTION_COUNTED_ALONE__GATE_UNTOUCHED`. Para a v387 o runtime deve
computar, **pela MESMA guarda** (`_V386_GUARDA`-equivalente, idêntica à regex proibida), um registro `core["three_stress_tests_v387"]` — padrão W04
(try/except; falha vira `NOT_RECORDED__RUNTIME_ERROR`, `does_not_gate_core: True`; nunca derruba o rito) — com, no mínimo:

```
verdict                       TGL_THREE_STRESS_TESTS_V387__<contagens>__RITES_<nf>_NOT_FALSIFIED_<inc>_INCONCLUSIVE_<fal>_FALSIFIED_SUBSTRINGS_NAMED__LEDGER_<n>_CHARGES_<f>_FALSIFIED__KERNEL_<ncl>_OF_<nex>__GPU_<t2u>_OF_<t2p>_<t4u>_OF_<t4i>_CPU_<dis>_DISAGREEMENTS__P1_COUNTED_P2_NOT_DETERMINED__THREE_PILLARS_COUNT_TOGETHER__NOT_A_CONFIRMATION__GATE_UNTOUCHED
n_verdicts, n_not_falsified, n_inconclusive, n_awaiting      (walk por chave 'verdict' que começa com 'TGL_')
falsified_substring_paths                                      (lista de caminhos; esperada: d1_camb_result, bancada_fases_5_6_7_v380, the_ledger_of_charges_v383)
falsified_substring_readings                                   (dict caminho -> leitura: SUPERSEDED / PAIR_NOT_THEORY / REGEX_FALSE_POSITIVE)
n_forbidden_word_as_verdict                                    (esperado 0; a MESMA regex da guarda)
ledger: {n_charges, counts, F2b_status}                        (lido de the_ledger_of_charges_v383 + ramo_b_preregistration_v386)
echo_routes_outside_the_ledger: {n, excluded_by_data, inconclusive}
rows: [ {channel_key, verdict_key_path, state, rg_recovered: "sim"|"nao"|"n/a", discriminates: "sim"|"nao"|"sem poder"|"aguardando", synth: bool} ]
      -> a coluna «RG?» é hoje leitura da gerência por linha dentro do pysnip; movê-la para o registro (uma lista congelada de chaves de canal
         com a leitura por canal) tira a leitura do texto e a põe no core, auditável; a contagem «N de N» passa a ser lida do registro
kernel: {n_theorems_clean, n_theorems_expected, axiom_report_total, axiom_report_in_trio, sorryAx_absent, gate_flags_true, gate_flags_total, omega_I_tag}
gpu:    {T2_points, T2_unique, T1_injections, T1_errors, T1_pass_sigma0_all_d, T3_controls_failed_as_required, T3_root_law_rejected_all_d, T4_instances, T4_unique, D128_status, cpuref_compared, cpuref_disagreements, engine_ok, mode}
joint:  {V3_P_all, V3_boolean, V3_max_abs_z, kernel_condition_met, gpu_in_joint: False, three_pillar_probability_in_core: False}
verbatim: {file, sha256 (= 2e45f759767d663499752857955a6647bc1827c21e7170599ae4108dcfc6c5f7), segments_ok: bool}   (como _V386_OPERATOR_VERBATIM: os 5 segmentos V1..V5 + «em que pese iremos achar» conferidos por sha256/substring)
forbidden_words_in_transcribed_fields: 0
p1_statement / p2_statement                                     (texto fixo: P1 contada pelos três; P2 não determinada; nenhum número inventado)
does_not_gate_core: True
```

Quando o registro existir, o pysnip o lê (`_t3s`) nas contagens e no veredito central, e diz «fonte: o registro …»; se faltar, conta sozinho e
diz que contou. **Nenhuma probabilidade dos três pilares deve ser inventada**: se o operador quiser um número para P1, isso é um estimador
PRÉ-REGISTRADO (v388), com a regra de pontuação escrita antes de ler o core.

## 4. O que a seção NÃO alcança e por quê (fail-closed, dito)

- `fail_closed_selftest` está só no **selo** (não em `core`/raiz): não é citado. Se a gerência quiser, ecoar em `core.three_stress_tests_v387.kernel.fail_closed_selftest`.
- `ga_window_status` (`…NOT_NONCIRCULAR_EVIDENCE…`) está na **raiz** do JSON, não em `core` nem em `verdict`: a seção diz «não é evidência não-circular» como leitura da gerência; para citar o token, ecoar em `core.three_stress_tests_v387.rows`.
- A «correspondência recuperada em N de N» é **contagem das linhas da tabela marcadas «sim» pela gerência** (16 de 16 na v386; as linhas de
  síntese do livro e da máquina não contam duas vezes); os números dentro de cada linha são lidos do core. É uma leitura, dita como tal.
- O Coma: o token do core carrega `NOT_BLIND_UNADJUSTED_POSTDICTION`; a seção escreve «não-cega, sem ajuste (novidade de uso)» por força da errata
  da gerência de 05/10 (pós-dição não é demérito) — o token fica no core como registro; ver pergunta 1.
- Os literais que a seção tem: os nomes dos canais, as leituras «sim/não/n/a» por linha, `1,75″`/`0,87″` (eclipse de 1919) e `43″/século` (Mercúrio) — todos \textsf{[KNOWN]} de literatura, não números da teoria; e os verbatins do operador (strings embutidas, a conferir por sha256 como na v386).

## 5. Conferências a fazer no pacote (como na v386)

1. `conferir_citacoes_v387.py`: os 6 segmentos verbatim (V1..V5 + «em que pese iremos achar») são substrings EXATAS de `scratchpad\v386\TRES_TESTES_operador_05out.txt` (sha256 `2e45f759…`) — conferido nesta lente: 6/6 EXATO.
2. Ensaio a seco (`ensaio_a_seco_v387.py`): o `build_pt`/`build_en` com o pysnip gera LaTeX sem a regex proibida (esta lente: 0/0) e sem «n/d» por ausência (esta lente: 0/0).
3. A guarda interna do pysnip: se o texto gerado bater na regex, a seção NÃO sai e imprime a linha «[GUARDA] …» (comportamento conferido por leitura; não disparou).
4. Depois do patch das frases curtas: `grep -c` conforme `APRESENTACAO_RESUMO_v387.md` §Conferência.
