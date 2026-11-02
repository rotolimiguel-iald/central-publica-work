"""Read-only current source, capture and encode progress."""
from context import *
def main():
 seal=read(N/'um_absoluto_selo.json');rows=[]
 for p in (V/'cinema/render/jobs').glob('*.json'):
  r=read(p);meta=r.get('metadata',{})
  if meta.get('source')=='v404':rows.append({'id':r.get('id'),'kind':meta.get('kind'),'frames':r.get('frames',r.get('render',{}).get('encoded')),'total':meta.get('total'),'complete':bool(r.get('finished_at'))})
 latest={}
 for row in rows:
  key=row['id']
  if key not in latest or row['complete'] or row['frames']>latest[key]['frames']:latest[key]=row
 state=read(H/'MEDIA_WATCH.json') if (H/'MEDIA_WATCH.json').exists() else {}
 print(json.dumps({'current_seal':seal['um_version'],'expected_seal_unchanged':pin(N/'um_absoluto_selo.json')==read(H/'SOURCE_CAPTURE.json')['canonical_seal'],'worker':state.get('status'),'completed':list(state.get('completed',{})),'jobs':list(latest.values()),'elapsed_worker_seconds':state.get('elapsed_seconds'),'actions':state.get('timings',[])},ensure_ascii=False))
if __name__=='__main__':main()
