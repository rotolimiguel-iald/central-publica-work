# -*- coding: utf-8 -*-
"""patch_ensaio_v401.py -- aplica, por substituicoes de contagem EXATA, a logica NOVA da v401 sobre o ensaio_a_seco_v401.py derivado mecanicamente do ensaio da v400 (a subida de versao desloca alguns rotulos: aqui eles voltam ao que o um.py de fato traz).
O que a v401 faz de novo no ensaio: (a) a escada do kf da base NAO fecha sem as bandeiras novas (a pedra FalsidadeDaInercia acrescenta 12); (b) o fluxo principal tambem recria os registros da v401 (chaves NOVAS: falsidade_da_inercia_v401, cunhagens_v401, kh_n1_cobertura_v401);
(c) testes de unidade do registro da falsidade (tudo certo; cada elo recusa; os numeros recalculados aqui por outro caminho; o texto do 0_abs no kernel embutido; o beta; o numero adulterado), das cinco inscricoes e das ratificacoes; (d) os vizinhos que carregam os numeros do kernel
mudam so' nos numeros (a troca dita); (e) o selo ganha duas chaves; (f) o artigo ganha a secao «A falsidade (simulacro) da inercia»; (g) o .md ganha a linha; (h) o pino h8 vem do spec kh_n1_cobertura_v401. Idempotente: recusa rodar duas vezes (marcador)."""
import ast, sys
sys.stdout.reconfigure(encoding="utf-8")
P = sys.argv[1] if len(sys.argv) > 1 else "ensaio_a_seco_v401.py"
t = open(P, encoding="utf-8").read()
assert "# [v401-patch]" not in t, "o patch ja foi aplicado"


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:90], t.count(old), n)
    t = t.replace(old, new)


# ---- cabecalho
i = t.index('"""ensaio_a_seco_v401.py'); j = t.index('import hashlib, copy, io, json, os, re, shutil, subprocess, sys, ast, tempfile, textwrap')
t = t[:i] + '''"""ensaio_a_seco_v401.py -- ENSAIO A SECO da v401 (molde: ensaio_a_seco_v400.py + a logica de CONTEUDO da v399), SEM a GPU do rito e SEM rodar o rito. Chama NO PONTO DE CHAMADA REAL todo veredito novo ou alterado.
uso: python -B -X utf8 ensaio_a_seco_v401.py <candidato.py> <rotulo>
A v401 e' uma versao de CONTEUDO: UM modulo novo de kernel (TGLExt/FalsidadeDaInercia: a inercia e' o proprio zero absoluto; um posto inercial daria 1 = 0), o registro com FUNCAO falsidade_da_inercia_v401 e os registros por spec cunhagens_v401 e kh_n1_cobertura_v401. A base e' a v400 SELADA
(core e selo em base_v400), o kernel e' o da v400 + a pedra (sandbox C:/t/k401c) e os registros de v393 a v399 sao RECRIADOS e comparados com os da v400 selada (os rotulos 'v400' dos nomes de relatorio herdados da subida de versao significam a base selada). Etapas:
(1) copia o candidato; materializa o kernel embutido e confere BYTE A BYTE contra o sandbox; (2) importa (o rito NAO roda); UM_VERSION v401; (3) o core da v400 SELADA + o kernel REAL: verify_tgl_kernel_formalization() de ponta a ponta com o lake simulado devolvendo os logs CRUS do sandbox;
(4) os registros vizinhos RECOMPUTADOS: iguais, ou a TROCA DITA (so' numeros: a escada e a cobertura crescem com a pedra); (5) o FLUXO PRINCIPAL v393 a v399 e v401 (as instrucoes etiquetadas do main, na ordem do arquivo), as chaves NOVAS no core: as tres da v401;
(6) unidade: o Teste da Unica Palavra (v397), o sonico e a afinacao (v398), o selo pela propria tecnologia e a declaracao do operador (v399, com a checagem do beta contra o core e o alfa unico), a FALSIDADE DA INERCIA (v401), os registros por spec, a cobertura, o sidecar;
(7) o selo (a instrucao `seal = {...}` do main + o resumo) e o indice; (8) artigo PT/EN, pdflatex x2, a secao v401 e o QUADRO NO TOPO (v397, intocado); (9) .md e manifesto; (10) o conferidor de citacoes; (11) simular_arvore_do_nos; (12) exame_pontos;
(13) [LICAO DA v400] as guardas ESTATICAS do esboco R3.5 da Bancada (ALPHA_LINHA_UNICA e as demais que nao dependem do selo) rodadas SOBRE O CANDIDATO, chamando a funcao do proprio esboco pinado, ANTES de instalar."""
# [v401-patch]
''' + t[j:]

