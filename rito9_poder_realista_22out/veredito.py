"""veredito.py - aplica o VEREDITO PRE-REGISTRADO do Rito 9 (poder realista, 22/10/2026). Pinado por sha256.

Uso:  python veredito.py <PREREGISTRO.json> <PINS.json> <dir_saida_da_rodada> <arquivo_veredito.json>

Regras (todas lidas de PREREGISTRO.json; este script NAO tem limiar proprio e NAO muda limiar):
  0. PINS: sha256 deste arquivo, do PREREGISTRO.json e dos scripts conferem com PINS.json; o MANIFEST_RODADA
     da rodada confere arquivo a arquivo. Divergencia = erro (fail-closed).
  1. PORTAS NUMERICAS: testes analiticos do nucleo; numero de casos; nenhum caso com FALHA_NUMERICA;
     monotonia do poder em n; massa residual; vazamento de janela; todo limiar c_n <= ln(1/p5sigma) + 0.02
     (limite de Wald, P0(Lambda>=c) <= exp(-c)); verificacao por simulacao (amostragem por importancia) dentro
     da tolerancia; robustez numerica dentro da tolerancia. Qualquer porta falha  ->  INCONCLUSIVE.
  2. POWERED_BNS  <=>  existe caso das familias realistas (P1, P2) com n_req <= N_alcancavel, em que
        N_alcancavel = max_eventos / fusoes_por_neutrino_esperado   (Kyutoku-Kashiyama, taxa declarada),
     i.e., o numero de neutrinos esperado de <= max_eventos fusoes ate D_eff na exposicao declarada.
  3. Caso contrario  ->  UNDERPOWERED_WALL_MEASURED.
Vereditos permitidos: POWERED_BNS | UNDERPOWERED_WALL_MEASURED | INCONCLUSIVE. Nada mais.
Estatuto: SYNTHETIC_DIAGNOSTIC_ONLY. observed_sigma = null. Nenhuma afirmacao sobre a natureza.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys

PERMITIDOS = ("POWERED_BNS", "UNDERPOWERED_WALL_MEASURED", "INCONCLUSIVE")


def sha256_arquivo(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def ler_csv(p):
    with open(p, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def num(x, default=None):
    if x is None or x == "":
        return default
    return float(x)


def main():
    if len(sys.argv) != 5:
        raise SystemExit(__doc__)
    prereg_path, pins_path, dir_saida, out_path = sys.argv[1:5]
    base = os.path.dirname(os.path.abspath(prereg_path))
    falhas = []

    # ---- 0. PINS ----
    pins = json.load(open(pins_path, "r", encoding="utf-8"))
    for nome, esperado in pins["sha256"].items():
        real = sha256_arquivo(os.path.join(base, nome))
        if real != esperado:
            raise SystemExit(f"PIN_CHANGED: {nome}: {real} != {esperado}")
    self_sha = sha256_arquivo(os.path.abspath(__file__))
    if pins["sha256"].get("veredito.py") != self_sha:
        raise SystemExit("PIN_CHANGED: veredito.py nao consta nos PINS ou diverge")
    man = json.load(open(os.path.join(dir_saida, "MANIFEST_RODADA.json"), "r", encoding="utf-8"))
    for nome, esperado in man["sha256"].items():
        real = sha256_arquivo(os.path.join(dir_saida, nome))
        if real != esperado:
            raise SystemExit(f"MANIFEST_RODADA divergente: {nome}")
    pr = json.load(open(prereg_path, "r", encoding="utf-8"))
    amb = json.load(open(os.path.join(dir_saida, "AMBIENTE_RODADA.json"), "r", encoding="utf-8"))
    if amb.get("modo") != "OFICIAL":
        raise SystemExit("rodada nao e OFICIAL")
    if amb.get("prereg_sha256") != sha256_arquivo(prereg_path):
        raise SystemExit("a rodada usou outro PREREGISTRO.json")

    # ---- 1. PORTAS NUMERICAS ----
    pv = pr["veredito"]
    casos = ler_csv(os.path.join(dir_saida, "n_req_por_caso.csv"))
    testes = json.load(open(os.path.join(dir_saida, "testes_nucleo.json"), "r", encoding="utf-8"))
    mc = ler_csv(os.path.join(dir_saida, "verificacao_mc.csv"))
    rob = ler_csv(os.path.join(dir_saida, "robustez_numerica.csv"))
    fam = pr["familias"]
    n_perfis_p1 = len(fam["P1"]["K"]) * len(fam["P1"]["S_ms"]) * len(fam["P1"]["gamma_fwhm_ms"]) * len(fam["P1"]["amp"])
    esperado_casos = len(fam["ell_km"]) * (n_perfis_p1 * (1 + len(fam["P2"]["tau_ms"]) * len(fam["P2"]["f_tail"]))
                                           + len(fam["P3"]["gamma_fwhm_ms"]) + len(fam["REF_ESQUELETO"]["sigma_e_ms"])
                                           + len(fam["SENS_VETO"]["f_tail"])
                                           + len(fam["SENS_ZERO"]["variantes"]) * len(fam["SENS_ZERO"]["sigma_offset_ms"]))
    gates = {}
    gates["testes_nucleo_passaram"] = all(v.get("passou") for v in testes.values())
    gates["numero_de_casos"] = (len(casos) == esperado_casos)
    gates["sem_falha_numerica"] = all(r["status"] in ("OK", "N_REQ_ACIMA_DE_N_MAX") for r in casos)
    gates["poder_monotono"] = all(r.get("monotono_ok") == "True" for r in casos if r["status"] == "OK")
    gates["massa_residual"] = all(num(r.get("massa_P0"), 0) >= 1 - pv["tol_massa"] and num(r.get("massa_P1"), 0) >= 1 - pv["tol_massa"]
                                  for r in casos if r["status"] in ("OK", "N_REQ_ACIMA_DE_N_MAX"))
    gates["janela_sem_vazamento"] = all(num(r.get("fora_max"), 0) <= pv["tol_fora"] for r in casos if r["status"] == "OK")
    varr = ler_csv(os.path.join(dir_saida, "varredura_n.csv"))
    wald = math.log(1.0 / (0.5 * math.erfc(5.0 / math.sqrt(2.0))))
    gates["limiar_respeita_limite_de_Wald"] = bool(varr) and max(float(r["c_n"]) for r in varr) <= wald + 0.02
    gates["mc_linhas_minimas"] = (len(mc) >= pv["mc_min_linhas"])
    gates["mc_dentro_da_tolerancia"] = bool(mc) and all(r.get("ok") == "True" for r in mc)
    gates["robustez_linhas_minimas"] = (len(rob) >= pv["robustez_min_linhas"])
    gates["robustez_dentro_da_tolerancia"] = bool(rob) and all(r.get("ok") == "True" for r in rob)
    falhas = [k for k, v in gates.items() if not v]

    # ---- constantes K-K declaradas ----
    KK = pr["taxa_KK"]
    fusoes_por_nu = float(KK["fusoes_por_neutrino_esperado"])
    expo_por_nu = float(KK["exposicao_Mt_ano_por_neutrino_esperado"])
    M_T = float(KK["massa_detector_declarada_Mt"])
    a_ref = float(KK["N_nu_a_100Mpc_por_Mt"])
    R = float(KK["R_Mpc3_por_Myr"])
    max_ev = int(pv["max_eventos"])
    N_alcancavel = max_ev / fusoes_por_nu

    def derivados(n):
        d_max = 100.0 * math.sqrt(a_ref * M_T / n)
        vol = 4.0 / 3.0 * math.pi * d_max ** 3
        return dict(
            n_req=n,
            fusoes_necessarias_ate_Deff=fusoes_por_nu * n,
            exposicao_Mt_ano=expo_por_nu * n,
            anos_com_detector_declarado=expo_por_nu * n / M_T,
            Dmax_um_evento_Mpc=d_max,
            eventos_por_seculo_dentro_de_Dmax=R * vol * 1e-4,
            massa_detector_Mt_para_max_eventos=n * fusoes_por_nu / max_ev / 1.0,
            fator_acima_do_alcance=n / N_alcancavel,
        )

    # ---- 2/3. VEREDITO ----
    realistas = [r for r in casos if r["familia"] in pv["familias_realistas"]]
    com_n = [r for r in realistas if r["n_req"] != ""]
    candidatos = [r["case_id"] for r in com_n if float(r["n_req"]) <= N_alcancavel]
    if falhas:
        veredito = "INCONCLUSIVE"
        motivo = "porta numerica falhou: " + ",".join(falhas)
    elif candidatos:
        veredito = "POWERED_BNS"
        motivo = f"{len(candidatos)} caso(s) realista(s) com n_req <= {N_alcancavel:.6g}"
    else:
        veredito = "UNDERPOWERED_WALL_MEASURED"
        motivo = (f"nenhum caso P1/P2 com n_req <= N_alcancavel = {max_ev}/{fusoes_por_nu:g} = {N_alcancavel:.6g} neutrinos "
                  f"esperados; menor n_req realista = {min(int(r['n_req']) for r in com_n) if com_n else 'NA'}")
    assert veredito in PERMITIDOS

    # ---- resumos ----
    resumo = {}
    for fam_nome in ("P1", "P2", "P3", "REF_ESQUELETO", "SENS_VETO", "SENS_ZERO"):
        for ell in fam["ell_km"]:
            sub = [r for r in casos if r["familia"] == fam_nome and float(r["ell_km"]) == float(ell)]
            ns = sorted(int(r["n_req"]) for r in sub if r["n_req"] != "")
            if not ns:
                resumo[f"{fam_nome}|ell{ell:g}"] = dict(n_casos=len(sub), n_req_min=None)
                continue
            melhor = min((r for r in sub if r["n_req"] != ""), key=lambda r: int(r["n_req"]))
            pior = max((r for r in sub if r["n_req"] != ""), key=lambda r: int(r["n_req"]))
            resumo[f"{fam_nome}|ell{ell:g}"] = dict(
                n_casos=len(sub), n_casos_sem_n_req=len(sub) - len(ns), n_req_min=ns[0], n_req_mediana=ns[len(ns) // 2],
                n_req_max=ns[-1], melhor_caso=melhor["case_id"], pior_caso=pior["case_id"],
                derivados_do_melhor=derivados(ns[0]), derivados_do_pior=derivados(ns[-1]))
    if com_n:
        melhor_global = min(com_n, key=lambda r: int(r["n_req"]))
        melhor_dict = dict(case_id=melhor_global["case_id"], **derivados(int(melhor_global["n_req"])))
    else:
        melhor_dict = None
    res = dict(
        id="RITO9_PODER_REALISTA_20261022", veredito=veredito, motivo=motivo, gates=gates, gates_falhos=falhas,
        regra=dict(N_alcancavel_neutrinos_esperados=N_alcancavel, max_eventos=max_ev, D_eff_Mpc=KK["D_eff_Mpc"],
                   fusoes_por_neutrino_esperado=fusoes_por_nu, massa_detector_declarada_Mt=M_T,
                   familias_realistas=pv["familias_realistas"]),
        n_casos=len(casos), n_casos_realistas=len(realistas), n_realistas_sem_n_req=len(realistas) - len(com_n),
        candidatos_powered=candidatos, melhor_caso_realista=melhor_dict, resumo_por_familia_e_ell=resumo,
        estatuto="SYNTHETIC_DIAGNOSTIC_ONLY", observed_sigma=None,
        entradas_sha256=dict(PREREGISTRO=sha256_arquivo(prereg_path), PINS=sha256_arquivo(pins_path),
                             veredito_py=self_sha, MANIFEST_RODADA=sha256_arquivo(os.path.join(dir_saida, "MANIFEST_RODADA.json")),
                             n_req_por_caso=sha256_arquivo(os.path.join(dir_saida, "n_req_por_caso.csv"))))
    res["modo_da_rodada"] = amb["modo"]
    # tabela derivada por caso (formulas K-K pinadas neste script)
    der_path = os.path.join(os.path.dirname(os.path.abspath(out_path)), "derivados_KK_por_caso.csv")
    cols = ["case_id", "familia", "perfil_id", "ell_km", "n_req", "fusoes_necessarias_ate_Deff", "exposicao_Mt_ano",
            "anos_com_detector_declarado", "Dmax_um_evento_Mpc", "eventos_por_seculo_dentro_de_Dmax",
            "massa_detector_Mt_para_max_eventos", "fator_acima_do_alcance"]
    with open(der_path, "x", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for r in casos:
            if r["n_req"] == "":
                continue
            d = derivados(int(r["n_req"]))
            w.writerow(dict(case_id=r["case_id"], familia=r["familia"], perfil_id=r["perfil_id"], ell_km=r["ell_km"], **d))
    res["derivados_KK_por_caso_sha256"] = sha256_arquivo(der_path)
    with open(out_path, "x", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    print(json.dumps(dict(veredito=veredito, motivo=motivo, gates_falhos=falhas), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
