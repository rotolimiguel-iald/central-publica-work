# -*- coding: utf-8 -*-
"""beta em RUNTIME pelos BYTES do um.py — implementacao PROPRIA do auditor de reproducao (nao copia do construtor).
Le l.95 (SEALED_CODATA_ALPHA, topo) e l.5557 (ALPHA_FINE_CODATA_2018, embutida em _NIVEL2_MCMC_FILES), calcula
beta = alpha*ONE*sqrt(e) em float64 e a 200 digitos (decimal e mpmath) a partir do LITERAL; confere com
BETA_RUNTIME_R2.json congelado. um.py NAO executado. Estatuto: [DERIVED: lido e calculado]. Uso: ... <saida.json>"""
import ast, decimal, hashlib, json, math, re, sys
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
FROZ = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\5_R2\0_ADENDO\saidas\BETA_RUNTIME_R2.json"
b = open(UM, "rb").read()
lines = b.split(b"\n")
l95 = lines[94].decode("utf-8"); l5557 = lines[5556].decode("utf-8"); l5558 = lines[5557].decode("utf-8"); l5559 = lines[5558].decode("utf-8")
m95 = re.match(r"^SEALED_CODATA_ALPHA\s*=\s*([0-9.eE+-]+)", l95)
m5557 = re.match(r"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", l5557)
assert m95 and m5557, "FALHA VISIVEL: linhas nao encontradas"
lit95, lit5557 = m95.group(1), m5557.group(1)
# todas as ocorrencias nao indentadas
occ = [i + 1 for i, L in enumerate(lines) if L.startswith(b"ALPHA_FINE_CODATA_2018")]
occ95 = [i + 1 for i, L in enumerate(lines) if L.startswith(b"SEALED_CODATA_ALPHA")]
ini = next(i + 1 for i, L in enumerate(lines) if L.startswith(b"_NIVEL2_MCMC_FILES = {"))
fim = next(i + 1 for i in range(ini, len(lines)) if lines[i].startswith(b"def materialize_nivel2_mcmc"))
alpha = float(ast.literal_eval(lit5557)); ONE = 1.0
beta = alpha * ONE * math.sqrt(math.e)
decimal.getcontext().prec = 200
D = decimal.Decimal
beta_200 = D(lit5557) * D(1) * D(1).exp().sqrt()
try:
    import mpmath
    with mpmath.mp.workdps(200):
        beta_mp = mpmath.mpf(lit5557) * mpmath.sqrt(mpmath.e)
        beta_mp_s = mpmath.nstr(beta_mp, 200)
        dif_mp_dec = mpmath.nstr(abs(beta_mp - mpmath.mpf(str(beta_200))), 5)
except Exception as e:
    beta_mp_s = "mpmath indisponivel: %r" % e; dif_mp_dec = None
fr = json.load(open(FROZ, encoding="utf-8"))
out = {"um_py": UM, "um_py_sha256": hashlib.sha256(b).hexdigest(), "um_py_bytes": len(b), "um_py_executado": False,
       "l95": l95.strip(), "l5557": l5557.strip(), "l5558": l5558.strip(), "l5559": l5559.strip(),
       "literal_l95": lit95, "literal_l5557": lit5557, "literais_iguais": lit95 == lit5557,
       "ocorrencias_nao_indentadas_ALPHA_FINE_CODATA_2018": occ, "ocorrencias_nao_indentadas_SEALED_CODATA_ALPHA": occ95,
       "envoltorio_NIVEL2_MCMC_FILES": {"inicio": ini, "def_seguinte": fim, "l5557_dentro": ini < 5557 < fim},
       "expressao_BETA_TGL_l5559_confere": l5559.strip() == "BETA_TGL = ALPHA_FINE_CODATA_2018 * ONE * math.sqrt(math.e)",
       "beta_float64": beta, "beta_hex": beta.hex(), "beta_200_decimal": str(beta_200), "beta_200_mpmath": beta_mp_s,
       "mpmath_vs_decimal_abs": dif_mp_dec,
       "conferencia_com_congelado": {"um_py_sha256_igual": hashlib.sha256(b).hexdigest() == fr["um_py_sha256"],
                                     "literal_igual": lit5557 == fr["ALPHA_FINE_CODATA_2018"]["literal"],
                                     "beta_float_igual": beta == fr["beta_runtime_float64"],
                                     "beta_hex_igual": beta.hex() == fr["beta_runtime_float64_hex"],
                                     "beta_200_decimal_igual": str(beta_200) == fr["beta_200_digitos_do_literal"]},
       "estatuto": "[DERIVED: lido nos bytes do um.py (l.5557 embutida == l.95 topo) e calculado em runtime alpha*ONE*sqrt(e); nao e medida]"}
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
