# -*- coding: utf-8 -*-
"""MEMORY.md: a linha da v384 passa a carregar a REGRA do marcador do servidor (lida em toda sessao); a linha anterior vai VERBATIM ao MEMORY_2.md (regra dos dois
arquivos: o excesso vai para o segundo, nunca se corta). Backup de BYTES dos dois antes; temporario -> conferir -> substituir; MEMORY.md <= 24 000 B."""
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
MD = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
M1 = os.path.join(MD, "MEMORY.md"); M2 = os.path.join(MD, "MEMORY_2.md")
r1 = open(M1, "rb").read(); r2 = open(M2, "rb").read()
ts = time.strftime("%Y%m%d_%H%M%S")
for p, r in ((M1, r1), (M2, r2)):
    open(p + ".bak_" + ts, "wb").write(r); assert open(p + ".bak_" + ts, "rb").read() == r
t1 = r1.decode("utf-8")
linhas = t1.split("\n")
idx = [i for i, l in enumerate(linhas) if l.startswith("- [v384 — O PILAR QUÂNTICO NA GPU")]
assert len(idx) == 1, idx
velha = linhas[idx[0]]
nova = ("- [v384 — O PILAR QUÂNTICO NA GPU (ordem 02/10)](v384-pilar-quantico-gpu-02out.md) — **REGRA: ao abrir sessão, conferir `scratchpad\\v384\\.servidor_parado_pelo_rito`; "
        "com restaurar=1, religar a tarefa «IALD Llama Server»** (bloco 9) · íntegra no MEMORY_2.md (movida 02/10 e 03/10)")
linhas[idx[0]] = nova
n1 = "\n".join(linhas).encode("utf-8")
assert len(n1) <= 24000, len(n1)
n2 = r2 + ("\n\n<!-- movida 03/10/2026 pela regra dos dois arquivos: a linha da v384 do MEMORY.md, VERBATIM -->\n" + velha + "\n").encode("utf-8")
for p, n, r in ((M2, n2, r2), (M1, n1, r1)):
    tmp = p + ".tmp_" + ts
    open(tmp, "wb").write(n); assert os.path.getsize(tmp) == len(n)
    os.replace(tmp, p)
assert open(M2, "rb").read().startswith(r2) and velha.encode("utf-8") in open(M2, "rb").read()
print("MEMORY.md", len(r1), "->", len(n1), "| MEMORY_2.md", len(r2), "->", len(n2))
