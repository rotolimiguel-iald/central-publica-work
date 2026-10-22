# -*- coding: utf-8 -*-
"""Apaga o toolchain Lean COPIADO para o sandbox da rodada 2 (prefixo \\\\?\\ para caminhos longos) e confere que
não sobrou .lake nem cache copiado na pasta da rodada 2. Grava um recibo.
Uso: python -I limpar_toolchain.py <recibo.json>
"""
import json
import os
import shutil
import sys
import time

R2 = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\3_KERNEL\rodada_2"
ALVO = os.path.join(R2, "sandbox", "toolchain")
LONG = "\\\\?\\"


def tamanho(p):
    n = b = 0
    for dp, _dn, fn in os.walk(LONG + p):
        for f in fn:
            n += 1
            b += os.stat(os.path.join(dp, f)).st_size
    return n, b


def main(recibo):
    if not os.path.abspath(ALVO).startswith(R2):
        raise SystemExit("RECUSA: alvo fora da rodada 2")
    existia = os.path.isdir(ALVO)
    n, b = tamanho(ALVO) if existia else (0, 0)
    t0 = time.time()
    if existia:
        shutil.rmtree(LONG + ALVO)
    sobras = []
    for dp, dn, fn in os.walk(LONG + R2):
        for d in dn:
            if d in (".lake", "toolchain", "build") or d.startswith("leanprover"):
                sobras.append(os.path.join(dp, d)[len(LONG):])
        for f in fn:
            if f.endswith((".ilean", ".trace", ".hash", ".c")):
                sobras.append(os.path.join(dp, f)[len(LONG):])
    rec = {"alvo": ALVO, "existia": existia, "arquivos_apagados": n, "bytes_apagados": b,
           "segundos": round(time.time() - t0, 1), "toolchain_existe_depois": os.path.isdir(ALVO),
           "sobras_de_lake_ou_cache": sobras, "feito_em": time.strftime("%Y-%m-%d %H:%M:%S")}
    with open(recibo, "w", encoding="utf-8") as fo:
        json.dump(rec, fo, ensure_ascii=False, indent=1)
    print(json.dumps(rec, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
