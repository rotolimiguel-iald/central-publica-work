# -*- coding: utf-8 -*-
"""D197: as cópias INSTALADAS da pedra genérica e da camada dos 16 recebem os MESMOS bytes da fonte da G1 (13/11/2026, claude-site-custodia).
Antes de copiar, confere que cada cópia instalada é igual ao backup .bak_<SUF>_d197 da fonte (a instalação estava em dia com a fonte
antiga): se não estiver, PARA. Backup de bytes; temporário; conferência byte a byte depois. Uso: python -X utf8 <este> <SUF>"""
import os, sys, time
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
SUF = sys.argv[1]
STAMP = time.strftime("%Y%m%d_%H%M%S")
PARES = [(CEN / "tools" / "custodia_g1" / "generico" / "custodia_generica.py", CEN / "fronteira_tgl" / "runner" / "custodia_generica.py"),
         (CEN / "tools" / "custodia_g1" / "generico" / "camada_generica.py", CEN / "patents" / "_formula_completa" / "camada_generica.py")]
for fonte, inst in PARES:
    antes = Path(str(fonte) + ".bak_%s_d197" % SUF).read_bytes()
    atual = inst.read_bytes()
    assert atual == antes, "a cópia instalada %s não é a fonte antiga - PARAR" % inst
    bak = inst.with_name(inst.name + ".bak_%s_d197" % STAMP)
    bak.write_bytes(atual)
    assert bak.read_bytes() == atual
    novo = fonte.read_bytes()
    t = inst.with_name(inst.name + ".tmp_d197")
    t.write_bytes(novo)
    assert t.read_bytes() == novo
    os.replace(t, inst)
    assert inst.read_bytes() == fonte.read_bytes()
    print("ok: %s = fonte (%d B) | backup %s" % (inst, len(novo), bak.name))
