from pathlib import Path
import json,hashlib,re,shutil
ROOT=Path(__file__).resolve().parent
KERNEL=Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel')
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
src=ROOT/'TGLExt/PonteDaEscalaDual.lean'
attempts=sorted((ROOT/'logs').glob('attempt_*.json'))
last=json.loads(attempts[-1].read_text())
assert last['exit_code']==0 and last['source_sha256']==pin(src)['sha256']
assert last['command'][-1]==str(src)
assert last['source_unchanged_during_build']
log=attempts[-1].with_suffix('.log');txt=log.read_text(encoding='utf-8')
rows=[]
for line in txt.splitlines():
    if line.startswith('O25_DECL\t'):
        _,name,kind,axs=line.split('\t');rows.append({'name':name,'kind':kind,'axioms':axs.split(',') if axs else []})
allowed={'propext','Classical.choice','Quot.sound'}
assert rows and all(set(x['axioms']) <= allowed for x in rows)
assert not re.search(r'\b(sorry|admit|axiom)\b',re.sub(r'/\-.*?\-/|--[^\n]*','',src.read_text(encoding='utf-8'),flags=re.S))
direct=[]
for name in re.findall(r'^import (\S+)',src.read_text(encoding='utf-8'),re.M):
    if name=='TGLExt.FalsidadeDaInercia':
        p=ROOT/(name.replace('.','/')+'.lean');origin=Path('C:/IALD/Central de Patentes/work/falsidade_da_inercia_v401/FalsidadeDaInercia.lean')
    else:
        p=KERNEL/(name.replace('.','/')+'.lean');origin=p
    ole=ROOT/(name.replace('.','/')+'.olean')
    rec={'module':name,'source':pin(p),'original':pin(origin),'sandbox_olean':pin(ole),'recompiled_here':name=='TGLExt.FalsidadeDaInercia'}
    if name!='TGLExt.FalsidadeDaInercia':
        cache=KERNEL/'.lake/build/lib/lean'/(name.replace('.','/')+'.olean')
        rec['readonly_cache']=pin(cache)
        rec['cache_copy_matches']=pin(cache)['sha256']==pin(ole)['sha256']
        assert rec['cache_copy_matches']
    direct.append(rec)
declnames=re.findall(r'^(?:def|abbrev|theorem)\s+(\w+)',src.read_text(encoding='utf-8'),re.M)
ax={'status':'PASS','allowed_axioms':sorted(allowed),'all_declarations_including_generated':rows,'declared_source_count':len(declnames),'explicit_print_count':len(re.findall(r'^#print axioms ',src.read_text(encoding='utf-8'),re.M)),'source':pin(src),'log':pin(log)}
(ROOT/'AXIOMAS.json').write_text(json.dumps(ax,indent=2),encoding='utf-8')
shutil.copyfile(log,ROOT/'BUILD_FINAL.log')
out={'status':'LEAN_COMPILED_AXIOMS_IN_TRIO','source':pin(src),'olean':pin(src.with_suffix('.olean')),'successful_attempt':pin(attempts[-1]),'build':last,'dependency_sources':direct,'dependency_copy_manifest':pin(ROOT/'DEPENDENCY_COPIES.json'),'axioms':pin(ROOT/'AXIOMAS.json'),'log':pin(ROOT/'BUILD_FINAL.log'),'provenance_errata':pin(ROOT/'logs/PROVENANCE_ERRATA.json'),'scope':'Current module and copied Falsidade recompiled; imported dependencies use copied caches, not newly recompiled. Source/cache semantic consistency not independently recompiled here.'}
(ROOT/'BUILD_FINAL.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'status':out['status'],'declarations':len(declnames),'all_including_generated':len(rows),'source_sha256':pin(src)['sha256'],'duration':last['duration_seconds']}))
