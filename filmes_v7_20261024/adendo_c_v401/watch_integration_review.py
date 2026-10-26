"""Local readiness watcher only; no render, TTS, model, network or product writes."""
from pathlib import Path
import datetime, hashlib, json, os, sys, time

C=Path(__file__).resolve().parent
TARGETS=('CONSTRUCTION_DELIVERY_V401.json','FINAL_PLAYER_V401.json')

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def write_new(name,value):
    path=C/name
    raw=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    temporary=path.with_name(path.name+'.tmp_'+str(os.getpid()))
    with temporary.open('xb') as stream:
        stream.write(raw);stream.flush();os.fsync(stream.fileno())
    assert temporary.stat().st_size==len(raw)
    if path.exists():
        raise FileExistsError(path)
    os.rename(temporary,path)

def snapshot():
    rows=[]
    for name in TARGETS:
        path=C/name
        try:
            raw=path.read_bytes()
            data=json.loads(raw.decode('utf-8-sig'))
            status=data.get('status')
            if not isinstance(status,str) or not status:
                return None
            if any(word in status.upper() for word in ('WAITING','RUNNING','PENDING','BUILDING')):
                return None
            rows.append({'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),
                         'bytes':len(raw),'declared_status':status,
                         'source':data.get('source'),'source_sha256':data.get('source_sha256')})
        except (FileNotFoundError,PermissionError,UnicodeError,json.JSONDecodeError):
            return None
    return rows

def main():
    # Exclusive persistent start record prevents accidental duplicate watchers.
    lock=C/'INTEGRATION_WATCH_STARTED.json'
    info={'status':'WAITING_FOR_STABLE_INPUTS','pid':os.getpid(),'started_at_utc':now(),
          'interval_seconds':5,'maximum_wait_seconds':21600,'targets':list(TARGETS),
          'network':False,'render':False,'tts':False,'model_calls':0}
    fd=os.open(lock,os.O_WRONLY|os.O_CREAT|os.O_EXCL)
    with os.fdopen(fd,'wb') as stream:
        stream.write((json.dumps(info,ensure_ascii=False,indent=2)+'\n').encode());stream.flush();os.fsync(stream.fileno())
    print(json.dumps(info),flush=True)
    previous=None;deadline=time.monotonic()+21600
    while time.monotonic()<deadline:
        current=snapshot()
        if current is not None and current==previous:
            write_new('INTEGRATION_REVIEW_INPUTS_READY.json',{
                'status':'INPUTS_READY_FOR_DOCUMENTARY_REVIEW','created_at_utc':now(),
                'inputs':current,'stable_observations':2,'observation_interval_seconds':5,
                'review_complete':False,'acceptance':False,
                'next_action':'Recuperar project da referência própria; aplicar INTEGRATION_REVIEW_PROTOCOL.json e emitir FINAL_INTEGRATION_REVIEW.json após leitura/verificação.'})
            print('INPUTS_READY_FOR_DOCUMENTARY_REVIEW',flush=True)
            return
        previous=current
        time.sleep(5)
    write_new('INTEGRATION_WATCH_TIMEOUT.json',{'status':'TIMED_OUT_NO_RETRY','time_utc':now(),
        'last_snapshot':previous,'review_complete':False})

if __name__=='__main__':
    main()
