"""Integrate verified tower proofs in the isolated, single-file program; never touch originals."""
import ast
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def write_atomic(path, raw):
    assert path.resolve().is_relative_to(ROOT)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == raw:
        return
    if path.exists():
        stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        backup = path.with_name(path.name + '.bak_' + stamp)
        before = path.read_bytes()
        backup.write_bytes(before)
        assert backup.read_bytes() == before
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_bytes(raw)
    assert temporary.stat().st_size == len(raw) and temporary.read_bytes() == raw
    temporary.replace(path)


original = ROOT / 'fontes' / 'um_v350_original.py'
raw = original.read_bytes()
text = raw.decode('utf-8')
tree = ast.parse(text)
assignment = next(n for n in tree.body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES'
                          for t in n.targets))
embedded = ast.literal_eval(assignment.value)
new = {}
module_names = ['CompressionLimit', 'TowerCommutation', 'TowerDuality', 'ModularCertificate', 'WedgeModularData',
                'L2OperatorLift', 'L2Translation', 'L2StrongContinuity',
                'RegularTowerRepresentation', 'RegularGeneratedAlgebra']
for name in module_names:
    source = (ROOT / 'kernel' / 'TGLV350' / (name + '.lean')).read_text(encoding='utf-8')
    for dependency in module_names:
        source = source.replace('import TGLV350.' + dependency,
                                'import TGLExt.V350' + dependency)
    new['TGLExt/V350' + name + '.lean'] = source

new['TGLExt/V350GateContract.lean'] = '''import TGLExt.V350ModularCertificate

set_option autoImplicit false
namespace TGLExt.V350Gate
noncomputable section

/-- Exact type bridges, independent of the names read by the Python parser. -/
def checkedConverse : (P : SiteProfile) → ConverseClauseContract P :=
  qgConverse_JMJ_contains_commutant
def checkedModular : ModularRealizationCertificate :=
  qgFrontier_modularRealization
def checkedActIII : ModularRealizationCertificate :=
  qgPrice_towerActIII_inhabitantConstructed

#print axioms checkedConverse
#print axioms checkedModular
#print axioms checkedActIII
end
end TGLExt.V350Gate
'''
root_import = '\nimport TGLExt.V350GateContract\nimport TGLExt.V350WedgeModularData\nimport TGLExt.V350RegularGeneratedAlgebra\n'
new['TGLExt.lean'] = embedded['TGLExt.lean'].rstrip() + root_import
audit = embedded['TGL/Audit.lean']
new['TGL/Audit.lean'] = root_import + audit.rstrip() + '''

-- 2026-09-11, isolated v350 extension: closed modular certificate, product tower only.
#print axioms TGLExt.qgConverse_JMJ_contains_commutant
#print axioms TGLExt.qgFrontier_modularRealization
#print axioms TGLExt.qgPrice_towerActIII_inhabitantConstructed
#print axioms TGLExt.V350Gate.checkedConverse
#print axioms TGLExt.V350Gate.checkedModular
#print axioms TGLExt.V350Gate.checkedActIII
#print axioms TGLExt.V350Continuous.towerAntiunitary
#print axioms TGLExt.V350Continuous.factorFlow
#print axioms TGLExt.V350Continuous.towerWedgeData
#print axioms TGLExt.V350Continuous.same_conjugation

-- Regular continuous representation; no canonical trace or core flag is asserted.
#print axioms TGLV350.Regular.fibreRepresentation
#print axioms TGLV350.Regular.fibre_injective
#print axioms TGLV350.Regular.shift_mul
#print axioms TGLV350.Regular.shift_star
#print axioms TGLV350.Regular.shift_commutes_fibre
#print axioms TGLV350.Regular.shift_strongly_continuous
#print axioms TGLV350.Regular.fibre_jointly_continuous
#print axioms TGLV350.Regular.regular_mul
#print axioms TGLV350.Regular.regular_unitary
#print axioms TGLV350.Regular.regular_covariance_on_factor
#print axioms TGLV350.Regular.regular_strongly_continuous
#print axioms TGLV350.Regular.regularCoreAlgebra
#print axioms TGLV350.Regular.regularCoreEmbedding_injective
#print axioms TGLV350.Regular.regularCore_minimal
'''

lines = text.splitlines(keepends=True)
starts = [0]
for line in lines:
    starts.append(starts[-1] + len(line))


def position(line, column):
    return starts[line - 1] + len(lines[line - 1].encode('utf-8')[:column].decode('utf-8'))


