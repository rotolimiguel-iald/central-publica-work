"""Run the exact deployment AST only against bounded synthetic fixture paths."""
from pathlib import Path
import ast,hashlib,json,subprocess,sys,uuid,datetime,unittest
BASE=Path(__file__).resolve().parents[1]
TESTS=BASE/'tests_core'
SOURCE=(BASE/'deploy_candidate.py').read_bytes()
SOURCE_SHA=hashlib.sha256(SOURCE).hexdigest()
RUN=TESTS/'temp'/('deploy_transaction_'+uuid.uuid4().hex)
RUN.mkdir(parents=True)
assert RUN.resolve().is_relative_to(TESTS.resolve())
SNAPSHOT=RUN/'deployment_source_snapshot.py';SNAPSHOT.write_bytes(SOURCE)
RESULTS=[]

RUNNER=r"""
from pathlib import Path
import ast,sys,os
source,root,mode,fail=sys.argv[1:]
root=Path(root).resolve()
if not root.is_relative_to(Path(__file__).resolve().parent):raise RuntimeError('fixture escaped')
target=root/'installed';candidate=root/'candidate'
for p in (root,target,candidate):
 if not p.resolve().is_relative_to(Path(__file__).resolve().parent):raise RuntimeError('unbounded fixture')
raw=Path(source).read_bytes();tree=ast.parse(raw.decode('utf-8-sig'))
values={'BASE':root,'CANDIDATE':candidate,'TARGET':target}
changed=[]
for node in tree.body:
 if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id in values:
  name=node.targets[0].id
  node.value=ast.Call(func=ast.Name(id='Path',ctx=ast.Load()),args=[ast.Constant(str(values[name]))],keywords=[])
  changed.append(name)
if sorted(changed)!=['BASE','CANDIDATE','TARGET']:raise RuntimeError('unexpected source layout')
ast.fix_missing_locations(tree)
if 'C:/IALD/Bancada_Um' in ast.unparse(tree):raise RuntimeError('production target survived rewrite')
# The only injected failure is before replacing the second synthetic file.
replace=os.replace;fired=False
if fail=='yes':
 def fail_once(src,dst):
  global fired
  if Path(dst).resolve()==(target/'bancada'/'second.py').resolve() and not fired:
   fired=True
   raise OSError('SYNTHETIC_SECOND_FILE_REPLACE_FAILURE')
  return replace(src,dst)
 os.replace=fail_once
sys.argv=['deploy_candidate.py']+(['--apply'] if mode=='apply' else [])
exec(compile(tree,str(source),'exec'),{'__name__':'__main__','__file__':str(root/'deploy_candidate.py')})
"""
runner=RUN/'fixture_runner.py';runner.write_text(RUNNER,encoding='utf-8')

def hashbytes(x):return hashlib.sha256(x).hexdigest()
def fixture(name):
 root=RUN/name;candidate=root/'candidate';target=root/'installed'
 candidate.mkdir(parents=True);target.mkdir()
 old={'bancada/first.py':b'OLD_FIRST\r\n','bancada/second.py':b'OLD_SECOND\r\n','canonical_contracts.json':b'{"old_synthetic_manifest":true}\r\n'}
 new={'bancada/first.py':b'NEW_FIRST\n','bancada/second.py':b'NEW_SECOND\n'}
 for rel,raw in old.items():p=target/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
 for rel,raw in new.items():p=candidate/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
 man={'code':[dict(path=n,sha256=hashbytes(v),bytes=len(v)) for n,v in new.items()],'sources':[]}
 new['canonical_contracts.json']=(json.dumps(man,indent=2)+'\n').encode();(candidate/'canonical_contracts.json').write_bytes(new['canonical_contracts.json'])
 baseline=[dict(source=str((target/n).resolve()),sha256=hashbytes(raw),bytes=len(raw)) for n,raw in old.items()]
 (root/'BASELINE_R1.json').write_text(json.dumps(baseline),encoding='utf-8')
 return root,target,new,old

def execute(root,mode,fail=False):
 cmd=[sys.executable,'-B','-X','utf8',str(runner),str(SNAPSHOT),str(root),mode,'yes' if fail else 'no']
 start=datetime.datetime.now(datetime.timezone.utc);r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');end=datetime.datetime.now(datetime.timezone.utc)
 name=mode+('_fault' if fail else '')+'.log';p=root/name
 with p.open('x',encoding='utf-8',newline='\n') as f:f.write('COMMAND: '+repr(cmd)+'\nSTART: '+start.isoformat()+'\nEND: '+end.isoformat()+'\nEXIT: '+str(r.returncode)+'\n'+r.stdout+r.stderr)
 return r

