# -*- coding: utf-8 -*-
"""gerar_esperados_v403.py -- ESPERADOS_v403.json LIDOS dos artefatos (molde: gerar_esperados_v402.py FINAL, com as licoes da v399 a v402): o estado SELADO da v402 pinado. A TROCA DITA: (i) os registros da v402 cujo veredito carrega os numeros do kernel (escada, declaracoes, arquivos varridos)
-- achados por script no ensaio (recomputados; so' numeros mudam) -- e (ii) o estatuto da prova (v391), cujo veredito carrega o hash do PROPRIO um.py (a certificacao pelo proprio hash). Todos os outros vereditos da v402 ficam IGUAIS, os da v402 inclusive (ponte_da_escala_dual_v402, queda_sem_geometria_v402,
esperanca_condicional_v402, cunhagens_v402 e kh_n1_cobertura_v402 sao RECRIADOS e iguais ao selado). +6 chaves novas no core (caminho_v403, vida_v403, verdade_adendo_v403, bandeiras_do_gate_v403, cunhagens_v403, kh_n1_cobertura_v403) e +5 chaves no selo (os quatro resumos e registros_v403); o selo pela propria
tecnologia (v399) muda so' nos hashes do novo um.py. O pilar pela mesma chave. O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo: os numeros dele vem do resultado pinado (v397\\insumos\\fase9) e o conferidor os confere de novo.
F8.1: o qg_closure da v403 e' o da v402 SALVO a lista de checks (que ganha UMA sonda, ProbeBlindNullAbsent, a setima): o ESPERADOS pina o hash do qg_closure da v402 sem a lista, a propria lista de seis checks e a letra do veredito (a letra do gate NAO muda).
Nada digitado: cada numero e hash vem de CANDIDATO_v403.json, ensaio_a_seco_v403.json, do core/selo da v402 (base_v402), de kernel\\FLAGS_v403.json, de ESPERADOS_v402.json (o que o quadro pinou) e do resultado pinado. Escrito a mao para a v403 (as chaves herdadas guardam os nomes da v402:
`vereditos_v402`, `flags_true_v402`... sao o estado da BASE). As erratas E5 e E6 e as decisoes D17 a D22 da gerencia vao nos registros (cunhagens_v403); aqui so' se pinam os vereditos, os valores, as estrelas e os contratos.
ORDEM DE USO: depende do ensaio (ensaio_a_seco_v403.json com veredito TUDO PASSOU e o sha16 do candidato): sem ele este script PARA no primeiro assert (fail-closed)."""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v403 as DL  # noqa: E402
import quadro_v397 as QV  # noqa: E402
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
J = lambda x: json.dumps(x, sort_keys=True, default=str)
BASE = os.path.join(HERE, DL.BASE_DIR)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v403.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, DL.CANDIDATO))
assert h16(os.path.join(BASE, "um.py")) == CM["base_v402_sha16"] == DL.BASE_SHA16_DA_ORDEM, "a base nao e' a v402 selada que a ordem deu"
_ens_p = os.path.join(HERE, "ensaio_a_seco_v403.json")
assert os.path.exists(_ens_p), "falta ensaio_a_seco_v403.json: o ensaio a seco (ato da gerencia) tem de rodar ANTES deste script -- nao gero ESPERADOS sem ele"
ens = json.load(open(_ens_p, encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"], (ens.get("veredito"), ens.get("sha16"))
R0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(BASE, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == DL.BASE_VERSION
E402 = json.load(open(os.path.join(DL.V402, "ESPERADOS_v402.json"), encoding="utf-8")); assert E402["candidato_sha16"] == CM["base_v402_sha16"]
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]; axr0 = kf["axiom_report"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
mud = ens["vizinhos"]["mudaram"]; te_ = ens["vizinhos"]["troca_esperada_so_o_hash_proprio"]
troca = sorted(set(mud) | set(te_))   # os vereditos da v402 que mudam: os que carregam os numeros do kernel (so' numeros) e o estatuto da prova (so' o hash proprio do um.py), recomputados pelo ensaio
assert troca, "a troca dita nao pode ser vazia (a escada mudou)"
assert set(te_) <= {"estatuto_da_prova_v391"}, te_
F = json.load(open(os.path.join(HERE, "FORMAL_MAP_v403.json"), encoding="utf-8"))
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v403.json"), encoding="utf-8"))["novos"]
pins = {p: F[p] for p in nov}
FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v403.json"), encoding="utf-8")); assert FJ["n_flags"] == CM["n_bandeiras"]
V402 = {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}
mf = ens["mainflow"]
SEL_KEYS = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "registros_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "registros_v394", "psibit_v395", "registros_v395", "testemunha_estatica_v396", "registros_v396",
            "teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "estatuto_da_prova_v391", "fundacao_v390", "text_label_errata_v389", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388",
            "declaracao_do_operador_v399", "registros_v399", "falsidade_da_inercia_v401", "registros_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402")
assert all(k in selo0 for k in SEL_KEYS), [k for k in SEL_KEYS if k not in selo0]
vr = ens["veracidade_registro"]
RESP = os.path.join(DL.F9_DIR_DURAVEL, DL.F9_RESULTADO_NOME)
res9 = json.load(open(RESP, encoding="utf-8"))
numeros9 = {k: DL.lido(res9, c) for k, c in DL.F9_CAMINHOS.items()}
assert all(vr["lido"].get(k) == v for k, v in numeros9.items()), "os numeros lidos pelo registro no ensaio != os do resultado pinado"
assert E402["veracidade"]["numeros_do_resultado"] == numeros9 and E402["veracidade"]["resultado"]["sha256"] == DL.F9_RESULTADO_SHA256_DA_ORDEM, "o que a v402 pinou do Teste da Unica Palavra != o resultado em disco"
a_pt, mach_pt = QV.esperados(res9, "pt"); a_en, mach_en = QV.esperados(res9, "en")
assert mach_pt == E402["quadro"]["linha_de_maquina_pt"] and mach_en == E402["quadro"]["linha_de_maquina_en"], "a linha de maquina do quadro mudou: o quadro NAO se mexe"
TW403 = "Caminho, Verdade e Vida"; TW403E = "Way, Truth and Life"
MARCAS403_PT = [TW403, "O Caminho.", "A Vida.", "A Verdade, como adendo.", "As bandeiras do gate.", "Erratas ao lado (v403)."]
MARCAS403_EN = [TW403E, "The Way.", "The Life.", "The Truth, as an addendum.", "The gate flags.", "Errata beside (v403)."]
MARCAS402_PT = list(E402["artigo_marcas"]["pt"]); MARCAS402_EN = list(E402["artigo_marcas"]["en"])
sa, dc, sc = ens["selo_acom_registro"], ens["declaracao_registro"], ens["sidecar"]
MF3 = mf["registros_novos_v403"]; R403 = ens["v403_registros"]
assert sorted(MF3) == sorted(list(DL.REGISTROS_FUNCAO) + [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]), sorted(MF3)
qg0 = core0.get("qg_closure") or {}
assert len(qg0.get("checks") or []) == 6 and (qg0.get("gate") or {}).get("verdict") == selo0.get("qg_closure_verdict"), "o gate da base (v402 selada) nao tem o formato esperado: seis checks e a letra do veredito == a do selo"
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v402_sha16"], "escada": [CM["escada"][1], CM["escada"][1]], "escada_v402_e_v403": CM["escada"], "n_bandeiras_novas": CM["n_bandeiras"],
       "bandeiras_novas_chaves": [f[0] for f in FJ["flags"]], "bandeiras_novas_nomes": [f[1] for f in FJ["flags"]],
       "cunhagens": CM["cunhagens"], "kernel": CM["kernel"], "pedras_sha256": pins, "formal_files_n": CM["formal_files_n"],
       "pedras_v402_sha256": {s["rel"]: kf["formal_files_sha256"][s["rel"]] for s in DL.D2.STONES},   # as tres pedras SELADAS da v402 (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional): ficam no kernel como registro, com o sha do core selado
       "qg_closure_verdict": selo0.get("qg_closure_verdict"),
       "qg_closure_v402_json_sha256": hashlib.sha256(J(qg0).encode("utf-8")).hexdigest(),
       "qg_closure_v402_sem_checks_json_sha256": hashlib.sha256(J({k: v for k, v in qg0.items() if k != "checks"}).encode("utf-8")).hexdigest(),
       "qg_closure_v402_checks": json.loads(J(qg0.get("checks"))),
       "qg_closure_gate_verdict_v402": (qg0.get("gate") or {}).get("verdict"),
       "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v402": V402, "troca_dita": troca, "veredito_da_troca_no_ensaio": {k: (mud.get(k) or te_.get(k))["depois"] for k in troca},
       "regra_da_mudanca_dita": "so' os vereditos de `troca_dita` podem mudar (carregam a escada, as declaracoes ou a contagem de arquivos do kernel; so' numeros); qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v402": {k: selo0.get(k) for k in SEL_KEYS},
       "selo_difere_do_v402_no_ensaio": ens["selo"]["difere_do_selo_v402"],
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v402": sorted(k for k, v in kf.items() if v is True), "axiom_report_v402_n": len(axr0),
       "runtime_seals_v402": core0["runtime_of_the_one"]["seals"], "what_remains_v402": core0["tgl_closure"]["what_remains_named"],
       "vereditos_novos_v403": {k: v["verdict"] for k, v in MF3.items()},
       "registros_v403": {k: v["verdict"] for k, v in MF3.items() if k in (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO)},
       "registros_v402": {k: V(k) for k in ("cunhagens_v402", "kh_n1_cobertura_v402")}, "registros_v401": {k: V(k) for k in ("cunhagens_v401", "kh_n1_cobertura_v401")}, "veredito_da_falsidade_v402": V("falsidade_da_inercia_v401"),
       "registros_funcao_v403": {**{s["key"]: {"nome": DL.REGISTRO_DE_PEDRA[s["key"]], "verdict": R403[s["key"]]["verdict"], "values": R403[s["key"]]["values"], "n_checks": R403[s["key"]]["n_checks"]} for s in DL.STONES},
                                 "gate": {"nome": DL.REGISTRO_BANDEIRAS, "verdict": R403["gate"]["verdict"], "values": R403["gate"]["values"], "n_checks": R403["gate"]["n_checks"]}},
       "estrelas_v403": {s["key"]: {"teorema": s["key_theorem"], "bandeira": FJ["bandeiras_do_contrato"][s["key"]][s["key_theorem"]]} for s in DL.STONES},
       "registros_v399": {k: v["verdict"] for k, v in mf["registros_v399"].items()},
       "cobertura_kh_n1": ens["verify_kernel_ponta_a_ponta"]["cobertura"], "axiom_report_esperado_min": ens["verify_kernel_ponta_a_ponta"]["axiom_report_n"],
       "selo_acom": {"verdict": sa["verdict"], "all_verified": sa["all_verified"], "perfil": sa["perfil"], "bloco_embutido_sha256": sa["bloco_embutido_sha256"], "sha256_do_um_py": sa["sha256_do_um_py"], "bytes": sa["bytes"], "psi": sa["psi"], "theta": sa["theta"], "kappa": sa["kappa"],
                     "lut_sha256": sa["lut_sha256"], "m_max_abs": sa["m_max_abs"], "f_exp": sa["f_exp"], "entropia_dos_estados_bits": sa["entropia_dos_estados_bits"], "erro_real_maximo_antes_do_rint": sa["erro_real_maximo_antes_do_rint"],
                     "controles": [len(sa["controles"]), all(o_.startswith("RECUSOU:") for _, o_ in sa["controles"])], "controles_obtidos": {i_: o_ for i_, o_ in sa["controles"]}, "n_checks": len(sa["checks"]), "checks": sa["checks"], "auditoria_de_separacao": sa["auditoria_de_separacao"], "tempo_total_s_no_ensaio": sa["tempo_total_s"]},
       "declaracao": {"verdict": dc["verdict"], "all_verified": dc["all_verified"], "verbatim_sha256": dc["verbatim_sha256"], "sha16": dc["verbatim_sha256"][:16], "n_checks": len(dc["checks"]), "checks": dc["checks"], "ancoras": dc["ancoras"], "pedra": dc["pedra"], "linhas_da_trava": dc["linhas_da_trava"],
                      "direcao_do_testemunho": {"o_operador": "testifica DA IALD", "o_um_py": "testifica EM HASH", "a_IALD": "NAO testifica do operador", "o_Pai_de_Jo_8_18": "le-se no absoluto, o Um"}},
       "sidecar": {"arquivo": DL.SIDECAR_NOME, "esquema": "um_absoluto_selo_acom/v1 (v399)", "objetos": [o["nome"] for o in sc["objetos"]], "veredito_esperado_prefixo": "TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED", "um_py": next(o for o in sc["objetos"] if o["nome"] == "um.py"),
                   "tempo_s_no_ensaio": sc["tempo_s"], "entra_na_custodia": "D5 (proposta da gerencia): o sidecar e' arquivo novo da custodia; o handoff o lista"},
       "acom_estudo": E402["acom_estudo"],   # a secao do selo pela propria tecnologia NAO muda na v403: o que a v402 pinou (runtime da v400, bloco embutido, fontes do operador)
       "decisoes_da_gerencia": dict(DL.DECISOES), "erratas_E5_e_E6": list(DL.ERRATAS_V403), "leitura_tripla_27out": dict(DL.LEITURA_TRIPLA_27OUT),
       "veracidade": E402["veracidade"], "quadro": E402["quadro"],   # o QUADRO do topo (v397) e o registro do Teste da Unica Palavra: o que a v397/v402 pinou, conferido de novo contra o resultado em disco
       "artigo_marcas": {"pt": MARCAS403_PT + MARCAS402_PT, "en": MARCAS403_EN + MARCAS402_EN},
       "artigo_nao": {"pt": list(E402["artigo_nao"]["pt"]) + ["Nesta rodada os registros da v403 NÃO selaram todos"], "en": list(E402["artigo_nao"]["en"]) + ["This round the v403 records did NOT all seal"]},
       "toc": {"pt": [TW403] + [w for w in E402["toc"]["pt"] if not w.startswith("v384 a ")] + ["v384 a " + DL.UM_VERSION], "en": [TW403E] + [w for w in E402["toc"]["en"] if not w.startswith("v384 to ")] + ["v384 to " + DL.UM_VERSION]},   # o titulo da introducao diz `v384 a <versao desta rodada>`
       "the_iald_index_v402": {"all_verified": (core0.get("the_iald_index") or {}).get("all_verified"), "verdict": V("the_iald_index")}, "the_iald_index_v403": {"verdict": ens["indice_da_iald"]["verdict"]},
       "md_carimbo": "**Versão v403**", "md_caminho": "Caminho, Verdade e Vida (v403, 27/10/2026)", "md_ponte": "A ponte da escala dual, a queda sem geometria e a esperança condicional (v402, 26/10/2026)", "md_falsidade": "A falsidade (simulacro) da inércia (v401, 25/10/2026)", "md_errata": "Errata ao lado (v400, 24/10/2026)",
       "md_testemunho": "O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026)", "md_sonico": "Sônico e a afinação das cordas (v398, 23/10/2026)", "md_token": "O Teste da Única Palavra e a pedra Token (v397, 23/10/2026)",
       "md_testemunha": "A testemunha estática (v396, 22/10/2026)", "md_psibit": "O modo psiônico na fractalização do Um (v395, 21/10/2026)",
       "ensaio_sha16": h16(_ens_p),
       "h8_entradas": CM["h8"]["entradas"], "h8_residuais_do_nos": CM["h8"]["residuais_do_nos"], "formal_files_n_no_rito": CM["h8"]["entradas"],
       "n_bandeiras_por_grupo": dict(FJ["por_grupo_bandeiras"]), "politica_de_bandeiras": CM["politica_de_bandeiras"], "pedras": CM["kernel"]["pedras"], "teoremas_das_pedras": {s["key"]: s["theorem"] for s in DL.STONES},
       "bandeiras_das_pedras": CM["politica_de_bandeiras"]["bandeiras_do_teorema"], "suporte_das_pedras": {s["key"]: dict(s["support"]) for s in DL.STONES},
       "contrato_das_pedras": {s["key"]: list(s["contract"]) for s in DL.STONES}, "candidato_anterior_sha16": CM["base_v402_sha16"],
       "f81": {"literais_na_base": CM["f81"]["literais_na_base"], "literais_no_candidato": CM["f81"]["literais_no_candidato"], "gate_recomputado_no_ensaio": ens.get("gate_recomputado")}}
assert esp["the_iald_index_v402"]["all_verified"] is True and esp["not_sealed_formais"] == [], (esp["the_iald_index_v402"], esp["not_sealed_formais"])
assert esp["h8_entradas"] == len(esp["h8_residuais_do_nos"]) + CM["formal_files_n"] and sum(esp["n_bandeiras_por_grupo"].values()) == esp["n_bandeiras_novas"], "os ESPERADOS novos nao fecham"
assert esp["kernel"]["modulos_novos"] == len(esp["pedras_sha256"]) == len(nov) == 3, "o numero de modulos novos != a lista"
assert len(esp["pedras_v402_sha256"]) == 3 and all(len(h_) == 64 for h_ in esp["pedras_v402_sha256"].values()), esp["pedras_v402_sha256"]
_vn = esp["vereditos_novos_v403"]
assert _vn["caminho_v403"].startswith("TGL_CAMINHO_V403__THE_DUAL_SCALING_BRIDGE") and _vn["vida_v403"].startswith("TGL_VIDA_V403__THE_FALL_WITHOUT_GEOMETRY") and _vn["verdade_adendo_v403"].startswith("TGL_VERDADE_ADENDO_V403__THE_CONDITIONAL_EXPECTATION"), _vn
assert _vn["bandeiras_do_gate_v403"].startswith("TGL_BANDEIRAS_DO_GATE_V403__ALL_18_FLAGS_ARE_COMPUTED") and _vn["cunhagens_v403"].startswith("TGL_CUNHAGENS_V403__") and _vn["kh_n1_cobertura_v403"].startswith("TGL_KH_N1_COBERTURA_V403__"), _vn
assert sorted(esp["registros_v403"]) == ["cunhagens_v403", "kh_n1_cobertura_v403"] and sorted(esp["registros_v402"]) == ["cunhagens_v402", "kh_n1_cobertura_v402"] and sorted(esp["registros_v401"]) == ["cunhagens_v401", "kh_n1_cobertura_v401"]
_rf = esp["registros_funcao_v403"]
assert _rf["caminho"]["values"]["same_pplus"] == 2.0 and _rf["caminho"]["values"]["lifts_same_pplus_masses"] == [1.0, 4.0, 9.0] and _rf["vida"]["values"]["finite_model_group_order"] == 12 and 0.0 < _rf["verdade_adendo"]["values"]["alpha_squared"] < _rf["verdade_adendo"]["values"]["beta"], _rf
assert [_rf[k]["n_checks"] for k in ("caminho", "vida", "verdade_adendo", "gate")] == [DL.N_CHECKS[k] for k in ("caminho", "vida", "verdade_adendo", "gate")], [(k, _rf[k]["n_checks"]) for k in _rf]
_gv = _rf["gate"]["values"]
assert _gv["n_flags"] == 18 == _gv["n_true"] == _gv["n_calculated"] and _gv["n_literal"] == 0 and _gv["n_read_by_the_verdict"] == 15 and _gv["read_by_the_verdict"] == [6, 5, 4] and _gv["gate_verdict_equals_v402"] is True and _gv["n_gate_checks"] == 7 and _gv["gate_verdict"] == esp["qg_closure_gate_verdict_v402"], _gv
assert esp["f81"]["literais_no_candidato"] == [] and sorted(esp["f81"]["literais_na_base"]) == sorted(DL.F81_LITERAIS), esp["f81"]
assert len(esp["qg_closure_v402_checks"]) == 6 and all(c_[1] is True for c_ in esp["qg_closure_v402_checks"]), esp["qg_closure_v402_checks"]
assert esp["selo_acom"]["perfil"] == "ACOM-INT-C96-Q8" and esp["selo_acom"]["controles"] == [13, True] and esp["selo_acom"]["all_verified"] is True and esp["declaracao"]["all_verified"] is True and esp["declaracao"]["verbatim_sha256"] == DL.sha256(open(DL.VERBATIM_ORIGEM[DL.DECLARACAO_IDX], "rb").read())
# o selo da v403 difere do da v402 SELADA em: o selo ACOM (hashes do novo um.py), a versao, o sha256, as chaves novas (os quatro resumos e registros_v403), e as chaves que carregam os numeros do kernel ou o hash proprio (a troca dita); o ensaio EXPLICA chave por chave
assert {"selo_pela_propria_tecnologia_v399", "um_version", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "registros_v403"} <= set(esp["selo_difere_do_v402_no_ensaio"]) and ens["selo"].get("difere_e_nao_e_so_o_esperado") == [], (esp["selo_difere_do_v402_no_ensaio"], ens["selo"].get("difere_e_nao_e_so_o_esperado"))
assert not ({"teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "declaracao_do_operador_v399", "registros_v399", "falsidade_da_inercia_v401", "registros_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402"} & set(esp["selo_difere_do_v402_no_ensaio"])), "o selo de uma versao anterior mudou: o quadro e os registros anteriores NAO se mexem"
assert esp["veracidade"]["z_disc_abaixo_de_5"] and esp["veracidade"]["poder_previo_acima_de_5"]
assert ens["quadro"]["ok"] is True
out = os.path.join(HERE, "ESPERADOS_v403.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v403:", esp["candidato_sha16"], "| vereditos v402 pinados:", len(esp["vereditos_v402"]), "| flags True v402:", len(esp["flags_true_v402"]), "| troca dita:", troca)
