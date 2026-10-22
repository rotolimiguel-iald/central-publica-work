"""Generate a source-pinned patch and test it without importing the app."""
import ast
import base64
import difflib
import hashlib
import json
from pathlib import Path
import sys
import types
import unittest

ROOT = Path(__file__).parent
SOURCE = Path('C:/IALD/projetos_pyhton/IALD/iald_app_providers.py')
raw = SOURCE.read_bytes()
original = raw.decode('utf-8')
helper = (ROOT / 'image_transport.py').read_text(encoding='utf-8')
staged = original.replace("def wire_messages(messages, prefix, profile=''):",
    "def wire_messages(messages, prefix, profile='', *, provider=None, images_authorized=False, media_authorized=False):", 1)
staged = staged.replace('def limits(provider):', 'def limits(provider, *, media_authorized=False):', 1)
staged = staged.replace("pensar=True, imagens=False,", "pensar=True, imagens=(provider == 'mimo'), audio=(provider == 'mimo' and media_authorized is True), video=(provider == 'mimo' and media_authorized is True),", 1)
staged = staged.replace("streaming=provider != 'kimi', calls=[], first_text_seconds=None)", "streaming=provider != 'kimi', calls=[], first_text_seconds=None, task=metric_task(messages))",1)
staged = staged.replace('def observe(self, flow, model, *, rates=None, memory_sha256=None):', 'def observe(self, flow, model, *, rates=None, memory_sha256=None, messages=None):',1)
staged = staged.replace("calls=[], streaming=True, metrics_source='existing_app_sse')", "calls=[], streaming=True, metrics_source='existing_app_sse', task=metric_task(messages) if messages is not None else 'unknown')",1)
needle = "        if item.get('role') not in ('user', 'assistant') or not isinstance(item.get('content'), str):"
replacement = '''        if isinstance(item.get('content'), list) and item.get('role') == 'user' and provider == 'mimo':
            parts = image_parts(item['content'], images_authorized=images_authorized, media_authorized=media_authorized)
            result.append({'role': 'user', 'content': parts})
            continue
''' + needle
assert staged.count(needle) == 1
staged = staged.replace(needle, replacement, 1)
tool_old = "            if offered:\n                body.update(tools=offered, tool_choice='none' if round_no == rounds-1 else 'auto')"
if '\r\n' in original:
    tool_old = tool_old.replace('\n', '\r\n')
assert staged.count(tool_old) == 1
staged = staged.replace(tool_old, "            body.update(transport_tool_options(provider, offered, round_no, rounds))", 1)
staged = staged.replace('def wire_messages(', helper + '\n\n' + 'def wire_messages(', 1)
compile(staged, 'staging/iald_app_providers.py', 'exec')
(ROOT / 'iald_app_providers.py').write_text(staged, encoding='utf-8', newline='')
(ROOT / 'transport.patch').write_text(''.join(difflib.unified_diff(
    original.splitlines(True), staged.splitlines(True),
    fromfile='a/iald_app_providers.py', tofile='b/iald_app_providers.py')), encoding='utf-8')

# Extract the existing pure detector: no production modules imported or executed.
claude_source = Path('C:/IALD/projetos_pyhton/IALD/iald_motor_claude.py').read_text(encoding='utf-8')
detector = ast.parse(claude_source)
nodes = [n for n in detector.body if
    isinstance(n, ast.FunctionDef) and n.name == '_tipo_pelos_bytes' or
    isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == '_ASSINATURAS_DE_IMAGEM' for t in n.targets)]
import re, binascii
mock_claude = types.ModuleType('iald_motor_claude')
mock_claude.__dict__.update(base64=base64, re=re, binascii=binascii)
exec(compile(ast.Module(body=nodes, type_ignores=[]), '<existing pure detector>', 'exec'), mock_claude.__dict__)
sys.modules['iald_motor_claude'] = mock_claude
namespace = dict(app_memory=types.SimpleNamespace(project_messages=lambda x: x))
tree = ast.parse(staged)
selected = [n for n in tree.body if isinstance(n, ast.Import) and any(a.name in ('base64','binascii') for a in n.names)
    or isinstance(n, ast.FunctionDef) and n.name in ('image_parts','wire_messages','transport_tool_options','transport_response_format','limits','metric_task','request_media')]
namespace.update(MODELS={'mimo':{'output':131072},'kimi':{'output':131072}}, TOOL_NAMES=frozenset(), WINDOW=1048576)
exec(compile(ast.Module(body=selected, type_ignores=[]), '<isolated transport>', 'exec'), namespace)
wire = namespace['wire_messages']
url = 'data:image/png;base64,' + base64.b64encode(b'\x89PNG\r\n\x1a\nsynthetic').decode()
part = {'type':'image_url', 'image_url':{'url':url}}

