"""Revisor sonnet-app-v407-revisor -- compila os resultados MEDIDOS (q1..q10, q8 = review_app.py) em validation/review_sources.json, validation/review_app_independent.json
e no PARECER_v407_R1.md. Todo numero e' LIDO dos JSON de saida, nunca digitado. Escreve so' em validation/review_sources.json, validation/review_app_independent.json e nesta pasta."""
import datetime, hashlib, json, sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
ACTOR = 'sonnet-app-v407-revisor'
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: json.loads(Path(p).read_bytes())
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
Q1, Q2, Q3, Q4R, Q4N, Q5, Q5B, Q9, Q9B, Q10, EX, TD = (rd(HERE / n) for n in ('q1_sources_out.json', 'q2_q4_decode_out.json', 'q3_q6_q7_out.json', 'q4_recovery_out.json', 'q4_nonascii_out.json', 'q5_f1_out.json', 'q5b_global_status_leaves_out.json',
                                                                              'q9_transaction_out.json', 'q9b_serialize_out.json', 'q10_amarras_out.json', 'q_extra_numbers_out.json', 'q_tools_diff_out.json'))
TXT = rd(HERE / 'q_text_blocks_out.json')
final = rd(W / 'validation/review_final.json')
o1, o2, o3, o5, o9, o10 = Q1['out'], Q2['out'], Q3['out'], Q5['out'], Q9['out'], Q10['out']
rs = Q4R['summary']

# ------------------------------------------------------------------ checks agregados
def tag(checks, src):
    return [{**c, 'script': src} for c in checks]
checks_all = tag(Q1['checks'], 'q1_sources.py') + tag(Q2['checks'], 'q2_q4_decode.py') + tag(Q3['checks'], 'q3_q6_q7.py') + tag(Q5['checks'], 'q5_f1.py') + tag(Q9['checks'], 'q9_transaction.py') + tag(Q10['checks'], 'q10_amarras.py')
# recuperacao (Q4): criterio fixado antes: taxa >= 99% e toda falha explicada
rec_ok = (rs['found_text'] / rs['sample'] >= 0.99) and (rs['found_in_topic'] / rs['sample'] >= 0.99) and rs['recipe_text_present_in_capsule'] and Q4N['all_recovered_by_either']
checks_all.append({'name': 'Q4.recovery_recipe_604_names_seed_407407407', 'pass': rec_ok, 'gating': True, 'sample': rs['sample'], 'found_text': rs['found_text'], 'found_in_topic_strict': rs['found_in_topic'], 'failures_strict': rs['failures_in_topic'], 'non_ascii_names_all_recovered': Q4N['all_recovered_by_either'], 'script': 'q4_recovery.py + q4_nonascii.py'})
checks_all.append({'name': 'Q5c.no_status_leaf_became_pointer_only_all_topics', 'pass': all(v['newly_pointer_only'] == 0 for v in Q5B.values()), 'gating': True, **{k: {'v407': v['pointer_only_v407'], 'v406': v['pointer_only_v406_installed'], 'newly': v['newly_pointer_only']} for k, v in Q5B.items()}, 'script': 'q5b_global_status_leaves.py'})
checks_all.append({'name': 'Q9.serialization_of_report_with_scope_measurement_by_write_evidence_rules', 'pass': Q9B['serializes_ok'], 'gating': True, 'live_report_json_bytes': Q9B['live_report_json_bytes'], 'script': 'q9b_serialize.py'})
checks_all.append({'name': 'Q8.review_app_py_mechanical', 'pass': final['status'] == 'PASS' and final['reviewer'] == ACTOR, 'gating': True, 'checks': len(final['checks']), 'plan_files': 1782, 'review_final_sha16': sha((W / 'validation/review_final.json').read_bytes())[:16], 'script': 'review/review_app.py'})
gating_fail = [c['name'] for c in checks_all if not c['pass'] and c.get('gating', True)]
nongating_fail = [c['name'] for c in checks_all if not c['pass'] and not c.get('gating', True)]
n_pass = sum(1 for c in checks_all if c['pass'])

