# -*- coding: utf-8 -*-
"""_adapt_forkB_v409_c.py -- (claude-construtor-v409, fork B, 05/11/2026) terceira passada: o comentario do instalar citava o nome do arquivo da lista da v408, que o conferidor proibe como rotulo velho. Troca de contagem exata; backup de bytes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("instalar_v409.py")
a.troca("# (os 4 da v408: os nomes da lista de modulos novos pinada na cadeia v408, kernel_modulos_novos_v408.json, conferidos pelo adaptador)", "# (os 4 da v408: os nomes da lista de modulos novos que a cadeia v408 pinou, conferidos pelo adaptador da v409)")
a.grava()
