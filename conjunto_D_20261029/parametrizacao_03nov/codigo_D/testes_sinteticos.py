# -*- coding: utf-8 -*-
"""testes_sinteticos.py -- testes do estimador, do veredito, da cegueira, do estagio cego, da abertura, do guarda e do desenho C2 em SINTETICO (resposta conhecida).
NENHUM dado real e aberto: so metadados do V1/catalogo/manifesto e numeros sorteados aqui. Roda em Python do Windows (sem bilby). Saida: tabela PASS/FAIL e JSON.
Uso: python -X utf8 testes_sinteticos.py [saida.json]
"""
import copy
import hashlib
import json
import math
import os
import shutil
import sys
import tempfile
import time
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

CODE = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE))
import abrir_D as AB  # noqa: E402
import blinding_D as B  # noqa: E402
import estagio_cego_D as EC  # noqa: E402
import estimador_ramo_b_v1 as E  # noqa: E402
import gerar_jobs_D as J  # noqa: E402
import gerar_pinos_D as GP  # noqa: E402
import guard_D as G  # noqa: E402
import injecao_c2 as I  # noqa: E402
import poder_planejamento as PP  # noqa: E402
import v1_ramo_b as V  # noqa: E402
import veredito_ramo_b as VR  # noqa: E402

RES = []
TMP = Path(tempfile.mkdtemp(prefix="testes_D_"))
V1, V1INFO = V.carregar_v1()
ROWS = V.tabela_eventos(V1)
D10 = V.eventos_d10(V1)
CR = V.criterios_fase6()
K = V.constantes_um_py()
FIT = json.loads(Path(V.native(PP.FIT)).read_text(encoding="utf-8"))
F31 = [f for f in FIT["fits"] if f["population"] == "GWTC5_31"][0]
B0, B1 = F31["coefficients_log_intercept_slope"]
SIG = {e: math.exp(B0 + B1 * math.log(ROWS[e]["SNR_rede_GWOSC"])) for e in D10}
DP = {e: ROWS[e]["delta_pred_exato"] for e in D10}


def teste(nome):
    def deco(f):
        t0 = time.time()
        try:
            detalhe = f()
            RES.append({"teste": nome, "ok": True, "detalhe": detalhe, "s": round(time.time() - t0, 2)})
        except Exception as exc:                                   # noqa: BLE001
            RES.append({"teste": nome, "ok": False, "detalhe": "".join(traceback.format_exception_only(type(exc), exc)).strip(), "s": round(time.time() - t0, 2)})
        return f
    return deco


def _eventos_sinteticos(rng, escala_sigma=1.0, verdade=None, c=(0.0, 0.0), n=10, com_amostras=False):
    """verdade: callable evento->delta verdadeiro. c: vies verdadeiro c0 + kc*sigma."""
    evs, amostras = [], {}
    for e in D10[:n]:
        s = SIG[e] * escala_sigma
        mu = (verdade(e) if verdade else 0.0) + c[0] + c[1] * s
        dh = mu + rng.normal(0, s)
        ev = {"evento": e, "delta_hat": dh, "delta_hat_mediana": dh, "sigma": s, "w90": 3.29 * s, "delta_pred": DP[e]}
        if com_amostras:
            x = rng.normal(dh, s, 4000)
            amostras[e] = x
        evs.append(ev)
    return evs, (amostras if com_amostras else None)


def _fit_c2(rng, J_cls, escala_sigma, c, verdade_cls):
    """J injecoes por classe: recuperado = verdade + c(sigma_j) + ruido; devolve (fit_RG, fit_B)."""
    out = {}
    base = sorted(D10, key=lambda e: ROWS[e]["SNR_rede_GWOSC"])
    for cls in ("GR", "RB"):
        pts = []
        for j in range(J_cls):
            e = base[round((j % 10) * 9 / 9)]
            s = SIG[e] * escala_sigma
            v = verdade_cls(cls, e)
            rec = v + c[0] + c[1] * s + rng.normal(0, s)
            pts.append({"sigma": s, "vies": rec - v, "sigma_vies": s})
        out[cls] = E.ajustar_vies(pts)
    return out["GR"], out["RB"]


# ----------------------------------------------------------------------------------------------- V1 e constantes
@teste("T01 V1 por hash e tabela 'informacao cega' reproduzida (delta_pred, k, N) a 1e-15")
def _():
    mx = 0.0
    for e in D10:
        d, x, k, N = V.previsao_por_spin(ROWS[e]["chi_f_mediana_GR"], K["beta"])
        mx = max(mx, abs(d - ROWS[e]["delta_pred_exato"]), abs(k - ROWS[e]["k_kms"]), abs(N - ROWS[e]["N_a"]))
    assert mx < 1e-15, mx
    assert abs(K["beta"] - V1["spec"]["beta"]["valor_runtime"]) < 1e-15
    return {"max_dif": mx, "beta": K["beta"], "criterios": {k: CR[k] for k in ("min_eventos", "poder_min", "z_excl", "sistematica_max_relativa")}}


# ----------------------------------------------------------------------------------------------- cegueira
(TMP / "guarda" / "priv").mkdir(parents=True, exist_ok=True)
SEMENTE_T = TMP / "guarda" / "priv" / "seed_teste.bin"
SEMENTE_T.write_bytes(os.urandom(32))
COMMIT_T = hashlib.sha256(SEMENTE_T.read_bytes()).hexdigest()
REG_T = {"blinding": {"seed_path": str(SEMENTE_T), "seed_commitment_sha256": COMMIT_T, "offset_half_range": 1.0}}


@teste("T02 cegueira: offset em (-1,1); sigma e W90 invariantes; desvelar devolve o bruto; compromisso errado recusa")
def _():
    rng = np.random.default_rng(1)
    raw = rng.normal(-0.3, 0.33, 5000)
    cols = {"dtau220": raw, "dtau440": np.zeros(5000), "domega220": np.zeros(5000), "domega440": np.zeros(5000)}
    s = B.shifted_samples(cols, "GW230919_215712", REG_T)
    bl = np.array(s["columns"]["blinded_dtau220"])
    off = float(np.mean(bl - raw))
    assert -1 < off < 1 and abs(off) > 1e-6
    assert np.allclose(bl - raw, off, atol=1e-12)
    a, b = B.estatisticas_invariantes(raw), B.estatisticas_invariantes(bl)
    assert abs(a["sigma"] - b["sigma"]) < 1e-12 and abs(a["w90"] - b["w90"]) < 1e-12
    back = B.unblind_samples({"blinded_dtau220": bl}, "GW230919_215712", REG_T)["dtau220"]
    assert np.allclose(back, raw, atol=1e-12)
    off2 = float(np.mean(np.array(B.shifted_samples(cols, "GW240513_183302", REG_T)["columns"]["blinded_dtau220"]) - raw))
    assert abs(off - off2) > 1e-9                                  # offsets por evento diferentes
    ruim = copy.deepcopy(REG_T)
    ruim["blinding"]["seed_commitment_sha256"] = "0" * 64
    try:
        B.shifted_samples(cols, "GW230919_215712", ruim)
        raise AssertionError("compromisso errado deveria recusar")
    except ValueError:
        pass
    return {"offset_exemplo_nao_e_o_real": "(teste com semente de teste, descartada)", "sigma_igual": True}


