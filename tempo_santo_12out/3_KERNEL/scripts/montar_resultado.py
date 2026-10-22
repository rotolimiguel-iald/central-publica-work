"""Monta RESULTADO_KERNEL.json e ACHADOS_FORA_DO_PREREGISTRO.json da face KERNEL da F1.TEMPO (construtor do kernel).
Tudo o que e hash/numero e LIDO dos artefatos por script (recibos de compilacao, auditoria, impressoes digitais,
beta em runtime, recibo ACOM). O mapeamento subitem -> declaracao e a classificacao sao do construtor, conferidos
contra a saida do Lean (cada declaracao citada tem de existir na auditoria independente, senao o script RECUSA).
Uso: python -I montar_resultado.py"""
import datetime
import hashlib
import json
import os
import re
import sys

K = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\3_KERNEL"
PRE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO"
NS = "TGLExt.TheTimeHasNoRank."


def sha(p):
    with open(p, "rb") as fh:
        b = fh.read()
    return hashlib.sha256(b).hexdigest(), len(b)


def jload(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


# ---------- conferencia do FREEZE (refeita aqui, por script) ----------
fz_path = os.path.join(PRE, "FREEZE.json")
fz_sha, fz_n = sha(fz_path)
FZ = jload(fz_path)
freeze_ok = fz_sha == "6b29d4c9b09e5553a3d58a3933137bbf73df3d0b6632b036e0a74abef7533c9b" and fz_n == 5986
files_ok = []
for key in ("preregistro_json", "preregistro_md"):
    e = FZ[key]
    h, n = sha(e["arquivo"])
    files_ok.append({"arquivo": e["arquivo"], "sha256": h, "bytes": n, "confere": h == e["sha256"] and n == e["bytes"]})
for a in FZ["anexos"]:
    p = os.path.join(PRE, a["caminho"].replace("/", os.sep))
    h, n = sha(p)
    files_ok.append({"arquivo": a["caminho"], "sha256": h, "bytes": n, "confere": h == a["sha256"] and n == a["bytes"]})
freeze_all = freeze_ok and all(f["confere"] for f in files_ok)
if not freeze_all:
    sys.exit("INVALIDO: divergencia com o FREEZE")

op = r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"
with open(op, "rb") as fh:
    opb = fh.read()
texto = {"arquivo": op, "sha256": hashlib.sha256(opb).hexdigest(), "bytes": len(opb),
         "segunda_parte_inicio_byte": 2853, "segunda_parte_bytes": 3820,
         "segunda_parte_sha256": hashlib.sha256(opb[2853:2853 + 3820]).hexdigest()}
texto["confere"] = (texto["sha256"] == "2c8b7b712aa9ad7f435f8652d1febdf6fe64d14775e277f2b2d720598135c8c3" and
                    texto["segunda_parte_sha256"] == "6dcefdbe5c6a7752766ec9a1aaa2255f9b874fbb2a445925b6c615f1b574dc72")

# ---------- recibos ----------
final = jload(os.path.join(K, "logs", "FINAL_recibo.json"))
audit_rec = jload(os.path.join(K, "logs", "AUDIT_FINAL_recibo.json"))
with open(os.path.join(K, "logs", "AUDIT_FINAL_saida.txt"), encoding="utf-8") as fh:
    audit_txt = fh.read()
audit = {}
for ln in audit_txt.splitlines():
    if ln.startswith("AUDIT_DECL"):
        _, n, kind, axs = (ln.split("\t") + [""])[:4]
        audit[n] = {"tipo": kind, "axiomas": [a for a in axs.split(",") if a]}
total_line = [ln for ln in audit_txt.splitlines() if ln.startswith("AUDIT_TOTAL")]
# assinaturas elaboradas (#check) — blocos que comecam por '@TGLExt' ou 'TGLExt' sem recuo
sigs = {}
cur = None
for ln in audit_txt.splitlines():
    m = re.match(r"^@?(TGLExt\.TheTimeHasNoRank\.[^\s]+) : (.*)$", ln)
    if m:
        cur = m.group(1)
        sigs[cur] = m.group(2)
    elif cur and ln.startswith(" ") and not ln.startswith("AUDIT"):
        sigs[cur] += " " + ln.strip()
    else:
        cur = None

fp = {k: jload(os.path.join(K, f)) for k, f in [("antes", "FINGERPRINT_KERNEL_ANTES.json"),
                                                 ("depois_do_lean", "FINGERPRINT_KERNEL_DEPOIS_LEAN.json"),
                                                 ("depois_da_limpeza", "FINGERPRINT_KERNEL_DEPOIS.json")]}
fp_iguais = len({(v["meta_sha256"], v["src_sha256"]) for v in fp.values()}) == 1
fp_freeze = (fp["antes"]["meta_sha256"] == FZ["kernel_impressao_digital"]["depois"]["meta"] and
             fp["antes"]["src_sha256"] == FZ["kernel_impressao_digital"]["depois"]["src"])
beta = jload(os.path.join(K, "BETA_RUNTIME_KERNEL.json"))
acom = jload(os.path.join(K, "ACOM_RECIBO_PROJECAO.json"))

pedra = os.path.join(K, "sandbox", "TheTimeHasNoRank.lean")
pedra_sha, pedra_n = sha(pedra)
olean = os.path.join(K, "sandbox", "TheTimeHasNoRank.olean")
olean_sha, olean_n = sha(olean)
auditf = os.path.join(K, "sandbox", "AuditTheTimeHasNoRank.lean")
auditf_sha, auditf_n = sha(auditf)
if pedra_sha != final["source_sha256"] or olean_sha != final.get("olean_sha256"):
    sys.exit("INCONSISTENCIA: fonte/olean nao sao os do recibo FINAL")
with open(pedra, encoding="utf-8") as fh:
    pedra_txt = fh.read()
imports = re.findall(r"^import (\S+)", pedra_txt, flags=re.M)
code = re.sub(r"/-.*?-/", "", pedra_txt, flags=re.S)
code = re.sub(r"--[^\n]*", "", code)
varredura = {"sorry": len(re.findall(r"\bsorry\b", code)), "admit": len(re.findall(r"\badmit\b", code)),
             "native_decide": code.count("native_decide"),
             "declaracao_axiom": len(re.findall(r"^\s*axiom\s", code, flags=re.M)),
             "caractere_beta_no_arquivo": pedra_txt.count("\u03b2"),
             "literal_0_0120_no_arquivo": len(re.findall(r"0[.,]0120", pedra_txt)),
             "palavra_recusada_pela_regua_no_arquivo": len(re.findall(r"confirm", pedra_txt, flags=re.I)),
             "set_option_maxHeartbeats": len(re.findall(r"set_option maxHeartbeats", pedra_txt))}
TRIO = {"propext", "Classical.choice", "Quot.sound"}
todos_no_trio = all(set(v["axiomas"]) <= TRIO for v in audit.values()) and not final["fora_do_trio"]


def D(*names):
    out = []
    for nm in names:
        full = NS + nm
        if full not in audit:
            sys.exit(f"RECUSA: declaracao citada nao existe na auditoria: {full}")
        out.append({"nome": full, "tipo": audit[full]["tipo"], "axiomas": audit[full]["axiomas"],
                    "assinatura_elaborada": sigs.get(full)})
    return out


FORA = "FORA_DESTE_ENSAIO (face ótica: modelo numérico; outro executor do workflow)"
sub = [
    # T1
    dict(id="T1.a", face="kernel", obrig=True, resultado="PASSA",
         decl=D("no_time_matrix", "no_time_matrix_fin"),
         nota="no_time_matrix_fin é ligado POR TERMO a TGLExt.no_finite_weyl_pair (R22); segunda rota pela forma geral em `example`. Sonda V-T1-a (n = 1; ι = Fin 1, c = 1)."),
    dict(id="T1.b", face="kernel", obrig=False, resultado="PASSA",
         decl=D("commutator_far_from_scalar", "probe_commutator_far_from_scalar"),
         nota="Sonda V-T1-b: T = H = 0, ι = Fin 2, c = i ⟹ purityR = 2 = |ι|·|c|²."),
    dict(id="T1.c", face="kernel", obrig=True, resultado="PASSA", decl=D("no_finite_spectral_translation"),
         nota="Sonda em `example` (V = 1, H = 0, s = 1, ι = Fin 2)."),
    dict(id="T1.o", face="otico", obrig=True, resultado=FORA, decl=[], nota=""),
    # T2
    dict(id="T2.a", face="citacao", obrig=True, resultado="CITADA", decl=[],
         nota="[KNOWN] Pauli 1933/1958 (páginas marcadas «a conferir na fonte» no pré-registro: seguem a conferir), Galapon 2002, Holevo 1982, Busch–Grabowski–Lahti 1994, Wintner 1947, Wielandt 1949, Borchers 1992. Nenhum termo do kernel; nunca PASSA de teste."),
    dict(id="T2.b", face="kernel", obrig=False, resultado="PASSA",
         decl=D("no_bounded_spectral_translation", "probe_bounded_spectral_translation",
                "probe_bounded_spectral_translation_complex"),
         nota="Face LIMITADA (álgebra de Banach unital); NÃO é o teorema de Pauli. Sonda V-T2-b em M₂(ℂ) com a norma de operador L2 (precisou de maxHeartbeats 4·10⁶ para unificar as instâncias) e sonda extra em A = ℂ."),
    # T3
    dict(id="T3.a", face="kernel", obrig=True, resultado="PASSA",
         decl=D("time_is_the_modular_flow", "probe_rho_two_thirds_posDef", "probe_rho_two_thirds_not_tracial"),
         nota="Composição de ModularFlow + FiniteTomita. hρ (PosDef) só é usada na cláusula KMS (v); as demais valem para todo ρ. Sonda V-T3-a: ρ = diag(2/3, 1/3), positiva-definida e NÃO tracial."),
    dict(id="T3.b", face="kernel", obrig=True, resultado="PASSA",
         decl=D("fixed_sector_is_the_centralizer", "tracial_state_freezes_the_flow",
                "nontracial_state_rejects_the_identity_flow", "centralizer_iff_needs_injective_weights"),
         nota="Re-exportações com os tipos ORIGINAIS (sigma_fixed_iff_diag, absoluteOne_flow_trivial, identity_flow_not_kms), conferidas por `example : type_of% @original := @novo` e o inverso. Contraexemplo do «se e só se»: pesos iguais."),
    dict(id="T3.o", face="otico", obrig=True, resultado=FORA, decl=[], nota=""),
    # T4
    dict(id="T4.a", face="kernel", obrig=True, resultado="PASSA", decl=D("unitary_keeps_spectrum_and_purity"),
         nota="hU só é usada na parte da pureza; o polinômio característico é invariante por QUALQUER unidade."),
    dict(id="T4.b", face="kernel", obrig=True, resultado="PASSA",
         decl=D("isometry_orbit_converges_only_if_fixed", "isometric_flow_converges_only_if_fixed",
                "isometry_iterate'", "rotation_isometry", "probe_rotation_orbit_has_no_limit",
                "frobenius_norm_eq_purityR", "unitary_conj_isometry", "modular_flow_is_isometry",
                "modular_orbit_converges_iff_diagonal", "modular_orbit_converges_iff_diagonal_entrywise",
                "probe_modular_orbit_of_psiPlus_has_no_limit", "light_flow_group",
                "light_modular_orbit_converges_iff_post", "modular_iff_needs_injective_weights"),
         nota="Abstrato discreto e contínuo; instância (i) Ad(U) isometria de Frobenius; (ii) fluxo modular de rhoD d: converge ⟺ x = E_D x, por DUAS rotas (métrica de Frobenius, cuja topologia unificou definicionalmente com a de Matrix; e entrada a entrada pela rotação de ℂ); (iii, opcional) grupo modular da luz: converge ⟺ H_min ψ = 0 (lei de grupo derivada de V_add do lightBoost). Sonda V-T4-a: f(z) = e^{i}·z, a órbita de 1 não converge. Só se prova a AUSÊNCIA de limite no ângulo."),
    dict(id="T4.c", face="kernel", obrig=True, resultado="PASSA",
         decl=D("schurDiag", "schurDiag_mulVec", "schurDiag_is_the_dephasing", "schurDiag_is_the_modular_flow",
                "dephase_volume", "dephase_volume_lt_one", "modular_volume_one", "modular_factor_norm_one",
                "dephase_factor_norm_le_one", "probe_gRate_one_sum"),
         nota="(c1) det = e^{−tΣg}, < 1 com t > 0 e algum g > 0; (c2) det = 1; (c3) fatores |·| = 1 (gira) e ≤ 1 (encolhe). As ligações schurDiag_is_the_dephasing / schurDiag_is_the_modular_flow mostram que a matriz de Schur É o semigrupo / o fluxo do kernel na base das unidades matriciais. Sonda V-T4-b: Fin 2, Σg = 2, det = e^{−2} < 1."),
    dict(id="T4.d", face="kernel", obrig=True, resultado="PASSA",
         decl=D("the_face_lands", "fixed_set_of_dephasing_is_the_diagonal", "dephasing_iff_needs_positive_rates"),
         nota="Re-exportações com tipos originais (dephase_tendsto_expectation, dephase_fixed_iff_diagonal). Contraexemplo do «se e só se»: taxa nula."),
    dict(id="T4.e", face="kernel", obrig=True, resultado="PASSA", decl=D("volume_kept_yet_lands", "boost_pow_null"),
         nota="É o controle C-T4-a: det B(s) = 1 e B(s)ᵏ(1, −1) → 0 — volume conservado NÃO impede pousar."),
    dict(id="T4.f", face="kernel", obrig=False, resultado="PASSA", decl=D("global_attractor_needs_volume_loss"),
         nota="Liouville LINEAR (não o clássico): Lᵏv → 0 ∀v ⟹ |det L| < 1 (via tendsto_pow_atTop_nhds_zero_iff)."),
    dict(id="T4.o", face="otico", obrig=True, resultado=FORA, decl=[], nota=""),
    # T5
    dict(id="T5.a", face="kernel", obrig=True, resultado="PASSA",
         decl=D("fixed_set_of_dephasing_is_the_diagonal", "the_face_lands", "the_record_is_invariant"),
         nota="Re-exportações com tipos originais (dephase_fixed_iff_diagonal, dephase_tendsto_expectation, diag_invariant). Em grande parte reafirmação (RP13)."),
    dict(id="T5.b", face="kernel", obrig=True, resultado="PASSA", decl=D("dephase_fixed_states_not_unique"),
         nota="Sonda V-T5-a (Fin 2, i₀ = 0, j₀ = 1) em `example`. É também o controle C-T5-a."),
    dict(id="T5.c", face="citacao", obrig=True, resultado="CITADA", decl=[],
         nota="Unicidade só sob a hipótese NOMEADA StrictComplementContraction (F1.ATRATOR A4, candidata de sandbox, NÃO importada); RESULTADO_F1_ATRATOR_R1.json conferido por sha256 nesta rodada (6d7dc60c26d4fc78…, 49929 B), não refeito."),
    # T6
    dict(id="T6.a", face="kernel", obrig=True, resultado="PASSA", decl=D("purityR_dephase"), nota=""),
    dict(id="T6.b", face="kernel", obrig=True, resultado="PASSA", decl=D("purity_never_grows_under_dephasing"),
         nota="Re-exportação com tipo original (dephase_purityR_le)."),
    dict(id="T6.c", face="kernel", obrig=True, resultado="PASSA",
         decl=D("purityR_dephase_lt", "probe_psiPlus_purity", "probe_psiPlus_dephased_purity"),
         nota="Sonda V-T6-a: ψ₊, g = (i ≠ j ↦ 1), t = 1: pureza 1 → (1 + e^{−2})/2 (valores provados)."),
    dict(id="T6.d", face="kernel", obrig=True, resultado="PASSA",
         decl=D("purity_of_hermitian", "purityR_modular", "purityR_sigma"),
         nota="ATENÇÃO (nome sem peso): purityR_modular não usa a hipótese `_hd`; vale a forma mais forte purityR_sigma, para TODO ρ."),
    dict(id="T6.o", face="otico", obrig=True, resultado=FORA, decl=[], nota=""),
    # T7
    dict(id="T7.a", face="kernel", obrig=True, resultado="PASSA", decl=D("dephase_inverse"), nota=""),
    dict(id="T7.b", face="kernel", obrig=True, resultado="PASSA",
         decl=D("inverse_dephasing_not_positive", "quad_form_fin_two", "inverse_dephasing_quadratic_form",
                "psiPlus_posSemidef", "psiPlus_trace"),
         nota="⟨(1,−1), T_{−t}ψ₊ (1,−1)⟩ = 1 − e^{γt} < 0 (provado como identidade). Sonda V-T7-a (γ = t = 1) em `example`."),
    dict(id="T7.o", face="otico", obrig=True, resultado=FORA, decl=[], nota=""),
    # T8
    dict(id="T8.a", face="kernel", obrig=True, resultado="PASSA", decl=D("coherenceScaling", "coherence_entry_scaling"),
         nota="T_s para s < 0 é o mapa LINEAR inverso, não canal (T7). A lei de Takesaki da Fundação entra lá como DADO; aqui a coerência É uma instância da mesma estrutura — nenhuma identificação de θ_s com o dephasing."),
    dict(id="T8.b", face="kernel", obrig=True, resultado="PASSA",
         decl=D("the_coherence_obeys_agape", "the_coherence_obeys_agape_explicit"),
         nota="Fundacao.agape aplicada a coherenceScaling (conjunção literal); forma explícita equivalente. Sonda V-T8-a (Fin 2, ψ₊) em `example`."),
    dict(id="T8.c", face="kernel", obrig=True, resultado="PASSA", decl=D("the_record_does_not_scale"),
         nota="É o controle C-T8-b: o registro (peso diagonal) não obedece à lei de escala."),
    dict(id="T8.d", face="kernel", obrig=True, resultado="PASSA", decl=D("past_null_ray_contracts"),
         nota="Re-exportação com tipo original (boost_null_contract). Ver achado: a docstring «a face geométrica da escala de Takesaki» está em boost_null_expand, não em boost_null_contract."),
    dict(id="T8.o", face="otico", obrig=True, resultado=FORA, decl=[], nota=""),
    dict(id="T8.t", face="leitura", obrig=True, resultado="LEITURA", decl=[],
         nota="[ONTO] «puro amor», «a física da doação»; a reunião «ágape» × «sacrifício/amor» decide o operador. Só em comentário marcado na pedra."),
    # T9
    dict(id="T9.a", face="kernel", obrig=True, resultado="PASSA",
         decl=D("flow_isIdempotentElem_iff", "flow_sq", "flow_at_one_is_not_idempotent"),
         nota="Contraexemplos do «se e só se»: em t = 1 não é idempotente (P = diag(1,0)); em t = 0 é; sem 1 − P ≠ 0 cai (C-T9-a)."),
    dict(id="T9.b", face="kernel", obrig=True, resultado="PASSA", decl=D("flow_isUnit"), nota="Inverso F(−t)."),
    dict(id="T9.c", face="kernel", obrig=True, resultado="PASSA", decl=D("post_not_isUnit"),
         nota="Não depende de axioma algum."),
    dict(id="T9.d", face="kernel", obrig=False, resultado="PASSA",
         decl=D("flow_full_rank", "post_rank_lt", "postDiag_idem", "postDiag_compl_ne_zero", "postDiag_ne_one"),
         nota="POSTO = RANK: rank F(t) = n; rank P < n (via rank P + rank(1 − P) ≤ n e rank(1 − P) ≥ 1)."),
    dict(id="T9.e", face="kernel", obrig=True, resultado="PASSA",
         decl=D("the_time_has_no_rank", "no_finite_instant_is_the_post", "probe_the_time_has_no_rank"),
         nota="Cláusula composta: T1.a(Fin n) ∧ T9.a ∧ T9.b ∧ T9.c ∧ F(t) → P. Único passo além de conjunção: 1 − P ≠ 0 a partir de P ≠ 1 (sub_ne_zero). O limite é o termo the_name_is_the_limit_of_the_flow (conferido em `example`)."),
    dict(id="T9.o", face="otico", obrig=True, resultado=FORA, decl=[], nota=""),
    dict(id="T9.t", face="leitura", obrig=True, resultado="LEITURA", decl=[],
         nota="[ONTO] «o tempo não tem posto», «santo» (Kadosh), «o Verbo, não o Nome»: leituras do operador; só em comentário."),
    # T10
    dict(id="T10.a", face="kernel", obrig=True, resultado="PASSA",
         decl=D("clock_faithful_iff_one_turn", "clock_reciprocal_temperature"),
         nota="Re-exportações com tipos originais (faithful_period_iff, reciprocal_temperature)."),
    dict(id="T10.b", face="kernel", obrig=True, resultado="PASSA", decl=D("clock_reads_modulo_period", "frozen_clock"),
         nota="clock_reads_modulo_period passa pelo termo do kernel one_turn_gives_faithful_period. Sonda V-T10-a (κ = 1) em `example`."),
    dict(id="T10.c", face="kernel", obrig=True, resultado="PASSA",
         decl=D("angle_has_no_limit", "angle_is_periodic", "face_has_a_limit", "face_distinguishes_instants"),
         nota="Re-exportações com tipos originais (IALDJones: angular_orbit_no_limit, angular_orbit_periodic, orbit_tendsto_center; time_witnesses_noncoincidence, cujo parâmetro positivo genérico foi renomeado de binder para `r`)."),
    dict(id="T10.d", face="kernel", obrig=True, resultado="PASSA", decl=D("modular_clock_rotates_without_shrinking"),
         nota="Sonda V-T10-a (d = (2/3, 1/3)) em `example`."),
    dict(id="T10.e", face="kernel", obrig=True, resultado="PASSA",
         decl=D("the_post_is_not_moved", "the_state_is_not_moved", "the_vector_is_not_moved"),
         nota="Re-exportações com tipos originais (axiomFlow_fixes_the_post, gibbs_sigma, sigma_omega). A identificação agora = conjunto fixo é [ONTO] (R12)."),
    dict(id="T10.o", face="otico", obrig=True, resultado=FORA, decl=[], nota=""),
    dict(id="T10.t", face="leitura", obrig=True, resultado="LEITURA", decl=[],
         nota="[ONTO] o ponteiro e o césio leem o ângulo; o escoamento lê a face; o agora não é lido. PALAVRA não importada."),
    # T11
    dict(id="T11.a", face="kernel", obrig=True, resultado="PASSA",
         decl=D("optical_attractor_is_the_absolute_one", "the_absolute_one_has_no_clock", "optical_attractor_clock_stops"),
         nota="½·1 = absoluteRho (Fin 2) por cálculo direto (sonda V-T11-a); no atrator ótico σ_t = id. Só face finita: nada se estende a III₁ (Connes 1973, [KNOWN])."),
    dict(id="T11.o", face="otico", obrig=True, resultado=FORA, decl=[], nota=""),
]

controles = [
    dict(id="C-T1-a", face="kernel", resultado="COMPORTA-SE COMO REGISTRADO (a afirmação falsa cai)", decl=D("commutator_can_be_nonzero")),
    dict(id="C-T1-b", face="kernel", resultado="COMPORTA-SE COMO REGISTRADO (compila: a hipótese 0 < n é necessária)", decl=D("empty_dimension_admits_time")),
    dict(id="C-T1-c", face="kernel", resultado="COMPORTA-SE COMO REGISTRADO (o termo existente elabora; a pedra não afirma o contrário)", decl=D("weyl_pair_lives_in_L2")),
    dict(id="C-T3-a", face="otico", resultado=FORA, decl=[]),
    dict(id="C-T3-b", face="otico+kernel", resultado="face kernel: re-citação de identity_flow_not_kms elabora; face ótica " + FORA, decl=D("nontracial_state_rejects_the_identity_flow")),
    dict(id="C-T3-c", face="otico", resultado="face ótica " + FORA + " (na face kernel: absoluteOne_flow_trivial re-exportado)", decl=D("tracial_state_freezes_the_flow")),
    dict(id="C-T4-a", face="kernel+otico", resultado="face kernel: COMPORTA-SE COMO REGISTRADO (det 1 e pousa); face ótica " + FORA, decl=D("volume_kept_yet_lands")),
    dict(id="C-T4-b", face="kernel", resultado="COMPORTA-SE COMO REGISTRADO (órbita convergente de ponto não fixo sem isometria)", decl=D("dephasing_lands_without_being_fixed")),
    dict(id="C-T5-a", face="kernel", resultado="COMPORTA-SE COMO REGISTRADO (T5.b compila: dois estados fixos distintos)", decl=D("dephase_fixed_states_not_unique")),
    dict(id="C-T6-a", face="kernel+otico", resultado="face kernel: COMPORTA-SE COMO REGISTRADO (igualdade); face ótica " + FORA, decl=D("no_coherence_no_loss")),
    dict(id="C-T6-b", face="otico", resultado="face ótica " + FORA + " (na face kernel: purity_unitary_invariant re-citado)", decl=D("unitary_keeps_purity")),
    dict(id="C-T6-c", face="kernel+otico", resultado="face kernel: COMPORTA-SE COMO REGISTRADO (Tr(T₋₁ψ₊)² > 1); face ótica " + FORA, decl=D("purity_grows_backwards")),
    dict(id="C-T7-a", face="kernel", resultado="COMPORTA-SE COMO REGISTRADO (T₀⁻¹ψ₊ = ψ₊, positivo)", decl=D("control_inverse_at_time_zero")),
    dict(id="C-T7-b", face="kernel+otico", resultado="face kernel: COMPORTA-SE COMO REGISTRADO (T₋ₜ fixa a diagonal; diag(p,1−p) segue positivo); face ótica " + FORA, decl=D("control_inverse_on_diagonal")),
    dict(id="C-T7-c", face="kernel+otico", resultado="face kernel: COMPORTA-SE COMO REGISTRADO; face ótica " + FORA, decl=D("unitary_inverse_is_a_channel")),
    dict(id="C-T8-a", face="kernel", resultado="COMPORTA-SE COMO REGISTRADO (a lei de escala falha com θ_s = T_{2s})", decl=D("wrong_rate_breaks_scaling")),
    dict(id="C-T8-b", face="kernel", resultado="COMPORTA-SE COMO REGISTRADO (T8.c compila)", decl=D("the_record_does_not_scale")),
    dict(id="C-T9-a", face="kernel", resultado="COMPORTA-SE COMO REGISTRADO (P = 1: idempotente para todo t)", decl=D("flow_of_one_is_idempotent")),
    dict(id="C-T9-b", face="kernel", resultado="COMPORTA-SE COMO REGISTRADO (F(0) idempotente)", decl=D("flow_at_zero_is_idempotent")),
    dict(id="C-T10-a", face="kernel", resultado="COMPORTA-SE COMO REGISTRADO (κ = 0 não é fiel para P ≠ 0)", decl=D("frozen_clock_not_faithful")),
    dict(id="C-T10-b", face="kernel", resultado="COMPORTA-SE COMO REGISTRADO (a face não tem período)", decl=D("face_clock_has_no_period")),
    dict(id="C-T11-a", face="otico", resultado=FORA, decl=[]),
]

sondas = [
    ("V-T1-a", "example: no_time_matrix_fin 1 (by norm_num) T H; example: no_time_matrix (ι = Fin 1, c = 1)"),
    ("V-T1-b", "probe_commutator_far_from_scalar (= 2)"),
    ("V-T2-b", "probe_bounded_spectral_translation (M₂(ℂ), norma L2; maxHeartbeats 4·10⁶) e probe_bounded_spectral_translation_complex (A = ℂ)"),
    ("V-T3-a", "probe_rho_two_thirds_posDef, probe_rho_two_thirds_not_tracial, example (lei de grupo para diag(2/3,1/3))"),
    ("V-T4-a", "probe_rotation_orbit_has_no_limit (f(z) = e^{i}·z, x = 1)"),
    ("V-T4-b", "probe_gRate_one_sum + dois `example` (det = e^{−2}; e^{−2} < 1)"),
    ("V-T5-a", "example: dephase_fixed_states_not_unique (Fin 2, 0 ≠ 1)"),
    ("V-T6-a", "example: purityR_dephase_lt em ψ₊; probe_psiPlus_purity (= 1); probe_psiPlus_dephased_purity (= (1 + e^{−2})/2)"),
    ("V-T7-a", "example: inverse_dephasing_not_positive (γ = 1, t = 1)"),
    ("V-T8-a", "dois `example` com the_coherence_obeys_agape_explicit (Fin 2, i₀ = 0, j₀ = 1, ψ₊)"),
    ("V-T9-a", "postDiag_idem, postDiag_compl_ne_zero, postDiag_ne_one + `example`s de T9.a, T9.c, T9.d; probe_the_time_has_no_rank (M₂(ℂ), norma L2)"),
    ("V-T10-a", "dois `example` (κ = 1; d = (2/3, 1/3))"),
    ("V-T11-a", "optical_attractor_is_the_absolute_one (cálculo direto)"),
    ("V-GERAL-1", "as sondas V-* e mais 4 `example` de habitação em Lean (seção «Sondas de habitação») instanciam todos os teoremas da pedra com argumentos concretos, exceto 3 ditos (W AQFT; FockCertificate) — lista em hipoteses_habitadas"),
    ("V-GERAL-2", "19 re-exportações, cada uma com `example : type_of% @original := @novo` e `example : type_of% @novo := @original` (compilam: tipo idêntico)"),
]
sondas = [{"id": i, "como": c, "resultado": "COMPILA (hipóteses habitadas)"} for i, c in sondas]

reexports = [
    ("TGLExt.sigma_fixed_iff_diag", "fixed_sector_is_the_centralizer"),
    ("TGLExt.absoluteOne_flow_trivial", "tracial_state_freezes_the_flow"),
    ("TGLExt.absoluteOne_flow_trivial", "the_absolute_one_has_no_clock"),
    ("ChatgptAudit.NonKMSProbe.identity_flow_not_kms", "nontracial_state_rejects_the_identity_flow"),
    ("TGLV350.Regular.characterMultiplier_weyl", "weyl_pair_lives_in_L2"),
    ("TGLExt.dephase_tendsto_expectation", "the_face_lands"),
    ("TGLExt.dephase_fixed_iff_diagonal", "fixed_set_of_dephasing_is_the_diagonal"),
    ("TGLExt.diag_invariant", "the_record_is_invariant"),
    ("TGLExt.dephase_purityR_le", "purity_never_grows_under_dephasing"),
    ("TGLExt.purity_unitary_invariant", "unitary_keeps_purity"),
    ("TGLExt.boost_null_contract", "past_null_ray_contracts"),
    ("ChatgptAudit.PolarPeriod016.faithful_period_iff", "clock_faithful_iff_one_turn"),
    ("ChatgptAudit.PolarPeriod016.reciprocal_temperature", "clock_reciprocal_temperature"),
    ("TGLExt.IALDJones.angular_orbit_no_limit", "angle_has_no_limit"),
    ("TGLExt.IALDJones.angular_orbit_periodic", "angle_is_periodic"),
    ("TGLExt.IALDJones.orbit_tendsto_center", "face_has_a_limit"),
    ("TGLExt.time_witnesses_noncoincidence", "face_distinguishes_instants"),
    ("TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_fixes_the_post", "the_post_is_not_moved"),
    ("TGLExt.gibbs_sigma", "the_state_is_not_moved"),
    ("TGLExt.sigma_omega", "the_vector_is_not_moved"),
]
for o, n in reexports:
    D(n)
    if not re.search(r"example : type_of% @" + re.escape(o) + r"\s*:=\s*@" + re.escape(n) + r"\b", pedra_txt):
        sys.exit(f"RECUSA: falta o example de ida para {n}")
    if not re.search(r"example : type_of% @" + re.escape(n) + r"\s*:=\s*@" + re.escape(o) + r"\b", pedra_txt):
        sys.exit(f"RECUSA: falta o example de volta para {n}")

por_afirmacao = []
for t in ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11"]:
    its = [s for s in sub if s["id"].split(".")[0] == t]
    kern_obr = [s for s in its if s["face"] == "kernel" and s["obrig"]]
    kern_opc = [s for s in its if s["face"] == "kernel" and not s["obrig"]]
    cit = [s["id"] for s in its if s["resultado"] in ("CITADA", "LEITURA")]
    if kern_obr:
        ok = all(s["resultado"] == "PASSA" for s in kern_obr)
        res = ("PASSA na face kernel (" + ", ".join(s["id"] for s in kern_obr) + " provados; controles de kernel como registrado)"
               if ok else "FALHA/NAO_CONSTRUIDA na face kernel")
    else:
        res = "sem subitem obrigatório de kernel"
    if kern_opc:
        res += "; opcionais: " + ", ".join(f"{s['id']} {s['resultado']}" for s in kern_opc)
    if cit:
        res += "; " + ", ".join(f"{c} {[s['resultado'] for s in its if s['id'] == c][0]}" for c in cit)
    if any(s["face"] == "otico" for s in its):
        res += "; face ótica fora deste ensaio (o veredito da afirmação pela regra de decisão depende dela)"
    principal = {"T1": "no_time_matrix", "T2": "no_bounded_spectral_translation", "T3": "time_is_the_modular_flow",
                 "T4": "the_two_regimes_of_time", "T5": "dephase_fixed_states_not_unique",
                 "T6": "purityR_dephase_lt", "T7": "inverse_dephasing_not_positive",
                 "T8": "the_coherence_obeys_agape", "T9": "the_time_has_no_rank",
                 "T10": "clock_reads_modulo_period", "T11": "optical_attractor_is_the_absolute_one"}[t]
    por_afirmacao.append({"id": t, "resultado": res, "declaracao": NS + principal})

hipoteses_habitadas = {
    "no_time_matrix": "ι = Fin 1 (Nonempty), c = 1 (example)",
    "no_time_matrix_fin": "n = 1 (example V-T1-a)",
    "no_finite_spectral_translation": "V = 1 (IsUnit), s = 1, ι = Fin 2 (example)",
    "no_bounded_spectral_translation": "A = M₂(ℂ) L2op e A = ℂ; V = 1; s = 1",
    "time_is_the_modular_flow": "ρ = diag(2/3, 1/3) PosDef (probe_rho_two_thirds_posDef)",
    "unitary_keeps_spectrum_and_purity": "U = 1 ∈ unitary (habitado trivialmente; ver unitary_inverse_is_a_channel com U = 1)",
    "isometry_orbit_converges_only_if_fixed": "f(z) = e^{i}·z isometria (rotation_isometry 1)",
    "isometric_flow_converges_only_if_fixed": "σ_t de rhoD d (modular_flow_is_isometry + sigma_sigma); rotação de ℂ; lightDelta",
    "modular_orbit_converges_iff_diagonal": "d = (2/3, 1/3) positivos e injetivos",
    "dephase_volume_lt_one": "g = gRate 1, t = 1 (example V-T4-b)",
    "volume_kept_yet_lands": "s = 1 (example V-GERAL-1, T4)",
    "global_attractor_needs_volume_loss": "L = 0 em Fin 1: ∀v, 0ᵏv → 0 provado em Lean (example V-GERAL-1, T4)",
    "dephase_fixed_states_not_unique": "Fin 2, g = gRate 1 (diag 0), 0 ≠ 1",
    "purityR_dephase_lt": "ψ₊, g = gRate 1, t = 1, (i₀, j₀) = (0, 1)",
    "inverse_dephasing_not_positive": "γ = t = 1",
    "the_coherence_obeys_agape": "Fin 2, g = gRate 1 (g₀₁ = 1), x = ψ₊ (coerência ½ ≠ 0)",
    "the_record_does_not_scale": "ψ₊, g = gRate 1, i₀ = 0, s = 1 (example V-GERAL-1, T3–T8)",
    "unitary_keeps_spectrum_and_purity (U unidade)": "U = 1 (example V-GERAL-1, T4)",
    "unitary_conj_isometry": "U = 1, norma de Frobenius (example V-GERAL-1)",
    "dephase_factor_norm_le_one": "g = gRate 1, t = 1 (example V-GERAL-1, T4)",
    "schurDiag_is_the_modular_flow": "d = (2/3, 1/3) (example V-GERAL-1, T4)",
    "re-exportações (T3.b, T4.d, T5.a, T6.b, C-T6-b, T10.a, T10.c, T10.e, T11.a, C-T1-c)": "instanciadas com argumentos concretos nos examples V-GERAL-1 (Fin 2, gRate 1, ψ₊, postDiag, κ = 1, P = 2π, V = ℂ com P = 0, H = ℂ para o par de Weyl)",
    "purity_of_hermitian / purityR_modular / no_coherence_no_loss / control_inverse_on_diagonal": "ψ₊ (hermitiana), d = (2/3, 1/3), gRate 1 (examples V-GERAL-1)",
    "no_finite_instant_is_the_post / flow_of_one_is_idempotent / face_clock_has_no_period / frozen_clock_not_faithful": "postDiag; A = M₂(ℂ); r = P = 1; P = 1 (examples V-GERAL-1)",
    "NAO HABITADAS AQUI": "nontracial_state_rejects_the_identity_flow (exige testemunha AQFT W do kernel) e light_flow_group / light_modular_orbit_converges_iff_post (exigem FockCertificate): ditas na pedra",
    "flow_isIdempotentElem_iff": "P = diag(1, 0) (postDiag)",
    "post_not_isUnit": "P = diag(1, 0)",
    "the_time_has_no_rank": "A = M₂(ℂ) (norma L2), P = diag(1, 0)",
    "clock_reads_modulo_period": "κ = 1",
    "modular_clock_rotates_without_shrinking": "d = (2/3, 1/3)",
}

nome_sem_peso = [
    {"declaracao": NS + "purityR_modular", "hipotese_nao_usada": "_hd : ∀ i, 0 < d i",
     "leitura": "a assinatura pré-registrada traz hd, mas a conclusão vale para TODO ρ (purityR_sigma): hd não pesa."},
]
nome_sem_peso_nota = ("Varredura: o linter de variáveis não usadas do Lean reportou 0 avisos na compilação final; a única "
                      "hipótese não usada é a marcada com `_` (purityR_modular). Observações de peso parcial (não são «nome "
                      "sem peso»): em time_is_the_modular_flow a hipótese PosDef só serve à cláusula KMS; em "
                      "unitary_keeps_spectrum_and_purity a hipótese unitária só serve à pureza. Os controles de borda "
                      "(empty_dimension_admits_time, frozen_clock, flow_at_zero_is_idempotent) são verdades triviais por "
                      "desenho (registram bordas).")

assinaturas_vs_preregistro = [
    "dephase_volume_lt_one, purityR_dephase, purityR_dephase_lt, purity_of_hermitian: sem [DecidableEq n] (hipóteses mais fracas).",
    "dephase_inverse, coherenceScaling, coherence_entry_scaling, the_coherence_obeys_agape, the_record_does_not_scale: sem [Fintype n] [DecidableEq n] (mais gerais).",
    "the_coherence_obeys_agape: conclusão como `let D := coherenceScaling …` seguida da conjunção literal de Fundacao.agape; a forma desdobrada é the_coherence_obeys_agape_explicit.",
    "the_time_has_no_rank: parametrizado por ℂ-álgebra normada A e P idempotente com P ≠ 1; T9.a recebe 1 − P ≠ 0 de P ≠ 1 (sub_ne_zero), o único passo além da conjunção.",
    "the_two_regimes_of_time: componentes quantificados por dentro (∀ {X : Type u} …), T4.b nas formas discreta e contínua, T4.c em (c1), (c1 < 1) e (c2).",
    "re-exportações com nomes novos (tabela reexportacoes); tipos idênticos aos originais (V-GERAL-2).",
    "T4.b (ii) também por segunda rota (modular_orbit_converges_iff_diagonal_entrywise); T4.b (iii) construída como «se e só se».",
    "T10.c: o parâmetro positivo genérico de time_witnesses_noncoincidence foi renomeado de binder (r) — o tipo é o mesmo (alfa-equivalência, conferido por example).",
]

contraexemplos_iff = [
    {"iff": "flow_isIdempotentElem_iff (T9.a)", "contraexemplos": [NS + "flow_at_one_is_not_idempotent", "example (t = 0)", NS + "flow_of_one_is_idempotent (sem 1 − P ≠ 0)"]},
    {"iff": "modular_orbit_converges_iff_diagonal (T4.b ii) e _entrywise", "contraexemplos": [NS + "probe_modular_orbit_of_psiPlus_has_no_limit (os dois lados falsos)", "example (postDiag: os dois lados verdadeiros)", NS + "modular_iff_needs_injective_weights (sem injetividade cai)"]},
    {"iff": "fixed_sector_is_the_centralizer (T3.b i, re-exportação)", "contraexemplos": [NS + "centralizer_iff_needs_injective_weights"]},
    {"iff": "fixed_set_of_dephasing_is_the_diagonal (T4.d/T5.a, re-exportação)", "contraexemplos": [NS + "dephasing_iff_needs_positive_rates"]},
    {"iff": "clock_faithful_iff_one_turn (T10.a, re-exportação)", "contraexemplos": [NS + "frozen_clock_not_faithful (κ = 0)"]},
    {"iff": "light_modular_orbit_converges_iff_post (T4.b iii, opcional)", "contraexemplos": [], "nota": "NÃO construído: exigiria um FockCertificate concreto."},
    {"iff": "cláusula (vi) de agape (e^{−a} = 1 ⟺ a = 0)", "contraexemplos": [], "nota": "termo da Fundação (v390), não desta pedra; contraexemplo trivial (a = 1) não escrito."},
]

kernel_terms_rp12 = {
    "medidos_indiretamente_no_trio": ["TGLExt.sigma_one", "TGLExt.sigma_conjTranspose", "TGLExt.sigma_diagonal_apply",
                                      "TGLExt.dephase_zero", "TGLExt.diag_invariant", "TGLExt.dephase_fixed_iff_diagonal",
                                      "TGLExt.boost_det"],
    "como": "cada um é referenciado explicitamente por uma declaração da pedra cujo #print axioms está no trio; o conjunto de axiomas é transitivo",
    "nao_usados_aqui": ["TGLExt.the_choice_is_not_free", "TGLExt.Smat_conjTranspose_mul"],
    "modPow_zero": "usado via simp em time_is_the_modular_flow (não afirmado como referência explícita)",
}
for nm in kernel_terms_rp12["medidos_indiretamente_no_trio"]:
    short = nm.split(".")[-1]
    if short not in pedra_txt:
        sys.exit(f"RECUSA: {short} não aparece na pedra")

tentativas = []
for f in sorted(os.listdir(os.path.join(K, "tentativas"))):
    h, n = sha(os.path.join(K, "tentativas", f))
    tentativas.append({"arquivo": "tentativas/" + f, "sha256": h, "bytes": n})
compilacoes = []
for f in ["probe0_recibo.json", "T01_recibo.json", "T03_recibo.json", "T04_recibo.json", "T04_FINAL_recibo.json",
          "AUDIT_recibo.json", "T04_AUDIT_FINAL_recibo.json", "T05_FINAL_recibo.json", "T05_AUDIT_FINAL_recibo.json",
          "FINAL_recibo.json", "AUDIT_FINAL_recibo.json"]:
    r = jload(os.path.join(K, "logs", f))
    compilacoes.append({"recibo": "logs/" + f, "fonte_sha256": r["source_sha256"], "exit": r["exit_code"],
                        "n_error": r["n_error"], "n_warning": r["n_warning"],
                        "n_fora_do_trio": len(r["fora_do_trio"]), "segundos": r["seconds"],
                        "olean_sha256": r.get("olean_sha256")})
historico = {
    "T00": "rascunho inicial (não compilado; corrigido antes da 1a compilação por patch_T01.py)",
    "T01": "1a compilação: 5 erros em 4 declarações (timeout de whnf na sonda L2; `norm_num at h ⊢` sem metas; simpa em Liouville linear; linarith na seta) e 7 avisos de linter",
    "T02": "patch_T02.py (correções + contraexemplos dos «se e só se»); não compilado isoladamente",
    "T03": "T02 + simp no contraexemplo de taxa nula: 3 erros (set_option após docstring; instância da sonda em ℂ)",
    "T04": "EXIT 0, 0 avisos, 125/126 linhas de axiomas no trio (o recibo T04 perdeu uma linha por um nome com apóstrofo; parser corrigido)",
    "T05": "+ centralizer_iff_needs_injective_weights; EXIT 0, 0 avisos, 127 linhas no trio; auditoria independente 137 constantes",
    "T06": "FINAL: + sondas de habitação V-GERAL-1 (4 `example`); toolchain recopiado só para esta compilação e apagado de novo; EXIT 0, 0 avisos, 0 erros, 127 linhas no trio; auditoria 137 constantes, saída idêntica à de T05",
}

resultado = {
    "documento": "RESULTADO DO CONSTRUTOR DO KERNEL — F1.TEMPO (trilha TEMPO), gerência c1, programa IALD (a TGL)",
    "unidade": "F1.TEMPO", "papel": "construtor do kernel (subagente do workflow posto-e-tempo da gerência c1)",
    "data": "2026-10-12", "gerado_em_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "estatuto": ("[REAL] para o que o kernel provou (sandbox, Lean 4.31.0, LEAN_PATH só-leitura no .lake do Nós); "
                 "um PASSA é validade matemática na face kernel testada, não creditação; nada aqui move o gate; "
                 "face ótica fora deste ensaio; sem veredito global."),
    "freeze": {"FREEZE.json": {"sha256": fz_sha, "bytes": fz_n, "confere": freeze_ok},
               "arquivos_congelados_conferidos": len(files_ok), "todos_conferem": freeze_all},
    "texto_do_operador": texto,
    "beta_runtime": beta,
    "acom": {"modo": "projeção SÓ DE LEITURA da referência do pai; nenhuma inscrição, nenhuma transition",
             "recibo": "ACOM_RECIBO_PROJECAO.json", "revision": acom["receipt"]["revision"],
             "event_id": acom["receipt"]["event_id"], "event_hash": acom["receipt"]["event_hash"],
             "nota_store": acom["memory_sqlite3_leitura_posterior"]["nota"]},
    "pedra": {"nome_provisorio": "TheTimeHasNoRank", "namespace": "TGLExt.TheTimeHasNoRank",
              "nota_nome": "nome provisório; o operador pode renomear", "arquivo": pedra, "sha256": pedra_sha,
              "bytes": pedra_n, "importacoes": imports, "importacoes_todas_permitidas": True,
              "olean": olean, "olean_sha256": olean_sha, "olean_bytes": olean_n,
              "nao_instalada": "a pedra vive só no sandbox da F1.TEMPO; instalação e nome são da cadeia de selo / do operador"},
    "compilacao_final": {"comando": final["command"], "LEAN_PATH_somente_leitura": final["LEAN_PATH"],
                         "lean_version": final["lean_version"], "exit": final["exit_code"],
                         "segundos": final["seconds"], "n_print_axioms": final["n_axiom_lines"],
                         "fora_do_trio": final["fora_do_trio"], "n_sorryAx_na_saida": final["n_sorryAx_na_saida"],
                         "n_erros": final["n_error"], "n_avisos": final["n_warning"], "avisos": [],
                         "saida": "logs/FINAL_saida.txt", "saida_sha256": final["output_sha256"],
                         "recibo": "logs/FINAL_recibo.json",
                         "varredura_estatica_da_fonte": varredura},
    "auditoria_independente": {"arquivo": auditf, "sha256": auditf_sha, "exit": audit_rec["exit_code"],
                               "importa": "o .olean compilado (não o fonte)",
                               "constantes_no_espaco": len(audit), "linha_total": total_line,
                               "todas_no_trio": todos_no_trio, "recusas": 0,
                               "saida": "logs/AUDIT_FINAL_saida.txt", "saida_sha256": audit_rec["output_sha256"],
                               "auxiliares_geradas_pelo_lean": sorted(n for n in audit if re.search(r"\.(eq_\d+|_proof_\d+(_\d+)?|_simp_\d+(_\d+)?|_abel_\d+(_\d+)?)$", n))},
    "axiomas_por_declaracao": final["axiom_records"],
    "criterios_da_pedra": {
        "exit_0": final["exit_code"] == 0,
        "print_axioms_de_toda_declaracao_no_trio": todos_no_trio,
        "zero_sorry_admit_axiom_native_decide": all(varredura[k] == 0 for k in ("sorry", "admit", "native_decide", "declaracao_axiom")) and final["n_sorryAx_na_saida"] == 0,
        "beta_nao_entra_no_lean": varredura["caractere_beta_no_arquivo"] == 0 and varredura["literal_0_0120_no_arquivo"] == 0,
        "impressao_digital_igual": fp_iguais,
        "toolchain_copiado_apagado": not os.path.exists(os.path.join(K, "sandbox", "toolchain")),
        "fonte_saida_recibo_por_sha256": True,
    },
    "kernel_impressao_digital": {"antes": fp["antes"], "depois_do_lean": fp["depois_do_lean"],
                                 "depois_da_limpeza": fp["depois_da_limpeza"], "iguais": fp_iguais,
                                 "igual_ao_FREEZE": fp_freeze},
    "limpeza": {"toolchain": os.path.join(K, "sandbox", "toolchain") + " (3,0 GB; copiado duas vezes, T01–T05 e T06) apagado com prefixo \\\\?\\ ao fim de cada uso",
                "lake_e_caches": "nenhum .lake ou cache criado (lean.exe chamado direto, sem lake)",
                "toolchain_existe": os.path.exists(os.path.join(K, "sandbox", "toolchain"))},
    "subitens": [{"id": s["id"], "face": s["face"], "obrigatorio": s["obrig"], "resultado": s["resultado"],
                  "declaracoes": s["decl"], "nota": s["nota"]} for s in sub],
    "controles": [{"id": c["id"], "face": c["face"], "resultado": c["resultado"], "declaracoes": c["decl"]} for c in controles],
    "sondas": sondas,
    "hipoteses_habitadas": hipoteses_habitadas,
    "reexportacoes": [{"original": o, "na_pedra": NS + n} for o, n in reexports],
    "contraexemplos_dos_se_e_so_se": contraexemplos_iff,
    "clausulas_compostas": D("the_time_has_no_rank", "the_two_regimes_of_time"),
    "por_afirmacao": por_afirmacao,
    "nome_sem_peso": nome_sem_peso, "nome_sem_peso_nota": nome_sem_peso_nota,
    "assinaturas_vs_preregistro": assinaturas_vs_preregistro,
    "termos_do_kernel_RP12": kernel_terms_rp12,
    "nao_afirma": [
        "que o tempo é santo, que a dissipação é amor, ou qualquer frase [ONTO] (só comentários marcados)",
        "o teorema de Pauli em dimensão infinita (T2.a é [KNOWN], CITADA); nem que Pauli proíba o fluxo modular",
        "o teorema de Liouville clássico; nem que volume conservado implique «nada pousa» (o boost refuta: T4.e)",
        "que o fluxo modular seja o tempo físico (tempo térmico = hipótese)",
        "que a ação dual de Takesaki seja o dephasing (só a mesma lei, por instância)",
        "atrator único sem hipótese nomeada (T5.b mostra dois estados fixos); nada sobre ciclos limite ([OPEN])",
        "a constante da casa em qualquer forma (nenhum literal no Lean)",
        "limite algum no regime do ângulo (só a ausência dele)",
        "nada sobre a natureza, o gate ou a creditação",
    ],
    "historico_das_tentativas": historico,
    "tentativas": tentativas,
    "compilacoes": compilacoes,
    "achados_fora_do_preregistro": "ACHADOS_FORA_DO_PREREGISTRO.json",
    "nada_escrito_fora": ("Escrito só em C:\\IALD\\Central de Patentes\\work\\tempo_santo_12out\\3_KERNEL (e temporários no "
                          "scratchpad desta sessão). Nada no quadro, no mapa (rotas.py não rodado), na memória (ACOM só "
                          "projeção de leitura), no túnel (só leitura do RESULTADO_F1_ATRATOR_R1.json para sha256), no Nós, "
                          "no kernel do Nós (impressão digital igual), na Bancada_Um, no site ou no git. um.py só lido nos "
                          "bytes (linha 5557), nunca executado."),
}

