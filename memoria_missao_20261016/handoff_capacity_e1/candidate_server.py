import importlib.util,runpy,sys
from pathlib import Path
root=Path(sys.argv[1]);server=Path(sys.argv[2])
sys.path.insert(0,str(server.parent))
spec=importlib.util.spec_from_file_location('iald_orchestrator.mission_bridge',root/'mission_bridge_candidate.py')
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
runpy.run_path(str(server),run_name='__main__')
