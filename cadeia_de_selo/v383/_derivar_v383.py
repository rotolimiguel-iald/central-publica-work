# -*- coding: utf-8 -*-
"""Deriva os scripts do pacote v383 a partir dos ATUAIS da v382 (que ja levam as correcoes das afericoes), com trocas de count conferido:
extrair_axiomas_v383.py, ensaio_a_seco_v383.py, gerar_esperados_v383.py, conferir_rito_v383.py, instalar_v383.py e rito_v383.sh.
A v383: BASE = a v381 custodiada (os backups de bytes que o instalador da v382 gravou); o canonico a SUBSTITUIR no Nos = a v382 (selada so localmente);
o MESMO kernel da v382; o livro em ONZE cobrancas; as NOVE rotas do eco fora do livro."""
import os, ast
HERE = os.path.dirname(os.path.abspath(__file__)); V2 = os.path.join(os.path.dirname(HERE), "v382")
rd = lambda n: open(os.path.join(V2, n), encoding="utf-8", newline="").read()


def wr(n, s, py=True):
    if py:
        ast.parse(s)
    p = os.path.join(HERE, n); assert not os.path.exists(p), p
    open(p, "w", encoding="utf-8", newline="").write(s); print("ok", n)


def subs(s, pares):
    for a, b, n in pares:
        assert s.count(a) == n, (a[:110], s.count(a), n); s = s.replace(a, b)
    return s


AP2_LINE = 'AP2 = json.load(open(os.path.join(os.path.dirname(HERE), "v382", "APLICADO_AO_CANONICO_20261002_174400.json"), encoding="utf-8"))   # v383: os backups de BYTES do estado v381 (a BASE)\n'

# ---- (1) extrair axiomas: so o nome da versao (o build e o mesmo da v382)
wr("extrair_axiomas_v383.py", rd("extrair_axiomas_v382.py").replace("v382", "v383"))

# ---- (2) ensaio a seco: o core de partida e o da v381 (backup de bytes conferido); o modulo, a tag e o artigo da v383
s = rd("ensaio_a_seco_v382.py")
s = subs(s, [
    ('import copy\n', 'import copy\nimport hashlib\n', 1),
    ('NOS = r"C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\Nós"   # v373: a v372 SELADA e o canonico (o estado de partida do ensaio)\n',
     'NOS = r"C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\Nós"   # v373: a v372 SELADA e o canonico (o estado de partida do ensaio)\n' + AP2_LINE
     + 'CORE0P = AP2["backups"]["um_absoluto.json"]["backup"]   # v383: o estado de partida do ensaio e a v381 (o Nos guarda a v382, selada so localmente)\n'
     + 'assert hashlib.sha256(open(CORE0P, "rb").read()).hexdigest()[:16] == AP2["backups"]["um_absoluto.json"]["sha16"], "o backup do core v381 mudou"\n', 1),
    ('R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))', 'R0 = json.load(open(CORE0P, encoding="utf-8"))', 1),
    ('TAG = "v382"', 'TAG = "v383"', 1),
    ('c["the_ledger_of_charges_v382"] = um.prove_the_ledger_of_charges_v382(1.0, c)', 'c["the_ledger_of_charges_v383"] = um.prove_the_ledger_of_charges_v383(1.0, c)', 1),
    ('"the_matrix_rule_v381", "the_ledger_of_charges_v382")', '"the_matrix_rule_v381", "the_ledger_of_charges_v383")', 3),
    ('DEVE = {"pt": ["Ao lado (v382) --- O livro de cobranças e a viscosidade", ', 'DEVE = {"pt": ["Ao lado (v383) --- O livro de cobranças e a viscosidade", "rotas examinadas do eco como cópia atrasada", "prefiro a primeira opção", ', 1),
    ('        "en": ["Beside (v382) --- The ledger of charges and the viscosity", ', '        "en": ["Beside (v383) --- The ledger of charges and the viscosity", "examined routes of the echo as a delayed copy", "prefiro a primeira opção", ', 1),
    ('um.build_pt(c, verdict, os.path.join(NOS, "um_absoluto.json"))', 'um.build_pt(c, verdict, CORE0P)', 1),
    ('um.build_en(c, verdict, os.path.join(NOS, "um_absoluto.json"))', 'um.build_en(c, verdict, CORE0P)', 1),
    ('    nome = "dry_v382_%s" % lang', '    nome = "dry_v383_%s" % lang', 1),
    ('rep["markdown_v376"] = {"v376": md.count("v382"), "carimbo": "**Versão v382**" in md,', 'rep["markdown_v376"] = {"v376": md.count("v383"), "carimbo": "**Versão v383**" in md,', 1),
    ('rep["manifest_v376"] = {"carimbo": "**Versão v382**" in open(mani, encoding="utf-8").read()}', 'rep["manifest_v376"] = {"carimbo": "**Versão v383**" in open(mani, encoding="utf-8").read()}', 1),
])
assert s.count("import hashlib") == 1, "o ensaio precisa de hashlib"
wr("ensaio_a_seco_v383.py", s)

