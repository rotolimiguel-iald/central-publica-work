# -*- coding: utf-8 -*-
# regras (lote C) de derivar_encanamento_v406.py: o ENSAIO (simular a arvore do Nos, exame dos pontos de chamada, ensaio a seco, guardas estaticas da Bancada). ORIGEM v405 FINAL (mapa 403 -> 405, 405 -> 406).
# A base mecanica sobe da v405 FINAL; a logica NOVA da v406 (os OITO registros com funcao, os specs v406, as oito pedras) entra como regras de contagem exata. Os blocos que tratam dos registros da v401, da v402, da v403 e da v405 (projecao_transversal_v404, jo8v32_v404, f2b_errata_v404)
# voltam do arquivo ORIGINAL da v405 sem subida de versao (a semantica deles e' a da v405: eles agora sao RECRIADOS e comparados com os da v405 selada; DL.X -> DL.D4.X para os nomes que a v406 sobrescreve).
# Escrito pela ferramenta Write (as barras invertidas e os apostrofos nao passam pelo heredoc).
import importlib.util as _ilu
CH_ = os.path.dirname(HERE)
_ORIG_ENS = open(os.path.join(CH_, "v405", "ensaio_a_seco_v405.py"), encoding="utf-8").read()
_ORIG_EXA = open(os.path.join(CH_, "v405", "exame_pontos_v405.py"), encoding="utf-8").read()
_DL5 = _ilu.spec_from_file_location("delta_v406_regras", os.path.join(HERE, "delta_v406.py")); DL5 = _ilu.module_from_spec(_DL5); _DL5.loader.exec_module(DL5)
_DL4 = DL5.D4
# os nomes de DL que a v406 SOBRESCREVE (ou cria) e que o texto original da v405 usa como "os da v405": viram DL.D4.<nome> nos blocos que RECRIAM os registros da v405
NOMES_SOBRESCRITOS = sorted(n_ for n_ in vars(_DL4) if not n_.startswith("__") and n_ in vars(DL5) and getattr(DL5, n_) is not getattr(_DL4, n_) and n_ not in ("D4", "D3", "D2", "D1", "D0", "D9", "HERE", "V405", "V403", "V402", "V401", "V400", "V399", "C", "WK", "CENTRAL"))


def para_d4(txt_):
    """no texto ORIGINAL da v405: `DL.<nome>` -> `DL.D4.<nome>` para cada nome que a v406 sobrescreve (os blocos recriam os registros da v405 com os dados DA v405)."""
    import re as _re
    for n_ in sorted(NOMES_SOBRESCRITOS, key=len, reverse=True):
        txt_ = _re.sub(r"\bDL\.%s\b" % n_, "DL.D4." + n_, txt_)
    return txt_


_REG406 = ["ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405"]
_CH406 = "; ".join("um.%s(core)" % n_ for n_ in _REG406)
_LS406 = ", ".join('"%s"' % n_ for n_ in _REG406 + ["cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405"])

# ------------------------------------------------------------------------------------------- simular a arvore do Nos: mais os oito registros (chamados no main logo depois do jo8v32_v404) e os specs da v406
entrada("simular_arvore_do_nos_v405.py", autoral=True, regras=[
    ("(mais os quatro registros com funcao da v405 e os tres da v406). Molde:", "(mais os quatro registros com funcao da v403, os tres da v405 e os oito da v406). Molde:", 1),
    ("um.projecao_transversal_v404(core); um.jo8v32_v404(core); um.f2b_errata_v404(core)   # (na fractalizacao", "um.projecao_transversal_v404(core); um.jo8v32_v404(core); um.f2b_errata_v404(core); " + _CH406 + "   # (na fractalizacao", 1),
    ("um._v403_rodar_specs(core); um._v404_rodar_specs(core)   # (v397:", "um._v403_rodar_specs(core); um._v404_rodar_specs(core); um._v405_rodar_specs(core)   # (v397:", 1),
    ('for k in ("projecao_transversal_v404", "jo8v32_v404",', "for k in (" + _LS406 + ', "projecao_transversal_v404", "jo8v32_v404",', 1),
])

