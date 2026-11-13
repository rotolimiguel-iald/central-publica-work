import json, os
CL = r"C:\IALD\Central_publica\central-publica-work"
R = json.load(open(os.path.join(CL, r"h0dn_bg1_v411_emenda_11nov\producao\RESULTADO_DA_ABERTURA_V411.json"), encoding="utf-8"))["resultado"]
core = json.load(open(r"C:\t\k411c\dry_v411\core_ensaio.json", encoding="utf-8"))["core"]["h0dn_bg1_v411"]
v = core["values"]; st = R["estatistica"]
res = {}
res["primario_t"] = v["primario"]["t"] == st["t"][0]
res["primario_z_null"] = v["primario"]["z_null"] == st["z_null"][0]
res["primario_z_tgl"] = v["primario"]["z_tgl"] == st["z_tgl"][0]
res["primario_D"] = v["primario"]["D"] == st["D_s0"][0]
res["primario_ramo"] = v["primario"]["ramo"] == R["veredito"]["ramo"] and v["primario"]["outcome"] == R["veredito"]["outcome"]
res["primario_cabeca"] = v["primario"]["cabeca_do_teste"] == R["veredito"]["cabeca"] == core["cabeca_do_teste"]
c = v["cefeidas_livres"]
res["cl_t_z_D"] = (c["t"], c["z_null"], c["z_tgl"], c["D"]) == (st["t"][1], st["z_null"][1], st["z_tgl"][1], st["D_s0"][1])
res["cl_ramo_cabeca"] = c["ramo"] == R["linha_ao_lado_cefeidas_livres"]["ramo"] and c["cabeca"] == R["linha_ao_lado_cefeidas_livres"]["cabeca"] and c["outcome"] == R["linha_ao_lado_cefeidas_livres"]["outcome"]
res["support"] = (v["support_l2"], v["support_max_abs"]) == (st["support_l2"], st["support_max_abs"])
for k in ("portao_1", "estresse", "coerencia"):
    res[k] = json.dumps(v[k], sort_keys=True) == json.dumps(R[k], sort_keys=True)
res["linha_cl_no_core"] = core["linha_ao_lado_cefeidas_livres"]["z_null"] == st["z_null"][1]
res["checks16"] = [c["id"] for c in core["mechanics"]["checks"] if c["ok"]] == ["c%d" % i for i in range(1, 17)]
res["passed"] = core["mechanics"]["passed"]
res["all_verified"] = core["all_verified"]
res["opened_once"] = core["opened_once"]
res["beta_ok"] = core["beta_ok"]; res["beta_core_rel_diff"] = core["beta_core_rel_diff"]
print(json.dumps(res, indent=1))
# decomposicao
print("decomp", json.dumps(v["decomposicao_conferencias"], sort_keys=True)[:200]); print("pub decomp", json.dumps(R["decomposicao"], sort_keys=True)[:200])
json.dump(res, open(r"C:\t\k411c\revisao_CU\a4_core_vs_publicado.json", "w"), indent=1)
