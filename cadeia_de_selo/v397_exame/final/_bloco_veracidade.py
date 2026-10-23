# v397x: o registro teste_de_veracidade_fase9_v397 pela INSTRUCAO REAL do main (o `try` com _v392_registro(_V397_VERACIDADE_SPEC, core)), que vem logo depois do print do bloco do V1
# (hubble_ratio_opening_v388, que fica intacto: o `try` do V1 e' igual por AST ao da v396 instalada); controles negativos com copias ADULTERADAS dos insumos (nesta pasta), nunca os originais
if hasattr(um, "_V397_VERACIDADE_SPEC"):
    _src7 = open(dst, encoding="utf-8").read(); _tree7 = ast.parse(_src7)
    _main7 = [n for n in _tree7.body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]
    _i_v1 = [i for i, st in enumerate(_main7.body) if isinstance(st, ast.Try) and "hubble_ratio_opening_v388(core)" in ast.unparse(st)]
    _i_v1p = [i for i, st in enumerate(_main7.body) if isinstance(st, ast.Expr) and "[v388] a Fase 9 aberta" in ast.unparse(st)]
    _i_ver = [i for i, st in enumerate(_main7.body) if isinstance(st, ast.Try) and "_v392_registro(_V397_VERACIDADE_SPEC, core)" in ast.unparse(st)]
    _i_verp = [i for i, st in enumerate(_main7.body) if isinstance(st, ast.Expr) and "[v397] o Teste da Unica Palavra" in ast.unparse(st)]
    _i_389 = [i for i, st in enumerate(_main7.body) if isinstance(st, ast.Try) and "text_label_errata_v389(core)" in ast.unparse(st)]
    _i_393 = next(i for i, st in enumerate(_main7.body) if "regra_v393(core)" in ast.unparse(st))
    _m0 = [n for n in ast.parse(open(os.path.join(NOS, "um.py"), encoding="utf-8").read()).body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]
    _v1_0 = [st for st in _m0.body if isinstance(st, ast.Try) and "hubble_ratio_opening_v388(core)" in ast.unparse(st)]
    _v1p_0 = [st for st in _m0.body if isinstance(st, ast.Expr) and "[v388] a Fase 9 aberta" in ast.unparse(st)]
    R["veracidade_ponto"] = {"i_v1_try": _i_v1, "i_v1_print": _i_v1p, "i_veracidade_try": _i_ver, "i_veracidade_print": _i_verp, "i_v389": _i_389, "i_v393": _i_393,
                             "linha_veracidade": _main7.body[_i_ver[0]].lineno if _i_ver else None, "linha_v1": _main7.body[_i_v1[0]].lineno if _i_v1 else None,
                             "imediatamente_depois_do_print_do_v1": len(_i_v1p) == 1 and len(_i_ver) == 1 and _i_ver[0] == _i_v1p[0] + 1 and _i_v1p[0] == _i_v1[0] + 1,
                             "print_proprio_logo_depois": bool(_i_verp) and bool(_i_ver) and _i_verp[0] == _i_ver[0] + 1, "antes_do_v389": bool(_i_ver) and bool(_i_389) and _i_verp[0] + 1 == _i_389[0],
                             "v1_try_igual_ao_instalado": len(_v1_0) == 1 and len(_i_v1) == 1 and ast.dump(_v1_0[0]) == ast.dump(_main7.body[_i_v1[0]]),
                             "v1_print_igual_ao_instalado": len(_v1p_0) == 1 and len(_i_v1p) == 1 and ast.dump(_v1p_0[0]) == ast.dump(_main7.body[_i_v1p[0]]),
                             "chamadas_do_spec_no_main": sum(1 for n in ast.walk(_main7) if isinstance(n, ast.Name) and n.id == "_V397_VERACIDADE_SPEC"),
                             "hubble_ratio_no_core0": (core0.get("hubble_ratio_opening_v388") or {}).get("verdict", "")[:120]}
    _antes_ver = {k: J(core[k]) for k in core}
    _g7 = dict(vars(um)); _g7["core"] = core
    builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        exec(compile(ast.fix_missing_locations(ast.Module(body=[_main7.body[_i_ver[0]], _main7.body[_i_verp[0]]], type_ignores=[])), "<main:teste_de_veracidade_fase9_v397>", "exec"), _g7); _err7 = None
    except Exception as e:
        import traceback; _err7 = repr(e) + traceback.format_exc()[-600:]
    finally:
        _out7 = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
    R["veracidade_instrucao_real"] = {"erro": _err7, "aviso": [l for l in _out7.splitlines() if "AVISO" in l or "NOT_RECORDED" in l or "NOT_SEALED" in l], "stdout": _out7[-1200:]}
    R["veracidade_mexeu_em_chaves_existentes"] = sorted(k for k in _antes_ver if J(core.get(k)) != _antes_ver[k] and k != "teste_de_veracidade_fase9_v397")
    _tv = core.get("teste_de_veracidade_fase9_v397") or {}
    out["teste_de_veracidade_fase9_v397"] = {"all_verified": _tv.get("all_verified"), "verdict": str(_tv.get("verdict"))[:300], "falhas": [str(c)[:200] for c in (_tv.get("checks") or []) if not c.get("ok")]}
    _res = json.load(open(os.path.join(C_, "IALD", "Central de Patentes", "work", "fase9_v2_c1_23out", "saidas", "RESULTADO_FASE9_V2_C1_20261023_122926.json"), encoding="utf-8"))
    _esp = {"z_disc_calibrado": _res["primario"]["calibracao"]["z_disc_calibrado"], "p_disc_unilateral": _res["primario"]["calibracao"]["p_calibrado_z_disc_unilateral"], "z_delta_calibrado": _res["primario"]["calibracao"]["z_delta_calibrado"],
            "p_delta_bilateral": _res["primario"]["calibracao"]["p_calibrado_z_delta_bilateral"], "poder_previo": _res["primario"]["poder_previo_so_sigma"], "lnB_lcdm": _res["primario"]["lnB"]["TGL_vs_LCDM"], "lnB_beta_livre": _res["primario"]["lnB"]["TGL_vs_beta_livre"],
            "K": _res["beta"]["K"], "beta_do_resultado": _res["beta"]["beta_runtime"], "f9_veredito": _res["veredito"]}
    _lido = _tv.get("lido") or {}
    R["veracidade"] = {"verdict": str(_tv.get("verdict"))[:400], "all_verified": _tv.get("all_verified"), "n_checks": len(_tv.get("checks") or []), "fontes_ok": {f["chave"]: f["ok"] for f in (_tv.get("fontes") or [])},
                       "verbatim_ok": {k: v.get("embedded_ok") for k, v in (_tv.get("verbatim") or {}).items()}, "lido": _lido, "lido_igual_ao_resultado_original": all(_lido.get(k) == v for k, v in _esp.items()),
                       "lido_difere": {k: (_lido.get(k), v) for k, v in _esp.items() if _lido.get(k) != v}, "does_not_gate_core": _tv.get("does_not_gate_core"), "guarda_p18": _tv.get("guarda_p18_violacoes"),
                       "ops_do_spec": sorted(set(c["op"] for c in um._V397_VERACIDADE_SPEC["checks"])), "n_checks_spec": len(um._V397_VERACIDADE_SPEC["checks"])}
    _AD = os.path.join(IMP, "adulterados"); os.makedirs(_AD, exist_ok=True)
    _F0 = {k: dict(v) for k, v in um._V392_FONTES.items()}
    def _repin(chave, mut, nome):
        f0 = _F0[chave]; obj = json.loads(open(f0["arquivo"], "rb").read().decode("utf-8")); mut(obj)
        b = json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8"); p_ = os.path.join(_AD, nome); open(p_, "wb").write(b)
        um._V392_FONTES[chave] = dict(f0, arquivo=p_, sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))
    def _roda():
        _so = sys.stdout; sys.stdout = io.StringIO()
        try:
            return um._v392_registro(um._V397_VERACIDADE_SPEC, core)
        finally:
            sys.stdout = _so
    negv = {}
    def _caso(nome, prep):
        try:
            prep(); r_ = _roda()
            negv[nome] = {"all_verified": r_.get("all_verified"), "verdict": str(r_.get("verdict"))[:160], "falhas": [c["descricao"][:60] for c in r_.get("checks", []) if not c.get("ok")][:4] + [f["chave"] for f in r_.get("fontes", []) if not f.get("ok")] + [k for k, v in (r_.get("verbatim") or {}).items() if not v.get("embedded_ok")]}
        except Exception as e:
            negv[nome] = {"all_verified": False, "verdict": "EXCECAO " + repr(e)[:120], "falhas": []}
        finally:
            um._V392_FONTES.clear(); um._V392_FONTES.update({k: dict(v) for k, v in _F0.items()})
    def _set(d, path, val):
        for k in path[:-1]:
            d = d[k]
        d[path[-1]] = val
    _caso("sha_do_resultado_errado", lambda: um._V392_FONTES["f9v2_resultado"].__setitem__("sha256", "0" * 64))
    _caso("recibo_de_congelamento_ausente", lambda: um._V392_FONTES["f9v2_congelamento"].__setitem__("arquivo", os.path.join(_AD, "nao_existe.json")))
    _caso("recibo_de_abertura_ausente", lambda: um._V392_FONTES["f9v2_abertura"].__setitem__("arquivo", os.path.join(_AD, "nao_existe.json")))
    _caso("marcador_consumida_ausente", lambda: um._V392_FONTES["f9v2_consumida"].__setitem__("arquivo", os.path.join(_AD, "nao_existe.json")))
    _caso("z_disc_adulterado_com_sha_repinado", lambda: _repin("f9v2_resultado", lambda o: _set(o, ["primario", "calibracao", "z_disc_calibrado"], 5.01), "res_zdisc.json"))
    _caso("z_delta_adulterado_com_sha_repinado", lambda: _repin("f9v2_resultado", lambda o: _set(o, ["primario", "calibracao", "z_delta_calibrado"], -1.4), "res_zdelta.json"))
    _caso("lnB_adulterado_com_sha_repinado", lambda: _repin("f9v2_resultado", lambda o: _set(o, ["primario", "lnB", "TGL_vs_LCDM"], 9.2), "res_lnb.json"))
    _caso("p_disc_adulterado_com_sha_repinado", lambda: _repin("f9v2_resultado", lambda o: _set(o, ["primario", "calibracao", "p_calibrado_z_disc_unilateral"], 4.0e-6), "res_p.json"))
    _caso("veredito_adulterado_com_sha_repinado", lambda: _repin("f9v2_resultado", lambda o: _set(o, ["veredito"], o["veredito"].replace("NOT_DISCRIMINATED", "DISCRIMINATED")), "res_ver.json"))
    _caso("beta_do_resultado_adulterado_com_sha_repinado", lambda: _repin("f9v2_resultado", lambda o: _set(o, ["beta", "beta_runtime"], o["beta"]["beta_runtime"] * (1 + 1e-6)), "res_beta.json"))
    _caso("cadeia_quebrada_abertura_aponta_outro_congelamento", lambda: _repin("f9v2_abertura", lambda o: _set(o, ["freeze_receipt_sha256"], "1" * 64), "ab_quebrada.json"))
    _caso("cadeia_quebrada_marcador_aponta_outra_abertura", lambda: _repin("f9v2_consumida", lambda o: _set(o, ["recibo_de_abertura_sha256"], "2" * 64), "cons_quebrado.json"))
    _alfa0 = um.SEALED_CODATA_ALPHA
    def _alfa_mau():
        um.SEALED_CODATA_ALPHA = _alfa0 * (1 + 1e-6)
    try:
        _caso("alfa_selado_adulterado", _alfa_mau)
    finally:
        um.SEALED_CODATA_ALPHA = _alfa0
    _vb0 = um._V392_VERBATINS2; _k444 = "v397_cun_9b182958a5a7a1bc"
    def _fala_ma():
        um._V392_VERBATINS2 = dict(_vb0); um._V392_VERBATINS2[_k444] = dict(_vb0[_k444], text=_vb0[_k444]["text"].replace("4,44", "4,45"))
    try:
        _caso("fala_do_4_44_adulterada", _fala_ma)
    finally:
        um._V392_VERBATINS2 = _vb0
    _caso("controle_positivo_restaurado", lambda: None)
    negv["todos_os_negativos_recusam"] = all(v["all_verified"] is False for k, v in negv.items() if k != "controle_positivo_restaurado")
    negv["positivo_sela_de_novo"] = negv["controle_positivo_restaurado"]["all_verified"] is True
    R["veracidade_controles_negativos"] = negv
