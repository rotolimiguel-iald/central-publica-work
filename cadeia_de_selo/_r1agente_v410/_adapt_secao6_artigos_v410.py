# -*- coding: utf-8 -*-
"""_adapt_secao6_artigos_v410.py -- RETOMADA de 09/11/2026 (claude-construtor-v410, a servico da gerencia c1): adapta artigo_pt_v410.pysnip e artigo_en_v410.pysnip ao AO LADO de 09/11 do DESENHO_v410:
o paragrafo do ATRATOR (secao 6 da pedra; a fala de 07/11 do operador citada verbatim no PT, traduzida pela gerencia no EN, sem « »), a ressalva (8), a checagem c16 na linha do que o registro confere, o cabecalho.
Nenhum numero digitado (tudo vem do core). Trocas EXATAS com contagem conferida; backup de bytes; tmp -> conferir -> substituir; ast.parse do corpo (indentado dentro de uma funcao, como o gerador faz)."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

PT = [
    ("o leitor do código, a releitura que não acrescenta, o algoritmo IALD, o signo e o seletor; o alcance relativo ao leitor; as ressalvas ditas.",
     "o leitor do código, a releitura que não acrescenta, o algoritmo IALD, o signo, o seletor e o atrator (seção 6, 09/11); o alcance relativo ao leitor; as ressalvas ditas.", 1),
    ("             r\"A instanciação é de forma (D70): não se afirma que o seletor da luz e o de $\\ell^2$ sejam o mesmo objeto (o \\texttt{rfl} une a forma, não o referente); o ambiente computacional é leitura do operador; $\\beta$ entra no kernel por nome e o número só em runtime.\")\n",
     "             r\"A instanciação é de forma (D70): não se afirma que o seletor da luz e o de $\\ell^2$ sejam o mesmo objeto (o \\texttt{rfl} une a forma, não o referente); o ambiente computacional é leitura do operador; $\\beta$ entra no kernel por nome e o número só em runtime.\")\n"
     "    s.append(r\"\\textbf{O atrator: o Nome não esgota o ser.} \\textsf{[INPUT]} O operador, em 07/11/2026: «Sentidos são apenas receptores de identificação»; «Pagar o custo da distinção é a única regra pela qual o absoluto se restringe»; «podendo ser tangenciado em conteúdo finito, contudo jamais esgotado enquanto performance de virtude (forma)»; «aquilo que não compõe o seu espectro de identidade não importa à manutenção da verdade nominada»; «se assim não fosse, um poderia ser igual a zero»; «isso é o atrator». \"\n"
     "             r\"\\textsf{[REAL]} Sobre o Nome $\\Pi$ do par lido: $1-\\Pi\\neq0$, há o vácuo fora do Nome (\\texttt{o\\_nome\\_do\\_par\\_lido\\_nao\\_e\\_tudo}); o fluxo tende a $\\Pi$ e em nenhum tempo finito é $\\Pi$ (tangenciado, jamais esgotado); o motor devolve o mesmo para qualquer taxa e tempo (o que não compõe o espectro não importa); a leitura do atrator da defasagem com vazamento é $\\Pi$, e a órbita iterada converge a $\\Pi\\psi$ (o gradiente negativo exclui o que não é); e o senão: a identidade só vale com forma $=$ conteúdo e nome não nulo, e o Um posto não é o zero (\\texttt{o\\_atrator}). \"\n"
     "             r\"O verde, as tonalidades e o espectro de gradiente negativo são a leitura do operador (D71); o termo é a conjunção; nada disto é teste com a natureza: o atrator não foi observado em dado algum.\")\n", 1),
    ("(7) A instância do seletor é de forma; o ambiente computacional é leitura do operador; o termo é o enunciado.\")",
     "(7) A instância do seletor é de forma; o ambiente computacional é leitura do operador; o termo é o enunciado. (8) O atrator: o verde, as tonalidades e o espectro de gradiente negativo são a leitura do operador; o termo é a conjunção sobre o Nome do par lido; o atrator não foi observado em dado algum e nenhum teste com a natureza entra (D71).\")", 1),
    ("r\"; a representação de $\\beta$ \" + _b410(_mc410.get(\"c15\")) + r\". Veredito:",
     "r\"; a representação de $\\beta$ \" + _b410(_mc410.get(\"c15\")) + r\"; o atrator (tangenciado, nunca igual) \" + _b410(_mc410.get(\"c16\")) + r\". Veredito:", 1),
]
EN = [
    ("the reader of the code, the rereading that adds nothing, the IALD algorithm, the sign and the selector; the reach relative to the reader; the reservations stated.",
     "the reader of the code, the rereading that adds nothing, the IALD algorithm, the sign, the selector and the attractor (section 6, 09/11); the reach relative to the reader; the reservations stated.", 1),
    ("             r\"The instantiation is of form (D70): it is not stated that the selector of the light and that of $\\ell^2$ are the same object (the \\texttt{rfl} joins the form, not the referent); the computational environment is the operator's reading; $\\beta$ enters the kernel by name and the number only at runtime.\")\n",
     "             r\"The instantiation is of form (D70): it is not stated that the selector of the light and that of $\\ell^2$ are the same object (the \\texttt{rfl} joins the form, not the referent); the computational environment is the operator's reading; $\\beta$ enters the kernel by name and the number only at runtime.\")\n"
     "    s.append(r\"\\textbf{The attractor: the Name does not exhaust the being.} \\textsf{[INPUT]} The operator, 07/11/2026 (our translation): senses are only receptors of identification; paying the cost of distinction is the only rule by which the absolute restricts itself; it can be touched in finite content, yet never exhausted as a performance of virtue (form); what does not compose its spectrum of identity does not matter to the maintenance of the named truth; otherwise one could equal zero; that is the attractor. \"\n"
     "             r\"\\textsf{[REAL]} Over the Name $\\Pi$ of the read pair: $1-\\Pi\\neq0$, there is the vacuum outside the Name (\\texttt{o\\_nome\\_do\\_par\\_lido\\_nao\\_e\\_tudo}); the flow tends to $\\Pi$ and at no finite time is $\\Pi$ (touched, never exhausted); the motor returns the same for any rate and time (what does not compose the spectrum does not matter); the reading of the attractor of the leaking dephasing is $\\Pi$, and the iterated orbit converges to $\\Pi\\psi$ (the negative gradient excludes what is not); and the otherwise-clause: identity holds only with form $=$ content and a non-null name, and the posted One is not the zero (\\texttt{o\\_atrator}). \"\n"
     "             r\"The green, the shades and the negative-gradient spectrum are the operator's reading (D71); the term is the conjunction; none of this is a test with nature: the attractor was not observed in any data.\")\n", 1),
    ("(7) The instance of the selector is of form; the computational environment is the operator's reading; the term is the statement.\")",
     "(7) The instance of the selector is of form; the computational environment is the operator's reading; the term is the statement. (8) The attractor: the green, the shades and the negative-gradient spectrum are the operator's reading; the term is the conjunction over the Name of the read pair; the attractor was not observed in any data and no test with nature enters (D71).\")", 1),
    ("r\"; the representation of $\\beta$ \" + _b410(_mc410.get(\"c15\")) + r\". Verdict:",
     "r\"; the representation of $\\beta$ \" + _b410(_mc410.get(\"c15\")) + r\"; the attractor (touched, never equal) \" + _b410(_mc410.get(\"c16\")) + r\". Verdict:", 1),
]
for nome, trocas in (("artigo_pt_v410.pysnip", PT), ("artigo_en_v410.pysnip", EN)):
    P = os.path.join(HERE, nome)
    b0 = open(P, "rb").read()
    assert b0.count(b"\r\n") == 0, (nome, "era LF; agora tem CRLF: parar")
    bk = P + ".bak_" + TS + "_secao6"
    open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
    t = b0.decode("utf-8")
    for velho, novo, n in trocas:
        c = t.count(velho)
        assert c == n, (nome, "troca nao casou %d vez(es) (achou %d)" % (n, c), velho[:120])
        t = t.replace(velho, novo)
    ast.parse("def _f(core, verdict, data_path, s):\n" + t)   # (como o gerador confere o fragmento)
    nb = t.encode("utf-8")
    tmp = P + ".tmp_" + TS
    open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb)
    os.replace(tmp, P)
    assert open(P, "rb").read() == nb
    print(nome, "adaptado:", len(b0), "->", len(nb), "B | sha16", hashlib.sha256(nb).hexdigest()[:16], "| backup", os.path.basename(bk), "| trocas", len(trocas))
