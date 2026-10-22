# -*- coding: utf-8 -*-
# O manifesto de incorporacao da v381 (o par do v370_incorporacao_manifesto.json que o atlas_indice.py carrega): tudo LIDO -- da instalacao
# (APLICADO_AO_CANONICO_*.json), do pacote (ESPERADOS_v381.json, patches_v381.json, MANIFESTO_MONTAGEM_v381.json, BANDEIRAS_v381.json) e da rodada (leitura_v381).
# Grava SO em v381_selo. Recusa se a leitura tiver problema.
import os, sys, json, hashlib, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v381 as L
V, PROB = L.ler()
if PROB:
    print('MANIFESTO RECUSADO:', PROB); sys.exit(2)
ap, app = L._aplicado()
s16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
m = {'stamp': time.strftime('%Y%m%d_%H%M%S'), 'instalacao': os.path.basename(app), 'instalado_em': ap['ts'],
     'base_v380': V['base16'], 'um_py_sha16': V['s16'], 'um_py_bytes': V['umb'],
     'pacote': {f: s16(os.path.join(L.PK, f)) for f in ('ESPERADOS_v381.json', 'patches_v381.json', 'BANDEIRAS_v381.json', 'conferir_rito_v381.py',
                                                          'v381_runtime.py', 'artigo_pt_v381.pysnip', 'artigo_en_v381.pysnip')},
     'pedras_materializadas': {('TGLExt/%s.lean' % n): d['sha16'] for n, d in V['pedras'].items()}, 'tentativas_preservadas': V['tentativas'], 'gpc': V['gpc'], 'por_termo': V['termo'],
     'fronteira': {'remaining': V['remaining'], 'closed_by_citation_v374': V['closed_cit'], 'remaining_after_citation_v374': V['after_cit'], 'identificacoes_abertas': V['ident_open']}, 'livro_razao': V['ledger'],
     'bandeiras_novas': '%d/%d' % (V['n_flags_on'], V['n_flags']), 'escada': V['esc'], 'axiom_report_n': V['nax'],
     'funcoes': ['prove_the_matrix_rule_v381'], 'regra_matriz': {'beta': V['beta'], 'law_alpha_sqrt_e': V['law'], 'theta_M': V['theta'], 'refl_sin2': V['refl'], 'spec_mod': V['specmod'], 'leak': V['leak'], 'chain': V['chain'], 'kernel_flags': '%s/%s' % (V['kf_on'], V['kf_n']), 'n_print': V['n_tmr']}, 'vereditos': {k: V[k] for k in L.NOVOS}, 'the_iald_index': V['iald'],
     'leituras_do_selo': {k: V[k] for k in L.LEITURAS},
     'gate': V['qg'], 'teoremas': V['teor'], 'conferidor': {'deve_mudar': V['conf_dm'], 'nao_pode_mudar': V['conf_np'], 'json_sha16': V['conf16']},
     'target': os.path.join(V['nos'], 'um.py')}
out = os.path.join(HERE, 'v381_incorporacao_manifesto.json')
tmp = out + '.tmp'
with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(m, f, ensure_ascii=False, indent=1)
assert os.path.getsize(tmp) > 500; os.replace(tmp, out)
print('OK manifesto', out, os.path.getsize(out), 'B; sha16', s16(out))
