"""Real local queue/core/CLI with fake transports; no real legacy job touched."""
import json,uuid,sys,subprocess,threading
from unittest.mock import patch
from test_queue_activity_r3 import QueueActivityTests,W,qa,om
from iald_orchestrator import legacy_activity_migration as migration
from iald_orchestrator.process_lock import process_lock

class LegacyMigrationTests(QueueActivityTests):
    # The runner loads only migration_* here, and the 29 regressions separately.
    def legacy(self,prepared=False,constraints=None):
        with patch.object(qa,'admit'):
            j=self.c.create('Original legacy command '+str(uuid.uuid4()),str(uuid.uuid4()),constraints)
        with self.rt.db() as db:db.execute('UPDATE coordination_jobs SET activity_version=0 WHERE id=?',(j['id'],))
        if prepared:self.c._act(j['id'],'prepare_without_work',{'reason':'assistance_not_needed','prompt':'Exact prepared local text'})
        with self.rt.db() as db:row=migration._row(db,j['id'])
        return row

    def request(self,row):
        i=migration.inspect(self.rt,row['id'])
        return dict(job_id=row['id'],expected_version=i['version'],expected_row_sha256=i['row_sha256'],
            expected_memory_revision=i['memory_revision'],expected_memory_state_sha256=i['memory_state_sha256'],event_id=str(uuid.uuid4()))

    def migration_local_preserves_semantics_and_enables_existing_flow(self):
        c={'mission_id':'ORDEM_016','branch_id':'TEST','lemma_id':'L1','role':'draft','required_provider':'kimi','max_calls':1,'memory_generation':'a'*64}
        for prepared in (False,True):
            row=self.legacy(prepared,c);r=self.request(row)
            with patch.object(self.rt,'start_worker',side_effect=AssertionError('NO WORKER')):
                result=migration.migrate(self.rt,**r)
            self.assertFalse(result['dispatch_allowed']);self.assertEqual(self.execute.call_count,0)
            with self.rt.db() as db:after=migration._row(db,row['id'])
            self.assertEqual({k:v for k,v in after.items() if k not in ('activity_version','version')},
                             {k:v for k,v in row.items() if k not in ('activity_version','version')})
            self.assertEqual(after['activity_version'],1);self.assertEqual(after['version'],row['version']+1)
            self.assertEqual(migration.migrate(self.rt,**r),dict(result,replayed=True))
            if not prepared:self.c.act(row['id'],'prepare_without_work',{'reason':'assistance_not_needed'})
            with patch.object(self.rt,'start_worker') as worker:self.c.act(row['id'],'execute')
            self.assertEqual(worker.call_count,1) # separate subsequent authorized queue command
            self.assertEqual(self.execute.call_count,0)

    def migration_inspect_is_readonly_and_cli_is_real_private(self):
        row=self.legacy(True);before=om.store(self.rt).get(row['memory_context_id'],om.SCOPE)
        def cli(payload):
            cp=subprocess.run([sys.executable,'-B','-X','utf8',str(W/'tests_queue/process_fixture_r3.py'),'migration',str(self.root)],
                input=json.dumps(payload),capture_output=True,text=True,encoding='utf-8',timeout=30)
            self.assertEqual(cp.returncode,0,cp.stderr+cp.stdout);return json.loads(cp.stdout)['result']
        v=cli({'operation':'inspect','job_id':row['id']});self.assertTrue(v['eligible'])
        self.assertEqual(before,om.store(self.rt).get(row['memory_context_id'],om.SCOPE))
        result=cli(dict(operation='migrate',**self.request(row)));self.assertEqual(result['activity_version'],1)
        self.assertEqual(self.execute.call_count,0)

    def migration_stale_cas_and_payload_refused(self):
        row=self.legacy();r=self.request(row)
        for field,value in [('expected_version',999),('expected_row_sha256','f'*64),('expected_memory_revision',999),('expected_memory_state_sha256','f'*64)]:
            with self.assertRaises(ValueError):migration.migrate(self.rt,**dict(r,**{field:value}))
        with self.rt.db() as db:self.assertEqual(migration._row(db,row['id'])['activity_version'],0)

    def migration_terminal_external_and_unknown_states_refused(self):
        for field,value in [('stage','completed'),('stage','draft_dispatching'),('stage','execution_waiting'),('thread_id',str(uuid.uuid4())),('execution_task_id',str(uuid.uuid4())),('error','uncertain'),('synthesis_source','executor'),('final_text','already returned')]:
            row=self.legacy();r=self.request(row)
            with self.rt.db() as db:db.execute('UPDATE coordination_jobs SET '+field+'=? WHERE id=?',(value,row['id']))
            with self.assertRaises(ValueError):migration.migrate(self.rt,**r)

    def migration_prior_dispatch_event_refused_even_if_fields_cleared(self):
        row=self.legacy();r=self.request(row)
        with self.rt.db() as db:
            db.execute('INSERT INTO coordination_events(job_id,at,action,from_stage,to_stage) VALUES(?,?,?,?,?)',
                (row['id'],'test','begin_draft','awaiting_dispatch','draft_dispatching'))
        with self.assertRaises(ValueError):migration.migrate(self.rt,**r)

    def migration_deterministic_child_and_orphan_attempt_refused(self):
        row=self.legacy();r=self.request(row);child=str(uuid.uuid5(uuid.NAMESPACE_URL,'iald-coordination:'+row['id']))
        with self.rt.db() as db:
            db.execute('INSERT INTO attempts(task_id,provider,started_at,status) VALUES(?,?,?,?)',(child,'kimi','test','uncertain'))
        with self.assertRaises(ValueError):migration.migrate(self.rt,**r)
        row=self.legacy();r=self.request(row);child=str(uuid.uuid5(uuid.NAMESPACE_URL,'iald-coordination:'+row['id']))
        with self.rt.db() as db:
            db.execute('INSERT INTO tasks(id,request_id,prompt,created_at,updated_at,status) VALUES(?,?,?,?,?,?)',
                (str(uuid.uuid4()),child,'unchanged','test','test','cancelled'))
        with self.assertRaises(ValueError):migration.migrate(self.rt,**r)

    def migration_external_or_uncertain_memory_handle_refused(self):
        for h in ({'id':'remote','status':'uncertain'},{'id':'remote','status':'completed'},{'id':'other','phase':'running'}):
            row=self.legacy();state=om.store(self.rt).get(row['memory_context_id'],om.SCOPE)
            om.store(self.rt).transition(row['memory_context_id'],om.SCOPE,state['revision'],str(uuid.uuid4()),qa.ACTOR,{'flow':{'handles':[h]}})
            self.assertFalse(migration.inspect(self.rt,row['id'])['eligible'])
            with self.assertRaises(ValueError):migration.migrate(self.rt,**self.request(row))

    def migration_crash_after_queue_intent_resumes_locally(self):
        row=self.legacy();r=self.request(row)
        with patch.object(migration._TrackedStore,'recover_steps',side_effect=RuntimeError('crash after durable queue intent')):
            with self.assertRaises(RuntimeError):migration.migrate(self.rt,**r)
        with self.rt.db() as db:
            self.assertEqual(migration._row(db,row['id'])['activity_version'],0)
            self.assertEqual(db.execute('SELECT status FROM queue_activity_migrations WHERE job_id=?',(row['id'],)).fetchone()[0],'prepared')
        self.assertEqual(migration.migrate(self.rt,**r)['activity_version'],1)
        self.assertEqual(self.execute.call_count,0)

    def migration_crash_after_acom_commit_before_queue_checkpoint_resumes(self):
        row=self.legacy();r=self.request(row)
        with patch.object(migration._TrackedStore,'_checkpoint',side_effect=RuntimeError('crash after ACOM commit')):
            with self.assertRaises(RuntimeError):migration.migrate(self.rt,**r)
        with self.rt.db() as db:self.assertEqual(migration._row(db,row['id'])['activity_version'],0)
        result=migration.migrate(self.rt,**r);self.assertEqual(result['activity_version'],1)
        with self.rt.db() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM queue_activity_migration_steps WHERE job_id=? AND receipt_json IS NULL',(row['id'],)).fetchone()[0],0)
        self.assertEqual(self.execute.call_count,0)

    def migration_foreign_memory_change_after_crash_is_not_rebased(self):
        row=self.legacy();r=self.request(row)
        with patch.object(migration._TrackedStore,'_checkpoint',side_effect=RuntimeError('crash')):
            with self.assertRaises(RuntimeError):migration.migrate(self.rt,**r)
        memory=om.store(self.rt);state=memory.get(row['memory_context_id'],om.SCOPE)
        memory.transition(row['memory_context_id'],om.SCOPE,state['revision'],'foreign-change',qa.ACTOR,{'flow':{'phase':'human-review'}})
        with self.assertRaises(ValueError):migration.migrate(self.rt,**r)
        with self.rt.db() as db:self.assertEqual(migration._row(db,row['id'])['activity_version'],0)
        self.assertEqual(self.execute.call_count,0)

    def migration_row_change_after_crash_is_not_rebased(self):
        row=self.legacy();r=self.request(row)
        with patch.object(migration._TrackedStore,'recover_steps',side_effect=RuntimeError('crash')):
            with self.assertRaises(RuntimeError):migration.migrate(self.rt,**r)
        with self.rt.db() as db:db.execute('UPDATE coordination_jobs SET prompt=? WHERE id=?',('changed',row['id']))
        with self.assertRaises(ValueError):migration.migrate(self.rt,**r)
        with self.assertRaises(ValueError):migration.migrate(self.rt,**dict(r,event_id=str(uuid.uuid4())))

    def migration_queue_lock_and_two_writers(self):
        row=self.legacy();r=self.request(row)
        with process_lock(self.rt.db_path,blocking=False) as locked:
            self.assertTrue(locked)
            with self.assertRaises(ValueError):migration.migrate(self.rt,**r)
        barrier=threading.Barrier(2);answers=[]
        def work():
            barrier.wait()
            try:answers.append(migration.migrate(self.rt,**r))
            except ValueError as exc:answers.append(str(exc))
        ts=[threading.Thread(target=work) for _ in range(2)]
        for t in ts:t.start()
        for t in ts:t.join(15);self.assertFalse(t.is_alive())
        self.assertEqual(sum(isinstance(x,dict) and not x['replayed'] for x in answers),1)

    def migration_no_model_tool_or_arbitrary_fields(self):
        row=self.legacy()
        with self.assertRaises(ValueError):migration.invoke(self.rt,{'operation':'inspect','job_id':row['id'],'actor':'operator'})
        from iald_orchestrator.activity_bridge import invoke
        with self.assertRaises(ValueError):invoke(self.rt,{'operation':'migrate','entity_kind':'coord','entity_id':row['id']})
        source=(W/'staging/queue/r3/mcp_server.py').read_text(encoding='utf-8')
        self.assertNotIn('legacy_activity_migration',source)
