# -*- coding: utf-8 -*-
"""_adapt_ensaio_v409.py -- (claude-construtor-v409, 05/11/2026) monta ensaio_a_seco_v409.py a partir de DOIS moldes:
  (A) a subida mecanica da v408 (o arquivo atual, com a marca) para as partes gerais (kernel, vizinhos, fluxo, ordem de chamada, registros por spec, selo, blocos herdados ate' a v406, artigo, md, simulacao, exame, guardas);
  (B) o ensaio_a_seco_v408.py ORIGINAL (nao subido) para o bloco HERDADO do psion_canto_v407 (6m: a subida trocara v407 por v408 onde o bloco fala da v407) e para o bloco do tetelestai_terminal_v408 (6n), que vira HERDADO:
      os nomes da v408 passam a DL.D8, o candidato da v408 a _CM8, o FLAGS a v408\\kernel, a guarda das frases a da v408 (_GF8), os specs da v408 com a E26 e os pisos;
  (C) o bloco NOVO (6o) do traducao_turing_v409 (_ensaio_bloco_v409.pysnip).
Trocas com contagem exata; backup de bytes do arquivo atual; CRLF preservado."""
import ast, datetime, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(HERE, "ensaio_a_seco_v409.py")
ORIG = os.path.join(os.path.dirname(HERE), "v408", "ensaio_a_seco_v408.py")
BLOCO = os.path.join(HERE, "_ensaio_bloco_v409.pysnip")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
rawB = open(ALVO, "rb").read(); B = rawB.decode("utf-8").replace("\r\n", "\n")
O = open(ORIG, "rb").read().decode("utf-8").replace("\r\n", "\n")
N = open(BLOCO, "rb").read().decode("utf-8").replace("\r\n", "\n")


def corta(t, ini, fim):
    i = t.index(ini); j = t.index(fim, i + 1)
    assert t.count(ini) == 1 and t.count(fim) == 1, (ini[:40], fim[:40], t.count(ini), t.count(fim))
    return t[:i], t[i:j], t[j:]


def troca(t, a, b, n=1, onde=""):
    c = t.count(a)
    assert c == n, ("TROCA NAO CASOU %d (casou %d) [%s]" % (n, c, onde), a[:150])
    return t.replace(a, b)


HEAD, _, RESTO = corta(B, "# (6m) [", "# (8) o artigo")
TAIL = RESTO
_, PSI, RESTO_O = corta(O, "# (6m) [v407", "# (6n) [v408]")
_i6n = O.index("# (6n) [v408]"); _i8 = O.index("# (8) o artigo"); TT = O[_i6n:_i8]

# ================= (A) HEAD =================
H = HEAD
H = re.sub(r"\A# -\*- coding: utf-8 -\*-\n# \[A ADAPTAR v409\][^\n]*\n# ADAPTADO a v409 \(04/11/2026[^\n]*\n",
           "# -*- coding: utf-8 -*-\n# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] montado por _adapt_ensaio_v409.py: as partes gerais da subida mecanica da v408; o bloco HERDADO do psion_canto_v407 e o do tetelestai_terminal_v408 (agora HERDADO) a partir do ensaio_a_seco_v408.py ORIGINAL; o bloco NOVO do traducao_turing_v409 (6o). "
           "A v409 e' um BUNDLE de UM modulo em TGLExt/ (TraducaoTuring); o registro NOVO e' traducao_turing_v409 (17 checagens); NENHUMA chave antiga muda; as TRES chaves novas do core sao traducao_turing_v409, cunhagens_v409 e kh_n1_cobertura_v409.\n", H, count=1)