# ----------------------------------------------------------------------------------------------- estimador / veredito
@teste("T03 estimador calibrado (RG): z_RG ~ N(0,1) com c(sigma)=0,03+0,08*sigma conhecido e medido por C2 (J=25): media~0, desvio em [0,9; 1,1]")
def _():
    rng = np.random.default_rng(2)
    c = (0.03, 0.08)
    zs = []
    for _i in range(1500):
        evs, _ = _eventos_sinteticos(rng, 1.0, None, c)
        fgr, fb = _fit_c2(rng, 25, 1.0, c, lambda cls, e: 0.0 if cls == "GR" else DP[e])
        r = E.estimar(evs, fit_RG=fgr, fit_B=fb)
        zs.append(r["z_RG"])
    zs = np.array(zs)
    assert abs(zs.mean()) < 0.1 and 0.85 < zs.std() < 1.1, (zs.mean(), zs.std())
    return {"media_z_RG": float(zs.mean()), "desvio_z_RG": float(zs.std())}


@teste("T04 estimador calibrado (B verdadeira): z_B ~ N(0,1) e z_excl pequeno")
def _():
    rng = np.random.default_rng(3)
    c = (0.03, 0.08)
    zs = []
    for _i in range(1500):
        evs, _ = _eventos_sinteticos(rng, 1.0, lambda e: DP[e], c)
        fgr, fb = _fit_c2(rng, 25, 1.0, c, lambda cls, e: 0.0 if cls == "GR" else DP[e])
        r = E.estimar(evs, fit_RG=fgr, fit_B=fb)
        zs.append(r["z_B"])
    zs = np.array(zs)
    assert abs(zs.mean()) < 0.1 and 0.85 < zs.std() < 1.1, (zs.mean(), zs.std())
    return {"media_z_B": float(zs.mean()), "desvio_z_B": float(zs.std())}


@teste("T05 sem corrigir o vies (c=0 assumido com vies real 0,05): z_B sai viesado; com C2 corrigido, nao -- o nuisance importa")
def _():
    rng = np.random.default_rng(4)
    c = (0.15, 0.0)
    z_sem, z_com = [], []
    for _i in range(600):
        evs, _ = _eventos_sinteticos(rng, 1.0, lambda e: DP[e], c)
        z_sem.append(E.estimar(evs)["z_B"])
        fgr, fb = _fit_c2(rng, 25, 1.0, c, lambda cls, e: 0.0 if cls == "GR" else DP[e])
        z_com.append(E.estimar(evs, fit_RG=fgr, fit_B=fb)["z_B"])
    assert np.mean(z_sem) > 1.0 and abs(np.mean(z_com)) < 0.2
    return {"media_z_B_sem_C2": float(np.mean(z_sem)), "media_z_B_com_C2": float(np.mean(z_com))}


def _entrada(est, n=10, controles=None, sist=0.1, kde=None):
    ctr = {c: "PASS" for c in ("C1", "C2", "C3", "C5", "C6", "C7", "C8", "C9")}
    ctr["C4"] = "NOT_APPLICABLE"
    ctr.update(controles or {})
    return {"n_eventos": n, "estimador_selado": True, "dado_aberto": True, "controles": ctr, "sist_rel": sist, "chi2_dof": est["chi2_dof"],
            "kde_discordancias": kde, "poder": est["poder"], "z_excl": est["z_excl"], "z_RG": est["z_RG"]}


@teste("T06 'D como A' (verdade +0,072) com o desenho do plano (poder < 5): NOT_FALSIFIED_UNDERPOWERED em ~100 % das 1000 realizacoes (a excecao so pode ser controle reprovado por acaso)")
def _():
    rng = np.random.default_rng(5)
    c = (0.0, 0.0)
    cont = {}
    for _i in range(1000):
        evs, _ = _eventos_sinteticos(rng, 1.0, lambda e: 0.072, c)
        r = E.estimar(evs)
        _, d, _ = VR.veredito(_entrada(r), CR)
        cont[d.split("__POWER")[0]] = cont.get(d.split("__POWER")[0], 0) + 1
    assert cont.get("NOT_FALSIFIED_UNDERPOWERED", 0) >= 995 and set(cont) <= {"NOT_FALSIFIED_UNDERPOWERED", "INCONCLUSIVE_SYSTEMATICS"}, cont
    assert "FALSIFIED_AT_5SIGMA" not in cont and "NOT_FALSIFIED_POWERED" not in cont
    return dict(cont, nota="o INCONCLUSIVE restante e chi2/dof > 3 por acaso (P ~ 0,14 % com 9 gl)")


@teste("T07 com informacao suficiente (sigma x0,45 => poder >= 5): verdade +0,072 => FALSIFIED_AT_5SIGMA; verdade B => NOT_FALSIFIED_POWERED; verdade RG => FALSIFIED (o teste PODE falhar o par)")
def _():
    rng = np.random.default_rng(6)
    out = {}
    for rotulo, ver in (("A_como_+0.072", lambda e: 0.072), ("B_verdadeira", lambda e: DP[e]), ("RG_verdadeira", lambda e: 0.0)):
        cont = {}
        for _i in range(400):
            evs, _ = _eventos_sinteticos(rng, 0.45, ver, (0, 0))
            r = E.estimar(evs)
            _, d, _ = VR.veredito(_entrada(r), CR)
            cont[d] = cont.get(d, 0) + 1
        out[rotulo] = cont
    assert out["A_como_+0.072"].get("FALSIFIED_AT_5SIGMA", 0) >= 390
    assert out["RG_verdadeira"].get("FALSIFIED_AT_5SIGMA", 0) >= 390
    assert sum(v for k, v in out["B_verdadeira"].items() if k.startswith("NOT_FALSIFIED_POWERED")) >= 390
    assert not any(k.startswith("FALSIFIED") for k in out["B_verdadeira"]), out["B_verdadeira"]
    return out


@teste("T08 ordem do veredito (tabela): n=9 -> AWAITING_DATA__INSUFFICIENT_SAMPLE antes de tudo; controle NOT_RUN; FAIL; sist_rel; chi2; discordancia; poder; z_excl; tensao com a RG")
def _():
    base = {"n_eventos": 10, "estimador_selado": True, "dado_aberto": True,
            "controles": {c: "PASS" for c in ("C1", "C2", "C3", "C5", "C6", "C7", "C8", "C9")}, "sist_rel": 0.1, "chi2_dof": 1.0, "kde_discordancias": None,
            "poder": 6.0, "z_excl": 1.0, "z_RG": 1.0}

    def v(**kw):
        e = copy.deepcopy(base)
        for k, val in kw.items():
            if k == "ctr":
                e["controles"].update(val)
            else:
                e[k] = val
        return VR.veredito(e, CR)[1]

    casos = [
        (v(n_eventos=9, poder=9.0, z_excl=9.0), "AWAITING_DATA__INSUFFICIENT_SAMPLE"),
        (v(dado_aberto=False), "AWAITING_DATA"),
        (v(estimador_selado=False), "AWAITING_DATA"),
        (v(ctr={"C2": "NOT_RUN"}), "AWAITING_DATA__CONTROLS_NOT_RUN"),
        (v(ctr={"C1": "FAIL"}, poder=1.0), "INCONCLUSIVE_SYSTEMATICS"),
        (v(sist_rel=0.31, poder=1.0), "INCONCLUSIVE_SYSTEMATICS"),
        (v(chi2_dof=3.01), "INCONCLUSIVE_SYSTEMATICS"),
        (v(kde_discordancias=["h1.0"]), "INCONCLUSIVE_SYSTEMATICS"),
        (v(poder=4.99, z_excl=9.0), "NOT_FALSIFIED_UNDERPOWERED__POWER_4P99_OF_5_SIGMA"),
        (v(poder=5.0, z_excl=5.0), "FALSIFIED_AT_5SIGMA"),
        (v(poder=5.0, z_excl=4.99), "NOT_FALSIFIED_POWERED"),
        (v(poder=6.0, z_excl=1.0, z_RG=5.2), "NOT_FALSIFIED_POWERED__GR_TENSION_REPORTED"),
    ]
    for obt, esp in casos:
        assert obt == esp, (obt, esp)
    toks = [VR.veredito(copy.deepcopy(base), CR)[0]]
    assert toks[0].endswith("__GATE_UNTOUCHED") and "CONFIRMED" not in toks[0] and "PROVED" not in toks[0]
    return {"casos": len(casos), "token_exemplo": toks[0]}


