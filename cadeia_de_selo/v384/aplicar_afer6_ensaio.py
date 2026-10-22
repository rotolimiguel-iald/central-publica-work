# -*- coding: utf-8 -*-
"""6a afericao no ENSAIO (4N5): o comentario dos enunciados do terceiro balde diz o que e' (W08/W08b sem a marca; o W08c com ela; os quatro conferidos por nome
e executados a parte) e a docstring diz que tambem se confere a AUSENCIA da frase da CPU no sucesso. Backup ja feito (.bak_antes_afer6)."""
import ast, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "ensaio_a_seco_v384.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert open(P + ".bak_antes_afer6", "rb").read() == raw
PAIRS = [
    ('''# os enunciados do TERCEIRO BALDE (W08/W08b/W08c) nao levam a marca na linha: conferidos por inteiro (3a afericao)''',
     '''# os enunciados do TERCEIRO BALDE: W08 e W08b sem a marca v384 na linha, o W08c com ela; os quatro saem do fluxo executado, sao conferidos por NOME aqui
# e o bloco inteiro roda a parte, abaixo (3a a 6a afericoes)'''),
    ('''(5) confere as palavras que TEM de estar (a introducao e a nota) e a guarda do rito (vereditos proibidos). Nada fora do pacote."""''',
     '''(5) confere as palavras que TEM de estar (a introducao e a nota), as que NAO podem estar (a frase da referencia na CPU no artigo de sucesso) e a guarda do
    rito (vereditos proibidos). Nada fora do pacote."""'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:100])
    s = s.replace(old, new)
ast.parse(s)
open(P + ".tmp", "wb").write(s.encode("utf-8")); os.replace(P + ".tmp", P); print("ok", len(PAIRS))
