"""Le, SEM EXECUTAR o um.py, as atribuicoes de alpha nos bytes (topo: SEALED_CODATA_ALPHA; embutida:
ALPHA_FINE_CODATA_2018 dentro de _NIVEL2_MCMC_FILES), confere o escopo pela AST, calcula beta = alpha*sqrt(e)
em runtime e compara com a conferencia lida do PREREGISTRO.json (a conferencia so confere).
Uso: python -I -X utf8 beta_dos_bytes.py <saida.json>"""
import ast, hashlib, json, math, re, sys

UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
PRE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO\PREREGISTRO.json"
b = open(UM, "rb").read()
txt = b.decode("utf-8")
lines = txt.split("\n")
out = {"um_py_sha256": hashlib.sha256(b).hexdigest(), "um_py_bytes": len(b)}
hits = {}
for name in ("SEALED_CODATA_ALPHA", "ALPHA_FINE_CODATA_2018"):
    pat = re.compile(r"^" + name + r"\s*=\s*([0-9.eE+\-]+)")
    hits[name] = [(i + 1, pat.match(ln).group(1)) for i, ln in enumerate(lines) if pat.match(ln)]
out["atribuicoes_nao_indentadas"] = hits
tree = ast.parse(txt)
top = {}
for node in tree.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id in ("SEALED_CODATA_ALPHA", "ALPHA_FINE_CODATA_2018", "_NIVEL2_MCMC_FILES"):
                top[t.id] = {"linha_ini": node.lineno, "linha_fim": node.end_lineno,
                             "valor": (repr(node.value.value) if isinstance(node.value, ast.Constant) else type(node.value).__name__)}
out["no_topo_da_AST"] = top
a_top = float(hits["SEALED_CODATA_ALPHA"][0][1])
a_emb = float(hits["ALPHA_FINE_CODATA_2018"][0][1])
sqrt_e = math.sqrt(math.e)
beta_top = a_top * 1.0 * sqrt_e
beta_emb = a_emb * 1.0 * sqrt_e
pre = json.load(open(PRE, encoding="utf-8"))
conf = pre["numeros_de_conferencia"]["beta"]
out.update({"alpha_topo": a_top, "alpha_embutido": a_emb, "iguais": a_top == a_emb,
            "beta_runtime_topo": beta_top, "beta_runtime_embutido": beta_emb,
            "beta_conferencia_lida_do_preregistro": conf,
            "dif_topo": abs(beta_top - conf), "dif_embutido": abs(beta_emb - conf),
            "lambda_1_menos_2beta": 1 - 2 * beta_top,
            "estatuto": "[REAL — lido nos bytes e calculado em runtime; NAO e medida de beta na natureza]"})
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps(out, ensure_ascii=False, indent=1))
