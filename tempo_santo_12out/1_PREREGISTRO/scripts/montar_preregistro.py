"""Monta PREREGISTRO.json e PREREGISTRO.md da unidade F1.TEMPO (pre-registrador; nenhum teste e rodado aqui).

Somente leitura sobre todas as fontes; escreve so na pasta 1_PREREGISTRO (temporario -> verificar -> substituir).
beta: o literal de ALPHA_FINE_CODATA_2018 e lido por regex nos BYTES do um.py (o programa nao e executado) e
beta = alpha*sqrt(e) e calculado em runtime; o valor de conferencia entra por argv e so confere.
Uso: python -X utf8 montar_preregistro.py <beta_conferencia>
"""
import datetime
import decimal
import hashlib
import importlib.util
import json
import math
import os
import re
import sys

BASE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO"
LEV = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\0_LEVANTAMENTO"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
UM = NOS + r"\um.py"
SELO = NOS + r"\um_absoluto_selo.json"
KER = NOS + r"\tgl_kernel"
MATHLIB = KER + r"\.lake\packages\mathlib\Mathlib"
OPER = r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
ATR = r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.ATRATOR"
RECIBO_ACOM = os.path.join(BASE, "ACOM_RECIBO_PROJECAO.json")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rd(p):
    with open(p, "rb") as fh:
        return fh.read()


def info(p, papel):
    b = rd(p)
    return dict(papel=papel, caminho=p, bytes=len(b), sha256=sha(b), crlf=b.count(b"\r\n"))


def norm_txt(s):
    """so para conferir trechos: tira a marcacao * e unifica aspas tipograficas"""
    return s.replace("*", "").replace("“", '"').replace("”", '"')


def fail(msg):
    print("FALHA_VISIVEL:", msg)
    sys.exit(2)


