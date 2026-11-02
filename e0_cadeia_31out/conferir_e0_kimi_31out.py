# -*- coding: utf-8 -*-
"""31/10/2026, gerência c1 — conferência INDEPENDENTE dos números do handoff do Kimi (E0/m2), com β = α·√e em runtime (nunca literal).
Não abre dado novo: usa só as entradas públicas já transcritas no determinacoes_m2_30out.json (centros e erros), refaz a aritmética por código
próprio e compara com os números do Kimi. Também confere a identidade Γ_B = Γ_ω(ω★) com ω★·τ★ = √2 e o ramo nativo planckiano."""
import json, math, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
# CODATA 2018 (SI exatas onde são)
c = 299792458.0; h = 6.62607015e-34; hbar = h / (2 * math.pi); G = 6.67430e-11; eV = 1.602176634e-19
tP = math.sqrt(hbar * G / c**5); lP = c * tP; EP = math.sqrt(hbar * c**5 / G)
print("beta (runtime) = %.15f | 1/beta = %.4f | sqrt(e) = %.6f" % (beta, 1 / beta, math.sqrt(math.e)))
print("t_P = %.6e s | l_P = %.6e m | E_P = %.6e eV" % (tP, lP, EP / eV))
# 1) a forma do neutrino (v404): m2 = beta*sin45*E0 com E0 = 1 eV [DECLARADO]
E0 = 1.0
m2 = beta * math.sin(math.pi / 4) * E0 * 1e3  # meV
print("m2_TGL = beta*sen45*E0 = %.10f meV (Kimi: 8.5074140999) | Delta_pred = %.10f e-5 eV^2 (Kimi: 7.2376094667)" % (m2, (m2 / 1e3)**2 / 1e-5))
# 2) ramo nativo (tau* = t_P): E = c^5 tau*/(4 pi G) = E_P/(4 pi)
E_nat = c**5 * tP / (4 * math.pi * G)
print("ramo nativo: E = c^5 t_P/(4piG) = %.5e eV = E_P/(4pi)? %s (Kimi: 9.716e26 eV)" % (E_nat / eV, abs(E_nat - EP / (4 * math.pi)) / E_nat < 1e-12))
print("R_B nativo = l_P/beta = %.4f l_P (o «1 em 83 raios» do operador, 28/10: 1/beta = %.2f)" % (1 / beta, 1 / beta))
# 3) tau* exigido para 1 eV e o que ele é: 2*pi*r_s/c, o tempo de luz da circunferência de Schwarzschild da energia
tau_1eV = 4 * math.pi * G * eV / c**5
rs = 2 * G * (eV / c**2) / c**2
print("tau* para 1 eV = %.10e s = %.10e t_P (Kimi: 5.5488494964e-71 s; 1.0292330321e-27 t_P) | = 2 pi r_s/c? %s" % (tau_1eV, tau_1eV / tP, abs(tau_1eV - 2 * math.pi * rs / c) / tau_1eV < 1e-12))
print("q0 = G E0/c^4 = %.10e m (Kimi: 1.3237738092e-63) = r_s/2 | F0 = 4 pi q0 = %.10e m (Kimi: 1.6635032296e-62)" % (G * eV / c**4, 4 * math.pi * G * eV / c**4))
# 4) a identidade das taxas: Gamma_omega(omega) = 1/2 beta tau* omega^2 ; Gamma_B = beta/tau*  <=> omega* tau* = sqrt(2)
for tau in (tP, 1e-20, 1.0):
    om = math.sqrt(2) / tau
    print("tau*=%.3e s: Gamma_omega(sqrt2/tau*) = %.6e | beta/tau* = %.6e | iguais: %s" % (tau, 0.5 * beta * tau * om**2, beta / tau, abs(0.5 * beta * tau * om**2 - beta / tau) / (beta / tau) < 1e-12))
# 5) as dez tensões, refeitas por código independente a partir das ENTRADAS do JSON do Kimi (não dos resultados dele)
J = json.loads(Path(r"C:\IALD\Central de Patentes\work\neutrino_E0_autonomia_30out\determinacoes_m2_30out.json").read_text(encoding="utf-8"))
print("\n%-22s %8s %8s %8s   %s" % ("determinação", "z(c1)", "z(Kimi)", "difer.", "grupo"))
for r in J["resultados"]:
    mu = r["mu"]; m2obs = math.sqrt(10 * mu)  # meV
    sig = r["err_p"] if r["side_to_pred"] == "up" else r["err_m"]
    # conferência da escolha do lado: a previsão está acima (up) ou abaixo (down) do centro?
    lado_esperado = "up" if m2 > m2obs else "down"
    z = abs(m2obs - m2) / (0.5 * (sig / mu) * m2obs)
    print("%-22s %8.3f %8.3f %8.1e   %s%s" % (r["id"], z, r["z_sigma"], abs(z - r["z_sigma"]), r["grupo"], "" if lado_esperado == r["side_to_pred"] else "  ⚠ lado do erro: esperado %s, usado %s" % (lado_esperado, r["side_to_pred"])))
# 6) a escala que o dado pediria (inversão PROIBIDA como derivação; só para dizer o número que a parede mede)
for r in J["resultados"]:
    if r["id"] in ("JUNO_207d", "SNO_plus", "SK_Gd_reator", "KamLAND", "Bari_2026a_NO"):
        print("inversão (não é derivação) %-14s E0 = %.4f eV" % (r["id"], math.sqrt(10 * r["mu"]) / 1e3 / (beta * math.sin(math.pi / 4))))
