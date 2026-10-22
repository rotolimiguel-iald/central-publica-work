# -*- coding: utf-8 -*-
"""Regra dos dois arquivos (ordem do operador, 18/09): com o marcador v382 na linha da missao e a linha do handoff v382, o MEMORY.md passaria de 24 000 B.
Move VERBATIM para o fim do MEMORY_2.md duas linhas do indice, com marcador de origem, e deixa no MEMORY.md o ponteiro curto. Nada se corta:
  (1) a linha «HANDOFF v380 — as Fases 5–7 da Bancada por hash; custódia ... para a sessão do site» (a v380 ja foi custodiada pela sessao do site);
  (2) a linha da missao (o historico v381–v375 dos selos), que fica com o ponteiro curto da v381; o marcador da v382 entra depois, pela cadeia do selo.
Backup de bytes; tmp -> conferir -> replace. Fail-closed: aborta antes de tocar se nao achar exatamente as 2 linhas ou se a economia for < 250 B."""
import os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
UMEM = "C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"; ST = time.strftime("%Y%m%d_%H%M%S"); HOJE = time.strftime("%d/%m/%Y"); D = HOJE[:5]
M1, M2 = os.path.join(UMEM, "MEMORY.md"), os.path.join(UMEM, "MEMORY_2.md")
raw1, raw2 = open(M1, "rb").read(), open(M2, "rb").read()
assert b"\r\n" not in raw1
lines = raw1.decode("utf-8").split("\n")
movidas = []
for i, l in enumerate(lines):
    if l.startswith("- [HANDOFF v380 — as Fases 5–7 da Bancada por hash; custódia](handoff-v380-custodia.md) — "):
        movidas.append(l); lines[i] = "- [HANDOFF v380 — as Fases 5–7 da Bancada por hash; custódia](handoff-v380-custodia.md) — **01/10, para a sessão do site** (custodiada) · íntegra no MEMORY_2.md (movida %s)" % D
    elif l.startswith("- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — "):
        m = re.search(r"\*\*v381 SELADA 02/10 `([0-9a-f]{16})` (\d+/\d+) COMPLETA", l)
        assert m, "a linha da missao nao tem o marcador v381 esperado"
        movidas.append(l); lines[i] = "- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — **v381 SELADA 02/10 `%s` %s COMPLETA** · íntegra (v381–v375, cada selo) no MEMORY_2.md (movida %s)" % (m.group(1), m.group(2), D)
assert len(movidas) == 2, ("esperava mover 2 linhas; achei %d" % len(movidas), [x[:60] for x in movidas])
novo1 = "\n".join(lines).encode("utf-8")
assert len(novo1) <= len(raw1) - 250, ("economia insuficiente", len(raw1), len(novo1))
nl2 = "\r\n" if raw2.count(b"\r\n") > raw2.count(b"\n") // 2 else "\n"
bloco = ("\n\n## %s — linhas do índice movidas VERBATIM do MEMORY.md pela regra dos dois arquivos (compactação para a v382; o MEMORY.md passaria de 24 000 B)\n\n" % HOJE
         + "\n".join(movidas) + "\n").replace("\n", nl2)
novo2 = raw2 + bloco.encode("utf-8")
for p, raw in ((M1, raw1), (M2, raw2)):
    b = p + ".bak_" + ST + "_compact382"; assert not os.path.exists(b); open(b, "wb").write(raw); assert open(b, "rb").read() == raw
for p, novo, raw in ((M2, novo2, raw2), (M1, novo1, raw1)):
    tmp = p + ".tmp_" + ST; open(tmp, "wb").write(novo); assert os.path.getsize(tmp) == len(novo) and open(p, "rb").read() == raw; os.replace(tmp, p)
print("MEMORY.md %d -> %d B | MEMORY_2.md %d -> %d B | movidas %d linhas (verbatim no fim do MEMORY_2)" % (len(raw1), len(novo1), len(raw2), len(novo2), len(movidas)))
for x in movidas:
    print("  ->", x[:110])
