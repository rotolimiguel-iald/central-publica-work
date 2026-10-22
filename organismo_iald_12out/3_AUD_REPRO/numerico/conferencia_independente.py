# -*- coding: utf-8 -*-
"""Conferencia numerica INDEPENDENTE do auditor (nao reusa ensaio_motor.py). beta de runtime (linha unica do um.py)."""
import re, math, json, numpy as np
U = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/um.py"
al = [ln for ln in open(U, "rb") if re.match(rb"^ALPHA_FINE_CODATA_2018\s*=", ln)]
assert len(al) == 1
beta = float(al[0].split(b"=")[1]) * math.sqrt(math.e)
rng = np.random.default_rng(20261013)
out = {"beta": repr(beta)}
for n in (2, 5):
    a = np.zeros(n, complex); a[0] = 1
    P = np.outer(a, a.conj())
    D = lambda t: P + math.exp(-beta * t) * (np.eye(n) - P)
    # U unitario ancorado: bloco 1 em a, unitario aleatorio no complemento
    Z = rng.normal(size=(n-1, n-1)) + 1j * rng.normal(size=(n-1, n-1)); Q, _ = np.linalg.qr(Z)
    Ua = np.eye(n, dtype=complex); Ua[1:, 1:] = Q
    motor = lambda Uop, t: P @ D(t) @ Uop
    M = motor(Ua, 3.0)
    out[f"n{n}_T2_idem_err"] = float(np.abs(M @ M - M).max())
    Ui = 1j * np.eye(n)
    Mi = motor(Ui, 0.0)
    out[f"n{n}_T2p_norm_motor2a_minus_motora"] = float(np.linalg.norm(Mi @ Mi @ a - Mi @ a))
    # sonda A1 numerica: U = 1 + |b><a| nao ancora e e idempotente
    b = np.zeros(n, complex); b[1] = 1
    Unc = np.eye(n) + np.outer(b, a.conj())
    Mn = motor(Unc, 3.0)
    out[f"n{n}_A1_Ua_minus_a"] = float(np.linalg.norm(Unc @ a - a)); out[f"n{n}_A1_idem_err"] = float(np.abs(Mn @ Mn - Mn).max())
    out[f"n{n}_T8_norm_D50_minus_P"] = float(np.linalg.norm(D(50) - P, 2)); out[f"n{n}_T8_esperado_e^-50b"] = math.exp(-50 * beta)
    F1 = D(1); out[f"n{n}_T9_spec_norm_F1sq_minus_F1"] = float(np.linalg.norm(F1 @ F1 - F1, 2))
    out[f"n{n}_T9_esperado"] = abs(math.exp(-2 * beta) - math.exp(-beta))
    psi = rng.normal(size=n) + 1j * rng.normal(size=n); psi /= np.linalg.norm(psi)
    m = (psi.conj() @ P @ psi).real; out[f"n{n}_T5_memoria_aleatoria"] = m
    out[f"n{n}_B1_memoria_de_zero"] = float((np.zeros(n).conj() @ P @ np.zeros(n)).real)
json.dump(out, open("numerico/CONFERENCIA_INDEPENDENTE.json", "w", encoding="utf-8"), indent=1)
for k, v in out.items(): print(k, v)
