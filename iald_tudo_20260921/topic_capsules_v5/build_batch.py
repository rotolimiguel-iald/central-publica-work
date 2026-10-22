"""Local proposal construction from loaded JSON only, immutable inputs."""
import hashlib,json,os,re,socket,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
WORK=ROOT.parent
BASE=WORK/'haiku_reviewed_section_20260922_130747_311801.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def has_ref(v):
    if isinstance(v,dict):return any(k.startswith('@') for k in v) or any(has_ref(x) for x in v.values())
    if isinstance(v,list):return any(has_ref(x) for x in v)
    return False
def save(n,data):
    b=data if isinstance(data,bytes) else data.encode('utf-8');p=ROOT/n;t=ROOT/(n+'.tmp')
    assert not p.exists(),str(p)
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b and len(b)>0
    t.rename(p)
os.environ['TIKTOKEN_CACHE_DIR']=r'C:\IALD\projetos_pyhton\IALD\.iald_runtime\tokenizer_cache'
def deny(*a,**k):raise RuntimeError('Network prohibited')
socket.socket=deny
import tiktoken
enc=tiktoken.get_encoding('o200k_base')
batch_path=ROOT/sys.argv[1]
batch_bytes=batch_path.read_bytes();batch=json.loads(batch_bytes)
base=BASE.read_bytes();text=base.decode('utf-8')
ranking=json.loads((WORK/'topic_capsules_v3/INDEX.json').read_text(encoding='utf-8'))
assert sha(base)==ranking['candidate_sha256']
allowed=[t['topic'] for b in ranking['next_batches'][:2] for t in b['topics']]
matches={m.group(1):m for m in re.finditer(r'(?m)^### ([^\n]+)\nFonte: resultado_publicado_integral ([^\n]+)\n([^\n]+)',text)}
rows=[]
for topic,spec in batch['topics'].items():
    assert topic in allowed
    m=matches[topic];original=m.group(0);o=json.loads(m.group(3));refs={};mapping=[]
    aux=spec.get('aux',[]);keep=spec.get('keep',[])
    for k,v in o.items():
        if has_ref(v):
            refs[k]=v;action='REFERENCE_UNCHANGED';why='Estrutura original integral inclusive fields/items/literais/spans; nao expandida.'
        elif k in aux:
            refs[k]={'@':'/'+k};action='AUXILIARY_RECOVERABLE';why='Residuo, serie, conversao redundante ou fingerprint auxiliar; nao substitui conclusao/controle.'
        elif k in keep or isinstance(v,(int,float,bool)):
            refs[k]=v;action='VALUE_UNCHANGED';why='Valor/flag central mantido literalmente, sem novo calculo.'
        elif k in ('selo','seals','verdict'):
            refs[k]={'@':'/'+k};action='SEAL_RECOVERABLE';why='Rotulo integral recuperavel; proposicoes, estatutos e limites explicitados na sintese.'
        else:
            action='SEMANTIC_CONDENSATION';why='Conteudo condensado na sintese; nenhuma expansao de conteudo nao carregado. Revisao independente exigida.'
        mapping.append({'field':'/'+k,'source_pointer':m.group(2)+'/'+k,'original_value':v,'action':action,'justification':why,'destination':'references/'+k if k in refs else 'synthesis'})
    cap='### '+topic+'\nFonte: resultado_publicado_integral '+m.group(2)+'\n'+spec['summary']+'\nRemissões/valores (relativos ao tópico; destinos internos preservados):\n'+json.dumps(refs,ensure_ascii=False,separators=(',',':'))+'\n'
    cb=cap.encode('utf-8');ob=original.encode('utf-8');start=len(text[:m.start()].encode('utf-8'))
    assert base[start:start+len(ob)]==ob
    for k,v in o.items():
        if has_ref(v):assert refs[k]==v
    row={'rank':16+allowed.index(topic),'topic':topic,'original_o200k':len(enc.encode(original)),'capsule_o200k':len(enc.encode(cap)),'capsule_sha256':sha(cb),'original_sha256':sha(ob)}
    row['saved_o200k']=row['original_o200k']-row['capsule_o200k'];rows.append(row)
    prov={'status':'CONSTRUCAO_NAO_APROVADA_NAO_INTEGRADA','candidate_path':str(BASE),'candidate_sha256':sha(base),'original_byte_span':[start,len(ob)],'capsule_byte_span':[0,len(cb)],'source_pointer':m.group(2),'measurement':row,'field_map':mapping,'construction_spec_path':str(batch_path),'construction_spec_sha256':sha(batch_bytes),'limits':['Somente conteudo efetivamente carregado; sem fonte expandida.','Igualdade estrutural de remissoes nao valida resolucao operacional nem coordenadas apos integracao.','Fidelidade semantica depende de revisao independente; nao certificada pelo construtor.','o200k local nao estima Anthropic; sem API/rede/execucao um.py/Lean.']}
    save(topic+'.md',cb);save(topic+'.original.md',ob);save(topic+'.provenance.json',json.dumps(prov,ensure_ascii=False,indent=2))
assert BASE.read_bytes()==base and batch_path.read_bytes()==batch_bytes
idx={'status':'PENDING_INDEPENDENT_REVIEW','batch':batch['batch'],'topics':rows,'totals':{k:sum(r[k] for r in rows) for k in ('original_o200k','capsule_o200k','saved_o200k')},'candidate_sha256':sha(base),'anthropic_measured':False,'integrated':False}
tag='batch_'+str(batch['batch'])
save(tag+'_index.json',json.dumps(idx,ensure_ascii=False,indent=2))
report='# V5 — lote '+str(batch['batch'])+'\n\nPropostas nao aprovadas nem integradas. Base original pinada; referencias existentes preservadas sem expansao. Originais e proveniencia campo a campo acompanham cada capsula.\n\n| Rank | Topico | Original | Capsula | Economia o200k |\n|---:|---|---:|---:|---:|\n'
report+='\n'.join(f"| {r['rank']} | {r['topic']} | {r['original_o200k']} | {r['capsule_o200k']} | {r['saved_o200k']} |" for r in rows)
report+='\n\nTotais: '+str(idx['totals'])+'. Nenhuma conversao para Claude. Nao foi feita validacao operacional dos ponteiros. Estatutos e negativos historicos mantidos no escopo do registro, sem fechamento por inferencia. Nao foi alterado nenhum dos quinze anteriores, exposicao, kernel, core ou Lean.\n'
save(tag+'_report.md',report)
print(json.dumps(idx,ensure_ascii=False,indent=2))