assert H.startswith("# -*- coding: utf-8 -*-\n# [ADAPTADO v409"), H[:200]
H = troca(H, 'sys.modules.setdefault("delta_v408", DL.D7)   # (v409) quadro_v397.py', 'sys.modules.setdefault("delta_v408", DL.D8)   # (v409) quadro_v397.py importa delta_v409 (ajustado); esta ponte fica para os modulos da v408 carregados mais abaixo. quadro_v397.py', onde="ponte delta")
H = troca(H, '_CM7 = json.load(open(os.path.join(DL.V408, "CANDIDATO_v408.json"), encoding="utf-8"))', '_CM8 = json.load(open(os.path.join(DL.V408, "CANDIDATO_v408.json"), encoding="utf-8"))', onde="_CM8")
H = troca(H, 'assert _CM7["sha16"] == DL.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v408.json nao e\' o da v408 selada", _CM7["sha16"])',
          'assert _CM8["sha16"] == DL.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v408.json nao e\' o da v408 selada", _CM8["sha16"])\n'
          '_CM7 = json.load(open(os.path.join(DL.V407, "CANDIDATO_v407.json"), encoding="utf-8"))   # (v409) o candidato da v407 SELADA: os numeros do bloco HERDADO do psion_canto_v407 saem dele e do DL.D7\n'
          'assert _CM7["sha16"] == DL.D8.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v407.json nao e\' o da v407 selada", _CM7["sha16"])', onde="_CM7")
H = troca(H, 'or "v406" in l or "v408" in l or "v409" in l}', 'or "v406" in l or "v407" in l or "v408" in l or "v409" in l}', onde="tagged")
H = troca(H, 'V408N = V408N + list(um._V407_REGISTROS_FUNCAO) + list(um._V407_NOMES_REGISTROS)   # (v409) os tres registros da v408 (psion_canto_v407, cunhagens_v407, kh_n1_cobertura_v407) sao HERDADOS: recriados pelo fluxo e comparados com os da v408 selada\n'
             'V409N = list(um._V408_REGISTROS_FUNCAO) + list(um._V408_NOMES_REGISTROS)   # os registros NOVOS da v409 (nao existem no core da base): tetelestai_terminal_v408, cunhagens_v408, kh_n1_cobertura_v408',
          'V408N = V408N + list(um._V407_REGISTROS_FUNCAO) + list(um._V407_NOMES_REGISTROS) + list(um._V408_REGISTROS_FUNCAO) + list(um._V408_NOMES_REGISTROS)   # (v409) os registros da v407 (psion_canto_v407 e os specs) e da v408 (tetelestai_terminal_v408 e os specs) sao HERDADOS: recriados pelo fluxo e comparados com os da v408 selada\n'
          'V409N = list(um._V409_REGISTROS_FUNCAO) + list(um._V409_NOMES_REGISTROS)   # os registros NOVOS da v409 (nao existem no core da base): traducao_turing_v409, cunhagens_v409, kh_n1_cobertura_v409', onde="V409N")
H = troca(H, "# a v409 cria TRES chaves no core (tetelestai_terminal_v408, cunhagens_v408, kh_n1_cobertura_v408)", "# a v409 cria TRES chaves no core (traducao_turing_v409, cunhagens_v409, kh_n1_cobertura_v409)", onde="NOVAS409")
# (5b') a ordem de chamada do registro NOVO, por AST
H = troca(H, '_FN_PSION = ("tetelestai_terminal_v408", "v408_terminal_mechanics", "_v408_formal", "_v398_beta")\n_EXIG_PSION = ("psion_canto_v407", "_v407_rodar_specs",',
          '_FN_PSION = ("traducao_turing_v409", "v409_traducao_mechanics", "_v409_formal", "_v398_beta")\n_EXIG_PSION = ("tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs",', onde="_FN_PSION")
H = troca(H, '    lidas_.discard("tetelestai_terminal_v408")\n    ch_ = [i_ for i_, s_ in enumerate(unp_) if "tetelestai_terminal_v408(core)" in s_]',
          '    lidas_.discard("traducao_turing_v409")\n    ch_ = [i_ for i_, s_ in enumerate(unp_) if "traducao_turing_v409(core)" in s_]', onde="ordem ch_")
