# -*- coding: utf-8 -*-
# Exame final v394: comparacao INDEPENDENTE (AST) do candidato com a r8 do Codex (so' leitura do tunel). Escreve so' em v394_exame.
import ast, hashlib, json, os, difflib, sys
H = os.path.dirname(os.path.abspath(__file__))
R8 = r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\coverage_candidate_r8\um_v394_prechecked.py"
CA = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v394\um_v394_candidato.py"
br8, bca = open(R8, "rb").read(), open(CA, "rb").read()
A, B = ast.parse(br8.decode("utf-8")), ast.parse(bca.decode("utf-8"))
def nm(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)): return n.name
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): return n.targets[0].id
    return None
da = {nm(n): n for n in A.body if nm(n)}; db = {nm(n): n for n in B.body if nm(n)}
h = lambda n: hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]
dif = sorted(k for k in da if k in db and h(da[k]) != h(db[k])); so_r8 = sorted(k for k in da if k not in db); so_ca = sorted(k for k in db if k not in da)
R = {"r8_sha16": hashlib.sha256(br8).hexdigest()[:16], "cand_sha16": hashlib.sha256(bca).hexdigest()[:16], "iguais": sum(1 for k in da if k in db and h(da[k]) == h(db[k])),
     "diferem": dif, "so_r8": so_r8, "so_candidato": so_ca, "detalhe": {}}
for k in dif:
    a_, b_ = da[k], db[k]
    if isinstance(a_, ast.Assign):
        try:
            va, vb = ast.literal_eval(a_.value), ast.literal_eval(b_.value)
            if isinstance(va, dict) and isinstance(vb, dict):
                R["detalhe"][k] = {"chaves_so_r8": sorted(set(va) - set(vb))[:10], "chaves_so_cand": sorted(set(vb) - set(va))[:10],
                                   "valores_diferentes": sorted(x for x in set(va) & set(vb) if va[x] != vb[x])[:20]}
            elif isinstance(va, list) and isinstance(vb, list):
                ja = [json.dumps(x, sort_keys=True, ensure_ascii=False) for x in va]; jb = [json.dumps(x, sort_keys=True, ensure_ascii=False) for x in vb]
                so_a = [x for x in ja if x not in jb]; so_b = [x for x in jb if x not in ja]
                R["detalhe"][k] = {"len_r8": len(va), "len_cand": len(vb), "so_r8": [x[:150] for x in so_a], "so_cand": [x[:150] for x in so_b]}
                # para specs: que checks mudaram
                if all(isinstance(x, dict) and "nome" in x for x in va + vb):
                    por = {}
                    for x in va:
                        y = next((z for z in vb if z["nome"] == x["nome"]), None)
                        if y is None: por[x["nome"]] = "so_r8"; continue
                        if x != y:
                            ca_ = {c["id"]: c for c in x.get("checks", [])}; cb_ = {c["id"]: c for c in y.get("checks", [])}
                            por[x["nome"]] = {"checks_mudados": {i: {"r8": {kk: ca_[i].get(kk) for kk in ("op", "valor")}, "cand": {kk: cb_[i].get(kk) for kk in ("op", "valor")}}
                                                                 for i in ca_ if i in cb_ and (ca_[i].get("op"), ca_[i].get("valor")) != (cb_[i].get("op"), cb_[i].get("valor"))},
                                              "outras_chaves_mudadas": sorted(kk for kk in set(x) | set(y) if kk != "checks" and x.get(kk) != y.get(kk))}
                    for y in vb:
                        if not any(x["nome"] == y["nome"] for x in va): por[y["nome"]] = "so_cand"
                    R["detalhe"][k]["specs"] = por
        except Exception as e:
            R["detalhe"][k] = {"nao_literal": repr(e)[:120]}
    else:
        sa, sb = ast.unparse(a_).splitlines(), ast.unparse(b_).splitlines()
        R["detalhe"][k] = {"diff": [l for l in difflib.unified_diff(sa, sb, "r8", "cand", n=0, lineterm="") if not l.startswith(("---", "+++"))][:60]}
json.dump(R, open(os.path.join(H, "COMPARACAO_R8_EXAME.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: R[k] for k in ("r8_sha16", "cand_sha16", "iguais", "diferem", "so_r8", "so_candidato")}, ensure_ascii=False))
for k, v in R["detalhe"].items():
    print("==", k, json.dumps(v, ensure_ascii=False)[:1500])
