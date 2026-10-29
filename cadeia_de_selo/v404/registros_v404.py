# -*- coding: utf-8 -*-
"""registros_v404.py -- os dados dos registros da v404: FONTES pinadas por sha256 (lidas do disco pelo montador, nunca digitadas), VERBATINS (as NOVE falas de 28/10/2026 ainda nao embutidas, todas do operador; EMBUTIDAS: a fala embutida manda, o arquivo e' so' informativo),
os CONTRATOS e os TEXTOS dos TRES registros com FUNCAO (`projecao_transversal_v404`, `jo8v32_v404` e `f2b_errata_v404`: gerar_candidato_v404.py os emite a partir de runtime_v404.py; cada contrato de pedra sai de contrato() abaixo, DERIVADO do build do sandbox;
o contrato da errata de F2b sai de contrato_f2b() abaixo, DERIVADO do core da v403 SELADA) e os dois SPECS interpretados pelo MOTOR _v392_registro (`cunhagens_v404` e `kh_n1_cobertura_v404`). Fontes so' em pasta DURAVEL: tudo vem de cadeia_de_selo\\v404\\insumos.
Texto novo passa pela guarda P18 (a cada rito). O NOME Jo8v32 e' do operador (28/10/2026); o da pedra do sen 45 graus e' PROVISORIO da gerencia, aceito pelo operador ate' ele dar outro; as pedras da v403 FICAM como registro. Molde: registros_v403.py."""
import ast, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v404 as DL  # noqa: E402
import runtime_v404 as RT  # noqa: E402   (so' as funcoes puras; nada do um.py e' executado)

INS = os.path.join(HERE, "insumos")
ASSINA = DL.ASSINA
PROJECAO, JO8 = DL.STONE_BY_KEY["projecao"], DL.STONE_BY_KEY["jo8v32"]
CHAVE_DE_FONTE = {"projecao": "projecao_pedra", "jo8v32": "jo8v32_pedra"}
CHAVE_LEVANTAMENTO = "levantamento_massa_28out"

