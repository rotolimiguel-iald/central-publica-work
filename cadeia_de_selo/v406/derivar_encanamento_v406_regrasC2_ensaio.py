# -*- coding: utf-8 -*-
# regras (lote C2) de derivar_encanamento_v406.py: o ENSAIO A SECO. ORIGEM v405 FINAL (ensaio_a_seco_v405.py). Variaveis herdadas do lote C: _ORIG_ENS (o texto ORIGINAL do ensaio da v405, sem subida de versao), para_d4 (DL.X -> DL.D4.X), DL5, NOMES_SOBRESCRITOS.
# A base mecanica sobe da v405 FINAL; os blocos (6f), (6g), (6h) e (6i) -- que tratam dos registros da v401, da v402, da v403 e da v405 -- voltam do arquivo ORIGINAL da v405 (a semantica deles e' a da base: eles sao RECRIADOS e comparados com os da v405 selada; os nomes que a v406 sobrescreve em DL
# viram DL.D4.*); o bloco (6j) NOVO traz os OITO registros da v406 (cada elo recusa visivelmente), as falas, as decisoes D27-D33, as erratas E10-E13, os campos fechados e as leituras, a guarda das frases e a cobertura exata. Escrito pela ferramenta Write (as barras invertidas e os apostrofos nao passam pelo heredoc).

_DOC_ENS = '''"""ensaio_a_seco_v406.py -- ENSAIO A SECO da v406 (molde: ensaio_a_seco_v405.py FINAL, que rodou na cadeia da v405, com as licoes da v399 a v405), SEM a GPU do rito e SEM rodar o rito. Chama NO PONTO DE CHAMADA REAL todo veredito novo ou alterado.
uso: python -B -X utf8 ensaio_a_seco_v406.py <candidato.py> <rotulo>
A v406 e' uma versao de CONTEUDO (01/11/2026): OITO modulos novos de kernel, com os nomes do operador (TGLExt/PonteDaMassa, MassaTensaoPura, Identidade, ObservadorTerminal, LeiDoDiminuto, TonicaDoHamiltoniano, DiscoDeEuler, PontoZeroDoPsion), os OITO registros com FUNCAO (ponte_da_massa_v405, massa_tensao_pura_v405, identidade_v405, observador_terminal_v405,
lei_do_diminuto_v405, tonica_do_hamiltoniano_v405, disco_de_euler_v405, ponto_zero_do_psion_v405), os registros por spec cunhagens_v405, campos_fechados_e_leituras_v405, ga_reclassificacao_v405 (a classe nova do teste do Grande Atrator, AO LADO, com quatro medidas em runtime) e kh_n1_cobertura_v405; o gate NAO muda (as duas funcoes do gate ficam byte a byte; o ensaio o RECOMPUTA sobre os dados do core da v405 selada), a funcao do neutrino NAO e' reescrita e o numero da massa NAO muda.
A MOLDURA (errata da gerencia c1, 01/11/2026): os campos das estruturas fecharam; as leituras do operador passaram do campo para a definicao; a leitura fisica nao virou teorema; dadas as entradas, a FORMA e' teorema. O ensaio cobra isto: cada registro recusa quando uma frase proibida e' plantada no texto dele.
A base e' a v405 SELADA (core e selo em base_v405), o kernel e' o da v405 + as oito pedras (sandbox C:/t/k406c); os registros de v393 a v399, os da v401, os da v402, os da v403 E OS DA V405 (projecao_transversal_v404, jo8v32_v404, f2b_errata_v404, cunhagens_v404, kh_n1_cobertura_v404) sao RECRIADOS e comparados com os da v405 selada. Etapas:
(1) copia o candidato; materializa o kernel embutido e confere BYTE A BYTE contra o sandbox; (2) importa (o rito NAO roda); UM_VERSION v406; (3) o core da v405 SELADA + o kernel REAL: verify_tgl_kernel_formalization() de ponta a ponta com o lake simulado devolvendo os logs CRUS do sandbox;
(4) os registros vizinhos RECOMPUTADOS: iguais, ou a TROCA DITA (so' numeros: a escada e a cobertura crescem com as pedras); (5) o FLUXO PRINCIPAL v393 a v399, v401 a v406 (as instrucoes etiquetadas do main, na ordem do arquivo), as chaves NOVAS no core: as doze da v406; (5b) a ORDEM DE CHAMADA, estatica, com controle negativo;
(6) unidade: o Teste da Unica Palavra (v397), o sonico e a afinacao (v398), o selo pela propria tecnologia e a declaracao do operador (v399), a FALSIDADE DA INERCIA (v401, recriada), os registros da v402, da v403 e da v405 (recriados), os OITO da v406 (cada elo recusa), o GATE recomputado, os registros por spec, a cobertura, o sidecar;
(7) o selo (a instrucao `seal = {...}` do main + o resumo) e o indice; (8) artigo PT/EN, pdflatex x2, as secoes v406 (antes da v405) e o QUADRO NO TOPO (v397, intocado); (9) .md e manifesto; (10) o conferidor de citacoes; (11) simular_arvore_do_nos; (12) exame_pontos;
(13) [LICAO DA v400, mantida] as guardas ESTATICAS do esboco R3.5 da Bancada (ALPHA_LINHA_UNICA e as demais que nao dependem do selo) rodadas SOBRE O CANDIDATO, chamando a funcao do proprio esboco pinado, ANTES de instalar."""
'''

