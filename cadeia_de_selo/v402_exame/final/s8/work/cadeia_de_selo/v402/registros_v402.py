# -*- coding: utf-8 -*-
"""registros_v402.py -- os dados dos registros da v402: FONTES pinadas por sha256 (lidas do disco pelo montador, nunca digitadas), VERBATINS (as TRES inscricoes de 26/10/2026 ainda nao embutidas, todas falas do operador; EMBUTIDAS: a fala embutida manda,
o arquivo e' so' informativo), os CONTRATOS e os TEXTOS dos TRES registros com FUNCAO (`ponte_da_escala_dual_v402`, `queda_sem_geometria_v402`, `esperanca_condicional_v402`: gerar_candidato_v402.py os emite a partir de runtime_v402.py; cada contrato sai de contrato() abaixo,
DERIVADO do build do sandbox) e os dois SPECS interpretados pelo MOTOR _v392_registro (`cunhagens_v402` e `kh_n1_cobertura_v402`). Fontes so' em pasta DURAVEL: tudo vem de cadeia_de_selo\\v402\\insumos. Texto novo passa pela guarda P18 (a cada rito).
A PONTE (modulo do Codex, ORDEM 025; exame independente INTEGRAR_COM_ERRATA_AO_LADO) entra COM as erratas E1-E4 ao lado (em nome proprio da gerencia c1): H_tau na forma literal e' REFUTADA no kernel; o que continua NOMEADO e' H_BW, H_cal, H3, a assinatura e rank c = 4.
Molde: registros_v401.py."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v402 as DL  # noqa: E402

INS = os.path.join(HERE, "insumos")
ASSINA = DL.ASSINA
PONTE, QUEDA, ESPERANCA = DL.STONE_BY_KEY["ponte"], DL.STONE_BY_KEY["queda"], DL.STONE_BY_KEY["esperanca"]
CHAVE_DE_FONTE = {"ponte": "ponte_pedra", "queda": "queda_pedra", "esperanca": "esperanca_pedra"}

FONTES = [{"chave": CHAVE_DE_FONTE["ponte"], "arquivo": os.path.join(INS, PONTE["insumo"]), "papel": "a pedra TGLExt/PonteDaEscalaDual.lean (modulo do Codex, ORDEM 025, sha16 da ordem da gerencia 0e55b6e448adbd91; copia de bytes, sem edicao; maxHeartbeats 2000000 dito; copia duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)"},
          {"chave": CHAVE_DE_FONTE["queda"], "arquivo": os.path.join(INS, QUEDA["insumo"]), "papel": "a pedra TGLExt/QuedaSemGeometria.lean (nome PROVISORIO; compilada e provada no sandbox; copia duravel; a que vale no rito e' a EMBUTIDA no kernel)"},
          {"chave": CHAVE_DE_FONTE["esperanca"], "arquivo": os.path.join(INS, ESPERANCA["insumo"]), "papel": "a pedra TGLExt/EsperancaCondicional.lean (nome PROVISORIO; compilada e provada no sandbox; copia duravel; a que vale no rito e' a EMBUTIDA no kernel)"},
          {"chave": "kh_n1_v402", "arquivo": os.path.join(INS, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox da v402 (pos_build_kernel_v402.py)"},
          {"chave": "adendo_v402", "arquivo": os.path.join(INS, "adendo", os.path.basename(DL.ADENDO_ARQ)), "papel": "o ADENDO de 03-04/09/2026 (Nos\\ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md; copia duravel; o original no Nos NAO e' tocado): as dividas da assinatura e do rank c = 4 que a ponte NAO paga, e o titulo do escriba «Lorentz vem da queda da fase» (E5)"}]


def _trecho(t):
    s = t.strip().splitlines()[0].strip() if t.strip() else ""
    s = s[:48].rstrip()
    assert s and s in t, s
    return s


_VD = DL.verbatins402(os.path.join(INS, "cunhagens"))
VERBATINS = [{"chave": v["chave"], "arquivo": v["arquivo"], "quando": v["quando"], "trechos": [_trecho(v["text"])], "papel": v["papel"], "fonte_original": v["fonte_original"]} for v in _VD]
VERB_CHAVES = [v["chave"] for v in _VD]
SHA16 = {os.path.basename(v["fonte_original"]): v["sha16"] for v in _VD}
S_ESPERANCA, S_QUEDA, S_PROSSIGA = tuple(v["sha16"] for v in _VD)          # LIDOS dos arquivos, na ordem de DL.VERBATIM_ORIGEM_V402 (o unpack recusa outro numero)
CH_ESPERANCA, CH_QUEDA, CH_PROSSIGA = tuple(v["chave"] for v in _VD)
TEXTOS = {v["sha16"]: v["text"] for v in _VD}
ADENDO_TXT = open(DL.ADENDO_ARQ, "rb").read().decode("utf-8")
ADENDO_SHA16 = DL.sha256(open(DL.ADENDO_ARQ, "rb").read())[:16]
assert ADENDO_SHA16 == DL.ADENDO_SHA16_DA_ORDEM
ADENDO_DIVIDA_1 = "DÍVIDA 1 — ASSINATURA"                                      # verbatim no adendo (o titulo da divida)
ADENDO_DIVIDA_2 = "DÍVIDA 2 — O QUATRO"
ADENDO_TITULO_E5 = "Lorentz vem da queda da fase"                              # o TITULO do escriba em E5 do adendo (NAO e' fala do operador)
assert ADENDO_DIVIDA_1 in ADENDO_TXT and ADENDO_DIVIDA_2 in ADENDO_TXT and ADENDO_TITULO_E5 in ADENDO_TXT
CH = lambda id_, desc_, onde_, caminho_, op_, valor_=None, cap_=None, est_="[REAL]": dict(id=id_, descricao=desc_, onde=onde_, caminho=caminho_, op=op_, **({"valor": valor_} if valor_ is not None else {}), **({"capturar": cap_} if cap_ else {}), estatuto=est_)


def _leitura(trecho, sha16, quando="26/10/2026", rotulo="INPUT/ONTO do operador"):
    assert trecho in TEXTOS[sha16], ("a leitura do operador NAO esta verbatim na fala", sha16, trecho)
    return {"trecho": trecho, "estatuto": "[%s, verbatim %s, sha16 %s]" % (rotulo, quando, sha16)}


# o texto-CONTEXTO que cada registro confere no kernel embutido do proprio rito (analogo do 0_abs da v401): lido do corpo embutido, nao digitado como prova
CONTEXTO = {"ponte": {"path": "TGLExt/BisognanoWichmann.lean", "needles": ["Bisognano", "U(Λ_W(2πt))"]},
            "queda": {"path": "TGLExt/Fundacao.lean", "needles": ["não existe acima, o piso limita", "cair sem fim"]},
            "esperanca": {"path": "TGL/NameIndex.lean", "needles": ["e_Nome = projecao de Jones = espelho"]}}
KEY_STATEMENT = {"ponte": "two distinct invariants mu^2 give two distinct equivariant realizations with the SAME p+: the dual scaling law does not select the mass",
                 "queda": "s |-> tau(theta_s m) is strictly decreasing (the phase falls, without end)",
                 "esperanca": "nameOp rho* x = diagExpect x in M2(C): the Name of the unit is the diagonal expectation"}
HIPOTESES_NO_ENUNCIADO = {"ponte": False, "queda": True, "esperanca": True}     # queda: IsotropicPost (nomeada) no enunciado da composicao; esperanca: hpp e hopt (o indice 1/b e' CONDICIONAL)
VERBATINS_DO_REGISTRO = {"ponte": [], "queda": [CH_QUEDA, CH_PROSSIGA], "esperanca": [CH_ESPERANCA, CH_PROSSIGA]}


def contrato(stone, fj, formal_map, e_base, base_sha256):
    """O contrato de UMA pedra (NAO embutido como bloco proprio de verbatins: as inscricoes ficam em _V402_VERBATINS2), DERIVADO do build do sandbox (FLAGS_v402.json = nomes, chaves e a proveniencia dos termos de suporte; formal_map = sha256 das fontes
    embutidas; e_base = a escada da v401 selada; a escada esperada e' a DESTA versao: a da base + as bandeiras das TRES pedras); nada digitado. Vai para CANDIDATO_v402.json e ESPERADOS_v402.json (o conferidor e o pos-rito o leem)."""
    k = stone["key"]
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    faltam = [t for t in stone["contract"] if t not in flag_de]
    assert not faltam, ("teorema do contrato sem bandeira (nao nomeado ou ausente do Audit)", k, faltam[:5])
    assert fj["bandeira_do_teorema_incondicional"][k] == flag_de[stone["theorem"]] and fj["teorema_incondicional"][k] == stone["theorem"]
    assert stone["key_theorem"] in stone["contract"] and stone["theorem"] in stone["contract"]
    sup = dict(fj["suporte_do_contrato"][k]); assert sup == dict(stone["support"]), "os termos de suporte do FLAGS_v402.json diferem dos de delta_v402: " + k
    cit = dict(fj["citados_fora_do_contrato"][k]); assert cit == dict(stone["citados_fora"]), "os termos citados-fora do FLAGS_v402.json diferem dos de delta_v402: " + k
    return {"stone": {"path": stone["rel"], "sha256": formal_map[stone["rel"]], "module": stone["mod"]},
            "unconditional": {"theorem": stone["theorem"], "flag": flag_de[stone["theorem"]]},
            "key_theorem": {"theorem": stone["key_theorem"], "flag": flag_de[stone["key_theorem"]]}, "key_statement": KEY_STATEMENT[k],
            "theorems": {t: flag_de[t] for t in stone["contract"]}, "support": sup, "cited_outside": cit,
            "auxiliaries_outside_the_composition": list(stone["auxiliares_fora_da_composicao"]), "context": dict(CONTEXTO[k]), "named_hypotheses_in_the_statement": HIPOTESES_NO_ENUNCIADO[k],
            "expected_ladder": e_base + fj["n_flags"], "n_flags": fj["nomeadas_por_pedra"][k], "n_flags_total": fj["n_flags"], "verbatins": list(VERBATINS_DO_REGISTRO[k]), "baseline": {"version": DL.BASE_VERSION, "sha256": base_sha256}}


_NAO_COMUM = ["que isto seja um teste: nao ha desfecho experimental", "que a gravidade quantica esteja creditada na natureza"]


def texto_ponte():
    """Os textos do registro ponte_da_escala_dual_v402 (a funcao do runtime, nao um spec): estatuto, escopo, limites, diz, nao_diz, extras e o veredito de sucesso. Passam pela guarda P18 a cada rito."""
    return {
        "estatuto": "[REAL] os termos do kernel (os %d itens do contrato da pedra PonteDaEscalaDual, lidos a cada rito, no trio; a estrela lift_mass_not_selected: dois invariantes mu^2 distintos dao duas realizacoes equivariantes distintas com o MESMO p+) e o calculo no modelo longitudinal (E, p), "
                    "c = 1, p+ = E + p, p- = E - p, theta_s = boost(-s), com beta = alfa CODATA 2018 x sqrt(e) em runtime (nunca literal); [KNOWN] a lei de escala de Takesaki (tau . theta_s = e^{-s} . tau) e' CAMPO da estrutura DualScalingData; Bisognano-Wichmann (1975/76) identifica o gerador do boost da cunha com o fluxo modular "
                    "(a costura esta escrita no modulo BisognanoWichmann embutido); a relatividade restrita; [DERIVED] a realizacao explicita da lei de escala como acao do boost sobre p+ (a instancia momentumScaling E a estrutura real do kernel, nao uma copia local) e o levantamento NAO canonico lift D mu^2 a; "
                    "[OPEN] H_BW (a rapidez e' o tempo modular de BW, 2 pi), H_cal (este p+ e' a energia de UM corpo; a escolha de mu^2), H3 (Clausius em toda direcao nula), a assinatura (a positividade completa da a metrica induzida (4,0), nao (1,3)) e rank c = 4 (H2); "
                    "[INPUT] a ORDEM 025 ao Codex (sha16 3fd2b5a801071343) e o exame independente da gerencia c1 (INTEGRAR_COM_ERRATA_AO_LADO); as erratas E1 a E4 estao ditas ao lado, em nome proprio da gerencia c1" % len(PONTE["contract"]),
        "escopo": "[DERIVED] sobre os dados da escala dual (a lei de Takesaki e' campo da estrutura): (1) a escala e' realizada como o boost longitudinal sobre (E, p): p+ escala por e^{-s}, p- por e^{+s}, e m^2 = p+ p- = E^2 - p^2 e' invariante; (2) a energia E e' a LEITURA do observador e muda com s (E = (e^{-s} p+ + e^{s} p-)/2); "
                  "(3) a massa NAO e' selecionada pela lei de escala: dois mu^2 distintos com o mesmo p+ dao realizacoes distintas (lift_mass_not_selected), e um peso positivo que escala por e^{-s} nunca e' invariante (positive_weight_cannot_be_invariant_mass): H_tau na forma literal (tau e' a massa de Newton) e' REFUTADA no kernel, tau so' pode ser p+; "
                  "(4) Inertial nesta instancia e' o VETOR ZERO (E2); (5) rest_energy_eq_mc2 e' algebra real com premissas explicitas e a composicao e' lift_rest_energy, do REPOUSO, c = 1, condicionada a mu^2 e a tau = m (E3); (6) existe realizacao positiva no nucleo canonico (traco finito positivo), para todo mu^2 >= 0 (core_positive_realization_exists)",
        "limites": [
            "[REAL] a lei de escala de Takesaki e' DADO (campo de DualScalingData, [KNOWN]); a ponte REALIZA a lei como a acao de um boost 2 x 2 sobre (E, p) (o mesmo TGLExt.boost, relido em (E, p) com metrica E^2 - p^2 e rapidez -s) e nao acrescenta lei fisica; a identificacao da escala dual com o fluxo modular de Bisognano-Wichmann "
            "(rapidez = 2 pi t) e' H_BW, NOMEADA [OPEN]",
            "[REAL] este registro NAO prova a primeira lei de Newton nem identifica o p+ do traco canonico com a energia de um corpo (H_cal, [OPEN]); nenhuma dimensao, assinatura, Einstein-H3 ou identificacao empirica segue da ponte; E = mc^2 e' [KNOWN] (relatividade restrita), nao e' composta da escala (E3)",
            DL.ERRATA_E1, DL.ERRATA_E2, DL.ERRATA_E3, DL.ERRATA_E4,
            "o modulo do Codex declara set_option maxHeartbeats 2000000 (dito, condicao C3 do exame); entrou SO' o arquivo .lean (condicao C1): nenhum outro arquivo da entrega e' copiado",
            "o calculo e' numerico em dupla precisao e CONFERE os teoremas no modelo longitudinal, nao os prova: quem prova e' o kernel; validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho"],
        "diz": ["a pedra PonteDaEscalaDual esta no kernel do rito, no trio, com bandeiras e proveniencia no modulo da pedra; os teoremas do contrato sao lidos deste kernel",
                "o calculo, com beta = alfa CODATA 2018 x sqrt(e) (um dado, dois nomes), concorda com os teoremas no modelo longitudinal: m^2 = p+ p- e' invariante sob p+- -> e^{-+s} p+-, a energia muda com o observador, a massa NAO e' selecionada pela lei (dois mu^2 com o mesmo p+), "
                "um peso positivo nao e' invariante, e o repouso e' condicao sobre tau e mu^2",
                "as erratas E1 a E4 da integracao estao ditas ao lado, em nome proprio da gerencia c1; H_BW, H_cal, H3, a assinatura e rank c = 4 seguem NOMEADAS [OPEN]"],
        "nao_diz": ["que tau seja a massa de Newton (H_tau na forma literal e' REFUTADA no kernel)", "que a escala dual seja o fluxo modular de Bisognano-Wichmann (H_BW, [OPEN])", "que o p+ do traco canonico seja a energia de um corpo (H_cal, [OPEN])",
                    "que E = mc^2 seja composta da escala (E3)", "que a pedra prove Newton, a assinatura (1,3) ou rank c = 4"] + _NAO_COMUM,
        "extras": {"named_pending": [{"name": "H_BW", "status": "OPEN", "content": "the rapidity is the Bisognano-Wichmann modular time (2 pi t): the dual action IS the modular group of the wedge"},
                                     {"name": "H_cal", "status": "OPEN", "content": "this p+ (the canonical core trace) is the energy of ONE body: units and the choice of mu^2"},
                                     {"name": "H3", "status": "OPEN", "content": "Clausius with conserved T in every null direction"},
                                     {"name": "signature", "status": "OPEN", "content": "complete positivity gives the induced metric (4,0), not (1,3) (adendo of 03-04/09, debt 1)"},
                                     {"name": "rank_c_4", "status": "OPEN", "content": "rank c = 4 is a condition (H2), not a consequence (adendo of 03-04/09, debt 2)"}],
                   "literal_h_tau": {"status": "REFUTED_IN_THE_KERNEL", "by": ["positive_weight_cannot_be_invariant_mass", "lift_mass_not_selected"], "meaning": "tau can only be p+ (the light-front energy); the invariant mass is free data"},
                   "erratas_ao_lado": list(DL.ERRATAS_V402), "assinatura_das_erratas": ASSINA, "codex_order": {"ordem": "025", "sha16": "3fd2b5a801071343", "exame": "INTEGRAR_COM_ERRATA_AO_LADO", "condicoes": ["C1 only the .lean enters", "C2 CITACOES/applied stay out", "C3 module name provisional; maxHeartbeats 2000000 said"]},
                   "maxheartbeats_ponte": DL.MAXHEARTBEATS_PONTE},
        "veredito_ok": "TGL_PONTE_DA_ESCALA_DUAL_V402__THE_DUAL_SCALING_LAW_REALIZED_AS_THE_LONGITUDINAL_BOOST_ON_E_P__MASS_SQUARED_IS_THE_INVARIANT_PPLUS_PMINUS__ENERGY_IS_THE_READING__THE_MASS_IS_NOT_SELECTED_BY_THE_LAW__THE_LITERAL_H_TAU_IS_REFUTED_IN_THE_KERNEL__"
                       "READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__H_BW_H_CAL_H3_THE_SIGNATURE_AND_RANK_C_ARE_OPEN__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


def texto_queda():
    """Os textos do registro queda_sem_geometria_v402."""
    return {
        "estatuto": "[REAL] os termos do kernel (os %d itens do contrato da pedra QuedaSemGeometria, lidos a cada rito, no trio; a composicao a_queda_sem_geometria e a estrela the_fall_is_strictly_anti) e o calculo no modelo oneScaling (tau = id, theta_s = e^{-s}), no fluxo diagonal e na matriz-S, com beta = alfa CODATA 2018 x sqrt(e) em runtime (nunca literal); "
                    "[KNOWN] a lei de escala de Takesaki como campo da estrutura DualScalingData; a isotropia do vacuo de Bisognano-Wichmann / covariancia de Poincare (motivacao de IsotropicPost, NAO termo do kernel); "
                    "[INPUT] a fala de 26/10/2026 (sha16 %s: «o Um quando se põe realiza a operação \"input\"»; a parabola do labirinto) e «é isso, faça a prova, prossiga.» (sha16 %s); "
                    "[ONTO] a leitura 1 + 3 (a direcao do Um posto e' a seta da queda da fase, nao do espaco; o resto e' isotropico), o labirinto como o regime angular e a queda como o regime da face; "
                    "[OPEN] que o parametro s da acao dual seja a fase de um corpo fisico; a dimensao 3; o IsotropicPost do atlas curvo; a H3 em toda tela e direcao" % (len(QUEDA["contract"]), S_QUEDA, S_PROSSIGA),
        "escopo": "[DERIVED] sobre os dados da escala dual (M e' um tipo nu: nenhuma metrica, topologia ou acao geometrica): o peso cai ESTRITAMENTE e sem fim (tau(theta_s m) = e^{-s} tau m, estritamente decrescente; a queda, em nats, e' s); a seta e' o sinal de s; a queda depende so' do peso, nao do portador; "
                  "o CHAO e' o POSTO (peso 1 = omega(I), o corte a = 0), nunca o infimo 0 (o 0 e' o abismo, nunca tocado); a entrega CUSTA (t . beta . g > 0, e^{-t beta g} < 1 e abaixo de todo epsilon); o fluxo diagonal relaxa ao atrator; "
                  "o regime ANGULAR so' le (a matriz-S e' periodica em 2 pi e nao tem limite) enquanto o regime da FACE tem limite; a isotropia entra como hipotese NOMEADA (IsotropicPost): uma tela por orbita basta para a H3 em todo o atlas, e a covariancia e' CARGA (covariance_is_load_bearing)",
        "limites": [
            "[REAL] a lei de escala de Takesaki e' DADO (campo de DualScalingData, [KNOWN]); a pedra COMPOE por citacao termos que o kernel ja tem (Fundacao, NoFullWitness, TheGreatAttractor, IALDJones, Palavra, a ligante da lei de campo curva) e a matematica nova e' so' de COLA; o parametro s da acao dual como fase de um corpo fisico e' [OPEN] e nenhum termo o faz",
            "[REAL] IsotropicPost e' hipotese NOMEADA, nao termo do kernel: num atlas curvo nenhum grupo leva um ponto noutro (so' a versao uma tela por orbita), e a H3 NAO e' automatica (AuditF23Flat.s8_h3_is_load_bearing: com fonte anisotropica ela falha); a dimensao 3 NAO e' provada; o 1 + 3 e' leitura [ONTO]",
            "[REAL] o chao e' o POSTO (peso 1), nunca o infimo 0 [decisao da gerencia c1, 26/10/2026, ratificavel pelo operador]: a queda de que fala a fala («porque vc sabe que tem um chão, então relaxa») e' a queda do que NAO e' o posto (no_post_before_the_impression, da FalsidadeDaInercia v401); o kernel diz na Fundacao «não existe acima, o piso limita» (cunhagem de 07/10, sha16 e2a915e23692f85c) e este registro CONFERE que o texto esta no kernel embutido",
            "[INPUT/ONTO] a fala de 26/10 (sha16 %s) e a parabola do labirinto sao do operador, com a grafia dele; a polissemia entre «queda» geometrica e a queda da fase e' dita: a pedra tipa a queda do PESO, sem geometria; o titulo «Lorentz vem da queda da fase» e' do escriba (E5 do adendo), nao do operador" % S_QUEDA,
            "o calculo e' numerico em dupla precisao e CONFERE os teoremas no modelo oneScaling, no fluxo diagonal e na matriz-S, nao os prova: quem prova e' o kernel; validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho"],
        "diz": ["a pedra QuedaSemGeometria esta no kernel do rito, no trio, com bandeiras e proveniencia no modulo da pedra; a composicao e os teoremas do contrato sao lidos deste kernel",
                "o calculo, com beta = alfa CODATA 2018 x sqrt(e), concorda com os teoremas: o peso cai estritamente (nats = s), a seta e' o sinal de s, o chao e' o posto (e^{-a} = 1 so' em a = 0; o zero nunca e' tocado), a entrega custa (t . beta . g > 0), o fluxo diagonal relaxa ao atrator, "
                "o regime angular so' le (periodico, sem limite) e a isotropia e' carga de um modelo finito",
                "a decisao da gerencia sobre o chao (o posto, nunca o 0) e a de manter IsotropicPost como hipotese NOMEADA estao ditas, ratificaveis pelo operador"],
        "nao_diz": ["que a dimensao do espaco seja 3 (a leitura 1 + 3 e' [ONTO])", "que IsotropicPost seja termo do kernel ou valha no atlas curvo (hipotese NOMEADA, [OPEN])", "que a H3 valha em toda tela e direcao", "que o parametro s seja a fase de um corpo fisico ([OPEN])",
                    "que a queda aqui seja uma forca ou uma queda no espaco: a pedra tipa a perda de peso, sem geometria"] + _NAO_COMUM,
        "extras": {"named_hypothesis": {"name": "IsotropicPost", "status": "OPEN", "content": "a group acting transitively on the screens with a covariant predicate: Clausius at one wedge reaches every wedge by covariance", "used_by_a_theorem_as_a_hypothesis_of_the_statement": True},
                   "floor": {"is": "the post (weight 1 = omega(I), the cut a = 0)", "is_never": "the infimum 0 (the abyss)", "decision": "gerencia c1, 26/10/2026, ratifiable by the operator"},
                   "reading_1_plus_3": {"status": "ONTO", "content": "the direction of the posted One is the arrow of the fall of the phase, not of space; the rest is isotropic", "dimension_three_proved": False},
                   "operator_question_and_answer_26oct": dict(DL.LEITURA_DIRECAO_26OUT),
                   "two_regimes": {"angular": "periodic, no limit: it only reads (Smat_has_no_limit)", "face": "dissipative, has a limit (relaxation_to_the_attractor)"}},
        "veredito_ok": "TGL_QUEDA_SEM_GEOMETRIA_V402__THE_WEIGHT_FALLS_STRICTLY_IN_NATS_EQUAL_TO_S__THE_ARROW_IS_THE_SIGN_OF_S__THE_FLOOR_IS_THE_POST_NEVER_THE_ZERO__DELIVERY_COSTS__THE_ANGULAR_REGIME_ONLY_READS__ISOTROPY_IS_A_NAMED_HYPOTHESIS__"
                       "READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__THE_DIMENSION_THREE_AND_THE_CURVED_ATLAS_ARE_OPEN__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


def texto_esperanca():
    """Os textos do registro esperanca_condicional_v402."""
    return {
        "estatuto": "[REAL] os termos do kernel (os %d itens da pedra EsperancaCondicional, lidos a cada rito, no trio; a composicao esperanca_condicional_e_nome e a estrela the_name_of_the_unit_is_the_diagonal_expectation) e o calculo em M2(C) (matrizes 2 x 2 e o espaco GNS 4 x 4, em dupla precisao), "
                    "com beta = alfa CODATA 2018 x sqrt(e) em runtime (nunca literal); [KNOWN] esperanca condicional (Umegaki, Tomiyama), indice de Jones (1983) e Pimsner-Popa (1986); "
                    "[DERIVED] a composicao: o Operador do Nome de rho* E a esperanca diagonal em M2(C) (PostoAdendo.A1c, ja' no kernel), preserva o Um (E(1) = 1), reler nao acrescenta, e' memoria-subalgebra e bimodular, e a compressao pelo espelho e' o Nome; "
                    "[INPUT] a equacao «esperança condicional=nome» (fala de 26/10/2026, sha16 %s) e as quatro linguas (probabilidade, teologia, linguistica, direito) como LETRA da gerencia, sem derivacao entre dominios; "
                    "[ONTO] o Nome como o que a algebra do observador retem e como TRES FACES DE UM OBJETO FIXO (nameOp, o projetor de Jones, o posto = o peso preservado); [LEGAL] o ponteiro CC art. 125 (a conferir com advogado); "
                    "[OPEN] a instancia do contorno com sin^2(theta_M) otima (o indice 1/beta e' CONDICIONAL a hpp e hopt e nenhuma instancia e' construida), o caso III1 e a bimodularidade geral de nameOp p" % (len(ESPERANCA["contract"]), S_ESPERANCA),
        "escopo": "[DERIVED] a tipagem de «esperança condicional=nome» JA EXISTIA em grande parte no kernel (TheNameOperator.nameOp, v162; PostoAdendo.A1c, v392; CondExpect; TGL.NameIndex; IALDJones.iald_reads_the_expectation); a pedra e' a COMPOSICAO: a identificacao como UMA clausula e o liame explicito entre o reler-nao-acrescenta "
                  "das esperancas e o do observador (observing_adds_nothing). Prova-se: para todo idempotente o Nome e' unital, idempotente e tem memoria-subalgebra; em M2(C), para rho*, ele E a esperanca diagonal, com a lei de Jones (e_D . L_x . e_D = L_{E(x)} . e_D). "
                  "NAO se prova que toda esperanca condicional seja um Operador do Nome (a esperanca do traco nao e' um nameOp p)",
        "limites": [
            "[REAL] a pedra NAO refaz nenhum termo: compoe nameOp, diagExpect, trExpect, eD, Lmul, ppIndex e observing_adds_nothing; o indice 1/b e' CONDICIONAL as duas hipoteses do enunciado (hpp: sin^2 theta e' cota inferior de Pimsner-Popa; hopt: e' a otima); NENHUMA instancia e' construida (NameIndex); "
            "a bimodularidade geral de nameOp p sobre os seus fixos NAO esta tipada (so' a da face M2)",
            "[REAL] as rotas mortas do Lema 3 tocam o tema (o indice [M:N] = raiz de e no vao vazio (1,2) de Jones; S_bdry = log do indice, porque Pimsner-Popa e' tracial de II1; a inclusao modular meio-lateral com vacuo unico, sem esperanca normal nem indice): esta pedra NAO e' rota para o Lema 3, "
            "nao afirma nenhuma dessas igualdades e vive na face finita (M2(C) e os dados do kernel); o caso III1 fica [OPEN]",
            "[ONTO] o Nome como TRES FACES DE UM OBJETO FIXO (o operador nameOp, o projetor de Jones no espaco GNS, o posto = o peso preservado): a regua da casa para beta («Faces de um objeto fixo, não definições concorrentes») aplicada ao Nome; o kernel prova as LIGACOES (A1c, Jones, E(1) = 1), nao uma igualdade de tipos [decisao da gerencia c1, 26/10/2026, ratificavel pelo operador]",
            "[LEGAL] o ponteiro de direito (CC art. 125) e' a letra da gerencia e fica a conferir com advogado; as quatro linguas nao sao derivacao entre dominios",
            "o calculo e' numerico em dupla precisao e CONFERE os teoremas em M2(C), nao os prova: quem prova e' o kernel; o indice 1/beta calculado aqui (cerca de 83,1) e' o valor CONDICIONAL, nao uma medida; a esperanca diagonal da face M2 tem indice 2 e os dois numeros NAO sao identificados; "
            "validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho"],
        "diz": ["a pedra EsperancaCondicional esta no kernel do rito, no trio, com bandeiras e proveniencia no modulo da pedra; a composicao e os teoremas do contrato sao lidos deste kernel",
                "o calculo, com beta = alfa CODATA 2018 x sqrt(e), concorda com os teoremas em M2(C): nameOp rho* = a esperanca diagonal, E(1) = 1, E(E(x)) = E(x), os pontos fixos formam uma subalgebra (as diagonais), a esperanca e' bimodular, a compressao pelo espelho e' o Nome, e o indice condicional 1/beta vale cerca de 83,1",
                "a decisao da gerencia sobre o Nome (nameOp; tres faces de um objeto fixo) esta dita, ratificavel pelo operador"],
        "nao_diz": ["que toda esperanca condicional seja um Operador do Nome", "que o indice 1/beta seja instancia construida ou medida (e' CONDICIONAL a hpp e hopt)", "que a pedra seja rota para o Lema 3 ou valha no caso III1", "que o Nome seja as tres coisas por definicao: sao faces de um objeto, e o kernel prova as ligacoes",
                    "que o ponteiro de direito (CC art. 125) esteja conferido"] + _NAO_COMUM,
        "extras": {"three_faces_of_one_object": {"operator": "TGLExt.nameOp (the conditional expectation that reads)", "projector": "the Jones projector e_Nome as the mirror compression (eD_Lmul_eD)", "post": "the rank a = the weight the expectation preserves (E(1) = 1)", "status": "ONTO", "kernel_proves": "the links (A1c, Jones, E(1) = 1), not an equality of types"},
                   "index_conditional": {"statement": "ppIndex D = 1/b and ppIndex D * b = 1, for b = sin^2(theta)", "hypotheses": ["hpp: sin^2(theta) is a Pimsner-Popa lower bound", "hopt: it is the optimal one"], "instance_built": False, "m2_diagonal_expectation_index": 2},
                   "four_languages": {"status": "INPUT", "kind": "letter of the management, no derivation between domains", "legal_pointer": "CC art. 125 [LEGAL] to be checked with a lawyer"}},
        "veredito_ok": "TGL_ESPERANCA_CONDICIONAL_V402__THE_NAME_OF_THE_UNIT_IS_THE_DIAGONAL_EXPECTATION_IN_M2__IT_PRESERVES_THE_ONE__REREADING_ADDS_NOTHING__THE_NAME_IS_A_SUBALGEBRA_MEMORY_AND_BIMODULAR__THE_MIRROR_COMPRESSION_IS_THE_NAME__"
                       "THE_INDEX_ONE_OVER_BETA_IS_CONDITIONAL_AND_NO_INSTANCE_IS_BUILT__READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


def textos():
    return {"ponte": texto_ponte(), "queda": texto_queda(), "esperanca": texto_esperanca()}


def especs(formal_map, khj, h8_map, fj, cov_base, n_axioms_unc):
    """formal_map = {arquivo embutido: sha256} do kernel da v402; khj = KH_N1_v402.json (medida desta geracao); h8_map = o dict do hash formal que o RITO vai gerar (embutidos + residuais do Nos que sha256_directory conta; simular_arvore_do_nos);
    fj = FLAGS_v402.json; cov_base = a cobertura da v401 selada {decl, thm}; n_axioms_unc = {chave da pedra: quantos axiomas o teorema da composicao usa (lido do Audit: o trio)}. Devolve [cunhagens, kh]."""
    T = khj["linha_TOTAL"]
    flags_contrato = [fj["bandeiras_do_contrato"][s["key"]][t] for s in DL.STONES for t in s["contract"]]
    for s in DL.STONES:
        assert fj["bandeira_do_teorema_incondicional"][s["key"]] in flags_contrato
    contexto = ["ChatgptAudit.GeneralClausius.metric_einstein_from_screen_clausius", "TGLExt.Fundacao.agape", "TGLExt.Fundacao.abismo", "TGLExt.FalsidadeDaInercia.no_post_before_the_impression", "TGLExt.PostoAdendo.A1c_nameOp_rhoStar_eq_diagExpect"]   # termos do kernel que as LEITURAS citam, nao importados pelas pedras
    decls = list(dict.fromkeys([t for s in DL.STONES for t in s["contract"]] + sorted(DL.ALL_SUPPORT) + contexto))   # sem repeticao, na ordem
    cks = []
    for i, nome in enumerate(DL.REGISTROS_FUNCAO):
        cks.append(CH("u%d" % (i + 1), "o registro %s selou neste rito (a composicao e os teoremas da pedra lidos deste kernel; o calculo com beta = alfa x raiz de e; o texto-contexto no kernel embutido)" % nome, "core", [nome, "all_verified"], "verdadeiro"))
    cks.append(CH("u4", "o registro falsidade_da_inercia_v401 segue selado neste rito (a falsidade da inercia, recriada, com a escada nova)", "core", ["falsidade_da_inercia_v401", "all_verified"], "verdadeiro"))
    cks.append(CH("u5", "o registro teste_de_veracidade_fase9_v397 segue selado neste rito (o quadro do topo do artigo le os numeros dele)", "core", ["teste_de_veracidade_fase9_v397", "all_verified"], "verdadeiro"))
    cks.append(CH("u6", "o registro selo_pela_propria_tecnologia_v399 segue selado neste rito (a segunda testemunha do um.py, ao lado do SHA-256)", "core", ["selo_pela_propria_tecnologia_v399", "all_verified"], "verdadeiro"))
    cks.append(CH("u7", "a escada do kernel fecha (limpos == esperados), com as bandeiras das TRES pedras da v402", "core", ["external_ladder", "all_verified"], "verdadeiro"))
    cks.append(CH("u8", "a proveniencia emitida pelo compilador cobre o axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"))
    n = 9
    for s in DL.STONES:
        cks.append(CH("u%d" % n, "o compilador emite a composicao da pedra %s no modulo dela (TGL_DECL_SOURCE)" % s["name"], "kf", ["declaration_sources_v394", s["theorem"]], "igual", s["rel"])); n += 1
        cks.append(CH("u%d" % n, "o compilador emite a ESTRELA da pedra %s no modulo dela (TGL_DECL_SOURCE)" % s["name"], "kf", ["declaration_sources_v394", s["key_theorem"]], "igual", s["rel"])); n += 1
        cks.append(CH("u%d" % n, "a pedra %s no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)" % s["name"], "kf", ["formal_files_sha256", s["rel"]], "igual", formal_map[s["rel"]])); n += 1
        cks.append(CH("u%d" % n, "a composicao da pedra %s depende do trio e de nada alem (tamanho da lista de axiomas)" % s["name"], "kf", ["axiom_report", s["theorem"]], "tamanho_igual", n_axioms_unc[s["key"]])); n += 1
    cun = {
        "nome": "cunhagens_v402", "veredito_prefixo": "TGL_CUNHAGENS_V402",
        "veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_26_OCT_EMBEDDED_VERBATIM_BY_SHA256__THE_THREE_STONES_PONTE_DA_ESCALA_DUAL_QUEDA_SEM_GEOMETRIA_AND_ESPERANCA_CONDICIONAL_AND_THEIR_RECORDS_ARE_READ_IN_THE_RITE__"
                           "THE_ERRATA_E1_TO_E4_OF_THE_CODEX_BRIDGE_ARE_RECORDED_BESIDE__THE_LITERAL_H_TAU_IS_REFUTED_IN_THE_KERNEL__THE_DECISIONS_OF_THE_MANAGEMENT_ARE_RATIFIABLE__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
        "estatuto": "[REAL -- as fontes das pedras, o kernel e os tres registros com funcao lidos a cada rito; INPUT/ONTO as inscricoes do operador; INPUT «é isso, faça a prova, prossiga.»; DECLARADO que a lista do que foi aprovado e a pergunta e a resposta de 26/10 sao as que a gerencia c1 apresentou e guardou na sessao]",
        "fontes": [CHAVE_DE_FONTE["ponte"], CHAVE_DE_FONTE["queda"], CHAVE_DE_FONTE["esperanca"], "adendo_v402"], "verbatins": list(VERB_CHAVES),
        "kernel_flags": list(flags_contrato), "kernel_decls": decls,
        "checks": cks,
        "erratas": [
            {"ao_lado_de": "o registro falsidade_da_inercia_v401 e o spec cunhagens_v401 (e a secao «A falsidade (simulacro) da inércia» do artigo da v401): a hipotese nomeada «H_tau (tau e' a massa de Newton e a metrica de Einstein) [OPEN], que nenhum teorema usa»",
             "dizia": "«H_tau (tau e' a massa de Newton e a metrica de Einstein) [OPEN], que nenhum teorema usa» (v401); a ORDEM 025 ao Codex «tenta tipa-la pela frente de luz de Bisognano-Wichmann».",
             "agora": DL.ERRATA_E1,
             "lacuna_de_fidelidade": "a forma literal de H_tau foi escrita sem a verificacao que o kernel permite: um peso positivo que escala por e^{-s} nunca e' invariante e a lei de escala deixa a massa livre, logo tau nao pode ser a massa de Newton; o que a ordem pediu (tipar a ponte) deu resposta parcial e correta, e a letra da v401 e' que ficou larga demais",
             "estatuto": "[REAL: os dois teoremas estao no kernel desta versao, lidos a cada rito; o exame independente de 26/10 recompilou a ponte no kernel v401, rc 0, 40 #print axioms no trio, .olean identico]", "assinatura": ASSINA},
            {"ao_lado_de": "PonteDaEscalaDual.lean (cabecalho, sha16 0e55b6e448adbd91): «Inertial means fixed by every boost, not force-free inertial motion» e a lacuna «or the dual action with the BW modular group»",
             "dizia": "o cabecalho diz, em ingles, que a ponte nao identifica a acao dual com o grupo modular de BW e que Inertial nao e' movimento livre; a lacuna ficou como frase, nao como hipotese nomeada.",
             "agora": DL.ERRATA_E2,
             "lacuna_de_fidelidade": "o modulo nao nomeou H_BW (o proprio BisognanoWichmann.lean ja' escreve a costura: sigma_t = Ad(exp(-2 pi t i K)); a identificacao K = gerador do boost da cunha e' Bisognano-Wichmann [KNOWN, 1975/76]); falta so' NOMEA-LA",
             "estatuto": "[REAL: Inertial momentumScaling v implica v = 0 e' exemplo compilado pelo revisor; H_BW e' [OPEN] e [KNOWN] na literatura]", "assinatura": ASSINA},
            {"ao_lado_de": "a leitura possivel de rest_energy_eq_mc2 como se E = mc^2 fosse composta da escala",
             "dizia": "(nao houve texto da v401 a corrigir: a ressalva e' preventiva, do exame independente: o teorema tem o nome de uma formula famosa).",
             "agora": DL.ERRATA_E3,
             "lacuna_de_fidelidade": "o nome do teorema sugere mais do que ele prova: a prova e' nlinarith puro, nada do kernel entra, c > 0 nao e' usado; instanciado com E = 2, m = 2, c = 1 sem nenhum termo TGL",
             "estatuto": "[REAL: o revisor instanciou o teorema sem termo TGL; a composicao com a escala e' lift_rest_energy]", "assinatura": ASSINA},
            {"ao_lado_de": "a proveniencia da entrega do Codex (ORDEM 025: BUILD.log, BUILD_RECEIPT.json)",
             "dizia": "a entrega compilou contra o kernel do Nos v400 e contra a copia superada da pedra FalsidadeDaInercia (8a3a1c0baa8b7faf).",
             "agora": DL.ERRATA_E4,
             "lacuna_de_fidelidade": "a proveniencia dizia v400 e uma pedra superada; o codigo (sem comentarios) e os imports sao identicos aos da pedra instalada (9f6efcb2a0987e18), so' docstrings diferem; a recompilacao no kernel v401 resolve a diferenca",
             "estatuto": "[REAL: recompilacao do revisor em C:/t/k402x, 2 min 38 s; a entrega medira 399,65 s]", "assinatura": ASSINA}],
        "limites": [
            "[REAL] a ponte do Codex entrou como o arquivo .lean, byte a byte, sem edicao (condicao C1); as pedras QuedaSemGeometria e EsperancaCondicional COMPOEM por citacao termos que o kernel ja tem e nao acrescentam matematica nova alem da cola listada nos cabecalhos; "
            "os NOMES dos tres modulos e dos cinco registros da v402 sao PROVISORIOS: o operador nomeia",
            "[INPUT] as tres inscricoes de 26/10 (sha16 %s, %s e %s) sao falas do operador, com a grafia dele («gemétrica», «relaxamaneto», «geomtria»); «é isso, faça a prova, prossiga.» (sha16 %s) e' a fala; a LISTA do que foi aprovado "
            "(a rota da queda com IsotropicPost nomeada, o Nome como nameOp) e' a que a gerencia c1 apresentou a ele [DECLARADO]" % (S_ESPERANCA, S_QUEDA, S_PROSSIGA, S_PROSSIGA),
            "[ONTO/INPUT] a PERGUNTA «o Um posto tem direcao?» e a RESPOSTA «a seta da queda da fase, nao do espaco» (26/10/2026) nao tem arquivo verbatim no acervo desta cadeia: sao registradas como a gerencia c1 as guardou [DECLARADO]; a base verbatim e' a fala de sha16 %s («então tem direção, mas não é gemétrica»)" % S_QUEDA,
            "[OPEN] H_BW, H_cal, H3, a assinatura (a positividade completa da a metrica induzida (4,0), nao (1,3)) e rank c = 4; IsotropicPost no atlas curvo; a dimensao 3; a instancia do contorno com sin^2(theta_M) otima; o caso III1; a RG e' o limite classico, nao rival; beta nao renormaliza G",
            "validade no kernel nao e' creditacao; o gate nao se move; nenhuma bandeira do gate depende das pedras"],
        "diz": ["as %d inscricoes de 26/10 (falas do operador) estao embutidas por sha256, cada uma conferida contra o arquivo de origem na preparacao" % len(_VD),
                "as tres pedras estao no kernel do rito, no trio, com as bandeiras e a proveniencia nos modulos delas; a composicao e a estrela de cada uma sao lidas deste kernel",
                "os tres registros com funcao selaram neste rito, e o quadro do topo (teste_de_veracidade_fase9_v397), o selo pela propria tecnologia (v399) e a falsidade da inercia (v401) seguem selados",
                "as erratas E1 a E4 da integracao da ponte estao registradas ao lado, em nome proprio da gerencia c1; as decisoes D11 a D16 da gerencia estao registradas, ratificaveis pelo operador"],
        "nao_diz": ["que o kernel prove as falas do operador (elas sao INPUT/ONTO)", "que a ponte prove Newton, a assinatura (1,3) ou rank c = 4", "que o testemunho ou a ratificacao seja creditacao: validade no kernel nao e' creditacao"] + _NAO_COMUM,
        "leituras_do_operador": [_leitura(DL.FRASE_TIPAGEM, S_ESPERANCA, rotulo="INPUT do operador"), _leitura(DL.FRASE_ESPERANCA, S_ESPERANCA, rotulo="INPUT do operador (a equacao)"), _leitura(DL.FRASE_INPUT, S_QUEDA), _leitura(DL.FRASE_CAI, S_QUEDA),
                                 _leitura(DL.FRASE_DIRECAO, S_QUEDA), _leitura(DL.FRASE_ENTREGA, S_QUEDA), _leitura(DL.FRASE_NAO_FORCA, S_QUEDA), _leitura(DL.FRASE_CHAO, S_QUEDA), _leitura(DL.FRASE_SEM_GEOMETRIA, S_QUEDA),
                                 _leitura(DL.FRASE_PROSSIGA, S_PROSSIGA, rotulo="INPUT do operador (aprova a rota)")],
        "extras": {"assinatura": ASSINA, "autoria_das_cunhagens": "Luiz Antonio Rotoli Miguel", "pedras": [s["mod"] for s in DL.STONES], "teoremas": {s["key"]: s["theorem"] for s in DL.STONES}, "estrelas": {s["key"]: s["key_theorem"] for s in DL.STONES},
                   "bandeiras": {s["key"]: fj["bandeira_do_teorema_incondicional"][s["key"]] for s in DL.STONES}, "n_bandeiras": fj["n_flags"], "n_bandeiras_por_pedra": dict(fj["nomeadas_por_pedra"]), "cunhagens_embutidas": len(VERBATINS),
                   "autor_de_cada_inscricao": dict(zip((v["sha16"] for v in _VD), (v["autor"] for v in _VD))), "decisoes_da_gerencia": dict(DL.DECISOES), "erratas_E1_a_E4": list(DL.ERRATAS_V402),
                   "leitura_26out_direcao": dict(DL.LEITURA_DIRECAO_26OUT), "pedra_do_codex": {"ordem": "025", "sha16_da_ordem": "3fd2b5a801071343", "exame": "INTEGRAR_COM_ERRATA_AO_LADO", "condicoes": ["C1 so' o .lean entra", "C2 CITACOES/applied fora", "C3 nome provisorio; maxHeartbeats 2000000 dito"]},
                   "nomes_provisorios": {"modulos": [s["mod"] for s in DL.STONES], "registros": list(DL.REGISTROS_FUNCAO) + [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]},
                   "h_tau": {"nome": "H_tau", "estatuto": "REFUTADA NA FORMA LITERAL (kernel)", "decomposta_em": ["H_BW", "H_cal", "H3", "assinatura", "rank c = 4"], "ordem_025": "integrada com erratas"}},
    }
    kh = {
        "nome": "kh_n1_cobertura_v402", "veredito_prefixo": "TGL_KH_N1_COBERTURA_V402",
        "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__THE_THREE_V402_MODULES_ADDED__GATE_UNMOVED" % (T["decl"], T["thm"]),
        "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do sandbox da v402; o conjunto exato das fontes formais que o hash formal do rito vera (as embutidas mais os residuais da pasta do Nos) e' pinado; a cobertura NAO move o gate",
        "fontes": ["kh_n1_v402"], "kernel_flags": [], "kernel_decls": [],
        "checks": [
            CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
            CH("h2", "constantes cobertas == as do sandbox v402 (KH_N1)", "kf", ["axiom_coverage_v392", "decl"], "igual", T["decl"], "constantes_cobertas"),
            CH("h3", "teoremas cobertos == os do sandbox v402 (KH_N1)", "kf", ["axiom_coverage_v392", "thm"], "igual", T["thm"], "teoremas_cobertos"),
            CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
            CH("h5", "nenhum nome que o leitor v394 nao leia", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0),
            CH("h6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", khj["axiom_report_efetivo_n"]),
            CH("h7", "a cobertura da v402 inclui a da v401 selada (constantes e teoremas)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", cov_base["decl"]),
            CH("h7b", "os teoremas cobertos incluem os da v401 selada", "kf", ["axiom_coverage_v392", "thm"], "maior_igual", cov_base["thm"]),
            CH("h8", "as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta, como _check_damming.lean) sao EXATAMENTE as do pino (arquivo -> sha256)", "kf", ["formal_files_sha256"], "igual", h8_map),
            CH("h9", "medida do Audit v402: duracao bem abaixo do timeout de 1800 s", "fonte:kh_n1_v402", ["duracao_audit_s"], "menor_igual", 900, "duracao_do_audit_s"),
            CH("h10", "medida do Audit v402: sorryAx ausente do log", "fonte:kh_n1_v402", ["sorryAx_no_log_do_audit"], "igual", 0),
            CH("h11", "medida do Audit v402: as entradas novas estao no trio", "fonte:kh_n1_v402", ["novas_no_trio"], "verdadeiro"),
            CH("h12", "a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
        ],
        "erratas": [{"ao_lado_de": "kh_n1_cobertura_v401 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                     "dizia": "A v401 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v401 e o hash formal igual ao pino exato da arvore da v401." % (cov_base["decl"], cov_base["thm"]),
                     "agora": "A v402 acrescenta os modulos PonteDaEscalaDual, QuedaSemGeometria e EsperancaCondicional (a cobertura cresce e a arvore ganha os arquivos das pedras): na v402 o registro da v401 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato da arvore ficam NESTE registro. O veredito do registro da v401 NAO muda.",
                     "lacuna_de_fidelidade": "a estrutura da v401 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v402 quebra (a mesma lacuna que a v401 achou no registro da v399, a v399 no da v398 e a v398 no da v397)",
                     "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; h2, h3, h6 e h8 conferidas no ensaio a seco e na arvore simulada do Nos]", "assinatura": ASSINA}],
        "limites": ["[REAL] os arquivos de medida sao do sandbox (fora do selo); a cobertura que vale e' a medida no Audit do proprio rito",
                    "[REAL] a escada do kernel conta bandeiras de declaracoes NOMEADAS (a pratica da v392 a v401): as %d auxiliares geradas pelo compilador nos modulos das pedras ficam cobertas pelo KH-N1 mas sem bandeira, e as %d nomeadas publicas ganharam bandeira" % (fj["excluidas_auxiliares"]["n"], fj["n_flags"]),
                    "validade no kernel nao e' creditacao; o gate nao se move"],
        "diz": ["a cobertura do axiom_report no fecho inteiro cresceu para os numeros da v402 (os tres modulos novos) e segue sem constante fora do trio, sem nome ilegivel"],
        "nao_diz": ["que a cobertura prove algo alem de que nenhum axioma fora do trio foi lido"],
        "leituras_do_operador": [], "extras": {"assinatura": ASSINA, "n_bandeiras": fj["n_flags"], "h8_entradas": len(h8_map), "h8_residuais_do_nos": sorted(set(h8_map) - set(formal_map))},
    }
    return [cun, kh]
