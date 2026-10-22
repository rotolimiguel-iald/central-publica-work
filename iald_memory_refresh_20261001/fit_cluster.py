from pathlib import Path
import json,sys,os,hashlib,datetime
W=Path(__file__).resolve().parent;APP=Path(r'C:\IALD\projetos_pyhton\IALD');sys.path.insert(0,str(APP));os.environ['TIKTOKEN_CACHE_DIR']=str(APP/'.iald_runtime/tokenizer_cache')
from iald_memoria_canonica import count_tokens,CanonicalMemory
from iald_kernel import KernelCatalog

def write(p,raw):
 if p.exists():
  b=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));b.write_bytes(p.read_bytes());assert b.read_bytes()==p.read_bytes()
 t=p.with_name(p.name+'.tmp');t.write_bytes(raw);assert t.read_bytes()==raw and raw;t.replace(p)
m=json.loads((W/'manifest_staged.json').read_bytes());prep=json.loads((W/'prepared.json').read_bytes());p=Path(m['active_cluster']['path']);text=p.read_text(encoding='utf-8');result=json.loads(Path(m['published_evidence']['result']['path']).read_bytes());chunks=text.split('\n### ');out=[chunks[0]+'\nCamadas de memória: a exposição canônica integral e as novas seções permanecem presentes. Em seções anteriores, comentários de andamento (statuses) e tabelas de auditoria ficam disponíveis integralmente no JSON indicado; não interpretar uma remissão como inexistência ou pendência atual. Os estatutos e veredictos mantidos continuam com seu escopo.\n'];refs=[]
for block in chunks[1:]:
 lines=block.split('\n');key=lines[0]
 try:value=json.loads(lines[2])
 except (ValueError,IndexError):out.append(block);continue
 fields={'hashes','runtime_s'}
 if key not in prep['new_sections']:fields|={'statuses','values','residuals','per_series','per_tracer','power_curve','angular_metrics'}
 if isinstance(value,dict):
  for f in fields:
   if f in value and count_tokens(json.dumps(value[f],ensure_ascii=False))>60:
    pointer='/core/'+key+'/'+f;source=result['core'][key][f];refs.append({'pointer':pointer,'items':len(source) if isinstance(source,(dict,list)) else None});value[f]={'DETAILS_IN_SOURCE':pointer,'role':'historical_commentary' if f=='statuses' else 'audit_details'}
 lines[2]=json.dumps(value,ensure_ascii=False,separators=(',',':'));out.append('\n'.join(lines))
text='\n### '.join(out);write(p,text.encode());m['active_cluster'].update(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),tokens=count_tokens(text));write(W/'manifest_staged.json',json.dumps(m,ensure_ascii=False,indent=2).encode());prep['cluster']=m['active_cluster'];prep['secondary_detail_pointers']=refs;write(W/'prepared.json',json.dumps(prep,ensure_ascii=False,indent=2).encode())
cat=KernelCatalog(m['active_cluster']['kernel_bundle']);report={'cluster_tokens':count_tokens(text),'secondary_pointers':len(refs),'all_sections':len(result['core']),'canonical_form_present':Path(next(e for e in m['entries'] if e['id']=='um_forma_canonica_integral')['path']).read_text(encoding='utf-8-sig') in text}
for public in (True,False):
 mem=CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',nucleus_manifest=W/'manifest_staged.json');prefix,meta=mem.prompt('',cat,public=public);key='public' if public else 'operator';write(W/(key+'_prefix.md'),prefix.encode());write(W/(key+'_metadata.json'),json.dumps(meta,ensure_ascii=False,indent=2).encode());report[key+'_tokens']=meta['context_tokens']
write(W/'context_validation.json',json.dumps(report,indent=2).encode());print(json.dumps(report))
