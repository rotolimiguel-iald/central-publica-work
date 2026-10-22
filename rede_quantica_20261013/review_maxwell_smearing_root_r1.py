"""Independent source-semantic review of the compact on-shell smearing into the same Fock."""
import datetime as dt
import json
import re
from pathlib import Path
from diary_r1 import ROOT, new, pin

out = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
delivery = out/'maxwell_smearing/FINAL_MAXWELL_SMEARING_RECEIPT_R1.json'
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
assert len(axioms) == 18
target = out/'network_review/MAXWELL_SMEARING_SEMANTIC_REVIEW_ROOT_R1.json'
new(target, dict(status='PASS_WITH_STATED_SCOPE', reviewer='codex-root',
    created_utc=dt.datetime.now(dt.timezone.utc).isoformat(), delivery=pin(delivery),
    source_files_read=[x['source'] for x in r['modules']], pins_verified=len(checked),
    printed_axioms=axioms, independent_rebuild=False, material_findings=[],
    findings=[
        'The explicit p-wedge-epsilon contraction is continuous on the support away from the chart axis and has compact support; its L2 membership is proved rather than assumed.',
        'The existing orbital L2 inverse transports this concrete coefficient into the original H1; addition and complex scalar multiplication of the smearing are proved.',
        'A compact Urysohn bump in the antisymmetric 01 component has coefficient b(y)*transverseMass. Positivity of the open-set measure upgrades its nonzero value to a nonzero H1 class.',
        'The lower-momentum divergence contracts the actual upper bivector to zero, and this descends through the concrete L2 map.',
        'The same existing Segal operator consumes the smeared H1 vector, inherits essential self-adjointness and the exponential core, and has a nonzero one-particle vacuum excitation.'
    ], limits=['The compact momentum-chart domain is not yet a Fourier restriction of spacetime Schwartz tests, and no spacetime locality, Wick stress, charge_link or MaxwellCertificate follows.',
        'Complex linearity is proved for the one-particle smearing; the self-adjoint Segal assignment is not thereby a complex-linear operator-valued distribution.',
        'This is source and receipt review, not an independent rebuild or a whole-program run.'],
    script=pin(__file__), production_modified=False, gate_modified=False))
print(json.dumps(dict(review=pin(target), pins=len(checked), declarations=len(axioms))))
