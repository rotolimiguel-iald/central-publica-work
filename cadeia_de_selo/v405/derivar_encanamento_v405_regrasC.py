# -*- coding: utf-8 -*-
# regras (lote C) de derivar_encanamento_v405.py: o ENSAIO (simular a arvore do Nos, exame dos pontos de chamada, ensaio a seco, guardas estaticas da Bancada). ORIGEM v404 FINAL (mapa 403 -> 404, 404 -> 405).
# A base mecanica sobe da v404 FINAL; a logica NOVA da v405 (os OITO registros com funcao, os specs v405, as oito pedras) entra como regras de contagem exata. Os blocos que tratam dos registros da v401, da v402, da v403 e da v404 (projecao_transversal_v404, jo8v32_v404, f2b_errata_v404)
# voltam do arquivo ORIGINAL da v404 sem subida de versao (a semantica deles e' a da v404: eles agora sao RECRIADOS e comparados com os da v404 selada; DL.X -> DL.D4.X para os nomes que a v405 sobrescreve).
# Escrito pela ferramenta Write (as barras invertidas e os apostrofos nao passam pelo heredoc).
import importlib.util as _ilu
CH_ = os.path.dirname(HERE)
_ORIG_ENS = open(os.path.join(CH_, "v404", "ensaio_a_seco_v404.py"), encoding="utf-8").read()
_ORIG_EXA = open(os.path.join(CH_, "v404", "exame_pontos_v404.py"), encoding="utf-8").read()
_DL5 = _ilu.spec_from_file_location("delta_v405_regras", os.path.join(HERE, "delta_v405.py")); DL5 = _ilu.module_from_spec(_DL5); _DL5.loader.exec_module(DL5)
_DL4 = DL5.D4
# os nomes de DL que a v405 SOBRESCREVE (ou cria) e que o texto original da v404 usa como "os da v404": viram DL.D4.<nome> nos blocos que RECRIAM os registros da v404
NOMES_SOBRESCRITOS = sorted(n_ for n_ in vars(_DL4) if not n_.startswith("__") and n_ in vars(DL5) and getattr(DL5, n_) is not getattr(_DL4, n_) and n_ not in ("D4", "D3", "D2", "D1", "D0", "D9", "HERE", "V404", "V403", "V402", "V401", "V400", "V399", "C", "WK", "CENTRAL"))


def para_d4(txt_):
    """no texto ORIGINAL da v404: `DL.<nome>` -> `DL.D4.<nome>` para cada nome que a v405 sobrescreve (os blocos recriam os registros da v404 com os dados DA v404)."""
    import re as _re
    for n_ in sorted(NOMES_SOBRESCRITOS, key=len, reverse=True):
        txt_ = _re.sub(r"\bDL\.%s\b" % n_, "DL.D4." + n_, txt_)
    return txt_


_REG405 = ["ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405"]
_CH405 = "; ".join("um.%s(core)" % n_ for n_ in _REG405)
_LS405 = ", ".join('"%s"' % n_ for n_ in _REG405 + ["cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405"])

# ------------------------------------------------------------------------------------------- simular a arvore do Nos: mais os oito registros (chamados no main logo depois do jo8v32_v404) e os specs da v405
entrada("simular_arvore_do_nos_v404.py", autoral=True, regras=[
    ("(mais os quatro registros com funcao da v404 e os tres da v405). Molde:", "(mais os quatro registros com funcao da v403, os tres da v404 e os oito da v405). Molde:", 1),
    ("um.projecao_transversal_v404(core); um.jo8v32_v404(core); um.f2b_errata_v404(core)   # (na fractalizacao", "um.projecao_transversal_v404(core); um.jo8v32_v404(core); um.f2b_errata_v404(core); " + _CH405 + "   # (na fractalizacao", 1),
    ("um._v403_rodar_specs(core); um._v404_rodar_specs(core)   # (v397:", "um._v403_rodar_specs(core); um._v404_rodar_specs(core); um._v405_rodar_specs(core)   # (v397:", 1),
    ('for k in ("projecao_transversal_v404", "jo8v32_v404",', "for k in (" + _LS405 + ', "projecao_transversal_v404", "jo8v32_v404",', 1),
])

