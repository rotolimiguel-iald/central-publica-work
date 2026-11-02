from math import exp, pi, sqrt

U = 1.602176634e-19       # J, unidade alvo usada apenas como requisito condicional
hbar = 1.054571817e-34   # J s
c = 299792458.0
G = 6.67430e-11
g = 9.80665
kB = 1.380649e-23
Estar = exp(0.5) * U
K = Estar**3 / hbar**2
M = K / (6 * g**2)
Omega_star = Estar / hbar
f_star = Omega_star / (2 * pi)
tau = 4 * pi * G * U / c**5
kappa = 2 * pi * U / hbar
T_U = U / kB

print(f"E_star={Estar:.12e} J")
print(f"K_necessario={K:.12e} J/s^2")
print(f"M_se_K_6Mg2={M:.12e} kg")
print(f"Omega_star={Omega_star:.12e} s^-1")
print(f"f_star={f_star:.12e} Hz")
print(f"tau_estrela={tau:.12e} s")
print(f"kappa={kappa:.12e} s^-1")
print(f"T_U={T_U:.9f} K")