def span(node):
    return position(node.lineno, node.col_offset), position(node.end_lineno, node.end_col_offset)


patches = []
for key, value in zip(assignment.value.keys, assignment.value.values):
    if key.value in new:
        patches.append((*span(value), repr(new[key.value])))
added = {key: value for key, value in new.items() if key not in embedded}
closing = span(assignment.value)[1] - 1
patches.append((closing, closing, ''.join(
    '\n    ' + repr(key) + ': ' + repr(value) + ',' for key, value in added.items()) + '\n'))

extension = (ROOT / 'gate_extension.py').read_text(encoding='utf-8')
evaluator = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                 and n.name == 'evaluate_quantum_gravity_closure')
start = span(evaluator)[0]
patches.append((start, start, extension + '\n\n'))

verifier = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                and n.name == 'verify_tgl_kernel_formalization')
last_return = verifier.body[-1]
assert isinstance(last_return, ast.Return) and isinstance(last_return.value, ast.Name)
patches.append((*span(last_return), 'return finalize_v350_modular_frontier(res)'))

gate = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'prove_qg_closure_gate')
gate_assignment = next(n for n in gate.body if isinstance(n, ast.Assign)
                       and any(isinstance(t, ast.Name) and t.id == 'gate' for t in n.targets))
end = span(gate_assignment)[1]
patches.append((end, end, '\n    gate["kernel_frontier"] = evaluate_v350_kernel_frontier(kf99)'))
# Verify the existing variable name instead of silently injecting an undefined alias.
assert any(isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'kf99'
           for t in n.targets) for n in gate.body)

# Preserve historical modules, but stop treating the absence of a future proof as an invariant.
changes = []
for function in (n for n in tree.body if isinstance(n, ast.FunctionDef)):
    for node in ast.walk(function):
        if not (isinstance(node, ast.Tuple) and len(node.elts) == 2):
            continue
        label, value = node.elts
        label_text = text[slice(*span(label))]
        expression = text[slice(*span(value))]
        updated = expression
        for flag in ('red_clause_JMJ_contains', 'gpf_tower_act_III_inhabitant_constructed'):
            updated = updated.replace('not kf.get("' + flag + '")',
                                      'v350_frontier_flag_has_proof(kf, "' + flag + '")')
        updated = updated.replace('not [k for k in kf if k.startswith("gpf_") and kf.get(k)]',
                                  'v350_gravity_flags_have_proof(kf)')
        updated = updated.replace('not any(kf.get(k) for k in kf if k.startswith("gpf_"))',
                                  'v350_gravity_flags_have_proof(kf)')
        if updated != expression:
            patches.append((*span(value), updated))
            new_label = '[ERRATA v350+ / proveniência] As flags modular e Ato III exigem prova tipada; este módulo isolado não as quita.'
            patches.append((*span(label), repr(new_label)))
            changes.append({'function': function.name, 'original_line': node.lineno,
                            'historical_label_source': label_text,
                            'old_expression': expression, 'new_expression': updated})

patches.sort(reverse=True)
previous = len(text) + 1
for start, end, replacement in patches:
    assert end <= previous, ('overlapping patches', start, end, previous)
    text = text[:start] + replacement + text[end:]
    previous = start
parsed = ast.parse(text)
integrated = ast.literal_eval(next(n for n in parsed.body if isinstance(n, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets)).value)
assert len(integrated) == len(embedded) + len(added)
for key, content in embedded.items():
    if key not in new:
        assert integrated[key] == content
for key, content in new.items():
    assert integrated[key] == content
    write_atomic(ROOT / 'kernel' / key, content.encode('utf-8'))
write_atomic(ROOT / 'um.py', text.encode('utf-8'))
record = {'base_sha256': hashlib.sha256(raw).hexdigest(),
          'working_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(),
          'added_kernel_files': list(added), 'updated_kernel_files': [k for k in new if k in embedded],
          'embedded_files': len(integrated), 'historical_checks_updated': changes,
          'status': 'INTEGRATED_SOURCE__FULL_RUNTIME_NOT_YET_EXECUTED'}
write_atomic(ROOT / 'integration.json', json.dumps(record, indent=2, ensure_ascii=False).encode('utf-8'))
print(json.dumps({k: v for k, v in record.items() if k != 'historical_checks_updated'}, ensure_ascii=False))
print('historical_checks_updated=' + str(len(changes)))
