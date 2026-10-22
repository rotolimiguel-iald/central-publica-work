# -*- coding: utf-8 -*-
"""Tentativa 2 da v380 (01/10/2026): a leitura gravada no selo da tentativa 1 nao trazia as correcoes do aferidor (subamostra; V5; 6+1+1 erratas).
Para reinstalar pelo molde (instalar_v380.py exige que o canonico seja a v379 selada), este script:
  (1) confere que o um.py do disco e a tentativa 1 (sha16 lido de APLICADO_AO_CANONICO_* mais recente) e que o backup do instalador e a v379 (origem_sha16 de ESPERADOS);
  (2) PRESERVA ao lado a tentativa 1: um.py, um_absoluto.json, um_absoluto_selo.json e rodada_v380_stdout.txt copiados como *.v380_tentativa1_<ts> (bytes conferidos);
  (3) repoe o um.py da v379 a partir do backup do instalador (bytes conferidos; tmp -> conferir -> replace).
Nao apaga nada. Fail-closed: qualquer sha diferente do esperado aborta antes de tocar."""
import os, sys, json, glob, hashlib, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
h16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v380.json"), encoding="utf-8"))
ap = json.load(open(sorted(glob.glob(os.path.join(HERE, "APLICADO_AO_CANONICO_*.json")))[-1], encoding="utf-8"))
t1 = ap["um_py_novo"]["sha16"]; bak = ap["backups"]["um.py"]["backup"]
um = os.path.join(NOS, "um.py"); raw = open(um, "rb").read()
assert h16(raw) == t1, "o um.py do disco (%s) nao e a tentativa 1 instalada (%s) -- nao toco" % (h16(raw), t1)
base = open(bak, "rb").read(); assert h16(base) == ESP["origem_sha16"] == ap["backups"]["um.py"]["sha16"], "o backup do instalador nao e a v379 selada"
ts = time.strftime("%Y%m%d_%H%M%S"); rec = {"ts": ts, "tentativa1_um_py_sha16": t1, "preservados": {}}
for rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "rodada_v380_stdout.txt"):
    p = os.path.join(NOS, rel)
    if not os.path.exists(p):
        print("ausente (nao preservado):", rel); continue
    b = open(p, "rb").read(); q = p + ".v380_tentativa1_" + ts; assert not os.path.exists(q)
    with open(q, "wb") as f:
        f.write(b)
    assert open(q, "rb").read() == b; rec["preservados"][rel] = {"copia": q, "bytes": len(b), "sha16": h16(b)}
tmp = um + ".tmp_restaurar_" + ts
with open(tmp, "wb") as f:
    f.write(base)
assert open(tmp, "rb").read() == base and open(um, "rb").read() == raw
os.replace(tmp, um); assert h16(open(um, "rb").read()) == ESP["origem_sha16"]
rec["um_py_restaurado"] = {"sha16": ESP["origem_sha16"], "de": bak}
out = os.path.join(HERE, "RESTAURADO_BASE_V379_TENTATIVA2_%s.json" % ts)
json.dump(rec, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1); print(json.dumps(rec, ensure_ascii=False, indent=1))
