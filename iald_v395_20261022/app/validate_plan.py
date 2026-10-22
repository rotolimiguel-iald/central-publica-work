"""Offline exact evidence validation and install plan (only after real native counts)."""
from pathlib import Path
from types import SimpleNamespace
import ast,copy,hashlib,json,sys
A=Path(__file__).resolve().parent;W=A.parent;R=Path(r'C:\IALD\projetos_pyhton\IALD');ST=A/'science/memory_stage'
sys.dont_write_bytecode=True;sys.path[:0]=[str(W),str(A/'build'),str(R)]
import task
assert task.check('app',actor='codex-v395-app-builder')['ready']
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,d):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(json.dumps(d,ensure_ascii=False,indent=2).encode())
def pin(p):p=Path(p);return {'path':str(p),'sha256':sha(p.read_bytes())}
import haiku_codec as c,iald_kernel,iald_release_binding,iald_jev_control,iald_core_indexado
from claude_memory_package import load_package
from claude_context_snapshot import load_snapshot,verify_native_tools
from claude_profiles import HAIKU
from iald_motor_claude import converter_pedido
import iald_fontes_publicas,iald_app_memory
m=json.loads((ST/'manifest_staged.json').read_bytes());binding=json.loads((A/'PREPARED_BINDING.json').read_bytes());catalog=iald_kernel.KernelCatalog(ST/'kernel',ST/'kernel_verification.json');tests=[]
def passed(name):tests.append({'name':name,'status':'PASS'})
assert iald_release_binding.load_release(ST/'manifest_staged.json').identity==binding['deployment'];passed('manifest_identity')
proof=json.loads(Path(m['published_evidence']['proof_manifest']['path']).read_bytes())
assert all(sha((ST/'kernel'/n).read_bytes())==v for n,v in proof['formal_files_sha256'].items());passed('1424_sources_sealed_formal_report')
old=json.loads((R/'iald_nucleo_fixo.json').read_bytes());oldc=json.loads(Path(old['jev_control']['path']).read_bytes());newc=iald_jev_control.load_contract(ST)
for k in ('schema','stopping_criterion','memory_admission','decision_metric','holographic_state','switching'):assert oldc[k]==newc[k]
passed('JEV_v2_extensions_preserved_core_packet_verified')
assert Path(m['mother_instruction']['path']).read_bytes()==Path(old['mother_instruction']['path']).read_bytes();assert Path(m['operational_core']['path']).read_bytes().startswith(Path(old['operational_core']['path']).read_bytes());passed('mother_integral_core_additive')
result=json.loads(Path(m['published_evidence']['result']['path']).read_bytes());full=(ST/'TGL_CLUSTER_v395_full.md').read_text(encoding='utf8');dictionary=json.loads(full.split('DICIONÁRIO DO CLUSTER\n',1)[1].split('\n',1)[0]);expo=full.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
blocks=c.source_topics(full,result['core']);assert len(blocks)==425
for name,body in blocks.items():
 ptr=c.child('/core',name);value=c.decode_literals(c.unpack_metadata(json.loads(body.splitlines()[1])),dictionary,expo);assert c.restore(value,result,ptr,ptr,{})==result['core'][name]
passed('425_full_cluster_topics_reconstruct_exact_originals')
docs=iald_core_indexado.DocumentCorpus(ST/'manifest_staged.json')._load();assert len(docs)==8 and json.loads(docs['resultado_publicado_integral']['text'])==result;passed('8_public_sources_complete_result_retrievable')
tools=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()+iald_app_memory.tool_definitions()
rows=json.loads((A/'DATA_PLAN.json').read_bytes())['files']
def add(p,d):rows.append({'source':str(p),'destination':str(d),'sha256':sha(p.read_bytes()),'baseline':sha(d.read_bytes()) if d.exists() else None})
# The runtime loads the named JEV packet relative to app root, not the contract folder.
add(ST/'core_packet_v395_bound.txt',R/'core_packet_v395_bound.txt')
for folder,destname in [('haiku_expanded','haiku55'),('shared','haiku')]:
 root=A/'packages'/folder;pkg=load_package(root,canonical_manifest=ST/'manifest_staged.json',source_sha=catalog.source_sha,expected_model=HAIKU.model)
 _,snapshot=load_snapshot(root,lambda path:load_package(path,canonical_manifest=ST/'manifest_staged.json',source_sha=catalog.source_sha))
 cfg=SimpleNamespace(modelo=HAIKU.model,max_saida=16384,cache_ttl='5m',esforco_claude='medium')
 wire=converter_pedido(cfg,{'model':HAIKU.model,'max_completion_tokens':16384,'messages':[{'role':'system','content':pkg.prefix},{'role':'user','content':'.'}],'tools':tools},prefixo=pkg.prefix)
 verify_native_tools(wire,snapshot,trusted_tools=wire['tools']);passed(folder+'_current_package_snapshot_fixed_and_scoped_tools')
 dest=R/'.iald_runtime'/destname;pm=json.loads((root/'manifest.json').read_bytes());pm['measurement_receipt']=str(dest/'native_count.json');write(root/'manifest_install.json',pm)
 for source,name in [(root/'prefix.md','prefix.md'),(root/'manifest_install.json','manifest.json'),(root/'native_count.json','native_count.json')]:add(source,dest/name)
rc=json.loads((A/'packages/sonnet_public/native_count.json').read_bytes());assert rc['budget']['ready'] and rc['prefix_sha256']==sha((A/'packages/sonnet_public/prefix.md').read_bytes());passed('sonnet_native_count_bound')
add(ST/'manifest_install.json',R/'iald_nucleo_fixo.json')
assert len({x['destination'] for x in rows})==len(rows)
assert not any(Path(x['destination']).parent==R and Path(x['destination']).suffix=='.py' for x in rows);passed('data_only_no_runtime_python_replacement')
assert all(sha(Path(x['path']).read_bytes())==x['sha256'] for x in json.loads((A/'RUNTIME_BASELINE.json').read_bytes())['files']);passed('all_current_runtime_sources_unchanged')
write(W/'install_plan.json',{'files':rows,'deployment_identity':binding['deployment'],'runtime_python_changes':0,'scope':'Data-only immutable science release plus packages, JEV packet and active manifest last','staging_only':True})
write(W/'validation/final_checks.json',{'passed':True,'plan_sha256':sha((W/'install_plan.json').read_bytes()),'tests':tests,'test_count':len(tests),'provider_calls_this_validation':0,'production_mutations':0})
write(A/'DELIVERY_PREPARED.json',{'status':'PREPARED_REVIEW_REQUIRED_NOT_INSTALLED','reference':str(task.REF),'actor':'codex-v395-app-builder','deployment':binding['deployment'],'topics':425,'formal_sources':len(proof['formal_files_sha256']),'files':len(rows),'plan':pin(W/'install_plan.json'),'tests':pin(W/'validation/final_checks.json'),'binding':pin(A/'PREPARED_BINDING.json'),'native_counts':pin(A/'NATIVE_COUNTS_COMPLETE.json'),'runtime_baseline':pin(A/'RUNTIME_BASELINE.json'),'remaining':['Distinct review','Controlled install and effective loading','Real activity/history admission','Live client test separately'],'production_writes':0,'kernel_execution':False})
print(json.dumps({'status':'PASS_PREPARED','tests':len(tests),'files':len(rows)}))
