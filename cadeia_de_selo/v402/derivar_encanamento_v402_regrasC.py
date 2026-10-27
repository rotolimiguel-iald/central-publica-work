# -*- coding: utf-8 -*-
# regras (lote C) de derivar_encanamento_v402.py: o ENSAIO (simular a arvore do Nos, exame dos pontos de chamada, ensaio a seco, guardas estaticas da Bancada). ORIGEM v401 (mapa 400 -> 401, 401 -> 402).
# A base mecanica sobe da v401 FINAL; a logica NOVA da v402 (os TRES registros com funcao, os specs v402, as tres pedras) entra como regras de contagem exata. Os blocos que tratam dos registros da v401 (falsidade_da_inercia_v401 etc.) voltam do arquivo
# ORIGINAL da v401 sem subida de versao (a semantica deles e' a da v401: eles agora sao RECRIADOS e comparados com os da v401 selada). Escrito pela ferramenta Write (as barras invertidas nao colapsam).

CH_ = os.path.dirname(HERE)
_ORIG_ENS = open(os.path.join(CH_, "v401", "ensaio_a_seco_v401.py"), encoding="utf-8").read()

# ------------------------------------------------------------------------------------------- simular a arvore do Nos: mais os tres registros (chamados no main logo depois da falsidade) e os specs da v402
entrada("simular_arvore_do_nos_v401.py", autoral=True, regras=[
    ("um.declaracao_do_operador_v399(core); um.falsidade_da_inercia_v401(core)   # (na fractalizacao", "um.declaracao_do_operador_v399(core); um.falsidade_da_inercia_v401(core); um.ponte_da_escala_dual_v402(core); um.queda_sem_geometria_v402(core); um.esperanca_condicional_v402(core)   # (na fractalizacao", 1),
    ("um._v399_rodar_specs(core); um._v401_rodar_specs(core)   # (v397:", "um._v399_rodar_specs(core); um._v401_rodar_specs(core); um._v402_rodar_specs(core)   # (v397:", 1),
    ('for k in ("falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", ', 'for k in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", ', 1),
    ("v394, v395, v397, v401 e v402 sobre esse kf.", "v394, v395, v397, v401 e v402 sobre esse kf (mais os tres registros com funcao da v402).", 1),
])

