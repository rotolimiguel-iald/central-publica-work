"""Capture every adapter boundary and typed Jev state; all I/O is mocked."""
import json
from pathlib import Path
from contextlib import ExitStack
from unittest.mock import patch,MagicMock
from test_operational_memory import QueueMemoryTests
from iald_orchestrator import providers, nos_packet, operational_memory as om, jev_decisions, jev


class AllAdapterMemoryTests(QueueMemoryTests):
    def packet(self):
        task=self.direct('OBJETIVO_COMUM_7_EXECUTORES')
        projection=om.projection(self.runtime,task['memory_context_id'],task['prompt'],None)
        return task,projection,nos_packet.prepare_queue(task['prompt'],None,providers.SYSTEM,operational_projection=projection)
    def test_all_seven_adapters_receive_same_original_q_p(self):
        task,projection,packet=self.packet()
        for name in ('local','kimi','mimo','deepseek','gemini','codex','claude'):
            with self.subTest(provider=name),ExitStack() as stack:
                capture=[]
                def execute(prompt,**kwargs):capture.append(prompt);return {'text':'fixture result','usage':{}}
                if name in ('kimi','mimo','deepseek','gemini'):
                    module='antigravity' if name=='gemini' else name
                    stack.enter_context(patch('iald_orchestrator.'+module+'.connection_status',return_value='ready'))
                    stack.enter_context(patch('iald_orchestrator.'+module+'.execute',side_effect=execute))
                elif name=='local':
                    response=MagicMock();response.__enter__.return_value=response
                    response.read.return_value=json.dumps({'choices':[{'finish_reason':'stop','message':{'content':'fixture result'}}]}).encode()
                    def urlopen(request,**kwargs):capture.append(json.loads(request.data)['messages'][-1]['content']);return response
                    stack.enter_context(patch.object(providers.urllib.request,'urlopen',side_effect=urlopen))
                else:
                    stack.enter_context(patch.object(providers,'client_command',return_value=['fixture-client']))
                    process=MagicMock();process.returncode=0
                    def communicate(prompt,**kwargs):
                        capture.append(prompt);return json.dumps({'subtype':'success','result':'fixture result'}),''
                    process.communicate.side_effect=communicate
                    stack.enter_context(patch.object(providers.subprocess,'Popen',return_value=process))
                    stack.enter_context(patch.object(providers,'_parse_codex',return_value={'text':'fixture result'}))
                result=providers.execute(name,task['prompt'],Path(self.temp.name),memory_packet=packet)
                self.assertEqual(len(capture),1)
                self.assertIn(task['prompt'],capture[0]);self.assertIn('"flow"',capture[0]);self.assertIn('"records"',capture[0])
                self.assertEqual(result['canonical_memory']['operational_memory']['context_id'],task['memory_context_id'])
    def test_typed_jev_body_contains_same_controller_state(self):
        task,projection,_=self.packet();root=Path(self.temp.name)/'jev';root.mkdir()
        policy=root/'policy.json';policy.write_text(json.dumps({'phase':'SHADOW','shadow_minimum_manager_accepted':True,
            'queue_shadow_enabled':True,'max_packet_chars':24000,'daily_call_limit':3}))
        doc='SAFE SCIENTIFIC FIXTURE'
        packet={'prompt':doc,'receipt':{'schema':nos_packet.SCHEMA,'selection':'SCIENTIFIC_ALLOWLIST_REREAD_NO_LEGAL_CONTENT',
            'packet_sha256':om.digest(doc),'sources':[{'id':'test'}],'canonical_memory':{'generation':'fixture'},'unit':'F1.3','mode':'shadow'}}
        questions={'D1':{'type':'noul','instructions':'Observe only; no authorization.'}}
        data={'model':jev_decisions.MODEL,'answers':{'D1':{'type':'noul','noul':0.8}},'usage':{'input_tokens':100,'output_tokens':4}}
        response=MagicMock();response.__enter__.return_value=response;response.read.return_value=json.dumps(data).encode()
        captured=[]
        def urlopen(request,**kwargs):captured.append(json.loads(request.data));return response
        with patch.object(jev_decisions,'ROOT',root),patch.object(jev_decisions,'POLICY',policy),\
             patch.object(jev,'availability',return_value={'status':'ready'}),patch.object(jev,'_key',return_value='offline-fixture'),\
             patch.object(jev_decisions.urllib.request,'urlopen',side_effect=urlopen),\
             patch.object(jev_decisions,'_event',return_value={'status':'offline'}),patch.object(jev_decisions,'publish_calibration'):
            _,receipt=jev_decisions.ask('Scientific task',questions,packet,operational_projection=projection)
            jev_decisions.ask('Scientific task',questions,packet,operational_projection=projection)
        self.assertEqual(len(captured),1)
        state=captured[0]['state']['operational_memory']
        self.assertEqual(state['objective'],task['prompt']);self.assertEqual(state['context_id'],task['memory_context_id'])
        self.assertIn('flow',state);self.assertIn('records',state);self.assertFalse(receipt['authority_granted'])
    def test_free_route_rite_pauses_once_without_retry_loop(self):
        task=self.direct()
        with patch.object(providers,'require_local_available',side_effect=providers.ProviderPausedByRite('fixture rite')) as availability,\
             patch.object(providers,'execute') as execute:
            self.runtime._drain();self.runtime._drain()
        self.assertEqual(availability.call_count,1);execute.assert_not_called()
        self.assertEqual(self.runtime.task(task['id'])['status'],'paused_by_rite')
    def test_restart_immediately_updates_shared_flow(self):
        task=self.direct();from iald_orchestrator.runtime import Runtime
        other=Runtime(self.temp.name,recover=True)
        state=om.store(other).get(task['memory_context_id'],om.SCOPE)
        self.assertEqual(state['p']['phase'],'interrupted')
        self.assertFalse(other.task(task['id'])['memory_checkpoint_pending'])