# -*- coding: utf-8 -*-
"""cmp_spec_funcao.py -- auditoria c1 (23/10/2026): compara a spec V2-c1 com a R5.2-E1 secao a secao (JSON canonico) e a funcao de veredito
V2-c1 com a fonte da R5.2 (as 3 trocas declaradas; AST e constantes numericas). So le. uso: python -P -E -X utf8 cmp_spec_funcao.py <R52.json> <V2C1.json> <veredito.py> <saida.json>"""
import ast, hashlib, json, sys, difflib
R52, V2, FN, OUT = sys.argv[1:5]
ra, va = json.load(open(R52, encoding="utf-8")), json.load(open(V2, encoding="utf-8"))
A, B = ra["spec"], va["spec"]
can = lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
R = {"r52_spec_sha256_campo": ra.get("spec_sha256"), "r52_spec_canon": hashlib.sha256(can(A).encode()).hexdigest(),
     "v2_spec_sha256_campo": va.get("spec_sha256"), "v2_spec_canon": hashlib.sha256(can(B).encode()).hexdigest()}
R["secoes_novas"] = sorted(set(B) - set(A)); R["secoes_removidas"] = sorted(set(A) - set(B))
R["secoes_alteradas"] = sorted(k for k in set(A) & set(B) if can(A[k]) != can(B[k]))
R["secoes_iguais"] = sorted(k for k in set(A) & set(B) if can(A[k]) == can(B[k]))
# funcao
fa = A["funcao_de_veredito"]["fonte"]; fb_spec = B["funcao_de_veredito"]["fonte"]; fb_file = open(FN, "rb").read().decode("utf-8")
R["funcao"] = {"r52_fonte_sha256": hashlib.sha256(fa.encode()).hexdigest(), "v2_spec_fonte_sha256": hashlib.sha256(fb_spec.encode()).hexdigest(),
               "v2_arquivo_sha256": hashlib.sha256(fb_file.encode()).hexdigest(), "spec_fonte_igual_arquivo": fb_spec == fb_file,
               "spec_declara_sha256": B["funcao_de_veredito"].get("sha256")}
ta, tb = ast.parse(fa), ast.parse(fb_file)
def norm(t):
    t = ast.parse(ast.unparse(t))
    for n in ast.walk(t):
        if isinstance(n, ast.FunctionDef):
            n.name = "F"
            if n.body and isinstance(n.body[0], ast.Expr) and isinstance(getattr(n.body[0], "value", None), ast.Constant) and isinstance(n.body[0].value.value, str):
                n.body[0].value.value = "DOC"
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value.startswith(("TGL_FASE9_RAZAO_DE_HUBBLE_V2_R5_2_DRAFT__", "TGL_FASE9_V2_A_UNICA_PALAVRA_BETA_TGL__")):
            n.value = "BASE"
    return ast.dump(t)
R["funcao"]["ast_igual_salvo_nome_docstring_base"] = norm(ta) == norm(tb)
nums = lambda t: sorted((type(n.value).__name__, repr(n.value)) for n in ast.walk(t) if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool))
strs = lambda t: sorted(n.value for n in ast.walk(t) if isinstance(n, ast.Constant) and isinstance(n.value, str))
R["funcao"]["constantes_numericas_iguais"] = nums(ta) == nums(tb); R["funcao"]["constantes_numericas"] = sorted(set(v for _, v in nums(tb)))
sa_, sb_ = strs(ta), strs(tb)
R["funcao"]["strings_so_r52"] = [s[:120] for s in sa_ if s not in sb_]; R["funcao"]["strings_so_v2"] = [s[:160] for s in sb_ if s not in sa_]
R["funcao"]["diff_linhas"] = [l[:200] for l in difflib.unified_diff(fa.splitlines(), fb_file.splitlines(), lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
# funcao_de_veredito: chaves alteradas
fva, fvb = A["funcao_de_veredito"], B["funcao_de_veredito"]
R["funcao_de_veredito_chaves_alteradas"] = sorted(k for k in set(fva) | set(fvb) if can(fva.get(k)) != can(fvb.get(k)))
R["funcao_de_veredito_novas"] = {k: str(fvb.get(k))[:600] for k in R["funcao_de_veredito_chaves_alteradas"] if k not in ("fonte", "testes_de_ramo", "branch_tests")}
json.dump(R, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1)[:12000])
