"""Audit a final module and reject one mathematical tamper in an isolated probe."""
from pathlib import Path
import datetime, hashlib, json, re, subprocess, sys, os
ROOT=Path(__file__).absolute().parent
stem,attempt,label,expected_count=sys.argv[1:]
SRC=ROOT/'kernel/TGLExt'/(stem+'.lean')
GOOD=ROOT/'attempts'/attempt
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,raw):
    assert not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(raw,str): raw=raw.encode('utf-8')
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f: f.write(raw)
    assert t.read_bytes()==raw
    os.replace(t,p)
source=SRC.read_text(encoding='utf-8')
expected=re.findall(r'^#print axioms (\w+)$',source,re.M)
assert len(expected)==int(expected_count) and len(set(expected))==len(expected)
run=json.loads((GOOD/'run.json').read_bytes());out=(GOOD/'stdout.txt').read_text(encoding='utf-8')
assert run['returncode']==0 and run['source_sha256']==sha(SRC)
assert not re.search(r'\b(error|warning):',out) and (GOOD/'stderr.txt').stat().st_size==0
rows=re.findall(r"'TGLV351\.(\w+)' depends on axioms: \[([^\]]*)\]",out)
allowed={'propext','Classical.choice','Quot.sound'}
assert len(rows)==len(expected) and {n for n,_ in rows}==set(expected)
assert all({x.strip() for x in a.split(',')} <= allowed for _,a in rows)
assert not re.search(r'\b(?:sorry|native_decide|trustCompiler)\b|^\s*axiom\s',source,re.M)
if label=='AVALIACAO_FUNCIONAL':
    old='baseDualEvaluation P A 0 = 0 := by simp [baseDualEvaluation]'
    replacement='baseDualEvaluation P A 0 = 1 := by simp [baseDualEvaluation]'
else:
    assert label=='LEIS_FUNCIONAIS'
    old='baseDualEvaluation P (positiveAverageSquare P) (baseVectorFunctional P (hOmega P)) = 1 := by'
    replacement=old.replace('= 1 := by','= 2 := by')
assert source.count(old)==1
probe=ROOT/'probes/TGLExt'/(stem+'Tampered.lean');new(probe,source.replace(old,replacement))
r=subprocess.run([sys.executable,'-X','utf8','-B',str(ROOT/'compile_a1.py'),str(probe)],capture_output=True)
adir=ROOT/'audits'/('functional_'+label.lower()+'_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
new(adir/'negative_stdout.txt',r.stdout);new(adir/'negative_stderr.txt',r.stderr)
nt=r.stdout.decode('utf-8')
assert r.returncode!=0 and 'error:' in nt and 'sorryAx' in nt
assert 'object file' not in nt and 'unknown module' not in nt
assert sha(SRC)==run['source_sha256']
record=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='PASS_AUTHOR_AUDIT__A1B_OPEN',
 source=str(SRC),source_sha256=sha(SRC),object_sha256=sha(ROOT/'build/TGLExt'/(stem+'.olean')),
 positive_attempt=str(GOOD),checked_declarations=expected,allowed_axioms=sorted(allowed),no_warning=True,
 negative=dict(path=str(probe),sha256=sha(probe),returncode=r.returncode,real_elaboration_error=True,
   mutation=old+' => '+replacement,sorryAx_rejected=True),
 no_python_program_change=True,remains_open=['full_normal_positive_cone_coverage','same_weight_modular_implementation','positive_generator','inverse_generator_trace'])
new(adir/'audit.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
new(ROOT/('AUDITORIA_A1_'+label+'.json'),json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False,indent=2))
