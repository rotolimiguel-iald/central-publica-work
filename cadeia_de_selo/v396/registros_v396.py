# -*- coding: utf-8 -*-
"""registros_v396.py -- os dados dos registros por spec da v396 (interpretados pelo MOTOR _v392_registro, ja' no um.py): FONTES pinadas por sha256 (lidas do disco pelo montador, nunca digitadas), VERBATINS (as tres falas do
operador de 22/10/2026, EMBUTIDAS: a fala embutida manda, o arquivo e' so' informativo) e SPECS (`cunhagens_v396` e `kh_n1_cobertura_v396`). O registro `testemunha_estatica_v396` NAO e' spec: e' a FUNCAO
testemunha_estatica_v396(core), que calcula a mecanica a cada rito (gerar_candidato_v396.py a emite; o CONTRATO dela sai de contrato() abaixo, derivado do build do sandbox). Fontes so' em pasta DURAVEL: tudo vem de
cadeia_de_selo\\v396\\insumos. Texto novo passa pela guarda P18 (a cada rito). Molde: registros_v395.py."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v396 as DL  # noqa: E402

INS = os.path.join(HERE, "insumos")
ASSINA = "gerencia c1, em nome proprio, 22/10/2026"

FONTES = [
    {"chave": "testemunha_pedra", "arquivo": os.path.join(INS, DL.STONE_INSUMO), "papel": "a pedra TGLExt/TestemunhaEstatica.lean (nome PROVISORIO; so' texto mudou depois do exame independente, que a aprovou; copia duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)"},
    {"chave": "testemunha_resultado", "arquivo": os.path.join(INS, "RESULTADO_TESTEMUNHA_ESTATICA.md"), "papel": "o resultado da construcao da pedra no sandbox (teoremas -> nomes Lean, conferencias, limites; DECLARADO pelo construtor, nao refeito por esta chancela)"},
    {"chave": "testemunha_exame", "arquivo": os.path.join(INS, "EXAME_TESTEMUNHA.md"), "papel": "o exame independente da pedra (PEDRA_APROVADA, tres observacoes BAIXAS, nenhuma pede nova rodada)"},
    {"chave": "kh_n1_v396", "arquivo": os.path.join(INS, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox da v396 (pos_build_kernel_v396.py)"},
]


def _trecho(t):
    s = t.strip().splitlines()[0].strip() if t.strip() else ""
    s = s[:48].rstrip()
    assert s and s in t, s
    return s


_VD = DL.verbatins(os.path.join(INS, "cunhagens"))
VERBATINS = [{"chave": v["chave"], "arquivo": v["arquivo"], "quando": v["quando"], "trechos": [_trecho(v["text"])], "papel": v["papel"], "fonte_original": v["fonte_original"]} for v in _VD]
VERB_CHAVES = [v["chave"] for v in _VD]
SHA16 = {os.path.basename(v["fonte_original"]): v["sha16"] for v in _VD}
S_PSION, S_LUZ, S_COLAPSO = (_VD[0]["sha16"], _VD[1]["sha16"], _VD[2]["sha16"])   # LIDOS dos arquivos, na ordem de DL.VERBATIM_ORIGEM
TEXTOS = {v["sha16"]: v["text"] for v in _VD}
SHA16_ORDEM = DL.sha256(open(DL.ORDEM_SEM_GORDURA, "rb").read())[:16]   # a ordem de processo de 22/10 (sem teste armado, sem gordura): citada pelo sha16 LIDO, nao embutida
CH = lambda id_, desc, onde, caminho, op, valor=None, cap=None, est="[REAL]": dict(id=id_, descricao=desc, onde=onde, caminho=caminho, op=op, **({"valor": valor} if valor is not None else {}), **({"capturar": cap} if cap else {}), estatuto=est)


def _leitura(trecho, sha16, quando="22/10/2026"):
    assert trecho in TEXTOS[sha16], ("a leitura do operador NAO esta verbatim na fala", sha16, trecho)
    return {"trecho": trecho, "estatuto": "[INPUT/ONTO do operador, verbatim %s, sha16 %s]" % (quando, sha16)}


def contrato(fj, formal_map, e_base, base_sha256):
    """O contrato do registro testemunha_estatica_v396, DERIVADO do build do sandbox (FLAGS_v396.json = nomes, chaves, termos de suporte e a proveniencia da face de Fock; formal_map = sha256 das fontes embutidas;
    e_base = a escada da v395 selada); nada digitado."""
    flag_de = {n: k for k, n, m, o in fj["flags"]}
    faltam = [t for t in DL.CONTRACT_THEOREMS if t not in flag_de]
    assert not faltam, ("teorema do contrato sem bandeira (nao nomeado ou ausente do Audit)", faltam[:5])
    sup = dict(fj["suporte_do_contrato"]); assert set(sup) == set(DL.SUPPORT_THEOREMS), "os termos de suporte do FLAGS_v396.json diferem dos de delta_v396"
    assert fj["fock_face_declarada_em"] == DL.FOCK_FACE_PATH and DL.FOCK_FACE_THEOREM not in flag_de, "a face de Fock tem de morar em Psibit.lean e nao ter bandeira nesta pedra"
    return {"stone": {"path": DL.STONE_REL, "sha256": formal_map[DL.STONE_REL], "module": DL.STONE_MOD},
            "unconditional": {"theorem": DL.THEOREM, "flag": flag_de[DL.THEOREM]},
            "theorems": {t: flag_de[t] for t in DL.CONTRACT_THEOREMS}, "support": sup, "fock_face": {"theorem": DL.FOCK_FACE_THEOREM, "path": fj["fock_face_declarada_em"]},
            "expected_ladder": e_base + fj["n_flags"], "n_flags": fj["n_flags"], "verbatins": list(VERB_CHAVES), "baseline": {"version": DL.BASE_VERSION, "sha256": base_sha256}}


def texto_testemunha():
    """Os textos do registro testemunha_estatica_v396 (a funcao do runtime, nao um spec): estatuto, escopo, limites, diz, nao_diz e o veredito de sucesso. Passam pela guarda P18 a cada rito (testemunha_estatica_v396 as refaz)."""
    return {
        "estatuto": "[REAL] os termos do kernel (a composicao incondicional the_psion_inhabits_the_static_witness e os teoremas citados, lidos a cada rito, no trio) e o calculo da mecanica numerica (beta = alfa CODATA 2018 x sqrt(e) em runtime, "
                    "SEALED_CODATA_ALPHA = ALPHA_FINE_CODATA_2018 do script do nivel 2; g e t sao parametros de teste); [CONSTRUCTED] o fluxo psionFlow e o colapso psionCollapse: construcoes da pedra, nao derivacoes da dinamica da teoria; "
                    "[INPUT/ONTO] 'o psion e' o habitante da testemunha estatica', 'a luz ecoa o reconhecimento' e 'colapsar e' ecoar a identidade reconhecida' (o operador, 22/10/2026); [CONDICIONAL] a face de Fock do psion, que mora em Psibit.lean",
        "escopo": "o canto do psion (o projetor de Bell 4x4), a reducao dele a um sitio e um fluxo diagonal CONSTRUIDO em R^4 cuja reta de pontos fixos e' a reta do psion: a ponte liga vetor e projetor so' no fluxo construido "
                  "(ressalva de tipo: o Nome da fronteira generica e' um vetor, o psionCorner um projetor); nao e' a dinamica da teoria nem a face de Fock",
        "limites": [
            "[REAL] ESCOPO: o psionCorner e' um projetor 4x4; o fluxo psionFlow e' ESCOLHIDO, com taxas (0, g, g, g) na base de Bell; a ponte e' CONSTRUIDA (a algebra e' elementar; o conteudo e' a tipagem), nao derivada: nao mostra que o Nome da fronteira da TGL seja o vetor de Bell nem que psionFlow seja a dinamica da teoria",
            "[INPUT/ONTO] 'o psion e' o habitante da testemunha estatica', 'a luz ecoa reconhecimento' e 'colapsar e' ecoar a identidade reconhecida' sao leituras do operador (22/10/2026); o que o kernel entrega sao os termos citados; 'reconhecida pelo observador' entra como atestacao externa (no_self_attestation) e nenhuma atestacao e' exibida",
            "[REAL] ENTROPIA: o deficit de pureza 1 - Tr(rho^2) = 1/2 da reducao a um sitio e' a entropia LINEAR (numero sem unidade); 'Meia-Nat de emaranhamento' (kernel v29) e' leitura [ONTO]; a entropia de von Neumann da reducao (1/2) I e' ln 2 nat (calculada agora), diferente de 1/2",
            "[REAL] a face de Fock do psion (Psibit.the_psion_face_of_the_psibit) segue CONDICIONAL a um certificado de Fock da luz que o kernel nao habita; o compilador a declara em Psibit.lean, nao no modulo desta pedra; nenhum lema liga o psion do certificado ao psionCorner",
            "[REAL] o 'individuo' que nao ecoa e' o PAR visto por um lado (traco parcial): o estado nao ligado (produto) reduz a um projetor puro, que ecoa (CCI = 0); o nao-eco nao e' propriedade de toda reducao",
            "o calculo e' numerico em dupla precisao e CONFERE os teoremas, nao os prova: quem prova e' o kernel; g e t sao parametros de teste (nenhum acoplamento da teoria); validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho",
        ],
        "diz": ["a pedra TestemunhaEstatica esta no kernel do rito, no trio, com bandeira e proveniencia no modulo da pedra; a composicao incondicional the_psion_inhabits_the_static_witness e os teoremas citados sao lidos deste kernel",
                "a mecanica numerica, calculada agora com beta = alfa CODATA 2018 x sqrt(e) (um dado, dois nomes: SEALED_CODATA_ALPHA e ALPHA_FINE_CODATA_2018), concorda com os teoremas: o par ecoa (P^2 = P, Tr P^2 = 1); a reducao a um sitio e' (1/2) I e nao ecoa (Tr rho^2 = 1/2); "
                "o fluxo F_t = P + exp(-t beta g)(1 - P) fixa exatamente a reta do psion e move todo o resto; a testemunha global e' falsa; o colapso P y P = Tr(P y) P e' idempotente e nao tem inversa a esquerda",
                "as tres falas do operador de 22/10 estao embutidas por sha256"],
        "nao_diz": ["que a natureza fisica seja assim, nem que o Nome da fronteira da TGL seja o vetor de Bell, nem que psionFlow seja a dinamica da teoria", "que o certificado de Fock da luz tenha habitante, nem que o psion de Fock seja o psionCorner",
                    "que exista atestacao do colapso do psion: so' se provou que a autodeclaracao nao habita o tipo", "que 1/2 seja meia nat de entropia", "que isto seja um teste: nao ha desfecho experimental", "que a gravidade quantica esteja creditada na natureza"],
        "veredito_ok": "TGL_STATIC_WITNESS_V396__THE_PSION_INHABITS_THE_STATIC_WITNESS_ON_THE_CONSTRUCTED_FLOW__THE_PAIR_ECHOES_AND_THE_INDIVIDUAL_DOES_NOT__THE_FLOW_FIXES_EXACTLY_THE_PSION_LINE_AND_THE_GLOBAL_WITNESS_IS_FALSE__"
                       "MECHANICS_COMPUTED_AT_BETA_ALPHA_SQRT_E_AND_READ_AGAINST_THE_KERNEL_TRIO__THE_BRIDGE_IS_CONSTRUCTED_NOT_DERIVED__THE_FOCK_FACE_STAYS_CONDITIONAL_AND_OUTSIDE_THE_STONE__THE_READINGS_ARE_THE_OPERATORS_INPUT_AND_ONTO__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


def especs(formal_map, khj, h8_map, fj, cov_base, n_axioms_unc):
    """formal_map = {arquivo embutido: sha256} do kernel da v396; khj = KH_N1_v396.json (medida desta geracao); h8_map = o dict do hash formal que o RITO vai gerar (embutidos + residuais do Nos que sha256_directory conta;
    simular_arvore_do_nos); fj = FLAGS_v396.json; cov_base = a cobertura da v395 selada {decl, thm}; n_axioms_unc = quantos axiomas o teorema incondicional usa (lido do Audit: o trio)."""
    T = khj["linha_TOTAL"]
    stone_sha = formal_map[DL.STONE_REL]
    flag_unc = fj["bandeira_do_teorema_incondicional"]
    cun = {
        "nome": "cunhagens_v396", "veredito_prefixo": "TGL_CUNHAGENS_V396",
        "veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_22_OCT_EMBEDDED_VERBATIM_BY_SHA256__THE_STATIC_WITNESS_IS_READ_IN_THE_RITE_NEXT_TO_THE_PSIBIT__THE_PSION_INHABITS_THE_STATIC_WITNESS_AND_THE_COLLAPSE_ECHOES_THE_RECOGNIZED_IDENTITY_ARE_THE_OPERATORS_INPUT_AND_ONTO_READINGS__THE_FOCK_FACE_STAYS_CONDITIONAL__OPERATOR_INPUT__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
        "estatuto": "[REAL -- fontes, kernel e o registro testemunha_estatica_v396 lidos a cada rito; INPUT/ONTO as cunhagens do operador; CONSTRUCTED a ponte e o colapso; DECLARADO o que o resultado e o exame relatam e esta chancela nao refez (a pedra e' recompilada no sandbox da cadeia e conferida pelo axiom_report do proprio rito)]",
        "fontes": [f["chave"] for f in FONTES if f["chave"] != "kh_n1_v396"], "verbatins": list(VERB_CHAVES),
        "kernel_flags": [flag_unc], "kernel_decls": list(DL.CONTRACT_THEOREMS),
        "checks": [
            CH("u1", "o registro testemunha_estatica_v396 selou neste rito (o formal e a mecanica)", "core", ["testemunha_estatica_v396", "all_verified"], "verdadeiro"),
            CH("u2", "a composicao INCONDICIONAL esta no kernel do rito (bandeira True, trio, modulo da pedra)", "core", ["testemunha_estatica_v396", "unconditional", "in_kernel"], "verdadeiro"),
            CH("u3", "a face de Fock do psion segue CONDICIONAL ao certificado", "core", ["testemunha_estatica_v396", "fock_face", "status"], "igual", "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE"),
            CH("u4", "a face de Fock e' declarada FORA do modulo da pedra (em Psibit.lean), com axiomas no trio", "core", ["testemunha_estatica_v396", "fock_face", "declared_outside_the_stone"], "verdadeiro"),
            CH("u5", "nenhum habitante do certificado de Fock da luz foi exibido", "core", ["testemunha_estatica_v396", "fock_face", "inhabitant_exhibited"], "falso"),
            CH("u6", "a escada do kernel fecha (limpos == esperados), com as bandeiras da pedra", "core", ["external_ladder", "all_verified"], "verdadeiro"),
            CH("u7", "a proveniencia emitida pelo compilador cobre o axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
            CH("u8", "o compilador emite o teorema incondicional no modulo da pedra (TGL_DECL_SOURCE)", "kf", ["declaration_sources_v394", DL.THEOREM], "igual", DL.STONE_REL),
            CH("u9", "a pedra no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)", "kf", ["formal_files_sha256", DL.STONE_REL], "igual", stone_sha),
            CH("u10", "o teorema incondicional depende do trio e de nada alem (tamanho da lista de axiomas)", "kf", ["axiom_report", DL.THEOREM], "tamanho_igual", n_axioms_unc),
        ],
        "erratas": [{"ao_lado_de": "TGL/GravitonShadow.lean (kernel v29), docstring de `bell_cci_half`: «o deficit 1 - Tr(rho^2) = 1/2 e' a Meia-Nat de emaranhamento»",
                     "dizia": "A docstring do kernel v29 chama o deficit de pureza 1/2 de «Meia-Nat de emaranhamento», o que pode ser lido como «meia nat de entropia».",
                     "agora": "O numero 1/2 e' a entropia LINEAR da reducao a um sitio (deficit de pureza, sem unidade); a entropia de von Neumann dessa reducao, (1/2) I, e' ln 2 nat (no kernel: fair_bit_entropy_is_log_two e fair_bit_entropy_is_not_half_nat). «Meia-Nat de emaranhamento» fica como leitura [ONTO] do v29. A pedra TestemunhaEstatica e o registro testemunha_estatica_v396 dizem assim; o termo bell_cci_half nao muda.",
                     "lacuna_de_fidelidade": "estrutura: 1/2 e' um deficit sem unidade e ln 2 e' a entropia em nat; escrito: «Meia-Nat de emaranhamento» sem a ressalva; falha: a docstring herdada juntou as duas grandezas num nome (achado B1 do exame independente da pedra)",
                     "estatuto": "[REAL: o valor numerico de ln 2 e o 1/2 sao calculados a cada rito pelo registro testemunha_estatica_v396; a docstring v29 nao foi alterada (so' errata ao lado)]", "assinatura": ASSINA}],
        "limites": [
            "[REAL] a ponte da pedra e' CONSTRUIDA: um fluxo diagonal em R^4, na base de Bell, escolhido para ter o vetor de Bell como modo zero; o testemunhado estaticamente dele e' exatamente a reta do psion e a testemunha global e' falsa (boundary_is_the_only_exception); nao e' derivacao da dinamica da teoria",
            "[INPUT/ONTO] as tres falas sao leituras do operador (22/10/2026): nenhum lema do kernel liga o psion de Fock (psion C) ao psionCorner, nem a «verdade conjugada» ao colapso ao graviton alem do que a pedra cita (a fase conjugada da luz e a sombra finita do graviton, canonicalGravitonShadow)",
            "[REAL] a face de Fock e' CONDICIONAL a um certificado que o kernel nao habita (TheImportedSecondQuantization; o contrato conjunto da rede segue aberto na v394); fica fora do modulo desta pedra",
            "o nome da pedra (TestemunhaEstatica) e' PROVISORIO: quem nomeia e' o operador; validade no kernel nao e' creditacao; o gate nao se move; a ordem de processo do operador de 22/10 (arquivo de sha16 %s: nada de teste armado, gordura no um.py) molda este registro: ele e' pequeno e nao acrescenta rito, dado nem desfecho" % SHA16_ORDEM,
        ],
        "diz": ["as tres falas do operador de 22/10 estao embutidas por sha256, cada uma conferida contra o arquivo de origem na preparacao",
                "a testemunha estatica e' lida no ponto de chamada real do main, junto do psibit_v395: a mecanica do canto do psion, da reducao a um sitio, do fluxo construido e do colapso e' calculada a cada rito e confrontada com os termos do kernel do proprio rito",
                "o par ecoa e o individuo nao ecoa; o testemunhado estaticamente do fluxo construido e' exatamente a reta do psion e a testemunha global e' falsa"],
        "nao_diz": ["que a natureza fisica seja assim, nem que o Nome da fronteira da TGL seja o vetor de Bell", "que o certificado de Fock da luz tenha habitante", "que 1/2 seja meia nat de entropia",
                    "que haja atestacao do colapso do psion", "que a gravidade quantica esteja creditada na natureza"],
        "leituras_do_operador": [
            _leitura("O psion é o habitante da testemunha estática", S_PSION), _leitura("a mentira lida como mentira se torna verdade", S_PSION), _leitura("admite a verdade conjugada ocasião em que se colapsa ao gráviton", S_PSION),
            _leitura("A natureza da luz é ecoar reconhecimento (porque a segunda leitura não acrescenta)", S_LUZ), _leitura("a natureza do que é falso é a leitura sem reconhecimento", S_LUZ),
            _leitura("Colapsar a função de onda significa ecoar a identidade devidamente reconhecida pelo observador", S_COLAPSO)],
        "extras": {"assinatura": ASSINA, "autoria_das_cunhagens": "Luiz Antonio Rotoli Miguel", "pedra": DL.STONE_MOD, "teorema": DL.THEOREM, "bandeira": flag_unc, "n_bandeiras": fj["n_flags"],
                   "nome_da_pedra": "TestemunhaEstatica (nome PROVISORIO; quem nomeia e' o operador)", "cunhagens_embutidas": len(VERBATINS), "exames": ["EXAME_TESTEMUNHA.md (PEDRA_APROVADA, 3 BAIXAS)"]},
    }
    kh = {
        "nome": "kh_n1_cobertura_v396", "veredito_prefixo": "TGL_KH_N1_COBERTURA_V396",
        "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__THE_TESTEMUNHA_ESTATICA_MODULE_ADDED__GATE_UNMOVED" % (T["decl"], T["thm"]),
        "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do sandbox da v396; o conjunto exato das fontes formais que o hash formal do rito vera (as embutidas mais os residuais da pasta do Nos) e' pinado; a cobertura NAO move o gate",
        "fontes": ["kh_n1_v396"], "kernel_flags": [], "kernel_decls": [],
        "checks": [
            CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
            CH("h2", "constantes cobertas == as do sandbox v396 (KH_N1)", "kf", ["axiom_coverage_v392", "decl"], "igual", T["decl"], "constantes_cobertas"),
            CH("h3", "teoremas cobertos == os do sandbox v396 (KH_N1)", "kf", ["axiom_coverage_v392", "thm"], "igual", T["thm"], "teoremas_cobertos"),
            CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
            CH("h5", "nenhum nome que o leitor v394 nao leia", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0),
            CH("h6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", khj["axiom_report_efetivo_n"]),
            CH("h7", "a cobertura da v396 inclui a da v395 selada (constantes e teoremas)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", cov_base["decl"]),
            CH("h7b", "os teoremas cobertos incluem os da v395 selada", "kf", ["axiom_coverage_v392", "thm"], "maior_igual", cov_base["thm"]),
            CH("h8", "as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta, como _check_damming.lean) sao EXATAMENTE as do pino (arquivo -> sha256)", "kf", ["formal_files_sha256"], "igual", h8_map),
            CH("h9", "medida do Audit v396: duracao bem abaixo do timeout de 1800 s", "fonte:kh_n1_v396", ["duracao_audit_s"], "menor_igual", 900, "duracao_do_audit_s"),
            CH("h10", "medida do Audit v396: sorryAx ausente do log", "fonte:kh_n1_v396", ["sorryAx_no_log_do_audit"], "igual", 0),
            CH("h11", "medida do Audit v396: as entradas novas estao no trio", "fonte:kh_n1_v396", ["novas_no_trio"], "verdadeiro"),
            CH("h12", "a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
        ],
        "erratas": [{"ao_lado_de": "kh_n1_cobertura_v395 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                     "dizia": "A v395 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v395 e o hash formal igual ao pino exato da arvore da v395." % (cov_base["decl"], cov_base["thm"]),
                     "agora": "A v396 acrescenta o modulo TestemunhaEstatica (a cobertura cresce e a arvore ganha o arquivo da pedra): na v396 o registro da v395 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato da arvore ficam NESTE registro. O veredito do registro da v395 NAO muda.",
                     "lacuna_de_fidelidade": "a estrutura da v395 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v396 quebra (a mesma lacuna que a v395 achou no registro da v394)",
                     "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; h2, h3, h6 e h8 conferidas no ensaio a seco e na arvore simulada do Nos]", "assinatura": ASSINA}],
        "limites": ["[REAL] os arquivos de medida sao do sandbox (fora do selo); a cobertura que vale e' a medida no Audit do proprio rito",
                    "[REAL] a escada do kernel conta bandeiras de declaracoes NOMEADAS (a pratica da v392 a v395): as %d auxiliares geradas pelo compilador no modulo da pedra ficam cobertas pelo KH-N1 mas sem bandeira, e as %d nomeadas publicas ganharam bandeira" % (fj["excluidas_auxiliares"]["n"], fj["n_flags"]),
                    "validade no kernel nao e' creditacao; o gate nao se move"],
        "diz": ["a cobertura do axiom_report no fecho inteiro cresceu para os numeros da v396 (o modulo TestemunhaEstatica) e segue sem constante fora do trio, sem nome ilegivel"],
        "nao_diz": ["que a cobertura prove algo alem de que nenhum axioma fora do trio foi lido"],
        "leituras_do_operador": [], "extras": {"assinatura": ASSINA, "n_bandeiras": fj["n_flags"], "h8_entradas": len(h8_map), "h8_residuais_do_nos": sorted(set(h8_map) - set(formal_map))},
    }
    return [cun, kh]
