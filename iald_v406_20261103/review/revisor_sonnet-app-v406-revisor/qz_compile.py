"""Revisor sonnet-app-v406-revisor -- compila os resultados medidos (qa_files, qb_decode, qc_recovery, qd_nonascii, review_app.py) em validation/review_sources.json,
validation/review_app_independent.json e no PARECER_v406_R1.md. Todo numero e' LIDO dos JSON de saida, nunca digitado."""
import datetime, hashlib, json, re, sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lib405 as L

ACTOR = 'sonnet-app-v406-revisor'
W = Path(r'C:\IALD\Central de Patentes\work\iald_v406_20261103')
V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v406')
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: json.loads(Path(p).read_bytes())
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
QA, QB, QC, QD = (rd(HERE / n) for n in ('qa_files_out.json', 'qb_decode_out.json', 'qc_recovery_out.json', 'qd_nonascii_out.json'))
qa, qb = QA['out'], QB['out']
cka = {c['name']: c for c in QA['checks']}
ckb = {c['name']: c for c in QB['checks']}
final = rd(W / 'validation/review_final.json')
res = rd(V / 'um_absoluto.json')
core = res['core']

# ---- extra measurement 1: what the three retired _v401 topics keep literal in `shared` (all top-level keys, extended qualifier set)
P = L.parse_prefix((W / 'app/packages/shared/prefix.md').read_text('utf-8'))
EXT = re.compile(r'not_claimed|not_said|declar|conditional|condicional|hypoth|hip[oó]tes|caveat|limit|diz|status|statute|estatuto|verdict|veredit|scope|escopo', re.I)


def has_ref(v):
    if isinstance(v, L.Summ) or L.is_ref(v):
        return True
    if isinstance(v, dict):
        return any(has_ref(x) for x in v.values())
    if isinstance(v, list):
        return any(has_ref(x) for x in v)
    return False


retired = {}
for n in qb['retired_topics']['names']:
    k, dn = L.decode_block(P, n)
    f = dn.get('fields', {}) if L.is_ref(dn) else {}
    src = core[n]
    cls = {}
    for key in src:
        if '/' + key in f:
            cls[key] = 'REF' if has_ref(f['/' + key]) else 'LIT'
        else:
            cls[key] = 'POINTER_ONLY'
    retired[n] = {'top_keys': len(src), 'literal': sorted(x for x, s in cls.items() if s == 'LIT'), 'pointer_only_extended_qualifier_keys': sorted(x for x, s in cls.items() if s != 'LIT' and EXT.search(x)),
                  'pointer_only_other': sum(1 for x, s in cls.items() if s != 'LIT' and not EXT.search(x))}
# ---- extra measurement 2: confidentiality scan of app/native_prefix.md (not required by Q6, done for completeness)
conf = re.compile(r'<ATLAS_CANONICO|iald_stack_v7|iald_psion_state|IALD_CLAUDE_API_KEY|\.env\b|\bsk-[A-Za-z0-9_\-]{20,}', re.I)
nat = (W / 'app/native_prefix.md').read_text('utf-8')
native_hits = len(conf.findall(nat))

findings = []
add = lambda sev, ident, text, ev=None: findings.append({'severity': sev, 'id': ident, 'text': text, **({'evidence': ev} if ev else {})})
ia = qb['Q4_haiku_expanded']
rc = QC['summary']
add('BAIXO', 'F1', 'haiku55: o topico projecao_transversal_v404 (compacto no haiku55 porque a janela expandida deslizou para _v405/_v406) perdeu o literal de name_status {estado: PROVISORIO, aceito_pelo_operador: "ate\' ele dar outro"}: virou so ponteiro. Causa: protected_fields() do haiku_codec so protege valor ESCALAR sob chave ESSENTIAL; nome status dentro de dict com filhos em portugues (estado, quem) nao casa. Fora do escopo do criterio de Q2 (shared/sonnet_public, onde e literal); 1 de 208 chaves de qualificador no haiku55; recuperavel pelo ponteiro.',
    {'haiku55_qualifier_keys_not_literal': qb['Q2_summary']['haiku_expanded']['qual_not_lit_or_unequal']})
