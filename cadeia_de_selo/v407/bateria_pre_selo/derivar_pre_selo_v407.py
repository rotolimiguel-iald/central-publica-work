# -*- coding: utf-8 -*-
# [ADAPTADO v407, 03/11/2026] ESTE DERIVADOR NAO SE APLICA A v407 e RECUSA (fail-closed) de proposito; ver abaixo.
"""derivar_pre_selo_v407.py -- NAO RODA. Na v406 este arquivo era o derivador que gerava os cinco scripts do B(n) pre-selo a partir dos da v405 por substituicao de versoes (v405 -> v406, v403 -> v405, v402 -> v403).
Na v407 os cinco scripts (gerar_pino_recibo_pre_selo, conferir_recibo_pre_selo, snap_producao, rodar_ensaio_1_pre_selo, limpar_sandbox_vb21) NASCERAM de outra forma: pela subida mecanica de rotulo de _bump_copia_v407.py
(405 -> 406, 406 -> 407, B14 -> B15, B15 -> B16; diffs em bump/) e foram ADAPTADOS A MAO (marca `# [ADAPTADO v407, 03/11/2026]` na 2a linha de cada um). Rodar o derivador da v406 so' trocando os rotulos nao reproduz isso, e MEDIDO:
as fontes (v406\\bateria_pre_selo) citam v404, v405 e v406, e o mapa herdado ({v406: v407, v403: v406, v402: v403}) so' admite 402, 403 e 406 -- a primeira assercao do corpo antigo reprovaria; e, pior, o mapa deixaria `base_v404` onde a v407 precisa de `base_v405`
(o controle negativo "selo anterior errado" usa o selo da versao ANTES da anterior: para a v407, a v405, guardada em v406\\base_v405).
Por isso o corpo antigo foi retirado, nao subido de rotulo: um derivador que falha por assercao, ou pior, que passa gerando arquivos errados, e' pior que nenhum. rodar_bn_pre_selo_v407.sh nao o chama mais; se faltar algum dos cinco scripts, ele PARA e manda refazer pela subida (_bump_copia_v407.py) e adaptar.
Esta recusa nao grava nada em lugar nenhum.
uso: python -I -B -X utf8 derivar_pre_selo_v407.py   (sai com codigo 2 e a explicacao)"""
import sys

sys.dont_write_bytecode = True
sys.stderr.write("derivar_pre_selo_v407.py: NAO SE APLICA (os cinco scripts da v407 nasceram de _bump_copia_v407.py e foram adaptados a mao; ver a docstring). Nada foi feito.\n")
sys.exit(2)
