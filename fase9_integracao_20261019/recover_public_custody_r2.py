"""Explicit retry of public GETs after DNS failure; no scientific execution retry."""
from custody_missing_readers_r2 import ROOT,pin,save,Text,Request,urlopen,json,datetime,os
d=ROOT/'r5_source_completion'
assert (d/'FETCH_FAILURE_R2.json').exists()
assert not list(d.glob('*.html'))
plan=json.loads((d/'FETCH_PLAN_R2.json').read_text(encoding='utf-8'))
receipts=[]
for name,url in plan['sources']:
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with urlopen(Request(url,headers={'User-Agent':'IALD-Research-Custody/1.0'}),timeout=40) as r:
            raw=r.read(4_000_001);meta={'status':r.status,'final_url':r.url,'content_type':r.headers.get('Content-Type')}
        assert raw and len(raw)<=4_000_000 and b'<html' in raw.lower()
        path=d/(name+'.html')
        with path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        parser=Text();parser.feed(raw.decode('utf-8',errors='strict'))
        text='\n'.join(' '.join(x.split()) for x in ''.join(parser.parts).splitlines() if x.strip())+'\n'
        save('r5_source_completion/'+name+'.txt',text)
        receipts.append({'name':name,'requested_url':url,'started_utc':start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),**meta,'raw':pin(path),'derived_text':pin(d/(name+'.txt'))})
    except Exception as e:
        receipts.append({'name':name,'url':url,'error':type(e).__name__+': '+str(e)})
        save('r5_source_completion/FETCH_RECOVERY_FAILURE_R2.json',receipts);raise
save('r5_source_completion/CUSTODY_R2.json',{'status':'PUBLIC_BYTES_CUSTODIED_NOT_ADMITTED','sources':receipts,
 'text_transformation':'HTMLParser, scripts/styles omitted, per-line whitespace normalized',
 'previous_failure':pin(d/'FETCH_FAILURE_R2.json'),'recovery':'Public GET after sandbox DNS failure; no scientific execution or provider request',
 'statistical_composition':False,'operator_admission':False,'scripts':[pin(__file__),pin(ROOT/'custody_missing_readers_r2.py')]})
print(json.dumps({'status':'PUBLIC_BYTES_CUSTODIED_NOT_ADMITTED','sources':len(receipts)}))
