# -*- coding: utf-8 -*-
"""As trocas de ESTRUTURA do runtime v383 (sobre a copia renomeada do v382): o livro em ONZE cobrancas; as NOVE rotas do eco FORA do livro (estado lido do
rotulo da Fase 6, conferido contra o V1.4; as fontes do motivo cruzadas no core); o pre-registro V1.4; o veredito, o estatuto e o retorno. Cada trecho velho
tem de ocorrer EXATAMENTE uma vez (fail-closed). Backup de bytes antes; tmp -> ast.parse -> replace."""
import ast, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "v383_runtime.py")
s = open(P, encoding="utf-8", newline="").read()
raw = s.encode("utf-8")
bak = P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_antes_estrutura"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw

# (1) o pre-registro V1.4
A = '''# o PRE-REGISTRO DOS DOIS LADOS V1.3 (02/10/2026; supersede o V1.2, o V1.1 e o V1 pelos achados das afericoes): caminho e sha256 LIDOS pelo gerador do candidato a partir dos arquivos
_V383_PREREG = {
    "json": {"path": "C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_3.json", "sha256": "__PREREG_JSON_SHA256__"},
    "md": {"path": "C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_3.md", "sha256": "__PREREG_MD_SHA256__"},
    "identificador": "PREREG_DOIS_LADOS_DELTA_K_20261002_V1_3", "mapa_seq": 282,
    "supersede": "PREREG_DOIS_LADOS_DELTA_K_20261002_V1_2 (mapa seq 279), que supersedia o V1.1 (seq 276) e o V1 (seq 275)",
}'''
B = '''# o PRE-REGISTRO DOS DOIS LADOS V1.4 (02/10/2026, noite; supersede o V1.3 pela DECISAO DO OPERADOR: os nove pares do eco fora do livro): caminho e sha256 LIDOS pelo gerador do candidato a partir dos arquivos
_V383_PREREG = {
    "json": {"path": "C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.json", "sha256": "__PREREG_JSON_SHA256__"},
    "md": {"path": "C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.md", "sha256": "__PREREG_MD_SHA256__"},
    "identificador": "PREREG_DOIS_LADOS_DELTA_K_20261002_V1_4", "mapa_seq": 290,
    "supersede": "PREREG_DOIS_LADOS_DELTA_K_20261002_V1_3 (mapa seq 282), que supersedia o V1.2 (seq 279), o V1.1 (seq 276) e o V1 (seq 275)",
}'''
REPS = [(A, B)]
REPS.append(("# e conferido contra o pre-registro V1.3]. Campos:", "# e conferido contra o pre-registro V1.4]. Campos:"))

# (2) as nove linhas do eco SAEM do livro (a primeira e a ultima, com tudo entre elas)
i = s.index('    ("R5a", "reflexo", "copia atrasada (fora da cadeia)"'); j = s.index('    ("R6", "face", "o custo POSTO na face por CONVENCAO')
ECO_ROWS = s[i:j]
assert ECO_ROWS.count('("R5') == 9 and ECO_ROWS.count("\n") == 18, (ECO_ROWS.count('("R5'), ECO_ROWS.count("\n"))
REPS.append((ECO_ROWS, ""))

