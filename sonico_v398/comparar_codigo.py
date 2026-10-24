# -*- coding: utf-8 -*-
"""comparar_codigo.py -- prova que a versao nova de Sonico.lean difere da REVISADA so em COMENTARIOS (docstrings): o codigo fora de /- ... -/ e de `--` e'
byte a byte o mesmo (imports, set_option, enunciados, provas, #print axioms). So leitura; grava conferencia_codigo_identico.json.
Uso: python -I -B -X utf8 comparar_codigo.py [sha16_da_versao_revisada]   (padrao: 1338622344dd80c7, a revisada em EXAME_SONICO.md)
"""
import glob
import hashlib
import json
import os
import re
import sys

W = r"C:\IALD\Central de Patentes\work\sonico_v398"
REVISADA16 = sys.argv[1] if len(sys.argv) > 1 else "1338622344dd80c7"
NOVA = os.path.join(W, "Sonico.lean")


def sem_comentarios(t):
    t = re.sub(r"/-.*?-/", "", t, flags=re.S)          # blocos (/-! ... -/ e /-- ... -/); sem aninhamento neste arquivo (conferido: /- e -/ em igual numero)
    t = re.sub(r"--[^\n]*", "", t)
    return t


def sha16(b):
    return hashlib.sha256(b).hexdigest()[:16]


antiga = None
for p in sorted(glob.glob(os.path.join(W, "Sonico.lean.bak_*"))):
    b = open(p, "rb").read()
    if sha16(b) == REVISADA16:
        antiga = (p, b)
        break
assert antiga, f"nenhum backup com sha16 {REVISADA16}"
nova_b = open(NOVA, "rb").read()
ta, tn = antiga[1].decode("utf-8"), nova_b.decode("utf-8")
ca, cn = sem_comentarios(ta), sem_comentarios(tn)
R = {
    "revisada": {"arquivo": antiga[0], "sha16": sha16(antiga[1]), "bytes": len(antiga[1])},
    "nova": {"arquivo": NOVA, "sha16": sha16(nova_b), "bytes": len(nova_b)},
    "blocos_de_comentario": {"revisada": ta.count("/-"), "nova": tn.count("/-")},
    "codigo_fora_dos_comentarios": {"revisada_sha16": sha16(ca.encode("utf-8")), "nova_sha16": sha16(cn.encode("utf-8")), "bytes_revisada": len(ca.encode("utf-8")), "bytes_nova": len(cn.encode("utf-8"))},
    "codigo_identico_byte_a_byte": ca == cn,
    "linhas_de_codigo_nao_vazias": sum(1 for l in cn.split("\n") if l.strip()),
}
json.dump(R, open(os.path.join(W, "conferencia_codigo_identico.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
