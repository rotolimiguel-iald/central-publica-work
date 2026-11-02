# -*- coding: utf-8 -*-
"""Acrescenta UMA linha-ponteiro ao MEMORY.md (índice da gerência) logo abaixo de «## Estado corrente», com backup de bytes, temporário →
conferir → substituir; respeita a regra dos dois arquivos (≤ 195 linhas, < 24.000 B) e depois a gerência re-pina com memoria.py pinar."""
import os, time
from pathlib import Path
M = Path("C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/MEMORY.md")
raw = M.read_bytes(); eol = b"\r\n" if b"\r\n" in raw else b"\n"
linha = ("- **[CONJUNTO D AUTORIZADO (29/10)](conjunto-d-autorizado-29out.md)** — **ordem do operador**: teste cego sob o V1 do ramo B (hash); "
         "D decide SÓ o par do ramo B; nada aberto antes do PODER com hash; `work\\conjunto_D_20261029`; **o teste em LLMs (P7) não dá o 5σ de β na natureza**").encode("utf-8")
marca = b"## Estado corrente"; assert raw.count(marca) == 1, raw.count(marca); assert b"conjunto-d-autorizado-29out" not in raw
i = raw.index(marca); j = raw.index(eol, i) + len(eol)
# pula a linha em branco que segue o cabeçalho, se houver
k = j + len(eol) if raw[j:j + len(eol)] == eol else j
novo = raw[:k] + linha + eol + raw[k:]
n_lin = novo.count(eol) + (0 if novo.endswith(eol) else 1)
assert len(novo) < 24000 and n_lin <= 195, (len(novo), n_lin)
ts = time.strftime("%Y%m%d_%H%M%S"); bak = M.with_name(M.name + ".bak_" + ts); bak.write_bytes(raw); assert bak.read_bytes() == raw
tmp = M.with_name(M.name + ".tmp_" + ts); tmp.write_bytes(novo); assert tmp.read_bytes() == novo and len(novo) > len(raw)
os.replace(tmp, M); print("MEMORY.md", len(raw), "->", len(M.read_bytes()), "B; linhas", n_lin, "; backup", bak.name)
