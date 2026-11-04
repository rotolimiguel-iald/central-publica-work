# -*- coding: utf-8 -*-
"""estimador_ramo_b_v1.py -- o ESTIMADOR do V1 do ramo B (secao `estimador` do PRE-REGISTRO V1, sha16 86f98fcc124dd9ca), implementado como funcoes
puras, deterministicas e testaveis em sintetico. NAO le arquivo nenhum, NAO abre dado: recebe numeros.

V1 (verbatim, resumo): primario = media ponderada 1/sigma^2 dos delta_tau_220, RELATIVA A RG, com nuisance da referencia c(sigma) = c0 + k_c*sigma PROFILADO sob as
duas hipoteses; offset fixo em 0 PROIBIDO como teste.  w_i = 1/(sigma_i^2 + sigma_sys^2); sigma_comb = 1/sqrt(sum w); sigma_usado = max(sigma_comb, sigma_jackknife).
delta_bar = sum w (delta_hat - c(sigma)) / sum w;  z_RG = delta_bar/sigma_comb;  z_B = (delta_bar - delta_bar_pred)/sigma_comb;  poder = |delta_bar_pred|/sigma_usado;
chi2/dof; jackknife por evento; fracao maxima de informacao por evento.  delta_i_pred = -x_i/(1+x_i), x_i = beta*k(a_i)*N(a_i), a_i = mediana do spin do remanescente.
Secundario: verossimilhanca conjunta por KDE (larguras 0,7/1,0/1,4) em delta_i_pred e em 0, mesmo nuisance; ln B(B/RG); o primario decide; discordancia de rotulo => INCONCLUSIVE.

ESCOLHAS DO DESENHO que o V1 deixa abertas (ditas ANTES; congeladas em ESCOLHAS_DO_DESENHO_03nov.json; a gerencia pode mudar ANTES de lancar, nunca depois):
  E1 valor central de delta_hat_i = MEDIA posterior (consistente com sigma por ddof=1); mediana como controle relatado.
  E2 c(sigma): "profilado sob as duas hipoteses" = c_RG(sigma) medido nas injecoes C2 so-RG e c_B(sigma) medido nas injecoes C2 com dtau220 = delta_pred; a incerteza
     dos coeficientes (covariancia) ENTRA no erro (so pode baixar o poder, nunca criar falsificacao): sigma_tot^2 = sigma_comb^2 + g' Sigma_c g.
  E3 sigma_sys dos pesos = max da familia declarada (0,038); a de 0,029 e relatada ao lado.
  E4 gaussianidade (C9): razao sigma_comb(W90/3,29)/sigma_comb(std) no CONJUNTO em [0,9; 1,1] (como o poder_cego do V1 compara A_31_width90 com A_31_std); por evento so relatada.
  E5 rotulo primario x secundario: sinal de ln B(B/RG) (gaussiano de pontos vs KDE nas tres larguras); sinais opostos => discordancia.
  E6 C2 '|vies| <= 0,2|delta_pred|': leitura ESTATISTICA (reprova so se |vies medido| - 1,645*sigma_vies > tolerancia); a leitura literal (estimativa pontual) e calculada ao lado.
"""
import math

import numpy as np

SIGMA_SYS_FAMILIA = (0.029, 0.038)
BANDAS_KDE = (0.7, 1.0, 1.4)


def _arr(x):
    a = np.asarray(x, dtype=float)
    if a.ndim != 1 or not np.isfinite(a).all():
        raise ValueError("vetor 1-D finito exigido")
    return a


