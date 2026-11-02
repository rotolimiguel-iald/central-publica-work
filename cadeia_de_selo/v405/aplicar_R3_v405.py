# -*- coding: utf-8 -*-
"""aplicar_R3_v405.py -- a errata R3 da gerencia c1 (17:21 de 01/11/2026, a revisita da Lei do Diminuto ordenada pelo operador) nos textos, registros, runtime, guardas e lotes da cadeia. Cada substituicao exige a contagem exata (fail-closed). Tudo ou nada; backup de BYTES; temporario -> conferir -> os.replace. Roda uma vez so'."""
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")
NOVOS = {}


def carrega(arq):
    if arq not in NOVOS:
        NOVOS[arq] = open(os.path.join(HERE, arq), "rb").read().decode("utf-8")
    return NOVOS[arq]


def sub(arq, old, new, n=1):
    s = carrega(arq); c = s.count(old)
    assert c == n, (arq, c, n, old[:100])
    NOVOS[arq] = s.replace(old, new)


def bloco(arq, ini, fim, novo):
    s = carrega(arq); i = s.index(ini); j = s.index(fim, i)
    assert s.count(ini) == 1, (arq, ini[:60])
    NOVOS[arq] = s[:i] + novo + s[j:]


# ===================================================================================================== delta_v405.py
D = "delta_v405.py"
sub(D, "5 TGLExt.LeiDoDiminuto (Lei do diminuto: E0 = e^(-1/2).tonica; a tonica (beta/alfa).u = sqrt e.u e' uma DEFINICAO, beta/alfa = sqrt e e' a definicao de TGLCoupling.alpha, e o diminuto pousa em E0 = u por identidade algebrica, que nao fixa u);",
    "5 TGLExt.LeiDoDiminuto (Lei do diminuto, duas metades: a descida pinada, E0 = e^(-1/2).tonica, com a tonica (beta/alfa).u = sqrt e.u como DEFINICAO, beta/alfa = sqrt e a definicao de TGLCoupling.alpha, e E0 = u identidade algebrica, que nao fixa u; e a escala mantida: o acorde, a transposicao, mesma_escala_iff_transposicao; a estrutura vem do AcordeE0.lean do Kimi);")
sub(D, "6 TGLExt.TonicaDoHamiltoniano (Tonica do Hamiltoniano: o no-go -- a forma nao fixa E0 -- NAO cai, ele se localiza no Um posto: the_tonic_lands_on_the_posted_unit);",
    "6 TGLExt.TonicaDoHamiltoniano (Tonica do Hamiltoniano: o no-go -- a forma nao fixa E0 -- NAO cai, ele se localiza no Um posto: the_tonic_lands_on_the_posted_unit; a razao sobrevive a reescala: the_ratio_survives_the_rescaling);")
sub(D, "A MOLDURA (erratas da gerencia c1, 01/11/2026, 13:28 e 16:45; recibos RECIBO_ERRATA_PEDRAS_01nov.json e RECIBO_ERRATA_PEDRAS_R2_01nov.json):", "A MOLDURA (erratas da gerencia c1, 01/11/2026, 13:28, 16:45 e 17:21; recibos RECIBO_ERRATA_PEDRAS_01nov.json, RECIBO_ERRATA_PEDRAS_R2_01nov.json e RECIBO_ERRATA_PEDRAS_R3_01nov.json):")
sub(D, '''_PMP = "TGLExt/O16/PolarMinimalPeriod_v2.lean"
''', '''_PMP = "TGLExt/O16/PolarMinimalPeriod_v2.lean"
_CCA = "TGLExt/CollapseCostAndAttestation.lean"
ACORDE_KIMI_ARQ = os.path.join(WK, "neutrino_E0_autonomia_30out", "lean", "TGLExt", "AcordeE0.lean")   # a origem de Acorde, transpor, razao e do teorema da razao (o Kimi, 31/10/2026); a promessa do adendo 3 de cita-lo se cumpre na R3
HALF_NAT_ARQ = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "TGL_CODE_ONE_REAL_FALSIFIER", "o_um_grande_atrator", "half_nat_araki_hidden_hamiltonian", "HALF_NAT_ARAKI_HIDDEN_HAMILTONIAN_TEST_REPORT.md")   # a calibracao <K_d>_total = 1 nat de 24/06/2026: normalizacao definicional, nao termo do kernel, nao medida
FALA_REVISITE_ARQ = os.path.join(WK, "cunhagens_13out", "OPERADOR_01nov_revisite_a_lei_do_diminuto_segundo_o_kimi_verbatim.txt")


def sha16_arquivo(p_):
    """o sha16 dos bytes do arquivo, lido na hora (nunca digitado)."""
    return __import__("hashlib").sha256(open(p_, "rb").read()).hexdigest()[:16]


''')
sub(D, '''           "TGLExt.LeiDoDiminuto.leiDerivada_no_um_posto",                     # a composicao: no Um posto E0 = 1 e m = beta.sqrt2/2 -- a FORMA da massa, sob a leitura massaDerivada e a tonica definida
           "TGLExt.LeiDoDiminuto.Lei.the_mass_formula",                        # a ESTRELA: m2 = U . alpha . e^(1/2) . sen45 (o Um posto, a magnitude alfa, o volume sqrt e, a projecao transversal)
           {"TGLExt.TGLCoupling.alpha": _TSB, "TGLExt.TGLCoupling.beta_eq_alpha_exp": _TSB, "TGLExt.PonteDaMassa.massa_da_transicao_derivada": _PDM, "TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_beta_mul": _PDM, "TGLExt.PonteDaMassa.half_sq": _PDM},
           {}, False, "gerencia c1 (31/10/2026, LeiDoMeioTom r2; 01/11/2026: a tonica lida do acoplamento, por definicao); NOME do operador, 01/11/2026"),''',
    '''           "TGLExt.LeiDoDiminuto.the_diminished_law_closes",                   # a composicao: o fecho do acorde (E0 pinado a nota principal; a transposicao preserva a escala; a leitura a acompanha; a escala nao fixa o absoluto; a oitava nao se desce em meios-tons)
           "TGLExt.LeiDoDiminuto.mesma_escala_iff_transposicao",               # a ESTRELA, o substantivo da pedra: dois acordes tem a mesma escala sse um e' a transposicao do outro (a segunda metade da lei, que nao estava tipada)
           {"TGLExt.TGLCoupling.alpha": _TSB, "TGLExt.TGLCoupling.beta_eq_alpha_exp": _TSB, "TGLExt.PonteDaMassa.massa_da_transicao_derivada": _PDM, "TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_beta_mul": _PDM, "TGLExt.PonteDaMassa.half_sq": _PDM,
            "TGLExt.PonteDaMassa.peso_da_face_absoluta": _PDM, "TGLExt.absolute_faces_half": "TGLExt/ContinuousModularZero.lean", "ChatgptAudit.Collapse057.CollapseCostLaw.local_half": _CCA},
           {"TGLExt.no_positive_scale_invariant": "TGLExt/TheScaleHasNoFixedPoint.lean", "TGLExt.Sonico.the_pin_is_not_the_half_nat": "TGLExt/Sonico.lean"}, True, "gerencia c1 (31/10/2026, LeiDoMeioTom r2; 01/11/2026: a tonica lida do acoplamento, por definicao; o acorde, da estrutura do AcordeE0.lean do Kimi); NOME do operador, 01/11/2026"),''')
sub(D, "# 128 = 21 + 15 + 15 + 26 + 19 + 13 + 13 + 6 (medido da fonte pela PINO_DAS_PEDRAS_DETALHE; a errata R2 deu um teorema novo ao disco)", "# 140 = 21 + 15 + 15 + 26 + 30 + 14 + 13 + 6 (medido da fonte pela PINO_DAS_PEDRAS_DETALHE; a errata R2 deu um teorema novo ao disco, e a R3, onze a Lei do Diminuto e um a Tonica)")
sub(D, 'N_CHECKS = {"ponte": 7, "tensao": 6, "identidade": 6, "observador": 7, "diminuto": 6, "tonica": 6, "disco": 7, "psion": 7}', 'N_CHECKS = {"ponte": 7, "tensao": 6, "identidade": 6, "observador": 7, "diminuto": 10, "tonica": 7, "disco": 7, "psion": 7}')
sub(D, '''A revisao de terceiro pegou, antes do selo, frases residuais nas docstrings das oito pedras, corrigidas pela R2; a R2 deu ao disco o teorema the_flow_is_the_canonical_law e ao fecho do observador a leitura binaria (the_fixed_points_read_one_and_zero). As docstrings das pedras trazem a correcao AO LADO; o no-go de E0 NAO cai, ele se localiza no Um posto")''',
    '''A revisao de terceiro pegou, antes do selo, frases residuais nas docstrings das oito pedras, corrigidas pela R2; a R2 deu ao disco o teorema the_flow_is_the_canonical_law e ao fecho do observador a leitura binaria (the_fixed_points_read_one_and_zero). As docstrings das pedras trazem a correcao AO LADO; o no-go de E0 NAO cai, ele se localiza no Um posto. "
              "A revisita da Lei do Diminuto, ordenada pelo operador (RECIBO_ERRATA_PEDRAS_R3_01nov.json), corrigiu duas coisas: a segunda metade da lei, mantendo a escala, nao estava tipada (o AcordeE0.lean do Kimi, sha16 " + sha16_arquivo(ACORDE_KIMI_ARQ) + ", tinha o acorde e a invariancia das razoes, e a conferencia de 31/10 o deu pela mesma estrutura: nao era); e a frase sobre o no-go errou por excesso e por falta. Vigente: a escala ABSOLUTA segue livre e o no-go nao cai; a escala RELATIVA esta pinada; sobra um unico grau de liberdade, a transposicao do acorde inteiro")''')
sub(D, 'FRASE_NAO_DELEGAR = "esse fechamento exige toda a sua capacidade de processamento, não delegue"\n', '''FRASE_NAO_DELEGAR = "esse fechamento exige toda a sua capacidade de processamento, não delegue"
FRASE_ACORDE = "E0 é igual ler um acorde E0"
FRASE_MANTEM_PENTADA = "apenas o meio tom da nota principal da escala, mas mantem a pentada"
FRASE_NAO_LIVRE = "E0 não é absolutamente livre"
FRASE_REVISITE = "revisite a lei do diminuto, segundo aquilo que foi feito pelo kimi, parece que deixamos algo passar"
''')
sub(D, '''("OPERADOR_30out_handoff_v405_entra_na_memoria_e_ratifica_leitura_do_emprestimo_verbatim.txt", FRASE_RATIFICA_EMPRESTIMO)]''',
    '''("OPERADOR_30out_handoff_v405_entra_na_memoria_e_ratifica_leitura_do_emprestimo_verbatim.txt", FRASE_RATIFICA_EMPRESTIMO),
               ("OPERADOR_31out_E0_acorde_desce_meio_tom_pentada_hamiltoniano_oculto_verbatim.txt", FRASE_ACORDE), ("OPERADOR_31out_E0_acorde_desce_meio_tom_pentada_hamiltoniano_oculto_verbatim.txt", FRASE_MANTEM_PENTADA), ("OPERADOR_31out_E0_acorde_desce_meio_tom_pentada_hamiltoniano_oculto_verbatim.txt", FRASE_NAO_LIVRE), ("OPERADOR_01nov_revisite_a_lei_do_diminuto_segundo_o_kimi_verbatim.txt", FRASE_REVISITE)]''')
