# -*- coding: utf-8 -*-
"""_adapt_forkB_conferir_rito_v410.py -- (claude-construtor-v410, fork B, 06/11/2026) MONTA conferir_rito_v410.py a partir do conferir_rito_v409.py ORIGINAL (a versao FINAL da v409, a que conferiu o rito selado), e
NAO da subida mecanica: a subida trocara rotulos de HISTORIA (ESP["estrelas_v408"] -> "_v409", RN408 -> RN409 sobre ESP["registros_v408"], os blocos herdados da v408 apontando para a v409) e deixara o bloco do registro NOVO da v409 com rotulo v410.
O que muda (DESENHO_v410 e o AO LADO; delta_v410): o registro com FUNCAO NOVO e' iald2_v410 (_iald2_ok: DL.N_CHECKS_FECHO checagens, as ancoras da pedra IALD2, 1 modulo, a ancora principal o_enunciado, nenhuma chave antiga, as respostas do operador,
a instancia SAT da v409 decidida, o alcance relativo ao leitor da D64); o da v409, traducao_turing_v409, passa a HERDADO (_traducao409_ok, com DL.D9 e as chaves _v409 dos ESPERADOS); tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406 seguem herdados;
os vereditos de BASE passam a ser os da v409 selada (ESP["vereditos_v409"], qg_closure_v409, neutrino_frozen_hash_v409, flags_true_v409, axiom_report_v409_n, selo_registros_v409, runtime_seals_v409, what_remains_v409, veredito_da_falsidade_v409);
os registros por spec: RN409 (da v409) RECRIADOS e RN410 NOVOS (cunhagens_v410, kh_n1_cobertura_v410); os bundles anteriores (2 da v409, 4 da v408, 9 da v407, 301 da v406) como registro; a secao v410 do artigo antes da da v409; a linha do .md da v410 antes da da v409.
NENHUMA guarda e' relaxada: cada DEVE/NAO da v409 fica, com o nome certo, e os da v410 entram. As chaves dos ESPERADOS que este conferidor LE sao listadas no fim (para o gerar_esperados_v410).
Grava conferir_rito_v410.py por temporario (backup de BYTES do arquivo atual, a subida mecanica, antes). Trocas de contagem EXATA."""
import ast, datetime, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402

ORIG = os.path.join(DL.V409, "conferir_rito_v409.py")
ALVO = os.path.join(HERE, "conferir_rito_v410.py")
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
HDR = ('# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] a v410 (IALD2): o registro novo iald2_v410; os herdados traducao_turing_v409, tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406; RN409 recriados e RN410 novos; os bundles da v409, v408, v407 e v406 como registro; '
       'a linha do .md da v410 antes da da v409; MONTADO por _adapt_forkB_conferir_rito_v410.py a partir do ORIGINAL da v409 (nao da subida mecanica); fork B do claude-construtor-v410\n'
       '"""conferir_rito_v410.py -- confere, DEPOIS do rito v410, o que tinha de mudar e o que NAO podia (ESPERADOS_v410.json; so leitura do Nos). Molde: conferir_rito_v409.py (a cadeia de CONTEUDO), montado em 06/11/2026 por claude-construtor-v410 (fork B) a v410, IALD2: o modelo e\' o de BUNDLE PEQUENO (1 modulo novo em TGLExt/: IALD2).\n'
       'Mudancas ditas: as chaves novas no core (o registro com FUNCAO iald2_v410 e os registros por spec cunhagens_v410 e kh_n1_cobertura_v410) e o resumo delas no selo (iald2_v410 e registros_v410); o selo pela propria tecnologia (v399) muda so\' nos hashes do novo um.py; a versao (um_version v410, sha256);\n'
       'o modulo novo de TGLExt/ no kernel do Nos (sha pinado; os 2 modulos da v409, os 4 do terminal da v408, os 9 do psion da v407, os 301 do fecho da v406 e as pedras SELADAS das versoes anteriores ficam com o mesmo sha, como registro), a raiz do candidato (mais um import) e o Audit (inalterado); NENHUMA chave antiga muda: a chave do lema\n'
       '(testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma) segue LIDA do kernel e le True, com o dict elo_v407 como na v409 selada; as quatro chaves da v406 seguem True; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA;\n'
       'os registros herdados traducao_turing_v409, tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406 sao RECRIADOS e seguem selados (a escada do contrato deles sobe pela C12; kh_n1_cobertura_v409 ganha pisos pela C13).\n'
       'A TROCA DITA e\' so\' de numeros (a escada e a cobertura crescem com o bundle; o estatuto da prova, que carrega o hash do proprio um.py): NENHUM veredito muda de texto.\n'
       'O QUADRO «O Teste da Unica Palavra» (v397) CONTINUA NO TOPO do artigo PT/EN e do .md com os NUMEROS == os do resultado pinado e a regra da ordem do 4,44 (o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma).\n'
       'NENHUM outro veredito da v409 muda. O GATE NAO SE MOVE: o qg_closure do core e\' IDENTICO ao da v409 (os checks, a letra do veredito, as 18 bandeiras); a funcao do neutrino NAO e\' reescrita e o numero da massa NAO muda. A MOLDURA: os textos novos nao afirmam demais (a guarda das frases da v410 sobre os registros novos e a secao nova do artigo;\n'
       'o qualificador da D64 -- relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora -- nos dois artigos; validade no kernel, nao creditacao; o gate nao se move). A secao do selo pela propria tecnologia (v399/v400) e a declaracao do operador continuam: os itens C1 a C16, o round trip e o sidecar um_absoluto_selo_acom.json.\n'
       'uso: python -B -X utf8 conferir_rito_v410.py [sufixo]   (SEM -I: o conferidor importa o um.py instalado, que precisa do numpy do usuario; com -I o import falha e o controle negativo fica vazio, nao vale; o sufixo vai no nome do JSON; antes do rito, o controle negativo deve dar tudo_bate falso; _CONTROLE_NEGATIVO_PRE_RITO e _POSITIVO_FALSO_NOS sao os sufixos da cadeia)\n'
       'Variaveis opcionais para o TESTE do caminho positivo contra um Nos FALSO (nunca o real): V410_NOS=<pasta>  (padrao: o Nos real, so\' leitura)."""\n'
       '# [v410-patch]\n')