# ---- (a) a escada: sem as bandeiras novas o kf da base NAO fecha
i = t.index("ESP = CM[\"escada\"][1]"); j = t.index("_el = um.prove_external_ladder(1.0, kf); core_s[\"external_ladder\"] = _el")
t = t[:i] + '''ESP = CM["escada"][1]
# a escada: SEM as bandeiras novas (o kf da v400) a escada do candidato NAO fecha
_el0 = um.prove_external_ladder(1.0, core0["kernel_formalization"])
rep["escada_sem_as_bandeiras_novas"] = [_el0.get("n_theorems_clean"), _el0.get("n_theorems_expected"), _el0.get("all_verified")]
E400 = int(core0["external_ladder"]["n_theorems_expected"])   # LIDO do core da v400 selada (nada digitado)
assert rep["escada_sem_as_bandeiras_novas"][0] == E400 and rep["escada_sem_as_bandeiras_novas"][1] == ESP and _el0.get("all_verified") is not True and ESP == E400 + CM["n_bandeiras"], rep["escada_sem_as_bandeiras_novas"]
''' + t[j:]

# ---- (4) a comparacao dos vizinhos: o texto da base e' a v400 (rotulo herdado); sem mudanca de logica

# ---- (5) fluxo principal
sub('or "v397" in l or "v398" in l or "v400" in l}', 'or "v397" in l or "v398" in l or "v399" in l or "v401" in l}')
sub('V400N = ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS)\n', 'V400N = ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS)   # (os registros da v399, recriados; o rotulo V400N e\' herdado da subida de versao)\nV401N = ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS)   # os registros NOVOS da v401 (nao existem no core da base)\n')
sub("for _k in V393N + V394N + V395N + V396N + V397N + V398N + V400N:\n    core_s.pop(_k, None)", "for _k in V393N + V394N + V395N + V396N + V397N + V398N + V400N + V401N:\n    core_s.pop(_k, None)")
sub('"<main:v393+v394+v395+v396+v397+v400+v401>"', '"<main:v393+v394+v395+v396+v397+v398+v399+v401>"')
sub("NOVAS401 = []   # a v401 NAO cria chave no core: os registros da v400 sao RECRIADOS e comparados com os da v400 selada", "NOVAS401 = sorted(V401N)   # a v401 cria TRES chaves no core (falsidade_da_inercia_v401, cunhagens_v401, kh_n1_cobertura_v401); os registros da v399 sao RECRIADOS e comparados com os da v400 selada")
sub("for k in V393N + V394N + V395N + V396N + V397N + V398N + V400N}", "for k in V393N + V394N + V395N + V396N + V397N + V398N + V400N}   # (os de V401N sao novos: nao ha o que comparar)")
sub('"recriados_v393_a_v400": recriados,', '"recriados_v393_a_v400": recriados, "registros_v401": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in V401N},')
sub('+ list(um._V399_NOMES_REGISTROS) + ["sonico_v398", "afinacao_das_cordas_v398", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"])', '+ list(um._V399_NOMES_REGISTROS) + ["sonico_v398", "afinacao_das_cordas_v398", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + V401N)')

