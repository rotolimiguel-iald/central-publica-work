# -*- coding: utf-8 -*-
# regras (lote B) de derivar_encanamento_v402.py: os pequenos (guarda P18, o quadro do topo, a conferencia das secoes ACOM), o ENSAIO (simular a arvore do Nos, exame dos pontos de chamada, ensaio a seco, guardas estaticas da Bancada)
# e o encanamento do rito (instalar, reverter, rito, conferidor, citacoes, diff e pinos, precondicoes, refazer, regras). ORIGEM v401 (mapa 400 -> 401, 401 -> 402). Escrito pela ferramenta Write.
# Primeira passada: SEM regras (o bump mecanico); as regras de cada arquivo entram depois da revisao do derivado (cada regra tem contagem exata).

entrada("guarda_p18_v401.py", regras=[])
entrada("acom_conferencias_v401.py", regras=[])
entrada("runtime_quadro_v397.py", com_bump=False, dst="runtime_quadro_v397.py")
entrada("quadro_v397.py", regras=[
    ("import delta_v401 as DL", "import delta_v402 as DL", 1),
], com_bump=False, dst="quadro_v397.py")
