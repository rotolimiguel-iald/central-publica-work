from review import *

packages=AUTHOR/'kernel'/'.lake'/'packages'
manifest=json.loads((ROOT/'inputs'/'lake-manifest.json').read_text(encoding='utf-8'))
rows=[]
for item in manifest['packages']:
    p=packages/item['name']
    cmd=['git','-C',str(p),'rev-parse','HEAD']
    result=subprocess.run(cmd,capture_output=True,env=env())
    revision=result.stdout.decode().strip()
    cache=p/'.lake'/'build'/'lib'/'lean'
    row=dict(name=item['name'],source_root=str(p),cache_root=str(cache),cache_exists=cache.is_dir(),
             expected_revision=item['rev'],command=cmd,returncode=result.returncode,
             actual_revision=revision,revision_matches=result.returncode==0 and revision==item['rev'],
             stderr=result.stderr.decode(errors='replace'))
    anchors=[]
    for rel in [item['configFile'], 'lean-toolchain', 'lake-manifest.json', 'Mathlib.lean']:
        if (p/rel).is_file(): anchors.append(info(p/rel))
    row['files_read']=anchors
    rows.append(row)
direct=[]
for module in ['Mathlib','Mathlib.Analysis.SpecialFunctions.Log.Basic']:
    base=packages/'mathlib'/'.lake'/'build'/'lib'/'lean'/Path(*module.split('.'))
    for suffix in ['.olean','.olean.private','.olean.server','.ir']:
        p=base.with_suffix(suffix)
        if p.is_file(): direct.append(info(p))
record(ROOT/'CACHE_EVIDENCE.json',dict(packages=rows,direct_import_objects=direct,
       all_revisions_match=all(r['revision_matches'] for r in rows),
       scope='Read-only third-party caches; source revision checks do not attest recompilation or all transitive object bytes',
       rebuilt=False,local_TGL_objects_reused=False))
print('Cache package revisions',sum(r['revision_matches'] for r in rows),'/',len(rows),flush=True)
