import copy
import json
import pathlib
import shutil
import subprocess
import tempfile
import threading
import unittest
from unittest.mock import patch
from iald_orchestrator import kimi, providers

MODEL = kimi.MODEL
EVIDENCE = [
    {'type':'profile.bind','profileName':'iald-text','modelAlias':MODEL,'activeToolNames':[],'subagents':[],'agentsMdPaths':[]},
    {'type':'llm.tools_snapshot','tools':[]},
    {'type':'llm.request','model':'k3','modelAlias':MODEL,'thinkingEffort':'max'},
    {'type':'usage.record','model':MODEL,'usageScope':'turn','usage':{'inputOther':30,'inputCacheRead':10,'inputCacheCreation':5,'output':7}},
    {'type':'context.append_loop_event','event':{'finishReason':'end_turn','rawFinishReason':'stop'}},
    {'type':'turn.ended','reason':'completed'},
]
EVENTS = [
    {'role':'meta','type':'system.version','version':'2.0.2'},
    {'role':'assistant','content':'def add(a, b): return a + b'},
    {'role':'meta','type':'session.resume_hint','session_id':'session_12345678-1234-1234-1234-123456789abc'},
]


class KimiTests(unittest.TestCase):
    def test_usage_includes_cached_and_reasoning_output(self):
        self.assertEqual(kimi.parse_evidence(EVIDENCE), {'prompt_tokens':45,'completion_tokens':7,'cached_input_tokens':10,'total_tokens':52})

    def test_incomplete_and_repeated_requests_fail(self):
        for records in (EVIDENCE[:-1], EVIDENCE+[EVIDENCE[2]]):
            with self.assertRaises(RuntimeError): kimi.parse_evidence(records)

    def test_tool_delegation_or_foreign_context_fail(self):
        for field in ('activeToolNames','subagents','agentsMdPaths'):
            records=copy.deepcopy(EVIDENCE); records[0][field]=['unexpected']
            with self.assertRaises(RuntimeError): kimi.parse_evidence(records)
        records=copy.deepcopy(EVIDENCE); records[1]['tools']=['Bash']
        with self.assertRaises(RuntimeError): kimi.parse_evidence(records)

    def test_wrong_model_truncation_and_bad_usage_fail(self):
        changes=[(2,'thinkingEffort','high'),(2,'model','other'),(3,'usageScope','other'),(5,'reason','failed')]
        for index,key,value in changes:
            records=copy.deepcopy(EVIDENCE); records[index][key]=value
            with self.assertRaises(RuntimeError): kimi.parse_evidence(records)
        records=copy.deepcopy(EVIDENCE); records[4]['event']['rawFinishReason']='length'
        with self.assertRaises(RuntimeError): kimi.parse_evidence(records)
        records=copy.deepcopy(EVIDENCE); records[3]['usage']['output']=-1
        with self.assertRaises(RuntimeError): kimi.parse_evidence(records)

    def test_stdout_requires_final_completion_and_no_tools(self):
        encode=lambda data:'\n'.join(json.dumps(e) for e in data)
        self.assertIn('return a + b', kimi.parse_stdout(encode(EVENTS))[0])
        with self.assertRaises(RuntimeError): kimi.parse_stdout(encode(EVENTS[:-1]))
        records=copy.deepcopy(EVENTS); records[1]['tool_calls']=[{'name':'Bash'}]
        with self.assertRaises(RuntimeError): kimi.parse_stdout(encode(records))
        records=copy.deepcopy(EVENTS); records[2]['session_id']='../../credentials'
        with self.assertRaises(RuntimeError): kimi.parse_stdout(encode(records))

    def test_cancel_does_not_start_client(self):
        cancel=threading.Event(); cancel.set()
        with patch.object(kimi.subprocess,'Popen') as start:
            with self.assertRaises(RuntimeError): kimi.execute('test',cancel=cancel)
            start.assert_not_called()

    def test_provider_dispatch_and_receipt_gate(self):
        with patch.object(kimi,'connection_status',return_value='installed_pending_auth_validation'), patch.object(kimi,'execute') as run:
            with self.assertRaises(RuntimeError): providers.execute('kimi','test',pathlib.Path('.'))
            run.assert_not_called()
        with patch.object(kimi,'connection_status',return_value='ready'), patch.object(kimi,'execute',return_value={'text':'ok','usage':{'total_tokens':2}}) as run:
            result=providers.execute('kimi','test',pathlib.Path('.'))
            self.assertEqual(result['text'],'ok'); self.assertIn('PEDIDO DO OPERADOR:\ntest',run.call_args.args[0])

    def test_node_bridge_uses_stdin_and_only_supported_flags(self):
        # Run the actual bridge against an inert CLI fixture, never the network.
        with tempfile.TemporaryDirectory() as folder:
            root=pathlib.Path(folder); adapter=root/'iald_orchestrator'; adapter.mkdir()
            launcher=adapter/'kimi_stdin.mjs'; launcher.write_bytes(kimi.LAUNCHER.read_bytes())
            entry=root/'clients/node_modules/@moonshot-ai/kimi-code/dist/main.mjs'
            entry.parent.mkdir(parents=True)
            entry.write_text('process.stdout.write(JSON.stringify(process.argv.slice(2)));',encoding='utf-8')
            prompt='PRIVATE_SENTINEL $() `x` \n Unicode: ação'
            args=[shutil.which('node'),str(launcher)]
            proc=subprocess.run(args,input=json.dumps(prompt),capture_output=True,text=True,encoding='utf-8',cwd=folder,timeout=10)
            self.assertEqual(proc.returncode,0,proc.stderr)
            flags=json.loads(proc.stdout)
            self.assertNotIn(prompt,' '.join(args))
            self.assertEqual(flags[flags.index('-p')+1],prompt)
            self.assertEqual(flags[flags.index('--model')+1],MODEL)
            self.assertNotIn('--yolo',flags)


if __name__=='__main__': unittest.main()
