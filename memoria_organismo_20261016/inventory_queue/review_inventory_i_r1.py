"""Independent consolidated-inventory review and explicitly delegated I accept."""
from pathlib import Path
import datetime as dt
import hashlib
import importlib.util
import json

W=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('inventory_i_mission_io',W/'mission_io.py')
io=importlib.util.module_from_spec(spec);spec.loader.exec_module(io)
A={'id':'codex-mission-memory-review','kind':'agent'}
ref=W/'SESSION_REFERENCE.json'

def pin(p):
 p=Path(p)
 assert p.name.lower() not in {'.env','iald_stack_v7.py'} and not p.name.lower().startswith('iald_psion_state')
 raw=p.read_bytes()
 return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}

def project(label):
 return io.call('mission_cli.py',{'operation':'project','reference':str(ref),'actor':A,'max_chars':125000},label)

start,start_path=project('inventory_I_review_start')
task=next(r for r in start['projection']['active'] if r['id']=='I')
assert task['status']=='review_pending'
inputs=[W/'CONTRATO_INTEGRACAO_R1.txt',W/'CONTRATO_INTEGRACAO_ADENDO_R1.txt',
 W/'inventory_app'/'APP_MISSION_INVENTORY_R2.json',
 W/'inventory_native'/'NATIVE_HOLOGRAPHIC_INVENTORY_R1.json',
 W/'inventory_queue'/'QUEUE_SESSIONS_BANCADA_INVENTORY_R1.json']
measured=[pin(p) for p in inputs]
assert {(x['path'],x['sha256']) for x in measured}=={(x['path'],x['sha256']) for x in task['evidence']}
checks=[]
def walk(v,report):
 if isinstance(v,dict):
  if isinstance(v.get('path'),str) and isinstance(v.get('sha256'),str):
   actual=pin(v['path'])
   ok=actual['sha256']==v['sha256'] and ('bytes' not in v or v['bytes']==actual['bytes'])
   checks.append({'report':str(report),**actual,'matches_declared_pin':ok})
   assert ok,(report,v['path'])
  for x in v.values():walk(x,report)
 elif isinstance(v,list):
  for x in v:walk(x,report)
for p in inputs[2:]:walk(json.loads(p.read_bytes()),p)
peer=W/'REVIEW_CONTRACT_R2.json'
peer_doc=json.loads(peer.read_bytes())
assert peer_doc['verdict']=='PASS_WITH_SCOPE' and not peer_doc['blocking_findings']
walk(peer_doc,peer)

