import ast,datetime,hashlib,json,pathlib,re,sys,os
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911');REV=ROOT/'revisao';R=ROOT/'r'
now=datetime.datetime.now().astimezone();stamp=now.strftime('%Y%m%d_%H%M%S_%f');OUT=REV/('full_runtime_formal_stage_'+stamp);OUT.mkdir()
def sha(b):return hashlib.sha256(b).hexdigest()
def metadata(p):
 b=p.read_bytes();s=p.stat();return {'path':str(p),'bytes':len(b),'sha256':sha(b),'mtime_ns':s.st_mtime_ns,'mtime':datetime.datetime.fromtimestamp(s.st_mtime).astimezone().isoformat()}
def dump(p,x):
 b=json.dumps(x,ensure_ascii=False,indent=2).encode('utf-8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
def capture(p):
 raw=p.read_bytes();t=raw.decode('utf-8-sig').replace('\r\n','\n');head,tail=t.split('--- STDOUT ---\n',1);out,err=tail.split('\n--- STDERR ---\n',1);assert err.endswith('\n');err=err[:-1]
 rc=int(re.search(r'^# returncode: (-?\d+)$',head,re.M).group(1));n,m=map(int,re.search(r'# len\(stdout\)=(\d+) len\(stderr\)=(\d+)',head).groups())
 row=metadata(p)|{'header':head,'returncode':rc,'stdout_characters_declared':n,'stderr_characters_declared':m,'stdout_characters_recovered':len(out),'stderr_characters_recovered':len(err),'lengths_match':len(out)==n and len(err)==m,'stdout_utf8_normalized_sha256':sha(out.encode()),'stderr_utf8_normalized_sha256':sha(err.encode()),'error_lines':[l for l in (out+'\n'+err).splitlines() if re.search(r'(^error:|: error:|^✖)',l)],'warning_count':len(re.findall(r'^warning:',out+'\n'+err,re.M)),'stderr_text':err}
 (OUT/p.name).write_bytes(raw)
 return row,out
contract=json.loads((ROOT/'CONTRATO_ATIVO_GATE_V350.json').read_bytes());proc=json.loads((R/'runtime_process_02.json').read_bytes());prep=json.loads((R/'preparation_status.json').read_bytes())
build,bs=capture(R/'tgl_kernel_build_capture.txt');audit,stream=capture(R/'tgl_kernel_audit_capture.txt')
start=datetime.datetime.fromisoformat(proc['started']);fresh=all(datetime.datetime.fromtimestamp(x['mtime_ns']/1e9,datetime.timezone.utc)>start for x in [build,audit])
raw=(ROOT/'um.py').read_bytes();rawr=(R/'um.py').read_bytes();t=ast.parse(rawr);emb=None;maps={}
for node in t.body:
 if isinstance(node,ast.Assign):
  for target in node.targets:
   if isinstance(target,ast.Name):
    if target.id=='_EMBEDDED_KERNEL_FILES':emb=ast.literal_eval(node.value)
    if target.id in ['_QG_CERTIFICATE_FLAGS','_QG_PHYSICS_FLAGS']:maps[target.id]=ast.literal_eval(node.value)
assert isinstance(emb,dict)
files=[]
for rel,source in emb.items():
 p=R/'tgl_kernel'/rel;assert p.resolve().is_relative_to((R/'tgl_kernel').resolve());b=p.read_bytes();want=source.encode('utf-8');normal=b.decode('utf-8-sig').replace('\r\n','\n')==source.replace('\r\n','\n')
 files.append(metadata(p)|{'embedded_name':rel,'embedded_utf8_sha256':sha(want),'literal_equal':b==want,'text_equal_after_CRLF_normalization':normal})
material=(R/'tgl_kernel/TGL/Audit.lean').read_text(encoding='utf-8-sig');expected_text=emb['TGL/Audit.lean']
# Remove nested Lean block comments and line comments before reading commands.
def code_only(s):
 out=[];i=0;depth=0
 while i<len(s):
  if s.startswith('/-',i):depth+=1;i+=2;continue
  if depth and s.startswith('-/',i):depth-=1;i+=2;continue
  if depth:
   if s[i]=='\n':out.append('\n')
   i+=1;continue
  if s.startswith('--',i):
   j=s.find('\n',i);i=len(s) if j<0 else j;continue
  out.append(s[i]);i+=1
 return ''.join(out)
expected=re.findall(r'^\s*#print\s+axioms\s+([^\s]+)',code_only(expected_text),re.M)
material_expected=re.findall(r'^\s*#print\s+axioms\s+([^\s]+)',code_only(material),re.M)
checks=re.findall(r'^\s*#check\s+@?([^\s]+)',code_only(material),re.M)
pat=re.compile(r"'([\w.']+)'\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)")
def parse_axioms(s):
 rows=[];groups={};conflicts=[]
 for m in pat.finditer(s):
  name=m.group(1);ax=re.findall(r"[\w.']+",m.group(2) or '');fmt='depends' if m.group(2) is not None else 'no_axioms';rows.append({'name':name,'axioms':ax,'format':fmt})
  if name in groups and set(groups[name])!=set(ax):conflicts.append(name)
  groups[name]=ax
 return rows,groups,conflicts
parsed,ax,conflicts=parse_axioms(stream);build_rows,bax,bconf=parse_axioms(bs);allow={'propext','Classical.choice','Quot.sound'}
expected_set=set(expected);missing=sorted(expected_set-set(ax));extra=sorted(set(ax)-expected_set)
gate=[]
for name,prefix in [('_QG_CERTIFICATE_FLAGS','qgc_'),('_QG_PHYSICS_FLAGS','qgp_')]:
 for flag,decl in maps[name].items():
  hits=[];short=decl.rsplit('.',1)[-1]
  for rel,src in emb.items():
   mm=re.search(r'^\s*(?:noncomputable\s+)?(?:def|theorem|lemma)\s+'+re.escape(short)+r'\b',src,re.M)
   if mm:hits.append({'file':rel,'line':src[:mm.start()].count('\n')+1,'materialized_sha256':next(x['sha256'] for x in files if x['embedded_name']==rel)})
  gate.append({'flag':prefix+flag,'declaration':decl,'in_audit_commands':decl in expected_set,'in_fresh_audit':decl in ax,'axioms':ax.get(decl),'allowed':decl in ax and set(ax[decl])<=allow,'source_hits':hits})
old={}
for name in ['tgl_kernel_build_capture.txt','tgl_kernel_audit_capture.txt']:
 p=R/'failed_attempt_01'/name;row,_=capture(p);(OUT/name).write_bytes((R/name).read_bytes());old[name]=row
seed=json.loads((R/'input_manifest.json').read_bytes());seedsummary={k:v for k,v in seed.items() if k!='copied_entries'};seedsummary['copied_entries_count']=len(seed['copied_entries'])
rootbins=[]
for mod in ['TGLExt','TGL/Audit']:
 p=R/'tgl_kernel/.lake/build/lib/lean'/(mod+'.olean')
 rootbins.append(metadata(p) if p.exists() else {'path':str(p),'exists':False})
build_jobs={'completion_messages':re.findall(r'Build completed successfully \([^\n]+',bs),'built_events':len(re.findall(r'^.*\] Built ',bs,re.M)),'replayed_events':len(re.findall(r'^.*\] Replayed ',bs,re.M))}
finding=[]
conditions={'copy_byte_equal':raw==rawr,'copy_matches_contract':sha(raw)==contract['working_sha256']==proc['working_sha256'],'fresh_timestamps':fresh,'build_rc0':build['returncode']==0,'audit_rc0':audit['returncode']==0,'capture_character_lengths_match':build['lengths_match'] and audit['lengths_match'],'no_error_lines':not build['error_lines'] and not audit['error_lines'],'all_embedded_files_materialized_text_equal':all(x['text_equal_after_CRLF_normalization'] for x in files),'embedded_materialized_audit_commands_equal':expected==material_expected,'no_missing_axiom_declarations':not missing,'no_extra_axiom_declarations':not extra,'no_conflicting_duplicate_axioms':not conflicts and not bconf,'all_axioms_allowed':all(set(a)<=allow for a in ax.values()),'gate_11_complete_allowed_unique_source':len(gate)==11 and all(x['in_audit_commands'] and x['in_fresh_audit'] and x['allowed'] and len(x['source_hits'])==1 for x in gate),'build_stream_covers_audit':all(n in bax and set(bax[n])==set(ax[n]) for n in ax)}
for k,v in conditions.items():
 if not v:finding.append({'verification_failed':k})
e={'timestamp':now.isoformat(),'scope':'PARTIAL_FRESH_FORMAL_STAGE_ONLY','new_build_started_by_reviewer':False,'author_session_consumed':False,'process_interrupted':False,'monolith_imported_or_executed_by_reviewer':False,'contract':metadata(ROOT/'CONTRATO_ATIVO_GATE_V350.json'),'root_copy':metadata(ROOT/'um.py'),'run_copy':metadata(R/'um.py'),'process_manifest':metadata(R/'runtime_process_02.json'),'process_manifest_at_read':proc,'preparation':prep,'input_manifest_pin':metadata(R/'input_manifest.json'),'input_manifest_summary':seedsummary,'build_capture':build,'audit_capture':audit,'failed_attempt_01_excluded':old,'embedded_files_count':len(files),'V350_modules_count':sum(x['embedded_name'].startswith('TGLExt/V350') and x['embedded_name'].endswith('.lean') for x in files),'file_comparison':files,'materialized_root_binaries':rootbins,'audit_print_commands_count':len(expected),'audit_unique_requested':len(expected_set),'audit_check_commands_count':len(checks),'checks_without_print_axioms':sorted(set(checks)-expected_set),'parsed_axiom_messages':len(parsed),'parsed_unique':len(ax),'no_axioms_messages':sum(x['format']=='no_axioms' for x in parsed),'no_axioms_unique':sorted({x['name'] for x in parsed if x['format']=='no_axioms'}),'apostrophe_identifiers':sorted(n for n in ax if "'" in n),'missing':missing,'extra':extra,'conflicts':conflicts,'axiom_report':ax,'gate_entries':gate,'build_events':build_jobs,'verification':conditions,'findings':finding,'full_run_selftest_seal_final_jsons_reviewed':False,'pending':'Restante do processo, cálculos/probes/autoteste, selo e JSONs finais; não certificados nesta revisão.'}
# Confirm captures and copies did not change while this finite read ran.
e['snapshots_stable_at_end']=all(sha(pathlib.Path(x['path']).read_bytes())==x['sha256'] for x in [build,audit,e['root_copy'],e['run_copy'],e['contract']])
dump(OUT/'evidence.json',e)
print(json.dumps({'out':str(OUT),'counts':{k:e[k] for k in ['embedded_files_count','V350_modules_count','audit_print_commands_count','audit_unique_requested','audit_check_commands_count','parsed_axiom_messages','parsed_unique','no_axioms_messages']},'checks_without_print_axioms':e['checks_without_print_axioms'][:15],'findings':finding,'verification':conditions,'snapshots_stable_at_end':e['snapshots_stable_at_end']},ensure_ascii=False,indent=2))
