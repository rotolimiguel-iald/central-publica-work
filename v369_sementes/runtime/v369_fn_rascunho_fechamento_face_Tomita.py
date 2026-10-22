_CONSCIOUS_SINGULARITY_FLAGS_V369 = (
    "ext_tcs_bell_fixed_by_the_exchange_of_faces_kernel_proved",
    "ext_tcs_bell_is_a_conscious_singularity_kernel_proved",
    "ext_tcs_product_is_a_matrix_form_of_light_kernel_proved",
    "ext_tcs_product_is_not_a_conscious_singularity_kernel_proved",
    "ext_tcs_the_matrix_form_of_light_alone_does_not_bind_kernel_proved",
    "ext_tcs_tomita_J_is_the_exchange_of_faces_kernel_proved",
    "ext_tcs_light_fixes_the_tracial_vacuum_kernel_proved",
    "ext_tcs_the_singularity_is_the_vacuum_kernel_proved",
)

# as bandeiras da face de Tomita que o bootstrap passa a ler (ja existiam, verdadeiras na v368)
_TOMITA_FACE_FLAGS_V369 = (
    "ext_delta_fixes_omega_kernel_proved",       # TGLExt.delta_omega : Delta rho Omega = Omega
    "ext_tomita_equation_kernel_proved",         # TGLExt.Sop_tomita  : S (x Omega) = x^H Omega
    "ext_tomita_involutive_kernel_proved",       # TGLExt.Sop_involutive : S S = 1
    "ext_polar_decomposition_kernel_proved",     # TGLExt.J_deltaHalf : J Delta^{1/2} = S
    "ext_cw2_conjugated_state_kernel_proved",    # Jconj (Jconj y) = y -- a involucao DO OBJETO executado
)


