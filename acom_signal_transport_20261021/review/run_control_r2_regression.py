from pathlib import Path
import os,runpy,sys,json
root=Path(__file__).resolve().parent/'t';p=root/'p'
def offline(event,args):
    if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen'):raise RuntimeError('OFFLINE_ONLY')
    if event=='open':
        path,mode,flags=args
        if isinstance(path,(str,bytes)) and ((mode and any(c in mode for c in 'wax+')) or flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT)):
            if not Path(path).resolve().is_relative_to(root):raise RuntimeError('REVIEW_WRITES_ONLY')
sys.addaudithook(offline);sys.path.insert(0,str(p))
runpy.run_path(str(p/'test_recovery.py'),run_name='__main__')
# Execute only the existing 55 regressions before the benchmark fixture section.
test=p/'test_benchmark.py';source=test.read_text(encoding='utf-8')
prefix=source.split('# Synthetic fixtures:')[0]
namespace={'__file__':str(test),'__name__':'__review_regressions__'}
exec(compile(prefix,str(test),'exec'),namespace)
namespace['store'].close()
print(json.dumps({'prior_regressions':len(namespace['checks']),'all_passed':all(namespace['checks'].values()),'benchmark_executed':False}))