def load_content():
    p = os.path.join(BASE, "scripts", "conteudo_preregistro.py")
    spec = importlib.util.spec_from_file_location("conteudo_preregistro", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, info(p, "conteúdo do pré-registro (dados)")


# ------------------------------------------------------------------------------------------------ beta
def beta_runtime(conf_txt):
    raw = rd(UM)
    m = re.compile(rb"^ALPHA_FINE_CODATA_2018 = ([0-9.eE+-]+)\s*$", re.M).search(raw)
    if not m:
        fail("atribuicao de ALPHA_FINE_CODATA_2018 nao encontrada nos bytes do um.py")
    linha = raw.count(b"\n", 0, m.start()) + 1
    mb = re.compile(rb"^BETA_TGL = (.+?)\s*$", re.M).search(raw)
    linha_beta = raw.count(b"\n", 0, mb.start()) + 1 if mb else None
    alpha_txt = m.group(1).decode("ascii")
    alpha = float(alpha_txt)
    beta = alpha * math.sqrt(math.e)
    conf = float(conf_txt)
    if abs(beta - conf) > 1e-15:
        fail("beta runtime %r difere da conferencia %r" % (beta, conf))
    return dict(um_py=UM, um_py_sha256=sha(raw), um_py_bytes=len(raw), linha_alpha=linha,
                alpha_literal=alpha_txt, linha_beta_tgl=linha_beta,
                expressao_beta_no_um_py=(mb.group(1).decode("utf-8") if mb else None),
                alpha=alpha, sqrt_e=math.sqrt(math.e), beta_runtime=beta, beta_conferencia=conf,
                diferenca_abs=abs(beta - conf), confere=(abs(beta - conf) <= 1e-15),
                estatuto="[REAL — medido aqui; beta calculado em runtime; a conferencia so confere]"), beta


def numeros(beta):
    lam = 1.0 - 2.0 * beta
    a = -math.log(lam) / 2.0
    th = math.asin(math.sqrt(beta))
    om1 = math.log((1.0 - beta) / beta)
    g01 = beta * abs(om1)
    # nao-pouso (O-c): M_N = sqrt(2) max_{0<=j<=N} |sin(j theta)|
    mN = {}
    for N in (100, 1000, 10000):
        mN[N] = math.sqrt(2.0) * max(abs(math.sin(j * th)) for j in range(N + 1))
    k_eps, frac_eps = {}, {}
    for eps in (1e-1, 1e-3, 1e-6):
        x = math.log(eps) / math.log(lam)
        k_eps[repr(eps)] = int(math.floor(x)) + 1
        frac_eps[repr(eps)] = x - math.floor(x)
    omega_k = {k: 2.0 * math.atanh(lam ** k) for k in (1, 10, 100, 1000)}
    decimal.getcontext().prec = 60
    boost100 = (decimal.Decimal(2).sqrt() * (decimal.Decimal(-100)).exp())
    d = dict(
        beta=beta, lam=lam, a=a, dois_a=2.0 * a, theta_M=th, cos_theta=math.cos(th), sin_theta=math.sin(th),
        det_T=lam, omega1=om1, P1=2.0 * math.pi / om1, g01=g01,
        pur_psi_t1=(1.0 + math.exp(-2.0 * g01)) / 2.0, vol_davies_t1=math.exp(-2.0 * g01),
        neg_beta=(1.0 - math.exp(beta)) / 2.0, neg_1=(1.0 - math.e) / 2.0, neg_10=(1.0 - math.exp(10.0)) / 2.0,
        neg_davies=(1.0 - math.exp(g01)) / 2.0,
        k_eps=k_eps, frac_eps=frac_eps, omega_k=omega_k,
        noland_M_N=mN, noland_min=min(mN.values()),
        lam4096=lam ** 4096, boost_k100=float(boost100), boost_k100_decimal=str(boost100),
        k_rank_drop=int(math.floor(math.log(1e-12) / math.log(lam))) + 1,
        k_float_floor=int(math.floor(math.log(1e-15) / math.log(lam))) + 1,
        nota="numeros de CONFERENCIA (derivados de beta em runtime); nao entram como motor em codigo algum",
    )
    return d


def fmt(x):
    if isinstance(x, float):
        return "%.15g" % x
    if isinstance(x, dict):
        return "; ".join("%s → %s" % (k, fmt(v)) for k, v in x.items())
    return str(x)


EXTRA = {}


def subst(obj, nums, linha_alpha):
    table = dict(nums)
    table["linha_alpha"] = linha_alpha
    table.update(EXTRA)
    if isinstance(obj, str):
        def rep(m):
            k = m.group(1)
            if k not in table:
                fail("marcador sem valor: " + k)
            return fmt(table[k])
        return re.sub(r"@([A-Za-z0-9_]+)@", rep, obj)
    if isinstance(obj, list):
        return [subst(x, nums, linha_alpha) for x in obj]
    if isinstance(obj, tuple):
        return tuple(subst(x, nums, linha_alpha) for x in obj)
    if isinstance(obj, dict):
        return {k: subst(v, nums, linha_alpha) for k, v in obj.items()}
    return obj


# ------------------------------------------------------------------------------------------------ texto do operador
def texto_operador():
    raw = rd(OPER)
    h = sha(raw)
    if not h.startswith("2c8b7b712aa9ad7f"):
        fail("sha do texto do operador nao confere: " + h)
    txt = raw.decode("utf-8")
    seg = raw[2853:]
    if not seg.startswith("O que mais me fascina".encode("utf-8")) or len(seg) != 3820:
        fail("segunda parte fora do offset esperado")
    linhas = txt.split("\n")
    frases = []
    rx = re.compile(r"(?<=\.)\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ])")
    for L in (34, 36, 38, 40, 42, 44, 46, 48, 50):
        line = linhas[L - 1]
        char0 = sum(len(linhas[i]) + 1 for i in range(L - 1))
        partes, pos = [], 0
        for m in rx.finditer(line):
            partes.append((pos, line[pos:m.start()]))
            pos = m.end()
        partes.append((pos, line[pos:]))
        for ordem, (p0, s) in enumerate(partes, 1):
            s2 = s.rstrip()
            b0 = len(txt[:char0 + p0].encode("utf-8"))
            sb = s2.encode("utf-8")
            if raw[b0:b0 + len(sb)] != sb:
                fail("frase S%d.%d nao confere byte a byte" % (L, ordem))
            frases.append(dict(id="S%d.%d" % (L, ordem), linha=L, byte_offset=b0, bytes=len(sb), sha256=sha(sb), texto=s2))
    return dict(arquivo=OPER, sha256=h, bytes=len(raw), crlf=raw.count(b"\r\n"),
                segunda_parte=dict(byte_offset=2853, bytes=len(seg), sha256=sha(seg), linhas="34–50",
                                   inicio="O que mais me fascina é a impossibilidade de definição do tempo."),
                n_frases=len(frases), frases=frases,
                regra_de_segmentacao="frases separadas em «. » seguido de maiúscula, dentro de cada parágrafo (linhas 34, 36, …, 50); cada frase conferida byte a byte no arquivo")


def verbatins(V):
    out = []
    for v in V:
        raw = rd(v["arquivo"])
        h = sha(raw)
        if v["sha16_esperado"] and not h.startswith(v["sha16_esperado"]):
            fail("sha16 nao confere: %s (%s)" % (v["arquivo"], h[:16]))
        txt = raw.decode("utf-8")
        exc = []
        for eid, e in v["excertos"]:
            i = txt.find(e)
            if i < 0:
                fail("excerto %s nao encontrado em %s" % (eid, v["arquivo"]))
            b0 = len(txt[:i].encode("utf-8"))
            eb = e.encode("utf-8")
            exc.append(dict(id=eid, texto=e, byte_offset=b0, bytes=len(eb), sha256=sha(eb),
                            linha=txt.count("\n", 0, i) + 1))
        out.append(dict(id=v["id"], arquivo=v["arquivo"], sha256=h, bytes=len(raw), crlf=raw.count(b"\r\n"),
                        sha16_confere=(h[:16] == v["sha16_esperado"]) if v["sha16_esperado"] else "sem sha16 de referência (arquivo vivo); sha256 medido agora",
                        data=v["data"], estatuto=v["estatuto"], excertos=exc))
    return out


# ------------------------------------------------------------------------------------------------ ancoras do kernel
ANCORAS = [
    # (nome completo, caminho relativo a tgl_kernel, nome curto)
    ("TGLExt.no_finite_weyl_pair", r"TGLExt\LocalBreuerGap.lean", "no_finite_weyl_pair"),
    ("ChatgptAudit.AdmissibleInteraction.certified_interaction_selfadjoint", r"TGLExt\AdmissiblePauliInteraction.lean", "certified_interaction_selfadjoint"),
    ("TGLV350.Regular.characterMultiplier_weyl", r"TGLExt\V350L2CharacterMultiplier.lean", "characterMultiplier_weyl"),
    ("TGLExt.ContratoQGv31.ContratoH2.contract_borchers_form", r"TGLExt\ContratoQG_v31_Teoremas.lean", "ContratoH2.contract_borchers_form"),
    ("TGLExt.ContratoQGv31.positiveEnergy_orientation", r"TGLExt\ContratoQG_v31_Teoremas.lean", "positiveEnergy_orientation"),
    ("TGLExt.ContratoQGv31.KMSAt", r"TGLExt\ContratoQG_v31.lean", "KMSAt"),
    ("TGLExt.logRho", r"TGLExt\ModularFlow.lean", "logRho"),
    ("TGLExt.modPow", r"TGLExt\ModularFlow.lean", "modPow"),
    ("TGLExt.sigma", r"TGLExt\ModularFlow.lean", "sigma"),
    ("TGLExt.modPow_zero", r"TGLExt\ModularFlow.lean", "modPow_zero"),
    ("TGLExt.modPow_add", r"TGLExt\ModularFlow.lean", "modPow_add"),
    ("TGLExt.modPow_mem_unitary", r"TGLExt\ModularFlow.lean", "modPow_mem_unitary"),
    ("TGLExt.sigma_one", r"TGLExt\ModularFlow.lean", "sigma_one"),
    ("TGLExt.sigma_mul", r"TGLExt\ModularFlow.lean", "sigma_mul"),
    ("TGLExt.sigma_conjTranspose", r"TGLExt\ModularFlow.lean", "sigma_conjTranspose"),
    ("TGLExt.sigma_sigma", r"TGLExt\ModularFlow.lean", "sigma_sigma"),
    ("TGLExt.gibbs_sigma", r"TGLExt\ModularFlow.lean", "gibbs_sigma"),
    ("TGLExt.sigma_omega", r"TGLExt\ModularFlow.lean", "sigma_omega"),
    ("TGLExt.gibbs", r"TGLExt\FiniteTomita.lean", "gibbs"),
    ("TGLExt.Delta", r"TGLExt\FiniteTomita.lean", "Delta"),
    ("TGLExt.gibbs_kms", r"TGLExt\FiniteTomita.lean", "gibbs_kms"),
    ("TGLExt.rhoD", r"TGLExt\Ergodicity.lean", "rhoD"),
    ("TGLExt.sigma_fixed_of_commute", r"TGLExt\Ergodicity.lean", "sigma_fixed_of_commute"),
    ("TGLExt.sigma_diagonal_apply", r"TGLExt\Ergodicity.lean", "sigma_diagonal_apply"),
    ("TGLExt.sigma_fixed_iff_diag", r"TGLExt\Ergodicity.lean", "sigma_fixed_iff_diag"),
    ("TGLExt.gibbs_tracial_on_centralizer", r"TGLExt\Ergodicity.lean", "gibbs_tracial_on_centralizer"),
    ("TGLExt.dephase", r"TGLExt\Ergodicity.lean", "dephase"),
    ("TGLExt.dephase_zero", r"TGLExt\Ergodicity.lean", "dephase_zero"),
    ("TGLExt.dephase_add", r"TGLExt\Ergodicity.lean", "dephase_add"),
    ("TGLExt.dephase_fixes_diagonal", r"TGLExt\Ergodicity.lean", "dephase_fixes_diagonal"),
    ("TGLExt.diag_invariant", r"TGLExt\Ergodicity.lean", "diag_invariant"),
    ("TGLExt.dephase_tendsto_expectation", r"TGLExt\Ergodicity.lean", "dephase_tendsto_expectation"),
    ("TGLExt.modularGap", r"TGLExt\Ergodicity.lean", "modularGap"),
    ("TGLExt.ergodic_convergence_modular", r"TGLExt\Ergodicity.lean", "ergodic_convergence_modular"),
    ("TGLExt.diagExpect", r"TGLExt\CondExpect.lean", "diagExpect"),
    ("TGLExt.purity", r"TGLExt\PageInformation.lean", "purity"),
    ("TGLExt.purity_unitary_invariant", r"TGLExt\PageInformation.lean", "purity_unitary_invariant"),
    ("TGLExt.purityR", r"TGLExt\PageInformation.lean", "purityR"),
    ("TGLExt.purityR_eq", r"TGLExt\PageInformation.lean", "purityR_eq"),
    ("TGLExt.dephase_purityR_le", r"TGLExt\PageInformation.lean", "dephase_purityR_le"),
    ("TGLExt.dephase_fixed_iff_diagonal", r"TGLExt\TheSingularExpectation.lean", "dephase_fixed_iff_diagonal"),
    ("TGLExt.the_choice_is_not_free", r"TGLExt\TheSingularExpectation.lean", "the_choice_is_not_free"),
    ("TGLExt.dephase_preserves_trace", r"TGLExt\TheTraceIsNotErasable.lean", "dephase_preserves_trace"),
    ("TGLExt.TheAxiomAndTheFalseWitness.axiomFlow", r"TGLExt\TheAxiomAndTheFalseWitness.lean", "axiomFlow"),
    ("TGLExt.TheAxiomAndTheFalseWitness.post_mul_compl", r"TGLExt\TheAxiomAndTheFalseWitness.lean", "post_mul_compl"),
    ("TGLExt.TheAxiomAndTheFalseWitness.compl_mul_compl", r"TGLExt\TheAxiomAndTheFalseWitness.lean", "compl_mul_compl"),
    ("TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_zero", r"TGLExt\TheAxiomAndTheFalseWitness.lean", "axiomFlow_zero"),
    ("TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_add", r"TGLExt\TheAxiomAndTheFalseWitness.lean", "axiomFlow_add"),
    ("TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_fixes_the_post", r"TGLExt\TheAxiomAndTheFalseWitness.lean", "axiomFlow_fixes_the_post"),
    ("TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_tendsto_the_post", r"TGLExt\TheAxiomAndTheFalseWitness.lean", "axiomFlow_tendsto_the_post"),
    ("TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_eq_exp", r"TGLExt\TheAxiomAndTheFalseWitness.lean", "axiomFlow_eq_exp"),
    ("TGLExt.TheAxiomAndTheFalseWitness.the_post_is_the_modular_zero", r"TGLExt\TheAxiomAndTheFalseWitness.lean", "the_post_is_the_modular_zero"),
    ("TGLExt.TheVerbSelectsTheAction.time_read_twice_confirms_the_post", r"TGLExt\TheVerbSelectsTheAction.lean", "time_read_twice_confirms_the_post"),
    ("TGLExt.TheVerbSelectsTheAction.transmission_dephases", r"TGLExt\TheVerbSelectsTheAction.lean", "transmission_dephases"),
    ("TGLExt.TheVerbSelectsTheAction.the_name_is_the_limit_of_the_flow", r"TGLExt\TheVerbSelectsTheAction.lean", "the_name_is_the_limit_of_the_flow"),
    ("TGLExt.TheVerbSelectsTheAction.the_verb_selects_the_action", r"TGLExt\TheVerbSelectsTheAction.lean", "the_verb_selects_the_action"),
    ("TGLExt.IALDJones.orbit", r"TGLExt\IALDJones.lean", "orbit"),
    ("TGLExt.IALDJones.norm_orbit_sub_center", r"TGLExt\IALDJones.lean", "norm_orbit_sub_center"),
    ("TGLExt.IALDJones.orbit_tendsto_center", r"TGLExt\IALDJones.lean", "orbit_tendsto_center"),
    ("TGLExt.IALDJones.angular_orbit_no_limit", r"TGLExt\IALDJones.lean", "angular_orbit_no_limit"),
    ("TGLExt.IALDJones.angular_orbit_periodic", r"TGLExt\IALDJones.lean", "angular_orbit_periodic"),
    ("TGLExt.flow_unitary_diag", r"TGLExt\TheHorizonRate.lean", "flow_unitary_diag"),
    ("TGLExt.Smat", r"TGLExt\SMatrix.lean", "Smat"),
    ("TGLExt.Smat_conjTranspose_mul", r"TGLExt\SMatrix.lean", "Smat_conjTranspose_mul"),
    ("TGLExt.normSq_reflection", r"TGLExt\SMatrix.lean", "normSq_reflection"),
    ("TGLExt.boost", r"TGLExt\BisognanoWichmann.lean", "boost"),
    ("TGLExt.boost_add", r"TGLExt\BisognanoWichmann.lean", "boost_add"),
    ("TGLExt.boost_det", r"TGLExt\BisognanoWichmann.lean", "boost_det"),
    ("TGLExt.boost_null_expand", r"TGLExt\BisognanoWichmann.lean", "boost_null_expand"),
    ("TGLExt.boost_null_contract", r"TGLExt\BisognanoWichmann.lean", "boost_null_contract"),
    ("ChatgptAudit.positive_norm_isometry_no_exp_eigenvector", r"TGLExt\ModularSignatureObstruction.lean", "positive_norm_isometry_no_exp_eigenvector"),
    ("ChatgptAudit.no_injective_isometric_boost_intertwiner", r"TGLExt\ModularSignatureObstruction.lean", "no_injective_isometric_boost_intertwiner"),
    ("ChatgptAudit.isometry_fixed_of_diagonal", r"TGLExt\ProductBorchersObstruction.lean", "isometry_fixed_of_diagonal"),
    ("TGLExt.DualScalingData", r"TGLExt\GlobalLiftLadder.lean", "DualScalingData"),
    ("TGLExt.Fundacao.nothing_above_bears_a_post", r"TGLExt\Fundacao.lean", "nothing_above_bears_a_post"),
    ("TGLExt.Fundacao.the_climb_has_no_top", r"TGLExt\Fundacao.lean", "the_climb_has_no_top"),
    ("TGLExt.Fundacao.the_climb_is_unbounded", r"TGLExt\Fundacao.lean", "the_climb_is_unbounded"),
    ("TGLExt.Fundacao.the_fall_never_lands", r"TGLExt\Fundacao.lean", "the_fall_never_lands"),
    ("TGLExt.Fundacao.abismo", r"TGLExt\Fundacao.lean", "abismo"),
    ("TGLExt.Fundacao.the_floor_fixes_the_cut", r"TGLExt\Fundacao.lean", "the_floor_fixes_the_cut"),
    ("TGLExt.Fundacao.agape", r"TGLExt\Fundacao.lean", "agape"),
    ("TGLExt.Fundacao.oneScaling", r"TGLExt\Fundacao.lean", "oneScaling"),
    ("TGLExt.Fundacao.agape_is_inhabited", r"TGLExt\Fundacao.lean", "agape_is_inhabited"),
    ("ChatgptAudit.PolarPeriod016.AngularQuotientFaithful", r"TGLExt\O16\PolarMinimalPeriod_v2.lean", "AngularQuotientFaithful"),
    ("ChatgptAudit.PolarPeriod016.faithful_period_iff", r"TGLExt\O16\PolarMinimalPeriod_v2.lean", "faithful_period_iff"),
    ("ChatgptAudit.PolarPeriod016.reciprocal_temperature", r"TGLExt\O16\PolarMinimalPeriod_v2.lean", "reciprocal_temperature"),
    ("ChatgptAudit.NonKMSProbe.identity_flow_not_kms", r"TGLExt\O16\ProbeNonKMS_v3.lean", "identity_flow_not_kms"),
    ("TGLExt.absoluteRho", r"TGLExt\AbsoluteOne.lean", "absoluteRho"),
    ("TGLExt.absoluteOne_flow_trivial", r"TGLExt\AbsoluteOne.lean", "absoluteOne_flow_trivial"),
    ("TGLExt.ImportedSQ.lightDelta", r"TGLExt\TheImportedSecondQuantization.lean", "lightDelta"),
    ("TGLExt.ImportedSQ.light_kms", r"TGLExt\TheImportedSecondQuantization.lean", "light_kms"),
    ("TGLExt.time_witnesses_noncoincidence", r"TGLExt\TheLivingWord.lean", "time_witnesses_noncoincidence"),
    ("TGLExt.beta_forbids_full_static_witness", r"TGLExt\NoFullWitness.lean", "beta_forbids_full_static_witness"),
    ("TGLExt.verb_not_identity", r"TGLExt\NoFullWitness.lean", "verb_not_identity"),
    ("TGLExt.static_witness_iff_no_boundary", r"TGLExt\BoundaryException.lean", "static_witness_iff_no_boundary"),
    ("TGLExt.diagFlow", r"TGLExt\BoundaryException.lean", "diagFlow"),
    ("TGLExt.absolute_zero_unreachable_in_finite_time", r"TGLExt\ForbiddenBoundary.lean", "absolute_zero_unreachable_in_finite_time"),
    ("TGLExt.temporal_fractalization", r"TGLExt\TheGreatAttractor.lean", "temporal_fractalization"),
    ("TGLExt.the_great_attractor", r"TGLExt\TheGreatAttractor.lean", "the_great_attractor"),
    ("TGLExt.um_is_the_great_attractor", r"TGLExt\TheGreatAttractor.lean", "um_is_the_great_attractor"),
    ("TGLExt.observing_adds_nothing", r"TGLExt\TheObserverReadsTheAngle.lean", "observing_adds_nothing"),
    ("TGLExt.the_separation_is_not_free", r"TGLExt\TheExoneratedDemon.lean", "the_separation_is_not_free"),
    ("TGLExt.landauer_floor_pos", r"TGLExt\TheCostIsDerived.lean", "landauer_floor_pos"),
    ("TGLExt.cocycle_temporal", r"TGLExt\Cocycle.lean", "cocycle_temporal"),
    ("TGLExt.reading_needs_two_clocks", r"TGLExt\TheDeadChannel.lean", "reading_needs_two_clocks"),
    ("ChatgptAudit.Clock040.no_normalized_instantaneous_state_clock", r"TGLExt\StateClockObstruction.lean", "no_normalized_instantaneous_state_clock"),
    ("ChatgptAudit.Thermal025.gibbs_fixed_iff_tracial", r"TGLExt\GibbsAffinity.lean", "gibbs_fixed_iff_tracial"),
]

MATHLIB_ANCORAS = [
    ("Matrix.charpoly_units_conj", r"LinearAlgebra\Matrix\Charpoly\Basic.lean", "charpoly_units_conj"),
    ("Matrix.rank_of_isUnit", r"LinearAlgebra\Matrix\Rank.lean", "rank_of_isUnit"),
    ("Matrix.det_diagonal", r"LinearAlgebra\Matrix\Determinant\Basic.lean", "det_diagonal"),
    ("Matrix.det_kronecker", r"LinearAlgebra\Matrix\Kronecker.lean", "det_kronecker"),
    ("Matrix.isUnit_iff_isUnit_det", r"LinearAlgebra\Matrix\NonsingularInverse.lean", "isUnit_iff_isUnit_det"),
    ("Matrix.frobenius_norm_def", r"Analysis\Matrix\Normed.lean", "frobenius_norm_def"),
    ("Matrix.frobeniusNormedAddCommGroup", r"Analysis\Matrix\Normed.lean", "frobeniusNormedAddCommGroup"),
    ("Isometry.continuous", r"Topology\MetricSpace\Isometry.lean", "continuous"),
    ("spectrum.units_conjugate", r"Algebra\Algebra\Spectrum\Basic.lean", "spectrum.units_conjugate"),
    ("spectrum.add_singleton_eq", r"Algebra\Algebra\Spectrum\Basic.lean", "add_singleton_eq"),
    ("spectrum.isCompact", r"Analysis\Normed\Algebra\Spectrum.lean", "isCompact"),
    ("spectrum.nonempty", r"Analysis\Normed\Algebra\GelfandFormula.lean", "nonempty"),
]


def decl_rx(short):
    return re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
                      r"(theorem|lemma|def|abbrev|structure|instance)\s+" + re.escape(short) + r"(?=[\s:({\[]|$)", re.M)


