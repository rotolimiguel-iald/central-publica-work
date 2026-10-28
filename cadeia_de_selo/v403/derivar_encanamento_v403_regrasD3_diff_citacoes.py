# -*- coding: utf-8 -*-
# regras (lote D3) de derivar_encanamento_v403.py: o diff do kernel e os pinos do B(n) (diff_e_pinos) e a conferencia das citacoes. ORIGEM v402. Escrito pela ferramenta Write; contagem exata; nada e' executado.
# O que a v403 muda: (a) o Audit NAO muda (so' a raiz ganha os tres imports): o diff do kernel e' as TRES pedras novas + a raiz; (b) o B(n) e' o passo simples v402 -> v403 (REPINADA_B12); (c) as inscricoes embutidas sao as DUAS falas de 27/10/2026
# (_V403_VERBATINS2, nomes protegidos: os da v402 nasceram no um.py e nao sobem sozinhos); as citacoes do operador nos snippets sao as dos snippets da v403.

entrada("diff_e_pinos_v402.py", autoral=True, regras=[
    ('sorted(mudados) == ["TGL/Audit.lean", "TGLExt.lean"], ("o diff do kernel nao e\' so\' a pedra + raiz + Audit", novos, removidos, mudados)',
     'sorted(mudados) == ["TGLExt.lean"], ("o diff do kernel nao e\' so\' as tres pedras + a raiz (o Audit nao muda na v403)", novos, removidos, mudados)', 1),
    ("REPINADA_B11__", "REPINADA_B12__", 1),
])

entrada("conferir_citacoes_v402.py", autoral=True, regras=[
    ("toda inscricao de 26/10/2026 que a v403 EMBUTE ou CITA", "toda inscricao de 27/10/2026 que a v403 EMBUTE ou CITA", 1),
    ("(a) cada texto embutido em _V402_VERBATINS2 e'", "(a) cada texto embutido em _V403_VERBATINS2 e'", 1),
    ("do registro cunhagens_v402 esta VERBATIM", "do registro cunhagens_v403 esta VERBATIM", 1),
    ("as tres inscricoes (todas falas do operador: nenhuma e' da gerencia)", "as duas inscricoes (todas falas do operador: nenhuma e' da gerencia)", 1),
    ('alvo = {"_V402_VERBATINS2", "_V402_SPECS", "_V402_CONTRACTS"}', 'alvo = {"_V403_VERBATINS2", "_V403_SPECS", "_V403_CONTRACTS"}', 1),
    ('V = ns["_V402_VERBATINS2"];', 'V = ns["_V403_VERBATINS2"];', 1),
    ("ok = ok and len(V) == len(DL.VERBATIM_ORIGEM_V403) == 3", "ok = ok and len(V) == len(DL.VERBATIM_ORIGEM_V403) == 2", 1),
    ('R["nenhuma_e_da_gerencia_as_tres_sao_do_operador"] = all(os.path.basename(v["fonte_original"]).startswith("OPERADOR_26out_") for v in V.values()); ok = ok and R["nenhuma_e_da_gerencia_as_tres_sao_do_operador"]',
     'R["nenhuma_e_da_gerencia_as_duas_sao_do_operador"] = all(os.path.basename(v["fonte_original"]).startswith("OPERADOR_27out_") for v in V.values()); ok = ok and R["nenhuma_e_da_gerencia_as_duas_sao_do_operador"]', 1),
    ('cg = [s for s in ns["_V402_SPECS"] if s["nome"] == "cunhagens_v402"][0]', 'cg = [s for s in ns["_V403_SPECS"] if s["nome"] == "cunhagens_v403"][0]', 1),
    ('R["leituras"]["cunhagens_v402: " + it["trecho"][:60]]', 'R["leituras"]["cunhagens_v403: " + it["trecho"][:60]]', 1),
    ('"h_tau na forma literal refutada no kernel"}', '"h_tau na forma literal refutada no kernel",\n            # v403: o titulo da secao nova e o seu rotulo no .md (rotulos da propria cadeia, nao citacao)\n            "caminho, verdade e vida (v403)", "caminho, verdade e vida", "way, truth and life"}', 1),
    ('CIT_OP = ["o Um quando se põe realiza a operação", DL.FRASE_CAI, DL.FRASE_DIRECAO, DL.FRASE_NAO_FORCA, DL.FRASE_ESPERANCA]',
     'CIT_OP = ["a meu ver o nome é", DL.FRASE_CONCORDO]   # (os fragmentos nao carregam aspas retas: o LaTeX as escreve de outro modo; a fala de 27/10 traz o resto)', 1),
])
