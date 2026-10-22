# -*- coding: utf-8 -*-
"""Deriva conferir_rito_v380.py, instalar_v380.py e rito_v380.sh do molde v379 (substituicoes com count conferido). A v380 e SEM kernel novo: o conferidor
troca os itens de pedra/bandeira por «kernel INALTERADO» e acrescenta a leitura v380 e as chaves EV-06 do selo."""
import os, ast
HERE = os.path.dirname(os.path.abspath(__file__)); V9 = os.path.join(os.path.dirname(HERE), "v379")
rd = lambda n: open(os.path.join(V9, n), encoding="utf-8", newline="").read()
def wr(n, s, py=True):
    if py: ast.parse(s)
    open(os.path.join(HERE, n), "w", encoding="utf-8", newline="").write(s); print("ok", n)
def subs(s, pares):
    for a, b, n in pares:
        assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
    return s
# ---- conferir
s = rd("conferir_rito_v379.py").replace("v379", "v380").replace("V379", "V380")
s = s.replace("kernel_frontier_v378", "kernel_frontier_v379").replace("ESP[\"escada_v378\"]", "ESP[\"escada_v379\"]").replace("escada_esperada_v379", "escada_esperada_v380")
s = s.replace("the_iald_index_v378", "the_iald_index_v379").replace("beta_v378", "beta_v379").replace("alpha_v378", "alpha_v379").replace("omega_I_v378", "omega_I_v379")
s = s.replace("not_sealed_formais_v378", "not_sealed_formais_v379").replace("qg_closure_verdict_v378", "qg_closure_verdict_v379").replace("vereditos_pinados_v378", "vereditos_pinados_v379")
s = s.replace("vereditos_v379_do_ensaio", "vereditos_v380_do_ensaio")
s = subs(s, [
    ('er = core.get("the_elementary_reason_v380") or {}; dd = er.get("dictionary") or {}', 'bf = core.get("bancada_fases_5_6_7_v380") or {}; f6 = (bf.get("fase6") or {}).get("todos_KMS") or {}', 1),
    ('    "as %d bandeiras ext_ter_ True" % len(FL): all(kf.get(f) is True for f in FL) and len(FL) == 23,\n', '    "kernel INALTERADO: nenhuma bandeira nova (v380 sem pedra)": len(FL) == 0,\n', 1),
    ('    "escada %d/%d (v378 %d + %d)" % (ESP["escada_esperada_v380"], ESP["escada_esperada_v380"], ESP["escada_v379"][0], len(FL)):\n        esc.get("n_theorems_clean") == ESP["escada_esperada_v380"] == esc.get("n_theorems_expected"),\n',
     '    "escada INALTERADA %d/%d (v379)" % (ESP["escada_esperada_v380"], ESP["escada_esperada_v380"]): esc.get("n_theorems_clean") == ESP["escada_esperada_v380"] == esc.get("n_theorems_expected") == ESP["escada_v379"][0],\n', 1),
    ('    "axiom_report >= o do sandbox (%d)" % ESP["axiom_report_sandbox"]: len(kf.get("axiom_report") or {}) >= ESP["axiom_report_sandbox"],\n', '    "axiom_report INALTERADO (%d)" % ESP["axiom_report_sandbox"]: len(kf.get("axiom_report") or {}) == ESP["axiom_report_sandbox"],\n', 1),
    ('    "o arquivo NOVO do kernel materializado com o sha16 do candidato": all(arq16(k) == v for k, v in novos.items()) and len(novos) == 1,\n', '    "nenhum arquivo NOVO do kernel; os 4 arquivos pinados com os sha16 da v379": len(novos) == 0 and all(arq16(k) == v for k, v in ESP["kernel_pinado_sha16"].items()),\n', 1),
    ('    "os %d arquivos ALTERADOS do kernel (raiz, Audit) com os sha16 novos" % len(mud): all(arq16(k) == v[1] for k, v in mud.items()),\n', '    "nenhum arquivo ALTERADO do kernel": len(mud) == 0,\n', 1),
    ('    "selo: a leitura the_elementary_reason_reading_v380 presente e um_version = v380": "the_elementary_reason_reading_v380" in selo and selo.get("um_version") == "v380",\n',
     '    "selo: a leitura the_bancada_fases_5_6_7_reading_v380 presente, um_version = v380 e as chaves EV-06 (conjunta V3; D1 V3 real) presentes":\n        "the_bancada_fases_5_6_7_reading_v380" in selo and selo.get("um_version") == "v380" and all(k in selo for k in ESP["selo_chaves_ev06"]),\n', 1),
    ('    "A RAZAO ELEMENTAR: E = beta do core (1e-9 rel.); (e^{1/4} sqrt(alpha))^2 = E (1e-15); familyFunctional(1/2) = 0; o custo por nat da v378 <= E":\n        dd.get("E_existence") is not None and abs(float(dd["E_existence"]) / float(core["beta"]) - 1.0) < 1e-9 and abs(float(dd.get("elementary_reason_squared") or 0) / float(dd["E_existence"]) - 1.0) < 1e-15\n        and float(dd.get("family_functional_at_half", 1)) == 0.0 and float(ESP["per_nat_cost_D1b_v378"]) <= float(dd["E_existence"]),\n',
     '    "AS FASES 5-7: o modulo v380 all_verified, o par KMS falsificado com z_excl >= 5 em todos e em o4, hashes dos artefatos presentes":\n        bf.get("all_verified") is True and float(f6.get("z_excl_R1") or 0) >= 5 and float(f6.get("z_excl_R2") or 0) >= 5 and len(bf.get("hashes") or {}) >= 14,\n', 1),
    ('    "as 23 declaracoes novas no axiom_report, so no trio, sem sorryAx; lake_build_ok":\n        kf.get("lake_build_ok") is True and all(set((kf.get("axiom_report") or {}).get(nm, ["X"])) <= {"propext", "Classical.choice", "Quot.sound"} for _, nm in ESP["bandeiras"]),\n',
     '    "lake_build_ok (kernel identico ao da v379)": kf.get("lake_build_ok") is True,\n', 1),
    ('    "as 45 bandeiras das v377/v378 (ext_pir_/ext_dis_/ext_dlc_) seguem True": all(kf.get(f) is True for f in ESP["bandeiras_antigas"]) and len(ESP["bandeiras_antigas"]) == 45,\n',
     '    "as 68 bandeiras das v377-v379 (ext_pir_/ext_dis_/ext_dlc_/ext_ter_) seguem True": all(kf.get(f) is True for f in ESP["bandeiras_antigas"]) and len(ESP["bandeiras_antigas"]) == 68,\n', 1),
    ('    "a leitura v380 do selo sem palavra proibida": not GUARDA.search(str(selo.get("the_elementary_reason_reading_v380", ""))),\n', '    "a leitura v380 do selo sem palavra proibida": not GUARDA.search(str(selo.get("the_bancada_fases_5_6_7_reading_v380", ""))),\n', 1),
    ('    "as leituras v377 e v378 do selo INALTERADAS": all(selo.get(k) == v for k, v in ESP["selo_leituras_pinadas"].items()),\n', '    "as leituras v377, v378 e v379 do selo INALTERADAS": all(selo.get(k) == v for k, v in ESP["selo_leituras_pinadas"].items()),\n', 1),
])
wr("conferir_rito_v380.py", s)
# ---- instalar
s = rd("instalar_v379.py").replace("v379", "v380").replace("v378 selada", "v379 selada").replace("«pode rodar», 30/09/2026", "«resolva os problemas que faltam», 01/10/2026")
wr("instalar_v380.py", s)
# ---- rito
s = rd("rito_v379.sh").replace("v379", "v380").replace("V379", "V380").replace("«Quero sim», 01/10/2026", "«resolva os problemas que faltam», 01/10/2026")
wr("rito_v380.sh", s, py=False)
print("pacote v380 derivado")