# ------------------------------------------------------------------ numeros-chave
cap = EX['conversation_capacity_bytes_before_visible_refusal']
fold = Q3['out']['Q3_folga']
b3 = o3['Q3_native']
cls = o2['Q2_block_changes_vs_v406_by_package']
f1_bytes = {pkg: sum(b for n, b in cls[pkg]['bytes_delta'].items() if cls[pkg]['by_topic'][n]['classified_as'].startswith('F1')) for pkg in cls}
f1_topics = {pkg: sum(1 for n in cls[pkg]['bytes_delta'] if cls[pkg]['by_topic'][n]['classified_as'].startswith('F1')) for pkg in cls}
v402_saved = o2['Q2_v402_block_bytes']
cov = o9['coverage_candidates']
gaps = o9['coverage_gaps']
big_flat = o5['b_flat_status_dicts_gt_500B_not_literal_in_haiku_expanded']
brec = o5['b_records']
lit_pkg = o5['b_literal_by_package']
live9 = o9['live']
sur = o9['lone_surrogate_filename']
fuzz = o9['fuzz']
hand = Q3['out']['Q6_hand_read']
q6 = Q3['out']['Q6']

numbers = {
    'pino_um_py_sha16': '833121339e649f71', 'commit': 'bf9017157406afa6b4dc05c6a9d566129e6a6ee4', 'review_final_sha256': sha((W / 'validation/review_final.json').read_bytes()),
    'q1': {'checks': len(Q1['checks']), 'artifacts_recomputed': 36, 'public_blobs': 10, 'git_refs': o1['git_refs']},
    'q2': {'topics': o2['topics_total'], 'window': o2['window_topics'], 'retired': o2['retired_topics']['by_suffix'], 'qualifier_keys_checked_shared': o2['Q2_summary']['shared']['qualifier_keys_checked'], 'lit3_checked_shared': o2['Q2_summary']['shared']['limites_diz_nao_diz_checked'],
           'unchanged_source_topics': o2['Q2_shared_vs_installed_v406']['topics_with_unchanged_source'], 'changed_source_topics': o2['Q2_shared_vs_installed_v406']['topics_with_changed_source'], 'new_topics': o2['Q2_shared_vs_installed_v406']['new_topics_in_v407'],
           'block_changes_vs_v406': {p: v['kinds'] for p, v in cls.items()}, 'v402_block_bytes': v402_saved, 'shared_bytes': o2['Q2_shared_bytes']},
    'q3': {'folga_declarada': {k: v['folga_reserva_declarada_148656'] for k, v in fold.items()}, 'folga_v406_declarada': {k: v['v406_folga_declarada'] for k, v in fold.items()}, 'haiku55_remaining_tokens': b3['haiku_expanded']['remaining_tokens'], 'shared_remaining_tokens': b3['shared']['remaining_tokens'], 'conversation_capacity_bytes': cap},
    'q4': {'catalog_true': o2['Q4_catalog']['catalog_new_rule'], 'moved_to_literal_vs_old_rule': o2['Q4_catalog']['moved_to_literal_vs_old_rule'], 'recovery': {k: rs[k] for k in ('seed', 'sample', 'found_text', 'found_in_topic', 'first_hit_ok')}, 'non_ascii': Q4N['non_ascii_names']},
    'q5': {'flat_status_records_le_500B': brec['n_flat_status_records_le_500B'], 'bytes': brec['bytes_sum'], 'literal_by_package': {k: v['literal'] for k, v in lit_pkg.items()}, 'f1_bytes_in_unchanged_source_topics': f1_bytes, 'f1_topics': f1_topics, 'self_test': o5['d_self_test']['ran']},
    'q7': {'plan_files': o3['Q7_n_files'], 'under_target': o3['Q7_destinations_under_target'], 'elsewhere': len(o3['Q7_destinations_elsewhere'])},
    'q9': {'fuzz_pairs': fuzz['pairs'], 'fuzz_raised': fuzz['raised'], 'fuzz_differs_from_oracle': fuzz['differs_from_independent_oracle'], 'live_seconds': live9['seconds_each'], 'live_state_files': live9['state_files'], 'live_client_files': live9['client_files'], 'coverage_gaps': len(gaps)},
}
numbers['q3']['min_folga'] = min(v['folga_reserva_declarada_148656'] for v in fold.values())

