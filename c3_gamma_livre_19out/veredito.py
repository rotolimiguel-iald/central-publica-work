#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
veredito.py -- FUNCAO DE VEREDITO PRE-REGISTRADA (C3 gamma LIVRE, 19/10/2026, gerencia c1).

Aplica, sem mudar limiar, as regras de REGRAS aos dados crus escritos por rodar.py.
Vereditos permitidos (e so eles):
  FLOOR_ONE_OCTAVE_NOT_FALSIFIED | NO_UNIVERSAL_FLOOR | GENERIC_NOT_TGL | MEASURE_BROKEN | INCONCLUSIVE

Observavel: O = D_folds(c3) do estado estacionario GKLS, em nats; oitava = O / ln 2.

FACE POSITIVA P: existe uma JANELA de gamma -- corrida contigua de pontos da grade logspace(-4, 0, 25)
  com extensao >= 1 decada (>= 7 pontos consecutivos, passo de 1/6 de decada) -- tal que, EM CADA ponto
  gamma da janela:
    (i)  para TODAS as 9 configs, a mediana de O nas sementes convergidas (>= 3 de 5) esta em ln 2 +- 0,05;
    (ii) |inclinacao (minimos quadrados) das 9 medianas contra x = ln(d/nc)| < 0,05.
FACE NEGATIVA:
  N1  estados Hilbert-Schmidt de cada d: mediana de O < 0,2 em TODAS as dimensoes;
  N2  o mesmo GKLS com saltos aleatorios de mesma norma NAO satisfaz P;
  N3  estado plano de posto d/2 da O = ln 2 e de posto d/4 da 2 ln 2 (erro < 1e-12).
PRECEDENCIA (primeira que vale decide):
  1. N3 falha                                   -> MEASURE_BROKEN
  2. > 10% dos pontos da grade principal sem convergir -> INCONCLUSIVE
  3. P falso                                    -> NO_UNIVERSAL_FLOOR
  4. (P verdadeiro) > 10% dos pontos de N2 sem convergir -> INCONCLUSIVE
  5. (P verdadeiro) N2 satisfaz P, ou N1 falha  -> GENERIC_NOT_TGL
  6. caso contrario (P e N1-N3 como previsto)   -> FLOOR_ONE_OCTAVE_NOT_FALSIFIED
