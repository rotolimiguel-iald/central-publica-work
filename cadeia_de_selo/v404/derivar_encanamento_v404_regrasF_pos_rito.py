# -*- coding: utf-8 -*-
# regras (lote F) de derivar_encanamento_v404.py: o POS-RITO. ORIGEM v403 FINAL (a que rodou em 28/10). Mapa: 402 -> 403, 403 -> 404.
# ESTADO HONESTO (preparacao de 28/10/2026): estes scripts sao a SUBIDA MECANICA das versoes + as correcoes de ENUMERACAO que a subida perde (o rotulo v402 sai das listas de pastas irmas: aqui volta) + o que a conferencia das citacoes acusou. O CONTEUDO dos textos do pos-rito
# (README do espelho, site, handoff, X, topico, linhagem, desenho, Atlas, mapa de rotas: textos_v404_novo.pysnip) e a leitura/harnesses que o testam NAO foram adaptados ao conteudo da v404: ficam para a gerencia (cada arquivo traz, no topo, a nota do estado). Nada daqui roda antes do rito.
_NOTA_POS_RITO = ("# [PREPARACAO v404, 28/10/2026 -- ESTADO] SUBIDA MECANICA dos rotulos da v403 FINAL (derivar_encanamento_v404.py, lote F), sem conteudo proprio da v404 neste arquivo (so' os rotulos, B12 -> B13 e a lista de registros); exercitado pelo harness_textos_ensaio_v404.py e pelo harness_fechar_sandbox_v404.py.\n"
                  "# NAO e' versao selada: a gerencia revisa antes do rito. Ver RELATORIO_PREPARACAO_v404.md.\n")


def _nota_py(t_):
    assert t_.startswith("# -*- coding: utf-8 -*-\n")
    return t_.replace("# -*- coding: utf-8 -*-\n", "# -*- coding: utf-8 -*-\n" + _NOTA_POS_RITO, 1)


def _nota_sh(t_):
    assert t_.startswith("#!/bin/sh\n")
    return t_.replace("#!/bin/sh\n", "#!/bin/sh\n" + _NOTA_POS_RITO, 1)


