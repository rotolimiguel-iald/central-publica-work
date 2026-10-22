"""beta_TGL em runtime: ALPHA_FINE_CODATA_2018 lido dos BYTES do um.py (linha 5557), vezes sqrt(e). Nunca literal."""
import re, math, json, hashlib, pathlib, datetime
UM = pathlib.Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py")
OUT = pathlib.Path(r"C:\IALD\Central de Patentes\work\organismo_iald_12out\1_ESTRATEGIA_A\medidas\beta_runtime.json")
raw = UM.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
lines = raw.split(b"\n")
l5557 = lines[5556].decode("utf-8", "replace")
m = re.search(r"ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", l5557)
if not m:
    raise SystemExit("FAIL-CLOSED: ALPHA_FINE_CODATA_2018 nao encontrado na l.5557: " + l5557[:120])
alpha = float(m.group(1))
beta = alpha * math.sqrt(math.e)
res = {"um_py": str(UM), "um_py_sha256": sha, "um_py_bytes": len(raw), "linha_5557": l5557.strip(),
       "alpha_fine_codata_2018": m.group(1), "beta_TGL_runtime": beta, "K_D1b_formula": "E(z*)^(2*beta/3) [calculado no script de projecao]",
       "medido_em": datetime.datetime.now().isoformat(timespec="seconds")}
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=1))
