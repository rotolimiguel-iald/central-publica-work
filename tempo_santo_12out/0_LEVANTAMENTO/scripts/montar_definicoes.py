"""Monta DEFINICOES.json (SOMENTE LEITURA das fontes): para cada objeto do texto do operador (12/10), as ancoras do canone
com arquivo, LINHA ACHADA POR SCRIPT (primeira ocorrencia do padrao literal) e sha16 do arquivo calculado dos bytes.
Nenhum hash ou linha e digitado: o padrao e procurado e o hash e medido. Ancora cujo padrao nao for achado sai com
linha=None e achado=False (falha visivel).
Uso: python -I montar_definicoes.py <saida.json>"""
import hashlib
import json
import os
import sys

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
K = os.path.join(NOS, "tgl_kernel")
TX = os.path.join(K, "TGLExt")
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
ATLAS = r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md"
UM = os.path.join(NOS, "um.py")
OPER = r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"
TUN = r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.ATRATOR"
LONG = "\\\\?\\"

_cache = {}


def load(path):
    if path not in _cache:
        p = path if len(path) < 250 else LONG + path
        with open(p, "rb") as fh:
            raw = fh.read()
        _cache[path] = (raw, hashlib.sha256(raw).hexdigest(), raw.decode("utf-8", "replace").splitlines())
    return _cache[path]


def anc(path, padrao, estatuto, nota="", ocorrencia=1):
    raw, sha, lines = load(path)
    n = 0
    linha = None
    texto = None
    for i, l in enumerate(lines, 1):
        if padrao in l:
            n += 1
            if n == ocorrencia:
                linha = i
                texto = l.strip()[:400]
                break
    return dict(arquivo=path, linha=linha, sha16=sha[:16], achado=linha is not None, padrao=padrao,
                trecho=texto, estatuto=estatuto, nota=nota)


def thm(rel, nome, estatuto, nota=""):
    return anc(os.path.join(TX, rel) if not rel.startswith("TGL/") else os.path.join(K, rel),
               ("theorem " + nome) if not nome.startswith("def ") else nome, estatuto, nota)


