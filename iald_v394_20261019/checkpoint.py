"""Persist only measured status and real execution handles, preserving the original."""
import hashlib,json
from pathlib import Path
import task
W=task.W
def main():
    snap=task.call({'operation':'get','reference':str(task.REF)},False)
    handles={h['id']:h for h in snap['p'].get('handles',[])}
    updates=[{'id':'app_builder','agent_id':'01a15604-76c6-7110-9a73-2dc692d95018','kind':'delegated_preparation','status':'working'},
       {'id':'sources_review','agent_id':'01a15607-da9a-76e2-a12f-7ce9a5ab4a54','kind':'independent_review','status':'accepted'},
       {'id':'app_foundation_review','agent_id':'01a15607-da9a-76e2-a12f-7ce9a5ab4a54','kind':'independent_review','status':'working'},
       {'id':'queue_preparation_inspection','agent_id':'01a15604-78a6-7a71-9e57-ec5b0dd5c8d3','kind':'delegated_inspection','status':'completed','note':'Sources checked; preparation refused before execution. No uncertain provider call.'},
       {'id':'queue_gate','kind':'operator_decision','status':'awaiting_operator','note':'Explicit approval requested to move F0.3.MEMORIA_CIENTIFICA_SYNC from AGUARDA_OPERADOR to EM_CURSO after concrete auto-review refusal.'},
       {'id':'public_v394','kind':'external_publication','status':'awaiting_external','note':'Custody394 verified; public local/remote Git last observed392. Do not infer URL394.'}]
    handles.update({h['id']:h for h in updates})
    source=W/'queue/DELIVERY_PREPARED.json'
    req={'operation':'transition','reference':str(task.REF),'actor':{'id':task.OWNER,'kind':'agent'},'expected_revision':snap['revision'],'event_id':'v394-preparation-status-checkpoint-r1','changes':{
        'records':[{'id':'queue-explicit-gate-pending','kind':'pending','statute':'OPEN','text':'Fila científica bloqueada antes da preparação: revisão automática recusou AGUARDA_OPERADOR→EM_CURSO da unidade recorrente. Autorização específica perguntada ao humano nesta sessão. App continua em staging; não houve instalação.','sources':[{'kind':'artifact','ref':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}]}],
        'flow':{'phase':'preparing_with_explicit_dependencies','next_action':'Concluir staging/revisão do app, recuperar decisão humana da fila e publicação394; ativar só os artefatos verificados.','handles':list(handles.values())}}}
    result=task.call(req,False);task.new('CHECKPOINT_R1.json',result)
    print(json.dumps({'revision':result['revision'],'event_id':result['event_id'],'pending_explicit':True}))
if __name__=='__main__':main()
