"""Reviewer (sonnet-app-v404-revisor) check 3a/3b: topics present in each package, 0 lost, capsules restore exactly,
statute-bearing fields preserved. OWN decoder (does not import haiku_codec / fit_*). Read-only. usage: script <release_dir> -> JSON on stdout."""
import json,re,sys,hashlib
from pathlib import Path
W=Path(sys.argv[1]) if len(sys.argv)>1 else Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029')
rel=W.name.split('_')[1]  # v404
VAULT=Path(r'C:\IALD\Central de Patentes\vault\originals_copy')/('um_unificado_'+rel)
sha=lambda b:hashlib.sha256(b).hexdigest()
res_raw=(VAULT/'um_absoluto.json').read_bytes()
seal=json.loads((VAULT/'um_absoluto_selo.json').read_bytes())
assert sha(res_raw)==seal['sha256']['um_absoluto.json'],'core not the sealed one'
res=json.loads(res_raw);core=res['core']
MARK='## Exposição canônica integral: fórmulas e derivações'
ALIAS={'"@F"':'"@SOURCE_FIELDS"','"@I"':'"@SOURCE_ITEMS"','"@L"':'"@TGL_LITERAL"','"@Y"':'"@SUMMARY"','"@X"':'"@EXPOSITION"'}
def unalias(s):
    for sh_,lg in ALIAS.items():s=s.replace(sh_,lg)
    return s
def resolve(v,ptr):
    if ptr=='':return v
    assert ptr.startswith('/'),ptr
    for part in ptr.split('/')[1:]:
        k=part.replace('~1','/').replace('~0','~')
        v=v[int(k)] if isinstance(v,list) else v[k]
    return v
def child(p,k):return p+'/'+str(k).replace('~','~0').replace('/','~1')
def unpack(v):
    if isinstance(v,list):return [unpack(x) for x in v]
    if not isinstance(v,dict):return v
    out={k:unpack(x) for k,x in v.items() if k not in('@SOURCE_FIELDS','@SOURCE_ITEMS')}
    if '@SOURCE_FIELDS' in v:
        for k in v['@SOURCE_FIELDS']:out[k]={'@':'/'+k}
    if '@SOURCE_ITEMS' in v:
        for k,n in v['@SOURCE_ITEMS'].items():out[k]={'@':'/'+k,'items':n}
    return out
class Summ:
    def __init__(self,ptr,a,n,topic=None):self.ptr=ptr;self.a=a;self.n=n;self.topic=topic
SUMM_COUNT=[0]
def dec_lit(v,D,E):
    if isinstance(v,list):return [dec_lit(x,D,E) for x in v]
    if not isinstance(v,dict):return v
    ks=set(v)
    if ks=={'@concat'}:return ''.join(dec_lit(x,D,E) for x in v['@concat'])
    if ks=={'@upper'}:return v['@upper'].upper()
    if ks=={'@enum'}:return v['@enum'].upper().replace(' ','_')
    if ks=={'@TGL_LITERAL'}:return dec_lit(D[v['@TGL_LITERAL']],D,E)
    if ks=={'@EXPOSITION'}:s,l=v['@EXPOSITION'];return E[s:s+l]
    if ks=={'@SUMMARY'} and isinstance(v['@SUMMARY'],list):return Summ(v['@SUMMARY'][0],v['@SUMMARY'][1],v['@SUMMARY'][2])
    if ks=={'@SUMMARY','source_pointer','span'}:return Summ(v['source_pointer'],v['span'][0],v['span'][1],v['@SUMMARY'])
    return {k:dec_lit(x,D,E) for k,x in v.items()}
def restore(v,src,cur,rep,E=''):
    if isinstance(v,Summ):
        topic=cur.split('/')[2];root='/core/'+topic
        ptr=v.ptr if v.ptr.startswith('/core/') else root+v.ptr
        piece=E[v.a:v.a+v.n]
        assert piece.startswith('**Estatutos ['+topic+']**'),('stale summary',cur)
        SUMM_COUNT[0]+=1
        return resolve(src,ptr)
    if isinstance(v,dict) and '@' in v:
        assert set(v)<={'@','fields','items','true_fields','false_fields'},('unknown meta',sorted(v))
        actual=resolve(src,cur)  # the '@' path must equal the place it sits at
        assert v['@']==cur[len(cur)-len(v['@']):] if v['@'] else True
        for suf,val in v.get('fields',{}).items():
            fv=restore(val,src,cur+suf,rep,E);assert resolve(actual,suf)==fv,('field differs',cur,suf);rep.append((cur+suf,fv))
        if 'items' in v:assert len(actual)==v['items'],('items',cur)
        if 'true_fields' in v:
            assert v['true_fields']==sum(actual.values()) and v['false_fields']==len(actual)-sum(actual.values())
        return actual
    if isinstance(v,dict):return {k:restore(x,src,child(cur,k),rep,E) for k,x in v.items()}
    if isinstance(v,list):return [restore(x,src,child(cur,i),rep,E) for i,x in enumerate(v)]
    return v
STATUS=re.compile(r'status|statute|estatuto|verdict|veredit|scope|escopo|hypothes|hip[oó]tese|assumption|premiss|claim|declar|residue|conjecture|not_claimed|not_said|statement|enunciad|formula|equa',re.I)
def status_paths(v,p=''):
    out={}
    if isinstance(v,dict):
        for k,x in v.items():
            q=child(p,k)
            if STATUS.search(str(k)) :out[q]=x
            else:out.update(status_paths(x,q))
    elif isinstance(v,list):
        for i,x in enumerate(v):out.update(status_paths(x,child(p,i)))
    return out