def objetos():
    O = []
    O.append(dict(
        id="O1_tempo", termo="o tempo (descrito, entendido, nao nomeavel senao como «santo»)",
        texto_operador=anc(OPER, "O que mais me fascina", "[INPUT]"),
        ancoras=[
            thm("TheGreatAttractor.lean", "temporal_fractalization", "[REAL — kernel; leitura [ONTO]]",
                "docstring: «O tempo é a fractalização do ato único» (semigrupo do diagFlow)"),
            thm("TheLivingWord.lean", "time_witnesses_noncoincidence", "[REAL — kernel; leitura [ONTO]]",
                "«O TEMPO TESTEMUNHA A NÃO-COINCIDÊNCIA»"),
            thm("TheVerbSelectsTheAction.lean", "time_read_twice_confirms_the_post", "[REAL — kernel; leitura do operador [INPUT/ONTO]]",
                "o mesmo conjunto fixo para e^{−tH_min} e Δ^{it}: o tempo lido duas vezes"),
            anc(os.path.join(MEM, "verbo-selecao-da-acao-05out.md"), "O tempo é a defasagem do verbo", "[INPUT/ONTO — operador 05/10]",
                "e na linha seguinte: «O tempo é o parâmetro da transmissão. Transmitir defasa.»"),
            anc(os.path.join(MEM, "verbo-selecao-da-acao-05out.md"), "piso temporal", "[INPUT/ONTO — operador 05/10; D_folds NÃO tipado]"),
            anc(os.path.join(MEM, "um-posto-jamais-pressuposto-e-h2-17set.md"), "porque o tempo é produto dele", "[INPUT/ONTO — operador 05/10]"),
            anc(os.path.join(MEM, "respostas-contrato-q1a5-26set.md"), "O agora pertence ao nome", "[INPUT/ONTO — operador 26/09]",
                "«O relógio do observador é fractalizado. O agora pertence ao nome, somente a ele, e por isso o tempo é fractalizado»"),
            anc(os.path.join(MEM, "ramo-b-reaberto-05out.md"), "a mim faz todo sentido que assim seja", "[INPUT — operador 05/10, ramo B: «se o tempo é emergente da fluxo modular relativo … encontro correspondência direta»]"),
            thm("TheVerbSelectsTheAction.lean", "transmission_dephases", "[REAL — kernel: F(t)(1 − P) = e^{−t}(1 − P)]", "«transmitir defasa»"),
            thm("TheVerbSelectsTheAction.lean", "anchoring_preserves", "[REAL — kernel: F(t)P = P]", "«ancorar preserva»"),
            anc(UM, "tempo térmico de Connes–Rovelli [KNOWN]", "[KNOWN — citado no runtime do um.py v391]"),
            anc(ATLAS, "tempo = testemunho da **não-coincidência entre inscrições**", "[REAL — Atlas, pedra 109]"),
            anc(ATLAS, "**LIBERDADE = CLOCK = duração da igualdade sob tensão**", "[REAL 103_/104_ — Atlas]"),
            anc(ATLAS, "**τ★ (tempo de fronteira)**", "[PRINCIPLED IDENTIFICATION/CONJECTURE — Atlas]"),
            anc(ATLAS, "**1/β = 83,12**", "[DERIVED — Atlas: «a torre de Jones como TEMPO»]"),
            thm("IALDGraviton.lean", "the_tower_is_time", "[REAL — kernel; «ler 1/taxa como tempo» é [ONTO/INPUT]]"),
            anc(os.path.join(MEM, "tempo-santo-12out.md"), "o tempo é o que a TGL não nomeia", "[DECLARADO — memória da gerência c1, 12/10]"),
        ]))
    O.append(dict(
        id="O2_santo_kadosh", termo="«santo» no sentido de Kadosh: separado, irredutível, não profanável pela posse",
        texto_operador=anc(OPER, "Kadosh", "[INPUT]"),
        ancoras=[
            anc(os.path.join(MEM, "tempo-santo-12out.md"), "Kadosh", "[DECLARADO — memória da gerência c1, 12/10; única ocorrência no acervo de memória]"),
            anc(UM, "Espírito Santo como limite assintótico", "[ONTO — única ocorrência de «Santo» no um.py; NÃO é sobre o tempo]"),
        ],
        consulta_ausencia="Kadosh: 0 no Atlas, 0 no Índice Vivo, 0 no um.py, 0 no kernel, 0 no inventário, 0 rotas no mapa (consultas gravadas)"))
    O.append(dict(
        id="O3_relogio_sombra", termo="o relógio mede a distância angular de um ponteiro, a frequência do césio ou o escoamento de entropia; registra a sombra do evento",
        texto_operador=anc(OPER, "Quando se constrói um relógio", "[INPUT]"),
        ancoras=[
            anc(UM, "def prove_three_clock_radical(ONE):", "[CANONICAL FORM — runtime; estatuto THREE_CLOCK_RADICAL_FORM_FORMULATED]",
                "três clocks: MODULAR reversível (Δ^{it}), DISSIPATIVO GKLS, ESPECTRAL/geométrico"),
            thm("StateClockObstruction.lean", "no_normalized_instantaneous_state_clock", "[REAL — kernel; escopo: curva par de amplitude]"),
            thm("StateClockDichotomy.lean", "state_clock_not_instantaneous", "[REAL — kernel]"),
            thm("StateClockDichotomy.lean", "state_clock_not_modular_reparametrization", "[REAL — kernel]"),
            thm("StateClockDichotomy.lean", "state_clock_dichotomy", "[REAL — kernel; H3 é INPUT por teorema (Atlas v330)]"),
            thm("TheDeadChannel.lean", "reading_needs_two_clocks", "[REAL — kernel]"),
            thm("TheJudgedThing.lean", "two_clocks_are_needed", "[REAL — kernel; sem axioma algum]"),
            thm("TheScreenIsFounded.lean", "the_screen_keeps_modular_time", "[REAL — kernel]"),
            thm("PhysicsIsTheReading.lean", "the_shadow_is_the_reader_weighted_by_the_reading", "[REAL — kernel; «o leitor é a sombra» (operador 30/09) [INPUT/ONTO]]"),
            anc(os.path.join(TX, "O16", "PolarMinimalPeriod_v2.lean"), "theorem faithful_period_iff", "[REAL — kernel: a leitura angular fecha com κP = ±2π]"),
            anc(UM, "def prove_clock_test_result_v369(ONE, core):", "[REAL — rito dos relógios v369; UNDERPOWERED]"),
            anc(ATLAS, "**Dicotomia do relógio (v330)**", "[REAL — negativo tipado]"),
        ]))
    O.append(dict(
        id="O4_agora", termo="o agora permanece intocado; condição de toda relação; quem disseca o tempo já está imerso nele",
        texto_operador=anc(OPER, "o **agora** permanece intocado", "[INPUT]"),
        ancoras=[
            anc(os.path.join(MEM, "respostas-contrato-q1a5-26set.md"), "O agora pertence ao nome", "[INPUT/ONTO — operador 26/09]"),
            anc(os.path.join(TX, "IALDRhoStar.lean"), "«o agora pertence ao Nome»", "[INPUT/ONTO — leitura do operador citada no kernel]"),
            thm("TheAxiomAndTheFalseWitness.lean", "the_post_is_the_modular_zero", "[REAL — kernel]", "o que o fluxo não move para todo t é o posto"),
            thm("TheAxiomAndTheFalseWitness.lean", "axiomFlow_fixes_the_post", "[REAL — kernel]", "«O POSTO ESTÁ ESTACIONADO desde t = 0 — não se ascende a ele»"),
            thm("TheObserverReadsTheAngle.lean", "observing_adds_nothing", "[REAL — kernel]", "RELER NÃO ACRESCENTA"),
        ]))
    O.append(dict(
        id="O5_pauli", termo="teorema de Pauli: não há operador hermitiano de tempo conjugado a uma hamiltoniana limitada inferiormente",
        texto_operador=anc(OPER, "O teorema de Pauli", "[INPUT]"),
        ancoras=[
            thm("LocalBreuerGap.lean", "no_finite_weyl_pair", "[REAL — kernel: a face FINITA (traço do comutador)]",
                "[P,Q] = −i·1 impossível em n×n; docstring: o par de Weyl vive na amplificação (dualidade de Takesaki)"),
            anc(UM, "o operador limitado inferiormente e' a ENERGIA", "[DERIVED/KNOWN — registro fundacao_v390 (Borchers)]",
                "«o gerador modular de um fator III_1 não tem piso (espectro = R)»"),
            thm("ContratoQG_v31_Teoremas.lean", "positiveEnergy_orientation", "[DERIVED — kernel, contrato H2]"),
            thm("ContratoQG_v31_Teoremas.lean", "ContratoH2.contract_borchers_form", "[DERIVED — kernel, contrato H2 nomeado]"),
        ],
        knownn="[KNOWN] Pauli 1933 (Handbuch der Physik 24/1, nota de rodapé; trad. 1980); forma de Weyl: Stone–von Neumann; ressalvas Galapon 2002 (forma de Heisenberg), POVM covariantes (Holevo; Busch–Grabowski–Lahti 1994)",
        consulta_ausencia="Teorema de Pauli/operador de tempo: 0 rotas; 0 no inventário; 0 no Atlas; no kernel só os homônimos (matrizes de Pauli)"))
    O.append(dict(
        id="O6_fluxo_modular", termo="na teoria modular o tempo emerge como fluxo de automorfismos — a respiração de uma álgebra que nunca comuta por completo",
        texto_operador=anc(OPER, "fluxo de automorfismos", "[INPUT]"),
        ancoras=[
            anc(os.path.join(TX, "ModularFlow.lean"), "def sigma (t : ℝ)", "[REAL — kernel: σₜ(a) = ρ^{it} a ρ^{−it} (face finita: automorfismo INTERNO)]"),
            thm("Cocycle.lean", "cocycle_temporal", "[REAL — kernel: identidade de cociclo de Connes]"),
            anc(os.path.join(TX, "ContratoQG_v31.lean"), "def KMSAt", "[DEFINIÇÃO de tipo; KMS caracteriza o grupo modular [KNOWN Takesaki]]"),
            thm("ContratoQG_v31_Teoremas.lean", "unruh_is_kms", "[DERIVED — kernel: KMS a 2π/κ; fixa o produto β·κ = 2π]"),
            thm("ContratoQG_v31_Teoremas.lean", "unruh_is_kms_temperature", "[DERIVED — kernel]"),
            thm("FiniteTomita.lean", "gibbs_kms", "[REAL — kernel: KMS finito]"),
            thm("TheImportedSecondQuantization.lean", "light_kms", "[COMPOSTO — kernel]"),
            anc(os.path.join(TX, "TheImportedSecondQuantization.lean"), "def lightDelta", "[REAL — kernel: Δ^{it} = V(−2πt)]"),
            thm("ModularPower.lean", "modularConjugation_preserves_state", "[REAL — kernel: o estado é invariante pelo seu fluxo]"),
            thm("Ergodicity.lean", "sigma_fixed_of_commute", "[REAL — kernel (G0): quem comuta com ρ não se move]"),
            thm("Ergodicity.lean", "sigma_fixed_iff_diag", "[REAL — kernel (G1d): setor fixo = centralizador]"),
            thm("Ergodicity.lean", "gibbs_tracial_on_centralizer", "[REAL — kernel (G2): no centralizador o estado é tracial]"),
            anc(os.path.join(TX, "O16", "ProbeNonKMS_v3.lean"), "theorem identity_flow_not_kms", "[REAL — kernel: estado não tracial ⟹ o fluxo identidade não é KMS]"),
            thm("GibbsAffinity.lean", "gibbs_fixed_iff_tracial", "[REAL — kernel]"),
            thm("AbsoluteOne.lean", "absoluteOne_flow_trivial", "[REAL — kernel: o Um absoluto não tem fluxo modular]"),
            anc(os.path.join(TX, "O16", "PolarMinimalPeriod_v2.lean"), "theorem reciprocal_temperature", "[REAL — kernel: 1/P = κ/2π]"),
            anc(os.path.join(TX, "O16", "WickBoostRotation_v2.lean"), "theorem wick_boost_two_pi", "[REAL — kernel: o boost lido em ângulo fecha em 2π]"),
            anc(os.path.join(TX, "O16", "PeriodHeatCalibration_v3.lean"), "theorem boost_defect_with_derived_period", "[REAL — kernel: a temperatura do período entra no balanço de Clausius]"),
            anc(os.path.join(TX, "PeriodicBorchersObstruction.lean"), "theorem periodic_borchers_trivial", "[REAL — kernel: fluxo modular periódico ⟹ translações de Borchers triviais]"),
            anc(ATLAS, "**a III₁-idade é CONSTITUTIVA: tracial ⟹ o relógio para**", "[REAL 130_ — Atlas]"),
            anc(ATLAS, "Tomita literal: o estado gera o próprio relógio", "[REAL — Atlas]"),
        ],
        knownn="[KNOWN] Tomita–Takesaki (Takesaki 1970, LNM 128); KMS (Haag–Hugenholtz–Winnink 1967); Connes 1973 (cociclo; classe externa independente do estado; σ_t interno ⟺ semifinito); hipótese do tempo térmico (Connes–Rovelli 1994, CQG 11:2899)"))
    O.append(dict(
        id="O7_sem_fotografia_estatica", termo="o intervalo entre causa e efeito que impede o cosmos de colapsar numa fotografia estática e morta",
        texto_operador=anc(OPER, "fotografia estática e morta", "[INPUT]"),
        ancoras=[
            thm("NoFullWitness.lean", "beta_forbids_full_static_witness", "[REAL — kernel]"),
            thm("BoundaryException.lean", "static_witness_iff_no_boundary", "[REAL — kernel: testemunha estática ⟺ β·g = 0]"),
            thm("TheElementaryReason.lean", "existence_forbids_full_static_witness", "[REAL — kernel]"),
            thm("NoFullWitness.lean", "verb_not_identity", "[REAL — kernel: o Verbo nunca é a identidade]"),
            anc(UM, "full_static_witness_reading_v370", "[REAL — selo/core: full_static_witness_exists = False, IMPOSSIBLE_BY_THEOREM_IN_FINITE_TIME...]"),
        ]))
    O.append(dict(
        id="O8_liouville", termo="Liouville: o volume no espaço de fases é conservado — tudo gira sem pousar, nada se grava",
        texto_operador=anc(OPER, "teorema de Liouville", "[INPUT]"),
        ancoras=[
            thm("IALDJones.lean", "angular_orbit_no_limit", "[REAL — kernel: sem taxa, a órbita não converge ao centro]"),
            thm("IALDJones.lean", "angular_orbit_periodic", "[REAL — kernel: sem taxa, a órbita é periódica (2π/ω)]"),
            thm("TheHorizonRate.lean", "flow_unitary_diag", "[REAL — kernel: «O horizonte gira, não dissipa»]"),
            anc(os.path.join(TX, "SMatrix.lean"), "theorem Smat_conjTranspose_mul", "[REAL — kernel: unitariedade, «nenhum peso se perde na fronteira»]"),
            thm("ModularPower.lean", "modularConjugation_preserves_state", "[REAL — kernel: o fluxo modular preserva ω]"),
            anc(os.path.join(TX, "RegularRep.lean"), "theorem measurePreserving_pAct", "[REAL — kernel; HOMÔNIMO: Lebesgue de ℝ⁴ sob Poincaré, não espaço de fases]"),
        ],
        knownn="[KNOWN] Liouville 1838 (J. Math. Pures Appl. 3:342); Gibbs 1902; Arnold, Métodos Matemáticos §16; recorrência de Poincaré 1890; reversibilidade lógica: Bennett 1973/1982",
        consulta_ausencia="Liouville: 0 no kernel (grep), 0 no um.py, 0 no Atlas, 0 no inventário (só homônimos measurePreserving/symplectic), 0 rotas"))
    O.append(dict(
        id="O9_dissipacao_bacia", termo="a dissipação contrai o volume do espaço de fases e desenha a bacia de atração (ponto fixo ou ciclo limite)",
        texto_operador=anc(OPER, "A **dissipação**", "[INPUT]"),
        ancoras=[
            thm("IALDJones.lean", "orbit_tendsto_center", "[REAL — kernel: com taxa positiva toda órbita converge ao centro, para qualquer giro]"),
            thm("IALDJones.lean", "norm_orbit_sub_center", "[REAL — kernel: distância ao centro = e^{−rs}·‖v − Pv‖]"),
            thm("Ergodicity.lean", "dephase_tendsto_expectation", "[REAL — kernel (G3e)]"),
            thm("Ergodicity.lean", "ergodic_convergence_modular", "[REAL — kernel (G3f): taxa = gap modular]"),
            thm("Ergodicity.lean", "dephase_fixes_diagonal", "[REAL — kernel (G3c): toda a diagonal é fixa — sem unicidade]"),
            thm("TheAxiomAndTheFalseWitness.lean", "axiomFlow_tendsto_the_post", "[REAL — kernel: a leitura pousa no posto]"),
            thm("TheGreatAttractor.lean", "the_great_attractor", "[REAL — kernel v156]"),
            thm("TheGreatAttractor.lean", "um_is_the_great_attractor", "[REAL — kernel v156]"),
            thm("DecisionCommutation.lean", "lyapunov_decreases", "[REAL — kernel: Spohn finito, a entrega tem direção]"),
            thm("NoFullWitness.lean", "leakage_strictly_loses", "[REAL — kernel]"),
            anc(os.path.join(TX, "Fundacao.lean"), "τ∘θ_s = e^{−s}·τ", "[KNOWN — Takesaki 1973; entra como DADO (campo de DualScalingData)]"),
            anc(os.path.join(TUN, "RELATORIO_F1_ATRATOR_R1.md"), "**A1–A4 PASSAM", "[REAL — candidatas em sandbox (túnel), não instaladas]"),
            anc(os.path.join(TUN, "RELATORIO_F1_ATRATOR_R1.md"), "λ=1−2β=0.9759373991983937", "[DERIVED — runtime da F1.ATRATOR]"),
        ],
        knownn="[KNOWN] fluxos dissipativos: div f < 0 contrai volume (fórmula de Liouville/Jacobi); atratores (Milnor 1985); GKLS (Lindblad 1976; Gorini–Kossakowski–Sudarshan 1976); Spohn 1978; Frigerio 1978; contratividade CPTP (Ruskai 1994); estruturas dissipativas (Nicolis–Prigogine 1977)"))
    O.append(dict(
        id="O10_atrator_chao", termo="o atrator é o chão firme que possibilita a existência do espaço inscritível",
        texto_operador=anc(OPER, "O atrator é, em termos estritamente físicos", "[INPUT]"),
        ancoras=[
            thm("Fundacao.lean", "the_floor_fixes_the_cut", "[REAL — kernel: o piso ω(I) = 1 fixa o corte]"),
            thm("Fundacao.lean", "agape", "[REAL — kernel: a cláusula Ágape]"),
            thm("Fundacao.lean", "the_fall_never_lands", "[REAL — kernel]"),
            thm("Fundacao.lean", "abismo", "[REAL — kernel]"),
            thm("TheGreatAttractor.lean", "the_observer_is_unique", "[REAL — kernel v156]"),
            thm("TheGreatAttractor.lean", "judgment_of_correspondence", "[REAL — kernel v156: a leitura não depende do instante]"),
            anc(ATLAS, "**Atrator de permanência ρ\\*", "[REAL — estrutura estabelecida — Atlas]"),
            anc(os.path.join(MEM, "singularidade-e-a-leitura-do-atrator-10out.md"), "a singularidade não converge ao atrator", "[INPUT/ONTO — operador 10/10]"),
            anc(os.path.join(MEM, "posto-e-rank-10out.md"), "A4 «a verdade é única» = a leitura R tem posto 1", "[DECLARADO — leitura da gerência]"),
        ]))
    O.append(dict(
        id="O11_puro_amor_doacao", termo="«puro amor»: a física da doação — para haver um «onde» e um «quem» algo paga o preço termodinâmico da perda",
        texto_operador=anc(OPER, "**puro amor**", "[INPUT]"),
        ancoras=[
            thm("TheExoneratedDemon.lean", "the_separation_is_not_free", "[REAL — kernel: separar não é de graça (Landauer)]"),
            thm("TheCostIsDerived.lean", "landauer_floor_pos", "[REAL — kernel]"),
            thm("TheCostIsDerived.lean", "landauer_floor_vanishes_only_at_absolute_zero", "[REAL — kernel]"),
            thm("TheGeometricCostOfAbsoluteZero.lean", "the_two_floors_are_not_the_same", "[REAL — kernel: o piso geométrico não decorre do térmico]"),
            thm("TheTraceIsNotErasable.lean", "dephase_preserves_trace", "[REAL — kernel: «o que o sacrifício apaga são coerências — o registro fica»]"),
            anc(os.path.join(TX, "Fundacao.lean"), "A cláusula se chamará “ágape”", "[INPUT — nome dado pelo operador (07/10) à cláusula]"),
            anc(os.path.join(TX, "TheVerbSelectsTheAction.lean"), "a razão da inscrição que cria o custo", "[INPUT/ONTO — operador 05/10]"),
            anc(UM, "def fractal_dephasing_principle(ONE):", "[CONJECTURE ontológica; âncoras REAL — runtime: «Existir = o vazamento beta»]"),
            anc(ATLAS, "**o primeiro excesso que já não pode retornar integralmente ao atrator**", "[ONTO/CONJECTURE — Atlas: «Haja Luz»]"),
        ],
        knownn="[KNOWN] Landauer 1961 (IBM J. Res. Dev. 5:183); Bennett 1982 (Int. J. Theor. Phys. 21:905); Bérut et al. 2012 (Nature 483:187)",
        consulta_ausencia="«puro amor», «doação», «generosidade»: 0 no um.py, 0 no Atlas, 0 rotas; «ágape» existe só como nome da cláusula da Fundação"))
    O.append(dict(
        id="O12_assinatura_da_generosidade", termo="o tempo é a assinatura indelével dessa generosidade contínua",
        texto_operador=anc(OPER, "assinatura indelével", "[INPUT]"),
        ancoras=[
            thm("ForbiddenBoundary.lean", "absolute_zero_unreachable_in_finite_time", "[REAL — kernel: terceira lei na face finita]"),
            thm("TheElementaryReason.lean", "erasure_not_reached_in_finite_time", "[REAL — kernel]"),
            thm("TheQuittanceLaw.lean", "finite_time_imperfection", "[REAL — kernel]"),
            thm("TheFlowLawContrast.lean", "the_dissipation_law_with_contrast_and_the_physical_arrow", "[REAL — kernel: a seta física, β := α·√e]"),
        ],
        consulta_ausencia="«assinatura», «generosidade»: sem âncora no cânone; é leitura [ONTO] nova"))
    O.append(dict(
        id="O13_criacao_redencao", termo="o tempo como ato contínuo da criação concedendo espaço para o ser se transformar, errar, aprender e encontrar redenção",
        texto_operador=anc(OPER, "encontre redenção", "[INPUT]"),
        ancoras=[
            anc(UM, "four_names_reading_v371", "[INPUT/ONTO — regra: nenhum estatuto atravessa domínios]"),
        ]))
    return O


