# -*- coding: utf-8 -*-
"""aplicar_R2_textos_v405.py -- aplica, de uma vez, a parte de TEXTO da errata R2 da gerencia c1 (16:45 de 01/11/2026; revisao de terceiro NAO aprovou a30f9f0ebf90c277): delta, registros, runtime, gerar_candidato.
Cada substituicao exige a contagem exata (fail-closed). Tudo ou nada: primeiro calcula todos os arquivos, depois faz backup de BYTES e temporario -> conferir -> os.replace. Roda uma vez so' (a segunda falha na contagem, de proposito)."""
import os, re, sys, time
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
    assert c == n, (arq, c, n, old[:90])
    NOVOS[arq] = s.replace(old, new)


# ===================================================================================================== delta_v405.py
D = "delta_v405.py"
sub(D, "campos_fechados_e_leituras_v405 (o que fechou: os campos das estruturas; o que entra: os dois postos e as quatro leituras, cada uma com o nome da definicao Lean)",
    "campos_fechados_e_leituras_v405 (o que fechou: os campos das estruturas; o que entra: os dois postos e as leituras da cadeia da massa, lista que nao e' fechada, cada uma com o nome Lean)")
sub(D, "7 TGLExt.DiscoDeEuler (Disco de Euler: parada em tempo finito, a perda constante e' a lei canonica, o corte da ressonancia residual, K como invariante; Disco.doAcoplamento);",
    "7 TGLExt.DiscoDeEuler (Disco de Euler: E(t) linear e Omega^2 = K/E sao DEFINICOES; a E definida e' solucao do fluxo, the_flow_is_the_canonical_law; zera em tempo finito; Omega^2 sem cota antes disso; o corte E^3 = hbar^2.K; K como invariante; Disco.doAcoplamento; a taxa de dephasing lida como perda de energia e a inscricao do zero no infinito sao leituras do operador);")
sub(D, "A MOLDURA (errata da gerencia c1, 01/11/2026, 13:28; recibo RECIBO_ERRATA_PEDRAS_01nov.json):", "A MOLDURA (erratas da gerencia c1, 01/11/2026, 13:28 e 16:45; recibos RECIBO_ERRATA_PEDRAS_01nov.json e RECIBO_ERRATA_PEDRAS_R2_01nov.json):")
sub(D, "[INPUT/ONTO] as quatro leituras (massaDerivada; theta = pi/4 escrito em transicaoDerivada; a tonica (beta/alfa).u; R = beta.u^2), que entram como definicao;",
    "[INPUT/ONTO] as leituras da cadeia da massa (massaDerivada; theta = pi/4 escrito em transicaoDerivada; a tonica (beta/alfa).u; R = beta.u^2; e as demais de LEITURAS_DEFINICOES: a lista nao e' fechada), que entram como definicao ou identificacao;")
sub(D, "a fusao e' um posto que pagou perda; dois pontos fixos; o terminal le 1)", "a fusao e' um posto que pagou perda; dois pontos fixos; o terminal le 1 e o abismo le 0 na leitura binaria; ao lado, o polo omega do par le 1 na identidade: homonimo)")
sub(D, "# a composicao: o disco PARA em tempo finito (E(t0) = 0): sob a lei canonica com o invariante, a perda e' constante", "# a composicao: a energia DEFINIDA zera em tempo finito (E(t0) = 0); ler a taxa de dephasing como perda de energia e' leitura [INPUT/ONTO]")
sub(D, "# a ESTRELA: a inscricao do zero no infinito -- antes da parada a frequencia^2 nao tem cota", "# a ESTRELA: antes da parada Omega^2 nao tem cota [REAL]; [ONTO] o operador le isso como a inscricao do zero no infinito")
sub(D, "# a composicao: no Um posto, (1/2).omega = beta.sen45 -- a massa e' o ponto zero do psion e a unica entrada e' o acoplamento", "# a composicao: no Um posto, (1/2).omega = beta.sen45, sob as leituras R = beta.u^2 e (1/2).omega = massa: entram o acoplamento e essas leituras")
sub(D, "# 127 = 21 + 15 + 15 + 26 + 19 + 13 + 12 + 6 (lido dos recibos pela PINO_DAS_PEDRAS_DETALHE)", "# 128 = 21 + 15 + 15 + 26 + 19 + 13 + 13 + 6 (medido da fonte pela PINO_DAS_PEDRAS_DETALHE; a errata R2 deu um teorema novo ao disco)")
sub(D, '_stone("tensao", "MassaTensaoPura", "Massa = tensão pura",', '_stone("tensao", "MassaTensaoPura", "Massa=tensão pura",')
sub(D, '_stone("observador", "ObservadorTerminal", "Observador = terminal",', '_stone("observador", "ObservadorTerminal", "observador=terminal",')
sub(D, 'N_CHECKS = {"ponte": 7, "tensao": 6, "identidade": 6, "observador": 6, "diminuto": 6, "tonica": 6, "disco": 6, "psion": 7}', 'N_CHECKS = {"ponte": 7, "tensao": 6, "identidade": 6, "observador": 7, "diminuto": 6, "tonica": 6, "disco": 7, "psion": 7}')
sub(D, "entram um Um posto, uma alfa medida e as quatro leituras (massaDerivada; theta = pi/4 escrito em transicaoDerivada; a tonica (beta/alfa).u; R = beta.u^2); dadas essas entradas, a FORMA e' teorema",
    "entram um Um posto, uma alfa medida e as leituras da cadeia da massa (massaDerivada; theta = pi/4 escrito em transicaoDerivada; a tonica (beta/alfa).u; R = beta.u^2; e as demais da lista, que nao e' fechada); dadas essas entradas, a FORMA e' teorema")
sub(D, "decisao do operador de 31/10/2026: «o meu um absoluto é o um de 1 eV e a constante da estrutura fina é a magnitude (cauda) dessa INSCRIÇÃO no bulk», sha16 9445171a763afcfc)", "decisao do operador de 31/10/2026: «{FALA_UM_E_CAUDA}», sha16 9445171a763afcfc)")
sub(D, 'FRASES_V405 = [("OPERADOR_01nov_nomes_das_sete_pedras_e_tudo_derivado_verbatim.txt", FRASE_NOMES),',
    'DECISOES["D29"] = DECISOES["D29"].replace("{FALA_UM_E_CAUDA}", FRASE_UM_DE_1EV + " e " + FRASE_ALFA_CAUDA)   # a fala dele com a grafia dele (achado 12 da revisao de terceiro): as duas constantes sao substring da fala e a junta tambem; conferir_citacoes confere o candidato\n'
    'FRASES_V405 = [("OPERADOR_01nov_nomes_das_sete_pedras_e_tudo_derivado_verbatim.txt", FRASE_NOMES),')
sub(D, '''ERRATA_E12 = ("E12 -- o adendo 4 do handoff v405 (DiscoDeEuler r1) escreveu K = 4Mg^2 para o invariante do disco de Euler real; a conferencia de 31/10 (nomes_do_disco_conferencia_31out.txt) corrige para K = 6Mg^2 (Omega^2 = 4g/(a.alpha) com a energia M.g.a.alpha + a cinetica: o fator e' 6, nao 4); "''',
    '''ERRATA_E12 = ("E12 -- o adendo 4 do handoff v405 (DiscoDeEuler r1) e a pedra TGLExt/DiscoDeEuler.lean, antes da errata R2, escreveram K = 4Mg^2 para o invariante do disco de Euler real; a conferencia de 31/10 (nomes_do_disco_conferencia_31out.txt) corrige para K = 6Mg^2 (Omega^2 = 4g/(a.alpha) com a energia TOTAL (3/2).M.g.a.alpha: o fator e' 6; com a energia potencial sozinha seriam 4Mg^2, a conta antiga); a pedra diz agora 6Mg^2 com a energia total e guarda a conta antiga ao lado; "''')
