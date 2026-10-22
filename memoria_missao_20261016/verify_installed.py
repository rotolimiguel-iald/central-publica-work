"""Read-only smoke test of installed MCP tools, using the actual current mission."""
from pathlib import Path
import asyncio, hashlib, json, sys
from datetime import datetime, timezone
from fastmcp import Client
from activate import ROOT, REF, pin, save

async def main():
    deploy=json.loads((ROOT/'DEPLOYMENT.json').read_bytes())
    checked=[]
    for row in deploy['files']:
        current=pin(row['target'])
        assert current['sha256']==row['new_sha256'],row['target']
        checked.append(current)
    server=ROOT.parent.parent/'Chatgpt/IALD_ORQUESTRACAO_20260923/mcp_server.py'
    config={'mcpServers':{'installed-mission':{'command':sys.executable,'args':['-B','-X','utf8',str(server)]}}}
    started=datetime.now(timezone.utc)
    async with Client(config,timeout=30) as client:
        names=sorted(t.name for t in await client.list_tools())
        required=['iald_mission_sync','iald_mission_preflight','iald_mission_transition','iald_mission_handoff']
        assert set(required)<=set(names)
        result=(await client.call_tool('iald_mission_sync',{'reference':str(REF),'max_chars':24000})).data
        initial=json.loads((ROOT/'FECHO_INITIAL_PROJECT_RECEIPT.json').read_bytes())['result']
        assert result['projection_sha256']==initial['projection_sha256']
        poll=(await client.call_tool('iald_mission_sync',{'reference':str(REF),
              'after_revision':result['receipt']['revision'],'wait_ms':0,'max_chars':24000})).data
        assert poll['changed'] is False
    ended=datetime.now(timezone.utc)
    receipt={'ok':True,'start':started.isoformat(),'end':ended.isoformat(),
       'seconds':(ended-started).total_seconds(),'installed_files':checked,'server':pin(server),
       'new_tools':required,'all_tools':names,'reference':pin(REF),'revision':result['receipt']['revision'],
       'projection_sha256':result['projection_sha256'],'projection_chars':result['actual_chars'],
       'checks':['installed_hashes','actual_stdio_discovery','own_mission_sync','matches_fresh_CLI','unchanged_poll'],
       'runtime':'Actual installed Runtime(recover=False) and Coordination; no stubs.',
       'provider_calls':0,'existing_processes_restarted':False,'actions_called':['list_tools','iald_mission_sync'],
       'limitation':'New process smoke test. Existing Codex MCP sessions were not reloaded.'}
    save('INSTALLED_MCP_VERIFICATION.json',receipt)
    print(json.dumps({'ok':True,'new_tools':required,'chars':result['actual_chars'],'seconds':receipt['seconds']}))

if __name__=='__main__':asyncio.run(main())
