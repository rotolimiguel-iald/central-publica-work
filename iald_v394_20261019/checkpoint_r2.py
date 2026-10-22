"""Record verified preparation; no production or source-file changes."""
from pathlib import Path
import hashlib,json
import task

def main():
    task.project()
    snap=task.call({'operation':'get','reference':str(task.REF)},False)
    handles={h['id']:h for h in snap['p'].get('handles',[])}
    updates=[
        {'id':'app_builder','agent_id':'01a15604-76c6-7110-9a73-2dc692d95018','kind':'delegated_preparation','status':'working','note':'422-topic projection prepared; R2 correction under preparation to avoid requiring publication of a derived local cluster.'},
        {'id':'app_foundation_review','agent_id':'01a15607-da9a-76e2-a12f-7ce9a5ab4a54','kind':'independent_review','status':'completed','note':'PASS_FOUNDATION_WITH_SCOPE; preparation only, no app acceptance or installation.'},
        {'id':'reader_compat_review','agent_id':'01a15607-da9a-76e2-a12f-7ce9a5ab4a54','kind':'independent_review','status':'accepted','note':'Two reader-size caps reviewed; not installed.'},
        {'id':'all_engines_review','agent_id':'01a15607-da9a-76e2-a12f-7ce9a5ab4a54','kind':'independent_review','status':'working','note':'R1 preparation submitted; final publication and provider-native admission still pending.'},
        {'id':'queue_gate','kind':'operator_decision','status':'awaiting_operator','note':'Specific question remains pending after automatic approval review rejected AGUARDA_OPERADOR to EM_CURSO.'},
        {'id':'public_v394','kind':'external_publication','status':'awaiting_external','note':'Read-only Git observation: v394 files now present as working changes; HEAD remains f15e51a1d4369eb6cc97c5521782aedc0ee6fb78. No immutable v394 URL inferred.'},
    ]
    handles.update({h['id']:h for h in updates})
    sources=[]
    for name in ['sources_verified.json','bancada_live_state.json','app/DELIVERY_PREPARED.json','app/engines/DELIVERY_PREPARED_R1.json','review/READER_COMPAT_R1.json','queue/DELIVERY_PREPARED.json']:
        p=task.W/name
        sources.append({'kind':'artifact','ref':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    changes={'records':[{'id':'v394-preparation-checkpoint-r2','kind':'fact','statute':'REAL','text':'Preparação local v394 e custódia conferidas; Bancada já relata v394. Pacotes Haiku/shared contados são históricos de staging. Projeção de422tópicos e correção de dois limites de leitores preparadas; nem app nem fila foram ativados. App seguev392 e fila393 conforme últimas leituras. Publicação final, vinculação, contagens finais e aprovação específica da fila permanecem pendentes.','sources':sources}],
        'flow':{'phase':'prepared_pending_publication_and_queue_gate','next_action':'Concluir revisão da projeção; obter resposta humana da fila e commit público v394; revalidar/revincular pacotes antes de qualquer implantação.','handles':list(handles.values())}}
    out=task.call({'operation':'transition','reference':str(task.REF),'actor':{'id':task.OWNER,'kind':'agent'},'expected_revision':snap['revision'],'event_id':'v394-preparation-checkpoint-r2','changes':changes},False)
    task.new('CHECKPOINT_R2.json',out)
    print(json.dumps({'revision':out['revision'],'event_id':out['event_id'],'production_modified':False}))

if __name__=='__main__':main()
