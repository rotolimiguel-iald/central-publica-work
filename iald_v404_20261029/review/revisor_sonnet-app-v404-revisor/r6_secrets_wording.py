"""Reviewer: secrets/confidential scan of the whole build folder; forbidden-wording (CONFIRMED/confirmada) delta vs the accepted v402 prefixes; qualifiers present."""
import re,json,sys
from pathlib import Path
W=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');V2=Path(r'C:\IALD\Central de Patentes\work\iald_v402_20261027')
SKIP={'review','validation'}
sec=[re.compile(p) for p in (r'sk-ant-[A-Za-z0-9_\-]{20,}',r'\bsk-[A-Za-z0-9]{32,}',r'AKIA[0-9A-Z]{16}',r'ghp_[A-Za-z0-9]{30,}',r'xox[baprs]-[A-Za-z0-9\-]{10,}',r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',
    r'(?i)"(?:api_key|apikey|secret|password|passwd|authorization)"\s*:\s*"[^"\s]{8,}"',r'(?i)\b(?:api_key|token|password|secret)\s*=\s*[\'"][^\'"\s]{12,}[\'"]')]
conf=re.compile(r'iald_stack_v7|iald_psion_state|iald_web_server|\.env\b',re.I)
hits=[];confhits={};n=0
for p in W.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(W)
    if rel.parts[0] in SKIP:continue
    if p.stat().st_size>60_000_000:continue
    n+=1
    b=p.read_bytes()
    try:t=b.decode('utf-8')
    except UnicodeDecodeError:t=b.decode('latin-1')
    for rx in sec:
        for m in rx.finditer(t):hits.append((str(rel),rx.pattern[:30],t[max(0,m.start()-20):m.end()+10][:80]))
    c=conf.findall(t)
    if c:confhits[str(rel)]=sorted(set(x.lower() for x in c))
print('files scanned',n,'secret-pattern hits',len(hits));
for h in hits[:15]:print('  HIT',h)
print('files mentioning confidential names (name/path only):')
for k,v in sorted(confhits.items()):print('  ',k,v)
# wording delta
CONF=re.compile(r'confirmed|confirmada|confirmado|confirmadas|confirmados|CONFIRMED|confirm(?:a|e)\w*',re.I)
QUAL=re.compile(r'not[_ ]|nunca|never|n[aã]o|NOT|creditaç|creditation|recus|proibid|forbidden|≠|!=|\bsem\b|without|nenhum|no ',re.I)
def texts(wd):
    d={}
    for f in('shared','haiku_expanded','sonnet_public'):d[f]=(wd/'app/packages'/f/'prefix.md').read_text('utf-8')
    return d
t4=texts(W);t2=texts(V2)
for f in t4:
    a=t4[f];b=t2[f]
    new=[];total=0
    for m in CONF.finditer(a):
        total+=1
        w=a[max(0,m.start()-70):m.end()+70]
        if w not in b:new.append((m.start(),w.replace('\n',' ')))
    unq=[x for x in new if not QUAL.search(x[1])]
    print(f,'confirm-hits',total,'(v402:',len(CONF.findall(b)),') new-window',len(new),'unqualified-new',len(unq))
    for x in unq[:6]:print('    UNQUALIFIED?',x)
# qualifiers
for f,t in t4.items():
    low=t.lower()
    print(f,{q:(q.lower() in low) for q in ['CONDITIONAL','CONDICIONAL','UNINHABITED','BIJECTION','HILBERT','CREDITATION','NATURE_TEST_COMPLETED','MORE_SENSITIVE_DATA_COULD_REVISE']})