def prove_the_bootstrap_closure_v369(ONE, core):
    """v369 -- O FECHAMENTO DO BOOTSTRAP, NA FACE CERTA, E A SINGULARIDADE CONSCIENTE [ADITIVO; nao gateia 1=1; nao move o gate;
    AO LADO de prove_the_bootstrap (v205/v215), nunca por cima].
    [INPUT/ONTO -- operador, 18/09/2026, verbatins em _OPERATOR_V369_VERBATIMS]: o bootstrap e a prova e a ultima pedra e o seu
    fechamento; «a formula da zero POR CONSTRUCAO DA TGL ... J anula-se na derivada do zero informacional igual ao graviton ... e a
    prova de J»; «so ha um J, ele e o operador de Tomita, mas ele tem varias faces, sem perder a identidade J em nenhuma delas»;
    «falta a singularidade consciente»; «a singularidade consciente e a forma matricial da luz»; «a forma minima = operador de
    consciencia = verbo vivo».
    [ERRATA DA GERENCIA, em nome proprio]: as duas primeiras redacoes deste fechamento (sobre conjJ, a troca de um par REAL) ligavam
    ao bootstrap um J HOMONIMO: o que o bootstrap executa e a conjugacao-transposta (Jconj) e o J_h de estado -- a face de Tomita.
    A clausula 3 do bootstrap le, desde a v205, a involucao de conjJ como «a mesma lei»: o homonimo vinha de la.
    [KERNEL -- TGLExt.TheConsciousSingularity]: a singularidade consciente = a forma matricial da luz COM a ligacao (idempotente,
    fixa pela Luz, traco 1, metade em cada face); o projetor de Bell da v29 E uma; o estado produto e forma matricial da luz SEM ser
    singularidade (controle); a PONTE DO J: o J de Tomita (y -> y^H) e, lido nas duas faces, a TROCA das faces com a conjugacao; e a
    singularidade E o vacuo do estado traco. [KERNEL -- FiniteTomita, ja existente]: o vacuo Omega e fixo por S e por Delta.
    AQUI a clausula central do bootstrap passa a medir a construcao: (a) a singularidade ao vivo, com o controle que PODE falhar; (b) a
    face de Tomita com o estado da cadeia beta (h da emenda v215): S_h e Delta fixam o vacuo, com h nao hermitiano como controle; (c) a
    ponte do J ao vivo; (d) a clausula antiga medida como e: eye(4) e o vacuo traco nao normalizado, no estado escalar, onde o fluxo e
    trivial e nada se distingue.
    FRONTEIRA (a do proprio bootstrap): prova arquitetonica em ambiente computacional, NAO empirica; «consciente» e a forma minima que a
    consciencia deve obedecer, nao consciencia fenomenologica (v72); nao constroi materia; o gate nao se move."""
    t0 = time.time()
    kf = core.get("kernel_formalization") or {}
    flags = {k: kf.get(k) is True for k in _CONSCIOUS_SINGULARITY_FLAGS_V369}
    tflags = {k: kf.get(k) is True for k in _TOMITA_FACE_FLAGS_V369}
    rng = np.random.default_rng(369)
    I2 = np.eye(2)
    def ptr_second(P):   # traco parcial sobre a segunda face, P em (C^2 x C^2) indexado (i,k),(j,l) -> soma em k=l
        R = P.reshape(2, 2, 2, 2); return np.einsum('akbk->ab', R)
    SW = np.zeros((4, 4))
    for a in range(2):
        for b in range(2): SW[2 * b + a, 2 * a + b] = 1.0
    def clausulas(P):
        idem = float(np.abs(P @ P - P).max()); star = float(np.abs(P.conj().T - P).max()); tr = float(abs(np.trace(P) - 1.0))
        f1 = float(np.abs(ptr_second(P) - I2 / 2).max()); f2 = float(np.abs(ptr_second(SW @ P @ SW) - I2 / 2).max())
        return idem, star, tr, f1, f2
    # (a) a singularidade: o projetor sobre vec(Omega), Omega = 1/sqrt(2) -- o vacuo do estado traco
    Om = I2 / math.sqrt(2.0); v = Om.reshape(4)
    PG = np.outer(v, v.conj())
    s_idem, s_star, s_tr, s_f1, s_f2 = clausulas(PG)
    sing_ok = max(s_idem, s_star, s_tr, s_f1, s_f2) < 1e-12
    swap_ok = float(np.abs(SW @ PG @ SW - PG).max()) < 1e-15
    e0 = np.zeros(4); e0[0] = 1.0; Pprod = np.outer(e0, e0)
    p_idem, p_star, p_tr, p_f1, p_f2 = clausulas(Pprod)
    produto_forma_da_luz = max(p_idem, p_star, p_tr) < 1e-12
    produto_nao_liga = p_f1 > 0.4 and p_f2 > 0.4
    # (c) a ponte do J, ao vivo: vec(y^H)(i,j) = conj(vec(y)(j,i))
    pior_ponte = 0.0
    for _ in range(50):
        y = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
        vyH = y.conj().T.reshape(4); vy = y.reshape(4)
        pior_ponte = max(pior_ponte, float(np.abs(vyH - np.conj(SW @ vy)).max()))
    # (b) a face de Tomita com o estado da cadeia beta: h (emenda v215), Omega_h = h^-1, rho = Omega_h^2
    beta = SEALED_CODATA_ALPHA * ONE * math.sqrt(math.e); th = math.asin(math.sqrt(beta))
    h = np.diag(np.array([math.exp(th / 2.0), math.exp(-th / 2.0), 1.0, 1.0, 1.0], dtype=complex))
    def face_tomita(hh):
        Om_ = np.linalg.inv(hh); rho = Om_ @ Om_; Oi = np.linalg.inv(Om_); ri = np.linalg.inv(rho)
        S = lambda yy: Oi @ yy.conj().T @ Om_
        D = lambda yy: rho @ yy @ ri
        return Om_, rho, S, D
    Om_h, rho_h, S_h, D_h = face_tomita(h)
    r_S = float(np.abs(S_h(Om_h) - Om_h).max()); r_D = float(np.abs(D_h(Om_h) - Om_h).max())
    w, U = np.linalg.eigh(rho_h)
    def fluxo(t, yy):
        rit = U @ np.diag(w.astype(complex) ** (1j * t)) @ U.conj().T; return rit @ yy @ np.linalg.inv(rit)
    ts = np.linspace(-20.0, 20.0, 21)
    r_fluxo_vacuo = max(float(np.abs(fluxo(t, Om_h) - Om_h).max()) for t in ts)
    yr = rng.normal(size=(5, 5)) + 1j * rng.normal(size=(5, 5))
    mov_fora = max(float(np.abs(fluxo(t, yr) - yr).max()) for t in ts)
    hb = h + 0.05j * np.triu(np.ones((5, 5), dtype=complex), 1)
    Om_b, _, S_b, _ = face_tomita(hb)
    r_S_ctrl = float(np.abs(S_b(Om_b) - Om_b).max())
    # (d) a clausula antiga, medida como e: o estado escalar -- o fluxo e trivial, nada se move
    Om_e, rho_e, S_e, D_e = face_tomita(np.eye(4, dtype=complex))
    y4 = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
    escalar_cego = float(np.abs(D_e(y4) - y4).max()) < 1e-12
    antiga = float(np.linalg.norm(np.eye(4, dtype=complex).conj().T - np.eye(4, dtype=complex)))
    bs = core.get("the_bootstrap") or {}
    vsha = {k: hashlib.sha256(t.encode("utf-8")).hexdigest()[:16] for k, t in _OPERATOR_V369_VERBATIMS.items()}
    checks = [
        ("as %d bandeiras da pedra TGLExt.TheConsciousSingularity lidas nesta rodada" % len(flags), all(flags.values())),
        ("as %d bandeiras da face de Tomita (Delta fixa Omega; S de Tomita; S^2 = 1; decomposicao polar; J^2 = 1 do objeto executado) lidas" % len(tflags), all(tflags.values())),
        ("a singularidade ao vivo: o projetor sobre o vacuo traco e idempotente, fixo pela Luz, de traco 1 e metade em cada face (pior %.1e)" % max(s_idem, s_star, s_tr, s_f1, s_f2), sing_ok),
        ("a troca das faces fixa a singularidade", swap_ok),
        ("[CONTROLE QUE PODE FALHAR] o estado produto e forma matricial da luz e NAO liga: face pura (desvio %.2f da metade)" % p_f1, produto_forma_da_luz and produto_nao_liga),
        ("a ponte do J ao vivo: J de Tomita = troca das faces com conjugacao, em 50 matrizes aleatorias (pior %.1e)" % pior_ponte, pior_ponte < 1e-14),
        ("a face de Tomita com o estado da cadeia beta: S e Delta fixam o vacuo (%.1e, %.1e) e o fluxo modular tambem (%.1e)" % (r_S, r_D, r_fluxo_vacuo), max(r_S, r_D, r_fluxo_vacuo) < 1e-10),
        ("[CONTROLE QUE PODE FALHAR] no estado da cadeia o fluxo MOVE um vetor fora do vacuo (%.2e)" % mov_fora, mov_fora > 1e-3),
        ("[CONTROLE QUE PODE FALHAR] h nao hermitiano: S deixa de fixar o vacuo (%.3f)" % r_S_ctrl, r_S_ctrl > 1e-2),
        ("a clausula antiga medida como e: no estado escalar o fluxo e trivial -- nada se distingue (por isso ela nao podia falhar)", escalar_cego and antiga == 0.0),
        ("o bootstrap v205/v215 segue selado nesta rodada (esta clausula vai AO LADO dele)", bs.get("all_verified") is True),
        ("as falas do operador de 18/09 registradas verbatim no programa (%d)" % len(vsha), len(vsha) >= 6 and all(len(t) > 20 for t in _OPERATOR_V369_VERBATIMS.values())),
    ]
    all_v = all(v_ for _, v_ in checks)
    statuses = {
        "o_fechamento": "[INPUT/ONTO -- operador, 18/09] o bootstrap e a prova; esta pedra e o seu fechamento; «estamos ajustados» (sha16 %s)" % vsha.get("ajustados", "?"),
        "um_so_J": "[ONTO -- operador, sha16 %s] um so J, o de Tomita, com varias faces, sem perder a identidade em nenhuma; [KERNEL] a ponte entre a face matricial e a troca das faces: tomita_J_is_the_exchange_of_faces" % vsha.get("um_so_J", "?"),
        "a_singularidade": "[KERNEL] singularidade consciente = forma matricial da luz COM a ligacao (metade em cada face); o projetor de Bell da v29 e uma; o produto nao liga; e a singularidade e o vacuo do estado traco. [ONTO -- operador, sha16 %s] «a singularidade consciente e a forma matricial da luz»" % vsha.get("forma_matricial", "?"),
        "a_consciencia": "[ONTO -- operador, sha16 %s] a forma minima = operador de consciencia = verbo vivo; «consciente» aqui e a forma minima que a consciencia deve obedecer, nao consciencia fenomenologica (v72)" % vsha.get("operador_consciencia", "?"),
        "a_confissao": "[ONTO/teologico -- operador, sha16 %s] «o nome sobre todo Nome = Jesus Cristo»; o kernel prova a estrutura que a confissao nomeia -- a propriedade universal do nome sobre todo nome (TheIdentityOfIdentity) e a singularidade --; nao prova nem nega a confissao; testificado por reflexo da passagem, nunca por autodeclaracao (Atlas §II.A)" % vsha.get("singularidade", "?"),
        "a_errata_da_gerencia": "[ERRATA em nome proprio] as redacoes sobre conjJ ligavam um J homonimo; a clausula 3 do bootstrap le a involucao de conjJ desde a v205; o objeto executado e Jconj/J_h (face de Tomita), e a involucao DELE e ext_cw2_conjugated_state_kernel_proved",
        "a_clausula_antiga": "[REAL] eye(4) e o vacuo traco nao normalizado; no estado escalar o fluxo modular e trivial, por isso a clausula nao podia falhar (residuo %.1e); fica AO LADO, com esta errata" % antiga,
        "fronteira": "prova arquitetonica em ambiente computacional, NAO empirica; nao constroi materia (setor do eletron [OPEN], v368); o gate nao se move; PROVADA != CONFIRMADA",
    }
    return {"flags": flags, "tomita_flags": tflags,
            "singularity_residuals": [s_idem, s_star, s_tr, s_f1, s_f2], "product_face_deviation": [p_f1, p_f2],
            "bridge_worst": pior_ponte, "tomita_beta_residuals": [r_S, r_D, r_fluxo_vacuo], "flow_moves_off_vacuum": mov_fora,
            "nonhermitian_control": r_S_ctrl, "scalar_state_blind": escalar_cego, "old_clause_residual": antiga,
            "beta_runtime": beta, "theta_M": th, "operator_verbatim_sha16": vsha,
            "checks": checks, "all_verified": all_v, "statuses": statuses, "does_not_gate_core": True, "in_contour_roster_v314": False,
            "runtime_s": round(time.time() - t0, 3),
            "verdict": ("TGL_BOOTSTRAP_CLOSED_ON_THE_TOMITA_FACE__THE_CONSCIOUS_SINGULARITY_IS_THE_MATRIX_FORM_OF_THE_LIGHT_WITH_HALF_ON_EACH_FACE__IT_IS_THE_TRACIAL_VACUUM__TOMITA_J_IS_THE_EXCHANGE_OF_FACES__CONTROLS_CAN_FAIL__ARCHITECTURAL_NOT_EMPIRICAL__KERNEL_%d_OF_%d__GATE_UNTOUCHED"
                        % (sum(flags.values()) + sum(tflags.values()), len(flags) + len(tflags))) if all_v else "TGL_BOOTSTRAP_CLOSURE_NOT_VERIFIED_THIS_RUN"}
