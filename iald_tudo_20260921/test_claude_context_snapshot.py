"""Focal S3/S4 offline tests; no ROOT, server, SDK, env or network import."""
import ast
from copy import deepcopy
from dataclasses import replace
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import socket
import sys
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch
sys.dont_write_bytecode = True
def blocked(*a, **k): raise AssertionError('Network forbidden')
socket.create_connection = blocked
socket.socket.connect = blocked
socket.socket.connect_ex = blocked
import claude_context_snapshot as p
W = Path(__file__).resolve().parent
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
    def test_public_metadata_never_exposes_internal_receipt_path(self):
        internal_path = r'C:\private-fixture\work\measurement.json'
        snapshot = replace(fixture_snapshot(), measurement_receipt=internal_path)
        self.assertEqual(snapshot.measurement_receipt, internal_path)
        for limits in (False, True):
            data, status = p.status_response(lambda: snapshot, lambda x: x, limits=limits)
            self.assertEqual(status, 200)
            self.assertNotIn('measurement_receipt', data)
            self.assertNotIn('private-fixture', json.dumps(data))
            self.assertEqual(data['origem_medicao'], 'pacote validado pelo servidor')
            self.assertEqual(data['prefix_sha256'], snapshot.prefix_sha256)
            self.assertEqual(data['tools_sha256'], snapshot.tools_sha256)

    def test_load_snapshot_uses_loader_and_detects_manifest_change(self):
        raw=json.dumps(manifest).encode('utf-8')
        loader=Mock(return_value=package(manifest))
        with patch.object(Path,'read_bytes',side_effect=[raw,raw]):
            pkg,snapshot=p.load_snapshot('fixture-only',loader)
        loader.assert_called_once_with('fixture-only')
        self.assertEqual(snapshot.permanent,183135)
        self.assertIs(pkg,loader.return_value)
        with patch.object(Path,'read_bytes',side_effect=[raw,raw+b' ']):
            with self.assertRaisesRegex(p.HaikuUnavailable,'manifest_changed'):
                p.load_snapshot('fixture-only',loader)

    def test_schema_duplicates_missing_and_malformed_rejected(self):
        for transform in (lambda t:t.__setitem__(1,deepcopy(t[0])),
                          lambda t:t[0].update(input_schema=None),
                          lambda t:t.__setitem__(0,None)):
            t=tools();transform(t)
            with self.assertRaises(p.HaikuUnavailable):p.native_tools_sha256(t)
        s=fixture_snapshot()
        with self.assertRaises(p.HaikuUnavailable):
            p.verify_native_tools({'model':p.MODEL},s)
        with self.assertRaises(p.HaikuUnavailable):
            p.verify_native_tools({'model':'other','tools':tools()},s)

    @classmethod
    def tearDownClass(cls):
        for path,raw in BEFORE.items():
            if path.read_bytes()!=raw:raise AssertionError('Input drift: '+str(path))

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
        self.assertEqual(d['margem'],0.90)
        self.assertEqual(d['n_ctx']*d['margem'],180000)
        self.assertEqual(d['margem_tokens'],1024)
        self.assertFalse(d['recorte_por_cpt_permitido'])

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


if __name__ == '__main__':
    unittest.main()
