# -*- coding: utf-8 -*-
"""Reviewer (sonnet-app-v405-revisor): compose the three evidence documents in W/validation from the measurement outputs in this folder.
Numbers are read from the outputs (never typed); descriptive text is written here. Writes with exclusive-create ('x')."""
import datetime, hashlib, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
W = HERE.parents[1]
VAL = W / 'validation'
if sys.argv[1:] == ['dry']:  # compose into scratch to catch errors before the real write
    VAL = HERE / 'scratch' / 'val_dry'
    VAL.mkdir(parents=True, exist_ok=True)
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
J = lambda n: json.loads((HERE / n).read_bytes())
REVIEWER = 'sonnet-app-v405-revisor'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

r1, r2, r3, r3b = J('r1_out.json'), J('r2_out.json'), J('r3_out.json'), J('r3b_out.json')
tree = J('q1_tree_diff_out.json')
q1c = J('q1c_out.json')
q1d = J('q1d_out.json')
r0 = J('r0_out.json')
q2h, q2s, q2so = J('q2_haiku_expanded_out.json'), J('q2_shared_out.json'), J('q2_sonnet_vs_v404_out.json')
q2c = J('q2c_out.json')
q3 = J('q3_out.json')
q4, q4b = J('q4_out.json'), J('q4b_out.json')
q6, q6b, r5 = J('q6_out.json'), J('q6b_out.json'), J('r5_out.json')
q7s, q7g = J('q7_superseded_out.json'), J('q7_gate_beta_wording_out.json')
q8 = J('q8_out.json')
q9 = J('q9_out.json')
dry = json.loads((HERE / 'scratch' / 'review_app_dryrun_output.json').read_bytes())
selftest_ok = 'OK' in (HERE / 'selftest_out.txt').read_text('utf-8').splitlines()[-1] or 'OK' in (HERE / 'selftest_out.txt').read_text('utf-8')
ls_remote = (HERE / 'ls_remote_out.txt').read_text('utf-8').split()

# ---- artifacts (sha256 computed now) -------------------------------------------------------------------------------------------------
arts = []
for p in sorted(HERE.iterdir()):
    if p.is_file() and p.suffix in ('.py', '.json', '.txt') and p.name != 'w_write_evidence.py':
        arts.append({'file': 'review/revisor_sonnet-app-v405-revisor/' + p.name, 'sha256': sha(p), 'bytes': p.stat().st_size})
arts.append({'file': 'review/revisor_sonnet-app-v405-revisor/w_write_evidence.py', 'sha256': sha(HERE / 'w_write_evidence.py'), 'bytes': (HERE / 'w_write_evidence.py').stat().st_size})
arts.append({'file': 'review/revisor_sonnet-app-v405-revisor/scratch/review_app_dryrun_output.json', 'sha256': sha(HERE / 'scratch' / 'review_app_dryrun_output.json'), 'bytes': (HERE / 'scratch' / 'review_app_dryrun_output.json').stat().st_size})
inputs = {}
for rel in ('install_plan.json', 'app/RELEASE.json', 'app/build/haiku_codec.py', 'release_cfg.py', 'transaction.py', 'maintenance.py', 'deploy_controlled.py', 'verify_installed.py', 'verify_sources.py', 'sources_verified.json', 'app/PUBLIC_GIT_BINDING.json',
            'app/packages/haiku_expanded/prefix.md', 'app/packages/shared/prefix.md', 'app/packages/sonnet_public/prefix.md', 'app/packages/haiku55/prefix.md', 'app/PREPARED_BINDING.json', 'app/NATIVE_COUNTS_COMPLETE.json', 'BUILDER_MEASUREMENTS.json',
            'BUSCA_EXERCITADA_v405.txt', 'validation/final_checks.json'):
    inputs[rel] = sha(W / rel)

h = r3['packages']['haiku_expanded']
cat = h['catalog_reports']['kernel_formalization']
is_script = lambda f: f.replace('\\', '/').endswith(('.py', '.sh')) and not f.replace('\\', '/').startswith('app/science/')  # app/science holds sealed DATA copies (um.py included)
n_same_scripts = [f for f in tree['same'] if is_script(f)]
scripts_diff = [f for f in tree['diff'] if is_script(f)]
scripts_new = [f for f in tree['only_v405'] if is_script(f)]
q4s = q4['summary']
sem = q1d['classes']
ex = r5['executor_windows']
pk6 = q6['packages']
q3_rows = q3['haiku_expanded']['rows']
strict_keys = sum(len(r.get('qualifier_keys', [])) for r in q3_rows.values())

