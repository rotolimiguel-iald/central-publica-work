"""Independent offline audit. No server import, network or writes outside review."""
from pathlib import Path
import sys, os, json, hashlib, ast, re, shutil, importlib.util, unittest, io
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parent
SRC=ROOT.parent/'recovery'
SNAP=ROOT/'snapshot'
SNAP.mkdir(exist_ok=True)
names=['iald_auto_recovery.py','iald_motores.py','server_functions.py','test_recovery.py','build_staging.py','iald_web_server.py.patch','iald_motores.py.patch','BASELINE.json','MANIFEST.json']
pins={}
for name in names:
    data=(SRC/name).read_bytes()
    pins[name]=hashlib.sha256(data).hexdigest()
    (SNAP/name).write_bytes(data)
sys.dont_write_bytecode=True
sys.path.insert(0,str(SNAP))
os.environ['TMP']=str(ROOT)
os.environ['TEMP']=str(ROOT)
def audit(event,args):
    if event in ('socket.connect','socket.getaddrinfo'):
        raise RuntimeError('Network prohibited by independent review')
    if event=='open':
        path,mode,flags=args
        writing=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and isinstance(path,(str,bytes,os.PathLike)):
            if not Path(path).resolve().is_relative_to(ROOT):raise RuntimeError('Write outside review prohibited')
sys.addaudithook(audit)
import test_recovery as t
import iald_auto_recovery as recovery

def deltas(output):
    values=[]
    for line in output.splitlines():
        if line.startswith('data: ') and line!='data: [DONE]':
            d=json.loads(line[6:])
            for c in d.get('choices',[]):
                if c.get('delta',{}).get('content'):values.append(c['delta']['content'])
    return values

observations=[]
class Independent(unittest.TestCase):
    def test_manual_switch_during_second_jev_must_block_dispatch(self):
        h=t.Harness()
        h.on_reselect=lambda h:setattr(h,'current_motor','openai')
        out=h.run()
        observations.append({'case':'manual_switch_during_second_jev','replacements':len(h.replacements),'mode_at_dispatch':h.current_motor,'assistant_deltas':deltas(out)})
        self.assertFalse(h.replacements)
    def test_no_retry_after_200_then_second_refusal(self):
        attempt=recovery.Attempt();attempt.before_send();attempt.inspect(t.Wire(200))
        attempt.before_send();attempt.inspect(t.Wire())
        self.assertIsNone(attempt.refusal)
    def test_direct_500_error_must_not_be_assistant(self):
        h=t.Harness(agent=False,responses=[t.Wire(500,'server_error')]);out=h.run()
        observations.append({'case':'direct_500','assistant_deltas':deltas(out),'selections':len(h.selections),'sends':len(h.sends)})
        self.assertEqual(deltas(out),[])
    def test_agent_500_error_must_not_be_assistant(self):
        h=t.Harness(agent=True,responses=[t.Wire(500,'server_error')]);out=h.run()
        observations.append({'case':'agent_500','assistant_deltas':deltas(out),'selections':len(h.selections),'sends':len(h.sends)})
        self.assertEqual(deltas(out),[])
    def test_direct_timeout_must_not_be_assistant(self):
        h=t.Harness(agent=False,responses=[TimeoutError('synthetic timeout')]);out=h.run()
        observations.append({'case':'direct_timeout','assistant_deltas':deltas(out),'selections':len(h.selections),'sends':len(h.sends)})
        self.assertEqual(deltas(out),[])
    def test_refusal_after_metadata_fragment_no_retry(self):
        r=recovery.Recovery({},object(),recovery.Circuit())
        r.attempt.before_send()
        try:r.attempt.inspect(t.Wire())
        except recovery.DefinitiveRefusal as e:e.settled=True
        def stream():
            yield 'data: {"iald_status":'
            raise r.attempt.refusal
        calls=[]
        response=t.Response(stream(),mimetype='text/event-stream')
        output=''.join(r.wrap(response,lambda:calls.append(True)).response)
        self.assertFalse(calls)
        self.assertNotIn('choices',output)
    def test_ttl_expiry_and_configuration_identity(self):
        clock=[0];c=recovery.Circuit(ttl=300,clock=lambda:clock[0]);a=object();b=object()
        c.block(a);self.assertEqual(c.excludes(a),{'openai'});self.assertFalse(c.excludes(b))
        clock[0]=300;self.assertFalse(c.excludes(a))
    def test_settlement_finalizer_failure_does_not_reselect(self):
        h=t.Harness();original=h.account
        def account():
            a=original()
            def fail():raise OSError('finalizer failure synthetic')
            a.fechar=fail
            return a
        h.account=account
        try:h.run()
        except OSError:pass
        self.assertEqual(len(h.selections),1)
    def test_replacement_error_frame_must_not_be_assistant(self):
        h=t.Harness()
        def replace(*args,**kwargs):
            return t.Response(t.sse({'iald_aviso':{'tipo':'falha_motor','texto':'synthetic failure'}})+t.sse({'choices':[{'delta':{'content':'synthetic failure'}}]})+t.sse('[DONE]'),mimetype='text/event-stream')
        h.env['_chat_avaliacao']=replace
        out=h.run()
        observations.append({'case':'replacement_failure','assistant_deltas':deltas(out),'selections':len(h.selections)})
        self.assertEqual(deltas(out),[])

log=io.StringIO()
author=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(t.RecoveryTests))
independent=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Independent))
(ROOT/'TEST_LOG.txt').write_text(log.getvalue(),encoding='utf-8')
result={'at':datetime.now(timezone.utc).isoformat(),'candidate_pins':pins,'author_suite':{'tests':author.testsRun,'failures':len(author.failures),'errors':len(author.errors)},'independent_suite':{'tests':independent.testsRun,'failures':len(independent.failures),'errors':len(independent.errors)},'observations':observations,'network':'prohibited by audit hook and socket guard','writes':'review only','production_server_imported':False,'candidate_still_matches':{name:hashlib.sha256((SRC/name).read_bytes()).hexdigest()==pin for name,pin in pins.items()}}
(ROOT/'TEST_RESULT.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
