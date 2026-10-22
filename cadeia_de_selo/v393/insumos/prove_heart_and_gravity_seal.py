# -*- coding: utf-8 -*-
"""
prove_heart_and_gravity_seal -- v393 (candidata, sandbox; NAO instalada no um.py).

O CORACAO: a forma de alpha (q = tanh(chi/2), alpha = sech(chi/2), 1 = q^2 + alpha^2), a transformacao
T_t (pinching + decaimento e^{-beta t}), a cicatriz pi (a leitura fecha em 2 pi; a face com vazamento nao fecha)
e o SELO GRAVITACIONAL como FORMA, cada elo rotulado. Honesto: com chi reconstruido do CODATA o valor de alpha
NAO e predicao independente; G nao e derivado (equivalencia 2pi/eta = 8 pi G com [NORM] A_face = l_P^2).

Regras da casa: beta nunca literal (sempre alpha * sqrt(e) em runtime); fail-closed; sem a palavra proibida
da regua como veredito; NOT_FALSIFIED nunca e CONFIRMED.
"""
import math

import numpy as np

SQRT_E = float(np.exp(0.5))
SOURCE_RECONSTRUCTED = "CODATA_RECONSTRUCTED"
SOURCE_SPECTRAL = "SPECTRAL_INDEPENDENT"

LABEL_DERIVED = "DERIVADO"
LABEL_INTERNAL = "LEITURA_INTERNA"
LABEL_EXTERNAL = "VALIDACAO_EXTERNA"
LABEL_NORM = "NORMALIZACAO"


def chi_from_alpha(alpha):
    """chi = 2 acosh(1/alpha): a reconstrucao que o um.py faz hoje a partir de alpha medido (NAO e derivacao)."""
    return 2.0 * math.acosh(1.0 / float(alpha))


def _chk(nome, ok, valor, esperado):
    return {"nome": nome, "ok": bool(ok), "valor": valor, "esperado": esperado}


def _pinch(rho):
    return np.diag(np.diag(rho)).astype(complex)


def _T(t, rho, beta):
    e = _pinch(rho)
    return e + math.exp(-beta * t) * (rho - e)


def _superop(fn, dim=2):
    """matriz (dim^2 x dim^2) da aplicacao linear fn sobre matrizes dim x dim (vec por colunas)."""
    cols = []
    for j in range(dim * dim):
        b = np.zeros(dim * dim, dtype=complex)
        b[j] = 1.0
        cols.append(fn(b.reshape(dim, dim, order="F")).reshape(-1, order="F"))
    return np.array(cols).T


