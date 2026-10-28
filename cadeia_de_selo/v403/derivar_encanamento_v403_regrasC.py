# -*- coding: utf-8 -*-
# regras (lote C) de derivar_encanamento_v403.py: o ENSAIO (simular a arvore do Nos, exame dos pontos de chamada, ensaio a seco, guardas estaticas da Bancada). ORIGEM v402 (mapa 401 -> 402, 402 -> 403).
# A base mecanica sobe da v402 FINAL; a logica NOVA da v403 (os QUATRO registros com funcao, os specs v403, as tres pedras, a F8.1) entra como regras de contagem exata. Os blocos que tratam dos registros da v401 (falsidade_da_inercia_v401 etc.) e da v402 (ponte, queda, esperanca)
# voltam do arquivo ORIGINAL da v402 sem subida de versao (a semantica deles e' a da v402: eles agora sao RECRIADOS e comparados com os da v402 selada; DL.STONES etc. viram DL.D2.*). Escrito pela ferramenta Write (as barras invertidas nao colapsam).

CH_ = os.path.dirname(HERE)
_ORIG_ENS = open(os.path.join(CH_, "v402", "ensaio_a_seco_v402.py"), encoding="utf-8").read()

# ------------------------------------------------------------------------------------------- simular a arvore do Nos: mais os quatro registros (chamados no main logo depois da esperanca condicional), os specs da v403 e o gate recomputado
entrada("simular_arvore_do_nos_v402.py", autoral=True, regras=[
    ("um.declaracao_do_operador_v399(core); um.falsidade_da_inercia_v401(core); um.ponte_da_escala_dual_v402(core); um.queda_sem_geometria_v402(core); um.esperanca_condicional_v402(core)   # (na fractalizacao",
     "um.declaracao_do_operador_v399(core); um.falsidade_da_inercia_v401(core); um.ponte_da_escala_dual_v402(core); um.queda_sem_geometria_v402(core); um.esperanca_condicional_v402(core); um.caminho_v403(core); um.vida_v403(core); um.verdade_adendo_v403(core); um.bandeiras_do_gate_v403(core)   # (na fractalizacao", 1),
    ("um._v401_rodar_specs(core); um._v402_rodar_specs(core)   # (v397:", "um._v401_rodar_specs(core); um._v402_rodar_specs(core); um._v403_rodar_specs(core)   # (v397:", 1),
    ('for k in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", ', 'for k in ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", ', 1),
    ('core = copy.deepcopy(C0); core["kernel_formalization"] = kf; core["external_ladder"] = um.prove_external_ladder(1.0, kf)',
     'core = copy.deepcopy(C0); core["kernel_formalization"] = kf; core["external_ladder"] = um.prove_external_ladder(1.0, kf)\n'
     'core["qg_closure"] = um.prove_qg_closure_gate(1.0, kf, independent_rite=core.get("void_floor_v11"), blind_null=core.get("void_stacking_blind"))   # F8.1 (v403): o gate recomputado com a prove_qg_closure_gate NOVA sobre o kf da arvore simulada e os dados (V11, teste nulo cego) do core da v402 selada, como o run_um do rito faz', 1),
    ("v394, v395, v397, v402 e v403 sobre esse kf (mais os tres registros com funcao da v403).", "v394, v395, v397, v401, v402 e v403 sobre esse kf (mais os tres registros com funcao da v402 e os quatro da v403).", 1),
])

# ------------------------------------------------------------------------------------------- exame dos pontos de chamada: os QUATRO pontos novos (caminho, vida, adendo da verdade, bandeiras do gate), em ordem, logo depois da esperanca condicional (v402)
_ANC_PV = '''# (4a') o PONTO DE CHAMADA REAL do teste_de_veracidade_fase9_v397'''
_BLOCO_PONTOS403 = '''# (4a-v403b) os PONTOS DE CHAMADA REAIS do caminho, da vida, do adendo da verdade e das bandeiras do gate (v403): as quatro instrucoes do main (cada uma um `try`) que vem IMEDIATAMENTE depois da esperanca_condicional_v402, em ordem, na fractalizacao do Um
_ANTERIOR_V403 = ["esperanca_condicional_v402(core)", "caminho_v403(core)", "vida_v403(core)", "verdade_adendo_v403(core)"]
for nome_, fn_, off_ in (("caminho", "caminho_v403", 4), ("vida", "vida_v403", 5), ("verdade_adendo", "verdade_adendo_v403", 6), ("bandeiras", "bandeiras_do_gate_v403", 7)):
    ii_ = [i for i, s_ in enumerate(unp) if fn_ + "(core)" in s_]
    assert len(ii_) == 1 and ii_[0] == ifa + off_, ("a instrucao do main que chama %s nao e' unica ou nao vem na ordem, logo depois da esperanca_condicional_v402" % fn_, ii_, ifa)
    ii_ = ii_[0]
    R["ponto_" + nome_] = {"indice_no_main": ii_, "linha": main.body[ii_].lineno, "antes_do_bloco_v393": ii_ < i0, "logo_depois_da_anterior": _ANTERIOR_V403[off_ - 4] in unp[ii_ - 1], "instrucao_anterior": unp[ii_ - 1][:160].replace("\\n", " | ")}
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
                                "estrela_in_kernel": (r_.get("key_theorem") or {}).get("in_kernel"), "contexto_ok": (r_.get("context") or {}).get("ok"), "beta_ok": r_.get("beta_ok"), "valores_do_gate": (r_.get("values") if nome_ == "bandeiras" else None)})
    out["core." + fn_] = {"all_verified": r_.get("all_verified"), "verdict": str(r_.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((r_.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
'''
_FALSOS403 = '''for nome_ in ("caminho", "vida", "verdade_adendo"):
    pp403b_ = R["ponto_" + nome_]
    if (pp403b_.get("erro") or pp403b_.get("avisos") or pp403b_.get("all_verified") is not True or not pp403b_.get("antes_do_bloco_v393") or not pp403b_.get("logo_depois_da_anterior") or pp403b_.get("unconditional_in_kernel") is not True or pp403b_.get("estrela_in_kernel") is not True
            or pp403b_.get("contexto_ok") is not True or pp403b_.get("beta_ok") is not True or (pp403b_.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS[nome_]): falsos.append("ponto_" + nome_)
pbg_ = R["ponto_bandeiras"]
if (pbg_.get("erro") or pbg_.get("avisos") or pbg_.get("all_verified") is not True or not pbg_.get("antes_do_bloco_v393") or not pbg_.get("logo_depois_da_anterior") or (pbg_.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS["gate"]
        or (pbg_.get("valores_do_gate") or {}).get("n_flags") != 18 or (pbg_.get("valores_do_gate") or {}).get("n_literal") != 0 or (pbg_.get("valores_do_gate") or {}).get("gate_verdict_equals_v402") is not True): falsos.append("ponto_bandeiras")
'''
_SELO403_EXAME = '''
                 "caminho_v403": {x: (seal.get("caminho_v403") or {}).get(x) for x in ("verdict", "all_verified")}, "vida_v403": {x: (seal.get("vida_v403") or {}).get(x) for x in ("verdict", "all_verified")}, "verdade_adendo_v403": {x: (seal.get("verdade_adendo_v403") or {}).get(x) for x in ("verdict", "all_verified")},
                 "bandeiras_do_gate_v403": {x: (seal.get("bandeiras_do_gate_v403") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v403": {n_: ((seal.get("registros_v403") or {}).get(n_) or {}).get("all_verified") for n_ in um._V403_NOMES_REGISTROS}'''
