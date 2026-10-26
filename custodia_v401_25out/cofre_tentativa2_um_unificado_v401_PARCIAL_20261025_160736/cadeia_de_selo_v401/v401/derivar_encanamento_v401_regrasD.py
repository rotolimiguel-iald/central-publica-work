# -*- coding: utf-8 -*-
# regras (lote D) de derivar_encanamento_v401.py: o EXAME DOS PONTOS DE CHAMADA com o ponto novo da v401 (falsidade_da_inercia_v401). Escrito pela ferramenta Write (as barras invertidas nao colapsam).
# O ponto novo e' a instrucao do main (um `try`) que vem IMEDIATAMENTE depois da declaracao_do_operador_v399, na fractalizacao do Um; o exame a re-executa isolada, como fez com os pontos anteriores.

_ANCORA_DECL = '''out["core.declaracao_do_operador_v399"] = {"all_verified": dc.get("all_verified"), "verdict": str(dc.get("verdict"))[:300], "falhas": [d_ for d_, v_ in (dc.get("checks") or []) if not v_]}
'''
_BLOCO_FALSIDADE = '''# (4a-v401) o PONTO DE CHAMADA REAL do falsidade_da_inercia_v401 (v401): a instrucao do main (um `try`) que vem IMEDIATAMENTE depois da declaracao_do_operador_v399 (que vem imediatamente depois do selo_acom_v399), na fractalizacao do Um
ifa = [i for i, s_ in enumerate(unp) if "falsidade_da_inercia_v401(core)" in s_]
assert len(ifa) == 1 and ifa[0] == idc + 1, ("a instrucao do main que chama falsidade_da_inercia_v401 nao e' unica ou nao vem IMEDIATAMENTE depois da declaracao_do_operador_v399", ifa, idc)
ifa = ifa[0]
R["ponto_falsidade"] = {"indice_no_main": ifa, "linha": main.body[ifa].lineno, "antes_do_bloco_v393": ifa < i0, "logo_depois_da_declaracao_v399": "declaracao_do_operador_v399(core)" in unp[ifa - 1], "instrucao_anterior": unp[ifa - 1][:160].replace("\\n", " | ")}
builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[ifa]], type_ignores=[])), "<main:falsidade_da_inercia_v401>", "exec"), g); errfa = None
except Exception as e:
    import traceback; errfa = repr(e) + traceback.format_exc()[-900:]
finally:
    stdout_fa = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
fa = core.get("falsidade_da_inercia_v401") or {}
R["ponto_falsidade"].update({"erro": errfa, "stdout": stdout_fa.splitlines(), "avisos": [l for l in stdout_fa.splitlines() if "AVISO" in l], "verdict": fa.get("verdict"), "all_verified": fa.get("all_verified"),
                            "mecanica": {"passed": (fa.get("mechanics") or {}).get("passed"), "n_checks": (fa.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (fa.get("unconditional") or {}).get("in_kernel"), "estrela_in_kernel": (fa.get("key_theorem") or {}).get("in_kernel"),
                            "costless_ok": (fa.get("costless") or {}).get("ok"), "beta_ok": fa.get("beta_ok"), "post_inertial_scales": (fa.get("values") or {}).get("post_inertial_scales"), "fixo_pelo_fluxo_inteiro": (fa.get("values") or {}).get("fixed_by_the_whole_flow")})
out["core.falsidade_da_inercia_v401"] = {"all_verified": fa.get("all_verified"), "verdict": str(fa.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((fa.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
'''
_FALSOS = '''pfa = R["ponto_falsidade"]
if (pfa.get("erro") or pfa.get("avisos") or pfa.get("all_verified") is not True or not pfa.get("antes_do_bloco_v393") or not pfa.get("logo_depois_da_declaracao_v399") or pfa.get("unconditional_in_kernel") is not True or pfa.get("estrela_in_kernel") is not True
        or pfa.get("costless_ok") is not True or pfa.get("beta_ok") is not True or pfa.get("post_inertial_scales") != [] or pfa.get("fixo_pelo_fluxo_inteiro") != [0.0] or (pfa.get("mecanica") or {}).get("n_checks") != 7): falsos.append("ponto_falsidade")
pv = R["ponto_veracidade"]
'''
entrada("exame_pontos_v400.py", autoral=True, regras=[
    ("list(um._V399_NOMES_REGISTROS):\n    core.pop(n_, None)", 'list(um._V399_NOMES_REGISTROS) + ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS):\n    core.pop(n_, None)', 1),
    (_ANCORA_DECL, _ANCORA_DECL + _BLOCO_FALSIDADE, 1),
    ('                   "novas": [k for k in R["chaves_novas_no_core"]', '                   "v401_falsidade": [k for k in ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n                   "novas": [k for k in R["chaves_novas_no_core"]', 1),
    ('"registros_v399": {n_: ((seal.get("registros_v399") or {}).get(n_) or {}).get("all_verified") for n_ in um._V399_NOMES_REGISTROS}}',
     '"registros_v399": {n_: ((seal.get("registros_v399") or {}).get(n_) or {}).get("all_verified") for n_ in um._V399_NOMES_REGISTROS},\n                 "falsidade_da_inercia_v401": {x: (seal.get("falsidade_da_inercia_v401") or {}).get(x) for x in ("verdict", "all_verified")},\n'
     '                 "registros_v401": {n_: ((seal.get("registros_v401") or {}).get(n_) or {}).get("all_verified") for n_ in um._V401_NOMES_REGISTROS}}', 1),
    ('pv = R["ponto_veracidade"]\n', _FALSOS, 1),
])
