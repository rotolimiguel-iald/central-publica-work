"""Exact real public package with synthetic operational memory; no provider call."""
from pathlib import Path
import hashlib,json,sys,tempfile
W=Path(__file__).parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(W/'final_stage'),str(R)]
from claude_memory_package import load_package
import iald_app_memory as memory
import iald_router_media_view as view
from iald_memory import MemoryStore
package=load_package(R/'.iald_runtime/haiku',canonical_manifest=R/'iald_nucleo_fixo.json')
prefix=package.prefix
assert prefix
cases=[]
for marker in ('Lean','mimo','para','IALD'):
    with tempfile.TemporaryDirectory(dir=W/'test_temp') as directory:
        root=Path(directory)
        store=MemoryStore(root/'state',snapshot_archive_dir=root/'archive')
        scope={'house':'IALD_APP','principal':'synthetic_science_integrity'}
        command='Discuss literal data:image/png;base64,'+marker
        store.ensure_context('fixture',objective=command,scope=scope,actor={'id':'fixture','kind':'agent'})
        binding=memory.Binding(store,'fixture',scope,'fixture-request')
        before=binding.snapshot()
        with memory.bound(binding):
            projected=memory.project_messages([{'role':'system','content':prefix},{'role':'user','content':command}])
            result=view.project_system_messages(projected)
        assert result[0]['content'].startswith(prefix),'Scientific package changed'
        assert result[-1]=={'role':'user','content':command},'Original user input changed'
        assert binding.snapshot()==before,'Original memory changed'
        cases.append({'marker':marker,'prefix_unchanged':True,'user_input_unchanged':True,'memory_unchanged':True})
report=dict(status='PASS',package_sha256=hashlib.sha256(prefix.encode()).hexdigest(),package_chars=len(prefix),
            cases=cases,provider_calls=0,production_writes=0)
(W/'FULL_SCIENCE_PROJECTION_TEST.json').write_bytes(json.dumps(report,indent=2).encode())
print(json.dumps(report))
