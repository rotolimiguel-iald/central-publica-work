# -*- coding: utf-8 -*-
"""_pos_build_audit_refeito_v409.py -- (claude-construtor-v409, 05/11/2026) a queda de energia de ~17:10 cortou o Audit; ele e' refeito sozinho (o build terminou com rc 0). A duracao do Audit passa a ser a
MEDIDA da propria rodada do Audit quando as marcas trazem epoch_audit_inicio (antes era fim do Audit menos fim do build, que incluiria a queda)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("pos_build_kernel_v409.py")
a.troca('''    dur_audit = mm_["epoch_audit_fim"] - mm_["epoch_build_fim"];''', '''    dur_audit = mm_["epoch_audit_fim"] - mm_.get("epoch_audit_inicio", mm_["epoch_build_fim"]);   # (v409: o Audit refeito depois da queda de energia mede a propria rodada)''')
a.grava()
