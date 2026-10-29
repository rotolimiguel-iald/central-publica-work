"""Common local guards for the authorized Adendo H update."""
from pathlib import Path
import json, sys, hashlib, os, time, datetime, subprocess
H=Path(__file__).resolve().parent
W=H.parent
E=W/'adendo_e_v402'
G=W/'adendo_g_v404'
V=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
N=V.parent.parent/'Nós'
S=H/'candidate_v404'
B=H/'baseline_v402'
T=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_022\ADENDO_H')
ORDER=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_022_ADENDO_H_duas_sinteses_adicionais_autorizadas.md')
sys.path[:0]=[str(W),str(E)]
from bootstrap import ACTOR,REF,cli
from record_operator_acceptance import create,read,pin
from manage_v402_data import atomic,save,sha
import mission
def project():return mission.call({'operation':'project','max_chars':450000})
def current(actor=ACTOR):
 p=project();return {'actor':actor,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256']}
def check(task_id='ADENDO_H_V404',actor=ACTOR):
 p=project();t=next(x for x in p['projection']['active'] if x['id']==task_id)
 r=mission.call({'operation':'check',**current(actor),'task_id':task_id,'lease_id':t['lease']['id'],'max_chars':450000});assert r['ready'];return r
def stable_seal():
 r=read(H/'SOURCE_INTAKE.json')
 for name in ('um.py','um_absoluto.json','um_absoluto_selo.json','tgl_kernel_proof_manifest.json','rodada_v404_stdout.txt'):
  assert pin(N/name)==r['files'][name], 'STOP_SOURCE_ADVANCED:'+name
 assert read(N/'um_absoluto_selo.json')['um_version']=='v404'
 return read(N/'um_absoluto_selo.json')
def run_receipt(name,args,cwd=H):
 r=subprocess.run(args,cwd=cwd,capture_output=True,text=True,encoding='utf-8');create(H/name,{'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 assert r.returncode==0,r.stderr[-2500:];return r
def setup():
 assert pin(ORDER)['sha256']=='d012dafc79df543becf7a17133b06640e02f46a66eb7dd94dc82e27c8aa09556'
 if not (H/'MISSION_EXTEND.json').exists():
  req=[{'id':'ADENDO_H_V404','criterion':'Adendo H/G: seis TTS novas autorizadas (horizon/return/einstein PT/EN), demais reutilizadas; sétima unidade ou qualquer outro número alterado exige parada. Comparação integral antes do render único v404; import um somente em cópia isolada. Entrega revista, PUBLIC_DELIVERY_V7.json e depósito; nenhuma publicação pela sessão do vídeo.','depends_on':[]},{'id':'V404_DATA','criterion':'Derivar dados v404 em cópia isolada e comparar integralmente todos os campos/números visíveis com v402; somente contagens/versionamento autorizados por G/H e mudanças do gate18/0; zero outra divergência. Conferir reprodutibilidade/replay/âncoras e preservar originais.','depends_on':[]}]
  create(H/'MISSION_EXTEND.json',mission.call({'operation':'extend',**current(),'event_id':'ordem022-adendo-h-v404-extend','requirements':req,'reason':'Adendo H resolve as duas sínteses adicionais apontadas pelo G.','sources':[{'path':str(ORDER),'sha256':sha(ORDER)}]}))
 if not (H/'MISSION_CLAIM.json').exists():create(H/'MISSION_CLAIM.json',mission.call({'operation':'claim',**current(),'task_id':'ADENDO_H_V404','lease_seconds':43200,'event_id':'ordem022-adendo-h-v404-claim'}))
 create(H/'PREFLIGHT.json',check())
 files={name:pin(N/name) for name in ['um.py','um_absoluto.json','um_absoluto_selo.json','tgl_kernel_proof_manifest.json','rodada_v404_stdout.txt']}
 seal=read(N/'um_absoluto_selo.json');assert seal['um_version']=='v404'
 for name in ['um.py','um_absoluto.json','tgl_kernel_proof_manifest.json']:assert files[name]['sha256']==seal['sha256'][name]
 assert files['um.py']['sha256']==read(G/'SOURCE_INTAKE.json')['program']['sha256']
 create(H/'SOURCE_INTAKE.json',{'files':files,'order':pin(ORDER),'version':seal['um_version'],'timestamp':seal['timestamp'],'baseline_pointer':pin(V.parent/'PUBLIC_DELIVERY_V7.json'),'baseline_manifest':pin(V/'PUBLIC_DELIVERY_V7.json'),'prior_stop':pin(G/'FINAL_STOP_DELIVERY.json')})
 for name,args in [('ROUTE_BEFORE.json',[r'C:\IALD\MAPA_DE_ROTAS\rotas.py','consultar','site.filmes.v7.ordem022','--limite','10']),('NOS_BEFORE.json',[r'C:\IALD\NOS_VIVO\consultar.py','--unidade','F0.FILMES_V7_20261024'])]:run_receipt(name,[sys.executable,'-B','-X','utf8',*args])
 run_receipt('BOARD_ACTIVE.json',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F0.FILMES_V7_20261024','--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ORDER),'--nota','Adendo H resolve a parada G; seis unidades TTS autorizadas, nenhum render antes da comparação integral.'])
 print(json.dumps({'status':'H_PREPARED','source':seal['um_version'],'reference':str(REF)}))
if __name__=='__main__':setup()