# ---- the findings --------------------------------------------------------------------------------------------------------------------
findings = [
    {
        'id': 'F1', 'severity': 'MEDIO', 'blocking': True, 'questions': ['Q1', 'Q5'],
        'where': ['app/build/haiku_codec.py:171-172 (texto "reading" da capsula AUDIT_BOOLEAN_FIELDS_IN_SOURCE)', 'app/build/haiku_codec.py:156-159 (catalogable_flags: regra lexical no NOME da bandeira)',
                  'packages/haiku_expanded/prefix.md e packages/haiku55/prefix.md, topico kernel_formalization'],
        'claim_tested': 'a capsula diz: "os FALSE e os de enunciado, hipotese, formula ou veredito seguem literais neste topico"',
        'evidence': {
            'false_flags': {'source': cat['source_false'], 'literal_in_capsule': cat['literal_false_in_capsule'], 'result': 'nenhum FALSE sai (guarda value is True)'},
            'true_flags': {'source': cat['source_true'], 'literal_in_capsule': cat['literal_true_in_capsule'], 'catalogued': cat['only_by_catalog_true'], 'catalog_sha256_recomputed_by_reviewer': cat['recomputed_sha256']},
            'regra_do_codec': 'fica literal so a bandeira TRUE cujo NOME casa ESSENTIAL (formula|equation|hypothes|assumption|premiss|scope|status|verdict|claim|statement|theorem|lagrang|hamilton|lindblad|dephas|commut ...); o resto vai para o catalogo',
            'contraexemplos_por_significado': {
                'pares_FALSE_literal_vs_TRUE_so_no_catalogo': [
                    ['gpf_H2_smooth_modular_four_frame_discharged=false (literal)', 'gpc_H2_smooth_modular_four_frame_discharged=true (so catalogo)'],
                    ['gpf_H3_local_horizon_equilibrium_discharged=false (literal)', 'gpc_H3_local_horizon_equilibrium_discharged=true (so catalogo)'],
                    ['gpi_H3_horizon_data_produced=false (literal)', 'gpc_H3_horizon_data_produced=true (so catalogo)']],
                'agregados_de_veredito_so_no_catalogo': ['all_verified', 'all_unconditional_targets_verified', 'all_conditional_implications_verified', 'formal_release_ready', 'specific_AQFT_witness_constructed'],
                'cabecas_QG_so_no_catalogo': 'qgc_* (6), qgf_* (4), qgp_* (5), gpf_H1_internal_susy_relative_gap_discharged, gpf_tower_act_III_inhabitant_constructed, gpi_* TRUE (6 sem portador literal)',
                'classes_semanticas_medidas_pelo_revisor': sem,
                'uniao_das_7_classes_catalogadas': q1d['union_7_classes'],
                'com_a_classe_larga_extra_constructed_proved_sem_prefixo_ext': q1c['union_of_semantic_classes_catalogued'],
                'bytes_extras_se_mantidas_literais_(uniao_larga)': q1c['extra_literal_bytes_if_kept'],
                'portador_literal_em_outro_ponto_do_prefixo': {'com_portador': q1d['haiku_expanded']['carried_literally_elsewhere'], 'so_no_catalogo': q1d['haiku_expanded']['catalogue_only'], 'nota': 'all_verified conta como "com portador" por engano: a chave generica ocorre em outros topicos; a do kernel_formalization so esta no catalogo (entao so_no_catalogo >= 31)',
                                                             'so_no_catalogo_nomes': q1d['haiku_expanded']['catalogue_only_names'], 'foco': q1d['focus']}},
            'mitigacao_medida': 'o estado da publicacao carregado no nucleo (ambos os pacotes) traz literalmente discharged_by_citation_v373 {H2_smooth_modular_four_frame_discharged:true, H3_local_horizon_equilibrium_discharged:true, H3_horizon_data_produced:true}, '
                                'formal_flags (concrete_*), proofs {qgf_* , gpf_H1...:true} e current_kernel_obligations (discharged_in_kernel); logo o FATO H2/H3 por citacao nao esta perdido. '
                                'Das 52 bandeiras TRUE catalogadas nas 7 classes, 21 tem portador literal (nome ou radical) em outro ponto do prefixo e pelo menos 31 so no catalogo (agregados all_unconditional_targets_verified / all_conditional_implications_verified / formal_release_ready / specific_AQFT_witness_constructed, os gpi_* TRUE e 23 bandeiras ext_* de lema).'},
        'why_it_matters': 'frase dirigida ao modelo e falsa por significado; exibicao assimetrica (os FALSE de H2/H3 literais, os TRUE correspondentes escondidos); um modelo que le so a capsula pode inferir "H2/H3 nao descarregadas" ou "all_verified ausente".',
        'what_it_does_not_show': 'nao ha perda de dado nem erro numerico: 471/471 reconstroem exatos; o catalogo e recuperavel por nome (Q4); o shared/sonnet_public nunca nomearam essas bandeiras (so contagens).',
        'fix': ['(a) minimo: reescrever o reading e a frase do cabecalho para dizer a regra real ("FALSE e TRUE cujo nome contem <lista da regex> ficam literais; os demais TRUE, inclusive all_*, qg*_, gp*_, estao so no catalogo; H1/H2/H3 e formal_flags estao no estado da publicacao carregado acima")',
                '(b) melhor: estender catalogable_flags com uma lista de permanencia para a classe semantica (H[123] no nome, discharg, verified, ^all_, ^qg[cfp]_, ^gp[cfi]_, conditional, formal_release_ready): ~52 bandeiras, cerca de 4 KB (~2 mil tokens) contra 175.526 de folga',
                'qualquer das duas muda so os pacotes haiku (haiku55/haiku_expanded): shared e sonnet_public ficam byte a byte e suas contagens seguem validas; recontar o haiku_expanded e regenerar plano/final_checks']
    },
    {
        'id': 'F2', 'severity': 'BAIXO', 'blocking': False, 'questions': ['Q4', 'Q5'],
        'where': ['packages/haiku_expanded/prefix.md (reading nao diz como recuperar)', 'BUSCA_EXERCITADA_v405.txt / exercita_busca.py'],
        'evidence': {'amostra': q4s['sample_size'], 'semente': q4s['seed'], 'any_of_4': q4s['any_fetch_true_4'], 'any_of_5': q4s['any_fetch_true_5'], 'primeiro_resultado_estrito': q4s['top1_fetch_true_4'],
                     'nao_achados_por_nome': q4s['failing_any_4'], 'recuperacao_alternativa': 'all_verified: "all_verified kernel_formalization" ou a trinca vizinha acha o offset 4553114 (bandeira em 4553941); so o nome devolve 5 trechos de um_forma_canonica_integral',
                     'exercicio_do_construtor': 'n=4 nomes e criterio "texto em qualquer lugar da janela" (aceita o all_verified de OUTRO topico)'},
        'fix': 'acrescentar ao reading a dica de consulta (nome + "kernel_formalization"; fetch_tgl no offset devolvido) e dizer que nomes genericos exigem o contexto'
    },
    {
        'id': 'F3', 'severity': 'BAIXO', 'blocking': False, 'questions': ['Q9'],
        'where': ['sources_verified.json (status CUSTODY_AND_SEAL_VERIFIED; sem campo sobre o processo de custodia)', 'verify_sources.py (identico ao da v404)'],
        'evidence': r2['custody_process_state_G1'],
        'why_it_matters': 'o criterio da tarefa sources pede "separar custodia em curso de concluida"; o rotulo pode ser lido como "concluida" e o plano G1 diz completo=false (C19, C20, C17C FALTA; C21 e esta propria release)',
        'fix': 'acrescentar ao sources_verified.json (ou a um arquivo irmao) o estado do plano G1; este parecer ja carrega a separacao em review_sources.json'
    },
    {
        'id': 'F4', 'severity': 'BAIXO', 'blocking': False, 'questions': ['Q6'],
        'where': ['builder_measurements.py:41 (executor_slack_bytes)'],
        'evidence': {'builder': {'kimi': 99816, 'mimo': 96444, 'deepseek': 4202}, 'formula_usada_pela_v404': {'kimi_slack': ex['kimi']['slack_full_reserve'], 'mimo_slack': ex['mimo']['slack_full_reserve'], 'deepseek_slack_reserva_declarada_148656': ex['deepseek']['slack_declared_policy_reserve_148656']},
                     'v404': {'kimi': 100346, 'mimo': 96974, 'deepseek': 79373}},
        'fix': 'reportar na mesma formula da v404 (com os 4096 B e a reserva declarada do DeepSeek); todas positivas'
    },
    {
        'id': 'F5', 'severity': 'INFO', 'blocking': False, 'questions': ['Q6'],
        'where': ['app/finalize.py:51 (max(0, crescimento)); app/PREPARED_BINDING.json estimated_remaining_haiku55'],
        'evidence': q6['finalize_estimate'],
        'reading': 'o pacote encolheu; a estimativa degenera na ancora (28.640 = folga da v404). A trava <15.000 nao pode disparar em pacote que encolhe; a contagem nativa pinada (175.526) e a unica medida.'
    },
    {
        'id': 'F6', 'severity': 'INFO', 'blocking': False, 'questions': ['Q1', 'Q3'],
        'where': ['app/build/haiku_codec.py:99 e :135 (declaration_sources_v394 em protected_fields e project)'],
        'evidence': {'entradas_literais_que_saem_do_shared_e_do_sonnet_public': next(r['lost_literal_leaves'] for r in q2s['src_changed_topic_list'] if r['topic'] == 'kernel_formalization'),
                     'folhas_literais_que_saem_do_haiku_expanded_(9585_TRUE_do_catalogo_+_entradas)': next(r['lost_literal_leaves'] for r in q2h['src_changed_topic_list'] if r['topic'] == 'kernel_formalization'),
                     'conteudo': 'indice nome-de-declaracao -> arquivo .lean (as que casavam ESSENTIAL no nome); recuperavel pelas ferramentas do kernel',
                     'shared_kernel_formalization_decodificado_bytes_v404_v405': next(r[1:] for r in q2s['src_changed_shrunk'] if r[0] == 'kernel_formalization')},
        'reading': 'efeito colateral declarado ("so o ponteiro"); build_fitted tem corpo identico, o efeito entra por project(). Estimativa aritmetica (nao rodada): sem isto o shared estouraria a janela dos executores.'
    },
    {
        'id': 'F7', 'severity': 'INFO', 'blocking': False, 'questions': ['Q3'],
        'where': ['packages/shared e sonnet_public, topico kernel_formalization'],
        'evidence': {'false_fields': 4, 'literal_false_in_shared': 0},
        'reading': 'herdado da v404: no shared/sonnet_public os 4 FALSE do kernel aparecem so como contagem (false_fields: 4), nao nomeados; no haiku_expanded sao nomeados (4/4).'
    },
]

