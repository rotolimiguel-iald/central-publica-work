# -*- coding: utf-8 -*-
"""_adapt_relatorio_v409_c.py -- (claude-construtor-v409, 05/11/2026) o portao harness_fechar fica MAIS estrito: so' conta a rodada INTEIRA do harness do fechar (a fila da memoria rodou com o pino REAL do memoria.py,
PINO_MEMORIA_PY_v409.json, e passou), nunca uma rodada --sem-fila ou --pino-emulado (que validam so' a parte do fechar enquanto a gerencia nao pinou o memoria.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("gerar_relatorio_v409.py")
a.troca('"harness_fechar": passou(H_F),', '"harness_fechar": bool(passou(H_F) and not (H_F or {}).get("pino_emulado") and (((H_F or {}).get("etapas") or {}).get("fila_da_memoria") or {}).get("tudo_passou") is True),   # (v409: so\' a rodada inteira, com a fila e o pino REAL)')
a.grava()
