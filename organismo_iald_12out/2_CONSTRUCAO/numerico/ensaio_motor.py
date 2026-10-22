# -*- coding: utf-8 -*-
"""Sanidade NUMERICA do motor unico (2_CONSTRUCAO, 12-13/10/2026). Nenhum dado observado; nenhum veredito sobre a natureza.
Roda o motor completo  inscricao a -> transporte F (unitario U) -> defasagem D_r(t) = P + e^{-rt}(1-P) -> leitura R = P
-> memoria M[psi] = <psi, P psi>  em 2x2 e em n x n sintetico (n = 2, 3, 6, 12), com r = beta de RUNTIME
(ALPHA_FINE_CODATA_2018 lido nos BYTES do um.py, linha unica; beta = alpha*sqrt(e); nenhum literal de beta aqui).
Mede: idempotencia da releitura (T2 sob ancora; T2' sem ancora = falsificador), traco 1 (Tr P), posto do ponto fixo
(rank P e dim Fix D), M no ponto fixo (T4), identidade M = 1 <=> P psi = psi (T5), reler nao acrescenta (T6),
relogio das metades (T8'), o Verbo sem posto (T9: F(t)^2 != F(t) para t > 0), e o CONTROLE beta = 0 (D = 1, sem segunda face;
T7/T7'). Tambem a face matricial da F1.FREQUENCIA: D sozinha leva rho de posto 1 a posto 2 (o traco sobrevive), a leitura
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
    return np.outer(a, a.conj())


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
    out["T2p_phase_i_breaks_idempotence_norm"] = float(np.linalg.norm(m2 - m1))  # esperado |(-1) - i| = sqrt 2
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
    # Face matricial (F1.FREQUENCIA): D sozinha (defasagem total na base de P) leva rho puro de posto 1 a posto 2; traco sobrevive;
    # a leitura R = P devolve posto 1 (Lueders): P rho P / Tr = P
    psi = rand_unit(n, rng)
    rho = np.outer(psi, psi.conj())
    w2, V2 = np.linalg.eigh(P)
    Bas = V2  # base propria de P
    rho_b = Bas.conj().T @ rho @ Bas
    rho_dinf = Bas @ np.diag(np.diag(rho_b)) @ Bas.conj().T  # D_inf: apaga coerencias na base de P
    out["FREQ_rank_rho_pure"] = rank(rho)
    out["FREQ_rank_after_D_inf"] = rank(rho_dinf)
    out["FREQ_trace_after_D_inf"] = float(np.trace(rho_dinf).real)
    Mv = np.vdot(psi, P @ psi).real
    out["FREQ_memory_of_psi"] = float(Mv)
    if Mv > 1e-9:
        out["FREQ_reading_restores_post_err"] = float(np.linalg.norm(P @ rho @ P / Mv - P))
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
            ("T2p", abs(f["T2p_phase_i_breaks_idempotence_norm"] - math.sqrt(2)) < 1e-10),
            ("T3", f["T3_image_rank"] == 1), ("T4", abs(f["T4_memory_at_name"] - 1) < TOL),
            ("T4p", f["T4p_born_maxerr"] < TOL), ("T5", f["T5_identity_violations"] == 0 and abs(f["T5_phase_of_name_memory"] - 1) < TOL),
            ("T6", f["T6_rereading_adds_nothing_maxerr"] < TOL), ("B3", f["B3_dim_fix_D"] == 1),
            ("B6", f["B6_D_pow_4000_minus_P"] < 1e-12 + 2 * math.exp(-4000 * beta)),
            ("T8", f["T8_never_arrives_norm_at_t50"] > 0 and abs(f["T8_never_arrives_norm_at_t50"] - math.exp(-50 * beta) * math.sqrt(n - 1)) < 1e-9),
            ("T8p", f["T8p_halving_clock_maxerr"] < 1e-10), ("T7", f["T7_F_0_is_identity_err"] < TOL),
            ("CTRL_beta0", f["CTRL_beta0_D_minus_1_max"] < TOL and f["CTRL_beta0_second_face_err"] < TOL),
            ("T7p", abs(f["T7p_beta_pos_second_face_separates_norm"] - f["T7p_expected_(1-e^-5beta)*sqrt(n-1)"]) < 1e-9 and f["T7p_beta_pos_second_face_separates_norm"] > 0),
            ("T9", (n == 1) or f["T9_F_t_not_idempotent_norm_t1"] > 1e-6),
            ("FREQ_D_drops_rank", f["FREQ_rank_after_D_inf"] >= 2), ("FREQ_trace_survives", abs(f["FREQ_trace_after_D_inf"] - 1) < 1e-9),
            ("FREQ_reading_restores", f.get("FREQ_reading_restores_post_err", 1.0) < 1e-9),
        ]
    res["checks_total"] = len(checks)
    res["checks_falhos"] = [c for c, ok in checks if not ok]
    res["sanidade"] = "PASSA" if not res["checks_falhos"] else "FALHA"
    res["estatuto"] = "[REAL - medido aqui; sanidade numerica da matematica do motor; nenhum dado observado; nao e veredito sobre a natureza]"
    json.dump(res, open(os.path.join(AQUI, "RESULTADO_NUMERICO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: res[k] for k in ("beta_repr", "alpha_linha", "checks_total", "checks_falhos", "sanidade")}, ensure_ascii=False))
    for f in res["faces"]:
        print(json.dumps({k: f[k] for k in ("n", "trace_P", "rank_P", "T2_idempotent_under_anchor_maxerr", "T2p_phase_i_breaks_idempotence_norm",
                                             "T4_memory_at_name", "B3_dim_fix_D", "T9_F_t_not_idempotent_norm_t1", "CTRL_beta0_D_minus_1_max",
                                             "FREQ_rank_after_D_inf", "FREQ_trace_after_D_inf")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
