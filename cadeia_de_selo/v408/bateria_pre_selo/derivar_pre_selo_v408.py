# -*- coding: utf-8 -*-
# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork C)] ESTE DERIVADOR NAO SE APLICA A v408 e RECUSA (fail-closed) de proposito; conferido em 04/11/2026: os cinco scripts de servico da v408 ja existem e foram adaptados a mao; ver abaixo.
"""derivar_pre_selo_v408.py -- NAO RODA. Na v407 este arquivo era o derivador que gerava os cinco scripts do B(n) pre-selo a partir dos da v405 por substituicao de versoes (v405 -> v407, v403 -> v405, v402 -> v403).
Na v408 os cinco scripts (gerar_pino_recibo_pre_selo, conferir_recibo_pre_selo, snap_producao, rodar_ensaio_1_pre_selo, limpar_sandbox_vb21) NASCERAM de outra forma: pela subida mecanica de rotulo de _bump_copia_v408.py
(o mapa de versoes e de geracoes B(n) de _bump_copia_v408.py; diffs em bump/) e foram ADAPTADOS A MAO em 04/11/2026 (nota `# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork C)]` na 2a linha de cada um). Rodar o derivador da v407 so' trocando os rotulos nao reproduz isso, e MEDIDO na v407:
as fontes (v407\\bateria_pre_selo) citam v404, v405 e v407, e o mapa herdado ({v407: v408, v403: v407, v402: v403}) so' admite 402, 403 e 407 -- a primeira assercao do corpo antigo reprovaria; e, pior, um mapa herdado deixaria `base_v405` onde a v408 precisa de `base_v406`
(o controle negativo "selo anterior errado" usa o selo da versao ANTES da anterior: para a v408, a v406, guardada em v407\\base_v406).
Por isso o corpo antigo foi retirado, nao subido de rotulo: um derivador que falha por assercao, ou pior, que passa gerando arquivos errados, e' pior que nenhum. rodar_bn_pre_selo_v408.sh nao o chama mais; se faltar algum dos cinco scripts, ele PARA e manda refazer pela subida (_bump_copia_v408.py) e adaptar.
Esta recusa nao grava nada em lugar nenhum.
uso: python -I -B -X utf8 derivar_pre_selo_v408.py   (sai com codigo 2 e a explicacao)"""
import sys

sys.dont_write_bytecode = True
sys.stderr.write("derivar_pre_selo_v408.py: NAO SE APLICA (os cinco scripts da v408 nasceram de _bump_copia_v408.py e foram adaptados a mao; ver a docstring). Nada foi feito.\n")
sys.exit(2)
