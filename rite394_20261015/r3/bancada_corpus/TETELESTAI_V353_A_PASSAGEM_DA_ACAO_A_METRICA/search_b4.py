from pathlib import Path
import subprocess, json, os, datetime
R=Path(__file__).resolve().parent;P=R.parent
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True)
    q=p.with_name(p.name+'.tmp');q.write_bytes(b)
    assert q.read_bytes()==b;os.replace(q,p)
pattern=r'Phi_flux|Hubble.*horizon|horizon.*Hubble|Cai.Kim|constant.w|two_routes|variance|Clausius|clausius'
jobs=[
 ('01_kernel',['rg','-n',pattern,str(R/'kernel'),'-g','*.lean','-g','!**/.lake/**']),
 ('02_notes',['rg','-n',pattern,str(P/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*','-g','!**/r/**','-g','!**/revisao/**']),
 ('03_deliveries',['rg','-n',pattern,str(P/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('03_workbenches',['rg','-l',pattern,str(P),'-g','*.lean','-g','!**/.lake/**','-g','!**/attempts/**','-g','!**/revisao/**','-g','!**/DEPENDENCIAS_CE*/**','-g','!*.bak*']),
 ('04_tree',['rg','-n',pattern+'|Einstein|Clausius',str(R/'inputs/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('05_toe',['rg','-n',pattern,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('06_acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py','Cai.Kim|friedmann2_TGL|Phi_flux','--max','25','--ctx','140']),
]
records=[]
for label,cmd in jobs:
    p=subprocess.run(cmd,capture_output=True)
    put(R/'searches_B4'/f'{label}.stdout.txt',p.stdout)
    put(R/'searches_B4'/f'{label}.stderr.txt',p.stderr)
    records.append(dict(label=label,command=cmd,returncode=p.returncode,stdout_bytes=len(p.stdout),stderr_bytes=len(p.stderr)))
    print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(R/'BUSCAS_B4.json',json.dumps(dict(timestamp=datetime.datetime.now().astimezone().isoformat(),searches=records),ensure_ascii=False,indent=2).encode('utf8'))
