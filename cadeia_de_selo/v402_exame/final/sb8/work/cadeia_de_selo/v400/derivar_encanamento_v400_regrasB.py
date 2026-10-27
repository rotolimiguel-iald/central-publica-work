# -*- coding: utf-8 -*-
# regras (lote B) de derivar_encanamento_v400.py: o ENSAIO A SECO (autoral=True: a logica muda; editado a mao depois da subida mecanica). Escrito pela ferramenta Write.
# O mapa subiu 398 -> 399 e 399 -> 400 em tudo menos nos nomes nascidos no um.py. O que o mapa nao pode saber (a v400 NAO traz chave nova no core nem pedra: recria e compara os registros da v399 SELADA; a Bancada; o erratum) esta nas regras.
import re

_DOC = '''"""ensaio_a_seco_v400.py -- ENSAIO A SECO da v400 (molde: ensaio_a_seco_v399.py), SEM a GPU do rito e SEM rodar o rito. Chama NO PONTO DE CHAMADA REAL todo veredito novo ou alterado.
uso: python -B -X utf8 ensaio_a_seco_v400.py <candidato.py> <rotulo>
A v400 e' uma CORRECAO da v399 (nenhum modulo de kernel, nenhum registro novo): a base e' a v399 SELADA (core e selo em base_v399), o kernel e' o da v399 (sandbox C:/t/k400c, copia do k399c) e os registros de v393 a v399 sao RECRIADOS e comparados com os da v399 selada;
so' `selo_pela_propria_tecnologia_v399` muda de proposito (a checagem do beta confronta com o core; os hashes sao os do novo um.py). Etapas:
(1) copia o candidato; materializa o kernel embutido e confere BYTE A BYTE contra o sandbox; (2) importa (o rito NAO roda); UM_VERSION v400; (3) o core da v399 SELADA + o kernel REAL: verify_tgl_kernel_formalization() de ponta a ponta com o lake simulado devolvendo os logs CRUS do sandbox;
(4) os registros vizinhos RECOMPUTADOS: TODOS iguais (o kernel nao mudou); (5) o FLUXO PRINCIPAL v393 a v399 (as instrucoes etiquetadas do main, na ordem do arquivo), as chaves NOVAS no core: nenhuma;
(6) unidade: o Teste da Unica Palavra (v397), o sonico e a afinacao (v398), o selo pela propria tecnologia e a declaracao do operador (v399) -- agora com a checagem do beta contra o core e o alfa unico --, os registros por spec, a cobertura, o sidecar;
(7) o selo (a instrucao `seal = {...}` do main + o resumo) e o indice; (8) artigo PT/EN, pdflatex x2, a secao v399, a ERRATA ao lado e o QUADRO NO TOPO (v397, intocado); (9) .md e manifesto; (10) o conferidor de citacoes; (11) simular_arvore_do_nos; (12) exame_pontos;
(13) [v400, LICAO NOVA] as guardas ESTATICAS do esboco R3.5 da Bancada (ALPHA_LINHA_UNICA e as demais que nao dependem do selo) rodadas SOBRE O CANDIDATO, chamando a funcao do proprio esboco pinado, ANTES de instalar."""
'''

