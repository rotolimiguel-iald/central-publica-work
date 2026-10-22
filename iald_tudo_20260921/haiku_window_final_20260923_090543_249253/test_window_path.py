"""Offline real chat/agent/account/transport; synthetic prefix and provider counts."""
import ast
import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import offline_bootstrap
from offline_bootstrap import install, load_server
STAGED = '--staged' in sys.argv
if STAGED:
    sys.argv.remove('--staged')
    offline_bootstrap.SERVER_SOURCE = Path(__file__).with_name('iald_web_server.py')

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
install(str(ROOT))
sys.path.insert(0, str(ROOT))
import iald_motores as mt
import iald_motor_claude as mc
import iald_orcamento as budget
from claude_request_guard import MemoryMeasurement
from claude_context_snapshot import native_tools_sha256
from claude_native_account import NativeAccount

# Reuse only reviewed pure fake SDK definitions, never execute original test setup.
source = ROOT/'tests/test_claude_rotas.py'
names = {'Roteiro','StreamFalso','GerenteFalso','ClienteFalso','_ini','roteiro_texto','roteiro_ferramenta'}
tree = ast.parse(source.read_text(encoding='utf-8-sig'))
nodes = [n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in names]
USO = {'input_tokens':20,'cache_creation_input_tokens':183135,'cache_read_input_tokens':0,'output_tokens':40}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),globals())
with contextlib.redirect_stdout(io.StringIO()):
    ws = load_server()
if STAGED:
    import importlib.util
    spec = importlib.util.spec_from_file_location('candidate_account',Path(__file__).with_name('claude_native_account.py'))
    candidate_account = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(candidate_account)
    ws._HaikuNativeAccount = candidate_account.NativeAccount

EVIDENCE = []

class WindowPath(unittest.TestCase):
    def run_case(self, counts, *, tool=False, factor=1.6, history=''):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        folder = Path(tmp.name)
        cfg = mt.Config(chave='synthetic-not-a-credential', provedor='claude',
            modelo='claude-sonnet-5',modelo_operador='claude-sonnet-5',
            contas=frozenset({'luiz'}), janela=600000,fator_tokens=factor,
            cota_global_usd=15,cota_usuario_usd=15,cota_operador_usd=15,
            memoria_modo='prompt',sucessor_automatico=False)
        ws.MOTORES_CFG = mt.Config(memoria_modo='prompt')
        ws.CLAUDE_CFG = cfg
        definitions = ws._haiku_tool_definitions()
        # Deliberately huge synthetic prefix: generic character estimates cannot fit.
        prefix = 'SYNTHETIC PUBLIC FIXTURE; NOT MEASURED MEMORY. ' * 25000
        package = SimpleNamespace(prefix=prefix,
            measurement=MemoryMeasurement(ws._HAIKU_PROFILE.model,hashlib.sha256(prefix.encode()).hexdigest(),183135),
            available_dynamic_tokens=10271,reserved_output_tokens=4096,
            tools_sha256=native_tools_sha256(mc.converter_ferramentas(definitions)))
        ws.CLAUDE_ROUTES=ws.RouteBridge(motors=mt,base_config=cfg,
            package_loader=lambda:package,enabled=True,public_daily_usd=None,public_group_daily_usd=None)
        ws.RAZAO_CLAUDE=mt.RazaoDeUso(str(folder/'ledger.json'))
        ws.GUARDA_CLAUDE=None
        ws.LIMITE_CLAUDE=mt.JanelaDePedidos(1000,60)
        ws.MODERACAO_LIGADA=False
        ws._sdk_claude_presente=lambda:True
        ws._contabilizar_uso=lambda *args:None
        ws._executar_ferramenta_claude=lambda *args,**kwargs:json.dumps({'source_sha256':'a'*64,'total':100,'next_offset':100,
            'files':[{'path':f'TGLExt/Fixture{i}.lean','sha256':str(i).zfill(64)} for i in range(100)]})
        ws.MAX_AGENT_LOOPS=2
        client=ClienteFalso()
        client.max_retries=0
        measured=[]
        def count_tokens(**wire):
            n=counts(wire) if callable(counts) else counts[min(len(measured),len(counts)-1)]
            measured.append({'count':n,'model':wire['model'],'tools':len(wire.get('tools',[])),
                'tool_choice':wire.get('tool_choice'),
                'has_tool_result':any(b.get('type')=='tool_result' for m in wire['messages']
                    for b in m.get('content',[]) if isinstance(b,dict))})
            return SimpleNamespace(input_tokens=n)
        client.count_tokens=count_tokens
        client.roteiros=([roteiro_ferramenta('search_tgl',{'query':'synthetic'})] if tool else [])+[roteiro_texto('SYNTHETIC ANSWER')]
        mc.definir_sdk(SimpleNamespace(APIStatusError=type('SyntheticStatusError',(Exception,),{})))
        mc.definir_fabrica_cliente(lambda cfg:client)
        record={'admin':True,'motor':'claude','modelo_claude':ws._HAIKU_PROFILE.model,
                'consentimento_ia_anthropic':mt.registro_de_consentimento('web','claude')}
        messages=([{'role':'user','content':'old fixture'},{'role':'assistant','content':history}] if history else [])
        messages.append({'role':'user','content':'Articule a solução matemática da TGL.'})
        with patch.object(budget,'input_estimates',side_effect=AssertionError('legacy estimator reached')), \
             patch.object(budget.ReservedAccount,'iniciar_chamada',side_effect=AssertionError('legacy reserve reached')), \
             ws.app.test_request_context(headers={'X-IALD-Context':'anthropic-native-v1'}):
            response=ws._chat_externo({'messages':messages,'stream':True},'luiz',record,True,0,'claude')
            body=response.get_data(as_text=True)
        with ws.GUARDA_CLAUDE._connect() as db:
            reserves=db.execute('SELECT COUNT(*) FROM calls').fetchone()[0]
        result={'counts':measured,'sends':len(client.chamadas),'reserves':reserves,
                'generic_window_message':budget.MSG_JANELA in body,'answer':'SYNTHETIC ANSWER' in body,
                'factor':factor,'truthful_followup_message':'a próxima volta não foi enviada' in body,
                'sent_wires':client.chamadas}
        EVIDENCE.append({k:v for k,v in result.items() if k!='sent_wires'})
        return result

    def test_large_generic_estimate_never_used_native_184906_fits(self):
        result=self.run_case([184906],factor=99)
        self.assertTrue(result['answer'],result)
        self.assertEqual((result['sends'],result['reserves'],len(result['counts'])),(1,1,1))
        self.assertFalse(result['generic_window_message'])

    def test_exact_boundary_194880_fits(self):
        result=self.run_case([194880])
        self.assertTrue(result['answer'],result)

    def test_native_194881_reproduces_reported_error_before_send(self):
        result=self.run_case([194881],history='SYNTHETIC HISTORY '*3000)
        self.assertTrue(result['generic_window_message'] if not STAGED else not result['answer'],
                        {k:v for k,v in result.items() if k!='sent_wires'})
        self.assertEqual((result['sends'],result['reserves']),(0,0))

    def test_tool_result_overflow_occurs_after_first_real_path_send(self):
        result=self.run_case([184906,195000],tool=True)
        self.assertTrue(result['generic_window_message'] if not STAGED else not result['answer'],
                        {k:v for k,v in result.items() if k!='sent_wires'})
        self.assertEqual((result['sends'],result['reserves']),(1,1))
        self.assertLessEqual(len(result['counts']),7)
        self.assertTrue(result['counts'][1]['has_tool_result'])

