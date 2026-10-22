# -*- coding: utf-8 -*-
"""As contagens da v385 deixam de ser o literal 28 (a forma exponencial entrou na pedra: 22 + 7 = 29): o conferidor, o ensaio a seco, os esperados e a
leitura da cadeia passam a LER o numero das listas (ESPERADOS / o runtime). E o ensaio a seco procura «The One is posited» (N8). Backup de bytes; ast."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); SP = os.path.dirname(HERE)
st = time.strftime("%Y%m%d_%H%M%S")


def aplica(P, pares):
    s0 = open(P, encoding="utf-8", newline="").read(); s = s0
    for a, b in pares:
        n = s.count(a)
        assert n == 1, (os.path.basename(P), "a troca nao e unica", n, a[:100])
        s = s.replace(a, b)
    ast.parse(s)
    open(P + ".bak_" + st + "_afer2", "wb").write(s0.encode("utf-8"))
    open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
    print("OK", os.path.basename(P), len(pares), "trocas")


aplica(os.path.join(HERE, "conferir_rito_v385.py"), [
    ('_prev = rp.get("previous") or {}\n', '_prev = rp.get("previous") or {}\nNF = len(ESP["flags_v385"])   # as bandeiras da v385 (22 da pedra + 7 do TheDarkSplit), LIDAS dos esperados\n'),
    ('"a escada subiu para %d/%d (28 pedras novas, todas limpas)" % (ESP["escada_v385"][1], ESP["escada_v385"][1]):',
     '"a escada subiu para %d/%d (%d pedras novas, todas limpas)" % (ESP["escada_v385"][1], ESP["escada_v385"][1], NF):'),
    ('"as 28 bandeiras da v385 True no kernel_formalization":', '"as %d bandeiras da v385 True no kernel_formalization" % NF:'),
    ('"as 28 declaracoes no axiom_report, todas dentro do trio":', '"as %d declaracoes no axiom_report, todas dentro do trio" % NF:'),
    ('"o Axioma SELOU: 28 de 28, o nome do degrau final lido do kernel e igual ao do operador": ax.get("all_verified") is True and ax.get("kernel_flags_ok") == 28',
     '"o Axioma SELOU: %d de %d, o nome do degrau final lido do kernel e igual ao do operador" % (NF, NF): ax.get("all_verified") is True and ax.get("kernel_flags_ok") == NF'),
    ('and "__KERNEL_28_OF_28__" in V("the_axiom_v385"),', 'and ("__KERNEL_%d_OF_%d__" % (NF, NF)) in V("the_axiom_v385"),'),
    ('"as bandeiras True do kernel = as da v384 + exatamente as 28 da v385":', '"as bandeiras True do kernel = as da v384 + exatamente as %d da v385" % NF:'),
])
aplica(os.path.join(HERE, "ensaio_a_seco_v385.py"), [
    ('assert len(FLAGS) == 28 and all(KREP["bandeiras"].get(f) is True for f in FLAGS)', 'NF = len(FLAGS); assert NF == 29 and all(KREP["bandeiras"].get(f) is True for f in FLAGS)'),
    ('and _ax.get("kernel_flags_ok") == 28 and', 'and _ax.get("kernel_flags_ok") == NF and'),
    ('and "__KERNEL_28_OF_28__" in str(_ax.get("verdict"))', 'and ("__KERNEL_%d_OF_%d__" % (NF, NF)) in str(_ax.get("verdict"))'),
    ('"en": ["Beside (v385): the Axiom and the false witness", "The One is posted",', '"en": ["Beside (v385): the Axiom and the false witness", "The One is posited",'),
])
aplica(os.path.join(HERE, "gerar_esperados_v385.py"), [
    ('assert len(FLAGS) == 28 and all(KR["bandeiras"].get(f) is True for f in FLAGS), "o sandbox nao deu 28/28"',
     'assert len(FLAGS) == 29 and all(KR["bandeiras"].get(f) is True for f in FLAGS), "o sandbox nao deu %d/%d" % (len(FLAGS), len(FLAGS))'),
    ('assert esp["escada_v385"] == [esp["escada_v384"][0], esp["escada_v384"][0] + 28], (esp["escada_v384"], esp["escada_v385"])',
     'assert esp["escada_v385"] == [esp["escada_v384"][0], esp["escada_v384"][0] + len(FLAGS)], (esp["escada_v384"], esp["escada_v385"])'),
])
aplica(os.path.join(SP, "v385_selo", "leitura_v385.py"), [
    ("        P.append('as bandeiras True do kernel (%d) != as da v384 (%d) + as 28 da v385' % (V['n_flags_true'], len(ESP['flags_true_v384'])))",
     "        P.append('as bandeiras True do kernel (%d) != as da v384 (%d) + as %d da v385' % (V['n_flags_true'], len(ESP['flags_true_v384']), len(ESP['flags_v385'])))"),
    ("    if not (ax.get('all_verified') is True and ax.get('kernel_flags_ok') == 28 and ax.get('kernel_flags_total') == 28 and",
     "    if not (ax.get('all_verified') is True and ax.get('kernel_flags_ok') == len(ESP['flags_v385']) and ax.get('kernel_flags_total') == len(ESP['flags_v385']) and"),
])
