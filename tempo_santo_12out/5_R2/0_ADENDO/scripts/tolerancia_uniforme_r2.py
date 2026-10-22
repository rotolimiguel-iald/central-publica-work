# -*- coding: utf-8 -*-
r"""ADENDO UNIFORME de tolerancias (O-f e T9.o(c)) — implementacao de REFERENCIA, normativa, do pre-registrador da R2.

Este arquivo E a definicao da regra (o codigo e a especificacao; o seu sha256 entra no FREEZE_R2.json).
So biblioteca padrao (fractions, decimal, math, json): roda com `python -I -X utf8`.

REGRA UNIFORME (uma so formula para os dois testes; constantes DERIVADAS, nao ajustadas ao resultado):

  (i)  caminho EXATO — decimal de 200 digitos (mpmath, mp.dps = 200; conferencia cruzada com o modulo `decimal`
       da biblioteca padrao a prec = 200); potencia por multiplicacao repetida (nunca pela identidade testada);
       tolerancia 1e-150 (absoluta em T9.o'(c), relativa em O-f'). Controle do caminho exato: a mp.dps = 20 o
       mesmo teste TEM de FALHAR a 1e-150 (a tolerancia nao e vazia).

  (ii) caminho FLOAT64 — para a quantidade testada Q_k apos k passos:
           |Q_k^float − Q_k^ideal|  <=  tau(k) := S_k * [ k*( w*|delta| + m*eps ) + c*eps ],   eps = 2^-52,
       com, por teste (fixado AGORA, antes do reensaio):
         delta : desvio EXATO (racional/decimal) do autovalor do modo testado da matriz float GUARDADA em relacao
                 ao autovalor ideal — o piso de representacao;
         w     : peso do modo testado na quantidade Q_k;
         m     : constante de arredondamento por passo, em unidades de eps, pelo limite de erro direto de Higham
                 (Accuracy and Stability of Numerical Algorithms, 2a ed., 2002, cap. 3; gamma_n = n*u/(1-n*u),
                 u = eps/2) [KNOWN];
         c     : arredondamentos da avaliacao da REFERENCIA ideal em float (pow/exp/sqrt/hypot), em unidades de eps;
         S_k   : escala (1 = absoluta; |Q_k^ideal| = relativa).
       T9.o'(c): Q_k = entrada (i,j) de T^k por numpy.linalg.matrix_power (E2: T = |S|^2 guardada); S_k = 1;
                 delta_T = (a + b) − 1 EXATO (Fraction) com a = T[0][0], b = T[0][1] floats guardados (modo neutro R);
                 w = 1/2 (R = J/2: o modo neutro pesa 1/2 em cada entrada); m = 1 (produto de matrizes 2x2 positivas:
                 gamma_2 ~ 2u = eps por multiplicacao, k multiplicacoes ou log2(k) quadrados — ambos <= k*eps a 1a ordem,
                 sem cancelamento); c = 2 (lam**k e a soma R + lam^k (I-R)).
                 Em k = 0 exige-se igualdade exata (T^0 = I = R + (I − R)).
                 => tau_T(k) = k*(|delta_T|/2 + eps) + 2*eps : e LITERALMENTE "k*|delta|/2 mais margem fixada agora".
       O-f'    : Q_k = ||B(1)^k (1,−1)|| pela orbita escalar IEEE (E4); S_k = sqrt(2)*e^{−k} (relativa);
                 delta_B = (mu_B − e^{−1})/e^{−1}, mu_B = fl(cosh 1) − fl(sinh 1) EXATO (Fraction -> Decimal 200), e^{−1} a
                 200 digitos (modo (1,−1), autovalor ideal e^{−1}); w = 1; m = (e^2 + 1)/2 (num passo x' = fl(fl(c1*x) +
                 fl(s1*y)) com y = −x: erro relativo <= u*(c1 + s1)/(c1 − s1) + u = u*(e^2 + 1); em unidades de eps,
                 (e^2 + 1)/2); c = 3 (hypot, sqrt(2), exp(−k)).
                 => tau_B(k) = k*(|delta_B| + ((e^2+1)/2)*eps) + 3*eps, relativa.
       APLICACAO IGUAL: a mesma formula, os mesmos tipos de parametro, a mesma derivacao; nenhum parametro ajustado ao
       resultado da R1. Os parametros ficam gravados em saidas/TOLERANCIA_UNIFORME_R2.json (sha256 no FREEZE_R2).

  Controles numericos do ADENDO (tinham de falhar / de passar, registrados antes):
       C-UNIF-a : O-f' pelo caminho numpy.linalg.matrix_power (sela mal condicionada: eps*e^{2k}) TEM de FALHAR tau_B em
                  algum k <= 10 (R1 anexo: rel 1,12e-14 em k = 3; 6,53e-9 em k = 10). Se passar, a tolerancia virou cheque
                  em branco: INVALIDO.
       C-UNIF-b : T9.o'(c) com a matriz ALT [[fl(1−b), b],[b, fl(1−b)]] e com a EST exatamente estocastica (do diagnostico
                  da R1) TEM de passar a MESMA tau_T (a regra nao depende da representacao): se alguma falhar, registra-se
                  (nao e licenca para trocar de representacao: a representacao do veredito e a E2).
       C-UNIF-c : o caminho exato a mp.dps = 20 TEM de FALHAR a 1e-150 (tolerancia nao vazia).
       C-UNIF-d : mpmath (dps 200) e decimal (prec 200) TEM de concordar a 1e-150 nas mesmas quantidades.

Uso: python -I -X utf8 tolerancia_uniforme_r2.py   -> saidas/TOLERANCIA_UNIFORME_R2.json
"""
import decimal
import json
import math
import os
import sys
from fractions import Fraction

