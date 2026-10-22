# -*- coding: utf-8 -*-
"""Fabrica os scripts da cadeia pos-rito v382 a partir dos da v381 (versao COM kernel; edicoes pontuais, count conferido): leitura, espera_rito, manifesto,
superficies, chain_pos_rito, arquivar. textos_v382.py, patch_arvore_indice_v382.py, handoff_v382.py e registrar_resultado_v382.py sao escritos a mao.
Nada e executado aqui. Base = v381 selada (duas pedras novas: TheLedgerOfCharges 19 + ThePsionAndTheViscosity 13 = 32 bandeiras)."""
import os, re, ast
HERE = os.path.dirname(os.path.abspath(__file__)); V1 = os.path.join(os.path.dirname(HERE), "v381_selo")


def rd(n): return open(os.path.join(V1, n), encoding="utf-8", newline="").read()


def wr(n, s, py=True):
    if py:
        ast.parse(s)
    open(os.path.join(HERE, n), "w", encoding="utf-8", newline="").write(s); print("ok", n)


def subs(s, pares):
    for a, b, n in pares:
        assert s.count(a) == n, (a[:100], s.count(a), n); s = s.replace(a, b)
    return s


# 0. leitura (de leitura_v381.py): v381 -> v382 nos nomes do pacote/rodada; depois as chaves da base v380 -> v381; depois os blocos da v382
s = rd("leitura_v381.py").replace("v381", "v382").replace("V381", "V382")
s = subs(s, [
    ("NOVOS = ('the_matrix_rule_v382',)", "NOVOS = ('the_ledger_of_charges_v382',)", 1),
    ("PEDRAS = ('TheMatrixRule',)", "PEDRAS = ('TheLedgerOfCharges', 'ThePsionAndTheViscosity')", 1),
    ("LEITURAS = ('the_matrix_rule_reading_v382',)", "LEITURAS = ('the_ledger_of_charges_reading_v382',)", 1),
    ("'the_elementary_reason_v379', 'bancada_fases_5_6_7_v380')", "'the_elementary_reason_v379', 'bancada_fases_5_6_7_v380', 'the_matrix_rule_v381')", 1),
    ("        P.append('base lida (%s) != origem v380 de ESPERADOS (%s)' % (V['base16'], ESP['origem_sha16']))", "        P.append('base lida (%s) != origem v381 de ESPERADOS (%s)' % (V['base16'], ESP['origem_sha16']))", 1),
    ("    if V['n_flags_on'] != len(FL) or len(FL) != 24:", "    if V['n_flags_on'] != len(FL) or len(FL) != 32:", 1),
    ("        P.append('bandeiras antigas (v377-v380) apagadas')", "        P.append('bandeiras antigas (v377-v381) apagadas')", 1),
    ("ESP['escada_v380']", "ESP['escada_v381']", 1), ("ESP['axiom_report_v380']", "ESP['axiom_report_v381']", 1),
    ("vereditos_pinados_v380", "vereditos_pinados_v381", 2), ("qg_closure_verdict_v380", "qg_closure_verdict_v381", 1),
])
i = s.index("    # ---- os numeros da v382"); j = s.index("    V['um_version'] = str(selo.get('um_version'))")
NUM = '''    # ---- os numeros da v382 (lidos do core: o modulo the_ledger_of_charges_v382)
    lc = core.get('the_ledger_of_charges_v382') or {}; rt = lc.get('runtime') or {}; pr = lc.get('preregistration') or {}; ct = lc.get('counts') or {}; bs = lc.get('by_side') or {}
    V['beta'] = _f(rt.get('beta_core'), 12); V['law'] = _f(rt.get('law_alpha_sqrt_e'), 12); V['theta'] = _f(rt.get('theta_M'), 9)
    V['facew'] = _f(rt.get('face_weight_cos2'), 12); V['reflw'] = _f(rt.get('reflection_weight_sin2'), 12); V['trans'] = _f(rt.get('transmitted_t1_g1'), 9); V['charged'] = _f(rt.get('charged_t1_g1'), 9); V['visc'] = _f(rt.get('viscosity_coefficient_g1'), 12)
    V['n_ledger'] = len(lc.get('ledger') or []); V['counts'] = ', '.join('%s %s' % (k, v) for k, v in ct.items()); V['by_side'] = '; '.join('%s: %s' % (sd, ', '.join('%s %s' % (k, v) for k, v in d.items() if v)) for sd, d in bs.items())
    V['by_how'] = ', '.join('%s %s' % (k, v) for k, v in (lc.get('by_how') or {}).items()); V['n_in_rule'] = lc.get('n_in_rule'); V['n_beside'] = lc.get('n_beside')
    V['counts_in_rule'] = ', '.join('%s %s' % (k, v) for k, v in (lc.get('counts_in_rule') or {}).items() if v)
    V['ledger_ids'] = ', '.join('%s (%s, %s)' % (c.get('id'), c.get('side'), c.get('outcome')) for c in (lc.get('ledger') or []))
    V['kf_on'] = sum(1 for v in (lc.get('kernel_flags') or {}).values() if v); V['kf_n'] = len(lc.get('kernel_flags') or {})
    V['pr_json16'] = str((pr.get('sha256_read') or {}).get('json') or 'AUSENTE')[:16]; V['pr_md16'] = str((pr.get('sha256_read') or {}).get('md') or 'AUSENTE')[:16]; V['pr_id'] = str(pr.get('identificador') or 'AUSENTE'); V['pr_seq'] = str(pr.get('mapa_seq') or 'n/d')
    V['pr_super'] = str(pr.get('supersede') or 'n/d')
    _lab = V['pr_id'].rsplit('_V', 1)[-1].split('_') if '_V' in V['pr_id'] else []
    V['pr_label'] = ('V' + '.'.join(_lab)) if (len(_lab) == 2 and all(x.isdigit() for x in _lab)) else 'AUSENTE'
    if V['pr_label'] == 'AUSENTE':
        P.append('o identificador do pre-registro nao da o rotulo da versao (%s)' % V['pr_id'])
    V['r2_gamma'] = ('%.2e' % rt['R2_gamma_100hz_per_s']) if isinstance(rt.get('R2_gamma_100hz_per_s'), (int, float)) else 'n/d'; V['r2_acc'] = ('%.2e' % rt['R2_gamma_accumulated_1gpc']) if isinstance(rt.get('R2_gamma_accumulated_1gpc'), (int, float)) else 'n/d'
    V['fsn'] = str(lc.get('final_step_name_proposed') or 'AUSENTE'); V['gate_unchanged'] = lc.get('gate_unchanged')
    _eco = lc.get('delayed_echo_pairs') or {}; V['eco_n'] = _eco.get('n'); V['eco_ext'] = _eco.get('extinguished'); V['eco_inc'] = _eco.get('inconclusive')
    if V['eco_n'] != 9 or (V['eco_ext'] or 0) + (V['eco_inc'] or 0) != 9:
        P.append('a contagem do eco como copia atrasada nao fecha (%s)' % _eco)
    if 'THE_TGL_IS_OPTICS_NOT_SEMI_BOTH_SIDES_READ' not in V['the_ledger_of_charges_v382'] or 'KERNEL_32_OF_32' not in V['the_ledger_of_charges_v382'] or 'NOT_A_CONFIRMATION' not in V['the_ledger_of_charges_v382']:
        P.append('as pedras v382 nao selaram como esperado')
    if V['n_ledger'] != 20 or V['kf_on'] != 32 or V['kf_n'] != 32 or pr.get('read_ok') is not True or lc.get('gate_unchanged') is not True:
        P.append('o livro lido nao tem vinte cobrancas / 32 bandeiras / pre-registro %s por hash / gate inalterado (%d; %d/%d; %s; %s)' % (V['pr_label'], V['n_ledger'], V['kf_on'], V['kf_n'], pr.get('read_ok'), lc.get('gate_unchanged')))
    if not all(c.get('outcome_ok') and c.get('matches_preregistration') for c in (lc.get('ledger') or [])) or lc.get('n_token_in_core') != lc.get('n_with_core_key'):
        P.append('alguma cobranca do livro nao bate com o core (pelo modo dito) ou com o pre-registro %s' % V['pr_label'])
'''
s = s[:i] + NUM + s[j:]
s = subs(s, [("    V['n_tmr'] = V['pedras'].get('TheMatrixRule', {}).get('n_print')\n", "    V['n_loc'] = V['pedras'].get('TheLedgerOfCharges', {}).get('n_print'); V['n_psv'] = V['pedras'].get('ThePsionAndTheViscosity', {}).get('n_print')\n", 1)])
assert "the_matrix_rule_v382" not in s and "the_matrix_rule_reading_v382" not in s
wr("leitura_v382.py", s)
# 1. espera (generica)
wr("espera_rito_v382.py", rd("espera_rito_v381.py").replace("v381", "v382").replace("V381", "V382"))
# 2. manifesto
s = rd("manifesto_v381.py").replace("v381", "v382").replace("V381", "V382").replace("base_v380", "base_v381")
s = re.sub(r"'funcoes': \[[^\]]*\]", "'funcoes': ['prove_the_ledger_of_charges_v382']", s)
i = s.index("'regra_matriz': {"); j = s.index("'n_print': V['n_tmr']}, ", i) + len("'n_print': V['n_tmr']}, ")
s = s[:i] + ("'livro_de_cobrancas': {'beta': V['beta'], 'law_alpha_sqrt_e': V['law'], 'theta_M': V['theta'], 'face_cos2': V['facew'], 'refl_sin2': V['reflw'], 'transmitted_1': V['trans'], 'charged_1': V['charged'], "
              "'viscosity_g1': V['visc'], 'n_ledger': V['n_ledger'], 'counts': V['counts'], 'by_side': V['by_side'], 'by_how': V['by_how'], 'n_in_rule': V['n_in_rule'], 'n_beside': V['n_beside'], 'counts_in_rule': V['counts_in_rule'], "
              "'R2_gamma_100hz_per_s': V['r2_gamma'], 'R2_gamma_accumulated_1gpc': V['r2_acc'], 'ledger': V['ledger_ids'], 'prereg': {'id': V['pr_id'], 'json16': V['pr_json16'], 'md16': V['pr_md16'], 'mapa_seq': V['pr_seq'], 'supersede': V['pr_super']}, "
              "'final_step_name_proposed': V['fsn'], 'gate_unchanged': V['gate_unchanged'], 'kernel_flags': '%s/%s' % (V['kf_on'], V['kf_n']), 'n_print': {'TheLedgerOfCharges': V['n_loc'], 'ThePsionAndTheViscosity': V['n_psv']}}, ") + s[j:]