sub(D, "Tres teoremas foram rebatizados antes do selo (RECIBO_ERRATA_PEDRAS_01nov.json; nenhuma prova mudou): nenhuma_hipotese_resta -> a_transicao_existe_para_todo_acoplamento; the_tonic_fixes_what_the_form_leaves_free -> the_tonic_lands_on_the_posted_unit; the_tonic_fixes_the_posted_one -> the_tonic_at_the_posted_one: o nome afirmava mais do que o teorema prova. As docstrings das pedras trazem a correcao AO LADO; o no-go de E0 NAO cai, ele se localiza no Um posto",
    "Quatro teoremas foram rebatizados antes do selo (RECIBO_ERRATA_PEDRAS_01nov.json e RECIBO_ERRATA_PEDRAS_R2_01nov.json; nenhuma prova mudou por isso): nenhuma_hipotese_resta -> a_transicao_existe_para_todo_acoplamento; the_tonic_fixes_what_the_form_leaves_free -> the_tonic_lands_on_the_posted_unit; the_tonic_fixes_the_posted_one -> the_tonic_at_the_posted_one; the_terminal_reads_one -> the_omega_pole_reads_one: o nome afirmava mais do que o teorema prova (no ultimo, um homonimo: o enunciado e' sobre o polo omega do par, nao sobre o nivel terminal da cascata). "
    "A revisao de terceiro pegou, antes do selo, frases residuais nas docstrings das oito pedras, corrigidas pela R2; a R2 deu ao disco o teorema the_flow_is_the_canonical_law e ao fecho do observador a leitura binaria (the_fixed_points_read_one_and_zero). As docstrings das pedras trazem a correcao AO LADO; o no-go de E0 NAO cai, ele se localiza no Um posto")
sub(D, '''VERBATIM_ORIGEM_V405 = sorted(glob.glob(os.path.join(_CUN_ESP, "OPERADOR_30out_*_verbatim.txt"))) + sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_30out_*_verbatim.txt"))) \\
    + sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_31out_*_verbatim.txt"))) + sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_01nov_*_verbatim.txt"))) + [_ENSAIO_ORIGINAL]
def verbatim_origem_pelo_glob():
    """a lista das falas pelo glob, como esta no disco AGORA (a lista que vale para o candidato e a congelada abaixo)."""
    return sorted(glob.glob(os.path.join(_CUN_ESP, "OPERADOR_30out_*_verbatim.txt"))) + sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_30out_*_verbatim.txt"))) + sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_31out_*_verbatim.txt"))) + sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_01nov_*_verbatim.txt"))) + [_ENSAIO_ORIGINAL]
''', '''# A LISTA DE EXCLUSAO (decisao da gerencia c1, 01/11/2026, errata R2): falas que ficam no acervo e NAO sao embutidas no um.py publico. A chave e' o sha16 do arquivo, lido na hora: o nome do arquivo traz o nome do terceiro e nao viaja para nenhum artefato gerado. O glob e o congelado passam por aqui, e a fala excluida nao entra em VERBATIM_ORIGEM_V405, em insumos nem no candidato.
VERBATIM_EXCLUIDAS_V405 = {"25c09b91c2a226c7": "a fala da leitura 3 de 30/10: tem dado pessoal de terceiro e nenhuma pedra a usa"}


def _sem_excluidas(lista_):
    """tira da lista as falas de VERBATIM_EXCLUIDAS_V405, pelo sha16 dos bytes do arquivo."""
    return [p_ for p_ in lista_ if __import__("hashlib").sha256(open(p_, "rb").read()).hexdigest()[:16] not in VERBATIM_EXCLUIDAS_V405]


VERBATIM_ORIGEM_V405 = _sem_excluidas(sorted(glob.glob(os.path.join(_CUN_ESP, "OPERADOR_30out_*_verbatim.txt"))) + sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_30out_*_verbatim.txt")))
                                      + sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_31out_*_verbatim.txt"))) + sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_01nov_*_verbatim.txt"))) + [_ENSAIO_ORIGINAL])
def verbatim_origem_pelo_glob():
    """a lista das falas pelo glob, como esta no disco AGORA, sem as excluidas (a lista que vale para o candidato e a congelada abaixo)."""
    return _sem_excluidas(sorted(glob.glob(os.path.join(_CUN_ESP, "OPERADOR_30out_*_verbatim.txt"))) + sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_30out_*_verbatim.txt"))) + sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_31out_*_verbatim.txt"))) + sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_01nov_*_verbatim.txt"))) + [_ENSAIO_ORIGINAL])
''')
sub(D, '''    VERBATIM_ORIGEM_V405 = list(json.load(open(_CONGELADO, encoding="utf-8"))["arquivos"])
assert all(os.path.exists(p_) for p_ in VERBATIM_ORIGEM_V405) and len(VERBATIM_ORIGEM_V405) == len(set(VERBATIM_ORIGEM_V405))
''', '''    VERBATIM_ORIGEM_V405 = list(json.load(open(_CONGELADO, encoding="utf-8"))["arquivos"])
assert all(os.path.exists(p_) for p_ in VERBATIM_ORIGEM_V405) and len(VERBATIM_ORIGEM_V405) == len(set(VERBATIM_ORIGEM_V405))
assert _sem_excluidas(VERBATIM_ORIGEM_V405) == VERBATIM_ORIGEM_V405, "uma fala da lista de exclusao esta na lista embutida (refaca VERBATIM_CONGELADO_v405.json)"
''')
sub(D, '''"definicao_lean": "TGLExt.PontoZeroDoPsion.pagamentoComoCurvatura", "modulo": "TGLExt/PontoZeroDoPsion.lean", "entra_como": "DEFINICAO, nao teorema"}]''',
    '''"definicao_lean": "TGLExt.PontoZeroDoPsion.pagamentoComoCurvatura", "modulo": "TGLExt/PontoZeroDoPsion.lean", "entra_como": "DEFINICAO, nao teorema"},
                       {"n": 5, "estatuto": "INPUT/ONTO", "leitura": "o meio-tom e^(-1/2): o tom e' a nat, leitura do operador; definicao da mesma natureza da tonica, necessaria a E0 = u", "definicao_lean": "TGLExt.LeiDoDiminuto.meioTom", "modulo": "TGLExt/LeiDoDiminuto.lean", "entra_como": "DEFINICAO, nao teorema"},
                       {"n": 6, "estatuto": "INPUT", "leitura": "a dispersao omega^2 = 2.beta.R: Tratado, secao 3, teoria propria, nao literatura", "definicao_lean": "TGLExt.PontoZeroDoPsion.omegaSq", "modulo": "TGLExt/PontoZeroDoPsion.lean", "entra_como": "DEFINICAO, nao teorema"},
                       {"n": 7, "estatuto": "INPUT/ONTO", "leitura": "a identificacao (1/2).omega = massa: o enunciado de the_mass_is_the_zero_point iguala numeros; o nome e' leitura", "definicao_lean": "TGLExt.PontoZeroDoPsion.the_mass_is_the_zero_point", "modulo": "TGLExt/PontoZeroDoPsion.lean", "entra_como": "LEITURA, nao teorema"},
                       {"n": 8, "estatuto": "INPUT/ONTO", "leitura": "o acoplamento da onda de materia = a massa inscrita: a hipotese de area_por_volta_da_massa_inscrita", "definicao_lean": "TGLExt.MassaTensaoPura.area_por_volta_da_massa_inscrita", "modulo": "TGLExt/MassaTensaoPura.lean", "entra_como": "HIPOTESE do enunciado, nao teorema"},
                       {"n": 9, "estatuto": "ONTO", "leitura": "b = 0 lido como o foton: foton_sem_massa e' algebra de uma forma generica; TGLCoupling exclui b = 0 e nenhum termo do kernel tem foton", "definicao_lean": "TGLExt.MassaTensaoPura.foton_sem_massa", "modulo": "TGLExt/MassaTensaoPura.lean", "entra_como": "LEITURA, nao teorema"},
                       {"n": 10, "estatuto": "INPUT/ONTO", "leitura": "no disco, a taxa de dephasing lida como taxa de perda de energia: the_flow_is_the_canonical_law e' sobre a energia definida", "definicao_lean": "TGLExt.DiscoDeEuler.Disco.the_flow_is_the_canonical_law", "modulo": "TGLExt/DiscoDeEuler.lean", "entra_como": "LEITURA, nao teorema"}]
LISTA_DE_LEITURAS_FECHADA = False                            # a lista acima e' a da cadeia da massa e NAO e' fechada (achado 7 da revisao de terceiro; nota AO LADO nas pedras); as quatro primeiras sao as centrais''')
sub(D, '''DADOS_DO_SISTEMA = ["os dados do sistema que le: o contraste g e o relogio kappa (emprestimo); no disco, K, tau e E0 (a identidade do disco) [INPUT]", "a dispersao do psion omega^2 = 2.beta.R como definicao (Tratado, §3) [KNOWN]"]''',
    '''DADOS_DO_SISTEMA = ["os dados do sistema que le: o contraste g e o relogio kappa (emprestimo); no disco, K, tau e E0 (a identidade do disco) [INPUT]", "o ponto zero (1/2).hbar.omega [KNOWN]; a dispersao do psion nao e' [KNOWN]: e' [INPUT, Tratado §3] e entra como definicao (omegaSq, leitura 6)"]''')

