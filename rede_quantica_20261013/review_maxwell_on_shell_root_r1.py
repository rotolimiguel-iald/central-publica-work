"""Independent source-semantic review of the actual on-shell Maxwell bivector."""
import datetime as dt
import json
import re
from pathlib import Path
from diary_r1 import ROOT, new, pin

out = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
delivery = out/'maxwell_smearing/FINAL_MAXWELL_ON_SHELL_RECEIPT_R1.json'
r = json.loads(delivery.read_bytes())
checked = {}
def verify(value):
    if isinstance(value, dict):
        if {'path', 'sha256'} <= value.keys():
            actual = pin(value['path'])
            assert actual['sha256'] == value['sha256'], value['path']
            if 'bytes' in value:
                assert actual['bytes'] == value['bytes']
            checked[value['path']] = actual
        for x in value.values(): verify(x)
    elif isinstance(value, list):
        for x in value: verify(x)
verify(r)
axioms = {}
for row in r['modules']:
    receipt = json.loads((Path(row['attempt'])/'RECEIPT.json').read_bytes())
    verify(receipt)
    assert type(receipt['exit_code']) is int and receipt['exit_code'] == 0
    assert receipt['readonly_dependencies_unchanged']
    assert receipt['source']['sha256'] == row['source']['sha256']
    text = Path(row['source']['path']).read_text(encoding='utf-8')
    assert not re.search(r'\b(sorry|admit|axiom)\b', text)
    log = (Path(row['attempt'])/'AXIOMS.txt').read_text(encoding='utf-8')
    parsed = {n: [a.strip() for a in xs.split(',') if a.strip()]
        for n, xs in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", log, re.S)}
    parsed.update({n: [] for n in re.findall(r"'([^']+)' does not depend on any axioms", log)})
    for name in row['printed_declarations']:
        assert name in parsed
        assert set(parsed[name]) <= {'propext', 'Classical.choice', 'Quot.sound'}
        axioms[name] = parsed[name]
assert len(axioms) == 11
target = out/'network_review/MAXWELL_ON_SHELL_SEMANTIC_REVIEW_ROOT_R1.json'
new(target, dict(status='PASS_WITH_STATED_SCOPE', reviewer='codex-root',
    created_utc=dt.datetime.now(dt.timezone.utc).isoformat(), delivery=pin(delivery),
    source_files_read=[x['source'] for x in r['modules']], pins_verified=len(checked),
    printed_axioms=axioms, independent_rebuild=False, material_findings=[],
    findings=[
        'The bivector p wedge epsilon is gauge invariant, satisfies the algebraic Bianchi identity and has divergence p_squared*epsilon - p*(p dot epsilon).',
        'The actual null-shell momentum and transverse circular screen give the source-free identity; the 01 component is the positive transverse radius, proving non-vacuity off the chart axis.',
        'The real screen transport follows from the existing null-frame decomposition; its longitudinal gauge term cancels in the bivector.',
        'The complex lift supplies the same exact bivector transport without importing an unproved global helicity phase.'
    ], limits=['This is the on-shell algebraic construction; it does not supply spacetime test smearing, a stress tensor, charge_link, or a MaxwellCertificate.',
        'This is source and receipt review, not an independent rebuild or a whole-program run.'],
    script=pin(__file__), production_modified=False, gate_modified=False))
print(json.dumps(dict(review=pin(target), pins=len(checked), declarations=len(axioms))))
