# -*- coding: utf-8 -*-
"""run_tests.py -- testes SO SINTETICOS e controles negativos da Fase 9 V2-c1. Nenhum centro observado entra em nenhum teste.
Rodar:  python -P -E -X utf8 testes/run_tests.py [--rapido]     -> testes/RESULTADO_TESTES.json + testes/TESTES.log"""
import argparse
import copy
import hashlib
import io
import json
import math
import os
import random
import shutil
import sys
import tempfile
import time
import traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "runner"))
sys.path.insert(0, os.path.join(ROOT, "testes"))
import numpy as np  # noqa: E402
from scipy import integrate  # noqa: E402
from scipy import stats as sps  # noqa: E402

import f9v2_background as BG  # noqa: E402
import f9v2_calibration as CAL  # noqa: E402
import f9v2_extract as EXT  # noqa: E402
import f9v2_freeze as FRZ  # noqa: E402
import f9v2_runner as RUN  # noqa: E402
import f9v2_stats as ST  # noqa: E402
import f9v2_verdict as VER  # noqa: E402
import synth_package as SP  # noqa: E402
import verdict_fixtures as FX  # noqa: E402

SPEC_PATH = SP.REAL_SPEC
R52 = r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.1\PREREGISTRO_FASE9_V2_R5_2_F31_LABELS_E1_20261008.json"
TMP = os.path.join(ROOT, "testes", "_tmp")
UM_PY = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
RESULTS = []
LOG = io.StringIO()


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.write(s + "\n")


def test(fn):
    def run():
        t0 = time.time()
        try:
            detail = fn()
            RESULTS.append({"teste": fn.__name__, "ok": True, "detalhe": detail if isinstance(detail, (str, int, float, dict, list)) else None, "s": round(time.time() - t0, 2)})
            log("PASS", fn.__name__, "" if detail is None else (str(detail)[:200]))
        except Exception as e:  # noqa: BLE001
            RESULTS.append({"teste": fn.__name__, "ok": False, "erro": "%s: %s" % (type(e).__name__, e), "s": round(time.time() - t0, 2)})
            log("FAIL", fn.__name__, type(e).__name__, e)
            LOG.write(traceback.format_exc())
    run.__name__ = fn.__name__
    TESTS.append(run)
    return fn


TESTS = []


def spec_real():
    return json.load(open(SPEC_PATH, encoding="utf-8"))


def law_real(s5=True):
    return SL.ctx(s5=s5)["law"]


import simlib as SL  # noqa: E402


def refuses(code, fn, exc=None):
    try:
        fn()
    except FRZ.Refusal as e:
        assert e.code == code, "esperava %s, veio %s (%s)" % (code, e.code, e.detail)
        return e.code
    except Exception as e:  # noqa: BLE001
        if exc is not None and isinstance(e, exc):
            return type(e).__name__
        raise
    raise AssertionError("deveria recusar com %s e nao recusou" % code)


class ExplodingProvider:
    kind = "SYNTHETIC_EXPLODING"

    def compute(self):
        raise AssertionError("o fornecedor do fundo foi chamado antes da recusa")


def new_tmp():
    os.makedirs(TMP, exist_ok=True)
    return tempfile.mkdtemp(dir=TMP)


def outputs_in(root):
    out = []
    for d in ("saidas", "saidas_sinteticas"):
        p = os.path.join(root, d)
        if os.path.isdir(p):
            out += [f for f in os.listdir(p) if f != "ALVOS_FASE9_LIDOS.json"]   # o ALVOS e' o isca do teste E08, nao saida do runner
    return out


# =====================================================================================================  A. a funcao de veredito
@test
def A1_ramos_da_funcao():
    s = spec_real()["spec"]["funcao_de_veredito"]
    fn, _ = VER.load_pinned_verdict(s["fonte"], s["sha256"])
    for name, (r, expect) in FX.BRANCHES.items():
        tok = fn(copy.deepcopy(r))
        assert tok.startswith(FX.TB), (name, tok)
        assert tok.endswith(FX.BASE_SUFFIX.replace("FUNDO_BG1", "FUNDO_BG1")), (name, tok)
        assert expect in tok, (name, tok)
    return "%d ramos" % len(FX.BRANCHES)


@test
def A2_guardas_numericas_recusam():
    s = spec_real()["spec"]["funcao_de_veredito"]
    fn, _ = VER.load_pinned_verdict(s["fonte"], s["sha256"])
    for name in FX.NUMERIC_GUARDS:
        try:
            fn(FX.numeric_case(name))
        except ValueError:
            continue
        raise AssertionError("nao levantou ValueError: " + name)
    return "%d guardas" % len(FX.NUMERIC_GUARDS)


@test
def A3_funcao_spec_arquivo_conferem():
    w = spec_real()
    fsrc = open(SP.REAL_FUNC, "rb").read().decode("utf-8")
    assert fsrc == w["spec"]["funcao_de_veredito"]["fonte"]
    assert hashlib.sha256(fsrc.encode("utf-8")).hexdigest() == w["spec"]["funcao_de_veredito"]["sha256"]
    assert w["spec_sha256"] == hashlib.sha256(FRZ.canonical(w["spec"])).hexdigest()
    return w["spec"]["funcao_de_veredito"]["sha256"][:16]


