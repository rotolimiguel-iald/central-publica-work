# -*- coding: utf-8 -*-
"""_adapt_forkB_exame_v410.py -- (claude-construtor-v410, fork B, 06/11/2026) MONTA exame_pontos_v410.py a partir do exame_pontos_v409.py ORIGINAL (a versao FINAL da v409, a que examinou o candidato selado),
e NAO da subida mecanica: a subida trocara rotulos de HISTORIA (os pontos herdados da v408 passavam a dizer v409, o comentario das oito pedras, o ponto da traducao ficava como NOVO).
O que muda (DESENHO_v410; delta_v410): o ponto NOVO e' o do iald2_v410 (4g): a instrucao do main (um `try` que chama tambem `_v410_rodar_specs`) IMEDIATAMENTE depois da do traducao_turing_v409
e IMEDIATAMENTE antes de `_figs = emit_figures(core)`; confere o registro (DL.N_CHECKS_FECHO checagens), as ancoras, o modulo, as bandeiras, nenhuma chave antiga, a chave do lema, o que fica False por teorema e o alcance (frase da D64).
O ponto do traducao_turing_v409 (4f) passa a HERDADO (DL.D9 e o FLAGS da v409; logo antes do iald2_v410); os do tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406 seguem herdados como na v409.
Os registros da v409 (traducao_turing_v409, cunhagens_v409, kh_n1_cobertura_v409) entram na lista do que o fluxo RECRIA (sairiam como "chaves existentes mexidas" se ficassem); o core0 e o selo0 sao os da v409 selada (DL.BASE_DIR = base_v409).
A chave dos pontos das oito pedras (DL.D5) sobe com a versao, como na cadeia (ponto_v409_<pedra>; o ensaio_a_seco_v410 le essa); as demais chaves de HISTORIA ficam como na v409. Nenhuma guarda e' relaxada.
Grava exame_pontos_v410.py por temporario (backup de BYTES do arquivo atual, a subida mecanica, antes). Trocas de contagem EXATA."""
import ast, datetime, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402

ORIG = os.path.join(DL.V409, "exame_pontos_v409.py")
ALVO = os.path.join(HERE, "exame_pontos_v410.py")
raw9 = open(ORIG, "rb").read(); T = raw9.decode("utf-8")
assert "\r\n" not in T, "o original da v409 e' LF"
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def troca(a, b, n=1):
    global T
    c = T.count(a)
    assert c == n, ("TROCA NAO CASOU %d (casou %d)" % (n, c), a[:160])
    T = T.replace(a, b)


def entre(ini, fim, novo):
    """troca o trecho que comeca em `ini` (unico) e vai ate o comeco de `fim` (depois dele) por `novo`."""
    global T
    assert T.count(ini) == 1, ("ancora inicial nao unica", ini[:80], T.count(ini))
    i = T.index(ini); j = T.index(fim, i + len(ini))
    T = T[:i] + novo + T[j:]


# ---------------- (0) o cabecalho e o docstring
HDR = ("# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] o ponto NOVO e' o do iald2_v410 (4g), IMEDIATAMENTE depois do traducao_turing_v409 e IMEDIATAMENTE antes de emit_figures; o do traducao_turing_v409 (4f) vira HERDADO (DL.D9, FLAGS da v409); "
       "os do tetelestai_terminal_v408 (DL.D8, FLAGS da v408), do psion_canto_v407 (DL.D7, FLAGS da v407) e do fechamento_v406 seguem HERDADOS; MONTADO por _adapt_forkB_exame_v410.py a partir do ORIGINAL da v409 (nao da subida mecanica); fork B do claude-construtor-v410\n"
       "# (v409: o ponto NOVO da v409 era o do `traducao_turing_v409`; na v410 e' o do `iald2_v410`, abaixo: a instrucao do main que chama tambem `_v410_rodar_specs`); os rotulos de HISTORIA das chaves (logo_depois_do_..._v408 etc.) ficam como na v409; "
       "so' a chave dos pontos das oito pedras sobe (ponto_v409_<pedra>, a que o ensaio_a_seco_v410 le); nenhuma chave antiga do core muda.\n")