# --- o bloco (6j) NOVO: os OITO registros da v406 ---
_B6J = r'''# (6j) [v405] os OITO registros com FUNCAO da v406: tudo certo, os numeros RECALCULADOS aqui por outro caminho e cada elo recusa visivelmente (controles negativos); a guarda das frases; as falas de 30/10 a 01/11, as decisoes D27-D33, as erratas E10-E13, os campos fechados e as leituras, a cobertura exata (specs) e o neutrino NAO reescrito
import types as _types5
import guarda_frases_v406 as _GF5
_REG406 = tuple((s_["key"], DL.REGISTRO_DE_PEDRA[s_["key"]]) for s_ in DL.STONES)
_TAMPER406 = {"ponte": "cos", "tensao": "sqrt", "identidade": "cos", "diminuto": "exp", "tonica": "sqrt", "disco": "exp", "psion": "sqrt"}   # a funcao do math adulterada, registro a registro (o observador e' aritmetica de grafo: o numero adulterado dele e' o omega_I do core)
R406 = {}
_bf5 = um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e)
_nm_antes5 = json.dumps(cs()["neutrino_mass"], sort_keys=True, default=str)
for k406_, n406_ in _REG406:
    fn_ = getattr(um, n406_); C_ = um._V405_CONTRACTS[k406_]; T_ = um._V405_TEXTS[k406_]
    cc5_ = cs(); r_ = fn_(cc5_); R406[k406_] = r_
    U["v406_%s_tudo_certo" % k406_] = bool(r_["all_verified"] is True and r_["verdict"] == T_["veredito_ok"] and r_["runtime_executed"] is True and r_["does_not_gate_core"] is True and all(ck_["ok"] for ck_ in r_["mechanics"]["checks"]) and r_["mechanics"]["n_checks"] == DL.N_CHECKS[k406_] == len(r_["mechanics"]["checks"])
                                           and r_["exact_ladder"] is True and r_["embedded_source_ok"] is True and r_["unconditional"]["in_kernel"] is True and r_["key_theorem"]["in_kernel"] is True and all(r_["formal_theorems"].values()) and all(r_["support_theorems"].values())
                                           and all(r_["inscriptions"].values()) and r_["context"]["ok"] is True and r_["beta_ok"] is True and r_["nome_do_operador"] == DL.STONE_BY_KEY[k406_]["nome_do_operador"])
    U["v406_%s_veredito_e_textos_sem_palavra_proibida" % k406_] = bool(not guarda_txt(r_) and not _GUARDA98.search(r_["verdict"]) and not um._v392_guarda_texto(json.dumps(r_["mechanics"]["checks"], ensure_ascii=False)) and not r_["guarda_p18_violacoes"] and not um._v405_guarda_frases(r_["verdict"]) and not um._v405_guarda_frases(json.dumps(r_["mechanics"]["checks"], ensure_ascii=False)))
    ok_ = True
    for th_, fl_ in C_["theorems"].items():   # bandeira falsa de CADA declaracao do contrato (a estrela e a composicao entre elas)
        c_ = cs(); c_["kernel_formalization"][fl_] = False; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and rr_["formal_theorems"][th_] is False
    U["v406_%s_bandeira_falsa_de_cada_declaracao_do_contrato_recusa" % k406_] = bool(ok_ and len(C_["theorems"]) == len(DL.STONE_BY_KEY[k406_]["contract"]) and C_["key_theorem"]["theorem"] in C_["theorems"] and C_["unconditional"]["theorem"] in C_["theorems"])
    ok_ = True
    for th_ in list(C_["theorems"]) + list(C_["support"]):   # axioma fora do trio em CADA termo lido
        c_ = cs(); c_["kernel_formalization"]["axiom_report"][th_] = ["propext", "sorryAx"]; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U["v406_%s_axioma_fora_do_trio_em_cada_termo_lido_recusa" % k406_] = bool(ok_)
    ok_ = True
    for th_ in [C_["unconditional"]["theorem"], C_["key_theorem"]["theorem"]] + list(C_["support"]):   # proveniencia errada
        c_ = cs(); c_["kernel_formalization"]["declaration_sources_v394"][th_] = "TGLExt/Outro.lean"; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U["v406_%s_proveniencia_errada_recusa" % k406_] = bool(ok_)
    c_ = cs(); c_["kernel_formalization"]["formal_files_sha256"][C_["stone"]["path"]] = "0" * 64; rr_ = fn_(c_)
    ef_ = dict(um._EMBEDDED_KERNEL_FILES); um._EMBEDDED_KERNEL_FILES[C_["stone"]["path"]] += " "
    try:
        rr2_ = fn_(cs())
    finally:
        um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
    U["v406_%s_fonte_da_pedra_adulterada_recusa" % k406_] = bool(rr_["all_verified"] is False and rr_["embedded_source_ok"] is False and rr2_["all_verified"] is False and rr2_["embedded_source_ok"] is False)
    c_ = cs(); c_["external_ladder"]["n_theorems_clean"] = int(c_["external_ladder"]["n_theorems_clean"]) - 1; rr_ = fn_(c_)
    c2_ = cs(); c2_["kernel_formalization"]["all_verified"] = False; rr2_ = fn_(c2_)
    U["v406_%s_escada_errada_ou_kernel_nao_verificado_recusa" % k406_] = bool(rr_["all_verified"] is False and rr_["exact_ladder"] is False and rr2_["all_verified"] is False)
    ok_ = True
    for ch_ in C_["verbatins"]:
        _ant = um._V405_VERBATINS2[ch_]["text"]; um._V405_VERBATINS2[ch_]["text"] += " "   # restaurado NO LUGAR (o objeto e' compartilhado com _V392_VERBATINS2)
        try:
            rr_ = fn_(cs()); ok_ = ok_ and rr_["all_verified"] is False and rr_["inscriptions"][ch_] is False
        finally:
            um._V405_VERBATINS2[ch_]["text"] = _ant
    U["v406_%s_inscricao_adulterada_recusa" % k406_] = bool(ok_ and len(C_["verbatins"]) >= 1)
    ef_ = dict(um._EMBEDDED_KERNEL_FILES); _cp = C_["context"]["path"]; um._EMBEDDED_KERNEL_FILES[_cp] = um._EMBEDDED_KERNEL_FILES[_cp].replace(C_["context"]["needles"][0], "xx")
    try:
        rr_ = fn_(cs())
    finally:
        um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
    U["v406_%s_texto_contexto_retirado_do_kernel_recusa" % k406_] = bool(r_["context"]["ok"] is True and rr_["all_verified"] is False and rr_["context"]["text_in_embedded_kernel"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"])
    c_ = cs(); c_["beta"] = c_["beta"] * 1.001; _rb = fn_(c_)
    _a0 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a0 * 1.001
    try:
        _ra = fn_(cs())
    finally:
        um.SEALED_CODATA_ALPHA = _a0
    U["v406_%s_beta_adulterado_recusa" % k406_] = bool(_rb["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _rb["verdict"] and _ra["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _ra["verdict"])
    if k406_ == "observador":
        c_ = cs(); c_["omega_I"] = 2.0; _rn = fn_(c_)
    else:
        _m0 = um._m405; tamper_ = _TAMPER406[k406_]
        um._m405 = _types5.SimpleNamespace(**{k_: getattr(_math, k_) for k_ in dir(_math) if not k_.startswith("__")}); setattr(um._m405, tamper_, (lambda f_: (lambda *x_: f_(*x_) * 1.001))(getattr(_math, tamper_)))
        try:
            _rn = fn_(cs())
        finally:
            um._m405 = _m0
    U["v406_%s_numero_adulterado_recusa" % k406_] = bool(_rn["all_verified"] is False and "MECHANICS_CHECK_FAILED" in _rn["verdict"] and any(not ck_["ok"] for ck_ in _rn["mechanics"]["checks"]))
_pv5, _mv5, _iv5, _ov5, _dv5, _tv5, _ev5, _zv5 = (R406[k_]["values"] for k_ in ("ponte", "tensao", "identidade", "observador", "diminuto", "tonica", "disco", "psion"))
_mnu5 = core0["neutrino_mass"]["m_nu_meV"]; _r25 = _math.sqrt(2.0); _alfa5 = um.SEALED_CODATA_ALPHA
U["v406_o_numero_da_massa_nao_muda_e_os_numeros_foram_recalculados_aqui"] = bool(abs(_pv5["beta"] - _bf5) <= 1e-15 and abs(_pv5["m_derivada_meV"] / _mnu5 - 1.0) <= 1e-12 and abs(_pv5["m_derivada_meV"] - _bf5 * _math.cos(_math.pi / 4.0) * 1000.0) <= 1e-9 and abs(_pv5["m_derivada_meV"] / _pv5["m_proporcional_meV"] - _r25) <= 1e-9
                                                                                 and abs(_mv5["retida_eV"] - _bf5) <= 1e-15 and abs(_mv5["transmitida_eV"] - (1.0 - _bf5)) <= 1e-15 and abs(_mv5["massa_meV"] / _mnu5 - 1.0) <= 1e-12
                                                                                 and abs(_dv5["sqrt_e"] - _math.sqrt(_math.e)) <= 1e-15 and abs(_dv5["meio_tom"] - _math.exp(-0.5)) <= 1e-15 and abs(_dv5["E0_eV"] - 1.0) <= 1e-12 and abs(_dv5["tonica_eV"] - _math.sqrt(_math.e)) <= 1e-12 and abs(_dv5["alpha_lida_do_acoplamento"] - _alfa5) <= 1e-15 and abs(_dv5["massa_formula_meV"] / _mnu5 - 1.0) <= 1e-12
                                                                                 and abs(_tv5["razao_m_sobre_E0"] - _bf5 * _r25 / 2.0) <= 1e-15 and abs(_tv5["E0_da_lei_derivada_eV"] - 1.0) <= 1e-12
                                                                                 and abs(_zv5["hbar_omega_meV"] - _r25 * _bf5 * 1000.0) <= 1e-9 and abs(_zv5["meia_hbar_omega_meV"] / _mnu5 - 1.0) <= 1e-12 and abs(_zv5["R_natural"] - _bf5) <= 1e-15
                                                                                 and abs(_ev5["E_star_modelo"] - 3.0 ** (1.0 / 3.0)) <= 1e-12 and abs(_ev5["U_modelo"] - _math.exp(-0.5) * 3.0 ** (1.0 / 3.0)) <= 1e-12 and abs(_ev5["disco_modelo"]["c"] - 0.5 * _bf5 * 0.7 * 3.0) <= 1e-12
                                                                                 and _iv5["eu_sou"] == {"2": 1.0, "3": 1.0, "4": 1.0} and _iv5["n_nomes"] == 12 and _iv5["vazio_peso"] == 0.0 and all(p_[1] == 0.5 for p_ in _iv5["faces_peso"]) and _ov5["terminal"] == ["gravidade"] and _ov5["inicial"] == ["luz"] and _ov5["omega_I"] == 1.0)
_c5p = cs(); _antes5p = json.dumps(_c5p["neutrino_mass"], sort_keys=True, default=str); _r5p = um.ponte_da_massa_v405(_c5p); _e10 = _r5p["neutrino_angle_errata"]
U["v406_a_errata_do_angulo_fica_ao_lado_o_texto_antigo_intacto_e_o_canal_do_neutrino_nao_se_move"] = bool(json.dumps(_c5p["neutrino_mass"], sort_keys=True, default=str) == _antes5p == _nm_antes5 and _c5p["neutrino_mass"]["angle_status"].startswith(DL.ANGLE_STATUS_ANTIGO_PREFIXO) and _e10["dizia_prefixo"] == DL.ANGLE_STATUS_ANTIGO_PREFIXO and _e10["agora"] == DL.ERRATA_E10 and _e10["assinatura"].startswith("gerencia c1, em nome proprio") and _c5p["neutrino_mass"]["verdict"] == core0["neutrino_mass"]["verdict"] and _c5p["neutrino_mass"]["frozen_hash"] == core0["neutrino_mass"]["frozen_hash"])
U["v406_a_ponte_o_u_e_posto_as_leituras_entram_como_definicao_e_o_nome_e_do_operador"] = bool(R406["ponte"]["u"]["status"] == "POSTO" and R406["ponte"]["u"]["derived_here"] is False and R406["ponte"]["reading_matter"]["status"] == "ONTO" and R406["ponte"]["reading_matter"]["is_a_kernel_term"] is False and [l_["n"] for l_ in R406["ponte"]["leituras_que_entram"]] == [1, 2] and all(l_["entra_como"] == "DEFINICAO, nao teorema" for l_ in R406["ponte"]["leituras_que_entram"])
                                                                                             and R406["ponte"]["name_status"]["quem"] == "operador" and R406["ponte"]["name_status"]["fala"] == DL.FRASE_NOMEACAO and DL.ERRATA_E13 in R406["ponte"]["limites"] and any("a massa do neutrino SEJA" in x_ for x_ in R406["ponte"]["nao_diz"]))
U["v406_a_tonica_o_no_go_nao_cai_alfa_e_medida_e_a_tonica_e_definicao"] = bool("NAO cai" in R406["tonica"]["no_go_e_tonica"]["no_go"] and "identidade algebrica" in R406["tonica"]["no_go_e_tonica"]["tonica"] and R406["tonica"]["alfa"]["status"].startswith("MEDIDA") and [l_["n"] for l_ in R406["tonica"]["leituras_que_entram"]] == [3] and [l_["n"] for l_ in R406["diminuto"]["leituras_que_entram"]] == [3, 5, 11, 12] and any("alfa tenha sido derivado" in x_ for x_ in R406["tonica"]["nao_diz"]) and any("que o no-go tenha caido" in x_ for x_ in R406["tonica"]["nao_diz"]))
U["v406_o_psion_a_curvatura_e_definicao_e_a_coincidencia_e_aritmetica"] = bool([l_["n"] for l_ in R406["psion"]["leituras_que_entram"]] == [4, 6, 7, 13, 14, 15] and "aritmetica" in R406["psion"]["duas_leituras_do_sen45"]["coincidem_por"] and any("pagamentoComoCurvatura" in x_ for x_ in R406["psion"]["limites"]))
U["v406_a_identidade_e_um_fato_sobre_projecoes_tipado_como_modelo"] = bool(any("tipada como modelo" in x_ for x_ in R406["identidade"]["limites"]) and "ONTO" in R406["identidade"]["lei"]["status"] and "ONTO" in R406["identidade"]["ensaio"]["status"] and "um fato sobre projecoes" in R406["identidade"]["estatuto"] and any("SEJA a identidade" in x_ for x_ in R406["identidade"]["nao_diz"]))
U["v406_o_verbatim_e_a_traducao_o_ensaio_e_o_do_operador_e_a_traducao_nao_e_citacao"] = bool(hashlib.sha256(um._V405_IDENTIDADE_TXT.encode("utf-8")).hexdigest() == um._V405_FONTES["ensaio_a_identidade_r2_01nov"]["sha256"] and hashlib.sha256(um._V405_IDENTIDADE_EN_TXT.encode("utf-8")).hexdigest() == um._V405_FONTES["ensaio_a_identidade_en_traducao_da_gerencia_01nov"]["sha256"] and um._V405_IDENTIDADE_TXT.rstrip().endswith("[EU SOU] = [O QUE SOU] se, e somente se, {[FORMA = CONTEÚDO] = [REFLEXÃO VERDADEIRA DO NOME / PROJEÇÃO FIEL]}.") and "NAO e' citacao" in um._V405_FONTES["ensaio_a_identidade_en_traducao_da_gerencia_01nov"]["papel"] and len(um._v405_ensaio_tex(um._V405_IDENTIDADE_TXT)) == len(um._v405_ensaio_tex(um._V405_IDENTIDADE_EN_TXT)))
# --- a GUARDA DAS FRASES no rito (ordem da gerencia c1, 01/11/2026): cada frase proibida plantada no texto de CADA registro recusa; a frase certa passa; o controle negativo da cadeia passa
_g5 = _GF5.controle_negativo(); ok_ = bool(_g5["ok"])
for k406_, n406_ in _REG406:
    fn_ = getattr(um, n406_); _dz = um._V405_TEXTS[k406_]["diz"]; _d0 = list(_dz)
    for f_ in ("tudo é teorema", "tudo derivado", "nenhuma hipótese resta", "everything is a theorem", "everything is derived", "no hypothesis remains"):
        _dz[:] = _d0 + ["a cadeia: " + f_]
        try:
            rr_ = fn_(cs())
        finally:
            _dz[:] = _d0
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and bool(rr_["guarda_p18_violacoes"])
    _dz[:] = _d0 + [DL.FRASE_DA_MOLDURA_PT]
    try:
        rr_ = fn_(cs())
    finally:
        _dz[:] = _d0
    ok_ = ok_ and rr_["all_verified"] is True
    ok_ = ok_ and fn_(cs())["all_verified"] is True
U["v406_guarda_das_frases_cada_frase_proibida_recusa_em_cada_registro_e_a_frase_certa_passa"] = bool(ok_)
# --- as falas de 30/10 a 01/11, as decisoes D27-D33, as erratas E10-E13 (registro cunhagens_v405), os campos fechados e as leituras e a cobertura exata (kh_n1_cobertura_v405)
_cn5 = c.get("cunhagens_v405") or {}; _xn5 = _cn5.get("extras") or {}
_sp5s = [s_ for s_ in um._V405_SPECS if s_["nome"] == "cunhagens_v405"][0]
U["cunhagens_v406_falas_decisoes_erratas_e_leituras"] = bool(_cn5.get("all_verified") is True and len(_cn5.get("verbatim") or {}) == len(DL.VERBATIM_ORIGEM_V406) and all(v_["embedded_ok"] for v_ in (_cn5.get("verbatim") or {}).values())
                                                             and len(_cn5.get("erratas") or []) == len(_sp5s["erratas"]) and all(e_["assinatura"].startswith("gerencia c1, em nome proprio") for e_ in (_cn5.get("erratas") or []))
                                                             and len(_cn5.get("leituras_do_operador") or []) == len(_sp5s["leituras_do_operador"]) and set(_xn5.get("decisoes_da_gerencia") or {}) >= {"D27", "D28", "D29", "D30", "D31", "D32", "D33"}
                                                             and _xn5.get("estrelas") == {s_["key"]: s_["key_theorem"] for s_ in DL.STONES} and _xn5.get("teoremas") == {s_["key"]: s_["theorem"] for s_ in DL.STONES}
                                                             and len(_xn5.get("erratas_E10_a_E13") or []) == 4 and (_xn5.get("autor_de_cada_inscricao") or {}) and all(a_ == "operador" for a_ in (_xn5.get("autor_de_cada_inscricao") or {}).values()))
_cf5 = c.get("campos_fechados_e_leituras_v405") or {}; _xf5 = _cf5.get("extras") or {}
_sp5c = [s_ for s_ in um._V405_SPECS if s_["nome"] == "campos_fechados_e_leituras_v405"][0]
U["campos_fechados_o_que_fechou_e_o_que_entra_cada_um_com_a_definicao_lean"] = bool(_cf5.get("all_verified") is True and set(_xf5.get("o_que_fechou_campos") or {}) == set(DL.CAMPOS_FECHADOS) and all(v_.get("termos") for v_ in (_xf5.get("o_que_fechou_campos") or {}).values()) and [d_["estatuto"] for d_ in (_xf5.get("o_que_entra") or {}).get("dois_postos", [])] == ["POSTO", "MEDIDA"]
                                                                                    and [l_["n"] for l_ in (_xf5.get("o_que_entra") or {}).get("leituras_da_cadeia_da_massa", [])] == [l_["n"] for l_ in DL.LEITURAS_DEFINICOES] and (_xf5.get("o_que_entra") or {}).get("lista_de_leituras_fechada") is False and all((l_["definicao_lean"] is None or l_["definicao_lean"] in _sp5c["kernel_decls"]) and l_["entra_como"].endswith(", nao teorema") for l_ in (_xf5.get("o_que_entra") or {}).get("leituras_da_cadeia_da_massa", []))
                                                                                    and _xf5.get("a_frase_da_moldura") == DL.FRASE_DA_MOLDURA_PT and len(_xf5.get("a_forma_real") or []) == 4 and len(_xf5.get("teoremas_rebatizados_antes_do_selo") or {}) == 4 and DL.ERRATA_E13 in (_cf5.get("limites") or []))
U["campos_fechados_o_registro_antigo_nao_existe_e_o_texto_nao_afirma_demais"] = bool("nomes_e_hipoteses_descarregadas_v406" not in c and "nomes_e_hipoteses_descarregadas_v406" not in um._V405_NOMES_REGISTROS and not um._v405_guarda_frases(json.dumps({k_: _cf5.get(k_) for k_ in ("limites", "diz", "nao_diz", "erratas")}, ensure_ascii=False)) and not um._v405_guarda_frases(str(_cf5.get("verdict"))))
# --- a reclassificacao do Grande Atrator (registro por especificacao, AO LADO): selou, as medidas recalculadas aqui por outro caminho, cada elo recusa e o selado fica identico
_gaS = [s_ for s_ in um._V405_SPECS if s_["nome"] == DL.GA_REGISTRO][0]; _ga5 = c.get(DL.GA_REGISTRO) or {}; _gv5 = _ga5.get("values") or {}; _gx5 = _ga5.get("extras") or {}
_GA_R = lambda c_: um._v405_ga_registro(um._v392_registro(_gaS, c_), c_, _gaS)
U["ga_reclassificacao_selou_a_classe_nova_ao_lado_e_o_estatuto_e_dito"] = bool(_ga5.get("all_verified") is True and _ga5.get("does_not_gate_core") is True and _ga5.get("runtime_executed") is True and (_ga5.get("mechanics") or {}).get("passed") is True and (_ga5.get("mechanics") or {}).get("n_checks") == 6 and _ga5.get("errata_do_parecer_ok") is True and not _ga5.get("guarda_frases_violacoes")
                                                                               and _gx5.get("classe_antes") == DL.GA_CLASSE_ANTES and _gx5.get("classe_agora") == DL.GA_CLASSE_AGORA and _gx5.get("e_evidencia") is False and _gx5.get("discrimina_da_RG") is False and _gx5.get("veto_da_janela") == "mantido" and _gx5.get("errata_ao_lado_do_parecer_da_entrega_005") == DL.errata_entrega_005()
                                                                               and len((_gx5.get("partitura") or {}).get("escolhas_antes_de_qualquer_teste") or []) == 4 and len(_gx5.get("quatro_medidas") or []) == 4 and not _GF5.violacoes(str(_ga5.get("verdict"))))
_por5 = um.C_LIGHT ** 2 / (4.0 * _math.pi * um.G_NEWTON) * um.MPC_M / um.MSUN; _MA5 = R0["verdict"]["masses_Msun"]["A_literature"]; _MB5 = R0["verdict"]["masses_Msun"]["B_cf4_positions"]
U["ga_as_medidas_recalculadas_aqui_com_o_beta_de_runtime_e_as_massas_do_verdict"] = bool(abs(_gv5.get("M_sobre_R_Msun_por_Mpc", 0.0) / (2.0 * _bf5 ** 2 * _por5) - 1.0) <= 1e-12 and _gv5.get("dM_du") == 0.0 and max(_gv5.get("residuos_M_igual_M") or [1.0]) <= 1e-14 and all(abs(x_ * _bf5 / (2.0 * _math.pi) - 1.0) <= 1e-12 for x_ in (_gv5.get("R_B_sobre_r_s") or [0.0]))
                                                                                         and abs(_gv5.get("piso_de_definicao", 0.0) - (_MA5 / _MB5 - 1.0)) <= 1e-12 and abs(_gv5.get("sigma_relativo_resposta_beta", 0.0) - _bf5 / 5.0) <= 1e-15 and abs(_gv5.get("sigma_relativo_forma_ancora", 0.0) - (5.4e16 - _MA5) / 5.0 / 5.4e16) <= 1e-12 and _gv5.get("M_A_Msun") == _MA5 and _gv5.get("M_B_Msun") == _MB5)
_negs5 = {}
_c5a = cs(); _c5a["beta"] = _c5a["beta"] * 1.001; _negs5["beta"] = _GA_R(_c5a)
_c5b = cs(); _c5b["mode_B"]["M_TGL_Msun"] = _c5b["mode_B"]["M_TGL_Msun"] * 1.001; _negs5["piso"] = _GA_R(_c5b)
_c5c = cs(); [x_.__setitem__("rule", DL.GA_CLASSE_AGORA) for x_ in _c5c["joint_coincidence_result_v3"]["inventory"] if x_.get("id") == "ga_mass_window"]; _negs5["linha_selada"] = _GA_R(_c5c)
_c5d = cs(); _c5d["ga_mass_audit"]["verdict"] = "OUTRO"; _negs5["auditoria"] = _GA_R(_c5d)
_gaE = _gaS["extras"]["errata_ao_lado_do_parecer_da_entrega_005"]; _gaS["extras"]["errata_ao_lado_do_parecer_da_entrega_005"] = _gaE + " "
try:
    _negs5["errata"] = _GA_R(cs())
finally:
    _gaS["extras"]["errata_ao_lado_do_parecer_da_entrega_005"] = _gaE
_gaD = list(_gaS["diz"]); _gaS["diz"][:] = _gaD + ["a cadeia: tudo derivado"]
try:
    _negs5["frase"] = _GA_R(cs())
finally:
    _gaS["diz"][:] = _gaD
_m05 = um._m405; um._m405 = _types5.SimpleNamespace(**{k_: getattr(_math, k_) for k_ in dir(_math) if not k_.startswith("__")}); um._m405.sqrt = (lambda f_: (lambda *x_: f_(*x_) * 1.001))(_math.sqrt)
try:
    _negs5["numero"] = _GA_R(cs())
finally:
    um._m405 = _m05
U["ga_cada_elo_recusa_beta_piso_linha_selada_auditoria_errata_frase_e_numero"] = bool(all(r_["all_verified"] is False and "NOT_SEALED_THIS_RUN" in r_["verdict"] for r_ in _negs5.values()) and len(_negs5) == 7 and _GA_R(cs())["all_verified"] is True)
_lgm5 = [x_ for x_ in c["joint_coincidence_result_v3"]["inventory"] if x_.get("id") == "ga_mass_window"]
U["ga_o_selado_fica_identico_a_constante_a_linha_e_a_auditoria"] = bool(um.GA_WINDOW_STATUS == R0["ga_window_status"] and len(_lgm5) == 1 and _lgm5[0]["rule"] == DL.GA_CLASSE_ANTES and _lgm5[0]["admissible"] is False and c["ga_mass_audit"]["verdict"] == core0["ga_mass_audit"]["verdict"])
rep["ga_registro"] = {"verdict": _ga5.get("verdict"), "all_verified": _ga5.get("all_verified"), "values": _gv5, "n_checks": (_ga5.get("mechanics") or {}).get("n_checks"), "ctl_negativos": {k_: r_["all_verified"] for k_, r_ in _negs5.items()}}
# --- o gap (registro por especificacao, AO LADO): selou, os numeros recalculados aqui por outro caminho, e cada elo recusa
_gpS = [s_ for s_ in um._V405_SPECS if s_["nome"] == DL.GAP_REGISTRO][0]; _gp5 = c.get(DL.GAP_REGISTRO) or {}; _gpv = _gp5.get("values") or {}
_GP_R = lambda c_: um._v405_gap_registro(um._v392_registro(_gpS, c_), c_, _gpS)
U["gap_selou_com_as_medidas_em_runtime_e_a_guarda"] = bool(_gp5.get("all_verified") is True and _gp5.get("does_not_gate_core") is True and _gp5.get("runtime_executed") is True and (_gp5.get("mechanics") or {}).get("passed") is True and (_gp5.get("mechanics") or {}).get("n_checks") == DL.GAP_N_CHECKS and not _gp5.get("guarda_frases_violacoes") and not _GF5.violacoes(str(_gp5.get("verdict"))))
U["gap_os_numeros_recalculados_aqui_com_o_beta_de_runtime"] = bool(abs(_gpv.get("Delta_eV", 0.0) / _bf5 - 1.0) <= 1e-14 and _gpv.get("gap_espectral_eV") == 1.0 and abs(_gpv.get("gap_sobre_Delta", 0.0) * _bf5 - 1.0) <= 1e-13 and abs(_gpv.get("Q", 0.0) * _bf5 / _math.sqrt(2.0) - 1.0) <= 1e-13 and abs(_gpv.get("Gamma_B_eV", 0.0) / _bf5 ** 2 - 1.0) <= 1e-13 and 56.0 < _gpv.get("log10_E_fluxo_eV", 0.0) < 58.0 and _gpv.get("tau_sobre_t_planck", 0.0) > 1.0e25)
_negsG = {}
_cGa = cs(); _cGa["beta"] = _cGa["beta"] * 1.001; _negsG["beta"] = _GP_R(_cGa)
_cGb = cs(); _cGb["neutrino_mass"]["m_nu_meV"] = _cGb["neutrino_mass"]["m_nu_meV"] * 1.001; _negsG["massa"] = _GP_R(_cGb)
_gpD = list(_gpS["diz"]); _gpS["diz"][:] = _gpD + ["o tau* foi derivado aqui"]
try:
    _negsG["frase_tau"] = _GP_R(cs())
finally:
    _gpS["diz"][:] = _gpD
_gpD = list(_gpS["diz"]); _gpS["diz"][:] = _gpD + ["kappa = F(alfa, beta, theta_M)"]
try:
    _negsG["frase_kappa"] = _GP_R(cs())
finally:
    _gpS["diz"][:] = _gpD
_gpD = list(_gpS["diz"]); _gpS["diz"][:] = _gpD + ["Delta e' o gap do lock"]
try:
    _negsG["frase_delta_gap"] = _GP_R(cs())
finally:
    _gpS["diz"][:] = _gpD
U["gap_cada_elo_recusa_beta_massa_e_as_frases"] = bool(all(r_["all_verified"] is False for r_ in _negsG.values()) and len(_negsG) == 5 and _GP_R(cs())["all_verified"] is True)
rep["gap_registro"] = {"verdict": _gp5.get("verdict"), "all_verified": _gp5.get("all_verified"), "values": _gpv, "n_checks": (_gp5.get("mechanics") or {}).get("n_checks"), "ctl_negativos": {k_: r_["all_verified"] for k_, r_ in _negsG.items()}}
_kh5 = c.get("kh_n1_cobertura_v405") or {}
_kh4s5 = [s_ for s_ in um._V404_SPECS if s_["nome"] == "kh_n1_cobertura_v404"][0]; _kh5s = [s_ for s_ in um._V405_SPECS if s_["nome"] == "kh_n1_cobertura_v405"][0]
U["kh_n1_cobertura_v405_virou_piso_e_a_v406_cobra_a_igualdade_exata"] = bool(_kh5.get("all_verified") is True and (c.get("kh_n1_cobertura_v404") or {}).get("all_verified") is True and {ck_["id"]: ck_["op"] for ck_ in _kh4s5["checks"] if ck_["id"] in _op_piso} == _op_piso and len(_kh4s5["erratas"]) >= 1
                                                                             and {ck_["id"]: ck_["op"] for ck_ in _kh5s["checks"] if ck_["id"] in _op_piso} == {"h2": "igual", "h3": "igual", "h6": "tamanho_igual", "h8": "igual"})
U["contratos_v405_de_pedra_pinam_a_escada_da_v406"] = bool(len(um._V404_CONTRACTS) == 3 and [c4_["expected_ladder"] for c4_ in um._V404_CONTRACTS.values()] == [ESP, ESP, None] and all(c5_["expected_ladder"] == ESP for c5_ in um._V405_CONTRACTS.values()) and len(um._V405_CONTRACTS) == 8)
rep["v406_registros"] = {k_: {"verdict": r_["verdict"], "all_verified": r_["all_verified"], "n_checks": r_["mechanics"]["n_checks"], "values": r_["values"], "unconditional": r_.get("unconditional"), "key_theorem": r_.get("key_theorem"), "context": r_.get("context")} for k_, r_ in R406.items()}
'''

