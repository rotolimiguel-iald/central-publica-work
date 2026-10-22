# -*- coding: utf-8 -*-
"""Monta RESULTADO_KERNEL.json e ACHADOS_FORA_DO_PREREGISTRO.json da RODADA 2 do construtor do kernel (F1.TEMPO).
Todo hash é LIDO dos arquivos por este script; os vereditos por subitem são dados explícitos abaixo, conferidos contra
os recibos de compilação e a auditoria do construtor (AuditR2.lean). Escreve SÓ em 3_KERNEL\\rodada_2.
Uso: python -I montar_resultado.py
"""
import datetime
import hashlib
import json
import os
import re

R2 = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\3_KERNEL\rodada_2"
K1 = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\3_KERNEL"
PRE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO"
P = lambda *a: os.path.join(R2, *a)


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def jl(p):
    with open(p, "rb") as f:
        return json.loads(f.read().decode("utf-8"))


def wjson(path, obj):
    with open(path + ".tmp", "wb") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(path + ".tmp", path)


agora = datetime.datetime.now(datetime.timezone.utc).isoformat()
pedra = P("sandbox", "TheTimeHasNoRank.lean")
olean = P("sandbox", "TheTimeHasNoRank.olean")
src = open(pedra, "rb").read().decode("utf-8")
rec_final = jl(P("logs", "T04_recibo.json"))
rec_repro = jl(P("logs", "REPRO_recibo.json"))
rec_audit = jl(P("logs", "AUDIT_FINAL_recibo.json"))
analise = jl(P("logs", "AUDIT_FINAL_analise.json"))
varred = jl(P("logs", "VARREDURA_FONTE_T04.json"))
vg1 = jl(P("logs", "V_GERAL_1_FINAL.json"))
beta = jl(P("BETA_RUNTIME_KERNEL.json"))
acom = jl(P("ACOM_RECIBO_PROJECAO.json"))
conf_a = jl(P("CONFERENCIA_FREEZE_E_RODADA1_ANTES.json"))
conf_d = jl(P("CONFERENCIA_FREEZE_E_RODADA1_DEPOIS.json"))
fp_a = jl(P("FINGERPRINT_KERNEL_ANTES.json"))
fp_l = jl(P("FINGERPRINT_KERNEL_DEPOIS_LEAN.json"))
fp_d = jl(P("FINGERPRINT_KERNEL_DEPOIS.json"))
limpeza = jl(P("LIMPEZA_RECIBO.json"))
rotas = jl(P("rotas_consultas", "RESUMO.json"))
inv = jl(P("rotas_consultas", "INVENTARIO_CONSULTAS.json"))
audit_txt = open(P("logs", "AUDIT_FINAL_saida.txt"), "rb").read().decode("utf-8")
m_aux = re.search(r"AUDIT_TOTAL\t(\d+)\tAUXILIARES\t(\d+)", audit_txt)
FREEZE_META = "b1b47447ac30f7c74ad33b200bd2a3025987650a13593038ddc7465de6fab21f"
FREEZE_SRC = "911cb40b9de1a8bb3bdd0789d5af3f718fa98ee9f0b1f5fcd6ffa4abb616bd3d"
PERMITIDAS = {"Mathlib", "TGLExt.LocalBreuerGap", "TGLExt.ModularFlow", "TGLExt.FiniteTomita", "TGLExt.Ergodicity",
              "TGLExt.PageInformation", "TGLExt.TheSingularExpectation", "TGLExt.TheTraceIsNotErasable",
              "TGLExt.TheAxiomAndTheFalseWitness", "TGLExt.TheVerbSelectsTheAction", "TGLExt.IALDJones",
              "TGLExt.TheLivingWord", "TGLExt.BisognanoWichmann", "TGLExt.Fundacao", "TGLExt.AbsoluteOne",
              "TGLExt.O16.PolarMinimalPeriod_v2", "TGLExt.O16.ProbeNonKMS_v3", "TGLExt.TheImportedSecondQuantization",
              "TGLExt.V350L2CharacterMultiplier"}
imports = re.findall(r"^import\s+(\S+)", src, re.M)
NS = "TGLExt.TheTimeHasNoRank."

# ---------------------------------------------------------------- correspondência pré-registro → rodada 2
correspondencia = [
    {"preregistrado": "time_is_the_modular_flow (T3.a)", "rodada_2": "modular_flow_is_a_kms_group",
     "mudanca": "RENOMEADO (achado M3(1): o nome afirmava a hipótese do tempo térmico, que a pedra não deve afirmar); enunciado idêntico"},
    {"preregistrado": "the_time_has_no_rank (T9.e, cláusula composta)", "rodada_2": "the_post_is_only_the_limit",
     "mudanca": "RENOMEADO (achado M3(2): lido por POSTO = RANK contradizia flow_full_rank); conjunção idêntica"},
    {"preregistrado": "optical_attractor_is_the_absolute_one (T11.a)", "rodada_2": "half_identity_is_absoluteRho_two",
     "mudanca": "RENOMEADO (achado M3(3): o enunciado não tem canal; o canal ótico é a face ótica e a F1.ATRATOR, não refeitos aqui); enunciado idêntico"},
    {"preregistrado": "purityR_modular (T6.d) com hd", "rodada_2": "purityR_modular sem hd",
     "mudanca": "MAIS FORTE: hipótese sem peso retirada (rodada 1: _hd; auditorias B3/M17)"},
    {"preregistrado": "clock_reads_modulo_period (T10.b) com κ ≠ 0", "rodada_2": "clock_reads_modulo_period (κ t : ℝ)",
     "mudanca": "MAIS FORTE: κ ≠ 0 sem peso na forma Lean (2π/0 = 0; auditoria B1/E5)"},
    {"preregistrado": "modular_clock_rotates_without_shrinking (T10.d) com hd", "rodada_2": "modular_clock_rotates_without_shrinking sem hd",
     "mudanca": "MAIS FORTE: achado DESTA rodada — hd não tem peso (vale para todo d real; logRho_rhoD_real_diagonal, modPow_rhoD_general)"},
    {"preregistrado": "(não pré-registrado; rodada 1) no_finite_instant_is_the_post com idempotência", "rodada_2": "no_finite_instant_is_the_post sem hP",
     "mudanca": "MAIS FORTE: idempotência sem peso (auditoria B)"},
    {"preregistrado": "(re-exportações, nomes livres) the_face_lands / face_has_a_limit / face_distinguishes_instants / face_clock_has_no_period",
     "rodada_2": "dephasing_lands_on_the_diagonal / damped_orbit_has_a_limit / decay_distinguishes_instants / decay_reading_has_no_period",
     "mudanca": "RENOMEADOS (achado M4; o próprio kernel marca a leitura decaimento = face hiperbólica como [ONTO], IALDJones.lean l.274–275); tipos originais"},
    {"preregistrado": "(rodada 1) the_absolute_one_has_no_clock, the_coherence_obeys_agape_explicit, probe_bounded_spectral_translation : True",
     "rodada_2": "removidos / com enunciado", "mudanca": "PESO MORTO (M17): re-export duplicado e duplicata removidos; a sonda L2 ganhou enunciado"},
    {"preregistrado": "(rodada 1) optical_attractor_clock_stops, probe_the_time_has_no_rank",
     "rodada_2": "half_identity_freezes_the_clock, probe_the_post_is_only_the_limit", "mudanca": "RENOMEADOS (acompanham M3)"},
    {"preregistrado": "todas as demais assinaturas de PREREGISTRO.json → lean_alvo", "rodada_2": "mesmos nomes",
     "mudanca": "nenhuma; cada assinatura pré-registrada foi conferida por `example` em AuditR2.lean (EXIT 0)"},
]