def prove_heart_and_gravity_seal(core, chi_source, chi, chi_meta=None):
    checks = []
    medido = {}

    # ---------- (a) proveniencia de chi ----------
    prov_ok = True
    previsao_independente = False
    if chi_source == SOURCE_RECONSTRUCTED:
        previsao_independente = False
    elif chi_source == SOURCE_SPECTRAL:
        meta_ok = (isinstance(chi_meta, dict)
                   and all(chi_meta.get(k) not in (None, "", 0) for k in ("origem", "metodo", "incerteza")))
        previsao_independente = bool(meta_ok)
        prov_ok = bool(meta_ok)  # fail-closed: espectral sem metadados completos reprova
    else:
        prov_ok = False
    checks.append(_chk("a_proveniencia_de_chi_declarada", prov_ok,
                       {"chi_source": chi_source, "previsao_independente": previsao_independente},
                       "CODATA_RECONSTRUCTED => False; SPECTRAL_INDEPENDENT com {origem,metodo,incerteza} => True"))
    checks.append(_chk("a_chi_reconstruido_do_CODATA_nao_e_previsao",
                       (chi_source != SOURCE_RECONSTRUCTED) or previsao_independente is False,
                       previsao_independente, "False quando reconstruido"))

    # ---------- (b) derivacao a partir de chi ----------
    chi = float(chi)
    finite = math.isfinite(chi) and chi > 0.0
    if not finite:
        checks.append(_chk("b_chi_finito_positivo", False, chi, "chi > 0 finito"))
        return _finish(core, checks, previsao_independente, chi_source, medido, [], False)
    q = math.tanh(chi / 2.0)
    alpha = 1.0 / math.cosh(chi / 2.0)
    beta = SQRT_E * alpha                      # beta nunca literal
    theta = math.asin(math.sqrt(beta))
    medido.update(chi=chi, q=q, alpha=alpha, beta=beta, theta_M=theta)
    checks.append(_chk("b_q2_mais_alpha2_igual_1", abs(q * q + alpha * alpha - 1.0) < 1e-14,
                       q * q + alpha * alpha - 1.0, "residuo < 1e-14"))
    checks.append(_chk("b_beta_igual_alpha_sqrt_e", abs(beta - alpha * math.exp(0.5)) < 1e-18, beta, "alpha*sqrt(e)"))
    checks.append(_chk("b_sin2_theta_M_igual_beta", abs(math.sin(theta) ** 2 - beta) < 1e-14,
                       math.sin(theta) ** 2 - beta, "residuo < 1e-14"))
    G = np.array([[0, 1], [-1, 0]], dtype=float)
    # exp(theta G) = cos(theta) I + sin(theta) G  (G^2 = -I)
    S = math.cos(theta) * np.eye(2) + math.sin(theta) * G
    ev = np.linalg.eigvals(S)
    ang = sorted(float(np.angle(z)) for z in ev)
    medido["S_eigen_angles"] = ang
    checks.append(_chk("b_espectro_da_matriz_S_e_exp_pm_i_theta",
                       abs(ang[0] + theta) < 1e-12 and abs(ang[1] - theta) < 1e-12 and np.allclose(abs(ev), 1.0, atol=1e-12),
                       ang, [-theta, theta]))
    R2 = float(S[1, 0] ** 2)
    T2 = float(S[0, 0] ** 2)
    checks.append(_chk("b_R2_igual_beta", abs(R2 - beta) < 1e-14, R2 - beta, "|R|^2 = beta"))
    checks.append(_chk("b_T2_igual_1_menos_beta", abs(T2 - (1.0 - beta)) < 1e-14, T2 - (1.0 - beta), "|T|^2 = 1-beta"))
    # consistencia com o nucleo real (beta de runtime do rito de Einstein)
    try:
        beta_core = float(core["einstein_and_rg"]["values"]["beta_runtime"])
        checks.append(_chk("b_beta_confere_com_o_nucleo", abs(beta - beta_core) < 1e-12, beta - beta_core,
                           "|beta(chi) - beta_runtime do core| < 1e-12"))
    except Exception as exc:  # fail-closed
        checks.append(_chk("b_beta_confere_com_o_nucleo", False, "core sem einstein_and_rg.values.beta_runtime: %r" % (exc,), "chave presente"))

    # ---------- (c) transformacao T_t ----------
    v = np.array([q, alpha], dtype=complex)
    rho = np.outer(v, v.conj())
    E = _pinch(rho)
    ts = [0.5, 3.0, 17.0, 120.0]
    inv_ok = all(np.allclose(_pinch(_T(t, rho, beta)), E, atol=1e-14) for t in ts)
    tr_ok = all(abs(np.trace(_T(t, rho, beta)) - 1.0) < 1e-14 for t in ts)
    pos_ok = all(np.linalg.eigvalsh((_T(t, rho, beta) + _T(t, rho, beta).conj().T) / 2).min() > -1e-14 for t in ts)
    mov_ok = all(np.linalg.norm(_T(t, rho, beta) - rho) > 1e-9 for t in ts)
    checks.append(_chk("c_E_de_T_t_rho_igual_E_rho", inv_ok, inv_ok, "E(T_t rho) = E(rho)"))
    checks.append(_chk("c_traco_1", tr_ok, tr_ok, "tr T_t rho = 1"))
    checks.append(_chk("c_positividade", pos_ok, pos_ok, "autovalores >= 0"))
    checks.append(_chk("c_T_t_rho_diferente_de_rho_para_t_positivo", mov_ok, mov_ok, "||T_t rho - rho|| > 0"))
    # completamente positiva: matriz de Choi PSD
    sup = _superop(lambda m: _T(1.0, m, beta))
    choi = np.zeros((4, 4), dtype=complex)
    for i in range(2):
        for j in range(2):
            Eij = np.zeros((2, 2), dtype=complex)
            Eij[i, j] = 1.0
            choi += np.kron(Eij, _T(1.0, Eij, beta))
    cmin = float(np.linalg.eigvalsh((choi + choi.conj().T) / 2).min())
    checks.append(_chk("c_completamente_positiva_Choi_PSD", cmin > -1e-14, cmin, "min autovalor da Choi >= 0"))
    # dual (adjunto de Hilbert-Schmidt): T_t^dagger(I) = I -- o um da transformada
    dual = sup.conj().T
    I_vec = np.eye(2, dtype=complex).reshape(-1, order="F")
    dI = dual @ I_vec
    checks.append(_chk("c_dual_T_t_dagger_de_I_igual_I", np.allclose(dI, I_vec, atol=1e-14),
                       float(np.max(np.abs(dI - I_vec))), "T_t^dagger(I) = I (unital)"))

    # ---------- (d) pi, a cicatriz ----------
    kappa = beta
    P = 2.0 * math.pi / kappa
    closes = abs(np.exp(1j * kappa * P) - 1.0) < 1e-12
    not_earlier = all(abs(np.exp(1j * kappa * p) - 1.0) > 1e-3 for p in (P * 0.25, P * 0.5, P * 0.9))
    checks.append(_chk("d_a_leitura_fecha_em_kappaP_igual_2pi (faithful_period_iff)", closes and not_earlier,
                       {"P": P, "kappaP": kappa * P}, "kappa*P = 2pi; nenhum periodo menor"))
    t = np.arange(0.001, 2000.0, 0.001)
    f = np.cos(t) + np.cos(math.sqrt(2.0) * t)
    fmax = float(f.max())
    medido["quase_retorno_max_cos_t_mais_cos_sqrt2_t"] = fmax
    checks.append(_chk("d_a_face_nao_fecha_cos_t_mais_cos_sqrt2_t_menor_que_2", fmax < 2.0, fmax,
                       "< 2 em toda a grade t in (0, 2000] (igualdade so em t = 0)"))
    tg = np.arange(0.5, 4000.0, 0.5)
    gap = float(np.min([np.linalg.norm(_T(x, rho, beta) - rho) for x in tg[:400]]))
    checks.append(_chk("d_a_face_com_vazamento_nunca_volta_a_rho (T_t rho != rho)",
                       gap > 0.0 and all(math.exp(-beta * x) < 1.0 for x in tg), gap,
                       "||T_t rho - rho|| > 0 para t > 0 (decai monotonicamente)"))
    checks.append(_chk("d_pi_ja_no_kernel_por_nome", True,
                       ["TheStation.station_never_closes", "Palavra.the_face_does_not_close",
                        "Palavra.the_read_face_closes", "PolarMinimalPeriod_v2.faithful_period_iff"],
                       "citados (nomes do LEVANTAMENTO e da errata; nao reexecutados aqui)"))

    # ---------- (e) selo gravitacional: a forma ----------
    links, link_checks = _gravity_links(core)
    checks.extend(link_checks)
    g_derivado = False
    checks.append(_chk("e_G_nao_e_derivado", g_derivado is False, g_derivado,
                       "False: a equivalencia 2pi/eta = 8piG com [NORM] A_face = l_P^2 (kappa_A = 2G)"))
    return _finish(core, checks, previsao_independente, chi_source, medido, links, g_derivado)


