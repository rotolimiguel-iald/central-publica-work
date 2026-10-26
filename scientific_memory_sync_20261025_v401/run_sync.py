import sys,json,hashlib,subprocess,datetime,os,sqlite3,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).parent
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
H=Path(r'C:\IALD\Central de Patentes\work\scientific_memory_sync_20261013')
REF=r'C:\IALD\MEMORIA_IALD\sessions\01a0ce2b-8c2f-71b0-a9a8-91b17715a569.json'
PY=r'C:\Python314\python.exe';UNIT='F0.3.MEMORIA_CIENTIFICA_SYNC';ACTOR={'id':'codex-coordenadora','kind':'agent'};TASK='scientific-sync-v401'
def sha(z):return hashlib.sha256(z).hexdigest()
def pin(p):
 p=Path(p);z=p.read_bytes();return {'path':str(p),'sha256':sha(z),'bytes':len(z)}
def save(name,obj):
 p=W/name;z=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode();old=p.read_bytes() if p.exists() else None
 if old==z:return
 if old is not None:
  bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));bk.write_bytes(old);assert bk.read_bytes()==old
 t=p.with_name(p.name+'.tmp');t.write_bytes(z);assert t.read_bytes()==z and (p.read_bytes() if p.exists() else None)==old
 os.replace(t,p);assert p.read_bytes()==z
 return obj
def cli(path,args=(),payload=None,out=None):
 r=subprocess.run([PY,'-B','-X','utf8',str(path),*args],input=None if payload is None else json.dumps(payload,ensure_ascii=False),capture_output=True,text=True,encoding='utf-8')
 if r.returncode:raise RuntimeError(str(path)+': '+r.stdout[:1500]+r.stderr[-1000:])
 try:d=json.loads(r.stdout)
 except ValueError:d={'stdout':r.stdout}
 if d.get('ok') is False:raise RuntimeError(str(d))
 if out:save(out,d)
 return d
def proj():return cli(r'C:\IALD\MEMORIA_IALD\mission_cli.py',payload={'operation':'project','reference':REF,'max_chars':1000000})['result']
def action(op,out,**kw):
 q=proj();payload=dict(operation=op,reference=REF,actor=ACTOR,expected_revision=q['receipt']['revision'],projection_sha256=q['projection_sha256'],event_id='scientific-sync-v401-'+op+'-20261025',**kw)
 return cli(r'C:\IALD\MEMORIA_IALD\mission_cli.py',payload=payload,out=out)
def preflight(out):
 lease=json.loads((W/'MISSION_CLAIM.json').read_bytes())['result']['task']['lease']['id'];q=proj()
 d=cli(r'C:\IALD\MEMORIA_IALD\mission_cli.py',payload=dict(operation='check',reference=REF,actor=ACTOR,expected_revision=q['receipt']['revision'],projection_sha256=q['projection_sha256'],task_id=TASK,lease_id=lease),out=out)
 assert d['result']['ready'];return d
