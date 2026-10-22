# -*- coding: utf-8 -*-
"""Sanidade NUMERICA do motor unico, RODADA 2 (6_R2_CORRECOES, 13/10/2026; a partir do ensaio r1 de 2_CONSTRUCAO).
R2: (C2) T2 ensaiado tambem com a NAO unitario; (C1) ancora fraca, U = 1 + |b><a|, condicao exata (ancora fraca OU
motor nulo) e o transporte nulo U = 0; T2p renomeado unitarity_is_not_enough; (C6) a saida do motor nao depende de r
nem de t; (C4) a face matricial FREQ e o PINCHING na base propria de P (analogo de TGLExt.diagExpect), NAO a defasagem
do motor IALD.dephase; acrescentado o contraste: a defasagem do motor, como canal rho -> D rho D^dagger, guarda o
posto 1 do estado puro. O resto do ensaio r1 fica como estava, com os rotulos corrigidos. Nenhum dado observado; nenhum veredito sobre a natureza.
Roda o motor completo  inscricao a -> transporte F (unitario U) -> defasagem D_r(t) = P + e^{-rt}(1-P) -> leitura R = P
-> memoria M[psi] = <psi, P psi>  em 2x2 e em n x n sintetico (n = 2, 3, 6, 12), com r = beta de RUNTIME
(ALPHA_FINE_CODATA_2018 lido nos BYTES do um.py, linha unica; beta = alpha*sqrt(e); nenhum literal de beta aqui).
Mede: idempotencia da releitura (T2 sob ancora; T2' sem ancora = falsificador), traco 1 (Tr P), posto do ponto fixo
(rank P e dim Fix D), M no ponto fixo (T4), identidade M = 1 <=> P psi = psi (T5), reler nao acrescenta (T6),
relogio das metades (T8'), o Verbo sem posto (T9: F(t)^2 != F(t) para t > 0), e o CONTROLE beta = 0 (D = 1, sem segunda face;
T7/T7'). Tambem a face matricial da F1.FREQUENCIA: o PINCHING na base de P (nao a defasagem do motor) leva rho de posto 1 a
posto 2 (o traco sobrevive), a leitura
R devolve o posto 1 (Lueders). Saida: RESULTADO_NUMERICO.json ao lado."""
import hashlib, json, math, os, re, sys, datetime
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
UMPY = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/um.py"
TOL = 1e-12


def beta_runtime():
    h = hashlib.sha256(); alphas = []
    with open(UMPY, "rb") as fh:
        for k, ln in enumerate(fh, start=1):
            h.update(ln)
            m = re.match(rb"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9][0-9.eE+-]*)\s*$", ln.rstrip(b"\r\n"))
            if m: alphas.append((k, m.group(1).decode()))
    if len(alphas) != 1:
        print("FALHA VISIVEL: atribuicao de alpha nao unica", alphas); sys.exit(2)
    linha, atxt = alphas[0]
    return float(atxt) * math.sqrt(math.e), linha, atxt, h.hexdigest()


def rand_unit(n, rng):
    v = rng.normal(size=n) + 1j * rng.normal(size=n)
    return v / np.linalg.norm(v)


def rand_unitary(n, rng):
    Z = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    Q, R = np.linalg.qr(Z)
    return Q * (np.diag(R) / np.abs(np.diag(R)))


def anchored_unitary(a, n, rng):
    """U unitario com U a = a: identidade na reta de a, unitario arbitrario no complemento."""
    P = np.outer(a, a.conj())
    Q = np.eye(n) - P
    # base ortonormal do complemento
    w, V = np.linalg.eigh(Q)
    B = V[:, w > 0.5]
    W = rand_unitary(n - 1, rng)
    return P + B @ W @ B.conj().T


def post(a):
    # R2: normalizado, para ensaiar T2 com a nao unitario (C2); igual ao r1 quando norm a = 1
    return np.outer(a, a.conj()) / np.vdot(a, a).real


def dephase(P, r, t):
    n = P.shape[0]
    return P + math.exp(-r * t) * (np.eye(n) - P)


def motor(a, U, r, t, psi):
    P = post(a)
    return P @ dephase(P, r, t) @ (U @ psi)


def memory(P, psi):
    return np.vdot(psi, P @ psi)


