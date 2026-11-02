"""Reviewer: the top-level compact capsules of the SHARED prefix (and sonnet_public): restore == source, status-like fields all inside the capsule (visible), zero omissions."""
import json,re,sys,io,contextlib,importlib.util
from pathlib import Path
W=Path(sys.argv[1]);sys.argv=['x',str(W)]
spec=importlib.util.spec_from_file_location('r3',str(Path(__file__).parent/'r3_topics_capsules.py'))
with contextlib.redirect_stdout(io.StringIO()):
    r3=importlib.util.module_from_spec(spec);spec.loader.exec_module(r3)
core,res=r3.core,r3.res
KEEP=re.compile(r'status|statute|estatuto|verdict|veredit|scope|escopo|hypothes|hip[oó]tese|assumption|premiss|claim|declar|residue|conjecture|not_claimed|not_said|statement|enunciad|diz\b|nao_diz|not_say',re.I)
def leaves(v,p=''):
    if isinstance(v,dict):
        for k,x in v.items():yield from leaves(x,r3.child(p,k))
    elif isinstance(v,list):
        for i,x in enumerate(v):yield from leaves(x,r3.child(p,i))
    else:yield p,v
def status_leaves(v,p='',inside=False):
    if isinstance(v,dict):
        for k,x in v.items():
            yield from status_leaves(x,r3.child(p,k),inside or bool(KEEP.search(str(k))))
    elif isinstance(v,list):
        for i,x in enumerate(v):yield from status_leaves(x,r3.child(p,i),inside)
    elif inside:yield p,v
TAG=re.compile(r'\[(REAL|DERIVED|POSTULATE|POSTO|CONJECTURE|ONTO|KNOWN|OPEN|INPUT|LEGAL|DECLARADO|DECLARED|INCONDICIONAL|CONDICIONAL|PROVED|PROVADO|PRINCIPLED)[^\]]*\]')
out={}
for pkg in ('shared','sonnet_public'):
    t=(W/'app/packages'/pkg/'prefix.md').read_text('utf-8');head=t.partition(r3.MARK)[0];head=r3.unalias(head)
    m=re.search(r'(?:DICIONÁRIO DE LITERAIS|LITERAIS_COMPARTILHADOS)\n(\{.*\})\n',head);D=json.loads(m.group(1))
    FL=json.loads(re.search(r'DICIONÁRIO DE INDICADORES LITERAIS\n(\{.*\})\n',head).group(1))
    E=t.partition(r3.MARK)[2].split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
    hs=list(re.finditer(r'(?m)^### ([^\n]+)\n',head));body={h[1]:head[h.end():(hs[i+1].start() if i+1<len(hs) else len(head))] for i,h in enumerate(hs)}
    caps=0;exact=0;bad=[];st_total=0;st_missing=[];tag_total=0;tag_missing=0;summ=0;only_ptr_tag=[]
    for n in core:
        if n not in body:continue
        lines=[l for l in body[n].split('\n') if l.strip() and not l.startswith('Fonte:')]
        if not lines or not lines[0].startswith('{"@"'):continue
        v=json.loads(lines[0]);caps+=1
        if '@B' in v:v.update(FL[str(v.pop('@B'))])
        dv=r3.dec_lit(r3.unpack(v),D,E);rep=[]
        try:
            got=r3.restore(dv,res,'/core/'+n,rep,E)
            if got==core[n]:exact+=1
            else:bad.append((n,'DIFF'))
        except Exception as e:bad.append((n,str(e)[:100]));continue
        vis={p for p,_ in rep}
        # status-like leaves of the source and whether each is carried inside the capsule fields
        for p,val in status_leaves(core[n],'/core/'+n):
            st_total+=1
            if not any(p==q or p.startswith(q+'/') or q.startswith(p+'/') for q in vis):st_missing.append((n,p))
        # statute tags anywhere in the source topic: count tag-bearing leaves not carried (info)
        for p,val in leaves(core[n],'/core/'+n):
            if isinstance(val,str) and TAG.search(val):
                tag_total+=1
                if not any(p==q or p.startswith(q+'/') or q.startswith(p+'/') for q in vis):tag_missing+=1
    out[pkg]={'top_level_capsules':caps,'restore_exactly':exact,'bad':bad[:10],'status_like_leaves_in_source':st_total,'status_like_leaves_not_in_capsule':len(st_missing),'examples_not_in_capsule':st_missing[:8],'statute_tag_bearing_leaves':tag_total,'tag_leaves_only_by_pointer':tag_missing}
print(json.dumps(out,ensure_ascii=False,indent=1))
