# -*- coding: utf-8 -*-
"""β em runtime a partir dos BYTES do um.py (o programa NÃO é executado; nada é importado dele).

Lê a atribuição `ALPHA_FINE_CODATA_2018 = <literal>` na linha fixada pelo pré-registro (l.5557) e confere a
atribuição de topo `SEALED_CODATA_ALPHA` (l.95). β = α·√e calculado aqui; o valor de conferência só confere.
Estatuto: [DERIVED — lido nos bytes e calculado em runtime] (não é medida).
Também instancia, com o β de runtime, as hipóteses GENÉRICAS que a pedra deixa em parâmetro (γ > 0, κ ≠ 0, …):
o kernel prova a forma; o runtime lê β.
Uso: python -I beta_runtime.py <saida.json>
"""
import hashlib
import json
import math
import re
import sys

UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
UM_SHA_PREREG = "8e7b9927ceae64b8b6812019f77cca24c08296222ae7968af41baf2fe7a67dc6"
CONFERENCIA = 0.012031300400803142  # só confere; nunca é motor


def main(out):
    b = open(UM, "rb").read()
    sha = hashlib.sha256(b).hexdigest()
    lines = b.split(b"\n")
    l5557 = lines[5556].decode("utf-8")
    m = re.match(r"^ALPHA_FINE_CODATA_2018 = ([0-9.eE+-]+)\s*$", l5557.rstrip("\r"))
    if not m:
        raise SystemExit("FALHA VISÍVEL: a l.5557 não é a atribuição de ALPHA_FINE_CODATA_2018")
    lit = m.group(1)
    alpha = float(lit)
    l95 = lines[94].decode("utf-8")
    m95 = re.match(r"^SEALED_CODATA_ALPHA = ([0-9.eE+-]+)", l95)
    alpha95 = float(m95.group(1)) if m95 else None
    l5511 = lines[5510].decode("utf-8")
    beta = alpha * math.sqrt(math.e)
    g01 = beta * abs(math.log((1.0 - beta) / beta))
    lam = 1.0 - 2.0 * beta
    theta = math.asin(math.sqrt(beta))
    omega1 = math.log((1.0 - beta) / beta)
    res = {
        "um_py": UM, "um_py_bytes": len(b), "um_py_sha256": sha,
        "um_py_sha256_confere_preregistro": sha == UM_SHA_PREREG,
        "um_py_executado": False,
        "linha_alpha": 5557, "texto_l5557": l5557.rstrip("\r"), "alpha_literal": lit, "alpha": alpha,
        "linha_5511_inicio_do_bloco_embutido": l5511[:40],
        "l5557_dentro_do_bloco_embutido_NIVEL2": l5511.startswith("_NIVEL2_MCMC_FILES = {"),
        "nota_bloco": ("a l.5557 fica dentro do texto embutido _NIVEL2_MCMC_FILES (início conferido aqui na l.5511; "
                       "o fim l.6027 é [DECLARADO pelos auditores da rodada 1]); a atribuição de topo é a l.95"),
        "texto_l95": l95.rstrip("\r")[:80], "alpha_l95": alpha95, "alpha_l95_igual_l5557": alpha95 == alpha,
        "beta_runtime": beta, "beta_conferencia": CONFERENCIA, "diferenca_abs": abs(beta - CONFERENCIA),
        "confere_1e-15": abs(beta - CONFERENCIA) <= 1e-15,
        "estatuto": "[DERIVED — lido nos bytes e calculado em runtime; a conferência só confere; o kernel não contém β]",
        "instanciacao_das_hipoteses_genericas": {
            "T7b_gamma_davies_g01": g01, "T7b_gamma_pos": g01 > 0,
            "T8a_g01_reescala": "g01 > 0 permite s = g01·t (g_{01} normalizado a 1 em coherenceScaling)",
            "T10_kappa_omega1": omega1, "T10_kappa_ne_0": omega1 != 0.0,
            "T11_lambda": lam, "T11_lambda_em_0_1": 0.0 < lam < 1.0,
            "theta_M": theta, "sin_theta_M_ne_0": math.sin(theta) != 0.0, "cos_theta_M_ne_0": math.cos(theta) != 0.0,
        },
    }
    with open(out + ".tmp", "w", encoding="utf-8") as fo:
        json.dump(res, fo, ensure_ascii=False, indent=1)
    import os
    os.replace(out + ".tmp", out)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("um_py_sha256_confere_preregistro", "alpha_literal", "alpha_l95_igual_l5557",
                                          "l5557_dentro_do_bloco_embutido_NIVEL2", "beta_runtime", "diferenca_abs",
                                          "confere_1e-15")}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
