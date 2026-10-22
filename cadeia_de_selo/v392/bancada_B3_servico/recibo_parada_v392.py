import datetime
import json
import os
import socket

D = os.path.dirname(os.path.abspath(__file__))
s = socket.socket()
s.settimeout(1)
aberta = s.connect_ex(("127.0.0.1", 18777)) == 0
s.close()
assert not aberta, "a porta 18777 está aberta"
rec = {"passo": "10-bis-a", "servico": "um_bancada.py", "pid": 118844,
       "linha_de_comando": r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py',
       "porta": 18777, "porta_fechada": True,
       "hora_recibo": datetime.datetime.now().astimezone().isoformat(),
       "nota": "o PID 118844 (iniciado 13/10 14:19) já não existia ao tentar a parada; porta 18777 conferida fechada",
       "religar": r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py',
       "autor": "claude-c1 (gerência), por autorização geral do operador de 13/10"}
p = os.path.join(D, "RECIBO_PARADA_v392.json")
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
os.replace(p + ".tmp", p)
print("ok", p)
