"""Preserve frozen Q/R1 and repair only custody/freshness separation in R2."""
import hashlib,json,shutil
from pathlib import Path
W=Path(__file__).resolve().parents[1]
old=W/'staging/queue';new=old/'r2'
assert not new.exists()
files=list(old.rglob('*.py'))
for p in files:
    dst=new/p.relative_to(old);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dst)
p=new/'iald_orchestrator/queue_activity.py'
s=p.read_text(encoding='utf-8')
s=s.replace("      CREATE TABLE IF NOT EXISTS queue_activity_returns (", """      CREATE TABLE IF NOT EXISTS queue_activity_custody (
        entity_id TEXT PRIMARY KEY, kind TEXT NOT NULL, binding_json TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS queue_activity_returns (""")
s=s.replace("    # Coordination is a durable operation spanning preparation/worker/synthesis.","""        # Separate immutable admission identity: current bindings may become stale
        # while an external call is in flight. Returns still belong to this UUID.
        admitted = db.execute('SELECT * FROM queue_activity_custody WHERE entity_id=?', (entity_id,)).fetchone()
        if admitted and (admitted['kind'] != kind or json.loads(admitted['binding_json']) != data):
            raise ValueError('Custody admission differs')
        db.execute('INSERT OR IGNORE INTO queue_activity_custody VALUES(?,?,?)',
                   (entity_id,kind,opmem.encode(data)))
    # Coordination is a durable operation spanning preparation/worker/synthesis.""")
s=s.replace("def load(runtime, kind, entity_id):", """def custody(runtime, kind, entity_id):
    \"\"\"Original server admission only; never a current dispatch/integration grant.\"\"\"
    if kind not in ('task','coord'):
        raise ValueError('Invalid entity kind')
    uuid.UUID(entity_id)
    with runtime.db() as db:
        row = db.execute('SELECT * FROM queue_activity_custody WHERE entity_id=?', (entity_id,)).fetchone()
    if not row or row['kind'] != kind:
        raise ValueError('Durable custody admission missing')
    data = json.loads(row['binding_json'])
    if data['id'] != entity_id or data['kind'] != kind or data['scope'] != opmem.SCOPE:
        raise ValueError('Invalid custody identity')
    return data

def load(runtime, kind, entity_id):""")
s=s.replace("    if data != _binding(row, kind, binding['parent_id']):", "    if data != custody(runtime,kind,entity_id) or data != _binding(row, kind, binding['parent_id']):")
s=s.replace("    load(runtime, kind, entity_id)\n    text = opmem.encode(result)", "    custody(runtime, kind, entity_id)\n    text = opmem.encode(result)")
s=s.replace("    result = describe(runtime,kind,entity_id)\n    with runtime.db() as db:", """    try:
        result = describe(runtime,kind,entity_id)
    except ValueError:
        # Current envelope refused; expose the existing return in its original
        # server-owned context. This is read-only, never a reconciliation grant.
        admitted = custody(runtime,kind,entity_id)
        result = {'protocol':'iald-queue-activity/v1','scope':opmem.SCOPE,
            'context_id':admitted['context_id'],'entity_id':entity_id,
            'request_id':admitted['request_id'],'parent_id':admitted['parent_id'],
            'reconciliation_required':True,'integration_allowed':False,
            'error':'current_activity_envelope_refused','automatic_retry':False,
            'semantic_acceptance':False,
            'projection':runtime_for(runtime,admitted['context_id']).project(max_chars=125000)}
    with runtime.db() as db:""")
