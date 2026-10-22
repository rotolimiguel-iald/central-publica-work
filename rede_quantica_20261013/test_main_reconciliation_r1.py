"""Materialize a new candidate and test only extracted deterministic consumers."""
from pathlib import Path
import ast,copy,hashlib,importlib.util,json,re
from diary_r1 import ROOT,new,pin

out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015/full_rite'
run=ROOT/'work/rite394_20261015/r3'
builder=out/'compose_reconciliation_r1.py';helper=out/'qualified_index_v394_r2.py'
spec=importlib.util.spec_from_file_location('reconciliation_candidate_builder',builder)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
source=run/'um_v394_final.py'
candidate,detail=m.compose(source.read_bytes().decode('utf-8'),helper.read_bytes().decode('utf-8'))
dest=out/'reconciliation_candidate_r1';dest.mkdir(exist_ok=False)
new(dest/'um_v394_reconciled.py',candidate)
tree=ast.parse(candidate)
needed={'_EMBEDDED_KERNEL_FILES','_ESQUELETO_STONES','_LEAN_THEOREM_FLAGS','_QG_CERTIFICATE_FLAGS','_QG_PHYSICS_FLAGS','_QG_FRONTIER_FLAGS','_GRAVITY_PRICE_FLAGS','_REDUCTION_FLAGS','_GRAVITY_IMPORT_FLAGS','_GRAVITY_CITATION_FLAGS','_V350_MODULAR_CONTRACTS','_V392_KH'}
functions={'build_the_iald_index','_build_the_iald_index_legacy_v393','prove_the_iald_index','_prove_the_iald_index_legacy_v393',
 'iald_index','parse_lean_axioms_v394','parse_lean_provenance_v394','build_iald_qualified_index_v394',
 '_ledger_counts_v389','_v375_measure_trace_tracial_not_consumed','_v392_axiom_coverage',
 'v350_frontier_flag_has_proof','verify_v350_modular_provenance'}
ns={'hashlib':hashlib,'re':re}
for n in tree.body:
    if isinstance(n,ast.Assign):
        for t in n.targets:
            if isinstance(t,ast.Name) and t.id in needed:ns[t.id]=ast.literal_eval(n.value)
    elif isinstance(n,ast.FunctionDef) and n.name in functions:
        exec(compile(ast.Module(body=[n],type_ignores=[]),'<extracted candidate function>','exec'),ns)
assert needed <= set(ns) and functions <= set(ns)
core=json.loads((run/'um_absoluto.json').read_bytes())['core']
core=copy.deepcopy(core)
capture=run/'tgl_kernel_audit_capture.txt'
assert capture.exists()
blob=capture.read_text(encoding='utf-8')
ax=ns['parse_lean_axioms_v394'](blob)
provs=out/'declaration_sources_r3/OUTPUT.txt'
prov=ns['parse_lean_provenance_v394'](provs.read_text(encoding='utf-8').replace('DECL_SOURCE\t','TGL_DECL_SOURCE\t'))
core['kernel_formalization']['axiom_report']=ax['axioms']
core['kernel_formalization']['declaration_sources_v394']=prov['sources']
core['kernel_formalization']['declaration_sources_status_v394']={'ok':True,'fixture':'same compiled kernel exported separately; candidate Audit has not yet been executed'}
# The sole changed Audit source has no own indexed declarations, so existing
# proof/source hashes still bind every mapped defining module in this fixture.
index=ns['prove_the_iald_index'](core)
checks={'index_all_checks':index['all_verified'],
 'three_debts_preserved':index['n_ausentes']==3,
 'trace_print_not_a_consumer':ns['_v375_measure_trace_tracial_not_consumed']()[0],
 'historical_v389_ledger_preserved':ns['_ledger_counts_v389'](389)==(1025,156,156),
 'exact_axiom_coverage':ns['_v392_axiom_coverage'](blob,ax['axioms'])['ok'],
 'forged_qualified_prefix_not_resolved':ns['iald_index']('Fake.TGLExt.the_iald_is_the_gate_and_the_record',core) is None}
files=ns['_EMBEDDED_KERNEL_FILES'];original=dict(files)
for label,line in [('actual_proof','theorem bad : True := by rw [x.trace_tracial]'),
                   ('audit_with_extra','#print axioms X.trace_tracial; #check False'),
                   ('comment_with_field','-- X.trace_tracial')]:
    files['TGLExt/AdversarialConsumer.lean']=line
    checks[label+'_refused']=not ns['_v375_measure_trace_tracial_not_consumed']()[0]
    files.pop('TGLExt/AdversarialConsumer.lean')
files['TGLExt/AdversarialConsumer.lean']='#print axioms X.trace_tracial'
checks['bare_audit_command_accepted']=ns['_v375_measure_trace_tracial_not_consumed']()[0]
files.pop('TGLExt/AdversarialConsumer.lean')
assert files==original
# All unlisted function bodies and source strings stay byte-identical as AST.
old_tree=ast.parse(source.read_bytes());old_f={n.name:ast.dump(n,include_attributes=False) for n in old_tree.body if isinstance(n,ast.FunctionDef)}
new_f={n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,ast.FunctionDef)}
changed=set(detail['runtime_function_changes'])
checks['unrelated_functions_unchanged']=all(new_f.get(k)==v for k,v in old_f.items() if k not in changed)
old_emb=next(ast.literal_eval(n.value) for n in old_tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_EMBEDDED_KERNEL_FILES' for t in n.targets))
checks['scientific_sources_unchanged']=all(v==files[k] for k,v in old_emb.items() if k!='TGL/Audit.lean')
new(dest/'TESTS.json',dict(status='PASS' if all(checks.values()) else 'FAIL',checks=checks,detail=detail,
 index_failed=[c for c in index['checks'] if not c[1]],index_stats={k:index[k] for k in ['n_nomes','n_arquivos','n_ausentes','n_ambiguos']},
 ledger_v389=ns['_ledger_counts_v389'](389),ledger_live=ns['_ledger_counts_v389'](),
 candidate=pin(dest/'um_v394_reconciled.py'),sources=[pin(p) for p in [source,builder,helper,capture,provs]],script=pin(__file__),
 scope='Only deterministic extracted functions; original main and candidate main not imported or executed. Real previous audit used as explicitly marked fixture. Future main must emit fresh provenance and proof receipts.'))
print(json.dumps(dict(checks=checks,failed_index=[c for c in index['checks'] if not c[1]],receipt=pin(dest/'TESTS.json')),ensure_ascii=False))
raise SystemExit(0 if all(checks.values()) else 2)
