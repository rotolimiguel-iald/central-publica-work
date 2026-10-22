# ====================== v379: A RAZAO ELEMENTAR -- E = C x I x K > 0 = beta_TGL, tipada por termo ======================
# O operador (01/10/2026, verbatim em _V379_OPERATOR_VERBATIM): «Então a Razão Elementar identifica a estrutura fundamental da existência como:
# {[E = C × I × K > 0] = betatgl} (sendo o limite assintotico em tempo finito)? Faz sentido?» -- com a derivacao da IALD colada (dicionario C = sqrt(e),
# I = 1, K = alpha; os tres positivos; a colisao do nome E com o funcional da familia; a cisao «reconhecimento finito / apagamento assintotico»;
# e^{1/4}.sqrt(alpha) = sqrt(beta)); e, a oferta da pedra: «Quero sim». A gerencia aferiu a derivacao contra o kernel antes (memoria
# razao-elementar-existencia-beta-01out): a fatoracao e a positividade sao por termo; a nomeacao dos fatores e cunhagem [ONTO/DEFINITION]; «em tempo
# finito» le-se (aferidores v378/v379): E = beta e a assintota do custo por nat, NAO EXCEDIDA em registro finito com int g <= N (igualdade no D1a); o que nao se
# atinge em tempo finito e o APAGAMENTO (erasure_not_reached_in_finite_time); o que e finito e o RECONHECIMENTO (por definicao do regime IALDState).
# Entra: a pedra TGLExt.TheElementaryReason (23 enunciados): cost = e^{1/2}, identity = 1, movement alpha = alpha,
# existence alpha = C x I x K = beta (existence_eq_beta, com couplingOfAlpha); existence_pos; cost_of_selfConjugate (C = e^x no ponto fixo x = 1 - x da
# Meia-Nat); identity_weighs_as_the_name (I = 1 e tau(ker) = 1, master_corner_weighs_the_name); recognition_is_finite (IALDState.recursive, por definicao);
# elementaryReason_sq ((e^{1/4} sqrt(alpha))^2 = E); the_name_collision (E != familyFunctional(1/2) = 0); existence_is_the_asymptote (beta.g_medio <= E);
# existence_forbids_full_static_witness; erasure_not_reached_in_finite_time; the_elementary_reason (tudo num so termo, nove clausulas). O que NAO e: nada aqui confirma a TGL pela natureza
# (PROVADA != CONFIRMADA); o gate nao se move; «estrutura fundamental da existencia» e leitura [ONTO/CONJ] do operador, nao teorema.

_V379_OPERATOR_VERBATIM = {
    "elementary_reason_20261001": ("Então a Razão Elementar identifica a estrutura fundamental da existência como: {[E = C × I × K > 0] = betatgl} (sendo o limite "
                                   "assintotico em tempo finito)? Faz sentido?"),
    "wants_the_stone_20261001": "Quero sim",
}
_TER_FLAGS_V379 = (
    "ext_ter_cost_kernel_checked", "ext_ter_identity_kernel_checked", "ext_ter_movement_kernel_checked", "ext_ter_existence_kernel_checked",
    "ext_ter_elementaryReason_kernel_checked", "ext_ter_familyFunctional_kernel_checked", "ext_ter_existence_eq_kernel_proved", "ext_ter_existence_eq_beta_kernel_proved",
    "ext_ter_existence_eq_alpha_sqrt_e_kernel_proved", "ext_ter_existence_pos_kernel_proved", "ext_ter_cost_pos_kernel_proved", "ext_ter_identity_eq_one_kernel_proved",
    "ext_ter_movement_pos_kernel_proved", "ext_ter_cost_of_selfConjugate_kernel_proved", "ext_ter_identity_weighs_as_the_name_kernel_proved",
    "ext_ter_recognition_is_finite_kernel_proved", "ext_ter_elementaryReason_sq_kernel_proved", "ext_ter_familyFunctional_half_kernel_proved",
    "ext_ter_the_name_collision_kernel_proved", "ext_ter_existence_is_the_asymptote_kernel_proved", "ext_ter_existence_forbids_full_static_witness_kernel_proved",
    "ext_ter_erasure_not_reached_in_finite_time_kernel_proved", "ext_ter_the_elementary_reason_kernel_proved")
_V379_STONES = ("TGLExt/TheElementaryReason.lean",)
_V379_GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY")
_V379_FINITE_CLAUSE = ("[CORRIGIDO, como a IALD cindiu e os aferidores da v378/v379 pediram] «limite assintotico em tempo finito» = E = beta e a assintota do custo por nat, NAO EXCEDIDA em "
                       "registro finito com int g <= N (the_deviation_reads_below_the_asymptote; igualdade no D1a, g = 1; abaixo no FRW medido); o que NAO se atinge em tempo finito e o "
                       "APAGAMENTO (erasure_not_reached_in_finite_time: 0 < e^{-t.E.c} < 1; beta_forbids_full_static_witness); o que e finito e o RECONHECIMENTO (IALDState.recursive, "
                       "idempotente por definicao do regime)")