p.write_text(s,encoding='utf-8',newline='\n')
# New test/harness versions; frozen R1 sources and reports stay byte-identical.
tests=(W/'tests_queue/test_queue_activity_r1.py').read_text(encoding='utf-8').replace("str(W/'staging/queue')", "str(W/'staging/queue/r2')").replace('process_fixture_r1.py','process_fixture_r2.py')
tests+='''

    def _return_after_mutation(self, column):
        t=self.task()
        whole={'text':'complete late response after '+column,'usage':{'output_tokens':17},'nested':{'all':[1,2,3]}}
        def result(*a,**kw):
            with self.rt.db() as db:
                if column=='prompt':
                    db.execute('UPDATE tasks SET prompt=? WHERE id=?',('Changed during provider',t['id']))
                elif column=='constraints':
                    db.execute('UPDATE tasks SET execution_constraints=? WHERE id=?',('null ',t['id']))
                    # Valid but changed restriction semantics, not only whitespace.
                    db.execute('UPDATE tasks SET execution_constraints=? WHERE id=?',(json.dumps({'mission_id':'ORDEM_016','branch_id':'NEW','lemma_id':'L2','role':'draft','required_provider':'mimo','max_calls':1}),t['id']))
                else:
                    b=db.execute('SELECT binding_json FROM queue_activity_bindings WHERE entity_id=?',(t['id'],)).fetchone()
                    data=json.loads(b[0]);data['prompt']='Binding changed while in flight'
                    db.execute('UPDATE queue_activity_bindings SET binding_json=? WHERE entity_id=?',(json.dumps(data),t['id']))
            return whole
        self.execute.side_effect=result
        done=self.perform(t)
        self.assertEqual(done['status'],'review_required',done['error'])
        self.assertEqual(done['result'],whole)
        with self.rt.db() as db:
            rows=db.execute('SELECT * FROM queue_activity_returns WHERE entity_id=?',(t['id'],)).fetchall()
        self.assertEqual(len(rows),1)
        self.assertEqual(json.loads(rows[0]['result_json']),whole)
        self.assertEqual(rows[0]['digest'],om.digest(om.encode(whole)))
        recovery=qa.recover(self.rt,'task',t['id'])
        self.assertTrue(recovery['reconciliation_required'])
        self.assertFalse(recovery['integration_allowed'])
        self.assertEqual(recovery['context_id'],t['memory_context_id'])
        self.assertNotEqual(recovery['projection']['activity']['active'][0]['status'],'satisfied')
        with self.assertRaises(ValueError):qa.reconcile(self.rt,'task',t['id'])
        self.rt._drain();self.assertEqual(self.execute.call_count,1)

    def test_return_after_prompt_mutation_is_durable(self):
        self._return_after_mutation('prompt')

    def test_return_after_constraints_mutation_is_durable(self):
        self._return_after_mutation('constraints')

    def test_return_after_binding_mutation_is_durable(self):
        self._return_after_mutation('binding')

    def test_raw_return_requires_prior_custody_identity(self):
        t=self.task()
        with self.assertRaises(ValueError):qa.raw_return(self.rt,'task',str(uuid.uuid4()),{'text':'unadmitted'})
        with self.assertRaises(ValueError):qa.raw_return(self.rt,'coord',t['id'],{'text':'wrong-kind'})
        self.assertEqual(self.execute.call_count,0)
'''
(W/'tests_queue/test_queue_activity_r2.py').write_text(tests,encoding='utf-8',newline='\n')
for src,dst in [('process_fixture_r1.py','process_fixture_r2.py'),('run_tests_r2.py','run_tests_r3.py'),('mcp_smoke_r3.py','mcp_smoke_r4.py')]:
    s=(W/'tests_queue'/src).read_text(encoding='utf-8')
    s=s.replace('test_queue_activity_r1','test_queue_activity_r2').replace('process_fixture_r1','process_fixture_r2')
    s=s.replace("staging/queue", "staging/queue/r2")
    if src=='run_tests_r2.py':s=s.replace('QUEUE_TEST_LOG_R2','QUEUE_TEST_LOG_R3').replace('QUEUE_TEST_RESULT_R2','QUEUE_TEST_RESULT_R3')
    if src=='mcp_smoke_r3.py':s=s.replace('MCP_STDIO_RESULT_R3','MCP_STDIO_RESULT_R4')
    (W/'tests_queue'/dst).write_text(s,encoding='utf-8',newline='\n')
print(json.dumps({'r2_source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'copied_python_files':len(files)}))
