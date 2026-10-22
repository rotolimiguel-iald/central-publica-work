"""Reversão da instalação v392 pela receita REVERTER_V392.md (gerência c1, 13/10/2026). Guarda o estado falho como registro, restaura os 8 backups de bytes e põe as 14 pedras em quarentena."""
import datetime
import glob
import hashlib
import json
import os
import shutil

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
CAD = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392"
TS = "20261013_160923"
T2 = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
alvos = ["um.py", "um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md",
         "um_absoluto_pilar_quantico.json", os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")]
rec = {"ts": T2, "backups": TS, "guardado": [], "restaurado": [], "quarentena": []}

# 1. guardar o estado falho como registro
reg = os.path.join(CAD, "tentativa1_rito_falhou_" + T2)
os.makedirs(reg)
for a in alvos + ["rodada_v392_stdout.txt"]:
    p = os.path.join(NOS, a)
    if os.path.exists(p):
        d = os.path.join(reg, a.replace(os.sep, "__"))
        shutil.copyfile(p, d)
        rec["guardado"].append({"arquivo": a, "sha16": sh(d)[:16], "bytes": os.path.getsize(d)})

# 2. restaurar os 8 backups de bytes
for a in alvos:
    p = os.path.join(NOS, a)
    b = p + ".bak_" + TS
    assert os.path.exists(b), b
    data = open(b, "rb").read()
    tmp = p + ".tmp_reverter"
    open(tmp, "wb").write(data)
    assert os.path.getsize(tmp) == len(data) and sh(tmp) == hashlib.sha256(data).hexdigest()
    os.replace(tmp, p)
    rec["restaurado"].append({"arquivo": a, "sha16": sh(p)[:16]})

# 3. quarentena das 14 pedras novas
esp = json.load(open(os.path.join(CAD, "ESPERADOS_v392.json"), encoding="utf-8"))
qd = os.path.join(CAD, "quarentena_pedras_" + T2)
os.makedirs(qd)
for nome in esp.get("pedras_sha256", {}):
    rel = nome.replace("/", os.sep)
    cands = [os.path.join(NOS, "tgl_kernel", rel), os.path.join(NOS, "tgl_kernel", "TGLExt", os.path.basename(rel))]
    for c in cands:
        if os.path.isfile(c):
            shutil.move(c, os.path.join(qd, os.path.basename(c)))
            rec["quarentena"].append(os.path.basename(c))
            break

umsha = sh(os.path.join(NOS, "um.py"))[:16]
rec["um_py_sha16"] = umsha
rec["ok"] = umsha == "8e7b9927ceae64b8"
json.dump(rec, open(os.path.join(CAD, "RECIBO_REVERSAO_" + T2 + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"ok": rec["ok"], "um_py": umsha, "restaurados": len(rec["restaurado"]), "quarentena": len(rec["quarentena"]), "registro": reg}, ensure_ascii=False))