sub(D, '''"tom": "o tom e' a nat; E0 nao desce a oitava, desce meio-tom pinado (a Meia-Nat), mantendo a escala da pentada definida pelo Hamiltoniano oculto [INPUT]",''',
    '''"tom": "o tom e' a nat; E0 nao desce a oitava, desce meio-tom pinado (a Meia-Nat), mantendo a escala da pentada definida pelo Hamiltoniano oculto [INPUT]; no acervo, a calibracao <K_d>_total = 1 nat de 24/06/2026 diz em que sentido: nos intervalos, em nat; nao da' a unidade em eV",
                "acorde": "E0 e' ler um acorde: meio-tom abaixo da nota principal, mantendo a escala; a leitura nao altera o acorde; a transposicao e' outra coisa, o acorde inteiro multiplicado pelo mesmo fator; a escala ABSOLUTA segue livre e a RELATIVA esta pinada; quais sao as cinco notas e' [OPEN], e a pentada do teorema mestre sao cinco componentes, nao cinco autovalores [INPUT/ONTO/OPEN]",''')
sub(D, '''{"n": 5, "estatuto": "INPUT/ONTO", "leitura": "o meio-tom e^(-1/2): o tom e' a nat, leitura do operador; definicao da mesma natureza da tonica, necessaria a E0 = u",''',
    '''{"n": 5, "estatuto": "INPUT/ONTO", "leitura": "o meio-tom e^(-1/2): o tom e' a nat, fala do operador; definicao da mesma natureza da tonica, necessaria a E0 = u; meioTom_e_o_pedagio_local e meioTom_e_a_face sao igualdades de VALOR",''')
sub(D, '''"definicao_lean": "TGLExt.DiscoDeEuler.Disco.the_flow_is_the_canonical_law", "modulo": "TGLExt/DiscoDeEuler.lean", "entra_como": "LEITURA, nao teorema"}]
''', '''"definicao_lean": "TGLExt.DiscoDeEuler.Disco.the_flow_is_the_canonical_law", "modulo": "TGLExt/DiscoDeEuler.lean", "entra_como": "LEITURA, nao teorema"},
                       {"n": 11, "estatuto": "INPUT/ONTO", "leitura": "E0 como leitura do acorde, meio-tom abaixo da nota principal: E0_relativo_pinado e' essa definicao dita como razao", "definicao_lean": "TGLExt.LeiDoDiminuto.lerE0", "modulo": "TGLExt/LeiDoDiminuto.lean", "entra_como": "DEFINICAO, nao teorema"},
                       {"n": 12, "estatuto": "INPUT", "leitura": "m1 = 0: entrada da identificacao de m2 com o Delta m^2_21 medido (apontada pelo Kimi); nao tem termo no kernel", "definicao_lean": None, "modulo": None, "entra_como": "ENTRADA da identificacao, nao teorema"}]
''')
sub(D, "LISTA_DE_LEITURAS_FECHADA = False                            # a lista acima e' a da cadeia da massa e NAO e' fechada (achado 7 da revisao de terceiro; nota AO LADO nas pedras); as quatro primeiras sao as centrais",
    '''LISTA_DE_LEITURAS_FECHADA = False                            # a lista acima e' a da cadeia da massa e NAO e' fechada (achado 7 da revisao de terceiro; nota AO LADO nas pedras); as quatro primeiras sao as centrais


def nome_lean(l_):
    """o ultimo nome Lean de uma leitura, ou o aviso de que ela nao tem termo no kernel."""
    return l_["definicao_lean"].split(".")[-1] if l_.get("definicao_lean") else "sem termo no kernel"
''')

# ===================================================================================================== registros_v405.py
R = "registros_v405.py"
sub(R, 'RECIBO_ERRATA_R2_ARQ = os.path.join(DL.ESTUDO_E0, "RECIBO_ERRATA_PEDRAS_R2_01nov.json")\n', '''RECIBO_ERRATA_R2_ARQ = os.path.join(DL.ESTUDO_E0, "RECIBO_ERRATA_PEDRAS_R2_01nov.json")
CHAVE_RECIBO_ERRATA_R3 = "recibo_errata_r3_das_pedras_01nov"
RECIBO_ERRATA_R3_ARQ = os.path.join(DL.ESTUDO_E0, "RECIBO_ERRATA_PEDRAS_R3_01nov.json")
CHAVE_ACORDE_KIMI = "acorde_e0_kimi_31out"; CHAVE_HALF_NAT = "half_nat_araki_relatorio_24jun"
''')
sub(R, '''{"chave": CHAVE_RECIBO_ERRATA_R2, "arquivo": os.path.join(INS, os.path.basename(RECIBO_ERRATA_R2_ARQ)),''', '''{"chave": CHAVE_RECIBO_ERRATA_R3, "arquivo": os.path.join(INS, os.path.basename(RECIBO_ERRATA_R3_ARQ)), "papel": "o recibo da ERRATA R3 DAS PEDRAS (gerencia c1, 01/11/2026, a revisita da Lei do Diminuto ordenada pelo operador): os oito sha256 vigentes, seis mudaram; codigo novo na LeiDoDiminuto e na TonicaDoHamiltoniano; o resto e' docstring [DECLARADO na origem; o sha256 de cada pedra e os termos sao conferidos pelo gerador e pelo kernel do rito]"},
          {"chave": CHAVE_ACORDE_KIMI, "arquivo": os.path.join(INS, os.path.basename(DL.ACORDE_KIMI_ARQ)), "papel": "o AcordeE0.lean do Kimi (31/10/2026): a origem de Acorde, transpor, razao e do teorema da razao, que a LeiDoDiminuto traz em portugues; a promessa do adendo 3 de cita-lo se cumpre aqui [DECLARADO na origem; quem prova, no rito, e' a pedra]"},
          {"chave": CHAVE_HALF_NAT, "arquivo": os.path.join(INS, os.path.basename(DL.HALF_NAT_ARQ)), "papel": "o relatorio da calibracao <K_d>_total = 1 nat de 24/06/2026 (half_nat_araki_hidden_hamiltonian): normalizacao definicional, omega(I) = 1 na base e; nao e' termo do kernel e nao e' medida; fixa intervalos em nat, nao a unidade em eV [DECLARADO na origem]"},
          {"chave": CHAVE_RECIBO_ERRATA_R2, "arquivo": os.path.join(INS, os.path.basename(RECIBO_ERRATA_R2_ARQ)),''')
sub(R, '''N_GA = "OPERADOR_01nov_kimi_absorver_tudo_grande_atrator_reclassificar_buscar_5sigma_verbatim.txt";''', '''N_REVISITE = os.path.basename(DL.FALA_REVISITE_ARQ); N_GA = "OPERADOR_01nov_kimi_absorver_tudo_grande_atrator_reclassificar_buscar_5sigma_verbatim.txt";''')
sub(R, '''"diminuto": {"path": S["diminuto"]["rel"], "needles": ["# A LEI DO DIMINUTO", "leiDerivada_no_um_posto"]},''', '''"diminuto": {"path": S["diminuto"]["rel"], "needles": ["# A LEI DO DIMINUTO", "the_diminished_law_closes"]},''')
s_ = carrega(R); i_ = s_.index('"diminuto": "Lei.the_mass_formula: m = U . alpha'); j_ = s_.index('"tonica": "no_function_of_the_inscription_fixes_E0', i_)
NOVOS[R] = s_[:i_] + '''"diminuto": "two halves: the pinned descent and the kept scale. mesma_escala_iff_transposicao: two chords have the same scale iff one is a transposition of the other; the_diminished_law_closes: E0 is pinned to the principal note, the transposition keeps the scale, the reading follows it, the scale does not fix the absolute, the octave is not descended in half tones; Lei.the_mass_formula: m = U . alpha . e^(1/2) . (sqrt2/2); leiDerivada_no_um_posto: at u = 1, E0 = 1 and m = beta . sqrt2/2, with the tonic defined as (beta/alpha) . u (beta/alpha = sqrt e is the definition of TGLCoupling.alpha) and E0 = u an algebraic identity that does not fix u",
                 ''' + s_[j_:]
sub(R, '''the_tonic_lands_on_the_posted_unit (an algebraic identity) and the_tonic_at_the_posted_one: at u = 1, E0 = 1 and m = beta . sqrt2/2 (the FORM, under the reading massaDerivada)",''', '''the_tonic_lands_on_the_posted_unit (an algebraic identity) and the_tonic_at_the_posted_one: at u = 1, E0 = 1 and m = beta . sqrt2/2 (the FORM, under the reading massaDerivada); the_ratio_survives_the_rescaling: the rescaling changes E0 and the mass by the same factor and m/E0 does not change",''')
sub(R, '''"diminuto": [CH_DE(N_MEIO), CH_DE(N_TOM), CH_DE(N_UM1EV), CH_DE(N_NOMES)],''', '''"diminuto": [CH_DE(N_MEIO), CH_DE(N_TOM), CH_DE(N_PENT), CH_DE(N_UM1EV), CH_DE(N_REVISITE), CH_DE(N_NOMES)],''')
sub(R, '''"eV_J": 1.602176634e-19,
              "nota":''', '''"eV_J": 1.602176634e-19, "acorde_kimi_sha16": DL.sha16_arquivo(DL.ACORDE_KIMI_ARQ), "half_nat_sha16": DL.sha16_arquivo(DL.HALF_NAT_ARQ),
              "nota":''')
