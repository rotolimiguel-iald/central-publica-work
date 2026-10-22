"""Read sealed snapshots; recompute historical arithmetic and test a draft engine."""
from pathlib import Path
from fractions import Fraction as F
import ast
import copy
import hashlib
import json
import math
from joint_contour_v1 import beta_runtime,gaussian_scores,evaluate,protocol_hash,chi2_survival,critical_value

ROOT = Path(__file__).resolve().parent
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def load(name):
    return json.loads((ROOT/name).read_text(encoding='utf-8-sig'))
def save(name,data):
    path = ROOT/name
    payload = (json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    if path.exists():
        assert path.read_bytes() == payload, 'Refusing changed output: '+str(path)
        return
    temp = path.with_suffix(path.suffix+'.tmp')
    with temp.open('xb') as stream:
        stream.write(payload)
    assert temp.stat().st_size == len(payload)
    temp.rename(path)

data = load('ordem005_um_absoluto.json')
seal = load('ordem005_um_absoluto_selo.json')
sealed_source = ROOT/'um_ordens003_004_snapshot.py'
current_source = ROOT/'um_ordem005_snapshot.py'
assert sha(ROOT/'ordem005_um_absoluto.json') == seal['sha256']['um_absoluto.json']
assert sha(sealed_source) == seal['sha256']['um.py']
trees = [ast.parse(p.read_text(encoding='utf-8-sig')) for p in [sealed_source,current_source]]
constants = {}
for node in trees[0].body:
    if isinstance(node,ast.Assign):
        for target in node.targets:
            if isinstance(target,ast.Name) and target.id in ('SEALED_CODATA_ALPHA','C_LIGHT','G_NEWTON','MSUN','MPC_M','SEALED_LIT_GEOMETRY','GA_ACCEPTED_WINDOW_Msun'):
                constants[target.id] = ast.literal_eval(node.value)
beta = constants['SEALED_CODATA_ALPHA']*math.sqrt(math.e)
assert beta == beta_runtime()
coefficient = 2*beta**2*constants['C_LIGHT']**2/(4*math.pi*constants['G_NEWTON'])*constants['MPC_M']/constants['MSUN']
ga = data['core']['ga_mass_audit']
mass_rows = []
for row in ga['scale_audit']:
    prediction = coefficient*row['R_Mpc']
    ratio = prediction/row['M_lit_Msun']
    assert math.isclose(prediction,row['M_form_Msun'],rel_tol=1e-14)
    mass_rows.append({**row,'recomputed_Msun':prediction,'recomputed_ratio':ratio,
                      'radius_to_match_Mpc':row['M_lit_Msun']/coefficient,
                      'required_multiplier':1/ratio})
v = beta*constants['C_LIGHT']/math.sqrt(2*math.pi)/1000
assert math.isclose(v,ga['values']['v_universal_implicada_kms'],rel_tol=1e-14)
function_names = ['prove_ga_mass_audit','prove_neutrino_m2','prove_coma_distance_dephasing',
                  'prove_void_floor_v11_sdss_independent','prove_evidence_audit']
function_audit = []
for name in function_names:
    nodes = [next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name==name) for t in trees]
    function_audit.append({'function':name,'sealed_line':nodes[0].lineno,'current_line':nodes[1].lineno,
                           'ast_identical':ast.dump(nodes[0])==ast.dump(nodes[1])})
snapshot_status = {'result_matches_seal':True,'prior_source_matches_seal':True,
                   'current_source_matches_seal':sha(current_source)==seal['sha256']['um.py'],
                   'source_functions':function_audit,
                   'hashes':{p.name:sha(p) for p in [sealed_source,current_source,ROOT/'ordem005_um_absoluto.json',
                                                   ROOT/'ordem005_um_absoluto_selo.json',ROOT/'ordem005_run_v98_stdout.txt']}}
save('ORDEM005_MASSA_CONTROLES.json',{'status':'REAL — recomputation of sealed inputs, not new observations',
     'constants':constants,'beta_runtime':beta,'mass_per_Mpc_Msun':coefficient,'v_characteristic_kms':v,
     'rows':mass_rows,'R_exact_40_over_h07':40/0.7,'mass_at_exact_radius':coefficient*40/0.7,
     'mass_GA_in_window':constants['GA_ACCEPTED_WINDOW_Msun'][0]<=coefficient*57<=constants['GA_ACCEPTED_WINDOW_Msun'][1],
     'relative_radius_rounding':57/(40/0.7)-1,'provenance':snapshot_status})

protocol = {'version':'JOINT_CONTOUR_V1_DRAFT','ratified':False,
            'roster':['neutrino_m2','coma_distance','ga_mass','void_floor'],
            'null':'beta=ALPHA_FINE_CODATA_2018*sqrt(e)','alternative':'one common free real constant',
            'noise':'known fixed Gaussian covariance','comparison':'AIC penalty 2',
            'kill':'chi2_n survival <= erfc(5/sqrt(2))','power':'lower bound >= 0.90 for uniform/single shifts +/- beta/2',
            'prospective_required':True,'optional_stopping':False}
digest = protocol_hash(protocol)
save('JOINT_CONTOUR_V1_SPEC_DRAFT.json',protocol)
n = 4
bf = F(str(beta))
sigma = bf/100
cov = [[str(sigma*sigma if i==j else F(0)) for j in range(n)] for i in range(n)]
base = {'data_kind':'synthetic','domains':[{'id':name,'eligible':True,'estimate':str(bf)} for name in protocol['roster']],
        'covariance':cov,'provenance_valid':True,'systematics_valid':True,
        'covariance_valid':True,'gaussian_model_valid':True}
