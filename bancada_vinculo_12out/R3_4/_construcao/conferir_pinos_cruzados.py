# -*- coding: utf-8 -*-
"""conferir_pinos_cruzados.py (R3.4, 19/10/2026) -- SO LEITURA, nao grava nada: (1) PINOS_R3_4.json: todo entregavel e todo insumo medido ainda tem o sha256 e o tamanho que o arquivo tem agora;
(2) PINOS_BN_v394.R3_4.json: todo par {path, sha256} citado (esboco, bateria, pino do um.py, driver, cadeia, recibo pre_selo, pino do recibo, recibo do kernel R3_4, os originais da pasta v394 viva)
ainda confere com o disco. Imprime o resumo e sai com 2 se algo diverge.
uso: python -I -B -X utf8 conferir_pinos_cruzados.py"""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def pares(o, caminho="$"):
    """todo dict que traz path e sha256 (e, se houver, bytes)."""
    if isinstance(o, dict):
        if isinstance(o.get("path"), str) and isinstance(o.get("sha256"), str) and len(o["sha256"]) == 64:
            yield caminho, o
        for k, v in o.items():
            yield from pares(v, caminho + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from pares(v, "%s[%d]" % (caminho, i))


def conferir(arq):
    d = json.loads((AQUI / arq).read_bytes())
    ok, ruins, ausentes = 0, [], []
    for onde, o in pares(d):
        p = Path(o["path"])
        if not p.is_absolute():
            p = AQUI / p
        if not p.is_file():
            ausentes.append((onde, str(p)))
            continue
        bate = sha(p) == o["sha256"] and ("bytes" not in o or p.stat().st_size == o["bytes"])
        if bate:
            ok += 1
        else:
            ruins.append((onde, str(p)))
    return dict(arquivo=arq, conferem=ok, divergem=ruins, ausentes=ausentes)


def conferir_copias():
    """PINO_RECIBO_PRE_SELO_v394_R3_4.json: copias_das_evidencias {nome: sha256} confere com recibo_pre_selo_v394/<nome>."""
    d = json.loads((AQUI / "PINO_RECIBO_PRE_SELO_v394_R3_4.json").read_bytes())
    ok, ruins = 0, []
    for nome, h in d["copias_das_evidencias"].items():
        p = AQUI / "recibo_pre_selo_v394" / nome.replace("\\", "/")
        if p.is_file() and sha(p) == h:
            ok += 1
        else:
            ruins.append(nome)
    return dict(arquivo="PINO_RECIBO_PRE_SELO_v394_R3_4.json#copias_das_evidencias", conferem=ok, divergem=ruins, ausentes=[])


r = [conferir("PINOS_R3_4.json"), conferir("PINOS_BN_v394.R3_4.json"), conferir("PINO_RECIBO_PRE_SELO_v394_R3_4.json"), conferir_copias()]
# a unica divergencia ESPERADA: adendo_de_pino_do_t12.antes traz o caminho do Nos real com o sha do pino ANTIGO (v391) do pre-registro congelado, de proposito
esperadas = {("PINO_RECIBO_PRE_SELO_v394_R3_4.json", "$.adendo_de_pino_do_t12.antes")}
inesperadas = [(x["arquivo"], d_[0]) for x in r for d_ in x["divergem"] if (x["arquivo"], d_[0] if isinstance(d_, (list, tuple)) else d_) not in esperadas]
print(json.dumps(r, ensure_ascii=False, indent=1))
print(json.dumps(dict(divergencias_inesperadas=inesperadas), ensure_ascii=False))
sys.exit(0 if not inesperadas and all(not x["ausentes"] for x in r) else 2)
