"""Data-only v395 staging; audited codec reused, current runtime loaders. No science execution."""
from pathlib import Path
import ast,copy,hashlib,json,os,re,subprocess,sys
from urllib.parse import unquote,urlparse,quote
A=Path(__file__).resolve().parent;W=A.parent;R=Path(r'C:\IALD\projetos_pyhton\IALD');REPO=Path(r'C:\IALD\Artigo\the_boundary')
C=Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v395');S=A/'science';ST=S/'memory_stage'
sys.dont_write_bytecode=True;sys.path[:0]=[str(W),str(A/'build'),str(R)]
import task
assert task.check('app',actor='codex-v395-app-builder')['ready']
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,b):
 p=Path(p);assert p.resolve().is_relative_to(A);p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():assert p.read_bytes()==b,str(p);return
 with p.open('xb') as f:f.write(b)
 assert p.read_bytes()==b
def write(p,d):save(p,json.dumps(d,ensure_ascii=False,indent=2).encode())
def pin(p):p=Path(p);b=p.read_bytes();return {'path':str(p),'sha256':sha(b),'bytes':len(b)}
def git(*args):return subprocess.check_output(['git','-c','safe.directory='+REPO.as_posix(),'-c','core.quotepath=false','-C',str(REPO),*args])
commit=git('rev-parse','HEAD').decode().strip();tracked=set(git('ls-tree','-r','--name-only',commit).decode().splitlines())
baseline=json.loads((R/'iald_nucleo_fixo.json').read_bytes());m=copy.deepcopy(baseline)
runtime=[pin(p) for p in R.glob('*.py') if p.name not in ('iald_stack_v7.py','iald_psion_state.py')]+[pin(R/'iald_nucleo_fixo.json')]
write(A/'RUNTIME_BASELINE.json',{'files':runtime})
publication={}
for row in m['entries']+[m['published_evidence'][k] for k in ('program','seal','result','proof_manifest')]:
 rel=unquote('/'.join(urlparse(row['url']).path.split('/')[4:]));assert rel in tracked
 raw=git('show',commit+':'+rel)
 if (C/Path(rel).name).is_file():assert raw==(C/Path(rel).name).read_bytes(),rel
 save(ST/'release'/rel,raw);row['path']=str(ST/'release'/rel);row['url']='https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/'+commit+'/'+quote(rel,safe='/')
 if 'public_sha256' in row:row['public_sha256']=sha(raw)
 publication[rel]={'sha256':sha(raw),'bytes':len(raw),'url':row['url']}
