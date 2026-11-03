# -*- coding: utf-8 -*-
"""gerar_esperados_v406.py -- ESPERADOS_v406.json LIDOS dos artefatos (molde: gerar_esperados_v405.py FINAL, com as licoes da v399 a v405; adaptado em 02/11/2026 ao FECHAMENTO: o modelo e' o de BUNDLE de 301 modulos, nao o das oito pedras): o estado SELADO da v405 pinado.
A TROCA DITA tem duas partes: (i) os vereditos da v405 que carregam os numeros do kernel (escada, declaracoes, arquivos varridos) e o estatuto da prova (v391), cujo veredito carrega o hash do PROPRIO um.py -- achados por script no ensaio (recomputados; so' numeros mudam) --
e (ii) a UNICA troca de TEXTO: rede_fock_v394 (JOINT_CONTRACT_OPEN -> JOINT_CERTIFICATE_INHABITED_V406__THREE_JOINT_ITEMS_STILL_OPEN), com o antes e o depois pinados em `troca_dita_textual`; os vereditos de psibit_v395 e testemunha_estatica_v396 NAO mudam. Todos os outros vereditos da v405 ficam IGUAIS
(os registros das v399 a v405 sao RECRIADOS e iguais ao selado, os oito de pedra da v405 inclusive). +3 chaves novas no core (fechamento_v406, cunhagens_v406 e kh_n1_cobertura_v406) e +2 chaves no selo (fechamento_v406 e registros_v406); o selo pela propria tecnologia (v399) muda so' nos hashes do novo um.py. O pilar pela mesma chave.
O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo: os numeros dele vem do resultado pinado (v397\\insumos\\fase9) e o conferidor os confere de novo.
As QUATRO chaves de testemunha (rede_fock_v394.whole_certificate_inhabited; psibit_v395...inhabitant_exhibited; testemunha_estatica_v396...inhabitant_exhibited; witness_layers.canonical_full_witness_term_constructed) passam a True, LIDAS do kernel (`chaves_v406_esperadas`, lidas do ensaio e asseveradas); full_static_witness_exists, trivial_inhabitant_exists e
linked_to_the_corner_by_a_lemma seguem False.
O GATE NAO SE MOVE: o qg_closure da v406 e' IDENTICO ao da v405 (sete checks, a letra do veredito, as 18 bandeiras): o ESPERADOS pina o hash do qg_closure da v405, o hash sem a lista de checks, a propria lista de sete checks e a letra do veredito. A funcao do neutrino NAO e' reescrita (o angle_status antigo fica):
o ESPERADOS pina o frozen_hash da regra de decisao e o veredito do canal; o V1 do ramo B (v386) e o livro da v383 seguem como estavam (o veredito deles e' o da base).
Nada digitado: cada numero e hash vem de CANDIDATO_v406.json, ensaio_a_seco_v406.json, do core/selo da v405 (base_v405), de kernel\\FLAGS_v406.json, de ESPERADOS_v405.json (o que o quadro pinou e os registros da v405) e do resultado pinado. As chaves herdadas guardam os nomes da v405:
`vereditos_v405`, `flags_true_v405`... sao o estado da BASE; `registros_funcao_v405/v404/v403` e `estrelas_v405/v404/v403` sao os pinos dos registros de pedra das tres versoes anteriores (RECRIADOS), lidos de ESPERADOS_v405; `pedras_v405_sha256` traz as TREZE pedras seladas das tres (oito da v405, duas da v404 e tres da v403).
As erratas E14 a E17 e as decisoes D34 a D40 da gerencia vao nos registros (cunhagens_v406); aqui so' se pinam os vereditos, os valores, as ancoras e os contratos.
ORDEM DE USO: depende do ensaio (ensaio_a_seco_v406.json com veredito TUDO PASSOU e o sha16 do candidato): sem ele este script PARA no primeiro assert (fail-closed). uso: python -I -B -X utf8 gerar_esperados_v406.py"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v406 as DL  # noqa: E402
import quadro_v397 as QV  # noqa: E402
import guarda_frases_v406 as GF  # noqa: E402
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
J = lambda x: json.dumps(x, sort_keys=True, default=str)
_num = lambda s_: re.sub(r"\d+", "#", re.sub(r"(?<![0-9a-f])[0-9a-f]{16}(?![0-9a-f])", "H", s_))
BASE = os.path.join(HERE, DL.BASE_DIR)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v406.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, DL.CANDIDATO))
assert h16(os.path.join(BASE, "um.py")) == CM["base_v405_sha16"] == DL.BASE_SHA16_DA_ORDEM, "a base nao e' a v405 selada que a ordem deu"
_ens_p = os.path.join(HERE, "ensaio_a_seco_v406.json")
assert os.path.exists(_ens_p), "falta ensaio_a_seco_v406.json: o ensaio a seco (ato da gerencia) tem de rodar ANTES deste script -- nao gero ESPERADOS sem ele"
ens = json.load(open(_ens_p, encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"], (ens.get("veredito"), ens.get("sha16"))
R0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(BASE, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == DL.BASE_VERSION
E405 = json.load(open(os.path.join(DL.V405, "ESPERADOS_v405.json"), encoding="utf-8")); assert E405["candidato_sha16"] == CM["base_v405_sha16"]
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]; axr0 = kf["axiom_report"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
mud = ens["vizinhos"]["mudaram"]; te_ = ens["vizinhos"]["troca_esperada_so_o_hash_proprio"]
# ---- a TROCA DITA: (i) so' numeros (mud) e o hash proprio (te_); (ii) o UNICO de texto, rede_fock_v394, pinado com o antes e o depois
REDE_FOCK_DEPOIS = "TGL_FOCK_NETWORK_V394__DERIVED_COMPONENTS__JOINT_CERTIFICATE_INHABITED_V406__THREE_JOINT_ITEMS_STILL_OPEN__GATE_UNMOVED"   # (o texto que o contrato da cadeia diz; o ensaio o mediu: asseverado igual abaixo)
tdv = ens["troca_dita_v406"]
assert tdv["declarada_no_candidato"] == CM["troca_dita_v406"] == ["rede_fock_v394"] and all(v_ is True for v_ in tdv["conferida"].values()), tdv
troca_dita_textual = {k_: {"antes": tdv["antes"][k_], "depois": tdv["depois"][k_]} for k_ in CM["troca_dita_v406"]}
assert troca_dita_textual["rede_fock_v394"]["antes"] == V("rede_fock_v394") and troca_dita_textual["rede_fock_v394"]["depois"] == REDE_FOCK_DEPOIS and "JOINT_CONTRACT_OPEN" in V("rede_fock_v394"), troca_dita_textual
for k_ in ("psibit_v395", "testemunha_estatica_v396"):   # estes dois NAO mudam de veredito
    assert k_ not in mud and k_ not in te_ and k_ not in troca_dita_textual, k_
troca = sorted(set(mud) | set(te_) | set(troca_dita_textual))   # os vereditos da v405 que mudam: so' numeros (escada, declaracoes, arquivos varridos), o hash proprio do um.py (estatuto da prova) e o de texto dito (rede_fock_v394)
assert troca, "a troca dita nao pode ser vazia (a escada mudou)"
assert set(te_) <= {"estatuto_da_prova_v391"}, te_
F = json.load(open(os.path.join(HERE, "FORMAL_MAP_v406.json"), encoding="utf-8"))
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v406.json"), encoding="utf-8"))["novos"]
assert nov == list(DL.BUNDLE_RELS) and len(nov) == DL.N_BUNDLE == 301
pins = {p: F[p] for p in nov}
assert all(pins[p] == DL.BUNDLE_POR_REL[p]["sha256"] for p in nov), "o FORMAL_MAP diverge do BUNDLE_v406.json"
FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v406.json"), encoding="utf-8")); assert FJ["n_flags"] == CM["n_bandeiras"] == 1794 and len(FJ["ancoras"]) == 8
bandeiras_novas_modulos = {f[1]: FJ["proveniencia_publicas"].get(f[1]) for f in FJ["flags"]}
assert all(bandeiras_novas_modulos.values()) and set(bandeiras_novas_modulos.values()) <= set(nov), "toda declaracao nomeada do bundle tem de ter o modulo que o compilador emitiu"
V405 = {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}
mf = ens["mainflow"]
SEL_STONES405 = ["ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405"]
SEL_KEYS = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "registros_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "registros_v394", "psibit_v395", "registros_v395", "testemunha_estatica_v396", "registros_v396",
            "teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "estatuto_da_prova_v391", "fundacao_v390", "text_label_errata_v389", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388",
            "declaracao_do_operador_v399", "registros_v399", "falsidade_da_inercia_v401", "registros_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402",
            "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "registros_v403", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "registros_v404") + tuple(SEL_STONES405) + ("registros_v405",)
assert all(k in selo0 for k in SEL_KEYS), [k for k in SEL_KEYS if k not in selo0]
difere_selo = ens["selo"]["difere_do_selo_v405"]
selo_chaves_que_mudam = sorted(k for k in SEL_KEYS if k in difere_selo and k not in troca)   # as chaves do selo da v405 que mudam por LEREM as quatro chaves do kernel (rede_fock_v394, psibit_v395, testemunha_estatica_v396): ditas, explicadas pelo ensaio
assert set(selo_chaves_que_mudam) <= {"rede_fock_v394", "psibit_v395", "testemunha_estatica_v396"}, selo_chaves_que_mudam
vr = ens["veracidade_registro"]
RESP = os.path.join(DL.F9_DIR_DURAVEL, DL.F9_RESULTADO_NOME)
res9 = json.load(open(RESP, encoding="utf-8"))
numeros9 = {k: DL.lido(res9, c) for k, c in DL.F9_CAMINHOS.items()}
assert all(vr["lido"].get(k) == v for k, v in numeros9.items()), "os numeros lidos pelo registro no ensaio != os do resultado pinado"
assert E405["veracidade"]["numeros_do_resultado"] == numeros9 and E405["veracidade"]["resultado"]["sha256"] == DL.F9_RESULTADO_SHA256_DA_ORDEM, "o que a v405 pinou do Teste da Unica Palavra != o resultado em disco"
a_pt, mach_pt = QV.esperados(res9, "pt"); a_en, mach_en = QV.esperados(res9, "en")
assert mach_pt == E405["quadro"]["linha_de_maquina_pt"] and mach_en == E405["quadro"]["linha_de_maquina_en"], "a linha de maquina do quadro mudou: o quadro NAO se mexe"
# ---- o artigo: os titulos e as marcas da secao v406 saem DOS PROPRIOS snippets (nada digitado); as marcas da v405 e anteriores vem do ESPERADOS_v405
_snip = {l_: open(os.path.join(HERE, "artigo_%s_v406.pysnip" % l_), encoding="utf-8").read() for l_ in ("pt", "en")}
_BS = chr(92)
TIT406 = {l_: re.findall(re.escape(_BS + "section*{") + r"([^{}]*)\}", _snip[l_]) for l_ in ("pt", "en")}
assert all(len(v_) == 1 for v_ in TIT406.values()), TIT406
TIT406 = {l_: v_[0] for l_, v_ in TIT406.items()}
_marcas_brutas = {l_: re.findall(re.escape(_BS + "textbf{") + r"([^{}]{3,160}\.|[^{}]{3,160}:[^{}]{0,200})\}", _snip[l_]) for l_ in ("pt", "en")}
_NAO406 = {l_: [m_.split(":")[0] for m_ in _marcas_brutas[l_] if m_.startswith(("Nesta rodada os registros da v406", "In this run the v406 records"))] for l_ in ("pt", "en")}
MARCAS406 = {l_: [TIT406[l_]] + [m_ for m_ in _marcas_brutas[l_] if m_.endswith(".") and not m_.startswith(("Nesta rodada", "In this run"))] for l_ in ("pt", "en")}
assert all(len(_NAO406[l_]) == 1 for l_ in ("pt", "en")) and all(len(MARCAS406[l_]) >= 6 for l_ in ("pt", "en")), (_NAO406, MARCAS406)
TV405 = E405["titulo_secao_v405"]   # {pt, en} = «A massa derivada e a identidade definida» (a secao da v405 vem logo depois da v406)
sa, dc, sc = ens["selo_acom_registro"], ens["declaracao_registro"], ens["sidecar"]
MF4 = mf["registros_novos_v406"]
assert sorted(MF4) == sorted(list(DL.REGISTROS_FUNCAO) + [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]), sorted(MF4)
FE = ens["fechamento_v406"]
assert FE["all_verified"] is True and FE["n_checks"] == DL.N_CHECKS_FECHO == 14 and FE["certificate_inhabited"] is True and FE["embedded_sources_n_ok"] == DL.N_BUNDLE and len(FE["anchors"]) == 8 and all(FE["anchors"].values()), FE.get("verdict")
chaves_v406_esperadas = dict(FE["four_keys"])
assert chaves_v406_esperadas["kernel_reads_the_certificate_as_inhabited"] is True and chaves_v406_esperadas["rede_fock_v394.whole_certificate_inhabited"] is True and chaves_v406_esperadas["psibit_v395.conditional_psion_face.inhabitant_exhibited"] is True and chaves_v406_esperadas["psibit_v395.conditional_psion_face.status"] == DL.STATUS_HABITADO \
    and chaves_v406_esperadas["testemunha_estatica_v396.fock_face.inhabitant_exhibited"] is True and chaves_v406_esperadas["testemunha_estatica_v396.fock_face.status"] == DL.STATUS_HABITADO and chaves_v406_esperadas["witness_layers.canonical_full_witness_term_constructed"] is True \
    and chaves_v406_esperadas["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is False and chaves_v406_esperadas["witness_rigidity.trivial_inhabitant_exists"] is False and chaves_v406_esperadas["qg_closure.gate.full_static_witness_exists"] is False, chaves_v406_esperadas
qg0 = core0.get("qg_closure") or {}
assert len(qg0.get("checks") or []) == 7 and (qg0.get("gate") or {}).get("verdict") == selo0.get("qg_closure_verdict"), "o gate da base (v405 selada) nao tem o formato esperado: sete checks e a letra do veredito == a do selo"
nm0 = core0["neutrino_mass"]; rb0 = core0["ramo_b_preregistration_v386"]


# ---- os registros de pedra das versoes anteriores, RECRIADOS: os pinos do ESPERADOS_v405 (os selados) e o que o ensaio recriou tem de ser a mesma coisa (veredito, checagens e valores)
def _stones(chaves_):
    """o dict de registros de pedra do ensaio que tem exatamente estas chaves (o ensaio guarda por versao: v402_registros, v403_registros... ; aqui se acha pela forma, nao pelo nome)"""
    ach_ = [v_ for k_, v_ in ens.items() if k_.endswith("_registros") and isinstance(v_, dict) and set(chaves_) <= set(v_)]
    assert ach_, ("o ensaio nao traz os registros", chaves_)
    return ach_[0]


def _feq(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_feq(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_feq(x, y) for x, y in zip(a, b))
    if isinstance(a, float) and isinstance(b, float):
        return a == b or abs(a - b) <= 1e-12 * max(1.0, abs(a), abs(b))
    return a == b


RF405, RF404, RF403 = E405["registros_funcao_v405"], E405["registros_funcao_v404"], E405["registros_funcao_v403"]
for nome_, RF_, ens_ in (("v405", RF405, _stones(["ponte", "tensao", "identidade", "observador", "diminuto", "tonica", "disco", "psion"])), ("v404", RF404, _stones(["projecao", "jo8v32", "f2b"])), ("v403", RF403, _stones(["caminho", "vida", "verdade_adendo"]))):
    for k_ in RF_:
        if k_ == "gate":
            continue
        assert ens_[k_]["verdict"] == RF_[k_]["verdict"] and ens_[k_]["n_checks"] == RF_[k_]["n_checks"], ("o registro recriado difere do selado", nome_, k_)
        assert _feq({kk_: ens_[k_]["values"].get(kk_) for kk_ in RF_[k_]["values"]}, RF_[k_]["values"]), ("os VALORES do registro recriado diferem dos selados", nome_, k_)
for k_, d_ in mf["recriados_v393_a_v405"].items():   # os registros por spec (cunhagens, kh_n1, campos, ga, gap) recriados: verdade, e igual ao selado ou so' numeros
    assert d_["all_verified"] is True, ("registro recriado nao selou", k_)
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v405_sha16"], "escada": [CM["escada"][1], CM["escada"][1]], "escada_v405_e_v406": CM["escada"], "n_bandeiras_novas": CM["n_bandeiras"],
       "bandeiras_novas_chaves": [f[0] for f in FJ["flags"]], "bandeiras_novas_nomes": [f[1] for f in FJ["flags"]], "bandeiras_novas_modulos": bandeiras_novas_modulos,
       "cunhagens": CM["cunhagens"], "kernel": {k_: v_ for k_, v_ in CM["kernel"].items() if k_ != "bundle"}, "bundle_sha256": pins, "formal_files_n": CM["formal_files_n"],
       "pedras_v405_sha256": {s["rel"]: kf["formal_files_sha256"][s["rel"]] for s in list(DL.D5.STONES) + list(DL.D4.STONES) + list(DL.D3.STONES)},   # as TREZE pedras SELADAS (oito da v405, duas da v404, tres da v403): ficam no kernel como registro, com o sha do core selado
       "qg_closure_verdict": selo0.get("qg_closure_verdict"),
       "qg_closure_v405_json_sha256": hashlib.sha256(J(qg0).encode("utf-8")).hexdigest(),
       "qg_closure_v405_sem_checks_json_sha256": hashlib.sha256(J({k: v for k, v in qg0.items() if k != "checks"}).encode("utf-8")).hexdigest(),
       "qg_closure_v405_checks": json.loads(J(qg0.get("checks"))),
       "qg_closure_gate_verdict_v405": (qg0.get("gate") or {}).get("verdict"),
       "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v405": V405, "troca_dita": troca, "troca_dita_textual": troca_dita_textual,
       "veredito_da_troca_no_ensaio": {k: ((mud.get(k) or te_.get(k) or {}).get("depois") if k not in troca_dita_textual else troca_dita_textual[k]["depois"]) for k in troca},
       "regra_da_mudanca_dita": "so' os vereditos de `troca_dita` podem mudar: os que carregam a escada, as declaracoes ou a contagem de arquivos do kernel (so' numeros), o estatuto da prova (so' o hash proprio do um.py) e UM de texto, rede_fock_v394, cujo antes e depois estao em `troca_dita_textual` (razao dita: o certificado de Fock esta' habitado por construcao no kernel; tres itens conjuntos seguem abertos); qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v405": {k: selo0.get(k) for k in SEL_KEYS}, "selo_chaves_que_mudam": selo_chaves_que_mudam,
       "selo_difere_do_v405_no_ensaio": difere_selo,
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v405": sorted(k for k, v in kf.items() if v is True), "axiom_report_v405_n": len(axr0),
       "runtime_seals_v405": core0["runtime_of_the_one"]["seals"], "what_remains_v405": core0["tgl_closure"]["what_remains_named"],
       "neutrino_frozen_hash_v405": nm0["frozen_hash"], "neutrino_angle_status_antigo_sha256": hashlib.sha256(nm0["angle_status"].encode("utf-8")).hexdigest(),
       "f2b_antes": {"F2b_status": rb0["F2b_status"], "veredito_do_V1": rb0["veredito_do_V1"], "conjunto_D_n": rb0["conjunto_D_n"], "charge_F2b_token": core0["ledger_errata_v386"]["charge_F2b"]["token"]}, "f2b_depois": {"F2b_status_now": DL.D4.F2B_FUTURO_TOKEN}, "m_nu_meV_v404": nm0["m_nu_meV"],
       "titulo_secao_v406": TIT406, "titulo_secao_v405": dict(TV405),
       "vereditos_novos_v406": {k: v["verdict"] for k, v in MF4.items()},
       "registros_v406": {k: v["verdict"] for k, v in MF4.items() if k in (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO)},
       "registros_v405": {k: V(k) for k in ("cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405")},
       "ga_values": ens["ga_registro"]["values"], "gap_values": ens["gap_registro"]["values"], "ga_window_status": R0["ga_window_status"],
       "registros_v404": {k: V(k) for k in ("cunhagens_v404", "kh_n1_cobertura_v404")},
       "registros_v403": {k: V(k) for k in ("cunhagens_v403", "kh_n1_cobertura_v403")}, "registros_v402": {k: V(k) for k in ("cunhagens_v402", "kh_n1_cobertura_v402")}, "registros_v401": {k: V(k) for k in ("cunhagens_v401", "kh_n1_cobertura_v401")}, "veredito_da_falsidade_v405": V("falsidade_da_inercia_v401"),
       "registros_funcao_v406": {"fechamento": {"nome": DL.FECHO_REGISTRO, "verdict": FE["verdict"], "values": FE["values"], "n_checks": FE["n_checks"]}},
       "registros_funcao_v405": RF405, "registros_funcao_v404": RF404, "registros_funcao_v403": RF403,
       "estrelas_v406": {nome_: {"teorema": nome_, "bandeira": a_["flag"], "rel": a_["rel"], "classe": a_.get("classe")} for nome_, a_ in FJ["ancoras"].items()},
       "estrelas_v405": E405["estrelas_v405"], "estrelas_v404": E405["estrelas_v404"], "estrelas_v403": E405["estrelas_v403"],
       "bandeiras_das_pedras_v405": E405["bandeiras_das_pedras"], "teoremas_das_pedras_v405": E405["teoremas_das_pedras"], "contrato_das_pedras_v405": E405["contrato_das_pedras"], "suporte_das_pedras_v405": E405["suporte_das_pedras"],
       "registros_v399": {k: v["verdict"] for k, v in mf["registros_v399"].items()},
       "cobertura_kh_n1": ens["verify_kernel_ponta_a_ponta"]["cobertura"], "axiom_report_esperado_min": ens["verify_kernel_ponta_a_ponta"]["axiom_report_n"],
       "selo_acom": {"verdict": sa["verdict"], "all_verified": sa["all_verified"], "perfil": sa["perfil"], "bloco_embutido_sha256": sa["bloco_embutido_sha256"], "sha256_do_um_py": sa["sha256_do_um_py"], "bytes": sa["bytes"], "psi": sa["psi"], "theta": sa["theta"], "kappa": sa["kappa"],
                     "lut_sha256": sa["lut_sha256"], "m_max_abs": sa["m_max_abs"], "f_exp": sa["f_exp"], "entropia_dos_estados_bits": sa["entropia_dos_estados_bits"], "erro_real_maximo_antes_do_rint": sa["erro_real_maximo_antes_do_rint"],
                     "controles": [len(sa["controles"]), all(o_.startswith("RECUSOU:") for _, o_ in sa["controles"])], "controles_obtidos": {i_: o_ for i_, o_ in sa["controles"]}, "n_checks": len(sa["checks"]), "checks": sa["checks"], "auditoria_de_separacao": sa["auditoria_de_separacao"], "tempo_total_s_no_ensaio": sa["tempo_total_s"]},
       "declaracao": {"verdict": dc["verdict"], "all_verified": dc["all_verified"], "verbatim_sha256": dc["verbatim_sha256"], "sha16": dc["verbatim_sha256"][:16], "n_checks": len(dc["checks"]), "checks": dc["checks"], "ancoras": dc["ancoras"], "pedra": dc["pedra"], "linhas_da_trava": dc["linhas_da_trava"],
                      "direcao_do_testemunho": {"o_operador": "testifica DA IALD", "o_um_py": "testifica EM HASH", "a_IALD": "NAO testifica do operador", "o_Pai_de_Jo_8_18": "le-se no absoluto, o Um"}},
       "sidecar": {"arquivo": DL.SIDECAR_NOME, "esquema": "um_absoluto_selo_acom/v1 (v399)", "objetos": [o["nome"] for o in sc["objetos"]], "veredito_esperado_prefixo": "TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED", "um_py": next(o for o in sc["objetos"] if o["nome"] == "um.py"),
                   "tempo_s_no_ensaio": sc["tempo_s"], "entra_na_custodia": "D5 (proposta da gerencia): o sidecar e' arquivo novo da custodia; o handoff o lista"},
       "acom_estudo": E405["acom_estudo"],   # a secao do selo pela propria tecnologia NAO muda na v406: o que a v405 pinou (runtime da v400, bloco embutido, fontes do operador)
       "decisoes_da_gerencia": dict(DL.DECISOES), "decisoes_v406_ids": sorted((k for k in DL.DECISOES if k[1:].isdigit() and int(k[1:]) >= 34), key=lambda k: int(k[1:])), "erratas_E14_E17": list(DL.ERRATAS_V406), "ressalvas": list(DL.RESSALVAS_V406), "leitura_v406": dict(DL.LEITURA_V406),
       "chaves_v406": [dict(c_) for c_ in DL.CHAVES_V406], "chaves_v406_esperadas": chaves_v406_esperadas, "fica_false_por_teorema": list(DL.FICAM_FALSE_POR_TEOREMA), "regra_do_4_44": DL.REGRA_DO_4_44, "guarda_frases": GF.controle_negativo()["ok"],
       "veracidade": E405["veracidade"], "quadro": E405["quadro"],   # o QUADRO do topo (v397) e o registro do Teste da Unica Palavra: o que a v397/v405 pinou, conferido de novo contra o resultado em disco
       "artigo_marcas": {l_: MARCAS406[l_] + list(E405["artigo_marcas"][l_]) for l_ in ("pt", "en")},
       "artigo_nao": {l_: list(E405["artigo_nao"][l_]) + _NAO406[l_] for l_ in ("pt", "en")},
       "toc": {"pt": [TIT406["pt"]] + [w for w in E405["toc"]["pt"] if not w.startswith("v384 a ")] + ["v384 a " + DL.UM_VERSION], "en": [TIT406["en"]] + [w for w in E405["toc"]["en"] if not w.startswith("v384 to ")] + ["v384 to " + DL.UM_VERSION]},   # o titulo da introducao diz `v384 a <versao desta rodada>`
       "the_iald_index_v405": {"all_verified": (core0.get("the_iald_index") or {}).get("all_verified"), "verdict": V("the_iald_index")}, "the_iald_index_v406": {"verdict": ens["indice_da_iald"]["verdict"]},
       "md_carimbo": "**Versão v406**", "md_fechamento": "O fechamento (v406, 02/11/2026)", "md_massa": E405["md_massa"], "md_jo8": E405["md_jo8"], "md_caminho": E405["md_caminho"], "md_ponte": E405["md_ponte"], "md_falsidade": E405["md_falsidade"], "md_errata": E405["md_errata"],
       "md_testemunho": E405["md_testemunho"], "md_sonico": E405["md_sonico"], "md_token": E405["md_token"], "md_testemunha": E405["md_testemunha"], "md_psibit": E405["md_psibit"],
       "ensaio_sha16": h16(_ens_p),
       "h8_entradas": CM["h8"]["entradas"], "h8_residuais_do_nos": CM["h8"]["residuais_do_nos"], "formal_files_n_no_rito": CM["h8"]["entradas"],
       "n_bandeiras_por_grupo": dict(FJ["por_grupo_bandeiras"]), "politica_de_bandeiras": {k_: v_ for k_, v_ in CM["politica_de_bandeiras"].items() if k_ != "contrato"},
       "candidato_anterior_sha16": CM["base_v405_sha16"],
       "gate_nao_se_move": {"funcoes_identicas_a_base": CM["gate_nao_se_move"]["funcoes_identicas_a_base"], "gate_recomputado_no_ensaio": ens.get("gate_recomputado")}}
assert esp["the_iald_index_v405"]["all_verified"] is True and esp["not_sealed_formais"] == [], (esp["the_iald_index_v405"], esp["not_sealed_formais"])
assert esp["h8_entradas"] == len(esp["h8_residuais_do_nos"]) + CM["formal_files_n"] == 1747 and sum(esp["n_bandeiras_por_grupo"].values()) == esp["n_bandeiras_novas"] == 1794, "os ESPERADOS novos nao fecham"
assert esp["kernel"]["modulos_novos"] == len(esp["bundle_sha256"]) == len(nov) == 301, "o numero de modulos novos != a lista"
assert len(esp["pedras_v405_sha256"]) == 13 and all(len(h_) == 64 for h_ in esp["pedras_v405_sha256"].values()), esp["pedras_v405_sha256"]
assert esp["escada"] == [11860, 11860] and esp["escada_v405_e_v406"] == [10066, 11860], esp["escada"]
assert esp["cobertura_kh_n1"]["decl"] == 33732 and esp["cobertura_kh_n1"]["thm"] == 26911 and esp["axiom_report_esperado_min"] == 33732 and esp["cobertura_kh_n1"].get("fora_do_trio") == 0, esp["cobertura_kh_n1"]
_vn = esp["vereditos_novos_v406"]
assert _vn[DL.FECHO_REGISTRO].startswith("TGL_FECHAMENTO_V406__THE_FOCK_CERTIFICATE_IS_INHABITED_BY_CONSTRUCTION") and _vn[DL.FECHO_REGISTRO].endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED") and _vn[DL.CUNHAGENS_REGISTRO].startswith("TGL_CUNHAGENS_V406__") and _vn[DL.KH_REGISTRO].startswith("TGL_KH_N1_COBERTURA_V406__"), _vn
assert all("__GATE_UNMOVED" in v_ for v_ in _vn.values()) and all(v_["all_verified"] is True for v_ in MF4.values()), MF4
assert sorted(esp["registros_v405"]) == ["campos_fechados_e_leituras_v405", "cunhagens_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405"] and sorted(esp["registros_v406"]) == ["cunhagens_v406", "kh_n1_cobertura_v406"] and sorted(esp["registros_v404"]) == ["cunhagens_v404", "kh_n1_cobertura_v404"] and sorted(esp["registros_v403"]) == ["cunhagens_v403", "kh_n1_cobertura_v403"] and sorted(esp["registros_v402"]) == ["cunhagens_v402", "kh_n1_cobertura_v402"] and sorted(esp["registros_v401"]) == ["cunhagens_v401", "kh_n1_cobertura_v401"]
_rf6 = esp["registros_funcao_v406"]["fechamento"]
assert _rf6["values"]["n_ancoras_ok"] == 8 and _rf6["values"]["n_modulos_ok"] == _rf6["values"]["n_modulos"] == 301 and _rf6["values"]["n_flags_true"] == _rf6["values"]["n_flags"] == 1794 and _rf6["values"]["escada"] == [11860, 11860, 11860] and _rf6["values"]["certificado_habitado_lido_do_kernel"] is True and _feq(_rf6["values"]["chaves"], chaves_v406_esperadas), _rf6["values"]
_rf5 = esp["registros_funcao_v405"]
assert abs(_rf5["ponte"]["values"]["m_derivada_meV"] / esp["m_nu_meV_v404"] - 1.0) <= 1e-12 and abs(_rf5["psion"]["values"]["meia_hbar_omega_meV"] / esp["m_nu_meV_v404"] - 1.0) <= 1e-12 and abs(_rf5["diminuto"]["values"]["E0_eV"] - 1.0) <= 1e-12, "o numero da massa mudou"
assert not any(GF.violacoes(v_) for v_ in _vn.values()), "um veredito novo afirma demais"
assert len(esp["qg_closure_v405_checks"]) == 7 and all(c_[1] is True for c_ in esp["qg_closure_v405_checks"]), esp["qg_closure_v405_checks"]
assert esp["selo_acom"]["perfil"] == "ACOM-INT-C96-Q8" and esp["selo_acom"]["controles"] == [13, True] and esp["selo_acom"]["all_verified"] is True and esp["declaracao"]["all_verified"] is True and esp["declaracao"]["verbatim_sha256"] == DL.sha256(open(DL.VERBATIM_ORIGEM[DL.DECLARACAO_IDX], "rb").read())
# o selo da v406 difere do da v405 SELADA em: o selo ACOM (hashes do novo um.py), a versao, o sha256, as chaves novas (fechamento_v406 e registros_v406), as chaves que carregam os numeros do kernel ou o hash proprio (a troca dita) e as tres que LEEM as chaves do kernel; o ensaio EXPLICA chave por chave
assert ({"selo_pela_propria_tecnologia_v399", "um_version", "fechamento_v406", "registros_v406"}) <= set(esp["selo_difere_do_v405_no_ensaio"]) and ens["selo"].get("difere_e_nao_e_so_o_esperado") == [], (esp["selo_difere_do_v405_no_ensaio"], ens["selo"].get("difere_e_nao_e_so_o_esperado"))
assert not ({"teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "declaracao_do_operador_v399", "registros_v399", "falsidade_da_inercia_v401", "registros_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402",
             "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "registros_v403", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "registros_v404", "registros_v405"} | set(SEL_STONES405)) & set(esp["selo_difere_do_v405_no_ensaio"]), "o selo de uma versao anterior mudou: o quadro e os registros anteriores NAO se mexem"
assert esp["veracidade"]["z_disc_abaixo_de_5"] and esp["veracidade"]["poder_previo_acima_de_5"]
assert ens["quadro"]["ok"] is True
out = os.path.join(HERE, "ESPERADOS_v406.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v406:", esp["candidato_sha16"], "| vereditos v405 pinados:", len(esp["vereditos_v405"]), "| flags True v405:", len(esp["flags_true_v405"]), "| troca dita:", troca, "| selo_chaves_que_mudam:", selo_chaves_que_mudam)