# ---------------------------------------------------------------- subitens (face kernel; ótico fora deste ensaio)
K = "kernel"
subitens = [
    ("T1.a", K, True, "PASSA", ["no_time_matrix", "no_time_matrix_fin"], "no_time_matrix_fin ligado por termo a TGLExt.no_finite_weyl_pair (R22)"),
    ("T1.b", K, False, "PASSA", ["commutator_far_from_scalar"], "opcional"),
    ("T1.c", K, True, "PASSA", ["no_finite_spectral_translation"], ""),
    ("T1.o", "otico", True, "FORA_DESTE_ENSAIO", [], "face ótica: 2_OPTICO"),
    ("T2.a", "citacao", True, "CITADA", [], "[KNOWN] Pauli 1933/1958 (páginas a conferir), Galapon 2002, Wintner 1947, Wielandt 1949; nunca recebe PASSA de teste"),
    ("T2.b", K, False, "PASSA", ["no_bounded_spectral_translation", "probe_bounded_spectral_translation", "probe_bounded_spectral_translation_complex"], "opcional; NÃO é o teorema de Pauli; a sonda V-T2-b em M₂(ℂ) (norma L2) agora tem enunciado"),
    ("T3.a", K, True, "PASSA", ["modular_flow_is_a_kms_group"], "nome pré-registrado time_is_the_modular_flow; enunciado idêntico; vale também para o fluxo congelado (sonda AUD-4)"),
    ("T3.b", K, True, "PASSA", ["fixed_sector_is_the_centralizer", "tracial_state_freezes_the_flow", "nontracial_state_rejects_the_identity_flow", "probe_identity_flow_not_kms_inhabited"], "re-exportações de tipo idêntico (V-GERAL-2); (iii) agora HABITADA pela testemunha concreta theSpecificAQFTWitness (V-GERAL-1 completa; ressalva da rodada 1 resolvida)"),
    ("T3.o", "otico", True, "FORA_DESTE_ENSAIO", [], ""),
    ("T4.a", K, True, "PASSA", ["unitary_keeps_spectrum_and_purity"], "a hipótese unitária só pesa na pureza (peso parcial, dito)"),
    ("T4.b", K, True, "PASSA", ["isometry_orbit_converges_only_if_fixed", "isometric_flow_converges_only_if_fixed", "unitary_conj_isometry", "modular_flow_is_isometry", "modular_orbit_converges_iff_diagonal", "modular_orbit_converges_iff_diagonal_entrywise"], "abstrato + instâncias obrigatórias (i) e (ii); instância opcional (iii) ver T4.b(iii)"),
    ("T4.b(iii)", K, False, "NAO_CONSTRUIDA", ["light_flow_group", "light_modular_orbit_converges_iff_post"], "o teorema CONDICIONAL compila (para todo FockCertificate), mas a sonda V-GERAL-1 é impossível no kernel atual: nenhum habitante de FockCertificate é exibido (TheImportedSecondQuantization.lean l.66); opcional, não afeta T4"),
    ("T4.c", K, True, "PASSA", ["schurDiag", "schurDiag_mulVec", "dephase_volume", "dephase_volume_lt_one", "modular_volume_one", "modular_factor_norm_one", "dephase_factor_norm_le_one", "schurDiag_is_the_dephasing", "schurDiag_is_the_modular_flow"], ""),
    ("T4.d", K, True, "PASSA", ["dephasing_lands_on_the_diagonal", "fixed_set_of_dephasing_is_the_diagonal"], "re-exportações de tipo idêntico; nomes neutros"),
    ("T4.e", K, True, "PASSA", ["volume_kept_yet_lands", "boost_pow_null"], "controle C-T4-a como registrado: volume conservado e pouso na direção estável"),
    ("T4.f", K, False, "PASSA", ["global_attractor_needs_volume_loss"], "opcional"),
    ("T4.o", "otico", True, "FORA_DESTE_ENSAIO", [], ""),
    ("T5.a", K, True, "PASSA", ["the_record_is_invariant", "fixed_set_of_dephasing_is_the_diagonal", "dephasing_lands_on_the_diagonal"], "re-exportações de tipo idêntico"),
    ("T5.b", K, True, "PASSA", ["dephase_fixed_states_not_unique"], "controle C-T5-a como registrado"),
    ("T5.c", "citacao", True, "CITADA", [], "F1.ATRATOR A4 (StrictComplementContraction), RESULTADO_F1_ATRATOR_R1.json 6d7dc60c…; não refeito"),
    ("T6.a", K, True, "PASSA", ["purityR_dephase"], ""),
    ("T6.b", K, True, "PASSA", ["purity_never_grows_under_dephasing"], "re-exportação de tipo idêntico"),
    ("T6.c", K, True, "PASSA", ["purityR_dephase_lt"], ""),
    ("T6.d", K, True, "PASSA", ["purity_of_hermitian", "purityR_modular", "purityR_sigma"], "purityR_modular mais forte (sem hd)"),
    ("T6.o", "otico", True, "FORA_DESTE_ENSAIO", [], ""),
    ("T7.a", K, True, "PASSA", ["dephase_inverse"], ""),
    ("T7.b", K, True, "PASSA", ["inverse_dephasing_not_positive", "quad_form_fin_two", "inverse_dephasing_quadratic_form"], ""),
    ("T7.o", "otico", True, "FORA_DESTE_ENSAIO", [], ""),
    ("T8.a", K, True, "PASSA", ["coherenceScaling", "coherence_entry_scaling"], ""),
    ("T8.b", K, True, "PASSA", ["the_coherence_obeys_agape"], "conjunção literal de Fundacao.agape conferida por type_of% em AuditR2"),
    ("T8.c", K, True, "PASSA", ["the_record_does_not_scale"], "controle C-T8-b como registrado"),
    ("T8.d", K, True, "PASSA", ["past_null_ray_contracts"], "re-exportação de tipo idêntico; citação de docstring corrigida (AF-01/M15: a leitura «a face geométrica da escala de Takesaki» é de boost_null_expand)"),
    ("T8.o", "otico", True, "FORA_DESTE_ENSAIO", [], ""),
    ("T8.t", "leitura", True, "LEITURA", [], "[ONTO]; nunca recebe PASSA de teste; a ponte tem conteúdo mínimo (scalar_decay_also_obeys_agape, fora do pré-registro)"),
    ("T9.a", K, True, "PASSA", ["flow_isIdempotentElem_iff", "flow_sq"], ""),
    ("T9.b", K, True, "PASSA", ["flow_isUnit"], ""),
    ("T9.c", K, True, "PASSA", ["post_not_isUnit"], "não depende de axioma algum"),
    ("T9.d", K, False, "PASSA", ["flow_full_rank", "post_rank_lt"], "opcional; posto PLENO em todo instante finito"),
    ("T9.e", K, True, "PASSA", ["the_post_is_only_the_limit"], "nome pré-registrado the_time_has_no_rank; conjunção idêntica (conferida por example)"),
    ("T9.o", "otico", True, "FORA_DESTE_ENSAIO", [], "na rodada 1 a face ótica registrou FALHA em T9.o(c) (tolerância 1e−13 abaixo do piso float64; achado A1); preservada"),
    ("T9.t", "leitura", True, "LEITURA", [], "[ONTO] da GERÊNCIA (achado A2: a frase «O tempo é o Verbo…» não é do operador); a pedra não a afirma"),
    ("T10.a", K, True, "PASSA", ["clock_faithful_iff_one_turn", "clock_reciprocal_temperature"], "re-exportações de tipo idêntico"),
    ("T10.b", K, True, "PASSA", ["clock_reads_modulo_period", "frozen_clock"], "clock_reads_modulo_period mais forte (sem κ ≠ 0)"),
    ("T10.c", K, True, "PASSA", ["angle_has_no_limit", "angle_is_periodic", "damped_orbit_has_a_limit", "decay_distinguishes_instants"], "re-exportações de tipo idêntico; nomes neutros; o ω ≠ 0 do termo do kernel angular_orbit_periodic não tem peso na forma Lean (sonda)"),
    ("T10.d", K, True, "PASSA", ["modular_clock_rotates_without_shrinking", "logRho_rhoD_commute_diagonal", "logRho_rhoD_real_diagonal", "modPow_rhoD_general", "phase_norm_one"], "MAIS FORTE (sem hd): achado desta rodada"),
    ("T10.e", K, True, "PASSA", ["the_post_is_not_moved", "the_state_is_not_moved", "the_vector_is_not_moved"], "re-exportações de tipo idêntico"),
    ("T10.o", "otico", True, "FORA_DESTE_ENSAIO", [], ""),
    ("T10.t", "leitura", True, "LEITURA", [], "[ONTO]; o verbo do operador é «registra»"),
    ("T11.a", K, True, "PASSA", ["half_identity_is_absoluteRho_two", "tracial_state_freezes_the_flow", "half_identity_freezes_the_clock"], "nome pré-registrado optical_attractor_is_the_absolute_one; enunciado idêntico; a ligação com o canal ótico é a face ótica e a F1.ATRATOR"),
    ("T11.o", "otico", True, "FORA_DESTE_ENSAIO", [], ""),
]
subitens_json = [{"id": s[0], "face": s[1], "obrigatorio": s[2], "resultado": s[3],
                  "declaracoes": [NS + d for d in s[4]], "nota": s[5]} for s in subitens]
