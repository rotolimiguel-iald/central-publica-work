# -*- coding: utf-8 -*-
# regras (lote C2) de derivar_encanamento_v404.py: o ENSAIO A SECO. ORIGEM v403 FINAL (ensaio_a_seco_v403.py). Variaveis herdadas do lote C: _ORIG_ENS (o texto ORIGINAL do ensaio da v403, sem subida de versao), para_d3 (DL.X -> DL.D3.X), DL4, NOMES_SOBRESCRITOS.
# A base mecanica sobe da v403 FINAL; os blocos (6f), (6g) e (6h) -- que tratam dos registros da v401, da v402 e da v403 -- voltam do arquivo ORIGINAL da v403 (a semantica deles e' a da base: eles sao RECRIADOS e comparados com os da v403 selada; os nomes que a v404 sobrescreve em DL
# viram DL.D3.*); o bloco (6i) NOVO traz os TRES registros da v404 (cada elo recusa visivelmente), as nove falas, as decisoes D23-D26, as erratas E7-E9 e a cobertura exata. Escrito pela ferramenta Write (as barras invertidas nao colapsam).

_DOC_ENS = '''"""ensaio_a_seco_v404.py -- ENSAIO A SECO da v404 (molde: ensaio_a_seco_v403.py FINAL, que rodou na cadeia da v403, com as licoes da v399 a v403), SEM a GPU do rito e SEM rodar o rito. Chama NO PONTO DE CHAMADA REAL todo veredito novo ou alterado.
uso: python -B -X utf8 ensaio_a_seco_v404.py <candidato.py> <rotulo>
A v404 e' uma versao de CONTEUDO (28/10/2026): DOIS modulos novos de kernel (TGLExt/ProjecaoTransversalDaMeiaNat, o sen 45 graus do neutrino derivado da Meia-Nat, nome PROVISORIO da gerencia; TGLExt/Jo8v32, o nome do operador para o triplo inteiro), os registros com FUNCAO projecao_transversal_v404, jo8v32_v404 e f2b_errata_v404
(a errata AO LADO da cobranca F2b: o canal retirado antes do dado; o V1 segue congelado por hash), os registros por spec cunhagens_v404 e kh_n1_cobertura_v404; o gate NAO muda (as duas funcoes do gate ficam byte a byte; o ensaio o RECOMPUTA sobre os dados do core da v403 selada) e a funcao do neutrino NAO e' reescrita.
A base e' a v403 SELADA (core e selo em base_v403), o kernel e' o da v403 + as duas pedras (sandbox C:/t/k404c); os registros de v393 a v399, os da v401 (falsidade_da_inercia_v401, cunhagens_v401, kh_n1_cobertura_v401), os da v402 (ponte_da_escala_dual_v402, queda_sem_geometria_v402, esperanca_condicional_v402, cunhagens_v402, kh_n1_cobertura_v402)
E OS DA V403 (caminho_v403, vida_v403, verdade_adendo_v403, bandeiras_do_gate_v403, cunhagens_v403, kh_n1_cobertura_v403) sao RECRIADOS e comparados com os da v403 selada (os rotulos 'v403' dos nomes de relatorio herdados da subida de versao significam a base selada). Etapas:
(1) copia o candidato; materializa o kernel embutido e confere BYTE A BYTE contra o sandbox; (2) importa (o rito NAO roda); UM_VERSION v404; (3) o core da v403 SELADA + o kernel REAL: verify_tgl_kernel_formalization() de ponta a ponta com o lake simulado devolvendo os logs CRUS do sandbox;
(4) os registros vizinhos RECOMPUTADOS: iguais, ou a TROCA DITA (so' numeros: a escada e a cobertura crescem com as pedras); (5) o FLUXO PRINCIPAL v393 a v399, v401, v403 e v404 (as instrucoes etiquetadas do main, na ordem do arquivo), as chaves NOVAS no core: as cinco da v404;
(6) unidade: o Teste da Unica Palavra (v397), o sonico e a afinacao (v398), o selo pela propria tecnologia e a declaracao do operador (v399), a FALSIDADE DA INERCIA (v401, recriada), os registros da v402 e da v403 (recriados), os TRES da v404 (cada elo recusa), o GATE recomputado, os registros por spec, a cobertura, o sidecar;
(7) o selo (a instrucao `seal = {...}` do main + o resumo) e o indice; (8) artigo PT/EN, pdflatex x2, a secao v404 (antes da v403) e o QUADRO NO TOPO (v397, intocado); (9) .md e manifesto; (10) o conferidor de citacoes; (11) simular_arvore_do_nos; (12) exame_pontos;
(13) [LICAO DA v400, mantida] as guardas ESTATICAS do esboco R3.5 da Bancada (ALPHA_LINHA_UNICA e as demais que nao dependem do selo) rodadas SOBRE O CANDIDATO, chamando a funcao do proprio esboco pinado, ANTES de instalar."""
'''