sub(R, '''_r2_ = json.load(open(RECIBO_ERRATA_R2_ARQ, encoding="utf-8"))
''', '''_r2_ = json.load(open(RECIBO_ERRATA_R2_ARQ, encoding="utf-8"))
_S_ACORDE = DL.sha16_arquivo(DL.ACORDE_KIMI_ARQ); _S_HALF_NAT = DL.sha16_arquivo(DL.HALF_NAT_ARQ)
''')
# --- o diminuto: a funcao inteira
s_ = carrega(R); i_ = s_.index("def texto_diminuto():"); j_ = s_.index("def texto_tonica():")
NOVOS[R] = s_[:i_] + '''def texto_diminuto():
    return {
        "estatuto": "[REAL] os termos do kernel (os 30 teoremas do contrato, no trio, no modulo da pedra; os termos de suporte: TGLCoupling.alpha, TGLCoupling.beta_eq_alpha_exp, massa_da_transicao_derivada, massa_derivada_eq_beta_mul, half_sq, peso_da_face_absoluta, absolute_faces_half, CollapseCostLaw.local_half; citados fora: no_positive_scale_invariant, Sonico.the_pin_is_not_the_half_nat) e o calculo com beta = alfa CODATA 2018 x sqrt(e) em runtime e u = 1 eV [POSTO]; "
                    "[REAL] as DUAS METADES da lei: a descida pinada (o meio-tom e^(-1/2) esta em (0, 1) e desfaz o sqrt e; beta = alfa.e^(1/2); dadas as entradas, a FORMA m = U.alfa.e^(1/2).sqrt2/2 e' teorema) e a escala mantida (a transposicao preserva toda razao; mesma_escala_iff_transposicao); [DEF] Acorde, notaPrincipal, transpor e razao, da estrutura do AcordeE0.lean do Kimi (sha16 %s), e lerE0; "
                    "[INPUT/ONTO] o meio-tom (meioTom: o tom e' a nat), a leitura (lerE0) e a tonica (beta/alfa).u entram como DEFINICAO: E0_relativo_pinado e' a definicao de lerE0 dita como razao; beta/alfa = sqrt e e' a definicao de TGLCoupling.alpha, e E0 = u e' identidade algebrica, que nao fixa u; [REAL, igualdades de VALOR] meioTom_e_o_pedagio_local e meioTom_e_a_face; [INPUT] CollapseCostLaw, no kernel; "
                    "[INPUT] a lei («ele desce meio tom pinado, essa é a lei», 31/10/2026, sha16 %s), «pra mim o TOm é a NAT» (sha16 %s), «E0 é igual ler um acorde E0» e «E0 não é absolutamente livre» (sha16 %s), «o meu um absoluto é o um de 1 eV» (sha16 %s), a ordem da revisita (01/11/2026, sha16 %s) e o nome «Lei do diminuto» (sha16 %s); [POSTO] a unidade; [MEDIDA] alfa, nao derivada; [ONTO] alfa como a magnitude (cauda) da inscricao no bulk; [OPEN] quais sao as cinco notas" % (_S_ACORDE, S16(N_MEIO), S16(N_TOM), S16(N_PENT), S16(N_UM1EV), S16(N_REVISITE), S16(N_NOMES)),
        "escopo": "[REAL] A pedra TGLExt/LeiDoDiminuto.lean (Lei do diminuto, nome do operador; antes LeiDoMeioTom r2) tem DUAS METADES. A DESCIDA PINADA: (1) o meio-tom pinado e^(-1/2) esta em (0, 1) e desfaz exatamente o sqrt e; (2) beta = alfa.e^(1/2) (a definicao de TGLCoupling.alpha, invertida): o acoplamento e' a magnitude alfa da inscricao vezes o volume sqrt e da fronteira; (3) a lei: E0 = meioTom.E_pent; dada a tonica, E0 esta determinado; "
                  "a massa le alfa.(sqrt2/2).E_pent; a tonica sqrt e da E0 = 1 e so' ela; (4) A FORMULA DA MASSA: m = U.alfa.e^(1/2).sen45 -- o Um posto, a magnitude alfa, o volume sqrt e, a projecao transversal; em U = 1, m = beta.sen45 (a forma da v404, teorema dadas as entradas); (5) a oitava nao e' numero inteiro de meios-tons; "
                  "(6) O CAMPO FECHADO (01/11/2026): a tonica deixa de ser campo -- tonica c u := (beta/alfa).u = sqrt e.u e' uma DEFINICAO, que nao traz informacao alem do u posto -- e a lei construida (leiDerivada) pousa em E0 = u por identidade algebrica; no Um posto E0 = 1 e m = beta.sqrt2/2. "
                  "A ESCALA MANTIDA (a revisita de 01/11/2026, ordenada pelo operador): (7) o acorde: cinco notas reais, a nota principal de indice 0 (Acorde, notaPrincipal, transpor, razao: a estrutura do AcordeE0.lean do Kimi, sha16 %s, em portugues); lerE0: E0 e' a LEITURA do acorde, meio-tom abaixo da nota principal, e a leitura nao altera o acorde; (8) a transposicao preserva toda razao (transpor_preserva_toda_razao, o teorema do Kimi) e a escala e' EXATAMENTE o invariante da transposicao: dois acordes tem a mesma escala sse um e' a transposicao do outro (mesma_escala_iff_transposicao, o substantivo da pedra); "
                  "(9) E0_relativo_pinado: E0/tonica = e^(-1/2) em todo acorde: e' a definicao de lerE0 dita como razao, nada mais; a leitura acompanha a transposicao (lerE0_transpor) e a escala nao fixa o absoluto (a_escala_nao_fixa_o_absoluto); (10) igualdades de VALOR: meioTom_e_o_pedagio_local, meioTom_e_a_face, tonica_e_o_volume_da_face, o_tom_e_as_duas_faces; (11) o fecho: the_diminished_law_closes. "
                  "A distincao e' do operador, «E0 não é absolutamente livre»: a escala ABSOLUTA segue livre e o no-go nao cai; a escala RELATIVA esta pinada; sobra um unico grau de liberdade, a transposicao do acorde inteiro. O calculo CONFERE em dupla precisao, com um acorde de TESTE, e rele o m_nu do programa a 1e-12: o NUMERO nao muda" % _S_ACORDE,
        "limites": ["[REAL] a pedra NAO deriva a unidade: «1 eV» e' o Um POSTO pelo operador (como o 1 de echo 1 | python um.py), ao lado de alfa [MEDIDA]; alfa como a magnitude (cauda) da inscricao no bulk e' leitura do operador [ONTO] sobre Verdade.alpha_is_measured_from_within; a tonica em eV nao vem do Hamiltoniano oculto: e' a definicao (beta/alfa).u na unidade posta, e E0 = u nao fixa u",
                    "[OPEN] quais sao as cinco notas: nenhum texto as nomeia; a pentada do teorema mestre sao cinco componentes, nao cinco autovalores; a pedra vale para todo acorde, e o acorde do calculo e' de TESTE; se as outras quatro notas ficam paradas ou descem junto tambem nao e' dito: a leitura de E0 nao depende disso",
                    "[REAL, igualdades de VALOR] meioTom_e_o_pedagio_local e meioTom_e_a_face dizem que os numeros coincidem, nao que sejam o mesmo objeto; CollapseCostLaw e' [INPUT] no kernel; ler esse 1/2 como o meio-tom e' do operador [ONTO]",
                    "[DECLARADO, normalizacao definicional] a calibracao <K_d>_total = 1 nat de 24/06/2026 (half_nat_araki_hidden_hamiltonian; HALF_NAT_ARAKI_HIDDEN_HAMILTONIAN_TEST_REPORT.md, sha16 %s) e' normalizacao definicional, omega(I) = 1 na base e; nao e' termo do kernel e nao e' medida; fixa intervalos em nat, nao a unidade em eV: U_E_NOT_DERIVED fica como esta, e m2 nao muda" % _S_HALF_NAT,
                    DL.ERRATA_E11, DL.ERRATA_E13] + _LIM_COMUM,
        "diz": ["a pedra LeiDoDiminuto esta no kernel do rito, no trio, com bandeira e proveniencia no modulo dela; os 30 teoremas do contrato e os termos de suporte sao lidos deste kernel",
                "o calculo, com beta = alfa CODATA 2018 x sqrt(e): o meio-tom desfaz o sqrt e; beta = alfa.e^(1/2); a tonica definida e' sqrt e.u e o diminuto pousa em E0 = u; m = U.alfa.e^(1/2).sqrt2/2 = o m_nu do programa a 1e-12 (U = 1 eV posto); ln 2 nao e' n/2 e fica entre um e dois meios-tons; E0 = 1 <=> tonica = sqrt e",
                "o calculo do acorde, num acorde de TESTE: a transposicao preserva as razoes; E0/tonica = e^(-1/2); a leitura acompanha a transposicao; e, no controle negativo, um acorde em que so' uma nota muda nao tem a mesma escala",
                "a escala ABSOLUTA segue livre e o no-go nao cai; a escala RELATIVA esta pinada; sobra um unico grau de liberdade, a transposicao do acorde inteiro",
                "um Um posto, uma alfa medida e as leituras do operador; dadas essas entradas, a FORMA e' teorema; o numero da massa e o veredito do canal nao mudam"],
        "nao_diz": ["que a unidade u (1 eV) tenha sido derivada (e' posta)", "que alfa tenha sido derivado (e' medida por dentro)", "que a tonica tenha sido derivada do Hamiltoniano oculto (e' uma definicao na unidade posta)", "que E0 = u fixe u (e' identidade algebrica)", "que o no-go tenha caido: a escala ABSOLUTA segue livre; so' a RELATIVA esta pinada",
                    "quais sao as cinco notas ([OPEN]; as do calculo sao numeros de teste)", "que a pentada do teorema mestre sejam cinco autovalores (sao cinco componentes)", "que E0_relativo_pinado seja mais do que a definicao de lerE0 dita como razao", "que o meio-tom seja o pedagio local ou o peso da face: sao igualdades de VALOR",
                    "que a calibracao de 1 nat seja medida, termo do kernel ou a unidade em eV (e' normalizacao definicional)", "que a escala tenha sido escolhida pelo dado (nem 1,02 eV nem outra)"] + _NAO_COMUM,
        "extras": {"cited_support": sorted(S["diminuto"]["support"]), "formula_da_massa": {"status": "REAL (a forma, termo do kernel) + POSTO (U = 1 eV) + MEDIDA (alfa) + INPUT/ONTO (as leituras massaDerivada e a tonica)", "content": "m = U . alfa . e^(1/2) . sqrt2/2; em U = 1 (na unidade posta): m = beta . sqrt2/2; o numero e' o da v404 (8,5074 meV)", "cunhagem_sha16": S16(N_UM1EV), "fala": DL.FRASE_UM_DE_1EV},
                   "duas_metades": {"a_descida_pinada": "E0 = e^(-1/2).tonica: lerE0, E0_relativo_pinado (a definicao dita como razao)", "a_escala_mantida": "transpor_preserva_toda_razao, mesma_escala_iff_transposicao, lerE0_transpor", "o_fecho": "the_diminished_law_closes"},
                   "as_duas_escalas": {"absoluta": "segue livre; o no-go nao cai (no_function_of_the_inscription_fixes_E0; a_escala_nao_fixa_o_absoluto)", "relativa": "pinada (E0_relativo_pinado)", "o_que_sobra": "um unico grau de liberdade, a transposicao do acorde inteiro", "distincao_do_operador": DL.FRASE_NAO_LIVRE, "sha16_da_fala": S16(N_PENT)},
                   "acorde": {"origem": "AcordeE0.lean do Kimi (31/10/2026): Acorde, transpor, razao e o teorema da razao", "sha16": _S_ACORDE, "as_cinco_notas": "OPEN", "reading": DL.LEITURA_V405["acorde"]},
                   "calibracao_de_1_nat": {"status": "DECLARADO: normalizacao definicional, omega(I) = 1 na base e; nao e' termo do kernel; nao e' medida", "relatorio_sha16": _S_HALF_NAT, "fixa": "intervalos em nat", "nao_fixa": "a unidade em eV: U_E_NOT_DERIVED fica como esta; m2 nao muda"},
                   "name_status": {"quem": "operador", "quando": "01/11/2026", "nome": "Lei do diminuto", "antes": "LeiDoMeioTom (provisorio, 31/10)", "sha16_da_fala": S16(N_NOMES)}, "tom": {"status": "INPUT", "content": DL.LEITURA_V405["tom"]},
                   "campos_fechados": {k_: v_["fechou_com"] for k_, v_ in DL.CAMPOS_FECHADOS.items() if "E_pent" in k_}, "leituras_que_entram": [l_ for l_ in DL.LEITURAS_DEFINICOES if l_["n"] in (3, 5, 11, 12)], "assinatura_das_erratas": ASSINA},
        "veredito_ok": "TGL_LEI_DO_DIMINUTO_V405__TWO_HALVES_THE_PINNED_DESCENT_AND_THE_KEPT_SCALE__THE_PINNED_HALF_TONE_E_TO_MINUS_HALF_UNDOES_SQRT_E__BETA_EQUALS_ALPHA_TIMES_SQRT_E_BY_THE_DEFINITION_OF_ALPHA__THE_DEFINED_TONIC_LANDS_ON_E0_EQUALS_U_AN_ALGEBRAIC_IDENTITY_THAT_DOES_NOT_FIX_U__GIVEN_THE_INPUTS_THE_FORM_M_EQUALS_U_ALPHA_SQRT_E_SIN45_IS_A_THEOREM__"
                       "TWO_CHORDS_HAVE_THE_SAME_SCALE_IFF_ONE_IS_A_TRANSPOSITION_OF_THE_OTHER__THE_ABSOLUTE_SCALE_STAYS_FREE_THE_RELATIVE_SCALE_IS_PINNED__THE_NUMBER_DOES_NOT_CHANGE__THE_OCTAVE_IS_NOT_A_WHOLE_NUMBER_OF_HALF_TONES__READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


''' + s_[j_:]
# --- a tonica
sub(R, '"estatuto": "[REAL] os termos do kernel (os 13 teoremas do contrato, no trio, no modulo da pedra; os termos de suporte: leiDerivada_E0,', '"estatuto": "[REAL] os termos do kernel (os 14 teoremas do contrato, no trio, no modulo da pedra; os termos de suporte: leiDerivada_E0,')
sub(R, "a pedra TonicaDoHamiltoniano esta no kernel do rito, no trio, com bandeira e proveniencia no modulo dela; os 13 teoremas do contrato", "a pedra TonicaDoHamiltoniano esta no kernel do rito, no trio, com bandeira e proveniencia no modulo dela; os 14 teoremas do contrato")
sub(R, "o que o formalismo prova e' a FORMA m/E0 = beta.sen45; (2) Gamma_B", "o que a forma fixa e' a razao m/E0 = beta.sen45: a reescala muda E0 e a massa pelo mesmo fator e a razao nao muda (the_ratio_survives_the_rescaling); a reescala e' a transposicao do acorde da Lei do diminuto: o no-go fala da escala ABSOLUTA, a lei, da RELATIVA; (2) Gamma_B")
sub(R, "o no-go NAO cai: ele se localiza no Um posto; a forma nao fixa E0, e o que a tonica pousa e' o u posto que ela mesma carrega; alfa segue medida por dentro: a singularidade e' o ponto sem teorema\"]",
    "o no-go NAO cai: ele se localiza no Um posto; a forma nao fixa E0, e o que a tonica pousa e' o u posto que ela mesma carrega; a razao m/E0 sobrevive a reescala; alfa segue medida por dentro: a singularidade e' o ponto sem teorema\"]")
