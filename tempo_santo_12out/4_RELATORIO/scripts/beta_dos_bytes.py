# -*- coding: utf-8 -*-
"""beta em RUNTIME a partir dos BYTES do um.py (sem executar o um.py).

Le o literal de ALPHA_FINE_CODATA_2018 (l.5557, dentro do texto embutido _NIVEL2_MCMC_FILES) e o de
SEALED_CODATA_ALPHA (l.95, atribuicao de topo), confere que sao iguais, e calcula
beta = alpha * ONE * sqrt(e), a mesma expressao do um.py. O valor de conferencia e LIDO do
PREREGISTRO.json congelado (nunca digitado aqui). Saida: saidas/BETA_RUNTIME_RELATORIO.json.
"""
import ast
import hashlib
import json
import math
import os
import re
import sys

UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
PRE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO\PREREGISTRO.json"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas",
                   "BETA_RUNTIME_RELATORIO.json")


def linha_de(b, nome):
    rx = re.compile(rb"^(" + re.escape(nome.encode()) + rb")\s*=\s*([0-9.eE+-]+)", re.M)
    achados = []
    for m in rx.finditer(b):
        n = b.count(b"\n", 0, m.start()) + 1
        achados.append((n, m.group(2).decode()))
    return achados


def main():
    b = open(UM, "rb").read()
    sha = hashlib.sha256(b).hexdigest()
    a_fine = linha_de(b, "ALPHA_FINE_CODATA_2018")
    a_seal = linha_de(b, "SEALED_CODATA_ALPHA")
    # a linha 5557 e a esperada pelo pre-registro; a 95 e a de topo
    fine = [x for x in a_fine if x[0] == 5557]
    seal = [x for x in a_seal if x[0] == 95]
    if not fine or not seal:
        raise SystemExit("FALHA VISIVEL: linhas de alpha nao encontradas onde esperado: %r %r" % (a_fine, a_seal))
    alpha_fine = float(ast.literal_eval(fine[0][1]))
    alpha_seal = float(ast.literal_eval(seal[0][1]))
    # confere o envoltorio: a l.5557 cai dentro de _NIVEL2_MCMC_FILES?
    linhas = b.split(b"\n")
    ini = next(i + 1 for i, L in enumerate(linhas) if L.startswith(b"_NIVEL2_MCMC_FILES = {"))
    fim = next(i + 1 for i in range(ini, len(linhas)) if linhas[i].startswith(b"def materialize_nivel2_mcmc"))
    ONE = 1.0
    beta = alpha_fine * ONE * math.sqrt(math.e)
    conf = json.load(open(PRE, encoding="utf-8"))["beta"]["beta_conferencia"]
    out = {
        "um_py": UM, "um_py_sha256": sha, "um_py_bytes": len(b), "um_py_executado": False,
        "ALPHA_FINE_CODATA_2018": {"linha": fine[0][0], "literal": fine[0][1],
                                   "todas_as_ocorrencias_no_inicio_de_linha": a_fine},
        "SEALED_CODATA_ALPHA": {"linha": seal[0][0], "literal": seal[0][1]},
        "alphas_iguais": alpha_fine == alpha_seal,
        "envoltorio_NIVEL2_MCMC_FILES": {"linha_inicio": ini, "linha_def_seguinte": fim,
                                         "l5557_dentro": ini < 5557 < fim},
        "beta_runtime": beta,
        "beta_conferencia_lida_do_PREREGISTRO": conf,
        "diferenca_abs": abs(beta - conf),
        "confere_1e-15": abs(beta - conf) <= 1e-15,
        "estatuto": "[DERIVED — lido nos bytes e calculado em runtime; nao e medida; a conferencia so confere]",
    }
    with open(OUT + ".tmp", "wb") as f:
        f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(OUT + ".tmp", OUT)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
