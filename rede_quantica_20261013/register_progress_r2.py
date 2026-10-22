"""Record one material milestone with durable intent; never repeat uncertain mutations."""
import datetime as dt
import json
import subprocess
import sys
import time
from diary_r1 import OUT, WORK, PY, CLI, WHO, claim, new, pin

def run(name, args, payload=None):
    path = OUT/'diary_events'/name
    if path.exists() or path.with_name(path.name+'.intent.json').exists():
        raise FileExistsError(path)
    command=[PY,'-B','-X','utf8',*args]
    new(path.with_name(path.name+'.intent.json'), {'command':command,'payload':payload,'at_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    start=dt.datetime.now(dt.timezone.utc); clock=time.perf_counter()
    cp=subprocess.run(command,input=None if payload is None else json.dumps(payload,ensure_ascii=False),capture_output=True,text=True,encoding='utf-8')
    result={'command':command,'start_utc':start.isoformat(),'end_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'seconds':time.perf_counter()-clock,'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr}
    new(path,result)
    if cp.returncode:raise RuntimeError(result)
    value=json.loads(cp.stdout)
    if value.get('ok') is False:raise RuntimeError(value)
    print(json.dumps({'receipt':str(path),'ok':True,'result':value.get('result',value) if name.startswith('BOARD') else 'recorded'},ensure_ascii=False))

def src(path):
    item=pin(path)
    return {'kind':'artifact','ref':item['path'],'sha256':item['sha256']}

if __name__=='__main__':
    claim()
    mode=sys.argv[1]
    snapshot=OUT/'diary_events/start-r2-20261013_DIARIO_SNAPSHOT.md'
    if mode=='board':
        run('BOARD_CONTINUATION_R2.json',[CLI,'avancar','F1.REDE','--quem',WHO,'--status','EM_CURSO','--evidencia',str(snapshot),str(OUT/'diary_events/start-r2-20261013_RECEIPT.json'),'--nota','Continuidade expressa do operador, diario criado com retrospectiva conferida; identificacao geometrica de J e primeiro setor bosonico concreto. Entrega R1 intacta.'])
    elif mode=='acom':
        payload={'operation':'transition','reference':str(WORK/'ACOM_REFERENCE.json'),'expected_revision':2,'event_id':'f1-rede-diary-continuation-r2-20261013','actor':{'id':WHO,'kind':'agent'},'changes':{
          'records':[{'id':'diary-continuation-r2','kind':'fact','statute':'REAL','text':'Diário solicitado pelo operador criado em memory/DIARIO_CONSTRUCAO_QG.md, com retrospectiva por evidências. Atlas, índice e aviso receberam remissão com backups de bytes sob reivindicação747. A continuação em sandbox aborda identificação geométrica de J e setor bosônico simétrico no mesmoH1; certificados conjuntos aindaOPEN.','sources':[src(WORK/'OPERADOR_DIARIO_CONTINUIDADE_20261013.txt'),src(snapshot),src(OUT/'diary_events/start-r2-20261013_RECEIPT.json')]}],
          'flow':{'phase':'geometric_and_fock_construction','next_action':'Concluir identificação geométrica de J e setor de duas partículas; revisar e registrar cada avanço no diário, mapa e quadro. Nenhum provedor repetido.','handles':[{'id':'f1-rede-deepseek','request_id':'701e5bcb-cb47-4706-a9be-9b5ed10f4a35','job_id':'4d57aa1f-2d40-43df-8f82-f16593d899a2','execution_task_id':'69dd527b-cf74-4b4d-9a15-0c51b8d191bd','provider':'deepseek','status':'completed_no_repeat','unit':'F1.REDE'}]}}}
        run('ACOM_CONTINUATION_R2.json',[r'C:\IALD\MEMORIA_IALD\session_memory.py'],payload)
    else:raise ValueError(mode)
