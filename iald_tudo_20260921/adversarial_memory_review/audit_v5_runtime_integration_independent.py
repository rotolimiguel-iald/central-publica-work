"""Read-only audit of V5/runtime integration. Does not import builders/verifiers."""
import hashlib,json,re
from pathlib import Path
from datetime import datetime,timezone
WORK=Path(__file__).resolve().parent.parent
TARGET=WORK/'haiku_reviewed_runtime_20260922_140939_606120.md'
READ={}
def read(p):
    p=Path(p).resolve()
    assert p.is_relative_to(WORK.resolve()),f'Outside audit scope: {p}'
    b=p.read_bytes();READ[p]=b;return b
def sha(b):return hashlib.sha256(b).hexdigest()
def document(p):return json.loads(read(p))
raw=read(TARGET);receipt=document(TARGET.with_suffix('.json'))
assert sha(raw)==receipt['sha256'] and receipt['runtime_synthesis_compaction']
parent=Path(receipt['parent_path']);parent_raw=read(parent)
assert sha(parent_raw)==receipt['parent_sha256']
runtime_review_raw=read(receipt['review_path']);runtime_review=json.loads(runtime_review_raw)
assert sha(runtime_review_raw)==receipt['review_sha256']
assert runtime_review['status']=='APROVADA_FIDELIDADE_DOCUMENTAL' and not runtime_review['remaining_required_changes']
original=read(receipt['original_path']);capsule=read(receipt['capsule_path'])
assert sha(original)==receipt['original_sha256']==runtime_review['pins']['original.md']['sha256']
assert sha(capsule)==receipt['capsule_sha256']==runtime_review['pins']['capsule_v2.md']['sha256']
heading,body=capsule.decode('utf-8').split('\n',1)
replacement=heading+'\n\n**Estatutos [runtime_synthesis]**\n'+body.lstrip('\n')
assert receipt['replacement']==replacement
text=raw.decode('utf-8');pt=parent_raw.decode('utf-8')
def exposure(t,n):
    headings=list(re.finditer(r'(?m)^## Exposição canônica integral: fórmulas e derivações\r?$',t))
    assert len(headings)==1
    return t[headings[0].end():headings[0].end()+n]
oldexp=exposure(pt,receipt['old_exposition_chars']);newexp=exposure(text,receipt['new_exposition_chars'])
assert sha(oldexp.encode())==receipt['old_exposition_sha256']
assert sha(newexp.encode())==receipt['new_exposition_sha256']
start=receipt['section_start'];end=start+receipt['old_length'];delta=len(newexp)-len(oldexp)
assert oldexp[start:end]==original.decode('utf-8')
assert newexp==oldexp[:start]+replacement+oldexp[end:]
label='**Estatutos [runtime_synthesis]**'
assert newexp.count(label)==1
summary_span=[newexp.index(label),len(replacement)-replacement.index(label)]
assert summary_span==receipt['summary_span']

# Determine the owning topic for each JSON line from actual parent headings.
owners={};current=''
for line in pt.splitlines(keepends=True):
    if line.startswith('Fonte: resultado_publicado_integral '):current=line.split(' ',2)[2].strip()
    owners[line]=current
changed_anchors=0;converted=0
def esc(k):return k.replace('~','~0').replace('/','~1')
def compare(before,after,path,topic):
    global changed_anchors,converted
    if isinstance(before,list):
        assert isinstance(after,list) and len(before)==len(after)
        for i,(a,b) in enumerate(zip(before,after)):compare(a,b,path+'/'+str(i),topic)
    elif isinstance(before,dict):
        assert isinstance(after,dict)
        if '@EXPOSITION' in before or '@SUMMARY' in before:
            a,n=before['span'];b,m=after['span']
            assert all(type(x) is int for x in (a,n,b,m))
            assert 0<=a<a+n<=len(oldexp) and 0<=b<b+m<=len(newexp)
            frag=oldexp[a:a+n]
            expected=before.get('starts_with') if '@EXPOSITION' in before else '**Estatutos ['+before['@SUMMARY']+']**'
            assert frag.startswith(expected)
            if a+n<=start or a>=end:
                assert newexp[b:b+m]==frag and m==n
                assert b==(a if a+n<=start else a+delta)
                assert {k:v for k,v in before.items() if k!='span'}=={k:v for k,v in after.items() if k!='span'}
            else:
                assert start<=a and a+n<=end,'Crossing reference boundary'
                assert '@EXPOSITION' in before and oldexp.count(frag)>=1
                if '@SUMMARY' in after:
                    assert frag not in newexp
                    assert after=={'@SUMMARY':'runtime_synthesis','source_pointer':path,'span':summary_span}
                    converted+=1
                else:
                    assert newexp.count(frag)==1 and newexp[b:b+m]==frag
                    assert {k:v for k,v in before.items() if k!='span'}=={k:v for k,v in after.items() if k!='span'}
            changed_anchors+=before!=after
            return
        assert set(before)==set(after)
        for k,v in before.items():
            if k=='fields' and '@' in before:
                assert isinstance(v,dict) and set(v)==set(after[k])
                for pointer,leaf in v.items():compare(leaf,after[k][pointer],topic+before['@']+pointer,topic)
            else:compare(v,after[k],path+'/'+esc(k),topic)
    else:assert before==after and type(before)==type(after)

for row in receipt['reference_lines']:
    assert pt.count(row['before'])==1 and text.count(row['after'])==1
    topic=owners[row['before']]
    compare(json.loads(row['before']),json.loads(row['after']),topic,topic)
