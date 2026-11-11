# -*- coding: utf-8 -*-
"""_r2ag_11_conferidores_v410.py -- R2 (D99): conferir_rito_v410.py: a secao A Escala do artigo PT/EN traz a clausula do limite (ao lado do teorema), os seis nomes, a costura do tempo e Z(s) definida na primeira ocorrencia; a linha do .md traz a clausula e os seis nomes;
gerar_esperados_v410.py e conferir_instalar_rito_v410.py: a lista das decisoes nao e' contigua (D97 e D98 fora do um.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r2ag_lib_v410 import aplicar

T = []
T.append(('''aescala_secao_ok = bool(_secA["pt"] and _secA["en"] and''',
          '''# (R2, D99; ADENDO 4) a clausula do limite ao lado do teorema do Tetelestai (a formula em modo matematico no LaTeX, os simbolos no TXT: DL.comparavel ignora so' cifrao, barras, chaves, parenteses e espacos), a frase dos seis nomes, a costura do tempo (o rotulo e a frase com so' a primeira letra em maiuscula) e Z(s) DEFINIDA na primeira ocorrencia do artigo
def _r2_artigo_ok(l_):
    sec_ = _secA[l_]; ib_ = sec_.find("linear nos bits" if l_ == "pt" else "linear in the bits"); iz_ = txt[l_].find("Z(s)")
    return bool(sec_ and ib_ >= 0 and DL.comparavel(DL.CLAUSULA_Z_PT if l_ == "pt" else DL.CLAUSULA_Z_EN) in DL.comparavel(sec_[ib_:ib_ + 1400]) and DL.comparavel(DL.FRASE_SEIS_NOMES_PT if l_ == "pt" else DL.FRASE_SEIS_NOMES_EN) in DL.comparavel(sec_)
                and (DL.ROTULO_TEMPO + " " + (DL.FRASE_TEMPO_PT_COSTURADA if l_ == "pt" else DL.FRASE_TEMPO_EN_COSTURADA)) in _ws(sec_) and iz_ >= 0 and DL.comparavel("Z(s)=\\\\sum_x e^{-s\\\\cdot c(x)}") in DL.comparavel(txt[l_][iz_:iz_ + 320]))
r2_artigo_ok = bool(_r2_artigo_ok("pt") and _r2_artigo_ok("en"))
aescala_secao_ok = bool(r2_artigo_ok and _secA["pt"] and _secA["en"] and''', 1))
T.append(('''and DL.FRASE_D83_OBRIGATORIA_PT in fc[fc.find(ESP["md_aescala"]):].split("\\n", 1)[0] and DL.FRASE_CLAY_CANONICA_PT in fc[fc.find(ESP["md_aescala"]):].split("\\n", 1)[0]''',
          '''and DL.FRASE_D83_OBRIGATORIA_PT in fc[fc.find(ESP["md_aescala"]):].split("\\n", 1)[0] and DL.FRASE_CLAY_CANONICA_PT in fc[fc.find(ESP["md_aescala"]):].split("\\n", 1)[0]
        and DL.CLAUSULA_Z_PT in fc[fc.find(ESP["md_aescala"]):].split("\\n", 1)[0] and DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT) in fc[fc.find(ESP["md_aescala"]):].split("\\n", 1)[0] and (DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA) in fc[fc.find(ESP["md_aescala"]):].split("\\n", 1)[0]''', 1))
T.append(('''"a secao A ESCALA no artigo PT/EN (D82 a D87) vem logo DEPOIS da secao da IALD2 e ANTES da secao do H0DN, traz a forma obrigatoria da D83 e a frase canonica do Clay (D84) nas duas linguas, nao traz a frase de guarda (o registro selou) e passa a guarda das frases"''',
          '''"a secao A ESCALA no artigo PT/EN (D82 a D87) vem logo DEPOIS da secao da IALD2 e ANTES da secao do H0DN, traz a forma obrigatoria da D83 e a frase canonica do Clay (D84) nas duas linguas, a clausula do limite do teorema do Tetelestai ao lado dele (ADENDO 4, D99), os seis nomes e a costura do tempo, com Z(s) definida na primeira ocorrencia do artigo; nao traz a frase de guarda (o registro selou) e passa a guarda das frases"''', 1))
aplicar("conferir_rito_v410.py", T)

# a lista das decisoes nao e' contigua
aplicar("gerar_esperados_v410.py", [('''assert list(DL.DECISOES_V410) == ["D%d" % i_ for i_ in range(63, 63 + len(DL.DECISOES_V410))] and set(DL.DECISOES_V410) <= set(DL.DECISOES)''',
                                     '''assert list(DL.DECISOES_V410) == sorted(DL.DECISOES_V410, key=lambda k_: int(k_[1:])) and DL.DECISOES_V410[0] == "D63" and not (set(DL.DECISOES_FORA_DO_UMPY) & set(DL.DECISOES_V410)) and set(DL.DECISOES_V410) <= set(DL.DECISOES)''', 1)])