class DeploymentFixtureTests(unittest.TestCase):
 def test_failed_second_replace_restores_first(self):
  root,target,new,old=fixture('injected_failure')
  prep=execute(root,'prepare');self.assertEqual(prep.returncode,0,prep.stderr)
  plan=json.loads((root/'DEPLOY_PLAN_R1.json').read_bytes());self.assertEqual(len(plan['files']),3)
  app=execute(root,'apply',True);self.assertNotEqual(app.returncode,0);self.assertIn('SYNTHETIC_SECOND_FILE_REPLACE_FAILURE',app.stderr)
  restored={n:(target/n).read_bytes()==raw for n,raw in old.items()};self.assertTrue(all(restored.values()),restored)
  failures=list(root.glob('DEPLOY_FAILURE_*.json'));self.assertEqual(len(failures),1)
  receipt=json.loads(failures[0].read_bytes());self.assertEqual(receipt['rollback'],[{'path':'bancada/first.py','restored':True}])
  self.assertFalse((root/'DEPLOY_RECEIPT_R1.json').exists())
  self.assertEqual(list(target.rglob('*.b2tmp')),[])
  backups={}
  for n in ('bancada/first.py','bancada/second.py'):
   p=target/n;bak=list(p.parent.glob(p.name+'.bak_B2_*'));self.assertEqual(len(bak),1);self.assertEqual(bak[0].read_bytes(),old[n]);backups[n]=hashbytes(bak[0].read_bytes())
  RESULTS.append({'scenario':'SECOND_REPLACE_FAILURE','prepare_exit':prep.returncode,'apply_exit':app.returncode,'restored_byte_for_byte':restored,'backups':backups,'failure_receipt':str(failures[0].relative_to(TESTS)),'fixture':str(root.relative_to(TESTS))})
 def test_success_preserves_backup_bytes(self):
  root,target,new,old=fixture('successful_install')
  prep=execute(root,'prepare');self.assertEqual(prep.returncode,0,prep.stderr)
  app=execute(root,'apply');self.assertEqual(app.returncode,0,app.stderr)
  receipt=json.loads((root/'DEPLOY_RECEIPT_R1.json').read_bytes());self.assertEqual(receipt['status'],'INSTALLED_AWAITING_RUNTIME_CHECK')
  results={}
  for e in receipt['files']:
   n=e['relative'];self.assertEqual((target/n).read_bytes(),new[n]);self.assertEqual(Path(e['backup']).read_bytes(),old[n]);self.assertEqual(e['old_sha256'],hashbytes(old[n]))
   results[n]={'new_matches':True,'backup_exact':True,'backup_sha256':hashbytes(old[n]),'new_sha256':hashbytes(new[n])}
  self.assertEqual(len(results),3);self.assertEqual(list(target.rglob('*.b2tmp')),[])
  RESULTS.append({'scenario':'SUCCESS','prepare_exit':prep.returncode,'apply_exit':app.returncode,'files':results,'fixture':str(root.relative_to(TESTS))})

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
 stable=hashbytes((BASE/'deploy_candidate.py').read_bytes())==SOURCE_SHA
 receipt={'source_sha256':SOURCE_SHA,'source_unchanged_after_test':stable,'tests':result.testsRun,'success':result.wasSuccessful(),'failures':len(result.failures),'errors':len(result.errors),'scenarios':RESULTS,'production_target_touched':False,'adapted_globals':['BASE','CANDIDATE','TARGET'],'fault_injection':'os.replace second synthetic file only','prepare_cli':'default mode without --apply; source has no --prepare flag','fixture_root':str(RUN),'retained_for_review':True}
 p=TESTS/'DEPLOY_TRANSACTION_FIXTURE_RESULT.json'
 with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(receipt,f,ensure_ascii=False,indent=2);f.write('\n')
 print(json.dumps({'receipt':str(p),'sha256':hashbytes(p.read_bytes()),'success':result.wasSuccessful(),'source_stable':stable},ensure_ascii=False))
 sys.exit(0 if result.wasSuccessful() and stable else 1)