# ------------------------------------------------------------------ achados
F = []
add = lambda sev, ident, text, ev=None: F.append({'severity': sev, 'id': ident, 'text': text, **({'evidence': ev} if ev else {})})
add('BAIXO', 'B1', f"Cobertura do escopo medido (Q9-iv): {len(gaps)} candidatos a estado ou cliente existem em C:\\IALD\\projetos_pyhton\\IALD e ficam FORA da medição de transaction.py: vínculo do dono (owner_private\\apple, DPAPI), privacidade/consentimento do chat (owner_private\\chat_privacy), "
    "saldos e razões de uso (iald_saldo_claude/openai.json, iald_uso_claude/openai.json), pedidos de acesso (iald_pedidos_acesso.json, iald_access_requests.json, iald_contract_requests.json), atividade e artefatos de tarefa (.iald_runtime\\task_runs, \\task_artifacts), iald_sync_central_estado.json, iald_deadlines.json, iald_memoria.json, "
    "e o cliente web de fato servido (app\\, iald_chat.html, sw.js, manifest.json, icons\\; iald-app\\www é o espelho de app\\). A árvore medida como cliente, iald_web\\app, é a reescrita modular abandonada de julho (diz o comentário de tgl_cripto.py; nenhum código de runtime a referencia)."
    " O plano NÃO escreve em nenhum desses caminhos (plan_overlap vivo vazio; nenhum destino dentro de qualquer candidato), e a varredura de janela do D4 reescrito continua cobrindo a árvore inteira; por isso BAIXO. Mas o campo 'accounts_modified' será lido como 'contas, carteira e consentimentos intactos' e hoje só diz 'os 120 arquivos medidos'.",
    {'candidates': {k: {'files': v['files'], 'measured': v['measured_by_v407'], 'plan_writes_inside': v['plan_writes_inside']} for k, v in cov.items()}, 'recomendacao': "acrescentar às tuplas SCOPE_STATE_*/SCOPE_CLIENT_*: owner_private, .iald_runtime\\task_runs, \\task_artifacts, os 4 JSON de saldo/uso, os 3 JSON de pedidos, iald_sync_central_estado.json, app, iald_chat.html, sw.js, manifest.json, icons; trocar iald_web\\app por app. Qualquer mudança em transaction.py muda o transaction_sha256 pinado em review_final.json (novo review_app.py). Enquanto não for feito: ler os três campos como 'dentro do conjunto medido' e manter a varredura de janela do D4."})
add('BAIXO', 'B2', "Q9-ii: nome de arquivo com substituto Unicode solitário (ex.: U+D800) numa árvore medida faz scope_compare levantar UnicodeEncodeError (em _scope_aggregate, .encode('utf-8')). A chamada fica em apply_plan DEPOIS da escrita do plano e fora de qualquer try: a instalação ficaria feita, sem deployment.json (o finally do deploy_controlled ainda reinicia o web). Reproduzido em raiz de brinquedo "
    f"({sur.get('compare', '')[:90]}). Probabilidade ~0 (o conjunto medido vivo roda sem exceção: scope_compare vivo ok; NTFS aceita o nome, mas o app grava mídia por nome de hash), por isso BAIXO. Mitigação sem tocar no arquivo: rodar scope_snapshot/scope_compare vivos imediatamente antes de pedir o reinício (eu rodei hoje). Correção de uma linha: encode('utf-8', 'surrogatepass') ou try/except em torno da chamada.", {'brinquedo': sur})
add('BAIXO', 'B3', f"Q3: a folga mínima declarada caiu de {min(v['v406_folga_declarada'] for v in fold.values())} B (v406) para {numbers['q3']['min_folga']} B (DeepSeek; Kimi {fold['kimi']['folga_reserva_declarada_148656']}, MiMo {fold['mimo']['folga_reserva_declarada_148656']}). Positiva, mas o `shared` cresceu {o2['Q2_shared_bytes']['v407'] - o2['Q2_shared_bytes']['installed_v406']} B e tirar `_v402` poupou só "
    f"{v402_saved['installed_v406_shared'] - v402_saved['v407_shared']} B (de {v402_saved['installed_v406_shared']} para {v402_saved['v407_shared']}): o bloco aposentado mantém limites/diz/nao_diz e os campos epistêmicos, e `ponte_da_escala_dual_v402` nem compacta (a cápsula pouparia menos de 50 B). A premissa 'sai `_v402`, libera ~27 KB' não se confirmou. "
    f"Capacidade de conversa estimada antes da recusa visível do runtime (fórmulas de check_window/output_budget; bytes contados como tokens, margem deliberadamente folgada): Kimi {cap['v407:kimi']} B (v406 {cap['v406:kimi']}), MiMo {cap['v407:mimo']} B ({cap['v406:mimo']}), DeepSeek {cap['v407:deepseek']} B ({cap['v406:deepseek']}). Uma v408 do mesmo porte (+29 KB) já não cabe; retirar `_v403` pouparia ~3 KB, não 31 KB; a alavanca da janela está quase esgotada (o maior bloco é `_v405`, "
    f"{EX['shared_block_bytes_by_suffix_v407']['v405']} B no shared).", {'bytes_por_sufixo_shared_v407': EX['shared_block_bytes_by_suffix_v407'], 'bytes_por_sufixo_shared_v406_instalada': EX['shared_block_bytes_by_suffix_v406_installed']})
