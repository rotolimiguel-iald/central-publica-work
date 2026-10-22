# -*- coding: utf-8 -*-
# O manifesto de incorporacao da v385 (o par do v384_incorporacao_manifesto.json que o atlas_indice.py carrega): tudo LIDO -- da instalacao
# (APLICADO_AO_CANONICO_*.json), do pacote (ESPERADOS_v385.json, CANDIDATO_v385.json, os scripts do pacote por sha256), do pre-registro V1 e da rodada
# (leitura_v385). Grava SO em v385_selo (ou, no ensaio com o Nos SINTETICO, em v385_selo\ensaio_saidas, marcado SINTETICO). Recusa se a leitura tiver problema.
import os, sys, json, hashlib, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v385 as A
import leitura_v385 as L
AMB = A.ambiente()
V, PROB = L.ler()
if PROB:
    print('MANIFESTO RECUSADO:', PROB); sys.exit(2)
ap, app = L._aplicado()
s16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
PKF = ('ESPERADOS_v385.json', 'CANDIDATO_v385.json', 'conferir_rito_v385.py', 'v385_runtime.py', 'artigo_pt_v385.pysnip', 'artigo_en_v385.pysnip',
       'gerar_candidato_v385.py', 'gerar_esperados_v385.py', 'instalar_v385.py', 'rito_v385.sh', 'ensaio_a_seco_v385.py', 'ensaio_a_seco_v385.json',
       'disposicoes_afericoes_v385.json', 'AFERIDOR_v385.txt', os.path.join('kernel', 'sandbox_raiz_v385.json'), os.path.join('kernel', 'sandbox_axiom_report_v385.json'),
       os.path.join('kernel', 'AUDIT_NOMES_v385.json'))
