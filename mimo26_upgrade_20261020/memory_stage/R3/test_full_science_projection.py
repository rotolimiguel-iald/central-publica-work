"""Exact real public package with synthetic operational memory; no provider call."""
from pathlib import Path
import ast,hashlib,json,sys,tempfile
W=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(OUT),str(R)]
from claude_memory_package import load_package
import iald_app_memory as memory
import iald_router_media_view as view
from iald_memory import MemoryStore
package=load_package(R/'.iald_runtime/haiku',canonical_manifest=R/'iald_nucleo_fixo.json')
prefix=package.prefix
assert prefix
# Exact legacy scientific excerpt, loaded by the router's real verified source
# function, not a synthetic prefix or a guessed file path.
tree=ast.parse((W/'final_stage/iald_auto_router.py').read_bytes())
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='memory_slice')
ns=dict(ROOT=R,json=json,Path=Path,hashlib=hashlib)
exec(compile(ast.Module(body=[node],type_ignores=[]),'actual_memory_slice','exec'),ns)
canonical,canonical_source=ns['memory_slice'](R)
assert len(canonical)==8000
cases=[]
for marker in ('para','IALD','Lean','role','mimo'):
    with tempfile.TemporaryDirectory(dir=OUT) as directory:
        root=Path(directory)
        store=MemoryStore(root/'state',snapshot_archive_dir=root/'archive')
        scope={'house':'IALD_APP','principal':'synthetic_science_integrity'}
        command='Discuss literal data:image/png;base64,'+marker
        store.ensure_context('fixture',objective=command,scope=scope,actor={'id':'fixture','kind':'agent'})
        binding=memory.Binding(store,'fixture',scope,'fixture-request')
        before=binding.snapshot()
        with memory.bound(binding):
            common=view.routing_state(memory)
            body=dict(state=dict(common_memory=common,canonical_memory=canonical,request=command,
                                 role='role',protocol_IALD='IALD',ordinary_para='para',ordinary_Lean='Lean'),
                      questions={'role':'role','Lean':'Lean','IALD':'IALD','para':'para'})
            clean=view.prepare_body(body,binding)
            assert clean['state']['canonical_memory']==canonical,'Actual canonical8000 changed'
            assert clean['questions']==body['questions'],'Protocol keys or values changed'
            assert view.assert_public_body(clean,binding)
            assert 'data:image/png;base64,' not in json.dumps(clean)
            projected=memory.project_messages([{'role':'system','content':prefix},{'role':'user','content':command}])
            result=view.project_system_messages(projected)
        assert result[0]['content'].startswith(prefix),'Scientific package changed'
        assert result[-1]=={'role':'user','content':command},'Original user input changed'
        assert binding.snapshot()==before,'Original memory changed'
        cases.append({'marker':marker,'prefix_unchanged':True,'canonical8000_unchanged':True,
                      'protocol_keys_unchanged':True,'final_egress_guard_passed':True,
                      'user_input_unchanged':True,'memory_unchanged':True})
report=dict(status='PASS',package_sha256=hashlib.sha256(prefix.encode()).hexdigest(),package_chars=len(prefix),
            canonical8000_sha256=hashlib.sha256(canonical.encode()).hexdigest(),canonical_source=canonical_source,
            cases=cases,provider_calls=0,production_writes=0)
(OUT/'FULL_SCIENCE_PROJECTION_TEST.json').write_bytes(json.dumps(report,indent=2).encode())
print(json.dumps(report))
