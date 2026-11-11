# -*- coding: utf-8 -*-
"""_r5ag_16_pos_rito_testes_v410.py -- R5: teste_textos_custodia_sem_candidato_v410.py: a clausula do limite aparece AGORA duas vezes no ENTROU_EN (ao lado do teorema da R4 e ao lado da clausula do Tetelestai em 1 - beta, D100): a contagem passa de 1 a 2 e o teste confere a clausula do Tetelestai (frase + clausula do limite logo depois),
a reconstrucao, a errata, o dispositivo com as ressalvas e a ratificacao D101 no README e no ENTROU_EN; controles negativos: o README sem a clausula do limite ao lado da clausula do Tetelestai e a citacao do dispositivo sem [PILOTO][SIM] reprovam."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _r5ag_lib_v410 import aplicar

HERE = os.path.dirname(os.path.abspath(__file__))
aplicar("teste_textos_custodia_sem_candidato_v410.py", [
    ('''dict(G["TEXTOS"])["ENTROU_EN"].count(DL.CLAUSULA_Z_EN) == 1 and''', '''dict(G["TEXTOS"])["ENTROU_EN"].count(DL.CLAUSULA_Z_EN) == 2 and''', 1),
    ('''    print("secao README (D85): tres itens,''',
     '''    _en5 = dict(G["TEXTOS"])["ENTROU_EN"]
    c5_ = bool(DL.FRASE_TETELESTAI_PT + ". " + DL.CLAUSULA_Z_PT in R and DL.FRASE_TETELESTAI_EN + ". " + DL.CLAUSULA_Z_EN in _en5 and DL.FRASE_RECONSTROI_PT in R and DL.FRASE_RECONSTROI_EN in _en5 and DL.FRASE_E36_PT in R and DL.FRASE_E36_EN in _en5 and DL.FRASE_DISPOSITIVO_PT in R and DL.FRASE_DISPOSITIVO_EN in _en5
               and "[PILOTO][SIM]" in R and "[PILOTO][SIM]" in _en5 and DL.costura_maiuscula(DL.FRASE_NOMES_RATIFICADOS_D101_PT) in R and DL.costura_maiuscula(DL.FRASE_NOMES_RATIFICADOS_D101_EN) in _en5 and "[DECLARADO, a ratificar]" not in R + _en5)   # (R5, D100 e D101)
    print("R5 (D100 e D101): a clausula do Tetelestai com a clausula do limite logo depois, a reconstrucao, a errata, o dispositivo com [PILOTO][SIM] e a ratificacao D101 no README e no ENTROU_EN: %s" % c5_); ok = ok and c5_
    for nome_, txt_, ok_esperado_ in (("README sem a clausula do limite logo depois da clausula do Tetelestai", R.replace(DL.FRASE_TETELESTAI_PT + ". " + DL.CLAUSULA_Z_PT, DL.FRASE_TETELESTAI_PT + ". (retirada)"), False), ("README com o dispositivo sem [PILOTO][SIM]", R.replace("[PILOTO][SIM]", "(retirado)"), False)):
        r_ = bool(DL.FRASE_TETELESTAI_PT + ". " + DL.CLAUSULA_Z_PT in txt_ and "[PILOTO][SIM]" in txt_)
        print("controle negativo (R5): %s: reprovou: %s" % (nome_, r_ is ok_esperado_)); ok = ok and (r_ is ok_esperado_)
    print("secao README (D85): tres itens,''', 1)], base=HERE)
