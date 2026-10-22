# -*- coding: utf-8 -*-
import io, re, hashlib, sys, json
sys.stdout.reconfigure(encoding="utf-8")
OP = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v386\TRES_TESTES_operador_05out.txt"
raw = open(OP, "rb").read()
print("sha256 operador:", hashlib.sha256(raw).hexdigest(), "| bytes:", len(raw))
op = raw.decode("utf-8")
out = {}
for lang in ("pt", "en"):
    tex = io.open(rf"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v387\redacao\render_{lang}_v387.tex", encoding="utf-8").read()
    quotes = re.findall(r"``(.*?)''", tex, flags=re.S)
    res = []
    for q in quotes:
        # unescape minimal LaTeX
        plain = q.replace(r"\_", "_").replace("\&", "&")
        exact = plain in op
        res.append({"quote": plain[:90], "len": len(plain), "exact_substring": exact})
        print(f"[{lang}] exact={exact} len={len(plain)} :: {plain[:80]!r}")
    out[lang] = res
json.dump(out, io.open("verbatim_check.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# Also: what does the operator text say between the quoted segments? (what was cut by "...")
print("\n--- texto completo do operador (para ver o que ficou de fora dos cortes) ---")
print(op)
