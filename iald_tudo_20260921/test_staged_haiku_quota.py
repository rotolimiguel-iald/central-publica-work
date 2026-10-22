import ast,hashlib,json,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
from test_claude_guard_real_converter import converter
from claude_profiles import HAIKU
W=Path(__file__).resolve().parent
from haiku_stage_fixture import STAGE, definitions
from claude_context_snapshot import attach_openai_tools

class NativeQuotaTests(unittest.TestCase):
    def setUp(self):
        tree=ast.parse(STAGE.read_text(encoding='utf-8'))
        chat=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='_chat_externo')
        nodes=[n for n in ast.walk(chat)if isinstance(n,ast.FunctionDef)and n.name in ('tokens_para_saldo','prefixo_da_cota','count_haiku_wire')]
        self.assertEqual(len(nodes),3)
        self.counter=Mock(return_value=185000);client=Mock();client.with_options.return_value=client
        adapter=SimpleNamespace(converter_pedido=converter.converter_pedido,cliente_para=lambda cfg:client)
        self.env={'haiku':True,'claude':True,'estado_claude':converter.EstadoClaude(),
            'native_count_cache':{},'prompt_externo':'fixed kernel',
            'cfg':SimpleNamespace(modelo=HAIKU.model,max_saida=4096,cache_ttl='5m',esforco_claude='high'),
            'haiku_package':SimpleNamespace(measurement=SimpleNamespace(permanent_tokens=183135)),
            'iald_motor_claude':adapter,'haiku_adapter':adapter,'permitidas':definitions(),
            '_haiku_attach_tools':attach_openai_tools,'_count_haiku_native_request':self.counter,
            'iald_memoria_canonica':SimpleNamespace(MemoryUnavailable=ValueError),'hashlib':hashlib,'json':json}
        exec(compile(ast.Module(body=nodes,type_ignores=[]),str(STAGE),'exec'),self.env)
        self.payload={'model':HAIKU.model,'max_completion_tokens':4096,'messages':[
            {'role':'developer','content':'fixed kernel'},{'role':'user','content':'question'}]}
    def test_quota_counts_provider_tokens_and_exact_measured_baseline(self):
        n=self.env['tokens_para_saldo'](self.payload)
        baseline=self.env['prefixo_da_cota'](self.payload['messages'])
        self.assertEqual(n-baseline,1865)
        self.assertEqual(self.counter.call_args.args[1]['thinking'],{'type':'disabled'})
    def test_identical_request_reuses_count_but_history_change_recounts(self):
        self.env['tokens_para_saldo'](self.payload);self.env['tokens_para_saldo'](self.payload)
        self.assertEqual(self.counter.call_count,1)
        self.payload['messages'][-1]['content']='different'
        self.env['tokens_para_saldo'](self.payload);self.assertEqual(self.counter.call_count,2)
    def test_counter_failure_blocks_instead_of_estimate(self):
        self.counter.side_effect=RuntimeError('offline')
        with self.assertRaisesRegex(ValueError,'nenhuma geração'):
            self.env['tokens_para_saldo'](self.payload)
        self.assertEqual(self.env['native_count_cache'],{})

if __name__=='__main__':unittest.main()
