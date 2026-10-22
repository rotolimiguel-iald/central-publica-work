from pathlib import Path
import json,sys,os,hashlib,datetime
W=Path(__file__).resolve().parent;APP=Path(r'C:\IALD\projetos_pyhton\IALD');sys.path.insert(0,str(APP));os.environ['TIKTOKEN_CACHE_DIR']=str(APP/'.iald_runtime/tokenizer_cache')
from iald_memoria_canonica import count_tokens,CanonicalMemory
from iald_kernel import KernelCatalog

def write(p,raw):
 if p.exists():
  b=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));b.write_bytes(p.read_bytes());assert b.read_bytes()==p.read_bytes()
 t=p.with_name(p.name+'.tmp');t.write_bytes(raw);assert t.read_bytes()==raw and raw;t.replace(p)
m=json.loads((W/'manifest_staged.json').read_bytes());prep=json.loads((W/'prepared.json').read_bytes());text=Path(m['active_cluster']['path']).read_text(encoding='utf-8');result=json.loads(Path(m['published_evidence']['result']['path']).read_bytes());refs=prep['secondary_detail_pointers']
cat=KernelCatalog(m['active_cluster']['kernel_bundle']);report={'cluster_tokens':count_tokens(text),'secondary_pointers':len(refs),'all_sections':len(result['core']),'canonical_form_present':Path(next(e for e in m['entries'] if e['id']=='um_forma_canonica_integral')['path']).read_text(encoding='utf-8-sig') in text}
for public in (True,False):
 mem=CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',nucleus_manifest=W/'manifest_staged.json');prefix,meta=mem.prompt('',cat,public=public);key='public' if public else 'operator';write(W/(key+'_prefix.md'),prefix.encode());write(W/(key+'_metadata.json'),json.dumps(meta,ensure_ascii=False,indent=2).encode());report[key+'_tokens']=meta['context_tokens']
write(W/'context_validation.json',json.dumps(report,indent=2).encode());print(json.dumps(report))
