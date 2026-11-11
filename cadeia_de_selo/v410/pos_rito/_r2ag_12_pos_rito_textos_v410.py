# -*- coding: utf-8 -*-
"""_r2ag_12_pos_rito_textos_v410.py -- R2 (D99): pos_rito\\textos_custodia_handoff_v410.py (ESCALA_TIPO_PT/EN: a clausula do limite ao lado do teorema, o item do Tetelestai como limiar, os seis nomes no README e no handoff, a costura do tempo) e
pos_rito\\textos_v410.py (a secao da escala: a clausula, o item do Tetelestai, os seis nomes, a costura do tempo; a faixa das decisoes lida do delta; _ea confere a clausula e os seis nomes no registro do core)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _r2ag_lib_v410 import aplicar

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ o handoff e o README
T = []
T.append(('''TEMPO_PT, TEMPO_EN = DL.FRASE_TEMPO_PT, DL.FRASE_TEMPO_EN   # D94/E33: a forma obrigatoria do tempo
''',
          '''TEMPO_PT, TEMPO_EN = DL.FRASE_TEMPO_PT, DL.FRASE_TEMPO_EN   # D94/E33: a forma obrigatoria do tempo
TEMPO_PT_C, TEMPO_EN_C = DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA, DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_EN_COSTURADA   # (R2, B4) a costura: o rotulo e a primeira letra em maiuscula; a constante da frase nao muda
CLZ_PT, CLZ_EN = DL.CLAUSULA_Z_PT, DL.CLAUSULA_Z_EN   # (R2, D99; ADENDO 4) a clausula do limite do teorema do Tetelestai, lida do delta (que a le do ADENDO 4)
SEIS_PT, SEIS_EN = DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT) + ".", DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_EN) + "."   # (R2, B3) a ratificacao de 09/11 e' dos nomes; seis deles passaram a ter outro enunciado nas R3/R4
assert all("%" not in x_ for x_ in (CLZ_PT, CLZ_EN, SEIS_PT, SEIS_EN, TEMPO_PT_C, TEMPO_EN_C)), "uma frase do delta traz «%%» (o formato dos textos quebraria)"
''', 1))
T.append(('''os passos são o ciclo até o Tetelestai (com n bits, passado o tempo de n oitavas, há solução se e só se Z(s) ≥ 1: a decisão em tempo finito do ciclo, linear nos bits) e a mentira lida como mentira é verdade. " + TEMPO_PT + ".")''',
          '''o limiar do Tetelestai (com n bits, passado o tempo de n oitavas, há solução se e só se Z(s) ≥ 1, e Z(s) separa o sim do não: a decisão em tempo finito do ciclo, linear nos bits) e a mentira lida como mentira é verdade. " + CLZ_PT + " " + TEMPO_PT_C + ".")''', 1))
T.append(('''the steps are the cycle up to the Tetelestai (with n bits, past the time of n octaves, there is a solution if and only if Z(s) ≥ 1: the decision in finite time of the cycle, linear in the bits) and a lie read as a lie is truth. " + TEMPO_EN + ".")''',
          '''the threshold of the Tetelestai (with n bits, past the time of n octaves, there is a solution if and only if Z(s) ≥ 1, and Z(s) separates the yes from the no: the decision in finite time of the cycle, linear in the bits) and a lie read as a lie is truth. " + CLZ_EN + " " + TEMPO_EN_C + ".")''', 1))
T.append(('''os %(nomes_aescala)d nomes anteriores seguem ratificados (D87).")''', '''os %(nomes_aescala)d nomes anteriores seguem ratificados (D87).") + " " + SEIS_PT''', 1))
T.append(('''the %(nomes_aescala)d earlier names stay ratified (D87).")''', '''the %(nomes_aescala)d earlier names stay ratified (D87).") + " " + SEIS_EN''', 1))
aplicar("textos_custodia_handoff_v410.py", T, base=HERE)

# ------------------------------------------------------------------ a secao da escala (Atlas) e a faixa das decisoes
T = []
T.append(('''cada ciclo aplica a mesma regra (`cada_ciclo_aplica_a_mesma_regra`); os passos são o ciclo até o Tetelestai (`os_passos_sao_o_ciclo_ate_o_tetelestai`): com n bits, passado o tempo de n oitavas, há solução se e só se Z(s) ≥ 1, o número de soluções ≤ Z(s) < o número de soluções + 1 e, sem solução, Z(s) < 1, a decisão em tempo finito do ciclo, linear nos bits; a mentira lida''',
          '''cada ciclo aplica a mesma regra (`cada_ciclo_aplica_a_mesma_regra`); o limiar do Tetelestai (`os_passos_sao_o_ciclo_ate_o_tetelestai`): com n bits, passado o tempo de n oitavas, há solução se e só se Z(s) ≥ 1, o número de soluções ≤ Z(s) < o número de soluções + 1 e, sem solução, Z(s) < 1: Z(s) separa o sim do não, a decisão em tempo finito do ciclo, linear nos bits (%s); que os passos sejam o ciclo até o Tetelestai é a leitura do dicionário [INPUT]; a mentira lida''', 1))
T.append(('''            ) % (DL_.FRASE_TEMPO_PT, cic["n_bits"],''', '''            ) % (DL_.CLAUSULA_Z_PT, DL_.ROTULO_TEMPO + " " + DL_.FRASE_TEMPO_PT_COSTURADA, cic["n_bits"],''', 1))
T.append(('''           ) % (DL_.FRASE_NOMES_RATIFICADOS_AESCALA_PT, ss["ratifico_tudo"], _cita(DL_.FRASE_RATIFICO_TUDO), len(DL_.NOMES_AESCALA), _cita(DL_.FRASE_SEM_AUTORIDADE))''',
          '''           ) % (DL_.FRASE_NOMES_RATIFICADOS_AESCALA_PT, ss["ratifico_tudo"], _cita(DL_.FRASE_RATIFICO_TUDO), len(DL_.NOMES_AESCALA), _cita(DL_.FRASE_SEM_AUTORIDADE)) + " " + DL_.costura_maiuscula(DL_.FRASE_SEIS_NOMES_PT) + "."   # (R2, B3: a ratificacao de 09/11 e' dos nomes; seis deles passaram a ter outro enunciado nas R3/R4)''', 1))
T.append(('''    ks = list(_dl().DECISOES_V410)
    return "%s a %s" % (ks[0], ks[-1])''', '''    return _dl().DECISOES_ROTULO   # (R2, D99: a lista NAO e' contigua -- D63 a D96 e D99; D97 e D98 ficam fora do um.py)''', 1))
T.append(('''and ea.get("estatuto_dos_nomes") == DL_.FRASE_NOMES_RATIFICADOS_AESCALA_PT, "a forma canonica do Clay (D84), a da D83 ou a ratificacao (D87) do registro != delta"''',
          '''and ea.get("estatuto_dos_nomes") == DL_.FRASE_NOMES_RATIFICADOS_AESCALA_PT, "a forma canonica do Clay (D84), a da D83 ou a ratificacao (D87) do registro != delta"
    assert ea.get("clausula_z_pt") == DL_.CLAUSULA_Z_PT and ea.get("clausula_z_en") == DL_.CLAUSULA_Z_EN and ea.get("frase_seis_nomes_pt") == DL_.FRASE_SEIS_NOMES_PT and ea.get("frase_seis_nomes_en") == DL_.FRASE_SEIS_NOMES_EN and (ev.get("clausula_z_no_texto") or {}) == {"pt": True, "en": True} and ev.get("seis_nomes_ditos") is True and not (ev.get("folhas_que_anunciam_sem_a_clausula") or []) and int(ev.get("n_folhas_que_anunciam_o_teorema") or 0) >= 3, "o registro a_escala_v410 do core nao traz a clausula do limite do teorema do Tetelestai (ADENDO 4, D99) ao lado de todo texto que o anuncia, nem os seis nomes (R2)"''', 1))
aplicar("textos_v410.py", T, base=HERE)