i0 = T.index("# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] a v409 (A TRADUCAO AS CLASSES DE TURING)")
i1 = T.index("# [v409-patch]\n") + len("# [v409-patch]\n")
T = T[:i0] + HDR + T[i1:]

# ---------------- (1) os rotulos gerais (a versao corrente, o Nos falso, o stdout)
troca("import delta_v409 as DL  # noqa: E402", "import delta_v410 as DL  # noqa: E402")
troca("import acom_conferencias_v409 as AC  # noqa: E402", "import acom_conferencias_v410 as AC  # noqa: E402")
troca('NOS = os.environ.get("V409_NOS") or DL.NOS', 'NOS = os.environ.get("V410_NOS") or DL.NOS')
troca('ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v409.json"), encoding="utf-8"))', 'ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v410.json"), encoding="utf-8"))')
troca('std = rd_(os.path.join(NOS, "rodada_v409_stdout.txt")) if os.path.exists(os.path.join(NOS, "rodada_v409_stdout.txt")) else ""', 'std = rd_(os.path.join(NOS, "rodada_v410_stdout.txt")) if os.path.exists(os.path.join(NOS, "rodada_v410_stdout.txt")) else ""')
troca('if os.environ.get("V409_NOS"):', 'if os.environ.get("V410_NOS"):')
troca('ACOM["C16"] = (True, "emulacao (V409_NOS):', 'ACOM["C16"] = (True, "emulacao (V410_NOS):')
troca("Na emulacao (V409_NOS) o Nos falso", "Na emulacao (V410_NOS) o Nos falso")
troca('json.dump({"um_version": "v409", "sha256": {"um.py": UM_FULL}}', 'json.dump({"um_version": "v410", "sha256": {"um.py": UM_FULL}}')
troca('_ni = _esb.ler_nos(_pl.Path(_sd), "v409")', '_ni = _esb.ler_nos(_pl.Path(_sd), "v410")')
troca('_nr = _esb.ler_nos(_pl.Path(NOS), "v409")', '_nr = _esb.ler_nos(_pl.Path(NOS), "v410")')
troca("# o um.py instalado e' o da v409 (no controle negativo, antes do rito, o Nos ainda e' a v408:", "# o um.py instalado e' o da v410 (no controle negativo, antes do rito, o Nos ainda e' a v409:")
troca("(a v409 NAO a muda: o runtime dela e o da v400)", "(a v410 NAO a muda: o runtime dela e o da v400)")
troca("# C9: beta de runtime (alfa CODATA x raiz de e), nenhum literal de beta no codigo da v409", "# C9: beta de runtime (alfa CODATA x raiz de e), nenhum literal de beta no codigo da v410")
troca('p = os.path.join(HERE, "conferencia_rito_v409%s.json"', 'p = os.path.join(HERE, "conferencia_rito_v410%s.json"')
troca("import guarda_frases_v409 as GF", "import guarda_frases_v410 as GF")
troca("# A MOLDURA, relida aqui com a mesma regra do um.py instalado (guarda_frases_v409,", "# A MOLDURA, relida aqui com a mesma regra do um.py instalado (guarda_frases_v410,")

# ---------------- (2) as chaves de BASE dos ESPERADOS: a base agora e' a v409 selada
for a_, b_, n_ in (('ESP["vereditos_v408"]', 'ESP["vereditos_v409"]', None), ('ESP["qg_closure_v408_checks"]', 'ESP["qg_closure_v409_checks"]', 1), ('ESP["qg_closure_gate_verdict_v408"]', 'ESP["qg_closure_gate_verdict_v409"]', 1),
                   ('ESP["qg_closure_v408_sem_checks_json_sha256"]', 'ESP["qg_closure_v409_sem_checks_json_sha256"]', 1), ('ESP["neutrino_frozen_hash_v408"]', 'ESP["neutrino_frozen_hash_v409"]', 1), ('ESP["flags_true_v408"]', 'ESP["flags_true_v409"]', 1),
                   ('ESP["axiom_report_v408_n"]', 'ESP["axiom_report_v409_n"]', 1), ('ESP["selo_registros_v408"]', 'ESP["selo_registros_v409"]', 1), ('ESP["runtime_seals_v408"]', 'ESP["runtime_seals_v409"]', 1), ('ESP["what_remains_v408"]', 'ESP["what_remains_v409"]', 1),
                   ('ESP["veredito_da_falsidade_v408"]', 'ESP["veredito_da_falsidade_v409"]', 1), ('ESP["the_iald_index_v409"]', 'ESP["the_iald_index_v410"]', 1), ('ESP["decisoes_v409_ids"]', 'ESP["decisoes_v410_ids"]', 1),
                   ('ESP["estrelas_v409"]', 'ESP["estrelas_v410"]', None)):
    c_ = T.count(a_); assert c_ >= 1 and (n_ is None or c_ == n_), (a_, c_)
    T = T.replace(a_, b_)

