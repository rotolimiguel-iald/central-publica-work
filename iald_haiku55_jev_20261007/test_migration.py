"""Offline regression at real adapter, authorization and memory boundaries."""
from pathlib import Path
from types import SimpleNamespace
import copy, hashlib, json, sys, tempfile, unittest
from unittest.mock import Mock, patch
W=Path(__file__).resolve().parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(W/'stage'),str(R),'C:/Users/rotol/AppData/Roaming/Python/Python314/site-packages']
from claude_profiles import HAIKU,LEGACY_HAIKU,SONNET,reasoning_parameters,context_budget
from claude_memory_package import load_package
from claude_context_snapshot import snapshot_from_manifest,CheckedAdapter,attach_openai_tools,HaikuUnavailable
from claude_profile_pipeline import profile_call
from claude_request_guard import MemoryMeasurement,guarded_call,ContextRejected
from claude_server_selection import selected_model,option_rows,config_for_model
from claude_route_bridge import RouteBridge
from claude_native_account import NativeAccount,usage_amount
import iald_motor_claude as adapter
import iald_kernel,iald_fontes_publicas,iald_core_indexado
import iald_task_policy as policy
import iald_jev_control as control
import iald_motores as motors

def definitions():
    return iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()

class Migration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package=load_package(W/'package',canonical_manifest=R/'iald_nucleo_fixo.json')
        cls.manifest=json.loads((W/'package/manifest.json').read_bytes())
        cls.snapshot=snapshot_from_manifest(cls.manifest,cls.package)
    def cfg(self):
        return SimpleNamespace(modelo=HAIKU.model,max_saida=16384,cache_ttl='5m',esforco_claude='medium')
    def payload(self):
        return {'model':HAIKU.model,'max_completion_tokens':16384,
            'messages':[{'role':'system','content':self.package.prefix},{'role':'user','content':'Explique a identidade e autoria da TGL.'}],
            'tools':definitions()}
    def test_complete_public_context_native_budget(self):
        self.assertEqual(self.package.measurement.model,HAIKU.model)
        self.assertGreater(self.package.measurement.permanent_tokens,500000)
        self.assertGreater(self.package.available_dynamic_tokens,300000)
        provenance=json.loads((W/'public_memory_provenance.json').read_bytes())
        self.assertFalse(provenance['private_atlas_included'])
        self.assertEqual(hashlib.sha256(self.package.prefix.encode()).hexdigest(),provenance['prefix_sha256'])
    def test_other_providers_keep_original_compact_bytes(self):
        legacy=load_package(R/'.iald_runtime/haiku',canonical_manifest=R/'iald_nucleo_fixo.json',expected_model=LEGACY_HAIKU.model)
        self.assertEqual(legacy.measurement.model,LEGACY_HAIKU.model)
        self.assertNotEqual(legacy.prefix,self.package.prefix)
        with self.assertRaises(ValueError):load_package(R/'.iald_runtime/haiku',canonical_manifest=R/'iald_nucleo_fixo.json')
    def test_counts_from_other_tokenizer_rejected(self):
        with self.assertRaises(ValueError):context_budget(HAIKU.model,counted_model=LEGACY_HAIKU.model,
            permanent_tokens=180001,request_input_tokens=182000,reserved_output_tokens=16384)
    def test_overflow_never_truncates_or_sends(self):
        wire=adapter.converter_pedido(self.cfg(),self.payload(),prefixo=self.package.prefix)
        wire.update(reasoning_parameters(HAIKU.model,16384))
        sent=Mock();before=copy.deepcopy(wire)
        with self.assertRaises(ContextRejected):guarded_call(wire,authorized_model=HAIKU.model,
            memory=self.package.measurement,count_request=lambda _:999000,send_request=sent)
        sent.assert_not_called();self.assertEqual(wire,before)
    def test_adaptive_and_sampling_migration(self):
        payload=self.payload();payload.update(temperature=.2,top_p=.1,top_k=2)
        sent=[];counted=[]
        response,decision=profile_call(requested_model=HAIKU.model,
            server_policy=dict(username='guest',account_approved=True,haiku_ready=True,sonnet_ready=False),
            cfg=self.cfg(),payload=payload,prefix=self.package.prefix,memory=self.package.measurement,
            converter=adapter.converter_pedido,count_request=lambda w:(counted.append(w) or 576000),
            send_request=lambda w:(sent.append(w) or 'sent'))
        self.assertEqual(sent,counted);self.assertTrue(decision['ready']);self.assertEqual(response,'sent')
        self.assertEqual(sent[0]['thinking'],{'type':'adaptive'})
        self.assertEqual(sent[0]['output_config'],{'effort':'medium'})
        self.assertFalse(set(sent[0])&{'temperature','top_p','top_k'})
    def test_manual_budget_not_sent_to_new_model(self):
        with self.assertRaises(ValueError):reasoning_parameters(HAIKU.model,16384,1024)
    def test_sonnet_restriction_and_legacy_selection(self):
        for user in ('guest','alanacaroline','liana'):
            model=selected_model({'modelo_claude':LEGACY_HAIKU.model},user,haiku_ready=True,sonnet_ready=True)
            self.assertEqual(model,HAIKU.model)
            self.assertEqual([r['modelo'] for r in option_rows({'admin':False},user,haiku_ready=True,sonnet_ready=True)],[HAIKU.model])
            with self.assertRaises(PermissionError):selected_model({'modelo_claude':SONNET.model},user,haiku_ready=True,sonnet_ready=True)
    def test_scoped_tools_pin_entire_schema(self):
        extra={'type':'function','function':{'name':'create_artifact','description':'Synthetic scope','parameters':{'type':'object','properties':{}}}}
        defs=definitions()+[extra];p=attach_openai_tools(self.payload()|{'tools':defs},defs)
        checked=CheckedAdapter(adapter,self.snapshot,trusted_openai_tools=defs)
        wire=checked.converter_pedido(self.cfg(),p,prefixo=self.package.prefix)
        self.assertEqual(wire['tools'][-1]['name'],'create_artifact')
        forged=copy.deepcopy(p);forged['tools'][-1]['function']['description']='Changed'
        with self.assertRaises(HaikuUnavailable):checked.converter_pedido(self.cfg(),forged,prefixo=self.package.prefix)
    def test_client_cannot_add_a_tool(self):
        p=self.payload();p['tools']=[*definitions(),{'function':{'name':'shell'}}]
        with self.assertRaises(HaikuUnavailable):attach_openai_tools(p,definitions())
        with self.assertRaises(HaikuUnavailable):CheckedAdapter(adapter,self.snapshot).converter_pedido(self.cfg(),p,prefixo=self.package.prefix)
    def test_thinking_binding_pins_system_during_loop(self):
        checked=CheckedAdapter(adapter,self.snapshot,trusted_openai_tools=definitions())
        p=self.payload();checked.converter_pedido(self.cfg(),p,prefixo=self.package.prefix)
        p['messages'][0]['content']+='\nChanged dynamic instruction'
        with self.assertRaises(HaikuUnavailable):checked.converter_pedido(self.cfg(),p,prefixo=self.package.prefix)
    def test_preflight_allows_host_moderation_before_first_generation(self):
        checked=CheckedAdapter(adapter,self.snapshot,trusted_openai_tools=definitions())
        p=self.payload()
        checked.converter_pedido(self.cfg(),p,prefixo=self.package.prefix,bind_context=False)
        p['messages'][0]['content']+='\n'+motors.INSTRUCAO_ACOLHIMENTO
        checked.converter_pedido(self.cfg(),p,prefixo=self.package.prefix)
        p['messages'][0]['content']+='\nChanged after generation'
        with self.assertRaises(HaikuUnavailable):
            checked.converter_pedido(self.cfg(),p,prefixo=self.package.prefix,bind_context=False)
    def test_native_counter_preserves_signed_tool_schema(self):
        from claude_native_counter import native_count_parameters
        wire=adapter.converter_pedido(self.cfg(),self.payload(),prefixo=self.package.prefix)
        before=copy.deepcopy(wire)
        counted=native_count_parameters(wire)
        self.assertEqual(counted['tools'],wire['tools'])
        self.assertEqual(wire,before)
    def test_whole_package_tamper_rejected(self):
        with tempfile.TemporaryDirectory(dir=W) as folder:
            root=Path(folder);(root/'manifest.json').write_bytes((W/'package/manifest.json').read_bytes())
            (root/'prefix.md').write_bytes(b'bad prefix')
            with self.assertRaises(ValueError):load_package(root,canonical_manifest=R/'iald_nucleo_fixo.json')
    def test_pricing_and_16k_reserved_output(self):
        rates=(.5,.05,2.5,.625)
        p,c,o,cost=usage_amount({'prompt_tokens':600000,'completion_tokens':2000,
            'prompt_tokens_details':{'cached_tokens':500000,'cache_write_tokens':50000}},rates)
        self.assertAlmostEqual(cost,.08625)
        class Budget:
            RESERVATION_MARGIN=1.15
            WindowError=ValueError
            BudgetError=ValueError
        guard=SimpleNamespace(check=lambda *_:None,reserve=Mock(return_value='hold'),settle=Mock())
        cfg=SimpleNamespace(janela=1000000,precos=lambda _:rates,cota_operador_usd=10,cota_usuario_usd=1,
            cota_global_usd=10,cota_global_gratuito_usd=5,somente_limite_global=True)
        acc=NativeAccount(motors=motors,budget=Budget,guard=guard,ledger=Mock(),cfg=cfg,user='luiz',
            admin=True,model=HAIKU.model,quota_key='fixture',plan='operador',prefix_tokens=573879,count_request=lambda _:600000)
        acc.iniciar_chamada({'max_completion_tokens':16384})
        self.assertEqual(acc.pending['output'],16384)
        self.assertAlmostEqual(acc.pending['cap'],.47221)
        acc.fechar();self.assertTrue(guard.settle.called)
    def test_task_eligibility_is_transport_based(self):
        for task in policy.TASKS:
            self.assertIn('claude-haiku',policy.eligible_managers(['claude-haiku','kimi','nativa'],task))
            if task!='conversation':self.assertNotIn('kimi',policy.eligible_managers(['claude-haiku','kimi'],task))
    def test_public_never_receives_operator_path(self):
        self.assertNotIn('operator_bench',control.questions(False)['work_path']['criteria'])
    def test_no_false_five_point_five_history_metrics(self):
        import sqlite3
        import iald_auto_router as router
        with tempfile.TemporaryDirectory(dir=W) as folder:
            path=Path(folder)/'.iald_runtime/app_evaluation/metrics.sqlite3';path.parent.mkdir(parents=True)
            with sqlite3.connect(path) as db:
                db.execute('CREATE TABLE turns (data TEXT)')
                for model in (LEGACY_HAIKU.model,HAIKU.model,SONNET.model):
                    db.execute('INSERT INTO turns VALUES (?)',(json.dumps(dict(status='completed',provider='claude',model=model,elapsed_seconds=1,calls=[])),))
            db.close()
            result=router.observations(['claude-haiku'],Path(folder))
            self.assertEqual(result['providers']['claude-haiku']['samples'],1)

if __name__=='__main__':unittest.main(verbosity=2)
