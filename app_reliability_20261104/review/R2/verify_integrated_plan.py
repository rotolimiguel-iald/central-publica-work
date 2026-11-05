from pathlib import Path
import sys,os,json,hashlib,importlib.util,unittest,io
ROOT=Path(__file__).resolve().parent
W=ROOT.parent.parent
sys.dont_write_bytecode=True
def guard(event,args):
    if event in ('socket.connect','socket.bind','socket.getaddrinfo'):raise RuntimeError('Offline review')
    if event=='open':
        p,mode,flags=args
        if (isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC)):
            if isinstance(p,(str,bytes,os.PathLike)) and not Path(p).resolve().is_relative_to(ROOT):raise RuntimeError('Write outside review')
sys.addaudithook(guard)
sys.path.insert(0,str(W))
import prepare_release as prep
plan=json.loads((W/'INSTALL_PLAN.json').read_bytes())
outputs=prep.staged_bytes()
checks=[]
for row in plan['files']:
    p=Path(row['path']);raw=outputs[p.name]
    checks.append({'name':p.name,'after_matches':hashlib.sha256(raw).hexdigest()==row['after'],'bytes_match':len(raw)==row['bytes'],'before_matches':(hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None)==row['before']})
sources=[{'path':row['path'],'match':hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256']} for row in plan['sources']]
spec=importlib.util.spec_from_file_location('credential_integration_offline',W/'test_integrated_credential.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.W=ROOT
log=io.StringIO();result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(m.CredentialTests))
(ROOT/'CREDENTIAL_INTEGRATION_LOG.txt').write_text(log.getvalue(),encoding='utf8')
out={'plan_sha256':hashlib.sha256((W/'INSTALL_PLAN.json').read_bytes()).hexdigest(),'installer_sha256':hashlib.sha256((W/'install_release.py').read_bytes()).hexdigest(),'checks':checks,'sources':sources,'credential_tests':{'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors)},'network':False,'production_written':False,'server_preamble_emitted':False,'private_credential_read':False}
(ROOT/'INTEGRATED_PLAN.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out))
