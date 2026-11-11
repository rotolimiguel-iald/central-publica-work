"""Record this completed synthetic stage; leave physical covariance explicitly open."""
import json,hashlib,subprocess
from pathlib import Path
from start_mission import BASE,REF,PY,ACTOR,call,save

def source(name):
    p=BASE/name
    return {'kind':'artifact','ref':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

p=call('project',max_chars=50000)
t=next(t for t in p['projection']['active'] if t['id']=='h0dn_bg1')
pre=call('check',actor=ACTOR,expected_revision=p['receipt']['revision'],projection_sha256=p['projection_sha256'],task_id=t['id'],lease_id=t['lease']['id'])
save('PREFLIGHT_DELIVERY.json',pre)
records=[
 {'id':'h0dn-bg1-computational-06nov','kind':'fact','statute':'REAL',
  'text':'C publicada255x255 rank183 e bloco BG1 3x3 montados;100000 injeções por hipótese e100000 importance por ajuste. Rótulos abertos após64escores pinados. D prospectivo6.823355/5.316944 e poderMC96.609%/62.485%, baseline/viésCefeidas livre. Simulação condicional, nenhum ajuste observado. Covariância física completa permanece OPEN por ausência de agregação/decomposição entre degraus. Resultado não altera gate.',
  'sources':[source('ENTREGA_H0DN_BG1.json')]},
 {'id':'afixacao-input-06nov','kind':'fact','statute':'INPUT',
  'text':(BASE/'OPERADOR_AFIXACAO.txt').read_text('utf-8').strip(),'sources':[source('OPERADOR_AFIXACAO.txt')]},
 {'id':'afixacao-instrument-open-06nov','kind':'candidate','statute':'DECLARADO',
  'text':'Interpretação candidata: travessia no próprio ato de leitura, sem exigir evento anterior; explicitar instrumento e variável de registro que realizam afixação. JKJ=-K e J²=I preservam escopo e tipos; não determinam sozinhos canal irreversível, tempo físico ou contagens.',
  'sources':[source('background/AFIXACAO_NOTA.md')]}]
req={'operation':'transition','reference':REF,'actor':ACTOR,'expected_revision':p['receipt']['revision'],
     'event_id':'h0dn-bg1-synthetic-stage-06nov','changes':{'records':records,
     'flow':{'phase':'synthetic_stage_delivered_physical_covariance_open',
             'next_action':'Reconstituir operador de agregação e covariância SN-only/host/PV, depois congelar ensaio completo. Afixação: definir instrumento de leitura e registro.',
             'handles':[{'id':'h0dn-bg1-blind-custody-06nov','status':'completed','source':str(BASE/'blind_custodian/SCORES_COMMIT.json'),'recorded_after_completion':True}]}}}
r=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\session_memory.py'],input=json.dumps(req,ensure_ascii=False),text=True,encoding='utf-8',capture_output=True)
d=json.loads(r.stdout)
if not d.get('ok'):raise RuntimeError(d)
save('ACOM_STAGE_RECEIPT.json',d)
p=call('project',max_chars=50000);t=next(t for t in p['projection']['active'] if t['id']=='h0dn_bg1')
ev=BASE/'ENTREGA_H0DN_BG1.json'
r=call('submit',actor=ACTOR,expected_revision=p['receipt']['revision'],projection_sha256=p['projection_sha256'],
       event_id='h0dn-bg1-submit-stage-06nov',task_id=t['id'],lease_id=t['lease']['id'],
       evidence=[{'path':str(ev),'sha256':hashlib.sha256(ev.read_bytes()).hexdigest()}])
save('MISSION_STAGE_SUBMIT.json',r)
print(json.dumps({'acom_receipt':d.get('result',{}).get('revision'), 'submit':r},ensure_ascii=False))
