"""beta em RUNTIME para a face kernel da F1.TEMPO (construtor do kernel).
Le, nos BYTES do um.py (sem executa-lo), a atribuicao de ALPHA_FINE_CODATA_2018 por regex, calcula beta = alpha*sqrt(e)
e confere com o valor de CONFERENCIA do pre-registro (que nunca e motor). Depois confere que as HIPOTESES dos teoremas
do kernel ficam habitadas quando o runtime instancia os parametros genericos com beta:
  T7.b  gamma = g01 = beta*|ln((1-beta)/beta)| > 0  (taxa de Davies)  e  t > 0
  T8.a  g_{i0 j0} = 1 apos reescalar o tempo por g01 (s = g01*t)
  T11   lambda = 1 - 2*beta em (0, 1)  (o canal otico contrai estritamente)
O kernel prova a FORMA em gamma/t/g; aqui so se mede que beta cai dentro das hipoteses. Nenhum dado observado.
Uso: python -I beta_runtime.py <saida.json>"""
import hashlib
import json
import math
import re
import sys

UM_PY = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
UM_PY_SHA256_PREREG = "8e7b9927ceae64b8b6812019f77cca24c08296222ae7968af41baf2fe7a67dc6"
BETA_CONFERENCIA = 0.012031300400803142  # so conferencia (pre-registro), nunca motor

with open(UM_PY, "rb") as fh:
    b = fh.read()
sha = hashlib.sha256(b).hexdigest()
lines = b.split(b"\n")
pat = re.compile(rb"^\s*ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)\s*\r?$")
hits = [(i + 1, m.group(1).decode()) for i, ln in enumerate(lines) for m in [pat.match(ln)] if m]
if len(hits) != 1:
    raise SystemExit(f"FALHA DE LEITURA: {len(hits)} atribuicoes de ALPHA_FINE_CODATA_2018")
linha, literal = hits[0]
alpha = float(literal)
beta = alpha * math.sqrt(math.e)
lam = 1.0 - 2.0 * beta
g01 = beta * abs(math.log((1.0 - beta) / beta))
out = {
    "um_py": UM_PY, "um_py_bytes": len(b), "um_py_sha256": sha,
    "um_py_sha256_confere_preregistro": sha == UM_PY_SHA256_PREREG,
    "linha_alpha": linha, "alpha_literal": literal, "alpha": alpha,
    "beta_runtime": beta, "beta_conferencia": BETA_CONFERENCIA,
    "diferenca_abs": abs(beta - BETA_CONFERENCIA),
    "confere_1e-15": abs(beta - BETA_CONFERENCIA) <= 1e-15,
    "instanciacao_das_hipoteses": {
        "T7b_gamma_davies_g01": g01, "T7b_gamma_pos": g01 > 0,
        "T11_lambda": lam, "T11_lambda_em_0_1": 0.0 < lam < 1.0,
        "T8a_reescala": "g01 > 0 permite s = g01*t (g_{01} normalizado a 1)", "T8a_g01_pos": g01 > 0,
    },
    "estatuto": "[REAL — medido aqui; beta calculado em runtime a partir dos bytes; a conferencia so confere; "
                "o kernel nao contem beta]",
    "um_py_executado": False,
}
with open(sys.argv[1], "w", encoding="utf-8") as fo:
    json.dump(out, fo, ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False))
