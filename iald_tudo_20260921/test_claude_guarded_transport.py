from types import SimpleNamespace
import hashlib,unittest
from unittest.mock import Mock
from test_claude_guard_real_converter import converter
from claude_profiles import HAIKU,SONNET
from claude_request_guard import MemoryMeasurement
from claude_guarded_transport import post_guarded

class TransportTests(unittest.TestCase):
    def setUp(self):
        self.prefix='fixture TGL'
        self.memory=MemoryMeasurement(HAIKU.model,hashlib.sha256(self.prefix.encode()).hexdigest(),183135)
        self.cfg=SimpleNamespace(modelo=SONNET.model,max_saida=4096,cache_ttl='5m',esforco_claude='high')
        self.payload={'model':HAIKU.model,'max_completion_tokens':4096,
          'messages':[{'role':'system','content':self.prefix},{'role':'user','content':'question'}]}
        self.client=Mock();self.manager=Mock();self.stream=SimpleNamespace(response=None)
        self.client.with_options.return_value=self.client;self.client.max_retries=0
        self.client.messages.stream.return_value=self.manager
        self.manager.__enter__=Mock(return_value=self.stream);self.manager.__exit__=Mock()
        self.flow=Mock();self.flow.linhas.return_value=iter(['fixture'])
        self.adapter=SimpleNamespace(converter_pedido=converter.converter_pedido,
            _leva_atlas_integral=lambda payload,prefix:False,_com_prazo=lambda client,timeout:client,
            cliente_para=Mock(return_value=self.client),_Fluxo=Mock(return_value=self.flow),
            _cabecalhos=lambda headers:{},RespostaClaude=lambda status,headers,**kwargs:(status,headers,kwargs),
            erro_openai=lambda status,kind,message:(status,kind,message),
            _resposta_de_excecao=lambda exc:(503,type(exc).__name__))
        self.policy=dict(username='testador',account_approved=True,haiku_ready=True,sonnet_ready=True)
    def call(self,**kwargs):
        args=dict(requested_model=HAIKU.model,server_policy=self.policy,prefix=self.prefix,
                  memory=self.memory,counter=lambda wire:184609)
        args.update(kwargs)
        return post_guarded(self.adapter,self.cfg,self.payload,**args)
    def test_stream_receives_exact_native_haiku_parameters_once(self):
        response,decision=self.call()
        self.assertEqual(response[0],200);self.assertTrue(decision['ready'])
        wire=self.client.messages.stream.call_args.kwargs
        self.assertEqual(wire['thinking'],{'type':'disabled'});self.assertNotIn('output_config',wire)
        self.client.messages.stream.assert_called_once()
        self.assertEqual(response[2]['fechar'],self.flow.cancelar)
    def test_public_sonnet_denied_before_client(self):
        response,_=self.call(requested_model=SONNET.model)
        self.assertEqual(response[0],403);self.adapter.cliente_para.assert_not_called()
    def test_overflow_does_not_open_stream(self):
        response,decision=self.call(counter=lambda wire:199000)
        self.assertEqual(response[0],400);self.assertFalse(decision['ready'])
        self.client.messages.stream.assert_not_called()
    def test_count_failure_does_not_open_stream(self):
        def fail(wire):raise RuntimeError('counter unavailable')
        response,_=self.call(counter=fail)
        self.assertEqual(response[0],503);self.client.messages.stream.assert_not_called()
    def test_sonnet_output_budget_not_inherited(self):
        self.payload['max_completion_tokens']=16000
        response,_=self.call()
        self.assertEqual(response[0],400);self.client.messages.stream.assert_not_called()
    def test_stream_setup_failure_closes_manager(self):
        self.adapter._Fluxo.side_effect=RuntimeError('setup failed')
        response,_=self.call()
        self.assertEqual(response[0],502);self.manager.__exit__.assert_called_once()
    def test_value_error_after_send_does_not_claim_no_generation(self):
        self.adapter._Fluxo.side_effect=ValueError('setup failed')
        response,_=self.call()
        self.assertEqual(response[0],502);self.manager.__exit__.assert_called_once()
    def test_retry_override_and_payload_mismatch(self):
        self.call();self.client.with_options.assert_called_once_with(max_retries=0)
        self.adapter.cliente_para.reset_mock()
        self.payload['model']=SONNET.model
        response,_=self.call()
        self.assertEqual(response[0],403);self.adapter.cliente_para.assert_not_called()
    def test_after_send_failure_cannot_release_real_spending_reservation(self):
        self.adapter.erro_openai=converter.erro_openai
        self.adapter._Fluxo.side_effect=ValueError('setup failed')
        response,decision=self.call()
        code=response.json()['error']['code']
        self.assertFalse(converter.recusa_sem_cobranca(response.status_code,code))
        self.assertTrue(decision['ready'])

if __name__=='__main__':unittest.main()