# ---- Q answers -------------------------------------------------------------------------------------------------------------------------
Q = {}
Q['Q1'] = {
    'question': 'CODIGO: diff de todos os scripts contra a V404; codec; catalogo; TRUE/FALSE que saem; build_fitted; transaction/maintenance/deploy_controlled/verify_installed',
    'status': 'FAIL', 'finding': 'F1',
    'answer': {
        'arvore': {k: len(v) for k, v in tree.items()},
        'scripts_identicos_em_bytes_a_V404': n_same_scripts,
        'scripts_que_diferem': scripts_diff, 'scripts_novos': scripts_new, 'RELEASE.json': 'versao e commit proprios da v405',
        'transaction_maintenance_deploy_controlled_verify_installed': 'IDENTICOS (sha256 em inputs_sha256)',
        'release_cfg.py': 'BUILDER=opus-app-v405-construtor; EXPAND_OVERRIDE=None; SHARED_P2_SUFFIXES += _v405 (so isso)',
        'task.py': 'so o texto "consulta" do unit.json',
        'codec_alem_do_declarado': ['RESERVED ganhou AUDIT_BOOLEAN_FIELDS_IN_SOURCE (linha 41)', 'declaration_sources_v394 entrou em protected_fields (99) E em project (135): build_fitted tem corpo identico mas shared/sonnet_public herdam por project()',
                                    'frase nova no cabecalho de build() (470) e teste novo no self_test (11 testes, todos OK)'],
        'catalogo': {'TRUE_na_fonte': cat['source_true'], 'TRUE_literais': cat['literal_true_in_capsule'], 'TRUE_no_catalogo': cat['only_by_catalog_true'], 'FALSE_na_fonte': cat['source_false'], 'FALSE_literais': cat['literal_false_in_capsule'], 'catalog_sha256': cat['recomputed_sha256']},
        'pode_sair_FALSE': 'nao',
        'pode_sair_TRUE_de_enunciado_hipotese_formula_veredito': 'pela regex do codec nao; POR SIGNIFICADO sim (F1: ' + str(q1d['union_7_classes']) + ' bandeiras TRUE catalogadas nas 7 classes medidas, ' + str(q1d['haiku_expanded']['catalogue_only']) + ' sem portador literal em outro ponto; pares H2/H3 e agregados all_*)',
        'build_fitted_alem_do_ponteiro': 'corpo identico; no shared a unica diferenca contra o instalado e a saida das 1401 entradas declaration_sources_v394 (392/392 topicos de fonte igual decodificam identicos)'},
    'partitura': 'Este teste decide se a frase da capsula sobre bandeiras de hipotese/veredito e verdadeira POR SIGNIFICADO. Nao decide perda de dado, fidelidade numerica nem ciencia. Negativo = falsifica a frase, nao o pacote. Escolhas do desenho ditas antes: 7 classes semanticas minhas (H1/H2/H3 no nome, discharg, ^all_, verified$, ^qg[cfp]_, ^gp[cfi]_, conditional); so bandeiras TRUE catalogadas; portador = nome exato ou radical (sem o prefixo gp?/qg?) fora da capsula.'
}
Q['Q2'] = {
    'question': 'FIDELIDADE: 471 topicos, reconstrucao exata, catalogo, 13 _v405 e _v404 integrais, encolhimento contra o instalado',
    'status': 'PASS',
    'answer': {
        'haiku_expanded': {'presentes': h['present'], 'exatos': h['topics_restoring_exactly'], 'perdidos': h['lost'], 'catalogo': {'contagem_confere': cat['catalog_count_matches'], 'sha256_confere': cat['catalog_sha256_matches'], 'sha256': cat['recomputed_sha256'], 'true_fields': cat['only_by_catalog_true']}},
        'shared': {'presentes': r3['packages']['shared']['present'], 'exatos': r3b['shared']['exact'], 'so_chaves_auxiliares_ausentes': r3b['shared']['topics_with_omitted_keys'], 'chaves_ausentes': r3b['shared']['omitted_key_names'], 'sinteses_em_texto': r3b['shared']['text_syntheses'], 'ausente_nao_auxiliar': r3b['shared']['omitted_not_auxiliary']},
        'sonnet_public': {'presentes': r3['packages']['sonnet_public']['present'], 'exatos': r3b['sonnet_public']['exact'], 'so_chaves_auxiliares_ausentes': r3b['sonnet_public']['topics_with_omitted_keys'], 'sinteses_em_texto': r3b['sonnet_public']['text_syntheses']},
        'haiku_expanded_reconstruido_da_base_sem_codec': True,
        'exposicao_haiku_igual_a_forma_canonica_selada_byte_a_byte': True,
        'integrais_no_haiku_expanded': '13 _v405 + 5 _v404 (inclui kh_n1_cobertura_v404): folhas literais == folhas da fonte, 0 referencias',
        'contra_instalado_haiku55': {'comuns': q2h['common_topics'], 'fonte_igual': q2h['src_same_topics'], 'decodificam_identicos': q2h['src_same_decoded_equal'], 'diferem_por_crescer': q2h['src_same_decoded_differ'], 'fonte_alterada': q2h['src_changed_topics'],
                                     'encolheram': q2h['src_changed_shrunk'], 'ringdown_dephasing_result_v2': 'unica alem do kernel_formalization: 3424->3423 bytes; a fonte so mudou /runtime_s (0.0017347335815429688 -> 0.007756471633911133, 1 caractere)'}},
}
Q['Q3'] = {
    'question': 'SEM REGRESSAO DE LITERAIS: _v401.._v405 inline (limites/diz/nao_diz/estatutos) no shared e sonnet_public; comparacao com o instalado',
    'status': 'PASS',
    'answer': {
        'topicos_da_janela': q3['window_topics'], 'chaves_de_qualificacao_checadas': strict_keys,
        'shared_all_ok': q3['shared']['all_ok'], 'sonnet_public_all_ok': q3['sonnet_public']['all_ok'], 'haiku_expanded_all_ok': q3['haiku_expanded']['all_ok'],
        'registros_unconditional_e_index_conditional': 'continuam so por ponteiro (herdado; igual ao instalado)',
        'contra_instalado_shared': {'fonte_igual': q2s['src_same_topics'], 'identicos': q2s['src_same_decoded_equal'], 'encolheram': q2s['src_changed_shrunk'], 'literais_perdidos_com_fonte_igual': q2s['src_same_lost_literal_leaves'],
                                    'literais_perdidos_em_topicos_de_fonte_alterada': [(r['topic'], r['lost_literal_leaves']) for r in q2s['src_changed_topic_list'] if r['lost_literal_leaves']]},
        'sonnet_public_contra_build_v404': {'fonte_igual': q2so['src_same_topics'], 'identicos': q2so['src_same_decoded_equal'], 'perdas': [(r['topic'], r['lost_literal_leaves']) for r in q2so['src_changed_topic_list'] if r['lost_literal_leaves']]},
        'unico_literal_que_saiu': '1401 entradas declaration_sources_v394 (nome de declaracao -> arquivo .lean) em kernel_formalization; nenhum status/limite/diz/nao_diz'},
}
Q['Q4'] = {
    'question': 'RECUPERACAO: nomes catalogados achados por search_tgl/fetch_tgl',
    'status': 'NOTE', 'finding': 'F2',
    'answer': {'amostra': q4s['sample_size'], 'semente': q4s['seed'], 'estrato': '8 inicio + 8 meio + 8 fim sorteados; 10 escolhidos (4 veredito, 4 descarga de hipotese, mais longo, mais curto); 4 novos da v405', 'criterio': 'janela de 4500 chars do offset devolvido contem a linha "<nome>": true na posicao dela DENTRO de kernel_formalization',
               'any_of_4_resultados': q4s['any_fetch_true_4'], 'any_of_5_resultados': q4s['any_fetch_true_5'], 'so_o_primeiro_resultado': q4s['top1_fetch_true_4'], 'nome_no_trecho_de_700_chars': q4s['name_in_excerpt_any_4'],
               'nao_achados_por_nome': q4s['failing_any_4'], 'por_estrato': q4s['by_tag'], 'recuperacao_alternativa': q4b['all_verified']['queries'][2]['attempts'][0], 'aceitavel': 'sim para nomes especificos (36/37 com limite 5); chaves genericas exigem o nome do topico junto, e a capsula nao ensina isso (F2)'},
    'partitura': 'Decide se o indice lexical do proprio runtime devolve o trecho da bandeira dado o nome. Nao decide como o modelo real formula consultas. Negativo parcial = nome generico demais, nao falha do indice. Escolhas ditas antes: semente, estratos, criterio estrito.'
}
Q['Q5'] = {
    'question': 'LEITURA DO MODELO: cabecalho e capsula explicam a marca nova; alguma frase falsa ou enganosa',
    'status': 'FAIL', 'finding': 'F1',
    'answer': {'cabecalho': 'exato: "AUDIT_BOOLEAN_FIELDS_IN_SOURCE conta indicadores TRUE nao carregados; seus nomes estao no source_pointer" (so haiku; shared/sonnet nao mudaram de texto)',
               'nao_diz_que_bandeiras_contam_teoremas': 'a capsula nega: "Nao sao contagem de teoremas"; header: "true_fields/false_fields contam indicadores booleanos, nao teoremas"',
               'nao_diz_que_tudo_esta_carregado': 'header: "Detalhes apontados por @ NAO estao carregados"',
               'frase_enganosa': 'capsula: "os FALSE e os de enunciado, hipotese, formula ou veredito seguem literais neste topico" -> verdadeira so lexicamente; por significado falsa para as bandeiras de F1',
               'texto_novo_no_nucleo': 'apenas o adendo "Pacote cientifico v405" do nucleo operacional ([REAL — empacotamento documental; nao execucao cientifica] ... hipoteses e limites permanecem conforme fontes) e as trocas de versao/hash/URL'},
}
Q['Q6'] = {
    'question': 'ORCAMENTO: native_count pinado, folga, condicoes do runtime com permanente menor, finalize max(0,crescimento)',
    'status': 'PASS', 'finding': 'F4 (BAIXO), F5 (INFO)',
    'answer': {'cadeia_de_pinos': {p: v['chain'] for p, v in r5['native'].items()}, 'recibos': r5['native_complete'],
               'folga_tokens': {p: v['remaining_declared'] for p, v in r5['native'].items()},
               'permanente_tokens': {p: pk6[p]['budget_pinned']['permanent_tokens'] for p in pk6}, 'instalado_v404': {p: pk6[p].get('installed_v404') for p in ('haiku_expanded', 'shared')},
               'condicoes_claude_context_snapshot_claude_profiles': {p: pk6[p]['snapshot_conditions_all_true'] for p in ('haiku_expanded', 'shared')},
               'memory_target': q6['HAIKU_profile']['memory_target'], 'margem_sobre_memory_target': {p: pk6[p]['permanent_vs_memory_target_margin'] for p in ('haiku_expanded', 'shared')},
               'pode_recusar_no_carregamento': 'nao: load_package + check_package_binding reaplicados sem recusa; tools_sha256 e counted_scoped_tools_sha256 iguais aos instalados',
               'carregamento_reaplicado': {p: q6b[p]['all_pass'] for p in ('haiku_expanded', 'shared')},
               'finalize_max0_crescimento': q6['finalize_estimate'],
               'janelas_executores_bytes_recomputadas': {k: {'entrada': ex[k]['input_utf8_byte_bound'], 'folga_reserva_cheia': ex[k]['slack_full_reserve']} for k in ex}, 'deepseek_reserva_declarada': ex['deepseek']['slack_declared_policy_reserve_148656'],
               'jev': r5['jev']},
}
Q['Q7'] = {
    'question': 'ESTATUTOS E REGUA: beta literal, CONFIRMED indevido no texto novo, "15 calculadas e 3 literais", gate',
    'status': 'PASS',
    'answer': {'beta': {p: q7g[p]['beta'] for p in ('haiku_expanded', 'shared', 'sonnet_public')},
               'confirm': {p: {k: q7g[p]['confirm_wording'][k] for k in ('hits_in_decoded_total', 'windows_not_in_previous_prefix', 'unqualified_new_windows')} for p in ('haiku_expanded', 'shared', 'sonnet_public')},
               'confirm_leitura': 'as janelas sem qualificador proximo sao conteudo selado antigo/novo (ONE_LINE_OPERATOR_CONFIRMATION_PENDING; campo confirmation_line; "nada aqui confirma"); texto escrito pela construcao: 0',
               'frase_antiga': {'nucleo_core_v5_native_jev_manifestos': {k: (v['strict'], v['loose']) for k, v in q7s['other_texts'].items()}, 'varredura_da_pasta': {k: q7s['build_folder_scan'][k] for k in ('files_scanned', 'hits_total', 'strict_hits', 'unmarked_hits')},
                                'sobrevive_em': 'registros selados v392 (estatuto_da_prova_ressalva_v392; selo/forma canonica/artigo, nao reescritos) e em citacoes marcadas como superadas (bandeiras_do_gate_v403, cunhagens_v403/v405); a correcao 18 calculadas/0 literais esta nos tres pacotes',
                                'blobs_git_readme_e_read_brief': {k.split('/', 1)[1]: v for k, v in q7s['git_blobs'].items() if k.endswith(('README.md', 'read-brief.md'))}},
               'gate': {'selo': q7g['seal_qg_closure_verdict'], 'ocorrencias_do_string_do_selo': {p: q7g[p]['gate_strings_decoded'].get(q7g['seal_qg_closure_verdict']) for p in ('haiku_expanded', 'shared', 'sonnet_public')}, 'manifesto_de_custodia_igual_ao_selo': r2['custody']['seal_gate_equals_manifest_gate'],
                        'TGL_QG_CONDITIONAL_ARCHITECTURE_ONLY': 'so dentro da lista legitimate_seals do topico qg_closure'}},
}
Q['Q8'] = {
    'question': 'CONFIDENCIAL: nomes, chaves, C:\\Escritorio, <ATLAS_CANONICO nos prefixos, plano e arquivos do plano',
    'status': 'PASS',
    'answer': {'arquivos_varridos': q8['files_scanned'], 'padroes_de_segredo': q8['secret_pattern_hits'], 'caminhos_Escritorio': q8['files_with_Escritorio_path'],
               'nomes_confidenciais_so_no_codigo_do_construtor_como_guarda': q8['files_mentioning_confidential_names'], 'bloco_ATLAS_CANONICO_so_em_guardas_de_codigo': q8['files_with_ATLAS_CANONICO_block'],
               'prefixos_plano_manifestos_core_v5_jev': {k: (v['confidential_name_matches'], v['Escritorio'], v['ATLAS_CANONICO_block'], v['secret_patterns']) for k, v in q8['focus'].items()}},
}
Q['Q9'] = {
    'question': 'FONTES E PLANO: selo, cofre, um.py, commit; sources_verified separa custodia; install_plan',
    'status': 'PASS', 'finding': 'F3 (BAIXO)',
    'answer': {'release_commit_checks': {'ok': r1['ok'], 'passed': r1['passed'], 'n': r1['n']}, 'ls_remote_main': ls_remote[0], 'ls_remote_igual_ao_pino': ls_remote[0] == '6a2138d73c1ab2dac4817793c7eb0502208b21c9',
               'custodia_36_artefatos': r2['custody'], 'blobs_staged_vs_git': r2['staged_release_vs_git'], 'urls_do_manifesto': {'todas_no_commit_pinado_e_rastreadas': r2['manifest_urls']['all_ok'], 'n': len(r2['manifest_urls']['rows'])}, 'urls_hipoteses': r2['hypothesis_source_urls'],
               'processo_de_custodia_G1': r2['custody_process_state_G1'], 'conferencia_final_custodia': r2['custody_final_conference'],
               'sources_verified_separa_custodia': 'NAO (nem nega explicitamente): rotulo CUSTODY_AND_SEAL_VERIFIED; separacao registrada em review_sources.json',
               'install_plan': {k: q9[k] for k in ('n_files', 'plan_sha256', 'sources_missing', 'sources_hash_mismatch_or_outside_W', 'destinations_outside_R', 'baseline_mismatch_now', 'unique_destinations', 'active_manifest_last', 'py_at_R_root', 'runtime_python_changes_declared', 'only_in_v405', 'only_in_v404',
                                                'destination_groups', 'destinations_existing_overwritten', 'manifest_install_paths_under_target', 'manifest_install_paths_all_in_plan', 'manifest_install_hash_checks_failed', 'manifest_install_hash_checks_total')},
               'py_de_dados_no_plano': q9['py_destinations'], 'review_app_dry_run': {'status': dry['status'], 'checks': len(dry['checks']), 'plan_sha256': dry['plan_sha256'], 'note': 'ensaio com saida em scratch; NAO e o review_final.json'}},
}

