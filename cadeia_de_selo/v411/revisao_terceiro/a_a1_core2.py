import json, os
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
b = json.load(open(os.path.join(V, "base_v410", "um_absoluto.json"), encoding="utf-8"))["core"]
c = json.load(open(r"C:\t\k411c\falso_nos_v411\um_absoluto.json", encoding="utf-8"))["core"]
def walk(x, y, p, out):
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) | set(y), key=str):
            if k not in x: out.append((p + "/" + str(k), "<ausente>", repr(y[k])[:140]))
            elif k not in y: out.append((p + "/" + str(k), repr(x[k])[:140], "<ausente>"))
            else: walk(x[k], y[k], p + "/" + str(k), out)
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y): out.append((p, "len %d" % len(x), "len %d" % len(y)))
        for i, (u, v) in enumerate(zip(x, y)): walk(u, v, p + "[%d]" % i, out)
    else:
        if x != y: out.append((p, repr(x)[:140], repr(y)[:140]))
for k in ["kernel_formalization", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "estatuto_da_prova_v391", "h0dn_bg1_v410", "kh_n1_cobertura_v410"]:
    out = []; walk(b[k], c[k], k, out)
    print("==", k, len(out))
    for o in out[:14]: print("  ", o[0][:90], "|", o[1][:100], "->", o[2][:100])
