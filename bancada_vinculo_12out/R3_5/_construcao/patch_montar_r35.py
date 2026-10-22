# -*- coding: utf-8 -*-
"""patch_montar_r35.py (R3.5, 19/10/2026) -- converte o montar_sandbox.py da R3.4 (copia de bytes em R3_5) para a R3.5: o b1 deixa de ler o Nos REAL (no meio do rito da v394) e passa a ser pinado num
stand-in da CUSTODIA v393 (nos_real/); nasce b1real (o manifesto pinando o caminho real, so para a guarda A2) e o stand-in do Nos v394 com o candidato real (nos_v394s/, b1v394s/).
uso: python -I -B -X utf8 patch_montar_r35.py"""
import os
import sys
sys.dont_write_bytecode = True
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
P = AQUI / "montar_sandbox.py"
R34 = AQUI.parent / "R3_4" / "montar_sandbox.py"
raw = P.read_bytes()
assert raw == R34.read_bytes(), "o montar_sandbox de partida nao e, byte a byte, o da R3.4"
t = raw.decode("utf-8")
ORIG = AQUI / "_construcao" / "montar_sandbox_R3_4_original.py"
if not ORIG.exists():
    with open(ORIG, "xb") as f:
        f.write(raw)


def sub(velho, novo):
    global t
    assert t.count(velho) == 1, (velho[:90], t.count(velho))
    t = t.replace(velho, novo)


def cortar(ini, fim, novo):
    global t
    assert t.count(ini) == 1 and t.count(fim) == 1, (ini[:70], t.count(ini), fim[:70], t.count(fim))
    a, b = t.index(ini), t.index(fim)
    assert a < b
    t = t[:a] + novo + t[b:]


bloco_b1 = (AQUI / "_construcao" / "bloco_b1_r35.txt").read_text(encoding="utf-8")
bloco_394 = (AQUI / "_construcao" / "bloco_v394s_r35.txt").read_text(encoding="utf-8")
sub('"""montar_sandbox.py (R3.4, 19/10/2026) -- R3.4:',
    '"""montar_sandbox.py (R3.5, 19/10/2026) -- R3.5: o Nos REAL esta no meio do rito da v394 (um.py v394 instalado, selo v393): o "Nos real v393" do b1 vem da CUSTODIA (nos_real/, copia de bytes de '
    'cadeia_de_selo/v394/base_v393); b1real/ pina o caminho REAL (so a guarda A2); nos_v394s/ e b1v394s/ trazem o candidato REAL da v394 com selo sintetico. R3.4:')
sub('revisao="R3.4 (19/10/2026)", raiz=str(RAIZ), b1=[], b2=[], nos={}, nos_v392={}, fx={})',
    'revisao="R3.5 (19/10/2026)", raiz=str(RAIZ), b1=[], b1real=[], b1v394s=[], b2=[], nos={}, nos_real_standin={}, nos_v392={}, fx={})')
sub('for sub in ("b1", "b2", "nos", "nos_v392", "fx"):', 'for sub in ("b1", "b1real", "b1v394s", "b2", "nos", "nos_real", "nos_v394s", "nos_v392", "fx"):')
cortar("# b1: a copia que pina o Nos REAL. Na R3.3 era", 'for e in man_prod["code"] + [s for s in man_prod["sources"] if not Path(s["path"]).is_absolute()]:', bloco_b1)
sub('    rec["b1"].append(gravar_novo(RAIZ / "b1" / e["path"], raw))\n',
    '    rec["b1"].append(gravar_novo(RAIZ / "b1" / e["path"], raw))\n    rec["b1real"].append(gravar_novo(RAIZ / "b1real" / e["path"], raw))\n    rec["b1v394s"].append(gravar_novo(RAIZ / "b1v394s" / e["path"], raw))\n')
sub('(RAIZ / "b1" / "estado").mkdir()\n', '(RAIZ / "b1" / "estado").mkdir()\n(RAIZ / "b1real" / "estado").mkdir()\n')
sub('(RAIZ / "b2" / "estado").mkdir()\n', '(RAIZ / "b2" / "estado").mkdir()\n' + bloco_394)
sub('p = RAIZ / "SANDBOX_MANIFEST_R3_4.json"', 'p = RAIZ / "SANDBOX_MANIFEST_R3_5.json"')
tmp = P.with_name(P.name + ".tmp_r35")
with open(tmp, "xb") as f:
    f.write(t.encode("utf-8"))
os.replace(tmp, P)
print("ok", len(raw), "->", P.stat().st_size)
