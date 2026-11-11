# -*- coding: utf-8 -*-
"""_r4ag_13_p00_v410.py -- p00_precondicoes_v410.py: o recibo dos nomes (da gerencia, ate' 09/11) cobre as falas ate' 09/11; as de 10/11 (ADENDOS 2 e 3) entram pelo prefixo de sha256 lido do texto dos adendos e conferido contra o arquivo no delta (DL.FALAS_FORA_DO_RECIBO).
Nada e' afrouxado: toda fala do candidato tem de estar no recibo OU ser uma das FALAS_FORA_DO_RECIBO com prefixo de sha256 do delta."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from _r4ag_lib_v410 import aplicar

A = 'and R_["falas_n"] == DL.N_FALAS_V410 == len(R_["falas"]) and {f_["sha256"] for f_ in R_["falas"]} == {(v_.get("sha256_arquivo_inteiro") or v_["sha256"]) for v_ in CM["cunhagens"].values()} and R_["ratificacao_aescala_D87"]'
B = ('and R_["falas_n"] == len(R_["falas"]) == DL.N_FALAS_V410 - len(DL.FALAS_FORA_DO_RECIBO) and all(n_ in DL.VERBATIM_PREFIXOS_DA_ORDEM_V410 for n_ in DL.FALAS_FORA_DO_RECIBO) and set(DL.FALAS_FORA_DO_RECIBO) <= set(DL.NOMES_V410_DO_DESENHO) and len(R_["falas"]) + len(DL.FALAS_FORA_DO_RECIBO) == len(CM["cunhagens"]) '
     'and {f_["sha256"] for f_ in R_["falas"]} == {(v_.get("sha256_arquivo_inteiro") or v_["sha256"]) for v_ in CM["cunhagens"].values() if v_.get("nome") not in DL.FALAS_FORA_DO_RECIBO} and R_["ratificacao_aescala_D87"]')
aplicar("p00_precondicoes_v410.py", [(A, B, 1)])
