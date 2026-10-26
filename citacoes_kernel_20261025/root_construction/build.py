from pathlib import Path
import os,json,subprocess,time,datetime,hashlib,sys
W=Path(__file__).resolve().parent
K=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN=r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
name=sys.argv[1]
src=W/(name+'.lean')
assert src.exists()
for ext in ['.olean','.log','.receipt.json']:
    assert not (W/(name+ext)).exists()
paths=[W,K/'.lake/build/lib/lean']+[p/'.lake/build/lib/lean' for p in (K/'.lake/packages').iterdir() if (p/'.lake/build/lib/lean').exists()]
env=os.environ.copy();env['LEAN_PATH']=';'.join(str(p) for p in paths)
cmd=[LEAN,'-o',str(W/(name+'.olean')),str(src)]
start=datetime.datetime.now(datetime.timezone.utc).isoformat();tic=time.monotonic()
r=subprocess.run(cmd,cwd=W,env=env,capture_output=True)
end=datetime.datetime.now(datetime.timezone.utc).isoformat();seconds=time.monotonic()-tic
rec={'command':cmd,'toolchain':subprocess.run([LEAN,'--version'],capture_output=True,text=True).stdout.strip(),'LEAN_PATH':env['LEAN_PATH'],'start':start,'end':end,'seconds':seconds,'exit_code':r.returncode,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
with (W/(name+'.log')).open('xb') as f:f.write((json.dumps(rec,ensure_ascii=False,indent=2)+'\n').encode()+r.stdout+r.stderr)
if (W/(name+'.olean')).exists():rec['olean_sha256']=hashlib.sha256((W/(name+'.olean')).read_bytes()).hexdigest()
with (W/(name+'.receipt.json')).open('xb') as f:f.write(json.dumps(rec,ensure_ascii=False,indent=2).encode())
print(json.dumps(rec,ensure_ascii=False));print(r.stdout.decode('utf-8'));print(r.stderr.decode('utf-8'))