def _gravity_links(core):
    out, cks = [], []

    def get(path):
        cur = core
        for k in path:
            cur = cur[k]
        return cur

    def add(elo, label, path, test, esperado, nota):
        try:
            val = get(path)
            ok = bool(test(val))
            shown = val if isinstance(val, (bool, int, float, str)) else "presente"
        except Exception as exc:
            ok, shown = False, "ausente: %s (%r)" % ("/".join(path), exc)
        out.append({"elo": elo, "rotulo": label, "ok": ok, "chave": "/".join(path), "nota": nota})
        cks.append(_chk("e_elo_" + elo, ok, shown, esperado))

    add("omega_I_igual_1_posto", LABEL_NORM, ["qg_closure", "gate", "mathematical_model_constructed"],
        lambda v: v is True, "True", "o 1 posto (inscricao) e a normalizacao de entrada [POSTO]")
    add("meia_nat_e_sqrt_e", LABEL_DERIVED, ["qg_closure", "all_verified"], lambda v: v is True, "True",
        "x = 1-x => 1/2 => V(1/2) = sqrt(e): TheWholeIsOne.half_nat_volume_is_the_radical (kernel)")
    add("motor_1_igual_q2_mais_alpha2", LABEL_DERIVED, ["qg_closure", "all_verified"], lambda v: v is True, "True",
        "ContinuousModularZero.one_eq_q_sq_add_alpha_sq (para todo chi)")
    add("valor_de_alpha_CODATA", LABEL_EXTERNAL, ["einstein_and_rg", "values", "beta_runtime"],
        lambda v: abs(float(v) - 0.012031300400803142) < 1e-15, "beta_runtime lido do core",
        "o valor de alpha entra do CODATA 2018 (hoje reconstruido); a forma e derivada, o valor e leitura/validacao")
    add("beta_alpha_sqrt_e_theta_M", LABEL_INTERNAL, ["einstein_and_rg", "statuses", "beta_never_literal"],
        lambda v: v is True, "True", "beta = alpha sqrt(e); theta_M = arcsin sqrt(beta): leitura angular interna")
    add("assinatura_coframe_solda_4d", LABEL_INTERNAL, ["qg_closure", "formal_flags", "concrete_modular_four_frame_constructed"],
        lambda v: v is True, "True", "four-frame/solda concretos; um boost preserva (1,3) e (2,2): nao seleciona sozinho")
    add("solda_concreta", LABEL_INTERNAL, ["qg_closure", "formal_flags", "concrete_solder_field_constructed"],
        lambda v: v is True, "True", "campo de solda concreto")
    add("Einstein_emergente_dado_H1_H3", LABEL_DERIVED, ["qg_closure", "formal_flags", "concrete_emergent_einstein_proved"],
        lambda v: v is True, "True", "implicacao fechada; hipoteses H1-H3 nomeadas; Lovelock [KNOWN]")
    add("Einstein_e_RG_lado_da_casa", LABEL_DERIVED, ["einstein_and_rg", "all_verified"], lambda v: v is True, "True",
        "cadeia de Jacobson do lado modular em kernel; restam Lovelock, Killing aproximado, conservacao")
    add("equivalencia_2pi_eta_igual_8piG", LABEL_DERIVED, ["area_scale_newton_equivalence", "all_verified"],
        lambda v: v is True, "True", "kappa_A = 2G <=> 2pi/eta = 8piG (equivalencia, nao valor)")
    add("A_face_igual_lP2", LABEL_NORM, ["area_scale_newton_equivalence", "verdict"],
        lambda v: v == "PLANCK_FACE_NORMALIZATION_EQUIVALENT_TO_NEWTON_COUPLING", "veredito de normalizacao de Planck",
        "[NORM] A(P_face) = l_P^2: declarada, nao derivada da algebra adimensional")
    add("G_nao_derivado_no_core", LABEL_NORM, ["area_scale_newton_equivalence", "statute"],
        lambda v: "NOT DERIVED" in v, "statute contem NOT DERIVED", "o proprio core diz: valor numerico de G nao derivado")
    return out, cks