# ---- (3) esperados: a BASE e a v381 (backups); a ORIGEM do instalador e a v382 (o canonico de agora); os tokens da v383
s = rd("gerar_esperados_v382.py")
s = subs(s, [
    ('NOS = r"C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\Nós"\n', 'NOS = r"C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\Nós"\n' + AP2_LINE, 1),
    ('cand = os.path.join(HERE, "um_v382_candidato.py")', 'cand = os.path.join(HERE, "um_v383_candidato.py")', 1),
    ('P = json.load(open(os.path.join(HERE, "patches_v382.json"), encoding="utf-8"))', 'P = json.load(open(os.path.join(HERE, "patches_v383.json"), encoding="utf-8"))', 1),
    ('ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v382.json"), encoding="utf-8"))', 'ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v383.json"), encoding="utf-8"))', 1),
    ('sbx = json.load(open(os.path.join(HERE, "sandbox_raiz_v382.json"), encoding="utf-8"))', 'sbx = json.load(open(os.path.join(HERE, "sandbox_raiz_v383.json"), encoding="utf-8"))', 1),
    ('R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]\nselo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))\n'
     'assert h16(os.path.join(NOS, "um.py")) == P["meta"]["um_py_base"], "o canonico nao e a base do candidato (a v381 selada)"\n',
     'BK = {rel: d["backup"] for rel, d in AP2["backups"].items()}\n'
     'for _rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json"):\n'
     '    assert h16(BK[_rel]) == AP2["backups"][_rel]["sha16"], "o backup de bytes da v381 mudou: %s" % _rel\n'
     'R0 = json.load(open(BK["um_absoluto.json"], encoding="utf-8")); core0 = R0["core"]\nselo0 = json.load(open(BK["um_absoluto_selo.json"], encoding="utf-8"))\n'
     'assert h16(BK["um.py"]) == P["meta"]["um_py_base"], "o backup da v381 nao e a base do candidato"\n'
     'ORIGEM = h16(os.path.join(NOS, "um.py")); assert ORIGEM == AP2["um_py_novo"]["sha16"], "o canonico no Nos nao e a v382 selada so localmente"\n', 1),
    ('FLAGS = json.load(open(os.path.join(HERE, "BANDEIRAS_v382.json"), encoding="utf-8"))', 'FLAGS = json.load(open(os.path.join(HERE, "BANDEIRAS_v383.json"), encoding="utf-8"))', 1),
    ('NOVOS = ("the_ledger_of_charges_v382",)', 'NOVOS = ("the_ledger_of_charges_v383",)', 1),
    ('''assert "THE_TGL_IS_OPTICS_NOT_SEMI_BOTH_SIDES_READ" in ce["the_ledger_of_charges_v382"] and "KERNEL_32_OF_32" in ce["the_ledger_of_charges_v382"]
assert "NO_OUTCOME_MOVES_THE_RULE" in ce["the_ledger_of_charges_v382"] and "PREREGISTRATION_OF_BOTH_SIDES_V1_3_READ_BY_HASH" in ce["the_ledger_of_charges_v382"]
assert "20_CHARGES_" in ce["the_ledger_of_charges_v382"] and "R2_POWER_STATED_IN_NUMBER" in ce["the_ledger_of_charges_v382"] and "F2_INCONCLUSIVE_BY_THE_MEASUREMENT_SYSTEMATIC" in ce["the_ledger_of_charges_v382"]
assert "0_FALSIFIED_IN_THE_RULE" in ce["the_ledger_of_charges_v382"] and "KEY_AND_OPTICS_INPUT_ONTO" in ce["the_ledger_of_charges_v382"]
assert "DELAYED_ECHO_OUTSIDE_THE_CHAIN_5_OF_9_PAIRS_EXTINGUISHED_4_INCONCLUSIVE" in ce["the_ledger_of_charges_v382"] and "R4_FROZEN_SET_HAS_NO_FALSIFIED" in ce["the_ledger_of_charges_v382"]
assert "NOT_A_CONFIRMATION" in ce["the_ledger_of_charges_v382"] and ce["the_ledger_of_charges_v382"].endswith("__GATE_UNTOUCHED")''',
     '''_v = ce["the_ledger_of_charges_v383"]
assert "THE_TGL_IS_OPTICS_NOT_SEMI_BOTH_SIDES_READ" in _v and "KERNEL_32_OF_32" in _v and "NO_OUTCOME_MOVES_THE_RULE" in _v and "PREREGISTRATION_OF_BOTH_SIDES_V1_4_READ_BY_HASH" in _v
assert "11_CHARGES_10_IN_THE_RULE_1_BESIDE__0_FALSIFIED_" in _v and "R2_POWER_STATED_IN_NUMBER" in _v and "F2_INCONCLUSIVE_BY_THE_MEASUREMENT_SYSTEMATIC" in _v and "KEY_AND_OPTICS_INPUT_ONTO" in _v
assert "THE_9_ECHO_ROUTES_ARE_NOT_CHARGES_OF_THE_THEORY_EXAMINED_OUTSIDE_THE_LEDGER_5_EXCLUDED_BY_DATA_4_INCONCLUSIVE__OPERATOR_DECISION__BASE_V381" in _v and "R4_FROZEN_SET_HAS_NO_FALSIFIED" in _v
assert "NOT_A_CONFIRMATION" in _v and _v.endswith("__GATE_UNTOUCHED") and "DELAYED_ECHO" not in _v''', 1),
    ('"candidato_sha16": h16(cand), "candidato_bytes": os.path.getsize(cand), "origem_sha16": P["meta"]["um_py_base"],',
     '"candidato_sha16": h16(cand), "candidato_bytes": os.path.getsize(cand), "origem_sha16": ORIGEM, "base_build_sha16": P["meta"]["um_py_base"], "v382_so_local_sha16": ORIGEM,', 1),
    ('"escada_esperada_v382": core0["external_ladder"]["n_theorems_clean"] + len(FLAGS),', '"escada_esperada_v383": core0["external_ladder"]["n_theorems_clean"] + len(FLAGS),', 1),
    ('"vereditos_v382_do_ensaio": {k: ce[k] for k in NOVOS},', '"vereditos_v383_do_ensaio": {k: ce[k] for k in NOVOS},', 1),
    ('"um_py_v381_sha16": h16(os.path.join(NOS, "um.py")),', '"um_py_v381_sha16": h16(BK["um.py"]),', 1),
    ('"md_carimbo": "**Versão v382**",', '"md_carimbo": "**Versão v383**",', 1),
    ('"ensaio_markdown_v382": ens.get("markdown_v376"), "ensaio_manifest_v382": ens.get("manifest_v376"),', '"ensaio_markdown_v383": ens.get("markdown_v376"), "ensaio_manifest_v383": ens.get("manifest_v376"),', 1),
    ('json.dump(esp, open(os.path.join(HERE, "ESPERADOS_v382.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)', 'json.dump(esp, open(os.path.join(HERE, "ESPERADOS_v383.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)', 1),
    ('"vereditos_v382_do_ensaio")}, ensure_ascii=False, indent=1)[:2500])', '"vereditos_v383_do_ensaio")}, ensure_ascii=False, indent=1)[:2500])', 1),
    ('print("ESPERADOS_v382.json:", {k: esp[k] for k in ("candidato_sha16", "origem_sha16", "escada_esperada_v382", "n_modulos_md_esperado")}',
     'print("ESPERADOS_v383.json:", {k: esp[k] for k in ("candidato_sha16", "origem_sha16", "base_build_sha16", "escada_esperada_v383", "n_modulos_md_esperado")}', 1),
])
s = subs(s, [('"""gerar_esperados_v382.py -- grava ESPERADOS_v382.json LENDO os artefatos (nada digitado): candidato, sandbox (build verde), ensaio e o selo v381 (canonico).',
              '"""gerar_esperados_v383.py -- grava ESPERADOS_v383.json LENDO os artefatos (nada digitado): candidato, sandbox (build verde), ensaio e o selo v381 (o backup de bytes: a BASE); a ORIGEM do instalador e a v382 do Nos.', 1)])
