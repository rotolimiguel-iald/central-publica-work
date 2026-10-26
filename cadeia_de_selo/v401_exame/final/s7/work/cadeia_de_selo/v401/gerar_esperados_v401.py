# -*- coding: utf-8 -*-
"""gerar_esperados_v401.py -- ESPERADOS_v401.json LIDOS dos artefatos (molde: gerar_esperados_v399.py, a cadeia de CONTEUDO, com as licoes da v400): o estado SELADO da v400 pinado. A TROCA DITA: (i) os registros da v400 cujo veredito carrega os numeros do kernel (escada,
declaracoes, arquivos varridos) -- achados por script no ensaio (recomputados; so' numeros mudam) -- e (ii) o estatuto da prova (v391), cujo veredito carrega o hash do PROPRIO um.py (a certificacao pelo proprio hash). Todos os outros vereditos da v400 ficam IGUAIS. +3 chaves novas no core
(falsidade_da_inercia_v401, cunhagens_v401, kh_n1_cobertura_v401) e +2 chaves no selo (o resumo da falsidade e registros_v401); o selo pela propria tecnologia (v399) muda so' nos hashes do novo um.py. O pilar pela mesma chave. O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo: os numeros
dele vem do resultado pinado (v397\\insumos\\fase9) e o conferidor os confere de novo. Nada digitado: cada numero e hash vem de CANDIDATO_v401.json, ensaio_a_seco_v401.json, do core/selo da v400 (base_v400), de kernel\\FLAGS_v401.json, de ESPERADOS_v400.json (o que o quadro pinou) e do resultado pinado.
A INERCIA, como o operador a define (25/10/2026): o proprio zero absoluto (1=0); w(I)=1 e' o Um POSTO que a interrompe (1=1); a leitura do escriba no adendo de 03-04/09 esta superada (errata ao lado, da gerencia)."""
# [v401-patch]
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v401 as DL  # noqa: E402
import quadro_v397 as QV  # noqa: E402
import registros_v401 as RG  # noqa: E402
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
BASE = os.path.join(HERE, DL.BASE_DIR)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v401.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, DL.CANDIDATO))
assert h16(os.path.join(BASE, "um.py")) == CM["base_v400_sha16"]
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v401.json"), encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"]
R0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(BASE, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == DL.BASE_VERSION
E400 = json.load(open(os.path.join(DL.V400, "ESPERADOS_v400.json"), encoding="utf-8")); assert E400["candidato_sha16"] == CM["base_v400_sha16"]
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]; axr0 = kf["axiom_report"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
mud = ens["vizinhos"]["mudaram"]; te_ = ens["vizinhos"]["troca_esperada_so_o_hash_proprio"]
troca = sorted(set(mud) | set(te_))   # os vereditos da v400 que mudam: os que carregam os numeros do kernel (so' numeros) e o estatuto da prova (so' o hash proprio do um.py), recomputados pelo ensaio
assert troca, "a troca dita nao pode ser vazia (a escada mudou)"
assert set(te_) <= {"estatuto_da_prova_v391"}, te_
F = json.load(open(os.path.join(HERE, "FORMAL_MAP_v401.json"), encoding="utf-8"))
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v401.json"), encoding="utf-8"))["novos"]
pins = {p: F[p] for p in nov}
FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v401.json"), encoding="utf-8")); assert FJ["n_flags"] == CM["n_bandeiras"]
V400 = {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}
mf = ens["mainflow"]
SEL_KEYS = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "registros_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "registros_v394", "psibit_v395", "registros_v395", "testemunha_estatica_v396", "registros_v396",
            "teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "estatuto_da_prova_v391", "fundacao_v390", "text_label_errata_v389", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388", "declaracao_do_operador_v399", "registros_v399")