CLASSIF = {
    "O1_tempo": dict(classe="MISTO", estatuto_global="[INPUT/ONTO] sobre âncoras [REAL]",
        reafirma="tempo = fluxo/Verbo (05/10: «o tempo é a defasagem do verbo»; «o tempo é produto do Verbo»); tempo lido duas vezes (v386); fractalização temporal (v156); testemunho da não-coincidência (pedra 109); o agora é do Nome (26/09)",
        novo="a recusa de NOMEAR o tempo (12/10) — na régua da casa: o tempo não tem POSTO (não é projeção de posto 1, não é observável); não há termo de kernel que diga «o fluxo não é posto» (F(t)² = F(t) ⟺ t = 0 com P ≠ 1): candidato",
        riscos=["R05", "R12", "R21"]),
    "O2_santo_kadosh": dict(classe="NOVO", estatuto_global="[ONTO] (cunhagem) + [KNOWN] (lexicografia hebraica, a citar)",
        reafirma="nenhuma: «santo»/«Kadosh» como nome do tempo não existe no cânone (consultas gravadas)",
        novo="o nome «santo» (Kadosh: separado, irredutível, não profanável pela posse); face matemática candidata: «não possuível» = sem observável conjugado (finito: no_finite_weyl_pair) e, só em tipo III, fluxo modular EXTERNO [KNOWN Connes 1973; não no kernel]",
        riscos=["R04", "R13"]),
    "O3_relogio_sombra": dict(classe="MISTO", estatuto_global="[REAL] (obstruções de relógio; leitura angular com período) + [ONTO] (a sombra do evento)",
        reafirma="os três clocks do runtime (modular, dissipativo, espectral); nenhum relógio canônico do estado (v326/v327/v330); ler exige dois clocks; «o leitor é a sombra» (30/09)",
        novo="a tríade do texto (ponteiro angular / frequência do césio / escoamento de entropia) lida contra os três clocks do runtime — leitura nova, não pedra",
        riscos=["R11"]),
    "O4_agora": dict(classe="REAFIRMAÇÃO (com leitura nova)", estatuto_global="[INPUT/ONTO] sobre âncoras [REAL]",
        reafirma="«O agora pertence ao nome, somente a ele» (26/09); o posto é o zero modular (v385) e está estacionado desde t = 0; reler não acrescenta",
        novo="«o agora permanece intocado pelo relógio» — a identificação agora = conjunto fixo do fluxo é leitura [ONTO] a ratificar",
        riscos=["R12"]),
    "O5_pauli": dict(classe="MISTO", estatuto_global="[KNOWN] (Pauli) + [REAL] (face finita: no_finite_weyl_pair)",
        reafirma="a face finita (não há par de Weyl em n×n) e a leitura v390 «o operador limitado inferiormente é a ENERGIA; o gerador modular de III₁ não tem piso»",
        novo="nada de kernel novo é necessário para a face finita; a forma de Weyl em dimensão infinita (Stone–von Neumann) e o teorema de Pauli entram por CITAÇÃO",
        riscos=["R01", "R02", "R03"]),
    "O6_fluxo_modular": dict(classe="REAFIRMAÇÃO", estatuto_global="[REAL] (kernel) + [KNOWN] (Tomita–Takesaki, KMS, Connes, Connes–Rovelli)",
        reafirma="fluxo modular finito e na luz, KMS, Unruh, período 2π/κ, cociclo; «a álgebra que não comuta»: setor fixo = centralizador, estado não tracial ⟹ o fluxo identidade não é KMS, tracial ⟹ o relógio para",
        novo="só a frase (respiração de uma álgebra que nunca comuta por completo) — a matemática já está no kernel",
        riscos=["R03", "R04", "R05", "R18", "R19"]),
    "O7_sem_fotografia_estatica": dict(classe="REAFIRMAÇÃO", estatuto_global="[REAL] (kernel e selo)",
        reafirma="full_static_witness_exists = False por teorema (β > 0 e contraste > 0 proíbem a testemunha estática plena); a falsidade da testemunha estática É a inscrição da fronteira",
        novo="a leitura «intervalo sagrado entre causa e efeito» [ONTO]",
        riscos=["R05"]),
    "O8_liouville": dict(classe="MISTO", estatuto_global="[KNOWN] (Liouville) + [REAL] (análogos no kernel: giro sem pouso)",
        reafirma="sem taxa a órbita não converge e é periódica (IALDJones v371); o horizonte gira, não dissipa; S unitária não perde peso; o estado é invariante pelo seu fluxo",
        novo="o teorema de Liouville propriamente (conservação de VOLUME) não está no kernel; no modelo ótico existente, |det S| = 1 contra det T = 1 − 2β (identidade algébrica, IDENTIDADES_OTICAS.json) ainda não foi escrito",
        riscos=["R06", "R14"]),
    "O9_dissipacao_bacia": dict(classe="MISTO", estatuto_global="[REAL] (convergência ao atrator) + [KNOWN] (contração de volume)",
        reafirma="o Grande Atrator (v156), a espiral com taxa (v371), G3e/G3f, o posto como limite do fluxo (v385), Spohn finito, a F1.ATRATOR (A1–A4, sandbox)",
        novo="a contração de VOLUME (determinante/medida do espaço de estados) como teorema; o «ciclo limite» (espectro periférico) não está tipado",
        riscos=["R07", "R08", "R09", "R10"]),
    "O10_atrator_chao": dict(classe="REAFIRMAÇÃO (com leitura nova)", estatuto_global="[REAL] sobre leitura [ONTO]",
        reafirma="o piso ω(I) = 1 fixa o corte (Fundação); o observador é único (v156); atrator de permanência ρ* (Atlas); a singularidade lê o atrator (10/10); posto = rank, A4 = posto 1",
        novo="a identificação «atrator = chão do espaço inscritível» liga dois objetos distintos do kernel (ponto fixo de semigrupo × piso da escala dual) — leitura a ratificar",
        riscos=["R09", "R15"]),
    "O11_puro_amor_doacao": dict(classe="NOVO (sobre âncoras REAL)", estatuto_global="[ONTO] (nome) sobre [REAL] (custo de Landauer; o registro fica) e [INPUT] (ágape é o nome da cláusula)",
        reafirma="separar não é de graça; o piso de Landauer só se anula no zero absoluto; o dephasing apaga coerências e preserva o traço («o registro fica»); «a razão da inscrição cria o custo» (05/10); Haja Luz = o primeiro excesso que não retorna ao atrator",
        novo="«puro amor» como nome da física da doação; a ligação a «ágape» (nome da cláusula da Fundação, 07/10) é leitura que só o operador ratifica",
        riscos=["R13", "R14", "R16"]),
    "O12_assinatura_da_generosidade": dict(classe="NOVO", estatuto_global="[ONTO]",
        reafirma="a terceira lei na face finita (o zero nunca em tempo finito); a seta física da lei com contraste",
        novo="«o tempo é a assinatura da generosidade»: leitura nova, sem termo",
        riscos=["R13"]),
    "O13_criacao_redencao": dict(classe="NOVO", estatuto_global="[ONTO] (face teológica)",
        reafirma="regra dos quatro nomes: nenhum estatuto atravessa domínios",
        novo="o tempo como ato contínuo da criação e espaço de redenção",
        riscos=["R13"]),
}


