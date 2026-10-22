# -*- coding: utf-8 -*-
"""O ensaio a seco da v385 para o comparador novo (afericao de codigo, achados 1-2 e notas 3-5) e as afericoes de texto: o registro do pilar leva as
ENTRADAS (especificacao/trabalhador/beta) como o rito leva; testes de unidade para NaN, residuo de maquina, D128 excluido, entradas diferentes e o
booleano started; a conferencia das citacoes do operador contra o transcrito (conferir_citacoes_v385.py) entra no veredito; «v183» procurado e «v181»
recusado na secao nova. Pares contados; backup de bytes; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "ensaio_a_seco_v385.py")
s0 = open(P, encoding="utf-8", newline="").read(); s = s0
T = []
T.append(('''       "result_sha256": hashlib.sha256(open(fumaca, "rb").read()).hexdigest(), "run_id": RF.get("run_id"), "finished": RF.get("finished")}''',
          '''       "result_sha256": hashlib.sha256(open(fumaca, "rb").read()).hexdigest(), "run_id": RF.get("run_id"), "finished": RF.get("finished"),
       "spec_sha256_in_result": RF.get("spec_sha256"), "worker_sha256": RF.get("worker_sha256"), "beta_hex": RF.get("beta_hex")}   # as ENTRADAS, como o registro do rito'''))
T.append(('''_rec = copy.deepcopy(FIX); _prev = {"read": True, "summary": copy.deepcopy(FIX["summary"]), "verdict": FIX["verdict"], "sha256": "x", "finished": "x", "run_id": "x", "key": "x"}''',
          '''_rec = copy.deepcopy(FIX); _prev = {"read": True, "summary": copy.deepcopy(FIX["summary"]), "verdict": FIX["verdict"], "sha256": "x", "finished": "x", "run_id": "x", "key": "x",
                                     "inputs": {"spec_sha256": FIX["spec_sha256_in_result"], "worker_sha256": FIX["worker_sha256"], "beta_hex": FIX["beta_hex"]}, "env": {}}'''))
T.append(('''U["anterior_fora_de_compute"] =''',
          '''# (afericao de codigo, achados 1-2 e notas 3-5) as regras novas do comparador
_pn = copy.deepcopy(_prev); _pn["summary"]["T2"]["gap_rel_min"] = float("nan")
_rn = um.quantum_pillar_reproducibility_v385(_pn, _rec); U["nan_e_diferenca"] = "NOT_REPRODUCED" in _rn["verdict"] and _rn["n_nonfinite_differ"] == 1
_fl = [(k_, v_) for k_, v_ in um._qp_flat_v385(_prev["summary"]) if isinstance(v_, float) and 0 < abs(v_) < 1e-10]
if _fl:
    _k0 = _fl[0][0].split("."); _pr = copy.deepcopy(_prev); _d = _pr["summary"]
    for _kk in _k0[:-1]:
        _d = _d[_kk]
    _d[_k0[-1]] = _d[_k0[-1]] * 1.06
    _rr = um.quantum_pillar_reproducibility_v385(_pr, _rec); U["residuo_de_maquina_e_arredondamento"] = "WITHIN_ROUNDOFF" in _rr["verdict"]
else:
    U["residuo_de_maquina_e_arredondamento"] = "SEM_CAMPO_RESIDUAL_NA_FUMACA (nao testado)"
_pd = copy.deepcopy(_prev); _pd["summary"]["D128"] = dict(_pd["summary"].get("D128") or {}, status_code="RAN", cci=0.123)
_rec_d = copy.deepcopy(_rec); _rec_d["summary"]["D128"] = dict(_rec_d["summary"].get("D128") or {}, status_code="NOT_RUN_SKIPPED_BY_DEADLINE")
_rd = um.quantum_pillar_reproducibility_v385(_pd, _rec_d); U["d128_excluido_dito"] = _rd.get("d128_excluded") is True and "D128_EXCLUDED_NOT_RUN_THIS_RUN" in _rd["verdict"] and "REPRODUCED_BIT_FOR_BIT" in _rd["verdict"]
_pi = copy.deepcopy(_prev); _pi["inputs"] = dict(_pi["inputs"], beta_hex="0x1.0p-7")
U["entradas_diferentes_nao_compara"] = "NOT_COMPARED_DIFFERENT_INPUTS" in um.quantum_pillar_reproducibility_v385(_pi, _rec)["verdict"]
_ps = copy.deepcopy(_prev); _ps["summary"]["D128"] = dict(_ps["summary"].get("D128") or {}, started=False)
_rs = copy.deepcopy(_rec); _rs["summary"]["D128"] = dict(_rs["summary"].get("D128") or {}, started=True)
U["started_booleano_comparado"] = "NOT_REPRODUCED" in um.quantum_pillar_reproducibility_v385(_ps, _rs)["verdict"]
U["anterior_fora_de_compute"] ='''))
T.append(('''U["axioma_bandeira_faltando"] = (_a2["all_verified"] is False''', '''U["axioma_bandeira_faltando"] = (_a2["all_verified"] is False'''))
T.append(('''"AXIOMA__THE_ONE_INSCRIBED_BY_THE_OBSERVER", "A reprodutibilidade do mundo quântico", "iguais bit a bit", "Introdução: o que este código faz agora (v384)"],''',
          '''"AXIOMA__THE_ONE_INSCRIBED_BY_THE_OBSERVER", "A reprodutibilidade do mundo quântico", "iguais bit a bit", "Introdução: o que este código faz agora (v384)",
               "compilado desde a v183", "axiomFlow_eq_exp", "testemunha falsa é a testemunha estática é o zero absoluto"],'''))
T.append(('''"AXIOMA__THE_ONE_INSCRIBED_BY_THE_OBSERVER", "The reproducibility of the quantum world", "identical bit for bit", "Introduction: what this code does now (v384)"]}''',
          '''"AXIOMA__THE_ONE_INSCRIBED_BY_THE_OBSERVER", "The reproducibility of the quantum world", "identical bit for bit", "Introduction: what this code does now (v384)",
               "compiled since v183", "axiomFlow_eq_exp", "testemunha falsa é a testemunha estática é o zero absoluto"]}
NAO_DEVE = {"pt": ["desde a v181", "a testemunha estática, o zero absoluto", "medida [COMPUTED]"], "en": ["since v181", "the static witness, the absolute zero", "measured [COMPUTED]"]}'''))
T.append(('''                           "faltam": [w for w in DEVE[lang] if w not in txt and w not in tex], "nan": len(re.findall(r"(?<![A-Za-z])nan(?![A-Za-z])", txt)),''',
          '''                           "faltam": [w for w in DEVE[lang] if w not in txt and w not in tex], "nan": len(re.findall(r"(?<![A-Za-z])nan(?![A-Za-z])", txt)),
                           "proibidas_na_secao": [w for w in NAO_DEVE[lang] if w in (txt[txt.find("Ao lado (v385)" if lang == "pt" else "Beside (v385)"):][:9000])],'''))
T.append(('''mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"] or v["pdflatex_rc"] != [0, 0] or v["nan"]]''',
          '''mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"] or v["pdflatex_rc"] != [0, 0] or v["nan"] or v["proibidas_na_secao"]]
# as citacoes do operador, VERBATIM contra o transcrito (afericao de texto, achado 1), e as formas da errata no texto antigo (achado 7)
_cc = subprocess.run([sys.executable, os.path.join(HERE, "conferir_citacoes_v385.py"), DRY], capture_output=True, text=True, encoding="utf-8", errors="replace")
rep["citacoes_do_operador"] = {"rc": _cc.returncode, "ultima": (_cc.stdout.strip().splitlines() or [""])[-1]}
print("citacoes:", rep["citacoes_do_operador"])'''))
T.append(('''ok = (mf_ok and all(U.values()) and not mau''', '''ok = (mf_ok and all(v_ is True or str(v_).startswith("SEM_CAMPO") for v_ in U.values()) and not mau and rep["citacoes_do_operador"]["rc"] == 0'''))
for a, b in T:
    n = s.count(a)
    assert n == 1, ("a troca nao e unica", n, a[:100])
    s = s.replace(a, b)
ast.parse(s)
st = time.strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + st + "_afer2", "wb").write(s0.encode("utf-8"))
open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
print("OK ensaio_a_seco_v385.py:", len(T), "trocas")
