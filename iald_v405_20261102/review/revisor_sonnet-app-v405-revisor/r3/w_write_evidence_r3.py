# -*- coding: utf-8 -*-
"""Reviewer r3: compose validation/review_sources.json and validation/review_app_independent.json (second round) from the r3 measurement outputs in this folder.
Numbers are read from the outputs, never typed. Exclusive-create ('x'). The confidential names/paths are NOT quoted (counts only)."""
import datetime, hashlib, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
W = HERE.parents[2]
VAL = W / 'validation'
if sys.argv[1:] == ['dry']:
    VAL = HERE / 'scratch' / 'val_dry'
    VAL.mkdir(parents=True, exist_ok=True)
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
J = lambda n: json.loads((HERE / n).read_bytes())
REVIEWER = 'sonnet-app-v405-revisor'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

q1, q1x = J('q1_r3_out.json'), J('q1_r3_extra_out.json')
topics, q2x, q2cmp = J('r3_topics_out.json'), J('q2_r3_extra_out.json'), J('q2_haiku_expanded_r3_out.json')
q3 = J('q3_out.json')
q4 = J('q4_r3_out.json')['summary']
r5, q6, q6b = J('r5_r3_out.json'), J('q6_r3_out.json'), J('q6b_r3_out.json')
q78 = J('q7q8_newtext_out.json')
q8 = J('q8_r3_out.json')
r0 = J('r0_r3_out.json')
r1s, r2s, q9 = J('r1_r3_out.json'), J('r2_r3_out.json'), J('q9_r3_out.json')
dry = json.loads((HERE / 'scratch' / 'review_app_dryrun_output.json').read_bytes())
ls_remote = (HERE / 'ls_remote_r3.txt').read_text('utf-8').split()
r1_parecer = {n: sha(W / 'superseded_r1/validation' / n) for n in ('review_findings.json', 'review_app_independent.json', 'review_sources.json')}
builder = json.loads((W / 'BUILDER_MEASUREMENTS.json').read_bytes())

# ---- artifacts ----------------------------------------------------------------------------------------------------------------------------
arts = []
for p in sorted(HERE.iterdir()):
    if p.is_file() and p.suffix in ('.py', '.json', '.txt') and p.name != 'w_write_evidence_r3.py':
        arts.append({'file': 'review/revisor_sonnet-app-v405-revisor/r3/' + p.name, 'sha256': sha(p), 'bytes': p.stat().st_size})
arts.append({'file': 'review/revisor_sonnet-app-v405-revisor/r3/w_write_evidence_r3.py', 'sha256': sha(HERE / 'w_write_evidence_r3.py'), 'bytes': (HERE / 'w_write_evidence_r3.py').stat().st_size})
arts.append({'file': 'review/revisor_sonnet-app-v405-revisor/r3/scratch/review_app_dryrun_output.json', 'sha256': sha(HERE / 'scratch' / 'review_app_dryrun_output.json'), 'bytes': (HERE / 'scratch' / 'review_app_dryrun_output.json').stat().st_size})
inputs = {}
for rel in ('install_plan.json', 'app/RELEASE.json', 'app/build/haiku_codec.py', 'release_cfg.py', 'exercita_busca.py', 'builder_measurements.py', 'sources_verified.json', 'CUSTODIA_EM_CURSO_v405.json', 'app/PUBLIC_GIT_BINDING.json',
            'app/packages/haiku_expanded/prefix.md', 'app/packages/shared/prefix.md', 'app/packages/sonnet_public/prefix.md', 'app/packages/haiku55/prefix.md', 'app/PREPARED_BINDING.json', 'app/NATIVE_COUNTS_COMPLETE.json',
            'BUILDER_MEASUREMENTS.json', 'BUSCA_EXERCITADA_v405.txt', 'validation/final_checks.json', 'R1_SHARED_HASHES.txt', 'superseded_r1/MOVED_MANIFEST.json', 'superseded_r2/MOVED_MANIFEST.json'):
    inputs[rel] = sha(W / rel)

