"""Use actual R3 bytes and synthetic mutations to test the consumer's refusal."""
from pathlib import Path
import copy,hashlib,json
from theta_gate import consume,ThetaGateError,MODELS
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):
    with (ROOT/n).open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2)
def main():
    source=ROOT.parent/'r2_refinement_r3/THETA_RESULT_R3.json';recipe=ROOT.parent/'r2_refinement_r3/RECIPE_R3.json'
    save('PLAN_R4.json',{'scope':'SYNTHETIC_MUTATIONS_OF_PINNED_R3_DIAGNOSTIC','source':{'path':str(source),'sha256':sha(source)},
        'recipe':{'path':str(recipe),'sha256':sha(recipe)},'module_sha256':sha(ROOT/'theta_gate.py'),
        'checks':['actual R3 refuses','synthetic equal levels pass diagnostic only','forged flag','altered gap',
                  'NaN','boolean numeric','missing model','callback mismatch','changed pin','missing level','internal failure'],
        'new_scientific_solver_calls':0})
    actual=consume(source,sha(source),recipe,sha(recipe));assert actual['status']=='REFUSE_NUMERICAL'
    assert len(actual['reasons'])==3
    original=json.loads(source.read_text(encoding='utf-8'));positive=copy.deepcopy(original)
    field='log_relative_integral_without_log_kappa'
    for m in MODELS:
        positive['levels'][-1]['models'][m][field]=positive['levels'][-2]['models'][m][field]
        positive['refinement']['last_absolute_log_difference'][m]=0.
    positive['refinement']['indicator_satisfied']=True
    save('FIXTURE_EQUAL_LEVELS_SYNTHETIC.json',positive);p=ROOT/'FIXTURE_EQUAL_LEVELS_SYNTHETIC.json'
    success=consume(p,sha(p),recipe,sha(recipe));assert success['status']=='REFINEMENT_DIAGNOSTIC_PASS' and not success['qualified_observed_verdict']
    changes=[('forged_flag',lambda d:d['refinement'].update(indicator_satisfied=True)),
      ('altered_gap',lambda d:d['refinement']['last_absolute_log_difference'].update(H1_TGL=0)),
      ('nan',lambda d:d['levels'][-1]['models']['H1_TGL'].update({field:float('nan')})),
      ('boolean',lambda d:d['levels'][-1]['models']['H1_TGL'].update({field:True})),
      ('missing_model',lambda d:d['levels'][-1]['models'].pop('H2_LCDM')),
      ('callback',lambda d:d['callback_counts'].update(completed=1)),
      ('missing_level',lambda d:d['levels'].pop(0))]
    refused=[]
    for label,change in changes:
        d=copy.deepcopy(original);change(d);name='MUTATION_'+label+'.json';save(name,d);p=ROOT/name
        try:consume(p,sha(p),recipe,sha(recipe))
        except ThetaGateError as exc:refused.append({'case':label,'reason':str(exc)})
        else:raise AssertionError(label)
    try:consume(source,'0'*64,recipe,sha(recipe))
    except ThetaGateError as exc:refused.append({'case':'pin','reason':str(exc)})
    else:raise AssertionError('pin')
    positive['conditional_precision_summary']['service_not_converged']=1
    save('FIXTURE_INNER_FAILURE_SYNTHETIC.json',positive);p=ROOT/'FIXTURE_INNER_FAILURE_SYNTHETIC.json'
    failure=consume(p,sha(p),recipe,sha(recipe));assert failure['status']=='REFUSE_NUMERICAL'
    save('RESULT_R4.json',{'status':'PASS_CONSUMER_SCOPE','actual_R3':actual,'synthetic_positive':success,
         'synthetic_inner_failure':failure,'refused_mutations':refused,'new_CAMB_calls':0,
         'plan_sha256':sha(ROOT/'PLAN_R4.json')})
    print(json.dumps({'actual':actual['status'],'reasons':actual['reasons'],'mutations_refused':len(refused)}))
if __name__=='__main__':main()
