
import copy,json,os,tempfile,unittest,hashlib,sys
from pathlib import Path
from unittest.mock import patch
sys.dont_write_bytecode=True
import scientific_memory_sync as helper
import importlib.util
spec=importlib.util.spec_from_file_location('iald_orchestrator.cm_sync_candidate',Path(__file__).parent/'candidate/iald_orchestrator/canonical_memory.py')
cm=importlib.util.module_from_spec(spec);spec.loader.exec_module(cm)
safe_spec=importlib.util.spec_from_file_location('iald_orchestrator.safe_sync_candidate',Path(__file__).parent/'candidate/iald_orchestrator/safe_files.py')
safe=importlib.util.module_from_spec(safe_spec);safe_spec.loader.exec_module(safe)
cm.save_json=safe.save_json

class SyncTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.src=self.root/'originals';self.src.mkdir()
  self.work=self.root/'work';self.releases=self.root/'releases';self.releases.mkdir()
  self.cat=self.root/'catalog.json';self.active=self.root/'ACTIVE.json'
  self.patches=[patch.object(cm,'CATALOG',self.cat),patch.object(cm,'RELEASES',self.releases),patch.object(cm,'ACTIVE',self.active),
    patch.object(helper,'require_claim'),patch('iald_orchestrator.program_controls.require_claim')]
  for p in self.patches:p.start()
  self.sync=helper.ScientificMemorySync(module=cm,work=self.work,_allowed_roots=(self.src,))
  self.write_sources('v900')
  self.active.write_text(json.dumps({'schema':1,'release':'v899','epoch':'v899_'+'0'*16,'generation':'0'*64,'manifest_sha256':'0'*64}))
  # Explicit cold-start fixture ONLY: no real ACTIVE or sources are consulted.
  original_load=cm.load
  def bootstrap(directory=None,**kw):
   if directory is None:return {'generation':'0'*64},'fixture_empty_baseline'
   return original_load(directory,**kw)
  with patch.object(cm,'load',side_effect=bootstrap):old=self.sync.prepare()
  self.sync.activate(old['epoch'])
  self.write_sources('v901')
  self.before=self.active.read_bytes()

 def tearDown(self):
  for p in reversed(self.patches):p.stop()
  self.temp.cleanup()

 def write_sources(self,version):
  payload={name:b'Scientific fixture line one\r\nline two remains CRLF\r\n' for name in cm.SNAPSHOT_NAMES}
  program=('UM_VERSION = \"'+version+'\"\r\n# original source never executed\r\n').encode();payload['um.py']=program
  record={'all_verified':True,'does_not_gate_core':True,'certificacao':{'um_py_sha256_lido_de_si':cm.digest(program)}}
  result={'core':{'estatuto_da_prova_v391':record,'estatuto_da_prova_ressalva_'+version:copy.deepcopy(record),'estatuto_reafirmado_'+version:copy.deepcopy(record)}}
  payload['um_absoluto.json']=json.dumps(result).encode()
  formal='a'*64;payload['tgl_kernel_proof_manifest.json']=json.dumps({'formal_source_hash':formal}).encode()
  payload['um_absoluto_selo.json']=json.dumps({'um_version':version,'fail_closed_selftest':'FAIL_CLOSED_SELFTEST_PASSED','formal_source_hash':formal,
   'sha256':{k:cm.digest(v) for k,v in payload.items() if k!='um_absoluto_selo.json'}}).encode()
  entries=[]
  for name,raw in payload.items():
   p=self.src/name;p.write_bytes(raw);entries.append({'source':str(p),'sha256':cm.digest(raw)})
  self.cat.write_text(json.dumps({'files':entries+[{'source':str(self.src/'article.pdf'),'sha256':'b'*64}]}))

 def test_check_readonly_detects_advance(self):
  before=list(self.work.iterdir());r=self.sync.check()
  self.assertEqual(r['sealed_version'],'v901');self.assertEqual(r['status'],'SEALED_ADVANCE_PENDING_SYNC')
  self.assertEqual(self.active.read_bytes(),self.before);self.assertEqual(before,list(self.work.iterdir()))

 def test_prepare_verify_crlf_generation_and_names(self):
  p=self.sync.prepare();v=self.sync.verify(p['epoch'])
  self.assertEqual(v['status'],'PASS');self.assertEqual(p['documents'],13)
  self.assertIn('estatuto_da_prova_v391',p['statute_record_names'])
  self.assertIn('estatuto_da_prova_ressalva_v901',p['statute_record_names'])
  snap=Path(p['target'])/'snapshots'/p['epoch']/'paper_PT.tex'
  self.assertEqual(snap.read_bytes(),(self.src/'paper_PT.tex').read_bytes());self.assertIn(b'\r\n',snap.read_bytes())
  self.assertEqual(self.active.read_bytes(),self.before)
  result=self.sync.prepare();self.assertEqual(result['status'],'REUSED_IMMUTABLE_RELEASE')

 def test_activation_existing_api_and_idempotency(self):
  p=self.sync.prepare();first=self.sync.activate(p['epoch']);active=self.active.read_bytes()
  self.assertEqual(first['status'],'ACTIVATED_BY_EXISTING_API')
  self.assertEqual(self.sync.activate(p['epoch'])['status'],'ALREADY_ACTIVE');self.assertEqual(active,self.active.read_bytes())
  helper.require_claim.assert_called_with('F0.3.MEMORIA_CIENTIFICA_SYNC','codex-coordenadora')

 def test_claim_failure_no_write(self):
  before=list(self.releases.iterdir())
  with patch.object(helper,'require_claim',side_effect=ValueError('not claimed')):
   with self.assertRaises(ValueError):self.sync.prepare()
  self.assertEqual(before,list(self.releases.iterdir()));self.assertEqual(self.before,self.active.read_bytes())

 def test_source_change_blocks_verify_and_activation(self):
  p=self.sync.prepare();(self.src/'paper_PT.tex').write_bytes(b'changed original')
  with self.assertRaises(ValueError):self.sync.verify(p['epoch'])
  with self.assertRaises(ValueError):self.sync.activate(p['epoch'])
  self.assertEqual(self.before,self.active.read_bytes())

 def test_seal_program_mismatch_refused(self):
  (self.src/'um.py').write_bytes(b'UM_VERSION = \"v902\"\\n')
  with self.assertRaises(ValueError):self.sync.prepare()
  self.assertEqual(self.before,self.active.read_bytes())

 def test_snapshot_adulteration_no_rebuild(self):
  p=self.sync.prepare();snapshot=Path(p['target'])/'snapshots'/p['epoch']/'paper_PT.tex';snapshot.write_bytes(b'altered')
  with self.assertRaises(ValueError):self.sync.verify(p['epoch'])
  with self.assertRaises(ValueError):self.sync.prepare()
  self.assertEqual(snapshot.read_bytes(),b'altered');self.assertEqual(self.before,self.active.read_bytes())

 def test_unreceipted_partial_release_refused(self):
  current=self.sync.current_sources();(self.releases/current['epoch']).mkdir()
  with self.assertRaises(ValueError):self.sync.prepare()
  self.assertEqual(self.before,self.active.read_bytes())


 def test_unknown_unit_refused(self):
  with self.assertRaises(ValueError):helper.ScientificMemorySync(module=cm,unit='F9.3')
  with self.assertRaises(ValueError):cm.activate_release(next(self.releases.iterdir()),unit='F9.3',member='codex-coordenadora')

 def test_index_altered_rejected_no_active_change(self):
  p=self.sync.prepare();index=Path(p['target'])/'index.sqlite3';index.write_bytes(index.read_bytes()+b'altered')
  with self.assertRaises(ValueError):self.sync.verify(p['epoch'])
  with self.assertRaises(ValueError):self.sync.activate(p['epoch'])
  self.assertEqual(self.active.read_bytes(),self.before)


 def test_concurrent_active_advance_preserved(self):
  first=self.sync.prepare()
  self.write_sources('v902');second=self.sync.prepare();self.sync.activate(second['epoch'])
  newer=self.active.read_bytes()
  self.write_sources('v901') # Restore first source pins in this disposable corpus.
  self.sync.verify(first['epoch'])
  with self.assertRaisesRegex(ValueError,'ACTIVE advanced'):
   self.sync.activate(first['epoch'])
  self.assertEqual(self.active.read_bytes(),newer)

 def test_change_between_api_gate_and_writer_read_refused(self):
  p=self.sync.prepare();baseline=self.active.read_bytes();competitor=baseline+b'\n'
  real_save=safe.save_json
  def raced(path,value,**kw):
   self.active.write_bytes(competitor)
   return real_save(path,value,**kw)
  before_backups=set(self.root.glob('ACTIVE.json.bak_*'))
  with patch.object(cm,'save_json',side_effect=raced):
   with self.assertRaisesRegex(ValueError,'baseline changed'):
    self.sync.activate(p['epoch'])
  self.assertEqual(self.active.read_bytes(),competitor)
  self.assertEqual(before_backups,set(self.root.glob('ACTIVE.json.bak_*')))

 def test_same_epoch_ack_after_changed_baseline_no_write(self):
  p=self.sync.prepare();self.sync.activate(p['epoch'])
  active=self.active.read_bytes();before=set(self.root.glob('ACTIVE.json.bak_*'))
  self.assertEqual(self.sync.activate(p['epoch'])['status'],'ALREADY_ACTIVE')
  self.assertEqual(active,self.active.read_bytes());self.assertEqual(before,set(self.root.glob('ACTIVE.json.bak_*')))

 def test_safe_writer_guard_before_commit(self):
  dest=self.root/'guarded.bin';dest.write_bytes(b'old')
  real=Path.read_bytes;count=[0]
  def inject(path):
   if path==dest:
    count[0]+=1
    if count[0]==2:path.write_bytes(b'newer')
   return real(path)
  with patch.object(Path,'read_bytes',inject):
   with self.assertRaisesRegex(ValueError,'before commit'):safe.replace_bytes(dest,b'candidate',expected_old=b'old')
  self.assertEqual(dest.read_bytes(),b'newer')


 def test_two_api_activations_share_lock_and_stale_loses(self):
  import threading
  p=self.sync.prepare();prior=json.loads(self.before);old_dir=self.releases/prior['epoch']
  entered=threading.Event();release=threading.Event();second_started=threading.Event();results=[];errors=[]
  real_save=safe.save_json
  def slow_save(*a,**kw):
   entered.set()
   if not release.wait(5):raise RuntimeError('fixture timeout')
   return real_save(*a,**kw)
  def first():
   try:results.append(cm.activate_release(Path(p['target']),unit=self.sync.unit,member=self.sync.member,expected_active_sha256=cm.digest(self.before)))
   except Exception as e:errors.append(('first',str(e)))
  def second():
   second_started.set()
   try:results.append(cm.activate_release(old_dir,unit=self.sync.unit,member=self.sync.member,expected_active_sha256=cm.digest(self.before)))
   except Exception as e:errors.append(('second',str(e)))
  with patch.object(cm,'save_json',side_effect=slow_save):
   a=threading.Thread(target=first);a.start();self.assertTrue(entered.wait(5))
   b=threading.Thread(target=second);b.start();self.assertTrue(second_started.wait(5));release.set();a.join(5);b.join(5)
   self.assertFalse(a.is_alive());self.assertFalse(b.is_alive())
  self.assertEqual(len(results),1);self.assertEqual(errors[0][0],'second')
  self.assertIn('ACTIVE advanced',errors[0][1]);self.assertEqual(json.loads(self.active.read_bytes())['epoch'],p['epoch'])


 def test_same_epoch_adulterated_pointer_refused(self):
  p=self.sync.prepare();self.sync.activate(p['epoch']);good=self.active.read_bytes()
  for field,value in [('manifest_sha256','0'*64),('release','v666'),('schema',99)]:
   bad=json.loads(good);bad[field]=value;raw=json.dumps(bad).encode();self.active.write_bytes(raw)
   with self.subTest(field=field),self.assertRaises(ValueError):self.sync.activate(p['epoch'])
   self.assertEqual(self.active.read_bytes(),raw)
   self.active.write_bytes(good)

if __name__=='__main__':unittest.main(verbosity=2)
