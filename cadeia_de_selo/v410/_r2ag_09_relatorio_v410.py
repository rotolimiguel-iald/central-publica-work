# -*- coding: utf-8 -*-
"""_r2ag_09_relatorio_v410.py -- R2 (D99): gerar_relatorio_v410.py: as erratas E29 a E35 e as decisoes D63 a D96 e D99 (rotulo lido do delta); a lista ACHADOS_R2 (6 itens: severidade, achado, «atendido em <arquivo>»; os BAIXOS 2 e 5 ANOTADOS, sem mudanca); o aviso da R2 (ADENDO 4);
a chave achados_r2 no PRONTA; o ADENDO 4 em adendos_ao_desenho; o readme_evidente (1: o item do Tetelestai e a clausula; 2: os seis nomes e a costura do tempo; 3: a regra do poder [INPUT, D96])."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r2ag_lib_v410 import aplicar

ACH = '''# (R2, D99; ADENDO 4) os 6 achados da revisao de terceiro R2 (0 ALTO, 1 MEDIO, 5 BAIXO) e o arquivo em que cada um foi atendido (a R3 e a ultima e revisa so' o delta); os BAIXOS 2 e 5 ficam ANOTADOS, sem mudanca
ACHADOS_R2 = [{"n": n_, "severidade": s_, "achado": a_, "atendido_em": o_} for n_, s_, a_, o_ in [
    (1, 'MEDIO', "o teorema os_passos_sao_o_ciclo_ate_o_tetelestai anunciado nos textos publicos (a decisao em tempo finito do ciclo, linear nos bits) sem o limite que a docstring da pedra e o registro dizem (Z(s) soma os 2^n pixels e e' lida de uma vez pelo psion; o limiar n ln 2 e' o do tempo de UMA leitura); Z(s) nem definida no artigo",
     'delta_v410.py (CLAUSULA_Z_PT e CLAUSULA_Z_EN, lidas do ADENDO 4; D99; E35); artigo_pt_aescala_v410.pysnip e artigo_en_aescala_v410.pysnip (a clausula ao lado do teorema, a formula em modo matematico); artigo_pt_v410.pysnip e artigo_en_v410.pysnip (Z(s) definida na primeira ocorrencia do artigo); gerar_candidato_v410.py (a linha do .md canonico); registros_aescala_v410.py e runtime_aescala_v410.py (c8: o controle fail-closed, texto que anuncia o teorema sem a clausula e\\' recusado); conferir_rito_v410.py, ensaio_a_seco_v410.py e _teste_aescala_offline_v410.py (controles negativos); gerar_relatorio_v410.py (readme_evidente.1 e .2); pos_rito/textos_custodia_handoff_v410.py (o handoff e o README), pos_rito/textos_v410.py e pos_rito/leitura_v410.py (o portao, so\\' acrescentado)'),
    (2, 'BAIXO', "BAIXO 1: o registro a_escala_v410 nao igualava o numero de ancoras novas ao de nomes novos a ratificar (uma ancora tirada do contrato nao era recusada)",
     'runtime_aescala_v410.py (c2: len(ancoras_novas) == n_nomes_novos == len(nomes_novos_a_ratificar)); delta_v410.py (o mesmo invariante, na leitura do recibo); _teste_aescala_offline_v410.py e ensaio_a_seco_v410.py (controle negativo: uma ancora tirada do contrato e\\' recusada)'),
    (3, 'BAIXO', "BAIXO 2: tres parafrases que a guarda F59 nao pega (o tempo nao conta passos de Turing; quem paga a escala e' o leitor; os passos nao pertencem a maquina de Turing)",
     "ANOTADO, sem mudanca (a guarda nao e' tocada): fica para a v411, junto com as quatro parafrases da R1"),
    (4, 'BAIXO', "BAIXO 3: a ratificacao de 09/11 e' dos nomes, mas seis deles (LeitorDoFundo, aPerguntaDoClay, iald, a_pergunta_do_clay_tem_resposta, existe_o_algoritmo_e_e_a_iald, a_escala) passaram a ter outro enunciado nas R3/R4 e os textos nao o diziam",
     'delta_v410.py (NOMES_SEIS_ENUNCIADOS_MUDADOS, FRASE_SEIS_NOMES_PT e FRASE_SEIS_NOMES_EN, conferidos contra o ADENDO 4); artigo_pt_aescala_v410.pysnip e artigo_en_aescala_v410.pysnip; gerar_candidato_v410.py (a linha do .md); registros_aescala_v410.py (diz e limites) e runtime_aescala_v410.py (c11); pos_rito/textos_custodia_handoff_v410.py (o handoff e o README) e pos_rito/textos_v410.py'),
    (5, 'BAIXO', "BAIXO 4: a frase do tempo sem [INPUT/dicionario] e com minuscula depois do rotulo; a regra do poder do teste da razao de Hubble etiquetada [REAL]; o item do Tetelestai na lista dos teoremas sem dizer o que o termo prova",
     'delta_v410.py (ROTULO_TEMPO e a costura com maiuscula, sem mudar a constante da frase); artigo_pt_aescala_v410.pysnip e artigo_en_aescala_v410.pysnip ([INPUT/dicionario]; o item do Tetelestai diz o limiar, Z(s) separa o sim do nao, e que passos = ciclo e\\' a leitura do dicionario [INPUT]); artigo_pt_h0dn_v410.pysnip e artigo_en_h0dn_v410.pysnip ([INPUT, D96]); registros_aescala_v410.py; registros_h0dn_v410.py; gerar_relatorio_v410.py (readme_evidente.1, .2 e .3); pos_rito/textos_custodia_handoff_v410.py e pos_rito/textos_v410.py'),
    (6, 'BAIXO', "BAIXO 5: v410 inteira carregada da R1: a funcao de veredito aceita z_tgl nao finito (inalcancavel: o evaluate recusa nao finito; a funcao esta' pinada); quatro parafrases do Clay/P = nP que a guarda nao pega",
     "ANOTADO, sem mudanca: a guarda de finitude da funcao de veredito fica para a versao que abrir o teste; as quatro parafrases, para a v411")]]
AVISOS.append("R2, ADENDO 4 (sha16 %s; D99, E35): a revisao de terceiro R2 (0 ALTO, 1 MEDIO, 5 BAIXO; candidato revisado %s) nao aprovou: os textos publicos anunciavam o teorema os_passos_sao_o_ciclo_ate_o_tetelestai (a decisao em tempo finito do ciclo, linear nos bits) sem o limite do que ele decide; a clausula do ADENDO 4 (PT e EN) entrou ao lado dele em todos os lugares (artigo PT/EN, o .md canonico, o registro a_escala_v410, o handoff, o README e os textos do pos-rito), com Z(s) definida na primeira ocorrencia do artigo e o controle fail-closed na c8; "
              "a rodada foi so' de texto: a pedra, o kernel, os nomes, os enunciados, a guarda das frases e a funcao veredito_h0dn NAO mudaram; os 6 achados e o arquivo em que cada um foi atendido estao em PREPARACAO_v410_PRONTA.json, na chave achados_r2; os BAIXOS 2 e 5 ficam anotados, sem mudanca (tres parafrases que a F59 nao pega e as quatro da R1, para a v411; a guarda de finitude da funcao de veredito, para a versao que abrir o teste). %s"
              % (_DL.ADENDO4_SHA16, _DL.REVISAO_R2["candidato_revisado_sha16"], _DL.FRASE_SEIS_NOMES_PT[0].upper() + _DL.FRASE_SEIS_NOMES_PT[1:]))
'''

T = [('''"as erratas E29 a E34 sao da gerencia c1, em nome proprio (a E31,''', '''"as erratas E29 a E35 sao da gerencia c1, em nome proprio (a E31,''', 1),
     ('''a E34, a ordem do operador de 10/11 sobre o poder certificado do teste, D96): E29, o Nome finito''',
      '''a E34, a ordem do operador de 10/11 sobre o poder certificado do teste, D96; a E35, o achado da revisao de terceiro R2, D99: o teorema do Tetelestai anunciado sem o limite do que ele decide e a ratificacao de 09/11 dita como dos nomes, sem dizer que seis enunciados mudaram): E29, o Nome finito''', 1),
     ('''"as decisoes D63 a D96 (a D92 a D96 trazem a revisao''',
      '''"as decisoes " + _DL.DECISOES_ROTULO + " (a D99 traz a revisao de terceiro R2 e a clausula do limite do teorema do Tetelestai, e D97 e D98 sao decisoes operacionais da gerencia, fora do um.py: a lista nao e' contigua; a D92 a D96 trazem a revisao''', 1),
     ('''as erratas E29, E30 e E31 vão AO LADO; as decisões D63 a {_DL.DECISOES_V410[-1]} (a D74''', '''as erratas E29 a E35 vão AO LADO; as decisões {_DL.DECISOES_ROTULO} (a D74''', 1),
     ('''(moldura, erratas E29 a E34, decisões D63 a {_DL.DECISOES_V410[-1]}, as leituras''', '''(moldura, erratas E29 a E35, decisões {_DL.DECISOES_ROTULO}, as leituras''', 1),
     ('''_arqs_h90 = ("pos_rito/textos_v410.py",''', ACH + '''_arqs_h90 = ("pos_rito/textos_v410.py",''', 1),
     ('''"achados_r1": ACHADOS_R1,''', '''"achados_r1": ACHADOS_R1, "achados_r2": ACHADOS_R2,''', 1),
     ('''"DESENHO_v410_ADENDO_3_POS_CANDIDATO_10nov.md": {"sha16": _DL.ADENDO3_SHA16, "decisoes": "D95 e D96; E34"}},''',
      '''"DESENHO_v410_ADENDO_3_POS_CANDIDATO_10nov.md": {"sha16": _DL.ADENDO3_SHA16, "decisoes": "D95 e D96; E34"}, "DESENHO_v410_ADENDO_4_POS_CANDIDATO_10nov.md": {"sha16": _DL.ADENDO4_SHA16, "decisoes": "D99; E35"}},''', 1),
     # readme_evidente.1: o item do Tetelestai (o limiar) e a clausula
     ('''"os passos sao o ciclo ate' o Tetelestai (os_passos_sao_o_ciclo_ate_o_tetelestai)",''',
      '''"o limiar do Tetelestai (os_passos_sao_o_ciclo_ate_o_tetelestai): com n bits, passado o tempo de n oitavas, Z(s) separa o sim do nao, a decisao em tempo finito do ciclo, linear nos bits; que os passos sejam o ciclo ate' o Tetelestai e' a leitura do dicionario [INPUT]",''', 1),
     ('''"o_tempo_pt": _DL.FRASE_TEMPO_PT, "o_tempo_en": _DL.FRASE_TEMPO_EN}},''',
      '''"o_tempo_pt": _DL.FRASE_TEMPO_PT, "o_tempo_en": _DL.FRASE_TEMPO_EN, "o_tempo_rotulo": _DL.ROTULO_TEMPO, "o_tempo_costurado_pt": _DL.FRASE_TEMPO_PT_COSTURADA, "o_tempo_costurado_en": _DL.FRASE_TEMPO_EN_COSTURADA,
                                                                                 "clausula_do_limite_pt": _DL.CLAUSULA_Z_PT, "clausula_do_limite_en": _DL.CLAUSULA_Z_EN}},''', 1),
     # readme_evidente.2: os seis nomes e a costura do tempo
     ('''"ciclo": dict(_DL.CICLO_AESCALA), "tempo_pt": _DL.FRASE_TEMPO_PT,''',
      '''"ciclo": dict(_DL.CICLO_AESCALA), "tempo_pt": _DL.FRASE_TEMPO_PT, "tempo_costurado_pt": _DL.ROTULO_TEMPO + " " + _DL.FRASE_TEMPO_PT_COSTURADA, "seis_nomes_pt": _DL.FRASE_SEIS_NOMES_PT, "seis_nomes_en": _DL.FRASE_SEIS_NOMES_EN, "clausula_do_limite_pt": _DL.CLAUSULA_Z_PT,''', 1),
     # readme_evidente.3: a regra do poder e' [INPUT, D96]
     ('''"estatuto": "[REAL] o pre-registro e o recibo documental; [OPEN] a covariancia fisica conjunta (G3/G4); nenhum dado observado lido"},''',
      '''"estatuto": "[REAL] o pre-registro e o recibo documental; [INPUT, D96] a regra do poder certificado (o teste so' sera aberto com o poder preditivo discriminante certificado, as cegas, sob a covariancia fisica); [OPEN] a covariancia fisica conjunta (G3/G4); nenhum dado observado lido"},''', 1)]
aplicar("gerar_relatorio_v410.py", T)