wr("manifesto_v382.py", s)
# 3. superficies
s = rd("superficies_v381.py").replace("v381", "v382").replace("V381", "V382").replace("_sup381", "_sup382")
s = subs(s, [("('beta-e-a-regra-matriz-02out.md', T.topico_regra(V)), ('fase6-eco-radical-01out.md', T.topico_fase6(V))",
              "('beta-e-a-regra-matriz-02out.md', T.topico_regra(V)), ('regra-dos-dois-regimes.md', T.topico_regimes(V))", 1),
             ("(A REGRA MATRIZ tipada: os dez nomes na ordem do operador, cada elo por termo; o critério de parada = o custo pago; a lei precede a cobrança; o eco como cópia atrasada fora da cadeia; gate intocado)",
              "(O LIVRO DE COBRANÇAS tipado: a TGL é ótica, lê a face e o custo; nenhum desfecho move a regra; ψ com norma 1 e a viscosidade; o pré-registro dos dois lados por hash; gate intocado)", 1)])
s = s.replace("# Registro da v376 SELADA:", "# Registro da v382 SELADA (molde herdado da v376):", 1).replace("a linha da missao ganha o marcador v376. Limite", "a linha da missao ganha o marcador v382. Limite").replace("(leitura_v376.ler)", "(leitura_v382.ler)")
wr("superficies_v382.py", s)
# 4. chain
s = rd("chain_pos_rito_v381.sh").replace("v381", "v382").replace("V381", "V382")
s = subs(s, [('"$UMEM/beta-e-a-regra-matriz-02out.md" "$UMEM/fase6-eco-radical-01out.md"', '"$UMEM/beta-e-a-regra-matriz-02out.md" "$UMEM/regra-dos-dois-regimes.md"', 1)])
s = s.replace("# v382 (26/09): CADEIA POS-RITO", "# v382 (02/10): CADEIA POS-RITO").replace("(backups _p376 ao lado)", "(backups _p382 ao lado)").replace("(backups .bak_<STAMP>_sup376 ao lado;", "(backups .bak_<STAMP>_sup382 ao lado;")
wr("chain_pos_rito_v382.sh", s, py=False)
# 5. arquivar
wr("arquivar_v382.py", rd("arquivar_v381.py").replace("v381", "v382"))
print("FABRICADO v382_selo (leitura, espera, manifesto, superficies, chain, arquivar)")
