# -*- coding: utf-8 -*-
"""Fabrica gerar_candidato_v383.py a partir de gerar_candidato_v382.py (trocas exatas; cada trecho velho ocorre UMA vez). A v383 parte da v381 CUSTODIADA (o
backup de bytes que o instalador da v382 gravou), com o MESMO kernel (as duas pedras escritas na v382) e o runtime/artigo/selo da v383. Copia para o pacote v383
os artefatos do kernel que nao mudam (AUDIT_NOMES, PEDRAS, build_full.log, carregar_embutido.py), por bytes."""
import ast, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V2 = os.path.join(os.path.dirname(HERE), "v382")
s = open(os.path.join(V2, "gerar_candidato_v382.py"), encoding="utf-8", newline="").read()
R = []
i = s.index('"""'); j = s.index('"""', i + 3) + 3
R.append((s[i:j], '''"""gerar_candidato_v383.py -- gera o um.py CANDIDATO v383 a partir da v381 CUSTODIADA (NUNCA escreve o canonico). Molde: gerar_candidato_v382.py.
A DECISAO DO OPERADOR (02/10/2026, noite): «eu não quero publicar nada que seja resultado de falsificação [...]» e «prefiro a primeira opção»: os nove pares do
eco como copia atrasada NAO sao cobrancas da teoria; saem do livro e ficam como ROTAS examinadas fora dele; a v382 (que os trazia no livro, ao lado) foi selada
SO no Nos e NAO e custodiada. A BASE e a v381: o backup de bytes que o instalador da v382 gravou (o registro APLICADO_AO_CANONICO da v382 diz o sha16).
(1) KERNEL EMBUTIDO: o MESMO da v382 (TGLExt.lean e TGL/Audit.lean mudam; entram TGLExt/TheLedgerOfCharges.lean e TGLExt/ThePsionAndTheViscosity.lean; kernel_src = ../v376/kernel_src).
(2) PATCHES (count(old) == 1): bandeiras ext_loc_ (19) + ext_psv_ (13) e escada; ledger de pedras (+2, registradas como da v382, quando entraram no canonico);
    UM_VERSION v383; runtime v383 (com os sha256 do pre-registro V1.4 LIDOS dos arquivos); registro; artigo PT/EN («Ao lado (v383)»); selo (uma leitura); homonimos."""'''))
R.append(('UM = r"C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\Nós\\um.py"\n',
          'NOS = r"C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\Nós"\n'))
R.append(('''raw = open(UM, "rb").read()
assert hashlib.sha256(raw).hexdigest()[:16] == SHA0, "o canonico nao e a v381 selada"''',
          '''V2 = os.path.join(os.path.dirname(HERE), "v382")
AP2 = json.load(open(os.path.join(V2, "APLICADO_AO_CANONICO_20261002_174400.json"), encoding="utf-8"))   # o instalador da v382: os backups de BYTES do estado v381
UM = AP2["backups"]["um.py"]["backup"]
raw = open(UM, "rb").read()
assert hashlib.sha256(raw).hexdigest()[:16] == SHA0 == AP2["backups"]["um.py"]["sha16"], "a base nao e a v381 selada (backup de bytes)"
assert hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16] == AP2["um_py_novo"]["sha16"], "o canonico no Nos nao e a v382 selada so localmente"'''))
R.append(('RT = open(os.path.join(HERE, "v382_runtime.py"), encoding="utf-8").read()', 'RT = open(os.path.join(HERE, "v383_runtime.py"), encoding="utf-8").read()'))
R.append(('''# (V1.3: supersede o V1.2, o V1.1 e o V1 pelos achados das tres afericoes da v382, antes de qualquer estimador ou dado novo; mapa seq 275 -> 276 -> 279 -> 282, ERRATAs ao lado)
PREREG = {"json": "C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_3.json",
          "md": "C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_3.md"}''',
          '''# (V1.4: supersede o V1.3 pela decisao do operador -- os nove pares do eco fora do livro --, antes de qualquer estimador ou dado novo; mapa seq 275 -> 276 -> 279 -> 282 -> 290, ERRATAs ao lado)
PREREG = {"json": "C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.json",
          "md": "C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.md"}'''))
