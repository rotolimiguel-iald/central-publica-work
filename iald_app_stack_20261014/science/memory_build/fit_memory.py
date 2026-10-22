"""Explicit historical-detail projection for the 200k model; sources stay intact.

Only unchanged historical topics are eligible. Current amendments, the complete
mother/core, typed hypotheses/formulas and epistemic qualifications stay resident.
The receipt lists each detail moved to exact source retrieval. No substring cut.
"""
import json, re, hashlib
import haiku_codec as c
import fit_transport as transport

KEEP = re.compile(r'status|statute|estatuto|declared|declaration|residue|claim|statement|enunciad|scope|escopo|hypothes|hip[oó]tes|assumption|premiss|not_claimed|not_said|verdict|veredit|formula|equation|equacao|equaç', re.I)
PRIORITY = re.compile(r'hamilton|lagrang|lindblad|dephas|commut|half_nat|cocycle_to_einstein|interface_is_light|right_angle|smatrix|selector|iald_executive|family_minimum|beta|light_eigenvector|contour_theory',re.I)

def fields(node, pointer=''):
    result={}
    if isinstance(node,dict):
        for key,value in node.items():
            p=c.child(pointer,key)
            if KEEP.search(key) or (key=='status' and not isinstance(value,(dict,list))):result[p]=value
            else:result.update(fields(value,p))
    elif isinstance(node,list):
        for i,value in enumerate(node):result.update(fields(value,c.child(pointer,i)))
    return result


def encode_enums(text, source):
    """Lossless token-friendly spelling of historical UPPER_SNAKE labels."""
    count=[0]
    def encode(value):
        if isinstance(value,str) and len(value)>=30 and re.fullmatch('[A-Z0-9_]+',value) and '_' in value:
            count[0]+=1;return {'@enum':value.lower().replace('_',' ')}
        if isinstance(value,str) and len(value)>=30 and value.upper()==value and value.lower()!=value and value.lower().upper()==value:
            count[0]+=1;return {'@upper':value.lower()}
        if isinstance(value,dict):return {key:encode(item) for key,item in value.items()}
        if isinstance(value,list):return [encode(item) for item in value]
        return value
    def decode(value):
        if isinstance(value,dict):
            if set(value)=={'@enum'}:return value['@enum'].upper().replace(' ','_')
            if set(value)=={'@upper'}:return value['@upper'].upper()
            return {key:decode(item) for key,item in value.items()}
        if isinstance(value,list):return [decode(item) for item in value]
        return value
    active=False;dictionary_next=False;rows=[]
    for line in text.splitlines(keepends=True):
        if line.startswith('### '):active=line.strip()[4:] in source['core']
        if line.startswith(c.MARKER):active=False
        is_dictionary=dictionary_next
        dictionary_next=line.strip()=='DICIONÁRIO DE LITERAIS'
        if active or is_dictionary:
            try:
                value=json.loads(line);encoded=encode(value);assert decode(encoded)==value
                rows.append(c.dump(encoded)+'\n');continue
            except ValueError:pass
        rows.append(line)
    notice='RÓTULOS REVERSÍVEIS: {"@enum":"palavras"} significa converter letras para MAIÚSCULAS e cada espaço para sublinhado; espaços duplos preservam __. {"@upper":"texto"} converte somente letras para MAIÚSCULAS, preservando pontuação. Vale também no dicionário de literais. @concat concatena suas partes e referências, sem separador. Não muda o estatuto nem o valor original.\n'
    return notice+''.join(rows),count[0]


