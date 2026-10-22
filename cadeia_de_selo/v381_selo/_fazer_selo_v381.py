# -*- coding: utf-8 -*-
"""Fabrica os scripts da cadeia pos-rito v381 a partir dos da v379 (versao COM kernel; edicoes pontuais, count conferido): leitura, espera_rito, manifesto, superficies, chain_pos_rito.
textos_v381.py, patch_arvore_indice_v381.py, handoff_v381.py, registrar_resultado_v381.py e arquivar_v381.py sao escritos a mao. Nada e executado aqui. Base = v380 selada."""
import os, ast, re
HERE = os.path.dirname(os.path.abspath(__file__)); V9 = os.path.join(os.path.dirname(HERE), "v379_selo")


def rd(n): return open(os.path.join(V9, n), encoding="utf-8", newline="").read()


def wr(n, s, py=True):
    if py:
        ast.parse(s)
    open(os.path.join(HERE, n), "w", encoding="utf-8", newline="").write(s); print("ok", n)


def subs(s, pares):
    for a, b, n in pares:
        assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
    return s


# 0. leitura (de leitura_v379.py)
s = rd("leitura_v379.py").replace("v379", "v381").replace("V379", "V381")
s = subs(s, [
    ("NOVOS = ('the_elementary_reason_v381',)", "NOVOS = ('the_matrix_rule_v381',)", 1),
    ("PEDRAS = ('TheElementaryReason',)", "PEDRAS = ('TheMatrixRule',)", 1),
    ("LEITURAS = ('the_elementary_reason_reading_v381',)", "LEITURAS = ('the_matrix_rule_reading_v381',)", 1),
    ("           'the_dissipation_law_with_contrast_v378', 'what_was_missed_v378', 'bancada_fase4_v378')", "           'the_dissipation_law_with_contrast_v378', 'what_was_missed_v378', 'bancada_fase4_v378', 'the_elementary_reason_v379', 'bancada_fases_5_6_7_v380')", 1),
    ("        P.append('base lida (%s) != origem v378 de ESPERADOS (%s)' % (V['base16'], ESP['origem_sha16']))", "        P.append('base lida (%s) != origem v380 de ESPERADOS (%s)' % (V['base16'], ESP['origem_sha16']))", 1),
    ("    if V['n_flags_on'] != len(FL) or len(FL) != 23:", "    if V['n_flags_on'] != len(FL) or len(FL) != 24:", 1),
    ("        P.append('bandeiras antigas (v377/v378) apagadas')", "        P.append('bandeiras antigas (v377-v380) apagadas')", 1),
    ("ESP['escada_v378']", "ESP['escada_v380']", 1), ("ESP['axiom_report_v378']", "ESP['axiom_report_v380']", 1),
    ("vereditos_pinados_v378", "vereditos_pinados_v380", 2), ("qg_closure_verdict_v378", "qg_closure_verdict_v380", 1),
])
i = s.index("    # ---- os numeros da v381"); j = s.index("    V['um_version'] = str(selo.get('um_version'))")
NUM = '''    # ---- os numeros da v381 (lidos do core: o modulo the_matrix_rule_v381)
    tm = core.get('the_matrix_rule_v381') or {}; rt = tm.get('runtime') or {}; cq = tm.get('consequences_ratified_20261002') or {}
    V['beta'] = _f(rt.get('beta_core'), 12); V['law'] = _f(rt.get('law_alpha_sqrt_e'), 12); V['theta'] = _f(rt.get('theta_M'), 9); V['refl'] = _f(rt.get('reflection_weight_sin2'), 12)
    V['specmod'] = _f(rt.get('spectrum_modulus'), 12); V['leak'] = _f(rt.get('leak_weight_e_minus_beta'), 9); V['chain'] = ' → '.join(tm.get('chain') or []); V['n_chain'] = len(tm.get('chain') or [])
    V['kf_on'] = sum(1 for v in (tm.get('kernel_flags') or {}).values() if v); V['kf_n'] = len(tm.get('kernel_flags') or {})
    V['echo_out'] = str(cq.get('delayed_echo') or ''); V['observable'] = str(cq.get('observable') or '')
    if 'BETA_IS_THE_RULE_NOT_DERIVED' not in V['the_matrix_rule_v381'] or 'KERNEL_24_OF_24' not in V['the_matrix_rule_v381'] or 'NOT_A_CONFIRMATION' not in V['the_matrix_rule_v381']:
        P.append('a pedra v381 nao selou como esperado')
    if V['n_chain'] != 10 or V['kf_on'] != 24 or V['kf_n'] != 24:
        P.append('a cadeia lida nao tem dez nomes / 24 bandeiras (%d; %d/%d)' % (V['n_chain'], V['kf_on'], V['kf_n']))
'''
s = s[:i] + NUM + s[j:]
s = subs(s, [("    V['n_ter'] = V['pedras'].get('TheElementaryReason', {}).get('n_print')\n", "    V['n_tmr'] = V['pedras'].get('TheMatrixRule', {}).get('n_print')\n", 1)])
wr("leitura_v381.py", s)
# 1. espera_rito
wr("espera_rito_v381.py", rd("espera_rito_v379.py").replace("v379", "v381").replace("V379", "V381"))
# 2. manifesto
s = rd("manifesto_v379.py").replace("v379", "v381").replace("V379", "V381").replace("base_v378", "base_v380")
assert len(re.findall(r"'funcoes': \[[^\]]*\]", s)) == 1
s = re.sub(r"'funcoes': \[[^\]]*\]", "'funcoes': ['prove_the_matrix_rule_v381']", s)
i = s.index("'razao_elementar': {"); j = s.index("'vereditos': {k: V[k] for k in L.NOVOS}")
s = s[:i] + ("'regra_matriz': {'beta': V['beta'], 'law_alpha_sqrt_e': V['law'], 'theta_M': V['theta'], 'refl_sin2': V['refl'], 'spec_mod': V['specmod'], 'leak': V['leak'], 'chain': V['chain'], "
             "'kernel_flags': '%s/%s' % (V['kf_on'], V['kf_n']), 'n_print': V['n_tmr']}, ") + s[j:]