FONTES = [{"chave": CHAVE_DE_FONTE["projecao"], "arquivo": os.path.join(INS, PROJECAO["insumo"]), "papel": "a pedra TGLExt/ProjecaoTransversalDaMeiaNat.lean (o nome e' PROVISORIO da gerencia, aceito pelo operador ate' ele dar outro; deriva o sen 45 graus do neutrino da Meia-Nat; compilada e provada no sandbox k403c e no k404c; copia duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)"},
          {"chave": CHAVE_DE_FONTE["jo8v32"], "arquivo": os.path.join(INS, JO8["insumo"]), "papel": "a pedra TGLExt/Jo8v32.lean (o nome «Jo8:32» e' do operador, 28/10/2026; conjuncao por citacao das tres estrelas da v403; compilada e provada no sandbox; copia duravel; a que vale no rito e' a EMBUTIDA no kernel)"},
          {"chave": "kh_n1_v404", "arquivo": os.path.join(INS, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox da v404 (pos_build_kernel_v404.py)"},
          {"chave": CHAVE_LEVANTAMENTO, "arquivo": os.path.join(INS, os.path.basename(DL.LEVANTAMENTO_ARQ)), "papel": "o levantamento «a transicao para a massa» (gerencia c1, 28/10/2026): onde o programa tem beta como massa, fracao ou contagem; a unica massa derivada de beta e' a do neutrino, com a escala E0 DECLARADA; leitura da gerencia, [DECLARADO] nos pontos do acervo"}]


def _trecho(t):
    s = t.strip().splitlines()[-1].strip() if t.strip() else ""     # a ultima linha da fala (a primeira e' o cabecalho com a data e o destinatario)
    s = s[:48].rstrip()
    assert s and s in t, s
    return s


_VD = DL.verbatins404(os.path.join(INS, "cunhagens"))
VERBATINS = [{"chave": v["chave"], "arquivo": v["arquivo"], "quando": v["quando"], "trechos": [_trecho(v["text"])], "papel": v["papel"], "fonte_original": v["fonte_original"]} for v in _VD]
VERB_CHAVES = [v["chave"] for v in _VD]
SHA16 = {os.path.basename(v["fonte_original"]): v["sha16"] for v in _VD}
S_BOCAS, S_CALIBRAR, S_UMABS, S_TRANSICAO, S_SOMBRA, S_PROJECAO, S_ORDEM, S_JO8, S_CONCORDO = tuple(v["sha16"] for v in _VD)    # LIDOS dos arquivos, na ordem de DL.VERBATIM_ORIGEM_V404 (o unpack recusa outro numero)
CH_BOCAS, CH_CALIBRAR, CH_UMABS, CH_TRANSICAO, CH_SOMBRA, CH_PROJECAO, CH_ORDEM, CH_JO8, CH_CONCORDO = tuple(v["chave"] for v in _VD)
TEXTOS = {v["sha16"]: v["text"] for v in _VD}
CH = lambda id_, desc_, onde_, caminho_, op_, valor_=None, cap_=None, est_="[REAL]": dict(id=id_, descricao=desc_, onde=onde_, caminho=caminho_, op=op_, **({"valor": valor_} if valor_ is not None else {}), **({"capturar": cap_} if cap_ else {}), estatuto=est_)


def _leitura(trecho, sha16, quando="28/10/2026", rotulo="INPUT do operador"):
    assert trecho in TEXTOS[sha16], ("a leitura do operador NAO esta verbatim na fala", sha16, trecho)
    return {"trecho": trecho, "estatuto": "[%s, verbatim %s, sha16 %s]" % (rotulo, quando, sha16)}


# o texto-CONTEXTO que cada registro confere no kernel embutido do proprio rito: o cabecalho da pedra (lido do corpo embutido, nao digitado como prova); conferido tambem NA GERACAO contra o arquivo da pedra
CONTEXTO = {"projecao": {"path": PROJECAO["rel"], "needles": ["# A PROJEÇÃO TRANSVERSAL DA MEIA-NAT", "transverse_amplitude_of_self_conjugate"]},
            "jo8v32": {"path": JO8["rel"], "needles": ["# Jo 8,32 — O TRIPLO INTEIRO: CAMINHO · VERDADE · VIDA", "a_verdade_vos_libertara"]}}
for _k, _cx in CONTEXTO.items():
    _src = open(DL.STONE_BY_KEY[_k]["src"], encoding="utf-8", newline="").read()
    assert all(n_ in _src for n_ in _cx["needles"]), ("o texto-contexto NAO esta na pedra", _k)
KEY_STATEMENT = {"projecao": "x = 1 - x => sqrt x = sin(pi/4) (self-conjugate x): the Half-Nat IS the 45-degree angle (sin^2(pi/4) = 1/2, unique in [0, pi/2]); the neutrino form beta . sin(45) . E0 = sin^2(theta_M) . sin(pi/4) . E0 (Theorem S-d: beta = sin^2 theta_M); theta_M != pi/4 when beta != 1/2; d(sin^2 theta)/d theta at pi/4 = 1",
                 "jo8v32": "(Caminho: caminho_e_a_ponte_da_escala_dual) /\\ (Verdade: verdade_e_a_esperanca_condicional) /\\ (Vida: vida_e_a_queda_sem_geometria): the conjunction of the three stars of the v403, in the order of John 8,31-32 (remain, know, free), by citation (type_of%): nothing new in mathematics"}
HIPOTESES_NO_ENUNCIADO = {"projecao": False, "jo8v32": True}     # jo8v32: a conjuncao e' um termo SEM hipoteses, mas dois dos tres componentes (Vida: IsotropicPost; Verdade: o indice 1/b, hpp e hopt) carregam hipoteses NOMEADAS no enunciado deles: citadas, nao pagas
VERBATINS_DO_REGISTRO = {"projecao": [CH_SOMBRA, CH_PROJECAO, CH_ORDEM, CH_CONCORDO], "jo8v32": [CH_JO8, CH_CONCORDO]}


def contrato(stone, fj, formal_map, e_base, base_sha256, core0=None):
    """O contrato de UMA pedra (as falas ficam em _V404_VERBATINS2), DERIVADO do build do sandbox (FLAGS_v404.json = nomes, chaves e a proveniencia dos termos de suporte; formal_map = sha256 das fontes embutidas; e_base = a escada da v403 selada;
    a escada esperada e' a DESTA versao: a da base + as bandeiras das DUAS pedras); nada digitado. core0 (opcional) = o core da v403 SELADA, de onde saem os pinos do registro da pedra do angulo. Vai para CANDIDATO_v404.json e ESPERADOS_v404.json."""
    k = stone["key"]
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    faltam = [t for t in stone["contract"] if t not in flag_de]
    assert not faltam, ("teorema do contrato sem bandeira (nao nomeado ou ausente do Audit)", k, faltam[:5])
    assert fj["bandeira_do_teorema_incondicional"][k] == flag_de[stone["theorem"]] and fj["teorema_incondicional"][k] == stone["theorem"]
    assert stone["key_theorem"] in stone["contract"] and stone["theorem"] in stone["contract"]
    sup = dict(fj["suporte_do_contrato"][k]); assert sup == dict(stone["support"]), "os termos de suporte do FLAGS_v404.json diferem dos de delta_v404: " + k
    cit = dict(fj["citados_fora_do_contrato"][k]); assert cit == dict(stone["citados_fora"]), "os termos citados-fora do FLAGS_v404.json diferem dos de delta_v404: " + k
    c = {"stone": {"path": stone["rel"], "sha256": formal_map[stone["rel"]], "module": stone["mod"]},
         "unconditional": {"theorem": stone["theorem"], "flag": flag_de[stone["theorem"]]},
         "key_theorem": {"theorem": stone["key_theorem"], "flag": flag_de[stone["key_theorem"]]}, "key_statement": KEY_STATEMENT[k],
         "theorems": {t: flag_de[t] for t in stone["contract"]}, "support": sup, "cited_outside": cit,
         "auxiliaries_outside_the_composition": list(stone["auxiliares_fora_da_composicao"]), "context": dict(CONTEXTO[k]), "named_hypotheses_in_the_statement": HIPOTESES_NO_ENUNCIADO[k],
         "expected_ladder": e_base + fj["n_flags"], "n_flags": fj["nomeadas_por_pedra"][k], "n_flags_total": fj["n_flags"], "verbatins": list(VERBATINS_DO_REGISTRO[k]), "baseline": {"version": DL.BASE_VERSION, "sha256": base_sha256}}
    if k == "jo8v32":
        c["order_of_the_verse"] = ["TGLExt.Caminho.caminho_e_a_ponte_da_escala_dual", "TGLExt.VerdadeAdendo.verdade_e_a_esperanca_condicional", "TGLExt.Vida.vida_e_a_queda_sem_geometria"]   # permanecer, conhecer, libertar (Jo 8,31-32)
        c["v403"] = {"n_checks": [DL.D3.N_CHECKS_CAMINHO, DL.D3.N_CHECKS_VIDA, DL.D3.N_CHECKS_VERDADE_ADENDO], "registros": ["caminho_v403", "verdade_adendo_v403", "vida_v403"]}
        c["name_phrase"] = DL.FRASE_JO8; c["ratification_phrase"] = DL.FRASE_CONCORDO404
        assert sorted(c["order_of_the_verse"]) == sorted(c["support"]), "a ordem do versiculo difere dos termos citados"
    if k == "projecao":
        nm0 = (core0 or {}).get("neutrino_mass") or {}
        assert str(nm0.get("angle_status", "")).startswith(DL.ANGLE_STATUS_ANTIGO_PREFIXO), "o angle_status da base (v403 selada) NAO comeca como a v404 espera (a errata ao lado cita o texto antigo)"
        c["neutrino"] = {"angle_status_antigo_prefixo": DL.ANGLE_STATUS_ANTIGO_PREFIXO, "angle_status_antigo_sha256": __import__("hashlib").sha256(nm0["angle_status"].encode("utf-8")).hexdigest(), "frozen_hash_v403": nm0["frozen_hash"], "m_nu_meV_v403": nm0["m_nu_meV"],
                         "verdict_v403": nm0["verdict"], "e0_declarado_eV": DL.E0_DECLARADO_EV, "rel_tol": 1e-12}
    return c


# ---------------------------------------------------------------- o CONTRATO do registro da errata de F2b: DERIVADO do core da v403 SELADA (a base); NA GERACAO, recusa (excecao visivel) se o V1 nao foi lido por hash ou se algum pino nao bate
def contrato_f2b(core0):
    rb = core0["ramo_b_preregistration_v386"]; le = core0["ledger_errata_v386"]; led = core0["the_ledger_of_charges_v383"]
    cv = rb["central_values_NOT_BLIND_read_from_V1"]; pin = rb["pins"]["delta_pred_A31_exato"]
    def _recusa(msg, det=None):
        raise RuntimeError("RECUSO (f2b_errata_v404): %s %s" % (msg, "" if det is None else repr(det)[:400]))
    if not (rb.get("all_verified") is True and rb.get("read_ok") is True and rb.get("F2b_status") == "AWAITING" and rb.get("veredito_do_V1") == DL.F2B_V1_TOKEN_ANTIGO):
        _recusa("o V1 do ramo B nao esta lido por hash no core da v403 selada, ou o estado dele nao e' o que a errata cita", {k: rb.get(k) for k in ("all_verified", "read_ok", "F2b_status", "veredito_do_V1")})
    m = RT.v404_parse_deformacao(cv.get("A_31_deformacao_comum_GWTC5"))
    if m is None:
        _recusa("a deformacao comum de A nao se le do V1", cv.get("A_31_deformacao_comum_GWTC5"))
    if not (pin.get("equal") is True and pin["read"] < 0.0):
        _recusa("o pino da previsao do par nao bate ou nao e' negativo", pin)
    ids = [c.get("id") for c in led.get("ledger") or []]
    r2 = next((c for c in led["ledger"] if c.get("id") == "R2"), None)
    if len(ids) != 11 or r2 is None or le.get("v383_ledger_intact") is not True or le.get("F2_untouched") is not True or le.get("R2_untouched") is not True:
        _recusa("o livro v383 nao esta intacto no core da base", ids)
    return {"kind": "f2b", "v1": {"identificador": rb["identificador_read"], "json_sha256": rb["sha256_read"]["json"], "spec_sha256": rb["spec_sha256_expected"], "veredito": rb["veredito_do_V1"], "token_estado": rb["token_estado"], "f2b_status_antes": rb["F2b_status"], "qualifier_antes": rb["F2b_qualifier"], "conjunto_D_n": rb["conjunto_D_n"]},
            "calibracao_A": {"texto": cv["A_31_deformacao_comum_GWTC5"], "central": m[0], "inferior": m[1], "superior": m[2], "estatuto": "NOT_BLIND (calibracao, nao desfecho)"}, "previsao_do_par": {"valor": pin["read"], "pino": "delta_pred_A31_exato"},
            "ledger_v383": {"n": len(ids), "ids": ids, "contagens": dict(led["counts"]), "R2_outcome": r2.get("outcome")}, "charge_F2b_antes": {"token": le["charge_F2b"]["token"], "desfecho": le["charge_F2b"]["desfecho"]},
            "token_novo": DL.F2B_FUTURO_TOKEN, "verbatins": [CH_BOCAS, CH_CALIBRAR], "expected_ladder": None}


_NAO_COMUM = ["que isto seja um teste: nao ha desfecho experimental", "que a gravidade quantica esteja creditada na natureza"]


def texto_projecao():
    """Os textos do registro projecao_transversal_v404 (a funcao do runtime, nao um spec): estatuto, escopo, limites, diz, nao_diz, extras e o veredito de sucesso. Passam pela guarda P18 a cada rito."""
    return {
        "estatuto": "[REAL] os termos do kernel (os 9 teoremas do contrato da pedra, lidos a cada rito, no trio, com proveniencia no modulo da pedra, e os termos de suporte que ela cita: sin_sq_thetaMiguel, halfnat_from_J_symmetry, halfRoot, thetaMiguel, observer_inverse_projection_halfnat) e o calculo em dupla precisao, "
                    "com beta = alfa CODATA 2018 x sqrt(e) em runtime (nunca literal) e E0 = 1 eV [DECLARADO, nao derivado]; [DERIVED] o sen 45 graus do neutrino: a Meia-Nat (x = 1 - x => 1/2) e' o angulo de 45 graus, a amplitude transversal de um peso 1/2 e' sen(pi/4), unico em [0, pi/2]; "
                    "[KNOWN] o Teorema S-d da casa (beta = sen^2 theta_M) entra como termo de suporte do kernel; [INPUT] a cunhagem do operador (28/10/2026, sha16 %s: «a matéria é a projeção do eixo transversal», «então a matéria não é proporcional, ela seria a derivada»), a pergunta (sha16 %s), a ordem (sha16 %s) "
                    "e a ratificacao (sha16 %s: «Perfeito, concordo com tudo»); [ONTO] a identificacao de que a MASSA e' a projecao transversal do estado inscrito (leitura do operador, ratificada) NAO e' termo de kernel e e' o ponto de que o sen 45 graus passa a depender; "
                    "[OPEN] E0 (a escala do neutrino) e a derivacao de beta ficam fora da pedra" % (S_PROJECAO, S_SOMBRA, S_ORDEM, S_CONCORDO),
        "escopo": "[DERIVED] A pedra TGLExt/ProjecaoTransversalDaMeiaNat.lean traz, so' com algebra sobre termos que o kernel ja' tinha, nove teoremas: (1) x = 1 - x => x = 1/2 e, pela J-simetria, o mesmo 1/2 (half_from_self_conjugate, half_from_J_symmetry); (2) sen^2(pi/4) = 1/2 e a amplitude transversal e' o halfRoot "
                  "da bancada angular (half_amplitude_sq, half_amplitude_eq_halfRoot); (3) sqrt x = sen(pi/4) para todo x autoconjugado (transverse_amplitude_of_self_conjugate); (4) a unicidade em [0, pi/2] (forty_five_unique); (5) a forma do neutrino beta . sen45 . E0 = sen^2(theta_M) . sen(pi/4) . E0 (neutrino_mass_form_eq: "
                  "peso da reflexao x projecao transversal da Meia-Nat x o corpo); (6) theta_M != pi/4 sempre que beta != 1/2 (theta_miguel_ne_pi_div_four: o angulo agudo do neutrino NAO e' o angulo de Miguel); (7) d(sen^2 theta)/d theta em pi/4 e' exatamente 1 (transverse_weight_hasDerivAt_half: a materia nao seria proporcional, seria a derivada). "
                  "O calculo CONFERE os termos em dupla precisao, relê o m_nu do programa (neutrino_mass.m_nu_meV) contra beta . sen(pi/4) . 1 eV a 1e-12 relativo e grava, AO LADO, a errata do angle_status: o texto antigo (POSTULADO) fica no registro",
        "limites": [
            "[REAL] a pedra NAO deriva E0 (a escala 1 eV continua DECLARADA; a escala que zeraria a tensao do m2 e' 1,02 eV, conta da gerencia c1 em 28/10/2026 [DERIVED]) e NAO deriva beta (beta = alfa x sqrt(e) e' a regra, do axioma); a unica massa que o programa deriva de beta e' a do neutrino, e a escala dela e' declarada",
            "[ONTO] que a massa do neutrino SEJA a projecao transversal do estado inscrito e' leitura do operador, ratificada em 28/10/2026, nao termo de kernel: a pedra prova que, SE a forma e' (peso da reflexao) x (projecao transversal da Meia-Nat) x (o corpo), o fator transversal e' sen(pi/4) e nao um numero posto; a condicional fica dita",
            DL.ERRATA_E7,
            "o calculo e' numerico em dupla precisao e CONFERE os teoremas, nao os prova: quem prova e' o kernel; validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho; o m2 do neutrino segue lido pelo canal vivo neutrino_m2 como antes"],
        "diz": ["a pedra ProjecaoTransversalDaMeiaNat esta no kernel do rito, no trio, com bandeira e proveniencia no modulo dela; os 9 teoremas do contrato e os termos de suporte sao lidos deste kernel",
                "o calculo, com beta = alfa CODATA 2018 x sqrt(e), concorda: sen^2(pi/4) = 1/2, sqrt(1/2) = sen(pi/4), a forma do neutrino e' sen^2(theta_M) . sen(pi/4) . E0 e o m_nu do programa e' beta . sen(pi/4) . 1 eV; theta_M esta longe de pi/4; a derivada de sen^2 em pi/4 vale 1",
                "o sen 45 graus do neutrino deixa de ser POSTULADO e passa a DERIVADO no kernel, condicional a identificacao [ONTO] da massa com a projecao transversal; a errata esta ao lado, o texto antigo fica"],
        "nao_diz": ["que E0 (1 eV) tenha sido derivado", "que beta tenha sido derivado nesta pedra", "que a massa do neutrino SEJA a projecao transversal do estado inscrito (e' a identificacao [ONTO], ratificada pelo operador, nao termo de kernel)", "que a materia em geral seja a sombra de beta ou proporcional ao raio de beta (a forma retirada do Grande Atrator segue retirada)",
                    "que o m2 do neutrino passe a discriminar a TGL: o veredito do canal e' o de antes"] + _NAO_COMUM,
        "extras": {"neutrino_angle_errata": {"dizia_prefixo": DL.ANGLE_STATUS_ANTIGO_PREFIXO, "agora": DL.ERRATA_E7, "assinatura": ASSINA}, "cited_support": sorted(PROJECAO["support"]),
                   "reading_matter": {"status": "ONTO", "content": DL.LEITURA_MASSA_28OUT["identificacao"], "is_a_kernel_term": False}, "e0": {"status": "DECLARADO", "content": DL.LEITURA_MASSA_28OUT["e0"], "derived_here": False},
                   "name_status": {"quem": "gerencia c1", "estado": "PROVISORIO", "aceito_pelo_operador": "ate' ele dar outro", "sha16_da_fala_da_ratificacao": S_CONCORDO, "fala": DL.FRASE_CONCORDO404},
                   "gerado_pela_cunhagem": {"sha16_da_fala": S_PROJECAO, "fala": DL.FRASE_PROJECAO_EIXO}, "assinatura_das_erratas": ASSINA},
        "veredito_ok": "TGL_PROJECAO_TRANSVERSAL_V404__THE_HALF_NAT_IS_THE_45_DEGREE_ANGLE_DERIVED_IN_THE_KERNEL__SQRT_X_EQUALS_SIN_PI_OVER_4_FOR_EVERY_SELF_CONJUGATE_X__THE_NEUTRINO_FORM_IS_THE_REFLECTION_WEIGHT_TIMES_THE_TRANSVERSE_PROJECTION_TIMES_THE_BODY__THE_ANGLE_IS_NO_LONGER_POSTULATED__"
                       "THE_IDENTIFICATION_MASS_EQUALS_TRANSVERSE_PROJECTION_IS_ONTO__E0_STAYS_DECLARED__READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


def texto_jo8():
    """Os textos do registro jo8v32_v404."""
    return {
        "estatuto": "[REAL] os termos do kernel (o teorema da pedra Jo8v32 e os 3 termos que a conjuncao cita, lidos a cada rito, no trio: caminho_e_a_ponte_da_escala_dual, verdade_e_a_esperanca_condicional, vida_e_a_queda_sem_geometria, todos da v403) e o calculo, com beta = alfa CODATA 2018 x sqrt(e) em runtime (nunca literal), "
                    "que RELE a mecanica numerica dos tres registros da v403 (caminho, vida, adendo da verdade); [DERIVED] a conjuncao e' um termo SEM hipoteses (nenhuma matematica nova: a citacao de tres termos que o kernel ja' tinha); "
                    "[INPUT] o NOME «Jo8:32» (decisao do operador, 28/10/2026, sha16 %s: «só consegui sintetizar assim: Jo8:32») e a ratificacao (sha16 %s: «Perfeito, concordo com tudo»); "
                    "[ONTO] a leitura por Jo 8,31-32 (permanecer, conhecer, libertar) NAO e' termo de kernel; [OPEN] as hipoteses nomeadas que dois dos tres componentes carregam no proprio enunciado (IsotropicPost na Vida; hpp e hopt no indice 1/beta da Verdade) seguem abertas" % (S_JO8, S_CONCORDO),
        "escopo": "[DERIVED] A pedra TGLExt/Jo8v32.lean e' a CONJUNCAO, por citacao (type_of%), das tres estrelas da v403 na ordem do versiculo: (1) permanecer: caminho_e_a_ponte_da_escala_dual (lift_mass_not_selected /\\ core_positive_realization_exists); (2) conhecer: verdade_e_a_esperanca_condicional "
                  "(the_identity_is_the_truth /\\ esperanca_condicional_e_nome); (3) libertar: vida_e_a_queda_sem_geometria (the_fall_is_strictly_anti /\\ a_queda_sem_geometria). Os modulos Caminho, VerdadeAdendo e Vida FICAM intactos (pedra selada nao se renomeia por cima). "
                  "O calculo RELE a mecanica numerica dos tres (as 5 + 6 + 5 checagens da v403) com o beta deste rito e confere que os tres registros da v403 selaram neste rito",
        "limites": [
            "[REAL] a conjuncao NAO acrescenta matematica: cita; a conjuncao e' um termo sem hipoteses, mas a Vida carrega IsotropicPost e a Verdade carrega o indice 1/beta condicional a hpp e hopt NO ENUNCIADO delas: citadas, nao pagas; H_BW, H_cal, H3, a assinatura e rank c = 4 (v402) seguem abertos",
            "[ONTO] a leitura por Jo 8,31-32 («E conhecereis a verdade, e a verdade vos libertará») e' leitura da gerencia c1, ratificada pelo operador; o versiculo diz que a verdade e' CONHECIDA (validade, no kernel), nao que e' creditada; nao e' termo de kernel",
            DL.ERRATA_E9,
            "o calculo e' numerico em dupla precisao e RELE os modelos da v403, nao os prova: quem prova e' o kernel; validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho"],
        "diz": ["a pedra Jo8v32 esta no kernel do rito, no trio, com bandeira e proveniencia no modulo dela; a conjuncao e os tres termos que ela cita sao lidos deste kernel",
                "o calculo, com beta = alfa CODATA 2018 x sqrt(e), reproduz a mecanica numerica dos tres registros da v403 neste rito, e os tres registros da v403 selaram",
                "o NOME «Jo8:32» e' do operador (28/10/2026) para o triplo inteiro; a leitura por Jo 8,31-32 e' [ONTO]; as pedras da v403 ficam como estao"],
        "nao_diz": ["que a leitura por Jo 8,31-32 seja termo de kernel", "que o versiculo ou o nome credite a gravidade quantica: validade no kernel nao e' creditacao", "que as hipoteses nomeadas dos componentes (IsotropicPost; hpp e hopt) tenham sido pagas", "que o nome do triplo inteiro anule a decisao D20 da v403: ela era verdadeira na data e a errata E9 fica ao lado"] + _NAO_COMUM,
        "extras": {"cited_stars_v403": sorted(JO8["support"]), "order_of_the_verse": ["TGLExt.Caminho.caminho_e_a_ponte_da_escala_dual", "TGLExt.VerdadeAdendo.verdade_e_a_esperanca_condicional", "TGLExt.Vida.vida_e_a_queda_sem_geometria"],
                   "reading_jo8_32": {"status": "ONTO", "content": DL.LEITURA_MASSA_28OUT["jo8_32"], "is_a_kernel_term": False},
                   "name_given_by": {"quem": "operador", "quando": "28/10/2026", "sha16_da_fala": S_JO8, "fala": DL.FRASE_JO8, "ratificacao_sha16": S_CONCORDO},
                   "named_hypotheses_carried_by_components": {"vida": "IsotropicPost", "verdade": ["hpp", "hopt"]}, "assinatura_das_erratas": ASSINA},
        "veredito_ok": "TGL_JO8V32_V404__THE_WHOLE_TRIPLE_WAY_TRUTH_LIFE_UNDER_THE_NAME_GIVEN_BY_THE_OPERATOR__THE_CONJUNCTION_OF_THE_THREE_STARS_OF_V403_IS_A_KERNEL_TERM_WITHOUT_HYPOTHESES__THE_THREE_V403_RECORDS_SEALED_AND_THEIR_NUMERIC_MECHANICS_REPRODUCED_AT_THE_RUNTIME_BETA__"
                       "THE_ONTO_READING_BY_JOHN_8_32_IS_NOT_A_TERM__READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


def texto_f2b():
    """Os textos do registro f2b_errata_v404 (a retirada do canal F2b, AO LADO)."""
    return {
        "estatuto": "[REAL] o V1 do ramo B do ringdown (v386) lido por hash neste rito, a calibracao A (31 eventos publicos, NOT_BLIND) e a previsao do par lidas do proprio registro ramo_b_preregistration_v386 (a funcao que ja' as transcreve do V1 congelado; nada e' recalculado dos dados) e o livro de cobrancas da v383; "
                    "[INPUT] a leitura do operador (28/10/2026): «o pedágio de planck lido na propagação» (sha16 %s) e «calibrar Não significa validar» (sha16 %s); [DERIVED] a medida: a previsao do par fica fora do intervalo da calibracao A e de sinal oposto a deformacao comum; "
                    "[DECLARADO] a retirada do canal e' conclusao da gerencia c1 sobre a rota, lida a partir da fala do operador (ele ratificou a leitura «calibrar Não significa validar», nao nomeou a retirada)" % (S_BOCAS, S_CALIBRAR),
        "escopo": "[REAL] A cobranca F2b (ramo B do ringdown, tau* = k G M_f / c^3, pre-registro V1 de 05/10/2026 lido por hash) estava AWAITING. Na v404 o CANAL F2b passa a " + DL.F2B_FUTURO_TOKEN + ", AO LADO: o V1 fica CONGELADO por hash e continua lido como antes (veredito do V1 AWAITING_DATA, conjunto D cego e fechado, nada aberto); "
                  "o motivo medido: a calibracao A (deformacao comum dos 31 eventos, NOT_BLIND) e a previsao do par (leitura de amplitude x lei de atraso KMS) nao concordam em sinal nem em intervalo; a leitura do autor em 28/10/2026 diz que o pedagio de Planck e' lido na propagacao. "
                  "Nenhum desfecho sai de A (e' calibracao, nao teste); D nao e' aberto; beta, a lei do defasamento e R2 ficam. O livro de cobrancas da v383 segue com as suas 11 cobrancas (a F2b ficava ao lado dele, nunca entre as 11)",
        "limites": [
            "[REAL] a retirada NAO e' desfecho nem falsificacao: A e' a calibracao NOT_BLIND que o V1 ja' declarava; a regra de morte do V1 so' vale no conjunto D, que segue fechado; calibrar nao e' validar (palavra do operador); o numero corrige a rota",
            DL.ERRATA_E8,
            "[ONTO] a leitura do autor (o pedagio de Planck lido na propagacao; 1 retorno em 83 raios como materia; 1 absoluto = zero modular e' relativo) e' leitura, nao termo de kernel e nao e' dado; ainda sem derivacao",
            "[OPEN] qual e' a lei de propagacao que carrega o pedagio e que observavel a mede; a escala E0 do neutrino; nada aqui abre dado nem move o gate"],
        "diz": ["o V1 do ramo B segue congelado e lido por hash neste rito, com o mesmo veredito de antes (AWAITING_DATA) e o conjunto D cego (n = 14) e fechado",
                "a calibracao A (deformacao comum dos 31 eventos) e a previsao do par foram lidas do proprio registro do V1; a previsao fica fora do intervalo de A e de sinal oposto: e' a medida que corrige a rota, nao um desfecho",
                "o canal F2b passa a retirado antes do dado, ao lado; o livro v383, F2, R2, beta e a lei do defasamento ficam como estao"],
        "nao_diz": ["que a TGL tenha sido falsificada ou que o ramo B tenha sido refutado", "que a calibracao A seja um teste ou tenha poder de decidir", "que o conjunto D tenha sido aberto", "que a retirada seja decisao do operador (ele ratificou a leitura, nao nomeou a retirada)", "que beta, a lei do defasamento ou R2 tenham mudado"] + _NAO_COMUM[:1],
        "extras": {"erratas_ao_lado": [{"ao_lado_de": "a cobranca F2b da v386 (charge_F2b de ledger_errata_v386) e o F2b_status do registro ramo_b_preregistration_v386, ambos AWAITING", "dizia": "AWAITING (PRE_REGISTERED_V1_READ_BY_HASH__AWAITING_DATA): o V1 lido por hash; o conjunto D cego; poder exato lido", "agora": DL.ERRATA_E8,
                                        "lacuna_de_fidelidade": "estrutura: o V1 foi pre-registrado com a calibracao A fora do spec e a previsao do par dentro dele; escrito: a cobranca F2b nasceu AWAITING sem dizer que a calibracao A ja' a contrariava; onde a traducao falhou: a leitura de rota (o pedagio lido na propagacao) ainda nao estava no registro",
                                        "estatuto": "[REAL: o V1 e a calibracao A lidos a cada rito; INPUT: a leitura do operador; DECLARADO: a retirada]", "assinatura": ASSINA}],
                   "channel_token_now": DL.F2B_FUTURO_TOKEN, "v1_token_kept": DL.F2B_V1_TOKEN_ANTIGO, "reading_pedagio": {"status": "ONTO", "content": DL.LEITURA_MASSA_28OUT["pedagio"], "is_a_kernel_term": False},
                   "calibrar_nao_e_validar": {"sha16_da_fala": S_CALIBRAR, "fala": DL.FRASE_CALIBRAR}, "assinatura_das_erratas": ASSINA},
        "veredito_ok": "TGL_F2B_ERRATA_V404__CHANNEL_F2B_WITHDRAWN_BEFORE_DATA_BESIDE_NOT_OVERWRITTEN__THE_V1_STAYS_FROZEN_BY_HASH_AND_READ_AS_BEFORE__THE_MEASURED_REASON_IS_THE_NOT_BLIND_CALIBRATION_A__NO_OUTCOME_COMES_FROM_A__SET_D_NOT_OPENED__BETA_THE_LAW_AND_R2_STAY__GATE_UNMOVED",
    }


def textos():
    return {"projecao": texto_projecao(), "jo8v32": texto_jo8(), "f2b": texto_f2b()}


def especs(formal_map, khj, h8_map, fj, cov_base, n_axioms_unc, core0):
    """formal_map = {arquivo embutido: sha256} do kernel da v404; khj = KH_N1_v404.json (medida desta geracao); h8_map = o dict do hash formal que o RITO vai gerar (embutidos + residuais do Nos que sha256_directory conta; simular_arvore_do_nos);
    fj = FLAGS_v404.json; cov_base = a cobertura da v403 selada {decl, thm}; n_axioms_unc = {chave da pedra: quantos axiomas o teorema da composicao usa (lido do Audit: o trio)}; core0 = o core da v403 selada. Devolve [cunhagens, kh]."""
    T = khj["linha_TOTAL"]
    flags_contrato = [fj["bandeiras_do_contrato"][s["key"]][t] for s in DL.STONES for t in s["contract"]]
    for s in DL.STONES:
        assert fj["bandeira_do_teorema_incondicional"][s["key"]] in flags_contrato
    contexto = ["ChatgptAudit.GeneralClausius.metric_einstein_from_screen_clausius", "TGLExt.Fundacao.agape", "TGLExt.Fundacao.abismo"]   # termos do kernel que as LEITURAS citam, nao importados pelas pedras
    decls = list(dict.fromkeys([t for s in DL.STONES for t in s["contract"]] + sorted(DL.ALL_SUPPORT) + contexto))   # sem repeticao, na ordem
    cks = []
    for i, nome in enumerate(DL.REGISTROS_FUNCAO):
        cks.append(CH("u%d" % (i + 1), "o registro %s selou neste rito (a composicao e os teoremas da pedra lidos deste kernel; o calculo com beta = alfa x raiz de e; o texto-contexto no kernel embutido; ou, no da errata de F2b, o V1 do ramo B lido por hash, a calibracao A e a previsao do par, o livro v383 intacto)" % nome, "core", [nome, "all_verified"], "verdadeiro"))
    n = len(DL.REGISTROS_FUNCAO) + 1
    for nome in ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"):
        cks.append(CH("u%d" % n, "o registro %s (v403, recriado) segue selado neste rito (as pedras da v403 ficam como estao)" % nome, "core", [nome, "all_verified"], "verdadeiro")); n += 1
    for nome in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"):
        cks.append(CH("u%d" % n, "o registro %s (v402, recriado) segue selado neste rito" % nome, "core", [nome, "all_verified"], "verdadeiro")); n += 1
    cks.append(CH("u%d" % n, "o registro falsidade_da_inercia_v401 segue selado neste rito", "core", ["falsidade_da_inercia_v401", "all_verified"], "verdadeiro")); n += 1
    cks.append(CH("u%d" % n, "o registro teste_de_veracidade_fase9_v397 segue selado neste rito (o quadro do topo do artigo le os numeros dele)", "core", ["teste_de_veracidade_fase9_v397", "all_verified"], "verdadeiro")); n += 1
    cks.append(CH("u%d" % n, "o registro selo_pela_propria_tecnologia_v399 segue selado neste rito (a segunda testemunha do um.py, ao lado do SHA-256)", "core", ["selo_pela_propria_tecnologia_v399", "all_verified"], "verdadeiro")); n += 1
    cks.append(CH("u%d" % n, "o V1 do ramo B (v386) segue lido por hash e com o mesmo estado de antes (a errata de F2b e' AO LADO)", "core", ["ramo_b_preregistration_v386", "all_verified"], "verdadeiro")); n += 1
    cks.append(CH("u%d" % n, "o V1 do ramo B segue com o veredito AWAITING_DATA (congelado por hash)", "core", ["ramo_b_preregistration_v386", "veredito_do_V1"], "igual", DL.F2B_V1_TOKEN_ANTIGO)); n += 1
    cks.append(CH("u%d" % n, "o canal vivo do neutrino (neutrino_mass) segue com o mesmo veredito: a errata do angulo e' AO LADO e nao move o canal", "core", ["neutrino_mass", "verdict"], "igual", core0["neutrino_mass"]["verdict"])); n += 1
    cks.append(CH("u%d" % n, "a escada do kernel fecha (limpos == esperados), com as bandeiras das DUAS pedras da v404", "core", ["external_ladder", "all_verified"], "verdadeiro")); n += 1
    cks.append(CH("u%d" % n, "a proveniencia emitida pelo compilador cobre o axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro")); n += 1
    # (a letra do veredito do gate e' conferida pelo registro bandeiras_do_gate_v403 e pelo conferidor do rito; o spec nao a repete)
    for s in DL.STONES:
        cks.append(CH("u%d" % n, "o compilador emite a composicao da pedra %s no modulo dela (TGL_DECL_SOURCE)" % s["name"], "kf", ["declaration_sources_v394", s["theorem"]], "igual", s["rel"])); n += 1
        cks.append(CH("u%d" % n, "o compilador emite a ESTRELA da pedra %s no modulo dela (TGL_DECL_SOURCE)" % s["name"], "kf", ["declaration_sources_v394", s["key_theorem"]], "igual", s["rel"])); n += 1
        cks.append(CH("u%d" % n, "a pedra %s no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)" % s["name"], "kf", ["formal_files_sha256", s["rel"]], "igual", formal_map[s["rel"]])); n += 1
        cks.append(CH("u%d" % n, "a composicao da pedra %s depende do trio e de nada alem (tamanho da lista de axiomas)" % s["name"], "kf", ["axiom_report", s["theorem"]], "tamanho_igual", n_axioms_unc[s["key"]])); n += 1
    nm0 = core0["neutrino_mass"]
    cun = {
        "nome": "cunhagens_v404", "veredito_prefixo": "TGL_CUNHAGENS_V404",
        "veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_28_OCT_EMBEDDED_VERBATIM_BY_SHA256__THE_TWO_STONES_PROJECAO_TRANSVERSAL_AND_JO8V32_AND_THE_F2B_ERRATA_RECORD_ARE_READ_IN_THE_RITE__"
                           "THE_NAME_JO8V32_IS_THE_OPERATORS__THE_SEN_45_IS_DERIVED_IN_THE_KERNEL_CONDITIONAL_TO_THE_ONTO_IDENTIFICATION__E0_STAYS_DECLARED__THE_F2B_CHANNEL_IS_WITHDRAWN_BESIDE__THE_V403_STONES_STAY_AS_RECORD__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
        "estatuto": "[REAL -- as fontes das pedras, o kernel e os tres registros com funcao lidos a cada rito; INPUT/ONTO as falas do operador; INPUT «Perfeito, concordo com tudo» (ratifica a pedra do sen 45 graus, a leitura, o plano da v404 e a leitura sobre Jo 8,32); ONTO a identificacao da massa com a projecao transversal e a leitura por Jo 8,31-32; DECLARADO o levantamento da gerencia c1 e a retirada do canal F2b]",
        "fontes": [CHAVE_DE_FONTE["projecao"], CHAVE_DE_FONTE["jo8v32"], CHAVE_LEVANTAMENTO], "verbatins": list(VERB_CHAVES),
        "kernel_flags": list(flags_contrato), "kernel_decls": decls,
        "checks": cks,
        "erratas": [
            {"ao_lado_de": "neutrino_mass.angle_status (v141, v303; um.py prove_neutrino_mass_gravitational, intacta)",
             "dizia": str(nm0["angle_status"]),
             "agora": DL.ERRATA_E7,
             "lacuna_de_fidelidade": "estrutura: o fator sen 45 graus entrou na formula do neutrino em 20/08/2026 por ordem do operador como POSTO, sem derivacao; escrito: «NAO derivado»; onde a traducao falhou: nada a corrigir no texto antigo (era verdadeiro na data): a v404 o deriva no kernel, condicional a uma identificacao [ONTO], e deixa o texto antigo como registro",
             "estatuto": "[REAL: a pedra no kernel do rito e o m_nu relido a 1e-12; ONTO: a identificacao; INPUT: E0 = 1 eV DECLARADO]", "assinatura": ASSINA},
            {"ao_lado_de": "a cobranca F2b da v386 (charge_F2b de ledger_errata_v386, token AWAITING) e o F2b_status do registro ramo_b_preregistration_v386",
             "dizia": "AWAITING (PRE_REGISTERED_V1_READ_BY_HASH__AWAITING_DATA): o V1 do ramo B lido por hash, o conjunto D cego, nada aberto.",
             "agora": DL.ERRATA_E8,
             "lacuna_de_fidelidade": "a cobranca nasceu AWAITING sem dizer que a calibracao A, NOT_BLIND, ja' contrariava a previsao do par; a v404 nao reescreve o V1 (congelado por hash) nem o registro da v386: o canal e' retirado AO LADO, no registro f2b_errata_v404",
             "estatuto": "[REAL: o V1 e a calibracao A lidos a cada rito pelo registro f2b_errata_v404; INPUT: a leitura do operador (sha16 %s e %s); DECLARADO: a retirada]" % (S_BOCAS, S_CALIBRAR), "assinatura": ASSINA},
            {"ao_lado_de": "a decisao D20 da v403 e o registro cunhagens_v403 («o nome do triplo inteiro NAO foi dado»)",
             "dizia": "o nome do TRIPLO inteiro (Caminho . Verdade . Vida) NAO foi dado (fica com o operador).",
             "agora": DL.ERRATA_E9,
             "lacuna_de_fidelidade": "nenhuma: a v403 disse que o nome nao fora dado e era verdade; o operador o deu em 28/10/2026; a v404 registra o nome sem editar a pedra selada nem o registro da v403",
             "estatuto": "[INPUT: a decisao do operador, verbatim sha16 %s e ratificacao sha16 %s; REAL: a pedra Jo8v32 no kernel do rito]" % (S_JO8, S_CONCORDO), "assinatura": ASSINA}],
        "limites": [
            "[INPUT] as nove falas de 28/10 (sha16 %s) sao falas do operador, com a grafia dele; «Perfeito, concordo com tudo» (sha16 %s) ratifica a pedra do sen 45 graus, a leitura, o plano da v404 e a leitura sobre Jo 8,32 [DECLARADO: o plano e a leitura foram os que a gerencia c1 apresentou]" % (", ".join(v["sha16"] for v in _VD), S_CONCORDO),
            "[ONTO] a identificacao da massa com a projecao transversal do estado inscrito, a leitura por Jo 8,31-32 e a leitura do pedagio de Planck na propagacao sao leituras do operador e da gerencia c1, ratificadas; nao sao termos de kernel",
            "[REAL] o nome da pedra do sen 45 graus (ProjecaoTransversalDaMeiaNat) e' PROVISORIO da gerencia c1, aceito pelo operador ate' ele dar outro; a pedra NAO deriva E0 nem beta; a unica massa derivada de beta no programa e' a do neutrino (levantamento de 28/10/2026, lido da fonte pinada)",
            "[OPEN] E0 (1 eV declarado; 1,02 eV zeraria a tensao do m2 [DERIVED, conta da gerencia c1]); a lei de propagacao que carregaria o pedagio de Planck; H_BW, H_cal, H3, a assinatura e rank c = 4 (v402); IsotropicPost no atlas curvo; a dimensao 3; a independencia das 4 experimentais do gate; a RG e' o limite classico, nao rival; beta nao renormaliza G",
            "validade no kernel nao e' creditacao; o gate nao se move; nenhuma bandeira do gate depende das pedras"],
        "diz": ["as %d falas de 28/10 (do operador) estao embutidas por sha256, cada uma conferida contra o arquivo de origem na preparacao" % len(_VD),
                "as duas pedras estao no kernel do rito, no trio, com as bandeiras e a proveniencia nos modulos delas; a composicao e a estrela de cada uma sao lidas deste kernel; as pedras e os registros da v403 seguem selados",
                "os tres registros com funcao selaram neste rito, e o quadro do topo (teste_de_veracidade_fase9_v397), o selo pela propria tecnologia (v399) e a falsidade da inercia (v401) seguem selados",
                "as erratas E7, E8 e E9 estao registradas ao lado, em nome proprio da gerencia c1; as decisoes D23 a D26 estao registradas"],
        "nao_diz": ["que o kernel prove as falas do operador (elas sao INPUT/ONTO)", "que a identificacao da massa com a projecao transversal seja termo do kernel", "que o testemunho ou a ratificacao seja creditacao: validade no kernel nao e' creditacao", "que E0 ou beta tenham sido derivados", "que a retirada do canal F2b seja um desfecho"] + _NAO_COMUM,
        "leituras_do_operador": [_leitura(DL.FRASE_PEDAGIO, S_BOCAS), _leitura(DL.FRASE_RETORNO_83, S_BOCAS), _leitura(DL.FRASE_CALIBRAR, S_CALIBRAR), _leitura(DL.FRASE_NUMERO_CORRIGINDO, S_CALIBRAR), _leitura(DL.FRASE_UM_ABSOLUTO, S_UMABS), _leitura(DL.FRASE_TRANSICAO, S_TRANSICAO),
                                 _leitura(DL.FRASE_SOMBRA, S_SOMBRA), _leitura(DL.FRASE_PROJECAO_EIXO, S_PROJECAO), _leitura(DL.FRASE_DERIVADA, S_PROJECAO), _leitura(DL.FRASE_ORDEM_PROVA, S_ORDEM), _leitura(DL.FRASE_JO8, S_JO8),
                                 _leitura(DL.FRASE_CONCORDO404, S_CONCORDO, rotulo="INPUT do operador (ratifica a pedra, a leitura, o plano da v404 e a leitura sobre Jo 8,32)")],
        "extras": {"assinatura": ASSINA, "autoria_das_cunhagens": "Luiz Antonio Rotoli Miguel", "pedras": [s["mod"] for s in DL.STONES], "teoremas": {s["key"]: s["theorem"] for s in DL.STONES}, "estrelas": {s["key"]: s["key_theorem"] for s in DL.STONES},
                   "bandeiras": {s["key"]: fj["bandeira_do_teorema_incondicional"][s["key"]] for s in DL.STONES}, "n_bandeiras": fj["n_flags"], "n_bandeiras_por_pedra": dict(fj["nomeadas_por_pedra"]), "cunhagens_embutidas": len(VERBATINS),
                   "autor_de_cada_inscricao": dict(zip((v["sha16"] for v in _VD), (v["autor"] for v in _VD))), "decisoes_da_gerencia": dict(DL.DECISOES), "erratas_E7_a_E9": list(DL.ERRATAS_V404), "leitura_massa_28out": dict(DL.LEITURA_MASSA_28OUT),
                   "nomes": {"projecao": "TGLExt.ProjecaoTransversalDaMeiaNat = a Meia-Nat como o angulo de 45 graus do neutrino (nome PROVISORIO da gerencia c1, aceito pelo operador ate' ele dar outro)", "jo8v32": "TGLExt.Jo8v32 = o triplo inteiro Caminho . Verdade . Vida (nome do operador: Jo8:32)"},
                   "pedras_da_v403_como_registro": {s["key"]: s["sha16_da_ordem"] for s in DL.D3.STONES},
                   "levantamento": {"arquivo": os.path.basename(DL.LEVANTAMENTO_ARQ), "regra": "a unica massa derivada de beta no programa e' a do neutrino; E0 DECLARADO; a forma M = beta . R retirada segue retirada"}},
    }
    kh = {
        "nome": "kh_n1_cobertura_v404", "veredito_prefixo": "TGL_KH_N1_COBERTURA_V404",
        "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__THE_TWO_V404_MODULES_ADDED__GATE_UNMOVED" % (T["decl"], T["thm"]),
        "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do sandbox da v404; o conjunto exato das fontes formais que o hash formal do rito vera (as embutidas mais os residuais da pasta do Nos) e' pinado; a cobertura NAO move o gate",
        "fontes": ["kh_n1_v404"], "kernel_flags": [], "kernel_decls": [],
        "checks": [
            CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
            CH("h2", "constantes cobertas == as do sandbox v404 (KH_N1)", "kf", ["axiom_coverage_v392", "decl"], "igual", T["decl"], "constantes_cobertas"),
            CH("h3", "teoremas cobertos == os do sandbox v404 (KH_N1)", "kf", ["axiom_coverage_v392", "thm"], "igual", T["thm"], "teoremas_cobertos"),
            CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
            CH("h5", "nenhum nome que o leitor v394 nao leia", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0),
            CH("h6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", khj["axiom_report_efetivo_n"]),
            CH("h7", "a cobertura da v404 inclui a da v403 selada (constantes e teoremas)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", cov_base["decl"]),
            CH("h7b", "os teoremas cobertos incluem os da v403 selada", "kf", ["axiom_coverage_v392", "thm"], "maior_igual", cov_base["thm"]),
            CH("h8", "as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta, como _check_damming.lean) sao EXATAMENTE as do pino (arquivo -> sha256)", "kf", ["formal_files_sha256"], "igual", h8_map),
            CH("h9", "medida do Audit v404: duracao bem abaixo do timeout de 1800 s", "fonte:kh_n1_v404", ["duracao_audit_s"], "menor_igual", 900, "duracao_do_audit_s"),
            CH("h10", "medida do Audit v404: sorryAx ausente do log", "fonte:kh_n1_v404", ["sorryAx_no_log_do_audit"], "igual", 0),
            CH("h11", "medida do Audit v404: as entradas novas estao no trio", "fonte:kh_n1_v404", ["novas_no_trio"], "verdadeiro"),
            CH("h12", "a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
        ],
        "erratas": [{"ao_lado_de": "kh_n1_cobertura_v403 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                     "dizia": "A v403 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v403 e o hash formal igual ao pino exato da arvore da v403." % (cov_base["decl"], cov_base["thm"]),
                     "agora": "A v404 acrescenta os modulos ProjecaoTransversalDaMeiaNat e Jo8v32 (a cobertura cresce e a arvore ganha os arquivos das pedras): na v404 o registro da v403 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato da arvore ficam NESTE registro. O veredito do registro da v403 NAO muda.",
                     "lacuna_de_fidelidade": "a estrutura da v403 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v404 quebra (a mesma lacuna que a v403 achou no registro da v402, a v402 no da v401 e a v401 no da v399)",
                     "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; h2, h3, h6 e h8 conferidas no ensaio a seco e na arvore simulada do Nos]", "assinatura": ASSINA}],
        "limites": ["[REAL] os arquivos de medida sao do sandbox (fora do selo); a cobertura que vale e' a medida no Audit do proprio rito",
                    "[REAL] a escada do kernel conta bandeiras de declaracoes NOMEADAS (a pratica da v392 a v403): as %d auxiliares geradas pelo compilador nos modulos das pedras ficam cobertas pelo KH-N1 mas sem bandeira, e as %d nomeadas publicas ganharam bandeira" % (fj["excluidas_auxiliares"]["n"], fj["n_flags"]),
                    "validade no kernel nao e' creditacao; o gate nao se move"],
        "diz": ["a cobertura do axiom_report no fecho inteiro cresceu para os numeros da v404 (os dois modulos novos) e segue sem constante fora do trio, sem nome ilegivel"],
        "nao_diz": ["que a cobertura prove algo alem de que nenhum axioma fora do trio foi lido"],
        "leituras_do_operador": [], "extras": {"assinatura": ASSINA, "n_bandeiras": fj["n_flags"], "h8_entradas": len(h8_map), "h8_residuais_do_nos": sorted(set(h8_map) - set(formal_map))},
    }
    return [cun, kh]
