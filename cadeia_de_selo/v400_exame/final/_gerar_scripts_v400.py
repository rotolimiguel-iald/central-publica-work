# -*- coding: utf-8 -*-
"""_gerar_scripts_v400.py -- gera, a partir dos MEUS scripts dos exames v398/v399, os do exame v400 (substituicoes conferidas: count exato):
 _bloco_v400.py (do _bloco_v399.py: chaves R["v400_*"]; + os `try` do selo, da declaracao e do sidecar iguais por AST aos da v399 INSTALADA; os controles do registro com
 beta_core passado -- para recusarem pela razao deles --, a falha de cada um, e os controles NOVOS da checagem do beta: SEALED_CODATA_ALPHA adulterado, beta do core
 adulterado a 1e-6 e a 2e-9, beta do core ausente/zero; e o positivo a 5e-10), exame_pontos_v400x.py (do exame_pontos_v398x.py + _bloco_v400.py) e
 simular_arvore_do_nos_v400x.py (do simular_arvore_do_nos_v399x.py)."""
import os, ast, shutil
F8 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v398_exame\final"
F9 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v399_exame\final"
F10 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v400_exame\final"


def sub(src, rep):
    for a, b, n in rep:
        assert src.count(a) == n, (a[:120], src.count(a), n)
        src = src.replace(a, b)
    return src


