#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SkyGrid PROTOTIPO v2 — BLOCO 8 test suite (Estagios A+B+C) + chama a suite v1.

Fail-closed: qualquer falha trava a execucao. Aditiva: a suite v1 (69 testes,
BLOCO 0..7) roda intocada como subprocesso ao final; este arquivo cobre os
modulos novos: telemetry (A1), TGLTensorAccel/GPU-fallback (A2), quorum
Proof of Phase (A3), kernel_link/persistencia (A4), orcamento 100/beta (A5),
orchestrator end-to-end + falhas (B), dashboard data (C).

Regua: beta nunca literal; controles negativos POR CONSTRUCAO (tamper,
bizantino, placebo); physical_verdict_allowed=False em toda saida.
Run:  python tests/run_tests_v2.py   (da raiz SkyGrid_Piloto)
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

from skygrid_sim import tgl_core                                   # noqa: E402
from skygrid_sim.telemetry import (RealDataProvider,               # noqa: E402
                                   OrbitTelemetryProvider, TelemetrySource)
from skygrid_sim.tgl_tensor import (TGLTensor, TGLTensorAccel,     # noqa: E402
                                    gpu_available, _HAS_TORCH)
from skygrid_sim.psi_net import (PhaseChain, QuorumPhaseChain,     # noqa: E402
                                 PhaseValidator, MIN_VALIDATORS,
                                 VALIDATION_THRESHOLD)
