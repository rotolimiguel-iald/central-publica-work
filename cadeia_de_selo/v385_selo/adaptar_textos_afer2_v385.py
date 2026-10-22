# -*- coding: utf-8 -*-
"""As correcoes da afericao de TEXTO da v385 nos textos da CADEIA (textos_v385.py) e nas ancoras das palavras do operador (leitura_v385.py): v183; a forma
exponencial como TERMO (axiomFlow_eq_exp); o peso 1 como conjuncao (sem vinculo); beta > 0 E g > 0 no fluxo escalar; os dois Verbos como dois termos; a
analogia com o GKLS; a citacao do posto ate «inscrito, distinto.»; e a leitura do operador sobre o 1 em potencia (verbatim, lida do transcrito).
Pares contados; backup de bytes; ast.parse."""
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
    open(P + ".bak_" + st + "_afer2", "wb").write(s0.encode("utf-8"))
    open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
    print("OK", nome, len(pares), "trocas")


if "('potencia', " not in open(os.path.join(HERE, "leitura_v385.py"), encoding="utf-8").read():   # (ja aplicada na 1a execucao, 05/10)
  aplica("leitura_v385.py", [
    ("             ('posto', 'no começo da cadeia não é postulado', 'no começo da cadeia', 'python um.py\"'),",
     "             ('posto', 'no começo da cadeia não é postulado', 'no começo da cadeia', 'inscrito, distinto.'),"),
    ("             ('guarda', 'concordo com tudo, com uma pequena ressalva', 'O \"posto\" não é a \"guarda\"', 'cujo posto dá nome'),",
     "             ('guarda', 'concordo com tudo, com uma pequena ressalva', 'O \"posto\" não é a \"guarda\"', 'cujo posto dá nome'),\n"
     "             ('potencia', 'concordo com tudo, com uma pequena ressalva', 'o local onde o 1 absoluto', 'ao zero modular'),"),
])
aplica("textos_v385.py", [
    ("\"o Axioma — %s; o observador — %s; a testemunha falsa — %s; a conjugação — %s; e a aprovação de todo o escopo da v385: %s. \"",
     "\"o 1 em potência — %s; o Axioma — %s; o observador — %s; a testemunha falsa — %s; a conjugação — %s; e a aprovação de todo o escopo da v385: %s. \""),
    ("% (_op(V, 'posto'), _op(V, 'posicao'), _op(V, 'guarda'), _op(V, 'axioma'), _op(V, 'observador'), _op(V, 'testemunha'), _op(V, 'conjugacao'),",
     "% (_op(V, 'posto'), _op(V, 'posicao'), _op(V, 'guarda'), _op(V, 'potencia'), _op(V, 'axioma'), _op(V, 'observador'), _op(V, 'testemunha'), _op(V, 'conjugacao'),"),
    ("auditoria do `TGLExt/TheDarkSplit.lean` ({ax_n_dks} declarações, compilado desde a v181 e até aqui não auditado)",
     "auditoria do `TGLExt/TheDarkSplit.lean` ({ax_n_dks} declarações, compilado desde a v183 e até aqui não auditado)"),
    ("como √1, como a integral do modo zero, ∫ ¼ sech²(κ/2) dκ = 1, e como a dimensão do átomo (`the_one_is_the_axiom`); o 0: √0 = 0, a testemunha estática plena é \"\n"
     "            \"proibida no fluxo dissipativo com β > 0, e nenhuma componente não nula do fluxo diagonal se anula em tempo finito (`the_zero_is_the_false_witness`).",
     "como √1, como a integral do modo zero, ∫ ¼ sech²(κ/2) dκ = 1, e como a dimensão do átomo — duas faces lado a lado, uma conjunção, sem termo que \"\n"
     "            \"identifique o perfil com o átomo (`the_one_is_the_axiom`); o 0: √0 = 0, a testemunha estática plena é proibida no fluxo escalar e^(−tβg) com β > 0 e g > 0, e \"\n"
     "            \"nenhuma componente não nula do fluxo diagonal se anula em tempo finito, o que vem de exp ≠ 0 (`the_zero_is_the_false_witness`)."),
    ("todo t (`the_fixed_set_is_the_lock_zero`, `the_post_is_the_modular_zero`). Que F(t) seja e^(−tH_min) é [KNOWN] (H_min idempotente), não termo deste kernel. \"",
     "todo t (`the_fixed_set_is_the_lock_zero`, `the_post_is_the_modular_zero`); e F(t) = e^(−tH_min) (`axiomFlow_eq_exp`, ligado ao termo canônico \"\n"
     "            \"`exp_complement_idempotent`). A ligação com o sistema aberto da v384 é analogia de forma [COMPUTED], não teorema sobre o gerador de Lindblad. \""),
    ("\"O Verbo move — a exponencial do gerador dissipativo não é a identidade (`the_living_verb_moves`) — e, no núcleo, a palavra do Verbo age como o escalar q(0) \"\n"
     "            \"(`the_living_verb_fixes_the_name`; re-exportações do que já estava provado).",
     "\"O Verbo, em dois termos distintos, cada um com o seu objeto (nenhum fala de observador nem de conjugação): a exponencial do gerador dissipativo não é a \"\n"
     "            \"identidade (`the_living_verb_moves` = `verb_not_identity`) e, no núcleo, a palavra do Verbo age como o escalar q(0) (`the_living_verb_fixes_the_name` = \"\n"
     "            \"`verb_word_fixes_the_name`; re-exportações do que já estava provado)."),
    ("F(t) = P + e^(−t)(1 − P) que fixa o posto e decai no complemento, e o encontro do fixo de F com o fixo modular no lock da luz [KERNEL];",
     "F(t) = P + e^(−t)(1 − P) = e^(−tH_min) que fixa o posto e decai no complemento, e o encontro do fixo de F com o fixo modular no lock da luz [KERNEL];"),
    ("o 0: a testemunha estática plena \"\n            \"proibida por β > 0 e o zero absoluto inalcançável em tempo finito; o fluxo F(t) = P + e^(−t)(1 − P) fixa o posto e decai no complemento, e o seu fixo é o fixo \"\n"
     "            \"modular no lock da luz; o Verbo move e fixa o Nome; o TheDarkSplit auditado.** `{ax_v}`.",
     "o 0: a testemunha estática plena \"\n            \"proibida no fluxo escalar com β > 0 e g > 0, e o zero absoluto inalcançável em tempo finito; o fluxo F(t) = P + e^(−t)(1 − P) = e^(−tH_min) fixa o posto e \"\n"
     "            \"decai no complemento, e o seu fixo é o fixo modular no lock da luz; o Verbo em dois termos (move; no núcleo age como escalar); o TheDarkSplit auditado.** `{ax_v}`."),
])