# confere que toda declaração citada existe na pedra (no espaço medido pela auditoria)
consts = set(re.findall(r"^AUDIT_DECL\t(\S+)\t", audit_txt, re.M))
faltam = [d for s in subitens_json for d in s["declaracoes"] if d not in consts]
if faltam:
    raise SystemExit("FALHA VISÍVEL: declarações citadas que não existem: %s" % faltam)

# ---------------------------------------------------------------- controles
controles = [
    ("C-T1-a", "kernel", "commutator_can_be_nonzero", "a afirmação falsa «nenhum comutador é não nulo» cai", "COMO_REGISTRADO"),
    ("C-T1-b", "kernel", "empty_dimension_admits_time", "em Fin 0 a igualdade vale: Nonempty é necessária", "COMO_REGISTRADO"),
    ("C-T1-c", "kernel", "weyl_pair_lives_in_L2", "re-citação de characterMultiplier_weyl (tipo idêntico): o par de Weyl existe em L²", "COMO_REGISTRADO"),
    ("C-T3-a", "otico", None, "", "FORA_DESTE_ENSAIO"),
    ("C-T3-b", "otico+kernel", "probe_identity_flow_not_kms_inhabited", "metade de kernel: o fluxo identidade NÃO é KMS para a testemunha concreta theSpecificAQFTWitness (agora habitada) e, na face finita, finite_face_identity_flow_not_kms (ρ = diag(2/3,1/3), a = E₀₁, b = E₁₀); metade ótica fora deste ensaio", "COMO_REGISTRADO (metade de kernel)"),
    ("C-T3-c", "otico", None, "", "FORA_DESTE_ENSAIO"),
    ("C-T4-a", "kernel+otico", "volume_kept_yet_lands", "det B(s) = 1 e B(s)ᵏ(1,−1) → 0: volume conservado NÃO impede pousar (metade ótica fora)", "COMO_REGISTRADO (metade de kernel)"),
    ("C-T4-b", "kernel", "dephasing_lands_without_being_fixed", "a defasagem (não isométrica) tem órbita convergente de ponto não fixo", "COMO_REGISTRADO"),
    ("C-T5-a", "kernel", "dephase_fixed_states_not_unique", "dois estados fixos distintos: a afirmação de que o conjunto fixo é um ponto cai", "COMO_REGISTRADO"),
    ("C-T6-a", "kernel+otico", "no_coherence_no_loss", "sem coerência a pureza não cai (metade ótica fora)", "COMO_REGISTRADO (metade de kernel)"),
    ("C-T6-b", "otico", "unitary_keeps_purity", "re-citação no kernel (purity_unitary_invariant); o controle é ótico", "FORA_DESTE_ENSAIO (re-citação de kernel presente)"),
    ("C-T6-c", "kernel+otico", "purity_grows_backwards", "para t < 0 a pureza cresce: (1 + e²)/2 > 1 (metade ótica fora)", "COMO_REGISTRADO (metade de kernel)"),
    ("C-T7-a", "kernel", "control_inverse_at_time_zero", "em t = 0 o inverso é a identidade e a positividade não cai (example)", "COMO_REGISTRADO"),
    ("C-T7-b", "kernel+otico", "control_inverse_on_diagonal", "T₋ₜ fixa a diagonal; diag(p,1−p) segue positiva (example) (metade ótica fora)", "COMO_REGISTRADO (metade de kernel)"),
    ("C-T7-c", "kernel+otico", "unitary_inverse_is_a_channel", "Ad(U*) inverte Ad(U) e preserva positividade (metade ótica fora)", "COMO_REGISTRADO (metade de kernel)"),
    ("C-T8-a", "kernel", "wrong_rate_breaks_scaling", "θ_s = T_{2s}: a lei de escala cai", "COMO_REGISTRADO"),
    ("C-T8-b", "kernel", "the_record_does_not_scale", "o registro não obedece à lei de escala", "COMO_REGISTRADO"),
    ("C-T9-a", "kernel", "flow_of_one_is_idempotent", "com P = 1 o fluxo é idempotente para todo t: 1 − P ≠ 0 é necessária", "COMO_REGISTRADO"),
    ("C-T9-b", "kernel", "flow_at_zero_is_idempotent", "F(0) = 1 é idempotente (borda)", "COMO_REGISTRADO"),
    ("C-T10-a", "kernel", "frozen_clock_not_faithful", "κ = 0: o relógio parado não é fiel para P ≠ 0", "COMO_REGISTRADO"),
    ("C-T10-b", "kernel", "decay_reading_has_no_period", "a leitura do decaimento não tem período (nome neutro; rodada 1: face_clock_has_no_period)", "COMO_REGISTRADO"),
    ("C-T11-a", "otico", None, "", "FORA_DESTE_ENSAIO"),
]
controles_json = [{"id": c[0], "face": c[1], "declaracao": (NS + c[2]) if c[2] else None, "comportamento": c[3],
                   "resultado": c[4]} for c in controles]