# --- os blocos (6f) a (6i) recriados + (6j) novo, no lugar do trecho bumpado [(6f), (8)) ---
_i6f = _ORIG_ENS.index("# (6f) [v401, recriado na v402, na v403 e na v405 e comparado com o selado]"); _i6i = _ORIG_ENS.index("# (6i) [v404] os TRES registros com FUNCAO da v405"); _iv = _ORIG_ENS.index('rep["v405_registros"] = ', _i6i)
_iu = _ORIG_ENS.index('rep["unidade"] = U;', _iv); _i8 = _ORIG_ENS.index("# (8) o artigo")
_A6 = para_d4(_ORIG_ENS[_i6f:_i6i]).replace("# (6f) [v401, recriado na v402, na v403 e na v405 e comparado com o selado]", "# (6f) [v401, recriado na v402, na v403, na v405 e na v406 e comparado com o selado]")
_I6 = para_d4(_ORIG_ENS[_i6i:_iv]).replace("# (6i) [v404] os TRES registros com FUNCAO da v405", "# (6i) [v405, recriados na v406 e comparados com os selados] os TRES registros com FUNCAO da v405")
_RV6 = para_d4(_ORIG_ENS[_iv:_iu])
_TL6 = _ORIG_ENS[_iu:_i8]
_ant_kh = 'U["kh_n1_cobertura_v403_virou_piso_e_a_v405_cobra_a_igualdade_exata"] = bool('
_ig_kh = 'if ck_["id"] in _op_piso} == {"h2": "igual", "h3": "igual", "h6": "tamanho_igual", "h8": "igual"})'
assert _I6.count(_ant_kh) == 1 and _I6.count(_ig_kh) == 1
_I6 = _I6.replace(_ant_kh, 'U["kh_n1_cobertura_v403_e_a_da_v405_viraram_piso"] = bool(')
_I6 = _I6.replace(_ig_kh, 'if ck_["id"] in _op_piso} == _op_piso and len([s_ for s_ in um._V404_SPECS if s_["nome"] == "kh_n1_cobertura_v404"][0]["erratas"]) >= 1)')
_arq_vb = 'DL.verbatins405(os.path.join(HERE, "insumos", "cunhagens"))[DL.JO8_IDX]'
assert _I6.count(_arq_vb) == 1
_I6 = _I6.replace(_arq_vb, 'DL.D4.verbatins405(os.path.join(DL.V405, "insumos", "cunhagens"))[DL.D4.JO8_IDX]')
_REGIAO_6F_8 = _A6 + _I6 + _RV6 + _B6J + _TL6