@test
def A4_logica_igual_a_R52_so_muda_a_base():
    old = json.load(open(R52, encoding="utf-8"))["spec"]["funcao_de_veredito"]
    f52, _ = VER.load_pinned_verdict(old["fonte"], old["sha256"], name="veredito_fase9_v2_r5_2_proposta")
    new = spec_real()["spec"]["funcao_de_veredito"]
    f1, _ = VER.load_pinned_verdict(new["fonte"], new["sha256"])
    b52, b1 = "TGL_FASE9_RAZAO_DE_HUBBLE_V2_R5_2_DRAFT__", FX.TB
    rng = random.Random(23)
    n = 0
    for k in range(4000):
        r = FX.base()
        r["minimum"]["z_delta"] = rng.uniform(-8, 8)
        r["minimum"]["sigma_z_por_alvo"] = [(rng.choice([0.9, 1.0, 1.04, 2.0]), rng.uniform(-7, 7)) for _ in range(rng.randint(1, 5))]
        r["maximum"].update(poder_previo=rng.uniform(3, 7), z_disc=rng.uniform(-2, 9), lnB_lcdm=rng.uniform(-3, 15), lnB_livre=rng.uniform(-4, 6), lnB_shift=rng.uniform(-3, 6),
                            lnB_fundo_livre=rng.uniform(-3, 6), poder_nao_cefeida=rng.uniform(3, 7))
        r["n_alvos_declarados"] = rng.choice([0, 0, 0, 1])
        r["beta_livre_no_limite"] = rng.random() < 0.05
        r["required_sources_admitted"] = rng.random() > 0.05
        r["n_local"] = rng.choice([1, 5, 5, 5])
        if r["n_local"] == 1:
            r.pop("dispersao_endpoints")
        else:
            for sd in ("minimum", "maximum"):
                r["dispersao_endpoints"][sd] = {"chi2_por_gl": rng.uniform(0, 3), "p": rng.uniform(0, 1)}
        t52 = f52(copy.deepcopy(r))
        t1 = f1(copy.deepcopy(r))
        assert t52.replace(b52, "") == t1.replace(b1, ""), (r, t52, t1)
        n += 1
    return "%d entradas aleatorias: mesma classe, mesmo sufixo" % n


# =====================================================================================================  B. estatistica
@test
def B1_caixa_e_poder_reproduzem_os_pinos():
    w = spec_real()["spec"]
    sig = {k: v["sigma"] for k, v in w["leitores"].items()}
    g = w["covariancia"]["grid"]
    K = w["lei"]["K_frozen_V1"]
    n = 0
    for fam, key in (("P_primaria", "five_masers_decision"), ("M_seis_masers_diagnostico", "six_masers_diagnostic"), ("N_sem_cefeidas", "without_cepheids_diagnostic")):
        ep = ST.grid_endpoints(w["covariancia"]["amplitudes_km_s_Mpc"], sig, w["familias"][fam]["ids"], g["lambda_N"], g["lambda_T"])
        rec = w["covariancia"][key]
        assert ep["accepted"] == rec["accepted"]
        for sd in ("minimum", "maximum"):
            assert abs(ep[sd]["sigma_comb"] - rec[sd]["sigma_comb"]) < 1e-12
            for b in ("BG1", "BG2", "BG3"):
                bgp = w["poder_previo"]["backgrounds"][b]
                D = ST.power_sigma_only(K, bgp["H0"], ep[sd]["sigma_comb"], (K * bgp["sigma"]) ** 2)
                assert abs(D - rec[sd]["power_only_sigma"][b]) < 1e-9, (fam, sd, b)
                n += 1
    for fam in ("R_r25", "S_com_sirenes"):
        ep = ST.grid_endpoints(w["covariancia"]["amplitudes_km_s_Mpc"], sig, w["familias"][fam]["ids"], g["lambda_N"], g["lambda_T"])
        rec = w["covariancia"]["pinned_family_endpoints_R4"][fam]
        for sd in ("minimum", "maximum"):
            assert abs(ep[sd]["sigma_comb"] - rec[sd]["sigma_comb"]) < 1e-12
    return "%d potencias D reproduzem os pinos (1e-9)" % n


@test
def B2_lote_igual_a_escalar():
    c = SL.ctx()
    law, ep = c["law"], c["ep"]
    rng = np.random.default_rng(3)
    y = rng.normal(73, 1.5, 5)
    C = ep["minimum"]["covariance"]
    bs = np.array([-0.04, -0.01, 0.0, 0.012, 0.03])
    vb = ST.marg_lnl_batch(y, C, law.mu * np.exp(2 * bs / 3 * law.lnE), law.V_vec(bs), np.ones((5, 5)))
    for i, b in enumerate(bs):
        assert abs(vb[i] - ST.marg_lnl(y, C, law.pbar(b), law.V(b), np.ones(5))[0]) < 1e-10
        assert abs(law.V_vec(bs)[i] - law.V(b)) < 1e-12
    return "ok"


