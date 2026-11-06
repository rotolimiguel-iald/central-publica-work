# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] regras de permissao da cadeia v409 (RECUSA sem V409_REGRAS_AUTORIZADAS=sim; ato da gerencia; nao executado)
import datetime
import json
import os
import sys

if os.environ.get("V409_REGRAS_AUTORIZADAS") != "sim":
    raise SystemExit("RECUSO: regras_v409.py muda ~/.claude/settings.json (permissoes) e so' roda por ato da gerencia: defina V409_REGRAS_AUTORIZADAS=sim")

# regras_v409.py -- ESCRITO em 05/11/2026 pela preparacao da cadeia v409 (claude-construtor-v409) e NAO EXECUTADO (ordem da gerencia: nao rodar regras de permissao; o proprio script RECUSA sem V409_REGRAS_AUTORIZADAS=sim). Molde: regras_v408.py (subida de rotulo por _bump_copia_v409.py); os cinco comandos abaixo sao os atos que existem na pasta (instalar_v409.py, rito_v409.sh, conferir_rito_v409.py, reverter_v409.py, pos_rito/chain_pos_rito_v409.sh).
# Quando a gerencia mandar rodar: faz BACKUP de bytes de ~/.claude/settings.json e ACRESCENTA (nunca remove) as cinco regras de permissao da cadeia v409; o conteudo das regras e' so' o comando exato de cada ato.
P = "C:/Users/rotol/.claude/settings.json"
b = open(P, "rb").read()
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + ts + "_regras_v409", "wb").write(b)
s = json.loads(b.decode("utf-8"))
allow = s["permissions"]["allow"]
base = 'cd "/c/IALD/Central de Patentes/work/cadeia_de_selo/v409'
regras = [
    "Bash(" + base + '" && python -B -X utf8 instalar_v409.py:*)',
    "Bash(" + base + '" && sh ./rito_v409.sh:*)',
    "Bash(" + base + '" && python -B -X utf8 conferir_rito_v409.py:*)',
    "Bash(" + base + '" && python -B -X utf8 reverter_v409.py:*)',
    "Bash(" + base + '/pos_rito" && sh ./chain_pos_rito_v409.sh:*)',
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
