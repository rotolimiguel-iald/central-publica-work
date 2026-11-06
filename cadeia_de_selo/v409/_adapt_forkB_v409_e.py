# -*- coding: utf-8 -*-
"""_adapt_forkB_v409_e.py -- (claude-construtor-v409, fork B, 05/11/2026) quinta passada: a mutacao M6 do controle negativo do servico procurava o nome do arquivo da fala, que agora aparece tambem
na nota da 2a linha do recibo da parada; a mutacao passa a casar so' o argumento do os.path.join (o caminho que o script ABRE). Troca de contagem exata; backup de bytes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("bancada_B3_servico/controle_negativo/mutar_conferidor_v409.py")
a.troca('    a = "OPERADOR_05nov_prossigamos_v409_concordo_com_os_nomes_verbatim.txt"\n    assert t.count(a) == 1\n    return t.replace(a, "OPERADOR_05nov_prossigamos_v410_concordo_com_os_nomes_verbatim.txt", 1)',
        '    a = \'"cunhagens_13out", "OPERADOR_05nov_prossigamos_v409_concordo_com_os_nomes_verbatim.txt")\'   # (so\' o caminho que o script ABRE; o nome aparece tambem na nota da 2a linha)\n'
        '    assert t.count(a) == 1\n    return t.replace(a, a.replace("_v409_", "_v410_"), 1)')
a.grava()