# ------------------------------------------------------------------------------------------- exame dos pontos de chamada: os OITO pontos novos, em ordem, logo depois do bloco do jo8v32_v404
_BLOCO_PONTOS405 = r'''# (4a-v405d) os PONTOS DE CHAMADA REAIS dos OITO registros de pedra da v405: oito instrucoes do main (cada uma um `try`), em ordem, logo depois de `_nan405 = float("nan")`, que vem IMEDIATAMENTE depois do jo8v32_v404, na fractalizacao do Um
_i405n = [i for i, s_ in enumerate(unp) if s_.startswith("_nan405 = float(")]
_i405j = [i for i, s_ in enumerate(unp) if "jo8v32_v404(core)" in s_]
assert len(_i405n) == 1 and len(_i405j) == 1 and _i405n[0] == _i405j[0] + 1, ("o ponto da v405 nao vem logo depois do jo8v32_v404", _i405n, _i405j)
for _k405, s405_ in enumerate(DL.STONES):
    nome_ = "v405_" + s405_["key"]; fn_ = DL.REGISTRO_DE_PEDRA[s405_["key"]]
    ii_ = [i for i, s_ in enumerate(unp) if fn_ + "(core)" in s_]
    assert len(ii_) == 1 and ii_[0] == _i405n[0] + 1 + _k405, ("a instrucao do main que chama %s nao e' unica ou nao vem na ordem das pedras" % fn_, ii_, _i405n)
    ii_ = ii_[0]
    R["ponto_" + nome_] = {"indice_no_main": ii_, "linha": main.body[ii_].lineno, "antes_do_bloco_v393": ii_ < i0, "instrucao_anterior": unp[ii_ - 1][:160].replace("\n", " | ")}
    builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[_i405n[0]], main.body[ii_]], type_ignores=[])), "<main:%s>" % fn_, "exec"), g); err_ = None
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
_FALSOS405 = r'''for s405_ in DL.STONES:
    pp405d_ = R["ponto_v405_" + s405_["key"]]
    if (pp405d_.get("erro") or pp405d_.get("avisos") or pp405d_.get("all_verified") is not True or not pp405d_.get("antes_do_bloco_v393") or pp405d_.get("unconditional_in_kernel") is not True or pp405d_.get("estrela_in_kernel") is not True
            or pp405d_.get("contexto_ok") is not True or pp405d_.get("beta_ok") is not True or (pp405d_.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS[s405_["key"]]): falsos.append("ponto_v405_" + s405_["key"])
'''
_SELO405_EXAME = ''.join(''',
                 "%s": {x: (seal.get("%s") or {}).get(x) for x in ("verdict", "all_verified")}''' % (n_, n_) for n_ in _REG405) + ''',
                 "registros_v405": {n_: ((seal.get("registros_v405") or {}).get(n_) or {}).get("all_verified") for n_ in um._V405_NOMES_REGISTROS}'''
entrada("exame_pontos_v404.py", autoral=True, regras=[
    ('# (4a\') o PONTO DE CHAMADA REAL do teste_de_veracidade_fase9_v397 (v397):', _BLOCO_PONTOS405 + '# (4a\') o PONTO DE CHAMADA REAL do teste_de_veracidade_fase9_v397 (v397):', 1),
    ('                   "v405_projecao_jo8v32_f2b": [k for k in ["projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404"] + list(um._V404_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n',
     '                   "v405_projecao_jo8v32_f2b": [k for k in ["projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404"] + list(um._V404_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n'
     '                   "v405_oito_pedras": [k for k in list(um._V405_REGISTROS_FUNCAO) + list(um._V405_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n', 1),
    ('"f2b_errata_v404": {x: (seal.get("f2b_errata_v404") or {}).get(x) for x in ("verdict", "all_verified", "F2b_status_now")}, "registros_v404": {n_: ((seal.get("registros_v404") or {}).get(n_) or {}).get("all_verified") for n_ in um._V404_NOMES_REGISTROS}',
     '"f2b_errata_v404": {x: (seal.get("f2b_errata_v404") or {}).get(x) for x in ("verdict", "all_verified", "F2b_status_now")}, "registros_v404": {n_: ((seal.get("registros_v404") or {}).get(n_) or {}).get("all_verified") for n_ in um._V404_NOMES_REGISTROS}' + _SELO405_EXAME, 1),
    ('or pp405c_.get("contexto_ok") is not True or pp405c_.get("beta_ok") is not True or (pp405c_.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS[nome_]): falsos.append("ponto_" + nome_)\n',
     'or pp405c_.get("contexto_ok") is not True or pp405c_.get("beta_ok") is not True or (pp405c_.get("mecanica") or {}).get("n_checks") != DL.D4.N_CHECKS[nome_]): falsos.append("ponto_" + nome_)\n', 1),
    ('(pf2_.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS["f2b"]', '(pf2_.get("mecanica") or {}).get("n_checks") != DL.D4.N_CHECKS["f2b"]', 1),
    ('pv = R["ponto_veracidade"]\n', _FALSOS405 + 'pv = R["ponto_veracidade"]\n', 1),
    ('+ ["caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"] + list(um._V403_NOMES_REGISTROS):\n    core.pop(n_, None)   # o fluxo os recria; comparam-se depois com os do core0',
     '+ ["caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"] + list(um._V403_NOMES_REGISTROS) + ["projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404"] + list(um._V404_NOMES_REGISTROS):\n    core.pop(n_, None)   # o fluxo os recria; comparam-se depois com os do core0', 1),
])

# ------------------------------------------------------------------------------------------- as guardas estaticas da Bancada: o mutante m6 usa um alvo errado que NAO e' o da v405
entrada("guardas_estaticas_bancada_v404.py", autoral=True, regras=[])   # o mutante m6 sobe para o alvo v404, que nao e o da v405 (o que ele cobra); o sandbox curto segue vb21 pela escolha da v405

# ------------------------------------------------------------------------------------------- o ENSAIO A SECO (as regras do ensaio entram no lote C2: derivar_encanamento_v405_regrasC2_ensaio.py)