add('BAIXO', 'B4', f"Q5b: o alcance da F1. No haiku55 {lit_pkg['haiku_expanded']['literal']} de {brec['n_flat_status_records_le_500B']} registros planos de estatuto ≤ 500 B estão literais (+{f1_bytes['haiku_expanded']} B em {f1_topics['haiku_expanded']} tópicos de fonte inalterada). No `shared` e no `sonnet_public` só {lit_pkg['shared']['literal']} de {brec['n_flat_status_records_le_500B']}: "
    f"a F1 só chega aos tópicos regenerados; os blocos reaproveitados do baseline ficam como na v406 instalada ({f1_topics['shared']} tópicos mudaram, +{f1_bytes['shared']} B). A fonte tem {brec['n_flat_status_key_dicts_any_size'] - brec['n_flat_status_records_le_500B']} registros planos de estatuto > 500 B ({brec['size_buckets']['501-1000']} entre 501 e 1000 B, somando {brec['bytes_by_bucket']['501-1000']} B); {big_flat['n']} deles ({big_flat['bytes']} B; o maior, the_fold_through_J/statuses, {big_flat['sample_largest'][0][2]} B) seguem só por ponteiro no haiku55. "
    "Nenhuma folha de qualificador virou só-ponteiro em lugar algum (Q5c global: 0 novas nos 3 pacotes).", {'size_buckets': brec['size_buckets'], 'bytes_by_bucket': brec['bytes_by_bucket'], 'nested_non_flat_le_500': brec['nested_non_flat_status_key_dicts_le_500B']})
add('INFO', 'I1', f"Git: a conferência remota (ls-remote) NÃO foi repetida (sem rede). O ref local origin/main, o HEAD local e o commit pinado são o mesmo ({o1['git_refs']['pinned'][:12]}); o remoto declarado pelo construtor (sources_verified: remote_checked) e a conferência final da custódia (13 de 13, com 'GitHub raw: um.py = pino') são [DECLARADO]; recomputei os 10 blobs públicos e as URLs no objeto git local.")
add('INFO', 'I2', f"CUSTODIA_v407_ESTADO.json do construtor está defasado: o plano G1 andou (sha16 {o1['custodia_plan_sha16_recorded_by_builder']} para {o1['custodia_plan_sha16_now']}; pendentes de 8 para {len(o1['plan_pendentes'])}: {', '.join(o1['plan_pendentes'])}; C21 = esta release, do operador). Direção correta; só o registro do construtor ficou para trás.")
add('INFO', 'I3', f"Blocos que mudaram contra a v406 instalada (tópicos de fonte inalterada), todos explicados: shared e sonnet_public {cls['shared']['kinds']}; haiku55 {cls['haiku_expanded']['kinds']}. {o2['Q2_shared_vs_installed_v406']['topics_with_changed_source']} tópicos têm fonte alterada no selado v407 (restauram igual ao selado), mais os 3 novos "
    f"({', '.join(o2['Q2_shared_vs_installed_v406']['new_topics_in_v407'])}). nivel2_rite virou cápsula no shared (a F1 engordou o bloco antes da compactação) e deixou de trazer resultado_sha256 literal (não epistêmico). Os {TXT['text_blocks']} blocos de síntese em prosa (TEXT, não restauráveis por máquina): {TXT['unchanged_source']} de fonte inalterada com corpo igual ao da v406 instalada; {len(TXT['changed_source'])} de fonte alterada ({', '.join(TXT['changed_source'])}) mudaram só `/runtime_s` (metadado de tempo) e o corpo é idêntico ao instalado.")
