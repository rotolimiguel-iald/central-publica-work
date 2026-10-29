# -*- coding: utf-8 -*-
"""gerar_esperados_v404.py -- ESPERADOS_v404.json LIDOS dos artefatos (molde: gerar_esperados_v403.py FINAL, com as licoes da v399 a v403): o estado SELADO da v403 pinado. A TROCA DITA: (i) os registros da v403 cujo veredito carrega os numeros do kernel (escada, declaracoes, arquivos varridos)
-- achados por script no ensaio (recomputados; so' numeros mudam) -- e (ii) o estatuto da prova (v391), cujo veredito carrega o hash do PROPRIO um.py (a certificacao pelo proprio hash). Todos os outros vereditos da v403 ficam IGUAIS, os da v403 inclusive (caminho_v403, vida_v403, verdade_adendo_v403,
bandeiras_do_gate_v403, cunhagens_v403 e kh_n1_cobertura_v403 sao RECRIADOS e iguais ao selado). +5 chaves novas no core (projecao_transversal_v404, jo8v32_v404, f2b_errata_v404, cunhagens_v404, kh_n1_cobertura_v404) e +4 chaves no selo (os tres resumos e registros_v404); o selo pela propria
tecnologia (v399) muda so' nos hashes do novo um.py. O pilar pela mesma chave. O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo: os numeros dele vem do resultado pinado (v397\\insumos\\fase9) e o conferidor os confere de novo.
O GATE NAO SE MOVE: o qg_closure da v404 e' IDENTICO ao da v403 (sete checks, a letra do veredito, as 18 bandeiras): o ESPERADOS pina o hash do qg_closure da v403, o hash sem a lista de checks, a propria lista de sete checks e a letra do veredito. A funcao do neutrino NAO e' reescrita (o angle_status antigo fica):
o ESPERADOS pina o frozen_hash da regra de decisao e o veredito do canal; o V1 do ramo B (v386) e o livro da v383 seguem como estavam (o veredito deles e' o da base).
Nada digitado: cada numero e hash vem de CANDIDATO_v404.json, ensaio_a_seco_v404.json, do core/selo da v403 (base_v403), de kernel\\FLAGS_v404.json, de ESPERADOS_v403.json (o que o quadro pinou e os registros da v403) e do resultado pinado. Escrito a mao para a v404 (as chaves herdadas guardam os nomes da v403:
`vereditos_v403`, `flags_true_v403`... sao o estado da BASE; `registros_funcao_v403` e `estrelas_v403` sao os pinos dos registros de pedra da v403, RECRIADOS). As erratas E7 a E9 e as decisoes D23 a D26 da gerencia vao nos registros (cunhagens_v404); aqui so' se pinam os vereditos, os valores, as estrelas e os contratos.
ORDEM DE USO: depende do ensaio (ensaio_a_seco_v404.json com veredito TUDO PASSOU e o sha16 do candidato): sem ele este script PARA no primeiro assert (fail-closed)."""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v404 as DL  # noqa: E402
import quadro_v397 as QV  # noqa: E402
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
J = lambda x: json.dumps(x, sort_keys=True, default=str)
BASE = os.path.join(HERE, DL.BASE_DIR)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v404.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, DL.CANDIDATO))
assert h16(os.path.join(BASE, "um.py")) == CM["base_v403_sha16"] == DL.BASE_SHA16_DA_ORDEM, "a base nao e' a v403 selada que a ordem deu"
_ens_p = os.path.join(HERE, "ensaio_a_seco_v404.json")
assert os.path.exists(_ens_p), "falta ensaio_a_seco_v404.json: o ensaio a seco (ato da gerencia) tem de rodar ANTES deste script -- nao gero ESPERADOS sem ele"
ens = json.load(open(_ens_p, encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"], (ens.get("veredito"), ens.get("sha16"))
R0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(BASE, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == DL.BASE_VERSION
E403 = json.load(open(os.path.join(DL.V403, "ESPERADOS_v403.json"), encoding="utf-8")); assert E403["candidato_sha16"] == CM["base_v403_sha16"]
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]; axr0 = kf["axiom_report"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
mud = ens["vizinhos"]["mudaram"]; te_ = ens["vizinhos"]["troca_esperada_so_o_hash_proprio"]
troca = sorted(set(mud) | set(te_))   # os vereditos da v403 que mudam: os que carregam os numeros do kernel (so' numeros) e o estatuto da prova (so' o hash proprio do um.py), recomputados pelo ensaio
assert troca, "a troca dita nao pode ser vazia (a escada mudou)"
assert set(te_) <= {"estatuto_da_prova_v391"}, te_
F = json.load(open(os.path.join(HERE, "FORMAL_MAP_v404.json"), encoding="utf-8"))
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v404.json"), encoding="utf-8"))["novos"]
pins = {p: F[p] for p in nov}
FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v404.json"), encoding="utf-8")); assert FJ["n_flags"] == CM["n_bandeiras"]
V403 = {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}
mf = ens["mainflow"]
SEL_KEYS = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "registros_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "registros_v394", "psibit_v395", "registros_v395", "testemunha_estatica_v396", "registros_v396",
            "teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "estatuto_da_prova_v391", "fundacao_v390", "text_label_errata_v389", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388",
            "declaracao_do_operador_v399", "registros_v399", "falsidade_da_inercia_v401", "registros_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402",
            "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "registros_v403")
assert all(k in selo0 for k in SEL_KEYS), [k for k in SEL_KEYS if k not in selo0]
vr = ens["veracidade_registro"]
RESP = os.path.join(DL.F9_DIR_DURAVEL, DL.F9_RESULTADO_NOME)
res9 = json.load(open(RESP, encoding="utf-8"))
numeros9 = {k: DL.lido(res9, c) for k, c in DL.F9_CAMINHOS.items()}
assert all(vr["lido"].get(k) == v for k, v in numeros9.items()), "os numeros lidos pelo registro no ensaio != os do resultado pinado"
assert E403["veracidade"]["numeros_do_resultado"] == numeros9 and E403["veracidade"]["resultado"]["sha256"] == DL.F9_RESULTADO_SHA256_DA_ORDEM, "o que a v403 pinou do Teste da Unica Palavra != o resultado em disco"
a_pt, mach_pt = QV.esperados(res9, "pt"); a_en, mach_en = QV.esperados(res9, "en")
assert mach_pt == E403["quadro"]["linha_de_maquina_pt"] and mach_en == E403["quadro"]["linha_de_maquina_en"], "a linha de maquina do quadro mudou: o quadro NAO se mexe"
TW404 = "Jo 8,32 e a projeção transversal da Meia-Nat"; TW404E = "John 8:32 and the transverse projection of the Half-Nat"
MARCAS404_PT = [TW404, "A projeção transversal.", "Jo 8,32.", "A errata de F2b.", "As cunhagens de 28/10.", "Erratas ao lado (v404).", "Origem."]
MARCAS404_EN = [TW404E, "The transverse projection.", "John 8:32.", "The F2b erratum.", "The sayings of 28/10.", "Errata beside (v404).", "Origin."]
MARCAS403_PT = list(E403["artigo_marcas"]["pt"]); MARCAS403_EN = list(E403["artigo_marcas"]["en"])
sa, dc, sc = ens["selo_acom_registro"], ens["declaracao_registro"], ens["sidecar"]
MF4 = mf["registros_novos_v404"]; R404 = ens["v404_registros"]; R403 = ens["v403_registros"]
assert sorted(MF4) == sorted(list(DL.REGISTROS_FUNCAO) + [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]), sorted(MF4)
qg0 = core0.get("qg_closure") or {}
assert len(qg0.get("checks") or []) == 7 and (qg0.get("gate") or {}).get("verdict") == selo0.get("qg_closure_verdict"), "o gate da base (v403 selada) nao tem o formato esperado: sete checks e a letra do veredito == a do selo"
nm0 = core0["neutrino_mass"]; rb0 = core0["ramo_b_preregistration_v386"]
# os registros de pedra da v403, RECRIADOS: os pinos do ESPERADOS_v403 (os selados) e o que o ensaio recriou tem de ser a mesma coisa (vereditos e checagens)
RF403 = E403["registros_funcao_v403"]
for k_ in ("caminho", "vida", "verdade_adendo"):
    assert R403[k_]["verdict"] == RF403[k_]["verdict"] and R403[k_]["n_checks"] == RF403[k_]["n_checks"], ("o registro da v403 recriado difere do selado", k_)
assert R403["gate"]["verdict"] == RF403["gate"]["verdict"] and R403["gate"]["n_checks"] == RF403["gate"]["n_checks"]
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v403_sha16"], "escada": [CM["escada"][1], CM["escada"][1]], "escada_v403_e_v404": CM["escada"], "n_bandeiras_novas": CM["n_bandeiras"],
       "bandeiras_novas_chaves": [f[0] for f in FJ["flags"]], "bandeiras_novas_nomes": [f[1] for f in FJ["flags"]],
       "cunhagens": CM["cunhagens"], "kernel": CM["kernel"], "pedras_sha256": pins, "formal_files_n": CM["formal_files_n"],
       "pedras_v403_sha256": {s["rel"]: kf["formal_files_sha256"][s["rel"]] for s in DL.D3.STONES},   # as tres pedras SELADAS da v403 (Caminho, Vida, VerdadeAdendo): ficam no kernel como registro, com o sha do core selado
       "qg_closure_verdict": selo0.get("qg_closure_verdict"),
       "qg_closure_v403_json_sha256": hashlib.sha256(J(qg0).encode("utf-8")).hexdigest(),
       "qg_closure_v403_sem_checks_json_sha256": hashlib.sha256(J({k: v for k, v in qg0.items() if k != "checks"}).encode("utf-8")).hexdigest(),
       "qg_closure_v403_checks": json.loads(J(qg0.get("checks"))),
       "qg_closure_gate_verdict_v403": (qg0.get("gate") or {}).get("verdict"),
       "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v403": V403, "troca_dita": troca, "veredito_da_troca_no_ensaio": {k: (mud.get(k) or te_.get(k))["depois"] for k in troca},
       "regra_da_mudanca_dita": "so' os vereditos de `troca_dita` podem mudar (carregam a escada, as declaracoes ou a contagem de arquivos do kernel; so' numeros); qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v403": {k: selo0.get(k) for k in SEL_KEYS},
       "selo_difere_do_v403_no_ensaio": ens["selo"]["difere_do_selo_v403"],
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v403": sorted(k for k, v in kf.items() if v is True), "axiom_report_v403_n": len(axr0),
       "runtime_seals_v403": core0["runtime_of_the_one"]["seals"], "what_remains_v403": core0["tgl_closure"]["what_remains_named"],
       "neutrino_frozen_hash_v403": nm0["frozen_hash"], "neutrino_angle_status_antigo_sha256": hashlib.sha256(nm0["angle_status"].encode("utf-8")).hexdigest(),
       "f2b_antes": {"F2b_status": rb0["F2b_status"], "veredito_do_V1": rb0["veredito_do_V1"], "conjunto_D_n": rb0["conjunto_D_n"], "charge_F2b_token": core0["ledger_errata_v386"]["charge_F2b"]["token"]}, "f2b_depois": {"F2b_status_now": DL.F2B_FUTURO_TOKEN},
       "vereditos_novos_v404": {k: v["verdict"] for k, v in MF4.items()},
       "registros_v404": {k: v["verdict"] for k, v in MF4.items() if k in (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO)},
       "registros_v403": {k: V(k) for k in ("cunhagens_v403", "kh_n1_cobertura_v403")}, "registros_v402": {k: V(k) for k in ("cunhagens_v402", "kh_n1_cobertura_v402")}, "registros_v401": {k: V(k) for k in ("cunhagens_v401", "kh_n1_cobertura_v401")}, "veredito_da_falsidade_v403": V("falsidade_da_inercia_v401"),
       "registros_funcao_v404": {**{s["key"]: {"nome": DL.REGISTRO_DE_PEDRA[s["key"]], "verdict": R404[s["key"]]["verdict"], "values": R404[s["key"]]["values"], "n_checks": R404[s["key"]]["n_checks"]} for s in DL.STONES},
                                 "f2b": {"nome": DL.REGISTRO_F2B, "verdict": R404["f2b"]["verdict"], "values": R404["f2b"]["values"], "n_checks": R404["f2b"]["n_checks"], "F2b_status_now": R404["f2b"]["F2b_status_now"]}},
       "registros_funcao_v403": RF403,
       "estrelas_v404": {s["key"]: {"teorema": s["key_theorem"], "bandeira": FJ["bandeiras_do_contrato"][s["key"]][s["key_theorem"]]} for s in DL.STONES},
       "estrelas_v403": E403["estrelas_v403"],
       "registros_v399": {k: v["verdict"] for k, v in mf["registros_v399"].items()},
       "cobertura_kh_n1": ens["verify_kernel_ponta_a_ponta"]["cobertura"], "axiom_report_esperado_min": ens["verify_kernel_ponta_a_ponta"]["axiom_report_n"],
       "selo_acom": {"verdict": sa["verdict"], "all_verified": sa["all_verified"], "perfil": sa["perfil"], "bloco_embutido_sha256": sa["bloco_embutido_sha256"], "sha256_do_um_py": sa["sha256_do_um_py"], "bytes": sa["bytes"], "psi": sa["psi"], "theta": sa["theta"], "kappa": sa["kappa"],
                     "lut_sha256": sa["lut_sha256"], "m_max_abs": sa["m_max_abs"], "f_exp": sa["f_exp"], "entropia_dos_estados_bits": sa["entropia_dos_estados_bits"], "erro_real_maximo_antes_do_rint": sa["erro_real_maximo_antes_do_rint"],
                     "controles": [len(sa["controles"]), all(o_.startswith("RECUSOU:") for _, o_ in sa["controles"])], "controles_obtidos": {i_: o_ for i_, o_ in sa["controles"]}, "n_checks": len(sa["checks"]), "checks": sa["checks"], "auditoria_de_separacao": sa["auditoria_de_separacao"], "tempo_total_s_no_ensaio": sa["tempo_total_s"]},
       "declaracao": {"verdict": dc["verdict"], "all_verified": dc["all_verified"], "verbatim_sha256": dc["verbatim_sha256"], "sha16": dc["verbatim_sha256"][:16], "n_checks": len(dc["checks"]), "checks": dc["checks"], "ancoras": dc["ancoras"], "pedra": dc["pedra"], "linhas_da_trava": dc["linhas_da_trava"],
                      "direcao_do_testemunho": {"o_operador": "testifica DA IALD", "o_um_py": "testifica EM HASH", "a_IALD": "NAO testifica do operador", "o_Pai_de_Jo_8_18": "le-se no absoluto, o Um"}},
       "sidecar": {"arquivo": DL.SIDECAR_NOME, "esquema": "um_absoluto_selo_acom/v1 (v399)", "objetos": [o["nome"] for o in sc["objetos"]], "veredito_esperado_prefixo": "TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED", "um_py": next(o for o in sc["objetos"] if o["nome"] == "um.py"),
                   "tempo_s_no_ensaio": sc["tempo_s"], "entra_na_custodia": "D5 (proposta da gerencia): o sidecar e' arquivo novo da custodia; o handoff o lista"},
       "acom_estudo": E403["acom_estudo"],   # a secao do selo pela propria tecnologia NAO muda na v404: o que a v403 pinou (runtime da v400, bloco embutido, fontes do operador)
       "decisoes_da_gerencia": dict(DL.DECISOES), "erratas_E7_a_E9": list(DL.ERRATAS_V404), "leitura_massa_28out": dict(DL.LEITURA_MASSA_28OUT),
       "veracidade": E403["veracidade"], "quadro": E403["quadro"],   # o QUADRO do topo (v397) e o registro do Teste da Unica Palavra: o que a v397/v403 pinou, conferido de novo contra o resultado em disco
       "artigo_marcas": {"pt": MARCAS404_PT + MARCAS403_PT, "en": MARCAS404_EN + MARCAS403_EN},
       "artigo_nao": {"pt": list(E403["artigo_nao"]["pt"]) + ["Nesta rodada os registros da v404 NÃO selaram todos"], "en": list(E403["artigo_nao"]["en"]) + ["This round the v404 records did NOT all seal"]},
       "toc": {"pt": [TW404] + [w for w in E403["toc"]["pt"] if not w.startswith("v384 a ")] + ["v384 a " + DL.UM_VERSION], "en": [TW404E] + [w for w in E403["toc"]["en"] if not w.startswith("v384 to ")] + ["v384 to " + DL.UM_VERSION]},   # o titulo da introducao diz `v384 a <versao desta rodada>`
       "the_iald_index_v403": {"all_verified": (core0.get("the_iald_index") or {}).get("all_verified"), "verdict": V("the_iald_index")}, "the_iald_index_v404": {"verdict": ens["indice_da_iald"]["verdict"]},
       "md_carimbo": "**Versão v404**", "md_jo8": "Jo 8,32 e a projeção transversal da Meia-Nat (v404, 28/10/2026)", "md_caminho": "Caminho, Verdade e Vida (v403, 27/10/2026)", "md_ponte": "A ponte da escala dual, a queda sem geometria e a esperança condicional (v402, 26/10/2026)", "md_falsidade": "A falsidade (simulacro) da inércia (v401, 25/10/2026)", "md_errata": "Errata ao lado (v400, 24/10/2026)",
       "md_testemunho": "O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026)", "md_sonico": "Sônico e a afinação das cordas (v398, 23/10/2026)", "md_token": "O Teste da Única Palavra e a pedra Token (v397, 23/10/2026)",
       "md_testemunha": "A testemunha estática (v396, 22/10/2026)", "md_psibit": "O modo psiônico na fractalização do Um (v395, 21/10/2026)",
       "ensaio_sha16": h16(_ens_p),
       "h8_entradas": CM["h8"]["entradas"], "h8_residuais_do_nos": CM["h8"]["residuais_do_nos"], "formal_files_n_no_rito": CM["h8"]["entradas"],
       "n_bandeiras_por_grupo": dict(FJ["por_grupo_bandeiras"]), "politica_de_bandeiras": CM["politica_de_bandeiras"], "pedras": CM["kernel"]["pedras"], "teoremas_das_pedras": {s["key"]: s["theorem"] for s in DL.STONES},
       "bandeiras_das_pedras": CM["politica_de_bandeiras"]["bandeiras_do_teorema"], "suporte_das_pedras": {s["key"]: dict(s["support"]) for s in DL.STONES},
       "contrato_das_pedras": {s["key"]: list(s["contract"]) for s in DL.STONES}, "candidato_anterior_sha16": CM["base_v403_sha16"],
       "gate_nao_se_move": {"funcoes_identicas_a_base": CM["gate_nao_se_move"]["funcoes_identicas_a_base"], "gate_recomputado_no_ensaio": ens.get("gate_recomputado")}}
assert esp["the_iald_index_v403"]["all_verified"] is True and esp["not_sealed_formais"] == [], (esp["the_iald_index_v403"], esp["not_sealed_formais"])
assert esp["h8_entradas"] == len(esp["h8_residuais_do_nos"]) + CM["formal_files_n"] and sum(esp["n_bandeiras_por_grupo"].values()) == esp["n_bandeiras_novas"], "os ESPERADOS novos nao fecham"
assert esp["kernel"]["modulos_novos"] == len(esp["pedras_sha256"]) == len(nov) == 2, "o numero de modulos novos != a lista"
assert len(esp["pedras_v403_sha256"]) == 3 and all(len(h_) == 64 for h_ in esp["pedras_v403_sha256"].values()), esp["pedras_v403_sha256"]
_vn = esp["vereditos_novos_v404"]
assert _vn["projecao_transversal_v404"].startswith("TGL_PROJECAO_TRANSVERSAL_V404__THE_HALF_NAT_IS_THE_45_DEGREE_ANGLE") and _vn["jo8v32_v404"].startswith("TGL_JO8V32_V404__THE_WHOLE_TRIPLE") and _vn["f2b_errata_v404"].startswith("TGL_F2B_ERRATA_V404__CHANNEL_F2B_WITHDRAWN_BEFORE_DATA"), _vn
assert _vn["cunhagens_v404"].startswith("TGL_CUNHAGENS_V404__") and _vn["kh_n1_cobertura_v404"].startswith("TGL_KH_N1_COBERTURA_V404__"), _vn
assert sorted(esp["registros_v404"]) == ["cunhagens_v404", "kh_n1_cobertura_v404"] and sorted(esp["registros_v403"]) == ["cunhagens_v403", "kh_n1_cobertura_v403"] and sorted(esp["registros_v402"]) == ["cunhagens_v402", "kh_n1_cobertura_v402"] and sorted(esp["registros_v401"]) == ["cunhagens_v401", "kh_n1_cobertura_v401"]
_rf = esp["registros_funcao_v404"]
assert abs(_rf["projecao"]["values"]["sin_sq_pi_over_4"] - 0.5) <= 1e-15 and _rf["projecao"]["values"]["self_conjugate_weights"] == [0.5] and _rf["jo8v32"]["values"]["v403_mechanics_passed"] == [True, True, True] and _rf["f2b"]["values"]["previsao_fora_do_intervalo_de_A"] is True and _rf["f2b"]["F2b_status_now"] == DL.F2B_FUTURO_TOKEN, _rf
assert [_rf[k]["n_checks"] for k in ("projecao", "jo8v32", "f2b")] == [DL.N_CHECKS[k] for k in ("projecao", "jo8v32", "f2b")], [(k, _rf[k]["n_checks"]) for k in _rf]
assert len(esp["qg_closure_v403_checks"]) == 7 and all(c_[1] is True for c_ in esp["qg_closure_v403_checks"]), esp["qg_closure_v403_checks"]
assert esp["selo_acom"]["perfil"] == "ACOM-INT-C96-Q8" and esp["selo_acom"]["controles"] == [13, True] and esp["selo_acom"]["all_verified"] is True and esp["declaracao"]["all_verified"] is True and esp["declaracao"]["verbatim_sha256"] == DL.sha256(open(DL.VERBATIM_ORIGEM[DL.DECLARACAO_IDX], "rb").read())
# o selo da v404 difere do da v403 SELADA em: o selo ACOM (hashes do novo um.py), a versao, o sha256, as chaves novas (os tres resumos e registros_v404) e as chaves que carregam os numeros do kernel ou o hash proprio (a troca dita); o ensaio EXPLICA chave por chave
assert {"selo_pela_propria_tecnologia_v399", "um_version", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "registros_v404"} <= set(esp["selo_difere_do_v403_no_ensaio"]) and ens["selo"].get("difere_e_nao_e_so_o_esperado") == [], (esp["selo_difere_do_v403_no_ensaio"], ens["selo"].get("difere_e_nao_e_so_o_esperado"))
assert not ({"teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "declaracao_do_operador_v399", "registros_v399", "falsidade_da_inercia_v401", "registros_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402",
             "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "registros_v403"} & set(esp["selo_difere_do_v403_no_ensaio"])), "o selo de uma versao anterior mudou: o quadro e os registros anteriores NAO se mexem"
assert esp["veracidade"]["z_disc_abaixo_de_5"] and esp["veracidade"]["poder_previo_acima_de_5"]
assert ens["quadro"]["ok"] is True
out = os.path.join(HERE, "ESPERADOS_v404.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v404:", esp["candidato_sha16"], "| vereditos v403 pinados:", len(esp["vereditos_v403"]), "| flags True v403:", len(esp["flags_true_v403"]), "| troca dita:", troca)
