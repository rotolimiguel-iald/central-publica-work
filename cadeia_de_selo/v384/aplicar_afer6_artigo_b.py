# -*- coding: utf-8 -*-
"""Conserto do aplicar_afer6_artigo: o parentese de abertura que faltava na ramificacao «sem registro / ausente» (PT e EN)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
for fn, old, new in (("artigo_pt_v384.pysnip", '+ (((r"Não há registro da comparação', '+ ((((r"Não há registro da comparação'),
                     ("artigo_en_v384.pysnip", '+ (((r"There is no record of the CPU comparison', '+ ((((r"There is no record of the CPU comparison')):
    p = os.path.join(HERE, fn); s = open(p, "rb").read().decode("utf-8")
    assert s.count(old) == 1, (fn, s.count(old))
    s = s.replace(old, new); b = s.encode("utf-8")
    open(p + ".tmp", "wb").write(b); os.replace(p + ".tmp", p); print("ok", fn)
