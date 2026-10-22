"""Verify E3 via fresh CLI and the existing MCP server, without changing state."""
import asyncio, copy
from fastmcp import Client
from support_e3 import *

def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,
        separators=(',',':'),allow_nan=False).encode('utf-8')).hexdigest()

async def main():
    assert pin(BASE/'mission_candidate_r2.py')['sha256']==pin(CORE/'lib/iald_memory/mission.py')['sha256'], 'Installed code differs from reviewed candidate'
    tools=load_tools()
    before=call('session_memory.py',dict(operation='get',reference=str(REF)),'LIVE_BEFORE_GET')
    p=tools['iald_mission_sync'](str(REF),max_chars=100000)
    b=p['projection']
    records=[r for r in before['q']['records'] if not (
        r.get('kind')=='fact' and r.get('statute')=='REAL' and
        'iald_mission_state_v1' in r.get('meta',{}))]
    index=b['terminal_build_records']
    by_id={r['id']:r for r in records}
    assert len(by_id)==len(records),'Duplicate record id in live state'
    assert len(b['current_records'])+len(index)==len(records)
    assert {r['id'] for r in b['current_records']+index}==set(by_id)
    assert all(r==by_id[r['id']] for r in b['current_records'])
    assert all(r['record_sha256']==digest(by_id[r['id']]) for r in index)
    recovery=b['terminal_build_records_recovery']
    assert recovery['revision']==before['revision']
    assert recovery['state_sha256']==before['receipt']['state_sha256']
    assert p['receipt']['revision']==before['revision']
    task=next(t for t in b['active'] if t['id']==TASK)
    arguments=dict(reference=str(REF),task_id=TASK,actor_id=ACTOR['id'],
        lease_id=task['lease']['id'],expected_revision=p['receipt']['revision'],
        projection_sha256=p['projection_sha256'])
    assert tools['iald_mission_preflight'](**arguments)['ready']
    server=CENTRAL/'Chatgpt/IALD_ORQUESTRACAO_20260923/mcp_server.py'
    config={'mcpServers':{'e3':{'command':sys.executable,
        'args':['-B','-X','utf8',str(server)]}}}
    start=dt.datetime.now(dt.timezone.utc)
    async with Client(config,timeout=30) as client:
        listed=await client.list_tools()
        assert {'iald_mission_sync','iald_mission_handoff','iald_mission_preflight',
            'iald_mission_transition'} <= {t.name for t in listed}
        synced=(await client.call_tool('iald_mission_sync',
            dict(reference=str(REF),max_chars=100000))).data
        handed=(await client.call_tool('iald_mission_handoff',
            dict(arguments,max_chars=100000))).data
        assert synced['projection']==handed['projection']==b
        assert handed['preflight']['ready']
        polled=(await client.call_tool('iald_mission_sync',dict(reference=str(REF),
            max_chars=100000,after_revision=p['receipt']['revision'],wait_ms=0))).data
        assert polled['changed'] is False
    after=call('session_memory.py',dict(operation='get',reference=str(REF)),'LIVE_AFTER_GET')
    assert after==before,'Concurrent state changed: recover before repeating verification'
    old=copy.deepcopy(b)
    old['current_records']=records
    old.pop('terminal_build_records');old.pop('terminal_build_records_recovery')
    old_chars=len(json.dumps(old,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False))
    result=dict(ok=True,at=dt.datetime.now(dt.timezone.utc).isoformat(),
        seconds=(dt.datetime.now(dt.timezone.utc)-start).total_seconds(),
        candidate=pin(BASE/'mission_candidate_r2.py'),installed=pin(CORE/'lib/iald_memory/mission.py'),
        reference=pin(REF),revision=before['revision'],state_sha256=before['receipt']['state_sha256'],
        full_projection_chars_same_snapshot=old_chars,compact_projection_chars=p['actual_chars'],
        reduction_chars=old_chars-p['actual_chars'],reduction_fraction=(old_chars-p['actual_chars'])/old_chars,
        indexed_mechanical_records=len(index),visible_records=len(b['current_records']),
        persistent_records=len(records),state_unchanged=True,records_preserved_in_get=True,
        visible_records_byte_equivalent=True,mcp_sync_equals_handoff=True,unchanged_poll=True,
        preflight=True,provider_calls=0,existing_processes_restarted=False,
        scope='Exact legacy mechanical build records only. Characters, not billed tokens. No science acceptance.')
    new('LIVE_VERIFICATION_E3.json',result)
    print(json.dumps({k:result[k] for k in ['ok','revision','full_projection_chars_same_snapshot',
        'compact_projection_chars','reduction_fraction','indexed_mechanical_records','state_unchanged']}))

if __name__=='__main__':asyncio.run(main())
