import sys, re, glob, os, json
sys.stdout.reconfigure(encoding="utf-8")
from cu_corpus import *
L = json.load(open("literais_v410.json", encoding="utf-8")); AC = L["_V410_AESCALA_CONTRACT"]
print("frase_e36_pt:", AC["frase_e36_pt"]); print("frase_e36_en:", AC["frase_e36_en"]); print("clausula_z_pt:", AC["clausula_z_pt"][:300])
CZ = ws(AC["clausula_z_pt"]); CZE = ws(AC["clausula_z_en"])
e36 = [ws(AC["frase_e36_pt"]), ws(AC["frase_e36_en"])]
srcs = {}
for p in sorted(glob.glob("C:/t/h410/harness_saida_v410/textos/*.txt")): srcs["H:" + os.path.basename(p)] = ws(rd(p))
for i, par in enumerate(re.split(r"\n\s*\n", rd("novo_pt.txt"))): srcs["novo_pt#%d" % i] = ws(par)
for i, par in enumerate(re.split(r"\n\s*\n", rd("novo_en.txt"))): srcs["novo_en#%d" % i] = ws(par)
srcs["md"] = ws(rd("novo_md.txt"))
srcs["pt_artigo"] = carregar()["pt"] if False else ""
print()
for k, x in srcs.items():
    tem_frase = any(f[:60] in x for f in e36) or re.search(r"um pixel entre|one pixel among|limiar de um pixel|one-pixel threshold", x)
    mE36 = re.search(r"E36", x)
    if mE36 or tem_frase:
        clz = (CZ in x) or (CZE in x) or ("soma os $2^n$ pixels e é lida de uma vez" in x) or ("soma os 2^n pixels e é lida de uma vez" in x) or ("sums the $2^n$ pixels and is read at once" in x) or ("sums the 2^n pixels and is read at once" in x)
        print("[%s] E36=%s frase_do_limiar=%s clausula=%s" % (k, bool(mE36), bool(tem_frase), clz))
        if not clz and tem_frase:
            m = re.search(r"um pixel entre|one pixel among|limiar de um pixel|one-pixel threshold", x)
            print("     CTX:", ctx(x, m, 160) if m else x[:200])
