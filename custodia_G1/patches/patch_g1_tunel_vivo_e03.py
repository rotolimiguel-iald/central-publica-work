# -*- coding: utf-8 -*-
"""G1 (25/10/2026, gerência a7, custódia v401): o TÚNEL é pasta VIVA — o Codex e a gerência escrevem nele o tempo todo. O _ja_e03 comparava a
cópia do túnel no espelho com o túnel vivo: qualquer ordem ou entrega nova depois do E03 reabria o E03 como FALTA, e o reaplicar falhava nas
pré-condições (espelho já na versão; árvore com o trabalho da própria custódia). Aconteceu na v400 (retomada) e na v401 (adendo B dos filmes).
Agora, com o espelho na versão, pares do tipo TUNEL com destino ausente ou tamanho diferente são «registros novos do túnel desde a cópia» e
entram na PRÓXIMA custódia: não reabrem o E03. Selados, declarados, stdouts, cache e kernel seguem conferidos como antes.
Trocas contadas; backup de bytes; py_compile. Rodar só com o G1 parado."""
import os, py_compile, time
from pathlib import Path

P = Path(r"C:\IALD\Central de Patentes\tools\custodia_g1\espelho.py")
raw = P.read_bytes(); s = raw.decode("utf-8")
CR, LF = chr(13), chr(10)
NL = CR + LF if (CR + LF) in s else LF
if "túnel vivo:" in s:
    raise SystemExit("já aplicado")
a = '''    pend, tot = EP.comparar(P, profundo=("SELADO",), barrados=barr)        # existe+tamanho em tudo; sha256 nos selados (o que o selo lista)
    ruim, orf = EP.comparar_kernel(ctx, P, profundo=True)                  # kernel: sha256 de cada arquivo formal (≈0,3 s)
    if pend or ruim or orf:
        return falta("%d de %d pares por copiar/diferentes; kernel: %d faltando/diferentes, %d órfãos" % (len(pend), tot, len(ruim), len(orf)))
    return aplicado("%d pares presentes no espelho (selados e kernel conferidos por sha256; %d barrados pela guarda, ditos no relatório); kernel %d arquivos" % (tot, len(barr), len(P.kernel["fmap"])))
'''
b = '''    pend, tot = EP.comparar(P, profundo=("SELADO",), barrados=barr)        # existe+tamanho em tudo; sha256 nos selados (o que o selo lista)
    ruim, orf = EP.comparar_kernel(ctx, P, profundo=True)                  # kernel: sha256 de cada arquivo formal (≈0,3 s)
    # 25/10/2026: o TÚNEL é pasta VIVA; com o espelho na versão, o que entrou ou mudou nele depois da cópia vai na PRÓXIMA custódia
    tun = [x for x in pend if x[2] == "TUNEL" and x[3] in ("destino ausente", "tamanho difere")] if rel == "igual" else []
    pend = [x for x in pend if x not in tun]
    if pend or ruim or orf:
        return falta("%d de %d pares por copiar/diferentes; kernel: %d faltando/diferentes, %d órfãos" % (len(pend), tot, len(ruim), len(orf)))
    return aplicado("%d pares presentes no espelho (selados e kernel conferidos por sha256; %d barrados pela guarda, ditos no relatório); kernel %d arquivos%s" % (
        tot, len(barr), len(P.kernel["fmap"]), ("; túnel vivo: %d registro(s) novo(s) desde a cópia, para a próxima custódia" % len(tun)) if tun else ""))
'''
a2, b2 = a.replace(LF, NL), b.replace(LF, NL)
assert s.count(a2) == 1, ("o fim do _ja_e03 mudou de forma — PARAR", s.count(a2))
s = s.replace(a2, b2)
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, P)
print("espelho.py: E03 tolera o túnel vivo | %d -> %d" % (len(raw), P.stat().st_size))