# ===================================================================================================== registros_v405.py
R = "registros_v405.py"
sub(R, 'RECIBO_ERRATA_ARQ = os.path.join(DL.ESTUDO_E0, "RECIBO_ERRATA_PEDRAS_01nov.json")\n',
    'RECIBO_ERRATA_ARQ = os.path.join(DL.ESTUDO_E0, "RECIBO_ERRATA_PEDRAS_01nov.json")\nCHAVE_RECIBO_ERRATA_R2 = "recibo_errata_r2_das_pedras_01nov"\nRECIBO_ERRATA_R2_ARQ = os.path.join(DL.ESTUDO_E0, "RECIBO_ERRATA_PEDRAS_R2_01nov.json")\n')
sub(R, "compilada e provada no sandbox k404c e no k405c;", "compilada e provada no sandbox k405c;")
sub(R, '''"papel": "o recibo da ERRATA DAS PEDRAS (gerencia c1, 01/11/2026): sha256 antes e depois dos sete arquivos, os tres teoremas rebatizados; nenhuma prova mudou [DECLARADO na origem; o sha256 de cada pedra e os termos sao conferidos pelo gerador e pelo kernel do rito]"},''',
    '''"papel": "o recibo da ERRATA DAS PEDRAS (gerencia c1, 01/11/2026): sha256 antes e depois dos sete arquivos, os tres teoremas rebatizados; nenhuma prova mudou [DECLARADO na origem; o sha256 de cada pedra e os termos sao conferidos pelo gerador e pelo kernel do rito]"},
          {"chave": CHAVE_RECIBO_ERRATA_R2, "arquivo": os.path.join(INS, os.path.basename(RECIBO_ERRATA_R2_ARQ)), "papel": "o recibo da ERRATA R2 DAS PEDRAS (gerencia c1, 01/11/2026, depois da revisao de terceiro): sha256 antes e depois dos oito arquivos; duas mudancas de codigo (o teorema novo do disco; o quarto rebatismo e o fecho do observador com a leitura binaria); o resto e' docstring e titulo de secao [DECLARADO na origem; o sha256 de cada pedra e os termos sao conferidos pelo gerador e pelo kernel do rito]"},''')
sub(R, "the_observers_posto_is_the_terminal: the terminal is unique, the only fixed point of the reading, res judicata, a posto that paid loss, two fixed points, and omega(I) = 1\"",
    "the_observers_posto_is_the_terminal: the terminal is unique, the only fixed point of the reading, res judicata, a posto that paid loss, two fixed points; the terminal reads 1 and the abyss reads 0 on the binary reading (the_fixed_points_read_one_and_zero); beside it, the omega pole of the pair reads 1 on the identity (a homonym: no term links the two; the link is the operator's [ONTO] reading)\"")
sub(R, '''"disco": "Disco.frequency_squared_unbounded_at_the_stop: before the stop Omega^2 = K/E has no bound (the inscription of zero at infinity); Disco.stops_in_finite_time: under the canonical law with the invariant Omega^2 . E = K the loss is constant and E(t0) = 0",''',
    '''"disco": "Disco.frequency_squared_unbounded_at_the_stop: before the stop Omega^2 = K/E has no bound, for the defined linear energy [REAL]; the operator reads this as the inscription of zero at infinity [ONTO]; Disco.stops_in_finite_time: the defined energy reaches zero at t0 = E0/c; Disco.the_flow_is_the_canonical_law: before t0, dE/dt = -Gamma.E, so the defined E solves the flow; reading the dephasing rate as an energy-loss rate is an [INPUT/ONTO] input",''')
sub(R, "(the payment read as curvature, a definition) and omega^2 = 2 beta R, (1/2) omega = beta . sin45 . u = neutrinoMassForm c u; at the posted one (u = 1) the inputs are the coupling and that reading\"",
    "(the payment read as curvature, a definition) and omega^2 = 2 beta R (a definition, Treatise section 3), (1/2) omega = beta . sin45 . u = neutrinoMassForm c u; the statement equates numbers: that (1/2) omega IS the mass is a reading [ONTO]; at the posted one (u = 1) the inputs are the coupling and those readings\"")
sub(R, 'RENOMES_DA_ERRATA = json.load(open(RECIBO_ERRATA_ARQ, encoding="utf-8"))["teoremas_renomeados"]\n',
    '''RENOMES_DA_ERRATA = dict(json.load(open(RECIBO_ERRATA_ARQ, encoding="utf-8"))["teoremas_renomeados"])
_r2_ = json.load(open(RECIBO_ERRATA_R2_ARQ, encoding="utf-8"))
assert any("the_terminal_reads_one" in m_ and "the_omega_pole_reads_one" in m_ for m_ in _r2_["codigo_mudado"]), "o recibo R2 nao traz o quarto rebatismo"
RENOMES_DA_ERRATA["ObservadorTerminal.the_terminal_reads_one"] = "ObservadorTerminal.the_omega_pole_reads_one"   # (o recibo R1 traz um dict; o R2 traz a frase, conferida acima)
''')
# --- a ponte
sub(R, "a unica massa que o programa deriva de beta e' a do neutrino", "a unica massa cuja forma o programa escreve a partir de beta e de u e' a do neutrino")
# --- a tensao
sub(R, "e os tres termos da «ligacao que falta» citados fora: frameCovectorStress", "e os tres termos da ligacao que ainda falta, citados fora: frameCovectorStress")
sub(R, "prova: (1) a massa e' o produto do acoplamento (beta.(sqrt2/2).E0); (2) o foton (acoplamento zero) nao tem massa e toda a energia atravessa; com acoplamento positivo ha massa e a transmissao e' menor que o incidente; (3) a massa e' o residuo (incidente menos transmitido, lido na projecao transversal); ",
    "prova: (1) a forma generica massaForma(b, E0) = b.(sqrt2/2).E0; sob a leitura massaDerivada, a massa e' o produto do acoplamento (beta.(sqrt2/2).E0); (2) massaForma anula com b = 0 e entao toda a energia atravessa (foton_sem_massa: algebra de uma forma generica); [ONTO] b = 0 e' LIDO como o foton, que acopla pela energia, nao por massa: TGLCoupling exclui b = 0 e nenhum termo do kernel tem foton; com acoplamento positivo ha massa e a transmissao e' menor que o incidente; (3) a forma se reparte como residuo (incidente menos transmitido, lido na projecao transversal); ")
