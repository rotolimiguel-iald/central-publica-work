from pathlib import Path
from datetime import datetime
import hashlib,json,os,re,subprocess,sys,time,traceback

R=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012')
V=R/'v'; K=R/'k'; OLD=R.parent/'kernel'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
CONFIG={
 'core':('revisao_core',['V351ScalarImaginaryLeftTransport','V351ScalarImaginaryCoreAction'],5,['REAPROVEITAMENTO_A1B_ESQUERDA','REAPROVEITAMENTO_A1B_ACAO_CORE']),
 'absorcao':('revisao_absorcao',['V351RegularFlowAbsorption'],6,['REAPROVEITAMENTO_A1B_ABSORCAO']),
 'fourier':('revisao_fourier',['V351FourierTranslation'],3,['REAPROVEITAMENTO_A1B_FOURIER_TRANSLACAO','ADENDO_FICHA_FOURIER_TRANSLACAO']),
 'grafo':('revisao_grafo',['V351RegularPositiveGraph'],15,['REAPROVEITAMENTO_A1B_GERADOR_POSITIVO','ADENDO_GERADOR_ANTECEDENTE_ESCALAR']),
 'espectral':('revisao_grafo_espectral',['V351RegularSpectralGraph'],3,['REAPROVEITAMENTO_A1B_GRAFO_ESPECTRAL']),
 'calculo':('revisao_calculo',['V351ScalarMultiplierCalculus'],5,['REAPROVEITAMENTO_A1B_CALCULO_MULTIPLICADOR']),
 'potencias':('revisao_potencias',['V351RegularImaginaryPowers'],4,['REAPROVEITAMENTO_A1B_POTENCIAS_REGULARES']),
 'afiliacao':('revisao_afiliacao',['V351RegularGeneratorAffiliation'],3,['REAPROVEITAMENTO_A1B_AFILIACAO_REGULAR']),
 'escala_dual':('revisao_escala_dual',['V351RegularGeneratorDualScaling'],7,['REAPROVEITAMENTO_A1B_ESCALA_DUAL_REGULAR','ADENDO_FICHA_ESCALA_DUAL']),
 'cortes_inverso':('revisao_cortes_inverso',['V351InverseGeneratorCutoff'],8,['REAPROVEITAMENTO_A1B_CORTES_INVERSO','ADENDO_FICHA_INVERSO_BILATERAL']),
 'fechamento_gns':('revisao_fechamento_gns',['V351ScalarGNSClosedness'],3,['REAPROVEITAMENTO_A1B_FECHAMENTO_GNS']),
 'limites_direita':('revisao_limites_direita',['V351ScalarRightActionLimits'],2,['REAPROVEITAMENTO_A1B_LIMITES_ACAO_DIREITA']),
 'algebra_direita':('revisao_algebra_direita',['V351ScalarRightActionAlgebra'],12,['REAPROVEITAMENTO_A1B_ALGEBRA_ACAO_DIREITA']),
 'seno_resolvente':('revisao_seno_resolvente',['V351SineResolventApprox'],11,['REAPROVEITAMENTO_A1B_APROXIMANTES_SENO','ADENDO_FICHA_SENO_DCT'])}
def now():return datetime.now().astimezone().isoformat()
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_bytes())
def ck(p):assert pin(Path(p['path']))==p,p
def fresh(p,b):
 assert p.resolve().is_relative_to(V.resolve()) or any(p.resolve().is_relative_to((R/x[0]).resolve()) for x in CONFIG.values()),p
 assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name(p.name+'.tmp')
 with tmp.open('xb') as f:f.write(b)
 assert tmp.read_bytes()==b;os.replace(tmp,p)
