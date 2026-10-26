import argparse,hashlib,json,pathlib,subprocess,time
BASE=pathlib.Path(__file__).resolve().parent
REF=str(BASE/'SESSION_REFERENCE.json');PY=r'C:\Python314\python.exe';CLI=r'C:\IALD\MEMORIA_IALD\mission_cli.py'
def call(p):
 p={'reference':REF,**p}
 r=subprocess.run([PY,'-B','-X','utf8',CLI],input=json.dumps(p,ensure_ascii=False),text=True,encoding='utf-8',capture_output=True)
 d=json.loads(r.stdout)
 if not d.get('ok'):raise RuntimeError(d)
 return d['result']
def project():return call({'operation':'project','max_chars':100000})
def current(actor):
 p=project();return {'actor':{'id':actor,'kind':'agent'},'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256']}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('op');p.add_argument('--task');p.add_argument('--actor',default='codex-video-v7');a=p.parse_args()
 if a.op=='configure':
  snap=call({'operation':'get'})
  src=pathlib.Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_022_os_dois_filmes_v7.md')
  req=[{'id':k,'criterion':v,'depends_on':[]} for k,v in {'A':'Reproveniência e comando único conforme ORDEM 022-A, fonte selada coerente e âncoras verificadas.','B':'Cenas e narrativa contínuas da emergência da gravidade, stdout real, números ancorados, estatutos e limiares da ORDEM 022-B/D.','C':'Execução offline no navegador por recorte Python exato ou porte explicitamente indicado, comparação de âncoras e adulteração recusada.','D':'Narração EN/PT-BR, quatro legendas, timing e loudness conforme ORDEM 022-D.','E':'Exportações e contrato público com hashes, API bg_scene compatível e fallback verificado conforme ORDEM 022-E.'}.items()]
  out=call({'operation':'configure','actor':{'id':a.actor,'kind':'agent'},'expected_revision':snap['revision'],'event_id':'ordem022-configure','requirements':req,'sources':[{'path':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()}]})
 elif a.op=='claim':out=call({'operation':'claim',**current(a.actor),'task_id':a.task,'lease_seconds':43200,'event_id':'ordem022-claim-'+a.task})
 elif a.op in ('check','handoff'):
  pr=project();tasks=pr['projection']['active']+pr['projection']['settled']
  task=tasks[a.task] if isinstance(tasks,dict) else next(t for t in tasks if t['id']==a.task)
  out=call({'operation':a.op,**current(a.actor),'task_id':a.task,'lease_id':task['lease']['id'],'max_chars':100000})
 else:out=project()
 path=BASE/('MISSION_'+a.op+'_'+(a.task or 'all')+'_'+str(time.time_ns())+'.json');path.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'receipt_file':str(path),'keys':list(out),'receipt':out.get('receipt'),'ready':out.get('ready')},ensure_ascii=False))
