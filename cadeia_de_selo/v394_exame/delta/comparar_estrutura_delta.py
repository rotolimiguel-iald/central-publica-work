# -*- coding: utf-8 -*-
"""comparar_estrutura_delta.py -- exame do delta v394: compara ESTRUTURALMENTE (AST/literal_eval) os nos de topo que mudaram entre o
candidato examinado (A) e o candidato final do delta (B). So' le; escreve so' em v394_exame\\delta.
uso: python -I -B -X utf8 comparar_estrutura_delta.py <A.py> <B.py> <saida.json>"""
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
AUX = re.compile(r"^(_proof_\d+|_simp_\d+(_\d+)*|match_\d+|_sunfold|eq_\d+|eq_def|congr_simp)$")
def aux(nome):
    return bool(AUX.match(nome.split(".")[-1]))
R = {}
# 1) bandeiras
fa, fb = lit(dA, "_LEAN_THEOREM_FLAGS"), lit(dB, "_LEAN_THEOREM_FLAGS")
rem = {k: v for k, v in fa.items() if k not in fb}; add = {k: v for k, v in fb.items() if k not in fa}
chg = [k for k in fa if k in fb and fa[k] != fb[k]]
R["bandeiras"] = {"n_A": len(fa), "n_B": len(fb), "removidas": len(rem), "removidas_nao_auxiliares": sorted(v for v in rem.values() if not aux(v))[:30],
                  "acrescentadas": len(add), "acrescentadas_por_prefixo": {p: sum(1 for k in add if k.startswith(p)) for p in sorted(set(re.sub(r"_\d+$", "", k) for k in add))},
                  "acrescentadas_auxiliares": sorted(v for v in add.values() if aux(v)), "valores_mudados": chg[:10],
                  "B_auxiliares_restantes": sorted(v for v in fb.values() if aux(v))[:10]}
# a escada esperada (lista em prove_external_ladder): a mesma troca?
def lista_escada(T, src):
    for n in T.body:
        if isinstance(n, ast.FunctionDef) and n.name == "prove_external_ladder":
            for m in ast.walk(n):
                if isinstance(m, (ast.List, ast.Tuple, ast.Set)) and len(m.elts) > 1000 and all(isinstance(e, ast.Constant) and isinstance(e.value, str) for e in m.elts):
                    return [e.value for e in m.elts]
    return None
la, lb = lista_escada(TA, sa), lista_escada(TB, sb)
R["escada_lista"] = {"n_A": len(la or []), "n_B": len(lb or []), "B_igual_chaves_das_bandeiras_novas_mais_antigas": (set(lb or []) == (set(la or []) - set(rem)) | set(add)) if la and lb else None}
# 2) specs
sA, sB = {s["nome"]: s for s in lit(dA, "_V394_SPECS")}, {s["nome"]: s for s in lit(dB, "_V394_SPECS")}
sp = {}
for nome in sorted(set(sA) | set(sB)):
    a, b = sA.get(nome), sB.get(nome)
    if a is None: sp[nome] = {"novo": True, "checks": [(c.get("id"), c.get("onde"), c.get("caminho"), c.get("op"), (("dict(%d)" % len(c["valor"])) if isinstance(c.get("valor"), dict) else c.get("valor"))) for c in b.get("checks", [])],
                              "fontes": b.get("fontes"), "verbatins": b.get("verbatins"), "kernel": {k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in (b.get("kernel") or {}).items()}}; continue
    if b is None: sp[nome] = {"removido": True}; continue
    ca, cb = {c["id"]: c for c in a.get("checks", [])}, {c["id"]: c for c in b.get("checks", [])}
    d = {"checks_novos": sorted(set(cb) - set(ca)), "checks_removidos": sorted(set(ca) - set(cb)),
         "checks_mudados": {i: {"A": {k: (("dict(%d)" % len(ca[i][k])) if isinstance(ca[i].get(k), dict) else ca[i].get(k)) for k in ("op", "valor", "caminho")},
                                "B": {k: (("dict(%d)" % len(cb[i][k])) if isinstance(cb[i].get(k), dict) else cb[i].get(k)) for k in ("op", "valor", "caminho")}}
                            for i in ca if i in cb and (ca[i].get("op"), ca[i].get("valor"), ca[i].get("caminho")) != (cb[i].get("op"), cb[i].get("valor"), cb[i].get("caminho"))},
         "outras_chaves_mudadas": sorted(k for k in set(a) | set(b) if k != "checks" and a.get(k) != b.get(k))}
    sp[nome] = d
    # o h8: B == embutidos de B + residuais do Nos?
    if nome == "kh_n1_cobertura_v394" and "h8" in cb:
        pin = cb["h8"]["valor"]; pinA = ca["h8"]["valor"]
        embB = lit(dB, "_EMBEDDED_KERNEL_FILES")
        shaB = {rel: hashlib.sha256(c.encode("utf-8")).hexdigest() for rel, c in embB.items()}
        res = {}
        for f in ("_check_damming.lean",):
            p = os.path.join(NOSK, f)
            if os.path.exists(p): res[f] = hashlib.sha256(open(p, "rb").read()).hexdigest()
        alvo = dict(shaB); alvo.update(res)
        d["h8_analise"] = {"n_A": len(pinA), "n_B": len(pin), "B_igual_embutidos_B_mais_residual_do_Nos": pin == alvo,
                           "so_em_B": sorted(set(pin) - set(pinA)), "so_em_A": sorted(set(pinA) - set(pin)),
                           "mudaram_de_sha": sorted(k for k in pin if k in pinA and pin[k] != pinA[k]),
                           "difere_do_alvo": sorted(k for k in set(pin) | set(alvo) if pin.get(k) != alvo.get(k))[:10]}