# ---------------- o bloco
b = open(os.path.join(F9, "_bloco_v399.py"), encoding="utf-8").read()
n_r = b.count('R["v399_')
b = b.replace('R["v399_', 'R["v400_')
b = sub(b, [
    ("# v399x: o SELO PELA PROPRIA TECNOLOGIA e a DECLARACAO DO OPERADOR pelas INSTRUCOES REAIS do main",
     "# v400x (do v399x; a v400 e' a CORRECAO: alfa nao redeclarado, beta do registro contra o core): o SELO PELA PROPRIA TECNOLOGIA e a DECLARACAO DO OPERADOR pelas INSTRUCOES REAIS do main", 1),
    # os try iguais por AST aos da v399 INSTALADA (o main nao muda na v400)
    ('    _afi0 = [st for st in _m0_9.body if isinstance(st, ast.Try) and "afinacao_das_cordas_v398(core)" in ast.unparse(st)]\n',
     '    _afi0 = [st for st in _m0_9.body if isinstance(st, ast.Try) and "afinacao_das_cordas_v398(core)" in ast.unparse(st)]\n'
     '    _sel0 = [st for st in _m0_9.body if isinstance(st, ast.Try) and "selo_acom_v399(core)" in ast.unparse(st)]\n'
     '    _dec0 = [st for st in _m0_9.body if isinstance(st, ast.Try) and "declaracao_do_operador_v399(core)" in ast.unparse(st)]\n'
     '    _um0_9 = [n for n in ast.parse(open(os.path.join(NOS, "um.py"), encoding="utf-8").read()).body if isinstance(n, ast.FunctionDef) and n.name == "_unified_main"][-1]\n'
     '    _sc0 = [st for st in _um0_9.body if isinstance(st, ast.Try) and "selo_acom_sidecar_v399()" in ast.unparse(st)]\n', 1),
    ('                       "try_afinacao_igual_ao_instalado": len(_afi0) == 1 and len(_i_afi9) == 1 and ast.dump(_afi0[0]) == ast.dump(_main9.body[_i_afi9[0]]),\n',
     '                       "try_afinacao_igual_ao_instalado": len(_afi0) == 1 and len(_i_afi9) == 1 and ast.dump(_afi0[0]) == ast.dump(_main9.body[_i_afi9[0]]),\n'
     '                       "try_selo_igual_ao_instalado_v399": len(_sel0) == 1 and len(_i_sel) == 1 and ast.dump(_sel0[0]) == ast.dump(_main9.body[_i_sel[0]]),\n'
     '                       "try_declaracao_igual_ao_instalado_v399": len(_dec0) == 1 and len(_i_dec) == 1 and ast.dump(_dec0[0]) == ast.dump(_main9.body[_i_dec[0]]),\n'
     '                       "try_sidecar_igual_ao_instalado_v399": len(_sc0) == 1 and len(_i_sc) == 1 and ast.dump(_sc0[0]) == ast.dump(_um9.body[_i_sc[0]]),\n'
     '                       "main_igual_ao_instalado_v399": ast.dump(_m0_9) == ast.dump(_main9), "unified_main_igual_ao_instalado_v399": ast.dump(_um0_9) == ast.dump(_um9),\n', 1),
    # os controles diretos do registro passam o beta do core (senao recusariam so' pela falta dele)
    ('neg9["selo:sha256_do_codigo_diferente"] = um.registro_core_v399(_b9, sha256_do_codigo="0" * 64).get("verdict")',
     '_rg = um.registro_core_v399(_b9, sha256_do_codigo="0" * 64, beta_core=core.get("beta")); neg9["selo:sha256_do_codigo_diferente"] = _rg.get("verdict"); _falhas9["selo:sha256_do_codigo_diferente"] = [d_ for d_, v_ in _rg["checks"] if not v_]', 1),
    ('neg9["selo:objeto_truncado_vs_sha_do_codigo"] = um.registro_core_v399(_b9[:-1], sha256_do_codigo=hashlib.sha256(_b9).hexdigest()).get("verdict")',
     '_rg = um.registro_core_v399(_b9[:-1], sha256_do_codigo=hashlib.sha256(_b9).hexdigest(), beta_core=core.get("beta")); neg9["selo:objeto_truncado_vs_sha_do_codigo"] = _rg.get("verdict"); _falhas9["selo:objeto_truncado_vs_sha_do_codigo"] = [d_ for d_, v_ in _rg["checks"] if not v_]', 1),
    ('um.CENTRO = 0; neg9["selo:perfil_centro_0"] = um.registro_core_v399(_b9[:1 << 20], sha256_do_codigo=hashlib.sha256(_b9[:1 << 20]).hexdigest()).get("verdict")',
     'um.CENTRO = 0; _rg = um.registro_core_v399(_b9[:1 << 20], sha256_do_codigo=hashlib.sha256(_b9[:1 << 20]).hexdigest(), beta_core=core.get("beta")); neg9["selo:perfil_centro_0"] = _rg.get("verdict"); _falhas9["selo:perfil_centro_0"] = [d_ for d_, v_ in _rg["checks"] if not v_]', 1),
    # o controle da v399 (alfa do bloco) vira os controles da v400 (a checagem do beta contra o core)
    ('        _al0 = um.ALPHA_FINE_CODATA_2018\n'
     '        try:\n'
     '            um.ALPHA_FINE_CODATA_2018 = _al0 * (1 + 1e-6); neg9["selo:alfa_do_bloco_adulterado"] = um.registro_core_v399(_b9[:1 << 20], sha256_do_codigo=hashlib.sha256(_b9[:1 << 20]).hexdigest()).get("verdict")\n'
     '        finally:\n'
     '            um.ALPHA_FINE_CODATA_2018 = _al0\n',
     '        R["v400_beta_info"] = {"ALPHA_FINE_CODATA_2018_existe_no_modulo": hasattr(um, "ALPHA_FINE_CODATA_2018"), "SEALED_CODATA_ALPHA": um.SEALED_CODATA_ALPHA, "beta_runtime": um._beta_runtime(), "beta_core": core.get("beta"),\n'
     '                               "rel": abs(um._beta_runtime() / core.get("beta") - 1.0), "fonte_beta_runtime": __import__("inspect").getsource(um._beta_runtime).strip()[-160:]}\n'
     '        _sa0 = um.SEALED_CODATA_ALPHA\n'
     '        try:\n'
     '            um.SEALED_CODATA_ALPHA = _sa0 * (1 + 1e-6); _rg = um.selo_acom_v399(copy.deepcopy(core)); neg9["selo:SEALED_CODATA_ALPHA_adulterado_1e-6"] = _rg.get("verdict"); _falhas9["selo:SEALED_CODATA_ALPHA_adulterado_1e-6"] = [d_ for d_, v_ in _rg["checks"] if not v_]\n'
     '        finally:\n'
     '            um.SEALED_CODATA_ALPHA = _sa0\n'
     '        for _nm, _f in (("selo:beta_do_core_adulterado_1e-6", 1 + 1e-6), ("selo:beta_do_core_adulterado_2e-9", 1 + 2e-9), ("selo:beta_do_core_zero", 0.0)):\n'
     '            _cb = copy.deepcopy(core); _cb["beta"] = core["beta"] * _f; _rg = um.selo_acom_v399(_cb); neg9[_nm] = _rg.get("verdict"); _falhas9[_nm] = [d_ for d_, v_ in _rg["checks"] if not v_]\n'
     '        _cb = copy.deepcopy(core); _cb.pop("beta", None); _rg = um.selo_acom_v399(_cb); neg9["selo:sem_beta_no_core"] = _rg.get("verdict"); _falhas9["selo:sem_beta_no_core"] = [d_ for d_, v_ in _rg["checks"] if not v_]\n'
     '        _rg = um.registro_core_v399(_b9[:1 << 20], sha256_do_codigo=hashlib.sha256(_b9[:1 << 20]).hexdigest()); neg9["selo:registro_chamado_sem_beta_core"] = _rg.get("verdict"); _falhas9["selo:registro_chamado_sem_beta_core"] = [d_ for d_, v_ in _rg["checks"] if not v_]\n'
     '        _cb = copy.deepcopy(core); _cb["beta"] = core["beta"] * (1 + 5e-10); _rg = um.selo_acom_v399(_cb); R["v400_beta_dentro_da_tolerancia_5e-10"] = {"verdict": _rg.get("verdict"), "rel": (_rg.get("values") or {}).get("rel_beta_vs_core")}\n', 1),
    ('    neg9 = {}\n', '    neg9 = {}; _falhas9 = {}\n', 1),
    ('    R["v400_controles_negativos"] = neg9\n', '    R["v400_controles_negativos"] = neg9; R["v400_controles_falhas"] = _falhas9\n', 1),
])
assert n_r >= 9
ast.parse("if True:\n    pass\n" + b) if False else None
open(os.path.join(F10, "_bloco_v400.py"), "w", encoding="utf-8").write(b)
# ---------------- exame_pontos_v400x (do v398x + o bloco)
s = open(os.path.join(F8, "exame_pontos_v398x.py"), encoding="utf-8").read()
s = sub(s, [('ap.add_argument("--sandbox", default=os.path.join(C_, "t", "k398c", "final"))', 'ap.add_argument("--sandbox", default=os.path.join(C_, "t", "k400c", "final"))', 1)])
s = s.replace('"""exame_pontos_v398x.py -- exame final v398', '"""exame_pontos_v400x.py -- exame final v400 (c1, 24/10/2026; molde: exame_pontos_v398x.py + _bloco_v400.py). Texto do molde: exame final v398', 1)
anchor = '# as instrucoes do main da v393 em diante (ate emit_figures), executadas como estao no candidato'
assert s.count(anchor) == 1
s = s.replace(anchor, b + "\n" + anchor, 1)
old = 'if "pedras_controles_negativos" in R and not ('
assert s.count(old) == 1
s = s.replace(old, 'if "v400_controles_negativos" in R and not (R["v400_controles_negativos"].get("todos_recusam") and R["v400_controles_negativos"].get("positivos_selam")): falsos.append("v400_controles")\n'
              'if R.get("v400_mexeu_em_chaves_existentes"): falsos.append("v400_mexeu")\n'
              'if "v400_ponto" in R and not all(R["v400_ponto"][k] for k in ("selo_imediatamente_depois_da_afinacao", "declaracao_imediatamente_depois_do_selo", "antes_do_bloco_v393", "try_afinacao_igual_ao_instalado", "try_selo_igual_ao_instalado_v399", "try_declaracao_igual_ao_instalado_v399", "try_sidecar_igual_ao_instalado_v399", "main_igual_ao_instalado_v399", "unified_main_igual_ao_instalado_v399", "sidecar_no_unified_main_depois_da_ultima_escrita_do_selo")): falsos.append("v400_ponto")\n'
              'if "selo_acom" in R and not (R["selo_acom"].get("all_verified") is True and R["declaracao"].get("all_verified") is True): falsos.append("v400_registros")\n'
              'if "v400_instrucao_real" in R and (R["v400_instrucao_real"]["erro"] or R["v400_instrucao_real"]["aviso"]): falsos.append("v400_instrucao_real")\n'
              'if "v400_d4" in R and not R["v400_d4"].get("ok"): falsos.append("v400_d4")\n'
              'if "v400_sidecar" in R and not R["v400_sidecar"].get("ok"): falsos.append("v400_sidecar")\n'
              'if "v400_beta_info" in R and (R["v400_beta_info"]["ALPHA_FINE_CODATA_2018_existe_no_modulo"] or not R["v400_beta_info"]["rel"] < 1e-9): falsos.append("v400_beta_info")\n' + old, 1)
ast.parse(s); open(os.path.join(F10, "exame_pontos_v400x.py"), "w", encoding="utf-8").write(s)
# ---------------- simular (do v399x)
s = open(os.path.join(F9, "simular_arvore_do_nos_v399x.py"), encoding="utf-8").read()
s = sub(s, [('V = os.path.join(os.path.dirname(os.path.dirname(H)), "v399")   # v399x: a pasta da cadeia v399', 'V = os.path.join(os.path.dirname(os.path.dirname(H)), "v400")   # v400x: a pasta da cadeia v400', 1),
            ('default=os.path.join(V, "um_v399_candidato.py")', 'default=os.path.join(V, "um_v400_candidato.py")', 1)])
s = s.replace('"""simular_arvore_do_nos_v399x.py -- exame final v399', '"""simular_arvore_do_nos_v400x.py -- exame final v400 (molde: simular_arvore_do_nos_v399x.py, so os caminhos). Texto do molde: exame final v399', 1)
ast.parse(s); open(os.path.join(F10, "simular_arvore_do_nos_v400x.py"), "w", encoding="utf-8").write(s)
print("ok", n_r)
