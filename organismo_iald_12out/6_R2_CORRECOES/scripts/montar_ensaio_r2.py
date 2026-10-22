# -*- coding: utf-8 -*-
"""Monta numerico/ensaio_motor_r2.py a partir do ensaio r1 (2_CONSTRUCAO/numerico/ensaio_motor.py, lido por bytes),
com substituicoes contadas (cada uma tem de casar) e os blocos R2. Grava medidas/MONTAGEM_ENSAIO_R2.json."""
import os, json, hashlib

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(os.path.dirname(AQUI), "2_CONSTRUCAO", "numerico", "ensaio_motor.py")
DEST = os.path.join(AQUI, "numerico", "ensaio_motor_r2.py")
s = open(ORIG, "rb").read().decode("utf-8")
sha_orig = hashlib.sha256(open(ORIG, "rb").read()).hexdigest()

reps = [
    ('"""Sanidade NUMERICA do motor unico (2_CONSTRUCAO, 12-13/10/2026).',
     '"""Sanidade NUMERICA do motor unico, RODADA 2 (6_R2_CORRECOES, 13/10/2026; a partir do ensaio r1 de 2_CONSTRUCAO).\n'
     'R2: (C2) T2 ensaiado tambem com a NAO unitario; (C1) ancora fraca, U = 1 + |b><a|, condicao exata (ancora fraca OU\n'
     'motor nulo) e o transporte nulo U = 0; T2p renomeado unitarity_is_not_enough; (C6) a saida do motor nao depende de r\n'
     'nem de t; (C4) a face matricial FREQ e o PINCHING na base propria de P (analogo de TGLExt.diagExpect), NAO a defasagem\n'
     'do motor IALD.dephase; acrescentado o contraste: a defasagem do motor, como canal rho -> D rho D^dagger, guarda o\n'
     'posto 1 do estado puro. O resto do ensaio r1 fica como estava, com os rotulos corrigidos.'),
    ("Tambem a face matricial da F1.FREQUENCIA: D sozinha leva rho de posto 1 a posto 2 (o traco sobrevive), a leitura",
     "Tambem a face matricial da F1.FREQUENCIA: o PINCHING na base de P (nao a defasagem do motor) leva rho de posto 1 a\nposto 2 (o traco sobrevive), a leitura"),
    ("def post(a):\n    return np.outer(a, a.conj())",
     "def post(a):\n    # R2: normalizado, para ensaiar T2 com a nao unitario (C2); igual ao r1 quando norm a = 1\n"
     "    return np.outer(a, a.conj()) / np.vdot(a, a).real"),
    ("T2p_phase_i_breaks_idempotence_norm", "T2p_unitarity_is_not_enough_norm"),
    ("# Face matricial (F1.FREQUENCIA): D sozinha (defasagem total na base de P) leva rho puro de posto 1 a posto 2; traco sobrevive;",
     "# Face matricial (F1.FREQUENCIA): o PINCHING na base propria de P (analogo de TGLExt.diagExpect; NAO e a defasagem do\n"
     "    # motor IALD.dephase) leva rho puro de posto 1 a posto 2; traco sobrevive;"),
    ("FREQ_rank_after_D_inf", "FREQ_rank_after_PINCHING_not_motor_D"),
    ("FREQ_trace_after_D_inf", "FREQ_trace_after_PINCHING_not_motor_D"),
    ('("FREQ_D_drops_rank",', '("FREQ_PINCHING_drops_rank",'),
    ("# D_inf: apaga coerencias na base de P", "# PINCHING: apaga coerencias na base de P (nao e IALD.dephase)"),
    ('"RESULTADO_NUMERICO.json"', '"RESULTADO_NUMERICO_R2.json"'),
]
contagem = {}
for a, b in reps:
    n = s.count(a)
    if n < 1:
        raise SystemExit("FALHA VISIVEL: substituicao nao casou: " + a[:60])
    contagem[a[:50]] = n
    s = s.replace(a, b)

