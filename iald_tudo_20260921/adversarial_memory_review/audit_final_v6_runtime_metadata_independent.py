"""Read-only audit of V5/runtime integration. Does not import builders/verifiers."""
import hashlib,json,re
from pathlib import Path
from datetime import datetime,timezone
WORK=Path(__file__).resolve().parent.parent
TARGET=WORK/'haiku_reviewed_runtime_20260922_141545_579740.md'
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


# Appended to independently written runtime audit, never to a builder.
topic_checks=[]
stage_path=parent;stage_raw=parent_raw
for version,n_expected in [('v6',38),('v5',23)]:
    stage_receipt=document(stage_path.with_suffix('.json'))
    assert stage_receipt['topic_compaction_'+version] and sha(stage_raw)==stage_receipt['sha256']
    ancestor=Path(stage_receipt['parent_path']);ancestor_raw=read(ancestor)
    assert sha(ancestor_raw)==stage_receipt['parent_sha256']
    approval_raw=read(stage_receipt['review_path']);approval=json.loads(approval_raw)
    assert sha(approval_raw)==stage_receipt['review_sha256']
    assert approval['status']=='APROVADA_FIDELIDADE_DOCUMENTAL'
    assert stage_receipt['changes']==approval['reviewed_topics'] and len(stage_receipt['changes'])==n_expected
    names=set();back=stage_raw
    for row in stage_receipt['changes']:
        assert row['topic'] not in names;names.add(row['topic'])
        old=read(row['original_path']);new=read(row['capsule_path'])
        assert sha(old)==row['original_sha256'] and sha(new)==row['capsule_sha256']
        assert row['status']=='APROVADA_FIDELIDADE_DOCUMENTAL'
        assert back.count(new)==1 and ancestor_raw.count(old)==1
        back=back.replace(new,old,1)
    assert back==ancestor_raw
    required_topic,required_file=('reading_direction','reading_direction_v2.md') if version=='v6' else ('alpha_inversion','alpha_inversion_v2.md')
    assert any(r['topic']==required_topic and Path(r['capsule_path']).name==required_file for r in stage_receipt['changes'])
    if version=='v6':
        delivery=document(WORK/'topic_capsules_v6/DELIVERY_ALL_60.json')
        excluded=delivery['original_retained_byte_exact'];assert len(excluded)==22
    else:
        delivery=document(WORK/'topic_capsules_v5/DELIVERY_ALL_30.json')
        excluded=[r['topic'] for r in delivery['non_reducing_topics']];assert len(excluded)==7
    assert not names.intersection(excluded)
    for name in excluded:
        old=read(WORK/('topic_capsules_'+version)/(name+'.original.md'))
        assert stage_raw.count(old)==1 and ancestor_raw.count(old)==1
    topic_checks.append({'stage':version,'path':str(stage_path),'sha256':sha(stage_raw),'reversed_byte_exact_to':str(ancestor),'ancestor_sha256':sha(ancestor_raw),'approved_capsules_exact':n_expected,'excluded_originals_intact':len(excluded),'required_v2_used':required_file,'approval_path':stage_receipt['review_path'],'approval_sha256':sha(approval_raw)})
    stage_path,stage_raw=ancestor,ancestor_raw

# Independently decode metadata; no module imports from builders or their verifier.
METADATA=WORK/'haiku_metadata_proposal_20260922_141555_464161.md'
metadata_raw=read(METADATA);mr=document(METADATA.with_suffix('.json'))
assert Path(mr['parent'])==TARGET and mr['parent_sha256']==sha(raw) and mr['sha256']==sha(metadata_raw)
protocol='\nRemissões compactas: em cada objeto JSON, @SOURCE_FIELDS:[k,...] equivale a k:{"@":"/k"} para cada nome k; @SOURCE_ITEMS:{k:n,...} equivale a k:{"@":"/k","items":n}. As rotas mantêm o tópico Fonte correspondente. São referências ao acervo, não conteúdo integral carregado. items conta itens documentais, não provas. Campos, hipóteses e estatutos retidos permanecem explícitos.\n'
assert mr['protocol']==protocol
mt=metadata_raw.decode('utf-8');assert mt.count(protocol)==1
def anchor(t,title):
    matches=list(re.finditer(r'(?m)^'+re.escape(title)+r'\r?$',t))
    assert len(matches)==1
    return matches[0].start()-1
lo=anchor(text,'## Fundamento, Um, Meia-Nat e custo geométrico')
hi=anchor(text,'## Exposição canônica integral: fórmulas e derivações')
assert 0<lo<hi and mt.index(protocol)==lo
body=mt.replace(protocol,'',1)
new_hi=anchor(body,'## Exposição canônica integral: fórmulas e derivações')
assert body[:lo].encode()==raw[:len(text[:lo].encode())]
assert body[new_hi:].encode()==text[hi:].encode()
group_counts={'source_fields_groups':0,'source_fields_refs':0,'source_items_groups':0,'source_items_refs':0}
def independent_decode(v):
    if isinstance(v,list):return [independent_decode(x) for x in v]
    if not isinstance(v,dict):return v
    decoded={k:independent_decode(x) for k,x in v.items() if k not in ('@SOURCE_FIELDS','@SOURCE_ITEMS')}
    for key,is_items in [('@SOURCE_FIELDS',False),('@SOURCE_ITEMS',True)]:
        if key not in v:continue
        group=v[key];assert isinstance(group,dict if is_items else list) and len(group)>=2
        seen=set()
        for name in group:
            assert isinstance(name,str) and name and not name.startswith('@') and '/' not in name and '~' not in name
            assert name not in seen and name not in decoded;seen.add(name)
            decoded[name]={'@':'/'+name}
            if is_items:
                number=group[name];assert type(number)is int and number>=0
                decoded[name]['items']=number
        label='source_items' if is_items else 'source_fields'
        group_counts[label+'_groups']+=1;group_counts[label+'_refs']+=len(group)
    return decoded