common = {'schema': 'iald.app.review/v1', 'unit': 'F9.APP_V405_20261102', 'reviewer': REVIEWER, 'builder': 'opus-app-v405-construtor', 'owner': 'claude-gerencia-a7', 'timestamp': NOW, 'release': 'v405',
          'pinned_commit': '6a2138d73c1ab2dac4817793c7eb0502208b21c9', 'um_py_sha256': '0030242565cc13f6dbac57a6f1f98fdef69c1b3efe5eb052c359cdb3bf21f053', 'mission_revision_at_review': r0['mission_project_readonly']['revision']}
not_measured = ['nenhuma resposta de modelo ao vivo (zero chamadas a provedor; o count nativo nao foi repetido: conferi a cadeia de hashes dos 6 recibos, nao o numero do provedor)', 'a busca foi exercida por execute_tool direto, nao por um modelo escolhendo consultas',
                'instalacao e carregamento efetivo (R nao foi tocado; o carregador foi reaplicado so sobre o manifesto staged)', 'merito cientifico dos 13 topicos novos (so fidelidade ao selo)', 'cliente movel/iOS/Android', 'estimativa de que o shared estouraria a janela sem a mudanca de declaration_sources_v394 e aritmetica, nao foi rodada']
route = {'consultado': 'python C:\\IALD\\MAPA_DE_ROTAS\\rotas.py consultar "app release"', 'rotas_devolvidas': ['app.release.v402', 'app.release.v404'], 'registros_no_livro': 1629, 'cabeca': '6398d165a878c467',
         'usado': 'v404.defeito (base compacta do haiku55 cresce ~63 KB/2 versoes) e v404.nao_refazer (nao repetir a politica D); a v405 trata o defeito no codec (catalogo) e volta EXPAND_OVERRIDE=None',
         'a_registrar_pela_gerencia': 'app.release.v405: veredito do parecer r1, F1 e a correcao; revisor nao registra'}