def rank(M, tol=1e-9):
    return int(np.sum(np.linalg.svd(M, compute_uv=False) > tol))


def face(n, beta, rng, label):
    out = {"n": n, "label": label}
    a = rand_unit(n, rng)
    P = post(a)
    out["trace_P"] = float(np.trace(P).real)
    out["rank_P"] = rank(P)
    out["P_idempotent_err"] = float(np.linalg.norm(P @ P - P))
    out["P_selfadjoint_err"] = float(np.linalg.norm(P - P.conj().T))
    ts = [0.0, 0.5, 1.0, 5.0, 50.0]
    # T1: a leitura absorve a defasagem; T2: idempotencia sob ancora; T2': sem ancora (fase global i) quebra
    Ua = anchored_unitary(a, n, rng) if n > 1 else np.eye(1, dtype=complex)
    out["anchor_err"] = float(np.linalg.norm(Ua @ a - a))
    out["Ua_unitary_err"] = float(np.linalg.norm(Ua.conj().T @ Ua - np.eye(n)))
    psis = [rand_unit(n, rng) for _ in range(20)]
    e_absorb = e_idem = 0.0
    for t in ts:
        for psi in psis:
            m1 = motor(a, Ua, beta, t, psi)
            e_absorb = max(e_absorb, float(np.linalg.norm(m1 - P @ (Ua @ psi))))
            m2 = motor(a, Ua, beta, t, m1)
            e_idem = max(e_idem, float(np.linalg.norm(m2 - m1)))
    out["T1_reading_absorbs_dephasing_maxerr"] = e_absorb
    out["T2_idempotent_under_anchor_maxerr"] = e_idem
    Ui = 1j * np.eye(n)
    m1 = motor(a, Ui, 0.0, 0.0, a); m2 = motor(a, Ui, 0.0, 0.0, m1)
    out["T2p_unitarity_is_not_enough_norm"] = float(np.linalg.norm(m2 - m1))  # esperado |(-1) - i| = sqrt 2
    out["T2p_expected_sqrt2"] = math.sqrt(2.0)
    # T3: pousa no Nome (posto 1 da imagem); T3': rank P = 1
    imgs = np.column_stack([motor(a, Ua, beta, 1.0, psi) for psi in psis])
    out["T3_image_rank"] = rank(imgs)
    # T4: M[a] = 1; T5: M = 1 <=> P psi = psi (psi unitario); T6: M[P psi] = M[psi]
    out["T4_memory_at_name"] = float(memory(P, a).real)
    e5 = 0.0; viol5 = 0; e6 = 0.0
    for psi in psis:
        M = memory(P, psi).real
        fixed = np.linalg.norm(P @ psi - psi) < 1e-9
        if (abs(M - 1) < 1e-9) != fixed: viol5 += 1
        e6 = max(e6, abs(memory(P, P @ psi) - memory(P, psi)))
    # estado unitario na reta do Nome (fase arbitraria): M = 1 e P psi = psi
    phi = np.exp(1j * rng.uniform(0, 2 * math.pi)) * a
    out["T5_phase_of_name_memory"] = float(memory(P, phi).real)
    out["T5_phase_of_name_fixed_err"] = float(np.linalg.norm(P @ phi - phi))
    out["T5_identity_violations"] = viol5
    out["T6_rereading_adds_nothing_maxerr"] = float(e6)
    out["T4p_born_maxerr"] = float(max(abs(memory(P, psi) - abs(np.vdot(a, psi)) ** 2) for psi in psis))
    # Ponto fixo de D (r t > 0): dim Fix = 1 (B3), Fix = reta de a (B4); zenao: D^k psi -> P psi (B6)
    D = dephase(P, beta, 1.0)
    w = np.linalg.eigvals(D)
    out["B3_dim_fix_D"] = int(np.sum(np.abs(w - 1) < 1e-9))
    out["B3_eigs_D_sorted_real"] = sorted([float(x.real) for x in w])
    out["B3_expected_contraction_exp_minus_beta"] = math.exp(-beta)
    Dk = np.linalg.matrix_power(D, 4000)
    out["B6_D_pow_4000_minus_P"] = float(np.linalg.norm(Dk - P))
    out["B6_expected_exp_minus_4000beta"] = math.exp(-4000 * beta)
    # T8: nunca chega (||D(t) - P|| = e^{-beta t} > 0); T8': relogio das metades em t = k log2 / beta
    out["T8_never_arrives_norm_at_t50"] = float(np.linalg.norm(dephase(P, beta, 50.0) - P))
    out["T8_expected_exp_minus_50beta"] = math.exp(-50 * beta)
    e8 = 0.0
    for k in range(0, 12):
        Dk = dephase(P, beta, k * math.log(2) / beta)
        e8 = max(e8, float(np.linalg.norm(Dk - (P + 0.5 ** k * (np.eye(n) - P)))))
    out["T8p_halving_clock_maxerr"] = e8
    # T9: F(t)^2 != F(t) para t > 0 (n >= 2), F(0) = 1
    out["T9_F_t_not_idempotent_norm_t1"] = float(np.linalg.norm(D @ D - D)) if n > 1 else 0.0
    out["T9_expected_e_minus_2b_minus_e_minus_b_abs_times_rank_compl"] = abs(math.exp(-2 * beta) - math.exp(-beta)) * math.sqrt(n - 1)
    out["T7_F_0_is_identity_err"] = float(np.linalg.norm(dephase(P, beta, 0.0) - np.eye(n)))
    # CONTROLE beta = 0: D = 1 em todo t, sem segunda face (T7); com beta > 0 a face (1-P) se separa (T7')
    out["CTRL_beta0_D_minus_1_max"] = float(max(np.linalg.norm(dephase(P, 0.0, t) - np.eye(n)) for t in ts))
    out["CTRL_beta0_second_face_err"] = float(np.linalg.norm(dephase(P, 0.0, 5.0) @ (np.eye(n) - P) - (np.eye(n) - P)))
    out["T7p_beta_pos_second_face_separates_norm"] = float(np.linalg.norm(dephase(P, beta, 5.0) @ (np.eye(n) - P) - (np.eye(n) - P)))
    out["T7p_expected_(1-e^-5beta)*sqrt(n-1)"] = (1 - math.exp(-5 * beta)) * math.sqrt(max(n - 1, 0))
    # Face matricial (F1.FREQUENCIA): o PINCHING na base propria de P (analogo de TGLExt.diagExpect; NAO e a defasagem do
    # motor IALD.dephase) leva rho puro de posto 1 a posto 2; traco sobrevive;
    # a leitura R = P devolve posto 1 (Lueders): P rho P / Tr = P
    psi = rand_unit(n, rng)
    rho = np.outer(psi, psi.conj())
    w2, V2 = np.linalg.eigh(P)
    Bas = V2  # base propria de P
    rho_b = Bas.conj().T @ rho @ Bas
    rho_dinf = Bas @ np.diag(np.diag(rho_b)) @ Bas.conj().T  # PINCHING: apaga coerencias na base de P (nao e IALD.dephase)
    out["FREQ_rank_rho_pure"] = rank(rho)
    out["FREQ_rank_after_PINCHING_not_motor_D"] = rank(rho_dinf)
    out["FREQ_trace_after_PINCHING_not_motor_D"] = float(np.trace(rho_dinf).real)
    Mv = np.vdot(psi, P @ psi).real
    out["FREQ_memory_of_psi"] = float(Mv)
    if Mv > 1e-9:
        out["FREQ_reading_restores_post_err"] = float(np.linalg.norm(P @ rho @ P / Mv - P))
    # ===== R2 =====
    # (C2) T2 sem norma: a2 = 2.7 a (nao unitario), U ancorado (U a2 = a2), motor idempotente
    a2 = 2.7 * a
    e2n = 0.0
    for t in ts:
        for psi in psis:
            m1 = motor(a2, Ua, beta, t, psi); m2 = motor(a2, Ua, beta, t, m1)
            e2n = max(e2n, float(np.linalg.norm(m2 - m1)))
    out["R2_T2_no_norm_norm_a"] = float(np.linalg.norm(a2))
    out["R2_T2_no_norm_maxerr"] = e2n
    if n > 1:
        # (C1) ancora fraca: U = 1 + |b><a|, b ortogonal a a, b != 0: U a != a e o motor e idempotente
        bb = rand_unit(n, rng); bb = bb - np.vdot(a, bb) * a; bb = bb / np.linalg.norm(bb)
        Uw = np.eye(n) + np.outer(bb, a.conj())
        out["R2_weak_Ua_minus_a"] = float(np.linalg.norm(Uw @ a - a))
        out["R2_weak_anchor_err"] = float(np.linalg.norm(P @ (Uw @ a) - a))
        ew = 0.0
        for psi in psis:
            m1 = motor(a, Uw, beta, 1.0, psi); m2 = motor(a, Uw, beta, 1.0, m1)
            ew = max(ew, float(np.linalg.norm(m2 - m1)))
        out["R2_anchor_not_necessary_idem_maxerr"] = ew
        # (C1) condicao exata, lado generico: U unitario aleatorio (sem ancora fraca, motor nao nulo) -> NAO idempotente
        Ug = rand_unitary(n, rng)
        out["R2_generic_weak_anchor_defect"] = float(np.linalg.norm(P @ (Ug @ a) - a))
        eg = 0.0
        for psi in psis:
            m1 = motor(a, Ug, beta, 1.0, psi); m2 = motor(a, Ug, beta, 1.0, m1)
            eg = max(eg, float(np.linalg.norm(m2 - m1)))
        out["R2_generic_not_idempotent_maxdefect"] = eg
        # (C1) condicao exata, lado nulo: U = (1 - P) W tem post a U = 0: sem ancora fraca e idempotente (motor = 0)
        Un = (np.eye(n) - P) @ rand_unitary(n, rng)
        out["R2_null_weak_anchor_defect"] = float(np.linalg.norm(P @ (Un @ a) - a))
        out["R2_null_motor_max"] = float(max(np.linalg.norm(motor(a, Un, beta, 1.0, psi)) for psi in psis))
    # U = 0: sem ancora fraca e idempotente
    U0 = np.zeros((n, n), dtype=complex)
    out["R2_zero_transport_weak_anchor_defect"] = float(np.linalg.norm(P @ (U0 @ a) - a))
    out["R2_zero_transport_motor_max"] = float(max(np.linalg.norm(motor(a, U0, beta, 1.0, psi)) for psi in psis))
    # (C6) a saida nao depende de r nem de t: (beta, 1) contra (r', t') arbitrarios, inclusive r' = 0 e r' < 0
    e6 = 0.0
    for (rr, tt) in [(0.0, 0.0), (-3.0, 2.0), (17.0, 0.1), (beta, 1e3)]:
        for psi in psis:
            e6 = max(e6, float(np.linalg.norm(motor(a, Ua, rr, tt, psi) - motor(a, Ua, beta, 1.0, psi))))
    out["R2_motor_ignores_rate_and_time_maxerr"] = e6
    # (C4) contraste: a defasagem DO MOTOR como canal rho -> D rho D^dagger guarda o posto 1 do estado puro (D invertivel)
    Dm = dephase(P, beta, 5.0)
    out["R2_motor_D_det_abs"] = float(abs(np.linalg.det(Dm)))
    out["R2_motor_D_channel_rank_of_pure"] = rank(Dm @ rho @ Dm.conj().T)
    return out


