"""Prepare immutable bounded-core release; no imports have filesystem effects."""
from pathlib import Path
import argparse, hashlib, json, re, shutil, sys

def sha(b): return hashlib.sha256(b).hexdigest()
def js(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2).encode('utf-8')+b'\n'
def prepare(descriptor, output):
    sys.path.insert(0, str(Path(__file__).parent / "runtime"))
    sys.path.insert(1, r"C:\IALD\projetos_pyhton\IALD")
    spec=json.loads(Path(descriptor).read_bytes())
    source=Path(spec['source_manifest']); raw=source.read_bytes()
    if sha(raw)!=spec['source_manifest_sha256']: raise ValueError('Source manifest hash mismatch')
    cfg=json.loads(raw); cluster=cfg.get('active_cluster',{}); core=cfg['operational_core']
    origin=cfg.get('source_identity') or {'release':cluster['release'],'source_sha256':cluster['release_source_sha256']}
    result_data=Path(cfg['published_evidence']['result']['path']).read_bytes()
    identity={'release':origin['release'],'source_sha256':origin['source_sha256'],
              'commit':cfg.get('source_commit') or cluster['commit'],'cluster_sha256':sha(result_data),
              'operational_core_sha256':core['sha256'],'jev_sha256':cfg['jev_control']['sha256']}
    for k in ('release','source_sha256','commit'):
        if spec['identity'][k]!=identity[k]: raise ValueError('Descriptor identity mismatch: '+k)
    out=Path(output).resolve()
    if out.exists(): raise ValueError('Output exists; preserve previous candidate, do not overwrite')
    out.mkdir(parents=True)
    artifacts=[]; documents=[]; units=[]
    def put(name,data):
        p=out/name;p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as f:f.write(data)
        if p.read_bytes()!=data:raise ValueError('Write verification failed')
        artifacts.append({'path':name,'sha256':sha(data),'bytes':len(data)})
    def readrecord(r,hashfield='sha256'):
        data=Path(r['path']).read_bytes()
        if sha(data)!=r[hashfield]:raise ValueError('Source changed')
        return data
    # Entire public documents, original raw bytes. No semantic rewriting.
    for e in cfg['entries']:
        data=readrecord(e,'public_sha256'); name='documents/'+e['id']+Path(e['path']).suffix
        put(name,data);documents.append({'id':e['id'],'path':name,'url':e['url'],'role':e['role']})
        text=data.decode('utf-8')
        if e['id']=='resultado_publicado_integral':
            obj=json.loads(data)
            for key,value in obj['core'].items():
                unittext=json.dumps({'core':{key:value}},ensure_ascii=False,indent=2)
                uid='topic_'+sha(key.encode())[:20]
                units.append({'id':uid,'document_id':e['id'],'json_pointer':'/core/'+key.replace('~','~0').replace('/','~1'),
                    'label':key,'text':unittext,'sha256':sha(unittext.encode()),'unit_scope':'WHOLE_JSON_TOPIC_ALL_FIELDS'})
            rest={k:v for k,v in obj.items() if k!='core'}
            ut=json.dumps(rest,ensure_ascii=False,indent=2)
            units.append({'id':'result_global_statutes','document_id':e['id'],'label':'verdict audit timestamp',
                          'text':ut,'sha256':sha(ut.encode()),'unit_scope':'WHOLE_RESULT_GLOBAL_FIELDS'})
        else:
            # Section units only at explicit top-level headings; no equation/paragraph splitting.
            marks=[m.start() for m in re.finditer(r'(?m)^(?:#{1,2} |\\(?:section|chapter)\*?\{)',text)]
            boundaries=sorted(set([0]+marks+[len(text)]))
            for n,(a,b) in enumerate(zip(boundaries,boundaries[1:])):
                if a==b:continue
                ut=text[a:b];uid=e['id']+'_section_'+str(n)
                units.append({'id':uid,'document_id':e['id'],'start_char':a,'end_char':b,
                              'line_start':text.count('\n',0,a)+1,'line_end':text.count('\n',0,b)+1,
                              'text':ut,'sha256':sha(ut.encode()),'unit_scope':'WHOLE_EXPLICIT_SECTION_NOT_ALL_LINKED_SOURCES'})
    program=Path(cfg['published_evidence']['program']['path']).read_bytes()
    if sha(program)!=identity['source_sha256']:raise ValueError('Program pin mismatch')
    put('documents/program.py',program)
    documents.append({'id':'programa_integral','path':'documents/program.py','url':cfg['published_evidence']['program']['url'],
                      'role':'Programa integral somente leitura; não executado'})
    kernelroot=Path(cfg.get('kernel_bundle') or cluster['kernel_bundle']); km=json.loads((kernelroot/'kernel_manifest.json').read_bytes())
    if km['source_sha256']!=identity['source_sha256']: raise ValueError('Kernel source mismatch')
    put('kernel/kernel_manifest.json',(kernelroot/'kernel_manifest.json').read_bytes())
    for r in km['files']:
        data=(kernelroot/r['path']).read_bytes()
        if sha(data)!=r['sha256'] or len(data)!=r['bytes']:raise ValueError('Kernel integrity mismatch')
        put('kernel/'+r['path'],data)
    put('kernel_verification.json',Path(cfg.get('kernel_verification') or cluster['kernel_verification']).read_bytes())
    mother=readrecord(cfg['mother_instruction']); corebytes=readrecord(core)
    put('mother.txt',mother);put('operational_core.md',corebytes)
    documents.extend([{'id':'memoria_mae_integral','path':'mother.txt','role':'Instrução-mãe aprovada do app; não fonte científica nova'},
                      {'id':'nucleo_operacional_integral','path':'operational_core.md','role':'Núcleo operacional aprovado do app'}])
    if cluster.get('release')==identity['release']:
        put('cluster.md',readrecord(cluster))
    put('jev.json',readrecord(cfg['jev_control']))
    for label,entry in cfg['published_evidence'].items():
        if isinstance(entry,dict) and 'path' in entry:
            put('evidence/'+label+Path(entry['path']).suffix,Path(entry['path']).read_bytes())
    full=source.parent/('TGL_CLUSTER_'+identity['release']+'_full.md')
    if cluster.get('release')==identity['release'] and full.is_file():
        fullbytes=full.read_bytes()
        if sha(fullbytes)!=cluster['full_cluster_sha256']:raise ValueError('Full cluster mismatch')
        put('cluster_full.md',fullbytes)
    # Keep complete formal index/topic records and all hypotheses/limits; selection is later.
    put('units.json',js(units))
    from iald_core_indexado import CORE_ADDENDUM
    from iald_response_contract import IDENTITY_PROTOCOL,SOLUTION_PROTOCOL
    prefix=('ACERVO VERSIONADO — CONTEXTO FIXO LIMITADO\n'+js(identity).decode()+
        '\nA versão desta chamada é a identificada acima. O acervo integral permanece imutável e recuperável. '
        'Somente identidade, instrução-mãe, núcleo operacional e regras abaixo estão fixos no prompt. '
        'Referências históricas a cluster/fontes carregadas significam disponíveis por consulta, não lidas nesta chamada. '
        'A seleção documental é parcial: zero resultados não prova ausência. Recupere hipóteses, estatutos, '
        'diz/não diz, limites e erratas vinculadas antes de concluir. Uma página não é fonte integral. '
        'Atualizações concorrentes não mudam esta versão. Não misture versões nem afirme leitura não feita.\n'+
        IDENTITY_PROTOCOL+SOLUTION_PROTOCOL+'\n'+mother.decode('utf-8-sig')+'\n'+corebytes.decode('utf-8-sig')+
        CORE_ADDENDUM.replace('v357',identity['release'])+
        '\nREGRA ATUAL DE RESIDÊNCIA: os termos “carregado” históricos acima não tornam o acervo todo literal; '
        'as ferramentas search_tgl/fetch_tgl e iald_kernel_* consultam exclusivamente esta versão. '
        'Os estatutos das fontes não são alterados pela recuperação.\n')
    if len(prefix.encode())>150000:raise ValueError('Bounded core exceeds limit; no truncation')
    put('prefix.md',prefix.encode())
    native=prefix.replace(mother.decode('utf-8-sig'), '\nInstrução-mãe v5 integral disponível por fetch_tgl memoria_mae_integral; não está literal neste contexto nativo.\n',1)
    put('native_prefix.md',native.encode())
    release={'schema':'iald.science-snapshot.v1','identity':identity,'prefix_file':'prefix.md','native_prefix_file':'native_prefix.md','units_file':'units.json',
             'jev_file':'jev.json','kernel_root':'kernel','kernel_verification':'kernel_verification.json',
             'documents':documents,'artifacts':artifacts,'source_manifest_sha256':sha(raw),
             'coverage':'FULL_ADMITTED_PUBLIC_CORPUS; PARTIAL_PER_CALL_RETRIEVAL',
             'admitted_corpus_coverage':cfg.get('admitted_corpus_coverage',{}),
             'limits':{'fixed_prefix_bytes':150000,'retrieval_bytes':120000,'provider_limits_unchanged':True}}
    put('release.json',js(release))
    return {'identity':identity,'manifest_sha256':sha((out/'release.json').read_bytes()),'prefix_bytes':len(prefix.encode()),
            'artifacts':len(artifacts)-1,'units':len(units),'output':str(out)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--descriptor',required=True);p.add_argument('--output',required=True)
    args=p.parse_args();print(json.dumps(prepare(args.descriptor,args.output),ensure_ascii=False))
if __name__=='__main__':main()