entrada("ensaio_a_seco_v399.py", prot_extra=("V398N",), autoral=True, regras=[
    # ---- docstring
    entre('"""ensaio_a_seco_v400.py -- ENSAIO A SECO da v400', "import hashlib, copy", _DOC, "docstring do ensaio v400"),
    # ---- a base e' a v399 selada: as chaves da v399 JA estao no core
    ('"selo_pela_propria_tecnologia_v399" not in core0 and "declaracao_do_operador_v399" not in core0 and "cunhagens_v399" not in core0 and selo0["um_version"] == "v399"',
     '"selo_pela_propria_tecnologia_v399" in core0 and "declaracao_do_operador_v399" in core0 and "cunhagens_v399" in core0 and "kh_n1_cobertura_v399" in core0 and selo0["um_version"] == "v399"', 1),
    # ---- a escada: a v400 nao acrescenta bandeira
    entre("# a escada: SEM as bandeiras novas", "_el = um.prove_external_ladder(1.0, kf); core_s",
          "# a escada: a v400 NAO acrescenta bandeira (o kernel e' o da v399): a escada do kf da v399 selada JA fecha e e' a do candidato\n"
          "_el0 = um.prove_external_ladder(1.0, core0[\"kernel_formalization\"])\n"
          "rep[\"escada_da_base_v399\"] = [_el0.get(\"n_theorems_clean\"), _el0.get(\"n_theorems_expected\"), _el0.get(\"all_verified\")]\n"
          "E399 = int(core0[\"external_ladder\"][\"n_theorems_expected\"])   # LIDO do core da v399 selada (nada digitado)\n"
          "assert rep[\"escada_da_base_v399\"][0] == E399 == rep[\"escada_da_base_v399\"][1] == ESP and _el0.get(\"all_verified\") is True, rep[\"escada_da_base_v399\"]\n", "escada da base"),
    # ---- o fluxo principal: v393 a v399 (a v398 volta a ser etiqueta; a v399 tambem) e os registros da v399 sao RECRIADOS
    ('or "v397" in l or "v399" in l or "v400" in l}', 'or "v397" in l or "v398" in l or "v399" in l}', 1),
    ('V398N = ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS)\n',
     'V398N = ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS)\nV399N = ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS)\n', 1),
    ("V393N + V394N + V395N + V396N + V397N + V398N", "V393N + V394N + V395N + V396N + V397N + V398N + V399N", 2),
    ('NOVAS400 = ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS)\n',
     'NOVAS400 = []   # a v400 NAO cria chave no core: os registros da v399 sao RECRIADOS e comparados com os da v399 selada\n', 1),
    # ---- o selo: o que muda em relacao ao selo da v399 e' so' o registro do selo ACOM (hashes do novo um.py), a versao e os pinos
    ('all(k in mud_selo for k in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "registros_v399", "um_version"))',
     '("selo_pela_propria_tecnologia_v399" in mud_selo and "um_version" in mud_selo and set(mud_selo) <= {"selo_pela_propria_tecnologia_v399", "um_version", "sha256"})', 1),
    # ---- o sidecar: o esquema nasceu na v399 e segue (v399)
    ('_sj9["esquema"] == "um_absoluto_selo_acom/v1 (v400)")', '_sj9["esquema"] == "um_absoluto_selo_acom/v1 (v399)")', 1),
    # ---- o artigo: a errata ao lado da secao v399
    ('DEVE = {"pt": [TN400, "A direção do testemunho."', 'DEVE = {"pt": [TN400, "Errata ao lado (v400).", "A direção do testemunho."', 1),
    ('"en": [TN400E, "The direction of the testimony."', '"en": [TN400E, "Erratum beside it (v400).", "The direction of the testimony."', 1),
    # ---- o md: os rotulos das secoes anteriores sao os que o um.py emite (v398, v399), nao os do mapa
    entre('rep["markdown"] = {"carimbo"', 'rep["quadro"]["md"] = QV.confere_md',
          'rep["markdown"] = {"carimbo": "**Versão v400**" in md, "errata_v400": "Errata ao lado (v400, 24/10/2026)" in md, "testemunho_v399_fica": "O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026)" in md, "sonico_v398_fica": "Sônico e a afinação das cordas (v398, 23/10/2026)" in md,\n'
          '                   "token_v397_fica": "O Teste da Única Palavra e a pedra Token (v397, 23/10/2026)" in md, "testemunha_v396_fica": "A testemunha estática (v396, 22/10/2026)" in md, "psibit_v395_fica": "O modo psiônico na fractalização do Um (v395, 21/10/2026)" in md,\n'
          '                   "v394_fica": "A integração do Codex e as cunhagens (v394, 19/10/2026)" in md, "v393_fica": "A regra e o coração (v393, 14/10/2026)" in md}\n', "markdown"),
    # ---- as fontes do operador (copias duraveis) moram na pasta da v399 (a v400 nao as copia de novo)
    ('_fo9 = os.path.join(HERE, "insumos", "acom", "fontes_operador")', '_fo9 = os.path.join(DL.V399, "insumos", "acom", "fontes_operador")', 1),
    # ---- (13) a LICAO NOVA: as guardas ESTATICAS do esboco R3.5 da Bancada sobre o CANDIDATO, antes de instalar (a v399 passou o ensaio e foi recusada pela Bancada: ALPHA_LINHA_NAO_UNICA)
    ('ok = (viz_ok and mf_ok and all(U.values()) and selo_ok',
     '# (13) [v400, LICAO NOVA] as guardas ESTATICAS do esboco R3.5 da Bancada (as que nao dependem do selo) rodadas SOBRE O CANDIDATO, com a FUNCAO ler_nos do proprio esboco pinado, ANTES de instalar; o defeito real da v399 tem de ser reproduzido (mensagem identica a do recibo da Bancada)\n'
     '_gb_p = os.path.join(HERE, "GUARDAS_ESTATICAS_BANCADA_v400.json")\n'
     '_gb = _pyr([os.path.join(HERE, "guardas_estaticas_bancada_v400.py"), _cand_p, _gb_p])\n'
     'try:\n'
     '    _gj = json.load(open(_gb_p, encoding="utf-8"))\n'
     'except (OSError, ValueError):\n'
     '    _gj = {}\n'
     'rep["guardas_estaticas_bancada"] = {"rc": _gb.returncode, "veredito": _gj.get("veredito"), "candidato_passa": (_gj.get("candidato_v400") or {}).get("passou"), "alfa": (_gj.get("candidato_v400") or {}).get("alpha"), "contagem_direta": _gj.get("contagem_direta"),\n'
     '                                    "v399_selada_recusada_com_a_mensagem_do_recibo_da_bancada": (_gj.get("v399_selada_o_defeito_real") or {}).get("mensagem_identica_a_do_recibo"), "recusa_da_v399": (_gj.get("v399_selada_o_defeito_real") or {}).get("recusa"),\n'
     '                                    "controles_negativos": {k_: v_.get("ok") for k_, v_ in (_gj.get("controles_negativos") or {}).items()}, "canonical_py_instalado": (_gj.get("canonical_py_instalado") or {}).get("ok"), "esboco_sha256": (_gj.get("esboco") or {}).get("sha256"), "sandbox_apagado": _gj.get("sandbox_apagado")}\n'
     'guardas_ok = bool(_gb.returncode == 0 and str(_gj.get("veredito")).startswith("GUARDAS_ESTATICAS_DA_BANCADA__CANDIDATO_PASSA") and rep["guardas_estaticas_bancada"]["controles_negativos"] and all(rep["guardas_estaticas_bancada"]["controles_negativos"].values()))\n'
     'print("guardas estaticas da Bancada (ler_nos do esboco R3.5) sobre o candidato:", guardas_ok, "|", rep["guardas_estaticas_bancada"]["veredito"])\n'
     'ok = (guardas_ok and viz_ok and mf_ok and all(U.values()) and selo_ok', 1),
    ('and sim_ok and exame_ok and rep["quadro"]["ok"])', 'and sim_ok and exame_ok and rep["quadro"]["ok"])\nrep["vizinhos_nenhum_mudou"] = (not rep["vizinhos"]["mudaram"])\nok = bool(ok and rep["vizinhos_nenhum_mudou"] and rep["mainflow"]["chaves_novas"] == [])', 1),
    ('json.dumps({"vizinhos": viz_ok,', 'json.dumps({"guardas_estaticas_bancada": guardas_ok, "vizinhos_nenhum_mudou": rep["vizinhos_nenhum_mudou"], "vizinhos": viz_ok,', 1),
    # ---- o exame dos pontos: as bandeiras sao as da v399 (a v400 nao tem bandeira nova)
    ('os.path.join(KD, "FLAGS_v400.json")', 'os.path.join(KD, "FLAGS_v399.json")', 1),
    # ---- o registro do selo ACOM no relatorio: o beta do core e a diferenca relativa
    ('"tempo_total_s": r9s["values"]["tempo_total_s"], "selagem_total_s": t_selo9',
     '"tempo_total_s": r9s["values"]["tempo_total_s"], "beta_core": r9s["values"]["beta_core"], "rel_beta_vs_core": r9s["values"]["rel_beta_vs_core"], "selagem_total_s": t_selo9', 1),
    # ---- (6d) os testes NOVOS da v400: a checagem do beta deixa de ser tautologica; alfa unico (depois do teste da direcao do testemunho)
    entre('U["selo_acom_direcao_do_testemunho_dita"]', "# controles negativos do registro do selo: SHA-256 do codigo diferente",
          'U["selo_acom_direcao_do_testemunho_dita"] = bool("o operador testifica DA IALD" in r9s["direcao_do_testemunho"] and "a IALD nao testifica do operador" in r9s["direcao_do_testemunho"] and "Jo 8,18" in r9s["direcao_do_testemunho"])\n'
          '# [v400, BAIXA B1 do exame da v399] a checagem «beta do runtime» NAO e\' mais tautologica: confronta com o beta do CORE do rito (que o main calcula por outro caminho) a 1e-9\n'
          '_vb = r9s["values"]; _b_core = cs()["beta"]\n'
          'U["selo_acom_beta_confronta_com_o_beta_do_core_a_1e_9"] = bool(_vb["beta_core"] == _b_core and _vb["rel_beta_vs_core"] is not None and _vb["rel_beta_vs_core"] < 1e-9 and r9s["checks"][5][0].startswith("beta do runtime (jamais literal) == o beta do core do rito") and r9s["checks"][5][1] is True)\n'
          '_c1 = cs(); _c1["beta"] = _c1["beta"] * (1 + 1e-6); _rbc = um.selo_acom_v399(_c1)\n'
          'U["selo_acom_beta_do_core_diferente_recusa"] = bool(_rbc["all_verified"] is False and _rbc["checks"][5][1] is False and _rbc["verdict"].endswith("_NOT_SEALED_THIS_RUN") and all(v_ for _, v_ in _rbc["checks"][:5]))\n'
          '_c2 = cs(); _c2.pop("beta"); _rbs = um.selo_acom_v399(_c2)\n'
          'U["selo_acom_sem_o_beta_do_core_recusa_fail_closed"] = bool(_rbs["all_verified"] is False and _rbs["checks"][5][1] is False)\n'
          '_a0 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a0 * 1.001\n'
          'try:\n'
          '    _rba = um.selo_acom_v399(cs())\n'
          'finally:\n'
          '    um.SEALED_CODATA_ALPHA = _a0\n'
          'U["selo_acom_alfa_do_programa_adulterado_agora_e_pego_pela_checagem_do_beta"] = bool(_rba["all_verified"] is False and _rba["checks"][5][1] is False)   # com a checagem tautologica da v399 isto NAO seria pego\n'
          '_RXB = AC.regexes_da_bancada(os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"), "02b22ba5c6d35c71922ae2f23939acc1c8f2283e8607bca31c4ff5b663fc36bf"); _txt_um = _UMB.decode("utf-8")\n'
          'U["alfa_unico_no_programa_a_secao_nao_redeclara_e_le_o_do_programa"] = bool("ALPHA_FINE_CODATA_2018" not in vars(um) and hasattr(um, "SEALED_CODATA_ALPHA") and len(_RXB["RE_ALPHA_LINHAS"].findall(_txt_um)) == 1 and not _RXB["RE_ALPHA_INDENTADA"].search(_txt_um)\n'
          '                                                                          and len(_RXB["RE_VERSAO_LINHAS"].findall(_txt_um)) == 1 and not _RXB["RE_VERSAO_INDENTADA"].search(_txt_um) and um._beta_runtime() == um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e))\n', "testes novos da v400 (6d)"),
    # ---- (licao da primeira corrida da v400) a comparacao dos vizinhos com a v399 SELADA: normalizar as CONTAGENS sobre a string INTEIRA e so' depois truncar para o relatorio
    #      (truncar a 300 ANTES de normalizar deixava "INCONCLUSIVE_9" -> "INCONCLUSIVE_10" (um digito a mais) virar mudanca: o instrumento errava, nao o candidato)
    ('        mud[nome] = {"antes": a[:300], "depois": b[:300], "so_numeros": _num(a) == _num(b), "all_verified": novo.get("all_verified")}',
     '        mud[nome] = {"antes": a, "depois": b, "so_numeros": _num(a) == _num(b), "all_verified": novo.get("all_verified")}', 1),
    ('        mud[n_] = {"antes": a[:300], "depois": b[:300], "so_numeros": _num(a) == _num(b), "all_verified": (cs2.get(n_) or {}).get("all_verified")}',
     '        mud[n_] = {"antes": a, "depois": b, "so_numeros": _num(a) == _num(b), "all_verified": (cs2.get(n_) or {}).get("all_verified")}', 1),
    ('        mud.pop(n_); iguais_v.append(n_ + "(contagens CORE_n_ normalizadas)")\n',
     '        mud.pop(n_); iguais_v.append(n_ + "(contagens CORE_n_ normalizadas)"); cs2[n_] = copy.deepcopy(core0[n_]); restauradas_contagens.append(n_)   # o rito computa este registro no ponto do main (o valor da v399 selada: o main e\' o mesmo); o ensaio o recomputa sobre o core inteiro: so\' as CONTAGENS diferem\n'
     '# [v400] a UNICA troca esperada: o veredito do estatuto da prova (v391) carrega o hash do PROPRIO um.py (a certificacao pelo proprio hash): o do candidato no lugar do da v399; so\' isso (e as contagens CORE_n_, normalizadas acima) pode mudar\n'
     '_HA, _HD = hashlib.sha256(open(os.path.join(BASE, "um.py"), "rb").read()).hexdigest(), hashlib.sha256(open(os.path.join(DRY, "um.py"), "rb").read()).hexdigest()\n'
     'troca_esperada = {}\n'
     'for n_, d_ in list(mud.items()):\n'
     '    if n_ == "estatuto_da_prova_v391" and d_.get("all_verified") is True and d_["antes"] != d_["depois"] and _nc(d_["antes"]).replace(_HA[:16], _HD[:16]) == _nc(d_["depois"]):\n'
     '        troca_esperada[n_] = mud.pop(n_)\n'
     'for d_ in mud.values():   # o relatorio guarda so\' o comeco; a comparacao acima foi sobre a string INTEIRA\n'
     '    d_["antes"], d_["depois"] = d_["antes"][:300], d_["depois"][:300]\n', 1),
    ('"mudaram": mud,', '"mudaram": mud, "troca_esperada_so_o_hash_proprio": troca_esperada, "contagens_do_instante_restauradas_ao_da_v399": restauradas_contagens,', 1),
    ('cs2 = copy.deepcopy(core_s); mud = {}; iguais_v = []', 'cs2 = copy.deepcopy(core_s); mud = {}; iguais_v = []; restauradas_contagens = []', 1),
    # ---- o selo: o que pode diferir do selo da v399 SELADA e' EXPLICADO, chave por chave (nada de "set(...) <= {...}" largo nem de "qualquer coisa")
    ('selo_ok = (not _seal_err and ',
     '# [v400] o que pode diferir do selo da v399 SELADA: (i) selo_pela_propria_tecnologia_v399, um_version e sha256 (os hashes do novo um.py -- o proprio proposito da versao); (ii) UMA chave que carrega o hash do proprio programa:\n'
     '#   estatuto_da_prova_v391 (a certificacao pelo proprio hash: o UNICO campo que muda e\' o hash do um.py, o do candidato no lugar do da v399)\n'
     '_H_ANTES = hashlib.sha256(open(os.path.join(BASE, "um.py"), "rb").read()).hexdigest(); _H_DEPOIS = hashlib.sha256(_UMB).hexdigest()\n'
     '\n\n'
     'def _selo_explica(k_):\n'
     '    a_, b_ = selo0.get(k_), seal.get(k_)\n'
     '    if k_ == "estatuto_da_prova_v391":\n'
     '        return J_(a_).replace(_H_ANTES, _H_DEPOIS).replace(_H_ANTES[:16], _H_DEPOIS[:16]) == J_(b_)\n'
     '    return False\n'
     '\n\n'
     '_selo_inexplicado = sorted(k_ for k_ in mud_selo if k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256") and not _selo_explica(k_))\n'
     'rep["selo"]["difere_e_nao_e_so_o_esperado"] = _selo_inexplicado\n'
     'selo_ok = (not _seal_err and ', 1),
    ('"um_version" in mud_selo and set(mud_selo) <= {"selo_pela_propria_tecnologia_v399", "um_version", "sha256"})',
     '"um_version" in mud_selo and not _selo_inexplicado)', 1),
    # ---- o sumario do artigo: o titulo da introducao diz `v384 a <versao desta rodada>`; com tres digitos o prefixo `v39` da v399 nao serve mais
    ('"v384 a v39"]', '"v384 a v400"]', 1),
    ('"v384 to v39"]', '"v384 to v400"]', 1),
])