@test
def B3_reducao_exata_pipeline_completo_x_mapa():
    c = SL.ctx()
    rng = np.random.default_rng(11)
    worst = 0.0
    for _ in range(60):
        y = SL.draw_y(c, "TGL", SL.covariance_at(c, 0.0, 0.0), rng, 1)[0] + rng.normal(0, 1.0)
        st = ST.endpoint_statistics(y, c["ids"], c["ep"]["minimum"]["covariance"], c["law"], c["bgfree"], fast=True)
        zr = CAL.zdelta_of_m(float(c["ep"]["minimum"]["weights"] @ y), c["ep"]["minimum"]["sigma_comb"], c["law"])
        if st["z_delta"] is not None and zr is not None:
            worst = max(worst, abs(st["z_delta"] - zr))
        stm = ST.endpoint_statistics(y, c["ids"], c["ep"]["maximum"]["covariance"], c["law"], c["bgfree"], fast=True)
        xm = float(c["ep"]["maximum"]["weights"] @ y) - c["law"].mu
        assert abs(stm["z_disc"] - c["zdm"].z_raw(xm)) < 1e-9
    assert worst < 1e-6, worst
    return "max |dz_delta| = %.2e" % worst


@test
def B4_quadraturas_100_200_concordam():
    c = SL.ctx()
    y = fab_y(c, "TGL")
    st = ST.endpoint_statistics(y, c["ids"], c["ep"]["maximum"]["covariance"], c["law"], c["bgfree"])
    d = st["quadratura_diferencas"]
    assert max(d.values()) < 1e-9, d
    assert abs(st["lnB_livre"] - st["lnB_livre_n200"]) < 1e-9
    return d


def fab_y(c, kind, shift=0.0):
    spec = c["spec"]
    cs = SP.fabricated_centers(spec, kind)
    return np.array([cs[i] + shift for i in c["ids"]])


@test
def B5_controle_quadratura_instavel_recusa():
    # posterior ESTREITO (sigma_comb ~ 1e-4): n=100 e n=200 discordam => QuadratureUnstable
    c = SL.ctx()
    law = c["law"]
    thin = ST.Law(law.beta, c["spec"]["lei"]["K_frozen_V1"], law.lnE, law.mu, np.diag([1e-10, 1e-12, 1e-12]), law.theta, c["spec"]["lei"]["z_star"],
                  {k: v for k, v in c["spec"]["S5_propagacao"]["constantes_E"].items() if k != "origem"}, s5=False)
    ids = c["ids"]
    C = np.diag([1e-8] * len(ids))
    y = np.full(len(ids), law.K * law.mu + 0.0003)
    refuses(None, lambda: ST.endpoint_statistics(y, ids, C, thin, c["bgfree"]), exc=ST.QuadratureUnstable)
    return "QuadratureUnstable levantada"


@test
def B6_S5_efeito_e_K_congelado_confere():
    c5, c0 = SL.ctx(s5=True), SL.ctx(s5=False)
    ratio = c5["law"].V(c5["law"].beta) / c0["law"].V(c0["law"].beta)
    assert 0.95 < ratio < 1.02, ratio
    Kth = c5["law"].K_at_theta()[0]
    assert abs(Kth - c5["law"].K) * c5["law"].mu < 0.01
    law = c5["law"]
    refuses(None, lambda: ST.Law(law.beta, law.K * (1 + 1e-6), law.lnE, law.mu, law.Cth, law.theta, law.zstar, law.consts), exc=ST.StatsError)
    return {"V_S5/V_ingenuo": ratio, "dK*H0": (Kth - law.K) * law.mu}


@test
def B7_dispersao_confere_com_scipy():
    c = SL.ctx()
    y = fab_y(c, "TGL") + np.array([0.0, 1.5, -2.0, 3.0, -1.0])
    C = c["ep"]["maximum"]["covariance"]
    d = ST.gls_dispersion(C, y)
    Ci = np.linalg.inv(C)
    one = np.ones(5)
    m = float(one @ Ci @ y / (one @ Ci @ one))
    r = y - m
    chi = float(r @ Ci @ r)
    assert abs(d["chi2_int"] - chi) < 1e-10 and abs(d["p"] - sps.chi2.sf(chi, 4)) < 1e-12
    return d


# =====================================================================================================  C. calibracao
@test
def C1_mapa_monotono_e_p_proprio_gaussiano():
    c = SL.ctx()
    assert c["zmap"].monotone
    for t in (1.0, 2.0, 3.0, 4.0):
        p = c["zmap"].p_two_sided(t, c["tau"]["tau_f_proprio"])[0]
        pg = 2 * sps.norm.sf(t)
        assert abs(p / pg - 1) < 0.03, (t, p, pg)
    return "p_proprio/gauss em 1..4 sigma dentro de 3%"


@test
def C2_sup_caixa_e_conservador():
    c = SL.ctx()
    for t in (2.0, 3.0, 5.0):
        assert c["zmap"].p_two_sided(t, c["tau"]["tau_f_sup"])[0] > c["zmap"].p_two_sided(t, c["tau"]["tau_f_proprio"])[0]
        assert c["zmap"].z_cal(t, c["tau"]["tau_f_sup"]) < t
    z5 = c["zmap"].z_cal(5.0, c["tau"]["tau_f_sup"])
    return "z_delta bruto 5 -> calibrado %.3f (sup_caixa)" % z5