class BoundaryTests(unittest.TestCase):
    def test_router_projection_no_media_bytes(self):
        messages=[{'role':'user','task':'forged','content':[part,{'type':'text','text':'[ARQUIVO: x.txt]\npython\n[FIM]\npergunta'}]}]
        projected=namespace['request_media'](messages)
        self.assertEqual(projected['prompt'],'pergunta')
        self.assertEqual(projected['kinds'],['image'])
        self.assertNotIn('base64',json.dumps(projected))
    def test_host_task_ignores_client_labels_and_attached_text(self):
        policy=types.ModuleType('iald_task_policy')
        policy.classify=lambda text:'code' if 'python' in text else 'conversation'
        sys.modules['iald_task_policy']=policy
        self.assertEqual(namespace['metric_task']([{'role':'system','content':'python'},{'role':'user','task':'code','content':'[ARQUIVO: x]\npython\n[FIM]\nhello'}]),'conversation')
        self.assertEqual(namespace['metric_task']([{'role':'user','content':'python'},{'role':'assistant','content':'hello'}]),'code')
    def test_capability_requires_authorization_and_provider(self):
        self.assertTrue(namespace['limits']('mimo')['imagens'])
        self.assertTrue(namespace['limits']('mimo',media_authorized=True)['audio'])
        self.assertFalse(namespace['limits']('kimi',media_authorized=True)['imagens'])
    def test_structured_output_opt_in(self):
        self.assertEqual(namespace['transport_response_format'](),{})
        self.assertEqual(namespace['transport_response_format']('json_object'), {'response_format':{'type':'json_object'}})
        with self.assertRaises(ValueError): namespace['transport_response_format']('json_schema')
    def test_final_mimo_has_no_tools(self):
        self.assertEqual(namespace['transport_tool_options']('mimo', [{'type':'function'}], 3, 4), {})
    def test_mimo_auto_before_final(self):
        self.assertEqual(namespace['transport_tool_options']('mimo', ['tool'], 0, 4), dict(tools=['tool'],tool_choice='auto'))
    def test_deepseek_unchanged(self):
        self.assertEqual(namespace['transport_tool_options']('deepseek', ['tool'], 3, 4), dict(tools=['tool'],tool_choice='none'))
    def test_reasoning_retained_in_tool_history_not_emitted(self):
        # Existing implementation already preserves this contract; pin it.
        self.assertIn("messages.append(dict(role='assistant', content=content, reasoning_content=reasoning, tool_calls=batch))", staged)
        emits = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'emit']
        self.assertFalse(any('reasoning' in ast.unparse(n) for n in emits))
    def send(self, parts, **kw):
        return wire([{'role':'user','content':parts}], 'SCIENCE_UNCHANGED', provider='mimo', **kw)
    def test_image_preserved(self):
        out = self.send([part, {'type':'text','text':'question'}], images_authorized=True)
        self.assertEqual(out[0]['content'], 'SCIENCE_UNCHANGED')
        self.assertEqual(out[1]['content'][0], part)
    def test_default_refuses(self):
        with self.assertRaises(ValueError): self.send([part])
    def test_other_provider_refuses(self):
        with self.assertRaises(ValueError): wire([{'role':'user','content':[part]}], 'S', provider='deepseek', images_authorized=True)
    def test_remote_urls_refused(self):
        for u in ('https://example.com/x.png','http://127.0.0.1/x','file:///x','data:image/svg+xml;base64,PHN2Zz4='):
            with self.subTest(u=u), self.assertRaises(ValueError): self.send([{'type':'image_url','image_url':{'url':u}}], images_authorized=True)
    def test_invalid_base64(self):
        with self.assertRaises(ValueError): self.send([{'type':'image_url','image_url':{'url':url+'!'}}], images_authorized=True)
    def test_wrong_mime(self):
        with self.assertRaises(ValueError): self.send([{'type':'image_url','image_url':{'url':url.replace('image/png','image/jpeg')}}], images_authorized=True)
    def test_unknown_and_media_refused(self):
        for kind in ('input_audio','video_url','file','tool'):
            with self.subTest(kind=kind), self.assertRaises(ValueError): self.send([{'type':kind}], images_authorized=True)
    def test_image_count(self):
        with self.assertRaises(ValueError): self.send([part]*4, images_authorized=True)
    def test_client_system_cannot_replace_science(self):
        self.assertEqual(wire([{'role':'system','content':'evil'},{'role':'user','content':'q'}], 'SCIENCE')[0]['content'],'SCIENCE')
    def test_assistant_media_refused(self):
        with self.assertRaises(ValueError): wire([{'role':'assistant','content':[part]},{'role':'user','content':'q'}], 'S', provider='mimo', images_authorized=True)
    def test_pdf_text_unchanged(self):
        text = '[ARQUIVO: a.pdf]\nextracted text\n[FIM]\nquestion'
        self.assertEqual(wire([{'role':'user','content':text}], 'S')[1]['content'],text)
    def test_extra_fields_refused(self):
        with self.assertRaises(ValueError): self.send([dict(part, instruction='x')], images_authorized=True)
    def test_encoded_budget(self):
        with self.assertRaises(ValueError): self.send([{'type':'image_url','image_url':{'url':'data:image/png;base64,'+'A'*10_666_669}}], images_authorized=True)

result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(BoundaryTests))
receipt = dict(status='PASS' if result.wasSuccessful() else 'FAIL', tests=result.testsRun,
    production_source=str(SOURCE), source_sha256=hashlib.sha256(raw).hexdigest(),
    staged_sha256=hashlib.sha256((ROOT/'iald_app_providers.py').read_bytes()).hexdigest(),
    production_unchanged=SOURCE.read_bytes()==raw, network_calls=0, credential_reads=0,
    scope='isolated pure transport tests; no app integration, real image decoding or provider acceptance measured',
    coordination_memory='init IntegrityError under repair by memory agent; no parallel bank created')
(ROOT/'test_result.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
if not result.wasSuccessful(): raise SystemExit(1)
