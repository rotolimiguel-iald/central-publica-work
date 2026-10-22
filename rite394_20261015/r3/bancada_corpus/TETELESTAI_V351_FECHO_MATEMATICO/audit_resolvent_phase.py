from pathlib import Path
import datetime,hashlib,json,re,subprocess,sys,os
R=Path(__file__).absolute().parent
STEMS=['V351ResolventPhaseFunctions','V351ResolventPhaseCalculus','V351ResolventImaginaryPowers','V351ResolventImaginaryContinuity','V351ScalarTomitaImaginaryPowers']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,b):
 assert not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True)
 if isinstance(b,str):b=b.encode('utf8')
 q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b and len(b)>0;os.replace(q,p)
records=[];expected_total=0
for stem in STEMS:
 p=R/'kernel/TGLExt'/(stem+'.lean');h=sha(p);text=p.read_text(encoding='utf8')
 declarations=re.findall(r'^#print axioms (\w+)$',text,re.M)
 assert len(set(declarations))==len(declarations)
 assert not re.search(r'\b(?:sorry|native_decide|trustCompiler)\b|^\s*axiom\s',text,re.M)
 good=[]
 for ap in (R/'attempts').glob('*/run.json'):
  d=json.loads(ap.read_bytes())
  if d['source_sha256']==h and d['returncode']==0:good.append(ap.parent)
 assert good,stem
 a=sorted(good)[-1];out=(a/'stdout.txt').read_text(encoding='utf8')
 assert not re.search(r'\b(?:warning|error):',out) and not (a/'stderr.txt').read_bytes()
 rows=re.findall(r"'TGLV350.Regular.(\w+)' depends on axioms: \[([^\]]*)\]",out)
 assert {n for n,_ in rows}==set(declarations) and len(rows)==len(declarations)
 assert all(set(re.findall(r'[\w.]+',axs))<={'propext','Classical.choice','Quot.sound'} for _,axs in rows)
 records.append(dict(module=stem,source=str(p),source_sha256=h,object=str(R/'build/TGLExt'/(stem+'.olean')),object_sha256=sha(R/'build/TGLExt'/(stem+'.olean')),attempt=str(a),declarations=declarations))
 expected_total+=len(declarations)
negatives=[]
for stem,old,new in [
 ('V351ResolventPhaseFunctions','‖resolventPhaseFunction t x‖ = ‖resolventDamping x‖ := by','‖resolventPhaseFunction t x‖ = 2 * ‖resolventDamping x‖ := by'),
 ('V351ScalarTomitaImaginaryPowers','scalarTomitaImaginaryPower P (s+t) x :=','scalarTomitaImaginaryPower P (s-t) x :=')]:
 p=R/'kernel/TGLExt'/(stem+'.lean');txt=p.read_text(encoding='utf8');assert txt.count(old)==1
 probe=R/'probes/TGLExt'/(stem+'Rejected.lean');put(probe,txt.replace(old,new))
 run=subprocess.run([sys.executable,'-X','utf8','-B',str(R/'compile_a1.py'),str(probe)],capture_output=True)
 put(probe.with_suffix('.stdout.txt'),run.stdout);put(probe.with_suffix('.stderr.txt'),run.stderr or b'EMPTY\n')
 out=run.stdout.decode('utf8');assert run.returncode!=0 and 'error:' in out and 'sorryAx' in out
 assert 'object file' not in out and 'unknown module' not in out
 negatives.append(dict(probe=str(probe),sha256=sha(probe),returncode=run.returncode,mutation=[old,new],real_elaboration_failure=True,stdout=str(probe.with_suffix('.stdout.txt'))))
 for rec in records:assert sha(Path(rec['source']))==rec['source_sha256'] and sha(Path(rec['object']))==rec['object_sha256']
previous=[]
for name in ['MANIFESTO_A1.json','MANIFESTO_A1_BASE_SEMIFINITUDE_APROXIMANTES.json','MANIFESTO_A1_AVALIACAO_LEIS_NORMALIDADE.json']:
 p=R/name;d=json.loads(p.read_bytes());files=d.get('files',d.get('artifacts',[]))
 assert files,name
 for f in files:assert sha(Path(f['path']))==f['sha256'],f['path']
 previous.append(dict(path=str(p),sha256=sha(p),verified_files=len(files)))
deps=json.loads((R/'DEPENDENCIAS_A1_FASE_RESOLVENTE.json').read_bytes())
for d in deps:assert sha(Path(d['source']))==d['source_sha256'] and sha(Path(d['object']))==d['object_sha256']
audit=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='AUTHOR_CHECKS_PASS__MODULAR_ACTION_AND_A1B_OPEN',modules=records,checked_declarations=expected_total,allowed_axioms=['propext','Classical.choice','Quot.sound'],negatives=negatives,verified_dependencies=len(deps),prior_manifests_verified=previous,program=dict(path=str(R/'um.py'),sha256=sha(R/'um.py')),full_program_run=False,reason='Only new Lean modules; monolith unchanged. No runtime or gate promotion.')
put(R/'AUDITORIA_A1_POTENCIAS_IMAGINARIAS.json',json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status=audit['status'],declarations=expected_total,modules=len(records),negative_controls=len(negatives),dependencies=len(deps)),indent=2))
