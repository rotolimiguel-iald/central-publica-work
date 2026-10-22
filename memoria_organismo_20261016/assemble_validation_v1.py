"""Assemble V exclusively from frozen staging sources and copied tests."""
from pathlib import Path
import ast, hashlib, json, os

W=Path(__file__).resolve().parent
V=W/'validation_final'
assert not V.exists(), 'Do not overwrite a validation attempt'
V.mkdir()
rows=[]
def pin(p):
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def put(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_name('.vtmp')
    with t.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==raw
    os.rename(t,p)
def copy(src,dest,changes=()):
    raw=src.read_bytes();edits=[]
    for old,new in changes:
        assert raw.count(old.encode())==1,(str(src),old,raw.count(old.encode()))
        raw=raw.replace(old.encode(),new.encode())
        edits.append({'old':old,'new':new})
    put(dest,raw)
    row={'source':pin(src),'copy':pin(dest),'adaptations':edits}
    if src.name.startswith('test_') and src.suffix=='.py':
        def assertions(data):
            tree=ast.parse(data)
            return sum(isinstance(n,ast.Assert) or (isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr.startswith('assert')) for n in ast.walk(tree))
        row['assertions_source']=assertions(src.read_bytes());row['assertions_copy']=assertions(raw)
        assert row['assertions_source']==row['assertions_copy']
    rows.append(row)
def tree(src,dest):
    for p in sorted(src.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix in ('.py','.js','.txt'):
            copy(p,dest/p.relative_to(src))
freeze=json.loads((W/'CORE_R2_SOURCE_FREEZE_R1.json').read_bytes())
assert all(pin(Path(p['path']))==p for p in freeze['files'])
for suffix in ('core','core_r2'):
    tree(W/'staging/core_r2/lib',V/f'staging/{suffix}/lib')
# A source tree with J replacement selected before copying; accepted A remains intact.
for p in sorted((W/'staging/app').rglob('*')):
    if p.is_file() and '__pycache__' not in p.parts and p.suffix in ('.py','.js'):
        rel=p.relative_to(W/'staging/app');overlay=W/'staging/app_r2'/rel
        copy(overlay if overlay.is_file() else p,V/'staging/app'/rel)
copy(W/'staging/app_r2/iald_jev_control.py',V/'staging/app/iald_jev_control.py')
for d in ('app_r2','native','queue/r3','sessions','bench_wrapper'):
    tree(W/'staging'/d,V/'staging'/d)
copy(Path(r'C:\IALD\MEMORIA_IALD\session_memory.py'),V/'staging/core/session_memory.py')
groups={
    'tests_core_r2':['test_activity.py','test_mission_regression.py','test_projection.py','mission_cli.py'],
    'tests_native':['test_native_activity.py','test_server_hooks.py'],
    'tests_queue':['test_queue_activity_r3.py','test_legacy_migration_r2.py','process_fixture_r3.py','mcp_smoke_r4.py'],
    'tests_app':['test_activity_app.py'],
    'tests_jev':['test_long_admission.py'],
}
for group,names in groups.items():
    for name in names:
        changes=[]
        if name=='test_mission_regression.py':changes=[("CORE=Path(r'C:\\IALD\\MEMORIA_IALD')","CORE=ROOT.parent/'staging/core'")]
        if name=='test_server_hooks.py':changes=[("APP = WORK/'tests_native/app_snapshot_r1'","APP = WORK/'staging/app'")]
        if name=='test_activity_app.py':changes=[('8017d2904acc2471ab2e15245a65e0802dbcdb856dd42ab992a2fad0ddb21263',pin(W/'staging/core_r2/lib/iald_memory/activity.py')['sha256'])]
        if name=='mcp_smoke_r4.py':
            # Multiple occurrence replacement has separate source-pin provenance below.
            src=W/group/name;raw=src.read_bytes()
            for old,new in [(b'test_queue_activity_r2',b'test_queue_activity_r3'),(b'process_fixture_r2',b'process_fixture_r3')]:raw=raw.replace(old,new)
            dest=V/group/name;put(dest,raw)
            rows.append({'source':pin(src),'copy':pin(dest),'adaptations':[{'kind':'fixture version paths','from':'r2','to':'r3'}]})
            continue
        copy(W/group/name,V/group/name,changes)
for p in (W/'tests_app').glob('JEV_C2_PACKET_*_R1.json'):copy(p,V/'tests_app'/p.name)
put(V/'ASSEMBLY_PROVENANCE_R1.json',(json.dumps({'status':'ASSEMBLED','source_freeze':pin(W/'CORE_R2_SOURCE_FREEZE_R1.json'),'files':rows,'production_writes':0,'test_assertions_preserved':True},ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'files':len(rows),'manifest':pin(V/'ASSEMBLY_PROVENANCE_R1.json')}))
