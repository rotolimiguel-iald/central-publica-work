# -*- coding: utf-8 -*-
# Exame final v393 (c1, modelo forte): re-execucao isolada dos pontos de chamada do candidato. Escreve so' em v393_exame.
import sys, os, io, json, copy, hashlib, re, time
H = os.path.dirname(os.path.abspath(__file__)); IMP = os.path.join(H, "imp")
V = os.path.join(os.path.dirname(H), "v393"); KD = os.path.join(V, "kernel")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
sys.path.insert(0, IMP); os.chdir(IMP)
_o = sys.stdout; sys.stdout = io.StringIO(); t = time.time()
try:
    import um
finally:
    sys.stdout = _o
sys.stdout.reconfigure(encoding="utf-8")
R = {"import_s": round(time.time() - t, 1), "UM_VERSION": um.UM_VERSION, "FORMAL_DIR": um.FORMAL_DIR}
for rel, content in um._EMBEDDED_KERNEL_FILES.items():
    p = os.path.join(IMP, "tgl_kernel", *rel.split("/")); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="").write(content)
LB = open(os.path.join(KD, "lake_build.log"), encoding="utf-8", errors="replace").read()
AUD = open(os.path.join(KD, "audit.log"), encoding="utf-8", errors="replace").read()
calls = []
def fake(cmd, cwd, tmo):
    calls.append(" ".join(cmd[1:]))
    o = {"cmd": " ".join(cmd), "returncode": 0, "stderr": "", "capture_exists": True, "capture_read_error": False, "elapsed_seconds": 0.0, "timeout": False}
    if cmd[1:] == ["--version"]: o["stdout"] = "Lake version 5.0.0-src+68218e8 (Lean version 4.31.0)"
    elif cmd[1:3] == ["env", "lean"] and "--version" in cmd: o["stdout"] = "Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)"
    elif cmd[1:] == ["build"]: o["stdout"] = LB
    else: o["stdout"] = AUD
    o["capture_nonempty"] = bool(o["stdout"]); o["capture_sha256"] = hashlib.sha256(o["stdout"].encode("utf-8")).hexdigest()
    return o
sv = (um.run_process_checked, um._find_lake); um.run_process_checked = fake; um._find_lake = lambda: "lake"
try:
    kf = um.verify_tgl_kernel_formalization()
finally:
    um.run_process_checked, um._find_lake = sv
ext = {k: v for k, v in kf.items() if k.startswith("ext_") and isinstance(v, bool)}
FJ = json.load(open(os.path.join(KD, "FLAGS_v393.json"), encoding="utf-8"))
novas = [f[0] for f in FJ["flags"]]
lean_flags_false = [k for k in getattr(um, "_LEAN_THEOREM_FLAGS", []) if kf.get(k) is not True]
R["verify"] = {"verdict": kf.get("verdict"), "all_verified": kf.get("all_verified"), "cobertura": kf.get("axiom_coverage_v392"), "axiom_report_n": len(kf.get("axiom_report") or {}),
               "ext_true": sum(ext.values()), "ext_false": [k for k, v in ext.items() if not v][:20], "n_ext": len(ext), "novas_144_true": sum(1 for f in novas if kf.get(f) is True), "n_novas": len(novas),
               "lean_flags_false": lean_flags_false[:20], "calls": calls, "lean_version": kf.get("lean_version"), "sorryAx_absent": kf.get("sorryAx_absent"),
               "source_forbidden_tokens_absent": kf.get("source_forbidden_tokens_absent"), "formal_release_ready": kf.get("formal_release_ready")}
el = um.prove_external_ladder(1.0, kf)
R["ladder"] = {k: el.get(k) for k in ("n_theorems_clean", "n_theorems_expected", "verdict", "all_verified")}
C0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))
core = copy.deepcopy(C0["core"]); core["kernel_formalization"] = kf; core["external_ladder"] = el
gate_keys = [k for k in core if re.search(r"gate|qg_closure|closure_verdict|formal_closure", k, re.I)]
J = lambda x: json.dumps(x, sort_keys=True, default=str)
snap = {k: J(core[k]) for k in core}
out = {}
def run(nome, fn):
    try:
        r = fn(); out[nome] = {"all_verified": (r or {}).get("all_verified") if isinstance(r, dict) else r, "verdict": str((r or {}).get("verdict"))[:220] if isinstance(r, dict) else None}
        if isinstance(r, dict) and r.get("checks"):
            out[nome]["falhas"] = [str(c)[:300] for c in r["checks"] if (isinstance(c, (list, tuple)) and len(c) > 1 and not c[1]) or (isinstance(c, dict) and c.get("ok") is False)][:10]
        return r
    except Exception as e:
        import traceback; out[nome] = {"EXCECAO": repr(e)[:300], "tb": traceback.format_exc()[-800:]}
core["the_iald_index"] = run("the_iald_index", lambda: um.prove_the_iald_index(core))
core["three_stress_tests_v387"] = run("three_stress_tests_v387", lambda: um.three_stress_tests_v387(core))
core["estatuto_da_prova_v391"] = run("estatuto_da_prova_v391", lambda: um.estatuto_da_prova_v391(core))
core["pedras_v392"] = run("pedras_v392", lambda: um.pedras_v392(core))
core["varredura_e_sorry_v392"] = run("varredura_e_sorry_v392", lambda: um.varredura_e_sorry_v392(core))
run("_v392_rodar_registros", lambda: {"all_verified": None, "verdict": str(um._v392_rodar_registros(core))})
antes_regra = {k: J(core[k]) for k in core}
run("regra_v393", lambda: (um.regra_v393(core), {"all_verified": None, "verdict": "chamada"})[1])
run("_v393_rodar_specs", lambda: {"all_verified": None, "verdict": str(um._v393_rodar_specs(core))})
for k in ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393", "kh_n1_cobertura_v392"):
    v = core.get(k) or {}
    out["core." + k] = {"all_verified": v.get("all_verified"), "verdict": str(v.get("verdict"))[:240],
                        "falhas": [str(c)[:300] for c in (v.get("checks") or []) if (isinstance(c, (list, tuple)) and len(c) > 1 and not c[1]) or (isinstance(c, dict) and c.get("ok") is False)][:10]}
# registros v392 por spec: todos selam?
r392 = {k: (core.get(k) or {}).get("all_verified") for k in core if k.endswith("_v392") and isinstance(core.get(k), dict) and "all_verified" in core[k]}
out["v392_registros_nao_verdes"] = [k for k, v in r392.items() if v is not True]
mud = sorted(k for k in antes_regra if J(core.get(k)) != antes_regra[k])
novas_chaves = sorted(set(core) - set(antes_regra))
R["regra_mexeu_em_chaves_existentes"] = mud; R["regra_chaves_novas"] = novas_chaves
R["gate_keys"] = {k: snap.get(k) == J(core.get(k)) for k in gate_keys}
R["pontos"] = out
json.dump(R, open(os.path.join(H, "EXAME_PONTOS_v393.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, indent=1, default=str)[:9000])
