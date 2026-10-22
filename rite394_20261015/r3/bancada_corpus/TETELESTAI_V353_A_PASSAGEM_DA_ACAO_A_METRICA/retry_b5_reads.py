from pathlib import Path
import subprocess,json,os,datetime
R=Path(__file__).resolve().parent
records=[]
for job in json.loads((R/'BUSCAS_B5.json').read_text(encoding='utf8'))['searches']:
    if job['label'] not in ['05_toe','06_acervo']:continue
    proc=subprocess.run(job['command'],capture_output=True)
    for suffix,data in [('stdout',proc.stdout),('stderr',proc.stderr)]:
        p=R/'searches_B5'/(job['label']+'_retry.'+suffix+'.txt')
        assert not p.exists();q=p.with_name(p.name+'.tmp');q.write_bytes(data)
        assert q.read_bytes()==data;os.replace(q,p)
    records.append(dict(label=job['label'],command=job['command'],returncode=proc.returncode,
        stdout_bytes=len(proc.stdout),stderr_bytes=len(proc.stderr)))
    print(job['label'],proc.returncode,len(proc.stdout),len(proc.stderr),flush=True)
p=R/'BUSCAS_B5_RETRY.json';assert not p.exists()
b=json.dumps(dict(timestamp=datetime.datetime.now().astimezone().isoformat(),searches=records),ensure_ascii=False,indent=2).encode('utf8')
q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
