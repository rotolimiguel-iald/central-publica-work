import json
T = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\tentativa1_rito_falhou_20261013_160045" + "\\"
d = json.load(open(T+"um_absoluto.json", encoding="utf-8"))
core = d.get("core", d)
kf = core["kernel_formalization"]
keys = ["lake_build_ok","audit_returncode","sentinels_present","sorryAx_absent","trustCompiler_absent","custom_TGL_axioms_absent","source_forbidden_tokens_absent","all_unconditional_targets_verified","all_conditional_implications_verified","build_capture_nonempty","audit_capture_nonempty","axiom_coverage_v392","verdict","source_forbidden_tokens_found"]
for k in keys: print(k, kf.get(k))
print("ext flags false:", sum(1 for k,v in kf.items() if k.startswith("ext_") and v is False), "true:", sum(1 for k,v in kf.items() if k.startswith("ext_") and v is True))
el = core.get("external_ladder", {}); print("ladder", {k:el.get(k) for k in ("n_theorems_clean","n_theorems_expected","verdict","all_verified")})
names = [k for k in core if k.endswith("_v392")]
for k in names:
    v = core[k]
    if isinstance(v, dict): print(k, v.get("all_verified"), str(v.get("verdict"))[:250])
