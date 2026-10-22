from pathlib import Path
import ast,datetime,hashlib,json,os
REV=Path(__file__).resolve().parent
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def write_new(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    q=p.with_name(p.name+'.tmp_'+stamp)
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;os.replace(q,p)
runs=sorted(REV.glob('right_fixed_graph_independent_*'))
assert len(runs)==1 and not (runs[0]/'compilation.json').exists()
failure={'stage':'DEPENDENCY_CATALOG_PREPARATION_BEFORE_LEAN','error':'AssertionError: TGLExt.ClosedAntilinearStandardSubspace','lean_invoked':False,'author_source_defect':False,'recovery':'Reuse independent compilation closed_antilinear_dependency_independent_20260912_095836_800005 after pins checks; no recompile.'}
write_new(runs[0]/'preparation_failure.json',(json.dumps(failure,indent=2)+'\n').encode())
p=REV/'run_right_fixed_graph_review.py';old=p.read_bytes();text=old.decode()
insert='''generic_origin=REV/'closed_antilinear_dependency_independent_20260912_095836_800005'
gm=load(generic_origin/'manifest.json');gc=load(generic_origin/'compilation.json')
assert gc['complete'] and gc['all_exit_zero'] and gc['all_axioms_allowed'] and gc['source_unchanged']
assert gm['compiler_sha256']==m['compiler_sha256'] and gm['lean_path'].split(os.pathsep)[1:]==pkg
gr=gc['records'][0];gx=gm['sources']['TGLExt/ClosedAntilinearStandardSubspace.lean']
assert gr['returncode']==0 and gr['source_sha256']==gx['sha256']
assert hf(gx['snapshot'])==gx['sha256'] and hf(gr['command'][2])==gr['output_sha256']
originpins[str(generic_origin)]={'manifest_sha256':hf(generic_origin/'manifest.json'),'compilation_sha256':hf(generic_origin/'compilation.json')}
catalog['TGLExt.ClosedAntilinearStandardSubspace']={'source':gx['snapshot'],'binary':gr['command'][2],'source_sha256':gx['sha256'],'sha256':gr['output_sha256'],'inherited_from':str(generic_origin),'reviewer_origin':str(generic_origin)}
'''
needle="parent=load(ROOT/'scalar_vna_custody.json')"
assert text.count(needle)==1;text=text.replace(needle,insert+needle)
needle2='for b in raws.values() for i in imports(b)'
assert text.count(needle2)==1
text=text.replace(needle2,"for b in list(raws.values())+[Path(gx['snapshot']).read_bytes()] for i in imports(b)")
ast.parse(text);backup=p.with_name(p.name+'.bak_'+stamp);write_new(backup,old)
new=text.encode();tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(new)
assert tmp.read_bytes()==new and p.read_bytes()==old and backup.read_bytes()==old
os.replace(tmp,p);assert p.read_bytes()==new
print(json.dumps({'failure_preserved':str(runs[0]/'preparation_failure.json'),'runner_backup':str(backup),'runner':str(p)}))
