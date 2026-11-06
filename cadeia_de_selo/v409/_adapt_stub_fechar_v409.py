# -*- coding: utf-8 -*-
"""_adapt_stub_fechar_v409.py -- (claude-construtor-v409, 05/11/2026) o harness do fechar (pos_rito/harness_fechar_sandbox_v409.py, etapa 2d) monta uma leitura STUB com a V minima que o fechar_v409.py usa;
a subida mecanica de rotulo da v408 deixou de fora as chaves da v407 HERDADA que o fechar_v409.py indexa direto (V["reg407d"], V["fecho407"], V["ancoras407"], V["bundle407"], V["chaves407"]):
o fechar com stubs caia em KeyError('reg407d'). A causa (o stub incompleto) e' corrigida: as cinco chaves entram com o MESMO tipo de valor stub das irmas da v408/v406. O fechar e as conferencias do harness nao mudam."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("pos_rito/harness_fechar_sandbox_v409.py")
a.troca("'reg408d': {'cunhagens_v407': {'ok': True}}, ", "'reg408d': {'cunhagens_v407': {'ok': True}}, 'reg407d': {'cunhagens_v407': {'ok': True}}, ")
a.troca("'fecho408': {'ok': True}, ", "'fecho408': {'ok': True}, 'fecho407': {'ok': True}, ")
a.troca("'ancoras408': {}, ", "'ancoras408': {}, 'ancoras407': {}, ")
a.troca("'bundle408': {}, ", "'bundle408': {}, 'bundle407': {}, ")
a.troca("'chaves408': {}, ", "'chaves408': {}, 'chaves407': {}, ")
a.grava()
