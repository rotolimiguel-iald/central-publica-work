"""Reviewer r2: v402 'check 18' re-implemented independently (the ORIGINAL review_app.py has NO literal-protection check; check 18 lived only in the v402 reviewer's own, unpreserved script).
For the 19 window topics (11 new in v404 + the 8 former _v401/_v402) in shared and sonnet_public:
 (a) block decodes and restores EXACTLY to the sealed topic;
 (b) every source top-level key that is a qualifier (status|statute|estatuto|verdict|veredit|scope|escopo|limites|diz|nao_diz) is INLINE (not a pointer reference) and equal to the source;
 (c) every status-like leaf (last path component status|statute|estatuto|verdict|veredit) outside the structured registers `unconditional`, `index_conditional`, `named_pending`
     (which v402 also left as pointers) is literal; the leaves under those registers are listed;
 (d) the block is NOT a top-level compact capsule (v402: new topics enter uncompressed);
 (e) the same 19 blocks, decoded, are IDENTICAL to the accepted v402 shared blocks for the 8 former topics."""
import json,re,sys,io,contextlib,importlib.util
from pathlib import Path
W=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');V2=Path(r'C:\IALD\Central de Patentes\work\iald_v402_20261027')
def load(wd):
    argv=sys.argv;sys.argv=['x',str(wd)]
    spec=importlib.util.spec_from_file_location('r3x',str(Path(__file__).parent/'r3_topics_capsules.py'))
    with contextlib.redirect_stdout(io.StringIO()):
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    sys.argv=argv;return m
m=load(W);m2=load(V2)
def block(mm,pkg,n):
    t=(mm.W/'app/packages'/pkg/'prefix.md').read_text('utf-8');head=mm.unalias(t.partition(mm.MARK)[0])
    Dm=re.search(r'(?:DICIONÁRIO DE LITERAIS|LITERAIS_COMPARTILHADOS)\n(\{.*\})\n',head);D=json.loads(Dm.group(1)) if Dm else {}
    F=re.search(r'DICIONÁRIO DE INDICADORES LITERAIS\n(\{.*\})\n',head);FL=json.loads(F.group(1)) if F else {}
    E=t.partition(mm.MARK)[2].split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
    hs=list(re.finditer(r'(?m)^### ([^\n]+)\n',head))
    for i,h in enumerate(hs):
        if h[1]==n:
            seg=head[h.end():(hs[i+1].start() if i+1<len(hs) else len(head))]
            line=[l for l in seg.split('\n') if l.strip() and not l.startswith('Fonte:')][0]
            v=json.loads(line)
            if isinstance(v,dict) and '@B' in v:v.update(FL[str(v.pop('@B'))])
            return mm.dec_lit(mm.unpack(v),D,E),E
    raise KeyError(n)
QK=re.compile(r'status|statute|estatuto|verdict|veredit|scope|escopo|limites|^diz$|^nao_diz$',re.I)
SL=re.compile(r'^(?:status|statute|estatuto|verdict|veredit\w*)$',re.I)
EXEMPT={'unconditional','index_conditional','named_pending'}
def is_ref(x):return isinstance(x,dict) and '@' in x
def inline_top(dv):
    """top-level keys carried as literal: plain (non-reference) values, or keys listed in a top-level capsule's fields"""
    if is_ref(dv):return {k.split('/')[1] for k in dv.get('fields',{}) if k.count('/')>=1}
    return {k for k,x in dv.items() if not is_ref(x)}
def status_leaves(v,p=''):
    if isinstance(v,dict):
        for k,x in v.items():yield from status_leaves(x,p+'/'+k)
    elif isinstance(v,list):
        for i,x in enumerate(v):yield from status_leaves(x,p+'/'+str(i))
    else:
        if SL.match(p.rsplit('/',1)[-1]):yield p
def lit_paths(dv,p=''):
    out=set()
    if is_ref(dv):
        for k in dv.get('fields',{}):out.add(p+k)
        return out
    if isinstance(dv,dict):
        for k,x in dv.items():out|=lit_paths(x,p+'/'+k) if not is_ref(x) else {p+'/'+k+kk for kk in x.get('fields',{})}
    elif isinstance(dv,list):
        for i,x in enumerate(dv):out|=lit_paths(x,p+'/'+str(i))
    else:out.add(p)
    return out
new11=[n for n in m.core if n not in m2.core];former=[n for n in m.core if re.search(r'_v40[12]$',n) and n in m2.core]
topics=new11+former
rows={};allok=True
for pkg in('shared','sonnet_public'):
    for n in topics:
        dv,E=block(m,pkg,n);rep=[]
        try:got=m.restore(dv,m.res,'/core/'+n,rep,E);exact=(got==m.core[n])
        except Exception as e:exact=False
        src=m.core[n];toplevel_cap=is_ref(dv) and dv.get('@')==''
        inl=inline_top(dv)
        missing=[k for k in src if QK.search(k) and k not in inl]
        # literal status leaves
        lp=lit_paths(dv)
        stat_missing=[];stat_exempt=[]
        for p in status_leaves(src):
            top=p.split('/')[1]
            if p in lp or any(q==p or q.startswith(p+'/') or p.startswith(q+'/') for q in lp):continue
            (stat_exempt if top in EXEMPT else stat_missing).append(p)
        ok=exact and not toplevel_cap and not missing and not stat_missing
        allok&=ok
        rows[(pkg,n)]={'exact':exact,'top_level_capsule':toplevel_cap,'qualifier_keys_missing_inline':missing,'status_leaves_pointer_only_outside_registers':stat_missing,'status_leaves_under_exempt_registers_pointer_only':len(stat_exempt),'ok':ok}
# (e) identical to v402 accepted for the former topics
ident={}
for n in former:
    d4,_=block(m,'shared',n);d2,_=block(m2,'shared',n)
    ident[n]=json.dumps(d4,sort_keys=True,default=lambda o:'S'+getattr(o,'ptr','')+str(getattr(o,'a',''))+str(getattr(o,'n','')))==json.dumps(d2,sort_keys=True,default=lambda o:'S'+getattr(o,'ptr','')+str(getattr(o,'a',''))+str(getattr(o,'n','')))
print(json.dumps({'topics_checked':len(topics),'new_in_v404':len(new11),'former_v401_v402':len(former),'all_ok':allok,
  'failing':[f'{p}:{n}' for (p,n),r in rows.items() if not r['ok']],
  'exempt_register_status_leaves_total_shared':sum(r['status_leaves_under_exempt_registers_pointer_only'] for (p,n),r in rows.items() if p=='shared'),
  'former_blocks_identical_to_accepted_v402_shared':ident,
  'top_level_capsules_among_19':[f'{p}:{n}' for (p,n),r in rows.items() if r['top_level_capsule']],
  'per_topic':{f'{p}:{n}':r for (p,n),r in rows.items() if p=='shared'}},ensure_ascii=False,indent=1))
