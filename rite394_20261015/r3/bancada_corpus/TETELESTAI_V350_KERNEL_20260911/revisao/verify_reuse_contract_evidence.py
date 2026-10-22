import ast,pathlib,json,hashlib,re,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911');BASE=ROOT.parent
RUN=ROOT/'revisao/reuse_contract_audit_20260913_080142_579115'
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def js(p):return json.loads(pathlib.Path(p).read_bytes())
def save(n,x):
 p=RUN/n; assert not p.exists();b=json.dumps(x,ensure_ascii=False,indent=2).encode('utf-8'); t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
pins={}
def pin(p):pins[str(p)]=sha(p);return pins[str(p)]
cust=js(ROOT/'paired_blocks_custody.json');e=js(ROOT/'kernel_incremental_evidence.json');a=js(ROOT/'AUDITORIA_REUSO_GATE_20260913/gate_evidence.json');inv=js(ROOT/'AUDITORIA_REUSO_GATE_20260913/external_source_reuse.json');base=js(ROOT/'fontes/um_absoluto.json')
for p in [ROOT/'paired_blocks_custody.json',ROOT/'um.py',ROOT/'gate_extension.py',ROOT/'kernel_incremental_evidence.json',ROOT/'integrated_compile.json',ROOT/'gate_tests.json',ROOT/'fontes/um_absoluto.json',ROOT/'audit_existing_gate_reuse.py',ROOT/'AUDITORIA_REUSO_GATE_20260913/gate_evidence.json',ROOT/'AUDITORIA_REUSO_GATE_20260913/external_source_reuse.json']:pin(p)
assert pins[str(ROOT/'um.py')]==cust['working_sha256']==a['working_sha256']
assert pins[str(ROOT/'paired_blocks_custody.json')]==a['parent_custody_sha256']
assert pins[str(ROOT/'kernel_incremental_evidence.json')]==cust['artifacts']['kernel_incremental_evidence.json']
tree=ast.parse((ROOT/'um.py').read_bytes());maps={};embed=None
for n in tree.body:
 if isinstance(n,ast.Assign):
  for t in n.targets:
   if isinstance(t,ast.Name):
    if t.id in ['_QG_CERTIFICATE_FLAGS','_QG_PHYSICS_FLAGS','_QG_FRONTIER_FLAGS','_GRAVITY_PRICE_FLAGS','_V350_MODULAR_CONTRACTS']:maps[t.id]=ast.literal_eval(n.value)
    if t.id=='_EMBEDDED_KERNEL_FILES':embed=ast.literal_eval(n.value)
g=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='evaluate_quantum_gravity_closure')
gets={x:[] for x in ['formal','physics','experiment']}
for n in ast.walk(g):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='get' and isinstance(n.func.value,ast.Name):
  k=n.func.value.id;assert k in gets;assert isinstance(n.args[0],ast.Constant);gets[k].append(n.args[0].value)
