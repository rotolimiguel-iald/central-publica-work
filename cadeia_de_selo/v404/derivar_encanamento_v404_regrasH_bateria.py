# -*- coding: utf-8 -*-
# regras (lote H) de derivar_encanamento_v404.py: o elo B(n) PRE-SELO -- o orquestrador rodar_bn_pre_selo (os cinco arquivos da bateria sao derivados por derivar_pre_selo_v404.py, que MEDE as contagens). ORIGEM v403. Mapa: 402 -> 403, 403 -> 404.
import re as _re_h

entrada("bateria_pre_selo/rodar_bn_pre_selo_v403.sh", dst="bateria_pre_selo/rodar_bn_pre_selo_v404.sh", autoral=True, regras=[
    ('[ -f derivar_pre_selo_v404.py ] || { echo "== 0a. derivar_derivador_pre_selo_v404.py $(date +%T)"; $PY derivar_derivador_pre_selo_v404.py; }\n', "", 1),
    (lambda t_: _re_h.sub(r"(?<![0-9A-Za-z])vb20(?![0-9])", "vb21", t_), "vb20 -> vb21 (o sandbox curto da v404)", 1),
])
