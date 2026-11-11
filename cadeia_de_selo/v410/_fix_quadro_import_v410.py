# -*- coding: utf-8 -*-
"""_fix_quadro_import_v410.py -- (claude-construtor-v410, 06/11/2026) achado do fork A: quadro_v397.py (copia literal) ainda importava delta_v409; so' o import do delta muda, como em cada copia desde a v400."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v410 import aplicar
aplicar(os.path.join(os.path.dirname(os.path.abspath(__file__)), "quadro_v397.py"), [
    ("import delta_v409 as DL  # noqa: E402   # (v409, 05/11", "import delta_v410 as DL  # noqa: E402   # (v410, 06/11, claude-construtor-v410: so' o import do delta muda, como em cada copia desde a v400; achado do fork A) (v409, 05/11", 1)])