sub(R, "a parcela nunca quita (0 < parcela < 1) e e' no maximo beta.g.P", "a parcela nunca quita numa volta (0 < parcela < 1; para qualquer tempo finito: the_charge_never_completes) e e' no maximo beta.g.P")
sub(R, "a leitura do nome «Massa = tensao pura» (o principal e' o retido projetado)", "a leitura do nome «Massa=tensão pura» (o principal e' o retido projetado)")
sub(R, "a massa e' beta.(sqrt2/2).u = o m_nu do programa a 1e-12; o foton nao tem massa; a massa e' o residuo;", "a massa e' beta.(sqrt2/2).u = o m_nu do programa a 1e-12; a forma anula com b = 0, lido como o foton [ONTO]; a forma se reparte como residuo;")
sub(R, '''"nao_diz": ["que o magnetismo tenha termo no kernel",''', '''"nao_diz": ["que b = 0 seja o foton por teorema (e' leitura [ONTO]: TGLCoupling exclui b = 0 e nenhum termo do kernel tem foton)", "que o magnetismo tenha termo no kernel",''')
sub(R, '"name_status": {"quem": "operador", "quando": "01/11/2026", "nome": "Massa = tensão pura",', '"name_status": {"quem": "operador", "quando": "01/11/2026", "nome": "Massa=tensão pura",')
sub(R, '''"campos_fechados": {k_: v_["fechou_com"] for k_, v_ in DL.CAMPOS_FECHADOS.items() if "fiel" in k_}, "assinatura_das_erratas": ASSINA},''',
    '''"campos_fechados": {k_: v_["fechou_com"] for k_, v_ in DL.CAMPOS_FECHADOS.items() if "fiel" in k_}, "leituras_que_entram": [l_ for l_ in DL.LEITURAS_DEFINICOES if l_["n"] in (8, 9)], "assinatura_das_erratas": ASSINA},''')
sub(R, "TGL_MASSA_TENSAO_PURA_V405__UNDER_THE_READING_MASSADERIVADA_MASS_IS_THE_PRODUCT_OF_THE_COUPLING_AND_THE_RESIDUE__THE_PHOTON_HAS_NO_MASS__THE_LOAN_IS_CONSTRUCTED_ONE_TURN_KAPPA_P_2PI_IS_A_THEOREM__",
    "TGL_MASSA_TENSAO_PURA_V405__UNDER_THE_READING_MASSADERIVADA_MASS_IS_THE_PRODUCT_OF_THE_COUPLING_AND_THE_RESIDUE__THE_FORM_VANISHES_AT_B_ZERO_READ_AS_THE_PHOTON__THE_LOAN_IS_CONSTRUCTED_ONE_TURN_KAPPA_P_2PI_IS_A_THEOREM__")
# --- o observador
sub(R, "[REAL] o posto terminal e' um so'; o colapso total e' um Um posto do kernel (nao pressuposto; pagou perda; dois pontos fixos); [INPUT] «observador=terminal»",
    "[REAL] num modelo finito cujos niveis sao rotulos: o posto terminal e' um so'; o colapso total e' um Um posto do kernel (nao pressuposto; pagou perda; dois pontos fixos); o terminal le 1 e o abismo le 0 na leitura binaria (the_fixed_points_read_one_and_zero); [ONTO] o polo omega do par, que le 1 na identidade (the_omega_pole_reads_one), e' homonimo: nenhum termo o liga ao nivel terminal da cascata, e liga-los e' leitura do operador; [INPUT] «observador=terminal»")
sub(R, "(5) sem o abismo a fusao le como pressuposta e nenhum Um posto le assim: o par 1 = 1 | 1 = 0 e' necessario; (6) o terminal le 1 (omega(I) = 1). \"\n                  \"O calculo CONFERE a cascata finita e o par (16 posicoes e leituras) e le omega(I) = 1 do core deste rito\",",
    "(5) sem o abismo a fusao le como pressuposta e nenhum Um posto le assim: o par 1 = 1 | 1 = 0 e' necessario; (6) o terminal le 1 e o abismo le 0 na leitura binaria (the_fixed_points_read_one_and_zero); (7) ao lado, o polo omega do par le 1 na identidade (the_omega_pole_reads_one, omega(I) = 1): HOMONIMO, dito: em TheAlphaAndTheOmega a palavra terminal nomeia o POLO do par alfa/omega; aqui nomeia o nivel gravidade da cascata; nenhum termo liga os dois, e liga-los e' leitura [ONTO] do operador. \"\n                  \"O calculo CONFERE a cascata finita e o par (quatro niveis e cinco posicoes) e le omega(I) = 1 do core deste rito\",")
sub(R, "sem o abismo a leitura preservada e' constante; omega(I) = 1 no core\",", "sem o abismo a leitura preservada e' constante; o terminal le 1 e o abismo le 0 na leitura binaria; ao lado, omega(I) = 1 no core (o polo omega do par: homonimo)\",")
sub(R, '''"nao_diz": ["que a gravidade, a luz ou o observador humano sejam entidades desta pedra (os niveis sao rotulos de posicao)", "que a pedra construa o colapso fisico",''',
    '''"nao_diz": ["que a gravidade, a luz ou o observador humano sejam entidades desta pedra (os niveis sao rotulos de posicao)", "que o polo omega do par e o nivel terminal da cascata sejam o mesmo objeto (homonimo: nenhum termo os liga; liga-los e' leitura [ONTO] do operador)", "que a pedra construa o colapso fisico",''')
sub(R, '"name_status": {"quem": "operador", "quando": "31/10/2026 (mantido em 01/11/2026)", "nome": "Observador = terminal",', '"homonimo_terminal": {"status": "ONTO", "polo": "the_omega_pole_reads_one: omega(I) = 1, o polo omega do par alfa/omega (TheAlphaAndTheOmega)", "nivel": "the_fixed_points_read_one_and_zero: o nivel gravidade da cascata, na leitura binaria", "liga_os_dois": "nenhum termo; a ligacao e\' leitura do operador", "is_a_kernel_term": False},\n                   "name_status": {"quem": "operador", "quando": "31/10/2026 (mantido em 01/11/2026)", "nome": "observador=terminal",')
sub(R, "THE_PAIR_IS_NECESSARY__THE_TERMINAL_READS_ONE__READ_AGAINST_THE_KERNEL_TRIO", "THE_PAIR_IS_NECESSARY__THE_FIXED_POINTS_READ_ONE_AND_ZERO__THE_OMEGA_POLE_IS_A_HOMONYM_ITS_LINK_IS_A_READING__READ_AGAINST_THE_KERNEL_TRIO")
# --- o diminuto
sub(R, "[REAL] o meio-tom pinado e^(-1/2); beta = alfa.e^(1/2); dadas as entradas, a FORMA m = U.alfa.e^(1/2).sqrt2/2 e' teorema; [INPUT/ONTO] a tonica (beta/alfa).u entra como DEFINICAO:",
    "[REAL] o meio-tom pinado e^(-1/2) esta em (0, 1) e desfaz o sqrt e; beta = alfa.e^(1/2); dadas as entradas, a FORMA m = U.alfa.e^(1/2).sqrt2/2 e' teorema; [INPUT/ONTO] o meio-tom (meioTom: o tom e' a nat) e a tonica (beta/alfa).u entram como DEFINICAO:")