@teste("T09 secundario KDE (3 larguras) concorda com o primario quando a verdade e B ou RG; discordancia sinalizada se amostras forem forcadas ao contrario")
def _():
    rng = np.random.default_rng(7)
    evs, am = _eventos_sinteticos(rng, 0.55, lambda e: DP[e], (0, 0), com_amostras=True)
    r = E.estimar(evs, amostras=am)
    assert r["lnB_primario_B_sobre_RG"] > 0 and all(v > 0 for v in r["lnB_secundario_KDE"].values()) and not r["kde_discordancias"]
    evs2, am2 = _eventos_sinteticos(rng, 0.55, lambda e: 0.0, (0, 0), com_amostras=True)
    r2 = E.estimar(evs2, amostras=am2)
    assert r2["lnB_primario_B_sobre_RG"] < 0 and all(v < 0 for v in r2["lnB_secundario_KDE"].values()) and not r2["kde_discordancias"]
    am3 = {e: rng.normal(DP[e], SIG[e] * 0.55, 4000) for e in D10}      # amostras dizem B; pontos dizem RG
    evs3, _ = _eventos_sinteticos(rng, 0.55, lambda e: 0.0, (0, 0))
    for ev in evs3:
        ev["delta_hat"] = 0.0
    r3 = E.estimar(evs3, amostras=am3)
    assert r3["kde_discordancias"], r3
    return {"lnB_B": r["lnB_primario_B_sobre_RG"], "lnB_RG": r2["lnB_primario_B_sobre_RG"], "discordancia_forcada": r3["kde_discordancias"]}


@teste("T10 C2: avaliacao literal x estatistica -- instrumento PERFEITO reprova por acaso na leitura literal (J=5) e quase nunca na estatistica")
def _():
    rng = np.random.default_rng(8)
    tol = 0.2 * 0.3985
    falha_lit = falha_est = 0
    N = 2000
    for _i in range(N):
        pts = []
        for j in range(5):
            s = SIG[D10[j]]
            pts.append({"sigma": s, "vies": rng.normal(0, s), "sigma_vies": s, "coberto": bool(rng.random() < 0.9)})
        r = E.avaliar_c2({"RB": pts}, tol)["RB"]
        falha_lit += (not r["literal_passa"])
        falha_est += (not r["estatistico_passa"])
    fl, fe = falha_lit / N, falha_est / N
    assert fl > 0.3 and fe < 0.1
    return {"J": 5, "reprova_leitura_literal": fl, "reprova_leitura_estatistica": fe, "tolerancia": tol}


# ----------------------------------------------------------------------------------------------- estagio cego + abertura (pipeline sintetico completo)
def _saida_sintetica(rng, ev, sigma, verdade, escala=1.0, spin=None, n=6000):
    row = ROWS[ev]
    raw = rng.normal(verdade, sigma, n)
    cols = {"dtau220": raw, "dtau440": np.zeros(n), "domega220": np.zeros(n), "domega440": np.zeros(n)}
    s = B.shifted_samples(cols, ev, REG_T)
    a = row["chi_f_mediana_GR"] + rng.normal(0, 0.01, n) if spin is None else spin
    return {"convergence_status": "CONVERGENCE_CRITERIA_MET_REQUIRES_INDEPENDENT_REVIEW", "columns": s["columns"],
            "paired_physical_columns": {"final_spin": a.tolist(), "final_mass_detector": (row["Mf_det_mediana_GR"] + rng.normal(0, 1.0, n)).tolist()}}, raw


def _pipeline(rng, verdade_fn, escala, c2_rb_J=12, c2_gr_J=12, nev=10, tmpdir=None):
    saidas, raws = {}, {}
    for e in D10[:nev]:
        saidas[e], raws[e] = _saida_sintetica(rng, e, SIG[e] * escala, verdade_fn(e))
    return saidas, raws


@teste("T11 estagio cego: so le invariantes; mesmo resultado com OUTRA semente; poder < 5 => veredito_se_mantido = UNDERPOWERED sem olhar o valor central")
def _():
    rng = np.random.default_rng(9)
    s1, _r = _pipeline(rng, lambda e: 0.072, 1.0)
    eg1 = EC.estagio_cego(s1, V1)
    # mesma amostra bruta, OUTRA semente => estagio cego identico (invariante ao offset)
    outra = TMP / "seed2.bin"
    outra.write_bytes(os.urandom(32))
    reg2 = {"blinding": {"seed_path": str(outra), "seed_commitment_sha256": hashlib.sha256(outra.read_bytes()).hexdigest(), "offset_half_range": 1.0}}
    s2 = {}
    for e, s in s1.items():
        bruto = B.unblind_samples({"blinded_dtau220": s["columns"]["blinded_dtau220"]}, e, REG_T)["dtau220"]
        z = np.zeros(len(bruto))
        s2[e] = dict(s, columns=B.shifted_samples({"dtau220": bruto, "dtau440": z, "domega220": z, "domega440": z}, e, reg2)["columns"])
    eg2 = EC.estagio_cego(s2, V1)
    for e in eg1["por_evento"]:
        for k in ("sigma", "w90", "a_PE_mediana", "delta_pred"):
            assert abs(eg1["por_evento"][e][k] - eg2["por_evento"][e][k]) < 1e-9
    assert abs(eg1["primario"]["poder"] - eg2["primario"]["poder"]) < 1e-9
    assert eg1["primario"]["poder"] < 5
    assert eg1["veredito_se_mantido"].split("__SET_D_O4_BLIND__")[1].startswith("NOT_FALSIFIED_UNDERPOWERED")
    assert eg1["controles_avaliaveis_no_estagio_cego"]["C1"] == "PASS"
    # nenhuma chave com media/mediana de dtau220
    txt = json.dumps(eg1)
    assert "media_dtau" not in txt and "delta_hat" not in txt
    # recusa evento nao convergido
    ruim = copy.deepcopy(s1)
    ruim[D10[0]]["convergence_status"] = "PARTIAL_MAXCALL_NOT_ACCEPTED"
    eg3 = EC.estagio_cego(ruim, V1)
    assert D10[0] in eg3["eventos_recusados"] and eg3["n_eventos_convergidos"] == 9 and "INSUFFICIENT_SAMPLE" in eg3["veredito_se_mantido"]
    return {"poder_estagio_cego": eg1["primario"]["poder"], "veredito_se_mantido": eg1["veredito_se_mantido"][-80:], "n9": eg3["veredito_se_mantido"][-60:]}


def _c2_saidas(rng, escala, c, J_cls):
    out = []
    base = sorted(D10, key=lambda e: ROWS[e]["SNR_rede_GWOSC"])
    for cls in ("GR", "RB"):
        for j in range(J_cls):
            e = base[j % 10]
            s = SIG[e] * escala
            ver = 0.0 if cls == "GR" else DP[e]
            mu = ver + c[0] + c[1] * s + rng.normal(0, s)
            out.append({"evento": e, "classe": cls, "verdade": ver, "samples": rng.normal(mu, s, 3000)})
    return out