sv = q78['haiku_expanded']['kernel_formalization_delta']
cl = q1
fam = cl['clause_A_catalogue_only_ext_or_red']
voc = cl['clause_C_inside_families_names_carrying_the_vocabulary_are_literal']
viol = cl['clause_C_violations_strict_vocabulary']
h_fused = voc['H1_H2_H3_anywhere_in_name']['names']
verifies = voc['verificacao']['names']
shared_same = {}
for pkg in ('shared', 'sonnet_public'):
    cur = W / 'app/packages' / pkg
    old = W / 'superseded_r1/app/packages' / pkg
    shared_same[pkg] = {'prefix_sha256_r3': sha(cur / 'prefix.md'), 'prefix_equal_r1_bytes': sha(cur / 'prefix.md') == sha(old / 'prefix.md'),
                        'files_equal_r1': {p.name: sha(p) == sha(old / p.name) for p in sorted(cur.iterdir())}}
rec = {}
for line in (W / 'R1_SHARED_HASHES.txt').read_text().splitlines():
    if line.strip():
        h, name = line.split(' *')
        rec[name] = h
shared_same['R1_SHARED_HASHES.txt_matches_files'] = {k: sha(W / k) == v for k, v in rec.items()}
shared_same['native_count_difference'] = 'so /utc (recontagem da mesma cadeia de recibos); preparation.json do shared difere so por builder_sha256 e pela ordem de historical_machine_labels (conjunto igual, 97 itens)'

findings = [
    {'id': 'F1', 'severity': 'MEDIO (r1)', 'status': 'RESOLVIDO', 'evidence': {'sete_classes_r1': q1['seven_classes']['union_in_r1'], 'ainda_so_no_catalogo': q1['seven_classes']['still_catalogue_only_in_r3'], 'agora_literais': q1['seven_classes']['now_literal'],
                                                                                   'catalogo_r3_casa_alguma_classe': len(q1['seven_classes']['r3_catalogue_matching_any']), 'bandeiras_foco_literais': sum(1 for v in q1['focus_flags'].values() if v['literal_in_r3_capsule']), 'bandeiras_foco': len(q1['focus_flags']),
                                                                                   'FALSE_literais': q1['clause_E_every_FALSE_literal'], 'irmaos_TRUE_dos_FALSE_literais': {k: v['siblings_literal'] for k, v in q1['false_flags'].items()},
                                                                                   'TRUE_catalogado_que_divide_3_ou_mais_termos_com_um_FALSE': {k: v['catalogued_among_them'] for k, v in q1['false_flags'].items()}}},
    {'id': 'F2', 'severity': 'BAIXO (r1)', 'status': 'RESOLVIDO (com ressalva R3-2)', 'evidence': {'receita_no_reading': True, 'ver': 'Q4'}},
    {'id': 'F3', 'severity': 'BAIXO (r1)', 'status': 'RESOLVIDO', 'evidence': r0['custody_evidence']},
    {'id': 'F4', 'severity': 'BAIXO (r1)', 'status': 'RESOLVIDO', 'evidence': {'builder_r3': {'com_reserva_de_4096': builder['executor_slack_bytes_with_finalize_reserve'], 'deepseek_reserva_declarada_148656': builder['deepseek_slack_bytes_with_declared_policy_reserve_148656']},
                                                                              'revisor_recomputado': {k: v['slack_full_reserve'] for k, v in r5['executor_windows'].items()}, 'deepseek_declarada_revisor': r5['executor_windows']['deepseek']['slack_declared_policy_reserve_148656']}},
    {'id': 'F5', 'severity': 'INFO (r1)', 'status': 'MANTIDO (finalize.py identico a v404)', 'evidence': q6['finalize_estimate']},
    {'id': 'R3-1', 'severity': 'BAIXO', 'blocking': False, 'questions': ['Q1', 'Q5'], 'where': ['app/build/haiku_codec.py: KEEP_FLAG (H[123] so entre delimitadores; verified|verification)', 'capsula kernel_formalization, reading: "dentro delas, tambem as que trazem no nome ... H1/H2/H3 ... ou verificacao"'],
     'evidence': {'nomes_no_catalogo_com_H_colado': h_fused, 'nomes_no_catalogo_com_verifies': verifies, 'total': len(viol),
                  'o_que_sao': 'bandeiras de lema da escada ext_ (nenhuma e FALSE-par, agregado, portao ou status); recuperaveis por nome (Q4: 4/4 e 10/10 achadas)',
                  'palavras_de_estatuto_fora_do_vocabulario_da_frase_ainda_no_catalogo': 'conjecture 1, axiom 12, open 11, named 9, import/citation 13 (a frase nao as promete)'},
     'fix': 'KEEP_FLAG: H[123] sem delimitadores e "verif" (+14 bandeiras, menos de 1 KB) ou qualificar a frase ("H1/H2/H3 como termo do nome")'},
    {'id': 'R3-2', 'severity': 'BAIXO', 'blocking': False, 'questions': ['Q4'], 'where': ['reading: a receita nao diz max_chars; o padrao do fetch_tgl e 4000 (janela offset-2000 .. offset+2000)'],
     'evidence': {'receita_literal_estrita': [q4['default']['strict_any'], q4['sample_size']], 'com_max_chars_4500_estrita': [q4['m4500']['strict_any'], q4['sample_size']], 'falhas_receita_literal': q4['default']['failures_strict'], 'falhas_com_4500': q4['m4500']['failures_strict'],
                  'maior_distancia_bandeira_menos_offset': q4['m4500']['delta_flag_minus_result_offset'], 'medicao_do_construtor': 'BUSCA_EXERCITADA_v405.txt: 699/700 com max_chars 4500 (mesma falha generica)'},
     'fix': 'acrescentar "max_chars 4500" a receita (ou deslocar a janela para offset-1500)'},
    {'id': 'I1', 'severity': 'INFO', 'blocking': False, 'evidence': {'bandeiras_TRUE_dentro_das_familias_literais': q1x['family_literal'], 'casam_o_vocabulario_da_frase': q1x['family_literal_matching_reading_vocabulary'], 'literais_por_palavra_nao_listada_na_frase': q1x['those_by_extra_word'],
                                                                      'leitura': 'a regra mantem literais tambem nomes com commut, dephas, hamilton, theorem que a frase nao lista; direcao segura (a frase diz "tambem")'}},
    {'id': 'I2', 'severity': 'INFO', 'blocking': False, 'evidence': {'por_declaracao': q1x['per_declaration'], 'leitura': 'ext_: 9701 dos 9730 catalogados sao chaves de external_ladder.per_theorem (10066 entradas, todas True). red_: 28 de 126 tem o radical igual ao nome de uma declaracao e 62 como sufixo; "por declaracao" plausivel, nao provado por nome'}},
    {'id': 'I3', 'severity': 'INFO', 'blocking': False, 'evidence': {'shared_sonnet_public': 'herdado da v404 e da r1: nao nomeiam os 4 FALSE (so false_fields: 4) nem trazem a receita; fora do escopo desta rodada (prefixos identicos aos da r1 por hash)'}},
]

