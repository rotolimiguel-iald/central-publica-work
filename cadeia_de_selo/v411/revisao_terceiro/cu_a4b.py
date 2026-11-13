import json, os, math
CL = r"C:\IALD\Central_publica\central-publica-work"
R = json.load(open(os.path.join(CL, r"h0dn_bg1_v411_emenda_11nov\producao\RESULTADO_DA_ABERTURA_V411.json"), encoding="utf-8"))["resultado"]
core = json.load(open(r"C:\t\k411c\dry_v411\core_ensaio.json", encoding="utf-8"))["core"]
v = core["h0dn_bg1_v411"]["values"]
def show(n, x): print(n, json.dumps(x, ensure_ascii=False)[:600])
show("core.primario", v["primario"]); show("pub.estatistica", R["estatistica"]); show("pub.veredito", {k: R["veredito"][k] for k in ("modelo","outcome","ramo")})
show("core.cefeidas_livres", v["cefeidas_livres"]); show("pub.linha_cl", R["linha_ao_lado_cefeidas_livres"])
show("core.portao_1", v["portao_1"]); show("pub.portao_1", R["portao_1"])
show("core.support", [v["support_l2"], v["support_max_abs"]])
show("core.estresse keys", list(v["estresse"].keys()) if isinstance(v["estresse"], dict) else type(v["estresse"]))
show("pub.estresse", R["estresse"] if len(json.dumps(R["estresse"])) < 1500 else list(R["estresse"].keys()) if isinstance(R["estresse"], dict) else type(R["estresse"]))
show("core.estresse", v["estresse"])
show("core.coerencia", v["coerencia"]); show("pub.coerencia", R["coerencia"])
