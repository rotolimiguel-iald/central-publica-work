"""Rodada do ESTUDO DE PODER REALISTA do Rito 9 (22/10/2026). Fail-closed.

Uso:  python rodar_estudo.py <PREREGISTRO.json> <PINS.json> <dir_saida> [--workers N] [--dry <config_dry.json>]

1. Confere os PINS (sha256 de PREREGISTRO.json e dos scripts). Divergencia = aborta.
2. Le SEALED_CODATA_ALPHA do um.py (so leitura) e calcula beta em runtime (nunca literal).
3. Roda os testes analiticos do nucleo (porta de entrada).
4. Avalia todos os casos (perfil x ell): n_req pelo LLR de forma completa com H0 CONHECIDO (oraculo).
5. Verificacao por simulacao (amostragem por importancia, semente fixa) e robustez numerica em amostra pre-registrada.
6. Grava CSVs crus + MANIFEST_RODADA.json com sha256 de cada saida.

Nenhuma saida fora de <dir_saida>. Nenhum dado observacional. observed_sigma = null.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import platform
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import scipy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nucleo_poder as N  # noqa: E402
import teste_nucleo  # noqa: E402


# ----------------------------------------------------------------------------------------------
def sha256_arquivo(p: str) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def carregar_json(p: str) -> dict:
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def verificar_pins(pins_path: str, base_dir: str) -> dict:
    pins = carregar_json(pins_path)
    for nome, esperado in pins["sha256"].items():
        p = os.path.join(base_dir, nome)
        real = sha256_arquivo(p)
        if real != esperado:
            raise SystemExit(f"PIN_CHANGED: {nome} sha256 {real} != pin {esperado} (fail-closed)")
    return pins


# ----------------------------------------------------------------------------------------------
# Casos
# ----------------------------------------------------------------------------------------------
def _id_p1(K, S, G, amp):
    return f"K{K}_S{S:g}_G{G:g}_{amp}"


def gerar_casos(prereg: dict, beta: float) -> list:
    fam = prereg["familias"]
    ells = fam["ell_km"]
    casos = []
    p1 = fam["P1"]
    for K in p1["K"]:
        for S in p1["S_ms"]:
            for G in p1["gamma_fwhm_ms"]:
                for amp in p1["amp"]:
                    g = N.perfil_burst(K, S, G, amp, p1["mu1_ms"], p1["r_damped"])
                    pid = _id_p1(K, S, G, amp)
                    for ell in ells:
                        casos.append(dict(case_id=f"P1|{pid}|ell{ell:g}", familia="P1", perfil_id=pid, ell_km=ell,
                                          K=K, S_ms=S, gamma_ms=G, amp=amp, tau_ms=None, f_tail=0.0,
                                          perfil=N.perfil_dict("P1", g, 0.0, None, pid)))
    p2 = fam["P2"]
    for K in p1["K"]:
        for S in p1["S_ms"]:
            for G in p1["gamma_fwhm_ms"]:
                for amp in p1["amp"]:
                    g = N.perfil_burst(K, S, G, amp, p1["mu1_ms"], p1["r_damped"])
                    for tau in p2["tau_ms"]:
                        for f in p2["f_tail"]:
                            pid = f"{_id_p1(K, S, G, amp)}_tau{tau:g}_f{f:g}"
                            for ell in ells:
                                casos.append(dict(case_id=f"P2|{pid}|ell{ell:g}", familia="P2", perfil_id=pid, ell_km=ell,
                                                  K=K, S_ms=S, gamma_ms=G, amp=amp, tau_ms=tau, f_tail=f,
                                                  perfil=N.perfil_dict("P2", g, f, tau, pid)))
    p3 = fam["P3"]
    for G in p3["gamma_fwhm_ms"]:
        sig = G * N.FWHM_TO_SIGMA
        pid = f"G{G:g}"
        for ell in ells:
            casos.append(dict(case_id=f"P3|{pid}|ell{ell:g}", familia="P3", perfil_id=pid, ell_km=ell,
                              K=1, S_ms=p3["mu_ms"], gamma_ms=G, amp="single", tau_ms=None, f_tail=0.0,
                              perfil=N.perfil_dict("P3", [(1.0, p3["mu_ms"], sig)], 0.0, None, pid)))
    sv = fam["SENS_VETO"]
    b = sv["base"]
    gsv = N.perfil_burst(b["K"], b["S_ms"], b["gamma_fwhm_ms"], b["amp"], p1["mu1_ms"], p1["r_damped"])
    for f in sv["f_tail"]:
        pid = f"{_id_p1(b['K'], b['S_ms'], b['gamma_fwhm_ms'], b['amp'])}_tau{sv['tau_ms']:g}_f{f:g}"
        for ell in ells:
            casos.append(dict(case_id=f"SENS_VETO|{pid}|ell{ell:g}", familia="SENS_VETO", perfil_id=pid, ell_km=ell,
                              K=b["K"], S_ms=b["S_ms"], gamma_ms=b["gamma_fwhm_ms"], amp=b["amp"], tau_ms=sv["tau_ms"],
                              f_tail=f, perfil=N.perfil_dict("SENS_VETO", gsv, f, sv["tau_ms"], pid)))
    sz = fam["SENS_ZERO"]
    b = sz["base"]
    gsz = N.perfil_burst(b["K"], b["S_ms"], b["gamma_fwhm_ms"], b["amp"], p1["mu1_ms"], p1["r_damped"])
    for var in sz["variantes"]:
        f = var["f_tail"]
        tau = var["tau_ms"]
        for so in sz["sigma_offset_ms"]:
            pid = f"{_id_p1(b['K'], b['S_ms'], b['gamma_fwhm_ms'], b['amp'])}_f{f:g}" + (f"_tau{tau:g}" if f > 0 else "") + f"_off{so:g}"
            for ell in ells:
                casos.append(dict(case_id=f"SENS_ZERO|{pid}|ell{ell:g}", familia="SENS_ZERO", perfil_id=pid, ell_km=ell,
                                  K=b["K"], S_ms=b["S_ms"], gamma_ms=b["gamma_fwhm_ms"], amp=b["amp"], tau_ms=tau if f > 0 else None,
                                  f_tail=f, perfil=N.perfil_dict("SENS_ZERO", gsz, f, tau if f > 0 else None, pid, sigma_offset_ms=so),
                                  sigma_offset_ms=so))
    ref = fam["REF_ESQUELETO"]
    for se in ref["sigma_e_ms"]:
        pid = f"sig{se:g}"
        for ell in ells:
            casos.append(dict(case_id=f"REF_ESQUELETO|{pid}|ell{ell:g}", familia="REF_ESQUELETO", perfil_id=pid,
                              ell_km=ell, K=1, S_ms=ref["mu_ms"], gamma_ms=se / N.FWHM_TO_SIGMA, amp="single",
                              tau_ms=None, f_tail=0.0,
                              perfil=N.perfil_dict("REF_ESQUELETO", [(1.0, ref["mu_ms"], se)], 0.0, None, pid)))
    return casos


# ----------------------------------------------------------------------------------------------
# Trabalhadores (funcoes de topo, picklaveis)
# ----------------------------------------------------------------------------------------------
def _preparar(caso, beta, num, cap=None, delta_fator=1.0):
    cap = num["cap_lambda"] if cap is None else cap
    edges, P0, P1, tau0 = N.celulas(caso["perfil"], caso["ell_km"], beta, num["massa_residual_log"])
    P0c, P1c, lam, lam_c = N.llr_celulas(P0, P1, cap)
    w0 = P0c / P0c.sum()
    m0 = float((w0 * lam_c).sum())
    sd0 = math.sqrt(float((w0 * (lam_c - m0) ** 2).sum()))
    delta = min(num["delta_max"], sd0 / num["delta_divisor_sd0"]) * delta_fator
    p0, p1, lo = N.pmf_rede(P0c, P1c, lam_c, delta)
    return dict(edges=edges, P0=P0, P1=P1, tau0=tau0, P0c=P0c, P1c=P1c, lam=lam, lam_c=lam_c, delta=delta,
                p0=p0, p1=p1, lo=lo, sd0=sd0, cap=cap)


def avaliar_caso(args):
    caso, beta, num = args
    t0 = time.perf_counter()
    base = dict(case_id=caso["case_id"], familia=caso["familia"], perfil_id=caso["perfil_id"], K=caso["K"],
                S_ms=caso["S_ms"], gamma_ms=round(caso["gamma_ms"], 12), amp=caso["amp"],
                tau_ms=caso["tau_ms"] if caso["tau_ms"] is not None else "", f_tail=caso["f_tail"],
                ell_km=caso["ell_km"], sigma_offset_ms=caso.get("sigma_offset_ms", 0.0), beta=beta)
    try:
        d = _preparar(caso, beta, num)
        kw = dict(janela_sd=num["janela_sd"], L_exato_max=num["L_exato_max"], L_max=num["L_max"])
        n_req, rows, diag = N.varrer_n(d["p0"], d["p1"], d["lo"], d["delta"], n_max=num["n_max"],
                                       alvo=num["alvo_poder"], **kw)
        P0c, P1c, lam, lam_c = d["P0c"], d["P1c"], d["lam"], d["lam_c"]
        sat = lam >= d["cap"]
        pos0 = np.isfinite(lam)
        kl10 = float((P1c * lam_c).sum() / P1c.sum())                       # KL(H1||H0), com teto
        kl01 = float(-(P0c[pos0] * lam[pos0]).sum() / P0c.sum())            # KL(H0||H1)
        q1_sat = float(P1c[sat].sum() / P1c.sum())
        q1_gt15 = float(P1c[lam >= 15.0].sum() / P1c.sum())
        linha_req = [r for r in rows if r["n"] == n_req][0] if n_req is not None else None
        row = dict(base)
        row.update(
            tau0_us=d["tau0"] * 1e3, n_celulas=int(d["edges"].size - 1),
            massa_P0=float(d["P0"].sum()), massa_P1=float(d["P1"].sum()),
            delta_rede=d["delta"], sd_lambda_h0=d["sd0"], kl_h1_h0_cap=kl10, kl_h0_h1=kl01,
            q1_sat=q1_sat, q1_lambda_gt15=q1_gt15,
            n_req=("" if n_req is None else int(n_req)),
            c_n_em_n_req=("" if linha_req is None else linha_req["c_n"]),
            poder_em_n_req=("" if linha_req is None else linha_req["poder"]),
            mediana_h1_em_n_req=("" if linha_req is None else linha_req["mediana_h1"]),
            exata_todas=bool(all(r["exata"] for r in rows)), fora_max=float(max(r["fora"] for r in rows)),
            monotono_ok=bool(diag.get("monotono_ok", True)), status=("OK" if n_req is not None else "N_REQ_ACIMA_DE_N_MAX"),
            erro="", segundos=time.perf_counter() - t0)
        scan = []
        for r in rows:
            scan.append(dict(case_id=caso["case_id"], n=r["n"], c_n=r["c_n"], poder=r["poder"],
                             mediana_h1=r["mediana_h1"], cauda_h0_em_c=r["cauda_h0_em_c"],
                             exata=r["exata"], fora=r["fora"], L=r["L"]))
        return row, scan
    except Exception as e:  # falha visivel, nunca silenciosa
        row = dict(base)
        row.update(status="FALHA_NUMERICA", erro=repr(e), segundos=time.perf_counter() - t0)
        return row, []


def verificar_caso_mc(args):
    caso, beta, num, ver, n_req, case_index = args
    out = []
    try:
        d = _preparar(caso, beta, num)
        for n in (n_req - 1, n_req):
            if n < 1 or n > ver["n_max_verificavel"]:
                continue
            kw = dict(janela_sd=num["janela_sd"], L_exato_max=num["L_exato_max"], L_max=num["L_max"])
            ev = N.avaliar_n(d["p0"], d["p1"], d["lo"], d["delta"], n, **kw)
            seed = np.random.SeedSequence([ver["seed_base"], case_index, n])
            mc = N.verificar_mc(d["P1c"], d["lam"], d["lam_c"], n, ev["c_n"], ver["M"], seed)
            ok_c = (not math.isnan(mc["c_hat"])) and abs(mc["c_hat"] - ev["c_n"]) <= ver["tol_c"]
            ok_pw = abs(mc["poder_mc"] - ev["poder"]) <= max(ver["tol_poder_abs"], ver["tol_poder_sigmas"] * mc["se_poder"])
            ok_t = abs(mc["cauda_nula_em_c_lat"] - N.P5) <= max(ver["tol_cauda_rel"] * N.P5,
                                                                ver["tol_poder_sigmas"] * mc["se_cauda"])
            out.append(dict(case_id=caso["case_id"], n=n, M=mc["M"], c_lattice=ev["c_n"], c_hat_mc=mc["c_hat"],
                            poder_lattice=ev["poder"], poder_mc=mc["poder_mc"], se_poder=mc["se_poder"],
                            cauda_nula_mc=mc["cauda_nula_em_c_lat"], se_cauda=mc["se_cauda"], p5=N.P5,
                            ok_c=bool(ok_c), ok_poder=bool(ok_pw), ok_cauda=bool(ok_t),
                            ok=bool(ok_c and ok_pw and ok_t), erro=""))
    except Exception as e:
        out.append(dict(case_id=caso["case_id"], n="", ok=False, erro=repr(e)))
    return out


def robustez_caso(args):
    caso, beta, num, rob, n_req_base, c_base, pw_base = args
    out = []
    try:
        kw = dict(janela_sd=num["janela_sd"], L_exato_max=num["L_exato_max"], L_max=num["L_max"])
        for var in rob["variantes"]:
            cap = var.get("cap_lambda", None)
            fat = var.get("delta_fator", 1.0)
            d = _preparar(caso, beta, num, cap=cap, delta_fator=fat)
            n_req, rows, diag = N.varrer_n(d["p0"], d["p1"], d["lo"], d["delta"], n_max=num["n_max"],
                                           alvo=num["alvo_poder"], **kw)
            ev = N.avaliar_n(d["p0"], d["p1"], d["lo"], d["delta"], n_req_base, **kw)
            ok_n = (n_req is not None) and abs(n_req - n_req_base) <= max(rob["tol_n_abs"], math.ceil(rob["tol_n_rel"] * n_req_base))
            ok_c = abs(ev["c_n"] - c_base) <= rob["tol_c"]
            ok_p = abs(ev["poder"] - pw_base) <= rob["tol_poder"]
            out.append(dict(case_id=caso["case_id"], variante=json.dumps(var, sort_keys=True), n_req_base=n_req_base,
                            n_req_variante=("" if n_req is None else n_req), c_base=c_base, c_variante=ev["c_n"],
                            poder_base=pw_base, poder_variante=ev["poder"], ok_n=bool(ok_n), ok_c=bool(ok_c),
                            ok_poder=bool(ok_p), ok=bool(ok_n and ok_c and ok_p), erro=""))
    except Exception as e:
        out.append(dict(case_id=caso["case_id"], variante="", ok=False, erro=repr(e)))
    return out


# ----------------------------------------------------------------------------------------------
def escrever_csv(path, linhas, colunas=None):
    if not linhas:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("")
        return
    if colunas is None:
        colunas = []
        for r in linhas:
            for k in r:
                if k not in colunas:
                    colunas.append(k)
    with open(path, "x", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=colunas, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in linhas:
            w.writerow(r)


def main():
    args = sys.argv[1:]
    workers = 12
    dry = None
    if "--workers" in args:
        i = args.index("--workers")
        workers = int(args[i + 1])
        del args[i:i + 2]
    if "--dry" in args:
        i = args.index("--dry")
        dry = args[i + 1]
        del args[i:i + 2]
    if len(args) != 3:
        raise SystemExit(__doc__)
    prereg_path, pins_path, out_dir = args
    base_dir = os.path.dirname(os.path.abspath(prereg_path))
    t_ini = time.perf_counter()
    if dry is None:
        pins = verificar_pins(pins_path, base_dir)
        print("[rodada] PINS conferidos:", len(pins["sha256"]), "arquivos", flush=True)
    else:
        print("[rodada] MODO DRY (config fora das familias pre-registradas); PINS nao exigidos", flush=True)
    prereg = carregar_json(dry if dry is not None else prereg_path)
    os.makedirs(out_dir, exist_ok=False if dry is None else True)
    um = N.ler_alpha_um(prereg["beta"]["um_py"])
    beta = N.beta_de_alpha(um["alpha"])
    aviso_um = None
    reg = prereg["beta"].get("alpha_lido_no_preregistro")
    if reg is not None and um["alpha"] != reg:
        raise SystemExit(f"alpha lido ({um['alpha']!r}) diverge do registrado no pre-registro ({reg!r}): aborta")
    reg_sha = prereg["beta"].get("lido_no_preregistro", {}).get("sha256")
    if reg_sha is not None and reg_sha != um["sha256"]:
        aviso_um = "o um.py mudou desde o pre-registro (sha256 diferente), mas o alpha lido e identico"
    print(f"[rodada] um.py bytes={um['bytes']} sha256={um['sha256']} linha={um['linha']} :: {um['texto']}", flush=True)
    print(f"[rodada] beta (runtime) = {beta!r}", flush=True)
    testes = teste_nucleo.executar(prereg["beta"]["um_py"])
    num = prereg["numerica"]
    casos = gerar_casos(prereg, beta)
    print(f"[rodada] casos: {len(casos)}", flush=True)
    ordem = sorted(range(len(casos)), key=lambda i: -(casos[i]["tau_ms"] or 0.0) if casos[i]["f_tail"] > 0 else 0.0)
    resultados = {}
    scans = {}
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = ex.map(avaliar_caso, [(casos[i], beta, num) for i in ordem], chunksize=1)
        for k, (row, scan) in zip(ordem, futs):
            resultados[k] = row
            scans[k] = scan
            if len(resultados) % 25 == 0:
                print(f"[rodada] {len(resultados)}/{len(casos)} casos ({time.perf_counter()-t_ini:.0f}s)", flush=True)
    linhas = [resultados[i] for i in range(len(casos))]
    scan_linhas = [r for i in range(len(casos)) for r in scans[i]]
    n_falhas = sum(1 for r in linhas if r["status"] == "FALHA_NUMERICA")
    print(f"[rodada] casos concluidos; falhas numericas: {n_falhas}", flush=True)

    # amostra pre-registrada para verificacao MC e robustez
    ver = prereg["verificacao_mc"]
    rob = prereg["robustez"]
    ids_por_fam = {}
    for r in linhas:
        ids_por_fam.setdefault(r["familia"], []).append(r["case_id"])
    rnd = random.Random(ver["seed_base"])
    escolhidos = []
    for fam, k in ver["amostra"].items():
        ids = sorted(ids_por_fam[fam])
        escolhidos += rnd.sample(ids, min(k, len(ids)))
    idx_por_id = {c["case_id"]: i for i, c in enumerate(casos)}
    tarefas_mc, tarefas_rob = [], []
    for cid in escolhidos:
        i = idx_por_id[cid]
        r = linhas[i]
        if r["status"] != "OK":
            continue
        tarefas_mc.append((casos[i], beta, num, ver, int(r["n_req"]), i))
        tarefas_rob.append((casos[i], beta, num, rob, int(r["n_req"]), float(r["c_n_em_n_req"]), float(r["poder_em_n_req"])))
    mc_linhas, rob_linhas = [], []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for out in ex.map(verificar_caso_mc, tarefas_mc, chunksize=1):
            mc_linhas += out
        print(f"[rodada] verificacao MC concluida: {len(mc_linhas)} linhas ({time.perf_counter()-t_ini:.0f}s)", flush=True)
        for out in ex.map(robustez_caso, tarefas_rob, chunksize=1):
            rob_linhas += out
    print(f"[rodada] robustez concluida: {len(rob_linhas)} linhas ({time.perf_counter()-t_ini:.0f}s)", flush=True)

    # perfis (tabela de definicao)
    perfis = []
    vistos = set()
    for c in casos:
        key = (c["familia"], c["perfil_id"])
        if key in vistos:
            continue
        vistos.add(key)
        perfis.append(dict(familia=c["familia"], perfil_id=c["perfil_id"], K=c["K"], S_ms=c["S_ms"],
                           gamma_fwhm_ms=round(c["gamma_ms"], 12), amp=c["amp"],
                           tau_ms=c["tau_ms"] if c["tau_ms"] is not None else "", f_tail=c["f_tail"],
                           picos_w_mu_sigma=json.dumps([[round(w, 12), round(m, 9), round(s, 9)] for (w, m, s) in c["perfil"]["gauss"]])))
    escrever_csv(os.path.join(out_dir, "perfis.csv"), perfis)
    escrever_csv(os.path.join(out_dir, "n_req_por_caso.csv"), linhas)
    escrever_csv(os.path.join(out_dir, "varredura_n.csv"), scan_linhas)
    escrever_csv(os.path.join(out_dir, "verificacao_mc.csv"), mc_linhas)
    escrever_csv(os.path.join(out_dir, "robustez_numerica.csv"), rob_linhas)
    with open(os.path.join(out_dir, "testes_nucleo.json"), "x", encoding="utf-8") as f:
        json.dump(testes, f, indent=2, default=float)
    amb = dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
               plataforma=platform.platform(), workers=workers, segundos_total=time.perf_counter() - t_ini,
               um_py=um, beta_runtime=beta, n_casos=len(casos), n_falhas_numericas=n_falhas,
               amostra_verificacao=escolhidos, prereg_sha256=sha256_arquivo(prereg_path),
               modo=("DRY" if dry else "OFICIAL"), aviso_um_py=aviso_um)
    with open(os.path.join(out_dir, "AMBIENTE_RODADA.json"), "x", encoding="utf-8") as f:
        json.dump(amb, f, indent=2, default=float, ensure_ascii=False)
    manifest = {}
    for nome in sorted(os.listdir(out_dir)):
        if nome in ("MANIFEST_RODADA.json",):
            continue
        manifest[nome] = sha256_arquivo(os.path.join(out_dir, nome))
    with open(os.path.join(out_dir, "MANIFEST_RODADA.json"), "x", encoding="utf-8") as f:
        json.dump(dict(sha256=manifest, nota="sha256 lidos dos arquivos por script"), f, indent=2)
    print("[rodada] FIM", flush=True)


if __name__ == "__main__":
    main()
