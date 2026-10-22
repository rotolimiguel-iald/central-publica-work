# -*- coding: utf-8 -*-
r"""
diagnostico_T9c.py -- F1.TEMPO, face otica. DIAGNOSTICO POST HOC (fora do pre-registro; informativo).

Feito DEPOIS de ver a FALHA do T9.o, criterio (c)-entradas (max_{k<=10^4} max_ij |T^k - (R + lambda^k (I-R))|
= 6,518e-13 > 1e-13). NAO muda o veredito registrado (T9.o = FALHA pela regra de decisao pre-registrada).
Separa duas causas numericas:
  (R) representacao: o T em float64 nao e exatamente estocastico; a soma de coluna e 1 + delta (delta calculado
      EXATAMENTE com fractions.Fraction sobre os floats); a potencia EXATA do T float da (1+delta)^k R + (a-b)^k (I-R),
      logo um desvio ~ k*delta/2 ao longo de R, mesmo sem arredondamento nenhum;
  (P) arredondamento do numpy.linalg.matrix_power (quadrados sucessivos), medido contra a potencia exata do float.
Compara tres representacoes de T: (E2) |Smat(theta_M)|^2 (a escolha fixada antes da rodada); (ALT) [[fl(1-b), b],
[b, fl(1-b)]] (a outra forma escrita no modelo do pre-registro); (EST) uma matriz float exatamente estocastica
[[1-b', b'], [b', 1-b']] com b' = fl(sin^2) arredondado a um diadico de 2^-53 tal que 1 - b' e exato (controle).
Escreve so em 2_OPTICO/diagnostico. beta lido pelo leitor do runner (bytes do um.py; sem executar).
"""
import json
import math
import os
import sys
import time
from fractions import Fraction

import numpy as np
import mpmath

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
if os.path.basename(PARENT) != "2_OPTICO" or os.path.basename(HERE) != "diagnostico":
    sys.exit("RECUSA: fora de 2_OPTICO/diagnostico")
sys.path.insert(0, PARENT)
import run_optico as RO  # noqa: E402  (so funcoes; main() nao roda na importacao)

mpmath.mp.dps = 80


def analyze(name, T, lam_f, R):
    a = Fraction(float(T[0, 0]))
    b = Fraction(float(T[0, 1]))
    sym = (T[0, 0] == T[1, 1]) and (T[0, 1] == T[1, 0])
    colsum = a + b
    delta = colsum - 1
    am = mpmath.mpf(float(T[0, 0]))
    bm = mpmath.mpf(float(T[0, 1]))
    lm = mpmath.mpf(lam_f)
    I = np.eye(2)
    rows = {}
    first_over = None
    max_float = 0.0
    k_max_float = 0
    max_exact = mpmath.mpf(0)
    for k in range(0, 10001):
        Tk = np.linalg.matrix_power(T, k)
        ref = R + lam_f ** k * (I - R)
        d_float = float(np.max(np.abs(Tk - ref)))
        if d_float > max_float:
            max_float, k_max_float = d_float, k
        if first_over is None and d_float > 1e-13:
            first_over = k
        if k in (1, 10, 100, 1000, 2000, 4096, 5000, 8192, 10000):
            p = (am + bm) ** k
            q = (am - bm) ** k
            ex = [[(p + q) / 2, (p - q) / 2], [(p - q) / 2, (p + q) / 2]]
            refm = [[(1 + lm ** k) / 2, (1 - lm ** k) / 2], [(1 - lm ** k) / 2, (1 + lm ** k) / 2]]
            d_rep = max(abs(ex[i][j] - refm[i][j]) for i in range(2) for j in range(2))
            d_pow = max(abs(mpmath.mpf(float(Tk[i, j])) - ex[i][j]) for i in range(2) for j in range(2))
            max_exact = max(max_exact, d_rep)
            rows["k=%d" % k] = {"float_matrix_power_vs_ref": d_float,
                                "potencia_EXATA_do_T_float_vs_ref (representacao)": float(d_rep),
                                "matrix_power_vs_potencia_exata (arredondamento)": float(d_pow),
                                "modelo_k*|delta|/2": float(abs(delta)) * k / 2}
    return {"T": T, "simetrica_exata": bool(sym), "soma_de_coluna_exata_menos_1 (delta)": float(delta),
            "delta_em_unidades_de_2^-53": float(delta * 2 ** 53),
            "a_menos_b_float": float(T[0, 0] - T[0, 1]), "lambda_float": lam_f,
            "max_k<=10^4_float": max_float, "k_do_max": k_max_float,
            "primeiro_k_com_desvio_>1e-13": first_over,
            "passaria_o_criterio_(c)_entradas_<=1e-13": bool(max_float <= 1e-13),
            "por_k": rows}


def main():
    t0 = time.time()
    _, prereg, _ = RO.preflight()
    binfo = RO.read_beta(prereg)
    M = RO.build_model(binfo["beta_runtime"])
    beta = M["beta"]
    lam = M["lam"]
    R = M["R"]
    T_e2 = M["T"]
    T_alt = np.array([[1 - beta, beta], [beta, 1 - beta]])
    b2 = float(T_e2[0, 1])
    bq = round(b2 * 2 ** 53) / 2 ** 53
    T_est = np.array([[1 - bq, bq], [bq, 1 - bq]])
    est_exact = (Fraction(1 - bq) + Fraction(bq) == 1)
    out = {"documento": "DIAGNOSTICO POST HOC da FALHA do T9.o (c)-entradas — fora do pre-registro; informativo; "
                        "nao muda o veredito registrado",
           "beta_runtime": beta, "beta_confere": binfo["confere"], "um_py_sha256": binfo["um_py_sha256"],
           "lambda_float": lam,
           "E2_|S|^2 (escolha fixada antes da rodada)": analyze("E2", T_e2, lam, R),
           "ALT_[[fl(1-b), b],[b, fl(1-b)]] (outra forma escrita no modelo)": analyze("ALT", T_alt, lam, R),
           "EST_exatamente_estocastica (controle; b' diadico 2^-53)": dict(analyze("EST", T_est, 1 - 2 * bq, R),
                                                                           soma_exata_igual_1=bool(est_exact),
                                                                           b_linha=bq, dif_b_linha_menos_beta=bq - beta),
           "leitura": ("A identidade T^k = R + lambda^k (I - R) e EXATA para a matriz real T = R + lambda(I - R) (o kernel "
                       "decide). Em float64, (i) a matriz T guardada nao e exatamente estocastica (delta != 0) e a sua "
                       "potencia EXATA ja se afasta de R + lambda^k (I-R) por ~k|delta|/2 ao longo de R; (ii) o "
                       "matrix_power acrescenta arredondamento que tambem cresce com k na direcao neutra (autovalor 1). "
                       "O contraste (T8.o (a)), que cancela o modo comum, passa a 1e-13. A F1.ATRATOR ja mediu esta "
                       "deriva: ||T^4096 - R|| = 5,3e-13 em float64."),
           "segundos": round(time.time() - t0, 1)}
    path = os.path.join(HERE, "DIAGNOSTICO_T9c.json")
    data = (json.dumps(RO.jsonable(out), ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, path)
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != "por_k"})
                      for k, v in RO.jsonable(out).items()}, ensure_ascii=False, indent=1))
    print("sha256", RO.sha256_bytes(data), len(data))


if __name__ == "__main__":
    main()
