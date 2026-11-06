# -*- coding: utf-8 -*-
"""_adapt_dois_modulos_gerador2_v409.py -- (claude-construtor-v409) gerar_candidato_v409.py: a conferencia das copias duraveis contra a fonte passa da candidata R8 e do recibo dela (superados) as candidatas
das DUAS pedras (R9 da TraducaoTuring; R2 da ParNaFaceDeFock) e as saidas do lean delas, com as chaves do registros_v409 (CHAVE_CANDIDATA, CHAVE_SAIDA_CANDIDATA). A igualdade fica; so' os arquivos mudam."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("gerar_candidato_v409.py")
a.troca('''for ch_, arq_ in ((RG.CHAVE_BUNDLE, DL.BUNDLE_ARQ), (RG.CHAVE_CANDIDATA_R8, DL.CANDIDATA_R8_ARQ), (RG.CHAVE_RECIBO_R8, DL.RECIBO_R8_ARQ)):''',
        '''_SAIDA_CAND = {"TraducaoTuring": DL.SAIDA_CANDIDATA_TU_ARQ, "ParNaFaceDeFock": DL.SAIDA_CANDIDATA_PAR_ARQ}
for ch_, arq_ in [(RG.CHAVE_BUNDLE, DL.BUNDLE_ARQ)] + [(RG.CHAVE_CANDIDATA[n_], DL.CANDIDATA_DE[n_]) for n_ in RG.CHAVE_CANDIDATA] + [(RG.CHAVE_SAIDA_CANDIDATA[n_], _SAIDA_CAND[n_]) for n_ in RG.CHAVE_SAIDA_CANDIDATA]:''')
a.grava()
