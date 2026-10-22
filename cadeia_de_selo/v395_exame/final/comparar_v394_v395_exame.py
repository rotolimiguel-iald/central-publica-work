# -*- coding: utf-8 -*-
"""comparar_v394_v395_exame.py -- exame final v395 (c1, modelo forte, 21/10/2026): comparação ESTRUTURAL (AST/literal_eval) dos nós que mudam entre a v394
instalada (A) e o candidato v395 (B). Só lê; escreve só em v395_exame\\final. uso: python -I -B -X utf8 comparar_v394_v395_exame.py <A.py> <B.py> <saida.json>"""
import ast, json, re, sys, hashlib, difflib, os
A_, B_, S_ = sys.argv[1:4]
NOSK = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "tgl_kernel")
sa, sb = open(A_, "rb").read().decode("utf-8"), open(B_, "rb").read().decode("utf-8")
TA, TB = ast.parse(sa), ast.parse(sb)
def top(T):
    d = {}
    for n in T.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): d[n.targets[0].id] = n
        elif isinstance(n, (ast.FunctionDef, ast.ClassDef)): d[n.name] = n
    return d
dA, dB = top(TA), top(TB)
lit = lambda d, k: ast.literal_eval(d[k].value)
AUX = re.compile(r"^(_proof_\d+(_\d+)*|_simp_\d+(_\d+)*|match_\d+|_sunfold|eq_\d+|eq_def|congr_simp)$")
R = {}
fa, fb = lit(dA, "_LEAN_THEOREM_FLAGS"), lit(dB, "_LEAN_THEOREM_FLAGS")
add = {k: v for k, v in fb.items() if k not in fa}
R["bandeiras"] = {"n_A": len(fa), "n_B": len(fb), "removidas": sorted(set(fa) - set(fb)), "mudadas": [k for k in fa if k in fb and fa[k] != fb[k]],
                  "acrescentadas": len(add), "prefixos": sorted(set(re.sub(r"_\d+$", "", k) for k in add)), "acrescentadas_auxiliares": sorted(v for v in add.values() if AUX.match(v.split(".")[-1])),
                  "acrescentadas_fora_de_Psibit": sorted(v for v in add.values() if not v.startswith("TGLExt.Psibit."))}
def escada(T):
    for n in T.body:
        if isinstance(n, ast.FunctionDef) and n.name == "prove_external_ladder":
            for m in ast.walk(n):
                if isinstance(m, (ast.List, ast.Tuple, ast.Set)) and len(m.elts) > 1000 and all(isinstance(e, ast.Constant) and isinstance(e.value, str) for e in m.elts):
                    return [e.value for e in m.elts]
la, lb = escada(TA), escada(TB)
R["escada"] = {"n_A": len(la), "n_B": len(lb), "B_igual_A_mais_novas": set(lb) == set(la) | set(add), "A_contida_em_B": set(la) <= set(lb)}
for c in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT"):
    a, b = lit(dA, c), lit(dB, c)
    R[c] = {k: {"A": a.get(k) if not isinstance(a.get(k), (list, dict)) else "len %d" % len(a.get(k)), "B": b.get(k) if not isinstance(b.get(k), (list, dict)) else "len %d" % len(b.get(k))} for k in set(a) | set(b) if a.get(k) != b.get(k)}
def specs_diff(nome_lista):
    sA, sB = {s["nome"]: s for s in lit(dA, nome_lista)}, {s["nome"]: s for s in lit(dB, nome_lista)}
    out = {}
    for n in sorted(set(sA) | set(sB)):
        a, b = sA.get(n), sB.get(n)
        if a == b: continue
        if a is None or b is None: out[n] = "so_A" if b is None else "so_B"; continue
        ca, cb = {c["id"]: c for c in a.get("checks", [])}, {c["id"]: c for c in b.get("checks", [])}
        sv = lambda v: ("dict(%d)" % len(v)) if isinstance(v, dict) else v
        out[n] = {"checks_mudados": {i: {"A": [ca[i].get("op"), sv(ca[i].get("valor"))], "B": [cb[i].get("op"), sv(cb[i].get("valor"))]} for i in ca if i in cb and (ca[i].get("op"), ca[i].get("valor")) != (cb[i].get("op"), cb[i].get("valor"))},
                  "checks_novos": sorted(set(cb) - set(ca)), "checks_removidos": sorted(set(ca) - set(cb)), "outras_chaves": sorted(k for k in set(a) | set(b) if k != "checks" and a.get(k) != b.get(k)),
                  "erratas_B_novas": [e for e in (b.get("erratas") or []) if e not in (a.get("erratas") or [])]}
    return out