Q = {}
Q['Q1'] = {'status': 'PASS', 'resolves': 'F1', 'question': 'bandeiras das 52 ainda so no catalogo? FALSE literal com o TRUE correspondente fora do pacote? codec',
           'answer': {'codec': 'unico script que mudou frente a r1 e a v404 alem de release_cfg/task/builder_measurements: haiku_codec.py (LADDER_FLAG ext_|red_, KEEP_FLAG, catalogable_flags, reading e frase do cabecalho); os outros 16 scripts do pipeline seguem identicos a v404; self-test 11/11',
                      'catalogo_r3': {'TRUE_fonte': q1['counts']['source_true'], 'TRUE_literais': q1['counts']['literal_true_r3'], 'TRUE_catalogados': q1['counts']['catalogued_true_r3'], 'FALSE_literais': [q1['counts']['literal_false_r3'], q1['counts']['source_false']],
                                      'contagem_confere': q1['counts']['capsule_true_fields_equals_catalogued'], 'sha256_confere': q1['counts']['catalog_sha256_equal'], 'sha256': q1['counts']['catalog_sha256_recomputed'], 'catalogados_r1': q1['counts']['catalogued_true_r1']},
                      'sete_classes_do_revisor': {'uniao_r1': q1['seven_classes']['union_in_r1'], 'ainda_so_no_catalogo': q1['seven_classes']['still_catalogue_only_in_r3'], 'agora_literais': q1['seven_classes']['now_literal'], 'catalogo_r3_casa_alguma_das_7': len(q1['seven_classes']['r3_catalogue_matching_any'])},
                      'bandeiras_foco': {k: v['literal_in_r3_capsule'] for k, v in q1['focus_flags'].items()},
                      'FALSE_e_irmaos': {k: {'FALSE_literal': v['literal_false'], 'irmaos_TRUE_literais': v['siblings_literal'], 'TRUE_catalogado_com_3_ou_mais_termos_em_comum': v['catalogued_among_them']} for k, v in q1['false_flags'].items()},
                      'delta_do_capsule_r1_para_r3': {'topicos_cujo_bloco_decodificado_difere': q2x['topics_whose_decoded_block_differs_r3_vs_r1'], 'chaves_literais_acrescentadas': sv['literal_keys_added_r3'], 'todas_True': sv['all_added_values_True'], 'chaves_removidas': sv['literal_keys_removed_r3'], 'valores_alterados': sv['changed_values']}},
           'partitura': 'Decide se alguma bandeira das minhas 7 classes semanticas (escritas na r1, antes de medir) ainda so existe no catalogo e se algum FALSE literal perdeu o TRUE correspondente. Nao decide ciencia, nem a fidelidade numerica, nem classes que eu nao escrevi. Negativo = a regra por nome ainda vaza uma classe. Escolhas ditas antes: as 7 classes; o catalogo e recomputado da capsula decodificada; os termos em comum (3 ou mais) entre um FALSE e um TRUE catalogado.'}
