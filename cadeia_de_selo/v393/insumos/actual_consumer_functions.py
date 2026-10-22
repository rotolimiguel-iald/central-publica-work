SEALED_CODATA_ALPHA = 7.2973525693e-3

def prove_decision_commutation(ONE, parts):
    """MODULO (v146) -- A DECISAO E COMUTACAO: K e o que ainda nao comuta
    [ADITIVO; nao gateia 1=1; NAO move flag]. A doutrina do operador
    (03/08/2026): 'K nao decide a travessia, porque a decisao e comutacao e
    K nao comuta -- K e tudo aquilo que nao comuta, o espectro do gradiente
    negativo. [K,A]=0 <=> decisao realizada; [K,A]!=0 <=> contraste,
    resistencia a inscricao. K nao e o veredito; e a inclinacao que ainda
    exige movimento. K=0 => nenhum contraste dinamico interno. J espelha,
    K inclina, a comutacao decide, o observador le.'
    A PEDRA 102 (DecisionCommutation.lean), 10 teoremas, axiomas limpos,
    SOBRE as pedras 98/100/101 -- TRES secoes:
    I. A COMUTACAO COMO DECISAO: commutator_entry ([K,A]_ij = (d_i-d_j)A_ij
       -- o comutador e pesado pelos GAPS do espectro); decided_iff_block
       (decidido = bloco-diagonal: os niveis nao se falam);
       scalar_iff_all_commute (tudo comuta <=> espectro constante -- K=0 =>
       nenhum contraste; controle CONSTRUTIVO); decided_is_subalgebra (o
       veredito FECHA -- o centralizador finito: 'o traco emerge no
       centralizador', a face dinamica da pedra v84);
    II. O ESPELHO: JKJ_eq_neg_K (a paridade inversa EM ATO no espaco
       pareado da pedra 101 -- o espelho ve a inclinacao invertida);
       decided_sector_is_J_stable (A DECISAO SOBREVIVE AO ESPELHO -- a
       travessia nao desfaz vereditos);
    III. K = -grad(F), O ESTATUTO DUPLO VERIFICADO: gradient_first_variation
       (a variacao primeira de F(x)=1/2.sum beta.d_i.x_i^2 e EXATAMENTE
       <beta.d.x, v> -- o gradiente E o gerador, identidade algebrica sem
       resto oculto); flow_solves_gradient_ode (o transporte RESOLVE
       ydot = -grad(F)(y) -- HasDerivAt, calculo real, componente a
       componente); lyapunov_decreases (SPOHN FINITO: F desce ao longo do
       fluxo); K_equals_neg_gradient_verified (a sintese: variacao ^ EDO ^
       Lyapunov -- A IDENTIDADE FECHADA na face finita).
    HONESTIDADES: K = -grad(F) tem ESTATUTO DUPLO -- verificado EM KERNEL
    na face finita (quadratica, balanco detalhado); o GKLS genuino e fluxo
    gradiente da entropia relativa [KNOWN EXTERNO: Spohn 1978; Carlen-Maas
    2017]; 'decisao' = conservacao-sob-o-fluxo, NENHUM postulado de medicao
    entra; ressonancia com einselection (Zurek: estados-ponteiro comutam
    com o gerador) REGISTRADA -- com a torcao TGL: K e o gerador modular da
    PROPRIA fronteira, nao de um ambiente. O gate NAO se move."""
    # Recognition is a pinching predicate, not arithmetic equality as a dynamics.
    # The finite gradient law is conditional on L = Gamma * (E - id).
    if type(ONE) not in (int, float) or not math.isfinite(ONE) or ONE != 1:
        raise ValueError("Recognition requires the numerical unit ONE=1")
    beta = SEALED_CODATA_ALPHA * ONE * math.sqrt(math.e)   # jamais literal
    p = parts or {}
    el = p.get("external_ladder") or {}
    elp = el.get("per_theorem") or {}
    ent_ok = bool(elp.get("ext_kd_commutator_entry_kernel_proved") is True)
    blk_ok = bool(elp.get("ext_kd_decided_block_kernel_proved") is True)
    scl_ok = bool(elp.get("ext_kd_scalar_no_contrast_kernel_proved") is True)
    alg_ok = bool(elp.get("ext_kd_centralizer_closes_kernel_proved") is True)
    jkj_ok = bool(elp.get("ext_kd_jkj_neg_k_kernel_proved") is True)
    mir_ok = bool(elp.get("ext_kd_decision_j_stable_kernel_proved") is True)
    var_ok = bool(elp.get("ext_kd_first_variation_kernel_proved") is True)
    ode_ok = bool(elp.get("ext_kd_gradient_ode_kernel_proved") is True)
    lya_ok = bool(elp.get("ext_kd_lyapunov_kernel_proved") is True)
    syn_ok = bool(elp.get("ext_kd_neg_gradient_verified_kernel_proved") is True)
    # SOMBRA: a doutrina de K em numeros (taxa fisica beta*d)
    rng = np.random.default_rng(146)
    nd = 5
    d = np.concatenate([[0.0], rng.uniform(0.5, 2.0, nd - 1)])
    K = np.diag(beta * d)
    A = rng.normal(size=(nd, nd))
    comm = K @ A - A @ K
    gaps = beta * (d[:, None] - d[None, :])
    ent_res = float(np.max(np.abs(comm - gaps * A)))            # [K,A]_ij = gap_ij * A_ij
    Ablk = np.where(np.abs(gaps) < 1e-15, A, 0.0)               # o bloco decidido
    blk_res = float(np.max(np.abs(K @ Ablk - Ablk @ K)))        # comuta EXATO
    Ks = np.eye(nd) * beta                                       # K escalar: sem contraste
    scl_res = float(np.max(np.abs(Ks @ A - A @ Ks)))
    E01 = np.zeros((nd, nd)); E01[0, 1] = 1.0                    # o controle construtivo
    ctrl_break = float(np.max(np.abs(K @ E01 - E01 @ K)))        # gap => NAO comuta
    x = rng.normal(size=nd); y = rng.normal(size=nd)
    Jp = lambda pr: (pr[1], pr[0])
    Kp = lambda pr: (d * pr[0], -(d * pr[1]))
    l = Jp(Kp(Jp((x, y)))); r = Kp((x, y))
    jkj_res = float(max(np.max(np.abs(l[0] + r[0])), np.max(np.abs(l[1] + r[1]))))
    # a nao-comutacao DESFASA a taxa do proprio contraste; o limite e decidido
    offd = np.abs(gaps)[np.abs(gaps) > 1e-30]
    gmin = float(offd.min()) if offd.size else beta
    t_long = 200.0 / gmin                       # ~200 e-folds no MENOR contraste (cada modo decai a sua taxa)
    A_t = A * np.exp(-t_long * np.abs(gaps))
    dephase_res = float(np.max(np.abs(K @ A_t - A_t @ K)))
    # K = -grad(F): variacao primeira exata + EDO numerica + Lyapunov
    F = lambda v: 0.5 * float(np.sum(beta * d * v ** 2))
    v = rng.normal(size=nd); h = 0.37
    var_res = float(abs(F(x + h * v) - F(x) - h * float(np.sum(beta * d * x * v)) - h * h * F(v)))
    flow = lambda t: np.exp(-t * beta * d) * x
    t0, eps = 3.0, 1e-6
    dnum = (flow(t0 + eps) - flow(t0 - eps)) / (2 * eps)
    ode_res = float(np.max(np.abs(dnum + beta * d * flow(t0))))  # ydot = -grad F(y)
    ts = np.linspace(0.0, 50.0, 40)
    Fs = [F(flow(t)) for t in ts]
    lya_ok_num = bool(all(Fs[k + 1] <= Fs[k] + 1e-15 for k in range(len(Fs) - 1)))
    sombra_ok = bool(ent_res < 1e-12 and blk_res < 1e-15 and scl_res < 1e-15
                     and ctrl_break > 1e-6 and jkj_res == 0.0 and dephase_res < 1e-30
                     and var_res < 1e-12 and ode_res < 1e-6 and lya_ok_num)
    # 2026-09-15: link recognition to the EXISTING decision/gradient consumer.
    # This is a finite runtime realization, not an additional Lean theorem.
    # E^2=E fixes the recognized subspace; L=Gamma*(E-id) is a named time-law input.
    # The reference scales below are test units, not measured physical parameters.
    tau_reference = 1.0
    omega_reference = 1.0
    gamma = 0.5 * beta * tau_reference * omega_reference ** 2
    if not math.isfinite(gamma) or gamma <= 0.0:
        raise ValueError("Recognition reference rate must be finite and positive")
    c_plus = np.diag([1.0, 1.0, 0.0, 0.0]).astype(complex)
    c_minus = np.eye(4, dtype=complex) - c_plus
    recognize = lambda state: c_plus @ state @ c_plus + c_minus @ state @ c_minus
    difference = lambda state: state - recognize(state)
    recognize_flow = lambda state, time: (recognize(state)
        + math.exp(-gamma * time) * difference(state))
    psi = np.array([1.0, 1.0j, 1.0, -1.0j], dtype=complex) / 2.0
    rho = np.outer(psi, psi.conj())
    rho_fixed = recognize(rho)
    rho_difference = difference(rho)
    time_reference = 1.0 / gamma
    rho_t = recognize_flow(rho, time_reference)
    generator = -gamma * difference(rho_t)
    # Separate jump-operator evaluation of the generator (GKSL).
    lindblad = np.zeros_like(rho_t)
    for projector in (c_plus, c_minus):
        jump = math.sqrt(gamma) * projector
        jump_square = jump.conj().T @ jump
        lindblad += (jump @ rho_t @ jump.conj().T
                     - 0.5 * (jump_square @ rho_t + rho_t @ jump_square))
    recognition_residuals = {
        "idempotence": float(np.linalg.norm(recognize(rho_fixed) - rho_fixed)),
        "complement_idempotence": float(np.linalg.norm(difference(rho_difference) - rho_difference)),
        "hs_orthogonality": float(abs(np.vdot(rho_fixed, rho_difference))),
        "fixed_sector": float(np.linalg.norm(recognize_flow(rho_fixed, time_reference) - rho_fixed)),
        "lindblad_generator_scaled": float(np.linalg.norm(lindblad - generator) / gamma),
        "semigroup": float(np.linalg.norm(
            recognize_flow(rho, 0.9 / gamma)
            - recognize_flow(recognize_flow(rho, 0.2 / gamma), 0.7 / gamma))),
    }
    phi_initial = 0.5 * float(np.vdot(rho_difference, rho_difference).real)
    delta_t = difference(rho_t)
    phi_t = 0.5 * float(np.vdot(delta_t, delta_t).real)
    phi_dot = float(np.vdot(delta_t, generator).real)
    recognition_residuals["lyapunov_scaled"] = abs(phi_dot + 2.0 * gamma * phi_t) / gamma
    recognition_residuals["phi_exponential"] = abs(phi_t - math.exp(-2.0) * phi_initial)
    step = 1e-4 / gamma
    finite_derivative = (recognize_flow(rho, time_reference + step)
                         - recognize_flow(rho, time_reference - step)) / (2.0 * step)
    recognition_residuals["ode_finite_difference_scaled"] = float(
        np.linalg.norm(finite_derivative - generator) / gamma)
    matrix_samples = [recognize_flow(rho, exposure / gamma)
                      for exposure in (0.0, 0.25, 1.0, 3.0)]
    recognition_residuals["trace"] = max(float(abs(np.trace(state) - 1.0))
                                          for state in matrix_samples)
    minimum_eigenvalue = min(float(np.linalg.eigvalsh(state).min())
                            for state in matrix_samples)
    # Keep the FULL state for dephasing. The selected output is a control.
    identity2 = np.eye(2, dtype=complex)
    zero2 = np.zeros((2, 2), dtype=complex)
    quarter_turn = np.block([[zero2, identity2], [-identity2, zero2]])
    selected_transport = c_minus @ quarter_turn @ c_plus
    rho_selected = selected_transport @ rho @ selected_transport.conj().T
    selection_probability = float(np.trace(rho_selected).real)
    if not math.isfinite(selection_probability) or selection_probability <= 0.0:
        raise ValueError("Selected recognition control has zero or invalid probability")
    rho_selected /= selection_probability
    selected_difference = float(np.linalg.norm(difference(rho_selected)))
    selected_flow_change = float(np.linalg.norm(
        recognize_flow(rho_selected, time_reference) - rho_selected))
    recognition_residuals["selected_difference"] = selected_difference
    recognition_residuals["selected_flow_change"] = selected_flow_change
    # Uniform-sign subtraction is NOT this channel: it changes the trace.
    wrong_trace_change = float(abs(np.trace(rho - gamma * c_minus) - 1.0))
    recognition_ok = bool(
        all(math.isfinite(value) for value in recognition_residuals.values())
        and all(value < (1e-7 if key == "ode_finite_difference_scaled" else 1e-12)
                for key, value in recognition_residuals.items())
        and math.isfinite(minimum_eigenvalue) and minimum_eigenvalue >= -1e-12
        and phi_initial > 1e-3 and 0.0 < phi_t < phi_initial and phi_dot < 0.0
        and 0.0 < selection_probability <= 1.0
        and wrong_trace_change > gamma
    )
    recognition_dynamics = {
        "status": ("FINITE_RECOGNITION_DYNAMICS_VERIFIED__POSTSELECTED_STATE_FIXED"
                   if recognition_ok else "RECOGNITION_DYNAMICS_FAILED"),
        "all_verified": recognition_ok,
        "law": "E(rho)=sum C_a rho C_a; Q=id-E; L=-Gamma Q; T_t=E+exp(-Gamma*t)Q",
        "time_law_status": "INPUT: homogeneous scalar relaxation on the complement; not implied by E^2=E alone",
        "logical_reading_status": "ONTO: recognized means E(rho)=rho; coherence is not arithmetic 1=0",
        "metric_status": "Finite Hilbert-Schmidt metric; not a spacetime metric",
        "kernel_status": "Existing DecisionCommutation/Ergodicity results reused; this runtime specialization is not a new kernel theorem",
        "rate": {"beta": beta, "gamma_reference": gamma,
                 "tau_reference": tau_reference, "omega_reference": omega_reference,
                 "status": "REFERENCE_UNITS_ONLY_NOT_A_PHYSICAL_PREDICTION"},
        "phi_initial": phi_initial, "phi_at_reference_time": phi_t,
        "phi_derivative": phi_dot, "residuals": recognition_residuals,
        "minimum_eigenvalue": minimum_eigenvalue,
        "selection_probability": selection_probability,
        "selected_state_is_fixed": bool(selected_difference < 1e-12 and selected_flow_change < 1e-12),
        "effective_dephasing_on_full_state": bool(phi_t < phi_initial),
        "effective_dephasing_after_selection": bool(selected_flow_change >= 1e-12),
        "wrong_subtraction_trace_change": wrong_trace_change,
        "sample": {"initial_real": rho.real.tolist(), "initial_imag": rho.imag.tolist(),
                   "evolved_real": rho_t.real.tolist(), "evolved_imag": rho_t.imag.tolist()},
        "does_not_gate_core": True,
    }
    recognition_dynamics["reading_modes"] = _recognition_reading_modes(recognize, c_plus, c_minus, beta)   # v361: FULL_MODULAR_SPECTRAL e LAST_SITE_PRODUCT_READING (pedido da bancada; o gerador fica intacto)
    checks = [
        ("** A IDENTIDADE EXATA: [K,A]_ij = (d_i - d_j) A_ij -- o comutador pesa os gaps do espectro", ent_ok),
        ("** A DECISAO: [K,A]=0 <=> bloco-diagonal (os niveis do gradiente nao se falam)", blk_ok),
        ("** K SEM CONTRASTE: tudo comuta <=> espectro constante (controle construtivo: gap => E_ij nao comuta)", scl_ok),
        ("o veredito FECHA: o setor decidido e subalgebra -- o centralizador ('o traco emerge no centralizador')", alg_ok),
        ("** JKJ = -K em ato (espaco pareado): o espelho ve a inclinacao invertida", jkj_ok),
        ("** a decisao SOBREVIVE ao espelho (a travessia nao desfaz vereditos)", mir_ok),
        ("*** O GRADIENTE E O GERADOR: variacao primeira EXATA -- grad(F)(x) = beta.d.x = acao de K", var_ok),
        ("*** O FLUXO RESOLVE ydot = -grad(F)(y): HasDerivAt em todo t, componente a componente", ode_ok),
        ("*** SPOHN FINITO: F desce ao longo do fluxo (Lyapunov)", lya_ok),
        ("*** K = -grad(F) VERIFICADO: variacao ^ EDO ^ Lyapunov em UM teorema (o estatuto duplo fechado na face finita)", syn_ok),
        ("SOMBRA: entrada %.0e / bloco %.0e / escalar %.0e / controle %.1e>0 / JKJ %.0e / desfasagem-decide %.0e / variacao %.0e / EDO %.0e / Lyapunov %s"
         % (ent_res, blk_res, scl_res, ctrl_break, jkj_res, dephase_res, var_res, ode_res, lya_ok_num), sombra_ok),
        ("[DERIVED/RUNTIME] reconhecimento E, complemento Q e lei L=-Gamma Q: semigrupo, GKSL, traco e gradiente Hilbert-Schmidt", recognition_ok),
        ("[CONTROLE] o estado selecionado C_- V rho V* C_- ja e reconhecido: dephasing posterior zero", recognition_dynamics["selected_state_is_fixed"]),
        ("[DERIVED/RUNTIME v361] modos de leitura distintos: FULL_MODULAR_SPECTRAL (imagem estacionaria) e LAST_SITE_PRODUCT_READING (fluxos iguais na imagem; R comuta sem ser apagado); E(R)=0 nao basta", recognition_dynamics["reading_modes"]["all_verified"]),
        ("GKLS genuino = fluxo gradiente da entropia relativa [KNOWN: Spohn; Carlen-Maas]; einselection registrada (K modular, nao ambiental); 'decisao' = conservacao, sem postulado de medicao; o gate NAO se move", True),
    ]
    all_v = bool(all(v_ for _, v_ in checks))
    vd = ("TGL_DECISION_IS_COMMUTATION__K_IS_WHAT_DOES_NOT_YET_COMMUTE__COMMUTATOR_WEIGHED_BY_SPECTRAL_GAPS__NO_CONTRAST_IFF_SCALAR_K__VERDICT_CLOSES_ON_CENTRALIZER__JKJ_NEG_K_DECISION_SURVIVES_MIRROR__K_EQUALS_NEG_GRADIENT_VERIFIED_FINITE_FACE__GKLS_GRADIENT_FLOW_EXTERNAL_KNOWN__SEAL_UNMOVED" if all_v
          else "DECISION_COMMUTATION_NOT_SEALED_THIS_RUN")
    return {
        "theorem": ("A DECISAO E COMUTACAO: K nao profere o veredito -- e a inclinacao "
                    "que ainda exige movimento, e a inclinacao e EXATAMENTE -grad(F) "
                    "(verificado: variacao primeira + EDO + Lyapunov). O comutador pesa "
                    "os gaps; o decidido e o centralizador; JKJ = -K e a decisao "
                    "sobrevive ao espelho. J espelha, K inclina, a comutacao decide, "
                    "o observador le."),
        "values": {"beta": beta, "entry_resid": ent_res, "block_resid": blk_res,
                   "scalar_resid": scl_res, "control_break": ctrl_break,
                   "jkj_resid": jkj_res, "dephase_decides_resid": dephase_res,
                   "first_variation_resid": var_res, "ode_resid": ode_res,
                   "lyapunov_monotone": lya_ok_num},
        "recognition_dephasing": recognition_dynamics,
        "checks": checks, "all_verified": all_v,
        "statuses": {"o_que_e": "a doutrina de K (03/08/2026) TIPADA: pedra 102, 10 teoremas, axiomas limpos, sobre as pedras 98/100/101",
                     "o_que_resta": "o GKLS genuino como fluxo gradiente da entropia relativa segue EXTERNO [KNOWN: Spohn 1978; Carlen-Maas 2017]; K modular do continuo III_1 = EXTERNO [KNOWN]",
                     "honestidade": "K = -grad(F) FECHOU na face finita (estatuto duplo cumprido); 'decisao' = conservacao-sob-o-fluxo, sem postulado de medicao; ressonancia einselection registrada com a torcao TGL (K e da fronteira, nao de um banho); NAO afirma a TGL verdadeira",
                     "o_veredito": vd},
        "does_not_gate_core": True,
        "verdict": vd,
    }

