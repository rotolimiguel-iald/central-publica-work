# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork B)] a ORDEM da v411 e' a fala do operador de 12/11/2026 (OPERADOR_12nov_otimo_vamos_rodar_tudo_pode_abrir_chegou_a_hora_da_v411_verbatim.txt; D169): o arquivo e' so' a fala, que e' LIDA inteira do arquivo (nunca digitada), o sha16 calculado na hora, a data 12/11/2026 no AUT; o resto do corpo (o passo B20, o recibo do religamento da v410 como ultimo conhecido, as chaves do recibo REAL da v410) ja' era o certo: nada de bundle nem de hash digitado
# (historico: o molde e' v410/bancada_B3_servico/recibo_religamento_v410.py, adaptado na v410 a ordem da v410; a copia subiu por rotulo em _bump_copia_v411.py, diff em bump/; o corpo vem da adaptacao da v408 [fork C], conferido de versao a versao; na v411 so' a ORDEM muda, e as datas das ordens anteriores nao ficam no script porque o conferidor estatico as recusa)
# O resto (geracao B<n> lida do recibo do B(n), deployment B<n>-v411-<data>-R1, versao servida v411, manifesto e um.py conferidos) e' generico e nao tem bundle, contagem de modulos nem hash digitado.
"""10-ter da v411: recibo do religamento do servico da Bancada Um, no molde do recibo_religamento_v410.py + completar_recibos.py.
Confere a identidade servida contra o Nos (sha do um.py lido na hora) e contra o recibo do 10-bis (manifesto novo lido do arquivo). Passo da Bancada: B20 (a producao pinava B19-v410-20261111-R1); o deployment servido tem de ser o que o APLICAR deixou (B20-v411-<data>-R1, lido do recibo do B(n)).
A autorizacao e' a ORDEM da v411, do operador, de 12/11/2026 (a ordem de abrir e a ordem da v411, D169; a fala inteira e' lida do arquivo e conferida contra o texto passado pelo orquestrador)."""
import datetime
import glob
import hashlib
import json
import os
import re
import subprocess
import urllib.request

D = os.path.dirname(os.path.abspath(__file__))
AUT = os.environ.get("V411_AUTORIZACAO_OPERADOR", "").strip()
assert AUT, "defina V411_AUTORIZACAO_OPERADOR com a ordem do operador que cobre este ato (data e texto): o script nao presume autorizacao"
# a autorizacao tem de ser a ORDEM da v411, de 12/11/2026 (a ordem de abrir e a ordem da v411, D169; nao a da v410 nem as anteriores): o sha16 da fala vem do ARQUIVO lido agora (nunca digitado), a fala INTEIRA e' lida do arquivo
# (o arquivo e' so' a fala do operador) e tem de estar no texto passado pelo orquestrador, com a data
ORDEM = os.path.join(D, "..", "..", "..", "cunhagens_13out", "OPERADOR_12nov_otimo_vamos_rodar_tudo_pode_abrir_chegou_a_hora_da_v411_verbatim.txt")
ORDEM_BYTES = open(ORDEM, "rb").read()
ORDEM_SHA16 = hashlib.sha256(ORDEM_BYTES).hexdigest()[:16]
FRASE_DA_ORDEM = ORDEM_BYTES.decode("utf-8").strip()   # a fala inteira, LIDA do arquivo (nunca digitada aqui)
assert FRASE_DA_ORDEM in ORDEM_BYTES.decode("utf-8") and len(FRASE_DA_ORDEM) >= 20 and FRASE_DA_ORDEM in AUT and ORDEM_SHA16 in AUT and "12/11/2026" in AUT, "a autorizacao passada nao e' a ordem do operador de 12/11/2026 (a ordem da v411: o sha16 da fala lido do arquivo e a fala inteira no texto, com a data)"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
um_sha = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()
rb = sorted(glob.glob(os.path.join(D, "..", "bancada_B3", "RECIBO_SINCRONIZACAO_v411_*.json")))
assert len(rb) == 1, rb
b = json.load(open(rb[0], encoding="utf-8"))
n_esp = int(b["manifesto_anterior"]["deployment_id"].split("-")[0][1:]) + 1   # B<n>: a geracao do manifesto anterior + 1
rb_ant = sorted(glob.glob(os.path.join(D, "..", "..", "v410", "bancada_B3", "RECIBO_SINCRONIZACAO_v410_*.json")))
assert len(rb_ant) == 1, rb_ant
ger_ant = int(json.load(open(rb_ant[0], encoding="utf-8"))["manifesto_novo"]["deployment_id"].split("-")[0][1:])   # a geracao que o B(n) da v410 deixou na Bancada
assert n_esp == ger_ant + 1, ("o manifesto anterior do B(n) da v411 nao e o que o B(n) da v410 deixou na Bancada", n_esp, ger_ant)
assert b["veredito"].startswith("REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO" % n_esp), b["veredito"]
assert "__SALTO_" not in b["veredito"], b["veredito"]   # passo simples: a Bancada pinava a v410 e o Nos passou a v411
man_novo = b["aplicacao"]["pos_conferencia"]["canonical_manifest_sha256"]
dep_esp = b["manifesto_novo"]["deployment_id"]   # o deployment que o APLICAR deixou na Bancada: B<n>-v411-<data>-R1 (B20 aqui)
assert re.fullmatch(r"B%d-v411-[0-9]{8}-R1" % n_esp, dep_esp) and b["aplicacao"]["pos_conferencia"]["deployment_id"] == dep_esp, (dep_esp, b["aplicacao"]["pos_conferencia"]["deployment_id"])
c = json.loads(urllib.request.urlopen("http://127.0.0.1:18777/api/contratos", timeout=15).read().decode("utf-8"))
e = json.loads(urllib.request.urlopen("http://127.0.0.1:18777/api/estado", timeout=15).read().decode("utf-8"))
assert c.get("canonical_version") == "v411", c.get("canonical_version")
assert c.get("deployment_id") == dep_esp, (c.get("deployment_id"), dep_esp)
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
p = os.path.join(D, "RECIBO_RELIGAMENTO_v411.json")
assert not os.path.exists(p), "o recibo ja existe: nao sobrescrevo"
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
os.replace(p + ".tmp", p)
print("ok", p, "pid", rec["pid"], rec["versao_servida"], rec["manifesto_sha256"][:16], "um.py", um_sha[:16])
