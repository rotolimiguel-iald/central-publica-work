"""Launch exactly one authorized local worker, with a durable start receipt."""
from pathlib import Path
import datetime, json, os, runpy, subprocess, sys

C=Path(__file__).resolve().parent
m=runpy.run_path(str(C/'media_v404_worker.py'))
save,pin,load=m['save_original'],m['pin'],m['load']

def main():
    assert '--start-authorized' in sys.argv
    from types import SimpleNamespace
    m['main'].__globals__['options']=SimpleNamespace(start_authorized=True,data_ready=C/'DATA_READY.json',audio_ready=C/'AUDIO_READY.json',audio_dir=m['R']/'audio')
    go=m['launch_guard']()
    preflight=m['preflight']()
    path=C/'MEDIA_START.json'
    assert not path.exists(), 'Start already recorded; recover its exact process, never duplicate'
    assert not m['LOCK'].exists() and not m['BASE'].exists()
    assert not list((m['R']/'render/.pipeline').glob('*.lock'))
    tested=load(C/'MEDIA_WORKER_TESTS.json')
    assert tested['status']=='PASS' and tested['worker']==pin(C/'media_v404_worker.py')
    command=[sys.executable,'-B','-X','utf8',str(C/'media_v404_worker.py'),'--start-authorized']
    value={'status':'START_INTENT','worker':pin(C/'media_v404_worker.py'),'launcher':pin(Path(__file__)),
           'go':go,'preflight':preflight,'source':'v404','source_sha256':load(C/'SOURCE_CAPTURE.json')['source_sha256'],
           'command':command,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'handle_id':'v404-media-worker-20261027','render_started_by_worker':False,
           'stdout':str(C/'MEDIA_WORKER.stdout.log'),'stderr':str(C/'MEDIA_WORKER.stderr.log')}
    save(path,value)
    with (C/'MEDIA_WORKER.stdout.log').open('xb') as out,(C/'MEDIA_WORKER.stderr.log').open('xb') as err:
        child=subprocess.Popen(command,cwd=C,stdin=subprocess.DEVNULL,stdout=out,stderr=err,
                    creationflags=subprocess.CREATE_NO_WINDOW|subprocess.CREATE_NEW_PROCESS_GROUP,
                    close_fds=True)
    value.update(status='STARTED_ONCE',pid=child.pid)
    save(path,value)
    print(json.dumps({'status':value['status'],'pid':child.pid,'receipt':pin(path)}))

if __name__=='__main__':main()