# ------------------------------------------------------------------------------------------------- nuisance c(sigma)
def ajustar_vies(pontos):
    """pontos: lista de dicts {sigma, vies, sigma_vies} (vies = recuperado - verdade, de UMA injecao C2).
    Minimos quadrados ponderados de vies = c0 + k_c*sigma (linear, J>=3 e sigma nao constante) ou c0 (constante, J>=2).
    Covariancia inflada por max(1, chi2/dof) (Birge). Fail-closed: J<2 => ValueError."""
    J = len(pontos)
    if J < 2:
        raise ValueError("C2 com menos de 2 injecoes na classe: c(sigma) nao medido")
    s = _arr([p["sigma"] for p in pontos])
    y = _arr([p["vies"] for p in pontos])
    sv = _arr([p["sigma_vies"] for p in pontos])
    if np.any(sv <= 0):
        raise ValueError("sigma_vies deve ser positivo")
    W = 1.0 / sv ** 2
    linear = J >= 3 and np.ptp(s) > 1e-9
    X = np.column_stack([np.ones(J), s]) if linear else np.ones((J, 1))
    A = X.T @ (W[:, None] * X)
    cov = np.linalg.inv(A)
    beta_hat = cov @ (X.T @ (W * y))
    resid = y - X @ beta_hat
    chi2 = float(np.sum(W * resid ** 2))
    dof = J - X.shape[1]
    inflar = max(1.0, chi2 / dof) if dof > 0 else 1.0
    cov = cov * inflar
    c0 = float(beta_hat[0])
    kc = float(beta_hat[1]) if linear else 0.0
    C = np.zeros((2, 2))
    C[: cov.shape[0], : cov.shape[1]] = cov
    return {"modo": "linear" if linear else "constante", "J": J, "c0": c0, "kc": kc, "cov": C.tolist(),
            "chi2": chi2, "dof": dof, "fator_Birge": inflar}


def c_de_sigma(fit, s):
    return fit["c0"] + fit["kc"] * np.asarray(s, dtype=float)


# ------------------------------------------------------------------------------------------------- perfil de uma hipotese
def _perfil(y, s, w, mu, fit, incluir_vies):
    """Perfil sob UMA hipotese (mu = previsao por evento: 0 para RG, delta_pred_i para B)."""
    c = c_de_sigma(fit, s) if fit is not None else np.zeros_like(y)
    D = y - c - mu                      # desvio relativo a previsao da hipotese
    sw = w.sum()
    dbar_rel = float((w * D).sum() / sw)
    sig_comb = float(1.0 / math.sqrt(sw))
    var_c = 0.0
    if fit is not None and incluir_vies:
        g = np.array([(w * 1.0).sum() / sw, (w * s).sum() / sw])
        var_c = float(g @ np.asarray(fit["cov"]) @ g)
    sig_tot = math.sqrt(sig_comb ** 2 + var_c)
    n = len(y)
    if n > 2:
        jk = np.array([((w * D).sum() - w[i] * D[i]) / (sw - w[i]) for i in range(n)])
        s_jack = float(math.sqrt((n - 1) / n * ((jk - jk.mean()) ** 2).sum()))
    else:
        s_jack = float("nan")
    chi2 = float((w * (D - dbar_rel) ** 2).sum())
    return {"dbar_rel": dbar_rel, "sigma_comb": sig_comb, "sigma_vies": math.sqrt(var_c), "sigma_tot": sig_tot,
            "sigma_jack": s_jack, "sigma_usado": max(sig_tot, s_jack) if np.isfinite(s_jack) else sig_tot,
            "chi2": chi2, "chi2_dof": chi2 / (n - 1) if n > 1 else float("nan"), "D": D.tolist()}


def _logkde(x, ponto, mult):
    n = len(x)
    h = mult * np.std(x, ddof=1) * n ** (-1.0 / 5.0)
    z = (ponto - x) / h
    m = np.max(-0.5 * z ** 2)
    return float(m + np.log(np.mean(np.exp(-0.5 * z ** 2 - m))) - math.log(h * math.sqrt(2 * math.pi)))


