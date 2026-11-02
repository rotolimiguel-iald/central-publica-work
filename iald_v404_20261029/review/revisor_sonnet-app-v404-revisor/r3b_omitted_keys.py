"""Reviewer: for shared/sonnet packages, list ALL keys that decoded blocks omit versus the sealed core (not only the first), and classify them."""
import json,re,sys,importlib.util,collections
from pathlib import Path
W=Path(sys.argv[1]);OUT=sys.argv[2] if len(sys.argv)>2 else None
sys.argv=[sys.argv[0],str(W)]
spec=importlib.util.spec_from_file_location('r3',str(Path(__file__).parent/'r3_topics_capsules.py'))
# reuse decoding helpers by exec-ing the module with output suppressed
import io,contextlib
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    r3=importlib.util.module_from_spec(spec);spec.loader.exec_module(r3)
core=r3.core;res=r3.res
def alldiff(a,b,p,acc):
    if type(a)!=type(b):acc.append((p,'type'));return
    if isinstance(a,dict):
        for k in set(a)|set(b):
            if k not in a:acc.append((p+'/'+k,'omitted'))
            elif k not in b:acc.append((p+'/'+k,'extra'))
            else:alldiff(a[k],b[k],p+'/'+k,acc)
    elif isinstance(a,list):
        if len(a)!=len(b):acc.append((p,'len'));return
        for i,(x,y) in enumerate(zip(a,b)):alldiff(x,y,p+'/'+str(i),acc)
    elif a!=b:acc.append((p,'value'))
def decode_topic(name,pkg):
    t=(W/'app/packages'/pkg/'prefix.md').read_text('utf-8')
    head,_,expo=t.partition(r3.MARK);head=r3.unalias(head)
    m=re.search(r'(?:DICIONÁRIO DE LITERAIS|LITERAIS_COMPARTILHADOS)\n(\{.*\})\n',head);D=json.loads(m.group(1)) if m else {}
    m2=re.search(r'DICIONÁRIO DE INDICADORES LITERAIS\n(\{.*\})\n',head);FL=json.loads(m2.group(1)) if m2 else {}
    E=expo.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
    hs=list(re.finditer(r'(?m)^### ([^\n]+)\n',head));body={}
    for i,h in enumerate(hs):
        body[h[1]]=head[h.end():(hs[i+1].start() if i+1<len(hs) else len(head))]
    line=[l for l in body[name].split('\n') if l.strip() and not l.startswith('Fonte:')][0]
    v=json.loads(line)
    if isinstance(v,dict) and '@B' in v:
        fl=FL[str(v.pop('@B'))];v.update(fl)
    dv=r3.dec_lit(r3.unpack(v),D,E);rep=[]
    return r3.restore(dv,res,'/core/'+name,rep,E)
rows=[];kinds=collections.Counter()
for pkg in ('shared','sonnet_public'):
    for name in core:
        try:
            got=decode_topic(name,pkg)
        except (IndexError,json.JSONDecodeError):
            rows.append({'pkg':pkg,'topic':name,'form':'TEXT_SYNTHESIS_OR_UNPARSED'});continue
        acc=[];alldiff(got,core[name],'',acc)
        if acc:rows.append({'pkg':pkg,'topic':name,'diffs':acc[:20],'n':len(acc)})
omitted=collections.Counter()
for r in rows:
    for p,k in r.get('diffs',[]):omitted[(p.rsplit('/',1)[-1],k)]+=1
status_like=re.compile(r'status|statute|estatuto|verdict|veredit|scope|escopo|hypothes|hip[oó]tese|assumption|premiss|claim|declar|residue|conjecture|not_claimed|not_said|statement|enunciad|formula|equa',re.I)
flag=[(k,n) for (k,kind),n in omitted.items() if status_like.search(k)]
out={'topics_with_omitted_keys':sorted({r['topic'] for r in rows if 'diffs' in r}),'text_syntheses':sorted({r['topic'] for r in rows if r.get('form')}),
     'omitted_key_names':{f'{k}:{kind}':n for (k,kind),n in omitted.most_common()},'status_like_omitted':flag}
print(json.dumps(out,ensure_ascii=False,indent=1))
