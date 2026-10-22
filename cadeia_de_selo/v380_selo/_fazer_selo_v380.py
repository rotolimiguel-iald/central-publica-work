# -*- coding: utf-8 -*-
"""Fabrica os scripts da cadeia pos-rito v380 a partir dos da v379 (edicoes pontuais, count conferido): leitura, espera_rito, manifesto, superficies, chain_pos_rito.
textos_v380.py, patch_arvore_indice_v380.py, handoff_v380.py e registrar_resultado_v380.py sao escritos a mao. Nada e executado aqui. A v380 e SEM kernel novo."""
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
s = rd("leitura_v379.py")
s = s.replace("v379", "v380").replace("V379", "V380")
s = subs(s, [
    ("NOVOS = ('the_elementary_reason_v380',)", "NOVOS = ('bancada_fases_5_6_7_v380',)", 1),
    ("PEDRAS = ('TheElementaryReason',)", "PEDRAS = ()", 1),
    ("LEITURAS = ('the_elementary_reason_reading_v380',)", "LEITURAS = ('the_bancada_fases_5_6_7_reading_v380',)", 1),
    ("           'the_dissipation_law_with_contrast_v378', 'what_was_missed_v378', 'bancada_fase4_v378')", "           'the_dissipation_law_with_contrast_v378', 'what_was_missed_v378', 'bancada_fase4_v378', 'the_elementary_reason_v379')", 1),
    ("        P.append('base lida (%s) != origem v378 de ESPERADOS (%s)' % (V['base16'], ESP['origem_sha16']))", "        P.append('base lida (%s) != origem v379 de ESPERADOS (%s)' % (V['base16'], ESP['origem_sha16']))", 1),
    ("    _nomes = json.load(open(os.path.join(PK, 'AUDIT_NOMES_v380.json'), encoding='utf-8'))", "    _nomes = {}   # v380: sem pedra nova", 1),
    ("    if V['n_flags_on'] != len(FL) or len(FL) != 23:", "    if V['n_flags_on'] != len(FL) or len(FL) != 0:", 1),
    ("        P.append('bandeiras antigas (v377/v378) apagadas')", "        P.append('bandeiras antigas (v377-v379) apagadas')", 1),
    ("    V['esc_ant'] = '%d/%d' % tuple(ESP['escada_v378']); V['nax'] = len(kf.get('axiom_report') or {}); V['nax_ant'] = ESP['axiom_report_v378']",
     "    V['esc_ant'] = '%d/%d' % tuple(ESP['escada_v379']); V['nax'] = len(kf.get('axiom_report') or {}); V['nax_ant'] = ESP['axiom_report_v379']\n    if V['esc'] != V['esc_ant']:\n        P.append('a escada MUDOU numa versao sem kernel novo (%s != %s)' % (V['esc'], V['esc_ant']))", 1),
    ("vereditos_pinados_v378", "vereditos_pinados_v379", 2),
    ("qg_closure_verdict_v378", "qg_closure_verdict_v379", 1),
])
i = s.index("    # ---- os numeros da v380"); j = s.index("    V['um_version'] = str(selo.get('um_version'))")
NUM = '''    # ---- os numeros da v380 (lidos do core: o modulo bancada_fases_5_6_7_v380)
    bf = core.get('bancada_fases_5_6_7_v380') or {}; f5 = bf.get('fase5') or {}; f6 = bf.get('fase6') or {}; f7 = bf.get('fase7') or {}; e4 = (bf.get('emenda_v4') or {}).get('todos_MAY') or {}; gb = bf.get('gw_bank') or {}
    va = f5.get('validacao') or {}; p5 = f5.get('P_sombra') or {}; k6 = f6.get('todos_KMS') or {}; o6 = f6.get('o4_KMS_cego') or {}; m6 = f6.get('todos_MAY') or {}
    V['h0_v'] = _f(va.get('H0'), 2); V['h0_s'] = _f(va.get('sigma_H0'), 2); V['h0_z'] = _f(va.get('z_vs_alvo'), 2); V['p5_z'] = _f(p5.get('z_delta'), 2)
    V['k6_a'] = _f(k6.get('a'), 3); V['k6_s'] = _f(k6.get('sigma_usado'), 3); V['k6_z1'] = _f(k6.get('z_excl_R1'), 1); V['k6_z2'] = _f(k6.get('z_excl_R2'), 1); V['k6_sys'] = _f(k6.get('sistematica_abs'), 3)
    V['o6_z1'] = _f(o6.get('z_excl_R1'), 1); V['o6_z2'] = _f(o6.get('z_excl_R2'), 1); V['m6_sys'] = _f(m6.get('sistematica_abs'), 2)
    V['v4_z2'] = _f(e4.get('z_excl_R2'), 1); V['v4_ctrl'] = _f(e4.get('controles_max_z'), 1)
    tz = f7.get('T_z_ganho') or {}; lb = f7.get('U_lnB_sombra_vs_acumulada') or {}; s7 = (f7.get('S_delta') or {}).get('moresco2020') or {}
    V['t7_diag'] = _f(tz.get('diagonal'), 2); V['t7_m20'] = _f(tz.get('moresco2020'), 2); V['u7_diag'] = _f(lb.get('diagonal'), 2); V['u7_m20'] = _f(lb.get('moresco2020'), 2); V['s7_z'] = _f(s7.get('z'), 2)
    V['gb_ok'] = gb.get('n_ok'); V['gb_n'] = gb.get('n_jobs'); V['n_erratas'] = len(bf.get('errata_beside_v380') or {})
    e5 = (bf.get('emenda_v5') or {}).get('todos_DEC') or {}; o5 = (bf.get('emenda_v5') or {}).get('o4_DEC_cego') or {}
    V['v5_z1'] = _f(e5.get('z_excl_R1'), 1); V['v5_z2'] = _f(e5.get('z_excl_R2'), 1); V['v5_o1'] = _f(o5.get('z_excl_R1'), 1); V['v5_o2'] = _f(o5.get('z_excl_R2'), 1); V['v5_r3p'] = _f(e5.get('poder_R3'), 1); V['v5_sys'] = _f(e5.get('sistematica_abs'), 3)
    # ---- os acrescimos do aferidor v380 (achados 1, 4, 5, 6, 10, 11): rotulo emitido e clausula V5; controle tau/2 de MAY na V3; subamostra O4; poder cego; banco por status; sistematica relativa
    ev5 = bf.get('emenda_v5') or {}; V['v5_r3lab'] = str(ev5.get('R3_rotulo_emitido') or 'AUSENTE').replace('TGL_ECHO_RADICAL_V3__', ''); V['v5_r3cp'] = _f(ev5.get('poder_R3_cego'), 2)
    V['v5_clausula'] = 'NÃO aplicada pelo pipeline (dito)' if ev5.get('clausula_v5_aplicada_pelo_pipeline') is False and ev5.get('clausula_v5_no_preregistro') is True else 'n/d'
    V['k6_n'] = k6.get('n_eventos'); V['o6_n'] = o6.get('n_eventos'); V['k6_sr1'] = _f(k6.get('sist_rel_R1'), 2); V['k6_sr2'] = _f(k6.get('sist_rel_R2'), 2)
    cm = f6.get('controles_MAY_v3_z') or {}; V['m6_c1'] = _f((cm.get('todos') or {}).get('x0.5'), 2); V['m6_c1o'] = _f((cm.get('o4') or {}).get('x0.5'), 2)
    V['m6_flag'] = 'NÃO gravada pelo pipeline (dito)' if f6.get('flag_delay_control_written_by_pipeline') is False else 'n/d'
    gbs = gb.get('status') or {}; V['gb_nan'] = gbs.get('NAN_IN_WINDOW'); V['gb_out'] = gbs.get('WINDOW_OUTSIDE_FILE'); V['n_crlf'] = len(bf.get('crlf_differs') or [])
    if 'KMS_PAIR_SQRT_BETA_AND_SIN2THETA_FALSIFIED_AT_DELAY_LAW' not in V['bancada_fases_5_6_7_v380'] or bf.get('all_verified') is not True:
        P.append('o modulo v380 nao selou como esperado')
    for tok in ('V5_CLAUSE_UNDERPOWERED_NOT_APPLIED_STATED', 'FLAG_NOT_WRITTEN_BY_PIPELINE_STATED', 'BLIND_O4_SUBSAMPLE_', 'ERRATA_BESIDE_6_PLUS_V378_1_PLUS_NOTE_1'):
        if tok not in V['bancada_fases_5_6_7_v380']:
            P.append('o veredito v380 nao carrega o token %s (aferidor)' % tok)
    if not all(k in selo for k in ('joint_coincidence_result_v3_verdict', 'd1_camb_v3_real_v366_verdict')):
        P.append('as chaves EV-06 nao estao no selo')
'''
s = s[:i] + NUM + s[j:]
s = s.replace("    V['n_ter'] = V['pedras'].get('TheElementaryReason', {}).get('n_print')\n", "")
wr("leitura_v380.py", s)
# 1. espera_rito
s = rd("espera_rito_v379.py").replace("v379", "v380").replace("V379", "V380")
wr("espera_rito_v380.py", s)
# 2. manifesto
s = rd("manifesto_v379.py").replace("v379", "v380").replace("V379", "V380").replace("base_v378", "base_v379")
assert len(re.findall(r"'funcoes': \[[^\]]*\]", s)) == 1
s = re.sub(r"'funcoes': \[[^\]]*\]", "'funcoes': ['prove_bancada_fases_5_6_7_v380']", s)
i = s.index("'razao_elementar': {"); j = s.index("'vereditos': {k: V[k] for k in L.NOVOS}")
s = s[:i] + ("'bancada_fases_5_6_7': {'h0_escada': [V['h0_v'], V['h0_s'], V['h0_z']], 'kms_todos': [V['k6_a'], V['k6_s'], V['k6_z1'], V['k6_z2'], V['k6_sys']], 'kms_o4_cego': [V['o6_z1'], V['o6_z2']], "
             "'may_sys': V['m6_sys'], 'may_ctrl_v3_tau_half': [V['m6_c1'], V['m6_c1o'], V['m6_flag']], 'v4': [V['v4_z2'], V['v4_ctrl']], 'v5': [V['v5_z1'], V['v5_z2'], V['v5_o1'], V['v5_o2'], V['v5_r3p'], V['v5_r3cp'], V['v5_r3lab'], V['v5_clausula']], "
             "'t7_z_ganho': [V['t7_diag'], V['t7_m20']], 'u7_lnB': [V['u7_diag'], V['u7_m20']], 'gw_bank': [V['gb_ok'], V['gb_n'], V['gb_nan'], V['gb_out']], 'n_erratas': V['n_erratas'], 'crlf_differs': V['n_crlf']}, ") + s[j:]