sondas = [
    ("V-T1-a", "examples com n = 1 (no_time_matrix_fin 1; no_time_matrix em Fin 1, c = 1)", "COMPILA"),
    ("V-T1-b", "probe_commutator_far_from_scalar: purityR(−i·1) = 2 em Fin 2", "COMPILA"),
    ("V-T2-b", "probe_bounded_spectral_translation (M₂(ℂ), norma L2, V = 1, H = 0, s = 1; COM enunciado) e probe_bounded_spectral_translation_complex (A = ℂ)", "COMPILA"),
    ("V-T3-a", "probe_rho_two_thirds_posDef, probe_rho_two_thirds_not_tracial e example da lei de grupo com ρ = diag(2/3,1/3)", "COMPILA"),
    ("V-T4-a", "probe_rotation_orbit_has_no_limit (rotação por 1 rad; a órbita de 1 não converge)", "COMPILA"),
    ("V-T4-b", "probe_gRate_one_sum e examples: det = e^{−2} < 1", "COMPILA"),
    ("V-T5-a", "example de dephase_fixed_states_not_unique em Fin 2, i₀ = 0, j₀ = 1", "COMPILA"),
    ("V-T6-a", "example de purityR_dephase_lt com ψ₊; probe_psiPlus_dephased_purity = (1 + e^{−2})/2", "COMPILA"),
    ("V-T7-a", "example com γ = 1, t = 1", "COMPILA"),
    ("V-T8-a", "examples: projeções de the_coherence_obeys_agape com ψ₊ (sem a duplicata _explicit)", "COMPILA"),
    ("V-T9-a", "postDiag = diag(1,0): idempotente, 1 − P ≠ 0, P ≠ 1; examples de T9.a–d; probe_the_post_is_only_the_limit em M₂(ℂ) (L2)", "COMPILA"),
    ("V-T10-a", "examples com κ = 1 e d = (2/3, 1/3)", "COMPILA"),
    ("V-T11-a", "half_identity_is_absoluteRho_two por cálculo direto", "COMPILA"),
    ("V-GERAL-1", "toda hipótese de teorema da pedra habitada: 56 teoremas com hipóteses, todos instanciados (V_GERAL_1_FINAL.json); T3.b(iii) agora habitada (probe_identity_flow_not_kms_inhabited); sondas de satisfazibilidade conjunta para T4.b abstrato; SEM habitante só light_flow_group e light_modular_orbit_converges_iff_post (FockCertificate, opcional T4.b(iii))", "COMPLETA, salvo T4.b(iii) opcional (dito)"),
    ("V-GERAL-2", "cada re-exportação provada nos dois sentidos por type_of% (na pedra) e de novo na auditoria AuditR2", "COMPILA"),
]
sondas_json = [{"id": s[0], "o_que": s[1], "resultado": s[2]} for s in sondas]

contraexemplos = [
    {"se_e_so_se": "T9.a flow_isIdempotentElem_iff", "contraexemplos": ["flow_at_one_is_not_idempotent (t = 1: lado esquerdo falha)", "example t = 0 (borda: vale)", "flow_of_one_is_idempotent (sem 1 − P ≠ 0 o iff cai)"]},
    {"se_e_so_se": "T4.b(ii) modular_orbit_converges_iff_diagonal (e _entrywise) / T3.b(i) fixed_sector_is_the_centralizer", "contraexemplos": ["probe_modular_orbit_of_psiPlus_has_no_limit (os dois lados falham para ψ₊)", "example postDiag (os dois lados valem)", "modular_iff_needs_injective_weights e centralizer_iff_needs_injective_weights (pesos iguais: o iff cai sem injetividade)"]},
    {"se_e_so_se": "T4.d/T5.a fixed_set_of_dephasing_is_the_diagonal", "contraexemplos": ["dephasing_iff_needs_positive_rates (taxa nula: ψ₊ fixo e não diagonal)"]},
    {"se_e_so_se": "T10.a clock_faithful_iff_one_turn", "contraexemplos": ["frozen_clock_not_faithful (sem κ ≠ 0 o iff cai)"]},
    {"se_e_so_se": "C-T3-b, face finita: identity_flow_kms_pair_iff", "contraexemplos": ["finite_face_identity_flow_not_kms (diag(2/3,1/3): falha)", "example com pesos iguais (vale)"]},
    {"se_e_so_se": "T4.b(iii) light_modular_orbit_converges_iff_post (opcional, condicional)", "contraexemplos": ["NÃO construído: exigiria um FockCertificate concreto, que o kernel não exibe (dito)"]},
]

hyp = analise["hipoteses"]
nome_sem_peso = {
    "criterio_termo": "a prova não usa a hipótese: medido no TERMO de cada teorema por AuditR2.lean (forallTelescope + instantiateLambda + containsFVar)",
    "resultado_termo": "nenhum: %d teoremas, %d com hipóteses, %d hipóteses medidas, todas usadas" % (hyp["n_teoremas"], hyp["n_teoremas_com_hipoteses"], hyp["n_hipoteses_medidas"]),
    "nao_usadas_no_termo": hyp["nao_usadas"],
    "criterio_semantico": "a hipótese é usada pela rota de prova mas a conclusão vale sem ela (o critério das auditorias da rodada 1, família B)",
    "removidas_por_peso_nulo": [
        {"declaracao": NS + "purityR_modular", "hipotese": "hd : ∀ i, 0 < d i", "origem": "rodada 1 (_hd; auditorias)"},
        {"declaracao": NS + "clock_reads_modulo_period", "hipotese": "κ ≠ 0", "origem": "auditoria de reprodução da rodada 1 (B1; x/0 = 0 no Lean)"},
        {"declaracao": NS + "no_finite_instant_is_the_post", "hipotese": "IsIdempotentElem P", "origem": "auditoria de reprodução da rodada 1 (B)"},
        {"declaracao": NS + "modular_clock_rotates_without_shrinking", "hipotese": "hd : ∀ i, 0 < d i", "origem": "ACHADO DESTA RODADA: a conclusão vale para todo d real (sonda d = (1, 0)); a rota do kernel por exp∘log é que a usava"},
    ],
    "observado_sem_remover": [
        {"declaracao": NS + "angle_is_periodic", "hipotese": "ω ≠ 0", "porque_fica": "re-exportação de TGLExt.IALDJones.angular_orbit_periodic: o tipo do kernel tem de ficar (V-GERAL-2); em ω = 0 a igualdade é trivial (2π/0 = 0; sonda example na pedra)"},
    ],
    "peso_parcial": [
        {"declaracao": NS + "modular_flow_is_a_kms_group", "hipotese": "hρ : ρ.PosDef", "nota": "só a cláusula KMS a usa (Delta usa ρ⁻¹); as outras sete valem para todo ρ"},
        {"declaracao": NS + "unitary_keeps_spectrum_and_purity", "hipotese": "hU", "nota": "só a pureza a usa; o polinômio característico vale para toda unidade"},
    ],
    "nome_e_termo": "nomes que diziam mais que o termo foram trocados (correspondência acima); o nome da pedra, TheTimeHasNoRank, segue provisório e é do operador: lido por POSTO = RANK diz o contrário de flow_full_rank",
}

