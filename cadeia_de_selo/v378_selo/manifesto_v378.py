# -*- coding: utf-8 -*-
# O manifesto de incorporacao da v378 (o par do v370_incorporacao_manifesto.json que o atlas_indice.py carrega): tudo LIDO -- da instalacao
# (APLICADO_AO_CANONICO_*.json), do pacote (ESPERADOS_v378.json, patches_v378.json, MANIFESTO_MONTAGEM_v378.json, BANDEIRAS_v378.json) e da rodada (leitura_v378).
# Grava SO em v378_selo. Recusa se a leitura tiver problema.
import os, sys, json, hashlib, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v378 as L
V, PROB = L.ler()
if PROB:
    print('MANIFESTO RECUSADO:', PROB); sys.exit(2)
ap, app = L._aplicado()
s16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
m = {'stamp': time.strftime('%Y%m%d_%H%M%S'), 'instalacao': os.path.basename(app), 'instalado_em': ap['ts'],
     'base_v377': V['base16'], 'um_py_sha16': V['s16'], 'um_py_bytes': V['umb'],
     'pacote': {f: s16(os.path.join(L.PK, f)) for f in ('ESPERADOS_v378.json', 'patches_v378.json', 'BANDEIRAS_v378.json', 'conferir_rito_v378.py',
                                                          'v378_runtime.py', 'artigo_pt_v378.pysnip', 'artigo_en_v378.pysnip')},
     'pedras_materializadas': {('TGLExt/%s.lean' % n): d['sha16'] for n, d in V['pedras'].items()}, 'tentativas_preservadas': V['tentativas'], 'gpc': V['gpc'], 'por_termo': V['termo'],
     'fronteira': {'remaining': V['remaining'], 'closed_by_citation_v374': V['closed_cit'], 'remaining_after_citation_v374': V['after_cit'], 'identificacoes_abertas': V['ident_open']}, 'livro_razao': V['ledger'],
     'bandeiras_novas': '%d/%d' % (V['n_flags_on'], V['n_flags']), 'escada': V['esc'], 'axiom_report_n': V['nax'],
     'funcoes': ['prove_the_dissipation_law_with_contrast_v378', 'prove_what_was_missed_v378', 'prove_bancada_fase4_v378'], 'contraste': {'K_D1a': V['Ka'], 'K_D1b': V['Kb'], 'I_b': V['Ib'], 'N_star': V['Nstar'], 'min_1_plus_w': V['gmin'], 'delta_over_beta_pred': V['dpred'], 'H0_local_D1b_de_67_36': V['H0b'], 'coma_v378_beside': V['coma_v378']}, 'o_que_faltou': {'shadow_z_d1b_planck': V['w_seis'], 'new_readers_z': V['w_novos'], 'stacked_z': V['w_emp'], 'reanalysis_sha16': V['w_h'], 'declared_blind': V['w_cega']}, 'fase4': {'veredito': V['f4_ver'], 'veredito_T': V['f4_verT'], 'P_delta': V['P_delta'], 'P_sigma': V['P_sigma'], 'P_z': V['P_z'], 'P_pull': V['P_pull'], 'P_lnB': V['P_lnB'], 'T_beta_hat': V['T_bhat'], 'T_delta': V['T_delta'], 'T_z': V['T_z'], 'T_gain': V['T_gain'], 'T_lnB': V['T_lnB'], 'S_z': V['S_z'], 'ctrl_z': V['ctrl_z'], 'poder_previo': V['poder'], 'hashes': V['bancada_hashes']}, 'conferencia_v376_pinada': {'contagens': V['cf_counts'], 'abertos': V['abertos']},
     'vereditos': {k: V[k] for k in L.NOVOS}, 'the_iald_index': V['iald'],
     'leituras_do_selo': {k: V[k] for k in L.LEITURAS},
     'gate': V['qg'], 'teoremas': V['teor'], 'conferidor': {'deve_mudar': V['conf_dm'], 'nao_pode_mudar': V['conf_np'], 'json_sha16': V['conf16']},
     'target': os.path.join(V['nos'], 'um.py')}
out = os.path.join(HERE, 'v378_incorporacao_manifesto.json')
tmp = out + '.tmp'
with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(m, f, ensure_ascii=False, indent=1)
assert os.path.getsize(tmp) > 500; os.replace(tmp, out)
print('OK manifesto', out, os.path.getsize(out), 'B; sha16', s16(out))