# ------------------------------------------------------------------------------------------------- estimador
def estimar(eventos, sigma_sys=SIGMA_SYS_FAMILIA[-1], fit_RG=None, fit_B=None, incluir_incerteza_do_vies=True, amostras=None):
    """eventos: lista de dicts {evento, delta_hat (media), delta_hat_mediana, sigma (std ddof=1), w90, delta_pred}.
    fit_RG/fit_B: saidas de ajustar_vies (ou None => c = 0 e a lacuna e DITA: c_conhecido=False).
    amostras: {evento: vetor dtau220 desvelado} para o secundario (KDE); opcional."""
    n = len(eventos)
    y = _arr([e["delta_hat"] for e in eventos])
    ym = _arr([e["delta_hat_mediana"] for e in eventos])
    s = _arr([e["sigma"] for e in eventos])
    dp = _arr([e["delta_pred"] for e in eventos])
    w90 = _arr([e["w90"] for e in eventos])
    if np.any(s <= 0) or sigma_sys < 0:
        raise ValueError("sigma_i > 0 e sigma_sys >= 0 exigidos")
    w = 1.0 / (s ** 2 + sigma_sys ** 2)
    sw = w.sum()
    dbar_pred = float((w * dp).sum() / sw)
    sig_comb = float(1.0 / math.sqrt(sw))
    zero = np.zeros(n)
    RG = _perfil(y, s, w, zero, fit_RG, incluir_incerteza_do_vies)
    B = _perfil(y, s, w, dp, fit_B, incluir_incerteza_do_vies)
    # grandezas no vocabulario do V1
    dbar_RG = RG["dbar_rel"]                       # delta_bar com c_RG (relativo a RG)
    dbar_B = B["dbar_rel"] + dbar_pred             # delta_bar com c_B
    z_RG = dbar_RG / RG["sigma_tot"]
    z_B = B["dbar_rel"] / B["sigma_tot"]
    sig_usado = B["sigma_usado"]
    poder = abs(dbar_pred) / sig_usado
    z_excl = abs(B["dbar_rel"]) / sig_usado
    # mediana como controle (E1)
    D_med = ym - (c_de_sigma(fit_B, s) if fit_B is not None else 0.0) - dp
    z_B_mediana = float((w * D_med).sum() / sw) / B["sigma_tot"]
    # gaussianidade no conjunto (E4)
    w90w = 1.0 / ((w90 / 3.29) ** 2 + sigma_sys ** 2)
    razao_gauss = math.sqrt(sw / w90w.sum())      # sigma_comb(W90)/sigma_comb(std)
    # rotulo primario (E5): ln B gaussiano de pontos com os pesos dos eventos
    c_RG = c_de_sigma(fit_RG, s) if fit_RG is not None else zero
    c_B = c_de_sigma(fit_B, s) if fit_B is not None else zero
    chi2_pt_RG = float((w * (y - c_RG) ** 2).sum())
    chi2_pt_B = float((w * (y - c_B - dp) ** 2).sum())
    lnB_prim = -0.5 * (chi2_pt_B - chi2_pt_RG)
    sec = None
    if amostras is not None:
        sec = {}
        for mult in BANDAS_KDE:
            v = 0.0
            for i, e in enumerate(eventos):
                x = _arr(amostras[e["evento"]])
                v += _logkde(x, dp[i] + c_B[i], mult) - _logkde(x, 0.0 + c_RG[i], mult)
            sec["h%.1f" % mult] = v
    discordancia = None
    if sec is not None:
        sinais = {k: (v > 0) for k, v in sec.items()}
        discordancia = [k for k, v in sinais.items() if v != (lnB_prim > 0)]
    # contraste (informativo, V1 'previsao_por_evento'): chi2/dof do conjunto em torno da media ponderada = o pior dos dois perfis
    return {
        "n": n, "sigma_sys": sigma_sys, "incluir_incerteza_do_vies": bool(incluir_incerteza_do_vies),
        "c_conhecido": {"RG": fit_RG is not None, "B": fit_B is not None},
        "delta_pred_ponderado": dbar_pred, "sigma_comb_sem_vies": sig_comb, "poder_V1_literal": abs(dbar_pred) / sig_comb,
        "delta_bar_RG": dbar_RG, "delta_bar_B": dbar_B,
        "z_RG": z_RG, "z_B": z_B, "z_B_com_mediana_controle": z_B_mediana,
        "sigma_usado": sig_usado, "poder": poder, "z_excl": z_excl,
        "perfil_RG": {k: v for k, v in RG.items() if k != "D"}, "perfil_B": {k: v for k, v in B.items() if k != "D"},
        "chi2_dof": max(RG["chi2_dof"], B["chi2_dof"]),
        "fracao_maxima_de_informacao_por_evento": float(w.max() / sw),
        "razao_gaussianidade_W90_sobre_std": razao_gauss,
        "lnB_primario_B_sobre_RG": lnB_prim, "lnB_secundario_KDE": sec, "kde_discordancias": discordancia,
        "sigma_sys_0p029": _relatorio_sys(y, s, dp, 0.029, fit_RG, fit_B, incluir_incerteza_do_vies),
    }