@teste("T12 abertura sintetica completa (poder<5): autorizacao ligada a hashes; abre UMA vez; sigma desvelado == estagio cego; veredito UNDERPOWERED; 2a abertura e hash errado recusam")
def _():
    rng = np.random.default_rng(10)
    saidas, _raws = _pipeline(rng, lambda e: 0.072, 1.0)
    eg = EC.estagio_cego(saidas, V1)
    d = TMP / "abrir1"
    d.mkdir()
    pod = d / "PODER_REAL.json"
    h_pod = EC.publicar_estagio_cego(eg, pod)
    est_p, ver_p = CODE / "estimador_ramo_b_v1.py", CODE / "veredito_ramo_b.py"
    pinos_dig = "1" * 64
    auth = {"poder_sha256": h_pod, "estimador_sha256": hashlib.sha256(est_p.read_bytes()).hexdigest(), "veredito_sha256": hashlib.sha256(ver_p.read_bytes()).hexdigest(),
            "pinos_sha256": pinos_dig, "ordem_operador_sha256": "2" * 64, "autorizado_utc": datetime.now(timezone.utc).isoformat(),
            "gates": {g: True for g in AB.GATES_OBRIGATORIOS}}
    ap = d / "AUTORIZACAO_ABERTURA_D.json"
    ap.write_text(json.dumps(auth))
    arqs = {"poder": pod, "estimador": est_p, "veredito": ver_p}
    c2 = _c2_saidas(rng, 1.0, (0.02, 0.05), 12)
    res, h = AB.abrir(ap, arqs, pinos_dig, REG_T, saidas, eg, c2, d)
    assert res["desfecho"].startswith("NOT_FALSIFIED_UNDERPOWERED") or res["desfecho"] == "INCONCLUSIVE_SYSTEMATICS", res["desfecho"]
    assert (d / "RESULTADO_RAMO_B_V1.json").exists() and (d / "ABERTURA_D.lock").exists()
    try:
        AB.abrir(ap, arqs, pinos_dig, REG_T, saidas, eg, c2, d)
        raise AssertionError("segunda abertura deveria falhar")
    except FileExistsError:
        pass
    d2 = TMP / "abrir2"
    d2.mkdir()
    auth2 = dict(auth, poder_sha256="f" * 64)
    ap2 = d2 / "A.json"
    ap2.write_text(json.dumps(auth2))
    try:
        AB.abrir(ap2, arqs, pinos_dig, REG_T, saidas, eg, c2, d2)
        raise AssertionError("hash errado deveria recusar")
    except AB.AberturaError:
        pass
    assert not (d2 / "ABERTURA_D.lock").exists()                  # recusou ANTES de travar/abrir
    auth3 = dict(auth, gates=dict(auth["gates"], C2_rodado=False))
    ap3 = d2 / "B.json"
    ap3.write_text(json.dumps(auth3))
    try:
        AB.abrir(ap3, arqs, pinos_dig, REG_T, saidas, eg, c2, d2)
        raise AssertionError("gate falso deveria recusar")
    except AB.AberturaError:
        pass
    return {"desfecho": res["desfecho"], "z_excl": res["estimador"]["z_excl"], "poder": res["estimador"]["poder"], "poder_V1_literal": res["estimador"]["poder_V1_literal"]}


@teste("T13 abertura com poder >= 5 (informacao ~5x: sigma x0,45): D parecido com A (+0,072) => FALSIFIED_AT_5SIGMA do par; D = B => NOT_FALSIFIED_POWERED; C2 reprovado => INCONCLUSIVE; sem C2 => AWAITING (controles nao rodados)")
def _():
    rng = np.random.default_rng(11)
    res_all = {}
    for rotulo, ver in (("A", lambda e: 0.072), ("B", lambda e: DP[e])):
        saidas, _r = _pipeline(rng, ver, 0.45)
        eg = EC.estagio_cego(saidas, V1)
        assert eg["primario"]["poder"] >= 5, eg["primario"]["poder"]
        d = TMP / ("abrir_" + rotulo)
        d.mkdir()
        pod = d / "P.json"
        h_pod = EC.publicar_estagio_cego(eg, pod)
        est_p, ver_p = CODE / "estimador_ramo_b_v1.py", CODE / "veredito_ramo_b.py"
        auth = {"poder_sha256": h_pod, "estimador_sha256": hashlib.sha256(est_p.read_bytes()).hexdigest(), "veredito_sha256": hashlib.sha256(ver_p.read_bytes()).hexdigest(),
                "pinos_sha256": "1" * 64, "ordem_operador_sha256": "2" * 64, "autorizado_utc": datetime.now(timezone.utc).isoformat(), "gates": {g: True for g in AB.GATES_OBRIGATORIOS}}
        ap = d / "A.json"
        ap.write_text(json.dumps(auth))
        c2 = _c2_saidas(rng, 0.45, (0.0, 0.0), 25)
        res, _h = AB.abrir(ap, {"poder": pod, "estimador": est_p, "veredito": ver_p}, "1" * 64, REG_T, saidas, eg, c2, d)
        res_all[rotulo] = res["desfecho"]
    assert res_all["A"] == "FALSIFIED_AT_5SIGMA", res_all
    assert res_all["B"].startswith("NOT_FALSIFIED_POWERED"), res_all           # com __GR_TENSION_REPORTED: B verdadeira se afasta da RG
    # sem C2 => controles nao rodados
    saidas, _r = _pipeline(rng, lambda e: DP[e], 0.45)
    eg = EC.estagio_cego(saidas, V1)
    d = TMP / "abrir_semC2"
    d.mkdir()
    pod = d / "P.json"
    h_pod = EC.publicar_estagio_cego(eg, pod)
    auth = {"poder_sha256": h_pod, "estimador_sha256": hashlib.sha256((CODE / "estimador_ramo_b_v1.py").read_bytes()).hexdigest(),
            "veredito_sha256": hashlib.sha256((CODE / "veredito_ramo_b.py").read_bytes()).hexdigest(), "pinos_sha256": "1" * 64, "ordem_operador_sha256": "2" * 64,
            "autorizado_utc": datetime.now(timezone.utc).isoformat(), "gates": {g: True for g in AB.GATES_OBRIGATORIOS}}
    ap = d / "A.json"
    ap.write_text(json.dumps(auth))
    res, _h = AB.abrir(ap, {"poder": pod, "estimador": CODE / "estimador_ramo_b_v1.py", "veredito": CODE / "veredito_ramo_b.py"}, "1" * 64, REG_T, saidas, eg, [], d)
    assert res["desfecho"] == "AWAITING_DATA__CONTROLS_NOT_RUN", res["desfecho"]
    res_all["sem_C2"] = res["desfecho"]
    # C2 com vies grande (0,5) injetado so em RB e medido mas NAO corrigido pela tolerancia? -> o vies e medido e corrigido; a leitura estatistica reprova se > tol
    c2 = _c2_saidas(rng, 0.45, (0.9, 0.0), 25)
    d = TMP / "abrir_c2ruim"
    d.mkdir()
    (d / "P.json").write_bytes(pod.read_bytes())
    ap = d / "A.json"
    ap.write_text(json.dumps(auth))
    res, _h = AB.abrir(ap, {"poder": d / "P.json", "estimador": CODE / "estimador_ramo_b_v1.py", "veredito": CODE / "veredito_ramo_b.py"}, "1" * 64, REG_T, saidas, eg, c2, d)
    assert res["desfecho"] == "INCONCLUSIVE_SYSTEMATICS", res["desfecho"]
    res_all["C2_com_vies_grande"] = res["desfecho"]
    return res_all


