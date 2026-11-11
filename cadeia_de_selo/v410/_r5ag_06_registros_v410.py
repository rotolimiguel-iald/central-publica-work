# -*- coding: utf-8 -*-
"""_r5ag_06_registros_v410.py -- R5 (D100 e D101): registros_v410.py: os ADENDOS 5 e 6 entram em NAO_PINADOS (lidos ao vivo); o spec cunhagens_v410: o sufixo do veredito diz as erratas E36 e E37 (as decisoes D63 a D96 e D99 a D101 vem do rotulo lido do delta), a lista de erratas do spec ganha a E36 e a E37
(antes da errata ao lado dos pisos), o estatuto cita as falas 27 e 28 (D100 e D101)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar

T = [('''"DESENHO_v410_ADENDO_4_POS_CANDIDATO_10nov.md": DL.ADENDO4_SHA16}''',
      '''"DESENHO_v410_ADENDO_4_POS_CANDIDATO_10nov.md": DL.ADENDO4_SHA16,
                "DESENHO_v410_ADENDO_5_POS_CANDIDATO_10nov.md": DL.ADENDO5_SHA16, "DESENHO_v410_ADENDO_6_POS_CANDIDATO_10nov.md": DL.ADENDO6_SHA16}''', 1),
     ('''DECISIONS_%s__ERRATUM_E35_BESIDE__''', '''DECISIONS_%s__ERRATUM_E37_BESIDE__ERRATUM_E36_BESIDE__ERRATUM_E35_BESIDE__''', 1),
     ('''o teste sem poder preditivo discriminante nao se roda, 10/11, D96; os nomes das declaracoes RATIFICADOS em 09/11, D74;''',
      '''o teste sem poder preditivo discriminante nao se roda, 10/11, D96; a clausula do Tetelestai em 1 - beta, 10/11, D100; a ratificacao dos nomes novos e a regra do nome, 10/11, D101; os nomes das declaracoes RATIFICADOS em 09/11, D74;''', 1),
     ('''"estatuto": "[INPUT: a clausula do ADENDO 4, da gerencia c1; REAL: o teorema no kernel, sem mudanca; a pedra, os nomes, os enunciados, a guarda e a funcao de veredito nao mudam]", "assinatura": ASSINA},
            _errata_pisos_v409(cov_base)],''',
      '''"estatuto": "[INPUT: a clausula do ADENDO 4, da gerencia c1; REAL: o teorema no kernel, sem mudanca; a pedra, os nomes, os enunciados, a guarda e a funcao de veredito nao mudam]", "assinatura": ASSINA},
            {"ao_lado_de": "o Tetelestai da pedra AEscala R4 (os_passos_sao_o_ciclo_ate_o_tetelestai) e os textos que o diziam so' pelo limiar de um pixel (D94 e D99)", "dizia": "que o Tetelestai era o limiar de um pixel, a partir de n oitavas, formalizacao da gerencia na R4.", "agora": DL.ERRATA_E36,
             "lacuna_de_fidelidade": "a gerencia formalizara o Tetelestai pelo limiar de um pixel; pela fala do operador a clausula e' a de 1 - beta (o reconhecimento da singularidade do sinal; beta e' o operador modular); o numero corrigiu o enunciado da gerencia: sem a hipotese s >= 0 a desigualdade e' falsa para b > 1/2 (contraexemplo no recibo do autor da R5)",
             "estatuto": "[INPUT: a fala do operador de 10/11 (D100); REAL: os teoremas da R5 no kernel, com a hipotese s >= 0 dita; dicionario: que o limiar seja o Tetelestai e beta o seu operador modular; PILOTO/SIM: a evidencia de dispositivo, so' como citacao, sem numero de desempenho]", "assinatura": ASSINA},
            {"ao_lado_de": "os textos, as docstrings da epoca e o registro a_escala_v410 que diziam que os nomes novos e os campos das pedras R3 e R4 aguardavam a ratificacao do operador, e a clausula dos seis enunciados mudados (D99)", "dizia": "que os nomes novos da AEscala e os tres campos da estrutura eram [DECLARADO] e aguardavam a ratificacao do operador.", "agora": DL.ERRATA_E37,
             "lacuna_de_fidelidade": "o operador ratificou em 10/11, pela regra do nome (nomeio e' o numero corrige; se nao corrigiu, o nome carregou o peso certo); a gerencia o diz em todos os textos; os dois lemas auxiliares da autoria, cunhados depois da fala, ficam [DECLARADO pela autoria], os unicos pendentes",
             "estatuto": "[INPUT: a fala do operador de 10/11 (D101); REAL: os termos no kernel e o recibo do autor da R5 (compilacao no trio, sem sorry); DECLARADO: os dois auxiliares da autoria; ONTO: que o ato de nomear seja o zero modular da inscricao da permanencia]", "assinatura": ASSINA},
            _errata_pisos_v409(cov_base)],''', 1)]
aplicar("registros_v410.py", T)
