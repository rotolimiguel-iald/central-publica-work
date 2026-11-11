"""Independent offline controls review. All mutations stay under this directory."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import sys
import types
import uuid

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent.parent
D = W / 'review' / ('controls_r1_' + uuid.uuid4().hex)
D.mkdir()
sha = lambda b: hashlib.sha256(b).hexdigest()
results = []
pins = {}
names = ('transaction.py','maintenance.py','deploy_controlled.py','preservation_guard.py','verify_installed.py')
for name in names:
    raw = (W/name).read_bytes()
    pins[name] = sha(raw)
    (D/name).write_bytes(raw)
    ast.parse(raw)

def load(name):
    m = types.ModuleType(name)
    m.__file__ = str(D/(name+'.py'))
    exec(compile((D/(name+'.py')).read_bytes(),m.__file__,'exec'),m.__dict__)
    return m

def check(name, fn):
    fn()
    results.append({'test':name,'status':'PASS'})

def refused(fn):
    try: fn()
    except (ValueError,RuntimeError,FileNotFoundError): return
    raise AssertionError('Expected refusal')

def eq(a,b):
    assert a == b,(a,b)

g = load('preservation_guard')
g.WORK = W
check('13 live preservation pins match current files',lambda:eq(len(g.verify()),13))
baseline_raw = (W/'PRESERVATION_BASELINE.json').read_bytes()
pins['PRESERVATION_BASELINE.json'] = sha(baseline_raw)
live = json.loads(baseline_raw)
check('13 unique pins and sizes',lambda:eq(len({r['path'] for r in live['files'] if Path(r['path']).stat().st_size==r['bytes']}),13))
g.WORK = D
g.ROOT = D/'runtime'
g.ROOT.mkdir()
f = g.ROOT/'protected.txt'; f.write_bytes(b'current post-v408')
baseline = {'files':[{'path':str(f),'sha256':sha(f.read_bytes())}]}
def put_baseline(b): (D/'PRESERVATION_BASELINE.json').write_text(json.dumps(b),encoding='utf-8')
put_baseline(baseline)
check('fixture preservation positive',lambda:eq(all(g.verify().values()),True))
f.write_bytes(b'old patch')
check('old patch replacement refused',lambda:refused(g.verify))
f.write_bytes(b'current post-v408')
put_baseline({'files':[]})
check('empty preservation refused',lambda:refused(g.verify))
outside=D/'outside.txt';outside.write_bytes(b'x')
put_baseline({'files':[{'path':str(outside),'sha256':sha(b'x')}]})
check('preservation path outside root refused',lambda:refused(g.verify))
check('missing restart approval refused',lambda:refused(g.approved_restart))
reply=D/'reply.txt';reply.write_bytes(b'synthetic approval only')
approval={'release':'v409','restart_web_8082':True,'operator_reply_path':str(reply),'operator_reply_sha256':sha(reply.read_bytes())}
ap=D/'APROVACAO_V409.json'
ap.write_text(json.dumps(approval))
check('synthetic restart approval positive',lambda:eq(g.approved_restart()['release'],'v409'))
reply.write_bytes(b'changed')
check('changed approval refused',lambda:refused(g.approved_restart))
approval['release']='v408';ap.write_text(json.dumps(approval))
check('wrong release approval refused',lambda:refused(g.approved_restart))

t=load('transaction');t.ROOT=g.ROOT;t.WORK=D
cfg=types.ModuleType('release_cfg');cfg.load=lambda **kw:types.SimpleNamespace(target_name='v409_fixture',release='v409')
sys.modules['release_cfg']=cfg
fixed=[t.ROOT/'core_packet_v409_bound.txt']+[t.ROOT/'.iald_runtime'/p/n for p in ('haiku','haiku55') for n in ('prefix.md','manifest.json','native_count.json')]
fixed += [t.ROOT/'iald_nucleo_fixo.json']
rows=[{'destination':str(p),'baseline':None} for p in fixed]
check('eight activation destinations accepted',lambda:t.check_science_destinations(rows))
for label,path in [('runtime',t.ROOT/'iald_motores.py'),('old release',t.ROOT/'canonical_releases/v408_old/a.txt'),('client',t.ROOT/'app/a.js')]:
    check(label+' destination refused',lambda path=path:refused(lambda:t.check_science_destinations([{'destination':str(path),'baseline':None}]+rows)))
check('duplicate destination refused',lambda:refused(lambda:t.check_science_destinations([rows[0]]+rows)))
check('manifest must be last',lambda:refused(lambda:t.check_science_destinations(list(reversed(rows)))))
check('existing immutable release refused',lambda:refused(lambda:t.check_science_destinations([{'destination':str(t.ROOT/'canonical_releases/v409_fixture/a.txt'),'baseline':'old'}]+rows)))
m=load('maintenance')
check('writes without maintenance refused',lambda:refused(m.assert_quiesced))

# Only fake maintenance and snapshots; no service, ledger or network access.
fake=types.ModuleType('maintenance');fake.assert_quiesced=lambda:None
sys.modules['maintenance']=fake
t.quiet=lambda:None
snapshot={'errors':[],'state':{'fixture':{'bytes':1,'sha256':'x'}},'client':{'fixture':{'bytes':1,'sha256':'x'}},'listeners':{'18765':[],'18766':[],'8081':[]},'plan_overlap':[]}
t.scope_snapshot=lambda dests:copy.deepcopy(snapshot)
(D/'validation').mkdir()
for i,row in enumerate(rows):
    dest=Path(row['destination']);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b'old\r\n')
    src=D/('source'+str(i));src.write_bytes(('new'+str(i)).encode())
    row.update(source=str(src),baseline=sha(dest.read_bytes()),sha256=sha(src.read_bytes()))
plan=D/'install_plan.json'
def setup():
    plan.write_text(json.dumps({'files':rows}))
    pin=sha(plan.read_bytes())
    (D/'validation/final_checks.json').write_text(json.dumps({'passed':True,'plan_sha256':pin}))
    (D/'validation/review_final.json').write_text(json.dumps({'status':'PASS','plan_sha256':pin}))
setup()
atomic=t.atomic
count=[0]
def fail_second(path,raw):
    count[0]+=1
    if count[0]==2: raise RuntimeError('injected write failure')
    atomic(path,raw)
t.atomic=fail_second
check('injected transaction failure refused',lambda:refused(lambda:t.apply_plan(plan)))
check('rollback restores original bytes',lambda:eq([Path(r['destination']).read_bytes() for r in rows],[b'old\r\n']*8))
check('backup preserves CRLF bytes',lambda:eq(all(p.read_bytes()==b'old\r\n' for p in t.ROOT.rglob('*.bak_*')),True))
t.atomic=atomic
Path(rows[0]['source']).write_bytes(b'tampered')
check('changed staged bytes refused',lambda:refused(lambda:t.apply_plan(plan)))
Path(rows[0]['source']).write_bytes(b'new0')
check('offline successful transaction',lambda:eq(t.apply_plan(plan)['status'],'INSTALLED_RESTART_REQUIRED'))
check('repeat transaction refused',lambda:refused(lambda:t.apply_plan(plan)))
check('parent scripts unchanged during review',lambda:eq({n:sha((W/n).read_bytes()) for n in names},{n:pins[n] for n in names}))
for name in ('deploy_controlled.py','verify_installed.py'):
    check(name+' no old patch import',lambda name=name:eq('operational_patch' in (W/name).read_text(),False))
report={'status':'PASS_PRELIMINARY_CONTROLS_ONLY','reviewer':'codex-app-v409-review','scope':'Offline copies and current 13 preservation file hashes; no runtime changes, process controls or paid generation','tests':results,'pins':pins,'findings':[], 'pending':['Final plan and builder source/app submissions','P2 v409+v408 literal equality, uncompressed index, historical retrieval, source/statute scope and public native counts','Final review artifact with all required binding hashes; no deployment authorization from this report'], 'fixture_dir':str(D)}
out=W/'review/CONTROLS_R1.json'
with out.open('x',encoding='utf-8') as fp:json.dump(report,fp,ensure_ascii=False,indent=2)
print(json.dumps({'status':report['status'],'tests':len(results),'report':str(out)}))
