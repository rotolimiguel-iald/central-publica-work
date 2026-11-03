"""Builder check (read-only; writes GREP_SUPERSEDED_RESULT.json once): the superseded gate-flag wording
('15 calculadas e 3 literais' / '15 computed and 3 literal', any spacing/case/connector) must appear only inside quoted
historical errata that say it was superseded. Scans every file of this build folder (packages, science, texts)."""
import re,json,hashlib
from pathlib import Path
W=Path(__file__).resolve().parent
strict=re.compile(r'15\W{1,6}(?:as\W+)?(?:calculad\w*|computed)\W{1,8}(?:e|and|\+)\W{1,6}3\W{1,6}(?:as\W+)?liter\w*',re.I)
loose=re.compile(r'\b3\W{1,6}(?:as\W+)?liter(?:ais|al|als)\b',re.I)
marks=re.compile(r'na v403|v403 recomput|passam a|ficam como registro|verdadeiros na sua data|superad|substitu|diziam|passa a ler|3 literals? (?:became|were)',re.I)
SELF={'GREP_SUPERSEDED_RESULT.json','grep_superseded_check.py','EXPAND_AND_COMMIT_MEASUREMENTS.json'}
rows=[];scanned=0
for p in sorted(W.rglob('*')):
    if not p.is_file() or p.suffix=='.pyc' or p.name in SELF or '.bak_' in p.name:continue
    if p.relative_to(W).parts[0] in ('superseded_r1','review'):continue  # r2: r1 build moved aside; reviewer folder is not part of the build
    scanned+=1;t=p.read_bytes().decode('utf-8','replace')
    for kind,rx in (('strict',strict),('loose_3_literal',loose)):
        for m in rx.finditer(t):
            ctx=t[max(0,m.start()-600):m.end()+700]
            rows.append({'file':str(p.relative_to(W)),'kind':kind,'offset':m.start(),'superseded_marker_in_context':bool(marks.search(ctx)),'excerpt':t[max(0,m.start()-80):m.end()+120].replace('\n',' ')})
unmarked=[r for r in rows if not r['superseded_marker_in_context']]
byfile={}
for r in rows:byfile.setdefault(r['file'],{'strict':0,'loose_3_literal':0,'all_in_superseded_context':True});byfile[r['file']][r['kind']]+=1;byfile[r['file']]['all_in_superseded_context']&=r['superseded_marker_in_context']
readme=[f for f in byfile if f.endswith('README.md') or f.endswith('read-brief.md')]
out={'status':'GREP_DONE','files_scanned':scanned,'hits_total':len(rows),'strict_hits':sum(r['kind']=='strict' for r in rows),'hits_without_superseded_context':len(unmarked),'hits_in_readme_or_read_brief':readme,'by_file':byfile,'unmarked_excerpts':unmarked[:20],'scope':'every non-backup file under the build folder; marker = text of the same passage saying the wording was true on its date, kept as record, and superseded in v403'}
with (W/'GREP_SUPERSEDED_RESULT.json').open('xb') as f:f.write(json.dumps(out,ensure_ascii=False,indent=2).encode())
print(json.dumps({k:out[k] for k in ('files_scanned','hits_total','strict_hits','hits_without_superseded_context','hits_in_readme_or_read_brief')}));print(json.dumps(byfile,indent=1))
