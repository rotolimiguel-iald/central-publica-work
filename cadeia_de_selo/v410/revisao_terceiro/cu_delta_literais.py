# -*- coding: utf-8 -*-
"""Conferencia unica, item A: para os literais herdados da v409 que mudaram desde a R3, mostra o que muda por trecho (difflib em nivel de caractere ao redor da diferenca)."""
import ast, difflib, hashlib, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
a = open(R + "um_v410_candidato.pre_r6fix.py", "rb").read().decode("utf-8")
b = open(R + "um_v410_candidato.py", "rb").read().decode("utf-8")
c = open(R + "base_v409/um.py", "rb").read().decode("utf-8")


def segs(src):
    tr = ast.parse(src); L = src.split("\n"); d = {}
    for n in tr.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            d[n.targets[0].id] = "\n".join(L[n.lineno - 1:n.end_lineno])
    return d


A = segs(a); B = segs(b); C = segs(c)
NOMES = ["_EMBEDDED_KERNEL_FILES", "_V394_FORMAL_CONTRACT", "_V394_NETWORK_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V398_SONICO_CONTRACT", "_V401_FALSIDADE_CONTRACT", "_V402_CONTRACTS", "_V403_CONTRACTS", "_V404_CONTRACTS", "_V405_CONTRACTS", "_V406_FECHO_CONTRACT", "_V407_PSION_CONTRACT", "_V408_TERMINAL_CONTRACT", "_V409_SPECS", "_V409_TRADUCAO_CONTRACT", "_V410_FONTES", "_V410_HMS13_TEXT"]


def trechos(x, y, ctx=40, maxn=6):
    sm = difflib.SequenceMatcher(None, x, y, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal": continue
        out.append((tag, x[max(0, i1 - ctx):i1] + "[[" + x[i1:i2][:200] + "]]" + x[i2:i2 + ctx], y[max(0, j1 - ctx):j1] + "[[" + y[j1:j2][:200] + "]]" + y[j2:j2 + ctx]))
        if len(out) >= maxn: break
    return out


for nm in NOMES:
    if nm == "_EMBEDDED_KERNEL_FILES" or len(A[nm]) > 3_000_000:
        # grande: so as linhas que diferem
        la = A[nm].split("\n"); lb = B[nm].split("\n")
        print("==", nm, "linhas", len(la), len(lb))
        for i, (x, y) in enumerate(zip(la, lb)):
            if x != y:
                print("  linha", i, "tam", len(x), len(y), "| sha16", hashlib.sha256(x.encode()).hexdigest()[:10], hashlib.sha256(y.encode()).hexdigest()[:10])
                # trechos curtos
                sm = difflib.SequenceMatcher(None, x[:400], y[:400], autojunk=False)
                print("    inicio a:", x[:160].replace("\n", " "))
                print("    inicio b:", y[:160].replace("\n", " "))
        continue
    if A[nm] == B[nm]: continue
    print("==", nm, "tam", len(A[nm]), len(B[nm]), "| v409 tinha:", nm in C and C[nm] == A[nm])
    la = A[nm].split("\n"); lb = B[nm].split("\n")
    # diferenca linha a linha, depois por caracteres
    n = 0
    for x, y in zip(la, lb):
        if x != y:
            for t in trechos(x, y, 36, 3):
                print("   ", t[0], "\n      a:", t[1].replace("\n", "|"), "\n      b:", t[2].replace("\n", "|"))
            n += 1
            if n >= 3: break
