"""Custody of the primary public papers consulted for the network contract."""
from pathlib import Path
import urllib.request
import hashlib
import json
import datetime as dt
import os

out=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REDE\sources')
items=[('BGL_2002_v2.pdf','https://arxiv.org/pdf/math-ph/0203021v2'),
       ('Fewster_Verch_1106.4785.pdf','https://arxiv.org/pdf/1106.4785')]
receipt=[]
for name,url in items:
    p=out/name
    if p.exists(): raise FileExistsError(p)
    with urllib.request.urlopen(url, timeout=45) as r:
        b=r.read(); final=r.url
    if not b.startswith(b'%PDF'): raise ValueError('Not PDF: '+url)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert tmp.read_bytes()==b
    os.rename(tmp,p)
    receipt.append({'url':url,'final_url':final,'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
with (out/'PUBLIC_PRIMARY_CUSTODY_R1.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,ensure_ascii=False,indent=2)
print(json.dumps(receipt,ensure_ascii=False))
