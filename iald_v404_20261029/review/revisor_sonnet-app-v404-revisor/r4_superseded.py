"""Reviewer: superseded gate-flag wording ('15 calculadas e 3 literais' / '15 computed and 3 literal') in the texts the models receive.
Scans (a) RAW prefix text, (b) DECODED topic JSON (enum/upper/concat/literal-dictionary decoded). Reports enclosing topic and json path."""
import json,re,sys,io,contextlib,importlib.util,collections
from pathlib import Path
W=Path(sys.argv[1]);sys.argv=['x',str(W)]
spec=importlib.util.spec_from_file_location('r3',str(Path(__file__).parent/'r3_topics_capsules.py'))
with contextlib.redirect_stdout(io.StringIO()):
    r3=importlib.util.module_from_spec(spec);spec.loader.exec_module(r3)
SEP=r'[\s\W_]{1,12}'
OLD=[re.compile(r'15'+SEP+r'(?:as'+SEP+r')?(?:calculad\w*|computad\w*|computed|calculated)'+SEP+r'(?:e|and|plus|\+|mais|com)?'+SEP+r'3'+SEP+r'(?:as'+SEP+r')?liter\w*',re.I),
     re.compile(r'(?:15|quinze)'+SEP+r'(?:bandeiras'+SEP+r')?(?:calculad\w*|computed|calculated)',re.I),
     re.compile(r'\b(?:3|tres|três|three)'+SEP+r'(?:flags'+SEP+r'|bandeiras'+SEP+r')?(?:literais|literal|literals)\b',re.I)]
NEW=[re.compile(r'18'+SEP+r'(?:bandeiras'+SEP+r')?(?:calculad\w*|computed)[^\n]{0,160}?0'+SEP+r'liter\w*',re.I),
     re.compile(r'(?:all|todas)'+SEP+r'(?:18'+SEP+r')?(?:flags'+SEP+r')?(?:are'+SEP+r')?(?:computed|calculad\w*)',re.I),
     re.compile(r'\b0'+SEP+r'liter(?:ais|al|als)\b',re.I)]
MARKS=re.compile(r'v403|supera|ficam? como registro|verdadeiros? na sua data|stay as (?:a )?record|remain as (?:a )?record|recomput',re.I)
def topic_at(head_text,pos):
    hs=[m for m in re.finditer(r'(?m)^### ([^\n]+)$',head_text) if m.start()<=pos]
    return hs[-1][1] if hs else None
out={}
for pkg in ('shared','haiku_expanded','haiku55','sonnet_public'):
    t=(W/'app/packages'/pkg/'prefix.md').read_text('utf-8')
    res={'bytes':len(t.encode()),'raw':{},'decoded':{}}
    # RAW
    for k,rx in enumerate(OLD):
        hits=[]
        for m in rx.finditer(t):
            ctx=t[max(0,m.start()-700):m.end()+700]
            hits.append({'topic':topic_at(t,m.start()),'span':[m.start(),m.end()],'text':t[m.start():m.end()][:90].replace('\n',' '),'marker_nearby':bool(MARKS.search(ctx))})
        res['raw']['old%d'%k]=hits
    for k,rx in enumerate(NEW):
        res['raw']['new%d'%k]=len(list(rx.finditer(t)))
    # DECODED
    head,_,expo=t.partition(r3.MARK);head=r3.unalias(head)
    m=re.search(r'(?:DICIONÁRIO DE LITERAIS|LITERAIS_COMPARTILHADOS)\n(\{.*\})\n',head);D=json.loads(m.group(1)) if m else {}
    FL=json.loads(re.search(r'DICIONÁRIO DE INDICADORES LITERAIS\n(\{.*\})\n',head).group(1)) if 'DICIONÁRIO DE INDICADORES LITERAIS' in head else {}
    E=expo.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
    # the dictionary itself, decoded
    dec_hits=collections.defaultdict(list)
    def scan(s,where):
        for k,rx in enumerate(OLD):
            for mm in rx.finditer(s):
                ctx=s[max(0,mm.start()-700):mm.end()+700]
                dec_hits['old%d'%k].append({'where':where,'text':s[mm.start():mm.end()][:90],'marker_nearby':bool(MARKS.search(ctx))})
    for lid,val in D.items():
        dv=r3.dec_lit(val,D,E)
        if isinstance(dv,str):scan(dv,'DICT:'+lid)
        else:scan(json.dumps(dv,ensure_ascii=False,default=lambda o:'SUMMARY_REF'),'DICT:'+lid)
    hs=list(re.finditer(r'(?m)^### ([^\n]+)\n',head))
    for i,h in enumerate(hs):
        seg=head[h.end():(hs[i+1].start() if i+1<len(hs) else len(head))]
        for ln in seg.split('\n'):
            if ln.startswith(('{','[')):
                try:v=json.loads(ln)
                except Exception:continue
                if isinstance(v,dict) and '@B' in v:v.update(FL[str(v.pop('@B'))])
                try:dv=r3.dec_lit(r3.unpack(v),D,E)
                except Exception:continue
                scan(json.dumps(dv,ensure_ascii=False,default=lambda o:'SUMMARY_REF'),'TOPIC:'+h[1])
            elif not ln.startswith('Fonte:'):
                scan(ln,'TEXT:'+h[1])
    # exposition (canonical text)
    scan(E,'EXPOSITION')
    res['decoded']={k:v for k,v in dec_hits.items()}
    res['has_bandeiras_v403_block']=('### bandeiras_do_gate_v403\n' in t)
    out[pkg]=res
# compact summary
summary={}
for pkg,r in out.items():
    s={'bytes':r['bytes'],'has_bandeiras_do_gate_v403':r['has_bandeiras_v403_block']}
    for k in ('old0','old1','old2'):
        s['RAW_'+k]=[(h['topic'],h['text'],h['marker_nearby']) for h in r['raw'][k]]
        s['DEC_'+k]=[(h['where'],h['text'],h['marker_nearby']) for h in r['decoded'].get(k,[])]
    s['RAW_new_counts']={k:v for k,v in r['raw'].items() if k.startswith('new')}
    s['DEC_new']='n/a'
    summary[pkg]=s
print(json.dumps(summary,ensure_ascii=False,indent=1))
