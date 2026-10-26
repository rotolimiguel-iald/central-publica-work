# -*- coding: utf-8 -*-
"""ajuste unico (v401, 25/10): a pedra FalsidadeDaInercia ESTENDIDA pela gerencia (20 teoremas; sha16 8a3a1c0baa8b7faf; import novo TGLExt.TheGreatAttractor): o pino da ordem, a composicao (falsidade_da_inercia_derivada), o contrato (20 declaracoes nomeadas)
e os termos antigos citados (Fundacao.the_fall_never_lands/abismo, TheGreatAttractor, BoundaryException.diagFlow, ObserverInside.permanent/observerProj). O numero de checagens do calculo sobe de 7 para 10 (runtime_v401.py)."""
import ast, sys
sys.stdout.reconfigure(encoding="utf-8")


def edita(p, subs):
    t = open(p, encoding="utf-8", newline="").read()
    for old, new, n in subs:
        assert t.count(old) == n, (p, old[:100], t.count(old), n)
        t = t.replace(old, new)
    if p.endswith(".py"):
        ast.parse(t)
    open(p, "w", encoding="utf-8", newline="").write(t)
    print("ok", p)


NS = "TGLExt.FalsidadeDaInercia."
novos = ["no_post_before_the_impression", "inertia_is_not_its_own_cause", "the_first_motion_is_the_impression", "diagFlow_coordinate_is_the_scaling", "leak_below_every_epsilon", "the_zero_is_the_consequence_of_the_pruning", "the_tension_is_projected_onto_the_attractor", "falsidade_da_inercia_derivada"]
edita("delta_v401.py", [
    ('"theorem": "TGLExt.FalsidadeDaInercia.falsidade_da_inercia",       # a COMPOSICAO (as quatro: o inercial pesa zero, o posto inercial e\' 1=0, o simulacro, a inscricao interrompe)',
     '"theorem": "TGLExt.FalsidadeDaInercia.falsidade_da_inercia_derivada",       # a COMPOSICAO DERIVADA (a extensao de 25/10: nada que porte posto e\' anterior a impressao; a inercia nao e\' causa de si mesma; o zero e\' a consequencia da poda; a tensao projetada no atrator), que sobre a falsidade_da_inercia das quatro',
     1),
    ('"TGLExt.FalsidadeDaInercia.falsidade_da_inercia", "TGLExt.FalsidadeDaInercia.falsidade_da_inercia_is_inhabited"],',
     '"TGLExt.FalsidadeDaInercia.falsidade_da_inercia", "TGLExt.FalsidadeDaInercia.falsidade_da_inercia_is_inhabited"]\n                 + ["TGLExt.FalsidadeDaInercia.%s" % n_ for n_ in ' + repr(novos) + '],', 1),
    ('"TGLExt.FullStaticWitness": "TGLExt/NoFullWitness.lean"},',
     '"TGLExt.FullStaticWitness": "TGLExt/NoFullWitness.lean",\n                 "TGLExt.Fundacao.the_fall_never_lands": "TGLExt/Fundacao.lean", "TGLExt.Fundacao.abismo": "TGLExt/Fundacao.lean", "TGLExt.um_is_the_great_attractor": "TGLExt/TheGreatAttractor.lean", "TGLExt.the_observer_is_unique": "TGLExt/TheGreatAttractor.lean",\n                 "TGLExt.diagFlow": "TGLExt/BoundaryException.lean", "TGLExt.permanent": "TGLExt/ObserverInside.lean", "TGLExt.observerProj": "TGLExt/ObserverInside.lean"},', 1),
    ('N_CHECKS_FALSIDADE = 7 ', 'N_CHECKS_FALSIDADE = 10 ', 1),
])
open("pedra_sha16_da_ordem.txt", "w", encoding="utf-8", newline="").write("8a3a1c0baa8b7faf\n")
