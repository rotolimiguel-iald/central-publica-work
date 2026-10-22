"""Bounded sequential suites, separate interpreters and inherited private guard."""
from pathlib import Path
import json, os, subprocess, sys, time
ROOT=Path(__file__).resolve().parent
env=os.environ.copy();env['PYTHONPATH']=str(ROOT);env['PYTHONDONTWRITEBYTECODE']='1'
records=[]
for suite in ('core','native','queue','app','jev','mcp'):
    cmd=[sys.executable,'-B','-X','utf8',str(ROOT/('tests_queue/mcp_smoke_r4.py' if suite=='mcp' else 'run_suite.py'))]
    if suite!='mcp':cmd.append(suite)
    start=time.perf_counter()
    cp=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf8',timeout=600)
    record={'suite':suite,'exit_code':cp.returncode,'seconds':time.perf_counter()-start,'stdout':cp.stdout,'stderr':cp.stderr,'command':cmd}
    out=ROOT/(suite+'_execution.json')
    with out.open('x',encoding='utf8') as f:json.dump(record,f,ensure_ascii=False,indent=2)
    records.append(record)
    print(json.dumps({k:record[k] for k in ('suite','exit_code','seconds')}),flush=True)
    if cp.returncode:print(cp.stdout[-18000:]+cp.stderr[-5000:],flush=True)
with (ROOT/'EXECUTIONS_R1.json').open('x',encoding='utf8') as f:json.dump(records,f,ensure_ascii=False,indent=2)
raise SystemExit(0 if all(x['exit_code']==0 for x in records) else 1)
