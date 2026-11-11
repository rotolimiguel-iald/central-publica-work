# -*- coding: utf-8 -*-
"""_r5ag_07_copiar_insumos_v410.py -- R5: copiar_insumos_v410.py: a nota da lista congelada (gerada so' se o congelado nao existe) diz as CINCO falas de 10/11 (ADENDOS 2, 3, 5 e 6; D94, D96, D100 e D101). O congelado de 28 falas foi gravado por _r5ag_01 com a mesma nota."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar

aplicar("copiar_insumos_v410.py", [('''as tres de 10/11 dos ADENDOS 2 e 3, D94 e D96); de %d, so' o trecho e' embutido e citado''', '''as cinco de 10/11 dos ADENDOS 2, 3, 5 e 6, D94, D96, D100 e D101); de %d, so' o trecho e' embutido e citado''', 1)])
