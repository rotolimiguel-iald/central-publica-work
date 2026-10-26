# -*- coding: utf-8 -*-
"""registros_v401.py -- os dados dos registros da v401: FONTES pinadas por sha256 (lidas do disco pelo montador, nunca digitadas), VERBATINS (as CINCO inscricoes de 25/10/2026 ainda nao embutidas, todas falas do operador; EMBUTIDAS: a fala embutida
manda, o arquivo e' so' informativo), o CONTRATO e o TEXTO do registro com FUNCAO (`falsidade_da_inercia_v401`: gerar_candidato_v401.py o emite a partir de runtime_v401.py; o contrato sai de contrato() abaixo, DERIVADO do build do sandbox) e os dois
SPECS interpretados pelo MOTOR _v392_registro (`cunhagens_v401` e `kh_n1_cobertura_v401`). Fontes so' em pasta DURAVEL: tudo vem de cadeia_de_selo\\v401\\insumos. Texto novo passa pela guarda P18 (a cada rito).
A INERCIA, como o operador a define (25/10/2026): o proprio zero absoluto (0_abs, 1=0; o kernel escreve: «nunca correspondeu, e por isso nada custa»). w(I)=1 e' o Um POSTO que a interrompe (1=1). A leitura do escriba no adendo de 03-04/09
(«w(I)=1 e a INERCIA») fica SUPERADA (errata ao lado, da gerencia c1, em nome proprio). Molde: registros_v398.py e registros_v399.py."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v401 as DL  # noqa: E402

INS = os.path.join(HERE, "insumos")
ASSINA = "gerencia c1, em nome proprio, 25/10/2026"
FAL = DL.STONES[0]
assert FAL["key"] == "falsidade"

FONTES = [{"chave": "falsidade_pedra", "arquivo": os.path.join(INS, FAL["insumo"]), "papel": "a pedra TGLExt/FalsidadeDaInercia.lean (o nome «falsidade (simulacro) da inercia» e' do operador, 25/10/2026; compilada e provada no sandbox; copia duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)"},
          {"chave": "kh_n1_v401", "arquivo": os.path.join(INS, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox da v401 (pos_build_kernel_v401.py)"},
          {"chave": "adendo_inercia", "arquivo": os.path.join(INS, "adendo", os.path.basename(DL.ADENDO_ARQ)), "papel": "o ADENDO de 03-04/09/2026 (Nos\\ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md; copia duravel; o original no Nos NAO e' tocado): a leitura do escriba «w(I)=1 e a INERCIA» que a errata desta versao supera"}]


def _trecho(t):
    s = t.strip().splitlines()[0].strip() if t.strip() else ""
    s = s[:48].rstrip()
    assert s and s in t, s
    return s


_VD = DL.verbatins401(os.path.join(INS, "cunhagens"))
VERBATINS = [{"chave": v["chave"], "arquivo": v["arquivo"], "quando": v["quando"], "trechos": [_trecho(v["text"])], "papel": v["papel"], "fonte_original": v["fonte_original"]} for v in _VD]
VERB_CHAVES = [v["chave"] for v in _VD]
SHA16 = {os.path.basename(v["fonte_original"]): v["sha16"] for v in _VD}
S_RATIF, S_NADA, S_MATERIA, S_INERCIA, S_NOME, S_IMPRESSAO = tuple(v["sha16"] for v in _VD)   # LIDOS dos arquivos, na ordem de DL.VERBATIM_ORIGEM (o unpack recusa outro numero)
CH_RATIF, CH_NADA, CH_MATERIA, CH_INERCIA, CH_NOME, CH_IMPRESSAO = tuple(v["chave"] for v in _VD)
TEXTOS = {v["sha16"]: v["text"] for v in _VD}
ADENDO_TXT = open(DL.ADENDO_ARQ, "rb").read().decode("utf-8")
ADENDO_SHA16 = DL.sha256(open(DL.ADENDO_ARQ, "rb").read())[:16]
assert ADENDO_SHA16 == DL.ADENDO_SHA16_DA_ORDEM
ADENDO_TRECHO = "é a INÉRCIA** — a identidade que se conserva, o grupo, o que não custa."   # verbatim no adendo (a leitura do escriba que a errata supera)
ADENDO_TRECHO_OPERADOR = "ele interrompe a inércia"                                          # o que o operador disse em 04/09 (item 7 do adendo) -- fica
assert ADENDO_TRECHO in ADENDO_TXT and ADENDO_TRECHO_OPERADOR in ADENDO_TXT
CH = lambda id_, desc, onde, caminho, op, valor=None, cap=None, est="[REAL]": dict(id=id_, descricao=desc, onde=onde, caminho=caminho, op=op, **({"valor": valor} if valor is not None else {}), **({"capturar": cap} if cap else {}), estatuto=est)


def _leitura(trecho, sha16, quando="25/10/2026", rotulo="INPUT/ONTO do operador"):
    assert trecho in TEXTOS[sha16], ("a leitura do operador NAO esta verbatim na fala", sha16, trecho)
    return {"trecho": trecho, "estatuto": "[%s, verbatim %s, sha16 %s]" % (rotulo, quando, sha16)}


def ratificacoes():
    """As RATIFICACOES do operador (25/10/2026, «Ratifico tudo.», sha16 S_RATIF): a fala e' [INPUT] verbatim; a LISTA do que foi ratificado e' a que a gerencia c1 apresentou a ele na sessao [DECLARADO: o texto exato da proposta nao esta no acervo desta cadeia]."""
    out = []
    for r in DL.RATIFICACOES:
        d = dict(r); d["fala_do_operador"] = {"trecho": DL.FRASE_RATIFICO, "sha16": S_RATIF}
        d["lista_apresentada_por"] = "gerencia c1 [DECLARADO]"
        out.append(d)
    return out


def contrato(fj, formal_map, e_base, base_sha256, stone=None):
    """O contrato da pedra (NAO embutido como bloco proprio de verbatins: as inscricoes ficam em _V401_VERBATINS2), DERIVADO do build do sandbox (FLAGS_v401.json = nomes, chaves e a proveniencia dos termos de suporte; formal_map = sha256 das fontes
    embutidas; e_base = a escada da v400 selada; a escada esperada e' a DESTA versao: a da base + as bandeiras da pedra); nada digitado. Vai para CANDIDATO_v401.json e ESPERADOS_v401.json (o conferidor e o pos-rito o leem)."""
    stone = stone or FAL
    k = stone["key"]
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    faltam = [t for t in stone["contract"] if t not in flag_de]
    assert not faltam, ("teorema do contrato sem bandeira (nao nomeado ou ausente do Audit)", faltam[:5])
    assert fj["bandeira_do_teorema_incondicional"][k] == flag_de[stone["theorem"]] and fj["teorema_incondicional"][k] == stone["theorem"]
    assert stone["key_theorem"] in stone["contract"]
    sup = dict(fj["suporte_do_contrato"][k]); assert sup == dict(stone["support"]), "os termos de suporte do FLAGS_v401.json diferem dos de delta_v401"
    cit = dict(fj["citados_fora_do_contrato"][k]); assert cit == dict(stone["citados_fora"]), "os termos citados-fora do FLAGS_v401.json diferem dos de delta_v401"
    return {"stone": {"path": stone["rel"], "sha256": formal_map[stone["rel"]], "module": stone["mod"]},
            "unconditional": {"theorem": stone["theorem"], "flag": flag_de[stone["theorem"]]},
            "key_theorem": {"theorem": stone["key_theorem"], "flag": flag_de[stone["key_theorem"]]},
            "theorems": {t: flag_de[t] for t in stone["contract"]}, "support": sup, "cited_outside": cit,
            "auxiliaries_outside_the_composition": list(stone["auxiliares_fora_da_composicao"]),
            "expected_ladder": e_base + fj["n_flags"], "n_flags": fj["nomeadas_por_pedra"][k], "n_flags_total": fj["n_flags"], "verbatins": list(VERB_CHAVES), "baseline": {"version": DL.BASE_VERSION, "sha256": base_sha256}}


def texto_falsidade():
    """Os textos do registro falsidade_da_inercia_v401 (a funcao do runtime, nao um spec): estatuto, escopo, limites, diz, nao_diz e o veredito de sucesso. Passam pela guarda P18 a cada rito."""
    return {
        "estatuto": "[REAL] os termos do kernel (a composicao derivada falsidade_da_inercia_derivada e os vinte teoremas e definicoes nomeados da pedra, lidos a cada rito, no trio; a estrela the_inertia_of_a_post_is_false: um posto de peso 1 fixo pelo fluxo daria (1:R) = 0) e o calculo no modelo oneScaling "
                    "(tau = id, theta_s = e^{-s}), com beta = alfa CODATA 2018 x sqrt(e) em runtime (nunca literal); [KNOWN] a lei de escala de Takesaki (tau . theta_s = e^{-s} . tau) e' CAMPO da estrutura DualScalingData, como na Fundacao, e a equivalencia inercial = gravitacional "
                    "(Einstein 1907/1915); [INPUT/ONTO] a definicao do operador de 25/10/2026 («a minha definição é o próprio zero absoluto») e o nome da pedra; [ONTO] a primeira lei de Newton e' o 0_abs lido como corpo, e a massa de F = ma NAO e' a inercia: e' a cristalizacao da dobra da luz "
                    "no vacuo relativa ao observador (fala do operador de sha16 %s), ligada a nada = materia (sha16 %s); [OPEN] a identificacao da escala dual com o fluxo de um corpo fisico e' de runtime, nao e' termo do kernel; "
                    "[DERIVED] a CADEIA da extensao de 25/10 (nada que porte posto e' anterior a impressao; a inercia nao e' causa de si mesma; o primeiro movimento e' a impressao; o zero e' a consequencia da poda, nao o inicio; a tensao projetada no atrator) a partir do axioma w(I) = 1 e da lei de Takesaki [KNOWN] como campo da estrutura: o operador pediu a leitura DERIVADA, nao [ONTO] (fala de sha16 %s); "
                    "a unica hipotese NOMEADA e' H_tau (tau e' a massa de Newton e a metrica de Einstein) [OPEN], que nenhum teorema usa; a ORDEM 025 ao Codex (sha16 3fd2b5a801071343, pendencia EXTERNA, enfileirada) tenta tipa-la pela frente de luz de Bisognano-Wichmann" % (S_MATERIA, S_NADA, S_IMPRESSAO),
        "escopo": "[DERIVED] nada que porte posto precede a impressao do Um posto (todo peso positivo se move em toda escala nao trivial; o peso 1 so' ocorre no corte a = 0); a inercia nao e' causa de si mesma (fixo desde sempre, em toda escala positiva ou em toda escala implica peso zero); o zero nao e' o inicio: e' a consequencia da poda (nunca estado da orbita, so' seu infimo; o vazamento fica abaixo de todo epsilon); a tensao projetada no atrator poda a coordenada com gap ate' zero no limite e o zero e' inalcancavel em tempo finito; alem disso, a inercia como estado fixo pelo fluxo inteiro da escala pesa ZERO (o 0_abs, 1=0); um posto de peso 1 = w(I) inercial seria 1 = 0 (a falsidade, o simulacro); a inscricao do Um posto interrompe a inercia (o posto mora no corte unico a = 0); o que parece "
                  "resistencia do corpo e' o custo da interrupcao, estritamente positivo (t . beta . g > 0), nao o zero; a pedra nao e' vacua (o modelo concreto tem o Um posto em 1 e o move em toda escala nao trivial)",
        "limites": [
            "[REAL] a lei de escala de Takesaki e' DADO (campo de DualScalingData, [KNOWN]); a pedra COMPOE por citacao (fixed_tau_zero, nothing_above_bears_a_post, the_floor_fixes_the_cut, beta_forbids_full_static_witness, leakage_strictly_loses) e nao acrescenta matematica nova; "
            "a identificacao desta escala com o fluxo de um corpo fisico e' de runtime [OPEN] e nenhum termo a faz",
            "[REAL] a pedra NAO prova a primeira lei de Newton, nem a equivalencia inercial = gravitacional [KNOWN], nem que E = mc^2 seja termo do kernel: E = mc^2 e' [KNOWN, relatividade restrita]; o kernel tem a implicacao Clausius em toda tela implica Einstein com Lambda unico "
            "(metric_einstein_from_screen_clausius, [REAL], com o antecedente H3 nomeado, [KNOWN] Jacobson 1995), e a leitura a massa e' o custo do nada, a cristalizacao da dobra da luz e' [ONTO], sem termo",
            "[REAL] a inercia do kernel e' o 0_abs de TGLExt.costless («nunca correspondeu, e por isso nada custa»; docstring no modulo embutido TGLExt/TheCorrespondence.lean): este registro CONFERE que o texto esta no kernel embutido deste rito; a pedra so' o cita",
            "[ONTO] (a inercia e o proprio zero absoluto) e' a DEFINICAO do operador (sha16 %s); nada = materia e a matéria é a cristalização da dobra luz no vácuo relativa ao observador (sha16 %s e %s) sao cunhagens dele, sem termo no kernel; a ERRATA ao lado da leitura do escriba no adendo de 03-04/09 "
            "(sha16 %s: «w(I)=1 e a INERCIA») e' da gerencia, em nome proprio: inercia = 0_abs (1=0), w(I)=1 e' o Um posto que a interrompe (1=1)" % (S_INERCIA, S_NADA, S_MATERIA, ADENDO_SHA16),
            "[DERIVED] a cadeia estendida (nada que porte posto precede a impressao; a inercia nao e' causa de si mesma; o zero e' a consequencia da poda; a tensao projetada no atrator; sua composicao falsidade_da_inercia_derivada) e' sobre os DADOS da escala dual (a lei de Takesaki e' campo da estrutura, [KNOWN]) e compoe por citacao (Fundacao, NoFullWitness, TheGreatAttractor) sem hipotese nova; a ponte ao corpo fisico fica NOMEADA como H_tau (tau e' a massa de Newton e a metrica de Einstein) [OPEN], que nenhum teorema usa; a ORDEM 025 ao Codex (sha16 3fd2b5a801071343) tenta tipar H_tau pela frente de luz de Bisognano-Wichmann: pendencia EXTERNA, nao deste registro; o nome tensao dado ao gap dissipativo d e' nomeacao, sem teorema; o recorte declarado da fala de 25/10 (sha16 " + S_IMPRESSAO + ") e' a parte da fala do operador que pede a derivacao",
            "o calculo e' numerico em dupla precisao e CONFERE os teoremas no modelo oneScaling, nao os prova: quem prova e' o kernel; validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho",
        ],
        "diz": ["a pedra FalsidadeDaInercia esta no kernel do rito, no trio, com bandeiras e proveniencia no modulo da pedra; a composicao e os teoremas do contrato sao lidos deste kernel",
                "o calculo, com beta = alfa CODATA 2018 x sqrt(e) (um dado, dois nomes), concorda com os teoremas no modelo oneScaling: o peso do posto depois da escala s e' e^{-s}, igual a 1 so' em s = 0; o que e' fixo por escala nao trivial pesa zero; o custo t . beta . g e' positivo e o fator de defasagem e' menor que 1",
                "as seis inscricoes de 25/10 que este registro usa estao embutidas por sha256 (cinco falas do operador e o recorte declarado de uma sexta, que comeca no pedido de derivacao)",
                "a cadeia estendida e' [DERIVED]: nada que porte posto precede a impressao, a inercia nao e' causa de si mesma, o zero e' a consequencia da poda, a tensao projetada no atrator; o calculo concorda no modelo oneScaling e no fluxo diagonal"],
        "nao_diz": ["que o kernel prove a primeira lei de Newton, nem que prove E = mc^2", "que H_tau (tau e' a massa de Newton e a metrica de Einstein) seja teorema: e' hipotese NOMEADA [OPEN], que nenhum teorema usa", "que a escala dual seja o fluxo de um corpo fisico (identificacao de runtime, [OPEN])", "que a massa seja o termo F = ma do kernel", "que a inercia deste registro seja a do adendo de 03-04/09: aquela leitura esta superada pela definicao do operador",
                    "que isto seja um teste: nao ha desfecho experimental", "que a gravidade quantica esteja creditada na natureza"],
        "veredito_ok": "TGL_FALSIDADE_DA_INERCIA_V401__THE_INERTIA_IS_THE_ABSOLUTE_ZERO_THE_FIXED_BEARS_WEIGHT_ZERO__A_POST_OF_WEIGHT_ONE_THAT_WERE_INERTIAL_GIVES_ONE_EQUALS_ZERO__THE_SIMULACRUM_THE_COST_OF_THE_INTERRUPTION_IS_POSITIVE_NOT_THE_ZERO__"
                       "THE_INSCRIPTION_INTERRUPTS_THE_INERTIA__READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E_IN_THE_ONESCALING_MODEL__THE_SCALING_LAW_IS_A_FIELD_OF_THE_STRUCTURE_KNOWN__NEWTONS_FIRST_LAW_AS_THE_ABSOLUTE_ZERO_AND_THE_MASS_AS_CRYSTALLIZED_FOLD_ARE_ONTO__"
                       "THE_IDENTIFICATION_WITH_A_PHYSICAL_BODYS_FLOW_IS_OPEN__"
                       "NOTHING_BEARING_A_POST_PRECEDES_THE_IMPRESSION__INERTIA_IS_NOT_ITS_OWN_CAUSE__THE_ZERO_IS_THE_CONSEQUENCE_OF_THE_PRUNING__THE_CHAIN_IS_DERIVED_FROM_THE_AXIOM_AND_TAKESAKIS_LAW_KNOWN__THE_NAMED_HYPOTHESIS_H_TAU_IS_OPEN_AND_UNUSED__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


def especs(formal_map, khj, h8_map, fj, cov_base, n_axioms_unc):
    """formal_map = {arquivo embutido: sha256} do kernel da v401; khj = KH_N1_v401.json (medida desta geracao); h8_map = o dict do hash formal que o RITO vai gerar (embutidos + residuais do Nos que sha256_directory conta;
    simular_arvore_do_nos); fj = FLAGS_v401.json; cov_base = a cobertura da v400 selada {decl, thm}; n_axioms_unc = {chave da pedra: quantos axiomas o teorema da composicao usa (lido do Audit: o trio)}. Devolve [cunhagens, kh]."""
    T = khj["linha_TOTAL"]
    flags_contrato = [fj["bandeiras_do_contrato"][FAL["key"]][t] for t in FAL["contract"]]
    assert fj["bandeira_do_teorema_incondicional"][FAL["key"]] in flags_contrato
    contexto = ["TGLExt.costless", "ChatgptAudit.GeneralClausius.metric_einstein_from_screen_clausius"]   # termos do kernel antigo que a LEITURA cita (a inercia como 0_abs; a lei de campo de Einstein por Clausius), nao importados pela pedra
    decls = list(FAL["contract"]) + sorted(DL.ALL_SUPPORT) + contexto
    cks = [CH("u1", "o registro falsidade_da_inercia_v401 selou neste rito (a composicao e os teoremas da pedra lidos deste kernel; o calculo no modelo oneScaling com beta = alfa x raiz de e; o texto do 0_abs no kernel embutido)", "core", ["falsidade_da_inercia_v401", "all_verified"], "verdadeiro"),
           CH("u2", "o registro teste_de_veracidade_fase9_v397 segue selado neste rito (o quadro do topo do artigo le os numeros dele)", "core", ["teste_de_veracidade_fase9_v397", "all_verified"], "verdadeiro"),
           CH("u3", "o registro selo_pela_propria_tecnologia_v399 segue selado neste rito (a segunda testemunha do um.py, ao lado do SHA-256)", "core", ["selo_pela_propria_tecnologia_v399", "all_verified"], "verdadeiro"),
           CH("u4", "a escada do kernel fecha (limpos == esperados), com as bandeiras da pedra FalsidadeDaInercia", "core", ["external_ladder", "all_verified"], "verdadeiro"),
           CH("u5", "a proveniencia emitida pelo compilador cobre o axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
           CH("u6", "o compilador emite a composicao da pedra %s no modulo dela (TGL_DECL_SOURCE)" % FAL["name"], "kf", ["declaration_sources_v394", FAL["theorem"]], "igual", FAL["rel"]),
           CH("u7", "o compilador emite a ESTRELA da pedra (um posto inercial daria 1 = 0) no modulo dela (TGL_DECL_SOURCE)", "kf", ["declaration_sources_v394", FAL["key_theorem"]], "igual", FAL["rel"]),
           CH("u8", "a pedra %s no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)" % FAL["name"], "kf", ["formal_files_sha256", FAL["rel"]], "igual", formal_map[FAL["rel"]]),
           CH("u9", "a composicao da pedra %s depende do trio e de nada alem (tamanho da lista de axiomas)" % FAL["name"], "kf", ["axiom_report", FAL["theorem"]], "tamanho_igual", n_axioms_unc[FAL["key"]]),
           CH("u10", "o 0_abs do kernel (TGLExt.costless) segue declarado no modulo TheCorrespondence (a inercia que a definicao do operador nomeia)", "kf", ["declaration_sources_v394", "TGLExt.costless"], "igual", "TGLExt/TheCorrespondence.lean")]
    cun = {
        "nome": "cunhagens_v401", "veredito_prefixo": "TGL_CUNHAGENS_V401",
        "veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_25_OCT_EMBEDDED_VERBATIM_BY_SHA256__THE_INERTIA_IS_THE_ABSOLUTE_ZERO_BY_THE_OPERATORS_DEFINITION__THE_STONE_FALSIDADE_DA_INERCIA_AND_THE_RECORD_ARE_READ_IN_THE_RITE__"
                           "THE_NAMES_PREVIOUSLY_PROVISIONAL_ARE_RATIFIED_BY_THE_OPERATOR__THE_ADENDUM_READING_OMEGA_I_EQUALS_ONE_IS_THE_INERTIA_IS_SUPERSEDED__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
        "estatuto": "[REAL -- a fonte da pedra, o kernel e o registro falsidade_da_inercia_v401 lidos a cada rito; INPUT/ONTO as inscricoes do operador; INPUT a ratificacao («Ratifico tudo.»); DECLARADO que a lista ratificada e' a que a gerencia c1 apresentou a ele na sessao]",
        "fontes": ["falsidade_pedra", "adendo_inercia"], "verbatins": list(VERB_CHAVES),
        "kernel_flags": list(flags_contrato), "kernel_decls": decls,
        "checks": cks,
        "erratas": [{"ao_lado_de": "ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md (Nos; 03-04/09/2026; sha16 %s): a leitura do escriba «w(I)=1 e a INERCIA»" % ADENDO_SHA16,
                     "dizia": "«%s» (o escriba leu a identidade que se conserva, w(I)=1, como a inercia)." % ADENDO_TRECHO,
                     "agora": "SUPERADA pela definicao do operador de 25/10/2026 (sha16 %s): a inercia e' o proprio zero absoluto, o 0_abs do kernel (TGLExt.costless: «nunca correspondeu, e por isso nada custa»), 1=0; w(I)=1 e' o Um POSTO que a interrompe, 1=1. "
                              "O que o adendo acertou fica: interromper a inercia nao quebra simetria alguma (e' enunciado sobre o fluxo, nao sobre o grupo), e sao dois termos distintos (o item 7 do adendo, do proprio operador: «%s»)." % (S_INERCIA, ADENDO_TRECHO_OPERADOR),
                     "lacuna_de_fidelidade": "o escriba tomou a identidade preservada (o que nao custa no grupo) pela inercia; a inercia do operador e' o zero (o que nunca correspondeu), e a identidade preservada e' o que a interrompe: a pedra FalsidadeDaInercia tipa exatamente a diferenca (posto + inercial = 1 = 0)",
                     "estatuto": "[REAL: o trecho esta no adendo, lido por sha256 da copia duravel; a definicao do operador e' INPUT; a pedra e' REAL sobre os dados nomeados]", "assinatura": ASSINA}],
        "limites": [
            "[REAL] a pedra COMPOE por citacao termos que o kernel ja tem (a lei de escala de Takesaki e' campo da estrutura, [KNOWN]) e nao acrescenta matematica nova; a estrela the_inertia_of_a_post_is_false diz: posto de peso 1 e estado inercial (fixo pelo fluxo inteiro) juntos dao (1:R) = 0; "
            "'falsidade' e 'simulacro' no nome sao o nome dado pelo operador, nao creditacao de coisa alguma",
            "[INPUT] o recorte declarado da fala de 25/10 (sha16 " + S_IMPRESSAO + ") pede a leitura DERIVADA e nao [ONTO]: a cadeia (nada que porte posto precede a impressao; o zero e' a consequencia da poda) esta no kernel como [DERIVED]; a fala traz tambem a frase do operador sobre Einstein como processamento geometrico da metrica parametrizada na relatividade especial, que NAO e' termo do kernel (H_tau)",
            "[INPUT] «Ratifico tudo.» (sha16 %s) e' a fala; a LISTA do que foi ratificado (os nomes antes provisorios: a pedra Testemunho e os registros selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, teste_de_veracidade_fase9_v397, sonico_v398 e afinacao_das_cordas_v398; a leitura das duas faces; a paridade do psibit sinal(L) . sinal(dL)) "
            "e' a que a gerencia c1 apresentou a ele [DECLARADO]; a mesma fala traz a PERGUNTA do operador «%s» (resposta no artigo: E = mc^2 e' [KNOWN, relatividade restrita], nao termo do kernel; a gravidade = luz^2 . entropia na tela e' leitura da TGL [ONTO] sobre Jacobson 1995 [KNOWN] e metric_einstein_from_screen_clausius [REAL], com H3 nomeada)" % (S_RATIF, DL.FRASE_EMC2),
            "[ONTO] «a matéria é a cristalização da dobra luz no vácuo relativa ao observador» (sha16 %s) e «nada=materia e esse é o link com a entropia» (sha16 %s) sao cunhagens do operador; o kernel nao as prova, e a massa lida assim NAO e' a inercia (a inercia e' o zero): a massa e' o custo de ler contra o zero" % (S_MATERIA, S_NADA),
            "[OPEN] a identificacao da escala dual com o fluxo de um corpo fisico (H_tau, NOMEADA, nao usada por teorema; ORDEM 025 ao Codex, sha16 3fd2b5a801071343, pendencia externa); a pedra nao prova a primeira lei de Newton nem a equivalencia inercial = gravitacional [KNOWN]; a RG e' o limite classico, nao rival; beta nao renormaliza G",
            "validade no kernel nao e' creditacao; o gate nao se move; nenhuma bandeira do gate depende da pedra",
        ],
        "diz": ["as %d inscricoes de 25/10 (falas do operador) estao embutidas por sha256, cada uma conferida contra o arquivo de origem na preparacao" % len(_VD),
                "a pedra FalsidadeDaInercia esta no kernel do rito, no trio, com as bandeiras e a proveniencia no modulo dela; a composicao e a estrela sao lidas deste kernel",
                "o registro falsidade_da_inercia_v401 selou neste rito, e o quadro do topo (teste_de_veracidade_fase9_v397) e o selo pela propria tecnologia (v399) seguem selados",
                "a errata ao lado da leitura do escriba no adendo de 03-04/09 esta registrada (a copia duravel do adendo esta pinada por sha256); as ratificacoes do operador estao registradas com a fala dele"],
        "nao_diz": ["que o kernel prove a definicao do operador (ela e' INPUT/ONTO)", "que a pedra prove Newton ou E = mc^2", "que o testemunho ou a ratificacao seja creditacao: validade no kernel nao e' creditacao", "que a gravidade quantica esteja creditada na natureza",
                    "que isto seja um teste: nao ha desfecho experimental novo"],
        "leituras_do_operador": [_leitura(DL.FRASE_RATIFICO, S_RATIF, rotulo="INPUT do operador"), _leitura(DL.FRASE_EMC2, S_RATIF), _leitura(DL.FRASE_NADA, S_NADA), _leitura(DL.FRASE_MATERIA, S_MATERIA),
                                 _leitura(DL.FRASE_INERCIA_NEWTON, S_INERCIA), _leitura(DL.FRASE_INERCIA, S_INERCIA, rotulo="DEFINICAO DO OPERADOR / INPUT"), _leitura(DL.FRASE_NOME, S_NOME, rotulo="INPUT do operador (o nome da pedra)"),
                                 _leitura(DL.FRASE_DERIVADO, S_IMPRESSAO, rotulo="INPUT do operador (a ordem: derivado, nao ONTO)"), _leitura(DL.FRASE_IMPRESSAO, S_IMPRESSAO, rotulo="INPUT do operador (o enunciado a derivar)"), _leitura(DL.FRASE_PRIMEIRO_MOVIMENTO, S_IMPRESSAO), _leitura(DL.FRASE_ZERO_PODA, S_IMPRESSAO)],
        "extras": {"assinatura": ASSINA, "autoria_das_cunhagens": "Luiz Antonio Rotoli Miguel", "pedras": [FAL["mod"]], "teoremas": {FAL["key"]: FAL["theorem"]}, "estrela": FAL["key_theorem"], "bandeiras": {FAL["key"]: fj["bandeira_do_teorema_incondicional"][FAL["key"]]},
                   "n_bandeiras": fj["n_flags"], "n_bandeiras_por_pedra": dict(fj["nomeadas_por_pedra"]), "cunhagens_embutidas": len(VERBATINS), "autor_de_cada_inscricao": dict(zip((v["sha16"] for v in _VD), (v["autor"] for v in _VD))),
                   "ratificacoes": ratificacoes(), "ratificacao_fala": {"sha16": S_RATIF, "trecho": DL.FRASE_RATIFICO}, "definicao_da_inercia": {"fala_sha16": S_INERCIA, "trecho": DL.FRASE_INERCIA, "kernel": "TGLExt.costless (0_abs: nunca correspondeu, e por isso nada custa)", "uns": "inercia 1=0; w(I)=1 posto 1=1"},
                   "adendo": {"sha16": ADENDO_SHA16, "erratado_por": ASSINA},
                   "cadeia_derivada": {"estatuto": "[DERIVED]", "base": "axioma w(I)=1 e lei de escala de Takesaki [KNOWN] como campo da estrutura", "ordem_do_operador_sha16": S_IMPRESSAO, "teoremas": ["no_post_before_the_impression", "inertia_is_not_its_own_cause", "the_first_motion_is_the_impression", "diagFlow_coordinate_is_the_scaling", "leak_below_every_epsilon", "the_zero_is_the_consequence_of_the_pruning", "the_tension_is_projected_onto_the_attractor", "falsidade_da_inercia_derivada"]},
                   "hipotese_nomeada": {"nome": "H_tau", "estatuto": "[OPEN]", "conteudo": "tau e' a massa de Newton e a metrica de Einstein", "usada_por_teorema": False, "pendencia_externa": "ORDEM 025 ao Codex, sha16 3fd2b5a801071343, enfileirada: tenta tipa-la pela frente de luz de Bisognano-Wichmann"}, "nome_da_pedra": "FalsidadeDaInercia («falsidade (simulacro) da inercia»; DADO pelo operador)", "decisoes_da_gerencia": dict(DL.DECISOES)},
    }
    kh = {
        "nome": "kh_n1_cobertura_v401", "veredito_prefixo": "TGL_KH_N1_COBERTURA_V401",
        "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__THE_FALSIDADE_DA_INERCIA_MODULE_ADDED__GATE_UNMOVED" % (T["decl"], T["thm"]),
        "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do sandbox da v401; o conjunto exato das fontes formais que o hash formal do rito vera (as embutidas mais os residuais da pasta do Nos) e' pinado; a cobertura NAO move o gate",
        "fontes": ["kh_n1_v401"], "kernel_flags": [], "kernel_decls": [],
        "checks": [
            CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
            CH("h2", "constantes cobertas == as do sandbox v401 (KH_N1)", "kf", ["axiom_coverage_v392", "decl"], "igual", T["decl"], "constantes_cobertas"),
            CH("h3", "teoremas cobertos == os do sandbox v401 (KH_N1)", "kf", ["axiom_coverage_v392", "thm"], "igual", T["thm"], "teoremas_cobertos"),
            CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
            CH("h5", "nenhum nome que o leitor v394 nao leia", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0),
            CH("h6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", khj["axiom_report_efetivo_n"]),
            CH("h7", "a cobertura da v401 inclui a da v400 selada (constantes e teoremas)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", cov_base["decl"]),
            CH("h7b", "os teoremas cobertos incluem os da v400 selada", "kf", ["axiom_coverage_v392", "thm"], "maior_igual", cov_base["thm"]),
            CH("h8", "as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta, como _check_damming.lean) sao EXATAMENTE as do pino (arquivo -> sha256)", "kf", ["formal_files_sha256"], "igual", h8_map),
            CH("h9", "medida do Audit v401: duracao bem abaixo do timeout de 1800 s", "fonte:kh_n1_v401", ["duracao_audit_s"], "menor_igual", 900, "duracao_do_audit_s"),
            CH("h10", "medida do Audit v401: sorryAx ausente do log", "fonte:kh_n1_v401", ["sorryAx_no_log_do_audit"], "igual", 0),
            CH("h11", "medida do Audit v401: as entradas novas estao no trio", "fonte:kh_n1_v401", ["novas_no_trio"], "verdadeiro"),
            CH("h12", "a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
        ],
        "erratas": [{"ao_lado_de": "kh_n1_cobertura_v399 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                     "dizia": "A v399 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v399 e o hash formal igual ao pino exato da arvore da v399." % (cov_base["decl"], cov_base["thm"]),
                     "agora": "A v401 acrescenta o modulo FalsidadeDaInercia (a cobertura cresce e a arvore ganha o arquivo da pedra): na v401 o registro da v399 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato da arvore ficam NESTE registro. O veredito do registro da v399 NAO muda.",
                     "lacuna_de_fidelidade": "a estrutura da v399 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v401 quebra (a mesma lacuna que a v399 achou no registro da v398, a v398 no da v397 e a v397 no da v396)",
                     "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; h2, h3, h6 e h8 conferidas no ensaio a seco e na arvore simulada do Nos]", "assinatura": ASSINA}],
        "limites": ["[REAL] os arquivos de medida sao do sandbox (fora do selo); a cobertura que vale e' a medida no Audit do proprio rito",
                    "[REAL] a escada do kernel conta bandeiras de declaracoes NOMEADAS (a pratica da v392 a v399): as %d auxiliares geradas pelo compilador no modulo da pedra ficam cobertas pelo KH-N1 mas sem bandeira, e as %d nomeadas publicas ganharam bandeira" % (fj["excluidas_auxiliares"]["n"], fj["n_flags"]),
                    "validade no kernel nao e' creditacao; o gate nao se move"],
        "diz": ["a cobertura do axiom_report no fecho inteiro cresceu para os numeros da v401 (o modulo FalsidadeDaInercia) e segue sem constante fora do trio, sem nome ilegivel"],
        "nao_diz": ["que a cobertura prove algo alem de que nenhum axioma fora do trio foi lido"],
        "leituras_do_operador": [], "extras": {"assinatura": ASSINA, "n_bandeiras": fj["n_flags"], "h8_entradas": len(h8_map), "h8_residuais_do_nos": sorted(set(h8_map) - set(formal_map))},
    }
    return [cun, kh]
