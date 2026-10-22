# -*- coding: utf-8 -*-
"""preparar_kernel_k394d.py -- DELTA 19/10 da v394: prepara o SANDBOX C:\\t\\k394d (copia de C:\\t\\k394\\final, feita por robocopy SEM /PURGE).
Escreve SO' em C:\\t\\k394d e em delta_19out. NUNCA toca C:\\t\\k394, o Nos, o candidato em exame, a Bancada nem o tunel.
 1. instala a pedra TGLExt/TheBinaryReadingAtTheFixedPoint.lean (copia de BYTES de delta_19out);
 2. acrescenta o import da pedra na raiz TGLExt.lean (depois de um separador em branco, como o Codex fez) e no topo de TGL/Audit.lean (como o Codex fez);
 3. guarda os bytes ANTERIORES da raiz e do Audit em delta_19out\\backup_k394d_pre (regra do backup imediato).
uso: python -I -B -X utf8 preparar_kernel_k394d.py"""
import hashlib, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
C = "C:" + os.sep
SB = os.path.join(C, "t", "k394d"); BASE = os.path.join(C, "t", "k394", "final")
sha = lambda b: hashlib.sha256(b).hexdigest()
IMPORT = "import TGLExt.TheBinaryReadingAtTheFixedPoint"
assert os.path.isdir(SB) and os.path.isdir(BASE), "sandbox ausente"
assert os.path.normcase(os.path.abspath(SB)) != os.path.normcase(os.path.abspath(BASE))
stone_src = os.path.join(HERE, "TheBinaryReadingAtTheFixedPoint.lean")
stone_dst = os.path.join(SB, "TGLExt", "TheBinaryReadingAtTheFixedPoint.lean")
bs = open(stone_src, "rb").read()
open(stone_dst + ".tmp", "wb").write(bs); assert os.path.getsize(stone_dst + ".tmp") == len(bs); os.replace(stone_dst + ".tmp", stone_dst)
assert open(stone_dst, "rb").read() == bs
BK = os.path.join(HERE, "backup_k394d_pre"); os.makedirs(BK, exist_ok=True)
rep = {"pedra_sha16": sha(bs)[:16]}
for rel in ("TGLExt.lean", "TGL/Audit.lean"):
    p = os.path.join(SB, *rel.split("/"))
    old = open(p, "rb").read().decode("utf-8")
    if IMPORT in old:
        rep[rel] = "ja' tinha o import (nao reescrito); a copia de bytes de antes do delta esta em backup_k394d_pre"
        continue
    pb = os.path.join(BASE, *rel.split("/"))
    assert open(pb, "rb").read().decode("utf-8") == old, ("o sandbox k394d difere do k394\\final antes do delta: " + rel)
    bk = os.path.join(BK, rel.replace("/", "__") + ".pre_delta19")
    if not os.path.exists(bk):
        open(bk, "wb").write(old.encode("utf-8"))
    if rel == "TGLExt.lean":
        assert old.endswith("\n") and old.rstrip("\n").endswith("import TGLExt.F1Fecho394.NetworkProofAuditR8"), "fim inesperado da raiz"
        new = old + "\n" + IMPORT + "\n"
    else:
        assert old.startswith("import TGLExt.F1Fecho394.NetworkProofAuditR8\n"), "inicio inesperado do Audit"
        new = IMPORT + "\n\n" + old
    nb = new.encode("utf-8")
    open(p + ".tmp", "wb").write(nb); assert os.path.getsize(p + ".tmp") == len(nb) > len(old.encode("utf-8")); os.replace(p + ".tmp", p)
    rep[rel] = {"sha16_antes": sha(old.encode("utf-8"))[:16], "sha16_depois": sha(nb)[:16], "bytes_antes": len(old.encode("utf-8")), "bytes_depois": len(nb)}
print(rep)
