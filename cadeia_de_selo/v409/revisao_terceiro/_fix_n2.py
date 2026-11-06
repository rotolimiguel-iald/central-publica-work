import re
for p in ("n_hashes_digitados.py", "n2_hashes_docs.py"):
    t = open(p, encoding="utf-8").read()
    t = re.sub(r"for root in \(R,[^\n]*\):", 'for root in (R, W + "cadeia_de_selo/v408/", W + "cadeia_de_selo/v407/", W + "cadeia_de_selo/v406/", W + "cadeia_de_selo/v405/", W + "cunhagens_13out/", W + "pedras_candidatas_05nov/", W + "conjunto_D_20261029/parametrizacao_03nov/", W + "pedras_candidatas_03nov/", W + "fechamento_02nov/", NOS):', t)
    t = t.replace("dry_v40", "dry_v40")
    open(p, "w", encoding="utf-8", newline="\n").write(t)