# ------------------------------------------------------------------------------------------- exame dos pontos de chamada: os TRES pontos novos (ponte, queda, esperanca), em ordem, logo depois da falsidade da inercia
_ANC_FAL = '''out["core.falsidade_da_inercia_v401"] = {"all_verified": fa.get("all_verified"), "verdict": str(fa.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((fa.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
'''
_BLOCO_PONTOS402 = '''# (4a-v402) os PONTOS DE CHAMADA REAIS da ponte, da queda e da esperanca (v402): as tres instrucoes do main (cada uma um `try`) que vem IMEDIATAMENTE depois da falsidade_da_inercia_v401, em ordem (ponte, queda, esperanca), na fractalizacao do Um
_ANTERIOR402 = ["falsidade_da_inercia_v401(core)", "ponte_da_escala_dual_v402(core)", "queda_sem_geometria_v402(core)"]
for nome_, fn_, off_ in (("ponte", "ponte_da_escala_dual_v402", 1), ("queda", "queda_sem_geometria_v402", 2), ("esperanca", "esperanca_condicional_v402", 3)):
    ii_ = [i for i, s_ in enumerate(unp) if fn_ + "(core)" in s_]
    assert len(ii_) == 1 and ii_[0] == ifa + off_, ("a instrucao do main que chama %s nao e' unica ou nao vem na ordem, logo depois da falsidade_da_inercia_v401" % fn_, ii_, ifa)
    ii_ = ii_[0]
    R["ponto_" + nome_] = {"indice_no_main": ii_, "linha": main.body[ii_].lineno, "antes_do_bloco_v393": ii_ < i0, "logo_depois_da_anterior": _ANTERIOR402[off_ - 1] in unp[ii_ - 1], "instrucao_anterior": unp[ii_ - 1][:160].replace("\\n", " | ")}
    builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[ii_]], type_ignores=[])), "<main:%s>" % fn_, "exec"), g); err_ = None
    except Exception as e:
        import traceback; err_ = repr(e) + traceback.format_exc()[-900:]
    finally:
        stdout_ = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
    r_ = core.get(fn_) or {}
    R["ponto_" + nome_].update({"erro": err_, "stdout": stdout_.splitlines(), "avisos": [l for l in stdout_.splitlines() if "AVISO" in l], "verdict": r_.get("verdict"), "all_verified": r_.get("all_verified"),
                                "mecanica": {"passed": (r_.get("mechanics") or {}).get("passed"), "n_checks": (r_.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (r_.get("unconditional") or {}).get("in_kernel"),
                                "estrela_in_kernel": (r_.get("key_theorem") or {}).get("in_kernel"), "contexto_ok": (r_.get("context") or {}).get("ok"), "beta_ok": r_.get("beta_ok")})
    out["core." + fn_] = {"all_verified": r_.get("all_verified"), "verdict": str(r_.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((r_.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
'''
_ANC_PV = '''pv = R["ponto_veracidade"]
'''
_FALSOS402 = '''for nome_ in ("ponte", "queda", "esperanca"):
    pp402_ = R["ponto_" + nome_]
    if (pp402_.get("erro") or pp402_.get("avisos") or pp402_.get("all_verified") is not True or not pp402_.get("antes_do_bloco_v393") or not pp402_.get("logo_depois_da_anterior") or pp402_.get("unconditional_in_kernel") is not True or pp402_.get("estrela_in_kernel") is not True
            or pp402_.get("contexto_ok") is not True or pp402_.get("beta_ok") is not True or (pp402_.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS[nome_]): falsos.append("ponto_" + nome_)
pv = R["ponto_veracidade"]
'''
entrada("exame_pontos_v401.py", autoral=True, regras=[
    ('+ ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS):\n    core.pop(n_, None)', '+ ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS) + ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS):\n    core.pop(n_, None)', 1),
    (_ANC_FAL, _ANC_FAL + _BLOCO_PONTOS402, 1),
    ('                   "v401_falsidade": [k for k in ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n',
     '                   "v401_falsidade": [k for k in ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n'
     '                   "v402_ponte_queda_esperanca": [k for k in ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n', 1),
    ('                 "registros_v401": {n_: ((seal.get("registros_v401") or {}).get(n_) or {}).get("all_verified") for n_ in um._V401_NOMES_REGISTROS}}\n',
     '                 "registros_v401": {n_: ((seal.get("registros_v401") or {}).get(n_) or {}).get("all_verified") for n_ in um._V401_NOMES_REGISTROS},\n'
     '                 "ponte_da_escala_dual_v402": {x: (seal.get("ponte_da_escala_dual_v402") or {}).get(x) for x in ("verdict", "all_verified")}, "queda_sem_geometria_v402": {x: (seal.get("queda_sem_geometria_v402") or {}).get(x) for x in ("verdict", "all_verified")},\n'
     '                 "esperanca_condicional_v402": {x: (seal.get("esperanca_condicional_v402") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v402": {n_: ((seal.get("registros_v402") or {}).get(n_) or {}).get("all_verified") for n_ in um._V402_NOMES_REGISTROS}}\n', 1),
    (_ANC_PV, _FALSOS402, 1),
])

# ------------------------------------------------------------------------------------------- as guardas estaticas da Bancada: a v399 SELADA (o defeito real) vem da copia de bytes que a cadeia v400 guardou; o mutante m6 usa um alvo errado que NAO e' o da v402
entrada("guardas_estaticas_bancada_v401.py", autoral=True, regras=[
    ('base_um = open(os.path.join(DL.V401, "base_v399", "um.py"), "rb").read()   # a v399 SELADA (o defeito real): copia de bytes guardada pela cadeia v401', 'base_um = open(os.path.join(DL.V400, "base_v399", "um.py"), "rb").read()   # a v399 SELADA (o defeito real): copia de bytes guardada pela cadeia v400', 1),
    ('(rodar("m6", cand, "v402", versao_no_selo="v402"), "UM_VERSION_DIFERENTE_DO_ALVO")', '(rodar("m6", cand, "v403", versao_no_selo="v403"), "UM_VERSION_DIFERENTE_DO_ALVO")', 1),
    ("(C:\\\\t\\\\vb18\\\\gate_*)", "(C:\\\\t\\\\vb19\\\\gate_*)", 1),
])