sub(R, "(3) a lei: E0 = meioTom.E_pent; dada a tonica, E0 esta determinado; ", "(3) a lei: E0 = meioTom.E_pent; dada a tonica, E0 esta determinado, e a liberdade de escala passa de E0 para a tonica: o no-go NAO cai; ")
sub(R, '''"que E0 = u fixe u (e' identidade algebrica)", "que a escala tenha sido escolhida pelo dado (nem 1,02 eV nem outra)"]''', '''"que E0 = u fixe u (e' identidade algebrica)", "que a lei levante o no-go: a mesma tonica da' o mesmo E0, mas a tonica segue livre (no_function_of_the_inscription_fixes_E0)", "que a escala tenha sido escolhida pelo dado (nem 1,02 eV nem outra)"]''')
sub(R, '''if "E_pent" in k_}, "leituras_que_entram": [l_ for l_ in DL.LEITURAS_DEFINICOES if l_["n"] == 3], "assinatura_das_erratas": ASSINA},''', '''if "E_pent" in k_}, "leituras_que_entram": [l_ for l_ in DL.LEITURAS_DEFINICOES if l_["n"] in (3, 5)], "assinatura_das_erratas": ASSINA},''')
# --- o disco: a funcao inteira
s_ = carrega(R); i_ = s_.index("def texto_disco():"); j_ = s_.index("def texto_psion():")
NOVOS[R] = s_[:i_] + '''def texto_disco():
    return {
        "estatuto": "[REAL] os termos do kernel (os 13 teoremas do contrato, no trio, no modulo da pedra; os termos de suporte: TGLCoupling.beta_pos, Fundacao.the_fall_never_lands, Fundacao.abismo) e o calculo sobre um disco-modelo (K, tau, E0 adimensionais: dados do disco) com beta = alfa CODATA 2018 x sqrt(e) em runtime; "
                    "[DEF] a energia linear E(t) = E0 - c.t e Omega^2 = K/E; [REAL] dadas essas definicoes: Gamma.E = c; a E definida e' solucao do fluxo dE/dt = -Gamma.E antes da parada (the_flow_is_the_canonical_law); E(t0) = 0 em tempo finito; Omega^2 sem cota antes de t0; o corte E^3 = hbar^2.K (algebra); a escala e' o invariante; [INPUT/ONTO] a taxa de dephasing lida como taxa de perda de energia; [ONTO] a inscricao do zero absoluto no infinito e a terceira lei na forma do disco, leituras do operador sobre Omega^2 sem cota; [KNOWN] o disco de Euler (Moffatt, Nature 404, 833, 2000); [INPUT] a cunhagem (31/10/2026, sha16 %s: «é a ressonância da parada do disco de euler sobre o espelho») e "
                    "«O disco é o substrato psionico, o condensado psionico» (sha16 %s); o nome (sha16 %s); [ONTO] a leitura do disco como o condensado psionico; [OPEN] QUAL e' o disco (o invariante K) -- pergunta do operador; nenhum K escolhido pelo alvo" % (S16(N_DISCO), S16(N_PSION), S16(N_NOMES)),
        "escopo": "[REAL] A pedra TGLExt/DiscoDeEuler.lean (Disco de Euler, nome do operador) tipa o disco: um invariante K = Omega^2.E > 0, a lei canonica (beta, tau*) e a energia inicial. [DEF] A energia e' linear por definicao, E(t) = E0 - c.t com c = (1/2).beta.tau*.K (E, E_linear), e Omega^2 = K/E (omegaSq). Dadas essas definicoes, prova: (1) Gamma_Omega.E = c (the_loss_is_the_canonical_law) e, antes da parada, dE/dt = -Gamma_Omega.E (the_flow_is_the_canonical_law): a E definida e' uma solucao do fluxo; ler a taxa de DEPHASING como taxa de perda de ENERGIA e' entrada [INPUT/ONTO], nao teorema; E(t0) = 0 em tempo finito (stops_in_finite_time); "
                  "(2) Omega^2 SEM COTA: antes da parada Omega^2 = K/E nao tem cota, para a energia linear definida (frequency_squared_unbounded_at_the_stop) [REAL]; [ONTO] o operador le isso como a inscricao do zero absoluto no infinito e como a terceira lei na forma do disco: leitura dele, nao teorema; (3) o contraste com o abismo: com taxa constante a energia nunca toca o zero (with_constant_rate_the_fall_never_lands); "
                  "(4) o corte: hbar.Omega = E acontece sse E^3 = hbar^2.K (the_residual_resonance_iff) [REAL, algebra]; [ONTO] o operador le a energia do corte como a ressonancia que permanece e a escala que nasce no infinito; (5) a parede nomeada: K = (e^(1/2).U)^3/hbar^2 (the_scale_is_the_invariant); (6) o campo fechado: beta do disco vem do acoplamento (Disco.doAcoplamento). "
                  "O calculo CONFERE num disco-modelo e REGISTRA, em SI, o K que a nota posta de 1 eV exige (o tamanho da parede), sem o escolher",
        "limites": ["[REAL] a pedra NAO identifica o disco da TGL com nenhum sistema fisico nem deriva a unidade: K, tau e E0 sao DADOS do disco (a sua identidade), nao hipoteses sobre a teoria; qual e' o disco e' pergunta do operador (a pergunta nas quatro linguas de 31/10 fica aberta); o Kimi mediu a mesma parede (U_E_NOT_DERIVED) e tem razao",
                    "[DEF + INPUT/ONTO] E(t) linear e Omega^2 = K/E sao definicoes da estrutura, nao consequencias; o teorema the_flow_is_the_canonical_law diz que a E definida e' UMA solucao do fluxo; que a taxa de dephasing Gamma seja taxa de perda de energia e' entrada [INPUT/ONTO] (a leitura 10 de campos_fechados_e_leituras_v405)",
                    "[KNOWN] os expoentes de Moffatt vem da dissipacao viscosa do ar; aqui a dissipacao e' a canonica da TGL (Gamma proporcional a omega^2): e' o disco da TGL, nao o de Moffatt",
                    DL.ERRATA_E12] + _LIM_COMUM,
        "diz": ["a pedra DiscoDeEuler esta no kernel do rito, no trio, com bandeira e proveniencia no modulo dela; os 13 teoremas do contrato e os termos de suporte sao lidos deste kernel",
                "o calculo num disco-modelo (K = 3, tau = 0,7, E0 = 2; beta do rito): Gamma.E = c; a E definida satisfaz dE/dt = -Gamma.E (diferenca finita centrada); E(t0) = 0; Omega^2 vence toda cota antes da parada; com taxa constante nunca para; o corte E^3 = hbar^2.K; K = (e^(1/2).U)^3/hbar^2; em SI o K que a nota posta exige fica registrado",
                "Omega^2 nao tem cota antes da parada [REAL]; a inscricao do zero absoluto no infinito e a terceira lei sao leituras do operador [ONTO]; a parede (qual e' o disco) esta nomeada, nao derivada"],
        "nao_diz": ["que o disco da TGL seja um sistema fisico identificado", "que a unidade u tenha sido derivada do disco", "que o invariante K tenha sido escolhido pelo alvo (nenhum numero de K e' escolhido)", "que a dissipacao do disco real (viscosa) seja a canonica", "que a energia seja linear por teorema (e' definicao; o teorema e' que a E definida resolve o fluxo)", "que a taxa de dephasing seja taxa de perda de energia por teorema (e' entrada [INPUT/ONTO])", "que a inscricao do zero no infinito ou a terceira lei sejam teoremas (sao leituras [ONTO] do operador)"] + _NAO_COMUM,
        "extras": {"cited_support": sorted(S["disco"]["support"]), "reading_disk": {"status": "ONTO/OPEN", "content": DL.LEITURA_V405["disco"], "is_a_kernel_term": False},
                   "name_status": {"quem": "operador", "quando": "01/11/2026 (nome provisorio mantido)", "nome": "Disco de Euler", "sha16_da_fala": S16(N_NOMES)},
                   "campos_fechados": {k_: v_["fechou_com"] for k_, v_ in DL.CAMPOS_FECHADOS.items() if "disco" in k_}, "leituras_que_entram": [l_ for l_ in DL.LEITURAS_DEFINICOES if l_["n"] == 10], "parede": "K = (e^(1/2).U)^3/hbar^2: a entrada dimensional e' o invariante do disco; QUAL e' o disco e' do operador", "assinatura_das_erratas": ASSINA},
        "veredito_ok": "TGL_DISCO_DE_EULER_V405__E_AND_OMEGA_SQUARED_ARE_DEFINED__THE_DEFINED_ENERGY_SOLVES_THE_FLOW_OF_THE_CANONICAL_LAW_AND_REACHES_ZERO_IN_FINITE_TIME__THE_DEPHASING_RATE_READ_AS_ENERGY_LOSS_IS_A_READING__BEFORE_THE_STOP_OMEGA_SQUARED_HAS_NO_BOUND__THE_ZERO_AT_INFINITY_AND_THE_THIRD_LAW_ARE_THE_OPERATORS_ONTO_READINGS__WITH_CONSTANT_RATE_THE_FALL_NEVER_LANDS__"
                       "THE_CUT_E_CUBED_EQUALS_HBAR2_K__THE_SCALE_IS_THE_INVARIANT_THE_WALL_IS_NAMED_NOT_DERIVED__BETA_FROM_THE_COUPLING__READ_AGAINST_THE_KERNEL_TRIO_AT_BETA_ALPHA_SQRT_E__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


''' + s_[j_:]
# --- o psion
sub(R, "hbar.omega = 2m; Tetelestai: a cobranca se consuma so' no limite; [KNOWN] a dispersao do psion (Tratado, §3) e o ponto zero (1/2).hbar.omega; ",
    "hbar.omega = 2m; a cobranca se consuma so' no limite; [INPUT/ONTO] o nome Tetelestai e a identificacao (1/2).omega = massa (o enunciado iguala numeros; o nome e' leitura); [INPUT, Tratado §3] a dispersao omega^2 = 2.beta.R, que entra como definicao (omegaSq); [KNOWN] o ponto zero (1/2).hbar.omega; ")
