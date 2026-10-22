"""Four focused checks of additive final-value validation; no solver."""
from pathlib import Path
import copy,hashlib,json
from theta_gate_r4b import consume,ThetaGateError
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):
    with (ROOT/n).open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2)
def main():
    source=ROOT.parent/'r2_refinement_r3/THETA_RESULT_R3.json';recipe=ROOT.parent/'r2_refinement_r3/RECIPE_R3.json'
    save('PLAN_R4B.json',{'status':'ADDITIVE_FOCAL_PLAN','new_solver_calls':0,
       'pins':[{'path':str(p),'sha256':sha(p)} for p in [source,recipe,ROOT/'theta_gate.py',ROOT/'theta_gate_r4b.py',Path(__file__)]],
       'checks':['actual R3 consistent but refused','forged final integral','forged final ratio','forged call sum']})
    original=json.loads(source.read_text(encoding='utf-8'))
    actual=consume(source,sha(source),recipe,sha(recipe));assert actual['status']=='REFUSE_NUMERICAL'
    cases=[('final_integral',lambda d:d['models']['H1_TGL'].update(log_relative_evidence_without_common_log_kappa=0.)),
           ('final_ratio',lambda d:d['lnB_against_H2_same_context'].update(H1_TGL=5.)),
           ('call_sum',lambda d:d['callback_counts']['background_calls'].update(new_calls_declared=1))]
    refused=[]
    for label,change in cases:
        d=copy.deepcopy(original);change(d);name='MUTATION_R4B_'+label+'.json';save(name,d);p=ROOT/name
        try:consume(p,sha(p),recipe,sha(recipe))
        except ThetaGateError as exc:refused.append({'case':label,'reason':str(exc)})
        else:raise AssertionError(label)
    save('RESULT_R4B.json',{'status':'PASS_FOCAL_SCOPE','actual_R3':actual,'refusals':refused,'plan_sha256':sha(ROOT/'PLAN_R4B.json')})
    print(json.dumps({'status':'PASS_FOCAL_SCOPE','refusals':len(refused)}))
if __name__=='__main__':main()