class ToolRecovery(WindowPath):
    # Run only new regression(s); original boundary suite remains separate.
    test_large_generic_estimate_never_used_native_184906_fits = None
    test_exact_boundary_194880_fits = None
    test_native_194881_reproduces_reported_error_before_send = None
    test_tool_result_overflow_occurs_after_first_real_path_send = None

    def test_current_overflow_recovers_with_explicit_partial_results(self):
        def measured(wire):
            text=json.dumps(wire['messages'],ensure_ascii=False)
            if 'tool_result' not in text:return 184906
            # Synthetic provider-count fixture depends on whole result content.
            return 196000 if 'PARTIAL_TOOL_RESULT' not in text else 190000
        result=self.run_case(measured,tool=True)
        self.assertTrue(result['answer'],{k:v for k,v in result.items() if k!='sent_wires'})
        self.assertEqual((result['sends'],result['reserves']),(2,2))
        wire=result['sent_wires'][-1]
        self.assertEqual(wire['tool_choice'],{'type':'none'})
        self.assertEqual(len(wire['tools']),7)
        self.assertLessEqual(len(result['counts']),7)
        self.assertIn('PARTIAL_TOOL_RESULT',json.dumps(wire['messages']))
        self.assertEqual(wire['system'],result['sent_wires'][0]['system'])
        # Real EstadoClaude restores assistant signature and tool_use unchanged.
        blocks=wire['messages'][1]['content']
        self.assertEqual(blocks[0],{'type':'thinking','thinking':'PENSO','signature':'SIG'})
        self.assertEqual(blocks[1]['id'],'toolu_1')
        self.assertEqual(blocks[1]['input'],{'query':'synthetic'})

if __name__=='__main__':
    result=unittest.main(exit=False)
    Path(__file__).with_name('staged_path_evidence.json' if STAGED else 'current_path_evidence.json').write_text(json.dumps(EVIDENCE,ensure_ascii=False,indent=2),encoding='utf-8')
    raise SystemExit(not result.result.wasSuccessful())
