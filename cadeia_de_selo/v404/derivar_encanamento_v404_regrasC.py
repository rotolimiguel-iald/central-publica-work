# -*- coding: utf-8 -*-
# regras (lote C) de derivar_encanamento_v404.py: o ENSAIO (simular a arvore do Nos, exame dos pontos de chamada, ensaio a seco, guardas estaticas da Bancada). ORIGEM v403 (mapa 402 -> 403, 403 -> 404).
# A base mecanica sobe da v403 FINAL; a logica NOVA da v404 (os TRES registros com funcao, os specs v404, as duas pedras, a errata de F2b) entra como regras de contagem exata. Os blocos que tratam dos registros da v401 (falsidade_da_inercia_v401 etc.), da v402 (ponte, queda, esperanca)
# e da v403 (caminho, vida, adendo da verdade, bandeiras do gate) voltam do arquivo ORIGINAL da v403 sem subida de versao (a semantica deles e' a da v403: eles agora sao RECRIADOS e comparados com os da v403 selada; DL.X -> DL.D3.X para os nomes que a v404 sobrescreve).
# Escrito pela ferramenta Write (as barras invertidas nao colapsam).
import importlib.util as _ilu
CH_ = os.path.dirname(HERE)
_ORIG_ENS = open(os.path.join(CH_, "v403", "ensaio_a_seco_v403.py"), encoding="utf-8").read()
_ORIG_EXA = open(os.path.join(CH_, "v403", "exame_pontos_v403.py"), encoding="utf-8").read()
_DL4 = _ilu.spec_from_file_location("delta_v404_regras", os.path.join(HERE, "delta_v404.py")); DL4 = _ilu.module_from_spec(_DL4); _DL4.loader.exec_module(DL4)
_DL3 = DL4.D3
# os nomes de DL que a v404 SOBRESCREVE (ou cria) e que o texto original da v403 usa como "os da v403": viram DL.D3.<nome> nos blocos que RECRIAM os registros da v403
NOMES_SOBRESCRITOS = sorted(n_ for n_ in vars(_DL3) if not n_.startswith("__") and n_ in vars(DL4) and getattr(DL4, n_) is not getattr(_DL3, n_) and n_ not in ("D3", "HERE", "V403", "C", "WK", "CENTRAL"))


def para_d3(txt_):
    """no texto ORIGINAL da v403: `DL.<nome>` -> `DL.D3.<nome>` para cada nome que a v404 sobrescreve (os blocos recriam os registros da v403 com os dados DA v403)."""
    import re as _re
    for n_ in sorted(NOMES_SOBRESCRITOS, key=len, reverse=True):
        txt_ = _re.sub(r"\bDL\.%s\b" % n_, "DL.D3." + n_, txt_)
    return txt_


# ------------------------------------------------------------------------------------------- simular a arvore do Nos: mais os tres registros (chamados no main logo depois do bandeiras_do_gate_v403) e os specs da v404
entrada("simular_arvore_do_nos_v403.py", autoral=True, regras=[
    ("(mais os tres registros com funcao da v403 e os quatro da v404). Molde:", "(mais os quatro registros com funcao da v403 e os tres da v404). Molde:", 1),
    ("um.caminho_v403(core); um.vida_v403(core); um.verdade_adendo_v403(core); um.bandeiras_do_gate_v403(core)   # (na fractalizacao",
     "um.caminho_v403(core); um.vida_v403(core); um.verdade_adendo_v403(core); um.bandeiras_do_gate_v403(core); um.projecao_transversal_v404(core); um.jo8v32_v404(core); um.f2b_errata_v404(core)   # (na fractalizacao", 1),
    ("um._v402_rodar_specs(core); um._v403_rodar_specs(core)   # (v397:", "um._v402_rodar_specs(core); um._v403_rodar_specs(core); um._v404_rodar_specs(core)   # (v397:", 1),
    ('for k in ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", ',
     'for k in ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", ', 1),
    ("# F8.1 (v404): o gate recomputado com a prove_qg_closure_gate NOVA sobre o kf da arvore simulada", "# (v404: o gate NAO muda) o gate recomputado com a prove_qg_closure_gate sobre o kf da arvore simulada", 1),
])

