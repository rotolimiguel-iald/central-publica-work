"""Read-only independent source and P2 checks; no provider counts or generation."""
from pathlib import Path
import hashlib,json,re,subprocess
from urllib.parse import quote

W=Path(__file__).resolve().parent.parent
A=W/'app'
V=Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v409')
N=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
G=Path(r'C:\IALD\Artigo\the_boundary')
read=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
pin=lambda p:{'path':str(p),'sha256':sha(Path(p).read_bytes())}
def save(name,data):
    if (W/'review'/name).exists():
        assert read(W/'review'/name)==data
        return
    with (W/'review'/name).open('x',encoding='utf-8') as f:json.dump(data,f,ensure_ascii=False,indent=2)
def git(*args):return subprocess.check_output(['git','-C',str(G),*args])

s=read(W/'sources_verified.json');pub=read(A/'PUBLIC_RAW_VERIFIED.json');rel=read(A/'RELEASE.json')
assert s['release']==rel['release']=='v409'
assert sha(Path(s['custody_manifest']['path']).read_bytes())==s['custody_manifest']['sha256']
custody=read(V/'CUSTODY_MANIFEST.json')
assert custody['version']==custody['um_version_no_selo']=='v409' and not custody['mismatches']
assert len(s['artifacts'])==len(custody['artifacts'])==36
catalog={r['file']:r for r in custody['artifacts']}
for row in s['artifacts']:
    path=(V/row['file']).resolve();assert path.is_relative_to(V.resolve())
    raw=path.read_bytes()
    assert sha(raw)==row['sha256']==catalog[row['file']]['sha256'] and len(raw)==row['bytes']
seal=read(V/'um_absoluto_selo.json');proof=read(V/'tgl_kernel_proof_manifest.json')
assert seal['um_version']=='v409' and seal['fail_closed_selftest']=='FAIL_CLOSED_SELFTEST_PASSED'
assert seal['formal_source_hash']==proof['formal_source_hash']==custody['formal_source_hash']==s['formal_source_hash']
assert sha((V/'um.py').read_bytes())==rel['um_py_sha256']==s['source_sha256']==custody['um_py_pin']
live=read(N/'um_absoluto_selo.json')['um_version']
live_compared=[]
for name in ('um.py','um_absoluto.json','tgl_kernel_proof_manifest.json','um_absoluto_forma_canonica.md'):
    raw=(V/name).read_bytes();assert sha(raw)==seal['sha256'][name]
    if live=='v409':
        assert (N/name).read_bytes()==raw;live_compared.append(name)
commit=rel['espelho_commit'];assert commit==pub['commit']==s['published']['pinned_commit']
tracked=set(git('ls-tree','-r','--name-only','-z',commit).decode().split('\0'))
git('merge-base','--is-ancestor',commit,s['published']['remote_main'])
binding=read(A/'PUBLIC_GIT_BINDING.json')
assert sha((A/'PUBLIC_GIT_BINDING.json').read_bytes())==pub['source_binding_sha256']
manifest=read(A/'science/memory_stage/manifest_staged.json')
entries={e['url']:e for e in manifest['entries']}
assert len(pub['files'])==10
for row in pub['files']:
    assert row['path'] in tracked
    url='https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/'+commit+'/'+quote(row['path'],safe='/')
    assert row['url']==url and row['http']==200
    raw=git('show',commit+':'+row['path'])
    assert sha(raw)==row['sha256']==binding['sources'][row['path']]['sha256'] and len(raw)==row['bytes']
    assert (A/'science/memory_stage/release'/row['path']).read_bytes()==raw
    if url in entries:
        entry=entries[url];assert Path(entry['path']).read_bytes()==raw and entry['public_sha256']==row['sha256']
baseline=read(W/'PRESERVATION_BASELINE.json')
assert len(baseline['files'])==13
for row in baseline['files']:assert sha(Path(row['path']).read_bytes())==row['sha256']
source_report={'status':'PASS','reviewer':'codex-app-v409-review','task_id':'sources','custody_artifacts':36,'public_git_and_staged_files':10,'preservation_pins':13,'live_version':live,'live_files_compared':live_compared,'release':'v409','commit':commit,'source_sha256':s['source_sha256'],'evidence':[pin(W/'sources_verified.json'),pin(A/'PUBLIC_RAW_VERIFIED.json'),pin(A/'PUBLIC_GIT_BINDING.json'),pin(V/'CUSTODY_MANIFEST.json')],'scope':'Independent local rehash of custody, seal, proof manifest, live sources, pinned git objects and staged public bytes. HTTP200 is the builders pinned receipt, not a new network observation. No Lean/program execution or scientific confirmation.','findings':[]}
save('SOURCES_R1.json',source_report)

