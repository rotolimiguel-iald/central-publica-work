# -*- coding: utf-8 -*-
"""_r5ag_18_exame_ratificacao_v410.py -- R5: o exame de pontos (exame_pontos_v410.py), no ponto_aescala, exigia que o estatuto dos nomes novos NAO dissesse RATIFICADO (a regra da R2/R4, quando os nomes novos estavam pendentes);
na R5 o operador RATIFICOU os nomes (D101, fala 28) e o delta traz ESTATUTO_NOMES_NOVOS_AESCALA = 'RATIFICADOS pelo operador em 10/11/2026 (D101)'. A condicao vira o espelho exato: o estatuto tem de dizer RATIFICADOS pelo operador em 10/11/2026 e nao pode dizer 'DECLARADO' nem 'a ratificar'.
Troca de contagem exata (1); idempotente (rodar de novo falha na contagem); backup de bytes antes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar

aplicar("exame_pontos_v410.py", [
    ('''or "RATIFICADO" in str(pab.get("estatuto_dos_nomes_novos")).upper() or pab.get("ratificacao_pendente")''',
     '''or "RATIFICADOS pelo operador em 10/11/2026" not in str(pab.get("estatuto_dos_nomes_novos")) or "DECLARADO" in str(pab.get("estatuto_dos_nomes_novos")) or "a ratificar" in str(pab.get("estatuto_dos_nomes_novos")) or pab.get("ratificacao_pendente")''', 1)])