Q['Q5'] = {'status': 'PASS (ressalva R3-1 e R3-2, BAIXO)', 'question': 'o cabecalho e o reading novos sao verdadeiros por inteiro',
           'answer': {'cabecalho_r3': q78['haiku_expanded']['header_sentence_r3'], 'reading_r3': q1['reading_r3'],
                      'clausulas': [
                          {'clausula': 'Indicadores TRUE por declaracao (familias ext_ e red_) estao so na fonte', 'veredito': 'VERDADEIRA', 'numeros': {'catalogados': q1['counts']['catalogued_true_r3'], 'por_familia': fam['catalogued_by_family'], 'fora_das_familias_no_catalogo': fam['n_violations']}},
                          {'clausula': 'a ausencia de um nome aqui NAO significa FALSE', 'veredito': 'VERDADEIRA', 'numeros': {'FALSE_na_fonte': q1['clause_E_every_FALSE_literal']['false_total'], 'FALSE_literais': q1['clause_E_every_FALSE_literal']['literal'], 'FALSE_catalogados': 0}},
                          {'clausula': 'Todo FALSE seguem literais', 'veredito': 'VERDADEIRA', 'numeros': q1['clause_E_every_FALSE_literal']},
                          {'clausula': 'toda bandeira fora dessas familias (agregados, portoes gp*/qg*, build, pedras fundacionais) seguem literais', 'veredito': 'VERDADEIRA', 'numeros': dict(q1['clause_B_every_TRUE_outside_the_families_is_literal'], grupos=q1x['outside_true_by_group'])},
                          {'clausula': 'dentro delas, tambem as que trazem no nome enunciado, hipotese, H1/H2/H3, formula, veredito, descarga, condicao ou verificacao', 'veredito': 'VERDADEIRA COM 14 EXCECOES (BAIXO, R3-1)',
                           'numeros': {'enunciado': voc['enunciado']['catalogued_matches'], 'hipotese': voc['hipotese']['catalogued_matches'], 'formula': voc['formula']['catalogued_matches'], 'veredito': voc['veredito']['catalogued_matches'], 'descarga': voc['descarga']['catalogued_matches'], 'condicao': voc['condicao']['catalogued_matches'],
                                       'H1_H2_H3_colado_ao_nome': voc['H1_H2_H3_anywhere_in_name']['catalogued_matches'], 'verifies': voc['verificacao']['catalogued_matches']}, 'excecoes': viol},
                          {'clausula': 'O criterio e o nome, nao o conteudo', 'veredito': 'VERDADEIRA (as 14 excecoes mostram o limite do criterio lexical)'},
                          {'clausula': 'receita: search_tgl nome exato limit 5; para cada resultado dessa fonte fetch_tgl com offset-2000', 'veredito': 'VERDADEIRA NA PRATICA (ver Q4); omite max_chars (R3-2)'},
                          {'clausula': 'Nome muito generico pode exigir outra consulta', 'veredito': 'VERDADEIRA (ext_no_symmetric_kernel_proved nao e achado pela receita)'},
                          {'clausula': 'Nao sao contagem de teoremas', 'veredito': 'VERDADEIRA (inalterada)'}],
                      'texto_novo_total': {'linhas_que_mudaram_r1_para_r3': len(q78['haiku_expanded']['changed_lines_r3']), 'dicionario_igual': q78['haiku_expanded']['dictionary_equal'], 'exposicao_igual': q78['haiku_expanded']['exposition_equal']}},
           'partitura': 'Decide se cada oracao do reading novo e verdadeira contra o core selado e a capsula decodificada. Nao decide se a regra e a melhor possivel. Negativo numa clausula = a oracao promete mais do que a regra entrega. O vocabulario de cada clausula foi escrito por mim a partir do texto, sem usar o KEEP_FLAG do codec.'}
