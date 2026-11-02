from math import pi

E_J = 1.602176634e-19
c = 299792458.0
G = 6.674e-11
beta = 0.012031300400803142

m_kg = E_J / c**2
q_m = G * E_J / c**4
flux_m = 4 * pi * q_m
R_B_m = flux_m / beta

print(f"m_equiv_kg={m_kg:.15e}")
print(f"q_monopolo_m={q_m:.15e}")
print(f"fluxo_4piq_m={flux_m:.15e}")
print(f"R_B_se_fluxo_beta_R_m={R_B_m:.15e}")