# ----------------------------------------------------------------------------------------------- planejamento
@teste("T14 poder de planejamento reproduz o plano de 29/10 (D10 3,73-3,93; D14 4,39-4,64) e o efeito do vies C2")
def _():
    out, raw = PP.gerar()
    p = out["poder_sem_incerteza_do_vies"]
    d10 = [v["poder"] for k, v in p.items() if k.startswith("D10") and "0.000" not in k.split("__")[1]]
    d14 = [v["poder"] for k, v in p.items() if k.startswith("D14") and "0.000" not in k.split("__")[1]]
    assert 3.72 <= min(d10) and max(d10) <= 3.94 and 4.38 <= min(d14) and max(d14) <= 4.65, (min(d10), max(d10), min(d14), max(d14))
    b = out["poder_com_incerteza_do_vies_D10"]["sigma_sys_0.038__info_mediana"]
    assert b["C2_minima_10PE_J5_por_classe"]["poder"] < b["C2_media_20PE_J10_por_classe"]["poder"] < b["C2_ampla_50PE_J25_por_classe"]["poder"] < b["sem_vies"]["poder"] < 5
    return {"D10": [round(min(d10), 2), round(max(d10), 2)], "D14": [round(min(d14), 2), round(max(d14), 2)],
            "com_vies_sigma_sys_0.038_mediana": {k: round(v["poder"], 2) for k, v in b.items()}}


# ----------------------------------------------------------------------------------------------- guarda
def _guarda_de_teste():
    """Pinos/relogio/jobs em pasta temporaria; semente de teste; sem tocar os oficiais."""
    base = TMP / "guarda"
    base.mkdir(exist_ok=True)
    G.PINOS, G.RELOGIO, G.JOBS, G.CONGELAMENTO = base / "PINOS.json", base / "RELOGIO.json", base / "JOBS.json", base / "CONG.json"
    G.PRIV, G.SAIDAS = base / "priv", base / "priv" / "pe"
    G.SAIDAS.mkdir(parents=True, exist_ok=True)
    B.SEMENTE_PADRAO = str(SEMENTE_T)
    pinos, h = GP.montar(destino=G.PINOS)
    return pinos, h


def _abrir_relogio(prazo=21, agora=None):
    ordem = TMP / "ORDEM_LANC.json"
    ordem.write_text(json.dumps({"opcao": "c", "ordem_operador_sha256": "3" * 64, "decidido_utc": "2026-11-03T00:00:00Z"}))
    if G.RELOGIO.exists():
        G.RELOGIO.unlink()
    return G.abrir_relogio(prazo, ordem, agora=agora)


@teste("T15 guarda: sem relogio recusa; com relogio novo aceita; relogio vencido, no futuro e ligado a outros pinos recusam")
def _():
    pinos, h = _guarda_de_teste()
    try:
        G.checked_registration()
        raise AssertionError("sem relogio deveria recusar")
    except G.GuardError:
        pass
    _abrir_relogio()
    reg, dig = G.checked_registration()
    assert dig == h and len(reg["eventos_d10"]) == 10
    # vencido
    _abrir_relogio(prazo=1, agora=datetime.now(timezone.utc) - timedelta(days=3))
    try:
        G.time_guard()
        raise AssertionError("vencido deveria recusar")
    except TimeoutError:
        pass
    # futuro
    _abrir_relogio(prazo=1, agora=datetime.now(timezone.utc) + timedelta(days=2))
    try:
        G.time_guard()
        raise AssertionError("futuro deveria recusar")
    except G.GuardError:
        pass
    # ligado a outros pinos
    _abrir_relogio()
    r = json.loads(G.RELOGIO.read_text())
    r["pinos_sha256"] = "0" * 64
    G.RELOGIO.write_text(json.dumps(r))
    try:
        G.time_guard()
        raise AssertionError("pinos errados deveriam recusar")
    except G.GuardError:
        pass
    _abrir_relogio()
    return {"pinos_sha16": h[:16], "relogio": "novo, 21 dias, ligado aos pinos"}


@teste("T16 guarda: evento com hold/pendente/fora de D10 recusa em qualquer modo; semente adulterada recusa o modo cego")
def _():
    pinos, h = _guarda_de_teste()
    _abrir_relogio()
    reg, dig = G.checked_registration()
    for ev in list(pinos["eventos_holds_FORA"]) + list(pinos["eventos_pendentes_FORA"]) + ["GW150914", "GW250114_082203"]:
        for modo in G.MODOS:
            try:
                G.authorize_event(reg, ev, modo)
                raise AssertionError("evento fora de D10 aceito: " + ev)
            except G.GuardError:
                pass
    try:
        G.authorize_event(reg, D10[0], "outro")
        raise AssertionError("modo desconhecido aceito")
    except G.GuardError:
        pass
    assert G.authorize_event(reg, D10[0], "blind_test") and G.authorize_event(reg, D10[0], "calibration")
    reg2 = copy.deepcopy(reg)
    reg2["blinding"]["seed_commitment_sha256"] = "0" * 64
    try:
        G.authorize_event(reg2, D10[0], "blind_test")
        raise AssertionError("semente adulterada aceita")
    except G.GuardError:
        pass
    return {"fora": len(pinos["eventos_holds_FORA"]) + len(pinos["eventos_pendentes_FORA"]) + 2}


@teste("T17 guarda: V1 adulterado, arvore de codigo alterada, GPS/strain divergentes do manifesto, copia RO alterada => recusa")
def _():
    pinos, h = _guarda_de_teste()
    _abrir_relogio()
    G.checked_registration()
    orig_tree, orig_copias = G.arvore_de_codigo, G.copias_ro
    try:
        G.arvore_de_codigo = lambda: dict(orig_tree(), **{"guard_D.py": "0" * 64})
        try:
            G.checked_registration()
            raise AssertionError("codigo alterado aceito")
        except G.GuardError:
            pass
    finally:
        G.arvore_de_codigo = orig_tree
    try:
        G.copias_ro = lambda: dict(orig_copias(), **{"injection_design.py": "0" * 64})
        try:
            G.checked_registration()
            raise AssertionError("copia RO alterada aceita")
        except G.GuardError:
            pass
    finally:
        G.copias_ro = orig_copias
    # pino de strain adulterado
    p = json.loads(G.PINOS.read_text())
    ev = D10[0]
    p["eventos"][ev]["strain"]["H1"]["hdf5_sha256"] = "0" * 64
    G.PINOS.write_text(json.dumps(p))
    _abrir_relogio()                                              # religa o relogio aos pinos adulterados para isolar o teste
    try:
        G.checked_registration()
        raise AssertionError("pino de strain adulterado aceito")
    except G.GuardError:
        pass
    # GPS adulterado
    pinos, h = _guarda_de_teste()
    p = json.loads(G.PINOS.read_text())
    p["eventos"][ev]["GPS"] += 1.0
    G.PINOS.write_text(json.dumps(p))
    _abrir_relogio()
    try:
        G.checked_registration()
        raise AssertionError("GPS adulterado aceito")
    except G.GuardError:
        pass
    # V1: hash de arquivo-pino divergente
    pinos, h = _guarda_de_teste()
    _abrir_relogio()
    orig_json = V.V1_JSON
    alt = TMP / "V1_alterado.json"
    alt.write_bytes(Path(V.native(orig_json)).read_bytes() + b" ")
    V.V1_JSON = str(alt).replace(chr(92), "/")
    try:
        try:
            G.checked_registration()
            raise AssertionError("V1 alterado aceito")
        except V.V1Error:
            pass
    finally:
        V.V1_JSON = orig_json
    return {"recusas": 5}