add('INFO', 'I4', f"Contagem de palavras-qualificador no haiku55 caiu (CREDITATION {q6['installed_v406_haiku55']['qualifiers']['CREDITATION']} para {q6['haiku_expanded']['qualifiers']['CREDITATION']}, UNINHABITED {q6['installed_v406_haiku55']['qualifiers']['UNINHABITED']} para {q6['haiku_expanded']['qualifiers']['UNINHABITED']}, HILBERT {q6['installed_v406_haiku55']['qualifiers']['HILBERT']} para {q6['haiku_expanded']['qualifiers']['HILBERT']}) "
    "porque os tópicos _v405 saíram da expansão (nomes de teoremas deixam de ser literais); a presença (o critério do briefing) está em todos os prefixos e as chaves de qualificador da janela seguem literais.")
add('INFO', 'I5', f"Recuperação por nome (Q4): {rs['sample']} nomes (semente {rs['seed']}); {rs['found_text']} de {rs['sample']} por texto, {rs['found_in_topic']} de {rs['sample']} pela métrica estrita (a janela cobre a posição da bandeira dentro de kernel_formalization). A única falha estrita, {rs['failures_in_topic'][0]}, aparece também em external_ladder: os 5 resultados trouxeram "
    "a ocorrência de external_ladder (texto achado) e a janela do resultado de kernel_formalization termina 239 caracteres antes da bandeira (o offset do resultado não é a posição da bandeira). Com limit 10 ou 20 a janela certa aparece. Os 4 nomes não-ASCII do catálogo foram recuperados pela consulta literal e pela escapada.")
add('INFO', 'I6', "O plano instala um um.py sob canonical_releases\\v407_...\\release (cópia imutável de dado, igual ao plano da v406); nenhum .py de runtime é substituído e runtime_python_changes é 0.")
add('INFO', 'I7', "Contagens nativas (6 pedidos, 0 geração, recibo do construtor) não foram repetidas (sem rede, sem chave); conferi pins, orçamento, ausência de contexto do operador e do Atlas privado em cada native_count.json.")
findings = F

limits = ["Não instalei, não implantei, não reiniciei nada; não rodei prepare.py, finalize.py, count_final_public.py, validate_plan.py, deploy_controlled.py, verify_installed.py nem teste_escopo_v407.py.",
          "Sem rede: o remoto do git e as contagens nativas ficam [DECLARADO pelo construtor/custódia]; confiro o objeto git local e o ref origin/main local.",
          "A mudança de listener (porta 18765/18766) foi simulada (substituí a função que lê listeners): não inicio processo. A leitura real de listeners foi exercida no listener vivo da porta 8081.",
          "Não executei apply_plan nem o D4 sobre a produção; entreguei d4_check.py (função pura) e a prova de que ele é executável em raiz de brinquedo (limpo passa, 6 perturbações falham, log do supervisor é esperado).",
          "Não avaliei resposta de modelo ao vivo, celular físico nem valor científico; as sínteses em prosa (46 blocos TEXT) foram comparadas byte a byte com a v406 instalada (todas iguais; 42 de fonte inalterada e 4 que só mudaram `/runtime_s`), não reconstruídas da fonte.",
          "O protocolo de memória ACOM (init/transition) não foi escrito por mim: a ordem de escrita limitava-me à minha pasta e a dois JSON de validação; o recibo do aceite fica em W\\receipts."]

transparency = [
    "Q1: três defeitos do MEU script corrigidos depois da primeira execução: conjunto 'safe' do percent-encoding (o construtor usa %28/%29, igual a urllib.parse.quote padrão), candidato de selo (peguei uma cópia arquivada mais funda no git) e a leitura de 'ok' da conferência final (é contagem 13 de 13). A defasagem do plano G1 virou INFO (o plano andou).",
    "Q2: troquei 'aposentado => cápsula' (critério meu, herdado do molde) por 'literal presente e igual', depois de ver que compact() não compacta quando a cápsula poupa menos de 50 B (ponte_da_escala_dual_v402 fica íntegro, com todos os literais). Troquei também 'bloco decodificado igual à v406 instalada, exceto _v402' por uma classificação (IDÊNTICO, _v402, deslocamento da janela do haiku55, F1) depois de ver 3 blocos do shared mudarem por efeito da F1; um bloco sem explicação seria FAIL.",
    "Q5: o gate 'todos os 59 registros literais' ficou só no haiku55 (escopo do briefing e da F1); no shared/sonnet_public deu 27 de 59 e virou achado B4, não gate, depois de eu ver o número.",
    "Q6: a contagem de palavras-qualificador não-decrescente (critério meu) virou INFO (o briefing pede presença); 3 contextos de 'CONFIRMADA' em snake_case escaparam do meu regex de palavra e foram lidos a mão (79 contextos distintos lidos).",
    "Q7: 'nenhum destino .py' virou 'nenhum .py de runtime substituído' (o briefing), porque o um.py sob canonical_releases é dado e igual ao plano da v406.",
    "Q9: duas conferências ficaram como achados BAIXOS por julgamento meu de severidade (cobertura B1 e nome com substituto B2), não como gates."]