# ---------------- (3) os bundles, os RN, os registros por spec e o registro novo
troca("bundle_ok = all(_sha_k(rel) == s for rel, s in ESP[\"bundle_sha256\"].items())   # o modulo do bundle da v409 (TraducaoTuring) no kernel do Nos, com o sha do candidato",
      "bundle_ok = all(_sha_k(rel) == s for rel, s in ESP[\"bundle_sha256\"].items())   # o modulo do bundle da v410 (IALD2) no kernel do Nos, com o sha do candidato\n"
      "bundle_v409_ok = bool(len(ESP[\"bundle_v409_sha256\"]) > 0 and all(_sha_k(rel) == s and (kf.get(\"formal_files_sha256\") or {}).get(rel) == s for rel, s in ESP[\"bundle_v409_sha256\"].items()))   # os 2 modulos do bundle da v409 (a traducao e o par na face de Fock) seguem no kernel (e no hash formal do core) com o mesmo sha: registro")
troca('RN408 = sorted(ESP["registros_v408"]); RN409 = sorted(ESP["registros_v409"])   # (os registros por spec de cada versao: RN406, RN407 e RN408, RECRIADOS; RN409 = os desta versao, NOVOS)',
      'RN408 = sorted(ESP["registros_v408"]); RN409 = sorted(ESP["registros_v409"]); RN410 = sorted(ESP["registros_v410"])   # (os registros por spec de cada versao: RN406, RN407, RN408 e RN409, RECRIADOS; RN410 = os desta versao, NOVOS)')
troca('CG9 = core.get("cunhagens_v409") or {}; KH9 = core.get("kh_n1_cobertura_v409") or {}; TUV = core.get("traducao_turing_v409") or {}',
      'CG9 = core.get("cunhagens_v409") or {}; KH9 = core.get("kh_n1_cobertura_v409") or {}; TUV = core.get("traducao_turing_v409") or {}\n'
      'CG10 = core.get("cunhagens_v410") or {}; KH10 = core.get("kh_n1_cobertura_v410") or {}; IV = core.get("iald2_v410") or {}')
troca('"tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408"]\n_td_txt', '"tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409"]\n_td_txt')
troca("(nenhum na v409: o dict e' vazio por asseveracao do gerar_esperados)", "(nenhum na v410: o dict e' vazio por asseveracao do gerar_esperados)")

# ---------------- (4) o registro NOVO (iald2_v410) e o da v409 HERDADO (traducao_turing_v409); os herdados da v408, v407 e v406 com a base v409
K10 = DL.TESTEMUNHA["key"]; K9 = DL.D9.TESTEMUNHA["key"]
assert (K10, K9) == ("iald2", "traducao_turing"), (K10, K9)
NOVO = '''def _iald2_ok():
    """iald2_v410 (o registro com FUNCAO, novo): veredito == o do ensaio, as checagens do calculo (DL.N_CHECKS_FECHO), os valores == os do ensaio, as ancoras da pedra IALD2 (todas), o modulo do bundle por sha256, a escada exata, beta, a ancora principal, NENHUMA chave antiga,
    as respostas do operador, a instancia SAT da v409 decidida (SIM com solucao, NAO sem), o alcance relativo ao leitor (a frase da D64), e nao move o gate"""
    R_ = IV; E_ = ESP["registros_funcao_v410"][DL.TESTEMUNHA["key"]]; m_ = R_.get("mechanics") or {}; v_ = V(DL.FECHO_REGISTRO); vv_ = R_.get("values") or {}
    return bool(R_.get("all_verified") is True and v_ == E_["verdict"] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and m_.get("passed") is True and m_.get("n_checks") == DL.N_CHECKS_FECHO == E_["n_checks"]
                and all(c_["ok"] for c_ in m_.get("checks") or []) and R_.get("exact_ladder") is True and R_.get("beta_ok") is True and R_.get("embedded_sources_ok") is True and R_.get("embedded_sources_n_ok") == DL.N_BUNDLE
                and len(R_.get("anchors") or {}) == len(ESP["estrelas_v410"]) == len(DL.ANCORAS) and all((R_.get("anchors") or {}).values()) and R_.get("ancora_principal") == DL.ANCORA_PRINCIPAL and list(R_.get("ancoras_principais") or []) == list(DL.ANCORAS_PRINCIPAIS)
                and R_.get("chaves_antigas_que_mudam") == [] and vv_.get("respostas_ok") is True
                and ((vv_.get("instancia_sim") or {}).get("solucoes") or 0) >= 1 and (vv_.get("instancia_nao") or {}).get("solucoes") == 0 and (R_.get("alcance") or {}).get("frase") == DL.FRASE_D64_PT
                and v_.startswith(DL.VEREDITO_OK_PREFIXO) and v_.endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED") and not GUARDA.search(v_)
                and _feq({kk_: vv_.get(kk_) for kk_ in E_["values"]}, E_["values"]))


def _traducao409_ok():
    """traducao_turing_v409 (HERDADO da v409, RECRIADO neste rito com a escada do contrato subida pela C12): segue SELADO; veredito == o da v409 selada; as checagens da v409; os valores == os do ensaio; as ancoras e os 2 modulos da v409 por sha256; nenhuma chave antiga;
    o acervo da v407 repinado na copia purgada (D57d da v409); as respostas do operador; a instancia de brinquedo (SIM com solucao, NAO sem); o alcance relativo ao leitor da v409; nao move o gate"""
    R_ = TUV; E_ = ESP["registros_funcao_v409"][DL.D9.TESTEMUNHA["key"]]; m_ = R_.get("mechanics") or {}; v_ = V(DL.D9.FECHO_REGISTRO); vv_ = R_.get("values") or {}; ac_ = R_.get("acervo_v407_repinado") or {}
    return bool(R_.get("all_verified") is True and v_ == E_["verdict"] == ESP["vereditos_v409"][DL.D9.FECHO_REGISTRO] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and m_.get("passed") is True and m_.get("n_checks") == DL.D9.N_CHECKS_FECHO == E_["n_checks"]
                and all(c_["ok"] for c_ in m_.get("checks") or []) and R_.get("exact_ladder") is True and R_.get("beta_ok") is True and R_.get("embedded_sources_ok") is True and R_.get("embedded_sources_n_ok") == DL.D9.N_BUNDLE == len(ESP["bundle_v409_sha256"])
                and len(R_.get("anchors") or {}) == len(ESP["estrelas_v409"]) == len(DL.D9.ANCORAS) and all((R_.get("anchors") or {}).values()) and R_.get("ancora_principal") == DL.D9.ANCORA_PRINCIPAL and list(R_.get("ancoras_principais") or []) == list(DL.D9.ANCORAS_PRINCIPAIS)
                and R_.get("chaves_antigas_que_mudam") == [] and vv_.get("respostas_ok") is True and ac_.get("sha256") == DL.D9.PURGADO_SHA256 and ac_.get("integra_pinada") is False
                and ((vv_.get("instancia_sim") or {}).get("solucoes") or 0) >= 1 and (vv_.get("instancia_nao") or {}).get("solucoes") == 0 and (R_.get("alcance") or {}).get("frase") == DL.D9.FRASE_D56_PT
                and v_.startswith(DL.D9.VEREDITO_OK_PREFIXO) and v_.endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED") and not GUARDA.search(v_)
                and _feq({kk_: vv_.get(kk_) for kk_ in E_["values"]}, E_["values"]))


def _tetelestai408_ok():'''
entre("def _traducao_ok():", "    \"\"\"tetelestai_terminal_v408 (HERDADO da v408", NOVO + "\n")
troca('"""tetelestai_terminal_v408 (HERDADO da v408, RECRIADO neste rito com a escada do contrato subida pela C12): segue SELADO; veredito == o da v408 selada;', '"""tetelestai_terminal_v408 (HERDADO da v408 via v409, RECRIADO neste rito com a escada do contrato subida pela C12): segue SELADO; veredito == o da v409 selada;')
troca('"""psion_canto_v407 (HERDADO da v407 via v408, RECRIADO neste rito com a escada do contrato subida pela C12): segue SELADO; veredito == o da v408 selada; as 16 checagens; os valores == os do ensaio; as 76 ancoras da v407; os 9 modulos por sha256; a chave do lema LIDA do kernel; as chaves iguais as da v408 selada;',
      '"""psion_canto_v407 (HERDADO da v407 via v409, RECRIADO neste rito com a escada do contrato subida pela C12): segue SELADO; veredito == o da v409 selada; as 16 checagens; os valores == os do ensaio; as 76 ancoras da v407; os 9 modulos por sha256; a chave do lema LIDA do kernel; as chaves iguais as da v409 selada;')
