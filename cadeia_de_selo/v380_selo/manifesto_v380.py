# -*- coding: utf-8 -*-
# O manifesto de incorporacao da v380 (o par do v370_incorporacao_manifesto.json que o atlas_indice.py carrega): tudo LIDO -- da instalacao
# (APLICADO_AO_CANONICO_*.json), do pacote (ESPERADOS_v380.json, patches_v380.json, MANIFESTO_MONTAGEM_v380.json, BANDEIRAS_v380.json) e da rodada (leitura_v380).
# Grava SO em v380_selo. Recusa se a leitura tiver problema.
import os, sys, json, hashlib, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v380 as L
V, PROB = L.ler()
if PROB:
    print('MANIFESTO RECUSADO:', PROB); sys.exit(2)
ap, app = L._aplicado()
s16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
m = {'stamp': time.strftime('%Y%m%d_%H%M%S'), 'instalacao': os.path.basename(app), 'instalado_em': ap['ts'],
     'base_v379': V['base16'], 'um_py_sha16': V['s16'], 'um_py_bytes': V['umb'],
     'pacote': {f: s16(os.path.join(L.PK, f)) for f in ('ESPERADOS_v380.json', 'patches_v380.json', 'BANDEIRAS_v380.json', 'conferir_rito_v380.py',
                                                          'v380_runtime.py', 'artigo_pt_v380.pysnip', 'artigo_en_v380.pysnip')},
     'pedras_materializadas': {('TGLExt/%s.lean' % n): d['sha16'] for n, d in V['pedras'].items()}, 'tentativas_preservadas': V['tentativas'], 'gpc': V['gpc'], 'por_termo': V['termo'],
     'fronteira': {'remaining': V['remaining'], 'closed_by_citation_v374': V['closed_cit'], 'remaining_after_citation_v374': V['after_cit'], 'identificacoes_abertas': V['ident_open']}, 'livro_razao': V['ledger'],
     'bandeiras_novas': '%d/%d' % (V['n_flags_on'], V['n_flags']), 'escada': V['esc'], 'axiom_report_n': V['nax'],
     'funcoes': ['prove_bancada_fases_5_6_7_v380'], 'bancada_fases_5_6_7': {'h0_escada': [V['h0_v'], V['h0_s'], V['h0_z']], 'kms_todos': [V['k6_a'], V['k6_s'], V['k6_z1'], V['k6_z2'], V['k6_sys']], 'kms_o4_cego': [V['o6_z1'], V['o6_z2']], 'may_sys': V['m6_sys'], 'may_ctrl_v3_tau_half': [V['m6_c1'], V['m6_c1o'], V['m6_flag']], 'v4': [V['v4_z2'], V['v4_ctrl']], 'v5': [V['v5_z1'], V['v5_z2'], V['v5_o1'], V['v5_o2'], V['v5_r3p'], V['v5_r3cp'], V['v5_r3lab'], V['v5_clausula']], 't7_z_ganho': [V['t7_diag'], V['t7_m20']], 'u7_lnB': [V['u7_diag'], V['u7_m20']], 'gw_bank': [V['gb_ok'], V['gb_n'], V['gb_nan'], V['gb_out']], 'n_erratas': V['n_erratas'], 'crlf_differs': V['n_crlf']}, 'vereditos': {k: V[k] for k in L.NOVOS}, 'the_iald_index': V['iald'],
     'leituras_do_selo': {k: V[k] for k in L.LEITURAS},
     'gate': V['qg'], 'teoremas': V['teor'], 'conferidor': {'deve_mudar': V['conf_dm'], 'nao_pode_mudar': V['conf_np'], 'json_sha16': V['conf16']},
     'target': os.path.join(V['nos'], 'um.py')}
out = os.path.join(HERE, 'v380_incorporacao_manifesto.json')
tmp = out + '.tmp'
with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(m, f, ensure_ascii=False, indent=1)
assert os.path.getsize(tmp) > 500; os.replace(tmp, out)
print('OK manifesto', out, os.path.getsize(out), 'B; sha16', s16(out))