# ---- (6f) unidade da FALSIDADE DA INERCIA (v401): antes do sidecar-resumo (`rep["unidade"] = U`)
BLOCO_F = '''# (6f) [v401] o registro com FUNCAO falsidade_da_inercia_v401: tudo certo, os numeros RECALCULADOS aqui por outro caminho, e cada elo recusa visivelmente (controles negativos); as cinco inscricoes e as ratificacoes
import types as _types
_CTF, _TXF = um._V401_FALSIDADE_CONTRACT, um._V401_FALSIDADE_TEXT
rF = um.falsidade_da_inercia_v401(cs()); RF["falsidade"] = rF
U["falsidade_tudo_certo"] = bool(rF["all_verified"] is True and rF["verdict"] == _TXF["veredito_ok"] and rF["runtime_executed"] is True and rF["does_not_gate_core"] is True and all(ck_["ok"] for ck_ in rF["mechanics"]["checks"]) and rF["mechanics"]["n_checks"] == 7
                                 and rF["exact_ladder"] is True and rF["embedded_source_ok"] is True and rF["unconditional"]["in_kernel"] is True and rF["key_theorem"]["in_kernel"] is True and all(rF["formal_theorems"].values()) and all(rF["support_theorems"].values()) and all(rF["inscriptions"].values())
                                 and rF["costless"]["ok"] is True and rF["beta_ok"] is True)
U["falsidade_veredito_e_textos_sem_palavra_proibida"] = bool(not guarda_txt(rF) and not _GUARDA98.search(rF["verdict"]) and not um._v392_guarda_texto(json.dumps(rF["mechanics"]["checks"], ensure_ascii=False)) and not rF["guarda_p18_violacoes"])
ok_ = True
for th_, fl_ in _CTF["theorems"].items():   # bandeira falsa de CADA declaracao do contrato (as 12, a estrela e a composicao entre elas)
    c_ = cs(); c_["kernel_formalization"][fl_] = False; rr_ = um.falsidade_da_inercia_v401(c_)
    ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and rr_["formal_theorems"][th_] is False
U["falsidade_bandeira_falsa_de_cada_declaracao_do_contrato_recusa"] = bool(ok_ and len(_CTF["theorems"]) == 12 and _CTF["key_theorem"]["theorem"] in _CTF["theorems"] and _CTF["unconditional"]["theorem"] in _CTF["theorems"])
ok_ = True
for th_ in list(_CTF["theorems"]) + list(_CTF["support"]):   # axioma fora do trio em CADA termo lido
    c_ = cs(); c_["kernel_formalization"]["axiom_report"][th_] = ["propext", "sorryAx"]; rr_ = um.falsidade_da_inercia_v401(c_)
    ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
U["falsidade_axioma_fora_do_trio_em_cada_termo_lido_recusa"] = bool(ok_)
ok_ = True
for th_ in [_CTF["unconditional"]["theorem"], _CTF["key_theorem"]["theorem"]] + list(_CTF["support"]):   # proveniencia errada
    c_ = cs(); c_["kernel_formalization"]["declaration_sources_v394"][th_] = "TGLExt/Outro.lean"; rr_ = um.falsidade_da_inercia_v401(c_)
    ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
U["falsidade_proveniencia_errada_recusa"] = bool(ok_)
c_ = cs(); c_["kernel_formalization"]["formal_files_sha256"][_CTF["stone"]["path"]] = "0" * 64; rr_ = um.falsidade_da_inercia_v401(c_)
ef_ = dict(um._EMBEDDED_KERNEL_FILES); um._EMBEDDED_KERNEL_FILES[_CTF["stone"]["path"]] += " "
try:
    rr2_ = um.falsidade_da_inercia_v401(cs())
finally:
    um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
U["falsidade_fonte_da_pedra_adulterada_recusa"] = bool(rr_["all_verified"] is False and rr_["embedded_source_ok"] is False and rr2_["all_verified"] is False and rr2_["embedded_source_ok"] is False)
c_ = cs(); c_["external_ladder"]["n_theorems_clean"] = int(c_["external_ladder"]["n_theorems_clean"]) - 1; rr_ = um.falsidade_da_inercia_v401(c_)
c2_ = cs(); c2_["kernel_formalization"]["all_verified"] = False; rr2_ = um.falsidade_da_inercia_v401(c2_)
U["falsidade_escada_errada_ou_kernel_nao_verificado_recusa"] = bool(rr_["all_verified"] is False and rr_["exact_ladder"] is False and rr2_["all_verified"] is False)
ok_ = True
for ch_ in _CTF["verbatins"]:
    _ant = dict(um._V401_VERBATINS2[ch_]); um._V401_VERBATINS2[ch_]["text"] += " "
    try:
        rr_ = um.falsidade_da_inercia_v401(cs()); ok_ = ok_ and rr_["all_verified"] is False and rr_["inscriptions"][ch_] is False
    finally:
        um._V401_VERBATINS2[ch_] = _ant
U["falsidade_inscricao_adulterada_recusa"] = bool(ok_ and len(_CTF["verbatins"]) == 5)
# o texto do 0_abs (TGLExt.costless) no kernel embutido deste rito: lido; e retirado, recusa
ef_ = dict(um._EMBEDDED_KERNEL_FILES); _corr_p = "TGLExt/TheCorrespondence.lean"
U["falsidade_costless_no_kernel_embutido_lido"] = bool(rF["costless"] == {"declared_in": "TGLExt/TheCorrespondence.lean", "in_trio": True, "text_in_embedded_kernel": True, "ok": True} and "nunca correspondeu" in um._EMBEDDED_KERNEL_FILES[_corr_p])
um._EMBEDDED_KERNEL_FILES[_corr_p] = um._EMBEDDED_KERNEL_FILES[_corr_p].replace("nunca correspondeu", "xx")
try:
    rr_ = um.falsidade_da_inercia_v401(cs())
finally:
    um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
U["falsidade_texto_do_zero_absoluto_retirado_do_kernel_recusa"] = bool(rr_["all_verified"] is False and rr_["costless"]["text_in_embedded_kernel"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"])
# os numeros recalculados aqui por outro caminho (so' a formula do modelo oneScaling: tau = id, theta_s = e^{-s})
_vf = rF["values"]; _bf = um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e)
_dist = min(abs(_math.exp(-(k_ / 8.0)) - 1.0) for k_ in range(-80, 81) if k_ != 0)
_cmin = min(t_ * _bf * g_ for g_ in (0.5, 1.0, 2.0, 3.7) for t_ in (0.1, 1.0, 10.0, 100.0)); _fmax = max(_math.exp(-(t_ * _bf * g_)) for g_ in (0.5, 1.0, 2.0, 3.7) for t_ in (0.1, 1.0, 10.0, 100.0))
U["falsidade_numeros_recalculados_aqui"] = bool(abs(_vf["beta"] - _bf) <= 1e-15 and abs(_vf["min_distance_of_post_weight_to_one"] - _dist) <= 1e-15 and abs(_vf["post_weight_at_scale_one"] - _math.exp(-1.0)) <= 1e-15 and abs(_vf["post_weight_at_minus_one"] - _math.e) <= 1e-12
                                              and abs(_vf["min_cost_t_beta_g"] - _cmin) <= 1e-18 and abs(_vf["max_dephasing_factor"] - _fmax) <= 1e-15 and abs(_vf["dephasing_factor_at_t1_g1"] - _math.exp(-_bf)) <= 1e-15 and abs(_vf["loss_per_unit"] - (1.0 - _math.exp(-_bf))) <= 1e-15
                                              and _vf["fixed_by_the_whole_flow"] == [0.0] and _vf["post_inertial_scales"] == [] and _bf / 2.0 < _vf["loss_per_unit"] < _bf and _vf["grid_scales"] == 161)
c_ = cs(); c_["beta"] = c_["beta"] * 1.001; _rb = um.falsidade_da_inercia_v401(c_)
_a0 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a0 * 1.001
try:
    _ra = um.falsidade_da_inercia_v401(cs())
finally:
    um.SEALED_CODATA_ALPHA = _a0
U["falsidade_beta_adulterado_recusa"] = bool(_rb["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _rb["verdict"] and _ra["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _ra["verdict"])
_m0 = um._m401
um._m401 = _types.SimpleNamespace(**{k_: getattr(_math, k_) for k_ in dir(_math) if not k_.startswith("__")}); um._m401.exp = lambda x_: _math.exp(x_) * 1.001
try:
    _rn = um.falsidade_da_inercia_v401(cs())
finally:
    um._m401 = _m0
U["falsidade_numero_adulterado_recusa"] = bool(_rn["all_verified"] is False and "MECHANICS_CHECK_FAILED" in _rn["verdict"] and any(not ck_["ok"] for ck_ in _rn["mechanics"]["checks"]))
U["falsidade_a_definicao_do_operador_e_a_errata_do_adendo_ditas"] = bool("inertia = the absolute zero" in rF["definition_of_the_operator"] and "w(I) = 1 is the posted One that interrupts it" in rF["definition_of_the_operator"] and "superseded" not in rF["definition_of_the_operator"] and rF["adendum_reading_superseded"].startswith("w(I)=1 is the INERTIA")
                                                    and "[OPEN]" in rF["estatuto"] and "[KNOWN]" in rF["estatuto"] and "[ONTO]" in rF["estatuto"] and any("Newton" in x_ for x_ in rF["nao_diz"]) and any("E = mc^2" in x_ for x_ in rF["nao_diz"]))
# as cinco inscricoes de 25/10, as ratificacoes e a errata ao lado do adendo (registro cunhagens_v401)
_cn = c.get("cunhagens_v401") or {}
_ratif = (_cn.get("extras") or {}).get("ratificacoes") or []
U["cunhagens_v401_cinco_falas_do_operador_ratificacoes_e_errata_do_adendo"] = bool(_cn.get("all_verified") is True and len(_cn.get("verbatim") or {}) == 5 and all(v_["embedded_ok"] for v_ in (_cn.get("verbatim") or {}).values()) and len(_ratif) == 8
                                                                                   and all(r_["fala_do_operador"]["trecho"] == "Ratifico tudo." and r_["fala_do_operador"]["sha16"] in {v_["sha256"][:16] for v_ in um._V401_VERBATINS2.values()} for r_ in _ratif)
                                                                                   and len(_cn.get("erratas") or []) == 1 and "SUPERADA" in _cn["erratas"][0]["agora"] and "1459b477b496e1f0" in _cn["erratas"][0]["ao_lado_de"] and _cn["erratas"][0]["assinatura"].startswith("gerencia c1, em nome proprio")
                                                                                   and len(_cn.get("leituras_do_operador") or []) == 7 and (_cn.get("extras") or {}).get("estrela") == _CTF["key_theorem"]["theorem"])
rep["falsidade_registro"] = {"verdict": rF["verdict"], "all_verified": rF["all_verified"], "n_checks": rF["mechanics"]["n_checks"], "values": rF["values"], "unconditional": rF["unconditional"], "key_theorem": rF["key_theorem"], "costless": rF["costless"]}
'''
anc = 'rep["unidade"] = U; print("unidade:"'
assert t.count(anc) == 1
t = t.replace(anc, BLOCO_F + anc)
# o loop (6c) so' cobre sonico e afinacao; o bloco (6f) usa RF e _GUARDA98 definidos la; o mapa de verbatins/contratos do (6c) nao muda