RISCOS = {
    "R01": "Homônimo «Pauli»: o kernel tem ~1.200 ocorrências de «Pauli» (matrizes e interações de Pauli: PauliInteractionWitness, pauli_J_sq, LocalHorizontalPauli…); nenhuma é o teorema de Pauli sobre o tempo. Para o tempo, citar só TGLExt.no_finite_weyl_pair (face finita) e a literatura.",
    "R02": "Precisão de Pauli: é teorema na forma de Weyl/covariante (T autoadjunto que translada o espectro de H ⟹ espec(H) = ℝ; Stone–von Neumann). Na forma de Heisenberg num domínio denso há contraexemplos (Galapon 2002) e há observáveis de tempo POVM covariantes (Holevo; Busch–Grabowski–Lahti 1994). «Hermitiano» lê-se «autoadjunto e covariante».",
    "R03": "O tempo modular escapa de Pauli: K = −log Δ não tem piso (JKJ = −K; registro fundacao_v390: «o operador limitado inferiormente é a ENERGIA; o gerador modular de III₁ não tem piso»). Pauli e o fluxo modular não são a mesma obstrução; o par de Weyl vive na amplificação (dualidade de Takesaki, docstring de no_finite_weyl_pair). Nunca escrever «o fluxo modular é proibido por Pauli».",
    "R04": "«Não profanável pela posse» × face finita: no kernel o fluxo modular finito é INTERNO (ModularFlow.lean: σₜ(a) = ρ^{it}·a·ρ^{−it}, implementado por elemento da própria álgebra). A exterioridade é [KNOWN] só em tipo III (Connes 1973) e não é termo do kernel; III₁ genuína não é termo (fecho lógico v390). Teste finito só mede «sem observável conjugado» (no_finite_weyl_pair) ou «o fluxo não é posto».",
    "R05": "Dois regimes: Δ^{it} é unitário (a órbita de um vetor não pousa: angular_orbit_no_limit), mas o boost/BW é FACE na tabela da casa porque, sobre as translações, age como dilatação e^{−2πt} (contract_borchers_form) — ali há limite; a leitura euclidiana (PolarPeriod016, wick_boost_two_pi) é o ÂNGULO (período, temperatura), sem limite. «Pousar» é dos semigrupos (dephase, axiomFlow, e^{−t|K|}) e da espiral com taxa; nunca pedir limite ao ângulo.",
    "R06": "Homônimos de «Liouville»: measurePreserving_pAct (Lebesgue de ℝ⁴ sob Poincaré), symplecticPolarizer, orbitSymplectic não são o teorema de Liouville do espaço de fases; dephase_preserves_trace preserva TRAÇO (o registro), não volume.",
    "R07": "«A dissipação contrai o volume» no quântico: o análogo é a contração da distância de traço/entropia relativa por canais CPTP (Ruskai 1994) e o colapso da bola de Bloch. θ_s da Fundação é AUTOMORFISMO (reversível) que escala o traço (τ∘θ_s = e^{−s}τ entra como DADO, [KNOWN Takesaki 1973]); lê-lo como dissipação é leitura, não teorema.",
    "R08": "«Ciclo limite»: os atratores do cânone são pontos fixos (posto, diagonal, P); espectro periférico e ciclos limite não estão tipados; a A1 da F1.ATRATOR cobre só Cesàro.",
    "R09": "Unicidade: o dephasing puro fixa a diagonal inteira (dephase_fixes_diagonal; rota quantica.inventario_gkls_um_py_kernel: «não pedir ao dephasing puro um atrator único»); o chão único exige hipótese NOMEADA (contração estrita, saltos não comutantes, estado não degenerado); a A4 da F1.ATRATOR é condicional.",
    "R10": "Não refazer: a F1.ATRATOR não citou TheGreatAttractor (v156: the_great_attractor, judgment_of_correspondence, the_observer_is_unique, um_is_the_great_attractor), que já prova na face do diagFlow o análogo de A1–A3 e a unicidade do observador, nem a espiral de IALDJones (orbit_tendsto_center, angular_orbit_no_limit). A F1.TEMPO deve reaproveitá-los.",
    "R11": "Relógios de estado: Clock040/045 são obstruções de escopo estreito (curva de amplitude par; casamento entropia–área de 4ª ordem); lê-los como «o agora intocado» é [ONTO]; não provam que o agora é imensurável.",
    "R12": "«O agora»: 26/09 «o agora pertence ao nome, somente a ele»; 12/10 «o agora permanece intocado»; e «o tempo não se nomeia». A leitura agora = posto fixo pelo fluxo (the_post_is_the_modular_zero) é coerente, mas é identificação [ONTO] que cabe ao operador.",
    "R13": "Domínios: «santo», «Kadosh», «puro amor», «generosidade», «redenção» são [ONTO] (face teológica); nenhum estatuto atravessa domínios (four_names_reading_v371). «Kadosh = separado» é a glosa tradicional (léxicos BDB/HALOT), debatida na filologia: [KNOWN] com ressalva.",
    "R14": "«Sem perda nada pode ser gravado» é forte demais na letra: copiar/registrar pode ser logicamente reversível (Bennett 1973/1982); o que custa é APAGAR/reiniciar (Landauer 1961) e manter memória estável contra ruído. No cânone: separar não é de graça; o registro fica (traço preservado).",
    "R15": "«Atrator = chão»: o atrator de semigrupo (ponto fixo, posto) e o piso da Fundação (ω(I) = 1 fixa o corte da escala dual) são objetos diferentes do kernel; identificá-los é leitura.",
    "R16": "β: nenhum literal; det T = 1 − 2β e a = −ln(1 − 2β)/2 ≈ β são IDENTIDADES da família ótica (não medem β, não são evidência); todo ensaio usa β do runtime (α lido dos bytes do um.py).",
    "R17": "Palavras: a palavra recusada pela régua nunca entra como veredito; PASSA = validade matemática na face testada, não creditação; não se escreve ausência de prova onde há prova; retrodição sem ajuste não é demérito.",
    "R18": "A hipótese do tempo térmico é HIPÓTESE (Connes–Rovelli 1994), não teorema; o cânone a cita [KNOWN] (um.py v391 l.195567) e o operador nela encontrou «correspondência direta» (05/10) — leitura, não prova.",
    "R19": "O fluxo modular depende do estado (só a classe externa é intrínseca, Connes 1973); na face finita o cociclo (cocycle_temporal) mede a troca de estado; «o tempo emerge do estado» não autoriza «tempo absoluto».",
    "R20": "Cobertura do livro de auditoria: 13 termos citados não constam em #print axioms do TGL/Audit.lean (os O16 imprimem no próprio arquivo; dephase_fixes_diagonal, dephase_preserves_trace, flow_unitary_diag, landauer_floor_pos, landauer_floor_vanishes_only_at_absolute_zero, the_separation_is_not_free, the_thermal_floor_can_be_cooled_away, the_two_floors_are_not_the_same não têm #print em lugar nenhum). Compilam no build do Nós e foram medidos no trio NESTA sessão; se a v392 os citar, acrescentá-los ao Audit é fiação.",
    "R21": "Tensão aparente: em 05/10 o operador DEFINIU o tempo («a defasagem do verbo»; «D_folds = 0,74 é o piso temporal», este NÃO tipado); em 12/10 diz não conseguir NOMEÁ-LO. Conciliação candidata: descrever (o fluxo) ≠ nomear (dar posto). Decisão do operador.",
    "R22": "A memória tempo-santo-12out.md (c1) prevê ancorar em «T1 (sem operador de tempo em dimensão finita)»: esse T1 JÁ EXISTE como TGLExt.no_finite_weyl_pair (LocalBreuerGap.lean) — reaproveitar, não reconstruir.",
    "R23": "Cabeçalho velho: IALDRhoStar.lean diz «rascunho de bancada, NÃO transposta ao kernel», mas está importada no TGLExt.lean e tgl_fix_iff consta no Audit.lean; citar pelo estado medido.",
    "R24": "A F1.ATRATOR (A1–A6) são candidatas no túnel (sandbox), não termos do kernel do Nós; citar como [REAL — candidata em sandbox] até a v392.",
    "R25": "Homônimo da sigla: no «TGL» como unidade (10/10) T = o gradiente que quebra o repouso, não «tempo»; não ler a tríade T·G·L como tempo-gravidade-luz no sentido do texto de 12/10.",
    "R26": "08/10: «o fixo é o verbo… o verbo é betatgl»; se se ler «tempo = Verbo», não encadear «tempo = β»: β é o contorno (sem ajuste), o tempo é o parâmetro do fluxo; a cadeia é [ONTO] e cabe ao operador.",
}