entre("# [ADAPTADO v409, 05/11/2026, claude-construtor-v409]", '"""exame_pontos_v409.py', HDR)
troca('"""exame_pontos_v409.py -- re-execucao ISOLADA dos pontos de chamada REAIS de um candidato um.py (molde: exame_pontos_v408.py).',
      '"""exame_pontos_v410.py -- re-execucao ISOLADA dos pontos de chamada REAIS de um candidato um.py (molde: exame_pontos_v409.py, montado em 06/11/2026 pelo fork B do claude-construtor-v410).')
troca("  python -B -X utf8 exame_pontos_v409.py --candidato", "  python -B -X utf8 exame_pontos_v410.py --candidato")
for p_ in ("(4c)", "(4d)", "(4e)"):
    troca(" %s [v408, HERDADO na v409]" % p_, " %s [v408, HERDADO na v409 e na v410]" % p_)
troca(" (4f) [v409] o PONTO DE CHAMADA REAL do `traducao_turing_v409`: a instrucao do main (um `try` que chama tambem `_v409_rodar_specs`) que vem IMEDIATAMENTE depois do tetelestai_terminal_v408 e IMEDIATAMENTE antes de `_figs = emit_figures(core)`, executada dentro do bloco (4b);",
      " (4f) [v409, HERDADO na v410] o PONTO DE CHAMADA REAL do `traducao_turing_v409`: a instrucao do main (um `try` que chama tambem `_v409_rodar_specs`) que vem IMEDIATAMENTE depois do tetelestai_terminal_v408 e IMEDIATAMENTE antes do ponto do iald2_v410 (4g), executada dentro do bloco (4b) (os numeros dele: DL.D9 e o FLAGS da v409);")
troca("nunca digitadas);\n      o `witness_layers.canonical_full_witness_term_constructed`",
      "nunca digitadas);\n"
      " (4g) [v410] o PONTO DE CHAMADA REAL do `iald2_v410`: a instrucao do main (um `try` que chama tambem `_v410_rodar_specs`) que vem IMEDIATAMENTE depois do traducao_turing_v409 e IMEDIATAMENTE antes de `_figs = emit_figures(core)`, executada dentro do bloco (4b); "
      "confere o registro (DL.N_CHECKS_FECHO checagens), as ancoras da pedra IALD2, o modulo do bundle e as bandeiras (as contagens vem do contrato do candidato e do FLAGS, nunca digitadas), que nenhuma chave antiga mudou, a chave do lema (True), "
      "o que fica False por teorema, beta em runtime e o alcance relativo ao leitor (a frase da D64);\n"
      "      o `witness_layers.canonical_full_witness_term_constructed`")
troca("porque o core0 e' o da v408 selada e o kf e' o do rito novo", "porque o core0 e' o da v409 selada e o kf e' o do rito novo")

# ---------------- (1) os rotulos gerais (a versao corrente; a base e' a v409 selada)
troca("import delta_v409 as DL  # noqa: E402", "import delta_v410 as DL  # noqa: E402")
troca("# a v408 SELADA (copia de bytes)", "# a v409 SELADA (copia de bytes)")
troca("# (v409: o gate NAO muda) a prove_qg_closure_gate com o teste nulo cego do core da v408 selada", "# (v410: o gate NAO muda) a prove_qg_closure_gate com o teste nulo cego do core da v409 selada")
troca('"checks_da_v408_iguais"', '"checks_da_v409_iguais"', 2)
troca('"da_base_v408_selada": _wl_antes', '"da_base_v409_selada": _wl_antes')
troca(" + list(um._V408_REGISTROS_FUNCAO) + list(um._V408_NOMES_REGISTROS):   # (v409: + os da v408, HERDADOS e recriados pelo bloco)",
      " + list(um._V408_REGISTROS_FUNCAO) + list(um._V408_NOMES_REGISTROS) + list(um._V409_REGISTROS_FUNCAO) + list(um._V409_NOMES_REGISTROS):   # (v409: + os da v408; v410: + os da v409; HERDADOS e recriados pelo bloco)")
