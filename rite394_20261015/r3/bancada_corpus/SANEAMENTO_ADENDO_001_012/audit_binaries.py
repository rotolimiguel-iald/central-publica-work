from support import *
import re,subprocess,sys
K=ROOT/'kernel';current=json.loads((ROOT/'binary/REBUILD_ATUAL.json').read_text(encoding='utf-8'))
results=json.loads(Path(current['results']).read_text(encoding='utf-8'));D=ROOT/'binary/axioms'/stamp();D.mkdir(parents=True)
mods=[];names=[]
for row in results:
 assert row['returncode']==0
 m=row['module'];mods.append(m);parts=m.split('.')
 for a in Path(row['output']).parent.glob(parts[-1]+'.*'):
  if a.suffix in ['.olean','.ilean'] or '.olean.' in a.name:atomic(D/'lib/lean'/Path(*parts[:-1])/a.name,a.read_bytes())
 ns='TGLExt' if parts[0]=='TGLExt' else 'TGL.AreaScale'
 s=Path(row['source']).read_text(encoding='utf-8-sig')
 for n in re.findall(r'^(?:@\[[^\]]*\]\s*)*(?:noncomputable\s+)?(?:theorem|def|abbrev)\s+([^\s(:{]+)',s,re.M):names.append(ns+'.'+n)
source='\n'.join('import '+m for m in mods)+'\nset_option pp.universes true\n'+'\n'.join('#check '+n+'\n#print axioms '+n for n in names)+'\n'
p=D/'AuditBinaries.lean';atomic(p,source)
base=subprocess.run([str(BIN/'lake.exe'),'env',sys.executable,'-c','import os;print(os.environ["LEAN_PATH"])'],cwd=K,env=clean_env(),capture_output=True,check=True).stdout.decode('utf-8').strip()
env=clean_env();env['LEAN_PATH']=str(D/'lib/lean')+os.pathsep+base
assert all(Path(s).resolve().is_relative_to(ROOT) or Path(s).resolve().is_relative_to(BIN.parent) for s in env['LEAN_PATH'].split(os.pathsep) if s)
arts={}
for row in results:arts.update(json.loads(Path(row['setup_path']).read_text(encoding='utf-8'))['importArts'])
for row in results:arts[row['module']]=[row['output']]
setup=D/'audit.setup.json';setup_data=json.loads(Path(results[0]['setup_path']).read_text(encoding='utf-8'));setup_data.update(name='AuditBinaries',importArts=arts);record(setup,setup_data)
env['LEAN_PATH']=base
cmd=[str(BIN/'lean.exe'),str(p),'--setup',str(setup)];r=subprocess.run(cmd,cwd=K,env=env,capture_output=True)
atomic(D/'stdout.txt',r.stdout);atomic(D/'stderr.txt',r.stderr)
text=(r.stdout+r.stderr).decode('utf-8',errors='replace');parsed={}
for n,ax in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",text,re.S):parsed[re.sub(r'\.\{[^}]*\}','',n)]=[re.sub(r'\.\{[^}]*\}','',a.strip()) for a in ax.replace('\n',' ').split(',') if a.strip()]
for n in re.findall(r"'([^']+)' does not depend on any axioms",text):parsed[re.sub(r'\.\{[^}]*\}','',n)]=[]
missing=sorted(set(names)-set(parsed));outside={n:ax for n,ax in parsed.items() if set(ax)-{'propext','Classical.choice','Quot.sound'}}
ok=r.returncode==0 and not missing and not outside
record(D/'RESULTADO.json',dict(command=cmd,cwd=str(K),lean_path=env['LEAN_PATH'],source=str(p),source_sha256=digest(p),returncode=r.returncode,expected=names,parsed=parsed,missing=missing,outside=outside,all_within_trio=ok,stdout=str(D/'stdout.txt'),stdout_sha256=digest(D/'stdout.txt'),union=sorted({a for aa in parsed.values() for a in aa})))
record(ROOT/'binary/AXIOMAS_ATUAL.json',dict(report=str(D/'RESULTADO.json'),ok=ok,expected=len(names)))
print('BINARY AXIOMS',r.returncode,ok,len(names),'missing',missing,'outside',outside)
if r.returncode:print(text)

sys.exit(0 if ok else 1)
