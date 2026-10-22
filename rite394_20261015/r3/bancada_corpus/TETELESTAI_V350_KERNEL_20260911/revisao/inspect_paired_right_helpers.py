"""Reviewer-only static inspection: never imports or executes author helpers."""
from pathlib import Path
from datetime import datetime
import ast
import hashlib
import json
import os

REV = Path(__file__).resolve().parent
ROOT = REV.parent
RUN = Path((REV / 'paired_right_final_latest_run.txt').read_text().strip())
assert RUN.resolve().is_relative_to(REV)
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
    return json.loads(p.read_bytes())
def atomic(p, data):
    assert p.resolve().is_relative_to(REV)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old = p.read_bytes()
        bk = p.with_name(p.name + '.bak_' + stamp)
        with bk.open('xb') as f:
            f.write(old)
        assert bk.read_bytes() == old
    tmp = p.with_name(p.name + '.tmp_' + stamp)
    with tmp.open('xb') as f:
        f.write(data)
    assert tmp.read_bytes() == data
    os.replace(tmp, p)
    assert p.read_bytes() == data
def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)
def assignment(tree, name):
    return next(n for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))

names = ['make_paired_right_helpers.py', 'record_paired_right_draft.py',
         'prepare_paired_right_stage.py', 'record_paired_right_progress.py',
         'verify_paired_right_custody.py']
parent = load(RUN / 'right_regularization_custody.json')
draft = load(RUN / 'paired_right_draft_status.json')
manifest = load(RUN / 'manifest.json')
helpers = {}
for name in names:
    assert sha(RUN / name) == sha(ROOT / name) == manifest['artifact_pins'][name]
    text = (RUN / name).read_text(encoding='utf-8')
    tree = ast.parse(text)
    imports = [n.module if isinstance(n, ast.ImportFrom) else a.name
               for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))
               for a in (n.names if isinstance(n, ast.Import) else [None])]
    assert set(imports) <= {'ast', 'datetime', 'hashlib', 'json', 'pathlib', 're', 'sys'}
    assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                   and n.func.id in {'exec', 'eval', '__import__', 'compile'} for n in ast.walk(tree))
    helpers[name] = {'sha256': sha(RUN / name), 'bytes': (RUN / name).stat().st_size,
                     'ast_parsed': True, 'imports': imports, 'executed_by_reviewer': False}

modules = list(draft['modules'])
assert modules == ['ScalarRightAdjointPair', 'ScalarCommutantSandwich', 'ScalarPairedRightAlgebra']
assert sum(r['targets'] for r in draft['modules'].values()) == len(draft['targets']) == 29
assert draft['report_sha256'] == sha(ROOT / 'RELATORIO_ALGEBRA_DIREITA_ADJUNTO_DEV.md')
assert draft['parent_custody_sha256'] == sha(ROOT / 'right_regularization_custody.json')
assert len(parent['surface_sha256']) == len(manifest['memory_surfaces']) == 34
assert set(parent['surface_sha256']) == set(manifest['memory_surfaces'])
assert sha(ROOT / 'um.py') == parent['working_sha256'] == draft['integrated_working_sha256']
assert sha(ROOT / 'gate_extension.py') == parent['artifacts']['gate_extension.py']
assert len(parent['remaining_flags']) == 6 and not any(parent['remaining_flags'].values())