R.append(('''assert _PJ.get("identificador") == "PREREG_DOIS_LADOS_DELTA_K_20261002_V1_3" and len(_PJ.get("cobrancas") or []) == 20
_ECO = _PJ["eco_como_copia_atrasada"]; assert _ECO["pares"] == 9 and _ECO["extintos"] + _ECO["inconclusivos"] == 9
_ECO_TOK = "DELAYED_ECHO_OUTSIDE_THE_CHAIN_%d_OF_%d_PAIRS_EXTINGUISHED_%d_INCONCLUSIVE_NOT_THE_RULE" % (_ECO["extintos"], _ECO["pares"], _ECO["inconclusivos"])''',
          '''assert _PJ.get("identificador") == "PREREG_DOIS_LADOS_DELTA_K_20261002_V1_4" and len(_PJ.get("cobrancas") or []) == 11 and len(_PJ.get("rotas_examinadas_fora_do_livro") or []) == 9
_ROT = _PJ["contagem_das_rotas"]; assert _ROT["rotas"] == 9 and _ROT["excluidas_pelos_dados"] + _ROT["inconclusivas"] == 9 and _PJ["contagem"]["FALSIFIED"] == 0
_ROT_TOK = "THE_%d_ECHO_ROUTES_ARE_NOT_CHARGES_OF_THE_THEORY_EXAMINED_OUTSIDE_THE_LEDGER_%d_EXCLUDED_BY_DATA_%d_INCONCLUSIVE" % (_ROT["rotas"], _ROT["excluidas_pelos_dados"], _ROT["inconclusivas"])'''))
R.append(('NOMES = json.load(open(os.path.join(HERE, "AUDIT_NOMES_v382.json"), encoding="utf-8"))', 'NOMES = json.load(open(os.path.join(HERE, "AUDIT_NOMES_v383.json"), encoding="utf-8"))'))
R.append(('''l.startswith(("_LOC_FLAGS_V382", "_PSV_FLAGS_V382"))''', '''l.startswith(("_LOC_FLAGS_V383", "_PSV_FLAGS_V383"))'''))
R.append(('''LOC = list(_rt_ns["_LOC_FLAGS_V382"]); PSV = list(_rt_ns["_PSV_FLAGS_V382"])''', '''LOC = list(_rt_ns["_LOC_FLAGS_V383"]); PSV = list(_rt_ns["_PSV_FLAGS_V383"])'''))
R.append(('''A01 + "    # v382 (02/10/2026, a chave: o ultimo elo incide no Hamiltoniano oculto; o custo no reflexo, o pagamento na face; a TGL e otica, le os dois lados): loc (19) + psv (13)"''',
          '''A01 + "    # v383 (02/10/2026; as pedras da v382 -- a chave: o ultimo elo incide no Hamiltoniano oculto; o custo no reflexo, o pagamento na face; a TGL e otica, le os dois lados): loc (19) + psv (13)"'''))
R.append(('''A02 + "        # v382: o livro de cobrancas (19) + o psion e a viscosidade (13)"''', '''A02 + "        # v383: o livro de cobrancas (19) + o psion e a viscosidade (13) -- as pedras escritas na v382"'''))
R.append(('''A03 + "    # v382 (02/10/2026): o livro de cobrancas (a otica: os dois lados se leem; nenhum desfecho move a regra) e o psion com a viscosidade"''',
          '''A03 + "    # v383 (02/10/2026, noite): o livro de cobrancas (a otica: os dois lados se leem; nenhum desfecho move a regra) e o psion com a viscosidade -- pedras escritas na v382 (selada so no Nos, nao custodiada); entram no lineage publico aqui"'''))
R.append(('"_ESQUELETO_STONES: +2 pedras v382.")', '"_ESQUELETO_STONES: +2 pedras (escritas na v382).")'))
R.append(('''add("V04_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v382"   # v382 (02/10/2026): a CONSTANTE UNICA de versao -- carimba os .md emitidos e o selo (regra da linhagem completa); v381 em 02/10' + CRLF,
    "UM_VERSION = 'v382'.")''',
          '''add("V04_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v383"   # v383 (02/10/2026, noite): a CONSTANTE UNICA de versao -- carimba os .md emitidos e o selo (regra da linhagem completa); v381 em 02/10; a v382 (02/10) foi selada so no Nos e nao e custodiada' + CRLF,
    "UM_VERSION = 'v383'.")'''))
