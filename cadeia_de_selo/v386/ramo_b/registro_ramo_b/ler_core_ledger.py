import json, hashlib, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
p = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
d = json.loads(open(p,"rb").read().decode("utf-8"))
core = d.get("core", d)
L = core["the_ledger_of_charges_v383"]
print("KEYS ledger:", list(L.keys()) if isinstance(L, dict) else type(L))
s = json.dumps(L, ensure_ascii=False, indent=1)
import re
# print R2 and R6 and anything with ringdown/ramo B
for m in re.finditer(r'"(R[1-6])":\s*"([^"]*)"', s):
    print(m.group(1), "=>", m.group(2)[:600])
for line in s.splitlines():
    if re.search(r"ringdown|ramo B|tau|GM/c", line, re.I): print("  L:", line.strip()[:400])
B = core["bancada_fases_5_6_7_v380"]
sb = json.dumps(B, ensure_ascii=False, indent=1)
print("\nKEYS bancada:", list(B.keys()) if isinstance(B, dict) else type(B))
for line in sb.splitlines():
    if re.search(r"ringdown|tau_star|GM|delay_law|lei|DEC|KMS|MAY", line): print("  B:", line.strip()[:300])