# Independently calculate the three proposed textual deltas in memory, without running prepare.
proposed = {}
for name in ['integrate_v350.py', 'compile_integrated.py', 'test_gate_extension.py']:
    p = ROOT / name
    assert sha(p) == parent['artifacts'][name]
    before = p.read_text(encoding='utf-8')
    ast.parse(before)
    if name == 'integrate_v350.py':
        old_batch = ast.literal_eval(assignment(ast.parse(before), 'tomita_batch').value)
        assert not set(modules).intersection(old_batch)
        after = once(before, "'ScalarRightRegularization', 'ScalarCommutantRegularization']",
            "'ScalarRightRegularization', 'ScalarCommutantRegularization',\n                " +
            ', '.join(map(repr, modules)) + ']')
        after = once(after, '== 544', '== 573')
        new_batch = ast.literal_eval(assignment(ast.parse(after), 'tomita_batch').value)
        assert new_batch == old_batch + modules
        scope = 'Only three-module append and asserted target batch 544 -> 573.'
    elif name == 'compile_integrated.py':
        anchor = "'TGLExt/V350ScalarCommutantRegularization.lean',\n"
        after = once(before, anchor, anchor + ''.join("                 'TGLExt/V350"+n+".lean',\n" for n in modules))
        assert after.index('TGLExt/V350ScalarPairedRightAlgebra.lean') < after.index("'TGLExt.lean'")
        scope = 'Three new integrated modules follow their parent and precede aggregate roots.'
    else:
        anchor = "        'scalarCommutant_mem_generated_rightBounded'),\n"
        after = once(before, anchor, anchor + "    'original_adjoint_pairs_and_generated_right_star_algebra': (\n"
            "        'scalarRightAdjointPair_maximal', 'scalarCommutantSandwich_in_original_adjoint',\n"
            "        'scalarCommutant_paired_right_approximation',\n"
            "        'scalarPairedRightAlgebra_generated_eq_commutant'),\n")
        scope = 'One new frontier group; current/historical Audit handling unchanged.'
    ast.parse(after)
    proposed[name] = {'current_sha256': sha(p),
        'candidate_text_sha256': hashlib.sha256(after.encode('utf-8')).hexdigest(),
        'syntax_valid': True, 'scope': scope, 'written_or_executed': False}

recorder = (RUN / 'record_paired_right_progress.py').read_text(encoding='utf-8')
verifier = (RUN / 'verify_paired_right_custody.py').read_text(encoding='utf-8')
for token in ["assert '--review-read' in sys.argv", "assert len(surfaces) == 34",
              "raw.startswith(before)", "with backup.open('xb')", "backup.read_bytes() == before",
              "temp.replace(path)", "path.read_bytes() == before", "'PAIRED_RIGHT_INTEGRATED_REVIEW'",
              "assert body(prior) == body(ROOT / 'um.py')", "evidence['historical_v350_audit_metadata']",
              "row['returncode'] == 0 and row['output_exists']", "sha(binary) == row['output_sha256']"]:
    assert token in recorder, token
for token in ["c['surface_before_sha256'] == parent['surface_sha256']",
              "len(compiled['records']) == c['integrated_records']",
              "sha(source) == row['sha256'] and sha(binary) == row['output_sha256']",
              "surface.read_bytes().startswith(backup.read_bytes())",
              "evidence['audit_stdout_sha256'] == evidence['audit_capture_sha256_full']",
              "assert not out.exists()"]:
    assert token in verifier, token
allowed_external = {ROOT.parent.parent / 'memory/TGL_ATLAS.md',
                    ROOT.parent.parent / 'memory/TGL_INDICE_VIVO.md'}
assert all(Path(p).is_relative_to(ROOT) or Path(p) in allowed_external for p in parent['surface_sha256'])
assert not (ROOT / 'paired_right_custody.json').exists()
assert not (ROOT / 'paired_right_custody_verification.json').exists()

data = {'timestamp': datetime.now().astimezone().isoformat(timespec='seconds'),
    'inspection': 'STATIC_ONLY__AUTHOR_HELPERS_NOT_EXECUTED',
    'helpers': helpers, 'draft_sha256': sha(RUN / 'paired_right_draft_status.json'),
    'report_sha256': sha(RUN / 'RELATORIO_ALGEBRA_DIREITA_ADJUNTO_DEV.md'),
    'parent_custody_sha256': sha(RUN / 'right_regularization_custody.json'),
    'modules': 3, 'targets': 29, 'proposed_changes': proposed,
    'mathematical_documentation_matches_read_theorems': True,
    'memory_surfaces': 34, 'writer_byte_backup_atomic_prefix_checks_present': True,
    'verifier_rereads_all_compiled_source_binary_pairs': True,
    'same_integrated_and_memory_parent': True, 'six_major_flags_false': True,
    'working_and_gate_hashes_equal_parent': True,
    'integrated_review_required_before_memory_recording': True,
    'new_custody_and_verification_not_present': True,
    'future_execution_and_integration_not_certified': True, 'findings': []}
atomic(RUN / 'helper_static_inspection.json', (json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
print(json.dumps({'helper_static_inspection_sha256': sha(RUN / 'helper_static_inspection.json'),
                  'draft_sha256': data['draft_sha256'], 'helpers': len(helpers),
                  'modules': 3, 'targets': 29, 'findings': []}, ensure_ascii=False))