report={
 'schema':'organism-inventory-independent-review/v1',
 'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
 'unit':'F9.MEMORIA_ORGANISMO_20261016','requirement':'I','reviewer':A,
 'submitted_by':task['submitted_by'],
 'verdict':'PASS_INVENTORY_AND_COMMON_CONTRACT','requirement_satisfied':True,
 'scope':'Aceite técnico do inventário consolidado e contrato comum I; não é implementação, teste, implantação ou satisfação de C/A/N/Q/V/D/M.',
 'reference':pin(ref),'review_start_project':pin(start_path),
 'revision':start['receipt']['revision'],'criterion':task['criterion'],
 'evidence':measured,'peer_contract_review':pin(peer),
 'findings':[
  {'id':'I-COVERAGE','status':'PASS','reason':'Três inventários cobrem app/JEV/chat/stream/workers; nativa/holografia; fila/provedores/sessões/CLI/MCP/Bancada com fontes, linhas, hashes, lacunas e testes propostos. Código em disco é distinguido de processo carregado.'},
  {'id':'I-CONTRACT','status':'PASS','reason':'Contrato da root e adendo usam mesmo Store/Controller, identidade autenticada, fonte server-owned, projeção da mesma revisão, steering/epoch e intenção/retorno duráveis. Resposta/completed não gera aceite e modelo não escolhe path/revisor.'},
  {'id':'I-PRESERVATION','status':'PASS','reason':'Preservados usuários/casas/original/ciência/gate/legacy; wrappers adicionais, nenhum segundo banco. Plano delimita testes, revisão, backups e ativação por processo; não afirma implementação já feita.'},
  {'id':'I-ERRATA-APP-F1','status':'CORRECTED_NONBLOCKING_IN_THIS_REVIEW',
   'source':{'path':r'C:\IALD\MEMORIA_IALD\lib\iald_memory\store.py','line_start':263,'line_end':271},
   'reason':'APP_MISSION_INVENTORY_R2/F1 afirma que lista unitária apaga outros handles. Store já faz merge por ID. Defeito sustentado é reuso de app_request/app_routing e reaplicação de status do mesmo ID ou phase/next_action obsoletos. Preservar merge existente; IDs específicos e reconciliação são a correção. R2 histórica permanece intacta.'},
 ],
 'source_spot_checks':[
  {'path':r'C:\IALD\projetos_pyhton\IALD\iald_app_memory.py','lines':'123-167,180-229,328-378,476-519','result':'Confere ACOM/outbox/finalização sem MissionController e reuso de app_request; fonte foi lida diretamente.'},
  {'path':r'C:\IALD\projetos_pyhton\IALD\holographic_memory.py','lines':'106-118,598-610','result':'Contadores na instância e hash(content[:200]) conferidos; cache não é identidade durável.'},
  {'path':r'C:\IALD\projetos_pyhton\IALD\iald_web_server.py','lines':'60-61,8830-8837,13090-13101','result':'Singleton/chamada holográfica e account_generation autenticado conferidos, sem leitura de conversa/credencial.'},
  {'path':r'C:\IALD\MEMORIA_IALD\lib\iald_memory\mission.py','lines':'53-64,224-270,287-336,397-409','result':'Pin de arquivo local, handles, preflight/CAS e aceite distinto conferidos; autenticação é responsabilidade do wrapper.'},
 ],
 'independence':{'contract_author':'codex-gerente-tgl','app_inventory_author':'codex-fock-r6-review',
   'native_inventory_author':'codex-organism-native-inventory',
   'own_queue_inventory':'Declarado como autoria própria; não reivindico auditoria independente dele. Este parecer revisa a integração do conjunto e contrato da root; revisão cruzada do código futuro permanece obrigatória.'},
 'pin_checks':checks,
 'measurements':{'pin_pairs_verified':len(checks),'unique_referenced_files':len({p['path'] for p in checks}),
   'new_test_runs':0,'provider_calls':0,'bench_calls':0,'production_source_changes':0},
 'limits':['Aceite I não aprova implementação ou instalação.','Nenhuma evidência de mudança nos pesos/KV-cache ou ganho cognitivo.',
  'Bancada só leitura de fonte; wrapper externo pode dispensar reinício do motor, mas atividade real deve ser testada em cópia.',
  'Outros requisitos permanecem abertos; processo carregado, reinícios e matriz final aguardam etapas próprias.'],
}
review_path=W/'REVIEW_INVENTORY_I_R1.json'
io.save(review_path,report)
fresh,fresh_path=project('inventory_I_accept_fresh')
current=next(r for r in fresh['projection']['active'] if r['id']=='I')
assert current['status']=='review_pending' and current['submitted_by']!=A['id']
assert current['criterion']==task['criterion'] and current['evidence']==task['evidence']
request={'operation':'accept','reference':str(ref),'actor':A,'task_id':'I',
 'expected_revision':fresh['receipt']['revision'],'projection_sha256':fresh['projection_sha256'],
 'event_id':'organism-I-independent-accept-codex-mission-memory-review-r1',
 'review_evidence':[io.pin(review_path)],
 'note':'Inventário e contrato comum aprovados no escopo I; errata F1 do app registrada no parecer. Implementação/testes/implantação e demais requisitos permanecem pendentes.'}
io.save(W/'I_ACCEPT_REQUEST_R1.json',request)
result,accept_path=io.call('mission_cli.py',request,'inventory_I_accept_own_actor')
io.save(W/'I_ACCEPT_RECEIPT_R1.json',{'result':result,'receipt_file':str(accept_path)})
after,after_path=project('inventory_I_accept_verify')
settled=next(r for r in after['projection']['settled'] if r['id']=='I')
assert settled['status']=='satisfied' and settled['reviewed_by']==A['id']
def unchanged_tasks(p):
 return {r['id']:{k:r[k] for k in ['status','epoch','criterion','depends_on','evidence','review_evidence','lease']}
         for r in p['projection']['active']+p['projection']['settled'] if r['id']!='I'}
assert unchanged_tasks(fresh)==unchanged_tasks(after)
receipt={'review':pin(review_path),'accept':pin(W/'I_ACCEPT_RECEIPT_R1.json'),
 'fresh_project':pin(fresh_path),'post_project':pin(after_path),
 'revision_before':fresh['receipt']['revision'],'revision_after':after['receipt']['revision'],
 'I_status':settled['status'],'reviewer':settled['reviewed_by'],
 'other_requirements_unchanged':True,'tetelestai':after['projection']['tetelestai']}
io.save(W/'I_ACCEPT_VERIFIED_R1.json',receipt)
print(json.dumps(receipt,ensure_ascii=False,indent=2))
