"""Focal S3/S4 offline tests; no ROOT, server, SDK, env or network import."""
import ast
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import socket
import sys
from types import SimpleNamespace as NS
import unittest
sys.dont_write_bytecode = True
def blocked(*a, **k): raise AssertionError('Network forbidden')
socket.create_connection = blocked
socket.socket.connect = blocked
socket.socket.connect_ex = blocked
import haiku_s3_s4_proposal as p
W = Path(__file__).resolve().parent.parent
MANIFEST = W/'haiku_package_20260922_141841_074636/manifest.json'
BUILDER = W/'count_native_reviewed_draft.py'
manifest = json.loads(MANIFEST.read_bytes())
RECEIPT = W/manifest['measurement_receipt']
receipt = json.loads(RECEIPT.read_bytes())
INPUTS = [MANIFEST, BUILDER, RECEIPT, W/'prepare_haiku_package.py', Path(p.__file__), Path(__file__)]
BEFORE = {q:q.read_bytes() for q in INPUTS}

def package(m):
    b = m['budget']
    return NS(measurement=NS(model=m['model'],prefix_sha256=m['prefix_sha256'],permanent_tokens=b['permanent_tokens']),
              reserved_output_tokens=b['reserved_output_tokens'],available_dynamic_tokens=b['remaining_tokens'],tools_sha256=m['tools_sha256'])

def tools():
    return [{'name':name,'description':'Descrição sintética çã',
             'input_schema':{'type':'object','properties':{}},'eager_input_streaming':True} for name in p.PUBLIC_NAMES]

def fixture_snapshot():
    m=deepcopy(manifest);m['tools_sha256']=p.native_tools_sha256(tools())
    return p.snapshot_from_manifest(m,package(m))