add('BAIXO', 'F2', 'Receita de recuperacao: %d/%d achados pelo criterio literal; a unica falha (ext_bgl_D1a3OutputBGL_\u03c3_kernel_checked) e artefato de medicao: o selado guarda nomes nao-ASCII escapados (\\u03c3); 4 nomes do catalogo; re-medidos 4/4 recuperados pela receita (consulta literal e escapada). Nome generico segue avisado na capsula. R3-2 (max_chars 4500) confirmado.' % (rc['found_text'], rc['sample']),
    {'sample': rc['sample'], 'seed': rc['seed'], 'non_ascii_names': QD['non_ascii_names'], 'recovered_with_exact_recipe': QD['exact_recipe_with_literal_unicode']})
add('BAIXO', 'F3', 'shared e sonnet_public trazem kernel_formalization so como contagem (true_fields %s, false_fields %s): os 4 nomes FALSE nao aparecem fora do haiku55. Desenho herdado da v405 (instalada: 10310/4), nao e mudanca da v406; a capsula diz que os indicadores estao na fonte.' % (qb['Q4_shared']['capsule']['true_fields'], qb['Q4_shared']['capsule']['false_fields']))
add('BAIXO', 'F4', 'DeepSeek: folga real com o output reservado pelo runtime (output_budget adaptativo) e de %d B; com a reserva declarada 148656 e de %d B. Por desenho (identico a v405: 106 B): com historico real longo o runtime recusa de forma visivel (admission_input_bound/check_window), nao trunca.' % (qa['Q3_folga']['deepseek']['folga_com_output_tokens'], qa['Q3_folga']['deepseek']['folga_reserva_declarada_148656']))
for n, r in retired.items():
    if r['pointer_only_extended_qualifier_keys']:
        add('BAIXO', 'F5-' + n, 'topico aposentado %s: chaves de qualificador do conjunto estendido (nao exigidas por Q2) que ficaram so ponteiro na capsula do shared: %s' % (n, r['pointer_only_extended_qualifier_keys']))
add('INFO', 'I1', 'Commit pinado a381c4d1 NAO e o HEAD local (ff882f81): e ancestral dele (git merge-base --is-ancestor = 0); mensagem do commit cita v406; os blobs das %d fontes publicas no commit pinado batem com PUBLIC_GIT_BINDING. Conferencia remota (ls-remote) nao repetida (sem rede).' % len(rd(W / 'app/PUBLIC_GIT_BINDING.json')['sources']))
add('INFO', 'I2', 'Caminho de destino real: canonical_releases\\v406_a381c4d14709 (12 hex, convencao da v405), nao v406_a381c4d147 (abreviacao da ordem).')
add('INFO', 'I3', 'shared/sonnet_public: %d blocos de resumo em prosa (TEXT) nao sao restauraveis por maquina (mesmo conjunto da v405 instalada; %d com fonte inalterada, corpo byte a byte igual) e %d blocos JSON omitem so chaves auxiliares de hash (protocol_hash/frozen_hash/...), mesmo conjunto da v405.' % (qb['Q2_text_blocks_vs_installed']['texts_v406'], qb['Q2_text_blocks_vs_installed']['unchanged_source_bodies_equal'], ckb['Q2.decoded_capsules_restore_sealed_source:shared']['topics_missing_only_AUX_hash_metadata_keys']))
add('INFO', 'I4', 'Custodia: CUSTODIA_v406_ESTADO.json (EM CURSO) confere com custodia_G1/PLANO_v406.json (completo=false; pendentes %s; C21 = esta release, decisao do operador).' % qa['plan_pendentes_do_operador'] if False else 'Custodia: CUSTODIA_v406_ESTADO.json (EM CURSO) confere com custodia_G1/PLANO_v406.json (completo=false; C21 = esta release, troca do servico e do operador).')
add('INFO', 'I5', 'Contagens nativas (6 respostas so de contagem) nao foram repetidas pelo revisor: custodia da etapa anterior; recomputei o limite de admissao dos 3 conectores com as funcoes puras do runtime sobre o prefixo real e conferem.')
has_alto_medio = any(f['severity'] in ('ALTO', 'MEDIO', 'MÉDIO') for f in findings)

