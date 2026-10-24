# -*- coding: utf-8 -*-
"""reprodutibilidade.py -- o selo ACOM e' REPRODUTIVEL entre interpretadores? Roda o `selar` do prototipo em DOIS Pythons/numpy/zlib diferentes (processos criados
aqui, que terminam sozinhos) sobre os mesmos tres objetos (um.py v398, core, selo da rodada) e confronta, objeto a objeto, os hashes de Psi, Theta e kappa e o SHA-256.
Saida: recibos/RECIBO_REPRODUTIBILIDADE.json. Uso: python -B -X utf8 reprodutibilidade.py"""
import json
import os
import subprocess
import sys
import time

W = os.path.dirname(os.path.abspath(__file__))
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
PROTO = os.path.join(W, "selo_acom_prototipo.py")
OBJ = [os.path.join(NOS, n) for n in ("um.py", "um_absoluto.json", "um_absoluto_selo.json")]
INTERPRETES = {
    "py3.14.3 + numpy 2.4.3 + zlib-ng 2.2.4": r"C:\Python314\python.exe",
    "py3.13.14 + numpy 2.4.1 + zlib 1.3.1": r"C:\Users\rotol\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe",
}
res = {}
for nome, exe in INTERPRETES.items():
    t0 = time.perf_counter()
    r = subprocess.run([exe, "-B", "-X", "utf8", PROTO, "selar"] + OBJ, capture_output=True, text=True, encoding="utf-8", timeout=900)
    dt = time.perf_counter() - t0
    if r.returncode != 0:
        res[nome] = {"erro": r.stderr[-600:], "returncode": r.returncode}
        continue
    sc = json.loads(r.stdout)
    import hashlib
    res[nome] = {"returncode": 0, "tempo_s": dt, "veredito": sc["veredito"], "beta_runtime": sc["beta_runtime"],
                 "objetos_do_sidecar_inteiros_sha256": hashlib.sha256(json.dumps(sc["objetos"], sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest(),
                 "objetos": {o["nome"]: {"sha256": o["sha256"], "psi": o["acom"]["psi"]["sha256"], "theta": o["acom"]["theta"]["sha256"], "kappa": o["acom"]["kappa"]["sha256"],
                                         "lut": o["acom"]["kappa"]["campos"]["lut_sha256"]} for o in sc["objetos"]}}
nomes = list(INTERPRETES)
ok = all("objetos" in res[n] for n in nomes)
iguais = {}
if ok:
    a, b = res[nomes[0]]["objetos"], res[nomes[1]]["objetos"]
    for obj in a:
        iguais[obj] = {k: a[obj][k] == b[obj][k] for k in a[obj]}
    iguais["_sidecar_objetos_inteiros_byte_a_byte"] = (res[nomes[0]]["objetos_do_sidecar_inteiros_sha256"] == res[nomes[1]]["objetos_do_sidecar_inteiros_sha256"])
    todos = all(all(v.values()) if isinstance(v, dict) else bool(v) for v in iguais.values()) and res[nomes[0]]["beta_runtime"] == res[nomes[1]]["beta_runtime"]
else:
    todos = False
out = {"interpretes": res, "iguais_por_objeto_e_campo": iguais, "todos_iguais": todos, "quando": time.strftime("%Y-%m-%d %H:%M:%S")}
os.makedirs(os.path.join(W, "recibos"), exist_ok=True)
p = os.path.join(W, "recibos", "RECIBO_REPRODUTIBILIDADE.json")
if os.path.exists(p):
    with open(p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"), "xb") as f:
        f.write(open(p, "rb").read())
with open(p, "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(json.dumps({"todos_iguais": todos, "iguais": iguais, "tempos": {n: res[n].get("tempo_s") for n in nomes}}, ensure_ascii=False, indent=1))