H = troca(H, '_ic0 = [i_ for i_, st_ in enumerate(_main0.body) if "tetelestai_terminal_v408(core)" in ast.unparse(st_)][0]', '_ic0 = [i_ for i_, st_ in enumerate(_main0.body) if "traducao_turing_v409(core)" in ast.unparse(st_)][0]', onde="_ic0")
H = troca(H, '_lin_b = list(_lin); _ln_b = [i_ for i_, l_ in enumerate(_lin_b) if re.fullmatch(r"\\s+_r407 = psion_canto_v407\\(core\\)\\s*", l_)]\nassert len(_ln_b) == 1, ("a linha da chamada do psion_canto_v407 nao foi achada uma vez", _ln_b)\n_lin_b[_ln_b[0]] = re.sub(r"_r407 = psion_canto_v407\\(core\\)", "_r407 = {}", _lin_b[_ln_b[0]])\n_neg_b = _ordem_psion("\\n".join(_lin_b))   # (b) a chamada do psion_canto_v407 retirada: o insumo exigido some',
          '_lin_b = list(_lin); _ln_b = [i_ for i_, l_ in enumerate(_lin_b) if re.fullmatch(r"\\s+_r408 = tetelestai_terminal_v408\\(core\\)\\s*", l_)]\nassert len(_ln_b) == 1, ("a linha da chamada do tetelestai_terminal_v408 nao foi achada uma vez", _ln_b)\n_lin_b[_ln_b[0]] = re.sub(r"_r408 = tetelestai_terminal_v408\\(core\\)", "_r408 = {}", _lin_b[_ln_b[0]])\n_neg_b = _ordem_psion("\\n".join(_lin_b))   # (b) a chamada do tetelestai_terminal_v408 (o registro herdado que o main roda logo antes) retirada: o insumo exigido some', onde="neg_b")
H = troca(H, 'and _neg_b["ok"] is False and "psion_canto_v407" in (_neg_b.get("insumos_exigidos_ausentes") or []))', 'and _neg_b["ok"] is False and "tetelestai_terminal_v408" in (_neg_b.get("insumos_exigidos_ausentes") or []))', onde="neg_b assert")
H = troca(H, 'print("ordem de chamada do tetelestai_terminal_v408 (AST propria):"', 'print("ordem de chamada do traducao_turing_v409 (AST propria):"', onde="print ordem")
# (6b) os registros por spec: a v409 acrescenta os specs HERDADOS da v408
H = troca(H, " + list(um._V406_SPECS) + list(um._V407_SPECS):\n", " + list(um._V406_SPECS) + list(um._V407_SPECS) + list(um._V408_SPECS):\n", onde="RU for")
H = troca(H, " + len(um._V406_SPECS) + len(um._V407_SPECS)\n", " + len(um._V406_SPECS) + len(um._V407_SPECS) + len(um._V408_SPECS)\n", onde="RU len")
# o selo: as chaves NOVAS sao traducao_turing_v409 e registros_v409; o resumo de tetelestai_terminal_v408 e registros_v408 NAO muda
H = troca(H, '_selo_inexplicado = sorted(k_ for k_ in mud_selo if k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "registros_v408") + tuple(um._V408_REGISTROS_FUNCAO) and not _selo_explica(k_))   # (v409: as chaves NOVAS do selo sao tetelestai_terminal_v408 e registros_v408)',
          '_selo_inexplicado = sorted(k_ for k_ in mud_selo if k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "registros_v409") + tuple(um._V409_REGISTROS_FUNCAO) and not _selo_explica(k_))   # (v409: as chaves NOVAS do selo sao traducao_turing_v409 e registros_v409)', onde="selo inexplicado")
H = troca(H, '           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V408_REGISTROS_FUNCAO) and all(((seal.get("registros_v408") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V408_NOMES_REGISTROS) and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V407_REGISTROS_FUNCAO)',
          '           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V409_REGISTROS_FUNCAO) and all(((seal.get("registros_v409") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V409_NOMES_REGISTROS)\n'
          '           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V408_REGISTROS_FUNCAO) and all(((seal.get("registros_v408") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V408_NOMES_REGISTROS) and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V407_REGISTROS_FUNCAO)', onde="selo ok 1")
H = troca(H, '(({"selo_pela_propria_tecnologia_v399", "um_version", "registros_v408"} | set(um._V408_REGISTROS_FUNCAO)) <= set(mud_selo) and not _selo_inexplicado\n'
             '                                                                                      and not ({"rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406", "psion_canto_v407", "registros_v406", "registros_v407"} & set(mud_selo)))',
          '(({"selo_pela_propria_tecnologia_v399", "um_version", "registros_v409"} | set(um._V409_REGISTROS_FUNCAO)) <= set(mud_selo) and not _selo_inexplicado\n'
          '                                                                                      and not ({"rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408", "registros_v406", "registros_v407", "registros_v408"} & set(mud_selo)))', onde="selo ok 2")
