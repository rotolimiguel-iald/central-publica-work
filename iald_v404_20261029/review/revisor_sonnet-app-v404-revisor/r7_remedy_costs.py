"""Reviewer: measure (not decide) what it would cost to carry in full the current-release topics: haiku55 (tokens) and shared (bytes)."""
import json,re,sys,io,contextlib,importlib.util
from pathlib import Path
W=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');sys.argv=['x',str(W)]
spec=importlib.util.spec_from_file_location('r3',str(Path(__file__).parent/'r3_topics_capsules.py'))
with contextlib.redirect_stdout(io.StringIO()):
    r3=importlib.util.module_from_spec(spec);spec.loader.exec_module(r3)
core=r3.core
dump=lambda v:json.dumps(v,ensure_ascii=False,separators=(',',':'))
new=['caminho_v403','vida_v403','verdade_adendo_v403','bandeiras_do_gate_v403','projecao_transversal_v404','jo8v32_v404','f2b_errata_v404','cunhagens_v403','kh_n1_cobertura_v403','cunhagens_v404','kh_n1_cobertura_v404']
def blk(pkg,n):
    t=(W/'app/packages'/pkg/'prefix.md').read_text('utf-8');head=t.partition(r3.MARK)[0]
    hs=list(re.finditer(r'(?m)^### ([^\n]+)\n',head))
    for i,h in enumerate(hs):
        if h[1]==n:return head[h.end():(hs[i+1].start() if i+1<len(hs) else len(head))].strip()
rows=[];tot={'haiku55':0,'shared':0}
for n in new:
    full=len(dump(core[n]).encode())+len(('Fonte: resultado_publicado_integral /core/'+n+'\n').encode())
    h=len(blk('haiku55',n).encode());s=len(blk('shared',n).encode())
    rows.append((n,full,h,s,full-h,full-s));tot['haiku55']+=full-h;tot['shared']+=full-s
for r in rows:print('%-28s full=%6d haiku55_now=%6d shared_now=%6d  +haiku55=%6d +shared=%6d'%r)
print('TOTAL extra bytes to carry all 11 in full: haiku55 +%d (~%d tokens at 0.60/byte, ~%d at 0.534 measured) ; shared +%d'%(tot['haiku55'],tot['haiku55']*0.60,tot['haiku55']*0.534,tot['shared']))
b=[r for r in rows if r[0]=='bandeiras_do_gate_v403'][0]
print('ONLY bandeiras_do_gate_v403 in full: haiku55 +%d bytes (~%d tokens at 0.60), headroom now 28640-10000=18640 tokens'%(b[4],b[4]*0.60))
