"""Reviewer: for the 11 topics new in v404, which top-level qualifier keys (status/scope/verdict/estatuto/limites/diz/nao_diz/...) are inline in shared vs only by pointer; and in v402 for its 5 new topics (uncompressed)."""
import json,re,sys,io,contextlib,importlib.util
from pathlib import Path
def load(wd):
    sys.argv=['x',str(wd)]
    spec=importlib.util.spec_from_file_location('r3x',str(Path(__file__).parent/'r3_topics_capsules.py'))
    with contextlib.redirect_stdout(io.StringIO()):
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m
def block(m,pkg,n):
    t=(m.W/'app/packages'/pkg/'prefix.md').read_text('utf-8');head=m.unalias(t.partition(m.MARK)[0])
    Dm=re.search(r'(?:DICIONÁRIO DE LITERAIS|LITERAIS_COMPARTILHADOS)\n(\{.*\})\n',head);D=json.loads(Dm.group(1)) if Dm else {}
    F=re.search(r'DICIONÁRIO DE INDICADORES LITERAIS\n(\{.*\})\n',head);FL=json.loads(F.group(1)) if F else {}
    E=t.partition(m.MARK)[2].split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
    hs=list(re.finditer(r'(?m)^### ([^\n]+)\n',head))
    for i,h in enumerate(hs):
        if h[1]==n:
            seg=head[h.end():(hs[i+1].start() if i+1<len(hs) else len(head))]
            line=[l for l in seg.split('\n') if l.strip() and not l.startswith('Fonte:')][0]
            v=json.loads(line)
            if isinstance(v,dict) and '@B' in v:v.update(FL[str(v.pop('@B'))])
            return m.dec_lit(m.unpack(v),D,E)
m4=load(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');m2=load(r'C:\IALD\Central de Patentes\work\iald_v402_20261027')
Q=re.compile(r'status|statute|estatuto|verdict|scope|escopo|limites|diz$|nao_diz|hypothes|not_claimed|declar|conditional|condicional',re.I)
def top(m,pkg,n):
    dv=block(m,pkg,n);src=m.core[n]
    if isinstance(dv,dict) and '@' in dv:
        inline=set(k.split('/')[1] for k in dv.get('fields',{}) if k.count('/')>=1)
    else:
        inline={k for k,x in dv.items() if not (isinstance(x,dict) and '@' in x)}
    qk=[k for k in src if Q.search(k)]
    return {'source_top_keys':len(src),'qualifier_keys_in_source':qk,'qualifier_keys_inline':[k for k in qk if k in inline],'qualifier_keys_only_by_pointer':[k for k in qk if k not in inline]}
new4=[n for n in m4.core if n not in m2.core];new2=[n for n in m2.core if n not in json.loads((Path(r'C:\IALD\Central de Patentes\work\iald_v401_20261025_s2')/'app/RELEASE.json').read_bytes()) ] if False else []
res={}
for n in new4:
    res[n]={p:top(m4,p,n) for p in ('shared',)}
for n,r in res.items():
    s=r['shared'];print(n,'| qualifiers only by pointer:',s['qualifier_keys_only_by_pointer'],'| inline:',s['qualifier_keys_inline'])
