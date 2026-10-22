"""10-bis-a da v394: recibo da parada do servico da Bancada Um (porta 18777), no molde do recibo_parada_v392.py."""
import datetime
import json
import os
import socket
import subprocess

D = os.path.dirname(os.path.abspath(__file__))
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
rel392 = json.load(open(os.path.join(D, "..", "..", "v392", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v392.json"), encoding="utf-8"))
pid_ultimo = rel392["pid"]
agora = datetime.datetime.now().astimezone().isoformat()
rec = {"passo": "10-bis-a", "servico": "um_bancada.py", "pid": pid_ultimo,
       "pid_estado": "ultimo PID conhecido do servico (religamento da v392, 13/10); o processo ja nao existe",
       "processos_um_bancada_vivos": n_proc,
       "linha_de_comando": r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py',
       "porta": 18777, "porta_fechada": True,
       "hora_recibo": agora, "hora": agora,
       "nota": "o servico ja estava fora do ar antes da v394 (indisponivel desde 16/10, DELIVERY_D_R1): nenhum processo um_bancada.py "
               "e a porta 18777 fechada, conferidas por este script; nada foi parado por esta cadeia",
       "religar": r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py',
       "autor": "claude-c1 (gerencia), por autorizacao geral do operador (13/10 e 19/10)"}
p = os.path.join(D, "RECIBO_PARADA_v394.json")
assert not os.path.exists(p), "o recibo ja existe: nao sobrescrevo"
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
os.replace(p + ".tmp", p)
print("ok", p, "pid_ultimo", pid_ultimo, "processos", n_proc)
