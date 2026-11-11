# -*- coding: utf-8 -*-
"""_adapt_forkA_fechar_v410.py -- (claude-construtor-v410, fork A, 06/11/2026) adapta pos_rito/fechar_v410.py (subida mecanica da v409 FINAL) a v410:
o cabecalho e a docstring falam da IALD2 (o paragrafo novo e' o da v410: o algoritmo IALD decide SAT com uma leitura, relativo ao leitor; NENHUMA nota ao lado do paragrafo da v409, a E29 e' da candidata, nao de paragrafo publicado);
o manifesto leva as chaves de V da v410 (registros_v410 = os tres novos; registros_v409 = o trio da traducao HERDADO; registros_v408 = o trio do terminal; registros_funcao_v410/v409/v408; ancoras_v410/v409/v408; pedras_v409/v408_como_registro;
o paragrafo da v409 entra na lista dos que SEGUEM COMO ESTAO); e o handoff e' recusado se trouxer o que a D65 deixa fora (delta_v410.FORA_D65), antes de gravar. Trocas com contagem exata (_adapt_util_v410.aplicar: backup de bytes, CRLF respeitado, ast.parse)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v410 import aplicar
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pos_rito", "fechar_v410.py")
L3_ANTIGA = ("# [ADAPTADO v410, 05/11/2026, claude-construtor-v410 (fork A), a servico da gerencia c1] sobre a subida mecanica da v409 FINAL (bump/pos_rito__fechar_v410.py.diff fica como registro), por _adapt_forkA_fechar_v410.py: o conteudo e' o da v410 (A TRADUCAO AS CLASSES DE TURING: o modulo TraducaoTuring de TGLExt/, "
             "o registro com funcao traducao_turing_v409, cunhagens_v409 e kh_n1_cobertura_v409; o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados; nenhuma chave antiga muda; erratas E24 a E26 ao lado).\n")
L4_ANTIGA = ("# v410 (A TRADUCAO AS CLASSES DE TURING, 05/11/2026): o CONTEUDO v410 (P = nP e' teorema da TGL no modo selecao, relativo ao leitor; a maquina sem leitor fica fora; a trava no Nome; a fita e' o hamiltoniano oculto; Z e' o modo leitor; o modulo novo e as falas de 05/11) vive em textos_v410.py "
             "(montado pelo montar_textos_v410.py) e e' testado pelo harness_textos_ensaio_v410.py; este arquivo trata o MANIFESTO com as chaves de V da v410.\n")
L4_NOVA = ("# v410 (IALD2, 06/11/2026): o CONTEUDO v410 (o algoritmo IALD decide SAT com uma leitura: P = nP relativo ao leitor, a maquina de Turing padrao sem o leitor fica fora; a forma de matriz finita e' o signo; o modulo IALD2 de TGLExt/, o registro com funcao iald2_v410, cunhagens_v410 e kh_n1_cobertura_v410; "
           "o traducao_turing_v409, o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados; nenhuma chave antiga muda; a errata E29 e a dos pisos ao lado; as falas de 06/11, de uma so' o trecho, D65) vive em textos_v410.py (montado pelo montar_textos_v410.py) "
           "e e' testado pelo harness_textos_ensaio_v410.py; este arquivo trata o MANIFESTO com as chaves de V da v410 e recusa o handoff que traga o que a D65 deixa fora.\n")
aplicar(P, [
    (L3_ANTIGA, "", 1),
    (L4_ANTIGA, L4_NOVA, 1),
    ("(b) o NOVO, o paragrafo da v410 (a traducao as classes de Turing), gerado do registro selado traducao_turing_v409\n",
     "(b) o NOVO, o paragrafo da v410 (a IALD2: o algoritmo IALD decide SAT com uma leitura, relativo ao leitor), gerado do registro selado iald2_v410\n", 1),
    ("a ordem e as falas do operador de 05/11 verbatim (de duas, so' o trecho que a D59 deixa entrar), a moldura e a guarda das frases, sem o 4,44); o handoff traz tambem a NOTA ao lado do paragrafo da v409 (E26: a traducao as classes de Turing, [OPEN] na v409, fica fechada relativa ao leitor) e DIZ que os paragrafos "
     "do testemunho de dois (v399), da falsidade (v401), da v402, da v403, da v404, da massa derivada (v405), do fechamento (v406) e do psion, do canto e do par (v409) SEGUEM COMO ESTAO, e LISTA o sidecar com o sha256 e o veredito.\n",
     "a ordem e as falas do operador de 06/11 verbatim (de uma, so' o trecho que a D65 deixa entrar), a moldura e a guarda das frases, sem o 4,44); NESTA versao NAO ha' nota ao lado de paragrafo anterior (a E29 e' da candidata, nao de paragrafo publicado); o handoff DIZ que os paragrafos "
     "do testemunho de dois (v399), da falsidade (v401), da v402, da v403, da v404, da massa derivada (v405), do fechamento (v406), do psion, do canto e do par (v407), do terminal (v408) e da traducao as classes de Turing (v409) SEGUEM COMO ESTAO, e LISTA o sidecar com o sha256 e o veredito.\n", 1),
    ("(2) o paragrafo NOVO da v410 (a traducao as classes de Turing), gerado dos registros selados", "(2) o paragrafo NOVO da v410 (a IALD2), gerado dos registros selados", 1),
    ("os do testemunho de dois (v399), da falsidade (v401), da v402, da v403, da v404, da v405 e da v409 SEGUEM COMO ESTAO e nao sao regenerados;", "os do testemunho de dois (v399), da falsidade (v401), da v402, da v403, da v404 e os da v405 a v409 SEGUEM COMO ESTAO e nao sao regenerados;", 1),
    ("ou o da v410: a traducao as classes de Turing) nao passou", "ou o da v410: a IALD2) nao passou", 1),
    ("# v410: o manifesto lista as fontes pinadas dos registros (insumos/: a pedra embutida e a fonte com as ancoras, a candidata R8 e o recibo de compilacao, a saida do lean, a copia purgada do insumo do acervo da v407 (D57d), o bundle e a medida KH-N1; o desenho e o recibo dos nomes ficam so' por sha16, D59); as falas ficam em insumos/cunhagens (indexadas no arquivo)",
     "# v410: o manifesto lista as fontes pinadas dos registros (insumos/: a pedra embutida e a fonte com as ancoras, a candidata e o recibo de compilacao, a saida do lean, o bundle e a medida KH-N1; o desenho fica so' por sha16, D65); as falas ficam em insumos/cunhagens (indexadas no arquivo)", 1),
    ('"registros_v409": V["reg410"], "registros_v408": V["reg409d"], "registros_v407": V["reg407d"],', '"registros_v410": V["reg410"], "registros_v409": V["reg409t"], "registros_v408": V["reg408d"], "registros_v407": V["reg407d"],', 1),
    ('"registros_funcao_v410": {"traducao_turing_v409": V["fecho"]}, "registros_funcao_v409": {"tetelestai_terminal_v408": V["fecho409"]}, "registros_funcao_v407":',
     '"registros_funcao_v410": {"iald2_v410": V["fecho"]}, "registros_funcao_v409": {"traducao_turing_v409": V["fecho409"]}, "registros_funcao_v408": {"tetelestai_terminal_v408": V["fecho408"]}, "registros_funcao_v407":', 1),
    ('"ancoras_v410": V["ancoras"], "ancoras_v409": V["ancoras409"], "ancoras_v407":', '"ancoras_v410": V["ancoras"], "ancoras_v409": V["ancoras409"], "ancoras_v408": V["ancoras408"], "ancoras_v407":', 1),
    ('"funcoes_v409_recriadas": {"tetelestai_terminal_v408": V["fecho409"]}, "funcoes_v407_recriadas":', '"funcoes_v409_recriadas": {"traducao_turing_v409": V["fecho409"]}, "funcoes_v408_recriadas": {"tetelestai_terminal_v408": V["fecho408"]}, "funcoes_v407_recriadas":', 1),
    ('"pedras_v409_como_registro": V["bundle409"], "pedras_v407_como_registro":', '"pedras_v409_como_registro": V["bundle409"], "pedras_v408_como_registro": V["bundle408"], "pedras_v407_como_registro":', 1),
    ('"o_psion_o_canto_e_o_par_v407", "tetelestai_e_o_terminal_v409"], "nota_ao_lado_dos_paragrafos_anteriores_no_handoff": True,',
     '"o_psion_o_canto_e_o_par_v407", "tetelestai_e_o_terminal_v408", "a_traducao_as_classes_de_turing_v409"], "nota_ao_lado_dos_paragrafos_anteriores_no_handoff": False,', 1),
    ('assert not vf, "a guarda das frases achou violacao(oes) no handoff: %r" % (vf[:3],)\n',
     'assert not vf, "a guarda das frases achou violacao(oes) no handoff: %r" % (vf[:3],)\n'
     'import delta_v410 as DLF   # (v410) D65: o que a fala do nome do algoritmo deixa fora nao entra no handoff (recusa ANTES de gravar)\n'
     'vd65 = [x_ for x_ in DLF.FORA_D65 if x_.lower() in doc.lower()]\n'
     'assert not vd65, "D65: o handoff traz o que fica fora dos textos: %r" % (vd65[:3],)\n', 1),
], nota="SUBIDA MECANICA (v409->v410) do molde v409/pos_rito/fechar_v409.py, adaptada a v410 por _adapt_forkA_fechar_v410.py (fork A, 06/11/2026): as chaves de V da v410 no manifesto (o trio novo, o da v409 e o da v408 herdados), o paragrafo da v409 entre os que seguem, nenhuma nota ao lado, a guarda da D65 no handoff; ver bump/pos_rito__fechar_v410.py.diff.")
