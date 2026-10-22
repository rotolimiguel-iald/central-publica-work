from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'TETELESTAI_V351_FECHO_MATEMATICO'/'RETOMADA_A1B_012'/'k'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
source=(ROOT/sys.argv[1]).resolve()
assert source.is_relative_to(ROOT) and source.suffix=='.lean'
attempt=ROOT/'attempts'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
attempt.mkdir(parents=True)
env=os.environ.copy()
env.pop('LEAN_PATH',None);env.pop('LEAN_SRC_PATH',None)
env['PATH']=str(BIN)+os.pathsep+env['PATH']
packages=sorted(p for p in (BASE/'.lake/packages').iterdir() if (p/'.git').exists())
env['GIT_CONFIG_COUNT']=str(len(packages))
for i,p in enumerate(packages):
    env[f'GIT_CONFIG_KEY_{i}']='safe.directory'
    env[f'GIT_CONFIG_VALUE_{i}']=str(p)
before=source.read_bytes()
command=[str(BIN/'lake.exe'),'env','lean','--root',str(ROOT),str(source)]
print(attempt,flush=True)
with (attempt/'stdout.txt').open('wb') as out,(attempt/'stderr.txt').open('wb') as err:
    result=subprocess.run(command,cwd=BASE,env=env,stdout=out,stderr=err)
record={'source':str(source),'sha256':hashlib.sha256(before).hexdigest(),
        'source_unchanged':source.read_bytes()==before,'command':command,
        'returncode':result.returncode,'dependency_cache':str(BASE),
        'note':'New source elaborated by Lean; existing imported dependency objects reused.'}
(attempt/'run.json').write_text(json.dumps(record,indent=2),encoding='utf8')
print((attempt/'stdout.txt').read_text(encoding='utf8'))
print((attempt/'stderr.txt').read_text(encoding='utf8'))
sys.exit(result.returncode if record['source_unchanged'] else 9)
