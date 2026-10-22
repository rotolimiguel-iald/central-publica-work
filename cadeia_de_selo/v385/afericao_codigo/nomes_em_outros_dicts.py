# SO LEITURA: os 28 nomes Lean aparecem em OUTRO dicionario de bandeiras (que viraria True so por a auditoria passar a imprimi-los)?
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
PK = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v385"
ESP = json.load(open(PK + r"\ESPERADOS_v385.json", encoding="utf-8"))
names = sorted(set(ESP["nomes_lean_v385"].values()))
L = open(PK + r"\um_v385_candidato.py", encoding="utf-8").read().splitlines()
# zonas: o dicionario embutido do kernel (8689 .. fim dele) e o _LEAN_THEOREM_FLAGS
def span(prefix):
    i = [k for k, l in enumerate(L) if l.startswith(prefix)][0]; j = i + 1
    while L[j].rstrip() != "}":
        j += 1
    return i, j
ek = span("_EMBEDDED_KERNEL_FILES = {"); lf = span("_LEAN_THEOREM_FLAGS = {")
hits = []
for n in names:
    pat = re.compile(r'["\']' + re.escape(n) + r'["\']')
    for k, l in enumerate(L):
        if ek[0] <= k <= ek[1] or lf[0] <= k <= lf[1]:
            continue
        if pat.search(l):
            hits.append((n, k + 1, l.strip()[:160]))
print("ocorrencias dos 28 nomes (entre aspas) fora do kernel embutido e de _LEAN_THEOREM_FLAGS:", len(hits))
for h in hits[:30]:
    print(h)
# e no core da v384: alguma bandeira (de qualquer prefixo) cujo valor depende desses nomes? (axiom_report da v384 ja os tinha?)
core = json.load(open(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json", encoding="utf-8"))["core"]
axr = (core.get("kernel_formalization") or {}).get("axiom_report") or {}
print("dos 28 nomes, ja no axiom_report da v384:", [n for n in names if n in axr])