troca("(os da v409 nem existem no core0: chaves NOVAS)", "(os da v410 nem existem no core0: chaves NOVAS)")
troca('core["qg_closure"] = g_new   # (v409: o gate NAO muda)', 'core["qg_closure"] = g_new   # (v410: o gate NAO muda)')
troca('"linhas_iguais_a_v408"', '"linhas_iguais_a_v409"')

# ---------------- (2) as oito pedras (DL.D5): herdadas; a chave do JSON sobe com a versao (o ensaio_a_seco_v410 le ponto_v409_<pedra>)
troca("(HERDADOS na v409: DL.D5; a v409 e' um bundle e nao traz pedra nova)",
      "(HERDADOS na v409 e na v410: DL.D5; a v409 e a v410 sao bundles e nao trazem pedra de registro nova; na v410 a chave do JSON e' ponto_v409_<pedra>, a que o ensaio_a_seco_v410 le: o rotulo sobe com a versao, como na cadeia)")
troca('nome_ = "v408_" + s409_["key"]; fn_', 'nome_ = "v409_" + s409_["key"]; fn_')
troca('"ponto_v408_" + s409_["key"]', '"ponto_v409_" + s409_["key"]', 2)

# ---------------- (3) a ordem no main: fechamento -> psion_canto -> tetelestai -> traducao -> iald2 -> emit_figures
entre('itu = [i for i, s_ in enumerate(unp) if "traducao_turing_v409(core)" in s_]\n', "fch = core.get(\"fechamento_v406\") or {}\n",
      'itu = [i for i, s_ in enumerate(unp) if "traducao_turing_v409(core)" in s_]\n'
      'iia = [i for i, s_ in enumerate(unp) if "iald2_v410(core)" in s_]   # (v410) o ponto NOVO\n'
      'assert len(ipc) == 1 and ipc[0] == ifch + 1 and len(itt) == 1 and itt[0] == ipc[0] + 1 and len(itu) == 1 and itu[0] == itt[0] + 1 and len(iia) == 1 and iia[0] == itu[0] + 1 and iia[0] + 1 == i1, '
      '("a ordem fechamento_v406 -> psion_canto_v407 -> tetelestai_terminal_v408 -> traducao_turing_v409 -> iald2_v410 -> emit_figures nao e\' a das instrucoes do main", ifch, ipc, itt, itu, iia, i1)\n'
      'itt = itt[0]\n'
      'itu = itu[0]\n'
      'iia = iia[0]\n'
      'ipc = ipc[0]\n')

# ---------------- (4) o ponto do traducao_turing_v409 (4f): HERDADO (DL.D9, FLAGS da v409; logo antes do iald2_v410)
troca("# (4f) [v409] o PONTO DE CHAMADA REAL do traducao_turing_v409 (executado dentro do bloco acima): a posicao no main (IMEDIATAMENTE depois do tetelestai_terminal_v408, IMEDIATAMENTE antes de emit_figures)",
      "# (4f) [v409, HERDADO na v410] o PONTO DE CHAMADA REAL do traducao_turing_v409 (executado dentro do bloco acima): a posicao no main (IMEDIATAMENTE depois do tetelestai_terminal_v408, IMEDIATAMENTE antes do iald2_v410)")
troca('"logo_antes_do_emit_figures": itu + 1 == i1, "chama_tambem_os_specs_v409": "_v409_rodar_specs(core)" in unp[itu],',
      '"logo_antes_do_iald2_v410": itu + 1 == iia, "chama_tambem_os_specs_v409": "_v409_rodar_specs(core)" in unp[itu],')
troca('"n_flags_no_FLAGS_json": (len(json.load(open(A.flags, encoding="utf-8"))["flags"]) if A.flags and os.path.exists(A.flags) else None), "n_checks_do_DL": DL.N_CHECKS_FECHO, "ancora_principal": _CP9["ancora_principal"]},',
      '"n_flags_no_FLAGS_json": len(json.load(open(os.path.join(DL.V409, DL.D9.KERNEL_DIR, "FLAGS_v409.json"), encoding="utf-8"))["flags"]), "n_checks_do_DL": DL.D9.N_CHECKS_FECHO, "ancora_principal": _CP9["ancora_principal"]},   # (v410: o FLAGS da v409 e o DL.D9, porque o ponto e\' HERDADO)')