class FocalTests(unittest.TestCase):
    def test_manifest_receipt_chain(self):
        self.assertEqual(manifest['tools_sha256'],receipt['native_tools_sha256'])
        self.assertEqual(manifest['budget'],receipt['budget'])
        self.assertEqual(manifest['prefix_sha256'],receipt['draft_sha256'])
        self.assertEqual(list(p.PUBLIC_NAMES),receipt['tool_names'])

    def test_exact_builder_serializer_ast_without_importing_builder(self):
        tree=ast.parse(BUILDER.read_text(encoding='utf-8'))
        expr=None
        for node in ast.walk(tree):
            if isinstance(node,ast.Dict):
                for key,value in zip(node.keys,node.values):
                    if isinstance(key,ast.Constant) and key.value=='native_tools_sha256':expr=value
        self.assertIsNotNone(expr)
        expected=eval(compile(ast.Expression(expr),str(BUILDER),'eval'),{'hashlib':hashlib,'json':json,'wire':{'tools':tools()}})
        self.assertEqual(p.native_tools_sha256(tools()),expected)
        compact=hashlib.sha256(json.dumps(tools(),sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
        self.assertNotEqual(compact,expected)

    def test_status_reference_not_current_balance(self):
        s=p.snapshot_from_manifest(manifest,package(manifest))
        d,status=p.status_response(lambda:s,lambda x:x)
        self.assertEqual(status,200)
        self.assertEqual((d['n_ctx'],d['janela']), (200000,200000))
        self.assertEqual(d['memoria_tokens_medidos'],183135)
        self.assertEqual(d['requisicao_referencia_tokens_medidos'],184609)
        self.assertEqual(d['reserva_dinamica_medida'],10271)
        self.assertIsNone(d['saldo_conversa_atual_tokens'])
        self.assertIsNone(d['cpt'])

    def test_limits_same_snapshot(self):
        s=fixture_snapshot();d,status=p.status_response(lambda:s,lambda x:x,limits=True)
        self.assertEqual(status,200);self.assertEqual(d['max_saida'],4096)
        self.assertFalse(d['pensar']);self.assertEqual(d['ferramentas'],list(p.PUBLIC_NAMES))
        self.assertEqual(d['janela'],200000)

    def test_unavailable_json_503_no_paths(self):
        for exc in (PermissionError,ValueError,OSError,KeyError,TypeError):
            def fail():raise exc('private path must not escape')
            d,status=p.status_response(fail,lambda x:x)
            self.assertEqual(status,503);self.assertFalse(d['disponivel'])
            self.assertNotIn('private path',json.dumps(d))

    def test_manifest_mismatch_and_bool_rejected(self):
        for key,value in [('remaining_tokens',10001),('permanent_tokens',True),('margin_tokens',0)]:
            m=deepcopy(manifest);m['budget'][key]=value
            with self.assertRaises(p.HaikuUnavailable):p.snapshot_from_manifest(m,package(m))
        m=deepcopy(manifest);pkg=package(m);pkg.tools_sha256='0'*64
        with self.assertRaises(p.HaikuUnavailable):p.snapshot_from_manifest(m,pkg)

    def test_none_keeps_seven_schemas_and_no_mutation(self):
        defs=[{'type':'function','function':{'name':n,'parameters':{'type':'object'}}} for n in p.PUBLIC_NAMES]
        original={'tool_choice':'none'}
        attached=p.attach_openai_tools(original,defs)
        self.assertEqual(original,{'tool_choice':'none'});self.assertEqual(len(attached['tools']),7)
        self.assertEqual(attached['tool_choice'],'none')
        s=fixture_snapshot()
        for choice in ('none',{'type':'none'}, {'type':'auto'}):
            wire={'model':p.MODEL,'tools':tools(),'tool_choice':choice}
            self.assertEqual(p.verify_native_tools(wire,s),s.tools_sha256)

    def test_changed_schema_order_and_flags_visible(self):
        s=fixture_snapshot()
        for mutate in (lambda t:t[0].update(description='changed'),lambda t:t.reverse(),
                       lambda t:t[0].pop('eager_input_streaming'),lambda t:t.pop()):
            t=tools();mutate(t)
            with self.assertRaises(p.HaikuUnavailable):p.verify_native_tools({'model':p.MODEL,'tools':t},s)

    def test_native_vs_openai_not_interchangeable(self):
        defs=[{'type':'function','function':{'name':n,'parameters':{'type':'object'}}} for n in p.PUBLIC_NAMES]
        with self.assertRaises(p.HaikuUnavailable):p.native_tools_sha256(defs)
        with self.assertRaises(p.HaikuUnavailable):p.attach_openai_tools({},tools())
        with self.assertRaises(p.HaikuUnavailable):p.attach_openai_tools({'tools':[]},defs)

    def test_final_converter_boundary(self):
        s=fixture_snapshot();seen=[]
        wire={'model':p.MODEL,'tools':tools(),'tool_choice':{'type':'none'}}
        adapter=NS(marker='preserved',converter_pedido=lambda *a,**k:seen.append(k) or deepcopy(wire))
        proxy=p.CheckedAdapter(adapter,s)
        result=proxy.converter_pedido('cfg','payload',prefixo='fixture')
        self.assertEqual(proxy.marker,'preserved');self.assertEqual(result,wire)
        self.assertEqual(seen,[{'prefixo':'fixture'}])
        wire['tools'].pop()
        with self.assertRaises(p.HaikuUnavailable):proxy.converter_pedido('cfg','payload')


if __name__=='__main__':
    stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(FocalTests))
    for path,raw in BEFORE.items():assert path.read_bytes()==raw, 'Input drift: '+str(path)
    out=Path(__file__).parent/('s3_s4_test_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
    out.mkdir()
    report={'status':'PROPOSTA_CONSTRUIDA_AGUARDA_REVISAO_INDEPENDENTE','tests':result.testsRun,
            'failures':len(result.failures),'errors':len(result.errors),
            'pins':{str(q):hashlib.sha256(b).hexdigest() for q,b in BEFORE.items()},
            'serializer':'json.dumps(wire["tools"],sort_keys=True,ensure_ascii=False).encode("utf-8"); default spaces; list order and eager_input_streaming retained',
            'receipt_tools_sha256':manifest['tools_sha256'],
            'limits':['No ROOT reads/imports, network, env, SDK or generation. No stage changes.',
                      'Builder hash expression executed on synthetic native schemas only. Receipt hash chain checked; actual seven native schema contents not stored in these W receipts, so actual schema rehash is deferred to integration.',
                      'Caller must wire callback validation and proxy per instructions. No complete_chat_externo or parent test repetition.']}
    for name,text in [('report.json',json.dumps(report,ensure_ascii=False,indent=2)),('tests.txt',stream.getvalue())]:
        b=text.encode('utf-8');tmp=out/(name+'.tmp')
        with tmp.open('xb') as f:f.write(b)
        assert tmp.read_bytes()==b;tmp.rename(out/name)
    print(json.dumps({'report':str(out/'report.json'),'tests':result.testsRun,'passed':result.wasSuccessful()},ensure_ascii=False))
    if not result.wasSuccessful():print(stream.getvalue());sys.exit(1)
