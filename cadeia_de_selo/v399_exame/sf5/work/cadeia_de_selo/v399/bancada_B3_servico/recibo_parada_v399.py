"""10-bis-a da v399: recibo da parada do servico da Bancada Um (porta 18777), no molde do recibo_parada_v398.py."""
import datetime
import json
import os
import socket
import subprocess

D = os.path.dirname(os.path.abspath(__file__))
AUT = os.environ.get("V399_AUTORIZACAO_OPERADOR", "").strip()
assert AUT, "defina V399_AUTORIZACAO_OPERADOR com a ordem do operador que cobre este ato (data e texto): o script nao presume autorizacao"
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
rel398 = json.load(open(os.path.join(D, "..", "..", "v398", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v398.json"), encoding="utf-8"))
pid_ultimo = rel398["pid"]
agora = datetime.datetime.now().astimezone().isoformat()
rec = {"passo": "10-bis-a", "servico": "um_bancada.py", "pid": pid_ultimo,
       "pid_estado": "ultimo PID conhecido do servico (religamento da v398, %s/%s); o processo ja nao existe" % (rel398["hora_recibo"][8:10], rel398["hora_recibo"][5:7]),
       "processos_um_bancada_vivos": n_proc,
       "linha_de_comando": r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py',
       "porta": 18777, "porta_fechada": True,
       "hora_recibo": agora, "hora": agora,
       "nota": ("nenhum processo um_bancada.py vivo e a porta 18777 fechada, conferidos por este script no momento do recibo; o script nao para nada: o servico foi religado no passo %s da v398 (PID %s), "
                "e a parada que precede este recibo e feita pelo PID (nunca por nome), nao por este script; quem a executou e sob que ordem do operador consta em autorizacao_do_operador" % (rel398.get("passo"), pid_ultimo)),
       "religar": r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py',
       "autor": "claude-c1 (gerencia)", "autorizacao_do_operador": AUT}
p = os.path.join(D, "RECIBO_PARADA_v399.json")
assert not os.path.exists(p), "o recibo ja existe: nao sobrescrevo"
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
os.replace(p + ".tmp", p)
print("ok", p, "pid_ultimo", pid_ultimo, "processos", n_proc)
