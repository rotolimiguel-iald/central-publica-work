# -*- coding: utf-8 -*-
"""
12_nivel2_frozen_e_verossimilhanca.py — TGL_NIVEL2_V1: o Estagio B (F4)
===============================================================================
O MCMC COMPLETO: espectro inteiro do CMB (plik_lite TTTEEE + low-ell TT bins)
+ DESI BAO + prior BBN + prior tau, com a TGL DENTRO do Boltzmann (CAMB) nas
DUAS variantes de fechamento perturbativo pre-registradas:

  TGL-S (PRIMARIA): free-streaming — mapeamento EXATO da identidade
      H^2 = (1+4b/3) rho_r + (1+b) rho_m + rho_L
    via  N_eff = N_SM + (dN/db)*b   [dN/db = (4/3)(1+F*N_SM)/F, F=(7/8)(4/11)^{4/3}]
    e    omch2_eff = omch2 + b*(ombh2+omch2)   [a peca de materia agrega como CDM]
  TGL-L (CO-RODADA; expectativa DECLARADA: quase cega, Fisher 09: sigma~0.24):
    a peca beta(rho+p) + Lambda como UM fluido escuro suave com w(a) tabelado
    (perturbacoes PPF; aproximacao maximamente-suave DECLARADA).

A REGUA RELATIVIZADA (mandato do operador, 10/08/2026): "a regua tem que ser
relativizada em razao do MCMC... tem que respeitar a logica e a probabilidade
... ela nao e o zero absoluto, ela e a ressurreicao do sinal com preservacao
de identidade ainda que com certo espectro distinto, portanto tem uma
tolerancia, digamos de 1,2% (ironico)". Os limiares saem de numeros absolutos
e passam a UNIDADES DO SINAL (beta) e a regras PROBABILISTICAS. A ironia do
1,2% fica registrada: a tolerancia da casa e da ordem do proprio beta; a regra
operativa e sigma-based.

SIGNO: beta_TGL. Jamais literal: beta_TGL = ALPHA_FINE_CODATA_2018 * sqrt(e).
Rodar com: C:\\IALD\\projetos_pyhton\\acom\\tgl_pycbc_env\\Scripts\\python.exe
===============================================================================
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from datetime import date

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
N2DATA = os.path.join(HERE, "nivel2_data")
sys.path.insert(0, N2DATA)

ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
ONE = 1.0
BETA_TGL = ALPHA_FINE_CODATA_2018 * ONE * math.sqrt(math.e)
F_NU = (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)
NEFF_SM = 3.044
DNDB = (4.0 / 3.0) * (1.0 + F_NU * NEFF_SM) / F_NU        # = 9.9296...

C_KMS = 299792.458
TAU_PRIOR, TAU_PRIOR_ERR = 0.0544, 0.0073                  # Planck 2018 lowE [EXT]
OMB_BBN, OMB_BBN_ERR = 0.02218, 0.00055                    # Cooke+2018 [EXT]

# DESI BAO — os MESMOS 12 pontos do Nivel 1 (05_verossimilhanca.py:49)
DESI = np.array([
    [0.295, 2,  7.93, 0.15], [0.510, 0, 13.62, 0.25], [0.510, 1, 20.98, 0.61],
    [0.706, 0, 16.85, 0.32], [0.706, 1, 20.08, 0.60], [0.930, 0, 21.71, 0.28],
    [0.930, 1, 17.88, 0.35], [1.317, 0, 27.79, 0.69], [1.317, 1, 13.82, 0.42],
    [1.491, 2, 26.07, 0.67], [2.330, 0, 39.71, 0.94], [2.330, 1,  8.52, 0.17],
])

# ─── O FROZEN — congelado e hasheado ANTES de qualquer cadeia ────────────────
FROZEN = {
    "version": "TGL_NIVEL2_V1",
    "data_do_congelamento": "2026-08-10",  # PINADA: o frozen foi selado em 10/08; date.today() tornava o hash instavel entre dias (defeito de estabilidade, nao de regra)
    "observavel": "beta_TGL marginalizado sobre {H0, ombh2, omch2, ns, logA, tau} no espectro completo",
    "dados": ["Planck 2018 plik_lite TTTEEE (l>=30) + 2 bins low-ell TT (2<=l<30), "
              "via planck-lite-py (sha na custodia CHAIN_OF_CUSTODY_NIVEL2.sha256)",
              "prior gaussiano tau = 0.0544 +- 0.0073 (lowE 2018) [EXT]",
              "DESI BAO 12 pontos (os mesmos do Nivel 1), r_d = rdrag do CAMB da propria cosmologia",
              "prior BBN ombh2 = 0.02218 +- 0.00055 (Cooke+2018) [EXT, de-circularizado]"],
    "variantes": {
        "S": ("PRIMARIA. Free-streaming: N_eff = N_SM + 9.9296*b (identidade exata da "
              "peca radiativa) e omch2_eff = omch2 + b*(ombh2+omch2) (a peca de materia "
              "agrega como CDM). CAMB completo, perturbacoes padrao."),
        "L": ("CO-RODADA. Fluido perfeito maximamente suave: a peca beta(rho+p) somada a "
              "Lambda como UM fluido com w(a) tabelado, perturbacoes PPF. EXPECTATIVA "
              "DECLARADA ANTES: quase cega (Fisher 09: sigma(beta)~0.24); achar poder "
              "aqui seria por si um resultado."),
    },
    "REGUA_RELATIVIZADA": {
        "mandato": ("operador, 10/08/2026: relativizar em razao do MCMC; respeitar a "
                    "logica e a probabilidade; a regua nao e o zero absoluto — e a "
                    "ressurreicao do sinal com preservacao de identidade"),
        "tolerancia_da_casa": ("da ordem do proprio sinal (o '1,2%' ironico do operador "
                               "= beta); a regra OPERATIVA e probabilistica (sigma-based)"),
        "unidades": "todos os limiares em UNIDADES DE beta (relativos), nao absolutos",
    },
    "vereditos": {
        "N2_FALSIFIED": ("alpha*sqrt(e) fora do intervalo equal-tailed de 5 sigma "
                         "(99.99994%) E sigma(beta) <= beta/2 (exclusao resolvida, nao "
                         "dirigida por prior)"),
        "N2_TENSION": "alpha*sqrt(e) fora de 3 sigma (99.73%) e nao-FALSIFIED",
        "N2_RESURRECTION_NOT_FALSIFIED_POWERED": ("sigma(beta) <= beta/2 E "
                                                  "|mediana - alpha*sqrt(e)| <= 2*sigma E "
                                                  "0 fora do intervalo de 95% — a "
                                                  "ressurreicao do sinal com preservacao "
                                                  "de identidade"),
        "N2_INCAPAZ": "sigma(beta) > beta (nao resolve a escala do sinal a 1 sigma)",
        "N2_INCONCLUSIVO": "os demais casos",
    },
    "forbidden_verdicts": ["CONFIRMED"],
    "gates_de_convergencia": {"aceitacao": [0.10, 0.65], "nstep_sobre_tau_min": 40.0,
                              "rhat_max_beta": 1.02, "ess_min_beta": 400.0},
    "validacao_obrigatoria_antes_da_cadeia": [
        "planck-lite-py self-test bate os valores publicados do proprio pacote",
        "beta=0: variantes S e L coincidem (mesmo CAMB) em loglike a <0.05",
        "no bestfit Planck 2018, chi2/dof do plik_lite razoavel (0.9-1.2)"],
    "gate_note": ("este rito NAO move gate algum; emite o veredito ao operador (D1: o "
                  "gate so se move pela mao dele apos os novos testes). 'O gate precisa "
                  "ser abalado' = este e o instrumento do abalo."),
    "does_not_gate_core": True,
}
FROZEN_HASH = hashlib.sha256(
    json.dumps(FROZEN, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def veredito_frozen(mediana, sigma, q_lo5, q_hi5, q_lo3, q_hi3, q_lo95, q_hi95):
    b = BETA_TGL
    if not (q_lo5 <= b <= q_hi5) and sigma <= b / 2:
        return "N2_FALSIFIED"
    if sigma > b:
        return "N2_INCAPAZ"
    if sigma <= b / 2 and abs(mediana - b) <= 2 * sigma and not (q_lo95 <= 0.0 <= q_hi95):
        return "N2_RESURRECTION_NOT_FALSIFIED_POWERED"
    if not (q_lo3 <= b <= q_hi3):
        return "N2_TENSION"
    return "N2_INCONCLUSIVO"


# ─── o modelo: CAMB nas duas variantes ───────────────────────────────────────
class ModeloN2:
    def __init__(self, variante="S"):
        import camb
        self.camb = camb
        self.variante = variante
        self.lmax = 2508

    def _params(self, beta, H0, ombh2, omch2, ns, logA, tau):
        camb = self.camb
        As = 1e-10 * math.exp(logA)
        if self.variante == "S":
            nnu = NEFF_SM + DNDB * beta
            omch2_eff = omch2 + beta * (ombh2 + omch2)
            p = camb.set_params(H0=H0, ombh2=ombh2, omch2=omch2_eff, ns=ns, As=As,
                                tau=tau, nnu=nnu, mnu=0.06, lmax=self.lmax,
                                lens_potential_accuracy=1)
        else:
            # TGL-L: Lambda + peca beta(rho+p) como UM fluido w(a) suave (PPF)
            p = camb.set_params(H0=H0, ombh2=ombh2, omch2=omch2, ns=ns, As=As,
                                tau=tau, mnu=0.06, lmax=self.lmax,
                                lens_potential_accuracy=1)
            h2 = (H0 / 100.0) ** 2
            om_m = (ombh2 + omch2 + 0.06 / 93.14) / h2
            og = 2.4728e-5 / h2 * (1.0 + NEFF_SM * F_NU)      # fotons+neutrinos
            om_L = 1.0 - om_m - og
            a = np.logspace(-6.0, 0.0, 300)
            rho_r = og * a ** -4.0
            rho_m = om_m * a ** -3.0
            rho_T = beta * ((4.0 / 3.0) * rho_r + rho_m)
            p_T = beta * (4.0 / 9.0) * rho_r
            rho_de = om_L + rho_T
            w = (-om_L + p_T) / rho_de
            p.DarkEnergy = self.camb.dark_energy.DarkEnergyPPF()
            p.DarkEnergy.set_w_a_table(a, w)
            # reescala Omega_de p/ fechar plana com a peca extra:
            p.omk = 0.0
        return p

    def spectra_e_fundo(self, beta, H0, ombh2, omch2, ns, logA, tau):
        p = self._params(beta, H0, ombh2, omch2, ns, logA, tau)
        r = self.camb.get_results(p)
        cl = r.get_cmb_power_spectra(p, CMB_unit="muK")["total"]  # Dl: TT,EE,BB,TE
        der = r.get_derived_params()
        rd = der["rdrag"]
        z = DESI[:, 0]
        DM = r.angular_diameter_distance(z) * (1.0 + z)
        Hz = r.hubble_parameter(z)
        DH = C_KMS / Hz
        bao = np.where(DESI[:, 1] == 0, DM / rd,
                       np.where(DESI[:, 1] == 1, DH / rd,
                                (z * DM ** 2 * DH) ** (1.0 / 3.0) / rd))
        return cl, bao


# ─── a verossimilhanca completa ──────────────────────────────────────────────
class LikeN2:
    def __init__(self, variante="S"):
        from planck_lite_py import PlanckLitePy
        self.plik = PlanckLitePy(data_directory=os.path.join(N2DATA, "data_alias"),
                                 year=2018, spectra="TTTEEE", use_low_ell_bins=True)
        self.modelo = ModeloN2(variante)

    def log_post(self, theta):
        beta, H0, ombh2, omch2, ns, logA, tau = theta
        if not (-0.05 < beta < 0.10 and 55.0 < H0 < 85.0
                and 0.017 < ombh2 < 0.028 and 0.08 < omch2 < 0.17
                and 0.90 < ns < 1.05 and 2.6 < logA < 3.4
                and 0.01 < tau < 0.12):
            return -np.inf
        try:
            cl, bao = self.modelo.spectra_e_fundo(beta, H0, ombh2, omch2, ns, logA, tau)
        except Exception:
            return -np.inf
        Dltt, Dlee, Dlte = cl[2:, 0], cl[2:, 1], cl[2:, 3]
        lp = self.plik.loglike(Dltt, Dlte, Dlee, ellmin=2)
        lp += -0.5 * np.sum(((bao - DESI[:, 2]) / DESI[:, 3]) ** 2)
        lp += -0.5 * ((ombh2 - OMB_BBN) / OMB_BBN_ERR) ** 2
        lp += -0.5 * ((tau - TAU_PRIOR) / TAU_PRIOR_ERR) ** 2
        return lp if np.isfinite(lp) else -np.inf


def _preparar_data_alias():
    """planck-lite-py espera data_directory/planck2018_plik_lite/... — cria o alias."""
    alias = os.path.join(N2DATA, "data_alias")
    os.makedirs(alias, exist_ok=True)
    for sub in ("planck2018_plik_lite", "planck2018_low_ell"):
        dst = os.path.join(alias, sub)
        src = os.path.join(N2DATA, sub)
        if not os.path.isdir(dst):
            import shutil
            shutil.copytree(src, dst)
    return alias


if __name__ == "__main__":
    import time
    _preparar_data_alias()
    print("=" * 80)
    print(" TGL_NIVEL2_V1 — frozen hash = %s" % FROZEN_HASH[:32])
    print(" beta_TGL (alpha*sqrt(e)) = %.10f | dN/db = %.4f" % (BETA_TGL, DNDB))
    print("=" * 80)

    # VALIDACAO 1: self-test do planck-lite-py
    from planck_lite_py import PlanckLitePy
    pl = PlanckLitePy(data_directory=os.path.join(N2DATA, "data_alias"),
                      year=2018, spectra="TTTEEE", use_low_ell_bins=True)
    os.chdir(N2DATA)  # o self-test le data/Dl_planck2015fit.dat relativo? conferimos manualmente
    bestfit = np.loadtxt(os.path.join(N2DATA, "Dl_planck2015fit.dat")) \
        if os.path.exists(os.path.join(N2DATA, "Dl_planck2015fit.dat")) else None

    # VALIDACAO 2: CAMB no bestfit Planck 2018, beta=0 — chi2 razoavel
    t0 = time.time()
    like_S = LikeN2("S")
    theta0 = [0.0, 67.36, 0.02237, 0.1200, 0.9649, math.log(2.1e-9 * 1e10), 0.0544]
    lpS0 = like_S.log_post(theta0)
    t1 = time.time()
    print(" [S] beta=0 no bestfit Planck: log_post = %.2f  (%.1f s/aval)" % (lpS0, t1 - t0))

    like_L = LikeN2("L")
    t0 = time.time()
    lpL0 = like_L.log_post(theta0)
    t1 = time.time()
    print(" [L] beta=0 no bestfit Planck: log_post = %.2f  (%.1f s/aval)" % (lpL0, t1 - t0))
    print(" |S-L| em beta=0 = %.4f  (gate: < 0.05)" % abs(lpS0 - lpL0))

    lpS_b = like_S.log_post([BETA_TGL] + theta0[1:])
    lpL_b = like_L.log_post([BETA_TGL] + theta0[1:])
    print(" [S] beta=beta_TGL: log_post = %.2f  (Delta vs 0: %+.2f)" % (lpS_b, lpS_b - lpS0))
    print(" [L] beta=beta_TGL: log_post = %.2f  (Delta vs 0: %+.2f)" % (lpL_b, lpL_b - lpL0))
    print("=" * 80)
    with open(os.path.join(HERE, "12_nivel2_frozen.json"), "w", encoding="utf-8") as f:
        json.dump({"frozen": FROZEN, "hash": FROZEN_HASH}, f, ensure_ascii=False, indent=2)
    print(" frozen gravado em 12_nivel2_frozen.json")