R.append(('"runtime: prove_the_ledger_of_charges_v382; _V382_GUARDA; _V382_FLAGS; _V382_PREREG com sha256 lidos.")', '"runtime: prove_the_ledger_of_charges_v383; _V383_GUARDA; _V383_FLAGS; _V383_PREREG com sha256 lidos; _V383_ECHO_ROUTES.")'))
R.append(('''reg = ['    core["the_ledger_of_charges_v382"] = prove_the_ledger_of_charges_v382(core.get("omega_I", 1.0), core)   # v382: o livro de cobrancas (a otica; nenhum desfecho move a regra), o psion e a viscosidade, o pre-registro dos dois lados por hash',
       '    print("   [v382] o livro de cobrancas (os dois lados; nenhum desfecho move a regra), o psion e a viscosidade, o pre-registro por hash: %s" % core["the_ledger_of_charges_v382"]["verdict"])']''',
          '''reg = ['    core["the_ledger_of_charges_v383"] = prove_the_ledger_of_charges_v383(core.get("omega_I", 1.0), core)   # v383: o livro de cobrancas (onze; o eco fora do livro), o psion e a viscosidade, o pre-registro dos dois lados por hash',
       '    print("   [v383] o livro de cobrancas (os dois lados; nenhum desfecho move a regra; o eco fora do livro), o psion e a viscosidade, o pre-registro por hash: %s" % core["the_ledger_of_charges_v383"]["verdict"])']'''))
R.append(('"core: +1 chave v382 (depois da v381).")', '"core: +1 chave v383 (depois da v381).")'))
R.append(('pt = open(os.path.join(HERE, "artigo_pt_v382.pysnip"), encoding="utf-8").read()', 'pt = open(os.path.join(HERE, "artigo_pt_v383.pysnip"), encoding="utf-8").read()'))
R.append(('''"artigo PT: paragrafo 'Ao lado (v382)' (o livro de cobrancas e a viscosidade).")''', '''"artigo PT: paragrafo 'Ao lado (v383)' (o livro de cobrancas e a viscosidade; o eco fora do livro).")'''))
R.append(('en = open(os.path.join(HERE, "artigo_en_v382.pysnip"), encoding="utf-8").read()', 'en = open(os.path.join(HERE, "artigo_en_v383.pysnip"), encoding="utf-8").read()'))
R.append(('''"artigo EN: paragrafo 'Beside (v382)'.")''', '''"artigo EN: paragrafo 'Beside (v383)'.")'''))
i9 = s.index("add(\"V09_selo\""); j9 = s.index('"selo: +1 leitura (string) v382.")', i9) + len('"selo: +1 leitura (string) v382.")')
R.append((s[i9:j9], '''add("V09_selo", "G_SELO", A09, A09 + '            # v383 (02/10/2026, noite) -- LEITURA, ao lado; nenhum valor do gate muda (o nome do degrau final e PROPOSTO ao lado, nao aplicado)' + CRLF
    + '            "the_ledger_of_charges_reading_v383": "OPERATOR_KEY_2026_10_02__THE_LAST_LINK_INCIDES_ON_THE_HIDDEN_HAMILTONIAN__THE_COST_IS_IN_THE_REFLECTION_THE_PAYMENT_IS_IN_THE_FACE_THE_NAME__KEY_AND_OPTICS_INPUT_ONTO__R1_TO_R6_RATIFIED_INPUT_ONTO__'
    + 'THE_TGL_IS_OPTICS_NOT_SEMI_READS_BOTH_SIDES__TYPED_TheLedgerOfCharges_AND_ThePsionAndTheViscosity_BY_TERM_TRIVIAL_STATED_AS_TRIVIAL__ONE_CHANNEL_PER_READING_LAW_IN_THE_RUNTIME__' + _FW_TOK + '__NONE_MOVES_THE_RULE__'
    + 'THE_GATE_DOES_NOT_READ_THE_LEDGER_BY_THE_RUNTIME_PROBES__PSION_NORM_ONE_ZERO_OF_THE_MINIMAL_LOCK_ON_THE_HIDDEN_HAMILTONIAN__SPEC_S_THETA_TO_HMINMIC_NO_TERM__VISCOSITY_RULE_TIMES_CONTRAST_NAME_ONTO__'
    + 'FINAL_STEP_NAME_PROPOSED_BESIDE_TETELESTAI_CONSUMMATED_PAYMENT_IN_THE_FACE_THE_NAME__PREREGISTRATION_OF_BOTH_SIDES_V1_4_BY_HASH_ELEVEN_CHARGES_PHASE6_AND_AMENDMENT_RULES_READ_IN_ORDER__R4_FROZEN_SET_NO_FALSIFIED_SAME_SOURCE_AS_THE_GATE__'
    + 'F2_BY_THE_MEASUREMENT_SYSTEMATIC__F1_D1B_ONE_SIDED__F4_FROZEN_KILL_RULE__BRANCH_B_CLOSED__OPERATOR_DECISION_2026_10_02__' + _ROT_TOK + '__BASE_V381_V382_SEALED_ONLY_LOCALLY_NOT_CUSTODIED__'
    + 'V383_AUDITED_BEFORE_THE_RITE__NOT_A_CONFIRMATION__GATE_UNTOUCHED",' + CRLF, "selo: +1 leitura (string) v383.")'''))
