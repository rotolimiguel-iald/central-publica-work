from pathlib import Path
import importlib.util,sys,types,math,json,hashlib,datetime
sys.dont_write_bytecode=True
p=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve()
if out.exists():raise FileExistsError(out)
pkg=types.ModuleType('beta_review');pkg.__path__=[str(p.parent)];sys.modules['beta_review']=pkg
spec=importlib.util.spec_from_file_location('beta_review.neutrino_contract',p);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
alpha=7.2973525693e-3
m.require_current=lambda op:dict(alpha=alpha,beta_tgl=alpha*math.sqrt(math.e),canonical_manifest_sha256='MOCK')
checks=[]
for chi in [100,1000,1500,1e300]:
    try:
        r=m.simulate({'channel':'beta_scale','chi':chi});beta=r['result']['beta_bulk']
        status='PASS' if beta>0 else 'FAIL_ZERO_UNDERFLOW_REPORTED_AS_BETA'
        checks.append(dict(chi=chi,status=status,beta_bulk=beta))
    except ValueError as e:checks.append(dict(chi=chi,status='PASS_VISIBLE_REFUSAL',error=str(e)))
report={'candidate_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'mathematical positivity or visible refusal; no claim of representability of arbitrarily small beta','checks':checks,'fail':sum(x['status'].startswith('FAIL') for x in checks)}
with out.open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
print(json.dumps(report))
