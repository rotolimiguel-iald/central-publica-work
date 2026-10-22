import re, math, json, hashlib, sys
P = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
b = open(P, "rb").read()
lines = b.split(b"\n")
l = lines[5556].decode("utf-8", "replace")
m = re.search(r"ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", l)
alpha = float(m.group(1))
beta = alpha * math.sqrt(math.e)
out = {"um_py_sha256": hashlib.sha256(b).hexdigest(), "um_py_bytes": len(b), "line": 5557, "line_text": l.strip(),
       "ALPHA_FINE_CODATA_2018": alpha, "beta_runtime": beta, "beta_repr": repr(beta)}
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
