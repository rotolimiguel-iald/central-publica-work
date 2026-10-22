# -*- coding: utf-8 -*-
"""patch de construcao (R3.4, parte 3): insere em ../controles_negativos_r3_4.py o bloco bloco_novos_r3_4.py.txt (os controles novos S, P e M) antes do run 2."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path

AQUI = Path(__file__).resolve().parent
P = AQUI.parent / "controles_negativos_r3_4.py"
t = P.read_text(encoding="utf-8")
bloco = (AQUI / "bloco_novos_r3_4.py.txt").read_text(encoding="utf-8")
ancora = "# ================================================================ run 2: o elo B3 na copia b2, com TUDO pinado e encadeado\n"
assert t.count(ancora) == 1, t.count(ancora)
assert "R34_S_pre_selo_salto_aceito" not in t, "o bloco ja foi inserido"
t = t.replace(ancora, bloco + "\n" + ancora)
P.write_text(t, encoding="utf-8", newline="")
print("ok", len(bloco))