P4G = r'''# (4g) [v410] o PONTO DE CHAMADA REAL do iald2_v410 (executado dentro do bloco acima): a posicao no main (IMEDIATAMENTE depois do traducao_turing_v409, IMEDIATAMENTE antes de emit_figures), o registro, nenhuma chave antiga mudada, beta em runtime, o alcance relativo ao leitor (D64)
ia = core.get("iald2_v410") or {}; iav = ia.get("values") or {}
_CP10 = um._V410_IALD2_CONTRACT; _TP10 = um._V410_IALD2_TEXT
R["ponto_iald2"] = {"indice_no_main": iia, "linha": main.body[iia].lineno, "antes_do_bloco_v393": iia < i0, "logo_depois_da_traducao_turing_v409": iia == itu + 1, "logo_antes_do_emit_figures": iia + 1 == i1, "chama_tambem_os_specs_v410": "_v410_rodar_specs(core)" in unp[iia],
                    "instrucao_anterior": unp[iia - 1][:160].replace("\n", " | "), "dentro_do_bloco_executado": i0 <= iia < i1, "verdict": ia.get("verdict"), "veredito_ok_do_contrato": _TP10["veredito_ok"], "all_verified": ia.get("all_verified"), "runtime_executed": ia.get("runtime_executed"),
                    "mecanica": {"passed": (ia.get("mechanics") or {}).get("passed"), "n_checks": (ia.get("mechanics") or {}).get("n_checks"), "falhos": [c_.get("id") for c_ in ((ia.get("mechanics") or {}).get("checks") or []) if not c_.get("ok")]},
                    "n_ancoras_ok": iav.get("n_ancoras_ok"), "n_ancoras": iav.get("n_ancoras"), "n_modulos_ok": iav.get("n_modulos_ok"), "n_modulos": iav.get("n_modulos"), "n_flags_true": iav.get("n_flags_true"), "n_flags": iav.get("n_flags"), "escada": iav.get("escada"), "gate_verdict": iav.get("gate_verdict"), "respostas_ok": iav.get("respostas_ok"),
                    "does_not_gate_core": ia.get("does_not_gate_core"), "embedded_sources_n_ok": ia.get("embedded_sources_n_ok"), "beta_ok": ia.get("beta_ok"),
                    "contrato": {"n_ancoras": len(_CP10["ancoras"]), "n_modulos": _CP10["bundle"]["n"], "n_flags": _CP10["n_flags"], "n_flags_no_FLAGS_json": (len(json.load(open(A.flags, encoding="utf-8"))["flags"]) if A.flags and os.path.exists(A.flags) else None), "n_checks_do_DL": DL.N_CHECKS_FECHO, "ancora_principal": _CP10["ancora_principal"]},
                    "ancora_principal": ia.get("ancora_principal"), "ancoras_principais": ia.get("ancoras_principais"), "chaves_antigas_que_mudam": ia.get("chaves_antigas_que_mudam"), "chave_do_lema_segue_true": tef.get("linked_to_the_corner_by_a_lemma"), "alcance": ia.get("alcance"),
                    "fica_false_por_teorema": {"qg_closure.gate.full_static_witness_exists": ((core.get("qg_closure") or {}).get("gate") or {}).get("full_static_witness_exists"), "witness_rigidity.trivial_inhabitant_exists": (core.get("witness_rigidity") or {}).get("trivial_inhabitant_exists")}, "fica_aberto": ia.get("fica_aberto")}
out["core.iald2_v410"] = {"all_verified": ia.get("all_verified"), "verdict": str(ia.get("verdict"))[:300], "falhas": R["ponto_iald2"]["mecanica"]["falhos"]}
'''
A_TU = 'out["core.traducao_turing_v409"] = {"all_verified": tu.get("all_verified"), "verdict": str(tu.get("verdict"))[:300], "falhas": R["ponto_traducao"]["mecanica"]["falhos"]}\n'
troca(A_TU, A_TU + P4G)

