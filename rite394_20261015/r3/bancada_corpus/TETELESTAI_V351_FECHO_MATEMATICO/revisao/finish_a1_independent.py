from pathlib import Path
import ast, datetime, difflib, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'revisao/a1_independent_20260914_081736_089694'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,data):
    if not isinstance(data,bytes): data=json.dumps(data,ensure_ascii=False,indent=2).encode('utf-8')
    assert not p.exists(),str(p)
    tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(data);assert tmp.stat().st_size==len(data);tmp.replace(p)
pre=json.loads((OUT/'preflight.json').read_text(encoding='utf-8'))
module=json.loads((OUT/'module.json').read_text(encoding='utf-8'))
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join(pre['lean_path'])
command=[pre['compiler'],'-o',str(OUT/'build/ReviewA1Audit.olean'),str(OUT/'kernel/ReviewA1Audit.lean')]
start=time.monotonic()
with (OUT/'auditor_recheck.stdout.txt').open('wb') as out,(OUT/'auditor_recheck.stderr.txt').open('wb') as err:
    run=subprocess.run(command,cwd=OUT/'kernel',env=env,stdout=out,stderr=err)
audit=dict(command=command,returncode=run.returncode,seconds=time.monotonic()-start,
    source_sha256=sha(OUT/'kernel/ReviewA1Audit.lean'),stdout_sha256=sha(OUT/'auditor_recheck.stdout.txt'),
    stderr_sha256=sha(OUT/'auditor_recheck.stderr.txt'),object_sha256=sha(OUT/'build/ReviewA1Audit.olean'))
save(OUT/'auditor_run.json',audit)
stdout=(OUT/'auditor_recheck.stdout.txt').read_text(encoding='utf-8')
assert run.returncode==0 and not (OUT/'auditor_recheck.stderr.txt').stat().st_size
assert 'error:' not in stdout and 'warning:' not in stdout
hits=re.findall(r"^'(.+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)\s*$",stdout,re.M)
raw={n:[a.strip() for a in ax.split(',') if a.strip()] for n,ax in hits}
normalized={n:[re.sub(r'\.\{[^{}]*\}$','',a) for a in vals] for n,vals in raw.items()}
allowed={'propext','Classical.choice','Quot.sound'}
assert len(hits)==len(raw)==len(pre['names'])==11
assert set(raw)==set(pre['names']) and all(set(x)<=allowed for x in normalized.values())
assert normalized==module['axioms']
audit['axioms_raw']=raw;audit['axioms_normalized']=normalized
save(OUT/'auditor.json',audit)
deps=json.loads((OUT/'dependencies.json').read_text(encoding='utf-8'))
deps_ok=all(sha(d['source'])==d['source_sha256'] and sha(d['object_origin'])==d['object_sha256'] and sha(d['copied_object'])==d['object_sha256'] and sha(ROOT/'build'/Path(*d['module'].split('.')).with_suffix('.olean'))==d['object_sha256'] for d in deps)
inputs_ok=all(sha(ROOT/k)==v for k,v in pre['pins'].items())
source=ROOT/'kernel/TGLExt/V351RegularCoreTraceContract.lean'
assert deps_ok and inputs_ok and sha(source)==pre['source_sha256']
binary_equal=sha(ROOT/'build/TGLExt/V351RegularCoreTraceContract.olean')==module['object_sha256']==pre['author_object_sha256']
assert binary_equal
save(OUT/'compilation.json',dict(all_exit_zero=True,exact_targets_and_allowed_axioms=True,
    module_binary_equals_author=binary_equal,author_source_dependencies_inputs_preserved=deps_ok and inputs_ok,
    project_dependencies=len(deps),module=module,auditor=audit,
    parser_correction='Universe suffixes printed under pp.universes normalized; first auditor output retained. Module not rebuilt after green.',
    completed=datetime.datetime.now().astimezone().isoformat()))