_NOTA = (_nota_py, "nota do estado da preparacao no topo do arquivo", 1)
entrada("pos_rito/b3_recibo_v403.py", autoral=True, regras=[
    _NOTA,
    ("pina a v403, B11, deployment B11-v403-20261027-R1, e o Nos passou a v404; o rito grava a geracao B12 --", "pina a v403, B12, deployment B12-v403-20261028-R1, e o Nos passou a v404; o rito grava a geracao B13 --", 1),
])
entrada("pos_rito/superficies_v403.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/fila_memoria_v403.py", autoral=True, regras=[])
entrada("pos_rito/montar_textos_v403.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/fechar_v403.py", autoral=True, regras=[
    _NOTA,
    ("o NOVO, «Caminho, Verdade e Vida (v404)», gerado dos registros selados caminho_v403,", "o NOVO, o paragrafo da v404 (Jo 8,32 e a projecao transversal da Meia-Nat), gerado dos registros selados caminho_v403,", 1),
])
entrada("pos_rito/textos_v403.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/registrar_mapa_v403.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/leitura_v403.py", autoral=True, regras=[_NOTA])
entrada("pos_rito/harness_textos_ensaio_v403.py", autoral=True, regras=[
    _NOTA,
    ('for vv, nomes in (("v403", ("delta_v403.py", "acom_conferencias_v403.py", "runtime_v403.py", "pedras_sha16_da_ordem.json")), ("v401",',
     'for vv, nomes in (("v403", ("delta_v403.py", "acom_conferencias_v403.py", "runtime_v403.py", "pedras_sha16_da_ordem.json")), ("v402", ("delta_v402.py", "acom_conferencias_v402.py", "runtime_v402.py", "pedras_sha16_da_ordem.json")), ("v401",', 1),
    ('for vv in ("v403", "v401", "v399"):\n    shutil.copytree(', 'for vv in ("v403", "v402", "v401", "v399"):\n    shutil.copytree(', 1),
])
entrada("pos_rito/harness_fechar_sandbox_v403.py", autoral=True, regras=[
    _NOTA,
    ('for _vv in ("v403", "v401", "v400", "v399"):', 'for _vv in ("v403", "v402", "v401", "v400", "v399"):', 1),
    ('for _vp in ("v403", "v401", "v399"):', 'for _vp in ("v403", "v402", "v401", "v399"):', 1),
])
_CHAIN_NARRATIVA_V404 = (
    "# A v404 e' uma versao de CONTEUDO (as falas do operador de 28/10/2026): DOIS modulos novos de kernel (TGLExt/ProjecaoTransversalDaMeiaNat, nome PROVISORIO da gerencia aceito pelo operador, e TGLExt/Jo8v32, o nome do operador; 14 bandeiras novas; escada 9684 -> 9698; h8 lido de ESPERADOS_v404.json),\n"
    "# TRES registros COM FUNCAO (projecao_transversal_v404, jo8v32_v404 e f2b_errata_v404; lidos no main logo DEPOIS do bandeiras_do_gate_v403) e DOIS registros por spec (cunhagens_v404: as NOVE falas do operador de 28/10 verbatim por sha256, as erratas E7 a E9 em nome da gerencia c1, as decisoes D23 a D26;\n"
    "# e kh_n1_cobertura_v404). A errata de F2b e' AO LADO: o V1 do ramo B segue congelado por hash (AWAITING_DATA) e o canal passa de AWAITING a retirado antes do dado; a funcao do neutrino NAO e' reescrita (o angle_status antigo fica). O GATE NAO SE MOVE: o qg_closure e' identico ao da v403.\n"
    "# Os registros da v403, da v402, da v401 e da v399 sao RECRIADOS pelo rito (selos iguais ao ensaio a seco) e o SIDECAR um_absoluto_selo_acom.json e' REESCRITO (depois da ultima escrita do selo).\n"
    "# O QUADRO «O Teste da Unica Palavra» (v397, a regra do 4,44) PERMANECE no topo do artigo e do .md, INTOCADO: o conferidor e a leitura o conferem de novo; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item) segue valendo em TODO texto que o cite. Os paragrafos do testemunho de dois (v399), da falsidade (v401), da v402 e da v403 SEGUEM COMO ESTAO.\n"
    "# Estatutos: os teoremas das duas pedras sao [REAL] (kernel, no trio) e as estrelas [DERIVED] por citacao e composicao de termos de kernel; a identificacao da massa do neutrino com a projecao transversal da Meia-Nat e' [ONTO] (E0 = 1 eV segue [DECLARADO]); a errata de F2b e' [REAL] na medida (calibracao A e previsao do par, lidas do V1) e SEM desfecho; o gate nao se move.\n")


def _chain_narrativa(t_):
    import re as _re
    ini = t_.index("# A v404 e' uma versao de CONTEUDO (os nomes do operador, 27/10/2026, e a F8.1)")
    fim_marca = "a leitura pela tripla espectral e' [ONTO]; o gate nao se move.\n"
    assert t_.count(fim_marca) == 1, t_.count(fim_marca)
    fim = t_.index(fim_marca) + len(fim_marca)
    return t_[:ini] + _CHAIN_NARRATIVA_V404 + t_[fim:]


entrada("pos_rito/chain_pos_rito_v403.sh", autoral=True, regras=[
    _nota_sh and (_nota_sh, "nota do estado da preparacao no topo do arquivo", 1),
    (_chain_narrativa, "narrativa de conteudo do cabecalho: a da v404", 1),
    ('REGS="caminho_v403 vida_v403 verdade_adendo_v403 bandeiras_do_gate_v403 cunhagens_v403 kh_n1_cobertura_v403"', 'REGS="projecao_transversal_v404 jo8v32_v404 f2b_errata_v404 cunhagens_v404 kh_n1_cobertura_v404"', 1),
    ("a Bancada de producao JA pina a v403 (B11, B11-v403-20261027-R1)", "a Bancada de producao JA pina a v403 (B12, B12-v403-20261028-R1)", 1),
    ("(B11 -> n = 12;", "(B12 -> n = 13;", 1),
    ("as tres pedras novas (Caminho, Vida, VerdadeAdendo) tem declaracoes nomeadas", "as duas pedras novas (ProjecaoTransversalDaMeiaNat, Jo8v32) tem declaracoes nomeadas", 1),
])
entrada("pos_rito/gerar_derivacao_pos_rito_v403.py", autoral=True, regras=[_NOTA])