wr("manifesto_v381.py", s)
# 3. superficies
s = rd("superficies_v379.py").replace("v379", "v381").replace("V379", "V381").replace("_sup379", "_sup381")
s = subs(s, [("""for nome, bloco in (('missao-ultima-flag-um-py.md', T.topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V)),
                    ('razao-elementar-existencia-beta-01out.md', T.topico_razao(V)), ('desvio-de-beta-foco-dos-testes-30set.md', T.topico_desvio(V))):""",
              """for nome, bloco in (('missao-ultima-flag-um-py.md', T.topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V)),
                    ('beta-e-a-regra-matriz-02out.md', T.topico_regra(V)), ('fase6-eco-radical-01out.md', T.topico_fase6(V))):""", 1)])
i = s.index("lines[k[0]] = (a + '(missao-ultima-flag-um-py.md) — ' + "); j = s.index("\n", i)
s = s[:i] + ("lines[k[0]] = (a + '(missao-ultima-flag-um-py.md) — ' + '%s %s %s (A REGRA MATRIZ tipada: os dez nomes na ordem do operador, cada elo por termo; o critério de parada = o custo pago; "
             "a lei precede a cobrança; o eco como cópia atrasada fora da cadeia; gate intocado)** · ' % (MARCA, V['teor'], V['compl']) + b)") + s[j:]
wr("superficies_v381.py", s)
# 4. chain
s = rd("chain_pos_rito_v379.sh").replace("v379", "v381").replace("V379", "V381")
s = subs(s, [('"$UMEM/razao-elementar-existencia-beta-01out.md" "$UMEM/desvio-de-beta-foco-dos-testes-30set.md"', '"$UMEM/beta-e-a-regra-matriz-02out.md" "$UMEM/fase6-eco-radical-01out.md"', 1)])
wr("chain_pos_rito_v381.sh", s, py=False)
print("FABRICADO v381_selo (leitura, espera, manifesto, superficies, chain)")