R["specs_v394_mudados"] = specs_diff("_V394_SPECS")
for nm in ("_V392_SPECS", "_V393_SPECS"):
    R["specs_%s_mudados" % nm] = specs_diff(nm)
# v395: o h8 do kh_n1_cobertura_v395 == embutidos de B + residuais do Nós?
sp5 = {s["nome"]: s for s in lit(dB, "_V395_SPECS")}
kh5 = sp5.get("kh_n1_cobertura_v395") or {}
R["kh_n1_cobertura_v395_checks"] = [(c.get("id"), c.get("onde"), c.get("caminho"), c.get("op"), ("dict(%d)" % len(c["valor"])) if isinstance(c.get("valor"), dict) else c.get("valor")) for c in kh5.get("checks", [])]
pin = next((c["valor"] for c in kh5.get("checks", []) if isinstance(c.get("valor"), dict) and c.get("caminho") == ["formal_files_sha256"]), None)
embB = lit(dB, "_EMBEDDED_KERNEL_FILES")
alvo = {rel: hashlib.sha256(c.encode("utf-8")).hexdigest() for rel, c in embB.items()}
for f in ("_check_damming.lean",):
    p = os.path.join(NOSK, f)
    if os.path.exists(p): alvo[f] = hashlib.sha256(open(p, "rb").read()).hexdigest()
R["h8_v395"] = {"n_pino": len(pin) if pin else None, "pino_igual_embutidos_mais_residual": pin == alvo if pin else None, "difere": sorted(k for k in set(pin or {}) | set(alvo) if (pin or {}).get(k) != alvo.get(k))[:10]}
eA, eB = lit(dA, "_EMBEDDED_KERNEL_FILES"), embB
R["_EMBEDDED_KERNEL_FILES"] = {"novos": sorted(set(eB) - set(eA)), "removidos": sorted(set(eA) - set(eB)), "mudados": sorted(k for k in eA if k in eB and eA[k] != eB[k])}
for k in R["_EMBEDDED_KERNEL_FILES"]["mudados"]:
    R["_EMBEDDED_KERNEL_FILES"]["diff_" + k] = [l for l in difflib.unified_diff(eA[k].splitlines(), eB[k].splitlines(), lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))][:10]
R["pedra_sha16_embutida"] = hashlib.sha256(eB.get("TGLExt/Psibit.lean", "").encode("utf-8")).hexdigest()[:16]
R["_ESQUELETO_STONES_so_B"] = [list(x) for x in lit(dB, "_ESQUELETO_STONES") if tuple(x) not in set(map(tuple, lit(dA, "_ESQUELETO_STONES")))]
for f in ("build_pt", "build_en", "emit_canonical_md", "main", "prove_external_ladder"):
    a, b = ast.unparse(dA[f]).splitlines(), ast.unparse(dB[f]).splitlines()
    dd = [l for l in difflib.unified_diff(a, b, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    R["diff_" + f] = {"removidas": [l[:300] for l in dd if l.startswith("-")][:20], "n_acrescentadas": sum(1 for l in dd if l.startswith("+")),
                      "acrescentadas_amostra": [l[:300] for l in dd if l.startswith("+")][:6] if f != "prove_external_ladder" else []}
# colisões de chave das fontes/falas
def keys(name, T):
    for n in T.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and getattr(n.targets[0], "id", None) == name:
            return set(ast.literal_eval(n.value).keys())
    return set()
F = {nm: keys(nm, TB) for nm in ("_V392_FONTES", "_V393_FONTES", "_V394_FONTES", "_V395_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", "_V394_VERBATINS2", "_V395_VERBATINS2")}
R["colisoes_v395"] = {"fontes": sorted(F["_V395_FONTES"] & (F["_V392_FONTES"] | F["_V393_FONTES"] | F["_V394_FONTES"])), "falas": sorted(F["_V395_VERBATINS2"] & (F["_V392_VERBATINS2"] | F["_V393_VERBATINS2"] | F["_V394_VERBATINS2"]))}
json.dump(R, open(S_, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, indent=1, default=str)[:24000])
