# -*- coding: utf-8 -*-
"""Insere na nota da GPU do artigo (PT e EN) a LEITURA do operador de 03/10/2026 («A forma matricial do verbo [...] "sobrenome" [...]»), verbatim do transcrito,
com [ONTO] e a correspondencia estrutural exata no sistema do pilar [DERIVED de leitura]. Nao muda o que se calcula."""
import ast, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
verb = None
with open(T, encoding="utf-8") as f:
    for line in f:
        if "A forma matricial do verbo" not in line:
            continue
        d = json.loads(line)
        if d.get("type") == "user":
            c = d.get("message", {}).get("content")
            for t in ([c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]):
                if t.strip().startswith("A forma matricial do verbo"):
                    verb = t.strip()
assert verb and not any(ch in verb for ch in "\\%&_#$^{}~"), "o verbatim tem caractere especial do LaTeX"
V = repr(verb)
BS = chr(92)
PT = [
    "    _sobrenome4 = " + V + "   # a cunhagem do operador (03/10/2026), verbatim do transcrito",
    '    s.append(r"\\textbf{Leitura do operador} \\textsf{[ONTO]} (03/10/2026, verbatim): ``" + _sobrenome4 + r"\'\'. "',
    '             r"A correspondência estrutural, exata neste sistema \\textsf{[DERIVED de leitura]}: $K\\Pi=0$ --- o Nome, como matriz, é o zero do operador modular ---; "',
    '             r"$L_{\\rm anti}\\Pi=0$; uma inscrição no bloco do Nome fica intocada pelo \\emph{dephasing} ($V_tP_F=P_F$, conferida pela GPU em cada $d$); "',
    '             r"e o Nome entra no objeto estacionário pelo traço, $\\mathrm{CCI}=\\mathrm{Tr}\\,\\Pi\\rho$ --- o índice que relaciona a identidade nominada sem retirá-la.")',
]
EN = [
    "    _sobrenome4 = " + V + "   # the operator's coinage (2026-10-03), verbatim from the transcript",
    '    s.append(r"\\textbf{The operator\'s reading} \\textsf{[ONTO]} (2026-10-03, verbatim, in Portuguese): ``" + _sobrenome4 + r"\'\'. "',
    '             r"The structural correspondence, exact in this system \\textsf{[DERIVED from reading]}: $K\\Pi=0$ --- the Name, as a matrix, is the zero of the modular operator ---; "',
    '             r"$L_{\\rm anti}\\Pi=0$; an inscription in the Name\'s block is left untouched by dephasing ($V_tP_F=P_F$, checked by the GPU at every $d$); "',
    '             r"and the Name enters the stationary object through the trace, $\\mathrm{CCI}=\\mathrm{Tr}\\,\\Pi\\rho$ --- the index that relates the named identity without removing it.")',
]
for fn, anchor, ins in (("artigo_pt_v384.pysnip", '    s.append(r"' + BS + 'textbf{O motor.}', PT), ("artigo_en_v384.pysnip", '    s.append(r"' + BS + 'textbf{The engine.}', EN)):
    p = os.path.join(HERE, fn)
    s = open(p, encoding="utf-8").read()
    if "_sobrenome4" in s:
        print(fn, "ja tem"); continue
    assert s.count(anchor) == 1, (fn, s.count(anchor))
    open(p + ".bak_antes_sobrenome", "w", encoding="utf-8", newline="").write(s)
    s2 = s.replace(anchor, "\n".join(ins) + "\n" + anchor)
    src = "def build(core, verdict, data_path):\n    s=[]; b=0.012; _nclean=1\n    _sci=lambda x,n: str(x)\n" + s2 + "    return s\n"
    ast.parse(src); ns = {}; exec(src, ns); out = ns["build"]({}, {}, "")
    hit = [x for x in out if "sobrenome" in x]
    assert hit and (BS + "Pi=0") in hit[0] and (BS + "mathrm{CCI}") in hit[0], hit[:1]
    open(p + ".tmp", "w", encoding="utf-8", newline=chr(10)).write(s2); os.replace(p + ".tmp", p)
    print(fn, "ok |", hit[0][:220])