assert "v382" not in s.replace('"v382", "APLICADO_AO_CANONICO', "").replace("v382_so_local", "").replace("a v382", "").replace("v382 selada", ""), [l for l in s.split("\n") if "v382" in l]
wr("gerar_esperados_v383.py", s)

# ---- (4) conferidor: os nomes v383; o livro de ONZE; as NOVE rotas fora do livro; a chave da v382 AUSENTE do core
s = rd("conferir_rito_v382.py").replace("v382", "v383").replace("V382", "V383")
s = subs(s, [
    ('''    "O LIVRO DE COBRANCAS: TESTES -- beta do core = alpha.sqrt(e) (1e-9 rel.); o pre-registro V1.3 lido por hash (JSON e MD = os do gerador; 20 cobrancas); as 20 cobrancas com o desfecho lido pelo modo dito (token / numero com regra / declarado) e iguais ao pre-registro; todas as chaves com token no veredito do core; >= 1 FALSIFIED, >= 1 EXCLUDED_IN_READING, >= 1 AWAITING; R2 sem poder em numero (Gamma(100 Hz) < 1e-30 s^-1); o nome do degrau final lido do fonte = o proposto; o gate inalterado; IDENTIDADES DE SANIDADE (nao testes) -- cos^2 theta_M = 1 - beta, sin^2 theta_M = beta, e^{-beta} + complemento = 1":
        rt.get("beta_core") is not None and abs(float(rt["law_alpha_sqrt_e"]) / float(core["beta"]) - 1.0) < 1e-9 and pr.get("read_ok") is True and pr.get("n_cobrancas") == 20
        and pr.get("sha256_read") == ESP["preregistro_sha256"] and len(lc.get("ledger") or []) == 20 and all(c.get("outcome_ok") and c.get("matches_preregistration") for c in (lc.get("ledger") or []))
        and lc.get("n_token_in_core") == lc.get("n_with_core_key") == 19 and sum((lc.get("by_how") or {}).values()) == 20 and (lc.get("counts_in_rule") or {}).get("FALSIFIED", 1) == 0
        and (lc.get("counts") or {}).get("FALSIFIED", 0) >= 1 and (lc.get("counts") or {}).get("EXCLUDED_IN_READING", 0) >= 1 and (lc.get("counts") or {}).get("AWAITING", 0) >= 1''',
     '''    "O LIVRO DE COBRANCAS: TESTES -- beta do core = alpha.sqrt(e) (1e-9 rel.); o pre-registro V1.4 lido por hash (JSON e MD = os do gerador; 11 cobrancas); as 11 cobrancas com o desfecho lido pelo modo dito (token / numero com regra / declarado) e iguais ao pre-registro; todas as chaves com token no veredito do core; 0 FALSIFIED no livro, >= 1 EXCLUDED_IN_READING, >= 1 AWAITING; as 9 ROTAS do eco FORA do livro (estado lido do rotulo da Fase 6, igual ao V1.4; 5 excluidas pelos dados, 4 inconclusivas; as fontes do motivo no core; a base v381); R2 sem poder em numero (Gamma(100 Hz) < 1e-30 s^-1); o nome do degrau final lido do fonte = o proposto; o gate inalterado; IDENTIDADES DE SANIDADE (nao testes) -- cos^2 theta_M = 1 - beta, sin^2 theta_M = beta, e^{-beta} + complemento = 1":
        rt.get("beta_core") is not None and abs(float(rt["law_alpha_sqrt_e"]) / float(core["beta"]) - 1.0) < 1e-9 and pr.get("read_ok") is True and pr.get("n_cobrancas") == 11
        and pr.get("sha256_read") == ESP["preregistro_sha256"] and len(lc.get("ledger") or []) == 11 and all(c.get("outcome_ok") and c.get("matches_preregistration") for c in (lc.get("ledger") or []))
        and lc.get("n_token_in_core") == lc.get("n_with_core_key") == 10 and sum((lc.get("by_how") or {}).values()) == 11 and (lc.get("counts") or {}).get("FALSIFIED", 1) == 0
        and (lc.get("counts") or {}).get("EXCLUDED_IN_READING", 0) >= 1 and (lc.get("counts") or {}).get("AWAITING", 0) >= 1
        and (lambda er: er.get("n") == 9 and er.get("excluded_by_data", 0) + er.get("inconclusive", 0) == 9 and er.get("not_charges_of_the_theory") is True and er.get("sources_in_core_ok") is True
             and all(r.get("state_ok") and r.get("matches_preregistration") and r.get("not_a_charge") is True for r in (er.get("routes") or [])) and len(er.get("routes") or []) == 9)(lc.get("echo_routes_outside_the_ledger") or {})
        and (lc.get("base_and_local_seal") or {}).get("base") == "v381" and (lc.get("base_and_local_seal") or {}).get("v382_local_only_sha16") == ESP["v382_so_local_sha16"]''', 1),
    ('''        and (lc.get("delayed_echo_pairs") or {}).get("n") == 9 and bool(lc.get("r4_frozen_set")) and bool(lc.get("corrections_beside_20261002")) and len(lc.get("readings_ratified_20261002") or {}) == 6,''',
     '''        and bool(lc.get("r4_frozen_set")) and bool(lc.get("corrections_beside_20261002")) and len(lc.get("readings_ratified_20261002") or {}) == 6
        and (lc.get("operator_decision_20261002") or {}).get("verbatim") == "prefiro a primeira opção",
    "a chave da v382 (selada so no Nos) NAO esta no core da v383": "the_ledger_of_charges_v382" not in core and "the_ledger_of_charges_reading_v382" not in selo,''', 1),
])
for t in ("o pre-registro V1.3", "20 cobrancas", "delayed_echo_pairs"):
    assert t not in s, t