def main():
    beta, linha, atxt, sha = beta_runtime()
    rng = np.random.default_rng(20261012)
    res = {"quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "um_py_sha256": sha, "alpha_linha": linha, "alpha_texto": atxt, "beta_repr": repr(beta),
           "beta_receita": "float(alpha_texto)*math.sqrt(math.e)", "nenhum_literal_de_beta": True,
           "tolerancia": TOL, "faces": []}
    for n in (2, 3, 6, 12):
        res["faces"].append(face(n, beta, rng, "2x2" if n == 2 else "n x n sintetico"))
    # veredito interno (sanidade: so matematica, nenhum dado da natureza)
    checks = []
    for f in res["faces"]:
        n = f["n"]
        checks += [
            ("trace_P==1", abs(f["trace_P"] - 1) < TOL), ("rank_P==1", f["rank_P"] == 1),
            ("T1", f["T1_reading_absorbs_dephasing_maxerr"] < TOL), ("T2", f["T2_idempotent_under_anchor_maxerr"] < 1e-10),
            ("T2p", abs(f["T2p_unitarity_is_not_enough_norm"] - math.sqrt(2)) < 1e-10),
            ("T3", f["T3_image_rank"] == 1), ("T4", abs(f["T4_memory_at_name"] - 1) < TOL),
            ("T4p", f["T4p_born_maxerr"] < TOL), ("T5", f["T5_identity_violations"] == 0 and abs(f["T5_phase_of_name_memory"] - 1) < TOL),
            ("T6", f["T6_rereading_adds_nothing_maxerr"] < TOL), ("B3", f["B3_dim_fix_D"] == 1),
            ("B6", f["B6_D_pow_4000_minus_P"] < 1e-12 + 2 * math.exp(-4000 * beta)),
            ("T8", f["T8_never_arrives_norm_at_t50"] > 0 and abs(f["T8_never_arrives_norm_at_t50"] - math.exp(-50 * beta) * math.sqrt(n - 1)) < 1e-9),
            ("T8p", f["T8p_halving_clock_maxerr"] < 1e-10), ("T7", f["T7_F_0_is_identity_err"] < TOL),
            ("CTRL_beta0", f["CTRL_beta0_D_minus_1_max"] < TOL and f["CTRL_beta0_second_face_err"] < TOL),
            ("T7p", abs(f["T7p_beta_pos_second_face_separates_norm"] - f["T7p_expected_(1-e^-5beta)*sqrt(n-1)"]) < 1e-9 and f["T7p_beta_pos_second_face_separates_norm"] > 0),
            ("T9", (n == 1) or f["T9_F_t_not_idempotent_norm_t1"] > 1e-6),
            ("FREQ_PINCHING_drops_rank", f["FREQ_rank_after_PINCHING_not_motor_D"] >= 2), ("FREQ_trace_survives", abs(f["FREQ_trace_after_PINCHING_not_motor_D"] - 1) < 1e-9),
            ("FREQ_reading_restores", f.get("FREQ_reading_restores_post_err", 1.0) < 1e-9),
            ("R2_T2_no_norm", f["R2_T2_no_norm_maxerr"] < 1e-10 and abs(f["R2_T2_no_norm_norm_a"] - 1) > 0.5),
            ("R2_anchor_not_necessary", n == 1 or (f["R2_weak_Ua_minus_a"] > 0.5 and f["R2_weak_anchor_err"] < 1e-10
                                                   and f["R2_anchor_not_necessary_idem_maxerr"] < 1e-10)),
            ("R2_exact_condition_generic", n == 1 or (f["R2_generic_weak_anchor_defect"] > 1e-6
                                                      and f["R2_generic_not_idempotent_maxdefect"] > 1e-6)),
            ("R2_exact_condition_null", n == 1 or (f["R2_null_weak_anchor_defect"] > 0.5 and f["R2_null_motor_max"] < 1e-12)),
            ("R2_zero_transport", abs(f["R2_zero_transport_weak_anchor_defect"] - 1) < 1e-12
                                  and f["R2_zero_transport_motor_max"] == 0.0),
            ("R2_ignores_rate_and_time", f["R2_motor_ignores_rate_and_time_maxerr"] < 1e-12),
            ("R2_motor_D_keeps_rank_of_pure", f["R2_motor_D_det_abs"] > 0 and f["R2_motor_D_channel_rank_of_pure"] == 1),
        ]
    res["checks_total"] = len(checks)
    res["checks_falhos"] = [c for c, ok in checks if not ok]
    res["sanidade"] = "PASSA" if not res["checks_falhos"] else "FALHA"
    res["estatuto"] = "[REAL - medido aqui; sanidade numerica da matematica do motor; nenhum dado observado; nao e veredito sobre a natureza]"
    json.dump(res, open(os.path.join(AQUI, "RESULTADO_NUMERICO_R2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: res[k] for k in ("beta_repr", "alpha_linha", "checks_total", "checks_falhos", "sanidade")}, ensure_ascii=False))
    for f in res["faces"]:
        print(json.dumps({k: f[k] for k in ("n", "trace_P", "rank_P", "T2_idempotent_under_anchor_maxerr", "T2p_unitarity_is_not_enough_norm",
                                             "T4_memory_at_name", "B3_dim_fix_D", "T9_F_t_not_idempotent_norm_t1", "CTRL_beta0_D_minus_1_max",
                                             "FREQ_rank_after_PINCHING_not_motor_D", "FREQ_trace_after_PINCHING_not_motor_D")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
