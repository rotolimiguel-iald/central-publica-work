"""Capture a new candidate qualification without overwriting prior receipts."""
from pathlib import Path
import sys,subprocess,hashlib,json,datetime,time
HERE=Path(__file__).resolve().parent
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
if __name__=='__main__':
    names=['TEST_LOG_R1.txt','RESULT_R1.json']
    for name in names:
        if (HERE/name).exists():raise FileExistsError(name)
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.monotonic()
    command=[sys.executable,'-B','-X','utf8',str(HERE/'test_operations.py'),'-v']
    r=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
    end=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (HERE/names[0]).open('xb') as f:f.write((r.stdout+r.stderr).encode('utf-8'))
    record={'status':'PASS_SYNTHETIC_CANDIDATE' if r.returncode==0 else 'FAIL','exit':r.returncode,
            'command':command,'start_utc':start,'end_utc':end,'seconds':time.monotonic()-clock,
            'source_pins':[pin(HERE/n) for n in ['admission.py','preflight_bridge.py','numerical_qualification.py','POLICY_R1.json','test_operations.py']],
            'log':pin(HERE/names[0]),'actual_D_H_received':False,'observed_data_opened':False,
            'authority_limit':'Trusted act pin must originate from authenticated operator workflow; this candidate does not authenticate humans.',
            'numerical_limit':'Refinement refusal implemented; agreement is diagnostic, not a certified global error bound.',
            'first_attempt_note':pin(HERE/'FIRST_ATTEMPT_NOTE.json')}
    with (HERE/names[1]).open('xb') as f:f.write(json.dumps(record,ensure_ascii=False,indent=2).encode('utf-8'))
    print(json.dumps({'status':record['status'],'exit':r.returncode,'seconds':record['seconds']}))
    sys.exit(r.returncode)