@teste("T18 desenho C2 (3 tamanhos): janelas >=76 s antes do evento, dentro da corrida limpa, GR/RB pareados, dtau220 = 0 ou delta_pred do V1, massas dentro do prior, truth suportada")
def _():
    pinos, h = _guarda_de_teste()
    dq = json.loads(Path("C:/IALD/Central de Patentes/work/conjunto_D_20261029/smoke/dq_meta_D_v2.json").read_text())
    res = {}
    for t, n in (("minima", 10), ("media", 20), ("ampla", 50)):
        d = I.desenho_c2(pinos, dq, t)
        assert d["n_PE"] == n and d["n_por_classe"]["GR"] == d["n_por_classe"]["RB"] == n // 2
        for x in d["injecoes"]:
            assert x["termina_antes_do_evento_s"] >= 76, x["termina_antes_do_evento_s"]
            assert all(x["janela_dentro_da_corrida_limpa"].values())
            e = pinos["eventos"][x["evento"]]
            p = x["parameters"]
            assert p["dtau220"] == (0.0 if x["classe"] == "GR" else e["delta_pred_pinado"])
            assert p["dtau440"] == p["domega220"] == p["domega440"] == 0.0
            assert x["target_network_optimal_SNR"] == e["snr_rede"]
            pri = G.priors_do_evento({"eventos": pinos["eventos"]}, x["evento"], p["geocent_time"])
            I.validate_truth_support_D(p, pri)
        por = {}
        for x in d["injecoes"]:
            por.setdefault((x["evento"], x["replica"]), {})[x["classe"]] = x["segment_start_GPS"]
        assert all(set(v) == {"GR", "RB"} and v["GR"] == v["RB"] for v in por.values()), "GR/RB nao pareadas na mesma janela"
        res[t] = {"n_PE": d["n_PE"], "eventos": len(d["eventos"])}
    # fixo != verdade => recusa
    x = I.desenho_c2(pinos, dq, "minima")["injecoes"][0]
    ruim = dict(x["parameters"], dtau440=0.1)
    try:
        I.validate_truth_support_D(ruim, G.priors_do_evento({"eventos": pinos["eventos"]}, x["evento"], x["parameters"]["geocent_time"]))
        raise AssertionError("parametro fixo divergente aceito")
    except ValueError:
        pass
    return res


@teste("T19 jobs (cegos + C2 media): validate_job_D do guarda E validate_config do pe_runner ORIGINAL aprovam; jobs ruins (prior, janela, injecao em cego, dtau220, strain) recusam")
def _():
    pinos, h = _guarda_de_teste()
    _abrir_relogio()
    reg, dig = G.checked_registration()
    dq = json.loads(Path("C:/IALD/Central de Patentes/work/conjunto_D_20261029/smoke/dq_meta_D_v2.json").read_text())
    d = I.desenho_c2(pinos, dq, "media")
    jobs = J.construir(reg, d)
    assert len(jobs) == 10 + 20
    for nome, cfg in jobs.items():
        G.validate_job_D(reg, nome, cfg)
    J.validar_com_pe_runner(jobs)
    nome_cego = "D_" + D10[0]
    ruins = {}

    def tenta(rotulo, nome, mut):
        cfg = copy.deepcopy(jobs[nome])
        mut(cfg)
        try:
            G.validate_job_D(reg, nome, cfg)
        except (G.GuardError, KeyError):
            ruins[rotulo] = "recusado"
            return
        raise AssertionError("job ruim aceito: " + rotulo)

    tenta("prior_distancia_antiga", nome_cego, lambda c: c["priors"]["luminosity_distance"].update(maximum=2000.0))
    tenta("janela_cega_deslocada", nome_cego, lambda c: c.__setitem__("segment_start_GPS", c["segment_start_GPS"] - 24))
    tenta("injecao_em_job_cego", nome_cego, lambda c: c.__setitem__("injection", {"family": "pSEOBNRv4HM_PA", "noise_kind": "REAL_OFFSOURCE"}))
    tenta("deformacao_440_livre", nome_cego, lambda c: c["priors"].__setitem__("dtau440", {"kind": "Uniform", "minimum": -0.8, "maximum": 2.0}))
    tenta("strain_sha_errado", nome_cego, lambda c: c["data"]["H1"].__setitem__("onsource_sha256", "0" * 64))
    tenta("strain_fora_da_raiz", nome_cego, lambda c: c["data"]["H1"].__setitem__("onsource_path", "C:/Windows/System32/x.hdf5"))
    nome_c2 = next(n for n in jobs if n.startswith("C2_"))
    tenta("C2_janela_encosta_no_evento", nome_c2, lambda c: c.__setitem__("segment_start_GPS", c["event_GPS"] - 30.0))
    tenta("C2_dtau220_arbitrario", nome_c2, lambda c: c["injection"]["parameters"].__setitem__("dtau220", 0.123))
    tenta("C2_ruido_nao_e_offsource_real", nome_c2, lambda c: c["injection"].__setitem__("noise_kind", "GAUSSIAN"))
    tenta("C2_snr_alvo_diferente", nome_c2, lambda c: c["injection"].__setitem__("target_network_optimal_SNR", 99.0))
    tenta("workers_acima_do_teto", nome_cego, lambda c: c["sampler"].__setitem__("workers", 40))
    tenta("evento_com_hold", nome_cego, lambda c: c.__setitem__("event", pinos["eventos_holds_FORA"][0]))
    return {"jobs_bons": len(jobs), "recusas": len(ruins)}


@teste("T20 canonico (C1): |z_A - z_RG| << 1e-30 com M_f,det de D; controle e reprovavel se a previsao canonica for 'ligada' (x sem o fator m_Planck/M_f)")
def _():
    s = np.array([SIG[e] for e in D10])
    w = 1 / (s ** 2 + 0.038 ** 2)
    mf = np.array([ROWS[e]["Mf_det_mediana_GR"] for e in D10]) * V.MSUN
    x = np.array([V.previsao_por_spin(ROWS[e]["chi_f_mediana_GR"], K["beta"])[1] for e in D10])
    c1 = E.controle_C1(w, mf, x, 1 / math.sqrt(w.sum()), K)
    assert c1["passa"] and c1["abs_zA_menos_zRG"] < 1e-30
    c1b = E.controle_C1(w, mf, x, 1 / math.sqrt(w.sum()), dict(K, m_planck=K["m_planck"] * 1e38))
    assert not c1b["passa"]
    return {"abs_zA_menos_zRG": c1["abs_zA_menos_zRG"]}


# ----------------------------------------------------------------------------------------------- pecas da opcao (c): derivadas, sinteticos, congelamento, D5, estagio cego da fila
import ast  # noqa: E402
import congelar_D as CG  # noqa: E402
import estagio_cego_fila_D as EF  # noqa: E402
import lancar_fila_D as L  # noqa: E402
import orquestrador_fila_D as OQ  # noqa: E402
import consultar_fila_D as CQ  # noqa: E402

MAN_SINT = CODE.parent / "SINTETICO_F41_MANIFESTO.json"
CRITERIO_OK = "CONVERGENCE_CRITERIA_MET_REQUIRES_INDEPENDENT_REVIEW"