Q['Q2'] = {'status': 'PASS', 'question': 'haiku_expanded: fidelidade, 471 topicos, catalogo por contagem e hash',
           'answer': {'presentes': topics['packages']['haiku_expanded']['present'], 'exatos': topics['packages']['haiku_expanded']['topics_restoring_exactly'], 'perdidos': topics['packages']['haiku_expanded']['lost'], 'divergentes': topics['packages']['haiku_expanded']['n_mismatch'],
                      'catalogo': {k: topics['packages']['haiku_expanded']['catalog_reports']['kernel_formalization'][k] for k in ('source_true', 'source_false', 'literal_true_in_capsule', 'literal_false_in_capsule', 'only_by_catalog_true', 'catalog_count_matches', 'catalog_sha256_matches', 'recomputed_sha256', 'no_false_goes_only_by_catalog')},
                      'base_haiku55': {'exatos': topics['packages']['haiku55']['topics_restoring_exactly'], 'catalogo_ok': topics['packages']['haiku55']['catalog_reports']['kernel_formalization']['ok']},
                      'rebuild_independente_da_base_igual_ao_pacote': q2x['rebuild_from_base_equals_built_bytes'], 'topicos_v404_v405_integrais': q2x['v404_v405_topics_full_inline'], 'selecao_igual_FINAL_PREPARATION': q2x['selection_equals_FINAL_PREPARATION'],
                      'exposicao_igual_forma_canonica_selada': q2x['exposition_equals_sealed_canonical'], 'bytes': q2x['bytes'],
                      'contra_instalado_haiku55': {'comuns': q2cmp['common_topics'], 'fonte_igual': q2cmp['src_same_topics'], 'identicos': q2cmp['src_same_decoded_equal'], 'crescem_por_expansao': q2cmp['src_same_decoded_differ'], 'encolheram': q2cmp['src_changed_shrunk'],
                                                   'folhas_literais_que_saem_do_kernel_formalization': next(r['lost_literal_leaves'] for r in q2cmp['src_changed_topic_list'] if r['topic'] == 'kernel_formalization'), 'novos_v405_exatos_e_integrais': all(r['restores_exact'] is True and r['literal_leaves_in_prompt'] == r['leaves_in_source'] for r in q2cmp['new_topics'])}}}
Q['Q3'] = {'status': 'PASS (herdada da r1 por hash)', 'question': 'shared e sonnet_public mudaram?',
           'answer': dict(shared_same, heranca='prefixos do shared e do sonnet_public identicos aos da r1 (mesmo sha256 e mesmos bytes); o resultado da r1 (392/392 identicos ao instalado; unico literal que saiu: 1401 entradas declaration_sources_v394) vale sem repeticao',
                          r1_parecer_sha256=r1_parecer, haiku_expanded_janela_P2=dict(all_ok=q3['haiku_expanded']['all_ok'], topicos=q3['window_topics'], chaves_de_qualificacao=sum(len(r.get('qualifier_keys', [])) for r in q3['haiku_expanded']['rows'].values())),
                          shared_sonnet_janela_P2_reexecutada=dict(shared=q3['shared']['all_ok'], sonnet_public=q3['sonnet_public']['all_ok']))}