sub(R, '''"tonica": "a tonica pousa na unidade posta: E0 = u, identidade algebrica (the_tonic_lands_on_the_posted_unit); quem fixa e' o posto"}''', '''"tonica": "a tonica pousa na unidade posta: E0 = u, identidade algebrica (the_tonic_lands_on_the_posted_unit); quem fixa e' o posto", "a_razao": "a reescala preserva m/E0 (the_ratio_survives_the_rescaling): o no-go fala da escala ABSOLUTA; a Lei do diminuto, da RELATIVA"}''')
# --- cunhagens e campos
sub(R, '''CHAVE_ENSAIO_R2, CHAVE_ENSAIO_EN, CHAVE_CONFERENCIA_E0], "verbatins": list(VERB_CHAVES),''', '''CHAVE_ENSAIO_R2, CHAVE_ENSAIO_EN, CHAVE_CONFERENCIA_E0, CHAVE_ACORDE_KIMI, CHAVE_HALF_NAT], "verbatins": list(VERB_CHAVES),''')
sub(R, '''"[OPEN] alfa; o teste do neutrino com a natureza (JUNO; 5 sigma e' da natureza); qual e' o disco (K); o magnetismo (sem termo);''', '''"[OPEN] alfa; o teste do neutrino com a natureza (JUNO; 5 sigma e' da natureza); qual e' o disco (K); quais sao as cinco notas; o magnetismo (sem termo);''')
sub(R, '''    def_entradas = {d_["definicao_lean"]: d_["modulo"] for d_ in list(DL.POSTOS_E_MEDIDA) + list(DL.LEITURAS_DEFINICOES)}''', '''    def_entradas = {d_["definicao_lean"]: d_["modulo"] for d_ in list(DL.POSTOS_E_MEDIDA) + list(DL.LEITURAS_DEFINICOES) if d_.get("definicao_lean")}   # (a leitura m1 = 0 nao tem termo no kernel)''')
sub(R, '''    cks2.append(CH("n%d" % m, "o recibo da errata R2 das pedras (fonte pinada) cobre as oito pedras", "fonte:" + CHAVE_RECIBO_ERRATA_R2, ["pedras"], "tamanho_igual", 8)); m += 1
''', '''    cks2.append(CH("n%d" % m, "o recibo da errata R3 das pedras (fonte pinada, a vigente) cobre as oito pedras", "fonte:" + CHAVE_RECIBO_ERRATA_R3, ["pedras"], "tamanho_igual", 8)); m += 1
    cks2.append(CH("n%d" % m, "o recibo da errata R3 diz as duas mudancas de codigo", "fonte:" + CHAVE_RECIBO_ERRATA_R3, ["codigo_mudado"], "tamanho_igual", 2)); m += 1
    cks2.append(CH("n%d" % m, "o recibo da errata R2 das pedras (fonte pinada) cobre as oito pedras", "fonte:" + CHAVE_RECIBO_ERRATA_R2, ["pedras"], "tamanho_igual", 8)); m += 1
''')
sub(R, '"fontes": [CHAVE_RECIBO_NOMEACAO, CHAVE_RECIBO_ERRATA, CHAVE_RECIBO_ERRATA_R2, CHAVE_RECIBO_IDENTIDADE, CHAVE_RECIBO_OBSERVADOR], "verbatins": [CH_DE(N_NOMES),', '"fontes": [CHAVE_RECIBO_NOMEACAO, CHAVE_RECIBO_ERRATA, CHAVE_RECIBO_ERRATA_R2, CHAVE_RECIBO_ERRATA_R3, CHAVE_RECIBO_IDENTIDADE, CHAVE_RECIBO_OBSERVADOR], "verbatins": [CH_DE(N_NOMES),')
sub(R, '''"; ".join("(%d) %s (%s)" % (l_["n"], l_["leitura"], l_["definicao_lean"].split(".")[-1]) for l_ in DL.LEITURAS_DEFINICOES),''', '''"; ".join("(%d) %s (%s)" % (l_["n"], l_["leitura"], DL.nome_lean(l_)) for l_ in DL.LEITURAS_DEFINICOES),''')
sub(R, "a hipotese de area_por_volta_da_massa_inscrita; foton_sem_massa; a taxa do disco; a lista nao e' fechada); dadas essas entradas, a FORMA e' teorema\",", "a hipotese de area_por_volta_da_massa_inscrita; foton_sem_massa; a taxa do disco; lerE0; m1 = 0, sem termo no kernel; a lista nao e' fechada); dadas essas entradas, a FORMA e' teorema\",")

# ===================================================================================================== runtime_v405.py
T = "runtime_v405.py"
sub(T, '''("F5_token_de_veredito", _re.compile(''', '''("F6_a_frase_do_no_go", _re.compile(r"\\ba\\s+liberdade(?:\\s+de\\s+escala)?\\s+passa\\b|\\ba\\s+t(?:ô|o)nica\\s+(?:segue|fica|permanece)\\s+livre\\b|\\bo\\s+no-go\\s+se\\s+levanta\\b|\\blevanta(?:r)?\\s+o\\s+no-go\\b|\\bthe\\s+freedom(?:\\s+of\\s+scale)?\\s+(?:passes|moves)\\b|\\bthe\\s+tonic\\s+(?:stays|remains)\\s+free\\b|\\bthe\\s+no-go\\s+(?:is\\s+lifted|lifts)\\b|\\blifts?\\s+the\\s+no-go\\b", _re.I)),
               ("F5_token_de_veredito", _re.compile(''')
