# -*- coding: utf-8 -*-
# O manifesto de incorporacao da v386 (o par do v385_incorporacao_manifesto.json que o atlas_indice.py carrega): tudo LIDO -- da instalacao
# (APLICADO_AO_CANONICO_*.json), do pacote (ESPERADOS_v386.json, CANDIDATO_v386.json, os scripts do pacote por sha256), dos dados da v386 (os quatro arquivos
# do operador, o ramo B, o kernel do sandbox, as afericoes) e da rodada (leitura_v386). Grava SO em v386_selo (ou, no ensaio com o Nos SINTETICO, em
# v386_selo\ensaio_saidas, marcado SINTETICO). Recusa se a leitura tiver problema.
import os, sys, json, hashlib, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v386 as A
import leitura_v386 as L
AMB = A.ambiente()
V, PROB = L.ler()
if PROB:
    print('MANIFESTO RECUSADO:', PROB); sys.exit(2)
ap, app = L._aplicado()
s16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
PKF = ('ESPERADOS_v386.json', 'CANDIDATO_v386.json', 'conferir_rito_v386.py', 'v386_runtime.py', 'v386_pins.py', 'artigo_pt_v386.pysnip', 'artigo_en_v386.pysnip',
       'gerar_candidato_v386.py', 'gerar_esperados_v386.py', 'instalar_v386.py', 'rito_v386.sh', 'ensaio_a_seco_v386.py', 'ensaio_a_seco_v386.json',
       'conferir_citacoes_v386.py', 'conferir_citacoes_v386.json', 'derivar_rito_v386.py', 'DIFF_rito_v385_v386.txt', 'ENTREGA_v386_pacote.json')
DATF = ('CONSTRUIR_v386_resultado.json', 'VERBO_operador_05out.txt', 'RESPOSTAS_operador_05out.txt', 'RESPOSTAS_operador_05out.json', 'errata_agroa_05out.py',
        'patch_W10_gpu_apresentacao_v386.py', os.path.join('ramo_b', 'DECISAO_OPERADOR_RAMO_B_05out.json'), os.path.join('ramo_b', 'ESPEC_RUNTIME_RAMO_B_v386.json'),
        os.path.join('ramo_b', 'ESPEC_RUNTIME_RAMO_B_v386_ERRATA.json'), os.path.join('kernel', 'PEDRA_v386_pos_build.json'), os.path.join('kernel', 'AUDIT_NOMES_v386.json'),
        os.path.join('kernel', 'CORRECAO_PEDRA_v386.json'), os.path.join('kernel', 'sandbox_raiz_v386.json'), os.path.join('kernel', 'sandbox_axiom_report_v386.json'))