entrada("exame_pontos_v402.py", autoral=True, regras=[
    ('g_new = um.prove_qg_closure_gate(1.0, kf, independent_rite=core0.get("void_floor_v11")); g_old = core0.get("qg_closure") or {}',
     'g_new = um.prove_qg_closure_gate(1.0, kf, independent_rite=core0.get("void_floor_v11"), blind_null=core0.get("void_stacking_blind")); g_old = core0.get("qg_closure") or {}   # F8.1 (v403): a prove_qg_closure_gate NOVA, com o teste nulo cego do core da v402 selada', 1),
    ('"n18_novo": n18(g_new), "n18_core0": n18(g_old), "flags_iguais": all(J(g_new.get(f)) == J(g_old.get(f)) for f in ("formal_flags", "physics_flags", "experiment_flags")), "all_verified": g_new.get("all_verified")}',
     '"n18_novo": n18(g_new), "n18_core0": n18(g_old), "flags_iguais": all(J(g_new.get(f)) == J(g_old.get(f)) for f in ("formal_flags", "physics_flags", "experiment_flags")), "all_verified": g_new.get("all_verified"),\n'
     '                             "sem_checks_igual": J({k_: v_ for k_, v_ in g_new.items() if k_ != "checks"}) == J({k_: v_ for k_, v_ in g_old.items() if k_ != "checks"}), "n_checks_novo": len(g_new.get("checks") or []), "n_checks_core0": len(g_old.get("checks") or []),\n'
     '                             "checks_da_v402_mais_a_sonda": bool(len(g_new.get("checks") or []) == len(g_old.get("checks") or []) + 1 and all(v_ is True for _, v_ in g_new["checks"]) and [c_[0] for c_ in g_new["checks"] if not str(c_[0]).startswith("ProbeBlindNullAbsent")] == [c_[0] for c_ in g_old["checks"]])}', 1),
    ('    core.pop(n_, None)   # o fluxo os recria; comparam-se depois com os do core0\nantes = ',
     '    core.pop(n_, None)   # o fluxo os recria; comparam-se depois com os do core0\n'
     'if isinstance(R.get("gate_recomputado"), dict) and "EXCECAO" not in R["gate_recomputado"]:\n'
     '    core["qg_closure"] = g_new   # F8.1 (v403): o gate recomputado com a prove_qg_closure_gate NOVA (o run_um do rito o faz antes de tudo); o registro bandeiras_do_gate_v403 le este qg_closure\n'
     'antes = ', 1),
    (_ANC_PV, _BLOCO_PONTOS403 + _ANC_PV, 1),
    ('                   "v403_ponte_queda_esperanca": [k for k in ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n',
     '                   "v403_ponte_queda_esperanca": [k for k in ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n'
     '                   "v403_caminho_vida_verdade_bandeiras": [k for k in ["caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"] + list(um._V403_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n', 1),
    ('"esperanca_condicional_v402": {x: (seal.get("esperanca_condicional_v402") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v402": {n_: ((seal.get("registros_v402") or {}).get(n_) or {}).get("all_verified") for n_ in um._V402_NOMES_REGISTROS}}',
     '"esperanca_condicional_v402": {x: (seal.get("esperanca_condicional_v402") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v402": {n_: ((seal.get("registros_v402") or {}).get(n_) or {}).get("all_verified") for n_ in um._V402_NOMES_REGISTROS},' + _SELO403_EXAME + '}', 1),
    ('if (R.get("gate_recomputado") or {}).get("verdict_igual") is not True or (R.get("gate_recomputado") or {}).get("n18_novo") != 18: falsos.append("gate")',
     'if (R.get("gate_recomputado") or {}).get("verdict_igual") is not True or (R.get("gate_recomputado") or {}).get("n18_novo") != 18 or (R.get("gate_recomputado") or {}).get("flags_iguais") is not True or (R.get("gate_recomputado") or {}).get("sem_checks_igual") is not True or (R.get("gate_recomputado") or {}).get("checks_da_v402_mais_a_sonda") is not True or (R.get("gate_recomputado") or {}).get("all_verified") is not True: falsos.append("gate")', 1),
    ('or (pp403_.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS[nome_]): falsos.append("ponto_" + nome_)\n', 'or (pp403_.get("mecanica") or {}).get("n_checks") != DL.D2.N_CHECKS[nome_]): falsos.append("ponto_" + nome_)\n' + _FALSOS403, 1),
])

# ------------------------------------------------------------------------------------------- as guardas estaticas da Bancada: a v399 SELADA (o defeito real) vem da copia de bytes que a cadeia v400 guardou; o mutante m6 usa um alvo errado que NAO e' o da v403
entrada("guardas_estaticas_bancada_v402.py", autoral=True, regras=[
    ('(rodar("m6", cand, "v403", versao_no_selo="v403"), "UM_VERSION_DIFERENTE_DO_ALVO")', '(rodar("m6", cand, "v404", versao_no_selo="v404"), "UM_VERSION_DIFERENTE_DO_ALVO")', 1),
    ("(C:\\\\t\\\\vb19\\\\gate_*)", "(C:\\\\t\\\\vb20\\\\gate_*)", 1),
])

