# -*- coding: utf-8 -*-
"""_r5ag_09b_artigos_beta_v410.py -- R5: o gerador recusa o beta em Unicode no fonte do snippet do artigo (licao da v408: so' em LaTeX); o _mz410 grava os simbolos por escape (barra, u, quatro hex); o resultado e' o mesmo.
(Nota: a ferramenta Write decodifica barra-u de UM so' nivel; aqui as escapes vao com DUAS barras no fonte deste script.)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar
OLD = '''(("|T|²", r"$|T|^2$"), ("|R|²", r"$|R|^2$"), ("α²", r"$\\alpha^2$"), ("√(b/(1 − b))", r"$\\sqrt{b/(1-b)}$"), ("−", "$-$"), ("≥", r"$\\ge$"), ("≤", r"$\\le$"), ("·", r"$\\cdot$"), ("β", r"$\\beta$"), ("½", r"$\\tfrac12$"), ("<", "$<$"), (">", "$>$"))'''
NEW = '''(("|T|\\u00b2", r"$|T|^2$"), ("|R|\\u00b2", r"$|R|^2$"), ("\\u03b1\\u00b2", r"$\\alpha^2$"), ("\\u221a(b/(1 \\u2212 b))", r"$\\sqrt{b/(1-b)}$"), ("\\u2212", "$-$"), ("\\u2265", r"$\\ge$"), ("\\u2264", r"$\\le$"), ("\\u00b7", r"$\\cdot$"), ("\\u03b2", r"$\\beta$"), ("\\u00bd", r"$\\tfrac12$"), ("<", "$<$"), (">", "$>$"))'''
for f in ("artigo_pt_aescala_v410.pysnip", "artigo_en_aescala_v410.pysnip"):
    aplicar(f, [(OLD, NEW, 1)], parse=False)
