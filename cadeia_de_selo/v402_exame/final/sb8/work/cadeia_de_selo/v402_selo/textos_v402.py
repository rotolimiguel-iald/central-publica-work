# -*- coding: utf-8 -*-
# STUB do harness (NAO sao os textos da cadeia): paragrafos e handoff minimos, limpos da guarda P18.
TOPICO_NOVO = 'v402-selada-ponte-queda-esperanca.md'


def paragrafo_readme():
    return 'PARAGRAFO DO QUADRO (stub do harness)\n', {'stub': True}


def paragrafo_v402():
    return 'PARAGRAFO DA V402 (stub do harness)\n', {'stub': True}


def handoff(V, k):
    return '---\nname: handoff-v402-custodia\ndescription: "handoff de ensaio (stub do harness)"\nmetadata:\n  type: project\n---\n\n# HANDOFF v402 (stub do harness)\n\n%s %s %s\n' % (V['s16'], k['ap_nome'], k['ap_ver'])