def firstdiff(a,b,p=''):
    if type(a)!=type(b):return p+' type '+type(a).__name__+' vs '+type(b).__name__+' :: '+repr(a)[:80]+' vs '+repr(b)[:80]
    if isinstance(a,dict):
        for k in set(a)|set(b):
            if k not in a:return p+'/'+k+' missing-in-got'
            if k not in b:return p+'/'+k+' extra-in-got'
            r=firstdiff(a[k],b[k],p+'/'+k)
            if r:return r
        return ''
    if isinstance(a,list):
        if len(a)!=len(b):return p+' len %d vs %d'%(len(a),len(b))
        for i,(x,y) in enumerate(zip(a,b)):
            r=firstdiff(x,y,p+'/'+str(i))
            if r:return r
        return ''
    return '' if a==b else p+' :: '+repr(a)[:80]+' vs '+repr(b)[:80]
def analyse(name):
    SUMM_COUNT[0]=0
    t=(W/'app/packages'/name/'prefix.md').read_text('utf-8')
    head,sep,expo_part=t.partition(MARK)
    head=unalias(head)
    D={};E=''
    m=re.search(r'(?:DICIONÁRIO DE LITERAIS|LITERAIS_COMPARTILHADOS)\n(\{.*\})\n',head)
    if m:D=json.loads(m.group(1))
    m2=re.search(r'DICIONÁRIO DE INDICADORES LITERAIS\n(\{.*\})\n',head)
    FL=json.loads(m2.group(1)) if m2 else {}
    if '<EXPOSICAO_CANONICA>\n' in expo_part:E=expo_part.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
    hs=list(re.finditer(r'(?m)^### ([^\n]+)\n',head))
    body={}
    for i,h in enumerate(hs):
        stop=hs[i+1].start() if i+1<len(hs) else len(head)
        body[h[1]]=head[h.end():stop]
    present=[n for n in core if n in body];lost=[n for n in core if n not in body]
    nonjson=[];mism=[];compact=0;full=0;partial=0;stat_cmp=0;stat_vis_missing=0;stat_total=0;unknown=[]
    for n in present:
        lines=[l for l in body[n].split('\n') if l.strip()]
        js=[l for l in lines if not l.startswith('Fonte:')]
        if not js:nonjson.append(n);continue
        try:v=json.loads(js[0])
        except Exception as e:nonjson.append((n,str(e)[:60]));continue
        top_at=isinstance(v,dict) and '@' in v
        if isinstance(v,dict) and '@B' in v:
            ident=str(v.pop('@B'));flags=FL[ident];assert not(set(flags)&set(v));v.update(flags)
        try:
            dv=dec_lit(unpack(v),D,E);rep=[]
            got=restore(dv,res,'/core/'+n,rep,E)
            ok=got==core[n]
            # inline ambiguity: restored equals source exactly; also check the pointer-only restore is not trivially the source itself
            if not ok:mism.append((n,'DIFF '+firstdiff(got,core[n])))
            has_ref='"@"' in js[0]
            if top_at:compact+=1
            elif has_ref:partial+=1
            else:full+=1
            # visible statute fields: how many source status-like leaves appear directly in what the model receives (fields or inline)
            sp=status_paths(core[n]);stat_total+=len(sp)
            vis=set(p for p,_ in rep)
            # inline (non-capsule) values are visible too: collect all leaf paths in dv that are not references
            def inline(x,p,acc):
                if isinstance(x,dict) and '@' in x:return
                if isinstance(x,dict):
                    for k,y in x.items():inline(y,child(p,k),acc)
                elif isinstance(x,list):
                    for i,y in enumerate(x):inline(y,child(p,i),acc)
                else:acc.add(p)
            acc=set();inline(dv,'/core/'+n,acc);vis|=acc
            for p,val in sp.items():
                full_p='/core/'+n+p
                # visible if the path or any descendant leaf or ancestor-held field is visible
                if any(q==full_p or q.startswith(full_p+'/') or full_p.startswith(q+'/') for q in vis):stat_cmp+=1
                else:stat_vis_missing+=1
        except Exception as e:
            mism.append((n,type(e).__name__+': '+str(e)[:120]))
    return {'package':name,'bytes':len(t.encode()),'headings':len(hs),'core_topics':len(core),'present':len(present),'lost':lost,
            'topics_restoring_exactly':len(present)-len(mism)-len(nonjson),'mismatch_or_error':mism[:60],'n_mismatch':len(mism),'nonjson':nonjson[:5],
            'form':{'top_level_capsule':compact,'partial_refs':partial,'full_inline':full},
            'status_like_source_paths':stat_total,'status_paths_visible_in_prompt':stat_cmp,'status_paths_only_by_pointer':stat_vis_missing,
            'summary_refs_resolved':SUMM_COUNT[0],'prefix_sha256':sha(t.encode())}
out={'release':rel,'sealed_core_sha256':sha(res_raw),'core_topics':len(core),'packages':{}}
for p in ('shared','haiku_expanded','haiku55','sonnet_public'):
    out['packages'][p]=analyse(p)
print(json.dumps(out,ensure_ascii=False,indent=1))
