# -*- coding: utf-8 -*-
"""Revisor terceiro v410 (R1): os 26 nos de nivel superior que mudaram. Constantes literais: deep-diff base x candidato por literal_eval (os contratos: SO' expected_ladder 12187->12271);
funcoes: diff de fonte; _EMBEDDED_KERNEL_FILES/_ESQUELETO_STONES/_LEAN_THEOREM_FLAGS: so' acrescimos. So le."""
import ast, difflib, json, re, sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
bs = open(R + "base_v409/um.py", "rb").read().decode("utf-8"); cs = open(R + "um_v410_candidato.py", "rb").read().decode("utf-8")
bt = ast.parse(bs); ct = ast.parse(cs); bl = bs.split("\n"); cl = cs.split("\n")
MUD = json.load(open(R + "revisao_terceiro/a_intocados_out.json", encoding="utf-8"))["mudados"]


def nodo(tr, nome):
    for n in tr.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == nome: return n
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == nome: return n
    return None


def dd(a, b, path="", out=None, lim=400):
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
            sa = [json.dumps(x, sort_keys=True, default=str) for x in a]; sb = [json.dumps(x, sort_keys=True, default=str) for x in b]
            ca, cb = Counter(sa), Counter(sb)
            out.append((path, "novos_elementos_n", sum((cb - ca).values()), [x[:100] for x in (cb - ca)][:3]))
            out.append((path, "elementos_removidos_n", sum((ca - cb).values()), [x[:100] for x in (ca - cb)][:3]))
        else:
            for i, (x, y) in enumerate(zip(a, b)): dd(x, y, path + "[%d]" % i, out, lim)
    else:
        if a != b: out.append((path, "valor", repr(a)[:200], repr(b)[:200]))
    return out


resumo = {}; contratos_ok = {}
for nome in MUD:
    a = nodo(bt, nome); b = nodo(ct, nome)
    if isinstance(a, ast.Assign):
        try:
            va = ast.literal_eval(a.value); vb = ast.literal_eval(b.value)
        except Exception as e:
            la = "\n".join(bl[a.lineno - 1:a.end_lineno]); lb = "\n".join(cl[b.lineno - 1:b.end_lineno])
            print("==", nome, "(nao literal)", len(la), len(lb))
            for l in list(difflib.unified_diff(la.split("\n"), lb.split("\n"), "base", "cand", lineterm="", n=0))[:12]: print("   ", l[:300])
            continue
        d = dd(va, vb)
        print("==", nome, "diferencas:", len(d))
        if nome == "_EMBEDDED_KERNEL_FILES":
            print("   novas chaves", sorted(set(vb) - set(va)), "removidas", sorted(set(va) - set(vb)), "mudadas", [k for k in va if k in vb and va[k] != vb[k]])
            print("   ordem da base e' prefixo:", list(vb)[:len(va)] == list(va))
        elif nome == "_LEAN_THEOREM_FLAGS":
            novas = set(vb) - set(va)
            print("   n base", len(va), "n cand", len(vb), "| base e' sub-dict igual:", all(vb.get(k) == v for k, v in va.items()), "| novas:", len(novas), "todas ext_iald2_410_/ext_aescala_410_:", all(k.startswith(("ext_iald2_410_", "ext_aescala_410_")) for k in novas))
            print("   valores novos sem repeticao:", len(set(vb[k] for k in novas)) == len(novas), "| valor novo coincide com valor antigo:", any(vb[k] in set(va.values()) for k in novas))
        elif nome == "_ESQUELETO_STONES":
            print("   tipo", type(va).__name__, "len", len(va), "->", len(vb), "| base e' prefixo:", (list(vb)[:len(va)] == list(va)) if isinstance(va, (list, tuple)) else None)
            for x in d[:8]: print("   ", x)
        else:
            solo_ladder = all(x[0].endswith("expected_ladder") and x[2] == "12187" and x[3] == "12271" for x in d)
            contratos_ok[nome] = (len(d), solo_ladder)
            for x in d[:14]: print("   ", x)
            if nome.endswith("CONTRACT") or nome.endswith("CONTRACTS"): print("   >> so' expected_ladder 12187->12271:", solo_ladder)
        resumo[nome] = [list(map(str, x)) for x in d[:60]]
    else:
        la = "\n".join(bl[a.lineno - 1:a.end_lineno]); lb = "\n".join(cl[b.lineno - 1:b.end_lineno])
        print("==", nome, "(funcao)", len(la), len(lb))
        dif = list(difflib.unified_diff(la.split("\n"), lb.split("\n"), "base", "cand", lineterm="", n=0))
        rem = [l for l in dif if l.startswith("-") and not l.startswith("---")]; add = [l for l in dif if l.startswith("+") and not l.startswith("+++")]
        print("   linhas removidas:", len(rem), "| acrescentadas:", len(add))
        for l in rem[:12]: print("   REM", l[:300])
        for l in add[:int(14)]: print("   ADD", l[:300])
        resumo[nome] = {"rem": len(rem), "add": len(add)}
nb = len(re.findall(r"'expected_ladder': 12187\b|\"expected_ladder\": 12187\b", bs)); nc = len(re.findall(r"'expected_ladder': 12271\b|\"expected_ladder\": 12271\b", cs))
print("expected_ladder 12187 na base:", nb, "| 12271 no cand:", nc, "| 12187 restantes no cand:", len(re.findall(r"'expected_ladder': 12187\b|\"expected_ladder\": 12187\b", cs)))
print("valores expected_ladder base:", Counter(re.findall(r"expected_ladder['\"]\s*:\s*(\d+)", bs)), "cand:", Counter(re.findall(r"expected_ladder['\"]\s*:\s*(\d+)", cs)))
print("contratos so' expected_ladder:", contratos_ok)
json.dump(resumo, open(R + "revisao_terceiro/a2_mudados_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
