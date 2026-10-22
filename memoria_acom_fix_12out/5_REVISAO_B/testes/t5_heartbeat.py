# Revisor B: heartbeat functions extracted by AST from the candidate web server (no import of the server,
# no network, no production path). Psion path redirected to a synthetic sandbox file.
import ast, os, sys, json, math, time, hashlib, secrets, subprocess, threading
from datetime import datetime
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'copia', 'projetos_pyhton', 'IALD', 'iald_web_server.py')
SB = os.path.join(HERE, 'sb_heartbeat')
if os.path.exists(SB):
    subprocess.run(['cmd', '/c', 'rmdir', '/s', '/q', SB])
os.makedirs(SB)
tree = ast.parse(open(SRC, encoding='utf-8').read())
want_funcs = {'_heartbeat_payload', '_heartbeat_payload_sha256', '_heartbeat_psion_admissible', '_heartbeat_tok_s',
              '_heartbeat_measure', '_heartbeat_aggregate', '_load_psion_state', '_save_psion_state',
              '_heartbeat_telemetry_rotate', '_heartbeat_telemetry_append', '_heartbeat_class',
              '_heartbeat_record_memory_if_due', '_heartbeat_health_load', '_heartbeat_health_save', '_update_psion_from_heartbeat'}
nodes = []
for n in tree.body:
    if isinstance(n, ast.FunctionDef) and n.name in want_funcs:
        nodes.append(n)
    elif isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and (t.id.startswith('HEARTBEAT_') or t.id in ('_ALPHA_FINE', '_SQRT_E', '_BETA_TGL', '_BETA_RED')) for t in n.targets):
        nodes.append(n)
mod = ast.Module(body=nodes, type_ignores=[])
ns = {'os': os, 'json': json, 'math': math, 'time': time, 'hashlib': hashlib, 'secrets': secrets, 'datetime': datetime,
      'SERVE_DIR': SB, 'threading': threading}
exec(compile(mod, SRC, 'exec'), ns)
R = {}
# H1: telemetry cap/rotation
ns['HEARTBEAT_LOG_DIR'] = os.path.join(SB, 'logs'); ns['HEARTBEAT_TELEMETRY_FILE'] = os.path.join(SB, 'logs', 'tel.jsonl')
ns['HEARTBEAT_TELEMETRY_MAX_BYTES'] = 2000
for i in range(200):
    ns['_heartbeat_telemetry_append']({'kind': 'beat', 'i': i, 'samples': [{'x': 'y' * 20}]})
files = sorted(os.listdir(os.path.join(SB, 'logs')))
R['H1_rotation'] = {'files': files, 'max_size': max(os.path.getsize(os.path.join(SB, 'logs', f)) for f in files),
                    'keep': ns['HEARTBEAT_TELEMETRY_KEEP'], 'real_cap_bytes': 4 * 1024 * 1024}
# H2: partial measurement admissibility (1 of 5 prompts, 1 of 2 runs)
pay = ns['_heartbeat_payload'](ns['HEARTBEAT_SYSTEM_MESSAGE'], ns['HEARTBEAT_PROMPTS'][2])
sha = ns['_heartbeat_payload_sha256'](pay)
partial = {'regime': 'generation_only', 'status': 'ok', 'results': [{'avg_tok_s': 140.0, 'variance': 0.0}],
           'samples': [{'prompt': 2, 'run': 0, 'ok': True, 'tok_s': 140.0, 'formula': 'timings.predicted_n/predicted_ms', 'payload_sha256': sha},
                       {'prompt': 0, 'run': 0, 'ok': False, 'http': 503}], 'formulas': ['timings.predicted_n/predicted_ms']}
R['H2_partial_1_of_10_samples_admissible'] = ns['_heartbeat_psion_admissible'](partial)
mixed = dict(partial); mixed['formulas'] = ['timings.predicted_n/predicted_ms', 'completion_tokens/elapsed']
mixed['samples'] = partial['samples'] + [{'prompt': 3, 'run': 0, 'ok': True, 'tok_s': 9.0, 'formula': 'completion_tokens/elapsed',
                                          'payload_sha256': ns['_heartbeat_payload_sha256'](ns['_heartbeat_payload'](ns['HEARTBEAT_SYSTEM_MESSAGE'], ns['HEARTBEAT_PROMPTS'][3]))}]
R['H2b_mixed_formulas_admissible'] = ns['_heartbeat_psion_admissible'](mixed)
# H3: psion load failure -> fresh state saved over the (synthetic) file?
fake = os.path.join(SB, 'iald_psion_state_32B.json')
with open(fake, 'wb') as f:
    f.write(b'{"beta_tgl": 0.012031300400803142, "generation": 777, "heartbeat": {"baseline_tok_s": 88.8}, "SYNTH": "\xc3\xa9"')  # truncated JSON (synthetic)
ns['HEARTBEAT_STATE_FILE'] = fake
before = open(fake, 'rb').read()
psion = ns['_load_psion_state']()
R['H3_load_on_corrupt'] = {'returned_generation': psion.get('generation'), 'returned_has_heartbeat': 'heartbeat' in psion}
psion = ns['_update_psion_from_heartbeat'](psion, 140.0, 0.01, 5)
ns['_save_psion_state'](psion)
after = open(fake, 'rb').read()
baks = [n for n in os.listdir(SB) if '.bak_' in n]
R['H3_load_on_corrupt'].update({'file_replaced_by_fresh_state': before != after and b'"generation": 1' in after,
                                'daily_bak_created': baks, 'bak_equals_original_bytes': bool(baks) and open(os.path.join(SB, baks[0]), 'rb').read() == before})
# H3b: second corrupt load on the same day -> no new bak (the earlier bak already exists)
with open(fake, 'wb') as f:
    f.write(b'{"generation": 900, "beta_tgl": 0.012031300400803142, "heartbeat": {"baseline_tok_s": 77.7, "total_beats": 900}}')
good_state = open(fake, 'rb').read()
with open(fake, 'ab') as f:
    f.write(b'GARBAGE')  # now corrupt again
p2 = ns['_load_psion_state'](); p2 = ns['_update_psion_from_heartbeat'](p2, 140.0, 0.01, 5); ns['_save_psion_state'](p2)
R['H3b_second_corruption_same_day'] = {'generation_900_lost': b'"generation": 900' not in open(fake, 'rb').read() and
                                       all(b'"generation": 900' not in open(os.path.join(SB, n), 'rb').read() for n in os.listdir(SB) if '.bak_' in n)}
# H4: memory cadence: class flapping, every beat
ns['HEARTBEAT_HEALTH_FILE'] = os.path.join(SB, 'logs', 'health.json')
calls = []
class FakeApp:
    @staticmethod
    def record_measurement(*a, **k):
        calls.append(k.get('event_id')); return {'revision': len(calls), 'context_id': 'x'}
ns['app_memory'] = FakeApp
now = 1_000_000.0
events = []
for beat, klass in enumerate(['ok', 'alerta', 'ok', 'alerta', 'ok', 'ok', 'ok', 'ok']):
    events.append(ns['_heartbeat_record_memory_if_due'](klass, {'at': str(beat)}, 'sha%d' % beat, now + beat * 1800) is not None)
R['H4_cadence_flapping_30min_beats'] = {'classes': ['ok', 'alerta', 'ok', 'alerta', 'ok', 'ok', 'ok', 'ok'], 'memory_event_written': events}
with open(os.path.join(HERE, 't5_result.json'), 'w', encoding='utf-8') as f:
    json.dump(R, f, ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