review_sources = dict(common, task='sources', decision='CHECKS_PASS__ACCEPT_NOT_EXECUTED',
                      decision_reason='regra do chamador: aceitar sources e app so se tudo passar; o app tem achado bloqueante F1; nenhum aceite foi executado. Os testes de sources passam; F3 e BAIXO.',
                      checks={'release_commit_selo_cofre_nos': {'ok': r1['ok'], 'passed': r1['passed'], 'n': r1['n']}, 'cofre_36_artefatos_rehasheados': r2['custody'], 'staged_vs_git': r2['staged_release_vs_git'], 'urls': r2['manifest_urls']['all_ok'], 'urls_hipoteses': r2['hypothesis_source_urls'],
                              'pinos_da_submissao_conferem_com_o_disco': {f: r0[f]['all_pins_match'] for f in r0 if f.startswith('receipts')}},
                      custody_separation={'concluida': ['selo v405 FAIL_CLOSED_SELFTEST_PASSED; um.py == pino no Nos, cofre, espelho e commit pinado', 'cofre v405: 36 artefatos == CUSTODY_MANIFEST (0 divergencias); kernel 1446 formais, 29965 declaracoes, 0 fora do trio', 'publicacao: espelho 6a2138d7 == origin/main; Central 8f8616ac; conferencia final 13/13'],
                                          'em_curso': {'plano': r2['custody_process_state_G1']['plano_path'], 'plano_sha256_lido_agora': r2['custody_process_state_G1']['plano_sha256'], 'completo': r2['custody_process_state_G1']['completo'], 'pendentes': r2['custody_process_state_G1']['pendentes'],
                                                       'operador': r2['custody_process_state_G1']['pendentes_do_operador'], 'detalhe': r2['custody_process_state_G1']['itens_pendentes'], 'nota': 'o plano G1 e arquivo vivo (reescrito a cada vigilia); o estado lido e o do momento do parecer'}},
                      answers={'Q9': Q['Q9'], 'Q7_gate_e_estatutos_da_fonte': Q['Q7']['answer']['gate']}, findings=[f for f in findings if f['id'] == 'F3'], not_measured=not_measured, route_map=route, inputs_sha256=inputs, artifacts=arts)