sub(R, "(2) com a dispersao do Tratado (omega^2 = 2.beta.R, m0 = 0), o quantum do psion e' omega = sqrt2.beta.u;", "(2) com a dispersao do Tratado, que entra como definicao (omegaSq: omega^2 = 2.beta.R, m0 = 0), o quantum do psion e' omega = sqrt2.beta.u;")
sub(R, "a coincidencia e' a aritmetica (1/2).sqrt2 = sen45; (4) hbar.omega = 2m; ", "a coincidencia e' a aritmetica (1/2).sqrt2 = sen45; o enunciado iguala numeros: que (1/2).omega SEJA a massa e' leitura [ONTO]; (4) hbar.omega = 2m; ")
sub(R, "(5) TETELESTAI, o limite assintotico: a cobranca continua do kernel tende a 1 quando t -> infinito e e' < 1 em todo t finito: o pagamento se consuma so' no limite; o que permanece no limite e' o ponto zero; (6) no Um posto (u = 1) entram o acoplamento e a leitura R = beta.u^2. ",
    "(5) TETELESTAI, nome do operador para o limite assintotico: a cobranca continua do kernel tende a 1 quando t -> infinito e e' < 1 em todo t finito: o pagamento se consuma so' no limite; [ONTO] o operador le o que permanece no limite como o ponto zero: nenhum teorema liga o limite da cobranca a (1/2).omega; the_zero_point_closes so' os conjuga; (6) no Um posto (u = 1) entram o acoplamento e as leituras R = beta.u^2 e (1/2).omega = massa. ")
sub(R, '''"nao_diz": ["que a unidade u tenha sido derivada", "que a curvatura do psion seja a curvatura da natureza (e' o pagamento, lido como curvatura dentro do bulk [ONTO])",''',
    '''"nao_diz": ["que a unidade u tenha sido derivada", "que (1/2).omega SEJA a massa (o enunciado iguala numeros; o nome e' leitura [ONTO])", "que o limite da cobranca seja o ponto zero (nenhum teorema liga os dois; e' leitura [ONTO])", "que a dispersao omega^2 = 2.beta.R seja literatura (e' teoria propria, Tratado §3, e entra como definicao)", "que a curvatura do psion seja a curvatura da natureza (e' o pagamento, lido como curvatura dentro do bulk [ONTO])",''')
sub(R, '''"coincidem_por": "aritmetica: (1/2).sqrt2 = sen45"}, "leituras_que_entram": [l_ for l_ in DL.LEITURAS_DEFINICOES if l_["n"] == 4], "assinatura_das_erratas": ASSINA},''',
    '''"coincidem_por": "aritmetica: (1/2).sqrt2 = sen45"}, "leituras_que_entram": [l_ for l_ in DL.LEITURAS_DEFINICOES if l_["n"] in (4, 6, 7)], "assinatura_das_erratas": ASSINA},''')
