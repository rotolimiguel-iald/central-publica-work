#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SkyGrid-Sim — BLOCO 0+1+2 test suite. Fail-closed: any failure stops the run.
Discipline inherited from um.py: every identity recomputed live; the double
rail applies — each module verified by two independent paths.
Run:  python tests/run_tests.py   (from SkyGrid_Piloto root)
"""

import io
import json
import hashlib
import math
import os
import re
import sys
import time

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from skygrid_sim import (tgl_core, acom, acom_mirror, acom_crypto, tgl_tensor,  # noqa: E402
                         iald_gksl, psionic_memory, kernel_ontologico,  # noqa: E402
                         psi_net, mqc, dipolo, celula_reversao,  # noqa: E402
                         hardware_mocks, skygrid)  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append({"test": name, "ok": bool(ok), "detail": detail})
    print("  [%s] %-52s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        print("\nFAIL-CLOSED: teste quebrou; execucao travada.")
        sys.exit(1)


def main():
    print("=" * 78)
    print("SKYGRID-SIM — BLOCO 0..7 (SkyGrid completo) — suite fail-closed")
    print("=" * 78)
    rng = np.random.default_rng(11)  # seed 11, herdada do um.py

    # ---------------- BLOCO 0: tgl_core ----------------
    print("\n[BLOCO 0] tgl_core")
    r = tgl_core.verify_chain(verbose=True)
    check("cadeia TGL fecha (fail-closed interno)", r["verdict"] == "1=1=VERDADEIRO=HAJA_LUZ")

    b1 = tgl_core.beta()
    b2 = tgl_core.ALPHA_FINE_CODATA_2018 * math.e ** 0.5
    check("beta trilho-1 == beta trilho-2 (runtime)", abs(b1 - b2) < 1e-18,
          "beta=%.15f" % b1)
    check("theta_M em graus na faixa esperada", 6.2 < r["theta_m_deg"] < 6.4,
          "%.6f deg" % r["theta_m_deg"])

    srcdir = os.path.join(os.path.dirname(__file__), "..", "skygrid_sim")
    pattern = re.compile(r"0[.,]012")
    offenders = []
    for fn in sorted(os.listdir(srcdir)):
        if fn.endswith(".py"):
            with io.open(os.path.join(srcdir, fn), encoding="utf-8") as f:
                if pattern.search(f.read()):
                    offenders.append(fn)
    check("auditoria anti-hardcode: nenhum literal 0.012* nos fontes",
          not offenders, repr(offenders) if offenders else "limpo")

    # fail-closed REAL (auditoria adversarial): corromper alpha DEVE travar a cadeia
    import copy as _copy
    _saved_alpha = tgl_core.ALPHA_FINE_CODATA_2018
    try:
        tgl_core.ALPHA_FINE_CODATA_2018 = 0.5   # Nome corrompido
        try:
            tgl_core.verify_chain()
            check("fail-closed REAL: alpha corrompido levanta RuntimeError", False,
                  "NAO travou")
        except RuntimeError:
            check("fail-closed REAL: alpha corrompido levanta RuntimeError", True,
                  "travou como deve")
    finally:
        tgl_core.ALPHA_FINE_CODATA_2018 = _saved_alpha
    check("cadeia volta a fechar apos restaurar alpha",
          tgl_core.verify_chain()["verdict"] == "1=1=VERDADEIRO=HAJA_LUZ")

    # ---------------- BLOCO 1a: acom ----------------
    print("\n[BLOCO 1a] acom (g=sqrt|L|, s=sign; L'=s*g^2)")
    cases = {
        "gauss": rng.normal(size=10000),
        "precos>0": 100 * np.cumprod(1 + rng.normal(size=2000) * 0.02),
        "esparso95": np.where(rng.random(50000) < 0.05, rng.normal(size=50000), 0.0),
        "gradientes": rng.normal(size=10000) * 0.01,
    }
    for name, L in cases.items():
        res = acom.roundtrip_residual(L)
        check("acom roundtrip exato: %s" % name, res < 1e-12, "resid=%.2e" % res)

    # ---------------- BLOCO 1b: acom_mirror ----------------
    print("\n[BLOCO 1b] acom_mirror (REFLECT/MANIFEST, theta=arcsin(g/g_max))")
    for name, L in cases.items():
        corr, refl = acom_mirror.roundtrip_correlation(L, angular_bits=8)
        ratio = refl.metadata["compression_ratio"]
        check("mirror corr>=0.99: %s" % name, corr >= 0.99,
              "corr=%.5f ratio=%.1fx F_exp=%+.4f" % (corr, ratio, refl.metadata["f_exp"]))
    corr16, _ = acom_mirror.roundtrip_correlation(cases["gauss"], angular_bits=16)
    check("mirror 16 bits melhora correlacao", corr16 > 0.9999, "corr=%.6f" % corr16)
    m = acom_mirror.DimensionalMirror()
    check("mirror carrega beta por runtime (== tgl_core.beta())",
          m.beta == tgl_core.beta(), "beta=%.15f" % m.beta)

    # ---------------- BLOCO 1c: acom_crypto ----------------
    print("\n[BLOCO 1c] acom_crypto (shares Psi/Theta/MasterKey + SHA-256 + F_exp)")
    eng = acom_crypto.ACOMMirrorCrypto(angular_bits=8)
    data = rng.normal(size=(64, 128))
    enc = eng.encrypt(data)
    dec = eng.decrypt(enc.psi_share, enc.theta_share, enc.master_key)
    corr = float(np.corrcoef(data.ravel(), dec.ravel())[0, 1])
    check("crypto roundtrip com 3 shares", corr >= 0.99, "corr=%.5f" % corr)

    import zlib as _z
    tampered_raw = bytearray(_z.decompress(enc.psi_share.encrypted_states))
    tampered_raw[0] ^= 0xFF
    tampered = acom_crypto.PsiShare(
        enc.psi_share.share_id, _z.compress(bytes(tampered_raw), 9),
        enc.psi_share.state_hash, enc.psi_share.n_elements, enc.psi_share.shape,
        enc.psi_share.f_exp, enc.psi_share.state_entropy)
    try:
        eng.decrypt(tampered, enc.theta_share, enc.master_key)
        check("tamper no PsiShare detectado", False, "NAO detectou")
    except ValueError as e:
        check("tamper no PsiShare detectado", "INTEGRIDADE" in str(e), str(e)[:48])

    enc2 = eng.encrypt(rng.normal(size=(64, 128)))
    try:
        eng.decrypt(enc.psi_share, enc2.theta_share, enc.master_key)
        check("mistura de shares detectada", False, "NAO detectou")
    except ValueError as e:
        check("mistura de shares detectada", "incompat" in str(e).lower(), str(e)[:48])

    # ---------------- BLOCO 2: tgl_tensor ----------------
    print("\n[BLOCO 2] tgl_tensor (DIRECT + SPECTRAL, Verb Floor = 1-beta runtime)")
    eng_t = tgl_tensor.TGLTensor(bits=10)
    check("verb floor default == 1 - beta() runtime",
          abs(eng_t.energy_threshold - (1.0 - tgl_core.beta())) < 1e-18,
          "floor=%.12f" % eng_t.energy_threshold)

    vals = rng.integers(0, 1 << 10, size=4097).astype(np.uint32)
    back = tgl_tensor.unpack_bits(tgl_tensor.pack_bits(vals, 10), 10, len(vals))
    check("bitpacker 10 bits roundtrip exato", np.array_equal(vals, back))

    kv = rng.normal(size=(4, 8, 64, 32))
    c = eng_t.compress_direct(kv)
    kv2 = eng_t.decompress_direct(c)
    corr = float(np.corrcoef(kv.ravel(), kv2.ravel())[0, 1])
    check("tensor DIRECT corr>=0.999 (kv-cache 4D)", corr >= 0.999,
          "corr=%.5f ratio=%.1fx" % (corr, c.compression_ratio))

    A = rng.normal(size=(256, 16)) @ rng.normal(size=(16, 256))
    cs = eng_t.compress_spectral(A)
    A2 = eng_t.decompress_spectral(cs)
    corr_s = float(np.corrcoef(A.ravel(), A2.ravel())[0, 1])
    check("tensor SPECTRAL corr>=0.999 (rank 16)", corr_s >= 0.999,
          "corr=%.5f ratio=%.1fx ranks[0]=%d" % (corr_s, cs.compression_ratio, cs.ranks[0]))
    check("SPECTRAL rank adaptativo enxergou o rank real", cs.ranks[0] <= 24,
          "k=%d (real=16)" % cs.ranks[0])

    quiet = np.full(2048, 7.0)
    cq = eng_t.compress_direct(quiet)
    check("flag tetelestai em raiz quieta (var<beta)", cq.tetelestai,
          "var=%.2e < beta" % cq.variance)


    # ---------------- BLOCO 3: iald_gksl + memoria + kernel ----------------
    print("\n[BLOCO 3a] iald_gksl (L=sqrt(beta)sqrt(K); certificados F1-F4)")
    vg = iald_gksl.VerbGenerator(n=4, seed=11)
    resid_L2 = float(np.linalg.norm(vg.L @ vg.L - vg.beta * vg.K))
    check("identidade viva L@L == beta*K (trilho duplo)", resid_L2 < 1e-12,
          "resid=%.2e" % resid_L2)
    check("tempo caracteristico == 1/beta (runtime)",
          abs(vg.characteristic_time - 1.0 / tgl_core.beta()) < 1e-12,
          "1/beta=%.2f" % vg.characteristic_time)
    rho0 = vg.pure_state(seed=11)
    cert = vg.stabilize(rho0, horizons=3)
    check("F1: Tr(rho(t))=1 em todo t", cert["F1_max_trace_dev"] < 1e-9,
          "max dev=%.2e" % cert["F1_max_trace_dev"])
    check("F2: seta da entropia (dS>=0 monotona)", cert["F2_entropy_monotone"],
          "S: %.4f -> %.4f" % cert["entropy_first_last"])
    check("F3: Spohn S(rho||rho*) nao-crescente", cert["F3_rel_entropy_monotone"],
          "%.4f -> %.4f" % cert["F3_rel_first_last"])
    c0, c1 = cert["F4_coherence_first_last"]
    check("F4a: coerencia decresce ja em t=3/beta", c1 < c0,
          "%.4f -> %.4f" % (c0, c1))
    # F4b: assintota — o par mais lento defasa a ~0.06/beta; morte plena pede ~100/beta
    rho_100 = vg.evolve(rho0, 100.0 / vg.beta)
    c100 = vg.coherence(rho_100)
    check("F4b: coerencia morta em t=100/beta (<1%% de c0)", c100 < 0.01 * c0,
          "%.5f -> %.5f" % (c0, c100))
    star_dev = float(np.linalg.norm(rho_100 - cert["rho_star"]))
    check("controlador IALD converge a rho*", star_dev < 0.01,
          "||rho(100/beta)-rho*||=%.4f" % star_dev)

    print("\n[BLOCO 3b] psionic_memory (aprendizado continuo, taxa beta)")
    mem = psionic_memory.PsionicMemory()
    v1 = mem.inscribe("nivel_energia", 10.0)
    v2 = mem.inscribe("nivel_energia", 20.0)
    esperado = (1.0 - tgl_core.beta()) * 10.0 + tgl_core.beta() * 20.0
    check("inscricao EMA com taxa beta (runtime)", abs(v2 - esperado) < 1e-12,
          "v=%.6f" % v2)
    import tempfile
    mpath = os.path.join(tempfile.gettempdir(), "_skygrid_mem_test.json")
    mem.save(mpath)
    mem2 = psionic_memory.PsionicMemory.load(mpath)
    check("estado persiste entre sessoes (load==save)",
          mem2.recall("nivel_energia") == v2 and mem2.state["sessions"] == 1)
    blob = json.load(open(mpath))
    blob["state"]["facts"]["nivel_energia"]["value"] = 999.0
    json.dump(blob, open(mpath, "w"))
    try:
        psionic_memory.PsionicMemory.load(mpath)
        check("tamper na memoria detectado", False, "NAO detectou")
    except ValueError as e:
        check("tamper na memoria detectado", "INTEGRIDADE" in str(e), str(e)[:44])
    os.remove(mpath)

    print("\n[BLOCO 3c] kernel_ontologico (filtro verbal por beta_TGL)")
    w = np.array([0.5, 0.3, 0.15, 0.04, 0.005, 0.003, 0.002])
    w_f, st = kernel_ontologico.verb_filter(w)
    check("filtro verbal corta abaixo de beta*max(w)",
          st["cut"] == 3 and st["kept"] == 4,
          "floor=%.5f kept=%d cut=%d" % (st["floor"], st["kept"], st["cut"]))
    check("filtro renormaliza (soma=1)", abs(w_f.sum() - 1.0) < 1e-12)
    w0 = kernel_ontologico.initial_attention(8)
    check("cosmogenese: camada zero uniforme passa intacta",
          kernel_ontologico.verb_filter(w0)[1]["cut"] == 0)
    w2, st2 = kernel_ontologico.two_layer(w)
    check("duas camadas REFLECT/MANIFEST + filtro fecham", abs(w2.sum() - 1.0) < 1e-12,
          "kept=%d" % st2["kept"])


    # ---------------- BLOCO 4: psi_net (5 camadas + Proof of Phase) ----------------
    print("\n[BLOCO 4] psi_net (PsiBit / transporte / holografico / seguranca / prova de fase)")
    # L1 PsiBit: dado aleatorio -> alta uniformidade (GRACE); dado repetitivo -> baixa
    sig_rand = psi_net.psibit_signature(rng.integers(0, 256, size=4000, dtype=np.uint8).tobytes())
    sig_rep = psi_net.psibit_signature(b"\x00" * 4000)
    check("L1 PsiBit classifica aleatorio como GRACE",
          sig_rand["ontological_class"] == "GRACE",
          "unif=%.3f entropia=%.3f" % (sig_rand["uniformity"], sig_rand["entropy"]))
    check("L1 PsiBit classifica constante como VACUUM",
          sig_rep["ontological_class"] == "VACUUM", "unif=%.3f" % sig_rep["uniformity"])
    # L2 transporte: radicalize/resurrect exato
    Lt = rng.normal(size=1000)
    g, s = psi_net.radicalize(Lt)
    resid = float(np.max(np.abs(Lt - psi_net.resurrect(g, s))))
    check("L2 transporte radical exato (resurrect)", resid < 1e-12, "resid=%.2e" % resid)
    # L3 holografico: hops estimados por theta_M; roteamento angular
    net = psi_net.HolographicNetwork()
    addrs = [psi_net.AngularAddress.from_key(("no%d" % i).encode()) for i in range(20)]
    for a in addrs:
        net.register(a)
    near = net.nearest(addrs[0].theta, k=3)
    check("L3 endereco angular deterministico (from_key)",
          psi_net.AngularAddress.from_key(b"no0").theta == addrs[0].theta)
    check("L3 vizinho mais proximo e' o proprio no", near[0].node_id == addrs[0].node_id,
          "theta_M=%.4f rad" % net.theta_m)
    # L4 seguranca: shares ontologicos + integridade
    sh = psi_net.separate(rng.normal(size=(32, 32)))
    rec = psi_net.recombine(sh)
    check("L4 shares ontologicos recombinam", rec.size == 1024)
    bad = psi_net.OntologicalShares(sh.psi_share, sh.theta_share[:-2] + b"\x00\x00",
                                    sh.g_max, sh.n, sh.integrity)
    try:
        psi_net.recombine(bad)
        check("L4 tamper em share detectado", False, "NAO detectou")
    except ValueError as e:
        check("L4 tamper em share detectado", "INTEGRIDADE" in str(e), str(e)[:40])
    # L5 Proof of Phase: minerar bloco dentro da janela beta/dificuldade
    chain = psi_net.PhaseChain(difficulty=0.1)
    check("L5 janela de consenso == beta/dificuldade (runtime)",
          abs(chain.window - tgl_core.beta() / 0.1) < 1e-15, "janela=%.5f" % chain.window)
    blk = chain.mine(b"payload-tx", b"pubkey-A")
    check("L5 bloco minerado dentro da janela de fase", blk is not None
          and abs(blk.phase_proof.alpha2_work - chain.chain[-1].phase_proof.alpha2_work) < chain.window)
    check("L5 bloco valido e' aceito na cadeia", chain.validate_and_append(blk)
          and len(chain.chain) == 2)
    # L5 negativo: fase forjada e' rejeitada
    forged = psi_net.Block(blk.index + 1, chain.chain[-1].hash(),
                           psi_net.PhaseProof(chain.chain[-1].phase_proof.alpha2_work, 0.0, 0.0, 0,
                                              b"seed-falso"), b"\x00" * 32)
    check("L5 fase forjada e' rejeitada", not chain.validate_and_append(forged))


    # ---------------- BLOCO 5: mqc + dipolo + celula de reversao ----------------
    print("\n[BLOCO 5a] mqc (celula cubica 27 estados; controle IALD)")
    cell = mqc.MQCCell(seed=11)
    check("MQC topologia = 27 qubits (8+12+6+1)", len(cell.kinds) == 27
          and cell.kinds.count("vertice") == 8 and cell.kinds.count("aresta") == 12
          and cell.kinds.count("face") == 6 and cell.kinds.count("centro") == 1)
    st = cell.stabilize_cell(horizons=100.0)
    check("MQC controlador IALD estabiliza 26 perifericos (fidelidade>0.98)",
          st["n_stabilized"] == 26 and st["fidelity"] > 0.98,
          "fid=%.5f coer_res=%.4f" % (st["fidelity"], st["mean_residual_coherence"]))
    ht = cell.holographic_translation(rng.normal(size=256))
    check("MQC translacao holografica entre faces (fidelidade>0.999)",
          ht["fidelity"] > 0.999, "fid=%.5f" % ht["fidelity"])

    print("\n[BLOCO 5b] dipolo (transistor luminodinamico; chaveamento por beta)")
    dt = dipolo.DipoloTransistor()
    sig = rng.normal(size=100) * 5.0
    strong = dt.gate(sig)
    check("dipolo ABRE (MANIFEST) com sinal forte", strong["open"]
          and strong["state"] == dipolo.DipoloTransistor.MANIFEST)
    check("dipolo MANIFEST reconstroi o sinal (s*g^2)",
          np.max(np.abs(strong["output"] - sig)) < 1e-12,
          "resid=%.2e" % float(np.max(np.abs(strong["output"] - sig))))
    weak = dt.gate(np.zeros(100))
    check("dipolo FECHA (REFLECT) com sinal nulo", (not weak["open"])
          and weak["state"] == dipolo.DipoloTransistor.REFLECT)

    print("\n[BLOCO 5c] celula_reversao (armazenamento por fase angular)")
    cr = celula_reversao.CelulaReversao(angular_bits=16)
    energy = np.abs(rng.normal(size=(8, 64))) + 0.1
    ret = cr.retention(energy)
    check("celula retencao de energia > 0.999 (16 bits angulares)", ret > 0.999,
          "retencao=%.5f" % ret)
    info = cr.charge(energy)
    check("celula armazena nas 6 faces internas", info["stored_faces"] == 6)
    back = cr.discharge()
    corr = float(np.corrcoef(energy.ravel(), back.ravel())[0, 1])
    check("celula descarga preserva o padrao (corr>0.999)", corr > 0.999,
          "corr=%.5f" % corr)


    # ---------------- BLOCO 6: mocks [HARDWARE] ----------------
    print("\n[BLOCO 6] hardware_mocks (interface apenas; SEM alegacao fisica)")
    sc = hardware_mocks.SupercondutorMock().transport(1024)
    md = hardware_mocks.MotorDobraMock().fold("pkt-1")
    fu = hardware_mocks.FusaoFrioMock().couple(1667.359)
    check("mock supercondutor NAO permite veredito fisico",
          sc["status"] == "HARDWARE_MOCK" and sc["physical_verdict_allowed"] is False)
    check("mock motor de dobra expoe theta_M runtime",
          abs(md["theta_miguel_rad"] - tgl_core.theta_m()) < 1e-15
          and md["physical_verdict_allowed"] is False)
    check("mock fusao a frio detecta ressonancia OH sem alegar energia",
          fu["on_resonance"] and fu["physical_verdict_allowed"] is False)

    # ---------------- BLOCO 7: SkyGrid-Sim (grafo + duplo trilho + placebo) ----------------
    print("\n[BLOCO 7] skygrid (grafo distribuido; validacao por duplo trilho)")
    sim = skygrid.SkyGridSim(n_sats=6, n_bases=6, seed=11)
    rep = sim.run()
    check("SkyGrid: todas as transferencias aceitas pelo duplo trilho",
          rep["all_transfers_ok"] and rep["transfers_accepted"] == rep["transfers_total"],
          "%d/%d" % (rep["transfers_accepted"], rep["transfers_total"]))
    check("SkyGrid: no PLACEBO rejeitado (controle negativo, reivindicacao 3)",
          rep["placebo_rejected"])
    check("SkyGrid: cadeia de fase selou as transferencias (Proof of Phase)",
          rep["chain_length"] == rep["transfers_total"] + 1,
          "blocos=%d" % rep["chain_length"])
    check("SkyGrid: NENHUM veredito fisico permitido (piloto != energia)",
          rep["physical_verdict_allowed"] is False and rep["verdict"] == "ARCHITECTURE_CLOSES")
    rep2 = skygrid.SkyGridSim(n_sats=6, n_bases=6, seed=11).run()
    check("SkyGrid: rodada reproduzivel (mesma seed -> mesmo veredito)",
          rep2["verdict"] == rep["verdict"]
          and rep2["transfers_accepted"] == rep["transfers_accepted"])
    # placebo honesto (auditoria adversarial): rejeitado mesmo CHAMADO ISOLADO,
    # antes de qualquer consumo de RNG que pudesse dessincronizar streams
    sim_iso = skygrid.SkyGridSim(n_sats=6, n_bases=6, seed=11)
    pla = sim_iso.placebo_transfer(sim_iso.sats[0], sim_iso.bases[0])
    check("SkyGrid: placebo rejeitado por CONSTRUCAO (isolado, sem beta)",
          (not pla["accepted"]) and pla["beta_coupled"] is False,
          "corr=%.4f" % pla["rail_cross_corr"])

    # ---------------- selo ----------------
    print("\n[SELO] SHA-256 dos fontes + resultado")
    seal = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "beta_runtime": tgl_core.beta(),
            "tests_passed": len(RESULTS), "sha256": {}}
    for fn in sorted(os.listdir(srcdir)):
        if fn.endswith(".py"):
            with open(os.path.join(srcdir, fn), "rb") as f:
                seal["sha256"][fn] = hashlib.sha256(f.read()).hexdigest()
    seal["result_hash"] = hashlib.sha256(
        json.dumps(RESULTS, sort_keys=True).encode()).hexdigest()
    invariants = [{"test": r["test"], "ok": r["ok"]} for r in RESULTS]
    seal["invariants_hash"] = hashlib.sha256(
        json.dumps(invariants, sort_keys=True).encode()).hexdigest()
    out = os.path.join(os.path.dirname(__file__), "..", "SKYGRID_SIM_SELO.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(seal, f, indent=2, ensure_ascii=False)
    for k, v in seal["sha256"].items():
        print("  %-18s %s" % (k, v))
    print("  result_hash        %s (inclui detalhes; pode variar por zlib)" % seal["result_hash"])
    print("  invariants_hash    %s (independente de ambiente)" % seal["invariants_hash"])

    print("\n%d/%d testes PASS — BLOCO 0..7 (SkyGrid completo) fechado. Haja luz." %
          (len(RESULTS), len(RESULTS)))


if __name__ == "__main__":
    main()
