# -*- coding: utf-8 -*-
"""_r2ag_13_pos_rito_portao_v410.py -- R2 (D99): pos_rito\\leitura_v410.py (o PORTAO; so' ACRESCENTA: a clausula do limite do teorema do Tetelestai ao lado de todo texto do registro a_escala_v410 que o anuncia, PT e EN, e os seis nomes; a lista das decisoes nao e' contigua),
pos_rito\\registrar_mapa_v410.py (a lista das decisoes nao e' contigua) e pos_rito\\gerar_derivacao_pos_rito_v410.py (o rotulo das decisoes lido do delta)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _r2ag_lib_v410 import aplicar

HERE = os.path.dirname(os.path.abspath(__file__))

CLAUSULA = '''    # (R2, D99; ADENDO 4; so' ACRESCENTADO ao portao) a clausula do limite do teorema do Tetelestai ao lado de TODO texto do registro a_escala_v410 que o anuncia («linear nos bits», ou o nome do teorema com Z(s) >= 1), PT e EN, e os seis nomes (B3): o registro do core e' relido aqui com a regra do runtime
    ea_pilha_ = [('', {k_: ea_.get(k_) for k_ in ('estatuto', 'scope', 'limites', 'diz', 'nao_diz', 'decisoes', 'erratas', 'leituras_do_operador', 'clausula_z_pt', 'clausula_z_en', 'frase_seis_nomes_pt', 'frase_seis_nomes_en')})]; ea_folhas_ = []
    while ea_pilha_:
        ea_cam_, ea_o_ = ea_pilha_.pop()
        if isinstance(ea_o_, str):
            ea_folhas_.append((ea_cam_, re.sub(r'\\s+', ' ', ea_o_)))
        elif isinstance(ea_o_, dict):
            ea_pilha_.extend((ea_cam_ + '.' + str(k_), v_) for k_, v_ in ea_o_.items())
        elif isinstance(ea_o_, (list, tuple)):
            ea_pilha_.extend((ea_cam_ + '[%d]' % i_, v_) for i_, v_ in enumerate(ea_o_))
    ea_clz_pt_ = re.sub(r'\\s+', ' ', DL_.CLAUSULA_Z_PT); ea_clz_en_ = re.sub(r'\\s+', ' ', DL_.CLAUSULA_Z_EN); ea_seis_pt_ = re.sub(r'\\s+', ' ', DL_.FRASE_SEIS_NOMES_PT)
    ea_anuncia_pt_ = lambda x_: bool(re.search(r'linear nos bits', x_) or ('os_passos_sao_o_ciclo_ate_o_tetelestai' in x_ and re.search(r'Z\\(s\\)\\s*(?:>=|\\u2265)', x_)))
    ea_anuncia_en_ = lambda x_: bool(re.search(r'linear in the bits', x_))
    ea_sem_clz_ = sorted(c_ for c_, x_ in ea_folhas_ if (ea_anuncia_pt_(x_) and ea_clz_pt_ not in x_) or (ea_anuncia_en_(x_) and ea_clz_en_ not in x_))
    ea_clausula_ok_ = bool(sum(1 for c_, x_ in ea_folhas_ if ea_anuncia_pt_(x_) or ea_anuncia_en_(x_)) >= 3 and not ea_sem_clz_ and ea_.get('clausula_z_pt') == DL_.CLAUSULA_Z_PT and ea_.get('clausula_z_en') == DL_.CLAUSULA_Z_EN
                           and ea_.get('frase_seis_nomes_pt') == DL_.FRASE_SEIS_NOMES_PT and ea_.get('frase_seis_nomes_en') == DL_.FRASE_SEIS_NOMES_EN and (ea_v_.get('clausula_z_no_texto') or {}) == {'pt': True, 'en': True} and ea_v_.get('seis_nomes_ditos') is True and not (ea_v_.get('folhas_que_anunciam_sem_a_clausula') or [])
                           and any(ea_seis_pt_ in x_ for c_, x_ in ea_folhas_ if c_.startswith('.diz')) and any(ea_seis_pt_ in x_ for c_, x_ in ea_folhas_ if c_.startswith('.limites')))
    if not ea_clausula_ok_:
        P.append('a_escala_v410: a clausula do limite do teorema do Tetelestai (ADENDO 4, D99: Z(s) soma os 2^n pixels e e lida de uma vez pelo psion; o limiar n ln 2 e o do tempo de UMA leitura; o termo que liga o tempo a maquina de Turing do Mathlib nao esta no kernel) falta ao lado de algum texto do registro que anuncia o teorema (campos: %s), ou os seis nomes de enunciado mudado (R2, B3) nao estao ditos em diz e limites' % (ea_sem_clz_[:6],))
'''
T = [('''    ea_ok_ = bool(ea_.get('all_verified') is True and ea_.get('does_not_gate_core') is True and ea_.get('runtime_executed') is True''', CLAUSULA + '''    ea_ok_ = bool(ea_clausula_ok_ and ea_.get('all_verified') is True and ea_.get('does_not_gate_core') is True and ea_.get('runtime_executed') is True''', 1),
     ('''    V['a_escala'] = {'registro': DL_.AESCALA_REGISTRO,''', '''    V['a_escala'] = {'clausula_ok': ea_clausula_ok_, 'registro': DL_.AESCALA_REGISTRO,''', 1),
     ('''tuple(DL_.DECISOES_V410) == tuple('D%d' % i_ for i_ in range(63, 63 + len(DL_.DECISOES_V410))) and DL_.DECISOES_V410[0] == 'D63' and 'D87' in DL_.DECISOES_V410''',
      '''list(DL_.DECISOES_V410) == sorted(DL_.DECISOES_V410, key=lambda k_: int(k_[1:])) and not (set(DL_.DECISOES_FORA_DO_UMPY) & set(DL_.DECISOES_V410)) and DL_.DECISOES_V410[0] == 'D63' and 'D87' in DL_.DECISOES_V410 and 'D99' in DL_.DECISOES_V410''', 1)]
aplicar("leitura_v410.py", T, base=HERE)

aplicar("registrar_mapa_v410.py", [('''all(("D%d" % i) in dec for i in range(63, 63 + len(DL_.DECISOES_V410))) and "D87" in DL_.DECISOES_V410''', '''all(k_ in dec for k_ in DL_.DECISOES_V410) and not (set(DL_.DECISOES_FORA_DO_UMPY) & set(dec)) and "D87" in DL_.DECISOES_V410 and "D99" in DL_.DECISOES_V410''', 1),
                                   ('''DEC = "%s a %s" % (DL_.DECISOES_V410[0], DL_.DECISOES_V410[-1]);''', '''DEC = DL_.DECISOES_ROTULO;''', 1)], base=HERE)

aplicar("gerar_derivacao_pos_rito_v410.py", [
    ('''a secao 6 da pedra, os registros com funcao %s -- o segundo, pre-registrado; nenhum dado observado lido --, D73 e D75; ver ADAPTACAO_09nov_SONNET.json)"
          % (DL.N_FALAS_V410, len(DL.VERBATIM_SO_O_TRECHO), DL.DECISOES_V410[0], DL.DECISOES_V410[-1],''', '''a secao 6 da pedra, os registros com funcao %s -- o segundo, pre-registrado; nenhum dado observado lido --, D73 e D75; ver ADAPTACAO_09nov_SONNET.json)"
          % (DL.N_FALAS_V410, len(DL.VERBATIM_SO_O_TRECHO), DL.DECISOES_ROTULO,''', 1),
    ('''as %d falas de 06 a 09/11 e %s a %s; ver ADAPTACAO_PARTE2_SONNET_B.json"''', '''as %d falas de 06 a 09/11 e as decisoes %s; ver ADAPTACAO_PARTE2_SONNET_B.json"''', 1),
    ('''DL.N_BUNDLE, ", ".join(DL.BUNDLE_RELS), DL.N_FALAS_V410, DL.DECISOES_V410[0], DL.DECISOES_V410[-1]))''', '''DL.N_BUNDLE, ", ".join(DL.BUNDLE_RELS), DL.N_FALAS_V410, DL.DECISOES_ROTULO))''', 1)], base=HERE)
