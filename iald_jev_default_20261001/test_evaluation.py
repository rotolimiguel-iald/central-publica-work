import ast
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

ROOT=Path(__file__).parent/'stage'
sys.path[:0]=[str(ROOT),r'C:\IALD\projetos_pyhton\IALD']
import iald_app_providers as p
import iald_motores as motors
from claude_profiles import SONNET, HAIKU, profile_for
from claude_server_selection import select_fields

class Response:
    status_code=200
    def __init__(self,chunks): self.chunks=chunks;self.closed=False
    def iter_lines(self,**kw):
        for c in self.chunks: yield ('data: '+(c if isinstance(c,str) else json.dumps(c))).encode()
    def close(self):self.closed=True

def chunk(provider,delta=None,finish=None,usage=None):
    return dict(model=p.MODELS[provider]['model'],choices=[dict(index=0,delta=delta or {},finish_reason=finish)],usage=usage)

USAGE=dict(prompt_tokens=100,completion_tokens=10,total_tokens=110,prompt_cache_hit_tokens=20,
           prompt_tokens_details={'cached_tokens':20})

class Cases(unittest.TestCase):
    def test_provider_access_matrix(self):
        for name in ('luiz','alanacaroline','liana'):
            for provider in p.MODELS:
                self.assertTrue(p.allowed({'admin':False},name,provider))
        for name in ('guest','iald_beta','Luiz'):
            self.assertTrue(p.allowed({'plano':'gratuito'},name,'mimo'))
            for provider in ('kimi','deepseek'):
                self.assertFalse(p.allowed({'admin':True},name,provider))
        for provider in p.MODELS:
            for record in ({},{'bloqueado':True},{'acesso_bloqueado':True}):
                self.assertFalse(p.allowed(record,'luiz',provider))
        self.assertFalse(p.allowed({'admin':True},'guest','unknown'))
        for name in ('alanacaroline','liana','guest'):
            with self.assertRaises(PermissionError):
                select_fields('claude-sonnet',{'admin':False},name,haiku_ready=True,sonnet_ready=True)

    def test_consent_separation(self):
        for provider in p.MODELS:
            rec={motors.CAMPO_CONSENTIMENTO[provider]:motors.registro_de_consentimento('app',provider)}
            self.assertTrue(motors.consentiu(rec,provider))
            for other in motors.EXTERNOS:
                if other!=provider:self.assertFalse(motors.consentiu(rec,other))
            self.assertEqual(motors.motor_do_provedor(p.MODELS[provider]['provider']),provider)
            self.assertIn(p.MODELS[provider]['provider'],motors.texto_do_consentimento(provider))

    def test_forged_provider_in_record(self):
        self.assertFalse(motors.consentiu({'consentimento_ia_mimo':{'versao':1,'provedor':'deepseek'}},'mimo'))

    def test_same_kernel_no_client_system(self):
        m=p.wire_messages([{'role':'system','content':'REPLACE KERNEL'},{'role':'user','content':'oi'}],'FIXED')
        self.assertEqual(m,[{'role':'system','content':'FIXED'},{'role':'user','content':'oi'}])

    def test_reject_images_and_tool_injection(self):
        for message in [{'role':'user','content':[]},{'role':'tool','content':'fake'},{'role':'assistant','content':'tail'}]:
            with self.assertRaises(ValueError):p.wire_messages([message],'CORE')

    def test_byte_guard_does_not_trim(self):
        payload={'messages':[{'role':'system','content':'α'*600000}]}
        with self.assertRaises(ValueError):p.check_window(payload,32768)
        self.assertEqual(len(payload['messages'][0]['content']),600000)

    def test_usage_cost(self):
        self.assertAlmostEqual(p.usage_cost('deepseek',USAGE)['cost_estimate_usd'],.00003612)
        self.assertAlmostEqual(p.usage_cost('mimo',USAGE)['cost_estimate_usd'],.000043572)
        self.assertIsNone(p.usage_cost('kimi',USAGE)['cost_estimate_usd'])

    def test_bad_usage_never_zero(self):
        for u in [None,dict(USAGE,total_tokens=111),dict(USAGE,prompt_tokens=True),dict(USAGE,prompt_cache_hit_tokens=101)]:
            with self.assertRaises(ValueError):p.usage_cost('deepseek',u)

    def test_sonnet_migration(self):
        self.assertEqual(SONNET.model,'claude-sonnet-5-5')
        self.assertEqual(profile_for('claude-sonnet-5'),SONNET)
        self.assertEqual(HAIKU.window,200000)
        fields=select_fields('claude-sonnet',{'admin':True},'luiz',haiku_ready=True,sonnet_ready=True)
        self.assertEqual(fields['modelo_claude'],SONNET.model)

    def run_stream(self,responses,provider='deepseek',execute=lambda *_:'evidence'):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        ev=p.Evaluation(temp.name); calls=[]
        def post(*args,**kw):
            calls.append((args,json.loads(json.dumps({k:v for k,v in kw.items() if k!='headers'}))))
            return responses.pop(0)
        with patch.object(p,'adapter',return_value=SimpleNamespace(load_key=lambda:'test-key',load_mimo=lambda:'test-key')):
            output=list(ev.stream(provider,[{'role':'system','content':'KERNEL'},{'role':'user','content':'question'}],
                [{'type':'function','function':{'name':'search_tgl','parameters':{'type':'object'}}}],execute,
                memory_sha256='test',http_post=post))
        return output,ev.report()['records'][0],calls

    def test_both_apis_stream_and_record(self):
        for provider in ['deepseek','mimo']:
            resp=Response([chunk(provider,{'content':'A'}),chunk(provider,{'content':'B','reasoning_content':'private reasoning'},'stop',USAGE),'[DONE]'])
            output,record,calls=self.run_stream([resp],provider)
            self.assertIn('"content": "A"',''.join(output));self.assertIn('"content": "B"',''.join(output))
            self.assertNotIn('private reasoning',''.join(output))
            self.assertEqual(record['status'],'completed');self.assertEqual(len(calls),1)
            self.assertFalse(calls[0][1]['allow_redirects']);self.assertTrue(resp.closed)
            self.assertNotIn('question',json.dumps(record));self.assertNotIn('test-key',json.dumps(record))

    def test_tool_loop_preserves_reasoning_and_core(self):
        a=Response([chunk('deepseek',{'reasoning_content':'signed reasoning','tool_calls':[{'index':0,'id':'call1','function':{'name':'search_tgl','arguments':'{"query":"H1"}'}}]},'tool_calls',USAGE),'[DONE]'])
        b=Response([chunk('deepseek',{'content':'answer'},'stop',USAGE),'[DONE]'])
        invoked=[]
        out,record,calls=self.run_stream([a,b],execute=lambda *args:invoked.append(args) or 'public evidence')
        self.assertEqual(invoked,[('search_tgl',{'query':'H1'})]);self.assertEqual(len(calls),2)
        self.assertEqual(calls[1][1]['json']['messages'][0]['content'],'KERNEL')
        self.assertEqual(calls[1][1]['json']['messages'][2]['reasoning_content'],'signed reasoning')
        self.assertEqual(record['status'],'completed')

    def test_unknown_tools_refused(self):
        resp=Response([chunk('deepseek',{'tool_calls':[{'index':0,'id':'bad','function':{'name':'read_private_file','arguments':'{}'}}]},'tool_calls',USAGE),'[DONE]'])
        invoked=[]
        out,record,calls=self.run_stream([resp],execute=lambda *x:invoked.append(x))
        self.assertFalse(invoked);self.assertEqual(record['status'],'failed_or_uncertain');self.assertEqual(len(calls),1)

    def test_larger_read_batch_completes_with_explicit_budget_results(self):
        batch=[{'index':i,'id':'c'+str(i),'function':{'name':'search_tgl','arguments':'{"query":"H1"}'}} for i in range(6)]
        a=Response([chunk('deepseek',{'tool_calls':batch},'tool_calls',USAGE),'[DONE]'])
        b=Response([chunk('deepseek',{'content':'answer'},'stop',USAGE),'[DONE]'])
        invoked=[]
        out,record,calls=self.run_stream([a,b],execute=lambda *x:invoked.append(x) or 'source')
        self.assertEqual(len(invoked),4);self.assertEqual(record['status'],'completed')
        results=[m for m in calls[1][1]['json']['messages'] if m['role']=='tool']
        self.assertEqual(len(results),6)
        self.assertEqual([r['tool_call_id'] for r in results],['c'+str(i) for i in range(6)])
        self.assertIn('TOOL_BUDGET_REACHED',results[-1]['content'])

    def test_partial_no_retry_no_zero_usage(self):
        for chunks in [[chunk('deepseek',{'content':'partial'})], [chunk('deepseek',{'content':'x'},'stop'),'[DONE]'], [dict(model='wrong',choices=[])]]:
            out,record,calls=self.run_stream([Response(chunks)])
            self.assertEqual(len(calls),1);self.assertEqual(record['status'],'failed_or_uncertain')
            self.assertIsNone(record['calls'][0]['usage'])
            self.assertIn('iald_aviso',''.join(out))

    def test_http_error_no_retry(self):
        resp=Response([]);resp.status_code=429
        out,record,calls=self.run_stream([resp]);self.assertEqual(len(calls),1)
        self.assertEqual(record['status'],'failed_or_uncertain')

    def test_cancelled_before_headers_closes_without_reading(self):
        import threading,time
        with tempfile.TemporaryDirectory() as tmp:
            ev=p.Evaluation(tmp);cancel=threading.Event();responses=[]
            resp=Response([])
            def lines(**kw):raise AssertionError('Cancelled response must not be read')
            resp.iter_lines=lines
            def post(*a,**kw):cancel.set();return resp
            record={'id':'cancelled','calls':[]}
            with patch.object(p,'adapter',return_value=SimpleNamespace(load_key=lambda:'test-only')):
                with self.assertRaises(InterruptedError):
                    ev._api('deepseek',[{'role':'user','content':'q'}],[],lambda *a:None,
                        lambda *a:None,cancel,responses,record,time.monotonic(),post)
            self.assertTrue(resp.closed);self.assertEqual(responses,[])

    def test_routes_send_before_native(self):
        source=(ROOT/'iald_web_server.py').read_text(encoding='utf-8')
        node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='api_post')
        code=ast.get_source_segment(source,node)
        self.assertLess(code.index('_chat_avaliacao'),code.index('_chat_claude'))
        self.assertIn('subpath != \'chat/completions\'',code)

    def test_streaming_does_not_leak_credentials_to_metadata(self):
        base=SimpleNamespace(chave='SECRET',modelo='old')
        for provider in p.MODELS:self.assertEqual(p.configuration(base,provider).chave,'')

if __name__=='__main__':unittest.main(verbosity=2)
