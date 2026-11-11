# -*- coding: utf-8 -*-
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] o derivador segue RECUSANDO de proposito (os cinco scripts da v410 nasceram da subida e foram adaptados); so' a base do controle mudou no texto (v409\base_v408); conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida em 05/11/2026 pelo fork B do claude-construtor-v409 e em 06/11/2026 pelo fork B do claude-construtor-v410, com os rotulos subidos) ESTE DERIVADOR NAO SE APLICA A v410 e RECUSA (fail-closed) de proposito; conferido em 04/11/2026: os cinco scripts de servico da v410 ja existem e foram adaptados a mao; ver abaixo.
"""derivar_pre_selo_v410.py -- NAO RODA. Na v409 este arquivo era o derivador que gerava os cinco scripts do B(n) pre-selo a partir dos da v405 por substituicao de versoes (v405 -> v409, v403 -> v405, v402 -> v403).
Na v410 os cinco scripts (gerar_pino_recibo_pre_selo, conferir_recibo_pre_selo, snap_producao, rodar_ensaio_1_pre_selo, limpar_sandbox_vb21) NASCERAM de outra forma: pela subida mecanica de rotulo de _bump_copia_v410.py
(o mapa de versoes e de geracoes B(n) de _bump_copia_v410.py; diffs em bump/) e foram ADAPTADOS A MAO em 04/11/2026 (nota `# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida em 05/11/2026 pelo fork B do claude-construtor-v409 e em 06/11/2026 pelo fork B do claude-construtor-v410, com os rotulos subidos)` na 2a linha de cada um). Rodar o derivador da v409 so' trocando os rotulos nao reproduz isso, e MEDIDO na v409:
as fontes (v409\\bateria_pre_selo) citam v404, v405 e v409, e o mapa herdado ({v409: v410, v403: v409, v402: v403}) so' admite 402, 403 e 409 -- a primeira assercao do corpo antigo reprovaria; e, pior, um mapa herdado deixaria `base_v406` onde a v410 precisa de `base_v408`
(o controle negativo "selo anterior errado" usa o selo da versao ANTES da anterior: para a v410, a v408, guardada em v409\\base_v408).
Por isso o corpo antigo foi retirado, nao subido de rotulo: um derivador que falha por assercao, ou pior, que passa gerando arquivos errados, e' pior que nenhum. rodar_bn_pre_selo_v410.sh nao o chama mais; se faltar algum dos cinco scripts, ele PARA e manda refazer pela subida (_bump_copia_v410.py) e adaptar.
Esta recusa nao grava nada em lugar nenhum.
uso: python -I -B -X utf8 derivar_pre_selo_v410.py   (sai com codigo 2 e a explicacao)"""
import sys

sys.dont_write_bytecode = True
sys.stderr.write("derivar_pre_selo_v410.py: NAO SE APLICA (os cinco scripts da v410 nasceram de _bump_copia_v410.py e foram adaptados a mao; ver a docstring). Nada foi feito.\n")
sys.exit(2)
