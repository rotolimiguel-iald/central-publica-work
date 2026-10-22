"""Explicit index refresh with immediate byte backups for BOTH derived files."""
from pathlib import Path
import datetime as dt, hashlib, json, subprocess
NOS=Path(r'C:\IALD\NOS_VIVO')
OUT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REDE')
stamp=dt.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
rec={'start':dt.datetime.now(dt.timezone.utc).isoformat(),'backups':[]}
for n in ['NOS_VIVO.md','nos_vivo.sqlite3']:
 p=NOS/n;b=p.read_bytes();bk=NOS/(n+'.bak_'+stamp+'_F1_REDE')
 with bk.open('xb') as f:f.write(b)
 assert bk.read_bytes()==b
 rec['backups'].append(pin(bk))
def run(args):
 c=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',*args],capture_output=True,text=True,encoding='utf-8')
 return {'args':args,'exit_code':c.returncode,'stdout':c.stdout,'stderr':c.stderr}
rec['build']=run([str(NOS/'construir.py')])
with (OUT/'NOS_BUILD_RECEIPT_R1.json').open('x',encoding='utf-8') as f:json.dump(rec,f,ensure_ascii=False,indent=2)
if rec['build']['exit_code']:raise RuntimeError(rec['build'])
for name,args in [('NOS_CONSULTA_R1.json',['--unidade','F1.REDE']),('NOS_PACOTE_R1.json',['--pacote','F1.REDE','--max','9000'])]:
 c=run([str(NOS/'consultar.py'),*args])
 with (OUT/name).open('x',encoding='utf-8') as f:json.dump(c,f,ensure_ascii=False,indent=2)
 if c['exit_code']:raise RuntimeError(c)
print(json.dumps({'build_exit':rec['build']['exit_code'],'unit':'F1.REDE','consultation':'PASS','backups':[x['path'] for x in rec['backups']]},ensure_ascii=False))