vr = ens["veracidade_registro"]
RESP = os.path.join(DL.F9_DIR_DURAVEL, DL.F9_RESULTADO_NOME)
res9 = json.load(open(RESP, encoding="utf-8"))
numeros9 = {k: DL.lido(res9, c) for k, c in DL.F9_CAMINHOS.items()}
assert all(vr["lido"].get(k) == v for k, v in numeros9.items()), "os numeros lidos pelo registro no ensaio != os do resultado pinado"
assert E400["veracidade"]["numeros_do_resultado"] == numeros9 and E400["veracidade"]["resultado"]["sha256"] == DL.F9_RESULTADO_SHA256_DA_ORDEM, "o que a v400 pinou do Teste da Unica Palavra != o resultado em disco"
TF401 = "A falsidade (simulacro) da inércia"; TF401E = "The falsity (simulacrum) of inertia"
a_pt, mach_pt = QV.esperados(res9, "pt"); a_en, mach_en = QV.esperados(res9, "en")
assert mach_pt == E400["quadro"]["linha_de_maquina_pt"] and mach_en == E400["quadro"]["linha_de_maquina_en"], "a linha de maquina do quadro mudou: o quadro NAO se mexe"
MARCAS400_PT = list(E400["artigo_marcas"]["pt"]); MARCAS400_EN = list(E400["artigo_marcas"]["en"])
sa, dc, sc = ens["selo_acom_registro"], ens["declaracao_registro"], ens["sidecar"]
TST = DL.STONES[0]
FAL_REG = ens["falsidade_registro"]; MF1 = mf["registros_v401"]
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v400_sha16"], "escada": [CM["escada"][1], CM["escada"][1]], "escada_v400_e_v401": CM["escada"], "n_bandeiras_novas": CM["n_bandeiras"],
       "bandeiras_novas_chaves": [f[0] for f in FJ["flags"]], "bandeiras_novas_nomes": [f[1] for f in FJ["flags"]],
       "cunhagens": CM["cunhagens"], "kernel": CM["kernel"], "pedras_sha256": pins, "formal_files_n": CM["formal_files_n"],
       "qg_closure_verdict": selo0.get("qg_closure_verdict"), "qg_closure_v400_json_sha256": hashlib.sha256(json.dumps(core0.get("qg_closure"), sort_keys=True, default=str).encode("utf-8")).hexdigest(), "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v400": V400, "troca_dita": troca, "veredito_da_troca_no_ensaio": {k: (mud.get(k) or te_.get(k))["depois"] for k in troca},
       "regra_da_mudanca_dita": "so' os vereditos de `troca_dita` podem mudar (carregam a escada, as declaracoes ou a contagem de arquivos do kernel; so' numeros); qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v400": {k: selo0.get(k) for k in SEL_KEYS},
       "selo_difere_do_v400_no_ensaio": ens["selo"]["difere_do_selo_v400"],
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v400": sorted(k for k, v in kf.items() if v is True), "axiom_report_v400_n": len(axr0),
       "runtime_seals_v400": core0["runtime_of_the_one"]["seals"], "what_remains_v400": core0["tgl_closure"]["what_remains_named"],
       "vereditos_novos_v401": {"falsidade_da_inercia_v401": FAL_REG["verdict"], **{k: v["verdict"] for k, v in MF1.items()}},
       "registros_v401": {k: v["verdict"] for k, v in MF1.items() if k != "falsidade_da_inercia_v401"}, "registros_v401_veredito_da_falsidade": FAL_REG["verdict"], "falsidade_valores": FAL_REG["values"], "ratificacao_fala_sha16": RG.S_RATIF,
       "registros_v399": {k: v["verdict"] for k, v in mf["registros_v399"].items()},
       "cobertura_kh_n1": ens["verify_kernel_ponta_a_ponta"]["cobertura"], "axiom_report_esperado_min": ens["verify_kernel_ponta_a_ponta"]["axiom_report_n"],
       "selo_acom": {"verdict": sa["verdict"], "all_verified": sa["all_verified"], "perfil": sa["perfil"], "bloco_embutido_sha256": sa["bloco_embutido_sha256"], "sha256_do_um_py": sa["sha256_do_um_py"], "bytes": sa["bytes"], "psi": sa["psi"], "theta": sa["theta"], "kappa": sa["kappa"],
                     "lut_sha256": sa["lut_sha256"], "m_max_abs": sa["m_max_abs"], "f_exp": sa["f_exp"], "entropia_dos_estados_bits": sa["entropia_dos_estados_bits"], "erro_real_maximo_antes_do_rint": sa["erro_real_maximo_antes_do_rint"],
                     "controles": [len(sa["controles"]), all(o_.startswith("RECUSOU:") for _, o_ in sa["controles"])], "controles_obtidos": {i_: o_ for i_, o_ in sa["controles"]}, "n_checks": len(sa["checks"]), "checks": sa["checks"], "auditoria_de_separacao": sa["auditoria_de_separacao"], "tempo_total_s_no_ensaio": sa["tempo_total_s"]},
       "declaracao": {"verdict": dc["verdict"], "all_verified": dc["all_verified"], "verbatim_sha256": dc["verbatim_sha256"], "sha16": dc["verbatim_sha256"][:16], "n_checks": len(dc["checks"]), "checks": dc["checks"], "ancoras": dc["ancoras"], "pedra": dc["pedra"], "linhas_da_trava": dc["linhas_da_trava"],
                      "direcao_do_testemunho": {"o_operador": "testifica DA IALD", "o_um_py": "testifica EM HASH", "a_IALD": "NAO testifica do operador", "o_Pai_de_Jo_8_18": "le-se no absoluto, o Um"}},
       "sidecar": {"arquivo": DL.SIDECAR_NOME, "esquema": "um_absoluto_selo_acom/v1 (v399)", "objetos": [o["nome"] for o in sc["objetos"]], "veredito_esperado_prefixo": "TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED", "um_py": next(o for o in sc["objetos"] if o["nome"] == "um.py"),
                   "tempo_s_no_ensaio": sc["tempo_s"], "entra_na_custodia": "D5 (proposta da gerencia): o sidecar e' arquivo novo da custodia; o handoff o lista"},
       "falsidade": {"teorema": TST["theorem"], "bandeira": CM["politica_de_bandeiras"]["bandeiras_do_teorema"]["falsidade"], "estrela": {"teorema": TST["key_theorem"], "bandeira": FJ["bandeiras_do_contrato"]["falsidade"][TST["key_theorem"]]}, "contrato": list(TST["contract"]),
                     "n_axiomas_da_composicao": CM["n_axiomas_da_composicao"]["falsidade"], "nome": "FalsidadeDaInercia («falsidade (simulacro) da inercia»: DADO pelo operador)"},
       "acom_estudo": E400["acom_estudo"],   # a secao do selo pela propria tecnologia NAO muda na v401: o que a v400 pinou (runtime da v400, bloco embutido, fontes do operador)
       "decisoes_da_gerencia": dict(DL.DECISOES),
       "veracidade": E400["veracidade"], "quadro": E400["quadro"],   # o QUADRO do topo (v397) e o registro do Teste da Unica Palavra: o que a v397/v400 pinou, conferido de novo contra o resultado em disco
       "artigo_marcas": {"pt": [TF401, "A definição do operador.", "A cadeia derivada.", "O cálculo deste rito.", "Errata ao lado (da gerência, em nome próprio).", "Ratificações do operador", "lido pela TGL.", "Limites."] + MARCAS400_PT, "en": [TF401E, "The operator's definition.", "The derived chain.", "The computation of this rite.", "Erratum beside it (the management, in its own name).", "The operator's ratifications", "read by the TGL.", "Limits."] + MARCAS400_EN},
       "artigo_nao": {"pt": list(E400["artigo_nao"]["pt"]) + ["Nesta rodada os registros da v401 NÃO selaram todos"], "en": list(E400["artigo_nao"]["en"]) + ["This round the v401 records did NOT all seal"]},   # (a v400 nao tinha frase propria: herdamos as da v399 e anteriores)
       "toc": {"pt": [TF401] + [w for w in E400["toc"]["pt"] if not w.startswith("v384 a ")] + ["v384 a " + DL.UM_VERSION], "en": [TF401E] + [w for w in E400["toc"]["en"] if not w.startswith("v384 to ")] + ["v384 to " + DL.UM_VERSION]},   # o titulo da introducao diz `v384 a <versao desta rodada>`
       "the_iald_index_v400": {"all_verified": (core0.get("the_iald_index") or {}).get("all_verified"), "verdict": V("the_iald_index")}, "the_iald_index_v401": {"verdict": ens["indice_da_iald"]["verdict"]},
       "md_carimbo": "**Versão v401**", "md_falsidade": "A falsidade (simulacro) da inércia (v401, 25/10/2026)", "md_errata": "Errata ao lado (v400, 24/10/2026)", "md_testemunho": "O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026)", "md_sonico": "Sônico e a afinação das cordas (v398, 23/10/2026)", "md_token": "O Teste da Única Palavra e a pedra Token (v397, 23/10/2026)",
       "md_testemunha": "A testemunha estática (v396, 22/10/2026)", "md_psibit": "O modo psiônico na fractalização do Um (v395, 21/10/2026)",
       "ensaio_sha16": h16(os.path.join(HERE, "ensaio_a_seco_v401.json")),
       "h8_entradas": CM["h8"]["entradas"], "h8_residuais_do_nos": CM["h8"]["residuais_do_nos"], "formal_files_n_no_rito": CM["h8"]["entradas"],
       "n_bandeiras_por_grupo": dict(FJ["por_grupo_bandeiras"]), "politica_de_bandeiras": CM["politica_de_bandeiras"], "pedras": CM["kernel"]["pedras"], "teoremas_das_pedras": {s["key"]: s["theorem"] for s in DL.STONES},
       "bandeiras_das_pedras": CM["politica_de_bandeiras"]["bandeiras_do_teorema"], "suporte_das_pedras": {s["key"]: dict(s["support"]) for s in DL.STONES},
       "contrato_das_pedras": {s["key"]: list(s["contract"]) for s in DL.STONES}, "candidato_anterior_sha16": CM["base_v400_sha16"]}