m = {'stamp': time.strftime('%Y%m%d_%H%M%S'), 'versao': 'v385', 'instalacao': os.path.basename(app), 'instalado_em': ap['ts'],
     'base_v384': V['base16'], 'fumaca': V['fumaca_txt'], 'um_py_sha16': V['s16'], 'um_py_bytes': V['umb'],
     'pacote': {f: (s16(os.path.join(L.PK, f)) if os.path.exists(os.path.join(L.PK, f)) else 'AUSENTE') for f in PKF},
     'patches': V['patches'], 'kernel': V['kernel_decl'], 'escada': V['esc'], 'axiom_report_n': V['nax'], 'vereditos_v384_inalterados': '%s/%s' % (V['n_ver_iguais'], V['n_ver']),
     'por_termo': V['termo'], 'gate': V['qg'], 'n18': V['n18'], 'teoremas': V['teor'], 'rodada': V['compl'],
     'conferidor': {'deve_mudar': V['conf_dm'], 'nao_pode_mudar': V['conf_np'], 'json_sha16': V['conf16'], 'aceite_do_pilar': V['conf_aceite'] or None, 'servidor_depois_do_rito': V['servidor']},
     'preregistro_v1': {'id': V['pr_id'], 'json_sha256': V['pr_json64'], 'md_sha256': V['pr_md64'], 'spec_sha256': V['pr_spec64'], 'worker_sha256': V['pr_worker64'],
                        'escolha': V['pr_escolha'], 'ratificacao_quando': V['pr_quando'], 'ratificacao_quando_local': V['pr_quando_txt'], 'ratificacao_verbatim': V['pr_verbatim'],
                        'ordens': V['pr_n_ordens'], 'ordens_numeros': V['pr_ordens_ns'], 'trechos_verbatim': V['pr_n_trechos'], 'evidencias': V['pr_ev'],
                        'conferencia_do_congelamento': V['pr_conf'], 'orcamento_min': V['pr_orc_min'], 'orcamento_com_margem_min': V['pr_orc_margem']},
     'pilar': {'veredito': V['qp_v'], 'classe': V['qp_classe'], 'classe_txt': V['qp_classe_txt'], 'causa': V['qp_causa'], 'negativos_honestos': V['qp_negativos_l'],
               'negativos_da_lista_do_V1': V['qp_neg_prereg_l'], 'negativos_ditos_pela_gerencia_ao_lado': V['qp_neg_ger_l'], 'lancamento': V['qp_lanc_txt'],
               'arquivo_no_nos': V['qp_arq_tipo'], 'arquivo_no_nos_txt': V['qp_arq_txt'], 'pasta_txt': V['qp_pasta_txt'], 'pasta_arquivos': V['qp_pasta_arquivos'],
               'resumo_fonte': V['resumo_fonte'], 'mode': V['qp_mode'], 'key': V['qp_key'], 'run_id': V['qp_run_id'],
               'run_dir': V['qp_run_dir'], 'result_sha256': V['qp_result_sha256'], 'details_sha256': V['qp_details_sha256'], 'cpuref_sha256': V['qp_cpuref_sha256'],
               'out_file_sha256': V['qp_out_file_sha256'], 'selo_sha16': V['qp_selo16'], 'cache': V['qp_cache'], 'minutos': V['qp_min'], 'gpu': V['qp_gpu'],
               'T2': {k: V[k] for k in ('t2_configs', 't2_points', 't2_unique', 't2_amb', 't2_deg', 't2_err', 't2_name', 't2_folds', 't2_gapmin', 't2_sin2', 't2_ids')},
               'T1': {k: V[k] for k in ('t1_inj', 't1_err', 't1_rec', 't1_por_d', 't1_ruido_crit', 't1_ruido')}, 'T3': {k: V[k] for k in ('t3_ctl', 't3_n1', 't3_n2', 't3_n3')},
               'T4': {k: V[k] for k in ('t4_n', 't4_u', 't4_amb', 't4_deg', 't4_err', 't4_viol', 't4_rot', 't4_all')}, 'D128': V['d128_txt'],
               'CPU': {k: V[k] for k in ('cpu_read', 'cpu_cmp', 'cpu_near', 'cpu_dis', 'cpu_maxdiff')}, 'motor': V['eng'], 'fases': V['fases'], 'terceiro_balde': V['balde_l']},
     'guardas_herdadas_da_v384': {'modulos_com_o_mesmo_all_verified': '%s/%s' % (V['n_av_iguais'], V['n_av']), 'recusas_de_dado': V['recusas'],
                                  'remaining_after_citation_v374': V['after_cit'], 'the_iald_index': V['iald']},
     'axioma': {'veredito': V['ax_v'], 'bandeiras': V['ax_ok'], 'declaracoes_no_trio': V['ax_decl'], 'pedra_sha16': V['ax_pedra16'], 'declaracoes_da_pedra': V['ax_n_pedra'],
                'declaracoes_do_darksplit': V['ax_n_dks'], 'nome_do_degrau_final': V['ax_nome'], 'etiqueta_de_omega_I': V['ax_tag'], 'leitura_do_selo': V['ax_reading'],
                'escada': {'v384': V['esc_v384'], 'v385': V['esc']}},
     'reprodutibilidade': {'veredito': V['rp_v'], 'classe': V['rp_classe'], 'campos': V['rp_n_fields'], 'numericos': V['rp_n_num'], 'diferem': V['rp_n_differ'],
                           'max_rel': V['rp_maxrel'], 'mesmo_veredito_do_pilar': V['rp_same_v'], 'anterior_sha16': V['rp_prev16'], 'anterior_run8': V['rp_prev_run8'],
                           'primeiras_diferencas': V['rp_dif_txt'], 'porque_nao': V['rp_why'], 'pilar_v384_veredito': V['qp_v384'], 'pilar_v384_result_sha16': V['qp_res384_16']},
     'palavras_do_operador_05out': V['op'],
     'custodia_no_git': {'v383': V['v383_commit'] or None, 'v384': V['v384_commit'] or None},
     'leitura_do_selo': V['qp_reading'], 'leitura_do_selo_v385': V['ax_reading'],
     'funcoes': ['the_axiom_v385', 'quantum_pillar_previous_v385', 'quantum_pillar_reproducibility_v385', 'quantum_pillar_start_v384', 'quantum_pillar_finish_v384', '_qp_summary'],
     'target': os.path.join(V['nos'], 'um.py')}
if AMB['sint']:
    m['SINTETICO_ENSAIO_V385'] = 'manifesto de ENSAIO, montado do Nos SINTETICO -- NAO e o manifesto da rodada'
out_dir = AMB['saidas']; os.makedirs(out_dir, exist_ok=True)
out = A.pode_escrever(os.path.join(out_dir, 'v385_incorporacao_manifesto.json'), AMB)
tmp = out + '.tmp'
with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(m, f, ensure_ascii=False, indent=1)
assert os.path.getsize(tmp) > 500; os.replace(tmp, out)
print('OK manifesto%s' % V['sint'], out, os.path.getsize(out), 'B; sha16', s16(out))