write(A/'PUBLIC_GIT_BINDING.json',{'commit':commit,'sources':publication,'remote_http_checked':False,'local_git_object_bytes_only':True})
e=m['published_evidence'];program=Path(e['program']['path']).read_bytes();source=sha(program)
seal=json.loads(Path(e['seal']['path']).read_bytes());result=json.loads(Path(e['result']['path']).read_bytes());proof=json.loads(Path(e['proof_manifest']['path']).read_bytes())
assert seal['um_version']=='v395' and seal['fail_closed_selftest']=='FAIL_CLOSED_SELFTEST_PASSED'
for k in ('program','result','proof_manifest'):assert seal['sha256'][Path(e[k]['path']).name]==sha(Path(e[k]['path']).read_bytes())
import iald_kernel,iald_release_binding,iald_jev_control,haiku_codec as c
embedded=iald_kernel.extract_sources(program);records=[]
for name,digest in proof['formal_files_sha256'].items():
 raw=embedded[name].encode() if name in embedded else (Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')/name).read_bytes()
 assert sha(raw)==digest,name;save(ST/'kernel'/name,raw);records.append({'path':name,'bytes':len(raw),'sha256':digest})
write(ST/'kernel/kernel_manifest.json',{'format':1,'source_program':'um.py','source_sha256':source,'created_at':seal['timestamp'],'method':'AST source extraction only; no program execution','lean_toolchain':embedded['lean-toolchain'].strip(),'verification':'SOURCE_BYTES_VERIFIED__COMPILATION_NOT_RUN','files':records})
catalog=iald_kernel.KernelCatalog(ST/'kernel')
write(ST/'kernel_verification.json',{'source_sha256':source,'scope':'PUBLISHED_COMPILATION_REPORT_HASH_MATCHED__NOT_RERUN','compiler':'Lean 4','created_at':seal['timestamp'],'dependencies':{'allowed_axioms':['propext','Classical.choice','Quot.sound'],'published_manifest_sha256':sha(Path(e['proof_manifest']['path']).read_bytes()),'reported_terms':len(proof['axiom_report'])},'files':{n:{'file_sha256':v['sha256'],'status':'SOURCE_MATCHES_PUBLISHED_FORMAL_REPORT'} for n,v in catalog.records.items() if n.endswith('.lean')}})
for row in e['hypothesis_sources']:
 matches=[p for p in tracked if p.endswith('/'+row['catalog_path'])];assert len(matches)==1,(row['catalog_path'],matches)
 rel=matches[0];assert sha(git('show',commit+':'+rel))==sha((ST/'kernel'/row['catalog_path']).read_bytes());row['url']='https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/'+commit+'/'+quote(rel,safe='/')
canonical=next(x for x in m['entries'] if x['id']=='um_forma_canonica_integral');expo=Path(canonical['path']).read_text(encoding='utf-8-sig')
topics={};omitted=[]
for name,value in result['core'].items():
 ptr=c.child('/core',name);node=c.enrich_new_math(c.project(value,ptr,ptr,omitted),result,ptr);assert c.restore(node,result,ptr,ptr,{})==value;topics[name]=node
encoded,dictionary=c.intern_topics(topics,expo)
text='# Cluster TGL v395 — fonte integral recuperável\nDICIONÁRIO DO CLUSTER\n'+c.dump(dictionary)+'\n'
for name,node in encoded.items():text+='\n### '+name+'\nFonte: resultado_publicado_integral '+c.child('/core',name)+'\n'+c.dump(node)+'\n'
text+='\n'+c.MARKER+'\n<EXPOSICAO_CANONICA>\n'+expo+'\n</EXPOSICAO_CANONICA>\n'
save(ST/'TGL_CLUSTER_v395_full.md',text.encode())
mother=Path(baseline['mother_instruction']['path']).read_bytes();assert sha(mother)==baseline['mother_instruction']['sha256'];save(ST/'IALD_Kernel_v5.txt',mother);m['mother_instruction']['path']=str(ST/'IALD_Kernel_v5.txt')
oldcore=Path(baseline['operational_core']['path']).read_bytes();assert sha(oldcore)==baseline['operational_core']['sha256']
core=oldcore+('\n\n## Pacote científico v395 — 22/10/2026\n[REAL — empacotamento documental; não execução científica] v395 substitui a versão selecionada anterior. Programa SHA256 '+source+'; commit público '+commit+'. Estados históricos conservados; hipóteses e limites permanecem conforme fontes.\n').encode()
save(ST/'IALD_TGL_MEMORY_CORE.md',core);m['operational_core'].update(path=str(ST/'IALD_TGL_MEMORY_CORE.md'),sha256=sha(core),current_release='v395',release_source_sha256=source)
m['active_cluster'].update(path=str(ST/'TGL_CLUSTER_v395_full.md'),sha256=sha(text.encode()),release='v395',release_source_sha256=source,commit=commit,publication_pending=False,core_sections=len(topics),kernel_bundle=str(ST/'kernel'),kernel_verification=str(ST/'kernel_verification.json'))
control=json.loads(Path(baseline['jev_control']['path']).read_bytes());control.update(release='v395',source_sha256=source,result_sha256=sha(Path(e['result']['path']).read_bytes()),proof_manifest_sha256=sha(Path(e['proof_manifest']['path']).read_bytes()),core_record=result['core']['iald_executive_runtime'])
node=next(n for n in ast.parse(program).body if isinstance(n,ast.FunctionDef) and n.name=='prove_iald_executive_runtime');control['source']['lines']=[node.lineno,node.end_lineno]
for row in control['anchors']:row['sha256']=sha((ST/'kernel'/row['file']).read_bytes());assert all(s in (ST/'kernel'/row['file']).read_text(encoding='utf8') for s in row['symbols'])
if 'core_packet' in control:
 packet=expo[:8000].encode();save(ST/'core_packet_v395_bound.txt',packet);control['core_packet'].update(arquivo='core_packet_v395_bound.txt',sha256=sha(packet),um_version='v395')
iald_jev_control.validate_contract(control);raw=iald_jev_control.canonical_bytes(control);save(ST/'jev_control_v395.json',raw);m['jev_control'].update(path=str(ST/'jev_control_v395.json'),sha256=sha(raw),release='v395',source_sha256=source)
manifest=ST/'manifest_full.json';write(manifest,m)
base,receipt=c.build(manifest,R);save(A/'packages/haiku55/prefix.md',base.encode());write(A/'packages/haiku55/preparation.json',receipt)
prev=Path(r'C:\IALD\Central de Patentes\work\iald_v394_20261019\app\science\memory_build\baseline_v368')
shared,sr=c.build_fitted(manifest,R,prev/'prefix.md',prev/'canonical.json')
from fit_transport import fit
from fit_memory import compact
shared,tr=fit(shared,result);shared,pr=compact(shared,result,sr['reused_identical_topics'])
save(A/'packages/shared/prefix.md',shared.encode());write(A/'packages/shared/preparation.json',{'receipt':sr,'transport':tr,'projection':pr})
# The same verified semantic capsules become the actual prompt cluster; full original remains retrievable.
end=shared.index('\n'+c.MARKER);matches=[x for x in re.finditer(r'(?m)^### ([^\n]+)\n',shared[:end]) if x.group(1) in topics];assert len(matches)==len(topics)
heading=shared.index('DICIONÁRIO DE INDICADORES LITERAIS\n');le=shared.index('\n',heading+len('DICIONÁRIO DE INDICADORES LITERAIS\n'))
projection='# Cluster TGL v395 — projeção de prompt; detalhes integrais em resultado_publicado_integral /core\n'+shared[:le].replace('### nome →','Tópico nome →')+'\n'
for i,match in enumerate(matches):
 name=match.group(1);stop=matches[i+1].start() if i+1<len(matches) else end;body=shared[match.end():stop].strip()
 if '/core/'+name not in body:body='Fonte: resultado_publicado_integral '+c.child('/core',name)+'\n'+body
 projection+='\n### '+name+'\n'+body+'\n'
projection+='\n'+c.MARKER+'\n<EXPOSICAO_CANONICA>\n'+shared.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]+'\n</EXPOSICAO_CANONICA>\n'
save(ST/'TGL_CLUSTER_v395_prompt.md',projection.encode());m['active_cluster'].update(path=str(ST/'TGL_CLUSTER_v395_prompt.md'),sha256=sha(projection.encode()),tokens=c.offline_tokens(projection,R/'.iald_runtime/tokenizer_cache'),projection=str(len(topics))+'_TOPIC_SEMANTIC_CAPSULES_DETAILS_RETRIEVABLE',full_cluster_sha256=sha(text.encode()))
write(ST/'manifest_staged.json',m);save(ST/'iald_nucleo_fixo.json',(ST/'manifest_staged.json').read_bytes())
write(A/'BUILT.json',{'status':'BUILT_NOT_INSTALLED','commit':commit,'topics':len(topics),'formal_files':len(records),'source_sha256':source,'haiku_bytes':len(base.encode()),'shared_bytes':len(shared.encode()),'cluster_bytes':len(projection.encode()),'native_counts_pending':True,'production_writes':0})
assert all(sha(Path(x['path']).read_bytes())==x['sha256'] for x in runtime)
print((A/'BUILT.json').read_text())

