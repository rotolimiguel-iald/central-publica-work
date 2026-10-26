    I = ONE * np.eye(2); omega_I = float(np.trace(I) / 2.0)
    TWO = ONE + ONE; HALF = ONE / TWO; FOUR = TWO + TWO
    PI = 4.0 * np.arctan(ONE); SQRT_E = np.exp(HALF)
    # Meia-Nat derivada: x = 1 - x => x = 1/2
    x = HALF; mn_resid = abs((ONE - x) - x)
    S_boundary = HALF; w_max = HALF
    s_can = ONE / (FOUR * PI)
