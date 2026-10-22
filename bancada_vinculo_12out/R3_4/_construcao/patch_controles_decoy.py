# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
from pathlib import Path
AQUI = Path(__file__).resolve().parent
P = AQUI.parent / "controles_negativos_r3_4.py"
t = P.read_text(encoding="utf-8")
bloco = (AQUI / "bloco_decoy_salto.py.txt").read_text(encoding="utf-8")
ancora = "# ================================================================ R3.4 (P): a bateria por versao\n"
assert t.count(ancora) == 1, t.count(ancora)
assert "R34_S_decoy_pre_selo_salto_na_producao" not in t
t = t.replace(ancora, bloco + "\n" + ancora)
P.write_text(t, encoding="utf-8", newline="")
print("ok")