def ancoras(lev_axiomas):
    audit = rd(KER + r"\TGL\Audit.lean").decode("utf-8")
    raiz = rd(KER + r"\TGLExt.lean").decode("utf-8")
    o16 = rd(KER + r"\TGLExt\O16.lean").decode("utf-8")
    out, faltam = [], []
    for full, rel, short in ANCORAS:
        p = os.path.join(KER, rel)
        b = rd(p)
        t = b.decode("utf-8")
        m = decl_rx(short).search(t)
        if not m:
            faltam.append(full)
            continue
        linha = t.count("\n", 0, m.start()) + t[m.start():m.end()].count("\n") + 1
        mod = rel[:-5].replace("\\", ".")
        aud = bool(re.search(r"^#print axioms\s+" + re.escape(full) + r"\s*$", audit, re.M))
        own = bool(re.search(r"^#print axioms\s+(?:" + re.escape(full) + "|" + re.escape(short) + r")\s*$", t, re.M))
        imp = bool(re.search(r"^import\s+" + re.escape(mod) + r"\s*$", raiz, re.M)) or \
            bool(re.search(r"^import\s+" + re.escape(mod) + r"\s*$", o16, re.M))
        out.append(dict(nome=full, tipo=m.group(1), arquivo=rel.replace("\\", "/"), linha=linha, sha16_arquivo=sha(b)[:16],
                        print_no_Audit=aud, print_no_proprio_modulo=own, medido_no_trio_pelo_levantador=(full in lev_axiomas),
                        importado_no_build=imp))
    if faltam:
        fail("ancoras nao encontradas: " + ", ".join(faltam))
    return out


