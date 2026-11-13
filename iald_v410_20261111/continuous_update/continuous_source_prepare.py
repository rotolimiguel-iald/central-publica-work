"""Parametric read-only source verification + immutable app source snapshot.

No scientific execution, topic synthesis, runtime mutation, or mission creation.
Git paths originate in the installed admitted catalog and ls-tree, not guessed URLs.
"""
import copy
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse, unquote, quote

def digest(raw): return hashlib.sha256(raw).hexdigest()
def dump(obj): return (json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()

def immutable(path, raw):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        if path.read_bytes()!=raw: raise ValueError('Immutable output differs')
        return
    with path.open('xb') as f: f.write(raw)
    if path.read_bytes()!=raw: raise IOError('Output mismatch')

def git(repo,*args):
    p=subprocess.run(['git','-c','safe.directory='+Path(repo).as_posix(),'-c',
                      'core.quotepath=false','-C',str(repo),*args],capture_output=True)
    if p.returncode: raise RuntimeError('Git verification failed: '+args[0])
    return p.stdout

def catalog_relative(url):
    parsed=urlparse(url)
    parts=parsed.path.split('/')
    if parsed.scheme!='https' or parsed.netloc!='raw.githubusercontent.com' or parts[1:3]!=['rotolimiguel-iald','the_boundary']:
        raise ValueError('Catalog publication origin not admitted')
    rel=unquote('/'.join(parts[4:]))
    if not rel or '..' in Path(rel).parts or Path(rel).is_absolute():
        raise ValueError('Invalid repository-relative path')
    return rel

def discover(vault_root, repo, installed):
    """Called only on small seal delta by adapter. Remote read, no fetch or push."""
    root=Path(vault_root)
    versions=sorted((p for p in root.glob('um_unificado_v*') if re.fullmatch('um_unificado_v[0-9]+',p.name)),
                    key=lambda p:int(p.name.split('_v')[-1]),reverse=True)
    if not versions: raise ValueError('No custody version')
    vault=versions[0]
    seal_raw=(vault/'um_absoluto_selo.json').read_bytes();seal=json.loads(seal_raw)
    custody_raw=(vault/'CUSTODY_MANIFEST.json').read_bytes();custody=json.loads(custody_raw)
    release=seal['um_version'];source=seal['sha256']['um.py']
    if release!=vault.name.removeprefix('um_unificado_') or custody['version']!=release:
        raise ValueError('Custody version mismatch')
    if seal['fail_closed_selftest']!='FAIL_CLOSED_SELFTEST_PASSED' or custody.get('mismatches'):
        raise ValueError('Incomplete seal/custody')
    baseline=json.loads(Path(installed).read_bytes())
    rel=catalog_relative(baseline['published_evidence']['seal']['url'])
    remote=git(repo,'ls-remote','origin','refs/heads/main').decode().split()[0]
    # Refuse missing local immutable remote object instead of fetching/mutating repo.
    git(repo,'cat-file','-e',remote+'^{commit}')
    candidates=[remote]+git(repo,'log','-100','--format=%H',remote,'--',rel).decode().splitlines()
    commit=next((c for c in dict.fromkeys(candidates) if git(repo,'show',c+':'+rel)==seal_raw),None)
    if commit is None: raise ValueError('Sealed bytes not found in published ancestry')
    git(repo,'merge-base','--is-ancestor',commit,remote)
    return {'identity':{'release':release,'source_sha256':source},'commit':commit,
            'vault':str(vault),'seal_sha256':digest(seal_raw),'custody_sha256':digest(custody_raw),
            'installed_catalog':str(Path(installed).resolve()),'repository':str(Path(repo).resolve())}

def prepare_sources(candidate, output, extract_sources, jev_module):
    """extract_sources is the already installed AST-only iald_kernel function."""
    out=Path(output).resolve();repo=Path(candidate['repository']);vault=Path(candidate['vault'])
    commit=candidate['commit']
    if not re.fullmatch('[0-9a-f]{40}',commit): raise ValueError('Commit pin invalid')
    seal_raw=(vault/'um_absoluto_selo.json').read_bytes()
    if digest(seal_raw)!=candidate['seal_sha256'] or digest((vault/'CUSTODY_MANIFEST.json').read_bytes())!=candidate['custody_sha256']:
        raise ValueError('Custody changed')
    seal=json.loads(seal_raw)
    custody=json.loads((vault/'CUSTODY_MANIFEST.json').read_bytes())
    for row in custody['artifacts']:
        p=vault/row['file']
        if not p.resolve().is_relative_to(vault.resolve()): raise ValueError('Custody traversal')
        if digest(p.read_bytes())!=row['sha256']: raise ValueError('Custody artifact mismatch')
    if (seal['um_version']!=candidate['identity']['release'] or
        seal['sha256']['um.py']!=candidate['identity']['source_sha256']):
        raise ValueError('Candidate identity mismatch')
    m=copy.deepcopy(json.loads(Path(candidate['installed_catalog']).read_bytes()))
    tracked=set(git(repo,'ls-tree','-r','--name-only',commit).decode().splitlines())
    rows=m['entries']+[m['published_evidence'][k] for k in ('program','seal','result','proof_manifest')]
    artifacts=[]
    for row in rows:
        rel=catalog_relative(row['url'])
        if rel not in tracked: raise ValueError('Catalog path absent in pinned commit')
        raw=git(repo,'show',commit+':'+rel)
        local=vault/Path(rel).name
        if local.is_file() and local.read_bytes()!=raw: raise ValueError('Published custody bytes differ')
        target=out/'sources'/rel
        if not target.resolve().is_relative_to(out): raise ValueError('Source traversal')
        immutable(target,raw)
        row['path']=str(target);row['public_sha256']=digest(raw)
        row['url']='https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/'+commit+'/'+quote(rel,safe='/')
        artifacts.append({'path':str(target.relative_to(out)),'sha256':digest(raw),'bytes':len(raw)})
    evidence=m['published_evidence']
    for name in ('program','result','proof_manifest'):
        p=Path(evidence[name]['path'])
        if digest(p.read_bytes())!=seal['sha256'][p.name]: raise ValueError('Seal artifact mismatch')
    proof=json.loads(Path(evidence['proof_manifest']['path']).read_bytes())
    if proof['formal_source_hash']!=seal['formal_source_hash']: raise ValueError('Formal source mismatch')
    program=Path(evidence['program']['path']).read_text(encoding='utf-8-sig')
    embedded=extract_sources(program)
    for name,pin in proof['formal_files_sha256'].items():
        matches=[p for p in tracked if p.endswith('/'+name)]
        if name in embedded: raw=embedded[name].encode()
        elif len(matches)==1: raw=git(repo,'show',commit+':'+matches[0])
        else: raise ValueError('Formal artifact missing or ambiguous')
        if digest(raw)!=pin: raise ValueError('Formal source bytes mismatch')
        target=out/'kernel'/name
        if not target.resolve().is_relative_to(out/'kernel'): raise ValueError('Kernel traversal')
        immutable(target,raw)
        artifacts.append({'path':str(target.relative_to(out)),'sha256':pin,'bytes':len(raw)})
    # Preserve trusted instruction/core bytes as inputs. Builder generates bounded
    # core/JEV/index and pins their final bytes in its separate package manifest.
    for name in ('mother_instruction','operational_core'):
        row=m[name];raw=Path(row['path']).read_bytes()
        if digest(raw)!=row['sha256']: raise ValueError('Installed trusted core changed')
        target=out/'trusted_inputs'/(name+'.txt');immutable(target,raw);row['path']=str(target)
        artifacts.append({'path':str(target.relative_to(out)),'sha256':digest(raw),'bytes':len(raw)})
    for row in evidence.get('hypothesis_sources',[]):
        name=row['catalog_path'];matches=[p for p in tracked if p.endswith('/'+name)]
        if len(matches)!=1: raise ValueError('Hypothesis path ambiguous')
        row['url']='https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/'+commit+'/'+quote(matches[0],safe='/')
    control_raw=Path(m['jev_control']['path']).read_bytes()
    if digest(control_raw)!=m['jev_control']['sha256']: raise ValueError('JEV baseline changed')
    control=json.loads(control_raw)
    result_raw=Path(evidence['result']['path']).read_bytes();result=json.loads(result_raw)
    release=candidate['identity']['release'];source=candidate['identity']['source_sha256']
    control.update(release=release,source_sha256=source,result_sha256=digest(result_raw),
                   proof_manifest_sha256=digest(Path(evidence['proof_manifest']['path']).read_bytes()),
                   core_record=result['core']['iald_executive_runtime'])
    nodes=[n for n in ast.parse(program).body if isinstance(n,ast.FunctionDef) and n.name=='prove_iald_executive_runtime']
    if len(nodes)!=1: raise ValueError('JEV source function missing or ambiguous')
    control['source']['lines']=[nodes[0].lineno,nodes[0].end_lineno]
    for row in control['anchors']:
        path=out/'kernel'/row['file']
        if not path.resolve().is_relative_to(out/'kernel'): raise ValueError('JEV anchor traversal')
        raw=path.read_bytes();row['sha256']=digest(raw)
        if not all(symbol in raw.decode('utf8') for symbol in row['symbols']): raise ValueError('JEV anchor missing')
    if 'core_packet' in control:
        canonical=next(r for r in m['entries'] if r['id']=='um_forma_canonica_integral')
        packet=Path(canonical['path']).read_text(encoding='utf-8-sig')[:8000].encode()
        name='core_packet_'+release+'_bound.txt';target=out/name;immutable(target,packet)
        control['core_packet'].update(arquivo=name,sha256=digest(packet),um_version=release)
        artifacts.append({'path':name,'sha256':digest(packet),'bytes':len(packet)})
    jev_module.validate_contract(control)
    raw=jev_module.canonical_bytes(control);target=out/('jev_control_'+release+'.json');immutable(target,raw)
    m['jev_control'].update(path=str(target),sha256=digest(raw),release=release,source_sha256=source)
    artifacts.append({'path':target.name,'sha256':digest(raw),'bytes':len(raw)})
    m.pop('active_cluster',None) # Full result/kernel remain available; no legacy prompt expansion.
    m['source_identity']=candidate['identity'];m['source_commit']=commit
    m['source_artifacts']=artifacts
    target=out/'source_manifest.json';immutable(target,dump(m))
    return {'source_manifest':str(target),'source_manifest_sha256':digest(target.read_bytes())}