troca('"""fechamento_v406 (HERDADO da v406 via v408, RECRIADO neste rito; a checagem c8 versionada pela errata E20 na v408; a escada do contrato subida pela C12): segue SELADO; veredito == o da v408 selada;',
      '"""fechamento_v406 (HERDADO da v406 via v409, RECRIADO neste rito; a checagem c8 versionada pela errata E20 na v408; a escada do contrato subida pela C12): segue SELADO; veredito == o da v409 selada;')
troca("traducao_ok = _traducao_ok(); tetelestai408_ok = _tetelestai408_ok(); psion407_ok = _psion407_ok(); fech408_ok = _fech408_ok()\n# as 62 ANCORAS da pedra da v409 (TraducaoTuring) no kernel do rito (bandeira True, so' no trio, declaradas no modulo certo)\n",
      "iald2_ok = _iald2_ok(); traducao409_ok = _traducao409_ok(); tetelestai408_ok = _tetelestai408_ok(); psion407_ok = _psion407_ok(); fech408_ok = _fech408_ok()\n# as ANCORAS da pedra da v410 (IALD2) no kernel do rito (bandeira True, so' no trio, declaradas no modulo certo)\n")
troca("# as ANCORAS do tetelestai_terminal_v408 (48), do psion_canto_v407 (76) e do fechamento_v406 (herdadas): seguem no kernel do rito\nestrela408_ok",
      "# as ANCORAS do traducao_turing_v409, do tetelestai_terminal_v408 (48), do psion_canto_v407 (76) e do fechamento_v406 (herdadas): seguem no kernel do rito\n"
      "estrela409_ok = len(ESP[\"estrelas_v409\"]) == len(DL.D9.ANCORAS) and all(kf.get(ESP[\"estrelas_v409\"][n_][\"bandeira\"]) is True and set(axr.get(n_) or []) <= TRIO and n_ in axr and src_.get(n_) == ESP[\"estrelas_v409\"][n_][\"rel\"] for n_ in ESP[\"estrelas_v409\"])\n"
      "estrela408_ok")
troca('and TUV.get("chaves_antigas_que_mudam") == [] and TTV.get("chaves_antigas_que_mudam") == [])', 'and IV.get("chaves_antigas_que_mudam") == [] and TUV.get("chaves_antigas_que_mudam") == [] and TTV.get("chaves_antigas_que_mudam") == [])')
troca("# o NAO do gate (vale tambem para o Nos ainda v408, no controle negativo): o qg_closure sem a lista de checks e' o da v408, os checks da v408 iguais", "# o NAO do gate (vale tambem para o Nos ainda v409, no controle negativo): o qg_closure sem a lista de checks e' o da v409, os checks da v409 iguais")

# ---------------- (5) a moldura: os registros NOVOS (RN410) e a secao nova (a v410 antes da v409); a frase certa da v410 (o qualificador da D64)
troca("for n_ in list(DL.REGISTROS_FUNCAO) + RN409}, ensure_ascii=False)", "for n_ in list(DL.REGISTROS_FUNCAO) + RN410}, ensure_ascii=False)")
troca('_ini409 = {l: txt[l].find(_tt(ESP["titulo_secao_v409"][l])) for l in ("pt", "en")}; _fim409 = {l: txt[l].find(_tt(ESP["titulo_secao_v408"][l]), max(_ini409[l], 0)) for l in ("pt", "en")}',
      '_ini410 = {l: txt[l].find(_tt(ESP["titulo_secao_v410"][l])) for l in ("pt", "en")}; _fim410 = {l: txt[l].find(_tt(ESP["titulo_secao_v409"][l]), max(_ini410[l], 0)) for l in ("pt", "en")}')