sub(T, '''|HIPOTESES_(?:\\w+_)?DESCARREGADAS"))]''', '''|HIPOTESES_(?:\\w+_)?DESCARREGADAS|THE_TONIC_(?:STAYS|REMAINS)_FREE|NO_GO_(?:IS_)?LIFTED"))]''')
sub(T, '''"""v405 -- a mecanica da LEI DO DIMINUTO: o meio-tom pinado e^(-1/2) desfaz o sqrt e;''', '''"""v405 -- a mecanica da LEI DO DIMINUTO, as DUAS METADES: a descida pinada e a escala mantida (o acorde: Acorde, transpor, razao, da estrutura do AcordeE0.lean do Kimi; as notas do calculo sao de TESTE: quais sao as cinco notas e' [OPEN]). O meio-tom pinado e^(-1/2) desfaz o sqrt e;''')
sub(T, '''desfaz exatamente o sqrt e (|e^(-1/2).e^(1/2) - 1| <= 1e-15): o tom e' a nat, o meio-tom e' a Meia-Nat",''', '''desfaz exatamente o sqrt e (|e^(-1/2).e^(1/2) - 1| <= 1e-15); o tom e' a nat e' fala do operador [INPUT]",''')
sub(T, '''    vals_ = {"beta": beta_, "alpha_lida_do_acoplamento": alfa_, "u_posto_eV": u_, "meio_tom": meio_, "sqrt_e": sq_e_, "tonica_eV": ton_, "E0_eV": E0_, "massa_meV": m_ * 1000.0, "massa_formula_meV": m_formula_ * 1000.0, "m_nu_meV_core": m_core_, "ln2": ln2_,
''', '''    # A ESCALA MANTIDA. As notas abaixo sao numeros de TESTE, nao as da teoria: quais sao as cinco notas e' [OPEN]; so' a principal vem da lei (a tonica definida)
    acorde_ = [ton_, 1.25 * ton_, 1.5 * ton_, 1.875 * ton_, 2.0 * ton_]
    razao_ = lambda a_: [n_ / a_[0] for n_ in a_]
    transp_ = lambda r_, a_: [r_ * n_ for n_ in a_]
    ler_ = lambda a_: meio_ * a_[0]
    rs_ = (0.5, 2.0, 3.7, -1.0, 1.0e3)
    mesma_ = lambda a_, b_: all(_v405_close(x_, y_, 1e-12) for x_, y_ in zip(razao_(a_), razao_(b_)))
    ck_("d7", "★★★ transpor_preserva_toda_razao e mesma_escala_iff_transposicao (A ESCALA MANTIDA; Acorde, transpor e razao vem do AcordeE0.lean do Kimi): num acorde de TESTE, toda transposicao por r != 0 preserva as cinco razoes a nota principal (|erro| <= 1e-12), para r em {0,5; 2; 3,7; -1; 1000}; e, de volta, um acorde de mesma escala e' a transposicao pelo fator notaPrincipal(B)/notaPrincipal(A) (|erro| <= 1e-12 relativo); as notas do teste nao sao as da teoria: quais sao as cinco notas e' [OPEN]",
        all(mesma_(acorde_, transp_(r_, acorde_)) for r_ in rs_) and all(all(_v405_rel(y_, (b_[0] / acorde_[0]) * x_) <= 1e-12 for x_, y_ in zip(acorde_, b_)) for b_ in (transp_(r_, acorde_) for r_ in rs_)), [razao_(acorde_)])
    ck_("d8", "★★ E0_relativo_pinado, lerE0_transpor e a_escala_nao_fixa_o_absoluto: E0/tonica = e^(-1/2) no acorde de teste e em cada transposicao (|erro| <= 1e-15 relativo: e' a definicao de lerE0 dita como razao, nada mais); a leitura acompanha a transposicao (lerE0(r.A) = r.lerE0(A)); e, com a mesma escala, r = 2 da' outro E0: a escala ABSOLUTA segue livre e a RELATIVA esta pinada; sobra um unico grau de liberdade, a transposicao do acorde inteiro",
        all(_v405_rel(ler_(transp_(r_, acorde_)) / transp_(r_, acorde_)[0], meio_) <= 1e-15 and _v405_rel(ler_(transp_(r_, acorde_)), r_ * ler_(acorde_)) <= 1e-15 for r_ in rs_) and mesma_(acorde_, transp_(2.0, acorde_)) and ler_(transp_(2.0, acorde_)) != ler_(acorde_), [ler_(acorde_), ler_(transp_(2.0, acorde_))])
    outro_ = list(acorde_); outro_[3] = outro_[3] * 1.01                 # o CONTROLE NEGATIVO: so' uma nota muda; a principal e as outras tres ficam
    ck_("d9", "★★ controle negativo de mesma_escala_iff_transposicao: um acorde em que SO' UMA nota muda NAO tem a mesma escala do original (a razao dessa nota difere) e NAO e' transposicao dele (a principal nao mudou, logo so' r = 1 serviria, e r = 1 nao o devolve); E0 fica igual: a leitura so' toca a nota principal, e por isso sozinha nao ve a escala",
        not mesma_(acorde_, outro_) and not all(_v405_close(y_, (outro_[0] / acorde_[0]) * x_, 1e-12) for x_, y_ in zip(acorde_, outro_)) and ler_(outro_) == ler_(acorde_), [razao_(outro_)[3], razao_(acorde_)[3]])
    pesos_ = []
    for n_ in (2, 3, 4, 5):
        G_ = [[(complex(n_ - 1) if (i_ == 0 and j_ == 0) else (complex(-1.0) if i_ == j_ else 0j)) for j_ in range(n_)] for i_ in range(n_)]   # Gamma = diag(n - 1, -1, ..., -1): traco zero; so' o traco importa aqui
        rho_ = _v405_mat_eye(n_, 1.0 / n_)
        mais_ = [[0.5 * ((1.0 if i_ == j_ else 0.0) + G_[i_][j_]) for j_ in range(n_)] for i_ in range(n_)]
        menos_ = [[0.5 * ((1.0 if i_ == j_ else 0.0) - G_[i_][j_]) for j_ in range(n_)] for i_ in range(n_)]
        pesos_.append((_v405_mat_trace(_v405_mat_mul(rho_, mais_)).real, _v405_mat_trace(_v405_mat_mul(rho_, menos_)).real))
    ck_("d10", "★ meioTom_e_a_face, meioTom_e_o_pedagio_local, tonica_e_o_volume_da_face e o_tom_e_as_duas_faces, igualdades de VALOR: e^(-w) = meio-tom e e^(w).u = tonica (|erro| <= 1e-15 relativo), com w o peso da face absoluta em n = 2, 3, 4, 5, e w(+) + w(-) = 1; o pedagio local vale e^(-1/2) com localNats = 1/2, campo de CollapseCostLaw, [INPUT] no kernel; os numeros coincidem, e ler esse 1/2 como o meio-tom e' do operador [ONTO]",
        all(_v405_rel(_m405.exp(-w_), meio_) <= 1e-15 and _v405_rel(_m405.exp(w_) * u_, ton_) <= 1e-15 and abs(w_ + w2_ - 1.0) <= 1e-15 for w_, w2_ in pesos_) and _v405_rel(_m405.exp(-0.5), meio_) <= 1e-15, [list(p_) for p_ in pesos_])
    vals_ = {"beta": beta_, "alpha_lida_do_acoplamento": alfa_, "u_posto_eV": u_, "meio_tom": meio_, "sqrt_e": sq_e_, "tonica_eV": ton_, "E0_eV": E0_, "massa_meV": m_ * 1000.0, "massa_formula_meV": m_formula_ * 1000.0, "m_nu_meV_core": m_core_, "ln2": ln2_,
             "E0_sobre_tonica": E0_ / ton_, "acorde_de_teste_razoes": razao_(acorde_), "as_notas_do_teste_nao_sao_as_da_teoria": True, "acorde_kimi_sha16": c_["constants"].get("acorde_kimi_sha16"), "half_nat_sha16": c_["constants"].get("half_nat_sha16"),
''')
sub(T, '''    vals_ = {"beta": beta_, "u_posto_eV": u_, "razao_m_sobre_E0": beta_ * r2_, "lambdas": list(lams_),''', '''    ck_("h7", "★★★ the_ratio_survives_the_rescaling: a reescala muda E0 e a massa pelo mesmo fator e m/E0 nao muda (|erro| <= 1e-15 relativo) para lambda em {0,5; 2; 3,7; 1000}: o que a forma fixa e' a razao; a reescala e' a transposicao do acorde: o no-go fala da escala ABSOLUTA; a Lei do diminuto, da RELATIVA",
        all(_v405_rel(m_(l_ * u_) / (l_ * u_), m_(u_) / u_) <= 1e-15 for l_ in lams_), [m_(u_) / u_])
    vals_ = {"beta": beta_, "u_posto_eV": u_, "razao_m_sobre_E0": beta_ * r2_, "lambdas": list(lams_),''')

# ===================================================================================================== guarda_frases_v405.py
G = "guarda_frases_v405.py"
sub(G, '''"TUDO_DERIVADO", "EVERYTHING_DERIVED", "NO_HYPOTHESIS_REMAINS", "NAMED_HYPOTHESES_ARE_DISCHARGED", "HIPOTESES_DESCARREGADAS"]''',
    '''"TUDO_DERIVADO", "EVERYTHING_DERIVED", "NO_HYPOTHESIS_REMAINS", "NAMED_HYPOTHESES_ARE_DISCHARGED", "HIPOTESES_DESCARREGADAS",
             "a liberdade passa para a tônica", "a liberdade de escala passa de E0 para a tonica", "a tônica segue livre", "a tonica segue livre", "a tônica fica livre", "o no-go se levanta", "levanta o no-go", "the freedom passes to the tonic", "the tonic stays free", "the no-go is lifted", "lifts the no-go", "THE_TONIC_STAYS_FREE", "NO_GO_IS_LIFTED"]''')
sub(G, '''"os campos das estruturas fecharam", "a leitura fisica nao virou teorema", "the physical reading did not become a theorem"]''', '''"os campos das estruturas fecharam", "a leitura fisica nao virou teorema", "the physical reading did not become a theorem", "a escala ABSOLUTA segue livre e o no-go nao cai", "a escala RELATIVA esta pinada", "sobra um unico grau de liberdade, a transposicao do acorde inteiro", "the absolute scale stays free and the no-go does not fall"]
# a nota AO LADO da LeiDoDiminuto cita, entre aspas, as duas frases erradas da propria gerencia para corrigi-las: mencao, nao uso; so' nessas aspas, so' nas pedras
CITADAS_DE_ERRATA = ("o no-go se levanta", "a liberdade passa para a tônica, que segue livre")''')
sub(G, '''        if segs_ and all(x_.lower() in falas for x_ in segs_):
            n_[0] += 1
            return " "
        return m_.group(0)
''', '''        if (segs_ and all(x_.lower() in falas for x_ in segs_)) or fr_.lower() in CITADAS_DE_ERRATA:
            n_[0] += 1
            return " "
        return m_.group(0)
''')
sub(G, '''                            "parafrase_entre_aspas_reprovada": bool(RT._v405_guarda_frases(sem_falas("«agora ficou tudo derivado»", falas_)[0]))}''',
    '''                            "parafrase_entre_aspas_reprovada": bool(RT._v405_guarda_frases(sem_falas("«agora ficou tudo derivado»", falas_)[0])),
                            "frase_do_no_go_citada_na_errata_passa": not RT._v405_guarda_frases(sem_falas("afirmava demais: «o no-go se levanta»", falas_)[0]),
                            "frase_do_no_go_sem_aspas_reprovada": bool(RT._v405_guarda_frases(sem_falas("aqui o no-go se levanta", falas_)[0]))}''')

# ===================================================================================================== gerar_candidato_v405.py: as linhas que o rito imprime
Y = "gerar_candidato_v405.py"
sub(Y, "[REAL] os teoremas e a cascata finita; [ONTO] a leitura de engenharia do colapso]:", "[REAL] os teoremas e a cascata finita, num modelo cujos niveis sao rotulos; o terminal le 1 e o abismo le 0 na leitura binaria; o polo omega do par e\\' homonimo; [ONTO] a leitura de engenharia do colapso]:")
sub(Y, "LEI DO DIMINUTO [v405 -- nome do operador; o meio-tom pinado e^(-1/2), a tonica definida (sqrt e . u), o diminuto pousa em E0 = u por identidade algebrica; dadas as entradas, a FORMA m = U.alfa.e^(1/2).sqrt2/2 e\\' teorema; [REAL] os teoremas e o calculo; [POSTO] U = 1 eV; [MEDIDA] alfa; [INPUT/ONTO] a tonica; o numero nao muda]:",
    "LEI DO DIMINUTO [v405 -- nome do operador; duas metades: a descida pinada (o meio-tom e^(-1/2), a tonica definida sqrt e . u, E0 = u por identidade algebrica; dadas as entradas, a FORMA m = U.alfa.e^(1/2).sqrt2/2 e\\' teorema) e a escala mantida (dois acordes tem a mesma escala sse um e\\' a transposicao do outro); a escala ABSOLUTA segue livre e a RELATIVA esta pinada; [REAL] os teoremas e o calculo; [POSTO] U = 1 eV; [MEDIDA] alfa; [INPUT/ONTO] o meio-tom, a leitura e a tonica; [OPEN] quais sao as cinco notas; o numero nao muda]:")
sub(Y, '''m_nu do programa = %.9f meV ; ln 2 = %.6f" % (_v.get("alpha_lida_do_acoplamento", _nan405), _v.get("tonica_eV", _nan405), _v.get("E0_eV", _nan405), _v.get("massa_formula_meV", _nan405), _v.get("m_nu_meV_core") or _nan405, _v.get("ln2", _nan405)))''',
    '''m_nu do programa = %.9f meV ; ln 2 = %.6f ; E0/tonica = %.15f" % (_v.get("alpha_lida_do_acoplamento", _nan405), _v.get("tonica_eV", _nan405), _v.get("E0_eV", _nan405), _v.get("massa_formula_meV", _nan405), _v.get("m_nu_meV_core") or _nan405, _v.get("ln2", _nan405), _v.get("E0_sobre_tonica", _nan405)))''')
