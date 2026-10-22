from pathlib import Path
from collections import Counter
import ast,datetime,difflib,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
DEV=Path((REV/'right_graph_core_final_latest_run.txt').read_text().strip())
OUT=REV/('right_graph_core_integrated_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda b:hashlib.sha256(b).hexdigest();hf=lambda p:sha(Path(p).read_bytes());load=lambda p:json.loads(Path(p).read_bytes())
def write(p,b):
 assert p.resolve().is_relative_to(REV) and not p.exists()
 p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp')
 with q.open('xb') as f:f.write(b)
 assert q.read_bytes()==b;q.replace(p)
def save(p,x):write(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def embedded(b):
 t=ast.parse(b);ns=[n for n in t.body if isinstance(n,ast.Assign) and any(isinstance(z,ast.Name) and z.id=='_EMBEDDED_KERNEL_FILES' for z in n.targets)]
 assert len(ns)==1;d=ast.literal_eval(ns[0].value);ns[0].value=ast.Constant('EXCLUDED_EMBEDDED_LEAN')
 return d,ast.dump(t,include_attributes=False)
files=['integration.json','scalar_vna_custody.json','scalar_vna_custody_verification.json','right_graph_core_draft_status.json','RELATORIO_GRAPH_CORE_ADJUNTO_ORIGINAL_F_DEV.md','make_right_graph_core_helpers.py','record_right_graph_core_draft.py','prepare_right_graph_core_stage.py','record_right_graph_core_progress.py','verify_right_graph_core_custody.py','integrate_v350.py','compile_integrated.py','test_gate_extension.py','gate_extension.py']
for n in files:write(OUT/n,(ROOT/n).read_bytes())
P=load(OUT/'scalar_vna_custody.json');PV=load(OUT/'scalar_vna_custody_verification.json');D=load(OUT/'right_graph_core_draft_status.json');I=load(OUT/'integration.json');M=load(DEV/'manifest.json');C=load(DEV/'compilation.json');HS=load(DEV/'verification.json')
assert C['complete'] and C['all_exit_zero'] and C['all_axioms_allowed'] and C['exact_57_targets'] and C['inherited_sources_binaries_preserved'] and C['new_binary_equals_author']
assert 'RIGHT_GRAPH_CORE_DEV_REVIEW' in (REV/'REVIEW_RIGHT_GRAPH_CORE_DEV.md').read_text(encoding='utf-8')
write(OUT/'REVIEW_RIGHT_GRAPH_CORE_DEV.frozen.md',(REV/'REVIEW_RIGHT_GRAPH_CORE_DEV.md').read_bytes())
assert PV['custody_ok'] and PV['custody_sha256']==hf(OUT/'scalar_vna_custody.json')==D['parent_custody_sha256']
assert P['working_sha256']==D['integrated_working_sha256']
assert D==load(DEV/'final_documents/right_graph_core_draft_status.json') and D['report_sha256']==hf(OUT/'RELATORIO_GRAPH_CORE_ADJUNTO_ORIGINAL_F_DEV.md')
assert C['records'][-1]['axioms']==D['targets'] and len(D['targets'])==57
oldum=next(p for p in sorted(ROOT.glob('um.py.bak_*'),reverse=True) if hf(p)==P['working_sha256'])
old,oa=embedded(oldum.read_bytes());raw=(ROOT/'um.py').read_bytes();cur,ca=embedded(raw)
assert oa==ca and sha(raw)==I['working_sha256'] and len(cur)==I['embedded_files']==909
trans={}
for n,d in D['modules'].items():
 key='TGLExt/V350'+n+'.lean';rel='TGLV350/'+n+'.lean';source=ROOT/'kernel'/rel;b=source.read_bytes();integrated=(ROOT/'kernel'/key).read_bytes()
 if rel in M['sources']:
  own_source=M['sources'][rel]['snapshot'];own_binary=next(x for x in C['records'] if x['module']==rel)['command'][2]
 else:
  dep=M['dependencies']['TGLV350.'+n];own_source=dep['frozen_source'];own_binary=dep['frozen_binary']
 assert b==Path(own_source).read_bytes() and sha(b)==d['source_sha256']
 assert hf(ROOT/'build/TGLV350'/(n+'.olean'))==hf(own_binary)==d['binary_sha256']
 assert re.sub(rb'^import TGLV350\.',b'import TGLExt.V350',b,flags=re.M)==integrated and cur[key].encode()==integrated
 write(OUT/'sources'/key,integrated)
 trans[n]={'dev_sha256':sha(b),'integrated_sha256':sha(integrated),'own_olean_sha256':hf(own_binary),'own_source':own_source,'own_binary':own_binary,'literal_import_rewrite_only':True,'embedded_bytes_equal':True,'targets':d['targets']}
newkeys={'TGLExt/V350'+n+'.lean' for n in trans};roots={'TGLExt.lean','TGL/Audit.lean'}
assert set(cur)-set(old)==newkeys and not(set(old)-set(cur)) and {k for k in old if old[k]!=cur[k]}==roots
for key in roots:
 assert (ROOT/'kernel'/key).read_bytes()==cur[key].encode()
 assert all(len(re.findall(r'^import TGLExt\.V350'+n+r'\s*$',cur[key],re.M))==1 for n in trans)
 write(OUT/'sources'/key,cur[key].encode())
 write(OUT/(key.replace('/','_')+'.diff'),''.join(difflib.unified_diff(old[key].splitlines(True),cur[key].splitlines(True),fromfile=key+'.parent',tofile=key)).encode())
oldnames=re.findall(r"^#print axioms ([\w.']+)",old['TGL/Audit.lean'],re.M);newnames=re.findall(r"^#print axioms ([\w.']+)",cur['TGL/Audit.lean'],re.M)
assert len(set(oldnames))==P['audit_declarations']==6982 and len(set(newnames))==7039
assert set(newnames)-set(oldnames)==set(D['targets']) and all(Counter(newnames)[n]==v for n,v in Counter(oldnames).items())
diffs={}
for name in ['integrate_v350.py','compile_integrated.py','test_gate_extension.py']:
 bp=next(p for p in sorted(ROOT.glob(name+'.bak_*'),reverse=True) if hf(p)==P['artifacts'][name])
 a=bp.read_bytes();b=(OUT/name).read_bytes();ast.parse(b)
 write(OUT/(name+'.parent'),a);write(OUT/(name+'.diff'),''.join(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile=bp.name,tofile=name)).encode())
 diffs[name]={'parent_backup':str(bp),'parent_sha256':sha(a),'current_sha256':sha(b)}
assert hf(OUT/'gate_extension.py')==P['artifacts']['gate_extension.py']
helpers={}
for name,pin in HS['helpers'].items():
 assert hf(ROOT/name)==pin['sha256'];ast.parse((ROOT/name).read_bytes());helpers[name]=pin
surfaces={}
for p,h in P['surface_sha256'].items():assert hf(p)==h;surfaces[p]=h
assert len(surfaces)==34
pending=['right_graph_core_custody.json','right_graph_core_custody_verification.json','RELATORIO_GRAPH_CORE_ADJUNTO_ORIGINAL_F_INTEGRADA.md']
assert not any((ROOT/n).exists() for n in pending)
original=hf(ROOT/'fontes/um_v350_original.py');assert original==P['original_sha256']==I['base_sha256']
assert hf(load(ROOT/'environment.json')['original_source'])==original
assert all(hf(p)==h for p,h in P['review_sha256'].items())
assert all(x is False for x in P['remaining_flags'].values())
tree=ast.parse(raw);sel={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['evaluate_quantum_gravity_closure','prove_qg_closure_gate','evaluate_v350_kernel_frontier']};assert len(sel)==3
for name,node in sel.items():write(OUT/'gate_AST'/(name+'.py.txt'),ast.get_source_segment(raw.decode(),node).encode())
evaln=sel['evaluate_quantum_gravity_closure'];assert [a.arg for a in evaln.args.args]==['formal','physics','experiment']
assert not any(isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value.startswith(('qgf_','gpf_')) for n in ast.walk(evaln))
caller=sel['prove_qg_closure_gate'];assigns={n.targets[0].id:n for n in caller.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
assert 'qgc_' in ast.unparse(assigns['formal']) and 'qgp_' in ast.unparse(assigns['physics']) and 'experiment_feed' in ast.unparse(assigns['_feed'])
assert ast.unparse(assigns['gate'].value)=='evaluate_quantum_gravity_closure(formal, physics, experiment)'
annex=next(n for n in caller.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Subscript) and ast.unparse(n.targets[0])=="gate['kernel_frontier']")
assert annex.lineno>assigns['gate'].lineno
save(OUT/'gate_wiring.json',{'evaluator_line':evaln.lineno,'caller_line':caller.lineno,'annex_line':annex.lineno,'six_flags_not_direct_evaluator_inputs':True,'AST_inspection_no_execution':True})
assert all(hf(ROOT/n)==hf(OUT/n) for n in files) and hf(ROOT/'um.py')==I['working_sha256']
S={'timestamp':datetime.datetime.now().astimezone().isoformat(),'mode':'STATIC_ONLY_BUILD_AND_TEST_RESULTS_NOT_CONSUMED','run':str(OUT),'artifact_pins':{n:hf(OUT/n) for n in files},'working_sha256':I['working_sha256'],'parent_working_sha256':P['working_sha256'],'parent_working_backup':str(oldum),'parent_custody_sha256':hf(OUT/'scalar_vna_custody.json'),'original_sha256':original,'canonical_original_freshly_read':True,'embedded_files':len(cur),'new_keys':sorted(newkeys),'changed_existing_keys':sorted(roots),'all_six_literal_import_rewrites':True,'transposition':trans,'python_AST_outside_embedded_equal':True,'python_AST_sha256':sha(ca.encode()),'gate_extension_equal_parent':True,'source_Audit_distinct':len(set(newnames)),'source_Audit_added':57,'source_Audit_parent_multiplicities_preserved':True,'own_DEV_run':str(DEV),'own_DEV_review_sha256':hf(REV/'REVIEW_RIGHT_GRAPH_CORE_DEV.md'),'own_DEV_compilation_sha256':hf(DEV/'compilation.json'),'helpers':helpers,'preparation_diffs':diffs,'surface_pins':surfaces,'surface_count':34,'parent_six_flags':P['remaining_flags'],'future_custody_artifacts_absent':pending,'no_author_code_executed':True,'Lean_executions':0,'live_integrated_compile_gate_tests_evidence_not_read':True,'pending':['author_build_final_notice','final_records_source_binary_log_stream_pins','final_Audit_map_current_and_historical_metadata','final_controls'],'P0':[],'P1':[],'P2':[]}
save(OUT/'static_verification.json',S)
write(REV/'right_graph_core_integrated_latest_run.txt',str(OUT).encode())
print(json.dumps({k:S[k] for k in ['run','working_sha256','embedded_files','all_six_literal_import_rewrites','python_AST_outside_embedded_equal','source_Audit_distinct','source_Audit_added','surface_count','pending']}))
