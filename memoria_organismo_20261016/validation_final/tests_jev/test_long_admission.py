"""Real JEV admission/transport paths, private receipts and simulated HTTP only."""
import copy
import hashlib
import json
from pathlib import Path
import socket
import sys
import types
import unittest
from unittest import mock
import uuid

WORK=Path(__file__).resolve().parents[1]
PROD=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(WORK/'staging/app_r2'),str(WORK/'staging/app'),str(WORK/'staging/core_r2/lib'),str(WORK/'staging/native'),str(PROD)]
import iald_auto_router as router
import iald_jev_control as control

def size(x):return len(json.dumps(x,ensure_ascii=True,allow_nan=False).encode('ascii'))
def body(padding=0):
    return {'model':control.MODEL,'state':{'source':{},'canonical_memory':'s'*1024,'data':'x'*padding},
        'questions':{'executor':{'type':'choice','instructions':'Choose','criteria':{'mimo':'Allowed'}}}}
def filled_request(target):
    b=body();b['state']['data']='x'*(target-size(b));assert size(b)==target;return b

class Response:
    status_code=200
    headers={'Content-Type':'application/json'}
    def __init__(self,body,status=200):
        self.body,self.status_code=body,status
    def json(self):return self.body

class JTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract=control.load_contract(PROD)
        cls.science=router.memory_slice(PROD)

    def setUp(self):
        self.root=WORK/'tests_jev/runs'/uuid.uuid4().hex[:12];self.root.mkdir(parents=True)
        self.network=mock.patch.object(socket,'create_connection',side_effect=AssertionError('NO NETWORK'))
        self.network.start()
    def tearDown(self):self.network.stop()

    def run_transport(self,padding=0,behavior='success'):
        seen=[];reserved=[]
        before_receipts=set((self.root/'.iald_runtime/app_routing').glob('*.json'))
        backend=types.SimpleNamespace(availability=lambda:{'status':'ready'},validate_prompt=lambda x:None,
            ENDPOINT='https://fixture.invalid/systemone',_key=lambda:'fixture-not-a-credential')
        memory=copy.deepcopy(json.loads((WORK/f'tests_app/JEV_C2_PACKET_ordinary_{100 if padding==100 else 10}_R1.json').read_bytes())['state']['common_memory']) if padding else None
        def post(url,**kw):
            seen.append((url,copy.deepcopy(kw)))
            if behavior=='timeout':raise TimeoutError('transport fixture')
            if behavior=='reject':return Response({},400)
            preferred={'scientific_mode':'explanation','work_path':'answer','memory_action':'use_loaded',
                'executor':'mimo','collaboration':'direct','memory_continuity':'continue'}
            answers={k:{'type':'choice','choice':preferred[k],'confidence':.9,
                'probabilities':{v:float(v==preferred[k]) for v in q['criteria']}} for k,q in kw['json']['questions'].items()}
            return Response({'model':control.MODEL,'usage':{'input_tokens':100},'answers':answers})
        patches=[mock.patch.object(router,'backend',return_value=backend),
            mock.patch.object(router,'available',return_value=True),
            mock.patch.object(control,'load_contract',return_value=self.contract),
            mock.patch.object(router,'memory_slice',return_value=self.science),
            mock.patch.object(router,'observations',return_value={'status':'no_samples'}),
            mock.patch.object(router.app_memory,'routing_state',return_value=memory),
            mock.patch.object(router.wallet_runtime,'routing_begin',side_effect=lambda cap:reserved.append(cap))]
        from contextlib import ExitStack
        with ExitStack() as stack:
            for patch in patches:stack.enter_context(patch)
            if behavior=='success':
                result=router.choose('Continue a atividade',['mimo'],root=self.root,post=post)
                self.assertEqual(result[0],'mimo')
            else:
                with self.assertRaises(Exception):router.choose('Continue a atividade',['mimo'],root=self.root,post=post)
        self.assertEqual(len(seen),1)
        new_receipts=set((self.root/'.iald_runtime/app_routing').glob('*.json'))-before_receipts
        self.assertEqual(len(new_receipts),1)
        record=json.loads(new_receipts.pop().read_bytes())
        wire=json.dumps(seen[0][1]['json'],ensure_ascii=True,allow_nan=False).encode('ascii')
        self.assertEqual(record['wire_payload_sha256'],hashlib.sha256(wire).hexdigest())
        self.assertEqual(record['admission']['request_bytes'],len(wire))
        self.assertEqual(reserved,[len(wire)*.042/1000000])
        self.assertNotIn('Authorization',record['transport_headers'])
        self.assertEqual(seen[0][1]['timeout'],(10,25));self.assertFalse(seen[0][1]['allow_redirects'])
        return seen[0][1],record

    def test_default_short_transport_header_absent(self):
        kw,record=self.run_transport()
        self.assertNotIn(control.LONG_CONTEXT_HEADER,kw['headers'])
        self.assertEqual(record['admission']['context_mode'],'short')

    def test_long_transport_header_wire_and_wallet(self):
        for count in (10,100):
            kw,record=self.run_transport(padding=count)
            self.assertEqual(kw['headers'][control.LONG_CONTEXT_HEADER],'true')
            self.assertEqual(record['transport_headers'][control.LONG_CONTEXT_HEADER],'true')
            self.assertEqual(record['admission']['context_mode'],'long')
            self.assertEqual(len(kw['json']['state']['canonical_memory']),1024)

    def test_large_optional_retrieval_is_reduced_before_long_mode(self):
        b=body();b['state']['canonical_memory']='x'*200000
        result=router._fit_routing_payload(b)
        self.assertEqual(result['context_mode'],'short')
        self.assertEqual(result['transport_headers'],{})
        self.assertLess(len(b['state']['canonical_memory']),200000)

    def test_rejection_does_not_retry_or_change_mode(self):
        kw,record=self.run_transport(padding=1,behavior='reject')
        self.assertEqual(kw['headers'][control.LONG_CONTEXT_HEADER],'true')
        self.assertNotEqual(record['status'],'selected')

    def test_timeout_does_not_retry_or_change_mode(self):
        kw,record=self.run_transport(padding=1,behavior='timeout')
        self.assertEqual(kw['headers'][control.LONG_CONTEXT_HEADER],'true')
        self.assertNotEqual(record['status'],'selected')

    def test_real_packets_1_10_100_preserve_required_context(self):
        for count in (1,10,100):
            for profile in ('ordinary','haja_luz'):
                b=json.loads((WORK/f'tests_app/JEV_C2_PACKET_{profile}_{count}_R1.json').read_bytes())
                before=copy.deepcopy(b)
                p=router._fit_routing_payload(b)
                self.assertEqual(p['context_mode'],'short' if count==1 else 'long')
                self.assertEqual(b['state']['common_memory'],before['state']['common_memory'])
                self.assertEqual(b['questions'],before['questions'])
                self.assertLessEqual(len(b['state']['canonical_memory']),len(before['state']['canonical_memory']))
                self.assertEqual(p['request_bytes'],size(b))

    def test_short_state_boundary(self):
        b=body();b['state']['data']='x'*(30000-size(b['state']))
        self.assertEqual(control.check_payload(b)['state_bytes'],30000)
        b['state']['data']+='x'
        with self.assertRaises(control.ControlError):control.check_payload(b)
        self.assertEqual(control.check_payload(b,long_context=True)['context_mode'],'long')

    def test_short_question_and_request_boundaries(self):
        b=body();q=b['questions']['executor'];q['instructions']='x'*(32000-size(b['state'])-size(q)+len(q['instructions']))
        self.assertEqual(control.check_payload(b)['state_longest_question_bytes'],32000)
        q['instructions']+='x'
        with self.assertRaises(control.ControlError):control.check_payload(b)
        b=body();b['questions']={str(i):{'type':'choice','instructions':'x'*19000} for i in range(3)}
        remaining=60000-size(b);b['questions']['0']['instructions']+='x'*remaining
        self.assertEqual(control.check_payload(b)['request_bytes'],60000)
        b['questions']['0']['instructions']+='x'
        with self.assertRaises(control.ControlError):control.check_payload(b)

    def test_long_request_boundary(self):
        self.assertEqual(control.check_payload(filled_request(250000),long_context=True)['request_bytes'],250000)
        with self.assertRaises(control.ControlError):control.check_payload(filled_request(250001),long_context=True)

    def test_long_question_is_bounded_and_body_limit_separate(self):
        b=body();b['questions']['executor']['instructions']='x'*250000
        with self.assertRaises(control.ControlError):control.check_payload(b,long_context=True)
        b=body(32*1024*1024)
        with mock.patch.object(control,'MAX_LONG_CONTEXT_BYTES',40*1024*1024):
            with self.assertRaisesRegex(control.ControlError,'HTTP byte limit'):control.check_payload(b,long_context=True)

    def test_unicode_uses_exact_escaped_json_bytes(self):
        import requests
        b=body();b['state']['data']='ç🙂漢'*1000
        p=control.check_payload(b,long_context=True)
        prepared=requests.Request('POST','https://fixture.invalid',json=b).prepare()
        self.assertEqual(p['request_bytes'],len(prepared.body))
        self.assertGreater(p['request_bytes'],len(json.dumps(b,ensure_ascii=False).encode()))
        self.assertFalse(p['tokenizer_exact'])

    def test_invalid_json_model_and_mode(self):
        for value in (float('nan'),float('inf'),'\ud800',set(),10**10000,{1:'numeric key'}):
            b=body();b['state']['data']=value
            with self.assertRaises(control.ControlError):control.check_payload(b,long_context=True)
        for change in ({'model':'jev-1.14.0'},{'questions':[]},{'questions':{}},{'state':[]}):
            b=body();b.update(change)
            with self.assertRaises(control.ControlError):control.check_payload(b)
        with self.assertRaises(control.ControlError):control.check_payload(body(),long_context='true')

    def test_cycles_depth_and_required_overflow_refuse_before_transport(self):
        b=body();b['state']['cycle']=b
        with self.assertRaises(control.ControlError):control.check_payload(b)
        value='x'
        for _ in range(65):value=[value]
        b=body();b['state']['data']=value
        with self.assertRaises(control.ControlError):control.check_payload(b)
        with self.assertRaises(router.RoutingContextOverflow):router._fit_routing_payload(body(260000))

if __name__=='__main__':unittest.main(verbosity=2)
