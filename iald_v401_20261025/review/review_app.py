from pathlib import Path
import json,hashlib,sys,re,datetime,ast
B=Path(__file__).resolve().parent.parent;A=B/'app';ST=A/'science/memory_stage';R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode=True;sys.path.insert(0,str(A/'build'));sys.path.insert(0,str(B));import haiku_codec as c,release_cfg
cfg=release_cfg.load(require_commit=True)
REVIEWER=sys.argv[1] if len(sys.argv)>1 else sys.exit('uso: review_app.py <id-do-revisor>  (OUTRO agente: nem o construtor nem o dono)')
assert REVIEWER not in (cfg.owner,cfg.builder),'o revisor deve ser independente'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_bytes())
checks=[]
def check(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise RuntimeError(n)
plan=read(B/'install_plan.json');m=read(ST/'manifest_staged.json');old=read(R/'iald_nucleo_fixo.json');result=read(m['published_evidence']['result']['path']);proof=read(m['published_evidence']['proof_manifest']['path']);seal=read(m['published_evidence']['seal']['path'])
check('seal_program',sha(m['published_evidence']['program']['path'])==seal['sha256']['um.py'])
for row in plan['files']:
 s=Path(row['source']);d=Path(row['destination']);check('pin:'+str(d.relative_to(R)),s.resolve().is_relative_to(B) and d.resolve().is_relative_to(R) and sha(s)==row['sha256'] and (sha(d) if d.exists() else None)==row['baseline'])
check('unique_destinations',len(set(x['destination'] for x in plan['files']))==len(plan['files']))
check('no_runtime_code',all(not (Path(x['destination']).parent==R and Path(x['destination']).suffix=='.py') for x in plan['files']))
check('active_manifest_last',Path(plan['files'][-1]['destination'])==R/'iald_nucleo_fixo.json')
for p in read(A/'RUNTIME_BASELINE.json')['files']:check('runtime_preserved:'+Path(p['path']).name,sha(p['path'])==p['sha256'])
check('mother_bytes',Path(m['mother_instruction']['path']).read_bytes()==Path(old['mother_instruction']['path']).read_bytes())
check('core_additive',Path(m['operational_core']['path']).read_bytes().startswith(Path(old['operational_core']['path']).read_bytes()))
newj=read(m['jev_control']['path']);oldj=read(old['jev_control']['path'])
mutable={'release','source_sha256','result_sha256','proof_manifest_sha256','core_record','source','anchors','core_packet'}
check('jev_all_nonversion_fields_preserved',{k:v for k,v in newj.items() if k not in mutable}=={k:v for k,v in oldj.items() if k not in mutable})
check('jev_real_core',newj['core_record']==result['core']['iald_executive_runtime'])
for name,h in proof['formal_files_sha256'].items():check('formal:'+name,sha(ST/'kernel'/name)==h)
check('formal_count',len(proof['formal_files_sha256'])==len(read(cfg.vault/'tgl_kernel_proof_manifest.json')['formal_files_sha256']))
full=(ST/('TGL_CLUSTER_'+cfg.release+'_full.md')).read_text('utf-8');dictionary=read if False else json.loads(full.split('DICIONÁRIO DO CLUSTER\n',1)[1].split('\n',1)[0]);expo=full.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
blocks=c.source_topics(full,result['core']);check('topic_coverage',len(blocks)==len(result['core'])==len(read(cfg.vault/'um_absoluto.json')['core']))
for name,body in blocks.items():
 ptr=c.child('/core',name);v=c.decode_literals(c.unpack_metadata(json.loads(body.splitlines()[1])),dictionary,expo);check('roundtrip:'+name,c.restore(v,result,ptr,ptr,{})==result['core'][name])
for folder in ['shared','haiku_expanded','sonnet_public']:
 root=A/'packages'/folder;man=read(root/'manifest.json');count=read(root/'native_count.json');prefix=(root/'prefix.md').read_text('utf-8')
 check('count_pin:'+folder,sha(root/'prefix.md')==man['prefix_sha256']==count['prefix_sha256'])
 check('count_budget:'+folder,man['budget']==count['budget'] and count['budget']['fits'] and count['budget']['remaining_tokens']>0)
 check('count_only_public:'+folder,count['generation_requests']==0 and not count['operator_context_sent'] and not count['private_atlas_included'])
 check(cfg.release+'_scientific_qualifiers:'+folder,all(x.lower() in prefix.lower() for x in ['CONDITIONAL','UNINHABITED','BIJECTION','HILBERT','CREDITATION']))
 check('all_prompt_topics:'+folder,set(re.findall(r'(?m)^### ([^\n]+)',prefix)).issuperset(result['core']))
check('release_binding',m['active_cluster']['release']==cfg.release and m['active_cluster']['commit']==cfg.espelho_commit and m['active_cluster']['release_source_sha256']==cfg.um_py_sha256==sha(m['published_evidence']['program']['path']))
check('result_equals_custody',Path(m['published_evidence']['result']['path']).read_bytes()==(cfg.vault/'um_absoluto.json').read_bytes())
check('program_equals_custody',Path(m['published_evidence']['program']['path']).read_bytes()==(cfg.vault/'um.py').read_bytes())
check('runtime_floor_haiku',all(read(A/'packages'/f/'native_count.json')['budget']['remaining_tokens']>=10000 for f in ('shared','haiku_expanded')))
current=read(B/'validation/final_checks.json');check('final_checks_plan',current['passed'] and current['plan_sha256']==sha(B/'install_plan.json'))
r={'status':'PASS','reviewer':REVIEWER,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'plan_sha256':sha(B/'install_plan.json'),'transaction_sha256':sha(B/'transaction.py'),'maintenance_sha256':sha(B/'maintenance.py'),'deploy_controlled_sha256':sha(B/'deploy_controlled.py'),'verify_installed_sha256':sha(B/'verify_installed.py'),'checks':checks,'scope':['Independent artifact and source comparison; not source science execution.',str(len(result['core']))+' full topics reconstruct; actual prompt capsules preserve '+str(len(result['core']))+' headings/current scope; historical details retrieved by pinned source.','Native token counts are custody of six earlier public count-only responses, not repeated by reviewer.','No deploy approval/installation yet; real activity and history admitted at request time.'],'findings':[]}
with (B/'validation/review_final.json').open('x',encoding='utf8') as f:json.dump(r,f,ensure_ascii=False,indent=2)
print(json.dumps({'status':'PASS','checks':len(checks),'plan_files':len(plan['files']),'review_sha256':sha(B/'validation/review_final.json')}))
