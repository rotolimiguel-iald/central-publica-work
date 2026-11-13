# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork B)] a ORDEM da v411 e' a fala do operador de 12/11/2026 (OPERADOR_12nov_otimo_vamos_rodar_tudo_pode_abrir_chegou_a_hora_da_v411_verbatim.txt; D169): o arquivo e' so' a fala, que e' LIDA inteira do arquivo (nunca digitada), o sha16 calculado na hora, a data 12/11/2026 no AUT; o resto do corpo (o passo B20, o recibo do religamento da v410 como ultimo conhecido, as chaves do recibo REAL da v410) ja' era o certo: nada de bundle nem de hash digitado
# (historico: o molde e' v410/bancada_B3_servico/recibo_parada_v410.py, adaptado na v410 a ordem da v410; a copia subiu por rotulo em _bump_copia_v411.py, diff em bump/; o corpo vem da adaptacao da v408 [fork C], conferido de versao a versao; na v411 so' a ORDEM muda, e as datas das ordens anteriores nao ficam no script porque o conferidor estatico as recusa)
# o ultimo religamento conhecido segue sendo o do B(n) da v410 (RECIBO_RELIGAMENTO_v410.json: PID, no_ar_desde), e o recibo diz se o PID lido da porta e' o mesmo; as chaves do recibo sao as do recibo REAL da v410; nada de bundle nem de hash digitado.
"""10-bis-a da v411: recibo da parada do servico da Bancada Um (porta 18777), no molde do recibo_parada_v410.py. Passo da Bancada: B20 (a producao pina B19-v410-20261111-R1). A autorizacao e' a ORDEM da v411, do operador, de 12/11/2026 (a ordem de abrir e a ordem da v411, D169; a fala inteira e' lida do arquivo e conferida contra o texto passado pelo orquestrador).
O ultimo religamento conhecido e' o do B(n) da v410 (RECIBO_RELIGAMENTO_v410.json, em v410/bancada_B3_servico): o PID registrado aqui e' o LIDO DA PORTA antes da parada; o recibo diz se e' o mesmo do religamento da v410 ou se o servico foi religado de novo depois."""
import datetime
import hashlib
import json
import os
import socket
import subprocess

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
rel410 = json.load(open(os.path.join(D, "..", "..", "v410", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v410.json"), encoding="utf-8"))   # o ultimo religamento conhecido: o do B(n) da v410 (o servico que a v410 deixou no ar)
pid_v410 = rel410["pid"]
assert str(pid_v410).isdigit() and rel410.get("no_ar_desde") and rel410.get("hora_recibo"), rel410
# emenda da gerencia c1 (28/10/2026, antes do uso): o numero corrige a frase -- o PID registrado e o LIDO DA PORTA antes da parada (V411_PID_PARADO), nao o de nenhum recibo anterior,
# porque o servico pode ter sido religado de novo depois do ultimo recibo (o processo da porta foi criado em outra hora); o PID do recibo anterior (o da v410) fica ao lado, como referencia.
PIDP = os.environ.get("V411_PID_PARADO", "").strip()
assert PIDP.isdigit(), "defina V411_PID_PARADO com o PID lido da porta 18777 antes da parada (linha de comando conferida): o script nao presume o PID"
CRIADO = os.environ.get("V411_PID_PARADO_CRIADO", "").strip()
assert CRIADO, "defina V411_PID_PARADO_CRIADO com a data/hora de criacao do processo parado (lida de Win32_Process antes da parada)"
vivo = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-Process -Id %s -ErrorAction SilentlyContinue | Measure-Object).Count" % PIDP], capture_output=True, text=True)
assert vivo.stdout.strip().splitlines()[-1] == "0", "o PID %s ainda existe: a parada nao se consumou" % PIDP
agora = datetime.datetime.now().astimezone().isoformat()
rec = {"passo": "10-bis-a", "servico": "um_bancada.py", "pid": int(PIDP),
       "pid_estado": "PID lido da porta 18777 antes da parada (processo criado em %s; linha de comando conferida), parado pelo PID; conferido aqui que ja nao existe; o recibo do religamento da v410 (RECIBO_RELIGAMENTO_v410.json, de %s/%s) registrou o PID %s, no ar desde %s: %s" % (CRIADO, rel410["hora_recibo"][8:10], rel410["hora_recibo"][5:7], pid_v410, rel410["no_ar_desde"], "igual ao parado" if str(pid_v410) == PIDP else "diferente do parado (o servico foi religado de novo depois do religamento da v410)"),
       "processos_um_bancada_vivos": n_proc,
       "linha_de_comando": r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py',
       "porta": 18777, "porta_fechada": True,
       "hora_recibo": agora, "hora": agora,
       "nota": ("nenhum processo um_bancada.py vivo e a porta 18777 fechada, conferidos por este script no momento do recibo; o script nao para nada: o servico foi religado no passo %s da v410 (PID %s, no ar desde %s); o PID parado, %s, e o lido da porta, "
                "e a parada que precede este recibo e feita pelo PID (nunca por nome), nao por este script; quem a executou e sob que ordem do operador consta em autorizacao_do_operador" % (rel410.get("passo"), pid_v410, rel410["no_ar_desde"], PIDP)),
       "religar": r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py',
       "autor": "claude-c1 (gerencia)", "autorizacao_do_operador": AUT}
p = os.path.join(D, "RECIBO_PARADA_v411.json")
assert not os.path.exists(p), "o recibo ja existe: nao sobrescrevo"
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
os.replace(p + ".tmp", p)
print("ok", p, "pid_parado", PIDP, "pid_recibo_v410", pid_v410, "processos", n_proc)