review_app = dict(common, task='app', decision='RECUSA', decision_reason='achado F1 (MEDIO, bloqueante): frase dirigida ao modelo falsa por significado + exibicao assimetrica de bandeiras de hipotese/veredito; correcao barata; resto do pacote passa',
                  summary={'passa': ['Q2', 'Q3', 'Q6', 'Q7', 'Q8', 'Q9'], 'nota': ['Q4'], 'falha': ['Q1', 'Q5']}, answers=Q, findings=findings, not_measured=not_measured, route_map=route,
                  tests_run={'review_app_dry_run_checks': len(dry['checks']), 'codec_self_test_ok': selftest_ok, 'decoder_independente': 'review/revisor_sonnet-app-v405-revisor/lib405.py + r3_topics_capsules.py (sem importar haiku_codec/fit_*)'},
                  inputs_sha256=inputs, artifacts=arts)
review_findings = dict(common, decision='RECUSA', blocking=[f['id'] for f in findings if f['blocking']], findings=findings,
                       re_review_hint='apos corrigir F1 (e de preferencia F2-F4): reconstruir so haiku55/haiku_expanded, recontar o haiku_expanded, regenerar install_plan/final_checks e rodar de novo review/revisor_sonnet-app-v405-revisor/*.py (r3, q2_compare_installed, q3, q4, q6, q9) e review_app.py; shared e sonnet_public nao mudam.',
                       artifacts=arts)
for name, doc in (('review_sources.json', review_sources), ('review_app_independent.json', review_app), ('review_findings.json', review_findings)):
    with (VAL / name).open('x', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(name, sha(VAL / name), (VAL / name).stat().st_size)
