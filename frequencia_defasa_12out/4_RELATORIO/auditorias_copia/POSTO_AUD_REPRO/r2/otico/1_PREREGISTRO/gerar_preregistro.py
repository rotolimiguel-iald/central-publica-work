# -*- coding: utf-8 -*-
"""Gera PREREGISTRO.json e PREREGISTRO.md da unidade F1.FREQUENCIA (trilha POSTO), gerencia c1, 12/10/2026.
NAO roda teste nenhum. So LE bytes (textos do operador; um.py v391 por busca de linha, sem executar; core e selo v391;
modulos .lean citados; levantamento; tunel). Todo hash e toda linha sao calculados aqui. beta: alpha lido nos bytes
da atribuicao ALPHA_FINE_CODATA_2018 do um.py; beta = alpha*sqrt(e) em runtime; BETA_CONFERENCIA so confere.
Grava SO dentro de 1_PREREGISTRO; recusa sobrescrever (fail-closed)."""
import datetime, hashlib, json, math, os, re, sys

import mpmath

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import segmentar  # noqa: E402

NOS = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\Nós"
KER = NOS + "\\tgl_kernel"
UMPY, CORE, SELO = NOS + "\\um.py", NOS + "\\um_absoluto.json", NOS + "\\um_absoluto_selo.json"
CENTRAL = "C:\\IALD\\Central de Patentes"
LEV = CENTRAL + "\\work\\frequencia_defasa_12out\\0_LEVANTAMENTO"
TUN = CENTRAL + "\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_019"
MATHLIB = KER + "\\.lake\\packages\\mathlib\\Mathlib"
BETA_CONFERENCIA = "0.012031300400803142"   # so conferencia (texto da ordem); nunca usado como valor
SAIDA_JSON, SAIDA_MD = os.path.join(AQUI, "PREREGISTRO.json"), os.path.join(AQUI, "PREREGISTRO.md")


