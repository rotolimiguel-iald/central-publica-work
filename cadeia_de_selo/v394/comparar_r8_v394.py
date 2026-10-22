# -*- coding: utf-8 -*-
"""comparar_r8_v394.py -- compara o CANDIDATO v394 (derivado por script da v393) com a candidata r8 do Codex (coverage_candidate_r8\\um_v394_prechecked.py, 01ca38fd1c327eb8), no=a=no (AST), e escreve
COMPARACAO_R8_v394.json + COMPARACAO_R8_v394.txt. Cada diferenca e' listada; EXPLICACOES (escritas por mim, depois de ler o diff) ficam em explicacoes_r8_v394.json e entram na tabela.
uso: python -I -B -X utf8 comparar_r8_v394.py"""
import ast, difflib, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta19_v394 as DL  # noqa: E402
C = "C:" + os.sep
R8P = os.path.join(C, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "F1.FECHO_20261015", "coverage_candidate_r8", "um_v394_prechecked.py")
MP = os.path.join(HERE, DL.CANDIDATO)
ta = open(MP, "rb").read().decode("utf-8"); tb = open(R8P, "rb").read().decode("utf-8")
A = ast.parse(ta); B = ast.parse(tb)
dump = lambda n: ast.dump(n)
h = lambda n: hashlib.sha256(dump(n).encode()).hexdigest()[:12]


def nm(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        return n.name
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
        return n.targets[0].id
    return None


def idx(tree):
    d, anon = {}, []
    for n in tree.body:
        k = nm(n)
        if k and k not in d:
            d[k] = n
        else:
            anon.append(n)
    return d, anon


da, anon_a = idx(A); db, anon_b = idx(B)
res = {"iguais": 0, "difere": {}, "so_meu": [], "so_r8": [], "anonimos": {}}
for k in da:
    if k in db:
        if h(da[k]) == h(db[k]):
            res["iguais"] += 1
        else:
            na, nb = da[k], db[k]; det = {"tipo": type(na).__name__}
            if isinstance(na, ast.Assign):
                try:
                    va, vb = ast.literal_eval(na.value), ast.literal_eval(nb.value)
                    if isinstance(va, dict) and isinstance(vb, dict):
                        det["chaves_so_meu"] = [str(x)[:90] for x in va if x not in vb][:12]; det["n_chaves_so_meu"] = sum(1 for x in va if x not in vb)
                        det["chaves_so_r8"] = [str(x)[:90] for x in vb if x not in va][:12]; det["n_chaves_so_r8"] = sum(1 for x in vb if x not in va)
                        det["valores_diferentes"] = [str(x)[:90] for x in va if x in vb and va[x] != vb[x]][:12]; det["n_valores_diferentes"] = sum(1 for x in va if x in vb and va[x] != vb[x])
                    elif isinstance(va, list) and isinstance(vb, list):
                        det["len_meu"], det["len_r8"] = len(va), len(vb)
                        det["so_meu"] = [str(x)[:100] for x in va if x not in vb][:6]; det["so_r8"] = [str(x)[:100] for x in vb if x not in va][:6]
                    else:
                        det["resumo"] = "valores diferentes (%s / %s)" % (type(va).__name__, type(vb).__name__)
                except Exception as e:  # noqa
                    det["resumo"] = "nao literal: " + repr(e)[:80]
            else:
                ua, ub = ast.unparse(na).splitlines(), ast.unparse(nb).splitlines()
                d = [l for l in difflib.unified_diff(ua, ub, "meu", "r8", lineterm="", n=0) if not l.startswith(("---", "+++", "@@"))]
                det["linhas_diff"] = len(d); det["amostra"] = [l[:200] for l in d[:24]]
            res["difere"][k] = det
    else:
        res["so_meu"].append(k)
res["so_r8"] = [k for k in db if k not in da]
ca = {}; cb = {}
for n in anon_a:
    ca[h(n)] = ca.get(h(n), []) + [ast.unparse(n)[:120]]
for n in anon_b:
    cb[h(n)] = cb.get(h(n), []) + [ast.unparse(n)[:120]]
res["anonimos"] = {"so_meu": [v[0] for k, v in ca.items() if k not in cb][:20], "so_r8": [v[0] for k, v in cb.items() if k not in ca][:20], "n_a": len(anon_a), "n_b": len(anon_b)}
expl = json.load(open(os.path.join(HERE, "explicacoes_r8_v394.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "explicacoes_r8_v394.json")) else {}
res["sem_explicacao"] = sorted(k for k in list(res["difere"]) + res["so_meu"] + res["so_r8"] if k not in expl)
res["explicacoes"] = {k: expl[k] for k in list(res["difere"]) + res["so_meu"] + res["so_r8"] if k in expl}
res["meu"] = {"bytes": len(ta.encode("utf-8")), "sha16": hashlib.sha256(ta.encode("utf-8")).hexdigest()[:16]}; res["r8"] = {"bytes": len(tb.encode("utf-8")), "sha16": hashlib.sha256(tb.encode("utf-8")).hexdigest()[:16]}
json.dump(res, open(os.path.join(HERE, "COMPARACAO_R8_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L = ["COMPARACAO v394 (derivado) x r8 do Codex", "meu %s %d B | r8 %s %d B" % (res["meu"]["sha16"], res["meu"]["bytes"], res["r8"]["sha16"], res["r8"]["bytes"]), "nos nomeados IGUAIS (AST): %d | DIFEREM: %d | so no meu: %d | so no r8: %d" % (res["iguais"], len(res["difere"]), len(res["so_meu"]), len(res["so_r8"])),
     "anonimos (Expr/Import/If...): so no meu %d, so no r8 %d" % (len(res["anonimos"]["so_meu"]), len(res["anonimos"]["so_r8"])), ""]
for k, d in res["difere"].items():
    L.append("DIFERE %s -- %s" % (k, json.dumps({x: y for x, y in d.items() if x != "amostra"}, ensure_ascii=False)[:600])); L.append("    explicacao: " + expl.get(k, "SEM EXPLICACAO"))
    for l in d.get("amostra", [])[:10]:
        L.append("      " + l)
for k in res["so_meu"]:
    L.append("SO NO MEU %s -- %s" % (k, expl.get(k, "SEM EXPLICACAO")))
for k in res["so_r8"]:
    L.append("SO NO R8 %s -- %s" % (k, expl.get(k, "SEM EXPLICACAO")))
L += ["anonimos so no meu: %s" % res["anonimos"]["so_meu"], "anonimos so no r8: %s" % res["anonimos"]["so_r8"], "SEM EXPLICACAO: %s" % res["sem_explicacao"]]
open(os.path.join(HERE, "COMPARACAO_R8_v394.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("\n".join(L[:4])); print("DIFEREM:", sorted(res["difere"])); print("SO MEU:", res["so_meu"]); print("SO R8:", res["so_r8"]); print("sem explicacao:", res["sem_explicacao"])