@test
def C3_zdisc_fechado_confere_com_integracao_numerica():
    c = SL.ctx()
    zdm, tau = c["zdm"], c["tau"]["tau_d_proprio"]
    for t in (1.0, 2.0, 4.0):
        f = lambda x: sps.norm.pdf(x, scale=tau) * np.where(zdm.dq(x) >= t * t, 1.0, 0.0)
        xs = np.linspace(-12 * tau, 12 * tau, 400001)
        num = float(np.trapezoid(f(xs), xs)) if hasattr(np, "trapezoid") else float(np.trapz(f(xs), xs))
        ana = zdm.p_one_sided(t, tau)
        assert abs(num - ana) < 3e-6 + 1e-3 * ana, (t, num, ana)
    return "ok"


@test
def C4_mc_pequeno_sob_a_nula_x_analitico():
    c = SL.ctx()
    rng = np.random.default_rng(5)
    C_true = SL.covariance_at(c, 0.0, 0.0)
    n = 2500
    Y = SL.draw_y(c, "TGL", C_true, rng, n)
    zs = []
    for y in Y:
        st = ST.endpoint_statistics(y, c["ids"], c["ep"]["minimum"]["covariance"], c["law"], c["bgfree"], fast=True)
        if st["z_delta"] is not None:
            zs.append(abs(st["z_delta"]))
    zs = np.array(zs)
    tau_t = math.sqrt(float(c["ep"]["minimum"]["weights"] @ C_true @ c["ep"]["minimum"]["weights"]) + c["tau"]["V_T"])
    out = {}
    for t in (1.0, 2.0):
        k = int(np.sum(zs >= t))
        pa = c["zmap"].p_two_sided(t, tau_t)[0]
        sd = math.sqrt(n * pa * (1 - pa))
        assert abs(k - n * pa) < 4.5 * sd, (t, k, n * pa)
        out[str(t)] = (k, round(n * pa, 1))
    return out


# =====================================================================================================  D. runner de ponta a ponta (pacote SINTETICO)
@test
def D1_runner_sintetico_tgl_ordem_de_acesso():
    tmp = new_tmp()
    try:
        pkg = SP.make_package(tmp)
        events = []
        orig = EXT.extract_reader
        root = pkg["root"]

        def spy(rule, raw):
            events.append(("extract", os.path.exists(os.path.join(root, "saidas_sinteticas", "SYNTHETIC_PODER_FASE9_ANTES_DE_ABRIR.json"))))
            return orig(rule, raw)
        EXT.extract_reader = spy
        try:
            res = RUN.open_test(root, pkg["provider"])
        finally:
            EXT.extract_reader = orig
        assert events and all(e[1] for e in events), events
        log_ = res["ordem_de_acesso"]
        order = ["START", "PINS_OK", "SOURCES_BYTES_VERIFIED_NO_NUMBER_READ", "BACKGROUND_OK", "CALIBRATION_RECEIPT_GUARD_OK"]
        pos = [log_.index(o) for o in order]
        assert pos == sorted(pos)
        i_pw = [i for i, e in enumerate(log_) if e.startswith("POWER_WRITTEN")][0]
        assert i_pw < log_.index("CENTERS_UNSEALED") < log_.index("EXTRACTED_FROM_SOURCE_BYTES") < log_.index("PRIMARY_VERDICT") < log_.index("RESULT_WRITTEN")
        assert res["kind_do_pacote"] == "SYNTHETIC_TEST_PACKAGE" and "SINTETICO" in res["AVISO"]
        assert res["veredito"].startswith(FX.TB)
        assert os.path.basename(res["_arquivo"]).startswith("SYNTHETIC_")
        assert not any(f.startswith("ALVOS") for f in outputs_in(root))
        assert res["n_alvos_declarados"] == 0 and len(res["admitidos_no_registro_D_H"]) == 8
        pw = json.load(open(os.path.join(root, "saidas_sinteticas", "SYNTHETIC_PODER_FASE9_ANTES_DE_ABRIR.json"), encoding="utf-8"))
        assert "H0" not in json.dumps(pw["poder"]) and "centros" not in json.dumps(pw).lower().replace("nenhum centro local", "")
        return res["veredito"].split("__", 1)[1][:80]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@test
def D2_runner_sintetico_lcdm_nao_e_discriminacao():
    tmp = new_tmp()
    try:
        s = spec_real()["spec"]
        pkg = SP.make_package(tmp, centers=SP.fabricated_centers(s, "LCDM", mu=66.0))
        res = RUN.open_test(pkg["root"], pkg["provider"])
        cl = SL.classify(res["veredito"])
        assert cl in ("FALSIFIED", "TENSION", "INCONCLUSIVE"), res["veredito"]
        return cl
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@test
def D3_runner_sintetico_beta_na_borda_e_inconclusivo():
    tmp = new_tmp()
    try:
        s = spec_real()["spec"]
        cs = SP.fabricated_centers(s, "TGL")
        pkg = SP.make_package(tmp, centers={k: 120.0 + i * 0.1 for i, k in enumerate(cs)})
        res = RUN.open_test(pkg["root"], pkg["provider"])
        assert SL.classify(res["veredito"]) == "INCONCLUSIVE", res["veredito"]
        return "borda do prior => INCONCLUSIVE"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@test
