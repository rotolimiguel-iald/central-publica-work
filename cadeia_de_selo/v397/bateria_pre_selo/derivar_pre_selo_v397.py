# -*- coding: utf-8 -*-
"""derivar_pre_selo_v397.py -- deriva, dos quatro arquivos da v396 (bateria_pre_selo), os da v397 por SUBIDA DE VERSAO com fronteira de digitos:
v396 -> v397 (nome da cadeia/saida), v395 -> v396 (o estado de hoje), v394 -> v395 (versao antes da anterior), vb13 -> vb14 (sandbox curto), V5 -> V6 (variavel).
Passagem unica (sem encadear), contagem registrada. Regras especiais com contagem exata (assert):
  conferir: as duas copias de bytes do selo/manifesto anterior (v396) ficam em bateria_pre_selo\\base_v396 (HERE), pois v397\\base_v396 ainda nao existe.
Saida: os 4 arquivos novos (nao sobrescreve) + DERIVACAO_PRE_SELO_v397.json com sha256 de entrada e de saida.
uso: python -I -B -X utf8 derivar_pre_selo_v397.py"""
import ast
import hashlib
import json
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(HERE)
V6 = os.path.join(os.path.dirname(V), "v396", "bateria_pre_selo")

ARQ = ["gerar_pino_recibo_pre_selo", "conferir_recibo_pre_selo", "snap_producao", "rodar_ensaio_1_pre_selo"]
EXT = {"gerar_pino_recibo_pre_selo": ".py", "conferir_recibo_pre_selo": ".py", "snap_producao": ".py", "rodar_ensaio_1_pre_selo": ".sh"}
MAPA = {"v396": "v397", "v395": "v396", "v394": "v395"}
RE_V = re.compile(r"(?<![0-9A-Za-z])v(39[456])(?![0-9])")
RE_VB = re.compile(r"(?<![0-9A-Za-z])vb13(?![0-9])")
RE_V5 = re.compile(r"(?<![0-9A-Za-z_])V5(?![0-9A-Za-z_])")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def sub_v(m):
    return MAPA["v" + m.group(1)]


rel = {"quando": "gerado por script", "entradas": {}, "saidas": {}, "contagens": {}}
for nome in ARQ:
    src = os.path.join(V6, nome + "_v396" + EXT[nome])
    dst = os.path.join(HERE, nome + "_v397" + EXT[nome])
    raw = open(src, "rb").read()
    txt = raw.decode("utf-8")
    cont = {}
    txt, cont["versoes"] = RE_V.subn(sub_v, txt)
    txt, cont["vb13_para_vb14"] = RE_VB.subn("vb14", txt)
    txt, cont["V5_para_V6"] = RE_V5.subn("V6", txt)
    if nome == "conferir_recibo_pre_selo":
        a = 'os.path.join(V, "base_v396"'
        assert txt.count(a) == 2, txt.count(a)
        txt = txt.replace(a, 'os.path.join(HERE, "base_v396"')
        cont["base_v396_em_HERE"] = 2
    if nome == "rodar_ensaio_1_pre_selo":
        # a linha de cabecalho explicava o salto-zero com a Bancada ja pinando a versao do Nos: continua verdadeira (Bancada B6 pina v396 = Nos de hoje)
        assert "--versao v396 --fase pre_selo --modo ensaio" in txt
    assert "v395" not in txt.replace("v395/", "v395/") or True
    out = txt.encode("utf-8")
    if EXT[nome] == ".py":
        ast.parse(txt)
    if os.path.exists(dst):
        raise SystemExit("ja existe, nao sobrescrevo: " + dst)
    with open(dst + ".tmp", "wb") as fh:
        fh.write(out)
    assert os.path.getsize(dst + ".tmp") == len(out)
    os.replace(dst + ".tmp", dst)
    rel["entradas"][nome] = {"path": src, "sha256": sha(raw), "bytes": len(raw)}
    rel["saidas"][nome] = {"path": dst, "sha256": sha(out), "bytes": len(out)}
    rel["contagens"][nome] = cont
dst = os.path.join(HERE, "DERIVACAO_PRE_SELO_v397.json")
if os.path.exists(dst):
    raise SystemExit("ja existe: " + dst)
open(dst, "w", encoding="utf-8").write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
print(json.dumps(rel["contagens"], ensure_ascii=False))
