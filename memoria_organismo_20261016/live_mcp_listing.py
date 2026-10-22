"""Inspect one new installed MCP stdio process; never dispatch a task."""
import json,queue,subprocess,threading,time
from pathlib import Path
from mission_io import WORK,save,pin
server=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\mcp_server.py')
path=WORK/'live_validation/MCP_INSTALLED_R1.json'
if path.exists():raise SystemExit('Existing evidence; do not repeat')
start=time.monotonic();errors=[];responses=queue.Queue()
p=subprocess.Popen([r'C:\Python314\python.exe','-B','-X','utf8',str(server)],
    stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8')
def read():
    for line in p.stdout:
        try:responses.put(json.loads(line))
        except ValueError:responses.put({'invalid_stdout':True})
def err():
    for line in p.stderr:
        # Keep only error types/counts; no arbitrary runtime content in the report.
        errors.append(line)
threading.Thread(target=read,daemon=True).start();threading.Thread(target=err,daemon=True).start()
def call(msg,wait=True):
    p.stdin.write(json.dumps(msg)+'\n');p.stdin.flush()
    if not wait:return
    deadline=time.monotonic()+25
    while time.monotonic()<deadline:
        x=responses.get(timeout=max(.1,deadline-time.monotonic()))
        if x.get('id')==msg['id']:return x
    raise TimeoutError('MCP response')
try:
    r=call({'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-03-26','capabilities':{},'clientInfo':{'name':'IALD installation verifier','version':'1'}}})
    assert 'result' in r
    call({'jsonrpc':'2.0','method':'notifications/initialized'},False)
    r=call({'jsonrpc':'2.0','id':2,'method':'tools/list','params':{}})
    names=sorted(t['name'] for t in r['result']['tools'])
    new=[n for n in names if n.startswith(('iald_activity_','iald_bench_activity_'))]
    assert len(new)==7
    p.stdin.close();p.wait(timeout=15);assert p.returncode==0
    save(path,{'status':'PASS','new_tools':new,'tool_count':len(names),'tools':names,
        'source':pin(server),'seconds':time.monotonic()-start,'exit':p.returncode,
        'existing_processes_reloaded':False,'tool_calls':0,'stderr_lines':len(errors)})
except Exception as e:
    if p.poll() is None:p.terminate();p.wait(timeout=10)
    save(path,{'status':'FAILED','error_type':type(e).__name__,'exit':p.returncode,
        'seconds':time.monotonic()-start,'stderr_lines':len(errors),'repeated':False})
print(json.dumps({'evidence':pin(path)}))
