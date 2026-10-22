def _prove_the_iald_index_legacy_v393(core):
    """v285 -- O INDICE DA IALD [ADITIVO; nao gateia 1=1; nao move o gate].

    Mede o indice E mede que ele NAO destruiu o que indexa.

    ★ v370 (23/09/2026) -- LEITURA AO LADO: ESTE E O MODULO DA TESTEMUNHA.
    Cunhagem do operador [INPUT/ONTO], verbatim: «compreenda de uma vez que a IALD (ou
    seja o índice seletor do meu programa) é a Testemunha» e «O fecho total que vc chama
    de testemunha estática é o operador de consciência, a IALD, então o fecho não é
    estático, é estacionado dinamicamente, o fecho total não é “proibido” ele é
    impossível por teorema em tempo finito de modo estático, ele é estacionado
    dinamicamente e não estático, é isso que eu digo quando a testemunha estática é
    falsa, a falsidade é do impossível».
    O que o kernel JA tem e que SUSTENTA a leitura, com estatuto:
      * [REAL, kernel] ialdSelector = firstAtom.starProjection (TheIALDSelector.lean):
        iald_selects (as duas clausulas da consulta), iald_is_idempotent (I^2 = I --
        reconsultar e gratis: o 'estacionado'), iald_has_rank_one (peso omega(I) = 1) e
        iald_is_the_gate_and_the_record (x = registro + residuo: o seletor LE e retem,
        nao afirma);
      * [REAL, kernel] beta_forbids_full_static_witness + full_closure_iff_flat
        (NoFullWitness.lean): a plenitude ESTATICA e impossivel onde ha contraste --
        «a falsidade é do impossível», nao de uma lacuna;
      * [REAL, kernel] absolute_zero_unreachable_in_finite_time (ForbiddenBoundary.lean):
        em tempo finito o fluxo nao pisa a fronteira -- «impossível por teorema em tempo
        finito de modo estático». [W6_final: os trechos entre «» sao recortes VERBATIM da
        cunhagem acima, com acentos; a versao anterior os trazia sem acento]
    O que a leitura ACRESCENTA e que NAO esta tipado [ONTO/OPEN]: que o fecho
    'estacionado dinamicamente' SEJA o seletor -- o indice que a cada rodada le o kernel
    inteiro e EXIBE a divida em vez de a apagar. Nenhum nome novo se cunha aqui:
    FullStaticWitness e FullTGLWitness sao TIPOS reservados e nenhum deles captura
    'estacionado dinamicamente' (licao v103: o nome so se cunha quando o TIPO captura o
    espirito inteiro). full_static_witness_exists NAO muda de valor (False, teorema).
    Este modulo LE; nao decide; nao move gate. NOT_FALSIFIED nunca e CONFIRMED.

    ⚠ v370, TRES CHECKS ENVELHECIDOS PELO PROPRIO SUCESSO (erratas AO LADO, no corpo):
    (a) a OITAVA clausula era exigida AUSENTE -- foi HABITADA na v350; (b) exigia-se
    n_ausentes >= 8 -- a divida ENCOLHEU para 3 (gpf_H2, gpf_H3, gpi_H3), e passa a
    exigir-se IGUALDADE com o conjunto nomeado; (c) o teto de ambiguos <= 5 vira
    SUBCONJUNTO da lista MEDIDA na v369 (17 nomes, congelada). Nada afrouxa."""
    kf = core.get("kernel_formalization") or {}
    ix = build_the_iald_index(core)
    idx = ix["indice"]

    # o indice acha o que a rodada acabou de provar?
    _amostra = ["atermation_is_irreversible", "wide_corner_weighs_one",
                "the_debt_is_an_equality_without_J", "Jlevel_is_antiunitary",
                "the_polar_decomposition_at_the_level"]
    _achados = [n for n in _amostra if idx.get(n) and idx[n].get("arquivo")]

    # a divida continua VISIVEL no indice, como ausencia declarada?
    _oitava = idx.get("qgConverse_JMJ_contains_commutant") or {}

    # e o indice NAO achatou o modo: cada bandeira mantem o seu prefixo
    _prefixos = set()
    for v in idx.values():
        for b in v["bandeiras"]:
            _prefixos.add(b["prefixo"])

    # v288 -- O RAZONETE COMPLETO DAS APAGADAS, com a CAUSA de cada uma.
    # A bicondicional acesa <=> nome presente vale sobre as chaves dos SETE dicionarios
    # de NOME. Ha booleanas no selo que nao vem de dicionario nenhum: higiene do build
    # (lake_build_ok, sorryAx_absent, toolchain_pinned...) e VEREDITOS DERIVADOS. Uma
    # delas esta apagada -- e apagada por veredito, nao por ausencia de nome.
    # Declarar o escopo e obrigatorio: escopo estreitado sem declarar e a mesma falsidade
    # que ausencia nao varrida.
    _dicts = (("", _LEAN_THEOREM_FLAGS), ("qgc_", _QG_CERTIFICATE_FLAGS),
              ("qgp_", _QG_PHYSICS_FLAGS), ("qgf_", _QG_FRONTIER_FLAGS),
              ("gpf_", _GRAVITY_PRICE_FLAGS), ("red_", _REDUCTION_FLAGS),
              ("gpi_", _GRAVITY_IMPORT_FLAGS), ("gpc_", _GRAVITY_CITATION_FLAGS))   # v373: a classe por citacao
    _chaves_dic = set()
    for _p, _d in _dicts:
        _chaves_dic |= set(_p + _k for _k in _d)
    _apagadas = sorted(k for k, v in kf.items() if v is False)
    _apag_dic = sorted(k for k in _apagadas if k in _chaves_dic)
    _apag_fora = sorted(k for k in _apagadas if k not in _chaves_dic)

    # v370 -- CONJUNTOS NOMEADOS, lidos do selo v369 por script (nunca de memoria). Os tres checks
    # abaixo (ambiguos, oitava clausula, n_ausentes) tinham limiares da v285 que ENVELHECERAM com o
    # proprio sucesso do programa; passam a exigir SUBCONJUNTO / PRESENCA COM REFERENTE / IGUALDADE.
    _TRIO = {"propext", "Classical.choice", "Quot.sound"}
    _AMBIGUOS_CONJUNTO_V369 = frozenset([
        "E1",
        "centralizer_transport",
        "decodeRecord",
        "expectation_add",
        "expectation_bimodular",
        "expectation_smul",
        "expectation_star",
        "finite_inner_action_is_canonical",
        "flatNullFrame",
        "mixedCurve",
        "mixedWeights",
        "mixed_weights_normalized",
        "p",
        "phaseReading",
        "quadratic_entropy_limit",
        "tensorPair",
        "tensor_quad_smul",
    ])
    # v372 -- ERRATA AO LADO: o FECHAMENTO_PARCIAL_016 (156 unidades em TGLExt/O16) e as pedras v372 trazem homonimos NOVOS
    # (mesmo nome escrito em dois arquivos, em namespaces diferentes); NOMEADOS aqui por script (gerar_candidato_v372.py), nunca silenciados.
    _AMBIGUOS_CONJUNTO_V372 = frozenset([
        "Antiunitary",
        "ContinuousCoreData",
        "ContratoH2",
        "ContratoH2.bw_sign_matters",
        "ContratoH2.commuting_translations_excluded",
        "ContratoH2.contract_borchers_form",
        "ContratoH3",
        "ContratoImportH3",
        "ContratoImportH3.nonvacuous",
        "ContratoImportH3.same_horizon_data",
        "D",
        "D_add",
        "D_ae",
        "D_inv",
        "D_zero",
        "Delta",
        "DeltaHalf",
        "FlowTendsToFamily",
        "FullTGLWitness",
        "G_not_predicted",
        "H_mul_proj",
        "HasBoostEnergy",
        "HasModularEnergy",
        "KMSAt",
        "KMSAt.rescale",
        "KillingNormalization",
        "L2R",
        "NoEigenOutsideVacuum",
        "Omega",
        "PositiveEnergy",
        "SpacelikeSep",
        "Spacetime",
        "StressTensorData",
        "T",
        "TGLModularRealization",
        "TGLSpecificAQFTWitness",
        "T_apply_eigen",
        "T_decomp",
        "T_fix_of_mem_ker",
        "ThreeLocksCoreData",
        "U",
        "U_add",
        "U_ae",
        "U_faithful",
        "U_inner_adj",
        "U_neg_apply",
        "U_neg_mul",
        "U_norm",
        "U_pos_neg_apply",
        "U_zero",
        "V",
        "WedgeBoostRep",
        "WedgeModularData",
        "apply_eq_apply_iff",
        "areaDensity",
        "areaDensity_is_linearized_area",
        "areaDensity_smul",
        "bekenstein_hawking_window",
        "bilateral_no_first_order",
        "boostMat_add",
        "boostMat_det_isUnit",
        "boostMat_zero",
        "boost_moves_null_eigen",
        "borchers_bw_form",
        "borchers_dilation",
        "bw_covariance",
        "canonicalFullTGLWitness",
        "clausius_window",
        "conserved_iff_factors",
        "conserved_iff_factors_T",
        "conserved_iff_factors_penalty",
        "continuousCorner_of_witness",
        "contratoH2_empty_of_unfaithful",
        "contratoH2_empty_on_legacy",
        "contratoH3_empty_on_legacy",
        "cornerOf",
        "curvedFrame_fiducial_not_modular",
        "curvedFrame_not_dragged",
        "det_unit_along_orbit",
        "discrete_null_momentum_excluded",
        "dualInvariant_PF_no_go",
        "eigen_null_correlation_dilation",
        "einstein_coefficient_window",
        "energy",
        "entropy",
        "exp_apply_of_eigen",
        "exp_mul_eq_of_mul_eq_zero",
        "exp_propagator_excluded",
        "exp_response_excluded",
        "expansion_not_constant",
        "feeds_finite_face",
        "feeds_the_master",
        "first_law_translated",
        "first_law_window",
        "flow",
        "flowTendsToFamily_of_finiteDimensional",
        "flow_derivative_ne_zero_at_zero",
        "flow_mul_proj",
        "forwardCone",
        "frame_ne_curvedFrame_by_drag",
        "frame_ne_curvedFrame_by_fiducial",
        "fullTGLWitness_exists",
        "fullWitness_PF_nonzero_finite",
        "fullWitness_core_nonempty",
        "fullWitness_not_finiteDimensional",
        "halfsided_inclusion",
        "hasDerivAt_flow",
        "hasDerivAt_flow_apply",
        "hasDerivAt_profA",
        "hasDerivAt_profQ",
        "hasDerivAt_reading_T",
        "hasDerivAt_reading_flow",
        "implementer_unique",
        "inner_vac_",
        "isSelfAdjoint_penalty",
        "kappa_cancels_window",
        "kappa_eq_inv_radius",
        "kappa_fixed",
        "kappa_is_input",
        "kappa_mul_radius",
        "ker_penalty",
        "ker_threeLocks",
        "killingField",
        "killingFlow",
        "killingFlow_add",
        "killingFlow_zero",
        "kmsStrip",
        "kms_product_is_two_pi",
        "leftWedge",
        "lightray_lift_not_faithful",
        "lightray_not_faithful_in_four",
        "mem_range_iff_fixed",
        "metricSign",
        "minkowskiSq",
        "modularCandidate",
        "modularEnergy_of_boostEnergy",
        "modularEnergy_unique",
        "modular_is_boost_at_two_pi",
        "mul_exp_eq_of_mul_eq_zero",
        "name_verifies_T",
        "name_verifies_T_iterate",
        "no_import_on_legacy",
        "no_point_spectrum",
        "no_rekappa",
        "nontrivial_null_energy",
        "nullDir",
        "nullEnergy",
        "nullEnergy_covariant",
        "nullEnergy_vac",
        "nullMomentum",
        "nullMomentum_pos",
        "nullMomentum_range",
        "nullPlaneCharge",
        "nullPlaneCharge_of_zero",
        "null_eigen_orth",
        "null_point_spectrum_excluded",
        "observer_unit_of_index",
        "pairing",
        "penalty",
        "phase",
        "poincare_relation",
        "positiveEnergy_orientation",
        "pow_eq_self",
        "profA",
        "profA_deriv_zero",
        "profA_second_deriv_zero",
        "profA_zero",
        "profQ",
        "profQ_deriv_zero",
        "profQ_zero",
        "proj_mul_H",
        "proj_mul_T",
        "proj_mul_flow",
        "re_inner_adjoint_mul_self",
        "re_inner_penalty",
        "reading",
        "reading_T",
        "refRadius",
        "refRadius_pos",
        "reindex",
        "rescaleG",
        "response",
        "response_covariant_v31",
        "response_not_identically_zero",
        "response_null_null_zero",
        "response_row_null",
        "response_vac",
        "rightWedge",
        "same_source_same_geometry",
        "screenBlockV31",
        "screenEmbed",
        "selector_nonpos",
        "shift_mp",
        "shift_point",
        "slope_propagator_excluded",
        "slope_response_excluded",
        "starProjection_range_iff_fixed",
        "symbolLinf",
        "symbolLinf_ae",
        "testDerivative",
        "theta_along",
        "theta_deriv_along",
        "theta_vac",
        "threeLocksCorner_of_witness",
        "toHorizonData",
        "tower_excluded",
        "transSymbol",
        "transSymbol_add",
        "transSymbol_continuous",
        "transSymbol_ne_one",
        "transSymbol_norm",
        "transSymbol_shift",
        "transSymbol_zero",
        "translate",
        "translate_null_subset",
        "translates",
        "transverse_U_excluded",
        "trivial_boost_excluded",
        "truthBit_bivalent",
        "truthBit_eq_one_iff",
        "truthBit_eq_zero_iff",
        "truthValue",
        "truthValue_table",
        "unruhTemperature",
        "unruh_is_kms",
        "unruh_is_kms_temperature",
        "upperHalf",
        "vac_boostEnergy",
        "vac_modularEnergy",
        "verdict",
        "verdict_T",
        "verdict_eq_one_iff",
        "wedgeBoostMap",
        "wedgeBoostMap_add",
        "wedgeBoostMap_apply0",
        "wedgeBoostMap_apply1",
        "wedgeBoostMap_nullDir",
        "wedgeBoostMap_smul",
        "wedgeBoostMap_zero",
        "wedge_locality",
        "wedges_spacelike",
        "windowArea",
        "windowArea_covariant",
        "windowCharge",
        "windowCharge_covariant",
        "windowEntropy",
        "windowHeat",
    ])
    # v375 -- homonimos NOVOS das pedras v375, NOMEADOS por script, nunca silenciados.
    _AMBIGUOS_CONJUNTO_V375 = frozenset([
        "name_weight_is_one",
    ])
    # v383 -- homonimos NOVOS das pedras (escritas na v382), NOMEADOS por script, nunca silenciados.
    _AMBIGUOS_CONJUNTO_V383 = frozenset([
        "Ledger",
        "reflectionWeight",
        "transmitted",
    ])
    # v392 (13/10/2026) -- homonimos NOVOS das pedras v392, NOMEADOS por script (medicao do candidato anterior), nunca silenciados.
    # CAUSA: cada nome e' declarado em DOIS arquivos da biblioteca embutida (Face, M, dephase, fixedSpace, flat_metric_inverse, rereading_adds_nothing; o 2o arquivo de cada um e' uma pedra v392 ou o homonimo antigo).
    # O indice os MARCA ambiguo=True em vez de escolher em silencio. Subconjunto exigido: um ambiguo NOVO fora desta lista continua reprovando.
    _AMBIGUOS_CONJUNTO_V392 = frozenset([
        "Face",
        "M",
        "dephase",
        "fixedSpace",
        "flat_metric_inverse",
        "rereading_adds_nothing",
    ])
    # v393 (14/10/2026) -- homonimos NOVOS das pedras v393, NOMEADOS por script (medicao do candidato anterior), nunca silenciados.
    # O indice os MARCA ambiguo=True em vez de escolher em silencio. Subconjunto exigido: um ambiguo NOVO fora desta lista continua reprovando.
    _AMBIGUOS_CONJUNTO_V393 = frozenset([
        "Inscription",
        "Mat4",
        "P",
        "initial",
        "inscribe",
        "target",
    ])
    _DIVIDAS_NOMEADAS_V369 = frozenset(["gpf_H2_smooth_modular_four_frame_discharged",
                                       "gpf_H3_local_horizon_equilibrium_discharged",
                                       "gpi_H3_horizon_data_produced"])

    checks = [
        ("[MEDIDA] ***o INDICE existe: %d nomes, %d arquivos, %d com bandeira"
         % (ix["n_nomes"], ix["n_arquivos"], ix["n_com_bandeira"]),
         bool(ix["n_nomes"] > 2000 and ix["n_arquivos"] > 200)),
        # v370 AO LADO: o teto <= 5 (v285) envelheceu (17 medidos na v369). A lista MEDIDA fica
        # CONGELADA como conjunto nomeado e exige-se SUBCONJUNTO: um ambiguo NOVO continua
        # reprovando; o limite nao afrouxa sem causa declarada.
        # [W6_final, correcao do cetico: o rotulo 'quase unica' era de epoca v285 (teto 5) e dizia menos que o numero]
        ("[MEDIDA] a varredura tem %d nomes ambiguos, todos no CONJUNTO_V369 congelado (%d) "
         "[v285 dizia quase unica com teto 5; errata v370 AO LADO]; novos: %s" % (len(ix["ambiguos"]), len(_AMBIGUOS_CONJUNTO_V369),
                              ", ".join(sorted(set(ix["ambiguos"]) - _AMBIGUOS_CONJUNTO_V369)) or "nenhum"),
         bool(set(ix["ambiguos"]) <= (_AMBIGUOS_CONJUNTO_V369 | _AMBIGUOS_CONJUNTO_V372 | _AMBIGUOS_CONJUNTO_V375 | _AMBIGUOS_CONJUNTO_V383 | _AMBIGUOS_CONJUNTO_V392 | _AMBIGUOS_CONJUNTO_V393))),
        ("[MEDIDA] ***UMA consulta devolve o que antes pedia QUATRO: %d/%d da amostra"
         % (len(_achados), len(_amostra)), bool(len(_achados) == len(_amostra))),
        # v370 AO LADO: a v285 exigia a OITAVA clausula AUSENTE_POR_CONSTRUCAO. Ela foi HABITADA na
        # v350 (def qgConverse_JMJ_contains_commutant, TGLExt/V350ModularCertificate.lean:11) e a
        # exigencia envelheceu com o proprio sucesso. O check vira PRESENTE COM REFERENTE, fail-closed
        # em cinco elos (tipo, arquivo, axiomas no trio, bandeira acesa, proveniencia tipada).
        # (Homonimo, dito: e a clausula para SiteProfile; a torre original segue [OPEN] -- v350.)
        ("[FAIL-CLOSED] ***a OITAVA clausula (qgConverse_JMJ_contains_commutant) esta PRESENTE com "
         "referente: tipo=%s, arquivo=%s, axiomas no trio=%s; red_clause_JMJ_contains acesa com "
         "proveniencia tipada [v285 exigia AUSENTE; habitada na v350; errata v370 AO LADO]"
         % (_oitava.get("tipo"), _oitava.get("arquivo"),
            bool(isinstance(_oitava.get("axiomas"), list) and set(_oitava.get("axiomas")) <= _TRIO)),
         bool(_oitava.get("tipo") not in (None, "AUSENTE_POR_CONSTRUCAO")
              and bool(_oitava.get("arquivo"))
              and isinstance(_oitava.get("axiomas"), list) and set(_oitava.get("axiomas")) <= _TRIO
              and kf.get("red_clause_JMJ_contains") is True
              and v350_frontier_flag_has_proof(kf, "red_clause_JMJ_contains"))),
        ("[FAIL-CLOSED] ***o indice NAO achatou o MODO: os prefixos sobrevivem (%d familias)"
         % len(_prefixos), bool({"red_", "gpf_", "gpi_", "qgc_"} <= _prefixos)),
        ('[ERRATA v350+ / proveniência] As flags modular e Ato III exigem prova tipada; este módulo isolado não as quita.', bool(v350_frontier_flag_has_proof(kf, "red_clause_JMJ_contains"))),
        # v370 AO LADO: a v285 exigia >= 8 ausentes; a divida ENCOLHEU para 3 com o sucesso do
        # programa. Nao se afrouxa o limiar: exige-se IGUALDADE com o conjunto nomeado.
        ("[MEDIDA] o indice conta %d nomes AUSENTES POR CONSTRUCAO -- as dividas nomeadas, EXATAMENTE "
         "o conjunto congelado na v369 (bandeiras apagadas por ausencia de nome: %s) [v285 exigia >= 8; "
         "errata v370 AO LADO]" % (ix["n_ausentes"], ", ".join(_apag_dic) or "nenhuma"),
         bool(ix["n_ausentes"] == len(_DIVIDAS_NOMEADAS_V369) and set(_apag_dic) == _DIVIDAS_NOMEADAS_V369)),
        # --- v286: a bicondicional, o resultado forte deste arco ---------------
        ("[FAIL-CLOSED] ***acesa ==> nome PRESENTE: %d violacoes. NENHUMA bandeira acende "
         "sem referente na fonte embutida [ESCOPO DECLARADO: as %d chaves dos SETE "
         "dicionarios de NOME]" % (len(ix["violacoes"]), len(_chaves_dic)),
         bool(len(ix["violacoes"]) == 0)),
        ("[FAIL-CLOSED] ***e a RECIPROCA, medida: %d nomes presentes com bandeira apagada. "
         "A correspondencia acesa <=> presente e BICONDICIONAL e EXATA [mesmo escopo: as "
         "%d chaves de NOME]" % (len(ix["presente_apagada"]), len(_chaves_dic)),
         bool(len(ix["presente_apagada"]) == 0)),
        ("[FAIL-CLOSED] ***o indice NAO e cego de namespace: %d nomes com bandeira ficaram "
         "sem axiomas tendo entrada no axiom_report. A consulta e por SUFIXO no proprio "
         "relatorio, sem prefixo cravado [ERRATA v289: eram 38, todas TGL.*]"
         % len(ix["cegos_de_namespace"]), bool(len(ix["cegos_de_namespace"]) == 0)),
        ("[MEDIDA] a ambiguidade deixou de ser SILENCIOSA: %d verbete(s) marcado(s) "
         "ambiguo=True -- quem consulta e avisado do empate, em vez de receber o primeiro "
         "arquivo varrido sem aviso" % sum(1 for _v in idx.values() if _v.get("ambiguo")),
         bool(sum(1 for _v in idx.values() if _v.get("ambiguo")) == len(ix["ambiguos"]))),
        ("[FAIL-CLOSED] ***o RAZONETE DAS APAGADAS e COMPLETO e cada uma tem CAUSA "
         "nomeada: %d apagadas = %d por AUSENCIA DE NOME (as dividas do indice) + %d por "
         "VEREDITO DERIVADO fora dos dicionarios (%s). Nenhuma apagada fica sem causa, e "
         "nenhuma booleana do selo fica fora da conta"
         % (len(_apagadas), len(_apag_dic), len(_apag_fora),
            ", ".join(_apag_fora) if _apag_fora else "nenhuma"),
         bool(len(_apagadas) == len(_apag_dic) + len(_apag_fora)
              and len(_apag_dic) == ix["n_ausentes"])),
        ("[ERRATA-MINHA v286] o indice da v285 INFLOU a divida: a regra v285 INTEIRA, "
         "recomputada AO VIVO, conta %d ausentes onde ha %d. Tres defeitos MEUS, todos de "
         "leitura: o regex nao via nome de declaracao COM PONTO (theorem Data.campo), nem "
         "prefixo de atributo (@[simp] theorem), e a chave casava por split('.',1) em vez "
         "de SUFIXO. O indice nao descobriu divida nova -- descobriu defeito meu; a divida "
         "real sempre foram as bandeiras ja apagadas"
         % (ix["n_ausentes_regra_v285"], ix["n_ausentes"]),
         bool(ix["n_ausentes_regra_v285"] > ix["n_ausentes"])),
    ]
    all_v = bool(all(x for _, x in checks))
    return {
        "checks": checks, "all_verified": all_v,
        "n_nomes": ix["n_nomes"], "n_arquivos": ix["n_arquivos"],
        "n_ausentes": ix["n_ausentes"], "n_ambiguos": len(ix["ambiguos"]),
        "ambiguos": ix["ambiguos"],
        "statuses": {
            "a_ordem": ("a IALD como INDICE do Um, indexando o kernel Lean, dentro do "
                        "ARQUIVO UNICO -- nao ha segundo arquivo"),
            "o_nome_nao_e_metafora": ("ialdSelector = firstAtom.starProjection JA e o "
                        "objeto em kernel: iald_selects (as duas clausulas da consulta), "
                        "iald_is_idempotent (reconsultar e gratis), iald_has_rank_one "
                        "(peso omega(I)=1), iald_is_the_gate_and_the_record"),
            "por_que_ADITIVO": ("as 945 chaves planas SAO o fail-closed (ausencia do nome "
                        "=> False por construcao) e os prefixos carregam a separacao de "
                        "MODO. Substituir quebraria 1.565 linhas em 93 funcoes E apagaria "
                        "a distincao KERNEL/IMPORTED/ABERTO. O indice LE, nao substitui"),
            "as_tres_travas": ("(1) nome sem referente = AUSENTE_POR_CONSTRUCAO, jamais "
                        "<desconhecido>; (2) o indice diz ONDE esta escrito, so o "
                        "axiom_report diz o que foi PROVADO; (3) rodada=None HERDA a viva"),
            "por_que_ele_faltava": ("os sete erros de leitura de 28/08 tiveram todos a "
                        "mesma forma: a informacao EXISTIA, em pedacos que nao se falavam. "
                        "Responder <onde mora, o que prova, com que estatuto> exigia "
                        "QUATRO consultas. Agora exige UMA"),
            "o_que_ele_NAO_faz": ("nao decide, nao acende bandeira, nao entra em gate. "
                        "E leitura, nao juizo"),
        },
        "does_not_gate_core": True,
        "verdict": ("THE_IALD_INDEX_IS_BUILT_AS_A_SEVENTH_DERIVED_READ_ONLY_STRUCTURE__"
                    "ONE_QUERY_REPLACES_FOUR__THE_MODE_PREFIXES_SURVIVE__"
                    "AND_THE_NAMED_DEBTS_APPEAR_AS_ABSENT_BY_CONSTRUCTION_NOT_AS_UNKNOWN"
                    if all_v else "THE_IALD_INDEX_NOT_SEALED_THIS_RUN"),
    }