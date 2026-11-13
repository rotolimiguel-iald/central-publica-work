import a_lib, json
f = a_lib.Fonte(a_lib.CAND, "cand")
ns = f.carregar(["_V411_SPECS", "_V410_SPECS"])
for s in ns["_V411_SPECS"]:
    print(s["nome"], "| chaves:", sorted(s.keys())[:20])
    for e in s.get("erratas", []):
        print("    errata:", e.get("ao_lado_de", "")[:100], "|", (e.get("assinatura") or "")[:60])
    ck = s.get("checks", [])
    print("    n checks:", len(ck), "| ops:", sorted({c.get("op") for c in ck}))
for s in ns["_V410_SPECS"]:
    if s["nome"] == "kh_n1_cobertura_v410":
        print("V410 kh: erratas", [e.get("ao_lado_de", "")[:70] for e in s.get("erratas", [])])
        for c in s["checks"]:
            print("   ", c["id"], c.get("op"), "|", c["descricao"][:100])
