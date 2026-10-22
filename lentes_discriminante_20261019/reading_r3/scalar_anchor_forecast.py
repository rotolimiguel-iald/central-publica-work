"""Conditional scalar D1b separation with an external background anchor; not a data verdict."""
from pathlib import Path
import json,math,hashlib,re,datetime
ROOT=Path(__file__).resolve().parent
SPEC=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.1\PREREGISTRO_FASE9_V2_R5_2_F31_LABELS_E1_20261008.json')
UM=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def save(n,d):
    with (ROOT/n).open('x',encoding='utf-8') as f:json.dump(d,f,ensure_ascii=False,indent=2)
def find(obj,key):
    if isinstance(obj,dict):
        if key in obj:yield obj[key]
        for v in obj.values():yield from find(v,key)
    elif isinstance(obj,list):
        for v in obj:yield from find(v,key)

def main():
    for n in ['SCALAR_ANCHOR_PLAN_R3.json','SCALAR_ANCHOR_RESULT_R3.json']:
        if (ROOT/n).exists():raise FileExistsError(n)
    save('SCALAR_ANCHOR_PLAN_R3.json',{'status':'INPUT_CONDITIONAL_FORECAST_ONLY','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'hypothesis':'Published scalar lens estimator really obeys H_lens=K H_bg, per house contract. Raw lens likelihood bridge remains OPEN.',
        'model':'Asimov Gaussian two-measurement contrast to common-H GR null; independent external background measurement. K treated fixed; optimistic for additional theory/covariance uncertainty.',
        'background':'BG1 and law coefficients from pinned house draft, NOT a new background fit',
        'lens_sigma_scenarios_km_s_Mpc':[2.3,2.4,3.9],
        'sigma_provenance':'2.3/2.4 are the asymmetric published2026 H0 bars, each treated as a separate symmetric Gaussian planning scenario;3.9 is published2025 upper bar. No centers or observed residuals enter.',
        'public_source_custody':pin(ROOT.parent/'PUBLIC_SOURCE_CUSTODY_R2.json'),
        'formula':'Z_A=(K-1)*H_bg/sqrt(sigma_lens^2+sigma_bg^2); ideal fixed-background upper norm uses sigma_bg=0',
        'priors_scope':'Not independent of every public analysis automatically; actual likelihood overlap and compression must be audited before data.',
        'sources':[pin(SPEC),pin(UM)],'script':pin(Path(__file__))})
    spec=json.loads(SPEC.read_text(encoding='utf-8'))
    laws=list(find(spec,'lei'));law=next(x for x in laws if isinstance(x,dict) and 'Omega_r' in x)
    bg=next(x['BG1'] for x in find(spec,'fundos') if 'BG1' in x)
    alpha=float(re.search(r'^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)',UM.read_text(encoding='utf-8'),re.M).group(1))
    beta=alpha*math.sqrt(math.e);z=law['z_star'];Om=law['Omega_m'];Or=law['Omega_r']
    E=math.sqrt(Om*(1+z)**3+Or*(1+z)**4+1-Om-Or);K=E**(2*beta/3)
    assert abs(K-law['K_frozen_V1'])<1e-12
    delta=(K-1)*bg['H0'];sb=bg['sigma']
    save('SCALAR_ANCHOR_RESULT_R3.json',{'status':'DERIVED_CONDITIONAL_FORECAST_NO_OBSERVED_TEST','beta_runtime':beta,'K_runtime':K,
        'H_bg_from_draft':bg['H0'],'sigma_bg_from_draft':sb,'expected_scalar_separation_km_s_Mpc':delta,
        'sigma_lens_required_for_median_norm5_with_bg':math.sqrt(max(0,(delta/5)**2-sb**2)),
        'rows':[{'sigma_lens_scenario':sl,'norm_with_declared_independent_BG1':delta/math.hypot(sl,sb),'ideal_fixed_BG_upper_norm':delta/sl} for sl in [2.3,2.4,3.9]],
        'scope':'Planning in the scalar contract only. No measured lens center, observed likelihood ratio, or confirmation. Does not establish raw estimator invariance, data independence, K uncertainty or 90percent discovery power.',
        'plan':pin(ROOT/'SCALAR_ANCHOR_PLAN_R3.json'),'script':pin(Path(__file__))})
    print(json.dumps({'K_runtime':K,'delta':delta,'required_sigma_lens':math.sqrt(max(0,(delta/5)**2-sb**2))}))

if __name__=='__main__':main()