# ------------------------------------------------------------------------------------------- o ENSAIO A SECO
_DOC_ENS = '''"""ensaio_a_seco_v402.py -- ENSAIO A SECO da v402 (molde: ensaio_a_seco_v401.py FINAL, que rodou na cadeia da v401, com as licoes da v399, v400 e v401), SEM a GPU do rito e SEM rodar o rito. Chama NO PONTO DE CHAMADA REAL todo veredito novo ou alterado.
uso: python -B -X utf8 ensaio_a_seco_v402.py <candidato.py> <rotulo>
A v402 e' uma versao de CONTEUDO: TRES modulos novos de kernel (TGLExt/PonteDaEscalaDual, do Codex, ORDEM 025; TGLExt/QuedaSemGeometria; TGLExt/EsperancaCondicional: nomes provisorios), os registros com FUNCAO ponte_da_escala_dual_v402, queda_sem_geometria_v402 e esperanca_condicional_v402 e os registros por spec cunhagens_v402 e kh_n1_cobertura_v402.
A base e' a v401 SELADA (core e selo em base_v401), o kernel e' o da v401 + as tres pedras (sandbox C:/t/k402c); os registros de v393 a v399 E OS DA V401 (falsidade_da_inercia_v401, cunhagens_v401, kh_n1_cobertura_v401) sao RECRIADOS e comparados com os da v401 selada
(os rotulos 'v401' dos nomes de relatorio herdados da subida de versao significam a base selada). Etapas:
(1) copia o candidato; materializa o kernel embutido e confere BYTE A BYTE contra o sandbox; (2) importa (o rito NAO roda); UM_VERSION v402; (3) o core da v401 SELADA + o kernel REAL: verify_tgl_kernel_formalization() de ponta a ponta com o lake simulado devolvendo os logs CRUS do sandbox;
(4) os registros vizinhos RECOMPUTADOS: iguais, ou a TROCA DITA (so' numeros: a escada e a cobertura crescem com as pedras); (5) o FLUXO PRINCIPAL v393 a v399, v401 e v402 (as instrucoes etiquetadas do main, na ordem do arquivo), as chaves NOVAS no core: as cinco da v402;
(6) unidade: o Teste da Unica Palavra (v397), o sonico e a afinacao (v398), o selo pela propria tecnologia e a declaracao do operador (v399), a FALSIDADE DA INERCIA (v401, recriada), os TRES registros com funcao da v402 (cada elo recusa), os registros por spec, a cobertura, o sidecar;
(7) o selo (a instrucao `seal = {...}` do main + o resumo) e o indice; (8) artigo PT/EN, pdflatex x2, a secao v402 (antes da v401) e o QUADRO NO TOPO (v397, intocado); (9) .md e manifesto; (10) o conferidor de citacoes; (11) simular_arvore_do_nos; (12) exame_pontos;
(13) [LICAO DA v400, mantida] as guardas ESTATICAS do esboco R3.5 da Bancada (ALPHA_LINHA_UNICA e as demais que nao dependem do selo) rodadas SOBRE O CANDIDATO, chamando a funcao do proprio esboco pinado, ANTES de instalar."""
'''
_6F = _ORIG_ENS[_ORIG_ENS.index("# (6f) [v401] o registro com FUNCAO falsidade_da_inercia_v401"):_ORIG_ENS.index('rep["unidade"] = U; print("unidade:"')]
_6F = (_6F.replace('len(DL.STONES[0]["contract"])', 'len(DL.D1.STONES[0]["contract"])').replace("len(DL.VERBATIM_ORIGEM_V401)", "len(DL.D1.VERBATIM_ORIGEM_V401)")
       .replace("# (6f) [v401] o registro com FUNCAO falsidade_da_inercia_v401:", "# (6f) [v401, recriado na v402 e comparado com o selado] o registro com FUNCAO falsidade_da_inercia_v401:"))