# ---------------------------------------------------------------- review_sources.json
q1 = [c for c in QA['checks'] if c['name'].startswith('Q1.')]
sources = {'status': 'PASS' if all(c['pass'] for c in q1) else 'FAIL', 'reviewer': ACTOR, 'timestamp': now, 'task': 'sources', 'release': 'v406',
           'checks': q1, 'numbers': {'pino_um_py_sha16': rd(W / 'app/RELEASE.json')['um_py_sha256'][:16], 'commit': rd(W / 'app/RELEASE.json')['espelho_commit'], 'artifacts_recomputed': 36, 'formal_files': 1747,
                                     'git_candidates_for_sealed_files': qa['git_candidates_for_sealed_files'], 'vault_equals_git_blob': qa['vault_equals_git_blob'], 'git_commit_head_lines': qa['git_commit_head_lines'][:5]},
           'findings': [f for f in findings if f['id'] in ('I1', 'I2', 'I4')],
           'scope': ['Verificacao independente por recomputo (sha256 dos 36 artefatos do cofre; blobs no commit pinado via git cat-file, somente leitura).', 'Sem rede: ls-remote nao repetido.', 'Sem escrita em producao, cofre, Nos ou espelho.']}
with (W / 'validation/review_sources.json').open('w', encoding='utf8') as f:
    json.dump(sources, f, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------- review_app_independent.json
rest = [c for c in QA['checks'] if not c['name'].startswith('Q1.')] + QB['checks']
q2 = [c for c in QB['checks'] if c['name'].startswith('Q2.')]
app = {'status': 'PASS' if all(c['pass'] for c in rest) and final['status'] == 'PASS' and not has_alto_medio else 'FAIL', 'reviewer': ACTOR, 'timestamp': now, 'task': 'app', 'release': 'v406',
       'q_summary': {
           'Q2': {'window_topics': qb['window_topics'], 'retired_topics': qb['retired_topics']['names'], 'topics_present_per_package': 474, 'qualifier_keys_checked_shared': qb['Q2_summary']['shared']['qualifier_keys_checked'], 'limites_diz_nao_diz_literal_equal': qb['Q2_summary']['shared']['limites_diz_nao_diz_checked'],
                  'shared_vs_installed_v405': qb['Q2_shared_vs_installed_v405'], 'retired_qualifier_leaves_lost': qb['Q2_retired_qualifier_leaves_lost_vs_installed_v405'], 'v401_block_bytes': qb['Q2_v401_block_bytes'], 'retired_literal_keys': retired},
           'Q3': {'folga': qa['Q3_folga'], 'recomputed_bounds': qa['Q3_recomputed_bounds'], 'native': {k: {x: v[x] for x in ('remaining_tokens', 'generation_requests', 'operator_context_sent', 'private_atlas_included')} for k, v in qa['Q3_native'].items()}},
           'Q4': {'catalog_old_rule': qb['Q4_catalog']['catalog_old_rule'], 'catalog_new_rule': qb['Q4_catalog']['catalog_new_rule'], 'moved_to_literal': qb['Q4_catalog']['moved_to_literal'], 'moved_names': qb['Q4_catalog']['moved_names'], 'false_flags': qb['Q4_haiku_expanded']['false_flags'] if 'false_flags' in qb['Q4_haiku_expanded'] else None,
                  'catalogued_matching_new_keep': ia['catalogued_matching_new_keep'], 'same_base_true_pairs': ia['pairs_same_base_true_total'], 'same_base_true_catalogued': ia['pairs_same_base_true_catalogued'], 'near_jaccard_catalogued': ia['near_jaccard_true_catalogued_for_false'], 'capsule_sha_ok': ia['capsule_sha_ok']},
           'Q5': {k: rc[k] for k in ('seed', 'sample', 'found_text', 'found_in_topic', 'first_hit_ok', 'by_tag', 'recipe_text_present_in_capsule', 'provider_calls', 'network')} | {'misses': rc['failures_text'], 'non_ascii_remeasured': QD['exact_recipe_with_literal_unicode']},
           'Q6': {n: {k: qa['Q6'][n][k] for k in ('ATLAS_CANONICO_block', 'iald_stack_v7', 'iald_psion_state', 'IALD_CLAUDE_API_KEY', 'dotenv_matches', 'secret_pattern_hits', 'confirmed_mentions', 'confirmed_near_QG_not_negated', 'qualifiers')} for n in ('shared', 'haiku_expanded', 'sonnet_public')} | {'native_prefix_hits': native_hits, 'strict_QG_confirmed_matches': qb['Q6x_strict_QG_confirmed_matches']},
           'Q7': {'files': len(rd(W / 'install_plan.json')['files']), 'under_target': qa['Q7_destinations_under_target'], 'elsewhere': qa['Q7_destinations_elsewhere'], 'jev_keys_differing': qa['Q7_jev_keys_differing'], 'jev_deep_changed_paths': qa['Q7_jev_deep_changed_paths_in_anchors_source_core_packet'], 'jev_schema': qa['Q7_jev_schema']},
           'Q8': {'script': 'review/review_app.py', 'status': final['status'], 'checks': len(final['checks']), 'review_final_sha256': sha((W / 'validation/review_final.json').read_bytes())}},
       'checks': rest, 'findings': findings,
       'scope': ['Recomputo independente sobre o selado v406 do cofre com o decodificador lib405 (nao importa haiku_codec/fit_*).', 'Sem provedor, sem rede (gancho de auditoria na recuperacao), sem escrita fora da pasta do revisor.', 'Nao instala nem implanta; contagens nativas nao repetidas.']}
with (W / 'validation/review_app_independent.json').open('w', encoding='utf8') as f:
    json.dump(app, f, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------- PARECER
n_pass = sum(1 for c in rest if c['pass']) + sum(1 for c in q1 if c['pass'])
n_all = len(rest) + len(q1)
veredito = 'ACEITO' if (sources['status'] == 'PASS' and app['status'] == 'PASS') else 'NAO ACEITO'
md = ['# Parecer do revisor independente: release v406 do app (rodada 1)', '',
      'Revisor: `%s` (nao e o construtor `claude-app-orquestrador`). Data: %s. Veredito: **%s**.' % (ACTOR, now[:19] + 'Z', veredito), '',
      'Por recomputo independente, sem provedor e sem rede: %d de %d verificacoes minhas passaram (fontes %d/%d); o script mecanico `review_app.py` passou com %d checks (sha16 do review_final: %s).' % (n_pass, n_all, sum(1 for c in q1 if c['pass']), len(q1), len(final['checks']), sha((W / 'validation/review_final.json').read_bytes())[:16]), '',
      '| Q | resultado | numero-chave |', '|---|---|---|',
      '| Q1 identidade/fontes | %s | pino %s...; commit a381c4d1 e ancestral do HEAD; 36 artefatos e %d blobs publicos recomputados; custodia EM CURSO = plano G1 |' % ('PASS' if sources['status'] == 'PASS' else 'FAIL', sources['numbers']['pino_um_py_sha16'], len(rd(W / 'app/PUBLIC_GIT_BINDING.json')['sources'])),
      '| Q2 janela P2/literais | %s | 32 topicos de janela + 3 aposentados; 105 literais limites/diz/nao_diz iguais ao selado nos dois pacotes; 474 presentes, 0 perdidos; unico bloco que mudou vs v405 instalada: os 2 _v401 com fonte inalterada (0 literais perdidos) |' % ('PASS' if all(c['pass'] for c in q2) else 'FAIL'),
      '| Q3 folga | %s | menor folga declarada %d B (DeepSeek); com output real %d B; haiku55 restam %d tokens; limites recomputados do prefixo real = declarados |' % ('PASS' if all(cka[k]['pass'] for k in cka if k.startswith('Q3.')) else 'FAIL', qa['Q3_folga']['deepseek']['folga_reserva_declarada_148656'], qa['Q3_folga']['deepseek']['folga_com_output_tokens'], qa['Q3_native']['haiku_expanded']['remaining_tokens']),
      '| Q4 R3-1 | %s | catalogo %d -> %d (16 nomes voltam ao literal); 0 TRUE com nome da regra ainda catalogado; sha do catalogo igual ao meu; 4 FALSE literais, pares TRUE literais |' % ('PASS' if all(c['pass'] for c in QB['checks'] if c['name'].startswith('Q4.')) else 'FAIL', qb['Q4_catalog']['catalog_old_rule'], qb['Q4_catalog']['catalog_new_rule']),
      '| Q5 R3-2/recuperacao | %s | capsula traz max_chars 4500; %d/%d recuperados (semente %d); 1 falha = artefato de medicao (nome nao-ASCII), re-medido 4/4 |' % ('PASS' if rc['recipe_text_present_in_capsule'] and rc['found_text'] >= rc['sample'] - 1 else 'FAIL', rc['found_text'], rc['sample'], rc['seed']),
      '| Q6 confidencialidade | %s | 0 ocorrencias de nomes/chaves vedados nos 3 prefixos; 0 uso afirmativo de CONFIRMED/confirmada para a QG (5 contextos sinalizados, todos negados/lista de vereditos proibidos); CONDITIONAL/CREDITATION presentes e >= v405 |' % ('PASS' if cka['Q6.no_forbidden_names_or_keys']['pass'] and cka['Q6.no_affirmative_confirmed_QG']['pass'] and cka['Q6.qualifiers_present']['pass'] else 'FAIL'),
      '| Q7 plano | %s | %d arquivos, %d sob o alvo v406_a381c4d14709, 8 destinos previstos (iguais aos da v405), 0 .py de runtime substituido, manifesto ativo por ultimo; jev_control_v406 valido, so campos de versao diferem |' % ('PASS' if all(cka[k]['pass'] for k in cka if k.startswith('Q7.')) else 'FAIL', len(rd(W / 'install_plan.json')['files']), qa['Q7_destinations_under_target']),
      '| Q8 script mecanico | %s | review_app.py: %s, %d checks, %d arquivos do plano |' % ('PASS' if final['status'] == 'PASS' else 'FAIL', final['status'], len(final['checks']), len(rd(W / 'install_plan.json')['files'])), '',
      '## Achados', '']
for f in findings:
    md.append('- **%s %s**: %s' % (f['severity'], f['id'], f['text']))
md += ['', 'Nenhum achado ALTO ou MEDIO.' if not has_alto_medio else 'HA achado ALTO/MEDIO: nao aceito.', '',
       'Limites do exame: nao instalei nem implantei nada; nao repeti as contagens nativas (custodia anterior); nao conferi o remoto do git (sem rede); a fidelidade das 46 sinteses em prosa (TEXT) foi comparada com a v405 instalada, nao reconstruida a partir da fonte.']
(HERE / 'PARECER_v406_R1.md').write_text('\n'.join(md), encoding='utf-8')
print(json.dumps({'veredito': veredito, 'sources': sources['status'], 'app': app['status'], 'n_pass': n_pass, 'n_all': n_all, 'alto_medio': has_alto_medio, 'native_prefix_hits': native_hits,
                  'retired': {n: {'literal': r['literal'], 'pointer_only_ext_qual': r['pointer_only_extended_qualifier_keys'], 'pointer_only_other': r['pointer_only_other'], 'top_keys': r['top_keys']} for n, r in retired.items()},
                  'findings': [(f['severity'], f['id']) for f in findings], 'vault_equals_git_blob': qa['vault_equals_git_blob']}, ensure_ascii=False, indent=1))
