"""Verify a completed local build; never rerun Lean or overwrite evidence."""
from pathlib import Path
import hashlib,json,re,sys
from task import W,new,pin

S=W/'sandbox'
K=Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel')
src=S/'TGLExt/PonteDaEscalaDual.lean'
attempt=S/'logs'/sys.argv[1]
r=json.loads(attempt.with_suffix('.json').read_text())
log=attempt.with_suffix('.log')
assert r['exit_code']==0 and r['source_unchanged_during_build']
assert r['source_sha256']==pin(src)['sha256']==pin(attempt.with_suffix('.lean'))['sha256']
assert Path(r['command'][-1])==src
text=log.read_text(encoding='utf-8')
assert not re.search(r'\berror:|sorryAx|AXIOM_AUDIT_REFUSED|NEW_AXIOM_REFUSED',text)
rows=[]
for line in text.splitlines():
    if line.startswith('O25_DECL\t'):
        _,name,kind,axioms=line.split('\t')
        rows.append(dict(name=name,kind=kind,axioms=axioms.split(',') if axioms else []))
allowed={'propext','Classical.choice','Quot.sound'}
assert rows and all(set(x['axioms'])<=allowed and x['kind']!='axiom' for x in rows)
code=src.read_text(encoding='utf-8')
plain=re.sub(r'/\-.*?\-/|--[^\n]*','',code,flags=re.S)
plain=re.sub(r'"(?:\\.|[^"\\])*"','""',plain)
assert not re.search(r'\b(sorry|admit|axiom)\b',plain)
decl=re.findall(r'^(?:def|abbrev|theorem)\s+(\w+)',code,re.M)
printed=re.findall(r'^#print axioms (\S+)',code,re.M)
assert len(printed)==len(decl)
assert set(printed)=={'TGLExt.PonteDaEscalaDual.'+n for n in decl}
assert set(printed)<={x['name'] for x in rows}
copies=json.loads((S/'DEPENDENCY_COPIES.json').read_text())
checked=[]
for c in copies:
    q=pin(Path(c['target']))
    assert q['sha256']==c['sha256'],c['target']
    checked.append(q)
direct=[]
for mod in re.findall(r'^import (\S+)',code,re.M):
    suffix=Path(mod.replace('.','/')+'.lean')
    source=S/suffix if mod=='TGLExt.FalsidadeDaInercia' else K/suffix
    ole=S/suffix.with_suffix('.olean')
    item={'module':mod,'source':pin(source),'sandbox_olean':pin(ole),'recompiled_here':mod=='TGLExt.FalsidadeDaInercia'}
    if not item['recompiled_here']:
        item['readonly_cache']=pin(K/'.lake/build/lib/lean'/suffix.with_suffix('.olean'))
        assert item['readonly_cache']['sha256']==item['sandbox_olean']['sha256']
    direct.append(item)
ax={'status':'PASS','declared_source_count':len(decl),'theorems':len(re.findall(r'^theorem ',code,re.M)),
    'explicit_print_count':len(printed),'all_declarations_including_generated':rows,
    'allowed_axioms':sorted(allowed),'source':pin(src),'log':pin(log),'zero_sorry':True}
new('AXIOMAS_VERIFIED.json',ax)
new('BUILD_VERIFIED.json',{'status':'PASS','source':pin(src),'olean':pin(src.with_suffix('.olean')),
    'build':r,'receipt':pin(attempt.with_suffix('.json')),'stdout':pin(log),'dependency_sources':direct,
    'dependency_manifest':pin(S/'DEPENDENCY_COPIES.json'),'copied_files_verified':len(checked),
    'copied_bytes':sum(c['bytes'] for c in copies),'lake_manifest':pin(K/'lake-manifest.json'),
    'lean_toolchain':pin(K/'lean-toolchain'),
    'scope':'Target and Falsidade rebuilt. Other imports reuse cache artifacts, verified by hashes; no full rebuild of canonical dependencies.'})
print(json.dumps({'status':'PASS','source_sha256':pin(src)['sha256'],'declarations':len(decl),
    'theorems':ax['theorems'],'including_generated':len(rows),'seconds':r['duration_seconds'],'copies':len(checked)}))
