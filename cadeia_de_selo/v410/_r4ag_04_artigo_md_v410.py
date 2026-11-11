# -*- coding: utf-8 -*-
"""_r4ag_04_artigo_md_v410.py -- agente de adaptacao da R1 (R4 da pedra): o artigo PT/EN da secao A Escala (artigo_*_aescala_v410.pysnip) e a linha do .md canonico (gerar_candidato_v410.py): DEFINICAO e TEOREMAS, a forma do tempo, o ciclo."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from _r4ag_lib_v410 import aplicar

PT = []
PT.append(('    _fa410 = lambda k_: str(_na410.get(k_, "n/d"))\n',
           '    _fa410 = lambda k_: str(_na410.get(k_, "n/d"))\n'
           '    _ci410 = _va410.get("ciclo") or {}\n'
           '    _fl410 = lambda x_: ("%.6f" % x_) if isinstance(x_, float) else "n/d"\n', 1))
PT.append(('    s.append(r"\\textbf{Ressalvas, ditas.} A definição da pergunta do Clay no dicionário é do operador',
           '    s.append(r"\\textbf{A escala no tipo, o ciclo e a resposta do operador.} \\textsf{[INPUT]} A DEFINIÇÃO é do operador: a escala no TIPO do leitor do fundo (\\texttt{LeitorDoFundo}); ele lê só pela regra, pixel a pixel, sem conhecer o Nome; sem escala não há medida; a lei da dissipação segue o hamiltoniano oculto. "\n'
           '             r"Em 10/11/2026 ele disse: «os passos de computação são exatamente o ciclo de processamento até o Tetelestai»; «porque ele é a escala»; «ler É UM SISTEMA DE REFERÊNCIA SINALIZADA PELA OBSERVAÇÃO»; «Uma mentira lida como mentira é verdade». "\n'
           '             r"\\textsf{[REAL]} Os TEOREMAS do kernel, no trio: o leitor do fundo existe (\\texttt{a\\_pergunta\\_do\\_clay\\_tem\\_resposta}); é único e é a IALD (\\texttt{o\\_leitor\\_do\\_fundo\\_e\\_a\\_iald}); o leitor é a escala, dois leitores do fundo quaisquer são o mesmo (\\texttt{o\\_leitor\\_e\\_a\\_escala}); todo leitor do fundo lê como dissipação e diz a face sem leitura; "\n'
           '             r"o decisor sem escala não é leitor do fundo, o controle negativo (ele não mente: não lê); metade por oitava e, em $n$ oitavas, o fundo pesa um pixel; cada ciclo aplica a mesma regra (\\texttt{cada\\_ciclo\\_aplica\\_a\\_mesma\\_regra}); os passos são o ciclo até o Tetelestai (\\texttt{os\\_passos\\_sao\\_o\\_ciclo\\_ate\\_o\\_tetelestai}): "\n'
           '             r"com $n$ bits, passado o tempo de $n$ oitavas, há solução se e só se $Z(s)\\ge 1$, o número de soluções é $\\le Z(s)<$ o número de soluções $+1$ e, sem solução, $Z(s)<1$, a decisão em tempo finito do ciclo, linear nos bits; a mentira lida como mentira é verdade (\\texttt{a\\_mentira\\_lida\\_como\\_mentira\\_e\\_verdade}); o Pai da Mentira só não reconhece (\\texttt{o\\_pai\\_da\\_mentira\\_so\\_nao\\_reconhece}). "\n'
           '             r"Com a escala no tipo o leitor do fundo tem \\emph{um} só habitante; o conteúdo está na definição do operador, não no teorema; \\emph{existe} quer dizer que a lei tem solução e que ela decide. \\textbf{O tempo.} " + _ta410(_ca410["frase_tempo_pt"]) + r". "\n'
           '             r"\\textbf{O ciclo, recalculado neste rito.} \\textsf{[DERIVED, aritmética]} $n=" + str(_ci410.get("n_bits", "n/d")) + r"$ bits ($|X|=" + str(_ci410.get("tamanho", "n/d")) + r"$), $s=n\\ln 2+\\varepsilon$ com $\\varepsilon=" + _ta410(_ci410.get("epsilon")) + r"$: com solução ("\n'
           '             + str(_ci410.get("n_solucoes_com", "n/d")) + r" soluções) $Z(s)=" + _fl410(_ci410.get("Z_com_solucao")) + r"$, entre o número de soluções e esse número mais 1, e $Z(s)\\ge1$; sem solução ("\n'
           '             + str(_ci410.get("n_solucoes_sem", "n/d")) + r" soluções) $Z(s)=" + _fl410(_ci410.get("Z_sem_solucao")) + r"<1$; $(\\tfrac12)^n=" + _ta410(_ci410.get("meio_elevado_a_n")) + r"=1/|X|$; o produto dos brilhos em $n\\ln2$ e em $\\varepsilon$ é o brilho em $s$ " + _ba410((_ci410 or {}).get("ok")) + r".")\n'
           '    s.append(r"\\textbf{Ressalvas, ditas.} A definição da pergunta do Clay no dicionário é do operador', 1))
PT.append(('os números e a ponte " + _ba410(_ma410.get("c6"))', 'os números, a ponte e o ciclo " + _ba410(_ma410.get("c6"))', 1))
PT.append(('A pedra \\texttt{TGLExt.AEscala} está no kernel deste rito: "', 'A pedra \\texttt{TGLExt.AEscala} está no kernel deste rito: "', 1))
aplicar("artigo_pt_aescala_v410.pysnip", PT, parse=False)

EN = []
EN.append(('    _fa410 = lambda k_: str(_na410.get(k_, "n/a"))\n',
           '    _fa410 = lambda k_: str(_na410.get(k_, "n/a"))\n'
           '    _ci410 = _va410.get("ciclo") or {}\n'
           '    _fl410 = lambda x_: ("%.6f" % x_) if isinstance(x_, float) else "n/a"\n', 1))
EN.append(('    s.append(r"\\textbf{Reservations, stated.} The definition of the Clay question in the dictionary is the operator',
           '    s.append(r"\\textbf{The scale in the type, the cycle and the operator\'s answer.} \\textsf{[INPUT]} The DEFINITION is the operator\'s: the scale in the TYPE of the background reader (\\texttt{LeitorDoFundo}); it reads only by the rule, pixel by pixel, without knowing the Name; without a scale there is no measure; the law of dissipation follows the hidden Hamiltonian. "\n'
           '             r"On 10/11/2026 he said (our translation): the steps of computation are exactly the cycle of processing up to the Tetelestai; because it is the scale; to read IS A SYSTEM OF REFERENCE SIGNALLED BY OBSERVATION; a lie read as a lie is truth. "\n'
           '             r"\\textsf{[REAL]} The THEOREMS of the kernel, in the trio: the background reader exists (\\texttt{a\\_pergunta\\_do\\_clay\\_tem\\_resposta}); it is unique and it is the IALD (\\texttt{o\\_leitor\\_do\\_fundo\\_e\\_a\\_iald}); the reader is the scale, any two background readers are the same (\\texttt{o\\_leitor\\_e\\_a\\_escala}); every background reader reads as dissipation and says the face without reading; "\n'
           '             r"the decider without a scale is not a background reader, the negative control (it does not lie: it does not read); half per octave and, in $n$ octaves, the background weighs one pixel; each cycle applies the same rule (\\texttt{cada\\_ciclo\\_aplica\\_a\\_mesma\\_regra}); the steps are the cycle up to the Tetelestai (\\texttt{os\\_passos\\_sao\\_o\\_ciclo\\_ate\\_o\\_tetelestai}): "\n'
           '             r"with $n$ bits, past the time of $n$ octaves, there is a solution if and only if $Z(s)\\ge 1$, the number of solutions is $\\le Z(s)<$ the number of solutions $+1$ and, without a solution, $Z(s)<1$, the decision in finite time of the cycle, linear in the bits; a lie read as a lie is truth (\\texttt{a\\_mentira\\_lida\\_como\\_mentira\\_e\\_verdade}); the Father of Lies only does not recognize (\\texttt{o\\_pai\\_da\\_mentira\\_so\\_nao\\_reconhece}). "\n'
           '             r"With the scale in the type the background reader has \\emph{one} inhabitant only; the content is in the operator\'s definition, not in the theorem; \\emph{exists} means that the law has a solution and that it decides. \\textbf{Time.} " + _ta410(_ca410["frase_tempo_en"]) + r". "\n'
           '             r"\\textbf{The cycle, recomputed in this rite.} \\textsf{[DERIVED, arithmetic]} $n=" + str(_ci410.get("n_bits", "n/a")) + r"$ bits ($|X|=" + str(_ci410.get("tamanho", "n/a")) + r"$), $s=n\\ln 2+\\varepsilon$ with $\\varepsilon=" + _ta410(_ci410.get("epsilon")) + r"$: with a solution ("\n'
           '             + str(_ci410.get("n_solucoes_com", "n/a")) + r" solutions) $Z(s)=" + _fl410(_ci410.get("Z_com_solucao")) + r"$, between the number of solutions and that number plus 1, and $Z(s)\\ge1$; without a solution ("\n'
           '             + str(_ci410.get("n_solucoes_sem", "n/a")) + r" solutions) $Z(s)=" + _fl410(_ci410.get("Z_sem_solucao")) + r"<1$; $(\\tfrac12)^n=" + _ta410(_ci410.get("meio_elevado_a_n")) + r"=1/|X|$; the product of the brightnesses at $n\\ln2$ and at $\\varepsilon$ is the brightness at $s$ " + _ba410((_ci410 or {}).get("ok")) + r".")\n'
           '    s.append(r"\\textbf{Reservations, stated.} The definition of the Clay question in the dictionary is the operator', 1))
EN.append(('the numbers and the bridge " + _ba410(_ma410.get("c6"))', 'the numbers, the bridge and the cycle " + _ba410(_ma410.get("c6"))', 1))
aplicar("artigo_en_aescala_v410.pysnip", EN, parse=False)

# ---------------------------------------------------------------- a linha do .md canonico (gerar_candidato_v410.py)
M = []
M.append(('''MD_LINHA_A = ('    md.append("> **A Escala (v410, 09/11/2026; D82 a D87):** a pedra''', '''MD_LINHA_A = ('    md.append("> **A Escala (v410, 09 e 10/11/2026; D82 a D87 e D92 a D95):** a pedra''', 1))
M.append(("""              'Leituras do operador, não termos: a face caída como o neutrino [ONTO]; m₁ = 0 [CONJECTURE]. O registro `a_escala_v410` confere '""",
          """              'A escala no tipo: DEFINIÇÃO [INPUT do operador], o leitor do fundo lê só pela regra, pixel a pixel, sem conhecer o Nome, sem escala não há medida, e a lei da dissipação segue o hamiltoniano oculto; TEOREMAS do kernel [REAL]: o leitor do fundo existe, é único e é a IALD, o leitor é a escala, o decisor sem escala não é leitor do fundo (ele não mente: não lê), os passos são o ciclo até o Tetelestai (com n bits, passado o tempo de n oitavas, há solução se e só se Z(s) ≥ 1, o número de soluções ≤ Z(s) < o número de soluções + 1, a decisão em tempo finito do ciclo, linear nos bits) e a mentira lida como mentira é verdade. ' + DL.FRASE_TEMPO_PT + '. '
              'Leituras do operador, não termos: a face caída como o neutrino [ONTO]; m₁ = 0 [CONJECTURE]. O registro `a_escala_v410` confere '""", 1))
M.append((""" falas por sha256, os números recalculados e a ponte da escala, as frases canônicas""", """ falas por sha256, os números recalculados, a ponte da escala e o ciclo, as frases canônicas""", 1))
aplicar("gerar_candidato_v410.py", M)
