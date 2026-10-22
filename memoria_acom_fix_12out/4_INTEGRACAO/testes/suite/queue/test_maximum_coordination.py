import json, tempfile, unittest, uuid
from pathlib import Path
from unittest.mock import patch
from iald_orchestrator import canonical_memory as memory
from iald_orchestrator.coordination import Coordination
from iald_orchestrator.runtime import Runtime

class MaximumCoordinationTests(unittest.TestCase):
    def test_long_persisted_request_is_readable_and_prepared_without_losing_memory(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); source=root/'um_absoluto_forma_canonica.md'
            source.write_text(('Scientific anchor and hypotheses. '*35+'\n\n')*20,encoding='utf-8')
            catalog=root/'catalog.json'
            catalog.write_text(json.dumps({'files':[{'source':str(source),'sha256':memory.digest(source.read_bytes())}]}))
            memory.build(root/'memory',catalog)
            runtime=Runtime(root/'runtime',recover=False); coordinator=Coordination(runtime)
            actual_prepare=memory.prepare
            def prepare(prompt,**kwargs):
                return actual_prepare(prompt,root/'memory',**kwargs)
            prompt=('Review Lean hypotheses. '+('x '*9344)).strip()
            for provider in ('kimi','mimo'):
                constraints=dict(mission_id='ORDEM_016',branch_id='recovery',lemma_id=provider,role='skeptic',required_provider=provider,max_calls=1)
                rid=str(uuid.uuid4())
                with patch.object(runtime,'source_status',return_value={'ok':True}),patch.object(runtime,'preview',return_value={'selected':provider}),patch.object(memory,'prepare',side_effect=prepare):
                    job=coordinator.create(prompt,rid,constraints)
                    packet=job['canonical_memory']
                    self.assertGreater(len(packet['prompt']),24000)
                    self.assertEqual(packet['receipt']['memory_mode'],'maximum')
                    from iald_orchestrator import operational_memory as om
                    body=om.typed_projection(job['operational_memory'])
                    self.assertEqual(body['objective'],prompt)
                    self.assertEqual(packet['prompt'].count(prompt),1)
                    om.verify_packet(packet)
                    same=coordinator.create(prompt,rid,constraints)
                    self.assertEqual(same['id'],job['id'])
                    ready=coordinator.act(job['id'],'prepare_without_work',{'reason':'assistance_not_needed'})
                    self.assertEqual(ready['stage'],'prompt_ready')
                    self.assertEqual(ready['prepared_prompt'],prompt)
                    self.assertEqual(ready['execution_constraints']['required_provider'],provider)
                    self.assertIsNone(ready['execution_task_id'])
            with runtime.db() as db:
                self.assertEqual(db.execute('SELECT count(*) FROM tasks').fetchone()[0],0)