# ------------------------------------------------------------------------------------------- o ENSAIO A SECO
_DOC_ENS = '''"""ensaio_a_seco_v403.py -- ENSAIO A SECO da v403 (molde: ensaio_a_seco_v402.py FINAL, que rodou na cadeia da v402, com as licoes da v399 a v402), SEM a GPU do rito e SEM rodar o rito. Chama NO PONTO DE CHAMADA REAL todo veredito novo ou alterado.
uso: python -B -X utf8 ensaio_a_seco_v403.py <candidato.py> <rotulo>
A v403 e' uma versao de CONTEUDO (os nomes do operador, 27/10/2026) e a F8.1: TRES modulos novos de kernel (TGLExt/Caminho, TGLExt/Vida, TGLExt/VerdadeAdendo), os registros com FUNCAO caminho_v403, vida_v403, verdade_adendo_v403 e bandeiras_do_gate_v403, os registros por spec cunhagens_v403 e kh_n1_cobertura_v403,
e as TRES bandeiras literais do gate passam a CALCULADAS (prove_qg_closure_gate com o kwarg blind_null): o gate e' RECOMPUTADO aqui sobre os dados do core da v402 selada e o ensaio confere que a letra do veredito, as chaves e os valores das 18 bandeiras NAO mudam.
A base e' a v402 SELADA (core e selo em base_v402), o kernel e' o da v402 + as tres pedras (sandbox C:/t/k403c); os registros de v393 a v399, os da v401 (falsidade_da_inercia_v401, cunhagens_v401, kh_n1_cobertura_v401) E OS DA V402 (ponte_da_escala_dual_v402, queda_sem_geometria_v402, esperanca_condicional_v402, cunhagens_v402, kh_n1_cobertura_v402)
sao RECRIADOS e comparados com os da v402 selada (os rotulos 'v402' dos nomes de relatorio herdados da subida de versao significam a base selada). Etapas:
(1) copia o candidato; materializa o kernel embutido e confere BYTE A BYTE contra o sandbox; (2) importa (o rito NAO roda); UM_VERSION v403; (3) o core da v402 SELADA + o kernel REAL: verify_tgl_kernel_formalization() de ponta a ponta com o lake simulado devolvendo os logs CRUS do sandbox;
(4) os registros vizinhos RECOMPUTADOS: iguais, ou a TROCA DITA (so' numeros: a escada e a cobertura crescem com as pedras); (5) o FLUXO PRINCIPAL v393 a v399, v401, v402 e v403 (as instrucoes etiquetadas do main, na ordem do arquivo), as chaves NOVAS no core: as seis da v403;
(6) unidade: o Teste da Unica Palavra (v397), o sonico e a afinacao (v398), o selo pela propria tecnologia e a declaracao do operador (v399), a FALSIDADE DA INERCIA (v401, recriada), os TRES registros com funcao da v402 (recriados), os QUATRO da v403 (cada elo recusa), o GATE recomputado, os registros por spec, a cobertura, o sidecar;
(7) o selo (a instrucao `seal = {...}` do main + o resumo) e o indice; (8) artigo PT/EN, pdflatex x2, a secao v403 (antes da v402) e o QUADRO NO TOPO (v397, intocado); (9) .md e manifesto; (10) o conferidor de citacoes; (11) simular_arvore_do_nos; (12) exame_pontos;
(13) [LICAO DA v400, mantida] as guardas ESTATICAS do esboco R3.5 da Bancada (ALPHA_LINHA_UNICA e as demais que nao dependem do selo) rodadas SOBRE O CANDIDATO, chamando a funcao do proprio esboco pinado, ANTES de instalar."""
'''
# --- os blocos (6f) da v401 e (6g) da v402 voltam do arquivo ORIGINAL da v402 (a semantica deles e' a da base: recriados e comparados com os selados); (6g) usa DL.D2.* (o delta da v402); o teste do piso do kh_n1 e' trocado (a v402 agora cobra piso) e entra no (6h)
_i6f = _ORIG_ENS.index("# (6f) [v401, recriado na v402 e comparado com o selado]"); _i6g = _ORIG_ENS.index("# (6g) [v402] os TRES registros com FUNCAO"); _i6x = _ORIG_ENS.index('rep["unidade"] = U; print("unidade:"')
_6F = _ORIG_ENS[_i6f:_i6g].replace("# (6f) [v401, recriado na v402 e comparado com o selado]", "# (6f) [v401, recriado na v402 e na v403 e comparado com o selado]")
_6G = _ORIG_ENS[_i6g:_i6x]
_kh_ini = _6G.index('_kh2 = c.get("kh_n1_cobertura_v402") or {}; _kh1s = '); _kh_fim = _6G.index('U["contratos_v394_a_v401_pinam_a_escada_da_v402"]')
_6G = _6G[:_kh_ini] + _6G[_kh_fim:]
for _old, _new, _n in (('DL.STONE_BY_KEY[k402_]', 'DL.D2.STONE_BY_KEY[k402_]', 1), ('DL.N_CHECKS[k402_]', 'DL.D2.N_CHECKS[k402_]', 1), ('DL.VERBATIM_ORIGEM_V402', 'DL.D2.VERBATIM_ORIGEM_V402', 1), ('for s_ in DL.STONES}', 'for s_ in DL.D2.STONES}', 2),
                       ('U["contratos_v394_a_v401_pinam_a_escada_da_v402"]', 'U["contratos_v394_a_v401_pinam_a_escada_da_v403"]', 1), ("# (6g) [v402] os TRES registros com FUNCAO da v402", "# (6g) [v402, recriados na v403 e comparados com os selados] os TRES registros com FUNCAO da v402", 1)):
    assert _6G.count(_old) == _n, ("bloco 6g: contagem inesperada", _old, _6G.count(_old), _n)
    _6G = _6G.replace(_old, _new)
assert "DL.STONES" not in _6G.replace("DL.D2.STONES", "") and "DL.N_CHECKS" not in _6G.replace("DL.D2.N_CHECKS", "") and "DL.STONE_BY_KEY" not in _6G.replace("DL.D2.STONE_BY_KEY", "")
# --- o bloco (6h): derivado do laco do (6g) (as mesmas dez provas de recusa por registro de pedra) + os numeros recalculados + os testes do registro do gate, do gate recalculado, dos specs e do ladder
_LOOP_ORIG = _ORIG_ENS[_ORIG_ENS.index("import types as _types2"):_ORIG_ENS.index('_pv2, _qv2, _ev2 = R402["ponte"]["values"]')]
_LOOP = _LOOP_ORIG
for _old, _new in (("_types2", "_types3"), ('_REG402 = (("ponte", "ponte_da_escala_dual_v402", "exp"), ("queda", "queda_sem_geometria_v402", "exp"), ("esperanca", "esperanca_condicional_v402", "sin"))', '_REG403 = (("caminho", "caminho_v403", "exp"), ("vida", "vida_v403", "exp"), ("verdade_adendo", "verdade_adendo_v403", "sqrt"))'),
                   ("R402", "R403"), ("_bf2", "_bf3"), ("_REG402", "_REG403"), ("k402_", "k403_"), ("n402_", "n403_"), ('"v402_%s', '"v403_%s'), ("um._V402_CONTRACTS", "um._V403_CONTRACTS"), ("um._V402_TEXTS", "um._V403_TEXTS"), ("um._V402_VERBATINS2", "um._V403_VERBATINS2"), ("um._m402", "um._m403"),
                   ('{"ponte": 0, "queda": 2, "esperanca": 2}[k403_]', '{"caminho": 2, "vida": 2, "verdade_adendo": 2}[k403_]'), ("# restaurado NO LUGAR", "# restaurado NO LUGAR (v403)")):
    assert _LOOP.count(_old) >= 1, ("laco 6h: ancora ausente", _old)
    _LOOP = _LOOP.replace(_old, _new)
