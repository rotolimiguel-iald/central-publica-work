# -*- coding: utf-8 -*-
# regras (lote B) de derivar_encanamento_v406.py: os pequenos (guarda P18, o quadro do topo, a conferencia das secoes ACOM, a guarda da ordem de chamada). ORIGEM v405. PRIMEIRA PASSADA: so' o bump mecanico.
entrada("guarda_p18_v405.py", regras=[])
entrada("acom_conferencias_v405.py", regras=[])
entrada("runtime_quadro_v397.py", com_bump=False, dst="runtime_quadro_v397.py")
entrada("quadro_v397.py", regras=[
    ("import delta_v405 as DL", "import delta_v406 as DL", 1),
], com_bump=False, dst="quadro_v397.py")
# a guarda da ORDEM DE CHAMADA (licao 1 da v405): AUTORAL na v406 (guarda_ordem_de_chamada_v406.py, escrita a mao): a da v405 olhava so o corpo da funcao chamada no main, e os registros da v406 sao de uma linha; a copia daria vacuo. Fora da derivacao.
