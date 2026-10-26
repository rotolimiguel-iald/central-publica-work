"""Mission glue for the app unit: claim / submit / accept with an EXPLICIT actor.

No default actor and no invented reviewer: the id is always passed on the command line. Receipts are
written once (xb) under receipts/. Not exercised against a live mission (none exists in phase A).

  python -B -X utf8 mission_step.py project
  python -B -X utf8 mission_step.py claim  <task_id> --actor ID [--lease-seconds N] [--event-suffix S]
  python -B -X utf8 mission_step.py submit <task_id> --actor ID --evidence FILE [FILE ...] [--event-suffix S]
  python -B -X utf8 mission_step.py accept <task_id> --actor ID --evidence FILE [FILE ...] [--event-suffix S]
      (accept: the reviewer's OWN artifacts; the server refuses the submitter as reviewer)
"""
import argparse,hashlib,json,sys
from pathlib import Path
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W))
import task
def pin(p):
    p=Path(p).resolve();assert p.is_file(),str(p)
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def receipt(name,value):
    d=W/'receipts';d.mkdir(exist_ok=True)
    with (d/name).open('xb') as f:f.write(json.dumps(value,ensure_ascii=False,indent=2).encode())
def main():
    a=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('op',choices=['project','claim','submit','accept']);a.add_argument('task_id',nargs='?')
    a.add_argument('--actor');a.add_argument('--lease-seconds',type=int,default=14400)
    a.add_argument('--evidence',nargs='+',default=[]);a.add_argument('--event-suffix',default='');a.add_argument('--note',default='')
    x=a.parse_args()
    p=task.project()
    if x.op=='project':
        print(json.dumps({'revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'active':[{k:t.get(k) for k in ('id','status','lease')} for t in p['projection']['active']]},ensure_ascii=False,indent=1));return
    if not x.task_id or not x.actor:a.error('task_id and --actor are required')
    event=task.REL+'-'+x.task_id+'-'+x.op+(('-'+x.event_suffix) if x.event_suffix else '')
    if x.op=='claim':
        r=task.act('claim',actor=x.actor,task_id=x.task_id,lease_seconds=x.lease_seconds,event_id=event)
    else:
        if not x.evidence:a.error('--evidence is required for '+x.op)
        ev=[pin(f) for f in x.evidence]
        if x.op=='submit':
            t=next(t for t in p['projection']['active'] if t['id']==x.task_id)
            r=task.act('submit',actor=x.actor,task_id=x.task_id,lease_id=t['lease']['id'],evidence=ev,event_id=event,note=x.note)
        else:
            r=task.act('accept',actor=x.actor,task_id=x.task_id,review_evidence=ev,event_id=event,note=x.note)
    receipt(event+'.json',r)
    print(json.dumps({'op':x.op,'task':x.task_id,'actor':x.actor,'event_id':event,'revision':r['receipt']['revision'],'status':(r.get('task') or {}).get('status')},ensure_ascii=False))
if __name__=='__main__':main()