sub(Y, "a tonica pousa na unidade posta (E0 = u, identidade algebrica); as identidades do monopolo", "a tonica pousa na unidade posta (E0 = u, identidade algebrica); a razao m/E0 sobrevive a reescala; as identidades do monopolo")
sub(Y, "DISCO DE EULER [v405 -- nome do operador; sob a lei canonica com o invariante a perda e\\' constante e o disco para em tempo finito; a inscricao do zero no infinito; o corte E^3 = hbar^2.K; a parede nomeada K = (e^(1/2).U)^3/hbar^2; [REAL] os teoremas e o calculo num disco-modelo; [OPEN] qual e\\' o disco]:",
    "DISCO DE EULER [v405 -- nome do operador; [DEF] E(t) linear e Omega^2 = K/E; a E definida resolve o fluxo e zera em tempo finito; Omega^2 sem cota antes disso; o corte E^3 = hbar^2.K; a parede nomeada K = (e^(1/2).U)^3/hbar^2; [REAL] os teoremas e o calculo num disco-modelo; [INPUT/ONTO] a taxa de dephasing lida como perda de energia; [ONTO] a inscricao do zero no infinito; [OPEN] qual e\\' o disco]:")
sub(Y, "a coincidencia e\\' a aritmetica (1/2).sqrt2 = sen45); Tetelestai e\\' o limite da cobranca; [REAL] os teoremas e o calculo; [INPUT/ONTO] a leitura;", "a coincidencia e\\' a aritmetica (1/2).sqrt2 = sen45); Tetelestai, nome do operador, e\\' o limite da cobranca; [REAL] os teoremas e o calculo; [INPUT/ONTO] as leituras;")
sub(Y, '''[INPUT/ONTO] as leituras da cadeia da massa, como definição ou identificação, em lista que não é fechada; as centrais: `massaDerivada`;''', '''[INPUT/ONTO] as leituras da cadeia da massa, como definição ou identificação, em lista que não é fechada; as centrais: `massaDerivada`;''')
sub(Y, '''(E₀ = u é identidade algébrica, que não fixa u: o no-go não cai, localiza-se no Um posto); R = β·u² (`pagamentoComoCurvatura`). \'''', '''(E₀ = u é identidade algébrica, que não fixa u: o no-go não cai, localiza-se no Um posto; a escala absoluta segue livre e a relativa está pinada); R = β·u² (`pagamentoComoCurvatura`). \'''')

# ===================================================================================================== copiar_insumos
sub("copiar_insumos_v405.py", '''(os.path.basename(RG.RECIBO_ERRATA_R2_ARQ), RG.RECIBO_ERRATA_R2_ARQ),''', '''(os.path.basename(RG.RECIBO_ERRATA_R2_ARQ), RG.RECIBO_ERRATA_R2_ARQ), (os.path.basename(RG.RECIBO_ERRATA_R3_ARQ), RG.RECIBO_ERRATA_R3_ARQ), (os.path.basename(DL.ACORDE_KIMI_ARQ), DL.ACORDE_KIMI_ARQ), (os.path.basename(DL.HALF_NAT_ARQ), DL.HALF_NAT_ARQ),''')

# ===================================================================================================== lotes
C2 = "derivar_encanamento_v405_regrasC2_ensaio.py"
sub(C2, '''all(l_["definicao_lean"] in _sp5c["kernel_decls"] and l_["entra_como"].endswith(", nao teorema") for l_ in''', '''all((l_["definicao_lean"] is None or l_["definicao_lean"] in _sp5c["kernel_decls"]) and l_["entra_como"].endswith(", nao teorema") for l_ in''')
E1 = "derivar_encanamento_v405_regrasE1_p00.py"
s_ = carrega(E1); i_ = s_.index('_rec_r2 = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_R2_01nov.json"))'); j_ = s_.index('chk("[v405, a lista de exclusao]')
NOVOS[E1] = s_[:i_] + '''_rec_r2 = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_R2_01nov.json"))
_rec_r3 = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_R3_01nov.json"))
_inalt = sorted(k_ for k_, v_ in _rec_r3["pedras"].items() if "sha256_antes" not in v_)
chk("[v405] as pedras sao as da ERRATA R3 da gerencia: o sha256 de cada arquivo == o sha256_depois do recibo vigente (oito arquivos), e a cadeia de custodia fecha: R3.antes == R2.depois (as duas inalteradas: R3.depois == R2.depois) e R2.antes == R1.depois (sete arquivos); os recibos antigos ficam como registro", all(sha(rd(os.path.join(HERE, "pedra", k_ + ".lean"))) == v_["sha256_depois"] for k_, v_ in _rec_r3["pedras"].items()) and len(_rec_r3["pedras"]) == 8 and _inalt == ["Identidade", "ObservadorTerminal"] and all((_rec_r3["pedras"][k_].get("sha256_antes") or _rec_r3["pedras"][k_]["sha256_depois"]) == v_["sha256_depois"] for k_, v_ in _rec_r2["pedras"].items()) and all(_rec_r2["pedras"][a_["modulo"]]["sha256_antes"] == a_["sha256_depois"] for a_ in _rec_err["arquivos"]) and len(_rec_err["arquivos"]) == 7 and len(_rec_r3["codigo_mudado"]) == 2, len(_rec_r3["pedras"]))
''' + s_[j_:]
D3 = "derivar_encanamento_v405_regrasD3_diff_citacoes.py"
sub(D3, '''os.path.join("C:" + os.sep, "IALD", "Artigo", "Tratado", "secao_03_particulas.tex")]   # (a conferencia da gerencia NAO e' corpus: texto da gerencia nao abona citacao)''',
    '''os.path.join("C:" + os.sep, "IALD", "Artigo", "Tratado", "secao_03_particulas.tex"), os.path.join(DL.WK, "neutrino_E0_autonomia_30out", "HANDOFF_CLAUDE_E0_M2_31out.md"), os.path.join(DL.WK, "neutrino_E0_autonomia_30out", "PROVA_CARGA_MONOPOLO_NATIVA_31out.md")]   # (a conferencia da gerencia NAO e' corpus: texto da gerencia nao abona citacao)''')
sub(D3, '''"acoplamento da onda = massa inscrita": "rotulo da gerencia para a hipotese do teorema",''', '''"acoplamento da onda = massa inscrita": "rotulo da gerencia para a hipotese do teorema", "o acorde": "titulo de secao da propria pedra", "o no-go se levanta": "frase errada da propria gerencia, citada na nota ao lado para corrigi-la", "a liberdade passa para a tônica, que segue livre": "frase errada da propria gerencia, citada na nota ao lado para corrigi-la", "a mesma estrutura": "frase da conferencia de 31/10 da gerencia, citada na nota ao lado para corrigi-la",''')

