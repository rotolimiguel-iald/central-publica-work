# Tamanho do efeito de laboratorio da lei de dephasing da TGL, Gamma_w = 1/2 * beta * tau_star * w^2, no ramo canonico tau_star = t_Planck.
# beta NUNCA literal: ALPHA_FINE_CODATA_2018 * sqrt(e) em runtime. Sensibilidades: [KNOWN, ordem de grandeza] -- Kimi deve fontear cada uma.
import math, json
ALPHA = 7.2973525693e-3          # CODATA 2018
T_PLANCK = 5.391247e-44          # s, CODATA 2018
HBAR_EVS = 6.582119569e-16       # eV s
C = 299792458.0
beta = ALPHA * math.sqrt(math.e)
def gamma(w): return 0.5 * beta * T_PLANCK * w * w
rows = []
def add(nome, w, sens, nota):
    g = gamma(w); rows.append(dict(canal=nome, omega_rad_s=w, Gamma_TGL_s=g, sensibilidade_s=sens, ordens_de_grandeza=math.log10(sens/g), nota=nota))
# neutrinos: n=-2 -> omega = Dm^2/(2E hbar)
add("neutrino DUNE E=1 GeV, Dm31^2=2.5e-3 eV^2", 2.5e-3/(2*1e9)/HBAR_EVS, 1e-23/6.582119569e-25, "sens.: cota de decoerencia ~1e-23 GeV (KNOWN, ordem) convertida a s^-1")
add("neutrino JUNO E=3 MeV, Dm21^2=7.5e-5 eV^2", 7.5e-5/(2*3e6)/HBAR_EVS, 1e-23/6.582119569e-25, "idem")
add("ringdown LIGO f=250 Hz", 2*math.pi*250, 50.0, "sens.: 1/tau_QNM ~ 250 s^-1 medido a ~20% -> dGamma ~ 50 s^-1 (KNOWN, ordem)")
add("NANOGrav f=1e-8 Hz", 2*math.pi*1e-8, 1e-9, "sens. simbolica 1e-9 s^-1 (1/30 anos); irrelevante: o efeito e ~1e-60")
add("relogio optico Sr 429 THz", 2*math.pi*4.29e14, 1e-2, "sens.: coerencia ~100 s -> dGamma ~ 1e-2 s^-1 (KNOWN, ordem)")
add("relogio nuclear Th-229 2.02 PHz", 2*math.pi*2.020e15, 1e-3, "sens.: aspiracao mHz em ion (KNOWN, ordem); estado da arte solido ~kHz")
add("Moessbauer Fe-57 14.4 keV", 14.4e3/HBAR_EVS, 7e6, "sens.: largura natural 1/141 ns ~ 7e6 s^-1")
# escala cosmologica, para contraste: beta entra como fracao/expoente O(1)
cosmo = dict(piso_dos_vazios_rho_min_sobre_rho_barra=beta, expoente_razao_de_hubble_2beta_3=2*beta/3)
# cota em tau_star se beta fixo e o relogio Th a mHz nao ve nada
tau_bound_Th = 2*1e-3/(beta*(2*math.pi*2.020e15)**2)
out = dict(beta=beta, t_planck=T_PLANCK, linhas=rows, contraste_cosmologico=cosmo, cota_tau_star_Th_mHz_s=tau_bound_Th, cota_sobre_t_planck=tau_bound_Th/T_PLANCK)
p = "C:/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/poder_5sigma_fora_cosmo.json"
json.dump(out, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("beta =", beta)
for r in rows:
    print("%-48s omega=%.3e  Gamma_TGL=%.2e s^-1  sens=%.1e  faltam %.1f ordens" % (r["canal"], r["omega_rad_s"], r["Gamma_TGL_s"], r["sensibilidade_s"], r["ordens_de_grandeza"]))
print("cosmo:", cosmo)
print("cota tau_star (Th a mHz, beta fixo): %.2e s = %.1e t_Planck" % (tau_bound_Th, tau_bound_Th/T_PLANCK))
