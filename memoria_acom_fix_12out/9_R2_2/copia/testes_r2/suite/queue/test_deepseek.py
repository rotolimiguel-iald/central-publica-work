"""Paid integration boundaries, with every external call simulated."""
import copy
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch, MagicMock
from iald_orchestrator import deepseek as ds, providers, canonical_memory as memory
from iald_orchestrator import request_controls as controls
from iald_orchestrator.policy import route


def response():
    return {'model': ds.MODEL, 'choices': [{'finish_reason': 'stop', 'message': {'content': '42', 'reasoning_content': 'never retained'}}],
            'usage': {'prompt_tokens': 100, 'completion_tokens': 20, 'total_tokens': 120,
                      'prompt_cache_hit_tokens': 40, 'prompt_cache_miss_tokens': 60}}


class DeepSeekTests(unittest.TestCase):
    def test_usage_and_cost_preserve_cache_and_exclude_reasoning(self):
        result = ds.parse_response(response())
        self.assertEqual(result['cost_estimate_usd'], '0.00004224')
        self.assertNotIn('reasoning_content', json.dumps(result))
        self.assertNotIn('never retained', json.dumps(result))

    def test_incomplete_wrong_model_tools_and_bad_usage_rejected(self):
        variants=[]
        for key, value in [('model', 'other'), ('usage', None)]:
            data=response();data[key]=value;variants.append(data)
        data=response();data['choices'][0]['finish_reason']='length';variants.append(data)
        data=response();data['choices'][0]['message']['tool_calls']=[{}];variants.append(data)
        data=response();data['usage']['total_tokens']=121;variants.append(data)
        data=response();data['usage']['prompt_cache_hit_tokens']=101;variants.append(data)
        for data in variants:
            with self.assertRaises(RuntimeError): ds.parse_response(data)

    def test_payload_maximum_single_request_and_no_tools(self):
        opener=MagicMock();opener.open.return_value.__enter__.return_value.read.return_value=json.dumps(response()).encode()
        with patch.object(ds,'authorization',return_value={'enabled':True}), patch.object(ds,'load_key',return_value='fake-not-a-key'), patch.object(ds.urllib.request,'build_opener',return_value=opener):
            result=ds.execute('x'*50000)
        req=opener.open.call_args.args[0];body=json.loads(req.data)
        self.assertEqual(body['model'],'deepseek-flash')
        self.assertEqual(body['max_tokens'],393216)
        self.assertEqual(body['reasoning_effort'],'max')
        self.assertEqual(body['thinking'],{'type':'enabled'})
        self.assertNotIn('tools',body)
        self.assertFalse(req.has_header('Authorization'))
        opener.open.assert_called_once()
        self.assertEqual(result['text'],'42')

    def test_authorization_cancel_and_redirect_block_network(self):
        with patch.object(ds,'authorization',return_value={'enabled':False}),patch.object(ds,'load_key') as key:
            with self.assertRaises(RuntimeError): ds.execute('public')
            key.assert_not_called()
        cancelled=threading.Event();cancelled.set()
        with patch.object(ds,'authorization',return_value={'enabled':True}),patch.object(ds,'load_key') as key:
            with self.assertRaises(RuntimeError): ds.execute('public',cancel=cancelled)
            key.assert_not_called()
        with self.assertRaises(RuntimeError): ds.NoRedirect().redirect_request(None,None,302,'',{},'https://other.example')

    def test_uncertain_validation_not_repeated(self):
        with tempfile.TemporaryDirectory() as folder,patch.object(ds,'execute') as execute:
            path=Path(folder)/'receipt.json';path.write_text('{"status":"validating"}')
            with patch.object(ds,'RECEIPT',path):
                with self.assertRaises(RuntimeError): ds.validate_connection()
            execute.assert_not_called()

    def test_medium_routing_excludes_unbenchmarked_high_complexity(self):
        p={'id':'deepseek','status':'ready','tier':'standard','billing':'authorized_api','billing_authorized':True,'daily_run_limit':None,'context_budget':ds.CONTEXT_WINDOW,'output_token_budget':ds.MAX_OUTPUT}
        self.assertEqual(route('Organize estes tópicos',[p],{})['selected'],'deepseek')
        self.assertIsNone(route('Demonstre este teorema',[p],{})['selected'])
        p['billing_authorized']=False
        self.assertIsNone(route('Organize estes tópicos',[p],{})['selected'])

    def test_common_memory_fits_real_output_reserve_and_provider_lock(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);source=root/'um_absoluto_forma_canonica.md'
            source.write_text(('TGL hypotheses and source facts. '*100+'\n\n')*400)
            catalog=root/'catalog.json';catalog.write_text(json.dumps({'files':[{'source':str(source),'sha256':memory.digest(source.read_bytes())}]}))
            memory.build(root/'memory',catalog)
            packet=memory.prepare('Organize os conceitos',root/'memory',mode=memory.mode_for_provider('deepseek'))
            self.assertGreater(packet['receipt']['context_bytes'],50000)
            self.assertLess(packet['receipt']['context_bytes'],ds.MAX_INPUT_BYTES)
            c=dict(mission_id='ORDEM_016',branch_id='test',lemma_id='deepseek',role='draft',required_provider='deepseek',max_calls=1)
            with patch.object(ds,'connection_status',return_value='ready'),patch.object(ds,'execute',return_value={'text':'ok','usage':{}}) as execute:
                result=providers.execute('deepseek','Organize os conceitos',root,memory_packet=packet,execution_constraints=c)
                self.assertIn(packet['prompt'],execute.call_args.args[0])
                self.assertEqual(result['canonical_memory'],packet['receipt'])
                with self.assertRaises(ValueError): providers.execute('kimi','Organize os conceitos',root,memory_packet=packet,execution_constraints=c)
                execute.assert_called_once()

    def test_web_key_requires_admin_origin_and_explicit_consent(self):
        from flask import Flask, jsonify
        from iald_orchestrator.web import install
        from iald_orchestrator.runtime import Runtime
        with tempfile.TemporaryDirectory() as folder:
            app=Flask(__name__);allowed=[False]
            def guard():
                return None if allowed[0] else (jsonify(error='login'),401)
            with patch('iald_orchestrator.web.Runtime',return_value=Runtime(folder,recover=False)):
                install(app,guard)
            client=app.test_client();url='/admin/api/orchestrator/connections/deepseek/key'
            body={'key':'fake-secret','authorize_paid_tasks':True}
            self.assertEqual(client.post(url,json=body).status_code,401)
            allowed[0]=True
            self.assertEqual(client.post(url,json=body,headers={'Origin':'https://other.example'}).status_code,403)
            headers={'Origin':'http://localhost'}
            with patch('iald_orchestrator.deepseek_secret_store.store_key') as store,patch('iald_orchestrator.safe_files.save_json') as save:
                self.assertEqual(client.post(url,json={'key':'fake-secret'},headers=headers).status_code,400)
                store.assert_not_called()
                self.assertEqual(client.post(url,json=body,headers=headers).status_code,200)
                self.assertTrue(save.call_args.args[1]['enabled'])


if __name__=='__main__': unittest.main()
