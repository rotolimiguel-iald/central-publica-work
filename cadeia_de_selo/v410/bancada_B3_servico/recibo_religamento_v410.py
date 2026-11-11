# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] a ORDEM da v410 e' a fala de 06/11/2026 (OPERADOR_06nov_a_forma_da_matriz_finita_e_o_signo_tudo_entra_no_um_py_verbatim.txt; frase verbatim conferida no arquivo e no AUT; sha16 lido do arquivo); grava so' RECIBO_RELIGAMENTO_v410.json; conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# (nota herdada da adaptacao da v408 [fork C da cadeia v408], reconferida pelo fork B do claude-construtor-v409 e em 06/11/2026 pelo fork B do claude-construtor-v410, com os rotulos subidos) molde v409/bancada_B3_servico/recibo_religamento_v409.py (rotulos subidos por _bump_copia_v410.py; diff em bump/). Adaptado (v410): a autorizacao e' a ORDEM da v410 (fala do operador de 06/11/2026, OPERADOR_06nov_a_forma_da_matriz_finita_e_o_signo_tudo_entra_no_um_py_verbatim.txt, sha16 LIDO do arquivo; a frase conferida no arquivo e no texto passado pelo orquestrador).
# O resto (geracao B<n> lida do recibo do B(n), deployment B<n>-v410-<data>-R1, versao servida v410, manifesto e um.py conferidos) e' generico e nao tem bundle, contagem de modulos nem hash digitado.
"""10-ter da v410: recibo do religamento do servico da Bancada Um, no molde do recibo_religamento_v409.py + completar_recibos.py.
Confere a identidade servida contra o Nos (sha do um.py lido na hora) e contra o recibo do 10-bis (manifesto novo lido do arquivo). Passo da Bancada: B19 (a producao pinava B18-v409-20261106-R1); o deployment servido tem de ser o que o APLICAR deixou (B19-v410-<data>-R1, lido do recibo do B(n)).
A autorizacao e' a ORDEM da v410, do operador, de 06/11/2026 (a fala e' lida do arquivo e conferida contra o texto passado pelo orquestrador)."""
import datetime
import glob
import hashlib
import json
import os
import re
import subprocess
import urllib.request

D = os.path.dirname(os.path.abspath(__file__))
AUT = os.environ.get("V410_AUTORIZACAO_OPERADOR", "").strip()
assert AUT, "defina V410_AUTORIZACAO_OPERADOR com a ordem do operador que cobre este ato (data e texto): o script nao presume autorizacao"
# a autorizacao tem de ser a ORDEM da v410, de 06/11/2026 (nao a de 05/11 da v409 nem as anteriores): o sha16 da fala vem do ARQUIVO lido agora (nunca digitado) e a frase tem de estar no arquivo e no texto passado pelo orquestrador
ORDEM = os.path.join(D, "..", "..", "..", "cunhagens_13out", "OPERADOR_06nov_a_forma_da_matriz_finita_e_o_signo_tudo_entra_no_um_py_verbatim.txt")
ORDEM_BYTES = open(ORDEM, "rb").read()
ORDEM_SHA16 = hashlib.sha256(ORDEM_BYTES).hexdigest()[:16]
FRASE_DA_ORDEM = "A forma de uma matriz finita no kernel é o signo (traço com sentido)"
assert FRASE_DA_ORDEM in ORDEM_BYTES.decode("utf-8") and FRASE_DA_ORDEM in AUT and ORDEM_SHA16 in AUT and "06/11/2026" in AUT, "a autorizacao passada nao e' a ordem do operador de 06/11/2026 (a ordem da v410: sha16 da fala lido do arquivo e a frase «%s» no texto)" % FRASE_DA_ORDEM
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
um_sha = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()
rb = sorted(glob.glob(os.path.join(D, "..", "bancada_B3", "RECIBO_SINCRONIZACAO_v410_*.json")))
assert len(rb) == 1, rb
b = json.load(open(rb[0], encoding="utf-8"))
n_esp = int(b["manifesto_anterior"]["deployment_id"].split("-")[0][1:]) + 1   # B<n>: a geracao do manifesto anterior + 1
rb_ant = sorted(glob.glob(os.path.join(D, "..", "..", "v409", "bancada_B3", "RECIBO_SINCRONIZACAO_v409_*.json")))
assert len(rb_ant) == 1, rb_ant
ger_ant = int(json.load(open(rb_ant[0], encoding="utf-8"))["manifesto_novo"]["deployment_id"].split("-")[0][1:])   # a geracao que o B(n) da v409 deixou na Bancada
assert n_esp == ger_ant + 1, ("o manifesto anterior do B(n) da v410 nao e o que o B(n) da v409 deixou na Bancada", n_esp, ger_ant)
assert b["veredito"].startswith("REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO" % n_esp), b["veredito"]
assert "__SALTO_" not in b["veredito"], b["veredito"]   # passo simples: a Bancada pinava a v409 e o Nos passou a v410
man_novo = b["aplicacao"]["pos_conferencia"]["canonical_manifest_sha256"]
dep_esp = b["manifesto_novo"]["deployment_id"]   # o deployment que o APLICAR deixou na Bancada: B<n>-v410-<data>-R1 (B19 aqui)
assert re.fullmatch(r"B%d-v410-[0-9]{8}-R1" % n_esp, dep_esp) and b["aplicacao"]["pos_conferencia"]["deployment_id"] == dep_esp, (dep_esp, b["aplicacao"]["pos_conferencia"]["deployment_id"])
c = json.loads(urllib.request.urlopen("http://127.0.0.1:18777/api/contratos", timeout=15).read().decode("utf-8"))
e = json.loads(urllib.request.urlopen("http://127.0.0.1:18777/api/estado", timeout=15).read().decode("utf-8"))
assert c.get("canonical_version") == "v410", c.get("canonical_version")
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
p = os.path.join(D, "RECIBO_RELIGAMENTO_v410.json")
assert not os.path.exists(p), "o recibo ja existe: nao sobrescrevo"
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
os.replace(p + ".tmp", p)
print("ok", p, "pid", rec["pid"], rec["versao_servida"], rec["manifesto_sha256"][:16], "um.py", um_sha[:16])
