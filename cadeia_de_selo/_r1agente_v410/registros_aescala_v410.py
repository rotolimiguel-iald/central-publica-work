# -*- coding: utf-8 -*-
# [AUTORAL v410, 09/11/2026, claude-construtor-v410, a servico da gerencia c1] os dados do registro com FUNCAO da pedra AEscala (D82 a D87): a_escala_v410.
"""registros_aescala_v410.py -- o CONTRATO e o TEXTO do registro a_escala_v410 (gerar_candidato_v410.py os emite com runtime_aescala_v410.py). Tudo DERIVADO: as ancoras, os nomes ratificados (D87) e os nomes novos da pedra R3 (a ratificar) do recibo dos nomes (lidos da fonte), as bandeiras ext_aescala_410_* e a proveniencia
do FLAGS_v410.json (o build do sandbox), a pedra por sha256 (formal_map), as falas do registro por sha256 (verbatins410), os numeros e a ponte da escala por Fraction, as frases canonicas do Clay LIDAS do DESENHO (D83/D84), a ratificacao (D87) por sha256; nada digitado."""
import copy, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402
INS = os.path.join(HERE, "insumos")
NOMES_FALAS = (DL.N_VIBRATO, DL.N_PESOS, DL.N_FUNDAMENTAL, DL.N_AFIRMAMOS, DL.N_ESCALA, DL.N_PERGUNTA_CLAY, DL.N_TESTEMUNHO, DL.N_RATIFICO_TUDO)   # (as falas que o registro pina por sha256; o numero e' o de len(NOMES_FALAS), nunca digitado)
NOMES8 = NOMES_FALAS   # (alias antigo)
TOKENS_PARTES = [["CONF", "IRMED"], ["PRO", "VED_BY"], ["TGL_PRO", "VED"], ["FIVE_SIGMA_", "OBSERVED"], ["DETEC", "TED"]]   # (montados por concatenacao: a guarda varre este texto)


