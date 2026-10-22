# -*- coding: utf-8 -*-
"""Lista (para excluir_do_preparo.py) os arquivos de um preparo cujo nome é RESERVADO no Windows — CON, PRN, AUX, NUL, COM1–9, LPT1–9, com
qualquer extensão (22/10/2026: «com1.events.jsonl», fixture de um teste de nomes, travou o git do work). Grava varredura_reservados_<preparo>.txt."""
import os, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RES = re.compile(r"(?i)^(con|prn|aux|nul|com[0-9¹²³]|lpt[0-9¹²³]|conin\$|conout\$)(\..*)?$")   # (COM0/LPT0 e sobrescritos também, 22/10)
for base in sys.argv[1:]:
    D = Path(base)
    raiz = "\\\\?\\" + str(D.resolve())
    achados = []
    for dp, dns, fns in os.walk(raiz):
        dns[:] = [x for x in dns if x != ".git"]
        for f in fns:
            if RES.match(f):
                achados.append(os.path.relpath(os.path.join(dp, f), raiz).replace(os.sep, "/"))
    out = Path(__file__).with_name("varredura_reservados_%s.txt" % D.name)
    out.write_text("\n".join(achados) + ("\n" if achados else ""), encoding="utf-8")
    print("%s: %d arquivos com nome reservado %s" % (D.name, len(achados), achados[:6]))
