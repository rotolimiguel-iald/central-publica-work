from pathlib import Path
import datetime,json,os,subprocess
R=Path(__file__).resolve().parent;CHAT=R.parent.parent
pattern=r'scalarTomitaImaginaryPower.*left|imaginaryPower.*left|Imaginary.*Left|matrixUnit_polar_left_weighted|regular_dual_weight_modular_implementation'
commands=[('01_kernel',['rg','-n',pattern,str(R/'k'),'-g','*.lean','-g','!**/.lake/**']),
 ('02_notes',['rg','-n',pattern,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('03_deliveries',['rg','-n',pattern,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('03_other_workbenches',['rg','-l',pattern,str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!**/attempts/**','-g','!*.bak*']),
 ('04_tree',['rg','-n',pattern+'|traço|peso dual|Tomita',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('05_toe',['rg','-n',pattern,str(Path(r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada')),'-g','*.lean','-g','!**/.lake/**']),
 ('06_acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pattern,'--max','25','--ctx','120'])]
def put(p,b):
 assert not p.exists(),p
 q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
D=R/'search_left';D.mkdir(exist_ok=False);rows=[]
for name,cmd in commands:
 p=subprocess.run(cmd,capture_output=True)
 put(D/(name+'.stdout.txt'),p.stdout);put(D/(name+'.stderr.txt'),p.stderr)
 rows.append(dict(label=name,command=cmd,returncode=p.returncode,stdout_bytes=len(p.stdout),stderr_bytes=len(p.stderr)))
 print(name,p.returncode,len(p.stdout),flush=True)
put(R/'BUSCAS_A1B_ESQUERDA.json',json.dumps(dict(timestamp=datetime.datetime.now().astimezone().isoformat(),searches=rows),ensure_ascii=False,indent=2).encode('utf8'))
