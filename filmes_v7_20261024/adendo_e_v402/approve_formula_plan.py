"""Record the parent's completed textual review of one explicitly pinned plan."""
import argparse, datetime, hashlib, json, os, sys
from pathlib import Path

E = Path(__file__).resolve().parent
sys.path.insert(0, str(E.parent))
import mission

def read(path): return json.loads(Path(path).read_bytes())
def pin(path):
    path = Path(path)
    raw = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
def verify(value):
    actual = pin(value['path'])
    assert actual == value, value['path']
def save(path, value):
    assert not path.exists(), 'Existing approval must be reconciled explicitly'
    raw = (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
    temporary = path.with_name(path.name+'.tmp')
    with temporary.open('xb') as stream: stream.write(raw)
    assert temporary.read_bytes() == raw
    os.replace(temporary, path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reviewed-plan', required=True)
    args = parser.parse_args()
    review = read(E/'FORMULA_NARRATION_REVIEW.json')
    assert review['plan_sha256'] == args.reviewed_plan
    independent = read(E/'FORMULA_NARRATION_INDEPENDENT_REVIEW.json')
    assert independent['status'].startswith('PASS'), 'Independent textual findings unresolved'
    assert independent['plan_sha256'] == args.reviewed_plan, 'Independent review is stale'
    contract = read(E/'FORMULA_NARRATION_APPROVAL_CONTRACT.json')
    project = mission.project()
    task = next(t for t in project['projection']['active'] if t['id']=='V402_FORMULA_NARRATION')
    preflight = mission.call({'operation':'check', **mission.current('codex-video-v7'),
                             'task_id': task['id'], 'lease_id':task['lease']['id'], 'max_chars':100000})
    assert preflight['ready']
    for name, spec in contract['required_approval_files'].items():
        data = dict(spec['required_fields'])
        assert data['plan_sha256'] == args.reviewed_plan
        for value in data.values():
            if isinstance(value, dict) and {'path','sha256','bytes'} <= value.keys(): verify(value)
        data.update(status='PASS_APPROVED_FOR_PUBLIC_TTS', actor='codex-video-v7',
                    reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    independent_review=pin(E/'FORMULA_NARRATION_INDEPENDENT_REVIEW.json'),
                    preflight=preflight,
                    scope='Textual meaning and four-language alignment reviewed; actual duration and perception remain separate.',
                    review_notes=[
                        'Fine-structure constant, derived beta TGL coupling and entropic factor explained by role.',
                        'Euler number distinct from entropy; boundary exponentiation described.',
                        'Identity, reflection, modular density, transport, curvature and spin explained as operations.',
                        'Hypotheses remain explicit; no promotion to empirical confirmation.',
                        'Adendo D terminology and distinct status of three supports preserved.',
                        '224/360 seconds retained; actual voice fit must pass without acceleration or truncation.',
                        'Only public narration to authorized Edge voices; personal voice excluded.'
                    ])
        save(E/name, data)
    print(json.dumps({'status':'PASS_APPROVED_FOR_PUBLIC_TTS','plan_sha256':args.reviewed_plan}))

if __name__ == '__main__': main()
