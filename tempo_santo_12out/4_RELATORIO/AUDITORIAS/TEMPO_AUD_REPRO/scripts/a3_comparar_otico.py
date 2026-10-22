"""A3 — compara folha a folha o RESULTADO_OPTICO do construtor com o da COPIA rodada pelo auditor.
Ignora so chaves volateis (horarios, segundos, caminho do runner, numero da tentativa, taken_at).
Tambem compara o ACHADOS_FORA_DO_PREREGISTRO.json (bytes) e o log (linhas sem o carimbo de hora).
Saida: JSON no caminho dado."""
import hashlib
import json
import os
import re
import sys

ORIG = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\2_OPTICO"
COPIA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "otico_copia", "2_OPTICO")
VOLATEIS = {"inicio_local", "fim_local", "segundos", "taken_at", "seconds", "tentativa", "arquivo"}

a = json.load(open(os.path.join(ORIG, "RESULTADO_OPTICO.json"), encoding="utf-8"))
b = json.load(open(os.path.join(COPIA, "RESULTADO_OPTICO.json"), encoding="utf-8"))
difs = []
n_leaves = [0]
n_num = [0]


def walk(x, y, path):
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) | set(y)):
            if k in VOLATEIS:
                continue
            if k not in x or k not in y:
                difs.append({"caminho": path + "/" + k, "so_em": "original" if k in x else "copia"})
                continue
            walk(x[k], y[k], path + "/" + k)
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            difs.append({"caminho": path, "len": [len(x), len(y)]})
        for i, (u, v) in enumerate(zip(x, y)):
            walk(u, v, "%s[%d]" % (path, i))
    else:
        n_leaves[0] += 1
        if isinstance(x, (int, float)) and not isinstance(x, bool):
            n_num[0] += 1
        if x != y:
            difs.append({"caminho": path, "original": x, "copia": y})


walk(a, b, "")
out = {"folhas_comparadas": n_leaves[0], "folhas_numericas": n_num[0], "diferencas": difs}
ha = hashlib.sha256(open(os.path.join(ORIG, "ACHADOS_FORA_DO_PREREGISTRO.json"), "rb").read()).hexdigest()
hb = hashlib.sha256(open(os.path.join(COPIA, "ACHADOS_FORA_DO_PREREGISTRO.json"), "rb").read()).hexdigest()
out["achados_sha256"] = {"original": ha, "copia": hb, "identicos": ha == hb}


def log_lines(p):
    L = []
    for ln in open(p, encoding="utf-8").read().splitlines():
        ln = re.sub(r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d  ", "", ln)
        ln = re.sub(r"tentativa \d{3} \(ensaio\) — .*$", "tentativa NNN (ensaio) — <dir>", ln)
        L.append(ln)
    return L


la = log_lines(os.path.join(ORIG, "run_optico.log"))
lb = log_lines(os.path.join(COPIA, "run_optico.log"))
ld = [(i, u, v) for i, (u, v) in enumerate(zip(la, lb)) if u != v]
out["log"] = {"linhas_original": len(la), "linhas_copia": len(lb), "linhas_diferentes": len(ld),
              "exemplos": ld[:12]}
tmp = sys.argv[1] + ".tmp"
with open(tmp, "w", encoding="utf-8") as fo:
    json.dump(out, fo, indent=1, ensure_ascii=False)
os.replace(tmp, sys.argv[1])
print("folhas comparadas:", n_leaves[0], "numericas:", n_num[0], "diferencas:", len(difs))
for d in difs[:40]:
    print(" ", json.dumps(d, ensure_ascii=False)[:300])
print("achados identicos:", out["achados_sha256"]["identicos"])
print("log: linhas", len(la), len(lb), "diferentes", len(ld))
for i, u, v in ld[:12]:
    print("  L%d\n    O: %s\n    C: %s" % (i, u[:200], v[:200]))