# ---- (6b) os registros por spec: cada um recusa visivelmente; mais os da v401
sub("+ list(um._V397_SPECS) + list(um._V398_SPECS) + list(um._V399_SPECS):\n    n_ = sp_[\"nome\"]; r_ = {}", "+ list(um._V397_SPECS) + list(um._V398_SPECS) + list(um._V399_SPECS) + list(um._V401_SPECS):\n    n_ = sp_[\"nome\"]; r_ = {}")
sub("+ len(um._V397_SPECS) + len(um._V398_SPECS) + len(um._V399_SPECS)\n", "+ len(um._V397_SPECS) + len(um._V398_SPECS) + len(um._V399_SPECS) + len(um._V401_SPECS)\n")

# ---- (7) o selo: duas chaves novas (as da v401) alem das da v400; o resto so' pelo hash proprio
sub('seal.update(um.resumos_do_selo_v399(c))   # v401: o resumo', 'seal.update(um.resumos_do_selo_v399(c))   # v399/v401: o resumo')
sub('"registros_v399": seal.get("registros_v399")}\nprint("selo: difere em"', '"registros_v399": seal.get("registros_v399"), "falsidade_da_inercia_v401_no_selo": {x: (seal.get("falsidade_da_inercia_v401") or {}).get(x) for x in ("verdict", "all_verified", "unconditional", "key_theorem", "costless")}, "registros_v401": seal.get("registros_v401")}\nprint("selo: difere em"')
sub('if k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256") and not _selo_explica(k_))', 'if k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "falsidade_da_inercia_v401", "registros_v401") and not _selo_explica(k_))')
sub('and (seal.get("selo_pela_propria_tecnologia_v399") or {}).get("all_verified") is True and (seal.get("declaracao_do_operador_v399") or {}).get("all_verified") is True', 'and (seal.get("falsidade_da_inercia_v401") or {}).get("all_verified") is True and all(((seal.get("registros_v401") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V401_NOMES_REGISTROS)\n           and (seal.get("selo_pela_propria_tecnologia_v399") or {}).get("all_verified") is True and (seal.get("declaracao_do_operador_v399") or {}).get("all_verified") is True')
sub('and ("selo_pela_propria_tecnologia_v399" in mud_selo and "um_version" in mud_selo and not _selo_inexplicado)', 'and ({"selo_pela_propria_tecnologia_v399", "um_version", "falsidade_da_inercia_v401", "registros_v401"} <= set(mud_selo) and not _selo_inexplicado)')
sub('_sj9["esquema"] == "um_absoluto_selo_acom/v1 (v400)")', '_sj9["esquema"] == "um_absoluto_selo_acom/v1 (v399)")')