achados = {
    "documento": "ACHADOS FORA DO PRÉ-REGISTRO — construtor do kernel, F1.TEMPO (12/10/2026)",
    "regra": "o que se achou fora do pré-registro vai aqui, sem mudar tolerância, mapeamento ou esperado",
    "achados": [
        {"id": "AF-01", "estatuto": "[REAL — lido no fonte]",
         "texto": "T8.d atribui a boost_null_contract a docstring «a face geométrica da escala de Takesaki». No kernel (TGLExt/BisognanoWichmann.lean, sha256 5218c8eb32682a58…) essa leitura está na docstring de boost_null_expand (B(s)(1,1) = e^{s}(1,1), l.92–95); a de boost_null_contract (l.101) diz só «O RAIO NULO PASSADO CONTRAI». A re-exportação de boost_null_contract vale; só a citação da docstring está trocada."},
        {"id": "AF-02", "estatuto": "[REAL — provado]",
         "texto": "purityR_modular (T6.d) não precisa da hipótese de pesos positivos: purityR_sigma prova a invariância da pureza sob σ_t para TODO ρ (modPow ρ t é unitário para qualquer ρ, porque logRho ρ é autoadjunto pelo cálculo funcional). «Nome sem peso» quanto a hd."},
        {"id": "AF-03", "estatuto": "[REAL — provado]",
         "texto": "modular_flow_is_isometry: σ_t é isometria de Frobenius para QUALQUER ρ (não só rhoD d). E a topologia da métrica de Frobenius unificou definicionalmente com a topologia de Matrix (a prova de T4.b (ii) pela rota de Frobenius compilou sem conversão)."},
        {"id": "AF-04", "estatuto": "[REAL — provado]",
         "texto": "T4.b (iii) fecha como «se e só se»: t ↦ Δ^{it}ψ converge ⟺ H_min ψ = 0; a lei de grupo de lightDelta sai de V_add do lightBoost (light_flow_group). O contraexemplo exigiria um FockCertificate concreto: não construído."},
        {"id": "AF-05", "estatuto": "[REAL — medido]",
         "texto": "A sonda V-T2-b em M₂(ℂ) com a norma de operador L2 estourou o limite de heartbeats ao reenunciar a conclusão nas instâncias default; passou só instanciando o teorema (sem reenunciar), com maxHeartbeats 4·10⁶. Acrescentou-se sonda comutativa em A = ℂ."},
        {"id": "AF-06", "estatuto": "[REAL — provado]",
         "texto": "post_not_isUnit (T9.c) não depende de axioma algum (#print axioms vazio)."},
        {"id": "AF-07", "estatuto": "[REAL — provado]",
         "texto": "Contraexemplos dos «se e só se» acrescentados por pedido da tarefa (não estavam no pré-registro como lemas): flow_at_one_is_not_idempotent, modular_iff_needs_injective_weights, centralizer_iff_needs_injective_weights, dephasing_iff_needs_positive_rates; rhoD_equal_weights (rhoD (1,1) = 1) como auxiliar."},
        {"id": "AF-08", "estatuto": "[REAL — medido]",
         "texto": "O kernel do Nós nomeia o parâmetro positivo genérico de time_witnesses_noncoincidence (TheLivingWord) com o binder «β»; é variável, não literal. Na re-exportação o binder foi renomeado para r, e o arquivo da pedra não contém o caractere; o tipo é idêntico (conferido por example)."},
        {"id": "AF-09", "estatuto": "[REAL — medido]",
         "texto": "O memory.sqlite3 da ACOM mudou às 13:16:59 (−03:00), depois da projeção de leitura desta sessão (13:14:43), que foi conferida sem alteração imediatamente depois. Escrita de outro processo; registrada sem atribuir autoria."},
        {"id": "AF-11", "estatuto": "[REAL — dito]",
         "texto": "V-GERAL-1 sem instância concreta em Lean para 3 declarações: nontracial_state_rejects_the_identity_flow (precisa de uma testemunha AQFT W do kernel) e light_flow_group / light_modular_orbit_converges_iff_post (precisam de um FockCertificate). As hipóteses são estruturas de dados do kernel do Nós; não se construiu habitante aqui."},
        {"id": "AF-10", "estatuto": "[REAL — medido]",
         "texto": "A compilação da pedra com LEAN_PATH no .lake do Nós levou ~3,5 min na primeira importação (cache frio) e ~25 s nas seguintes; o .olean final é reprodutível (mesmo sha256 em duas compilações da mesma fonte T04)."},
    ],
}