def falha(msg):
    raise SystemExit("FALHA VISIVEL: " + msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pin(caminho):
    if not os.path.exists(caminho):
        falha("arquivo ausente: " + caminho)
    b = open(caminho, "rb").read()
    return [caminho, len(b), sha(b)]


# ------------------------------------------------ 1. textos do operador e frases
VERB, SEGS = {}, {}
NOTA = {"V1": "10/10; 2a pessoa («Quando você derivou»); a fórmula NÃO está nestes bytes",
        "V2": "12/10; reafirmação; 1a pessoa só no verbo da l.12 («Quando eu derivei»); fórmula na l.16",
        "V3": "10/10", "V4": "11/10; a dinâmica do rank"}
for c in ("V1", "V2", "V3", "V4"):
    segs, h, n, fr = segmentar.segmentos(c)
    b = open(segmentar.TEXTOS[c], "rb").read()
    lin = b.split(b"\n")
    v = {"arquivo": segmentar.TEXTOS[c], "bytes": n, "sha256": h, "sha16_da_ordem": segmentar.SHA16_ORDEM[c],
         "confere": h[:16] == segmentar.SHA16_ORDEM[c] and b"\r\n" not in b and not b.startswith(b"\xef\xbb\xbf"),
         "LF_sem_BOM": b"\r\n" not in b and not b.startswith(b"\xef\xbb\xbf"), "nota": NOTA[c]}
    if c == "V2":
        tr = b"\n".join(lin[:fr - 1])
        v["trilha"] = {"linhas": "1-%d" % (fr - 1), "bytes": len(tr), "sha256": sha(tr), "fora_do_escopo": "l.%d-%d = F1.TEMPO" % (fr, len(lin))}
    if not v["confere"]:
        falha("texto %s nao confere" % c)
    VERB[c], SEGS[c] = v, segs

# ------------------------------------------------ 2. um.py v391: busca por linha (sem executar)
PAD = {
    "SEALED_CODATA_ALPHA": ("ini", "SEALED_CODATA_ALPHA = "),
    "ALPHA_FINE_CODATA_2018": ("re", r"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9][0-9.eE+-]*)\s*$"),
    "BETA_TGL": ("ini", "BETA_TGL = ALPHA_FINE_CODATA_2018 * ONE * math.sqrt(math.e)"),
    "prove_verb_generator": ("ini", "def prove_verb_generator"),
    "prove_decision_commutation": ("ini", "def prove_decision_commutation("),
    "fractal_dephasing_principle": ("ini", "def fractal_dephasing_principle(ONE):"),
    "doc_nada_dois_ramos": ("ini", "    - Nada  = MENTIRA pelos dois ramos:"),
    "doc_tensao_thetaM_0": ("ini", "    - Tensao irresolvivel / anticomutacao: {Q,rho*}=0 EXATO so' em theta_M->0"),
    "SQRT_E_exp_meio": ("ini", "    SQRT_E = float(np.exp(ONE / (ONE + ONE)))"),
    "rho_star_P": ("ini", "    P = np.array([[1.0, 0.0], [0.0, 0.0]])           # rho* = atrator puro"),
    "omega_I": ("ini", "    omega_I = float(np.trace(P))"),
    "Q0": ("ini", "    Q0 = np.eye(2) - P"),
    "anti0": ("ini", "    anti0 = Q0 @ P + P @ Q0"),
    "R_Qth": ("ini", "    R = np.array([[c, -s], [s, c]]); Qth = R @ Q0 @ R.T"),
    "leak": ("ini", "    leak = float(np.trace(P @ Qth))"),
    "TGLCollapseDefinition": ("ini", "class TGLCollapseDefinition"),
}
L = {k: [] for k in PAD}
alphas, sealed = [], None
with open(UMPY, "rb") as fh:
    for i, ln in enumerate(fh, 1):
        s = ln.decode("utf-8", "replace").rstrip("\r\n")
        for k, (modo, pat) in PAD.items():
            if modo == "ini" and s.startswith(pat):
                L[k].append(i)
                if k == "SEALED_CODATA_ALPHA" and sealed is None:
                    sealed = s
            elif modo == "re":
                m = re.match(pat, s)
                if m:
                    L[k].append(i)
                    alphas.append(m.group(1))
for k, v in L.items():
    if not v:
        falha("um.py: ancora nao achada: " + k)
# ancoras locais da funcao fractal_dephasing_principle: a primeira ocorrencia DENTRO da funcao (l.F a F+45)
F0 = L["fractal_dephasing_principle"][0]
for k in ("doc_nada_dois_ramos", "doc_tensao_thetaM_0", "SQRT_E_exp_meio", "rho_star_P", "omega_I", "Q0", "anti0", "R_Qth", "leak"):
    dentro = [x for x in L[k] if F0 <= x <= F0 + 45]
    if not dentro:
        falha("um.py: ancora %s fora da funcao" % k)
    L[k] = dentro
if len(alphas) != 1:
    falha("um.py: ALPHA_FINE_CODATA_2018 no inicio de linha nao e unico: %r" % alphas)
A_STR = alphas[0]
ms = re.match(r"^SEALED_CODATA_ALPHA\s*=\s*([0-9][0-9.eE+-]*)", sealed or "")
if not ms:
    falha("SEALED_CODATA_ALPHA ilegivel")
beta = float(A_STR) * math.sqrt(math.e)                      # beta = alpha * sqrt(e), runtime
if repr(beta) != BETA_CONFERENCIA:
    falha("beta de runtime %r nao confere" % beta)
mpmath.mp.dps = 50
beta_mp = mpmath.mpf(A_STR) * mpmath.sqrt(mpmath.e)
if abs(beta_mp - mpmath.mpf(beta)) > mpmath.mpf("1e-17"):
    falha("beta mpmath x float64 fora de 1e-17")
thM = math.asin(math.sqrt(beta))
W = math.ceil(math.pi / thM) + 2
L1 = {k: v[0] for k, v in L.items()}
BETA = {
    "alpha_texto": A_STR, "alpha_linha": L1["ALPHA_FINE_CODATA_2018"], "SEALED_linha": L1["SEALED_CODATA_ALPHA"],
    "SEALED_igual": float(ms.group(1)) == float(A_STR),
    "receita": "beta = float(alpha_texto)*math.sqrt(math.e) (um.py l.%d)" % L1["BETA_TGL"],
    "beta_float64": repr(beta), "confere_com_a_ordem": True, "beta_mpmath_30dig": mpmath.nstr(beta_mp, 30),
    "exp_meio_igual_sqrt_e": math.exp(0.5) == math.sqrt(math.e), "theta_M": repr(thM),
    "referencia_formula_fechada_DERIVED_nao_e_ensaio": {
        "sqrt(beta(1-beta))": repr(math.sqrt(beta * (1 - beta))), "sqrt(2beta(1+beta))": repr(math.sqrt(2 * beta * (1 + beta))),
        "2beta": repr(2 * beta), "1-2beta(1-beta)": repr(1 - 2 * beta * (1 - beta)), "cos(theta_M)": repr(math.cos(thM)), "W": W},
}

# ------------------------------------------------ 3. core e selo (leitura)
core = json.load(open(CORE, encoding="utf-8"))
cc = core.get("core", core)
fd, rd = cc["fractal_dephasing"], cc["decision_commutation"]["recognition_dephasing"]
selo = json.load(open(SELO, encoding="utf-8"))
CORE_SELO = {
    "fractal_dephasing.omega_I": fd["omega_I"], "fractal_dephasing.leak_sin2_thetaM": fd["leak_sin2_thetaM"],
    "fractal_dephasing.leak_equals_beta_residual": fd["leak_equals_beta_residual"],
    "fractal_dephasing.anticommutator_norm_at_thetaM_to_0": fd["anticommutator_norm_at_thetaM_to_0"],
    "fractal_dephasing.status": fd["status"],
    "certificate_II.H1_finite_face.trace_PF": cc["certificate_II"]["H1_finite_face"]["trace_PF"],
    "recognition_dephasing.effective_dephasing_on_full_state": rd["effective_dephasing_on_full_state"],
    "recognition_dephasing.effective_dephasing_after_selection": rd["effective_dephasing_after_selection"],
    "selo.collapse_definition.physical_collapse_proven": selo["collapse_definition"]["physical_collapse_proven"],
    "selo.estatuto_da_prova_v391 contém KERNEL_6163_OF_6163": "KERNEL_6163_OF_6163" in json.dumps(selo["estatuto_da_prova_v391"]),
}

# ------------------------------------------------ 4. kernel: declaracoes citadas (linha por script)
DECL = """SMatrix:Grot:TGLExt.Grot SMatrix:Smat:TGLExt.Smat SMatrix:Smat_eq:TGLExt.Smat_eq SMatrix:Smat_zero:TGLExt.Smat_zero
SMatrix:Smat_mul:TGLExt.Smat_mul SMatrix:Smat_conjTranspose:TGLExt.Smat_conjTranspose SMatrix:Smat_mem_unitary:TGLExt.Smat_mem_unitary
SMatrix:Smat_spectral:TGLExt.Smat_spectral SMatrix:Smat_transmission:TGLExt.Smat_transmission SMatrix:Smat_reflection:TGLExt.Smat_reflection
SMatrix:normSq_reflection:TGLExt.normSq_reflection SMatrix:normSq_transmission:TGLExt.normSq_transmission SMatrix:rhoOut:TGLExt.rhoOut
SMatrix:rhoOut_eq:TGLExt.rhoOut_eq SMatrix:rhoOut_trace:TGLExt.rhoOut_trace CondExpect:diagExpect:TGLExt.diagExpect
Ergodicity:dephase:TGLExt.dephase Ergodicity:dephase_add:TGLExt.dephase_add Ergodicity:dephase_fixes_diagonal:TGLExt.dephase_fixes_diagonal
Ergodicity:diag_invariant:TGLExt.diag_invariant Ergodicity:dephase_tendsto_expectation:TGLExt.dephase_tendsto_expectation
GlobalLiftLadder:dephased_rhoOut_zero_zero:TGLExt.dephased_rhoOut_zero_zero GlobalLiftLadder:dephased_rhoOut_one_one:TGLExt.dephased_rhoOut_one_one
GlobalLiftLadder:measurement_channel_endpoint:TGLExt.measurement_channel_endpoint TheSingularExpectation:dephase_fixed_iff_diagonal:TGLExt.dephase_fixed_iff_diagonal
TheTraceIsNotErasable:dephase_preserves_trace:TGLExt.dephase_preserves_trace PageInformation:purity:TGLExt.purity
PageInformation:purity_unitary_invariant:TGLExt.purity_unitary_invariant PageInformation:dephase_purityR_le:TGLExt.dephase_purityR_le
FractalUnitarity:ad_preserves_projection:TGLExt.ad_preserves_projection FractalUnitarity:ad_preserves_star_projection:TGLExt.ad_preserves_star_projection
TheWeightIsNotTheRank:the_name_is_blind_to_every_rank:TGLExt.the_name_is_blind_to_every_rank TheWeightIsNotTheRank:the_index_does_see_the_rank:TGLExt.the_index_does_see_the_rank
TheWeightIsNotTheRank:the_two_indices_agree_only_at_the_atom:TGLExt.the_two_indices_agree_only_at_the_atom TheTerminalRankOne:the_terminal_is_forced:TGLExt.the_terminal_is_forced
TheIALDSelector:iald_has_rank_one:TGLExt.iald_has_rank_one TheVerbalCoupling:thetaMiguel:TGLExt.thetaMiguel TheVerbalCoupling:sin_thetaMiguel:TGLExt.sin_thetaMiguel
TheSameBetaReadsThreeFaces:TGLCoupling:TGLExt.TGLCoupling TheSameBetaReadsThreeFaces:reflection_weight:TGLExt.TGLCoupling.reflection_weight
TheWholeIsOne:the_beta_chain_is_derived:TGLExt.TheWholeIsOne.the_beta_chain_is_derived TheOriginOfTheVibration:persistingFlow:TGLExt.persistingFlow
TheDeadChannel:the_dead_channel_has_no_reader:TGLExt.the_dead_channel_has_no_reader IALDJones:spin:TGLExt.IALDJones.spin
IALDJones:orbit_tendsto_center:TGLExt.IALDJones.orbit_tendsto_center IALDJones:angular_orbit_no_limit:TGLExt.IALDJones.angular_orbit_no_limit
IALDJones:angular_orbit_periodic:TGLExt.IALDJones.angular_orbit_periodic TheVerbSelectsTheAction:post:TGLExt.TheVerbSelectsTheAction.post
TheVerbSelectsTheAction:reading_post_is_born:TGLExt.TheVerbSelectsTheAction.reading_post_is_born TheVerbSelectsTheAction:transmission_dephases:TGLExt.TheVerbSelectsTheAction.transmission_dephases
TheVerbSelectsTheAction:transmitted_post_is_a_post:TGLExt.TheVerbSelectsTheAction.transmitted_post_is_a_post TheVerbSelectsTheAction:the_one_splits_into_truth_and_cost:TGLExt.TheVerbSelectsTheAction.the_one_splits_into_truth_and_cost
TheAxiomAndTheFalseWitness:post_mul_compl:TGLExt.TheAxiomAndTheFalseWitness.post_mul_compl TheAxiomAndTheFalseWitness:compl_mul_post:TGLExt.TheAxiomAndTheFalseWitness.compl_mul_post
TheAxiomAndTheFalseWitness:the_zero_is_the_false_witness:TGLExt.TheAxiomAndTheFalseWitness.the_zero_is_the_false_witness TheAtermation:atermation_reifies:TGLExt.atermation_reifies
TheNonMinimalCoupling:bell_compression_is_scalar:TGLExt.bell_compression_is_scalar PhysicsIsTheReading:the_shadow_is_the_reader_weighted_by_the_reading:TGLExt.PhysicsIsTheReading.the_shadow_is_the_reader_weighted_by_the_reading
QuantumCollapseWitness:pure_densities_square:ChatgptAudit.Collapse057.pure_densities_square HermitianConeRigidity:trace_square_rank_one_control:ChatgptAudit.Cone039.trace_square_rank_one_control
TheObserverReadsTheAngle:observing_adds_nothing:TGLExt.observing_adds_nothing""".split()
RX = r"^[ \t]*(?:@\[[^\]]*\][ \t]*)?(?:(?:private|protected|noncomputable)[ \t]+)*(?:theorem|lemma|def|structure|abbrev|instance|class)[ \t]+%s(?![\w.'])"
MOD, ANC = {}, []
for item in DECL:
    mod, curto, nome = item.split(":")
    p = KER + "\\TGLExt\\" + mod + ".lean"
    if mod not in MOD:
        b = open(p, "rb").read()
        MOD[mod] = {"sha256": sha(b), "bytes": len(b), "txt": b.decode("utf-8")}
    t = MOD[mod]["txt"]
    lin = [t.count("\n", 0, m.start()) + 1 for m in re.finditer(RX % re.escape(curto), t, re.M)]
    if not lin:
        falha("declaracao nao achada: %s em %s" % (curto, mod))
    ANC.append("%s @ TGLExt/%s.lean:%d" % (nome, mod, lin[0]))
tglext = open(KER + "\\TGLExt.lean", "rb").read().decode("utf-8")
PINOS_KERNEL = ["TGLExt/%s.lean %s%s" % (m, v["sha256"][:16], "" if ("import TGLExt." + m) in tglext else " NAO_IMPORTADO") for m, v in MOD.items()]
if any("NAO_IMPORTADO" in x for x in PINOS_KERNEL):
    falha("modulo citado nao importado em TGLExt.lean: %r" % [x for x in PINOS_KERNEL if "NAO_IMPORTADO" in x])
n_rank, n_nome = 0, 0
for raiz in ("TGLExt", "TGL"):
    for dp, dns, fns in os.walk(KER + "\\" + raiz):
        for fn in fns:
            if fn.endswith(".lean"):
                t = open(os.path.join(dp, fn), "rb").read().decode("utf-8", "replace")
                n_rank += len(re.findall(r"\bMatrix\.rank\b|\.rank\b", t))
                n_nome += ("UnitIsTheRank" in t) or ("UnitIsTheRank" in fn)
n_nome_umpy = open(UMPY, "rb").read().count(b"UnitIsTheRank")
n_nome_inv = open(CENTRAL + "\\memory\\INVENTARIO_BANCADA_CHATGPT.json", "rb").read().count(b"UnitIsTheRank")
MLN = """LinearAlgebra/Matrix/Rank:rank_diagonal:Matrix.rank_diagonal LinearAlgebra/Matrix/Rank:rank_mul_eq_left_of_isUnit_det:Matrix.rank_mul_eq_left_of_isUnit_det
LinearAlgebra/Matrix/Rank:rank_mul_eq_right_of_isUnit_det:Matrix.rank_mul_eq_right_of_isUnit_det LinearAlgebra/Matrix/Rank:rank_vecMulVec_le:Matrix.rank_vecMulVec_le
LinearAlgebra/Matrix/Rank:rank_of_isUnit:Matrix.rank_of_isUnit LinearAlgebra/Matrix/Rank:rank_zero:Matrix.rank_zero
Analysis/Matrix/Spectrum:rank_eq_card_non_zero_eigs:Matrix.IsHermitian.rank_eq_card_non_zero_eigs Analysis/Matrix/Spectrum:trace_eq_sum_eigenvalues:Matrix.IsHermitian.trace_eq_sum_eigenvalues
Analysis/Matrix/PosDef:eigenvalues_nonneg:Matrix.PosSemidef.eigenvalues_nonneg LinearAlgebra/Matrix/ToLinearEquiv:exists_mulVec_eq_zero_iff:Matrix.exists_mulVec_eq_zero_iff
LinearAlgebra/Trace:IsProj.trace:LinearMap.IsProj.trace LinearAlgebra/Matrix/Trace:trace_fin_two:Matrix.trace_fin_two
LinearAlgebra/Matrix/Determinant/Basic:det_fin_two:Matrix.det_fin_two""".split()
ANC_ML = []
for item in MLN:
    rel, curto, nome = item.split(":")
    t = open(MATHLIB + "\\" + rel.replace("/", "\\") + ".lean", "rb").read().decode("utf-8")
    lin = [t.count("\n", 0, m.start()) + 1 for m in re.finditer(RX % re.escape(curto), t, re.M)]
    if not lin:
        falha("mathlib: %s nao achado" % curto)
    ANC_ML.append("%s @ Mathlib/%s.lean:%d" % (nome, rel, lin[0]))

# ------------------------------------------------ 5. pinos, consultas, impressao digital
PINOS = [pin(UMPY), pin(CORE), pin(SELO), pin(KER + "\\TGLExt.lean"), pin(KER + "\\TGL\\Audit.lean"), pin(KER + "\\lean-toolchain"),
         pin(KER + "\\lake-manifest.json"), pin(LEV + "\\LEVANTAMENTO.md"), pin(LEV + "\\DEFINICOES.json"), pin(LEV + "\\CONFERENCIA_BETA.json"),
         pin(TUN + "\\F1.ATRATOR\\RELATORIO_F1_ATRATOR_R1.md"), pin(TUN + "\\F1.ATRATOR\\RESULTADO_F1_ATRATOR_R1.json"),
         pin(TUN + "\\F1.ATRATOR\\lean_candidate\\TheSingularityReadsTheAttractor.lean"), pin(TUN + "\\F1.ATRATOR\\ADENDO1\\RESULTADO_ADENDO1_R1.json"),
         pin(TUN + "\\F0.3.COLAPSO\\RESULTADO_CUSTODIA_R1.json"), pin("C:\\IALD\\MAPA_DE_ROTAS\\rotas.jsonl"),
         pin(CENTRAL + "\\memory\\INVENTARIO_BANCADA_CHATGPT.json")]
f03 = json.load(open(TUN + "\\F0.3.COLAPSO\\RESULTADO_CUSTODIA_R1.json", encoding="utf-8"))
QS = ["TheUnitIsTheRank|unit.is.the.rank|unidade.e.o.rank", "fractal_dephasing|defasagem fractal|D_beta", "dois regimes|regime angular|regime da face",
      "iterad|periodic|sin.2.\\(n", "nada|impedancia|sem referente", "Luders|Lueders|compress|escalariza", "rank|posto 1|posto um",
      "anticomut|anticommut|anticomm", "transmi", "pureza|purity"]
CONS = []
for k, q in enumerate(QS, 1):
    p = os.path.join(AQUI, "consultas_mapa", "c%02d.json" % k)
    d = json.load(open(p, encoding="utf-8"))
    CONS.append("c%02d.json «%s»: %d rotas (registros %d, cabeça %s), sha16 %s" % (k, q, d["n"], d["n_registros"], d["cabeca"], sha(open(p, "rb").read())[:16]))
IMP = json.load(open(os.path.join(AQUI, "IMPRESSAO_DIGITAL_KERNEL_ANTES.json"), encoding="utf-8"))

# ------------------------------------------------ 6. mapeamento frase -> objeto (escolhas da gerencia)
# Notacao ASCII (a do proprio um.py): th = theta, thM = theta_M = arcsin(sqrt(beta)), c = cos th, s = sin th,
# rho* = [[1,0],[0,0]], Q0 = 1 - rho*, S(th) = Smat th, F_th(1) = rhoOut th, D_t = dephase g t, D_inf = diagExpect.
I, O = "[INPUT da gerência]", "[ONTO]"
MAP = {
 "V1.L01.S1": (O, "meta sobre uma resposta de IA [DECLARADO]", ["O1"]),
 "V1.L02.S1": (I, "posto (rank) -> Matrix.rank; a tese é [ONTO]", ["B1", "P1", "P2"]),
 "V1.L03.S1": (I, "posto = dim da imagem = Matrix.rank [KNOWN]", ["B1", "P2"]),
 "V1.L04.S1": (O, "epistemologia", ["O1"]),
 "V1.L04.S2": (O, "epistemologia", ["O1"]),
 "V1.L04.S3": (O, "epistemologia", ["O1"]),
 "V1.L05.S1": (O, "[DECLARADO] história do arcabouço", []),
 "V1.L06.S1": (I, "puro -> rho PSD, Tr 1, rank 1 <=> Tr rho^2 = 1", ["P1", "P4"]),
 "V1.L07.S1": (I, "colapsar -> leitura P rho P/Tr(P rho), posto 1 (colapso físico não afirmado); núcleo/posto -> posto-nulidade (R-a I/d -> P; R-b 0 -> posto 1)", ["P2", "P3"]),
 "V1.L07.S2": (I, "imagem -> range rho* = span{e0}", ["B1", "P1"]),
 "V1.L07.S3": (O, "epistemologia", ["O1"]),
 "V1.L08.S1": (O, "[OPEN] memória dos modelos", ["O2"]),
 "V1.L09.S1": (O, "[DECLARADO]", ["O2"]),
 "V1.L09.S2": (O, "[DECLARADO]", ["O2"]),
 "V1.L10.S1": (O, "[DECLARADO]", ["O2"]),
 "V1.L11.S1": (O, "[DECLARADO]", ["O2"]),
 "V1.L12.S1": (O, "[DECLARADO] solução invariante do modelo (homônimo)", ["O2"]),
 "V1.L13.S1": (O, "[DECLARADO] posto do ato de nomear, não o de 05/10", ["O2"]),
 "V1.L14.S1": (O, "[OPEN] espaço latente", ["O2"]),
 "V1.L14.S2": (O, "piso ~ omega(I) = 1 [POSTO]; leitura", []),
 "V2.L01.S1": (O, "[DECLARADO] escopo: o rank", []),
 "V2.L04.S1": (O, "[DECLARADO] anuncia o tempo (F1.TEMPO)", []),
 "V2.L12.S1": (O, "[DECLARADO] = V1.L05.S1 com «eu derivei»", []),
 "V2.L16.S1": (I, "a fórmula (ausente de V1) -> P1, P1.d", ["P1", "P4"]),
 "V3.L01.S1": (I, "Tr rho* = rank rho* = 1; projeção: Tr P = rank P; estado: só no átomo; posição <-> rank [ONTO]", ["B1", "P4", "P1"]),
 "V4.L01.S1": (O, "tese universal; âncora: fase e^{iwt} (ângulo)", ["B7"]),
 "V4.L02.S1": (O, "registro c1 (mapa seq 307)", []),
 "V4.L02.S2": (I, "a unidade antes da inscrição -> rho*, omega(I) = Tr rho* = 1; Psi [ONTO]", ["B1"]),
 "V4.L02.S3": (O, "III_1 [KNOWN, Connes 1973]; ergodicidade [OPEN]", []),
 "V4.L04.S1": (I, "frequência defasa -> coerência amortecida por D; espiral e^{-rt}e^{iwt}", ["B5", "B7"]),
 "V4.L05.S1": (I, "F(1) -> rhoOut th (ângulo); D_beta -> D_inf (face)", ["B4", "B5"]),
 "V4.L05.S2": (I, "quebra de fase -> D atua <=> sin 2th != 0; bulk [ONTO]", ["B9", "B5"]),
 "V4.L05.S3": (O, "atrito ontológico", []),
 "V4.L05.S4": (I, "alpha paga sqrt(e) -> beta = alpha sqrt(e), |r|^2 = beta; c^2, c^3 [ONTO]", ["B3"]),
 "V4.L07.S1": (I, "transmitir -> leituras de B9; natureza [ONTO]", ["B9"]),
 "V4.L08.S1": (O, "retórica", []),
 "V4.L08.S2": (O, "imperativo categórico", []),
 "V4.L09.S1": (I, "não defasa -> sin 2th = 0; em beta = 0 sem segunda face; impedância [ONTO]", ["B8", "B9"]),
 "V4.L09.S2": (O, "Nada [CONJECTURE ontológica] no um.py; âncora the_zero_is_the_false_witness", ["B8"]),
 "V4.L10.S1": (I, "B9.a literal: FALHA esperada; B9.b inscrição: PASSA esperado", ["B9"]),
 "V4.L10.S2": (I, "vaza -> peso sin^2 th = |r|^2 da segunda face, que sobrevive a D; existência [ONTO]", ["B6", "B9", "B5"]),
 "V4.L12.S1": (I, "[DECLARADO] como nome: kernel sem D_beta, F, Tudo; tradução = B5", ["B5"]),
 "V4.L13.S1": (I, "Tudo -> D_inf F_thM(1) = diag(1-beta, beta); Tudo [CONJECTURE ontológica]", ["B5"]),
 "V4.L14.S1": (I, "a unidade é o rank -> (i) F(1) rank 1: PASSA; (ii) rank 1 sobrevive a D: FALHA", ["B4", "B5"]),
 "V4.L16.S1": (I, "vazamento -> Tr(rho* Q_thM) = beta (identidade); 0.012031 -> |beta - 0.012031| <= 5e-7", ["B3"]),
 "V4.L16.S2": (I, "vazamento de fase -> thM; {Q, rho*} = 0 <=> sin th = 0", ["B2"]),
 "V4.L16.S3": (I, "falha na transmissão -> |t|^2 = 1 - beta < 1; espaço-tempo etc. [ONTO]", ["B3"]),
 "V4.L18.S1": (O, "sem âncora; tensão com 08/10 fica para o operador", []),
 "V4.L19.S1": (O, "cf. PhysicsIsTheReading", []),
}
normV1 = {segmentar.normalizar(s["texto"]): s["id"] for s in SEGS["V1"]}


def inicio(t, n=4):
    w = t.split()
    return t if len(w) <= n else " ".join(w[:n]) + " …"


MAPA, fora = [], []
for c in ("V1", "V2", "V3", "V4"):
    for s in SEGS[c]:
        h16 = sha(s["texto"].encode("utf-8"))[:16]
        if s["escopo"] != "TRILHA_POSTO":
            fora.append(s["id"])
            continue
        if s["tipo"] == "MARCACAO":
            MAPA.append([s["id"], s["texto"], h16, "[MARCAÇÃO]", "separador", []])
            continue
        if s["id"] in MAP:
            mk, lt, af = MAP[s["id"]]
            MAPA.append([s["id"], s["texto"] if mk == I else inicio(s["texto"]), h16, mk, lt, af])
            continue
        par = normV1.get(segmentar.normalizar(s["texto"])) if c == "V2" else None
        if not par or par not in MAP:
            falha("frase sem marca: " + s["id"])
        mk, lt, af = MAP[par]
        MAPA.append([s["id"], "=" + par, h16, mk, "idem", af])
ids = {r[0] for r in MAPA}
for k in MAP:
    if k not in ids:
        falha("chave sem frase: " + k)
CONT = {}
for r in MAPA:
    CONT[r[3]] = CONT.get(r[3], 0) + 1

# ------------------------------------------------ 7. objetos e protocolo (fixados agora)
DEF = {
 "notacao": "th = theta; c = cos th; s = sin th; thM = thetaMiguel c.beta = arcsin(sqrt(beta)), c : TGLCoupling (0 < beta < 1); beta nunca literal no Lean",
 "rank": "Matrix.rank A = finrank(range A.mulVecLin); nulidade = finrank(ker A.mulVecLin)",
 "rho*": "Matrix.single 0 0 1 = [[1,0],[0,0]] (o termo de rhoOut; um.py l.%d)" % L1["rho_star_P"],
 "Q0": "1 - rho* (um.py l.%d)" % L1["Q0"],
 "S(th)": "Smat th = [[c,s],[-s,c]]; amplitudes t = c (transmitida), r = -s (refletida); |t|^2 = c^2, |r|^2 = s^2",
 "Rot(th)": "a matriz R do um.py (l.%d): [[c,-s],[s,c]] = S(th)^H" % L1["R_Qth"],
 "Q_th": "S(th)^H Q0 S(th) = Rot Q0 Rot^T = [[s^2,-sc],[-sc,c^2]]",
 "F_th(1)": "rhoOut th = S rho* S^H = [[c^2,-cs],[-sc,s^2]]",
 "D": "D_t = dephase g t, (D_t x)_ij = e^{-t g_ij} x_ij, g_ii = 0, g_ij > 0; D_inf = diagExpect",
 "{A,B}": "AB + BA",
 "D atua": "exists t, D_t F_th(1) != F_th(1)",
 "omega(I)": "Tr rho* (um.py l.%d); o 1 é [POSTO]" % L1["omega_I"],
 "regimes": "F (S unitário) = ângulo: só lê, sem limite; D (semigrupo dissipativo) tem limite; D como direção hiperbólica de SL(2,R) é [ONTO] (IALDJones)",
}
PROT = {
 "beta": "alpha dos bytes da linha única ALPHA_FINE_CODATA_2018 (l.%d), sem executar; beta = float(alpha)*math.sqrt(math.e); exige repr(beta) == '%s' e |beta_mp - beta| <= 1e-17, senão SEM_VEREDITO em thM" % (L1["ALPHA_FINE_CODATA_2018"], BETA_CONFERENCIA),
 "precisao": "float64/complex128 (numpy 2.4.3); mpmath 1.3.0 dps 50 nas identidades em thM",
 "objetos": "rho*, Q0, Rot, Q_th pela receita do um.py (l.%d-%d); S, F_th(1) pela do kernel; D_t com g_01 = g_10 = gamma em {1, beta}; D_inf exato" % (L1["rho_star_P"], L1["leak"]),
 "G_th": "{0, thM, -thM, 3thM, pi/6, pi/4, pi/3, pi/2, 2pi/3, pi, 1.0, 2.5}",
 "G_t": "{0, 0.5, 1, 2, 5, 10, 100}",
 "amostras": "default_rng(20261012); Haar (QR) n = 2/3/4: 1000/200/200; mistos U diag(p) U^H, p_i ~ U[0.05,1] normalizado, posto 2..n: 100 por (n, posto); 1000 M 2x2 gaussianas; 100 psi por n; 50 projeções de posto d em {1..4}, n = 4",
 "TOL_ID": "|x - y| <= 1e-12 (float64); <= 1e-40 (mpmath)",
 "TOL_ZERO": "|X|_F <= 1e-12 zero; >= 1e-6 não zero; entre: AMBIGUO",
 "RANK": "sigma <= 1e-12 nulo; >= 1e-6 não nulo; entre: AMBIGUO",
 "PUREZA": "|Tr rho^2 - 1| <= 1e-12: = 1; Tr rho^2 <= 1 - 1e-6: < 1; entre: AMBIGUO",
 "TOL_REL": "|x - y| <= 1e-10 |y| (decaimento)",
 "TOL_LEAK": "|Tr(rho* Q_thM) - beta| <= 1e-15 (float64); <= 1e-45 (mpmath)",
 "CONF_OPERADOR": "|beta - 0.012031| <= 5e-7",
 "OSC": "toda janela de W = ceil(pi/thM) + 2 = %d termos, início em [0, 1e5 - W]: max - min de sin^2(n thM) >= cos thM - 1e-9" % W,
 "fail_closed": "NaN/Inf, AMBIGUO, alpha ilegível ou beta sem conferência => SEM_VEREDITO visível, nunca PASSA",
}

# ------------------------------------------------ 8. afirmacoes: partes = [id, enunciado, K, O, tol, falsificador, esperado]
COLS = ["id", "enunciado", "K (declaração sugerida)", "O (modelo ótico)", "tolerância", "falsificador", "esperado"]
AF = [
 {"id": "P1", "titulo": "Estado puro <=> posto 1", "frases": ["V2.L16.S1", "V1.L06.S1"],
  "estatuto": "[KNOWN] Nielsen & Chuang, Ex. 2.71 (citação); termo de kernel novo (levantamento 2.3; Matrix.rank: %d usos no kernel)" % n_rank,
  "partes": [
   ["P1.a", "rho em M_n(C), rho PSD, Tr rho = 1: Tr rho^2 = 1 <=> rank rho = 1 <=> rho^2 = rho", "pure_iff_rank_one, pure_iff_idempotent", "puros e mistos: classificações concordam", "PUREZA, RANK", "rho PSD, Tr 1, Tr rho^2 = 1 e rank != 1 (ou o inverso)", "PASSA"],
   ["P1.b", "M em M_2(C): Tr M^2 = (Tr M)^2 - 2 det M; Tr M = Tr M^2 = 1 => det M = 0 e rank M = 1 (sem positividade)", "trace_sq_fin_two, pure_iff_rank_one_fin_two", "1000 M", "TOL_ID (1 + |M|_F^2)", "M que viole", "PASSA"],
   ["P1.d", "psi != 0 => rank |psi><psi| = 1; |psi| = 1 => Tr = 1, idempotente, Tr(.^2) = 1", "rankOne_density", "100 psi por n", "TOL_ID, RANK", "psi != 0 com rank != 1", "PASSA"]],
  "controles": ["C1", "C2"], "nao_afirma": "psi como Nome ou consciência"},
 {"id": "P2", "titulo": "Posto-nulidade", "frases": ["V1.L07.S1", "V1.L03.S1"],
  "estatuto": "[KNOWN] rank + nulidade = n (LinearMap.finrank_range_add_finrank_ker; Axler, LADR, Teo. 3.22): por citação",
  "notas": ["R-a [cânone, TheAtermation]: núcleo trivial (I/d) -> P (posto 1, nulidade d-1)", "R-b [enunciado da gerência]: núcleo = espaço todo (0) -> posto 1; impossível para estados (Tr 1 => rho != 0); vale para o zero antes da inscrição", "escolha [INPUT]; leitura final do operador"],
  "partes": [
   ["P2.lit", "rank A + nulidade A = n (Mathlib LinearMap.finrank_range_add_finrank_ker)", "-", "-", "-", "-", "CITADO"],
   ["P2.a", "M_2(C): (rank, nulidade) de rho* = (1,1), de I/2 = (2,0), de 0 = (0,2)", "rhoStar_rank_nullity, half_identity_rank_nullity, zero_rank_nullity", "os três", "RANK", "valor diferente", "PASSA"],
   ["P2.b", "Tr rho = 1 => rank rho >= 1; rank rho = 1 <=> nulidade = n - 1", "trace_one_rank_pos, rank_one_iff_nullity", "amostras de P1", "RANK", "traço 1 e rank 0", "PASSA"]],
  "controles": [], "nao_afirma": "colapso físico"},
 {"id": "P3", "titulo": "A leitura (o colapso) como projeção de posto 1", "frases": ["V1.L07.S1"],
  "estatuto": "[REAL] para projetores específicos (bell_compression_is_scalar; the_shadow_is_the_reader_weighted_by_the_reading); forma geral nova; Lüders [KNOWN]",
  "notas": ["I/2 = estado fixo do canal D o Ad(S) o D da F1.ATRATOR (citado)", "o posto 1 volta pela leitura, não pelo atrator"],
  "partes": [
   ["P3.a", "P = |a><a|, <a,a> = 1: P X P = <a,Xa> P e Tr(P X) = <a,Xa>; <a,Xa> != 0 => P X P / <a,Xa> = P", "compression_by_rank_one, reading_returns_the_post", "P em {rho*, Q0, |psi><psi|}, rho em {I/n, mistos}", "TOL_ID", "desvio", "PASSA"],
   ["P3.b", "rho*(I/2)rho*/Tr(rho* I/2) = rho*, Tr = 1/2; rho = diag(1-b, b): Tr(rho* rho) = 1 - b = |t|^2, Tr(Q0 rho) = b = |r|^2", "reading_of_the_attractor_state, reading_weights_are_truth_and_cost", "b = beta", "TOL_ID", "desvio", "PASSA"]],
  "controles": ["C4", "C5"], "nao_afirma": "P = R da F1.ATRATOR (espaços diferentes)"},
 {"id": "P4", "titulo": "O nome e o índice na densidade", "frases": ["V2.L16.S1", "V3.L01.S1", "V4.L14.S1"],
  "estatuto": "[DERIVED no levantamento]; face de densidade de TheWeightIsNotTheRank (distinção com condição, não ponte)",
  "partes": [
   ["P4", "P^2 = P = P^H, d = rank P >= 1, rho = P/d: Tr P = d; Tr rho = 1 (nome); Tr rho^2 = 1/d (índice); Tr rho^2 = Tr rho <=> d = 1", "trace_eq_rank_of_projection, normalized_projection_name, normalized_projection_index, name_meets_rank_only_at_the_atom", "n = 4, d em {1..4}", "TOL_ID", "d >= 2 com Tr rho^2 = Tr rho", "PASSA"]],
  "controles": ["C3"], "nao_afirma": "os dois 1 encadeados fora do átomo"},
 {"id": "B1", "titulo": "A unidade: Tr rho* = rank rho* = 1 (POSTO = RANK)", "frases": ["V3.L01.S1", "V4.L02.S2", "V4.L14.S1", "V1.L07.S2"],
  "estatuto": "[REAL runtime] rho* = diag(1,0), omega(I) = Tr rho* = 1 (um.py l.%d-%d; core %r); posição <-> rank [ONTO]" % (L1["rho_star_P"], L1["omega_I"], fd["omega_I"]),
  "partes": [
   ["B1.a", "Tr rho* = 1, rank rho* = 1, rho*^2 = rho* = rho*^H", "rhoStar_trace, rhoStar_rank, rhoStar_idem, rhoStar_herm", "rho*", "TOL_ID, RANK", "igualdade falsa", "PASSA"],
   ["B1.b", "P^2 = P => Tr P = rank P", "trace_eq_rank_of_projection", "projeções de P4", "TOL_ID", "Tr P != rank P", "PASSA"],
   ["B1.c", "range rho* = span{e0}; rank rho* = finrank(span{e0}) = 1 (mesmo espaço Fin 2 -> C)", "range_rhoStar", "vetor singular +-e0", "TOL_ID", "range != span{e0}", "PASSA"]],
  "controles": ["C3"], "nao_afirma": "rho* = firstAtom, PFmic, post Omega, bellProjector, P_F (tr %r) ou R" % CORE_SELO["certificate_II.H1_finite_face.trace_PF"]},
 {"id": "B2", "titulo": "O anticomutador {Q_th, rho*}", "frases": ["V4.L16.S2"],
  "estatuto": "[REAL runtime] só em th = 0 (um.py l.%d; core %r); em thM só a docstring [DECLARADO]; ausente do kernel (levantamento 2.12; mapa c08 = 0)" % (L1["anti0"], fd["anticommutator_norm_at_thetaM_to_0"]),
  "notas": ["'= 0 exato só em thM -> 0' (l.%d) = avaliação em th = 0, nunca limite no ângulo" % L1["doc_tensao_thetaM_0"], "sem poder discriminante"],
  "partes": [
   ["B2.a", "Q_th = [[s^2,-sc],[-sc,c^2]]; {Q_th, rho*} = [[2s^2,-sc],[-sc,0]]; = 0 <=> sin th = 0; Tr = 2s^2; soma |.|^2 = 2s^2(1 + s^2)", "Qtheta_eq, anticomm_eq, anticomm_zero_iff, anticomm_trace, anticomm_frob", "G_th (zero só em 0, pi)", "TOL_ID, TOL_ZERO", "sin th != 0 com anticomutador nulo, ou o inverso", "PASSA"],
   ["B2.b", "c : TGLCoupling: {Q_thM, rho*} != 0, Tr = 2 beta, soma |.|^2 = 2 beta (1 + beta)", "anticomm_at_thetaMiguel", "receita do um.py em thM", "TOL_ID, TOL_ZERO", "desvio ou zero", "PASSA"]],
  "controles": ["C14"], "nao_afirma": "os homônimos J_and_K_anticommute, current_anticommutes"},
 {"id": "B3", "titulo": "O vazamento", "frases": ["V4.L16.S1", "V4.L16.S3", "V4.L05.S4"],
  "estatuto": "[REAL runtime, identidade] (um.py l.%d; core leak %r, resíduo %r)" % (L1["leak"], fd["leak_sin2_thetaM"], fd["leak_equals_beta_residual"]),
  "notas": ["sem poder discriminante: identidade de thM (mapa seq 294); PASSA = validade algébrica"],
  "partes": [
   ["B3.a", "Tr(rho* Q_th) = sin^2 th = Tr(F_th(1) Q0) = (rhoOut th)_11 = |r(th)|^2", "leak_eq, leak_eq_rhoOut, leak_eq_reflected_weight", "G_th", "TOL_ID", "desvio", "PASSA"],
   ["B3.b", "c : TGLCoupling: Tr(rho* Q_thM) = beta", "leak_at_thetaMiguel", "trace(P @ Qth)", "TOL_LEAK", "desvio", "PASSA"],
   ["B3.d", "|beta - 0.012031| <= 5e-7 (número de V4 l.16)", "-", "beta de runtime", "CONF_OPERADOR", "> 5e-7", "PASSA"]],
  "controles": [], "nao_afirma": "que o vazamento discrimina beta"},
 {"id": "B4", "titulo": "F preserva o Um", "frases": ["V4.L05.S1", "V4.L14.S1"],
  "estatuto": "[REAL] pedra 116; lacuna L4 (Ad(u) preserva o posto) via Mathlib",
  "notas": ["F é ângulo: só lê"],
  "partes": [
   ["B4.a", "u^H u = 1: Tr(u rho u^H) = Tr rho, rank(u rho u^H) = rank rho; u P u^H é projeção; em rho*: Tr = rank = 1", "ad_trace, ad_rank, ad_rhoStar", "Haar n em {2,3,4}", "TOL_ID, RANK", "u que mude traço ou rank", "PASSA"],
   ["B4.b", "rhoOut th: rank 1, Tr 1, idempotente, hermitiana, pureza 1", "fractal_one_is_rank_one", "G_th", "TOL_ID, RANK, PUREZA", "rank != 1", "PASSA"]],
  "controles": ["C6", "C7"], "nao_afirma": "a leitura fractal como teorema"},
 {"id": "B5", "titulo": "Tudo = D(F(1)): o ponto final", "frases": ["V4.L13.S1", "V4.L12.S1", "V4.L14.S1", "V4.L05.S1", "V4.L04.S1"],
  "estatuto": "Tudo = D_beta(F(1)) [CONJECTURE ontológica] (um.py l.%d); peças no kernel; o posto do ponto final é novo" % L1["fractal_dephasing_principle"],
  "notas": ["o cânone sustenta (i) e nega (ii) (levantamento R4)", "o limite é de D, nunca de F"],
  "partes": [
   ["B5.a", "D_inf F_th(1) = diag(c^2, s^2); Tr 1; rank 2 <=> sin 2th != 0 (senão 1); pureza 1 - 2s^2c^2 < 1 <=> sin 2th != 0", "endpoint_eq, endpoint_rank_two_iff, endpoint_rank_one_iff, endpoint_purity", "G_th", "TOL_ID, RANK, PUREZA", "violação dos <=>", "PASSA"],
   ["B5.b", "b em [0,1]: rank diag(1-b, b) = 2 <=> 0 < b < 1, = 1 em b = 0 (e b = 1); c : TGLCoupling: D_inf F_thM(1) = diag(1-beta, beta), rank 2, pureza 1 - 2beta(1-beta) < 1", "endpoint_at_thetaMiguel", "thM em float64 e mpmath", "TOL_ID, RANK, PUREZA", "desvio; rank != 2", "PASSA"],
   ["B5.c", "g_ii = 0, g_01, g_10 > 0, t > 0: rank D_t F_th(1) = 2 <=> sin 2th != 0 (det = c^2 s^2 (1 - e^{-t(g_01+g_10)})); t = 0: rank 1; traço preservado", "dephased_rank_two_iff, dephased_trace", "thM, gamma, G_t; pureza não cresce", "TOL_ID, RANK", "t > 0, sin 2th != 0 e rank != 2", "PASSA"],
   ["B5.e(i)", "F(1) tem rank 1", "= B4.b", "= B4.b", "RANK", "= B4.b", "PASSA"],
   ["B5.e(ii)", "para todo th: rank D_inf F_th(1) = rank F_th(1)", "rank_not_preserved_by_dephasing (negação, testemunha thM), trace_survives_dephasing", "thM: 2 != 1", "RANK", "a negação com thM", "FALHA (negativo honesto: sobrevive o traço, não o posto)"]],
  "controles": ["C8", "C9"], "nao_afirma": "Tudo como teorema; que D o F devolve o posto 1"},
 {"id": "B6", "titulo": "O vazamento sobrevive à defasagem", "frases": ["V4.L10.S2"],
  "estatuto": "termo novo; invariância diagonal (identidade)",
  "partes": [
   ["B6.a", "g_ii = 0: Tr(rho* D_t Q_th) = sin^2 th para todo t", "leak_survives_dephasing", "G_th x G_t x gamma", "TOL_ID", "dependência em t", "PASSA"],
   ["B6.b", "{D_t Q_th, rho*} = [[2s^2, -e^{-t g_01} sc],[-e^{-t g_10} sc, 0]] = 0 <=> sin th = 0; {D_inf Q_th, rho*} = diag(2s^2, 0)", "anticomm_dephased_eq, anticomm_dephased_zero_iff, anticomm_limit", "thM: diag(2beta, 0)", "TOL_ID, TOL_ZERO", "anulação com sin th != 0", "PASSA"]],
  "controles": ["C10"], "nao_afirma": "invariância para leitor não diagonal"},
 {"id": "B7", "titulo": "Os dois regimes", "frases": ["V4.L04.S1", "V4.L01.S1"],
  "estatuto": "B7.a novo; B7.b e B7.c CITADO_REAL",
  "notas": ["IALDJones: o decaimento como face hiperbólica de SL(2,R) é [ONTO]; aqui só: o ângulo não tem limite, o semigrupo tem"],
  "partes": [
   ["B7.a1", "S(th)^n = S(n th); peso refletido após n passagens = sin^2(n th)", "Smat_pow, leak_after_n_passes", "n em {1,2,3,10,100,1000}", "TOL_ID n", "desvio", "PASSA"],
   ["B7.a2", "sin th != 0 => sin^2(n th) não tem limite; sin th = 0 => constante 0", "angular_leak_no_limit, angular_leak_zero_converges", "janelas; C11", "OSC", "convergência com sin th != 0; janela abaixo da cota", "PASSA"],
   ["B7.b", "taxas > 0 => D_t x -> D_inf x", "re-exporta dephase_tendsto_expectation", "decaimento e^{-gamma t}", "TOL_REL", "violação", "CITADO_REAL"],
   ["B7.c", "spin r w s = e^{-rs} e^{iws}: r > 0 => órbita -> centro; r = 0 => sem limite no centro, periódica", "re-exporta IALDJones.orbit_tendsto_center, angular_orbit_no_limit, angular_orbit_periodic", "-", "-", "-", "CITADO_REAL"]],
  "controles": ["C11", "C9"], "nao_afirma": "limite positivo no ângulo"},
 {"id": "B8", "titulo": "O ramo do nada", "frases": ["V4.L09.S1", "V4.L09.S2"],
  "estatuto": "álgebra; nada sem referente [ONTO]; Nada = MENTIRA pelos dois ramos [CONJECTURE ontológica] (um.py l.%d)" % L1["doc_nada_dois_ramos"],
  "partes": [
   ["B8.a", "th = 0: Tr(rho* Q0) = 0, {Q0, rho*} = 0, F_0(1) = rho* = D_t rho* para todo t; rank 1, pureza 1", "nothing_branch", "th = 0 exato", "TOL_ID, RANK", "valor diferente", "PASSA"],
   ["B8.b", "(para todo t, D_t F_th(1) = F_th(1)) <=> sin 2th = 0 (beta = 0 ou beta = 1; rank 1 nos dois)", "dephasing_trivial_iff", "G_th", "TOL_ZERO", "violação do <=>", "PASSA"]],
  "controles": [], "nao_afirma": "nada e impedância como termos"},
 {"id": "B9", "titulo": "A sonda honesta: o que transmite defasa", "frases": ["V4.L10.S1", "V4.L09.S1", "V4.L07.S1", "V4.L05.S2"],
  "estatuto": "duas leituras; transmitir é [INPUT da gerência]",
  "notas": ["o cânone sustenta B9.b: fractal_dephasing_principle ('Existir = o vazamento beta'), dephased_rhoOut_one_one ('o dephasing a inscreve como peso'), TGLCoupling (0 < beta < 1); V4 l.9 só é teorema nela; B9.a falha no ramo do nada", "transmitido 1 - beta (verdade), refletido beta (custo): the_one_splits_into_truth_and_cost"],
  "partes": [
   ["B9.a", "literal (transmitir = |t|^2 > 0): para todo th, cos^2 th > 0 => D atua", "literal_transmission_does_not_force_dephasing (negação; th = 0)", "th = 0", "TOL_ZERO", "contraexemplo th = 0", "FALHA (negativo honesto)"],
   ["B9.a'", "simétrico (vazar = |r|^2 > 0): para todo th, sin^2 th > 0 => D atua", "literal_leak_does_not_force_dephasing (negação; th = pi/2)", "th = pi/2", "TOL_ZERO", "contraexemplo th = pi/2", "FALHA (controle)"],
   ["B9.b", "inscrição: D atua <=> |t|^2 > 0 e |r|^2 > 0 (cos^2 th > 0 e sin^2 th > 0); em thM D atua e (D_inf F(1))_11 = beta", "dephasing_acts_iff_transmits_and_leaks, inscription_at_thetaMiguel", "G_th; thM", "TOL_ZERO, TOL_ID", "violação do <=>", "PASSA"],
   ["B9.c", "transmitir defasa (05/10): F(t)(1-P) = e^{-t}(1-P), fluxo do lock", "re-exporta transmission_dephases", "-", "-", "-", "CITADO_REAL"]],
  "controles": ["C12", "C13"], "nao_afirma": "natureza e existência como termos"},
 {"id": "O1", "titulo": "Probabilidade x vínculos", "frases": ["V1.L04.S2", "V1.L04.S3", "V1.L04.S1", "V1.L07.S3", "V1.L01.S1"],
  "estatuto": "[ONTO, epistemologia]",
  "notas": ["a validade não se aposta: no kernel é binária (selo v391 KERNEL_6163_OF_6163: %s) e os vereditos aqui são binários por face; o teste com a natureza é estatístico por desenho (sigma, ln B, poder; Fases 4/5/9); nenhum PASSA é creditação; retrodição sem ajuste não é demérito" % CORE_SELO["selo.estatuto_da_prova_v391 contém KERNEL_6163_OF_6163"]],
  "partes": [["O1", "ou os vínculos fecham, ou não fecham", "-", "-", "-", "-", "NAO_TESTAVEL"]],
  "controles": [], "nao_afirma": "que a natureza deixa de ser testada estatisticamente"},
 {"id": "O2", "titulo": "O espaço latente", "frases": ["V1.L08.S1..V1.L14.S1", "V2.L22.S1..V2.L32.S1"],
  "estatuto": "[OPEN]",
  "notas": ["F0.3.COLAPSO: %s; sem telemetria latente; neural = ilustração" % f03["verdict"]],
  "partes": [["O2", "a leitura da memória dos modelos", "-", "-", "-", "-", "ABERTO"]],
  "controles": [], "nao_afirma": "nada sobre o espaço latente"},
]
CTRL = [
 "C1 (P1.a): diag(2/3, 2/3, -1/3) em M_3(C), não PSD: Tr 1, Tr^2 1, rank 3 [psd_is_necessary]",
 "C2 (P1.a): rho*/2: PSD, rank 1, Tr rho^2 = 1/4 [normalization_is_necessary]",
 "C3 (B1, P4): I/2: Tr 1, rank 2; citado: tr P_F ~ 4 [trace_one_not_rank_one]",
 "C4 (P3): P = rho*, rho = Q0: Tr(P rho) = 0, P rho P = 0 [reading_needs_weight]",
 "C5 (P3): P = 1, rho = I/2: saída de rank 2 [reading_needs_rank_one]",
 "C6 (B4): A = diag(2,1): Tr(A rho* A^H) = 4 [nonunitary_changes_trace]",
 "C7 (B4): A = Q0: A rho* A^H = 0, rank 0 [singular_kills_rank]",
 "C8 (B5): th em {0, pi/2}: D_inf F_th(1) = F_th(1), rank 1 [endpoint_rank_one_iff]",
 "C9 (B5, B7.b): g = 0: D_t = id, sem convergência [zero_rate_no_dephasing]",
 "C10 (B6): leitor |+><+| em thM, gamma = 1: 1/2 - e^{-t} sc varia com t (delta >= 1e-3) [nondiagonal_reader_sees_time]",
 "C11 (B7.a2): th = pi: sin^2(n pi) = 0 para todo n (<= 1e-10 em float64 até 1e5) [angular_leak_zero_converges]",
 "C12 (B9.a): th = 0: |t|^2 = 1 e D não atua [literal_transmission_does_not_force_dephasing]",
 "C13 (B9.a'): th = pi/2: |r|^2 = 1 e D não atua [literal_leak_does_not_force_dephasing]",
 "C14 (B2): th = 0: {Q0, rho*} = 0 [anticomm_zero_iff]",
]
SONDAS = [
 "toda hipótese habitada por example: rho* (PSD, Tr 1); e0 e I/2; diag(1,1,0,0); th = pi/4 e th = 0 (os <=>); th = 1 e th = pi; g_01 = g_10 = 1",
 "TGLCoupling habitada com beta = 1/2 só para mostrar 0 < beta < 1 satisfazível; esse 1/2 não substitui beta",
 "cada <=> com os dois lados realizados; C1-C14 como teoremas (exists / não para todo); nenhum enunciado True ou trivial; grep: zero sorry, admit, axiom, native_decide, implemented_by, extern, opaque; nenhum literal de alpha ou beta",
]
KER_CURTO = [x.replace("TGLExt.", "").replace(" @ TGLExt/", "@").replace(".lean:", ":") for x in ANC]
ML_CURTO = [x.replace(" @ Mathlib/", "@").replace(".lean:", ":") for x in ANC_ML]
PEDRA = {
 "nome": "TheUnitIsTheRank (provisório; o operador pode renomear)",
 "nome_livre": "kernel %d arquivos; um.py %d; inventário %d; mapa 0 rotas (c01)" % (n_nome, n_nome_umpy, n_nome_inv),
 "arquivo": "TheUnitIsTheRank.lean, namespace TGLExt.TheUnitIsTheRank, em sandbox (sugestão 2_CONSTRUCAO); instalar no Nós é ato da v392",
 "imports": "GlobalLiftLadder, TheSingularExpectation, TheTraceIsNotErasable, PageInformation, FractalUnitarity, TheWeightIsNotTheRank, TheVerbalCoupling, TheSameBetaReadsThreeFaces, IALDJones, TheVerbSelectsTheAction, TheAxiomAndTheFalseWitness, Mathlib",
 "deve_provar": "as partes K com PASSA esperado, as negações de B5.e(ii), B9.a, B9.a', os controles C1-C14 e as re-exportações TRIVIAIS de B7.b, B7.c, B9.c; docstring com V1-V4 por sha16 e estatuto",
 "nao_afirma": ["beta no Lean (th genérico ou thetaMiguel c.beta)", "rho* = firstAtom, PFmic, post Omega, bellProjector, P_F ou R", "os dois 1 fora do átomo",
                "que D preserva o posto ou devolve o posto 1; que I/2 tem posto 1", "limite no ângulo; D como direção hiperbólica", "colapso físico, seleção na natureza, espaço latente",
                "Tudo, Nada, matéria, verbo, consciência como termos", "que o vazamento discrimina beta", "nome reservado, gate, a palavra proibida, frase que negue a prova"],
 "criterios_K": ["Lean 4.31.0 copiado ao sandbox, LEAN_PATH só-leitura ao .lake do Nós, EXIT 0", "print axioms dentro de {propext, Classical.choice, Quot.sound}; zero sorryAx",
                 "o tipo implica o enunciado (generalizar com example literal; hipótese a mais = NAO_CONSTRUIDO)", "impressão digital do tgl_kernel igual antes e depois",
                 "apagar toolchains, .lake e caches copiados; preservar tentativas"],
 "kernel_reaproveitado": KER_CURTO, "mathlib_KNOWN": ML_CURTO,
}
REGRA = [
 "PASSA_K: compila nos critérios, enunciado fiel, sondas passam; FALHA_K: termo prova a negação; NAO_CONSTRUIDO_K: não compilou/provou ou o enunciado mudou (não é veredito sobre a matemática)",
 "PASSA_O: toda checagem na tolerância com beta conferido; FALHA_O: fora da tolerância; SEM_VEREDITO_O: fail-closed",
 "parte: PASSA <=> PASSA_K e PASSA_O (onde há uma face só, ela decide); FALHA <=> FALHA_K ou FALHA_O; senão NAO_CONSTRUIDO",
 "FALHA pré-registrada em B5.e(ii), B9.a, B9.a': é o esperado (negativo honesto); PASSA nelas é erro e paralisa a trilha",
 "controles: esperado FALHA_SEM_HIPOTESE; controle que não falha deixa a parte de origem SEM_VEREDITO até auditoria",
 "[KNOWN] não recebe PASSA de teste (entra por citação: veredito CITADO); formalizado no kernel, o PASSA é do TERMO e o conteúdo segue [KNOWN]; [ONTO] = NAO_TESTAVEL; [OPEN] = ABERTO; já no kernel = CITADO_REAL",
 "identidades de thM (B3; partes em thM de B2, B5, B6): PASSA = validade algébrica, sem poder discriminante",
 "PASSA = validade na face testada, não creditação; não move o gate; não fala da natureza",
 "elegíveis à v392 com o teorema do atrator: partes com PASSA e os termos das negações; NAO_CONSTRUIDO não entra; decisão da gerência e do operador",
 "nada muda após o FREEZE; mudança só por pré-registro aditivo novo, com razão, preservando este e as tentativas",
]
ATRATOR = [
 "o posto que entra com o atrator é o da LEITURA: P de posto 1 nos estados (P3, B1); da F1.ATRATOR (citado), R de posto 1 nas populações (A4); o estado atrator I/2 tem posto 2; a pedra não identifica P com R",
 "não refazer formal.singularidade_le_atrator (seqs 1000-1004): nem recompilação nem A1-A6",
 "a única ponte proposta é de estado: P3.b (a leitura de posto 1 aplicada a I/2 devolve rho*)",
]
c01 = json.load(open(os.path.join(AQUI, "consultas_mapa", "c01.json"), encoding="utf-8"))
CETICO = {
 "mapa": "rotas.py consultar; %d registros; cabeça %s; arquivos consultas_mapa\\c01..c10.json" % (c01["n_registros"], c01["cabeca"]),
 "consultas": ["c%02d '%s': %d" % (k, q, json.load(open(os.path.join(AQUI, "consultas_mapa", "c%02d.json" % k), encoding="utf-8"))["n"]) for k, q in enumerate(QS, 1)],
 "Matrix.rank no kernel": n_rank,
 "ausencias": ["pureza <=> posto 1 geral (levantamento 2.3)", "{Q_th, rho*} fora de th = 0 (levantamento 2.12; c08)", "termos D_beta, F, Tudo (levantamento 2.8)", "Ad(u) preserva o posto (levantamento 2.6)", "S(th)^n: nenhum lema; o não-limite angular existe como órbita (IALDJones)"],
}
AFR = ["%s - %s: %s" % (a["id"], a["titulo"], "; ".join("%s %s" % (p[0], p[6].split(" (")[0]) for p in a["partes"])) for a in AF]

agora = datetime.datetime.now(datetime.timezone.utc).isoformat()
PIN_OUT = [[p[0], p[1], p[2] if k < 3 else p[2][:16]] for k, p in enumerate(PINOS)]
VERB_OUT = {c: {"arquivo": v["arquivo"].split("\\")[-1], "bytes": v["bytes"], "sha256": v["sha256"], "confere": v["confere"], "nota": v["nota"]} for c, v in VERB.items()}
VERB_OUT["V2"]["trilha"] = VERB["V2"]["trilha"]
DOC = {
 "documento": "PRE-REGISTRO F1.FREQUENCIA (trilha POSTO)", "gerencia": "c1", "autor": "pré-registrador (subagente)", "data": "2026-10-12", "gerado_utc": agora,
 "estatuto": "[INPUT da gerência] protocolo congelado por hash (FREEZE.json) antes de qualquer ensaio; nenhum teste, Lean ou ensaio dos objetos rodado aqui",
 "ordem": "cunhar e testar no kernel e no modelo ótico; o que passar entra no um.py v392, no apanhado geral da Bancada, com o teorema do atrator",
 "escopo": "escrita só em 1_PREREGISTRO; um.py não executado; nada no quadro, mapa, memória, túnel, Nós, Bancada_Um, site ou git; sem dado observado, provedor ou Bancada",
 "acom": "[INPUT do pré-registrador] README lido; sem referência própria e com a escrita na memória proibida pela ordem, não houve init; a inscrição é ato da gerência",
 "pasta_textos": "C:\\IALD\\Central de Patentes\\work\\cunhagens_12out (V1, V2) e cunhagens_10out (V3, V4)",
 "a_verbatins": VERB_OUT, "beta_runtime": BETA, "ancoras_um_py": L1, "ancoras_core_selo": CORE_SELO,
 "b_mapeamento": {"colunas": ["id", "frase (INPUT: íntegra; ONTO: início; =id: idêntica)", "sha16 da frase íntegra", "marca", "leitura", "afirmações"], "linhas": MAPA},
 "b_contagem": CONT, "b_fora_do_escopo": "%d frases de V2 (%s..%s, l.34-50): [FORA DO ESCOPO - F1.TEMPO]" % (len(fora), fora[0], fora[-1]),
 "b_segmentacao": "segmentar.py: linhas não vazias; corte após . ! ? seguido de maiúscula, aspas, asterisco ou parêntese, exceto após dígito",
 "objetos": DEF, "protocolo_otico": PROT,
 "c_colunas_das_partes": COLS, "c_afirmacoes": AF,
 "d_controles": {"esperado": "FALHA_SEM_HIPOTESE (C12, C13 = a FALHA das leituras literais)", "lista": CTRL}, "d_sondas_de_vacuidade": SONDAS,
 "e_pedra": PEDRA, "f_regra_de_decisao": REGRA, "interface_atrator": ATRATOR, "cetico_aferidor": CETICO,
 "pinos": PIN_OUT, "pinos_kernel_sha16": PINOS_KERNEL,
 "impressao_digital_kernel_antes": [IMP["sha256_metadados"], IMP["sha256_conteudo_lean"], IMP["n_arquivos"]],
 "afirmacoes_resumo": AFR,
}


# ------------------------------------------------ 9. serializacao compacta e guardas
def plano(v):
    return isinstance(v, list) and all(not isinstance(x, (dict, list)) or (isinstance(x, list) and all(not isinstance(y, (dict, list)) for y in x)) for x in v)


def fmt(v, ind=0):
    sp = " " * ind
    if isinstance(v, list) and v and plano(v) and any(isinstance(x, list) for x in v):
        return json.dumps(v, ensure_ascii=False, separators=(", ", ": "))
    if isinstance(v, (dict, list)) and v:
        c = json.dumps(v, ensure_ascii=False, separators=(", ", ": "))
        if len(c) + ind <= 150:
            return c
        if isinstance(v, dict):
            return "{\n" + ",\n".join("%s %s: %s" % (sp, json.dumps(k, ensure_ascii=False), fmt(x, ind + 1)) for k, x in v.items()) + "\n" + sp + "}"
        return "[\n" + ",\n".join("%s %s" % (sp, fmt(x, ind + 1)) for x in v) + "\n" + sp + "]"
    return json.dumps(v, ensure_ascii=False)


js = fmt(DOC) + "\n"
if json.loads(js) != DOC:
    falha("serializacao nao reproduz o documento")
PROIBIDAS = ("CONFIRMED", "CONFIRMADA", "não provou", "nao provou", "pós-dição", "pos-dicao")
for pr in PROIBIDAS:
    if pr in js:
        falha("palavra proibida: " + pr)


def cel(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


M = []
A = M.append
A("# PRÉ-REGISTRO — F1.FREQUENCIA (trilha POSTO)")
A("")
A("Gerência c1 · pré-registrador · %s UTC. **%s.** Ordem: %s. Escopo: %s. ACOM: %s. Notação ASCII do um.py (th = θ, thM = θ_M, c = cos th, s = sin th). Íntegra em PREREGISTRO.json." % (agora, DOC["estatuto"], DOC["ordem"], DOC["escopo"], DOC["acom"]))
A("")
A("**β de runtime** [REAL, bytes do um.py, sem executar]: α = `%s` (l.%d; SEALED l.%d igual: %s); β = α√e = `%s` (confere); thM = `%s`." % (A_STR, BETA["alpha_linha"], BETA["SEALED_linha"], BETA["SEALED_igual"], BETA["beta_float64"], BETA["theta_M"]))
A("")
A("## (a) Verbatins")
A("")
for c, v in VERB.items():
    A("- %s `%s`: %d B, sha256 `%s`, confere %s; %s" % (c, v["arquivo"].split("\\")[-1], v["bytes"], v["sha256"], v["confere"], v["nota"]))
A("- V2 na trilha: l.%s, %d B, sha256 `%s`; %s" % (VERB["V2"]["trilha"]["linhas"], VERB["V2"]["trilha"]["bytes"], VERB["V2"]["trilha"]["sha256"], DOC["b_fora_do_escopo"]))
A("")
A("## (b) Mapeamento (%s)" % ", ".join("%s %d" % (k, v) for k, v in CONT.items()))
A("")
for r in MAPA:
    A("- %s %s %s — %s — %s" % (r[0], r[3], r[1], r[4], ", ".join(r[5]) or "-"))
A("")
A("## Objetos e protocolo")
A("")
A("; ".join("**%s**: %s" % (k, v) for k, v in DEF.items()) + ".")
A("")
A("; ".join("**%s**: %s" % (k, v) for k, v in PROT.items()) + ".")
A("")
A("## (c) Afirmações (enunciado | tolerância | falsificador | esperado)")
for a in AF:
    A("")
    A("**%s - %s.** %s.%s" % (a["id"], a["titulo"], a["estatuto"], (" " + "; ".join(a["notas"]) + ".") if a.get("notas") else ""))
    for p in a["partes"]:
        A("- %s: %s | %s | %s | **%s**" % (p[0], p[1], p[4], p[5], p[6]))
A("")
A("## (d) Controles e sondas")
A("")
for c in CTRL:
    A("- %s" % c)
for s in SONDAS:
    A("- sonda: %s" % s)
A("")
A("## (e) Pedra %s" % PEDRA["nome"])
A("")
A("- %s; %s; deve provar: %s." % (PEDRA["arquivo"], PEDRA["nome_livre"], PEDRA["deve_provar"]))
A("- NÃO afirma: " + "; ".join(PEDRA["nao_afirma"]) + ".")
A("- critérios K: " + "; ".join(PEDRA["criterios_K"]) + ".")
A("")
A("## (f) Regra de decisão")
A("")
for r in REGRA:
    A("- %s" % r)
A("")
A("## Atrator, cético aferidor, pinos")
A("")
for r in ATRATOR:
    A("- %s" % r)
A("- %s: %s" % (CETICO["mapa"], "; ".join(CETICO["consultas"])))
A("- Matrix.rank no kernel: %d usos; ausências: %s" % (n_rank, "; ".join(CETICO["ausencias"])))
for p in PIN_OUT[:3]:
    A("- `%s` %d B `%s`" % (p[0].split("\\")[-1], p[1], p[2]))
md = "\n".join(M).rstrip("\n") + "\n"
for pr in PROIBIDAS:
    if pr in md:
        falha("palavra proibida no MD: " + pr)
if "\t" in md or "\t" in js or " \n" in md or " \n" in js:
    falha("tab ou espaço no fim de linha")

for alvo, txt in ((SAIDA_JSON, js), (SAIDA_MD, md)):
    if os.path.exists(alvo):
        falha("destino já existe (não sobrescrevo): " + alvo)
    b = txt.encode("utf-8")
    tmp = alvo + ".tmp"
    open(tmp, "wb").write(b)
    if open(tmp, "rb").read() != b:
        falha("temporário não confere")
    os.replace(tmp, alvo)
    if open(alvo, "rb").read() != b:
        falha("gravado não confere")
    print(alvo, len(b), sha(b))
print("frases na trilha:", len(MAPA), CONT, "fora:", len(fora))
print("afirmacoes:", [a["id"] for a in AF])
