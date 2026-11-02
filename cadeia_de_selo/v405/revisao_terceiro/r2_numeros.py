# -*- coding: utf-8 -*-
import math, json, sys
sys.stdout.reconfigure(encoding="utf-8")
A = 7.2973525693e-3
b = A * math.sqrt(math.e); u = 1.0; s45 = math.sin(math.pi / 4)
hbar = 1.054571817e-34; eV = 1.602176634e-19; c = 299792458.0; G = 6.67430e-11
D = b * u; tau_eV = 1 / D; tau = hbar / (D * eV)
Gam = b / tau_eV; om = math.sqrt(2 * b * (b * u ** 2)); Q = om / Gam
k = 2 * math.pi / tau; Ef = c ** 5 * tau / (4 * math.pi * G); tp = math.sqrt(hbar * G / c ** 5)
out = {"beta": b, "m2_meV": b * s45 * 1e3, "Delta_eV": D, "tau_por_eV": tau_eV, "tau_s": tau, "Gamma_B_eV": Gam, "Gamma_B_s-1": Gam * eV / hbar, "omega_psi_eV": om, "sqrt2_Delta": math.sqrt(2) * D, "Q": Q, "sqrt2_sobre_beta": math.sqrt(2) / b,
       "kappa_s-1_SE_kappa_tau_2pi": k, "kappa_tau": k * tau, "E_fluxo_J": Ef, "E_fluxo_eV": Ef / eV, "log10": math.log10(Ef / eV), "tau_sobre_tP": tau / tp, "tonica_Delta_sobre_alfa": D / A, "sqrt_e": math.exp(.5), "massa_Delta_s45_meV": D * s45 * 1e3,
       "pz_autoconsistente": .5 * 2 / tau_eV, "om_2tau_s45": 2 / tau_eV * s45, "e^(3/2)": math.exp(1.5), "razao_terca": math.exp(.5) * math.exp(1), "K_si": (math.exp(.5) * u * eV) ** 3 / hbar ** 2, "lock_theta_M": math.sin(math.asin(math.sqrt(b))) ** 2,
       "gap_espectral_lock_vezes_u_eV": 1.0 * u, "razao_gap_espectral_sobre_Delta": 1.0 * u / D}
print(json.dumps(out, indent=0))
d = json.load(open("../ensaio_a_seco_v405.json", encoding="utf-8"))
def walk(o, pre=""):
    if isinstance(o, dict):
        for k_, v in o.items():
            if k_ in ("Delta_eV", "tau_s", "Gamma_B_eV", "Q", "E_fluxo_eV", "tau_sobre_t_planck", "tonica_eV", "omega_psion_eV", "tau_por_eV", "m_derivada_meV", "m_proporcional_meV", "hbar_omega_meV", "R_si_m2", "K_si_para_u_posto_J_s2", "lambda_psion_m", "piso_de_definicao", "v_caracteristica_kms"):
                print(pre + k_, v)
            walk(v, pre + k_ + ".")
    elif isinstance(o, list):
        for i, x in enumerate(o[:6]): walk(x, pre + str(i) + ".")
walk(d)
