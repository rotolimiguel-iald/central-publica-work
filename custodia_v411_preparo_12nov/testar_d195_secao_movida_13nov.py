# -*- coding: utf-8 -*-
"""Teste da D195 parte A (13/11/2026, claude-site-custodia): a seção das sete ressalvas MOVIDA no ESTADO_ATUAL.
Compara o retrato <PASTA>/*_antes.* com o estado atual do espelho (e grava *_depois.*):
- a seção (do título até o próximo «## ») é a MESMA, byte a byte; o ESTADO_ATUAL novo = o antigo com a seção movida, nada mais;
- a seção fica logo depois do bloco «Proved on three supports» e antes de «## The seal», dentro dos 100.000 primeiros caracteres;
- o README renderizado é o MESMO, byte a byte;
- o que saiu dos 100.000 primeiros caracteres (títulos e blocos), e se algum apresenta o resultado ou o selo;
- a F67 da página: o mesmo conjunto de achados antes e depois.
Uso: python -X utf8 testar_d195_secao_movida_13nov.py <PASTA_DO_RETRATO>"""
import re, subprocess, sys
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import h0dn  # noqa: E402

D = Path(sys.argv[1])
r = subprocess.run([sys.executable, "-X", "utf8", str(CEN / "work" / "custodia_v411_preparo_12nov" / "retrato_estado_readme_13nov.py"), str(D), "depois"],
                   capture_output=True, text=True, encoding="utf-8")
print(r.stdout.strip())
assert r.returncode == 0, r.stderr[-2000:]
RES = {"ok": 0, "falhas": []}


def caso(nome, cond, detalhe=""):
    if cond:
        RES["ok"] += 1
        print("  ok  ", nome)
    else:
        RES["falhas"].append(nome)
        print("  FALHA", nome, detalhe)


A = (D / "ESTADO_ATUAL_antes.md").read_text(encoding="utf-8")
N = (D / "ESTADO_ATUAL_depois.md").read_text(encoding="utf-8")
TIT = "## " + h0dn.TITULO_SECAO_RESSALVAS


def secao(t):
    i = t.index(TIT)
    j = t.index("\n## ", i + 1)
    return i, t[i:j + 1]


ia, sa = secao(A)
in_, sn = secao(N)
caso("a seção é a mesma, byte a byte (%d caracteres)" % len(sa), sa == sn)
caso("o novo = o antigo com a seção movida, nada mais", A.replace(sa, "", 1) == N.replace(sn, "", 1))
seal = N.index("## The seal")
prov = N.index("## Proved on three supports")
caso("no novo: «Proved on three supports» (%d) < a seção (%d) < «## The seal» (%d)" % (prov, in_, seal), prov < in_ < seal and N[in_ + len(sn):].startswith("## The seal"))
caso("a seção inteira está nos 100.000 primeiros caracteres (termina em %d)" % (in_ + len(sn)), in_ + len(sn) <= 100000)
caso("o README renderizado é o mesmo, byte a byte", (D / "README_renderizado_antes.md").read_bytes() == (D / "README_renderizado_depois.md").read_bytes())
fa, fn = sorted(t for _, t in h0dn.f67(A)), sorted(t for _, t in h0dn.f67(N))
caso("a F67 da página: o mesmo conjunto antes e depois (%d achados)" % len(fn), fa == fn, (len(fa), len(fn)))
# o que saiu dos 100.000 primeiros caracteres
corte = 100000
print("\n  o que saiu dos %d primeiros caracteres (deslocamento de %d caracteres):" % (corte, len(sn)))
heads_a = [(m.start(), m.group(0)) for m in re.finditer(r"^#{1,4} [^\n]+", A, re.M)]
pos_n = {h: m.start() for m in re.finditer(r"^#{1,4} [^\n]+", N, re.M) for h in [m.group(0)]}
fora = [(pa, h, pos_n.get(h)) for pa, h in heads_a if pa < corte and (pos_n.get(h) or 0) >= corte]
for pa, h, pn in fora:
    print("     título %r: %d -> %d" % (h[:110], pa, pn))
# o bloco que cruzou o corte: o texto do antigo entre (corte - deslocamento) e corte, que agora fica além do corte
saiu = A[corte - len(sn):corte] if ia > corte else ""
blocos = [b for b in re.split(r"\n\s*\n", saiu) if b.strip()]
print("     texto que cruzou o corte: %d caracteres, %d bloco(s)" % (len(saiu), len(blocos)))
for b in blocos:
    print("       · %s%s" % (b.strip()[:160].replace("\n", " | "), " …" if len(b.strip()) > 160 else ""))
RX_RES = re.compile(r"6[.,]11|6\{,\}11|acima de 5\s*σ|above 5\s*σ|H0DN|BG1", re.I)
RX_SELO = re.compile(r"## The seal|pin_um_py|1203b1f9202020d6|um_absoluto_selo", re.I)
apres = [b[:100] for b in blocos if RX_RES.search(b) or RX_SELO.search(b)]
caso("nada que saiu apresenta o resultado ou o selo", not apres, apres)
print("\nRESULTADO: %d ok, %d falha(s)%s" % (RES["ok"], len(RES["falhas"]), (": " + "; ".join(RES["falhas"])) if RES["falhas"] else ""))
sys.exit(1 if RES["falhas"] else 0)