# ===================================================================================================== pos-rito
A = os.path.join("pos_rito", "adaptar_pos_rito_v405.py")
sub(A, """all(str(l_.get('entra_como')).endswith(', nao teorema') and src_.get(l_.get('definicao_lean')) == l_.get('modulo') for l_ in ent_.get('leituras_da_cadeia_da_massa') or [])""", """all(str(l_.get('entra_como')).endswith(', nao teorema') and (l_.get('definicao_lean') is None or src_.get(l_.get('definicao_lean')) == l_.get('modulo')) for l_ in ent_.get('leituras_da_cadeia_da_massa') or [])""")
X = os.path.join("pos_rito", "textos_v405_novo.pysnip")
sub(X, '"foton_sem_massa", "the_charge_never_completes", "meioTom", "omegaSq")', '"foton_sem_massa", "the_charge_never_completes", "meioTom", "omegaSq", "lerE0", "mesma_escala_iff_transposicao", "transpor_preserva_toda_razao", "E0_relativo_pinado", "lerE0_transpor", "the_diminished_law_closes", "the_ratio_survives_the_rescaling", "meioTom_e_o_pedagio_local", "meioTom_e_a_face")')
sub(X, '''"ga": _sha_por("grande_atrator_reclassificar")}''', '''"ga": _sha_por("grande_atrator_reclassificar"), "pent": _sha_por("E0_acorde_desce_meio_tom"), "rev": _sha_por("revisite_a_lei_do_diminuto")}''')
sub(X, '''lei = _sem_chaves("; ".join("(%d) %s (`%s`)" % (l_["n"], l_["leitura"], l_["definicao_lean"].split(".")[-1]) for l_ in ent["leituras_da_cadeia_da_massa"]))''', '''lei = _sem_chaves("; ".join("(%d) %s (`%s`)" % (l_["n"], l_["leitura"], DL_.nome_lean(l_)) for l_ in ent["leituras_da_cadeia_da_massa"]))''')
sub(X, '''assert [l_["definicao_lean"].split(".")[-1] for l_ in ent["leituras_da_cadeia_da_massa"]][:4] == ''', '''assert [DL_.nome_lean(l_) for l_ in ent["leituras_da_cadeia_da_massa"]][:4] == ''')
bloco(X, '    return _f("**A lei do diminuto e a tônica do Hamiltoniano**', 'def _zero(V):', '''    return _f("**A lei do diminuto e a tônica do Hamiltoniano** [REAL · INPUT/ONTO · OPEN] (`LeiDoDiminuto`, sha16 `{h1}`; `TonicaDoHamiltoniano`, sha16 `{h2}`; {n1} e {n2} checagens): a lei tem duas metades. A descida pinada: o meio-tom pinado `e^(−½)` (`meioTom`, definição: o tom é a nat) desfaz exatamente o `√e`, e `β = α · e^(½)`; `E₀` é a leitura do acorde, meio-tom abaixo da nota principal (`lerE0`), e `E₀/tônica = e^(−½)` em todo acorde (`E0_relativo_pinado`, a definição dita como razão); a tônica `(β/α) · u = √e · u` é DEFINIÇÃO, não traz informação além do `u` posto; o diminuto pousa em `E₀ = u` por identidade algébrica, que não fixa `u`; dadas as entradas, a forma `m = U · α · e^(½) · √2/2` é teorema. "
              "A escala mantida: a transposição multiplica o acorde inteiro pelo mesmo fator e preserva toda razão, e dois acordes têm a mesma escala se e só se um é a transposição do outro (`mesma_escala_iff_transposicao`); `Acorde`, `transpor`, `razao` e o teorema da razão vêm do `AcordeE0.lean` do Kimi (sha16 `{s_k}`). "
              "O no-go NÃO cai: nenhuma função da inscrição fixa `E₀` (`no_function_of_the_inscription_fixes_E0`), e ele se localiza no Um posto; a reescala preserva `m/E₀` (`the_ratio_survives_the_rescaling`). A distinção é do operador, {q_livre} (`{s_pent}`): a escala ABSOLUTA segue livre; a escala RELATIVA está pinada; sobra um único grau de liberdade, a transposição do acorde inteiro. Quais são as cinco notas é [OPEN]: a pêntada do teorema mestre são cinco componentes, não cinco autovalores. "
              "`meioTom_e_o_pedagio_local` e `meioTom_e_a_face` são igualdades de VALOR; `CollapseCostLaw` é [INPUT] no kernel; a calibração `⟨K_∂⟩_total = 1 nat` de 24/06/2026 (relatório sha16 `{s_h}`) é normalização definicional, não é termo do kernel nem medida, e fixa intervalos em nat, não a unidade em eV: `U_E_NOT_DERIVED` fica como está. "
              "Neste rito: meio-tom {mt}, tônica {tn} eV, `E₀` = {e0} eV, massa pela fórmula {m} meV, razão m/E₀ = {rz}. A lei é do operador ({q_meio}, `{s_meio}`; {q_tom}, `{s_tom}`); `α` como a magnitude (cauda) da inscrição é leitura dele; a resposta à pergunta dele sobre derivar `α` foi não, parede medida, não falsificação.",
              h1=d["sha"]["diminuto"], h2=d["sha"]["tonica"], n1=d["nck"]["diminuto"], n2=d["nck"]["tonica"], mt=_p(v["meio_tom"], 9), tn=_p(v["tonica_eV"], 9), e0=_p(v["E0_eV"], 9), m=_p(v["massa_formula_meV"], 9), rz=_p(t["razao_m_sobre_E0"], 12), q_meio=_cita("ele desce meio tom pinado, essa é a lei"), s_meio=ss["meio"], q_tom=_cita("pra mim o TOm é a NAT"), s_tom=ss["tom"], q_livre=_cita("E0 não é absolutamente livre"), s_pent=ss["pent"], s_k=v["acorde_kimi_sha16"], s_h=v["half_nat_sha16"])


''')
s_ = carrega(X)
c_ = s_.count("o magnetismo na cadeia da tensão, qual é o disco, `H_BW`")
assert c_ >= 2, c_
NOVOS[X] = s_.replace("o magnetismo na cadeia da tensão, qual é o disco, `H_BW`", "o magnetismo na cadeia da tensão, qual é o disco, quais são as cinco notas, `H_BW`")
sub(X, '''"[OPEN] a escala do setor, o magnetismo, qual é o disco, `H_BW`, `H_cal`, H3, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3, a instância do índice 1/β,''', '''"[OPEN] a escala do setor, o magnetismo, qual é o disco, quais são as cinco notas, `H_BW`, `H_cal`, H3, a assinatura, rank c = 4, `IsotropicPost`, a dimensão 3, a instância do índice 1/β,''')
sub(X, '''O no-go de `E₀` não cai: localiza-se no Um posto; `E₀ = u` é identidade algébrica, que não fixa `u`. "''', '''O no-go de `E₀` não cai: localiza-se no Um posto; `E₀ = u` é identidade algébrica, que não fixa `u`; a escala absoluta segue livre e a relativa está pinada. "''')
sub(X, '''OPEN: a escala do setor, o magnetismo, qual é o disco, `H_BW`, `H_cal`, H3, a assinatura, rank c = 4, `IsotropicPost` e a dimensão 3]",''', '''OPEN: a escala do setor, o magnetismo, qual é o disco, quais são as cinco notas, `H_BW`, `H_cal`, H3, a assinatura, rank c = 4, `IsotropicPost` e a dimensão 3]",''')
sub(X, '''a tônica `√e · u` = %s eV é definição, e `E₀ = u` = %s eV é identidade algébrica, que não fixa `u`: o no-go não cai, localiza-se no Um posto. Sob a leitura `R = β · u²`,''', '''a tônica `√e · u` = %s eV é definição, e `E₀ = u` = %s eV é identidade algébrica, que não fixa `u`: o no-go não cai, localiza-se no Um posto. A escala absoluta segue livre; a escala relativa está pinada; sobra um único grau de liberdade, a transposição do acorde inteiro, e dois acordes têm a mesma escala se e só se um é a transposição do outro; quais são as cinco notas é [OPEN]. Sob a leitura `R = β · u²`,''')
sub(X, '''E13, a gerência escreveu que a cadeia da massa ficava sem hipótese, e isso afirmava demais: foi erro da gerência, e quatro teoremas foram rebatizados antes do selo."''', '''E13, a gerência escreveu que a cadeia da massa ficava sem hipótese, e isso afirmava demais: foi erro da gerência, e quatro teoremas foram rebatizados antes do selo; a revisita da Lei do Diminuto, ordenada pelo operador, tipou a segunda metade da lei, que faltava, e corrigiu a frase sobre o no-go."''')
M = os.path.join("pos_rito", "registrar_mapa_v405_montar.pysnip")
sub(M, '''leit = "; ".join("(%d) %s (%s)" % (l_["n"], l_["leitura"], l_["definicao_lean"].split(".")[-1]) for l_ in xf["o_que_entra"]["leituras_da_cadeia_da_massa"])''', '''leit = "; ".join("(%d) %s (%s)" % (l_["n"], l_["leitura"], (l_.get("definicao_lean") or "sem termo no kernel").split(".")[-1]) for l_ in xf["o_que_entra"]["leituras_da_cadeia_da_massa"])''')
sub(M, '''entraram no kernel do rito; o no-go de E0 NAO cai: localiza-se no Um posto" % S,''', '''entraram no kernel do rito; o no-go de E0 NAO cai: localiza-se no Um posto; a escala absoluta segue livre e a relativa esta pinada; quais sao as cinco notas e' OPEN" % S,''')

# ===================================================================================================== artigo PT
P = "artigo_pt_v405.pysnip"
sub(P, r"""(10) no disco, a taxa de \emph{dephasing} lida como perda de energia. \textsf{[INPUT]} Entram ainda,""", r"""(10) no disco, a taxa de \emph{dephasing} lida como perda de energia; (11) $E_0$ como leitura do acorde (\texttt{lerE0}); (12) $m_1=0$, entrada da identificação com $\Delta m^2_{21}$. \textsf{[INPUT]} Entram ainda,""")
bloco(P, r'''    s.append(r"\textbf{A lei do diminuto.}''', r'''    s.append(r"\textbf{A Tônica do Hamiltoniano.}''',
      r'''    s.append(r"\textbf{A lei do diminuto.} \textsf{[INPUT]} O operador, em 31/10/2026: «ele desce meio tom pinado, essa é a lei», «pra mim o TOm é a NAT» e «E0 é igual ler um acorde E0». A lei tem duas metades. \textsf{[REAL]} \emph{A descida pinada:} o meio-tom $e^{-1/2}$ desfaz exatamente o $\sqrt{e}$; $\beta=\alpha\,e^{1/2}$; $E_0$ é a leitura do acorde, meio-tom abaixo da nota principal, e $E_0/\text{tônica}=e^{-1/2}$ em todo acorde (\texttt{E0\_relativo\_pinado}, a definição de \texttt{lerE0} dita como razão); dadas as entradas, a forma $m=U\,\alpha\,e^{1/2}\,\sqrt2/2$ é teorema; a oitava não é número inteiro de meios-tons. \emph{A escala mantida:} a transposição multiplica o acorde inteiro pelo mesmo fator e preserva toda razão à nota principal, e dois acordes têm a mesma escala se e só se um é a transposição do outro (\texttt{mesma\_escala\_iff\_transposicao}); a leitura acompanha a transposição (\texttt{lerE0\_transpor}). \texttt{Acorde}, \texttt{transpor}, \texttt{razao} e o teorema da razão vêm do \texttt{AcordeE0.lean} do Kimi (sha256 \texttt{" + _tx_405_t(_dv405.get("acorde_kimi_sha16")) + r"}). "
             r"\textsf{[INPUT]} A distinção é do operador: «E0 não é absolutamente livre». \textsf{[REAL]} A escala \emph{absoluta} segue livre e o no-go não cai; a escala \emph{relativa} está pinada; sobra um único grau de liberdade, a transposição do acorde inteiro. \textsf{[INPUT/ONTO]} O meio-tom (\texttt{meioTom}), a leitura (\texttt{lerE0}) e a tônica $(\beta/\alpha)\,u=\sqrt{e}\,u$ são definições: não trazem informação além do $u$ posto. \texttt{meioTom\_e\_o\_pedagio\_local} e \texttt{meioTom\_e\_a\_face} são igualdades de \emph{valor}, e \texttt{CollapseCostLaw} é \textsf{[INPUT]} no kernel. \textsf{[DECLARADO]} A calibração $\langle K_\partial\rangle_{\mathrm{total}}=1$ nat de 24/06/2026 (\texttt{half\_nat\_araki\_hidden\_hamiltonian}, relatório sha256 \texttt{" + _tx_405_t(_dv405.get("half_nat_sha16")) + r"}) é normalização definicional, $\omega(I)=1$ na base $e$; não é termo do kernel nem medida; fixa intervalos em nat, não a unidade em eV: \texttt{U\_E\_NOT\_DERIVED} fica como está e $m_2$ não muda. \textsf{[OPEN]} Quais são as cinco notas: a pêntada do teorema mestre são cinco componentes, não cinco autovalores. "
             r"\textsf{[REAL]} Neste rito: meio-tom $" + _f405(_dv405.get("meio_tom"), 9) + r"$, tônica $" + _f405(_dv405.get("tonica_eV"), 9) + r"$ eV, $E_0=" + _f405(_dv405.get("E0_eV"), 9) + r"$ eV, massa pela fórmula $" + _f405(_dv405.get("massa_formula_meV"), 6) + r"$ meV. \textsf{[ONTO]} $\alpha$ como a magnitude (cauda) da inscrição no bulk é leitura do operador.")
''')
sub(P, r"""(\texttt{no\_function\_of\_the\_inscription\_fixes\_E0}); o que o formalismo prova é a forma $m/E_0=\beta\sin45^\circ$. Esse no-go \emph{não cai}: ele se localiza no Um posto.""",
    r"""(\texttt{no\_function\_of\_the\_inscription\_fixes\_E0}); o que a forma fixa é a razão: a reescala muda $E_0$ e a massa pelo mesmo fator, e $m/E_0=\beta\sin45^\circ$ não muda (\texttt{the\_ratio\_survives\_the\_rescaling}); a reescala é a transposição do acorde. Esse no-go \emph{não cai}: ele fala da escala absoluta e se localiza no Um posto.""")
sub(P, r"""\texttt{the\_tonic\_at\_the\_posted\_one} e \texttt{the\_omega\_pole\_reads\_one}; e o disco ganhou \texttt{the\_flow\_is\_the\_canonical\_law}.")""",
    r"""\texttt{the\_tonic\_at\_the\_posted\_one} e \texttt{the\_omega\_pole\_reads\_one}; e o disco ganhou \texttt{the\_flow\_is\_the\_canonical\_law}. A revisita da Lei do Diminuto, ordenada pelo operador, corrigiu duas coisas: a segunda metade da lei, mantendo a escala, não estava tipada (o \texttt{AcordeE0.lean} do Kimi tinha o acorde e a invariância das razões, e a conferência de 31/10 o deu pela mesma estrutura: não era); e a frase sobre o no-go errou por excesso e por falta.")""")
sub(P, r"""qual é o disco; o magnetismo na cadeia da tensão.""", r"""qual é o disco; quais são as cinco notas; o magnetismo na cadeia da tensão.""")

