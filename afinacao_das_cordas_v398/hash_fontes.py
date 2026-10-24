# -*- coding: utf-8 -*-
"""hash_fontes.py -- le (so leitura) os arquivos citados e imprime sha256/sha16/bytes; confere Nos x sandbox k398b para os modulos do kernel.
Nada de hash de memoria. Uso: python -I -B -X utf8 hash_fontes.py
"""
import hashlib
import json
import os

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt"
SB = r"C:\t\k398b\TGLExt"
KERNEL = ["O16/PolarMinimalPeriod_v2.lean", "Palavra.lean", "TheStation.lean", "Fundacao.lean", "O16/PeriodHeatCalibration_v3.lean"]
OUTROS = {
    "operador_verbatim": r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_23out_cordas_10_dimensoes_fechar_a_face_tetelestai_verbatim.txt",
    "ultima_corda_tex": r"C:\IALD\Artigo\the_boundary\Genesis da Unificação\Artigos_fundadores\A_ultima_corda_v3.tex",
    "mathlib_HurwitzZetaValues": r"C:\t\k398b\.lake\packages\mathlib\Mathlib\NumberTheory\LSeries\HurwitzZetaValues.lean",
    "lake_manifest": r"C:\t\k398b\lake-manifest.json",
}


def h(p):
    b = open(p, "rb").read()
    x = hashlib.sha256(b).hexdigest()
    return {"caminho": p, "sha256": x, "sha16": x[:16], "bytes": len(b)}


R = {"kernel": {}, "outros": {}}
for k in KERNEL:
    a = h(os.path.join(NOS, *k.split("/")))
    b = h(os.path.join(SB, *k.split("/")))
    R["kernel"][k] = {"nos": a, "sandbox": b, "iguais": a["sha256"] == b["sha256"]}
for k, p in OUTROS.items():
    R["outros"][k] = h(p)
print(json.dumps(R, ensure_ascii=False, indent=1))
