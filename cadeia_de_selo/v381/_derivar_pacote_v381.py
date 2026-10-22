# -*- coding: utf-8 -*-
"""Deriva conferir_rito_v381.py (do molde v379, versao com kernel), instalar_v381.py e rito_v381.sh (do molde v380) com substituicoes de count conferido.
A v381 TEM kernel novo (TheMatrixRule, 22 bandeiras ext_tmr_); a base e a v380 selada; o conferidor acrescenta as chaves EV-06 e as leituras v379/v380 pinadas."""
import os, ast
HERE = os.path.dirname(os.path.abspath(__file__)); V9 = os.path.join(os.path.dirname(HERE), "v379"); V0 = os.path.join(os.path.dirname(HERE), "v380")
rd = lambda d, n: open(os.path.join(d, n), encoding="utf-8", newline="").read()


def wr(n, s, py=True):
    if py:
        ast.parse(s)
    open(os.path.join(HERE, n), "w", encoding="utf-8", newline="").write(s); print("ok", n)


def subs(s, pares):
    for a, b, n in pares:
        assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
    return s


# ---- conferir (molde v379: versao com kernel)
s = rd(V9, "conferir_rito_v379.py").replace("v379", "v381").replace("V379", "V381")
for a, b in (("kernel_frontier_v378", "kernel_frontier_v380"), ('ESP["escada_v378"]', 'ESP["escada_v380"]'), ("the_iald_index_v378", "the_iald_index_v380"),
             ("beta_v378", "beta_v380"), ("alpha_v378", "alpha_v380"), ("omega_I_v378", "omega_I_v380"), ("not_sealed_formais_v378", "not_sealed_formais_v380"),
             ("qg_closure_verdict_v378", "qg_closure_verdict_v380"), ("vereditos_pinados_v378", "vereditos_pinados_v380"), ("Contra o selo v378", "Contra o selo v380")):
    assert a in s, a; s = s.replace(a, b)
s = subs(s, [
    ('er = core.get("the_elementary_reason_v381") or {}; dd = er.get("dictionary") or {}', 'tm = core.get("the_matrix_rule_v381") or {}; rt = tm.get("runtime") or {}', 1),
    ('    "as %d bandeiras ext_ter_ True" % len(FL): all(kf.get(f) is True for f in FL) and len(FL) == 23,\n', '    "as %d bandeiras ext_tmr_ True" % len(FL): all(kf.get(f) is True for f in FL) and len(FL) == 24,\n', 1),
    ('    "escada %d/%d (v378 %d + %d)" % (ESP["escada_esperada_v381"], ESP["escada_esperada_v381"], ESP["escada_v380"][0], len(FL)):\n',
     '    "escada %d/%d (v380 %d + %d)" % (ESP["escada_esperada_v381"], ESP["escada_esperada_v381"], ESP["escada_v380"][0], len(FL)):\n', 1),
    ('    "selo: a leitura the_elementary_reason_reading_v381 presente e um_version = v381": "the_elementary_reason_reading_v381" in selo and selo.get("um_version") == "v381",\n',
     '    "selo: a leitura the_matrix_rule_reading_v381 presente e um_version = v381": "the_matrix_rule_reading_v381" in selo and selo.get("um_version") == "v381",\n', 1),
    ('    "A RAZAO ELEMENTAR: E = beta do core (1e-9 rel.); (e^{1/4} sqrt(alpha))^2 = E (1e-15); familyFunctional(1/2) = 0; o custo por nat da v378 <= E":\n'
     '        dd.get("E_existence") is not None and abs(float(dd["E_existence"]) / float(core["beta"]) - 1.0) < 1e-9 and abs(float(dd.get("elementary_reason_squared") or 0) / float(dd["E_existence"]) - 1.0) < 1e-15\n'
     '        and float(dd.get("family_functional_at_half", 1)) == 0.0 and float(ESP["per_nat_cost_D1b_v378"]) <= float(dd["E_existence"]),\n',
     '    "A REGRA MATRIZ: TESTES -- beta do core = alpha.sqrt(e) (1e-9 rel.), (e^{1/4} sqrt(alpha))^2 = beta, dez nomes na ordem lidos do fonte, 8 havendo no verbatim; IDENTIDADES DE SANIDADE (nao testes) -- sin^2 theta_M = beta, |e^{i theta_M}| = 1, 0 < e^{-beta} < 1":\n'
     '        rt.get("beta_core") is not None and abs(float(rt["law_alpha_sqrt_e"]) / float(core["beta"]) - 1.0) < 1e-9 and abs(float(rt["reflection_weight_sin2"]) - float(core["beta"])) < 1e-12\n'
     '        and abs(float(rt["spectrum_modulus"]) - 1.0) < 1e-12 and len(tm.get("chain") or []) == 10 and 0.0 < float(rt["leak_weight_e_minus_beta"]) < 1.0\n        and abs(float(rt["radical_squared"]) / float(core["beta"]) - 1.0) < 1e-12 and tm.get("n_havendo_verbatim") == 8 and list(tm.get("chain_from_source") or []) == list(tm.get("chain") or []),\n', 1),
    ('    "as 23 declaracoes novas no axiom_report, so no trio, sem sorryAx; lake_build_ok":\n', '    "as 24 declaracoes novas no axiom_report, so no trio, sem sorryAx; lake_build_ok":\n', 1),
    ('    "as 45 bandeiras das v377/v378 (ext_pir_/ext_dis_/ext_dlc_) seguem True": all(kf.get(f) is True for f in ESP["bandeiras_antigas"]) and len(ESP["bandeiras_antigas"]) == 45,\n',
     '    "as 68 bandeiras das v377-v379 (ext_pir_/ext_dis_/ext_dlc_/ext_ter_) seguem True": all(kf.get(f) is True for f in ESP["bandeiras_antigas"]) and len(ESP["bandeiras_antigas"]) == 68,\n'
     '    "as chaves EV-06 do selo (conjunta V3; D1 V3 real) seguem presentes": all(k in selo for k in ESP["selo_chaves_ev06"]),\n', 1),
    ('    "a leitura v381 do selo sem palavra proibida": not GUARDA.search(str(selo.get("the_elementary_reason_reading_v381", ""))),\n',
     '    "a leitura v381 do selo sem palavra proibida (com a terceira palavra)": not GUARDA.search(str(selo.get("the_matrix_rule_reading_v381", ""))) and "TGL_PRO" + "VED" not in str(selo.get("the_matrix_rule_reading_v381", "")),\n', 1),
    ('    "as leituras v377 e v378 do selo INALTERADAS": all(selo.get(k) == v for k, v in ESP["selo_leituras_pinadas"].items()),\n',
     '    "as leituras v377, v378, v379 e v380 do selo INALTERADAS": all(selo.get(k) == v for k, v in ESP["selo_leituras_pinadas"].items()),\n', 1),
])
wr("conferir_rito_v381.py", s)
# ---- instalar (molde v380)
s = rd(V0, "instalar_v380.py").replace("v380", "v381").replace("v379 selada", "v380 selada").replace("«resolva os problemas que faltam», 01/10/2026", "«É exatamente isso» (a regra matriz), 02/10/2026")
wr("instalar_v381.py", s)
# ---- rito (molde v380)
s = rd(V0, "rito_v380.sh").replace("v380", "v381").replace("V380", "V381").replace("«resolva os problemas que faltam», 01/10/2026", "«É exatamente isso» (a regra matriz), 02/10/2026")
wr("rito_v381.sh", s, py=False)
print("pacote v381 derivado")
