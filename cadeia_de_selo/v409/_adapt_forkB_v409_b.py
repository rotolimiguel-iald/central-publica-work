# -*- coding: utf-8 -*-
"""_adapt_forkB_v409_b.py -- (claude-construtor-v409, fork B, 05/11/2026) segunda passada: dois textos que a primeira deixou com a contagem da v408 (instalar e reverter). Trocas de contagem exata; backup de bytes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("instalar_v409.py")
a.troca("(b) os 4 modulos novos da v409 (em TGLExt/, nao em F1Fecho394) NAO", "(b) o modulo novo da v409 (em TGLExt/, nao em F1Fecho394) NAO")
a.grava()
a = Arq("reverter_v409.py")
a.troca("(o bundle de quatro modulos em TGLExt/)", "(o bundle de um modulo em TGLExt/)")
a.grava()