def intern_across_topics(text, source):
    """Deduplicate literal strings across historical/current JSON without data loss."""
    from collections import Counter
    dm='DICIONÁRIO DE LITERAIS\n'
    raw_dictionary=text.split(dm,1)[1].split('\n',1)[0]
    dictionary=json.loads(raw_dictionary)
    exposition=text.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
    rows=text.splitlines(keepends=True); active=False; nodes={}; counts=Counter()
    def scan(v):
        if isinstance(v,str) and len(v)>=35:counts[v]+=1
        elif isinstance(v,dict):
            for k,item in v.items():
                if not k.startswith('@') and k not in ('span','source_pointer','starts_with'):scan(item)
        elif isinstance(v,list):
            for item in v:scan(item)
    for i,line in enumerate(rows):
        if line.startswith('### '):active=line.strip()[4:] in source['core']
        if line.startswith(c.MARKER):active=False
        if active:
            try:nodes[i]=json.loads(line);scan(nodes[i])
            except ValueError:pass
    lookup={}; records=[]
    for value,count in sorted(counts.items()):
        ident='D'+str(len(lookup)); node={'@TGL_LITERAL':ident}
        if (count-1)*len(c.dump(value))-count*len(c.dump(node))-len(ident)-4<=45:continue
        assert ident not in dictionary
        lookup[value]=node;dictionary[ident]=value
        records.append({'literal':ident,'occurrences':count,'sha256':c.sha(value.encode())})
    def encode(v):
        if isinstance(v,str):return lookup.get(v,v)
        if isinstance(v,list):return [encode(x) for x in v]
        if isinstance(v,dict):return {k:(x if k.startswith('@') or k in ('span','source_pointer','starts_with') else encode(x)) for k,x in v.items()}
        return v
    for i,node in nodes.items():
        encoded=encode(node)
        assert c.decode_literals(encoded,dictionary,exposition)==c.decode_literals(node,dictionary,exposition)
        rows[i]=c.dump(encoded)+'\n'
    result=''.join(rows).replace(dm+raw_dictionary,dm+c.dump(dictionary),1)
    return result,records


def compact_coordinates(text, source):
    """Remove redundant coordinate prose; exact summary pointers still recoverable."""
    exposition=text.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
    records=[]; topic=''
    def visit(v):
        if isinstance(v,dict):
            if set(v)=={'@EXPOSITION','starts_with','span'}:
                a,n=v['span'];assert v['@EXPOSITION']=='literal na exposição carregada'
                assert exposition[a:a+n].startswith(v['starts_with'])
                records.append({'kind':'literal','span':[a,n],'sha256':c.sha(exposition[a:a+n].encode())})
                return {'@EXPOSITION':[a,n]}
            if set(v)=={'@SUMMARY','source_pointer','span'}:
                label=v['@SUMMARY'];assert label==topic;root='/core/'+label
                assert v['source_pointer'].startswith(root+'/')
                a,n=v['span'];out={'@SUMMARY':[v['source_pointer'][len(root):],a,n]}
                restored={'@SUMMARY':topic,'source_pointer':'/core/'+topic+out['@SUMMARY'][0],'span':out['@SUMMARY'][1:]}
                assert restored==v
                records.append({'kind':'summary','source_pointer':v['source_pointer'],'span':[a,n],'sha256':c.sha(exposition[a:a+n].encode())})
                return out
            return {k:visit(x) for k,x in v.items()}
        if isinstance(v,list):return [visit(x) for x in v]
        return v
    rows=[];active=False
    for line in text.splitlines(keepends=True):
        if line.startswith('### '):
            topic=line.strip()[4:];active=topic in source['core']
        if line.startswith(c.MARKER):active=False
        if active:
            try:line=c.dump(visit(json.loads(line)))+'\n'
            except ValueError:pass
        rows.append(line)
    notice='@SUMMARY:[p,a,n] = síntese do tópico ### atual; fonte /core/<tópico>+p, trecho [a,n] na exposição, não valor literal da fonte.\n'
    return notice+''.join(rows),records

