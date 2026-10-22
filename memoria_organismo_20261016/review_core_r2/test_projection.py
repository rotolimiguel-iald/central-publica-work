"""Exact terminal-receipt projection; all stores and review actors are fixtures."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import test_activity as original
from iald_memory import ProjectionOverflow
from iald_memory.activity import ActivityRuntime, ActivityError, KEY
from iald_memory.mission import digest, MissionError


class ProjectionTests(unittest.TestCase):
    setUp = original.ActivityTests.setUp
    start = original.ActivityTests.start
    snap = original.ActivityTests.snap
    append = original.ActivityTests.append

    def finish(self, request_id='r1', command='Preserve this literal instruction.'):
        t=self.start(request_id,command)
        p=self.rt.preflight(t,'provider')
        self.rt.complete(p['ticket'],'provider',{'answer':'Candidate, not approved.'})
        return t

    def wire(self,p):
        return json.loads(p['text'].split('<IALD_ACTIVITY_V1>\n')[1].split('\n</IALD_ACTIVITY_V1>')[0])

    def test_pending_semantics_does_not_prevent_terminal_receipt_index(self):
        t=self.finish();s=self.snap();p=self.rt.project(24000)
        ids=self.rt._ids('r1')
        self.assertEqual(len(p['indexed_record_ids']),2)
        self.assertEqual(p['activity']['active'][0]['status'],'review_pending')
        self.assertFalse(p['activity']['tetelestai'])
        self.assertIn(ids['steering'],p['required_record_ids'])
        self.assertIn('Preserve this literal instruction.',p['text'])
        self.assertIn(p['activity']['active'][0]['criterion'],p['text'])
        self.assertEqual(self.snap(),s)
        self.assertNotIn('flow',self.wire(p))
        self.assertEqual(self.wire(p)['terminal_handles'],[])

    def test_index_digest_recovers_exact_current_records_and_handles(self):
        self.finish();p=self.rt.project(24000);row=p['terminal_execution_index']['rows'][0]
        recovered=self.rt.recover(row[0])
        records=[r for r in recovered['records'] if r['meta'][KEY]['kind'] in {'request','intent'}]
        self.assertEqual(row[2],digest(sorted(records,key=lambda r:r['id'])))
        self.assertEqual(row[3],digest(sorted(recovered['handles'],key=lambda h:h['id'])))
        self.assertEqual(p['receipt'],recovered['receipt'])
        self.assertFalse(recovered['automatic_retry'])

    def test_restart_same_projection_no_dispatch(self):
        t=self.finish();old=self.rt.project(24000)
        self.rt=ActivityRuntime(self.store,'conversation-a',self.scope,self.actor)
        self.assertEqual(self.rt.project(24000),old)
        with self.assertRaises((ActivityError,MissionError)):
            self.rt.preflight(t,'provider',refresh=True)
        self.assertEqual(self.rt.recover('r1')['records'],
            [r for r in self.snap()['q']['records'] if r.get('meta',{}).get(KEY,{}).get('data',{}).get('request_id')=='r1'])

    def test_one_snapshot_even_with_terminal_index(self):
        self.finish()
        with patch.object(self.rt,'_get',wraps=self.rt._get) as getter:
            p=self.rt.project(24000)
        self.assertEqual(getter.call_count,1)
        self.assertEqual(p['receipt']['revision'],p['activity']['revision'])
        self.assertEqual(p['projection_sha256'],hashlib.sha256(p['text'].encode()).hexdigest())

    def test_general_facts_errata_and_pending_preserved(self):
        self.finish()
        for rid,kind,statute in [('science','fact','REAL'),('correction','erratum','INPUT'),('pending','pending','OPEN')]:
            self.append(rid,'Full literal '+rid,kind=kind,statute=statute)
        p=self.rt.project(24000)
        for rid in ('science','correction','pending'):
            self.assertIn(rid,p['required_record_ids']);self.assertIn('Full literal '+rid,p['text'])

    def test_artifact_tamper_visible(self):
        self.finish()
        record=self.rt._record(self.snap(),self.rt._ids('r1')['request'])
        Path(record['sources'][0]['ref']).write_bytes(b'changed')
        with self.assertRaisesRegex(ActivityError,'artifact_bytes_mismatch'):self.rt.project(24000)

    def test_admission_tamper_visible(self):
        self.finish()
        record=self.rt._record(self.snap(),self.rt._ids('r1')['request'])
        Path(record['meta'][KEY]['data']['source']['path']).write_bytes(b'changed admission')
        with self.assertRaises(MissionError):self.rt.project(24000)

    def test_result_custody_tamper_visible(self):
        self.finish()
        record=next(r for r in self.snap()['q']['records'] if r.get('meta',{}).get(KEY,{}).get('kind')=='result')
        Path(record['sources'][0]['ref']).write_bytes(b'changed return')
        with self.assertRaises(ActivityError):self.rt.project(24000)

    def alter_handle(self,**changes):
        s=self.snap();h=next(h for h in s['p']['handles'] if h['kind']=='activity_operation')
        self.store.transition('conversation-a',self.scope,s['revision'],'handle-change',self.actor,
            {'flow':{'handles':[dict(id=h['id'],**changes)]}})

    def test_unknown_handle_state_remains_full(self):
        self.finish();self.alter_handle(status='mysterious_state')
        p=self.rt.project(125000)
        self.assertEqual(p['indexed_record_ids'],[])
        self.assertIn('mysterious_state',p['text'])

    def test_contradictory_phase_remains_full(self):
        self.finish();self.alter_handle(phase='running')
        p=self.rt.project(125000)
        self.assertEqual(p['indexed_record_ids'],[])
        self.assertEqual(len(p['activity']['unresolved_handles']),1)

    def test_unknown_machine_record_remains_full(self):
        self.finish();s=self.snap()
        record=self.rt._metadata_record('future-receipt','future-schema',{'request_id':'r1','keep':'unknown required fact'})
        self.store.transition('conversation-a',self.scope,s['revision'],'unknown',self.actor,{'records':[record]})
        p=self.rt.project(125000)
        self.assertEqual(p['indexed_record_ids'],[])
        self.assertIn('future-receipt',p['required_record_ids'])

    def test_correction_lineage_of_machine_record_remains_full(self):
        self.finish();s=self.snap();request_id=self.rt._ids('r1')['request']
        record={'id':'correct-receipt','kind':'erratum','statute':'INPUT','text':'Keep correction literal.',
            'supersedes':request_id,'sources':[{'kind':'operator','ref':'private-test'}]}
        self.store.transition('conversation-a',self.scope,s['revision'],'correct',self.actor,{'records':[record]})
        p=self.rt.project(125000)
        self.assertEqual(p['indexed_record_ids'],[])
        self.assertIn(request_id,p['required_record_ids']);self.assertIn('correct-receipt',p['required_record_ids'])

    def test_uncertain_operation_keeps_full_state(self):
        t=self.start();p=self.rt.preflight(t,'provider');self.rt.mark_uncertain(p['ticket'],'provider','unknown external outcome')
        s=self.snap();out=self.rt.project(125000)
        self.assertEqual(out['indexed_record_ids'],[])
        self.assertIn('unknown external outcome',out['text']);self.assertEqual(self.snap(),s)

    def test_settled_compaction_preserves_literal_criterion(self):
        t=self.finish();file=self.root/'synthetic-review.json';file.write_bytes(b'{"fixture_review":true}')
        p=self.rt.controller.project(125000)
        self.rt.controller.action({'operation':'accept','actor':{'kind':'agent','id':'independent-fixture-reviewer'},
            'task_id':t['task_id'],'event_id':'fixture-accept','expected_revision':p['receipt']['revision'],
            'projection_sha256':p['projection_sha256'],'note':'Human fixture review: preserve this restriction.',
            'review_evidence':[{'path':str(file),'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}]})
        out=self.rt.project(24000);wire=self.wire(out)
        self.assertEqual(wire['settled'][0]['criterion'],out['activity']['settled'][0]['criterion'])
        self.assertEqual(wire['settled'][0]['reviewed_by'],'independent-fixture-reviewer')
        self.assertEqual(wire['settled'][0]['note'],'Human fixture review: preserve this restriction.')
        self.assertEqual(wire['settled'][0]['review_evidence'],out['activity']['settled'][0]['review_evidence'])
        self.assertEqual(wire['settled'][0]['evidence'],out['activity']['settled'][0]['evidence'])
        self.assertTrue(out['activity']['tetelestai'])

    def test_large_genuine_pending_refuses_without_mutation(self):
        self.finish();self.append('long-human-pending','Unresolved input. '*1500,kind='pending',statute='INPUT',source_kind='operator')
        before=self.snap()
        with self.assertRaises(ProjectionOverflow):self.rt.project(24000)
        self.assertEqual(before,self.snap())

    def test_unrelated_adapter_handle_is_retained(self):
        self.finish();s=self.snap()
        self.store.transition('conversation-a',self.scope,s['revision'],'adapter-handle',self.actor,
            {'flow':{'handles':[{'id':'app_request','kind':'app_request','request_id':'r1',
                'status':'unknown-adapter-state','note':'Do not hide adapter state'}]}})
        p=self.rt.project(24000)
        self.assertEqual(len(p['indexed_record_ids']),2)
        self.assertIn('Do not hide adapter state',p['text'])
        self.assertEqual(p['activity']['unresolved_handles'][0]['id'],'app_request')

    def test_ten_pending_conserves_all_semantic_records_and_criteria(self):
        for n in range(10):self.finish('turn'+str(n),'Keep literal command '+str(n))
        s=self.snap();p=self.rt.project(24000)
        body,_=json.JSONDecoder().raw_decode(p['text'][p['text'].index('{'):])
        self.assertEqual(len(p['activity']['active']),10)
        projected={r['id']:r for r in body['records']}
        for record in s['q']['records']:
            if record['kind']=='decision':
                self.assertEqual(projected[record['id']],record)
        self.assertEqual(len(p['indexed_record_ids']),20)
        for task in p['activity']['active']:
            self.assertEqual(task['status'],'review_pending')
            self.assertIn(task['criterion'],p['text'])
        self.assertEqual(s,self.snap())

    def test_overflow_reports_exact_combined_minimum(self):
        self.finish()
        with self.assertRaises(ProjectionOverflow) as caught:self.rt.project(256)
        p=self.rt.project(caught.exception.required_chars)
        self.assertEqual(p['required_chars'],caught.exception.required_chars)
        self.assertEqual(p['actual_chars'],p['required_chars'])


if __name__=='__main__':unittest.main(verbosity=2)