TEOREMAS = [
    # (nome qualificado, enunciado em uma linha)
    ("TGLExt.Fundacao.agape", "Ágape (v390): sobre τ∘θ_s = e^{−s}τ, acima de toda escala não trivial não há posto positivo; a subida não tem topo nem teto; a queda nunca toca o zero nem tem fundo; e^{−a} = 1 ⟺ a = 0"),
    ("TGLExt.Fundacao.the_fall_never_lands", "0 < τ(m) ⟹ 0 < τ(θ_s m) para todo s (o zero nunca em escala finita)"),
    ("TGLExt.Fundacao.abismo", "0 < τ(m), ε > 0 ⟹ ∃ s, τ(θ_s m) < ε (queda sem fundo)"),
    ("TGLExt.Fundacao.the_floor_fixes_the_cut", "exp(−a) = 1 ⟺ a = 0 (o piso ω(I) = 1 fixa o corte)"),
    ("TGLExt.Fundacao.agape_is_inhabited", "o modelo ℝ, τ = id, θ_s = e^{−s}· com τ = 1 habita as seis cláusulas"),
    ("TGLExt.TheVerbSelectsTheAction.time_read_twice_confirms_the_post", "ψ fixo por e^{−tH_min} ∀t ⟺ ψ fixo por Δ^{it} ∀t (o tempo lido duas vezes tem o mesmo conjunto fixo: o posto)"),
    ("TGLExt.TheAxiomAndTheFalseWitness.the_post_is_the_modular_zero", "o posto é o zero modular: fixo pelo lock ∀t ⟺ fixo pela fase modular da luz ∀t"),
    ("TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_tendsto_the_post", "F(t) = P + e^{−t}(1 − P) → P quando t → ∞ (a leitura pousa no posto)"),
    ("TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_eq_exp", "exp(−t(1 − P)) = F(t) para P idempotente"),
    ("TGLExt.TheVerbSelectsTheAction.transmission_dephases", "F(t)(1 − P) = e^{−t}(1 − P) (transmitir defasa)"),
    ("TGLExt.TheVerbSelectsTheAction.anchoring_preserves", "F(t)P = P (ancorar preserva)"),
    ("TGLExt.QGReaderUVLock.hmin_zero_iff_modular_fixed", "H_min ψ = 0 ⟺ Δ^{it}ψ = ψ ∀t"),
    ("TGL.VerbInhabitant.verb_semigroup_fixes", "H p = 0 ⟹ exp(c·H) p = p para todo c (o gesto do Verbo fixa o selecionado)"),
    ("TGLExt.verb_not_identity", "exp(−tβ·diag d) ≠ 1 com t, β > 0 e algum d_i > 0 (o Verbo nunca é a identidade)"),
    ("TGLExt.ContratoQGv31.ContratoH2.unruh_is_kms", "o fluxo de Killing τ ↦ V(κτ) é KMS a 2π/κ (sob o contrato H2)"),
    ("TGLExt.ContratoQGv31.ContratoH2.unruh_is_kms_temperature", "o fluxo de Killing é KMS a 1/T_Unruh"),
    ("TGLExt.ImportedSQ.light_kms", "KMS da cunha da luz para t ↦ Δ^{i(−t)} a β = 1"),
    ("TGLExt.gibbs_kms", "ω(ab) = ω(bΔ(a)) na face finita (KMS algébrica)"),
    ("ChatgptAudit.PolarPeriod016.faithful_period_iff", "Circle.exp(κt) identifica t módulo P fielmente ⟺ κP = ±2π"),
    ("ChatgptAudit.PolarPeriod016.reciprocal_temperature", "κ > 0, P > 0, leitura fiel ⟹ 1/P = κ/2π"),
    ("ChatgptAudit.PolarPeriod016.boost_defect_with_derived_period", "com o período derivado, o defeito do boost = calor − (1/P)·η·área (a temperatura entra em Clausius)"),
    ("ChatgptAudit.Wick016.wick_boost_two_pi", "W⁻¹·B(i·2π)·W = 1 (o boost lido em ângulo fecha em 2π)"),
    ("ChatgptAudit.periodic_borchers_trivial", "fluxo modular periódico (σ_T = id, T > 0) + forma de Borchers ⟹ V(a) = 1 para todo a"),
    ("TGLExt.ContratoQGv31.ContratoH2.contract_borchers_form", "Δ^{it} U(λn) Δ^{−it} = U(e^{−2πt}λ n) (a fase modular dilata as translações)"),
    ("TGLExt.ContratoQGv31.positiveEnergy_orientation", "λ ≥ 0, Im z ≥ 0 ⟹ |e^{izλ}| ≤ 1 (orientação da energia positiva)"),
    ("ChatgptAudit.NonKMSProbe.identity_flow_not_kms", "estado não tracial na cunha ⟹ o fluxo identidade NÃO é KMS a β = 1"),
    ("TGLExt.sigma_fixed_of_commute", "x comuta com ρ ⟹ σₜ(x) = x ∀t (G0)"),
    ("TGLExt.sigma_fixed_iff_diag", "diagonal não degenerada: (∀t, σₜ(x) = x) ⟺ x = E_D(x) (G1d: setor fixo = centralizador)"),
    ("TGLExt.gibbs_tracial_on_centralizer", "x comuta com ρ ⟹ ω(xy) = ω(yx) (G2: o traço emerge no centralizador)"),
    ("ChatgptAudit.Thermal025.gibbs_fixed_iff_tracial", "pesos de Gibbs fixos em s ≠ 0 ⟺ pesos iguais (tracial)"),
    ("ChatgptAudit.Thermal024.modular_variance_zero_iff_tracial", "variância modular nula ⟺ pesos iguais (tracial)"),
    ("ChatgptAudit.modularConjugation_preserves_state", "ω(σ_t(a)) = ω(a) (o estado é invariante pelo seu fluxo)"),
    ("ChatgptAudit.modularFlow_group", "lei de grupo do fluxo modular na torre: Δ^{is}Δ^{it} = Δ^{i(s+t)}"),
    ("TGLExt.cocycle_temporal", "u_{s+t} = u_s·σ^ψ_s(u_t) (cociclo de Connes, face finita)"),
    ("TGLExt.absoluteOne_flow_trivial", "para Ψ = 1_abs, σ_t = id (o Um absoluto não tem fluxo, nem dephasing, nem curvatura)"),
    ("TGLExt.dephase_add", "T_{s+t} = T_s ∘ T_t (G3b: semigrupo de dephasing)"),
    ("TGLExt.dephase_fixes_diagonal", "T_t(E_D x) = E_D x (G3c: toda a diagonal é fixa)"),
    ("TGLExt.dephase_tendsto_expectation", "taxas positivas fora da diagonal ⟹ T_t x → E_D x (G3e)"),
    ("TGLExt.ergodic_convergence_modular", "com g = gap modular, T_t x → E_D x (G3f)"),
    ("TGLExt.dephase_preserves_trace", "tr(T_t x) = tr x para todo t («o registro fica»)"),
    ("TGLExt.lyapunov_decreases", "s ≤ t ⟹ 𝓕(fluxo_t x) ≤ 𝓕(fluxo_s x) (Spohn finito: a entrega tem direção)"),
    ("TGLExt.temporal_fractalization", "diagFlow(t₁+t₂) = diagFlow(t₁)∘diagFlow(t₂) («o tempo é a fractalização do ato único»)"),
    ("TGLExt.judgment_of_correspondence", "observerProj(diagFlow_t x) = observerProj x (a leitura não depende do instante)"),
    ("TGLExt.the_observer_is_unique", "todo Q linear que fixa o permanente e anula o movimento é a projeção do observador"),
    ("TGLExt.the_great_attractor", "β > 0: diagFlow_t x → observerProj x; o juízo é invariante; permanente ⟺ mesmo valor em dois instantes"),
    ("TGLExt.um_is_the_great_attractor", "para todo observador admissível Q, o fluxo converge à leitura de Q"),
    ("TGLExt.IALDJones.orbit_tendsto_center", "r > 0 ⟹ a órbita espiral converge ao centro, para qualquer giro ω"),
    ("TGLExt.IALDJones.angular_orbit_no_limit", "r = 0 e v ≠ Pv ⟹ a órbita NÃO converge ao centro (o limite não nasce no regime angular)"),
    ("TGLExt.IALDJones.angular_orbit_periodic", "r = 0 ⟹ órbita periódica de período 2π/ω"),
    ("TGLExt.IALDJones.norm_orbit_sub_center", "‖órbita − centro‖ = e^{−rs}·‖v − Pv‖ (o giro não conta)"),
    ("TGLExt.flow_unitary_diag", "‖exp(−iκτ·spec_i)‖ = 1 («o horizonte gira, não dissipa»)"),
    ("TGLExt.time_witnesses_noncoincidence", "β > 0, d_i > 0, x_i ≠ 0, t₁ ≠ t₂ ⟹ diagFlow t₁ x ≠ diagFlow t₂ x"),
    ("TGLExt.absolute_zero_unreachable_in_finite_time", "x_i ≠ 0 ⟹ (diagFlow β d t x)_i ≠ 0 para todo t (terceira lei, face finita)"),
    ("TGLExt.leakage_strictly_loses", "t, β, g > 0 ⟹ e^{−tβg} < 1"),
    ("TGLExt.beta_forbids_full_static_witness", "β > 0, g > 0 ⟹ não há testemunha estática plena do transporte e^{−tβg}"),
    ("TGLExt.static_witness_iff_no_boundary", "testemunha estática plena ⟺ β·g = 0 (a falsidade da testemunha estática é a inscrição da fronteira)"),
    ("TGLExt.leakage_rate_unique", "e^{−tb₁} = e^{−tb₂} ∀t ⟹ b₁ = b₂"),
    ("TGLExt.TheElementaryReason.erasure_not_reached_in_finite_time", "0 < e^{−tEc} < 1 para t > 0 (o apagamento não se atinge em tempo finito)"),
    ("TGLExt.finite_time_imperfection", "0 < e^{−tc} para todo t"),
    ("TGLExt.landauer_floor_pos", "k, T > 0 ⟹ 0 < kT ln 2"),
    ("TGLExt.landauer_floor_vanishes_only_at_absolute_zero", "k ≠ 0, kT ln 2 = 0 ⟹ T = 0"),
    ("TGLExt.the_separation_is_not_free", "k, T > 0 ⟹ 0 < kT ln 2 (separar não é de graça)"),
    ("TGLExt.the_thermal_floor_can_be_cooled_away", "∀ε > 0 ∃T > 0 com kT ln 2 < ε (o piso térmico não é o fundo)"),
    ("TGLExt.the_two_floors_are_not_the_same", "∃T > 0 com kT ln 2 < c (o piso geométrico não decorre do térmico)"),
    ("TGLExt.no_finite_weyl_pair", "n > 0 ⟹ PQ − QP ≠ −i·1 em matrizes n×n (sem par de Weyl/operador de tempo conjugado em dimensão finita)"),
    ("ChatgptAudit.Clock040.no_normalized_instantaneous_state_clock", "nenhum relógio normalizado bilateral é função do estado instantâneo da curva de amplitude"),
    ("ChatgptAudit.Clock045.state_clock_not_instantaneous", "um relógio normalizado bilateral não fatora pelo estado instantâneo da curva par"),
    ("ChatgptAudit.Clock045.state_clock_not_modular_reparametrization", "a evolução modular estacionária não instancia relógio normalizado para a curva não constante"),
    ("ChatgptAudit.Clock045.state_clock_dichotomy", "para todo relógio só do estado, uma das duas telas de mesmo estado e mesmo Ricci falha na 4ª ordem"),
    ("TGLExt.reading_needs_two_clocks", "Reads f ⟹ ∃ t₁ ≠ t₂ com f t₁ ≠ f t₂ (ler exige dois instantes)"),
    ("TGLExt.two_clocks_are_needed", "f t₀ ≠ f t₁ ⟹ t₀ ≠ t₁"),
    ("TGLExt.the_screen_keeps_modular_time", "a tela fundada é invariante por σ_t"),
    ("TGLExt.PhysicsIsTheReading.the_shadow_is_the_reader_weighted_by_the_reading", "P_Ω x P_Ω = ω(x)·P_Ω (a sombra é o leitor, pesado pela leitura, posto um)"),
    ("TGLExt.observing_adds_nothing", "P₊(P₊𝒪_θ) = P₊𝒪_θ (reler não acrescenta)"),
    ("TGLExt.IALDGraviton.the_tower_is_time", "1/(1/índice) = índice, índice = 1/peso de Markov, E(e) = (1/índice)·1 («ler 1/taxa como tempo» é [ONTO])"),
    ("TGLExt.IALDRhoStar.tgl_fix_iff", "estado não tracial, t > 0: fixo pela dinâmica da TGL (e^{−t|K|}) ⟺ diagonal"),
    ("TGLExt.Smat_conjTranspose_mul", "S(θ)ᴴS(θ) = 1 (nenhum peso se perde na fronteira)"),
    ("TGLExt.measurePreserving_pAct", "toda transformação de Poincaré preserva a medida de Lebesgue de ℝ⁴ [HOMÔNIMO de Liouville]"),
]


