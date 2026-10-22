# -*- coding: utf-8 -*-
"""beta de runtime: le a linha unica `ALPHA_FINE_CODATA_2018 = ...` nos BYTES do um.py (SEM executa-lo),
calcula beta = alpha*sqrt(e) e theta_M = asin(sqrt beta). Grava BETA_RUNTIME.json ao lado. Nenhum literal de beta."""
import hashlib, json, math, os, re, sys, datetime
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UMPY = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/um.py"
h = hashlib.sha256(); alphas = []; n = 0
with open(UMPY, "rb") as fh:
    for k, ln in enumerate(fh, start=1):
        h.update(ln); n = k
        m = re.match(rb"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9][0-9.eE+-]*)\s*$", ln.rstrip(b"\r\n"))
        if m: alphas.append((k, m.group(1).decode()))
if len(alphas) != 1:
    print("FALHA VISIVEL: atribuicao de alpha nao unica:", alphas); sys.exit(2)
linha, atxt = alphas[0]; alpha = float(atxt); beta = alpha*math.sqrt(math.e)
out = {"quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "um_py": UMPY,
       "um_py_sha256": h.hexdigest(), "um_py_bytes": os.path.getsize(UMPY), "um_py_linhas": n,
       "alpha_linha": linha, "alpha_texto": atxt, "beta_receita": "float(alpha_texto)*math.sqrt(math.e)",
       "beta_repr": repr(beta), "theta_M_repr": repr(math.asin(math.sqrt(beta))),
       "lambda_otico_repr (1-2beta)": repr(1-2*beta), "TGLCoupling_habitado (0<beta<exp(-1/2)*... )": bool(0 < beta < 1),
       "um_py_executado": False, "estatuto": "[REAL - medido aqui por script]"}
json.dump(out, open(os.path.join(AQUI, "BETA_RUNTIME.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