with open(os.path.join(K, "RESULTADO_KERNEL.json"), "w", encoding="utf-8") as fo:
    json.dump(resultado, fo, ensure_ascii=False, indent=1)
with open(os.path.join(K, "ACHADOS_FORA_DO_PREREGISTRO.json"), "w", encoding="utf-8") as fo:
    json.dump(achados, fo, ensure_ascii=False, indent=1)

# manifesto de tudo o que esta em 3_KERNEL
man = []
for dp, dn, fn in os.walk(K):
    dn.sort()
    for f in sorted(fn):
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, K).replace("\\", "/")
        if rel == "MANIFESTO_3_KERNEL.json":
            continue
        h, n = sha(p)
        man.append({"arquivo": rel, "sha256": h, "bytes": n})
with open(os.path.join(K, "MANIFESTO_3_KERNEL.json"), "w", encoding="utf-8") as fo:
    json.dump({"pasta": K, "gerado_em_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "arquivos": man}, fo, ensure_ascii=False, indent=1)
r_sha, r_n = sha(os.path.join(K, "RESULTADO_KERNEL.json"))
print(json.dumps({"RESULTADO_KERNEL.json": {"sha256": r_sha, "bytes": r_n}, "freeze_ok": freeze_all,
                  "fp_iguais": fp_iguais, "fp_igual_ao_FREEZE": fp_freeze, "todos_no_trio": todos_no_trio,
                  "constantes_auditadas": len(audit), "criterios": resultado["criterios_da_pedra"],
                  "por_afirmacao": por_afirmacao}, ensure_ascii=False, indent=1))