assert set(gets['formal'])==set(maps['_QG_CERTIFICATE_FLAGS']) and set(gets['physics'])==set(maps['_QG_PHYSICS_FLAGS'])
assert len(gets['experiment'])==4 and not any(k.startswith(('qgf_','gpf_')) for v in gets.values() for k in v)
auditrec=next(x for x in js(ROOT/'integrated_compile.json')['records'] if pathlib.Path(x['source']).name=='Audit.lean')
assert auditrec['returncode']==auditrec['lean_returncode']==0 and auditrec['source_unchanged_during_compile'] and auditrec['output_exists']
assert pin(auditrec['source'])==auditrec['sha256'];assert pin(auditrec['command'][2])==auditrec['output_sha256']
stdout=pathlib.Path(auditrec['stdout']);stream=stdout.read_text(encoding='utf-8');assert pin(stdout)==e['audit_stdout_sha256']==e['audit_capture_sha256_full']==cust['current_audit_stdout_sha256']
log=stdout.with_name(stdout.name.replace('.stdout.txt','.json'));assert js(log)==auditrec;pin(log)
ax={n:re.findall(r'[\w.]+',body) for n,body in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",stream,re.S)}
for n in re.findall(r"'([\w.']+)' does not depend on any axioms",stream):ax.setdefault(n,[])
assert {k:set(v) for k,v in ax.items()}=={k:set(v) for k,v in e['axiom_report'].items()}
allowed={'propext','Classical.choice','Quot.sound'}
rows=[]
for x in a['entries']:
 p=pathlib.Path(x['source']['file']);assert pin(p)==x['source']['sha256'];rel=p.relative_to(ROOT/'kernel').as_posix();assert p.read_text(encoding='utf-8').replace('\r\n','\n')==embed[rel].replace('\r\n','\n')
 assert e[x['flag']] is True and set(ax[x['declaration']])==set(x['axioms'])<=allowed
 assert base['core']['kernel_formalization'][x['flag']] is True
 rows.append(x)
assert len(rows)==11
feed=base['core']['void_floor_v11']['experiment_feed'];assert all(feed.get(k) is True for k in gets['experiment'])
assert a['gate_result']==base['core']['qg_closure']['gate']=={'mathematical_model_constructed':True,'physical_quantum_gravity_constructed':True,'empirical_test_completed':True,'full_static_witness_exists':False,'verdict':js(ROOT/'gate_tests.json')['legacy_gate']}
assert len(a['tests'])==12 and len([s for s in a['tests'] if s.startswith('remove_')])==11
assert not inv['failures'] and inv['paths_inventoried']==inv['files_read']==50571 and inv['distinct_byte_hashes']==1281
assert len(inv['matches'])==inv['distinct_matching_hashes']==398
assert sum(len(m['paths']) for m in inv['matches'])==inv['matching_paths']==29524
assert len({f for m in inv['matches'] for f in m['embedded_files']})==398
def norm(b):
 t=b.decode('utf-8-sig').replace('\r\n','\n'); m=re.search(r'^import\s',t,re.M)
 if m:t=t[m.start():]
 return hashlib.sha256(t.strip().encode()).hexdigest()
selected=['StrongAssembly','SolderField','EmergentEinstein','TheCoinage','PhysicsCertificates','FrontierCertificate','TheConditionalCertificate','TheProfileDuality','TheImportedCommutation','ModularPower','ModularFlowSpectrum','ModularSquare','TowerModular','TheImportedEquilibrium','TheMasterFires','TriadMaster','TheRootOfTheProofTree','ModularRealization','BenchCertificate','WitnessV3']
reuse=[]
for short in selected:
 name=('TGL/' if short=='ModularRealization' else 'TGLExt/')+short+'.lean';p=ROOT/'kernel'/name;pin(p)
 found=[m for m in inv['matches'] if name in m['embedded_files']]
 if found:
  m=found[0];ext=pathlib.Path(min(m['paths'],key=lambda s:(len(pathlib.Path(s).parts),len(s),s)))
  assert not ext.is_relative_to(ROOT);assert pin(ext)==m['sha256'];assert norm(ext.read_bytes())==norm(embed[name].encode())==m['normalized_sha256']
  reuse.append({'module':name,'external_source':str(ext),'external_sha256':sha(ext),'current_source':str(p),'current_sha256':sha(p),'normalized_sha256':norm(ext.read_bytes()),'literal_bytes_equal':ext.read_bytes()==p.read_bytes(),'external_copies_reported':len(m['paths'])})
 else:reuse.append({'module':name,'external_normalized_match_in_author_inventory':False})
 # Full declarations, not their proofs, captured for type/provenance inspection.
 ls=p.read_text(encoding='utf-8').splitlines();heads=[]
 for i,line in enumerate(ls):
  if re.match(r'(?:noncomputable )?(?:theorem|def|lemma|abbrev|structure) ',line):
   end=next((j for j in range(i,min(i+60,len(ls))) if ':=' in ls[j] or (j>i and ls[j].startswith('/--'))),min(i+20,len(ls)-1))
   heads.append({'line':i+1,'text':'\n'.join(ls[i:end+1])})
 save(short+'_declarations.json',heads)
for name in ['V350ModularCertificate','V350GateContract','V350WedgeModularData','V350CoreContractCounterexample']:pin(ROOT/'kernel/TGLExt'/f'{name}.lean')
for names in maps['_V350_MODULAR_CONTRACTS'].values():
 for n in names:assert n in ax and set(ax[n])<=allowed
readonly=all(sha(p)==h for p,h in cust['surface_sha256'].items())
assert readonly
original=pathlib.Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py');assert pin(original)==cust['original_sha256']
save('independent_verification.json',{'timestamp':datetime.datetime.now().astimezone().isoformat(),'status':'STATIC_CONTRACT_AND_EVIDENCE_REUSE_AUDIT','pins':pins,'gate_get_keys':gets,'gate_line':g.lineno,'gate_end_line':g.end_lineno,'gate_AST_sha256':hashlib.sha256(ast.dump(g,include_attributes=False).encode()).hexdigest(),'maps':maps,'entries':rows,'current_audit_record':auditrec,'current_audit_entries':len(ax),'current_audit_log':str(log),'original_preserved':True,'parent_34_surface_pins_preserved':readonly,'experimental_feed_provenance':'Historical baseline read; no rerun or new empirical validation','baseline_experimental_keys':{k:feed[k] for k in gets['experiment']},'source_samples_verified':reuse,'author_inventory_counts_arithmetically_consistent':True,'author_inventory_full_read_not_repeated':True,'author_ablation_code_read_not_reexecuted':True,'no_monolith_or_author_helper_executed':True,'new_Lean_compiles_in_reuse_audit':0,'additional_original_S_goal_not_gate_input':True})
print(json.dumps({'verified_entries':len(rows),'current_Audit':len(ax),'reuse_samples':len(reuse),'report_inputs':str(RUN),'original_preserved':True,'surface34_preserved':True},ensure_ascii=False))
