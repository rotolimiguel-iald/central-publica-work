# -*- coding: utf-8 -*-
"""reverter_v393.py -- REVERSAO da instalacao v393 (ato da gerencia c1; usar so' se o rito falhar). Le o ULTIMO APLICADO_AO_CANONICO_*.json desta pasta (o carimbo dos backups; nada digitado),
guarda o estado falho como registro, restaura os 8 backups de BYTES (um.py, core, selo, .md, manifesto, pilar, TGLExt.lean, TGL/Audit.lean) e poe as 3 pedras da regra em QUARENTENA (nunca apaga).
Confere ao fim que o um.py voltou a ser a v392 selada (b590c0aa80055e2a). Fail-closed: backup ausente => para sem tocar o que resta. Molde: reverter_v392.py (que tinha o carimbo digitado)."""
import datetime, glob, hashlib, json, os, shutil, sys

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
CAD = os.path.dirname(os.path.abspath(__file__))
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
ap_p = sorted(glob.glob(os.path.join(CAD, "APLICADO_AO_CANONICO_*.json")))
assert ap_p, "nenhum APLICADO_AO_CANONICO_*.json: nada instalado por instalar_v393.py"
AP = json.load(open(ap_p[-1], encoding="utf-8")); TS = AP["ts"]
T2 = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
alvos = list(AP["backups"].keys())
assert sorted(alvos) == sorted(["um.py", "um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "um_absoluto_pilar_quantico.json",
                                os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")]), alvos
for a in alvos:   # fail-closed: todos os backups existem e batem com o que o instalador gravou, ANTES de qualquer escrita
    b = AP["backups"][a]["backup"]; assert os.path.exists(b) and sh(b)[:16] == AP["backups"][a]["sha16"], ("backup ausente ou alterado", b)
rec = {"ts": T2, "backups": TS, "aplicado": os.path.basename(ap_p[-1]), "guardado": [], "restaurado": [], "quarentena": []}
reg = os.path.join(CAD, "tentativa_v393_rito_falhou_" + T2)
os.makedirs(reg)
for a in alvos + ["rodada_v393_stdout.txt"]:
    p = os.path.join(NOS, a)
    if os.path.exists(p):
        d = os.path.join(reg, a.replace(os.sep, "__")); shutil.copyfile(p, d)
        rec["guardado"].append({"arquivo": a, "sha16": sh(d)[:16], "bytes": os.path.getsize(d)})
for a in alvos:
    p = os.path.join(NOS, a); b = AP["backups"][a]["backup"]
    data = open(b, "rb").read(); tmp = p + ".tmp_reverter"
    open(tmp, "wb").write(data)
    assert os.path.getsize(tmp) == len(data) and sh(tmp) == hashlib.sha256(data).hexdigest()
    os.replace(tmp, p)
    rec["restaurado"].append({"arquivo": a, "sha16": sh(p)[:16]})
esp = json.load(open(os.path.join(CAD, "ESPERADOS_v393.json"), encoding="utf-8"))
qd = os.path.join(CAD, "quarentena_pedras_" + T2)
os.makedirs(qd)
for nome in esp.get("pedras_sha256", {}):
    p = os.path.join(NOS, "tgl_kernel", *nome.split("/"))
    if os.path.isfile(p):
        shutil.move(p, os.path.join(qd, os.path.basename(p))); rec["quarentena"].append(os.path.basename(p))
umsha = sh(os.path.join(NOS, "um.py"))[:16]
rec["um_py_sha16"] = umsha
rec["ok"] = umsha == esp["origem_sha16"] == "b590c0aa80055e2a"
json.dump(rec, open(os.path.join(CAD, "RECIBO_REVERSAO_" + T2 + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"ok": rec["ok"], "um_py": umsha, "restaurados": len(rec["restaurado"]), "quarentena": len(rec["quarentena"]), "registro": reg}, ensure_ascii=False))
sys.exit(0 if rec["ok"] else 1)
