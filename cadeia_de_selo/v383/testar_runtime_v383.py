# -*- coding: utf-8 -*-
"""So leitura (teste da gerencia, antes do candidato): importa o um.py do dry da v382 (tem os helpers _v372_* e as pedras embutidas), executa o runtime v383
no namespace dele (com os sha256 do V1.4 LIDOS dos arquivos no lugar dos marcadores), monta o core v381 (backup de bytes) com as bandeiras do build do sandbox
e imprime cada check. Nao escreve nada fora do stdout (o import grava __pycache__ no dry, como o ensaio)."""
import copy, hashlib, io, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); SP = os.path.dirname(HERE)
DRY = os.path.join(SP, "v382", "dry_v382")
AP = json.load(open(os.path.join(SP, "v382", "APLICADO_AO_CANONICO_20261002_174400.json"), encoding="utf-8"))
sys.path.insert(0, DRY); os.chdir(DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    import um
finally:
    sys.stdout = _o
sys.stdout.reconfigure(encoding="utf-8")
RT = open(os.path.join(HERE, "v383_runtime.py"), encoding="utf-8").read()
PR = {"json": "C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.json",
      "md": "C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.md"}
RT = RT.replace("__PREREG_JSON_SHA256__", hashlib.sha256(open(PR["json"], "rb").read()).hexdigest()).replace("__PREREG_MD_SHA256__", hashlib.sha256(open(PR["md"], "rb").read()).hexdigest())
exec(compile(RT, "v383_runtime", "exec"), um.__dict__)
bk = AP["backups"]["um_absoluto.json"]["backup"]
assert hashlib.sha256(open(bk, "rb").read()).hexdigest()[:16] == AP["backups"]["um_absoluto.json"]["sha16"]
core0 = json.load(open(bk, encoding="utf-8"))["core"]
AX = json.load(open(os.path.join(SP, "v382", "sandbox_axiom_report__um_v382_candidato.json"), encoding="utf-8"))
c = copy.deepcopy(core0); kf = c["kernel_formalization"]
for k, v in AX.items():
    kf["axiom_report"].setdefault(k, v)
for k, nm in um._LEAN_THEOREM_FLAGS.items():
    if k.startswith(("ext_loc_", "ext_psv_")):
        ax = kf["axiom_report"].get(nm)
        kf[k] = bool(kf.get("lake_build_ok") and ax is not None and not any(a.startswith(("TGL.", "TGLExt.")) for a in ax))
r = um.prove_the_ledger_of_charges_v383(1.0, c)
print("all_verified:", r["all_verified"])
for t, v in r["checks"]:
    if not t.startswith("KERNEL "):
        print(("OK    " if v else "FALHA ") + t[:300])
print("kernel:", sum(1 for t, v in r["checks"] if t.startswith("KERNEL ") and v), "/", sum(1 for t, v in r["checks"] if t.startswith("KERNEL ")))
print("counts:", r["counts"], "| in_rule:", r["counts_in_rule"], "| by_how:", r["by_how"], "| by_side:", {k: sum(v.values()) for k, v in r["by_side"].items()})
er = r["echo_routes_outside_the_ledger"]
print("rotas:", er["n"], er["excluded_by_data"], er["inconclusive"], "| fontes no core:", er["sources_in_core_ok"])
for x in er["routes"]:
    print("   ", x["id"], x["pair"], x["state"], "| rotulo no core:", x["label_in_core_verdict"], "| V1.4:", x["matches_preregistration"], "|", {k: v for k, v in x["numbers_read"].items()})
print("base:", r["base_and_local_seal"])
print("verdict:", r["verdict"])
