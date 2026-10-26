# v400x (do v399x; a v400 e' a CORRECAO: alfa nao redeclarado, beta do registro contra o core): o SELO PELA PROPRIA TECNOLOGIA e a DECLARACAO DO OPERADOR pelas INSTRUCOES REAIS do main (os dois `try`), logo depois do `try` da afinacao (v398) e antes do bloco
# v393; o sidecar em _unified_main depois da ultima escrita do selo; o bloco ACOM embutido == afc80b74 (texto LF); controles negativos; D4 (a recusa so' registra); o sidecar
# gravado NUMA PASTA MINHA (um.OUT redirecionado), nunca no Nos
if hasattr(um, "selo_acom_v399") and hasattr(um, "declaracao_do_operador_v399"):
    _src9 = open(dst, encoding="utf-8").read(); _tree9 = ast.parse(_src9)
    _main9 = [n for n in _tree9.body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]
    _um9 = [n for n in _tree9.body if isinstance(n, ast.FunctionDef) and n.name == "_unified_main"][-1]
    _i_afi9 = [i for i, st in enumerate(_main9.body) if isinstance(st, ast.Try) and "afinacao_das_cordas_v398(core)" in ast.unparse(st)]
    _i_sel = [i for i, st in enumerate(_main9.body) if isinstance(st, ast.Try) and "selo_acom_v399(core)" in ast.unparse(st)]
    _i_dec = [i for i, st in enumerate(_main9.body) if isinstance(st, ast.Try) and "declaracao_do_operador_v399(core)" in ast.unparse(st)]
    _i_393_9 = next(i for i, st in enumerate(_main9.body) if "regra_v393(core)" in ast.unparse(st))
    _i_ns = [i for i, st in enumerate(_main9.body) if isinstance(st, ast.Assign) and "seal['not_sealed_this_run']" in ast.unparse(st)]
    _i_res = [i for i, st in enumerate(_main9.body) if "resumos_do_selo_v399(core)" in ast.unparse(st)]
    _i_sc = [i for i, st in enumerate(_um9.body) if isinstance(st, ast.Try) and "selo_acom_sidecar_v399()" in ast.unparse(st)]
    _i_fail = [i for i, st in enumerate(_um9.body) if isinstance(st, ast.If) and "FAIL_CLOSED_SELFTEST_FAILED" in ast.unparse(st.test)]
    _i_wsel = [i for i, st in enumerate(_um9.body) if "um_absoluto_selo.json" in ast.unparse(st) and ("open(" in ast.unparse(st) or "write" in ast.unparse(st) or "dump" in ast.unparse(st))]
    _m0_9 = [n for n in ast.parse(open(os.path.join(NOS, "um.py"), encoding="utf-8").read()).body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]
    _afi0 = [st for st in _m0_9.body if isinstance(st, ast.Try) and "afinacao_das_cordas_v398(core)" in ast.unparse(st)]
    _sel0 = [st for st in _m0_9.body if isinstance(st, ast.Try) and "selo_acom_v399(core)" in ast.unparse(st)]
    _dec0 = [st for st in _m0_9.body if isinstance(st, ast.Try) and "declaracao_do_operador_v399(core)" in ast.unparse(st)]
    _um0_9 = [n for n in ast.parse(open(os.path.join(NOS, "um.py"), encoding="utf-8").read()).body if isinstance(n, ast.FunctionDef) and n.name == "_unified_main"][-1]
    _sc0 = [st for st in _um0_9.body if isinstance(st, ast.Try) and "selo_acom_sidecar_v399()" in ast.unparse(st)]
    R["v400_ponto"] = {"i_afinacao": _i_afi9, "i_selo": _i_sel, "i_declaracao": _i_dec, "i_v393": _i_393_9, "i_not_sealed_assign": _i_ns, "i_resumos": _i_res, "i_sidecar_unified": _i_sc, "i_fail_closed_unified": _i_fail, "i_escritas_do_selo_unified": _i_wsel,
                       "linha_selo": _main9.body[_i_sel[0]].lineno if _i_sel else None, "linha_declaracao": _main9.body[_i_dec[0]].lineno if _i_dec else None, "linha_afinacao": _main9.body[_i_afi9[0]].lineno if _i_afi9 else None,
                       "selo_imediatamente_depois_da_afinacao": len(_i_afi9) == 1 and len(_i_sel) == 1 and _i_sel[0] == _i_afi9[0] + 1,
                       "declaracao_imediatamente_depois_do_selo": len(_i_sel) == 1 and len(_i_dec) == 1 and _i_dec[0] == _i_sel[0] + 1,
                       "antes_do_bloco_v393": bool(_i_dec) and _i_dec[0] < _i_393_9, "resumos_logo_depois_do_not_sealed": bool(_i_ns) and bool(_i_res) and _i_res[0] == _i_ns[0] + 1,
                       "try_afinacao_igual_ao_instalado": len(_afi0) == 1 and len(_i_afi9) == 1 and ast.dump(_afi0[0]) == ast.dump(_main9.body[_i_afi9[0]]),
                       "try_selo_igual_ao_instalado_v399": len(_sel0) == 1 and len(_i_sel) == 1 and ast.dump(_sel0[0]) == ast.dump(_main9.body[_i_sel[0]]),
                       "try_declaracao_igual_ao_instalado_v399": len(_dec0) == 1 and len(_i_dec) == 1 and ast.dump(_dec0[0]) == ast.dump(_main9.body[_i_dec[0]]),
                       "try_sidecar_igual_ao_instalado_v399": len(_sc0) == 1 and len(_i_sc) == 1 and ast.dump(_sc0[0]) == ast.dump(_um9.body[_i_sc[0]]),
                       "main_igual_ao_instalado_v399": ast.dump(_m0_9) == ast.dump(_main9), "unified_main_igual_ao_instalado_v399": ast.dump(_um0_9) == ast.dump(_um9),
                       "sidecar_no_unified_main_depois_da_ultima_escrita_do_selo": bool(_i_sc) and bool(_i_fail) and _i_sc[0] + 1 == _i_fail[0] and (not _i_wsel or max(_i_wsel) < _i_sc[0]),
                       "chamadas_no_main": {"selo_acom_v399": sum(1 for n in ast.walk(_main9) if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "selo_acom_v399"), "declaracao_do_operador_v399": sum(1 for n in ast.walk(_main9) if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "declaracao_do_operador_v399")}}
    # o bloco ACOM embutido no candidato, por bytes (texto LF do primeiro INICIO ate a linha-marcador de FIM do acom_crypto)
    _t9 = open(dst, "rb").read().decode("utf-8").replace("\r\n", "\n")
    _ini9 = _t9.index("# >>> ACOM_EMBUTIDO_INICIO"); _marca9 = "# <<< ACOM_EMBUTIDO_FIM: skygrid_sim/acom_crypto.py <<<\n"; _fim9 = _t9.index(_marca9) + len(_marca9)
    R["v400_bloco_embutido"] = {"sha256_meu": hashlib.sha256(_t9[_ini9:_fim9].encode("utf-8")).hexdigest(), "declarado": um.ACOM_PROVENIENCIA["bloco_embutido_sha256"], "funcao_do_candidato": um.conferir_bloco_embutido(),
                                "igual_ao_estudo_afc80b74": hashlib.sha256(_t9[_ini9:_fim9].encode("utf-8")).hexdigest().startswith("afc80b740f71ca0a"), "linhas": _t9[_ini9:_fim9].count("\n"),
                                "fontes": {c["arquivo"].split("/")[-1]: c["sha256"][:16] for c in um.ACOM_PROVENIENCIA["codigo_embutido_de"]}, "patentes": [p_["numero"] for p_ in um.ACOM_PROVENIENCIA["patentes"]]}
    # as instrucoes reais
    _antes9 = {k: J(core[k]) for k in core}
    _g9 = dict(vars(um)); _g9["core"] = core
    builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        exec(compile(ast.fix_missing_locations(ast.Module(body=[_main9.body[_i_sel[0]], _main9.body[_i_dec[0]]], type_ignores=[])), "<main:selo_acom_e_declaracao_v399>", "exec"), _g9); _err9 = None
    except Exception as e:
        import traceback; _err9 = repr(e) + traceback.format_exc()[-600:]
    finally:
        _out9 = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
    R["v400_instrucao_real"] = {"erro": _err9, "aviso": [l for l in _out9.splitlines() if "AVISO" in l or "REFUSED" in l or "NOT_SEALED" in l], "stdout": _out9[-3500:]}
    R["v400_mexeu_em_chaves_existentes"] = sorted(k for k in _antes9 if J(core.get(k)) != _antes9[k] and k not in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"))
    _sl9 = core.get("selo_pela_propria_tecnologia_v399") or {}; _dc9 = core.get("declaracao_do_operador_v399") or {}
    out["selo_pela_propria_tecnologia_v399"] = {"all_verified": _sl9.get("all_verified"), "verdict": str(_sl9.get("verdict"))[:200], "falhas": [d_ for d_, v_ in (_sl9.get("checks") or []) if not v_]}
    out["declaracao_do_operador_v399"] = {"all_verified": _dc9.get("all_verified"), "verdict": str(_dc9.get("verdict"))[:200], "falhas": [d_ for d_, v_ in (_dc9.get("checks") or []) if not v_]}
    _s9 = _sl9.get("selo") or {}; _a9 = _s9.get("acom") or {}
    R["selo_acom"] = {"verdict": _sl9.get("verdict"), "all_verified": _sl9.get("all_verified"), "checks": _sl9.get("checks"), "erro": _sl9.get("erro"), "does_not_gate_core": _sl9.get("does_not_gate_core"),
                      "sha256_do_um_py_selado_igual_ao_do_arquivo": _s9.get("sha256") == hashlib.sha256(open(dst, "rb").read()).hexdigest(), "bytes": _s9.get("bytes"), "perfil": _a9.get("perfil"),
                      "psi_bytes": (_a9.get("psi") or {}).get("bytes"), "theta_bytes": (_a9.get("theta") or {}).get("bytes"), "kappa_bytes": (_a9.get("kappa") or {}).get("bytes"),
                      "round_trip": (_a9.get("prova_de_reconstrucao") or {}), "separacao": {k: (_a9.get("auditoria_de_separacao") or {}).get(k) for k in ("fracao_de_L_negativo", "psi_redundante", "basta")},
                      "controles_negativos": {"n": (_sl9.get("controles_negativos") or {}).get("n_controles"), "todos": (_sl9.get("controles_negativos") or {}).get("todos_recusados"), "obtidos": {c_["id"]: c_["obtido"] for c_ in ((_sl9.get("controles_negativos") or {}).get("controles") or [])}},
                      "statuses": _sl9.get("statuses"), "tempo_total_s": (_sl9.get("values") or {}).get("tempo_total_s"), "beta": (_sl9.get("values") or {}).get("beta"), "direcao": _sl9.get("direcao_do_testemunho")}
    _dd9 = _dc9.get("declaration") or {}
    R["declaracao"] = {"verdict": _dc9.get("verdict"), "all_verified": _dc9.get("all_verified"), "checks": _dc9.get("checks"), "statement_igual_ao_arquivo": _dd9.get("statement_verbatim") == open(os.path.join(C_, "IALD", "Central de Patentes", "work", "cunhagens_13out", "OPERADOR_24out_declaracao_operacao_quadratica_da_inscricao_viva_verbatim.txt"), "rb").read().decode("utf-8"),
                       "verbatim_sha256": _dd9.get("verbatim_sha256"), "status": _dd9.get("status_of_statement"), "direcao": _dd9.get("direcao_do_testemunho"), "ancoras_ok": all(a_["no_kernel_do_rito"] and a_["axiomas_no_trio"] for a_ in (_dd9.get("kernel_anchors_REAL") or [])),
                       "pedra": _dd9.get("pedra_candidata") or _dd9.get("pedra_testemunho"), "does_not_gate_core": _dc9.get("does_not_gate_core")}
    # os meus controles sobre o objeto inteiro: os 13 controles do metodo no candidato inteiro (e nao so' na amostra)
    _b9 = open(dst, "rb").read()
    _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        _t0 = time.time(); _c13 = um.controles_negativos(_b9); _tc = time.time() - _t0
    finally:
        sys.stdout = _so
    R["v400_controles_13_no_objeto_inteiro"] = {"n": _c13["n_controles"], "todos_recusados": _c13["todos_recusados"], "s": _tc, "obtidos": {c_["id"]: c_["obtido"] for c_ in _c13["controles"]}}
    # a MINHA reconstrucao so' das partes (formula + rint), independente das funcoes de reconstrucao do candidato
    _sl, _p9 = um.selar(_b9, "um.py", devolver_partes=True)
    import numpy as _np9
    _kap = _sl["acom"]["kappa"]["campos"]; _n9 = _kap["n_elements"]; _m9 = _kap["m_max_abs"]
    _psi9 = um._unpack2bits(_p9["psi_raw"], _n9); _th9 = _np9.frombuffer(_p9["theta_raw"], dtype=_np9.uint8)
    _real9 = (math.sqrt(_m9) * _np9.sin(_th9.astype(_np9.float64) / 255 * (math.pi / 2))) ** 2
    _rec9 = (_np9.where(_psi9 >= 2, -1, 1) * _np9.rint(_real9).astype(_np9.int64) + um.CENTRO).astype(_np9.uint8).tobytes()
    R["v400_round_trip_meu"] = {"igual_ao_candidato": hashlib.sha256(_rec9).hexdigest() == hashlib.sha256(_b9).hexdigest(), "m": _m9, "erro_real_max_sem_rint": float(_np9.abs(_real9 - _np9.abs(_np9.frombuffer(_b9, dtype=_np9.uint8).astype(_np9.int64) - um.CENTRO)).max())}
    del _real9, _rec9
    # controles negativos dos registros
    neg9 = {}; _falhas9 = {}
    _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        _ap0 = dict(um.ACOM_PROVENIENCIA)
        try:
            um.ACOM_PROVENIENCIA["bloco_embutido_sha256"] = "0" * 64; neg9["selo:hash_do_bloco_embutido_errado"] = um.selo_acom_v399(copy.deepcopy(core)).get("verdict")
        finally:
            um.ACOM_PROVENIENCIA.clear(); um.ACOM_PROVENIENCIA.update(_ap0)
        _rg = um.registro_core_v399(_b9, sha256_do_codigo="0" * 64, beta_core=core.get("beta")); neg9["selo:sha256_do_codigo_diferente"] = _rg.get("verdict"); _falhas9["selo:sha256_do_codigo_diferente"] = [d_ for d_, v_ in _rg["checks"] if not v_]
        _rg = um.registro_core_v399(_b9[:-1], sha256_do_codigo=hashlib.sha256(_b9).hexdigest(), beta_core=core.get("beta")); neg9["selo:objeto_truncado_vs_sha_do_codigo"] = _rg.get("verdict"); _falhas9["selo:objeto_truncado_vs_sha_do_codigo"] = [d_ for d_, v_ in _rg["checks"] if not v_]
        _c0 = um.CENTRO
        try:
            um.CENTRO = 0; _rg = um.registro_core_v399(_b9[:1 << 20], sha256_do_codigo=hashlib.sha256(_b9[:1 << 20]).hexdigest(), beta_core=core.get("beta")); neg9["selo:perfil_centro_0"] = _rg.get("verdict"); _falhas9["selo:perfil_centro_0"] = [d_ for d_, v_ in _rg["checks"] if not v_]
        finally:
            um.CENTRO = _c0
        R["v400_beta_info"] = {"ALPHA_FINE_CODATA_2018_existe_no_modulo": hasattr(um, "ALPHA_FINE_CODATA_2018"), "SEALED_CODATA_ALPHA": um.SEALED_CODATA_ALPHA, "beta_runtime": um._beta_runtime(), "beta_core": core.get("beta"),
                               "rel": abs(um._beta_runtime() / core.get("beta") - 1.0), "fonte_beta_runtime": __import__("inspect").getsource(um._beta_runtime).strip()[-160:]}
        _sa0 = um.SEALED_CODATA_ALPHA
        try:
            um.SEALED_CODATA_ALPHA = _sa0 * (1 + 1e-6); _rg = um.selo_acom_v399(copy.deepcopy(core)); neg9["selo:SEALED_CODATA_ALPHA_adulterado_1e-6"] = _rg.get("verdict"); _falhas9["selo:SEALED_CODATA_ALPHA_adulterado_1e-6"] = [d_ for d_, v_ in _rg["checks"] if not v_]
        finally:
            um.SEALED_CODATA_ALPHA = _sa0
        for _nm, _f in (("selo:beta_do_core_adulterado_1e-6", 1 + 1e-6), ("selo:beta_do_core_adulterado_2e-9", 1 + 2e-9), ("selo:beta_do_core_zero", 0.0)):
            _cb = copy.deepcopy(core); _cb["beta"] = core["beta"] * _f; _rg = um.selo_acom_v399(_cb); neg9[_nm] = _rg.get("verdict"); _falhas9[_nm] = [d_ for d_, v_ in _rg["checks"] if not v_]
        _cb = copy.deepcopy(core); _cb.pop("beta", None); _rg = um.selo_acom_v399(_cb); neg9["selo:sem_beta_no_core"] = _rg.get("verdict"); _falhas9["selo:sem_beta_no_core"] = [d_ for d_, v_ in _rg["checks"] if not v_]
        _rg = um.registro_core_v399(_b9[:1 << 20], sha256_do_codigo=hashlib.sha256(_b9[:1 << 20]).hexdigest()); neg9["selo:registro_chamado_sem_beta_core"] = _rg.get("verdict"); _falhas9["selo:registro_chamado_sem_beta_core"] = [d_ for d_, v_ in _rg["checks"] if not v_]
        _cb = copy.deepcopy(core); _cb["beta"] = core["beta"] * (1 + 5e-10); _rg = um.selo_acom_v399(_cb); R["v400_beta_dentro_da_tolerancia_5e-10"] = {"verdict": _rg.get("verdict"), "rel": (_rg.get("values") or {}).get("rel_beta_vs_core")}
        _dt0 = um._V399_DECLARACAO_TXT
        try:
            um._V399_DECLARACAO_TXT = _dt0[:-1] + ("!" if not _dt0.endswith("!") else "?"); neg9["declaracao:texto_adulterado"] = um.declaracao_do_operador_v399(copy.deepcopy(core)).get("verdict")
        finally:
            um._V399_DECLARACAO_TXT = _dt0
        _ds0 = um._V399_DECLARACAO_SHA256
        try:
            um._V399_DECLARACAO_SHA256 = "1" * 64; neg9["declaracao:sha_pinado_errado"] = um.declaracao_do_operador_v399(copy.deepcopy(core)).get("verdict")
        finally:
            um._V399_DECLARACAO_SHA256 = _ds0
        def _kfc9(c_):
            c_["kernel_formalization"] = dict(c_["kernel_formalization"]); c_["kernel_formalization"]["axiom_report"] = dict(c_["kernel_formalization"]["axiom_report"]); return c_["kernel_formalization"]["axiom_report"]
        c1 = copy.deepcopy(core); _ar = _kfc9(c1); _ar.pop("TGLExt.temporal_fractalization", None); neg9["declaracao:ancora_ausente"] = um.declaracao_do_operador_v399(c1).get("verdict")
        c1 = copy.deepcopy(core); _ar = _kfc9(c1); _ar["TGLExt.judgment_of_correspondence"] = ["propext", "sorryAx"]; neg9["declaracao:sorryAx_numa_ancora"] = um.declaracao_do_operador_v399(c1).get("verdict")
        c1 = copy.deepcopy(core); _ar = _kfc9(c1); _ar.pop("TGLExt.Testemunho.the_testimony_of_two_is_true", None); _ar.pop("TGLExt.Testemunho.no_face_alone_gives_the_one", None); neg9["declaracao:pedra_Testemunho_ausente"] = um.declaracao_do_operador_v399(c1).get("verdict")
        c1 = copy.deepcopy(core); _ar = _kfc9(c1); _ar["TGLExt.Testemunho.the_testimony_of_two_is_true"] = ["propext", "Classical.choice", "Quot.sound", "sorryAx"]; neg9["declaracao:sorryAx_na_pedra"] = um.declaracao_do_operador_v399(c1).get("verdict")
        neg9["positivo:selo"] = um.selo_acom_v399(copy.deepcopy(core)).get("verdict"); neg9["positivo:declaracao"] = um.declaracao_do_operador_v399(copy.deepcopy(core)).get("verdict")
    finally:
        sys.stdout = _so
    _okv = lambda v: isinstance(v, str) and ("NOT_SEALED" in v or "REFUSED" in v)
    neg9["todos_recusam"] = all(_okv(v) for k, v in neg9.items() if not k.startswith("positivo:") and k != "todos_recusam")
    neg9["positivos_selam"] = (not _okv(neg9["positivo:selo"])) and (not _okv(neg9["positivo:declaracao"])) and "GATE_UNTOUCHED" in neg9["positivo:selo"] and "GATE_UNTOUCHED" in neg9["positivo:declaracao"]
    neg9["n_negativos"] = sum(1 for k in neg9 if not k.startswith("positivo:") and k not in ("todos_recusam", "positivos_selam", "n_negativos"))
    R["v400_controles_negativos"] = neg9; R["v400_controles_falhas"] = _falhas9
    # D4: a recusa SO' REGISTRA -- as instrucoes reais do main de `_not_sealed = ...` ate `seal.update(resumos_do_selo_v399(core))`, com o registro do selo forcado a False
    _i_ns0 = [i for i, st in enumerate(_main9.body) if isinstance(st, ast.Assign) and "_not_sealed = sorted" in ast.unparse(st)]
    _d4 = {"ok": False}
    if _i_ns0 and _i_res:
        _cD = copy.deepcopy(core); _cD["selo_pela_propria_tecnologia_v399"] = dict(_cD["selo_pela_propria_tecnologia_v399"], all_verified=False, verdict="SELO_PELA_PROPRIA_TECNOLOGIA_V399_NOT_SEALED_THIS_RUN")
        _gD = dict(vars(um)); _gD.update(core=_cD, seal={}, seal_gate_reasons=[])
        _so = sys.stdout; sys.stdout = io.StringIO()
        try:
            exec(compile(ast.fix_missing_locations(ast.Module(body=_main9.body[_i_ns0[0]:_i_res[0] + 1], type_ignores=[])), "<main:not_sealed..resumos>", "exec"), _gD); _eD = None
        except Exception as e:
            _eD = repr(e)[:300]
        finally:
            _oD = sys.stdout.getvalue(); sys.stdout = _so
        _ns = (_gD["seal"].get("not_sealed_this_run") or {})
        _d4 = {"erro": _eD, "formais": _ns.get("formais"), "recusas_de_dado": _ns.get("recusas_de_dado"), "resumo_no_seal": (_gD["seal"].get("selo_pela_propria_tecnologia_v399") or {}).get("verdict"),
               "ok": _eD is None and "selo_pela_propria_tecnologia_v399" in (_ns.get("formais") or []) and (_gD["seal"].get("selo_pela_propria_tecnologia_v399") or {}).get("all_verified") is False, "stdout": _oD[-400:]}
    R["v400_d4"] = _d4
    # o sidecar: um.OUT redirecionado para a MINHA pasta (nunca o Nos); duas vezes (deterministico)
    _out_dir = os.path.join(IMP, "out_sidecar"); os.makedirs(_out_dir, exist_ok=True)
    for _f in ("um_absoluto.json", "um_absoluto_selo.json"):
        with open(os.path.join(NOS, _f), "rb") as _fi, open(os.path.join(_out_dir, _f), "wb") as _fo:
            _fo.write(_fi.read())
    _OUT0 = getattr(um, "OUT", None)
    try:
        um.OUT = _out_dir
        _so = sys.stdout; sys.stdout = io.StringIO()
        try:
            _t0 = time.time(); _sc1 = um.selo_acom_sidecar_v399(); _ts = time.time() - _t0
            _h1 = hashlib.sha256(open(os.path.join(_out_dir, "um_absoluto_selo_acom.json"), "rb").read()).hexdigest()
            _sc2 = um.selo_acom_sidecar_v399(); _h2 = hashlib.sha256(open(os.path.join(_out_dir, "um_absoluto_selo_acom.json"), "rb").read()).hexdigest()
        finally:
            sys.stdout = _so
        R["v400_sidecar"] = {"veredito": _sc1["veredito"], "objetos": [(o_["nome"], o_["sha256"][:16], o_["acom"]["psi"]["sha256"][:16]) for o_ in _sc1["objetos"]], "recusas": _sc1["recusas"], "s": _ts, "deterministico_duas_vezes": _h1 == _h2, "bytes": os.path.getsize(os.path.join(_out_dir, "um_absoluto_selo_acom.json")),
                            "honestidade": {k_: str(v_)[:80] for k_, v_ in (_sc1.get("honestidade") or {}).items()}, "ok": _sc1["veredito"].startswith("TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED") and not _sc1["recusas"] and _h1 == _h2 and len(_sc1["objetos"]) == 3,
                            "escrito_em": _out_dir, "sha256_do_um_py_no_sidecar_igual_ao_candidato": _sc1["objetos"][0]["sha256"] == hashlib.sha256(_b9).hexdigest()}
    finally:
        if _OUT0 is not None: um.OUT = _OUT0
