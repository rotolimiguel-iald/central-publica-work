# -*- coding: utf-8 -*-
"""_r2ag_04_runtime_aescala_v410.py -- R2 (D99; ADENDO 4; B1 e B3): runtime_aescala_v410.py (o registro a_escala_v410; as 12 checagens seguem 12): o CONTROLE fail-closed da clausula (c8: todo campo de texto que anuncia o teorema
os_passos_sao_o_ciclo_ate_o_tetelestai traz a clausula do limite, PT e EN), o invariante B1 (c2: as ancoras novas == os nomes novos == a lista a ratificar) e os seis nomes de enunciado mudado (c11). A guarda das frases NAO muda."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r2ag_lib_v410 import aplicar

T = []
T.append(('''# Fonte autoral deste bloco: runtime_aescala_v410.py (cadeia_de_selo/v410); o contrato''',
          '''# (R2, D99, ADENDO 4) c8 tambem confere a CLAUSULA do limite (Z(s) soma os 2^n pixels e e' lida de uma vez pelo psion; o limiar n ln 2 e' o do tempo de UMA leitura; que o tempo conte os passos da maquina de Turing e' a traducao do dicionario e o termo que a liga ao Mathlib nao esta' no kernel) ao lado de TODO texto do registro que anuncia o teorema os_passos_sao_o_ciclo_ate_o_tetelestai; c2 tambem iguala as ancoras novas aos nomes novos a ratificar (B1); c11 tambem confere os seis nomes de enunciado mudado (B3)
# Fonte autoral deste bloco: runtime_aescala_v410.py (cadeia_de_selo/v410); o contrato''', 1))

# c2 (B1)
T.append(('''and bool(novas_) and all(novas_.values()) and bool(r4_) and all(r4_.values())
    # ---- c3 a pedra embutida''',
          '''and bool(novas_) and all(novas_.values()) and bool(r4_) and all(r4_.values()) and len(c_["ancoras_novas"]) == c_["n_nomes_novos"] == len(c_["nomes_novos_a_ratificar"])   # (R2, B1: o numero de ancoras novas == o de nomes novos a ratificar)
    # ---- c3 a pedra embutida''', 1))

# c8 (a clausula)
T.append(('''    c8_ok_ = d83_ in txt_ws_ and d83_ in body_ws_''',
          '''    # (R2, D99; ADENDO 4) a clausula do limite ao lado de TODO texto que anuncia o teorema: as folhas de texto do registro inteiro (estatuto, escopo, limites, diz, nao_diz e extras) que dizem «linear nos bits» (ou o nome do teorema com Z(s) >= 1)
    # trazem a clausula PT; as que dizem «linear in the bits» trazem a EN; o registro traz as duas; e o controle nao e' vazio (ha' folhas que anunciam)
    ws_ = lambda x_: _re410.sub(r"\\s+", " ", str(x_))
    clz_pt_ = ws_(c_["clausula_z_pt"]); clz_en_ = ws_(c_["clausula_z_en"])
    pilha_ = [("", t_)]; folhas_ = []
    while pilha_:
        cam_, o_ = pilha_.pop()
        if isinstance(o_, str):
            folhas_.append((cam_, ws_(o_)))
        elif isinstance(o_, dict):
            pilha_.extend((cam_ + "." + str(k_), v_) for k_, v_ in o_.items())
        elif isinstance(o_, (list, tuple)):
            pilha_.extend((cam_ + "[%d]" % i_, v_) for i_, v_ in enumerate(o_))
    anuncia_pt_ = lambda x_: bool(_re410.search(r"linear nos bits", x_) or ("os_passos_sao_o_ciclo_ate_o_tetelestai" in x_ and _re410.search(r"Z\\(s\\)\\s*(?:>=|\\u2265)", x_)))
    anuncia_en_ = lambda x_: bool(_re410.search(r"linear in the bits", x_))
    sem_pt_ = sorted(cam_ for cam_, x_ in folhas_ if anuncia_pt_(x_) and clz_pt_ not in x_)
    sem_en_ = sorted(cam_ for cam_, x_ in folhas_ if anuncia_en_(x_) and clz_en_ not in x_)
    n_anunciam_ = sum(1 for cam_, x_ in folhas_ if anuncia_pt_(x_) or anuncia_en_(x_))
    clausula_ok_ = bool(n_anunciam_ >= 3 and not sem_pt_ and not sem_en_ and clz_pt_ in txt_ws_ and clz_en_ in txt_ws_ and "Z(s) = \\u03a3_x" in clz_pt_ and "Z(s) = \\u03a3_x" in clz_en_)
    c8_ok_ = d83_ in txt_ws_ and d83_ in body_ws_''', 1))
T.append(('''and "o_leitor_e_a_escala" in txt_ws_ and "os_passos_sao_o_ciclo_ate_o_tetelestai" in txt_ws_
    # ---- c9 a guarda do texto''',
          '''and "o_leitor_e_a_escala" in txt_ws_ and "os_passos_sao_o_ciclo_ate_o_tetelestai" in txt_ws_ and clausula_ok_
    # ---- c9 a guarda do texto''', 1))

# c11 (B3: os seis nomes)
T.append(('''    c11_ok_ = (len(decl_) == c_["n_nomes"] == len(c_["nomes"])''',
          '''    seis_pt_ = ws_(c_["frase_seis_nomes_pt"]); seis_en_ = ws_(c_["frase_seis_nomes_en"])   # (R2, B3: a ratificacao de 09/11 e' dos nomes; seis deles passaram a ter outro enunciado nas R3/R4)
    seis_ok_ = bool(c_["seis_nomes"] and all(n_ in c_["nomes"] and n_ not in c_["nomes_novos_a_ratificar"] and n_ in seis_pt_ and n_ in seis_en_ for n_ in c_["seis_nomes"]) and any(seis_pt_ in ws_(x_) for x_ in t_["diz"]) and any(seis_pt_ in ws_(x_) for x_ in t_["limites"]) and seis_pt_ in txt_ws_ and seis_en_ in txt_ws_)
    c11_ok_ = (len(decl_) == c_["n_nomes"] == len(c_["nomes"])''', 1))
T.append(('''and "RATIFICADOS" in c_["estatuto_dos_nomes"] and novos_ok_)''',
          '''and "RATIFICADOS" in c_["estatuto_dos_nomes"] and novos_ok_ and seis_ok_)''', 1))

# as descricoes das tres checagens
T.append(('''a principal (a_escala) e as de secao entre elas" % c_["n_ancoras"]''', '''a principal (a_escala) e as de secao entre elas; as ancoras novas == os nomes novos a ratificar (R2, B1)" % c_["n_ancoras"]''', 1))
T.append(('''a forma obrigatoria da D83 no texto e na pedra (existe o algoritmo, e' a IALD; le a face sem leitura como dissipacao termica; validade no kernel; a creditacao e' do Clay), em PT e EN"''',
          '''a forma obrigatoria da D83 no texto e na pedra (existe o algoritmo, e' a IALD; le a face sem leitura como dissipacao termica; validade no kernel; a creditacao e' do Clay), em PT e EN; a forma do tempo (D94); a clausula do limite do teorema do Tetelestai (ADENDO 4, D99), PT e EN, ao lado de todo texto que o anuncia"''', 1))
T.append(('''e o registro os diz [DECLARADO, a ratificar], nunca ratificados" % (c_["n_nomes"], c_["n_nomes_novos"], len(c_["campos_novos_da_estrutura"]))''',
          '''e o registro os diz [DECLARADO, a ratificar], nunca ratificados; os seis nomes de enunciado mudado ditos (R2, B3)" % (c_["n_nomes"], c_["n_nomes_novos"], len(c_["campos_novos_da_estrutura"]))''', 1))

# os valores
T.append(('''"tempo_pt_no_texto": tempo_pt_ in txt_ws_, "tempo_en_no_texto": tempo_en_ in txt_ws_,''',
          '''"tempo_pt_no_texto": tempo_pt_ in txt_ws_, "tempo_en_no_texto": tempo_en_ in txt_ws_, "clausula_z_no_texto": {"pt": clz_pt_ in txt_ws_, "en": clz_en_ in txt_ws_}, "n_folhas_que_anunciam_o_teorema": n_anunciam_, "folhas_que_anunciam_sem_a_clausula": sem_pt_ + sem_en_, "seis_nomes_ditos": bool(seis_ok_),''', 1))
aplicar("runtime_aescala_v410.py", T)
