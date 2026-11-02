# -*- coding: utf-8 -*-
"""aplicar_R6c_v405.py -- o relatorio alcanca a R6 (uso unico; nao toca nada que entre no candidato).
Backup de BYTES (.bak_<ts>_R6c); temporario -> conferir -> os.replace; cada ancora exatamente 1x."""
import os, time

HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")
p = os.path.join(HERE, "gerar_relatorio_v405.py")
b = open(p, "rb").read()
s = b.decode("utf-8")
SUBS = [
    ("## 1b. As erratas R2 e R3 (a revisão de terceiro não aprovou `a30f9f0ebf90c277`)", "## 1b. As erratas R2 a R6 (a revisão de terceiro não aprovou `a30f9f0ebf90c277`)"),
    ("«as leituras da cadeia da massa», dez itens, lista declarada não fechada", "«as leituras da cadeia da massa», catorze itens hoje, lista declarada não fechada"),
    ("| R3: a frase do no-go | a escala absoluta segue livre e o no-go não cai; a relativa está pinada; sobra a transposição do acorde inteiro;", "| R3: a frase do no-go | o valor absoluto segue livre e o no-go não cai; o valor relativo à tônica está pinado; sobra a transposição do acorde inteiro;"),
    ('NAO_REVISADO = "este candidato (errata R2) NAO foi revisado por terceiro:', 'NAO_REVISADO = "este candidato (erratas R2 a R6) NAO foi revisado por terceiro:'),
    ('''    "nenhum nome do contrato com o orquestrador divergiu",
''', '''    "o recibo R6 repete as entradas do R5 (com o sha256_antes do R5): o pino e o p00 leem a pedra mudada na R6 por depois diferente do R5, e a cadeia R6 -> R5 -> R4 -> R3 -> R2 fecha assim",
    "a reclassificacao do Grande Atrator diz a escala do setor; nos textos novos desta preparacao se le o valor absoluto do setor, pela regra da mensagem da gerencia de 19:03; o documento dela fica como esta",
    "nenhum nome do contrato com o orquestrador divergiu",
'''),
]
for a, c in SUBS:
    n = s.count(a)
    assert n == 1, (n, a[:100])
    s = s.replace(a, c)
open(p + ".bak_" + TS + "_R6c", "wb").write(b)
t = p + ".tmp_R6c"
open(t, "wb").write(s.encode("utf-8"))
assert open(t, "rb").read() == s.encode("utf-8")
os.replace(t, p)
print("ok gerar_relatorio_v405.py", len(SUBS), TS)
