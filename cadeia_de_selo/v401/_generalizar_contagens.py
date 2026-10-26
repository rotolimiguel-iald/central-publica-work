# -*- coding: utf-8 -*-
"""ajuste unico (v401): os literais de contagem que dependem da pedra e das inscricoes (12 declaracoes, 7 checagens, 5 inscricoes) passam a ser LIDOS do delta/spec, para a pedra poder ser estendida sem cacar numeros digitados."""
import ast, re, sys
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


edita("conferir_rito_v401.py", [
    ('len(ESP["cunhagens"]) == len(DL.VERBATIM_ORIGEM_V401) == 5 and', 'len(ESP["cunhagens"]) == len(DL.VERBATIM_ORIGEM_V401) and', 1),
    ('(FA.get("mechanics") or {}).get("n_checks") == 7', '(FA.get("mechanics") or {}).get("n_checks") == DL.N_CHECKS_FALSIDADE', 1),
    ('; 7 checagens do calculo no modelo oneScaling', '; as checagens do calculo no modelo oneScaling', 1),
])
edita("exame_pontos_v401.py", [('(pfa.get("mecanica") or {}).get("n_checks") != 7', '(pfa.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS_FALSIDADE', 1)])
edita("conferir_citacoes_v401.py", [('len(V) == len(DL.VERBATIM_ORIGEM_V401) == 5', 'len(V) == len(DL.VERBATIM_ORIGEM_V401)', 1)])
edita("p00_precondicoes_v401.py", [
    ('len([k for k in MI if k.startswith("cunhagens/")]) == 5', 'len([k for k in MI if k.startswith("cunhagens/")]) == len(DL.VERBATIM_ORIGEM_V401)', 1),
    ('"insumos", "cunhagens"))) == 5,', '"insumos", "cunhagens"))) == len(DL.VERBATIM_ORIGEM_V401),', 1),
])
edita("gerar_candidato_v401.py", [('assert set(RG.VERB_CHAVES) == set(verb) and len(verb) == 5', 'assert set(RG.VERB_CHAVES) == set(verb) and len(verb) == len(DL.VERBATIM_ORIGEM_V401)', 1)])
