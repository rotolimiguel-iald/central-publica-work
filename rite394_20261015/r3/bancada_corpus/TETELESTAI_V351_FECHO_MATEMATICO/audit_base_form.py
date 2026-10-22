"""Audit compiled declarations and a mathematical tamper, without running um.py."""
from pathlib import Path
import datetime, hashlib, json, re, subprocess, sys, os

ROOT=Path(__file__).absolute().parent
SRC=ROOT/'kernel/TGLExt/V351ExtendedBaseDualWeight.lean'
GOOD=ROOT/'attempts/20260914_084253_409522'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p, raw):
    assert not p.exists(), p
    p.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(raw,str): raw=raw.encode('utf-8')
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f: f.write(raw)
    assert t.read_bytes()==raw
    os.replace(t,p)

source=SRC.read_text(encoding='utf-8')
expected=re.findall(r'^#print axioms (\w+)$',source,re.M)
assert len(expected)==14 and len(set(expected))==14
run=json.loads((GOOD/'run.json').read_bytes())
out=(GOOD/'stdout.txt').read_text(encoding='utf-8')
assert run['returncode']==0 and run['source_sha256']==sha(SRC)
assert not re.search(r'\b(error|warning):',out)
assert (GOOD/'stderr.txt').stat().st_size==0
rows=re.findall(r"'TGLV351\.(\w+)' depends on axioms: \[([^\]]*)\]",out)
allowed={'propext','Classical.choice','Quot.sound'}
assert {n for n,_ in rows}==set(expected)
assert all({x.strip() for x in a.split(',')} <= allowed for _,a in rows)
assert not re.search(r'\b(?:sorry|native_decide|trustCompiler)\b|^\s*axiom\s',source,re.M)

old='(baseDualWeight P (positiveAverageSquare P)).value (hOmega P) = 1 :='
assert source.count(old)==1
bad=source.replace(old,old.replace('= 1 :=','= 2 :='))
probe=ROOT/'probes/TGLExt/V351ExtendedBaseDualWeightTampered.lean'
new(probe,bad)
r=subprocess.run([sys.executable,'-X','utf8','-B',str(ROOT/'compile_a1.py'),str(probe)],capture_output=True)
negdir=ROOT/'audits'/('base_form_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
negdir.mkdir(parents=True)
new(negdir/'negative_stdout.txt',r.stdout)
new(negdir/'negative_stderr.txt',r.stderr)
nt=r.stdout.decode('utf-8')
assert r.returncode !=0 and 'error: Type mismatch' in nt and 'sorryAx' in nt
assert 'object file' not in nt and 'unknown module' not in nt
assert sha(SRC)==run['source_sha256']
obj=ROOT/'build/TGLExt/V351ExtendedBaseDualWeight.olean'
record=dict(timestamp=datetime.datetime.now().isoformat(),status='PASS_AUTHOR_AUDIT__A1B_STILL_OPEN',
 source=str(SRC),source_sha256=sha(SRC),object_sha256=sha(obj),positive_attempt=str(GOOD),
 checked_declarations=expected,allowed_axioms=sorted(allowed),no_warning=True,
 controls=['affiliation_in_original_base','pointwise_normality_on_all_base_vectors','bimodule_uses_fixedBaseEquiv','faithful_zero_test','unit_infinite_for_nonzero_vector','same_averageSquare_equals_one','tampered_averageSquare_equals_two_rejected'],
 negative=dict(path=str(probe),sha256=sha(probe),returncode=r.returncode,real_elaboration_error=True,audit_contains_sorryAx=True),
 parent_ficha_sha256=sha(ROOT/'REAPROVEITAMENTO_A1_BASE_ESTENDIDA.json'),
 dependency_manifest_sha256=sha(ROOT/'DEPENDENCIAS_A1_BASE_ESTENDIDA.json'),
 no_new_python_gate_or_program_change=True,
 remains_open=['predual_extended_positive_identification','dual_weight_modular_implementation','positive_generator','inverse_generator_trace'])
new(negdir/'audit.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
new(ROOT/'AUDITORIA_A1_BASE_ESTENDIDA.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False,indent=2))
