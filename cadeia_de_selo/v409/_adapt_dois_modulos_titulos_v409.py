# -*- coding: utf-8 -*-
"""_adapt_dois_modulos_titulos_v409.py -- (claude-construtor-v409) os titulos do PLANO e do RELATORIO dizem as duas pedras (a traducao as classes de Turing e o par na face de Fock)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("gerar_relatorio_v409.py")
a.troca('PLANO = f"""# PLANO da v409 — A tradução às classes de Turing (preparação)', 'PLANO = f"""# PLANO da v409 — A tradução às classes de Turing e o par na face de Fock (preparação)')
a.troca('RELATORIO = f"""# RELATÓRIO DA PREPARAÇÃO DA v409 — A tradução às classes de Turing', 'RELATORIO = f"""# RELATÓRIO DA PREPARAÇÃO DA v409 — A tradução às classes de Turing e o par na face de Fock')
a.grava()
