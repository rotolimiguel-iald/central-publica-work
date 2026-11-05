# -*- coding: utf-8 -*-
"""_adapt_ensaio_d408_v408.py -- os TITULOS tipados do ensaio (D408/D408E, o oraculo independente da secao v408 do artigo) acompanham a correcao de citacao dos snippets (04/11/2026, claude-construtor-v408):
o cabecalho da regra deixa as aspas « » (a regra «provar ou podar» e' nome da gerencia, nao fala do operador) e o cabecalho «P=nP» escreve o nome como o operador escreveu. Backup de bytes; contagem EXATA. Escrito pela ferramenta Write (o heredoc do Bash colapsa barras)."""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "ensaio_a_seco_v408.py")
raw = open(P, "rb").read(); open(P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_D408", "wb").write(raw)
t = raw.decode("utf-8")


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:100], t.count(old), n); t = t.replace(old, new)


sub('"O que o operador identificou e foi provado (regra «provar ou podar»):", "Erratas em nome próprio (E22).", "O tempo é a moeda de $\\\\beta$.", "O ponto de contradição.", "«P = nP».",',
    '"O que o operador identificou e foi provado (a regra provar ou podar, nome que a gerência deu à fala acima):", "Erratas em nome próprio (E22).", "O tempo é a moeda de $\\\\beta$.", "O ponto de contradição.", "«P=nP».",')
sub('"What the operator identified and was proved (the ``prove or prune\'\' rule):", "Errata in its own name (E22).", "Time is the currency of $\\\\beta$.", "The point of contradiction.", "``P = nP\'\'.",',
    '"What the operator identified and was proved (the prove or prune rule, the management\'s name for the saying above):", "Errata in its own name (E22).", "Time is the currency of $\\\\beta$.", "The point of contradiction.", "P = nP.",')
for l_ in ("pt", "en"):
    sn_ = open(os.path.join(HERE, "artigo_%s_v408.pysnip" % l_), encoding="utf-8").read()
    for cab_ in (("O que o operador identificou e foi provado (a regra provar ou podar, nome que a gerência deu à fala acima):", "«P=nP».") if l_ == "pt" else ("What the operator identified and was proved (the prove or prune rule, the management's name for the saying above):", "P = nP.")):
        assert cab_ in sn_, ("o titulo tipado nao esta no snippet", l_, cab_)
ast.parse(t); open(P, "wb").write(t.encode("utf-8")); print("ok ensaio D408/D408E", len(raw), "->", len(t.encode("utf-8")))
