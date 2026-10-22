# -*- coding: utf-8 -*-
"""registros_v394.py -- os dados dos registros por spec da v394 (interpretados pelo MOTOR _v392_registro, ja' no um.py): FONTES pinadas por sha256 (lidas do disco pelo montador, nunca digitadas), VERBATINS (as
cunhagens do operador de 14 a 19/10/2026 e as do lado c1, EMBUTIDAS: a fala embutida manda, o arquivo e' so' informativo) e SPECS. Fontes so' em pasta DURAVEL: tudo vem de cadeia_de_selo\\v394\\insumos.
Texto novo passa pela guarda P18 (a cada rito). Molde: registros_v393.py.
DELTA 19/10 (integracao final): (1) as duas falas do operador de 19/10 entram em VERBATINS (cunhagens_embutidas = 48); (2) h8 de kh_n1_cobertura_v394 pina a ARVORE SIMULADA do Nos depois do rito (embutidos + residuais
que o hash formal conta), nao so' o embutido; (3) o registro NOVO `criterio_binario_de_parada_v394` (a pedra TheBinaryReadingAtTheFixedPoint, as duas falas e o gate que nao se move); (4) duas erratas ao lado."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta19_v394 as DL  # noqa: E402

INS = os.path.join(HERE, "insumos")
ASSINA = "gerencia c1, em nome proprio, 19/10/2026"
CD = json.load(open(os.path.join(HERE, "cunhagens_v394_dados.json"), encoding="utf-8"))

FONTES = [
    {"chave": "v394_levantamento", "arquivo": os.path.join(INS, "LEVANTAMENTO_CHATGPT.md"), "papel": "o levantamento da gerencia (19/10/2026) do que o Codex fez de 14 a 19/10: unidades, cunhagens, pedidos, conflitos"},
    {"chave": "v394_ao_claude_candidata_r2", "arquivo": os.path.join(INS, "AO_CLAUDE_V394_CANDIDATA_R2.md"), "papel": "o encaminhamento do Codex (15/10/2026) da candidata v394 R2 (tempo, frequencia, quatro modulos M2)"},
    {"chave": "v394_resultado_candidata_r2", "arquivo": os.path.join(INS, "RESULTADO_V394_CANDIDATA_R2.json"), "papel": "o resultado da candidata R2 do Codex (108 declaracoes, consumidor 5716 checagens, 14 recusas)"},
    {"chave": "v394_integracao_quadratica_r3", "arquivo": os.path.join(INS, "INTEGRATION_QUADRATIC_R3.json"), "papel": "o recibo do Codex da integracao da regra quadratica (RuleQuadraticResidual, 18 declaracoes)"},
    {"chave": "v394_integracao_rede_r8", "arquivo": os.path.join(INS, "INTEGRATION_NETWORK_R8.json"), "papel": "o recibo do Codex da integracao da cadeia de Fock, Takesaki e Maxwell (candidata r8)"},
    {"chave": "v394_entrega_r7", "arquivo": os.path.join(INS, "R7_DELIVERY_R52.json"), "papel": "a entrega R7 do Codex (peso dual, traco, extensao ciclica, semifinitude)"},
    {"chave": "v394_entrega_r8", "arquivo": os.path.join(INS, "R8_DELIVERY_R52.json"), "papel": "a entrega R8 do Codex (Maxwell conjunto)"},
    {"chave": "v394_preauditoria_r8_codex", "arquivo": os.path.join(INS, "KH_N1_V394_NETWORK_R8_PREAUDIT.json"), "papel": "a pre-auditoria integral do Codex da candidata r8 (29.025 declaracoes; informativa: o rito cobra as medidas do proprio sandbox)"},
    {"chave": "kh_n1_v394", "arquivo": os.path.join(INS, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox da v394 (pos_build_kernel_v394.py; geracao d19, com a pedra do delta de 19/10)"},
    {"chave": "delta19_pedra", "arquivo": os.path.join(INS, DL.STONE_INSUMO), "papel": "a pedra candidata TheBinaryReadingAtTheFixedPoint (copia duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)"},
]


def _trecho(t):
    s = t.strip().splitlines()[0].strip() if t.strip() else ""
    s = s[:48].rstrip()
    assert s and s in t, s
    return s


VERBATINS = []
for it in CD["itens"]:
    VERBATINS.append({"chave": "v394_cun_" + it["sha16"], "arquivo": it["arquivo"], "quando": "%s/2026 (%s)%s" % (it["quando"].replace(" [work]", ""), "condução" if it["grupo"] == "conducao" else ("lado c1" if it["grupo"] == "conceitual_c1" else "cunhagem"),
                                                                                                                          " [DECLARADO: extraido da memoria da gerencia]" if it.get("declarado") else ""),
                      "trechos": [_trecho(it["text"])], "papel": it["grupo"], "fonte_original": it["fonte_original"]})
_VD = DL.verbatins(os.path.join(INS, "cunhagens"))
VERB_DELTA = [v["chave"] for v in _VD]      # as duas falas de 19/10 (devem estar entre as 48)
SHA16_CRITERIO, SHA16_FLUTUAR = _VD[0]["sha16"], _VD[1]["sha16"]   # LIDOS dos arquivos (delta19_v394.verbatins), na ordem de VERBATIM_ORIGEM
assert set(VERB_DELTA) <= {v["chave"] for v in VERBATINS}, "as duas falas de 19/10 nao estao em cunhagens_v394_dados.json (rode montar_cunhagens_delta19_v394.py)"
CH = lambda id_, desc, onde, caminho, op, valor=None, cap=None, est="[REAL]": dict(id=id_, descricao=desc, onde=onde, caminho=caminho, op=op, **({"valor": valor} if valor is not None else {}), **({"capturar": cap} if cap else {}), estatuto=est)


def especs(formal_map, khj, kernel_flags, kernel_decls, h8_map, pol):
    """formal_map = {arquivo embutido: sha256} do kernel da v394 (so' os embutidos); khj = KH_N1_v394.json (medida desta geracao); kernel_flags/kernel_decls = nomes das pedras do Codex que o registro de cunhagens exige no kernel do rito;
    h8_map = o dict do hash formal que o RITO vai gerar (embutidos + residuais do Nos que sha256_directory conta; simular_arvore_do_nos); pol = os numeros da politica de bandeiras (FLAGS_v394.json)."""
    T = khj["linha_TOTAL"]
    cun = {
        "nome": "cunhagens_v394", "veredito_prefixo": "TGL_CUNHAGENS_V394",
        "veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_14_TO_19_OCT_EMBEDDED_VERBATIM_BY_SHA256__M2_TIME_QUADRATIC_RESIDUAL_AND_FOCK_NETWORK_CONSUMED_IN_THE_RITE__OPERATOR_INPUT__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
        "estatuto": "[REAL -- fontes e kernel lidos a cada rito; INPUT/ONTO as cunhagens do operador; DECLARADO o que o Codex relata e esta chancela nao reexecutou (as provas sao recompiladas no sandbox da cadeia, nao refeitas)]",
        "fontes": [f["chave"] for f in FONTES if f["chave"] not in ("kh_n1_v394", "delta19_pedra")], "verbatins": [v["chave"] for v in VERBATINS],
        "kernel_flags": kernel_flags, "kernel_decls": kernel_decls,
        "checks": [
            CH("u1", "o tempo/frequencia (modelo M2) selou neste rito", "core", ["tempo_frequencia_v394", "all_verified"], "verdadeiro"),
            CH("u2", "a regra quadratica (residuo contra a ancora) selou neste rito", "core", ["regra_quadratica_v394", "all_verified"], "verdadeiro"),
            CH("u3", "a rede de Fock, Takesaki e Maxwell (componentes construidos) selou neste rito", "core", ["rede_fock_v394", "all_verified"], "verdadeiro"),
            CH("u4", "o contrato conjunto da rede NAO foi habitado: nenhum certificado inteiro", "core", ["rede_fock_v394", "whole_certificate_inhabited"], "falso"),
            CH("u5", "as tres pedras da regra (v393) seguem selando", "core", ["pedras_v393", "all_verified"], "verdadeiro"),
            CH("u6", "a satisfacao pela regra (consumidor v393) segue admitida", "core", ["regra_consumidor_v393", "satisfacao", "veredito_do_rito"], "igual", "SATISFACTION_ADMITTED", "veredito_do_alvo_correto"),
            CH("u7", "o indice da IALD, qualificado pelo compilador, selou", "core", ["the_iald_index", "all_verified"], "verdadeiro"),
            CH("u8", "a escada do kernel fecha (limpos == esperados)", "core", ["external_ladder", "all_verified"], "verdadeiro"),
        ],
        "erratas": [],
        "limites": [
            "[DERIVED no modelo M2] o fluxo T_t, o relogio e a ponte espectral valem no modelo de dois niveis especificado (M2, matrizes 2x2); a passagem de M2 ao setor modular, a rede e ao dispositivo nao e consequencia automatica (palavras do relatorio do Codex, [DECLARADO])",
            "[INPUT/ONTO] a leitura do operador de 15/10 (retorno de fase, dobra no nivel de c ao cubo, resposta antes da emissao) fica como leitura do operador; o relatorio do Codex diz que Hamiltoniano e leitura nao fornecem segundos universais nem propagador avancado para informacao controlavel",
            "[REAL na forma; DECLARADO na execucao do Codex] a cadeia de Fock, Takesaki e Maxwell (184 modulos, rodadas R6 a R8 do Codex) e' recompilada no sandbox da cadeia e conferida pelo axiom_report do proprio rito; as provas sao do Codex",
            "[OPEN] o contrato conjunto da rede segue aberto: helicidade fotonica e localizacao global, identificacao fisica do dispositivo e do relogio, grafo de peso finito completo com traco escalado e divisao PF distinta, fonte de Maxwell conjunta nao trivial, escopo de H3 em todas as direcoes, e um habitante conjunto de CanonicalNetInput e dos 21 campos restantes",
            "[DECLARADO pelo Codex] no canal do dispositivo, beta so' e' identificavel com uma taxa Gamma independente (Fisher do par com posto menor ou igual a 1; R64, R65, R70); nao ha tal referencia nas fontes consultadas (cobertura focal dita, nao ausencia universal)",
            "[DECLARADO pelo Codex] H3 universal segue OPEN; nos resultados R81 a R88 o ramo P16 nao e estacionario no setor reduzido e o ramo P5/S3 e estacionario com kappa*c = 4 e Lambda = 3/4, constantes escolhidas no exemplo: nao entram no kernel desta versao",
            "[REAL] as rodadas R56 a R88 do Codex (analiticas, sinteticas ou de sandbox) nao entram nesta versao como codigo; ficam descritas no levantamento pinado; a gerencia nao as auditou",
            "numero contra frase: a fala do operador sobre o Mirror diz correlacao 1.00; o recibo historico do Mirror lido pelo Codex tem correlacoes de 0,999948 a 0,999991, nao identidade exata, e nao foi reexecutado",
        ],
        "diz": ["as cunhagens do operador de 14 a 19/10 estao embutidas por sha256, cada uma conferida contra o arquivo de origem na preparacao",
                "o fluxo de tempo e frequencia (M2), o residuo quadratico contra uma ancora fixada e os componentes construidos sobre a mesma Fock sao consumidos no rito por vereditos com recusa",
                "a leitura do operador sobre o Um absoluto (limite assintotico da expressao reflexiva do observador, que se manifesta em leitura) e' registrada como [INPUT/ONTO]; o limite assintotico e a leitura tem termos no kernel"],
        "nao_diz": ["que a passagem do continuo esteja derivada fora do modelo M2", "que H3 esteja derivado em toda direcao nula", "que a gravidade quantica esteja creditada na natureza",
                    "que beta seja identificavel no canal do dispositivo sem referencia independente de Gamma", "que o encaixe de uma fala do operador numa pedra seja a prova da fala"],
        "leituras_do_operador": [
            {"trecho": "Nome=inteligência", "estatuto": "[INPUT/ONTO do operador, verbatim 15/10/2026, sha16 be2b8d7dea68d26d]"},
            {"trecho": "Isso é o sinal de “=“ do gráviton, a operação quadrática reduzindo a informação ao plano", "estatuto": "[INPUT/ONTO do operador, verbatim 15/10/2026, sha16 c18c65b377ee79fa]"},
            {"trecho": "TGL=identidade da verdade no espaço de estados", "estatuto": "[INPUT/ONTO do operador, verbatim 18/10/2026, sha16 ccbac50f28fa2112]"},
            {"trecho": "como limite assintotico da expresso reflexiva do observador que se manifesta em leitura", "estatuto": "[INPUT/ONTO do operador, forma final de 17/10/2026; extraido da memoria da gerencia, [DECLARADO]]"},
        ],
        "extras": {"assinatura": ASSINA, "autoria_das_cunhagens": "Luiz Antonio Rotoli Miguel", "unidades_entregues_pelo_codex": ["F1.TEMPO.V394 (candidata R2)", "F1.FECHO_20261015 (R1 a R8; regra quadratica; cadeia de Fock, Takesaki e Maxwell)"],
                   "cunhagens_embutidas": len(VERBATINS), "ja_na_v393": CD["ja_na_v393"]},
    }
    kh = {
        "nome": "kh_n1_cobertura_v394", "veredito_prefixo": "TGL_KH_N1_COBERTURA_V394",
        "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__GATE_UNMOVED" % (T["decl"], T["thm"]),
        "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do sandbox da v394; o conjunto exato das fontes formais que o hash formal do rito vera (as embutidas mais os residuais da pasta do Nos) e' pinado; a cobertura NAO move o gate",
        "fontes": ["kh_n1_v394"], "kernel_flags": [], "kernel_decls": [],
        "checks": [
            CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
            CH("h2", "constantes cobertas == as do sandbox v394 (KH_N1, geracao d19)", "kf", ["axiom_coverage_v392", "decl"], "igual", T["decl"], "constantes_cobertas"),
            CH("h3", "teoremas cobertos == os do sandbox v394 (KH_N1, geracao d19)", "kf", ["axiom_coverage_v392", "thm"], "igual", T["thm"], "teoremas_cobertos"),
            CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
            CH("h5", "nenhum nome que o leitor v394 nao leia (os 4 nomes com «» da v392 agora sao lidos)", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0),
            CH("h6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", khj["axiom_report_efetivo_n"]),
            CH("h7", "a cobertura da v394 inclui a da v393 (constantes >= 25161, teoremas >= 19901)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", 25161),
            CH("h8", "as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta, como _check_damming.lean) sao EXATAMENTE as do pino (arquivo -> sha256)", "kf", ["formal_files_sha256"], "igual", h8_map),
            CH("h9", "medida do Audit v394: duracao bem abaixo do timeout de 1800 s", "fonte:kh_n1_v394", ["duracao_audit_s"], "menor_igual", 900, "duracao_do_audit_s"),
            CH("h10", "medida do Audit v394: sorryAx ausente do log", "fonte:kh_n1_v394", ["sorryAx_no_log_do_audit"], "igual", 0),
            CH("h11", "medida do Audit v394: as entradas novas estao no trio", "fonte:kh_n1_v394", ["novas_no_trio"], "verdadeiro"),
            CH("h12", "a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
        ],
        "erratas": [{"ao_lado_de": "kh_n1_cobertura_v393 (h2/h3: igualdades de contagem; h5: quatro nomes que o leitor nao le)",
                     "dizia": "A v393 cobrava constantes == 25161 e teoremas == 19901 e declarava 4 nomes com «» que o regex do um.py nao le.",
                     "agora": "A v394 acrescenta as declaracoes das pedras do Codex (a cobertura cresce) e troca o leitor de axiomas pela versao do Codex, que le tambem os nomes com «»; o registro da v393 passa a cobrar a inclusao (piso 25161/19901); a igualdade exata e a leitura sem excecao ficam neste registro.",
                     "lacuna_de_fidelidade": "a estrutura da v393 dizia que o piso 25161 era a cobertura exata para sempre; o texto escrito deixou o registro preso a uma igualdade que a propria v394 quebra",
                     "estatuto": "[REAL: contagens lidas do log do Audit do sandbox]; a mesma troca por piso foi proposta pelo Codex na candidata r8 (F1.FECHO, rodada R7/R8), [DECLARADO]", "assinatura": ASSINA},
                    {"ao_lado_de": "kh_n1_cobertura_v394 (h8: as fontes formais embutidas == as do sandbox)",
                     "dizia": "O pino de h8 listava so' as fontes EMBUTIDAS no kernel do candidato (uma entrada por arquivo embutido).",
                     "agora": "O hash formal que o rito calcula (sha256_directory sobre Nos\\tgl_kernel) tambem conta os arquivos .lean que moram na pasta e NAO estao embutidos (hoje: _check_damming.lean, de 31/08, 226 bytes; ExtrairDeps.lean sai por exclusao nominal e declarada). "
                              "O pino de h8 passa a ser a ARVORE SIMULADA do Nos depois do rito: as fontes embutidas do candidato mais esses residuais, calculado por script (gerar_candidato_v394.py, conferido por simular_arvore_do_nos). Sem isto o registro NAO selaria no rito real; "
                              "e o pino fica preso tambem ao residual: se alguem mexer nele antes do rito, o h8 recusa (fail-closed).",
                     "lacuna_de_fidelidade": "estrutura: o hash formal e' o da pasta do Nos; escrito: o pino so' das fontes embutidas; falha: o ensaio a seco materializava so' o embutido e nao via o residual (achado do exame final de 19/10: SIMULACAO_ARVORE_NOS_4022ad521dc7293d.json)",
                     "estatuto": "[REAL: simulado sobre a pasta do Nos, so' leitura; o pino e' recalculado a cada geracao do candidato]", "assinatura": ASSINA},
                    {"ao_lado_de": "estatuto_da_prova_v391 (token KERNEL_N_OF_N_THEOREMS_M_OF_M_DECLARATIONS_IN_THE_TRIO)",
                     "dizia": "O veredito do estatuto lia a escada externa como «THEOREMS» (KERNEL_N_OF_N_THEOREMS).",
                     "agora": "A escada externa conta BANDEIRAS de declaracoes nomeadas (len(ext_flags)), e nem toda declaracao nomeada e' teorema: ha definicoes, estruturas e recursores gerados para as estruturas (mk, rec, recOn, casesOn, noConfusion e afins). "
                              "Desde a v394 o token diz KERNEL_N_OF_N_FLAGS; os numeros nao mudam de significado, so' a palavra. O estatuto_da_prova_ressalva_v392 (13/10) ja' dizia que a escada e' a externa, nao o total de teoremas.",
                     "lacuna_de_fidelidade": "estrutura: a escada conta bandeiras de declaracoes nomeadas; escrito: THEOREMS; falha: o substantivo «teorema» nao vale para todo item contado (exame final de 19/10, §4)",
                     "estatuto": "[REAL: nas bandeiras novas ha %d declaracoes nomeadas de modulos do Codex e da pedra do delta; as geradas para estruturas e inducoes estao entre elas]" % pol["n_flags"], "assinatura": ASSINA}],
        "limites": ["[REAL] os arquivos de medida sao do sandbox (fora do selo); a cobertura que vale e' a medida no Audit do proprio rito",
                    "[DECLARADO] a pre-auditoria integral do Codex (29.025 declaracoes, 23.068 teoremas) e' pinada como informativa; a medida do sandbox desta cadeia (com a pedra do delta) e' a que o rito cobra",
                    "[REAL] a escada do kernel conta bandeiras de declaracoes NOMEADAS (a pratica da v392 e da v393): as %d auxiliares geradas pelo compilador nos modulos do Codex (%d delas marcadas pelo Codex; _proof_N, _simp_N, match_N, _sunfold, eq_N, eq_def, congr_simp) ficam cobertas pelo KH-N1 mas sem bandeira, e as %d nomeadas que o Codex nao marcou ganharam bandeira" % (pol["n_auxiliares"], pol["n_excluidas"], pol["n_nomeadas_sem_bandeira"]),
                    "validade no kernel nao e' creditacao; o gate nao se move"],
        "diz": ["a cobertura do axiom_report no fecho inteiro cresceu para os numeros da v394 e segue sem constante fora do trio, sem nome ilegivel"],
        "nao_diz": ["que a cobertura prove algo alem de que nenhum axioma fora do trio foi lido"],
        "leituras_do_operador": [], "extras": {"assinatura": ASSINA, "politica_de_bandeiras": {k: pol[k] for k in ("n_flags", "n_codex_nomeadas", "n_nomeadas_sem_bandeira", "n_excluidas", "n_auxiliares", "por_grupo_bandeiras")}, "h8_entradas": len(h8_map),
                                               "h8_residuais_do_nos": sorted(set(h8_map) - set(formal_map))},
    }
    stone_sha = formal_map[DL.STONE_REL]
    crit = {
        "nome": "criterio_binario_de_parada_v394", "veredito_prefixo": "TGL_BINARY_STOP_CRITERION_V394",
        "veredito_sufixo": "THE_BINARY_READING_FLOATS_AT_THE_FIXED_POINT__EIGHT_KERNEL_THEOREMS_COMPOSED_BY_CITATION_IN_THE_TRIO__THE_STOP_IS_THE_FIXED_POINT_IS_AN_ONTO_READING_OF_THE_OPERATOR__QUBIT_ANALOGY_HOLDS_ON_THE_WEIGHTS_NOT_ON_THE_ENTROPY__OPERATOR_INSCRIPTIONS_OF_19_OCT_EMBEDDED_VERBATIM_BY_SHA256__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
        "estatuto": "[REAL -- a conjuncao (oito teoremas do kernel compostos por citacao) lida a cada rito do kernel do proprio rito; INPUT/ONTO a TGL binaria e a leitura «a parada e' o ponto fixo» (do operador); o kernel entrega a forma estrutural, a identificacao dela com o criterio de parada e' do operador]",
        "fontes": ["delta19_pedra"], "verbatins": VERB_DELTA, "kernel_flags": [DL.FLAG_KEY], "kernel_decls": [DL.THEOREM] + DL.CITED,
        "checks": [
            CH("g1", "a escada do kernel fecha (limpos == esperados), com a bandeira da pedra", "core", ["external_ladder", "all_verified"], "verdadeiro"),
            CH("g2", "a cobertura do axiom_report no fecho inteiro passou (nenhuma constante fora do trio)", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
            CH("g3", "a proveniencia emitida pelo compilador cobre o axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
            CH("g4", "o compilador emite o teorema de composicao no modulo da pedra (TGL_DECL_SOURCE)", "kf", ["declaration_sources_v394", DL.THEOREM], "igual", DL.STONE_REL),
            CH("g5", "a pedra no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)", "kf", ["formal_files_sha256", DL.STONE_REL], "igual", stone_sha),
            CH("g6", "o teorema de composicao depende de tres axiomas (o trio, conferido por inclusao em kernel_decls)", "kf", ["axiom_report", DL.THEOREM], "tamanho_igual", len(DL.TRIO)),
        ],
        "erratas": [],
        "limites": [
            "[REAL] a pedra compoe oito teoremas que ja' estavam no kernel e nao acrescenta hipotese nem lema; cada peso (1/2, 1/2) vale sob a hipotese que o teorema citado nomeia (traco nulo da graduacao de paridade; J-simetria do peso com soma 1)",
            "[ONTO] a identificacao do ponto fixo do colapso (C.step x = x) com o criterio de parada, e do par positivo/negativo com as faces P+ e P-, e' leitura do operador; o kernel entrega a estrutura (a leitura de ambos e' total sobre a forma, reler nao acrescenta, no ponto fixo nao ha transicao mudada, a iteracao e' estavel), nao um procedimento de decisao",
            "[REAL] a analogia com o qubit vale nos pesos (1/2, 1/2), nao na entropia: a entropia do bit justo (ln 2) nao e' a meia-nat (fair_bit_entropy_is_not_half_nat)",
            "[REAL] o 1 = 0 do negativo nao e' tipado como igualdade literal de numerais; o que o kernel entrega para o par positivo/negativo e' o par de faces (P+, P-)",
            "[OPEN] um procedimento de parada (algoritmo) como regra de auditoria nao esta no kernel: e' decisao do operador e da gerencia",
            "o nome da pedra e' provisorio: o operador nomeia; validade no kernel nao e' creditacao; o gate nao se move",
        ],
        "diz": ["as duas falas do operador de 19/10 estao embutidas por sha256, cada uma conferida contra o arquivo de origem na preparacao",
                "a conjuncao the_binary_reading_floats_at_the_fixed_point (oito teoremas do kernel, so' citados) esta no kernel do rito, dentro do trio, com bandeira e proveniencia no modulo da pedra",
                "no ponto fixo nao ha transicao mudada e a iteracao e' estavel; as duas faces partem a identidade e a leitura de ambas e' total sobre a forma"],
        "nao_diz": ["que a TGL seja um sistema quantico de dois niveis, nem que exista superposicao fisica de {1=1, 1=0}", "que o criterio de parada esteja formalizado como procedimento de decisao",
                    "que o 1 = 0 do negativo seja a igualdade literal de numerais", "que a gravidade quantica esteja creditada na natureza"],
        "leituras_do_operador": [
            {"trecho": "a TGL é binária: {[1=1=VERDADEIRO][1=0=Falso]}", "estatuto": "[INPUT/ONTO do operador, verbatim 19/10/2026, sha16 %s]" % SHA16_CRITERIO},
            {"trecho": "e a leitura de ambos é o resultado", "estatuto": "[INPUT/ONTO do operador, verbatim 19/10/2026, sha16 %s]" % SHA16_CRITERIO},
            {"trecho": "O sistema precisa flutuar no ponto fixo, igual um sistema quântico flutua sobre 1 e 0", "estatuto": "[INPUT/ONTO do operador, verbatim 19/10/2026, sha16 %s]" % SHA16_FLUTUAR},
        ],
        "extras": {"assinatura": ASSINA, "pedra": DL.STONE_MOD, "teorema": DL.THEOREM, "bandeira": DL.FLAG_KEY, "teoremas_citados": list(DL.CITED), "nome_da_pedra": "provisorio (o operador nomeia)"},
    }
    return [cun, kh, crit]