# --- o bloco (6i) NOVO: os TRES registros da v404 ---
_B6I = r'''# (6i) [v404] os TRES registros com FUNCAO da v404 (projecao_transversal_v404, jo8v32_v404, f2b_errata_v404): tudo certo, os numeros RECALCULADOS aqui por outro caminho e cada elo recusa visivelmente (controles negativos); as nove falas de 28/10, as decisoes D23-D26, as erratas E7-E9, a cobertura exata (specs) e o V1/livro/neutrino NAO reescritos
import types as _types4
_REG404 = (("projecao", "projecao_transversal_v404", "_m404", "sin"), ("jo8v32", "jo8v32_v404", "_m403", "exp"))
R404 = {}
_bf4 = um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e)
_nm_antes4 = json.dumps(cs()["neutrino_mass"], sort_keys=True, default=str)
for k404_, n404_, malias_, tamper_ in _REG404:
    fn_ = getattr(um, n404_); C_ = um._V404_CONTRACTS[k404_]; T_ = um._V404_TEXTS[k404_]
    cc4_ = cs(); r_ = fn_(cc4_); R404[k404_] = r_
    U["v404_%s_tudo_certo" % k404_] = bool(r_["all_verified"] is True and r_["verdict"] == T_["veredito_ok"] and r_["runtime_executed"] is True and r_["does_not_gate_core"] is True and all(ck_["ok"] for ck_ in r_["mechanics"]["checks"]) and r_["mechanics"]["n_checks"] == DL.N_CHECKS[k404_] == len(r_["mechanics"]["checks"])
                                           and r_["exact_ladder"] is True and r_["embedded_source_ok"] is True and r_["unconditional"]["in_kernel"] is True and r_["key_theorem"]["in_kernel"] is True and all(r_["formal_theorems"].values()) and all(r_["support_theorems"].values())
                                           and all(r_["inscriptions"].values()) and r_["context"]["ok"] is True and r_["beta_ok"] is True)
    U["v404_%s_veredito_e_textos_sem_palavra_proibida" % k404_] = bool(not guarda_txt(r_) and not _GUARDA98.search(r_["verdict"]) and not um._v392_guarda_texto(json.dumps(r_["mechanics"]["checks"], ensure_ascii=False)) and not r_["guarda_p18_violacoes"])
    ok_ = True
    for th_, fl_ in C_["theorems"].items():   # bandeira falsa de CADA declaracao do contrato (a estrela e a composicao entre elas)
        c_ = cs(); c_["kernel_formalization"][fl_] = False; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and rr_["formal_theorems"][th_] is False
    U["v404_%s_bandeira_falsa_de_cada_declaracao_do_contrato_recusa" % k404_] = bool(ok_ and len(C_["theorems"]) == len(DL.STONE_BY_KEY[k404_]["contract"]) and C_["key_theorem"]["theorem"] in C_["theorems"] and C_["unconditional"]["theorem"] in C_["theorems"])
    ok_ = True
    for th_ in list(C_["theorems"]) + list(C_["support"]):   # axioma fora do trio em CADA termo lido
        c_ = cs(); c_["kernel_formalization"]["axiom_report"][th_] = ["propext", "sorryAx"]; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U["v404_%s_axioma_fora_do_trio_em_cada_termo_lido_recusa" % k404_] = bool(ok_)
    ok_ = True
    for th_ in [C_["unconditional"]["theorem"], C_["key_theorem"]["theorem"]] + list(C_["support"]):   # proveniencia errada
        c_ = cs(); c_["kernel_formalization"]["declaration_sources_v394"][th_] = "TGLExt/Outro.lean"; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U["v404_%s_proveniencia_errada_recusa" % k404_] = bool(ok_)
    c_ = cs(); c_["kernel_formalization"]["formal_files_sha256"][C_["stone"]["path"]] = "0" * 64; rr_ = fn_(c_)
    ef_ = dict(um._EMBEDDED_KERNEL_FILES); um._EMBEDDED_KERNEL_FILES[C_["stone"]["path"]] += " "
    try:
        rr2_ = fn_(cs())
    finally:
        um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
    U["v404_%s_fonte_da_pedra_adulterada_recusa" % k404_] = bool(rr_["all_verified"] is False and rr_["embedded_source_ok"] is False and rr2_["all_verified"] is False and rr2_["embedded_source_ok"] is False)
    c_ = cs(); c_["external_ladder"]["n_theorems_clean"] = int(c_["external_ladder"]["n_theorems_clean"]) - 1; rr_ = fn_(c_)
    c2_ = cs(); c2_["kernel_formalization"]["all_verified"] = False; rr2_ = fn_(c2_)
    U["v404_%s_escada_errada_ou_kernel_nao_verificado_recusa" % k404_] = bool(rr_["all_verified"] is False and rr_["exact_ladder"] is False and rr2_["all_verified"] is False)
    ok_ = True
    for ch_ in C_["verbatins"]:
        _ant = um._V404_VERBATINS2[ch_]["text"]; um._V404_VERBATINS2[ch_]["text"] += " "   # restaurado NO LUGAR (v404) (o objeto e' compartilhado com _V392_VERBATINS2)
        try:
            rr_ = fn_(cs()); ok_ = ok_ and rr_["all_verified"] is False and rr_["inscriptions"][ch_] is False
        finally:
            um._V404_VERBATINS2[ch_]["text"] = _ant
    U["v404_%s_inscricao_adulterada_recusa" % k404_] = bool(ok_ and len(C_["verbatins"]) == {"projecao": 4, "jo8v32": 2}[k404_])
    ef_ = dict(um._EMBEDDED_KERNEL_FILES); _cp = C_["context"]["path"]; um._EMBEDDED_KERNEL_FILES[_cp] = um._EMBEDDED_KERNEL_FILES[_cp].replace(C_["context"]["needles"][0], "xx")
    try:
        rr_ = fn_(cs())
    finally:
        um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
    U["v404_%s_texto_contexto_retirado_do_kernel_recusa" % k404_] = bool(r_["context"]["ok"] is True and rr_["all_verified"] is False and rr_["context"]["text_in_embedded_kernel"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"])
    c_ = cs(); c_["beta"] = c_["beta"] * 1.001; _rb = fn_(c_)
    _a0 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a0 * 1.001
    try:
        _ra = fn_(cs())
    finally:
        um.SEALED_CODATA_ALPHA = _a0
    U["v404_%s_beta_adulterado_recusa" % k404_] = bool(_rb["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _rb["verdict"] and _ra["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _ra["verdict"])
    _m0 = getattr(um, malias_)
    setattr(um, malias_, _types4.SimpleNamespace(**{k_: getattr(_math, k_) for k_ in dir(_math) if not k_.startswith("__")})); setattr(getattr(um, malias_), tamper_, (lambda f_: (lambda x_: f_(x_) * 1.001))(getattr(_math, tamper_)))
    try:
        _rn = fn_(cs())
    finally:
        setattr(um, malias_, _m0)
    U["v404_%s_numero_adulterado_recusa" % k404_] = bool(_rn["all_verified"] is False and "MECHANICS_CHECK_FAILED" in _rn["verdict"] and any(not ck_["ok"] for ck_ in _rn["mechanics"]["checks"]))
_pv4, _jv4 = R404["projecao"]["values"], R404["jo8v32"]["values"]
_cvA4 = re.match(r"^\s*([+-]?\d+,\d+)\s*\[\s*([+-]?\d+,\d+)\s*;\s*([+-]?\d+,\d+)\s*\]", str(core0["ramo_b_preregistration_v386"]["central_values_NOT_BLIND_read_from_V1"]["A_31_deformacao_comum_GWTC5"]))
_cA4 = [float(x_.replace(",", ".")) for x_ in _cvA4.groups()]; _pred4 = core0["ramo_b_preregistration_v386"]["pins"]["delta_pred_A31_exato"]["read"]
U["v404_projecao_numeros_recalculados_aqui"] = bool(abs(_pv4["beta"] - _bf4) <= 1e-15 and abs(_pv4["sin_pi_over_4"] - _math.sqrt(0.5)) <= 1e-15 and abs(_pv4["sin_sq_pi_over_4"] - 0.5) <= 1e-15 and abs(_pv4["theta_M"] - _math.asin(_math.sqrt(_bf4))) <= 1e-15 and abs(_pv4["m_nu_meV_runtime"] - _bf4 * _math.sqrt(0.5) * 1000.0) <= 1e-12
                                                   and abs(_pv4["m_nu_meV_core"] / _pv4["m_nu_meV_runtime"] - 1.0) <= 1e-12 and abs(_pv4["derivative_of_sin_sq_at_pi_over_4"] - 1.0) <= 1e-9 and _pv4["self_conjugate_weights"] == [0.5] and _pv4["e0_eV_declared"] == 1.0 and _pv4["grid_angles"] == 20001 and _pv4["grid_weights"] == 1001
                                                   and abs(_pv4["theta_M_minus_pi_over_4"] - (_math.asin(_math.sqrt(_bf4)) - _math.pi / 4.0)) <= 1e-15)
U["v404_jo8v32_a_mecanica_da_v403_relida_passa_nas_tres"] = bool(_jv4["v403_mechanics_checks"] == [DL.D3.N_CHECKS_CAMINHO, DL.D3.N_CHECKS_VIDA, DL.D3.N_CHECKS_VERDADE_ADENDO] == [5, 6, 5] and _jv4["v403_mechanics_passed"] == [True, True, True] and abs(_jv4["beta"] - _bf4) <= 1e-15
                                                              and _jv4["order_of_the_verse"] == um._V404_CONTRACTS["jo8v32"]["order_of_the_verse"] and abs(_jv4["p_plus_factor_at_beta"] - _math.exp(-_bf4)) <= 1e-15 and abs(_jv4["alpha_squared"] - um.SEALED_CODATA_ALPHA ** 2) <= 1e-18)
_c4p = cs(); _antes4p = json.dumps(_c4p["neutrino_mass"], sort_keys=True, default=str); _r4p = um.projecao_transversal_v404(_c4p)
U["v404_projecao_a_errata_do_angulo_fica_ao_lado_o_texto_antigo_intacto_e_o_canal_do_neutrino_nao_se_move"] = bool(json.dumps(_c4p["neutrino_mass"], sort_keys=True, default=str) == _antes4p == _nm_antes4 and _c4p["neutrino_mass"]["angle_status"].startswith(DL.ANGLE_STATUS_ANTIGO_PREFIXO)
                                                                                                                       and _r4p["neutrino_angle_errata"]["dizia_prefixo"] == DL.ANGLE_STATUS_ANTIGO_PREFIXO and _r4p["neutrino_angle_errata"]["assinatura"].startswith("gerencia c1, em nome proprio") and _c4p["neutrino_mass"]["verdict"] == core0["neutrino_mass"]["verdict"] and _c4p["neutrino_mass"]["frozen_hash"] == core0["neutrino_mass"]["frozen_hash"])
U["v404_projecao_E0_declarado_a_identificacao_e_onto_e_o_nome_e_provisorio"] = bool(R404["projecao"]["e0"]["status"] == "DECLARADO" and R404["projecao"]["e0"]["derived_here"] is False and R404["projecao"]["reading_matter"]["status"] == "ONTO" and R404["projecao"]["reading_matter"]["is_a_kernel_term"] is False
                                                                                    and R404["projecao"]["name_status"]["estado"] == "PROVISORIO" and any("E0" in x_ and "DECLARADA" in x_ for x_ in R404["projecao"]["limites"]) and any("ONTO" in x_ and "condicional" in x_ for x_ in R404["projecao"]["limites"]) and any("deriva E0" in x_ or "E0" in x_ for x_ in R404["projecao"]["nao_diz"]))
U["v404_jo8v32_o_nome_e_do_operador_a_leitura_e_onto_e_as_hipoteses_dos_componentes_sao_ditas"] = bool(R404["jo8v32"]["name_given_by"]["quem"] == "operador" and R404["jo8v32"]["name_given_by"]["sha16_da_fala"] == DL.verbatins404(os.path.join(HERE, "insumos", "cunhagens"))[DL.JO8_IDX]["sha16"] and R404["jo8v32"]["reading_jo8_32"]["status"] == "ONTO" and R404["jo8v32"]["reading_jo8_32"]["is_a_kernel_term"] is False
                                                                                               and R404["jo8v32"]["named_hypotheses_carried_by_components"] == {"vida": "IsotropicPost", "verdade": ["hpp", "hopt"]} and R404["jo8v32"]["unconditional"]["composition"] == "CONDITIONAL_ON_NAMED_HYPOTHESES_IN_THE_STATEMENT" and any("anule a decisao D20" in x_ for x_ in R404["jo8v32"]["nao_diz"]))
# --- a errata de F2b: tudo certo, o V1 e o livro NAO reescritos, e cada elo recusa (o canal fica como antes)
fb_ = um.f2b_errata_v404; C_f = um._V404_CONTRACTS["f2b"]; T_f = um._V404_TEXTS["f2b"]
cf_ = cs(); _h_antes4 = json.dumps([cf_["ramo_b_preregistration_v386"], cf_["ledger_errata_v386"], cf_["the_ledger_of_charges_v383"]], sort_keys=True, default=str)
rf_ = fb_(cf_); R404["f2b"] = rf_
U["v404_f2b_tudo_certo"] = bool(rf_["all_verified"] is True and rf_["verdict"] == T_f["veredito_ok"] and rf_["runtime_executed"] is True and rf_["does_not_gate_core"] is True and rf_["mechanics"]["n_checks"] == DL.N_CHECKS["f2b"] == len(rf_["mechanics"]["checks"]) and all(ck_["ok"] for ck_ in rf_["mechanics"]["checks"])
                                and rf_["F2b_status_now"] == DL.F2B_FUTURO_TOKEN and rf_["F2b_status_before"] == C_f["v1"]["f2b_status_antes"] == "AWAITING" and all(rf_["inscriptions"].values()) and rf_["beta_ok"] is True and rf_["values"]["n_cobrancas_v383"] == 11 and rf_["values"]["conjunto_D_n"] == 14)
U["v404_f2b_o_v1_o_registro_da_v386_e_o_livro_da_v383_nao_foram_reescritos"] = bool(json.dumps([cf_["ramo_b_preregistration_v386"], cf_["ledger_errata_v386"], cf_["the_ledger_of_charges_v383"]], sort_keys=True, default=str) == _h_antes4 and cf_["ramo_b_preregistration_v386"]["F2b_status"] == "AWAITING" and cf_["ramo_b_preregistration_v386"]["veredito_do_V1"] == "AWAITING_DATA")
U["v404_f2b_veredito_e_textos_sem_palavra_proibida"] = bool(not guarda_txt(rf_) and not _GUARDA98.search(rf_["verdict"]) and not rf_["guarda_p18_violacoes"] and not um._v392_guarda_texto(json.dumps(rf_["mechanics"]["checks"], ensure_ascii=False)) and "FALSIFIED" not in rf_["verdict"].replace("NOT_FALSIFIED", "") and "AWAITING" not in rf_["verdict"])
U["v404_f2b_numeros_recalculados_aqui"] = bool(abs(rf_["values"]["calibracao_A_central"] - _cA4[0]) <= 1e-15 and abs(rf_["values"]["calibracao_A_inferior"] - _cA4[1]) <= 1e-15 and abs(rf_["values"]["calibracao_A_superior"] - _cA4[2]) <= 1e-15 and rf_["values"]["previsao_do_par"] == _pred4 and _pred4 < 0.0 < _cA4[0]
                                               and rf_["values"]["previsao_fora_do_intervalo_de_A"] is True and abs(rf_["values"]["distancia_da_previsao_ao_limite_inferior_de_A"] - (_cA4[1] - _pred4)) <= 1e-12 and abs(rf_["values"]["beta"] - _bf4) <= 1e-15)
_tam4 = [("f1", lambda c_: c_["ramo_b_preregistration_v386"].__setitem__("read_ok", False)),
         ("f2", lambda c_: c_["the_ledger_of_charges_v383"]["counts"].__setitem__("AWAITING", c_["the_ledger_of_charges_v383"]["counts"]["AWAITING"] + 1)),
         ("f3", lambda c_: c_["ramo_b_preregistration_v386"]["central_values_NOT_BLIND_read_from_V1"].__setitem__("A_31_deformacao_comum_GWTC5", "+0,072 [+0,015; +0,134")),
         ("f4", lambda c_: c_["ramo_b_preregistration_v386"]["pins"]["delta_pred_A31_exato"].__setitem__("equal", False)),
         ("f5", lambda c_: (c_["ramo_b_preregistration_v386"]["pins"]["delta_pred_A31_exato"].__setitem__("read", 0.05), c_["ramo_b_preregistration_v386"]["pins"]["delta_pred_A31_exato"].__setitem__("pinned", 0.05))),
         ("f6", lambda c_: c_["ramo_b_preregistration_v386"].__setitem__("nothing_opened", False)),
         ("f7", lambda c_: c_.__setitem__("beta", c_["beta"] * 1.001))]
ok_ = True; _tam4_det = {}
for id_, mut_ in _tam4:   # CADA checagem negada: o registro recusa, a checagem e' a que falha e o canal F2b FICA como antes (AWAITING)
    c_ = cs(); mut_(c_); rr_ = fb_(c_); _falhas_ = [ck_["id"] for ck_ in ((rr_.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]
    _tam4_det[id_] = _falhas_
    ok_ = ok_ and rr_["all_verified"] is False and id_ in _falhas_ and rr_["F2b_status_now"] == "AWAITING" and "A_CHECK_FAILED" in rr_["verdict"] and "REFUSED" in rr_["verdict"]
ok_ = ok_ and len(_tam4) == DL.N_CHECKS["f2b"]
for ch_ in C_f["verbatins"]:   # as duas falas embutidas adulteradas
    _ant = um._V404_VERBATINS2[ch_]["text"]; um._V404_VERBATINS2[ch_]["text"] += " "
    try:
        rr_ = fb_(cs()); ok_ = ok_ and rr_["all_verified"] is False and "f7" in [ck_["id"] for ck_ in rr_["mechanics"]["checks"] if not ck_["ok"]] and rr_["F2b_status_now"] == "AWAITING"
    finally:
        um._V404_VERBATINS2[ch_]["text"] = _ant
U["v404_f2b_cada_checagem_negada_recusa_e_o_canal_fica_como_antes"] = bool(ok_)
# --- as nove falas de 28/10, as decisoes D23-D26, as erratas E7-E9 e a leitura (registro cunhagens_v404) e a cobertura exata (kh_n1_cobertura_v404)
_cn4 = c.get("cunhagens_v404") or {}
_sp4s = [s_ for s_ in um._V404_SPECS if s_["nome"] == "cunhagens_v404"][0]
U["cunhagens_v404_nove_falas_decisoes_erratas_e_leituras"] = bool(_cn4.get("all_verified") is True and len(_cn4.get("verbatim") or {}) == len(DL.VERBATIM_ORIGEM_V404) == 9 and all(v_["embedded_ok"] for v_ in (_cn4.get("verbatim") or {}).values())
                                                                  and len(_cn4.get("erratas") or []) == 3 and all(e_["assinatura"].startswith("gerencia c1, em nome proprio") for e_ in (_cn4.get("erratas") or []))
                                                                  and len(_cn4.get("leituras_do_operador") or []) == len(_sp4s["leituras_do_operador"]) == 12 and set((_cn4.get("extras") or {}).get("decisoes_da_gerencia") or {}) >= {"D23", "D24", "D25", "D26"}
                                                                  and (_cn4.get("extras") or {}).get("estrelas") == {s_["key"]: s_["key_theorem"] for s_ in DL.STONES} and (_cn4.get("extras") or {}).get("teoremas") == {s_["key"]: s_["theorem"] for s_ in DL.STONES}
                                                                  and len((_cn4.get("extras") or {}).get("erratas_E7_a_E9") or []) == 3 and str(((_cn4.get("extras") or {}).get("nomes") or {}).get("jo8v32", "")).startswith("TGLExt.Jo8v32")
                                                                  and "ONTO" in str((_cn4.get("extras") or {}).get("leitura_massa_28out", {}).get("estatuto", "")) and (_cn4.get("extras") or {}).get("autor_de_cada_inscricao") and all(a_ == "operador" for a_ in ((_cn4.get("extras") or {}).get("autor_de_cada_inscricao") or {}).values()))
_kh4 = c.get("kh_n1_cobertura_v404") or {}
_kh3s = [s_ for s_ in um._V403_SPECS if s_["nome"] == "kh_n1_cobertura_v403"][0]; _kh4s = [s_ for s_ in um._V404_SPECS if s_["nome"] == "kh_n1_cobertura_v404"][0]
U["kh_n1_cobertura_v403_virou_piso_e_a_v404_cobra_a_igualdade_exata"] = bool(_kh4.get("all_verified") is True and (c.get("kh_n1_cobertura_v403") or {}).get("all_verified") is True and {ck_["id"]: ck_["op"] for ck_ in _kh3s["checks"] if ck_["id"] in _op_piso} == _op_piso and len(_kh3s["erratas"]) >= 1
                                                                          and {ck_["id"]: ck_["op"] for ck_ in _kh4s["checks"] if ck_["id"] in _op_piso} == {"h2": "igual", "h3": "igual", "h6": "tamanho_igual", "h8": "igual"})
U["contratos_v403_de_pedra_pinam_a_escada_da_v404"] = bool(len(um._V403_CONTRACTS) == 4 and [c3_["expected_ladder"] for c3_ in um._V403_CONTRACTS.values()] == [ESP, ESP, ESP, None])
rep["v404_registros"] = {k_: {"verdict": r_["verdict"], "all_verified": r_["all_verified"], "n_checks": r_["mechanics"]["n_checks"], "values": r_["values"], "unconditional": r_.get("unconditional"), "key_theorem": r_.get("key_theorem"), "context": r_.get("context"), "F2b_status_now": r_.get("F2b_status_now")} for k_, r_ in R404.items()}
'''