# --- cunhagens: as erratas E12 e E13
sub(R, '''{"ao_lado_de": "o adendo 4 do handoff v405 (DiscoDeEuler r1), que escreveu Omega^2.E = 4Mg^2",''', '''{"ao_lado_de": "o adendo 4 do handoff v405 (DiscoDeEuler r1) e a pedra DiscoDeEuler antes da errata R2, que escreveram Omega^2.E = 4Mg^2",''')
sub(R, "a r1 contou so' a energia potencial; a conferencia de 31/10 (nomes_do_disco_conferencia_31out.txt) inclui a cinetica e da 6Mg^2;", "a r1 contou so' a energia potencial; a conferencia de 31/10 (nomes_do_disco_conferencia_31out.txt) conta a energia total e da 6Mg^2; a pedra guardava as duas contas sem nota, e a R2 pos a nota ao lado;")
sub(R, "(a leitura que a gerencia c1 fez dos campos fechados) e tres nomes de teorema nas pedras antes do selo", "(a leitura que a gerencia c1 fez dos campos fechados) e quatro nomes de teorema nas pedras antes do selo")
sub(R, "teoremas chamados nenhuma_hipotese_resta, the_tonic_fixes_what_the_form_leaves_free e the_tonic_fixes_the_posted_one.", "teoremas chamados nenhuma_hipotese_resta, the_tonic_fixes_what_the_form_leaves_free, the_tonic_fixes_the_posted_one e the_terminal_reads_one.")
sub(R, "corrigido AO LADO antes do selo (RECIBO_ERRATA_PEDRAS_01nov.json: nenhuma prova mudou)", "corrigido AO LADO antes do selo (RECIBO_ERRATA_PEDRAS_01nov.json e RECIBO_ERRATA_PEDRAS_R2_01nov.json: nenhuma prova mudou por isso)")
# --- campos fechados
sub(R, '''cks2.append(CH("n%d" % m, "a DEFINICAO Lean do que ENTRA, %s, e' emitida pelo compilador no modulo dela (TGL_DECL_SOURCE)" % t_.split(".")[-1],''', '''cks2.append(CH("n%d" % m, "o termo Lean do que ENTRA, %s, e' emitido pelo compilador no modulo dele (TGL_DECL_SOURCE)" % t_.split(".")[-1],''')
sub(R, '''    cks2.append(CH("n%d" % m, "o recibo da nomeacao diz sorry 0 no build das pedras",''', '''    cks2.append(CH("n%d" % m, "o recibo da errata R2 das pedras (fonte pinada) cobre as oito pedras", "fonte:" + CHAVE_RECIBO_ERRATA_R2, ["pedras"], "tamanho_igual", 8)); m += 1
    cks2.append(CH("n%d" % m, "o recibo da errata R2 diz as duas mudancas de codigo", "fonte:" + CHAVE_RECIBO_ERRATA_R2, ["codigo_mudado"], "tamanho_igual", 2)); m += 1
    cks2.append(CH("n%d" % m, "o recibo da nomeacao diz sorry 0 no build das pedras",''')
sub(R, "WHAT_ENTERS_ONE_POSTED_ONE_ONE_MEASURED_ALPHA_AND_FOUR_READINGS__", "WHAT_ENTERS_ONE_POSTED_ONE_ONE_MEASURED_ALPHA_AND_THE_READINGS_OF_THE_MASS_CHAIN__THE_LIST_IS_NOT_CLOSED__")
sub(R, "INPUT/ONTO as quatro leituras, que entram como definicao; DECLARADO os recibos da gerencia (pinados por sha256)", "INPUT/ONTO as leituras da cadeia da massa, que entram como definicao ou identificacao, em lista que nao e' fechada; DECLARADO os recibos da gerencia (pinados por sha256)")
sub(R, '"fontes": [CHAVE_RECIBO_NOMEACAO, CHAVE_RECIBO_ERRATA, CHAVE_RECIBO_IDENTIDADE, CHAVE_RECIBO_OBSERVADOR], "verbatins": [CH_DE(N_NOMES),', '"fontes": [CHAVE_RECIBO_NOMEACAO, CHAVE_RECIBO_ERRATA, CHAVE_RECIBO_ERRATA_R2, CHAVE_RECIBO_IDENTIDADE, CHAVE_RECIBO_OBSERVADOR], "verbatins": [CH_DE(N_NOMES),')
sub(R, '"[INPUT/ONTO] as quatro leituras entram como DEFINICAO, nao como teorema: " + ', '"[INPUT/ONTO] as leituras da cadeia da massa entram como definicao ou identificacao, nao como teorema, e a lista NAO e\' fechada: " + ')
sub(R, '''"[INPUT/KNOWN] entram ainda, como dados do sistema que le e definicao conhecida: " + "; ".join(DL.DADOS_DO_SISTEMA),''', '''"[INPUT/KNOWN] entram ainda: " + "; ".join(DL.DADOS_DO_SISTEMA),''')
sub(R, "um Um posto (umPosto), uma alfa medida (TGLCoupling.alpha) e as leituras do operador (massaDerivada; transicaoDerivada, onde o angulo e' escrito; tonica; pagamentoComoCurvatura); dadas essas entradas, a FORMA e' teorema\",",
    "um Um posto (umPosto), uma alfa medida (TGLCoupling.alpha) e as leituras da cadeia da massa (massaDerivada; transicaoDerivada, onde o angulo e' escrito; tonica; pagamentoComoCurvatura; meioTom; omegaSq; a identificacao em the_mass_is_the_zero_point; a hipotese de area_por_volta_da_massa_inscrita; foton_sem_massa; a taxa do disco; a lista nao e' fechada); dadas essas entradas, a FORMA e' teorema\",")
sub(R, '''"o_que_entra": {"dois_postos": list(DL.POSTOS_E_MEDIDA), "quatro_leituras": list(DL.LEITURAS_DEFINICOES), "dados_do_sistema_que_le": list(DL.DADOS_DO_SISTEMA)},''', '''"o_que_entra": {"dois_postos": list(DL.POSTOS_E_MEDIDA), "leituras_da_cadeia_da_massa": list(DL.LEITURAS_DEFINICOES), "lista_de_leituras_fechada": DL.LISTA_DE_LEITURAS_FECHADA, "dados_do_sistema_que_le": list(DL.DADOS_DO_SISTEMA)},''')

# ===================================================================================================== runtime_v405.py
T = "runtime_v405.py"
sub(T, "# os campos fechados: a face absoluta (gibbs(1/n)((1/2)(1 + Gamma)) com Tr Gamma = 0) pesa 1/2 em dimensao 2, 3, 4 e 5, para uma graduacao de paridade fora da base canonica;", "# os campos fechados: a face absoluta (gibbs(1/n)((1/2)(1 + Gamma)) com Tr Gamma = 0) pesa 1/2 em dimensao 2, 3, 4 e 5, para Gamma = diag(n-1, -1, ..., -1) (diagonal, de traco nulo; so' o traco importa aqui; para n >= 3 ela nao e' involutiva);")
sub(T, "# Gamma = diag(n - 1, -1, ..., -1): traco zero, autovalores +-, uma graduacao de paridade", "# Gamma = diag(n - 1, -1, ..., -1): traco zero")
sub(T, "        Q_ = _v405_rot_projector(n_, 1, 0.3); _ = Q_                                 # (a rotacao so' serve de controle de que a base nao importa: o traco e' invariante)\n", "")
sub(T, "sem o abismo a fusao le como pressuposta; o terminal le 1 (omega(I) = 1 do core). Devolve", "sem o abismo a fusao le como pressuposta; o terminal le 1 e o abismo le 0 na leitura binaria; ao lado, o polo omega do par le 1 na identidade (homonimo: omega(I) = 1 do core). Devolve")
sub(T, '''    ck_("o6", "★★★ the_terminal_reads_one (= omega_of_one): o terminal le 1 na identidade -- omega(I) = 1 no core deste rito (o Um posto, o echo 1) -- e beta = alfa x raiz de e no runtime",
        isinstance(om_, (int, float)) and float(om_) == 1.0 and 0.0 < beta_ < 1.0, [om_])
''', '''    ck_("o6", "★★★ the_fixed_points_read_one_and_zero: na leitura binaria, o terminal da cascata (o nivel gravidade) le 1 e o abismo le 0: e' este o teorema da frase o terminal le 1",
        leitura_(("nivel", "gravidade")) is True and leitura_(("abismo", None)) is False, [leitura_(("nivel", "gravidade")), leitura_(("abismo", None))])
    ck_("o7", "★★ the_omega_pole_reads_one (= omega_of_one): ao lado, o polo omega do par le 1 na identidade -- omega(I) = 1 no core deste rito (o Um posto, o echo 1) -- e beta = alfa x raiz de e no runtime; HOMONIMO, dito: ali a palavra terminal nomeia o polo do par alfa/omega, aqui o nivel gravidade da cascata; nenhum termo liga os dois, e liga-los e' leitura [ONTO] do operador",
        isinstance(om_, (int, float)) and float(om_) == 1.0 and 0.0 < beta_ < 1.0, [om_])
''')
sub(T, '''"""v405 -- a mecanica do DISCO DE EULER (unidades do disco: K, tau e E0 sao DADOS do disco, nao hipoteses sobre a teoria; beta vem do acoplamento): a perda e' constante e e' a lei canonica (Gamma_Omega.E = (1/2).beta.tau.K); E(t) = E0 - c.t para em t0 = E0/c;
    antes da parada Omega^2 = K/E nao tem cota (a inscricao do zero no infinito); com taxa constante''', '''"""v405 -- a mecanica do DISCO DE EULER (unidades do disco: K, tau e E0 sao DADOS do disco, nao hipoteses sobre a teoria; beta vem do acoplamento): E(t) = E0 - c.t e Omega^2 = K/E sao DEFINICOES; Gamma_Omega.E = (1/2).beta.tau.K = c; a E definida satisfaz dE/dt = -Gamma_Omega.E e zera em t0 = E0/c;
    antes da parada Omega^2 nao tem cota (o operador le isso como a inscricao do zero no infinito [ONTO]); com taxa constante''')