(a regra 5 inclui "ou N1 falha" para tornar a funcao total: P sem linha de base baixa nao distingue o GKLS do generico.)
"""

import os
import sys
import csv
import json
import math
import hashlib
import statistics

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
LN2 = math.log(2.0)

CONFIGS = [(8, 2), (10, 2), (12, 2), (14, 2), (16, 2), (16, 3), (20, 3), (24, 3), (32, 4)]
SEEDS = [42, 43, 44, 45, 46]
N_GAMMA = 25
N1_STATES = 200

VEREDITOS = ["FLOOR_ONE_OCTAVE_NOT_FALSIFIED", "NO_UNIVERSAL_FLOOR", "GENERIC_NOT_TGL",
             "MEASURE_BROKEN", "INCONCLUSIVE"]

REGRAS = {
    "observavel": "O = D_folds(c3) em nats; oitava = O / ln 2",
    "banda_abs_nats": 0.05,
    "inclinacao_max_abs": 0.05,
    "x_config": "ln(d/nc)",
    "inclinacao": "minimos quadrados ordinarios das 9 medianas (nas sementes) contra x, em CADA gamma da janela",
    "janela_min_decadas": 1.0,
    "janela_tolerancia_decadas": 1e-9,
    "janela_definicao": "corrida contigua de pontos da grade em que a condicao C(gamma) vale; >= 7 pontos",
    "min_sementes_convergidas_por_celula": 3,
    "n1_mediana_max": 0.2,
    "n3_tolerancia_abs": 1e-12,
    "naoconv_max_frac": 0.10,
    "vereditos_permitidos": VEREDITOS,
    "precedencia": [
        "1. N3 falha -> MEASURE_BROKEN",
        "2. >10% dos pontos da grade principal sem convergir -> INCONCLUSIVE",
        "3. P falso -> NO_UNIVERSAL_FLOOR",
        "4. P verdadeiro e >10% dos pontos de N2 sem convergir -> INCONCLUSIVE",
        "5. P verdadeiro e (N2 satisfaz P ou N1 falha) -> GENERIC_NOT_TGL",
        "6. senao -> FLOOR_ONE_OCTAVE_NOT_FALSIFIED",
    ],
}

BAND = REGRAS["banda_abs_nats"]
SLOPE_MAX = REGRAS["inclinacao_max_abs"]
WIN_DEC = REGRAS["janela_min_decadas"]
WIN_TOL = REGRAS["janela_tolerancia_decadas"]
MIN_SEEDS = REGRAS["min_sementes_convergidas_por_celula"]
N1_MAX = REGRAS["n1_mediana_max"]
N3_TOL = REGRAS["n3_tolerancia_abs"]
NONCONV_MAX = REGRAS["naoconv_max_frac"]


# ----------------------------------------------------------------------------- leitura

def _f(s):
    return float(s)


def load_rows(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(dict(set=r["set"], d=int(r["d"]), nc=int(r["nc"]), seed=int(r["seed"]), gi=int(r["gi"]),
                             gamma=_f(r["gamma"]), O=_f(r["O"]), conv=(r["conv"] == "1"), reason=r["reason"]))
    return rows


def load_n1(path):
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.append(dict(d=int(r["d"]), k=int(r["k"]), O=_f(r["O"])))
    return out


def check_complete(rows, nome):
    esperado = len(CONFIGS) * len(SEEDS) * N_GAMMA
    if len(rows) != esperado:
        raise SystemExit("DADOS INCOMPLETOS em %s: %d linhas, esperado %d" % (nome, len(rows), esperado))
    chaves = {(r["d"], r["nc"], r["seed"], r["gi"]) for r in rows}
    if len(chaves) != esperado:
        raise SystemExit("DADOS COM CHAVES REPETIDAS OU FALTANDO em %s" % nome)
    gam = {}
    for r in rows:
        if gam.setdefault(r["gi"], r["gamma"]) != r["gamma"]:
            raise SystemExit("gamma inconsistente no indice %d em %s" % (r["gi"], nome))
    if sorted(gam) != list(range(N_GAMMA)):
        raise SystemExit("indices de gamma incompletos em %s" % nome)
    return [gam[i] for i in range(N_GAMMA)]


# ----------------------------------------------------------------------------- estatistica

def ols_slope(x, y):
    n = len(x)
    xm = sum(x) / n
    ym = sum(y) / n
    sxx = sum((a - xm) ** 2 for a in x)
    sxy = sum((a - xm) * (b - ym) for a, b in zip(x, y))
    return sxy / sxx


def nonconv_fraction(rows):
    return sum(1 for r in rows if not r["conv"]) / len(rows)


def evaluate_P(rows, gammas):
    """Aplica a face positiva P a um conjunto de linhas (principal ou N2)."""
    cells = {}
    for r in rows:
        cells.setdefault((r["d"], r["nc"], r["gi"]), []).append(r)
    xs = [math.log(d / nc) for (d, nc) in CONFIGS]

    per = []
    for gi in range(len(gammas)):
        meds, valid = [], True
        for (d, nc) in CONFIGS:
            vals = [r["O"] for r in cells.get((d, nc, gi), []) if r["conv"] and math.isfinite(r["O"])]
            if len(vals) < MIN_SEEDS:
                valid = False
                meds.append(None)
            else:
                meds.append(statistics.median(vals))
        if valid:
            band_ok = all(abs(m - LN2) <= BAND for m in meds)
            slope = ols_slope(xs, meds)
            slope_ok = abs(slope) < SLOPE_MAX
            n_in = sum(1 for m in meds if abs(m - LN2) <= BAND)
            lo, hi = min(meds) / LN2, max(meds) / LN2
        else:
            band_ok = slope_ok = False
            slope = None
            n_in = sum(1 for m in meds if m is not None and abs(m - LN2) <= BAND)
            have = [m for m in meds if m is not None]
            lo = min(have) / LN2 if have else None
            hi = max(have) / LN2 if have else None
        per.append(dict(gi=gi, gamma=gammas[gi], valido=valid,
                        medianas_oitavas=[None if m is None else m / LN2 for m in meds],
                        n_na_banda=n_in, min_oitavas=lo, max_oitavas=hi, inclinacao=slope,
                        banda_ok=band_ok, inclinacao_ok=slope_ok, C=bool(valid and band_ok and slope_ok)))

    def runs(key):
        out, start = [], None
        for i, p in enumerate(per + [dict(**{key: False})]):
            if p[key] and start is None:
                start = i
            if (not p[key]) and start is not None:
                end = i - 1
                span = math.log10(gammas[end]) - math.log10(gammas[start])
                out.append(dict(inicio_gi=start, fim_gi=end, n_pontos=end - start + 1, extensao_decadas=span,
                                gamma_min=gammas[start], gamma_max=gammas[end]))
                start = None
        return out

    runs_C = runs("C")
    runs_band = runs("banda_ok")
    runs_slope = runs("inclinacao_ok")

    def best(rs):
        return max(rs, key=lambda r: (r["n_pontos"], -r["inicio_gi"])) if rs else None

    janelas_ok = [r for r in runs_C if r["extensao_decadas"] >= WIN_DEC - WIN_TOL]
    return dict(P=bool(janelas_ok), melhor_janela=best(janelas_ok) if janelas_ok else best(runs_C),
                janelas_C=runs_C, so_banda_maior_corrida=best(runs_band), so_inclinacao_maior_corrida=best(runs_slope),
                por_gamma=per)


def evaluate_N1(n1_rows):
    por_d = {}
    for r in n1_rows:
        por_d.setdefault(r["d"], []).append(r["O"])
    dims = sorted({c[0] for c in CONFIGS})
    if sorted(por_d) != dims or any(len(v) != N1_STATES for v in por_d.values()):
        raise SystemExit("N1 INCOMPLETO")
    med = {d: statistics.median(por_d[d]) for d in dims}
    return dict(ok=all(m < N1_MAX for m in med.values()), mediana_por_d=med)


def evaluate_N3(n3):
    dims = sorted({c[0] for c in CONFIGS})
    esperados = [(d, f) for d in dims for f in (2, 4) if d % f == 0]
    casos = {(c["d"], c["frac"]): c for c in n3["casos"]}
    if sorted(casos) != sorted(esperados):
        raise SystemExit("N3 INCOMPLETO")
    pior = 0.0
    for (d, f), c in casos.items():
        alvo = LN2 if f == 2 else 2.0 * LN2
        pior = max(pior, abs(c["O"] - alvo))
    return dict(ok=pior < N3_TOL, pior_erro_abs=pior, n_casos=len(casos))


def decide(main_rows, n2_rows, n1_rows, n3):
    gam = check_complete(main_rows, "main")
    gam2 = check_complete(n2_rows, "N2")
    if gam != gam2:
        raise SystemExit("grades de gamma diferentes entre main e N2")
    P_main = evaluate_P(main_rows, gam)
    P_n2 = evaluate_P(n2_rows, gam)
    N1 = evaluate_N1(n1_rows)
    N3 = evaluate_N3(n3)
    nc_main = nonconv_fraction(main_rows)
    nc_n2 = nonconv_fraction(n2_rows)

    if not N3["ok"]:
        v, ramo = "MEASURE_BROKEN", "1: N3 falhou"
    elif nc_main > NONCONV_MAX:
        v, ramo = "INCONCLUSIVE", "2: mais de 10% da grade principal sem convergir"
    elif not P_main["P"]:
        v, ramo = "NO_UNIVERSAL_FLOOR", "3: P falso"
    elif nc_n2 > NONCONV_MAX:
        v, ramo = "INCONCLUSIVE", "4: P verdadeiro, mas mais de 10% de N2 sem convergir"
    elif P_n2["P"] or not N1["ok"]:
        v, ramo = "GENERIC_NOT_TGL", "5: P verdadeiro e (N2 satisfaz P ou N1 falhou)"
    else:
        v, ramo = "FLOOR_ONE_OCTAVE_NOT_FALSIFIED", "6: P verdadeiro, N1-N3 como previsto"
    assert v in VEREDITOS
    return dict(veredito=v, ramo=ramo, P=P_main["P"], P_N2=P_n2["P"], N1=N1, N3=N3,
                naoconv_main=nc_main, naoconv_N2=nc_n2,
                n_pontos_main=len(main_rows), n_pontos_N2=len(n2_rows),
                janela=P_main["melhor_janela"], so_banda_maior_corrida=P_main["so_banda_maior_corrida"],
                so_inclinacao_maior_corrida=P_main["so_inclinacao_maior_corrida"],
                janelas_C_main=P_main["janelas_C"],
                N2_melhor_janela=P_n2["melhor_janela"],
                por_gamma_main=P_main["por_gamma"], por_gamma_N2=P_n2["por_gamma"])


# ----------------------------------------------------------------------------- saidas

def write_curve(rows, set_name, gammas, w):
    cells = {}
    for r in rows:
        cells.setdefault((r["d"], r["nc"], r["gi"]), []).append(r)
    for (d, nc) in CONFIGS:
        for gi in range(len(gammas)):
            vals = [r["O"] for r in cells[(d, nc, gi)] if r["conv"] and math.isfinite(r["O"])]
            if vals:
                m = statistics.median(vals)
                w.writerow([set_name, d, nc, gi, repr(gammas[gi]), len(vals), repr(m), repr(m / LN2),
                            repr(min(vals) / LN2), repr(max(vals) / LN2)])
            else:
                w.writerow([set_name, d, nc, gi, repr(gammas[gi]), 0, "", "", "", ""])


def sha_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    pre_path = os.path.join(HERE, "PREREGISTRO.json")
    man_path = os.path.join(HERE, "manifesto_dados.json")
    if not (os.path.isfile(pre_path) and os.path.isfile(man_path)):
        raise SystemExit("faltam PREREGISTRO.json ou manifesto_dados.json: sem veredito")
    with open(pre_path, encoding="utf-8") as f:
        pre = json.load(f)
    with open(man_path, encoding="utf-8") as f:
        man = json.load(f)
    meu = sha_file(os.path.join(HERE, "veredito.py"))
    if pre["arquivos_sha256"].get("veredito.py") != meu:
        raise SystemExit("veredito.py NAO e o pinado no pre-registro")
    if man["preregistro_sha256"] != sha_file(pre_path):
        raise SystemExit("o PREREGISTRO.json mudou depois da rodada")
    for fn, h in man["arquivos_sha256"].items():
        if sha_file(os.path.join(HERE, fn)) != h:
            raise SystemExit("dado alterado depois da rodada: %s" % fn)

    main_rows = load_rows(os.path.join(HERE, "dados_crus_main.csv"))
    n2_rows = load_rows(os.path.join(HERE, "dados_crus_N2.csv"))
    n1_rows = load_n1(os.path.join(HERE, "dados_N1.csv"))
    with open(os.path.join(HERE, "controle_N3.json"), encoding="utf-8") as f:
        n3 = json.load(f)

    res = decide(main_rows, n2_rows, n1_rows, n3)
    gam = [p["gamma"] for p in res["por_gamma_main"]]

    res["entradas_sha256"] = dict(man["arquivos_sha256"])
    res["veredito_py_sha256"] = meu
    res["preregistro_sha256"] = sha_file(pre_path)
    res["regras"] = REGRAS
    with open(os.path.join(HERE, "veredito.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1, ensure_ascii=True)

    with open(os.path.join(HERE, "curva_O_gamma_oitavas.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["set", "d", "nc", "gi", "gamma", "n_conv", "O_mediana_nats", "O_mediana_oitavas",
                    "O_min_oitavas", "O_max_oitavas"])
        write_curve(main_rows, "main", gam, w)
        write_curve(n2_rows, "N2", gam, w)

    print("VEREDITO:", res["veredito"])
    print("ramo:", res["ramo"])
    print("P =", res["P"], "| P(N2) =", res["P_N2"], "| N1 ok =", res["N1"]["ok"], "| N3 ok =", res["N3"]["ok"])
    print("sem convergir: main %.4f | N2 %.4f" % (res["naoconv_main"], res["naoconv_N2"]))
    print("janela:", res["janela"])


if __name__ == "__main__":
    main()