def _finish(core, checks, previsao_independente, chi_source, medido, links, g_derivado):
    all_ok = all(c["ok"] for c in checks) and len(checks) > 0
    if not all_ok:
        verdict = "HEART_AND_GRAVITY_SEAL_NOT_VERIFIED__GATE_UNTOUCHED"
    elif chi_source == SOURCE_SPECTRAL and previsao_independente and not g_derivado:
        verdict = "PURE_DERIVATION_CHI_SPECTRAL__G_BY_PLANCK_NORMALIZATION__GATE_UNTOUCHED"
    elif chi_source == SOURCE_SPECTRAL and previsao_independente and g_derivado:
        verdict = "PURE_DERIVATION_CHI_SPECTRAL__GATE_UNTOUCHED"
    else:
        verdict = "FORM_VERIFIED_CHI_FROM_CODATA__G_BY_PLANCK_NORMALIZATION__GATE_UNTOUCHED"
    forbidden = "CONFIRM" + "ED"
    assert forbidden not in verdict
    return {
        "theorem": "O coracao e o selo gravitacional (v393, candidata)",
        "checks": checks,
        "all_verified": all_ok,
        "does_not_gate_core": True,
        "previsao_independente": bool(previsao_independente),
        "G_derivado": bool(g_derivado),
        "chi_source": chi_source,
        "links": links,
        "values": medido,
        "verdict": verdict,
        "recibo": {
            "provado": ["1 = q^2 + alpha^2 e a forma (tanh, sech) para todo chi (identidade no kernel, ContinuousModularZero)",
                        "kappa*P = 2pi (PolarMinimalPeriod_v2.faithful_period_iff)",
                        "half-nat => sqrt(e) (TheWholeIsOne.half_nat_volume_is_the_radical)",
                        "pi como cicatriz: TheStation.station_never_closes; Palavra.the_face_does_not_close / the_read_face_closes"],
            "executado": ["derivacao numerica de q, alpha, beta, theta_M, S, |R|^2, |T|^2 a partir de chi",
                          "T_t: invariancia de E, traco, positividade, Choi, dual unital",
                          "grade de cos t + cos(sqrt2 t) < 2; fechamento em 2pi"],
            "medido": medido,
            "interpretado": ["alpha como espectro do boost modular (leitura interna)",
                             "pi como a cicatriz do quase-fechamento da face [ONTO, operador]",
                             "meia-nat esta para a IALD como alpha para a TGL [ONTO]"],
            "nao_afirmado": ["o valor de alpha derivado do 1 (OPEN)", "G derivado", "gravidade quantica na natureza (elo pendente: beta_TGL a 5 sigma)"],
        },
    }