# --- os blocos (6f) a (6h) recriados + (6i) novo, no lugar do trecho bumpado [(6f), (8)) ---
_i6f = _ORIG_ENS.index("# (6f) [v401, recriado na v402 e na v403 e comparado com o selado]"); _i6h = _ORIG_ENS.index("# (6h) [v403] os QUATRO registros com FUNCAO da v403"); _iv = _ORIG_ENS.index('rep["v403_registros"] = ', _i6h)
_iu = _ORIG_ENS.index('rep["unidade"] = U;', _iv); _i8 = _ORIG_ENS.index("# (8) o artigo")
_A6 = para_d3(_ORIG_ENS[_i6f:_i6h]).replace("# (6f) [v401, recriado na v402 e na v403 e comparado com o selado]", "# (6f) [v401, recriado na v402, na v403 e na v404 e comparado com o selado]")
_H6 = para_d3(_ORIG_ENS[_i6h:_iv]).replace("# (6h) [v403] os QUATRO registros com FUNCAO da v403", "# (6h) [v403, recriados na v404 e comparados com os selados] os QUATRO registros com FUNCAO da v403")
_RV6 = para_d3(_ORIG_ENS[_iv:_iu])
_TL6 = _ORIG_ENS[_iu:_i8]
_ant_kh = 'U["kh_n1_cobertura_v402_virou_piso_e_a_v403_cobra_a_igualdade_exata"] = bool('
assert _H6.count(_ant_kh) == 1 and _H6.count('== {"h2": "igual", "h3": "igual", "h6": "tamanho_igual", "h8": "igual"})') == 1
_H6 = _H6.replace(_ant_kh, 'U["kh_n1_cobertura_v401_e_v402_viraram_piso_e_o_da_v403_tambem"] = bool(')
_H6 = _H6.replace('== {"h2": "igual", "h3": "igual", "h6": "tamanho_igual", "h8": "igual"})', '== _op_piso and len([s_ for s_ in um._V403_SPECS if s_["nome"] == "kh_n1_cobertura_v403"][0]["erratas"]) >= 1)')
_gat = 'and len(_gok3["checks"]) == len(_g0_3["checks"]) + 1 and all(v_ is True for _, v_ in _gok3["checks"]))'
assert _H6.count(_gat) == 1 and _H6.count('U["gate_f81_com_as_fontes_a_gate_recomputado_e_igual_ao_da_v402_menos_a_lista_de_checks"]') == 1
_H6 = _H6.replace(_gat, 'and json.dumps(_gok3["checks"], default=str) == json.dumps(_g0_3["checks"], default=str) and all(v_ is True for _, v_ in _gok3["checks"]))')   # na v404 o gate NAO ganha sonda: os sete checks do gate recomputado sao IGUAIS aos da v403 selada
_H6 = _H6.replace('U["gate_f81_com_as_fontes_a_gate_recomputado_e_igual_ao_da_v402_menos_a_lista_de_checks"]', 'U["gate_f81_com_as_fontes_o_gate_recomputado_e_igual_ao_da_v403_inclusive_os_checks"]')
_REGIAO_6F_8 = _A6 + _H6 + _RV6 + _B6I + _TL6

