# -*- coding: utf-8 -*-
"""So leitura: importa o candidato do dry_v382 (como o ensaio), monta o core do ensaio sobre o core v381 com as bandeiras do build do sandbox,
roda prove_the_ledger_of_charges_v382 e imprime cada check (texto + valor). Nao escreve nada fora do stdout."""
import copy, io, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DRY = os.path.join(HERE, "dry_v382")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
sys.path.insert(0, DRY); os.chdir(DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    import um
finally:
    sys.stdout = _o
sys.stdout.reconfigure(encoding="utf-8")
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
AX = json.load(open(os.path.join(HERE, "sandbox_axiom_report__um_v382_candidato.json"), encoding="utf-8"))
c = copy.deepcopy(core0); kf = c["kernel_formalization"]
for k, v in AX.items():
    kf["axiom_report"].setdefault(k, v)
for k, nm in um._LEAN_THEOREM_FLAGS.items():
    if k.startswith(("ext_loc_", "ext_psv_")):
        ax = kf["axiom_report"].get(nm)
        kf[k] = bool(kf.get("lake_build_ok") and ax is not None and not any(a.startswith(("TGL.", "TGLExt.")) for a in ax))
r = um.prove_the_ledger_of_charges_v382(1.0, c)
print("all_verified:", r["all_verified"])
for t, v in r["checks"]:
    if t.startswith("KERNEL "):
        continue
    print(("OK  " if v else "FALHA ") + t[:330])
print("kernel:", sum(1 for t, v in r["checks"] if t.startswith("KERNEL ") and v), "/", sum(1 for t, v in r["checks"] if t.startswith("KERNEL ")))
print("r4_feeds:", r["r4_feeds_the_gate_experimental_step"])
print("R3 numbers:", next(x for x in r["ledger"] if x["id"] == "R3")["numbers_read"])
print("F4 register:", next(x for x in r["ledger"] if x["id"] == "F4")["register"])
print("counts:", r["counts"], "in_rule:", r["counts_in_rule"], "eco:", r["delayed_echo_pairs"])
print("verdict tail:", r["verdict"][-200:])