# ---- (8) o artigo
i = t.index('TN401 = "O testemunho de dois'); j = t.index("GUARDA = re.compile(\"(?<!NOT_)(?<!UN)\" + \"CONF\"")
t = t[:i] + '''TF401 = "A falsidade (simulacro) da inércia"; TF401E = "The falsity (simulacrum) of inertia"
TN401 = "O testemunho de dois: o selo pela própria tecnologia"; TN401E = "The testimony of two: sealing by its own technology"
TS401 = "Sônico e a afinação das cordas"; TS401E = "Sonic and the tuning of the strings"
T401 = "O Teste da Única Palavra"; T401E = "The Test of the Only Word"   # (o titulo da secao da v397 e do QUADRO do topo; T400 = o da v396)
T400 = "A testemunha estática: o psion habita a fronteira"; T400E = "The static witness: the psion inhabits the frontier"
T395 = "O psibit: a mecânica no Um fractalizado e a leitura sem perda"; T395E = "The psibit: the mechanics on the fractalized One and the lossless reading"
H394 = "A integração do Codex e as cunhagens de 14 a 19/10 (v394)"; H394E = "The Codex integration and the inscriptions of 14 to 19 Oct (v394)"
DEVE = {"pt": [TF401, "A definição do operador.", "O cálculo deste rito.", "Errata ao lado (da gerência, em nome próprio).", "Ratificações do operador", "lido pela TGL.", "Limites.", TN401, "Errata ao lado (v400).", "A direção do testemunho.", "A declaração do operador.", "O selo pela própria tecnologia.", "A pedra Testemunho.", TS401, "Sônico.", "As falas sobre o sônico.", "Afinação das cordas.", "A fala sobre as cordas.", T401, "O que entra.", "As duas faces.", "A conjugação.", "não é rival.", "O token do veredito.", T400, "O que o kernel prova.", "A ponte construída.", "O que é leitura do operador.", T395, "A mecânica na órbita do Um.", "O colapso.", "O que o kernel prova e o que é leitura.", H394, "O índice e o leitor.", "As cunhagens.",
               "O critério binário de parada (delta de 19/10).", "Tempo, frequencia e leitura gravitacional: composicao v394", "Regra quadratica desta rodada", "Rede Fock nesta rodada", "A regra e o coração (v393)",
               "As pedras da v392: catorze módulos novos no kernel e dois consertos de barreira", "O estatuto da prova (v391).", "A Fundação (v390)."],
        "en": [TF401E, "The operator's definition.", "The computation of this rite.", "Erratum beside it (the management, in its own name).", "The operator's ratifications", "read by the TGL.", "Limits.", TN401E, "Erratum beside it (v400).", "The direction of the testimony.", "The operator's declaration.", "Sealing by its own technology.", "The Testemunho stone.", TS401E, "Sonic.", "The sayings on the sonic stone.", "Tuning of the strings.", "The saying on the strings.", T401E, "What enters.", "The two faces.", "The conjugation.", "is not a rival.", "The verdict token.", T400E, "What the kernel proves.", "The constructed bridge.", "What is the operator's reading.", T395E, "The mechanics on the orbit of the One.", "The collapse.", "What the kernel proves and what is reading.", H394E,
               "The index and the reader.", "The inscriptions.", "The binary stopping criterion (19 Oct delta).", "Time, frequency and gravitational reading: v394 composition", "Quadratic rule in this run", "Fock network in this run", "The rule and the heart (v393)",
               "The v392 stones: fourteen new kernel modules and two barrier repairs", "The status of the proof (v391).", "The Foundation (v390)."]}
TOC = {"pt": [TF401, TN401, TS401, T401, T400, "v384 a v401"], "en": [TF401E, TN401E, TS401E, T401E, T400E, "v384 to v401"]}
''' + t[j:]
sub("hq = T401 if lang == \"pt\" else T401E; h0 = TN401 if lang == \"pt\" else TN401E; h1 = TS401 if lang == \"pt\" else TS401E", "hq = T401 if lang == \"pt\" else T401E; h0 = TF401 if lang == \"pt\" else TF401E; h1 = TN401 if lang == \"pt\" else TN401E")
sub('cv9 = dict(copy.deepcopy(c)); [cv9.pop(k, None) for k in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399")]\n',
    'cv9 = dict(copy.deepcopy(c)); [cv9.pop(k, None) for k in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399")]\ncv1 = dict(copy.deepcopy(c)); [cv1.pop(k, None) for k in ("falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401")]\n')