def _env_com_sinteticos(nome="env"):
    """Pinos/relogio em pasta temporaria COM o evento sintetico (arquivos pequenos falsos, sha256 certo; parametros de injecao do manifesto real)."""
    base = TMP / nome
    (base / "priv" / "sintetico").mkdir(parents=True, exist_ok=True)
    G.PINOS, G.RELOGIO, G.JOBS, G.CONGELAMENTO = base / "PINOS.json", base / "RELOGIO.json", base / "JOBS.json", base / "CONG.json"
    G.PRIV, G.SAIDAS = base / "priv", base / "priv" / "pe"
    G.SAIDAS.mkdir(parents=True, exist_ok=True)
    man = json.loads(MAN_SINT.read_text(encoding="utf-8"))
    for det in ("H1", "L1"):
        f = base / "priv" / "sintetico" / ("SYN_%s.hdf5" % det)
        f.write_bytes(os.urandom(2048))
        man["strain"][det] = {"hdf5": str(f).replace(chr(92), "/"), "hdf5_bytes": 2048, "hdf5_sha256": hashlib.sha256(f.read_bytes()).hexdigest()}
    mp = base / "MANIFESTO_SINT.json"
    mp.write_text(json.dumps(man))
    sem = base / "priv" / "seed.bin"
    shutil.copyfile(SEMENTE_T, sem)
    B.SEMENTE_PADRAO = str(sem)
    pinos, h = GP.montar(destino=G.PINOS, sinteticos_manifesto=str(mp))
    return pinos, h


@teste("T21 pecas derivadas: pe_runner_D/run_controlled_D = copia RO + SO as substituicoes enumeradas (reconstituicao exata); sintaxe valida")
def _():
    sys.path.insert(0, str(CODE.parent))
    import derivar_pecas_mecanicas as DP
    d = CODE.parent
    for nome_orig, nome_der, subst in (("pe_runner.py", "pe_runner_D.py", DP.SUBST_PE), ("run_controlled.py", "run_controlled_D.py", DP.SUBST_RC)):
        orig = (d / "copias_somente_leitura" / nome_orig).read_text(encoding="utf-8")
        der = (CODE / nome_der).read_text(encoding="utf-8")
        ast.parse(der)
        t = orig
        for old, new, n in subst:
            assert t.count(old) == n
            t = t.replace(old, new)
        assert der.endswith(t), nome_der
        extra = der[: len(der) - len(t)]
        assert all(l.startswith("#") for l in extra.splitlines()), "cabecalho so de comentarios"
        assert "import registration_guard" not in der and "from registration_guard" not in der
    return {"arquivos": 2, "substituicoes": len(DP.SUBST_PE) + len(DP.SUBST_RC)}


@teste("T22 sinteticos no guarda: SYN_F41 so em mode=calibration; blind_test recusa; job sintetico valido; job com strain real, dtau220 != 0, janela encostada, SNR diferente, parede acima do teto e arquivo adulterado recusam")
def _():
    pinos, h = _env_com_sinteticos("env22")
    _abrir_relogio()
    reg, dig = G.checked_registration()
    assert "SYN_F41" in reg["sinteticos"] and "SYN_F41" in reg["calibration_event_ids"] and reg["event_reference_GPS"]["SYN_F41"] == reg["sinteticos"]["SYN_F41"]["GPS"]
    assert G.authorize_event(reg, "SYN_F41", "calibration")
    try:
        G.authorize_event(reg, "SYN_F41", "blind_test")
        raise AssertionError("sintetico em blind_test aceito")
    except G.GuardError:
        pass
    reg = dict(reg, limites={"wall_max_por_job_s": 216000})
    nome, cfg = J.job_sintetico(reg, "F41_SYN_GR", CG.PRIMARIO, CG.WALL_PRIMARIO_S)
    assert G.validate_job_D(reg, nome, cfg)
    J.validar_com_pe_runner({nome: cfg})
    ruins = 0
    h1 = pinos["eventos"][D10[0]]["strain"]["H1"]["hdf5"]
    for rotulo, mut in (("strain_real", lambda c: c["data"]["H1"].update(onsource_path=h1, offsource_path=h1)),
                        ("dtau220_nao_zero", lambda c: c["injection"]["parameters"].update(dtau220=-0.3)),
                        ("janela_encosta", lambda c: c.__setitem__("segment_start_GPS", c["event_GPS"] - 20.0)),
                        ("snr_diferente", lambda c: c["injection"].__setitem__("target_network_optimal_SNR", 30.0)),
                        ("parede_acima_do_teto", lambda c: c.__setitem__("wall_budget_seconds", 300000))):
        c2 = copy.deepcopy(cfg)
        mut(c2)
        try:
            G.validate_job_D(reg, nome, c2)
            raise AssertionError("job sintetico ruim aceito: " + rotulo)
        except (G.GuardError, KeyError):
            ruins += 1
    f = Path(pinos["sinteticos"]["SYN_F41"]["strain"]["H1"]["hdf5"])
    f.write_bytes(os.urandom(2048))
    try:
        G.checked_registration()
        raise AssertionError("sintetico adulterado aceito")
    except G.GuardError:
        pass
    return {"recusas_de_job": ruins, "snr_alvo_F41": pinos["sinteticos"]["SYN_F41"]["snr_rede"]}


@teste("T23 congelar_D: 22 jobs (mini + F4.1 + 10 cegos + 10 repeticoes D5 maxcall x2); o guarda carrega; byte alterado em JOBS recusa; congelar de novo recusa (exclusivo)")
def _():
    pinos, h = _env_com_sinteticos("env23")
    _abrir_relogio()
    cong, hj, hc = CG.congelar()
    assert len(cong["jobs"]) == 2 + 20 and cong["pinos_sha256"] == h and cong["opcao"] == "c"
    reg, dig = G.checked_registration()
    assert reg["limites"]["wall_max_por_job_s"] == CG.WALL_REPETICAO_S
    jobs = G.load_jobs(reg, dig)
    r1 = jobs["D_" + D10[0] + "_R1"]
    p1 = jobs["D_" + D10[0]]
    assert r1["sampler"]["maxcall"] == 2 * p1["sampler"]["maxcall"] and r1["sampler"]["seed"] != p1["sampler"]["seed"] and r1["wall_budget_seconds"] == CG.WALL_REPETICAO_S
    assert {k: v for k, v in jobs["F41_SYN_GR"]["sampler"].items() if k != "seed"} == {k: v for k, v in p1["sampler"].items() if k != "seed"} and jobs["F41_SYN_GR"]["injection"]["parameters"]["dtau220"] == 0.0
    try:
        CG.congelar()
        raise AssertionError("congelar duas vezes")
    except FileExistsError:
        pass
    raw = G.JOBS.read_bytes()
    G.JOBS.write_bytes(raw.replace(b"512", b"513", 1))
    try:
        G.load_jobs(reg, dig)
        raise AssertionError("JOBS alterado aceito")
    except G.GuardError:
        pass
    return {"jobs": len(cong["jobs"]), "limites": cong["limites"], "amostrador": cong["amostrador_primario"]}