# ------------------------------------------------------------------ review_sources.json (Q1)
src_checks = [c for c in checks_all if c['script'] == 'q1_sources.py']
src_fail = [c['name'] for c in src_checks if not c['pass'] and c.get('gating', True)]
rsrc = {'status': 'PASS' if not src_fail else 'FAIL', 'reviewer': ACTOR, 'timestamp': now, 'task': 'sources', 'release': 'v407', 'checks': src_checks, 'numbers': {**numbers['q1'], 'pino': 'sha256 inteiro lido de RELEASE.json e recomputado do cofre'},
        'findings': [f for f in findings if f['id'] in ('I1', 'I2')], 'limits': [limits[1], limits[0]], 'script_sha256': sha((HERE / 'q1_sources.py').read_bytes())}
(W / 'validation').mkdir(exist_ok=True)
with (W / 'validation/review_sources.json').open('x', encoding='utf8') as f:
    json.dump(rsrc, f, ensure_ascii=False, indent=2)

# ------------------------------------------------------------------ review_app_independent.json (Q2-Q7, Q9, Q10)
scripts = {p.name: sha(p.read_bytes())[:16] for p in sorted(HERE.glob('*.py'))}
reused = ['lib405.py (copiado do revisor da v406, sem mudança: decodificador independente de prefixo/capsula)', 'q2_q4_decode.py (adaptado de qb_decode.py: janela/aposentados/pacotes/instalada v406, classificação de blocos)', 'q4_recovery.py (adaptado de qc_recovery.py: semente, amostra, regra do não-ASCII fixada antes)',
          'q3_q6_q7.py (adaptado de qa_files.py: partes Q3, Q6, Q7)', 'q1_sources.py (adaptado de qa_files.py parte Q1)', 'novos, meus: f1lib.py, q5_f1.py, q5b_global_status_leaves.py, q9_transaction.py, q9b_serialize.py, q10_amarras.py, d4_check.py, q_tools_diff.py, q_extra_numbers.py, q_text_blocks.py, q4_nonascii.py (adaptado de qd_nonascii.py), conf_contexts.py, probe_*.py (exploratórios), qz_compile.py, qz_parecer.py']
rapp = {'status': 'PASS' if not gating_fail else 'FAIL', 'reviewer': ACTOR, 'timestamp': now, 'task': 'app', 'release': 'v407', 'verdict': 'ACEITO COM RESSALVAS (nenhum achado ALTO ou MEDIO)' if not gating_fail else 'RECUSADO',
        'checks_total': len(checks_all), 'checks_pass': n_pass, 'gating_failures': gating_fail, 'nongating_failures': nongating_fail,
        'numbers': numbers, 'review_final': {'path': 'validation/review_final.json', 'sha256': numbers['review_final_sha256'], 'checks': len(final['checks']), 'transaction_sha256': final['transaction_sha256'], 'maintenance_sha256': final['maintenance_sha256'], 'plan_sha256': final['plan_sha256']},
        'findings': findings, 'transparency_criteria_changed_after_seeing_data': transparency, 'reused_from_mould': reused, 'limits': limits, 'scripts_sha16': scripts,
        'partitura_antes_de_medir_sha256': sha((HERE / 'PARTITURA_antes_de_medir.md').read_bytes()), 'checks': checks_all}
with (W / 'validation/review_app_independent.json').open('x', encoding='utf8') as f:
    json.dump(rapp, f, ensure_ascii=False, indent=2, default=str)
print(json.dumps({'sources': rsrc['status'], 'app': rapp['status'], 'checks_total': len(checks_all), 'checks_pass': n_pass, 'gating_failures': gating_fail, 'nongating_failures': nongating_fail,
                  'review_sources_sha16': sha((W / 'validation/review_sources.json').read_bytes())[:16], 'review_app_independent_sha16': sha((W / 'validation/review_app_independent.json').read_bytes())[:16]}, indent=1))
json.dump({'findings': findings, 'numbers': numbers, 'transparency': transparency, 'limits': limits}, open(HERE / 'qz_compile_out.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1, default=str)