_ANT_DEVE_PT = '"pt": [TW406, "A projeção transversal.", "Jo 8,32.", "A errata de F2b.", "As cunhagens de 28/10.", "Erratas ao lado (v406).", "Origem.", TC405, "O Caminho.", "A Vida.", "A Verdade, como adendo.", "As bandeiras do gate.", "Erratas ao lado (v405).", TP406,'
_NOV_DEVE_PT = ('"pt": [TW406, "O que entra.", "A moldura: o que fechou e o que entra.", "A Ponte da Massa.", "Massa = tensão pura.", "A lei do diminuto.", "A Tônica do Hamiltoniano.", "O Ponto Zero do Psíon.", "O Disco de Euler.", "Observador = terminal.", "A pedra Identidade.", "O Grande Atrator.", "Erratas ao lado (v406).", "Limites.", "O fecho.", "Origem.", '
                'TI406, "Moldura da seção.", "Eu sou o que sou?", "se, e somente se, {[FORMA = CONTEÚDO] = [REFLEXÃO VERDADEIRA DO NOME / PROJEÇÃO FIEL]}.", TJ405, "A projeção transversal.", "Jo 8,32.", "A errata de F2b.", "As cunhagens de 28/10.", "Erratas ao lado (v405).", TC405, "O Caminho.", "A Vida.", "A Verdade, como adendo.", "As bandeiras do gate.", "Erratas ao lado (v403).", TP406,')
