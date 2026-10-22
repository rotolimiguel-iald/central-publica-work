"""Bind the human's specific approval to the unchanged R3 payloads."""
import datetime as dt
import json
import sqlite3
import subprocess
from diary_r1 import ROOT,OUT,WORK,PY,claim,new,pin

D=OUT/'orchestration_r3'
BASE=ROOT/'Chatgpt/IALD_ORQUESTRACAO_20260923'

def capture(name,args,payload=None):
 cp=subprocess.run([PY,'-B','-X','utf8',*map(str,args)],input=None if payload is None else json.dumps(payload,ensure_ascii=False),capture_output=True,text=True,encoding='utf-8')
 try:response=json.loads(cp.stdout)
 except json.JSONDecodeError:response=None
 new(D/name,{'observed_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'command':[str(a) for a in args],'exit_code':cp.returncode,'response':response,'stdout':cp.stdout if response is None else None,'stderr':cp.stderr})
 if cp.returncode:raise RuntimeError(name)
 return response

def main():
 active=claim()
 pending=json.loads((D/'HANDOFF_PENDING_APPROVAL_R3.json').read_text(encoding='utf-8'))
 approval={'questionItemId':'["request_user_input_async","call_537d6c922c8a4a20a56656c130719427",0]','question':'A revisão automática bloqueou o registro do novo pedido MiMo por considerar insuficiente a autorização para este pacote específico de material interno. Autoriza os dois envios únicos da F1.REDE: MiMo (vetores exponenciais; pedido de 20.586 caracteres + contexto canônico de cerca de 909 KB) e DeepSeek (Γ(J); 23.422 caracteres + cerca de 646 KB)? Os pacotes completos estão em F1.REDE\\orchestration_r3\\REQUEST_MIMO_R3_1.json e REQUEST_DEEPSEEK_R3_1.json. São fontes científicas e memória interna TGL, sem credenciais ou acervo jurídico.','answer':'Autorizar os dois envios'}
 new(D/'OPERADOR_AUTORIZACAO_R3_20261014.json',{'source':'Direct human response in this Codex thread','user_date':'2026-10-14','recorded_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'reply_verbatim':approval,'claim':active,'scope':'Only the two named persisted payloads, one execution each, plus required canonical scientific context. Original limits and confidentiality rules remain.','requests':pending['requests']})
 db=sqlite3.connect((BASE/'state/tasks.sqlite3').as_uri()+'?mode=ro',uri=True)
 checks=[]
 for item in pending['requests']:
  p=item['payload'];assert pin(p['path'])==p
  req=json.loads(open(p['path'],encoding='utf-8').read())
  assert req['request_id']==item['request_id']
  assert req['execution_constraints']['branch_id']=='F1.REDE'
  assert req['execution_constraints']['max_calls']==1
  existing={t:[dict(zip(('id','request_id'),r)) for r in db.execute(f'SELECT id,request_id FROM {t} WHERE request_id=?',(req['request_id'],))] for t in ('tasks','coordination_jobs')}
  assert not any(existing.values()), 'Request already exists: recover, never duplicate'
  assert not (D/f'SUBMIT_{item["provider"].upper()}_R3_1_INTENT.json').exists()
  for s in json.loads(open(item['sources']['path'],encoding='utf-8').read())['sources']:
   assert pin(s['path'])['sha256']==s['sha256']
  checks.append({'provider':item['provider'],'request_id':req['request_id'],'payload':p,'existing':existing,'source_hashes_verified':True})
 db.close()
 sync=capture('SCIENTIFIC_MEMORY_APPROVED_20261014.json',[ROOT/'work/scientific_memory_sync_20261013/scientific_memory_sync.py','check'])
 assert 'CURRENT' in json.dumps(sync)
 for item in pending['requests']:
  req=json.loads(open(item['payload']['path'],encoding='utf-8').read())
  assert req['execution_constraints']['memory_generation'] in json.dumps(sync)
  req['operation']='preview_execution'
  result=capture(f'PREVIEW_{item["provider"].upper()}_APPROVED_20261014.json',[BASE/'transport_cli.py'],req)
  assert result['selected']==item['provider']
  assert result['canonical_memory']['generation']==req['execution_constraints']['memory_generation']
 capture('NOS_VIVO_APPROVED_20261014.json',[r'C:\IALD\NOS_VIVO\consultar.py','--unidade','F1.REDE'])
 result={'status':'SPECIFIC_HUMAN_APPROVAL_VERIFIED_READY_FOR_SINGLE_SUBMISSION','authorization':pin(D/'OPERADOR_AUTORIZACAO_R3_20261014.json'),'checks':checks,'scientific_check':pin(D/'SCIENTIFIC_MEMORY_APPROVED_20261014.json'),'supersedes_pending_state_of':pin(D/'HANDOFF_PENDING_APPROVAL_R3.json'),'kimi_takesaki':'Unaffected; no authorization inferred for that unit.','execution_owner':'Existing official coordinator, never parallel dispatch by origin session.'}
 new(D/'PREFLIGHT_APPROVED_20261014.json',result)
 new(BASE/'state/handoffs/F1REDE_R3_OPERATOR_AUTHORIZATION_20261014.json',result)
 print(json.dumps({'status':result['status'],'approval':result['authorization'],'requests':[x['request_id'] for x in checks]},ensure_ascii=False))

if __name__=='__main__':main()
