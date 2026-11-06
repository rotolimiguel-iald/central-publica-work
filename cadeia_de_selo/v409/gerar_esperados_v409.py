# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] a v409 (A TRADUCAO AS CLASSES DE TURING): o registro novo traducao_turing_v409 (2 modulos, 82 ancoras, 20 checagens); o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados; o esquema de chaves que o pos-rito le; md_traducao lida do candidato
"""gerar_esperados_v409.py -- ESPERADOS_v409.json LIDOS dos artefatos (molde: gerar_esperados_v408.py FINAL, com as licoes da v399 a v408; adaptado em 05/11/2026 por claude-construtor-v409 a v409, A TRADUCAO AS CLASSES DE TURING:
bundle de 2 modulos em TGLExt/ -- TraducaoTuring e ParNaFaceDeFock --, registro com funcao traducao_turing_v409, 82 ancoras, 20 checagens): o estado SELADO da v408 pinado.
A TROCA DITA da v409 e' SO' de NUMEROS: os vereditos da v408 que carregam os numeros do kernel (escada, declaracoes, arquivos varridos) e o estatuto da prova (v391), cujo veredito carrega o hash do PROPRIO um.py -- achados por script no ensaio (recomputados; so' numeros mudam).
NAO ha troca dita de TEXTO (o CANDIDATO_v409.json nao declara `troca_dita_v409`) e NENHUMA chave antiga muda: os vereditos de rede_fock_v394, psibit_v395, testemunha_estatica_v396, fechamento_v406, psion_canto_v407 e tetelestai_terminal_v408 NAO mudam; `troca_dita_textual` fica vazio, por asseveracao (se o ensaio medir que algum deles mudou, este script PARA no assert: e' defeito do candidato ou do contrato, nao se 'conserta' aqui).
Todos os outros vereditos da v408 ficam IGUAIS (os registros das v399 a v408 sao RECRIADOS e iguais ao selado; o fechamento_v406, o psion_canto_v407 e o tetelestai_terminal_v408 recriados com a escada do contrato subida pela C12, o veredito igual). +3 chaves novas no core (traducao_turing_v409, cunhagens_v409 e kh_n1_cobertura_v409) e +2 chaves no selo (traducao_turing_v409 e registros_v409); o selo pela propria tecnologia (v399) muda so' nos hashes do novo um.py. O pilar pela mesma chave.
O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo: os numeros dele vem do resultado pinado (v397\\insumos\\fase9) e o conferidor os confere de novo.
As CHAVES: nenhuma nova e nenhuma antiga muda (`chaves_v409` vazio); as que o psion_canto_v407 le seguem como na v408 selada (`chaves_v407_esperadas`, lidas do ensaio e asseveradas iguais as de ESPERADOS_v408); full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA.
O GATE NAO SE MOVE: o qg_closure da v409 e' IDENTICO ao da v408 (sete checks, a letra do veredito, as 18 bandeiras): o ESPERADOS pina o hash do qg_closure da v408, o hash sem a lista de checks, a propria lista de sete checks e a letra do veredito. A funcao do neutrino NAO e' reescrita (o angle_status antigo fica):
o ESPERADOS pina o frozen_hash da regra de decisao e o veredito do canal; o V1 do ramo B (v386) e o livro da v383 seguem como estavam (o veredito deles e' o da base).
Nada digitado: cada numero e hash vem de CANDIDATO_v409.json, ensaio_a_seco_v409.json, do core/selo da v408 (base_v408), de kernel\\FLAGS_v409.json, kernel\\KH_N1_v409.json, de ESPERADOS_v408.json (o que o quadro pinou e os registros da v408) e do resultado pinado. As chaves herdadas guardam os nomes da v408:
`vereditos_v408`, `flags_true_v408`... sao o estado da BASE; `registros_funcao_v405/v404/v403` e `estrelas_v405/v404/v403` sao os pinos dos registros de pedra das versoes anteriores (RECRIADOS), lidos de ESPERADOS_v408;
`registros_funcao_v406.fechamento` e `estrelas_v406` sao o fechamento_v406 herdado; `registros_funcao_v407.psion_canto` e `estrelas_v407` (as 76 ancoras) sao o psion_canto_v407 herdado; `registros_funcao_v408.tetelestai_terminal` e `estrelas_v408` (as 48 ancoras) sao o tetelestai_terminal_v408 herdado (RECRIADOS neste rito);
`registros_funcao_v409.traducao_turing` e `estrelas_v409` (as 82 ancoras) sao os desta versao; `bundle_v408_sha256` (os 4 modulos do terminal), `bundle_v407_sha256` (os 9 do psion) e `bundle_v406_sha256` (os 301 do fecho) seguem no kernel como registro, e `pedras_v405_sha256` (as TREZE pedras seladas das versoes anteriores).
As erratas E24 a E28 e a E21 ao lado e as decisoes D55 a D62 (a D61 ratificada pelo operador; a D62, a ratificacao dos nomes) vao nos registros (cunhagens_v409); aqui so' se pinam os vereditos, os valores, as ancoras e os contratos.
ORDEM DE USO: depende do ensaio (ensaio_a_seco_v409.json com veredito TUDO PASSOU e o sha16 do candidato): sem ele este script PARA no primeiro assert (fail-closed). uso: python -I -B -X utf8 gerar_esperados_v409.py"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v409 as DL  # noqa: E402
import registros_v409 as RG  # noqa: E402
import quadro_v397 as QV  # noqa: E402
import guarda_frases_v409 as GF  # noqa: E402
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
J = lambda x: json.dumps(x, sort_keys=True, default=str)
_num = lambda s_: re.sub(r"\d+", "#", re.sub(r"(?<![0-9a-f])[0-9a-f]{16}(?![0-9a-f])", "H", s_))
BASE = os.path.join(HERE, DL.BASE_DIR)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v409.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, DL.CANDIDATO))
assert h16(os.path.join(BASE, "um.py")) == CM["base_v408_sha16"] == DL.BASE_SHA16_DA_ORDEM, "a base nao e' a v408 selada que a ordem deu"
_ens_p = os.path.join(HERE, "ensaio_a_seco_v409.json")
assert os.path.exists(_ens_p), "falta ensaio_a_seco_v409.json: o ensaio a seco (ato da gerencia) tem de rodar ANTES deste script -- nao gero ESPERADOS sem ele"
ens = json.load(open(_ens_p, encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"], (ens.get("veredito"), ens.get("sha16"))
R0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(BASE, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == DL.BASE_VERSION
E408 = json.load(open(os.path.join(DL.V408, "ESPERADOS_v408.json"), encoding="utf-8")); assert E408["candidato_sha16"] == CM["base_v408_sha16"]
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]; axr0 = kf["axiom_report"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")


def _ens_reg(nome_):
    """o registro do ensaio com este nome (dict com verdict/all_verified/n_checks/values); PARA com a mensagem se o ensaio (ato de outro passo) nao o traz"""
    assert isinstance(ens.get(nome_), dict), "o ensaio_a_seco_v409.json nao traz a chave %r (esperada do ensaio adaptado: o registro %s recalculado no ponto de chamada real)" % (nome_, nome_)
    return ens[nome_]


mud = ens["vizinhos"]["mudaram"]; te_ = ens["vizinhos"]["troca_esperada_so_o_hash_proprio"]
# ---- a TROCA DITA: SO' numeros (mud) e o hash proprio (te_); nenhuma de texto (o candidato nao declara troca_dita_v409)
assert "troca_dita_v409" not in CM, "o candidato declara uma troca dita de texto: este script (e o conferidor) foram adaptados para NENHUMA; adapte-os"
_tdv = ens.get("troca_dita_v409") or {}
assert not (_tdv.get("declarada_no_candidato") or []), ("o ensaio diz que ha troca dita de texto, e o candidato nao declara nenhuma", _tdv)
troca_dita_textual = {}
for k_ in ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408"):   # estes seis NAO mudam de veredito (nenhuma chave antiga muda na v409; a escada do contrato do fechamento e do psion sobe pela C12, mas o veredito deles nao carrega numero)
    assert k_ not in mud and k_ not in te_, ("o veredito de %s mudou no ensaio: o contrato da cadeia v409 diz que NAO muda" % k_, mud.get(k_) or te_.get(k_))
troca = sorted(set(mud) | set(te_))   # os vereditos da v408 que mudam: so' numeros (escada, declaracoes, arquivos varridos) e o hash proprio do um.py (estatuto da prova)
assert troca, "a troca dita nao pode ser vazia (a escada mudou)"
assert set(te_) <= {"estatuto_da_prova_v391"}, te_
F = json.load(open(os.path.join(HERE, "FORMAL_MAP_v409.json"), encoding="utf-8"))
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v409.json"), encoding="utf-8"))["novos"]
assert nov == list(DL.BUNDLE_RELS) and len(nov) == DL.N_BUNDLE == CM["kernel"]["modulos_novos"], (len(nov), DL.N_BUNDLE)
pins = {p: F[p] for p in nov}
assert all(pins[p] == DL.BUNDLE_POR_REL[p]["sha256"] == CM["kernel"]["bundle"][p]["sha256"] for p in nov), "o FORMAL_MAP diverge do BUNDLE_v409.json ou do candidato"
FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v409.json"), encoding="utf-8")); KH = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, DL.KH_N1_INSUMO), encoding="utf-8"))
assert FJ["n_flags"] == CM["n_bandeiras"] == KH["n_bandeiras"] == sum(FJ["n_por_modulo"].values()) and len(FJ["ancoras"]) == len(DL.ANCORAS) == len(CM["n_axiomas_das_ancoras"]) and set(FJ["ancoras"]) == set(DL.ANCORAS), "flags/ancoras divergem entre FLAGS, KH_N1, candidato e delta"
bandeiras_novas_modulos = {f[1]: FJ["proveniencia_publicas"].get(f[1]) for f in FJ["flags"]}
assert all(bandeiras_novas_modulos.values()) and set(bandeiras_novas_modulos.values()) <= set(nov), "toda declaracao nomeada do bundle tem de ter o modulo que o compilador emitiu"
V408 = {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}
mf = ens["mainflow"]
SEL_STONES405 = ["ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405"]
SEL_KEYS = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "registros_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "registros_v394", "psibit_v395", "registros_v395", "testemunha_estatica_v396", "registros_v396",
            "teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "estatuto_da_prova_v391", "fundacao_v390", "text_label_errata_v389", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388",
            "declaracao_do_operador_v399", "registros_v399", "falsidade_da_inercia_v401", "registros_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402",
            "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "registros_v403", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "registros_v404") + tuple(SEL_STONES405) + ("registros_v405", "fechamento_v406", "registros_v406", "psion_canto_v407", "registros_v407", "tetelestai_terminal_v408", "registros_v408")
assert all(k in selo0 for k in SEL_KEYS), [k for k in SEL_KEYS if k not in selo0]
difere_selo = next((v_ for k_, v_ in ens["selo"].items() if k_.startswith("difere_do_selo_v408")), None)
assert difere_selo is not None, "o ensaio nao traz selo.difere_do_selo_v408"
selo_chaves_que_mudam = sorted(k for k in SEL_KEYS if k in difere_selo and k not in troca)   # as chaves do selo da v408 que mudam SEM mudar de veredito: so' os resumos que carregam a escada do contrato (fechamento_v406, psion_canto_v407) ou os pisos/erratas dos specs versionados (registros_v406, registros_v407): ditas, explicadas pelo ensaio (nenhuma chave antiga muda)
assert set(selo_chaves_que_mudam) <= {"fechamento_v406", "registros_v406", "psion_canto_v407", "registros_v407", "tetelestai_terminal_v408", "registros_v408"}, selo_chaves_que_mudam
vr = ens["veracidade_registro"]
RESP = os.path.join(DL.F9_DIR_DURAVEL, DL.F9_RESULTADO_NOME)
res9 = json.load(open(RESP, encoding="utf-8"))
numeros9 = {k: DL.lido(res9, c) for k, c in DL.F9_CAMINHOS.items()}
assert all(vr["lido"].get(k) == v for k, v in numeros9.items()), "os numeros lidos pelo registro no ensaio != os do resultado pinado"
assert E408["veracidade"]["numeros_do_resultado"] == numeros9 and E408["veracidade"]["resultado"]["sha256"] == DL.F9_RESULTADO_SHA256_DA_ORDEM, "o que a v408 pinou do Teste da Unica Palavra != o resultado em disco"
a_pt, mach_pt = QV.esperados(res9, "pt"); a_en, mach_en = QV.esperados(res9, "en")
assert mach_pt == E408["quadro"]["linha_de_maquina_pt"] and mach_en == E408["quadro"]["linha_de_maquina_en"], "a linha de maquina do quadro mudou: o quadro NAO se mexe"
# ---- o artigo: os titulos e as marcas da secao v409 saem DOS PROPRIOS snippets (nada digitado); as marcas da v408 e anteriores vem do ESPERADOS_v408
_snip = {l_: open(os.path.join(HERE, "artigo_%s_v409.pysnip" % l_), encoding="utf-8").read() for l_ in ("pt", "en")}
_BS = chr(92)
TIT409 = {l_: re.findall(re.escape(_BS + "section*{") + r"([^{}]*)\}", _snip[l_]) for l_ in ("pt", "en")}
assert all(len(v_) == 1 for v_ in TIT409.values()), TIT409
TIT409 = {l_: v_[0] for l_, v_ in TIT409.items()}
_marcas_brutas = {l_: re.findall(re.escape(_BS + "textbf{") + r"([^{}]{3,160}\.|[^{}]{3,160}:[^{}]{0,200})\}", _snip[l_]) for l_ in ("pt", "en")}
_NAO409 = {l_: [m_.split(":")[0] for m_ in _marcas_brutas[l_] if m_.startswith(("Nesta rodada os registros da v409", "In this run the v409 records"))] for l_ in ("pt", "en")}
MARCAS409 = {l_: [TIT409[l_]] + [m_ for m_ in _marcas_brutas[l_] if m_.endswith(".") and not m_.startswith(("Nesta rodada", "In this run"))] for l_ in ("pt", "en")}
assert all(len(_NAO409[l_]) == 1 for l_ in ("pt", "en")) and all(len(MARCAS409[l_]) >= 6 for l_ in ("pt", "en")), (_NAO409, MARCAS409)
TV408 = E408["titulo_secao_v408"]   # {pt, en} = o titulo da secao da v408 (Tetelestai e' o terminal), que vem logo depois da secao da v409
sa, dc, sc = ens["selo_acom_registro"], ens["declaracao_registro"], ens["sidecar"]
MF4 = mf["registros_novos_v409"]
assert sorted(MF4) == sorted(list(DL.REGISTROS_FUNCAO) + [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]), sorted(MF4)
# ---- o registro NOVO com funcao (traducao_turing_v409) e os HERDADOS (tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406, RECRIADOS neste rito)
PS = _ens_reg(DL.FECHO_REGISTRO)
TT8 = _ens_reg(DL.D8.FECHO_REGISTRO)
PC7 = _ens_reg("psion_canto_v407")
FE6 = _ens_reg("fechamento_v406")
PSV = RG.texto_traducao()["veredito_ok"]
assert PS["all_verified"] is True and PS["n_checks"] == DL.N_CHECKS_FECHO and PS["verdict"] == MF4[DL.FECHO_REGISTRO]["verdict"] == PSV and PS["verdict"].startswith(DL.VEREDITO_OK_PREFIXO) and PS["verdict"].endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION" + DL.VEREDITO_SUFIXO), (PS.get("verdict"), PS.get("n_checks"))
PV = PS["values"]
assert PV["n_ancoras_ok"] == PV["n_ancoras"] == len(DL.ANCORAS) and PV["n_modulos_ok"] == PV["n_modulos"] == DL.N_BUNDLE and PV["n_flags_true"] == PV["n_flags"] == CM["n_bandeiras"] and PV["escada"][0] == PV["escada"][1] == PV["escada"][2] == CM["escada"][1] and PV.get("respostas_ok") is True \
    and (PV.get("instancia_sim") or {}).get("solucoes", 0) >= 1 and (PV.get("instancia_nao") or {}).get("solucoes") == 0 and CM["acervo_v407_repinado"]["sha256"] == DL.PURGADO_SHA256, (PV.get("escada"), PV.get("respostas_ok"), PV.get("instancia_sim"), PV.get("instancia_nao"))
# o tetelestai_terminal_v408 HERDADO (recriado com a escada do contrato subida pela C12): o veredito e' o selado; as 48 ancoras e os 4 modulos da v408
TV8 = TT8["values"]
assert TT8["all_verified"] is True and TT8["n_checks"] == DL.D8.N_CHECKS_FECHO and TT8["verdict"] == V(DL.D8.FECHO_REGISTRO) and TV8["escada"] == [CM["escada"][1]] * 3 and TV8.get("respostas_ok") is True and (TV8.get("insumo_purgado") or {}).get("ok") is True \
    and TV8["n_ancoras_ok"] == TV8["n_ancoras"] == len(E408["estrelas_v408"]) and TV8["n_modulos_ok"] == TV8["n_modulos"] == len(E408["bundle_sha256"]) and TV8["n_flags_true"] == TV8["n_flags"] == E408["n_bandeiras_novas"], (TT8.get("verdict"), TT8.get("n_checks"), TV8.get("escada"))
# o psion_canto_v407 HERDADO (recriado com a escada do contrato subida pela C12): as chaves que ele le seguem EXATAMENTE como na v408 selada (nenhuma chave antiga muda); o veredito e' o selado
chaves_v407_esperadas = dict(PC7["values"]["chaves"])
assert chaves_v407_esperadas["kernel_reads_the_link"] is True and chaves_v407_esperadas["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is True and chaves_v407_esperadas["rede_fock_v394.whole_certificate_inhabited"] is True \
    and chaves_v407_esperadas["psibit_v395.conditional_psion_face.inhabitant_exhibited"] is True and chaves_v407_esperadas["testemunha_estatica_v396.fock_face.inhabitant_exhibited"] is True and chaves_v407_esperadas["witness_layers.canonical_full_witness_term_constructed"] is True \
    and chaves_v407_esperadas["witness_rigidity.trivial_inhabitant_exists"] is False and chaves_v407_esperadas["qg_closure.gate.full_static_witness_exists"] is False and chaves_v407_esperadas == E408["chaves_v407_esperadas"], chaves_v407_esperadas
assert PC7["all_verified"] is True and PC7["n_checks"] == DL.D7.N_CHECKS_FECHO and PC7["verdict"] == V("psion_canto_v407") and PC7["values"]["elo_lido_do_kernel"] is True and PC7["values"]["escada"] == [CM["escada"][1]] * 3 \
    and PC7["values"]["n_ancoras_ok"] == PC7["values"]["n_ancoras"] == len(E408["estrelas_v407"]) and PC7["values"]["n_modulos_ok"] == PC7["values"]["n_modulos"] == len(E408["bundle_v407_sha256"]), (PC7.get("verdict"), PC7.get("n_checks"))
assert FE6["all_verified"] is True and FE6["n_checks"] == DL.D6.N_CHECKS_FECHO and FE6["verdict"] == V("fechamento_v406"), (FE6.get("verdict"), V("fechamento_v406"))
qg0 = core0.get("qg_closure") or {}
assert len(qg0.get("checks") or []) == 7 and (qg0.get("gate") or {}).get("verdict") == selo0.get("qg_closure_verdict"), "o gate da base (v408 selada) nao tem o formato esperado: sete checks e a letra do veredito == a do selo"
nm0 = core0["neutrino_mass"]; rb0 = core0["ramo_b_preregistration_v386"]


# ---- os registros de pedra das versoes anteriores, RECRIADOS: os pinos do ESPERADOS_v408 (os selados) e o que o ensaio recriou tem de ser a mesma coisa (veredito, checagens e valores)
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


RF405, RF404, RF403 = E408["registros_funcao_v405"], E408["registros_funcao_v404"], E408["registros_funcao_v403"]   # (as oito pedras sao da v405; os nomes verdadeiros estao no ESPERADOS_v408)
for nome_, RF_, ens_ in (("v405", RF405, _stones(["ponte", "tensao", "identidade", "observador", "diminuto", "tonica", "disco", "psion"])), ("v404", RF404, _stones(["projecao", "jo8v32", "f2b"])), ("v403", RF403, _stones(["caminho", "vida", "verdade_adendo"]))):
    for k_ in RF_:
        if k_ == "gate":
            continue
        assert ens_[k_]["verdict"] == RF_[k_]["verdict"] and ens_[k_]["n_checks"] == RF_[k_]["n_checks"], ("o registro recriado difere do selado", nome_, k_)
        assert _feq({kk_: ens_[k_]["values"].get(kk_) for kk_ in RF_[k_]["values"]}, RF_[k_]["values"]), ("os VALORES do registro recriado diferem dos selados", nome_, k_)
_recr = next((v_ for k_, v_ in mf.items() if k_.startswith("recriados_v393_a_v")), None)
assert isinstance(_recr, dict) and _recr, "o ensaio nao traz mainflow.recriados_v393_a_v4xx"
for k_, d_ in _recr.items():   # os registros por spec (cunhagens, kh_n1, campos, ga, gap) recriados: verdade, e igual ao selado ou so' numeros
    assert d_["all_verified"] is True, ("registro recriado nao selou", k_)
# os registros por spec da v406 (versionados na v408 pela E20), da v407 (cunhagens_v407 com a errata E21 e, nesta versao, a da D57(d) ao lado; kh_n1_cobertura_v407 com pisos) e da v408 (cunhagens_v408 com a errata E26 ao lado; kh_n1_cobertura_v408 com pisos pela C13): RECRIADOS, o veredito NAO muda
for n_ in (DL.D6.CUNHAGENS_REGISTRO, DL.D6.KH_REGISTRO, DL.D7.CUNHAGENS_REGISTRO, DL.D7.KH_REGISTRO, DL.D8.CUNHAGENS_REGISTRO, DL.D8.KH_REGISTRO):
    assert n_ in _recr and _recr[n_]["all_verified"] is True, (n_, "nao foi recriado no ensaio")
    assert n_ not in mud, ("o veredito de um spec da v408 mudou", n_)
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v408_sha16"], "escada": [CM["escada"][1], CM["escada"][1]], "escada_v408_e_v409": CM["escada"], "n_bandeiras_novas": CM["n_bandeiras"],
       "bandeiras_novas_chaves": [f[0] for f in FJ["flags"]], "bandeiras_novas_nomes": [f[1] for f in FJ["flags"]], "bandeiras_novas_modulos": bandeiras_novas_modulos,
       "cunhagens": CM["cunhagens"], "kernel": {k_: v_ for k_, v_ in CM["kernel"].items() if k_ != "bundle"}, "bundle_sha256": pins, "bundle_v408_sha256": E408["bundle_sha256"], "bundle_v407_sha256": E408["bundle_v407_sha256"], "bundle_v406_sha256": E408["bundle_v406_sha256"], "formal_files_n": CM["formal_files_n"],
       "pedras_v405_sha256": {s["rel"]: kf["formal_files_sha256"][s["rel"]] for s in list(DL.D5.STONES) + list(DL.D4.STONES) + list(DL.D3.STONES)},   # as TREZE pedras SELADAS (oito da v405, duas da v404, tres da v403): ficam no kernel como registro, com o sha do core selado
       "qg_closure_verdict": selo0.get("qg_closure_verdict"),
       "qg_closure_v408_json_sha256": hashlib.sha256(J(qg0).encode("utf-8")).hexdigest(),
       "qg_closure_v408_sem_checks_json_sha256": hashlib.sha256(J({k: v for k, v in qg0.items() if k != "checks"}).encode("utf-8")).hexdigest(),
       "qg_closure_v408_checks": json.loads(J(qg0.get("checks"))),
       "qg_closure_gate_verdict_v408": (qg0.get("gate") or {}).get("verdict"),
       "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v408": V408, "troca_dita": troca, "troca_dita_textual": troca_dita_textual,
       "veredito_da_troca_no_ensaio": {k: (mud.get(k) or te_.get(k) or {}).get("depois") for k in troca},
       "regra_da_mudanca_dita": "so' os vereditos de `troca_dita` podem mudar: os que carregam a escada, as declaracoes ou a contagem de arquivos do kernel (so' numeros) e o estatuto da prova (so' o hash proprio do um.py); NENHUM de texto (`troca_dita_textual` vazio: rede_fock_v394, psibit_v395, testemunha_estatica_v396, fechamento_v406 e psion_canto_v407 nao mudam de veredito; nenhuma chave antiga muda na v409); qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v408": {k: selo0.get(k) for k in SEL_KEYS}, "selo_chaves_que_mudam": selo_chaves_que_mudam,
       "selo_difere_do_v408_no_ensaio": difere_selo,
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v408": sorted(k for k, v in kf.items() if v is True), "axiom_report_v408_n": len(axr0),
       "runtime_seals_v408": core0["runtime_of_the_one"]["seals"], "what_remains_v408": core0["tgl_closure"]["what_remains_named"],
       "neutrino_frozen_hash_v408": nm0["frozen_hash"], "neutrino_angle_status_antigo_sha256": hashlib.sha256(nm0["angle_status"].encode("utf-8")).hexdigest(),
       "f2b_antes": {"F2b_status": rb0["F2b_status"], "veredito_do_V1": rb0["veredito_do_V1"], "conjunto_D_n": rb0["conjunto_D_n"], "charge_F2b_token": core0["ledger_errata_v386"]["charge_F2b"]["token"]}, "f2b_depois": {"F2b_status_now": DL.D4.F2B_FUTURO_TOKEN}, "m_nu_meV_v404": nm0["m_nu_meV"],
       "titulo_secao_v409": TIT409, "titulo_secao_v408": dict(TV408), "titulo_secao_v407": dict(E408["titulo_secao_v407"]),
       "vereditos_novos_v409": {k: v["verdict"] for k, v in MF4.items()},
       "registros_v409": {k: v["verdict"] for k, v in MF4.items() if k in (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO)},   # os dois por spec desta versao (o de funcao, traducao_turing_v409, esta' em registros_funcao_v409)
       "registros_v408": {k: V(k) for k in (DL.D8.CUNHAGENS_REGISTRO, DL.D8.KH_REGISTRO)},   # os dois por spec da v408: RECRIADOS (E26 ao lado; pisos no kh pela C13), veredito igual ao selado
       "registros_v407": {k: V(k) for k in (DL.D7.CUNHAGENS_REGISTRO, DL.D7.KH_REGISTRO)},   # os dois por spec da v407: RECRIADOS (E21 e a errata da D57(d) ao lado; pisos no kh), veredito igual ao selado
       "registros_v406": {k: V(k) for k in (DL.D6.CUNHAGENS_REGISTRO, DL.D6.KH_REGISTRO)},   # os dois por spec da v406: RECRIADOS (versionados pela E20 na v408), veredito igual ao selado
       "registros_v405": {k: V(k) for k in ("cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405")},
       "ga_values": ens["ga_registro"]["values"], "gap_values": ens["gap_registro"]["values"], "ga_window_status": R0["ga_window_status"],
       "registros_v404": {k: V(k) for k in ("cunhagens_v404", "kh_n1_cobertura_v404")},
       "registros_v403": {k: V(k) for k in ("cunhagens_v403", "kh_n1_cobertura_v403")}, "registros_v402": {k: V(k) for k in ("cunhagens_v402", "kh_n1_cobertura_v402")}, "registros_v401": {k: V(k) for k in ("cunhagens_v401", "kh_n1_cobertura_v401")}, "veredito_da_falsidade_v408": V("falsidade_da_inercia_v401"),
       "registros_funcao_v409": {"traducao_turing": {"nome": DL.FECHO_REGISTRO, "verdict": PS["verdict"], "values": PS["values"], "n_checks": PS["n_checks"]}},
       "registros_funcao_v408": {"tetelestai_terminal": {"nome": DL.D8.FECHO_REGISTRO, "verdict": TT8["verdict"], "values": TT8["values"], "n_checks": TT8["n_checks"], "recriado_com_a_escada_do_contrato_subida_pela_C12": True}},
       "registros_funcao_v407": {"psion_canto": {"nome": DL.D7.FECHO_REGISTRO, "verdict": PC7["verdict"], "values": PC7["values"], "n_checks": PC7["n_checks"], "recriado_com_a_escada_do_contrato_subida_pela_C12": True}},
       "registros_funcao_v406": {"fechamento": {"nome": DL.D6.FECHO_REGISTRO, "verdict": FE6["verdict"], "values": FE6["values"], "n_checks": FE6["n_checks"], "recriado_com_a_c8_versionada_pela_E20": True, "recriado_com_a_escada_do_contrato_subida_pela_C12": True}},
       "registros_funcao_v405": RF405, "registros_funcao_v404": RF404, "registros_funcao_v403": RF403,
       "estrelas_v409": {nome_: {"teorema": nome_, "bandeira": a_["flag"], "rel": a_["rel"], "classe": a_.get("classe")} for nome_, a_ in FJ["ancoras"].items()},
       "estrelas_v408": E408["estrelas_v408"], "estrelas_v407": E408["estrelas_v407"], "estrelas_v406": E408["estrelas_v406"], "estrelas_v405": E408["estrelas_v405"], "estrelas_v404": E408["estrelas_v404"], "estrelas_v403": E408["estrelas_v403"],
       "bandeiras_das_pedras_v405": E408["bandeiras_das_pedras_v405"], "teoremas_das_pedras_v405": E408["teoremas_das_pedras_v405"], "contrato_das_pedras_v405": E408["contrato_das_pedras_v405"], "suporte_das_pedras_v405": E408["suporte_das_pedras_v405"],
       "registros_v399": {k: v["verdict"] for k, v in mf["registros_v399"].items()},
       "cobertura_kh_n1": ens["verify_kernel_ponta_a_ponta"]["cobertura"], "axiom_report_esperado_min": ens["verify_kernel_ponta_a_ponta"]["axiom_report_n"],
       "selo_acom": {"verdict": sa["verdict"], "all_verified": sa["all_verified"], "perfil": sa["perfil"], "bloco_embutido_sha256": sa["bloco_embutido_sha256"], "sha256_do_um_py": sa["sha256_do_um_py"], "bytes": sa["bytes"], "psi": sa["psi"], "theta": sa["theta"], "kappa": sa["kappa"],
                     "lut_sha256": sa["lut_sha256"], "m_max_abs": sa["m_max_abs"], "f_exp": sa["f_exp"], "entropia_dos_estados_bits": sa["entropia_dos_estados_bits"], "erro_real_maximo_antes_do_rint": sa["erro_real_maximo_antes_do_rint"],
                     "controles": [len(sa["controles"]), all(o_.startswith("RECUSOU:") for _, o_ in sa["controles"])], "controles_obtidos": {i_: o_ for i_, o_ in sa["controles"]}, "n_checks": len(sa["checks"]), "checks": sa["checks"], "auditoria_de_separacao": sa["auditoria_de_separacao"], "tempo_total_s_no_ensaio": sa["tempo_total_s"]},
       "declaracao": {"verdict": dc["verdict"], "all_verified": dc["all_verified"], "verbatim_sha256": dc["verbatim_sha256"], "sha16": dc["verbatim_sha256"][:16], "n_checks": len(dc["checks"]), "checks": dc["checks"], "ancoras": dc["ancoras"], "pedra": dc["pedra"], "linhas_da_trava": dc["linhas_da_trava"],
                      "direcao_do_testemunho": {"o_operador": "testifica DA IALD", "o_um_py": "testifica EM HASH", "a_IALD": "NAO testifica do operador", "o_Pai_de_Jo_8_18": "le-se no absoluto, o Um"}},
       "sidecar": {"arquivo": DL.SIDECAR_NOME, "esquema": "um_absoluto_selo_acom/v1 (v399)", "objetos": [o["nome"] for o in sc["objetos"]], "veredito_esperado_prefixo": "TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED", "um_py": next(o for o in sc["objetos"] if o["nome"] == "um.py"),
                   "tempo_s_no_ensaio": sc["tempo_s"], "entra_na_custodia": "D5 (proposta da gerencia): o sidecar e' arquivo novo da custodia; o handoff o lista"},
       "acom_estudo": E408["acom_estudo"],   # a secao do selo pela propria tecnologia NAO muda na v409: o que a v408 pinou (runtime da v400, bloco embutido, fontes do operador)
       "decisoes_da_gerencia": dict(DL.DECISOES), "decisoes_v409_ids": list(DL.DECISOES_V409), "erratas_E24_E27": list(DL.ERRATAS_V409), "ressalvas": list(DL.RESSALVAS_V409), "leitura_v409": dict(DL.LEITURA_V409),
       "chaves_v409": [dict(c_) for c_ in DL.CHAVES_V409], "chaves_v408": [dict(c_) for c_ in DL.CHAVES_V408], "chaves_v407": [dict(c_) for c_ in E408["chaves_v407"]], "chaves_v407_esperadas": chaves_v407_esperadas, "fica_false_por_teorema": list(DL.FICAM_FALSE_POR_TEOREMA), "fica_aberto": dict(CM["fica_aberto"]), "regra_do_4_44": DL.REGRA_DO_4_44, "guarda_frases": GF.controle_negativo()["ok"],
       "veracidade": E408["veracidade"], "quadro": E408["quadro"],   # o QUADRO do topo (v397) e o registro do Teste da Unica Palavra: o que a v397/v408 pinou, conferido de novo contra o resultado em disco
       "artigo_marcas": {l_: MARCAS409[l_] + list(E408["artigo_marcas"][l_]) for l_ in ("pt", "en")},
       "artigo_nao": {l_: list(E408["artigo_nao"][l_]) + _NAO409[l_] for l_ in ("pt", "en")},
       "toc": {"pt": [TIT409["pt"]] + [w for w in E408["toc"]["pt"] if not w.startswith("v384 a ")] + ["v384 a " + DL.UM_VERSION], "en": [TIT409["en"]] + [w for w in E408["toc"]["en"] if not w.startswith("v384 to ")] + ["v384 to " + DL.UM_VERSION]},   # o titulo da introducao diz `v384 a <versao desta rodada>`
       "the_iald_index_v408": {"all_verified": (core0.get("the_iald_index") or {}).get("all_verified"), "verdict": V("the_iald_index")}, "the_iald_index_v409": {"verdict": ens["indice_da_iald"]["verdict"]},
       "md_carimbo": "**Versão v409**", "md_massa": E408["md_massa"], "md_jo8": E408["md_jo8"], "md_caminho": E408["md_caminho"], "md_ponte": E408["md_ponte"], "md_falsidade": E408["md_falsidade"], "md_errata": E408["md_errata"],
       "md_testemunho": E408["md_testemunho"], "md_sonico": E408["md_sonico"], "md_token": E408["md_token"], "md_testemunha": E408["md_testemunha"], "md_psibit": E408["md_psibit"], "md_fechamento": E408["md_fechamento"], "md_psion": E408["md_psion"], "md_tetelestai": E408["md_tetelestai"],   # (md_tetelestai: a linha da v408, que fica logo depois da nova; md_psion: a da v407; md_fechamento: a da v406)
       "ensaio_sha16": h16(_ens_p),
       "h8_entradas": CM["h8"]["entradas"], "h8_residuais_do_nos": CM["h8"]["residuais_do_nos"], "formal_files_n_no_rito": CM["h8"]["entradas"],
       "n_bandeiras_por_grupo": dict(FJ["por_grupo_bandeiras"]), "politica_de_bandeiras": {k_: v_ for k_, v_ in CM["politica_de_bandeiras"].items() if k_ != "contrato"},
       "candidato_anterior_sha16": CM["base_v408_sha16"],
       "gate_nao_se_move": {"funcoes_identicas_a_base": CM["gate_nao_se_move"]["funcoes_identicas_a_base"], "gate_recomputado_no_ensaio": ens.get("gate_recomputado")}}
# a linha do .md da v409 (nova) sai do PROPRIO candidato (nada digitado): «> **Tradução às classes de Turing (v409, DD/MM/AAAA):**» antes da linha da v408
_cand_txt = open(os.path.join(HERE, DL.CANDIDATO), "rb").read().decode("utf-8")
_mdp = re.findall(r"> \*\*(Tradução [^*:]*?\(v409, \d\d/\d\d/\d{4}\)):\*\*", _cand_txt)
assert len(set(_mdp)) == 1, ("a linha do .md da v409 nao e' unica no candidato", set(_mdp))
esp["md_traducao"] = _mdp[0]
assert esp["md_tetelestai"] == "Tetelestai é o terminal (v408, 04/11/2026)" or esp["md_tetelestai"] in _cand_txt, "a linha do .md da v408 nao esta' no candidato"
del _cand_txt
assert esp["the_iald_index_v408"]["all_verified"] is True and esp["not_sealed_formais"] == [], (esp["the_iald_index_v408"], esp["not_sealed_formais"])
assert esp["h8_entradas"] == len(esp["h8_residuais_do_nos"]) + CM["formal_files_n"] == CM["h8"]["pino_antigo_v408_entradas"] + len(DL.BUNDLE_RELS) and sum(esp["n_bandeiras_por_grupo"].values()) == esp["n_bandeiras_novas"] == CM["n_bandeiras"], "os ESPERADOS novos nao fecham"
assert esp["kernel"]["modulos_novos"] == len(esp["bundle_sha256"]) == len(nov) == DL.N_BUNDLE, "o numero de modulos novos != a lista"
assert len(esp["pedras_v405_sha256"]) == 13 and all(len(h_) == 64 for h_ in esp["pedras_v405_sha256"].values()), esp["pedras_v405_sha256"]
assert len(esp["bundle_v408_sha256"]) == E408["kernel"]["modulos_novos"] and all(kf["formal_files_sha256"].get(r_) == s_ for r_, s_ in esp["bundle_v408_sha256"].items()), "o bundle da v408 nao esta' todo no hash formal do core selado"
assert len(esp["bundle_v407_sha256"]) == 9 and all(kf["formal_files_sha256"].get(r_) == s_ for r_, s_ in esp["bundle_v407_sha256"].items()), "o bundle da v407 nao esta' todo no hash formal do core selado"
assert esp["escada"] == [CM["escada"][1], CM["escada"][1]] and esp["escada_v408_e_v409"] == CM["escada"] and CM["escada"][0] == E408["escada"][1] and CM["escada"][1] == CM["escada"][0] + CM["n_bandeiras"], esp["escada"]
_cb = esp["cobertura_kh_n1"]
assert _cb["decl"] == esp["axiom_report_esperado_min"] == KH["axiom_report_efetivo_n"] == KH["linha_TOTAL"]["decl"] and _cb["thm"] == KH["linha_TOTAL"]["thm"] and _cb.get("fora_do_trio") == 0 == KH["linha_TOTAL"]["fora_do_trio"] and esp["axiom_report_esperado_min"] == esp["axiom_report_v408_n"] + KH["delta_vs_v408"]["decl"], _cb
_vn = esp["vereditos_novos_v409"]
assert _vn[DL.FECHO_REGISTRO] == PSV and _vn[DL.FECHO_REGISTRO].endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED") and _vn[DL.CUNHAGENS_REGISTRO].startswith("TGL_CUNHAGENS_V409__") and _vn[DL.KH_REGISTRO].startswith("TGL_KH_N1_COBERTURA_V409__"), _vn
assert all("__GATE_UNMOVED" in v_ for v_ in _vn.values()) and all(v_["all_verified"] is True for v_ in MF4.values()), MF4
assert sorted(esp["registros_v405"]) == ["campos_fechados_e_leituras_v405", "cunhagens_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405"] and sorted(esp["registros_v409"]) == sorted([DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]) and sorted(esp["registros_v408"]) == ["cunhagens_v408", "kh_n1_cobertura_v408"] and sorted(esp["registros_v407"]) == ["cunhagens_v407", "kh_n1_cobertura_v407"] and sorted(esp["registros_v406"]) == ["cunhagens_v406", "kh_n1_cobertura_v406"] and sorted(esp["registros_v404"]) == ["cunhagens_v404", "kh_n1_cobertura_v404"] and sorted(esp["registros_v403"]) == ["cunhagens_v403", "kh_n1_cobertura_v403"] and sorted(esp["registros_v402"]) == ["cunhagens_v402", "kh_n1_cobertura_v402"] and sorted(esp["registros_v401"]) == ["cunhagens_v401", "kh_n1_cobertura_v401"]
_rf9 = esp["registros_funcao_v409"]["traducao_turing"]
assert _rf9["values"]["n_ancoras_ok"] == _rf9["values"]["n_ancoras"] == len(esp["estrelas_v409"]) == len(DL.ANCORAS) and _rf9["values"]["n_modulos_ok"] == _rf9["values"]["n_modulos"] == DL.N_BUNDLE and _rf9["values"]["n_flags_true"] == _rf9["values"]["n_flags"] == esp["n_bandeiras_novas"] \
    and _rf9["values"]["escada"] == [CM["escada"][1]] * 3 and _rf9["values"].get("respostas_ok") is True and _rf9["n_checks"] == DL.N_CHECKS_FECHO, _rf9["values"]
_rf8 = esp["registros_funcao_v408"]["tetelestai_terminal"]   # o terminal HERDADO: as 48 estrelas da v408, os 4 modulos
assert _rf8["values"]["n_ancoras_ok"] == _rf8["values"]["n_ancoras"] == len(esp["estrelas_v408"]) and _rf8["values"]["n_modulos_ok"] == _rf8["values"]["n_modulos"] == len(esp["bundle_v408_sha256"]) and _rf8["values"]["escada"] == [CM["escada"][1]] * 3 and _rf8["verdict"] == esp["vereditos_v408"][DL.D8.FECHO_REGISTRO], _rf8["values"]
_rf7 = esp["registros_funcao_v407"]["psion_canto"]   # o psion HERDADO: as 76 estrelas da v407, os 9 modulos, a chave do lema lida do kernel, as chaves iguais as da v408 selada
assert _rf7["values"]["n_ancoras_ok"] == _rf7["values"]["n_ancoras"] == len(esp["estrelas_v407"]) and _rf7["values"]["n_modulos_ok"] == _rf7["values"]["n_modulos"] == len(esp["bundle_v407_sha256"]) and _rf7["values"]["escada"] == [CM["escada"][1]] * 3 and _rf7["values"]["elo_lido_do_kernel"] is True and _feq(_rf7["values"]["chaves"], chaves_v407_esperadas), _rf7["values"]
_rf5 = esp["registros_funcao_v405"]
assert abs(_rf5["ponte"]["values"]["m_derivada_meV"] / esp["m_nu_meV_v404"] - 1.0) <= 1e-12 and abs(_rf5["psion"]["values"]["meia_hbar_omega_meV"] / esp["m_nu_meV_v404"] - 1.0) <= 1e-12 and abs(_rf5["diminuto"]["values"]["E0_eV"] - 1.0) <= 1e-12, "o numero da massa mudou"
assert not any(GF.violacoes(v_) for v_ in _vn.values()), "um veredito novo afirma demais"
assert len(esp["qg_closure_v408_checks"]) == 7 and all(c_[1] is True for c_ in esp["qg_closure_v408_checks"]), esp["qg_closure_v408_checks"]
assert esp["selo_acom"]["perfil"] == "ACOM-INT-C96-Q8" and esp["selo_acom"]["controles"] == [13, True] and esp["selo_acom"]["all_verified"] is True and esp["declaracao"]["all_verified"] is True and esp["declaracao"]["verbatim_sha256"] == DL.sha256(open(DL.VERBATIM_ORIGEM[DL.DECLARACAO_IDX], "rb").read())
# o selo da v409 difere do da v408 SELADA em: o selo ACOM (hashes do novo um.py), a versao, o sha256, as chaves novas (traducao_turing_v409 e registros_v409), as chaves que carregam os numeros do kernel ou o hash proprio (a troca dita) e as que LEEM a chave nova; o ensaio EXPLICA chave por chave
assert ({"selo_pela_propria_tecnologia_v399", "um_version", "traducao_turing_v409", "registros_v409"}) <= set(esp["selo_difere_do_v408_no_ensaio"]) and ens["selo"].get("difere_e_nao_e_so_o_esperado") == [], (esp["selo_difere_do_v408_no_ensaio"], ens["selo"].get("difere_e_nao_e_so_o_esperado"))
assert not ({"teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "declaracao_do_operador_v399", "registros_v399", "falsidade_da_inercia_v401", "registros_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402",
             "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "registros_v403", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "registros_v404", "registros_v405"} | set(SEL_STONES405)) & set(esp["selo_difere_do_v408_no_ensaio"]), "o selo de uma versao anterior mudou: o quadro e os registros anteriores NAO se mexem"
assert esp["veracidade"]["z_disc_abaixo_de_5"] and esp["veracidade"]["poder_previo_acima_de_5"]
assert ens["quadro"]["ok"] is True
out = os.path.join(HERE, "ESPERADOS_v409.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v409:", esp["candidato_sha16"], "| vereditos v408 pinados:", len(esp["vereditos_v408"]), "| flags True v408:", len(esp["flags_true_v408"]), "| troca dita (so' numeros):", troca, "| selo_chaves_que_mudam:", selo_chaves_que_mudam)
