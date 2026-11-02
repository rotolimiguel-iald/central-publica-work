"""Reviewer: topics new in v404 vs v402 (sealed cores); per package: form and exact restore; text-synthesis counts in v402 vs v404."""
import json,re,sys,io,contextlib,importlib.util
from pathlib import Path
base=Path(r'C:\IALD\Central de Patentes\work')
def load(rel,wd):
    sys.argv=['x',str(wd)]
    spec=importlib.util.spec_from_file_location('r3_'+rel,str(Path(__file__).parent/'r3_topics_capsules.py'))
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf):
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m
m4=load('v404',base/'iald_v404_20261029');m2=load('v402',base/'iald_v402_20261027')
new=[n for n in m4.core if n not in m2.core];gone=[n for n in m2.core if n not in m4.core]
changed=[n for n in m4.core if n in m2.core and m4.core[n]!=m2.core[n]]
print('new topics (v404 not in v402):',len(new),new);print('removed:',gone);print('changed value topics:',len(changed),changed[:40])
def form(m,pkg,n):
    t=(m.W/'app/packages'/pkg/'prefix.md').read_text('utf-8');head=t.partition(m.MARK)[0]
    i=head.find('\n### '+n+'\n');seg=head[i+5+len(n)+1:]
    j=seg.find('\n### ');seg=seg[:j] if j>=0 else seg
    lines=[l for l in seg.split('\n') if l.strip() and not l.startswith('Fonte:')]
    first=lines[0] if lines else ''
    return ('JSON_CAPSULE' if first.startswith('{"@"') else 'JSON' if first.startswith(('{','[','"')) or re.match(r'^[-0-9tfn]',first) else 'TEXT'),len(seg)
for n in new:
    print(n,{p:form(m4,p,n) for p in ('shared','sonnet_public','haiku_expanded','haiku55')})
# text synthesis counts
def count_text(m,pkg):
    c=0
    for n in m.core:
        if form(m,pkg,n)[0]=='TEXT':c+=1
    return c
print('TEXT-form topics shared v402/v404:',count_text(m2,'shared'),count_text(m4,'shared'),' haiku55:',count_text(m2,'haiku55'),count_text(m4,'haiku55'))