# (3) as NOVE ROTAS examinadas FORA DO LIVRO, depois do livro (antes das leituras ratificadas)
ROTAS = '''# as NOVE ROTAS examinadas FORA DO LIVRO -- o eco como COPIA ATRASADA (decisao do operador, 02/10, noite: NAO sao cobrancas da teoria; nao entram nas contagens
# do livro, nao tem desfecho do tipo Charge, nao movem a regra). Campos: id, id no V1.3, par (amplitude, lei de atraso), chave do core, o ROTULO da Fase 6
# (CITADO como fonte; o estado da rota e lido dele), caminho do veredito aninhado (ou None), estado ESPERADO (EXCLUDED_BY_DATA: o dado exclui o par; ou
# INCONCLUSIVE), numeros (caminhos no core). O motivo de cada rota vem do pre-registro V1.4 (lido por hash) e as suas fontes sao cruzadas no core.
_V383_ECHO_ROUTES = (
    ("ECO_a", "R5a", "(sqrt(beta), KMS 2pi/kappa)", _V383_B, "KMS_PAIR_SQRT_BETA_AND_SIN2THETA_FALSIFIED_AT_DELAY_LAW", None, "EXCLUDED_BY_DATA",
     {"z_excl": [_V383_B, "fase6", "todos_KMS", "z_excl_R1"], "z_excl_o4_cego": [_V383_B, "fase6", "o4_KMS_cego", "z_excl_R1"], "n_eventos": [_V383_B, "fase6", "todos_KMS", "n_eventos"]}),
    ("ECO_b", "R5b", "(sin 2theta, KMS 2pi/kappa)", _V383_B, "KMS_PAIR_SQRT_BETA_AND_SIN2THETA_FALSIFIED_AT_DELAY_LAW", None, "EXCLUDED_BY_DATA",
     {"z_excl": [_V383_B, "fase6", "todos_KMS", "z_excl_R2"], "z_excl_o4_cego": [_V383_B, "fase6", "o4_KMS_cego", "z_excl_R2"], "n_eventos": [_V383_B, "fase6", "todos_KMS", "n_eventos"]}),
    ("ECO_c", "R5c", "(sqrt(beta), DEC 2GM_f/(beta c^3))", _V383_B, "DEC2025_LAW_FROM_THE_ARCHIVE_DECLARED_BLIND_TO_THE_NEW_DELAY_ONLY_PAIR_SQRT_BETA_AND_SIN2THETA_FALSIFIED_Z_EXCL_8P95_AND_16P83", None, "EXCLUDED_BY_DATA",
     {"z_excl": [_V383_B, "emenda_v5", "todos_DEC", "z_excl_R1"], "z_excl_o4_cego": [_V383_B, "emenda_v5", "o4_DEC_cego", "z_excl_R1"], "n_eventos": [_V383_B, "emenda_v5", "todos_DEC", "n_eventos"]}),
    ("ECO_d", "R5d", "(sin 2theta, DEC)", _V383_B, "DEC2025_LAW_FROM_THE_ARCHIVE_DECLARED_BLIND_TO_THE_NEW_DELAY_ONLY_PAIR_SQRT_BETA_AND_SIN2THETA_FALSIFIED_Z_EXCL_8P95_AND_16P83", None, "EXCLUDED_BY_DATA",
     {"z_excl": [_V383_B, "emenda_v5", "todos_DEC", "z_excl_R2"], "z_excl_o4_cego": [_V383_B, "emenda_v5", "o4_DEC_cego", "z_excl_R2"], "n_eventos": [_V383_B, "emenda_v5", "todos_DEC", "n_eventos"]}),
    ("ECO_e", "R5e", "(sin 2theta, MAY ln 1/beta) -- V4, NAO cega", _V383_B, "AMENDMENT_V4_NOT_BLIND_SIN2THETA_MAY_FALSIFIED_Z_8P75_CONTROLS_MAX_Z_4P81", None, "EXCLUDED_BY_DATA",
     {"z_excl": [_V383_B, "emenda_v4", "todos_MAY", "z_excl_R2"], "controles_max_z": [_V383_B, "emenda_v4", "todos_MAY", "controles_max_z"]}),
    ("ECO_f", "R5f", "(sqrt(beta), MAY ln 1/beta)", _V383_B, "SQRT_BETA_MAY_INCONCLUSIVE_IS_THE_ESTIMATOR_LIMIT", None, "INCONCLUSIVE",
     {"sist_rel": [_V383_B, "emenda_v4", "todos_MAY", "sist_rel_R1"]}),
    ("ECO_g", "R5g", "(beta, DEC) -- o documento de dezembro", _V383_B, "DOC_PAIR_BETA_DEC_INCONCLUSIVE_SYSTEMATICS_BY_RULE_2_POWER_0P87_BLIND_POWER_1P47", None, "INCONCLUSIVE",
     {"sist_rel": [_V383_B, "emenda_v5", "todos_DEC", "sist_rel_R3"], "poder_ao_lado": [_V383_B, "emenda_v5", "todos_DEC", "poder_R3"]}),
    ("ECO_h", "R5h", "(beta, KMS 2pi/kappa)", _V383_B, "INCONCLUSIVE_SYSTEMATICS", [_V383_B, "fase6", "veredito_principal", "KMS|R3_quadrado"], "INCONCLUSIVE", {}),
    ("ECO_i", "R5i", "(beta, MAY ln 1/beta) -- V4", _V383_B, "INCONCLUSIVE_SYSTEMATICS", [_V383_B, "emenda_v4", "vereditos_todos", "MAY", "R3_quadrado"], "INCONCLUSIVE", {}),
)
_V383_READINGS_RATIFIED = {'''
REPS.append(("_V383_READINGS_RATIFIED = {", ROTAS))

