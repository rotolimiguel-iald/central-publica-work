"""Record an independent source review; this does not claim a second build."""
import datetime as dt
import json
import re
from pathlib import Path
from diary_r1 import ROOT, new, pin

out = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
base = out / 'takesaki_fock'
delivery = base / 'FOCK_GNS_MODULAR_FLOW_RECEIPT_R1.json'
r = json.loads(delivery.read_bytes())
checked = {}

def verify(value):
    if isinstance(value, dict):
        if {'path', 'sha256'} <= value.keys():
            actual = pin(value['path'])
            assert actual['sha256'] == value['sha256'], value['path']
            if 'bytes' in value:
                assert actual['bytes'] == value['bytes'], value['path']
            checked[value['path']] = actual
        for child in value.values():
            verify(child)
    elif isinstance(value, list):
        for child in value:
            verify(child)

verify(r)
count = 0
for row in r['records']:
    receipt = json.loads(Path(row['receipt']['path']).read_bytes())
    verify(receipt)
    assert type(row['exit_code']) is int and row['exit_code'] == 0
    assert receipt['exit_code'] == 0
    text = Path(row['source']['path']).read_text(encoding='utf-8')
    assert not re.search(r'\b(sorry|admit|axiom)\b', text)
    log = Path(row['axioms']['path']).read_text(encoding='utf-8')
    for declaration, axioms in row['printed_axioms'].items():
        assert declaration in log
        assert set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}
        count += 1
assert count == r['printed_declarations'] == 63

findings = [
    {'module': 'ClosedTomitaOperatorR1', 'lines': [19, 25, 35, 101, 158, 184, 242, 246],
     'conclusion': 'The generic input names the exact closed dense antilinear involution. The adjoint is maximal, the square uses the actual composition domain, and graph projection gives surjectivity of I+S* S and positive self-adjointness. No self-adjoint extension is inserted as an extra input.'},
    {'module': 'ClosedTomitaFlowR1', 'lines': [20, 40, 47, 75],
     'conclusion': 'The involution proves a zero kernel for its square; therefore both bounded-resolvent endpoints are injective. Existing resolvent CFC gives imaginary powers with a dense-range damping characterization, group law, inverse and strong continuity.'},
    {'module': 'CanonicalFockWeightModularOperatorR3', 'lines': [16, 25, 27, 75],
     'conclusion': 'All five generic proof fields are supplied by the previously constructed concrete GNS closed Tomita operator. The resulting square and resolvent act on that GNS Hilbert space and retain their exact domains.'},
    {'module': 'CanonicalFockWeightModularFlowR3', 'lines': [13, 42],
     'conclusion': 'The instantiated imaginary powers use the same concrete square and inherit its proven damping identity, uniqueness and continuous group laws.'},
]
target = out / 'network_review/GNS_MODULAR_FLOW_SEMANTIC_REVIEW_ROOT_R1.json'
new(target, {
    'status': 'PASS_WITH_STATED_SCOPE', 'reviewer': 'codex-root',
    'time_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
    'delivery': pin(delivery), 'sources_read': [row['source'] for row in r['records']],
    'pins_verified': len(checked), 'printed_axioms_checked': count,
    'findings': findings, 'material_findings': [], 'independent_rebuild': False,
    'limits': [
        'The underlying S is the closure of the original uniform finite-weight star core; equality with the full finite-weight star-core closure is not proved by these four modules.',
        'These proofs do not identify the constructed imaginary powers with conjugation by the regular translation unitaries.',
        'The exp(-s)-scaled trace and remaining PF/core interface fields are not supplied by this delivery.',
        'No production installation, full-program execution or gate change follows from this source review.'
    ], 'script': pin(__file__)
})
print(json.dumps({'review': pin(target), 'pins_verified': len(checked), 'printed_axioms': count}))