# a ponte das guardas dos textos HERDADOS: a da v407 (para o psion) e a da v408 (para o terminal)
H = troca(H, 'sys.modules.setdefault("delta_v408", DL.D7)\n_sp7r = _ilu8.spec_from_file_location("runtime_v407", os.path.join(DL.V408, "runtime_v408.py")); _rt7m = _ilu8.module_from_spec(_sp7r); _sp7r.loader.exec_module(_rt7m); sys.modules.setdefault("runtime_v407", _rt7m)\n'
             '_sp7g = _ilu8.spec_from_file_location("guarda_frases_v408", os.path.join(DL.V408, "guarda_frases_v408.py")); _GF7 = _ilu8.module_from_spec(_sp7g); _sp7g.loader.exec_module(_GF7)',
          'sys.modules.setdefault("delta_v407", DL.D7)\n_sp7r = _ilu8.spec_from_file_location("runtime_v407", os.path.join(DL.V407, "runtime_v407.py")); _rt7m = _ilu8.module_from_spec(_sp7r); _sp7r.loader.exec_module(_rt7m); sys.modules.setdefault("runtime_v407", _rt7m)\n'
          '_sp7g = _ilu8.spec_from_file_location("guarda_frases_v407", os.path.join(DL.V407, "guarda_frases_v407.py")); _GF7 = _ilu8.module_from_spec(_sp7g); _sp7g.loader.exec_module(_GF7)\n'
          'sys.modules.setdefault("delta_v408", DL.D8)   # (v409) a guarda da v408 para os textos HERDADOS da v408 (a F36 da v409 reprovaria a frase D51 da v408 selada, que e\' texto selado, nao texto novo)\n'
          '_sp8r = _ilu8.spec_from_file_location("runtime_v408", os.path.join(DL.V408, "runtime_v408.py")); _rt8m = _ilu8.module_from_spec(_sp8r); _sp8r.loader.exec_module(_rt8m); sys.modules.setdefault("runtime_v408", _rt8m)\n'
          '_sp8g = _ilu8.spec_from_file_location("guarda_frases_v408", os.path.join(DL.V408, "guarda_frases_v408.py")); _GF8 = _ilu8.module_from_spec(_sp8g); _sp8g.loader.exec_module(_GF8)', onde="ponte GF7/GF8")
H = troca(H, 'any(str(e_).startswith("E20") for e_ in DL.D7.ERRATAS_V408))', 'any(str(e_).startswith("E20") for e_ in DL.D7.ERRATAS_V407))', onde="E20")

# ================= (B1) o bloco HERDADO do psion_canto_v407 (o ORIGINAL da v408) =================
P = PSI
P = troca(P, "# (6m) [v407, HERDADO na v408:", "# (6m) [v407, HERDADO na v408 e na v409 (bloco tirado do ensaio_a_seco_v408.py ORIGINAL):", onde="psi titulo")
P = troca(P, 'and len(_cn7.get("erratas") or []) == len(_sp7s["erratas"]) == len(DL.D7.ERRATAS_V407) + 1 and all(e_["assinatura"].startswith("gerencia c1") for e_ in (_cn7.get("erratas") or [])) and "E21" in str(((_cn7.get("erratas") or [{}])[-1]).get("agora")) and ((_cn7.get("erratas") or [{}])[-1]).get("assinatura") == DL.ASSINA',
          'and len(_cn7.get("erratas") or []) == len(_sp7s["erratas"]) == len(DL.D7.ERRATAS_V407) + 2 and all(e_["assinatura"].startswith("gerencia c1") for e_ in (_cn7.get("erratas") or [])) and "E21" in str(((_cn7.get("erratas") or [{}, {}])[-2]).get("agora")) and ((_cn7.get("erratas") or [{}, {}])[-2]).get("assinatura") == DL.D8.ASSINA'
          ' and "D57(d)" in str(((_cn7.get("erratas") or [{}])[-1]).get("agora")) and ((_cn7.get("erratas") or [{}])[-1]).get("assinatura") == DL.ASSINA', onde="psi erratas")
