"""Read-only AST/pin inspection of author helpers. Never execute their code."""
from pathlib import Path
import ast, datetime, hashlib, json, re

REV = Path(__file__).resolve().parent
ROOT = REV.parent
RUN = Path((REV/'right_regularization_latest_run.txt').read_text().strip())
hf = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
load = lambda p: json.loads(Path(p).read_bytes())

def save(name, data):
    p = RUN/name
    assert p.resolve().is_relative_to(REV) and not p.exists()
    raw = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
    temp = p.with_name(p.name+'.tmp')
    with temp.open('xb') as f: f.write(raw)
    assert temp.read_bytes()==raw
    temp.replace(p)

M = load(RUN/'manifest.json')
D = load(RUN/'right_regularization_draft_status.json')
P = load(RUN/'gaussian_polar_custody.json')
names = list(D['modules'])
assert names == ['ScalarRightRegularization', 'ScalarCommutantRegularization']
helpers = ['make_right_regularization_helpers.py','record_right_regularization_draft.py',
    'prepare_right_regularization_stage.py','record_right_regularization_progress.py',
    'verify_right_regularization_custody.py']
pins = {}
texts = {}
for name in helpers:
    raw = (ROOT/name).read_bytes()
    assert hf(ROOT/name)==M['artifact_pins'][name] and raw==(RUN/name).read_bytes()
    tree = ast.parse(raw)
    texts[name] = raw.decode('utf-8')
    pins[name] = {'sha256':hf(ROOT/name),'lines':len(raw.splitlines()),'ast_parsed':True,
        'fully_read':True,'author_execution_by_reviewer':False,
        'functions':{n.name:n.lineno for n in tree.body if isinstance(n,ast.FunctionDef)}}

prep = texts[helpers[2]]
rec = texts[helpers[3]]
ver = texts[helpers[4]]
assert "assert count == 525" in prep and "'== 525', '== 544'" in prep
assert "len(draft['targets']) == 19" in prep
assert "assert '--review-read' in sys.argv" in prep and "assert '--review-read' in sys.argv" in rec
assert "assert len(surfaces) == 34" in rec
assert "backup.read_bytes() == before" in rec and "raw.startswith(before)" in rec
assert "temp.replace(path)" in rec and "path.read_bytes() == before" in rec
assert "sha(source) == row['sha256'] and sha(binary) == row['output_sha256']" in rec
assert "sha(source) == row['sha256'] and sha(binary) == row['output_sha256']" in ver
assert "len(modules) == 2 and len(targets) == 19" in rec
assert "c['surface_before_sha256'] == parent['surface_sha256']" in ver
assert "right_bounded_reconstruction_still_open" in rec and "'KMS_proved': False" in rec

# Interpret only the three already-read literal insertions, in memory.
old_integrator = (ROOT/'integrate_v350.py').read_text(encoding='utf-8')
itree = ast.parse(old_integrator)
batch = ast.literal_eval(next(n.value for n in itree.body if isinstance(n,ast.Assign)
    and any(isinstance(t,ast.Name) and t.id=='tomita_batch' for t in n.targets)))
old_targets = sum(len(re.findall(r'^#print axioms ',(ROOT/'kernel/TGLV350'/(n+'.lean')).read_text(encoding='utf-8'),re.M)) for n in batch)
assert old_targets==525 and not set(names).intersection(batch)

def once(text, old, new):
    assert text.count(old)==1, old
    return text.replace(old,new,1)

new_integrator = once(old_integrator,"'ScalarGaussianImage', 'ScalarGaussianUnitary']",
    "'ScalarGaussianImage', 'ScalarGaussianUnitary',\n                "+', '.join(map(repr,names))+']')
new_integrator = once(new_integrator,'== 525','== 544')
ast.parse(new_integrator)
compiler = (ROOT/'compile_integrated.py').read_text(encoding='utf-8')
anchor = "'TGLExt/V350ScalarGaussianUnitary.lean',\n"
projected_compile = once(compiler,anchor,anchor+''.join("                 'TGLExt/V350"+n+".lean',\n" for n in names))
ast.parse(projected_compile)
assert projected_compile.index('TGLExt/V350ScalarCommutantRegularization.lean') < projected_compile.index("'TGLExt.lean'",projected_compile.index('TGLExt/V350ScalarCommutantRegularization.lean'))
tests = (ROOT/'test_gate_extension.py').read_text(encoding='utf-8')
anchor = "        'scalarGNSCyclicVector_cyclic'),\n"
addition = "    'full_weight_right_regularization_and_commutant_approximation': (\n"+\
    "        'scalarRightRegularization_embedding', 'scalarRightRegularization_tendsto',\n"+\
    "        'scalarCommutant_rightBounded_approximation',\n"+\
    "        'scalarCommutant_mem_generated_rightBounded'),\n"
assert addition in prep.replace('"\n    "','').replace('"\n    "','') or all(s in prep for s in ['full_weight_right_regularization_and_commutant_approximation','scalarCommutant_mem_generated_rightBounded'])
projected_tests = once(tests,anchor,anchor+addition)
ast.parse(projected_tests)
assert 'CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES' in projected_tests
assert 'historical_v350_audit_metadata' in projected_tests
assert projected_tests.replace(addition,'',1)==tests
for f in ['integrate_v350.py','compile_integrated.py','test_gate_extension.py','gate_extension.py']:
    assert hf(ROOT/f)==P['artifacts'][f], f
assert hf(ROOT/'um.py')==P['working_sha256']
assert all(hf(p)==pin for p,pin in P['surface_sha256'].items())
assert not (ROOT/'right_regularization_custody.json').exists()
assert not (ROOT/'RELATORIO_REGULARIZACAO_COMUTANTE_INTEGRADA.md').exists()

save('helper_static_inspection.json',{
    'timestamp':datetime.datetime.now().astimezone().isoformat(),
    'mode':'STATIC_READ_AND_AST_ONLY__NO_AUTHOR_HELPER_EXECUTION',
    'helper_pins':pins, 'parent_custody_sha256':hf(ROOT/'gaussian_polar_custody.json'),
    'draft_sha256':hf(ROOT/'right_regularization_draft_status.json'),
    'report_sha256':hf(ROOT/'RELATORIO_REGULARIZACAO_COMUTANTE_DEV.md'),
    'current_parent_helpers_and_gate_unchanged':True,'working_unchanged':True,
    '34_parent_memory_surfaces_unchanged':True,
    'planned_append_byte_backups_atomic_per_file':True,
    'planned_source_binary_reread_in_recorder_and_verifier':True,
    'planned_import_batch':{'old':old_targets,'new':old_targets+len(D['targets']),'modules':names},
    'planned_new_test_groups':1,'audit_metadata_logic_unchanged':True,
    'planned_changes_parse_and_anchors_unique':True,
    'integration_and_memory_recording_not_executed_or_certified':True,
    'mathematical_text_explicit_one_sided_right_bounded_only':True,
    'conditional_Q_reconstruction_premise_explicit':True,
    'new_findings':[],
    'limits':['Static inspection is not execution or custody certification.',
      'No adjoint vector/full Hilbert algebra/reconstruction as original J*pi(b)*J is asserted.',
      'No KMS, modular-flow identification or gate/runtime promotion.']})
print(json.dumps({'helpers':len(pins),'targets':len(D['targets']),
    'helper_static_inspection_sha256':hf(RUN/'helper_static_inspection.json')}))