# (4) a correcao ao lado sobre o eco (da gerencia, aplicando a decisao do operador)
REPS.append(('''    "optics": "a TGL e OTICA, nao semi-otica''', '''    "echo": "os nove pares do eco como copia atrasada NAO sao cobrancas da teoria (decisao do operador, 02/10, noite: «prefiro a primeira opção»): sao rotas examinadas FORA do livro, com o estado lido do rotulo da Fase 6, os numeros e o motivo; a definicao do operador de 16/09 (o eco como resposta da fronteira) FICA",
    "optics": "a TGL e OTICA, nao semi-otica'''))

# (5) o estatuto
REPS.append(('''"pre-registro V1.3 por hash [REAL]; F2 e inconclusivo''', '''"pre-registro V1.4 por hash [REAL]; F2 e inconclusivo'''))
REPS.append(('''R4 nao tem FALSIFIED no conjunto congelado e a MESMA fonte alimenta o degrau experimental do gate; dos nove pares do eco como copia atrasada, os extintos e os inconclusivos "
                 "sao contados (o veredito diz os dois numeros); as cobrancas AO LADO (R5a-i, R6) nao sao da regra canonica e contam em separado; nenhum desfecho move beta;''',
             '''R4 nao tem FALSIFIED no conjunto congelado e a MESMA fonte alimenta o degrau experimental do gate; os nove pares do eco como copia atrasada NAO sao cobrancas da "
                 "teoria (decisao do operador): sao ROTAS examinadas fora do livro, com o estado lido do rotulo da Fase 6, os numeros e o motivo (o veredito diz quantas o dado exclui e quantas "
                 "sao inconclusivas); a cobranca AO LADO (R6) nao e da regra canonica e conta em separado; a base e a v381 custodiada e a v382 foi selada so no Nos (nao custodiada); nenhum desfecho move beta;'''))

# (6) a docstring da funcao
REPS.append(('''    """v382 -- O LIVRO DE COBRANCAS + o psion com a viscosidade + o pre-registro dos dois lados (V1.3) por hash [ADITIVO; nao move o gate].''',
             '''    """v383 -- O LIVRO DE COBRANCAS (ONZE cobrancas; os nove pares do eco FORA do livro, como rotas examinadas, pela decisao do operador) + o psion com a viscosidade
    + o pre-registro dos dois lados (V1.4) por hash [ADITIVO; nao move o gate].'''))
REPS.append(("os checks sobre o fonte sao presenca no texto embutido + bandeira. RUNTIME: o livro concreto (VINTE cobrancas, UMA por lei de leitura), cada desfecho",
             "os checks sobre o fonte sao presenca no texto embutido + bandeira. RUNTIME: o livro concreto (ONZE cobrancas, UMA por lei de leitura), cada desfecho"))
REPS.append(("    LIDO do core pelo modo dito (token no veredito do modulo ou no aninhado / numero com regra / declarado) e conferido contra o pre-registro V1.3 lido por",
             "    LIDO do core pelo modo dito (token no veredito do modulo ou no aninhado / numero com regra / declarado) e conferido contra o pre-registro V1.4 lido por"))