por_afirmacao = [
    {"id": "T1", "declaracao": NS + "no_time_matrix", "resultado": "face kernel PASSA (T1.a, T1.c obrigatórios provados; T1.b opcional PASSA; C-T1-a, C-T1-b, C-T1-c como registrado; sondas V-T1-a/b compilam). O veredito da afirmação depende também da face ótica (T1.o), fora deste ensaio."},
    {"id": "T2", "declaracao": NS + "no_bounded_spectral_translation", "resultado": "CITADA (T2.a, [KNOWN]: Pauli em dimensão infinita não está no kernel); T2.b opcional PASSA na face limitada (álgebra de Banach), com a sonda V-T2-b agora com enunciado. Nunca T2 PASSA."},
    {"id": "T3", "declaracao": NS + "modular_flow_is_a_kms_group", "resultado": "face kernel PASSA (T3.a; T3.b (i)–(iii) re-exportações de tipo idêntico, e (iii) agora HABITADA por theSpecificAQFTWitness, sem a ressalva da rodada 1; metade de kernel do C-T3-b como registrado, também na face finita). Nome neutro no lugar de time_is_the_modular_flow. Depende também da face ótica (T3.o, C-T3-a/b/c)."},
    {"id": "T4", "declaracao": NS + "isometry_orbit_converges_only_if_fixed", "resultado": "face kernel PASSA (T4.a–e obrigatórios; T4.f opcional PASSA; T4.b(iii) opcional NÃO_CONSTRUÍDA como subitem com sonda — o teorema condicional compila, mas o kernel não exibe FockCertificate; C-T4-a e C-T4-b como registrado). Depende também da face ótica (T4.o)."},
    {"id": "T5", "declaracao": NS + "dephase_fixed_states_not_unique", "resultado": "face kernel PASSA (T5.a re-exportações; T5.b; C-T5-a como registrado); T5.c CITADA (F1.ATRATOR A4). Sem subitem ótico obrigatório: pela regra, PASSA."},
    {"id": "T6", "declaracao": NS + "purityR_dephase_lt", "resultado": "face kernel PASSA (T6.a–d; purityR_modular mais forte, sem hd; C-T6-a e C-T6-c como registrado na metade de kernel). Depende também da face ótica (T6.o, C-T6-b)."},
    {"id": "T7", "declaracao": NS + "inverse_dephasing_not_positive", "resultado": "face kernel PASSA (T7.a, T7.b; C-T7-a, C-T7-b, C-T7-c como registrado na metade de kernel). Depende também da face ótica (T7.o)."},
    {"id": "T8", "declaracao": NS + "the_coherence_obeys_agape", "resultado": "face kernel PASSA (T8.a–d; citação da docstring de T8.d corrigida; C-T8-a, C-T8-b como registrado); T8.t LEITURA. A ponte é só a lei e^{−s} (scalar_decay_also_obeys_agape, fora do pré-registro). Depende também da face ótica (T8.o)."},
    {"id": "T9", "declaracao": NS + "the_post_is_only_the_limit", "resultado": "face kernel PASSA (T9.a, T9.b, T9.c, T9.e; T9.d opcional PASSA; C-T9-a, C-T9-b como registrado); T9.t LEITURA da gerência (achado A2). Pela regra congelada a afirmação depende da face ótica, que na rodada 1 registrou FALHA em T9.o(c) (piso numérico; achado A1), preservada e fora deste ensaio. Nome neutro no lugar de the_time_has_no_rank."},
    {"id": "T10", "declaracao": NS + "clock_reads_modulo_period", "resultado": "face kernel PASSA (T10.a–e; clock_reads_modulo_period sem κ ≠ 0 e modular_clock_rotates_without_shrinking sem hd, ambos mais fortes; C-T10-a, C-T10-b como registrado); T10.t LEITURA. Depende também da face ótica (T10.o)."},
    {"id": "T11", "declaracao": NS + "half_identity_is_absoluteRho_two", "resultado": "face kernel PASSA (T11.a: ½·1 = absoluteRho (Fin 2) e o fluxo modular trivial nele; nome neutro no lugar de optical_attractor_is_the_absolute_one). ½·1 tem posto 2 e pureza ½ (fora do pré-registro). Depende também da face ótica (T11.o, C-T11-a); só face finita."},
]

tentativas = []
for f in sorted(os.listdir(P("tentativas"))):
    tentativas.append({"arquivo": "tentativas/" + f, "sha256": sha(P("tentativas", f)), "bytes": os.path.getsize(P("tentativas", f))})
compilacoes = []
for f in sorted(os.listdir(P("logs"))):
    if f.endswith("_recibo.json"):
        r = jl(P("logs", f))
        compilacoes.append({"recibo": "logs/" + f, "fonte_sha256": r["source_sha256"], "exit": r["exit_code"],
                            "erros": r["n_error"], "avisos": r["n_warning"], "sorryAx": r["n_sorryAx_na_saida"],
                            "fora_do_trio": [a["decl"] for a in r["fora_do_trio"]], "segundos": r["seconds"],
                            "olean_sha256": r.get("olean_sha256")})

