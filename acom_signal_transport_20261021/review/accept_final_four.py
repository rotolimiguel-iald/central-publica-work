"""Verify applied receipts and record four distinct reviews; no runtime execution."""
import hashlib,json,sys
from pathlib import Path
from datetime import datetime,timezone
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(W))
import task
ACTOR='codex-readability-reviewer'
IDS=('engineering','memory_prepare','budget_fix','deployment')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def pin(p):return dict(path=str(p),sha256=sha(p))
def verify(e):
    assert sha(e['path'])==e['sha256'],e['path']
    if 'bytes' in e:assert Path(e['path']).stat().st_size==e['bytes'],e['path']
def refs(obj):
    if isinstance(obj,dict):
        if 'path' in obj and 'sha256' in obj:verify(obj)
        for v in obj.values():refs(v)
    elif isinstance(obj,list):
        for v in obj:refs(v)
def new(p,obj):
    with p.open('xb') as f:f.write((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())

reportpath=W/'review/FINAL_REVIEW.json'
if '--accept' not in sys.argv:
    previous=load(W/'review/MATERIAL_FINAL_CHECKS_R1.json')
    assert previous['status']=='PASS'
    for e in previous['evidence']:verify(e)
    mr=load(W/'review/MEMORY_PREPARE_REVIEW_R1.json'); ar=load(W/'review/ADMIN_DEADLINES37_REVIEW_R2.json')
    assert mr['status']==ar['status']=='PASS';refs(mr);refs(ar)
    mp=load(mr['plan']['path']); ma=load(W/'MEMORY_APPLIED_FINAL.json')
    assert ma['status']=='PASS' and ma['plan_sha256']==mr['plan_sha256']
    planned={x['path']:x for x in mp['surfaces']}; actual={x['path']:x for x in ma['surfaces']}
    assert len(planned)==len(actual)==8 and planned.keys()==actual.keys()
    chunk=Path(mp['append']['path']).read_bytes()
    for path,entry in actual.items():
        expected=planned[path]; backup=Path(entry['backup']); before=backup.read_bytes(); after=Path(path).read_bytes()
        assert backup.parent==Path(path).parent
        assert sha(backup)==entry['before_sha256']==expected['before_sha256']
        assert sha(path)==entry['after_sha256']==expected['expected_after_sha256']
        assert after==before+chunk and len(after)==entry['bytes']==expected['expected_after_bytes']
    aa=load(W/'admin_deadlines37stage/DELIVERY_APPLIED_R2.json');refs(aa)
    ap=load(ar['plan']['path'])
    assert aa['plan']['sha256']==ar['plan_sha256'] and aa['review']['sha256']==sha(W/'review/ADMIN_DEADLINES37_REVIEW_R2.json')
    assert aa['backup']['sha256']==ap['baseline_sha256'] and aa['destination']['sha256']==ap['candidate']['sha256']
    assert Path(aa['backup']['path']).parent==Path(aa['destination']['path']).parent
    assert aa['visibility']=='ADMIN_ONLY' and aa['restart'] is False
    assert len(aa['admin_snapshot'])==2 and all(r['level']=='unknown' and r['expires_at'] is None and r['days_remaining'] is None for r in aa['admin_snapshot'])
    runtime={}
    for prefix in ('','budget_fix/'):
        for f in load(W/(prefix+'install_plan.json'))['files']:runtime[f['destination']]=f['sha256']
    assert len(runtime)==18
    for path,h in runtime.items():assert sha(path)==h,path
    science=load(W/'SCIENCE_BASELINE.json')['files'];assert len(science)==5
    for e in science:verify(e)
    submission=load(W/'DEPLOYMENT_SUBMITTED_FINAL.json');assert submission['task']['status']=='review_pending'
    for e in submission['task']['evidence']:verify(e)
    state=task.project()
    for tid in IDS:
        t=next(x for x in state['projection']['active'] if x['id']==tid)
        assert t['status']=='review_pending' and t['submitted_by']!=ACTOR
        for e in t['evidence']:verify(e)
    evidence=[pin(W/n) for n in ['review/MATERIAL_FINAL_CHECKS_R1.json','review/FINAL_CONTROL_R2.json','review/LUMINIDIC_REVIEW_R1.json','prototype_R2/PROVENANCE_ADDENDUM.json','validation/review_final.json','budget_fix/validation/review_final.json','review/MEMORY_PREPARE_REVIEW_R1.json','review/ADMIN_DEADLINES37_REVIEW_R2.json','MEMORY_APPLIED_FINAL.json','admin_deadlines37stage/DELIVERY_APPLIED_R2.json','DEPLOYMENT_SUBMITTED_FINAL.json','delivery.json','live_validation.json','availability.json']]
    new(reportpath,dict(status='PASS',reviewer=ACTOR,created_utc=datetime.now(timezone.utc).isoformat(),scope='Revisão final independente: engineering, memory_prepare, budget_fix e deployment; recibos e estado aplicado, sem novos testes.',tasks=list(IDS),findings=[],evidence=evidence,checks=['Reutilizado MATERIAL_FINAL_CHECKS_R1 PASS; evidências continuam pinadas','8 memórias = backup imediato + APPEND exato, hashes e tamanhos confirmados','Admin R2 instalado idêntico ao candidato revisado; backup e parecer vinculados; apenas dois subobjetos','18 runtime e 5 ciência íntegros','4 tarefas submetidas por atores distintos do revisor; evidências pinadas'],limitations=['Sem instalação física mobile verificada; Google Play não publicado','Wirebytes do teste live não medidos; custo estimado não é fatura','Controle luminídico experimental não implantado; nenhuma proteção quântica ou ganho genérico alegado','Nenhuma API, teste novo, aplicação ou alteração de gate científico/quadro pelo revisor'],projection_revision=state['receipt']['revision']))
    print(json.dumps(pin(reportpath)))
else:
    report=load(reportpath);assert report['status']=='PASS' and report['reviewer']==ACTOR
    for e in report['evidence']:verify(e)
    for tid in IDS:
        output=W/'review'/(tid.upper()+'_ACCEPTED_FINAL.json')
        if output.exists():raise RuntimeError('Receipt exists; reconcile before repeating: '+str(output))
        current=task.project(); t=next(x for x in current['projection']['active'] if x['id']==tid)
        assert t['status']=='review_pending' and t['submitted_by']!=ACTOR
        for e in t['evidence']:verify(e)
        result=task.act('accept',actor=ACTOR,task_id=tid,event_id='signal-final-independent-accept-'+tid+'-20261021',review_evidence=[pin(reportpath)])
        new(output,dict(status='ACCEPT_RECORDED',actor=ACTOR,task_id=tid,result=result,review_evidence=pin(reportpath)))
        print(json.dumps(dict(task_id=tid,receipt=pin(output),revision=result['receipt']['revision'])),flush=True)
    final=task.project()
    tasks=[t for t in final['projection']['settled'] if t['id'] in IDS]
    assert len(tasks)==4 and all(t['status']=='satisfied' and t['reviewed_by']==ACTOR for t in tasks)
    out=dict(status='PASS',reviewer=ACTOR,receipt=final['receipt'],tasks=[{k:t[k] for k in ('id','status','reviewed_by','submitted_by')} for t in tasks],active_tasks=final['projection']['active'],tetelestai=final['projection']['tetelestai'],review=pin(reportpath))
    new(W/'review/FINAL_ACCEPTANCE_STATE.json',out)
    print(json.dumps(out,ensure_ascii=False))
