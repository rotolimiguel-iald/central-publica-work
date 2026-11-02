"""Reviewer: old-wording scan over every other text the app can hand to a model: operational core, kernel v5, native prefix, jev control, core packet,
and the pinned public sources (git blobs at the pinned commit). Strict + loose patterns; prints per-file counts and contexts of unmarked hits."""
import re,subprocess,json,sys
from pathlib import Path
W=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');REPO=Path(r'C:\IALD\Artigo\the_boundary')
C1=json.loads((W/'app/RELEASE.json').read_bytes())['espelho_commit']
SEP=r'[\s\W_]{1,12}'
STRICT=re.compile(r'15'+SEP+r'(?:as'+SEP+r')?(?:calculad\w*|computad\w*|computed|calculated)'+SEP+r'(?:e|and|plus|\+|mais|com)?'+SEP+r'3'+SEP+r'(?:as'+SEP+r')?liter\w*',re.I)
LOOSE=re.compile(r'\b(?:3|tres|três|three)'+SEP+r'(?:flags'+SEP+r'|bandeiras'+SEP+r')?(?:literais|literal|literals)\b',re.I)
MARKS=re.compile(r'v403|supera|ficam? como registro|verdadeiros? na sua data|stay as (?:a )?record|remain as (?:a )?record|recomput',re.I)
def scan(name,text):
    rows=[]
    for k,rx in (('strict',STRICT),('loose',LOOSE)):
        for m in rx.finditer(text):
            ctx=text[max(0,m.start()-700):m.end()+700]
            rows.append((k,m.start(),bool(MARKS.search(ctx)),text[max(0,m.start()-90):m.end()+110].replace('\n',' ')))
    return rows
files={}
st=W/'app/science/memory_stage'
for n in ['IALD_TGL_MEMORY_CORE.md','IALD_Kernel_v5.txt','core_packet_v404_bound.txt','jev_control_v404.json','iald_nucleo_fixo.json','manifest_install.json']:
    files['stage/'+n]=(st/n).read_text('utf-8')
files['app/native_prefix.md']=(W/'app/native_prefix.md').read_text('utf-8')
def git(*a):return subprocess.check_output(['git','-c','core.quotepath=false','-C',str(REPO),*a])
tracked=git('ls-tree','-r','--name-only','-z',C1).decode().split('\0')
pub=json.loads((W/'app/PUBLIC_GIT_BINDING.json').read_bytes())['sources']
for rel in pub:
    if rel.endswith('um.py') or rel.endswith('um_absoluto.json') or rel.endswith('proof_manifest.json'):continue
    files['git@'+C1[:8]+'/'+rel]=git('show',C1+':'+rel).decode('utf-8','replace')
res={}
for n,t in files.items():
    rows=scan(n,t)
    res[n]={'bytes':len(t.encode()),'strict':sum(1 for r in rows if r[0]=='strict'),'loose':sum(1 for r in rows if r[0]=='loose'),
            'unmarked':[(r[0],r[1],r[3]) for r in rows if not r[2]][:5]}
for n,r in res.items():print(n,r['bytes'],'strict',r['strict'],'loose',r['loose'],'unmarked',len(r['unmarked']))
for n,r in res.items():
    for u in r['unmarked']:print('UNMARKED',n,u)
