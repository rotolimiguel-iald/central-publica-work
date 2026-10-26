"""Validate file pins and exact excerpts in the three bounded source inventories."""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

BASE=Path(__file__).resolve().parent
def pin(p):
    data=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}

def new(name,data):
    with (BASE/name).open('xb') as f:
        f.write(json.dumps(data,ensure_ascii=False,indent=2).encode())

def main():
    for n in ['SOURCES_VERIFIED.json','PRIMARY_ERRATA.json']:
        if (BASE/n).exists(): raise FileExistsError(BASE/n)
    checks=[]
    for name in ['ROOT_SOURCES.json','MASS_SOURCES.json','H3_SOURCES.json']:
        d=json.loads((BASE/name).read_text(encoding='utf-8'))
        for s in d['sources']:
            p=Path(s['path']);actual=pin(p)
            if actual['sha256']!=s['sha256']: raise RuntimeError(f'Pin changed: {p}')
            lines=p.read_text(encoding='utf-8-sig').splitlines()
            anchors=s.get('anchors',s.get('excerpts',[]))
            for a in anchors:
                if 'start_line' in a:
                    lo,hi=a['start_line'],a['end_line']
                else:
                    lo,hi=a['first_line'],a['last_line']
                if not (1<=lo<=hi<=len(lines)): raise RuntimeError(f'Range invalid: {p}')
                if a['text']!='\n'.join(lines[lo-1:hi]): raise RuntimeError(f'Excerpt changed: {p}')
            checks.append({'catalog':name,**actual,'exact_excerpts':len(anchors)})
    p=Path(r'C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py')
    lines=p.read_text(encoding='utf-8').splitlines()
    new('PRIMARY_ERRATA.json',{'author':'codex-gerente-tgl','status':'REAL_DOCUMENTARY_WITH_SCOPE',
       'corrects':'MASS_SOURCES.json reuse_matrix M11: historical Chandrasekhar route must not be used as current prediction',
       'source':{**pin(p),'start_line':17878,'end_line':17898,
                 'text':'\n'.join(lines[17877:17898])},
       'scope':'Records the explicit author withdrawal; empirical numbers in this passage are not revalidated here.'})
    new('SOURCES_VERIFIED.json',{'status':'PASS_PINS_AND_EXACT_EXCERPTS',
        'timestamp_utc':datetime.now(timezone.utc).isoformat(),'checks':checks,
        'catalog_entries':len(checks),'unique_source_files':len({x['path'] for x in checks}),
        'excerpt_count':sum(x['exact_excerpts'] for x in checks),
        'scope':'Read-only custody checks, not a build or proof of the scientific content.'})
    print(json.dumps({'status':'PASS','catalog_entries':len(checks),
          'unique_sources':len({x['path'] for x in checks}),
          'exact_excerpts':sum(x['exact_excerpts'] for x in checks)}))

if __name__=='__main__':main()
