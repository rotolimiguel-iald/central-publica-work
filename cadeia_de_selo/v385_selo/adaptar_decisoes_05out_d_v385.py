# -*- coding: utf-8 -*-
"""A CORRECAO do operador de 05/10 14:35 (a forma falsa = qualquer conteudo menos o do posto) na cadeia da v385: a leitura ganha o verbatim 'forma_falsa';
os textos o poem no diario; o handoff diz que a leitura (b) da gerencia foi retratada e que a leitura refeita esta ao lado. Pares contados; backup de bytes."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
st = time.strftime("%Y%m%d_%H%M%S")


def aplica(nome, pares):
    P = os.path.join(HERE, nome)
    s0 = open(P, encoding="utf-8", newline="").read(); s = s0
    for a, b in pares:
        n = s.count(a)
        assert n == 1, (nome, "a troca nao e unica", n, a[:100])
        s = s.replace(a, b)
    ast.parse(s)
    open(P + ".bak_" + st + "_dec05d", "wb").write(s0.encode("utf-8"))
    open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
    print("OK", nome, len(pares), "trocas")


aplica("leitura_v385.py", [
    ("             ('tornar', 'Concordo como nome sugerido para a subpasta', 'Vou explicar o que eu quis dizer', None))   # a linha INTEIRA, com a pergunta final (nenhum corte sem marca)",
     "             ('tornar', 'Concordo como nome sugerido para a subpasta', 'Vou explicar o que eu quis dizer', None),   # a linha INTEIRA, com a pergunta final (nenhum corte sem marca)\n"
     "             ('forma_falsa', 'tem uma coisa errada no que vc prop', 'tem uma coisa errada', None))   # 05/10 14:35: a correcao -- a forma falsa tem qualquer conteudo menos o do posto"),
])
aplica("textos_v385.py", [
    ("            \"«tornou-se Posto» (v365) × «não se ascende ao posto» — %s. \"\n",
     "            \"«tornou-se Posto» (v365) × «não se ascende ao posto» — %s. E a correção da leitura da gerência sobre a forma falsa — %s (a leitura (b) da gerência, \"\n"
     "            \"«a forma falsa = o ponto fixo 0», fica retratada: a forma falsa é o complemento do posto, 1 − P; ver [[um-posto-jamais-pressuposto-e-h2-17set]]). \"\n"),
    ("_op(V, 'nome_axioma'), _op(V, 'subpasta'), _op(V, 'v1_espelho'), _op(V, 'tornar')))",
     "_op(V, 'nome_axioma'), _op(V, 'subpasta'), _op(V, 'v1_espelho'), _op(V, 'tornar'), _op(V, 'forma_falsa')))"),
])
aplica("handoff_v385.py", [
    ('for _n in ("custodia", "espelho", "nome_axioma", "prossiga", "posto", "subpasta", "v1_espelho", "tornar"):',
     'for _n in ("custodia", "espelho", "nome_axioma", "prossiga", "posto", "subpasta", "v1_espelho", "tornar", "forma_falsa"):'),
    ("COM ERRATA AO LADO — três frases dela não têm termo na pedra —, a ratificar: pendência 4).",
     "COM ERRATA AO LADO — três frases dela não têm termo na pedra — e com a CORREÇÃO do operador das 14:35: %(op_forma_falsa)s — a leitura (b) da gerência fica retratada: a forma falsa é o complemento do posto, 1 − P; a leitura refeita está ao lado, [ONTO], a ratificar: pendência 4)."),
])
