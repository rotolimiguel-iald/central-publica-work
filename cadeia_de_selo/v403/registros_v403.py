# -*- coding: utf-8 -*-
"""registros_v403.py -- os dados dos registros da v403: FONTES pinadas por sha256 (lidas do disco pelo montador, nunca digitadas), VERBATINS (as DUAS falas de 27/10/2026 ainda nao embutidas, ambas do operador; EMBUTIDAS: a fala embutida manda, o arquivo e' so' informativo),
os CONTRATOS e os TEXTOS dos QUATRO registros com FUNCAO (`caminho_v403`, `vida_v403`, `verdade_adendo_v403` e `bandeiras_do_gate_v403`: gerar_candidato_v403.py os emite a partir de runtime_v403.py; cada contrato de pedra sai de contrato() abaixo, DERIVADO do build do sandbox;
o contrato do gate sai de bandeiras_do_gate_v403() abaixo, DERIVADO do AST e do core da v402 SELADA) e os dois SPECS interpretados pelo MOTOR _v392_registro (`cunhagens_v403` e `kh_n1_cobertura_v403`). Fontes so' em pasta DURAVEL: tudo vem de cadeia_de_selo\\v403\\insumos.
Texto novo passa pela guarda P18 (a cada rito). Os NOMES (Caminho, Vida, VerdadeAdendo) sao do operador (27/10/2026); as pedras da v402 FICAM como registro. Molde: registros_v402.py."""
import ast, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v403 as DL  # noqa: E402
import runtime_v403 as RT  # noqa: E402   (so' as funcoes puras: _v403_ast_do_gate le o codigo do gate; nada do um.py e' executado)

INS = os.path.join(HERE, "insumos")
ASSINA = DL.ASSINA
CAMINHO, VIDA, VERDADE = DL.STONE_BY_KEY["caminho"], DL.STONE_BY_KEY["vida"], DL.STONE_BY_KEY["verdade_adendo"]
CHAVE_DE_FONTE = {"caminho": "caminho_pedra", "vida": "vida_pedra", "verdade_adendo": "verdade_adendo_pedra"}