assert converted==3 and changed_anchors==len(receipt['reference_changes'])
# Full scan includes unchanged references, not merely receipt-listed updates.
counts={'literal':0,'summary':0,'runtime_summary':0}
def scan(v):
    if isinstance(v,list):
        for x in v:scan(x)
    elif isinstance(v,dict):
        if '@EXPOSITION' in v or '@SUMMARY' in v:
            a,n=v['span'];assert type(a)is int and type(n)is int and 0<=a<a+n<=len(newexp)
            frag=newexp[a:a+n]
            if '@EXPOSITION' in v:assert frag.startswith(v['starts_with']);counts['literal']+=1
            else:
                assert frag.startswith('**Estatutos ['+v['@SUMMARY']+']**') and v['source_pointer'].startswith('/core/')
                counts['summary']+=1
                if v['@SUMMARY']=='runtime_synthesis':assert v['span']==summary_span;counts['runtime_summary']+=1
        else:
            for x in v.values():scan(x)
for line in text.splitlines():
    try:obj=json.loads(line)
    except json.JSONDecodeError:continue
    scan(obj)
assert counts=={'literal':22,'summary':59,'runtime_summary':3}
reversed_text=text
for row in receipt['reference_lines']:
    assert reversed_text.count(row['after'])==1
    reversed_text=reversed_text.replace(row['after'],row['before'],1)
assert reversed_text.count(replacement)==1
reversed_text=reversed_text.replace(replacement,original.decode(),1)
assert reversed_text.encode()==parent_raw

# V5 integration audit: approve operation, not our own authored semantics.
v5=document(parent.with_suffix('.json'));assert v5['topic_compaction_v5'] and sha(parent_raw)==v5['sha256']
v4path=Path(v5['parent_path']);v4raw=read(v4path);assert sha(v4raw)==v5['parent_sha256']
review_raw=read(v5['review_path']);review=json.loads(review_raw)
assert sha(review_raw)==v5['review_sha256'] and review['status']=='APROVADA_FIDELIDADE_DOCUMENTAL'
assert v5['changes']==review['reviewed_topics'] and len(v5['changes'])==23
topics=set();back=parent_raw;capsule_pins=[]
for row in v5['changes']:
    assert row['topic'] not in topics;topics.add(row['topic'])
    old=read(row['original_path']);new=read(row['capsule_path'])
    assert sha(old)==row['original_sha256'] and sha(new)==row['capsule_sha256']
    assert row['status']=='APROVADA_FIDELIDADE_DOCUMENTAL'
    assert back.count(new)==1 and v4raw.count(old)==1
    back=back.replace(new,old,1)
    capsule_pins.append({'topic':row['topic'],'sha256':sha(new)})
assert back==v4raw
delivery=document(WORK/'topic_capsules_v5/DELIVERY_ALL_30.json')
excluded=[r['topic'] for r in delivery['non_reducing_topics']]
assert len(excluded)==7 and not (topics & set(excluded))
for name in excluded:
    old=read(WORK/'topic_capsules_v5'/(name+'.original.md'))
    assert parent_raw.count(old)==1 and v4raw.count(old)==1
assert any(r['topic']=='alpha_inversion' and Path(r['capsule_path']).name=='alpha_inversion_v2.md' for r in v5['changes'])
for p,b in READ.items():assert p.read_bytes()==b,f'Concurrent drift: {p}'
now=datetime.now(timezone.utc)
report={'status':'APROVADA_INTEGRACAO_DOCUMENTAL_V5_RUNTIME_NO_ESCOPO_AUDITADO','created_utc':now.isoformat(),'independence':'Nao importado nem executado builder/verificador do pai. Revisor escreveu V5: esta aprovacao e somente da operacao de integracao; semantica V5 aprovada exclusivamente pelo pai no parecer pinado.','target':{'path':str(TARGET),'sha256':sha(raw)},'parents':{'v5':{'path':str(parent),'sha256':sha(parent_raw)},'v4':{'path':str(v4path),'sha256':sha(v4raw)}},'checks':{'runtime_reversed_byte_exact_to_v5':True,'v5_reversed_byte_exact_to_v4':True,'v5_capsules_exact_approved':23,'v5_excluded_originals_intact':excluded,'alpha_inversion_v2_used':True,'runtime_capsule_v2_exact_with_declared_wrapper':True,'runtime_reference_lines_checked':len(receipt['reference_lines']),'changed_reference_objects_checked':changed_anchors,'old_literal_content_preserved_outside_runtime':True,'runtime_converted_refs':converted,'all_internal_reference_counts':counts,'outside_declared_changes_all_bytes_preserved':True},'v5_approval':{'path':v5['review_path'],'sha256':sha(review_raw)},'runtime_approval':{'path':receipt['review_path'],'sha256':sha(runtime_review_raw)},'capsules':capsule_pins,'limits':['Nao reaprova semantica das capsulas de autoria deste revisor; toma a aprovacao independente do pai como precondicao documental pinada.','Auditoria encerra no parent V4 byte-exato,nao repete toda cadeia anterior ate fontes primarias/kernel.','Verifica spans/fragmentos internos e caminhos das tres conversoes runtime; nao executa recuperacao externa por JSONpointer.','Nao inclui compactacao metadata,novo builder/decoder/derivado,implantacao,Lean,prova fisica ou contagem Anthropic.','Numeros de capacidade anteriores informados pelo operador nao sao atribuidos a este novo hash.']}
dest=WORK/'adversarial_memory_review'/('v5_runtime_integration_'+now.strftime('%Y%m%d_%H%M%S_%f')+'.json')
temp=dest.with_suffix('.json.tmp');data=json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8')
with temp.open('xb') as f:f.write(data)
assert temp.read_bytes()==data and not dest.exists();temp.rename(dest)
print(json.dumps({'path':str(dest),'status':report['status'],'target':report['target'],'checks':report['checks']},ensure_ascii=False,indent=2))
