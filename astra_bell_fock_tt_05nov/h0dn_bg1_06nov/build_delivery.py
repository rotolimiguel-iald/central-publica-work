"""Assemble a scoped result with source pins; never modifies frozen analysis."""
from pathlib import Path
from datetime import datetime,timezone
import json, hashlib, numpy as np
from scipy.stats import norm
BASE=Path(__file__).resolve().parent

def load(rel):return json.loads((BASE/rel).read_text('utf-8'))
def pin(rel):
    p=BASE/rel
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
def new(rel,data):
    p=BASE/rel
    with p.open('x',encoding='utf-8') as f:json.dump(data,f,ensure_ascii=False,indent=2,allow_nan=False)

def main():
    freeze=load('FREEZE_R2.json')
    for row in freeze['files']:
        assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256']
    geo=load('PROSPECTIVE_GEOMETRY.json');bg=load('background/BG1.json')
    mc=load('blind_custodian/UNBLINDED_RESULTS.json');exact=load('blind_custodian/EXACT_BG_SUPPLEMENT.json')
    alt=next(c for c in mc['outputs'] if c['kind']=='ordinary' and c['hypothesis']==1 and c['fixed_bias']==0 and c['random_sd']==0)
    tail=[c for c in mc['outputs'] if c['kind']=='importance']
    models=[]
    for row in alt['models']:
        name=row['name'];q=next(q for q in exact['quadrature'] if q['name']==name)
        t=next(x for c in tail for x in c['models'] if x['name']==name and x['score']=='z_null')
        models.append({'name':name,'D_expected':geo['models'][name]['D'],
            'power_MC_frozen_threshold':row['rejection'],'power_analytic_gaussian':geo['models'][name]['power_at_5sigma'],
            'null_tail_importance':t,'TGL_residual_coverage95':row['TGL_compatibility_coverage95'],
            'exact_bg_cut_five_equivalent_sigma':q['original_equivalent_normal_sigma'],
            'exact_bg_calibrated_future_cut':q['exact_future_q_over_sd0'],
            'exact_bg_calibrated_future_power':q['exact_future_power']})
    envelope=load('cross_rung/PSD_ENVELOPE.json')
    cross=[]
    for r in envelope['results']:
        rho25=next(s for s in r['scenarios'] if s['rho']==.25)
        sig=rho25['reoptimized_GLS_sigma'];D=geo['logK']/np.sqrt(sig**2+geo['background_variance_logH'])
        cross.append({'free_cepheid_bias':r['free_cepheid_bias'],
            'cross_only_fixed_estimator_worst_D':float(geo['logK']/np.sqrt(r['cross_only_sigma_max']**2+geo['background_variance_logH'])),
            'illustrative_rho_025_reoptimized_D':float(D),'illustrative_rho_025_power':float(norm.sf(5-D)),
            'status':'Mathematical sensitivity only. Adversarial signs from influence weights, not measured physical correlations; not a selection criterion or falsification.'})
    sources=['analysis_plan.json','FREEZE.json','FREEZE_R2.json','estimator.py','prepare_estimator.py','estimator_frozen.npz',
             'network/MANIFEST.json','network/network.npz','background/BG1.json','background/SOURCE_PINS.json',
             'background/POST_FREEZE_CHANGE.json','blind_custodian/INDEPENDENT_GEOMETRY_REVIEW.json',
             'blind_custodian/CUSTODY_COMMIT.json','blind_custodian/SCORES_COMMIT.json','ACK_SCORES.json',
             'blind_custodian/UNBLINDED_RESULTS.json','blind_custodian/EXACT_BG_SUPPLEMENT.json',
             'cross_rung/DELIVERY.json','cross_rung/PSD_ENVELOPE.json','DESIGN_MARGINS.json',
             'background/MARGINS_REVIEW.json','OPERADOR_AFIXACAO.txt','background/AFIXACAO_NOTA.md',
             'background/AFIXACAO_SOURCE_PINS.json','PODER_CEGO.png']
    result={
      'status':'CONDITIONAL_POWER_VALIDATED__FULL_PHYSICAL_COVARIANCE_OPEN',
      'created_utc':datetime.now(timezone.utc).isoformat(),
      'unit':'F3.H0DN_COV_06NOV','acom_reference':str(BASE.parent/'SESSION_REFERENCE.json'),
      'scientific_statute':'REAL for construction and computations; DERIVED conditional power; OPEN missing covariance and empirical discrimination',
      'headline':'O modelo publicado conserva separação prospectiva acima de5sigma; a completude física da covariância não está demonstrada.',
      'instrument':{'live_contract':bg['live_contract'],
          'execution':'Extensão local reprodutível de análise, ligada ao contrato da Bancada e ao BG1 qualificado. Não é novo endpoint implantado nem novo ajuste BG1.'},
      'matrices':{'H0DN_A_shape':[255,64],'H0DN_C_shape':[255,255],'rank_C':183,'nullity_C':72,
                  'joint_C_shape':[258,258],'joint_rank':186,'cepheid_bias_column_rows':119,
                  'SN_Ia_equations':'55 calibradores + 1 intercepto','SBF_equations':'14 calibradores + 1 intercepto',
                  'cross_background':'Zero only under explicit conditional independence, not a measured zero.'},
      'model':'Centered y=A eta+a_h h+c_C delta_C+epsilon. Z=(hhat-log10Hbg)/sigma_null; fixed positive predicted shift log10K. Cepheid bias free is a separate prespecified robustness model.',
      'K':geo['K'],'log10K':geo['logK'],'models':models,
      'blind_trials':{'ordinary_independent_per_hypothesis':100000,'importance_independent_per_model':100000,
           'total_independent_primitive_realizations':400000,'total_processed_scenario_realizations':1600000,
           'scenarios':16,'score_blocks':64,'paired_stress_and_fits':True,
           'labels_opened_only_after_scores_pinned':True,'historical_public_estimates_were_already_known':True},
      'rare_tail':'Analytic Gaussian tail plus importance sampling. Zero ordinary-null exceedances alone is not evidence of a5sigma bound.',
      'exact_background':'Nonlinear log transform makes frozen5 slightly less than exact5sigma; additive quadrature gives future calibrated cuts, without changing frozen trials.',
      'covariance_completeness':load('cross_rung/DELIVERY.json')['conclusions'],
      'cross_covariance_sensitivity':cross,
      'scope_conditions':['Published H0DN Gaussian magnitude/log-H model and fixed q0=-0.55,j0=1.',
          'BG1 Planck compressed plus DESI DR2 uses archived Gauss-Newton covariance; source pins still match current Bancada.',
          'TGL K is frozen; S5 local derivative propagated separately for compatibility, with tiny reference-center discrepancy explicitly recorded.',
          'No observed local data fit, no empirical5sigma finding, no gate change. Additional physical correlations remain unquantified.'],
      'next_steps':['Recover the light-curve aggregation operator, validated IDs/aliases, and SN-only/host/PV covariance decomposition before completing physical joint covariance.',
          'Freeze a follow-up covariance and use the exact calibrated threshold if choosing Gaussian H0 rather than Gaussian logH0.',
          'For90% robust power, the present model needs about16.9% lower network sigma; an actually independent Cepheid-bias constraint at0.0183mag is one conditional design route. No such measurement is asserted.'],
      'afixacao':{'operator_input':pin('OPERADOR_AFIXACAO.txt'),
          'interpretation':'Travessia definida pelo operador no próprio ato de leitura/conjugação/temporalização; não exigir passagem anterior independente.',
          'open':'Distinguir J da face finita e J antiunitário. JKJ=-K e J²=I não determinam sozinhos instrumento, relógio ou irreversibilidade do registro.'},
      'sources':[pin(p) for p in sources]}
    new('ENTREGA_H0DN_BG1.json',result)
    route={'tipo':'ROTA','rota_id':'estatistica.h0dn_bg1.cov_injecoes_06nov','dominio':'ESTATISTICA_CONJUNTA',
           'status':'EXAMINADA_COM_DEFEITO','estatuto':'REAL','titulo':'H0DN x BG1: matriz publicada e injeções cegas',
           'metodo':'A255x64,C255x255 rank183; BG1cov3x3; GLS suporte singular;100k por hipótese, importance sampling, labels após64escores pinados.',
           'resultado':f"D={models[0]['D_expected']:.6f}/{models[1]['D_expected']:.6f}; poder MC={models[0]['power_MC_frozen_threshold']['estimate']:.5f}/{models[1]['power_MC_frozen_threshold']['estimate']:.5f}, baseline/viés Cefeidas livre.",
           'defeito':'Covariância física entre calibradores e entre degraus não reconstruível univocamente dos insumos localizados; pesos,8IDs e decomposição SN/host ausentes.',
           'olhou_dados':True,'nota':'IDs, erros e covariâncias públicos; nenhum ajuste dos centros observados. Somente simulações. Afixação registrada como INPUT, instrumento OPEN.',
           'nao_refazer':'Reutilizar frozenR2 e scores; não gerar novas seeds para reproduzir a mesma unidade.',
           'proximo_passo':result['next_steps'][0],'artefatos':[str(BASE/'ENTREGA_H0DN_BG1.json')]}
    new('ROTA_RESULTADO.json',route)
    print(json.dumps({'delivery':pin('ENTREGA_H0DN_BG1.json'),'models':models},ensure_ascii=False))

if __name__=='__main__':main()