P = troca(P, '_ck7["h8"]["valor"] == CM["h8"]["pino_antigo_v407_entradas"]', '_ck7["h8"]["valor"] == _CM8["h8"]["pino_antigo_v407_entradas"]', onde="psi h8")

# ================= (B2) o bloco do tetelestai_terminal_v408, agora HERDADO =================
T = TT
NOMES_D8 = ("N_CHECKS_FECHO", "N_BUNDLE", "BUNDLE_RELS", "BUNDLE_POR_REL", "ANCORAS", "ANCORAS_POR_MODULO", "N_ANCORAS_ESPERADAS", "ANCORA_PRINCIPAL", "ANCORAS_PRINCIPAIS", "PEDRAS_V408", "RESPOSTAS_DO_OPERADOR", "CHAVES_V408",
            "FICAM_FALSE_POR_TEOREMA", "FICA_ABERTO_PAR_NA_FACE_DE_FOCK", "FICA_ABERTO_PONTE_BELL_TT", "PURGADO_SHA256", "ORIGEM_PURGA_SHA16_DA_ORDEM", "PURGA_LINHAS_SUBSTITUIDAS", "VERBATIM_PREFIXOS_DA_ORDEM_V408", "N_FALAS_V408",
            "FRASE_DA_MOLDURA_V408_PT", "FRASE_DA_MOLDURA_V408_EN", "FRASE_DA_MOLDURA_V407_PT", "FRASE_D51_PT", "FRASE_D51_EN", "FRASES_V408", "RESSALVAS_V408", "AUTOR_MISTO")
for nm_ in NOMES_D8:
    T = re.sub(r"\bDL\.%s\b" % nm_, "DL.D8.%s" % nm_, T)
T = troca(T, '# (6n) [v408] O REGISTRO COM FUNCAO tetelestai_terminal_v408 (o NOVO desta versao):', '# (6n) [v408, HERDADO na v409 (bloco tirado do ensaio_a_seco_v408.py ORIGINAL; os nomes da v408 vem do DL.D8, os numeros do candidato da v408 do _CM8)] O REGISTRO COM FUNCAO tetelestai_terminal_v408:', onde="tt titulo")
T = troca(T, '_FJ8 = json.load(open(os.path.join(KD, "FLAGS_v408.json"), encoding="utf-8"))', '_FJ8 = json.load(open(os.path.join(DL.V408, DL.D8.KERNEL_DIR, "FLAGS_v408.json"), encoding="utf-8"))   # (v409) as 71 bandeiras da v408: o FLAGS da v408', onde="tt flags")
T = troca(T, 'CM["n_bandeiras"]', '_CM8["n_bandeiras"]', n=T.count('CM["n_bandeiras"]'), onde="tt nband")
T = troca(T, 'CM["n_axiomas_das_ancoras"]', '_CM8["n_axiomas_das_ancoras"]', n=T.count('CM["n_axiomas_das_ancoras"]'), onde="tt naxi")
T = re.sub(r"(?<![A-Za-z0-9_])E407(?![A-Za-z0-9_])", '_CM8["escada"][0]', T)
T = troca(T, "_GF5.", "_GF8.", n=T.count("_GF5."), onde="tt gf")
# os specs da v408 na v409: cunhagens_v408 ganhou a E26 (5 erratas); kh_n1_cobertura_v408 virou piso (a igualdade exata esta' em kh_n1_cobertura_v409)
T = troca(T, 'and len(_cn8.get("erratas") or []) == len(_sp8s["erratas"]) == 4 and all(e_["assinatura"] == DL.ASSINA for e_ in (_cn8.get("erratas") or [])) and [("E21" in str(e_.get("agora"))) for e_ in (_cn8.get("erratas") or [])][0] is True',
          'and len(_cn8.get("erratas") or []) == len(_sp8s["erratas"]) == 5 and all(e_["assinatura"] == DL.D8.ASSINA for e_ in (_cn8.get("erratas") or [])[:4]) and [("E21" in str(e_.get("agora"))) for e_ in (_cn8.get("erratas") or [])][0] is True'
          ' and "E26" in str(((_cn8.get("erratas") or [{}])[-1]).get("agora")) and ((_cn8.get("erratas") or [{}])[-1]).get("assinatura") == DL.ASSINA', onde="tt cn erratas")