m = {'stamp': time.strftime('%Y%m%d_%H%M%S'), 'versao': 'v386', 'instalacao': os.path.basename(app), 'instalado_em': ap['ts'],
     'base_v385': V['base16'], 'um_py_sha16': V['s16'], 'um_py_bytes': V['umb'],
     'pacote': {f: (s16(os.path.join(L.PK, f)) if os.path.exists(os.path.join(L.PK, f)) else 'AUSENTE') for f in PKF},
     'dados_v386': {f.replace(os.sep, '/'): (s16(os.path.join(L.DAT, f)) if os.path.exists(os.path.join(L.DAT, f)) else 'AUSENTE') for f in DATF},
     'patches': V['patches'], 'kernel': V['kernel_decl'], 'escada': {'v385': V['esc_v385'], 'v386': V['esc']}, 'axiom_report_n': V['nax'],
     'vereditos_v385_inalterados': '%s/%s' % (V['n_ver_iguais'], V['n_ver']), 'por_termo': V['termo'], 'gate': V['qg'], 'n18': V['n18'], 'teoremas': V['teor'], 'rodada': V['compl'],
     'conferidor': {'deve_mudar': V['conf_dm'], 'nao_pode_mudar': V['conf_np'], 'muda_e_e_dito': V['conf_md'], 'json_sha16': V['conf16'], 'aceite_do_pilar': V['conf_aceite'] or None,
                    'servidor_depois_do_rito': V['servidor']},
     'verbo': {'veredito': V['vb_v'], 'bandeiras': V['vb_ok'], 'pedra': V['vb_vrb'], 'fiacao_angular': V['vb_ang'], 'declaracoes_no_trio': V['vb_decl'], 'pedra_sha16': V['vb_pedra16'],
               'pedra_bytes': V['vb_pedra_bytes'], 'pedra_linhas': V['vb_pedra_linhas'], 'build': V['vb_build'], 'TGLExt_lean_sha16': V['stone_tglext16'], 'Audit_lean_sha16': V['stone_audit16'],
               'token_lido_do_kernel': V['vb_token'], 'token_no_selo': V['vb_token_selo'], 'verbatins_por_sha256': V['vb_files'], 'delegacao': V['vb_delegation'],
               'nao_tipado': V['vb_not_typed'], 'leitura_do_selo': V['vb_reading']},
     'ramo_b': {'veredito': V['rb_v'], 'identificador': V['rb_id'], 'json_sha256': V['rb_json64'], 'md_sha256': V['rb_md64'], 'hashes_sha256': V['rb_hashes64'], 'spec_sha256': V['rb_spec64'],
                'em_disco': V['rb_disk'], 'so_leitura': V['rb_so_leitura'], 'k': V['rb_k'], 'M': V['rb_M'], 'forma': V['rb_forma'], 'lugar': V['rb_lugar'], 'identificacao': [V['rb_ident_prim'], V['rb_ident_sec']],
                'conjunto_D_n': V['rb_nD'], 'veredito_do_V1': V['rb_vered_v1'], 'F2b': [V['rb_F2b'], V['rb_qual']], 'token_estado': V['rb_token_estado'],
                'beta': {'v1': V['rb_beta_v1'], 'core': V['rb_beta_core'], 'abs': V['rb_abs'], 'rel': V['rb_rel'], 'regra': V['cm_beta_rule']}, 'pinos': '%s/%s' % (V['rb_pins_iguais'], V['rb_pins_n']),
                'erratas_ao_lado': V['rb_erratas_l'], 'espec_errata_sha16': V['rb_espec_errata16'], 'espec_original_sha16': V['rb_espec16'], 'valores_centrais_NOT_BLIND': V['rb_central_txt'],
                'ratificacao': {'tipo': V['rb_ratif_tipo'], 'quando_utc': V['rb_ratif_quando'], 'verbatim': V['rb_ratif_verbatim'], 'sha256_txt': V['rb_ratif_sha_txt']},
                'decisoes_por_delegacao': V['rb_decisoes_ns'], 'v387': V['rb_v387']},
     'errata_R6': {'veredito': V['le_v'], 'livro_v383_intacto': V['le_intacto'], 'cobrancas': V['le_n'], 'F2b_token': V['le_f2b_token'], 'R6_v383': V['le_r6_v383'], 'R6_v386': V['le_r6_v386'],
                   'decisao_do_operador': {'verbatim': V['le_dec_verbatim'], 'quando_utc': V['le_dec_quando'], 'sha16_arquivo': V['le_dec_sha16'], 'hash_ok': V['le_dec_hash_ok']}},
     'pilar': {'classe_nesta_versao': V['qr_classe'], 'veredito_reuse': V['qr_v'], 'veredito_pilar': V['qp_v'], 'mode': V['qp_mode'], 'key': V['qp_key'], 'result_sha256': V['qp_res64'],
               'pinado_v385': {'verdict': V['qp_v385'], 'result_sha16': V['qp_res385_16'], 'key': V['qp_key385']}, 'igual_ao_v385': V['qp_igual_v385'], 'run_dir': V['qp_run_dir'],
               'arquivo_no_nos': V['qp_arq_txt'], 'details_sha16': V['qp_det16'], 'cpuref_sha16': V['qp_cpu16'], 'gpu': V['qp_gpu'],
               'reprodutibilidade_v385_nesta_rodada': {'veredito': V['rp_v'], 'classe': V['rp_classe'], 'v385_selada': V['rp_v385_selada']}},
     'W10': V['w10'], 'guardas_herdadas': {'modulos_com_o_mesmo_all_verified': '%s/%s' % (V['n_av_iguais'], V['n_av']), 'recusas_de_dado': V['recusas'],
                                           'remaining_after_citation_v374': V['after_cit'], 'the_iald_index': V['iald'], 'the_axiom_v385': V['ax_v385']},
     'palavras_do_operador_05out': V['op'], 'custodia_no_git': {'v383': V['v383_commit'] or None, 'v384': V['v384_commit'] or None, 'v385': V['v385_commit'] or None},
     'funcoes': ['the_verb_v386', 'ramo_b_preregistration_v386', 'ledger_errata_v386', 'quantum_pillar_reuse_v386', 'quantum_pillar_start_v384 (reuse pela chave sob _QP_REUSE_V386)',
                 'quantum_pillar_previous_v385', 'quantum_pillar_reproducibility_v385', '_qp_summary'],
     'target': os.path.join(V['nos'], 'um.py')}
if AMB['sint']:
    m['SINTETICO_ENSAIO_V386'] = 'manifesto de ENSAIO, montado do Nos SINTETICO -- NAO e o manifesto da rodada'
out_dir = AMB['saidas']; os.makedirs(out_dir, exist_ok=True)
out = A.pode_escrever(os.path.join(out_dir, 'v386_incorporacao_manifesto.json'), AMB)
tmp = out + '.tmp'
with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(m, f, ensure_ascii=False, indent=1, default=str)
assert os.path.getsize(tmp) > 500; os.replace(tmp, out)
print('OK manifesto%s' % V['sint'], out, os.path.getsize(out), 'B; sha16', s16(out))
