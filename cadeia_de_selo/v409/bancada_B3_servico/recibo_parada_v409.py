# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] a ORDEM da v409 e' a fala de 05/11/2026 (OPERADOR_05nov_prossigamos_v409_concordo_com_os_nomes_verbatim.txt; frase verbatim conferida no arquivo e no AUT; sha16 lido do arquivo); grava so' RECIBO_PARADA_v409.json
# (nota herdada da adaptacao da v408 [fork C da cadeia v408], com os rotulos subidos; reconferida em 05/11/2026 pelo fork B do claude-construtor-v409) molde v408/bancada_B3_servico/recibo_parada_v408.py (rotulos subidos por _bump_copia_v409.py; diff em bump/). Adaptado (v409): a autorizacao e' a ORDEM da v409 (fala do operador de 05/11/2026, OPERADOR_05nov_prossigamos_v409_concordo_com_os_nomes_verbatim.txt, sha16 LIDO do arquivo; a frase conferida no arquivo e no texto passado pelo orquestrador);
# o ultimo religamento conhecido segue sendo o do B(n) da v408 (RECIBO_RELIGAMENTO_v408.json: PID, no_ar_desde), e o recibo diz se o PID lido da porta e' o mesmo; as chaves do recibo sao as do recibo REAL da v408; nada de bundle nem de hash digitado.
"""10-bis-a da v409: recibo da parada do servico da Bancada Um (porta 18777), no molde do recibo_parada_v408.py. Passo da Bancada: B18 (a producao pina B17-v408-20261105-R1). A autorizacao e' a ORDEM da v409, do operador, de 05/11/2026 (a fala e' lida do arquivo e conferida contra o texto passado pelo orquestrador).
O ultimo religamento conhecido e' o do B(n) da v408 (RECIBO_RELIGAMENTO_v408.json, em v408/bancada_B3_servico): o PID registrado aqui e' o LIDO DA PORTA antes da parada; o recibo diz se e' o mesmo do religamento da v408 ou se o servico foi religado de novo depois."""
import datetime
import hashlib
import json
import os
import socket
import subprocess

D = os.path.dirname(os.path.abspath(__file__))
AUT = os.environ.get("V409_AUTORIZACAO_OPERADOR", "").strip()
assert AUT, "defina V409_AUTORIZACAO_OPERADOR com a ordem do operador que cobre este ato (data e texto): o script nao presume autorizacao"
# a autorizacao tem de ser a ORDEM da v409, de 05/11/2026 (nao a de 04/11 da v408 nem as anteriores): o sha16 da fala vem do ARQUIVO lido agora (nunca digitado) e a frase tem de estar no arquivo e no texto passado pelo orquestrador
ORDEM = os.path.join(D, "..", "..", "..", "cunhagens_13out", "OPERADOR_05nov_prossigamos_v409_concordo_com_os_nomes_verbatim.txt")
ORDEM_BYTES = open(ORDEM, "rb").read()
ORDEM_SHA16 = hashlib.sha256(ORDEM_BYTES).hexdigest()[:16]
FRASE_DA_ORDEM = "Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados"
assert FRASE_DA_ORDEM in ORDEM_BYTES.decode("utf-8") and FRASE_DA_ORDEM in AUT and ORDEM_SHA16 in AUT and "05/11/2026" in AUT, "a autorizacao passada nao e' a ordem do operador de 05/11/2026 (a ordem da v409: sha16 da fala lido do arquivo e a frase «%s» no texto)" % FRASE_DA_ORDEM
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
rel408 = json.load(open(os.path.join(D, "..", "..", "v408", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v408.json"), encoding="utf-8"))   # o ultimo religamento conhecido: o do B(n) da v408 (o servico que a v408 deixou no ar)
pid_v408 = rel408["pid"]
assert str(pid_v408).isdigit() and rel408.get("no_ar_desde") and rel408.get("hora_recibo"), rel408
# emenda da gerencia c1 (28/10/2026, antes do uso): o numero corrige a frase -- o PID registrado e o LIDO DA PORTA antes da parada (V409_PID_PARADO), nao o de nenhum recibo anterior,
# porque o servico pode ter sido religado de novo depois do ultimo recibo (o processo da porta foi criado em outra hora); o PID do recibo anterior (o da v408) fica ao lado, como referencia.
PIDP = os.environ.get("V409_PID_PARADO", "").strip()
assert PIDP.isdigit(), "defina V409_PID_PARADO com o PID lido da porta 18777 antes da parada (linha de comando conferida): o script nao presume o PID"
CRIADO = os.environ.get("V409_PID_PARADO_CRIADO", "").strip()
assert CRIADO, "defina V409_PID_PARADO_CRIADO com a data/hora de criacao do processo parado (lida de Win32_Process antes da parada)"
vivo = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-Process -Id %s -ErrorAction SilentlyContinue | Measure-Object).Count" % PIDP], capture_output=True, text=True)
assert vivo.stdout.strip().splitlines()[-1] == "0", "o PID %s ainda existe: a parada nao se consumou" % PIDP
agora = datetime.datetime.now().astimezone().isoformat()
rec = {"passo": "10-bis-a", "servico": "um_bancada.py", "pid": int(PIDP),
       "pid_estado": "PID lido da porta 18777 antes da parada (processo criado em %s; linha de comando conferida), parado pelo PID; conferido aqui que ja nao existe; o recibo do religamento da v408 (RECIBO_RELIGAMENTO_v408.json, de %s/%s) registrou o PID %s, no ar desde %s: %s" % (CRIADO, rel408["hora_recibo"][8:10], rel408["hora_recibo"][5:7], pid_v408, rel408["no_ar_desde"], "igual ao parado" if str(pid_v408) == PIDP else "diferente do parado (o servico foi religado de novo depois do religamento da v408)"),
       "processos_um_bancada_vivos": n_proc,
       "linha_de_comando": r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py',
       "porta": 18777, "porta_fechada": True,
       "hora_recibo": agora, "hora": agora,
       "nota": ("nenhum processo um_bancada.py vivo e a porta 18777 fechada, conferidos por este script no momento do recibo; o script nao para nada: o servico foi religado no passo %s da v408 (PID %s, no ar desde %s); o PID parado, %s, e o lido da porta, "
                "e a parada que precede este recibo e feita pelo PID (nunca por nome), nao por este script; quem a executou e sob que ordem do operador consta em autorizacao_do_operador" % (rel408.get("passo"), pid_v408, rel408["no_ar_desde"], PIDP)),
       "religar": r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py',
       "autor": "claude-c1 (gerencia)", "autorizacao_do_operador": AUT}
p = os.path.join(D, "RECIBO_PARADA_v409.json")
assert not os.path.exists(p), "o recibo ja existe: nao sobrescrevo"
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
os.replace(p + ".tmp", p)
print("ok", p, "pid_parado", PIDP, "pid_recibo_v408", pid_v408, "processos", n_proc)