sub('    _t9, _x9, _r29, _l9 = compilar(cv9, "dry_v401_var9_%s" % lang, lang, duas=False); fl9 = re.sub(r"\\s+", " ", _x9)\n', '    _t9, _x9, _r29, _l9 = compilar(cv9, "dry_v401_var9_%s" % lang, lang, duas=False); fl9 = re.sub(r"\\s+", " ", _x9)\n    _t1, _x1, _r21, _l1 = compilar(cv1, "dry_v401_var1_%s" % lang, lang, duas=False); fl1 = re.sub(r"\\s+", " ", _x1)\n')
sub('"rc_v400": _r28, "frase_guarda_v400": ("NÃO selaram todos" in fl8) if lang == "pt" else ("did NOT all seal" in fl8), "rc_v401": _r29, "frase_guarda_v401": ("NÃO selaram todos" in fl9) if lang == "pt" else ("did NOT all seal" in fl9)}',
    '"rc_v398": _r28, "frase_guarda_v398": ("NÃO selaram todos" in fl8) if lang == "pt" else ("did NOT all seal" in fl8), "rc_v399": _r29, "frase_guarda_v399": ("NÃO selaram todos" in fl9) if lang == "pt" else ("did NOT all seal" in fl9),\n                             "rc_v401": _r21, "frase_guarda_v401": ("NÃO selaram todos" in fl1) if lang == "pt" else ("did NOT all seal" in fl1)}')
