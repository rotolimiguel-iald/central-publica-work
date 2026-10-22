import importlib.util,runpy,sys
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