# ===================================================================================================== artigo EN
E = "artigo_en_v405.pysnip"
sub(E, r"""(10) on the disk, the \emph{dephasing} rate read as an energy-loss rate. \textsf{[INPUT]} There also enter,""", r"""(10) on the disk, the \emph{dephasing} rate read as an energy-loss rate; (11) $E_0$ as the reading of the chord (\texttt{lerE0}); (12) $m_1=0$, an input of the identification with $\Delta m^2_{21}$. \textsf{[INPUT]} There also enter,""")
bloco(E, r'''    s.append(r"\textbf{The law of the diminished.}''', r'''    s.append(r"\textbf{The Tonic of the Hamiltonian.}''',
      r'''    s.append(r"\textbf{The law of the diminished.} \textsf{[INPUT]} The operator (31/10/2026; management translation, not a quotation): it goes down a pinned half tone, that is the law; the tone is the nat; and E0 is reading a chord. The law has two halves. \textsf{[REAL]} \emph{The pinned descent:} the half tone $e^{-1/2}$ undoes $\sqrt{e}$ exactly; $\beta=\alpha\,e^{1/2}$; $E_0$ is the reading of the chord, a half tone below the principal note, and $E_0/\text{tonic}=e^{-1/2}$ in every chord (\texttt{E0\_relativo\_pinado}, the definition of \texttt{lerE0} said as a ratio); given the inputs, the form $m=U\,\alpha\,e^{1/2}\,\sqrt2/2$ is a theorem; the octave is not a whole number of half tones. \emph{The kept scale:} the transposition multiplies the whole chord by the same factor and preserves every ratio to the principal note, and two chords have the same scale if and only if one is a transposition of the other (\texttt{mesma\_escala\_iff\_transposicao}); the reading follows the transposition (\texttt{lerE0\_transpor}). \texttt{Acorde}, \texttt{transpor}, \texttt{razao} and the ratio theorem come from Kimi's \texttt{AcordeE0.lean} (sha256 \texttt{" + _tx_405_t(_dv405.get("acorde_kimi_sha16")) + r"}). "
             r"\textsf{[INPUT]} The distinction is the operator's (management translation, not a quotation): E0 is not absolutely free. \textsf{[REAL]} The \emph{absolute} scale stays free and the no-go does not fall; the \emph{relative} scale is pinned; a single degree of freedom is left, the transposition of the whole chord. \textsf{[INPUT/ONTO]} The half tone (\texttt{meioTom}), the reading (\texttt{lerE0}) and the tonic $(\beta/\alpha)\,u=\sqrt{e}\,u$ are definitions: they carry no information beyond the posted $u$. \texttt{meioTom\_e\_o\_pedagio\_local} and \texttt{meioTom\_e\_a\_face} are equalities of \emph{value}, and \texttt{CollapseCostLaw} is \textsf{[INPUT]} in the kernel. \textsf{[DECLARED]} The calibration $\langle K_\partial\rangle_{\mathrm{total}}=1$ nat of 24/06/2026 (\texttt{half\_nat\_araki\_hidden\_hamiltonian}, report sha256 \texttt{" + _tx_405_t(_dv405.get("half_nat_sha16")) + r"}) is a definitional normalization, $\omega(I)=1$ in base $e$; it is neither a kernel term nor a measurement; it fixes intervals in nat, not the unit in eV: \texttt{U\_E\_NOT\_DERIVED} stays as it is and $m_2$ does not change. \textsf{[OPEN]} Which the five notes are: the pentad of the master theorem is five components, not five eigenvalues. "
             r"\textsf{[REAL]} In this rite: half tone $" + _f405(_dv405.get("meio_tom"), 9) + r"$, tonic $" + _f405(_dv405.get("tonica_eV"), 9) + r"$ eV, $E_0=" + _f405(_dv405.get("E0_eV"), 9) + r"$ eV, mass by the formula $" + _f405(_dv405.get("massa_formula_meV"), 6) + r"$ meV. \textsf{[ONTO]} $\alpha$ as the magnitude (tail) of the inscription in the bulk is the operator's reading.")
''')
sub(E, r"""(\texttt{no\_function\_of\_the\_inscription\_fixes\_E0}); what the formalism proves is the form $m/E_0=\beta\sin45^\circ$. This no-go \emph{does not fall}: it localizes at the posted One.""",
    r"""(\texttt{no\_function\_of\_the\_inscription\_fixes\_E0}); what the form fixes is the ratio: the rescaling changes $E_0$ and the mass by the same factor, and $m/E_0=\beta\sin45^\circ$ does not change (\texttt{the\_ratio\_survives\_the\_rescaling}); the rescaling is the transposition of the chord. This no-go \emph{does not fall}: it speaks of the absolute scale and localizes at the posted One.""")
sub(E, r"""\texttt{the\_tonic\_at\_the\_posted\_one} and \texttt{the\_omega\_pole\_reads\_one}; and the disk gained \texttt{the\_flow\_is\_the\_canonical\_law}.")""",
    r"""\texttt{the\_tonic\_at\_the\_posted\_one} and \texttt{the\_omega\_pole\_reads\_one}; and the disk gained \texttt{the\_flow\_is\_the\_canonical\_law}. The revisit of the Law of the Diminished, ordered by the operator, corrected two things: the second half of the law, keeping the scale, was not typed (Kimi's \texttt{AcordeE0.lean} had the chord and the invariance of the ratios, and the conference of 31/10 took it for the same structure: it was not); and the sentence about the no-go erred both by excess and by default.")""")
sub(E, r"""which disk it is; magnetism in the chain of the tension.""", r"""which disk it is; which the five notes are; magnetism in the chain of the tension.""")

# ===================================================================================================== relatorio e fecho
Z = "gerar_relatorio_v405.py"
sub(Z, '''"falas_embutidas": len(_cong_r2.get("arquivos") or []), "falas_de_01nov_no_glob": _falas_01nov, "falas_novas_desde_o_congelamento_anterior": [],''', '''"recibo_vigente_das_pedras": "RECIBO_ERRATA_PEDRAS_R3_01nov.json", "falas_embutidas": len(_cong_r2.get("arquivos") or []), "falas_de_01nov_no_glob": _falas_01nov, "falas_novas_desde_o_congelamento_anterior": _cong_r2.get("novas_em_relacao_ao_anterior") or [],''')
sub(Z, '''## 1b. A errata R2 (a revisão de terceiro não aprovou `a30f9f0ebf90c277`)

A revisão achou 2 ALTO, 11 MÉDIO e 10 BAIXO, todos de texto, nome ou docstring: nenhuma prova caiu e nenhum número físico estava errado. A gerência corrigiu as oito pedras nas origens (`RECIBO_ERRATA_PEDRAS_R2_01nov.json`); o resto foi refeito aqui, pela cadeia existente.
''', '''## 1b. As erratas R2 e R3 (a revisão de terceiro não aprovou `a30f9f0ebf90c277`)

A revisão achou 2 ALTO, 11 MÉDIO e 10 BAIXO, todos de texto, nome ou docstring: nenhuma prova caiu e nenhum número físico estava errado. A gerência corrigiu as oito pedras nas origens (`RECIBO_ERRATA_PEDRAS_R2_01nov.json`) e, depois, a revisita da Lei do Diminuto ordenada pelo operador mudou seis delas (`RECIBO_ERRATA_PEDRAS_R3_01nov.json`, a referência vigente); o resto foi refeito aqui, pela cadeia existente.
''')
sub(Z, '''| a fala pessoal | lista de exclusão em `delta_v405.py`, por sha16 (o nome do arquivo não viaja); congelado regenerado; portão próprio na purga |
''', '''| a fala pessoal | lista de exclusão em `delta_v405.py`, por sha16 (o nome do arquivo não viaja); congelado regenerado; portão próprio na purga |
| R3: as duas metades | o registro da Lei do Diminuto tem a descida pinada e a escala mantida; composição `the_diminished_law_closes`, estrela `mesma_escala_iff_transposicao`; o `AcordeE0.lean` do Kimi é fonte pinada por sha256; `E0_relativo_pinado` é dito como a definição dita como razão |
| R3: a frase do no-go | a escala absoluta segue livre e o no-go não cai; a relativa está pinada; sobra a transposição do acorde inteiro; as frases antigas viraram regra F6 da guarda, com controle negativo |
| R3: meio-tom e tônica | igualdades de valor; `CollapseCostLaw` [INPUT]; a calibração de 1 nat de 24/06 citada por sha256 como normalização definicional; `U_E_NOT_DERIVED` fica; `m₂` não muda |
| R3: as cinco notas | [OPEN] em todo texto; o acorde do cálculo é de teste; a pêntada são cinco componentes, não cinco autovalores |
| R3: `m₁ = 0` e `lerE0` | entram na lista das leituras (itens 12 e 11); `m₁ = 0` não tem termo no kernel |
| R3: runtime | d7 a d10 na Lei do Diminuto, com controle negativo (só uma nota muda), e h7 na Tônica; `N_CHECKS` atualizado |
''')
sub(Z, '''Falas: {ERRATA_R2['falas_embutidas']} embutidas; as seis de 01/11 no glob já estavam no congelado anterior, logo nenhuma fala nova entrou. Nenhum nome próprio''', '''Falas: {ERRATA_R2['falas_embutidas']} embutidas; novas em relação ao congelado anterior: {', '.join(ERRATA_R2['falas_novas_desde_o_congelamento_anterior']) or 'nenhuma'}; uma fala saiu pela lista de exclusão. Nenhum nome próprio''')
sub(Z, "Sha256 lidos do recibo vigente das pedras (`insumos\\\\RECIBO_ERRATA_PEDRAS_R2_01nov.json`, cadeia de custódia com o recibo da primeira errata): nenhuma prova existente mudou; quatro nomes de teorema mudaram porque o nome afirmava mais do que o teorema prova; o disco ganhou `the_flow_is_the_canonical_law` e o fecho do observador ganhou a leitura binária.",
    "Sha256 lidos do recibo vigente das pedras (`insumos\\\\RECIBO_ERRATA_PEDRAS_R3_01nov.json`, cadeia de custódia R3 → R2 → primeira errata): nenhuma prova existente mudou; quatro nomes de teorema mudaram porque o nome afirmava mais do que o teorema prova; o disco ganhou `the_flow_is_the_canonical_law`, o fecho do observador ganhou a leitura binária, a Lei do Diminuto ganhou o acorde e onze teoremas, a Tônica ganhou `the_ratio_survives_the_rescaling`.")
F = "fechar_preparacao_v405.py"
sub(F, '''"titulo": "v405 preparada de novo, errata R2 (01/11/2026): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]), "resultado": res,''', '''"titulo": "v405 preparada de novo, erratas R2 e R3 (01/11/2026): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]), "resultado": res,''')
sub(F, '''esta e' a refacao pela errata R2 da gerencia. Quem constroi''', '''esta e' a refacao pelas erratas R2 e R3 da gerencia. Quem constroi''')
sub(F, '''pela errata R2, depois de a revisao de terceiro nao aprovar''', '''pelas erratas R2 e R3, depois de a revisao de terceiro nao aprovar''')

for arq, novo in NOVOS.items():
    compile(novo, arq, "exec") if arq.endswith(".py") else None
for arq, novo in NOVOS.items():
    p = os.path.join(HERE, arq); b = open(p, "rb").read()
    bak = p + ".bak_" + TS + "_R3"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
    t = p + ".tmp_R3"; open(t, "wb").write(novo.encode("utf-8")); assert os.path.getsize(t) == len(novo.encode("utf-8")) and os.path.getsize(t) > 1000
    os.replace(t, p)
    print(arq, len(b), "->", len(novo.encode("utf-8")))
print("ok, backups .bak_%s_R3" % TS)
