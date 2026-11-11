# -*- coding: utf-8 -*-
"""_r4ag_10_conferidores_v410.py -- agente de adaptacao da R1 (R4, ADENDOS 2 e 3): os conferidores da raiz sem contagem digitada: conferir_rito_v410.py (erratas lidas de DL.ERRATAS_V410; falas e decisoes lidas), gerar_esperados_v410.py (a mensagem do assert),
p00_precondicoes_v410.py (a prosa da checagem das falas) e o cabecalho de rito_v410.sh (comentario; o corpo do rito NAO muda)."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from _r4ag_lib_v410 import aplicar

C = []
C.append(('as %d falas de 06 a 09/11 embutidas por sha256 (embedded_ok e sha256 == os ESPERADOS; todas do operador; de algumas, so\' o trecho: D65 e as de DL.VERBATIM_SO_O_TRECHO); as erratas E29, E30, E31 e E32 e a dos pisos (em nome proprio da gerencia c1) e as decisoes D63 a D92 estao no registro;',
          'as %d falas de 06 a 10/11 embutidas por sha256 (embedded_ok e sha256 == os ESPERADOS; todas do operador; de algumas, so\' o trecho: D65 e as de DL.VERBATIM_SO_O_TRECHO); as erratas da v410 (DL.ERRATAS_V410, E29 em diante) e a dos pisos (em nome proprio da gerencia c1) e as decisoes de ESPERADOS[decisoes_v410_ids] (D63 em diante) estao no registro;', 1))
C.append(('for n_ in (29, 30, 31, 32))', 'for n_ in range(29, 29 + len(DL.ERRATAS_V410)))', 1))
C.append(('\n# [ADAPTADO v410 PARTE 2, 09/11/2026 (~18h)', '\n# [ADAPTADO v410 R1/R4, 10/11/2026, agente de adaptacao, a servico do construtor claude-construtor-v410] as falas (DL.N_FALAS_V410: 06 a 10/11), as decisoes (D63 em diante: ESPERADOS[decisoes_v410_ids]) e as erratas (E29 em diante: DL.ERRATAS_V410) sao LIDAS do delta e dos ESPERADOS; nenhuma contagem digitada; a prosa abaixo, da epoca da R3, fica como registro\n# [ADAPTADO v410 PARTE 2, 09/11/2026 (~18h)', 1))
aplicar("conferir_rito_v410.py", C)

G = []
G.append(('"D63 a D92 (a ultima e\' a de DL.DECISOES_V410[-1]), E29, E30, E31 e E32, as ressalvas"', '"as decisoes de D63 a DL.DECISOES_V410[-1], as erratas de E29 em diante (DL.ERRATAS_V410) e as ressalvas"', 1))
G.append(('# ---- as falas (DL.N_FALAS_V410, por sha256), as decisoes (D63 a D92) e as erratas (E29, E30, E31, E32): o candidato == o delta == os registros', '# ---- as falas (DL.N_FALAS_V410, por sha256), as decisoes (D63 a DL.DECISOES_V410[-1]) e as erratas (E29 em diante: DL.ERRATAS_V410): o candidato == o delta == os registros', 1))
aplicar("gerar_esperados_v410.py", G)

P = []
P.append(('as %d falas de 06 a 09/11 tem os prefixos', 'as %d falas de 06 a 10/11 tem os prefixos', 1))
aplicar("p00_precondicoes_v410.py", P)

S = []
S.append(('#!/bin/sh\n', '#!/bin/sh\n# [ADAPTADO v410 R1/R4, 10/11/2026, agente de adaptacao, a servico do construtor claude-construtor-v410] so\' o texto descritivo do cabecalho; o corpo do rito NAO muda: com a pedra AEscala R4 (o leitor E\' a escala; os passos sao o ciclo ate\' o Tetelestai), o registro a_escala_v410 le TODAS as ancoras, bandeiras, falas e o ciclo do contrato (lidos do delta, do FLAGS e dos ESPERADOS); as falas sao as de 06 a 10/11 (DL.N_FALAS_V410), as decisoes de D63 em diante (ate\' DL.DECISOES_V410[-1]) e as erratas de E29 em diante (DL.ERRATAS_V410); o teste H0DN (pré-registrado; nenhum dado observado lido) so\' sera aberto com o poder certificado (D96); os numeros do cabecalho abaixo sao da epoca da R3 e ficam como registro\n', 1))
aplicar("rito_v410.sh", S)
