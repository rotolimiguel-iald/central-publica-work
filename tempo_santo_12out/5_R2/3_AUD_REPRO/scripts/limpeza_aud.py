# -*- coding: utf-8 -*-
"""Apaga o toolchain copiado para o sandbox do auditor (prefixo de caminho longo) e grava o recibo de limpeza.
Uso: python -I -X utf8 limpeza_aud.py <saida.json>"""
import datetime
import json
import os
import shutil
import stat
import sys

A = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\5_R2\3_AUD_REPRO"
TC = os.path.join(A, "sandbox", "toolchain")
LONG = "\\\\?\\"  # \\?\


def onerr(func, path, exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)


n_antes = sum(len(f) for _, _, f in os.walk(LONG + TC))
shutil.rmtree(LONG + TC, onerror=onerr)
rest = sorted(os.listdir(os.path.join(A, "sandbox")))
out = {"apagado": TC, "prefixo_usado": LONG, "arquivos_antes": n_antes, "existe_depois": os.path.exists(LONG + TC),
       "lake_no_sandbox": os.path.exists(os.path.join(A, "sandbox", ".lake")),
       "caches_no_sandbox": [p for p in rest if p.startswith(".") or p.endswith(".cache")], "restam_no_sandbox": rest,
       "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "nota": ("toolchain v4.31.0 copiado do elan para o sandbox do auditor apagado ao final com o prefixo de caminho longo; "
                "LEAN_PATH so-leitura no .lake do Nos e, uma vez, no 3_KERNEL/sandbox (.olean da R1, so leitura); -o so para o "
                "sandbox do auditor. O elan, o Nos, a R1 e as pastas 0_ADENDO/1_PEDRA/2_REENSAIO nao foram tocados.")}
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
