"""Revisor independente F0.3 v407 - Q6 (pins/ativacao/quadro) e Q7 (recuperacao) - somente leitura. Saida: review\\REV_Q6_Q7.json"""
import sys, os, json, hashlib, re, datetime
sys.dont_write_bytecode = True
from pathlib import Path

BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.path.insert(0, str(BASE))
from iald_orchestrator import canonical_memory as cm
from iald_orchestrator import program_controls as pc

W = Path(r'C:\IALD\Central de Patentes\work\scientific_memory_sync_20261104_v407')
REV = W / 'review'
EPOCH = 'v407_4323b401f15cc971'
REL = cm.RELEASES / EPOCH
SNAP = REL / 'snapshots' / EPOCH
UNIT = 'F0.3.MEMORIA_CIENTIFICA_SYNC'
MEMBER = 'claude-app-orquestrador'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pin(p):
    p = Path(p)
    st = p.stat()
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': sha(b), 'sha16': sha(b)[:16],
            'mtime_local': datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'mtime_before_today': datetime.datetime.fromtimestamp(st.st_mtime).date() < datetime.date(2026, 11, 4)}


out = {'problems': []}
prep = json.loads((W / ('PREPARATION_' + EPOCH + '.json')).read_bytes())
manifest = json.loads((REL / 'manifest.json').read_bytes())

# ---------- Q6
q6 = {}
mod = pin(cm.__file__)
q6['canonical_memory_pin_now'] = mod
q6['canonical_memory_pin_in_PREPARATION'] = prep['module_pin']
q6['canonical_memory_sha_eq_prep'] = (mod['sha256'] == prep['module_pin']['sha256'] and mod['bytes'] == prep['module_pin']['bytes'])
q6['canonical_memory_mtime_before_today'] = mod['mtime_before_today']
if not q6['canonical_memory_sha_eq_prep']:
    out['problems'].append('canonical_memory.py differs from PREPARATION module_pin')
