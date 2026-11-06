# -*- coding: utf-8 -*-
"""_pos_build_dur_fix_v409.py -- (claude-construtor-v409) corrige a MINHA troca anterior (_pos_build_audit_refeito_v409.py): o comentario entrou no meio da linha e engoliu `dur_build = ...` (NameError, fail-closed). A causa e' minha; o teste nao muda."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("pos_build_kernel_v409.py")
a.troca('''    dur_audit = mm_["epoch_audit_fim"] - mm_.get("epoch_audit_inicio", mm_["epoch_build_fim"]);   # (v409: o Audit refeito depois da queda de energia mede a propria rodada) dur_build = mm_["epoch_build_fim"] - mm_["epoch_inicio"]''',
        '''    dur_audit = mm_["epoch_audit_fim"] - mm_.get("epoch_audit_inicio", mm_["epoch_build_fim"]); dur_build = mm_["epoch_build_fim"] - mm_["epoch_inicio"]   # (v409: o Audit refeito depois da queda de energia mede a propria rodada)''')
a.grava()
