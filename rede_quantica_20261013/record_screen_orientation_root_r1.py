"""Custody for the actual proper-Lorentz screen orientation construction."""
import datetime as dt
import json
import re
from pathlib import Path
from diary_r1 import ROOT, new, pin

out = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
base = out/'orbital_rotation'
trio = {'propext', 'Classical.choice', 'Quot.sound'}
rows = []
for name, count in [('NullFrameDetRootR4', 1), ('ScreenOrientationDetRootR3', 5)]:
    source = base/(name+'.lean')
    matches = []
    for receipt_path in (base/'attempts').glob('*/RECEIPT.json'):
        r = json.loads(receipt_path.read_bytes())
        if r['source']['sha256'] == pin(source)['sha256'] and type(r['exit_code']) is int and r['exit_code'] == 0:
            matches.append((receipt_path, r))
    assert matches, ('No actual successful attempt', name)
    receipt_path, r = sorted(matches)[-1]
    attempt = receipt_path.parent
    assert r['readonly_dependencies_unchanged']
    for meta in r['dependencies'] + r['artifacts']:
        assert pin(meta['path']) == meta
    text = (attempt/'AXIOMS.txt').read_text(encoding='utf-8')
    parsed = {n:[v.strip() for v in values.split(',') if v.strip()]
        for n,values in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", text, re.S)}
    assert len(parsed) == count and 'sorryAx' not in text
    assert all(set(v) <= trio for v in parsed.values())
    rows.append(dict(name=name, source=pin(source), attempt=str(attempt),
        receipt=pin(receipt_path), object=pin(attempt/(name+'.olean')),
        printed_declarations=list(parsed), axioms=parsed, seconds=r['seconds'], exit_code=0))

failed = []
for receipt_path in (base/'attempts').glob('*/RECEIPT.json'):
    r = json.loads(receipt_path.read_bytes())
    stem = Path(r['source']['path']).stem
    if (stem.startswith('NullFrameDetRoot') or stem.startswith('ScreenOrientationDetRoot')) and r['exit_code'] != 0:
        failed.append(dict(receipt=pin(receipt_path), source=r['source'],
            log=pin(receipt_path.parent/'BUILD.log'), exit_code=r['exit_code']))

dest = base/'FINAL_SCREEN_ORIENTATION_ROOT_RECEIPT_R1.json'
new(dest, dict(unit='F1.FECHO_20261015', claim=845,
    created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
    status='REAL_KERNEL_TERMS_PENDING_INDEPENDENT_REVIEW', modules=rows,
    failed_attempts_preserved=failed, script=pin(__file__),
    construction='The actual O16 null frame has determinant one. Coordinate decomposition factors the actual four-dimensional transport through the null frames; its fixed first column and second row reduce the determinant to that of the transverse screen.',
    hypotheses=['Off-axis input and output chart points', 'Actual momentum transport',
        'Minkowski metric preservation', 'Determinant of the actual linear map equals one'],
    conclusion='ScreenOrientationMeasured follows from those hypotheses; it is not assumed.',
    limits=['This is the proper-transport orientation lemma; the global unitary representation and localized net are separate consumers.',
        'Compilation is in sandbox; no production kernel or gate changes.'],
    production_modified=False, gate_modified=False))
print(json.dumps(dict(delivery=pin(dest), declarations=sum(len(r['axioms']) for r in rows))))
