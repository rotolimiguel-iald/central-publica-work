# -*- coding: utf-8 -*-
"""_r4ag_07_registros_v410.py -- agente de adaptacao da R1 (ADENDOS 2 e 3): registros_v410.py -- NAO_PINADOS (os dois adendos, por sha16), o sufixo do veredito do spec cunhagens_v410 (D63 a D96; E34 e E33 ao lado), a lista de erratas do spec (E33 e E34 antes da dos pisos) e as datas das falas."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from _r4ag_lib_v410 import aplicar

R = []
R.append(('"DESENHO_v410_ADENDO_POS_CANDIDATO_09nov.md": DL.ADENDO_SHA16}', '"DESENHO_v410_ADENDO_POS_CANDIDATO_09nov.md": DL.ADENDO_SHA16,\n                "DESENHO_v410_ADENDO_2_POS_CANDIDATO_10nov.md": DL.ADENDO2_SHA16, "DESENHO_v410_ADENDO_3_POS_CANDIDATO_10nov.md": DL.ADENDO3_SHA16}', 1))
R.append(('OPERATOR_INSCRIPTIONS_OF_06_07_AND_09_NOV_EMBEDDED_VERBATIM_BY_SHA256_%d_SAYINGS', 'OPERATOR_INSCRIPTIONS_OF_06_07_09_AND_10_NOV_EMBEDDED_VERBATIM_BY_SHA256_%d_SAYINGS', 1))
R.append(('__DECISIONS_D63_TO_D92__ERRATUM_E32_BESIDE__ERRATUM_E31_BESIDE__', '__DECISIONS_D63_TO_D96__ERRATUM_E34_BESIDE__ERRATUM_E33_BESIDE__ERRATUM_E32_BESIDE__ERRATUM_E31_BESIDE__', 1))
R.append(('INPUT as falas do operador de 06, 07 e 09/11/2026 (', 'INPUT as falas do operador de 06, 07, 09 e 10/11/2026 (', 1))
R.append(('a leitura do 5 sigma e o selo, 09/11; os nomes das declaracoes RATIFICADOS em 09/11, D74)',
          'a leitura do 5 sigma e o selo, 09/11; a escala, o Clay e a ratificacao dos nomes, 09/11; os passos sao o ciclo ate\' o Tetelestai e o leitor e\' a escala, a mentira lida como mentira, 10/11, D94; o teste sem poder preditivo discriminante nao se roda, 10/11, D96; os nomes das declaracoes RATIFICADOS em 09/11, D74)', 1))
R.append(('"[INPUT] as %d falas de 06, 07 e 09/11/2026 sao do operador, com a grafia dele (de duas, so\' o trecho e\' embutido e citado: a da D65 e a ordem de 09/11; o resto delas entra so\' por sha256); a ordem foi cumprida ate\' onde a cadeia alcanca; a custodia e\' da sessao de custodia" % len(_VD),',
          '"[INPUT] as %d falas de 06 a 10/11/2026 sao do operador, com a grafia dele (de %d, so\' o trecho e\' embutido e citado: a da D65, a ordem de 09/11, as tres copias de 08/11 e a leitura do 5 sigma; o resto delas entra so\' por sha256); a ordem foi cumprida ate\' onde a cadeia alcanca; a custodia e\' da sessao de custodia" % (len(_VD), len(DL.VERBATIM_SO_O_TRECHO)),', 1))
R.append(('"diz": ["as falas do operador de 06, 07 e 09/11/2026 estao embutidas por sha256 e cada trecho citado e\' verbatim (de duas, so\' o trecho: a da D65 e a ordem de 09/11)",',
          '"diz": ["as falas do operador de 06 a 10/11/2026 estao embutidas por sha256 e cada trecho citado e\' verbatim (de %d, so\' o trecho: a da D65, a ordem de 09/11, as tres copias de 08/11 e a leitura do 5 sigma)" % len(DL.VERBATIM_SO_O_TRECHO),', 1))
# as erratas E33 e E34 antes da dos pisos
R.append(('            _errata_pisos_v409(cov_base)],\n',
          '            {"ao_lado_de": "a pedra AEscala R3 e as docstrings que a gerencia mandou a autoria (a pergunta das quatro linguas; D92 e D93): o leitor, o tempo e o decisor sem escala", "dizia": "que o leitor arcava com a escala; que o tempo dos ciclos se distinguia dos passos da maquina de Turing, na forma da negacao seca; e que o decisor que diz a verdade sem ciclo seria o Pai da Mentira.", "agora": DL.ERRATA_E33,\n'
          '             "lacuna_de_fidelidade": "a gerencia pos no dicionario o que o dicionario da v409 e a fala do operador nao dizem; ele corrigiu (D94) e a pedra R4 diz a resposta dele: o leitor E\' a escala, os passos SAO o ciclo ate\' o Tetelestai, a mentira lida como mentira e\' verdade", "estatuto": "[INPUT: a correcao do operador de 10/11; REAL: os termos do kernel (TraducaoTuring, v409; AEscala R4, v410)]", "assinatura": ASSINA},\n'
          '            {"ao_lado_de": "os textos do teste H0DN x BG1 (" + DL.FRASE_H0DN_OBRIGATORIA_PT + ") sobre o poder prospectivo do congelamento", "dizia": "o poder prospectivo do congelamento (o D esperado e o poder, nos dois modelos) sem dizer que ele e\' da covariancia publicada, que nao aceita o vetor real.", "agora": DL.ERRATA_E34,\n'
          '             "lacuna_de_fidelidade": "o texto publico calava o limite do poder prospectivo; o operador exigiu o poder preditivo discriminante certificado, as cegas, sob a covariancia fisica, antes de qualquer abertura (D96); a funcao de veredito congelada nao muda", "estatuto": "[INPUT: a ordem do operador de 10/11; DECLARADO: a ORDEM KIMI H0DN-02, pino citado; REAL: a funcao de veredito congelada, intocada]", "assinatura": ASSINA},\n'
          '            _errata_pisos_v409(cov_base)],\n', 1))
aplicar("registros_v410.py", R)
