# -*- coding: utf-8 -*-
"""comparar_runtime_v399.py -- exame final v399 (c1, 24/10/2026): o runtime do selo ACOM e da declaracao, como esta NO CANDIDATO, contra o codigo que a revisao independente
do estudo APROVOU (patch_proposto\\secao_colavel_v399.py b589f78e e trechos_v399_para_o_um_py.py 623e4780): por AST, com docstrings e comentarios fora, funcao a funcao e classe
a classe; as constantes de TEXTO que diferem sao listadas (as 9 edicoes declaradas em RUNTIME_MONTAGEM_v399.json). So le; grava so' o JSON nesta pasta."""
import ast, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
S = r"C:\IALD\Central de Patentes\work\v399_selo_e_testemunho\patch_proposto"
CAND = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v399\um_v399_candidato.py"
sec = open(os.path.join(S, "secao_colavel_v399.py"), "rb").read().decode("utf-8"); tre = open(os.path.join(S, "trechos_v399_para_o_um_py.py"), "rb").read().decode("utf-8")
cand = open(CAND, "rb").read().decode("utf-8")
def tops(src):
    d = {}
    for n in ast.parse(src).body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)): d[n.name] = n
        elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): d[n.targets[0].id] = n
    return d
A = tops(sec); A.update(tops(tre)); B = tops(cand)
def strip_doc(node):
    node = ast.parse(ast.unparse(node)).body[0]
    for n in ast.walk(node):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.Module)) and n.body and isinstance(n.body[0], ast.Expr) and isinstance(getattr(n.body[0], "value", None), ast.Constant) and isinstance(n.body[0].value.value, str):
            n.body = n.body[1:] or [ast.Pass()]
    return node
def skel(node):
    return re.sub(r"Constant\(value='(?:[^'\\]|\\.)*'\)", "STR", re.sub(r'Constant\(value="(?:[^"\\]|\\.)*"\)', "STR", ast.dump(strip_doc(node))))
def strs(node):
    return [x.value for x in ast.walk(node) if isinstance(x, ast.Constant) and isinstance(x.value, str)]
R = {"secao_sha16": hashlib.sha256(sec.encode("utf-8")).hexdigest()[:16], "trechos_sha16": hashlib.sha256(tre.encode("utf-8")).hexdigest()[:16], "candidato_sha16": hashlib.sha256(cand.encode("utf-8")).hexdigest()[:16], "nos": {}}
iguais = codigo_igual_texto_difere = difere_codigo = ausentes = []
iguais, cit, dc, aus = [], [], [], []
for k, na in A.items():
    nb = B.get(k)
    if nb is None:
        aus.append(k); continue
    if ast.dump(na) == ast.dump(nb):
        iguais.append(k); continue
    if skel(na) == skel(nb):
        sa, sb = strs(na), strs(nb)
        cit.append({"no": k, "so_A": [x[:200] for x in sa if x not in sb][:6], "so_B": [x[:200] for x in sb if x not in sa][:6]})
    else:
        dc.append({"no": k, "A": ast.unparse(strip_doc(na))[:600], "B": ast.unparse(strip_doc(nb))[:600]})
R["iguais_por_AST"] = iguais; R["codigo_igual_so_texto_difere"] = cit; R["CODIGO_DIFERE"] = dc; R["ausentes_no_candidato"] = aus
R["n"] = {"aprovados": len(A), "iguais": len(iguais), "so_texto": len(cit), "codigo_difere": len(dc), "ausentes": len(aus)}
# as 9 edicoes declaradas
try:
    M = json.load(open(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v399\RUNTIME_MONTAGEM_v399.json", encoding="utf-8"))
    R["edicoes_declaradas"] = [{k: (str(v)[:160]) for k, v in e.items()} if isinstance(e, dict) else str(e)[:200] for e in (M.get("edicoes_declaradas") or [])]
    R["conferencias_da_montagem"] = M.get("conferencias")
except Exception as e:
    R["edicoes_declaradas"] = repr(e)[:200]
json.dump(R, open(os.path.join(H, "COMPARACAO_RUNTIME_v399.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k not in ("iguais_por_AST",)}, ensure_ascii=False, indent=1)[:9000])
print("iguais:", R["iguais_por_AST"])
