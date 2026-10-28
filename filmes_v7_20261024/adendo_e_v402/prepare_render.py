"""Freeze verified inputs and record intent before one browser capture pipeline."""
from pathlib import Path
import datetime, hashlib, json, os, sys
from finalizer_guards import validate_frozen_data, validate_replay, validate_audio

E = Path(__file__).resolve().parent
W = E.parent
V = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
N = V.parent.parent / 'Nós'
sys.path.insert(0, str(W))
sys.path.insert(0, str(V/'cinema'))
import mission
from bootstrap import cli, REF, ACTOR
from render_sources import collect

def read(p): return json.loads(p.read_bytes())
def pin(p):
    b = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
def save(p, value):
    assert not p.exists(), 'Recover existing intent; do not start another capture'
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
    tmp = p.with_suffix('.tmp')
    with tmp.open('xb') as f: f.write(raw)
    assert tmp.read_bytes() == raw
    os.replace(tmp, p)

def main():
    assert not (E/'RENDER_INTENT.json').exists(), 'Inspect existing intent/jobs first'
    p = mission.project()
    t = next(t for t in p['projection']['active'] if t['id'] == 'ADENDO_E_V402')
    check = mission.call({'operation': 'check', **mission.current(ACTOR['id']),
        'task_id': t['id'], 'lease_id': t['lease']['id'], 'max_chars': 100000})
    assert check['ready']
    source = validate_frozen_data(E, V, N)
    validate_replay(V, source)
    audio = validate_audio(E, V, source)
    found = []
    for job in (V/'cinema/render/jobs').glob('*.json'):
        if '.bak_' in job.name: continue
        d = read(job)
        if d.get('metadata', {}).get('source') == 'v402': found.append(str(job))
    assert not found, 'Existing v402 job(s): inspect, do not repeat ' + repr(found)
    prepared = read(E/'MEDIA_PREPARED.json')
    assert prepared['source'] == 'v402'
    intent = {'status': 'INTENT_BEFORE_SINGLE_BROWSER_PIPELINE',
        'created_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source': 'v402', 'source_sha256': source,
        'seal': pin(N/'um_absoluto_selo.json'),
        'url': 'http://127.0.0.1:8797/cinema/index.html?pipeline=all',
        'render_closure': collect(V),
        'data_ready': pin(E/'DATA_READY.json'), 'audio_ready': pin(E/'AUDIO_READY.json'),
        'numeric_review': pin(E/'PARENT_NUMERIC_REVIEW.json'),
        'media_prepared': pin(E/'MEDIA_PREPARED.json'),
        'personal_voice': 'EXCLUDED_AWAITING_HUMAN_LISTENING', 'preflight': check}
    save(E/'RENDER_INTENT.json', intent)
    s = cli(r'C:\IALD\MEMORIA_IALD\session_memory.py', {'operation': 'get', 'reference': str(REF)})['result']
    handles = s['p']['handles']
    hid = 'v402-adendo-e-pipeline-20261027'
    assert not any(h['id'] == hid for h in handles)
    handles.append({'id': hid, 'kind': 'local_render_pipeline', 'task_id': t['id'],
        'status': 'prepared', 'version': 'v402', 'evidence': str(E/'RENDER_INTENT.json')})
    result = cli(r'C:\IALD\MEMORIA_IALD\session_memory.py', {'operation': 'transition',
        'reference': str(REF), 'actor': ACTOR, 'expected_revision': s['revision'],
        'event_id': 'ordem022-v402-pipeline-intent', 'changes': {'flow': {
            'phase': 'v402_render_prepared', 'next_action': 'Open recorded pipeline once; recover jobs by identity before any retry.', 'handles': handles}}})
    assert result['ok']
    save(E/'RENDER_INTENT_ACOM.json', result)
    print(json.dumps({'status': intent['status'], 'dependencies': len(intent['render_closure']), 'source': source}))

if __name__ == '__main__': main()