s = s.replace("'BANDEIRAS_v380.json', 'conferir_rito_v380.py',", "'BANDEIRAS_v380.json', 'conferir_rito_v380.py',")
wr("manifesto_v380.py", s)
# 3. superficies
s = rd("superficies_v379.py")
s = s.replace("import leitura_v379, textos_v379 as T", "import leitura_v380, textos_v380 as T").replace("leitura_v379.ler()", "leitura_v380.ler()")
s = s.replace("V379_REMAP_DIR", "V380_REMAP_DIR").replace("V379_WRITE_ROOT", "V380_WRITE_ROOT").replace("_sup379", "_sup380")
s = subs(s, [("""for nome, bloco in (('missao-ultima-flag-um-py.md', T.topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V)),
                    ('razao-elementar-existencia-beta-01out.md', T.topico_razao(V)), ('desvio-de-beta-foco-dos-testes-30set.md', T.topico_desvio(V))):""",
              """for nome, bloco in (('missao-ultima-flag-um-py.md', T.topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V)),
                    ('fase6-eco-radical-01out.md', T.topico_fase6(V)), ('fase7-cc-covariancia-01out.md', T.topico_fase7(V)), ('bancada-um.md', T.topico_bancada(V))):""", 1),
             ("MARCA = '**v379 SELADA %s `%s`' % (V['data'][:5], V['s16'])", "MARCA = '**v380 SELADA %s `%s`' % (V['data'][:5], V['s16'])", 1)])