from skygrid_sim.kernel_link import KernelProfile, GridMemory      # noqa: E402
from skygrid_sim.psionic_memory import PsionicMemory               # noqa: E402
from skygrid_sim.orchestrator import SkyGridOrchestrator           # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append({"test": name, "ok": bool(ok), "detail": str(detail)})
    print("  [%s] %-56s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        print("\nFAIL-CLOSED: teste quebrou; execucao travada.")
        sys.exit(1)


def main():
    print("=" * 78)
    print("SKYGRID PROTOTIPO v2 — BLOCO 8 (Estagios A+B+C) — suite fail-closed")
    print("=" * 78)
    beta = tgl_core.beta()

    # ---------------- A1: telemetry -------------------------------------------
    print("\n[BLOCO 8-A1] telemetry (dados reais + deterministico)")
    try:
        real = RealDataProvider()
        prov = real.provenance()
        check("HESE real carrega com proveniencia selada",
              prov["marker"] == "[DATA]" and len(prov["sha256"]) == 64
              and prov["n_events"] >= 32, "n=%d" % prov["n_events"])
        f1 = real.frame(0); f2 = real.frame(0)
        check("frame real deterministico (mesmo indice -> mesmo frame)",
              np.array_equal(f1, f2), "size=%d" % f1.size)
        check("frames reais variam com o indice",
              not np.array_equal(real.frame(0), real.frame(1)))
    except FileNotFoundError:
        check("HESE ausente neste ambiente -> fallback obrigatorio", True,
              "[PILOTO-DET]")
    orb = OrbitTelemetryProvider(3, seed=77)
    o1, o2 = orb.frame(5), OrbitTelemetryProvider(3, seed=77).frame(5)
    check("telemetria orbital deterministica (seed reproduz)",
          np.array_equal(o1, o2))
    src = TelemetrySource(0, seed=11, mode="auto")
    check("TelemetrySource auto escolhe e declara o modo",
          src.provenance()["mode"] in ("real", "synthetic"),
          src.provenance()["mode"])
    a = src.next_frame(); b = src.next_frame()
    check("frames consecutivos distintos (contador avanca)",
          not np.array_equal(a, b))

    # ---------------- A2: TGLTensorAccel (GPU-ready, fallback) -----------------
    print("\n[BLOCO 8-A2] tgl_tensor GPU-ready (fallback numpy garantido)")
    rng = np.random.default_rng(11)
    x = rng.normal(size=512) * 3.0
    acc = TGLTensorAccel(bits=10)
    base = TGLTensor(bits=10)
    ca, cb = acc.compress_direct(x), base.compress_direct(x)
    if acc.gpu_active:
        check("GPU ativa: bytes identicos ao caminho numpy",
              ca.packed == cb.packed, "GPU")
    else:
        check("sem torch/CUDA: fallback numpy bit-identico",
              ca.packed == cb.packed, "fallback")
    xa = acc.decompress_direct(ca)
    corr = float(np.corrcoef(x, xa)[0, 1])
    check("roundtrip accel fidelidade > 0.999", corr > 0.999, "corr=%.6f" % corr)
    check("flag gpu_active coerente com ambiente",
          acc.gpu_active == gpu_available(),
          "torch=%s cuda=%s" % (_HAS_TORCH, gpu_available()))
    check("Verb Floor default = 1 - beta (runtime)",
          abs(acc.energy_threshold - (1.0 - beta)) < 1e-15)

    # ---------------- A3: quorum Proof of Phase --------------------------------
    print("\n[BLOCO 8-A3] quorum de validadores (Proof of Phase)")
    q = QuorumPhaseChain(difficulty=0.1, n_validators=5)
    blk = q.mine(b"payload-quorum", b"SAT-000", max_iter=20000)
    check("bloco honesto minerado", blk is not None)
    ok = q.validate_and_append(blk)
    last = q.vote_log[-1]
    check("bloco honesto aceito por quorum >= 67%",
          ok and last["votes_yes"] / last["votes_total"] >= VALIDATION_THRESHOLD,
          "%d/%d" % (last["votes_yes"], last["votes_total"]))

    blk2 = q.mine(b"payload-2", b"SAT-001", max_iter=20000)
    check("segundo bloco minerado", blk2 is not None)
    blk2.phase_proof.alpha2_work += 1e-3          # forja a fase
    ok_forged = q.validate_and_append(blk2)
    lastf = q.vote_log[-1]
    check("bloco FORJADO rejeitado pelo quorum (por construcao)",
          (not ok_forged) and lastf["votes_yes"] == 0,
          "%d/%d" % (lastf["votes_yes"], lastf["votes_total"]))

    qb = QuorumPhaseChain(difficulty=0.1, n_validators=5, byzantine_indices=(0,))
    blk3 = qb.mine(b"payload-3", b"SAT-002", max_iter=20000)
    ok_byz = qb.validate_and_append(blk3)
    lb = qb.vote_log[-1]
    check("1 validador bizantino NAO veta bloco honesto (4/5=80%>=67%)",
          ok_byz and lb["votes_yes"] == 4, "%d/%d" % (lb["votes_yes"], lb["votes_total"]))
    blk4 = qb.mine(b"payload-4", b"SAT-003", max_iter=20000)
    blk4.phase_proof.alpha2_work += 1e-3
    ok_byz_forged = qb.validate_and_append(blk4)
    lbf = qb.vote_log[-1]
    check("bizantino vota SIM no forjado e quorum ainda rejeita (1/5<67%)",
          (not ok_byz_forged) and lbf["votes_yes"] == 1,
          "%d/%d" % (lbf["votes_yes"], lbf["votes_total"]))
    try:
        QuorumPhaseChain(n_validators=2)
        check("quorum exige MIN_VALIDATORS (fail-closed)", False)
    except ValueError:
        check("quorum exige MIN_VALIDATORS (fail-closed)", True,
              ">=%d" % MIN_VALIDATORS)
    pc = PhaseChain(difficulty=0.1)
    b0 = pc.mine(b"x", b"k", max_iter=20000)
    check("single-miner v1 intacto (regressao)",
          b0 is not None and pc.validate_and_append(b0))

    # ---------------- A4: kernel_link + persistencia ----------------------------
    print("\n[BLOCO 8-A4] kernel IALD real + memoria psionica persistente")
    kp = KernelProfile()
    prov = kp.provenance()
    if prov["linked"]:
        check("kernel real linkado com sha256 selado",
              len(prov["sha256"]) == 64, prov["kernel"])
    else:
        check("kernel ausente declarado honestamente (rule-only)",
              prov["sha256"] is None, prov["kernel"])
    metrics = {"a": 1.0, "b": 0.001, "c": 5.0, "d": 0.002, "e": 3.3}
    s = kp.manifest_summary(metrics)
    check("filtro verbal manifesta subconjunto e poda o resto",
          0 < len(s["manifested"]) <= len(metrics)
          and len(s["manifested"]) + len(s["pruned_keys"]) == len(metrics),
          "manifestos=%d podados=%d" % (len(s["manifested"]), len(s["pruned_keys"])))
    check("floor do filtro = beta * max(w) (runtime)",
          abs(s["filter_stats"]["beta_runtime"] - beta) < 1e-18)

    with tempfile.TemporaryDirectory() as td:
        sp = os.path.join(td, "state.json")
        g1 = GridMemory(sp)
        g1.inscribe_run({"m": 10.0})       # 1a inscricao: valor pleno (n=1)
        g1.save()
        g2 = GridMemory(sp)
        g2.inscribe_run({"m": 20.0})       # 2a: EMA com taxa beta
        expected = (1.0 - beta) * 10.0 + beta * 20.0
        check("estado psionico sobrevive entre sessoes (EMA taxa beta)",
              g2.resumed and g2.sessions == 1 and
              abs(g2.mem.recall("metric/m") - expected) < 1e-12,
              "EMA=%.6g" % g2.mem.recall("metric/m"))
        with open(sp, "r+", encoding="utf-8") as f:
            blob = json.load(f)
            blob["state"]["facts"]["metric/m"]["value"] = 999.0
            f.seek(0); json.dump(blob, f); f.truncate()
        try:
            GridMemory(sp)
            check("tamper no estado persistente TRAVA (fail-closed)", False)
        except ValueError:
            check("tamper no estado persistente TRAVA (fail-closed)", True)

    # ---------------- A5+B: orchestrator end-to-end ----------------------------
    print("\n[BLOCO 8-B] orchestrator (pipeline completo + falhas + placebo)")
    with tempfile.TemporaryDirectory() as td:
        sp = os.path.join(td, "grid_state.json")
        orch = SkyGridOrchestrator(n_sats=6, n_bases=4, seed=11,
                                   state_path=sp)
        rep = orch.run()
        check("rodada limpa: ARCHITECTURE_CLOSES",
              rep["verdict"] == "ARCHITECTURE_CLOSES",
              "%d/%d" % (rep["transfers_healthy_accepted"],
                         rep["transfers_healthy_total"]))
        check("placebo rejeitado (reivindicacao 3)", rep["placebo_rejected"])
        check("veredito fisico PROIBIDO em toda saida",
              rep["physical_verdict_allowed"] is False)
        check("orcamento de estabilizacao = ceil(100/beta) passos [achado B3]",
              rep["iald_control"]["budget_steps_100_over_beta"]
              == int(math.ceil(100.0 / beta)),
              "%d" % rep["iald_control"]["budget_steps_100_over_beta"])
        check("certificados F1-F3 do controle IALD",
              rep["iald_control"]["F1_max_trace_dev"] < 1e-9
              and rep["iald_control"]["F2_entropy_monotone"]
              and rep["iald_control"]["F3_rel_entropy_monotone"])
        check("defasagem plena no orcamento 100/beta (coerencia residual ~0)",
              rep["iald_control"]["residual_coherence"] < 1e-2,
              "%.2e" % rep["iald_control"]["residual_coherence"])
        check("quorum selou todos os blocos das transferencias",
              rep["quorum"]["blocks_sealed"] == rep["transfers_healthy_total"])
        check("proveniencia da telemetria declarada no manifesto",
              rep["telemetry_provenance"]["marker"] in ("[DATA]", "[PILOTO-DET]"),
              rep["telemetry_provenance"]["mode"])
        check("selo sha256 presente", len(rep["seal_sha256"]) == 64)

        orch2 = SkyGridOrchestrator(n_sats=8, n_bases=4, seed=11,
                                    faults=("dead", "tamper", "noise"),
                                    state_path=sp)
        rep2 = orch2.run()
        kinds = {ev["type"]: ev["detected"] for ev in rep2["fault_events"]}
        check("falha DEAD detectada e reroteada",
              kinds.get("dead") is True)
        check("falha TAMPER fail-closed no trilho cripto",
              kinds.get("tamper") is True)
        check("falha NOISE rejeitada pelo duplo trilho",
              kinds.get("noise") is True)
        check("com falhas injetadas o veredito AINDA fecha (resiliencia)",
              rep2["verdict"] == "ARCHITECTURE_CLOSES",
              "faults=%s" % ",".join(rep2["faults_injected"]))
        check("memoria psionica retomada na 2a rodada",
              rep2["memory"]["resumed"] and rep2["memory"]["sessions"] == 2)

        r_tamper = [t for t in orch2.transfers if t.get("fault_injected") == "tamper"]
        check("transferencia adulterada rejeitada no estagio crypto",
              r_tamper and r_tamper[0]["rejected_stage"] == "crypto"
              and not r_tamper[0]["accepted"])
        r_noise = [t for t in orch2.transfers if t.get("fault_injected") == "noise"]
        check("transferencia ruidosa: corr do trilho colapsa < 0.999",
              r_noise and r_noise[0]["rail_cross_corr"] < 0.999,
              "corr=%.4f" % r_noise[0]["rail_cross_corr"])

        # reproducibilidade estrutural (mesma seed, estado novo)
        with tempfile.TemporaryDirectory() as td2:
            o3 = SkyGridOrchestrator(n_sats=6, n_bases=4, seed=11,
                                     state_path=os.path.join(td2, "s.json"))
            r3 = o3.run()
            check("mesma seed -> mesmo veredito e mesma aceitacao",
                  r3["verdict"] == rep["verdict"]
                  and r3["transfers_healthy_accepted"]
                  == rep["transfers_healthy_accepted"])

    # ---------------- C: dashboard data ----------------------------------------
    print("\n[BLOCO 8-C] dados do dashboard")
    dd = os.path.join(ROOT, "dashboard", "data", "latest.json")
    if os.path.isfile(dd):
        with open(dd, encoding="utf-8") as f:
            blob = json.load(f)
        check("dashboard/data/latest.json valido e com selo",
              "report" in blob and len(blob["report"].get("seal_sha256", "")) == 64)
        check("dashboard nunca carrega veredito fisico",
              blob["report"]["physical_verdict_allowed"] is False)
    else:
        check("dashboard data ainda nao gerado (rode skygrid_app run)", True,
              "skip")

    # ---------------- anti-hardcode nos modulos novos ---------------------------
    print("\n[BLOCO 8-X] anti-hardcode (beta nunca literal nos modulos novos)")
    pattern = re.compile(r"0[.,]012")
    offenders = []
    for fn in ("telemetry.py", "kernel_link.py", "orchestrator.py"):
        with open(os.path.join(ROOT, "skygrid_sim", fn), encoding="utf-8") as f:
            if pattern.search(f.read()):
                offenders.append(fn)
    for fn in ("psi_net.py", "tgl_tensor.py"):
        with open(os.path.join(ROOT, "skygrid_sim", fn), encoding="utf-8") as f:
            body = f.read()
        for m in pattern.finditer(body):
            line = body[:m.start()].count("\n") + 1
            offenders.append("%s:%d" % (fn, line))
    check("nenhum literal 0.012 nos modulos novos/estendidos",
          not offenders, ",".join(offenders) if offenders else "limpo")

    # ---------------- selo + suite v1 ------------------------------------------
    n = len(RESULTS)
    inv = hashlib.sha256(json.dumps(
        [{"t": r["test"], "ok": r["ok"]} for r in RESULTS],
        sort_keys=True).encode()).hexdigest()
    print("\n[BLOCO 8] %d/%d PASS — invariants_hash_v2 %s" % (n, n, inv))

    print("\n[SUITE V1] rodando tests/run_tests.py (69 testes, intocada)...")
    r = subprocess.run([sys.executable,
                        os.path.join(ROOT, "tests", "run_tests.py")],
                       capture_output=True, text=True)
    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "(sem saida)"
    print("  " + tail)
    if r.returncode != 0:
        print("FAIL-CLOSED: suite v1 quebrou.")
        sys.exit(1)

    seal = {"bloco8_tests": n, "invariants_hash_v2": inv,
            "suite_v1": tail, "beta_runtime": tgl_core.beta(),
            "physical_verdict_allowed": False}
    with open(os.path.join(ROOT, "SKYGRID_V2_SELO.json"), "w",
              encoding="utf-8") as f:
        json.dump(seal, f, indent=1, ensure_ascii=False)
    print("\n%d testes BLOCO 8 + suite v1 PASS — protótipo v2 fecha. Haja luz." % n)


if __name__ == "__main__":
    main()