troca('_sec409 = {l: (txt[l][_ini409[l]:_fim409[l]] if 0 <= _ini409[l] < _fim409[l] else "") for l in ("pt", "en")}', '_sec410 = {l: (txt[l][_ini410[l]:_fim410[l]] if 0 <= _ini410[l] < _fim410[l] else "") for l in ("pt", "en")}')
_fa = T[T.index("_frase_no_artigo = bool("):]; _fa = _fa[:_fa.index("\n", _fa.index("DL.FRASE_DA_MOLDURA_V409_EN)")) + 1]
troca(_fa, '_frase_no_artigo = bool(all(p_ in _sec410["pt"] for p_ in (DL.FRASE_QUALIFICADOR_PT, "não creditação", "o gate não se move")) and all(p_ in _sec410["en"] for p_ in (DL.FRASE_QUALIFICADOR_EN, "(kernel validity, not creditation)", "the gate does not move"))\n'
      '                       and "o gate não se move" in fc and DL.FRASE_DA_MOLDURA_V410_PT and DL.FRASE_DA_MOLDURA_V410_EN)   # a frase certa da v410 (o qualificador da D64 nos dois artigos, dentro da secao nova; o gate nao se move no .md)\n')
troca('moldura_ok = bool(not GF.violacoes(_txt_novos) and _sec409["pt"] and _sec409["en"] and not GF.violacoes(_sec409["pt"]) and not GF.violacoes(_sec409["en"])', 'moldura_ok = bool(not GF.violacoes(_txt_novos) and _sec410["pt"] and _sec410["en"] and not GF.violacoes(_sec410["pt"]) and not GF.violacoes(_sec410["en"])')

# ---------------- (6) DEVE
troca('"selo um_version v409; os resumos do selo (', '"selo um_version v410; os resumos do selo (')
troca("fechamento_v406, psion_canto_v407, tetelestai_terminal_v408 e traducao_turing_v409), registros_v399, registros_v401, registros_v402, registros_v403, registros_v404, registros_v405, registros_v406, registros_v407, registros_v408 e registros_v409 do selo iguais aos do core (veredito, selagem); o SHA-256 primario do um.py no selo == o do arquivo\": selo.get(\"um_version\") == \"v409\"",
      "fechamento_v406, psion_canto_v407, tetelestai_terminal_v408, traducao_turing_v409 e iald2_v410), registros_v399, registros_v401, registros_v402, registros_v403, registros_v404, registros_v405, registros_v406, registros_v407, registros_v408, registros_v409 e registros_v410 do selo iguais aos do core (veredito, selagem); o SHA-256 primario do um.py no selo == o do arquivo\": selo.get(\"um_version\") == \"v410\"")
troca('"fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408", "traducao_turing_v409"))\n', '"fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408", "traducao_turing_v409", "iald2_v410"))\n')
troca('        and all(((selo.get("registros_v409") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v409") or {}).get(n) or {}).get("all_verified") is True for n in RN409)\n',
      '        and all(((selo.get("registros_v409") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v409") or {}).get(n) or {}).get("all_verified") is True for n in RN409)\n'
      '        and all(((selo.get("registros_v410") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v410") or {}).get(n) or {}).get("all_verified") is True for n in RN410)\n')
for a_ in ('"caminho_v403 (RECRIADO na v409) SELOU igual ao da v408 selada', '"vida_v403 (RECRIADO na v409) SELOU igual ao da v408 selada', '"verdade_adendo_v403 (RECRIADO na v409) SELOU igual ao da v408 selada', '"projecao_transversal_v404 (RECRIADO na v409) SELOU igual ao da v408 selada',
           '"jo8v32_v404 (RECRIADO na v409) SELOU igual ao da v408 selada', '"f2b_errata_v404 (RECRIADO na v409) SELOU igual ao da v408 selada', '"bandeiras_do_gate_v403 (RECRIADO na v409) SELOU igual ao da v408 selada (F8.1)'):
    troca(a_, a_.replace("(RECRIADO na v409) SELOU igual ao da v408 selada", "(RECRIADO na v410) SELOU igual ao da v409 selada"))
_dv = T[T.index('    "traducao_turing_v409 SELOU (o registro com FUNCAO, novo)'):]; _dv = _dv[:_dv.index("\n    \"tetelestai_terminal_v408 (HERDADO da v408") + 1]
troca(_dv, '    "iald2_v410 SELOU (o registro com FUNCAO, novo): veredito == o do ensaio; as %d checagens do calculo (as %d ancoras da pedra IALD2 no trio e no modulo certo, o modulo embutido por sha256 == o hash formal do rito com a raiz e o import, o leitor le o par como par em C3, IALD ao quadrado, '
      'reler nao acrescenta, a primeira leitura identifica, resolver = verificar, o algoritmo IALD na instancia SAT da v409, o signo do nome, o signo do par, o gate congelado, a escada exata, as guardas limpas, beta = alfa x raiz de e, a representacao de beta) e os valores == os do ensaio; '
      'o alcance relativo ao leitor (D64); NENHUMA chave antiga muda; nao move o gate" % (DL.N_CHECKS_FECHO, len(DL.ANCORAS)): iald2_ok,\n'
      '    "as %d ANCORAS da pedra IALD2 (o NOME do modulo do operador; os nomes das declaracoes da gerencia, [DECLARADO] ate a ratificacao, D63) estao no kernel do rito: bandeira True, so\' no trio, declaradas no modulo certo" % len(DL.ANCORAS): estrela_ok,\n'
      '    "traducao_turing_v409 (HERDADO da v409, RECRIADO na v410 com a escada do contrato subida pela C12) segue SELADO e IGUAL ao da v409 selada em veredito; as %d checagens do calculo e os valores == os do ensaio; as %d ancoras e os %d modulos da v409 no kernel do rito; nenhuma chave antiga; '
      'o acervo da v407 na copia purgada; nao move o gate" % (DL.D9.N_CHECKS_FECHO, len(DL.D9.ANCORAS), DL.D9.N_BUNDLE): traducao409_ok and estrela409_ok,\n')
