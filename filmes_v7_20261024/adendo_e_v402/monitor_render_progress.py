"""Read-only progress monitor. Never starts, retries or changes a render."""
from pathlib import Path
import datetime, json, time

E = Path(__file__).resolve().parent
J = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7\cinema\render\jobs')

def snapshot():
    rows = []
    for path in J.glob('*.json'):
        if '.bak_' in path.name: continue
        try: data = json.loads(path.read_bytes())
        except (OSError, ValueError): continue
        meta = data.get('metadata', {})
        if meta.get('source') != 'v402': continue
        if path.name.endswith('.progress.json'):
            rows.append({'kind':meta.get('kind'), 'id':data.get('id'),
                         'frames':data.get('frames'), 'total':meta.get('total')})
        else:
            render = data.get('render', {})
            rows.append({'receipt':path.name, 'kind':meta.get('kind'),
                         'encoded':render.get('encoded'), 'total':meta.get('total')})
    watch = {}
    if (E/'MEDIA_WATCH.json').exists():
        watch = json.loads((E/'MEDIA_WATCH.json').read_bytes())
    return {'at':datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
            'jobs':rows,'worker_status':watch.get('status'),
            'stage':watch.get('stage'), 'error':watch.get('error')}

if __name__ == '__main__':
    while True:
        result = snapshot()
        print(json.dumps(result, ensure_ascii=False), flush=True)
        if result['worker_status'] in {'COMPLETE','FAILED','STOPPED','ERROR'}: break
        time.sleep(45)
