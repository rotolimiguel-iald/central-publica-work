from pathlib import Path
import datetime,json,os,subprocess
R=Path(__file__).resolve().parent;CHAT=R.parent.parent
pat='regularFlowAbsorptionUnitary|regularFlowField|regularUnitary_shift_conjugate|regular_unitary_positive_generator|operatorFieldLift_star'
queries=[('kernel',['rg','-n',pat,str(R/'k/TGLExt'),'-g','*.lean']),('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),('tree',['rg','-n',pat+'|gerador|traço',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150'])]
def put(p,b):
 assert p.is_relative_to(R) and not p.exists(),p
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
D=R/'search_absorption';D.mkdir(exist_ok=False);rows=[]
for label,cmd in queries:
 p=subprocess.run(cmd,capture_output=True);put(D/(label+'.stdout.txt'),p.stdout);put(D/(label+'.stderr.txt'),p.stderr)
 rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout_bytes=len(p.stdout),stderr_bytes=len(p.stderr)));print(label,p.returncode,len(p.stdout),flush=True)
put(R/'BUSCAS_A1B_ABSORCAO_REGULAR.json',json.dumps(dict(timestamp=datetime.datetime.now().astimezone().isoformat(),searches=rows),ensure_ascii=False,indent=2).encode('utf8'))