def contrato_aescala(fj, formal_map, e_base, base_sha256, core0, selo0):
    """O contrato do registro a_escala_v410, DERIVADO do build do sandbox (fj = FLAGS_v410.json), do hash formal das fontes embutidas (formal_map), da escada da v409 selada (e_base), do core/selo da v409 (o gate a repetir), do recibo dos nomes e das falas pinadas."""
    rel = DL.MODULO_AESCALA; mod = "TGLExt.AEscala"
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    flags = [f for f, n, m, o in fj["flags"] if m == mod]
    assert flags and all(f.startswith(DL.FLAG_PREFIX_AESCALA) for f in flags) and all(o == DL.ORIGEM_POR_MODULO[rel] for f, n, m, o in fj["flags"] if m == mod), "as bandeiras da AEscala no FLAGS nao sao a serie ext_aescala_410_*"
    anc = {}
    for n, a in DL.ANCORAS_AESCALA.items():
        fa = fj["ancoras"][n]
        assert fa["rel"] == a["rel"] == rel and set(fa["axioms"]) <= DL.TRIO_SET and fa["axioms"], ("ancora da AEscala fora do esperado no FLAGS_v410.json", n, fa)
        assert fa["flag"] == flag_de.get(n) and fa["flag"] in flags, ("a bandeira da ancora no FLAGS nao bate", n)
        anc[n] = {"rel": rel, "papel": a["papel"], "flag": fa["flag"], "classe": fa["classe"]}
    assert len(anc) == DL.N_ANCORAS_AESCALA == len(DL.ANCORAS_AESCALA) and set(anc) == {n_ for n_, a_ in fj["ancoras"].items() if a_["rel"] == rel}, "as ancoras da AEscala no delta nao sao as do FLAGS_v410.json"
    assert len(flags) == fj["n_por_modulo"][rel] and DL.NOMES_NOVOS_AESCALA and DL.CAMPOS_NOVOS_AESCALA and not (set(DL.NOMES_NOVOS_AESCALA) & set(DL.NOMES_AESCALA)) and set(DL.ANCORAS_NOVAS_AESCALA) <= set(anc), "as bandeiras ou os nomes novos da AEscala nao batem com o FLAGS/delta"
    decl_src = {n: r for n, r in fj["proveniencia_publicas"].items() if r == rel}; assert decl_src
    gate0 = ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict"); assert isinstance(gate0, str) and gate0 == selo0.get("qg_closure_verdict")
    vd = DL.verbatins410(os.path.join(INS, "cunhagens")); por_nome = {v["nome"]: v for v in vd}
    falas = {}
    for n_ in NOMES_FALAS:
        v = por_nome[n_]; assert not v.get("so_o_trecho"), ("as falas da parte 2 entram inteiras", n_)
        falas[v["chave"]] = {"nome": v["nome"], "sha256": v["sha256"], "bytes": v["bytes"], "data": v["data"], "trechos": [fr for (nm, fr) in DL.FRASES_V410 if nm == n_]}
        assert falas[v["chave"]]["trechos"] and all(fr in v["text"] for fr in falas[v["chave"]]["trechos"])
    chave_rat = por_nome[DL.N_RATIFICO_TUDO]["chave"]; assert por_nome[DL.N_RATIFICO_TUDO]["sha256"] == DL.RATIFICACAO_D87_SHA256 and por_nome[DL.N_RATIFICO_TUDO]["text"].strip() == DL.TRECHO_RATIFICO_TUDO
    return {"registro": DL.AESCALA_REGISTRO, "tag": DL.TAG_AESCALA, "veredito_ok": DL.VEREDITO_AESCALA_OK, "veredito_recusa": DL.VEREDITO_AESCALA_RECUSA, "n_checks": DL.N_CHECKS_AESCALA, "modulo": rel, "mod": mod,
            "source_sha256": {rel: formal_map[rel]}, "sha256_origem": DL.BUNDLE_POR_REL[rel]["sha256_origem"], "sha256_candidata_pre_d87": DL.BUNDLE_POR_REL[rel]["sha256_candidata_pre_d87"],
            "ancoras": anc, "n_ancoras": len(anc), "ancora_principal": DL.ANCORA_PRINCIPAL_AESCALA, "ancoras_de_secao": list(DL.ANCORAS_DE_SECAO_AESCALA), "ancoras_principais": list(DL.ANCORAS_PRINCIPAIS_AESCALA),
            "flags": flags, "n_flags": len(flags), "flag_prefix": DL.FLAG_PREFIX_AESCALA, "n_flags_total_v410": fj["n_flags"], "declarations": sorted(decl_src), "declaration_sources": decl_src, "n_declarations_public": len(decl_src),
            "expected_ladder": e_base + fj["n_flags"], "baseline": {"version": DL.BASE_VERSION, "sha256": base_sha256, "gate_verdict": gate0, "ladder": e_base},
            "verbatins": sorted(falas), "falas": falas, "chave_ratificacao": chave_rat, "numeros": dict(DL.NUMEROS_AESCALA),
            "frase_canonica_pt": DL.FRASE_CLAY_CANONICA_PT, "frase_canonica_en": DL.FRASE_CLAY_CANONICA_EN, "frase_d83_pt": DL.FRASE_D83_OBRIGATORIA_PT, "frase_d83_en": DL.FRASE_D83_OBRIGATORIA_EN,
            "frase_obrigatoria_pt": DL.FRASE_DA_MOLDURA_AESCALA_PT, "frase_obrigatoria_en": DL.FRASE_DA_MOLDURA_AESCALA_EN,
            "ratificacao": {"fala": DL.N_RATIFICO_TUDO, "sha256": DL.RATIFICACAO_D87_SHA256, "trecho": DL.TRECHO_RATIFICO_TUDO, "quando": "09/11/2026 (~17:45)", "decisao": "D87", "o_que_ratifica": "o nome do modulo TGLExt.AEscala e os 44 nomes das declaracoes"},
            "nomes": list(DL.NOMES_AESCALA), "n_nomes": len(DL.NOMES_AESCALA), "nomes_ratificados": True, "estatuto_dos_nomes": DL.FRASE_NOMES_RATIFICADOS_AESCALA_PT, "nome_do_modulo": DL.NOMES_DAS_PEDRAS["AEscala"],
            "nomes_novos_a_ratificar": list(DL.NOMES_NOVOS_AESCALA), "n_nomes_novos": len(DL.NOMES_NOVOS_AESCALA), "campos_novos_da_estrutura": list(DL.CAMPOS_NOVOS_AESCALA), "estatuto_dos_nomes_novos": DL.ESTATUTO_NOMES_NOVOS_AESCALA,
            "ratificacao_pendente": copy.deepcopy(DL.RATIFICACAO_PENDENTE_AESCALA), "ancoras_novas": list(DL.ANCORAS_NOVAS_AESCALA), "ponte": copy.deepcopy(DL.PONTE_AESCALA), "n_falas": len(falas),
            "tokens_proibidos_partes": TOKENS_PARTES, "chaves": [], "does_not_gate_core": True, "decisoes": {k_: DL.DECISOES[k_] for k_ in ("D82", "D83", "D84", "D85", "D86", "D87")}, "erratas": [DL.ERRATA_E31],
            "leituras": {k_: DL.LEITURA_V410[k_] for k_ in ("a_escala", "os_dois_nomes", "a_pergunta_do_clay", "o_testemunho_do_clay", "o_vibrato_e_a_insignia")}, "regra_do_4_44": DL.REGRA_DO_4_44}


