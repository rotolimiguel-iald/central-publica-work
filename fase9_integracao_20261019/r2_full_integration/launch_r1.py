"""Single-use Windows receipt around the already pinned synthetic WSL campaign."""
from pathlib import Path
import datetime,hashlib,json,subprocess,time,sys
H=Path(__file__).resolve().parent
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def put(name,obj):
    b=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    with (H/name).open('xb') as f:f.write(b)
def main():
    pin=hashlib.sha256((H/'PLAN_R1.json').read_bytes()).hexdigest()
    if sys.argv[1:]!=[pin]:raise ValueError('Plan SHA required')
    review=json.loads((H/'REVIEW_PREFLIGHT_R1.json').read_bytes())
    if review.get('status')!='PASS_WITH_SCOPE' or review.get('reviewer')!='/root/r68_independent_review':
        raise ValueError('Independent reviewer/status required')
    required={'PLAN_R1.json','run_full_prior_r1.py','launch_r1.py','EXECUTION_LIMITS_R1.txt'}
    covered=set()
    for item in review['evidence']:
        source=Path(item['path'])
        if not source.is_absolute():source=H/source
        if hashlib.sha256(source.read_bytes()).hexdigest()!=item['sha256']:
            raise ValueError('Review evidence changed: '+str(source))
        if source.parent.resolve()==H.resolve():covered.add(source.name)
    if not required<=covered:raise ValueError('Incomplete review coverage')
    linux='/mnt/c/'+str(H/'run_full_prior_r1.py')[3:].replace('\\','/')
    cmd=['wsl.exe','--','env','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','NUMEXPR_NUM_THREADS=1','PYTHONDONTWRITEBYTECODE=1','timeout','--kill-after=10s','600s','/opt/lal_env/bin/python','-B',linux,pin]
    put('LAUNCH_START_R1.json',{'started_utc':stamp(),'command':cmd,'plan_sha256':pin,'execution_count':1})
    start=time.perf_counter()
    cp=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for name,b in [('STDOUT_R1.log',cp.stdout),('STDERR_R1.log',cp.stderr)]:
        with (H/name).open('xb') as f:f.write(b)
    put('COMMAND_RESULT_R1.json',{'ended_utc':stamp(),'seconds':time.perf_counter()-start,'exit_code':cp.returncode,'command':cmd,'plan_sha256':pin,'stdout_sha256':hashlib.sha256(cp.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(cp.stderr).hexdigest(),'no_retry':True})
    print(cp.stdout.decode('utf-8',errors='replace'));print(cp.stderr.decode('utf-8',errors='replace'),file=sys.stderr)
    raise SystemExit(cp.returncode)
if __name__=='__main__':main()