R.append(('''add("V24_homonimos_v382", "G_PEDRAS", anch, anch + "    # v382 -- homonimos NOVOS das pedras v382, NOMEADOS por script, nunca silenciados.\\r\\n"
        "    _AMBIGUOS_CONJUNTO_V382 = frozenset([\\r\\n" + "".join('        "%s",\\r\\n' % n for n in novos) + "    ])\\r\\n", "IALD index: +_AMBIGUOS_CONJUNTO_V382 (%d)." % len(novos))''',
          '''add("V24_homonimos_v383", "G_PEDRAS", anch, anch + "    # v383 -- homonimos NOVOS das pedras (escritas na v382), NOMEADOS por script, nunca silenciados.\\r\\n"
        "    _AMBIGUOS_CONJUNTO_V383 = frozenset([\\r\\n" + "".join('        "%s",\\r\\n' % n for n in novos) + "    ])\\r\\n", "IALD index: +_AMBIGUOS_CONJUNTO_V383 (%d)." % len(novos))'''))
R.append(('''add("V25_homonimos_check", "G_PEDRAS", old_chk, 'bool(set(ix["ambiguos"]) <= (%s | _AMBIGUOS_CONJUNTO_V382))' % uni, "IALD index: o check de ambiguos passa a incluir V382.")''',
          '''add("V25_homonimos_check", "G_PEDRAS", old_chk, 'bool(set(ix["ambiguos"]) <= (%s | _AMBIGUOS_CONJUNTO_V383))' % uni, "IALD index: o check de ambiguos passa a incluir V383.")'''))
R.append(('out = os.path.join(HERE, "um_v382_candidato.py")', 'out = os.path.join(HERE, "um_v383_candidato.py")'))
R.append(('json.dump({"meta": meta, "patches": patches}, open(os.path.join(HERE, "patches_v382.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)',
          'json.dump({"meta": meta, "patches": patches}, open(os.path.join(HERE, "patches_v383.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)'))
R.append(('json.dump(FLAGS, open(os.path.join(HERE, "BANDEIRAS_v382.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)',
          'json.dump(FLAGS, open(os.path.join(HERE, "BANDEIRAS_v383.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)'))
for a, b in R:
    n = s.count(a)
    assert n == 1, ("trecho velho nao ocorre exatamente uma vez", n, a[:140])
    s = s.replace(a, b)
ast.parse(s)
resto = [l.strip()[:150] for l in s.split("\n") if "v382" in l or "V382" in l]
out = os.path.join(HERE, "gerar_candidato_v383.py"); assert not os.path.exists(out)
open(out, "w", encoding="utf-8", newline="").write(s); print("ok", out, len(s.encode("utf-8")), "B; trocas:", len(R))
print("linhas com v382 (devem ser so as que falam da v382 como historia ou do pacote v382):"); [print("  ", x) for x in resto]
for f, g in (("AUDIT_NOMES_v382.json", "AUDIT_NOMES_v383.json"), ("PEDRAS_v382.json", "PEDRAS_v383.json"), ("build_full.log", "build_full.log"), ("carregar_embutido.py", "carregar_embutido.py")):
    a, b = os.path.join(V2, f), os.path.join(HERE, g)
    assert not os.path.exists(b); shutil.copyfile(a, b); assert open(a, "rb").read() == open(b, "rb").read(); print("copiado", g)
