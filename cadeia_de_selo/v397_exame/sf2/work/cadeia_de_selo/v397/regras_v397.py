import datetime
import json
import os
import sys

if os.environ.get("V397_REGRAS_AUTORIZADAS") != "sim":
    raise SystemExit("RECUSO: regras_v397.py muda ~/.claude/settings.json (permissoes) e so' roda por ato da gerencia: defina V397_REGRAS_AUTORIZADAS=sim")

# regras_v397.py -- ESCRITO em 23/10/2026 pela preparacao da cadeia v397 e NAO EXECUTADO (ordem da gerencia: nao rodar regras de permissao). Molde: regras_v396.py.
# Quando a gerencia mandar rodar: faz BACKUP de bytes de ~/.claude/settings.json e ACRESCENTA (nunca remove) as cinco regras de permissao da cadeia v397; o conteudo das regras e' so' o comando exato de cada ato.
P = "C:/Users/rotol/.claude/settings.json"
b = open(P, "rb").read()
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + ts + "_regras_v397", "wb").write(b)
s = json.loads(b.decode("utf-8"))
allow = s["permissions"]["allow"]
base = 'cd "/c/IALD/Central de Patentes/work/cadeia_de_selo/v397'
regras = [
    "Bash(" + base + '" && python -B -X utf8 instalar_v397.py:*)',
    "Bash(" + base + '" && sh ./rito_v397.sh:*)',
    "Bash(" + base + '" && python -I -B -X utf8 conferir_rito_v397.py:*)',
    "Bash(" + base + '" && python -B -X utf8 reverter_v397.py:*)',
    "Bash(" + base + '/pos_rito" && sh ./chain_pos_rito_v397.sh:*)',
]
n0 = len(allow)
for r in regras:
    if r not in allow:
        allow.append(r)
t = json.dumps(s, ensure_ascii=False, indent=2) + "\n"
open(P + ".tmp", "w", encoding="utf-8", newline="\n").write(t)
json.load(open(P + ".tmp", encoding="utf-8"))
os.replace(P + ".tmp", P)
print("ok", n0, "->", len(allow))
