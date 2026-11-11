"""Preserve the actual post-v408 runtime and client, with no secret reads."""
import hashlib
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')


def verify():
    baseline = json.loads((WORK / 'PRESERVATION_BASELINE.json').read_bytes())
    result = {}
    for row in baseline['files']:
        path = Path(row['path'])
        if path.resolve(strict=True) != path or not path.is_relative_to(ROOT):
            raise RuntimeError('Invalid preservation path')
        result[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
    if not result or not all(result.values()):
        raise RuntimeError('Existing runtime/client changed; reconcile before deployment')
    return result


def approved_restart():
    approval = json.loads((WORK / 'APROVACAO_V409.json').read_bytes())
    if approval.get('release') != 'v409' or approval.get('restart_web_8082') is not True:
        raise RuntimeError('Explicit operator decision for v409 restart is required')
    source = Path(approval['operator_reply_path'])
    if source.resolve(strict=True) != source or source.parent != WORK:
        raise RuntimeError('Approval source outside this mission')
    if hashlib.sha256(source.read_bytes()).hexdigest() != approval['operator_reply_sha256']:
        raise RuntimeError('Approval source changed')
    return approval
