# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork B)] o derivador segue RECUSANDO de proposito (os cinco scripts da v411 nasceram da subida e foram adaptados a mao pelo fork B do construtor da v411); so' o texto da base do controle mudou (v410\base_v409)
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] o derivador segue RECUSANDO de proposito (os cinco scripts da v410 nasceram da subida e foram adaptados); so' a base do controle mudou no texto (v409\base_v408); conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida em 05/11/2026 pelo fork B do claude-construtor-v410 e em 06/11/2026 pelo fork B do claude-construtor-v410, com os rotulos subidos; na v411, adaptado em 12/11/2026 pelo fork B do claude-construtor-v411, retomada) ESTE DERIVADOR NAO SE APLICA A v411 e RECUSA (fail-closed) de proposito; conferido em 04/11/2026: os cinco scripts de servico da v411 ja existem e foram adaptados a mao; ver abaixo.
"""derivar_pre_selo_v411.py -- NAO RODA. Na v410 este arquivo era o derivador que gerava os cinco scripts do B(n) pre-selo a partir dos da v405 por substituicao de versoes (v405 -> v410, v403 -> v405, v402 -> v403).
Na v411 os cinco scripts (gerar_pino_recibo_pre_selo, conferir_recibo_pre_selo, snap_producao, rodar_ensaio_1_pre_selo, limpar_sandbox_vb22) NASCERAM de outra forma: pela subida mecanica de rotulo de _bump_copia_v411.py
(o mapa de versoes e de geracoes B(n) de _bump_copia_v411.py; diffs em bump/) e foram ADAPTADOS A MAO em 04/11/2026 (nota `# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida em 05/11/2026 pelo fork B do claude-construtor-v410 e em 06/11/2026 pelo fork B do claude-construtor-v410, com os rotulos subidos; na v411, adaptado em 12/11/2026 pelo fork B do claude-construtor-v411, retomada)` na 2a linha de cada um). Rodar o derivador da v410 so' trocando os rotulos nao reproduz isso, e MEDIDO na v410:
as fontes (v410\\bateria_pre_selo) citam v404, v405 e v410, e o mapa herdado ({v410: v411, v403: v410, v402: v403}) so' admite 402, 403 e 410 -- a primeira assercao do corpo antigo reprovaria; e, pior, um mapa herdado deixaria a base errada onde a v411 precisa de `v410\\base_v409`
(o controle negativo "selo anterior errado" usa o selo da versao ANTES da anterior: para a v411, a v409, guardada em v410\\base_v409).
Por isso o corpo antigo foi retirado, nao subido de rotulo: um derivador que falha por assercao, ou pior, que passa gerando arquivos errados, e' pior que nenhum. rodar_bn_pre_selo_v411.sh nao o chama mais; se faltar algum dos cinco scripts, ele PARA e manda refazer pela subida (_bump_copia_v411.py) e adaptar.
Esta recusa nao grava nada em lugar nenhum.
uso: python -I -B -X utf8 derivar_pre_selo_v411.py   (sai com codigo 2 e a explicacao)"""
import sys

sys.dont_write_bytecode = True
sys.stderr.write("derivar_pre_selo_v411.py: NAO SE APLICA (os cinco scripts da v411 nasceram de _bump_copia_v411.py e foram adaptados a mao; ver a docstring). Nada foi feito.\n")
sys.exit(2)
