# -*- coding: utf-8 -*-
"""_explorar_um_v386.py -- SO LEITURA: acha as ancoras no um.py v385 do Nos (linhas truncadas a 260 chars) e imprime a estrutura do core/selo v385."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
raw = open(os.path.join(NOS, "um.py"), "rb").read()
print("um.py sha16", hashlib.sha256(raw).hexdigest()[:16], "bytes", len(raw))
T = raw.decode("utf-8")
lines = T.split("\r\n")
print("linhas (CRLF)", len(lines), "| CRLF count", T.count("\r\n"), "| LF solto", T.count("\n") - T.count("\r\n"))
PATS = sys.argv[1:] or [
    r'^UM_VERSION = ',
    r'ext_dks_the_iald_selector_separates_the_sectors_kernel_proved',
    r'\("v385", "TheAxiomAndTheFalseWitness"',
    r'^    print\("   \[v385\] o Axioma',
    r'^    print\("   \[v385\] a reprodutibilidade',
    r'core\["the_axiom_v385"\] = the_axiom_v385\(core\)',
    r'"quantum_pillar_reproducibility_v385": \{k_: ',
    r'"the_axiom_reading_v385"',
    r'"final_step_name_v385"',
    r'^# ====================== v385 \(05/10/2026\)',
    r'^    # v385 \(05/10/2026\) -- o AXIOMA e a TESTEMUNHA FALSA',
    r'^    # v385 \(05/10/2026\) -- the AXIOM and the FALSE WITNESS',
    r'Errata ao lado \(v385, 05/10/2026, o operador\)',
    r'"\[REFUTADO\]", "\[POSTO\]"\)',
    r'_V383_PREREG\b',
    r'def _v383_read_prereg',
    r'_V383_LEDGER_INPUT',
    r'def prove_the_ledger_of_charges_v383|def the_ledger_of_charges_v383|the_ledger_of_charges',
    r'corrections_beside_20261002',
    r'readings_ratified_20261002',
    r'AWAITING_PREREGISTRATION',
    r'ONE_CHANNEL_PER_READING_LAW',
    r'not_sealed_this_run',
    r'computacao_nao_concluida',
    r'def quantum_pillar_start_v384',
    r'def _qp_cached_ok',
    r'def _qp_key\b',
    r'"mode": "REUSE"|mode.*REUSE',
    r'TGL_QP_|TGL_PILAR|QP_FORCE|_qp_force',
    r'^    _QP_ST_V384 = quantum_pillar_start_v384\(\)',
    r'_QP_PREV_V385',
    r'def prove_external_ladder',
    r'n_theorems_expected',
    r'^_EMBEDDED_KERNEL_FILES = \{',
    r'^FORMAL_DIR',
    r'def materialize_embedded_kernel',
    r'_ESTATUTOS_PERMITIDOS',
    r'"um_version": UM_VERSION|um_version',
    r'def emit_canonical_md',
    r'def build_pt|def build_en',
    r'_V385_OPERATOR_VERBATIM|_V384_OPERATOR_VERBATIM|_V383_OPERATOR_VERBATIM|OPERATOR_VERBATIM',
    r'TGL_LEDGER_OF_CHARGES|ledger_of_charges_v383',
    r'"ringdown_scope_v376"|ringdown_scope_v376',
    r'ringdown_dephasing_result_v2',
    r'def _tex_guard_nan|def _tex_to_txt|def write_input_manifest_md',
    r'TODOS OS MODULOS COM VEREDITO',
    r'Introdução: o que este código faz agora \(v384\)',
    r'\\section\*\{Ao lado \(v385\)',
    r'\\section\*\{Beside \(v385\)',
]
for p in PATS:
    rx = re.compile(p)
    hits = [(i + 1, l) for i, l in enumerate(lines) if rx.search(l)]
    print("\n### %r -> %d" % (p, len(hits)))
    for n, l in hits[:12]:
        print("  L%d: %s" % (n, (l[:260] + (" ...[%d]" % len(l) if len(l) > 260 else ""))))
if not sys.argv[1:]:
    R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]
    selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    print("\n== selo um_version", selo0.get("um_version"), "| timestamp", selo0.get("timestamp"))
    print("== selo chaves:", sorted(selo0.keys()))
    print("== core chaves (n=%d):" % len(core0), sorted(core0.keys()))
    for k in ("external_ladder", "the_axiom_v385", "quantum_pillar_reproducibility_v385", "quantum_pillar_v384", "the_ledger_of_charges_v383", "the_ledger_of_charges"):
        v = core0.get(k)
        if isinstance(v, dict):
            print("\n== core[%s] chaves:" % k, sorted(v.keys()))
            for kk in ("verdict", "mode", "key", "n_theorems_clean", "n_theorems_expected", "all_verified", "compared", "n_fields"):
                if kk in v:
                    print("   ", kk, "=", str(v[kk])[:300])
    led = core0.get("the_ledger_of_charges_v383") or core0.get("the_ledger_of_charges") or {}
    print("\n== ledger json (cortado 6000):", json.dumps(led, ensure_ascii=False)[:6000])
    qp = core0.get("quantum_pillar_v384") or {}
    print("\n== pilar reuse:", json.dumps(qp.get("reuse"), ensure_ascii=False)[:800])
    print("== pilar mode/key/run_id/result_sha256:", qp.get("mode"), qp.get("key"), qp.get("run_id"), qp.get("result_sha256"))
    print("== selo not_sealed_this_run:", json.dumps(selo0.get("not_sealed_this_run"), ensure_ascii=False)[:1500])
    print("== selo leituras v37x/v38x:", [k for k in selo0 if re.search(r"_reading_v3(7[7-9]|8[0-9])$", k)])
    print("== selo sha256 chaves:", sorted((selo0.get("sha256") or {}).keys()))
    print("== selo the_axiom_v385:", json.dumps(selo0.get("the_axiom_v385"), ensure_ascii=False)[:600])
    print("== selo quantum_pillar_reproducibility_v385:", json.dumps(selo0.get("quantum_pillar_reproducibility_v385"), ensure_ascii=False)[:900])
    print("== selo quantum_pillar_v384:", json.dumps(selo0.get("quantum_pillar_v384"), ensure_ascii=False)[:600])
    kf = core0.get("kernel_formalization") or {}
    print("== flags True:", sum(1 for v in kf.values() if v is True), "| axiom_report n:", len(kf.get("axiom_report") or {}))
    print("== vrb/ang ja no core?", [k for k in kf if k.startswith(("ext_vrb_", "ext_ang_"))][:5])