_ANT_DEVE_EN = '"en": [TW406E, "The transverse projection.", "John 8:32.", "The F2b erratum.", "The sayings of 28/10.", "Errata beside (v406).", "Origin.", TC405E, "The Way.", "The Life.", "The Truth, as an addendum.", "The gate flags.", "Errata beside (v405).", TP406E,'
_NOV_DEVE_EN = ('"en": [TW406E, "What enters.", "The frame: what closed and what enters.", "The Bridge of the Mass.", "Mass = pure tension.", "The law of the diminished.", "The Tonic of the Hamiltonian.", "The Zero Point of the Psion.", "Euler\'s Disk.", "Observer = terminal.", "The stone Identity.", "The Great Attractor.", "Errata alongside (v406).", "Limits.", "The closing.", "Origin.", '
                'TI406E, "Frame of the section.", "Am I what I am?", "if, and only if, {[FORM = CONTENT] = [TRUE REFLECTION OF THE NAME / FAITHFUL PROJECTION]}.", TJ405E, "The transverse projection.", "John 8:32.", "The F2b erratum.", "The sayings of 28/10.", "Errata beside (v405).", TC405E, "The Way.", "The Life.", "The Truth, as an addendum.", "The gate flags.", "Errata beside (v403).", TP406E,')

# --- as regras do ensaio ---
entrada("ensaio_a_seco_v405.py", autoral=True, regras=[
    entre('"""ensaio_a_seco_v406.py', "import hashlib, copy, io, json, os, re, shutil, subprocess, sys, ast, tempfile, textwrap", _DOC_ENS, "docstring do ensaio"),
    ('or "v401" in l or "v402" in l or "v405" in l or "v406" in l}', 'or "v401" in l or "v402" in l or "v403" in l or "v405" in l or "v406" in l}', 1),   # a subida de versao perdeu o rotulo v403 da enumeracao das instrucoes etiquetadas do main
    ('+ ["caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"] + list(um._V403_NOMES_REGISTROS)   # (os registros das v399, v401, v402 e v405, recriados e comparados com os da v405 selada; o rotulo V405N e\' o da BASE)',
     '+ ["caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"] + list(um._V403_NOMES_REGISTROS) + ["projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404"] + list(um._V404_NOMES_REGISTROS)   # (os registros das v399, v401, v402, v403 e v405, recriados e comparados com os da v405 selada; o rotulo V405N e\' o da BASE)', 1),
    ('V406N = ["projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404"] + list(um._V404_NOMES_REGISTROS)   # os registros NOVOS da v406 (nao existem no core da base)',
     'V406N = list(um._V405_REGISTROS_FUNCAO) + list(um._V405_NOMES_REGISTROS)   # os registros NOVOS da v406 (nao existem no core da base)', 1),
    ('NOVAS406 = sorted(V406N)   # a v406 cria CINCO chaves no core (projecao_transversal_v404, jo8v32_v404, f2b_errata_v404, cunhagens_v404, kh_n1_cobertura_v404); os registros das v399, v401, v402 e v405 sao RECRIADOS e comparados com os da v405 selada',
     'NOVAS406 = sorted(V406N)   # a v406 cria TREZE chaves no core (os oito registros de pedra, cunhagens_v405, campos_fechados_e_leituras_v405, ga_reclassificacao_v405, gap_v405 e kh_n1_cobertura_v405); os registros das v399, v401, v402, v403 e v405 sao RECRIADOS e comparados com os da v405 selada', 1),
    ("+ list(um._V401_SPECS) + list(um._V402_SPECS) + list(um._V403_SPECS) + list(um._V404_SPECS):\n", "+ list(um._V401_SPECS) + list(um._V402_SPECS) + list(um._V403_SPECS) + list(um._V404_SPECS) + list(um._V405_SPECS):\n", 1),
    ("+ len(um._V401_SPECS) + len(um._V402_SPECS) + len(um._V403_SPECS) + len(um._V404_SPECS)\n", "+ len(um._V401_SPECS) + len(um._V402_SPECS) + len(um._V403_SPECS) + len(um._V404_SPECS) + len(um._V405_SPECS)\n", 1),
    ('k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "registros_v404")',
     'k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "registros_v405") + tuple(um._V405_REGISTROS_FUNCAO)', 1),
    ('and seal.get("qg_closure_verdict") == selo0.get("qg_closure_verdict") and ({"selo_pela_propria_tecnologia_v399", "um_version", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "registros_v404"} <= set(mud_selo) and not _selo_inexplicado)',
     'and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V405_REGISTROS_FUNCAO) and all(((seal.get("registros_v405") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V405_NOMES_REGISTROS)\n'
     '           and seal.get("qg_closure_verdict") == selo0.get("qg_closure_verdict") and (({"selo_pela_propria_tecnologia_v399", "um_version", "registros_v405"} | set(um._V405_REGISTROS_FUNCAO)) <= set(mud_selo) and not _selo_inexplicado)', 1),
    entre("# (6f) [v401, recriado na v402, na v405 e na v406 e comparado com o selado]", "# (8) o artigo", _REGIAO_6F_8, "blocos (6f) a (6j)"),
    # a guarda da ordem de chamada: AUTORAL na v406, com controle negativo
    ('U["v406_ordem_de_chamada_todo_insumo_do_core_atribuido_no_main_antes_da_leitura"] = bool(_ordem["ok"] and set((_ordem["funcoes"].get("f2b_errata_v404") or {}).get("insumos_atribuidos_no_main") or {}) >= set(_GOC.INSUMOS_EXIGIDOS["f2b_errata_v404"]))\n',
     '_ctl_ordem = _GOC.controle_negativo(src); rep["ordem_de_chamada_v406_controle_negativo"] = _ctl_ordem\nU["v406_ordem_de_chamada_todo_insumo_do_core_pronto_antes_da_leitura_com_controle_negativo"] = bool(_ordem["ok"] and _ctl_ordem["ok"] and all((_ordem["funcoes"].get(n_) or {}).get("n_chaves_lidas", 0) >= 3 for n_ in _GOC.FUNCOES_V406))\n', 1),
    ('print("ordem de chamada (guarda estatica, licao da 1a tentativa):", _ordem["ok"], "| f2b lida depois de:", sorted((_ordem["funcoes"].get("f2b_errata_v404") or {}).get("insumos_atribuidos_no_main") or {}))\n',
     'print("ordem de chamada (guarda estatica, licao da 1a tentativa):", _ordem["ok"], "| controle negativo:", _ctl_ordem["ok"])\n', 1),
    # o artigo
    ('TW406 = "Jo 8,32 e a projeção transversal da Meia-Nat"; TW406E = "John 8:32 and the transverse projection of the Half-Nat"   # a secao NOVA da v406\n',
     'TW406 = "A massa derivada e a identidade definida"; TW406E = "The derived mass and the defined identity"; TI406 = "A identidade"; TI406E = "The identity"   # as duas secoes NOVAS da v406\nTJ405 = "Jo 8,32 e a projeção transversal da Meia-Nat"; TJ405E = "John 8:32 and the transverse projection of the Half-Nat"   # (o titulo da secao da v405, que fica logo depois da v406)\n', 1),
    (_ANT_DEVE_PT, _NOV_DEVE_PT, 1),
    (_ANT_DEVE_EN, _NOV_DEVE_EN, 1),
    ('TOC = {"pt": [TW406, TC405, TP406,', 'TOC = {"pt": [TW406, TI406, TJ405, TC405, TP406,', 1),
    ('"en": [TW406E, TC405E, TP406E,', '"en": [TW406E, TI406E, TJ405E, TC405E, TP406E,', 1),
    ('cv4 = dict(copy.deepcopy(c)); [cv4.pop(k, None) for k in ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404")]\n',
     'cv4 = dict(copy.deepcopy(c)); [cv4.pop(k, None) for k in ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404")]\n'
     'cv5 = dict(copy.deepcopy(c)); [cv5.pop(k, None) for k in list(um._V405_REGISTROS_FUNCAO) + list(um._V405_NOMES_REGISTROS)]\n', 1),
    ('    _t4, _x4, _r24, _l4 = compilar(cv4, "dry_v406_var4_%s" % lang, lang, duas=False); fl4 = re.sub(r"\\s+", " ", _x4)\n',
     '    _t4, _x4, _r24, _l4 = compilar(cv4, "dry_v406_var4_%s" % lang, lang, duas=False); fl4 = re.sub(r"\\s+", " ", _x4)\n'
     '    _t5, _x5, _r25v, _l5 = compilar(cv5, "dry_v406_var5_%s" % lang, lang, duas=False); fl5 = re.sub(r"\\s+", " ", _x5)\n', 1),
    ('"rc_novo_v406": _r24, "frase_guarda_novo_v406": ("NÃO selaram todos" in fl4) if lang == "pt" else ("did NOT all seal" in fl4)}',
     '"rc_novo_v406": _r24, "frase_guarda_novo_v406": ("NÃO selaram todos" in fl4) if lang == "pt" else ("did NOT all seal" in fl4),\n'
     '                             "rc_oito_v406": _r25v, "frase_guarda_oito_v406": ("NÃO selaram todos" in fl5) if lang == "pt" else ("did NOT all seal" in fl5)}', 1),
    ('or v["rc_novo_v406"] != [0] or not v["frase_guarda_novo_v406"]]', 'or v["rc_novo_v406"] != [0] or not v["frase_guarda_novo_v406"] or v["rc_oito_v406"] != [0] or not v["frase_guarda_oito_v406"]]', 1),
    ('"jo8_v406": "Jo 8,32 e a projeção transversal da Meia-Nat (v406, 28/10/2026)" in md, "caminho_v405_fica": "Caminho, Verdade e Vida (v405, 27/10/2026)" in md,',
     '"massa_v405": "A massa derivada e a identidade definida (v406, 01/11/2026)" in md, "frase_da_moldura": "dadas essas entradas, a FORMA é teorema" in md, "jo8_v405_fica": "Jo 8,32 e a projeção transversal da Meia-Nat (v405, 28/10/2026)" in md, "caminho_v403_fica": "Caminho, Verdade e Vida (v403, 27/10/2026)" in md,', 1),
    ('_kh = [s_ for s_ in um._V404_SPECS if s_["nome"] == "kh_n1_cobertura_v404"][0]; _h8 =', '_kh = [s_ for s_ in um._V405_SPECS if s_["nome"] == "kh_n1_cobertura_v405"][0]; _h8 =', 1),
    ('_regs_sim = ("projecao_transversal_v404", "jo8v32_v404",', '_regs_sim = tuple(um._V405_REGISTROS_FUNCAO) + tuple(um._V405_NOMES_REGISTROS) + ("projecao_transversal_v404", "jo8v32_v404",', 1),
    ('"ponto_projecao": _ej.get("ponto_projecao"), "ponto_jo8v32": _ej.get("ponto_jo8v32"), "ponto_f2b": _ej.get("ponto_f2b"),', '"ponto_projecao": _ej.get("ponto_projecao"), "ponto_jo8v32": _ej.get("ponto_jo8v32"), "ponto_f2b": _ej.get("ponto_f2b"), "pontos_v406": {s_["key"]: _ej.get("ponto_v406_" + s_["key"]) for s_ in DL.STONES},', 1),
])