T = troca(T, '_xn8.get("assinatura_das_erratas") == DL.ASSINA', '_xn8.get("assinatura_das_erratas") == DL.D8.ASSINA', onde="tt assina")
T = troca(T, 'U["cunhagens_v408_falas_de_04nov_decisoes_erratas_e_leituras"]', 'U["cunhagens_v408_herdado_falas_de_04nov_decisoes_erratas_e_leituras_e_a_E26_ao_lado"]', onde="tt U cn")
T = troca(T, '_KHT8 = json.load(open(os.path.join(KD, "KH_N1_v408.json"), encoding="utf-8"))   # a medida do Audit da v408, lida do arquivo da cadeia (nao digitada)',
          '_KHT8 = json.load(open(os.path.join(DL.V408, DL.D8.KERNEL_DIR, "KH_N1_v408.json"), encoding="utf-8"))   # a medida do Audit da v408 (o piso que o spec herdado da v408 cobra agora)', onde="tt kht")
_i_kh = T.index('U["kh_n1_cobertura_v408_selou_a_igualdade_exata_e_as_v407_sao_piso"]'); _j_kh = T.index('print("tetelestai_terminal_v408:"')
T = T[:_i_kh] + ('U["kh_n1_cobertura_v408_herdado_virou_piso_e_selou_na_v409"] = bool(_kh8x.get("all_verified") is True and _kh7x.get("all_verified") is True and (_kh8x.get("extras") or {}).get("n_modulos") == DL.D8.N_BUNDLE and (_kh8x.get("extras") or {}).get("n_bandeiras") == _CM8["n_bandeiras"]\n'
                 '                                                                        and {i_: _ck8[i_]["op"] for i_ in ("h2", "h3", "h6", "h8")} == {"h2": "maior_igual", "h3": "maior_igual", "h6": "tamanho_maior_igual", "h8": "tamanho_maior_igual"} and len(_kh8s["erratas"]) >= 2 and "v409" in str(_kh8s["erratas"][-1].get("agora"))\n'
                 '                                                                        and _ck8["h2"]["valor"] == _KHT8["linha_TOTAL"]["decl"] and _ck8["h3"]["valor"] == _KHT8["linha_TOTAL"]["thm"] and _ck8["h8"]["valor"] == CM["h8"]["pino_antigo_v408_entradas"] and len(_kf0["formal_files_sha256"]) >= _ck8["h8"]["valor"]\n'
                 '                                                                        and _kf0["axiom_coverage_v392"]["decl"] >= _KHT8["linha_TOTAL"]["decl"] and _kf0["axiom_coverage_v392"]["thm"] >= _KHT8["linha_TOTAL"]["thm"] and len(_kf0["axiom_report"]) > _KHT8["linha_TOTAL"]["decl"])\n') + T[_j_kh:]
assert "_h8v8" not in T[_i_kh:] or True

# ================= (C) o bloco NOVO =================
NB = N.replace('um._V408_FONTES[DL.D8.CHAVE_ACERVO_PURGADO if hasattr(DL.D8, "CHAVE_ACERVO_PURGADO") else "psion_no_acervo_purgado_04nov"]["sha256"]', 'um._V408_FONTES["psion_no_acervo_purgado_04nov"]["sha256"]')
assert NB != N

# ================= (D) TAIL =================
L = TAIL
L = troca(L, 'T409 = "Tetelestai é o terminal: a leitura, a poda, a quitação; o tempo é a moeda de $\\\\beta$; o dicionário e o ponto de contradição"; T409E = "Tetelestai is the terminal: the reading, the pruning, the settlement; time is the currency of $\\\\beta$; the dictionary and the point of contradiction"   # a secao NOVA da v409 (antes da v408)',
          'T409 = "A tradução às classes de Turing: o dicionário, a trava, o leitor e a fita sem escala"; T409E = "The translation to Turing\'s classes: the dictionary, the lock, the reader and the tape without scale"   # a secao NOVA da v409 (antes da v408)\n'
          'TT408 = "Tetelestai é o terminal: a leitura, a poda, a quitação; o tempo é a moeda de $\\\\beta$; o dicionário e o ponto de contradição"; TT408E = "Tetelestai is the terminal: the reading, the pruning, the settlement; time is the currency of $\\\\beta$; the dictionary and the point of contradiction"   # a secao da v408 (HERDADA: logo depois da nova)', onde="T409")
