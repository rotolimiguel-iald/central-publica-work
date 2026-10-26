# -*- coding: utf-8 -*-
"""limpar_vb17_v400.py -- guarda a EVIDENCIA do sandbox curto C:\\t\\vb17 (as fotografias da producao e do Nos antes/depois da reconferencia do recibo pre_selo e os controles negativos) em
bateria_pre_selo\\vb17_evidencia (copia de BYTES, com o sha256 de cada arquivo em VB17_EVIDENCIA_v400.json) e SO' ENTAO apaga C:\\t\\vb17 (a pasta que ESTA preparacao criou; nada mais). Reexecutavel: se C:\\t\\vb17 ja' nao existe, so' o diz.
uso: python -I -B -X utf8 limpar_vb17_v400.py"""
import hashlib, json, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
VB = os.path.join("C:" + os.sep, "t", "vb17")
DST = os.path.join(HERE, "bateria_pre_selo", "vb17_evidencia")
sha = lambda b: hashlib.sha256(b).hexdigest()
if not os.path.isdir(VB):
    print("C:\\t\\vb17 nao existe (nada a fazer)"); sys.exit(0)
assert os.path.normcase(os.path.abspath(VB)) == os.path.normcase(os.path.join("C:" + os.sep, "t", "vb17")), VB
man = {}
for raiz, _, fs in os.walk(VB):
    for f in fs:
        p = os.path.join(raiz, f); rel = os.path.relpath(p, VB).replace(os.sep, "/")
        b = open(p, "rb").read(); d = os.path.join(DST, *rel.split("/")); os.makedirs(os.path.dirname(d), exist_ok=True)
        if os.path.exists(d):
            assert open(d, "rb").read() == b, ("a evidencia ja existe e DIFERE: nao sobrescrevo", d)
        else:
            open(d + ".tmp", "wb").write(b); os.replace(d + ".tmp", d)
        assert open(d, "rb").read() == b
        man[rel] = {"bytes": len(b), "sha256": sha(b)}
json.dump({"contrato": "VB17_EVIDENCIA_v400", "origem": VB, "copia": DST, "arquivos": man, "nota": "copia de bytes feita ANTES de apagar C:\\t\\vb17 (o sandbox curto da preparacao da v400)"}, open(os.path.join(HERE, "bateria_pre_selo", "VB17_EVIDENCIA_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
shutil.rmtree(VB)
assert not os.path.exists(VB)
print("evidencia guardada (%d arquivos) em %s; C:\\t\\vb17 apagado" % (len(man), DST))
