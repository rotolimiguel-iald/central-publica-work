# -*- coding: utf-8 -*-
"""_marca_adaptado_v410.py -- (claude-construtor-v410, 06/11/2026) troca a marca `# [A ADAPTAR v410] ...` (a linha que o bump pos) pela marca `# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] <nota>`
e devolve as marcas herdadas da v409 (que o bump subiu para «[ADAPTADO v410, 05/11/2026, claude-construtor-v410]») ao rotulo verdadeiro (v409). Backup de BYTES antes; o fim de linha de cada linha e' preservado.
Uso: python -I -B -X utf8 _marca_adaptado_v410.py <arquivo> "<nota>" [<arquivo> "<nota>" ...]"""
import datetime, os, re, sys
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
args = sys.argv[1:]
assert args and len(args) % 2 == 0, "uso: arquivo nota [arquivo nota ...]"
for p, nota in zip(args[0::2], args[1::2]):
    raw = open(p, "rb").read(); t = raw.decode("utf-8")
    linhas = t.split("\n")
    idx = [i for i, l in enumerate(linhas[:4]) if l.startswith("# [A ADAPTAR v410]")]
    assert len(idx) == 1, (p, "marca [A ADAPTAR v410] nao achada nas 4 primeiras linhas")
    i = idx[0]; cr = "\r" if linhas[i].endswith("\r") else ""
    linhas[i] = "# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] " + nota + cr
    n_her = 0
    for k, l in enumerate(linhas):
        if l.startswith("#") and "[ADAPTADO v410, 05/11/2026, claude-construtor-v410]" in l:
            linhas[k] = l.replace("[ADAPTADO v410, 05/11/2026, claude-construtor-v410]", "[ADAPTADO v409, 05/11/2026, claude-construtor-v409 -- marca herdada da v409]"); n_her += 1
    novo = "\n".join(linhas).encode("utf-8")
    bk = p + ".bak_" + ts + "_marca"
    open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo); os.replace(p + ".tmp", p)
    if p.endswith(".py"):
        import ast; ast.parse(novo.decode("utf-8"))
    print(p, "marca trocada; herdadas devolvidas:", n_her)