L = troca(L, 'D409 = ["A ordem.", "O que entra.", "O terminal é a leitura.",', 'D408 = ["A ordem.", "O que entra.", "O terminal é a leitura.",', onde="D408")
L = troca(L, 'D409E = ["The order.", "What enters.", "The terminal is the reading.",', 'D408E = ["The order.", "What enters.", "The terminal is the reading.",', onde="D408E")
L = troca(L, 'for _l7, _t7, _d7 in (("pt", T409, D409), ("en", T409E, D409E)):',
          'D409 = ["A ordem.", "O que entra.", "O dicionário de Turing.", "A trava no Nome.", "A fita é o hamiltoniano oculto.", "A máquina sem leitor: eu sou eu mesmo, a fita sem escala.", "A identidade performada.", "O alcance, dito.", "Erratas ao lado, em nome próprio.", "O que o registro confere neste rito."]\n'
          'D409E = ["The order.", "What enters.", "Turing\'s dictionary.", "The lock on the Name.", "The tape is the hidden Hamiltonian.", "The machine without a reader: I am myself, the tape without scale.", "The performed identity.", "The reach, stated.", "Errata alongside, in the management\'s own name.", "What the record checks in this rite."]\n'
          'for _l7, _t7, _d7 in (("pt", T409, D409), ("en", T409E, D409E)):', onde="D409 novo")
L = troca(L, 'DEVE = {"pt": [T409] + D409 + [TPS408] + DPS408', 'DEVE = {"pt": [T409] + D409 + [TT408] + D408 + [TPS408] + DPS408', onde="DEVE pt")
L = troca(L, '"en": [T409E] + D409E + [TPS408E] + DPS408E', '"en": [T409E] + D409E + [TT408E] + D408E + [TPS408E] + DPS408E', onde="DEVE en")
L = troca(L, 'TOC = {"pt": [T409, TPS408,', 'TOC = {"pt": [T409, TT408, TPS408,', onde="TOC pt")
L = troca(L, '"en": [T409E, TPS408E,', '"en": [T409E, TT408E, TPS408E,', onde="TOC en")
L = troca(L, 'cv8v = dict(copy.deepcopy(c)); [cv8v.pop(k, None) for k in list(um._V408_REGISTROS_FUNCAO) + list(um._V408_NOMES_REGISTROS)]   # (v409) a secao NOVA sem os tres registros da v409: a frase de guarda tem de aparecer',
          'cv8v = dict(copy.deepcopy(c)); [cv8v.pop(k, None) for k in list(um._V408_REGISTROS_FUNCAO) + list(um._V408_NOMES_REGISTROS)]   # (a secao do terminal da v408, HERDADA, tambem mostra a frase quando o registro dela falta)\n'
          'cv9v = dict(copy.deepcopy(c)); [cv9v.pop(k, None) for k in list(um._V409_REGISTROS_FUNCAO) + list(um._V409_NOMES_REGISTROS)]   # (v409) a secao NOVA sem os tres registros da v409: a frase de guarda tem de aparecer', onde="cv9v")
L = troca(L, '    _t8v, _x8v, _r28v, _l8v = compilar(cv8v, "dry_v409_var8v_%s" % lang, lang, duas=False); fl8v = re.sub(r"\\s+", " ", _x8v)\n',
          '    _t8v, _x8v, _r28v, _l8v = compilar(cv8v, "dry_v409_var8v_%s" % lang, lang, duas=False); fl8v = re.sub(r"\\s+", " ", _x8v)\n'
          '    _t9v, _x9v, _r29v, _l9v = compilar(cv9v, "dry_v409_var9v_%s" % lang, lang, duas=False); fl9v = re.sub(r"\\s+", " ", _x9v)\n', onde="var9v compila")