def save(p,x):fresh(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def uncomment(s):
 out=[];d=0;i=0
 while i<len(s):
  if s.startswith('/-',i):d+=1;i+=2
  elif d and s.startswith('-/',i):d-=1;i+=2
  elif d:
   if s[i]=='\n':out.append('\n')
   i+=1
  elif s.startswith('--',i):
   j=s.find('\n',i);i=len(s) if j<0 else j
  else:out.append(s[i]);i+=1
 assert d==0;return ''.join(out)
def main(key):
 folder,names,count,docs=CONFIG[key];out=R/folder;out.mkdir(exist_ok=True)
 a=out/('independent_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'));a.mkdir()
 print('ATTEMPT',a,flush=True)
 base=[]
 for parent in ['revisao','revisao_core','revisao_absorcao','revisao_fourier','revisao_grafo','revisao_grafo_espectral','revisao_calculo','revisao_potencias','revisao_afiliacao','revisao_escala_dual','revisao_cortes_inverso','revisao_fechamento_gns','revisao_limites_direita','revisao_algebra_direita']:
  if parent==folder:break
  p=R/parent/'compilation.json';j=load(p);base.append(pin(p))
  for r in j['objects']:
   for field in ['own','object','trace']:
    if field in r:ck(r[field])
 protected=[]
 for prefix in ['TGL','TGLExt']:
  for p in sorted((V/prefix).rglob('*.lean')):protected.append(pin(p))
 for p in sorted((V/'.lake/build/lib/lean').rglob('*')):
  if p.is_file() and p.suffix in ['.olean','.ilean','.trace','.hash','.server','.private']:protected.append(pin(p))
 for n in ['lakefile.toml','lake-manifest.json','lean-toolchain']:protected.append(pin(V/n))
 for folder0 in ['revisao','revisao_core','revisao_absorcao','revisao_fourier','revisao_grafo','revisao_grafo_espectral','revisao_calculo','revisao_potencias','revisao_afiliacao','revisao_escala_dual','revisao_cortes_inverso','revisao_fechamento_gns','revisao_limites_direita','revisao_algebra_direita']:
  if folder0==folder:break
  for p in (R/folder0).glob('*'):
   if p.is_file() and (p.name.startswith('REVIEW') or p.name=='compilation.json'):protected.append(pin(p))
 for p in R.glob('*ORFAOS_A1B.json'):protected.append(pin(p))
 sources=[];seen=set();targets=[]
 def visit(mod):
  if mod in seen:return
  seen.add(mod);rel=Path(mod.replace('.','/')+'.lean');dst=V/rel
  target=mod.split('.')[-1] in names
  if dst.exists():
   assert not target,('target already present; inspect previous attempt',mod)
   src=dst;b=dst.read_bytes();inherited=True
  else:
   src=(K if target else OLD)/rel
   b=src.read_bytes();inherited=False
   if not target:
    assert not mod.split('.')[-1].startswith('V351'),('unauthorized new dependency',mod)
    assert b==(K/rel).read_bytes(),mod
  code=uncomment(b.decode('utf-8-sig'));imports=[]
  for m in re.finditer(r'^\s*(?:public\s+)?import\s+([^\n]+)',code,re.M):imports+=m.group(1).split()
  for dep in imports:
   if dep.startswith(('TGL.','TGLExt.')) or dep in ['TGL','TGLExt']:visit(dep)
  if not inherited:fresh(dst,b)
  if target:
   assert not re.findall(r'\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe)\b',code),mod
   ns=re.findall(r'^namespace\s+(\S+)',code,re.M);assert ns==['TGLV350.Regular'],(mod,ns)
   nms=re.findall(r'^#print axioms\s+(\S+)',code,re.M)
   for nm in nms:
    dec=re.search(r'^(?:noncomputable\s+)?(theorem|def)\s+'+re.escape(nm)+r'\b',code,re.M);assert dec,(mod,nm)
    targets.append(dict(name='TGLV350.Regular.'+nm,module=mod,kind=dec.group(1)))
   fresh(a/src.name,b)
  sources.append(dict(module=mod,original=pin(src),copy=pin(dst),imports=imports,target=target,source_preexisting=inherited))
 for name in names:visit('TGLExt.'+name)
 assert len(targets)==count and len({x['name'] for x in targets})==count
 audit='TGLExt.ReviewA1'+key.capitalize();ap=V/(audit.replace('.','/')+'.lean')
 txt='\n'.join('import TGLExt.'+n for n in names)+'\nset_option pp.universes true\n'+''.join('#check '+t['name']+'\n#print axioms '+t['name']+'\n' for t in targets)
 fresh(ap,txt.encode());documents=[]
 for name in docs:
  for ext in ['.md','.json']:
   p=R/(name+ext);fresh(a/p.name,p.read_bytes());documents.append(pin(p))
 snap=dict(timestamp=now(),scope=key,modules=['TGLExt.'+n for n in names],targets=targets,sources=sources,documents=documents,base_compilations=base,protected=protected,own_auditor=pin(ap),auditor_module=audit,project_objects_inherited_from_author=False,dev_objects_used=False)
 save(a/'snapshot.json',snap);save(out/'SNAPSHOT_POINTER.json',dict(attempt=str(a),snapshot=pin(a/'snapshot.json')))
 print('PINNED',len(sources),'BASE_OBJECTS',len(list((V/'.lake/build/lib/lean').rglob('*.olean'))),'NEW_SOURCES',sum(not x['source_preexisting'] for x in sources),flush=True)
 env=os.environ.copy()
 for k in ['LEAN_PATH','LEAN_SRC_PATH']:env.pop(k,None)
 env['PATH']=str(BIN)+os.pathsep+env.get('PATH','');env['GIT_OPTIONAL_LOCKS']='0'
 n=int(env.get('GIT_CONFIG_COUNT','0'))
 pkgs=load(V/'lake-manifest.json')['packages']
 for i,pkg in enumerate(pkgs,n):
  env[f'GIT_CONFIG_KEY_{i}']='safe.directory';env[f'GIT_CONFIG_VALUE_{i}']=str((V/'.lake/packages'/pkg['name']).resolve()).replace('\\','/')
 env['GIT_CONFIG_COUNT']=str(n+len(pkgs))
 cmd=[str(BIN/'lake.exe'),'build',*snap['modules'],audit];start=time.time()
 with (a/'lake_stdout.txt').open('xb') as stdout,(a/'lake_stderr.txt').open('xb') as stderr:
  proc=subprocess.Popen(cmd,cwd=V,env=env,stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW)
  save(a/'process.json',dict(pid=proc.pid,command=cmd,cwd=str(V),started=now()))
  print('LAKE_STARTED',proc.pid,flush=True);rc=proc.wait()
 run=dict(returncode=rc,elapsed_seconds=time.time()-start,finished=now(),command=cmd,cwd=str(V),streams=[pin(a/'lake_stdout.txt'),pin(a/'lake_stderr.txt')],executables=[pin(BIN/'lake.exe'),pin(BIN/'lean.exe')])
 save(a/'run.json',run);print('LAKE_EXIT',rc,flush=True)
 for p in protected:ck(p)
 for x in sources:ck(x['original']);ck(x['copy'])
 for p in documents:ck(p)
 save(a/'preservation.json',dict(timestamp=now(),protected_count=len(protected),all_unchanged=True,run=pin(a/'run.json')))
 return rc
if __name__=='__main__':sys.exit(main(sys.argv[1]))
