# -*- coding: utf-8 -*-
"""gerar_esperados_v405.py -- ESPERADOS_v405.json LIDOS dos artefatos (molde: gerar_esperados_v404.py FINAL, com as licoes da v399 a v404): o estado SELADO da v404 pinado. A TROCA DITA: (i) os registros da v404 cujo veredito carrega os numeros do kernel (escada, declaracoes, arquivos varridos)
-- achados por script no ensaio (recomputados; so' numeros mudam) -- e (ii) o estatuto da prova (v391), cujo veredito carrega o hash do PROPRIO um.py (a certificacao pelo proprio hash). Todos os outros vereditos da v404 ficam IGUAIS, os da v404 inclusive (os registros da v403 e projecao_transversal_v404, jo8v32_v404, f2b_errata_v404,
cunhagens_v404 e kh_n1_cobertura_v404 sao RECRIADOS e iguais ao selado). +13 chaves novas no core (os oito registros de pedra, cunhagens_v405, campos_fechados_e_leituras_v405, ga_reclassificacao_v405, gap_v405 e kh_n1_cobertura_v405) e +9 chaves no selo (os oito resumos e registros_v405); o selo pela propria
tecnologia (v399) muda so' nos hashes do novo um.py. O pilar pela mesma chave. O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo: os numeros dele vem do resultado pinado (v397\\insumos\\fase9) e o conferidor os confere de novo.
O GATE NAO SE MOVE: o qg_closure da v405 e' IDENTICO ao da v404 (sete checks, a letra do veredito, as 18 bandeiras): o ESPERADOS pina o hash do qg_closure da v404, o hash sem a lista de checks, a propria lista de sete checks e a letra do veredito. A funcao do neutrino NAO e' reescrita (o angle_status antigo fica):
o ESPERADOS pina o frozen_hash da regra de decisao e o veredito do canal; o V1 do ramo B (v386) e o livro da v383 seguem como estavam (o veredito deles e' o da base).
Nada digitado: cada numero e hash vem de CANDIDATO_v405.json, ensaio_a_seco_v405.json, do core/selo da v404 (base_v404), de kernel\\FLAGS_v405.json, de ESPERADOS_v404.json (o que o quadro pinou e os registros da v404) e do resultado pinado. Escrito a mao para a v405 (as chaves herdadas guardam os nomes da v404:
`vereditos_v404`, `flags_true_v404`... sao o estado da BASE; `registros_funcao_v403/v404` e `estrelas_v403/v404` sao os pinos dos registros de pedra das duas versoes anteriores, RECRIADOS; `pedras_v404_sha256` traz as CINCO pedras seladas das duas). As erratas E10 a E13 e as decisoes D27 a D33 da gerencia vao nos registros (cunhagens_v405); aqui so' se pinam os vereditos, os valores, as estrelas e os contratos.
ORDEM DE USO: depende do ensaio (ensaio_a_seco_v405.json com veredito TUDO PASSOU e o sha16 do candidato): sem ele este script PARA no primeiro assert (fail-closed)."""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v405 as DL  # noqa: E402
import quadro_v397 as QV  # noqa: E402
import guarda_frases_v405 as GF  # noqa: E402
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
J = lambda x: json.dumps(x, sort_keys=True, default=str)
BASE = os.path.join(HERE, DL.BASE_DIR)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v405.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, DL.CANDIDATO))
assert h16(os.path.join(BASE, "um.py")) == CM["base_v404_sha16"] == DL.BASE_SHA16_DA_ORDEM, "a base nao e' a v404 selada que a ordem deu"
_ens_p = os.path.join(HERE, "ensaio_a_seco_v405.json")
assert os.path.exists(_ens_p), "falta ensaio_a_seco_v405.json: o ensaio a seco (ato da gerencia) tem de rodar ANTES deste script -- nao gero ESPERADOS sem ele"
ens = json.load(open(_ens_p, encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"], (ens.get("veredito"), ens.get("sha16"))
R0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(BASE, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == DL.BASE_VERSION
E404 = json.load(open(os.path.join(DL.V404, "ESPERADOS_v404.json"), encoding="utf-8")); assert E404["candidato_sha16"] == CM["base_v404_sha16"]
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]; axr0 = kf["axiom_report"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
mud = ens["vizinhos"]["mudaram"]; te_ = ens["vizinhos"]["troca_esperada_so_o_hash_proprio"]
troca = sorted(set(mud) | set(te_))   # os vereditos da v404 que mudam: os que carregam os numeros do kernel (so' numeros) e o estatuto da prova (so' o hash proprio do um.py), recomputados pelo ensaio
assert troca, "a troca dita nao pode ser vazia (a escada mudou)"
assert set(te_) <= {"estatuto_da_prova_v391"}, te_
F = json.load(open(os.path.join(HERE, "FORMAL_MAP_v405.json"), encoding="utf-8"))
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v405.json"), encoding="utf-8"))["novos"]
pins = {p: F[p] for p in nov}
FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v405.json"), encoding="utf-8")); assert FJ["n_flags"] == CM["n_bandeiras"]
V404 = {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}
mf = ens["mainflow"]
SEL_KEYS = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "registros_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "registros_v394", "psibit_v395", "registros_v395", "testemunha_estatica_v396", "registros_v396",
            "teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "estatuto_da_prova_v391", "fundacao_v390", "text_label_errata_v389", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388",
            "declaracao_do_operador_v399", "registros_v399", "falsidade_da_inercia_v401", "registros_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402",
            "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "registros_v403", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "registros_v404")
assert all(k in selo0 for k in SEL_KEYS), [k for k in SEL_KEYS if k not in selo0]
vr = ens["veracidade_registro"]
RESP = os.path.join(DL.F9_DIR_DURAVEL, DL.F9_RESULTADO_NOME)
res9 = json.load(open(RESP, encoding="utf-8"))
numeros9 = {k: DL.lido(res9, c) for k, c in DL.F9_CAMINHOS.items()}
assert all(vr["lido"].get(k) == v for k, v in numeros9.items()), "os numeros lidos pelo registro no ensaio != os do resultado pinado"
assert E404["veracidade"]["numeros_do_resultado"] == numeros9 and E404["veracidade"]["resultado"]["sha256"] == DL.F9_RESULTADO_SHA256_DA_ORDEM, "o que a v404 pinou do Teste da Unica Palavra != o resultado em disco"
a_pt, mach_pt = QV.esperados(res9, "pt"); a_en, mach_en = QV.esperados(res9, "en")
assert mach_pt == E404["quadro"]["linha_de_maquina_pt"] and mach_en == E404["quadro"]["linha_de_maquina_en"], "a linha de maquina do quadro mudou: o quadro NAO se mexe"
TW405 = "A massa derivada e a identidade definida"; TW405E = "The derived mass and the defined identity"; TI405 = "A identidade"; TI405E = "The identity"
TJ404 = "Jo 8,32 e a projeção transversal da Meia-Nat"; TJ404E = "John 8:32 and the transverse projection of the Half-Nat"
MARCAS405_PT = [TW405, "O que entra.", "A moldura: o que fechou e o que entra.", "A Ponte da Massa.", "Massa = tensão pura.", "A lei do diminuto.", "A Tônica do Hamiltoniano.", "O Ponto Zero do Psíon.", "O Disco de Euler.", "Observador = terminal.", "A pedra Identidade.", "Erratas ao lado (v405).", "Limites.", "O fecho.", "Origem.", TI405, "Moldura da seção."]
MARCAS405_EN = [TW405E, "What enters.", "The frame: what closed and what enters.", "The Bridge of the Mass.", "Mass = pure tension.", "The law of the diminished.", "The Tonic of the Hamiltonian.", "The Zero Point of the Psion.", "Euler's Disk.", "Observer = terminal.", "The stone Identity.", "Errata alongside (v405).", "Limits.", "The closing.", "Origin.", TI405E, "Frame of the section."]
MARCAS404_PT = list(E404["artigo_marcas"]["pt"]); MARCAS404_EN = list(E404["artigo_marcas"]["en"])
sa, dc, sc = ens["selo_acom_registro"], ens["declaracao_registro"], ens["sidecar"]
MF4 = mf["registros_novos_v405"]; R405 = ens["v405_registros"]; R404 = ens["v404_registros"]
assert sorted(MF4) == sorted(list(DL.REGISTROS_FUNCAO) + [DL.CUNHAGENS_REGISTRO, DL.CAMPOS_REGISTRO, DL.GA_REGISTRO, DL.GAP_REGISTRO, DL.KH_REGISTRO]), sorted(MF4)
qg0 = core0.get("qg_closure") or {}
assert len(qg0.get("checks") or []) == 7 and (qg0.get("gate") or {}).get("verdict") == selo0.get("qg_closure_verdict"), "o gate da base (v404 selada) nao tem o formato esperado: sete checks e a letra do veredito == a do selo"
nm0 = core0["neutrino_mass"]; rb0 = core0["ramo_b_preregistration_v386"]
# os registros de pedra da v404, RECRIADOS: os pinos do ESPERADOS_v404 (os selados) e o que o ensaio recriou tem de ser a mesma coisa (vereditos e checagens)
RF404 = E404["registros_funcao_v404"]
for k_ in ("projecao", "jo8v32", "f2b"):
    assert R404[k_]["verdict"] == RF404[k_]["verdict"] and R404[k_]["n_checks"] == RF404[k_]["n_checks"], ("o registro da v404 recriado difere do selado", k_)
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v404_sha16"], "escada": [CM["escada"][1], CM["escada"][1]], "escada_v404_e_v405": CM["escada"], "n_bandeiras_novas": CM["n_bandeiras"],
       "bandeiras_novas_chaves": [f[0] for f in FJ["flags"]], "bandeiras_novas_nomes": [f[1] for f in FJ["flags"]],
       "cunhagens": CM["cunhagens"], "kernel": CM["kernel"], "pedras_sha256": pins, "formal_files_n": CM["formal_files_n"],
       "pedras_v404_sha256": {s["rel"]: kf["formal_files_sha256"][s["rel"]] for s in list(DL.D3.STONES) + list(DL.D4.STONES)},   # as CINCO pedras SELADAS da v403 e da v404: ficam no kernel como registro, com o sha do core selado
       "qg_closure_verdict": selo0.get("qg_closure_verdict"),
       "qg_closure_v404_json_sha256": hashlib.sha256(J(qg0).encode("utf-8")).hexdigest(),
       "qg_closure_v404_sem_checks_json_sha256": hashlib.sha256(J({k: v for k, v in qg0.items() if k != "checks"}).encode("utf-8")).hexdigest(),
       "qg_closure_v404_checks": json.loads(J(qg0.get("checks"))),
       "qg_closure_gate_verdict_v404": (qg0.get("gate") or {}).get("verdict"),
       "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v404": V404, "troca_dita": troca, "veredito_da_troca_no_ensaio": {k: (mud.get(k) or te_.get(k))["depois"] for k in troca},
       "regra_da_mudanca_dita": "so' os vereditos de `troca_dita` podem mudar (carregam a escada, as declaracoes ou a contagem de arquivos do kernel; so' numeros); qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v404": {k: selo0.get(k) for k in SEL_KEYS},
       "selo_difere_do_v404_no_ensaio": ens["selo"]["difere_do_selo_v404"],
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v404": sorted(k for k, v in kf.items() if v is True), "axiom_report_v404_n": len(axr0),
       "runtime_seals_v404": core0["runtime_of_the_one"]["seals"], "what_remains_v404": core0["tgl_closure"]["what_remains_named"],
       "neutrino_frozen_hash_v404": nm0["frozen_hash"], "neutrino_angle_status_antigo_sha256": hashlib.sha256(nm0["angle_status"].encode("utf-8")).hexdigest(),
       "f2b_antes": {"F2b_status": rb0["F2b_status"], "veredito_do_V1": rb0["veredito_do_V1"], "conjunto_D_n": rb0["conjunto_D_n"], "charge_F2b_token": core0["ledger_errata_v386"]["charge_F2b"]["token"]}, "f2b_depois": {"F2b_status_now": DL.D4.F2B_FUTURO_TOKEN}, "m_nu_meV_v404": nm0["m_nu_meV"], "titulo_secao_v405": {"pt": TW405, "en": TW405E}, "titulo_secao_v404": {"pt": TJ404, "en": TJ404E},
       "vereditos_novos_v405": {k: v["verdict"] for k, v in MF4.items()},
       "registros_v405": {k: v["verdict"] for k, v in MF4.items() if k in (DL.CUNHAGENS_REGISTRO, DL.CAMPOS_REGISTRO, DL.GA_REGISTRO, DL.GAP_REGISTRO, DL.KH_REGISTRO)},
       "ga_values": ens["ga_registro"]["values"], "gap_values": ens["gap_registro"]["values"], "ga_window_status": R0["ga_window_status"],
       "registros_v404": {k: V(k) for k in ("cunhagens_v404", "kh_n1_cobertura_v404")},
       "registros_v403": {k: V(k) for k in ("cunhagens_v403", "kh_n1_cobertura_v403")}, "registros_v402": {k: V(k) for k in ("cunhagens_v402", "kh_n1_cobertura_v402")}, "registros_v401": {k: V(k) for k in ("cunhagens_v401", "kh_n1_cobertura_v401")}, "veredito_da_falsidade_v404": V("falsidade_da_inercia_v401"),
       "registros_funcao_v405": {s["key"]: {"nome": DL.REGISTRO_DE_PEDRA[s["key"]], "verdict": R405[s["key"]]["verdict"], "values": R405[s["key"]]["values"], "n_checks": R405[s["key"]]["n_checks"]} for s in DL.STONES},
       "registros_funcao_v404": RF404, "registros_funcao_v403": E404["registros_funcao_v403"],
       "estrelas_v405": {s["key"]: {"teorema": s["key_theorem"], "bandeira": FJ["bandeiras_do_contrato"][s["key"]][s["key_theorem"]]} for s in DL.STONES},
       "estrelas_v404": E404["estrelas_v404"], "estrelas_v403": E404["estrelas_v403"],
       "registros_v399": {k: v["verdict"] for k, v in mf["registros_v399"].items()},
       "cobertura_kh_n1": ens["verify_kernel_ponta_a_ponta"]["cobertura"], "axiom_report_esperado_min": ens["verify_kernel_ponta_a_ponta"]["axiom_report_n"],
       "selo_acom": {"verdict": sa["verdict"], "all_verified": sa["all_verified"], "perfil": sa["perfil"], "bloco_embutido_sha256": sa["bloco_embutido_sha256"], "sha256_do_um_py": sa["sha256_do_um_py"], "bytes": sa["bytes"], "psi": sa["psi"], "theta": sa["theta"], "kappa": sa["kappa"],
                     "lut_sha256": sa["lut_sha256"], "m_max_abs": sa["m_max_abs"], "f_exp": sa["f_exp"], "entropia_dos_estados_bits": sa["entropia_dos_estados_bits"], "erro_real_maximo_antes_do_rint": sa["erro_real_maximo_antes_do_rint"],
                     "controles": [len(sa["controles"]), all(o_.startswith("RECUSOU:") for _, o_ in sa["controles"])], "controles_obtidos": {i_: o_ for i_, o_ in sa["controles"]}, "n_checks": len(sa["checks"]), "checks": sa["checks"], "auditoria_de_separacao": sa["auditoria_de_separacao"], "tempo_total_s_no_ensaio": sa["tempo_total_s"]},
       "declaracao": {"verdict": dc["verdict"], "all_verified": dc["all_verified"], "verbatim_sha256": dc["verbatim_sha256"], "sha16": dc["verbatim_sha256"][:16], "n_checks": len(dc["checks"]), "checks": dc["checks"], "ancoras": dc["ancoras"], "pedra": dc["pedra"], "linhas_da_trava": dc["linhas_da_trava"],
                      "direcao_do_testemunho": {"o_operador": "testifica DA IALD", "o_um_py": "testifica EM HASH", "a_IALD": "NAO testifica do operador", "o_Pai_de_Jo_8_18": "le-se no absoluto, o Um"}},
       "sidecar": {"arquivo": DL.SIDECAR_NOME, "esquema": "um_absoluto_selo_acom/v1 (v399)", "objetos": [o["nome"] for o in sc["objetos"]], "veredito_esperado_prefixo": "TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED", "um_py": next(o for o in sc["objetos"] if o["nome"] == "um.py"),
                   "tempo_s_no_ensaio": sc["tempo_s"], "entra_na_custodia": "D5 (proposta da gerencia): o sidecar e' arquivo novo da custodia; o handoff o lista"},
       "acom_estudo": E404["acom_estudo"],   # a secao do selo pela propria tecnologia NAO muda na v405: o que a v404 pinou (runtime da v400, bloco embutido, fontes do operador)
       "decisoes_da_gerencia": dict(DL.DECISOES), "erratas_E10_a_E13": list(DL.ERRATAS_V405), "leitura_v405": dict(DL.LEITURA_V405), "campos_fechados": dict(DL.CAMPOS_FECHADOS), "postos_e_medida": list(DL.POSTOS_E_MEDIDA), "leituras_definicoes": list(DL.LEITURAS_DEFINICOES), "forma_real": list(DL.FORMA_REAL), "guarda_frases": GF.controle_negativo()["ok"],
       "veracidade": E404["veracidade"], "quadro": E404["quadro"],   # o QUADRO do topo (v397) e o registro do Teste da Unica Palavra: o que a v397/v404 pinou, conferido de novo contra o resultado em disco
       "artigo_marcas": {"pt": MARCAS405_PT + MARCAS404_PT, "en": MARCAS405_EN + MARCAS404_EN},
       "artigo_nao": {"pt": list(E404["artigo_nao"]["pt"]) + ["Nesta rodada os registros da v405 NÃO selaram todos"], "en": list(E404["artigo_nao"]["en"]) + ["This round the v405 records did NOT all seal"]},
       "toc": {"pt": [TW405, TI405] + [w for w in E404["toc"]["pt"] if not w.startswith("v384 a ")] + ["v384 a " + DL.UM_VERSION], "en": [TW405E, TI405E] + [w for w in E404["toc"]["en"] if not w.startswith("v384 to ")] + ["v384 to " + DL.UM_VERSION]},   # o titulo da introducao diz `v384 a <versao desta rodada>`
       "the_iald_index_v404": {"all_verified": (core0.get("the_iald_index") or {}).get("all_verified"), "verdict": V("the_iald_index")}, "the_iald_index_v405": {"verdict": ens["indice_da_iald"]["verdict"]},
       "md_carimbo": "**Versão v405**", "md_massa": "A massa derivada e a identidade definida (v405, 01/11/2026)", "md_jo8": "Jo 8,32 e a projeção transversal da Meia-Nat (v404, 28/10/2026)", "md_caminho": "Caminho, Verdade e Vida (v403, 27/10/2026)", "md_ponte": "A ponte da escala dual, a queda sem geometria e a esperança condicional (v402, 26/10/2026)", "md_falsidade": "A falsidade (simulacro) da inércia (v401, 25/10/2026)", "md_errata": "Errata ao lado (v400, 24/10/2026)",
       "md_testemunho": "O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026)", "md_sonico": "Sônico e a afinação das cordas (v398, 23/10/2026)", "md_token": "O Teste da Única Palavra e a pedra Token (v397, 23/10/2026)",
       "md_testemunha": "A testemunha estática (v396, 22/10/2026)", "md_psibit": "O modo psiônico na fractalização do Um (v395, 21/10/2026)",
       "ensaio_sha16": h16(_ens_p),
       "h8_entradas": CM["h8"]["entradas"], "h8_residuais_do_nos": CM["h8"]["residuais_do_nos"], "formal_files_n_no_rito": CM["h8"]["entradas"],
       "n_bandeiras_por_grupo": dict(FJ["por_grupo_bandeiras"]), "politica_de_bandeiras": CM["politica_de_bandeiras"], "pedras": CM["kernel"]["pedras"], "teoremas_das_pedras": {s["key"]: s["theorem"] for s in DL.STONES},
       "bandeiras_das_pedras": CM["politica_de_bandeiras"]["bandeiras_do_teorema"], "suporte_das_pedras": {s["key"]: dict(s["support"]) for s in DL.STONES},
       "contrato_das_pedras": {s["key"]: list(s["contract"]) for s in DL.STONES}, "candidato_anterior_sha16": CM["base_v404_sha16"],
       "gate_nao_se_move": {"funcoes_identicas_a_base": CM["gate_nao_se_move"]["funcoes_identicas_a_base"], "gate_recomputado_no_ensaio": ens.get("gate_recomputado")}}
assert esp["the_iald_index_v404"]["all_verified"] is True and esp["not_sealed_formais"] == [], (esp["the_iald_index_v404"], esp["not_sealed_formais"])
assert esp["h8_entradas"] == len(esp["h8_residuais_do_nos"]) + CM["formal_files_n"] and sum(esp["n_bandeiras_por_grupo"].values()) == esp["n_bandeiras_novas"], "os ESPERADOS novos nao fecham"
assert esp["kernel"]["modulos_novos"] == len(esp["pedras_sha256"]) == len(nov) == 8, "o numero de modulos novos != a lista"
assert len(esp["pedras_v404_sha256"]) == 5 and all(len(h_) == 64 for h_ in esp["pedras_v404_sha256"].values()), esp["pedras_v404_sha256"]
_vn = esp["vereditos_novos_v405"]
assert all(_vn[DL.REGISTRO_DE_PEDRA[s["key"]]].startswith("TGL_") and "__GATE_UNMOVED" in _vn[DL.REGISTRO_DE_PEDRA[s["key"]]] for s in DL.STONES), _vn
assert _vn["cunhagens_v405"].startswith("TGL_CUNHAGENS_V405__") and _vn["campos_fechados_e_leituras_v405"].startswith("TGL_CAMPOS_FECHADOS_E_LEITURAS_V405") and _vn["ga_reclassificacao_v405"].startswith("TGL_GA_RECLASSIFICACAO_V405__") and _vn["gap_v405"].startswith("TGL_GAP_V405__") and _vn["kh_n1_cobertura_v405"].startswith("TGL_KH_N1_COBERTURA_V405__"), _vn
assert sorted(esp["registros_v405"]) == ["campos_fechados_e_leituras_v405", "cunhagens_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405"] and sorted(esp["registros_v404"]) == ["cunhagens_v404", "kh_n1_cobertura_v404"] and sorted(esp["registros_v403"]) == ["cunhagens_v403", "kh_n1_cobertura_v403"] and sorted(esp["registros_v402"]) == ["cunhagens_v402", "kh_n1_cobertura_v402"] and sorted(esp["registros_v401"]) == ["cunhagens_v401", "kh_n1_cobertura_v401"]
_rf = esp["registros_funcao_v405"]
assert abs(_rf["ponte"]["values"]["m_derivada_meV"] / esp["m_nu_meV_v404"] - 1.0) <= 1e-12 and abs(_rf["psion"]["values"]["meia_hbar_omega_meV"] / esp["m_nu_meV_v404"] - 1.0) <= 1e-12 and abs(_rf["diminuto"]["values"]["E0_eV"] - 1.0) <= 1e-12, _rf
assert [_rf[k]["n_checks"] for k in DL.N_CHECKS] == [DL.N_CHECKS[k] for k in DL.N_CHECKS] and sorted(_rf) == sorted(DL.N_CHECKS), [(k, _rf[k]["n_checks"]) for k in _rf]
assert not any(GF.violacoes(v_) for v_ in _vn.values()), "um veredito novo afirma demais"
assert len(esp["qg_closure_v404_checks"]) == 7 and all(c_[1] is True for c_ in esp["qg_closure_v404_checks"]), esp["qg_closure_v404_checks"]
assert esp["selo_acom"]["perfil"] == "ACOM-INT-C96-Q8" and esp["selo_acom"]["controles"] == [13, True] and esp["selo_acom"]["all_verified"] is True and esp["declaracao"]["all_verified"] is True and esp["declaracao"]["verbatim_sha256"] == DL.sha256(open(DL.VERBATIM_ORIGEM[DL.DECLARACAO_IDX], "rb").read())
# o selo da v405 difere do da v404 SELADA em: o selo ACOM (hashes do novo um.py), a versao, o sha256, as chaves novas (os oito resumos e registros_v405) e as chaves que carregam os numeros do kernel ou o hash proprio (a troca dita); o ensaio EXPLICA chave por chave
assert ({"selo_pela_propria_tecnologia_v399", "um_version", "registros_v405"} | set(DL.REGISTROS_FUNCAO)) <= set(esp["selo_difere_do_v404_no_ensaio"]) and ens["selo"].get("difere_e_nao_e_so_o_esperado") == [], (esp["selo_difere_do_v404_no_ensaio"], ens["selo"].get("difere_e_nao_e_so_o_esperado"))
assert not ({"teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "declaracao_do_operador_v399", "registros_v399", "falsidade_da_inercia_v401", "registros_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402",
             "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "registros_v403", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "registros_v404"} & set(esp["selo_difere_do_v404_no_ensaio"])), "o selo de uma versao anterior mudou: o quadro e os registros anteriores NAO se mexem"
assert esp["veracidade"]["z_disc_abaixo_de_5"] and esp["veracidade"]["poder_previo_acima_de_5"]
assert ens["quadro"]["ok"] is True
out = os.path.join(HERE, "ESPERADOS_v405.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v405:", esp["candidato_sha16"], "| vereditos v404 pinados:", len(esp["vereditos_v404"]), "| flags True v404:", len(esp["flags_true_v404"]), "| troca dita:", troca)
