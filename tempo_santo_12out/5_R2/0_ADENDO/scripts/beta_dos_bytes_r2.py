# -*- coding: utf-8 -*-
"""beta em RUNTIME a partir dos BYTES do um.py (sem executar o um.py) — pre-registrador da R2 (F1.TEMPO).

Le o literal de ALPHA_FINE_CODATA_2018 (l.5557, dentro do texto embutido _NIVEL2_MCMC_FILES) e o de
SEALED_CODATA_ALPHA (l.95, a atribuicao de TOPO), confere que sao iguais, confere a linha de BETA_TGL
(l.5559: ALPHA_FINE_CODATA_2018 * ONE * math.sqrt(math.e)) e calcula beta = alpha * ONE * sqrt(e) em float64
(a mesma expressao do um.py) e tambem em decimal de 200 digitos A PARTIR DO LITERAL (para o caminho exato
do ADENDO uniforme). O valor de conferencia e LIDO do PREREGISTRO.json congelado (nunca digitado aqui).
Estatuto: [DERIVED — lido nos bytes e calculado em runtime; nao e medida]. Saida: saidas/BETA_RUNTIME_R2.json.
Uso: python -I -X utf8 beta_dos_bytes_r2.py
"""
import ast
import decimal
import hashlib
import json
import math
import os
import re
import sys

UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
PRE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO\PREREGISTRO.json"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas",
                   "BETA_RUNTIME_R2.json")


def linhas_de(b, nome):
    rx = re.compile(rb"^(" + re.escape(nome.encode()) + rb")\s*=\s*(.+?)\s*(#.*)?$", re.M)
    achados = []
    for m in rx.finditer(b):
        n = b.count(b"\n", 0, m.start()) + 1
        achados.append((n, m.group(2).decode().strip()))
    return achados


def main():
    b = open(UM, "rb").read()
    sha = hashlib.sha256(b).hexdigest()
    a_fine = linhas_de(b, "ALPHA_FINE_CODATA_2018")
    a_seal = linhas_de(b, "SEALED_CODATA_ALPHA")
    a_one = [x for x in linhas_de(b, "ONE") if x[0] == 5558]
    a_beta = [x for x in linhas_de(b, "BETA_TGL") if x[0] == 5559]
    fine = [x for x in a_fine if x[0] == 5557]
    seal = [x for x in a_seal if x[0] == 95]
    if not fine or not seal:
        raise SystemExit("FALHA VISIVEL: linhas de alpha nao encontradas onde esperado: %r %r" % (a_fine, a_seal))
    lit_fine = fine[0][1]
    lit_seal = seal[0][1]
    alpha_fine = float(ast.literal_eval(lit_fine))
    alpha_seal = float(ast.literal_eval(lit_seal))
    linhas = b.split(b"\n")
    ini = next(i + 1 for i, L in enumerate(linhas) if L.startswith(b"_NIVEL2_MCMC_FILES = {"))
    fim = next(i + 1 for i in range(ini, len(linhas)) if linhas[i].startswith(b"def materialize_nivel2_mcmc"))
    ONE = 1.0
    beta = alpha_fine * ONE * math.sqrt(math.e)
    # caminho exato (200 digitos) a partir do LITERAL, nao do float
    decimal.getcontext().prec = 200
    D = decimal.Decimal
    sqrt_e_200 = D(1).exp().sqrt()
    beta_200 = D(lit_fine) * D(1) * sqrt_e_200
    conf = json.load(open(PRE, encoding="utf-8"))["beta"]["beta_conferencia"]
    out = {
        "um_py": UM, "um_py_sha256": sha, "um_py_bytes": len(b), "um_py_executado": False,
        "ALPHA_FINE_CODATA_2018": {"linha": 5557, "literal": lit_fine,
                                   "todas_as_ocorrencias_no_inicio_de_linha": a_fine},
        "SEALED_CODATA_ALPHA": {"linha": 95, "literal": lit_seal,
                                "todas_as_ocorrencias_no_inicio_de_linha": a_seal},
        "ONE_l5558": a_one[0][1] if a_one else None,
        "BETA_TGL_l5559": a_beta[0][1] if a_beta else None,
        "expressao_BETA_TGL_confere": bool(a_beta and a_beta[0][1] == "ALPHA_FINE_CODATA_2018 * ONE * math.sqrt(math.e)"),
        "alphas_iguais": alpha_fine == alpha_seal and lit_fine == lit_seal,
        "envoltorio_NIVEL2_MCMC_FILES": {"linha_inicio": ini, "linha_def_seguinte": fim,
                                         "l5557_dentro": ini < 5557 < fim},
        "beta_runtime_float64": beta,
        "beta_runtime_float64_hex": beta.hex(),
        "beta_200_digitos_do_literal": str(beta_200),
        "sqrt_e_200_digitos": str(sqrt_e_200),
        "beta_200_menos_float_abs": str(abs(beta_200 - D(beta))),
        "beta_conferencia_lida_do_PREREGISTRO": conf,
        "diferenca_abs": abs(beta - conf),
        "confere_1e-15": abs(beta - conf) <= 1e-15,
        "estatuto": "[DERIVED — lido nos bytes do um.py e calculado em runtime (alpha * ONE * sqrt(e)); nao e medida; "
                    "a conferencia so confere; a l.5557 e embutida (_NIVEL2_MCMC_FILES) e a atribuicao de topo e a l.95, "
                    "de mesmo literal]",
    }
    with open(OUT + ".tmp", "wb") as f:
        f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(OUT + ".tmp", OUT)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