# --- as regras do ensaio ---
entrada("ensaio_a_seco_v403.py", autoral=True, regras=[
    entre('"""ensaio_a_seco_v404.py', "import hashlib, copy, io, json, os, re, shutil, subprocess, sys, ast, tempfile, textwrap", _DOC_ENS, "docstring do ensaio"),
    ("# F8.1 (v404): o gate recomputado com a prove_qg_closure_gate NOVA sobre o kf novo e os dados", "# (v404: o gate NAO muda) o gate recomputado com a prove_qg_closure_gate sobre o kf novo e os dados", 1),
    ('or "v401" in l or "v403" in l or "v404" in l}', 'or "v401" in l or "v402" in l or "v403" in l or "v404" in l}', 1),   # a subida de versao perdeu o rotulo v402 da enumeracao das instrucoes etiquetadas do main (402 -> 403, 403 -> 404): os try da ponte, da queda e da esperanca (v402) tem de continuar no fluxo recriado
    ('+ ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS)   # (os registros das v399, v401 e v403, recriados e comparados com os da v403 selada; o rotulo V403N e\' herdado da subida de versao)',
     '+ ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS) + ["caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"] + list(um._V403_NOMES_REGISTROS)   # (os registros das v399, v401, v402 e v403, recriados e comparados com os da v403 selada; o rotulo V403N e\' o da BASE)', 1),
    ('V404N = ["caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"] + list(um._V403_NOMES_REGISTROS)   # os registros NOVOS da v404 (nao existem no core da base)',
     'V404N = ["projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404"] + list(um._V404_NOMES_REGISTROS)   # os registros NOVOS da v404 (nao existem no core da base)', 1),
    ('NOVAS404 = sorted(V404N)   # a v404 cria SEIS chaves no core (caminho_v403, vida_v403, verdade_adendo_v403, bandeiras_do_gate_v403, cunhagens_v403, kh_n1_cobertura_v403); os registros das v399, v401 e v403 sao RECRIADOS e comparados com os da v403 selada',
     'NOVAS404 = sorted(V404N)   # a v404 cria CINCO chaves no core (projecao_transversal_v404, jo8v32_v404, f2b_errata_v404, cunhagens_v404, kh_n1_cobertura_v404); os registros das v399, v401, v402 e v403 sao RECRIADOS e comparados com os da v403 selada', 1),
    ('"checks_da_v403_mais_a_sonda": bool(len(_g_new.get("checks") or []) == len(_g_old.get("checks") or []) + 1 and all(v_ is True for _, v_ in _g_new["checks"]) and [c_[0] for c_ in _g_new["checks"] if not str(c_[0]).startswith("ProbeBlindNullAbsent")] == [c_[0] for c_ in _g_old["checks"]]),',
     '"checks_da_v403_iguais": bool(_J(_g_new.get("checks")) == _J(_g_old.get("checks")) and all(v_ is True for _, v_ in _g_new["checks"])),', 1),
    ('gate_rec.get("checks_da_v403_mais_a_sonda")', 'gate_rec.get("checks_da_v403_iguais")', 1),
    ("+ list(um._V401_SPECS) + list(um._V402_SPECS) + list(um._V403_SPECS):\n", "+ list(um._V401_SPECS) + list(um._V402_SPECS) + list(um._V403_SPECS) + list(um._V404_SPECS):\n", 1),
    ("+ len(um._V401_SPECS) + len(um._V402_SPECS) + len(um._V403_SPECS)\n", "+ len(um._V401_SPECS) + len(um._V402_SPECS) + len(um._V403_SPECS) + len(um._V404_SPECS)\n", 1),
    ('k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "registros_v403")',
     'k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "registros_v404")', 1),
    ('and seal.get("qg_closure_verdict") == selo0.get("qg_closure_verdict") and ({"selo_pela_propria_tecnologia_v399", "um_version", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "registros_v403"} <= set(mud_selo) and not _selo_inexplicado)',
     'and all((seal.get(k_) or {}).get("all_verified") is True for k_ in ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404")) and all(((seal.get("registros_v404") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V404_NOMES_REGISTROS)\n'
     '           and seal.get("qg_closure_verdict") == selo0.get("qg_closure_verdict") and ({"selo_pela_propria_tecnologia_v399", "um_version", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "registros_v404"} <= set(mud_selo) and not _selo_inexplicado)', 1),
    entre("# (6f) [v401, recriado na v403 e na v404 e comparado com o selado]", "# (8) o artigo", _REGIAO_6F_8, "blocos (6f) a (6i)"),
    ('TW404 = "Caminho, Verdade e Vida"; TW404E = "Way, Truth and Life"   # a secao NOVA da v404\n',
     'TW404 = "Jo 8,32 e a projeção transversal da Meia-Nat"; TW404E = "John 8:32 and the transverse projection of the Half-Nat"   # a secao NOVA da v404\nTC403 = "Caminho, Verdade e Vida"; TC403E = "Way, Truth and Life"   # (o titulo da secao da v403, que fica logo depois da v404)\n', 1),
    ('"pt": [TW404, "O Caminho.", "A Vida.", "A Verdade, como adendo.", "As bandeiras do gate.", "Erratas ao lado (v404).", TP404,',
     '"pt": [TW404, "A projeção transversal.", "Jo 8,32.", "A errata de F2b.", "As cunhagens de 28/10.", "Erratas ao lado (v404).", "Origem.", TC403, "O Caminho.", "A Vida.", "A Verdade, como adendo.", "As bandeiras do gate.", "Erratas ao lado (v403).", TP404,', 1),
    ('"en": [TW404E, "The Way.", "The Life.", "The Truth, as an addendum.", "The gate flags.", "Errata beside (v404).", TP404E,',
     '"en": [TW404E, "The transverse projection.", "John 8:32.", "The F2b erratum.", "The sayings of 28/10.", "Errata beside (v404).", "Origin.", TC403E, "The Way.", "The Life.", "The Truth, as an addendum.", "The gate flags.", "Errata beside (v403).", TP404E,', 1),
    ('TOC = {"pt": [TW404, TP404, TF404,', 'TOC = {"pt": [TW404, TC403, TP404, TF404,', 1),
    ('"en": [TW404E, TP404E, TF404E,', '"en": [TW404E, TC403E, TP404E, TF404E,', 1),
    ('cv3 = dict(copy.deepcopy(c)); [cv3.pop(k, None) for k in ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403")]\n',
     'cv3 = dict(copy.deepcopy(c)); [cv3.pop(k, None) for k in ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403")]\n'
     'cv4 = dict(copy.deepcopy(c)); [cv4.pop(k, None) for k in ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404")]\n', 1),
    ('    _t3, _x3, _r23, _l3 = compilar(cv3, "dry_v404_var3_%s" % lang, lang, duas=False); fl3 = re.sub(r"\\s+", " ", _x3)\n',
     '    _t3, _x3, _r23, _l3 = compilar(cv3, "dry_v404_var3_%s" % lang, lang, duas=False); fl3 = re.sub(r"\\s+", " ", _x3)\n'
     '    _t4, _x4, _r24, _l4 = compilar(cv4, "dry_v404_var4_%s" % lang, lang, duas=False); fl4 = re.sub(r"\\s+", " ", _x4)\n', 1),
    ('"rc_v404_registros": _r23, "frase_guarda_v404_registros": ("NÃO selaram todos" in fl3) if lang == "pt" else ("did NOT all seal" in fl3)}',
     '"rc_v404_registros": _r23, "frase_guarda_v404_registros": ("NÃO selaram todos" in fl3) if lang == "pt" else ("did NOT all seal" in fl3),\n'
     '                             "rc_novo_v404": _r24, "frase_guarda_novo_v404": ("NÃO selaram todos" in fl4) if lang == "pt" else ("did NOT all seal" in fl4)}', 1),
    ('or v["rc_v404_registros"] != [0] or not v["frase_guarda_v404_registros"]]', 'or v["rc_v404_registros"] != [0] or not v["frase_guarda_v404_registros"] or v["rc_novo_v404"] != [0] or not v["frase_guarda_novo_v404"]]', 1),
    ('"caminho_v403": "Caminho, Verdade e Vida (v404, 27/10/2026)" in md, "ponte_v403_fica": "A ponte da escala dual, a queda sem geometria e a esperança condicional (v403, 26/10/2026)" in md,',
     '"jo8_v404": "Jo 8,32 e a projeção transversal da Meia-Nat (v404, 28/10/2026)" in md, "caminho_v403_fica": "Caminho, Verdade e Vida (v403, 27/10/2026)" in md, "ponte_v402_fica": "A ponte da escala dual, a queda sem geometria e a esperança condicional (v402, 26/10/2026)" in md,', 1),
    ('_kh = [s_ for s_ in um._V403_SPECS if s_["nome"] == "kh_n1_cobertura_v403"][0]; _h8 =', '_kh = [s_ for s_ in um._V404_SPECS if s_["nome"] == "kh_n1_cobertura_v404"][0]; _h8 =', 1),
    ('_regs_sim = ("caminho_v403", "vida_v403",', '_regs_sim = ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404", "caminho_v403", "vida_v403",', 1),
    ('"ponto_verdade_adendo": _ej.get("ponto_verdade_adendo"), "ponto_bandeiras": _ej.get("ponto_bandeiras"),', '"ponto_verdade_adendo": _ej.get("ponto_verdade_adendo"), "ponto_bandeiras": _ej.get("ponto_bandeiras"), "ponto_projecao": _ej.get("ponto_projecao"), "ponto_jo8v32": _ej.get("ponto_jo8v32"), "ponto_f2b": _ej.get("ponto_f2b"),', 1),
])
