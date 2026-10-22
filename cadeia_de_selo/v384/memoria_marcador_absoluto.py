# -*- coding: utf-8 -*-
"""5a afericao (#9a): o caminho do marcador do servidor na memoria passa a ser ABSOLUTO (o scratchpad e' por sessao). MEMORY.md: a linha da v384 com o caminho
absoluto (a anterior vai VERBATIM ao MEMORY_2.md); a memoria da v384: errata AO LADO do bloco 9 (so acrescimo). Backups de BYTES; <= 24 000 B."""
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
MD = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
M1 = os.path.join(MD, "MEMORY.md"); M2 = os.path.join(MD, "MEMORY_2.md"); MV = os.path.join(MD, "v384-pilar-quantico-gpu-02out.md")
ABS = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".servidor_parado_pelo_rito")
assert ABS.startswith("C:\\Users\\rotol\\AppData\\Local\\Temp\\claude\\c--IALD-Central-de-Patentes\\6da8f00d-d44f-4888-a88d-fc9f73eead3d\\scratchpad\\v384\\"), ABS
ts = time.strftime("%Y%m%d_%H%M%S")
R = {p: open(p, "rb").read() for p in (M1, M2, MV)}
for p, r in R.items():
    open(p + ".bak_" + ts, "wb").write(r); assert open(p + ".bak_" + ts, "rb").read() == r
linhas = R[M1].decode("utf-8").split("\n")
idx = [i for i, l in enumerate(linhas) if l.startswith("- [v384 — O PILAR QUÂNTICO NA GPU")]
assert len(idx) == 1
velha = linhas[idx[0]]
nova = "- [v384 — PILAR QUÂNTICO NA GPU](v384-pilar-quantico-gpu-02out.md) — **REGRA: ao abrir sessão, conferir `%s`; com restaurar=1, religar «IALD Llama Server»** · íntegra MEMORY_2.md" % ABS
linhas[idx[0]] = nova
n1 = "\n".join(linhas).encode("utf-8"); assert len(n1) <= 24000, len(n1)
n2 = R[M2] + ("\n\n<!-- movida 04/10/2026 pela regra dos dois arquivos (o caminho do marcador passa a ser absoluto): a linha da v384 do MEMORY.md, VERBATIM -->\n" + velha + "\n").encode("utf-8")
nv = R[MV] + ("\n\n<!-- errata_bloco9_caminho_absoluto_04out -->\n**ERRATA AO LADO do bloco 9 (04/10/2026, gerência; 5ª aferição #9a):** o caminho do marcador escrito acima é RELATIVO ao scratchpad, que muda a cada sessão. "
              "O caminho que vale é o ABSOLUTO: `%s`.\n" % ABS).encode("utf-8")
for p, n in ((M2, n2), (MV, nv), (M1, n1)):
    tmp = p + ".tmp_" + ts; open(tmp, "wb").write(n); assert os.path.getsize(tmp) == len(n); os.replace(tmp, p)
assert open(M2, "rb").read().startswith(R[M2]) and open(MV, "rb").read().startswith(R[MV])
print("MEMORY.md", len(R[M1]), "->", len(n1), "| MEMORY_2.md", len(R[M2]), "->", len(n2), "| v384", len(R[MV]), "->", len(nv))
