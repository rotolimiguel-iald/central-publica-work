import json, hashlib, sys
p = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
b = open(p,"rb").read()
print("core sha256", hashlib.sha256(b).hexdigest(), "bytes", len(b))
d = json.loads(b.decode("utf-8"))
core = d.get("core", d)
keys = [k for k in core.keys() if any(s in k.lower() for s in ["ringdown","branch_b","ramo_b","tau_star","dephasing","gw250114","ledger_of_charges","bancada_fases_5_6_7","echo_anchored","gw_echo"])]
print("N keys", len(keys))
for k in keys: print(k)
print("um_version", core.get("um_version") or d.get("um_version"))