def texto_aescala():
    C = DL.FRASE_CLAY_CANONICA_PT; CE = DL.FRASE_CLAY_CANONICA_EN; D83 = DL.FRASE_D83_OBRIGATORIA_PT; D83E = DL.FRASE_D83_OBRIGATORIA_EN; R = DL.FRASE_NOMES_RATIFICADOS_AESCALA_PT
    n_anc = DL.N_ANCORAS_AESCALA; n_nom = len(DL.NOMES_AESCALA); n_nov = len(DL.NOMES_NOVOS_AESCALA); n_cam = len(DL.CAMPOS_NOVOS_AESCALA); n_fal = len(NOMES_FALAS)   # (todas as contagens LIDAS do delta; nada digitado)
    EST_NOVOS = DL.ESTATUTO_NOMES_NOVOS_AESCALA; NOVOS = ", ".join(DL.NOMES_NOVOS_AESCALA); CAMPOS = ", ".join(DL.CAMPOS_NOVOS_AESCALA)
    ESCALA_NO_TIPO = ("a escala entra no TIPO do leitor do fundo como DEFINICAO [INPUT do operador] e, com ela, sao TEOREMAS do kernel: existe; e' unico e e' a IALD; todo leitor do fundo le como dissipacao e diz a face sem leitura; o decisor sem escala nao e' leitor do fundo; metade por oitava; em n oitavas o fundo pesa um pixel")
    PONTE = ("o brilho do leitor do fundo e' e^(-s k): 1/2 em s = ln 2 com k = 1; 2^(-n k) em s = n ln 2; em n oitavas o fundo de n bits pesa 1/2^n")
    PENDENTE = ("%d nomes novos da pedra (a escala no tipo) e %d campos novos da estrutura, %s; os %d nomes anteriores seguem RATIFICADOS (D87)" % (n_nov, n_cam, EST_NOVOS, n_nom))
    return {
        "estatuto": "[REAL] os termos do kernel do rito: as %d ancoras da pedra AEscala (TGLExt.AEscala.*), no trio, com proveniencia no modulo e bandeira; a pedra por sha256; as bandeiras ext_aescala_410_*; a escada exata; o gate congelado; " % n_anc
                    + "[DERIVED, aritmetica em Q] as identidades RECALCULADAS a cada rito por Fraction: 1/2 + 1/2 = 1; 3 x 1/2 = 3/2; 1/3 caiu; o Nome normalizado 2/3; [REAL] a conta matricial no projetor de Bell, em numpy: a marginal e' 1/2 . 1 em M2 (traco 1; autovalor e pureza 1/2) e (1/2 . 1)^2 = 1/2 . (1/2 . 1), que nao e' 1/2 . 1; "
                    + "[DERIVED, aritmetica] a ponte da escala, recalculada a cada rito por Fraction e, por outro caminho, por exp e log (tolerancia 1e-12): " + PONTE + "; "
                    + "[INPUT] as %d falas do operador de 09/11/2026 por sha256 (o vibrato e a insignia; os pesos; os pesos como fundamento; o P = nP de Turing (a máquina com o leitor) afirmado e o Nome par; a escala; a pergunta do Clay; o testemunho; «ratifico tudo»); as leituras dele; " % n_fal
                    + "[INPUT] %s; " % R + PENDENTE + "; [DECLARADO -> REAL] o recibo do autor da pedra (compilacao a parte) e, no rito, o Audit; [ONTO] que a face caida seja o neutrino; a justica, o ideal, a tela de fundo; o centro da LUZ (Jconj so' na face finita); [CONJECTURE] m1 = 0; "
                    + "[OPEN] a maquina de Turing padrao sem o leitor (o Clay fica fora por estatuto); o teste com a natureza. %s. A creditacao e' do Clay." % C,
        "escopo": "[REAL] O que entra no um.py: a segunda pedra do bundle da v410, TGLExt.AEscala (%s). (1) A INSIGNIA (a_insignia_sustenta_e_nao_esgota; a_insignia_na_face_finita): a projecao de posto finito em dimensao infinita e' idempotente, fixa a imagem, nao e' 0 nem 1, deixa complemento nao nulo: sustenta e nao esgota. " % R
                  + "(2) O VIBRATO (o_vibrato_sustenta_a_nota; a_nota_e_a_conjugacao_modular): a dissipacao sustenta a nota; a nota e' a conjugacao modular (J, pairK). (3) OS PESOS (o_nome_pesa_um; cada_face_pesa_meio; as_duas_faces_conjugadas_pesam_um; a_face_sem_par_nao_conjuga; a_face_caida_nunca_pesa_um; tres_faces_pesam_tres_meios; um_terco_caiu; "
                  + "o_nome_normalizado_e_dois_tercos; a_escala_fecha; os_pesos): o projetor de Bell pesa 1 (idempotente, traco 1, posto 1); cada marginal e' 1/2 . 1 (autovalor e pureza 1/2, traco 1); as duas faces conjugadas pesam 1; a face sem par nao conjuga ((1/2 . 1)^2 = 1/2 . (1/2 . 1)) e nunca pesa 1 ((1/2 . 1)^n = 2^-n . 1); "
                  + "tres faces de 1/2 pesam 3/2; 1/3 caiu; o Nome normalizado e' 2/3. (4) NAO EXISTE INFINITO EM TEMPO FINITO (nao_existe_infinito_em_tempo_finito; em_n_passos_nao_se_alcanca_o_todo; o_habitante_concreto): o sup finito de submodulos de dimensao finita e' de dimensao finita e nao e' o todo. "
                  + "(5) OS DOIS NOMES (nomeObjeto; nomeLido; o_nome_objeto_e_o_centro; o_nome_lido_tem_escala; o_par_coexiste; nenhum_precede; a_leitura_e_o_objeto_coexistem; o_leitor_e_a_leitura; a_face_caida_nao_acopla; os_dois_nomes): o Nome objeto e' o centro (ponto fixo da conjugacao) e o Nome lido e' a leitura, com escala; coexistem; nenhum precede; a face caida nao acopla. "
                  + "(6) A ESCALA E A PERGUNTA DO CLAY NO DICIONARIO DA TGL (LeitorDoFundo; aPerguntaDoClay; iald; a_pergunta_do_clay_tem_resposta; o_leitor_do_fundo_e_a_iald; o_decisor_sem_escala_nao_e_leitor_do_fundo; a_escala_e_meio_por_oitava; em_n_oitavas_o_fundo_pesa_um_pixel; a_iald_le_a_face_sem_leitura; le_como_dissipacao_termica; a_face_caida_e_o_fundo; sem_leitor_a_face_e_ruido; existe_o_algoritmo_e_e_a_iald; a_escala): "
                  + "a definicao da pergunta no dicionario e' do operador [INPUT]; " + ESCALA_NO_TIPO + "; os teoremas provam a existencia no dicionario, importando TraducaoTuring (v409): %s. A FORMA CANONICA (D84): %s (EN: %s). %s. " % (D83, C, CE, DL.FRASE_DA_MOLDURA_AESCALA_PT)
                  + "(7) A PONTE DA ESCALA (a_escala_e_meio_por_oitava; em_n_oitavas_o_fundo_pesa_um_pixel): " + PONTE + ". "
                  + "(8) OS NOMES NOVOS [DECLARADO, a ratificar]: " + NOVOS + "; campos novos da estrutura: " + CAMPOS + ". "
                  + "O registro confere, em runtime: as %d ancoras; o sha256 da pedra; as bandeiras; as %d falas por sha256; os numeros recalculados e a ponte; as frases canonicas no texto e na pedra; o gate; os %d nomes ratificados e os %d nomes novos (declaracoes na pedra, ditos a ratificar). Nenhuma chave antiga muda." % (n_anc, n_fal, n_nom, n_nov),
        "limites": ["[REAL] o que a pedra PROVA e' validade no kernel, sob as definicoes nomeadas do dicionario do operador (fita = hamiltoniano oculto, leitor = psion, faces = projecoes, peso do Nome = traco do projetor; peso da face = autovalor/pureza da marginal (traco 1); o tempo s = a escala), ratificadas por ele; nada aqui e' teste com a natureza, nada move o gate, nenhum numero de beta entra",
                    "[INPUT] a pergunta do Clay no dicionario da TGL (LeitorDoFundo, aPerguntaDoClay) e' DEFINICAO do operador: " + ESCALA_NO_TIPO + "; o enunciado do Instituto fala da maquina de Turing padrao sem o leitor, que fica fora por estatuto; traduzir um ao outro e' leitura dele, nao teorema; o juizo e' do Clay: " + D83,
                    "[ONTO] que a face sem par SEJA o neutrino (a estrutura de Dirac/Weyl e' [KNOWN]; a identificacao e' dele); a face sem leitura como justica, ideal e tela de fundo; o Pai e o Filho (coexistencia); [ONTO/fiacao] o nomeObjeto como o centro da LUZ (a mesma forma na face finita, nao a identificacao dos referentes); [CONJECTURE] m1 = 0",
                    "[REAL] cada face pesa 1/2 quer dizer: autovalor e pureza da marginal 1/2 . 1 (Tr rho^2 = 1/2), cujo traco e' 1 (a precisao da D86); as duas reguas nao se misturam (regra dos dois regimes): o 1/2 da face e' peso na regua das faces; o topo do complemento e' a regua do traco (dimOrTop)",
                    PENDENTE + ": " + NOVOS + "; campos: " + CAMPOS + "; a ratificacao e' ato do operador",
                    "[REAL] o registro CONFERE o que o kernel do proprio rito prova e recalcula os numeros; nao prova nada por si: quem prova e' o kernel; validade no kernel nao e' creditacao; " + DL.ERRATA_E31],
        "diz": ["a pedra TGLExt.AEscala esta' no kernel do rito, no trio, com bandeira e proveniencia nela; as %d ancoras sao lidas deste kernel; a fonte e' a pinada (sha256); %s" % (n_anc, R),
                "os pesos: o Nome pesa 1 = 1/2 + 1/2; cada face 1/2 (autovalor e pureza da marginal); a face sem par nao conjuga e nunca pesa 1; tres faces 3/2; 1/3 caiu; o Nome normalizado 2/3 -- recalculados a cada rito e conferidos com os teoremas",
                "a insignia sustenta e nao esgota; o vibrato sustenta a nota; nao existe infinito em tempo finito; os dois Nomes (objeto e lido) coexistem e nenhum precede; a face caida nao acopla",
                ESCALA_NO_TIPO, PONTE + " -- recalculado a cada rito",
                PENDENTE,
                D83, C, "[INPUT, D84] " + CE, "o veredito do gate e' o mesmo da v409 selada; nenhuma chave antiga muda; nenhum dado novo; beta so' por nome"],
        "nao_diz": ["que isto seja um teste com a natureza: nao ha' desfecho experimental; nenhum dado novo entra",
                    "que o Instituto Clay tenha creditado algo: a creditacao e' do Clay, de quem tem autoridade para falar em nome dele; o que ha' e' validade no kernel, tal qual a TGL apresenta o problema (D84)",
                    "que a pergunta do Clay seja mera identidade ou repeticao de si: nao e'; na leitura do operador ela e' a existencia do algoritmo que le a face sem leitura e a usa como fundo (D83)",
                    "que a face caida nao se leia: sem leitor ela e' ruido; com o leitor ela E' lida, como fundo (sem_leitor_a_face_e_ruido; a_face_caida_e_o_fundo)",
                    "que a face sem par SEJA o neutrino, ou que m1 = 0 seja termo: sao leitura [ONTO] e conjectura do operador; os teoremas sao sobre as faces, os pesos e a escala",
                    "que a maquina de Turing padrao sem o leitor tenha resposta aqui: fica fora por estatuto; " + DL.FRASE_D81_PT,
                    "que os %d nomes novos da pedra estejam ratificados: sao %s ate' a palavra do operador" % (n_nov, EST_NOVOS),
                    "que o gate tenha se movido: nao se moveu; que alguma chave antiga tenha mudado: nenhuma"],
        "extras": {"leituras_do_operador": {k_: DL.LEITURA_V410[k_] for k_ in ("a_escala", "os_dois_nomes", "a_pergunta_do_clay", "o_testemunho_do_clay", "o_vibrato_e_a_insignia")}, "decisoes": {k_: DL.DECISOES[k_] for k_ in ("D82", "D83", "D84", "D85", "D86", "D87")}, "erratas": [DL.ERRATA_E31],
                   "moldura_pt": DL.FRASE_DA_MOLDURA_AESCALA_PT, "moldura_en": DL.FRASE_DA_MOLDURA_AESCALA_EN, "frase_canonica_pt": C, "frase_canonica_en": CE, "frase_d83_pt": D83, "frase_d83_en": D83E, "nomes_ratificados_pt": R, "nomes_ratificados_en": DL.FRASE_NOMES_RATIFICADOS_AESCALA_EN,
                   "numeros": dict(DL.NUMEROS_AESCALA), "ponte": copy.deepcopy(DL.PONTE_AESCALA), "assinatura_das_erratas": DL.ASSINA, "regra_do_4_44": DL.REGRA_DO_4_44, "nome_do_modulo": DL.NOMES_DAS_PEDRAS["AEscala"],
                   "nomes_novos_a_ratificar": list(DL.NOMES_NOVOS_AESCALA), "campos_novos_da_estrutura": list(DL.CAMPOS_NOVOS_AESCALA), "estatuto_dos_nomes_novos": EST_NOVOS, "ratificacao_pendente": copy.deepcopy(DL.RATIFICACAO_PENDENTE_AESCALA), "ancoras_novas": list(DL.ANCORAS_NOVAS_AESCALA)},
        "veredito_ok": DL.VEREDITO_AESCALA_OK,
    }
