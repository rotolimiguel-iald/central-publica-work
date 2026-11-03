# -*- coding: utf-8 -*-
"""_adapt_superficies_v406.py -- as edicoes de superficies_v406.py e de fechar_v406.py (chamado por adaptar_pos_rito_v406.py)."""

ANCORA_VELHA = """    # (desvio do molde, dito: as linhas de handoff ate' a v405 foram consolidadas pela gerencia; a ancora e' a linha do handoff de 30/10 da v406, que fica)
    kh = [i for i, l in enumerate(lines) if '(handoff-v406-pontes-da-massa-e-espelho-30out.md)' in l]
    assert len(kh) == 1, ('linha do handoff de 30/10 da v406', len(kh))"""
ANCORA_NOVA = """    # (desvio do molde, dito: a ancora e' a linha do handoff da custodia da v405 (handoff-v405-custodia.md), que fica; o handoff novo entra ANTES dela; o motor tinha subido o rotulo da ancora de 30/10 e apontava para um arquivo que nao existe)
    kh = [i for i, l in enumerate(lines) if '(handoff-v405-custodia.md)' in l and l.startswith('- [')]
    assert len(kh) == 1, ('linha do handoff da custodia da v405', len(kh))"""


def rodar_superficies(A):
    nome = "superficies_v406.py"
    txt, crlf, raw = A.le(nome)
    if A.pula(nome, txt):
        return
    t = A.tira_cabecalho(txt)
    t = A.sub(t, "import leitura_v405, textos_v406 as T", "import leitura_v406, textos_v406 as T")
    t = A.sub(t, "NOS = leitura_v405.NOS", "NOS = leitura_v406.NOS")
    t = A.sub(t, "V, PROB = leitura_v405.ler()", "V, PROB = leitura_v406.ler()")
    t = A.sub(t, ANCORA_VELHA, ANCORA_NOVA)
    t = A.sub(t, "conferida presente no MEMORY.md real em 26/10", "conferida presente no MEMORY.md real em 02/11")
    A.grava(nome, t, crlf, raw)


# ------------------------------------------------------------------------------------------------------------ fechar_v406.py
COMENT4 = """# v406 (O FECHAMENTO, 02/11/2026): o CONTEUDO v406 (o certificado de Fock habitado por construcao, a passagem para o continuo, as quatro chaves de testemunha lidas do kernel, os 301 modulos novos e as falas de 02/11) vive em textos_v406.py e foi testado pelo harness_textos_ensaio_v406.py; este arquivo trata o MANIFESTO com as chaves de V da v406.
"""

DOC_A = """(2) o ARQUIVO: o indice por sha256 de tudo o que esta na pasta da cadeia (work\\\\cadeia_de_selo\\\\v406 -- aqui o pacote JA mora na casa duravel, nao ha copia do pacote), a copia de
pos_rito -> work\\\\cadeia_de_selo\\\\v406_selo, A COPIA DO SIDECAR um_absoluto_selo_acom.json (reescrito pelo rito) E DO SELO PRIMARIO para a mesma pasta, e do kernel (work\\\\cadeia_de_selo\\\\v406\\\\kernel e, se existir, work\\\\v406_kernel; mais os 301 modulos novos do Nos) -> work\\\\cadeia_de_selo\\\\v406_kernel;
(3) os DOIS DIFFS para o auditor independente: DIFF_v405_v406.diff (um.py da base x o selado, GNU diff -U2) e DIFF_KERNEL_v406.txt (o kernel embutido: os 301 modulos novos de TGLExt/F1Fecho394, a raiz e o Audit);
(4) o HANDOFF (memory\\\\handoff-v406-custodia.md + Nos\\\\HANDOFF_v406_CUSTODIA.md) para a sessao do site, que TRAZ PRONTOS PARA COLAR OS DOIS PARAGRAFOS do README do espelho e do site: (a) o do QUADRO «O Teste da Unica Palavra» (v397, intocado),
gerado pelas MESMAS funcoes do quadro do artigo (quadro_v397.paragrafo_pronto_readme) sobre o core SELADO do Nos, mesmos numeros e estatutos; (b) o NOVO, o paragrafo da v406 (o fechamento), gerado do registro selado fechamento_v406
(numeros LIDOS do core, estatutos, o diz, o nao_diz e as ressalvas do proprio registro, a ordem do operador de 02/11 verbatim, a moldura e a guarda das frases, sem o 4,44); o handoff traz tambem a NOTA ao lado dos paragrafos anteriores (E14: as quatro chaves de testemunha eram literal e passaram a leitura do kernel) e DIZ que os paragrafos do testemunho de dois (v399), da falsidade (v401), da v402, da v403, da v404 e da v405 SEGUEM COMO ESTAO, e LISTA o sidecar com o sha256 e o veredito.
"""