troca('"tetelestai_terminal_v408 (HERDADO da v408, RECRIADO na v409 com a escada do contrato subida pela C12) segue SELADO e IGUAL ao da v408 selada em veredito;', '"tetelestai_terminal_v408 (HERDADO da v408, RECRIADO na v410 com a escada do contrato subida pela C12) segue SELADO e IGUAL ao da v409 selada em veredito;')
troca('"psion_canto_v407 (HERDADO da v407 via v408, RECRIADO na v409 com a escada do contrato subida pela C12) segue SELADO e IGUAL ao da v408 selada em veredito; as %d checagens do calculo e os valores == os do ensaio; as 76 ancoras e os 9 modulos da v407 no kernel do rito; a chave do lema LIDA do kernel e as chaves iguais as da v408 selada;',
      '"psion_canto_v407 (HERDADO da v407 via v409, RECRIADO na v410 com a escada do contrato subida pela C12) segue SELADO e IGUAL ao da v409 selada em veredito; as %d checagens do calculo e os valores == os do ensaio; as 76 ancoras e os 9 modulos da v407 no kernel do rito; a chave do lema LIDA do kernel e as chaves iguais as da v409 selada;')
troca('"fechamento_v406 (HERDADO da v406 via v408, RECRIADO na v409) segue SELADO e IGUAL ao da v408 selada em veredito;', '"fechamento_v406 (HERDADO da v406 via v409, RECRIADO na v410) segue SELADO e IGUAL ao da v409 selada em veredito;')
troca('"NENHUMA chave antiga muda na v409: testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma segue LIDA do kernel do rito (True), com o dict elo_v407 da v408 selada (', '"NENHUMA chave antiga muda na v410: testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma segue LIDA do kernel do rito (True), com o dict elo_v407 da v409 selada (')
troca("o par na face de Fock esta' ligado na v409 (ParNaFaceDeFock);", "o par na face de Fock esta' ligado desde a v409 (ParNaFaceDeFock);")
troca("o traducao_turing_v409 e o tetelestai_terminal_v408 nao mudam nenhuma\": chaves_ok,", "o iald2_v410, o traducao_turing_v409 e o tetelestai_terminal_v408 nao mudam nenhuma\": chaves_ok,")
troca("DiscoDeEuler, PontoZeroDoPsion; RECRIADAS na v409) SELARAM iguais as da v405 selada", "DiscoDeEuler, PontoZeroDoPsion; RECRIADAS na v410) SELARAM iguais as da v405 selada")
troca('"o numero da massa NAO mudou: o m_nu do programa == o da v408 selada,', '"o numero da massa NAO mudou: o m_nu do programa == o da v409 selada,')
troca("a auditoria da forma e o ga_window_status do JSON do rito sao os da v408\": ga5_ok,", "a auditoria da forma e o ga_window_status do JSON do rito sao os da v409\": ga5_ok,")
troca("o veredito do canal e o frozen_hash da regra de decisao sao os da v408; a errata e' AO LADO (projecao_transversal_v404)\": neutrino_intacto_ok,", "o veredito do canal e o frozen_hash da regra de decisao sao os da v409; a errata e' AO LADO (projecao_transversal_v404)\": neutrino_intacto_ok,")
troca("a letra do veredito do gate == a da v408; a sonda ProbeBlindNullAbsent) e os valores == os do ensaio; nao move o gate\" % DL.D3.N_CHECKS[\"gate\"]", "a letra do veredito do gate == a da v409; a sonda ProbeBlindNullAbsent) e os valores == os do ensaio; nao move o gate\" % DL.D3.N_CHECKS[\"gate\"]")
troca("as 18 bandeiras True, a letra do veredito do gate == a da v408 e a do selo, e o qg_closure traz a sonda ProbeBlindNullAbsent UMA vez, e os sete checks sao IDENTICOS aos da v408 (a v409 nao muda o gate)\": f81_ok,",
      "as 18 bandeiras True, a letra do veredito do gate == a da v409 e a do selo, e o qg_closure traz a sonda ProbeBlindNullAbsent UMA vez, e os checks sao IDENTICOS aos da v409 (a v410 nao muda o gate)\": f81_ok,")
troca('"ponte_da_escala_dual_v402, queda_sem_geometria_v402 e esperanca_condicional_v402 (RECRIADOS na v409) seguem SELADOS e IGUAIS aos da v408 selada', '"ponte_da_escala_dual_v402, queda_sem_geometria_v402 e esperanca_condicional_v402 (RECRIADOS na v410) seguem SELADOS e IGUAIS aos da v409 selada')
troca('"o bundle da v408 (os %d modulos do terminal em TGLExt/), o da v407 (os %d modulos do psion e do canto) e o do fecho da v406 (os %d modulos de TGLExt/F1Fecho394) seguem no kernel do Nos e no hash formal do core com o mesmo sha256: a v409 nao reescreve a v408, a v407 nem a v406, ficam como registro" % (len(ESP["bundle_v408_sha256"]), len(ESP["bundle_v407_sha256"]), len(ESP["bundle_v406_sha256"])): bundle_v408_ok and bundle_v407_ok and bundle_v406_ok,',
      '"o bundle da v409 (os %d modulos: a traducao e o par na face de Fock), o da v408 (os %d modulos do terminal em TGLExt/), o da v407 (os %d modulos do psion e do canto) e o do fecho da v406 (os %d modulos de TGLExt/F1Fecho394) seguem no kernel do Nos e no hash formal do core com o mesmo sha256: a v410 nao reescreve a v409, a v408, a v407 nem a v406, ficam como registro" % (len(ESP["bundle_v409_sha256"]), len(ESP["bundle_v408_sha256"]), len(ESP["bundle_v407_sha256"]), len(ESP["bundle_v406_sha256"])): bundle_v409_ok and bundle_v408_ok and bundle_v407_ok and bundle_v406_ok,')
