# -*- coding: utf-8 -*-
# regras (lote B) de derivar_encanamento_v401.py: os pequenos (guarda P18, o quadro do topo, a conferencia das secoes ACOM). Escrito pela ferramenta Write.
# A guarda P18 e o quadro «O Teste da Unica Palavra» (v397) sao os mesmos da v400 (o quadro NAO se mexe: regra do 4,44); so' o import do delta muda.
entrada("guarda_p18_v400.py", regras=[])
entrada("runtime_quadro_v397.py", com_bump=False, dst="runtime_quadro_v397.py")
entrada("quadro_v397.py", regras=[
    ("import delta_v400 as DL", "import delta_v401 as DL", 1),
], com_bump=False, dst="quadro_v397.py")