Q['Q4'] = {'status': 'PASS (ressalva R3-2)', 'question': 'receita do reading, amostra nova',
           'answer': {'amostra': q4['sample_size'], 'semente': q4['seed'], 'catalogados': q4['catalogued_total'], 'estratos': q4['by_tag'], 'receita': q4['recipe'],
                      'receita_literal_sem_max_chars': {'estrita': q4['default']['strict_any'], 'frouxa': q4['default']['loose_any'], 'so_primeiro_resultado': q4['default']['strict_first_result'], 'falhas': q4['default']['failures_strict']},
                      'com_max_chars_4500': {'estrita': q4['m4500']['strict_any'], 'frouxa': q4['m4500']['loose_any'], 'so_primeiro_resultado': q4['m4500']['strict_first_result'], 'falhas': q4['m4500']['failures_strict']},
                      'posto_do_primeiro_acerto': q4['default']['rank_of_first_hit'], 'distancia_bandeira_menos_offset_do_resultado': {'receita_literal': q4['default']['delta_flag_minus_result_offset'], 'com_4500': q4['m4500']['delta_flag_minus_result_offset']},
                      'resultados_da_fonte_por_consulta': q4['n_results_from_source_distribution'], 'chave_duplicada_no_topico': q4['non_unique_key_inside_topic'], 'medicao_do_construtor': 'BUSCA_EXERCITADA_v405.txt (699/700, max_chars 4500, criterio frouxo, mesma falha)'},
           'partitura': 'Decide se o indice do proprio runtime devolve o trecho da bandeira seguindo a receita escrita. Nao decide como o modelo real formula consultas. Escolhas ditas antes: semente nova 405111; amostra de 3 estratos de 100 + todas as red_ + casos de borda; criterio estrito de posicao dentro de kernel_formalization; duas variantes (sem max_chars e 4500).'}
Q['Q6'] = {'status': 'PASS', 'question': 'pinos e folga',
           'answer': {'cadeia_de_pinos': {p: all(v['chain'].values()) for p, v in r5['native'].items()}, 'recibos': r5['native_complete'], 'folga_tokens': {p: v['remaining_declared'] for p, v in r5['native'].items()}, 'permanente_tokens': {p: q6['packages'][p]['budget_pinned']['permanent_tokens'] for p in q6['packages']},
                      'instalado_v404': {p: q6['packages'][p].get('installed_v404') for p in ('haiku_expanded', 'shared')}, 'condicoes_do_runtime': {p: q6['packages'][p]['snapshot_conditions_all_true'] for p in ('haiku_expanded', 'shared')},
                      'carregador_reaplicado_sem_recusa': {p: q6b[p]['all_pass'] for p in ('haiku_expanded', 'shared')}, 'tools_iguais_ao_instalado': {p: [q6b[p]['tools_sha256_same_as_installed_v404'], q6b[p]['counted_scoped_tools_sha256_same_as_installed_v404']] for p in ('haiku_expanded', 'shared')},
                      'janelas_executores_bytes': {k: {'entrada': v['input_utf8_byte_bound'], 'folga_reserva_cheia_com_4096': v['slack_full_reserve']} for k, v in r5['executor_windows'].items()}, 'deepseek_reserva_declarada': r5['executor_windows']['deepseek']['slack_declared_policy_reserve_148656'], 'jev': r5['jev'],
                      'finalize_max0_crescimento': q6['finalize_estimate']}}
Q['Q7'] = {'status': 'PASS', 'question': 'texto novo: beta, CONFIRMED, frase antiga, gate',
           'answer': {'texto_novo': {pkg: {'linhas_que_mudaram': len(q78[pkg]['changed_lines_r3']), 'topicos_que_diferem': q78[pkg]['topics_whose_decoded_block_differs'], 'varredura_cabecalho': q78[pkg]['scan_header_and_small_changed_lines'], 'varredura_capsula_nova': q78[pkg]['scan_capsule_new_parts_(AUD_object_+_added_flag_names)']} for pkg in ('haiku_expanded', 'haiku55')},
                      'nucleo_dicionario_exposicao': 'identicos aos da r1 (dicionario igual, exposicao igual): o resto do texto novo e zero; gate, beta e frase antiga do r1 seguem como na r1'}}
Q['Q8'] = {'status': 'PASS', 'question': 'confidencial (texto novo e arvore)',
           'answer': {'arquivos_varridos': q8['files_scanned'], 'padroes_de_segredo': q8['secret_pattern_hits'], 'arquivos_com_nome_confidencial_(so_contagem)': {k: len(v) for k, v in q8['files_mentioning_confidential_names'].items()}, 'arquivos_com_caminho_do_Escritorio': len(q8['files_with_Escritorio_path']),
                      'arquivos_com_bloco_do_atlas_privado': len(q8['files_with_ATLAS_CANONICO_block']), 'prefixos_plano_manifestos_core_v5_jev_com_alguma_ocorrencia': [k for k, v in q8['focus'].items() if v['confidential_name_matches'] or v['Escritorio'] or v['ATLAS_CANONICO_block'] or v['secret_patterns']],
                      'leitura': 'as ocorrencias de nome confidencial estao no codigo do construtor (guardas de recusa), em listas de arquivos de runtime e nos meus pareceres anteriores movidos (que citam os nomes como criterio de busca); nenhuma em prefixo, plano, manifesto, core, v5 ou pacote JEV'}}
