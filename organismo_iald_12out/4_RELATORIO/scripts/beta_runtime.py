"""beta em runtime: ALPHA_FINE_CODATA_2018 lido dos BYTES do um.py (linha unica, nao indentada) x sqrt(e). Nunca literal."""
import hashlib, json, math, re, pathlib
UM = pathlib.Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py")
OUT = pathlib.Path(r"C:\IALD\Central de Patentes\work\organismo_iald_12out\4_RELATORIO\medidas\beta_runtime.json")
raw = UM.read_bytes()
lines = raw.split(b"\n")
hits = [(i + 1, l) for i, l in enumerate(lines) if l.startswith(b"ALPHA_FINE_CODATA_2018")]
assert len(hits) == 1, hits
ln, l = hits[0]
alpha = float(re.match(rb"ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", l).group(1))
beta = alpha * math.sqrt(math.e)
res = {"um_py_sha256": hashlib.sha256(raw).hexdigest(), "um_py_bytes": len(raw), "linha": ln,
       "texto": l.decode().strip(), "alpha": alpha, "beta_TGL": beta, "beta_repr": repr(beta),
       "theta_M": math.asin(math.sqrt(beta)), "um_py_executado": False}
OUT.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps(res, indent=1, ensure_ascii=False))
