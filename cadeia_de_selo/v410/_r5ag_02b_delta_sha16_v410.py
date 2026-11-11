# -*- coding: utf-8 -*-
"""_r5ag_02b_delta_sha16_v410.py -- R5: a frase da ratificacao D101 (PT e EN) cita a fala por sha256 com o PREFIXO de 16 hex (sha16 lido do arquivo) e reticencias, como as demais falas nos textos (o sha256 inteiro fica no contrato, em ratificacao_d101, e na D101);
um hash de 64 caracteres numa frase de artigo estoura a linha do PDF."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar
aplicar("delta_v410.py", [
    ("""% (len(NOMES_RATIFICADOS_D101_AESCALA), len(TEOREMAS_R5_AESCALA), len(CAMPOS_RATIFICADOS_D101_AESCALA), RATIFICACAO_D101_SHA256, ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS), len(NOMES_PENDENTES_AESCALA), ", ".join(NOMES_PENDENTES_AESCALA))""",
     """% (len(NOMES_RATIFICADOS_D101_AESCALA), len(TEOREMAS_R5_AESCALA), len(CAMPOS_RATIFICADOS_D101_AESCALA), RATIFICACAO_D101_SHA256[:16] + "...", ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS), len(NOMES_PENDENTES_AESCALA), ", ".join(NOMES_PENDENTES_AESCALA))""", 2)])
