# -*- coding: utf-8 -*-
"""Uma linha-ponteiro no MEMORY.md abaixo de «## Estado corrente» (backup de bytes; tmp -> conferir -> os.replace; <24000 B, <=195 linhas)."""
import os, time
from pathlib import Path
M = Path("C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/MEMORY.md")
raw = M.read_bytes(); eol = b"\r\n" if b"\r\n" in raw else b"\n"
linha = ("- **[TREINO v4 DA IALD NATIVA — um.py v404 inteiro (29/10)](treino-nativa-v4-29out.md)** — **ordem do operador**: termos e estrutura, sem os resultados; "
         "Qwen3.6-35B-A3B mantido; salvaguardas de energia = padrão (`PROTOCOLO_PADRAO_DE_TREINO_IALD_NATIVA.md`); demo fora do ar durante o treino; D adiado por ele").encode("utf-8")
marca = b"## Estado corrente"; assert raw.count(marca) == 1; assert b"treino-nativa-v4-29out" not in raw
i = raw.index(marca); j = raw.index(eol, i) + len(eol); k = j + len(eol) if raw[j:j + len(eol)] == eol else j
novo = raw[:k] + linha + eol + raw[k:]
n_lin = novo.count(eol) + (0 if novo.endswith(eol) else 1)
assert len(novo) < 24000 and n_lin <= 195, (len(novo), n_lin)
ts = time.strftime("%Y%m%d_%H%M%S"); bak = M.with_name(M.name + ".bak_" + ts); bak.write_bytes(raw); assert bak.read_bytes() == raw
tmp = M.with_name(M.name + ".tmp_" + ts); tmp.write_bytes(novo); assert tmp.read_bytes() == novo
os.replace(tmp, M); print("MEMORY.md", len(raw), "->", len(M.read_bytes()), "B; linhas", n_lin, "; backup", bak.name)
