"""Fail-closed checks of the exact accepted module and negative proof probe."""
from pathlib import Path
import json,re,hashlib,datetime
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'kernel/TGLExt/V351RegularCoreTraceContract.lean'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
allowed={'propext','Classical.choice','Quot.sound'}
required=set(re.findall(r'^#print axioms (.+)$',SOURCE.read_text(encoding='utf-8'),re.M))
required={'TGLV351.'+n for n in required}
def check(rc,stdout):
 matches=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",stdout)
 parsed={n:set(filter(None,(a.strip() for a in axioms.split(',')))) for n,axioms in matches}
 return rc==0 and 'error:' not in stdout and 'warning:' not in stdout and len(matches)==len(parsed) and set(parsed)==required and all(a<=allowed for a in parsed.values())
attempts=[]
for p in sorted((ROOT/'attempts').glob('*/run.json')):
 d=json.loads(p.read_text());out=(p.parent/'stdout.txt').read_text(encoding='utf-8')
 attempts.append((p,d,out))
valid=[a for a in attempts if a[1]['source_sha256']==sha(SOURCE) and check(a[1]['returncode'],a[2])]
assert valid,'No accepted current-source compilation'
p,run,out=valid[-1]
negative=[a for a in attempts if Path(a[1]['command'][-1]).name=='A1FalseValue.lean']
assert negative and negative[-1][1]['returncode']!=0 and 'error:' in negative[-1][2] and 'sorryAx' in negative[-1][2], 'Expected elaboration failure in false theorem, not environment failure'
tests={
 'current_source_accepts':check(run['returncode'],out),
 'nonzero_returncode_rejects':not check(1,out),
 'missing_axiom_entry_rejects':not check(0,'\n'.join(out.splitlines()[:-1])),
 'unknown_axiom_rejects':not check(0,out.replace('Quot.sound','Quot.sound, UNTRUSTED_CONTROL',1)),
 'duplicate_axiom_entry_rejects':not check(0,out+out),
 'false_numeric_theorem_rejected_by_lean':negative[-1][1]['returncode']!=0,
 'false_numeric_theorem_rejected_by_audit':not check(negative[-1][1]['returncode'],negative[-1][2]),
 'program_copy_unchanged':sha(ROOT/'um.py')==json.loads((ROOT/'BASE_E_FONTES.json').read_text(encoding='utf-8'))['program_sha256'],
}
assert all(tests.values()),tests
deps=json.loads((ROOT/'DEPENDENCIAS_A1.json').read_text())
assert all(sha(ROOT/'build'/Path(*d['module'].split('.')).with_suffix('.olean'))==d['object_sha256'] for d in deps)
data=dict(status='PASS_STRICT_MODULE_AUDIT',time=datetime.datetime.now().isoformat(),source_sha256=sha(SOURCE),accepted_attempt=str(p),negative_attempt=str(negative[-1][0]),axiom_entries=len(required),allowed_axioms=sorted(allowed),dependency_objects_checked=len(deps),tests=tests,
 scope='One new module, not full um.py runtime. No canonical integration or gate movement.',acceptance={'a':'PAGO_KERNEL','b':'NAO_PAGO','c':'PAGO_KERNEL_AUDIT'})
target=ROOT/'AUDITORIA_A1.json'
if target.exists():
 target=ROOT/'audits'/('audit_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.json')
 target.parent.mkdir(parents=True,exist_ok=True)
temp=target.with_suffix('.json.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');assert temp.stat().st_size>0;temp.replace(target)
print(json.dumps(data,ensure_ascii=False,indent=2))
