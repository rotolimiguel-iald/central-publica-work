"""Build a reviewable data-only future installation plan; never applies it."""
import copy,json
from pathlib import Path
from continuous_source_prepare import digest,dump,immutable

def build_plan(candidate,cfg):
    candidate=Path(candidate).resolve();root=Path(cfg['runtime']).resolve();package=candidate/'package'
    release_path=package/'release.json';release=json.loads(release_path.read_bytes())
    identity=release['identity'];pin=digest(release_path.read_bytes())
    target_name=identity['release']+'_'+pin[:16]
    target=root/'canonical_releases'/target_name
    old=Path(cfg['installed_catalog']);baseline=old.read_bytes();catalog=copy.deepcopy(json.loads(baseline))
    files=[];certificates=[]
    def row(source,destination):
        raw=source.read_bytes()
        return {'source':str(source),'destination':str(destination),'bytes':len(raw),'sha256':digest(raw),
                'baseline':digest(destination.read_bytes()) if destination.is_file() else None}
    known=[r['path'] for r in release['artifacts']]+['release.json']
    packages={}
    for name in ('haiku55','sonnet'):
        folder=package/'native'/name;manifest=folder/'manifest.json';m=json.loads(manifest.read_bytes())
        expected={**identity,'manifest_sha256':pin}
        if m['deployment']!=expected or not m['budget']['ready']: raise ValueError('Native package not bound/ready')
        if digest((folder/'prefix.md').read_bytes())!=m['prefix_sha256']: raise ValueError('Native prefix mismatch')
        if (folder/'prefix.md').read_bytes()!=(package/release['prefix_file']).read_bytes(): raise ValueError('Native context differs')
        packages[name]={'path':str(target/'native'/name),'manifest_sha256':digest(manifest.read_bytes())}
        certificates.append({'path':str(manifest),'sha256':digest(manifest.read_bytes())})
        for f in sorted(folder.iterdir()):
            if f.is_file(): known.append(str(f.relative_to(package)))
    if len(known)!=len(set(known)): raise ValueError('Duplicate artifact in plan')
    for rel in known:
        src=(package/rel).resolve(strict=True)
        if not src.is_relative_to(package): raise ValueError('Plan source traversal')
        files.append(row(src,target/rel))
    source_raw=(candidate/'source/source_manifest.json').read_bytes()
    if digest(source_raw)!=release['source_manifest_sha256']: raise ValueError('Source catalog binding changed')
    source=json.loads(source_raw)
    artifact_map={r['path']:r for r in release['artifacts']}
    def bound_path(rel):
        record=artifact_map[rel];raw=(package/rel).read_bytes()
        if digest(raw)!=record['sha256'] or len(raw)!=record['bytes']: raise ValueError('Metadata artifact changed')
        return str(target/rel),record['sha256']
    documents={r['id']:r for r in release['documents']}
    entries=[]
    for entry in source['entries']:
        record=copy.deepcopy(entry);path,pin_entry=bound_path(documents[entry['id']]['path'])
        if pin_entry!=entry['public_sha256']: raise ValueError('Entry source mismatch')
        record.update(path=path,public_sha256=pin_entry);entries.append(record)
    catalog['entries']=entries
    evidence=copy.deepcopy(source['published_evidence'])
    for label,entry in evidence.items():
        if isinstance(entry,dict) and 'path' in entry:
            rel='evidence/'+label+Path(entry['path']).suffix
            path,pin_entry=bound_path(rel)
            if digest(Path(entry['path']).read_bytes())!=pin_entry: raise ValueError('Evidence source mismatch')
            entry.update(path=path,public_sha256=pin_entry)
    for entry in evidence.get('hypothesis_sources',[]):
        path,pin_entry=bound_path('kernel/'+entry['catalog_path'].replace('\\','/'))
        entry.update(path=path,sha256=pin_entry)
    catalog['published_evidence']=evidence
    for name,rel in [('mother_instruction','mother.txt'),('operational_core','operational_core.md'),('jev_control',release['jev_file'])]:
        record=copy.deepcopy(source[name]);path,pin_entry=bound_path(rel)
        record.update(path=path,sha256=pin_entry)
        if name=='operational_core':
            record.update(current_release=identity['release'],release_source_sha256=identity['source_sha256'])
            if pin_entry!=identity['operational_core_sha256']: raise ValueError('Core identity mismatch')
        elif name=='jev_control':
            record.update(release=identity['release'],source_sha256=identity['source_sha256'])
            actual=json.loads((package/rel).read_bytes())
            if actual['release']!=identity['release'] or actual['source_sha256']!=identity['source_sha256']:
                raise ValueError('JEV content identity mismatch')
            if pin_entry!=identity['jev_sha256']: raise ValueError('JEV identity mismatch')
        catalog[name]=record
    catalog['kernel_bundle']=str(target/release['kernel_root'])
    catalog['kernel_verification']=bound_path(release['kernel_verification'])[0]
    history=candidate/'historical_catalog.json';immutable(history,baseline)
    files.append(row(history,target/'historical_catalog.json'))
    catalog['historical_catalog']={'path':str(target/'historical_catalog.json'),'sha256':digest(baseline),
                                   'scope':'PREVIOUS_CATALOG_NOT_ACTIVE_SCIENCE'}
    catalog['science_snapshot']={'path':str(target/'release.json'),'sha256':pin,'packages':packages}
    catalog['selected_science_identity']={**identity,'manifest_sha256':pin}
    catalog.pop('active_cluster',None)
    catalog.pop('legacy_catalog_scope',None)
    pointer=candidate/'next_catalog.json';immutable(pointer,dump(catalog))
    files.append(row(pointer,old))
    plan={'schema':'iald.app.data-only-plan.v1','target_name':target_name,'identity':{**identity,'manifest_sha256':pin},
          'files':files,'capacity_certificates':certificates,'historical_catalog_retained':True,
          'runtime_updates':False,'mutable_pointer':str(old)}
    immutable(candidate/'install_plan.json',dump(plan))
    return plan
