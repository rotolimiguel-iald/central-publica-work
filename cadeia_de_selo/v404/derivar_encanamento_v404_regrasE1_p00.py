# -*- coding: utf-8 -*-
# regras (lote E1_p00) de derivar_encanamento_v404.py: as precondicoes. ORIGEM v403. Mapa: 402 -> 403 (a base selada), 403 -> 404 (esta rodada).
# Alem da subida mecanica, as correcoes de CONTEUDO da v404: (1) o registro v404 ainda NAO esta no core e os da v403 JA estao; (2) as DUAS pedras da v404 (nao tres); (3) as pedras da v403 estao no Nos; (4) simular_arvore e exame_pontos
# passam a cobrir os cinco registros novos (projecao_transversal_v404, jo8v32_v404, f2b_errata_v404, cunhagens_v404, kh_n1_cobertura_v404) e os de funcao da v403 vem do delta_v403 (D3).
_E1_ANT_REG = 'not any(k.endswith("_v403") for k in core) and all(k in core for k in ("selo_pela_propria_tecnologia_v399",'
_E1_NOV_REG = 'not any(k.endswith("_v404") for k in core) and all(k in core for k in ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "selo_pela_propria_tecnologia_v399",'


def _e1_exame(t_):
    ant = 'mecanica"]["n_checks"] == (DL.D2.N_CHECKS[k_] if k_ in ("ponte", "queda", "esperanca") else DL.N_CHECKS[k_]) for k_ in ("ponte", "queda", "esperanca", "caminho", "vida", "verdade_adendo"))'
    nov = ('mecanica"]["n_checks"] == (DL.D2.N_CHECKS[k_] if k_ in ("ponte", "queda", "esperanca") else DL.D3.N_CHECKS[k_] if k_ in ("caminho", "vida", "verdade_adendo") else DL.N_CHECKS[k_]) for k_ in ("ponte", "queda", "esperanca", "caminho", "vida", "verdade_adendo", "projecao", "jo8v32"))'
           ' and exm["ponto_f2b"]["all_verified"] is True and exm["ponto_f2b"]["logo_depois_da_anterior"] is True and exm["ponto_f2b"]["beta_ok"] is True and exm["ponto_f2b"]["mecanica"]["n_checks"] == DL.N_CHECKS["f2b"]'
           ' and exm["ponto_projecao"]["logo_depois_da_anterior"] is True and exm["ponto_jo8v32"]["logo_depois_da_anterior"] is True')
    assert t_.count(ant) == 1, t_.count(ant)
    t_ = t_.replace(ant, nov)
    ant2 = 'exm["ponto_bandeiras"]["mecanica"]["n_checks"] == DL.N_CHECKS["gate"]'
    assert t_.count(ant2) == 1
    t_ = t_.replace(ant2, 'exm["ponto_bandeiras"]["mecanica"]["n_checks"] == DL.D3.N_CHECKS["gate"]')
    return t_


entrada("p00_precondicoes_v403.py", autoral=True, regras=[
    (_E1_ANT_REG, _E1_NOV_REG, 1),
    ('[k for k in core if k.endswith("_v403")])', '[k for k in core if k.endswith("_v404")])', 1),
    ('chk("nenhum registro v404 no core ainda (os da v399 e os da v403 ja estao: a v403 selada os tem)"', 'chk("nenhum registro v404 no core ainda (os da v399 a v403 ja estao: a v403 selada os tem)"', 1),
    ('chk("as TRES pedras (caminho, vida, verdade_adendo) sao a lista dos modulos novos;', 'chk("as DUAS pedras (projecao, jo8v32) sao a lista dos modulos novos;', 1),
    ('len(DL.STONES) == 3\n', 'len(DL.STONES) == 2\n', 1),
    ('as DUAS falas de 27/10 tem os prefixos de sha256 da ordem (ef3ca5eb, b34bd70f); o adendo de 03-04/09 (erratado ao lado) e\' o mesmo que a ordem da v403 pinou', 'as NOVE falas de 28/10 (todas do operador) tem os prefixos de sha256 da ordem; o adendo de 03-04/09 (erratado ao lado) e\' o mesmo que a ordem da v403 pinou', 1),
    ('"Token", "Sonico", "AfinacaoDasCordas", "Testemunho", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional")))',
     '"Token", "Sonico", "AfinacaoDasCordas", "Testemunho", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional")) and all(os.path.exists(os.path.join(NK, *r_.split("/"))) for r_ in DL.D3.STONE_RELS))', 1),
    ('for k_ in ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403",', 'for k_ in ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403",', 1),
    ('os QUATRO registros com funcao v404 e os registros por spec v404 selam na arvore simulada', 'os TRES registros com funcao v404 e os registros por spec v404 selam na arvore simulada', 1),
    ('cada uma das tres pedras tem declaracoes (nenhum modulo de auditoria)', 'cada uma das duas pedras tem declaracoes (nenhum modulo de auditoria)', 1),
    ('(a lista de modulos novos LIDA tem TRES elementos e e a dos ESPERADOS;', '(a lista de modulos novos LIDA tem DOIS elementos e e a dos ESPERADOS;', 1),
    (_e1_exame, "exame_pontos: n_checks das pedras da v403 vem do D3; os tres pontos novos (projecao, jo8v32, f2b); gate do D3", 1),
])