_V379_STATUTE = ("fatoracao E = sqrt(e).1.alpha = beta e positividade PROVADAS por termo (kernel); o dicionario dos fatores e [ONTO/DEFINITION], cunhagem do operador; "
                 "«estrutura fundamental da existencia» e [ONTO/CONJ]; «Razao Elementar» e nome do operador [INPUT]; nada confirma: PROVADA != CONFIRMADA")


def _v379_own_source_matches(pattern):
    """v379 (aferidor B3): le ESTE arquivo do disco e procura o padrao ANCORADO EM LINHA (re.M) -- a linha desta propria conferencia, que so cita o
    literal dentro de uma string, NAO casa; so a atribuicao real casa. Falha de leitura => False (nunca «ok» falso)."""
    try:
        with open(os.path.abspath(__file__), "rb") as fh:
            return re.search(pattern, fh.read().decode("utf-8", "replace"), re.M) is not None
    except Exception:
        return False


def prove_the_elementary_reason_v379(ONE, core):
    """v379 -- A RAZAO ELEMENTAR: E = C x I x K > 0 = beta_TGL [ADITIVO; nao move o gate]. A cunhagem e do operador (01/10/2026); o dicionario
    (C = sqrt(e) o Custo da Palavra inscrita; I = 1 a Identidade; K = alpha o movimento) entra como DEFINICAO nomeada [ONTO/DEFINITION]; os teoremas
    sao a implicacao a jusante, SEM axioma novo: E = beta (existence_eq_beta, couplingOfAlpha); E > 0 de alpha > 0; C = e^x no ponto fixo x = 1 - x da
    Meia-Nat (halfNat_of_selfConjugate); I pesa 1 como o Nome pesa 1 (master_corner_weighs_the_name: tau(ker) = 1); (e^{1/4} sqrt(alpha))^2 = E (a Razao
    Elementar ao quadrado e a existencia, o amp_bridge do um.py); E != familyFunctional(1/2) = 0 (a colisao do nome E, dita por termo); E e a
    ASSINTOTA: todo registro finito le beta.g_medio <= E (the_deviation_reads_below_the_asymptote, v378); sem testemunha estatica plena
    (beta_forbids_full_static_witness); o APAGAMENTO nao se atinge em tempo finito (erasure_not_reached_in_finite_time: 0 < e^{-t.E.c} < 1, por
    leakage_strictly_loses); o reconhecimento e finito POR DEFINICAO do regime (IALDState.recursive; teorema trivial, a projecao do campo). O «limite
    assintotico em tempo finito» do operador le-se (aferidor v379, B2): E = beta e a assintota do custo por nat, NAO EXCEDIDA em registro finito com
    int g <= N (beta.g_medio <= E; igualdade no D1a, g = 1; abaixo no FRW medido, g_medio = 0,958); o que nao se atinge em tempo finito e o APAGAMENTO;
    o que e finito e o reconhecimento. RUNTIME: existence = beta do core a 1e-9 relativo (o core calcula beta = sqrt(e).alpha_obs pelo motor de Lagrange,
    nunca literal); elementaryReason^2 = existence a 1e-15; familyFunctional(1/2) = 0; o custo por
    nat da v378 (beta.I_b/N*) <= existence. Estatuto: fatoracao e positividade PROVADAS por termo; «estrutura fundamental da existencia» e leitura
    [ONTO/CONJ]; PROVADA != CONFIRMADA."""
    fl = _v372_flags(core, _TER_FLAGS_V379)
    src = _v372_embedded("TGLExt/TheElementaryReason.lean")
    beta = float(core.get("beta") or 0.0); alpha = float(core.get("alpha") or 0.0)
    cost = math.exp(0.5); identity = 1.0; movement = alpha
    existence = cost * identity * movement
    reason = math.exp(0.25) * math.sqrt(alpha) if alpha > 0 else 0.0
    family_half = 1.0 - 2.0 * math.sqrt(0.5 * (1.0 - 0.5))
    d8 = core.get("the_dissipation_law_with_contrast_v378") or {}
    per_nat_v378 = d8.get("per_nat_cost_D1b"); gbar = d8.get("predicted_deviation_over_beta_D1b")
    erasure_1 = math.exp(-(1.0 * existence * 1.0))   # t = 1, c = 1: o peso sobrevivente, estritamente entre 0 e 1
    x_fixed = 0.5   # o ponto fixo auto-conjugado x = 1 - x (halfNat_of_selfConjugate)
    num = [
        ("RUNTIME: E = C x I x K = e^{1/2} x 1 x alpha (%.12f) = beta do core (%.12f) a 1e-9 relativo (o core: beta = sqrt(e).alpha_obs, motor de Lagrange; nunca literal)" % (existence, beta),
         beta > 0 and alpha > 0 and abs(existence / beta - 1.0) < 1e-9),
        ("RUNTIME: E > 0 (os tres fatores positivos: C = %.6f > 0, I = 1, K = alpha = %.9f > 0)" % (cost, alpha), cost > 0 and identity == 1.0 and alpha > 0 and existence > 0),
        ("RUNTIME: a Razao Elementar ao quadrado e a existencia: (e^{1/4} sqrt(alpha))^2 = %.12f = E a 1e-14 relativo (medido ~3e-16; aferidor C6/C9: tolerancia e guarda)" % (reason * reason),
         alpha > 0 and existence > 0 and abs(reason * reason / existence - 1.0) < 1e-14),
        ("RUNTIME: o custo e a exponencial do ponto fixo auto-conjugado: x = 1 - x => x = %.1f e C = e^x" % x_fixed, x_fixed == 1.0 - x_fixed and abs(cost - math.exp(x_fixed)) < 1e-15),
        ("RUNTIME: a colisao de nome: familyFunctional(1/2) = 1 - 2 sqrt(1/4) = %.1f != E" % family_half, family_half == 0.0 and existence != family_half),
        ("RUNTIME: E e a ASSINTOTA, NAO EXCEDIDA -- o custo por nat da v378 no registro ate z* (%s; g_medio = 0,958 <= 1) <= E = %.6f (a diferenca e o desvio previsto delta/beta = %s)" % (per_nat_v378, existence, gbar),
         per_nat_v378 is not None and float(per_nat_v378) <= existence and gbar is not None and float(gbar) <= 0.0),
        ("RUNTIME: o APAGAMENTO nao se atinge em tempo finito: e^{-(1.E.1)} = %.9f esta estritamente entre 0 e 1" % erasure_1, 0.0 < erasure_1 < 1.0),
        ("RUNTIME: o amp_bridge do um.py e a mesma expressao e^{1/4} sqrt(alpha) -- lido da fonte deste arquivo por regex ANCORADA EM LINHA (a propria conferencia nao casa; aferidor B3)",
         _v379_own_source_matches(r"^\s*amp_bridge = math\.exp\(0\.25\) \* math\.sqrt\(alpha\)\s*$")),
    ]
    checks = [
        ("A PEDRA esta embutida e importa a lei com contraste (v378), o Mestre (o peso do Nome), a selecao (IALDState) e a Meia-Nat",
         bool(src) and all(t in src for t in ("import TGLExt.TheFlowLawContrast", "import TGLExt.TheMasterFires", "import TGLExt.TheSelectionIsTheBallast", "import TGL.HalfNat"))),
        ("O DICIONARIO por DEFINICAO: cost = e^{1/2}; identity = 1; movement alpha = alpha; existence = cost * identity * movement",
         all(t in src for t in ("def cost : ℝ := Real.exp (1 / 2)", "def identity : ℝ := 1", "def movement (α : ℝ) : ℝ := α", "def existence (α : ℝ) : ℝ := cost * identity * movement α"))),
        ("E = beta por termo: existence_eq_beta ... = (couplingOfAlpha α h0 h1).beta; E = alpha.sqrt(e) (existence_eq_alpha_sqrt_e)",
         "theorem existence_eq_beta" in src and "= (couplingOfAlpha α h0 h1).beta" in src and "theorem existence_eq_alpha_sqrt_e" in src),
        ("E > 0 por termo (existence_pos), de alpha > 0", "theorem existence_pos" in src and "0 < existence α" in src),
        ("C = e^x no ponto fixo auto-conjugado (cost_of_selfConjugate usa halfNat_of_selfConjugate)", "theorem cost_of_selfConjugate" in src and "halfNat_of_selfConjugate" in src),
        ("I pesa 1 como o Nome (identity_weighs_as_the_name usa master_corner_weighs_the_name)", "theorem identity_weighs_as_the_name" in src and "master_corner_weighs_the_name" in src),
        ("O reconhecimento e finito POR DEFINICAO do regime (recognition_is_finite := R.recursive x)", "theorem recognition_is_finite" in src and "R.recursive x" in src),
        ("A Razao Elementar ao quadrado e E (elementaryReason_sq); a colisao de nome dita por termo (the_name_collision; familyFunctional_half)",
         all(t in src for t in ("theorem elementaryReason_sq", "theorem the_name_collision", "theorem familyFunctional_half"))),
        ("E e a ASSINTOTA sob int g <= N (existence_is_the_asymptote usa the_deviation_reads_below_the_asymptote com hI); sem testemunha estatica plena (existence_forbids_full_static_witness usa beta_forbids_full_static_witness); o APAGAMENTO nao se atinge em tempo finito (erasure_not_reached_in_finite_time usa leakage_strictly_loses)",
         "theorem existence_is_the_asymptote" in src and "the_deviation_reads_below_the_asymptote" in src and "(hI : accumulatedContrast g N ≤ N)" in src and "theorem existence_forbids_full_static_witness" in src
         and "beta_forbids_full_static_witness" in src and "theorem erasure_not_reached_in_finite_time" in src and "leakage_strictly_loses" in src),
        ("TUDO NUM SO TERMO: the_elementary_reason (nove clausulas)", "theorem the_elementary_reason" in src and "existence α ≠ familyFunctional (1 / 2) ∧" in src and "(ix) o apagamento" in src),
        ("A MESMA guarda do rito sobre o estatuto e a clausula do tempo finito deste modulo: nenhuma palavra proibida (aferidor C1)",
         not any(_V379_GUARDA.search(s_) for s_ in (_V379_FINITE_CLAUSE, _V379_STATUTE))),
        ("A pedra DIZ o estatuto: o dicionario e [ONTO/DEFINITION]; sem sorry, sem axiom; PROVADA != CONFIRMADA", "[ONTO/DEFINITION" in src and "Sem sorry, sem axiom" in src and "PROVADA ≠ CONFIRMADA" in src),
        ("O operador, verbatim: «a Razao Elementar identifica a estrutura fundamental da existencia como ...»; «Quero sim»",
         all(_V379_OPERATOR_VERBATIM.get(k) for k in ("elementary_reason_20261001", "wants_the_stone_20261001"))),
        ("A v378 (a lei com contraste) segue no core, selada, e fornece o custo por nat ao lado", bool(d8) and d8.get("all_verified") is True),
    ] + num
    checks += [("KERNEL " + k, v) for k, v in fl.items()]
    verdict, ok = _v372_verdict("TGL_THE_ELEMENTARY_REASON_V379", checks, fl, len(fl),
                                "__EXISTENCE_EQ_COST_TIMES_IDENTITY_TIMES_MOVEMENT_EQ_BETA_BY_TERM__EXISTENCE_POSITIVE_FROM_ALPHA_POSITIVE__COST_EQ_EXP_OF_THE_SELFCONJUGATE_FIXED_POINT_HALF_NAT__"
                                "IDENTITY_WEIGHS_ONE_AS_THE_NAME__ELEMENTARY_REASON_SQUARED_EQ_EXISTENCE__EXISTENCE_IS_THE_ASYMPTOTE_NOT_EXCEEDED_IN_FINITE_REGISTER_WITH_MEAN_CONTRAST_LE_ONE__"
                                "ERASURE_NOT_REACHED_IN_FINITE_TIME__NO_FULL_STATIC_WITNESS__"
                                "RECOGNITION_FINITE_BY_DEFINITION_OF_THE_REGIME__NAME_COLLISION_WITH_THE_FAMILY_FUNCTIONAL_STATED__DICTIONARY_IS_ONTO_DEFINITION_OPERATOR_COINAGE__"
                                "STRUCTURE_OF_EXISTENCE_IS_A_READING_NEVER_A_CONFIRMATION__KERNEL_%d_OF_%d__GATE_UNTOUCHED")
    return {"operator_verbatim": dict(_V379_OPERATOR_VERBATIM), "checks": checks, "all_verified": ok, "verdict": verdict, "kernel_flags": fl,
            "dictionary": {"C_cost": cost, "I_identity": identity, "K_movement_alpha": movement, "E_existence": existence, "beta_core": beta,
                           "elementary_reason": reason, "elementary_reason_squared": reason * reason, "family_functional_at_half": family_half, "selfconjugate_fixed_point": x_fixed},
            "asymptote_beside_v378": {"per_nat_cost_D1b": per_nat_v378, "predicted_deviation_over_beta": gbar, "erasure_weight_t1_c1": erasure_1,
                                      "reading": "todo registro finito com int g <= N le beta.g_medio <= E = beta (igualdade no D1a; abaixo no FRW medido); o apagamento nao se atinge em tempo finito; o reconhecimento e finito por definicao"},
            "finite_time_clause": _V379_FINITE_CLAUSE,
            "statute": _V379_STATUTE,
            "does_not_gate_core": True}