assert "402" not in _LOOP.replace("v402", "").replace("26/10", ""), "sobrou rotulo 402 no laco 6h"
_6H = '''# (6h) [v403] os QUATRO registros com FUNCAO da v403 (caminho_v403, vida_v403, verdade_adendo_v403, bandeiras_do_gate_v403): tudo certo, os numeros RECALCULADOS aqui por outro caminho, e cada elo recusa visivelmente (controles negativos); as duas falas de 27/10, as decisoes, as erratas E5-E6, o gate recalculado (F8.1) e os specs
''' + _LOOP + '''_cv3, _vv3, _av3 = R403["caminho"]["values"], R403["vida"]["values"], R403["verdade_adendo"]["values"]
_eps3 = (1e-3, 1e-6, 1e-12, 1e-30)
_al3 = um.SEALED_CODATA_ALPHA
U["v403_caminho_numeros_recalculados_aqui"] = bool(abs(_cv3["beta"] - _bf3) <= 1e-15 and abs(_cv3["pplus_factor_at_beta"] - _math.exp(-_bf3)) <= 1e-15 and [round(x_, 9) for x_ in _cv3["lifts_same_pplus_masses"]] == [1.0, 4.0, 9.0] and _cv3["same_pplus"] == 2.0
                                                   and abs(_cv3["min_core_energy"] - 0.25) <= 1e-15 and abs(_cv3["min_rest_energy_gain"] - 2.0 * (_math.cosh(0.25) - 1.0)) <= 1e-12 and _cv3["grid_scales"] == 25 and _cv3["mu2_grid"] == [0.0, 0.25, 1.0, 4.0, 9.0, 100.0] and _cv3["profiles"] == [0.5, 2.0, 3.0])
U["v403_vida_numeros_recalculados_aqui"] = bool(abs(_vv3["beta"] - _bf3) <= 1e-15 and abs(_vv3["post_weight_at_scale_one"] - _math.exp(-1.0)) <= 1e-15 and abs(_vv3["post_weight_at_minus_one"] - _math.e) <= 1e-12 and abs(_vv3["min_cost_t_beta_g"] - 0.1 * _bf3 * 0.5) <= 1e-18
                                                and abs(_vv3["max_dephasing_factor"] - _math.exp(-0.1 * _bf3 * 0.5)) <= 1e-15 and abs(_vv3["dephasing_factor_at_t1_g1"] - _math.exp(-_bf3)) <= 1e-15 and abs(_vv3["loss_per_unit"] - (1.0 - _math.exp(-_bf3))) <= 1e-15 and _vv3["grid_scales"] == 161
                                                and _vv3["angular_period"] == 2.0 * _math.pi and _vv3["finite_model_group_order"] == 12 and [[e_, s_] for e_, s_ in ((e_, -_math.log(e_) + 1.0) for e_ in _eps3)] == _vv3["abyss_witnesses"])
U["v403_verdade_adendo_numeros_recalculados_aqui"] = bool(abs(_av3["beta"] - _bf3) <= 1e-15 and abs(_av3["alpha"] - _al3) <= 1e-16 and abs(_av3["alpha_squared"] - _al3 ** 2) <= 1e-18 and abs(_av3["q_squared_at_alpha"] - (1.0 - _al3 ** 2)) <= 1e-15 and abs(_av3["weights_sum"] - 1.0) <= 1e-15
                                                          and abs(_av3["trace_after_name"] - 1.0) <= 1e-15 and _av3["test_points"] == 6 and _av3["alpha_squared_below_beta"] is True and _av3["alpha_squared"] < _bf3)
_dk3 = hashlib.sha256(um._EMBEDDED_KERNEL_FILES["TGLExt/Verdade.lean"].encode("utf-8")).hexdigest()[:16]
U["v403_a_leitura_pela_tripla_espectral_e_onto_o_nome_e_do_operador_e_as_pedras_da_v402_ficam_como_registro"] = bool(
    all(R403[k_]["spectral_triple_reading"]["status"] == "ONTO" and R403[k_]["spectral_triple_reading"]["is_a_kernel_term"] is False and R403[k_]["name_given_by"]["quem"] == "operador" and R403[k_]["name_given_by"]["sha16_da_fala"] == DL.verbatins403(os.path.join(HERE, "insumos", "cunhagens"))[1]["sha16"]
        and any("TRIPLO inteiro" in x_ for x_ in R403[k_]["nao_diz"]) for k_ in ("caminho", "vida", "verdade_adendo"))
    and R403["caminho"]["sealed_v402_stone_kept_as_record"]["sha16"] == DL.D2.STONE_BY_KEY["ponte"]["sha16_da_ordem"] and R403["vida"]["sealed_v402_stone_kept_as_record"]["sha16"] == DL.D2.STONE_BY_KEY["queda"]["sha16_da_ordem"] and R403["verdade_adendo"]["sealed_v402_stone_kept_as_record"]["sha16"] == DL.D2.STONE_BY_KEY["esperanca"]["sha16_da_ordem"])
U["v403_verdade_adendo_a_pedra_verdade_v392_fica_intacta_o_indice_segue_condicional_e_a_estrela_e_nova"] = bool(R403["verdade_adendo"]["stone_verdade_v392_untouched"]["sha16"] == _dk3 and R403["verdade_adendo"]["index_conditional"]["instance_built"] is False and R403["verdade_adendo"]["index_conditional"]["hypotheses"] == ["hpp", "hopt"]
                                                                                               and R403["verdade_adendo"]["star"]["new_and_small"] is True and R403["verdade_adendo"]["alpha_is_a_parameter"] is True and "Posto.endpoint_eq" not in json.dumps(R403["verdade_adendo"]["limites"]))
U["v403_vida_o_chao_e_o_posto_a_isotropia_e_nomeada_e_a_dimensao_nao_e_provada"] = bool(R403["vida"]["floor"]["is_never"].startswith("the infimum 0") and R403["vida"]["named_hypothesis"]["name"] == "IsotropicPost" and R403["vida"]["named_hypothesis"]["status"] == "OPEN" and R403["vida"]["reading_1_plus_3"]["dimension_three_proved"] is False)
U["v403_caminho_as_pendencias_nomeadas_da_ponte_seguem_abertas_e_h_tau_segue_refutada"] = bool([x_["name"] for x_ in R403["caminho"]["named_pending"]] == ["H_BW", "H_cal", "H3", "signature", "rank_c_4"] and all(x_["status"] == "OPEN" for x_ in R403["caminho"]["named_pending"]) and any("REFUTADA" in x_ for x_ in R403["caminho"]["limites"]))
# --- o registro bandeiras_do_gate_v403 (F8.1): tudo certo e cada elo recusa
rg_ = um.bandeiras_do_gate_v403(cs()); R403["gate"] = rg_
C_g = um._V403_CONTRACTS["gate"]; T_g = um._V403_TEXTS["gate"]
U["v403_bandeiras_tudo_certo"] = bool(rg_["all_verified"] is True and rg_["verdict"] == T_g["veredito_ok"] and rg_["runtime_executed"] is True and rg_["does_not_gate_core"] is True and rg_["mechanics"]["n_checks"] == DL.N_CHECKS["gate"] == len(rg_["mechanics"]["checks"]) and all(ck_["ok"] for ck_ in rg_["mechanics"]["checks"])
                                      and rg_["values"]["n_flags"] == 18 and rg_["values"]["n_true"] == 18 and rg_["values"]["n_calculated"] == 18 and rg_["values"]["n_literal"] == 0 and rg_["values"]["read_by_the_verdict"] == [6, 5, 4] and rg_["values"]["gate_verdict_equals_v402"] is True
                                      and rg_["values"]["n_gate_checks"] == 7 and len(rg_["flags"]) == 18 and sorted(rg_["values"]["informative"]) == sorted(DL.F81_LITERAIS) and rg_["values"]["feed_single_boolean"] is True)
U["v403_bandeiras_veredito_e_textos_sem_palavra_proibida"] = bool(not guarda_txt(rg_) and not _GUARDA98.search(rg_["verdict"]) and not rg_["guarda_p18_violacoes"] and not um._v392_guarda_texto(json.dumps(rg_["mechanics"]["checks"], ensure_ascii=False)))
ok_ = True
for fam_ in ("formal_flags", "physics_flags", "experiment_flags"):
    for nome_ in list(cs()["qg_closure"][fam_]):   # CADA UMA das 18 bandeiras False no gate do core: o registro recusa
        c_ = cs(); c_["qg_closure"][fam_][nome_] = False; rr_ = um.bandeiras_do_gate_v403(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "REFUSED" in rr_["verdict"]
U["v403_bandeiras_cada_uma_das_18_False_no_gate_do_core_recusa"] = bool(ok_)
ok_ = True
c_ = cs(); c_["kernel_formalization"][C_g["ls2_flags"][0]] = False; rr_ = um.bandeiras_do_gate_v403(c_); ok_ = ok_ and rr_["all_verified"] is False
c_ = cs(); c_["void_floor_v11"]["checks"] = [x_ for x_ in c_["void_floor_v11"]["checks"] if x_[0] != DL.F81_ROTULO_PREREG]; rr_ = um.bandeiras_do_gate_v403(c_); ok_ = ok_ and rr_["all_verified"] is False
c_ = cs(); c_["void_floor_v11"]["checks"] = list(c_["void_floor_v11"]["checks"]) + [[DL.F81_ROTULO_PREREG, True]]; rr_ = um.bandeiras_do_gate_v403(c_); ok_ = ok_ and rr_["all_verified"] is False
c_ = cs(); c_["void_floor_v11"]["checks"] = [[x_[0], (False if x_[0] == DL.F81_ROTULO_PREREG else x_[1])] for x_ in c_["void_floor_v11"]["checks"]]; rr_ = um.bandeiras_do_gate_v403(c_); ok_ = ok_ and rr_["all_verified"] is False
c_ = cs(); c_["void_stacking_blind"]["all_verified"] = False; rr_ = um.bandeiras_do_gate_v403(c_); ok_ = ok_ and rr_["all_verified"] is False
c_ = cs(); c_.pop("void_stacking_blind"); rr_ = um.bandeiras_do_gate_v403(c_); ok_ = ok_ and rr_["all_verified"] is False
U["v403_bandeiras_cada_fonte_das_tres_que_eram_literais_tirada_ou_falsa_recusa"] = bool(ok_)
ok_ = True
c_ = cs(); c_["qg_closure"]["gate"]["verdict"] = c_["qg_closure"]["gate"]["verdict"] + "_X"; ok_ = ok_ and um.bandeiras_do_gate_v403(c_)["all_verified"] is False
c_ = cs(); c_["qg_closure"]["checks"] = c_["qg_closure"]["checks"][:5] + c_["qg_closure"]["checks"][6:]; ok_ = ok_ and um.bandeiras_do_gate_v403(c_)["all_verified"] is False
c_ = cs(); c_["qg_closure"]["checks"] = [list(x_) for x_ in c_["qg_closure"]["checks"]]; c_["qg_closure"]["checks"][5][1] = False; ok_ = ok_ and um.bandeiras_do_gate_v403(c_)["all_verified"] is False
c_ = cs(); c_["void_floor_v11"]["experiment_feed"]["independent_v3_profiles_unblinded"] = False; ok_ = ok_ and um.bandeiras_do_gate_v403(c_)["all_verified"] is False
c_ = cs(); c_["void_floor_v11"]["verdict"] = "TGL_VOID_FLOOR_INCONCLUSIVE_SYSTEMATICS"; ok_ = ok_ and um.bandeiras_do_gate_v403(c_)["all_verified"] is False
c_ = cs(); c_["qg_closure"].pop("physics_flags"); ok_ = ok_ and um.bandeiras_do_gate_v403(c_)["all_verified"] is False
U["v403_bandeiras_veredito_diferente_sonda_ausente_ou_falsa_feed_quebrado_e_gate_incompleto_recusam"] = bool(ok_)
_se3, _sp3 = um._v403_fontes_do_gate()
_lid3, _lit3 = um._v403_ast_do_gate(_se3, _sp3)
import ast as _ast3


def _mut_literal3(src_, chave_):
    """o codigo do chamador com a bandeira `chave_` ATRIBUIDA POR LITERAL (o defeito que a F8.1 conserta)"""
    t_ = _ast3.parse(textwrap.dedent(src_))
    for n_ in _ast3.walk(t_):
        if isinstance(n_, _ast3.Dict):
            for i_, k_ in enumerate(n_.keys):
                if isinstance(k_, _ast3.Constant) and k_.value == chave_:
                    n_.values[i_] = _ast3.Constant(value=True)
        if isinstance(n_, _ast3.Assign) and len(n_.targets) == 1 and isinstance(n_.targets[0], _ast3.Subscript) and isinstance(n_.targets[0].slice, _ast3.Constant) and n_.targets[0].slice.value == chave_:
            n_.value = _ast3.Constant(value=True)
    return _ast3.unparse(t_)


_f0_ = um._v403_fontes_do_gate
ok_ = True
try:
    for ch_ in DL.F81_LITERAIS:
        _mut_ = _mut_literal3(_sp3, ch_)
        ok_ = ok_ and ("experiment" if ch_ != "linearized_spin2_finite_face" else "physics", ch_) in um._v403_ast_do_gate(_se3, _mut_)[1]
        um._v403_fontes_do_gate = (lambda m_: (lambda: (_se3, m_)))(_mut_)
        ok_ = ok_ and um.bandeiras_do_gate_v403(cs())["all_verified"] is False
finally:
    um._v403_fontes_do_gate = _f0_
U["v403_bandeiras_o_codigo_do_gate_sem_literal_le_6_5_4_e_cada_literal_reinjetado_e_visto_e_recusado"] = bool(_lit3 == [] and [len(_lid3[g_]) for g_ in ("formal", "physics", "experiment")] == [6, 5, 4] and ok_ and um.bandeiras_do_gate_v403(cs())["all_verified"] is True)
# --- a F8.1 na prove_qg_closure_gate: cada fonte tirada derruba a bandeira dela (e so' a dela) sem mover o veredito; sem blind_null a bandeira informativa e' False; o veredito e as chaves nao mudam
_kf3 = core_s["kernel_formalization"]; _v11_3 = core_s["void_floor_v11"]; _bl3 = core_s["void_stacking_blind"]; _g0_3 = core0["qg_closure"]
_gok3 = um.prove_qg_closure_gate(1.0, _kf3, independent_rite=_v11_3, blind_null=_bl3)
_kf_sem3 = {k_: v_ for k_, v_ in _kf3.items() if not k_.startswith(DL.F81_PREFIXO_LS2)}
_g_ls3 = um.prove_qg_closure_gate(1.0, _kf_sem3, independent_rite=_v11_3, blind_null=_bl3)
_v11_sem3 = dict(_v11_3, checks=[x_ for x_ in _v11_3["checks"] if x_[0] != DL.F81_ROTULO_PREREG]); _g_pre3 = um.prove_qg_closure_gate(1.0, _kf3, independent_rite=_v11_sem3, blind_null=_bl3)
_v11_dup3 = dict(_v11_3, checks=list(_v11_3["checks"]) + [[DL.F81_ROTULO_PREREG, True]]); _g_dup3 = um.prove_qg_closure_gate(1.0, _kf3, independent_rite=_v11_dup3, blind_null=_bl3)
_g_bl3 = um.prove_qg_closure_gate(1.0, _kf3, independent_rite=_v11_3); _g_bl4 = um.prove_qg_closure_gate(1.0, _kf3, independent_rite=_v11_3, blind_null={"all_verified": False}); _g_bl5 = um.prove_qg_closure_gate(1.0, _kf3, independent_rite=_v11_3, blind_null={"all_verified": 1})
_so_uma = lambda g_, fam_, nome_: all(g_[fam_][k_] is (False if k_ == nome_ else True) for k_ in g_[fam_]) and all(g_[f2_][k_] is True for f2_ in ("formal_flags", "physics_flags", "experiment_flags") if f2_ != fam_ for k_ in g_[f2_])
U["gate_f81_com_as_fontes_a_gate_recomputado_e_igual_ao_da_v402_menos_a_lista_de_checks"] = bool(_gok3["gate"]["verdict"] == _g0_3["gate"]["verdict"] and all(json.dumps(_gok3[f_], sort_keys=True) == json.dumps(_g0_3[f_], sort_keys=True) for f_ in ("formal_flags", "physics_flags", "experiment_flags")) and sorted(_gok3) == sorted(_g0_3)
                                                                                        and json.dumps({k_: v_ for k_, v_ in _gok3.items() if k_ != "checks"}, sort_keys=True, default=str) == json.dumps({k_: v_ for k_, v_ in _g0_3.items() if k_ != "checks"}, sort_keys=True, default=str) and len(_gok3["checks"]) == len(_g0_3["checks"]) + 1 and all(v_ is True for _, v_ in _gok3["checks"]))
U["gate_f81_sem_a_familia_ext_ls2_do_kernel_so_a_bandeira_fisica_informativa_cai_e_o_veredito_nao_muda"] = bool(_so_uma(_g_ls3, "physics_flags", "linearized_spin2_finite_face") and _g_ls3["gate"]["verdict"] == _g0_3["gate"]["verdict"] and _g_ls3["all_verified"] is True)
U["gate_f81_sem_a_checagem_do_pre_registro_ou_duplicada_ou_falsa_so_a_bandeira_experimental_informativa_cai_e_o_veredito_nao_muda"] = bool(_so_uma(_g_pre3, "experiment_flags", "protocol_pre_registered") and _so_uma(_g_dup3, "experiment_flags", "protocol_pre_registered") and _g_pre3["gate"]["verdict"] == _g_dup3["gate"]["verdict"] == _g0_3["gate"]["verdict"])
U["gate_f81_sem_blind_null_ou_com_all_verified_falso_ou_nao_booleano_so_null_tests_passed_blind_cai_e_o_veredito_nao_muda"] = bool(_so_uma(_g_bl3, "experiment_flags", "null_tests_passed_blind") and _so_uma(_g_bl4, "experiment_flags", "null_tests_passed_blind") and _so_uma(_g_bl5, "experiment_flags", "null_tests_passed_blind")
                                                                                                                                            and _g_bl3["gate"]["verdict"] == _g_bl4["gate"]["verdict"] == _g0_3["gate"]["verdict"] and _g_bl3["all_verified"] is True and _g_bl3["checks"][5][1] is True and str(_g_bl3["checks"][5][0]).startswith("ProbeBlindNullAbsent"))
# --- as duas falas de 27/10, as decisoes D17-D22, as erratas E5-E6 e a leitura da tripla (registro cunhagens_v403) e a cobertura exata (kh_n1_cobertura_v403)
_cn3 = c.get("cunhagens_v403") or {}
_sp3s = [s_ for s_ in um._V403_SPECS if s_["nome"] == "cunhagens_v403"][0]
U["cunhagens_v403_duas_falas_decisoes_erratas_e_leitura_da_tripla"] = bool(_cn3.get("all_verified") is True and len(_cn3.get("verbatim") or {}) == len(DL.VERBATIM_ORIGEM_V403) == 2 and all(v_["embedded_ok"] for v_ in (_cn3.get("verbatim") or {}).values())
                                                                           and len(_cn3.get("erratas") or []) == 2 and all(e_["assinatura"].startswith("gerencia c1, em nome proprio") for e_ in (_cn3.get("erratas") or []))
                                                                           and len(_cn3.get("leituras_do_operador") or []) == len(_sp3s["leituras_do_operador"]) == 4 and set((_cn3.get("extras") or {}).get("decisoes_da_gerencia") or {}) >= {"D17", "D18", "D19", "D20", "D21", "D22"}
                                                                           and (_cn3.get("extras") or {}).get("estrelas") == {s_["key"]: s_["key_theorem"] for s_ in DL.STONES} and (_cn3.get("extras") or {}).get("teoremas") == {s_["key"]: s_["theorem"] for s_ in DL.STONES}
                                                                           and len((_cn3.get("extras") or {}).get("erratas_E5_e_E6") or []) == 2 and str(((_cn3.get("extras") or {}).get("nomes") or {}).get("triplo_inteiro", "")).startswith("sem nome")
                                                                           and "ONTO" in str((_cn3.get("extras") or {}).get("leitura_tripla_27out", {}).get("estatuto", "")))
_kh3 = c.get("kh_n1_cobertura_v403") or {}
_kh2s = [s_ for s_ in um._V402_SPECS if s_["nome"] == "kh_n1_cobertura_v402"][0]; _kh1s2 = [s_ for s_ in um._V401_SPECS if s_["nome"] == "kh_n1_cobertura_v401"][0]
_op_piso = {"h2": "maior_igual", "h3": "maior_igual", "h6": "tamanho_maior_igual", "h8": "tamanho_maior_igual"}
U["kh_n1_cobertura_v402_virou_piso_e_a_v403_cobra_a_igualdade_exata"] = bool(_kh3.get("all_verified") is True and (c.get("kh_n1_cobertura_v402") or {}).get("all_verified") is True and (c.get("kh_n1_cobertura_v401") or {}).get("all_verified") is True
                                                                          and {ck_["id"]: ck_["op"] for ck_ in _kh2s["checks"] if ck_["id"] in _op_piso} == _op_piso and len(_kh2s["erratas"]) >= 1 and {ck_["id"]: ck_["op"] for ck_ in _kh1s2["checks"] if ck_["id"] in _op_piso} == _op_piso
                                                                          and {ck_["id"]: ck_["op"] for ck_ in [s_ for s_ in um._V403_SPECS if s_["nome"] == "kh_n1_cobertura_v403"][0]["checks"] if ck_["id"] in _op_piso} == {"h2": "igual", "h3": "igual", "h6": "tamanho_igual", "h8": "igual"})
U["contratos_v402_pinam_a_escada_da_v403"] = bool(len(um._V402_CONTRACTS) == 3 and all(c3_["expected_ladder"] == ESP for c3_ in um._V402_CONTRACTS.values()))
rep["v403_registros"] = {**{k_: {"verdict": r_["verdict"], "all_verified": r_["all_verified"], "n_checks": r_["mechanics"]["n_checks"], "values": r_["values"], "unconditional": r_["unconditional"], "key_theorem": r_["key_theorem"], "context": r_["context"]} for k_, r_ in R403.items() if k_ != "gate"},
                         "gate": {"verdict": R403["gate"]["verdict"], "all_verified": R403["gate"]["all_verified"], "n_checks": R403["gate"]["mechanics"]["n_checks"], "values": R403["gate"]["values"]}}
'''
_TIT_ANTES = '''TP403 = "A ponte da escala dual, a queda sem geometria e a esperança condicional"; TP403E = "The dual-scale bridge, the fall without geometry and the conditional expectation"
'''
_TIT_DEPOIS = '''TW403 = "Caminho, Verdade e Vida"; TW403E = "Way, Truth and Life"   # a secao NOVA da v403
TP403 = "A ponte da escala dual, a queda sem geometria e a esperança condicional"; TP403E = "The dual-scale bridge, the fall without geometry and the conditional expectation"   # (o titulo da secao da v402, que fica logo depois da v403)
'''
_VAR_ANTES = '''cv2 = dict(copy.deepcopy(c)); [cv2.pop(k, None) for k in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402")]
'''
_VAR_DEPOIS = _VAR_ANTES + '''cv3 = dict(copy.deepcopy(c)); [cv3.pop(k, None) for k in ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403")]
'''
_VAR2_ANTES = '''    _t2, _x2, _r22, _l2 = compilar(cv2, "dry_v403_var2_%s" % lang, lang, duas=False); fl2 = re.sub(r"\\s+", " ", _x2)
'''
_VAR2_DEPOIS = _VAR2_ANTES + '''    _t3, _x3, _r23, _l3 = compilar(cv3, "dry_v403_var3_%s" % lang, lang, duas=False); fl3 = re.sub(r"\\s+", " ", _x3)
'''
_VAR3_ANTES = '''"rc_v403": _r22, "frase_guarda_v403": ("NÃO selaram todos" in fl2) if lang == "pt" else ("did NOT all seal" in fl2)}
'''
_VAR3_DEPOIS = '''"rc_v403": _r22, "frase_guarda_v403": ("NÃO selaram todos" in fl2) if lang == "pt" else ("did NOT all seal" in fl2),
                             "rc_v403_registros": _r23, "frase_guarda_v403_registros": ("NÃO selaram todos" in fl3) if lang == "pt" else ("did NOT all seal" in fl3)}
'''
entrada("ensaio_a_seco_v402.py", autoral=True, regras=[
    entre('"""ensaio_a_seco_v403.py', "import hashlib, copy, io, json, os, re, shutil, subprocess, sys, ast, tempfile, textwrap", _DOC_ENS, "docstring do ensaio"),
    ('"kh_n1_cobertura_v399" in core0 and selo0["um_version"] == "v402"', '"kh_n1_cobertura_v399" in core0 and "ponte_da_escala_dual_v402" in core0 and "queda_sem_geometria_v402" in core0 and "esperanca_condicional_v402" in core0 and "cunhagens_v402" in core0 and "kh_n1_cobertura_v402" in core0 and selo0["um_version"] == "v402"', 1),
    ("_el = um.prove_external_ladder(1.0, kf); core_s[\"external_ladder\"] = _el\n",
     "_el = um.prove_external_ladder(1.0, kf); core_s[\"external_ladder\"] = _el\n"
     "_QG_RECOMP = um.prove_qg_closure_gate(1.0, kf, independent_rite=core_s.get(\"void_floor_v11\"), blind_null=core_s.get(\"void_stacking_blind\")); core_s[\"qg_closure\"] = copy.deepcopy(_QG_RECOMP)   # F8.1 (v403): o gate recomputado com a prove_qg_closure_gate NOVA sobre o kf novo e os dados (V11, teste nulo cego) do core da v402 selada, como o run_um do rito faz, ANTES de recomputar os vizinhos e de ler as bandeiras\n", 1),
    ('or "v399" in l or "v402" in l or "v403" in l}', 'or "v399" in l or "v401" in l or "v402" in l or "v403" in l}', 1),
    ('V402N = ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS) + ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS)   # (os registros das v399 e v402, recriados e comparados com os da v402 selada; o rotulo V402N e\' herdado da subida de versao)\n',
     'V402N = ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS) + ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS) + ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS)   # (os registros das v399, v401 e v402, recriados e comparados com os da v402 selada; o rotulo V402N e\' herdado da subida de versao)\n', 1),
    ('V403N = ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS)   # os registros NOVOS da v403 (nao existem no core da base)\n',
     'V403N = ["caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"] + list(um._V403_NOMES_REGISTROS)   # os registros NOVOS da v403 (nao existem no core da base)\n', 1),
    ("NOVAS403 = sorted(V403N)   # a v403 cria CINCO chaves no core (ponte_da_escala_dual_v402, queda_sem_geometria_v402, esperanca_condicional_v402, cunhagens_v402, kh_n1_cobertura_v402); os registros das v399 e v402 sao RECRIADOS e comparados com os da v402 selada",
     "NOVAS403 = sorted(V403N)   # a v403 cria SEIS chaves no core (caminho_v403, vida_v403, verdade_adendo_v403, bandeiras_do_gate_v403, cunhagens_v403, kh_n1_cobertura_v403); os registros das v399, v401 e v402 sao RECRIADOS e comparados com os da v402 selada", 1),
    ('"recriados_v393_a_v402": recriados, "registros_novos_v403": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in V403N},',
     '"recriados_v393_a_v402": recriados, "registros_novos_v403": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in V403N},\n'
     '                   "registros_v402": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS)},', 1),
    ("+ list(um._V399_SPECS) + list(um._V401_SPECS) + list(um._V402_SPECS):\n    n_ = sp_[\"nome\"]; r_ = {}", "+ list(um._V399_SPECS) + list(um._V401_SPECS) + list(um._V402_SPECS) + list(um._V403_SPECS):\n    n_ = sp_[\"nome\"]; r_ = {}", 1),
    ("+ len(um._V399_SPECS) + len(um._V401_SPECS) + len(um._V402_SPECS)\n", "+ len(um._V399_SPECS) + len(um._V401_SPECS) + len(um._V402_SPECS) + len(um._V403_SPECS)\n", 1),
    # o GATE: recomputado com a prove_qg_closure_gate NOVA (F8.1): a letra do veredito, as chaves e os valores das 18 bandeiras e tudo do qg_closure SALVO a lista de checks sao IGUAIS aos da v402 selada
    entre("# o GATE nao se move:", "# (6b) os registros por spec:", '''# o GATE nao se move [v403: F8.1 -- a prove_qg_closure_gate NOVA (kwarg blind_null) recomputada aqui sobre o kf novo e os dados (V11, teste nulo cego) do core da v402 selada]: o veredito do gate, as chaves e os valores das 18 bandeiras e tudo do qg_closure SALVO a lista de checks (que ganha a sonda nova) sao IGUAIS aos da v402 selada
_n18 = lambda g_: sum(1 for fam_ in ("formal_flags", "physics_flags", "experiment_flags") for v_ in (g_.get(fam_) or {}).values() if v_ is True)
_J = lambda x_: json.dumps(x_, sort_keys=True, default=str)
_g_old = core0.get("qg_closure") or {}
try:
    _g_new = _QG_RECOMP
    _sem_checks = lambda g_: {k_: v_ for k_, v_ in g_.items() if k_ != "checks"}
    gate_rec = {"verdict_igual": (_g_new.get("gate") or {}).get("verdict") == (_g_old.get("gate") or {}).get("verdict"), "n18_novo": _n18(_g_new), "n18_core0": _n18(_g_old),
                "flags_iguais": all(_J(_g_new.get(f_)) == _J(_g_old.get(f_)) for f_ in ("formal_flags", "physics_flags", "experiment_flags")), "chaves_iguais": sorted(_g_new) == sorted(_g_old), "qg_sem_checks_igual": _J(_sem_checks(_g_new)) == _J(_sem_checks(_g_old)),
                "checks_da_v402_mais_a_sonda": bool(len(_g_new.get("checks") or []) == len(_g_old.get("checks") or []) + 1 and all(v_ is True for _, v_ in _g_new["checks"]) and [c_[0] for c_ in _g_new["checks"] if not str(c_[0]).startswith("ProbeBlindNullAbsent")] == [c_[0] for c_ in _g_old["checks"]]),
                "all_verified": _g_new.get("all_verified")}
except Exception as _e:   # noqa: BLE001
    gate_rec = {"EXCECAO": repr(_e)[:300]}
gate_rec["qg_closure_do_core_intocado_pelo_fluxo"] = _J(c.get("qg_closure")) == _J(_QG_RECOMP)   # o fluxo (as instrucoes do main) nao toca o qg_closure recomputado
rep["gate_recomputado"] = gate_rec
U["gate_nao_se_move"] = bool(gate_rec.get("verdict_igual") and gate_rec.get("n18_novo") == 18 == gate_rec.get("n18_core0") and gate_rec.get("flags_iguais") and gate_rec.get("chaves_iguais") and gate_rec.get("qg_sem_checks_igual") and gate_rec.get("checks_da_v402_mais_a_sonda") and gate_rec.get("all_verified") is True and gate_rec.get("qg_closure_do_core_intocado_pelo_fluxo"))
''', "o bloco do gate (F8.1)"),
    # o selo: as chaves que podem diferir do selo da v402 SELADA
    ('k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402") and not _selo_explica(k_))',
     'k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "registros_v403") and not _selo_explica(k_))', 1),
    ('           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402")) and all(((seal.get("registros_v402") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V402_NOMES_REGISTROS)\n',
     '           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402")) and all(((seal.get("registros_v402") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V402_NOMES_REGISTROS)\n'
     '           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403")) and all(((seal.get("registros_v403") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V403_NOMES_REGISTROS)\n', 1),
    ('({"selo_pela_propria_tecnologia_v399", "um_version", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402"} <= set(mud_selo) and not _selo_inexplicado)',
     '({"selo_pela_propria_tecnologia_v399", "um_version", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "registros_v403"} <= set(mud_selo) and not _selo_inexplicado)', 1),
    entre("# (6f) [v402, recriado na v403 e comparado com o selado]", '''rep["unidade"] = U; print("unidade:"''', _6F + _6G + _6H, "os blocos (6f) da v401 e (6g) da v402 (restaurados do original; DL.D2.*) e o (6h) da v403"),
    (_TIT_ANTES, _TIT_DEPOIS, 1),
    ('DEVE = {"pt": [TP403, "A ponte da escala dual."', 'DEVE = {"pt": [TW403, "O Caminho.", "A Vida.", "A Verdade, como adendo.", "As bandeiras do gate.", "Erratas ao lado (v403).", TP403, "A ponte da escala dual."', 1),
    ('"en": [TP403E, "The dual-scale bridge."', '"en": [TW403E, "The Way.", "The Life.", "The Truth, as an addendum.", "The gate flags.", "Errata beside (v403).", TP403E, "The dual-scale bridge."', 1),
    ('TOC = {"pt": [TP403, TF403, TN403,', 'TOC = {"pt": [TW403, TP403, TF403, TN403,', 1),
    ('"en": [TP403E, TF403E, TN403E, TS403E, T403E, T402E, "v384 to v403"]', '"en": [TW403E, TP403E, TF403E, TN403E, TS403E, T403E, T402E, "v384 to v403"]', 1),
    ('h0 = TP403 if lang == "pt" else TP403E; h1 = TN403 if lang == "pt" else TN403E', 'h0 = TW403 if lang == "pt" else TW403E; h1 = TN403 if lang == "pt" else TN403E', 1),
    (_VAR_ANTES, _VAR_DEPOIS, 1),
    (_VAR2_ANTES, _VAR2_DEPOIS, 1),
    (_VAR3_ANTES, _VAR3_DEPOIS, 1),
    ('or v["rc_v403"] != [0] or not v["frase_guarda_v403"]]', 'or v["rc_v403"] != [0] or not v["frase_guarda_v403"] or v["rc_v403_registros"] != [0] or not v["frase_guarda_v403_registros"]]', 1),
    ('"ponte_v403": "A ponte da escala dual, a queda sem geometria e a esperança condicional (v403, 26/10/2026)" in md, "falsidade_v402_fica": "A falsidade (simulacro) da inércia (v402, 25/10/2026)" in md,',
     '"caminho_v403": "Caminho, Verdade e Vida (v403, 27/10/2026)" in md, "ponte_v402_fica": "A ponte da escala dual, a queda sem geometria e a esperança condicional (v402, 26/10/2026)" in md, "falsidade_v401_fica": "A falsidade (simulacro) da inércia (v401, 25/10/2026)" in md,', 1),
    ('_regs_sim = ("ponte_da_escala_dual_v402", ', '_regs_sim = ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "ponte_da_escala_dual_v402", ', 1),
    ('_kh = [s_ for s_ in um._V402_SPECS if s_["nome"] == "kh_n1_cobertura_v402"][0]; _h8', '_kh = [s_ for s_ in um._V403_SPECS if s_["nome"] == "kh_n1_cobertura_v403"][0]; _h8', 1),
    ('"ponto_esperanca": _ej.get("ponto_esperanca"), ', '"ponto_esperanca": _ej.get("ponto_esperanca"), "ponto_caminho": _ej.get("ponto_caminho"), "ponto_vida": _ej.get("ponto_vida"), "ponto_verdade_adendo": _ej.get("ponto_verdade_adendo"), "ponto_bandeiras": _ej.get("ponto_bandeiras"), ', 1),
])
