from pathlib import Path
import sys,json,subprocess
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from task import *
B=Path(__file__).resolve().parent
S=B/'ORIGEM.txt'
def write(name,data):
    if not isinstance(data,bytes):data=json.dumps(data,ensure_ascii=False,indent=2).encode('utf8')
    with (B/name).open('xb') as f:f.write(data)
write('EXTEND.json',act('extend',requirements=[{'id':'physical_sources','criterion':'Localizar e conferir fontes autorais de selecao de massa, fonte metrica, fluxo/Clausius/H3; produzir matriz de reuso e ponte derivada apenas no alcance sustentado; nao repetir provas nem alterar originais.','depends_on':[]}],sources=[pin(S)],reason='Continuacao humana explicita apos a entrega ORDEM025.',event_id='o25-physical-sources-extend'))
write('CLAIM.json',act('claim',task_id='physical_sources',lease_seconds=21600,event_id='o25-physical-sources-claim'))
p=project();t=next(x for x in p['projection']['active'] if x['id']=='physical_sources')
write('PREFLIGHT.json',act('check',task_id=t['id'],lease_id=t['lease']['id']))
for name,cmd in [('NOS_QUERY.txt',[r'C:\IALD\NOS_VIVO\consultar.py','--unidade',UNIT]),
                 ('NOS_PACKET.txt',[r'C:\IALD\NOS_VIVO\consultar.py','--pacote',UNIT,'--max','9000']),
                 ('MAP_QUERY.json',[r'C:\IALD\MAPA_DE_ROTAS\rotas.py','consultar','massa.*(espectro|clock|fonte)|sele[cç][aã]o.*massa|Clausius.*(ponte|fonte)|H3.*(fonte|a[cç][aã]o)'])]:
    x=subprocess.run([PY,'-B','-X','utf8',*cmd],capture_output=True)
    assert x.returncode==0,x.stderr
    write(name,x.stdout)
p=project()
write('ANCHOR.json',{'reference':str(REF),'task_id':t['id'],'lease_id':t['lease']['id'],'revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'unit':UNIT,'packet':pin(B/'NOS_PACKET.txt')})
print(json.dumps({'anchor':str(B/'ANCHOR.json'),'revision':p['receipt']['revision'],'packet':pin(B/'NOS_PACKET.txt')},ensure_ascii=False))
