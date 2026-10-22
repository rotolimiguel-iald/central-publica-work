"""Record independently accepted preparation and the exact remaining dependencies."""
import ast,hashlib,json,os
from pathlib import Path
from datetime import datetime,timezone
import task

def pin(p):
    raw=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}

def main():
    p=task.project()
    assert {'sources','reader_compat','all_engines_admission'} <= {x['id'] for x in p['projection']['settled'] if x['status']=='satisfied'}
    review=task.W/'review/ALL_ENGINES_R2.json'
    assert json.loads(review.read_bytes())['verdict']=='PASS_PREPARATION_NOT_ACTIVATED'
    status={'status':'PREPARATION_REVIEWED_NOT_ACTIVATED','at':datetime.now(timezone.utc).isoformat(),'reference':str(task.REF),
        'evidence':[pin(task.W/n) for n in ['PREPARATION_STATUS_R2.json','review/ALL_ENGINES_R2.json','review/ALL_ENGINES_ACCEPT_R2.json','MEMORY_PREPARATION_R2.json']],
        'versions':{'app':'v392_last_verified','queue':'v393_last_verified','bancada':'v394_reported_by_live_read'},
        'remaining':['Specific human authorization to reopen F0.3.MEMORIA_CIENTIFICA_SYNC','Verified immutable publication of the v394 scientific sources','Final rebinding and model-specific context admission','Queue preparation and independent review','Controlled deployment and effective-use validation'],
        'new_builds':False,'production_modified':False}
    task.new('PREPARATION_STATUS_R3.json',status)
    marker='IALD_V394_PREPARATION_REVIEW_R2_20261019'
    text=f'\n\n### 19/10/2026 — Revisão R2 da preparação v394 concluída\n<!-- {marker} -->\n[REAL — correção ao lado] A revisão independente R2 aceitou a preparação dos contextos: 422tópicos e valores completos recuperáveis no JSON científico, sem exigir publicação nova do cluster derivado local. Requisito all_engines_admission satisfeito na própria missão; fontes e compatibilidade de leitores também satisfeitas. O app NÃO foi ativado. Continuam pendentes a autorização específica da fila, publicação imutável v394, bindings/contagens finais, implantação e uso efetivo. As versões ativas do adendo anterior permanecem inalteradas. Recibo: {task.W / "PREPARATION_STATUS_R3.json"}.\n<!-- END_{marker} -->\n'
    old=task.W.parent/'iald_monthly_wallet_20261007/record_memory.py'
    node=next(n for n in ast.parse(old.read_bytes()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets))
    ns={'Path':Path};exec(compile(ast.Module(body=[node],type_ignores=[]),'established_memory_paths','exec'),ns)
    rows=[];stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    for path in ns['paths']:
        before=path.read_bytes()
        if marker.encode() in before:rows.append({'path':str(path),'status':'already_present'});continue
        after=before+text.replace('\n','\r\n' if b'\r\n' in before else '\n').encode()
        backup=path.with_name(path.name+'.bak_'+stamp)
        with backup.open('xb') as f:f.write(before);f.flush();os.fsync(f.fileno())
        assert backup.read_bytes()==before
        tmp=path.with_name(path.name+'.tmp_v394_review_'+str(os.getpid()))
        with tmp.open('xb') as f:f.write(after);f.flush();os.fsync(f.fileno())
        assert tmp.read_bytes()==after and path.read_bytes()==before
        os.replace(tmp,path);assert path.read_bytes()==after and after.startswith(before)
        rows.append({'path':str(path),'backup':str(backup),'sha256':hashlib.sha256(after).hexdigest()})
    task.new('MEMORY_PREPARATION_R3.json',{'status':'PREPARATION_ONLY','surfaces':rows})
    snap=task.call({'operation':'get','reference':str(task.REF)},False)
    handles={h['id']:h for h in snap['p'].get('handles',[])}
    for ident,state in [('app_builder','completed'),('all_engines_review','accepted')]:
        handles[ident]={**handles[ident],'status':state,'note':'Preparation only; R2 independently reviewed. No app or queue activation.'}
    src=pin(task.W/'PREPARATION_STATUS_R3.json')
    result=task.call({'operation':'transition','reference':str(task.REF),'actor':{'id':task.OWNER,'kind':'agent'},'expected_revision':snap['revision'],'event_id':'v394-preparation-reviewed-checkpoint-r3','changes':{
        'records':[{'id':'v394-preparation-r2-reviewed','kind':'fact','statute':'REAL','text':'Preparação R2 aceita por revisor distinto. Fontes, dois leitores e projeção422tópicos satisfeitos; sem ativação de app/fila. Pendentes decisão humana específica e publicação, depois binding/admissão/implantação.','sources':[{'kind':'artifact','ref':src['path'],'sha256':src['sha256']}]}],
        'flow':{'phase':'preparation_reviewed_awaiting_human_and_publication','next_action':'Recuperar a resposta específica da fila e o commit público v394. Retomar a mesma referência; não duplicar snapshots, IDs ou chamadas.','handles':list(handles.values())}}},False)
    task.new('CHECKPOINT_R3.json',result)
    print(json.dumps({'status':'PREPARATION_REVIEWED_NOT_ACTIVATED','revision':result['revision'],'memory_surfaces':len(rows)}))

if __name__=='__main__':main()