@teste("T24 regra D5: so PARTIAL_*/BUDGET_STOPPED repetem, uma unica vez; aceito, falha de processo e EDOM nao repetem; 2 em paralelo sem travar")
def _():
    ok = {"status_controlador": "CHILD_COMPLETED_REQUIRES_REVIEW", "aceito": True, "status_pe": CRITERIO_OK}
    tabela = {
        "D_A": ok,
        "D_B": {"status_controlador": "PARTIAL_MAXCALL_NOT_ACCEPTED", "aceito": False, "status_pe": "PARTIAL_MAXCALL_NOT_ACCEPTED"},
        "D_B_R1": ok,
        "D_C": {"status_controlador": "BUDGET_STOPPED_PARTIAL_NOT_POSTERIOR", "aceito": None, "status_pe": None},
        "D_C_R1": {"status_controlador": "PARTIAL_LOW_ESS", "aceito": False, "status_pe": "PARTIAL_LOW_ESS"},
        "D_D": {"status_controlador": "CHILD_FAILED_OR_INTERRUPTED", "aceito": None, "status_pe": None},
        "D_E": {"status_controlador": "CHILD_FAILED_OR_INTERRUPTED", "aceito": False, "status_pe": "FAILED_EDOM_INSIDE_POSTERIOR_REGION"},
    }
    chamadas = []
    orig = L.executar_job
    L.executar_job = lambda nome, estado: (chamadas.append(nome), dict(tabela[nome], controlador=True))[1]
    L.FILA, L.ESTADO = TMP / "fila_t24", TMP / "fila_t24" / "E.json"
    try:
        est = {"jobs": {"D_A": {}, "D_B": {}, "D_C": {}, "D_D": {}, "D_E": {}}}
        fin = L.rodar_com_d5(["D_A", "D_B", "D_C", "D_D", "D_E"], est, 2)
    finally:
        L.executar_job = orig
    assert sorted(chamadas) == sorted(["D_A", "D_B", "D_B_R1", "D_C", "D_C_R1", "D_D", "D_E"]), chamadas
    assert fin["D_A"]["aceito"] and fin["D_B"]["aceito"] and fin["D_B"]["job_usado"] == "D_B_R1"
    assert not fin["D_C"]["aceito"] and fin["D_C"]["job_usado"] == "D_C_R1"
    assert not fin["D_D"]["aceito"] and fin["D_D"]["job_usado"] == "D_D" and not fin["D_E"]["aceito"]
    assert "D_C_R1_R1" not in chamadas
    return {"chamadas": sorted(chamadas)}


def _fake_job(saida, nome, aceito, pe_status, saida_analista=None, hdf5=True):
    d = saida / nome
    d.mkdir(parents=True)
    ctl = {"status": "CHILD_COMPLETED_REQUIRES_REVIEW" if aceito else pe_status, "returncode": 0 if aceito else 3, "wall_seconds": 3600.0,
           "children_user_cpu_seconds": 70000.0, "children_system_cpu_seconds": 2000.0}
    (d / "CONTROLLER.json").write_text(json.dumps(ctl))
    (d / "PRIVATE_CONVERGENCE.json").write_text(json.dumps({"status": pe_status, "accepted_for_analysis": aceito, "ncall": 12345678, "delta_logz": 0.05 if aceito else 40.0, "ess": 300.0,
                                                          "posterior_samples": 4000, "threshold": 0.1, "minimum_ess": 100}))
    if saida_analista is not None:
        (d / "ANALYST_OUTPUT.json").write_text(json.dumps(saida_analista))
    if hdf5:
        (d / (nome + "_result.hdf5")).write_bytes(os.urandom(4096))        # NAO e um HDF5: prova que o estagio cego so le os bytes
    return d


@teste("T25 estagio cego da fila: usa a primaria aceita ou a R1; grava sha256 do hdf5 SEM abri-lo (bytes aleatorios); evento sem analise aceita fica listado; sem valor central de dtau220")
def _():
    pinos, h = _env_com_sinteticos("env25")
    _abrir_relogio()
    rng = np.random.default_rng(25)
    for k, e in enumerate(D10):
        if k == 9:
            _fake_job(G.SAIDAS, "D_" + e, False, "PARTIAL_MAXCALL_NOT_ACCEPTED")
            _fake_job(G.SAIDAS, "D_" + e + "_R1", False, "PARTIAL_MAXCALL_NOT_ACCEPTED")
            continue
        s, _r = _saida_sintetica(rng, e, SIG[e], 0.072)
        if k == 3:
            _fake_job(G.SAIDAS, "D_" + e, False, "PARTIAL_LOW_ESS")
            _fake_job(G.SAIDAS, "D_" + e + "_R1", True, CRITERIO_OK, s)
        else:
            _fake_job(G.SAIDAS, "D_" + e, True, CRITERIO_OK, s)
    EF.DESTINO = TMP / "estagio_t25" / "PODER_RAMO_B_ANTES_DE_ABRIR.json"
    eg, hh = EF.executar(destino=EF.DESTINO)
    assert eg["n_eventos_convergidos"] == 9 and D10[9] in eg["eventos_sem_analise_aceita"] and eg["jobs_usados"][D10[3]].endswith("_R1")
    assert "INSUFFICIENT_SAMPLE" in eg["veredito_se_mantido"]
    hs = eg["hash_dos_posteriores_sha256"]["D_" + D10[0]]
    assert hs["D_%s_result.hdf5" % D10[0]] == hashlib.sha256((G.SAIDAS / ("D_" + D10[0]) / ("D_%s_result.hdf5" % D10[0])).read_bytes()).hexdigest()
    txt = EF.DESTINO.read_text()
    assert "delta_hat" not in txt and "media_dtau" not in txt and hashlib.sha256(txt.encode()).hexdigest() == hh
    try:
        EF.executar(destino=EF.DESTINO)
        raise AssertionError("estagio cego sobrescreveu")
    except FileExistsError:
        pass
    return {"aceitos": eg["n_eventos_convergidos"], "sem_analise": list(eg["eventos_sem_analise_aceita"]), "veredito_se_mantido": eg["veredito_se_mantido"][-62:]}


@teste("T26 avaliacao da F4.1 e consulta da fila: convergiu => recuperacao sintetica + projecao; nao convergiu => parede medida; consultar resume sem ler posterior")
def _():
    pinos, h = _env_com_sinteticos("env26")
    rng = np.random.default_rng(26)
    ao = {"columns": {"dtau220": rng.normal(0.02, 0.30, 5000).tolist()}}
    _fake_job(G.SAIDAS, "F41_SYN_GR", True, CRITERIO_OK, ao)
    r = OQ.avaliar_f41()
    assert r["convergiu"] and r["wall_h"] == 1.0 and abs(r["cpu_h"] - 20.0) < 1e-9 and r["recuperacao_sintetica"]["verdade_dentro_de_q05_q95"] and "projecao_fila_D" in r
    shutil.rmtree(G.SAIDAS / "F41_SYN_GR")
    _fake_job(G.SAIDAS, "F41_SYN_GR", False, "PARTIAL_MAXCALL_NOT_ACCEPTED", None)
    r2 = OQ.avaliar_f41()
    assert (not r2["convergiu"]) and "parede_medida" in r2 and r2["delta_logz"] == 40.0
    L.FILA, L.ESTADO = TMP / "fila_t26", TMP / "fila_t26" / "E.json"
    est = {"fase": "TESTE", "jobs": {"D_x": {"estado": "EM_CURSO", "inicio_utc": L.agora()}, "D_y": {"estado": "CONCLUIDO", "aceito": True, "ncall": 5}}}
    L.gravar_estado(est)
    res = CQ.resumo()
    assert res["contagem_por_estado"] == {"EM_CURSO": 1, "CONCLUIDO": 1} and "decorrido_h" in res["jobs"]["D_x"]
    return {"F41_ok": r["status_pe"], "F41_falha": r2["status_pe"], "consulta": res["contagem_por_estado"]}


if __name__ == "__main__":
    total, ok = len(RES), sum(1 for r in RES if r["ok"])
    for r in RES:
        print(("PASS " if r["ok"] else "FAIL ") + r["teste"][:150])
        if not r["ok"]:
            print("     ->", r["detalhe"])
    print("%d/%d testes passam" % (ok, total))
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(json.dumps({"total": total, "ok": ok, "resultados": RES}, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    shutil.rmtree(TMP, ignore_errors=True)
    sys.exit(0 if ok == total else 1)
