import json, os, re, difflib, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
D = r"C:\t\k411c\dry_v411"
rd = lambda p: open(p, "rb").read().decode("utf-8").replace("\r\n", "\n")
des = rd(os.path.join(V, "DESENHO_v411.md"))
E = {"pt": re.search(r"^- \*\*E44\*\* (.+)$", des, re.M).group(1).strip(), "en": re.search(r"^- \*\*E44 \(EN\)\*\* (.+)$", des, re.M).group(1).strip()}
for lang in ("pt", "en"):
    tx = rd(os.path.join(D, "dry_v411_%s.txt" % lang))
    paras = re.findall(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", tx)
    p = [x for x in paras if x.startswith("E44 ")][0]
    a = re.sub(r"\s+", " ", p[4:]).strip()
    b = re.sub(r"\s+", " ", E[lang])
    print(lang, "txt == DESENHO (espacos normalizados):", a == b, len(a), len(b))
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for op in sm.get_opcodes():
        if op[0] != "equal":
            print("   ", op[0], repr(a[op[1]:op[2]])[:70], "->", repr(b[op[3]:op[4]])[:70])
core = json.load(open(os.path.join(D, "core_ensaio.json"), encoding="utf-8"))["core"]
cu = core["cunhagens_v411"]
for i, e in enumerate(cu["erratas"]):
    print("cunhagens erratas[%d] keys:" % i, sorted(e.keys()))
e44 = [e for e in cu["erratas"] if "agora_en" in e]
print("cunhagens_v411.erratas com agora_en:", len(e44))
if e44:
    print("   agora == E44 PT:", e44[0]["agora"] == E["pt"], "| agora_en == E44 EN:", e44[0]["agora_en"] == E["en"])