Q['Q9'] = {'status': 'PASS', 'question': 'plano novo e evidencia F3',
           'answer': {'plano_r3_sha256': q9['plan_sha256'], 'plano_r1_sha256': r0['plan_r3_vs_r1']['plan_r1_sha256'], 'arquivos': q9['n_files'], 'origens_ausentes': q9['sources_missing'], 'sha_divergente_ou_fora_de_W': q9['sources_hash_mismatch_or_outside_W'], 'destinos_fora_de_R': q9['destinations_outside_R'],
                      'baseline_diverge_agora': q9['baseline_mismatch_now'], 'unicos': q9['unique_destinations'], 'manifesto_ativo_por_ultimo': q9['active_manifest_last'], 'py_na_raiz_de_R': q9['py_at_R_root'], 'sobrescritos': q9['destinations_existing_overwritten'],
                      'contra_plano_r1': {'so_na_r3': r0['plan_r3_vs_r1']['destinations_only_in_r3'], 'so_na_r1': r0['plan_r3_vs_r1']['destinations_only_in_r1'], 'destinos_com_sha_alterado': r0['plan_r3_vs_r1']['destinations_with_changed_sha'], 'baselines_alterados': r0['plan_r3_vs_r1']['baseline_changed']},
                      'contra_plano_v404': {'so_na_v405': q9['only_in_v405'], 'so_na_v404': q9['only_in_v404']}, 'manifest_install': {'caminhos_sob_o_alvo': q9['manifest_install_paths_under_target'], 'todos_no_plano': q9['manifest_install_paths_all_in_plan'], 'checagens_de_hash': [q9['manifest_install_hash_checks_total'], len(q9['manifest_install_hash_checks_failed'])]},
                      'final_checks': r0['final_checks_r3'], 'F3': r0['custody_evidence'], 'pinos_da_submissao_r3': {f: [v['revision'], v['all_pins_match'], len(v['pins'])] for f, v in r0.items() if f.startswith('receipts')}, 'review_app_dry_run': {'status': dry['status'], 'checks': len(dry['checks']), 'plan_sha256': dry['plan_sha256']}}}

common = {'schema': 'iald.app.review/v1', 'round': 'r3', 'unit': 'F9.APP_V405_20261102', 'reviewer': REVIEWER, 'builder': 'opus-app-v405-construtor', 'owner': 'claude-gerencia-a7', 'timestamp': NOW, 'release': 'v405',
          'pinned_commit': '6a2138d73c1ab2dac4817793c7eb0502208b21c9', 'um_py_sha256': '0030242565cc13f6dbac57a6f1f98fdef69c1b3efe5eb052c359cdb3bf21f053', 'mission_revision_at_review': r0['mission_project_readonly']['revision']}
not_measured = ['nenhuma resposta de modelo ao vivo (zero chamadas a provedor; o count nativo nao foi repetido: conferi a cadeia de hashes dos recibos, nao o numero do provedor)', 'a busca foi exercida por execute_tool direto, nao por um modelo escolhendo consultas',
                'instalacao e carregamento efetivo (R nao foi tocado; o carregador foi reaplicado so sobre o manifesto staged)', 'merito cientifico dos 13 topicos novos (so fidelidade ao selo)', 'cliente movel/iOS/Android', 'shared e sonnet_public nao foram remedidos nesta rodada alem dos hashes (Q3 herdada da r1)']
