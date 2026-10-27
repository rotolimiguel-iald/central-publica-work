# -*- coding: utf-8 -*-
"""gerar_esperados_v400.py -- ESPERADOS_v400.json LIDOS dos artefatos (molde: gerar_esperados_v399.py): o estado SELADO da v399 pinado. A v400 e' uma CORRECAO: NENHUMA chave nova no core nem no selo, NENHUM modulo de kernel; a escada e' a da v399.
A TROCA DITA e' UMA so': o veredito do estatuto da prova (v391) carrega o hash do PROPRIO um.py (a certificacao pelo proprio hash) e muda com o programa; as contagens CORE_n_ que o ensaio computa sobre o core inteiro (um artefato dele, nao do rito) sao normalizadas.
Todos os outros vereditos da v399 ficam IGUAIS. O que a correcao muda de proposito: so' o registro do selo ACOM (os hashes do novo um.py e a checagem do beta contra o core), o sidecar, a versao e a errata ao lado no artigo e no .md. O pilar pela mesma chave.
O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo: os numeros dele vem do resultado pinado (v397\\insumos\\fase9) e o conferidor os confere de novo. Nada digitado: cada numero e hash vem de CANDIDATO_v400.json, ensaio_a_seco_v400.json, do core/selo
da v399 (base_v399), de kernel\\FLAGS_v399.json, de ESPERADOS_v399.json (o que o quadro pinou) e do resultado pinado. A DIRECAO DO TESTEMUNHO fica nos ESPERADOS como dado: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador; o Pai de Jo 8,18 le-se no absoluto."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v400 as DL  # noqa: E402
import quadro_v397 as QV  # noqa: E402
import registros_v400 as RG  # noqa: E402
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
BASE = os.path.join(HERE, DL.BASE_DIR)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v400.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, DL.CANDIDATO))
assert h16(os.path.join(BASE, "um.py")) == CM["base_v399_sha16"]
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v400.json"), encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"]
R0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(BASE, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == DL.BASE_VERSION
E399 = json.load(open(os.path.join(DL.V399, "ESPERADOS_v399.json"), encoding="utf-8")); assert E399["candidato_sha16"] == CM["base_v399_sha16"]
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]; axr0 = kf["axiom_report"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
mud = ens["vizinhos"]["mudaram"]
assert not mud, ("nenhum vizinho da v399 muda alem da troca esperada (so' o hash proprio no estatuto da prova)", sorted(mud))
te_ = ens["vizinhos"]["troca_esperada_so_o_hash_proprio"]
troca = sorted(te_)   # a UNICA troca dita: o estatuto da prova carrega o hash do proprio um.py
assert troca == ["estatuto_da_prova_v391"], troca
F = {}   # a v400 nao acrescenta modulo: nao ha FORMAL_MAP novo
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v400.json"), encoding="utf-8"))["novos"]
pins = {p: F[p] for p in nov}
FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v399.json"), encoding="utf-8")); assert CM["n_bandeiras"] == 0 and FJ["n_flags"] == CM["politica_de_bandeiras"]["n_flags"]   # FLAGS_v399: as bandeiras da v399 (novas so' para a Bancada, que pina a v398)
V399 = {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}
mf = ens["mainflow"]
SEL_KEYS = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "registros_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "registros_v394", "psibit_v395", "registros_v395", "testemunha_estatica_v396", "registros_v396",
            "teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "estatuto_da_prova_v391", "fundacao_v390", "text_label_errata_v389", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388", "declaracao_do_operador_v399", "registros_v399")
vr = ens["veracidade_registro"]
RESP = os.path.join(DL.F9_DIR_DURAVEL, DL.F9_RESULTADO_NOME)
res9 = json.load(open(RESP, encoding="utf-8"))
numeros9 = {k: DL.lido(res9, c) for k, c in DL.F9_CAMINHOS.items()}
assert all(vr["lido"].get(k) == v for k, v in numeros9.items()), "os numeros lidos pelo registro no ensaio != os do resultado pinado"
assert E399["veracidade"]["numeros_do_resultado"] == numeros9 and E399["veracidade"]["resultado"]["sha256"] == DL.F9_RESULTADO_SHA256_DA_ORDEM, "o que a v399 pinou do Teste da Unica Palavra != o resultado em disco"
TN400 = "O testemunho de dois: o selo pela própria tecnologia"; TN400E = "The testimony of two: sealing by its own technology"
a_pt, mach_pt = QV.esperados(res9, "pt"); a_en, mach_en = QV.esperados(res9, "en")
assert mach_pt == E399["quadro"]["linha_de_maquina_pt"] and mach_en == E399["quadro"]["linha_de_maquina_en"], "a linha de maquina do quadro mudou: o quadro NAO se mexe"
MARCAS399_PT = list(E399["artigo_marcas"]["pt"]); MARCAS399_EN = list(E399["artigo_marcas"]["en"])
sa, dc, sc = ens["selo_acom_registro"], ens["declaracao_registro"], ens["sidecar"]
TST = DL.STONES_DESDE_B8[0]   # a pedra Testemunho: nova para a Bancada (v398), nao para a v400
RM = json.load(open(os.path.join(HERE, "RUNTIME_MONTAGEM_v400.json"), encoding="utf-8"))
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v399_sha16"], "escada": [CM["escada"][1], CM["escada"][1]], "escada_v399_e_v400": CM["escada"], "n_bandeiras_novas": CM["n_bandeiras"],
       "bandeiras_novas_chaves": [], "bandeiras_novas_nomes": [], "bandeiras_desde_a_bancada": {"chaves": [f[0] for f in FJ["flags"]], "nomes": [f[1] for f in FJ["flags"]]},
       "cunhagens": CM["cunhagens"], "kernel": CM["kernel"], "pedras_sha256": pins, "formal_files_n": CM["formal_files_n"],
       "qg_closure_verdict": selo0.get("qg_closure_verdict"), "qg_closure_v399_json_sha256": hashlib.sha256(json.dumps(core0.get("qg_closure"), sort_keys=True, default=str).encode("utf-8")).hexdigest(), "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v399": V399, "troca_dita": troca, "veredito_da_troca_no_ensaio": {k: te_[k]["depois"] for k in troca},
       "regra_da_mudanca_dita": "so' os vereditos de `troca_dita` podem mudar (carregam a escada, as declaracoes ou a contagem de arquivos do kernel; so' numeros); qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v399": {k: selo0.get(k) for k in SEL_KEYS},
       "selo_difere_do_v399_no_ensaio": ens["selo"]["difere_do_selo_v399"],
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v399": sorted(k for k, v in kf.items() if v is True), "axiom_report_v399_n": len(axr0),
       "runtime_seals_v399": core0["runtime_of_the_one"]["seals"], "what_remains_v399": core0["tgl_closure"]["what_remains_named"],
       "vereditos_novos_v400": {"selo_pela_propria_tecnologia_v399": sa["verdict"], "declaracao_do_operador_v399": dc["verdict"]},
       "registros_v399": {k: v["verdict"] for k, v in mf["registros_v399"].items()},
       "cobertura_kh_n1": ens["verify_kernel_ponta_a_ponta"]["cobertura"], "axiom_report_esperado_min": ens["verify_kernel_ponta_a_ponta"]["axiom_report_n"],
       "selo_acom": {"verdict": sa["verdict"], "all_verified": sa["all_verified"], "perfil": sa["perfil"], "bloco_embutido_sha256": sa["bloco_embutido_sha256"], "sha256_do_um_py": sa["sha256_do_um_py"], "bytes": sa["bytes"], "psi": sa["psi"], "theta": sa["theta"], "kappa": sa["kappa"],
                     "lut_sha256": sa["lut_sha256"], "m_max_abs": sa["m_max_abs"], "f_exp": sa["f_exp"], "entropia_dos_estados_bits": sa["entropia_dos_estados_bits"], "erro_real_maximo_antes_do_rint": sa["erro_real_maximo_antes_do_rint"],
                     "controles": [len(sa["controles"]), all(o_.startswith("RECUSOU:") for _, o_ in sa["controles"])], "controles_obtidos": {i_: o_ for i_, o_ in sa["controles"]}, "n_checks": len(sa["checks"]), "checks": sa["checks"], "auditoria_de_separacao": sa["auditoria_de_separacao"], "tempo_total_s_no_ensaio": sa["tempo_total_s"]},
       "declaracao": {"verdict": dc["verdict"], "all_verified": dc["all_verified"], "verbatim_sha256": dc["verbatim_sha256"], "sha16": RG.S_DECL, "n_checks": len(dc["checks"]), "checks": dc["checks"], "ancoras": dc["ancoras"], "pedra": dc["pedra"], "linhas_da_trava": dc["linhas_da_trava"],
                      "direcao_do_testemunho": {"o_operador": "testifica DA IALD", "o_um_py": "testifica EM HASH", "a_IALD": "NAO testifica do operador", "o_Pai_de_Jo_8_18": "le-se no absoluto, o Um"}},
       "sidecar": {"arquivo": DL.SIDECAR_NOME, "esquema": "um_absoluto_selo_acom/v1 (v399)", "objetos": [o["nome"] for o in sc["objetos"]], "veredito_esperado_prefixo": "TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED", "um_py": next(o for o in sc["objetos"] if o["nome"] == "um.py"),
                   "tempo_s_no_ensaio": sc["tempo_s"], "entra_na_custodia": "D5 (proposta da gerencia): o sidecar e' arquivo novo da custodia; o handoff o lista"},
       "testemunho": {"teorema": TST["theorem"], "bandeira": CM["politica_de_bandeiras"]["bandeiras_do_teorema"]["testemunho"], "contrato": list(TST["contract"]), "n_axiomas_da_composicao": CM["n_axiomas_da_composicao"]["testemunho"], "nome": "Testemunho (PROVISORIO: quem nomeia e' o operador)"},
       "acom_estudo": {"runtime_sha256": RM["runtime"]["sha256"], "bloco_embutido_sha256": CM["acom"]["bloco_embutido_sha256"], "edicoes_declaradas": [e["edicao"] for e in RM["edicoes_declaradas"]], "colisoes_de_nomes": CM["acom"]["colisoes_de_nomes_no_um_py"],
                       "fontes_do_operador": {n: DL.sha256(open(o, "rb").read()) for n, o in DL.ACOM_FONTES_OPERADOR.items()}, "estudo": {n: DL.sha256(open(o, "rb").read())[:16] for n, (o, _) in DL.ACOM_ESTUDO.items()}},
       "decisoes_da_gerencia": dict(DL.DECISOES),
       "veracidade": E399["veracidade"], "quadro": E399["quadro"],   # o QUADRO do topo (v397) e o registro do Teste da Unica Palavra: o que a v397/v399 pinou, conferido de novo contra o resultado em disco
       "artigo_marcas": {"pt": ["Errata ao lado (v400)."] + MARCAS399_PT, "en": ["Erratum beside it (v400)."] + MARCAS399_EN},
       "artigo_nao": {"pt": list(E399["artigo_nao"]["pt"]), "en": list(E399["artigo_nao"]["en"])},
       "toc": {"pt": [w for w in E399["toc"]["pt"] if not w.startswith("v384 a ")] + ["v384 a " + DL.UM_VERSION], "en": [w for w in E399["toc"]["en"] if not w.startswith("v384 to ")] + ["v384 to " + DL.UM_VERSION]},   # nenhuma secao nova (a errata e' um paragrafo da secao da v399); o titulo da introducao diz `v384 a <versao desta rodada>`
       "the_iald_index_v399": {"all_verified": (core0.get("the_iald_index") or {}).get("all_verified"), "verdict": V("the_iald_index")}, "the_iald_index_v400": {"verdict": ens["indice_da_iald"]["verdict"]},
       "md_carimbo": "**Versão v400**", "md_errata": "Errata ao lado (v400, 24/10/2026)", "md_testemunho": "O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026)", "md_sonico": "Sônico e a afinação das cordas (v398, 23/10/2026)", "md_token": "O Teste da Única Palavra e a pedra Token (v397, 23/10/2026)",
       "md_testemunha": "A testemunha estática (v396, 22/10/2026)", "md_psibit": "O modo psiônico na fractalização do Um (v395, 21/10/2026)",
       "ensaio_sha16": h16(os.path.join(HERE, "ensaio_a_seco_v400.json")),
       "h8_entradas": CM["h8"]["entradas"], "h8_residuais_do_nos": CM["h8"]["residuais_do_nos"], "formal_files_n_no_rito": CM["h8"]["entradas"],
       "n_bandeiras_por_grupo": {}, "bandeiras_por_grupo_desde_a_bancada": dict(FJ["por_grupo_bandeiras"]), "politica_de_bandeiras": CM["politica_de_bandeiras"], "pedras": CM["kernel"]["pedras"], "pedras_desde_a_bancada": CM["kernel"]["pedras_desde_a_bancada"], "teoremas_das_pedras": {s["key"]: s["theorem"] for s in DL.STONES_DESDE_B8},
       "bandeiras_das_pedras": CM["politica_de_bandeiras"]["bandeiras_do_teorema"], "suporte_das_pedras": {s["key"]: dict(s["support"]) for s in DL.STONES_DESDE_B8},
       "contrato_das_pedras": {s["key"]: list(s["contract"]) for s in DL.STONES_DESDE_B8}, "candidato_anterior_sha16": CM["base_v399_sha16"]}
assert esp["the_iald_index_v399"]["all_verified"] is True and esp["not_sealed_formais"] == [], (esp["the_iald_index_v399"], esp["not_sealed_formais"])
assert esp["h8_entradas"] == len(esp["h8_residuais_do_nos"]) + CM["formal_files_n"] and sum(esp["n_bandeiras_por_grupo"].values()) == esp["n_bandeiras_novas"], "os ESPERADOS novos nao fecham"
assert esp["kernel"]["modulos_novos"] == len(esp["pedras_sha256"]) == len(nov) == 0, "a v400 nao acrescenta modulo: o numero de modulos novos != a lista (vazia)"
assert esp["vereditos_novos_v400"]["selo_pela_propria_tecnologia_v399"].startswith("TGL_SELO_PELA_PROPRIA_TECNOLOGIA_V399__SECOND_WITNESS_BESIDE_SHA256") and esp["vereditos_novos_v400"]["declaracao_do_operador_v399"].startswith("TGL_OPERATOR_DECLARATION_OF_24OCT_REGISTERED__")
assert esp["selo_acom"]["perfil"] == "ACOM-INT-C96-Q8" and esp["selo_acom"]["controles"] == [13, True] and esp["selo_acom"]["all_verified"] is True and esp["declaracao"]["all_verified"] is True and esp["declaracao"]["verbatim_sha256"] == RG.DECL_SHA256
assert {"selo_pela_propria_tecnologia_v399", "um_version"} <= set(esp["selo_difere_do_v399_no_ensaio"]) <= {"selo_pela_propria_tecnologia_v399", "um_version", "sha256", "estatuto_da_prova_v391", "three_stress_tests_v387"} and ens["selo"].get("difere_e_nao_e_so_o_esperado") == [], (esp["selo_difere_do_v399_no_ensaio"], ens["selo"].get("difere_e_nao_e_so_o_esperado"))   # estatuto_da_prova_v391 (so' o hash proprio do um.py) e three_stress_tests_v387 (so' as contagens do core no instante) sao EXPLICADOS chave por chave pelo ensaio; o resto do selo e' o da v399
assert not ({"teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398"} & set(esp["selo_difere_do_v399_no_ensaio"])), "o selo de uma versao anterior mudou: o quadro e os registros anteriores NAO se mexem"
assert esp["veracidade"]["z_disc_abaixo_de_5"] and esp["veracidade"]["poder_previo_acima_de_5"]
assert ens["quadro"]["ok"] is True
out = os.path.join(HERE, "ESPERADOS_v400.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v400:", esp["candidato_sha16"], "| vereditos v399 pinados:", len(esp["vereditos_v399"]), "| flags True v399:", len(esp["flags_true_v399"]), "| troca dita:", troca)