# (7) as rotas, depois do livro; os cruzamentos das fontes do motivo
A7 = '''    counts = {o: sum(1 for c in ledger if c["outcome"] == o) for o in _V383_OUTCOMES}'''
B7 = '''    # ---- as NOVE ROTAS fora do livro (o eco como copia atrasada): o estado lido do rotulo da Fase 6 no veredito do core, conferido contra o V1.4 (por hash)
    pr_rot = {r.get("id"): r for r in ((pr["json"] or {}).get("rotas_examinadas_fora_do_livro") or [])} if pr["json"] else {}
    routes = []
    for rid, rid13, par, chave, token, vpath, state, nums_p in _V383_ECHO_ROUTES:
        verd = str(_v383_get(core, vpath) or "") if vpath else Vd(chave)
        tin = token in verd
        derived = "EXCLUDED_BY_DATA" if ("FALSIFIED" in token and "NOT_FALSIFIED" not in token) else ("INCONCLUSIVE" if "INCONCLUSIVE" in token else "UNREAD")
        pc = pr_rot.get(rid) or {}
        pre_ok = (bool(pc) and pc.get("id_no_v1_3") == rid13 and pc.get("estado") == state and pc.get("chave_core") == chave and pc.get("token") == token
                  and (pc.get("caminho_veredito") or None) == (vpath or None) and pc.get("nao_e_cobranca") is True)
        routes.append({"id": rid, "id_in_v1_3": rid13, "pair": par, "core_key": chave, "phase6_label_cited": token, "verdict_path": vpath, "state": state, "state_derived": derived,
                       "label_in_core_verdict": tin, "state_ok": bool(tin and derived == state), "matches_preregistration": pre_ok,
                       "numbers_read": {k: _v383_get(core, p) for k, p in nums_p.items()}, "reasons_from_preregistration": list(pc.get("motivo") or []),
                       "delay_law_from_preregistration": dict(pc.get("lei_de_atraso") or {}), "amplitude_from_preregistration": dict(pc.get("amplitude") or {}), "not_a_charge": True})
    n_rt = len(routes); rt_exc = sum(1 for r in routes if r["state"] == "EXCLUDED_BY_DATA"); rt_inc = sum(1 for r in routes if r["state"] == "INCONCLUSIVE")
    routes_ok = (all(r["state_ok"] and r["matches_preregistration"] for r in routes) and len(pr_rot) == n_rt == len(_V383_ECHO_ROUTES)
                 and not ({r["id"] for r in routes} & {c["id"] for c in ledger}) and not ({r["id_in_v1_3"] for r in routes} & {c["id"] for c in ledger}))
    # as FONTES do motivo, presentes no core (cruzamento): a errata GWECO-05 da lei KMS e a consequencia ratificada da v381 (o eco como copia atrasada fora da cadeia)
    gweco = str(_v383_get(core, [_V383_B, "errata_beside_v380", "gw_echo_kms_law__period_in_imaginary_time"]) or "")
    fora = str(_v383_get(core, ["the_matrix_rule_v381", "consequences_ratified_20261002", "delayed_echo"]) or "")
    sources_ok = (bool(gweco) and "GWECO-05" in gweco and bool(fora) and "fora da cadeia" in fora and "DELAYED_ECHO_OUTSIDE_THE_CHAIN" in Vd("the_matrix_rule_v381")
                  and all(any(fora in str(m) for m in r["reasons_from_preregistration"]) for r in routes)
                  and all(r["delay_law_from_preregistration"].get("errata_gweco05") == gweco for r in routes if "KMS" in r["pair"]))
    up = ((pr["json"] or {}).get("um_py") or {}); v382l = up.get("v382_so_local") or {}
    base_ok = up.get("base_versao") == "v381" and len(str(v382l.get("sha256") or "")) == 64
    counts = {o: sum(1 for c in ledger if c["outcome"] == o) for o in _V383_OUTCOMES}'''
