"""Focused regression for a real, growing mission; no production mutation."""
from pathlib import Path
import ast, asyncio, json, sys
from datetime import datetime, timezone
from fastmcp import Client
from prepare import ROOT, PARENT, BRIDGE, REF, ACTOR, TASK, new, pin, load_bridge

SERVER=PARENT.parent.parent/'Chatgpt/IALD_ORQUESTRACAO_20260923/mcp_server.py'

def expect_refusal(fn, args, fragment):
    try: fn(**args)
    except ValueError as exc:
        assert fragment in str(exc),str(exc)
        return {'refused':True,'reason':str(exc)}
    raise AssertionError('Expected refusal: '+fragment)

async def main(mode):
    assert mode in {'candidate','installed'}
    target=ROOT/'mission_bridge_candidate.py' if mode=='candidate' else BRIDGE
    tools=load_bridge(target)
    old_ast=ast.parse((PARENT/'mission_bridge.py').read_bytes())
    new_ast=ast.parse(target.read_bytes())
    def defs(tree):return {n.name:ast.dump(n,include_attributes=False) for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)}
    before,after=defs(old_ast),defs(new_ast)
    changed=sorted(k for k in before if before[k]!=after[k])
    assert changed==['iald_mission_handoff','register_tools'],changed
    p=tools['iald_mission_sync'](str(REF),max_chars=100000)
    task=next(t for t in p['projection']['active'] if t['id']==TASK)
    args={'reference':str(REF),'task_id':TASK,'actor_id':ACTOR['id'],'lease_id':task['lease']['id'],
          'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256']}
    assert p['actual_chars']>24000
    failures={
        'default_overflow':expect_refusal(tools['iald_mission_handoff'],args,'projection_overflow_required_'),
        'one_char_short':expect_refusal(tools['iald_mission_handoff'],{**args,'max_chars':p['actual_chars']-1},'projection_overflow_required_'),
        'invalid_budget':expect_refusal(tools['iald_mission_handoff'],{**args,'max_chars':255},'invalid_projection_budget'),
        'stale_revision':expect_refusal(tools['iald_mission_handoff'],{**args,'max_chars':100000,'expected_revision':0},'stale_revision_refresh_required'),
    }
    exact=tools['iald_mission_handoff'](**args,max_chars=p['actual_chars'])
    assert exact['projection']==p['projection'] and exact['preflight']['ready']
    assert exact['projection_sha256']==p['projection_sha256']
    assert exact['projection']['settled']==p['projection']['settled']
    harness=ROOT/'candidate_server.py'
    if mode=='candidate':
        new(harness.name,('''import importlib.util,runpy,sys
from pathlib import Path
root=Path(sys.argv[1]);server=Path(sys.argv[2])
sys.path.insert(0,str(server.parent))
spec=importlib.util.spec_from_file_location('iald_orchestrator.mission_bridge',root/'mission_bridge_candidate.py')
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
runpy.run_path(str(server),run_name='__main__')
''').encode('utf-8'))
        command=[str(harness),str(ROOT),str(SERVER)]
    else:command=[str(SERVER)]
    config={'mcpServers':{'large-mission':{'command':sys.executable,'args':['-B','-X','utf8',*command]}}}
    started=datetime.now(timezone.utc)
    async with Client(config,timeout=30) as client:
        discovered=await client.list_tools()
        handoff=next(t for t in discovered if t.name=='iald_mission_handoff')
        assert 'max_chars' in handoff.inputSchema['properties']
        sync=(await client.call_tool('iald_mission_sync',{'reference':str(REF),'max_chars':100000})).data
        assert sync['projection_sha256']==p['projection_sha256']
        received=(await client.call_tool('iald_mission_handoff',{**args,'max_chars':100000})).data
        assert received['projection']==sync['projection']
        assert received['preflight']['ready'] and received['reference']==str(REF)
        unchanged=(await client.call_tool('iald_mission_sync',{'reference':str(REF),'max_chars':100000,
                  'after_revision':sync['receipt']['revision'],'wait_ms':0})).data
        assert unchanged['changed'] is False
    end=datetime.now(timezone.utc)
    receipt={'ok':True,'mode':mode,'at':end.isoformat(),'seconds':(end-started).total_seconds(),
        'reference':pin(REF),'bridge':pin(target),'server':pin(SERVER),'revision':p['receipt']['revision'],
        'actual_chars':p['actual_chars'],'projection_sha256':p['projection_sha256'],
        'exact_capacity_passed':True,'mcp_schema_exposes_budget':True,'mcp_handoff_equals_sync':True,
        'unchanged_poll':True,'negative_checks':failures,
        'AST_changed_only_handoff_and_enclosing_registration':True,
        'runtime':'Existing real Runtime(recover=False) and Coordination, no mocked providers or store.',
        'provider_calls':0,'scientific_executions':0,'state_mutations':0,'existing_processes_restarted':False}
    dest=new('VERIFICATION_'+mode.upper()+'.json',receipt)
    print(json.dumps({'ok':True,'mode':mode,'chars':p['actual_chars'],'revision':p['receipt']['revision'],
                      'receipt':str(dest)},ensure_ascii=False))

if __name__=='__main__':asyncio.run(main(sys.argv[1]))
