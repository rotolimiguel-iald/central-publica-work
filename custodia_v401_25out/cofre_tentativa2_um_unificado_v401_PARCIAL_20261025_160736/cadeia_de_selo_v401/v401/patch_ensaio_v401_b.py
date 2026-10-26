# -*- coding: utf-8 -*-
"""patch_ensaio_v401_b.py -- LICAO DA v401 no ensaio: os dicts de verbatins das versoes anteriores sao COMPARTILHADOS com _V392_VERBATINS2 (`_V392_VERBATINS2.update(_V40x_VERBATINS2)` no um.py): adulterar o texto de `um._V392_VERBATINS2[k]["text"]` e restaurar
trocando a ENTRADA do mapa por uma copia deixava o objeto compartilhado ADULTERADO nos outros mapas (nas versoes anteriores nada lia o texto depois; na v401 o registro falsidade_da_inercia_v401 le _V401_VERBATINS2 e reprovava). Aqui o texto e' restaurado NO LUGAR, no mesmo objeto.
Substituicoes de contagem exata; recusa rodar duas vezes."""
import ast, sys
sys.stdout.reconfigure(encoding="utf-8")
P = sys.argv[1] if len(sys.argv) > 1 else "ensaio_a_seco_v401.py"
t = open(P, encoding="utf-8").read()
assert "# [v401-patch-b]" not in t


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:100], t.count(old), n)
    t = t.replace(old, new)


for mapa, var in (("_V397_VERBATINS2", "_ch"), ("_V398_VERBATINS2", "ch_"), ("_V392_VERBATINS2", "vch_"), ("_V401_VERBATINS2", "ch_")):
    ant = "_ant" if mapa != "_V392_VERBATINS2" else "ant_"
    sub('%s = dict(um.%s[%s]); um.%s[%s]["text"] += " "' % (ant, mapa, var, mapa, var), '%s = um.%s[%s]["text"]; um.%s[%s]["text"] += " "   # [v401-patch-b] restaurado NO LUGAR (o objeto e\' compartilhado com _V392_VERBATINS2)' % (ant, mapa, var, mapa, var))
    sub("um.%s[%s] = %s" % (mapa, var, ant), 'um.%s[%s]["text"] = %s' % (mapa, var, ant))
ast.parse(t)
open(P + ".tmp", "w", encoding="utf-8", newline="").write(t)
import os
os.replace(P + ".tmp", P)
print("patch b aplicado:", P)
