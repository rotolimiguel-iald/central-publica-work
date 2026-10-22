import datetime
import hashlib
import json
from pathlib import Path
import sys
import time
import traceback

HERE=Path(__file__).resolve().parent

def save(name,obj):
    with (HERE/name).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')

def main():
    for n in ['START_R1.json','RESULT_R1.json']:
        if (HERE/n).exists():raise FileExistsError(n)
    freeze=json.loads((HERE/'FREEZE_R1.json').read_text(encoding='utf-8'))
    for p in freeze['pins']:
        if hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()!=p['sha256']:
            raise ValueError('PREEXEC_PIN_MISMATCH:'+p['path'])
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.perf_counter()
    save('START_R1.json',{'started_utc':start,'command':[sys.executable,'-B','-X','utf8',str(Path(__file__).resolve())],'freeze_sha256':hashlib.sha256((HERE/'FREEZE_R1.json').read_bytes()).hexdigest()})
    code=1
    try:
        from controls_r1 import run
        result=run()
        from nominal_design_r1 import run as nominal_design
        result['nominal_design']=nominal_design()
        code=0 if result['passed'] else 1
    except Exception:result={'passed':False,'traceback':traceback.format_exc()}
    result.update(started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.perf_counter()-t,exit_code=code)
    save('RESULT_R1.json',result)
    print(json.dumps({k:result.get(k) for k in ['passed','count','exit_code','R1_physical_status']}))
    return code

if __name__=='__main__':raise SystemExit(main())