W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
RES = os.path.join(W, "2_OPTICO", "RESULTADO_OPTICO.json")
DIAG = os.path.join(W, "2_OPTICO", "diagnostico", "DIAGNOSTICO_T9c.json")
ACH = os.path.join(W, "2_OPTICO", "ACHADOS_FORA_DO_PREREGISTRO.json")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas",
                   "TOLERANCIA_UNIFORME_R2.json")

EPS = 2.0 ** -52          # epsilon de maquina (distancia 1 -> proximo float)
U = 2.0 ** -53            # unit roundoff
decimal.getcontext().prec = 200
D = decimal.Decimal


# ----------------------------------------------------------------------------- a regra (normativa)
def tau(k, delta_abs, w, m, c, S=1.0):
    """tau(k) = S * [ k*( w*|delta| + m*eps ) + c*eps ]  — em float64, por k >= 1."""
    if k < 1:
        raise ValueError("k >= 1 (em k = 0 exige-se igualdade exata)")
    return S * (k * (w * abs(delta_abs) + m * EPS) + c * EPS)


def params_T(T):
    """delta_T exato (Fraction) a partir da matriz float GUARDADA (soma de coluna − 1); w, m, c fixos."""
    a = Fraction(float(T[0][0]))
    b = Fraction(float(T[0][1]))
    sym = (T[0][0] == T[1][1]) and (T[0][1] == T[1][0])
    delta = a + b - 1
    return {"a_hex": float(T[0][0]).hex(), "b_hex": float(T[0][1]).hex(), "simetrica_exata": bool(sym),
            "delta_T_exato_fraction": str(delta), "delta_T": float(delta),
            "delta_T_em_unidades_de_2^-53": float(delta * 2 ** 53),
            "a_menos_b_exato_vs_lambda_float": None, "w": 0.5, "m": 1.0, "c": 2.0, "escala": "absoluta (S_k = 1)"}


