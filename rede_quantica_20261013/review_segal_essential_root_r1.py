"""Independent source-semantic review of the concrete Segal closure."""
import datetime as dt
import json
import re
from pathlib import Path
from diary_r1 import ROOT, new, pin

out = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
delivery = out/'segal_selfadjoint/FINAL_SEGAL_ESSENTIAL_RECEIPT_R1.json'
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
assert len(axioms) == 13
target = out/'network_review/SEGAL_ESSENTIAL_SEMANTIC_REVIEW_ROOT_R1.json'
new(target, dict(status='PASS_WITH_STATED_SCOPE', reviewer='codex-root',
    created_utc=dt.datetime.now(dt.timezone.utc).isoformat(), delivery=pin(delivery),
    source_files_read=[x['source'] for x in r['modules']], pins_verified=len(checked),
    printed_axioms=axioms, independent_rebuild=False, material_findings=[],
    findings=[
        'Closed-graph projection yields self-adjointness from both actual deficiency spaces; no extension or resolvent surjectivity is assumed.',
        'The adjoint is unchanged by closure of a densely defined symmetric operator; the closed criterion therefore establishes essential self-adjointness.',
        'A deficiency vector would produce a bounded scalar orbit with nonzero real exponential growth, which the explicitly proved scalar lemma excludes.',
        'The concrete consumer supplies group law, norm preservation, invariant exponential domain, actual derivative i*sqrt(2)*Phi, density and symmetry from the same existing Fock/Weyl objects.',
        'The closure is self-adjoint and its original exponential span is a graph core.'
    ], limits=['No spacetime smearing, Maxwell stress, charge_link or all-direction curved H3 is supplied.',
        'This is source and receipt review, not a second compilation or a whole-program run.'],
    script=pin(__file__), production_modified=False, gate_modified=False))
print(json.dumps(dict(review=pin(target), pins=len(checked), declarations=len(axioms))))