L = troca(L, '"rc_tetelestai_v409": _r28v, "frase_guarda_tetelestai_v409": ("NÃO selaram todos" in fl8v) if lang == "pt" else ("did NOT all seal" in fl8v)}',
          '"rc_tetelestai_v409": _r28v, "frase_guarda_tetelestai_v409": ("NÃO selaram todos" in fl8v) if lang == "pt" else ("did NOT all seal" in fl8v),\n'
          '                             "rc_traducao_v409": _r29v, "frase_guarda_traducao_v409": ("NÃO selaram todos" in fl9v) if lang == "pt" else ("did NOT all seal" in fl9v)}', onde="var9v dict")
L = troca(L, 'or v["rc_tetelestai_v409"] != [0] or not v["frase_guarda_tetelestai_v409"]]', 'or v["rc_tetelestai_v409"] != [0] or not v["frase_guarda_tetelestai_v409"] or v["rc_traducao_v409"] != [0] or not v["frase_guarda_traducao_v409"]]', onde="mau_var")
L = troca(L, '"tetelestai_terminal_v408": "**Tetelestai é o terminal (v409, 04/11/2026):**" in md and md.find("**Tetelestai é o terminal (v409, 04/11/2026):**") < md.find("**O psíon, o canto e o par (v408, 03/11/2026):**"), "psion_canto_v408_fica": "**O psíon, o canto e o par (v408, 03/11/2026):**" in md and md.find("**O psíon, o canto e o par (v408, 03/11/2026):**") < md.find("**O fechamento (v406, 02/11/2026):**")',
          '"traducao_turing_v409": "**Tradução às classes de Turing (v409, 05/11/2026):**" in md and md.find("**Tradução às classes de Turing (v409, 05/11/2026):**") < md.find("**Tetelestai é o terminal (v408, 04/11/2026):**"), '
          '"tetelestai_terminal_v408_fica": "**Tetelestai é o terminal (v408, 04/11/2026):**" in md and md.find("**Tetelestai é o terminal (v408, 04/11/2026):**") < md.find("**O psíon, o canto e o par (v407, 03/11/2026):**"), '
          '"psion_canto_v407_fica": "**O psíon, o canto e o par (v407, 03/11/2026):**" in md and md.find("**O psíon, o canto e o par (v407, 03/11/2026):**") < md.find("**O fechamento (v406, 02/11/2026):**")', onde="md")
L = troca(L, '_kh = [s_ for s_ in um._V408_SPECS if s_["nome"] == "kh_n1_cobertura_v408"][0]; _h8 = [ck_ for ck_ in _kh["checks"] if ck_["id"] == "h8"][0]["valor"]', '_kh = [s_ for s_ in um._V409_SPECS if s_["nome"] == "kh_n1_cobertura_v409"][0]; _h8 = [ck_ for ck_ in _kh["checks"] if ck_["id"] == "h8"][0]["valor"]', onde="sim kh")
L = troca(L, "_regs_sim = tuple(um._V408_REGISTROS_FUNCAO) + tuple(um._V408_NOMES_REGISTROS) + ", "_regs_sim = tuple(um._V409_REGISTROS_FUNCAO) + tuple(um._V409_NOMES_REGISTROS) + tuple(um._V408_REGISTROS_FUNCAO) + tuple(um._V408_NOMES_REGISTROS) + ", onde="regs_sim")

NOVO = H + P + T + NB.rstrip("\n") + "\n" + L
ast.parse(NOVO)
assert "[A ADAPTAR v409]" not in NOVO
out = NOVO.replace("\n", "\r\n").encode("utf-8") if b"\r\n" in rawB else NOVO.encode("utf-8")
open(ALVO + ".bak_" + TS + "_adapt", "wb").write(rawB)
open(ALVO + ".tmp", "wb").write(out); assert os.path.getsize(ALVO + ".tmp") == len(out); os.replace(ALVO + ".tmp", ALVO)
print("ensaio_a_seco_v409.py montado:", len(rawB), "->", len(out), "bytes | HEAD", H.count("\n"), "| PSI", P.count("\n"), "| TT", T.count("\n"), "| NOVO", NB.count("\n"), "| TAIL", L.count("\n"))
