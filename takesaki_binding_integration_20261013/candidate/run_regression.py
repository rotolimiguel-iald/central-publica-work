
import sys,unittest,json,hashlib,io,gc
from pathlib import Path
from unittest.mock import patch
sys.dont_write_bytecode=True
BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
TARGET=Path(__file__).parent if sys.argv[1]=='candidate' else BASE
sys.path.insert(0,str(TARGET));sys.path.append(str(BASE))
from iald_orchestrator import runtime as rt,canonical_memory as cm,operational_memory as om
import test_coordination,test_optional_work
def packet(prompt,c,system,*args,operational_projection=None):
 p={'prompt':'Scientific fixture '+prompt,'receipt':{'generation':'a'*64,'sources':[],
   'memory_mode':cm.mode_for_provider(c['required_provider'],c) if c else 'standard'}}
 p['receipt']['packet_sha256']=cm.digest(p['prompt'].encode())
 return om.attach(p,operational_projection,system,c['required_provider'] if c else 'local',c)
suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(m) for m in [test_coordination,test_optional_work]])
stream=io.StringIO()
with patch.object(rt.Runtime,'source_status',return_value={'ok':True}),patch.object(rt.nos_packet,'prepare_queue',side_effect=packet),\
 patch.object(rt.providers,'require_local_available'),patch.object(rt.providers,'execute',side_effect=AssertionError('Unmocked remote forbidden')),\
 patch.object(rt.jev_body_shadow,'observe',return_value={'status':'regression_stub'}):
 result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
gc.collect()
report={'mode':sys.argv[1],'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'success':result.wasSuccessful(),
 'scope':'existing test_coordination.py and test_optional_work.py with same isolated source_status/nos_packet/local availability safety harness; executor calls mocked by existing tests',
 'log':stream.getvalue()}
out=Path(__file__).parent/('REGRESSION_'+sys.argv[1]+'.json')
data=json.dumps(report,ensure_ascii=False,indent=2).encode();assert not out.exists();tmp=out.with_suffix('.tmp')
with tmp.open('xb') as f:f.write(data);f.flush();__import__('os').fsync(f.fileno())
assert tmp.read_bytes()==data;__import__('os').replace(tmp,out)
print(json.dumps({k:v for k,v in report.items() if k!='log'}))
print('sha256',hashlib.sha256(data).hexdigest())
if not result.wasSuccessful():print(stream.getvalue());sys.exit(1)
