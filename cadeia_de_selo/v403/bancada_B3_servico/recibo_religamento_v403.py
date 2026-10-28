"""10-ter da v403: recibo do religamento do servico da Bancada Um, no molde do recibo_religamento_v402.py + completar_recibos.py.
Confere a identidade servida contra o Nos (sha do um.py lido na hora) e contra o recibo do 10-bis (manifesto novo lido do arquivo)."""
import datetime
import glob
import hashlib
import json
import os
import subprocess
import urllib.request

D = os.path.dirname(os.path.abspath(__file__))
AUT = os.environ.get("V403_AUTORIZACAO_OPERADOR", "").strip()
assert AUT, "defina V403_AUTORIZACAO_OPERADOR com a ordem do operador que cobre este ato (data e texto): o script nao presume autorizacao"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
um_sha = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()
rb = sorted(glob.glob(os.path.join(D, "..", "bancada_B3", "RECIBO_SINCRONIZACAO_v403_*.json")))
assert len(rb) == 1, rb
b = json.load(open(rb[0], encoding="utf-8"))
n_esp = int(b["manifesto_anterior"]["deployment_id"].split("-")[0][1:]) + 1   # B<n>: a geracao do manifesto anterior + 1
rb_ant = sorted(glob.glob(os.path.join(D, "..", "..", "v402", "bancada_B3", "RECIBO_SINCRONIZACAO_v402_*.json")))
assert len(rb_ant) == 1, rb_ant
ger_ant = int(json.load(open(rb_ant[0], encoding="utf-8"))["manifesto_novo"]["deployment_id"].split("-")[0][1:])   # a geracao que o B(n) da v402 deixou na Bancada
assert n_esp == ger_ant + 1, ("o manifesto anterior do B(n) da v403 nao e o que o B(n) da v402 deixou na Bancada", n_esp, ger_ant)
assert b["veredito"].startswith("REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO" % n_esp), b["veredito"]
assert "__SALTO_" not in b["veredito"], b["veredito"]   # passo simples: a Bancada pinava a v402 e o Nos passou a v403
man_novo = b["aplicacao"]["pos_conferencia"]["canonical_manifest_sha256"]
c = json.loads(urllib.request.urlopen("http://127.0.0.1:18777/api/contratos", timeout=15).read().decode("utf-8"))
e = json.loads(urllib.request.urlopen("http://127.0.0.1:18777/api/estado", timeout=15).read().decode("utf-8"))
assert c.get("canonical_version") == "v403", c.get("canonical_version")
assert c.get("canonical_manifest_sha256") == man_novo, (c.get("canonical_manifest_sha256"), man_novo)
assert c.get("um_py_sha256") == um_sha, (c.get("um_py_sha256"), um_sha)
pid = subprocess.run(["powershell", "-NoProfile", "-Command",
                      "(Get-NetTCPConnection -State Listen -LocalPort 18777).OwningProcess"], capture_output=True, text=True).stdout.strip()
agora = datetime.datetime.now().astimezone().isoformat()
rec = {"passo": "10-ter", "servico": "um_bancada.py", "porta": 18777,
       "comando": r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py',
       "no_ar_desde": e.get("no_ar_desde"), "pronta": e.get("pronta"),
       "identidade": {k: c.get(k) for k in ("deployment_id", "canonical_version", "um_py_sha256", "seal_sha256", "canonical_manifest_sha256")},
       "versao_servida": c.get("canonical_version"), "manifesto_sha256": c.get("canonical_manifest_sha256"),
       "recibo_do_10_bis": {"path": os.path.abspath(rb[0]), "sha256": hashlib.sha256(open(rb[0], "rb").read()).hexdigest()},
       "pid": int(pid.splitlines()[0]),
       "mcp": "a reconexao dos adaptadores MCP das sessoes (/mcp) e ato do operador em cada sessao aberta",
       "hora_recibo": agora, "hora": agora,
       "autor": "claude-c1 (gerencia)", "autorizacao_do_operador": AUT}
p = os.path.join(D, "RECIBO_RELIGAMENTO_v403.json")
assert not os.path.exists(p), "o recibo ja existe: nao sobrescrevo"
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
os.replace(p + ".tmp", p)
print("ok", p, "pid", rec["pid"], rec["versao_servida"], rec["manifesto_sha256"][:16], "um.py", um_sha[:16])
