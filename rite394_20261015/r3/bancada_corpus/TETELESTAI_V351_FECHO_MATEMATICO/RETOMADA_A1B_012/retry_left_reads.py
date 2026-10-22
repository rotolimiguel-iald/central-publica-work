from pathlib import Path
import datetime,json,os,subprocess
R=Path(__file__).resolve().parent
source=json.loads((R/'BUSCAS_A1B_ESQUERDA.json').read_text(encoding='utf8'))
def put(p,b):
 assert p.is_relative_to(R) and not p.exists()
 q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
rows=[]
for row in source['searches']:
 if row['returncode']!=2:continue
 p=subprocess.run(row['command'],capture_output=True)
 put(R/'search_left'/(row['label']+'.retry.stdout.txt'),p.stdout)
 put(R/'search_left'/(row['label']+'.retry.stderr.txt'),p.stderr)
 rows.append(dict(label=row['label'],command=row['command'],returncode=p.returncode,stdout_bytes=len(p.stdout),stderr_bytes=len(p.stderr)))
 print(row['label'],p.returncode,len(p.stdout),flush=True)
put(R/'BUSCAS_A1B_ESQUERDA_RETRY.json',json.dumps(dict(timestamp=datetime.datetime.now().astimezone().isoformat(),searches=rows),ensure_ascii=False,indent=2).encode('utf8'))