REPS.append((A7, B7))
# o eco ja nao e lido do livro
REPS.append(('''    eco = [c for c in ledger if c["id"].startswith("R5")]; eco_ext = sum(1 for c in eco if c["extinguished"]); eco_inc = sum(1 for c in eco if c["outcome"] == "INCONCLUSIVE")\n''', ""))
# as rotas entram na guarda das palavras proibidas
REPS.append(('''    all_strings = ([s for row in _V383_LEDGER_INPUT for s in row if isinstance(s, str)] + list(_V383_READINGS_RATIFIED.values()) + list(_V383_CORRECTIONS_BESIDE.values()) + [_V383_STATUTE, _V383_FINAL_STEP_NAME]''',
             '''    all_strings = ([s for row in _V383_LEDGER_INPUT for s in row if isinstance(s, str)] + [s for row in _V383_ECHO_ROUTES for s in row if isinstance(s, str)]
                   + list(_V383_READINGS_RATIFIED.values()) + list(_V383_CORRECTIONS_BESIDE.values()) + [_V383_STATUTE, _V383_FINAL_STEP_NAME, _V383_OPTION_CHOSEN]'''))

# (8) os checks
REPS.append(('''        ("RUNTIME (cruzamento real): o PRE-REGISTRO DOS DOIS LADOS V1.3 lido por bytes''', '''        ("RUNTIME (cruzamento real): o PRE-REGISTRO DOS DOIS LADOS V1.4 lido por bytes'''))
REPS.append(('''         pr_ok and (pr["json"] or {}).get("identificador") == _V383_PREREG["identificador"] and len(pr_cob) == len(_V383_LEDGER_INPUT) and len(_V383_LEDGER_INPUT) == 20),''',
             '''         pr_ok and (pr["json"] or {}).get("identificador") == _V383_PREREG["identificador"] and len(pr_cob) == len(_V383_LEDGER_INPUT) and len(_V383_LEDGER_INPUT) == 11),'''))
REPS.append(('''todos iguais ao pre-registro V1.3 (%d/%d); contagens %s; na regra %d (%s) / ao lado %d" % (''', '''todos iguais ao pre-registro V1.4 (%d/%d); contagens %s; na regra %d (%s) / ao lado %d" % ('''))
REPS.append(('''         all_outcomes_ok and all_pre_ok and n_token_ok == n_with_key == 19 and counts["FALSIFIED"] >= 1 and counts["AWAITING"] >= 1 and counts["EXCLUDED_IN_READING"] >= 1),''',
             '''         all_outcomes_ok and all_pre_ok and n_token_ok == n_with_key == 10 and counts["FALSIFIED"] == 0 and counts["AWAITING"] >= 1 and counts["EXCLUDED_IN_READING"] >= 1),'''))
A8 = '''        ("RUNTIME (cruzamento real): o eco como copia atrasada -- %d pares no livro: %d extintos (FALSIFIED) e %d inconclusivos; o R4 le um conjunto congelado SEM FALSIFIED (%s), a mesma fonte do degrau experimental do gate: as %d bandeiras do experiment_feed do V11 (%s) estao no degrau experimental do gate com o mesmo valor (%s)" % (
            len(eco), eco_ext, eco_inc, ", ".join(str(x) for x in r4set), len(vff), ", ".join(sorted(vff)), r4_feeds_gate),
         len(eco) == 9 and eco_ext + eco_inc == 9 and bool(r4set) and not any(("FALSIFIED" in str(x) and "NOT_FALSIFIED" not in str(x)) for x in r4set) and r4_feeds_gate),'''
B8 = '''        ("RUNTIME (cruzamento real): o R4 le um conjunto congelado SEM FALSIFIED (%s), a mesma fonte do degrau experimental do gate: as %d bandeiras do experiment_feed do V11 (%s) estao no degrau experimental do gate com o mesmo valor (%s)" % (
            ", ".join(str(x) for x in r4set), len(vff), ", ".join(sorted(vff)), r4_feeds_gate),
         bool(r4set) and not any(("FALSIFIED" in str(x) and "NOT_FALSIFIED" not in str(x)) for x in r4set) and r4_feeds_gate),
        ("RUNTIME (cruzamento real): as %d ROTAS examinadas FORA DO LIVRO (o eco como copia atrasada; NAO sao cobrancas da teoria, decisao do operador) -- o rotulo da Fase 6 de cada uma lido no veredito do core e CITADO; estado igual ao V1.4 (%d/%d): %d excluidas pelos dados, %d inconclusivas; nenhuma no livro; as fontes do motivo no core (a errata GWECO-05 da lei KMS; a consequencia ratificada da v381, o eco fora da cadeia)" % (
            n_rt, sum(1 for r in routes if r["state_ok"] and r["matches_preregistration"]), n_rt, rt_exc, rt_inc),
         routes_ok and sources_ok and rt_exc + rt_inc == n_rt == 9),
        ("RUNTIME (cruzamento real): a base declarada no V1.4 e a v381 custodiada; a v382 (sha16 %s) foi selada so no Nos e NAO e custodiada (o V1.4 o diz)" % str(v382l.get("sha256") or "AUSENTE")[:16],
         base_ok),'''
