# -*- coding: utf-8 -*-
# regras (lote E1) de derivar_encanamento_v403.py: as PRECONDICOES de bytes (p00_precondicoes_v403.py). ORIGEM v402. Escrito pela ferramenta Write; contagem exata; nada e' executado.
# O que a v403 muda: (a) o core da base (v402 selada) JA traz os registros da v402 (ponte, queda, esperanca, cunhagens e kh_n1) e NAO traz nenhum *_v403; (b) as pedras da v402 entram na lista das que ja estao no kernel do Nos; (c) os pontos de chamada do exame
# incluem os QUATRO registros novos (caminho, vida, verdade_adendo, bandeiras) e a arvore simulada os seis registros da v403; (d) as falas sao DUAS, de 27/10 (prefixos ef3ca5eb e b34bd70f, do plano).

entrada("p00_precondicoes_v402.py", autoral=True, regras=[
    ('not any(k.endswith("_v402") for k in core) and all(k in core for k in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401")), [k for k in core if k.endswith("_v402")])',
     'not any(k.endswith("_v403") for k in core) and all(k in core for k in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402")), [k for k in core if k.endswith("_v403")])', 1),
    ("(runtime_v403.py: os tres registros com funcao ponte_da_escala_dual_v402, queda_sem_geometria_v402 e esperanca_condicional_v402, escritos a mao)",
     "(runtime_v403.py: os QUATRO registros com funcao caminho_v403, vida_v403, verdade_adendo_v403 e bandeiras_do_gate_v403, escritos a mao)", 1),
    ("as TRES pedras (ponte, queda, esperanca) sao a lista dos modulos novos;", "as TRES pedras (caminho, vida, verdade_adendo) sao a lista dos modulos novos;", 1),
    ("as TRES inscricoes de 26/10 tem os prefixos de sha256 da ordem (5d3976cd, 36cfa002, a1c4bae4);", "as DUAS falas de 27/10 tem os prefixos de sha256 da ordem (ef3ca5eb, b34bd70f);", 1),
    ('"Testemunho", "FalsidadeDaInercia")))', '"Testemunho", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional")))', 1),
    ('chk("as tres cunhagens de 26/10 (todas falas do operador): arquivo duravel', 'chk("as DUAS falas de 27/10 (ambas do operador): arquivo duravel', 1),
    ("as TRES inscricoes de 26/10 desta versao tem os prefixos de sha256 que a ordem da gerencia deu (todas falas do operador)", "as DUAS falas de 27/10 desta versao tem os prefixos de sha256 que a ordem da gerencia deu (ambas do operador)", 1),
    ("os tres registros com funcao v403 e os registros por spec v403 selam na arvore simulada do Nos", "os QUATRO registros com funcao v403 e os registros por spec v403 selam na arvore simulada do Nos", 1),
    ('for k_ in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402", "falsidade_da_inercia_v401",',
     'for k_ in ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402", "falsidade_da_inercia_v401",', 1),
    ("o da esperanca_condicional_v402 logo depois da queda e o do teste_de_veracidade_fase9_v397 logo depois do bloco do V1)",
     "o da esperanca_condicional_v402 logo depois da queda, o do caminho_v403 logo depois da esperanca, o da vida_v403 logo depois do caminho, o do verdade_adendo_v403 logo depois da vida, o das bandeiras_do_gate_v403 logo depois do adendo e o do teste_de_veracidade_fase9_v397 logo depois do bloco do V1)", 1),
    ('and exm["ponto_" + k_]["mecanica"]["n_checks"] == DL.N_CHECKS[k_] for k_ in ("ponte", "queda", "esperanca"))',
     'and exm["ponto_" + k_]["mecanica"]["n_checks"] == (DL.D2.N_CHECKS[k_] if k_ in ("ponte", "queda", "esperanca") else DL.N_CHECKS[k_]) for k_ in ("ponte", "queda", "esperanca", "caminho", "vida", "verdade_adendo")) and exm["ponto_bandeiras"]["all_verified"] is True and exm["ponto_bandeiras"]["logo_depois_da_anterior"] is True and exm["ponto_bandeiras"]["mecanica"]["n_checks"] == DL.N_CHECKS["gate"] and (exm["ponto_bandeiras"].get("valores_do_gate") or {}).get("n_literal") == 0', 1),
])