# ------------------------------------------------------------------------------------------- exame dos pontos de chamada: os OITO pontos novos, em ordem, logo depois do bloco do jo8v32_v404
_BLOCO_PONTOS406 = r'''# (4a-v406d) os PONTOS DE CHAMADA REAIS dos OITO registros de pedra da v406: oito instrucoes do main (cada uma um `try`), em ordem, logo depois de `_nan405 = float("nan")`, que vem IMEDIATAMENTE depois do jo8v32_v404, na fractalizacao do Um
_i406n = [i for i, s_ in enumerate(unp) if s_.startswith("_nan405 = float(")]
_i406j = [i for i, s_ in enumerate(unp) if "jo8v32_v404(core)" in s_]
assert len(_i406n) == 1 and len(_i406j) == 1 and _i406n[0] == _i406j[0] + 1, ("o ponto da v406 nao vem logo depois do jo8v32_v404", _i406n, _i406j)
for _k406, s406_ in enumerate(DL.STONES):
    nome_ = "v406_" + s406_["key"]; fn_ = DL.REGISTRO_DE_PEDRA[s406_["key"]]
    ii_ = [i for i, s_ in enumerate(unp) if fn_ + "(core)" in s_]
    assert len(ii_) == 1 and ii_[0] == _i406n[0] + 1 + _k406, ("a instrucao do main que chama %s nao e' unica ou nao vem na ordem das pedras" % fn_, ii_, _i406n)
    ii_ = ii_[0]
    R["ponto_" + nome_] = {"indice_no_main": ii_, "linha": main.body[ii_].lineno, "antes_do_bloco_v393": ii_ < i0, "instrucao_anterior": unp[ii_ - 1][:160].replace("\n", " | ")}
    builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[_i406n[0]], main.body[ii_]], type_ignores=[])), "<main:%s>" % fn_, "exec"), g); err_ = None
    except Exception as e:
        import traceback; err_ = repr(e) + traceback.format_exc()[-900:]
    finally:
        stdout_ = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
    r_ = core.get(fn_) or {}
    R["ponto_" + nome_].update({"erro": err_, "stdout": stdout_.splitlines(), "avisos": [l for l in stdout_.splitlines() if "AVISO" in l or "RECUSA" in l], "verdict": r_.get("verdict"), "all_verified": r_.get("all_verified"),
                                "mecanica": {"passed": (r_.get("mechanics") or {}).get("passed"), "n_checks": (r_.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (r_.get("unconditional") or {}).get("in_kernel"),
                                "estrela_in_kernel": (r_.get("key_theorem") or {}).get("in_kernel"), "contexto_ok": (r_.get("context") or {}).get("ok"), "beta_ok": r_.get("beta_ok")})
    out["core." + fn_] = {"all_verified": r_.get("all_verified"), "verdict": str(r_.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((r_.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
'''
_FALSOS406 = r'''for s406_ in DL.STONES:
    pp406d_ = R["ponto_v406_" + s406_["key"]]
    if (pp406d_.get("erro") or pp406d_.get("avisos") or pp406d_.get("all_verified") is not True or not pp406d_.get("antes_do_bloco_v393") or pp406d_.get("unconditional_in_kernel") is not True or pp406d_.get("estrela_in_kernel") is not True
            or pp406d_.get("contexto_ok") is not True or pp406d_.get("beta_ok") is not True or (pp406d_.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS[s406_["key"]]): falsos.append("ponto_v406_" + s406_["key"])
'''
_SELO406_EXAME = ''.join(''',
                 "%s": {x: (seal.get("%s") or {}).get(x) for x in ("verdict", "all_verified")}''' % (n_, n_) for n_ in _REG406) + ''',
                 "registros_v405": {n_: ((seal.get("registros_v405") or {}).get(n_) or {}).get("all_verified") for n_ in um._V405_NOMES_REGISTROS}'''
entrada("exame_pontos_v405.py", autoral=True, regras=[
    ('# (4a\') o PONTO DE CHAMADA REAL do teste_de_veracidade_fase9_v397 (v397):', _BLOCO_PONTOS406 + '# (4a\') o PONTO DE CHAMADA REAL do teste_de_veracidade_fase9_v397 (v397):', 1),
    ('                   "v406_projecao_jo8v32_f2b": [k for k in ["projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404"] + list(um._V404_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n',
     '                   "v406_projecao_jo8v32_f2b": [k for k in ["projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404"] + list(um._V404_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n'
     '                   "v406_oito_pedras": [k for k in list(um._V405_REGISTROS_FUNCAO) + list(um._V405_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n', 1),
    ('"f2b_errata_v404": {x: (seal.get("f2b_errata_v404") or {}).get(x) for x in ("verdict", "all_verified", "F2b_status_now")}, "registros_v404": {n_: ((seal.get("registros_v404") or {}).get(n_) or {}).get("all_verified") for n_ in um._V404_NOMES_REGISTROS}',
     '"f2b_errata_v404": {x: (seal.get("f2b_errata_v404") or {}).get(x) for x in ("verdict", "all_verified", "F2b_status_now")}, "registros_v404": {n_: ((seal.get("registros_v404") or {}).get(n_) or {}).get("all_verified") for n_ in um._V404_NOMES_REGISTROS}' + _SELO406_EXAME, 1),
    ('or pp406c_.get("contexto_ok") is not True or pp406c_.get("beta_ok") is not True or (pp406c_.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS[nome_]): falsos.append("ponto_" + nome_)\n',
     'or pp406c_.get("contexto_ok") is not True or pp406c_.get("beta_ok") is not True or (pp406c_.get("mecanica") or {}).get("n_checks") != DL.D4.N_CHECKS[nome_]): falsos.append("ponto_" + nome_)\n', 1),
    ('(pf2_.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS["f2b"]', '(pf2_.get("mecanica") or {}).get("n_checks") != DL.D4.N_CHECKS["f2b"]', 1),
    ('pv = R["ponto_veracidade"]\n', _FALSOS406 + 'pv = R["ponto_veracidade"]\n', 1),
    ('+ ["caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"] + list(um._V403_NOMES_REGISTROS):\n    core.pop(n_, None)   # o fluxo os recria; comparam-se depois com os do core0',
     '+ ["caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"] + list(um._V403_NOMES_REGISTROS) + ["projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404"] + list(um._V404_NOMES_REGISTROS):\n    core.pop(n_, None)   # o fluxo os recria; comparam-se depois com os do core0', 1),
])

# ------------------------------------------------------------------------------------------- as guardas estaticas da Bancada: o mutante m6 usa um alvo errado que NAO e' o da v406
entrada("guardas_estaticas_bancada_v405.py", autoral=True, regras=[])   # o mutante m6 sobe para o alvo v405, que nao e o da v406 (o que ele cobra); o sandbox curto segue vb21 pela escolha da v406

# ------------------------------------------------------------------------------------------- o ENSAIO A SECO (as regras do ensaio entram no lote C2: derivar_encanamento_v406_regrasC2_ensaio.py)