assert _6F.count("DL.D1.STONES[0]") == 1 and _6F.count("DL.D1.VERBATIM_ORIGEM_V401") >= 1 and "falsidade_da_inercia_v401" in _6F
_6G = '''# (6g) [v402] os TRES registros com FUNCAO da v402 (ponte_da_escala_dual_v402, queda_sem_geometria_v402, esperanca_condicional_v402): tudo certo, os numeros RECALCULADOS aqui por outro caminho, e cada elo recusa visivelmente (controles negativos); as tres inscricoes de 26/10, as decisoes, as erratas E1-E4 e o spec da cobertura
import types as _types2
_REG402 = (("ponte", "ponte_da_escala_dual_v402", "exp"), ("queda", "queda_sem_geometria_v402", "exp"), ("esperanca", "esperanca_condicional_v402", "sin"))
R402 = {}
_bf2 = um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e)
for k402_, n402_, tamper_ in _REG402:
    fn_ = getattr(um, n402_); C_ = um._V402_CONTRACTS[k402_]; T_ = um._V402_TEXTS[k402_]
    r_ = fn_(cs()); R402[k402_] = r_
    U["v402_%s_tudo_certo" % k402_] = bool(r_["all_verified"] is True and r_["verdict"] == T_["veredito_ok"] and r_["runtime_executed"] is True and r_["does_not_gate_core"] is True and all(ck_["ok"] for ck_ in r_["mechanics"]["checks"]) and r_["mechanics"]["n_checks"] == DL.N_CHECKS[k402_]
                                           and r_["exact_ladder"] is True and r_["embedded_source_ok"] is True and r_["unconditional"]["in_kernel"] is True and r_["key_theorem"]["in_kernel"] is True and all(r_["formal_theorems"].values()) and all(r_["support_theorems"].values())
                                           and all(r_["inscriptions"].values()) and r_["context"]["ok"] is True and r_["beta_ok"] is True)
    U["v402_%s_veredito_e_textos_sem_palavra_proibida" % k402_] = bool(not guarda_txt(r_) and not _GUARDA98.search(r_["verdict"]) and not um._v392_guarda_texto(json.dumps(r_["mechanics"]["checks"], ensure_ascii=False)) and not r_["guarda_p18_violacoes"])
    ok_ = True
    for th_, fl_ in C_["theorems"].items():   # bandeira falsa de CADA declaracao do contrato (a estrela e a composicao entre elas)
        c_ = cs(); c_["kernel_formalization"][fl_] = False; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and rr_["formal_theorems"][th_] is False
    U["v402_%s_bandeira_falsa_de_cada_declaracao_do_contrato_recusa" % k402_] = bool(ok_ and len(C_["theorems"]) == len(DL.STONE_BY_KEY[k402_]["contract"]) and C_["key_theorem"]["theorem"] in C_["theorems"] and C_["unconditional"]["theorem"] in C_["theorems"])
    ok_ = True
    for th_ in list(C_["theorems"]) + list(C_["support"]):   # axioma fora do trio em CADA termo lido
        c_ = cs(); c_["kernel_formalization"]["axiom_report"][th_] = ["propext", "sorryAx"]; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U["v402_%s_axioma_fora_do_trio_em_cada_termo_lido_recusa" % k402_] = bool(ok_)
    ok_ = True
    for th_ in [C_["unconditional"]["theorem"], C_["key_theorem"]["theorem"]] + list(C_["support"]):   # proveniencia errada
        c_ = cs(); c_["kernel_formalization"]["declaration_sources_v394"][th_] = "TGLExt/Outro.lean"; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U["v402_%s_proveniencia_errada_recusa" % k402_] = bool(ok_)
    c_ = cs(); c_["kernel_formalization"]["formal_files_sha256"][C_["stone"]["path"]] = "0" * 64; rr_ = fn_(c_)
    ef_ = dict(um._EMBEDDED_KERNEL_FILES); um._EMBEDDED_KERNEL_FILES[C_["stone"]["path"]] += " "
    try:
        rr2_ = fn_(cs())
    finally:
        um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
    U["v402_%s_fonte_da_pedra_adulterada_recusa" % k402_] = bool(rr_["all_verified"] is False and rr_["embedded_source_ok"] is False and rr2_["all_verified"] is False and rr2_["embedded_source_ok"] is False)
    c_ = cs(); c_["external_ladder"]["n_theorems_clean"] = int(c_["external_ladder"]["n_theorems_clean"]) - 1; rr_ = fn_(c_)
    c2_ = cs(); c2_["kernel_formalization"]["all_verified"] = False; rr2_ = fn_(c2_)
    U["v402_%s_escada_errada_ou_kernel_nao_verificado_recusa" % k402_] = bool(rr_["all_verified"] is False and rr_["exact_ladder"] is False and rr2_["all_verified"] is False)
    ok_ = True
    for ch_ in C_["verbatins"]:
        _ant = um._V402_VERBATINS2[ch_]["text"]; um._V402_VERBATINS2[ch_]["text"] += " "   # restaurado NO LUGAR (o objeto e' compartilhado com _V392_VERBATINS2)
        try:
            rr_ = fn_(cs()); ok_ = ok_ and rr_["all_verified"] is False and rr_["inscriptions"][ch_] is False
        finally:
            um._V402_VERBATINS2[ch_]["text"] = _ant
    U["v402_%s_inscricao_adulterada_recusa" % k402_] = bool(ok_ and len(C_["verbatins"]) == {"ponte": 0, "queda": 2, "esperanca": 2}[k402_])
    ef_ = dict(um._EMBEDDED_KERNEL_FILES); _cp = C_["context"]["path"]; um._EMBEDDED_KERNEL_FILES[_cp] = um._EMBEDDED_KERNEL_FILES[_cp].replace(C_["context"]["needles"][0], "xx")
    try:
        rr_ = fn_(cs())
    finally:
        um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
    U["v402_%s_texto_contexto_retirado_do_kernel_recusa" % k402_] = bool(r_["context"]["ok"] is True and rr_["all_verified"] is False and rr_["context"]["text_in_embedded_kernel"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"])
    c_ = cs(); c_["beta"] = c_["beta"] * 1.001; _rb = fn_(c_)
    _a0 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a0 * 1.001
    try:
        _ra = fn_(cs())
    finally:
        um.SEALED_CODATA_ALPHA = _a0
    U["v402_%s_beta_adulterado_recusa" % k402_] = bool(_rb["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _rb["verdict"] and _ra["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _ra["verdict"])
    _m0 = um._m402
    um._m402 = _types2.SimpleNamespace(**{k_: getattr(_math, k_) for k_ in dir(_math) if not k_.startswith("__")}); setattr(um._m402, tamper_, (lambda f_: (lambda x_: f_(x_) * 1.001))(getattr(_math, tamper_)))
    try:
        _rn = fn_(cs())
    finally:
        um._m402 = _m0
    U["v402_%s_numero_adulterado_recusa" % k402_] = bool(_rn["all_verified"] is False and "MECHANICS_CHECK_FAILED" in _rn["verdict"] and any(not ck_["ok"] for ck_ in _rn["mechanics"]["checks"]))
_pv2, _qv2, _ev2 = R402["ponte"]["values"], R402["queda"]["values"], R402["esperanca"]["values"]
_eps2 = (1e-3, 1e-6, 1e-12, 1e-30)
U["v402_ponte_numeros_recalculados_aqui"] = bool(abs(_pv2["beta"] - _bf2) <= 1e-15 and abs(_pv2["pplus_factor_at_beta"] - _math.exp(-_bf2)) <= 1e-15 and abs(_pv2["cosh_beta_minus_one"] - (_math.cosh(_bf2) - 1.0)) <= 1e-15 and abs(_pv2["min_null_energy_shift"] - (1.0 - _math.exp(-0.25))) <= 1e-12
                                                  and abs(_pv2["min_rest_energy_shift"] - 2.0 * (_math.cosh(0.25) - 1.0)) <= 1e-12 and [round(x_, 9) for x_ in _pv2["lifts_same_pplus_masses"]] == [1.0, 4.0, 9.0] and _pv2["rest_lift"] == [3.0, 0.0] and _pv2["off_rest_lift"] == [5.0, -4.0] and _pv2["fixed_by_every_boost"] == [[0.0, 0.0]]
                                                  and abs(_pv2["rest_post_min_displacement"] - _math.hypot(_math.cosh(0.25) - 1.0, _math.sinh(0.25))) <= 1e-12 and _pv2["rest_energy_c2"] == 12.0 and _pv2["grid_scales"] == 25 and _pv2["n_states"] == 8)
U["v402_queda_numeros_recalculados_aqui"] = bool(abs(_qv2["beta"] - _bf2) <= 1e-15 and abs(_qv2["post_weight_at_scale_one"] - _math.exp(-1.0)) <= 1e-15 and abs(_qv2["post_weight_at_minus_one"] - _math.e) <= 1e-12 and abs(_qv2["min_cost_t_beta_g"] - 0.1 * _bf2 * 0.5) <= 1e-18
                                                 and abs(_qv2["max_dephasing_factor"] - _math.exp(-0.1 * _bf2 * 0.5)) <= 1e-15 and abs(_qv2["dephasing_factor_at_t1_g1"] - _math.exp(-_bf2)) <= 1e-15 and abs(_qv2["loss_per_unit"] - (1.0 - _math.exp(-_bf2))) <= 1e-15 and _qv2["grid_scales"] == 161
                                                 and _qv2["angular_period"] == 2.0 * _math.pi and _qv2["finite_model_group_order"] == 12 and _qv2["diag_flow_gap_zero_is_fixed"] is True and [[e_, s_] for e_, s_ in ((e_, -_math.log(e_) + 1.0) for e_ in _eps2)] == _qv2["abyss_witnesses"])
U["v402_esperanca_numeros_recalculados_aqui"] = bool(abs(_ev2["beta"] - _bf2) <= 1e-15 and abs(_ev2["theta_M"] - _math.asin(_math.sqrt(_bf2))) <= 1e-15 and abs(_ev2["sin2_theta_M"] - _bf2) <= 1e-15 and abs(_ev2["name_index_one_over_beta"] - 1.0 / _bf2) <= 1e-9 and 83.1 < _ev2["name_index_one_over_beta"] < 83.2
                                                    and _ev2["diagonal_expectation_pp_constant"] == 0.5 and _ev2["diagonal_expectation_index_M2"] == 2 and _ev2["test_matrices"] == 6 and _ev2["test_angles"] == 5 and _ev2["gns_dimension"] == 4)
U["v402_a_forma_literal_de_H_tau_e_refutada_e_as_pendencias_nomeadas_ditas"] = bool("literal_h_tau" in R402["ponte"] and R402["ponte"]["literal_h_tau"]["status"] == "REFUTED_IN_THE_KERNEL" and [x_["name"] for x_ in R402["ponte"]["named_pending"]] == ["H_BW", "H_cal", "H3", "signature", "rank_c_4"] and all(x_["status"] == "OPEN" for x_ in R402["ponte"]["named_pending"])
                                                                      and len(R402["ponte"]["erratas_ao_lado"]) == 4 and R402["ponte"]["assinatura_das_erratas"].startswith("gerencia c1, em nome proprio") and R402["ponte"]["maxheartbeats_ponte"] == 2000000
                                                                      and any("H_tau" in x_ and "OPEN" in x_ for x_ in R402["ponte"]["limites"]) and any("E = mc^2" in x_ for x_ in R402["ponte"]["nao_diz"]) and any("Bisognano" in x_ for x_ in R402["ponte"]["nao_diz"]))
U["v402_queda_o_chao_e_o_posto_a_isotropia_e_nomeada_e_a_dimensao_nao_e_provada"] = bool(R402["queda"]["floor"]["is_never"].startswith("the infimum 0") and R402["queda"]["named_hypothesis"]["name"] == "IsotropicPost" and R402["queda"]["named_hypothesis"]["status"] == "OPEN" and R402["queda"]["reading_1_plus_3"]["dimension_three_proved"] is False and R402["queda"]["reading_1_plus_3"]["status"] == "ONTO"
                                                                                          and R402["queda"]["operator_question_and_answer_26oct"]["resposta"] == "a seta da queda da fase, nao do espaco")
U["v402_esperanca_tres_faces_de_um_objeto_fixo_e_indice_condicional"] = bool(R402["esperanca"]["three_faces_of_one_object"]["status"] == "ONTO" and R402["esperanca"]["index_conditional"]["instance_built"] is False and len(R402["esperanca"]["index_conditional"]["hypotheses"]) == 2
                                                                         and R402["esperanca"]["four_languages"]["status"] == "INPUT" and "[LEGAL]" in R402["esperanca"]["four_languages"]["legal_pointer"])
# as tres inscricoes de 26/10, as decisoes D11-D16, a pergunta e a resposta de 26/10 e as erratas E1-E4 (registro cunhagens_v402)
_cn2 = c.get("cunhagens_v402") or {}
_sp2 = [s_ for s_ in um._V402_SPECS if s_["nome"] == "cunhagens_v402"][0]
U["cunhagens_v402_tres_falas_decisoes_erratas_e_leitura_de_26out"] = bool(_cn2.get("all_verified") is True and len(_cn2.get("verbatim") or {}) == len(DL.VERBATIM_ORIGEM_V402) == 3 and all(v_["embedded_ok"] for v_ in (_cn2.get("verbatim") or {}).values())
                                                                          and len(_cn2.get("erratas") or []) == 4 and all(e_["assinatura"].startswith("gerencia c1, em nome proprio") for e_ in (_cn2.get("erratas") or [])) and "REFUTADA" in (_cn2.get("erratas") or [{}])[0].get("agora", "")
                                                                          and len(_cn2.get("leituras_do_operador") or []) == len(_sp2["leituras_do_operador"]) and set((_cn2.get("extras") or {}).get("decisoes_da_gerencia") or {}) >= {"D11", "D12", "D13", "D14", "D15", "D16"}
                                                                          and ((_cn2.get("extras") or {}).get("leitura_26out_direcao") or {}).get("resposta") == "a seta da queda da fase, nao do espaco" and (_cn2.get("extras") or {}).get("estrelas") == {s_["key"]: s_["key_theorem"] for s_ in DL.STONES}
                                                                          and (_cn2.get("extras") or {}).get("teoremas") == {s_["key"]: s_["theorem"] for s_ in DL.STONES} and len((_cn2.get("extras") or {}).get("erratas_E1_a_E4") or []) == 4)
_kh2 = c.get("kh_n1_cobertura_v402") or {}; _kh1s = [s_ for s_ in um._V401_SPECS if s_["nome"] == "kh_n1_cobertura_v401"][0]
U["kh_n1_cobertura_v401_virou_piso_e_a_v402_cobra_a_igualdade_exata"] = bool(_kh2.get("all_verified") is True and (c.get("kh_n1_cobertura_v401") or {}).get("all_verified") is True
                                                                            and {ck_["id"]: ck_["op"] for ck_ in _kh1s["checks"] if ck_["id"] in ("h2", "h3", "h6", "h8")} == {"h2": "maior_igual", "h3": "maior_igual", "h6": "tamanho_maior_igual", "h8": "tamanho_maior_igual"} and len(_kh1s["erratas"]) >= 1
                                                                            and {ck_["id"]: ck_["op"] for ck_ in [s_ for s_ in um._V402_SPECS if s_["nome"] == "kh_n1_cobertura_v402"][0]["checks"] if ck_["id"] in ("h2", "h3", "h6", "h8")} == {"h2": "igual", "h3": "igual", "h6": "tamanho_igual", "h8": "igual"})
U["contratos_v394_a_v401_pinam_a_escada_da_v402"] = bool(all(getattr(um, nm_)["expected_ladder"] == ESP for nm_ in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V401_FALSIDADE_CONTRACT")))
rep["v402_registros"] = {k_: {"verdict": r_["verdict"], "all_verified": r_["all_verified"], "n_checks": r_["mechanics"]["n_checks"], "values": r_["values"], "unconditional": r_["unconditional"], "key_theorem": r_["key_theorem"], "context": r_["context"]} for k_, r_ in R402.items()}
'''
_ANC_UNIDADE = '''rep["unidade"] = U; print("unidade:"'''
# titulos do artigo (secao 8)
_TIT_ANTES = '''TF402 = "A falsidade (simulacro) da inércia"; TF402E = "The falsity (simulacrum) of inertia"
'''
_TIT_DEPOIS = '''TP402 = "A ponte da escala dual, a queda sem geometria e a esperança condicional"; TP402E = "The dual-scale bridge, the fall without geometry and the conditional expectation"
TF402 = "A falsidade (simulacro) da inércia"; TF402E = "The falsity (simulacrum) of inertia"   # (o titulo da secao da v401, que fica logo depois da v402)
'''
_VAR_ANTES = '''cv1 = dict(copy.deepcopy(c)); [cv1.pop(k, None) for k in ("falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401")]
'''
_VAR_DEPOIS = _VAR_ANTES + '''cv2 = dict(copy.deepcopy(c)); [cv2.pop(k, None) for k in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402")]
'''
_VAR2_ANTES = '''    _t1, _x1, _r21, _l1 = compilar(cv1, "dry_v402_var1_%s" % lang, lang, duas=False); fl1 = re.sub(r"\\s+", " ", _x1)
'''
_VAR2_DEPOIS = _VAR2_ANTES + '''    _t2, _x2, _r22, _l2 = compilar(cv2, "dry_v402_var2_%s" % lang, lang, duas=False); fl2 = re.sub(r"\\s+", " ", _x2)
'''
_VAR3_ANTES = '''"rc_v402": _r21, "frase_guarda_v402": ("NÃO selaram todos" in fl1) if lang == "pt" else ("did NOT all seal" in fl1)}
'''
_VAR3_DEPOIS = '''"rc_v401": _r21, "frase_guarda_v401": ("NÃO selaram todos" in fl1) if lang == "pt" else ("did NOT all seal" in fl1),
                             "rc_v402": _r22, "frase_guarda_v402": ("NÃO selaram todos" in fl2) if lang == "pt" else ("did NOT all seal" in fl2)}
'''
entrada("ensaio_a_seco_v401.py", autoral=True, regras=[
    entre('"""ensaio_a_seco_v402.py', "import hashlib, copy, io, json, os, re, shutil, subprocess, sys, ast, tempfile, textwrap", _DOC_ENS, "docstring do ensaio"),
    ('V401N = ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS)   # (os registros da v399, recriados; o rotulo V401N e\' herdado da subida de versao)\n',
     'V401N = ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS) + ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS)   # (os registros das v399 e v401, recriados e comparados com os da v401 selada; o rotulo V401N e\' herdado da subida de versao)\n', 1),
    ('V402N = ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS)   # os registros NOVOS da v402 (nao existem no core da base)\n',
     'V402N = ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS)   # os registros NOVOS da v402 (nao existem no core da base)\n', 1),
    ('or "v399" in l or "v402" in l}', 'or "v399" in l or "v401" in l or "v402" in l}', 1),
    ('NOVAS402 = sorted(V402N)   # a v402 cria TRES chaves no core (falsidade_da_inercia_v401, cunhagens_v401, kh_n1_cobertura_v401); os registros da v399 sao RECRIADOS e comparados com os da v401 selada',
     'NOVAS402 = sorted(V402N)   # a v402 cria CINCO chaves no core (ponte_da_escala_dual_v402, queda_sem_geometria_v402, esperanca_condicional_v402, cunhagens_v402, kh_n1_cobertura_v402); os registros das v399 e v401 sao RECRIADOS e comparados com os da v401 selada', 1),
    ('+ ["sonico_v398", "afinacao_das_cordas_v398", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + V402N)', '+ ["sonico_v398", "afinacao_das_cordas_v398", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + V401N + V402N)', 1),
    ('_fo9 = os.path.join(DL.V401, "insumos", "acom", "fontes_operador")', '_fo9 = os.path.join(DL.V400, "insumos", "acom", "fontes_operador")', 1),
    ("+ list(um._V399_SPECS) + list(um._V401_SPECS):\n    n_ = sp_[\"nome\"]; r_ = {}", "+ list(um._V399_SPECS) + list(um._V401_SPECS) + list(um._V402_SPECS):\n    n_ = sp_[\"nome\"]; r_ = {}", 1),
    ("+ len(um._V399_SPECS) + len(um._V401_SPECS)\n", "+ len(um._V399_SPECS) + len(um._V401_SPECS) + len(um._V402_SPECS)\n", 1),
    ('"falsidade_da_inercia_v401", "registros_v401") and not _selo_explica(k_))', '"ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402") and not _selo_explica(k_))', 1),
    ('           and (seal.get("falsidade_da_inercia_v401") or {}).get("all_verified") is True and all(((seal.get("registros_v401") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V401_NOMES_REGISTROS)\n',
     '           and (seal.get("falsidade_da_inercia_v401") or {}).get("all_verified") is True and all(((seal.get("registros_v401") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V401_NOMES_REGISTROS)\n'
     '           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402")) and all(((seal.get("registros_v402") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V402_NOMES_REGISTROS)\n', 1),
    ('({"selo_pela_propria_tecnologia_v399", "um_version", "falsidade_da_inercia_v401", "registros_v401"} <= set(mud_selo) and not _selo_inexplicado)', '({"selo_pela_propria_tecnologia_v399", "um_version", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402"} <= set(mud_selo) and not _selo_inexplicado)', 1),
    entre("# (6f) [v401] o registro com FUNCAO falsidade_da_inercia_v401", _ANC_UNIDADE, _6F + _6G, "os blocos (6f) da v401 (restaurado do original) e (6g) da v402"),
    (_TIT_ANTES, _TIT_DEPOIS, 1),
    ('DEVE = {"pt": [TF402, "A definição do operador."', 'DEVE = {"pt": [TP402, "A ponte da escala dual.", "Erratas ao lado", "A queda sem geometria.", "A esperança condicional é o Nome.", TF402, "A definição do operador."', 1),
    ('"en": [TF402E, "The operator\'s definition."', '"en": [TP402E, "The dual-scale bridge.", "Errata beside", "The fall without geometry.", "The conditional expectation is the Name.", TF402E, "The operator\'s definition."', 1),
    ('TN402, "Errata ao lado (v401).", "A direção do testemunho."', 'TN402, "Errata ao lado (v400).", "A direção do testemunho."', 1),
    ('TN402E, "Erratum beside it (v401).", "The direction of the testimony."', 'TN402E, "Erratum beside it (v400).", "The direction of the testimony."', 1),
    ('TOC = {"pt": [TF402, TN402,', 'TOC = {"pt": [TP402, TF402, TN402,', 1),
    ('"en": [TF402E, TN402E, TS402E, T402E, T401E, "v384 to v402"]', '"en": [TP402E, TF402E, TN402E, TS402E, T402E, T401E, "v384 to v402"]', 1),
    ('h0 = TF402 if lang == "pt" else TF402E; h1 = TN402 if lang == "pt" else TN402E', 'h0 = TP402 if lang == "pt" else TP402E; h1 = TN402 if lang == "pt" else TN402E', 1),
    (_VAR_ANTES, _VAR_DEPOIS, 1),
    (_VAR2_ANTES, _VAR2_DEPOIS, 1),
    (_VAR3_ANTES, _VAR3_DEPOIS, 1),
    ('or v["rc_v402"] != [0] or not v["frase_guarda_v402"]]', 'or v["rc_v401"] != [0] or not v["frase_guarda_v401"] or v["rc_v402"] != [0] or not v["frase_guarda_v402"]]', 1),
    ('"falsidade_v402": "A falsidade (simulacro) da inércia (v402, 25/10/2026)" in md, "errata_v401_fica": "Errata ao lado (v401, 24/10/2026)" in md,',
     '"ponte_v402": "A ponte da escala dual, a queda sem geometria e a esperança condicional (v402, 26/10/2026)" in md, "falsidade_v401_fica": "A falsidade (simulacro) da inércia (v401, 25/10/2026)" in md, "errata_v400_fica": "Errata ao lado (v400, 24/10/2026)" in md,', 1),
    ('_kh = [s_ for s_ in um._V401_SPECS if s_["nome"] == "kh_n1_cobertura_v401"][0]; _h8', '_kh = [s_ for s_ in um._V402_SPECS if s_["nome"] == "kh_n1_cobertura_v402"][0]; _h8', 1),
    ('_regs_sim = ("falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", ', '_regs_sim = ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", ', 1),
    ('"ponto_falsidade": _ej.get("ponto_falsidade"), ', '"ponto_falsidade": _ej.get("ponto_falsidade"), "ponto_ponte": _ej.get("ponto_ponte"), "ponto_queda": _ej.get("ponto_queda"), "ponto_esperanca": _ej.get("ponto_esperanca"), ', 1),
    ('"recriados_v393_a_v401": recriados, "registros_v401": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in V402N},',
     '"recriados_v393_a_v401": recriados, "registros_novos_v402": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in V402N},\n'
     '                   "registros_v401": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS)},', 1),
])
