import hashlib
import json
from pathlib import Path
import subprocess
import sys
sys.dont_write_bytecode=True
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
PUBLIC=Path(r'C:\IALD\Artigo\the_boundary')
WORK=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from iald_memoria_canonica import CanonicalMemory,count_tokens
from iald_kernel import KernelCatalog
files=subprocess.check_output(['git','-C',str(PUBLIC),'ls-files','-z']).decode().split('\0')
def find(name):
    hits=[p for p in files if p and Path(p).name==name]
    assert len(hits)==1,(name,hits)
    return PUBLIC/hits[0]
selected={}
for line in (ROOT/'.env').read_text(encoding='utf-8-sig').splitlines():
    key,sep,value=line.partition('=')
    if key in ('IALD_KERNEL_BUNDLE','IALD_OPENAI_JANELA'): selected[key]=value.strip()
catalog=KernelCatalog(selected['IALD_KERNEL_BUNDLE'])
proof=json.loads(find('tgl_kernel_proof_manifest.json').read_bytes())
formal={k:v for k,v in proof['formal_files_sha256'].items() if k.endswith('.lean')}
missing=[k for k in catalog.records if k.endswith('.lean') and k not in formal]
different=[k for k,v in catalog.records.items() if k in formal and v['sha256']!=formal[k]]
extra=[k for k in formal if k not in catalog.records]
assert not missing and not different,(missing,different)
manifest=json.loads((ROOT/'iald_nucleo_fixo.json').read_bytes())
for entry,name in zip(manifest['entries'][4:],['um_absoluto_pt.txt','um_absoluto_forma_canonica.md','um_absoluto_selo.json']):
    entry['path']=str(find(name))
    entry['id']=entry['id'].replace('_local','_publicado')
    entry['role']='Texto integral publicado da rodada identificada no selo, relido nesta requisição. Consulta documental; não é uma execução nova.'
manifest['published_evidence']={key:{'path':str(find(name))} for key,name in
    [('program','um.py'),('seal','um_absoluto_selo.json'),('result','um_absoluto.json'),('proof_manifest','tgl_kernel_proof_manifest.json')]}
from urllib.parse import quote
commit=subprocess.check_output(['git','-C',str(PUBLIC),'rev-parse','HEAD'],text=True).strip()
for entry in manifest['entries']+list(manifest['published_evidence'].values()):
    relative=Path(entry['path']).relative_to(PUBLIC).as_posix()
    assert relative in files
    entry['url']='https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/'+commit+'/'+quote(relative,safe='/')
for name,data in [('iald_nucleo_fixo.json',manifest)]:
    with (WORK/name).open('x',encoding='utf-8') as f: json.dump(data,f,ensure_ascii=False,indent=2)
memory=CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',nucleus_manifest=WORK/'iald_nucleo_fixo.json')
prompt,info=memory.prompt('',catalog)
report={'remote_commit':commit,'kernel':catalog.status(),'proof_lean_files':len(formal),'matched_lean_files':len(formal)-len(extra),
    'extra_formal_files':extra,'old_window':int(selected['IALD_OPENAI_JANELA']),
    'new_context_tokens_before_evidence':info['context_tokens'],'nucleus':info,
    'baseline':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['iald_memoria_canonica.py','iald_nucleo_fixo.json','iald_web_server.py','iald_motores.py']}}
with (WORK/'source_inspection.json').open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
print(json.dumps({k:v for k,v in report.items() if k not in ('nucleus','baseline')},ensure_ascii=False))
