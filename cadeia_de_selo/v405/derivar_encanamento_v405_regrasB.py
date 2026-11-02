# -*- coding: utf-8 -*-
# regras (lote B) de derivar_encanamento_v405.py: os pequenos (guarda P18, o quadro do topo, a conferencia das secoes ACOM, a guarda da ordem de chamada). ORIGEM v404. PRIMEIRA PASSADA: so' o bump mecanico.
entrada("guarda_p18_v404.py", regras=[])
entrada("acom_conferencias_v404.py", regras=[])
entrada("runtime_quadro_v397.py", com_bump=False, dst="runtime_quadro_v397.py")
entrada("quadro_v397.py", regras=[
    ("import delta_v404 as DL", "import delta_v405 as DL", 1),
], com_bump=False, dst="quadro_v397.py")
# a guarda da ORDEM DE CHAMADA (licao 1 da v404): AUTORAL na v405 (guarda_ordem_de_chamada_v405.py, escrita a mao): a da v404 olhava so o corpo da funcao chamada no main, e os registros da v405 sao de uma linha; a copia daria vacuo. Fora da derivacao.
