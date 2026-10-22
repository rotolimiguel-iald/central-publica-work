from pathlib import Path
import datetime,json,os,subprocess
R=Path(__file__).resolve().parent
pattern='scalarTomitaImaginaryPower_left|matrixUnit_imaginaryPower_left|scalarTomitaImaginaryPower_regular_left|matrixUnit_polar_left_weighted|regular_dual_weight_modular_implementation'
cmd=[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pattern,'--max','25','--ctx','160']
p=subprocess.run(cmd,capture_output=True)
for name,b in [('06_acervo_refined.stdout.txt',p.stdout),('06_acervo_refined.stderr.txt',p.stderr)]:
 q=R/'search_left'/name;assert not q.exists();t=q.with_name(q.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,q)
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),command=cmd,returncode=p.returncode,stdout_bytes=len(p.stdout),stderr_bytes=len(p.stderr),reason='Prior unbounded Imaginary.*Left regex matched long serialized package lists, not a left-transport theorem')
q=R/'BUSCA_A1B_ACERVO_REFINADA.json';assert not q.exists();b=json.dumps(d,ensure_ascii=False,indent=2).encode('utf8');t=q.with_name(q.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,q)
print(json.dumps(d,ensure_ascii=False));print(p.stdout.decode('utf8')[:10000]);print(p.stderr.decode('utf8'))