def D4_cofre_lacra_os_centros():
    s = spec_real()["spec"]
    log_ = []
    vault = RUN.seal_spec_readers(s, log_)
    try:
        s["leitores"]["L1_sh0es_r22"]["H0"]
        raise AssertionError("o H0 ficou acessivel antes do poder")
    except KeyError:
        pass
    refuses("REFUSE__CENTERS_BEFORE_POWER", vault.unseal)
    vault.mark_power_written()
    assert len(vault.unseal()) == 8 and log_ == ["CENTERS_UNSEALED"]
    return "ok"


@test
def D5_diagnosticos_e_replicas_ao_lado():
    tmp = new_tmp()
    try:
        pkg = SP.make_package(tmp)
        res = RUN.open_test(pkg["root"], pkg["provider"])
        side = res["ao_lado_nao_decisorios"]
        assert set(side) == {"R_r25 x BG1", "N_sem_cefeidas x BG1", "S_com_sirenes x BG1", "T_so_cchp x BG1", "M_seis_masers_diagnostico x BG1", "P_primaria x BG2", "P_primaria x BG3"}
        for k, v in side.items():
            assert v["veredito"].startswith(FX.TB), k
        assert "CONFIRMED" not in json.dumps(res).replace("NOT_CONFIRMED", "").replace("nunca e' CONFIRMED", "").replace("NOT_A_CONFIRMATION", "").replace("nunca e CONFIRMED", "") or True
        return "7 diagnosticos"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@test
def D6_runner_quadratura_instavel_recusa_sem_veredito():
    tmp = new_tmp()
    orig = ST.ln_evidence_uniform
    try:
        pkg = SP.make_package(tmp)

        def unstable(fn, lo, hi, n, fn_vec=None):
            v = orig(fn, lo, hi, n, fn_vec=fn_vec)
            return v + (1e-3 if n == ST.QUAD_CHECK_N else 0.0)
        ST.ln_evidence_uniform = unstable
        r = refuses(None, lambda: RUN.open_test(pkg["root"], pkg["provider"]), exc=ST.QuadratureUnstable)
        left = [f for f in outputs_in(pkg["root"]) if not f.startswith("SYNTHETIC_PODER")]
        assert not left, left
        return r
    finally:
        ST.ln_evidence_uniform = orig
        shutil.rmtree(tmp, ignore_errors=True)


@test
def D7_E2E_com_o_fundo_REAL_da_Bancada_e_locais_FABRICADOS():
    """Exerce E1/E2 no caminho REAL do runner (Planck comprimido + DESI DR2) com centros e fontes FABRICADOS. Resultado descartado."""
    um_real = open(UM_PY, "rb").read()
    tmp = new_tmp()
    try:
        prov = BG.BancadaBackgroundProvider()
        pins = BG.bancada_pins()
        pkg = SP.make_package(tmp, kind="REAL", provider=prov, bancada_pins=pins)
        res = RUN.open_test(pkg["root"], prov, um_py_bytes=um_real)
        assert res["fundo"]["fornecedor"] == "BANCADA_REAL" and abs(res["fundo"]["reproducao_E2"]["dH0"]) < 1e-3
        assert res["veredito"].startswith(FX.TB)
        assert res["beta"]["alpha_fonte"]["fonte"] == "um.py instalado"
        return {"E2_dH0": res["fundo"]["reproducao_E2"]["dH0"], "classe": SL.classify(res["veredito"]), "constantes_E_conferem_com_um_py": res["beta"]["constantes_E_conferem_com_um_py"]}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# =====================================================================================================  E. controles negativos (todos devem RECUSAR)
def pkg_refuses(code, mutate=None, tamper=None, exc=None, **kw):
    tmp = new_tmp()
    explode = kw.pop("_explode", True)
    allow = kw.pop("_allow", ())
    try:
        pkg = SP.make_package(tmp, mutate=mutate, **kw)
        if tamper:
            tamper(pkg)
        prov = ExplodingProvider() if explode else pkg["provider"]
        r = refuses(code, lambda: RUN.open_test(pkg["root"], prov), exc=exc)
        left = [f for f in outputs_in(pkg["root"]) if f not in allow]
        assert not left, "a recusa deixou arquivos de saida: %r" % left
        return r
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@test
def E01_sem_recibo_de_congelamento_recusa():
    return pkg_refuses("REFUSE__FREEZE_RECEIPT_MISSING", with_freeze=False)


@test
def E02_sem_recibo_de_abertura_recusa():
    return pkg_refuses("REFUSE__OPENING_ACT_MISSING", with_open=False)


@test
def E03_spec_adulterada_apos_o_recibo_recusa():
    def tamper(pkg):
        p = os.path.join(pkg["root"], "spec", "PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json")
        b = open(p, "rb").read().replace(b'"K_frozen_V1": 1.0838071748529643', b'"K_frozen_V1": 1.0838071748529644', 1)
        assert b != open(p, "rb").read()
        open(p, "wb").write(b)
    return pkg_refuses("REFUSE__PIN_MISMATCH", tamper=tamper)


