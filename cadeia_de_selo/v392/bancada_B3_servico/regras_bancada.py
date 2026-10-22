import datetime
import json
import os

P = "C:/Users/rotol/.claude/settings.json"
b = open(P, "rb").read()
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + ts + "_regras_bancada", "wb").write(b)
s = json.loads(b.decode("utf-8"))
allow = s["permissions"]["allow"]
regras = [
    r"PowerShell(Stop-Process -Id 118844 -Force)",
    r"""PowerShell(Start-Process "C:\Python314\pythonw.exe" -ArgumentList '-X','utf8','C:\IALD\Bancada_Um\um_bancada.py')""",
]
for r in regras:
    if r not in allow:
        allow.append(r)
t = json.dumps(s, ensure_ascii=False, indent=2) + "\n"
open(P + ".tmp", "w", encoding="utf-8", newline="\n").write(t)
json.load(open(P + ".tmp", encoding="utf-8"))
os.replace(P + ".tmp", P)
print("ok")