orch = BASE / 'iald_orchestrator'
q6['other_module_pins'] = {n: pin(orch / n) for n in ('program_controls.py', 'safe_files.py', 'process_lock.py', 'policy.py', 'matrix.py', '__init__.py')}
q6['helper_and_wrapper_pins'] = {
    'scientific_memory_sync.py': pin(r'C:\IALD\Central de Patentes\work\scientific_memory_sync_20261013\scientific_memory_sync.py'),
    'rodar_f03_v407.py': pin(W / 'rodar_f03_v407.py'),
    'PROGRAMA.json_sha16_now': sha(Path(r'C:\IALD\PROGRAMA_IALD\PROGRAMA.json').read_bytes())[:16],
}
active_raw = Path(cm.ACTIVE).read_bytes()
active = json.loads(active_raw)
bp = prep['baseline_active_pin']
q6['ACTIVE_now'] = {'bytes': len(active_raw), 'sha256': sha(active_raw), 'content': active, 'mtime_local': datetime.datetime.fromtimestamp(Path(cm.ACTIVE).stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}
q6['baseline_active_pin_in_PREPARATION'] = bp
q6['CAS_expected_sha_eq_ACTIVE_now'] = (bp['sha256'] == sha(active_raw) and bp['bytes'] == len(active_raw) and bp['path'] == str(cm.ACTIVE))
q6['ACTIVE_content_eq_PREPARATION_previous_active'] = active == prep['previous_active']
if not q6['CAS_expected_sha_eq_ACTIVE_now']:
    out['problems'].append('CAS: baseline_active_pin != ACTIVE now')
# does ACTIVE.json formatting match save_json (indent=2, ensure_ascii False)? -> lets me predict the post-activation bytes
q6['ACTIVE_now_bytes_eq_save_json_format'] = json.dumps(active, ensure_ascii=False, indent=2).encode('utf-8') == active_raw
pointer = {'schema': 1, 'release': json.loads((SNAP / 'SEALED_SNAPSHOT.json').read_bytes())['release'], 'epoch': REL.name,
           'generation': manifest['generation'], 'manifest_sha256': sha((REL / 'manifest.json').read_bytes())}
predicted = json.dumps(pointer, ensure_ascii=False, indent=2).encode('utf-8')
q6['predicted_pointer_after_activation'] = pointer
q6['predicted_ACTIVE_bytes'] = len(predicted)
q6['predicted_ACTIVE_sha256'] = sha(predicted)
q6['predicted_pointer_passes_resolve_directory_rules'] = {
    'keys_exact': set(pointer) == {'schema', 'release', 'epoch', 'generation', 'manifest_sha256'},
    'epoch_regex': re.fullmatch(r'v[0-9]+_[0-9a-f]{16}', pointer['epoch']) is not None,
    'epoch_eq_release_plus_generation16': pointer['epoch'] == pointer['release'] + '_' + pointer['generation'][:16],
    'manifest_sha_eq_pointer': sha((REL / 'manifest.json').read_bytes()) == pointer['manifest_sha256'],
    'manifest_generation_eq_pointer': manifest['generation'] == pointer['generation'],
    'manifest_source_mode_ok': manifest.get('source_mode') == cm.SNAPSHOT_MODE,
    'release_dir_under_RELEASES': REL.resolve(strict=True).parent == cm.RELEASES.resolve(strict=True),
}
# claim check, with the module's own function (read-only) and a negative control
try:
    q6['require_claim_ok'] = pc.require_claim(UNIT, MEMBER)
except Exception as ex:  # noqa
    q6['require_claim_ok'] = 'RAISED: ' + str(ex)
    out['problems'].append('require_claim raised for claude-app-orquestrador')
try:
    pc.require_claim(UNIT, 'codex-coordenadora')
    q6['require_claim_negative_control_codex_coordenadora'] = 'NOT RAISED (unexpected)'
except Exception as ex:  # noqa
    q6['require_claim_negative_control_codex_coordenadora'] = 'raised as expected: ' + str(ex)
board = pc.read_board()
u = [x for x in board['unidades'] if x['id'] == UNIT]
q6['unit'] = {'n_matches': len(u), 'status': u[0]['status'], 'gate': u[0].get('gate'), 'reivindicacao': u[0].get('reivindicacao'),
              'dono': u[0].get('dono'),
              'now_local': datetime.datetime.now().astimezone().isoformat(),
              'claim_still_valid': datetime.datetime.fromisoformat(u[0]['reivindicacao']['vence_em']) > datetime.datetime.now().astimezone()}
q6['activate_release_unit_whitelist_contains_unit'] = UNIT in ('F0.3', 'F9.2', 'F0.3.MEMORIA_CIENTIFICA_SYNC')
q6['lock_file'] = {'path': str(cm.ACTIVE) + '.worker.lock', 'exists': Path(str(cm.ACTIVE) + '.worker.lock').exists(),
                   'bytes': Path(str(cm.ACTIVE) + '.worker.lock').stat().st_size if Path(str(cm.ACTIVE) + '.worker.lock').exists() else None}
out['Q6'] = q6

# ---------- Q7
q7 = {}
ver = json.loads((W / 'VERIFY_RESULT.json').read_bytes())
q7['VERIFY_RESULT'] = {'status': ver['status'], 'epoch': ver['epoch'], 'generation_eq_manifest': ver['generation'] == manifest['generation'],
                       'documents': ver['documents'], 'chunks': ver['chunks'], 'checks': ver['checks'], 'provider_calls': ver['provider_calls'], 'source_execution': ver['source_execution']}
q7['VERIFY_modes'] = {}
for mode, r in ver['retrieval'].items():
    q7['VERIFY_modes'][mode] = {'generation_eq_manifest': r['generation'] == manifest['generation'], 'index_sha256_eq_manifest': r['index_sha256'] == manifest['index_sha256'],
                                'packet_sha256': r['packet_sha256'], 'n_sources': len(r['sources']), 'freshness': r['freshness'], 'memory_mode': r['memory_mode'],
                                'document_pins_eq_manifest': all(any(d['name'] == p['name'] and d['sha256'] == p['sha256'] and d['bytes'] == p['bytes'] for d in manifest['documents']) for p in r['document_pins']),
                                'sources_all_sha_match_manifest': all(any(d['name'] == s['file'] and d['sha256'] == s['sha256'] for d in manifest['documents']) for s in r['sources'])}
    if not (q7['VERIFY_modes'][mode]['generation_eq_manifest'] and q7['VERIFY_modes'][mode]['index_sha256_eq_manifest']):
        out['problems'].append('VERIFY mode ' + mode + ' generation/index differ')

# own recovery, standard mode, same call as the helper's verify()
query = ' '.join(prep['statute_record_names'])
ALLOWED = ['um.py', 'um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_forma_canonica.md']
p = cm.prepare(query, REL, allowed_sources=ALLOWED, mode='standard', max_chars=24000)
rc = p['receipt']
q7['own_standard'] = {'receipt_generation_eq_manifest': rc['generation'] == manifest['generation'], 'packet_sha256': rc['packet_sha256'],
                      'packet_sha256_eq_digest_of_prompt': rc['packet_sha256'] == sha(p['prompt'].encode()),
                      'equals_VERIFY_standard_packet_sha256': rc['packet_sha256'] == ver['retrieval']['standard']['packet_sha256'],
                      'freshness': rc['freshness'], 'index_sha256_eq_manifest': rc['index_sha256'] == manifest['index_sha256'],
                      'context_bytes': rc['context_bytes'], 'n_sources': len(rc['sources']), 'blocked': rc['blocked_passages'], 'budget_skipped': rc['budget_skipped_passages'],
                      'folded': rc['folded'], 'retrieval_scope': rc['retrieval_scope'], 'weights_modified': rc['weights_modified'],
                      'receipt_sources_eq_VERIFY_standard_sources': rc['sources'] == ver['retrieval']['standard']['sources']}
if not (q7['own_standard']['receipt_generation_eq_manifest'] and q7['own_standard']['packet_sha256_eq_digest_of_prompt']):
    out['problems'].append('own standard recovery inconsistent')
# cross-check each retrieved passage (file, first_line, last_line) against the snapshot text
prompt = p['prompt']
cross = []
for s in rc['sources']:
    pre = '\nFONTE ' + json.dumps(s, ensure_ascii=False) + '\n'
    i = prompt.find(pre)
    ok_found = i >= 0
    body = None
    if ok_found:
        j = prompt.find('\nFIM DO TRECHO\n', i + len(pre))
        body = prompt[i + len(pre):j]
    text = (SNAP / s['file']).read_bytes().decode('utf-8-sig')
    lines = text.splitlines(keepends=True)
    full = ''.join(lines[s['first_line'] - 1:s['last_line']])
    exact = body == full
    piece = (s['first_line'] == s['last_line'] and body is not None and body in full)
    cross.append({'file': s['file'], 'first_line': s['first_line'], 'last_line': s['last_line'], 'found_in_prompt': ok_found, 'body_eq_lines_slice': exact, 'body_is_piece_of_long_line': (piece and not exact),
                  'sha_eq_manifest': any(d['name'] == s['file'] and d['sha256'] == s['sha256'] for d in manifest['documents'])})
q7['own_standard_passage_crosscheck'] = cross
q7['own_standard_all_passages_faithful'] = all(c['found_in_prompt'] and (c['body_eq_lines_slice'] or c['body_is_piece_of_long_line']) and c['sha_eq_manifest'] for c in cross)
if not q7['own_standard_all_passages_faithful']:
    out['problems'].append('some retrieved passage does not match its line slice')
# header facts printed by the packet
hdr = prompt.split('\nTRECHOS RECUPERADOS')[0]
q7['own_standard_header_tail'] = hdr[-900:]

# a v407-specific retrieval: does the new release answer from the NEW content?
p2 = cm.prepare('UM_VERSION v407 rodada selo', REL, allowed_sources=ALLOWED, mode='standard', max_chars=24000)
q7['own_v407_probe'] = {'generation_eq_manifest': p2['receipt']['generation'] == manifest['generation'], 'n_sources': len(p2['receipt']['sources']),
                        'prompt_mentions_v407': 'v407' in p2['prompt'], 'count_v407_in_prompt': p2['prompt'].count('v407'),
                        'files_in_sources': sorted({s['file'] for s in p2['receipt']['sources']}), 'packet_sha256': p2['receipt']['packet_sha256']}
# and the same probe against the ACTIVE (v404) release: the probe should show OLD content (informational: shows what changes at activation)
try:
    p3 = cm.prepare('UM_VERSION v407 rodada selo', None, allowed_sources=ALLOWED, mode='standard', max_chars=24000)
    q7['probe_via_ACTIVE_pointer_today'] = {'generation16': p3['receipt']['generation'][:16], 'prompt_mentions_v407': 'v407' in p3['prompt'], 'count_v407_in_prompt': p3['prompt'].count('v407')}
except Exception as ex:  # noqa
    q7['probe_via_ACTIVE_pointer_today'] = 'RAISED ' + str(ex)
out['Q7'] = q7
out['iald_memory_imported'] = 'iald_memory' in sys.modules
(REV / 'REV_Q6_Q7.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print('problems:', out['problems'])
print(json.dumps(out['Q6'], ensure_ascii=False, indent=1))
print(json.dumps({k: v for k, v in out['Q7'].items() if k not in ('own_standard_passage_crosscheck', 'own_standard_header_tail')}, ensure_ascii=False, indent=1))
print('crosscheck rows:', len(cross), [(c['file'], c['first_line'], c['last_line'], c['body_eq_lines_slice'], c['body_is_piece_of_long_line']) for c in cross])
