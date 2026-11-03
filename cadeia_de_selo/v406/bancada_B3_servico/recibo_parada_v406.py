"""10-bis-a da v406: recibo da parada do servico da Bancada Um (porta 18777), no molde do recibo_parada_v405.py. Passo da Bancada: B15 (a producao pina B14-v405-20261102-R1). A autorizacao e' a ordem do operador de 02/11/2026 (a fala e' lida do arquivo e conferida contra o texto passado pelo orquestrador).
O ultimo religamento conhecido e' o de 02/11 (RELIGAMENTO_PREVIO_02nov.json, ao lado): o recibo da v405 fica como referencia, porque aquele processo nao sobreviveu aos reinicios da sessao."""
import datetime
import hashlib
import json
import os
import socket
import subprocess

D = os.path.dirname(os.path.abspath(__file__))
AUT = os.environ.get("V406_AUTORIZACAO_OPERADOR", "").strip()
assert AUT, "defina V406_AUTORIZACAO_OPERADOR com a ordem do operador que cobre este ato (data e texto): o script nao presume autorizacao"
# a autorizacao tem de ser a de 02/11/2026 (nao a de 01/11 da v405): o sha16 da fala vem do ARQUIVO lido agora (nunca digitado) e a frase tem de estar no arquivo e no texto passado pelo orquestrador
ORDEM = os.path.join(D, "..", "..", "..", "cunhagens_13out", "OPERADOR_02nov_quando_terminar_compile_v406_rode_publique_atualize_tudo_e_planeje_o_readme_pinado_com_o_4_44_sigma_verbatim.txt")
ORDEM_BYTES = open(ORDEM, "rb").read()
ORDEM_SHA16 = hashlib.sha256(ORDEM_BYTES).hexdigest()[:16]
FRASE_DA_ORDEM = "compile a nova versão do um.py, rode, publique e atualize tudo por favor"
assert FRASE_DA_ORDEM in ORDEM_BYTES.decode("utf-8") and FRASE_DA_ORDEM in AUT and ORDEM_SHA16 in AUT and "02/11/2026" in AUT, "a autorizacao passada nao e' a ordem do operador de 02/11/2026 (sha16 da fala lido do arquivo e a frase «%s» no texto)" % FRASE_DA_ORDEM
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
rel405 = json.load(open(os.path.join(D, "..", "..", "v405", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v405.json"), encoding="utf-8"))
pid_v405 = rel405["pid"]   # o religamento da v405 (02/11 00:24): referencia, de um processo que nao sobreviveu aos reinicios da sessao
prev = json.load(open(os.path.join(D, "RELIGAMENTO_PREVIO_02nov.json"), encoding="utf-8"))   # o religamento de 02/11 que antecede o B(n) da v406 (o servico estava fora do ar)
assert prev.get("contrato") == "RELIGAMENTO_PREVIO_v406" and prev.get("porta") == 18777 and str(prev.get("pid", "")).isdigit() and prev.get("criado"), prev
pid_ultimo = prev["pid"]
# emenda da gerencia c1 (28/10/2026, antes do uso): o numero corrige a frase -- o PID registrado e o LIDO DA PORTA antes da parada (V406_PID_PARADO), nao o de nenhum recibo anterior,
# porque o servico pode ter sido religado de novo depois do ultimo recibo (o processo da porta foi criado em outra hora); os PIDs dos recibos anteriores ficam ao lado, como referencia.
PIDP = os.environ.get("V406_PID_PARADO", "").strip()
assert PIDP.isdigit(), "defina V406_PID_PARADO com o PID lido da porta 18777 antes da parada (linha de comando conferida): o script nao presume o PID"
CRIADO = os.environ.get("V406_PID_PARADO_CRIADO", "").strip()
assert CRIADO, "defina V406_PID_PARADO_CRIADO com a data/hora de criacao do processo parado (lida de Win32_Process antes da parada)"
vivo = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-Process -Id %s -ErrorAction SilentlyContinue | Measure-Object).Count" % PIDP], capture_output=True, text=True)
assert vivo.stdout.strip().splitlines()[-1] == "0", "o PID %s ainda existe: a parada nao se consumou" % PIDP
agora = datetime.datetime.now().astimezone().isoformat()
rec = {"passo": "10-bis-a", "servico": "um_bancada.py", "pid": int(PIDP),
       "pid_estado": "PID lido da porta 18777 antes da parada (processo criado em %s; linha de comando conferida), parado pelo PID; conferido aqui que ja nao existe; o religamento previo de 02/11 (RELIGAMENTO_PREVIO_02nov.json) registrou o PID %s criado em %s, %s; o recibo da v405 (religamento de %s/%s) trazia o PID %s, de um processo que nao sobreviveu aos reinicios da sessao de 02/11" % (CRIADO, pid_ultimo, prev["criado"], "igual ao parado" if str(pid_ultimo) == PIDP else "diferente do parado (o servico foi religado de novo depois)", rel405["hora_recibo"][8:10], rel405["hora_recibo"][5:7], pid_v405),
       "processos_um_bancada_vivos": n_proc,
       "linha_de_comando": r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py',
       "porta": 18777, "porta_fechada": True,
       "hora_recibo": agora, "hora": agora,
       "nota": ("nenhum processo um_bancada.py vivo e a porta 18777 fechada, conferidos por este script no momento do recibo; o script nao para nada: o servico foi religado no passo %s da v405 (PID %s), nao sobreviveu aos reinicios da sessao de 02/11 e foi religado de novo (PID %s, criado em %s, RELIGAMENTO_PREVIO_02nov.json); o PID parado, %s, e o lido da porta, "
                "e a parada que precede este recibo e feita pelo PID (nunca por nome), nao por este script; quem a executou e sob que ordem do operador consta em autorizacao_do_operador" % (rel405.get("passo"), pid_v405, pid_ultimo, prev["criado"], PIDP)),
       "religar": r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py',
       "autor": "claude-c1 (gerencia)", "autorizacao_do_operador": AUT}
p = os.path.join(D, "RECIBO_PARADA_v406.json")
assert not os.path.exists(p), "o recibo ja existe: nao sobrescrevo"
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
os.replace(p + ".tmp", p)
print("ok", p, "pid_parado", PIDP, "pid_religamento_previo", pid_ultimo, "pid_recibo_v405", pid_v405, "processos", n_proc)
