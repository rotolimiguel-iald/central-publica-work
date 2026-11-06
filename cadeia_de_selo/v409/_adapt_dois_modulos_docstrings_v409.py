# -*- coding: utf-8 -*-
"""_adapt_dois_modulos_docstrings_v409.py -- (claude-construtor-v409) so' docstrings/comentarios do conferidor, do gerador dos ESPERADOS e do teste positivo: 2 modulos (TraducaoTuring, ParNaFaceDeFock), 82 ancoras,
20 checagens, erratas E24 a E28 e a E21 ao lado. Nenhum codigo muda (os numeros seguem lidos do DL)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
c = Arq("conferir_rito_v409.py")
c.troca("as 62 ancoras (todas), o modulo do bundle por sha256,", "as 82 ancoras (todas), os dois modulos do bundle por sha256,")
c.troca("o modelo e' o de BUNDLE PEQUENO (1 modulo novo em TGLExt/: TraducaoTuring).", "o modelo e' o de BUNDLE PEQUENO (2 modulos novos em TGLExt/: TraducaoTuring e ParNaFaceDeFock; ordem do operador: tudo na v409).")
c.grava()
g = Arq("gerar_esperados_v409.py")
g.troca("o registro novo traducao_turing_v409 (1 modulo, 62 ancoras, 17 checagens);", "o registro novo traducao_turing_v409 (2 modulos, 82 ancoras, 20 checagens);")
g.troca("bundle de 1 modulo em TGLExt/ -- TraducaoTuring --, registro com funcao traducao_turing_v409, 62 ancoras, 17 checagens)", "bundle de 2 modulos em TGLExt/ -- TraducaoTuring e ParNaFaceDeFock --, registro com funcao traducao_turing_v409, 82 ancoras, 20 checagens)")
g.troca("`estrelas_v409` (as 62 ancoras)", "`estrelas_v409` (as 82 ancoras)")
g.troca("As erratas E24 a E27 e as decisoes D55 a D61", "As erratas E24 a E28 e a E21 ao lado e as decisoes D55 a D61")
g.grava()
t = Arq("teste_conferidor_positivo_v409.py")
t.troca("o registro novo traducao_turing_v409 (62 ancoras, 1 modulo) e os herdados;", "o registro novo traducao_turing_v409 (82 ancoras, 2 modulos) e os herdados;")
t.troca("as 62 ancoras e o modulo do bundle;", "as 82 ancoras e os dois modulos do bundle;")
t.grava()
