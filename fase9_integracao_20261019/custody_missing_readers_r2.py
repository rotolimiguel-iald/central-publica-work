"""Archive public source bytes only; no statistical composition or admission."""
from setup_mission import ROOT,pin,save
from pathlib import Path
from urllib.request import Request,urlopen
from html.parser import HTMLParser
import json,datetime,os

class Text(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'):self.skip+=1
        if tag in ('p','div','li','h1','h2','h3','blockquote','br'):self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in ('script','style'):self.skip-=1
        if tag in ('p','div','li','h1','h2','h3','blockquote'):self.parts.append('\n')
    def handle_data(self,s):
        if self.skip==0:self.parts.append(s)

if __name__=='__main__':
    d=ROOT/'r5_source_completion';d.mkdir(exist_ok=False)
    plan=[('L1b_arxiv_2509_01667v1','https://arxiv.org/abs/2509.01667v1'),
          ('L6_ligo_P2400152','https://dcc.ligo.org/LIGO-P2400152/public'),
          ('L6_ligo_summary','https://ligo.org/science-summaries/o4a_cosmology/')]
    save('r5_source_completion/FETCH_PLAN_R2.json',{'sources':plan,'purpose':'Documentary custody only; no observed composition, no source admission'})
    receipts=[]
    for name,url in plan:
        started=datetime.datetime.now(datetime.timezone.utc).isoformat()
        try:
            req=Request(url,headers={'User-Agent':'IALD-Research-Custody/1.0'})
            with urlopen(req,timeout=40) as r:
                raw=r.read(4_000_001)
                if len(raw)>4_000_000:raise ValueError('oversize source')
                meta={'status':r.status,'final_url':r.url,'content_type':r.headers.get('Content-Type')}
            if not raw or b'<html' not in raw.lower():raise ValueError('Expected HTML')
            path=d/(name+'.html')
            with path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
            parser=Text();parser.feed(raw.decode('utf-8',errors='strict'))
            lines=[' '.join(x.split()) for x in ''.join(parser.parts).splitlines() if x.strip()]
            save('r5_source_completion/'+name+'.txt','\n'.join(lines)+'\n')
            receipts.append({'name':name,'requested_url':url,'started_utc':started,
                'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),**meta,
                'raw':pin(path),'derived_text':pin(d/(name+'.txt')),'text_transformation':'HTMLParser; scripts/styles omitted; per-line whitespace normalized'})
        except Exception as e:
            receipts.append({'name':name,'requested_url':url,'started_utc':started,'error':type(e).__name__+': '+str(e)})
            save('r5_source_completion/FETCH_FAILURE_R2.json',receipts)
            raise
    save('r5_source_completion/CUSTODY_R2.json',{'status':'PUBLIC_BYTES_CUSTODIED_NOT_ADMITTED','sources':receipts,
         'source_numbers_read':True,'statistical_composition':False,'operator_admission':False,'script':pin(__file__)})
    print(json.dumps({'status':'PUBLIC_BYTES_CUSTODIED_NOT_ADMITTED','sources':len(receipts)},ensure_ascii=False))
