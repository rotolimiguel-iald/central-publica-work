# -*- coding: utf-8 -*-
"""beta de runtime para a face K (somente leitura do um.py, SEM executa-lo).
Le a linha unica `ALPHA_FINE_CODATA_2018 = ...` nos bytes do um.py, calcula beta = alpha*sqrt(e) e confere:
(i) a conferencia da ordem (repr igual ao texto de conferencia do pre-registro, lido do PREREGISTRO.json);
(ii) 0 < beta < 1, isto e, o `TGLCoupling` do kernel e habitado pelo beta de runtime (a pedra prova as formas
para todo c : TGLCoupling; o numero de beta nunca entra no Lean). Grava BETA_RUNTIME.json em 3_KERNEL."""
import hashlib, json, math, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
UMPY = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\um.py"
PRE = os.path.join(os.path.dirname(AQUI), "1_PREREGISTRO", "PREREGISTRO.json")

h = hashlib.sha256()
alphas = []
with open(UMPY, "rb") as fh:
    for k, ln in enumerate(fh, start=1):
        h.update(ln)
        m = re.match(rb"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9][0-9.eE+-]*)\s*$", ln.rstrip(b"\r\n"))
        if m:
            alphas.append((k, m.group(1).decode()))
if len(alphas) != 1:
    print("FALHA VISIVEL: atribuicao de alpha nao unica:", alphas)
    sys.exit(2)
linha, alpha_txt = alphas[0]
alpha = float(alpha_txt)
beta = alpha * math.sqrt(math.e)
theta_M = math.asin(math.sqrt(beta))
pre = json.loads(open(PRE, "rb").read().decode("utf-8"))
conf = pre["beta_runtime"]["beta_float64"]          # texto de conferencia do pre-registro (nao e usado como valor)
out = {
    "um_py_sha256": h.hexdigest(),
    "alpha_linha": linha,
    "alpha_texto": alpha_txt,
    "beta_receita": "float(alpha_texto) * math.sqrt(math.e)",
    "beta_repr": repr(beta),
    "beta_confere_com_a_conferencia_do_preregistro": repr(beta) == conf,
    "theta_M_repr": repr(theta_M),
    "theta_M_confere": repr(theta_M) == pre["beta_runtime"]["theta_M"],
    "TGLCoupling_habitado_pelo_beta_de_runtime": (0.0 < beta < 1.0),
    "nota": "[REAL - medido aqui] o kernel prova as formas para todo c : TGLCoupling (0 < beta < 1); o beta de runtime "
            "satisfaz 0 < beta < 1, logo as instancias em theta_M valem para ele. Identidades de theta_M (B2.b, B3.b, "
            "B5.b, B6, B9.b) sao validade algebrica, sem poder discriminante.",
}
dst = os.path.join(AQUI, "BETA_RUNTIME.json")
with open(dst + ".tmp", "wb") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8") + b"\n")
os.replace(dst + ".tmp", dst)
print(json.dumps(out, ensure_ascii=False, indent=1))
sys.exit(0 if (out["beta_confere_com_a_conferencia_do_preregistro"] and out["TGLCoupling_habitado_pelo_beta_de_runtime"]) else 2)