# ------------------------------------------------------------------------------------------- exame dos pontos de chamada: os TRES pontos novos (projecao, jo8v32, errata de F2b), em ordem, logo depois do bandeiras_do_gate_v403
_BLOCO_PONTOS404 = r'''# (4a-v404c) os PONTOS DE CHAMADA REAIS da projecao transversal, do jo8v32 e da errata de F2b (v404): as duas instrucoes de pedra do main (cada uma um `try`) que vem IMEDIATAMENTE depois do bandeiras_do_gate_v403, em ordem, e a da errata de F2b, que vem IMEDIATAMENTE depois da errata ao lado de R6 da v386 (depois dos tres insumos do core que ela le), na fractalizacao do Um
_ANTERIOR_V404C = {"projecao": "bandeiras_do_gate_v403(core)", "jo8v32": "projecao_transversal_v404(core)", "f2b": "a errata ao lado de R6 e a cobranca F2b"}
# [licao da 1a tentativa do rito v404, 28/10/2026] a errata de F2b vem logo DEPOIS da errata ao lado de R6 da v386 e DEPOIS das tres atribuicoes do core que ela le
# (ramo_b_preregistration_v386, ledger_errata_v386, the_ledger_of_charges_v383): chamada logo depois do Jo8v32 ela lia um core sem elas e recusava as 7 checagens
_ATRIB_MAIN = {}
for _ia, _sta in enumerate(main.body):
    for _na in ast.walk(_sta):
        if isinstance(_na, ast.Assign):
            for _ta in _na.targets:
                if isinstance(_ta, ast.Subscript) and isinstance(_ta.value, ast.Name) and _ta.value.id == "core" and isinstance(_ta.slice, ast.Constant) and isinstance(_ta.slice.value, str):
                    _ATRIB_MAIN.setdefault(_ta.slice.value, _ia)
_INSUMOS_F2B = ("ramo_b_preregistration_v386", "ledger_errata_v386", "the_ledger_of_charges_v383")
for nome_, fn_, off_ in (("projecao", "projecao_transversal_v404", 8), ("jo8v32", "jo8v32_v404", 9), ("f2b", "f2b_errata_v404", None)):
    ii_ = [i for i, s_ in enumerate(unp) if fn_ + "(core)" in s_]
    if off_ is not None:
        assert len(ii_) == 1 and ii_[0] == ifa + off_, ("a instrucao do main que chama %s nao e' unica ou nao vem na ordem, logo depois do bandeiras_do_gate_v403" % fn_, ii_, ifa)
    else:
        _ins_ = {k_: _ATRIB_MAIN.get(k_) for k_ in _INSUMOS_F2B}
        assert len(ii_) == 1 and all(v_ is not None and v_ < ii_[0] for v_ in _ins_.values()) and _ANTERIOR_V404C["f2b"] in unp[ii_[0] - 1], ("a instrucao do main que chama %s nao e' unica, nao vem logo depois da errata ao lado de R6 (v386) ou vem ANTES de um insumo do core que ela le" % fn_, ii_, _ins_)
    ii_ = ii_[0]
    R["ponto_" + nome_] = {"indice_no_main": ii_, "linha": main.body[ii_].lineno, "antes_do_bloco_v393": ii_ < i0, "logo_depois_da_anterior": _ANTERIOR_V404C[nome_] in unp[ii_ - 1], "insumos_do_core_atribuidos_antes": ({k_: {"indice": _ATRIB_MAIN.get(k_), "antes": (_ATRIB_MAIN.get(k_) is not None and _ATRIB_MAIN[k_] < ii_)} for k_ in _INSUMOS_F2B} if nome_ == "f2b" else None), "instrucao_anterior": unp[ii_ - 1][:160].replace("\n", " | ")}
    builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[ii_]], type_ignores=[])), "<main:%s>" % fn_, "exec"), g); err_ = None
    except Exception as e:
        import traceback; err_ = repr(e) + traceback.format_exc()[-900:]
    finally:
        stdout_ = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
    r_ = core.get(fn_) or {}
    R["ponto_" + nome_].update({"erro": err_, "stdout": stdout_.splitlines(), "avisos": [l for l in stdout_.splitlines() if "AVISO" in l or "RECUSA" in l], "verdict": r_.get("verdict"), "all_verified": r_.get("all_verified"),
                                "mecanica": {"passed": (r_.get("mechanics") or {}).get("passed"), "n_checks": (r_.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (r_.get("unconditional") or {}).get("in_kernel"),
                                "estrela_in_kernel": (r_.get("key_theorem") or {}).get("in_kernel"), "contexto_ok": (r_.get("context") or {}).get("ok"), "beta_ok": r_.get("beta_ok"), "valores": (r_.get("values") if nome_ == "f2b" else None), "f2b_status_now": (r_.get("F2b_status_now") if nome_ == "f2b" else None)})
    out["core." + fn_] = {"all_verified": r_.get("all_verified"), "verdict": str(r_.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((r_.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
'''
_FALSOS404 = r'''for nome_ in ("projecao", "jo8v32"):
    pp404c_ = R["ponto_" + nome_]
    if (pp404c_.get("erro") or pp404c_.get("avisos") or pp404c_.get("all_verified") is not True or not pp404c_.get("antes_do_bloco_v393") or not pp404c_.get("logo_depois_da_anterior") or pp404c_.get("unconditional_in_kernel") is not True or pp404c_.get("estrela_in_kernel") is not True
            or pp404c_.get("contexto_ok") is not True or pp404c_.get("beta_ok") is not True or (pp404c_.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS[nome_]): falsos.append("ponto_" + nome_)
pf2_ = R["ponto_f2b"]
if (pf2_.get("erro") or pf2_.get("avisos") or pf2_.get("all_verified") is not True or not pf2_.get("antes_do_bloco_v393") or not pf2_.get("logo_depois_da_anterior") or (pf2_.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS["f2b"]
        or pf2_.get("f2b_status_now") != DL.F2B_FUTURO_TOKEN or (pf2_.get("valores") or {}).get("previsao_fora_do_intervalo_de_A") is not True or (pf2_.get("valores") or {}).get("n_cobrancas_v383") != 11): falsos.append("ponto_f2b")
'''
_SELO404_EXAME = '''
                 "projecao_transversal_v404": {x: (seal.get("projecao_transversal_v404") or {}).get(x) for x in ("verdict", "all_verified")}, "jo8v32_v404": {x: (seal.get("jo8v32_v404") or {}).get(x) for x in ("verdict", "all_verified")},
                 "f2b_errata_v404": {x: (seal.get("f2b_errata_v404") or {}).get(x) for x in ("verdict", "all_verified", "F2b_status_now")}, "registros_v404": {n_: ((seal.get("registros_v404") or {}).get(n_) or {}).get("all_verified") for n_ in um._V404_NOMES_REGISTROS}'''