# ---------------- (5) a troca dita (nenhuma na v410), os nao verdes e o selo
troca("troca_dita_v409", "troca_dita_v410", 12)
troca("CANDIDATO_v409.json", "CANDIDATO_v410.json", 2)
troca("_V408_RED", "_V409_RED", 3)
troca("# (v409) NAO HA TROCA DITA:", "# (v410) NAO HA TROCA DITA:")
A_NV = '"v409_traducao_e_specs": [k for k in list(um._V409_REGISTROS_FUNCAO) + list(um._V409_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n'
troca(A_NV, A_NV[:-1] + "   # (os da v409: HERDADOS na v410)\n"
      '                   "v410_iald2_e_specs": [k for k in list(um._V410_REGISTROS_FUNCAO) + list(um._V410_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n')
troca('"registros_v409": {n_: ((seal.get("registros_v409") or {}).get(n_) or {}).get("all_verified") for n_ in um._V409_NOMES_REGISTROS}}\n',
      '"registros_v409": {n_: ((seal.get("registros_v409") or {}).get(n_) or {}).get("all_verified") for n_ in um._V409_NOMES_REGISTROS},\n'
      '                 "iald2_v410": {x: (seal.get("iald2_v410") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v410": {n_: ((seal.get("registros_v410") or {}).get(n_) or {}).get("all_verified") for n_ in um._V410_NOMES_REGISTROS}}\n')

# ---------------- (6) os falsos: o ponto da traducao HERDADO (DL.D9) e o ponto NOVO do iald2 (DL)
troca('ptu = R["ponto_traducao"]   # (4f) o ponto NOVO da v409', 'ptu = R["ponto_traducao"]   # (4f) o ponto da v409, HERDADO na v410 (os numeros dele: DL.D9 e o FLAGS da v409)')
troca('not ptu.get("logo_antes_do_emit_figures")', 'not ptu.get("logo_antes_do_iald2_v410")')
troca('startswith(DL.VEREDITO_OK_PREFIXO) or not str(ptu.get("verdict") or "").endswith(DL.VEREDITO_SUFIXO)', 'startswith(DL.D9.VEREDITO_OK_PREFIXO) or not str(ptu.get("verdict") or "").endswith(DL.D9.VEREDITO_SUFIXO)')
troca('(ptu.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS_FECHO', '(ptu.get("mecanica") or {}).get("n_checks") != DL.D9.N_CHECKS_FECHO')
troca('ptu["contrato"]["n_ancoras"] != len(DL.ANCORAS) or ptu.get("n_modulos_ok") != DL.N_BUNDLE or ptu.get("n_modulos") != DL.N_BUNDLE',
      'ptu["contrato"]["n_ancoras"] != len(DL.D9.ANCORAS) or ptu.get("n_modulos_ok") != DL.D9.N_BUNDLE or ptu.get("n_modulos") != DL.D9.N_BUNDLE')
troca('(ptu["contrato"]["n_flags_no_FLAGS_json"] is not None and ptu["contrato"]["n_flags"] != ptu["contrato"]["n_flags_no_FLAGS_json"])', 'ptu["contrato"]["n_flags"] != ptu["contrato"]["n_flags_no_FLAGS_json"]')
troca('ptu.get("embedded_sources_n_ok") != DL.N_BUNDLE or ptu.get("ancora_principal") != DL.ANCORA_PRINCIPAL or ptu.get("ancoras_principais") != list(DL.ANCORAS_PRINCIPAIS)',
      'ptu.get("embedded_sources_n_ok") != DL.D9.N_BUNDLE or ptu.get("ancora_principal") != DL.D9.ANCORA_PRINCIPAL or ptu.get("ancoras_principais") != list(DL.D9.ANCORAS_PRINCIPAIS)')