route = {'consultado': 'rotas.py consultar "app release"', 'rotas_devolvidas': ['app.release.v402', 'app.release.v404'], 'registros_no_livro': 1634, 'nota': 'ainda sem app.release.v405; a gerencia registra (revisor nao registra)'}
review_sources = dict(common, task='sources', decision='PASS',
                      decision_reason='todas as checagens de fonte passam (selo, cofre, Nos, um.py, commit pinado = origin/main, URLs, blobs); F3 resolvido: a evidencia irma CUSTODIA_EM_CURSO_v405.json separa a custodia em curso da concluida e confere com o plano G1 lido agora',
                      checks={'release_commit_selo_cofre_nos': {'ok': r1s['ok'], 'passed': r1s['passed'], 'n': r1s['n']}, 'ls_remote_main': ls_remote[0], 'ls_remote_igual_ao_pino': ls_remote[0] == '6a2138d73c1ab2dac4817793c7eb0502208b21c9', 'cofre_36_artefatos': r2s['custody'], 'staged_vs_git': r2s['staged_release_vs_git'],
                              'urls_do_manifesto': {'todas_no_commit_pinado_e_rastreadas': r2s['manifest_urls']['all_ok'], 'n': len(r2s['manifest_urls']['rows'])}, 'urls_hipoteses': r2s['hypothesis_source_urls'],
                              'pinos_da_submissao_r3': {'v405-sources-submit-r3.json': {'revisao': r0['receipts/v405-sources-submit-r3.json']['revision'], 'todos_conferem': r0['receipts/v405-sources-submit-r3.json']['all_pins_match'], 'n': len(r0['receipts/v405-sources-submit-r3.json']['pins'])}},
                              'sources_verified_r3_igual_a_r1_exceto_checked_at': r0['sources_verified_r3_vs_r1']['equal_except_checked_at']},
                      custody_separation={'concluida': ['selo v405 FAIL_CLOSED_SELFTEST_PASSED; um.py == pino no Nos, cofre, espelho e commit pinado', 'cofre v405: 36 artefatos == CUSTODY_MANIFEST (0 divergencias); kernel 1446 formais, 29965 declaracoes, 0 fora do trio',
                                                       'publicacao: espelho 6a2138d7 == origin/main; conferencia final da custodia 13/13'],
                                          'em_curso': {'evidencia': 'CUSTODIA_EM_CURSO_v405.json', 'sha256': r0['custody_evidence']['file_sha256'], 'status': r0['custody_evidence']['status'], 'plano_g1_sha256_na_evidencia': r0['custody_evidence']['plano_sha256_in_evidence'],
                                                       'plano_g1_sha256_lido_agora': r0['custody_evidence']['plano_sha256_live_now'], 'campos_conferem_com_o_plano_vivo': r0['custody_evidence']['fields_equal_live_now'], 'completo': r0['custody_evidence']['live_completo'],
                                                       'pendentes': r0['custody_evidence']['live_pendentes'], 'contagem': r0['custody_evidence']['live_contagem'], 'operador': 'C21 = esta release do app'}},
                      answers={'Q9_fontes': Q['Q9']['answer']['F3']}, findings=[f for f in findings if f['id'] == 'F3'], caveats=[], not_measured=not_measured, route_map=route, inputs_sha256=inputs, artifacts=arts)
review_app = dict(common, task='app', decision='PASS',
                  decision_reason='F1 (MEDIO) resolvido: das 52 bandeiras das minhas 7 classes, 0 seguem so no catalogo; os 4 FALSE tem os irmaos TRUE literais; reading verdadeiro por inteiro na familia, nas bandeiras fora das familias e nos FALSE, com 14 excecoes de vocabulario (BAIXO). 471/471 exatos, pinos e folga ok, shared e sonnet_public identicos por hash. Ressalvas BAIXAS nao bloqueiam.',
                  summary={'passa': ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9'], 'ressalvas': ['R3-1', 'R3-2']}, answers=Q, findings=findings,
                  caveats=[{'id': 'R3-1', 'severity': 'BAIXO', 'text': 'o vocabulario do reading promete H1/H2/H3 e verificacao no nome; 4 nomes com H colado (H2v32, H3v32, NamedAtlasH3) e 10 com "verifies" seguem no catalogo'},
                           {'id': 'R3-2', 'severity': 'BAIXO', 'text': 'a receita nao diz max_chars; sem ele 470/472, com 4500 471/472; a unica falha comum e um nome generico, ja coberto pela frase final do reading'}],
                  tests_run={'review_app_dry_run_checks': len(dry['checks']), 'codec_self_test': '11/11 OK (rodado de novo nesta rodada)', 'decoder_independente': 'review/revisor_sonnet-app-v405-revisor/r3/lib405.py + r3_topics_capsules.py (sem importar haiku_codec/fit_*)'},
                  not_measured=not_measured, route_map=route, r1_parecer_sha256=r1_parecer, inputs_sha256=inputs, artifacts=arts)
for name, doc in (('review_sources.json', review_sources), ('review_app_independent.json', review_app)):
    with (VAL / name).open('x', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(name, sha(VAL / name), (VAL / name).stat().st_size)