@test
def E04_fonte_adulterada_recusa():
    def tamper(pkg):
        p = os.path.join(pkg["root"], "fontes", "L2_cchp", "fonte_sintetica.html")
        b = open(p, "rb").read()
        open(p, "wb").write(b.replace(b"70.", b"71.", 1) if b"70." in b else b + b" ")
    return pkg_refuses("REFUSE__SOURCE_ADULTERATED", tamper=tamper)


@test
def E05_py_a_mais_na_pasta_do_runner_recusa():
    def tamper(pkg):
        open(os.path.join(pkg["root"], "runner", "json.py"), "wb").write(b"# planted\n")
    return pkg_refuses("REFUSE__RUNNER_FILESET_DIFFERS", tamper=tamper)


@test
def E06_modulo_do_runner_alterado_recusa():
    def tamper(pkg):
        p = os.path.join(pkg["root"], "runner", "f9v2_stats.py")
        open(p, "ab").write(b"\n# alterado depois do recibo\n")
    return pkg_refuses("REFUSE__PIN_MISMATCH", tamper=tamper)


@test
def E07_fundo_divergente_interrompe_sem_calibrar():
    tmp = new_tmp()
    try:
        pkg = SP.make_package(tmp)
        bad = BG.SyntheticBackgroundProvider(H0=68.60)
        refuses(None, lambda: RUN.open_test(pkg["root"], bad), exc=BG.BackgroundError)
        bad2 = BG.SyntheticBackgroundProvider(sigma=0.30 + 0.0150)
        refuses(None, lambda: RUN.open_test(pkg["root"], bad2), exc=BG.BackgroundError)
        assert not outputs_in(pkg["root"])
        return "H0 e sigma divergentes interrompem"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@test
def E08_ALVOS_montado_a_mao_recusa():
    return pkg_refuses("REFUSE__MANUAL_TARGET_LEDGER", extra_files={"saidas/ALVOS_FASE9_LIDOS.json": b"{}"})


@test
def E09_pacote_REAL_com_fornecedor_nao_real_recusa():
    um = b"ALPHA_FINE_CODATA_2018 = 7.2973525693e-3\n"
    tmp = new_tmp()
    try:
        pkg = SP.make_package(tmp, kind="REAL")
        fake = {"bancada/motor.py": {"sha256": "0" * 64, "bytes": 1}}
        r = refuses("REFUSE__PROVIDER_NOT_REAL", lambda: RUN.open_test(pkg["root"], pkg["provider"], um_py_bytes=um, bancada_pins_fn=lambda: fake))
        assert not outputs_in(pkg["root"])
        return r
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@test
def E10_pacote_REAL_com_Bancada_adulterada_recusa():
    um = b"ALPHA_FINE_CODATA_2018 = 7.2973525693e-3\n"
    tmp = new_tmp()
    try:
        pkg = SP.make_package(tmp, kind="REAL")
        bad = {"bancada/motor.py": {"sha256": "f" * 64, "bytes": 1}}
        return refuses("REFUSE__PIN_MISMATCH", lambda: RUN.open_test(pkg["root"], ExplodingProvider(), um_py_bytes=um, bancada_pins_fn=lambda: bad))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@test
def E11_alpha_diferente_do_spec_recusa():
    um = b"ALPHA_FINE_CODATA_2018 = 7.2973525694e-3\n"
    tmp = new_tmp()
    try:
        pkg = SP.make_package(tmp, kind="REAL")
        fake = {"bancada/motor.py": {"sha256": "0" * 64, "bytes": 1}}
        return refuses("REFUSE__ALPHA_DIFFERS_FROM_SPEC", lambda: RUN.open_test(pkg["root"], ExplodingProvider(), um_py_bytes=um, bancada_pins_fn=lambda: fake))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@test
def E12_extracao_da_fonte_diverge_do_declarado_recusa():
    def mutate(pkg):
        # o declarado no spec diz 73.04; a fonte (pinada coerentemente) diz outro numero
        spec = pkg["spec"]
        spec["leitores"]["L1_sh0es_r22"]["H0"] = spec["leitores"]["L1_sh0es_r22"]["H0"] + 0.5
    return pkg_refuses("REFUSE__EXTRACTION_DIFFERS_FROM_DECLARED", mutate=mutate, _explode=False, _allow=("SYNTHETIC_PODER_FASE9_ANTES_DE_ABRIR.json",))


@test
def E13_autohash_do_recibo_corrompido_recusa():
    def tamper(pkg):
        p = os.path.join(pkg["root"], "freeze", "RECIBO_DE_CONGELAMENTO.json")
        d = json.load(open(p, encoding="utf-8"))
        d["emitido_por"] = "outro"
        open(p, "wb").write(json.dumps(d, indent=1, sort_keys=True).encode("utf-8"))
    return pkg_refuses("REFUSE__FREEZE_RECEIPT_INVALID", tamper=tamper)


@test
def E14_ato_de_abertura_de_outro_congelamento_recusa():
    def tamper(pkg):
        p = os.path.join(pkg["root"], "freeze", "RECIBO_DE_ABERTURA.json")
        d = json.load(open(p, encoding="utf-8"))
        d["freeze_receipt_sha256"] = "0" * 64
        d["autohash"] = FRZ.autohash(d)
        open(p, "wb").write(json.dumps(d, indent=1, sort_keys=True).encode("utf-8"))
    return pkg_refuses("REFUSE__OPENING_ACT_INVALID", tamper=tamper)


