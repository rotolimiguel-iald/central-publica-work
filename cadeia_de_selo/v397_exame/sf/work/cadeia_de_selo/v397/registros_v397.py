# -*- coding: utf-8 -*-
"""registros_v397.py -- os dados dos registros por spec da v397 (interpretados pelo MOTOR _v392_registro, ja' no um.py): FONTES pinadas por sha256 (lidas do disco pelo montador, nunca digitadas), VERBATINS (as QUATRO falas do
operador de 23/10/2026, EMBUTIDAS: a fala embutida manda, o arquivo e' so' informativo) e tres SPECS: `teste_de_veracidade_fase9_v397` (o REGISTRO do resultado do Teste da Unica Palavra: le por sha256 o resultado e os tres
recibos e compoe a leitura binaria do operador; NENHUM sigma novo), `cunhagens_v397` (as quatro falas, a pedra Token e a conjuncao no kernel) e `kh_n1_cobertura_v397` (a cobertura exata do Audit). O registro de veracidade NAO e'
funcao nova: e' spec, chamado no ponto real do main ao lado do V1 (hubble_ratio_opening_v388); a formatacao do quadro mora em runtime_quadro_v397.py. Fontes so' em pasta DURAVEL: tudo vem de cadeia_de_selo\\v397\\insumos.
Texto novo passa pela guarda P18 (a cada rito). Molde: registros_v396.py."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v397 as DL  # noqa: E402

INS = os.path.join(HERE, "insumos")
INS_F9 = os.path.join(INS, "fase9")
ASSINA = "gerencia c1, em nome proprio, 23/10/2026"
NOME_VERACIDADE = "teste_de_veracidade_fase9_v397"        # nome PROVISORIO; quem nomeia e' o operador

_F9 = DL.f9_fontes(INS_F9)
FONTES = ([{"chave": "token_pedra", "arquivo": os.path.join(INS, DL.STONE_INSUMO), "papel": "a pedra TGLExt/Token.lean (o nome «token» e' do operador, 23/10/2026; copia duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256)"},
           {"chave": "kh_n1_v397", "arquivo": os.path.join(INS, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox da v397 (pos_build_kernel_v397.py)"}]
          + [{"chave": f["chave"], "arquivo": f["arquivo"], "papel": p} for f, p in zip(_F9, (
              "o RESULTADO do Teste da Unica Palavra (Fase 9 V2-c1), aberto UMA vez em 23/10/2026 pela funcao de veredito congelada antes; copia duravel, byte a byte, do resultado original (work\\fase9_v2_c1_23out\\saidas)",
              "o RECIBO DE CONGELAMENTO da Fase 9 V2-c1 (a funcao, o pre-registro e as fontes dos leitores pinados antes da abertura); copia duravel",
              "o RECIBO DE ABERTURA da Fase 9 V2-c1 (ato da gerencia: a abertura UNICA, apos o congelamento); copia duravel",
              "o marcador ABERTURA_CONSUMIDA da Fase 9 V2-c1 (impede uma segunda abertura); copia duravel"))])


def _trecho(t):
    s = t.strip().splitlines()[0].strip() if t.strip() else ""
    s = s[:48].rstrip()
    assert s and s in t, s
    return s


_VD = DL.verbatins(os.path.join(INS, "cunhagens"))
VERBATINS = [{"chave": v["chave"], "arquivo": v["arquivo"], "quando": v["quando"], "trechos": [_trecho(v["text"])], "papel": v["papel"], "fonte_original": v["fonte_original"]} for v in _VD]
VERB_CHAVES = [v["chave"] for v in _VD]
SHA16 = {os.path.basename(v["fonte_original"]): v["sha16"] for v in _VD}
S_UNICA, S_TOKEN, S_VERAC, S_444 = (_VD[0]["sha16"], _VD[1]["sha16"], _VD[2]["sha16"], _VD[3]["sha16"])   # LIDOS dos arquivos, na ordem de DL.VERBATIM_ORIGEM
CH_UNICA, CH_TOKEN, CH_VERAC, CH_444 = (_VD[0]["chave"], _VD[1]["chave"], _VD[2]["chave"], _VD[3]["chave"])
TEXTOS = {v["sha16"]: v["text"] for v in _VD}
SHA16_ORDEM = DL.sha256(open(DL.ORDEM_SEM_GORDURA, "rb").read())[:16]   # a ordem de processo de 22/10 (sem teste armado, sem gordura): citada pelo sha16 LIDO, nao embutida
CH = lambda id_, desc, onde, caminho, op, valor=None, cap=None, est="[REAL]": dict(id=id_, descricao=desc, onde=onde, caminho=caminho, op=op, **({"valor": valor} if valor is not None else {}), **({"capturar": cap} if cap else {}), estatuto=est)


def _leitura(trecho, sha16, quando="23/10/2026"):
    assert trecho in TEXTOS[sha16], ("a leitura do operador NAO esta verbatim na fala", sha16, trecho)
    return {"trecho": trecho, "estatuto": "[INPUT/ONTO do operador, verbatim %s, sha16 %s]" % (quando, sha16)}


def f9_dados():
    """Os quatro JSON do Teste da Unica Palavra LIDOS do disco (as copias duraveis em insumos\\fase9) + os sha256: {chave: {json, sha256}}. Nada digitado."""
    out = {}
    for f in _F9:
        b = open(f["arquivo"], "rb").read() if os.path.exists(f["arquivo"]) else open(f["origem"], "rb").read()
        assert DL.sha256(b) == f["sha256"], ("a copia duravel difere da origem", f["chave"])
        out[f["chave"]] = {"json": json.loads(b.decode("utf-8")), "sha256": f["sha256"]}
    return out


def _fz(x, nd=2):
    """numero -> sufixo de veredito: 4.44 -> 4P44, -1.48 -> M1P48 (formatado por script a partir do resultado pinado)."""
    s = ("%.*f" % (nd, abs(x))).replace(".", "P")
    return ("M" if x < 0 else "") + s


def _fp(p):
    """p -> 4.4E_M6 (mantissa 1 casa, expoente)."""
    m, e = ("%.1e" % p).split("e")
    return "%sE_%s%d" % (m.replace(".", "P"), "M" if int(e) < 0 else "P", abs(int(e)))


def espec_veracidade(f9):
    """O spec do REGISTRO do Teste da Unica Palavra. f9 = f9_dados(). Os valores esperados dos checks sao LIDOS dos arquivos pinados (nada digitado); o veredito carrega os numeros formatados por script."""
    res, cong, aber, cons = (f9[k]["json"] for k in ("f9v2_resultado", "f9v2_congelamento", "f9v2_abertura", "f9v2_consumida"))
    sh = {k: f9[k]["sha256"] for k in f9}
    R = lambda *cam: DL.lido(res, list(cam))
    n = {k: DL.lido(res, c) for k, c in DL.F9_CAMINHOS.items()}
    ent_min, ent_max = DL.lido(res, ["primario", "entrada_da_funcao", "minimum"]), DL.lido(res, ["primario", "entrada_da_funcao", "maximum"])
    assert n["z_delta_calibrado"] == ent_min["z_delta"] and n["z_disc_calibrado"] == ent_max["z_disc"] and n["poder_previo"] == ent_max["poder_previo"], "o resultado nao e' coerente consigo mesmo"
    assert n["lnB_lcdm"] == ent_max["lnB_lcdm"] and n["lnB_beta_livre"] == ent_max["lnB_livre"], "o lnB do resultado nao e' coerente consigo mesmo"
    assert n["z_disc_calibrado"] < 5.0 < n["poder_previo"], "a leitura 'abaixo de 5 sigma, com poder' NAO vale nos numeros pinados"
    F = "fonte:"
    ck = [
        # --- o resultado: identidade, veredito, cadeia de pinos
        CH("r1", "o resultado e' pacote REAL", F + "f9v2_resultado", ["kind_do_pacote"], "igual", "REAL"),
        CH("r2", "o token-base do veredito e' o da Unica Palavra", F + "f9v2_resultado", ["token_base"], "igual", DL.F9_TOKEN_BASE),
        CH("r3", "o veredito comeca pelo token-base e e' o da funcao congelada (lido)", F + "f9v2_resultado", ["veredito"], "comeca", DL.F9_TOKEN_BASE + "__", "f9_veredito"),
        CH("r4", "o veredito diz NOT_FALSIFIED_POWERED (nao falsificada, com poder)", F + "f9v2_resultado", ["veredito"], "contem", "NOT_FALSIFIED_POWERED"),
        CH("r5", "o veredito diz NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY (abaixo do degrau de 5 sigma)", F + "f9v2_resultado", ["veredito"], "contem", "NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY"),
        CH("r6", "o veredito diz NOT_BLIND_TO_DATA_STATED (os centros dos leitores sao publicos)", F + "f9v2_resultado", ["veredito"], "contem", "NOT_BLIND_TO_DATA_STATED"),
        CH("r7", "o veredito diz NOT_A_CONFIRMATION e GATE_UNTOUCHED", F + "f9v2_resultado", ["veredito"], "contem", "NOT_A_CONFIRMATION__GATE_UNTOUCHED"),
        CH("r8", "o veredito do primario e' o do topo do resultado", F + "f9v2_resultado", ["primario", "veredito"], "igual", res["veredito"]),
        CH("r9", "o resultado pina o recibo de congelamento (sha256 do arquivo pinado aqui)", F + "f9v2_resultado", ["pinos", "recibo_de_congelamento_sha256"], "igual", sh["f9v2_congelamento"], "f9_recibo_congelamento_sha256"),
        CH("r10", "o resultado pina o recibo de abertura (sha256 do arquivo pinado aqui)", F + "f9v2_resultado", ["pinos", "recibo_de_abertura_sha256"], "igual", sh["f9v2_abertura"], "f9_recibo_abertura_sha256"),
        CH("r11", "o resultado pina o autohash do recibo de abertura", F + "f9v2_resultado", ["pinos", "abertura_autohash"], "igual", aber["autohash"]),
        CH("r12", "o resultado pina a funcao de veredito congelada (sha256 do recibo de congelamento)", F + "f9v2_resultado", ["pinos", "funcao_sha256"], "igual", cong["pins"]["funcao_arquivo"]["sha256"]),
        CH("r13", "o resultado pina o pre-registro canonico congelado", F + "f9v2_resultado", ["pinos", "spec_canonico_sha256"], "igual", cong["pins"]["spec_canonico_sha256"]),
        CH("r14", "o resultado pina o registro D-H", F + "f9v2_resultado", ["pinos", "registro_dh_sha256"], "igual", cong["pins"]["registro_dh"]["sha256"]),
        # --- os recibos: schema e a cadeia congelamento -> abertura -> consumida
        CH("c1", "o recibo de congelamento tem o schema da Fase 9 V2-c1", F + "f9v2_congelamento", ["schema"], "igual", DL.F9_SCHEMAS["f9v2_congelamento"]),
        CH("c2", "o recibo de congelamento e' pacote REAL e tem o token-base", F + "f9v2_congelamento", ["token_base"], "igual", DL.F9_TOKEN_BASE),
        CH("a1", "o recibo de abertura tem o schema da Fase 9 V2-c1", F + "f9v2_abertura", ["schema"], "igual", DL.F9_SCHEMAS["f9v2_abertura"]),
        CH("a2", "o recibo de abertura pina o recibo de congelamento (sha256)", F + "f9v2_abertura", ["freeze_receipt_sha256"], "igual", sh["f9v2_congelamento"]),
        CH("k1", "o marcador de abertura consumida tem o schema da Fase 9 V2-c1", F + "f9v2_consumida", ["schema"], "igual", DL.F9_SCHEMAS["f9v2_consumida"]),
        CH("k2", "o marcador pina o recibo de abertura (sha256)", F + "f9v2_consumida", ["recibo_de_abertura_sha256"], "igual", sh["f9v2_abertura"]),
        CH("k3", "o marcador pina o recibo de congelamento (sha256)", F + "f9v2_consumida", ["recibo_de_congelamento_sha256"], "igual", sh["f9v2_congelamento"]),
        CH("k4", "o marcador pina o autohash do recibo de abertura", F + "f9v2_consumida", ["recibo_de_abertura_autohash"], "igual", aber["autohash"]),
        # --- beta: alfa CODATA 2018 x sqrt(e) em runtime, conferido contra o beta do resultado
        CH("b1", "o beta do resultado concorda com alfa CODATA 2018 x sqrt(e) calculado neste rito (tolerancia relativa 1e-12)", F + "f9v2_resultado", ["beta", "beta_runtime"], "perto_de_beta_runtime", 1e-12, "beta_do_resultado"),
        # --- os numeros do resultado (lidos; nenhum sigma novo): valor lido == valor pinado na geracao; capturados para o artigo, o quadro e o conferidor
        CH("n1", "z_disc calibrado (Lambda sem beta)", F + "f9v2_resultado", DL.F9_CAMINHOS["z_disc_calibrado"], "igual", n["z_disc_calibrado"], "z_disc_calibrado"),
        CH("n2", "p unilateral calibrado de z_disc", F + "f9v2_resultado", DL.F9_CAMINHOS["p_disc_unilateral"], "igual", n["p_disc_unilateral"], "p_disc_unilateral"),
        CH("n3", "z_delta calibrado (a TGL)", F + "f9v2_resultado", DL.F9_CAMINHOS["z_delta_calibrado"], "igual", n["z_delta_calibrado"], "z_delta_calibrado"),
        CH("n4", "p bilateral calibrado de z_delta", F + "f9v2_resultado", DL.F9_CAMINHOS["p_delta_bilateral"], "igual", n["p_delta_bilateral"], "p_delta_bilateral"),
        CH("n5", "poder previo (so' pelo sigma)", F + "f9v2_resultado", DL.F9_CAMINHOS["poder_previo"], "igual", n["poder_previo"], "poder_previo"),
        CH("n6", "ln B(TGL/LCDM) (razao de verossimilhanca integrada)", F + "f9v2_resultado", DL.F9_CAMINHOS["lnB_lcdm"], "igual", n["lnB_lcdm"], "lnB_lcdm"),
        CH("n7", "ln B(TGL/beta livre) (beta fixo contra beta ajustado)", F + "f9v2_resultado", DL.F9_CAMINHOS["lnB_beta_livre"], "igual", n["lnB_beta_livre"], "lnB_beta_livre"),
        CH("n8", "o fator K = E(z*)^(2 beta/3) do resultado", F + "f9v2_resultado", DL.F9_CAMINHOS["K"], "igual", n["K"], "K"),
        CH("n9", "z_disc calibrado esta ABAIXO do degrau de 5 sigma da creditacao (a discriminacao a 5 sigma nao foi alcancada)", F + "f9v2_resultado", DL.F9_CAMINHOS["z_disc_calibrado"], "menor_igual", 5.0),
        CH("n10", "o poder previo (so' pelo sigma) e' de pelo menos 5 sigma (nao falsificada COM PODER)", F + "f9v2_resultado", DL.F9_CAMINHOS["poder_previo"], "maior_igual", 5.0),
        CH("n11", "o z_disc do primario e' o da entrada da funcao congelada (extremo de maior sigma)", F + "f9v2_resultado", ["primario", "entrada_da_funcao", "maximum", "z_disc"], "igual", n["z_disc_calibrado"]),
        CH("n12", "o z_delta do primario e' o da entrada da funcao congelada (extremo de menor sigma)", F + "f9v2_resultado", ["primario", "entrada_da_funcao", "minimum", "z_delta"], "igual", n["z_delta_calibrado"]),
    ]
    suf = ("THE_UNIQUE_WORD_TEST_OPENED_ONCE_READ_BY_HASH__LAMBDA_ALONE_FACE_Z_DISC_%s_P_UNILATERAL_%s_BELOW_5SIGMA_NOT_DISCRIMINATED_THE_CREDITATION_STEP_NOT_REACHED__"
           "TGL_FACE_Z_DELTA_%s_P_BILATERAL_%s_PRIOR_POWER_%s_NOT_FALSIFIED_WITH_POWER__"
           "CONJUGATION_LNB_TGL_LCDM_%s_LNB_TGL_BETA_FREE_%s_BETA_FIXED_BEATS_BETA_FREE__LNB_IS_NOT_SIGMA_THE_READINGS_ARE_NOT_MULTIPLIED__"
           "NOT_BLIND_TO_DATA_STATED__NO_NEW_SIGMA_COMPUTED__THE_BINARY_READING_IS_THE_OPERATORS_INPUT_AND_ONTO__VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED"
           % (_fz(n["z_disc_calibrado"]), _fp(n["p_disc_unilateral"]), _fz(n["z_delta_calibrado"]), _fz(n["p_delta_bilateral"]), _fz(n["poder_previo"]), _fz(n["lnB_lcdm"]), _fz(n["lnB_beta_livre"])))
    return {
        "nome": NOME_VERACIDADE, "veredito_prefixo": "TGL_FASE9_VERACIDADE_V397", "veredito_sufixo": suf,
        "estatuto": "[REAL -- o resultado do Teste da Unica Palavra (Fase 9 V2-c1, aberto UMA vez em 23/10/2026) e os tres recibos, lidos a cada rito por sha256; os numeros sao os do resultado, nenhum sigma novo e' calculado; "
                    "beta = alfa CODATA 2018 x sqrt(e) em runtime, conferido contra o do resultado; INPUT/ONTO a leitura binaria do operador; KNOWN a escala de Jeffreys]",
        "fontes": ["f9v2_resultado", "f9v2_congelamento", "f9v2_abertura", "f9v2_consumida"], "verbatins": [CH_UNICA, CH_VERAC, CH_444], "kernel_flags": [], "kernel_decls": [],
        "checks": ck,
        "erratas": [],
        "limites": [
            "[REAL] NAO e' teste novo nem armado: e' o REGISTRO do resultado do Teste da Unica Palavra, aberto UMA vez em 23/10/2026 pela funcao de veredito congelada antes (recibo de congelamento); este registro so' LE o resultado e os tres recibos por sha256 e compoe a leitura; "
            "nenhum sigma, p ou lnB e' calculado aqui; a abertura consumida nao se repete; a ordem de processo do operador de 22/10 (arquivo de sha16 %s: nada de teste armado, gordura no um.py) molda este registro" % SHA16_ORDEM,
            "[REAL] ln B nao se converte em sigma; z_delta, z_disc e ln B sao leituras do MESMO objeto (os mesmos leitores locais e o mesmo fundo), nao testemunhas autonomas: nao se multiplicam nem se somam; a regra v315 do acervo (para falsificar) pede duas determinacoes mutuamente autonomas a 5 sigma ou mais",
            "[REAL] validade nao e' creditacao: a discriminacao a 5 sigma e' o degrau da creditacao e NAO foi alcancada (z_disc calibrado abaixo de 5, com o p unilateral lido do resultado); «decisivo» na escala de Jeffreys e' [KNOWN] e fala de ln B, nao de sigma; NOT_FALSIFIED nunca e' a palavra da creditacao",
            "[REAL] o teste NAO foi cego ao dado: os centros dos leitores locais sao publicos (o token do veredito diz NOT_BLIND_TO_DATA_STATED); o resultado se preserva como saiu",
            "[INPUT/ONTO] 'Lambda sem beta nao ecoa', o 1=1 da TGL e o 1=0 do Lambda sozinho sao a leitura binaria do operador (23/10/2026); o que o registro entrega sao os numeros e os tokens do veredito; 'a Palavra flutua sobre o abismo pelo fator K' e' leitura do operador (K lido do resultado)",
            "o gate nao se move (qg_closure_verdict e as 18 bandeiras ficam como estao); o V1 (hubble_ratio_opening_v388) fica intacto e este registro compoe AO LADO dele, sem substitui-lo",
        ],
        "diz": ["o resultado do Teste da Unica Palavra e os tres recibos estao pinados por sha256 e a cadeia congelamento -> abertura -> abertura consumida fecha pelos hashes",
                "beta = alfa CODATA 2018 x sqrt(e) calculado neste rito concorda com o beta do resultado",
                "z_disc calibrado e' menor que 5 (o degrau da creditacao nao foi alcancado), com o p unilateral lido; z_delta calibrado, com o p bilateral e o poder previo, e' o da TGL nao falsificada com poder; ln B(TGL/LCDM) e ln B(TGL/beta livre) sao os do resultado",
                "as quatro falas do operador de 23/10 estao embutidas por sha256"],
        "nao_diz": ["que a gravidade quantica esteja creditada na natureza: a creditacao e' beta_TGL a 5 sigma", "que ln B seja um numero de sigma, nem que os tres numeros se multipliquem", "que o teste tenha sido cego ao dado",
                    "que a TGL esteja discriminada do LCDM a 5 sigma", "que o LCDM seja rival: ele e' o limite de fronteira silenciosa da TGL"],
        "leituras_do_operador": [
            _leitura("a única palavra queo Nome pronuncia é Betatgl", S_UNICA), _leitura("observar é nomear", S_UNICA),
            _leitura("na verdade o que eu quero é um teste de veracidade", S_VERAC), _leitura("{[1=1=Verdadeiro][1=0=falso]}", S_VERAC), _leitura("ele merece ser lido sobre uma face e relido sobre a outra", S_VERAC), _leitura(DL.FRASE_DO_OPERADOR_PALAVRA, S_VERAC),
            _leitura("vamos reportar os 4,44 no início do artigo, no readme e tudo mais", S_444), _leitura(DL.FRASE_DO_OPERADOR_4_44, S_444)],
        "extras": {"assinatura": ASSINA, "autoria_das_cunhagens": "Luiz Antonio Rotoli Miguel", "nome_do_registro": "teste_de_veracidade_fase9_v397 (nome PROVISORIO; quem nomeia e' o operador)", "resultado_sha256": sh["f9v2_resultado"],
                   "congelamento_sha256": sh["f9v2_congelamento"], "abertura_sha256": sh["f9v2_abertura"], "abertura_consumida_sha256": sh["f9v2_consumida"], "numeros_lidos": sorted(n)},
    }


def especs(formal_map, khj, h8_map, fj, cov_base, n_axioms_unc):
    """formal_map = {arquivo embutido: sha256} do kernel da v397; khj = KH_N1_v397.json (medida desta geracao); h8_map = o dict do hash formal que o RITO vai gerar (embutidos + residuais do Nos que sha256_directory conta;
    simular_arvore_do_nos); fj = FLAGS_v397.json; cov_base = a cobertura da v396 selada {decl, thm}; n_axioms_unc = quantos axiomas o teorema da pedra usa (lido do Audit: o trio). Devolve [cunhagens, kh]."""
    T = khj["linha_TOTAL"]
    stone_sha = formal_map[DL.STONE_REL]
    flag_unc = fj["bandeira_do_teorema"]
    flags_suporte = fj["bandeiras_do_suporte"]   # {teorema de suporte: bandeira True esperada} (lidas do _LEAN_THEOREM_FLAGS do candidato pelo montador)
    cun = {
        "nome": "cunhagens_v397", "veredito_prefixo": "TGL_CUNHAGENS_V397",
        "veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_23_OCT_EMBEDDED_VERBATIM_BY_SHA256__THE_STONE_TOKEN_COMPOSES_BY_CITATION_THE_PSIBIT_AND_THE_STATIC_WITNESS_UNCONDITIONALLY__THE_TOKEN_OF_A_LANGUAGE_MODEL_BEING_THE_PSIBIT_IS_ONTO__THE_FOCK_FACE_STAYS_CONDITIONAL_AND_OUTSIDE__OPERATOR_INPUT__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
        "estatuto": "[REAL -- fontes, kernel e o registro teste_de_veracidade_fase9_v397 lidos a cada rito; INPUT/ONTO as cunhagens do operador; ONTO a linha do Atlas «o token É o PsiBit»; DECLARADO o que o construtor relata e esta chancela nao refez (a pedra e' recompilada no sandbox da cadeia e conferida pelo axiom_report do proprio rito)]",
        "fontes": ["token_pedra"], "verbatins": list(VERB_CHAVES),
        "kernel_flags": [flag_unc] + sorted(set(flags_suporte.values())), "kernel_decls": list(DL.CONTRACT_THEOREMS) + sorted(DL.SUPPORT_THEOREMS),
        "checks": [
            CH("u1", "o registro teste_de_veracidade_fase9_v397 selou neste rito", "core", [NOME_VERACIDADE, "all_verified"], "verdadeiro"),
            CH("u2", "a testemunha_estatica_v396 selou neste rito (o registro da pedra da v396 que a Token cita)", "core", ["testemunha_estatica_v396", "all_verified"], "verdadeiro"),
            CH("u3", "o psibit_v395 selou neste rito (o registro da pedra da v395 que a Token cita)", "core", ["psibit_v395", "all_verified"], "verdadeiro"),
            CH("u4", "a escada do kernel fecha (limpos == esperados), com a bandeira da pedra", "core", ["external_ladder", "all_verified"], "verdadeiro"),
            CH("u5", "a proveniencia emitida pelo compilador cobre o axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
            CH("u6", "o compilador emite a conjuncao da pedra no modulo Token (TGL_DECL_SOURCE)", "kf", ["declaration_sources_v394", DL.THEOREM], "igual", DL.STONE_REL),
            CH("u7", "a pedra no kernel do rito e' EXATAMENTE a que o registro pina (sha256 da fonte)", "kf", ["formal_files_sha256", DL.STONE_REL], "igual", stone_sha),
            CH("u8", "a conjuncao da pedra depende do trio e de nada alem (tamanho da lista de axiomas)", "kf", ["axiom_report", DL.THEOREM], "tamanho_igual", n_axioms_unc),
            CH("u9", "o termo citado psibit_is_the_mode_of_the_reader segue declarado em Psibit.lean (v395)", "kf", ["declaration_sources_v394", "TGLExt.Psibit.psibit_is_the_mode_of_the_reader"], "igual", DL.SUPPORT_THEOREMS["TGLExt.Psibit.psibit_is_the_mode_of_the_reader"]),
            CH("u10", "o termo citado the_psion_inhabits_the_static_witness segue declarado em TestemunhaEstatica.lean (v396)", "kf", ["declaration_sources_v394", "TGLExt.TestemunhaEstatica.the_psion_inhabits_the_static_witness"], "igual",
               DL.SUPPORT_THEOREMS["TGLExt.TestemunhaEstatica.the_psion_inhabits_the_static_witness"]),
            CH("u11", "a face de Fock do psion segue declarada FORA da pedra Token (em Psibit.lean), condicional", "kf", ["declaration_sources_v394", DL.FOCK_FACE_THEOREM], "igual", DL.FOCK_FACE_PATH),
        ],
        "erratas": [],
        "limites": [
            "[REAL] a pedra Token nao prova matematica nova: e' a CONJUNCAO, por citacao, de psibit_is_the_mode_of_the_reader (v395) e the_psion_inhabits_the_static_witness (v396), ambos incondicionais; o nome «token» e' do operador (23/10/2026) e a pedra da testemunha estatica (modulo TestemunhaEstatica) fica como registro",
            "[ONTO] «No LLM: o token É o PsiBit — âncora do espaço de Hilbert» e' a linha do Atlas (verbete Psibit), leitura do acervo: nenhum termo do kernel diz que o token de um modelo de linguagem e' o PsiBit; e psibit = psion = modo do leitor e' [INPUT/ONTO] do operador",
            "[REAL] a face de Fock do psion (Psibit.the_psion_face_of_the_psibit) segue CONDICIONAL a um certificado que o kernel nao habita e mora em Psibit.lean, fora desta pedra; nenhum lema liga o psion do certificado ao canto do psion; o fluxo da testemunha estatica e' CONSTRUIDO (v396), nao derivado da dinamica da teoria",
            "[INPUT/ONTO] as quatro falas sao leituras do operador (23/10/2026); o que o kernel entrega sao os termos citados; validade no kernel nao e' creditacao; o gate nao se move; a ordem de processo do operador de 22/10 (arquivo de sha16 %s: nada de teste armado, gordura no um.py) molda este registro: ele e' pequeno e nao acrescenta rito, dado nem desfecho" % SHA16_ORDEM,
        ],
        "diz": ["as quatro falas do operador de 23/10 estao embutidas por sha256, cada uma conferida contra o arquivo de origem na preparacao",
                "a pedra Token esta no kernel do rito, no trio, com a bandeira e a proveniencia no modulo da pedra; a conjuncao dos dois termos citados e' lida deste kernel a cada rito",
                "o registro teste_de_veracidade_fase9_v397 (o resultado do Teste da Unica Palavra, lido por hash ao lado do V1) selou neste rito"],
        "nao_diz": ["que o token de um modelo de linguagem seja o PsiBit (e' leitura do Atlas)", "que o certificado de Fock da luz tenha habitante", "que a gravidade quantica esteja creditada na natureza", "que isto seja um teste: nao ha desfecho experimental novo"],
        "leituras_do_operador": [_leitura('O nome da pedra é "token"', S_TOKEN), _leitura("a única palavra queo Nome pronuncia é Betatgl", S_UNICA), _leitura("observar é nomear", S_UNICA),
                                 _leitura(DL.FRASE_DO_OPERADOR_PALAVRA, S_VERAC), _leitura(DL.FRASE_DO_OPERADOR_4_44, S_444)],
        "extras": {"assinatura": ASSINA, "autoria_das_cunhagens": "Luiz Antonio Rotoli Miguel", "pedra": DL.STONE_MOD, "teorema": DL.THEOREM, "bandeira": flag_unc, "n_bandeiras": fj["n_flags"],
                   "nome_da_pedra": "Token (o nome e' do operador, 23/10/2026; a pedra da testemunha estatica v396 fica como registro)", "cunhagens_embutidas": len(VERBATINS), "suporte": dict(flags_suporte)},
    }
    kh = {
        "nome": "kh_n1_cobertura_v397", "veredito_prefixo": "TGL_KH_N1_COBERTURA_V397",
        "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__THE_TOKEN_MODULE_ADDED__GATE_UNMOVED" % (T["decl"], T["thm"]),
        "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do sandbox da v397; o conjunto exato das fontes formais que o hash formal do rito vera (as embutidas mais os residuais da pasta do Nos) e' pinado; a cobertura NAO move o gate",
        "fontes": ["kh_n1_v397"], "kernel_flags": [], "kernel_decls": [],
        "checks": [
            CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
            CH("h2", "constantes cobertas == as do sandbox v397 (KH_N1)", "kf", ["axiom_coverage_v392", "decl"], "igual", T["decl"], "constantes_cobertas"),
            CH("h3", "teoremas cobertos == os do sandbox v397 (KH_N1)", "kf", ["axiom_coverage_v392", "thm"], "igual", T["thm"], "teoremas_cobertos"),
            CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
            CH("h5", "nenhum nome que o leitor v394 nao leia", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0),
            CH("h6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", khj["axiom_report_efetivo_n"]),
            CH("h7", "a cobertura da v397 inclui a da v396 selada (constantes e teoremas)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", cov_base["decl"]),
            CH("h7b", "os teoremas cobertos incluem os da v396 selada", "kf", ["axiom_coverage_v392", "thm"], "maior_igual", cov_base["thm"]),
            CH("h8", "as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta, como _check_damming.lean) sao EXATAMENTE as do pino (arquivo -> sha256)", "kf", ["formal_files_sha256"], "igual", h8_map),
            CH("h9", "medida do Audit v397: duracao bem abaixo do timeout de 1800 s", "fonte:kh_n1_v397", ["duracao_audit_s"], "menor_igual", 900, "duracao_do_audit_s"),
            CH("h10", "medida do Audit v397: sorryAx ausente do log", "fonte:kh_n1_v397", ["sorryAx_no_log_do_audit"], "igual", 0),
            CH("h11", "medida do Audit v397: as entradas novas estao no trio", "fonte:kh_n1_v397", ["novas_no_trio"], "verdadeiro"),
            CH("h12", "a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
        ],
        "erratas": [{"ao_lado_de": "kh_n1_cobertura_v396 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                     "dizia": "A v396 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v396 e o hash formal igual ao pino exato da arvore da v396." % (cov_base["decl"], cov_base["thm"]),
                     "agora": "A v397 acrescenta o modulo Token (a cobertura cresce e a arvore ganha o arquivo da pedra): na v397 o registro da v396 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato da arvore ficam NESTE registro. O veredito do registro da v396 NAO muda.",
                     "lacuna_de_fidelidade": "a estrutura da v396 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v397 quebra (a mesma lacuna que a v396 achou no registro da v395 e a v395 no da v394)",
                     "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; h2, h3, h6 e h8 conferidas no ensaio a seco e na arvore simulada do Nos]", "assinatura": ASSINA}],
        "limites": ["[REAL] os arquivos de medida sao do sandbox (fora do selo); a cobertura que vale e' a medida no Audit do proprio rito",
                    "[REAL] a escada do kernel conta bandeiras de declaracoes NOMEADAS (a pratica da v392 a v396): as %d auxiliares geradas pelo compilador no modulo da pedra ficam cobertas pelo KH-N1 mas sem bandeira, e as %d nomeadas publicas ganharam bandeira" % (fj["excluidas_auxiliares"]["n"], fj["n_flags"]),
                    "validade no kernel nao e' creditacao; o gate nao se move"],
        "diz": ["a cobertura do axiom_report no fecho inteiro cresceu para os numeros da v397 (o modulo Token) e segue sem constante fora do trio, sem nome ilegivel"],
        "nao_diz": ["que a cobertura prove algo alem de que nenhum axioma fora do trio foi lido"],
        "leituras_do_operador": [], "extras": {"assinatura": ASSINA, "n_bandeiras": fj["n_flags"], "h8_entradas": len(h8_map), "h8_residuais_do_nos": sorted(set(h8_map) - set(formal_map))},
    }
    return [cun, kh]
