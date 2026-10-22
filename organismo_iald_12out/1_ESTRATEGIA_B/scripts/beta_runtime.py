"""beta_TGL em runtime: ALPHA_FINE_CODATA_2018 lido dos BYTES do um.py (l.5557), vezes sqrt(e). Nunca literal."""
import hashlib, json, math, re, sys, datetime
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
raw = open(UM, "rb").read()
h = hashlib.sha256(raw).hexdigest()
lines = raw.split(b"\n")
l5557 = lines[5556].decode("utf-8", "replace").rstrip("\r")
m = re.match(r"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)\s*$", l5557)
if not m:
    print(json.dumps({"ok": False, "erro": "linha 5557 nao e a definicao de ALPHA_FINE_CODATA_2018", "linha": l5557})); sys.exit(2)
alpha = float(m.group(1)); beta = alpha * math.sqrt(math.e)
ver = next((ln.decode("utf-8","replace").rstrip("\r") for ln in lines if ln.startswith(b"UM_VERSION")), "")
out = {"ok": True, "um_py": UM, "um_py_sha256": h, "um_py_bytes": len(raw), "um_version_line": ver[:60],
       "linha_5557": l5557, "ALPHA_FINE_CODATA_2018": alpha, "sqrt_e": math.sqrt(math.e), "beta_TGL_runtime": beta,
       "beta_repr": repr(beta), "quando": datetime.datetime.now().isoformat(timespec="seconds")}
print(json.dumps(out, ensure_ascii=False, indent=1))