resultado = {
    "documento": "RESULTADO DO KERNEL — F1.TEMPO, RODADA 2 do construtor do kernel (pedra candidata corrigida)",
    "unidade": "F1.TEMPO",
    "papel": "construtor do kernel (subagente do workflow posto-e-tempo da gerência c1), reinvocado na retomada do workflow",
    "data": "2026-10-12",
    "gerado_em_utc": agora,
    "estatuto": "[REAL] para o que o kernel provou no sandbox (Lean 4.31.0, LEAN_PATH só-leitura no .lake do Nós); um PASSA é validade matemática na face kernel testada, não creditação; nada aqui move o gate; a face ótica está fora deste ensaio; sem veredito global.",
    "por_que_rodada_2": ("A rodada 1 do kernel (3_KERNEL, 51 arquivos, RESULTADO_KERNEL.json 5a56eab2…, pedra 7105eda4…) terminou e está preservada byte a byte "
                         "(50/50 arquivos do MANIFESTO_3_KERNEL conferem antes e depois). O relatório final da rodada 1 (4_RELATORIO\\RELATORIO_FINAL.md, gravado antes de o agente falhar) "
                         "registra que aquela pedra não entra no um.py como está: atribuía ao operador frases que ele não escreveu (M2), três nomes diziam mais que o termo (M3), o cabeçalho "
                         "estendia a regra dos dois regimes (M4), V-GERAL-1 ficou incompleta (M5), uma citação de docstring estava trocada (M15) e havia peso morto (M17); o item E5 pede "
                         "pedra corrigida, nova compilação e nova auditoria. A regra congelada manda que um reensaio grave ao lado sem sobrescrever. Esta rodada 2 testa EXATAMENTE o pré-registro "
                         "(mesmos enunciados, tolerâncias, mapeamento e esperado) com a pedra corrigida, em 3_KERNEL\\rodada_2; os nomes foram ajustados como a convenção do pré-registro permite "
                         "(«nomes … podem ajustar-se sem enfraquecer hipóteses nem conclusões; o auditor confere no #check»), e cada assinatura pré-registrada foi conferida por example."),
    "freeze": {"FREEZE.json": conf_a["freeze"], "arquivos_conferidos_antes": "%d de %d" % (conf_a["freeze_conferem"], conf_a["freeze_total"]),
               "arquivos_conferidos_depois": "%d de %d" % (conf_d["freeze_conferem"], conf_d["freeze_total"]),
               "todos_conferem": conf_a["freeze_ok"] and conf_d["freeze_ok"],
               "conferencias": ["CONFERENCIA_FREEZE_E_RODADA1_ANTES.json", "CONFERENCIA_FREEZE_E_RODADA1_DEPOIS.json"]},
    "texto_do_operador": conf_d["texto_do_operador"],
    "rodada_1_preservada": {"antes": conf_a["rodada_1_kernel"], "depois": conf_d["rodada_1_kernel"]},
    "beta_runtime": beta,
    "acom": {"modo": "projeção SÓ DE LEITURA da referência da gerência; nenhum init e nenhuma transition (a tarefa proíbe escrever na memória; a transição de q/p é ato da gerência)",
             "recibo": "ACOM_RECIBO_PROJECAO.json", "revision": (acom.get("receipt") or {}).get("revision"),
             "event_id": (acom.get("receipt") or {}).get("event_id"), "db_inalterado_pela_projecao": acom.get("db_inalterado_pela_projecao")},
    "cetico_aferidor": {"mapa_de_rotas": {"livro_inalterado": rotas["livro_inalterado"], "consultas": [{"tema": c["tema"], "sha256": c["sha256"]} for c in rotas["consultas"]],
                                           "nota": "só consultar; 10 temas; FockCertificate: 2 rotas, nenhuma sobre habitante; os demais: 0 rotas"},
                        "inventario_da_bancada": {"sha256": inv["sha256"], "termos": {t: v["n"] for t, v in inv["termos"].items()}},
                        "kernel": "theSpecificAQFTWitness (WedgeNet.lean:357) e omega_not_tracial (SignatureInTheLimit.lean:201) estão no fecho transitivo das importações permitidas (sem linha nova de import); FockCertificate: o kernel diz «nenhum habitante de `FockCertificate` … é exibido» (TheImportedSecondQuantization.lean l.66)"},
    "pedra": {"nome_provisorio": "TheTimeHasNoRank", "namespace": "TGLExt.TheTimeHasNoRank",
              "nota_nome": "nome provisório; o operador pode renomear (lido por POSTO = RANK diz o contrário de flow_full_rank: decisão dele)",
              "arquivo": pedra, "sha256": sha(pedra), "bytes": os.path.getsize(pedra),
              "importacoes": imports, "importacoes_todas_permitidas": all(i in PERMITIDAS for i in imports),
              "olean": olean, "olean_sha256": sha(olean), "olean_bytes": os.path.getsize(olean),
              "olean_reprodutivel": rec_final.get("olean_sha256") == rec_repro.get("olean_sha256") == sha(olean),
              "olean_repro": "sandbox/repro/TheTimeHasNoRank.olean", "nao_instalada": "a pedra vive só no sandbox da F1.TEMPO (rodada 2); instalação e nome são da cadeia de selo / do operador",
              "rodada_1": {"arquivo": os.path.join(K1, "sandbox", "TheTimeHasNoRank.lean"), "sha256": sha(os.path.join(K1, "sandbox", "TheTimeHasNoRank.lean")), "preservada": True}},
    "compilacao_final": {"comando": rec_final["command"], "LEAN_PATH_somente_leitura": rec_final["LEAN_PATH"], "lean_version": rec_final["lean_version"],
                         "exit": rec_final["exit_code"], "segundos": rec_final["seconds"], "n_print_axioms": rec_final["n_axiom_lines"],
                         "fora_do_trio": rec_final["fora_do_trio"], "n_sorryAx_na_saida": rec_final["n_sorryAx_na_saida"],
                         "n_erros": rec_final["n_error"], "n_avisos": rec_final["n_warning"], "avisos": [],
                         "saida": "logs/T04_saida.txt", "saida_sha256": rec_final["output_sha256"], "recibo": "logs/T04_recibo.json",
                         "recibo_sha256": sha(P("logs", "T04_recibo.json")),
                         "reproducao": {"recibo": "logs/REPRO_recibo.json", "exit": rec_repro["exit_code"], "olean_sha256": rec_repro.get("olean_sha256"),
                                        "saida_identica": rec_repro["output_sha256"] == rec_final["output_sha256"]}},
    "varredura_estatica_da_fonte": {k: varred[k] for k in ("sha256", "n_declaracoes", "n_print_axioms", "declaracoes_sem_print", "prints_sem_declaracao",
                                                           "declaracoes_duplicadas", "tokens_proibidos_no_codigo", "constante", "regua", "n_citacoes",
                                                           "n_citacoes_nao_achadas", "operador_12out_ocorrencias_de_verbo", "varredura_ok")}
                                   | {"relatorio": "logs/VARREDURA_FONTE_T04.json", "citacoes": varred["citacoes"]},
    "auditoria_do_construtor": {"arquivo": P("sandbox", "AuditR2.lean"), "sha256": sha(P("sandbox", "AuditR2.lean")), "exit": rec_audit["exit_code"],
                                "erros": rec_audit["n_error"], "avisos": rec_audit["n_warning"], "importa": "o .olean compilado da pedra (TEMPO_IMPORTA_SANDBOX=1)",
                                "constantes_no_namespace": int(m_aux.group(1)), "auxiliares_geradas_pelo_lean": int(m_aux.group(2)),
                                "constantes_alem_das_declaradas": analise["constantes_alem_das_declaradas"],
                                "todas_no_trio": not analise["fora_do_trio"], "perfil_de_axiomas": analise["perfil_de_axiomas_contagem"],
                                "sem_axioma_algum": analise["perfil_de_axiomas"].get("(nenhum)", []),
                                "assinaturas_preregistradas_conferidas_por_example": True,
                                "saida": "logs/AUDIT_FINAL_saida.txt", "saida_sha256": rec_audit["output_sha256"], "analise": "logs/AUDIT_FINAL_analise.json"},
    "axiomas_por_declaracao": rec_final["axiom_records"],
    "criterios_da_pedra": {"exit_0": rec_final["exit_code"] == 0,
                           "print_axioms_de_toda_declaracao_no_trio": (not rec_final["fora_do_trio"]) and rec_final["n_axiom_lines"] == varred["n_declaracoes"],
                           "zero_sorry_admit_axiom_native_decide": all(v == 0 for v in varred["tokens_proibidos_no_codigo"].values()) and rec_final["n_sorryAx_na_saida"] == 0,
                           "beta_nao_entra_no_lean": varred["constante"]["caractere_beta"] == 0 and all(v == 0 for v in varred["constante"]["literais_de_conferencia"].values()),
                           "impressao_digital_igual": fp_a["meta_sha256"] == fp_l["meta_sha256"] == fp_d["meta_sha256"] and fp_a["src_sha256"] == fp_l["src_sha256"] == fp_d["src_sha256"],
                           "toolchain_copiado_apagado": (not limpeza["toolchain_existe_depois"]) and not limpeza["sobras_de_lake_ou_cache"],
                           "fonte_saida_recibo_por_sha256": True},
    "kernel_impressao_digital": {"antes": fp_a, "depois_do_lean": fp_l, "depois_da_limpeza": fp_d,
                                 "iguais": fp_a["meta_sha256"] == fp_l["meta_sha256"] == fp_d["meta_sha256"] and fp_a["src_sha256"] == fp_l["src_sha256"] == fp_d["src_sha256"],
                                 "igual_ao_FREEZE": fp_d["meta_sha256"] == FREEZE_META and fp_d["src_sha256"] == FREEZE_SRC},
    "limpeza": limpeza,
    "correspondencia_preregistro_rodada_2": correspondencia,
    "subitens": subitens_json,
    "controles": controles_json,
    "sondas": sondas_json,
    "hipoteses_habitadas": {"relatorio": "logs/V_GERAL_1_FINAL.json", "teoremas_com_hipoteses": len(vg1["teoremas"]), "sem_uso_algum": vg1["sem_uso_algum"],
                            "so_usados_em_provas": vg1["so_usado_em_provas"],
                            "leitura": "os três só usados dentro de outras provas são instanciados com argumentos concretos: coherence_entry_scaling em wrong_rate_breaks_scaling; no_bounded_spectral_translation nas duas sondas de T2.b; flow_isUnit via flow_full_rank (example com postDiag) e probe_the_post_is_only_the_limit",
                            "nao_habitadas": [NS + "light_flow_group", NS + "light_modular_orbit_converges_iff_post"],
                            "por_que": "exigem um FockCertificate; o kernel não exibe habitante (TheImportedSecondQuantization.lean l.66); T4.b(iii) é opcional"},
    "contraexemplos_dos_se_e_so_se": contraexemplos,
    "nome_sem_peso": nome_sem_peso,
    "por_afirmacao": por_afirmacao,
    "ciclo_limite_S46_3": "ABERTA [OPEN]: nada aqui o trata",
    "clausulas_compostas": [
        {"nome": NS + "the_post_is_only_the_limit", "conteudo": "T1.a (Fin n) ∧ T9.a ∧ T9.b ∧ T9.c ∧ F(t) → P", "so_conjuncao": True, "nome_preregistrado": "the_time_has_no_rank"},
        {"nome": NS + "the_two_regimes_of_time", "conteudo": "T4.b (discreto e contínuo) ∧ T4.c (c1, c1 < 1, c2) ∧ T6.c ∧ T7.b ∧ T10.b (forma mais forte, sem κ ≠ 0) ∧ frozen_clock", "so_conjuncao": True,
         "nota": "nome do pré-registro; dois regimes DINÂMICOS (isométrico × dissipativo); a identificação com FACE/ÂNGULO da casa segue [OPEN]"},
    ],
    "nao_afirma": [
        "que o tempo é santo, que a dissipação é amor, ou qualquer frase [ONTO] como teorema: só em comentário, marcadas, com citação conferida nos bytes",
        "o teorema de Pauli em dimensão infinita (T2.a CITADA); nem que Pauli proíba o fluxo modular",
        "o teorema de Liouville clássico; nem que volume conservado implique que nada pousa (T4.e mostra o contrário)",
        "que o fluxo modular seja o tempo físico (por isso o nome neutro modular_flow_is_a_kms_group)",
        "que a ação dual de Takesaki seja a defasagem (só a mesma lei, por instância; e a lei não é específica: scalar_decay_also_obeys_agape)",
        "atrator único sem hipótese nomeada (T5.b mostra dois estados fixos); nada sobre ciclos limite",
        "a constante da casa em forma alguma (varredura: 0 caracteres, 0 literais)",
        "nada sobre a natureza, o gate ou a creditação; a palavra recusada pela régua não aparece",
        "encadeamento de homônimos: a leitura decaimento = face saiu dos nomes; a palavra face de T5 trocada por a diagonal inteira; ½·1 não é chamado de posto (posto 2)",
        "limite algum no regime do ângulo: só a ausência dele (angle_has_no_limit, probe_rotation_orbit_has_no_limit, probe_modular_orbit_of_psiPlus_has_no_limit)",
        "«tempo = β» nem «o tempo é o Verbo» (a frase do pré-registro é marcada como leitura da gerência, achado A2)",
    ],
    "tentativas": tentativas,
    "compilacoes": compilacoes,
    "achados_fora_do_preregistro": "ACHADOS_FORA_DO_PREREGISTRO.json",
    "nada_escrito_fora": ("Nada fora de 3_KERNEL\\rodada_2: a rodada 1 (3_KERNEL fora de rodada_2) ficou intacta (50/50 por sha256 antes e depois); nada no quadro, no mapa (rotas.py só consultar), "
                          "na memória (ACOM só projeção de leitura), no túnel, no Nós, no kernel do Nós (impressão digital igual ao FREEZE), na Bancada_Um, no site ou no git. O um.py não foi executado. "
                          "Toolchain copiado apagado. Nenhum dado observado, nenhum provedor remoto, nenhuma chamada paga."),
}