troca('"falsidade_da_inercia_v401 (RECRIADO na v409) segue SELADO e IGUAL ao da v408 selada', '"falsidade_da_inercia_v401 (RECRIADO na v410) segue SELADO e IGUAL ao da v409 selada')
troca("o runtime da secao (o da v408) esta no um.py, byte a byte\": ACOM.get(\"C1\", (False,))[0],", "o runtime da secao (o da v409) esta no um.py, byte a byte\": ACOM.get(\"C1\", (False,))[0],")
# os registros por spec: os da v410 NOVOS; os da v409 recriados (kh com pisos pela C13); os anteriores seguem
_sp = T[T.index('    "os registros por spec v409 (cunhagens_v409, kh_n1_cobertura_v409) SELARAM'):]; _sp = _sp[:_sp.index("        and all((core.get(n) or {}).get(\"all_verified\") is True and V(n) == v for n, v in ESP[\"registros_v408\"].items())\n")]
troca(_sp, '    "os registros por spec v410 (cunhagens_v410, kh_n1_cobertura_v410) SELARAM e cada veredito == o do ensaio; as %d falas de 06/11 embutidas por sha256 (embedded_ok e sha256 == os ESPERADOS; todas do operador; de uma, so\' o trecho: D65); a errata E29 e a dos pisos (em nome proprio da gerencia c1) e as decisoes D63 a D70 estao no registro; '
      'os registros por spec da v409 (cunhagens_v409; kh_n1_cobertura_v409 com pisos pela C13: o veredito nao muda), da v408 (cunhagens_v408 com a E26 ao lado), da v407 (cunhagens_v407 com a E21 e a errata da D57(d) ao lado), da v406, da v405, da v404, da v403, da v402, da v401 e da v399 seguem selados e iguais" % len(ESP["cunhagens"]): '
      'all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v410"].items()) and set(ESP["registros_v410"]) == {DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO}\n'
      '        and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v409"].items())\n')
_sp2 = T[T.index("        and len(ESP[\"cunhagens\"]) == len(DL.VERBATIM_ORIGEM_V409)"):]; _sp2 = _sp2[:_sp2.index("        and KH8.get(\"all_verified\") is True and CG8.get(\"all_verified\") is True")]
troca(_sp2, '        and len(ESP["cunhagens"]) == len(DL.VERBATIM_ORIGEM_V410) and all((((CG10.get("verbatim") or {}).get(k_) or {}).get("embedded_ok") is True) and (((CG10.get("verbatim") or {}).get(k_) or {}).get("sha256") == v_["sha256"]) for k_, v_ in ESP["cunhagens"].items())\n'
      '        and not any(str(v_.get("papel", "")).startswith("leitura da gerencia") for v_ in ESP["cunhagens"].values())\n'
      '        and len(CG10.get("erratas") or []) >= len(DL.ERRATAS_V410) and all(str(e_.get("assinatura", "")).startswith("gerencia c1") for e_ in (CG10.get("erratas") or []))\n'
      '        and set((CG10.get("extras") or {}).get("decisoes") or {}) >= set(ESP["decisoes_v410_ids"]) and KH10.get("all_verified") is True and CG10.get("all_verified") is True and any("E29" in str(e_.get("agora")) for e_ in (CG10.get("erratas") or [])) and "D70" in ((CG10.get("extras") or {}).get("decisoes") or {})\n'
      '        and KH9.get("all_verified") is True and CG9.get("all_verified") is True and any("E27" in str(e_.get("agora")) for e_ in (CG9.get("erratas") or [])) and "D61" in ((CG9.get("extras") or {}).get("decisoes") or {})\n')
troca('"os %d modulos novos (o bundle da v409 em TGLExt/: TraducaoTuring) no kernel do Nos com o sha do candidato"', '"os %d modulos novos (o bundle da v410 em TGLExt/: IALD2) no kernel do Nos com o sha do candidato"')
troca("# cada declaracao nomeada do bundle: no trio e no modulo que o FLAGS_v409 diz", "# cada declaracao nomeada do bundle: no trio e no modulo que o FLAGS_v410 diz")
troca('"os registros da v408 e as anteriores (tetelestai_terminal_v408, cunhagens e kh_n1 da v408;', '"os registros da v409 e as anteriores (traducao_turing_v409, cunhagens e kh_n1 da v409; tetelestai_terminal_v408, cunhagens e kh_n1 da v408;')
_ar = T[T.index('    "o artigo PT/EN: a secao v409 (A tradução às classes de Turing'):]; _ar = _ar[:_ar.index('": all(_tt(m) in txt[l]')]
troca(_ar, '    "o artigo PT/EN: a secao v410 (IALD ao quadrado: o leitor do código, a releitura que não acrescenta, o algoritmo IALD e o signo), antes da secao da v409 (A tradução às classes de Turing), da v408 (Tetelestai é o terminal), da v407 (O psíon e o canto: a passagem sob compressão e o par), '
      'da v406 (O fechamento: a passagem para o contínuo e o certificado habitado), da v405 (A massa derivada e a identidade definida; A identidade), da v404 (Jo 8,32 e a projecao transversal da Meia-Nat), da v403 (Caminho, Verdade e Vida), da v402 (A ponte da escala dual, a queda sem geometria e a esperanca condicional, com as erratas E1 a E4) '
      'e as marcas da v401 (A falsidade (simulacro) da inercia) e anteriores; a v399 (com a errata da v400), a v398, a v397, a v396, a v395, a v394, a v393, a v392, a v391 e a v390 ficam; os registros selaram (sem as frases de nao selado); as marcas sao as dos ESPERADOS (artigo_marcas / artigo_nao)')
