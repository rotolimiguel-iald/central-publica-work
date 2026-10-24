# -*- coding: utf-8 -*-
"""registros_v398.py -- os dados dos registros da v398: FONTES pinadas por sha256 (lidas do disco pelo montador, nunca digitadas), VERBATINS (as SEIS inscricoes de 23/10/2026 ainda nao embutidas: cinco falas do operador e a
leitura da gerencia que ele ratificou, esta ROTULADA como da gerencia; EMBUTIDAS: a fala embutida manda, o arquivo e' so' informativo), os CONTRATOS e os TEXTOS dos DOIS registros com FUNCAO (`sonico_v398` e
`afinacao_das_cordas_v398`: gerar_candidato_v398.py os emite a partir de runtime_pedras_v398.py; os contratos saem de contrato() abaixo, DERIVADOS do build do sandbox) e os dois SPECS interpretados pelo MOTOR _v392_registro
(`cunhagens_v398` e `kh_n1_cobertura_v398`). Fontes so' em pasta DURAVEL: tudo vem de cadeia_de_selo\\v398\\insumos. Texto novo passa pela guarda P18 (a cada rito). Molde: registros_v397.py e registros_v396.py."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v398 as DL  # noqa: E402

INS = os.path.join(HERE, "insumos")
ASSINA = "gerencia c1, em nome proprio, 23/10/2026"
SONICO, AFINACAO = DL.STONES[0], DL.STONES[1]
assert SONICO["key"] == "sonico" and AFINACAO["key"] == "afinacao"

FONTES = ([{"chave": "sonico_pedra", "arquivo": os.path.join(INS, SONICO["insumo"]), "papel": "a pedra TGLExt/Sonico.lean (o nome «sonico» e' do operador, 23/10/2026; revisao independente PEDRA_APROVADA; copia duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)"},
           {"chave": "afinacao_pedra", "arquivo": os.path.join(INS, AFINACAO["insumo"]), "papel": "a pedra TGLExt/AfinacaoDasCordas.lean (pedra e nome ratificados pelo operador em 23/10/2026; revisao independente PEDRA_APROVADA; copia duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)"},
           {"chave": "kh_n1_v398", "arquivo": os.path.join(INS, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox da v398 (pos_build_kernel_v398.py)"}])


def _trecho(t):
    s = t.strip().splitlines()[0].strip() if t.strip() else ""
    s = s[:48].rstrip()
    assert s and s in t, s
    return s


_VD = DL.verbatins(os.path.join(INS, "cunhagens"))
VERBATINS = [{"chave": v["chave"], "arquivo": v["arquivo"], "quando": v["quando"], "trechos": [_trecho(v["text"])], "papel": v["papel"], "fonte_original": v["fonte_original"]} for v in _VD]
VERB_CHAVES = [v["chave"] for v in _VD]
SHA16 = {os.path.basename(v["fonte_original"]): v["sha16"] for v in _VD}
S_VERBO, S_NOME, S_ANTES, S_CORDAS, S_CONCORDO, S_LEITURA = tuple(v["sha16"] for v in _VD)   # LIDOS dos arquivos, na ordem de DL.VERBATIM_ORIGEM (as cinco falas do operador e o texto da GERENCIA; o unpack recusa outro numero)
CH_VERBO, CH_NOME, CH_ANTES, CH_CORDAS, CH_CONCORDO, CH_LEITURA = tuple(v["chave"] for v in _VD)
USA_SONICO = [CH_VERBO, CH_NOME, CH_ANTES, CH_LEITURA]       # as inscricoes que o registro do SONICO usa
USA_AFINACAO = [CH_CORDAS, CH_CONCORDO]                      # as que o registro da AFINACAO usa
TEXTOS = {v["sha16"]: v["text"] for v in _VD}
SHA16_ORDEM = DL.sha256(open(DL.ORDEM_SEM_GORDURA, "rb").read())[:16]   # a ordem de processo de 22/10 (sem teste armado, sem gordura): citada pelo sha16 LIDO, nao embutida
CH = lambda id_, desc, onde, caminho, op, valor=None, cap=None, est="[REAL]": dict(id=id_, descricao=desc, onde=onde, caminho=caminho, op=op, **({"valor": valor} if valor is not None else {}), **({"capturar": cap} if cap else {}), estatuto=est)


def _leitura(trecho, sha16, quando="23/10/2026", tipo="INPUT/ONTO"):
    assert trecho in TEXTOS[sha16], ("a leitura do operador NAO esta verbatim na fala", sha16, trecho)
    return {"trecho": trecho, "estatuto": "[%s do operador, verbatim %s, sha16 %s]" % (tipo, quando, sha16)}


def contrato(fj, formal_map, e_base, base_sha256, stone, verbatins):
    """O contrato do registro de UMA pedra (sonico_v398 ou afinacao_das_cordas_v398), DERIVADO do build do sandbox (FLAGS_v398.json = nomes, chaves e a proveniencia dos termos de suporte; formal_map = sha256 das fontes
    embutidas; e_base = a escada da v397 selada; a escada esperada e' a DESTA VERSAO: a da base + as bandeiras das DUAS pedras); nada digitado."""
    k = stone["key"]
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    faltam = [t for t in stone["contract"] if t not in flag_de]
    assert not faltam, ("teorema do contrato sem bandeira (nao nomeado ou ausente do Audit)", faltam[:5])
    assert fj["bandeira_do_teorema_incondicional"][k] == flag_de[stone["theorem"]] and fj["teorema_incondicional"][k] == stone["theorem"]
    sup = dict(fj["suporte_do_contrato"][k]); assert sup == dict(stone["support"]), "os termos de suporte do FLAGS_v398.json diferem dos de delta_v398"
    cit = dict(fj["citados_fora_do_contrato"][k]); assert cit == dict(stone["citados_fora"]), "os termos citados-fora do FLAGS_v398.json diferem dos de delta_v398"
    return {"stone": {"path": stone["rel"], "sha256": formal_map[stone["rel"]], "module": stone["mod"]},
            "unconditional": {"theorem": stone["theorem"], "flag": flag_de[stone["theorem"]]},
            "theorems": {t: flag_de[t] for t in stone["contract"]}, "support": sup, "cited_outside": cit,
            "auxiliaries_outside_the_composition": list(stone["auxiliares_fora_da_composicao"]),
            "expected_ladder": e_base + fj["n_flags"], "n_flags": fj["nomeadas_por_pedra"][k], "n_flags_total": fj["n_flags"], "verbatins": list(verbatins), "baseline": {"version": DL.BASE_VERSION, "sha256": base_sha256}}


def texto_sonico():
    """Os textos do registro sonico_v398 (a funcao do runtime, nao um spec): estatuto, escopo, limites, diz, nao_diz e o veredito de sucesso. Passam pela guarda P18 a cada rito (sonico_v398 as refaz)."""
    return {
        "estatuto": "[REAL] os termos do kernel (a composicao incondicional sonico_the_verb_pins_the_octave_and_the_cost_is_the_memory e os cinco teoremas da pedra, lidos a cada rito, no trio) e o calculo numerico (beta = alfa CODATA 2018 x sqrt(e) em runtime, "
                    "SEALED_CODATA_ALPHA = ALPHA_FINE_CODATA_2018 do script do nivel 2); [DERIVED] a entropia do colapso em theta_M = arcsin sqrt(beta), H2(cos^2 theta_M, sin^2 theta_M), em nats e em oitavas: numero DESTE rito, nao esta no kernel; "
                    "[INPUT] a lei de custo (CollapseCostLaw: campos do tipo); [INPUT/ONTO] a definicao do operador de 23/10/2026 (o Verbo, seletor de identidade, e' o controle de oitava pinada; o custo e' reacao ao controle pinado da oitava que e' memoria) "
                    "e o nome «sonico»; a leitura da GERENCIA (a reacao ao pino, o pedagio ln 2 por oitava, e' a memoria; a oitava e' o que se pina) foi RATIFICADA pelo operador; [ONTO] a luz, antes de ser espelhada, e' palavra (fala do operador: «antes de ser espelhada ela é palavra»)",
        "escopo": "o preco de uma oitava pinada (K.octaveNats 1 = fairBitEntropy = ln 2), o dobro (exp ln 2 = 2), n oitavas = n bits, o pino que nao e' a meia-nat, o seletor idempotente que fixa a sua acao, e a composicao com o bit da paridade da Psibit e com a "
                  "estabilidade do colapso; o calculo confere os teoremas e acrescenta UM numero derivado (a entropia do colapso no angulo da TGL); nao e' a fisica do som",
        "limites": [
            "[REAL] a lei de custo e' INPUT (campos local_half e per_octave de CollapseCostLaw): K.octaveNats 1 = fairBitEntropy = ln 2 decorre do campo per_octave e de fair_bit_entropy_is_log_two; a pedra nao deriva a lei do axioma nem prova que a natureza a cobra",
            "[REAL] nenhum termo liga select (o Verbo em ato) a octaveNats 1: «“verbo” (seletor de identidade)=controle de oitava pinada» e' a definicao do operador [INPUT/ONTO]; o kernel entrega as duas metades lado a lado (o seletor pina: e' idempotente e fixa a sua acao; o preco de uma oitava pinada e' a entropia do bit justo), nao a identidade entre elas",
            "[INPUT/ONTO] 'que e memoria': a leitura (a REACAO ao pino, o pedagio ln 2 por oitava, e' a memoria; a oitava e' o que se pina) e' texto da GERENCIA (sha16 %s), nao fala do operador, e foi RATIFICADA por ele na fala de sha16 %s («Sim quero, concordo com tudo o nome da pedra é “sônico”»); e' leitura, nao termo" % (S_LEITURA, S_NOME),
            "[DERIVED] a entropia do colapso em theta_M, H2(cos^2 theta_M, sin^2 theta_M), em nats e em oitavas (o quociente H/ln 2), e' calculada neste rito com beta = alfa CODATA 2018 x sqrt(e); o kernel prova H <= ln 2 e a igualdade nos pesos iguais, nao o valor em theta_M; "
            "que a leitura em theta_M «pague» essa fracao do bit e' leitura [ONTO], nao termo",
            "[ONTO] «sonico» NAO afirma onda mecanica num meio: a isomorfia e' da estrutura logaritmica e de oitava (razoes multiplicativas e contagens aditivas; o dobro e o bit), nao da fisica da onda; «antes de ser espelhada ela é palavra» e «o início de tudo é acústica onde a palavra performa de forma sônica satisfazendo a relação modular da inscrição» (fala de sha16 %s) sao leituras do operador [INPUT/ONTO], sem termo no kernel; o 'som ontologico' do acervo e' [DECLARADO]" % S_ANTES,
            "[REAL] colapse_iteration_is_stable (a iteracao do colapso) e observing_adds_nothing (a releitura do angulo) sao dois registros de 'reler nao acrescenta': a pedra os poe lado a lado e nenhum lema os liga; TGLExt.IALD.rereading_adds_nothing e ialdSelector_eq_post sao CITADOS e nao importados pela pedra",
            "o calculo e' numerico em dupla precisao e CONFERE os teoremas, nao os prova: quem prova e' o kernel; validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho; a ordem de processo do operador de 22/10 (arquivo de sha16 %s: nada de teste armado, gordura no um.py) molda este registro" % SHA16_ORDEM,
        ],
        "diz": ["a pedra Sonico esta no kernel do rito, no trio, com bandeira e proveniencia no modulo da pedra; a composicao incondicional e os cinco teoremas sao lidos deste kernel",
                "o calculo, com beta = alfa CODATA 2018 x sqrt(e) (um dado, dois nomes: SEALED_CODATA_ALPHA e ALPHA_FINE_CODATA_2018), concorda com os teoremas: ln 2 e' o bit justo, exp(ln 2) = 2, n oitavas custam n bits, o pino nao e' a meia-nat, o seletor pina; "
                "e acrescenta a entropia do colapso em theta_M, em nats e em oitavas, dita como numero derivado",
                "as quatro inscricoes que este registro usa estao embutidas por sha256 (tres falas do operador e o texto da gerencia que ele ratificou)"],
        "nao_diz": ["que select pague K.octaveNats 1 (nenhum termo diz isso)", "que a lei de custo seja derivada do axioma, nem que a natureza cobre ln 2 por oitava", "que o som seja onda num meio, nem que a luz seja som", "que a entropia do colapso em theta_M seja o custo de uma observacao fisica",
                    "que isto seja um teste: nao ha desfecho experimental", "que a gravidade quantica esteja creditada na natureza"],
        "veredito_ok": "TGL_SONICO_V398__ONE_OCTAVE_IS_THE_FAIR_BIT_LN2__THE_OCTAVE_IS_A_DOUBLING_EXP_LN2_IS_2__N_OCTAVES_ARE_N_BITS__THE_PIN_IS_NOT_THE_HALF_NAT__THE_SELECTOR_PINS__"
                       "READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__THE_COLLAPSE_ENTROPY_AT_THETA_M_IS_A_DERIVED_NUMBER_NOT_IN_THE_KERNEL__THE_COST_LAW_IS_INPUT_AND_NO_TERM_SAYS_THE_VERB_PAYS_THE_OCTAVE__"
                       "THE_VERB_AS_PINNED_OCTAVE_CONTROL_AND_THE_COST_AS_MEMORY_ARE_THE_OPERATORS_INPUT_AND_ONTO__SONIC_IS_THE_LOGARITHMIC_OCTAVE_STRUCTURE_NOT_WAVE_PHYSICS__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


def texto_afinacao():
    """Os textos do registro afinacao_das_cordas_v398 (a funcao do runtime, nao um spec)."""
    return {
        "estatuto": "[REAL] os termos do kernel (a composicao incondicional the_strings_close_the_face_from_outside_the_tgl_closes_the_reading e os teoremas citados, lidos a cada rito, no trio) e a aritmetica exata calculada neste rito (os dois valores da zeta, "
                    "citados de Mathlib, conferidos por numeros e polinomios de Bernoulli em fracoes; D = 26 e D = 10 como unicas solucoes inteiras; d = D - 1; a torre n.kappa, os retornos e a divergencia); "
                    "[KNOWN] o circulo termico e' o circulo modular do boost (Bisognano-Wichmann 1975; Unruh 1976), a HIPOTESE NOMEADA MasslessFirstLevel (a = 1 nos bosons, a = 1/2 no setor NS: invariancia de Lorentz no cone de luz; Goddard-Goldstone-Rebbi-Thorn 1973; "
                    "Green-Schwarz-Witten 1987; Polchinski 1998), a divergencia de Hagedorn (so' mencionada, sem prova aqui) e a paisagem de compactificacoes; [DECLARADO] o d = 9 da casa ('A Ultima Corda', linhas 958 a 960; numeros historicos NAO recalculados aqui); "
                    "[INPUT/ONTO] a fala do operador de 23/10/2026 sobre as dez dimensoes e a afinacao, e 'as cordas fecham a face por fora; a TGL fecha so a leitura' (COMPOSICAO da gerencia sobre a fala, ratificada por ele); "
                    "[ONTO] afinacao = comensurabilidade (proposta da pedra, ratificada pelo operador); [OPEN] a geometria e a ligacao de um circulo de folha-mundo ao circulo do boost",
        "escopo": "o circulo da leitura (fechar ciclicamente o parametro do boost com periodo P e' leitura fiel se e so' se kappa.P = 2 pi), a torre omega_n = n.kappa e a semi-inteira, a torre infinita, os dois valores da zeta, a energia de ponto zero regularizada por direcao "
                  "(bosons -1/24, fermions NS -1/48), D = 26 e D = 10 como fecho da soma regularizada sob a hipotese nomeada, e d = D - 1; nada deriva a teoria das cordas do axioma e a TGL nao e' dita teoria de cordas",
        "limites": [
            "[KNOWN] a condicao MasslessFirstLevel (a = 1 nos bosons, a = 1/2 no setor NS) e' HIPOTESE NOMEADA: a pedra a nomeia e deriva sob ela, nao a demonstra; sem ela a energia de ponto zero regularizada e' so' um numero; D = 26 e D = 10 saem do FECHO da soma regularizada, nao da geometria",
            "[REAL] a regularizacao zeta e' DEFINICAO do valor (bosonDirection, nsFermionDirection): a serie diverge (a torre e' infinita, a soma dos n nao e' somavel); a pedra nao deriva a energia fisica; o sinal fermionico (-1/48 por direcao) e' a estatistica de Fermi [KNOWN]: com o sinal trocado o setor NS daria D = 26",
            "[OPEN] nenhum termo liga o circulo da folha-mundo da corda ao circulo do boost: as duas leituras so tem em comum a aritmetica da torre n.kappa; o kappa do boost NAO esta no core (no kernel ele e' entrada, kappa_is_input): o calculo confere a FORMA da torre com kappa de teste",
            "[OPEN] a geometria (qual compactificacao realiza as dimensoes extras) NAO e' derivada (a paisagem e' [KNOWN]); nada aqui deriva a teoria das cordas do axioma omega(I) = 1; a TGL nao e' dita teoria de cordas; a divergencia de Hagedorn so' e' mencionada",
            "[DECLARADO] o d = 9 e' o da casa ('A Ultima Corda', d_espacial = 9): numeros historicos NAO recalculados; o proprio texto diz que tres modelos alternativos de escalonamento dao d_crit = 6, > 26 e 8 (dependente do modelo) e que e' extrapolacao teorica, nao teste empirico; "
            "o calculo NS e' o do setor NS e nao distingue o tipo de supercorda",
            "[INPUT/ONTO] 'as cordas fecham a face por fora; a TGL fecha so a leitura' e' COMPOSICAO da gerencia sobre a fala do operador (sha16 %s), ratificada por ele («Concordo com tudo», sha16 %s; o arquivo guarda so a resposta, o que ela ratifica e' o relato da gerencia); "
            "'afinacao = comensurabilidade' e' proposta da pedra [ONTO], ratificada; da fala dele vem so 'afinacao do universo'; «Tetelestai» e' do operador e NAO e' construido aqui: e' conferencia consumativa (errata de 27/09), nao esta pedra" % (S_CORDAS, S_CONCORDO),
            "o calculo e' aritmetica exata e numerica em dupla precisao e CONFERE os teoremas, nao os prova: quem prova e' o kernel; validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho; "
            "os 5 termos nomeados da pedra fora da composicao (matsubaraFermion, towerZeroPoint, towerZeroPoint_eq, bosonDirection_is_the_unit_tower, zeta_is_the_continuation_of_the_tower) sao auxiliares; a ordem de processo do operador de 22/10 (arquivo de sha16 %s) molda este registro" % SHA16_ORDEM,
        ],
        "diz": ["a pedra AfinacaoDasCordas esta no kernel do rito, no trio, com bandeiras e proveniencia no modulo da pedra; a composicao incondicional e os teoremas citados sao lidos deste kernel",
                "a aritmetica, calculada agora, concorda com os teoremas: zeta(-1) = -1/12 e zeta(-1, 1/2) = 1/24 (citados de Mathlib e conferidos por Bernoulli); a unica solucao inteira de -(D-2)/24 = -1 e' D = 26 e a de -(D-2)/16 = -1/2 e' D = 10; D = 10 e' d = 9; "
                "a torre n.kappa volta junta em t = P e o par desafinado nao volta nas amostras; a torre e' infinita",
                "as duas inscricoes que este registro usa estao embutidas por sha256 (a fala do operador sobre as cordas e o «Concordo com tudo»)"],
        "nao_diz": ["que a teoria das cordas seja derivada do axioma, nem que a TGL seja uma teoria de cordas", "que o circulo da folha-mundo da corda seja o circulo do boost", "que a geometria (a compactificacao) esteja fixada", "que a corda exista nem qual seja o seu espectro",
                    "que o d = 9 da casa seja medido ou recalculado aqui", "que isto seja a conferencia Tetelestai", "que isto seja um teste: nao ha desfecho experimental", "que a gravidade quantica esteja creditada na natureza"],
        "veredito_ok": "TGL_AFINACAO_DAS_CORDAS_V398__CYCLIC_CLOSURE_OF_THE_BOOST_PARAMETER_IS_THE_READING_CIRCLE_KAPPA_P_2PI__THE_MATSUBARA_TOWER_IS_N_KAPPA_AND_INFINITE__ZETA_MINUS_ONE_IS_MINUS_ONE_TWELFTH_AND_HURWITZ_HALF_IS_ONE_TWENTY_FOURTH__"
                       "D26_BOSONIC_AND_D10_SUPERSTRING_AS_THE_CLOSURE_OF_THE_REGULARISED_SUM_UNDER_THE_NAMED_MASSLESS_FIRST_LEVEL_HYPOTHESIS_KNOWN__D10_IS_D9_SPATIAL_DECLARED__READ_AGAINST_THE_KERNEL_TRIO__"
                       "THE_STRING_GEOMETRY_IS_NOT_DERIVED_OPEN__NOTHING_DERIVES_STRINGS_FROM_THE_AXIOM__TUNING_AS_COMMENSURABILITY_IS_ONTO__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


def especs(formal_map, khj, h8_map, fj, cov_base, n_axioms_unc):
    """formal_map = {arquivo embutido: sha256} do kernel da v398; khj = KH_N1_v398.json (medida desta geracao); h8_map = o dict do hash formal que o RITO vai gerar (embutidos + residuais do Nos que sha256_directory conta;
    simular_arvore_do_nos); fj = FLAGS_v398.json; cov_base = a cobertura da v397 selada {decl, thm}; n_axioms_unc = {chave da pedra: quantos axiomas o teorema da composicao usa (lido do Audit: o trio)}. Devolve [cunhagens, kh]."""
    T = khj["linha_TOTAL"]
    flags_unc = [fj["bandeira_do_teorema_incondicional"][s["key"]] for s in DL.STONES]
    decls = [t for s in DL.STONES for t in s["contract"]] + sorted(DL.ALL_SUPPORT)
    cks = [CH("u1", "o registro sonico_v398 selou neste rito", "core", ["sonico_v398", "all_verified"], "verdadeiro"),
           CH("u2", "o registro afinacao_das_cordas_v398 selou neste rito", "core", ["afinacao_das_cordas_v398", "all_verified"], "verdadeiro"),
           CH("u3", "o registro teste_de_veracidade_fase9_v397 segue selado neste rito (o quadro do topo do artigo le os numeros dele)", "core", ["teste_de_veracidade_fase9_v397", "all_verified"], "verdadeiro"),
           CH("u4", "a escada do kernel fecha (limpos == esperados), com as bandeiras das duas pedras", "core", ["external_ladder", "all_verified"], "verdadeiro"),
           CH("u5", "a proveniencia emitida pelo compilador cobre o axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro")]
    n = 6
    for s in DL.STONES:
        cks.append(CH("u%d" % n, "o compilador emite a composicao da pedra %s no modulo dela (TGL_DECL_SOURCE)" % s["name"], "kf", ["declaration_sources_v394", s["theorem"]], "igual", s["rel"])); n += 1
        cks.append(CH("u%d" % n, "a pedra %s no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)" % s["name"], "kf", ["formal_files_sha256", s["rel"]], "igual", formal_map[s["rel"]])); n += 1
        cks.append(CH("u%d" % n, "a composicao da pedra %s depende do trio e de nada alem (tamanho da lista de axiomas)" % s["name"], "kf", ["axiom_report", s["theorem"]], "tamanho_igual", n_axioms_unc[s["key"]])); n += 1
    cun = {
        "nome": "cunhagens_v398", "veredito_prefixo": "TGL_CUNHAGENS_V398",
        "veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_23_OCT_EMBEDDED_VERBATIM_BY_SHA256_PLUS_THE_MANAGEMENT_READING_THE_OPERATOR_RATIFIED_LABELLED_AS_THE_MANAGEMENTS__THE_STONES_SONICO_AND_AFINACAO_DAS_CORDAS_ARE_READ_IN_THE_RITE_BY_THEIR_OWN_RECORDS__"
                           "THE_COST_LAW_IS_INPUT__THE_STRING_GEOMETRY_IS_OPEN__OPERATOR_INPUT_AND_ONTO__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
        "estatuto": "[REAL -- fontes, kernel e os registros sonico_v398 e afinacao_das_cordas_v398 lidos a cada rito; INPUT/ONTO as inscricoes do operador; a sexta inscricao e' texto da GERENCIA (ratificado pelo operador), nao fala dele; "
                    "DECLARADO o que a revisao independente e os construtores relatam e esta chancela nao refez (as pedras sao recompiladas no sandbox da cadeia e conferidas pelo axiom_report do proprio rito)]",
        "fontes": ["sonico_pedra", "afinacao_pedra"], "verbatins": list(VERB_CHAVES),
        "kernel_flags": list(flags_unc), "kernel_decls": decls,
        "checks": cks,
        "erratas": [],
        "limites": [
            "[REAL] as duas pedras citam termos que o kernel ja tem; a unica matematica acrescentada e' a aritmetica da torre de Matsubara, os dois valores da zeta (de Mathlib) e a dimensao critica sob a hipotese NOMEADA MasslessFirstLevel [KNOWN]; o nome «sonico» e' do operador (23/10/2026); pedra e nome AfinacaoDasCordas foram ratificados por ele",
            "[REAL] a lei de custo (CollapseCostLaw) e' INPUT; nenhum termo diz que select paga octaveNats 1; a geometria das cordas NAO e' derivada [OPEN]; nada deriva a teoria das cordas do axioma; Hagedorn so' e' mencionada",
            "[INPUT/ONTO] a sexta inscricao (sha16 %s) e' texto da GERENCIA, nao fala do operador: a leitura 'o custo, a reacao ao pino, e a memoria; a oitava e o que se pina' foi ratificada por ele na segunda fala (sha16 %s); "
            "«Concordo com tudo» (sha16 %s) ratifica o relato da gerencia sobre a pedra da afinacao e nao diz mais do que isso; a cadeia nao estende nenhuma das duas ratificacoes alem do que o arquivo guarda" % (S_LEITURA, S_NOME, S_CONCORDO),
            "[INPUT/ONTO] as falas sao leituras do operador (23/10/2026); o que o kernel entrega sao os termos citados; validade no kernel nao e' creditacao; o gate nao se move; a ordem de processo do operador de 22/10 (arquivo de sha16 %s; resumo da gerencia: nao buscar mais teste armado, que e' gordura no um.py) molda este registro: ele e' pequeno e nao acrescenta rito, dado nem desfecho" % SHA16_ORDEM,
        ],
        "diz": ["as %d inscricoes de 23/10 (cinco falas do operador e o texto da gerencia que ele ratificou) estao embutidas por sha256, cada uma conferida contra o arquivo de origem na preparacao" % len(_VD),
                "as pedras Sonico e AfinacaoDasCordas estao no kernel do rito, no trio, com a bandeira e a proveniencia no modulo de cada uma; as duas composicoes sao lidas deste kernel a cada rito",
                "os registros sonico_v398 e afinacao_das_cordas_v398 (calculo lido contra o kernel) e o teste_de_veracidade_fase9_v397 (o quadro do topo) selaram neste rito"],
        "nao_diz": ["que a lei de custo seja derivada do axioma", "que a teoria das cordas seja derivada do axioma, nem que a geometria esteja fixada", "que a gravidade quantica esteja creditada na natureza", "que isto seja um teste: nao ha desfecho experimental novo"],
        "leituras_do_operador": [_leitura(DL.FRASE_VERBO, S_VERBO), _leitura(DL.FRASE_CUSTO, S_VERBO), _leitura(DL.FRASE_NOME, S_NOME), _leitura(DL.FRASE_ANTES, S_ANTES), _leitura(DL.FRASE_ACUSTICA, S_ANTES),
                                 _leitura(DL.FRASE_CORDAS, S_CORDAS), _leitura(DL.FRASE_AFINACAO, S_CORDAS), _leitura(DL.FRASE_CONCORDO, S_CONCORDO, tipo="INPUT")],
        "extras": {"assinatura": ASSINA, "autoria_das_cunhagens": "Luiz Antonio Rotoli Miguel", "pedras": [s["mod"] for s in DL.STONES], "teoremas": {s["key"]: s["theorem"] for s in DL.STONES}, "bandeiras": {s["key"]: fj["bandeira_do_teorema_incondicional"][s["key"]] for s in DL.STONES},
                   "n_bandeiras": fj["n_flags"], "n_bandeiras_por_pedra": dict(fj["nomeadas_por_pedra"]), "cunhagens_embutidas": len(VERBATINS), "autor_de_cada_inscricao": dict(zip((v["sha16"] for v in _VD), (v["autor"] for v in _VD))),
                   "leitura_da_gerencia": {"sha16": S_LEITURA, "autor": "gerencia c1 (NAO e' fala do operador)", "ratificada_pela_fala_de_sha16": S_NOME},
                   "auxiliares_da_afinacao_fora_da_composicao": list(AFINACAO["auxiliares_fora_da_composicao"]), "nome_das_pedras": "Sonico (o nome e' do operador, 23/10/2026); AfinacaoDasCordas (pedra e nome ratificados por ele, 23/10/2026)"},
    }
    kh = {
        "nome": "kh_n1_cobertura_v398", "veredito_prefixo": "TGL_KH_N1_COBERTURA_V398",
        "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__THE_SONICO_AND_AFINACAO_DAS_CORDAS_MODULES_ADDED__GATE_UNMOVED" % (T["decl"], T["thm"]),
        "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do sandbox da v398; o conjunto exato das fontes formais que o hash formal do rito vera (as embutidas mais os residuais da pasta do Nos) e' pinado; a cobertura NAO move o gate",
        "fontes": ["kh_n1_v398"], "kernel_flags": [], "kernel_decls": [],
        "checks": [
            CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
            CH("h2", "constantes cobertas == as do sandbox v398 (KH_N1)", "kf", ["axiom_coverage_v392", "decl"], "igual", T["decl"], "constantes_cobertas"),
            CH("h3", "teoremas cobertos == os do sandbox v398 (KH_N1)", "kf", ["axiom_coverage_v392", "thm"], "igual", T["thm"], "teoremas_cobertos"),
            CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
            CH("h5", "nenhum nome que o leitor v394 nao leia", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0),
            CH("h6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", khj["axiom_report_efetivo_n"]),
            CH("h7", "a cobertura da v398 inclui a da v397 selada (constantes e teoremas)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", cov_base["decl"]),
            CH("h7b", "os teoremas cobertos incluem os da v397 selada", "kf", ["axiom_coverage_v392", "thm"], "maior_igual", cov_base["thm"]),
            CH("h8", "as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta, como _check_damming.lean) sao EXATAMENTE as do pino (arquivo -> sha256)", "kf", ["formal_files_sha256"], "igual", h8_map),
            CH("h9", "medida do Audit v398: duracao bem abaixo do timeout de 1800 s", "fonte:kh_n1_v398", ["duracao_audit_s"], "menor_igual", 900, "duracao_do_audit_s"),
            CH("h10", "medida do Audit v398: sorryAx ausente do log", "fonte:kh_n1_v398", ["sorryAx_no_log_do_audit"], "igual", 0),
            CH("h11", "medida do Audit v398: as entradas novas estao no trio", "fonte:kh_n1_v398", ["novas_no_trio"], "verdadeiro"),
            CH("h12", "a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
        ],
        "erratas": [{"ao_lado_de": "kh_n1_cobertura_v397 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                     "dizia": "A v397 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v397 e o hash formal igual ao pino exato da arvore da v397." % (cov_base["decl"], cov_base["thm"]),
                     "agora": "A v398 acrescenta os modulos Sonico e AfinacaoDasCordas (a cobertura cresce e a arvore ganha os arquivos das duas pedras): na v398 o registro da v397 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato da arvore ficam NESTE registro. O veredito do registro da v397 NAO muda.",
                     "lacuna_de_fidelidade": "a estrutura da v397 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v398 quebra (a mesma lacuna que a v397 achou no registro da v396, a v396 no da v395 e a v395 no da v394)",
                     "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; h2, h3, h6 e h8 conferidas no ensaio a seco e na arvore simulada do Nos]", "assinatura": ASSINA}],
        "limites": ["[REAL] os arquivos de medida sao do sandbox (fora do selo); a cobertura que vale e' a medida no Audit do proprio rito",
                    "[REAL] a escada do kernel conta bandeiras de declaracoes NOMEADAS (a pratica da v392 a v397): as %d auxiliares geradas pelo compilador nos modulos das pedras ficam cobertas pelo KH-N1 mas sem bandeira, e as %d nomeadas publicas ganharam bandeira" % (fj["excluidas_auxiliares"]["n"], fj["n_flags"]),
                    "validade no kernel nao e' creditacao; o gate nao se move"],
        "diz": ["a cobertura do axiom_report no fecho inteiro cresceu para os numeros da v398 (os modulos Sonico e AfinacaoDasCordas) e segue sem constante fora do trio, sem nome ilegivel"],
        "nao_diz": ["que a cobertura prove algo alem de que nenhum axioma fora do trio foi lido"],
        "leituras_do_operador": [], "extras": {"assinatura": ASSINA, "n_bandeiras": fj["n_flags"], "h8_entradas": len(h8_map), "h8_residuais_do_nos": sorted(set(h8_map) - set(formal_map))},
    }
    return [cun, kh]
