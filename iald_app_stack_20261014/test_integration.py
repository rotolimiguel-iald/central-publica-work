"""Offline production-loader checks for current scientific and ACOM contracts."""
from pathlib import Path
import ast, hashlib, json, sys, types, unittest, threading, time
from unittest.mock import patch
W=Path(__file__).resolve().parent; R=Path('C:/IALD/projetos_pyhton/IALD');S=W/'science/memory_stage'
sys.path[:0]=[str(W/'integration'),str(W/'routing/patched'),str(R)]
from claude_memory_package import load_package
from claude_profiles import HAIKU
from claude_context_snapshot import snapshot_from_manifest,attach_openai_tools,verify_native_tools
import iald_kernel,iald_fontes_publicas,iald_core_indexado,iald_motor_claude,iald_app_memory,iald_jev_control
import iald_app_providers as providers

class Integration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads((S/'manifest_staged.json').read_bytes())
        cls.identity=cls.manifest['active_cluster']['release_source_sha256']
        cls.full=load_package(W/'science/package',canonical_manifest=S/'manifest_staged.json',source_sha=cls.identity)
        cls.shared=load_package(W/'science/shared_count/package',canonical_manifest=S/'manifest_staged.json',source_sha=cls.identity)
    def test_full_current_and_reserve(self):
        self.assertIn('v392',self.full.prefix)
        self.assertGreater(self.full.available_dynamic_tokens,10000)
        self.assertGreater(self.full.measurement.permanent_tokens,600000)
    def test_shared_current_and_mother_intact(self):
        self.assertIn('v392',self.shared.prefix)
        for key in ('mother_instruction','operational_core'):
            text=Path(self.manifest[key]['path']).read_text(encoding='utf-8-sig')
            self.assertIn(text,self.shared.prefix); self.assertIn(text,self.full.prefix)
    def test_new_scientific_contract(self):
        c=json.loads((S/'jev_control_v392.json').read_bytes())
        iald_jev_control.validate_contract(c)
        self.assertEqual(c['source_sha256'],self.identity)
        self.assertEqual(c['release'],'v392')
    def test_acom_scoped_tool_loader(self):
        defs=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()+iald_app_memory.tool_definitions()
        cfg=types.SimpleNamespace(modelo=HAIKU.model,max_saida=HAIKU.default_output,cache_ttl='5m',esforco_claude='medium')
        wire=iald_motor_claude.converter_pedido(cfg,attach_openai_tools({'model':cfg.modelo,'max_completion_tokens':cfg.max_saida,'messages':[{'role':'system','content':self.full.prefix},{'role':'user','content':'.'}]},defs),prefixo=self.full.prefix)
        snap=snapshot_from_manifest(json.loads((W/'science/package/manifest.json').read_bytes()),self.full)
        self.assertEqual(verify_native_tools(wire,snap,trusted_tools=wire['tools']),self.full.tools_sha256)
        with self.assertRaises(ValueError): verify_native_tools(wire,snap)
        edited=json.loads(json.dumps(wire));edited['tools'][0]['description']='tampered'
        with self.assertRaises(ValueError): verify_native_tools(edited,snap,trusted_tools=wire['tools'])
    def test_shared_transport_bounds(self):
        messages=[{'role':'system','content':self.shared.prefix},{'role':'user','content':'Explique o Hamiltoniano da TGL v392.'}]
        defs=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()+iald_app_memory.tool_definitions()
        for name in providers.MODELS:
            spec=providers.MODELS[name]
            body={'model':spec['model'],'messages':messages,'max_tokens':spec['output']}
            if name!='kimi':body['tools']=defs
            reserve=spec['output'] if name=='kimi' else providers.output_budget(body,spec['output'])
            body['max_tokens']=reserve
            used=providers.check_window(body,reserve)
            self.assertLessEqual(used+reserve+4096,providers.WINDOW,name)
            self.assertGreaterEqual(reserve,16384)
        self.assertEqual(providers.MODELS['deepseek']['output'],393216)
    def test_output_budget_preserves_input_and_maximum(self):
        body={'messages':[{'role':'user','content':'small request'}]}
        before=json.dumps(body)
        self.assertEqual(providers.output_budget(body,393216),393216)
        body['messages'][0]['content']='x'*700000
        before=json.dumps(body)
        reserve=providers.output_budget(body,393216)
        self.assertGreater(reserve,16384);self.assertLess(reserve,393216)
        self.assertEqual(before,json.dumps(body))
        providers.check_window(dict(body,max_tokens=reserve),reserve)
        with self.assertRaises(ValueError):providers.output_budget({'messages':['x'*(providers.WINDOW-8192)]},393216)
    def test_actual_deepseek_wire_and_spending_use_fitted_reserve(self):
        record={'id':'offline','calls':[],'first_text_seconds':None};wire=[];reserved=[]
        spec=providers.MODELS['deepseek']
        class Response:
            status_code=200
            def close(self):pass
            def iter_lines(self,**kw):
                yield ('data: '+json.dumps({'model':spec['model'],'choices':[{'index':0,'delta':{'content':'OK'},'finish_reason':'stop'}],'usage':{'prompt_tokens':100,'completion_tokens':1,'total_tokens':101}})).encode()
                yield b'data: [DONE]'
        def post(*args,**kwargs):wire.append(kwargs['json']);return Response()
        account=types.SimpleNamespace(before=lambda p,b,n:reserved.append(b['max_tokens']),settle=lambda m:None)
        ev=providers.Evaluation(W/'validation/offline_unused')
        messages=[{'role':'system','content':'x'*700000},{'role':'user','content':'test'}]
        with patch.object(ev,'save'),patch.object(providers,'adapter',return_value=types.SimpleNamespace(load_key=lambda:'synthetic-test-only')),patch.object(providers.app_memory,'project_messages',side_effect=lambda m:m):
            ev._api('deepseek',messages,[],lambda *a:None,lambda *a:None,threading.Event(),[],record,time.monotonic(),post,spending=account)
        self.assertEqual(len(wire),1)
        self.assertEqual(wire[0]['messages'],messages)
        self.assertLess(wire[0]['max_tokens'],spec['output'])
        self.assertEqual(reserved,[wire[0]['max_tokens']])
        self.assertEqual(record['calls'][0]['output_reserved_tokens'],wire[0]['max_tokens'])
        providers.check_window(wire[0],wire[0]['max_tokens'])
    def test_excessive_history_fails_before_credentials_or_network(self):
        from unittest.mock import Mock
        key=Mock();post=Mock();ev=providers.Evaluation(W/'validation/offline_unused')
        messages=[{'role':'system','content':'x'*providers.WINDOW},{'role':'user','content':'test'}]
        with patch.object(ev,'save'),patch.object(providers,'adapter',return_value=types.SimpleNamespace(load_key=key)),patch.object(providers.app_memory,'project_messages',side_effect=lambda m:m):
            with self.assertRaises(ValueError):ev._api('deepseek',messages,[],lambda *a:None,lambda *a:None,threading.Event(),[],{'calls':[]},time.monotonic(),post)
        key.assert_not_called();post.assert_not_called()
    def test_only_expected_server_changes(self):
        before=ast.parse((R/'iald_web_server.py').read_bytes());after=ast.parse((W/'integration/iald_web_server.py').read_bytes())
        old={getattr(n,'name',str(i)):ast.dump(n,include_attributes=False) for i,n in enumerate(before.body)}
        new={getattr(n,'name',str(i)):ast.dump(n,include_attributes=False) for i,n in enumerate(after.body)}
        self.assertEqual(set(old),set(new))
        self.assertEqual({k for k in old if old[k]!=new[k]},{'_load_shared_science_package','_load_haiku_package','_chat_avaliacao'})

if __name__=='__main__': unittest.main(verbosity=2)
