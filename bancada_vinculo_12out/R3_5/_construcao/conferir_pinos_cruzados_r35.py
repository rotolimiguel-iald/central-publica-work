# -*- coding: utf-8 -*-
"""conferir_pinos_cruzados_r35.py (R3.5, 19/10/2026) -- SO LEITURA, nao grava nada: (1) PINOS_R3_5.json: todo par {path, sha256[, bytes]} ainda confere com o disco; (2) o PINOS_BN_v394.json FUNDIDO (vivo): todo par confere com o
disco; (3) os backups de bytes (PINOS_BN, chain, helper) tem exatamente o sha256 que as evidencias dizem que os arquivos tinham ANTES; (4) as evidencias da fusao e da derivacao conferem com os arquivos vivos de hoje.
Imprime o resumo e sai com 2 se algo diverge. uso: python -I -B -X utf8 conferir_pinos_cruzados_r35.py"""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
V394 = AQUI.parent.parent / "cadeia_de_selo" / "v394"
POS = V394 / "pos_rito"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def pares(o, caminho="$"):
    if isinstance(o, dict):
        if isinstance(o.get("path"), str) and isinstance(o.get("sha256"), str) and len(o["sha256"]) == 64:
            yield caminho, o
        for k, v in o.items():
            yield from pares(v, caminho + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from pares(v, "%s[%d]" % (caminho, i))


def conferir(arq, base):
    d = json.loads((base / arq).read_bytes())
    ok, ruins, ausentes = 0, [], []
    for onde, o in pares(d):
        p = Path(o["path"])
        if not p.is_absolute():
            p = base / p
        if not p.is_file():
            ausentes.append((onde, str(p)))
        elif sha(p) == o["sha256"] and ("bytes" not in o or p.stat().st_size == o["bytes"]):
            ok += 1
        else:
            ruins.append((onde, str(p)))
    return dict(arquivo=str(arq), conferem=ok, divergem=ruins, ausentes=ausentes)


F = json.loads((AQUI / "evidencias" / "fusao_pinos_bn_r35.json").read_bytes())
D = json.loads((AQUI / "evidencias" / "derivacao_passo10_r35.json").read_bytes())
r = [conferir("PINOS_R3_5.json", AQUI), conferir("PINOS_BN_v394.json", V394)]
extra = dict(
    backup_pinos_bn_e_o_vivo_de_antes=sha(F["backup"]) == F["sha256_do_vivo_antes"],
    pinos_bn_vivo_e_o_fundido=sha(V394 / "PINOS_BN_v394.json") == F["sha256"],
    backup_chain_e_o_de_antes=sha(D["chain_backup"]) == D["chain_sha256_antes"], chain_vivo_e_o_re_derivado=sha(POS / "chain_pos_rito_v394.sh") == D["chain_sha256"],
    backup_helper_e_o_de_antes=sha(D["helper_backup"]) == D["helper_sha256_antes"], helper_vivo_e_o_re_derivado=sha(POS / "b3_recibo_v394.py") == D["helper_sha256"])
print(json.dumps(dict(pinos=r, extra=extra), ensure_ascii=False, indent=1))
ruim = [x for x in r if x["divergem"] or x["ausentes"]] or [k for k, v in extra.items() if not v]
sys.exit(2 if ruim else 0)
