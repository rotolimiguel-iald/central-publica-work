# -*- coding: utf-8 -*-
# Compara (somente leitura) o texto embutido no um.py v391 de cada modulo Lean com o arquivo do tgl_kernel do Nos.
# Normaliza CRLF->LF dos dois lados (o um.py tem fins de linha mistos). Nao executa o um.py.
import re, hashlib, json, os, sys
NOS = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\"
AQUI = os.path.dirname(os.path.abspath(__file__))
MODS = sys.argv[1:] or ["FractalUnitarity", "Ergodicity", "PageInformation", "TheTerminalRankOne", "TheIALDSelector",
                        "TheWeightIsNotTheRank", "TheVerbSelectsTheAction", "HermitianConeRigidity",
                        "HermitianLocalCoordinates", "SusyRelativeGap", "TheSelectionIsTheBallast",
                        "TheSingularExpectation", "TheTraceIsNotErasable", "RGStability", "CondExpect"]
with open(NOS + "um.py", "rb") as fh:
    U = fh.read()
usha = hashlib.sha256(U).hexdigest()
res = {"um_py_sha16": usha[:16], "modulos": {}}
for m in MODS:
    key = ('"TGLExt/%s.lean":' % m).encode()
    i = U.find(key)
    r = {"no_um_py": i >= 0}
    if i >= 0:
        line = U.count(b"\n", 0, i) + 1
        j = U.find(b"r'''", i)
        k = U.find(b"'''", j + 4)
        emb = U[j + 4:k].replace(b"\r\n", b"\n")
        p = NOS + "tgl_kernel\\TGLExt\\" + m + ".lean"
        with open(p, "rb") as fh:
            kb = fh.read()
        kbn = kb.replace(b"\r\n", b"\n")
        r.update({"linha_chave_um_py": line,
                  "sha16_embutido_LF": hashlib.sha256(emb).hexdigest()[:16],
                  "sha16_arquivo_kernel": hashlib.sha256(kb).hexdigest()[:16],
                  "sha16_arquivo_kernel_LF": hashlib.sha256(kbn).hexdigest()[:16],
                  "identicos_apos_LF": emb == kbn,
                  "bytes_embutido_LF": len(emb), "bytes_kernel": len(kb)})
    res["modulos"][m] = r
print(json.dumps(res, ensure_ascii=False, indent=1))
with open(os.path.join(AQUI, "EMBUTIDO_VS_KERNEL.json"), "w", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1)