# Independent review of the author's eight controls: invoke only the pure check
# function extracted from its AST, never its top-level filesystem writer.
author=json.loads((ROOT/'AUDITORIA_A1.json').read_text(encoding='utf-8'))
positive_run=Path(author['accepted_attempt']);negative_run=Path(author['negative_attempt'])
pr=json.loads(positive_run.read_text());nr=json.loads(negative_run.read_text())
pos=(positive_run.parent/'stdout.txt').read_text(encoding='utf-8')
neg=(negative_run.parent/'stdout.txt').read_text(encoding='utf-8')
tree=ast.parse((ROOT/'audit_a1.py').read_text(encoding='utf-8'))
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='check')
scope={'re':re,'required':set(pre['names']),'allowed':allowed}
exec(compile(ast.Module(body=[fn],type_ignores=[]),'<pure check AST>','exec'),scope)
check=scope['check']
own_controls={
 'current_source_accepts':check(pr['returncode'],pos),
 'nonzero_returncode_rejects':not check(1,pos),
 'missing_axiom_entry_rejects':not check(0,'\n'.join(pos.splitlines()[:-1])),
 'unknown_axiom_rejects':not check(0,pos.replace('Quot.sound','Quot.sound, UNTRUSTED_CONTROL',1)),
 'duplicate_axiom_entry_rejects':not check(0,pos+pos),
 'false_numeric_theorem_rejected_by_lean':nr['returncode']!=0 and "'change' tactic failed" in neg and '= 2' in neg and 'sorryAx' in neg,
 'false_numeric_theorem_rejected_by_audit':not check(nr['returncode'],neg),
 'program_copy_unchanged':sha(ROOT/'um.py')==json.loads((ROOT/'BASE_E_FONTES.json').read_text())['program_sha256']}
assert all(own_controls.values()) and own_controls==author['tests']
probe=ROOT/'probes/A1FalseValue.lean'
assert sha(probe)==nr['source_sha256']==sha(negative_run.parent/probe.name)
snapshot=positive_run.parent/'V351RegularCoreTraceContract.lean'
assert sha(snapshot)==sha(source)==pr['source_sha256']==author['source_sha256']
history=[]
for p in sorted((ROOT/'attempts').glob('*/run.json')):
    d=json.loads(p.read_text());sp=p.parent/Path(d['command'][-1]).name
    op=p.parent/'stdout.txt';ep=p.parent/'stderr.txt'
    assert sha(sp)==d['source_sha256']
    history.append(dict(attempt=p.parent.name,returncode=d['returncode'],source_sha256=sha(sp),run_sha256=sha(p),stdout_sha256=sha(op),stderr_sha256=sha(ep),acceptance='accepted exact final source' if p==positive_run else 'negative mathematical probe' if p==negative_run else 'historical, not counted'))
    dest=OUT/'inputs'/p.parent.name;dest.mkdir(exist_ok=True)
    for q in [p,op,ep,sp]: save(dest/q.name,q.read_bytes())
diff=''.join(difflib.unified_diff(source.read_text(encoding='utf-8').splitlines(True),probe.read_text(encoding='utf-8').splitlines(True),fromfile='accepted_source',tofile='negative_probe'))
save(OUT/'negative_probe.diff.txt',diff.encode('utf-8'))
verification=dict(time=datetime.datetime.now().astimezone().isoformat(),status='PASS_LIMITED_A1_REVIEW',
    author_audit_sha256=sha(ROOT/'AUDITORIA_A1.json'),author_audit_script_sha256=sha(ROOT/'audit_a1.py'),
    compilation_sha256=sha(OUT/'compilation.json'),own_controls=own_controls,
    control_scope='Pure AST check function evaluated against saved streams. False numeric Lean probe not rerun; actual rc1/error/sorryAx output and pinned source read.',
    author_audit_idempotency='Existing report preserved; new execution would write timestamped audits/audit_*.json. Top-level not executed by reviewer.',
    history=history,source_sha256=sha(source),binary_sha256=module['object_sha256'],pins=pre['pins'],
    acceptance={'a':'PAGO_KERNEL','b':'NAO_PAGO','c':'PAGO_KERNEL_AUDIT'},findings_P0_P2=[])
save(OUT/'verification.json',verification)
print(json.dumps({k:verification[k] for k in ['status','acceptance','source_sha256','binary_sha256','findings_P0_P2']},ensure_ascii=False))
