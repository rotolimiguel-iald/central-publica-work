"""Fresh-process REAL CLI/MCP over an explicitly private queue/store only."""
import json,os,runpy,sys
from pathlib import Path
W=Path(__file__).resolve().parents[1]
root=Path(sys.argv[2]).resolve()
assert root.is_relative_to((W/'tests_queue').resolve())
sys.path[:0]=[str(W/'staging/core/lib'),str(W/'staging/queue')]
os.environ['IALD_MEMORY_SNAPSHOT_ARCHIVE_DIR']=str(root/'archives')
from iald_orchestrator import runtime,providers
Real=runtime.Runtime
class PrivateRuntime(Real):
    def __init__(self,*args,**kwargs):
        super().__init__(root/'queue',recover=False,memory_root=root/'memory')
    def source_status(self):return {'ok':True}
runtime.Runtime=PrivateRuntime
def prohibited(*args,**kwargs):raise AssertionError('NO PROVIDER OR HTTP IN PROCESS SMOKE')
providers.execute=prohibited
import urllib.request
urllib.request.urlopen=prohibited
mode=sys.argv[1]
if mode=='transport':runpy.run_path(str(W/'staging/queue/transport_cli.py'),run_name='__main__')
elif mode=='session':runpy.run_path(str(W/'staging/sessions/queue_activity_session.py'),run_name='__main__')
elif mode=='mcp':runpy.run_path(str(W/'staging/queue/mcp_server.py'),run_name='__main__')
else:raise ValueError('Unknown private fixture')