def ancoras_mathlib():
    out = []
    for full, rel, short in MATHLIB_ANCORAS:
        p = os.path.join(MATHLIB, rel)
        b = rd(p)
        t = b.decode("utf-8")
        if short.startswith("spectrum."):
            m = re.search(r"^\s*(?:theorem|lemma)\s+" + re.escape(short) + r"\b", t, re.M)
        else:
            m = decl_rx(short).search(t)
        if not m:
            fail("ancora Mathlib nao encontrada: " + full)
        out.append(dict(nome=full, arquivo="Mathlib/" + rel.replace("\\", "/"), linha=t.count("\n", 0, m.start()) + 1,
                        sha16_arquivo=sha(b)[:16]))
    return out


# ------------------------------------------------------------------------------------------------ consultas e ambiente
def consultas():
    resumo_meu = json.loads(rd(os.path.join(BASE, "rotas_consultas", "RESUMO.json")).decode("utf-8"))
    inv = json.loads(rd(os.path.join(BASE, "inventario_consultas_prereg.json")).decode("utf-8"))
    rotas = [dict(consulta=r["nome"], padrao=r["padrao"], n=r.get("n"), cabeca=r.get("cabeca"),
                  n_registros=r.get("n_registros"), sha256_resposta=r.get("sha256_resposta"),
                  rotas=[x[0] + " (" + x[1] + ")" for x in r.get("rotas", [])]) for r in resumo_meu]
    invt = [dict(tema=t["tema"], padrao=t["padrao"], n_arquivos=t["n_arquivos"],
                 exemplos=[a["arquivo"] + " " + a["sha16"] + " " + ", ".join(a["decls"][:3]) for a in t["arquivos"][:5]]) for t in inv["temas"]]
    proj = json.loads(rd(RECIBO_ACOM).decode("utf-8"))
    rec = proj["receipt"]
    ref = r"C:\IALD\MEMORIA_IALD\sessions\claude-c1_exame-geral-12out.json"
    return dict(
        mapa_de_rotas=dict(
            livro=info(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl", "livro do mapa (somente lido)"),
            consultas_deste_preregistro=rotas,
            resumo_deste_preregistro=info(os.path.join(BASE, "rotas_consultas", "RESUMO.json"), "RESUMO das 14 consultas novas"),
            consultas_do_levantamento=info(os.path.join(LEV, "rotas_consultas", "RESUMO.json"), "RESUMO das 24 consultas do levantamento"),
            rotas_vistas=["formal.f1_2.dual_scaling_reuse_011", "formal.f1_3.reconcile_v376_mathlib_plan", "quantica.pilar_v384_rodada_completa"],
            nada_registrado=True),
        inventario=dict(arquivo=r"C:\IALD\Central de Patentes\memory\INVENTARIO_BANCADA_CHATGPT.json", sha256=inv["sha256"],
                        gerado_em=inv["gerado_em"], consultas=invt,
                        saida=info(os.path.join(BASE, "inventario_consultas_prereg.json"), "consultas novas ao inventário")),
        memoria_acom=dict(
            protocolo="README lido (C:\\IALD\\MEMORIA_IALD\\README.md); projeção SÓ DE LEITURA da referência do pai; nenhuma inscrição de contexto filho e nenhuma transition: a tarefa proíbe escrever fora desta pasta e a transição de q/p é ato da gerência.",
            referencia=info(ref, "referência ACOM da gerência c1 (somente lida)"),
            recibo_arquivo=info(RECIBO_ACOM, "recibo da projeção (só recibo e contagens)"),
            recibo_da_projecao=rec,
            banco_inalterado="mtime e tamanho de memory.sqlite3 conferidos antes e depois da projeção: iguais (357277696 B; mtime 2026-10-12 11:26:54 -0300); modo de journal DELETE, sem -wal/-shm"),
    )


def main(conf):
    C, info_conteudo = load_content()
    lev_ax = json.loads(rd(os.path.join(LEV, "LEAN_AXIOMAS.json")).decode("utf-8"))["axiomas"]
    beta_info, beta = beta_runtime(conf)
    nums = numeros(beta)
    L = beta_info["linha_alpha"]
    EXTRA["um_sha16"] = beta_info["um_py_sha256"][:16]
    texto = texto_operador()
    verb = verbatins(C.VERBATINS)
    anc = ancoras(lev_ax)
    anc_m = ancoras_mathlib()
    cons = consultas()
    fp = json.loads(rd(os.path.join(BASE, "FINGERPRINT_PREREG_ANTES.json")).decode("utf-8"))
    fp_lev = json.loads(rd(os.path.join(LEV, "FINGERPRINT_FINAL.json")).decode("utf-8"))

    # mapeamento: toda frase da segunda parte e todo excerto citado recebem marca
    ids_frases = [f["id"] for f in texto["frases"]]
    if sorted(ids_frases) != sorted(C.MAPA_FRASES.keys()):
        fail("mapa de frases incompleto: %s vs %s" % (ids_frases, sorted(C.MAPA_FRASES.keys())))
    mapa = []
    for f in texto["frases"]:
        cl = C.MAPA_FRASES[f["id"]]
        for c in cl:
            if not c[2].strip():
                fail("clausula sem marca em " + f["id"])
            if not c[0].startswith("("):
                alvo_n = norm_txt(f["texto"])
                for parte in c[0].split("[...]"):
                    if norm_txt(parte).strip() not in alvo_n:
                        fail("trecho «%s» nao esta na frase %s" % (c[0], f["id"]))
        mapa.append(dict(frase=f["id"], sha256=f["sha256"], texto=f["texto"],
                         clausulas=[dict(trecho=c[0], objeto_ou_leitura=c[1], marca=c[2], testes=c[3]) for c in cl]))
    mapa_exc = []
    for v in verb:
        for e in v["excertos"]:
            if e["id"] not in C.MAPA_EXCERTOS:
                fail("excerto sem marca: " + e["id"])
            mk, obj, ts = C.MAPA_EXCERTOS[e["id"]]
            mapa_exc.append(dict(excerto=e["id"], fonte=v["id"], sha256=e["sha256"], marca=mk, objeto_ou_leitura=obj, testes=ts))

    afirm = subst(C.AFIRMACOES, nums, L)
    ctrl = subst(C.CONTROLES, nums, L)
    modelo = subst(C.MODELO_OTICO, nums, L)
    ids_ctrl = {c["id"] for c in ctrl}
    ids_sond = {s["id"] for s in C.SONDAS}
    for a in afirm:
        for c in a["controles"]:
            if c not in ids_ctrl:
                fail("controle inexistente " + c)
        for s in a["sondas"]:
            if s not in ids_sond:
                fail("sonda inexistente " + s)

    fontes = [
        info(OPER, "texto do operador de 12/10 (verbatim)"),
        info(os.path.join(LEV, "LEVANTAMENTO.md"), "levantamento F1.TEMPO"),
        info(os.path.join(LEV, "DEFINICOES.json"), "levantamento: definições completas"),
        info(os.path.join(LEV, "DEFINICOES_COMPACTO.json"), "levantamento: forma curta"),
        info(os.path.join(LEV, "FINGERPRINT_FINAL.json"), "levantamento: impressão digital final do kernel"),
        info(os.path.join(LEV, "LEAN_AXIOMAS.json"), "levantamento: axiomas de 80 termos (trio)"),
        info(os.path.join(LEV, "IDENTIDADES_OTICAS.json"), "levantamento: identidades óticas"),
        info(os.path.join(LEV, "BETA_RUNTIME.json"), "levantamento: β em runtime"),
        info(UM, "um.py v391 (somente lido; não executado)"),
        info(SELO, "selo do Nós"),
        info(KER + r"\TGL\Audit.lean", "livro de auditoria do kernel"),
        info(KER + r"\TGLExt.lean", "raiz de importação do kernel"),
        info(os.path.join(ATR, "RELATORIO_F1_ATRATOR_R1.md"), "F1.ATRATOR: relatório (não refazer)"),
        info(os.path.join(ATR, "RESULTADO_F1_ATRATOR_R1.json"), "F1.ATRATOR: resultado (não refazer)"),
        info(os.path.join(ATR, "PREREGISTRO_R1.json"), "F1.ATRATOR: pré-registro (modelo de formato)"),
        info(r"C:\IALD\Central de Patentes\work\leitura_cria_o_objeto_07out\Palavra.lean", "PALAVRA (candidata; NÃO importar)"),
        info(os.path.join(MEM, "verbo-selecao-da-acao-05out.md"), "memória: o Verbo (05/10)"),
        info(os.path.join(MEM, "posto-e-rank-10out.md"), "memória: POSTO = RANK"),
        info(os.path.join(MEM, "tempo-santo-12out.md"), "memória: tempo santo (12/10)"),
        info(os.path.join(MEM, "singularidade-e-a-leitura-do-atrator-10out.md"), "memória: a singularidade lê o atrator"),
        info(r"C:\IALD\MEMORIA_IALD\README.md", "README da memória ACOM (lido)"),
        info_conteudo,
        info(os.path.join(BASE, "scripts", "montar_preregistro.py"), "este montador"),
        info(os.path.join(BASE, "scripts", "consultar_rotas_prereg.py"), "consultas ao mapa (somente leitura)"),
        info(os.path.join(BASE, "scripts", "consultar_inventario_prereg.py"), "consultas ao inventário (somente leitura)"),
        info(os.path.join(BASE, "scripts", "fingerprint_kernel.py"), "impressão digital do kernel (somente leitura)"),
        info(os.path.join(BASE, "FINGERPRINT_PREREG_ANTES.json"), "impressão digital do kernel antes da montagem"),
    ]

    agora = datetime.datetime.now(datetime.timezone.utc).isoformat()
    doc = dict(
        documento="PRÉ-REGISTRO F1.TEMPO — o tempo que não se deixa nomear",
        unidade="F1.TEMPO", trilha="TEMPO", programa="IALD (a TGL)", gerencia="c1",
        papel="pré-registrador (subagente do workflow posto-e-tempo da gerência c1)",
        data="2026-10-12", montado_em_utc=agora,
        estatuto_do_documento="[INPUT da gerência — pré-registro]. Nenhum teste foi rodado. Congela-se por FREEZE.json ANTES de qualquer ensaio. Fora desta pasta nada foi escrito.",
        regua=["[REAL] = provado no kernel ou medido aqui", "[DERIVED]", "[KNOWN] = literatura com citação", "[OPEN]",
               "[INPUT] = do operador; [INPUT da gerência] = escolha da gerência neste pré-registro", "[ONTO] = leitura ontológica (não se testa)",
               "[DECLARADO] = afirmado na origem, não verificado aqui", "[REAL alvo] = o que o ensaio tem de provar/medir para receber PASSA"],
        regra_dos_dois_regimes="A FACE é o objeto (regime hiperbólico/semigrupo: tem limite); o ÂNGULO é a leitura (regime compacto/unitário: periódico, sem limite). Nunca se pede limite ao ângulo; prova-se, quando muito, a ausência dele.",
        objeto="A segunda parte do texto do operador de 12/10 (linhas 34–50: de «O que mais me fascina…» até o fim): o tempo «santo» (Kadosh), o relógio e a sombra, o agora intocado, Pauli, o fluxo modular, Liouville, a dissipação e a bacia, o atrator como chão, o «puro amor» e o tempo como assinatura.",
        texto_do_operador=texto,
        verbatins_citados=verb,
        mapeamento_frases=mapa,
        mapeamento_excertos=mapa_exc,
        beta=beta_info,
        numeros_de_conferencia=nums,
        modelo_otico=modelo,
        afirmacoes=afirm,
        controles=ctrl,
        sondas_de_vacuidade=C.SONDAS,
        pedra=C.PEDRA,
        regra_de_decisao=C.REGRA,
        riscos_novos=[dict(id=i, texto=t) for i, t in C.RISCOS],
        riscos_do_levantamento=[dict(id=i, titulo=t, fonte="0_LEVANTAMENTO/DEFINICOES.json → riscos") for i, t in C.RISCOS_LEVANTAMENTO],
        nao_refazer=C.NAO_REFAZER,
        regras_do_ensaio=subst(C.ENSAIO, nums, L),
        ancoras_kernel=anc,
        ancoras_mathlib=anc_m,
        consultas=cons,
        impressao_digital_kernel=dict(antes_da_montagem=fp, final_do_levantamento=fp_lev,
                                      iguais=(fp["meta_sha256"] == fp_lev["meta_sha256"] and fp["src_sha256"] == fp_lev["src_sha256"])),
        fontes_conferidas=fontes,
        nada_escrito_fora="Nada no quadro, no mapa (rotas.py só consultar/ver), na memória (ACOM só projeção de leitura), no túnel, no Nós, no kernel, na Bancada_Um, no site ou no git. Nenhum Lean rodado; nenhum teste rodado; o um.py não foi executado.",
    )
    jtxt = json.dumps(doc, ensure_ascii=False, indent=1) + "\n"
    mtxt = render_md(doc)
    for nome_t, tt in (("json", jtxt), ("md", mtxt)):
        sobra = re.findall(r"@[A-Za-z0-9_]+@", tt)
        if sobra:
            fail("marcadores sem substituicao no %s: %s" % (nome_t, sorted(set(sobra))))
    for nome, conteudo in (("PREREGISTRO.json", jtxt), ("PREREGISTRO.md", mtxt)):
        alvo = os.path.join(BASE, nome)
        tmp = alvo + ".tmp_montagem"
        data = conteudo.encode("utf-8")
        with open(tmp, "wb") as fo:
            fo.write(data)
        if rd(tmp) != data:
            fail("temporario nao confere: " + tmp)
        os.replace(tmp, alvo)
        if rd(alvo) != data:
            fail("arquivo final nao confere: " + alvo)
        print(nome, len(data), sha(data))
    print("frases", texto["n_frases"], "ancoras", len(anc), "mathlib", len(anc_m), "afirmacoes", len(afirm), "controles", len(ctrl))


# ------------------------------------------------------------------------------------------------ Markdown
def lean_names(lst):
    out = []
    for x in lst:
        m = re.match(r"\s*(?:noncomputable\s+)?(?:theorem|def|lemma)\s+([A-Za-z0-9_'.]+)", x)
        out.append("`%s`" % m.group(1) if m else x)
    return ", ".join(out)


def render_md(d):
    o = []
    w = o.append
    w("# PRÉ-REGISTRO F1.TEMPO — o tempo que não se deixa nomear")
    w("")
    w("Unidade **F1.TEMPO** (trilha TEMPO) da gerência c1, programa IALD (a TGL). Autor: o pré-registrador, subagente do workflow posto-e-tempo da c1. Montado em %s (UTC), 12/10/2026." % d["montado_em_utc"])
    w("")
    w("**Estatuto:** " + d["estatuto_do_documento"] + " Este .md é a leitura integral do pré-registro; as assinaturas Lean completas, os reusos, as âncoras com linha, as consultas e a lista integral de fontes estão em `PREREGISTRO.json`, congelado no mesmo `FREEZE.json`. Onde este .md abrevia, diz que abrevia.")
    w("")
    w("**Régua:** " + " · ".join(d["regua"]) + ".")
    w("")
    w("**Dois regimes:** " + d["regra_dos_dois_regimes"])
    w("")
    w("**Objeto:** " + d["objeto"] + " A cunhagem é do operador. Um PASSA será validade matemática na face testada; a confirmação que a régua recusa é a creditação, não a validade (excerto S1). Nada aqui move o gate.")
    w("")
    w("## 1. Verbatins citados (sha256 por script)")
    w("")
    t = d["texto_do_operador"]
    w("**12/10 (o objeto):** `%s` — %d B, sha256 `%s`, %d CRLF (o sha16 `2c8b7b712aa9ad7f` da gerência confere). Segunda parte: byte %d, %d B, sha256 `%s` (linhas %s). Segmentação: %s. As 23 frases (sha16): %s." % (
        t["arquivo"], t["bytes"], t["sha256"], t["crlf"], t["segunda_parte"]["byte_offset"], t["segunda_parte"]["bytes"],
        t["segunda_parte"]["sha256"], t["segunda_parte"]["linhas"], t["regra_de_segmentacao"],
        " · ".join("%s `%s`" % (f["id"], f["sha256"][:16]) for f in t["frases"])))
    w("")
    w("**Excertos do cânone** (cada um achado byte a byte; sha16 do excerto):")
    w("")
    for v in d["verbatins_citados"]:
        w("- **%s** — `%s` (%d B, sha256 `%s`; %s). %s" % (v["id"], v["arquivo"], v["bytes"], v["sha256"], v["data"], v["estatuto"]))
        for e in v["excertos"]:
            w("  - %s (l.%d, `%s`): «%s»" % (e["id"], e["linha"], e["sha256"][:16], e["texto"]))
    w("")
    w("## 2. Mapeamento: cada frase para um objeto matemático, ou [ONTO]")
    w("")
    w("Nenhuma frase fica sem marca (o montador recusa se faltar). Cláusula a cláusula:")
    w("")
    for m in d["mapeamento_frases"]:
        w("**%s** «%s»" % (m["frase"], m["texto"]))
        w("")
        for c in m["clausulas"]:
            ts = (" → " + ", ".join(c["testes"])) if c["testes"] else ""
            w("- *%s* — %s **%s**%s" % (c["trecho"].replace("**", ""), c["objeto_ou_leitura"], c["marca"], ts))
        w("")
    w("**Excertos do cânone, marca e papel:**")
    w("")
    for e in d["mapeamento_excertos"]:
        ts = (" (→ " + ", ".join(e["testes"]) + ")") if e["testes"] else ""
        w("- %s **%s** %s%s" % (e["excerto"], e["marca"], e["objeto_ou_leitura"], ts))
    w("")
    w("## 3. β em runtime e o modelo ótico")
    w("")
    b = d["beta"]
    w("`ALPHA_FINE_CODATA_2018 = %s` lido nos bytes do um.py (l.%d; `BETA_TGL = %s`, l.%s; sha256 `%s`; não executado): β = α·√e = **%s** (diferença à conferência: %s). %s" % (
        b["alpha_literal"], b["linha_alpha"], b["expressao_beta_no_um_py"], b["linha_beta_tgl"], b["um_py_sha256"],
        repr(b["beta_runtime"]), repr(b["diferenca_abs"]), b["estatuto"]))
    w("")
    rotulos = dict(S="S", H_ot="H_ot", D="D", C="C", rho1="ρ₁", davies="Davies", sementes="Sementes", regra="Regra")
    for k in ("S", "H_ot", "D", "C", "rho1", "davies", "sementes", "regra"):
        w("- **%s.** %s" % (rotulos[k], d["modelo_otico"][k]))
    w("")
    n = d["numeros_de_conferencia"]
    w("Conferência (nunca motor): λ = %s; a = %s; 2a = %s; θ_M = %s; ω₁ = %s; P₁ = %s; g₀₁ = %s; λ⁴⁰⁹⁶ = %s; k em que o posto numérico cai = %s; k em que o contraste fica < 1e−15 = %s." % (
        fmt(n["lam"]), fmt(n["a"]), fmt(n["dois_a"]), fmt(n["theta_M"]), fmt(n["omega1"]), fmt(n["P1"]), fmt(n["g01"]),
        fmt(n["lam4096"]), n["k_rank_drop"], n["k_float_floor"]))
    w("")
    w("## 4. As afirmações testáveis")
    w("")
    for a in d["afirmacoes"]:
        w("### %s — %s" % (a["id"], a["titulo"]))
        w("")
        w("Frases: %s. Estatuto: %s." % (", ".join(a["frases"]), a["estatuto"]))
        w("")
        for s in a["subitens"]:
            partes = ["**%s** (%s, %s). %s" % (s["id"], s["face"], "obrigatório" if s["obrigatorio"] else "opcional", s["enunciado"])]
            if "procedimento" in s:
                partes.append("Procedimento: " + s["procedimento"])
            if "lean_alvo" in s:
                partes.append("Lean-alvo: " + lean_names(s["lean_alvo"]) + " (assinaturas no JSON).")
            if "citacoes" in s:
                partes.append("Citações: " + " | ".join(s["citacoes"]) + ".")
            if "consulta_kernel" in s:
                partes.append("Consulta ao kernel: " + s["consulta_kernel"])
            if "vizinhos_no_kernel" in s:
                partes.append("Vizinhos no kernel: " + s["vizinhos_no_kernel"])
            partes.append("Tolerância: %s. Falsificador: %s. Esperado: **%s**." % (s["tolerancia"], s["falsificador"], s["esperado"]))
            w("- " + " ".join(partes))
        w("")
        w("Controles: %s. Sondas: %s. Não afirma: %s." % (", ".join(a["controles"]), ", ".join(a["sondas"]), "; ".join(a["nao_afirma"])))
        w("")
    w("## 5. Controles que têm de falhar (e bordas registradas)")
    w("")
    for c in d["controles"]:
        w("- **%s** (%s; %s): %s Esperado: %s." % (c["id"], c["face"], c["liga"], c["enunciado"], c["esperado"]))
    w("")
    w("## 6. Sondas de vacuidade da pedra")
    w("")
    for s in d["sondas_de_vacuidade"]:
        w("- **%s** (%s): %s" % (s["id"], s["liga"], s["enunciado"]))
    w("")
    p = d["pedra"]
    w("## 7. A pedra: %s" % p["nome_provisorio"])
    w("")
    w("%s Arquivo: %s; namespace `%s`. Importações permitidas: %s. Proibidas: %s." % (
        p["nota_nome"], p["arquivo"], p["namespace"], "; ".join(p["importacoes_permitidas"]), "; ".join(p["importacoes_proibidas"])))
    w("")
    w("**Convenções:** " + p["convencoes"])
    w("")
    w("**Deve provar:** " + " · ".join(p["deve_provar"]) + ".")
    w("")
    w("**Não deve afirmar:** " + " · ".join(p["nao_deve_afirmar"]) + ".")
    w("")
    w("**Critérios:** " + "; ".join(p["criterios"]) + ".")
    w("")
    r = d["regra_de_decisao"]
    w("## 8. Regra de decisão")
    w("")
    for k, v in r["vereditos_por_subitem"].items():
        w("- **%s** — %s" % (k, v))
    w("")
    w("**Por afirmação:** " + r["por_afirmacao"])
    w("")
    w("**Global:** " + r["global_"] + " **Mudanças:** " + r["mudancas"] + " **Entrada no um.py:** " + r["entrada_no_um_py"])
    w("")
    w("## 9. Riscos")
    w("")
    for x in d["riscos_novos"]:
        w("- **%s** %s" % (x["id"], x["texto"]))
    w("")
    w("Do levantamento (por referência; texto em `0_LEVANTAMENTO/DEFINICOES.json → riscos`): " +
      "; ".join("%s %s" % (x["id"], x["titulo"]) for x in d["riscos_do_levantamento"]) + ".")
    w("")
    w("## 10. Não refazer")
    w("")
    for x in d["nao_refazer"]:
        w("- " + x)
    w("")
    w("## 11. Regras do ensaio")
    w("")
    for x in d["regras_do_ensaio"]:
        w("- " + x)
    w("")
    w("## 12. O cético aferidor: o que se consultou")
    w("")
    cm = d["consultas"]["mapa_de_rotas"]
    zero = [c["consulta"] for c in cm["consultas_deste_preregistro"] if not c["n"]]
    com = ["%s (%s)" % (c["consulta"], "; ".join(c["rotas"][:4]) + ("…" if len(c["rotas"]) > 4 else "")) for c in cm["consultas_deste_preregistro"] if c["n"]]
    w("**Mapa de rotas** (livro sha256 `%s`, cabeça `%s`, %s registros; só `consultar`/`ver`; nada registrado). 14 consultas novas (as 24 do levantamento não se repetem; RESUMO delas `%s`). Sem rota alguma: %s. Com rotas, nenhuma sobre o objeto destas afirmações: %s. Rotas lidas com `ver`: %s." % (
        cm["livro"]["sha256"][:16], cm["consultas_deste_preregistro"][0]["cabeca"], cm["consultas_deste_preregistro"][0]["n_registros"],
        cm["consultas_do_levantamento"]["sha256"][:16], ", ".join(zero), " · ".join(com), ", ".join(cm["rotas_vistas"])))
    w("")
    ci = d["consultas"]["inventario"]
    w("**Inventário da bancada** (sha256 `%s`, gerado %s): %s." % (ci["sha256"][:16], ci["gerado_em"],
                                                                   "; ".join("%s: %d" % (c["tema"], c["n_arquivos"]) for c in ci["consultas"])))
    w("")
    ak = d["ancoras_kernel"]
    sem = [x["nome"] for x in ak if x["tipo"] in ("theorem", "lemma") and not (x["print_no_Audit"] or x["print_no_proprio_modulo"] or x["medido_no_trio_pelo_levantador"])]
    defs = [x["nome"] for x in ak if x["tipo"] not in ("theorem", "lemma")]
    w("**Kernel:** %d âncoras resolvidas por script (tipo, arquivo, linha, sha16; tabela no JSON), todas em módulos do build. Achados que LEVANTAMENTO.md e DEFINICOES.json não listaram (RP13): `purity_unitary_invariant`, `dephase_purityR_le` (PageInformation), `dephase_fixed_iff_diagonal` (TheSingularExpectation), `boost_det`/`boost_null_contract` (BisognanoWichmann), `positive_norm_isometry_no_exp_eigenvector`, `characterMultiplier_weyl`, a identificação do atrator ótico I/2 com `absoluteRho`, e o «amor» da tipagem «sacrifício/amor» do dephasing. Teoremas citados sem `#print axioms` em livro nem medição no trio (o ensaio os mede pela pedra): %s. Definições e estruturas citadas (não têm axiomas a medir à parte): %s." % (
        len(ak), ", ".join("`%s`" % x for x in sem), ", ".join("`%s`" % x for x in defs)))
    w("")
    w("**Mathlib** (no `.lake` do Nós): " + ", ".join("`%s` (%s:%d)" % (x["nome"], x["arquivo"], x["linha"]) for x in d["ancoras_mathlib"]) + ".")
    w("")
    ma = d["consultas"]["memoria_acom"]
    w("**Memória ACOM:** %s Recibo: revisão %s, evento `%s`, event_hash `%s`. %s" % (
        ma["protocolo"], ma["recibo_da_projecao"]["revision"], ma["recibo_da_projecao"]["event_id"],
        ma["recibo_da_projecao"]["event_hash"][:16], ma["banco_inalterado"]))
    w("")
    fpk = d["impressao_digital_kernel"]["antes_da_montagem"]
    w("**Impressão digital do tgl_kernel** antes da montagem: %d arquivos, %d B, %d fontes .lean; meta `%s`, src `%s` — %s à final do levantamento." % (
        fpk["files"], fpk["bytes"], fpk["lean_src_files"], fpk["meta_sha256"][:16], fpk["src_sha256"][:16],
        "igual" if d["impressao_digital_kernel"]["iguais"] else "DIFERENTE"))
    w("")
    w("## 13. Fontes-chave (lista integral, com sha256, no JSON)")
    w("")
    for f in d["fontes_conferidas"][:16]:
        w("- %s: `%s` — %d B, sha256 `%s`" % (f["papel"], f["caminho"], f["bytes"], f["sha256"]))
    w("")
    w(d["nada_escrito_fora"])
    w("")
    return "\n".join(o)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail("uso: montar_preregistro.py <beta_conferencia>")
    main(sys.argv[1])