def compact(text, source, unchanged):
    original=text
    # Expand only transport tag aliases, avoiding changes to arbitrary prose.
    for long,short in transport.ALIASES.items():text=text.replace(short,long)
    dm='DICIONÁRIO DE LITERAIS\n'; old_dictionary=text.split(dm,1)[1].split('\n',1)[0]
    dictionary=json.loads(old_dictionary)
    marker='<EXPOSICAO_CANONICA>\n'; end='\n</EXPOSICAO_CANONICA>'
    exposition=text.split(marker,1)[1].split(end,1)[0]
    bodies={}
    headers=list(re.finditer(r'(?m)^### ([^\n]+)\n',text.split(c.MARKER)[0]))
    headers=[h for h in headers if h[1] in source['core']]
    for i,h in enumerate(headers):
        stop=headers[i+1].start() if i+1<len(headers) else text.index(c.MARKER)
        bodies[h[1]]=text[h.end():stop].strip()
    selected=[]
    for name in unchanged:
        node=source['core'][name]
        if PRIORITY.search(name) or not isinstance(node,dict):continue
        retained=fields(node)
        for key in ('theorem','all_verified','does_not_gate_core'):
            if key in node:retained['/'+key]=node[key]
        meaningful=[key for key in retained if key not in ('/all_verified','/does_not_gate_core') and not re.search(r'status|statute|estatuto',key,re.I)]
        if not meaningful:continue
        candidate={'@':'','items':len(node),'fields':retained}
        seen={};p='/core/'+name
        assert c.restore(candidate,source,p,p,seen)==node
        for path,value in retained.items():assert c.is_represented(p+path,value,seen)
        encoded,extra=c.intern_topics({name:candidate},exposition)
        ident='H'+str(len(selected))+'_'
        def rename(v):
            if isinstance(v,dict):
                if set(v)=={'@TGL_LITERAL'}:return {'@TGL_LITERAL':ident+v['@TGL_LITERAL']}
                return {k:rename(x) for k,x in v.items()}
            if isinstance(v,list):return [rename(x) for x in v]
            return v
        body=c.dump(rename(encoded[name]))
        saving=len(bodies[name].encode())-len(body.encode())-len(c.dump(extra).encode())
        if saving<50:continue
        selected.append({'topic':name,'source_pointer':p,'retained_paths':list(retained),
            'source_sha256':c.sha(c.dump(node).encode()),'previous_body_sha256':c.sha(bodies[name].encode()),
            'saved_bytes_before_span_relocation':saving,'scope':'HISTORICAL_CONCEPT_AND_EPISTEMIC_FIELDS__DETAILS_BY_FETCH'})
        bodies[name]=body;dictionary.update({ident+k:v for k,v in extra.items()})
    # Preserve every referenced span verbatim, the foundation and current errata.
    spans=[]
    def refs(v):
        if isinstance(v,dict):
            if '@EXPOSITION'in v or '@SUMMARY'in v:
                span=v.get('span',v.get('@EXPOSITION'));assert isinstance(span,list)
                spans.append(tuple(span))
            else:
                for x in v.values():refs(x)
        elif isinstance(v,list):
            for x in v:refs(x)
    for body in bodies.values():
        for line in body.splitlines():
            try:refs(json.loads(line))
            except ValueError:pass
    first_history=exposition.index('## v8 ')
    current=exposition.index('## Correções canônicas da release ')
    intervals=[(0,first_history),(current,len(exposition))]+[(a,a+n) for a,n in spans]
    merged=[]
    for a,b in sorted(intervals):
        assert 0<=a<b<=len(exposition)
        if merged and a<=merged[-1][1]:merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
        else:merged.append((a,b))
    new_exposition='';mapping=[]
    for a,b in merged:
        if new_exposition:new_exposition+='\n\n'
        mapping.append((a,b,len(new_exposition)));new_exposition+=exposition[a:b]
    def move(v):
        if isinstance(v,dict):
            if '@EXPOSITION'in v or '@SUMMARY'in v:
                key='span' if 'span'in v else '@EXPOSITION';a,n=v[key]
                match=next((x,y,z) for x,y,z in mapping if x<=a and a+n<=y)
                x,y,z=match;out=dict(v);out[key]=[z+a-x,n]
                assert exposition[a:a+n]==new_exposition[z+a-x:z+a-x+n]
                return out
            return {k:move(x) for k,x in v.items()}
        if isinstance(v,list):return [move(x) for x in v]
        return v
    for name,body in bodies.items():
        rows=[]
        for line in body.splitlines():
            try:rows.append(c.dump(move(json.loads(line))))
            except ValueError:rows.append(line)
        bodies[name]='\n'.join(rows)
    for i in range(len(headers)-1,-1,-1):
        h=headers[i];stop=headers[i+1].start() if i+1<len(headers) else text.index(c.MARKER)
        text=text[:h.end()]+bodies[h[1]]+'\n\n'+text[stop:]
    original_dictionary=dict(dictionary)
    factored=[]
    for key,value in original_dictionary.items():
        if not isinstance(value,str):continue
        candidates=[(len(piece),other,piece) for other,piece in original_dictionary.items()
                    if other!=key and isinstance(piece,str) and 100<=len(piece)<len(value) and piece in value]
        if not candidates:continue
        _,other,piece=max(candidates)
        at=value.index(piece);parts=[value[:at],{'@TGL_LITERAL':other},value[at+len(piece):]]
        node={'@concat':[part for part in parts if part!='']}
        if len(c.dump(node))+40>=len(c.dump(value)):continue
        dictionary[key]=node;factored.append({'literal':key,'substring_literal':other,'sha256':c.sha(value.encode())})
    for key,value in original_dictionary.items():
        assert c.decode_literals({'@TGL_LITERAL':key},dictionary,exposition)==value
    text=text.replace(dm+old_dictionary,dm+c.dump(dictionary),1)
    text=text.replace(marker+exposition+end,marker+new_exposition+end,1)
    notice=('PACOTE HAIKU: os tópicos históricos sem alteração podem usar cápsulas de conceito, enunciado, hipóteses, fórmulas nomeadas, estatutos e vereditos; @:"" aponta ao tópico integral. ### nome com @ vazio resolve resultado_publicado_integral /core/nome. '
        'Detalhes das rotas históricas e demonstrações permanecem em fetch_tgl/iald_kernel_read. Consulte automaticamente quando precisar desses detalhes. '
        'A exposição histórica mantém a cadeia fundacional e todos os trechos referenciados; as correções literais atuais permanecem integrais. Nenhum arquivo-fonte foi reduzido.\n')
    text=notice+text
    text,coordinate_records=compact_coordinates(text,source)
    text,cross_literals=intern_across_topics(text,source)
    for long,short in transport.ALIASES.items():text=text.replace(long,short)
    text,enum_count=encode_enums(text,source)
    compact_legends=[]
    for line in text.splitlines(keepends=True):
        if line.startswith('RÓTULOS REVERSÍVEIS:'):
            line='CODEC: @enum=MAIÚSCULAS, espaços→_; @upper=MAIÚSCULAS sem trocar pontuação; @concat=concatenação sem separador. Também no dicionário.\n'
        elif line.startswith('PACOTE HAIKU:'):
            line='HAIKU: cápsulas históricas retêm conceito e escopo; detalhes por fetch_tgl/iald_kernel_read. ### nome + @:"" = resultado_publicado_integral /core/nome. Exposição: fundamentos, excertos referenciados e correções atuais.\n'
        elif line.startswith('v5/Core integrais;'):
            line='v5/Core integrais; enunciados Lean carregados, provas integrais por iald_kernel_read. Exposição v368 parcial/histórica; correções atuais prevalecem. Consulte detalhes automaticamente.\n'
        elif line.startswith('METADADOS REVERSÍVEIS: @B'):
            line='@B acrescenta os pares literais do dicionário de indicadores, sem sobrescrever. Rol ambíguo integral: resultado_publicado_integral /core/the_iald_index/ambiguos; n_ambiguos carregado.\n'
        compact_legends.append(line)
    text=''.join(compact_legends)
    redundant='@Y referencia a síntese documental nomeada nesse bloco, NÃO o valor literal da fonte. Seus source_pointer permanecem recuperáveis. '
    assert text.count(redundant)==1
    text=text.replace(redundant,'',1)
    text=text.replace('FONTE IMPLÍCITA de cada cabeçalho ### nome: resultado_publicado_integral /core/nome.', '### nome → resultado_publicado_integral /core/nome.',1)

    receipt={'coordinate_roundtrips':coordinate_records,'cross_topic_literals':cross_literals,'factored_dictionary_literals':factored,'enum_values_roundtripped':enum_count,'policy':'FIXED_FOUNDATION_CURRENT_AMENDMENTS_AND_ALL_TOPICS__HISTORICAL_DETAILS_RETRIEVABLE',
        'input_sha256':c.sha(original.encode()),'output_sha256':c.sha(text.encode()),
        'historical_topics_projected':selected,'historical_exposition_source_sha256':c.sha(exposition.encode()),
        'retained_historical_spans':[{'start':a,'end':b,'new_start':z,'sha256':c.sha(exposition[a:b].encode())} for a,b,z in mapping],
        'old_exposition_bytes':len(exposition.encode()),'new_exposition_bytes':len(new_exposition.encode()),
        'all_source_files_unchanged':True,'new_topics_projected':False,'mother_and_core_unchanged':True}
    return text,receipt
