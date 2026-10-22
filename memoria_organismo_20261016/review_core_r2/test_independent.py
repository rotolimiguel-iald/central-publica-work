import copy,json,hashlib
from pathlib import Path
import unittest
from test_projection import ProjectionTests
from iald_memory.activity import ActivityRuntime,ActivityError,KEY
from iald_memory.mission import digest,MissionError

class IndependentTests(ProjectionTests):
    # Runner selects only independent_* here; inherited builder tests run once.
    def independent_semantic_record_with_activity_metadata_never_hidden(self):
        self.finish();s=self.snap()
        r={'id':'operator-side-condition','kind':'fact','statute':'REAL','text':'Keep the substantive side condition intact.',
           'sources':[{'kind':'tool','ref':'fixture'}],
           'meta':{KEY:{'kind':'request','data':{'request_id':'r1'}},'semantic_note':'must retain'}}
        self.store.transition('conversation-a',self.scope,s['revision'],'semantic-extra',self.actor,{'records':[r]})
        p=self.rt.project(125000)
        self.assertEqual(p['indexed_record_ids'],[])
        self.assertIn(r['text'],p['text']);self.assertIn(r['id'],p['required_record_ids'])

    def independent_intent_pin_missing_fails_visibly(self):
        self.finish();record=next(r for r in self.snap()['q']['records'] if r.get('meta',{}).get(KEY,{}).get('kind')=='intent')
        Path(record['sources'][0]['ref']).unlink()
        with self.assertRaises(ActivityError):self.rt.project(125000)

    def independent_terminal_failure_not_completed_execution(self):
        self.finish();self.alter_handle(status='failed')
        p=self.rt.project(125000)
        self.assertEqual(p['indexed_record_ids'],[])
        self.assertIn('activity_op_',p['text'])
        self.assertFalse(p['activity']['tetelestai'])

    def independent_null_state_field_keeps_full(self):
        self.finish();self.alter_handle(phase=None)
        p=self.rt.project(125000)
        self.assertEqual(p['indexed_record_ids'],[])
        self.assertTrue(p['activity']['unresolved_handles'])

    def independent_multi_operation_exact_recovery(self):
        t=self.start();p=self.rt.preflight(t,'route')
        mid=self.rt.complete(p['ticket'],'route',{'route':'fixture'},terminal=False)
        p=self.rt.preflight(mid['ticket'],'answer');self.rt.complete(p['ticket'],'answer',{'body':'candidate'})
        before=self.snap();out=self.rt.project(125000);row=out['terminal_execution_index']['rows'][0]
        recovered=self.rt.recover('r1')
        selected=sorted([r for r in recovered['records'] if r['meta'][KEY]['kind'] in ('request','intent')],key=lambda r:r['id'])
        self.assertEqual(row[1],['answer','route']);self.assertEqual(row[2],digest(selected))
        self.assertEqual(row[3],digest(sorted(recovered['handles'],key=lambda h:h['id'])))
        self.assertEqual(len(out['indexed_record_ids']),3);self.assertEqual(before,self.snap())

    def independent_review_pin_mutation_refuses_settled_projection(self):
        t=self.finish();review=self.root/'review.json';review.write_bytes(b'fixture evidence')
        p=self.rt.controller.project(125000)
        self.rt.controller.action({'operation':'accept','actor':{'kind':'agent','id':'independent-fixture'},
            'task_id':t['task_id'],'event_id':'review','expected_revision':p['receipt']['revision'],
            'projection_sha256':p['projection_sha256'],'note':'Only this exact test scope.',
            'review_evidence':[{'path':str(review),'sha256':hashlib.sha256(review.read_bytes()).hexdigest()}]})
        good=self.rt.project(125000);self.assertIn('Only this exact test scope.',good['text'])
        review.write_bytes(b'changed')
        with self.assertRaises(MissionError):self.rt.project(125000)

    def independent_foreign_context_record_refused(self):
        self.finish();scope={'house':'IALD_APP','principal':'foreign-fixture'}
        self.store.ensure_context('foreign',objective='Foreign command',scope=scope,actor={'kind':'operator','id':'fixture'})
        other=ActivityRuntime(self.store,'foreign',scope,self.actor)
        other.begin('foreign-request','Foreign command',origin='authenticated_operator')
        foreign=next(r for r in other._get()['q']['records'] if r.get('meta',{}).get(KEY,{}).get('kind')=='request')
        s=self.snap();self.store.transition('conversation-a',self.scope,s['revision'],'cross-scope-record',self.actor,{'records':[foreign]})
        with self.assertRaises(ActivityError):self.rt.project(125000)

    def independent_index_does_not_make_old_ticket_dispatchable(self):
        t=self.finish();p=self.rt.project(125000)
        self.assertEqual(len(p['indexed_record_ids']),2)
        with self.assertRaises((ActivityError,MissionError)):self.rt.preflight(t,'new-effect',refresh=True)
        self.assertFalse(p['activity']['tetelestai'])