def _relatorio_sys(y, s, dp, ss, fit_RG, fit_B, incl):
    w = 1.0 / (s ** 2 + ss ** 2)
    B = _perfil(y, s, w, dp, fit_B, incl)
    return {"poder": abs(float((w * dp).sum() / w.sum())) / B["sigma_usado"], "z_excl": abs(B["dbar_rel"]) / B["sigma_usado"]}


# ------------------------------------------------------------------------------------------------- controle C1 (ramo canonico)
def controle_C1(pesos, mf_det_kg, x, sigma_tot, constantes):
    """Ramo canonico (tau* = t_Planck) como controle nulo: x_can = x * (m_Planck/M_f,det) ~ 1e-40; exige |z_A - z_RG| = |delta_can|/sigma < 1e-30.
    pesos: w_i; mf_det_kg: M_f,det por evento em kg; x: x_i = beta*k*N."""
    w = np.asarray(pesos, dtype=float)
    xc = np.asarray(x, dtype=float) * (constantes["m_planck"] / np.asarray(mf_det_kg, dtype=float))
    dcan = -xc / (1 + xc)
    dbar_can = float((w * dcan).sum() / w.sum())
    dif = abs(dbar_can) / sigma_tot
    return {"delta_canonico_ponderado": dbar_can, "abs_zA_menos_zRG": dif, "passa": bool(dif < 1e-30)}


# ------------------------------------------------------------------------------------------------- controle C2 (injecoes)
def avaliar_c2(pontos_por_classe, tolerancia):
    """pontos_por_classe: {'GR': [{sigma, vies, sigma_vies, coberto}], 'RB': [...]}. tolerancia = 0,2*|delta_bar_pred|.
    Devolve, por classe, a leitura LITERAL (estimativa pontual) e a ESTATISTICA (E6) lado a lado."""
    from scipy.stats import binomtest
    out = {}
    for cls, pts in pontos_por_classe.items():
        if len(pts) < 2:
            out[cls] = {"J": len(pts), "status": "NOT_RUN"}
            continue
        vies = _arr([p["vies"] for p in pts])
        sv = _arr([p["sigma_vies"] for p in pts])
        w = 1.0 / sv ** 2
        m = float((w * vies).sum() / w.sum())
        sm = float(1.0 / math.sqrt(w.sum()))
        k = int(sum(1 for p in pts if p["coberto"]))
        p_cob = float(binomtest(k, len(pts), 0.90).pvalue)
        literal = abs(m) <= tolerancia
        estat = (abs(m) - 1.645 * sm) <= tolerancia
        cob_ok = p_cob >= 0.01
        out[cls] = {"J": len(pts), "vies_medio": m, "sigma_vies_medio": sm, "tolerancia": tolerancia,
                    "literal_passa": bool(literal), "estatistico_passa": bool(estat), "cobertura": "%d/%d" % (k, len(pts)),
                    "cobertura_p_binomial_vs_0p90": p_cob, "cobertura_ok": bool(cob_ok),
                    "status_literal": "PASS" if (literal and cob_ok) else "FAIL",
                    "status_estatistico": "PASS" if (estat and cob_ok) else "FAIL"}
    return out
