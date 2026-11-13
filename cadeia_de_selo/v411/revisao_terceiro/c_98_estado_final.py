import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
for it, txt in (("C1", "feito (11 mudancas; nenhum controle removido; ver REVISAO_TERCEIRO_v411.R1.C.json)"), ("C3", "feito (tabela de 15 linhas; ALTO C-01)"), ("C4", "feito"), ("C5", "feito"),
                ("C6", "feito"), ("C7", "feito (handoff real inexistente; ensaio lido)"), ("C8", "feito"), ("C9", "feito (29 portoes lidos)"), ("ENTREGA", "REVISAO_TERCEIRO_v411.R1.C.json e .md gravados; aprovada=false (1 ALTO, 0 MEDIO, 10 BAIXO)")):
    estado_item(it, txt)
e = estado_load(); print(sorted(e["itens"]), len(e["achados"]))
