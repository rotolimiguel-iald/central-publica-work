import concurrent.futures
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import threading
import time
import unittest
from types import SimpleNamespace

STAGE=Path(__file__).parent/'stage'
sys.path.insert(0,str(STAGE))
sys.path.insert(1,r'C:\IALD\projetos_pyhton\IALD')
import iald_operator_bench as api
from iald_research_routes import Routes

class Store:
    def __init__(self):self.values=[]
    def ingest(self,owner,name,raw):
        self.values.append((owner,name,json.loads(raw)))
        return {'id':'artifact','filename':name,'bytes':len(raw),'sha256':'test','app_url':'https://example.invalid/artifact','mobile_url':'SECRET'}

class Catalog:
    def __init__(self):self.generation=1;self.calls=0;self.failure=False;self.block=None
    def catalog(self,section):return {'section':section}
    def normalize(self,operation,parameters):
        if operation not in ('calculate','status') or set(parameters)-{'x'}:raise ValueError()
        value=parameters.get('x',1)
        if type(value) not in (int,float) or not 0<=value<100:raise ValueError()
        return {'x':float(value)}
    def writes(self,operation):return operation=='calculate'
    def provenance(self,operation,parameters):return {'source_generation':self.generation}
    def request(self,operation,parameters):
        self.calls+=1
        if self.block:self.block.wait(2)
        if self.failure:raise TimeoutError('Secret from transport')
        return {'status':'ok','value':parameters['x']*2}

class BenchTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.record={'admin':True,'classe_usuario':'operador'}
        self.cat=Catalog();self.store=Store()
        self.api=api.OperatorBench(self.root,'luiz',lambda _:self.record,self.store,self.cat,self.root/'bench')
    def tearDown(self):
        with api._LOCK:active=api._ACTIVE.get(self.api.key)
        if active:active[1].result(timeout=4)
        self.temp.cleanup()
    def plan(self,**changes):
        args=dict(operation='calculate',parameters={},objective='Test',hypothesis='Twice input',falsifier='Result differs')
        args.update(changes)
        return self.api.execute('bench_plan',args)
    def finish(self,identifier):return self.api.execute('bench_result',{'route_id':identifier,'wait_seconds':3})
    def test_exact_role_not_inherited_from_admin_or_billing(self):
        for user,record in [('luiz',{'admin':True}),('other',self.record),('luiz',{'admin':1,'classe_usuario':'operador'}),('luiz',dict(self.record,bloqueado=True))]:
            self.assertFalse(api.is_operator(record,user))
        self.assertTrue(api.is_operator(self.record,'luiz'))
    def test_public_attach_no_storage_or_catalog(self):
        scope=SimpleNamespace(tools=[],store=self.store)
        self.assertIs(api.attach(scope,self.root,'other',lambda _:{'admin':True}),scope)
        self.assertFalse((self.root/'.iald_runtime').exists())
    def test_plan_requires_role_without_any_io(self):
        self.record={}
        self.assertEqual(self.plan()['status'],'FORBIDDEN')
        self.assertFalse((self.root/'.iald_runtime').exists())
    def test_semantic_duplicate_and_description_dont_repeat(self):
        first=self.plan();second=self.plan(parameters={'x':1.0},objective='Different wording')
        self.assertEqual(first['route_id'],second['route_id'])
        identifier=first['route_id']
        self.api.execute('bench_run',{'route_id':identifier});self.assertEqual(self.finish(identifier)['status'],'COMPLETED')
        self.api.execute('bench_run',{'route_id':identifier});self.assertEqual(self.cat.calls,1)
        self.assertEqual(self.store.values[0][0],'luiz')
        self.assertNotIn('mobile_url',self.finish(identifier)['artifact'])
    def test_concurrent_same_route_dispatches_once(self):
        identifier=self.plan()['route_id']
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            list(pool.map(lambda _:self.api.execute('bench_run',{'route_id':identifier}),range(10)))
        self.finish(identifier);self.assertEqual(self.cat.calls,1)
    def test_changed_source_blocks_without_network(self):
        identifier=self.plan()['route_id'];self.cat.generation=2
        self.assertEqual(self.api.execute('bench_run',{'route_id':identifier})['status'],'STALE_PLAN')
        self.assertEqual(self.cat.calls,0)
    def test_revocation_between_plan_and_run(self):
        identifier=self.plan()['route_id'];self.record['classe_usuario']='comum'
        self.assertEqual(self.api.execute('bench_run',{'route_id':identifier})['status'],'FORBIDDEN')
        self.assertEqual(self.cat.calls,0)
    def test_uncertain_never_resent_even_new_session(self):
        self.cat.failure=True;identifier=self.plan()['route_id']
        self.api.execute('bench_run',{'route_id':identifier})
        self.assertEqual(self.finish(identifier)['status'],'UNCERTAIN')
        other=api.OperatorBench(self.root,'luiz',lambda _:self.record,self.store,self.cat,self.root/'bench')
        other.execute('bench_run',{'route_id':identifier})
        self.assertEqual(self.cat.calls,1)
        self.assertNotIn('Secret',json.dumps(other.execute('bench_result',{'route_id':identifier})))
    def test_crash_claim_never_resent(self):
        identifier=self.plan()['route_id'];self.api.ledger().claim(identifier)
        result=self.api.execute('bench_run',{'route_id':identifier})
        self.assertEqual(result['status'],'UNCERTAIN');self.assertEqual(self.cat.calls,0)
    def test_restart_with_unresolved_old_route_blocks_new_dispatch(self):
        first=self.plan()['route_id'];self.api.ledger().claim(first)
        second=self.plan(parameters={'x':2})['route_id']
        self.assertEqual(self.api.execute('bench_run',{'route_id':second})['status'],'BENCH_REFUSED')
        self.assertEqual(self.cat.calls,0)
    def test_source_changed_during_execution_retains_evidence(self):
        old=self.cat.request
        def changed(*args):
            result=old(*args);self.cat.generation+=1;return result
        self.cat.request=changed
        identifier=self.plan()['route_id'];self.api.execute('bench_run',{'route_id':identifier})
        result=self.finish(identifier)
        self.assertEqual(result['status'],'RESULT_SOURCE_CHANGED')
        self.assertEqual(json.loads(result['text'])['value'],2)
        self.api.execute('bench_run',{'route_id':identifier});self.assertEqual(self.cat.calls,1)
    def test_write_cannot_hide_as_query(self):
        result=self.api.execute('bench_query',{'operation':'calculate','parameters':{}})
        self.assertEqual(result['status'],'BENCH_REFUSED');self.assertEqual(self.cat.calls,0)
    def test_extra_fields_and_nonfinite_rejected(self):
        self.assertEqual(self.plan(user='luiz')['status'],'BENCH_REFUSED')
        self.assertEqual(self.plan(parameters={'x':float('nan')})['status'],'BENCH_REFUSED')
    def test_ledger_append_only(self):
        identifier=self.plan()['route_id'];ledger=self.api.ledger()
        with self.assertRaises(sqlite3.IntegrityError):
            with ledger.db() as db:db.execute('DELETE FROM routes')
        self.assertEqual(ledger.get(identifier)['state'],'PLANNED')
    def test_history_import_is_idempotent_and_original_unchanged(self):
        state=self.root/'bench/state';state.mkdir(parents=True)
        path=state/'runs.sqlite3'
        with closing(sqlite3.connect(path)) as db:
            db.execute('CREATE TABLE runs(id INTEGER PRIMARY KEY,operation TEXT,parameters_json TEXT)')
            db.execute('CREATE TABLE inquiries(id INTEGER PRIMARY KEY,question TEXT)')
            db.execute('INSERT INTO runs VALUES(1,?,?)',('dephasing','{"x":1}'))
            db.commit()
        before=path.read_bytes();ledger=self.api.ledger()
        self.assertEqual(ledger.import_history(self.root/'bench')['inserted'],1)
        self.assertEqual(ledger.import_history(self.root/'bench')['inserted'],0)
        self.assertEqual(path.read_bytes(),before)
        self.assertEqual(ledger.search('dephasing')['counts']['legacy'],1)

if __name__=='__main__':unittest.main()
