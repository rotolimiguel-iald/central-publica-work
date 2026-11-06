# -*- coding: utf-8 -*-
"""_adapt_deposito_atualiza_v409.py -- (claude-construtor-v409, 05/11/2026 ~19h40) a preparacao foi REFEITA depois da revisao dos insumos pela gerencia (citacoes e estatuto dos nomes): o deposito novo na fila
diz que SUBSTITUI o anterior (o PRONTA anterior, lido do marcador .DEPOSITADO_CONSTRUTOR_<sha16>), e a rota cadeia.preparacao_v409, que ja' existe no Mapa (o rotas.py recusa ROTA repetida), recebe um RESULTADO
com o mesmo rota_id (correcao ao lado, nada reescrito). Os textos seguem montados dos arquivos."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("depositar_construtor_v409.py")
a.troca('''rota = [{"tipo": "ROTA", "rota_id": "cadeia.preparacao_v409",''',
        '''_ANT = sorted(n_[len(".DEPOSITADO_CONSTRUTOR_"):] for n_ in os.listdir(HERE) if n_.startswith(".DEPOSITADO_CONSTRUTOR_") and n_ != os.path.basename(MARCA))   # os PRONTA anteriores ja' depositados (lidos dos marcadores)
_JA = any(('"rota_id": "cadeia.preparacao_v409"' in l_ and '"tipo": "ROTA"' in l_) for l_ in open(os.path.join(os.path.dirname(ROTAS), "rotas.jsonl"), encoding="utf-8"))   # a ROTA ja' existe? (so' leitura do livro)
rota = [{"tipo": "RESULTADO" if _JA else "ROTA", "rota_id": "cadeia.preparacao_v409",''')
a.troca('''         "nota": "agente de preparacao claude-construtor-v409; quem constroi nao aprova (revisor: Sonnet, D58)"}]''',
        '''         "nota": "agente de preparacao claude-construtor-v409; quem constroi nao aprova (revisor: Sonnet, D58)" + ("; REFEITA depois da revisao dos insumos pela gerencia c1 (05/11 ~19h30: citacoes verbatim; os nomes acrescentados na R9 e os da ParNaFaceDeFock [DECLARADO] ate a ratificacao): este PRONTA (%s) substitui o(s) anterior(es) %s" % (S, ", ".join(_ANT)) if _ANT else "")}]''')
a.troca('''txt = ("v409 (A traducao as classes de Turing e o par na face de Fock) preparada em 05/11/2026''',
        '''_ANT0 = sorted(n_[len(".DEPOSITADO_CONSTRUTOR_"):] for n_ in os.listdir(HERE) if n_.startswith(".DEPOSITADO_CONSTRUTOR_") and n_ != os.path.basename(MARCA))   # os PRONTA anteriores ja' depositados
_PREFIXO_SUBST = ("SUBSTITUI o deposito do PRONTA anterior (%s): a preparacao foi refeita depois da revisao dos insumos pela gerencia c1 (05/11 ~19h30: citacoes verbatim; o estatuto dos nomes). " % ", ".join(_ANT0)) if _ANT0 else ""
txt = (_PREFIXO_SUBST + "v409 (A traducao as classes de Turing e o par na face de Fock) preparada em 05/11/2026''')
a.grava()
