# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork C)] molde v407/bancada_B3_servico/recibo_parada_v407.py (rotulos subidos por _bump_copia_v408.py; diff em bump/). Adaptado: a autorizacao e' a ORDEM da v408 (fala do operador de 04/11/2026, OPERADOR_04nov_ordem_v408_..., sha16 LIDO do arquivo; a frase conferida no arquivo e no texto passado pelo orquestrador);
# o ultimo religamento conhecido segue sendo o do B(n) da v407 (RECIBO_RELIGAMENTO_v407.json: PID, no_ar_desde), e o recibo diz se o PID lido da porta e' o mesmo; as chaves do recibo sao as do recibo REAL da v407; nada de bundle nem de hash digitado.
"""10-bis-a da v408: recibo da parada do servico da Bancada Um (porta 18777), no molde do recibo_parada_v407.py. Passo da Bancada: B17 (a producao pina B16-v407-20261104-R1). A autorizacao e' a ORDEM da v408, do operador, de 04/11/2026 (a fala e' lida do arquivo e conferida contra o texto passado pelo orquestrador).
O ultimo religamento conhecido e' o do B(n) da v407 (RECIBO_RELIGAMENTO_v407.json, em v407/bancada_B3_servico): o PID registrado aqui e' o LIDO DA PORTA antes da parada; o recibo diz se e' o mesmo do religamento da v407 ou se o servico foi religado de novo depois."""
import datetime
import hashlib
import json
import os
import socket
import subprocess

D = os.path.dirname(os.path.abspath(__file__))
AUT = os.environ.get("V408_AUTORIZACAO_OPERADOR", "").strip()
assert AUT, "defina V408_AUTORIZACAO_OPERADOR com a ordem do operador que cobre este ato (data e texto): o script nao presume autorizacao"
# a autorizacao tem de ser a ORDEM da v408, de 04/11/2026 (nao a de 03/11 da v407 nem a de 02/11 da v406): o sha16 da fala vem do ARQUIVO lido agora (nunca digitado) e a frase tem de estar no arquivo e no texto passado pelo orquestrador
ORDEM = os.path.join(D, "..", "..", "..", "cunhagens_13out", "OPERADOR_04nov_ordem_v408_liste_as_pedras_produza_rode_handoff_custodia_completa_verbatim.txt")
ORDEM_BYTES = open(ORDEM, "rb").read()
ORDEM_SHA16 = hashlib.sha256(ORDEM_BYTES).hexdigest()[:16]
FRASE_DA_ORDEM = "liste as pedras que eu preciso nominar e em seguida produza a v408, rode e quando estiver completa, dê a ordem de handoff para a sessão irmã realizar a custódia completa e atualizar tudo"
assert FRASE_DA_ORDEM in ORDEM_BYTES.decode("utf-8") and FRASE_DA_ORDEM in AUT and ORDEM_SHA16 in AUT and "04/11/2026" in AUT, "a autorizacao passada nao e' a ordem do operador de 04/11/2026 (a ordem da v408: sha16 da fala lido do arquivo e a frase «%s» no texto)" % FRASE_DA_ORDEM
s = socket.socket()
s.settimeout(1)
aberta = s.connect_ex(("127.0.0.1", 18777)) == 0
s.close()
assert not aberta, "a porta 18777 esta aberta: parar o servico pelo PID antes deste recibo"
ps = subprocess.run(["powershell", "-NoProfile", "-Command",
                     "(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*um_bancada.py*' -and $_.ProcessId -ne $PID } | "
                     "Measure-Object).Count"], capture_output=True, text=True)
n_proc = int(ps.stdout.strip().splitlines()[-1])
assert n_proc == 0, "ha %d processo(s) um_bancada.py vivos: parar pelo PID antes deste recibo" % n_proc
rel407 = json.load(open(os.path.join(D, "..", "..", "v407", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v407.json"), encoding="utf-8"))   # o ultimo religamento conhecido: o do B(n) da v407 (o servico que a v407 deixou no ar)
pid_v407 = rel407["pid"]
assert str(pid_v407).isdigit() and rel407.get("no_ar_desde") and rel407.get("hora_recibo"), rel407
# emenda da gerencia c1 (28/10/2026, antes do uso): o numero corrige a frase -- o PID registrado e o LIDO DA PORTA antes da parada (V408_PID_PARADO), nao o de nenhum recibo anterior,
# porque o servico pode ter sido religado de novo depois do ultimo recibo (o processo da porta foi criado em outra hora); o PID do recibo anterior (o da v407) fica ao lado, como referencia.
PIDP = os.environ.get("V408_PID_PARADO", "").strip()
assert PIDP.isdigit(), "defina V408_PID_PARADO com o PID lido da porta 18777 antes da parada (linha de comando conferida): o script nao presume o PID"
CRIADO = os.environ.get("V408_PID_PARADO_CRIADO", "").strip()
assert CRIADO, "defina V408_PID_PARADO_CRIADO com a data/hora de criacao do processo parado (lida de Win32_Process antes da parada)"
vivo = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-Process -Id %s -ErrorAction SilentlyContinue | Measure-Object).Count" % PIDP], capture_output=True, text=True)
assert vivo.stdout.strip().splitlines()[-1] == "0", "o PID %s ainda existe: a parada nao se consumou" % PIDP
agora = datetime.datetime.now().astimezone().isoformat()
rec = {"passo": "10-bis-a", "servico": "um_bancada.py", "pid": int(PIDP),
       "pid_estado": "PID lido da porta 18777 antes da parada (processo criado em %s; linha de comando conferida), parado pelo PID; conferido aqui que ja nao existe; o recibo do religamento da v407 (RECIBO_RELIGAMENTO_v407.json, de %s/%s) registrou o PID %s, no ar desde %s: %s" % (CRIADO, rel407["hora_recibo"][8:10], rel407["hora_recibo"][5:7], pid_v407, rel407["no_ar_desde"], "igual ao parado" if str(pid_v407) == PIDP else "diferente do parado (o servico foi religado de novo depois do religamento da v407)"),
       "processos_um_bancada_vivos": n_proc,
       "linha_de_comando": r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py',
       "porta": 18777, "porta_fechada": True,
       "hora_recibo": agora, "hora": agora,
       "nota": ("nenhum processo um_bancada.py vivo e a porta 18777 fechada, conferidos por este script no momento do recibo; o script nao para nada: o servico foi religado no passo %s da v407 (PID %s, no ar desde %s); o PID parado, %s, e o lido da porta, "
                "e a parada que precede este recibo e feita pelo PID (nunca por nome), nao por este script; quem a executou e sob que ordem do operador consta em autorizacao_do_operador" % (rel407.get("passo"), pid_v407, rel407["no_ar_desde"], PIDP)),
       "religar": r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py',
       "autor": "claude-c1 (gerencia)", "autorizacao_do_operador": AUT}
p = os.path.join(D, "RECIBO_PARADA_v408.json")
assert not os.path.exists(p), "o recibo ja existe: nao sobrescrevo"
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
os.replace(p + ".tmp", p)
print("ok", p, "pid_parado", PIDP, "pid_recibo_v407", pid_v407, "processos", n_proc)
