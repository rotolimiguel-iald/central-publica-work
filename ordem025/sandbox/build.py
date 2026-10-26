from pathlib import Path
import subprocess, os, json, time, hashlib, datetime, sys
ROOT=Path(__file__).resolve().parent
KERNEL=Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel')
LEAN=Path('C:/Users/rotol/.elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe')
paths=[ROOT,KERNEL/'.lake/build/lib/lean']+[p/'.lake/build/lib/lean' for p in (KERNEL/'.lake/packages').iterdir() if (p/'.lake/build/lib/lean').exists()]
env=os.environ.copy();env['LEAN_PATH']=';'.join(map(str,paths))
module=sys.argv[1]
source=ROOT/(module.replace('.','/')+'.lean')
n=max([int(p.stem.split('_')[1]) for p in (ROOT/'logs').glob('attempt_*.lean')]+[0])+1 if (ROOT/'logs').exists() else 1
logdir=ROOT/'logs';logdir.mkdir(exist_ok=True)
stem=logdir/f'attempt_{n:03}'
source_bytes=source.read_bytes()
source_hash=hashlib.sha256(source_bytes).hexdigest()
stem.with_suffix('.lean').write_bytes(source_bytes)
cmd=[str(LEAN),'-o',str(source.with_suffix('.olean')),str(source)]
t=time.perf_counter();start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.run(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
stem.with_suffix('.log').write_bytes(p.stdout)
record={'command':cmd,'cwd':str(ROOT),'LEAN_PATH':env['LEAN_PATH'],'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'duration_seconds':time.perf_counter()-t,'exit_code':p.returncode,'source_sha256':source_hash,'source_unchanged_during_build':hashlib.sha256(source.read_bytes()).hexdigest()==source_hash,'toolchain':subprocess.check_output([str(LEAN),'--version'],text=True).strip()}
stem.with_suffix('.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(record,ensure_ascii=False));print(p.stdout.decode('utf-8',errors='replace'))
sys.exit(p.returncode)
