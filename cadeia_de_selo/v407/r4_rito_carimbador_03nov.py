# -*- coding: utf-8 -*-
"""03/11/2026 18:0x, gerencia c1 (pedido do gerente central do LAR, 03/11, para o filme em par; a v406 saiu sem o jsonl de tempos): o rito v407 passa a gravar, ALEM do stdout canonico
identico em bytes (rodada_v407_stdout.txt, no Nos, como sempre), o rodada_v407_stdout_tempos.jsonl no PACOTE (ao lado de rito_horarios_v407.txt; o inventario do Nos nao muda), por meio do
carimbador binario-seguro carimbar_stdout_v407.py (testado no scratchpad: bytes identicos, sha256 igual, RC do um.py preservado por pipefail, carimbos em tempo real com PYTHONUNBUFFERED=1
so' no subshell do rito). A linha de lancamento do um.py fica literal (invariante do conferidor); o comentario novo NAO a repete, para nao mudar contagens. Um jsonl anterior e' renomeado
com data, como o stdout de tentativa. Troca em bytes com backup; `sh -n` em seguida. Escrito pelo Write (a edicao inline anterior falhou pelo colapso de barras do heredoc)."""
import os, subprocess, time
V7 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v407"; ARQ = os.path.join(V7, "rito_v407.sh"); TS = time.strftime("%Y%m%d_%H%M%S")
O1 = b'( echo 1 | python um.py > rodada_v407_stdout.txt 2>&1 ) &\n'
N1 = (b'# [03/11, pedido do gerente do LAR para o filme em par] o stdout canonico segue IDENTICO em bytes em rodada_v407_stdout.txt (no Nos); o carimbador grava ao lado, NO PACOTE, o rodada_v407_stdout_tempos.jsonl\n'
      b'# ({linha, hora_utc, bytes} por linha + registro final com bytes_total e sha256 do stdout antes do trailer). pipefail: o RC do subshell e\' o do um.py (o carimbador so\' falha com rc 3 se os bytes gravados diferirem dos recebidos).\n'
      b'# PYTHONUNBUFFERED=1 so\' neste subshell: cada linha chega ao carimbador quando o um.py a escreve. A linha de lancamento do um.py fica literal (invariante do conferidor).\n'
      b'[ -f "$PK/rodada_v407_stdout_tempos.jsonl" ] && mv "$PK/rodada_v407_stdout_tempos.jsonl" "$PK/rodada_v407_stdout_tempos_tentativa_$(date +%Y%m%d_%H%M%S).jsonl"\n'
      b'( set -o pipefail; export PYTHONUNBUFFERED=1; echo 1 | python um.py 2>&1 | python -u "$PK/carimbar_stdout_v407.py" rodada_v407_stdout.txt "$PK/rodada_v407_stdout_tempos.jsonl" ) &\n')
b = open(ARQ, "rb").read()
nl = b"\r\n" if b.count(b"\r\n") > b.count(b"\n") // 2 else b"\n"
o1 = O1.replace(b"\n", nl); n1 = N1.replace(b"\n", nl)
assert b.count(o1) == 1, b.count(o1)
novo = b.replace(o1, n1)
assert novo.count(b"echo 1 | python um.py") == b.count(b"echo 1 | python um.py") and b"carimbar_stdout_v407.py" in novo and novo.count(b"rodada_v407_stdout.txt") == b.count(b"rodada_v407_stdout.txt") + 1
bak = ARQ + ".bak_r4_carimbador_" + TS; open(bak, "xb").write(b); assert open(bak, "rb").read() == b
tmp = ARQ + ".tmp_" + TS; open(tmp, "xb").write(novo); assert os.path.getsize(tmp) == len(novo); os.replace(tmp, ARQ); assert open(ARQ, "rb").read() == novo
print("rito_v407.sh: %d -> %d B (fim de linha %r); backup %s" % (len(b), len(novo), nl, os.path.basename(bak)))
r = subprocess.run([r"C:\Program Files\Git\bin\sh.exe", "-n", ARQ], capture_output=True, text=True); assert r.returncode == 0, r.stderr; print("sh -n ok")
assert os.path.exists(os.path.join(V7, "carimbar_stdout_v407.py"))
