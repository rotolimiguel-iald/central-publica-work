from pathlib import Path
import json,sys,os,hashlib,datetime
W=Path(__file__).resolve().parent;APP=Path(r'C:\IALD\projetos_pyhton\IALD');sys.path.insert(0,str(APP));os.environ['TIKTOKEN_CACHE_DIR']=str(APP/'.iald_runtime/tokenizer_cache')
from iald_memoria_canonica import count_tokens,CanonicalMemory
from iald_kernel import KernelCatalog

def write(p,raw):
 if p.exists():
  backup=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));backup.write_bytes(p.read_bytes());assert backup.read_bytes()==p.read_bytes()
 tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw and raw;tmp.replace(p)
m=json.loads((W/'manifest_staged.json').read_bytes());p=Path(m['active_cluster']['path']);original=p.read_text(encoding='utf-8');memo={};refs=[]
def compress(v,path):
 if isinstance(v,dict) and 'DETAILS_IN_SOURCE' in v:return v
 s=json.dumps(v,ensure_ascii=False,separators=(',',':'))
 if len(s)>240 and isinstance(v,(dict,list,str)):
  if s in memo:
   refs.append({'pointer':path,'same_as':memo[s]});return {'same_as':memo[s]}
  memo[s]=path
 if isinstance(v,dict):return {k:compress(x,path+'/'+k.replace('~','~0').replace('/','~1')) for k,x in v.items()}
 if isinstance(v,list):return [compress(x,path+'/'+str(i)) for i,x in enumerate(v)]
 return v
chunks=original.split('\n### ');out=[chunks[0]+'\nCompactação sem perda semântica: `same_as` indica um conteúdo idêntico já presente sob o ponteiro informado no mesmo JSON; recupere o original integral por fetch_tgl quando precisar. Fórmulas canônicas integrais estão ao final.\n']
for block in chunks[1:]:
 lines=block.split('\n');key=lines[0]
 try:value=json.loads(lines[2])
 except (ValueError,IndexError):out.append(block);continue
 lines[2]=json.dumps(compress(value,'/core/'+key),ensure_ascii=False,separators=(',',':'));out.append('\n'.join(lines))
text='\n### '.join(out)
rawresult=json.loads(Path(m['published_evidence']['result']['path']).read_bytes())
def resolve(path):
 v=rawresult
 for k in path.split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)] if isinstance(v,list) else v[k]
 return v
for ref in refs:assert resolve(ref['pointer'])==resolve(ref['same_as'])
write(p,text.encode());m['active_cluster'].update(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),tokens=count_tokens(text));write(W/'manifest_staged.json',json.dumps(m,ensure_ascii=False,indent=2).encode())
prep=json.loads((W/'prepared.json').read_bytes());prep['cluster']=m['active_cluster'];prep['deduplicated_containers']=refs;write(W/'prepared.json',json.dumps(prep,ensure_ascii=False,indent=2).encode())
cat=KernelCatalog(m['active_cluster']['kernel_bundle']);report={'cluster_tokens':count_tokens(text),'duplicate_references':len(refs),'lossless_references_checked':True}
for public in (True,False):
 mem=CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',nucleus_manifest=W/'manifest_staged.json');prefix,meta=mem.prompt('',cat,public=public);key='public' if public else 'operator'
 write(W/(key+'_prefix.md'),prefix.encode());write(W/(key+'_metadata.json'),json.dumps(meta,ensure_ascii=False,indent=2).encode());report[key+'_tokens']=meta['context_tokens']
write(W/'context_validation.json',json.dumps(report,indent=2).encode());print(json.dumps(report))
