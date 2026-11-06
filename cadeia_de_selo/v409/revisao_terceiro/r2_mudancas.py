import hashlib, json, sys, difflib, os, glob
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
r1 = json.load(open(R + "revisao_terceiro/REVISAO_TERCEIRO_v409.R1.json", encoding="utf-8"))
sha16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
mud = {}
for k, v in r1["arquivos_revisados"].items():
    n = sha16(R + k)
    if n != v: mud[k] = (v, n)
print("mudaram desde a R1:", json.dumps(mud, indent=1))
# outros arquivos recentes na pasta v409 (pos R1 21:54+)
import time
ref = os.path.getmtime(R + "revisao_terceiro/REVISAO_TERCEIRO_v409.R1.json")
rec = []
for dp, dn, fn in os.walk(R):
    if "revisao_terceiro" in dp or "__pycache__" in dp or "sim_" in dp or "imp_" in dp or "arvore_simulada" in dp or "conferidor_import" in dp or "antes_de" in dp: continue
    for f in fn:
        p = os.path.join(dp, f)
        try:
            if os.path.getmtime(p) > ref - 1800 and not f.endswith((".pyc",)) and ".bak_" not in f: rec.append((time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(p))), os.path.relpath(p, R)))
        except OSError: pass
for t, p in sorted(rec)[:80]: print(t, p)
