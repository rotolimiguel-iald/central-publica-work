# -*- coding: utf-8 -*-
"""_adapt_forkA_fechar_v409.py -- (claude-construtor-v409, fork A, 05/11/2026) adapta fechar_v409.py (subida mecanica da v408) a v409, A TRADUCAO AS CLASSES DE TURING:
o cabecalho e o manifesto com as chaves de V da leitura_v409 (registros_v409/v408/v407/v406; registros_funcao_v409 = traducao, v408 = tetelestai herdado, v407 = psion herdado, v406 = fechamento herdado; ancoras, bandeiras e bundles por versao);
os paragrafos anteriores que seguem como estao (+ Tetelestai e' o terminal, v408). Trocas com contagem exata (_adapt_util_v409.Arq)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("pos_rito/fechar_v409.py")
ls = a.t.split("\n")
assert ls[1].startswith("# [A ADAPTAR v409]") and ls[2].startswith("# [ADAPTADO v409, 04/11/2026, claude-construtor-v409 (fork B)]") and ls[3].startswith("# v409 (TETELESTAI E' O TERMINAL, 04/11/2026)")
ls[1] = ("# [ADAPTADO v409, 05/11/2026, claude-construtor-v409 (fork A), a servico da gerencia c1] sobre a subida mecanica da v408 FINAL (bump/pos_rito__fechar_v409.py.diff fica como registro), por _adapt_forkA_fechar_v409.py: o conteudo e' o da v409 "
         "(A TRADUCAO AS CLASSES DE TURING: o modulo TraducaoTuring de TGLExt/, o registro com funcao traducao_turing_v409, cunhagens_v409 e kh_n1_cobertura_v409; o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados; nenhuma chave antiga muda; erratas E24 a E26 ao lado).")
ls[2] = ("# v409 (A TRADUCAO AS CLASSES DE TURING, 05/11/2026): o CONTEUDO v409 (P = nP e' teorema da TGL no modo selecao, relativo ao leitor; a maquina sem leitor fica fora; a trava no Nome; a fita e' o hamiltoniano oculto; Z e' o modo leitor; o modulo novo e as falas de 05/11) vive em textos_v409.py "
         "(montado pelo montar_textos_v409.py) e e' testado pelo harness_textos_ensaio_v409.py; este arquivo trata o MANIFESTO com as chaves de V da v409.")
del ls[3]
a.t = "\n".join(ls)
a.troca("(b) o NOVO, o paragrafo da v409 (Tetelestai e' o terminal), gerado do registro selado tetelestai_terminal_v408", "(b) o NOVO, o paragrafo da v409 (a traducao as classes de Turing), gerado do registro selado traducao_turing_v409")
a.troca("a ordem e as decisoes do operador de 04/11 verbatim", "a ordem e as falas do operador de 05/11 verbatim (de duas, so' o trecho que a D59 deixa entrar)")
a.troca("o handoff traz tambem a NOTA ao lado do paragrafo da v408 (E21: o [OPEN] do par na face de Fock e' de ligacao, nao de ausencia de termo)", "o handoff traz tambem a NOTA ao lado do paragrafo da v408 (E26: a traducao as classes de Turing, [OPEN] na v408, fica fechada relativa ao leitor)")
a.troca("(2) o paragrafo NOVO da v409 (Tetelestai e' o terminal), gerado dos registros sela", "(2) o paragrafo NOVO da v409 (a traducao as classes de Turing), gerado dos registros sela")
a.troca("ou o da v409: Tetelestai e' o terminal) nao passou nas verificacoes", "ou o da v409: a traducao as classes de Turing) nao passou nas verificacoes")
a.troca('"registros_v408": V["reg409"], "registros_v407": V["reg408d"], "registros_v406": V.get("reg406d"),',
        '"registros_v409": V["reg409"], "registros_v408": V["reg408d"], "registros_v407": V["reg407d"], "registros_v406": V.get("reg406d"),')
a.troca('"registros_funcao_v409": {"tetelestai_terminal_v408": V["fecho"]}, "registros_funcao_v408": {"psion_canto_v407": V["fecho408"]}, "registros_funcao_v406": {"fechamento_v406": V.get("fecho406")}, "ancoras_v409": V["ancoras"], "ancoras_v408": V["ancoras408"], "ancoras_v406": V.get("ancoras406"), "bandeiras_v409": V["bandeiras"], "bandeiras_v408": V["bandeiras408"], "bandeiras_v406": V.get("bandeiras406"), "chaves_v407": V["chaves408"], "chaves_v406": V.get("chaves406"),',
        '"registros_funcao_v409": {"traducao_turing_v409": V["fecho"]}, "registros_funcao_v408": {"tetelestai_terminal_v408": V["fecho408"]}, "registros_funcao_v407": {"psion_canto_v407": V["fecho407"]}, "registros_funcao_v406": {"fechamento_v406": V.get("fecho406")}, "ancoras_v409": V["ancoras"], "ancoras_v408": V["ancoras408"], "ancoras_v407": V["ancoras407"], "ancoras_v406": V.get("ancoras406"), "bandeiras_v409": V["bandeiras"], "bandeiras_ate_v408": V["bandeiras408"], "chaves_v407": V["chaves407"], "chaves_v406": V.get("chaves406"),')
a.troca('"funcoes_v408_recriadas": {"psion_canto_v407": V["fecho408"]}, "funcoes_v406_recriadas": {"fechamento_v406": V.get("fecho406")},',
        '"funcoes_v408_recriadas": {"tetelestai_terminal_v408": V["fecho408"]}, "funcoes_v407_recriadas": {"psion_canto_v407": V["fecho407"]}, "funcoes_v406_recriadas": {"fechamento_v406": V.get("fecho406")},')
a.troca('"pedras_v408_como_registro": V["bundle408"], "pedras_v406_como_registro": V.get("bundle406"),', '"pedras_v408_como_registro": V["bundle408"], "pedras_v407_como_registro": V["bundle407"], "pedras_v406_como_registro": V.get("bundle406"),')
a.troca('"o_fechamento_v406", "o_psion_o_canto_e_o_par_v408"]', '"o_fechamento_v406", "o_psion_o_canto_e_o_par_v407", "tetelestai_e_o_terminal_v408"]')
a.troca("# v409: o manifesto lista as fontes pinadas dos registros (insumos/: os quatro modulos e as candidatas de origem, os recibos de compilacao, a afericao do traco e do dicionario, a copia purgada do insumo do acervo e o recibo da purga, o recibo dos nomes, o desenho, o bundle e a medida KH-N1)",
        "# v409: o manifesto lista as fontes pinadas dos registros (insumos/: a pedra embutida e a fonte com as ancoras, a candidata R8 e o recibo de compilacao, a saida do lean, a copia purgada do insumo do acervo da v407 (D57d), o bundle e a medida KH-N1; o desenho e o recibo dos nomes ficam so' por sha16, D59)")
a.grava()
