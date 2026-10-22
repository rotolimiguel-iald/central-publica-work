# -*- coding: utf-8 -*-
# Auditor de estatuto (r2): beta em runtime a partir dos BYTES do um.py (sem executa-lo); conferencias de leitura.
import re, math, json, os, hashlib
NOS = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xf3) + "s"
b = open(os.path.join(NOS, "um.py"), "rb").read()
t = b.decode("utf-8")
ms = list(re.finditer(r"^ALPHA_FINE_CODATA_2018 = ([0-9.eE+-]+)[ \t]*\r?$", t, re.M))
assert len(ms) == 1, "FALHA VISIVEL: atribuicao de alpha nao e unica"
linha = t.count("\n", 0, ms[0].start()) + 1
alpha = float(ms[0].group(1))
beta = alpha * math.sqrt(math.e)
thM = math.asin(math.sqrt(beta))
s, c = math.sin(thM), math.cos(thM)
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))
fd = core.get("fractal_dephasing") or core.get("core", {}).get("fractal_dephasing")
v4 = open(r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt", "rb").read().decode("utf-8")
num_op = re.search("approx (0[.][0-9]+)", v4).group(1)
out = {
 "um_py_sha16": hashlib.sha256(b).hexdigest()[:16], "alpha_linha": linha, "alpha_texto": ms[0].group(1),
 "beta_repr": repr(beta), "beta_confere_texto_de_conferencia": repr(beta) == "0.012031300400803142",
 "theta_M": thM,
 "endpoint_diag": [c * c, s * s], "endpoint_p1_menos_beta": s * s - beta,
 "pureza_endpoint": c**4 + s**4, "pureza_forma_1_menos_2b1mb": 1 - 2 * beta * (1 - beta),
 "anticomm_frob_thetaM": math.sqrt(2 * s * s * (1 + s * s)), "anticomm_traco_thetaM": 2 * s * s,
 "numero_do_operador_V4": num_op, "abs_beta_menos_operador": abs(beta - float(num_op)),
 "round_beta_6": round(beta, 6),
 "core_fractal_dephasing": fd,
 "leak_core_igual_beta_bit_a_bit": (fd or {}).get("leak_sin2_thetaM") == beta,
}
dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "BETA_R2_AUDITOR.json")
open(dest, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
print(json.dumps(out, ensure_ascii=False, indent=1))
