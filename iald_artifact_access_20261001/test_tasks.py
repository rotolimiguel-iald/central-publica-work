import sys,json,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
W=Path(__file__).resolve().parent
sys.path[:0]=[str(W/'stage'),r'C:\IALD\projetos_pyhton\IALD']
import iald_task_policy as policy
from iald_task_session import TaskSession
import iald_auto_router as router
from iald_task_bridge import SandboxAccount

class Tasks(unittest.TestCase):
    def session(self,tmp,delegate=None,authorize=lambda p:True,python=None,store=None):
        return TaskSession(tmp,'luiz',store or SimpleNamespace(create=lambda *a,**k:{'status':'generated'}),authorize,
            delegate or (lambda *a:{'status':'DRAFT_COMPLETED','text':'result'}),
            python or (lambda *a:{'status':'execution_observed'}), {'type':'function','function':{'name':'create_artifact'}})

    def artifact_store(self,body='draft',filename='draft.md'):
        path=Mock()
        path.read_text.return_value=body
        meta={'id':'12345678-1234-4234-8234-123456789abc','filename':filename,'mime':'text/markdown' if filename.endswith('.md') else 'application/octet-stream',
            'sha256':'0'*64,'bytes':len(body.encode()),'url':'https://demo.iald.ia.br/api/task-artifacts/12345678-1234-4234-8234-123456789abc',
            'owner_hash':'INTERNAL_OWNER','local_path':'INTERNAL_PATH'}
        store=Mock()
        store.resolve.return_value=(path,meta)
        store.issue_ticket.side_effect=lambda *a:'https://demo.iald.ia.br/task-download/12345678-1234-4234-8234-123456789abc/token-'+str(store.issue_ticket.call_count)
        store.resolve_ticket.return_value=(path,{**meta,'expires_at':'2026-10-01T00:15:00Z'})
        return store,path
    def test_no_family_pilot(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(PermissionError):TaskSession(tmp,'liana',None,None,None,None,None)
    def test_same_step_never_repeated_and_journal_has_no_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            calls=[];s=self.session(tmp,delegate=lambda *a:(calls.append(a) or {'text':'DRAFT_ONLY_SECRET','status':'DRAFT_COMPLETED'}))
            args={'objective':'PRIVATE_OBJECTIVE','role':'implement'}
            self.assertEqual(s.execute('delegate_task',args),s.execute('delegate_task',args))
            self.assertEqual(len(calls),1)
            for secret in ('PRIVATE_OBJECTIVE','DRAFT_ONLY_SECRET'):self.assertNotIn(secret,s.path.read_text())
    def test_uncertain_is_terminal_for_same_step(self):
        with tempfile.TemporaryDirectory() as tmp:
            calls=[]
            def fail(*args):calls.append(1);raise RuntimeError('SECRET_BODY')
            s=self.session(tmp,fail);args={'objective':'one','role':'implement'}
            a=s.execute('delegate_task',args);b=s.execute('delegate_task',args)
            self.assertEqual(len(calls),1);self.assertEqual(b['status'],'PREVIOUS_ATTEMPT_UNCERTAIN')
            self.assertNotIn('SECRET_BODY',json.dumps(a)+s.path.read_text())

    def test_uncertain_python_defaults_share_identity_in_both_orders(self):
        variants=[{'code':'print(42)'},{'code':'print(42)','data':{}}]
        for first,second in (variants,list(reversed(variants))):
            with self.subTest(first=first),tempfile.TemporaryDirectory() as tmp:
                executor=Mock(side_effect=TimeoutError('PRIVATE_REQUEST'))
                s=self.session(tmp,python=executor)
                original=json.dumps(first)
                self.assertEqual(s.execute('execute_python',first)['status'],'FAILED_OR_UNCERTAIN')
                self.assertEqual(s.execute('execute_python',second)['status'],'PREVIOUS_ATTEMPT_UNCERTAIN')
                executor.assert_called_once()
                self.assertEqual(executor.call_args.args[0],{'code':'print(42)','data':{}})
                self.assertEqual(json.dumps(first),original)
                self.assertEqual(len(s.steps),1)
                self.assertEqual(s.counts['execute_python'],1)
                self.assertNotIn('PRIVATE_REQUEST',s.path.read_text())

    def test_uncertain_context_defaults_share_identity_in_both_orders(self):
        variants=[{'objective':'draft','role':'analyze'},{'objective':'draft','role':'analyze','context':''}]
        for first,second in (variants,list(reversed(variants))):
            with self.subTest(first=first),tempfile.TemporaryDirectory() as tmp:
                delegate=Mock(side_effect=TimeoutError())
                s=self.session(tmp,delegate=delegate)
                self.assertEqual(s.execute('delegate_task',first)['status'],'FAILED_OR_UNCERTAIN')
                self.assertEqual(s.execute('delegate_task',second)['status'],'PREVIOUS_ATTEMPT_UNCERTAIN')
                delegate.assert_called_once()
                self.assertEqual(delegate.call_args.args[0]['context'],'')
                self.assertEqual(len(s.steps),1)
                self.assertEqual(s.counts['delegate_task'],1)

    def test_invalid_role_never_reaches_journal_or_delegate(self):
        with tempfile.TemporaryDirectory() as tmp:
            delegate=Mock(return_value={'status':'DRAFT_COMPLETED'})
            s=self.session(tmp,delegate=delegate)
            original=s.path.read_bytes()
            for role in ('invalid','IMPLEMENT','',None,False,{},[]):
                with self.subTest(role=role),patch.object(s,'_save') as save:
                    result=s.execute('delegate_task',{'objective':'draft','role':role})
                    self.assertEqual(result['status'],'INVALID_ARGUMENTS')
                    save.assert_not_called()
            self.assertEqual(s.execute('delegate_task',{'objective':'draft'})['status'],'INVALID_ARGUMENTS')
            self.assertFalse(s.steps)
            self.assertFalse(s.counts)
            delegate.assert_not_called()
            self.assertEqual(s.path.read_bytes(),original)

    def test_invalid_fields_do_not_consume_attempts(self):
        cases=[('execute_python',{'code':None}),('execute_python',{'code':'  '}),
            ('execute_python',{'code':'x','data':None}),('execute_python',{'code':'x','data':[]}),
            ('execute_python',{'code':'x','data':{'n':float('nan')}}),
            ('delegate_task',{'role':'analyze','objective':''}),
            ('delegate_task',{'role':'implement','objective':'x','context':None}),
            ('read_task_artifact',{'artifact_id':'x','offset':True}),
            ('read_task_artifact',{'artifact_id':'x','offset':-1}),
            ('read_task_artifact',{'artifact_id':'x','extra':0}),
            ('get_task_capabilities',{'extra':True})]
        with tempfile.TemporaryDirectory() as tmp:
            s=self.session(tmp)
            for name,args in cases:
                with self.subTest(name=name,args=args):
                    self.assertEqual(s.execute(name,args)['status'],'INVALID_ARGUMENTS')
            self.assertFalse(s.steps)
            self.assertFalse(s.counts)

    def test_canonical_snapshot_and_cached_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            executor=Mock(return_value={'status':'execution_observed'})
            s=self.session(tmp,python=executor)
            first=s.execute('execute_python',{'code':'x'})
            self.assertEqual(s.execute('execute_python',{'data':{},'code':'x'}),first)
            executor.assert_called_once()
        with tempfile.TemporaryDirectory() as tmp:
            def mutate(args,*rest):
                args['data']['changed']='executor mutation'
                raise TimeoutError()
            s=self.session(tmp,python=Mock(side_effect=mutate))
            args={'code':'x','data':{}}
            s.execute('execute_python',args)
            self.assertEqual(args,{'code':'x','data':{}})
            self.assertEqual(s.execute('execute_python',{'code':'x'})['status'],'PREVIOUS_ATTEMPT_UNCERTAIN')
            s.python.assert_called_once()

    def test_journal_records_sandbox_state_without_changing_result(self):
        cases=[({'success':False,'state':'execution_failed'},'execution_failed'),
            ({'success':True,'state':'execution_observed'},'execution_observed'),
            ({'status':'explicit_status','state':'other_state'},'explicit_status'),
            ({'success':False},'returned')]
        for result,expected in cases:
            with self.subTest(result=result),tempfile.TemporaryDirectory() as tmp:
                executor=Mock(return_value=result)
                s=self.session(tmp,python=executor)
                self.assertEqual(s.execute('execute_python',{'code':'x'}),result)
                self.assertEqual(next(iter(s.steps.values()))['result_status'],expected)
                journal=json.loads(s.path.read_text())
                self.assertEqual(next(iter(journal['steps'].values()))['result_status'],expected)
                executor.assert_called_once()

    def test_equivalent_request_blocked_while_first_is_running(self):
        import threading
        with tempfile.TemporaryDirectory() as tmp:
            started,release=threading.Event(),threading.Event()
            def execute(*args):
                started.set()
                if not release.wait(5):raise AssertionError('Test failed to release the worker')
                raise TimeoutError()
            executor=Mock(side_effect=execute)
            s=self.session(tmp,python=executor)
            worker=threading.Thread(target=lambda:s.execute('execute_python',{'code':'x'}))
            worker.start()
            try:
                self.assertTrue(started.wait(5))
                self.assertEqual(s.execute('execute_python',{'code':'x','data':{}})['status'],'PREVIOUS_ATTEMPT_UNCERTAIN')
            finally:
                release.set();worker.join(5)
            self.assertFalse(worker.is_alive())
            executor.assert_called_once()

    def test_read_pages_keep_metadata_and_next_offset_before_text(self):
        body='0123456789'*1000+'fim'
        with tempfile.TemporaryDirectory() as tmp:
            store,path=self.artifact_store(body)
            s=self.session(tmp,store=store)
            offset,parts=0,[]
            while True:
                result=s.execute('read_task_artifact',{'artifact_id':'12345678-1234-4234-8234-123456789abc','offset':offset})
                self.assertLessEqual(len(result['text']),3500)
                keys=list(result)
                self.assertLess(keys.index('metadata'),keys.index('text'))
                self.assertLess(keys.index('next_offset'),keys.index('text'))
                self.assertEqual(result['total_chars'],len(body))
                self.assertEqual(result['source_sha256'],'0'*64)
                self.assertEqual(result['metadata']['expires_at'],'2026-10-01T00:15:00Z')
                serialized=json.dumps(result,ensure_ascii=False)
                self.assertLess(len(serialized),6000)
                self.assertNotIn('INTERNAL_',serialized)
                parts.append(result['text'])
                offset=result['next_offset']
                if result['status']=='COMPLETE_RANGE':break
            self.assertEqual(''.join(parts),body)
            self.assertEqual(offset,len(body))
            self.assertEqual(store.issue_ticket.call_count,3)
            store.issue_ticket.assert_called_with('luiz','12345678-1234-4234-8234-123456789abc')
            store.resolve_ticket.assert_called_with('12345678-1234-4234-8234-123456789abc','token-3')
            path.read_text.assert_called_with(encoding='utf-8')

    def test_read_uses_character_offsets_and_empty_end_page(self):
        body='á🙂漢'*1200
        with tempfile.TemporaryDirectory() as tmp:
            store,_=self.artifact_store(body)
            s=self.session(tmp,store=store)
            first=s.execute('read_task_artifact',{'artifact_id':'12345678-1234-4234-8234-123456789abc'})
            self.assertEqual(first['text'],body[:3500])
            self.assertEqual(first['next_offset'],3500)
            last=s.execute('read_task_artifact',{'artifact_id':'12345678-1234-4234-8234-123456789abc','offset':3500})
            self.assertEqual(first['text']+last['text'],body)
            end=s.execute('read_task_artifact',{'artifact_id':'12345678-1234-4234-8234-123456789abc','offset':len(body)})
            self.assertEqual(end['text'],'')
            self.assertEqual(end['status'],'COMPLETE_RANGE')
            self.assertEqual(end['next_offset'],len(body))

    def test_successful_read_renews_ticket_on_equivalent_offset(self):
        with tempfile.TemporaryDirectory() as tmp:
            store,_=self.artifact_store()
            s=self.session(tmp,store=store)
            first=s.execute('read_task_artifact',{'artifact_id':'12345678-1234-4234-8234-123456789abc'})
            second=s.execute('read_task_artifact',{'artifact_id':'12345678-1234-4234-8234-123456789abc','offset':0})
            self.assertEqual(first['text'],second['text'])
            self.assertNotEqual(first['metadata']['mobile_url'],second['metadata']['mobile_url'])
            self.assertEqual(store.issue_ticket.call_count,2)
            self.assertEqual(len(s.steps),1)
            self.assertEqual(s.counts['read_task_artifact'],2)
            self.assertNotIn('token-',s.path.read_text())

    def test_binary_read_returns_metadata_and_renewed_links_without_content(self):
        for filename in ('book.xlsx','slides.pptx','picture.png','report.pdf'):
            with self.subTest(filename=filename),tempfile.TemporaryDirectory() as tmp:
                store,path=self.artifact_store(filename=filename)
                path.read_text.side_effect=AssertionError('Binary contents must not be read')
                s=self.session(tmp,store=store)
                result=s.execute('read_task_artifact',{'artifact_id':'12345678-1234-4234-8234-123456789abc'})
                self.assertEqual(result['status'],'METADATA_ONLY')
                self.assertEqual(result['metadata']['filename'],filename)
                self.assertIn('mobile_url',result['metadata'])
                self.assertIn('url',result['metadata'])
                self.assertIn('expires_at',result['metadata'])
                self.assertNotIn('text',result)
                self.assertIsNone(result['next_offset'])
                path.read_text.assert_not_called()
                store.issue_ticket.assert_called_once_with('luiz','12345678-1234-4234-8234-123456789abc')

    def test_failed_read_or_renewal_stays_uncertain_and_does_not_leak(self):
        with tempfile.TemporaryDirectory() as tmp:
            store,path=self.artifact_store()
            s=self.session(tmp,store=store)
            args={'artifact_id':'12345678-1234-4234-8234-123456789abc'}
            self.assertEqual(s.execute('read_task_artifact',args)['status'],'COMPLETE_RANGE')
            store.issue_ticket.side_effect=RuntimeError('PRIVATE_TOKEN')
            failed=s.execute('read_task_artifact',args)
            self.assertEqual(failed['status'],'FAILED_OR_UNCERTAIN')
            self.assertEqual(s.execute('read_task_artifact',{'artifact_id':'12345678-1234-4234-8234-123456789abc','offset':0})['status'],'PREVIOUS_ATTEMPT_UNCERTAIN')
            self.assertEqual(store.issue_ticket.call_count,2)
            self.assertNotIn('PRIVATE_TOKEN',json.dumps(failed)+s.path.read_text())
            path.read_text.assert_called_once()
        with tempfile.TemporaryDirectory() as tmp:
            store,path=self.artifact_store()
            store.resolve.side_effect=PermissionError('other owner')
            s=self.session(tmp,store=store)
            self.assertEqual(s.execute('read_task_artifact',{'artifact_id':'12345678-1234-4234-8234-123456789abc'})['status'],'FAILED_OR_UNCERTAIN')
            store.issue_ticket.assert_not_called()
            path.read_text.assert_not_called()
    def test_revocation_before_any_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            def auth(p):raise PermissionError()
            with patch('builtins.print'):
                s=self.session(tmp,authorize=auth)
                self.assertEqual(s.execute('execute_python',{'code':'print(42)'})['status'],'FAILED_OR_UNCERTAIN')
                self.assertFalse(s.steps)
    def test_tool_limits_are_visible(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=self.session(tmp)
            for i in range(3):self.assertEqual(s.execute('delegate_task',{'objective':str(i),'role':'implement'})['status'],'DRAFT_COMPLETED')
            self.assertEqual(s.execute('delegate_task',{'objective':'four','role':'implement'})['status'],'FAILED_OR_UNCERTAIN')
    def test_task_policy_and_transport_capabilities(self):
        for request,task in [('faça planilha xlsx','spreadsheet'),('crie apresentação','presentation'),('crie site','website'),('escreva código python','code'),('calcule a média','calculation')]:
            self.assertEqual(policy.classify(request),task)
            self.assertNotIn('kimi',policy.eligible_managers(['kimi','mimo'],task))
        self.assertIn('kimi',policy.eligible_managers(['kimi'],'conversation'))
        self.assertIn('preference',policy.executor_criteria(['claude-sonnet'],router.DESCRIPTIONS,'code')['claude-sonnet'])
    def test_worker_mode_keeps_text_worker_and_one_public_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            bodies=[]
            def post(*a,**k):
                bodies.append(k['json'])
                return SimpleNamespace(status_code=200,close=lambda:None,json=lambda:{'model':'jev-1.13.0','answers':{'executor':{'choice':'kimi','confidence':1.0,'probabilities':{'kimi':1.0}}},'usage':{'input_tokens':10}})
            backend=SimpleNamespace(availability=lambda:{'status':'ready'},validate_prompt=lambda *a,**k:None,_key=lambda:'UNIT_KEY',ENDPOINT='https://example.invalid')
            with patch.dict(sys.modules,{'requests':SimpleNamespace(post=post)}),patch.object(router,'backend',return_value=backend),patch.object(router,'memory_slice',return_value=('PUBLIC_MEMORY',{'release':'test'})):
                chosen,_=router.choose('Implemente Python',['kimi'],root=Path(tmp),post=post,validation_probe=True,worker=True)
            self.assertEqual(chosen,'kimi');self.assertEqual(bodies[0]['state']['canonical_memory'],'PUBLIC_MEMORY')
    def test_sandbox_reserves_existing_global_guard_and_keeps_unknown_cost(self):
        class Guard:
            def __init__(self):self.calls=[]
            def reserve(self,*args,**kw):self.calls.append(('reserve',args));return 'hold'
            def settle(self,*args,**kw):self.calls.append(('settle',args,kw))
        g=Guard();records=[]
        cfg=SimpleNamespace(modelo='claude-haiku',precos=lambda m:(1,.1,5,1.25),cota_global_usd=100,cota_operador_usd=1,somente_limite_global=True)
        a=SandboxAccount(g,cfg,'luiz',SimpleNamespace(registrar=lambda *a,**k:records.append(a)))
        a.before(180000,8192);self.assertEqual(g.calls[0][1][-2:],(100,100));a.close()
        self.assertEqual(g.calls[-1][1],('hold',));self.assertFalse(records)

if __name__=='__main__':unittest.main(verbosity=2)
