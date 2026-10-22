from pathlib import Path
import datetime, hashlib, json, os, re

root = Path(__file__).resolve().parent
def pin(path):
    b = path.read_bytes()
    return {'path': str(path), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def latest(module, success=True):
    source = root/'src/TGLExt'/f'{module}.lean'
    sha = pin(source)['sha256']
    matches = []
    for record in (root/'attempts').glob('*/RESULT.json'):
        d = json.loads(record.read_bytes())
        if d['source']['sha256'] == sha and d['source_unchanged'] and ((d['returncode'] == 0) == success):
            matches.append((record, d))
    assert matches, (module, success)
    record, d = sorted(matches, key=lambda x: str(x[0]))[-1]
    for key in ('stdout', 'stderr'):
        assert pin(Path(d[key]['path'])) == d[key], (module, key)
    if success:
        assert pin(Path(d['object']['path'])) == d['object'], module
    return record, d

inventory = json.loads((root/'AUDIT_NAMES_FULL.json').read_bytes())
builds = {n: latest(n) for n in inventory['modules'] + ['AuditFullLegacy012', 'GoodTraceCompletion012', 'GoodFullLegacy012']}
output = Path(builds['AuditFullLegacy012'][1]['stdout']['path']).read_text(encoding='utf8')
expected = re.findall(r'^#print axioms (\S+)$', (root/'src/TGLExt/AuditFullLegacy012.lean').read_text(encoding='utf8'), re.M)
assert expected == inventory['names'] and len(set(expected)) == len(expected)
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
rows = []
for name in expected:
    pattern = r"'" + re.escape(name) + r"' (?:depends on axioms: \[([^]]*)\]|(does not depend on any axioms))"
    found = re.findall(pattern, output, re.S)
    assert len(found) == 1, (name, found)
    deps = {re.sub(r'\.\{[^}]*\}', '', x.strip()) for x in found[0][0].split(',') if x.strip()}
    rows.append({'name': name, 'axioms': sorted(deps), 'allowed': deps <= allowed})

controls = []
for name in ['BadTraceCommute012', 'BadTraceZero012', 'BadFullLegacyZero012', 'BadFullLegacyOperator012']:
    record, d = latest(name, False)
    content = Path(d['stdout']['path']).read_text(encoding='utf8')
    rejection = bool(re.search(r'(Type mismatch|type mismatch|Application type mismatch|Tactic `rfl` failed)', content))
    infrastructure = bool(re.search(r'(does not exist|unknownIdentifier|unexpected token|timeout)', content))
    controls.append({'name': name, 'result': pin(record), 'returncode': d['returncode'],
                     'semantic_rejection': rejection and not infrastructure,
                     'scope': ('Wrong definitional identification H3Lt=1 rejected by rfl; not by itself a universal inequality theorem.'
                               if name == 'BadFullLegacyOperator012' else
                               'Misuse of the actual interface is refused by type checking; no physical assertion.')})
sources = [root/'src/TGLExt'/f'{n}.lean' for n in inventory['modules']]
lexical = []
for p in sources:
    hits = re.findall(r'\b(axiom|sorry|native_decide|trustCompiler)\b', p.read_text(encoding='utf8'))
    lexical.append({'source': pin(p), 'forbidden_hits': hits})
    assert not hits, (p, hits)
data = {
    'timestamp': datetime.datetime.now().astimezone().isoformat(),
    'status': 'AUTHOR_EXACT_LEGACY_FULL_WITNESS_AND_POSITIVE_TRACE_COMPATIBILITY_VERIFIED',
    'sources': [pin(p) for p in sources],
    'builds': {n: {'record': pin(p), 'returncode': d['returncode']} for n, (p, d) in builds.items()},
    'axiom_checks': rows, 'all_axioms_allowed': all(r['allowed'] for r in rows),
    'controls': controls, 'all_controls_semantic': all(c['semantic_rejection'] for c in controls),
    'lexical_checks': lexical,
    'full_trace_A1_previously_constructed': True,
    'positive_trace_compatibility_proved': True,
    'exact_legacy_full_witness_constructed': True,
    'gate_changed': False,
    'shared_supplier': 'V354BoundedPolar: 11 names authored by Poincare, compiled here from identical source; do not double count in the SUSY union.',
    'review': 'Independent review by Carver is a separate artifact; this file is author verification only.',
    'proven_scope': [
        'Total cyclic ENNReal reader agrees with actual A1 trace on every positive operator, including infinite trace.',
        'Positive shift compatibility is a theorem, with no extra compatibility premise at the final use.',
        'Exact legacy ContinuousCoreData, ThreeLocksCoreData, TGLModularRealization and FullTGLWitness have actual terms.',
        'PF and H3Lt in the packaged term are definitionally the prior finite support and minimal operator 1-PF.',
        'Existing CoreSupport, WitnessV3 and wedge suppliers are reused, not reconstructed.'
    ],
    'limits': [
        'The total ENNReal reader is not claimed complex-linear or additive on the entire ring; it agrees with the trace on the positive cone.',
        'H3Lt is the constructed bounded minimal operator 1-PF, not identified with an independently derived microscopic Hamiltonian or standard bounded transform.',
        'Legacy wedge data retain their existing formal scope, including U=1; no new physical Bisognano-Wichmann theorem.',
        'No physical confirmation, sigma calculation, canonical source modification or runtime flag integration in this audit.',
        'Separate SUSY author audit and joint independent review must accompany the final handoff.'
    ],
    'supersedes_current_status_only': str(root/'AUDITORIA_AUTORAL_COMPLETION_012.json')
}
assert data['all_axioms_allowed'] and data['all_controls_semantic']
p = root/'AUDITORIA_AUTORAL_FULL_LEGACY_012.json'
assert not p.exists()
b = json.dumps(data, ensure_ascii=False, indent=2).encode('utf8')
t = p.with_name(p.name+'.tmp'); t.write_bytes(b); assert t.read_bytes() == b; os.replace(t, p)
print(json.dumps({'path': str(p), 'names': len(rows), 'controls': len(controls), 'status': data['status']}))