cap=read(A/'CAPACITY_BLOCKED.json');prefixraw=Path(cap['prefix']['path']).read_bytes()
assert sha(prefixraw)==cap['prefix']['sha256'] and len(prefixraw)==cap['shared_bytes']==890840
prefix=prefixraw.decode();history=read(A/'D53_HISTORY.json')
entry=next(e for e in manifest['entries'] if e['id']=='resultado_publicado_integral')
document=Path(entry['path']).read_bytes().decode('utf-8')
assert sha(document.encode())==history['source_text_sha256']==entry['public_sha256']
source=json.loads(document);core=source['core']
resident={name for name in core if name.endswith(('_v408','_v409'))}|{'the_iald_index'}
assert set(history['resident'])==resident
assert not resident.intersection(history['spans'])
literals=json.loads(prefix.split('DICIONÁRIO DE LITERAIS\n',1)[1].split('\n',1)[0])
flags=json.loads(prefix.split('DICIONÁRIO DE INDICADORES LITERAIS\n',1)[1].split('\n',1)[0])
exposition=prefix.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
aliases={'@F':'@SOURCE_FIELDS','@I':'@SOURCE_ITEMS','@L':'@TGL_LITERAL','@Y':'@SUMMARY','@X':'@EXPOSITION'}
def decode(v):
    if isinstance(v,list):return [decode(x) for x in v]
    if not isinstance(v,dict):return v
    v={aliases.get(k,k):x for k,x in v.items()}
    if set(v)=={'@TGL_LITERAL'}:return decode(literals[v['@TGL_LITERAL']])
    if set(v)=={'@EXPOSITION'}:
        start,size=v['@EXPOSITION'];assert start>=0 and size>0 and start+size<=len(exposition)
        return exposition[start:start+size]
    if set(v)=={'@concat'}:return ''.join(decode(x) for x in v['@concat'])
    if set(v)=={'@upper'}:return v['@upper'].upper()
    if set(v)=={'@enum'}:return v['@enum'].upper().replace(' ','_')
    result={k:decode(x) for k,x in v.items() if k not in ('@SOURCE_FIELDS','@SOURCE_ITEMS')}
    for field in v.get('@SOURCE_FIELDS',[]):
        assert field not in result;result[field]={'@':'/'+field}
    for field,count in v.get('@SOURCE_ITEMS',{}).items():
        assert field not in result;result[field]={'@':'/'+field,'items':count}
    if '@B' in result:
        extra=flags[result.pop('@B')];assert not set(extra).intersection(result);result.update(extra)
    return result
head=prefix.split('## Exposição canônica integral: fórmulas e derivações',1)[0]
headings=[m for m in re.finditer(r'(?m)^### ([^\n]+)\n',head) if m[1] in core]
assert len(headings)==len(core)==len({m[1] for m in headings})
checked=[]
for i,m in enumerate(headings):
    name=m[1]
    if name not in resident and name not in history['spans']:continue
    block=head[m.end():headings[i+1].start() if i+1<len(headings) else len(head)]
    obj=decode(json.loads(next(line for line in block.splitlines() if line.startswith('{'))))
    if name in resident:
        assert obj==core[name],name
    else:
        offset,size=obj.pop('@H');assert [offset,size]==history['spans'][name]
        assert offset>=0 and size>0 and offset+size<=len(document)
        recovered=json.loads(document[offset:offset+size]);assert recovered==core[name],name
        assert all(recovered[k]==value for k,value in obj.items()),name
    checked.append(name)
high=read(A/'KERNEL_HIGHLIGHTS.json')
scope=source
for part in high['scope_pointer'].strip('/').split('/'):
    scope=scope[int(part)] if isinstance(scope,list) else scope[part]
assert scope==high['scope'] and scope in prefix
for anchor in high['anchors']:
    paths=[p for p in tracked if p.endswith('/'+anchor['path'])]
    matching=[git('show',commit+':'+p) for p in paths]
    matching=[b for b in matching if sha(b)==anchor['sha256']]
    assert matching,anchor['path']
    lo,hi=anchor['lines'];lines=matching[0].decode().splitlines()
    segment='\n'.join(lines[lo-1:hi])
    assert segment.startswith(anchor['statement'])
    assert segment[len(anchor['statement']):].startswith(' :='),anchor['symbol']
    assert sha(matching[0])==proof['formal_files_sha256'][anchor['path']]
    assert anchor['symbol'] in proof['axiom_report']
    assert anchor['statement'] in prefix
assert '<ATLAS_CANONICO' not in prefix
for name,m in cap['bounds_with_declared_reserve'].items():
    assert m['slack']==cap['window']-m['input_bound']-cap['declared_output_reserve']-cap['safety_margin']
save('P2_R1.json',{'status':'PASS_P2_ONLY_APP_NOT_ACCEPTED','reviewer':'codex-app-v409-review','resident_complete':sorted(resident),'historical_exact':len(history['spans']),'topics':len(core),'statements_matched_to_pinned_lean':len(high['anchors']),'scope_literal_equal_source':True,'index_full_equality':True,'shared_bytes':len(prefixraw),'capacity_measured_by_builder':cap['bounds_with_declared_reserve'],'counts_repeated':False,'app_accepted':False,'finalize_executed':False,'evidence':[pin(A/'CAPACITY_BLOCKED.json'),pin(A/'D53_HISTORY.json'),pin(A/'KERNEL_HIGHLIGHTS.json'),pin(Path(cap['prefix']['path']))],'scope':'Own decoder checks full resident JSON equality using only resident dictionaries/exposition; 177 history spans checked against the pinned full public source; no provider calls or counts. App capacity remains blocked.'})
print(json.dumps({'sources':'PASS','P2':'PASS','resident':len(resident),'historical':len(history['spans']),'statements':len(high['anchors']),'app':'NOT_ACCEPTED'}))
