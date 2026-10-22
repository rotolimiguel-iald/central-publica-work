# -*- coding: utf-8 -*-
# O manifesto de incorporacao da v383 (o par do v370_incorporacao_manifesto.json que o atlas_indice.py carrega): tudo LIDO -- da instalacao
# (APLICADO_AO_CANONICO_*.json), do pacote (ESPERADOS_v383.json, patches_v383.json, MANIFESTO_MONTAGEM_v383.json, BANDEIRAS_v383.json) e da rodada (leitura_v383).
# Grava SO em v383_selo. Recusa se a leitura tiver problema.
import os, sys, json, hashlib, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v383 as L
V, PROB = L.ler()
if PROB:
    print('MANIFESTO RECUSADO:', PROB); sys.exit(2)
ap, app = L._aplicado()
s16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
m = {'stamp': time.strftime('%Y%m%d_%H%M%S'), 'instalacao': os.path.basename(app), 'instalado_em': ap['ts'],
     'base_build_v381': V['base_build16'], 'substituida_no_nos_v382_so_local': V['base16'], 'um_py_sha16': V['s16'], 'um_py_bytes': V['umb'],
     'pacote': {f: s16(os.path.join(L.PK, f)) for f in ('ESPERADOS_v383.json', 'patches_v383.json', 'BANDEIRAS_v383.json', 'conferir_rito_v383.py',
                                                          'v383_runtime.py', 'artigo_pt_v383.pysnip', 'artigo_en_v383.pysnip')},
     'pedras_materializadas': {('TGLExt/%s.lean' % n): d['sha16'] for n, d in V['pedras'].items()}, 'tentativas_preservadas': V['tentativas'], 'gpc': V['gpc'], 'por_termo': V['termo'],
     'fronteira': {'remaining': V['remaining'], 'closed_by_citation_v374': V['closed_cit'], 'remaining_after_citation_v374': V['after_cit'], 'identificacoes_abertas': V['ident_open']}, 'livro_razao': V['ledger'],
     'bandeiras_novas': '%d/%d' % (V['n_flags_on'], V['n_flags']), 'escada': V['esc'], 'axiom_report_n': V['nax'],
     'funcoes': ['prove_the_ledger_of_charges_v383'], 'livro_de_cobrancas': {'beta': V['beta'], 'law_alpha_sqrt_e': V['law'], 'theta_M': V['theta'], 'face_cos2': V['facew'], 'refl_sin2': V['reflw'], 'transmitted_1': V['trans'], 'charged_1': V['charged'], 'viscosity_g1': V['visc'], 'n_ledger': V['n_ledger'], 'counts': V['counts'], 'by_side': V['by_side'], 'by_how': V['by_how'], 'n_in_rule': V['n_in_rule'], 'n_beside': V['n_beside'], 'counts_in_rule': V['counts_in_rule'], 'R2_gamma_100hz_per_s': V['r2_gamma'], 'R2_gamma_accumulated_1gpc': V['r2_acc'], 'ledger': V['ledger_ids'], 'prereg': {'id': V['pr_id'], 'json16': V['pr_json16'], 'md16': V['pr_md16'], 'mapa_seq': V['pr_seq'], 'supersede': V['pr_super']}, 'final_step_name_proposed': V['fsn'], 'gate_unchanged': V['gate_unchanged'], 'kernel_flags': '%s/%s' % (V['kf_on'], V['kf_n']), 'n_print': {'TheLedgerOfCharges': V['n_loc'], 'ThePsionAndTheViscosity': V['n_psv']}, 'rotas_fora_do_livro': {'n': V['rot_n'], 'excluidas_pelos_dados': V['rot_exc'], 'inconclusivas': V['rot_inc'], 'ids': V['rot_ids'], 'nao_sao_cobrancas_da_teoria': True}, 'decisao_do_operador': V['decisao']}, 'vereditos': {k: V[k] for k in L.NOVOS}, 'the_iald_index': V['iald'],
     'leituras_do_selo': {k: V[k] for k in L.LEITURAS},
     'gate': V['qg'], 'teoremas': V['teor'], 'conferidor': {'deve_mudar': V['conf_dm'], 'nao_pode_mudar': V['conf_np'], 'json_sha16': V['conf16']},
     'target': os.path.join(V['nos'], 'um.py')}
out = os.path.join(HERE, 'v383_incorporacao_manifesto.json')
tmp = out + '.tmp'
with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(m, f, ensure_ascii=False, indent=1)
assert os.path.getsize(tmp) > 500; os.replace(tmp, out)
print('OK manifesto', out, os.path.getsize(out), 'B; sha16', s16(out))
