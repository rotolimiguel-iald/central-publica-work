"""Read-only verification of the current mission through CLI and actual MCP."""
import asyncio
from fastmcp import Client
from support_e2 import *

async def main():
    tools=load_tools()
    raw=call('session_memory.py',dict(operation='get',reference=str(REF)),'LIVE_BEFORE_GET')
    p=tools['iald_mission_sync'](str(REF),max_chars=100000)
    assert p['actual_chars']<100000
    terminal=p['projection']['terminal_handles']
    active=p['projection']['flow']['handles']
    assert len(active)+len(terminal)==len(raw['p']['handles'])
    assert {h['id'] for h in active+terminal}=={h['id'] for h in raw['p']['handles']}
    by_id={h['id']:h for h in raw['p']['handles']}
    assert all(h==by_id[h['id']] for h in active)
    assert p['projection']['terminal_handles_recovery']['state_sha256']==raw['receipt']['state_sha256']
    assert p['receipt']['revision']==raw['revision']
    t=next(t for t in p['projection']['active'] if t['id']==TASK)
    arguments=dict(reference=str(REF),task_id=TASK,actor_id=ACTOR['id'],lease_id=t['lease']['id'],
                   expected_revision=p['receipt']['revision'],projection_sha256=p['projection_sha256'])
    assert tools['iald_mission_preflight'](**arguments)['ready']
    server=CENTRAL/'Chatgpt/IALD_ORQUESTRACAO_20260923/mcp_server.py'
    config={'mcpServers':{'e2':{'command':sys.executable,'args':['-B','-X','utf8',str(server)]}}}
    start=dt.datetime.now(dt.timezone.utc)
    async with Client(config,timeout=30) as client:
        discovered=await client.list_tools()
        assert {'iald_mission_sync','iald_mission_handoff','iald_mission_preflight','iald_mission_transition'} <= {t.name for t in discovered}
        synced=(await client.call_tool('iald_mission_sync',dict(reference=str(REF),max_chars=100000))).data
        handed=(await client.call_tool('iald_mission_handoff',dict(arguments,max_chars=100000))).data
        assert synced['projection']==handed['projection']==p['projection']
        assert handed['preflight']['ready']
        polled=(await client.call_tool('iald_mission_sync',dict(reference=str(REF),max_chars=100000,
                      after_revision=p['receipt']['revision'],wait_ms=0))).data
        assert polled['changed'] is False
    after=call('session_memory.py',dict(operation='get',reference=str(REF)),'LIVE_AFTER_GET')
    assert after==raw,'Concurrent state changed: refresh verification, do not claim equality'
    old_project=dict(p['projection'])
    # The size comparator is the full pre-E2 projection at this SAME snapshot.
    old_project['flow']=raw['p']
    old_project.pop('terminal_handles');old_project.pop('terminal_handles_recovery')
    old_chars=len(json.dumps(old_project,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False))
    new_chars=p['actual_chars']
    result=dict(ok=True,at=dt.datetime.now(dt.timezone.utc).isoformat(),
        seconds=(dt.datetime.now(dt.timezone.utc)-start).total_seconds(),
        candidate=pin(BASE/'mission_candidate.py'),installed=pin(CORE/'lib/iald_memory/mission.py'),
        reference=pin(REF),revision=raw['revision'],state_sha256=raw['receipt']['state_sha256'],
        full_projection_chars_same_snapshot=old_chars,compact_projection_chars=new_chars,
        reduction_chars=old_chars-new_chars,reduction_fraction=(old_chars-new_chars)/old_chars,
        terminal_handles=len(terminal),active_handles=len(active),persistent_handles=len(raw['p']['handles']),
        facts_preserved=True,state_unchanged=True,mcp_sync_equals_handoff=True,unchanged_poll=True,
        preflight=True,provider_calls=0,existing_processes_restarted=False,
        scope='Characters, not measured billed tokens. Current full get retained; terminal index only in projection.')
    new('LIVE_VERIFICATION_E2.json',result)
    print(json.dumps({k:result[k] for k in ['ok','revision','full_projection_chars_same_snapshot',
        'compact_projection_chars','reduction_fraction','terminal_handles','active_handles','state_unchanged']}))

if __name__=='__main__':asyncio.run(main())
