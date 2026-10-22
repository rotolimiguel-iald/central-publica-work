# -*- coding: utf-8 -*-
"""4a afericao no ENSAIO A SECO: os enunciados do terceiro balde (que leem variaveis locais do main) saem de `comeca`/`contem` e o BLOCO INTEIRO da custodia de
sentido (de `_not_sealed = sorted(` ao print do W08c) e' extraido do candidato e executado a parte, com core sintetico e seal = {}, em dois casos (pilar
nao concluido e pilar concluido), conferindo o balde e a linha impressa; e duas variantes novas do artigo: o D128 rodado e o resultado sem cache por falta
do D128. Backup ja feito (.bak_antes_afer4)."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "ensaio_a_seco_v384.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert open(P + ".bak_antes_afer4", "rb").read() == raw
NL = chr(10)
PAIRS = [
    ('''comeca = [st for st in main.body if st.lineno in tagged]
contem = [st for st in main.body if st not in comeca and any(ln in tagged for ln in range(st.lineno, (st.end_lineno or st.lineno) + 1))]''',
     '''_txt_st = lambda st: NL.join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])
NL = chr(10)
# os enunciados do TERCEIRO BALDE leem variaveis locais do main (_not_sealed, _formais, _recusas, _computacao): nao vao ao fluxo executado; o bloco inteiro roda
# a parte, abaixo (4a afericao)
comeca = [st for st in main.body if st.lineno in tagged and "_computacao" not in _txt_st(st)]
contem = [st for st in main.body if st not in comeca and "_computacao" not in _txt_st(st) and any(ln in tagged for ln in range(st.lineno, (st.end_lineno or st.lineno) + 1))]'''),
    ('''balde = [st for st in main.body if st not in comeca and st not in contem and "_computacao" in "\\n".join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])]''',
     '''balde = [st for st in main.body if "_computacao" in _txt_st(st)]'''),
    ('''# as VARIANTES do registro (3a afericao)''', '''# o BLOCO DA CUSTODIA DE SENTIDO, executado a parte (4a afericao): de `_not_sealed = sorted(` ao print do W08c, com core sintetico e seal = {}
_i0 = next(i for i, l in enumerate(lines) if l.strip().startswith("_not_sealed = sorted("))
_i1 = next(i for i in range(_i0, len(lines)) if "computacao nao concluida: %s" in lines[i])
_i1 = next(i for i in range(_i1, len(lines)) if lines[i].rstrip().endswith('or "nenhuma"))'))
_bloco = textwrap.dedent(NL.join(lines[_i0:_i1 + 1]))
rep["custodia_de_sentido"] = {}
for _cn, _qv, _av in (("pilar_nao_concluido", "TGL_QUANTUM_PILLAR_V1__NOT_RUN__LAUNCH_FAILED__GATE_UNTOUCHED", False),
                      ("pilar_concluido", "TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__ENSAIO__GATE_UNTOUCHED", True)):
    _core_s = {"mod_a": {"verdict": "X_OK", "all_verified": True}, "mod_formal": {"verdict": "ALGO_EM_DIVIDA", "all_verified": False},
               "mod_recusa": {"verdict": "Y__INCONCLUSIVE__Z", "all_verified": False}, "quantum_pillar_v384": {"verdict": _qv, "all_verified": _av}}
    _ns_b = {"core": _core_s, "seal": {}}
    _o = sys.stdout; sys.stdout = io.StringIO()
    try:
        exec(compile(_bloco, "<custodia_de_sentido>", "exec"), _ns_b)
        _pr = sys.stdout.getvalue(); _er = None
    except Exception as e:  # noqa
        _pr = sys.stdout.getvalue(); _er = repr(e)
    finally:
        sys.stdout = _o
    _bal = (_ns_b.get("seal") or {}).get("not_sealed_this_run") or {}
    _esp = ["quantum_pillar_v384"] if not _av else []
    _ok_b = (_er is None and _bal.get("computacao_nao_concluida") == _esp and _bal.get("formais") == ["mod_formal"] and _bal.get("recusas_de_dado") == ["mod_recusa"]
             and ("computacao nao concluida: " + (", ".join(_esp) or "nenhuma")) in _pr)
    rep["custodia_de_sentido"][_cn] = {"ok": _ok_b, "erro": _er, "balde": _bal, "impresso": _pr.strip()}
print("custodia de sentido:", json.dumps({k: v["ok"] for k, v in rep["custodia_de_sentido"].items()}))
mau_bloco = [k for k, v in rep["custodia_de_sentido"].items() if not v["ok"]]
# as VARIANTES do registro (3a afericao)'''),
    ('''        "t1_sem_solucao": (dict(copy.deepcopy(FIX), summary=um._qp_summary(_RFi)), {"pt": ["sem solução finita"], "en": ["no finite solution"]})}''',
     '''        "t1_sem_solucao": (dict(copy.deepcopy(FIX), summary=um._qp_summary(_RFi)), {"pt": ["sem solução finita"], "en": ["no finite solution"]}),
        # 4a afericao: o D128 rodado (a fumaca nao o roda) e o resultado sem cache por falta do D128
        "d128_rodado": (dict(copy.deepcopy(FIX), summary=dict(copy.deepcopy(FIX["summary"]), D128={"d": 128, "nc": 3, "gamma_diss": 1.0, "started": True, "ran": True, "status_code": "RAN",
                                                                                                   "status": "UNIQUE", "n0": 1, "zero_mode_ok": True, "cci": 0.5, "spectrum_s": 600.0})),
                        {"pt": ["atrator UNIQUE"], "en": ["attractor UNIQUE"]}),
        "sem_cache_d128": (dict(copy.deepcopy(FIX), reuse={"reused": False, "reading": "ENSAIO", "not_cached_code": "D128_NOT_RAN:NOT_RUN_DEADLINE",
                                                           "not_cached_because": "o D128 nao rodou nesta rodada (NOT_RUN_DEADLINE)"}),
                           {"pt": ["não foi guardado para reaproveitamento"], "en": ["not stored for reuse"]})}'''),
    ('''ok = (not mau and not mau_var and not bad and not _mf_err''', '''ok = (not mau and not mau_var and not mau_bloco and not bad and not _mf_err'''),
    ('''rep["veredito"] = "TUDO PASSOU" if ok else ("FALHOU: " + json.dumps({"artigo": mau, "variantes": mau_var, "nomes": bad,''',
     '''rep["veredito"] = "TUDO PASSOU" if ok else ("FALHOU: " + json.dumps({"artigo": mau, "variantes": mau_var, "custodia": mau_bloco, "nomes": bad,'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
ast.parse(s)
open(P + ".tmp", "wb").write(s.encode("utf-8")); os.replace(P + ".tmp", P); print("ok", len(PAIRS))