i = s.index("lines[k[0]] = (a + '(missao-ultima-flag-um-py.md) — ' + ")
j = s.index("\n", i)
s = s[:i] + ("lines[k[0]] = (a + '(missao-ultima-flag-um-py.md) — ' + '%s %s %s (AS FASES 5–7 DA BANCADA, O BANCO DE GW E 6+1+1 ERRATAS POR HASH: o par (√β ou sin 2θ, 2π/κ e DEC) falsificado em 240 BBH e na subamostra cega O4; "
             "MAY inconclusivo; a covariância dos cronômetros enfraquece as Fases 4–5; dois desvios do pipeline ditos; sem kernel novo; gate intocado)** · ' % (MARCA, V['teor'], V['compl']) + b)") + s[j:]
s = s.replace("print('NADA A GRAVAR: todas as superficies ja tem a v379 (idempotente)')", "print('NADA A GRAVAR: todas as superficies ja tem a v380 (idempotente)')")
s = s.replace("print('SUPERFICIES v379:", "print('SUPERFICIES v380:")
s = s.replace("'<!-- linha integral do índice (gerência, v379) -->'", "'<!-- linha integral do índice (gerência, v380) -->'")
s = s.replace("'marcador v379 na missao;", "'marcador v380 na missao;")
wr("superficies_v380.py", s)
# 4. chain
s = rd("chain_pos_rito_v379.sh").replace("v379", "v380").replace("V379", "V380")
s = subs(s, [('"$UMEM/razao-elementar-existencia-beta-01out.md" "$UMEM/desvio-de-beta-foco-dos-testes-30set.md"',
              '"$UMEM/fase6-eco-radical-01out.md" "$UMEM/fase7-cc-covariancia-01out.md" "$UMEM/bancada-um.md"', 1)])
wr("chain_pos_rito_v380.sh", s, py=False)
print("FABRICADO v380_selo (leitura, espera, manifesto, superficies, chain)")
