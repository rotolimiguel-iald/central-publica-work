import datetime
import json
import os
import urllib.request

D = os.path.dirname(os.path.abspath(__file__))
c = json.loads(urllib.request.urlopen("http://127.0.0.1:18777/api/contratos", timeout=10).read().decode("utf-8"))
e = json.loads(urllib.request.urlopen("http://127.0.0.1:18777/api/estado", timeout=10).read().decode("utf-8"))
assert c.get("canonical_version") == "v392", c.get("canonical_version")
assert c.get("canonical_manifest_sha256", "").startswith("6733b9a28c725244"), c.get("canonical_manifest_sha256")
assert c.get("um_py_sha256", "").startswith("b590c0aa80055e2a")
rec = {"passo": "10-ter", "servico": "um_bancada.py", "porta": 18777,
       "comando": r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py',
       "no_ar_desde": e.get("no_ar_desde"), "pronta": e.get("pronta"),
       "identidade": {k: c.get(k) for k in ("deployment_id", "canonical_version", "um_py_sha256", "seal_sha256", "canonical_manifest_sha256")},
       "mcp": "a reconexão dos adaptadores MCP das sessões (/mcp) é ato do operador em cada sessão aberta",
       "hora_recibo": datetime.datetime.now().astimezone().isoformat(),
       "autor": "claude-c1 (gerência), por autorização geral do operador de 13/10"}
p = os.path.join(D, "RECIBO_RELIGAMENTO_v392.json")
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
os.replace(p + ".tmp", p)
print("ok", p)