tests = {}
def check(name,payload,want,hash_value=digest):
    result = evaluate(payload,protocol,hash_value)
    assert result['verdict']==want,(name,result)
    tests[name]=result
good='JOINT_CONTOUR_NOT_FALSIFIED'
bad='JOINT_CONTOUR_FALSIFIED'
inc='JOINT_CONTOUR_INCONCLUSIVE'
check('A_correct',base,good)
for sign in [-1,1]:
    shifted=copy.deepcopy(base)
    for row in shifted['domains']:
        row['estimate']=str(bf+sign*10*sigma)
    check('B_correct_shift_'+str(sign),shifted,bad)
    assert tests['B_correct_shift_'+str(sign)]['aic_preference']=='B'
opposed=copy.deepcopy(base)
for i,row in enumerate(opposed['domains']):
    row['estimate']=str(bf+(10 if i%2 else -10)*sigma)
check('opposite_residuals',opposed,bad)
assert tests['opposite_residuals']['aic_preference']=='A'
low=copy.deepcopy(base)
low['covariance']=[[str(bf*bf if i==j else F(0)) for j in range(n)] for i in range(n)]
check('low_power',low,inc)
missing=copy.deepcopy(base)
missing['domains'].pop()
check('missing_domain',missing,inc)
invalid=copy.deepcopy(base)
invalid['systematics_valid']=False
check('systematics_failure',invalid,inc)
correlated=copy.deepcopy(base)
correlated['covariance']=[[str(sigma*sigma*(1 if i==j else F(1,2))) for j in range(n)] for i in range(n)]
check('correlated_covariance',correlated,good)
assert F(tests['correlated_covariance']['information'])==F(tests['A_correct']['information'])*F(2,5)
singular=copy.deepcopy(base)
singular['covariance']=[[str(sigma*sigma)]*n for _ in range(n)]
check('singular_covariance',singular,inc)
asymmetric=copy.deepcopy(base)
asymmetric['covariance'][0][1]=str(sigma*sigma/2)
check('asymmetric_covariance',asymmetric,inc)
nonfinite=copy.deepcopy(base)
nonfinite['domains'][0]['estimate']=float('nan')
check('nonfinite',nonfinite,inc)
check('altered_hash',base,inc,'0'*64)
draft=copy.deepcopy(base)
draft['data_kind']='prospective'
draft['prospective_lock_verified']=True
check('unratified_draft',draft,inc)
for qa in [0,1,5,25,50]:
    assert math.isclose(chi2_survival(qa,2),math.exp(-qa/2),rel_tol=1e-14)
    assert math.isclose(chi2_survival(qa,4),math.exp(-qa/2)*(1+qa/2),rel_tol=1e-14)
assert math.isclose(critical_value(1,math.erfc(5/math.sqrt(2))),25,rel_tol=1e-14)
identity=[[int(i==j) for j in range(4)] for i in range(4)]
exact = {}
for name,values in [('center',[1,1,1,1]),('shift',[2,2,2,2]),('opposed',[11,-9,11,-9])]:
    score=gaussian_scores(values,identity,1)
    exact[name]={key:str(score[key]) for key in ('qa','qb','gain','delta_aic')}
assert exact['center']['delta_aic']=='2'
assert exact['shift']['delta_aic']=='-2'
assert exact['opposed']['qa']=='400' and exact['opposed']['gain']=='0'
save('JOINT_CONTOUR_V1_CONTROLES.json',{'protocol_hash':digest,'tests':tests,'exact_controls':exact,
                                      'chi_square_reference_checks':True})

core=data['core']
eligibility={
 'neutrino_m2':{'eligible':False,'reason':'One independent input can be proposed; Gaussian transform, m1=0 and 1eV normalization need fixed model; JUNO/global overlap not resolved',
                 'sealed':core['neutrino_m2']['values']},
 'coma_distance':{'eligible':False,'reason':'Sealed primary comparison is null; missing full input uncertainties',
                   'sealed':core['coma_distance_dephasing']},
 'ga_mass':{'eligible':False,'reason':'Conditional source law; no sigma_R, sigma_M or covariance; broad window not likelihood','sealed':ga},
 'void_floor':{'eligible':False,'reason':'One-sided density bound is not a point estimate of beta; 6.2 profile SNR has failed systematics',
                'sealed_primary':core['void_floor_v11']['primary'],'sealed_primary_verdict':core['void_floor_v11']['verdict'],
                'sealed_profile_snr':core['void_floor_final']['snr_profile'],
                'sealed_profile_systematics':core['void_floor_final']['systematics'],
                'sealed_profile_fisher':core['void_floor_final']['power_fisher_separation_sigma2']}}
actual={'data_kind':'prospective','prospective_lock_verified':False,
        'domains':[{'id':name,'eligible':eligibility[name]['eligible']} for name in protocol['roster']]}
actual_result=evaluate(actual,protocol,digest)
assert actual_result['verdict']==inc
save('JOINT_CONTOUR_V1_ELEGIBILIDADE.json',{'status':'DRAFT — known sealed summaries; not a prospective test',
      'eligibility':eligibility,'machine_result':actual_result,'provenance':snapshot_status,
      'real_joint_statistic_computed':False})
print(json.dumps({'mass_cases':len(mass_rows),'engine_tests':len(tests),'exact_worlds':len(exact),
                  'known_sealed_state':actual_result['verdict'],'source_provenance':snapshot_status},ensure_ascii=False))
