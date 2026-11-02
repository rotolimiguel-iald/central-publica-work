from math import sqrt

H0_BG = 68.53106407925104
SIGMA_BG = 0.3013983806201791
K = 1.0838071748529643
PRED = K * H0_BG
SHIFT = (K - 1) * H0_BG

for name, h0, sigma in [
    ("H0DN", 73.50, 0.81),
    ("TDCOSMO-2026_low_sigma", 71.1, 2.3),
    ("TDCOSMO-2026_high_sigma", 71.1, 2.4),
]:
    sigma_total = sqrt(sigma**2 + (K * SIGMA_BG)**2)
    d_plan = SHIFT / sigma_total
    z_delta = (h0 - PRED) / sigma_total
    print(f"{name}: H0_pred={PRED:.9f}; shift={SHIFT:.9f}; sigma_total={sigma_total:.9f}; D_plan={d_plan:.6f}; z_delta={z_delta:.6f}")