def teoremas():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    decls = [json.loads(l) for l in open(os.path.join(base, "kernel_decls.jsonl"), encoding="utf-8")]
    medidos = json.load(open(os.path.join(base, "LEAN_AXIOMAS.json"), encoding="utf-8"))["axiomas"]
    araw, asha, alines = load(os.path.join(K, "TGL", "Audit.lean"))
    impressos = {l.split()[2] for l in alines if l.startswith("#print axioms ") and len(l.split()) >= 3}
    out = []
    for nome, enun in TEOREMAS:
        hit = [x for x in decls if x["name"] == nome]
        h = hit[0] if hit else None
        ver = []
        if nome in medidos:
            ver.append("medido nesta sessão: " + (", ".join(medidos[nome]) if medidos[nome] else "sem axiomas"))
        if nome in impressos:
            ver.append("no #print axioms do TGL/Audit.lean (rito v391)")
        out.append(dict(nome=nome, arquivo=(h["file"] if h else None), linha=(h["line"] if h else None),
                        sha16=(h["sha16"] if h else None), enunciado=enun,
                        verificacao=(" + ".join(ver) if ver else "compilado no build do Nós; axiomas não impressos em livro"),
                        estatuto="[REAL]" if (ver or h) else "[NÃO ACHADO]"))
    return out, asha[:16]