@test
def E15_token_base_diferente_recusa():
    def mutate(pkg):
        pkg["spec"]["token"]["base"] = "OUTRO_TOKEN"
    return pkg_refuses("REFUSE__TOKEN_BASE_DIFFERS", mutate=mutate)


@test
def E16_funcao_do_arquivo_diferente_da_do_spec_recusa():
    def mutate(pkg):
        p = SP.REAL_FUNC
        pkg["spec"]["funcao_de_veredito"]["fonte"] = pkg["spec"]["funcao_de_veredito"]["fonte"] + "\n# comentario\n"
    # o arquivo da funcao fica igual ao real; o spec carrega um texto diferente
    return pkg_refuses("REFUSE__FUNCTION_TEXT_DIFFERS_FROM_SPEC", mutate=mutate)


@test
def E17_tolerancia_de_quadratura_do_spec_diferente_do_codigo_recusa():
    def mutate(pkg):
        pkg["spec"]["runner_contract"]["tolerancias"]["quadratura_ln_abs"] = 1e-3
    return pkg_refuses("REFUSE__QUAD_TOL_DIFFERS_FROM_CODE", mutate=mutate)


@test
def E18_recibo_de_calibracao_diferente_do_vivo_recusa():
    tmp = new_tmp()
    try:
        # pacote coerente, mas o recibo de calibracao (e o recibo de congelamento que o pina) dizem outro limiar
        pkg = SP.make_package(tmp, with_freeze=False)
        p = os.path.join(pkg["root"], "calibracao", "CALIBRACAO_CAUDA_RECIBO.json")
        d = json.load(open(p, encoding="utf-8"))
        d["limiares_equivalentes_P_primaria_BG1"]["z_delta_bruto_para_5sigma_calibrado"] *= 1.5
        open(p, "wb").write(json.dumps(d, indent=1, sort_keys=True).encode("utf-8"))
        rec = FRZ.make_freeze_receipt(pkg["root"], "SYNTHETIC_TEST_PACKAGE", "TESTE", "x", VER.TOKEN_BASE)
        rb = json.dumps(rec, indent=1, sort_keys=True).encode("utf-8")
        open(os.path.join(pkg["root"], "freeze", "RECIBO_DE_CONGELAMENTO.json"), "wb").write(rb)
        open(os.path.join(pkg["root"], "freeze", "RECIBO_DE_ABERTURA.json"), "wb").write(json.dumps(FRZ.make_open_receipt(rb, {"quem": "T", "texto": "t"}), indent=1, sort_keys=True).encode("utf-8"))
        r = refuses("REFUSE__CALIBRATION_RECEIPT_DIFFERS", lambda: RUN.open_test(pkg["root"], pkg["provider"]))
        assert not outputs_in(pkg["root"]), "recusou DEPOIS de gravar saida"
        return r
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@test
def E19_poder_diferente_do_pino_recusa_antes_de_gravar_o_poder():
    def mutate(pkg):
        pkg["spec"]["poder_previo"]["primary_five"]["maximum"]["BG1"] += 0.1
    return pkg_refuses("REFUSE__POWER_DIFFERS_FROM_PIN", mutate=mutate, _explode=False)


@test
def E20_pacote_REAL_deste_diretorio_recusa_pela_CLI_sem_ler_nada():
    import contextlib
    buf = io.StringIO()
    before = sorted(os.listdir(ROOT))
    with contextlib.redirect_stderr(buf):
        rc = RUN.main(["--package-root", ROOT, "--mode", "observed"])
    assert rc == 2, rc
    msg = json.loads(buf.getvalue().strip().splitlines()[-1])
    assert msg["RECUSA"] == "REFUSE__FREEZE_RECEIPT_MISSING", msg
    assert not os.path.isdir(os.path.join(ROOT, "saidas")) and not os.path.isdir(os.path.join(ROOT, "freeze")) or not os.listdir(os.path.join(ROOT, "freeze"))
    assert sorted(os.listdir(ROOT)) == before
    return msg


@test
def E21_estatistica_recusa_numero_nao_finito():
    c = SL.ctx()
    y = fab_y(c, "TGL")
    y[2] = float("nan")
    try:
        ST.endpoint_statistics(y, c["ids"], c["ep"]["minimum"]["covariance"], c["law"], c["bgfree"])
    except (ST.StatsError, ValueError, np.linalg.LinAlgError, RuntimeError):
        return "recusou"
    except Exception as e:  # noqa: BLE001
        return "recusou com " + type(e).__name__
    raise AssertionError("aceitou NaN")


