"""Custody of public scientific documents; no likelihood/sample ingestion."""
from pathlib import Path
import urllib.request, json, hashlib, datetime
ROOT=Path(__file__).resolve().parent
items=[('TDCOSMO_2026_ABSTRACT','https://arxiv.org/abs/2610.14781v1'),
       ('TDCOSMO_2026_HTML','https://arxiv.org/html/2610.14781v1'),
       ('TDCOSMO_2025_ABSTRACT','https://arxiv.org/abs/2506.03023v4'),
       ('COSMOSIS_TDCOSMO','https://cosmosis.readthedocs.io/en/latest/reference/standard_library/tdcosmo.html'),
       ('SN_H0PE','https://arxiv.org/abs/2403.18902')]
rows=[]
for name,url in items:
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'IALD-research-source-custody/1.0'}),timeout=30) as response:
            raw=response.read(); final=response.url;status=response.status
        path=ROOT/(name+'.html')
        with path.open('xb') as f:f.write(raw)
        rows.append({'url':url,'final_url':final,'utc':now,'status':status,'path':str(path),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    except Exception as exc:
        rows.append({'url':url,'utc':now,'status':'FAILED','error':str(exc),'claim':'web-tool reading only; no bytes custodied here'})
with (ROOT/'PUBLIC_SOURCE_CUSTODY.json').open('x',encoding='utf-8') as f:json.dump(rows,f,ensure_ascii=False,indent=2)
print(json.dumps([{'url':r['url'],'status':r['status'],'bytes':r.get('bytes')} for r in rows]))