def params_B(s=1.0):
    """delta_B relativo (Decimal 200) a partir dos floats fl(cosh s), fl(sinh s) deste runtime; w, m, c fixos."""
    c1 = math.cosh(s)
    s1 = math.sinh(s)
    mu = Fraction(c1) - Fraction(s1)                      # autovalor EXATO do modo (1,−1) da B float
    mu_d = D(mu.numerator) / D(mu.denominator)
    ideal = (-D(s)).exp()                                # e^{−s} a 200 digitos
    delta_rel = (mu_d - ideal) / ideal
    det_minus_1 = Fraction(c1) ** 2 - Fraction(s1) ** 2 - 1
    m = (math.exp(2 * s) + 1.0) / 2.0
    return {"s": s, "cosh_hex": c1.hex(), "sinh_hex": s1.hex(), "cosh": c1, "sinh": s1,
            "mu_B_exato_fraction": str(mu), "mu_B_decimal200": str(mu_d), "e^-s_decimal200": str(ideal),
            "delta_B_rel_decimal200": str(delta_rel), "delta_B_rel": float(delta_rel),
            "det_B_float_menos_1_exato": str(det_minus_1), "det_B_float_menos_1": float(det_minus_1),
            "w": 1.0, "m": m, "m_formula": "(e^{2s} + 1)/2", "c": 3.0, "escala": "relativa (S_k = sqrt(2) e^{-ks})"}


