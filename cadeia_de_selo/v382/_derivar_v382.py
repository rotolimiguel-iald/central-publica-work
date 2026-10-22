# -*- coding: utf-8 -*-
"""Deriva, com substituicoes de count conferido, a partir dos moldes da v381: ensaio_a_seco_v382.py, conferir_rito_v382.py, instalar_v382.py e rito_v382.sh.
A v382 TEM kernel novo (duas pedras, 32 bandeiras ext_loc_/ext_psv_); a base e a v381 selada; o conferidor pina tambem a v381 (veredito e leitura do selo)."""
import os, ast
HERE = os.path.dirname(os.path.abspath(__file__)); V1 = os.path.join(os.path.dirname(HERE), "v381")
rd = lambda d, n: open(os.path.join(d, n), encoding="utf-8", newline="").read()


def wr(n, s, py=True):
    if py:
        ast.parse(s)
    open(os.path.join(HERE, n), "w", encoding="utf-8", newline="").write(s); print("ok", n)


def subs(s, pares):
    for a, b, n in pares:
        assert s.count(a) == n, (a[:100], s.count(a), n); s = s.replace(a, b)
    return s


# ---- ensaio a seco (molde v381; substituicoes pontuais: nada de "v381"->"v382" cego, porque the_matrix_rule_v381 e chave de modulo)
s = rd(V1, "ensaio_a_seco_v381.py")
s = subs(s, [
    ('TAG = "v381"', 'TAG = "v382"', 1),
    ('    if k.startswith(("ext_ter_", "ext_tmr_")):', '    if k.startswith(("ext_ter_", "ext_tmr_", "ext_loc_", "ext_psv_")):', 1),
    ('c["the_matrix_rule_v381"] = um.prove_the_matrix_rule_v381(1.0, c)\n',
     'c["the_matrix_rule_v381"] = um.prove_the_matrix_rule_v381(1.0, c)\nc["the_ledger_of_charges_v382"] = um.prove_the_ledger_of_charges_v382(1.0, c)\n', 1),
    ('"the_matrix_rule_v381")', '"the_matrix_rule_v381", "the_ledger_of_charges_v382")', 3),
    ('DEVE = {"pt": ["Ao lado (v381) --- A regra matriz", ',
     'DEVE = {"pt": ["Ao lado (v382) --- O livro de cobranças e a viscosidade", "Hamiltoniano oculto", "a TGL é ótica", "viscosidade", "pré-registro dos dois lados", "Ao lado (v381) --- A regra matriz", ', 1),
    ('        "en": ["Beside (v381) --- The matrix rule", ',
     '        "en": ["Beside (v382) --- The ledger of charges and the viscosity", "hidden Hamiltonian", "the TGL is optics", "viscosity", "pre-registration of both sides", "Beside (v381) --- The matrix rule", ', 1),
    ('    nome = "dry_v381_%s" % lang', '    nome = "dry_v382_%s" % lang', 1),
    ('rep["markdown_v376"] = {"v376": md.count("v381"), "carimbo": "**Versão v381**" in md,', 'rep["markdown_v376"] = {"v376": md.count("v382"), "carimbo": "**Versão v382**" in md,', 1),
    ('rep["manifest_v376"] = {"carimbo": "**Versão v381**" in open(mani, encoding="utf-8").read()}', 'rep["manifest_v376"] = {"carimbo": "**Versão v382**" in open(mani, encoding="utf-8").read()}', 1),
])
wr("ensaio_a_seco_v382.py", s)
# ---- conferir (molde v381): (1) v381 -> v382 (nomes do pacote/rodada), (2) v380 -> v381 (as chaves da base em ESPERADOS), (3) as linhas da v382
s = rd(V1, "conferir_rito_v381.py").replace("v381", "v382").replace("V381", "V382").replace("v380", "v381")
s = subs(s, [
    ('tm = core.get("the_matrix_rule_v382") or {}; rt = tm.get("runtime") or {}', 'lc = core.get("the_ledger_of_charges_v382") or {}; rt = lc.get("runtime") or {}; pr = lc.get("preregistration") or {}', 1),
    ('    "as %d bandeiras ext_tmr_ True" % len(FL): all(kf.get(f) is True for f in FL) and len(FL) == 24,\n', '    "as %d bandeiras ext_loc_/ext_psv_ True" % len(FL): all(kf.get(f) is True for f in FL) and len(FL) == 32,\n', 1),
    ('    "o arquivo NOVO do kernel materializado com o sha16 do candidato": all(arq16(k) == v for k, v in novos.items()) and len(novos) == 1,\n',
     '    "os 2 arquivos NOVOS do kernel materializados com os sha16 do candidato": all(arq16(k) == v for k, v in novos.items()) and len(novos) == 2,\n', 1),
    ('    "selo: a leitura the_matrix_rule_reading_v382 presente e um_version = v382": "the_matrix_rule_reading_v382" in selo and selo.get("um_version") == "v382",\n',
     '    "selo: a leitura the_ledger_of_charges_reading_v382 presente e um_version = v382": "the_ledger_of_charges_reading_v382" in selo and selo.get("um_version") == "v382",\n', 1),
    ('    "A REGRA MATRIZ: TESTES -- beta do core = alpha.sqrt(e) (1e-9 rel.), (e^{1/4} sqrt(alpha))^2 = beta, dez nomes na ordem lidos do fonte, 8 havendo no verbatim; IDENTIDADES DE SANIDADE (nao testes) -- sin^2 theta_M = beta, |e^{i theta_M}| = 1, 0 < e^{-beta} < 1":\n'
     '        rt.get("beta_core") is not None and abs(float(rt["law_alpha_sqrt_e"]) / float(core["beta"]) - 1.0) < 1e-9 and abs(float(rt["reflection_weight_sin2"]) - float(core["beta"])) < 1e-12\n'
     '        and abs(float(rt["spectrum_modulus"]) - 1.0) < 1e-12 and len(tm.get("chain") or []) == 10 and 0.0 < float(rt["leak_weight_e_minus_beta"]) < 1.0\n'
     '        and abs(float(rt["radical_squared"]) / float(core["beta"]) - 1.0) < 1e-12 and tm.get("n_havendo_verbatim") == 8 and list(tm.get("chain_from_source") or []) == list(tm.get("chain") or []),\n',
     '    "O LIVRO DE COBRANCAS: TESTES -- beta do core = alpha.sqrt(e) (1e-9 rel.); o pre-registro V1.3 lido por hash (JSON e MD = os do gerador; 20 cobrancas); as 20 cobrancas com o desfecho lido pelo modo dito (token / numero com regra / declarado) e iguais ao pre-registro; todas as chaves com token no veredito do core; >= 1 FALSIFIED, >= 1 EXCLUDED_IN_READING, >= 1 AWAITING; R2 sem poder em numero (Gamma(100 Hz) < 1e-30 s^-1); o nome do degrau final lido do fonte = o proposto; o gate inalterado; IDENTIDADES DE SANIDADE (nao testes) -- cos^2 theta_M = 1 - beta, sin^2 theta_M = beta, e^{-beta} + complemento = 1":\n'
     '        rt.get("beta_core") is not None and abs(float(rt["law_alpha_sqrt_e"]) / float(core["beta"]) - 1.0) < 1e-9 and pr.get("read_ok") is True and pr.get("n_cobrancas") == 20\n'
     '        and pr.get("sha256_read") == ESP["preregistro_sha256"] and len(lc.get("ledger") or []) == 20 and all(c.get("outcome_ok") and c.get("matches_preregistration") for c in (lc.get("ledger") or []))\n'
     '        and lc.get("n_token_in_core") == lc.get("n_with_core_key") == 19 and sum((lc.get("by_how") or {}).values()) == 20 and (lc.get("counts_in_rule") or {}).get("FALSIFIED", 1) == 0\n'
     '        and (lc.get("counts") or {}).get("FALSIFIED", 0) >= 1 and (lc.get("counts") or {}).get("EXCLUDED_IN_READING", 0) >= 1 and (lc.get("counts") or {}).get("AWAITING", 0) >= 1\n'
     '        and 0.0 < float(rt["R2_gamma_100hz_per_s"]) < 1e-30 and lc.get("final_step_name_from_source") == lc.get("final_step_name_proposed") and lc.get("gate_unchanged") is True\n'
     '        and abs(float(rt["face_weight_cos2"]) - (1.0 - float(core["beta"]))) < 1e-12 and abs(float(rt["reflection_weight_sin2"]) - float(core["beta"])) < 1e-12\n'
     '        and abs(float(rt["transmitted_t1_g1"]) + float(rt["charged_t1_g1"]) - 1.0) < 1e-12\n'
     '        and (lc.get("delayed_echo_pairs") or {}).get("n") == 9 and bool(lc.get("r4_frozen_set")) and bool(lc.get("corrections_beside_20261002")) and len(lc.get("readings_ratified_20261002") or {}) == 6,\n'
     '    "os %d homonimos novos (nomeados em _AMBIGUOS_CONJUNTO_V382) estao no conjunto de ambiguos do indice da IALD" % len(ESP["homonimos_novos"]):\n'
     '        len(ESP["homonimos_novos"]) == 3 and all(n in set(ix.get("ambiguos") or []) for n in ESP["homonimos_novos"]),\n', 1),
    ('    "as 24 declaracoes novas no axiom_report, so no trio, sem sorryAx; lake_build_ok":\n', '    "as 32 declaracoes novas no axiom_report, so no trio, sem sorryAx; lake_build_ok":\n', 1),
    ('    "as 68 bandeiras das v377-v379 (ext_pir_/ext_dis_/ext_dlc_/ext_ter_) seguem True": all(kf.get(f) is True for f in ESP["bandeiras_antigas"]) and len(ESP["bandeiras_antigas"]) == 68,\n',
     '    "as 92 bandeiras das v377-v381 (ext_pir_/ext_dis_/ext_dlc_/ext_ter_/ext_tmr_) seguem True": all(kf.get(f) is True for f in ESP["bandeiras_antigas"]) and len(ESP["bandeiras_antigas"]) == 92,\n', 1),
    ('    "a leitura v382 do selo sem palavra proibida (com a terceira palavra)": not GUARDA.search(str(selo.get("the_matrix_rule_reading_v382", ""))) and "TGL_PRO" + "VED" not in str(selo.get("the_matrix_rule_reading_v382", "")),\n',
     '    "a leitura v382 do selo sem palavra proibida (com a terceira palavra)": not GUARDA.search(str(selo.get("the_ledger_of_charges_reading_v382", ""))) and "TGL_PRO" + "VED" not in str(selo.get("the_ledger_of_charges_reading_v382", "")),\n', 1),
    ('    "as leituras v377, v378, v379 e v381 do selo INALTERADAS": all(selo.get(k) == v for k, v in ESP["selo_leituras_pinadas"].items()),\n',
     '    "as leituras v377, v378, v379, v380 e v381 do selo INALTERADAS": all(selo.get(k) == v for k, v in ESP["selo_leituras_pinadas"].items()),\n', 1),
])
assert "the_matrix_rule_v382" not in s and "the_matrix_rule_reading_v382" not in s, "sobrou referencia errada a v382 na regra matriz"
wr("conferir_rito_v382.py", s)
# ---- instalar e rito (molde v381)
s = rd(V1, "instalar_v381.py").replace("v381", "v382").replace("v380 selada", "v381 selada").replace("«É exatamente isso» (a regra matriz), 02/10/2026", "«isso mesmo, prossiga» (o livro de cobranças; a TGL é ótica), 02/10/2026")
# aferidor da v382, E1: o rito sobrescreve as duas memorias canonicas .md -- backup de BYTES delas tambem (regra do backup imediato)
s = subs(s, [('for rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")):',
              'for rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")):', 1)])
s = subs(s, [("um.py, um_absoluto.json, um_absoluto_selo.json, tgl_kernel/TGLExt.lean, tgl_kernel/TGL/Audit.lean (.bak_<ts> na mesma pasta)", "um.py, um_absoluto.json, um_absoluto_selo.json, um_absoluto_forma_canonica.md, um_absoluto_manifest.md, tgl_kernel/TGLExt.lean, tgl_kernel/TGL/Audit.lean (.bak_<ts> na mesma pasta)", 1)])
wr("instalar_v382.py", s)
s = rd(V1, "rito_v381.sh").replace("v381", "v382").replace("V381", "V382").replace("«É exatamente isso» (a regra matriz), 02/10/2026", "«isso mesmo, prossiga» (o livro de cobranças; a TGL é ótica), 02/10/2026")
wr("rito_v382.sh", s, py=False)
print("pacote v382 derivado")