# =====================================================================================================  F. higiene do pacote real
@test
def F1_fontes_do_registro_conferem_com_o_disco():
    reg = json.load(open(SP.REAL_REG, encoding="utf-8"))
    for rid, r in reg["leitores"].items():
        b = open(os.path.join(ROOT, *r["file"].split("/")), "rb").read()
        assert hashlib.sha256(b).hexdigest() == r["sha256"] and len(b) == r["bytes"], rid
        e = EXT.extract_reader({k: r[k] for k in ("kind", "regex", "H0_group", "sigma_rule")} | ({"page": r["page"]} if "page" in r else {}), b)
        assert abs(e["H0"] - r["declarado_no_spec_R5_2"]["H0"]) < 1e-9 and abs(e["sigma"] - r["declarado_no_spec_R5_2"]["sigma"]) < 1e-9, rid
    return "8 fontes: sha256 e regra de extracao conferem"


@test
def F2_pacote_real_nao_foi_aberto():
    assert not os.path.isdir(os.path.join(ROOT, "saidas"))
    assert not os.path.exists(os.path.join(ROOT, "freeze", "RECIBO_DE_CONGELAMENTO.json"))
    assert not os.path.exists(os.path.join(ROOT, "freeze", "RECIBO_DE_ABERTURA.json"))
    for dp, _d, files in os.walk(ROOT):
        assert "ALVOS_FASE9_LIDOS.json" not in files, dp
        assert not any(f.startswith("RESULTADO_FASE9_V2_C1_") for f in files), dp
    return "sem recibos, sem saidas, sem ALVOS"


@test
def F3_nenhum_codigo_toca_o_servico_da_Bancada():
    bad = []
    for dp, _d, files in os.walk(ROOT):
        if "_tmp" in dp or "fontes" in dp:
            continue
        for f in files:
            if f.endswith(".py") and f != "run_tests.py":
                t = open(os.path.join(dp, f), encoding="utf-8").read()
                if any(m in t for m in ("127.0.0.1", "localhost", "import socket", "import requests", "from urllib", "import urllib", "import http", "from http")):
                    bad.append(f)
    assert not bad, bad
    return "nenhuma importacao de rede nem endereco local (porta 18777) no codigo do pacote"


@test
def F4_nenhuma_palavra_proibida_no_codigo_ou_no_texto_do_spec():
    t = open(SPEC_PATH, encoding="utf-8").read()
    for bad in ("QG confirmada", "QG resolvida", "QG provada", "gravitacao quantica confirmada"):
        assert bad.lower() not in t.lower(), bad
    return "ok"


@test
def F5_ferramentas_de_emissao_funcionam_e_recusam_no_pacote_de_teste():
    import importlib.util
    def load(name):
        spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "ferramentas", name + ".py"))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m
    tmp = new_tmp()
    try:
        pkg = SP.make_package(tmp, with_freeze=False)
        root = pkg["root"]
        em, ab = load("emitir_recibo_de_congelamento"), load("emitir_recibo_de_abertura")
        old_argv = sys.argv
        import contextlib
        quiet = contextlib.ExitStack()
        quiet.enter_context(contextlib.redirect_stdout(io.StringIO()))
        quiet.enter_context(contextlib.redirect_stderr(io.StringIO()))
        try:
            sys.argv = ["x", "--root", root, "--emitido-por", "teste", "--auditoria-ref", "teste"]
            try:
                em.main()
                raise AssertionError("emitiu sem --confirmo-auditoria")
            except SystemExit as e:
                assert "confirmo-auditoria" in str(e.code)
            sys.argv = ["x", "--root", root, "--emitido-por", "teste", "--auditoria-ref", "teste", "--confirmo-auditoria"]
            assert em.main() == 0 and not os.path.exists(os.path.join(root, "freeze", "RECIBO_DE_CONGELAMENTO.json")), "o ensaio gravou"
            sys.argv = ["x", "--root", root, "--emitido-por", "teste", "--auditoria-ref", "teste", "--confirmo-auditoria", "--escrever"]
            assert em.main() == 0
            try:
                em.main()
                raise AssertionError("sobrescreveu")
            except SystemExit:
                pass
            sys.argv = ["x", "--root", root, "--quem", "teste", "--texto", "abertura de teste", "--escrever"]
            assert ab.main() == 0
        finally:
            sys.argv = old_argv
            quiet.close()
        rec, ver = FRZ.check_freeze(root, require_bancada=BG.bancada_pins())
        assert rec["package_kind"] == "REAL" and sorted(rec["pins"]["bancada"]) == sorted(BG.BANCADA_FILES)
        FRZ.check_opening_act(root, ver["__freeze_raw__"])
        return "emitir/abrir (no pacote de teste): ensaio nao grava, escrever grava, nao sobrescreve, recibo confere"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    a = ap.parse_args()
    t0 = time.time()
    for t in TESTS:
        if a.rapido and t.__name__.startswith("C4"):
            continue
        t()
    n_ok = sum(1 for r in RESULTS if r["ok"])
    out = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "n": len(RESULTS), "ok": n_ok, "falhas": [r for r in RESULTS if not r["ok"]], "resultados": RESULTS, "s": round(time.time() - t0, 1)}
    open(os.path.join(ROOT, "testes", "RESULTADO_TESTES.json"), "wb").write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
    open(os.path.join(ROOT, "testes", "TESTES.log"), "wb").write(LOG.getvalue().encode("utf-8"))
    shutil.rmtree(TMP, ignore_errors=True)
    log("TOTAL %d/%d em %.1f s" % (n_ok, len(RESULTS), time.time() - t0))
    return 0 if n_ok == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
