# -*- coding: utf-8 -*-
"""_adapt_forkA_harness_fechar_v409.py -- (claude-construtor-v409, fork A, 05/11/2026) adapta harness_fechar_sandbox_v409.py (subida mecanica da v408, adaptada pelo fork B em 04/11 ao conteudo da v408) a v409, A TRADUCAO AS CLASSES DE TURING:
MAN_CHAVES (as chaves do manifesto que o fechar_v409 grava), os stubs (TOPICO_NOVO, REGS), os controles negativos do fechar (a traducao; o terminal, o psion e o fechamento HERDADOS; E24 a E26; D55 a D60; a leitura de 05/11; a E26 ao lado de cunhagens_v408 e a D57(d) ao lado de cunhagens_v407),
o espelho da casa (D59: nenhum nome de arquivo com o que fica fora entra no resumo; so' a contagem), as descricoes e o veredito. Trocas com contagem exata (_adapt_util_v409.Arq)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("pos_rito/harness_fechar_sandbox_v409.py")
ls = a.t.split("\n")
assert ls[1].startswith("# [A ADAPTAR v409]") and ls[2].startswith("# [ADAPTADO v409, 04/11/2026, claude-construtor-v409 (fork B)]")
ls[1] = ("# [ADAPTADO v409, 05/11/2026, claude-construtor-v409 (fork A), a servico da gerencia c1] sobre a subida mecanica de rotulo da v408 FINAL (bump/ fica como registro) e a adaptacao do fork B de 04/11, por _adapt_forkA_harness_fechar_v409.py: o conteudo e' o da v409 "
         "(A TRADUCAO AS CLASSES DE TURING: UM modulo novo, o registro com funcao traducao_turing_v409, o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 HERDADOS e recriados, nenhuma chave antiga muda); MAN_CHAVES, os stubs e os controles negativos sao os da v409; "
         "a montagem do sandbox (as pastas irmas, o BUNDLE_v406 com origem_integracao, o espelho da casa medido na importacao do delta) fica a do fork B; a gerencia revisa antes do rito (nao e' versao selada).")
del ls[2]
a.t = "\n".join(ls)
a.troca("Derivado do harness_fechar_sandbox_v408.py (que rodou na v408), adaptado a v409 por _adapt_harness_fechar_v409.py (claude-construtor-v409, fork B, 04/11/2026): Tetelestai e' o terminal (o bundle de quatro modulos, o registro tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados, nenhuma chave antiga muda; o passo simples B17 -> B18).",
        "Derivado do harness_fechar_sandbox_v408.py (que rodou na v408), adaptado a v409 (fork B, 04/11; fork A, 05/11/2026): a traducao as classes de Turing (UM modulo novo, o registro traducao_turing_v409; o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados, nenhuma chave antiga muda; o passo simples B17 -> B18).")
a.troca("o da v409 (Tetelestai e' o terminal)\nigual ao gerado do core e aprovado por T.verificar_paragrafo_v409) e a NOTA ao lado dos paragrafos anteriores entre os seus marcadores, a frase de que os paragrafos do testemunho de dois, da falsidade e da v408 SEGUEM COMO ESTAO",
        "o da v409 (a traducao as classes de Turing)\nigual ao gerado do core e aprovado por T.verificar_paragrafo_v409) e a NOTA ao lado do paragrafo da v408 (E26) entre os seus marcadores, a frase de que os paragrafos do testemunho de dois, da falsidade e das versoes anteriores SEGUEM COMO ESTAO")
a.troca("com um numero do tetelestai_terminal_v408, do psion_canto_v407 (herdado) ou do fechamento_v406 (herdado) adulterado, com uma chave antiga dita mudada,\n"
        "com a direcao do testemunho invertida, com uma inscricao de 04/11 nao embutida, com a leitura de 04/11 dita REAL, com a errata E21 ou a decisao D54 a menos (e com a E21 ao lado da cunhagens_v407 herdada ausente),",
        "com um numero do traducao_turing_v409, do tetelestai_terminal_v408 (herdado), do psion_canto_v407 (herdado) ou do fechamento_v406 (herdado) adulterado, com uma chave antiga dita mudada,\n"
        "com a direcao do testemunho invertida, com uma inscricao de 05/11 nao embutida, com a leitura de 05/11 dita REAL, com a errata E24 ou a decisao D56 a menos (e com a E26 ao lado da cunhagens_v408 ou a errata da D57(d) ao lado da cunhagens_v407, herdadas, ausente),")

# ---------------------------------------------------------------- MAN_CHAVES (o manifesto que o fechar_v409 grava)
a.troca_re(r"^# v409: as chaves do MANIFESTO de incorporacao que fechar_v409\.py grava \(nomes versionados: [^\n]*$",
           "# v409: as chaves do MANIFESTO de incorporacao que fechar_v409.py grava (nomes versionados: *_v409 = os registros desta versao (traducao_turing_v409 e os dois specs); *_v408 = os HERDADOS da v408 (tetelestai_terminal_v408 e os dois specs); *_v407 = os da v407 (psion_canto_v407 e os dois specs); *_v406 = o fechamento_v406 e os dois specs; *_v405 = os treze da v405 selada, e assim por diante; SEM chaves_v409: nenhuma chave antiga muda)")
a.troca('MAN_CHAVES = ("registros_v408", "registros_v407", "registros_v406", "registros_v405", "registros_v404", "registros_v403", "registros_v402", "registros_v401", "registros_v399", "registros_funcao_v409", "registros_funcao_v408", "registros_funcao_v406", "ancoras_v409", "ancoras_v408", "ancoras_v406", "bandeiras_v409", "bandeiras_v408", "bandeiras_v406", "chaves_v407", "chaves_v406", "f2b_errata", "bandeiras_do_gate_recriado",\n'
        '              "funcoes_v408_recriadas", "funcoes_v406_recriadas", "funcoes_v405_recriadas", "funcoes_v403_recriadas", "funcoes_v402_recriadas", "pedras_v408_como_registro", "pedras_v406_como_registro", "pedras_v405_como_registro",',
        'MAN_CHAVES = ("registros_v409", "registros_v408", "registros_v407", "registros_v406", "registros_v405", "registros_v404", "registros_v403", "registros_v402", "registros_v401", "registros_v399", "registros_funcao_v409", "registros_funcao_v408", "registros_funcao_v407", "registros_funcao_v406", "ancoras_v409", "ancoras_v408", "ancoras_v407", "ancoras_v406", "bandeiras_v409", "bandeiras_ate_v408", "chaves_v407", "chaves_v406", "f2b_errata", "bandeiras_do_gate_recriado",\n'
        '              "funcoes_v408_recriadas", "funcoes_v407_recriadas", "funcoes_v406_recriadas", "funcoes_v405_recriadas", "funcoes_v403_recriadas", "funcoes_v402_recriadas", "pedras_v408_como_registro", "pedras_v407_como_registro", "pedras_v406_como_registro", "pedras_v405_como_registro",')

# ---------------------------------------------------------------- os stubs
a.troca("TOPICO_NOVO = 'v409-selada-tetelestai-e-o-terminal.md'\nREGS = 'tetelestai_terminal_v408 cunhagens_v408 kh_n1_cobertura_v408'", "TOPICO_NOVO = 'v409-selada-traducao-turing.md'\nREGS = 'traducao_turing_v409 cunhagens_v409 kh_n1_cobertura_v409'")
a.troca("TOPICO_NOVO = \\'v409-selada-tetelestai-e-o-terminal.md\\'", "TOPICO_NOVO = \\'v409-selada-traducao-turing.md\\'")

# ---------------------------------------------------------------- o espelho da casa: D59 (nenhum nome com o que fica fora no resumo; so' a contagem)
a.troca("_ESP_N = 0; _ESP_B = 0; _ESP_LISTA = []", "_ESP_N = 0; _ESP_B = 0; _ESP_LISTA = []; _ESP_D59_N = 0   # (v409, D59: o arquivo cujo NOME traz o que fica fora dos textos e' copiado, mas o nome nao entra no resumo; so' a contagem)")
a.troca("_ESP_N += 1; _ESP_B += os.path.getsize(_dst_a); _ESP_LISTA.append(os.path.relpath(_p_a, _CEN_REAL))",
        "_ESP_N += 1; _ESP_B += os.path.getsize(_dst_a)\n    if re.search(r\"(?i)kimi|mil[eê]nio|navier\", _p_a):\n        _ESP_D59_N += 1\n    else:\n        _ESP_LISTA.append(os.path.relpath(_p_a, _CEN_REAL))")
a.troca('"n_falas_excluidas_nao_copiadas_nem_nomeadas": _ESP_EXCL_N,', '"n_falas_excluidas_nao_copiadas_nem_nomeadas": _ESP_EXCL_N, "n_arquivos_copiados_sem_nome_no_resumo_D59": _ESP_D59_N,')
a.troca('"as falas de 04/11 do operador nao estao todas na pasta do sandbox', '"as falas de 05/11 do operador nao estao todas na pasta do sandbox')

# ---------------------------------------------------------------- os controles negativos do fechar
a.troca('_recusa_com_core("fechar_tetelestai_valor_adulterado", "o numero de modulos ok do tetelestai_terminal_v408 adulterado no core (3 de 4)", lambda c: c["tetelestai_terminal_v408"]["values"].__setitem__("n_modulos_ok", 3))',
        '_recusa_com_core("fechar_traducao_valor_adulterado", "o numero de modulos ok do traducao_turing_v409 adulterado no core (0 de 1)", lambda c: c["traducao_turing_v409"]["values"].__setitem__("n_modulos_ok", 0))\n'
        '_recusa_com_core("fechar_traducao_acervo_integra_pinada", "o pino do acervo da v407 dito na integra no traducao_turing_v409 (D57d)", lambda c: c["traducao_turing_v409"]["acervo_v407_repinado"].__setitem__("integra_pinada", True))\n'
        '_recusa_com_core("fechar_tetelestai_valor_adulterado", "o numero de modulos ok do tetelestai_terminal_v408 (herdado) adulterado no core (3 de 4)", lambda c: c["tetelestai_terminal_v408"]["values"].__setitem__("n_modulos_ok", 3))')
a.troca('_recusa_com_core("fechar_tetelestai_frase_proibida", "uma frase proibida nos limites do tetelestai_terminal_v408", lambda c: c["tetelestai_terminal_v408"]["limites"].append("a TGL nao tem terminal"))\n'
        '_recusa_com_core("fechar_tetelestai_chave_antiga_mudada", "o registro do terminal diz que uma chave antiga mudou (chaves_antigas_que_mudam nao vazia; controle extra do fork B)", lambda c: c["tetelestai_terminal_v408"]["chaves_antigas_que_mudam"].append("rede_fock_v394.whole_certificate_inhabited"))',
        '_recusa_com_core("fechar_traducao_frase_proibida", "uma frase proibida nos limites do traducao_turing_v409 (o problema do Clay dado por resolvido)", lambda c: c["traducao_turing_v409"]["limites"].append("o problema do Clay esta resolvido"))\n'
        '_recusa_com_core("fechar_traducao_chave_antiga_mudada", "o registro da traducao diz que uma chave antiga mudou (chaves_antigas_que_mudam nao vazia)", lambda c: c["traducao_turing_v409"]["chaves_antigas_que_mudam"].append("rede_fock_v394.whole_certificate_inhabited"))')
a.troca("# a PORTA do paragrafo novo isolada: T.paragrafo_v409() da copia do sandbox tem de LEVANTAR com o numero de modulos do terminal adulterado no core",
        "# a PORTA do paragrafo novo isolada: T.paragrafo_v409() da copia do sandbox tem de LEVANTAR com o numero de modulos da traducao adulterado no core")
a.troca('cj = json.loads(raw_core.decode("utf-8")); cj["core"]["tetelestai_terminal_v408"]["values"]["n_modulos_ok"] = 3', 'cj = json.loads(raw_core.decode("utf-8")); cj["core"]["traducao_turing_v409"]["values"]["n_modulos_ok"] = 0')
a.troca('"a porta do paragrafo novo (paragrafo_v409, chamada pelo fechar) levanta com o numero de modulos do tetelestai_terminal_v408 adulterado"', '"a porta do paragrafo novo (paragrafo_v409, chamada pelo fechar) levanta com o numero de modulos do traducao_turing_v409 adulterado"')
a.troca('_recusa_com_core("fechar_inscricao_nao_embutida", "uma inscricao de 04/11 deixou de estar embutida no core (cunhagens_v408)", lambda c: list(c["cunhagens_v408"]["verbatim"].values())[0].__setitem__("embedded_ok", False))\n'
        '_recusa_com_core("fechar_sem_errata_e21", "a errata E21 ausente do registro cunhagens_v408 (restam E22 e E23)", lambda c: c["cunhagens_v408"]["erratas"].pop(0))\n'
        '_recusa_com_core("fechar_sem_decisao_d54", "a decisao D54 da gerencia ausente do registro cunhagens_v408", lambda c: c["cunhagens_v408"]["extras"]["decisoes"].pop("D54"))\n'
        '_recusa_com_core("fechar_leitura_sem_onto", "a leitura de 04/11 dita [REAL] no core (e\' ONTO)", lambda c: c["cunhagens_v408"]["extras"]["leituras"].__setitem__("estatuto", "[REAL]"))\n'
        '_recusa_com_core("fechar_cunhagens_v408_sem_e21_ao_lado", "a errata E21 ao lado de cunhagens_v407 (herdada, recriada) ausente do core", lambda c: c["cunhagens_v407"]["erratas"].pop())',
        '_recusa_com_core("fechar_inscricao_nao_embutida", "uma inscricao de 05/11 deixou de estar embutida no core (cunhagens_v409)", lambda c: list(c["cunhagens_v409"]["verbatim"].values())[0].__setitem__("embedded_ok", False))\n'
        '_recusa_com_core("fechar_sem_errata_e24", "a errata E24 ausente do registro cunhagens_v409 (restam E25, E26 e a dos pisos)", lambda c: c["cunhagens_v409"]["erratas"].pop(0))\n'
        '_recusa_com_core("fechar_sem_decisao_d56", "a decisao D56 (o alcance) da gerencia ausente do registro cunhagens_v409", lambda c: c["cunhagens_v409"]["extras"]["decisoes"].pop("D56"))\n'
        '_recusa_com_core("fechar_leitura_sem_input", "a leitura de 05/11 dita [REAL] no core (e\' INPUT)", lambda c: c["cunhagens_v409"]["extras"]["leituras"].__setitem__("estatuto", "[REAL]"))\n'
        '_recusa_com_core("fechar_cunhagens_v408_sem_e26_ao_lado", "a errata E26 ao lado de cunhagens_v408 (herdada, recriada) ausente do core", lambda c: c["cunhagens_v408"]["erratas"].pop())\n'
        '_recusa_com_core("fechar_cunhagens_v407_sem_d57d_ao_lado", "a errata da D57(d) ao lado de cunhagens_v407 (herdada, recriada) ausente do core", lambda c: c["cunhagens_v407"]["erratas"].pop())')
a.troca('    print("  paragrafo novo (Tetelestai e\' o terminal) e nota ao lado dos anteriores no handoff:', '    print("  paragrafo novo (a traducao as classes de Turing) e nota ao lado do paragrafo da v408 no handoff:')
a.troca('"o b3_recibo confere o passo simples B17 -> B18; o fechar grava o handoff (com os dois paragrafos do README/site aprovados: o do quadro pelo quadro, o da v409 (Tetelestai e\' o terminal) pela verificacao propria; a nota ao lado do paragrafo da v408 (E21);',
        '"o b3_recibo confere o passo simples B17 -> B18; o fechar grava o handoff (com os dois paragrafos do README/site aprovados: o do quadro pelo quadro, o da v409 (a traducao as classes de Turing) pela verificacao propria; a nota ao lado do paragrafo da v408 (E26);')
a.troca("com um numero do tetelestai_terminal_v408, do psion_canto_v407 herdado, do fechamento_v406 herdado,", "com um numero do traducao_turing_v409, do tetelestai_terminal_v408 herdado, do psion_canto_v407 herdado, do fechamento_v406 herdado,")
a.troca("com a direcao do testemunho invertida, com uma inscricao de 04/11 nao embutida, com uma chave antiga dita mudada, \"",
        "com a direcao do testemunho invertida, com uma inscricao de 05/11 nao embutida, com uma chave antiga dita mudada, com o pino do acervo da v407 na integra, \"")
a.troca('"com a errata E21 ou a decisao D54 a menos (e com a E21 ao lado da cunhagens_v407 herdada ausente), com a leitura de 04/11 dita REAL,',
        '"com a errata E24 ou a decisao D56 a menos (e com a E26 ao lado da cunhagens_v408 ou a D57(d) ao lado da cunhagens_v407, herdadas, ausente), com a leitura de 05/11 dita REAL,')
a.grava()
