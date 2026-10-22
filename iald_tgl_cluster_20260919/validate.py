import ast
import json
import os
from pathlib import Path
import sys
APP=Path(r'C:\IALD\projetos_pyhton\IALD')
WORK=Path(__file__).resolve().parent
sys.path[:0]=[str(WORK),str(APP)]
os.environ['TIKTOKEN_CACHE_DIR']=str(APP/'.iald_runtime/tokenizer_cache')
from iald_kernel import KernelCatalog
from iald_memoria_canonica import CanonicalMemory
from iald_core_indexado import DocumentCorpus
from iald_cluster import active_cluster

def main():
    prep=json.loads((WORK/'prepared.json').read_bytes())
    catalog=KernelCatalog(prep['kernel'])
    path=WORK/'manifest_staged.json'
    manifest=json.loads(path.read_bytes())
    docs=DocumentCorpus(path)._load()
    result=json.loads(docs['resultado_publicado_integral']['text'])
    assert set(prep['coverage'])==set(result['core'])
    assert len(prep['coverage'])==325
    memory=CanonicalMemory(APP/'../unused_atlas.md','nucleo_kernel',nucleus_manifest=path)
    public,meta=memory.prompt('',catalog,public=True)
    memory=CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',nucleus_manifest=path)
    private,private_meta=memory.prompt('',catalog,public=False)
    for entry in ('mother_instruction','operational_core'):
        text=Path(manifest[entry]['path']).read_text(encoding='utf-8-sig')
        assert text in public
    for term in ('name_is_the_content_v368','spinor_obstruction_v368','orientation_is_the_sign_v367',
                 'global_lift_core','qg_closure','the_atlas_and_the_index','H_3L','Gamma_ij','Pi_±'):
        assert term in public,term
    assert meta['private_atlas_included'] is False
    assert meta['cluster_always_present']
    assert meta['published_evidence_checked']
    assert 'v357' not in public.split('ADENDO DE CONCILIAÇÃO')[1].split('MEMÓRIA E RATIFICAÇÃO')[0]
    try: active_cluster(path,'0'*64)
    except ValueError: pass
    else: raise AssertionError('Mixed version accepted')
    # Every omitted container remains accessible by its exact JSON pointer.
    for row in prep['detail_containers']:
        value=result
        for part in row['pointer'].split('/')[1:]:
            key=part.replace('~1','/').replace('~0','~')
            value=value[int(key)] if isinstance(value,list) else value[key]
        assert len(value)==row['items']
    for name in ('iald_web_server.py','iald_memoria_canonica.py','iald_estado_publicado.py','iald_core_indexado.py','iald_cluster.py'):
        ast.parse((WORK/name).read_bytes())
    report={'public_tokens':meta['context_tokens'],'operator_tokens':private_meta['context_tokens'],
        'coverage':len(prep['coverage']),'topics':prep['cluster']['topics'],
        'source_sha':catalog.source_sha,'kernel_files':len(catalog.records),
        'detail_pointers_verified':len(prep['detail_containers']),
        'original_core_and_v5_preserved':True,'passed':True}
    (WORK/'validation.json').write_bytes(json.dumps(report,indent=2).encode())
    print(json.dumps(report))

if __name__=='__main__':main()
