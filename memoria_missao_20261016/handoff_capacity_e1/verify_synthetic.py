"""One large isolated mission through the actual MCP transport and memory CLI."""
from pathlib import Path
import asyncio, hashlib, json, sys
from fastmcp import Client
from prepare import ROOT, CORE, new, pin
sys.path.insert(0,str(CORE/'lib'))
from iald_memory import MemoryStore
from iald_memory.mission import MissionController

async def main():
    area=ROOT/'synthetic'
    area.mkdir(exist_ok=False)
    state=area/'state';scope={'house':'IALD','principal':'synthetic-handoff-e1'}
    actor={'id':'synthetic-builder','kind':'agent'};cid='synthetic-handoff-e1'
    store=MemoryStore(state)
    snap=store.ensure_context(cid,objective='Synthetic large mission: preserve all eight requirements.',scope=scope,actor=actor)
    ref=area/'REFERENCE.json'
    ref.write_text(json.dumps({'protocol':'iald-memory-session/v1','store':str(state),'context_id':cid,
        'scope':scope,'objective_sha256':snap['objective_sha256']}),encoding='utf-8')
    evidence=area/'source.txt';evidence.write_bytes(b'Synthetic fixture; no science or production data.')
    ctl=MissionController(store,cid,scope)
    requirements=[{'id':f'A{i}','criterion':f'Unique requirement {i}: '+('keep this clause; '*260),'depends_on':[]} for i in range(8)]
    ctl.action({'operation':'configure','expected_revision':0,'event_id':'configure','actor':actor,
                'requirements':requirements,'sources':[pin(evidence)]})
    p=ctl.project(100000)
    claim=ctl.action({'operation':'claim','expected_revision':p['receipt']['revision'],
        'projection_sha256':p['projection_sha256'],'event_id':'claim','actor':actor,'task_id':'A0'})
    p=ctl.project(100000);assert p['actual_chars']>24000
    harness=new('synthetic_server.py',b'''import importlib.util,runpy,sys
from pathlib import Path
root=Path(sys.argv[1]);state=Path(sys.argv[2]);server=Path(sys.argv[3])
sys.path.insert(0,str(server.parent))
spec=importlib.util.spec_from_file_location('iald_orchestrator.mission_bridge',root/'mission_bridge_candidate.py')
bridge=importlib.util.module_from_spec(spec);sys.modules[spec.name]=bridge;spec.loader.exec_module(bridge)
original_run=bridge.subprocess.run
def isolated_run(args,**kwargs):
    return original_run([*args,'--store',str(state)],**kwargs)
bridge.subprocess.run=isolated_run
runpy.run_path(str(server),run_name='__main__')
''')
    server=ROOT.parent.parent.parent/'Chatgpt/IALD_ORQUESTRACAO_20260923/mcp_server.py'
    config={'mcpServers':{'synthetic':{'command':sys.executable,'args':['-B','-X','utf8',str(harness),str(ROOT),str(state),str(server)]}}}
    async with Client(config,timeout=30) as client:
        sync=(await client.call_tool('iald_mission_sync',{'reference':str(ref),'max_chars':100000})).data
        args={'reference':str(ref),'task_id':'A0','actor_id':actor['id'],'lease_id':claim['task']['lease']['id'],
            'expected_revision':sync['receipt']['revision'],'projection_sha256':sync['projection_sha256'],'max_chars':100000}
        handoff=(await client.call_tool('iald_mission_handoff',args)).data
        assert handoff['projection']==sync['projection']==p['projection']
        assert handoff['projection']['objective']==snap['objective']
        assert len(handoff['projection']['active'])==8
    dest=new('SYNTHETIC_MCP.json',{'ok':True,'bridge':pin(ROOT/'mission_bridge_candidate.py'),
        'test':pin(Path(__file__)),'chars':p['actual_chars'],'requirements':8,
        'sync_handoff_exact_match':True,'reference':pin(ref),'store_scope':scope,
        'provider_calls':0,'production_store_mutations':0,
        'transport':'New process MCP; real CLI/controller with --store pointing to isolated synthetic state.'})
    print(json.dumps({'ok':True,'chars':p['actual_chars'],'receipt':str(dest)}))

if __name__=='__main__':asyncio.run(main())
