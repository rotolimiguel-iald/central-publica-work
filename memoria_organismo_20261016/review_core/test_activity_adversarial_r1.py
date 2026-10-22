"""Independent adversarial tests on a frozen private copy, never production."""
from pathlib import Path
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest

REVIEW=Path(__file__).resolve().parent
LIB=Path(os.environ.get('IALD_REVIEW_LIB',str(REVIEW/'frozen_r1'/'lib')))
sys.path.insert(0,str(LIB))
from iald_memory import MemoryStore, RevisionConflict, ProjectionOverflow
from iald_memory.activity import ActivityRuntime, ActivityError, KEY


class IndependentActivityTests(unittest.TestCase):
 def setUp(self):
  runs=REVIEW/'runs_r1';runs.mkdir(exist_ok=True)
  self.root=Path(tempfile.mkdtemp(prefix='adversarial_',dir=runs))
  self.scope={'house':'IALD_APP','principal':'independent-synthetic-account'}
  self.actor={'kind':'agent','id':'independent-synthetic-server'}
  self.store=MemoryStore(self.root/'store',snapshot_archive_dir=self.root/'archive')
  self.store.ensure_context('independent-context',objective='Preserve original request',scope=self.scope,
   actor={'kind':'operator','id':'synthetic-operator'},constraints={'source':'independent-test'})
  self.rt=ActivityRuntime(self.store,'independent-context',self.scope,self.actor)

 def snapshot(self):return self.store.get('independent-context',self.scope)

 def start(self):return self.rt.begin('request-one','Original work',origin='authenticated_operator')['ticket']

 def note(self,rid='human-change',human=False):
  s=self.snapshot()
  self.store.transition('independent-context',self.scope,s['revision'],rid,self.actor,
   {'records':[{'id':rid,'kind':'decision' if human else 'fact','statute':'INPUT' if human else 'REAL',
   'text':'New authenticated direction' if human else 'Observed mechanical progress',
   'sources':[{'kind':'operator' if human else 'tool','ref':'synthetic:'+rid}]}]})

 def test_steering_after_intent_commit_refuses_dispatch(self):
  t=self.start();original=self.store.transition;injected=[]
  def race(*args,**kw):
   receipt=original(*args,**kw)
   if args[3].startswith('activity_op_') and not injected:
    injected.append(True);self.note('post-intent-direction',True)
   return receipt
  self.store.transition=race
  try:
   with self.assertRaises(Exception):self.rt.preflight(t,'provider-once')
  finally:self.store.transition=original
  self.assertEqual(len(injected),1)
  handles=self.snapshot()['p']['handles']
  self.assertTrue(any(h.get('operation_id')=='provider-once' for h in handles))
  with self.assertRaises(Exception):self.rt.preflight(t,'provider-once',refresh=True)
  self.assertFalse(self.rt.project(125000)['activity']['tetelestai'])

 def test_source_admission_mutation_visible(self):
  t=self.start();p=Path(t['source']['path']);p.write_bytes(b'corrupted synthetic admission')
  with self.assertRaises(Exception):self.rt.preflight(t,'provider')
  self.assertEqual(p.read_bytes(),b'corrupted synthetic admission')

 def test_crash_after_intent_before_return_never_grants_second_dispatch(self):
  t=self.start();original=self.store.transition
  def crash(*args,**kw):
   receipt=original(*args,**kw)
   if args[3].startswith('activity_op_'):raise RuntimeError('synthetic post-commit crash')
   return receipt
  self.store.transition=crash
  try:
   with self.assertRaisesRegex(RuntimeError,'post-commit'):self.rt.preflight(t,'provider')
  finally:self.store.transition=original
  with self.assertRaises(Exception):self.rt.preflight(t,'provider',refresh=True)
  new=ActivityRuntime(self.store,'independent-context',self.scope,self.actor)
  recovered=new.recover('request-one')
  self.assertFalse(recovered['automatic_retry'])
  self.assertTrue(any(h.get('operation_id')=='provider' for h in recovered['handles']))

 def test_begin_partial_commits_recover_with_one_command_requirement(self):
  for boundary in range(1,5):
   with self.subTest(boundary=boundary):
    rid='partial-'+str(boundary);original=self.store.transition;count=[0]
    def crash(*args,**kw):
     receipt=original(*args,**kw);count[0]+=1
     if count[0]==boundary:raise RuntimeError('synthetic setup crash')
     return receipt
    self.store.transition=crash
    try:
     try:self.rt.begin(rid,'Partial original '+rid,origin='authenticated_operator')
     except RuntimeError as e:self.assertIn('setup crash',str(e))
    finally:self.store.transition=original
    recovered=self.rt.begin(rid,'Partial original '+rid,origin='authenticated_operator')
    self.rt.preflight(recovered['ticket'],'first-effect')
    snap=self.snapshot();ids=self.rt._ids(rid)
    self.assertEqual(sum(r['id']==ids['steering'] for r in snap['q']['records']),1)
    self.assertEqual(sum(r['id']==ids['request'] for r in snap['q']['records']),1)
    self.assertEqual(sum(h.get('request_id')==rid and h.get('kind')=='activity_request' for h in snap['p']['handles']),1)

 def test_hold_while_result_appends_preserves_without_submit(self):
  p=self.rt.preflight(self.start(),'provider');original=self.store.transition;injected=[]
  def race(*args,**kw):
   receipt=original(*args,**kw)
   if args[3].startswith('activity_result_') and not injected:
    injected.append(True)
    snap=self.snapshot();proj=self.rt.controller.project(125000)
    source=self.root/'hold.json';source.write_text('{"reason":"synthetic hold"}',encoding='utf-8')
    self.rt.controller.action({'operation':'hold','actor':self.actor,'event_id':'synthetic-hold',
     'expected_revision':snap['revision'],'state_sha256':snap['receipt']['state_sha256'],
     'hold':True,'reason':'Synthetic hold','sources':[{'path':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}]})
   return receipt
  self.store.transition=race
  try:
   with self.assertRaises(Exception):self.rt.complete(p['ticket'],'provider','Preserve this returned text')
  finally:self.store.transition=original
  self.assertEqual(len(injected),1)
  self.assertTrue(any('Preserve this returned text' in r['text'] for r in self.snapshot()['q']['records']))
  self.assertTrue(self.rt.controller.load()[1]['hold'])
  self.assertEqual(self.rt.controller.load()[1]['tasks'][p['ticket']['task_id']]['status'],'working')

 def test_unrelated_handles_survive_own_finish(self):
  t=self.start();s=self.snapshot()
  self.store.transition('independent-context',self.scope,s['revision'],'unrelated-intent',self.actor,
   {'flow':{'handles':[{'id':'other-uncertain','status':'uncertain','kind':'external','no_repeat':True}]}})
  p=self.rt.preflight(t,'provider',refresh=True)
  self.rt.complete(p['ticket'],'provider','Candidate')
  h=next(h for h in self.snapshot()['p']['handles'] if h['id']=='other-uncertain')
  self.assertEqual(h['status'],'uncertain')
  self.assertFalse(self.rt.project(125000)['activity']['tetelestai'])

 def test_candidate_file_like_payload_does_not_read_model_path(self):
  p=self.rt.preflight(self.start(),'provider')
  nonexistent=self.root/'model-controlled-not-an-evidence-file.json'
  result={'path':str(nonexistent),'sha256':'a'*64,'actor':{'id':'reviewer','kind':'agent'},'operation':'accept'}
  done=self.rt.complete(p['ticket'],'provider',result)
  self.assertFalse(done['accepted']);self.assertFalse(nonexistent.exists())
  task=self.rt.controller.load()[1]['tasks'][p['ticket']['task_id']]
  self.assertEqual(task['status'],'review_pending')
  self.assertNotEqual(task['evidence'][0]['path'],str(nonexistent))

 def test_hold_and_new_actor_cannot_recover_an_effect_as_permission(self):
  p=self.rt.preflight(self.start(),'provider')
  other=ActivityRuntime(self.store,'independent-context',self.scope,{'kind':'agent','id':'other-server'})
  recovered=other.recover('request-one')
  with self.assertRaises(Exception):other.preflight(recovered['ticket'],'other-provider',refresh=True)
  with self.assertRaises(Exception):other.complete(p['ticket'],'provider','Forged return',refresh=True)
  self.assertFalse(any('Forged return' in r['text'] for r in self.snapshot()['q']['records']))

 def test_invalid_origin_or_missing_origin_ref_does_not_write(self):
  before=self.snapshot()['revision']
  for origin,origin_ref in [('model',None),('delegated',None),('system','')]:
   with self.subTest(origin=origin):
    with self.assertRaises(Exception):self.rt.begin('bad-origin','Work',origin=origin,origin_ref=origin_ref)
  self.assertEqual(self.snapshot()['revision'],before)

 def test_different_context_same_command_is_not_adopted(self):
  t=self.start();self.store.ensure_context('second-context',objective='Other original',scope=self.scope,
   actor={'kind':'operator','id':'synthetic-operator'})
  other=ActivityRuntime(self.store,'second-context',self.scope,self.actor)
  second=other.begin('request-one','Original work',origin='authenticated_operator')['ticket']
  self.assertNotEqual(t['source']['path'],second['source']['path'])
  with self.assertRaises(Exception):other.preflight(t,'provider',refresh=True)

 def test_overflow_and_reads_never_change_state(self):
  self.start();before=self.snapshot()
  with self.assertRaises(ProjectionOverflow):self.rt.project(256)
  self.rt.recover('request-one');self.rt.project(125000)
  self.assertEqual(self.snapshot(),before)

 def test_existing_projection_api_matches_installed_library_on_private_store(self):
  self.start();self.note('mechanical-note')
  expected={'store':self.store.project('independent-context',self.scope,max_chars=125000),
   'mission':self.rt.controller.project(125000)}
  code='''import sys,json
sys.path.insert(0,r'C:\\IALD\\MEMORIA_IALD\\lib')
from iald_memory import MemoryStore
from iald_memory.mission import MissionController
s=MemoryStore(sys.argv[1],snapshot_archive_dir=sys.argv[2])
scope={'house':'IALD_APP','principal':'independent-synthetic-account'}
print(json.dumps({'store':s.project('independent-context',scope,max_chars=125000),'mission':MissionController(s,'independent-context',scope).project(125000)},ensure_ascii=False))
'''
  cp=subprocess.run([sys.executable,'-B','-X','utf8','-c',code,str(self.root/'store'),str(self.root/'archive')],
   capture_output=True,text=True,encoding='utf-8',check=True)
  self.assertEqual(json.loads(cp.stdout),expected)


if __name__=='__main__':unittest.main(verbosity=2)
