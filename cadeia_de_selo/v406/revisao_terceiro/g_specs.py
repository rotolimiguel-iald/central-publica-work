# -*- coding: utf-8 -*-
"""Revisor terceiro v406: os quatro blocos de specs reescritos por pformat (_V394_SPECS, _V395_SPECS, _V396_SPECS, _V405_SPECS) e os contratos _V402..405_CONTRACTS,
_V39x_*_CONTRACT: o que mudou base v405 -> candidato, ao nivel de campo."""
import ast, json, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v406/"
def lit(p, nomes):
    s = open(p, "rb").read().decode("utf-8"); tr = ast.parse(s); out = {}
    for n in tr.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in nomes:
            out[n.targets[0].id] = ast.literal_eval(n.value)
    return out
NOMES = ["_V394_SPECS", "_V395_SPECS", "_V396_SPECS", "_V405_SPECS", "_V394_FORMAL_CONTRACT", "_V394_NETWORK_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT",
         "_V398_AFINACAO_CONTRACT", "_V398_SONICO_CONTRACT", "_V401_FALSIDADE_CONTRACT", "_V402_CONTRACTS", "_V403_CONTRACTS", "_V404_CONTRACTS", "_V405_CONTRACTS", "_ESQUELETO_STONES", "UM_VERSION"]
B = lit(R + "base_v405/um.py", NOMES); C = lit(R + "um_v406_candidato.py", NOMES)
def difs(a, b, p=""):
    out = []
    if type(a) != type(b): return [(p, "tipo", repr(a)[:80], repr(b)[:80])]
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b), key=str):
            if k not in a: out.append((p + "/" + str(k), "novo", None, repr(b[k])[:200]))
            elif k not in b: out.append((p + "/" + str(k), "removido", repr(a[k])[:200], None))
            else: out += difs(a[k], b[k], p + "/" + str(k))
    elif isinstance(a, list):
        if all(isinstance(x, dict) and "id" in x for x in a + b) and a and b:
            da = {x["id"]: x for x in a}; db = {x["id"]: x for x in b}
            for k in da:
                if k not in db: out.append((p + "[id=%s]" % k, "removido", "", ""))
            for k in db:
                if k not in da: out.append((p + "[id=%s]" % k, "novo", "", repr(db[k])[:200]))
                else: out += difs(da[k], db[k], p + "[id=%s]" % k)
        else:
            if len(a) != len(b): out.append((p, "len", len(a), len(b)))
            for i, (x, y) in enumerate(zip(a, b)): out += difs(x, y, p + "[%d]" % i)
    else:
        if a != b: out.append((p, "valor", repr(a)[:300], repr(b)[:300]))
    return out
for n in NOMES:
    if n not in B or n not in C: print("ausente", n, n in B, n in C); continue
    d = difs(B[n], C[n], n)
    print("=====", n, "mudancas:", len(d))
    for x in d[:60]:
        print("  ", x[0][:140], "|", x[1]);
        if x[2] is not None: print("       base:", str(x[2])[:260])
        if x[3] is not None: print("       cand:", str(x[3])[:360])