sub(T, '''ck_("k1", "★★★ c_pos, E_linear, stops_in_finite_time e t0_pos: a perda c = (1/2).beta.tau.K e' positiva, a energia E(t) = E0 - c.t e' linear e o disco PARA em tempo finito t0 = E0/c (|E(t0)| <= 1e-12): o zero e' alcancado",''',
    '''ck_("k1", "★★★ c_pos, E_linear, stops_in_finite_time e t0_pos: c = (1/2).beta.tau.K e' positiva; a energia DEFINIDA E(t) = E0 - c.t zera em tempo finito t0 = E0/c (|E(t0)| <= 1e-12)",''')
sub(T, '''Gamma_Omega.E = c (|erro| <= 1e-12 relativo) e Omega^2.E = K: com o invariante do disco, a lei Gamma proporcional a omega^2 da TGL faz a energia cair a taxa constante",''',
    '''Gamma_Omega.E = c (|erro| <= 1e-12 relativo) e Omega^2.E = K: com o invariante do disco, o produto Gamma.E da lei Gamma proporcional a omega^2 e' constante",''')
sub(T, '''ck_("k3", "★★★ frequency_squared_unbounded_at_the_stop (A INSCRICAO DO ZERO NO INFINITO): para toda cota B (1e3, 1e6, 1e9) existe t < t0 com Omega^2(t) > B (t = (E0 - eps)/c, eps = min(E0/2, K/(2(B+1))), a testemunha da prova com folga numerica): o zero so' se inscreve com frequencia infinita",''',
    '''ck_("k3", "★★★ frequency_squared_unbounded_at_the_stop (Omega^2 SEM COTA): para toda cota B (1e3, 1e6, 1e9) existe t < t0 com Omega^2(t) > B (t = (E0 - eps)/c, eps = min(E0/2, K/(2(B+1))), a testemunha da prova com folga numerica); [ONTO] o operador le isso como a inscricao do zero absoluto no infinito",''')
sub(T, '''ck_("k5", "★★★ the_residual_resonance_iff (A RESSONANCIA QUE PERMANECE): o corte quantico hbar^2.Omega^2 = E^2 acontece exatamente quando E^3 = hbar^2.K''', '''ck_("k5", "★★ the_residual_resonance_iff (O CORTE, algebra): o corte hbar^2.Omega^2 = E^2 acontece exatamente quando E^3 = hbar^2.K''')
sub(T, '''    vals_ = {"beta": beta_, "disco_modelo": {"K": K_, "tau": tau_, "E0": E0_, "c": cc_, "t0": t0_},''', '''    h_ = t0_ * 1e-3
    fluxo_ = [(t_, (E_(t_ + h_) - E_(t_ - h_)) / (2.0 * h_), -(gam_(t_) * E_(t_))) for t_ in ts_[1:4]]
    ck_("k7", "★★★ the_flow_is_the_canonical_law: antes da parada, dE/dt = -Gamma_Omega.E: a derivada centrada da E definida coincide com -Gamma.E em tres instantes (|erro| <= 1e-9 relativo): a E definida e' uma solucao do fluxo; ler a taxa de dephasing Gamma como taxa de perda de energia e' entrada [INPUT/ONTO]",
        all(_v405_rel(d_, g_) <= 1e-9 for _, d_, g_ in fluxo_), [[round(t_, 6), d_, g_] for t_, d_, g_ in fluxo_])
    vals_ = {"beta": beta_, "disco_modelo": {"K": K_, "tau": tau_, "E0": E0_, "c": cc_, "t0": t0_},''')
sub(T, "-- o pagamento se consuma so' no limite; o que permanece e' o ponto zero\",", "-- o pagamento se consuma so' no limite; [ONTO] o operador le o que permanece como o ponto zero: nenhum teorema liga os dois\",")
sub(T, '''"para kappa em {0,5; 1; 2; 10} e g em {0,25; 1; 3}: o emprestimo nao se quita em volta nenhuma",''', '''"para kappa em {0,5; 1; 2; 10} e g em {0,25; 1; 3}: uma volta nao quita; para qualquer tempo finito o termo do kernel e' the_charge_never_completes",''')
sub(T, '''    du_ = [forma_(57.0) - forma_(57.0) for _u in (0.5, 1.0, 2.0)]\n''', '')
sub(T, '''forma_.__code__.co_varnames == ("R_",) and du_ == [0.0, 0.0, 0.0] and _v405_rel(beta_, medida_["beta_runtime"])''', '''forma_.__code__.co_varnames == ("R_",) and _v405_rel(beta_, medida_["beta_runtime"])''')

# ===================================================================================================== gerar_candidato_v405.py
G = "gerar_candidato_v405.py"
sub(G, "[INPUT/ONTO] as quatro leituras, como definição: `massaDerivada`; o estado inscrito lido em θ = π/4 (em `transicaoDerivada` o ângulo é escrito; o valor coincide com o peso da face absoluta: coincidência de valor, não ponte); a tônica (β/α)·u (E₀ = u é identidade algébrica, que não fixa u: o no-go não cai, localiza-se no Um posto); R = β·u² (`pagamentoComoCurvatura`). '",
    "[INPUT/ONTO] as leituras da cadeia da massa, como definição ou identificação, em lista que não é fechada; as centrais: `massaDerivada`; o estado inscrito lido em θ = π/4 (em `transicaoDerivada` o ângulo é escrito; o valor coincide com o peso da face absoluta: coincidência de valor, não ponte); a tônica (β/α)·u (E₀ = u é identidade algébrica, que não fixa u: o no-go não cai, localiza-se no Um posto); R = β·u² (`pagamentoComoCurvatura`). '")

# ===================================================================================================== grava (tudo ou nada)
for arq, novo in NOVOS.items():
    compile(novo, arq, "exec") if arq.endswith(".py") else None
for arq, novo in NOVOS.items():
    p = os.path.join(HERE, arq); b = open(p, "rb").read()
    bak = p + ".bak_" + TS + "_R2"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
    t = p + ".tmp_R2"; open(t, "wb").write(novo.encode("utf-8")); assert os.path.getsize(t) == len(novo.encode("utf-8")) and os.path.getsize(t) > 1000
    os.replace(t, p)
    print(arq, len(b), "->", len(novo.encode("utf-8")))
print("ok, backups .bak_%s_R2" % TS)
