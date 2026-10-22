"""Authorized local stdio smoke: allow Windows internal loopback IPC, no remote network."""
from pathlib import Path
import json, os, subprocess, sys, time
V=Path(__file__).resolve().parent
source=V/'tests_queue/mcp_smoke_v2.py'
target=V/'tests_queue/mcp_smoke_v3.py'
raw=source.read_bytes().replace(b'MCP_STDIO_RESULT_V2.json',b'MCP_STDIO_RESULT_V3.json')
with target.open('xb') as f:f.write(raw)
env=os.environ.copy();env['PYTHONPATH']=str(V/'guard_r2');env['PYTHONDONTWRITEBYTECODE']='1'
start=time.perf_counter()
cp=subprocess.run([sys.executable,'-B','-X','utf8',str(target)],env=env,cwd=V,capture_output=True,text=True,encoding='utf8',timeout=100)
report={'exit_code':cp.returncode,'seconds':time.perf_counter()-start,'stdout':cp.stdout,'stderr':cp.stderr,
 'reason':'Sandboxed Windows socketpair stopped at accept, proven in SOCKETPAIR_DIAGNOSTIC_R1. Private audit guard retained. Only local stdio test process; no providers or production writes.'}
with (V/'mcp_execution_r3.json').open('x',encoding='utf8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
print(json.dumps(report));raise SystemExit(cp.returncode)
