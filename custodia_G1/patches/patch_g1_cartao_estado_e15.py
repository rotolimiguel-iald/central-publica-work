# -*- coding: utf-8 -*-
"""G1 (25/10/2026, gerência a7): o CARTÃO DE ESTADO do site (estado.json, estado.txt, read-brief.txt) entra no E15.
A ORDEM 023 (auditoria de leitura por IA) pediu um cartão JSON/TXT enxuto numa URL estável, com o commit imutável do espelho, e uma
alternativa text/plain do read-brief. O gerador é v3.0_bancada/tools/gerar_cartao_estado.py. O E15 roda depois do push do espelho (E11),
então o HEAD já guarda o um.py do pino e o cartão sai com o commit. O _ja_e15 passa a exigir o pin16 também em estado.json e estado.txt.
Trocas contadas; backup de bytes; py_compile."""
import os, py_compile, time
from pathlib import Path

P = Path(r"C:\IALD\Central de Patentes\tools\custodia_g1\site.py")
raw = P.read_bytes(); s = raw.decode("utf-8")
CR, LF = chr(13), chr(10)
NL = CR + LF if (CR + LF) in s else LF
if "gerar_cartao_estado.py" in s:
    raise SystemExit("já aplicado")
pares = [
    ('''    faltam = [n for n in ("llms-full.txt", "index.md") if ctx.pin16 not in ctx.ler(ctx.c.SITE / n)]
    if not faltam:
        return aplicado("llms-full.txt e index.md trazem %s" % ctx.pin16)
''', '''    faltam = [n for n in ("llms-full.txt", "index.md", "estado.json", "estado.txt") if ctx.pin16 not in ctx.ler(ctx.c.SITE / n)]
    if not faltam:
        return aplicado("llms-full.txt, index.md e o cartão de estado trazem %s" % ctx.pin16)
'''),
    ('''def _ap_e15(ctx):
    exigir_rc0(_banc(ctx, "gerar_llms_full.py"), "gerar_llms_full.py")
''', '''def _ap_e15(ctx):
    exigir_rc0(_banc(ctx, "gerar_cartao_estado.py"), "gerar_cartao_estado.py")   # 25/10/2026 (ORDEM 023): estado.json, estado.txt, read-brief.txt
    exigir_rc0(_banc(ctx, "gerar_llms_full.py"), "gerar_llms_full.py")
'''),
    ('''escreve="SITE\\\\llms-full.txt, SITE\\\\index.md"),''',
     '''escreve="SITE\\\\llms-full.txt, SITE\\\\index.md, SITE\\\\estado.json, SITE\\\\estado.txt, SITE\\\\read-brief.txt"),'''),
]
for a, b in pares:
    a, b = a.replace(LF, NL), b.replace(LF, NL)
    n = s.count(a)
    assert n == 1, (a[:70], n)
    s = s.replace(a, b)
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, P)
print("site.py: E15 gera e confere o cartão de estado | %d -> %d" % (len(raw), P.stat().st_size))
