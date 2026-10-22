"""One real stdio MCP process, private stores, prohibited HTTP/providers."""
import hashlib,json,os,queue,subprocess,sys,threading,time,traceback,uuid
from pathlib import Path
from test_queue_activity_r2 import QueueActivityTests,W,qa

def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def save(path,value):
    raw=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
    tmp=path.with_name(path.name+'.tmp_'+uuid.uuid4().hex)
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    os.rename(tmp,path)

case=QueueActivityTests();case.setUp();process=None
log=[];checks=[];start=time.monotonic()
report=W/'tests_queue/MCP_STDIO_RESULT_R4.json'
try:
    task=case.task();expected=qa.describe(case.rt,'task',task['id']);before=case.state(task)
    cmd=[sys.executable,'-B','-X','utf8',str(W/'tests_queue/process_fixture_r2.py'),'mcp',str(case.root)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',bufsize=1)
    received=queue.Queue();errors=[]
    def output():
        for line in process.stdout:
            log.append({'stdout':line.rstrip()})
            try:received.put(json.loads(line))
            except ValueError:received.put({'invalid_stdout':line})
    def stderr():
        for line in process.stderr:errors.append(line.rstrip())
    threads=[threading.Thread(target=output,daemon=True),threading.Thread(target=stderr,daemon=True)]
    for t in threads:t.start()
    def call(message,expected_id):
        process.stdin.write(json.dumps(message)+'\n');process.stdin.flush()
        if expected_id is None:return
        end=time.monotonic()+45
        while time.monotonic()<end:
            answer=received.get(timeout=max(.1,end-time.monotonic()))
            if answer.get('id')==expected_id:return answer
        raise TimeoutError('MCP stdio response timeout')
    init=call({'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-03-26','capabilities':{},'clientInfo':{'name':'Q-private-review','version':'1'}}},1)
    assert 'result' in init,init;checks.append('initialize real stdio')
    call({'jsonrpc':'2.0','method':'notifications/initialized'},None)
    listing=call({'jsonrpc':'2.0','id':2,'method':'tools/list','params':{}},2)
    tools=listing['result']['tools'];names={t['name'] for t in tools}
    assert {'iald_mission_sync','iald_mission_preflight','iald_mission_handoff','iald_mission_transition'}<=names,names
    checks.append('four existing mission tools preserved')
    new={n for n in names if n.startswith('iald_activity_') or n.startswith('iald_bench_activity_')}
    assert len(new)==7,new
    for tool in tools:
        if tool['name'] in new:
            assert not {'actor','scope','path','evidence','review_evidence','ticket','url'} & set(tool['inputSchema']['properties'])
    checks.append('seven tools expose ledger IDs only')
    answer=call({'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'iald_activity_project','arguments':{'entity_kind':'task','entity_id':task['id'],'max_chars':125000}}},3)
    result=answer['result'];assert not result.get('isError'),answer
    value=result.get('structuredContent')
    if value is None:value=json.loads(next(c['text'] for c in result['content'] if c['type']=='text'))
    assert value==expected,(value.keys(),expected.keys());checks.append('same exact current private projection as Python')
    overflow=call({'jsonrpc':'2.0','id':4,'method':'tools/call','params':{'name':'iald_activity_project','arguments':{'entity_kind':'task','entity_id':task['id'],'max_chars':256}}},4)
    assert overflow.get('error') or overflow['result'].get('isError'),overflow
    checks.append('mandatory projection overflow refused')
    assert case.state(task)==before;checks.append('project does not mutate revision/state')
    process.stdin.close();process.wait(timeout=15)
    assert process.returncode==0,process.returncode;checks.append('own private process clean EOF exit')
    save(report,{'verdict':'PASS','checks':checks,'tool_count':len(tools),'new_tools':sorted(new),
        'process_id':process.pid,'command':cmd,'exit_code':process.returncode,'seconds':time.monotonic()-start,
        'fixture':pin(W/'tests_queue/process_fixture_r2.py'),'provider_calls':0,'real_bench_http_calls':0,
        'state_scope':'private queue/store only; no assertion about already-running MCP processes',
        'stderr':errors,'source':pin(Path(__file__))})
except BaseException as exc:
    if process and process.poll() is None:process.terminate();process.wait(timeout=15)
    save(report,{'verdict':'FAIL','checks':checks,'error':repr(exc),'traceback':traceback.format_exc(),
        'own_process_id':process.pid if process else None,'log':log,'stderr':errors if process else []})
    raise
finally:
    case.tearDown()
print(json.dumps({'report':pin(report),'checks':checks},ensure_ascii=False))