R["specs_v394"] = sp
# 3) contratos
for c in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT"):
    a, b = lit(dA, c), lit(dB, c)
    R[c] = {k: {"A": a.get(k) if not isinstance(a.get(k), (list, dict)) else "%s(%d)" % (type(a.get(k)).__name__, len(a.get(k))),
                "B": b.get(k) if not isinstance(b.get(k), (list, dict)) else "%s(%d)" % (type(b.get(k)).__name__, len(b.get(k)))}
            for k in set(a) | set(b) if a.get(k) != b.get(k)}
# 4) fontes, verbatins, nomes de registros
fA, fB = lit(dA, "_V394_FONTES"), lit(dB, "_V394_FONTES")
R["_V394_FONTES"] = {"novas": {k: fB[k].get("arquivo") for k in fB if k not in fA}, "removidas": sorted(set(fA) - set(fB)), "mudadas": sorted(k for k in fA if k in fB and fA[k] != fB[k])}
vA, vB = lit(dA, "_V394_VERBATINS2"), lit(dB, "_V394_VERBATINS2")
R["_V394_VERBATINS2"] = {"novas": {k: {"sha16": vB[k]["sha256"][:16], "bytes": vB[k].get("bytes"), "arquivo": vB[k].get("arquivo"), "text_sha_ok": hashlib.sha256(vB[k]["text"].encode("utf-8")).hexdigest() == vB[k]["sha256"]} for k in vB if k not in vA},
                         "removidas": sorted(set(vA) - set(vB)), "mudadas": sorted(k for k in vA if k in vB and vA[k] != vB[k])}
R["_V394_NOMES_REGISTROS"] = {"A": lit(dA, "_V394_NOMES_REGISTROS"), "B": lit(dB, "_V394_NOMES_REGISTROS")}
# 5) kernel embutido e ledger
eA, eB = lit(dA, "_EMBEDDED_KERNEL_FILES"), lit(dB, "_EMBEDDED_KERNEL_FILES")
R["_EMBEDDED_KERNEL_FILES"] = {"novos": sorted(set(eB) - set(eA)), "removidos": sorted(set(eA) - set(eB)), "mudados": sorted(k for k in eA if k in eB and eA[k] != eB[k])}
for k in R["_EMBEDDED_KERNEL_FILES"]["mudados"]:
    R["_EMBEDDED_KERNEL_FILES"]["diff_" + k] = [l for l in difflib.unified_diff(eA[k].splitlines(), eB[k].splitlines(), lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))][:20]
R["_ESQUELETO_STONES"] = {"so_B": [list(x) for x in lit(dB, "_ESQUELETO_STONES") if tuple(x) not in set(map(tuple, lit(dA, "_ESQUELETO_STONES")))]}
# 6) funcoes de texto e estatuto
for f in ("build_pt", "build_en", "emit_canonical_md", "estatuto_da_prova_v391", "UM_VERSION"):
    if f in dA and f in dB:
        a, b = ast.unparse(dA[f]).splitlines(), ast.unparse(dB[f]).splitlines()
        R["diff_" + f] = [l[:700] for l in difflib.unified_diff(a, b, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))][:30]
json.dump(R, open(S_, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, indent=1, default=str)[:30000])
