"""Reviewer: count the corrected wording; check bandeiras_do_gate_v403 in full in haiku55 and haiku_expanded; check key correcting statements present."""
import json,re,sys,io,contextlib,importlib.util
from pathlib import Path
W=Path(sys.argv[1]);sys.argv=['x',str(W)]
spec=importlib.util.spec_from_file_location('r3',str(Path(__file__).parent/'r3_topics_capsules.py'))
with contextlib.redirect_stdout(io.StringIO()):
    r3=importlib.util.module_from_spec(spec);spec.loader.exec_module(r3)
core,res=r3.core,r3.res
SEP=r'[\s\W_]{1,12}'
NEWRX={'18_calculadas_0_literais':re.compile(r'18'+SEP+r'(?:de'+SEP+r'18'+SEP+r')?(?:bandeiras'+SEP+r')?(?:calculad\w*|computed)[^\n]{0,200}?\b0'+SEP+r'liter\w*',re.I),
       '18_computed_0_literal':re.compile(r'(?:18|all'+SEP+r'18)'+SEP+r'(?:flags'+SEP+r')?(?:are'+SEP+r')?computed[^\n]{0,200}?(?:0'+SEP+r'literal|none'+SEP+r'is'+SEP+r'a'+SEP+r'literal)',re.I),
       'todas_calculadas':re.compile(r'todas'+SEP+r'(?:as'+SEP+r')?(?:18'+SEP+r')?(?:bandeiras'+SEP+r')?calculad',re.I),
       '0_literais_any':re.compile(r'\b0'+SEP+r'liter(?:ais|al)\b',re.I),
       'none_is_a_literal':re.compile(r'none'+SEP+r'is'+SEP+r'a'+SEP+r'literal',re.I)}
out={}
for pkg in ('shared','haiku_expanded','haiku55','sonnet_public'):
    t=(W/'app/packages'/pkg/'prefix.md').read_text('utf-8')
    head,_,expo=t.partition(r3.MARK);head=r3.unalias(head)
    m=re.search(r'(?:DICIONÁRIO DE LITERAIS|LITERAIS_COMPARTILHADOS)\n(\{.*\})\n',head);D=json.loads(m.group(1)) if m else {}
    FL=json.loads(re.search(r'DICIONÁRIO DE INDICADORES LITERAIS\n(\{.*\})\n',head).group(1)) if 'DICIONÁRIO DE INDICADORES LITERAIS' in head else {}
    E=expo.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
    # decoded full text (topic JSON lines decoded + dictionary + text lines + exposition)
    pieces=[]
    for lid,val in D.items():pieces.append(json.dumps(r3.dec_lit(val,D,E),ensure_ascii=False,default=lambda o:'SUMMARY_REF'))
    hs=list(re.finditer(r'(?m)^### ([^\n]+)\n',head))
    for i,h in enumerate(hs):
        seg=head[h.end():(hs[i+1].start() if i+1<len(hs) else len(head))]
        for ln in seg.split('\n'):
            if ln.startswith(('{','[')):
                try:
                    v=json.loads(ln)
                    if isinstance(v,dict) and '@B' in v:v.update(FL[str(v.pop('@B'))])
                    pieces.append(json.dumps(r3.dec_lit(r3.unpack(v),D,E),ensure_ascii=False,default=lambda o:'SUMMARY_REF'))
                except Exception:pieces.append(ln)
            else:pieces.append(ln)
    pieces.append(E)
    dec='\n'.join(pieces)
    out[pkg]={'raw':{k:len(rx.findall(t)) for k,rx in NEWRX.items()},'decoded':{k:len(rx.findall(dec)) for k,rx in NEWRX.items()}}
    # bandeiras_do_gate_v403 completeness
    n='bandeiras_do_gate_v403'
    body=None
    for i,h in enumerate(hs):
        if h[1]==n:body=head[h.end():(hs[i+1].start() if i+1<len(hs) else len(head))]
    lines=[l for l in body.split('\n') if l.strip() and not l.startswith('Fonte:')]
    v=json.loads(lines[0])
    if isinstance(v,dict) and '@B' in v:v.update(FL[str(v.pop('@B'))])
    dv=r3.dec_lit(r3.unpack(v),D,E)
    def refs(x):
        if isinstance(x,dict):
            return (1 if '@' in x else 0)+sum(refs(y) for y in x.values())
        if isinstance(x,list):return sum(refs(y) for y in x)
        return 0
    def leaves(x):
        if isinstance(x,dict):return sum(leaves(y) for y in x.values())
        if isinstance(x,list):return sum(leaves(y) for y in x)
        return 1
    rep=[];got=r3.restore(dv,res,'/core/'+n,rep,E)
    out[pkg]['bandeiras_do_gate_v403']={'present':True,'form_top_level_capsule':isinstance(dv,dict) and '@' in dv,'pointer_refs_in_block':refs(dv),'decoded_restore_equals_sealed_topic':got==core[n],'source_leaves':leaves(core[n]),'inline_leaves_in_block':leaves(dv),'summary_refs_in_block':json.dumps(dv,default=lambda o:'SUMMARY_REF').count('SUMMARY_REF'),'block_bytes':len(body.encode())}
    # the topic's own correcting statements (sealed source)
    s=json.dumps(core[n],ensure_ascii=False)
    out[pkg]['source_topic_states']={'18_calculadas_0_literais':bool(re.search(r'18[^"]{0,40}CALCULADAS[^"]{0,60}0 literais',s)),'veredito_le_15':'15' in s}
# the superseding statements as they are in the sealed topic
n='bandeiras_do_gate_v403'
print(json.dumps({'sealed_topic_estatuto':core[n].get('estatuto'),'sealed_topic_scope':core[n].get('scope'),'sealed_topic_verdict':core[n].get('verdict'),'keys':list(core[n].keys())},ensure_ascii=False,indent=1)[:3500])
print(json.dumps(out,ensure_ascii=False,indent=1))
