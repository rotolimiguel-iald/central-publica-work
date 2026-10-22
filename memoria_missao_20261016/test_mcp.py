"""Actual MCP stdio in a new process, with existing queue runtime replaced by inert stubs."""
from pathlib import Path
import ast, asyncio, hashlib, json, shutil, sys, tempfile
from fastmcp import Client
ROOT=Path(__file__).resolve().parent
BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
STAGE=ROOT/'stage'
sys.path.insert(0,str(STAGE/'lib'))
from iald_memory import MemoryStore
from iald_memory.mission import MissionController


async def main():
    raw=(BASE/'mcp_server.py').read_bytes()
    addition=b'from iald_orchestrator.mission_bridge import register_tools as register_mission_tools\nregister_mission_tools(server)\n\n\n'
    marker=b'if __name__ == "__main__":'
    assert raw.count(marker)==1
    candidate=raw.replace(marker,addition+marker)
    (ROOT/'mcp_server_candidate.py').write_bytes(candidate)
    def functions(b):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(b).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    assert functions(raw)==functions(candidate)
    shutil.copy2(ROOT/'mission.py',STAGE/'lib'/'iald_memory'/'mission.py')
    shutil.copy2(ROOT/'mission_cli.py',STAGE/'mission_cli.py')
    shutil.copy2(Path(r'C:\IALD\MEMORIA_IALD\session_memory.py'),STAGE/'session_memory.py')
    with tempfile.TemporaryDirectory(prefix='mcp_test_',dir=ROOT) as temp:
        p=Path(temp);store=MemoryStore(p/'state');scope={'house':'IALD','principal':'mcp-test'}
        actor={'id':'builder','kind':'agent'}
        snap=store.ensure_context('mcp-test',objective='Synthetic MCP integration',scope=scope,actor=actor)
        ref=p/'REFERENCE.json';ref.write_text(json.dumps({'protocol':'iald-memory-session/v1','store':str(p/'state'),
            'context_id':'mcp-test','scope':scope,'objective_sha256':snap['objective_sha256']}),encoding='utf-8')
        evidence=p/'source.txt';evidence.write_bytes(b'synthetic pinned input')
        pin={'path':str(evidence),'sha256':hashlib.sha256(evidence.read_bytes()).hexdigest()}
        harness=p/'server.py'
        harness.write_text('''import importlib.util,runpy,sys,types
from pathlib import Path
root=Path(sys.argv[1]);state=Path(sys.argv[2])
package=types.ModuleType('iald_orchestrator');package.__path__=[];sys.modules[package.__name__]=package
for name,attribute in [('runtime','Runtime'),('coordination','Coordination')]:
    module=types.ModuleType('iald_orchestrator.'+name);setattr(module,attribute,lambda *a,**k:object());sys.modules[module.__name__]=module
spec=importlib.util.spec_from_file_location('iald_orchestrator.mission_bridge',root/'mission_bridge.py')
bridge=importlib.util.module_from_spec(spec);sys.modules[spec.name]=bridge;spec.loader.exec_module(bridge)
original_run=bridge.subprocess.run
def run(args,**kwargs):
    args=[*args[:4],str(root/'stage'/'mission_cli.py'),'--store',str(state)]
    return original_run(args,**kwargs)
bridge.subprocess.run=run
runpy.run_path(str(root/'mcp_server_candidate.py'),run_name='__main__')
''',encoding='utf-8')
        config={'mcpServers':{'mission-test':{'command':sys.executable,'args':['-B','-X','utf8',str(harness),str(ROOT),str(p/'state')]}}}
        async with Client(config,timeout=20) as client:
            names={t.name for t in await client.list_tools()}
            needed={'iald_mission_sync','iald_mission_preflight','iald_mission_transition','iald_mission_handoff'}
            assert needed<=names
            async def call(name,args):
                r=await client.call_tool(name,args)
                return r.data
            req={'operation':'configure','reference':str(ref),'expected_revision':0,'event_id':'cfg','actor':actor,
                 'requirements':[{'id':'A','criterion':'Test real stdio','depends_on':[]}],'sources':[pin]}
            await call('iald_mission_transition',{'request':req})
            v=await call('iald_mission_sync',{'reference':str(ref)})
            req.update(operation='claim',expected_revision=v['receipt']['revision'],projection_sha256=v['projection_sha256'],task_id='A',event_id='claim')
            claim=await call('iald_mission_transition',{'request':req})
            v=await call('iald_mission_sync',{'reference':str(ref)})
            args={'reference':str(ref),'task_id':'A','actor_id':'builder','lease_id':claim['task']['lease']['id'],
                  'expected_revision':v['receipt']['revision'],'projection_sha256':v['projection_sha256']}
            check=await call('iald_mission_preflight',args);assert check['ready']
            handoff=await call('iald_mission_handoff',args);assert handoff['projection']['objective']=='Synthetic MCP integration'
            unchanged=await call('iald_mission_sync',{'reference':str(ref),'after_revision':v['receipt']['revision']})
            assert unchanged['changed'] is False
            args['expected_revision']=0
            bad=await client.call_tool('iald_mission_preflight',args,raise_on_error=False)
            assert bad.is_error
        return {'ok':True,'transport':'new_process_stdio','new_tools':sorted(needed),'total_tools':len(names),
                'existing_function_AST_identical':True,'assertions':['discover','configure','claim','sync','preflight','handoff','unchanged_poll','stale_refused'],
                'runtime_stub':'Existing queue Runtime and Coordination are inert in this test; mission CLI/store are real isolated processes.'}

if __name__=='__main__':print(json.dumps(asyncio.run(main()),ensure_ascii=False))