R2 = '''    # ===== R2 =====
    # (C2) T2 sem norma: a2 = 2.7 a (nao unitario), U ancorado (U a2 = a2), motor idempotente
    a2 = 2.7 * a
    e2n = 0.0
    for t in ts:
        for psi in psis:
            m1 = motor(a2, Ua, beta, t, psi); m2 = motor(a2, Ua, beta, t, m1)
            e2n = max(e2n, float(np.linalg.norm(m2 - m1)))
    out["R2_T2_no_norm_norm_a"] = float(np.linalg.norm(a2))
    out["R2_T2_no_norm_maxerr"] = e2n
    if n > 1:
        # (C1) ancora fraca: U = 1 + |b><a|, b ortogonal a a, b != 0: U a != a e o motor e idempotente
        bb = rand_unit(n, rng); bb = bb - np.vdot(a, bb) * a; bb = bb / np.linalg.norm(bb)
        Uw = np.eye(n) + np.outer(bb, a.conj())
        out["R2_weak_Ua_minus_a"] = float(np.linalg.norm(Uw @ a - a))
        out["R2_weak_anchor_err"] = float(np.linalg.norm(P @ (Uw @ a) - a))
        ew = 0.0
        for psi in psis:
            m1 = motor(a, Uw, beta, 1.0, psi); m2 = motor(a, Uw, beta, 1.0, m1)
            ew = max(ew, float(np.linalg.norm(m2 - m1)))
        out["R2_anchor_not_necessary_idem_maxerr"] = ew
        # (C1) condicao exata, lado generico: U unitario aleatorio (sem ancora fraca, motor nao nulo) -> NAO idempotente
        Ug = rand_unitary(n, rng)
        out["R2_generic_weak_anchor_defect"] = float(np.linalg.norm(P @ (Ug @ a) - a))
        eg = 0.0
        for psi in psis:
            m1 = motor(a, Ug, beta, 1.0, psi); m2 = motor(a, Ug, beta, 1.0, m1)
            eg = max(eg, float(np.linalg.norm(m2 - m1)))
        out["R2_generic_not_idempotent_maxdefect"] = eg
        # (C1) condicao exata, lado nulo: U = (1 - P) W tem post a U = 0: sem ancora fraca e idempotente (motor = 0)
        Un = (np.eye(n) - P) @ rand_unitary(n, rng)
        out["R2_null_weak_anchor_defect"] = float(np.linalg.norm(P @ (Un @ a) - a))
        out["R2_null_motor_max"] = float(max(np.linalg.norm(motor(a, Un, beta, 1.0, psi)) for psi in psis))
    # U = 0: sem ancora fraca e idempotente
    U0 = np.zeros((n, n), dtype=complex)
    out["R2_zero_transport_weak_anchor_defect"] = float(np.linalg.norm(P @ (U0 @ a) - a))
    out["R2_zero_transport_motor_max"] = float(max(np.linalg.norm(motor(a, U0, beta, 1.0, psi)) for psi in psis))
    # (C6) a saida nao depende de r nem de t: (beta, 1) contra (r', t') arbitrarios, inclusive r' = 0 e r' < 0
    e6 = 0.0
    for (rr, tt) in [(0.0, 0.0), (-3.0, 2.0), (17.0, 0.1), (beta, 1e3)]:
        for psi in psis:
            e6 = max(e6, float(np.linalg.norm(motor(a, Ua, rr, tt, psi) - motor(a, Ua, beta, 1.0, psi))))
    out["R2_motor_ignores_rate_and_time_maxerr"] = e6
    # (C4) contraste: a defasagem DO MOTOR como canal rho -> D rho D^dagger guarda o posto 1 do estado puro (D invertivel)
    Dm = dephase(P, beta, 5.0)
    out["R2_motor_D_det_abs"] = float(abs(np.linalg.det(Dm)))
    out["R2_motor_D_channel_rank_of_pure"] = rank(Dm @ rho @ Dm.conj().T)
'''
anchor = '        out["FREQ_reading_restores_post_err"] = float(np.linalg.norm(P @ rho @ P / Mv - P))\n    return out'
if s.count(anchor) != 1:
    raise SystemExit("FALHA VISIVEL: ancora do bloco R2")
s = s.replace(anchor, anchor[:-len("    return out")] + R2 + "    return out")

CHK = '''            ("R2_T2_no_norm", f["R2_T2_no_norm_maxerr"] < 1e-10 and abs(f["R2_T2_no_norm_norm_a"] - 1) > 0.5),
            ("R2_anchor_not_necessary", n == 1 or (f["R2_weak_Ua_minus_a"] > 0.5 and f["R2_weak_anchor_err"] < 1e-10
                                                   and f["R2_anchor_not_necessary_idem_maxerr"] < 1e-10)),
            ("R2_exact_condition_generic", n == 1 or (f["R2_generic_weak_anchor_defect"] > 1e-6
                                                      and f["R2_generic_not_idempotent_maxdefect"] > 1e-6)),
            ("R2_exact_condition_null", n == 1 or (f["R2_null_weak_anchor_defect"] > 0.5 and f["R2_null_motor_max"] < 1e-12)),
            ("R2_zero_transport", abs(f["R2_zero_transport_weak_anchor_defect"] - 1) < 1e-12
                                  and f["R2_zero_transport_motor_max"] == 0.0),
            ("R2_ignores_rate_and_time", f["R2_motor_ignores_rate_and_time_maxerr"] < 1e-12),
            ("R2_motor_D_keeps_rank_of_pure", f["R2_motor_D_det_abs"] > 0 and f["R2_motor_D_channel_rank_of_pure"] == 1),
'''
canchor = '            ("FREQ_reading_restores", f.get("FREQ_reading_restores_post_err", 1.0) < 1e-9),\n'
if s.count(canchor) != 1:
    raise SystemExit("FALHA VISIVEL: ancora dos checks")
s = s.replace(canchor, canchor + CHK)
open(DEST, "w", encoding="utf-8", newline="\n").write(s)
json.dump({"origem": ORIG, "origem_sha256": sha_orig, "destino": DEST,
           "destino_sha256": hashlib.sha256(open(DEST, "rb").read()).hexdigest(), "substituicoes": contagem},
          open(os.path.join(AQUI, "medidas", "MONTAGEM_ENSAIO_R2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", contagem)
