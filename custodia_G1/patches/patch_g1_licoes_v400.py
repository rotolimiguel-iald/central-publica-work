# -*- coding: utf-8 -*-
"""G1 (25/10/2026, gerência a7): três lições da custódia conjunta v399+v400 (LICOES_v400_25out.md, «A fazer»).
 1. util.ascii_sem_acento apagava as letras gregas do assunto do commit («o α de uma linha só» virou «o  de uma linha so», commit b8e028fb).
    Agora as gregas e os sinais da casa são transliterados ANTES da decomposição (α→alfa, β→beta, σ→sigma, ≠→!=, →→->, —→-).
 2. --trabalho relativo quebrava o commit do E10 (o git roda com -C noutra pasta): o caminho passa a absoluto logo depois do parse.
 3. O E08 dizia APLICADO quando o README tinha o pin16 (que o E06 já escreve no bloco das portas) sem a FRENTE ter sido regerada.
    Agora o _ja_e08 exige também a linha da tabela da frente «| version · versão | **vN** (sealed».
Trocas contadas; backup de bytes; py_compile. Rodar só com o G1 parado."""
import os, py_compile, time
from pathlib import Path

T = Path(r"C:\IALD\Central de Patentes\tools")
TS = time.strftime("%Y%m%d_%H%M%S")
CR, LF = chr(13), chr(10)


def patch(p, pares, marca):
    raw = p.read_bytes(); s = raw.decode("utf-8")
    if marca in s:
        print(p.name, "já aplicado"); return
    nl = CR + LF if (CR + LF) in s else LF
    for a, b in pares:
        a, b = a.replace(LF, nl), b.replace(LF, nl)
        n = s.count(a)
        assert n == 1, (p.name, a[:70], n)
        s = s.replace(a, b)
    p.with_name(p.name + ".bak_" + TS).write_bytes(raw)
    t = p.with_name(p.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, p)
    print(p.name, len(raw), "->", p.stat().st_size)


patch(T / "custodia_g1" / "util.py", [(
'''def ascii_sem_acento(s):
    import unicodedata
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
''',
'''_TRANSLIT = {  # 25/10/2026: as gregas e os sinais da casa viram palavras ANTES da decomposição (o commit b8e028fb perdeu o «α»)
    "\\u03b1": "alfa", "\\u03b2": "beta", "\\u03b3": "gama", "\\u03b4": "delta", "\\u0394": "Delta", "\\u03b5": "epsilon",
    "\\u03b8": "theta", "\\u03ba": "kappa", "\\u03bb": "lambda", "\\u039b": "Lambda", "\\u03bc": "mu", "\\u03bd": "nu",
    "\\u03c0": "pi", "\\u03c1": "rho", "\\u03c3": "sigma", "\\u03a3": "Sigma", "\\u03c4": "tau", "\\u03c6": "phi",
    "\\u03c7": "chi", "\\u03c8": "psi", "\\u03c9": "omega", "\\u03a9": "Omega",
    "\\u2260": "!=", "\\u2192": "->", "\\u2190": "<-", "\\u21d2": "=>", "\\u2264": "<=", "\\u2265": ">=", "\\u2014": "-", "\\u2013": "-",
    "\\u00d7": "x", "\\u221a": "sqrt", "\\u2248": "~", "\\u00b7": ".", "\\u2026": "...",
}


def ascii_sem_acento(s):
    import unicodedata
    s = "".join(_TRANSLIT.get(ch, ch) for ch in s)
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
''')], "_TRANSLIT = {")

patch(T / "custodiar.py", [(
'''    a = ap.parse_args(argv)
    try:
''',
'''    a = ap.parse_args(argv)
    if getattr(a, "trabalho", None):              # 25/10/2026: --trabalho relativo quebrou o commit do E10 — sempre absoluto
        a.trabalho = str(Path(a.trabalho).resolve())
    try:
''')], "--trabalho relativo quebrou")

patch(T / "custodia_g1" / "espelho.py", [(
'''    if not _portas_ok(ctx):
        return falta("PORTA/TUNEL/README não trazem %s" % ctx.pin16)
    d = auditar_numeros_citados(ctx)
''',
'''    if not _portas_ok(ctx):
        return falta("PORTA/TUNEL/README não trazem %s" % ctx.pin16)
    if ("| version \\u00b7 vers\\u00e3o | **%s** (sealed" % ctx.versao) not in ctx.ler(ctx.c.TB / "README.md"):   # 25/10/2026: o pin16 do bloco das portas não prova a frente
        return falta("a frente do README não foi regerada para %s (linha «version · versão» da tabela ausente)" % ctx.versao)
    d = auditar_numeros_citados(ctx)
''')], "o pin16 do bloco das portas não prova a frente")
