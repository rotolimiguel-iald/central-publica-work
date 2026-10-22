# -*- coding: utf-8 -*-
"""Nota de CONTINUIDADE (05/10, rito v385 em curso) na memoria do pilar: se a sessao cair com o rito no meio, a proxima sabe que o marcador do servidor
parado agora mora no pacote v385. So acrescimo; backup de BYTES; temporario -> conferir -> substituir; idempotente pela marca."""
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "v384-pilar-quantico-gpu-02out.md")
SP = os.path.join("C:" + os.sep, "Users", "rotol", "AppData", "Local", "Temp", "claude", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d", "scratchpad")
MARCA = "<!-- rito_v385_em_curso_05out -->"
raw = open(P, "rb").read()
if MARCA.encode() in raw:
    print("JA ESTA"); sys.exit(0)
st = time.strftime("%Y%m%d_%H%M%S")
bak = P + ".bak_" + st + "_rito385"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
nl = "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"
txt = (MARCA + nl +
       "**05/10/2026, 10:37 — RITO v385 EM CURSO (gerência, em nome próprio):** o `um.py` `d406ae5725105145` foi instalado no Nós às 10:36 e o rito completo "
       "começou às 10:37:06, com o pilar de novo sob o mesmo V1 (chave `75dc30bc9cc8d330e31f99ca`). **O marcador do servidor parado agora mora no pacote v385:** `"
       + os.path.join(SP, "v385", ".servidor_parado_pelo_rito") + "` (restaurar=1). Se esta sessão cair antes do fim: conferir esse marcador e, com restaurar=1 e o "
       "rito morto, religar a tarefa «IALD Llama Server». A cadeia pós-rito da v385 roda em segundo plano (`" + os.path.join(SP, "v385_selo", "chain_pos_rito_v385.sh")
       + "`; saída em `chain_pos_rito_v385_REAL_out.txt`)." + nl)
novo = raw + (nl * 2).encode() + txt.encode("utf-8")
open(P + ".tmp", "wb").write(novo); assert os.path.getsize(P + ".tmp") == len(novo) > len(raw); os.replace(P + ".tmp", P)
assert open(P, "rb").read()[:len(raw)] == raw
print("OK", len(raw), "->", len(novo))
