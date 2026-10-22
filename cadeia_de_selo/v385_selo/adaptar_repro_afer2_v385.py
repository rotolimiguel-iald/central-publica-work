# -*- coding: utf-8 -*-
"""A cadeia da v385 para o comparador novo (afericao de codigo): a diferenca maxima lida de max_scaled_diff (escala max(1,|a|,|b|)); NOT_COMPARED_DIFFERENT_INPUTS
e NOT_COMPARED_RUNTIME_ERROR na classe «nao comparado»; o D128 excluido dito; e «logo depois de lancar o trabalhador» no lugar de «antes do calculo».
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
    open(P + ".bak_" + st + "_repro", "wb").write(s0.encode("utf-8"))
    open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
    print("OK", nome, len(pares), "trocas")


aplica("leitura_v385.py", [
    ("    if '__NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT__' in v:",
     "    if any(t_ in v for t_ in ('__NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT__', '__NOT_COMPARED_DIFFERENT_INPUTS__', '__NOT_COMPARED_RUNTIME_ERROR__')):"),
    ("    V['rp_maxrel'] = _e(rp.get('max_rel_diff')); V['rp_same_v'] = _sim(rp.get('same_pillar_verdict'))",
     "    V['rp_maxrel'] = _e(rp.get('max_scaled_diff')); V['rp_same_v'] = _sim(rp.get('same_pillar_verdict'))   # a escala max(1,|a|,|b|) (afericao de codigo)\n"
     "    V['rp_d128_excl'] = rp.get('d128_excluded') is True; V['rp_nonfinite'] = rp.get('n_nonfinite_differ', 'n/d')\n"
     "    V['rp_entradas'] = _sim(((rp.get('inputs') or {}).get('same'))); V['rp_ambiente'] = _sim(((rp.get('env') or {}).get('same')))"),
])
aplica("textos_v385.py", [
    ("        X['rp_frase'] = ('iguais a menos de arredondamento: {rp_n_differ} de {rp_n_fields} campos diferem, diferença relativa máxima {rp_maxrel} (≤ 1e-9); '",
     "        X['rp_frase'] = ('iguais a menos de arredondamento: {rp_n_differ} de {rp_n_fields} campos diferem, diferença máxima na escala max(1, |a|, |b|) {rp_maxrel} (≤ 1e-9); '"),
    ("        X['rp_frase'] = ('DIFERENTES em {rp_n_differ} de {rp_n_fields} campos (diferença relativa máxima {rp_maxrel}) — é resultado, e fica dito; '",
     "        X['rp_frase'] = ('DIFERENTES em {rp_n_differ} de {rp_n_fields} campos (diferença máxima na escala max(1, |a|, |b|) {rp_maxrel}; {rp_nonfinite} campo(s) não finito(s) diferente(s)) — é resultado, e fica dito; '"),
    ("    X['rp_curta'] =", "    if V.get('rp_d128_excl'):\n        X['rp_frase'] += ' — os campos do D128 ficaram fora da comparação (o D128 não rodou nesta rodada e rodou na anterior)'\n"
                          "    X['rp_frase'] += ' (entradas iguais: {rp_entradas}; ambiente igual: {rp_ambiente})'.format(**V)\n    X['rp_curta'] ="),
    ("com o registro `quantum_pillar_reproducibility_v385`: antes do cálculo, o `um.py` lê o \"",
     "com o registro `quantum_pillar_reproducibility_v385`: logo depois de lançar o trabalhador, antes que o cálculo novo possa substituí-lo, o `um.py` lê o \""),
])
