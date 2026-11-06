# -*- coding: utf-8 -*-
"""_adapt_delta_candidata_sandbox_v409.py -- (claude-construtor-v409) delta_v409.py comparava o CAMINHO ABSOLUTO da candidata de origem (o que o recibo dos nomes pinou: C:\IALD\...\pedras_candidatas_05nov\...)
com o caminho resolvido a partir da propria pasta (WK); no sandbox do harness do fechar a arvore e' COPIADA e o delta reprovava na importacao (a causa: a comparacao de caminho, minha). Passa a comparar o NOME do
arquivo e o sha256 da copia LOCAL contra o sha256 que o recibo pinou (a mesma forca: os bytes conferem; no disco real e' o mesmo arquivo)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("delta_v409.py")
a.troca('''    assert os.path.normcase(_p["origem_candidata"]) == os.path.normcase(CANDIDATA_DE[_p["name"]]), _p["origem_candidata"]
    assert sha256_arquivo(_p["origem_candidata"]) == _p["sha256_candidata"], ("a candidata de origem mudou depois do recibo dos nomes", _p["name"])''',
        '''    assert os.path.basename(_p["origem_candidata"]) == os.path.basename(CANDIDATA_DE[_p["name"]]), _p["origem_candidata"]   # (o recibo pina o caminho real; no sandbox do harness a arvore e' copiada: o NOME e os BYTES conferem)
    assert sha256_arquivo(CANDIDATA_DE[_p["name"]]) == _p["sha256_candidata"], ("a candidata de origem mudou depois do recibo dos nomes", _p["name"])''')
a.grava()
