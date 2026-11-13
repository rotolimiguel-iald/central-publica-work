"""Preserve the actual post-v408 runtime and client, with no secret reads."""
import hashlib
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')


def runtime_delta():
    path = WORK / 'RUNTIME_DELTA_R4.json'
    raw = path.read_bytes()
    value = json.loads(raw)
    review = json.loads((WORK / 'validation/review_final.json').read_bytes())
    if review.get('status') != 'PASS' or review.get('runtime_delta_sha256') != hashlib.sha256(raw).hexdigest():
        raise RuntimeError('Runtime delta lacks matching independent review')
    rows = value['files']
    allowed = {}
    for row in rows:
        path = Path(row['destination'])
        source = Path(row['source'])
        if path != path.resolve() or path.parent != ROOT or path.suffix != '.py' or path in allowed:
            raise RuntimeError('Invalid runtime delta destination')
        if not source.resolve().is_relative_to(WORK) or hashlib.sha256(source.read_bytes()).hexdigest() != row['sha256']:
            raise RuntimeError('Changed runtime staging')
        allowed[path] = row
    return allowed


def verify(*, installed=False):
    baseline = json.loads((WORK / 'PRESERVATION_BASELINE.json').read_bytes())
    delta = runtime_delta()
    result = {}
    for row in baseline['files']:
        path = Path(row['path'])
        if path.resolve(strict=True) != path or not path.is_relative_to(ROOT):
            raise RuntimeError('Invalid preservation path')
        expected = delta[path]['sha256'] if installed and path in delta else row['sha256']
        if path in delta and delta[path]['baseline'] != row['sha256']:
            raise RuntimeError('Runtime delta does not preserve original baseline')
        result[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest() == expected
    for path, row in delta.items():
        measured = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
        result[str(path)] = measured == (row['sha256'] if installed else row['baseline'])
    if not result or not all(result.values()):
        raise RuntimeError('Existing runtime/client changed; reconcile before deployment')
    return result


def approved_restart():
    approval = json.loads((WORK / 'APROVACAO_V410.json').read_bytes())
    if approval.get('release') != 'v410' or approval.get('restart_web_8082') is not True:
        raise RuntimeError('Explicit operator decision for v410 restart is required')
    source = Path(approval['operator_reply_path'])
    if source.resolve(strict=True) != source or source.parent != WORK:
        raise RuntimeError('Approval source outside this mission')
    if hashlib.sha256(source.read_bytes()).hexdigest() != approval['operator_reply_sha256']:
        raise RuntimeError('Approval source changed')
    return approval
