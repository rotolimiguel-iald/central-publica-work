# -*- coding: utf-8 -*-
"""ajuste unico (v401, 25/10): o artigo (PT/EN) ganha o paragrafo «A cadeia derivada» [DERIVED] (a extensao da pedra) com a hipotese NOMEADA H_tau [OPEN] e a ORDEM 025 como pendencia externa; as citacoes sao verbatim da sexta inscricao."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
ORDEM025 = "3fd2b5a801071343"
ANC = '    _b401 = _fv401.get("beta")\n'


def edita(p, bloco):
    t = open(p, encoding="utf-8", newline="").read()
    assert "cadeia derivada" not in t.lower() and "derived chain" not in t.lower()
    assert t.count(ANC) == 1
    t = t.replace(ANC, bloco + ANC)
    open(p, "w", encoding="utf-8", newline="").write(t)
    print("ok", p)


PT = '''    s.append(r"\\textbf{A cadeia derivada.} \\textsf{[DERIVED]} O operador pediu que a leitura não fosse sua [ONTO] e sim derivada: «eu não queria que a leitura fosse ONTO minha, quero que seja derivado», para o enunciado «a gravitação universal e a inércia não existem antes da posição impressa do Um absoluto». A pedra foi estendida e o kernel agora prova, a partir do axioma $\\omega(I)=1$ e da lei de escala de Takesaki (\\textsf{[KNOWN]}, campo da estrutura): "
             r"(i) \\texttt{no\\_post\\_before\\_the\\_impression}: todo peso positivo é movido por toda escala não trivial, e o peso $1$ só ocorre no corte $a=0$ (a impressão); (ii) \\texttt{inertia\\_is\\_not\\_its\\_own\\_cause}: o que fosse fixo desde sempre (em toda escala negativa), ou em toda escala positiva, pesa zero, e todo estado de peso positivo se move em alguma escala; "
             r"(iii) \\texttt{the\\_first\\_motion\\_is\\_the\\_impression}: «o primeiro movimento é a impressão do posto absoluto ocupado por 1»; (iv) \\texttt{the\\_zero\\_is\\_the\\_consequence\\_of\\_the\\_pruning} e \\texttt{leak\\_below\\_every\\_epsilon}: o zero não é estado da órbita, é o ínfimo da poda (a queda sem fundo, \\texttt{abismo}), e o vazamento $e^{-t\\beta g}$ fica abaixo de todo $\\varepsilon>0$; "
             r"(v) \\texttt{the\\_tension\\_is\\_projected\\_onto\\_the\\_attractor} e \\texttt{diagFlow\\_coordinate\\_is\\_the\\_scaling}: o fluxo diagonal do Grande Atrator é a escala dual, a coordenada com gap vai a zero no limite, é diferente de zero em tempo finito e a sem gap é o equilíbrio; a composição é \\texttt{falsidade\\_da\\_inercia\\_derivada}. "
             r"Neste rito: o menor peso do posto na grade é " + _f401(_fv401.get("min_weight_on_the_grid_positive"), 6) + r" ($>0$), e a coordenada com gap, depois de $t=10^9/\\beta$, vale em módulo " + (_f401(max(_fv401.get("diag_flow_gap_pruned_at_1e9_over_beta") or [float("nan")]), 3) if isinstance(_fv401.get("diag_flow_gap_pruned_at_1e9_over_beta"), list) else r"\\text{n/d}") + r". "
             r"\\textsf{[OPEN]} A ponte ao corpo físico fica NOMEADA, não provada: a hipótese $H_\\tau$ (o peso $\\tau$ é a massa de Newton e a métrica de Einstein) que nenhum teorema usa; a ORDEM 025 ao Codex (sha16 \\texttt{ORDEM025}, enfileirada) tenta tipá-la pela frente de luz de Bisognano--Wichmann: pendência \\emph{externa} a esta versão. O nome «tensão» dado ao gap dissipativo é nomeação, sem teorema.")
'''.replace("ORDEM025", ORDEM025)
EN = '''    s.append(r"\\textbf{The derived chain.} \\textsf{[DERIVED]} The operator asked that the reading not be his [ONTO] but derived (``eu não queria que a leitura fosse ONTO minha, quero que seja derivado'': he did not want the reading to be his ONTO, he wants it derived), for the statement ``a gravitação universal e a inércia não existem antes da posição impressa do Um absoluto'' (universal gravitation and inertia do not exist before the impressed position of the absolute One). The stone was extended and the kernel now proves, from the axiom $\\omega(I)=1$ and Takesaki's scaling law (\\textsf{[KNOWN]}, a field of the structure): "
             r"(i) \\texttt{no\\_post\\_before\\_the\\_impression}: every positive weight is moved by every nontrivial scale, and weight $1$ occurs only at the cut $a=0$ (the impression); (ii) \\texttt{inertia\\_is\\_not\\_its\\_own\\_cause}: what were fixed from always (on every negative scale), or on every positive scale, weighs zero, and every state of positive weight moves at some scale; "
             r"(iii) \\texttt{the\\_first\\_motion\\_is\\_the\\_impression}: the first motion is the impression of the absolute post occupied by $1$; (iv) \\texttt{the\\_zero\\_is\\_the\\_consequence\\_of\\_the\\_pruning} and \\texttt{leak\\_below\\_every\\_epsilon}: the zero is not a state of the orbit, it is the infimum of the pruning (the bottomless fall, \\texttt{abismo}), and the leak $e^{-t\\beta g}$ falls below every $\\varepsilon>0$; "
             r"(v) \\texttt{the\\_tension\\_is\\_projected\\_onto\\_the\\_attractor} and \\texttt{diagFlow\\_coordinate\\_is\\_the\\_scaling}: the diagonal flow of the Great Attractor is the dual scaling, the coordinate with a gap goes to zero in the limit, is nonzero at finite time, and the gapless one is the equilibrium; the composition is \\texttt{falsidade\\_da\\_inercia\\_derivada}. "
             r"In this rite: the smallest post weight on the grid is " + _f401(_fv401.get("min_weight_on_the_grid_positive"), 6) + r" ($>0$), and the coordinate with a gap, after $t=10^9/\\beta$, has modulus " + (_f401(max(_fv401.get("diag_flow_gap_pruned_at_1e9_over_beta") or [float("nan")]), 3) if isinstance(_fv401.get("diag_flow_gap_pruned_at_1e9_over_beta"), list) else r"\\text{n/a}") + r". "
             r"\\textsf{[OPEN]} The bridge to the physical body is NAMED, not proved: the hypothesis $H_\\tau$ ($\\tau$ is Newton's mass and Einstein's metric), which no theorem uses; ORDER 025 to Codex (sha16 \\texttt{ORDEM025}, queued) tries to type it through the Bisognano--Wichmann light front: a pending item \\emph{external} to this version. The name ``tension'' given to the dissipative gap is a naming, with no theorem.")
'''.replace("ORDEM025", ORDEM025)
edita("artigo_pt_v401.pysnip", PT)
edita("artigo_en_v401.pysnip", EN)
