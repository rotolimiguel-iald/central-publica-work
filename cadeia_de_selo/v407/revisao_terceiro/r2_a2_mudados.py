# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R1): os 25 nomes de nivel superior que mudaram. Para cada constante literal: deep-diff base x candidato por literal_eval;
para as funcoes: diff de fonte (resumido). Confere (d): todos os 'expected_ladder': 11860 viraram 11958 e so' eles. So le."""
import ast, difflib, hashlib, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
bs = open(R + "base_v406/um.py", "rb").read().decode("utf-8"); cs = open(R + "um_v407_candidato.py", "rb").read().decode("utf-8")
bt = ast.parse(bs); ct = ast.parse(cs); bl = bs.split("\n"); cl = cs.split("\n")
MUD = ['UM_VERSION', '_EMBEDDED_KERNEL_FILES', '_ESQUELETO_STONES', '_LEAN_THEOREM_FLAGS', '_V394_FORMAL_CONTRACT', '_V394_NETWORK_CONTRACT', '_V394_QUADRATIC_CONTRACT', '_V395_PSIBIT_CONTRACT', '_V396_TESTEMUNHA_CONTRACT', '_V398_AFINACAO_CONTRACT', '_V398_SONICO_CONTRACT', '_V401_FALSIDADE_CONTRACT', '_V402_CONTRACTS', '_V403_CONTRACTS', '_V404_CONTRACTS', '_V405_CONTRACTS', '_V406_FECHO_CONTRACT', '_V406_SPECS', 'build_en', 'build_pt', 'emit_canonical_md', 'main', 'prove_external_ladder']


def nodo(tr, nome):
    for n in tr.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == nome: return n
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == nome: return n
    return None


def dd(a, b, path="", out=None, lim=40):
    if out is None: out = []
    if len(out) > lim: return out
    if type(a) != type(b): out.append((path, "tipo", repr(a)[:120], repr(b)[:120])); return out
    if isinstance(a, dict):
        for k in a:
            if k not in b: out.append((path + "/" + str(k), "removida", repr(a[k])[:100], None))
            else: dd(a[k], b[k], path + "/" + str(k), out, lim)
        for k in b:
            if k not in a: out.append((path + "/" + str(k), "nova", None, repr(b[k])[:160]))
    elif isinstance(a, (list, tuple)):
        if len(a) != len(b):
            out.append((path, "len %d->%d" % (len(a), len(b)), None, None))
            # o que ha' a mais
            sa = {json.dumps(x, sort_keys=True, default=str) for x in a}; sb = [json.dumps(x, sort_keys=True, default=str) for x in b]
            novos = [x[:100] for x in sb if x not in sa]; out.append((path, "novos_elementos_n", len(novos), novos[:3]))
            sb_ = set(sb); gone = [json.dumps(x, sort_keys=True, default=str)[:100] for x in a if json.dumps(x, sort_keys=True, default=str) not in sb_]; out.append((path, "elementos_removidos_n", len(gone), gone[:3]))
        else:
            for i, (x, y) in enumerate(zip(a, b)): dd(x, y, path + "[%d]" % i, out, lim)
    else:
        if a != b: out.append((path, "valor", repr(a)[:200], repr(b)[:200]))
    return out


resumo = {}
for nome in MUD:
    a = nodo(bt, nome); b = nodo(ct, nome)
    if isinstance(a, ast.Assign):
        try:
            va = ast.literal_eval(a.value); vb = ast.literal_eval(b.value)
        except Exception as e:
            la = "\n".join(bl[a.lineno - 1:a.end_lineno]); lb = "\n".join(cl[b.lineno - 1:b.end_lineno])
            print("==", nome, "(nao literal)", len(la), len(lb));
            for l in list(difflib.unified_diff(la.split("\n"), lb.split("\n"), "base", "cand", lineterm="", n=0))[:12]: print("   ", l[:300])
            continue
        d = dd(va, vb)
        print("==", nome, "diferencas:", len(d))
        if nome == "_EMBEDDED_KERNEL_FILES":
            print("   so repasso: novas chaves", sorted(set(vb) - set(va)), "removidas", sorted(set(va) - set(vb)), "mudadas", [k for k in va if k in vb and va[k] != vb[k]])
        else:
            for x in d[:14]: print("   ", x)
        resumo[nome] = [list(map(str, x)) for x in d[:40]]
    else:
        la = "\n".join(bl[a.lineno - 1:a.end_lineno]); lb = "\n".join(cl[b.lineno - 1:b.end_lineno])
        print("==", nome, "(funcao)", len(la), len(lb))
        if nome in ("main", "build_pt", "build_en", "emit_canonical_md", "prove_external_ladder"):
            for l in list(difflib.unified_diff(la.split("\n"), lb.split("\n"), "base", "cand", lineterm="", n=0))[:40]: print("   ", l[:420])

# (d) expected_ladder
nb = len(re.findall(r"'expected_ladder': 11860\b|\"expected_ladder\": 11860\b", bs)); nc = len(re.findall(r"'expected_ladder': 11958\b|\"expected_ladder\": 11958\b", cs))
print("expected_ladder 11860 na base:", nb, "| 11958 no cand:", nc, "| 11860 restantes no cand:", len(re.findall(r"'expected_ladder': 11860\b|\"expected_ladder\": 11860\b", cs)))
outros_b = re.findall(r"expected_ladder['\"]\s*:\s*(\d+)", bs); outros_c = re.findall(r"expected_ladder['\"]\s*:\s*(\d+)", cs)
from collections import Counter
print("valores expected_ladder base:", Counter(outros_b), "cand:", Counter(outros_c))
print("occorrencias 11860 total base:", bs.count("11860"), "cand:", cs.count("11860"), "| 11958 cand:", cs.count("11958"))
# o Expr novo
for n in ct.body:
    if isinstance(n, ast.Expr):
        print("Expr topo:", n.lineno, ast.dump(n)[:200])
json.dump(resumo, open(R + "revisao_terceiro/r2_a2_mudados_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