def unique_pairs(pairs):
    result={}
    for key,value in pairs:
        assert key not in result,'Duplicate JSON key'
        result[key]=value
    return result
oldlines=text.splitlines(keepends=True);newlines=body.splitlines(keepends=True)
assert len(oldlines)==len(newlines)
changed=[];position=0;decoded_lines=[];restored=[]
for i,(old,new) in enumerate(zip(oldlines,newlines)):
    if old!=new:
        assert lo<=position<hi
        a=json.loads(old,object_pairs_hook=unique_pairs);b=json.loads(new,object_pairs_hook=unique_pairs)
        dec=independent_decode(b)
        assert dec==a
        changed.append(i);decoded_lines.append(dec);restored.append(old)
    else:
        restored.append(new)
        try:decoded_lines.append(independent_decode(json.loads(new,object_pairs_hook=unique_pairs)))
        except json.JSONDecodeError:pass
    position+=len(old)
assert changed==mr['changed_line_numbers_zero_based'] and len(changed)==156
assert ''.join(restored).encode('utf-8')==raw
runtime_counts=counts.copy();counts={'literal':0,'summary':0,'runtime_summary':0}
for obj in decoded_lines:scan(obj)
assert counts==runtime_counts=={'literal':22,'summary':59,'runtime_summary':3}
assert exposure(body,receipt['new_exposition_chars'])==newexp
for path,old in READ.items():assert path.read_bytes()==old,'Concurrent input change'

now=datetime.now(timezone.utc)
report={'status':'APROVADA_OPERACAO_INTEGRACAO_E_METADATA_NO_ESCOPO_DOCUMENTAL','created_utc':now.isoformat(),'task_complete':True,'independence':'Auditoria de operacao escrita pelo revisor sem importar/executar builders ou verificadores do pai. Semantica de V5/V6 de autoria deste revisor nao reaprovida: aprovacoes independentes do pai pinadas como precondicoes.','runtime_target':{'path':str(TARGET),'sha256':sha(raw)},'metadata_target':{'path':str(METADATA),'sha256':sha(metadata_raw)},'runtime_checks':{'approved_capsule_v2_exact':True,'declared_wrapper_exact':True,'only_declared_exposition_interval_changed':True,'runtime_reversed_byte_exact_to_v6':True,'remapped_lines_checked':len(receipt['reference_lines']),'changed_anchors_checked':changed_anchors,'runtime_summary_conversions':converted,'references':runtime_counts},'topic_integrations':topic_checks,'metadata_checks':{'exact_protocol_header_checked':True,'anchored_unique_region_boundaries':True,'changed_json_lines':len(changed),'groups':group_counts,'independent_decoder_roundtrip_all_changed_lines':True,'duplicate_json_keys_rejected':True,'prefix_outside_protocol_byte_exact':True,'exposition_and_suffix_byte_exact':True,'all_parent_bytes_recovered_using_original_line_serialization':True,'references_after_decode':counts},'capacity':{'source':'INFORMADA_PELO_OPERADOR_NAO_RECONTADA_NESTA_AUDITORIA','permanent_anthropic':183135,'request_anthropic':184609,'output_reserved':4096,'margin_reserved':1024,'reported_dynamic_remaining':10271,'arithmetic_checked':200000-184609-4096-1024==10271,'permanent_target_interval':[180000,183406],'reported_permanent_within_interval':180000<=183135<=183406,'api_calls':0},'limits':['Aprovacao de operacao/integridade documental somente,nao nova aprovacao semantica de capsulas proprias.','Cadeia reversivel auditada termina no draft V4 pai byte-exato; nao recompila Lean nem reaudita todas fontes anteriores.','Decoder restaura estrutura JSON; ordem/espacos originais recuperados por comparacao com linhas do pai,nao inferidos da notacao compacta.','Protocolo define duas notacoes e escopo Fonte,sem afirmar compreensao pelo modelo ou compatibilidade operacional de ferramentas de recuperacao.','Ancora interna validada por span/fragmento; sem acesso externo por JSONpointer/API/rede.','Capacidade e contagem nativa informadas pelo operador; aritmetica conferida,nao contagem independente Anthropic nem teste de implantacao.','Sem producao/implantacao,sem QG confirmada,sem novos conceitos ou capsulas.']}
dest=WORK/'adversarial_memory_review'/('FINAL_integration_metadata_'+now.strftime('%Y%m%d_%H%M%S_%f')+'.json')
temp=dest.with_suffix('.json.tmp');data=json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8')
with temp.open('xb') as f:f.write(data)
assert temp.read_bytes()==data and not dest.exists();temp.rename(dest)
print(json.dumps({'report':str(dest),'status':report['status'],'runtime':report['runtime_target'],'metadata':report['metadata_target'],'runtime_checks':report['runtime_checks'],'metadata_checks':report['metadata_checks'],'capacity_arithmetic':report['capacity']['arithmetic_checked']},ensure_ascii=False,indent=2))