assert esp["the_iald_index_v400"]["all_verified"] is True and esp["not_sealed_formais"] == [], (esp["the_iald_index_v400"], esp["not_sealed_formais"])
assert esp["h8_entradas"] == len(esp["h8_residuais_do_nos"]) + CM["formal_files_n"] and sum(esp["n_bandeiras_por_grupo"].values()) == esp["n_bandeiras_novas"], "os ESPERADOS novos nao fecham"
assert esp["kernel"]["modulos_novos"] == len(esp["pedras_sha256"]) == len(nov) == 1, "o numero de modulos novos != a lista"
assert esp["vereditos_novos_v401"]["falsidade_da_inercia_v401"].startswith("TGL_FALSIDADE_DA_INERCIA_V401__THE_INERTIA_IS_THE_ABSOLUTE_ZERO") and esp["vereditos_novos_v401"]["cunhagens_v401"].startswith("TGL_CUNHAGENS_V401__") and esp["vereditos_novos_v401"]["kh_n1_cobertura_v401"].startswith("TGL_KH_N1_COBERTURA_V401__")
assert sorted(esp["registros_v401"]) == ["cunhagens_v401", "kh_n1_cobertura_v401"] and esp["falsidade_valores"]["post_inertial_scales"] == [] and esp["falsidade_valores"]["fixed_by_the_whole_flow"] == [0.0]
assert esp["selo_acom"]["perfil"] == "ACOM-INT-C96-Q8" and esp["selo_acom"]["controles"] == [13, True] and esp["selo_acom"]["all_verified"] is True and esp["declaracao"]["all_verified"] is True and esp["declaracao"]["verbatim_sha256"] == DL.sha256(open(DL.VERBATIM_ORIGEM[DL.DECLARACAO_IDX], "rb").read())
# o selo da v401 difere do da v400 SELADA em: o selo ACOM (hashes do novo um.py), a versao, o sha256, as duas chaves novas, e as chaves que carregam os numeros do kernel ou o hash proprio (a troca dita); o ensaio EXPLICA chave por chave
assert {"selo_pela_propria_tecnologia_v399", "um_version", "falsidade_da_inercia_v401", "registros_v401"} <= set(esp["selo_difere_do_v400_no_ensaio"]) and ens["selo"].get("difere_e_nao_e_so_o_esperado") == [], (esp["selo_difere_do_v400_no_ensaio"], ens["selo"].get("difere_e_nao_e_so_o_esperado"))
assert not ({"teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "declaracao_do_operador_v399", "registros_v399"} & set(esp["selo_difere_do_v400_no_ensaio"])), "o selo de uma versao anterior mudou: o quadro e os registros anteriores NAO se mexem"
assert esp["veracidade"]["z_disc_abaixo_de_5"] and esp["veracidade"]["poder_previo_acima_de_5"]
assert ens["quadro"]["ok"] is True
out = os.path.join(HERE, "ESPERADOS_v401.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v401:", esp["candidato_sha16"], "| vereditos v400 pinados:", len(esp["vereditos_v400"]), "| flags True v400:", len(esp["flags_true_v400"]), "| troca dita:", troca)