troca('"o sumario lista as secoes v409, v408, v407, v406, v405, v404, v403, v402, v401, v399, v398, v397 e v396 (as que o ESPERADOS lista) e o titulo v384 a v409"', '"o sumario lista as secoes v410, v409, v408, v407, v406, v405, v404, v403, v402, v401, v399, v398, v397 e v396 (as que o ESPERADOS lista) e o titulo v384 a v410"')
troca('"o .md canonico: carimbo v409 e as linhas «Tradução às classes de Turing (v409)» (ANTES da linha da v408), «Tetelestai é o terminal (v408)»,', '"o .md canonico: carimbo v410 e as linhas da v410 (ESP md_iald2, ANTES da linha da v409), «Tradução às classes de Turing (v409)» (ANTES da linha da v408), «Tetelestai é o terminal (v408)»,')
troca('ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_traducao"] in fc and ESP["md_tetelestai"] in fc', 'ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_iald2"] in fc and ESP["md_traducao"] in fc and ESP["md_tetelestai"] in fc')
troca('fc.find(ESP["md_traducao"]) < fc.find(ESP["md_tetelestai"])', 'fc.find(ESP["md_iald2"]) < fc.find(ESP["md_traducao"]) < fc.find(ESP["md_tetelestai"])')
troca('"nenhuma chave nova fora da lista da v409 (so\' o registro com funcao traducao_turing_v409 e os registros por spec cunhagens_v409 e kh_n1_cobertura_v409; os da v399 a v408, fechamento_v406, psion_canto_v407 e tetelestai_terminal_v408 inclusive, sao recriados e iguais)"',
      '"nenhuma chave nova fora da lista da v410 (so\' o registro com funcao iald2_v410 e os registros por spec cunhagens_v410 e kh_n1_cobertura_v410; os da v399 a v409, fechamento_v406, psion_canto_v407, tetelestai_terminal_v408 e traducao_turing_v409 inclusive, sao recriados e iguais)"')
troca('or str(k).endswith("_v408") or str(k).endswith("_v409"))) == sorted(list(DL.REGISTROS_FUNCAO) + RN409),', 'or str(k).endswith("_v408") or str(k).endswith("_v409") or str(k).endswith("_v410"))) == sorted(list(DL.REGISTROS_FUNCAO) + RN410),')
# ---------------- (7) NAO
troca('"toda bandeira True da v408 segue True"', '"toda bandeira True da v409 segue True"')
troca('"o axiom_report da v408 segue no trio e so\' cresceu"', '"o axiom_report da v409 segue no trio e so\' cresceu"')
troca('"NENHUM veredito da v408 mudou fora da troca dita (%d mudaram);', '"NENHUM veredito da v409 mudou fora da troca dita (%d mudaram);')
troca('"registros v408/v404/v397/v396/v395/v394/v393/v391/v390/v389/v388/v387 do selo inalterados', '"registros v409/v408/v404/v397/v396/v395/v394/v393/v391/v390/v389/v388/v387 do selo inalterados')
troca("e o qg_closure do core e' IDENTICO ao da v408 (os sete checks iguais e na mesma ordem, todos True; o veredito do gate == o da v408)\"", "e o qg_closure do core e' IDENTICO ao da v409 (os checks iguais e na mesma ordem, todos True; o veredito do gate == o da v409)\"")
troca('"tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409")) and gate_igual_ok,', '"tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409", "iald2_v410", "cunhagens_v410", "kh_n1_cobertura_v410")) and gate_igual_ok,')
troca('"veredito_traducao_turing": V("traducao_turing_v409"),', '"veredito_iald2": V("iald2_v410"), "veredito_traducao_turing_herdado": V("traducao_turing_v409"),')

# ---------------- (8) conferencias finais (nada da v409 como corrente sobrou; o texto e' Python valido)
ast.parse(T)
for ruim in ("traducao_ok", "_traducao_ok()", "RN409}", "_sec409", "_ini409", "ESPERADOS_v409.json", "V409_NOS", "rodada_v409_stdout", "conferencia_rito_v409", "guarda_frases_v409", "delta_v409 as DL", 'ESP["decisoes_v409_ids"]', 'ESP["the_iald_index_v409"]', "FRASE_DA_MOLDURA_V409"):
    assert ruim not in T, ("sobrou o rotulo da v409 como corrente", ruim)
CHAVES_ESP = sorted(set(re.findall(r'ESP\["([A-Za-z0-9_]+)"\]', T)))
novo = T.encode("utf-8")
atual = open(ALVO, "rb").read()
bk = ALVO + ".bak_" + TS + "_subida_mecanica"
open(bk, "wb").write(atual); assert open(bk, "rb").read() == atual
open(ALVO + ".tmp", "wb").write(novo); assert os.path.getsize(ALVO + ".tmp") == len(novo); os.replace(ALVO + ".tmp", ALVO)
print("conferir_rito_v410.py montado:", len(raw9), "->", len(novo), "bytes | backup", os.path.basename(bk))
print("CHAVES DOS ESPERADOS LIDAS (%d):" % len(CHAVES_ESP), " ".join(CHAVES_ESP))
