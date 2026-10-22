"""Custody and minimal MCP correction; no provider or science execution."""
from pathlib import Path
import hashlib, importlib.util, json, os, subprocess, sys, uuid
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
CORE = Path(r'C:\IALD\MEMORIA_IALD')
REF = PARENT/'FECHO_MISSION_REFERENCE.json'
ACTOR = {'id':'codex-gerente-tgl','kind':'agent'}
OUT = PARENT.parent.parent/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
BRIDGE = PARENT.parent.parent/'Chatgpt/IALD_ORQUESTRACAO_20260923/iald_orchestrator/mission_bridge.py'
TASK = 'M1_HANDOFF_CAPACITY'

def new(name, value):
    path=ROOT/name
    raw=value if isinstance(value,bytes) else (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    if path.exists(): raise FileExistsError(path)
    tmp=path.with_name(path.name+'.tmp_'+uuid.uuid4().hex)
    with tmp.open('xb') as f:
        f.write(raw);f.flush();os.fsync(f.fileno())
    assert tmp.stat().st_size==len(raw)
    tmp.rename(path)
    return path

def pin(path):
    p=Path(path).resolve()
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def source(path):
    p=pin(path)
    return {'kind':'artifact','ref':p['path'],'sha256':p['sha256']}

def call(cli,request,name):
    new(name+'_REQUEST.json',request)
    r=subprocess.run([sys.executable,'-B','-X','utf8',str(CORE/cli)],
        input=json.dumps(request,ensure_ascii=False),capture_output=True,text=True,encoding='utf-8')
    j=json.loads(r.stdout);new(name+'_RECEIPT.json',j)
    if r.returncode or not j.get('ok'):raise RuntimeError(j)
    return j['result']

def project(name):
    return call('mission_cli.py',{'operation':'project','reference':str(REF),'max_chars':100000},name)

def base(p):
    return {'reference':str(REF),'actor':ACTOR,'expected_revision':p['receipt']['revision'],
            'projection_sha256':p['projection_sha256']}

def load_bridge(path):
    spec=importlib.util.spec_from_file_location('tested_mission_bridge',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    class Registry:
        def __init__(self):self.tools={}
        def tool(self):
            def add(fn):self.tools[fn.__name__]=fn;return fn
            return add
    registry=Registry();module.register_tools(registry)
    return registry.tools

def main():
    p=project('INITIAL')
    start=OUT/'orbital_rotation/attempts/20261016T130457_992603Z/START_RECEIPT.json'
    handle_id='build-20261016T130457_992603Z'
    flow=dict(p['projection']['flow'])
    assert handle_id not in {h['id'] for h in flow['handles']}
    start_value=json.loads(start.read_bytes())
    flow['handles']=[*flow['handles'],{'id':handle_id,'task_id':'R7','kind':'lean_prefix_probe',
        'name':'R7SineWindowPrefixProbeR1','status':'running','pid_at_start':start_value['pid'],
        'no_repeat':True,'start_receipt':pin(start)}]
    flow.update(phase='memory_handoff_capacity_correction',next_action='Correct and independently review MCP handoff capacity before new science; preserve existing running builds.')
    call('session_memory.py',{'operation':'transition','reference':str(REF),'actor':ACTOR,
        'expected_revision':p['receipt']['revision'],'event_id':'memory-e1-prefix-handle-custody',
        'changes':{'records':[{'id':'memory-e1-prefix-handle-custody','kind':'fact','statute':'REAL',
            'text':'Recovered the exact already-started prefix-probe handle after resumption. No restart. Scientific work waits for the concrete MCP handoff correction.',
            'sources':[source(start)]}],'flow':flow}},'HANDLE')
    p=project('BEFORE_EXTEND')
    r7=next(t for t in p['projection']['active'] if t['id']=='R7')
    args={'reference':str(REF),'task_id':'R7','actor_id':ACTOR['id'],
          'lease_id':r7['lease']['id'],'expected_revision':p['receipt']['revision'],
          'projection_sha256':p['projection_sha256']}
    before=load_bridge(BRIDGE)
    assert before['iald_mission_preflight'](**args)['ready']
    try:
        before['iald_mission_handoff'](**args)
    except ValueError as exc:
        assert 'projection_overflow_required_' in str(exc),str(exc)
        finding=new('FINDING.json',{'at':datetime.now(timezone.utc).isoformat(),'statute':'REAL',
            'bridge':pin(BRIDGE),'reference':pin(REF),'revision':p['receipt']['revision'],
            'actual_chars':p['actual_chars'],'error':str(exc),
            'cause':'MCP handoff has no max_chars argument; CLI defaults to 24000. The current mission passes preflight but cannot be handed off.',
            'prior_work_reused':['ACOM mission controller','four installed MCP tools','map route infra.memoria_missao.ancoragem_e_poda_20261016'],
            'no_provider_calls':True,'no_new_science':True})
    else: raise AssertionError('Expected large-mission failure was not reproduced')
    call('mission_cli.py',{**base(p),'operation':'extend','event_id':'memory-e1-handoff-extend',
        'requirements':[{'id':TASK,'criterion':'Expose and forward the same explicit projection budget in MCP handoff; refuse insufficient/invalid budgets without truncation. Verify current mission and large synthetic mission over real MCP; independent review, byte backups and additive custody.',
                         'depends_on':['M0_MEMORIA']}],
        'reason':'Concrete handoff failure on the current mission after growth beyond 24000 characters.',
        'sources':[pin(finding)]},'EXTEND')
    p=project('BEFORE_CLAIM')
    call('mission_cli.py',{**base(p),'operation':'claim','task_id':TASK,'event_id':'memory-e1-handoff-claim',
                         'lease_seconds':7200},'CLAIM')
    p=project('BEFORE_EDIT');task=next(t for t in p['projection']['active'] if t['id']==TASK)
    call('mission_cli.py',{**base(p),'operation':'check','task_id':TASK,'lease_id':task['lease']['id']},'PREFLIGHT')
    raw=BRIDGE.read_bytes()
    old=b'def iald_mission_handoff(reference: str, task_id: str, actor_id: str, lease_id: str, expected_revision: int, projection_sha256: str) -> dict:'
    changed=old.replace(b') -> dict:',b', max_chars: int = 24000) -> dict:')
    assert raw.count(old)==1
    raw=raw.replace(old,changed)
    old_req=b"'lease_id':lease_id,'expected_revision':expected_revision,'projection_sha256':projection_sha256}"
    new_req=b"'lease_id':lease_id,'expected_revision':expected_revision,'projection_sha256':projection_sha256,\n            'max_chars':max_chars}"
    assert raw.count(old_req)==1
    raw=raw.replace(old_req,new_req)
    new('mission_bridge_candidate.py',raw)
    new('PROTOCOL_ADDENDUM.md',b'\n\n## 16/10/2026 - Handoff capacity correction\n\nThe MCP `iald_mission_handoff` accepts `max_chars`, as sync does. Pass the same explicit budget to both (for example 100000 for the current mission). The default remains 24000 for compatibility. Insufficient or invalid capacity is refused without truncation; refresh revision and projection before retrying. A larger capacity does not require printing the full packet into coordinator output: retain the complete receipt and expose only the relevant result summary. Existing processes need reload; the absolute CLI works immediately.\n')
    print(json.dumps({'ok':True,'task':TASK,'revision':p['receipt']['revision'],'finding':str(finding)}))

if __name__=='__main__':main()
