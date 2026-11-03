import json
from pathlib import Path
R=Path(r'C:\IALD\projetos_pyhton\IALD');W=Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
fs=json.loads((W/'install_plan.json').read_bytes())['files']
nuc=str(R/'iald_nucleo_fixo.json')
print('n',len(fs),'manifest index',[i for i,r in enumerate(fs) if r['destination']==nuc])
for i in (0,1,2,len(fs)-8,len(fs)-7,len(fs)-6,len(fs)-5,len(fs)-4,len(fs)-3,len(fs)-2,len(fs)-1):
    print(i,fs[i]['destination'].replace(str(R),'R')[:110])
print((W/'review/revisor_sonnet-app-v405-revisor/ls_remote_out.txt').read_text(encoding='utf-8',errors='replace')[:300])
