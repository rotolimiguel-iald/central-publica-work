# -*- coding: utf-8 -*-
# regras (lote B) de derivar_encanamento_v403.py: os pequenos (guarda P18, o quadro do topo, a conferencia das secoes ACOM). ORIGEM v402. PRIMEIRA PASSADA: so' o bump mecanico.
entrada("guarda_p18_v402.py", regras=[])
entrada("acom_conferencias_v402.py", regras=[])
entrada("runtime_quadro_v397.py", com_bump=False, dst="runtime_quadro_v397.py")
entrada("quadro_v397.py", regras=[
    ("import delta_v402 as DL", "import delta_v403 as DL", 1),
], com_bump=False, dst="quadro_v397.py")