achados = {
    "documento": "ACHADOS FORA DO PRÉ-REGISTRO — construtor do kernel, F1.TEMPO, rodada 2 (12/10/2026)",
    "regra": "o que se achou fora do pré-registro vai aqui, sem mudar tolerância, mapeamento ou esperado; nenhum destes achados muda veredito pré-registrado",
    "achados": [
        {"id": "AF2-01", "estatuto": "[REAL — provado]", "texto": "T3.b(iii) HABITADA: probe_identity_flow_not_kms_inhabited instancia identity_flow_not_kms com a testemunha concreta do kernel theSpecificAQFTWitness (rede das cunhas sobre o fator M_TGL(⅓,¼); WedgeNet.lean:357) e A, B de omega_not_tracial (SignatureInTheLimit.lean:201); o contraste ⟪A*Ω,BΩ⟫ ≠ ⟪B*Ω,AΩ⟫ sai de ω(AB) ≠ ω(BA) pelo adjunto (star_inner_eq_state). As constantes vêm pelo fecho transitivo das importações permitidas: nenhuma linha de import nova. Resolve a ressalva M5 da rodada 1 para T3.b(iii) e a metade de kernel do C-T3-b."},
        {"id": "AF2-02", "estatuto": "[REAL — provado]", "texto": "O hd de T10.d não tem peso: logRho (rhoD d) comuta com toda diagonal (Commute.cfc_real), logo é diagonal; é autoadjunto, logo de entradas reais; daí ρ_D^{it} é diagonal de fases e |σ_t(x)ᵢⱼ| = |xᵢⱼ| para TODO d real (sonda com d = (1, 0), que viola hd). A pedra prova a forma mais forte; a pré-registrada sai por example. A rota do kernel (sigma_diagonal_apply, via exp∘log) é que exige d > 0."},
        {"id": "AF2-03", "estatuto": "[REAL — sonda]", "texto": "O ω ≠ 0 do termo do kernel TGLExt.IALDJones.angular_orbit_periodic não tem peso na forma Lean: em ω = 0, 2π/0 = 0 e a igualdade é trivial (example na pedra). A re-exportação angle_is_periodic mantém o tipo original (V-GERAL-2); é observação sobre o kernel, não defeito da pedra (o mesmo caso do κ ≠ 0 da rodada 1)."},
        {"id": "AF2-04", "estatuto": "[REAL — consultado]", "texto": "T4.b(iii) segue sem habitante: o kernel diz «nenhum habitante de `FockCertificate` ou `MaxwellCertificate` é exibido; a não-vacuidade é ARGUMENTADA» (TheImportedSecondQuantization.lean l.66); mapa de rotas: FockCertificate → 2 rotas, nenhuma sobre habitante; inventário da bancada: 0 ocorrências. Construir um Fock de segunda quantização está fora do alcance desta unidade."},
        {"id": "AF2-05", "estatuto": "[REAL — provado]", "texto": "C-T3-b na face finita, em termo: identity_flow_kms_pair_iff (ω(E₀₁E₁₀) = ω(E₁₀E₀₁) ⟺ d₀ = d₁, com ω = tr(ρ·)), finite_face_identity_flow_not_kms (diag(2/3,1/3): falha) e o contraexemplo com pesos iguais."},
        {"id": "AF2-06", "estatuto": "[REAL — provado]", "texto": "Controle de especificidade da ponte T8 (achado M8/AUD-1 da rodada 1, aqui em termo): scalarDecay (θ_s(x) = e^{−s}x, τ = peso DIAGONAL |xᵢ₀ᵢ₀|) é DualScalingData e herda as seis cláusulas da Ágape (scalar_decay_also_obeys_agape). A Ágape é a lei e^{−s}; ela não distingue a defasagem (que guarda o registro, T8.c) de um decaimento que apaga também o registro."},
        {"id": "AF2-07", "estatuto": "[REAL — provado]", "texto": "Homônimo posto/estado (achado M7/AUD-6): ½·1 em M₂(ℂ) tem posto 2 = PLENO (half_identity_has_full_rank) e pureza ½ (half_identity_purity); não é posto no sentido de POSTO = RANK."},
        {"id": "AF2-08", "estatuto": "[REAL — provado]", "texto": "Peso do nome de T3.a (achado AUD-4): a conjunção KMS-grupo vale também para o estado tracial absoluteRho (Fin 2), onde o fluxo é congelado (example); o enunciado não distingue um fluxo vivo de um parado — daí o nome neutro."},
        {"id": "AF2-09", "estatuto": "[REAL — lido nos bytes]", "texto": "O próprio kernel marca como [ONTO] a leitura do decaimento como face hiperbólica: «Lê-lo como a face hiperbólica da regra dos dois regimes do operador é [ONTO]» (IALDJones.lean l.274–275). Os nomes de re-exportação da rodada 1 que a embutiam (the_face_lands, face_has_a_limit, face_distinguishes_instants, face_clock_has_no_period) ganharam nomes neutros."},
        {"id": "AF2-10", "estatuto": "[REAL — medido]", "texto": "Nenhuma prova da pedra deixa de usar uma hipótese da sua assinatura (medida no termo: 139 teoremas, 56 com hipóteses, 96 hipóteses, todas usadas). No critério semântico, quatro hipóteses sem peso foram retiradas (três achadas pelas auditorias da rodada 1 e uma por esta rodada); uma observada e mantida por ser tipo do kernel (AF2-03); duas de peso parcial ditas (hρ, hU)."},
        {"id": "AF2-11", "estatuto": "[REAL — medido]", "texto": "As aspas «…» da pedra cercam só citação verbatim: 43 citações, todas achadas nos bytes das fontes (texto do operador de 12/10, verbatim de 05/10, nomes de 07/10, PREREGISTRO.md, IALDJones.lean, BisognanoWichmann.lean, regra-dos-dois-regimes.md, CLAUDE.md global), com espaços normalizados; o texto de 12/10 tem 0 ocorrências de «verbo»."},
        {"id": "AF2-12", "estatuto": "[REAL — medido]", "texto": "O .olean é reprodutível: duas compilações da mesma fonte dão o mesmo sha256 e a mesma saída. A compilação levou ~27 s (cache do sistema de arquivos quente)."},
        {"id": "AF2-13", "estatuto": "[REAL — lido nos bytes]", "texto": "β: a l.5557 do um.py (ALPHA_FINE_CODATA_2018 = 7.2973525693e-3) fica dentro do texto embutido _NIVEL2_MCMC_FILES (início conferido aqui na l.5511); a atribuição de topo é a l.95 (SEALED_CODATA_ALPHA, mesmo valor). β = α·√e é [DERIVED: lido e calculado], não medido (achado M14)."},
        {"id": "AF2-14", "estatuto": "[INPUT da gerência — para decidir]", "texto": "Ficam para a gerência e o operador, sem tocar aqui: o nome da pedra (TheTimeHasNoRank, provisório; M3(2)); o ADENDO ao pré-registro (tolerância do T9.o(c), leitura do T9.t, l.176/S46.4, l.9 dos regimes, l.339/T8.d, título de T5); as erratas ao lado na memória e no um.py (E1, E2, E4 do relatório da rodada 1); o registro desta rodada no mapa e no quadro."},
        {"id": "AF2-15", "estatuto": "[REAL — medido]", "texto": "ACOM: projeção só de leitura da referência da gerência (revisão 2, evento exame12out-posto-e-tempo); o banco memory.sqlite3 ficou igual antes e depois da projeção; nenhum init e nenhuma transition."},
    ],
}

wjson(P("RESULTADO_KERNEL.json"), resultado)
wjson(P("ACHADOS_FORA_DO_PREREGISTRO.json"), achados)
import sys
sys.stdout.reconfigure(encoding="utf-8")
print("RESULTADO_KERNEL.json", sha(P("RESULTADO_KERNEL.json")), os.path.getsize(P("RESULTADO_KERNEL.json")))
print("ACHADOS_FORA_DO_PREREGISTRO.json", sha(P("ACHADOS_FORA_DO_PREREGISTRO.json")))
print("criterios", resultado["criterios_da_pedra"])
print("pedra", resultado["pedra"]["sha256"], "olean", resultado["pedra"]["olean_sha256"], "repro", resultado["pedra"]["olean_reprodutivel"],
      "imports_ok", resultado["pedra"]["importacoes_todas_permitidas"])