def main():
    res = json.load(open(RES, encoding="utf-8"))
    diag = json.load(open(DIAG, encoding="utf-8"))
    ach = json.load(open(ACH, encoding="utf-8"))
    T = res["modelo"]["T"]
    lam = res["modelo"]["lambda"]
    pT = params_T(T)
    pT["a_menos_b_exato_vs_lambda_float"] = {"a_menos_b_float": float(T[0][0] - T[0][1]), "lambda_float": lam,
                                             "iguais": float(T[0][0] - T[0][1]) == lam,
                                             "nota": "o modo lambda nao e o modo testado pelo criterio (c)-entradas; informativo"}
    pB = params_B(1.0)

    # tabela tau_T(k) e predicoes a partir dos numeros da R1 (diagnostico, E2)
    e2 = diag["E2_|S|^2 (escolha fixada antes da rodada)"]
    assert e2["T"] == T, "a matriz do diagnostico nao e a guardada"
    ks = [1, 10, 100, 1000, 1529, 2000, 4096, 5000, 8192, 10000]
    tabela_T = []
    for k in ks:
        t = tau(k, pT["delta_T"], pT["w"], pT["m"], pT["c"])
        row = {"k": k, "tau_T(k)": t, "k*|delta_T|/2": k * abs(pT["delta_T"]) / 2, "k*eps": k * EPS}
        key = "k=%d" % k
        if key in e2["por_k"]:
            med = e2["por_k"][key]["float_matrix_power_vs_ref"]
            row["R1_medido_float_matrix_power_vs_ref"] = med
            row["R1_passaria_tau_T"] = med <= t
            row["razao_medido/tau"] = med / t
            # conferencia: a formula k*|delta|/2 deste script == a do diagnostico
            row["k*|delta|/2_confere_com_diagnostico"] = abs(row["k*|delta_T|/2"] - e2["por_k"][key]["modelo_k*|delta|/2"]) <= 1e-30
        tabela_T.append(row)
    maxk = e2["max_k<=10^4_float"]
    pred_T = {"R1_max_k<=1e4": maxk, "k_do_max": e2["k_do_max"], "tau_T(1e4)": tau(10000, pT["delta_T"], 0.5, 1.0, 2.0),
              "predicao_T9.o'(c)_float_E2": "PASSA" if maxk <= tau(10000, pT["delta_T"], 0.5, 1.0, 2.0) else "FALHA",
              "razao": maxk / tau(10000, pT["delta_T"], 0.5, 1.0, 2.0),
              "nota": "predicao a partir do valor da R1 (mesma maquina, mesmo numpy): o reensaio decide; o criterio e por k (todo k <= 1e4)"}
    # C-UNIF-b: ALT e EST com a mesma tau_T (delta medido de CADA matriz guardada no diagnostico)
    cunif_b = {}
    for nome, key in (("ALT", "ALT_[[fl(1-b), b],[b, fl(1-b)]] (outra forma escrita no modelo)"),
                      ("EST", "EST_exatamente_estocastica (controle; b' diadico 2^-53)")):
        blk = diag[key]
        p = params_T(blk["T"])
        rows = {}
        okall = True
        for kk, v in blk["por_k"].items():
            k = int(kk.split("=")[1])
            if k < 1:
                continue
            t = tau(k, p["delta_T"], 0.5, 1.0, 2.0)
            ok = v["float_matrix_power_vs_ref"] <= t
            okall = okall and ok
            rows[kk] = {"medido": v["float_matrix_power_vs_ref"], "tau_T": t, "ok": ok}
        cunif_b[nome] = {"delta_T": p["delta_T"], "por_k_amostrado": rows, "passa_nos_k_amostrados": okall,
                         "max_k<=1e4_R1": blk["max_k<=10^4_float"], "tau_T(1e4)": tau(10000, p["delta_T"], 0.5, 1.0, 2.0),
                         "predicao": "PASSA" if blk["max_k<=10^4_float"] <= tau(10000, p["delta_T"], 0.5, 1.0, 2.0) else "FALHA"}

    # tabela tau_B(k) relativa, k = 1..10 (obrigatorio) e 100 (informativo), e predicoes da R1 (E4) e do controle
    of = res["subitens_oticos"]["T4.o"]["medidas"]["Of"]["float64_IEEE_escalar"]
    paths = ach["itens"]["O-f_caminhos_aritmeticos_float64"]["por_k"]
    tabela_B = []
    first_fail_mp = None
    first_fail_blas = None
    okE4 = True
    for k in list(range(1, 13)) + [100]:
        t = tau(k, pB["delta_B_rel"], pB["w"], pB["m"], pB["c"])
        row = {"k": k, "tau_B_rel(k)": t, "k*|delta_B|": k * abs(pB["delta_B_rel"]), "k*m*eps": k * pB["m"] * EPS}
        key = "k=%d" % k
        if key in of:
            row["R1_E4_rel"] = of[key]["rel"]
            row["R1_E4_passaria_tau_B"] = of[key]["rel"] <= t
            if k <= 10:
                okE4 = okE4 and (of[key]["rel"] <= t)
        if key in paths:
            row["R1_anexo_rel_matrix_power"] = paths[key]["rel_matrix_power"]
            row["R1_anexo_rel_BLAS"] = paths[key]["rel_BLAS_B@v"]
            row["matrix_power_passaria_tau_B"] = paths[key]["rel_matrix_power"] <= t
            row["BLAS_passaria_tau_B"] = paths[key]["rel_BLAS_B@v"] <= t
            if first_fail_mp is None and paths[key]["rel_matrix_power"] > t:
                first_fail_mp = k
            if first_fail_blas is None and paths[key]["rel_BLAS_B@v"] > t:
                first_fail_blas = k
        tabela_B.append(row)
    pred_B = {"predicao_O-f'_float_E4_k<=10": "PASSA" if okE4 else "FALHA",
              "R1_E4_max_rel_k<=10": max(of["k=%d" % k]["rel"] for k in range(1, 11)),
              "tau_B_rel(10)": tau(10, pB["delta_B_rel"], 1.0, pB["m"], 3.0),
              "C-UNIF-a_predicao": {"caminho": "numpy.linalg.matrix_power(B,k) @ (1,-1)",
                                    "primeiro_k_que_FALHA_tau_B_pelos_numeros_da_R1": first_fail_mp,
                                    "esperado": "FALHA em algum k <= 10 (predito: desde k = %s)" % first_fail_mp},
              "BLAS_B@v_informativo": {"primeiro_k_que_FALHA_tau_B_pelos_numeros_da_R1_k<=12": first_fail_blas,
                                       "nota": "informativo, sem veredito (como na R1)"}}

    # autotestes da regra
    auto = {
        "tau_T_crescente_em_k": all(tabela_T[i]["tau_T(k)"] < tabela_T[i + 1]["tau_T(k)"] for i in range(len(tabela_T) - 1)),
        "tau_T(k) >= k*|delta_T|/2": all(r["tau_T(k)"] >= r["k*|delta_T|/2"] for r in tabela_T),
        "k*|delta|/2 confere com o diagnostico em todo k amostrado": all(r.get("k*|delta|/2_confere_com_diagnostico", True) for r in tabela_T),
        "tau_B_crescente_em_k": all(tabela_B[i]["tau_B_rel(k)"] < tabela_B[i + 1]["tau_B_rel(k)"] for i in range(len(tabela_B) - 1)),
        "eps": EPS, "u": U,
    }
    out = {
        "documento": "ADENDO UNIFORME de tolerancias (O-f e T9.o(c)) — parametros DERIVADOS e tabela tau(k); implementacao de referencia",
        "estatuto": "[INPUT da gerencia — regra de pre-registro R2]; delta_T e delta_B [DERIVED: lidos da matriz guardada / do runtime e calculados em aritmetica exata]; m por Higham [KNOWN]",
        "regra": {
            "float64": "|Q_k^float − Q_k^ideal| <= tau(k) := S_k * [ k*( w*|delta| + m*eps ) + c*eps ], eps = 2^-52, k >= 1; k = 0 exige igualdade exata",
            "exato": "mpmath mp.dps = 200 (conferencia cruzada: decimal prec = 200), potencia por multiplicacao repetida; tolerancia 1e-150 (absoluta em T9.o'(c); relativa em O-f')",
            "controles": ["C-UNIF-a", "C-UNIF-b", "C-UNIF-c", "C-UNIF-d"],
        },
        "eps": EPS, "u": U,
        "T9.o'(c)": {"parametros": pT, "tabela": tabela_T, "predicao": pred_T, "C-UNIF-b": cunif_b},
        "O-f'": {"parametros": pB, "tabela": tabela_B, "predicao": pred_B},
        "autotestes": auto,
        "fontes": {"RESULTADO_OPTICO.json": RES, "DIAGNOSTICO_T9c.json": DIAG, "ACHADOS_FORA_DO_PREREGISTRO.json": ACH},
    }
    with open(OUT + ".tmp", "wb") as f:
        f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(OUT + ".tmp", OUT)
    sys.stdout.reconfigure(encoding="utf-8")
    resumo = {"delta_T": pT["delta_T"], "delta_T_2^-53": pT["delta_T_em_unidades_de_2^-53"],
              "tau_T(1e4)": pred_T["tau_T(1e4)"], "pred_T": pred_T["predicao_T9.o'(c)_float_E2"], "razao_T": pred_T["razao"],
              "delta_B_rel": pB["delta_B_rel"], "m_B": pB["m"], "tau_B(10)": pred_B["tau_B_rel(10)"],
              "pred_B_E4": pred_B["predicao_O-f'_float_E4_k<=10"], "R1_E4_max": pred_B["R1_E4_max_rel_k<=10"],
              "C-UNIF-a_primeiro_k": first_fail_mp, "BLAS_primeiro_k": first_fail_blas,
              "C-UNIF-b": {k: v["predicao"] for k, v in cunif_b.items()}, "autotestes": auto}
    print(json.dumps(resumo, ensure_ascii=False, indent=1))
    for r in tabela_T:
        print("T k=%6d tau=%.3e  R1=%s  ok=%s" % (r["k"], r["tau_T(k)"], r.get("R1_medido_float_matrix_power_vs_ref"), r.get("R1_passaria_tau_T")))
    for r in tabela_B:
        print("B k=%4d tau_rel=%.3e  E4=%s  mp=%s  mp_ok=%s" % (r["k"], r["tau_B_rel(k)"], r.get("R1_E4_rel"), r.get("R1_anexo_rel_matrix_power"), r.get("matrix_power_passaria_tau_B")))


if __name__ == "__main__":
    main()