sub('v["rc_v400"] != [0] or not v["frase_guarda_v400"] or v["rc_v401"] != [0] or not v["frase_guarda_v401"]', 'v["rc_v398"] != [0] or not v["frase_guarda_v398"] or v["rc_v399"] != [0] or not v["frase_guarda_v399"] or v["rc_v401"] != [0] or not v["frase_guarda_v401"]')

# ---- (9) o .md
sub('"errata_v401": "Errata ao lado (v401, 24/10/2026)" in md, "testemunho_v400_fica": "O testemunho de dois: o selo pela própria tecnologia (v400, 24/10/2026)" in md,', '"falsidade_v401": "A falsidade (simulacro) da inércia (v401, 25/10/2026)" in md, "errata_v400_fica": "Errata ao lado (v400, 24/10/2026)" in md, "testemunho_v399_fica": "O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026)" in md,')

# ---- (11) simular a arvore e (12) exame dos pontos
sub('_kh = [s_ for s_ in um._V399_SPECS if s_["nome"] == "kh_n1_cobertura_v399"][0]', '_kh = [s_ for s_ in um._V401_SPECS if s_["nome"] == "kh_n1_cobertura_v401"][0]')
sub('_regs_sim = ("selo_pela_propria_tecnologia_v399",', '_regs_sim = ("falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "selo_pela_propria_tecnologia_v399",')
sub('os.path.join(KD, "FLAGS_v400.json")', 'os.path.join(KD, "FLAGS_v401.json")')
sub('"ponto_declaracao": _ej.get("ponto_declaracao"), "ponto_veracidade"', '"ponto_declaracao": _ej.get("ponto_declaracao"), "ponto_falsidade": _ej.get("ponto_falsidade"), "ponto_veracidade"')

