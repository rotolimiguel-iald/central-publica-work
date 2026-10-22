# -*- coding: utf-8 -*-
"""Disposicoes da afericao de TEXTO da v385 no runtime (v385_runtime.py):
 achado 4: a bandeira nova ext_axm_axiomFlow_eq_exp_kernel_proved (a forma exponencial ligada ao kernel), na posicao do Audit.lean (depois do tendsto);
 achado 2: «v181» -> «v183» no comentario; N5: o token do veredito diz o alcance certo -- a testemunha ESTATICA proibida por beta; o zero absoluto
 inalcancavel em tempo finito (exp != 0, sem beta); as contagens nas docstrings. Backup de bytes; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "v385_runtime.py")
s0 = open(P, encoding="utf-8", newline="").read(); s = s0
T = [('    "ext_axm_axiomFlow_tendsto_the_post_kernel_proved",\n',
      '    "ext_axm_axiomFlow_tendsto_the_post_kernel_proved",\n    "ext_axm_axiomFlow_eq_exp_kernel_proved",\n'),
     ("# v385 AUDITA o TheDarkSplit (compilado desde a v181, nao auditado ate a v384).",
      "# v385 AUDITA o TheDarkSplit (compilado desde a v183 -- «v181» corrigido pela afericao de texto --, nao auditado ate a v384)."),
     ('"THE_ONE_IS_THE_AXIOM_THE_ZERO_MODE_OF_WEIGHT_ONE__THE_ZERO_IS_THE_FALSE_WITNESS_STATIC_THE_ABSOLUTE_ZERO_FORBIDDEN_BY_BETA__"',
      '"THE_ONE_IS_THE_AXIOM_THE_ZERO_MODE_OF_WEIGHT_ONE__THE_ZERO_IS_THE_FALSE_WITNESS_THE_STATIC_ONE_FORBIDDEN_BY_BETA_THE_ABSOLUTE_ZERO_UNREACHABLE_IN_FINITE_TIME__"'),
     ('"THE_POST_IS_THE_MODULAR_ZERO_THE_GRADIENT_EMERGES_FROM_THE_POST__THE_LIVING_VERB_MOVES_AND_FIXES_THE_NAME__THE_DARK_SPLIT_AUDITED__"',
      '"THE_POST_IS_THE_MODULAR_ZERO_THE_FLOW_IS_THE_EXPONENTIAL_OF_THE_LOCK__THE_LIVING_VERB_TWO_TERMS_MOVES_AND_ACTS_AS_A_SCALAR_ON_THE_NAME__THE_DARK_SPLIT_AUDITED__"'),
     ('"""O AXIOMA (v385): as 21 declaracoes da pedra e as 7 do TheDarkSplit verificadas pelo kernel desta rodada',
      '"""O AXIOMA (v385): as declaracoes da pedra (22) e as do TheDarkSplit (7) verificadas pelo kernel desta rodada')]
for a, b in T:
    n = s.count(a)
    assert n == 1, ("a troca nao e unica", n, a[:100])
    s = s.replace(a, b)
ast.parse(s)
st = time.strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + st + "_afer2", "wb").write(s0.encode("utf-8"))
open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
print("OK v385_runtime.py:", len(T), "trocas")
