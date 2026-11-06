"""Install the independently reviewed tool/stream fixes as a separate transaction."""
import ast
import json
from pathlib import Path

from maintenance import assert_quiesced
from transaction import ROOT, WORK, atomic, backup, digest, write_evidence

STAGE = WORK / 'integration_review'
PLAN = STAGE / 'PATCH_PLAN_R2.json'
REVIEW = WORK / 'review' / 'OPERATIONAL_R2.json'

def validated_rows():
    review = json.loads(REVIEW.read_bytes())
    plan_bytes = PLAN.read_bytes()
    if (review['status'] != 'PASS' or review['plan_sha256'] != digest(plan_bytes)
            or review['installer_sha256'] != digest(Path(__file__).read_bytes())):
        raise ValueError('Operational review is missing or stale')
    rows = json.loads(plan_bytes)['files']
    permitted = {'iald_app_providers.py', 'iald_app_memory.py'}
    if len(rows) != len(permitted) or {Path(r['destination']).name for r in rows} != permitted:
        raise ValueError('Unexpected operational patch set')
    checked = []
    for row in rows:
        dest = Path(row['destination'])
        source = Path(row['source'])
        if dest != ROOT / dest.name or dest.resolve(strict=True) != dest or not source.resolve(strict=True).is_relative_to(STAGE):
            raise ValueError('Operational path mismatch')
        original, replacement = dest.read_bytes(), source.read_bytes()
        if digest(original) != row['baseline_sha256'] or digest(replacement) != row['sha256']:
            raise ValueError('Operational patch baseline changed')
        ast.parse(replacement, filename=dest.name)
        checked.append((dest, original, replacement))
    return digest(plan_bytes), tuple(checked)

def coherent(rows):
    measured = [dest.read_bytes() for dest,_,_ in rows]
    return any(all(actual == row[index] for row,actual in zip(rows,measured)) for index in (1,2))

def install(plan_pin,rows):
    assert_quiesced()
    # Validate the whole operand set again after admission freezes and before
    # creating any backup or changing either runtime module.
    if any(dest.resolve(strict=True) != dest or dest.read_bytes() != original
           for dest,original,_ in rows):
        raise RuntimeError('Operational batch changed before installation')
    saved = {str(dest):backup(dest) for dest,_,_ in rows}
    touched = []
    try:
        for dest,original,replacement in rows:
            if dest.read_bytes() != original:
                raise RuntimeError('Concurrent operational edit')
            touched.append((dest,original,replacement))
            atomic(dest,replacement)
        assert_quiesced()
        if any(dest.read_bytes() != replacement for dest,_,replacement in rows):
            raise RuntimeError('Installed operational files differ from the reviewed bytes')
        write_evidence(STAGE/'DEPLOYMENT.json',{'status':'PASS','plan_sha256':plan_pin,
                       'installed':{str(dest):digest(dest.read_bytes()) for dest,_,_ in rows},'backups':saved})
    except BaseException:
        for dest,original,replacement in reversed(touched):
            if dest.read_bytes() == replacement:
                atomic(dest,original)
        raise
