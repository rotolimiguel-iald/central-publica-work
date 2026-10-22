import pathlib,subprocess,json,hashlib,datetime,ast,sys
sys.stdout.reconfigure(encoding='utf-8')
BASE=pathlib.Path(r'C:\IALD\Central de Patentes\Chatgpt'); ROOT=BASE/'TETELESTAI_V350_KERNEL_20260911'; REV=ROOT/'revisao'
RUN=REV/('reuse_contract_audit_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));RUN.mkdir()
def h(b):return hashlib.sha256(b).hexdigest()
def save(n,x): (RUN/n).write_bytes(json.dumps(x,ensure_ascii=False,indent=2).encode('utf-8'))
queries={
'original_scalar':r'scalarTomitaPolarFactor|ScalarGNSHilbert|scalarRightPairGraph_closure_eq_original',
'reserved_suppliers':r'^\s*(noncomputable\s+)?(def|theorem|lemma|abbrev)\s+(qgFrontier_|qgPrice_|qgStrongCertificate_|qgClosureCertificateV2|qgPhysicsCertificate_)',
'contract_structures':r'^(structure|abbrev) (ContinuousCoreData|TGLModularRealization|FullTGLWitness|ModularRealizationCertificate|QGClosureCertificateStrong)|^.*(def|theorem) .*(: FullTGLWitness|: ContinuousCoreData|: TGLModularRealization)',
'modular_implementations':r'^\s*(noncomputable\s+)?(def|theorem|lemma)\s+\w*(JMJ|commutant|modular|KMS|kms|modPower|continuousCore)\w*',
}
index={}
for name,pattern in queries.items():
 cmd=['rg','-l','--glob','*.lean','--glob','!TETELESTAI_V350_KERNEL_20260911/**','--glob','!**/.lake/**','--glob','!**/build/**',pattern,'.']
 p=subprocess.run(cmd,cwd=BASE,capture_output=True); paths=p.stdout.decode('utf-8',errors='replace').splitlines(); groups={}; errors=[]
 for rel in paths:
  f=BASE/rel
  try:
   b=f.read_bytes(); key=h(b); d=groups.setdefault(key,{'sha256':key,'bytes':len(b),'paths':[]});d['paths'].append(str(f))
  except OSError as e:errors.append({'path':str(f),'error':str(e)})
 save(name+'.json',{'command':cmd,'exit_code':p.returncode,'stderr':p.stderr.decode('utf-8',errors='replace'),'files':len(paths),'unique_sources':len(groups),'groups':list(groups.values()),'read_errors':errors})
 index[name]={'files':len(paths),'unique_sources':len(groups),'errors':len(errors),'rg_stderr':p.stderr.decode('utf-8',errors='replace')[:1000]}
tree=ast.parse((ROOT/'um.py').read_bytes());ls=(ROOT/'um.py').read_text(encoding='utf-8').splitlines(); extracted={}
names={'_QG_CERTIFICATE_FLAGS','_QG_PHYSICS_FLAGS','_QG_FRONTIER_FLAGS','_GRAVITY_PRICE_FLAGS','_V350_MODULAR_CONTRACTS'}
for n in tree.body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets):
  for t in n.targets:
   if isinstance(t,ast.Name) and t.id in names:extracted[t.id]={'line':n.lineno,'value':ast.literal_eval(n.value),'source':'\n'.join(ls[n.lineno-1:n.end_lineno])}
 if isinstance(n,ast.FunctionDef) and (n.name in ['evaluate_quantum_gravity_closure','verify_v350_modular_provenance','evaluate_v350_kernel_frontier']):extracted[n.name]={'line':n.lineno,'source':'\n'.join(ls[n.lineno-1:n.end_lineno])}
save('python_contracts.json',extracted)
save('index.json',index)
print('RUN',RUN);print(json.dumps(index,ensure_ascii=False,indent=2))
