# -*- coding: utf-8 -*-
"""registros_v395.py -- os dados dos registros por spec da v395 (interpretados pelo MOTOR _v392_registro, ja' no um.py): FONTES pinadas por sha256 (lidas do disco pelo montador, nunca digitadas), VERBATINS (as quatro falas do
operador de 21/10/2026, EMBUTIDAS: a fala embutida manda, o arquivo e' so' informativo) e SPECS (`cunhagens_v395` e `kh_n1_cobertura_v395`). O registro `psibit_v395` NAO e' spec: e' a FUNCAO psibit_v395(core), que calcula
a mecanica a cada rito (gerar_candidato_v395.py a emite; o CONTRATO dela sai de contrato() abaixo, derivado do build do sandbox). Fontes so' em pasta DURAVEL: tudo vem de cadeia_de_selo\\v395\\insumos.
Texto novo passa pela guarda P18 (a cada rito). Molde: registros_v394.py."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v395 as DL  # noqa: E402

INS = os.path.join(HERE, "insumos")
ASSINA = "gerencia c1, em nome proprio, 21/10/2026"

FONTES = [
    {"chave": "psibit_pedra", "arquivo": os.path.join(INS, DL.STONE_INSUMO), "papel": "a pedra TGLExt/Psibit.lean (2a versao, PEDRA_APROVADA na rodada 2 do exame independente; copia duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)"},
    {"chave": "psibit_definicao_patente", "arquivo": os.path.join(INS, "DEFINICAO_PSIBIT_PATENTE.md"), "papel": "a definicao do PsiBit nas patentes do operador, com arquivo, linhas e sha16 lidos por script, e a divergencia interna da tabela do ACOM Mirror"},
    {"chave": "psibit_resultado", "arquivo": os.path.join(INS, "RESULTADO_PSIBIT.md"), "papel": "o resultado da construcao da pedra (teoremas da ordem -> nomes Lean, conferencias, limites)"},
    {"chave": "psibit_exame_r1", "arquivo": os.path.join(INS, "EXAME_PSIBIT.md"), "papel": "o exame independente da 1a versao da pedra (APROVADA_COM_CORRECOES; as correcoes foram aplicadas na 2a versao)"},
    {"chave": "psibit_exame_r2", "arquivo": os.path.join(INS, "EXAME_PSIBIT_RODADA2.md"), "papel": "o exame independente da 2a versao da pedra, a ULTIMA rodada: PEDRA_APROVADA"},
    {"chave": "kh_n1_v395", "arquivo": os.path.join(INS, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox da v395 (pos_build_kernel_v395.py)"},
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
S_PSION, S_NOME, S_MECANICA, S_RATIFICA = (_VD[0]["sha16"], _VD[1]["sha16"], _VD[2]["sha16"], _VD[3]["sha16"])   # LIDOS dos arquivos, na ordem de DL.VERBATIM_ORIGEM
TEXTOS = {v["sha16"]: v["text"] for v in _VD}
CH = lambda id_, desc, onde, caminho, op, valor=None, cap=None, est="[REAL]": dict(id=id_, descricao=desc, onde=onde, caminho=caminho, op=op, **({"valor": valor} if valor is not None else {}), **({"capturar": cap} if cap else {}), estatuto=est)


def _leitura(trecho, sha16, quando="21/10/2026"):
    assert trecho in TEXTOS[sha16], ("a leitura do operador NAO esta verbatim na fala", sha16, trecho)
    return {"trecho": trecho, "estatuto": "[INPUT/ONTO do operador, verbatim %s, sha16 %s]" % (quando, sha16)}


def contrato(fj, formal_map, e_base, base_sha256):
    """O contrato do registro psibit_v395, DERIVADO do build do sandbox (FLAGS_v395.json = nomes e chaves; formal_map = sha256 das fontes embutidas; e_base = a escada da v394 selada); nada digitado."""
    flag_de = {n: k for k, n, m, o in fj["flags"]}
    faltam = [t for t in DL.CONTRACT_THEOREMS if t not in flag_de]
    assert not faltam, ("teorema do contrato sem bandeira (nao nomeado ou ausente do Audit)", faltam[:5])
    return {"stone": {"path": DL.STONE_REL, "sha256": formal_map[DL.STONE_REL], "module": DL.STONE_MOD},
            "unconditional": {"theorem": DL.THEOREM, "flag": flag_de[DL.THEOREM]},
            "conditional": {"theorem": DL.THEOREM_COND, "flag": flag_de[DL.THEOREM_COND]},
            "theorems": {t: flag_de[t] for t in DL.CONTRACT_THEOREMS}, "expected_ladder": e_base + fj["n_flags"], "n_flags": fj["n_flags"],
            "verbatins": list(VERB_CHAVES), "baseline": {"version": DL.BASE_VERSION, "sha256": base_sha256}}


def texto_psibit():
    """Os textos do registro psibit_v395 (a funcao do runtime, nao um spec): estatuto, escopo, limites, diz, nao_diz e o veredito de sucesso. Passam pela guarda P18 a cada rito (psibit_v395 as refaz)."""
    return {
        "estatuto": "[REAL] os termos do kernel (a conjuncao incondicional e os teoremas citados, lidos a cada rito, no trio) e o calculo da mecanica (beta = alfa CODATA 2018 x sqrt(e) em runtime, SEALED_CODATA_ALPHA = ALPHA_FINE_CODATA_2018 do script do nivel 2; theta_M = arcsin sqrt(beta)); "
                    "[INPUT/ONTO] psibit = psion = modo do leitor (o operador, 21/10/2026); [CONDICIONAL] a face do psion, a um certificado de Fock da luz que o kernel nao habita",
        "escopo": "a ORBITA do Um pela matriz-S (familia real de um parametro, plano real 2x2): a leitura do par (peso, Palavra, Verbo) e' uma bijecao de conjuntos sobre o livro de codigos, com perda zero; a travessia (o colapso D_inf) perde exatamente a paridade, um bit; "
                  "nao e' toda a mecanica quantica nem isomorfismo de espacos de Hilbert",
        "limites": [
            "[REAL] ESCOPO: a orbita do Um pela matriz-S, nao toda a mecanica quantica; a bijecao e' de CONJUNTOS (circulo unitario <-> livro de codigos, decodificador explicito), sem transportar estrutura alguma; o nome «isomorfismo» e' do operador",
            "[INPUT/ONTO] psibit = psion = modo do leitor e' a leitura do operador (21/10/2026): nenhum lema do kernel liga o psion (o vetor do vacuo do certificado da luz) ao codigo psibit; ler L como a transmissao e dL como a refletida tambem e' leitura dele",
            "[REAL] a face do psion (the_psion_face_of_the_psibit) e' CONDICIONAL: vale para todo certificado de Fock da luz, e o kernel nao exibe habitante algum; nao mostra que o psion exista e fica fora da composicao incondicional",
            "[REAL] ENTROPIA: so' H(cos^2 theta) = ln 2 nos pesos iguais (theta = pi/4 + k pi/2) e H <= ln 2; 'perde exatamente a paridade' e' estrutural (qual variavel se perde: um bit), nao quantidade de informacao; em theta_M a entropia dos resultados e' menor que ln 2",
            "[ONTO] 'ponto fixo' para os pesos iguais e' o nome do operador (19/10); o que o colapso e a conjugacao pela matriz-S fixam e' (1/2) I",
            "[REAL] em ponto flutuante o ida e volta do codigo erra ate' ~1e-12 muito perto dos eixos (cancelamento em 1 - w); em theta_M e nos angulos de controle o residuo e' < 1e-15; em R a igualdade e' exata (termo Lean)",
            "[LEGAL] a patente ACOM Mirror diverge de si mesma na nominacao dos estados por indice; a pedra nomeia por PAR DE SINAIS e segue o produto (formula, reivindicacoes 3 e 4, codigo): a escolha da leitura canonica e' decisao do operador",
            "o calculo e' numerico em dupla precisao e CONFERE os teoremas, nao os prova: quem prova e' o kernel; validade no kernel nao e' creditacao; o gate nao se move",
        ],
        "diz": ["a pedra Psibit esta no kernel do rito, no trio, com bandeira e proveniencia no modulo da pedra; a conjuncao psibit_is_the_mode_of_the_reader (incondicional) e a face do psion (condicional) sao lidas deste kernel",
                "a mecanica da orbita do Um pela matriz-S em theta_M = arcsin sqrt(beta), com beta = alfa CODATA 2018 x sqrt(e) em runtime (um dado, dois nomes: SEALED_CODATA_ALPHA e ALPHA_FINE_CODATA_2018), e' calculada agora e concorda com os teoremas: o Verbo e' metade da derivada do Nome; o estado e' puro; o codigo (peso, Palavra, Verbo) decodifica sem perda; "
                "o colapso D_inf nao ve a paridade; nos pesos iguais o colapso e' (1/2) I e a entropia dos resultados e' ln 2",
                "as quatro falas do operador de 21/10 estao embutidas por sha256"],
        "nao_diz": ["que a natureza fisica seja o psibit, nem que o psion fisico seja o modo do leitor", "que exista isomorfismo de espacos de Hilbert entre a orbita e a teoria da informacao (so' bijecao de conjuntos sobre o livro de codigos)",
                    "que o certificado de Fock da luz tenha habitante, nem que o psion exista", "que a perda do colapso valha ln 2 em geral", "que a divergencia da tabela da patente esteja decidida", "que a gravidade quantica esteja creditada na natureza"],
        "veredito_ok": "TGL_PSIBIT_V395__THE_PSIONIC_MODE_IN_THE_FRACTALIZATION_OF_THE_ONE__MECHANICS_COMPUTED_ON_THE_ORBIT_BY_THE_S_MATRIX_AT_THETA_M_AND_READ_AGAINST_THE_KERNEL_TRIO__THE_READING_OF_THE_PAIR_LOSES_NOTHING_AND_THE_COLLAPSE_LOSES_EXACTLY_THE_PARITY__"
                       "THE_PSION_FACE_IS_CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE__PSIBIT_EQUALS_PSION_EQUALS_THE_READERS_MODE_IS_THE_OPERATORS_ONTO_READING__A_BIJECTION_OF_SETS_NOT_A_HILBERT_ISOMORPHISM__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


def especs(formal_map, khj, h8_map, fj, cov_base, n_axioms_unc):
    """formal_map = {arquivo embutido: sha256} do kernel da v395; khj = KH_N1_v395.json (medida desta geracao); h8_map = o dict do hash formal que o RITO vai gerar (embutidos + residuais do Nos que sha256_directory conta;
    simular_arvore_do_nos); fj = FLAGS_v395.json; cov_base = a cobertura da v394 selada {decl, thm}; n_axioms_unc = quantos axiomas o teorema incondicional usa (lido do Audit: o trio)."""
    T = khj["linha_TOTAL"]
    stone_sha = formal_map[DL.STONE_REL]
    flag_unc, flag_cond = fj["bandeira_do_teorema_incondicional"], fj["bandeira_do_teorema_condicional"]
    cun = {
        "nome": "cunhagens_v395", "veredito_prefixo": "TGL_CUNHAGENS_V395",
        "veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_21_OCT_EMBEDDED_VERBATIM_BY_SHA256__THE_PSIBIT_MODE_IS_READ_IN_THE_RITE_AT_THE_FRACTALIZATION_OF_THE_ONE__PSIBIT_EQUALS_PSION_EQUALS_THE_READERS_MODE_IS_THE_OPERATORS_ONTO_READING__THE_PSION_FACE_IS_CONDITIONAL__OPERATOR_INPUT__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
        "estatuto": "[REAL -- fontes, kernel e o registro psibit_v395 lidos a cada rito; INPUT/ONTO as cunhagens do operador e a identidade psibit = psion = modo do leitor; DECLARADO o que os exames e o resultado relatam e esta chancela nao refez (a pedra e' recompilada no sandbox da cadeia e conferida pelo axiom_report do proprio rito)]",
        "fontes": [f["chave"] for f in FONTES if f["chave"] != "kh_n1_v395"], "verbatins": list(VERB_CHAVES),
        "kernel_flags": [flag_unc, flag_cond], "kernel_decls": list(DL.CONTRACT_THEOREMS),
        "checks": [
            CH("u1", "o registro psibit_v395 selou neste rito (o formal e a mecanica)", "core", ["psibit_v395", "all_verified"], "verdadeiro"),
            CH("u2", "a composicao INCONDICIONAL esta no kernel do rito (bandeira True, trio, modulo da pedra)", "core", ["psibit_v395", "unconditional", "in_kernel"], "verdadeiro"),
            CH("u3", "a face do psion segue CONDICIONAL ao certificado", "core", ["psibit_v395", "conditional_psion_face", "status"], "igual", "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE"),
            CH("u4", "nenhum habitante do certificado de Fock da luz foi exibido", "core", ["psibit_v395", "conditional_psion_face", "inhabitant_exhibited"], "falso"),
            CH("u5", "a escada do kernel fecha (limpos == esperados), com as bandeiras da pedra", "core", ["external_ladder", "all_verified"], "verdadeiro"),
            CH("u6", "a proveniencia emitida pelo compilador cobre o axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
            CH("u7", "o compilador emite o teorema incondicional no modulo da pedra (TGL_DECL_SOURCE)", "kf", ["declaration_sources_v394", DL.THEOREM], "igual", DL.STONE_REL),
            CH("u8", "a pedra no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)", "kf", ["formal_files_sha256", DL.STONE_REL], "igual", stone_sha),
            CH("u9", "o teorema incondicional depende do trio e de nada alem (tamanho da lista de axiomas)", "kf", ["axiom_report", DL.THEOREM], "tamanho_igual", n_axioms_unc),
        ],
        "erratas": [{"ao_lado_de": "RESULTADO_PSIBIT.md (21/10/2026), secao «Conferencias independentes»",
                     "dizia": "O resultado dizia que a 2a versao da pedra (sha16 50c199eb01976151) ainda NAO tinha sido reexaminada pelo exame independente.",
                     "agora": "O exame independente reexaminou essa mesma versao (EXAME_PSIBIT_RODADA2.md, gerencia c1, modelo forte, 21/10/2026, a 2a e ULTIMA rodada) e a aprovou: composicao incondicional nao vacua, face do psion condicional e dita como tal, bijecao nos dois sentidos, recompilacao e axiomas no trio. Os dois exames estao pinados como fontes deste registro.",
                     "lacuna_de_fidelidade": "estrutura: a pedra foi reexaminada e aprovada; escrito: o resultado dizia que ainda nao; falha: o documento de resultado foi escrito antes do fim do exame da rodada 2 e nao foi reescrito depois",
                     "estatuto": "[REAL: o sha16 da pedra no exame da rodada 2 e' o da pedra pinada; lido por script na preparacao]", "assinatura": ASSINA}],
        "limites": [
            "[REAL] a pedra prova, sobre a ORBITA do Um pela matriz-S (familia real de um parametro, plano real 2x2), uma BIJECAO de CONJUNTOS entre o circulo unitario e o livro de codigos, com decodificador explicito: nao e' isomorfismo de espacos de Hilbert nem de categorias, e nao e' toda a mecanica quantica",
            "[INPUT/ONTO] psibit = psion = modo do leitor e' a leitura do operador (21/10/2026): nenhum lema do kernel liga o psion (o vetor do vacuo do certificado da luz) ao codigo psibit; ler L como a transmissao (cos theta) e dL como a refletida tambem e' leitura dele",
            "[REAL] a face do psion e' um teorema CONDICIONAL: vale para todo certificado de Fock da luz, e o kernel nao exibe habitante algum (TheImportedSecondQuantization, l.66-67; os montadores da v394 partem de entradas restantes sem habitante exibido); o enunciado nao mostra que o psion exista",
            "[REAL] entropia: so' H(cos^2 theta) = ln 2 nos pesos iguais (theta = pi/4 + k pi/2) e H <= ln 2; nao se diz que o colapso perde ln 2 em geral, nem a entropia de canal fisico algum; 'perde exatamente a paridade' e' estrutural (qual variavel), nao quantidade de informacao",
            "[ONTO] o nome 'ponto fixo' para os pesos iguais e' leitura do operador (19/10); a equacao e' [REAL] e (1/2) I e' fixado pelo colapso e por toda conjugacao pela matriz-S",
            "[LEGAL] a patente ACOM Mirror diverge de si mesma na nominacao dos estados por indice (tabela x formula de indice x docstring do codigo); a pedra nomeia por PAR DE SINAIS e segue o produto (formula, reivindicacoes 3 e 4, codigo executado); qual leitura e' canonica, e se isso mexe nas patentes, e' decisao do operador",
            "o nome da pedra e' do operador («Eu prefiro que seja psibit»); validade no kernel nao e' creditacao; o gate nao se move",
        ],
        "diz": ["as quatro falas do operador de 21/10 estao embutidas por sha256, cada uma conferida contra o arquivo de origem na preparacao",
                "o modo psionico e' lido NA FRACTALIZACAO DO UM, no ponto de chamada real do main: a mecanica da orbita do Um pela matriz-S em theta_M (beta, rho, codigo psibit, decodificacao, colapso, Verbo como derivada do Nome, bit justo) e' calculada a cada rito e confrontada com os termos do kernel do proprio rito",
                "a leitura do par (peso, Palavra, Verbo) nao perde nada e o colapso perde exatamente a paridade: o separante e o separador no mesmo objeto"],
        "nao_diz": ["que a natureza fisica seja o psibit, nem que o psion fisico seja o modo do leitor", "que exista isomorfismo de espacos de Hilbert entre a orbita e a teoria da informacao", "que o certificado de Fock da luz tenha habitante",
                    "que a divergencia da tabela da patente esteja decidida", "que a gravidade quantica esteja creditada na natureza"],
        "leituras_do_operador": [
            _leitura("[psibit=psion=modo do leitor]", S_PSION), _leitura("sem o pareamento binário não há leitura", S_PSION),
            _leitura("eu quero que o modo psionico entre no código na fractalização do um igual porque aí eu inclusive provo a mecânica", S_NOME),
            _leitura("a mecânica demonstra o isoformismo com a teoria da informação com perda residual zero", S_MECANICA),
            _leitura("sua correção de leitura quanto a perda residual zero  está certa e a correção é justa", S_RATIFICA)],
        "extras": {"assinatura": ASSINA, "autoria_das_cunhagens": "Luiz Antonio Rotoli Miguel", "pedra": DL.STONE_MOD, "teorema": DL.THEOREM, "teorema_condicional": DL.THEOREM_COND, "bandeira": flag_unc, "bandeira_condicional": flag_cond,
                   "n_bandeiras": fj["n_flags"], "nome_da_pedra": "Psibit (o nome e' do operador)", "cunhagens_embutidas": len(VERBATINS), "exames": ["EXAME_PSIBIT.md (1a versao, APROVADA_COM_CORRECOES)", "EXAME_PSIBIT_RODADA2.md (2a versao, PEDRA_APROVADA)"]},
    }
    kh = {
        "nome": "kh_n1_cobertura_v395", "veredito_prefixo": "TGL_KH_N1_COBERTURA_V395",
        "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__THE_PSIBIT_MODULE_ADDED__GATE_UNMOVED" % (T["decl"], T["thm"]),
        "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do sandbox da v395; o conjunto exato das fontes formais que o hash formal do rito vera (as embutidas mais os residuais da pasta do Nos) e' pinado; a cobertura NAO move o gate",
        "fontes": ["kh_n1_v395"], "kernel_flags": [], "kernel_decls": [],
        "checks": [
            CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
            CH("h2", "constantes cobertas == as do sandbox v395 (KH_N1)", "kf", ["axiom_coverage_v392", "decl"], "igual", T["decl"], "constantes_cobertas"),
            CH("h3", "teoremas cobertos == os do sandbox v395 (KH_N1)", "kf", ["axiom_coverage_v392", "thm"], "igual", T["thm"], "teoremas_cobertos"),
            CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
            CH("h5", "nenhum nome que o leitor v394 nao leia", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0),
            CH("h6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", khj["axiom_report_efetivo_n"]),
            CH("h7", "a cobertura da v395 inclui a da v394 selada (constantes e teoremas)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", cov_base["decl"]),
            CH("h7b", "os teoremas cobertos incluem os da v394 selada", "kf", ["axiom_coverage_v392", "thm"], "maior_igual", cov_base["thm"]),
            CH("h8", "as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta, como _check_damming.lean) sao EXATAMENTE as do pino (arquivo -> sha256)", "kf", ["formal_files_sha256"], "igual", h8_map),
            CH("h9", "medida do Audit v395: duracao bem abaixo do timeout de 1800 s", "fonte:kh_n1_v395", ["duracao_audit_s"], "menor_igual", 900, "duracao_do_audit_s"),
            CH("h10", "medida do Audit v395: sorryAx ausente do log", "fonte:kh_n1_v395", ["sorryAx_no_log_do_audit"], "igual", 0),
            CH("h11", "medida do Audit v395: as entradas novas estao no trio", "fonte:kh_n1_v395", ["novas_no_trio"], "verdadeiro"),
            CH("h12", "a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
        ],
        "erratas": [{"ao_lado_de": "kh_n1_cobertura_v394 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                     "dizia": "A v394 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v394 e o hash formal igual ao pino exato da arvore da v394." % (cov_base["decl"], cov_base["thm"]),
                     "agora": "A v395 acrescenta o modulo Psibit (a cobertura cresce e a arvore ganha o arquivo da pedra): na v395 o registro da v394 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato da arvore ficam NESTE registro. O veredito do registro da v394 NAO muda.",
                     "lacuna_de_fidelidade": "a estrutura da v394 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v395 quebra (achado no ensaio a seco: o registro da v394 NAO selaria sem a troca)",
                     "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; h2, h3, h6 e h8 conferidas no ensaio a seco e na arvore simulada do Nos]", "assinatura": ASSINA}],
        "limites": ["[REAL] os arquivos de medida sao do sandbox (fora do selo); a cobertura que vale e' a medida no Audit do proprio rito",
                    "[REAL] a escada do kernel conta bandeiras de declaracoes NOMEADAS (a pratica da v392, v393 e v394): as %d auxiliares geradas pelo compilador no modulo da pedra ficam cobertas pelo KH-N1 mas sem bandeira, e as %d nomeadas publicas ganharam bandeira" % (fj["excluidas_auxiliares"]["n"], fj["n_flags"]),
                    "validade no kernel nao e' creditacao; o gate nao se move"],
        "diz": ["a cobertura do axiom_report no fecho inteiro cresceu para os numeros da v395 (o modulo Psibit) e segue sem constante fora do trio, sem nome ilegivel"],
        "nao_diz": ["que a cobertura prove algo alem de que nenhum axioma fora do trio foi lido"],
        "leituras_do_operador": [], "extras": {"assinatura": ASSINA, "n_bandeiras": fj["n_flags"], "h8_entradas": len(h8_map), "h8_residuais_do_nos": sorted(set(h8_map) - set(formal_map))},
    }
    return [cun, kh]
