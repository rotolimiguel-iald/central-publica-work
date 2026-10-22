# Reconstroi C:/t/k392/final (os 16 arquivos do kernel que o gerador le) a partir do candidato anterior (1fa00d79), cujo
# ensaio a seco ja provou byte a byte == sandbox. Confere contra os sha da tentativa1 (TGLExt.lean, Audit.lean) e os pinos das pedras.
import os, sys, json, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(WK, "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar
import v392_pedras as P
EMB, _, _, h16 = carregar(os.path.join(HERE, "um_v392_candidato_1fa00d79.anterior.py"))
assert h16 == "1fa00d79696c3d2e", h16
KB = os.path.join("C:" + os.sep, "t", "k392", "final")
T1 = os.path.join(HERE, "tentativa1_rito_falhou_20261013_160045")
rels = ["TGLExt.lean", "TGL/Audit.lean"] + ["TGLExt/%s.lean" % s["mod"] for s in P.STONES]
for rel in rels:
    p = os.path.join(KB, *rel.split("/")); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write(EMB[rel].encode("utf-8"))
sh = lambda b: hashlib.sha256(b).hexdigest()
assert sh(open(os.path.join(KB, "TGLExt.lean"), "rb").read()) == sh(open(os.path.join(T1, "tgl_kernel__TGLExt.lean"), "rb").read())
assert sh(open(os.path.join(KB, "TGL", "Audit.lean"), "rb").read()) == sh(open(os.path.join(T1, "tgl_kernel__TGL__Audit.lean"), "rb").read())
print("ok", len(rels), "arquivos em", KB)
