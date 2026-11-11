# -*- coding: utf-8 -*-
"""Revisor v410 R2: o DELTA do candidato: pre_r1fix (o que revisei na R1) x candidato atual, por no de nivel superior (AST). Lista nos mudados/novos/removidos; para funcoes, o diff de linhas (-/+ resumido);
para literais, so' o tamanho. Confere que veredito_h0dn (texto-fonte) e' IDENTICO."""
import ast, difflib, hashlib, json, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
a = open(R + "um_v410_candidato.pre_r2fix.py", "rb").read().decode("utf-8"); b = open(R + "um_v410_candidato.py", "rb").read().decode("utf-8")
al = a.split("\n"); bl = b.split("\n")
ta = ast.parse(a); tb = ast.parse(b)


def top(tr, L):
    d = {}
    for n in tr.body:
        nm = None
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)): nm = n.name
        elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): nm = n.targets[0].id
        if nm: d[nm] = (hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12], "\n".join(L[n.lineno - 1:n.end_lineno]), isinstance(n, ast.FunctionDef))
    return d


A = top(ta, al); B = top(tb, bl)
mud = sorted(k for k in A if k in B and A[k][0] != B[k][0]); nov = sorted(k for k in B if k not in A); rem = sorted(k for k in A if k not in B)
print("mudados", len(mud), "novos", nov, "removidos", rem)
res = {"mudados": mud, "novos": nov, "removidos": rem, "funcoes": {}}
for k in mud:
    fa, fb = A[k][1], B[k][1]
    if B[k][2]:
        d = [l for l in difflib.unified_diff(fa.split("\n"), fb.split("\n"), "pre", "novo", lineterm="", n=0) if (l.startswith("+") or l.startswith("-")) and not l.startswith("+++") and not l.startswith("---")]
        print("== FUNCAO", k, "linhas -/+:", len(d))
        for l in d[:40]: print("    ", l[:300])
        res["funcoes"][k] = len(d)
    else:
        print("== LITERAL", k, len(fa), "->", len(fb))
src_a = A["veredito_h0dn"][1]; src_b = B["veredito_h0dn"][1]
print("veredito_h0dn: texto-fonte identico:", src_a == src_b, "| sha256 do texto (como inspect.getsource, sem indentacao extra):", hashlib.sha256(src_b.encode("utf-8")).hexdigest()[:16])
res["veredito_h0dn_identico"] = src_a == src_b
for nm in ("_v410_h0dn_decode", "_v410_h0dn_cabeca", "_v410_h0dn_vigia_arquivos", "_v410_guarda_frases", "_v410_hms13_mechanics", "_v410_hms13_numeros", "iald2_v410", "v410_iald2_mechanics", "_v410_formal", "h0dn_bg1_v410", "_v410_h0dn_mechanics", "a_escala_v410", "_v410_aescala_mechanics", "_v410_aescala_bell", "_v410_aescala_ciclo", "_v410_rotacao", "_v410_sem_falas_do_operador", "_v410_rodar_specs", "h0dn_fontes_hms13_v410"):
    print("  %-28s %s" % (nm, "novo" if nm in nov else ("MUDOU" if nm in mud else ("igual" if nm in A else "ausente"))))
json.dump(res, open(R + "revisao_terceiro/r2_delta_nos_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