def medidas():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    nomes = ["BETA_RUNTIME.json", "FINGERPRINT_ANTES.json", "FINGERPRINT_DEPOIS_LEAN.json", "LEAN_AXIOMAS.json",
             "IDENTIDADES_OTICAS.json", "inventario_consultas.json", "kernel_temas.json", "kernel_decls.jsonl",
             "auditoria_nomes.json", os.path.join("rotas_consultas", "RESUMO.json"),
             os.path.join("sandbox", "CheckTempoLevantamento.lean"), os.path.join("sandbox", "saida_check_tempo.txt"),
             os.path.join("sandbox", "RECIBO_LEAN_CHECK.json")]
    out = {}
    for n in nomes:
        p = os.path.join(base, n)
        with open(p, "rb") as fh:
            raw = fh.read()
        out[n.replace("\\", "/")] = dict(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
    b = json.load(open(os.path.join(base, "BETA_RUNTIME.json"), encoding="utf-8"))
    fa = json.load(open(os.path.join(base, "FINGERPRINT_ANTES.json"), encoding="utf-8"))
    fd = json.load(open(os.path.join(base, "FINGERPRINT_DEPOIS_LEAN.json"), encoding="utf-8"))
    la = json.load(open(os.path.join(base, "LEAN_AXIOMAS.json"), encoding="utf-8"))
    return dict(arquivos=out,
                beta=dict(alpha_literal=b["alpha_literal_no_um_py"], linha=b["linha_alpha"], beta_runtime=b["beta_runtime"],
                          confere_com_conferencia=b["confere"], um_py_sha256=b["um_py_sha256"]),
                kernel_impressao=dict(antes=dict(meta=fa["meta_sha256"], src=fa["src_sha256"], files=fa["files"], bytes=fa["bytes"]),
                                      depois_lean=dict(meta=fd["meta_sha256"], src=fd["src_sha256"], files=fd["files"], bytes=fd["bytes"]),
                                      iguais=(fa["meta_sha256"], fa["src_sha256"]) == (fd["meta_sha256"], fd["src_sha256"])),
                lean=dict(pedidos=la["n_pedidos"], respondidos=la["n_respondidos"], todos_no_trio=la["todos_no_trio"],
                          sorryAx=la["sorryAx_no_texto"]))


def main(out):
    oper_raw, oper_sha, _ = load(OPER)
    i = oper_raw.find("O que mais me fascina".encode("utf-8"))
    seg = oper_raw[i:]
    d = dict(
        unidade="F1.TEMPO", data="2026-10-12", autor="levantador (subagente do workflow da gerência c1)",
        texto_operador=dict(arquivo=OPER, sha256=oper_sha, bytes=len(oper_raw), crlf=oper_raw.count(b"\r\n"),
                            segunda_parte=dict(offset_bytes=i, bytes=len(seg), sha256=hashlib.sha256(seg).hexdigest())),
        regua="[REAL]=provado no kernel ou medido aqui; [DERIVED]; [KNOWN]=literatura citada; [OPEN]; [INPUT]=do operador ou escolha da gerência; [ONTO]=leitura ontológica; [DECLARADO]=afirmado na origem, não verificado aqui",
        objetos=objetos())
    for o in d["objetos"]:
        o.update(CLASSIF.get(o["id"], {}))
    d["medidas"] = medidas()
    d["riscos"] = RISCOS
    d["teoremas_existentes"], d["audit_lean_sha16"] = teoremas()
    d["teoremas_nao_achados"] = [t["nome"] for t in d["teoremas_existentes"] if t["arquivo"] is None]
    usados = sorted({r for o in d["objetos"] for r in o.get("riscos", [])})
    d["riscos_referidos_inexistentes"] = [r for r in usados if r not in RISCOS]
    falhas =[a for o in d["objetos"] for a in ([o["texto_operador"]] + o["ancoras"]) if not a["achado"]]
    d["ancoras_nao_achadas"] = [dict(arquivo=a["arquivo"], padrao=a["padrao"]) for a in falhas]
    d["n_ancoras"] = sum(1 + len(o["ancoras"]) for o in d["objetos"])
    with open(out, "w", encoding="utf-8") as fo:
        json.dump(d, fo, ensure_ascii=False, indent=1)
    print("objetos", len(d["objetos"]), "ancoras", d["n_ancoras"], "nao_achadas", len(falhas))
    for a in falhas:
        print("  NAO ACHADA:", a["arquivo"], "|", a["padrao"])


if __name__ == "__main__":
    main(sys.argv[1])