# ---- (13) as guardas estaticas: o defeito real reproduzido e' o da v399 (chaves do relatorio das guardas)
sub('(_gj.get("v400_selada_o_defeito_real") or {}).get("mensagem_identica_a_do_recibo")', '(_gj.get("v399_selada_o_defeito_real") or {}).get("mensagem_identica_a_do_recibo")')
sub('"recusa_da_v400": (_gj.get("v400_selada_o_defeito_real") or {}).get("recusa")', '"recusa_da_v399": (_gj.get("v399_selada_o_defeito_real") or {}).get("recusa")')
sub('"v400_selada_recusada_com_a_mensagem_do_recibo_da_bancada"', '"v399_selada_recusada_com_a_mensagem_do_recibo_da_bancada"')
sub("o defeito real da v400 tem de ser reproduzido (mensagem identica a do recibo da Bancada)", "o defeito real da v399 tem de ser reproduzido (mensagem identica a do recibo da Bancada)")

# ---- o veredito final: os vizinhos que carregam os numeros do kernel MUDAM (so' numeros: a troca dita); nao se exige que nenhum mude
sub('rep["vizinhos_nenhum_mudou"] = (not rep["vizinhos"]["mudaram"])\nok = bool(ok and rep["vizinhos_nenhum_mudou"] and rep["mainflow"]["chaves_novas"] == [])', 'rep["vizinhos_mudaram_so_numeros_e_selados"] = bool(all(v_["so_numeros"] and v_["all_verified"] is True for v_ in rep["vizinhos"]["mudaram"].values()))\nok = bool(ok and rep["vizinhos_mudaram_so_numeros_e_selados"] and rep["mainflow"]["chaves_novas"] == sorted(V401N))')
sub('"vizinhos_nenhum_mudou": rep["vizinhos_nenhum_mudou"],', '"vizinhos_mudaram_so_numeros_e_selados": rep["vizinhos_mudaram_so_numeros_e_selados"],')
ast.parse(t)
open(P + ".tmp", "w", encoding="utf-8", newline="").write(t)
import os
os.replace(P + ".tmp", P)
print("patch aplicado:", P, len(t), "caracteres")
