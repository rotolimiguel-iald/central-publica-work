from math import pi, sqrt

alpha = 7.2973525693e-3
e = 2.718281828459045
beta = alpha * e**0.5
c = 299792458.0
G = 6.674e-11
tP = 5.391247e-44
hbar = 1.054571817e-34
E0 = 1.602176634e-19
ellP = c * tP
EP = (hbar * c**5 / G)**0.5

R_B = c * tP / beta
q = c * tP / (4 * pi)
E = c**4 * q / G
tau_needed = 4 * pi * G * E0 / c**5

print(f"beta={beta:.15e}")
print(f"R_B_nativa={R_B:.12e} m")
print(f"R_B_em_lP={R_B/ellP:.9f}")
print(f"q_nativa={q:.12e} m")
print(f"q_em_lP={q/ellP:.9f}")
print(f"E_nativa={E:.12e} J = {E/E0:.12e} eV")
print(f"E_P_sobre_4pi={EP/(4*pi):.12e} J")
print(f"tau_estrela_para_1eV={tau_needed:.12e} s = {tau_needed/tP:.12e} tP")
