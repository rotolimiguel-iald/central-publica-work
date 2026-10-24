# v398x: os registros sonico_v398 e afinacao_das_cordas_v398 pelas INSTRUCOES REAIS do main (os dois `try` que os chamam, executados como estao no candidato), na ordem
# (logo depois do `try` da testemunha estatica, antes do bloco da v393); adjacencia por AST; o `try` da testemunha e o do psibit iguais aos do um.py instalado; nao mexem em
# chave existente; os numeros recalculados AQUI (beta = SEALED_CODATA_ALPHA x sqrt(e); H2; ln 2; Bernoulli); controles negativos (copias profundas; o modulo e' restaurado)
if hasattr(um, "sonico_v398") and hasattr(um, "afinacao_das_cordas_v398"):
    _src8 = open(dst, encoding="utf-8").read(); _tree8 = ast.parse(_src8)
    _main8 = [n for n in _tree8.body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]
    _i_psb8 = [i for i, st in enumerate(_main8.body) if isinstance(st, ast.Try) and "psibit_v395(core)" in ast.unparse(st)]
    _i_tes8 = [i for i, st in enumerate(_main8.body) if isinstance(st, ast.Try) and "testemunha_estatica_v396(core)" in ast.unparse(st)]
    _i_son = [i for i, st in enumerate(_main8.body) if isinstance(st, ast.Try) and "sonico_v398(core)" in ast.unparse(st)]
    _i_afi = [i for i, st in enumerate(_main8.body) if isinstance(st, ast.Try) and "afinacao_das_cordas_v398(core)" in ast.unparse(st)]
    _i_393_8 = next(i for i, st in enumerate(_main8.body) if "regra_v393(core)" in ast.unparse(st))
    _m0_8 = [n for n in ast.parse(open(os.path.join(NOS, "um.py"), encoding="utf-8").read()).body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]
    _tes0 = [st for st in _m0_8.body if isinstance(st, ast.Try) and "testemunha_estatica_v396(core)" in ast.unparse(st)]
    _psb0 = [st for st in _m0_8.body if isinstance(st, ast.Try) and "psibit_v395(core)" in ast.unparse(st)]
    R["pedras_ponto"] = {"i_psibit": _i_psb8, "i_testemunha": _i_tes8, "i_sonico": _i_son, "i_afinacao": _i_afi, "i_v393": _i_393_8,
                         "linha_sonico": _main8.body[_i_son[0]].lineno if _i_son else None, "linha_afinacao": _main8.body[_i_afi[0]].lineno if _i_afi else None, "linha_testemunha": _main8.body[_i_tes8[0]].lineno if _i_tes8 else None,
                         "sonico_imediatamente_depois_da_testemunha": len(_i_tes8) == 1 and len(_i_son) == 1 and _i_son[0] == _i_tes8[0] + 1,
                         "afinacao_imediatamente_depois_do_sonico": len(_i_son) == 1 and len(_i_afi) == 1 and _i_afi[0] == _i_son[0] + 1,
                         "antes_do_bloco_v393": bool(_i_afi) and _i_afi[0] < _i_393_8, "testemunha_depois_do_psibit": len(_i_psb8) == 1 and len(_i_tes8) == 1 and _i_tes8[0] == _i_psb8[0] + 1,
                         "try_testemunha_igual_ao_instalado": len(_tes0) == 1 and len(_i_tes8) == 1 and ast.dump(_tes0[0]) == ast.dump(_main8.body[_i_tes8[0]]),
                         "try_psibit_igual_ao_instalado": len(_psb0) == 1 and len(_i_psb8) == 1 and ast.dump(_psb0[0]) == ast.dump(_main8.body[_i_psb8[0]]),
                         "chamadas_no_main": {"sonico_v398": sum(1 for n in ast.walk(_main8) if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "sonico_v398"),
                                              "afinacao_das_cordas_v398": sum(1 for n in ast.walk(_main8) if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "afinacao_das_cordas_v398")}}
    _antes8 = {k: J(core[k]) for k in core}
    _g8 = dict(vars(um)); _g8["core"] = core
    builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        exec(compile(ast.fix_missing_locations(ast.Module(body=[_main8.body[_i_son[0]], _main8.body[_i_afi[0]]], type_ignores=[])), "<main:sonico_afinacao_v398>", "exec"), _g8); _err8 = None
    except Exception as e:
        import traceback; _err8 = repr(e) + traceback.format_exc()[-600:]
    finally:
        _out8 = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
    R["pedras_instrucao_real"] = {"erro": _err8, "aviso": [l for l in _out8.splitlines() if "AVISO" in l or "REFUSED" in l], "stdout": _out8[-3000:]}
    R["pedras_mexeu_em_chaves_existentes"] = sorted(k for k in _antes8 if J(core.get(k)) != _antes8[k] and k not in ("sonico_v398", "afinacao_das_cordas_v398"))
    _so8 = core.get("sonico_v398") or {}; _af8 = core.get("afinacao_das_cordas_v398") or {}
    for _nm, _rg in (("sonico_v398", _so8), ("afinacao_das_cordas_v398", _af8)):
        out[_nm] = {"all_verified": _rg.get("all_verified"), "verdict": str(_rg.get("verdict"))[:300], "falhas": [str(c)[:300] for c in ((_rg.get("mechanics") or {}).get("checks") or []) if not c.get("ok")]}
    _res = lambda _rg: {k: _rg.get(k) for k in ("verdict", "all_verified", "exact_ladder", "embedded_source_ok", "beta_ok", "beta_core_rel_diff", "alpha_two_names_same", "does_not_gate_core", "runtime_executed", "guarda_p18_violacoes", "hypothesis", "geometry", "derives_strings_from_the_axiom") if k in _rg}
    R["sonico"] = _res(_so8); R["afinacao"] = _res(_af8)
    for _nm, _rg in (("sonico", _so8), ("afinacao", _af8)):
        R[_nm].update(n_checks=(_rg.get("mechanics") or {}).get("n_checks"), ids=[c.get("id") for c in ((_rg.get("mechanics") or {}).get("checks") or [])], unconditional=_rg.get("unconditional"),
                      formal_theorems_false=[k for k, v in (_rg.get("formal_theorems") or {}).items() if not v], support_false=[k for k, v in (_rg.get("support_theorems") or {}).items() if not v],
                      cited_outside_false=[k for k, v in (_rg.get("cited_outside") or {}).items() if not v], aux_false=[k for k, v in (_rg.get("auxiliaries_outside_the_composition") or {}).items() if not v],
                      inscriptions=_rg.get("inscriptions"), values=_rg.get("values"))
    # os numeros, recalculados AQUI, contra os do registro
    _b8 = um.SEALED_CODATA_ALPHA * math.sqrt(math.e); _th8 = math.asin(math.sqrt(_b8)); _c28 = math.cos(_th8) ** 2; _s28 = math.sin(_th8) ** 2
    _h28 = -_c28 * math.log(_c28) - _s28 * math.log(_s28)
    from fractions import Fraction as _Fx
    _B2 = _Fx(1, 6); _z1 = -_B2 / 2; _zh = -(_Fx(1, 4) - _Fx(1, 2) + _Fx(1, 6)) / 2
    _vs = _so8.get("values") or {}; _va = _af8.get("values") or {}
    R["numeros_independentes"] = {"beta": _b8, "theta_M_rad": _th8, "H2_nats": _h28, "H2_oitavas": _h28 / math.log(2), "ln2": math.log(2), "exp_ln2": math.exp(math.log(2)), "zeta_minus_one": str(_z1), "hurwitz_zeta_minus_one_half": str(_zh),
                                  "D_bos": [d for d in range(200) if (d - 2) * _Fx(-1, 24) == -1], "D_NS": [d for d in range(200) if (d - 2) * _Fx(-1, 16) == _Fx(-1, 2)], "D_sinal_trocado": [d for d in range(200) if (d - 2) * (_Fx(-1, 24) + _Fx(1, 48)) == _Fx(-1, 2)],
                                  "iguais_aos_do_registro": {"beta": _vs.get("beta") == _b8 and abs(core.get("beta", 0) - _b8) / _b8 <= 1e-9, "theta_M": abs(_vs.get("theta_M_rad", 9) - _th8) <= 1e-15, "H2_nats": abs(_vs.get("collapse_entropy_theta_M_nats", 9) - _h28) <= 1e-15,
                                                             "H2_oitavas": abs(_vs.get("collapse_entropy_theta_M_octaves", 9) - _h28 / math.log(2)) <= 1e-15, "ln2": _vs.get("ln2") == math.log(2) and _vs.get("octave_one_nats") == math.log(2), "exp_ln2": _vs.get("exp_ln2") == 2.0,
                                                             "zeta": _va.get("zeta_minus_one") == str(_z1), "hurwitz": _va.get("hurwitz_zeta_minus_one_half") == str(_zh), "D": (_va.get("bosonic_critical_dimension"), _va.get("superstring_critical_dimension"), _va.get("wrong_fermion_sign_dimension")) == (26, 10, 26),
                                                             "d_casa": _va.get("house_spatial_dimension") == 9, "kappa_from_core_None": _va.get("kappa_from_core") is None, "kappa_de_teste": _va.get("kappa_tests")}}
    # controles negativos
    C8s = um._V398_SONICO_CONTRACT; C8a = um._V398_AFINACAO_CONTRACT
    negp = {}
    def _kfc8(c_):
        c_["kernel_formalization"] = dict(c_["kernel_formalization"]); return c_["kernel_formalization"]
    _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        for _nm, _fn, _C in (("sonico", um.sonico_v398, C8s), ("afinacao", um.afinacao_das_cordas_v398, C8a)):
            c1 = copy.deepcopy(core); _kfc8(c1)[_C["unconditional"]["flag"]] = False; negp[_nm + ":bandeira_incondicional_falsa"] = _fn(c1).get("verdict")
            _outro = [t for t in _C["theorems"] if t != _C["unconditional"]["theorem"]][0]
            c1 = copy.deepcopy(core); _kfc8(c1)[_C["theorems"][_outro]] = False; negp[_nm + ":bandeira_de_outro_teorema_falsa"] = _fn(c1).get("verdict")
            _sup = sorted(_C["support"])[0]
            c1 = copy.deepcopy(core); k1 = _kfc8(c1); k1["axiom_report"] = dict(k1["axiom_report"]); k1["axiom_report"][_sup] = ["propext", "TGLExt.axiomaPlantado"]; negp[_nm + ":axioma_plantado_num_suporte"] = _fn(c1).get("verdict")
            c1 = copy.deepcopy(core); k1 = _kfc8(c1); k1["axiom_report"] = dict(k1["axiom_report"]); k1["axiom_report"][_C["unconditional"]["theorem"]] = ["propext", "Classical.choice", "Quot.sound", "sorryAx"]; negp[_nm + ":sorryAx_na_composicao"] = _fn(c1).get("verdict")
            c1 = copy.deepcopy(core); k1 = _kfc8(c1); k1["declaration_sources_v394"] = dict(k1["declaration_sources_v394"]); k1["declaration_sources_v394"][_outro] = "TGLExt/Psibit.lean"; negp[_nm + ":proveniencia_de_um_teorema_em_outro_modulo"] = _fn(c1).get("verdict")
            c1 = copy.deepcopy(core); k1 = _kfc8(c1); k1["formal_files_sha256"] = dict(k1["formal_files_sha256"]); k1["formal_files_sha256"][_C["stone"]["path"]] = "0" * 64; negp[_nm + ":sha_da_pedra_errado_no_kernel"] = _fn(c1).get("verdict")
            c1 = copy.deepcopy(core); c1["external_ladder"] = dict(c1["external_ladder"]); c1["external_ladder"]["n_theorems_clean"] -= 1; negp[_nm + ":escada_nao_fecha"] = _fn(c1).get("verdict")
            c1 = copy.deepcopy(core); k1 = _kfc8(c1); k1["all_verified"] = False; negp[_nm + ":kernel_nao_verificado"] = _fn(c1).get("verdict")
            _vb = um._V398_VERBATINS2; _k0 = _C["verbatins"][0]
            try:
                um._V398_VERBATINS2 = copy.deepcopy(_vb); um._V398_VERBATINS2[_k0]["text"] = _vb[_k0]["text"][:-1] + ("!" if not _vb[_k0]["text"].endswith("!") else "?")
                negp[_nm + ":inscricao_adulterada"] = _fn(copy.deepcopy(core)).get("verdict")
            finally:
                um._V398_VERBATINS2 = _vb
            _emb0 = um._EMBEDDED_KERNEL_FILES
            try:
                um._EMBEDDED_KERNEL_FILES = dict(_emb0); um._EMBEDDED_KERNEL_FILES[_C["stone"]["path"]] = _emb0[_C["stone"]["path"]] + "\n-- adulterada\n"
                negp[_nm + ":fonte_embutida_adulterada"] = _fn(copy.deepcopy(core)).get("verdict")
            finally:
                um._EMBEDDED_KERNEL_FILES = _emb0
        # os especificos
        c1 = copy.deepcopy(core); c1["beta"] = c1["beta"] * (1 + 1e-6); negp["sonico:beta_do_core_adulterado"] = um.sonico_v398(c1).get("verdict")
        _alfa = um.SEALED_CODATA_ALPHA
        try:
            um.SEALED_CODATA_ALPHA = _alfa * (1 + 1e-6); negp["sonico:alfa_selado_adulterado"] = um.sonico_v398(copy.deepcopy(core)).get("verdict")
        finally:
            um.SEALED_CODATA_ALPHA = _alfa
        c1 = copy.deepcopy(core); k1 = _kfc8(c1); k1["declaration_sources_v394"] = dict(k1["declaration_sources_v394"]); k1["declaration_sources_v394"]["TGLExt.AfinacaoDasCordas.matsubaraFermion"] = "TGLExt/Palavra.lean"
        negp["afinacao:auxiliar_declarada_fora_da_pedra"] = um.afinacao_das_cordas_v398(c1).get("verdict")
        c1 = copy.deepcopy(core); k1 = _kfc8(c1); k1["declaration_sources_v394"] = dict(k1["declaration_sources_v394"]); k1["declaration_sources_v394"]["TGLExt.IALD.rereading_adds_nothing"] = "TGLExt/Sonico.lean"
        negp["sonico:citado_fora_com_proveniencia_errada"] = um.sonico_v398(c1).get("verdict")
        _h20 = um._v398_h2
        try:
            um._v398_h2 = lambda p_: (0.0 if p_ <= 0 or p_ >= 1 else -p_ * math.log(p_))   # metade da entropia: numero adulterado
            _mm = um.v398_sonico_mechanics(_b8); negp["sonico:mecanica_numero_adulterado_passed"] = _mm.get("passed"); negp["sonico:mecanica_numero_adulterado_falhas"] = [c["id"] for c in _mm["checks"] if not c["ok"]]
            negp["sonico:registro_com_numero_adulterado"] = um.sonico_v398(copy.deepcopy(core)).get("verdict")
        finally:
            um._v398_h2 = _h20
        _bn0 = um._v398_bernoulli
        try:
            um._v398_bernoulli = lambda n_: [_Fx(1), _Fx(-1, 2), _Fx(1, 5)] + [_Fx(0)] * (n_ - 2)   # B_2 errado: numero adulterado
            _mm = um.v398_afinacao_mechanics(); negp["afinacao:aritmetica_numero_adulterado_passed"] = _mm.get("passed"); negp["afinacao:aritmetica_numero_adulterado_falhas"] = [c["id"] for c in _mm["checks"] if not c["ok"]]
            negp["afinacao:registro_com_numero_adulterado"] = um.afinacao_das_cordas_v398(copy.deepcopy(core)).get("verdict")
        finally:
            um._v398_bernoulli = _bn0
        negp["sonico:mecanica_beta_fora_de_0_1_passed"] = um.v398_sonico_mechanics(1.5).get("passed"); negp["sonico:mecanica_beta_int_passed"] = um.v398_sonico_mechanics(0).get("passed")
        negp["positivo:sonico"] = um.sonico_v398(copy.deepcopy(core)).get("verdict"); negp["positivo:afinacao"] = um.afinacao_das_cordas_v398(copy.deepcopy(core)).get("verdict")
    finally:
        sys.stdout = _so
    _pas8 = [k for k in negp if k.endswith("_passed")]
    negp["todos_recusam"] = all(isinstance(v, str) and "REFUSED" in v for k, v in negp.items() if not k.endswith(("_passed", "_falhas")) and not k.startswith("positivo:") and k != "todos_recusam") and all(negp[k] is False for k in _pas8)
    negp["positivos_selam"] = negp["positivo:sonico"] == um._V398_SONICO_TEXT["veredito_ok"] and negp["positivo:afinacao"] == um._V398_AFINACAO_TEXT["veredito_ok"]
    negp["n_negativos"] = sum(1 for k in negp if not k.endswith(("_passed", "_falhas")) and not k.startswith("positivo:") and k not in ("todos_recusam", "positivos_selam", "n_negativos"))
    R["pedras_controles_negativos"] = negp
