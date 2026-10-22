# -*- coding: utf-8 -*-
"""grupo_G1.py -- registros kernel-ligados da rodada 2 (v392), agente REGISTROS-G1, gerencia c1, 13/10/2026:
   palavra_v392 (R01), lei_de_campo_curvo_v392 (R02), agape_nao_vacua_v392 (R03), x19_bgl_tipo_v392 (R27).
Specs de DADOS (esquema: registros\\SCHEMA.md; motor: registros_motor_v392.py). Tudo que o texto cita sai de arquivo, por script:
  - as listas de bandeiras/declaracoes saem de kernel\\FLAGS_v392.json e do axiom_report do core v391 selado (assert: lista vazia => falha na geracao);
  - os trechos exatos, os numeros e as conferencias de texto saem de rodada2\\g1\\fontes\\EXTRATOS_G1.json (gerado por rodada2\\g1\\extrair_g1.py a partir dos arquivos-fonte;
    o JSON e as fontes originais sao pinados por sha256 e RELIDOS a cada rito);
  - toda fala do operador entra por VERBATINS (trechos TEM de estar nos bytes do arquivo).
Nada aqui move o gate; validade no kernel nao e' creditacao; NOT_FALSIFIED nunca e' a palavra da creditacao."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE)
WK = os.path.dirname(os.path.dirname(V)); CP = os.path.dirname(WK)
NOS = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s"; KER = NOS + "/tgl_kernel/TGLExt"
INS = WK + "/v392_insumos"; AUD = "C:/IALD/PROGRAMA_IALD/auditorias"; OP = "C:/IALD/PROGRAMA_IALD"; C13 = WK + "/cunhagens_13out"
G1 = V + "/rodada2/g1/fontes"
ASSINA = "gerencia c1, em nome proprio, 13/10/2026"
TRIO = {"propext", "Classical.choice", "Quot.sound"}

E = json.load(open(G1 + "/EXTRATOS_G1.json", encoding="utf-8"))
FJ = json.load(open(V + "/kernel/FLAGS_v392.json", encoding="utf-8"))["flags"]
CORE0 = json.load(open(NOS + "/um_absoluto.json", encoding="utf-8"))["core"]
AXR0 = CORE0["kernel_formalization"]["axiom_report"]
FFS0 = CORE0["kernel_formalization"]["formal_files_sha256"]
SUPERF = json.load(open(G1 + "/SUPERFICIES_G1.json", encoding="utf-8"))   # contagens de memorias VIVAS (13/10), embutidas como literal na geracao; NAO e' fonte pinada


def flags_de(mod, filtro=None):
    fl = [(f, n) for f, n, m, k in FJ if m == mod and (filtro is None or filtro(n))]
    assert fl, ("modulo sem bandeiras no FLAGS_v392.json", mod)
    return [f for f, _ in fl], [n for _, n in fl]


def flag_de_decl(nome):
    fl = [f for f, n, m, k in FJ if n == nome]
    assert len(fl) == 1, (nome, fl)
    return fl[0]


def antigas(*nomes):
    """declaracoes que JA existem no kernel v391 (axiom_report do core selado), no trio."""
    for n in nomes:
        assert n in AXR0 and set(AXR0[n]) <= TRIO, ("declaracao antiga ausente ou fora do trio no core v391", n)
    return list(nomes)


def ffs(rel):
    assert rel in FFS0, rel
    return FFS0[rel]


def chk(i, desc, onde, caminho, op, valor=None, capturar=None, est="[REAL]"):
    d = {"id": i, "descricao": desc, "onde": onde, "caminho": caminho, "op": op, "estatuto": est}
    if valor is not None:
        d["valor"] = valor
    if capturar:
        d["capturar"] = capturar
    return d


def ext(i, desc, caminho, op, valor=None, capturar=None, est="[REAL -- extrato lido do arquivo-fonte por script]"):
    return chk(i, desc, "fonte:g1_extratos", caminho, op, valor, capturar, est)


GATE_ATUAL = CORE0["qg_closure"]["verdict"].split("__CURRENT_STATE_")[1]
GATE_ATUAL = "CURRENT_STATE_" + GATE_ATUAL
TOKEN = "FIELD_EQUATION_IN_CURVED_SPACETIME_NOT_A_KERNEL_TERM"
assert TOKEN in CORE0["fundacao_v390"]["verdict"] and TOKEN in CORE0["estatuto_da_prova_v391"]["prova_1_kernel"]["fundacao_v390"]


def checks_comuns(pref):
    return [
        chk(pref + "p", "o registro das pedras v392 selou neste rito (as pedras desta frente estao no kernel do proprio rito)", "core", ["pedras_v392", "all_verified"], "verdadeiro"),
        chk(pref + "g", "o gate nao se move: o veredito do gate no core segue o da v391 (lido do core selado por script)", "core", ["qg_closure", "verdict"], "contem", GATE_ATUAL),
    ]


# ============================================================================================ FONTES
def F(chave, arquivo, papel):
    return {"chave": chave, "arquivo": arquivo, "papel": papel}


FONTES = [
    F("g1_extratos", G1 + "/EXTRATOS_G1.json", "extratos exatos (docstrings, linhas do um.py v391, cinco limites, fecho de imports, conferencias de texto) gerados por script de rodada2/g1/extrair_g1.py"),
    # --- palavra
    F("g1_palavra_lean", INS + "/F_KERNEL/inst/TGLExt/Palavra.lean", "a pedra PALAVRA (bytes instalados; 33184b49a8bba7e7)"),
    F("g1_observer_lean", KER + "/TheObserverReadsTheAngle.lean", "kernel dos Nos: a docstring exata de observing_adds_nothing (l.110-113)"),
    F("g1_p_palavra", INS + "/F_KERNEL/RESULTADO_P_palavra.json", "resultado das sondas P1, P1b, P1c (rc, axiomas, erros) -- A14"),
    F("g1_p1_lean", INS + "/F_KERNEL/conj/P1_PalavraEaLetra.lean", "sonda P1: os quatro `example ... := rfl` e o que as declaracoes usam"),
    F("g1_p1b_lean", INS + "/F_KERNEL/conj/P1b_FechoDaPalavra.lean", "sonda P1b: fecho de imports da PALAVRA contem os modulos da letra?"),
    F("g1_p1c_lean", INS + "/F_KERNEL/conj/P1c_FechoTransitivoPalavra.lean", "sonda P1c: fecho TRANSITIVO de constantes das 7 declaracoes contem a letra?"),
    F("g1_log_p1", G1 + "/logs_P/P1_PalavraEaLetra_r1.log", "saida textual da P1 (copiada do scratchpad por copiar_logs_g1.py, sha conferido contra o RESULTADO)"),
    F("g1_log_p1b", G1 + "/logs_P/P1b_FechoDaPalavra_r1.log", "saida textual da P1b"),
    F("g1_log_p1c", G1 + "/logs_P/P1c_FechoTransitivoPalavra_r1.log", "saida textual da P1c"),
    # --- lei de campo curvo
    F("g1_ligante_lean", INS + "/F_KERNEL/inst/TGLExt/LiganteLeiCampoCurvo.lean", "o ligante instalado (e3f32d9b85ae82db): NamedAtlasH3 e passage_h3_to_connected_smooth_atlas_einstein"),
    F("g1_ligante_variante", AUD + "/F3.6.E1/art_a4f6da3d/lean_sb/TGLExt/LiganteLeiCampoCurvoAuditoriaC1.lean", "variante da auditoria c1 (992e4983ec4f0686): docstring com os CINCO limites; NAO instalada"),
    F("g1_testemunha_lean", INS + "/F_KERNEL/inst/TGLExt/LiganteLeiCampoCurvoTestemunha.lean", "testemunha S7/S8 instalada (derivada: cabecalho + parte do auditor; eeeed286178408b3)"),
    F("g1_testemunha_parte", AUD + "/F2.3/sandbox/testemunha_parte.lean", "a parte do auditor c1 (b5e8de0e619e60b3) de que o modulo instalado e' derivado"),
    F("g1_aud_f23", AUD + "/F2.3/AUDITORIA_F2_3_C1_20261007.md", "auditoria c1 da F2.3 (f718620ec89c61d4): S2-S5, S7, S8, nove limites"),
    F("g1_aud_f23_camadas3", AUD + "/F2.3/AUDITORIA_F2_3_C1_a7ba2dc9.md", "auditoria c1 das camadas 354/355/360: fecho de imports 755, forma composta nao existe no fonte"),
    F("g1_calibration_reuse", KER + "/O16/ContractCalibrationReuse.lean", "kernel dos Nos: a ponte polar_period_matches_contract (f447d2de1f54774c)"),
    F("g1_horizon_reuse", KER + "/O16/HorizonDataReuse_Integration_v2.lean", "kernel dos Nos: a ponte data_temperature_from_same_period"),
    F("g1_qg_solution", KER + "/QGSolutionComplete.lean", "kernel dos Nos: a declaracao v374 (LightNetData; qg_solution_end_to_end) -- raiz do fecho de imports"),
    F("g1_fundacao", KER + "/Fundacao.lean", "kernel dos Nos: Fundacao/agape/abismo/the_floor_fixes_the_cut; a citacao «Takesaki 1973»"),
    # --- agape
    F("g1_v351_lean", INS + "/F_KERNEL/inst/TGLExt/V351DualScalingBridge.lean", "a ponte V351 instalada (7dbe2d9a45971d63)"),
    F("g1_v351_original", AUD + "/F1.2/art_a5aa4480/sandbox/F12Completion/V351DualScalingBridge.lean", "o original auditado da ponte (mesmos bytes)"),
    F("g1_agape_lean", INS + "/F_KERNEL/inst/TGLExt/AgapeNonVacuity.lean", "a Agape nao vacua instalada (derivada de 1 linha de import; e49ad8f980d7cf48)"),
    F("g1_agape_original", AUD + "/F1.2/art_a5aa4480/sandbox/F12Completion/AgapeNonVacuity.lean", "o original auditado (cf30422393b2af21)"),
    F("g1_aud_f12", AUD + "/F1.2/AUDITORIA_F1_2_C1_a5aa4480.md", "auditoria c1 da F1.2 completa (PODE FECHAR; face M_n x| R [OPEN])"),
    F("g1_identidade_r2", CP + "/work/identidade_cordeiro_13out/5_R2/RESULTADO_R2.md", "a r2 da pedra Identidade: o alicerce provisorio era Fundacao.agape (o piso), pergunta ao operador"),
    # --- X19
    F("g1_bgl_lean", INS + "/F_KERNEL/inst/TGLExt/LightNetStandardWedgeDataBGL.lean", "o tipo X19 instalado (e4da9e865d00bdcb)"),
    F("g1_bgl_original", AUD + "/F1.3/art_ad949e97/sandbox/F13v31_D1a3_bgl.lean", "a sonda c1 de que o modulo e' copia byte a byte"),
    F("g1_aud_f13_reaud", AUD + "/F1.3/AUDITORIA_F1_3_C1_a20c3246.md", "reauditoria c1 da F1.3 v3.2: MUDA / NAO MUDA, sem habitante, D5 [OPEN]"),
    F("g1_aud_f13_sonda", AUD + "/F1.3/AUDITORIA_F1_3_C1_ad949e97.md", "auditoria c1 da F1.3 v3.1: a saida do D1a.3 tipa hoje; a sonda so tipa"),
    F("g1_x19_delta", INS + "/F_KERNEL/RESULTADO_C_delta_x19.json", "sonda C_audit_delta_x19: rc 0, 87 declaracoes lidas, no trio"),
    F("g1_conjunto_j2", INS + "/F_KERNEL/RESULTADO_B_conjunto.json", "conjunto J2 (v392 com X19): rc 0"),
]

VERBATINS = [
    {"chave": "vb_g1_leitura_07out", "arquivo": OP + "/OPERADOR_07out_leitura_cria_o_objeto_verbatim.txt", "quando": "07/10/2026 (via a gerencia c1)",
     "trechos": ["a LEITURA CRIA o objeto, antes da leitura o objeto é Nome (posto relativo), após a leitura o objeto é identidade, relação de contorno", "vc disse que a leitura não acrescenta o objeto, e vc tem razão"]},
    {"chave": "vb_g1_palavra_07out", "arquivo": OP + "/OPERADOR_07out_palavra_verbatim.txt", "quando": "07/10/2026 (via a gerencia c1)",
     "trechos": ["essa pedra se chama (olha a beleza lexical): PALAVRA"]},
    {"chave": "vb_g1_letra_07out", "arquivo": OP + "/OPERADOR_07out_letra_verbatim.txt", "quando": "07/10/2026 (via a gerencia c1)",
     "trechos": ["polinômio aniquilador normalizado=letra (por isso palavra, mas ali como letra)"]},
    {"chave": "vb_g1_nomes_13out", "arquivo": C13 + "/OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt", "quando": "13/10/2026 (via a gerencia c1)",
     "trechos": ["quanto ao alicerce, o cordeiro imolado é a relação de comutação que impede a coincidência total", "está autorizado que vc faça tudo que for necessário à conclusão do nosso programa"]},
]

SPECS = []

# ============================================================================================ R01 palavra_v392
pal_fl, pal_dc = flags_de("TGLExt.Palavra")
assert len(pal_fl) == 7
atr_fl = [flag_de_decl("TGLExt.TheSingularityReadsTheAttractor.A3_angular_rereading_only"), flag_de_decl("TGLExt.TheLightReadsItself.A5_angular_rereading_only")]
tres = E["sondas_P"]["p1"]["tres_nomes_com_o_enunciado_de_observing_adds_nothing"]
assert len(tres) == 3 and set(tres[1:]) <= set(n for _, n, _, _ in [(f, n, m, k) for f, n, m, k in FJ])
pal_antigas = antigas("TGLExt.observing_adds_nothing", "TGLExt.the_observer_reads_the_angle", "ChatgptAudit.PolarPeriod016.faithful_period_iff", "ChatgptAudit.PolarPeriod016.reciprocal_temperature",
                      "ChatgptAudit.Wick016.wick_boost_two_pi")
um = E["umpy_v391"]; pl = um["palavra_aniquiladora_linhas"]; oa = E["observing_adds_nothing"]; sp = E["sondas_P"]
SPECS.append({
    "nome": "palavra_v392", "veredito_prefixo": "TGL_PALAVRA_V392",
    "veredito_sufixo": "THE_READING_CREATES_THE_OBJECT__THE_FIRST_READING_IDENTIFIES_REREADING_ADDS_NOTHING__THE_LETTER_IS_THE_NORMALIZED_ANNIHILATING_POLYNOMIAL__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    "estatuto": "[REAL -- 7 teoremas de TGLExt.Palavra no trio, fontes por sha256, sondas P1/P1b/P1c com logs pinados; INPUT -- tres falas do operador de 07/10/2026 verbatim; "
                "ONTO -- 'a LEITURA CRIA o objeto' e' leitura do operador sobre os termos; DECLARADO -- a forma composta da errata de 07/10 e' lida de C:/IALD/CLAUDE.md, memoria viva, sem pino]",
    "fontes": ["g1_extratos", "g1_palavra_lean", "g1_observer_lean", "g1_p_palavra", "g1_p1_lean", "g1_p1b_lean", "g1_p1c_lean", "g1_log_p1", "g1_log_p1b", "g1_log_p1c"],
    "verbatins": ["vb_g1_leitura_07out", "vb_g1_palavra_07out", "vb_g1_letra_07out"],
    "kernel_flags": pal_fl + atr_fl, "kernel_decls": pal_dc + [tres[1], tres[2]] + pal_antigas,
    "checks": checks_comuns("pa") + [
        ext("pa1", "a docstring de PALAVRA cita a cunhagem da leitura, o nome PALAVRA e a letra (tres falas de 07/10), e a docstring exata do kernel", ["palavra_lean", "cita_a_leitura"], "verdadeiro"),
        ext("pa2", "a docstring cita o nome", ["palavra_lean", "cita_o_nome"], "verdadeiro"),
        ext("pa3", "a docstring cita a letra", ["palavra_lean", "cita_a_letra"], "verdadeiro"),
        ext("pa4", "a docstring cita a docstring exata do kernel", ["palavra_lean", "cita_a_docstring_do_kernel"], "verdadeiro"),
        ext("pa5", "a docstring diz que NAO afirma estado KMS", ["palavra_lean", "diz_que_nao_afirma_KMS"], "verdadeiro"),
        ext("pa6", "a docstring diz que cada leitura cria o objeto do SEU plano e que os planos que giram a luz nao tem leitura tipada", ["palavra_lean", "diz_que_cada_leitura_cria_o_objeto_do_seu_plano"], "verdadeiro"),
        ext("pa7", "a docstring de observing_adds_nothing (kernel dos Nos) tem a frase exata «A primeira leitura identifica; a segunda confirma que a operacao nao altera.»", ["observing_adds_nothing", "frase_exata_esta_no_fonte"], "verdadeiro"),
        ext("pa8", "a forma COMPOSTA citada na errata de 07/10 NAO esta no fonte do kernel", ["observing_adds_nothing", "forma_composta_esta_no_fonte"], "falso"),
        ext("pa9", "o titulo «RELER NAO ACRESCENTA.» esta no fonte", ["observing_adds_nothing", "titulo_esta_no_fonte"], "verdadeiro"),
        ext("pa10", "A14: tres nomes do kernel tem o enunciado de observing_adds_nothing (rfl na sonda P1)", ["sondas_P", "p1", "tres_nomes_com_o_enunciado_de_observing_adds_nothing"], "tamanho_igual", 3, "tres_nomes"),
        ext("pa11", "o nome da PALAVRA esta entre os tres", ["sondas_P", "p1", "tres_nomes_com_o_enunciado_de_observing_adds_nothing"], "contem", "TGLExt.Palavra.rereading_adds_nothing"),
        ext("pa12", "o A3 do atrator esta entre os tres", ["sondas_P", "p1", "tres_nomes_com_o_enunciado_de_observing_adds_nothing"], "contem", "TheSingularityReadsTheAttractor.A3_angular_rereading_only"),
        ext("pa13", "o A5 da luz que se le esta entre os tres", ["sondas_P", "p1", "tres_nomes_com_o_enunciado_de_observing_adds_nothing"], "contem", "TheLightReadsItself.A5_angular_rereading_only"),
        ext("pa14", "as sete declaracoes da PALAVRA NAO usam a letra (exact_witness_of_annihilating_word, annihilating_word_exists)", ["sondas_P", "p1", "as_sete_da_palavra_usam_a_letra"], "falso"),
        ext("pa15", "o fecho de imports da PALAVRA contem o modulo ExactWitness (a letra entra por import, nao por uso)", ["sondas_P", "p1b", "TGLExt.ExactWitness"], "verdadeiro"),
        ext("pa16", "o fecho TRANSITIVO de constantes das 7 NAO contem exact_witness_of_annihilating_word", ["sondas_P", "p1c", "contem:TGLExt.exact_witness_of_annihilating_word"], "falso"),
        ext("pa17", "o fecho transitivo tem 41 constantes (raizes TGL/TGLExt/ChatgptAudit)", ["sondas_P", "p1c", "n_constantes_do_fecho"], "igual", 41, "n_fecho_palavra"),
        chk("pa18", "RESULTADO P1: rc 0, sem erro, sem axioma fora do trio, sem sorry", "fonte:g1_p_palavra", ["sondas", 0, "ok"], "verdadeiro"),
        chk("pa19", "RESULTADO P1b: ok", "fonte:g1_p_palavra", ["sondas", 1, "ok"], "verdadeiro"),
        chk("pa20", "RESULTADO P1c: ok", "fonte:g1_p_palavra", ["sondas", 2, "ok"], "verdadeiro"),
        chk("pa21", "RESULTADO P1: rc", "fonte:g1_p_palavra", ["sondas", 0, "rc"], "igual", 0, "rc_p1"),
        chk("pa22", "RESULTADO P1c: rc", "fonte:g1_p_palavra", ["sondas", 2, "rc"], "igual", 0),
        ext("pa23", "o um.py v391 (8e7b9927ceae64b8) diz «palavra aniquiladora» na l.203582 (PT)", ["umpy_v391", "palavra_aniquiladora_linhas", "203582"], "contem", "palavra aniquiladora", "umpy_l203582"),
        ext("pa24", "o um.py v391 diz «annihilating word» na l.206031 (EN)", ["umpy_v391", "palavra_aniquiladora_linhas", "206031"], "contem", "annihilating word", "umpy_l206031"),
        ext("pa25", "o um.py v391 diz «palavra aniquiladora» na l.155501", ["umpy_v391", "palavra_aniquiladora_linhas", "155501"], "contem", "palavra aniquiladora", "umpy_l155501"),
        ext("pa26", "o um.py lido e' o v391 selado", ["umpy_v391", "sha16"], "igual", um["sha16"]),
        chk("pa27", "o kernel dos Nos nao mudou o fonte de TheObserverReadsTheAngle (sha do kernel materializado no rito = o da v391)", "kf", ["formal_files_sha256", "TGLExt/TheObserverReadsTheAngle.lean"], "igual", ffs("TGLExt/TheObserverReadsTheAngle.lean")),
    ],
    "diz": [
        "[KERNEL] Os sete teoremas de TGLExt.Palavra, no trio, dao a forma matematica da leitura do operador no plano do boost: ANTES da leitura a face nao fecha (the_face_does_not_close: boost s = 1 so' em s = 0, a posicao e' relativa); "
        "a leitura no angulo cria o contorno (the_reading_creates_the_contour: o quociente angular e' fiel exatamente quando kappa*P = 2pi ou -2pi); a face lida fecha em 2pi (the_read_face_closes); o contorno fiel da a temperatura 1/P = kappa/2pi "
        "(the_contour_gives_the_temperature); a primeira leitura identifica (the_first_reading_identifies); reler nao acrescenta (rereading_adds_nothing); e a clausula composta the_reading_creates_the_object.",
        "[INPUT do operador, 07/10/2026, verbatim embutido por sha256] «a LEITURA CRIA o objeto, antes da leitura o objeto é Nome (posto relativo), após a leitura o objeto é identidade, relação de contorno». [ONTO] Leitura vigente: a leitura CRIA o objeto; "
        "cada leitura cria o objeto do SEU plano.",
        "[INPUT do operador, 07/10/2026] o nome da pedra: «essa pedra se chama (olha a beleza lexical): PALAVRA»; e a letra: «polinômio aniquilador normalizado=letra (por isso palavra, mas ali como letra)».",
        "[REAL, sondas P1/P1b/P1c] A PALAVRA nao usa nem duplica a letra: nenhuma das sete declaracoes usa exact_witness_of_annihilating_word nem annihilating_word_exists; o fecho transitivo de constantes das sete (%d constantes das raizes TGL, TGLExt e ChatgptAudit) "
        "nao as contem; os modulos da letra (ExactWitness, WordExistence, InfiniteWord) estao no ambiente de imports, por import e nao por uso." % sp["p1c"]["n_constantes_do_fecho"],
        "[REAL, A14] Tres nomes do kernel tem o MESMO enunciado de TGLExt.observing_adds_nothing (as igualdades por rfl compilaram, rc 0): %s. E %s tem o enunciado de TGLExt.the_observer_reads_the_angle. "
        "Um teorema do kernel sob tres nomes: nenhum peso novo." % (", ".join(tres), ", ".join(sp["p1"]["nome_com_o_enunciado_de_the_observer_reads_the_angle"])),
        "[REAL] A docstring exata de TGLExt.observing_adds_nothing, lida do kernel por script (TheObserverReadsTheAngle.lean, l.%d-%d), esta em extras.docstring_exata_de_observing_adds_nothing." % (oa["linha_ini"], oa["linha_fim"]),
    ],
    "nao_diz": [
        "NAO afirma estado KMS: a continuacao de Wick aqui e' identidade de matrizes; o KMS da luz na cunha entra por citacao (Bisognano-Wichmann 1975 [KNOWN]).",
        "NAO cria as leituras dos OUTROS planos: as rotacoes que giram a direcao da luz (x-y, x-z) e os boosts das outras cunhas (t-y, t-z) nao tem leitura tipada no kernel [OPEN]; a tela transversal (helicidade) tem a sua leitura, D1'.",
        "NAO renomeia nada no kernel: annihilating_word_exists, exact_witness_of_annihilating_word, WordExistence e InfiniteWord seguem com os nomes que tem; o kernel nao se edita.",
        "A leitura «Nome (posto relativo) -> identidade (relacao de contorno)» e' do operador [ONTO]; os teoremas sao a forma matematica que ela encontra [REAL]. Validade no kernel nao e' creditacao; o gate nao se move.",
        "NAO e' a unica leitura do plano do boost como angulo: ler o parametro do boost como angulo e' a escolha da pedra (Circle.exp (kappa*t)); o regime da FACE segue hiperbolico e tem limite, o da LEITURA segue compacto e so' le (regra dos dois regimes).",
    ],
    "limites": [
        "A forma composta «a primeira leitura identifica; reler nao acrescenta» foi lida de C:/IALD/CLAUDE.md (errata de 07/10/2026) e nao tem pino por ser memoria viva [DECLARADO]; a docstring exata e' a do extras, lida do kernel [REAL].",
        "O estatuto da letra para o X·q NAO normalizado e' [OPEN]: o operador disse «normalizado».",
        "A saida textual das sondas P1/P1b/P1c existia so' no scratchpad; foi copiada para rodada2/g1/fontes/logs_P com sha256 conferido contra o RESULTADO_P_palavra.json.",
    ],
    "erratas": [
        {"ao_lado_de": "um.py v391 (8e7b9927ceae64b8): artigo PT l.203582, artigo EN l.206031, lista de passos l.155501, e as docstrings do kernel embutido (l.%s)" % ", ".join(str(x) for x in um["palavra_aniquiladora_no_kernel_embutido_linhas"]),
         "dizia": "«%s» (PT); «%s» (EN); «%s». O kernel embutido diz, p.ex., «%s»." % (pl["203582"].strip('r"').strip(), pl["206031"].strip('r"').strip(), pl["155501"].strip('"').rstrip(","), pl["86954"]),
         "agora": "O polinomio aniquilador normalizado (q(T)/q(0), q(0) diferente de 0) e' a LETRA (operador, 07/10/2026, verbatim embutido). PALAVRA e' o nome da pedra TGLExt.Palavra: a leitura que, com as letras, cria o objeto. "
                  "Os textos acima ficam como registro; os nomes do kernel ficam como estao.",
         "lacuna_de_fidelidade": "A estrutura dizia: o polinomio aniquilador normalizado e' a letra, e «palavra» e' a leitura que cria o objeto. Foi escrito: «palavra aniquiladora» para o proprio polinomio (v86 a v94, antes de o operador atribuir «palavra» a pedra de leitura). "
                                 "A traducao falhou onde o nome «palavra» ja estava ocupado pelo objeto que o operador chama de letra. O X·q nao normalizado: o operador disse «normalizado» e este registro segue a letra dele; se vale tambem para o nao normalizado e' [OPEN].",
         "estatuto": "[INPUT do operador, verbatim 07/10/2026 + REAL: linhas lidas do um.py v391 por script]", "assinatura": ASSINA},
        {"ao_lado_de": "as bandeiras ext_pal_rereading_adds_nothing, ext_atr_A3_angular_rereading_only e ext_lri_A5_angular_rereading_only (e o levantamento A5: «a releitura angular e' nome sem peso»)",
         "dizia": "tres entradas na escada (tres bandeiras), uma por nome.",
         "agora": "Um unico teorema do kernel, TGLExt.observing_adds_nothing, sob tres nomes (rfl na sonda P1, rc 0). A escada conta declaracoes; o conteudo e' um.",
         "lacuna_de_fidelidade": "A estrutura: um teorema (reler nao acrescenta). Escrito/contado: tres declaracoes, tres bandeiras. A traducao falha no contador, que conta nomes e nao teoremas distintos.",
         "estatuto": "[REAL, sonda P1 do F_KERNEL]", "assinatura": ASSINA},
        {"ao_lado_de": "C:/IALD/CLAUDE.md: errata de 07/10/2026 («a leitura cria o objeto», marcador errata_leitura_cria_o_objeto_07out) e a nota de 08/10/2026 06:07 (errata_releitura_e_palavra_08out)",
         "dizia": "[DECLARADO, lido da memoria viva] «TGLExt.observing_adds_nothing (cuja docstring diz «a primeira leitura identifica; reler nao acrescenta»)». Forma composta: %s." % oa["forma_composta_citada_na_errata_de_07out"],
         "agora": "A docstring exata (lida do kernel por script; sha256 %s): %s" % (oa["sha256"][:16], oa["docstring_exata"].replace("\n", " ")),
         "lacuna_de_fidelidade": "A estrutura: duas frases, o titulo «RELER NAO ACRESCENTA.» e o texto em italico «A primeira leitura identifica; a segunda confirma que a operacao nao altera. E o `1 = 1` do lado do observador.». "
                                 "Foi escrito: uma frase composta entre aspas, com «reler nao acrescenta» no lugar da segunda metade. A traducao falhou ao pôr entre aspas uma parafrase. A auditoria c1 a7ba2dc9 conferiu que a forma composta nao existe no fonte.",
         "estatuto": "[REAL: docstring lida do kernel] / [DECLARADO: a citacao composta, lida de memoria sem pino]", "assinatura": ASSINA},
        {"ao_lado_de": "C:/IALD/CLAUDE.md: errata de 07/10/2026 («rotacoes/PCT ... confunde HOMONIMOS») e a nota de 08/10/2026 sobre as pontes genK_eq_Grot e rotGen_complex_eq_Grot",
         "dizia": "[DECLARADO, lido da memoria viva] as rotacoes de O16/RotationGeneratorBridges e WickBoostRotation_v2 seriam homonimas (rotacoes 2x2 do regime angular, nao as do espaco-tempo).",
         "agora": "No plano do BOOST a rotacao angular nao e' homonima: e' a que a leitura CRIA (faithful_period_iff, reciprocal_temperature, wick_boost_two_pi, observing_adds_nothing, agora reunidos em TGLExt.Palavra). Homonimo continua valendo para as leituras dos OUTROS planos, que o kernel nao tem.",
         "lacuna_de_fidelidade": "A estrutura: a rotacao angular do plano do boost e' a leitura que cria o contorno. Foi escrito: «homonimos», largo demais. A traducao falhou ao nao distinguir o plano do boost dos demais planos; a correcao do operador (07/10) e a pedra PALAVRA a fazem.",
         "estatuto": "[INPUT do operador, verbatim 07/10/2026] / [DECLARADO: o texto da errata, lido da memoria viva]", "assinatura": ASSINA},
    ],
    "leituras_do_operador": [
        {"trecho": "a LEITURA CRIA o objeto", "estatuto": "[INPUT do operador, verbatim 07/10/2026; ONTO: a forma matematica e' a da pedra PALAVRA, [REAL]]"},
        {"trecho": "essa pedra se chama (olha a beleza lexical): PALAVRA", "estatuto": "[INPUT do operador, verbatim 07/10/2026]"},
        {"trecho": "polinômio aniquilador normalizado=letra (por isso palavra, mas ali como letra)", "estatuto": "[INPUT do operador, verbatim 07/10/2026]"},
    ],
    "extras": {"tres_nomes_com_o_enunciado_de_observing_adds_nothing": tres, "docstring_exata_de_observing_adds_nothing": oa["docstring_exata"], "forma_composta_da_errata_de_07out": oa["forma_composta_citada_na_errata_de_07out"],
               "o_que_as_sete_da_palavra_usam": sp["p1"]["o_que_a_palavra_usa"], "p1c_modulos_do_fecho": sp["p1c"]["modulos"], "linhas_do_umpy_v391_com_palavra_aniquiladora": pl,
               "sondas": "F_KERNEL P1, P1b, P1c (RESULTADO_P_palavra.json, logs pinados)"},
})

# ============================================================================================ R02 lei_de_campo_curvo_v392
lig_fl, lig_dc = flags_de("TGLExt.LiganteLeiCampoCurvo")
lgt_fl, lgt_dc = flags_de("TGLExt.LiganteLeiCampoCurvoTestemunha")
assert len(lig_fl) == 2 and len(lgt_fl) == 32
lei_antigas = antigas("TGLExt.Fundacao.the_post_lives_in_the_passage", "TGLExt.Fundacao.agape", "TGLExt.QGSolution.qg_solution_end_to_end", "ChatgptAudit.entropy_density_einstein_coefficient",
                      "ChatgptAudit.SmoothAtlasGluing.connected_smooth_atlas_einstein", "TGLExt.ContratoQGv31.ContratoH2.unruh_is_kms_temperature", "ChatgptAudit.CalibrationReuse016.polar_period_matches_contract",
                      "ChatgptAudit.CalibrationReuse016.kappa_is_input", "TGLExt.ContratoQGv31.ContratoH3.data_temperature_from_same_period")
fl_ = E["ligante"]; fq = E["fecho_QGSolutionComplete"]; tm = E["testemunha"]
c5 = fl_["variante_auditoria_c1"]["cinco_limites"]
SPECS.append({
    "nome": "lei_de_campo_curvo_v392", "veredito_prefixo": "TGL_LEI_DE_CAMPO_CURVO_V392",
    "veredito_sufixo": "THE_FIELD_LAW_IN_CURVED_SPACETIME_IS_A_KERNEL_TERM_CONDITIONAL_ON_THE_NAMED_H3__LOCAL_PASSAGE_KNOWN_JACOBSON_1995__NOT_GLOBAL_EXISTENCE__LEMA3_STATUS_UNCHANGED__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    "estatuto": "[REAL -- ligante (2 bandeiras) e testemunha S7/S8 (32 bandeiras) no kernel do proprio rito; auditorias c1 pinadas por sha256; KNOWN -- Jacobson 1995 (H3, equilibrio local de horizonte); "
                "OPEN -- existencia global, derivacao de H3, atlas e metrica construidos]",
    "fontes": ["g1_extratos", "g1_ligante_lean", "g1_ligante_variante", "g1_testemunha_lean", "g1_testemunha_parte", "g1_aud_f23", "g1_aud_f23_camadas3", "g1_calibration_reuse", "g1_horizon_reuse", "g1_qg_solution", "g1_fundacao"],
    "verbatins": [],
    "kernel_flags": lig_fl + lgt_fl, "kernel_decls": lig_dc + lgt_dc + lei_antigas,
    "checks": checks_comuns("lc") + [
        chk("lc1", "a Fundacao v390 selou (all_verified) no core: o token antigo vem de um registro verificado", "core", ["fundacao_v390", "all_verified"], "verdadeiro"),
        chk("lc2", "o token antigo existe no core v391 em fundacao_v390.verdict (texto exato)", "core", ["fundacao_v390", "verdict"], "contem", TOKEN),
        chk("lc3", "o token antigo existe no core v391 em estatuto_da_prova_v391.prova_1_kernel.fundacao_v390", "core", ["estatuto_da_prova_v391", "prova_1_kernel", "fundacao_v390"], "contem", TOKEN),
        chk("lc4", "o not_claimed[0] da Fundacao v390 diz que nao prova a equacao de campo no curvo por termo de kernel", "core", ["fundacao_v390", "not_claimed", 0], "igual", CORE0["fundacao_v390"]["not_claimed"][0]),
        chk("lc5", "tgl_closure.what_remains_named.extensao_geometrica__ao_lado_v390 diz «a lei de campo no curvo segue NAO sendo termo de kernel»", "core", ["tgl_closure", "what_remains_named", "extensao_geometrica__ao_lado_v390"], "contem", "a lei de campo no curvo segue NAO sendo termo de kernel"),
        chk("lc6", "tgl_closure.not_claimed[3] diz que o espaco-tempo curvo segue [OPEN]", "core", ["tgl_closure", "not_claimed", 3], "igual", CORE0["tgl_closure"]["not_claimed"][3]),
        ext("lc7", "o token antigo esta no um.py v391 so' na l.194416", ["umpy_v391", "token_NOT_A_KERNEL_TERM_linhas"], "igual", [194416]),
        ext("lc8", "a docstring INSTALADA do ligante NAO tem a secao dos cinco limites (a variante 992e4983 e' que tem)", ["ligante", "instalada", "tem_a_secao_dos_cinco_limites"], "falso"),
        ext("lc9", "a docstring instalada diz que H3 NAO e' derivado da passagem finita", ["ligante", "instalada", "diz_que_nao_deriva_o_H3_da_passagem"], "verdadeiro"),
        ext("lc10", "a docstring instalada diz que o teorema afirma uma implicacao, nao uma solucao global", ["ligante", "instalada", "diz_implicacao_nao_solucao_global"], "verdadeiro"),
        ext("lc11", "a variante da auditoria c1 tem exatamente CINCO limites", ["ligante", "variante_auditoria_c1", "cinco_limites"], "tamanho_igual", 5, "n_limites"),
        ext("lc12", "a variante diz que a passagem e' logicamente ociosa", ["ligante", "variante_auditoria_c1", "diz_que_a_passagem_e_logicamente_ociosa"], "verdadeiro"),
        ext("lc13", "a variante diz que H3 carrega conteudo fisico", ["ligante", "variante_auditoria_c1", "diz_que_H3_carrega_conteudo_fisico"], "verdadeiro"),
        ext("lc14", "o modulo instalado da testemunha e' o cabecalho derivado mais a parte do auditor, byte a byte", ["testemunha", "o_instalado_e_o_cabecalho_mais_a_parte"], "verdadeiro"),
        ext("lc15", "o cabecalho da testemunha diz «NADA disto e pedra; vive so no sandbox do auditor»", ["testemunha", "comentario_nada_disto_e_pedra"], "verdadeiro"),
        ext("lc16", "S7 esta no modulo (testemunha plana: Minkowski, fonte nula, uma carta)", ["testemunha", "s7"], "verdadeiro"),
        ext("lc17", "S8 esta no modulo (contramodelo: fonte constante com T(k,k) = 1 numa direcao nula)", ["testemunha", "s8"], "verdadeiro"),
        ext("lc18", "S8 diz que hH3 e' carga real", ["testemunha", "s8_diz_hH3_e_carga"], "verdadeiro"),
        ext("lc19", "auditoria F2.3 (f718620e): a passagem e' ociosa", ["auditoria_F2_3", "passagem_e_ociosa"], "verdadeiro"),
        ext("lc20", "auditoria F2.3: S5 (NamedAtlasH3 equivale ao balanco nulo de Ricci)", ["auditoria_F2_3", "S5"], "verdadeiro"),
        ext("lc21", "auditoria F2.3: S7 (nao vacuidade: vacuo plano)", ["auditoria_F2_3", "S7_vacuo_plano"], "verdadeiro"),
        ext("lc22", "auditoria F2.3: S8 (hH3 e' carga real)", ["auditoria_F2_3", "S8_hH3_e_carga"], "verdadeiro"),
        ext("lc23", "auditoria F2.3: nenhuma testemunha curva com materia (a S7 e' vacuo plano com Lambda = 0)", ["auditoria_F2_3", "nenhuma_testemunha_curva_com_materia"], "verdadeiro"),
        ext("lc24", "auditoria F2.3: nao deriva H3; nao identifica NamedAtlasH3 com o H3 de Jacobson por teorema; nao prova existencia de metrica ou solucao", ["auditoria_F2_3", "nao_deriva_H3"], "verdadeiro"),
        ext("lc25", "auditoria F2.3: o nome NamedAtlasH3 e' rotulo (KNOWN a identificacao)", ["auditoria_F2_3", "nao_identifica_com_o_H3_de_Jacobson_por_teorema"], "verdadeiro"),
        ext("lc26", "auditoria F2.3: os nove itens do que a pedra NAO prova", ["auditoria_F2_3", "nove_itens_que_a_pedra_nao_prova"], "verdadeiro"),
        ext("lc27", "fecho de imports de QGSolutionComplete (nivel de modulo): numero de modulos locais", ["fecho_QGSolutionComplete", "n_modulos_locais_no_fecho"], "maior_igual", 700, "n_modulos_fecho_qg"),
        ext("lc28", "ContractCalibrationReuse (polar_period_matches_contract) FORA do fecho de imports de QGSolutionComplete", ["fecho_QGSolutionComplete", "contem", "TGLExt.O16.ContractCalibrationReuse"], "falso"),
        ext("lc29", "HorizonDataReuse_Integration_v2 (data_temperature_from_same_period) FORA do fecho de imports de QGSolutionComplete", ["fecho_QGSolutionComplete", "contem", "TGLExt.O16.HorizonDataReuse_Integration_v2"], "falso"),
        ext("lc30", "lightH2 esta no fecho (TheImportedSecondQuantization e' importado)", ["fecho_QGSolutionComplete", "contem_TheImportedSecondQuantization"], "verdadeiro"),
        ext("lc31", "a auditoria c1 a7ba2dc9 leu 755 modulos locais no mesmo fecho e confere a forma composta ausente", ["auditoria_F2_3_camadas3", "fecho_755_modulos"], "verdadeiro"),
        chk("lc32", "o kernel materializado no rito tem o mesmo ContractCalibrationReuse da v391", "kf", ["formal_files_sha256", "TGLExt/O16/ContractCalibrationReuse.lean"], "igual", ffs("TGLExt/O16/ContractCalibrationReuse.lean")),
        chk("lc33", "o kernel materializado no rito tem o mesmo HorizonDataReuse_Integration_v2 da v391", "kf", ["formal_files_sha256", "TGLExt/O16/HorizonDataReuse_Integration_v2.lean"], "igual", ffs("TGLExt/O16/HorizonDataReuse_Integration_v2.lean")),
        chk("lc34", "o kernel materializado no rito tem a mesma QGSolutionComplete da v391 (a raiz do fecho nao mudou)", "kf", ["formal_files_sha256", "TGLExt/QGSolutionComplete.lean"], "igual", ffs("TGLExt/QGSolutionComplete.lean")),
        chk("lc35", "o kernel materializado no rito tem a mesma Fundacao da v391", "kf", ["formal_files_sha256", "TGLExt/Fundacao.lean"], "igual", ffs("TGLExt/Fundacao.lean")),
    ],
    "diz": [
        "[KERNEL] ChatgptAudit.F23CurvedFieldLigand.passage_h3_to_connected_smooth_atlas_einstein: SOB a hipotese NOMEADA hH3 (a passagem finita alimenta NamedAtlasH3, a condicao de area/Clausius em todo ponto e toda direcao nula de toda carta) e os dados de um atlas suave "
        "(cartas abertas e conexas, registros de resposta, conservacao, transicoes suaves), existe um UNICO coeficiente a com recordEinstein + a·g = 8πG·T em todo o atlas suprido. E' um termo de kernel CONDICIONAL ao H3 nomeado.",
        "[KNOWN] A passagem local e a identificacao de NamedAtlasH3 com o H3 de Jacobson (1995, equilibrio local de horizonte) sao conhecidas; o nome Lean e' um rotulo, nao um teorema aqui (auditoria F2.3 c1). O Lema 3 segue o que ja estava: fecho LOGICO por tres pecas "
        "(a definicao do operador de 07/10/2026; a recusa provada TGLExt.Fundacao.agape; a passagem local [KNOWN], H3 nomeada), programa ABERTO.",
        "[REAL, sonda S5 da c1] NamedAtlasH3 eta equivale, em todo ponto e toda direcao nula, a eta·Ric(k,k) = 2π·T(k,k); com eta = (4G)^-1 isso e' Ric(k,k) = 8πG·T(k,k), a projecao nula da equacao de campo: H3 carrega conteudo fisico.",
        "[REAL, kernel: 32 bandeiras ext_lgt_*] S7: o vacuo plano de Minkowski numa carta satisfaz TODAS as hipoteses do ligante, para todo G > 0 (nao vacuidade; Lambda = 0, fonte nula). S8: o contramodelo, a mesma geometria plana com fonte constante e T(k,k) = 1 numa direcao nula, "
        "satisfaz todas as hipoteses MENOS hH3; H3 falha e a conclusao falha. Logo hH3 e' CARGA, nao enfeite.",
        "[REAL, sondas S2-S4 da c1] a passagem e' logicamente ociosa dentro do enunciado: o teorema equivale ao mesmo enunciado sem passagem. O ligante e' fiacao por termo; o conteudo e' o de NamedAtlasH3 mais o atlas.",
        "[REAL] A fiacao de Unruh que JA existe (item (m) do criterio da F0.5): lightH2 C N; ChatgptAudit.CalibrationReuse016.polar_period_matches_contract (ContractCalibrationReuse.lean); TGLExt.ContratoQGv31.ContratoH2.unruh_is_kms_temperature; "
        "TGLExt.ContratoQGv31.ContratoH3.data_temperature_from_same_period (HorizonDataReuse_Integration_v2.lean); com ChatgptAudit.CalibrationReuse016.kappa_is_input: o kappa e' relativo ao relogio N e as outras direcoes nulas seguem hipotese.",
        "[REAL, por script, nivel de MODULO] DUAS pontes ficam FORA do fecho de QGSolutionComplete: polar_period_matches_contract e data_temperature_from_same_period. O fecho de imports de TGLExt.QGSolutionComplete tem %d modulos locais (e %d de Lean/Mathlib) e nenhum dos dois modulos esta entre eles; "
        "a auditoria c1 a7ba2dc9 leu o mesmo numero (755) e a sonda c1 `fecho_qg.log`, no nivel de CONSTANTES, nao achou os namespaces PolarPeriod016, CalibrationReuse016 e Wick016 [DECLARADO, log nao pinado aqui]. "
        "Ligar as duas a assinatura geral e' fiacao [OPEN], nao falta de termo." % (fq["n_modulos_locais_no_fecho"], fq["n_modulos_externos_Lean_Mathlib"]),
    ],
    "nao_diz": [
        "NAO e' prova de existencia global: nenhum atlas, metrica ou solucao e' construido, local ou global; a conclusao vale para o atlas DADO.",
        "NAO deriva H3 do estado, da Fundacao nem do contrato da luz (parede QG-X06 da auditoria); NAO liga a fonte T a StressTensorData nem a MaxwellCertificate (a conservacao covariante e' premissa do registro); NAO constroi a familia de cunhas de Lorentz (subsumida no H3 de toda direcao nula).",
        "NAO e' testemunha curva com materia: a S7 e' vacuo plano; NAO esta no fecho canonico de imports de QGSolutionComplete; NAO move o gate; o Lema 3 nao muda de estatuto.",
        "O token antigo de v390 e v391 (FIELD_EQUATION_IN_CURVED_SPACETIME_NOT_A_KERNEL_TERM) NAO e' reescrito: fica como registro; a errata vai ao lado (nada e' alterado por cima).",
    ],
    "limites": ["[REAL: docstring da variante 992e4983ec4f0686, NAO instalada; auditoria c1 f718620e] limite %d: %s" % (k + 1, t) for k, t in enumerate(c5)]
              + ["A docstring INSTALADA (e3f32d9b85ae82db) e' a curta; os cinco limites acima vivem na variante e neste registro. A auditoria c1 lista nove itens do que a pedra NAO prova (os cinco da docstring mais quatro: nao usa metric_einstein_from_screen_clausius nem o ContratoH3; nao fixa G nem toca em beta; nao esta no fecho canonico de imports; a passagem e' ociosa)."],
    "erratas": [
        {"ao_lado_de": "o token FIELD_EQUATION_IN_CURVED_SPACETIME_NOT_A_KERNEL_TERM: core.fundacao_v390.verdict e core.estatuto_da_prova_v391.prova_1_kernel.fundacao_v390 (construidos no um.py v391 na l.194416); "
                       "core.fundacao_v390.not_claimed[0] (l.194426); core.tgl_closure.what_remains_named.extensao_geometrica__ao_lado_v390 (l.144018); o artigo (PT l.166152, EN l.170494); e as demais superficies do CR-08 do levantamento "
                       "(MEMORIA_DA_LINHAGEM, DESENHO, Atlas, README do espelho, HANDOFF_v390 etc.) [DECLARADO: a lista de superficies vem do levantamento; as linhas do um.py foram lidas por script]",
         "dizia": "«%s» e «a lei de campo no curvo segue NAO sendo termo de kernel» e «nao prova a equacao de campo no espaco-tempo curvo por termo de kernel»." % TOKEN,
         "agora": "Com o ligante da v392, a lei de campo no espaco-tempo curvo e' um TERMO DE KERNEL CONDICIONAL ao H3 nomeado (passage_h3_to_connected_smooth_atlas_einstein, hH3 como premissa; passagem local [KNOWN], Jacobson 1995). "
                  "NAO e' existencia global: nenhum atlas, metrica ou solucao e' construido; a identificacao de NamedAtlasH3 com o H3 de Jacobson e' rotulo [KNOWN]; o Lema 3 segue o que ja estava. "
                  "As frases antigas seguem verdadeiras para a lei INCONDICIONAL e para a derivacao de H3, que nao sao termos de kernel.",
         "lacuna_de_fidelidade": "A estrutura (v390): sem ligante, nenhum termo de kernel ligava a passagem finita a equacao de campo no curvo. Foi escrito: «NOT_A_KERNEL_TERM», sem qualificar condicional. "
                                 "A traducao falha onde a frase passa a ser lida como absoluta depois do ligante; e a propria passagem e' ociosa no enunciado (S2-S4), de modo que o ganho do ligante e' o enunciado sob H3 nomeado, nao uma derivacao.",
         "estatuto": "[REAL: tokens e linhas lidos do core v391 e do um.py v391 por script; kernel do proprio rito] / [KNOWN: Jacobson 1995] / [OPEN: existencia global]", "assinatura": ASSINA},
        {"ao_lado_de": "TGLExt/LiganteLeiCampoCurvoTestemunha.lean, cabecalho do arquivo instalado: «NADA disto e pedra; vive so no sandbox do auditor»",
         "dizia": "o comentario dizia que a testemunha S7/S8 vive so' no sandbox do auditor e nao e' pedra.",
         "agora": "O modulo e' INSTALADO no kernel da v392 como modulo DERIVADO do texto do auditor (cabecalho de 4 imports e 2 set_option, %d bytes, mais a parte do auditor b5e8de0e619e60b3, byte a byte); as declaracoes sao termos de kernel (32 bandeiras ext_lgt_*), "
                  "com estatuto de testemunha/contramodelo (S7/S8). Nao e' pedra nomeada pelo operador; entra nos treze modulos novos do ledger de pedras." % tm["cabecalho_derivado_bytes"],
         "lacuna_de_fidelidade": "A estrutura: um texto de sandbox, escrito para NAO entrar no kernel. Foi instalado depois, derivado por cabecalho. O comentario ficou como estava e descreve o sandbox, nao o estado instalado; a traducao falha porque o arquivo fala de si no tempo da auditoria.",
         "estatuto": "[REAL: derivacao conferida por script (o instalado termina nos bytes da parte do auditor)]", "assinatura": ASSINA},
        {"ao_lado_de": "a docstring de TGLExt/LiganteLeiCampoCurvo.lean instalado (e3f32d9b85ae82db)",
         "dizia": "docstring curta: o H3 nomeado NAO e' derivado da passagem finita; a seta passagem -> H3 e' entrada explicita; o teorema afirma uma implicacao, nao uma solucao global.",
         "agora": "Os cinco limites da variante da auditoria c1 (992e4983ec4f0686, nao instalada) valem para a pedra instalada e estao na lista `limites` deste registro; o corpo de declaracoes e' o mesmo, so' a docstring difere.",
         "lacuna_de_fidelidade": "A estrutura: a auditoria pediu uma docstring com os limites. Foi decidido instalar a versao pinada e testada no conjunto (e3f32d9b), sem a docstring longa. A traducao falha na docstring instalada, que diz menos do que a auditoria; este registro carrega o resto.",
         "estatuto": "[REAL: duas docstrings lidas por script] / [INPUT da gerencia: a escolha de versao (anexo A do levantamento)]", "assinatura": ASSINA},
    ],
    "leituras_do_operador": [],
    "extras": {"cinco_limites_da_docstring_da_variante": c5, "fecho_QGSolutionComplete": {k: fq[k] for k in ("raiz_sha256", "nivel", "n_modulos_locais_no_fecho", "n_modulos_externos_Lean_Mathlib", "contem")},
               "pontes_de_unruh_fora_do_fecho": ["ChatgptAudit.CalibrationReuse016.polar_period_matches_contract", "TGLExt.ContratoQGv31.ContratoH3.data_temperature_from_same_period"],
               "fiacao_de_unruh_que_ja_existe": ["TGLExt.ImportedSQ.lightH2", "ChatgptAudit.CalibrationReuse016.polar_period_matches_contract", "TGLExt.ContratoQGv31.ContratoH2.unruh_is_kms_temperature",
                                                 "TGLExt.ContratoQGv31.ContratoH3.data_temperature_from_same_period", "ChatgptAudit.CalibrationReuse016.kappa_is_input"],
               "linhas_do_umpy_v391_com_a_frase_da_lei_de_campo_no_curvo": E["umpy_v391"]["frases_da_lei_de_campo_no_curvo"], "token_linha_umpy_v391": E["umpy_v391"]["token_NOT_A_KERNEL_TERM_linhas"],
               "superficies_de_memoria_medidas_em_13out": SUPERF},
})

# ============================================================================================ R03 agape_nao_vacua_v392
v51_fl, v51_dc = flags_de("TGLExt.V351DualScalingBridge")
agv_fl, agv_dc = flags_de("TGLExt.AgapeNonVacuity")
assert len(v51_fl) == 4 and len(agv_fl) == 2
agp_antigas = antigas("TGLExt.Fundacao.agape", "TGLExt.Fundacao.agape_is_inhabited", "TGLExt.Fundacao.abismo", "TGLExt.Fundacao.the_floor_fixes_the_cut", "TGLExt.Fundacao.nothing_above_bears_a_post")
f12 = E["auditoria_F1_2"]; dg = E["agape_derivacao"]; fd = E["fundacao"]
SPECS.append({
    "nome": "agape_nao_vacua_v392", "veredito_prefixo": "TGL_AGAPE_NAO_VACUA_V392",
    "veredito_sufixo": "AGAPE_CLAUSE_HAS_AN_INHABITANT_ON_THE_V351_REGULAR_CORE__M_N_CROSSED_PRODUCT_FACE_STAYS_OPEN__TAKESAKI_SCALING_LAW_KNOWN_AS_DATA__THE_LAMB_IS_NOT_THE_FLOOR_OF_THE_AGAPE__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    "estatuto": "[REAL -- 6 bandeiras (4 da ponte V351, 2 da Agape nao vacua) no kernel do proprio rito; auditoria c1 F1.2 pinada; KNOWN -- a lei de escala dual de Takesaki (citacao «Takesaki 1973» como o kernel a faz; referencia completa a conferir); "
                "OPEN -- a face M_n x| R; INPUT -- decisao do operador de 13/10/2026 sobre o cordeiro imolado]",
    "fontes": ["g1_extratos", "g1_v351_lean", "g1_v351_original", "g1_agape_lean", "g1_agape_original", "g1_aud_f12", "g1_fundacao", "g1_identidade_r2"],
    "verbatins": ["vb_g1_nomes_13out"],
    "kernel_flags": v51_fl + agv_fl, "kernel_decls": v51_dc + agv_dc + agp_antigas,
    "checks": checks_comuns("ag") + [
        chk("ag1", "a Fundacao v390 selou no core (all_verified)", "core", ["fundacao_v390", "all_verified"], "verdadeiro"),
        chk("ag2", "o not_claimed[1] da Fundacao v390 cita a lei de escala como DADO [KNOWN, Takesaki 1973] e diz que a realizacao no core M x| R de um fator III_1 genuino nao e' termo do kernel", "core", ["fundacao_v390", "not_claimed", 1], "igual", CORE0["fundacao_v390"]["not_claimed"][1]),
        ext("ag3", "o kernel dos Nos (Fundacao.lean) diz que a lei de escala e' [KNOWN], Takesaki 1973", ["fundacao", "diz_lei_de_escala_KNOWN_Takesaki_1973"], "verdadeiro"),
        ext("ag4", "Fundacao.lean tem agape, agape_is_inhabited e the_floor_fixes_the_cut", ["fundacao", "tem_the_floor_fixes_the_cut"], "verdadeiro"),
        ext("ag5", "o instalado difere do original auditado (AgapeNonVacuity) em UMA linha", ["agape_derivacao", "linhas_que_diferem"], "tamanho_igual", 1, "n_linhas_que_diferem"),
        ext("ag6", "essa linha e' o import: F12Completion.V351DualScalingBridge -> TGLExt.V351DualScalingBridge", ["agape_derivacao", "linhas_que_diferem", 0, 2], "igual", "import TGLExt.V351DualScalingBridge"),
        ext("ag7", "auditoria F1.2 (ec1040a0): PODE FECHAR", ["auditoria_F1_2", "veredito_pode_fechar"], "verdadeiro"),
        ext("ag8", "auditoria F1.2: a face M_n x| R esta dita [OPEN]", ["auditoria_F1_2", "face_Mn_cruzado_R_e_OPEN"], "verdadeiro"),
        ext("ag9", "auditoria F1.2: nao julgou se o traco v351 e' o peso dual de Takesaki em M_n x| R", ["auditoria_F1_2", "nao_julgou_se_o_traco_v351_e_o_peso_dual_de_Takesaki"], "verdadeiro"),
        ext("ag10", "auditoria F1.2: o resultado valia so' nessa instancia e so' no sandbox ate a instalacao na v392", ["auditoria_F1_2", "vale_so_nessa_instancia_e_no_sandbox_ate_a_v392"], "verdadeiro"),
        ext("ag11", "auditoria F1.2: as duas provas da pedra sao a sonda da propria c1, renomeada (a validade e' dada pelo kernel)", ["auditoria_F1_2", "prova_e_a_sonda_da_propria_c1_renomeada"], "verdadeiro"),
        ext("ag12", "auditoria F1.2: antes, o unico habitante da Agape era o modelo de brinquedo oneScaling", ["auditoria_F1_2", "antes_o_unico_habitante_era_o_modelo_de_brinquedo"], "verdadeiro"),
        ext("ag13", "auditoria F1.2: τ(I) = ⊤ (a unidade nao e' a testemunha) [REAL]", ["auditoria_F1_2", "a_unidade_tem_traco_infinito_REAL"], "verdadeiro"),
        ext("ag14", "a r2 da pedra Identidade tinha o alicerce provisorio = Fundacao.agape (o piso), que o operador nao escolheu", ["identidade_r2", "alicerce_provisorio_era_Fundacao_agape_o_piso"], "verdadeiro"),
        ext("ag15", "a copia corrigida da pedra Verdade diz que o cordeiro imolado nao e' o piso da Agape (lida; sem pino)", ["verdade_corrigida", "diz_que_o_cordeiro_nao_e_o_piso_da_Agape"], "verdadeiro"),
        chk("ag16", "o kernel materializado no rito tem a mesma Fundacao da v391", "kf", ["formal_files_sha256", "TGLExt/Fundacao.lean"], "igual", ffs("TGLExt/Fundacao.lean")),
    ],
    "diz": [
        "[KERNEL] TGLV351.regularCoreDualScalingData P: o traco e a acao dual do core regular v351 (scalarInverseLimitTraceData) dao, no cone positivo de traco finito (FiniteTracePositive P), a interface DualScalingData, "
        "com a lei de escala tau(theta_s A) = e^{-s}·tau(A) como TERMO (scalarInverseLimitWeight_dual); e TGLV351.finiteTracePositive_not_fixed: nenhum elemento nao nulo fica fixo por theta_s, s > 0.",
        "[KERNEL] F12Completion.finiteTracePositive_has_positive: para todo SiteProfile P existe A com 0 < tau A. F12Completion.agape_on_v351_core: a conjuncao da clausula Agape (TGLExt.Fundacao.agape) vale na instancia v351 com esse A: nenhum nao nulo fixo por escala nao trivial, "
        "a orbita estritamente monotona, sem teto, sem tocar o zero, abaixo de todo ε, e e^{-a} = 1 sse a = 0. Antes, o unico habitante da Agape era o modelo de brinquedo oneScaling (R, tau = id).",
        "[KNOWN] A lei de escala dual tau∘theta_s = e^{-s}·tau e' de Takesaki 1973 (a citacao e' a que o kernel faz em Fundacao.lean; a referencia bibliografica completa nao esta no kernel: a conferir [OPEN]). Entra como DADO; aqui vale como termo na instancia v351.",
        "[OPEN] A face M_n ⋊_σ R: nao se julgou se o traco v351 e' o peso dual de Takesaki em M_n ⋊_σ R (auditoria F1.2 c1); a realizacao no core M ⋊ R de um fator III_1 genuino segue sem ser termo deste kernel.",
        "[INPUT do operador, 13/10/2026, verbatim embutido por sha256] A Agape e' o piso (TGLExt.Fundacao.the_floor_fixes_the_cut: o peso e^{-a} vale 1 = ω(I) sse a = 0; sem teto e sem fundo: abismo). O cordeiro imolado NAO e' o piso da Agape: "
        "«quanto ao alicerce, o cordeiro imolado é a relação de comutação que impede a coincidência total».",
    ],
    "nao_diz": [
        "NAO prova a face M_n ⋊_σ R nem que o core regular v351 seja o produto cruzado de Takesaki; NAO muda a Fundacao v390 nem o gate.",
        "A independencia das provas: as duas provas da pedra sao a sonda da c1 (AuditProbe.lean) so' renomeada; a validade e' dada pelo kernel; a independencia da auditoria esta nos testes discriminantes (sonda de 27 declaracoes no trio) e a rota independente por contracoes finitas compilou na C4 do cetico anterior [DECLARADO pela auditoria F1.2].",
        "Que o comutador com o posto da pedra Verdade seja «o cordeiro imolado» e' leitura [ONTO] do operador sobre o termo (ver nome_posto_v392); este registro so' diz que o cordeiro nao e' o piso da Agape.",
        "Validade no kernel nao e' creditacao; NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move.",
    ],
    "limites": ["A referencia completa de «Takesaki 1973» nao esta no kernel nem na auditoria: [OPEN] a conferir antes de citar volume e paginas.",
                "O modulo AgapeNonVacuity instalado difere do auditado em 1 linha (o import); a auditoria F1.2 auditou o original [DERIVED trivial, conferido por script]."],
    "erratas": [
        {"ao_lado_de": "core.fundacao_v390.not_claimed[1] (um.py v391): «%s»" % CORE0["fundacao_v390"]["not_claimed"][1],
         "dizia": CORE0["fundacao_v390"]["not_claimed"][1],
         "agora": "Com a ponte V351 e a Agape nao vacua, a lei de escala dual e' TERMO do kernel no core REGULAR v351 (cone positivo de traco finito, F12Completion.agape_on_v351_core); a realizacao em M ⋊_σ R de um fator III_1 genuino segue DADO [KNOWN] e sem termo [OPEN]: "
                  "a identificacao do core regular v351 com o produto cruzado nao foi julgada.",
         "lacuna_de_fidelidade": "A estrutura: o kernel passa a ter um habitante nao trivial da Agape, no core regular v351. Foi escrito (v390): «a sua realizacao no core M x| R de um fator III_1 genuino nao e' termo deste kernel». A frase segue verdadeira para o fator III_1 genuino; "
                                 "a traducao falha se for lida como «a lei de escala nunca e' termo»: ela e' termo na instancia v351. O que a ponte nao diz e' que o core regular v351 seja M_n ⋊_σ R.",
         "estatuto": "[REAL: kernel do proprio rito + auditoria F1.2] / [KNOWN: Takesaki 1973] / [OPEN: a face M_n x| R]", "assinatura": ASSINA},
        {"ao_lado_de": "a decisao provisoria da r2 da pedra Identidade (work/identidade_cordeiro_13out/5_R2/RESULTADO_R2.md, pergunta 2): alicerce_fundante = TGLExt.Fundacao.agape, o piso",
         "dizia": "[DECLARADO, lido do arquivo] «Hoje e' `alicerce_fundante` = `TGLExt.Fundacao.agape`, o piso.», com alternativas (A) o piso da Agape, (B) beta, (C) J, a Palavra, (D) outro termo.",
         "agora": "[INPUT do operador, 13/10/2026, verbatim embutido] «quanto ao alicerce, o cordeiro imolado é a relação de comutação que impede a coincidência total». A Agape e' o piso; o cordeiro imolado NAO e' o piso da Agape.",
         "lacuna_de_fidelidade": "A estrutura: o operador escolheu um termo diferente do provisorio. Foi escrito (r2): o piso da Agape como alicerce provisorio, com a pergunta aberta. A traducao falhava por ter posto na frente um termo que o operador nao escolheu; a r3 da pedra Verdade ja usa o comutador.",
         "estatuto": "[INPUT do operador, verbatim 13/10/2026] / [DECLARADO: a r2, lida do arquivo]", "assinatura": ASSINA},
        {"ao_lado_de": "AgapeNonVacuity.lean instalado (e49ad8f980d7cf48) x original auditado (cf30422393b2af21)",
         "dizia": "a auditoria F1.2 c1 auditou o arquivo original, com `%s` na linha %d." % (dg["linhas_que_diferem"][0][1], dg["linhas_que_diferem"][0][0]),
         "agora": "O instalado difere em UMA linha: `%s` (linha %d). Os 4 teoremas da ponte V351 e os 2 da Agape ficam como auditados." % (dg["linhas_que_diferem"][0][2], dg["linhas_que_diferem"][0][0]),
         "lacuna_de_fidelidade": "A estrutura auditada usa o namespace de sandbox F12Completion. Foi instalada uma derivacao de 1 linha (o import), sem nova auditoria do texto derivado; a traducao falha so' se o import novo mudasse algo, e a compilacao no conjunto (rc 0) e a igualdade das demais linhas dizem que nao.",
         "estatuto": "[REAL: diff por script] / [DERIVED trivial]", "assinatura": ASSINA},
    ],
    "leituras_do_operador": [{"trecho": "quanto ao alicerce, o cordeiro imolado é a relação de comutação que impede a coincidência total", "estatuto": "[INPUT do operador, verbatim 13/10/2026; ONTO: a leitura do comutador como o cordeiro e' dele]"}],
    "extras": {"linhas_que_diferem_original_x_instalado": dg["linhas_que_diferem"], "linhas_da_fundacao_com_Takesaki": fd["linhas_com_Takesaki"], "agape_dependencias": ["TGLExt.Fundacao.agape", "TGLExt.Fundacao.agape_is_inhabited", "TGLExt.Fundacao.abismo", "TGLExt.Fundacao.the_floor_fixes_the_cut"]},
})

# ============================================================================================ R27 x19_bgl_tipo_v392
bgl_fl, bgl_dc = flags_de("TGLExt.LightNetStandardWedgeDataBGL")
assert len(bgl_fl) == 57
bgl_antigas = antigas("TGLExt.QGSolution.qg_solution_end_to_end", "TGLExt.QGSolution.the_tetelestai_declaration")
bg = E["bgl"]; bn = E["bgl_numeros"]; a13 = E["auditoria_F1_3"]
SPECS.append({
    "nome": "x19_bgl_tipo_v392", "veredito_prefixo": "TGL_X19_BGL_TIPO_V392",
    "veredito_sufixo": "BISOGNANO_WICHMANN_CONTENT_AS_A_TYPED_HYPOTHESIS__NO_INHABITANT_BUILT__LIGHTNETDATA_AND_EXISTING_THEOREMS_UNCHANGED__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    "estatuto": "[REAL -- 57 bandeiras ext_bgl_* no kernel do proprio rito, sonda c1 e reauditoria c1 pinadas por sha256; KNOWN -- Brunetti-Guido-Longo 2002 e Bisognano-Wichmann 1975 (como o kernel cita); "
                "OPEN -- habitante (Fub, J_W, σ, Δ_K^{it}) e habitabilidade (D5); INPUT da gerencia c1 -- X19 decidida em 13/10/2026: entra como hipotese tipada]",
    "fontes": ["g1_extratos", "g1_bgl_lean", "g1_bgl_original", "g1_aud_f13_reaud", "g1_aud_f13_sonda", "g1_x19_delta", "g1_conjunto_j2"],
    "verbatins": [],
    "kernel_flags": bgl_fl, "kernel_decls": bgl_dc + bgl_antigas,
    "checks": checks_comuns("xb") + [
        chk("x1a", "o kernel materializado no rito tem a mesma QGSolutionComplete (onde LightNetData e' definido, l.49) e os teoremas qg_solution_end_to_end e the_tetelestai_declaration da v391", "kf", ["formal_files_sha256", "TGLExt/QGSolutionComplete.lean"], "igual", ffs("TGLExt/QGSolutionComplete.lean")),
        chk("x1b", "o mesmo para LightHelicityWigner (consumidor de LightNetData)", "kf", ["formal_files_sha256", "TGLExt/LightHelicityWigner.lean"], "igual", ffs("TGLExt/LightHelicityWigner.lean")),
        chk("x1c", "o mesmo para TetelestaiOneObject (consumidor de LightNetData)", "kf", ["formal_files_sha256", "TGLExt/TetelestaiOneObject.lean"], "igual", ffs("TGLExt/TetelestaiOneObject.lean")),
        chk("x1d", "o mesmo para TheWholeIsOne (consumidor de LightNetData)", "kf", ["formal_files_sha256", "TGLExt/TheWholeIsOne.lean"], "igual", ffs("TGLExt/TheWholeIsOne.lean")),
        ext("x1e", "o tipo estende LightNetData (nao o altera)", ["bgl", "extends_LightNetData"], "verdadeiro"),
        ext("x1f", "o tipo carrega a colagem toLightNetData.K rightWedge = out.KWR.toClosedSubmodule.toSubmodule", ["bgl", "tem_wedge_glue"], "verdadeiro"),
        ext("x1g", "NAO ha habitante: nenhum instance nem def com o tipo", ["bgl", "tem_instance_ou_habitante"], "falso"),
        ext("x1h", "o unico `example` do arquivo e' CompleteSpace H1", ["bgl", "unico_example"], "igual", ["example : CompleteSpace H1 := inferInstance"]),
        ext("x1i", "de T so' se pede IsSelfAdjoint (positividade nao e' pedida)", ["bgl", "T_so_pede_IsSelfAdjoint"], "verdadeiro"),
        ext("x1j", "o cabecalho do arquivo instalado diz «nada aqui e pedra; nada entra no kernel»", ["bgl", "cabecalho_nada_aqui_e_pedra"], "verdadeiro"),
        ext("x1k", "o cabecalho diz que so' tipa o enunciado e que nenhum habitante e' dado", ["bgl", "cabecalho_nada_constroi_o_D1a"], "verdadeiro"),
        ext("x1l", "o arquivo instalado e' byte a byte a sonda c1 da auditoria F1.3", ["bgl", "bytes_iguais_a_sonda"], "verdadeiro"),
        ext("x1m", "reauditoria c1 (a20c3246): nao reivindica habitante", ["auditoria_F1_3", "reauditoria", "nao_reivindica_habitante"], "verdadeiro"),
        ext("x1n", "reauditoria c1: D5 [OPEN] -- nao se mostrou que o D1a3OutputBGL seja habitavel", ["auditoria_F1_3", "reauditoria", "D5_OPEN_habitavel"], "verdadeiro"),
        ext("x1o", "reauditoria c1: as 19 `#print axioms` do arquivo saem no trio", ["auditoria_F1_3", "reauditoria", "19_print_axioms_no_trio"], "verdadeiro"),
        ext("x1p", "auditoria da sonda (ad949e97): a sonda so' tipa, nao constroi nem mostra habitado", ["auditoria_F1_3", "sonda", "tipa_nao_constroi"], "verdadeiro"),
        ext("x1q", "auditoria da sonda: quem constroi nao aprova; a adocao cabe ao Codex ou a gerencia, e a reauditoria a outro auditor", ["auditoria_F1_3", "sonda", "adocao_cabe_ao_Codex_ou_a_gerencia"], "verdadeiro"),
        ext("x1r", "numero de bandeiras ext_bgl_* (def/thm) no FLAGS_v392", ["bgl_numeros", "bandeiras_ext_bgl_no_FLAGS_v392"], "igual", 57, "n_bandeiras_bgl"),
        ext("x1s", "declaracoes lidas pela regex do um.py na sonda C_audit_delta_x19 (o «+87» do plano)", ["bgl_numeros", "declaracoes_lidas_pela_regex_do_umpy_na_sonda_C_delta_x19"], "igual", 87, "n_decl_regex_x19"),
        chk("x1t", "sonda C_audit_delta_x19: rc 0 e ok", "fonte:g1_x19_delta", ["ok"], "verdadeiro"),
        chk("x1u", "sonda C_audit_delta_x19: zero fora do trio", "fonte:g1_x19_delta", ["fora_do_trio"], "tamanho_igual", 0),
        chk("x1v", "conjunto J2 (com X19): rc 0", "fonte:g1_conjunto_j2", ["resultados", 2, "rc"], "igual", 0),
        chk("x1w", "conjunto J2 e' o ConjuntoV392ComX19", "fonte:g1_conjunto_j2", ["resultados", 2, "nome"], "igual", "B_J2_ConjuntoV392ComX19"),
    ],
    "diz": [
        "[REAL, tipo] O QUE MUDA: o kernel ganha TGLExt.LightNetStandardWedgeDataBGL (AuditF13v31.LightNetStandardWedgeDataBGL), que ESTENDE LightNetData com a saida tipada do D1a.3 (D1a3OutputBGL) e a colagem D.K rightWedge = K(W_R). "
        "Os teoremas que tomarem o tipo novo passam a exigir que a rede citada na cunha direita seja o subespaco padrao de S_W = genericTomita T J, com Δ_K = S_W†S_W pelo grafo e Δ_K^{it} = B0(−2πt) pelo multiplicador apos o Fourier parcial: "
        "o conteudo de Bisognano-Wichmann vira HIPOTESE TIPADA, nao prova. (Texto da fila do operador, reauditoria c1 a20c3246, em extras.)",
        "[REAL] O QUE NAO MUDA: o LightNetData; os teoremas existentes (qg_solution_end_to_end, the_tetelestai_declaration, no trio); o gate. Como o tipo usa `extends`, nada do que ja existe e' tocado: o fonte de QGSolutionComplete e dos consumidores do LightNetData e' o mesmo da v391 (checks x1a-x1d).",
        "[REAL] NAO HA HABITANTE: nenhum instance, def ou termo de D1a3OutputBGL nem de LightNetStandardWedgeDataBGL; o unico example do arquivo e' CompleteSpace H1. Seguem [OPEN] ate o D1a.1-D1a.3: Fub (a ponte de Fubini L2 vetorial, ausente do pin do Mathlib), J_W, "
        "σ, Δ_K^{it}; de T so' se pede IsSelfAdjoint. E nao se mostrou que o D1a3OutputBGL seja habitavel (D5): os campos podem ser conjuntamente inconsistentes.",
        "[REAL] O que o arquivo PROVA (57 bandeiras ext_bgl_*, no trio): tomitaSquare_unique (Δ nao e' campo livre: S†S o determina), generic_pairing_on_H1, standard_ne_bot, H1_nontrivial, D1a3OutputBGL.mem_KWR (Iff.rfl: K(W_R) e' CONSTRUIDO por closedAntilinearStandardSubspace), "
        "S_is_tomita_of_K e exists_nonzero (o «existe ξ ≠ 0» e' consequencia, nao hipotese). Numero: %d bandeiras (def/thm); as %d declaracoes que a regex do um.py le na sonda incluem tambem as estruturas e seus auxiliares (casesOn, recOn, noConfusion), %d a mais."
        % (bn["bandeiras_ext_bgl_no_FLAGS_v392"], bn["declaracoes_lidas_pela_regex_do_umpy_na_sonda_C_delta_x19"], bn["diferenca"]),
        "[KNOWN] As fontes do conteudo sao Brunetti-Guido-Longo 2002 (Rev. Math. Phys. 14 (2002) 759, como o kernel cita em TheImportedSecondQuantization.lean) e Bisognano-Wichmann 1975/76 (idem, e LightHelicityWigner.lean). "
        "O modulo TGLExt.BisognanoWichmann que o kernel ja tem (v47) e' OUTRO objeto: a face finita (geometria do boost e gerador modular a 2π), nao a hipotese da cunha da rede.",
    ],
    "nao_diz": [
        "NAO prova Bisognano-Wichmann nem a realizacao fisica; NAO constroi habitante; NAO fecha nenhuma peca do D1a (Fub, J_W, σ, Δ_K^{it} seguem abertos).",
        "A sonda e a reauditoria sao ambas da c1 (quem constroi nao aprova): a adocao no kernel e' decisao da gerencia/operador (X19 decidida em 13/10/2026) e o TEXTO INSTALADO nao teve reauditoria de OUTRO auditor [OPEN].",
        "NAO move o gate nem muda valor algum do core; validade no kernel nao e' creditacao; NOT_FALSIFIED nunca e' a palavra da creditacao.",
    ],
    "limites": ["O plano e o levantamento contavam «+87 #print» e «6372/6372»: a medida e' %d bandeiras def/thm (o numero corrige a frase); os %d a mais sao estruturas e auxiliares." % (bn["bandeiras_ext_bgl_no_FLAGS_v392"], bn["diferenca"]),
                "O pin do Mathlib nao tem a ponte de Fubini L2 vetorial (so' MemLp.comp_fst/comp_snd; WithLp/PiLp sao produtos finitos) [DECLARADO pela auditoria F1.3]."],
    "erratas": [
        {"ao_lado_de": "TGLExt/LightNetStandardWedgeDataBGL.lean instalado, cabecalho: «nada aqui e pedra; nada entra no kernel»",
         "dizia": "o cabecalho dizia que nada do arquivo e' pedra e que nada entra no kernel (era a sonda de auditoria da c1, so' sandbox).",
         "agora": "O arquivo e' INSTALADO no kernel da v392, byte a byte igual a sonda (sha256 %s), como TIPO: hipotese tipada, sem habitante. O cabecalho descreve o sandbox, nao o estado instalado." % bg["sha256"][:16],
         "lacuna_de_fidelidade": "A estrutura: um texto de auditoria para NAO entrar no kernel. Foi instalado depois, por decisao da gerencia (X19), sem trocar o cabecalho (trocaria os bytes auditados). A traducao falha porque o arquivo fala de si no tempo da auditoria.",
         "estatuto": "[REAL: bytes iguais, conferido por script] / [INPUT da gerencia: X19]", "assinatura": ASSINA},
        {"ao_lado_de": "o plano (PLANO_V392 §5, patch K11; levantamento A11): «+87 #print axioms», «6372/6372 com a X19», «209 a mais»",
         "dizia": "«+87 #print» e escada 6372/6372 com a X19.",
         "agora": "%d bandeiras ext_bgl_* (def/thm). As 87 sao as declaracoes que a regex de leitura do um.py devolve na sonda C_audit_delta_x19 (inclui estruturas e auxiliares). A soma das bandeiras novas do conjunto v392 e' a de FLAGS_v392.json (730)." % bn["bandeiras_ext_bgl_no_FLAGS_v392"],
         "lacuna_de_fidelidade": "A estrutura: o contador da escada conta def e thm. Foi escrito: o numero de declaracoes lidas pela regex, que tambem conta estruturas e auxiliares. A traducao falhou ao tomar o numero da sonda pelo da escada.",
         "estatuto": "[REAL: FLAGS_v392.json e RESULTADO_C_delta_x19.json lidos por script]", "assinatura": ASSINA},
    ],
    "leituras_do_operador": [],
    "extras": {"texto_para_a_fila_do_operador_reauditoria_c1": a13["reauditoria"]["texto_para_a_fila_do_operador"], "campos_de_D1a3OutputBGL": bg["campos_de_D1a3OutputBGL"],
               "citacoes_do_kernel_BGL_BW": E["bgl_citacoes_do_kernel"], "bandeiras": bn},
})