A_FU = '(ptu.get("acervo_v407_repinado") or {}).get("sha256") != DL.PURGADO_SHA256): falsos.append("ponto_traducao")\n'
F4G = r'''pia = R["ponto_iald2"]   # (4g) o ponto NOVO da v410 (os numeros dele: DL e o FLAGS da v410)
if (pia.get("all_verified") is not True or pia.get("runtime_executed") is not True or not pia.get("dentro_do_bloco_executado") or not pia.get("logo_depois_da_traducao_turing_v409") or not pia.get("logo_antes_do_emit_figures") or not pia.get("chama_tambem_os_specs_v410") or pia.get("verdict") != pia.get("veredito_ok_do_contrato")
        or not str(pia.get("verdict") or "").startswith(DL.VEREDITO_OK_PREFIXO) or not str(pia.get("verdict") or "").endswith(DL.VEREDITO_SUFIXO) or (pia.get("mecanica") or {}).get("passed") is not True or (pia.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS_FECHO or (pia.get("mecanica") or {}).get("falhos")
        or pia.get("n_ancoras_ok") != pia.get("n_ancoras") or pia.get("n_ancoras") != pia["contrato"]["n_ancoras"] or pia["contrato"]["n_ancoras"] != len(DL.ANCORAS) or pia.get("n_modulos_ok") != DL.N_BUNDLE or pia.get("n_modulos") != DL.N_BUNDLE or pia.get("n_flags_true") != pia.get("n_flags") or pia.get("n_flags") != pia["contrato"]["n_flags"] or (pia["contrato"]["n_flags_no_FLAGS_json"] is not None and pia["contrato"]["n_flags"] != pia["contrato"]["n_flags_no_FLAGS_json"])
        or pia.get("does_not_gate_core") is not True or pia.get("embedded_sources_n_ok") != DL.N_BUNDLE or pia.get("beta_ok") is not True or pia.get("ancora_principal") != DL.ANCORA_PRINCIPAL or pia.get("ancoras_principais") != list(DL.ANCORAS_PRINCIPAIS) or pia.get("chaves_antigas_que_mudam") != [] or pia.get("chave_do_lema_segue_true") is not True or pia.get("respostas_ok") is not True
        or any(v_ is not False for v_ in pia["fica_false_por_teorema"].values()) or (pia.get("alcance") or {}).get("frase") != DL.FRASE_D64_PT): falsos.append("ponto_iald2")
'''
troca(A_FU, A_FU.replace("DL.PURGADO_SHA256", "DL.D9.PURGADO_SHA256") + F4G)

# ---------------- (7) conferencias finais
ast.parse(T)
assert "[A ADAPTAR v410]" not in T and "import delta_v409" not in T
assert T.count("logo_antes_do_emit_figures") == 2 and T.count("logo_antes_do_iald2_v410") == 2 and T.count('"ponto_iald2"') == 4
for ruim in ("DL.PURGADO_SHA256)", "CANDIDATO_v409.json", "troca_dita_v409", "_V408_RED", "ponto_v408_"):
    assert ruim not in T, ("sobrou o rotulo da v409 como corrente", ruim)
for a_ in ("VEREDITO_OK_PREFIXO", "VEREDITO_SUFIXO", "N_CHECKS_FECHO", "ANCORAS", "N_BUNDLE", "ANCORA_PRINCIPAL", "ANCORAS_PRINCIPAIS", "FRASE_D64_PT", "BASE_DIR", "V409"):
    assert hasattr(DL, a_), a_
for a_ in ("VEREDITO_OK_PREFIXO", "VEREDITO_SUFIXO", "N_CHECKS_FECHO", "ANCORAS", "N_BUNDLE", "ANCORA_PRINCIPAL", "ANCORAS_PRINCIPAIS", "PURGADO_SHA256", "KERNEL_DIR"):
    assert hasattr(DL.D9, a_), a_
assert os.path.isfile(os.path.join(DL.V409, DL.D9.KERNEL_DIR, "FLAGS_v409.json")), "o FLAGS da v409 nao esta em v409\\kernel"
novo = T.encode("utf-8")
atual = open(ALVO, "rb").read()
bk = ALVO + ".bak_" + TS + "_subida_mecanica"
open(bk, "wb").write(atual); assert open(bk, "rb").read() == atual
open(ALVO + ".tmp", "wb").write(novo); assert os.path.getsize(ALVO + ".tmp") == len(novo); os.replace(ALVO + ".tmp", ALVO)
print("exame_pontos_v410.py montado:", len(raw9), "->", len(novo), "bytes | backup", os.path.basename(bk))