REPS.append((A8, B8))

# (9) o veredito
A9 = '''              "PREREGISTRATION_OF_BOTH_SIDES_V1_3_READ_BY_HASH__R2_POWER_STATED_IN_NUMBER__R4_FROZEN_SET_HAS_NO_FALSIFIED_SAME_SOURCE_AS_THE_GATE_EXPERIMENTAL_STEP__FINAL_STEP_NAME_PROPOSED_BESIDE_GATE_UNCHANGED__BRANCH_B_CLOSED__"
              "DELAYED_ECHO_OUTSIDE_THE_CHAIN_%d_OF_%d_PAIRS_EXTINGUISHED_%d_INCONCLUSIVE__NOT_THE_RULE__"'''
B9 = '''              "PREREGISTRATION_OF_BOTH_SIDES_V1_4_READ_BY_HASH__R2_POWER_STATED_IN_NUMBER__R4_FROZEN_SET_HAS_NO_FALSIFIED_SAME_SOURCE_AS_THE_GATE_EXPERIMENTAL_STEP__FINAL_STEP_NAME_PROPOSED_BESIDE_GATE_UNCHANGED__BRANCH_B_CLOSED__"
              "THE_%d_ECHO_ROUTES_ARE_NOT_CHARGES_OF_THE_THEORY_EXAMINED_OUTSIDE_THE_LEDGER_%d_EXCLUDED_BY_DATA_%d_INCONCLUSIVE__OPERATOR_DECISION__BASE_V381__"'''
REPS.append((A9, B9))
REPS.append(('''                 eco_ext, len(eco), eco_inc))''', '''                 n_rt, rt_exc, rt_inc))'''))

# (10) o retorno
A10 = '''            "delayed_echo_pairs": {"n": len(eco), "extinguished": eco_ext, "inconclusive": eco_inc}, "r4_frozen_set": list(r4set),'''
B10 = '''            "echo_routes_outside_the_ledger": {"n": n_rt, "excluded_by_data": rt_exc, "inconclusive": rt_inc, "not_charges_of_the_theory": True, "routes": routes,
                                               "rule": str((pr["json"] or {}).get("rotas_regra") or ""), "sources_in_core_ok": sources_ok},
            "operator_decision_20261002": {"verbatim": _V383_OPERATOR_VERBATIM["decision_20261002"], "no_publish_verbatim": _V383_OPERATOR_VERBATIM["no_publish_20261002"], "option_chosen": _V383_OPTION_CHOSEN},
            "base_and_local_seal": {"base": up.get("base_versao"), "base_sha16": str(up.get("base_sha256") or "")[:16], "v382_local_only_sha16": str(v382l.get("sha256") or "")[:16],
                                    "v382_statute": str(v382l.get("estatuto") or "")},
            "r4_frozen_set": list(r4set),'''
REPS.append((A10, B10))

for a, b in REPS:
    n = s.count(a)
    assert n == 1, ("trecho velho nao ocorre exatamente uma vez", n, a[:120])
    s = s.replace(a, b)
ast.parse(s)
left = [l.strip()[:140] for l in s.split("\n") if re.search(r"\beco\b|eco_ext|eco_inc|V1\.3|V1_3|VINTE|== 20\b|== 19\b", l)]
open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
print("ok", P, len(s.encode("utf-8")), "B; trechos trocados:", len(REPS))
print("linhas ainda com eco/V1.3/vinte/20/19 (conferir a mao):"); [print("  ", x) for x in left]
