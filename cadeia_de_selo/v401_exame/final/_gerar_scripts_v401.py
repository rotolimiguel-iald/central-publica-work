# -*- coding: utf-8 -*-
"""_gerar_scripts_v401.py -- gera, dos MEUS scripts dos exames v399/v400, os do exame v401 (substituicoes com contagem exata):
comparar_v400_v401_exame.py (do comparar_v398_v399_exame.py), simular_arvore_do_nos_v401x.py e exame_pontos_v401x.py (dos v400x; + o `try` real do
falsidade_da_inercia_v401 logo depois da declaracao, executado com os outros dois, os controles negativos dele e o main igual ao instalado SEM o try novo)."""
import ast, os
F9 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v399_exame\final"
F10 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v400_exame\final"
F11 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v401_exame\final"


def sub(s, rep):
    for a, b, n in rep:
        assert s.count(a) == n, (a[:110], s.count(a), n)
        s = s.replace(a, b)
    return s


# ---------------- comparar
s = open(os.path.join(F9, "comparar_v398_v399_exame.py"), encoding="utf-8").read()
s = sub(s, [
    ('"""comparar_v398_v399_exame.py -- exame final v399 (c1, modelo forte, 24/10/2026): comparacao ESTRUTURAL (AST/literal_eval) entre a v398\ninstalada (A = Nos) e o candidato v399 (B). Molde: comparar_v397_v398_exame.py.',
     '"""comparar_v400_v401_exame.py -- exame final v401 (c1, modelo forte, 25/10/2026): comparacao ESTRUTURAL (AST/literal_eval) entre a v400\ninstalada (A = Nos) e o candidato v401 (B). Molde: comparar_v398_v399_exame.py.', 1),
    ('if not v.startswith("TGLExt.Testemunho.")),', 'if not v.startswith("TGLExt.FalsidadeDaInercia.")),', 1),
    ('"acrescentadas_por_pedra": {"Testemunho": sum(1 for v in add.values() if v.startswith("TGLExt.Testemunho."))},',
     '"acrescentadas_por_pedra": {"FalsidadeDaInercia": sum(1 for v in add.values() if v.startswith("TGLExt.FalsidadeDaInercia."))},', 1),
    ('for nm in ("_V392_SPECS", "_V393_SPECS", "_V394_SPECS", "_V395_SPECS", "_V396_SPECS", "_V397_SPECS", "_V398_SPECS"):',
     'for nm in ("_V392_SPECS", "_V393_SPECS", "_V394_SPECS", "_V395_SPECS", "_V396_SPECS", "_V397_SPECS", "_V398_SPECS", "_V399_SPECS"):', 1),
    ('sp6 = {s["nome"]: s for s in lit(dB, "_V399_SPECS")}\nR["v399_specs"]', 'sp6 = {s["nome"]: s for s in lit(dB, "_V401_SPECS")}\nR["v401_specs"]', 1),
    ('kh6 = sp6.get("kh_n1_cobertura_v399") or {}', 'kh6 = sp6.get("kh_n1_cobertura_v401") or {}', 1),
    ('R["h8_v399"] =', 'R["h8_v401"] =', 1),
    ('for k in ("TGLExt/Testemunho.lean",)}', 'for k in ("TGLExt/FalsidadeDaInercia.lean",)}', 1),
    ('"_V395_PSIBIT_CONTRACT", "_V398_SPECS", "_V396_TESTEMUNHA_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V398_SONICO_CONTRACT", "_unified_main", "build_en", "build_pt", "emit_canonical_md", "main", "prove_external_ladder"}',
     '"_V395_PSIBIT_CONTRACT", "_V399_SPECS", "_V396_TESTEMUNHA_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V398_SONICO_CONTRACT", "build_en", "build_pt", "emit_canonical_md", "main", "prove_external_ladder"}', 1),
    ('"_V396_FONTES", "_V397_FONTES", "_V398_FONTES", "_V399_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", "_V394_VERBATINS2", "_V395_VERBATINS2", "_V396_VERBATINS2", "_V397_VERBATINS2", "_V398_VERBATINS2", "_V399_VERBATINS2")}',
     '"_V396_FONTES", "_V397_FONTES", "_V398_FONTES", "_V399_FONTES", "_V401_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", "_V394_VERBATINS2", "_V395_VERBATINS2", "_V396_VERBATINS2", "_V397_VERBATINS2", "_V398_VERBATINS2", "_V399_VERBATINS2", "_V401_VERBATINS2")}', 1),
    ('R["colisoes_v399"] = {"fontes": sorted(FB["_V399_FONTES"] & (FB["_V392_FONTES"] | FB["_V393_FONTES"] | FB["_V394_FONTES"] | FB["_V395_FONTES"] | FB["_V396_FONTES"] | FB["_V397_FONTES"] | FB["_V398_FONTES"])),\n                      "falas": sorted(FB["_V399_VERBATINS2"] & (FB["_V392_VERBATINS2"] | FB["_V393_VERBATINS2"] | FB["_V394_VERBATINS2"] | FB["_V395_VERBATINS2"] | FB["_V396_VERBATINS2"] | FB["_V397_VERBATINS2"] | FB["_V398_VERBATINS2"]))}',
     'R["colisoes_v401"] = {"fontes": sorted(FB["_V401_FONTES"] & (FB["_V392_FONTES"] | FB["_V393_FONTES"] | FB["_V394_FONTES"] | FB["_V395_FONTES"] | FB["_V396_FONTES"] | FB["_V397_FONTES"] | FB["_V398_FONTES"] | FB["_V399_FONTES"])),\n                      "falas": sorted(FB["_V401_VERBATINS2"] & (FB["_V392_VERBATINS2"] | FB["_V393_VERBATINS2"] | FB["_V394_VERBATINS2"] | FB["_V395_VERBATINS2"] | FB["_V396_VERBATINS2"] | FB["_V397_VERBATINS2"] | FB["_V398_VERBATINS2"] | FB["_V399_VERBATINS2"]))}', 1),
    ('"sonico_v398", "afinacao_das_cordas_v398", "v398_sonico_mechanics", "v398_afinacao_mechanics", "_v398_formal", "_v398_beta", "_v398_h2", "_v398_bernoulli", "_v398_bernoulli_poly", "_v398_rodar_specs"):',
     '"sonico_v398", "afinacao_das_cordas_v398", "v398_sonico_mechanics", "v398_afinacao_mechanics", "_v398_formal", "_v398_beta", "_v398_h2", "_v398_bernoulli", "_v398_bernoulli_poly", "_v398_rodar_specs",\n          "selo_acom_v399", "declaracao_do_operador_v399", "registro_core_v399", "_beta_runtime", "_theta_m_runtime", "selar", "controles_negativos", "conferir_bloco_embutido", "resumos_do_selo_v399", "selo_acom_sidecar_v399", "sidecar", "_v399_rodar_specs", "_v376_same_alpha_literal"):', 1),
    ('for f in ("_V397_VERACIDADE_SPEC", "_V397_FONTES", "_V397_VERBATINS2", "_V397_FRASE_444", "_V397_CHAVES_NUM", "_V396_SPECS", "_V395_SPECS", "_V394_SPECS", "_V393_SPECS", "_V392_SPECS", "_V392_FONTES", "_V392_VERBATINS2", "_V398_VERBATINS2", "_V398_FONTES", "_V398_SONICO_TEXT", "_V398_AFINACAO_TEXT", "_V397_SPECS"):',
     'for f in ("_V397_VERACIDADE_SPEC", "_V397_FONTES", "_V397_VERBATINS2", "_V397_FRASE_444", "_V397_CHAVES_NUM", "_V396_SPECS", "_V395_SPECS", "_V394_SPECS", "_V393_SPECS", "_V392_SPECS", "_V392_FONTES", "_V392_VERBATINS2", "_V398_VERBATINS2", "_V398_FONTES", "_V398_SONICO_TEXT", "_V398_AFINACAO_TEXT", "_V397_SPECS", "_V398_SPECS", "_V399_FONTES", "_V399_VERBATINS2", "_V399_DECLARACAO_TXT", "_V399_DECLARACAO_SHA256", "ACOM_PROVENIENCIA", "PERFIL_ID", "CENTRO"):', 1),
])
ast.parse(s); open(os.path.join(F11, "comparar_v400_v401_exame.py"), "w", encoding="utf-8").write(s)
# ---------------- simular
s = open(os.path.join(F10, "simular_arvore_do_nos_v400x.py"), encoding="utf-8").read()
s = sub(s, [
    ('V = os.path.join(os.path.dirname(os.path.dirname(H)), "v400")   # v400x: a pasta da cadeia v400', 'V = os.path.join(os.path.dirname(os.path.dirname(H)), "v401")   # v401x: a pasta da cadeia v401', 1),
    ('default=os.path.join(V, "um_v400_candidato.py")', 'default=os.path.join(V, "um_v401_candidato.py")', 1),
    ("(um.declaracao_do_operador_v399(core) if hasattr(um, 'declaracao_do_operador_v399') else None)\n",
     "(um.declaracao_do_operador_v399(core) if hasattr(um, 'declaracao_do_operador_v399') else None)\n(um.falsidade_da_inercia_v401(core) if hasattr(um, 'falsidade_da_inercia_v401') else None)\n", 1),
    ("(um._v399_rodar_specs(core) if hasattr(um, '_v399_rodar_specs') else None)", "(um._v399_rodar_specs(core) if hasattr(um, '_v399_rodar_specs') else None)\n(um._v401_rodar_specs(core) if hasattr(um, '_v401_rodar_specs') else None)", 1),
    ('"selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399"):',
     '"selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401"):', 1),
    ('um._V399_SPECS if s_["nome"] == "kh_n1_cobertura_v399"', 'um._V401_SPECS if s_["nome"] == "kh_n1_cobertura_v401"', 2),
    ('"h8_pino_kh_n1_v399_n"', '"h8_pino_kh_n1_v401_n"', 1),
])
s = s.replace('"""simular_arvore_do_nos_v400x.py -- exame final v400', '"""simular_arvore_do_nos_v401x.py -- exame final v401 (+ falsidade_da_inercia_v401 e os specs v401). Texto do molde: exame final v400', 1)
ast.parse(s); open(os.path.join(F11, "simular_arvore_do_nos_v401x.py"), "w", encoding="utf-8").write(s)
# ---------------- exame_pontos
s = open(os.path.join(F10, "exame_pontos_v400x.py"), encoding="utf-8").read()
n_r = s.count('R["v400_'); assert n_r >= 9
s = s.replace('R["v400_', 'R["v401_').replace('falsos.append("v400_', 'falsos.append("v401_').replace('if "v400_', 'if "v401_').replace('R.get("v400_', 'R.get("v401_')
s = sub(s, [
    ('ap.add_argument("--sandbox", default=os.path.join(C_, "t", "k400c", "final"))', 'ap.add_argument("--sandbox", default=os.path.join(C_, "t", "k401c", "final"))', 1),
    ('    _i_dec = [i for i, st in enumerate(_main9.body) if isinstance(st, ast.Try) and "declaracao_do_operador_v399(core)" in ast.unparse(st)]\n',
     '    _i_dec = [i for i, st in enumerate(_main9.body) if isinstance(st, ast.Try) and "declaracao_do_operador_v399(core)" in ast.unparse(st)]\n'
     '    _i_fal = [i for i, st in enumerate(_main9.body) if isinstance(st, ast.Try) and "falsidade_da_inercia_v401(core)" in ast.unparse(st)]\n', 1),
    ('                       "main_igual_ao_instalado_v399": ast.dump(_m0_9) == ast.dump(_main9), "unified_main_igual_ao_instalado_v399": ast.dump(_um0_9) == ast.dump(_um9),\n',
     '                       "falsidade_imediatamente_depois_da_declaracao": len(_i_fal) == 1 and len(_i_dec) == 1 and _i_fal[0] == _i_dec[0] + 1, "falsidade_antes_do_bloco_v393": bool(_i_fal) and _i_fal[0] < _i_393_9,\n'
     '                       "linha_falsidade": _main9.body[_i_fal[0]].lineno if _i_fal else None, "chamadas_falsidade_no_main": sum(1 for n in ast.walk(_main9) if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "falsidade_da_inercia_v401"),\n'
     '                       "main_igual_ao_instalado_sem_o_try_novo": [ast.dump(st) for i, st in enumerate(_main9.body) if i not in _i_fal] == [ast.dump(st) for st in _m0_9.body] and ast.dump(_main9.args) == ast.dump(_m0_9.args),\n'
     '                       "unified_main_igual_ao_instalado_v400": ast.dump(_um0_9) == ast.dump(_um9),\n', 1),
    ('body=[_main9.body[_i_sel[0]], _main9.body[_i_dec[0]]]', 'body=[_main9.body[_i_sel[0]], _main9.body[_i_dec[0]], _main9.body[_i_fal[0]]]', 1),
    ('k not in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399")', 'k not in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "falsidade_da_inercia_v401")', 1),
    ('    out["declaracao_do_operador_v399"] = {"all_verified": _dc9.get("all_verified"), "verdict": str(_dc9.get("verdict"))[:200], "falhas": [d_ for d_, v_ in (_dc9.get("checks") or []) if not v_]}\n',
     '    out["declaracao_do_operador_v399"] = {"all_verified": _dc9.get("all_verified"), "verdict": str(_dc9.get("verdict"))[:200], "falhas": [d_ for d_, v_ in (_dc9.get("checks") or []) if not v_]}\n'
     '    _fl9 = core.get("falsidade_da_inercia_v401") or {}\n'
     '    out["falsidade_da_inercia_v401"] = {"all_verified": _fl9.get("all_verified"), "verdict": str(_fl9.get("verdict"))[:260], "falhas": [c_.get("id") or c_.get("nome") or str(c_)[:80] for c_ in ((_fl9.get("mechanics") or {}).get("checks") or []) if isinstance(c_, dict) and c_.get("ok") is False]}\n'
     '    R["falsidade"] = {k_: _fl9.get(k_) for k_ in ("verdict", "all_verified", "estatuto", "exact_ladder", "formal_theorems", "support_theorems", "embedded_source_ok", "inscriptions", "beta_ok", "beta_core_rel_diff", "unconditional", "key_theorem", "costless", "runtime_executed", "mechanics", "values", "named_hypothesis", "chain_status", "does_not_gate_core", "guarda_p18_violacoes")}\n', 1),
    ('        neg9["positivo:selo"] = um.selo_acom_v399(copy.deepcopy(core)).get("verdict"); neg9["positivo:declaracao"] =',
     '        _KT = "TGLExt.FalsidadeDaInercia.the_inertia_of_a_post_is_false"\n'
     '        c1 = copy.deepcopy(core); _ar = _kfc9(c1)\n'
     '        for _k in [k_ for k_ in list(_ar) if k_.startswith("TGLExt.FalsidadeDaInercia.")]: _ar.pop(_k, None)\n'
     '        neg9["falsidade:pedra_ausente_do_axiom_report"] = um.falsidade_da_inercia_v401(c1).get("verdict")\n'
     '        c1 = copy.deepcopy(core); _ar = _kfc9(c1); _ar[_KT] = ["propext", "Classical.choice", "Quot.sound", "sorryAx"]; neg9["falsidade:sorryAx_na_estrela"] = um.falsidade_da_inercia_v401(c1).get("verdict")\n'
     '        c1 = copy.deepcopy(core); c1["kernel_formalization"] = dict(c1["kernel_formalization"]); c1["kernel_formalization"]["ext_fdi401_0001"] = False; neg9["falsidade:bandeira_da_pedra_False"] = um.falsidade_da_inercia_v401(c1).get("verdict")\n'
     '        c1 = copy.deepcopy(core); c1["beta"] = core["beta"] * (1 + 1e-6); neg9["falsidade:beta_do_core_adulterado_1e-6"] = um.falsidade_da_inercia_v401(c1).get("verdict")\n'
     '        _vb0 = um._V401_VERBATINS2; _k0 = sorted(_vb0)[0]; _t0 = _vb0[_k0]["text"]\n'
     '        try:\n'
     '            _vb0[_k0]["text"] = _t0 + "."; neg9["falsidade:inscricao_adulterada"] = um.falsidade_da_inercia_v401(copy.deepcopy(core)).get("verdict")\n'
     '        finally:\n'
     '            _vb0[_k0]["text"] = _t0\n'
     '        neg9["positivo:falsidade"] = um.falsidade_da_inercia_v401(copy.deepcopy(core)).get("verdict")\n'
     '        neg9["positivo:selo"] = um.selo_acom_v399(copy.deepcopy(core)).get("verdict"); neg9["positivo:declaracao"] =', 1),
    ('    neg9["positivos_selam"] = (not _okv(neg9["positivo:selo"])) and (not _okv(neg9["positivo:declaracao"])) and "GAT',
     '    neg9["positivos_selam"] = (not _okv(neg9["positivo:falsidade"])) and "GATE_UNMOVED" in neg9["positivo:falsidade"] and (not _okv(neg9["positivo:selo"])) and (not _okv(neg9["positivo:declaracao"])) and "GAT', 1),
    ('if "selo_acom" in R and not (R["selo_acom"].get("all_verified") is True and R["declaracao"].get("all_verified") is True): falsos.append("v401_registros")',
     'if "selo_acom" in R and not (R["selo_acom"].get("all_verified") is True and R["declaracao"].get("all_verified") is True and (R.get("falsidade") or {}).get("all_verified") is True): falsos.append("v401_registros")', 1),
    ('"try_selo_igual_ao_instalado_v399", "try_declaracao_igual_ao_instalado_v399", "try_sidecar_igual_ao_instalado_v399", "main_igual_ao_instalado_v399", "unified_main_igual_ao_instalado_v399", "sidecar_no_unified_main_depois_da_ultima_escrita_do_selo")): falsos.append("v401_ponto")',
     '"try_selo_igual_ao_instalado_v399", "try_declaracao_igual_ao_instalado_v399", "try_sidecar_igual_ao_instalado_v399", "falsidade_imediatamente_depois_da_declaracao", "falsidade_antes_do_bloco_v393", "main_igual_ao_instalado_sem_o_try_novo", "unified_main_igual_ao_instalado_v400", "sidecar_no_unified_main_depois_da_ultima_escrita_do_selo")): falsos.append("v401_ponto")', 1),
])
# a palavra "REFUSED" do veredito de recusa da falsidade: _okv ja' aceita REFUSED
assert '"REFUSED" in v' in s
s = s.replace('"""exame_pontos_v400x.py -- exame final v400', '"""exame_pontos_v401x.py -- exame final v401 (c1, 25/10/2026; molde: exame_pontos_v400x.py + o try real da falsidade). Texto do molde: exame final v400', 1)
ast.parse(s); open(os.path.join(F11, "exame_pontos_v401x.py"), "w", encoding="utf-8").write(s)
print("ok", n_r)
