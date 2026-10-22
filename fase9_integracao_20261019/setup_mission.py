"""Anchor the five user requirements; all implementation stays in this copy."""
from pathlib import Path
import json,sys,subprocess,hashlib,uuid
ROOT=Path(__file__).resolve().parent
UNIT='F3.INTEGRACAO_20261019'
ACTOR={'id':'codex-gerente-tgl','kind':'agent'}
REF=str(ROOT/'SESSION_REFERENCE.json')
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest()}
def save(n,v):
 with (ROOT/n).open('xb') as f:f.write((v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)).encode('utf-8'))
def shell(n,args):
 r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8');save(n,{'cmd':args,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 if r.returncode:raise RuntimeError(r.stdout+r.stderr)
 return json.loads(r.stdout)
def call(n,request,mission=True):
 cli=r'C:\IALD\MEMORIA_IALD\mission_cli.py' if mission else r'C:\IALD\MEMORIA_IALD\session_memory.py'
 r=subprocess.run([sys.executable,'-B','-X','utf8',cli],input=json.dumps(request),capture_output=True,text=True,encoding='utf-8')
 save(n,{'request':request,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr});j=json.loads(r.stdout)
 if r.returncode or not j.get('ok'):raise RuntimeError(j)
 return j['result']
if __name__=='__main__':
 objective='''1. Sistemáticas compartilhadas: completar ou limitar as correlações SN/Pantheon/âncoras e conferir os mapas físicos dos observáveis. A caixa atual não cobre todas essas dependências.
2. Execução física: ligar o fornecedor cosmológico real. O cálculo contra o fundo livre ainda usa uma simulação simplificada, suficiente para testar o código, mas insuficiente para discriminar os modelos físicos.
3. Incerteza cosmológica: beta fixo não elimina a incerteza dos parâmetros usados em K. Precisamos propagá-la corretamente ou manter a conclusão explicitamente condicional.
4. Significância estatística: qualificar a distribuição do escore e a multiplicidade. Uma raiz de diferença de ajustes não é automaticamente um sigma de cauda.
5. Integração operacional: consumir as admissões pinadas, estabelecer recusa por falta de convergência numérica e cumprir os atos pendentes antes de congelar e abrir.'''
 save('OPERADOR_OBJETIVO.txt',objective)
 save('UNIT.json',[{'id':UNIT,'frente':'F3','titulo':'Integração Fase9: sistemáticas, fornecedor físico, calibração e admissões','dono':ACTOR['id'],'status':'PRONTA','gate':'Cópias e qualificação sintética; dados observados/congelamento/d72 exigem atos próprios','criterio_de_fechado':objective,'ordem_fonte':str(ROOT/'OPERADOR_OBJETIVO.txt'),'reaproveitamento':r'work\fase9_auditoria_20261019\DELIVERY_R1.json; F3.1/F3.2 E1; ORDEM018 covariance/theta/verdict'}])
 shell('NEW.json',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','nova','--json',str(ROOT/'UNIT.json'),'--quem',ACTOR['id']])
 shell('CLAIM.json',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','reivindicar',UNIT,'--quem',ACTOR['id'],'--nota','Continuação da meta explícita: implementar cinco requisitos em work/fase9_integracao_20261019; reutilizar auditoriaF3. Memória prevista TGL_ATLAS.md,TGL_INDICE_VIVO.md,DIARIO_CONSTRUCAO_QG.md com backups. Nenhum original/freeze/observado/d72.'])
 call('INIT.json',{'operation':'init','objective_file':str(ROOT/'OPERADOR_OBJETIVO.txt'),'objective_sha256':pin(ROOT/'OPERADOR_OBJETIVO.txt')['sha256'],'request_id':str(uuid.uuid4()),'scope':{'house':'IALD','principal':'luiz-antonio-rotoli-miguel'},'actor':ACTOR,'write_reference':REF,'constraints':{'unit':UNIT,'no_observed_opening':True,'no_freeze':True,'no_production_change':True,'no_parameter_tuning':True,'immutable_previous_artifacts':True}},False)
 requirements=[{'id':'R'+str(i),'criterion':line[3:],'depends_on':[]} for i,line in enumerate(objective.splitlines(),1)]
 call('CONFIGURE.json',{'operation':'configure','reference':REF,'actor':ACTOR,'expected_revision':0,'event_id':'configure-five-requirements','requirements':requirements,'sources':[pin(ROOT/'OPERADOR_OBJETIVO.txt')]})
 for task in ['R1','R2','R3','R4','R5']:
  p=call('PROJECT_BEFORE_'+task+'.json',{'operation':'project','reference':REF})
  call('CLAIM_'+task+'.json',{'operation':'claim','reference':REF,'actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'event_id':'claim-'+task.lower(),'task_id':task,'lease_seconds':43200})
 p=call('PROJECT_READY.json',{'operation':'project','reference':REF})
 save('HANDOFF.json',{'reference':REF,'unit':UNIT,'actor':ACTOR,'projection':p})
 print(json.dumps({'unit':UNIT,'reference':REF,'revision':p['receipt']['revision']},ensure_ascii=False))