spec=importlib.util.spec_from_file_location('scientific_sync',H/'scientific_memory_sync.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);SYNC=mod.ScientificMemorySync(work=W)
def queuepins():
 with sqlite3.connect((B/'state/tasks.sqlite3').as_uri()+'?mode=ro',uri=True) as c:
  return {table:{'count':len(rows),'sha256':sha(json.dumps(rows,ensure_ascii=False,default=str).encode())} for table in ('coordination_jobs','tasks') for rows in [c.execute('SELECT * FROM '+table+' ORDER BY rowid').fetchall()]}
def releases():return [pin(p) for p in sorted(SYNC.cm.RELEASES.glob('*/manifest.json'))]
def prepare():
 cli(r'C:\IALD\NOS_VIVO\consultar.py',['--unidade',UNIT],out='NOS_BEFORE.json')
 cli(r'C:\IALD\MAPA_DE_ROTAS\rotas.py',['consultar','iald.ordem019.f0_3.memoria_v391'],out='MAP_BEFORE.json')
 cli(r'C:\IALD\PROGRAMA_IALD\iald.py',['reivindicar',UNIT,'--quem',ACTOR['id'],'--nota','Avanco selado v401; snapshot documental com revisao independente e API baseline/CAS.'],out='BOARD_CLAIM.json')
 # Confirm deployed helper and API against the audited delivery and last verified preparation.
 dep=json.loads((H/'DEPLOYMENT_R2.json').read_bytes())
 prior=json.loads(Path(r'C:\IALD\Central de Patentes\work\scientific_memory_sync_20261024_v400\REVIEW_R1.json').read_bytes())
 for key in ('current_module','current_module_deployment','current_module_review','helper_review'):
  assert pin(prior[key]['path'])==prior[key]
 for x in dep['modules']:
  expected=prior['current_module']['sha256'] if Path(x['path']).name=='canonical_memory.py' else x['sha256']
  assert pin(x['path'])['sha256']==expected
 hp=json.loads((H/'RECIBO_HELPER_R2.json').read_bytes())['files'][0];assert pin(hp['path'])['sha256']==hp['sha256']
 save('REUSED_DEPLOYMENT_PINS.json',{'deployment':pin(H/'DEPLOYMENT_R2.json'),'helper':pin(H/'scientific_memory_sync.py'),'review':prior['helper_review'],'current_module_deployment':prior['current_module_deployment'],'current_module_review':prior['current_module_review'],'modules':[pin(x['path']) for x in dep['modules']]})
 c=SYNC.check();assert c['status']=='SEALED_ADVANCE_PENDING_SYNC' and c['sealed_version']=='v401';save('INITIAL_CHECK.json',c)
 save('QUEUE_PINS_BEFORE.json',queuepins());save('PREVIOUS_RELEASES_BEFORE.json',releases())
 source=H/'OPERADOR_13out_memoria_cientifica_sync_verbatim.txt'
 action('extend','MISSION_EXTEND.json',requirements=[{'id':TASK,'criterion':'Snapshot imutavel v401 das13 fontes: programa/selo/proof, hashes e todos trechos/linhas; revisao independente antes da API baseline/CAS; geracao recebida em processo novo; releases e pedidos preservados; memorias e entrega por versao. Sem executar/importar um.py/Lean, provedores, reinicio ou mudanca de gate.','depends_on':[]}],reason='Avanco selado v401 validado pelo helper; ordem humana permanente de13/10.',sources=[{k:v for k,v in pin(p).items() if k!='bytes'} for p in (source,W/'INITIAL_CHECK.json')])
 action('claim','MISSION_CLAIM.json',task_id=TASK,lease_seconds=43200)
 preflight('PREFLIGHT_R1.json')
 p=SYNC.prepare();save('VERIFY_R1.json',SYNC.verify(p['epoch']))
 assert p['generation']==c['sealed_generation'];assert queuepins()==json.loads((W/'QUEUE_PINS_BEFORE.json').read_bytes())
 # Version-specific append plan: final tense applies only after activation and fresh verification.
 m=p['manifest']['sha256'];g=p['generation'];chunks=p['chunks']
 text=f'\n## 25/10/2026 — Memória científica da fila sincronizada com v401\n<!-- IALD_QUEUE_MEMORY_V401_20261025 -->\n[REAL — empacotamento local] Snapshot imutável v401; generation {g}; manifest SHA256 {m}. Treze documentos e {chunks} trechos conferidos integralmente por hashes, UTF-8 e linhas; recuperação em três modos. Ativação pela API existente com baseline/CAS após revisão independente; geração recebida em processo novo no recibo. v400 e anteriores preservadas; pedidos e gerações fixadas intactos.\n[ESCOPO] Sincronização documental da fila, sem execução/importação de um.py ou Lean, chamada de provedor, reinício, alteração de original científico ou gate. Não afirma atualização do app/JEV nem nova prova. Guardas transitórias programa/selo e selftest ausente preservadas; fontes coerentes admitidas posteriormente. Aprovações específicas e envios terminais/incertos continuam independentes.\n[PROCESSO] Claim do quadro, requisito e preflight ACOM precederam o preparo. Revisão independente documental não reproduz ciência.\n[CONTINUIDADE] CURRENT dispensa reconstrução; helper auditado em processo novo no heartbeat existente. Nunca alterar memory_generation para forçar envio. Recibos: C:/IALD/Central de Patentes/work/scientific_memory_sync_20261025_v401/DELIVERY_R1.json e REVIEW_R1.json.\n'
 old=json.loads(Path(r'C:\IALD\Central de Patentes\work\scientific_memory_sync_20261024_v400\SURFACE_PLAN_R1.json').read_bytes())
 surfaces=[]
 for x in old['surfaces']:
  path=Path(x['path']);z=path.read_bytes();body=text if path.name!='MEMORY.md' else '\n<!-- IALD_QUEUE_MEMORY_V401_20261025 -->\nMemória científica da fila v401: entrega e limites em MEMORY_2.md, adendo25/10/2026; recibo C:/IALD/Central de Patentes/work/scientific_memory_sync_20261025_v401/DELIVERY_R1.json.\n'
  assert 'IALD_QUEUE_MEMORY_V401_20261025' not in z.decode('utf-8-sig')
  surfaces.append({'path':str(path),'baseline_sha256':sha(z),'baseline_bytes':len(z),'append_utf8':body})
 save('SURFACE_PLAN_R1.json',{'status':'NOT_APPLIED_PENDING_INDEPENDENT_REVIEW_AND_ACTIVATION','surfaces':surfaces})
 event={'tipo':'ANOTACAO','rota_id':'iald.ordem019.f0_3.memoria_v391','dominio':'IALD_OPERACIONAL','titulo':'Snapshot cientifico v401 preparado inativo','resultado':f'13 documentos/{chunks} trechos; verificacao integral; revisao independente pendente antes de ativar.','veredito':'PREPARED_INACTIVE','estatuto':'REAL','status':'EM_CURSO','olhou_dados':False,'nao_refazer':'Reutilizar '+p['epoch'],'proximo_passo':'Revisao independente e API baseline/CAS.','artefatos':[str(SYNC.report_path(p['epoch'])),str(W/'VERIFY_R1.json')]}
 save('MAP_PREPARATION.json',event);cli(r'C:\IALD\MAPA_DE_ROTAS\rotas.py',['registrar',str(W/'MAP_PREPARATION.json'),'--quem',ACTOR['id']],out='MAP_PREPARATION_RESULT_R1.json')
 print(json.dumps({'prepared':p['epoch'],'generation':g,'chunks':chunks,'manifest':p['manifest'],'surface_count':len(surfaces)},ensure_ascii=False))

def preparation():return json.loads(next(W.glob('PREPARATION_v401_*.json')).read_bytes())
def receive():
 p=preparation();c=SYNC.check();assert c['status']=='CURRENT' and c['sealed_generation']==p['generation'];receipts={}
 for mode in ('standard','maximum','deepseek_maximum'):
  packet=SYNC.cm.prepare('memoria cientifica estatuto',mode=mode,max_chars=24000)
  assert packet['receipt']['generation']==p['generation'];receipts[mode]=packet['receipt']
 save('RECEIVED_GENERATION_R1.json',{'status':'CURRENT_RECEIVED_FRESH_PROCESS','check':c,'retrieval':receipts,'provider_calls':0,'um_execution':False})
 print('FRESH_PROCESS_CURRENT_RECEIVED',p['generation'])
def activate():
 p=preparation();review=json.loads((W/'REVIEW_R1.json').read_bytes());surface=json.loads((W/'SURFACE_REVIEW_R1.json').read_bytes())
 assert review['status'] in ('PASS','PASS_WITH_SCOPE') and review['epoch']==p['epoch']
 assert surface['status'] in ('PASS','PASS_WITH_SCOPE')
 save('APPROVED_REVIEW_PINS_R1.json',{'review':pin(W/'REVIEW_R1.json'),'surface_review':pin(W/'SURFACE_REVIEW_R1.json'),'surface_plan':pin(W/'SURFACE_PLAN_R1.json')})
 preflight('ACTIVATION_PREFLIGHT_R1.json');save('ACTIVATION_R1.json',SYNC.activate(p['epoch']))
 cli(W/'run_sync.py',['receive'],out='FRESH_PROCESS_COMMAND_R1.json')
 print('ACTIVATED_AND_RECEIVED',p['generation'])
def finish():
 p=preparation();c=SYNC.check();assert c['status']=='CURRENT' and c['sealed_generation']==p['generation']
 approved=json.loads((W/'APPROVED_REVIEW_PINS_R1.json').read_bytes())
 for x in approved.values():assert pin(x['path'])==x
 received=json.loads((W/'RECEIVED_GENERATION_R1.json').read_bytes());assert received['check']['sealed_generation']==p['generation']
 preflight('APPEND_PREFLIGHT_R1.json');plan=json.loads((W/'SURFACE_PLAN_R1.json').read_bytes());pending=[]
 for x in plan['surfaces']:
  path=Path(x['path']);old=path.read_bytes();assert sha(old)==x['baseline_sha256'] and len(old)==x['baseline_bytes'],str(path)
  new=old+x['append_utf8'].encode();assert new.startswith(old)
  if path.name=='MEMORY.md':assert len(new)<=24576
  pending.append((path,old,new))
 applied=[]
 for path,old,new in pending:
  bk=path.with_name(path.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));bk.write_bytes(old);assert bk.read_bytes()==old
  t=path.with_name(path.name+'.tmp_v401');t.write_bytes(new);assert t.read_bytes()==new and path.read_bytes()==old
  os.replace(t,path);assert path.read_bytes()==new
  applied.append({'path':str(path),'backup':str(bk),'before_sha256':sha(old),'after_sha256':sha(new),'before_bytes':len(old),'after_bytes':len(new),'append_verified':True})
 save('MEMORY_APPLIED_R1.json',{'status':'APPENDED_WITH_BYTE_BACKUPS_AND_CAS','surfaces':applied,'count':len(applied)})
 before=json.loads((W/'QUEUE_PINS_BEFORE.json').read_bytes());assert queuepins()==before
 previous=json.loads((W/'PREVIOUS_RELEASES_BEFORE.json').read_bytes())
 for x in previous:assert pin(x['path'])==x
 save('PRESERVATION_R1.json',{'queue_before_after':before,'previous_release_manifests_verified':previous,'active':json.loads(SYNC.cm.ACTIVE.read_bytes()),'provider_calls':0,'um_execution':False,'restarts':False})
 delivery={'status':'ACTIVATED_VERIFIED_NEW_PROCESS','release':'v401','generation':p['generation'],'epoch':p['epoch'],'manifest':p['manifest'],'documents':p['documents'],'chunks':p['chunks'],'activation':str(W/'ACTIVATION_R1.json'),'received':str(W/'RECEIVED_GENERATION_R1.json'),'review':str(W/'REVIEW_R1.json'),'memory_applied':str(W/'MEMORY_APPLIED_R1.json'),'queue_unchanged':before,'previous_release_count':len(previous),'provider_calls':0,'um_execution':False,'restart':False,'scientific_gate_changed':False,'process_scope':'Board claim and ACOM requirement/preflight before preparation; independent snapshot/surface review before activation/append; baseline/CAS; generations and queue preserved. First local guard used old13out module pin and refused before build; current module verified against audited21out deployment and v400 review; no module changed.','preflight':str(W/'PREFLIGHT_R1.json'),'activation_preflight':str(W/'ACTIVATION_PREFLIGHT_R1.json')}
 save('DELIVERY_R1.json',delivery)
 cli(r'C:\IALD\PROGRAMA_IALD\iald.py',['avancar',UNIT,'--quem',ACTOR['id'],'--status','ENTREGUE','--evidencia',str(W/'DELIVERY_R1.json'),str(W/'REVIEW_R1.json'),'--nota','Memoria cientifica v401 ativada via baseline/CAS;13 fontes28323 trechos verificados; geracao recebida em processo novo; anteriores e pedidos preservados.'],out='BOARD_DELIVERY_R1.json')
 event={'tipo':'ANOTACAO','rota_id':'iald.ordem019.f0_3.memoria_v391','dominio':'IALD_OPERACIONAL','titulo':'Memoria cientifica v401 ativada e verificada','resultado':f'13 documentos/{p["chunks"]} trechos; revisao independente, API baseline/CAS, geracao recebida em processo novo; anteriores/pedidos preservados e10 superficies append com backup.','veredito':delivery['status'],'estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,'nao_refazer':'Recuperar '+p['epoch'],'proximo_passo':'Check CURRENT no heartbeat existente; preservar aprovacoes especificas.','artefatos':[str(W/n) for n in ('DELIVERY_R1.json','REVIEW_R1.json','RECEIVED_GENERATION_R1.json','MEMORY_APPLIED_R1.json')]}
 save('MAP_DELIVERY.json',event);cli(r'C:\IALD\MAPA_DE_ROTAS\rotas.py',['registrar',str(W/'MAP_DELIVERY.json'),'--quem',ACTOR['id']],out='MAP_RESULT_R1.json')
 lease=json.loads((W/'MISSION_CLAIM.json').read_bytes())['result']['task']['lease']['id']
 action('submit','SUBMIT_MISSION_R1.json',task_id=TASK,lease_id=lease,evidence=[{k:v for k,v in pin(W/n).items() if k!='bytes'} for n in ('DELIVERY_R1.json','REVIEW_R1.json','SURFACE_PLAN_R1.json','SURFACE_REVIEW_R1.json','MEMORY_APPLIED_R1.json','RECEIVED_GENERATION_R1.json','PRESERVATION_R1.json')],note='Entrega tecnica; aceite semantico por revisor real distinto pendente.')
 q=proj();changes={'records':[{'id':'scientific-sync-v401-delivered-20261025','kind':'fact','statute':'REAL','sources':[{'kind':'artifact','ref':str(W/'DELIVERY_R1.json'),'sha256':pin(W/'DELIVERY_R1.json')['sha256']}],'text':'Memoria cientifica da fila v401 ativada por API baseline/CAS apos revisao independente;13 documentos28323 trechos integrais e geracao recebida em processo novo. Anteriores e pedidos preservados;10 superficies append com backup. Sem um.py/Lean, provedores, reinicio ou mudanca de gate. Aceite do requisito por revisor distinto pendente.'}],'flow':{'phase':'scientific_v401_delivery_review','next_action':'Revisor independente confere entrega e aceita o requisito scientific-sync-v401; checks futuros CURRENT sem reconstruir.'}}
 cli(r'C:\IALD\MEMORIA_IALD\session_memory.py',payload=dict(operation='transition',reference=REF,actor=ACTOR,expected_revision=q['receipt']['revision'],event_id='scientific-sync-v401-delivery-20261025',changes=changes),out='ACOM_DELIVERY_R1.json')
 print('DELIVERED',pin(W/'DELIVERY_R1.json'))

if __name__=='__main__':globals()[sys.argv[1]]()
