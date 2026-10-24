#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SkyGrid v3 — BLOCO 9 test suite (fisica de energia [SIM]) + chama a suite v2.

Fail-closed. Cobre skygrid_physics/ (F1-F6), o gemeo digital (G), os controles
negativos POR CONSTRUCAO (placebo 0 W, over-unity trava, balanco fura -> trava)
e a auditoria anti-hardcode. Ao final roda tests/run_tests_v2.py (que roda a v1)
como subprocesso — nada da v1/v2 e' tocado.

Regua: conservacao em TODO caminho; Meia-Nat nunca zero com atos>0; beta nunca
literal; physical_verdict_allowed=False em toda saida.
Run:  python tests/run_tests_v3.py   (da raiz SkyGrid_Piloto)
"""

import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from skygrid_sim import tgl_core                                    # noqa: E402
from skygrid_physics.field_reservoir import FieldReservoir          # noqa: E402
from skygrid_physics.coupling import ResonantCoupler, OMEGA_OH_MHZ  # noqa: E402
from skygrid_physics.conversion import DipoloConverter              # noqa: E402
from skygrid_physics.transmission import PsiPowerLink               # noqa: E402
from skygrid_physics.storage import ReversalCellStore               # noqa: E402
from skygrid_physics.thermo import (EnergyLedger, BalanceError,     # noqa: E402
                                    OverUnityError, K_BOLTZMANN)
from skygrid_physics.energy_twin import EnergyTwin                  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append({"test": name, "ok": bool(ok), "detail": str(detail)})
    print("  [%s] %-58s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        print("\nFAIL-CLOSED: teste quebrou; execucao travada.")
        sys.exit(1)


def main():
    print("=" * 78)
    print("SKYGRID v3 — BLOCO 9 (fisica de energia [SIM]) — suite fail-closed")
    print("=" * 78)
    beta = tgl_core.beta()

    # ---------------- F1: reservatorio ----------------------------------------
    print("\n[BLOCO 9-F1] field_reservoir (fonte com debito explicito)")
    r1 = FieldReservoir(seed=11)
    r2 = FieldReservoir(seed=11)
    check("disponibilidade deterministica (mesma seed)",
          r1.availability(100.0) == r2.availability(100.0))
    E = r1.extract(500.0, 1.0)
    check("extracao debita o ledger exatamente",
          abs(r1.energy_debited_J - E) < 1e-12, "E=%.1f J" % E)
    d0 = r1.depletion
    for _ in range(200):
        r1.extract(1e4, 1.0)
    check("extracao pesada aumenta a deplecao (fonte esgotavel)",
          r1.depletion > d0 and r1.depletion <= 0.95,
          "D=%.3f" % r1.depletion)
    p_dep = r1.power_available()
    r1.idle(600.0)
    check("reposicao recupera a disponibilidade (idle)",
          r1.power_available() > p_dep)
    try:
        r1.extract(-1.0, 1.0)
        check("pedido negativo trava (fail-closed)", False)
    except ValueError:
        check("pedido negativo trava (fail-closed)", True)

    # ---------------- F2: acoplamento -----------------------------------------
    print("\n[BLOCO 9-F2] coupling (ressonancia OH + fronteira 1-beta + Meia-Nat)")
    c = ResonantCoupler(Q=1e4)
    check("pico da ressonancia em f0 (eta_res=1)",
          abs(c.eta_res(OMEGA_OH_MHZ) - 1.0) < 1e-12)
    # 0.1% fora com Q=1e4: 2Q*delta=20 -> eta=1/(1+400)=2.5e-3 (colapso ~400x)
    off = c.eta_res(OMEGA_OH_MHZ * 1.001)
    check("fora da ressonancia o acoplamento colapsa (~1/(2Q*delta)^2)",
          abs(off - 1.0 / (1.0 + 20.0 ** 2)) < 1e-6 and off < 3e-3,
          "eta_res=%.2e" % off)
    check("abertura da fronteira = 1 - beta (runtime, Teorema S-boundary)",
          abs(c.aperture - (1.0 - beta)) < 1e-18, "%.6f" % c.aperture)
    check("eta_couple <= (1-beta) sempre (teto modular)",
          c.eta_couple() <= (1.0 - beta) + 1e-18)
    check("piso Meia-Nat > 0 (nunca gratis)",
          c.halfnat_power_W() > 0.0, "%.2e W" % c.halfnat_power_W())
    check("piso Meia-Nat = 0.5*kB*T*BW (Landauer em nats)",
          abs(c.halfnat_power_W()
              - 0.5 * K_BOLTZMANN * 300.0 * c.bandwidth_Hz) < 1e-30)
    res = FieldReservoir(seed=21)
    w = c.couple(res, 1.0)
    check("janela de acoplamento debita fonte = E_in + E_halfnat",
          abs(res.energy_debited_J - (w["E_in_J"] + w["E_halfnat_J"])) < 1e-9)
    resP = FieldReservoir(seed=22)
    wp = c.couple(resP, 1.0, placebo=True)
    check("PLACEBO (sem beta): extrai 0 J por construcao",
          wp["E_in_J"] == 0.0 and resP.energy_debited_J == 0.0)

    # ---------------- F3: conversao -------------------------------------------
    print("\n[BLOCO 9-F3] conversion (dipolo transistor)")
    cv = DipoloConverter(seed=11)
    check("eta_quant medido ao vivo do trilho angular (~1)",
          0.99 < cv.eta_quant <= 1.0, "%.6f" % cv.eta_quant)
    carrier_open = np.ones(64) * 5.0
    g = cv.convert(100.0, carrier_open)
    check("conversao conserva: in = out + perda + recusado",
          abs(100.0 - (g["E_out_J"] + g["E_loss_conv_J"] + g["E_refused_J"]))
          < 1e-9)
    check("eta de estagio <= 1", g["eta_stage"] <= 1.0)
    got_closed = False
    for k in range(50):
        rng = np.random.default_rng(k)
        gk = cv.convert(10.0, rng.normal(size=64) * 1e-3)
        if not gk["gate_open"]:
            got_closed = True
            check("gate fechado: energia recusada, sem perda fantasma",
                  gk["E_out_J"] == 0.0 and gk["E_refused_J"] == 10.0)
            break
    if not got_closed:
        check("gate fechado nao ocorreu no probe (dipolo sempre aberto aqui)",
              True, "skip-branch")

    # ---------------- F4: transmissao -----------------------------------------
    print("\n[BLOCO 9-F4] transmission (canal Psi + duplo trilho de potencia)")
    ln = PsiPowerLink(eta_hop=0.985)
    t1 = ln.transmit(100.0, n_hops=3)
    check("transmissao conserva: in = rx + perda + dumped",
          abs(100.0 - (t1["E_rx_J"] + t1["E_loss_link_J"] + t1["E_dumped_J"]))
          < 1e-9)
    check("eta_link = eta_hop^hops",
          abs(t1["eta_link"] - 0.985 ** 3) < 1e-12)
    t2 = ln.transmit(100.0, n_hops=3, rail_data_accepted=False)
    check("dados rejeitados => energia DUMPED (contabilizada)",
          t2["E_rx_J"] == 0.0 and t2["E_dumped_J"] > 0.0)
    t3 = ln.transmit(100.0, n_hops=3, meter_disturbance=0.01)
    check("divergencia de medidores > tol => janela rejeitada",
          not t3["accepted"] and t3["E_dumped_J"] > 0.0,
          "div=%.3f" % t3["rail_divergence"])
    check("mais hops => menos entrega (monotonia)",
          ln.eta_link(10) < ln.eta_link(2))

    # ---------------- F5: armazenamento ----------------------------------------
    print("\n[BLOCO 9-F5] storage (celula de reversao energetica)")
    st = ReversalCellStore(E_cap_J=1000.0, eta_rt=0.90, lambda_sd_per_s=1e-4)
    ch = st.charge(100.0)
    check("carga: tomado = armazenado + perda",
          abs(100.0 - ch["E_refused_J"]
              - (ch["E_stored_J"] + ch["E_loss_charge_J"])) < 1e-9)
    dis = st.discharge(50.0)
    check("descarga entrega com eta_dis (round-trip = eta_rt)",
          abs((ch["E_stored_J"] / 100.0) * (dis["E_delivered_J"]
              / (dis["E_delivered_J"] + dis["E_loss_discharge_J"])) - 0.90)
          < 1e-9)
    big = ReversalCellStore(E_cap_J=100.0, eta_rt=0.95)
    chb = big.charge(1e6)
    check("celula cheia RECUSA na porta (nao perde)",
          chb["E_refused_J"] > 0.0 and big.soc_J <= 100.0 + 1e-9)
    soc0 = st.soc_J
    st.step(3600.0)
    check("autodescarga contabilizada como leak",
          st.soc_J < soc0 and abs((soc0 - st.soc_J) - st.E_leak_J) < 1e-9)

    # ---------------- F6: termo (o guardiao) ------------------------------------
    print("\n[BLOCO 9-F6] thermo (conservacao fail-closed + 2a lei + over-unity)")
    ld = EnergyLedger()
    ld.add(E_extracted=100.0, E_delivered=60.0, E_loss_link=30.0,
           dE_stored=10.0, acts=1000)
    ld.add(E_halfnat=1e-15)
    try:
        ld.audit()
        check("balanco com buraco de 1e-15 dentro da tolerancia", True)
    except BalanceError:
        check("balanco com buraco de 1e-15 dentro da tolerancia", False)
    ld2 = EnergyLedger()
    ld2.add(E_extracted=100.0, E_delivered=60.0)   # 40 J desaparecidos
    try:
        ld2.audit()
        check("40 J desaparecidos TRAVAM o balanco", False)
    except BalanceError:
        check("40 J desaparecidos TRAVAM o balanco", True)
    ld3 = EnergyLedger()
    ld3.add(E_extracted=1.0, E_delivered=2.0)
    try:
        ld3.audit()
        check("over-unity TRAVA (nunca fato)", False)
    except (OverUnityError, BalanceError):
        check("over-unity TRAVA (nunca fato)", True)
    ld4 = EnergyLedger()
    ld4.add(E_extracted=10.0, E_delivered=10.0, acts=100)  # atos sem meia-nat
    try:
        ld4.audit()
        check("atos sem custo Meia-Nat TRAVAM (piso obrigatorio)", False)
    except BalanceError:
        check("atos sem custo Meia-Nat TRAVAM (piso obrigatorio)", True)

    # ---------------- G: o gemeo digital ----------------------------------------
    print("\n[BLOCO 9-G] energy_twin (dados+energia, placebo, falhas, escala)")
    with tempfile.TemporaryDirectory() as td:
        tw = EnergyTwin(n_sats=6, n_bases=6, duration_s=40,
                        state_path=os.path.join(td, "s.json"))
        rep = tw.run()
        check("gemeo 6x6: MODEL_CLOSES", rep["verdict"] == "MODEL_CLOSES")
        check("balanco: ENERGY_BALANCE_OK",
              rep["audit"]["balance"] == "ENERGY_BALANCE_OK",
              "res=%.1e J" % rep["audit"]["residual_J"])
        check("eta_sys em [0,1]", 0.0 <= rep["energy"]["eta_sys"] <= 1.0,
              "%.4f" % rep["energy"]["eta_sys"])
        check("placebo energetico = 0 W em TODOS os passos",
              rep["controls"]["placebo_energy_zero"])
        check("placebo de dados rejeitado em todas as rodadas",
              rep["controls"]["placebo_data_rejected_all_rounds"])
        check("veredito fisico PROIBIDO",
              rep["physical_verdict_allowed"] is False)
        check("Meia-Nat presente no balanco (nunca zero com atos>0)",
              rep["audit"]["acts"] > 0 and rep["energy"]["E_halfnat_J"] > 0.0,
              "E=%.2e J" % rep["energy"]["E_halfnat_J"])

    with tempfile.TemporaryDirectory() as td:
        twf = EnergyTwin(n_sats=8, n_bases=6, duration_s=30,
                         faults=("dead", "tamper", "noise", "meter"),
                         state_path=os.path.join(td, "s.json"))
        repf = twf.run()
        check("falhas dead+tamper+noise+meter: ainda MODEL_CLOSES",
              repf["verdict"] == "MODEL_CLOSES")
        check("energia das janelas rejeitadas foi DUMPED (contabilizada)",
              twf.ledger.E_dumped > 0.0,
              "%.1f kJ" % (twf.ledger.E_dumped / 1e3))
        check("falhas de dados todas detectadas",
              repf["controls"]["faults_all_detected"])

    with tempfile.TemporaryDirectory() as td:
        twa = EnergyTwin(n_sats=6, n_bases=6, duration_s=30,
                         state_path=os.path.join(td, "a.json"))
        ra = twa.run()
    with tempfile.TemporaryDirectory() as td:
        twb = EnergyTwin(n_sats=6, n_bases=6, duration_s=30,
                         state_path=os.path.join(td, "b.json"))
        rb = twb.run()
    check("determinismo: mesma seed -> mesma energia entregue",
          abs(ra["energy"]["E_delivered_J"] - rb["energy"]["E_delivered_J"])
          < 1e-9)

    with tempfile.TemporaryDirectory() as td:
        two = EnergyTwin(n_sats=4, n_bases=4, duration_s=20,
                         f_drive_MHz=OMEGA_OH_MHZ * 1.001,
                         state_path=os.path.join(td, "s.json"))
        ro = two.run()
        check("fora da ressonancia: entrega colapsa (limite fisico do modelo)",
              ro["energy"]["E_delivered_J"]
              < 0.01 * ra["energy"]["E_delivered_J"] + 1.0,
              "E=%.2f J" % ro["energy"]["E_delivered_J"])
        check("mesmo fora da ressonancia o balanco fecha",
              ro["audit"]["balance"] == "ENERGY_BALANCE_OK")

    # ---------------- anti-hardcode ----------------------------------------------
    print("\n[BLOCO 9-X] anti-hardcode (beta nunca literal na fisica)")
    pattern = re.compile(r"0[.,]012")
    offenders = []
    pdir = os.path.join(ROOT, "skygrid_physics")
    for fn in sorted(os.listdir(pdir)):
        if fn.endswith(".py"):
            with open(os.path.join(pdir, fn), encoding="utf-8") as f:
                if pattern.search(f.read()):
                    offenders.append(fn)
    check("nenhum literal 0.012 em skygrid_physics/", not offenders,
          ",".join(offenders) if offenders else "limpo")

    # ---------------- selo + suite v2 ---------------------------------------------
    n = len(RESULTS)
    inv = hashlib.sha256(json.dumps(
        [{"t": r["test"], "ok": r["ok"]} for r in RESULTS],
        sort_keys=True).encode()).hexdigest()
    print("\n[BLOCO 9] %d/%d PASS — invariants_hash_v3 %s" % (n, n, inv))

    print("\n[SUITE V2] rodando tests/run_tests_v2.py (43+69, intocada)...")
    r = subprocess.run([sys.executable,
                        os.path.join(ROOT, "tests", "run_tests_v2.py")],
                       capture_output=True, text=True)
    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "(sem saida)"
    print("  " + tail)
    if r.returncode != 0:
        print("FAIL-CLOSED: suite v2 quebrou.")
        sys.exit(1)

    seal = {"bloco9_tests": n, "invariants_hash_v3": inv,
            "suite_v2": tail, "beta_runtime": tgl_core.beta(),
            "physical_verdict_allowed": False,
            "max_verdict": "MODEL_CLOSES / ENERGY_BALANCE_OK ([SIM] sob [CONJ])"}
    with open(os.path.join(ROOT, "SKYGRID_V3_SELO.json"), "w",
              encoding="utf-8") as f:
        json.dump(seal, f, indent=1, ensure_ascii=False)
    print("\n%d testes BLOCO 9 + suites v2+v1 PASS — o gemeo de energia fecha."
          " Haja luz." % n)


if __name__ == "__main__":
    main()