FONTES = [{"chave": CHAVE_DE_FONTE["caminho"], "arquivo": os.path.join(INS, CAMINHO["insumo"]), "papel": "a pedra TGLExt/Caminho.lean (o nome «Caminho» e' do operador, 27/10/2026; compoe por citacao a ponte da escala dual da v402; compilada e provada no sandbox k403c; copia duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)"},
          {"chave": CHAVE_DE_FONTE["vida"], "arquivo": os.path.join(INS, VIDA["insumo"]), "papel": "a pedra TGLExt/Vida.lean (o nome «Vida» e' do operador, 27/10/2026; compoe por citacao a queda sem geometria da v402; compilada e provada no sandbox k403c; copia duravel; a que vale no rito e' a EMBUTIDA no kernel)"},
          {"chave": CHAVE_DE_FONTE["verdade_adendo"], "arquivo": os.path.join(INS, VERDADE["insumo"]), "papel": "a pedra TGLExt/VerdadeAdendo.lean (adendo da pedra Verdade da v392: a esperanca condicional lida pelo Nome; o nome «Verdade» para a esperanca condicional e' do operador, 27/10/2026; compilada e provada no sandbox k403c; copia duravel; a que vale no rito e' a EMBUTIDA no kernel)"},
          {"chave": "kh_n1_v403", "arquivo": os.path.join(INS, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox da v403 (pos_build_kernel_v403.py)"}]


def _trecho(t):
    s = t.strip().splitlines()[0].strip() if t.strip() else ""
    s = s[:48].rstrip()
    assert s and s in t, s
    return s


_VD = DL.verbatins403(os.path.join(INS, "cunhagens"))
VERBATINS = [{"chave": v["chave"], "arquivo": v["arquivo"], "quando": v["quando"], "trechos": [_trecho(v["text"])], "papel": v["papel"], "fonte_original": v["fonte_original"]} for v in _VD]
VERB_CHAVES = [v["chave"] for v in _VD]
SHA16 = {os.path.basename(v["fonte_original"]): v["sha16"] for v in _VD}
S_NOME, S_CONCORDO = tuple(v["sha16"] for v in _VD)          # LIDOS dos arquivos, na ordem de DL.VERBATIM_ORIGEM_V403 (o unpack recusa outro numero)
CH_NOME, CH_CONCORDO = tuple(v["chave"] for v in _VD)
TEXTOS = {v["sha16"]: v["text"] for v in _VD}
CH = lambda id_, desc_, onde_, caminho_, op_, valor_=None, cap_=None, est_="[REAL]": dict(id=id_, descricao=desc_, onde=onde_, caminho=caminho_, op=op_, **({"valor": valor_} if valor_ is not None else {}), **({"capturar": cap_} if cap_ else {}), estatuto=est_)


def _leitura(trecho, sha16, quando="27/10/2026", rotulo="INPUT do operador"):
    assert trecho in TEXTOS[sha16], ("a leitura do operador NAO esta verbatim na fala", sha16, trecho)
    return {"trecho": trecho, "estatuto": "[%s, verbatim %s, sha16 %s]" % (rotulo, quando, sha16)}


# o texto-CONTEXTO que cada registro confere no kernel embutido do proprio rito: o cabecalho da pedra (lido do corpo embutido, nao digitado como prova); conferido tambem NA GERACAO contra o arquivo da pedra
CONTEXTO = {"caminho": {"path": CAMINHO["rel"], "needles": ["# CAMINHO — o nome que o operador deu à ponte da escala dual", "lift_mass_not_selected"]},
            "vida": {"path": VIDA["rel"], "needles": ["# VIDA — o nome que o operador deu à queda sem geometria", "the_fall_is_strictly_anti"]},
            "verdade_adendo": {"path": VERDADE["rel"], "needles": ["# ADENDO da pedra VERDADE", "the_name_reads_the_inscription_as_weights"]}}
for _k, _cx in CONTEXTO.items():
    _src = open(DL.STONE_BY_KEY[_k]["src"], encoding="utf-8", newline="").read()
    assert all(n_ in _src for n_ in _cx["needles"]), ("o texto-contexto NAO esta na pedra", _k)
KEY_STATEMENT = {"caminho": "lift_mass_not_selected /\\ core_positive_realization_exists: two distinct invariants mu^2 give two distinct equivariant realizations with the SAME p+ (the dual scaling law does not select the mass), and every mu^2 >= 0 has a positive realization of the core (p+ > 0, m^2 = mu^2, E > 0): the Way",
                 "vida": "the_fall_is_strictly_anti /\\ a_queda_sem_geometria: s |-> tau(theta_s m) is strictly decreasing (the phase falls, without end) and the whole composition (arrow = sign of s, floor = the post, delivery costs, the angular regime only reads, isotropy a named hypothesis): the Life, the fall without geometry",
                 "verdade_adendo": "diagExpect (identityProj a) = diagonal ![q^2, a^2] in M2(C): the Name (nameOp rho*) reads the inscription of the Truth as its weights; it preserves the One (trace 1) and rereading adds nothing: the Truth read by the Name"}
HIPOTESES_NO_ENUNCIADO = {"caminho": False, "vida": True, "verdade_adendo": True}     # vida: a composicao citada (a_queda_sem_geometria) traz IsotropicPost (nomeada) no enunciado; verdade_adendo: a composicao citada (esperanca_condicional_e_nome) tem o indice 1/b CONDICIONAL a hpp e hopt
VERBATINS_DO_REGISTRO = {"caminho": [CH_NOME, CH_CONCORDO], "vida": [CH_NOME, CH_CONCORDO], "verdade_adendo": [CH_NOME, CH_CONCORDO]}


def contrato(stone, fj, formal_map, e_base, base_sha256):
    """O contrato de UMA pedra (NAO embutido como bloco proprio de verbatins: as falas ficam em _V403_VERBATINS2), DERIVADO do build do sandbox (FLAGS_v403.json = nomes, chaves e a proveniencia dos termos de suporte; formal_map = sha256 das fontes
    embutidas; e_base = a escada da v402 selada; a escada esperada e' a DESTA versao: a da base + as bandeiras das TRES pedras); nada digitado. Vai para CANDIDATO_v403.json e ESPERADOS_v403.json (o conferidor e o pos-rito o leem)."""
    k = stone["key"]
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    faltam = [t for t in stone["contract"] if t not in flag_de]
    assert not faltam, ("teorema do contrato sem bandeira (nao nomeado ou ausente do Audit)", k, faltam[:5])
    assert fj["bandeira_do_teorema_incondicional"][k] == flag_de[stone["theorem"]] and fj["teorema_incondicional"][k] == stone["theorem"]
    assert stone["key_theorem"] in stone["contract"] and stone["theorem"] in stone["contract"]
    sup = dict(fj["suporte_do_contrato"][k]); assert sup == dict(stone["support"]), "os termos de suporte do FLAGS_v403.json diferem dos de delta_v403: " + k
    cit = dict(fj["citados_fora_do_contrato"][k]); assert cit == dict(stone["citados_fora"]), "os termos citados-fora do FLAGS_v403.json diferem dos de delta_v403: " + k
    return {"stone": {"path": stone["rel"], "sha256": formal_map[stone["rel"]], "module": stone["mod"]},
            "unconditional": {"theorem": stone["theorem"], "flag": flag_de[stone["theorem"]]},
            "key_theorem": {"theorem": stone["key_theorem"], "flag": flag_de[stone["key_theorem"]]}, "key_statement": KEY_STATEMENT[k],
            "theorems": {t: flag_de[t] for t in stone["contract"]}, "support": sup, "cited_outside": cit,
            "auxiliaries_outside_the_composition": list(stone["auxiliares_fora_da_composicao"]), "context": dict(CONTEXTO[k]), "named_hypotheses_in_the_statement": HIPOTESES_NO_ENUNCIADO[k],
            "expected_ladder": e_base + fj["n_flags"], "n_flags": fj["nomeadas_por_pedra"][k], "n_flags_total": fj["n_flags"], "verbatins": list(VERBATINS_DO_REGISTRO[k]), "baseline": {"version": DL.BASE_VERSION, "sha256": base_sha256}}


# ---------------------------------------------------------------- o CONTRATO do registro do GATE (F8.1): DERIVADO do AST e do core da v402 SELADA (a base); NA GERACAO, recusa (excecao visivel) se uma bandeira CALCULADA viria False ou se a letra do veredito diverge
def bandeiras_do_gate_v403(T0, core0, selo0):
    """O contrato do registro bandeiras_do_gate_v403. T0 = o texto do um.py da v402 SELADA; core0/selo0 = o core e o selo da v402 SELADA (base_v402). Le o AST do gate (as chaves que o veredito le; os literais do chamador), as tabelas de bandeiras
    (_QG_CERTIFICATE_FLAGS, _QG_PHYSICS_FLAGS, _LEAN_THEOREM_FLAGS) e o core; devolve o dict do contrato. RECUSA com RuntimeError («RECUSO: ...») se: o veredito do selo difere do do core; as contagens nao fecham (18 = 6+6+6; 15 = 6+5+4); as tres literais da base nao sao exatamente as tres da F8.1;
    ou qualquer uma das TRES bandeiras, recalculada da sua fonte NO CORE DA v402 SELADA, viria False (nesse caso o rito da v403 nao teria como selar sem mover o gate: o numero corrige a frase)."""
    tr = ast.parse(T0)
    top = {}
    for n in tr.body:
        if isinstance(n, ast.FunctionDef):
            top[n.name] = n
        elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("_QG_CERTIFICATE_FLAGS", "_QG_PHYSICS_FLAGS", "_LEAN_THEOREM_FLAGS"):
            top[n.targets[0].id] = ast.literal_eval(n.value)
    src_eval = ast.get_source_segment(T0, top["evaluate_quantum_gravity_closure"]); src_prove = ast.get_source_segment(T0, top["prove_qg_closure_gate"])
    lidas, literais = RT._v403_ast_do_gate(src_eval, src_prove)
    def _recusa(msg, det=None):
        raise RuntimeError("RECUSO (bandeiras_do_gate_v403): %s %s" % (msg, "" if det is None else repr(det)[:400]))
    if [len(lidas["formal"]), len(lidas["physics"]), len(lidas["experiment"])] != [6, 5, 4]:
        _recusa("a funcao do veredito da base nao le 6+5+4 bandeiras", {g: len(v) for g, v in lidas.items()})
    qg = core0["qg_closure"]; fam = {"formal": qg["formal_flags"], "physics": qg["physics_flags"], "experiment": qg["experiment_flags"]}
    formal_nomes = list(top["_QG_CERTIFICATE_FLAGS"]); physics_nomes = list(top["_QG_PHYSICS_FLAGS"]) + ["linearized_spin2_finite_face"]; experiment_nomes = list(DL.F81_FEED) + ["protocol_pre_registered", "null_tests_passed_blind"]
    if [sorted(fam[g]) for g in ("formal", "physics", "experiment")] != [sorted(formal_nomes), sorted(physics_nomes), sorted(experiment_nomes)]:
        _recusa("as chaves das 18 bandeiras do core da base diferem das tabelas do programa", {g: sorted(fam[g]) for g in fam})
    if not all(v is True for g in fam for v in fam[g].values()) or sum(len(fam[g]) for g in fam) != 18:
        _recusa("o core da base nao traz as 18 bandeiras True", {g: fam[g] for g in fam})
    if sorted(n for g, n in literais) != sorted(DL.F81_LITERAIS):
        _recusa("os literais do chamador da base nao sao exatamente as tres da F8.1", literais)
    no_veredito = {g: list(lidas[g]) for g in ("formal", "physics", "experiment")}
    informativas = sorted(set(formal_nomes + physics_nomes + experiment_nomes) - set(n for g in no_veredito for n in no_veredito[g]))
    if informativas != sorted(DL.F81_LITERAIS):
        _recusa("as bandeiras que o veredito NAO le nao sao as tres da F8.1", informativas)
    # as TRES fontes, avaliadas NO CORE DA v402 SELADA (a mesma leitura que o rito da v403 fara)
    kf0 = core0["kernel_formalization"]
    ls2 = [k for k in top["_LEAN_THEOREM_FLAGS"] if k.startswith(DL.F81_PREFIXO_LS2)]
    ls2_ladder = None
    for n in ast.walk(top["prove_external_ladder"]):
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "ls2_keys":
            ls2_ladder = ast.literal_eval(n.value)
    if ls2_ladder is None or sorted(ls2) != sorted(ls2_ladder) or len(ls2) != 6:
        _recusa("a familia ext_ls2_* de _LEAN_THEOREM_FLAGS difere de ls2_keys (o termo dLs2 de prove_external_ladder)", [ls2, ls2_ladder])
    f_ls2 = bool(len(ls2) > 0 and all(kf0.get(k) is True for k in ls2))
    pre = [c[1] for c in (core0["void_floor_v11"].get("checks") or []) if isinstance(c, (list, tuple)) and len(c) == 2 and c[0] == DL.F81_ROTULO_PREREG]
    f_pre = bool(len(pre) == 1 and pre[0] is True)
    f_blind = bool(core0["void_stacking_blind"].get("all_verified") is True)
    if not (f_ls2 and f_pre and f_blind):
        _recusa("uma bandeira CALCULADA viria False no core da v402 selada: o rito da v403 nao poderia selar sem mover o gate", {"ext_ls2": f_ls2, "pre_registro_v11": f_pre, "teste_nulo_cego": f_blind})
    gate_v = qg["gate"]["verdict"]
    if gate_v != selo0.get("qg_closure_verdict") or "NATURE_TEST_COMPLETED" not in gate_v:
        _recusa("a letra do veredito do gate no core difere da do selo da base", [gate_v, selo0.get("qg_closure_verdict")])
    feed0 = core0["void_floor_v11"].get("experiment_feed") or {}
    if sorted(feed0) != sorted(DL.F81_FEED) or not all(v is True for v in feed0.values()) or core0["void_floor_v11"].get("verdict") != "TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED":
        _recusa("o feed do V11 da base nao tem as 4 chaves True com o veredito powered", feed0)
    fontes = []
    for n in formal_nomes:
        fontes.append({"grupo": "formal", "nome": n, "no_veredito": n in no_veredito["formal"], "fonte": {"tipo": "termo_lean", "termo": top["_QG_CERTIFICATE_FLAGS"][n], "chave_no_kernel_formalization": "qgc_" + n}})
    for n in physics_nomes:
        if n == "linearized_spin2_finite_face":
            fontes.append({"grupo": "physics", "nome": n, "no_veredito": False, "fonte": {"tipo": "familia_de_bandeiras_do_kernel", "prefixo": DL.F81_PREFIXO_LS2, "n": len(ls2), "bandeiras": list(ls2), "termos_lean": [top["_LEAN_THEOREM_FLAGS"][k] for k in ls2], "origem_no_programa": "o termo dLs2 de prove_external_ladder", "antes_da_v403": "literal True (v75 [KERNEL] informativo)"}})
        else:
            fontes.append({"grupo": "physics", "nome": n, "no_veredito": n in no_veredito["physics"], "fonte": {"tipo": "termo_lean", "termo": top["_QG_PHYSICS_FLAGS"][n], "chave_no_kernel_formalization": "qgp_" + n}})
    for n in experiment_nomes:
        if n in DL.F81_FEED:
            fontes.append({"grupo": "experiment", "nome": n, "no_veredito": n in no_veredito["experiment"], "fonte": {"tipo": "feed_do_rito_V11", "chave": n, "fonte_unica": "o veredito do V11 ser NOT_FALSIFIED_POWERED (GV-03, declarado)"}})
        elif n == "protocol_pre_registered":
            fontes.append({"grupo": "experiment", "nome": n, "no_veredito": False, "fonte": {"tipo": "checagem_de_rito", "rito": "V11", "rotulo": DL.F81_ROTULO_PREREG, "antes_da_v403": "literal True (v67 [hash])"}})
        else:
            fontes.append({"grupo": "experiment", "nome": n, "no_veredito": False, "fonte": {"tipo": "teste_nulo_cego_v73", "chave": "void_stacking_blind.all_verified", "antes_da_v403": "literal True (v73 [dados reais])"}})
    assert len(fontes) == 18 and sum(1 for f in fontes if f["no_veredito"]) == 15
    return {"kind": "gate", "flags": {"formal": formal_nomes, "physics": physics_nomes, "experiment": experiment_nomes}, "no_veredito": no_veredito, "informativas": informativas, "feed": list(DL.F81_FEED), "ls2_flags": list(ls2), "n_ls2": len(ls2),
            "prefixo_ls2": DL.F81_PREFIXO_LS2, "rotulo_prereg": DL.F81_ROTULO_PREREG, "gate_verdict_v402": gate_v, "fontes": fontes, "n_flags": 18, "n_no_veredito": 15, "decomposicao_do_veredito": [6, 5, 4], "decomposicao_de_todas": [6, 6, 6],
            "literais_na_base_v402": sorted(n for g, n in literais), "fontes_avaliadas_no_core_v402": {"ext_ls2": f_ls2, "pre_registro_v11": f_pre, "teste_nulo_cego": f_blind}, "expected_ladder": None}


_NAO_COMUM = ["que isto seja um teste: nao ha desfecho experimental", "que a gravidade quantica esteja creditada na natureza"]
_PENDENCIAS = [{"name": "H_BW", "status": "OPEN", "content": "the rapidity is the Bisognano-Wichmann modular time (2 pi t): the dual action IS the modular group of the wedge"},
               {"name": "H_cal", "status": "OPEN", "content": "this p+ (the canonical core trace) is the energy of ONE body: units and the choice of mu^2"},
               {"name": "H3", "status": "OPEN", "content": "Clausius with conserved T in every null direction"},
               {"name": "signature", "status": "OPEN", "content": "complete positivity gives the induced metric (4,0), not (1,3) (adendo of 03-04/09, debt 1)"},
               {"name": "rank_c_4", "status": "OPEN", "content": "rank c = 4 is a condition (H2), not a consequence (adendo of 03-04/09, debt 2)"}]


def texto_caminho():
    """Os textos do registro caminho_v403 (a funcao do runtime, nao um spec): estatuto, escopo, limites, diz, nao_diz, extras e o veredito de sucesso. Passam pela guarda P18 a cada rito."""
    return {
        "estatuto": "[REAL] os termos do kernel (o item do contrato da pedra Caminho e os 2 termos da ponte da escala dual que a conjuncao cita, lidos a cada rito, no trio: lift_mass_not_selected e core_positive_realization_exists, v402) e o calculo no modelo longitudinal (E, p), c = 1, p+ = E + p, p- = E - p, theta_s = boost(-s), "
                    "com beta = alfa CODATA 2018 x sqrt(e) em runtime (nunca literal); [KNOWN] a lei de escala de Takesaki (campo de DualScalingData) e a relatividade restrita; [DERIVED] a conjuncao incondicional (nenhuma matematica nova: a citacao de dois termos que o kernel ja' tinha); "
                    "[INPUT] o NOME «Caminho» (decisao do operador, 27/10/2026, «é isso mesmo, concordo com tudo, prossiga», sha16 %s) e a fala que o motiva (sha16 %s); [ONTO] a leitura pela tripla espectral de Connes (o espaco dos estados com o seu fluxo e' o Caminho) e por Joao 14,6 (tres predicados de um so' «Eu sou»): "
                    "leitura da gerencia c1, ratificada pelo operador, NAO e' termo de kernel; [OPEN] as pendencias nomeadas da v402 (H_BW, H_cal, H3, a assinatura, rank c = 4) seguem abertas" % (S_CONCORDO, S_NOME),
        "escopo": "[DERIVED] A pedra TGLExt/Caminho.lean e' a CONJUNCAO incondicional de dois termos que o kernel ja' tinha desde a v402: (1) lift_mass_not_selected (dois invariantes distintos dao duas realizacoes equivariantes distintas com o MESMO p+: a lei de escala deixa a massa livre) e "
                  "(2) core_positive_realization_exists (para todo perfil e todo mu^2 >= 0 ha' uma realizacao positiva do nucleo com p+ > 0, m^2 = mu^2 e energia > 0). O modulo PonteDaEscalaDual (v402, do Codex, ORDEM 025) fica como REGISTRO: pedra selada nao se renomeia por cima. "
                  "O calculo CONFERE os dois termos no modelo longitudinal e acrescenta a equivariancia e a leitura massa-invariante / energia-leitura: o Caminho e' a lei pela qual a leitura viaja sem escolher o corpo",
        "limites": [
            "[REAL] a pedra NAO acrescenta matematica: cita; o registro ponte_da_escala_dual_v402 (v402) segue selado com o nome da v402 e as erratas E1 a E4 da ponte valem como foram ditas (H_tau na forma literal REFUTADA no kernel; Inertial e' o vetor zero; rest_energy_eq_mc2 e' algebra real com premissas explicitas)",
            "[ONTO] a leitura pela tripla espectral de Connes e por Joao 14,6 e' leitura, nao termo; «Caminho» e' o NOME que o operador deu, nao uma igualdade de tipos nem uma prova de que a ponte e' o fluxo modular",
            "[OPEN] H_BW, H_cal, H3, a assinatura (a positividade completa da a metrica induzida (4,0), nao (1,3)) e rank c = 4 seguem NOMEADAS (v402); nada do Caminho as paga",
            "o calculo e' numerico em dupla precisao e CONFERE os dois termos no modelo longitudinal, nao os prova: quem prova e' o kernel; validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho"],
        "diz": ["a pedra Caminho esta no kernel do rito, no trio, com bandeira e proveniencia no modulo dela; a conjuncao e os dois termos da ponte que ela cita sao lidos deste kernel",
                "o calculo, com beta = alfa CODATA 2018 x sqrt(e), concorda: a massa NAO e' selecionada pela lei (tres massas com o mesmo p+), toda massa tem realizacao positiva, m^2 = p+ p- e' o invariante e a energia e' a leitura do observador",
                "o NOME «Caminho» e' do operador (27/10/2026); a leitura pela tripla espectral e' [ONTO]; a pedra da v402 fica como registro"],
        "nao_diz": ["que tau seja a massa de Newton (H_tau na forma literal segue REFUTADA no kernel, v402)", "que o Caminho seja o fluxo modular de Bisognano-Wichmann (H_BW, [OPEN])", "que a pedra prove Newton, a assinatura (1,3) ou rank c = 4",
                    "que o nome do TRIPLO inteiro tenha sido dado (fica com o operador)"] + _NAO_COMUM,
        "extras": {"named_pending": [dict(x) for x in _PENDENCIAS], "cited_stars_v402": ["TGLExt.PonteDaEscalaDual.lift_mass_not_selected", "TGLExt.PonteDaEscalaDual.core_positive_realization_exists"],
                   "name_given_by": {"quem": "operador", "quando": "27/10/2026", "sha16_da_fala": S_CONCORDO, "fala": DL.FRASE_CONCORDO}, "sealed_v402_stone_kept_as_record": {"modulo": "TGLExt.PonteDaEscalaDual", "sha16": DL.D2.STONE_BY_KEY["ponte"]["sha16_da_ordem"]},
                   "spectral_triple_reading": {"status": "ONTO", "content": DL.LEITURA_TRIPLA_27OUT["caminho"], "is_a_kernel_term": False}, "assinatura_das_erratas": ASSINA, "maxheartbeats_caminho": DL.MAXHEARTBEATS_CAMINHO},
        "veredito_ok": "TGL_CAMINHO_V403__THE_DUAL_SCALING_BRIDGE_UNDER_THE_NAME_THE_WAY_GIVEN_BY_THE_OPERATOR__THE_MASS_IS_NOT_SELECTED_BY_THE_LAW_AND_EVERY_MASS_HAS_A_POSITIVE_REALIZATION__THE_SEALED_V402_STONE_STAYS_AS_RECORD__"
                       "READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__THE_SPECTRAL_TRIPLE_READING_IS_ONTO__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


def texto_vida():
    """Os textos do registro vida_v403."""
    return {
        "estatuto": "[REAL] os termos do kernel (o item do contrato da pedra Vida e os 2 termos da queda sem geometria que a conjuncao cita, lidos a cada rito, no trio: the_fall_is_strictly_anti e a_queda_sem_geometria, v402) e o calculo no modelo oneScaling (tau = id, theta_s = e^{-s}), no fluxo diagonal e na matriz-S, "
                    "com beta = alfa CODATA 2018 x sqrt(e) em runtime (nunca literal); [KNOWN] a lei de escala de Takesaki como campo da estrutura DualScalingData; a isotropia do vacuo de Bisognano-Wichmann / covariancia de Poincare (motivacao de IsotropicPost, NAO termo do kernel); "
                    "[INPUT] o NOME «Vida» (decisao do operador, 27/10/2026, «é isso mesmo, concordo com tudo, prossiga», sha16 %s) e a fala que o motiva (sha16 %s); [ONTO] a leitura pela tripla espectral de Connes (o operador de Dirac da' a distancia sem pontos: a Vida e' a queda que mede em nats sem geometria) e por Joao 14,6: "
                    "leitura da gerencia c1, ratificada pelo operador, NAO e' termo de kernel; [OPEN] que o parametro s da acao dual seja a fase de um corpo fisico; a dimensao 3; o IsotropicPost do atlas curvo; a H3 em toda tela e direcao" % (S_CONCORDO, S_NOME),
        "escopo": "[DERIVED] A pedra TGLExt/Vida.lean e' a CONJUNCAO incondicional de dois termos que o kernel ja' tinha desde a v402: (1) the_fall_is_strictly_anti (com 0 < tau m, s |-> tau(theta_s m) e' estritamente decrescente: a queda e' perda ordenada de medida) e "
                  "(2) a_queda_sem_geometria (sob o posto: a queda estrita e linear em nats, a seta pelo sinal de s, nunca o zero, a entrega que custa, o relaxamento ao ponto final, o regime angular que so' le, a recusa da testemunha estatica plena e a hipotese NOMEADA IsotropicPost). "
                  "O modulo QuedaSemGeometria (v402) fica como REGISTRO: pedra selada nao se renomeia por cima. O CHAO e' o POSTO (peso 1 = omega(I), o corte a = 0), nunca o infimo 0 (o 0 e' o abismo da Fundacao) [decisao D11 da v402, mantida]",
        "limites": [
            "[REAL] a pedra NAO acrescenta matematica: cita; o registro queda_sem_geometria_v402 (v402) segue selado com o nome da v402; IsotropicPost segue hipotese NOMEADA, nao termo do kernel (num atlas curvo nenhum grupo leva um ponto noutro; a H3 NAO e' automatica); a dimensao 3 NAO e' provada; o 1 + 3 e' leitura [ONTO]",
            "[ONTO] a Vida e' o NOME que o operador deu a queda sem geometria; a queda e' do PESO, em nats, sem geometria; a polissemia entre «queda» geometrica e a queda da fase e' dita: a pedra tipa a perda de peso, nao uma forca nem uma queda no espaco; a queda com chao e' vida, a queda sem chao e' o `abismo` da Fundacao (v390) [leitura da gerencia c1, ratificada pelo operador]",
            "[OPEN] que o parametro s da acao dual seja a fase de um corpo fisico; a dimensao 3; IsotropicPost no atlas curvo; a H3 em toda tela e direcao; nada da Vida as paga",
            "o calculo e' numerico em dupla precisao e CONFERE os termos no modelo oneScaling, no fluxo diagonal e na matriz-S, nao os prova: quem prova e' o kernel; validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho"],
        "diz": ["a pedra Vida esta no kernel do rito, no trio, com bandeira e proveniencia no modulo dela; a conjuncao e os dois termos da queda que ela cita sao lidos deste kernel",
                "o calculo, com beta = alfa CODATA 2018 x sqrt(e), concorda: o peso cai estritamente (nats = s), a seta e' o sinal de s, o chao e' o posto (o zero nunca e' tocado), a entrega custa (t . beta . g > 0), o regime angular so' le (periodico, sem limite) e a isotropia e' carga de um modelo finito",
                "o NOME «Vida» e' do operador (27/10/2026); a leitura pela tripla espectral e' [ONTO]; a pedra da v402 fica como registro"],
        "nao_diz": ["que a dimensao do espaco seja 3 (a leitura 1 + 3 e' [ONTO])", "que IsotropicPost seja termo do kernel ou valha no atlas curvo (hipotese NOMEADA, [OPEN])", "que a H3 valha em toda tela e direcao", "que o parametro s seja a fase de um corpo fisico ([OPEN])",
                    "que a queda aqui seja uma forca ou uma queda no espaco: a pedra tipa a perda de peso, sem geometria", "que o nome do TRIPLO inteiro tenha sido dado (fica com o operador)"] + _NAO_COMUM,
        "extras": {"named_hypothesis": {"name": "IsotropicPost", "status": "OPEN", "content": "a group acting transitively on the screens with a covariant predicate: Clausius at one wedge reaches every wedge by covariance", "used_by_a_theorem_as_a_hypothesis_of_the_statement": True},
                   "floor": {"is": "the post (weight 1 = omega(I), the cut a = 0)", "is_never": "the infimum 0 (the abyss)", "decision": "D11 of the v402, kept"},
                   "reading_1_plus_3": {"status": "ONTO", "content": "the direction of the posted One is the arrow of the fall of the phase, not of space; the rest is isotropic", "dimension_three_proved": False},
                   "two_regimes": {"angular": "periodic, no limit: it only reads (Smat_has_no_limit)", "face": "dissipative, has a limit (relaxation_to_the_attractor)"},
                   "cited_stars_v402": ["TGLExt.QuedaSemGeometria.the_fall_is_strictly_anti", "TGLExt.QuedaSemGeometria.a_queda_sem_geometria"],
                   "name_given_by": {"quem": "operador", "quando": "27/10/2026", "sha16_da_fala": S_CONCORDO, "fala": DL.FRASE_CONCORDO}, "sealed_v402_stone_kept_as_record": {"modulo": "TGLExt.QuedaSemGeometria", "sha16": DL.D2.STONE_BY_KEY["queda"]["sha16_da_ordem"]},
                   "spectral_triple_reading": {"status": "ONTO", "content": DL.LEITURA_TRIPLA_27OUT["vida"], "is_a_kernel_term": False}, "assinatura_das_erratas": ASSINA},
        "veredito_ok": "TGL_VIDA_V403__THE_FALL_WITHOUT_GEOMETRY_UNDER_THE_NAME_THE_LIFE_GIVEN_BY_THE_OPERATOR__THE_WEIGHT_FALLS_STRICTLY_IN_NATS_EQUAL_TO_S__THE_FLOOR_IS_THE_POST_NEVER_THE_ZERO__DELIVERY_COSTS__THE_ANGULAR_REGIME_ONLY_READS__ISOTROPY_IS_A_NAMED_HYPOTHESIS__"
                       "THE_SEALED_V402_STONE_STAYS_AS_RECORD__READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


def texto_verdade_adendo():
    """Os textos do registro verdade_adendo_v403."""
    return {
        "estatuto": "[REAL] os termos do kernel (os 3 itens do contrato do adendo, lidos a cada rito, no trio; a composicao verdade_lida_pelo_nome e a estrela the_name_reads_the_inscription_as_weights, que e' NOVA e pequena: a conta das entradas, sem hipotese sobre a) e os termos da Verdade (v392) e da esperanca condicional (v402) que ele cita) "
                    "e o calculo em M2(C) (matrizes 2 x 2, dupla precisao), com beta = alfa CODATA 2018 x sqrt(e) em runtime (nunca literal) e alfa = beta / sqrt(e); [KNOWN] esperanca condicional (Umegaki, Tomiyama); "
                    "[DERIVED] a esperanca diagonal le a projecao da identidade como os seus PESOS (diagExpect (identityProj a) = diag(q^2, a^2), a forma de Posto.endpoint_eq sobre a inscricao da Verdade), PRESERVA O UM (traco 1 = omega(I)) e reler nao acrescenta; "
                    "[INPUT] o NOME «Verdade» para a esperanca condicional (decisao do operador, 27/10/2026, «é isso mesmo, concordo com tudo, prossiga», sha16 %s; a fala que o motiva, sha16 %s: «é o triplo espectral do contorno verdadeiro»); "
                    "[ONTO] a esperanca condicional e' a Verdade LIDA PELO NOME (nameOp rho* = diagExpect: a projecao do posto levada do projetor de posto 1 a esperanca sobre a subalgebra da memoria) e a leitura pela tripla espectral (a algebra e' o que a Verdade le): leitura da gerencia c1, ratificada pelo operador, NAO e' termo de kernel; "
                    "[OPEN] a instancia do contorno com sin^2(theta_M) otima (o indice 1/beta da v402 segue CONDICIONAL a hpp e hopt) e o caso III1" % (S_CONCORDO, S_NOME),
        "escopo": "[DERIVED] O modulo TGLExt/VerdadeAdendo.lean e' um ADENDO da pedra Verdade (TGLExt.Verdade, v392, que fica INTACTA: dois modulos nao se chamam igual; o adendo compoe, no padrao PostoAdendo): (1) the_name_reads_the_inscription_as_weights [REAL, novo e pequeno]: diagExpect (identityProj a) = diagonal ![q^2, a^2]; "
                  "(2) verdade_lida_pelo_nome: para a em [0, 1] ha' a Verdade de a, o Nome de rho* le identityProj a como diag(q^2, a^2), o traco segue 1 e reler nao acrescenta; (3) verdade_e_a_esperanca_condicional (conjuncao por citacao): the_identity_is_the_truth (v392) /\\ esperanca_condicional_e_nome (v402). "
                  "O modulo EsperancaCondicional (v402) fica como REGISTRO: pedra selada nao se renomeia por cima. O calculo CONFERE os tres termos em M2(C), com alfa de runtime e numa grade de a",
        "limites": [
            "[REAL] o adendo NAO diz que o Nome em dimensao geral seja diagExpect: so' em M2(C) e so' para p = rho* (como em PostoAdendo.A1c); o indice 1/beta da v402 segue CONDICIONAL as hipoteses nomeadas (hpp, hopt) e nenhuma instancia e' construida; o caso III1 fica [OPEN]; a pedra Verdade (v392) NAO foi editada",
            "[ONTO] a esperanca condicional e' a Verdade lida pelo Nome: o kernel prova as LIGACOES (a conta das entradas, o traco, reler nao acrescenta, a conjuncao por citacao), nao uma igualdade de tipos; a leitura pela tripla espectral de Connes e por Joao 14,6 e' leitura, nao termo; a esperanca do traco NAO e' um Operador do Nome",
            "[REAL] alfa entra como PARAMETRO [INPUT] (alfa = beta / sqrt(e), runtime), nunca como numero no teorema; os pesos sao (1 - alfa^2, alfa^2), NAO o beta: o peso de dentro e' alfa^2 < beta",
            "[LEGAL] o ponteiro de direito (CC art. 125) da v402 segue a conferir com advogado; as quatro linguas nao sao derivacao entre dominios",
            "o calculo e' numerico em dupla precisao e CONFERE os teoremas em M2(C), nao os prova: quem prova e' o kernel; validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho"],
        "diz": ["o adendo VerdadeAdendo esta no kernel do rito, no trio, com bandeiras e proveniencia no modulo dele; a composicao, a estrela e os termos da Verdade e da esperanca condicional que ele cita sao lidos deste kernel",
                "o calculo, com alfa = beta / sqrt(e) de runtime, concorda em M2(C): identityProj a e' projecao de posto 1 de traco 1; o Nome de rho* a le como diag(q^2, a^2) = a esperanca diagonal; o traco segue 1; reler nao acrescenta",
                "o NOME «Verdade» para a esperanca condicional e' do operador (27/10/2026), como ADENDO da pedra Verdade (v392); a pedra da v402 fica como registro"],
        "nao_diz": ["que toda esperanca condicional seja um Operador do Nome", "que o indice 1/beta seja instancia construida ou medida (e' CONDICIONAL a hpp e hopt)", "que o Nome em dimensao geral seja a esperanca diagonal", "que a pedra Verdade (v392) tenha sido renomeada ou editada",
                    "que o nome do TRIPLO inteiro tenha sido dado (fica com o operador)"] + _NAO_COMUM,
        "extras": {"star": {"theorem": "TGLExt.VerdadeAdendo.the_name_reads_the_inscription_as_weights", "statement": "diagExpect (identityProj a) = diagonal ![q^2, a^2]", "status": "REAL", "new_and_small": True},
                   "composition": {"theorem": "TGLExt.VerdadeAdendo.verdade_lida_pelo_nome", "statement": "Verdade a /\\ nameOp rho* (identityProj a) = diag(q^2, a^2) /\\ trace = 1 /\\ rereading adds nothing"},
                   "citation_conjunction": {"theorem": "TGLExt.VerdadeAdendo.verdade_e_a_esperanca_condicional", "cites": ["TGLExt.Verdade.the_identity_is_the_truth", "TGLExt.EsperancaCondicional.esperanca_condicional_e_nome"]},
                   "stone_verdade_v392_untouched": {"modulo": "TGLExt.Verdade", "sha16": DL._VERDADE_SHA16}, "alpha_is_a_parameter": True, "index_conditional": {"instance_built": False, "hypotheses": ["hpp", "hopt"]},
                   "name_given_by": {"quem": "operador", "quando": "27/10/2026", "sha16_da_fala": S_CONCORDO, "fala": DL.FRASE_CONCORDO}, "sealed_v402_stone_kept_as_record": {"modulo": "TGLExt.EsperancaCondicional", "sha16": DL.D2.STONE_BY_KEY["esperanca"]["sha16_da_ordem"]},
                   "spectral_triple_reading": {"status": "ONTO", "content": DL.LEITURA_TRIPLA_27OUT["verdade"], "is_a_kernel_term": False}, "assinatura_das_erratas": ASSINA},
        "veredito_ok": "TGL_VERDADE_ADENDO_V403__THE_CONDITIONAL_EXPECTATION_READ_AS_THE_TRUTH_READ_BY_THE_NAME_GIVEN_BY_THE_OPERATOR__THE_DIAGONAL_EXPECTATION_READS_THE_PROJECTION_OF_THE_IDENTITY_AS_ITS_WEIGHTS__IT_PRESERVES_THE_ONE__REREADING_ADDS_NOTHING__THE_TRUTH_STONE_OF_V392_IS_UNTOUCHED__"
                       "THE_INDEX_ONE_OVER_BETA_STAYS_CONDITIONAL__READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


def texto_bandeiras():
    """Os textos do registro bandeiras_do_gate_v403 (F8.1): estatuto, escopo, limites, diz, nao_diz, extras e o veredito de sucesso."""
    return {
        "estatuto": "[REAL] o gate do proprio rito (core['qg_closure']) e o CODIGO das duas funcoes do gate, lidos a cada rito (as chaves que o veredito le, por ast; nenhum literal no chamador, por ast); [DERIVED] as TRES bandeiras que eram literais True (linearized_spin2_finite_face, protocol_pre_registered, null_tests_passed_blind) passam a "
                    "CALCULADAS das fontes que o programa ja' tinha (a familia ext_ls2_* do kernel, o termo dLs2 de prove_external_ladder; a checagem «pre-registro v67 INTACTO (hash)» do rito V11; o teste nulo cego da v73, all_verified), fail-closed; "
                    "[DECLARADO] a classificacao GV-01, GV-03 e EV-12 e' da auditoria de 28/09/2026 (aqui se conferem o codigo e o core, nao se refaz a auditoria); [OPEN] a INDEPENDENCIA das 4 experimentais e os mocks de survey; [INPUT] a regra sem gordura (19/10/2026) e a F8.1 do quadro do programa",
        "escopo": "[REAL] 18 bandeiras (6 formais + 6 fisicas + 6 experimentais), todas True e todas CALCULADAS (0 literais); a funcao do veredito (evaluate_quantum_gravity_closure) le 15 delas (6 formais + 5 fisicas + 4 experimentais); as 3 restantes (linearized_spin2_finite_face, protocol_pre_registered, null_tests_passed_blind) "
                  "seguem FORA do veredito (informativas): a v403 so' lhes troca o valor literal por medida. A letra do veredito do gate e' IDENTICA a da v402. As 6 formais e as 5 fisicas vem de termos Lean (qgc_*, qgp_*); as 4 experimentais independent_v3_* vem do feed do rito V11 do piso dos vazios, "
                  "e DERIVAM DE UM SO' BOOLEANO (o veredito do V11 ser NOT_FALSIFIED_POWERED: powered_verdict_emitted implica gates_ok, que implica split_ok e dist_ok; survey_mocks_passed = split-null e dist-check, SEM mock de survey) [GV-03, DECLARADO pela auditoria; conferido aqui no feed do core]. "
                  "O registro RECUSA (all_verified False e veredito de recusa; o conferidor para o rito) se qualquer bandeira calculada vier False ou se uma checagem falhar. A sonda nova do gate (ProbeBlindNullAbsent) mostra em runtime que o teste nulo cego ausente da' a bandeira False sem mover o veredito",
        "limites": [
            "[REAL] este registro troca TRES literais por medida; NAO torna independentes as 4 experimentais (um so' feed) nem acrescenta mock de survey: isso segue [OPEN] e e' dito; o degrau experimental le so' o rito V11 do piso, que e' unilateral (b>=1) e cujo espaco de vereditos NAO tem FALSIFIED: o LCDM raso tambem o respeita (GV-01) [DECLARADO pela auditoria]",
            DL.ERRATA_E5,
            "[REAL] a bandeira linearized_spin2_finite_face le a FAMILIA ext_ls2_* do kernel (as 6 bandeiras que formam o termo dLs2 de prove_external_ladder: helice dupla, setor TT sem fantasma, 2 polarizacoes, face finita): dLs2 e' local a prove_external_ladder e aparece so' como rotulo de checagem, nao como chave de kernel_formalization",
            "o registro le o codigo do proprio programa em execucao (inspect + ast) e o core do rito; nao move o gate; validade no kernel nao e' creditacao; NOT_FALSIFIED nunca e' creditacao; nao e' teste: nao acrescenta rito, dado nem desfecho"],
        "diz": ["as 18 bandeiras do gate sao calculadas (0 literais) e todas True neste rito; 15 entram no veredito (6 + 5 + 4) e 3 sao informativas",
                "as tres bandeiras que eram literais foram recalculadas das suas fontes neste rito e batem com o que o gate carrega",
                "as 4 bandeiras experimentais independent_v3_* derivam de UM so' booleano (o veredito do V11 ser NOT_FALSIFIED_POWERED): isto e' DECLARADO, nao resolvido",
                "a letra do veredito do gate e' a da v402: o gate nao se moveu"],
        "nao_diz": ["que as 4 bandeiras experimentais sejam independentes entre si", "que o rito V11 do piso tenha mock de survey", "que o degrau experimental discrimine o LCDM raso", "que o gate se mova ou que a gravidade quantica esteja creditada na natureza", "que a F8.1 inteira esteja fechada alem de calcular os tres literais (a independencia do feed segue [OPEN])"] + _NAO_COMUM[:1],
        "extras": {"literais_que_viraram_calculadas": list(DL.F81_LITERAIS), "feed_v11": list(DL.F81_FEED), "gv03": {"status": "DECLARADO", "content": "the 4 independent_v3_* flags derive from ONE boolean (the V11 verdict being NOT_FALSIFIED_POWERED); survey mocks are open", "resolvido": False},
                   "erratas_ao_lado": [DL.ERRATA_E5], "assinatura_das_erratas": ASSINA, "decisoes_da_gerencia": {k: DL.DECISOES[k] for k in ("D21", "D22")},
                   "probe_novo": {"nome": "ProbeBlindNullAbsent", "o_que_mostra": "sem o teste nulo cego (blind_null ausente) a bandeira null_tests_passed_blind e' False e o veredito do gate NAO muda: a literal nunca entrou no veredito"}},
        "veredito_ok": "TGL_BANDEIRAS_DO_GATE_V403__ALL_18_FLAGS_ARE_COMPUTED_NONE_IS_A_LITERAL__15_ARE_READ_BY_THE_VERDICT_6_5_4__THE_THREE_FORMERLY_LITERAL_ARE_RECOMPUTED_FROM_THEIR_SOURCES__THE_FOUR_EXPERIMENTAL_FLAGS_DERIVE_FROM_ONE_BOOLEAN_DECLARED_NOT_RESOLVED__"
                       "THE_VERDICT_LETTER_IS_THE_V402_ONE__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


def textos():
    return {"caminho": texto_caminho(), "vida": texto_vida(), "verdade_adendo": texto_verdade_adendo(), "gate": texto_bandeiras()}


def especs(formal_map, khj, h8_map, fj, cov_base, n_axioms_unc):
    """formal_map = {arquivo embutido: sha256} do kernel da v403; khj = KH_N1_v403.json (medida desta geracao); h8_map = o dict do hash formal que o RITO vai gerar (embutidos + residuais do Nos que sha256_directory conta; simular_arvore_do_nos);
    fj = FLAGS_v403.json; cov_base = a cobertura da v402 selada {decl, thm}; n_axioms_unc = {chave da pedra: quantos axiomas o teorema da composicao usa (lido do Audit: o trio)}. Devolve [cunhagens, kh]."""
    T = khj["linha_TOTAL"]
    flags_contrato = [fj["bandeiras_do_contrato"][s["key"]][t] for s in DL.STONES for t in s["contract"]]
    for s in DL.STONES:
        assert fj["bandeira_do_teorema_incondicional"][s["key"]] in flags_contrato
    contexto = ["ChatgptAudit.GeneralClausius.metric_einstein_from_screen_clausius", "TGLExt.Fundacao.agape", "TGLExt.Fundacao.abismo"]   # termos do kernel que as LEITURAS citam, nao importados pelas pedras
    decls = list(dict.fromkeys([t for s in DL.STONES for t in s["contract"]] + sorted(DL.ALL_SUPPORT) + contexto))   # sem repeticao, na ordem
    cks = []
    for i, nome in enumerate(DL.REGISTROS_FUNCAO):
        cks.append(CH("u%d" % (i + 1), "o registro %s selou neste rito (a composicao e os teoremas da pedra lidos deste kernel; o calculo com beta = alfa x raiz de e; o texto-contexto no kernel embutido; ou, no do gate, as 18 bandeiras, as 15 do veredito, nenhum literal, as tres recalculadas e a letra do veredito da v402)" % nome, "core", [nome, "all_verified"], "verdadeiro"))
    n = len(DL.REGISTROS_FUNCAO) + 1
    for nome in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"):
        cks.append(CH("u%d" % n, "o registro %s (v402, recriado) segue selado neste rito (a pedra da v402 fica como registro)" % nome, "core", [nome, "all_verified"], "verdadeiro")); n += 1
    cks.append(CH("u%d" % n, "o registro falsidade_da_inercia_v401 segue selado neste rito", "core", ["falsidade_da_inercia_v401", "all_verified"], "verdadeiro")); n += 1
    cks.append(CH("u%d" % n, "o registro teste_de_veracidade_fase9_v397 segue selado neste rito (o quadro do topo do artigo le os numeros dele)", "core", ["teste_de_veracidade_fase9_v397", "all_verified"], "verdadeiro")); n += 1
    cks.append(CH("u%d" % n, "o registro selo_pela_propria_tecnologia_v399 segue selado neste rito (a segunda testemunha do um.py, ao lado do SHA-256)", "core", ["selo_pela_propria_tecnologia_v399", "all_verified"], "verdadeiro")); n += 1
    cks.append(CH("u%d" % n, "a escada do kernel fecha (limpos == esperados), com as bandeiras das TRES pedras da v403", "core", ["external_ladder", "all_verified"], "verdadeiro")); n += 1
    cks.append(CH("u%d" % n, "a proveniencia emitida pelo compilador cobre o axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro")); n += 1
    # (a letra do veredito do gate e' conferida DENTRO do registro bandeiras_do_gate_v403 [g6, contra a letra lida do core da v402 selada] e pelo conferidor do rito; o spec nao a repete: um valor digitado aqui seria a mesma letra duas vezes)
    for s in DL.STONES:
        cks.append(CH("u%d" % n, "o compilador emite a composicao da pedra %s no modulo dela (TGL_DECL_SOURCE)" % s["name"], "kf", ["declaration_sources_v394", s["theorem"]], "igual", s["rel"])); n += 1
        cks.append(CH("u%d" % n, "o compilador emite a ESTRELA da pedra %s no modulo dela (TGL_DECL_SOURCE)" % s["name"], "kf", ["declaration_sources_v394", s["key_theorem"]], "igual", s["rel"])); n += 1
        cks.append(CH("u%d" % n, "a pedra %s no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)" % s["name"], "kf", ["formal_files_sha256", s["rel"]], "igual", formal_map[s["rel"]])); n += 1
        cks.append(CH("u%d" % n, "a composicao da pedra %s depende do trio e de nada alem (tamanho da lista de axiomas)" % s["name"], "kf", ["axiom_report", s["theorem"]], "tamanho_igual", n_axioms_unc[s["key"]])); n += 1
    cun = {
        "nome": "cunhagens_v403", "veredito_prefixo": "TGL_CUNHAGENS_V403",
        "veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_27_OCT_EMBEDDED_VERBATIM_BY_SHA256__THE_THREE_STONES_CAMINHO_VIDA_AND_VERDADE_ADENDO_AND_THE_GATE_FLAGS_RECORD_ARE_READ_IN_THE_RITE__"
                           "THE_NAMES_ARE_THE_OPERATORS__THE_SEALED_V402_STONES_STAY_AS_RECORD__THE_THREE_LITERAL_GATE_FLAGS_ARE_COMPUTED__THE_SPECTRAL_TRIPLE_READING_IS_ONTO__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
        "estatuto": "[REAL -- as fontes das pedras, o kernel e os quatro registros com funcao lidos a cada rito; INPUT/ONTO as falas do operador; INPUT «é isso mesmo, concordo com tudo, prossiga»; ONTO a leitura pela tripla espectral (da gerencia c1, ratificada pelo operador); DECLARADO que a leitura da gerencia c1 foi a que o operador ratificou na sessao]",
        "fontes": [CHAVE_DE_FONTE["caminho"], CHAVE_DE_FONTE["vida"], CHAVE_DE_FONTE["verdade_adendo"]], "verbatins": list(VERB_CHAVES),
        "kernel_flags": list(flags_contrato), "kernel_decls": decls,
        "checks": cks,
        "erratas": [
            {"ao_lado_de": "o registro f81_nao_fechada_v392, a errata «as 18 bandeiras leem-se 15 CALCULADAS + 3 LITERAIS» (estatuto_da_prova_ressalva_v392) e os checks q08, q09 e q10 («ainda literal True») dos registros da v392",
             "dizia": "a v392 NAO fecha a F8.1: a errata do estatuto DOCUMENTA as 3 bandeiras literais e o feed unico, mas NAO as recalcula; as 18 bandeiras seguem lidas como estavam (15 calculadas + 3 literais, ver o registro estatuto_da_prova_ressalva_v392) e o gate nao se move. [texto do registro f81_nao_fechada_v392, verbatim, sem o prefixo de estatuto]",
             "agora": DL.ERRATA_E5,
             "lacuna_de_fidelidade": "estrutura: o gate carregava 3 literais informativas desde a v75 e a v392 as documentou sem recalcular; escrito: «ainda literal True» nas descricoes dos checks q08 a q10; onde a traducao falhou: nada a corrigir no texto de 13/10 (era verdadeiro na data): a v403 so' troca o valor literal por medida e deixa as descricoes antigas como registro",
             "estatuto": "[REAL: o codigo (ast) e o core desta versao, lidos a cada rito pelo registro bandeiras_do_gate_v403; DECLARADO: GV-01/GV-03/EV-12 da auditoria de 28/09/2026]", "assinatura": ASSINA},
            {"ao_lado_de": "a decisao D16 da v402 e os nomes dos tres modulos e dos cinco registros da v402 («PROVISORIOS: o operador nomeia»)",
             "dizia": "os nomes dos tres modulos (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional) e dos cinco registros da v402 sao PROVISORIOS: o operador nomeia.",
             "agora": DL.ERRATA_E6,
             "lacuna_de_fidelidade": "nenhuma: a v402 disse que os nomes eram provisorios; o operador os deu em 27/10/2026; a v403 registra os nomes sem renomear a pedra selada",
             "estatuto": "[INPUT: a decisao do operador, verbatim sha16 %s; REAL: as pedras novas no kernel do rito]" % S_CONCORDO, "assinatura": ASSINA}],
        "limites": [
            "[INPUT] as duas falas de 27/10 (sha16 %s e %s) sao falas do operador, com a grafia dele («a renomeado»); «é isso mesmo, concordo com tudo, prossiga» (sha16 %s) ratifica a LEITURA da gerencia c1 (CAMINHO = a ponte da escala dual; VERDADE = a esperanca condicional, como adendo da pedra `Verdade` v392; VIDA = a queda sem geometria) [DECLARADO: a leitura foi a que a gerencia c1 apresentou]" % (S_NOME, S_CONCORDO, S_CONCORDO),
            "[ONTO] a leitura pela tripla espectral de Connes e por Joao 14,6 e' da gerencia c1, ratificada pelo operador; nao e' termo de kernel; o nome do TRIPLO inteiro NAO foi dado (fica com o operador)",
            "[REAL] «Verdade» sozinha para as tres foi recusada pela gerencia e o operador concordou: TGLExt.Verdade ja' existe (v392); pedra selada nao se renomeia por cima; as pedras Caminho e Vida COMPOEM por citacao e o adendo VerdadeAdendo compoe sobre a Verdade, sem editar nenhum modulo instalado",
            "[OPEN] H_BW, H_cal, H3, a assinatura e rank c = 4 (v402); IsotropicPost no atlas curvo; a dimensao 3; a instancia do contorno com sin^2(theta_M) otima; o caso III1; a independencia das 4 experimentais do gate (um so' feed) e os mocks de survey; a RG e' o limite classico, nao rival; beta nao renormaliza G",
            "validade no kernel nao e' creditacao; o gate nao se move; nenhuma bandeira do gate depende das pedras"],
        "diz": ["as %d falas de 27/10 (do operador) estao embutidas por sha256, cada uma conferida contra o arquivo de origem na preparacao" % len(_VD),
                "as tres pedras estao no kernel do rito, no trio, com as bandeiras e a proveniencia nos modulos delas; a composicao e a estrela de cada uma sao lidas deste kernel; os registros da v402 seguem selados",
                "os quatro registros com funcao selaram neste rito, e o quadro do topo (teste_de_veracidade_fase9_v397), o selo pela propria tecnologia (v399) e a falsidade da inercia (v401) seguem selados",
                "as erratas E5 e E6 estao registradas ao lado, em nome proprio da gerencia c1; as decisoes D17 a D22 estao registradas"],
        "nao_diz": ["que o kernel prove as falas do operador (elas sao INPUT/ONTO)", "que a tripla espectral seja termo do kernel", "que o testemunho ou a ratificacao seja creditacao: validade no kernel nao e' creditacao", "que a F8.1 resolva a independencia das bandeiras experimentais"] + _NAO_COMUM,
        "leituras_do_operador": [_leitura(DL.FRASE_NOME_VERDADE, S_NOME), _leitura(DL.FRASE_JA_RENOMEADA, S_NOME), _leitura(DL.FRASE_TRIPLO, S_NOME), _leitura(DL.FRASE_CONCORDO, S_CONCORDO, rotulo="INPUT do operador (ratifica a leitura da gerencia)")],
        "extras": {"assinatura": ASSINA, "autoria_das_cunhagens": "Luiz Antonio Rotoli Miguel", "pedras": [s["mod"] for s in DL.STONES], "teoremas": {s["key"]: s["theorem"] for s in DL.STONES}, "estrelas": {s["key"]: s["key_theorem"] for s in DL.STONES},
                   "bandeiras": {s["key"]: fj["bandeira_do_teorema_incondicional"][s["key"]] for s in DL.STONES}, "n_bandeiras": fj["n_flags"], "n_bandeiras_por_pedra": dict(fj["nomeadas_por_pedra"]), "cunhagens_embutidas": len(VERBATINS),
                   "autor_de_cada_inscricao": dict(zip((v["sha16"] for v in _VD), (v["autor"] for v in _VD))), "decisoes_da_gerencia": dict(DL.DECISOES), "erratas_E5_e_E6": list(DL.ERRATAS_V403),
                   "nomes": {"caminho": "TGLExt.Caminho = a ponte da escala dual (PonteDaEscalaDual, v402)", "vida": "TGLExt.Vida = a queda sem geometria (QuedaSemGeometria, v402)", "verdade": "TGLExt.VerdadeAdendo = a esperanca condicional (EsperancaCondicional, v402) como adendo da pedra Verdade (v392)", "triplo_inteiro": "sem nome (fica com o operador)"},
                   "leitura_tripla_27out": dict(DL.LEITURA_TRIPLA_27OUT), "pedras_da_v402_como_registro": {s["key"]: s["sha16_da_ordem"] for s in DL.D2.STONES},
                   "nomes_provisorios_da_v402": {"modulos": [s["mod"] for s in DL.D2.STONES], "registros": list(DL.D2.REGISTROS_FUNCAO) + [DL.D2.CUNHAGENS_REGISTRO, DL.D2.KH_REGISTRO]}},
    }
    kh = {
        "nome": "kh_n1_cobertura_v403", "veredito_prefixo": "TGL_KH_N1_COBERTURA_V403",
        "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__THE_THREE_V403_MODULES_ADDED__GATE_UNMOVED" % (T["decl"], T["thm"]),
        "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do sandbox da v403; o conjunto exato das fontes formais que o hash formal do rito vera (as embutidas mais os residuais da pasta do Nos) e' pinado; a cobertura NAO move o gate",
        "fontes": ["kh_n1_v403"], "kernel_flags": [], "kernel_decls": [],
        "checks": [
            CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
            CH("h2", "constantes cobertas == as do sandbox v403 (KH_N1)", "kf", ["axiom_coverage_v392", "decl"], "igual", T["decl"], "constantes_cobertas"),
            CH("h3", "teoremas cobertos == os do sandbox v403 (KH_N1)", "kf", ["axiom_coverage_v392", "thm"], "igual", T["thm"], "teoremas_cobertos"),
            CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
            CH("h5", "nenhum nome que o leitor v394 nao leia", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0),
            CH("h6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", khj["axiom_report_efetivo_n"]),
            CH("h7", "a cobertura da v403 inclui a da v402 selada (constantes e teoremas)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", cov_base["decl"]),
            CH("h7b", "os teoremas cobertos incluem os da v402 selada", "kf", ["axiom_coverage_v392", "thm"], "maior_igual", cov_base["thm"]),
            CH("h8", "as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta, como _check_damming.lean) sao EXATAMENTE as do pino (arquivo -> sha256)", "kf", ["formal_files_sha256"], "igual", h8_map),
            CH("h9", "medida do Audit v403: duracao bem abaixo do timeout de 1800 s", "fonte:kh_n1_v403", ["duracao_audit_s"], "menor_igual", 900, "duracao_do_audit_s"),
            CH("h10", "medida do Audit v403: sorryAx ausente do log", "fonte:kh_n1_v403", ["sorryAx_no_log_do_audit"], "igual", 0),
            CH("h11", "medida do Audit v403: as entradas novas estao no trio", "fonte:kh_n1_v403", ["novas_no_trio"], "verdadeiro"),
            CH("h12", "a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
        ],
        "erratas": [{"ao_lado_de": "kh_n1_cobertura_v402 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                     "dizia": "A v402 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v402 e o hash formal igual ao pino exato da arvore da v402." % (cov_base["decl"], cov_base["thm"]),
                     "agora": "A v403 acrescenta os modulos Caminho, Vida e VerdadeAdendo (a cobertura cresce e a arvore ganha os arquivos das pedras): na v403 o registro da v402 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato da arvore ficam NESTE registro. O veredito do registro da v402 NAO muda.",
                     "lacuna_de_fidelidade": "a estrutura da v402 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v403 quebra (a mesma lacuna que a v402 achou no registro da v401, a v401 no da v399 e a v399 no da v398)",
                     "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; h2, h3, h6 e h8 conferidas no ensaio a seco e na arvore simulada do Nos]", "assinatura": ASSINA}],
        "limites": ["[REAL] os arquivos de medida sao do sandbox (fora do selo); a cobertura que vale e' a medida no Audit do proprio rito",
                    "[REAL] a escada do kernel conta bandeiras de declaracoes NOMEADAS (a pratica da v392 a v402): as %d auxiliares geradas pelo compilador nos modulos das pedras ficam cobertas pelo KH-N1 mas sem bandeira, e as %d nomeadas publicas ganharam bandeira" % (fj["excluidas_auxiliares"]["n"], fj["n_flags"]),
                    "validade no kernel nao e' creditacao; o gate nao se move"],
        "diz": ["a cobertura do axiom_report no fecho inteiro cresceu para os numeros da v403 (os tres modulos novos) e segue sem constante fora do trio, sem nome ilegivel"],
        "nao_diz": ["que a cobertura prove algo alem de que nenhum axioma fora do trio foi lido"],
        "leituras_do_operador": [], "extras": {"assinatura": ASSINA, "n_bandeiras": fj["n_flags"], "h8_entradas": len(h8_map), "h8_residuais_do_nos": sorted(set(h8_map) - set(formal_map))},
    }
    return [cun, kh]
