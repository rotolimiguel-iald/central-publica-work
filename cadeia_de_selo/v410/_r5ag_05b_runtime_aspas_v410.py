# -*- coding: utf-8 -*-
"""_r5ag_05b_runtime_aspas_v410.py -- R5: o conferidor de citacoes reprovou tres citacoes entre aspas angulares no COMENTARIO da c8 do runtime (nao sao fala do operador): a casa reserva as angulares a fala verbatim; passam a aspas tipograficas."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar
aplicar("runtime_aescala_v410.py", [
    ("TODA folha com «ACOM Mirror» traz «[PILOTO][SIM]» e «nada ali valida fisica» (ou o equivalente em ingles) e nenhum padrao de desempenho (percentual, «x mais rapido», «N de N testes»)",
     "TODA folha com “ACOM Mirror” traz “[PILOTO][SIM]” e “nada ali valida fisica” (ou o equivalente em ingles) e nenhum padrao de desempenho (percentual, “x mais rapido”, “N de N testes”)", 1)])