entrada("exame_pontos_v403.py", autoral=True, regras=[
    ('# F8.1 (v404): a prove_qg_closure_gate NOVA, com o teste nulo cego do core da v403 selada', '# (v404: o gate NAO muda) a prove_qg_closure_gate com o teste nulo cego do core da v403 selada', 1),
    ('"checks_da_v403_mais_a_sonda": bool(len(g_new.get("checks") or []) == len(g_old.get("checks") or []) + 1 and all(v_ is True for _, v_ in g_new["checks"]) and [c_[0] for c_ in g_new["checks"] if not str(c_[0]).startswith("ProbeBlindNullAbsent")] == [c_[0] for c_ in g_old["checks"]])}',
     '"checks_da_v403_iguais": bool(J(g_new.get("checks")) == J(g_old.get("checks")) and all(v_ is True for _, v_ in g_new["checks"]))}', 1),
    ('(R.get("gate_recomputado") or {}).get("checks_da_v403_mais_a_sonda") is not True', '(R.get("gate_recomputado") or {}).get("checks_da_v403_iguais") is not True', 1),
    ('# F8.1 (v404): o gate recomputado com a prove_qg_closure_gate NOVA (o run_um do rito o faz antes de tudo); o registro bandeiras_do_gate_v403 le este qg_closure', '# (v404: o gate NAO muda) o gate recomputado com a prove_qg_closure_gate (o run_um do rito o faz antes de tudo); o registro bandeiras_do_gate_v403 le este qg_closure', 1),
    ('# (4a\') o PONTO DE CHAMADA REAL do teste_de_veracidade_fase9_v397 (v397):', _BLOCO_PONTOS404 + '# (4a\') o PONTO DE CHAMADA REAL do teste_de_veracidade_fase9_v397 (v397):', 1),
    ('                   "v404_caminho_vida_verdade_bandeiras": [k for k in ["caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"] + list(um._V403_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n',
     '                   "v404_caminho_vida_verdade_bandeiras": [k for k in ["caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"] + list(um._V403_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n'
     '                   "v404_projecao_jo8v32_f2b": [k for k in ["projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404"] + list(um._V404_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n', 1),
    ('"bandeiras_do_gate_v403": {x: (seal.get("bandeiras_do_gate_v403") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v403": {n_: ((seal.get("registros_v403") or {}).get(n_) or {}).get("all_verified") for n_ in um._V403_NOMES_REGISTROS}}',
     '"bandeiras_do_gate_v403": {x: (seal.get("bandeiras_do_gate_v403") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v403": {n_: ((seal.get("registros_v403") or {}).get(n_) or {}).get("all_verified") for n_ in um._V403_NOMES_REGISTROS},' + _SELO404_EXAME + '}', 1),
    ('or pp404b_.get("contexto_ok") is not True or pp404b_.get("beta_ok") is not True or (pp404b_.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS[nome_]): falsos.append("ponto_" + nome_)\n',
     'or pp404b_.get("contexto_ok") is not True or pp404b_.get("beta_ok") is not True or (pp404b_.get("mecanica") or {}).get("n_checks") != DL.D3.N_CHECKS[nome_]): falsos.append("ponto_" + nome_)\n', 1),
    ('(pbg_.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS["gate"]', '(pbg_.get("mecanica") or {}).get("n_checks") != DL.D3.N_CHECKS["gate"]', 1),
    ('pv = R["ponto_veracidade"]\n', _FALSOS404 + 'pv = R["ponto_veracidade"]\n', 1),
    ('+ ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS):\n    core.pop(n_, None)   # o fluxo os recria; comparam-se depois com os do core0',
     '+ ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS) + ["caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"] + list(um._V403_NOMES_REGISTROS):\n    core.pop(n_, None)   # o fluxo os recria; comparam-se depois com os do core0', 1),
])

# ------------------------------------------------------------------------------------------- as guardas estaticas da Bancada: o mutante m6 usa um alvo errado que NAO e' o da v404
entrada("guardas_estaticas_bancada_v403.py", autoral=True, regras=[
    ('(rodar("m6", cand, "v404", versao_no_selo="v404"), "UM_VERSION_DIFERENTE_DO_ALVO")', '(rodar("m6", cand, "v403", versao_no_selo="v403"), "UM_VERSION_DIFERENTE_DO_ALVO")', 1),
    ("(C:\\\\t\\\\vb20\\\\gate_*)", "(C:\\\\t\\\\vb21\\\\gate_*)", 1),
])

# ------------------------------------------------------------------------------------------- o ENSAIO A SECO (as regras do ensaio entram no lote C2: derivar_encanamento_v404_regrasC2_ensaio.py)
