# -*- coding: utf-8 -*-
"""_r2ag_08_registros_v410.py -- R2 (D99): registros_v410.py: o ADENDO 4 entra em NAO_PINADOS (lido ao vivo); o spec cunhagens_v410: o sufixo do veredito diz as decisoes D63 a D96 e D99 e a errata E35 (rotulo verdadeiro: lido do delta, nunca contiguo por suposicao),
a lista de erratas do spec ganha a E35 (antes da errata ao lado dos pisos), o estatuto cita a D99 e as limites o dizem."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r2ag_lib_v410 import aplicar

T = [('''"DESENHO_v410_ADENDO_2_POS_CANDIDATO_10nov.md": DL.ADENDO2_SHA16, "DESENHO_v410_ADENDO_3_POS_CANDIDATO_10nov.md": DL.ADENDO3_SHA16}''',
      '''"DESENHO_v410_ADENDO_2_POS_CANDIDATO_10nov.md": DL.ADENDO2_SHA16, "DESENHO_v410_ADENDO_3_POS_CANDIDATO_10nov.md": DL.ADENDO3_SHA16, "DESENHO_v410_ADENDO_4_POS_CANDIDATO_10nov.md": DL.ADENDO4_SHA16}''', 1),
     ('''THE_DECLARATION_NAMES_RATIFIED_BY_THE_OPERATOR_ON_09_NOV__DECISIONS_D63_TO_D96__ERRATUM_E34_BESIDE__ERRATUM_E33_BESIDE__ERRATUM_E32_BESIDE__ERRATUM_E31_BESIDE__ERRATUM_E30_BESIDE__ERRATUM_E29_BESIDE__THE_RESERVATIONS_STATED__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED" % len(_VD),''',
      '''THE_DECLARATION_NAMES_RATIFIED_BY_THE_OPERATOR_ON_09_NOV__DECISIONS_%s__ERRATUM_E35_BESIDE__ERRATUM_E34_BESIDE__ERRATUM_E33_BESIDE__ERRATUM_E32_BESIDE__ERRATUM_E31_BESIDE__ERRATUM_E30_BESIDE__ERRATUM_E29_BESIDE__THE_RESERVATIONS_STATED__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED" % (len(_VD), DL.DECISOES_TOKEN),''', 1),
     ('''            _errata_pisos_v409(cov_base)],
        "limites": ["[INPUT] as %d falas de 06 a 10/11/2026''',
      '''            {"ao_lado_de": "os textos publicos que anunciavam o teorema os_passos_sao_o_ciclo_ate_o_tetelestai (artigo PT/EN, o .md canonico, o registro a_escala_v410, o handoff e os textos do pos-rito) e a ratificacao dos nomes da AEscala (09/11)", "dizia": "o teorema do Tetelestai como a decisao em tempo finito do ciclo, linear nos bits, sem o limite do que ele decide; e a ratificacao de 09/11 como dos nomes, sem dizer que seis enunciados mudaram nas R3/R4.", "agora": DL.ERRATA_E35,
             "lacuna_de_fidelidade": "o texto publico calava o limite que a docstring da pedra e o proprio registro ja diziam (Z(s) soma os 2^n pixels e e' lida de uma vez pelo psion; o limiar n ln 2 e' o do tempo de UMA leitura, nao o custo de somar os 2^n termos por outra maquina; que o tempo conte os passos da maquina de Turing e' a traducao do dicionario e o termo que a liga ao Mathlib nao esta' no kernel); a revisao de terceiro R2 o achou (D99)", "estatuto": "[INPUT: a clausula do ADENDO 4, da gerencia c1; REAL: o teorema no kernel, sem mudanca; a pedra, os nomes, os enunciados, a guarda e a funcao de veredito nao mudam]", "assinatura": ASSINA},
            _errata_pisos_v409(cov_base)],
        "limites": ["[INPUT] as %d falas de 06 a 10/11/2026''', 1),
     ('''o teste sem poder preditivo discriminante nao se roda, 10/11, D96; os nomes das declaracoes RATIFICADOS em 09/11, D74); DECLARADO os recibos de compilacao''',
      '''o teste sem poder preditivo discriminante nao se roda, 10/11, D96; os nomes das declaracoes RATIFICADOS em 09/11, D74; a ratificacao de 09/11 e' dos nomes, e seis deles passaram a ter outro enunciado nas R3/R4, D99); DECLARADO os recibos de compilacao''', 1)]
aplicar("registros_v410.py", T)