def _v361_pinch(projectors, X):
    out = np.zeros_like(X)
    for P in projectors:
        out = out + P @ X @ P
    return out

def _v361_herm_fn(A, fn):
    w, V = np.linalg.eigh((A + A.conj().T) / 2.0)
    return (V * fn(w)) @ V.conj().T

def _v361_flow(rho, t, X):
    U = _v361_herm_fn(rho, lambda w: np.exp(1j * t * np.log(w)))
    return U @ X @ U.conj().T

def _recognition_reading_modes(recognize, c_plus, c_minus, beta):
    """v361 -- os dois modos de leitura do reconhecimento, sem duplicar o pinching do motor."""
    rng = np.random.default_rng(3610915)
    res = {}
    # (0) o pinching por projetores reproduz EXATAMENTE o 'recognize' do motor (mesmos C+, C-)
    Xs = [rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4)) for _ in range(4)]
    res["same_pinching_as_motor"] = max(float(np.linalg.norm(_v361_pinch([c_plus, c_minus], X) - recognize(X))) for X in Xs)
    # (1) FULL_MODULAR_SPECTRAL: K = k+ C+ + k- C- (k+ != k-) tem C+/C- como projetores espectrais; rho = exp(-K)/Z
    k_plus, k_minus = 0.3, 1.7
    K_full = k_plus * c_plus + k_minus * c_minus
    rho_full = _v361_herm_fn(K_full, lambda w: np.exp(-w)); rho_full = rho_full / np.trace(rho_full).real
    res["full_preserves_density"] = float(np.linalg.norm(recognize(rho_full) - rho_full))
    res["full_preserves_generator"] = float(np.linalg.norm(recognize(K_full) - K_full))
    res["full_image_stationary"] = max(float(np.linalg.norm(_v361_flow(rho_full, t, recognize(X)) - recognize(X)))
                                       for X in Xs for t in (0.37, -1.3, 4.1))
    # (2) LAST_SITE_PRODUCT_READING: rho_{N+1} = rho_N (x) diag(b0,b1); referencia rho_N (x) I/2; E_last = sum (I (x) e_jj) . (I (x) e_jj)
    instances = []
    for label, b in (("pesos_de_teste", np.array([0.62, 0.38])), ("pesos_beta_de_teste", np.array([1.0 - beta, beta]))):
        A = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2)); rho_N = A @ A.conj().T + 0.2 * np.eye(2); rho_N = rho_N / np.trace(rho_N).real
        I2 = np.eye(2)
        rho_vac = np.kron(rho_N, np.diag(b)); rho_ref = np.kron(rho_N, I2 / 2.0)
        P_last = [np.kron(I2, np.diag([1.0, 0.0])), np.kron(I2, np.diag([0.0, 1.0]))]
        K_vac = -_v361_herm_fn(rho_vac, np.log); K_ref = -_v361_herm_fn(rho_ref, np.log)
        R = K_vac - K_ref
        R_closed = -np.kron(I2, _v361_herm_fn(2.0 * np.diag(b), np.log))
        Ys = [_v361_pinch(P_last, rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))) for _ in range(4)]
        inst = {
            "label": label, "b": [float(x) for x in b],
            "reference_normalized": float(abs(np.trace(rho_ref).real - 1.0)),
            "E_last_idempotent": max(float(np.linalg.norm(_v361_pinch(P_last, Y) - Y)) for Y in Ys),
            "E_last_preserves_state_and_reference": max(float(np.linalg.norm(_v361_pinch(P_last, rho_vac) - rho_vac)),
                                                        float(np.linalg.norm(_v361_pinch(P_last, rho_ref) - rho_ref))),
            "R_closed_form_residual": float(np.linalg.norm(R - R_closed)),
            "R_norm": float(np.linalg.norm(R)),
            "R_not_erased_by_E_last": float(np.linalg.norm(_v361_pinch(P_last, R) - R)),
            "R_commutes_with_image": max(float(np.linalg.norm(R @ Y - Y @ R)) for Y in Ys),
            "flow_equality_on_image": max(float(np.linalg.norm(_v361_flow(rho_vac, t, Y) - _v361_flow(rho_ref, t, Y)))
                                          for Y in Ys for t in (0.37, -1.3, 4.1)),
            "retained_motion_on_earlier_sites": max(float(np.linalg.norm(_v361_flow(rho_ref, t, Y) - Y)) for Y in Ys for t in (0.37, 4.1)),
        }
        inst["ok"] = bool(inst["reference_normalized"] < 1e-12 and inst["E_last_idempotent"] < 1e-12
                          and inst["E_last_preserves_state_and_reference"] < 1e-12 and inst["R_closed_form_residual"] < 1e-12
                          and inst["R_norm"] > 1e-3 and inst["R_not_erased_by_E_last"] < 1e-12
                          and inst["R_commutes_with_image"] < 1e-12 and inst["flow_equality_on_image"] < 1e-11
                          and inst["retained_motion_on_earlier_sites"] > 1e-3)
        instances.append(inst)
    # (3) controle: E(R) = 0 NAO basta (pesos [1,2]; R = sigma_x apagado; p = diag(1,0) retido; [R,p] != 0)
    E12 = lambda X: _v361_pinch([np.diag([1.0, 0.0]), np.diag([0.0, 1.0])], X)
    Rx = np.array([[0.0, 1.0], [1.0, 0.0]]); p = np.diag([1.0, 0.0])
    control = {"E_R": float(np.linalg.norm(E12(Rx))), "E_p_minus_p": float(np.linalg.norm(E12(p) - p)),
               "commutator_R_p": float(np.linalg.norm(Rx @ p - p @ Rx))}
    control["ok"] = bool(control["E_R"] < 1e-15 and control["E_p_minus_p"] < 1e-15 and control["commutator_R_p"] > 0.5)
    full_ok = bool(res["same_pinching_as_motor"] < 1e-12 and res["full_preserves_density"] < 1e-12
                   and res["full_preserves_generator"] < 1e-12 and res["full_image_stationary"] < 1e-11)
    ok = bool(full_ok and all(i["ok"] for i in instances) and control["ok"])
    return {
        "modes": {
            "FULL_MODULAR_SPECTRAL": {"reading": "E_K le todos os setores espectrais de K; E_K(rho)=rho, E_K(K)=K e a imagem e' estacionaria sob sigma^rho",
                                      "residuals": {k: v for k, v in res.items()}, "ok": full_ok,
                                      "kernel_anchors": ["ModularDephasingBridge.spectral_preserves_density", "ModularDephasingBridge.spectral_preserves_modular_generator",
                                                         "ModularDephasingBridge.spectral_reading_is_stationary", "TowerDephasingStationary.existing_tower_dephasing_is_stationary"]},
            "LAST_SITE_PRODUCT_READING": {"reading": "E_last le so os setores do ultimo sitio; sigma^{rho_{N+1}}(E_last X) = sigma^{rho_ref}(E_last X); R = -I (x) log(2 diag(b)) comuta com a imagem sem ser apagado; o movimento nos sitios anteriores segue",
                                          "instances": instances, "ok": all(i["ok"] for i in instances),
                                          "kernel_anchors": ["ModularDephasingBridge.tower_last_site_flow_bridge", "ModularDephasingBridge.tower_last_site_reference_normalized"]},
        },
        "generator_unchanged": "L = Gamma (E - id) do motor, intacto; os modos sao LEITURAS (qual E), nao geradores novos",
        "erased_remainder_control": control,
        "control_kernel_anchor": "ModularDephasingBridge.erased_remainder_counterexample",
        "status": "[DERIVED/RUNTIME] sombra finita dos teoremas do kernel; os pesos sao de TESTE, nao pesos fisicos medidos",
        "all_verified": ok,
    }