wr("conferir_rito_v383.py", s)

# ---- (5) instalar e (6) rito: os nomes v383; a ORIGEM e a v382 selada so no Nos (lida de ESPERADOS_v383.origem_sha16)
s = rd("instalar_v382.py").replace("v382", "v383")
s = subs(s, [("«isso mesmo, prossiga» (o livro de cobranças; a TGL é ótica), 02/10/2026", "«prefiro a primeira opção» (os nove pares do eco fora do livro), 02/10/2026, noite", 1),
             ("  * o canonico tem de ser a v381 selada (sha16 lido de ESPERADOS_v383.json.origem_sha16) e o candidato o de ESPERADOS (candidato_sha16);",
              "  * o canonico tem de ser a v382 selada SO no Nos (sha16 lido de ESPERADOS_v383.json.origem_sha16; a base do candidato e a v381) e o candidato o de ESPERADOS (candidato_sha16);", 1),
             ('assert h16(raw0) == ESP["origem_sha16"], "o canonico nao e a v381 selada (%s)" % h16(raw0)', 'assert h16(raw0) == ESP["origem_sha16"], "o canonico nao e a v382 selada so no Nos (%s)" % h16(raw0)', 1)])
wr("instalar_v383.py", s)
s = rd("rito_v382.sh").replace("v382", "v383")
s = subs(s, [("«isso mesmo, prossiga» (o livro de cobranças; a TGL é ótica), 02/10/2026", "«prefiro a primeira opção» (os nove pares do eco fora do livro), 02/10/2026, noite", 1)])
wr("rito_v383.sh", s, py=False)
print("pacote v383 derivado")