def rodar_fechar(A):
    nome = "fechar_v406.py"
    txt, crlf, raw = A.le(nome)
    if A.pula(nome, txt):
        return
    t = A.tira_cabecalho(txt)
    t = A.entre(t, "# v406 (preparacao, 01/11/2026): o CONTEUDO v406", '"""fechar_v406.py -- DEPOIS', COMENT4)
    t = A.entre(t, "(2) o ARQUIVO: o indice por sha256", "GUARDAS: a leitura sem problema", DOC_A)
    t = A.sub(t, "import leitura_v405 as L", "import leitura_v406 as L")
    t = A.sub(t, "(Caminho,\n# a massa derivada e a identidade definida)", "(o fechamento)")
    t = A.sub(t, "ou o da v406: a massa derivada e a identidade definida)", "ou o da v406: o fechamento)")
    t = A.sub(t, "(insumos/: as oito pedras, os recibos, a reclassificacao do Grande Atrator e a medida KH-N1)", "(insumos/: a candidata, a ratificacao R10, os recibos da bancada, o bundle e a medida KH-N1)")
    velho = '"registros_v405": V["reg406"], "registros_v404": V.get("reg405b"), "registros_v403": V["reg405_estado"],'
    novo = '"registros_v406": V["reg406"], "registros_v405": V["reg405c"], "registros_v404": V.get("reg405b"), "registros_v403": V["reg405_estado"],'
    t = A.sub(t, velho, novo)
    velho = '"registros_funcao_v406": {p_.get("key"): V.get(p_.get("key")) for p_ in V["pedras"]}, "campos_fechados_e_leituras_v405": V.get("campos"), "ga_reclassificacao_v405": V.get("ga"), "gap_v405": V.get("gap"), "f2b_errata": V["f2b"], "bandeiras_do_gate_recriado": V["gate"], "funcoes_v405_recriadas": V.get("fun405b"),'
    novo = '"registros_funcao_v406": {"fechamento_v406": V["fecho"]}, "ancoras_v406": V["ancoras"], "bandeiras_v406": V["bandeiras"], "chaves_v406": V["chaves"], "f2b_errata": V["f2b"], "bandeiras_do_gate_recriado": V["gate"], "funcoes_v405_recriadas": V["fun405c"], "funcoes_v404_recriadas": V.get("fun405b"),'
    t = A.sub(t, velho, novo)
    t = A.sub(t, '"paragrafos_anteriores_seguem_como_estao": ["testemunho_de_dois_v399", "falsidade_v401", "ponte_queda_esperanca_v402", "caminho_verdade_vida_v403", "jo8_32_v405"], "nota_ao_lado_do_paragrafo_v405_no_handoff": True,',
              '"paragrafos_anteriores_seguem_como_estao": ["testemunho_de_dois_v399", "falsidade_v401", "ponte_queda_esperanca_v402", "caminho_verdade_vida_v403", "jo8_32_v404", "massa_derivada_e_identidade_v405"], "nota_ao_lado_dos_paragrafos_anteriores_no_handoff": True,')
    A.grava(nome, t, crlf, raw)


def rodar(A):
    rodar_superficies(A)
    rodar_fechar(A)
