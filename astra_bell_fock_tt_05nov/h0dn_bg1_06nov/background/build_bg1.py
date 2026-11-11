"""Recover qualified BG1 without opening local H0 data or instantiating Motor.

Outputs use log10 throughout. Historical S5 is an anchored local linearization:
the mean uses frozen K, while the derivative comes from K(theta).
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
F9 = Path('C:/IALD/Central de Patentes/work/fase9_v2_c1_23out')
BANCADA = Path('C:/IALD/Bancada_Um')
QPATH = F9 / 'testes/QUALIFICACAO_FORNECEDOR_REAL.json'
SPATH = F9 / 'spec/PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json'

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def pin(path):
    data = path.read_bytes()
    return dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))

def atomic(path, data):
    if path.exists():
        stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
        backup = path.with_name(path.name + '.bak_' + stamp)
        backup.write_bytes(path.read_bytes())
    temp = path.with_name(path.name + '.tmp')
    temp.write_bytes(data)
    assert temp.stat().st_size == len(data) > 0
    os.replace(temp, path)

def save(path, obj):
    atomic(path, (json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8'))

def main():
    qualification = read_json(QPATH)
    # Only law/constants/background fields are selected; no local H0 center is used.
    spec = read_json(SPATH)['spec']
    law = spec['lei']
    constants = spec['S5_propagacao']['constantes_E']
    theta = np.array(qualification['fundo']['bg1']['theta_H0_ombh2_omch2'], float)
    C = np.array(qualification['fundo']['bg1']['cov_theta'], float)
    assert np.allclose(C, C.T, rtol=0, atol=1e-18)
    C = (C + C.T) / 2
    H, wb, wc = theta
    ALPHA_FINE_CODATA_2018 = float(spec['beta']['alpha_read'])
    beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
    z = float(law['z_star'])
    h2 = (H / 100) ** 2
    omega_r = constants['og_coef'] * constants['TCMB'] ** 4 * (1 + constants['Neff'] * 7/8 * (4/11) ** (4/3))
    omega_nu = constants['mnu_eV'] / 93.14
    Om = (wb + wc + omega_nu) / h2
    Or = omega_r / h2
    A, B = (1+z)**3 - 1, (1+z)**4 - 1
    E2 = 1 + Om*A + Or*B
    lnE = math.log(E2) / 2
    grad_lnE = np.array([-(Om*A + Or*B)/(H*E2), A/(2*h2*E2), A/(2*h2*E2)])
    ln10 = math.log(10)
    gh = np.array([1/(H*ln10), 0, 0])
    gk = (2*beta/3/ln10)*grad_lnE
    gp = gh + gk
    K = float(law['K_frozen_V1'])
    K_theta = math.exp((2*beta/3)*lnE)
    logK = math.log10(K)
    gOm = np.array([-2*Om/H, 1/h2, 1/h2])
    gOr = np.array([-2*Or/H, 0, 0])
    gq = 1.5*gOm + 2*gOr
    gj = 2*gOr
    names = ['log10_H0', 'Omega_m', 'Omega_r', 'log10_K', 'q0_flat_LCDM_radiation', 'j0_flat_LCDM_radiation', 'log10_Hlocal']
    jac = np.array([gh, gOm, gOr, gk, gq, gj, gp])
    derived_cov = jac @ C @ jac.T
    derived_mean = [math.log10(H), Om, Or, logK, 1.5*Om+2*Or-1, 1+2*Or, math.log10(H)+logK]
    L = np.diag([1/(H*ln10), 1, 1])
    Linv = np.diag([H*ln10, 1, 1])
    Clog = L @ C @ L.T
    sd = np.sqrt(np.diag(C))
    corr = C/np.outer(sd,sd)
    historical = qualification['bancada_pins']
    comparisons = []
    for rel, expected in historical.items():
        current = pin(BANCADA / rel)
        comparisons.append(dict(relative_path=rel, qualified=expected, current=current,
                                identical=(expected['sha256'] == current['sha256'] and expected['bytes'] == current['bytes'])))
    loader = importlib.util.spec_from_file_location('f9v2_stats_bg1_audit', F9 / 'runner/f9v2_stats.py')
    module = importlib.util.module_from_spec(loader)
    loader.loader.exec_module(module)
    numeric_grad = np.array(module.grad_lnE(theta, z, constants))
    assert np.allclose(grad_lnE, numeric_grad, rtol=2e-8, atol=1e-11)
    expected = spec['S5_propagacao']['efeito_medido_no_fundo_real_de_qualificacao']
    linear_P_gradient = K*(np.array([1.,0,0]) + H*(2*beta/3)*grad_lnE)
    linear_P_variance = float(linear_P_gradient @ C @ linear_P_gradient)
    assert abs(linear_P_variance-expected['V_T_S5']) < 1e-9
    assert abs(K_theta-expected['K_no_theta_do_fundo']) < 1e-12
    assert np.linalg.matrix_rank(C) == 3
    np.linalg.cholesky(C)
    contract_path = ROOT / 'BANCADA_CONTRACT_HTTP.json'
    contract = read_json(contract_path) if contract_path.exists() else None
    if contract:
        assert contract['ok'] is True
        assert math.isclose(float(contract['alpha']), ALPHA_FINE_CODATA_2018, rel_tol=0, abs_tol=1e-16)
        assert math.isclose(float(contract['beta_tgl']), beta, rel_tol=0, abs_tol=1e-16)
    out = dict(
        schema='H0DN_BG1_BACKGROUND_v1', created_utc=datetime.now(timezone.utc).isoformat(),
        status='DERIVED_FROM_QUALIFIED_BG1_ARCHIVE_NOT_A_NEW_BACKGROUND_FIT',
        parameter_names=['H0','omega_b','omega_c'], parameter_units=['km/s/Mpc','dimensionless','dimensionless'],
        mean_parameters=theta.tolist(), covariance=C.tolist(), correlation=corr.tolist(),
        background_rank=3, H0=float(H), sigma_H0=float(sd[0]), K=K, logK=logK, log_base=10,
        gradient_h=gh.tolist(), gradient_k=gk.tolist(), gradient_h_plus_k=gp.tolist(),
        variance_h=float(gh@C@gh), variance_k=float(gk@C@gk), covariance_h_k=float(gh@C@gk),
        variance_h_plus_k=float(gp@C@gp),
        bg1_chi2=qualification['fundo']['bg1']['chi2'],
        r_d_Mpc=qualification['fundo']['r_d_modelo_no_BG1'],
        covariance_method='inverse(J_residual.T @ J_residual), unrescaled Gauss-Newton local Gaussian approximation',
        exact_observed_hessian=None,
        exact_observed_hessian_status='NOT_SAVED_IN_QUALIFICATION; Gauss-Newton omits sum residual_i Hessian(residual_i)',
        gauss_newton_precision=np.linalg.inv(C).tolist(),
        gaussian_log_parameterization=dict(parameter_names=['log10_H0','omega_b','omega_c'],
            mean_parameters=[math.log10(H),float(wb),float(wc)],covariance=Clog.tolist(),
            gradient_h=(gh@Linv).tolist(),gradient_k=(gk@Linv).tolist(),gradient_h_plus_k=(gp@Linv).tolist(),
            scope='First-order Gaussian approximation in log10 H0. Literal log of Gaussian H0 is a separate nonlinear sensitivity.'),
        derived=dict(names=names,mean=derived_mean,jacobian=jac.tolist(),covariance=derived_cov.tolist(),
            rank_maximum=3,scope='All derived from the same three background parameters; singularity is expected.'),
        law=dict(form='K=E(z_star)^(2 beta/3)',beta=beta,ALPHA_FINE_CODATA_2018=ALPHA_FINE_CODATA_2018,
            beta_rule='ALPHA_FINE_CODATA_2018 * sqrt(e), evaluated at runtime',z_star=z,
            constants_E={k:v for k,v in constants.items() if k != 'origem'},
            frozen_Omega_m=law['Omega_m'],frozen_Omega_r=law['Omega_r'],
            Omega_m_from_theta=Om,Omega_r_from_theta=Or,omega_nu=omega_nu,
            K_at_theta=K_theta,log10K_at_theta=math.log10(K_theta),
            center_difference_log10=math.log10(K_theta/K),center_difference_Hlocal=float((K_theta-K)*H),
            mean_convention='F9 frozen K; gradient is S5 local K(theta), an anchored local linearization, not strict constant K.',
            gradient_lnE=grad_lnE.tolist(),gradient_log10K_wrt_beta=(2/3)*lnE/ln10,
            gradient_log10K_wrt_zstar=(beta/3/ln10)*(3*Om*(1+z)**2+4*Or*(1+z)**3)/E2,
            strict_conditional_K=dict(gradient_k=[0,0,0],variance_h_plus_k=float(gh@C@gh),
                scope='Only if Omega_m and Omega_r of the law are explicitly fixed independently of theta; not historical S5.'),
            coherent_theta_mean=dict(K=K_theta,logK=math.log10(K_theta),scope='Diagnostic alternative mean, not chosen by observed local H0.')),
        fixed_parameters=['beta','z_star','TCMB','Neff','mnu_eV','og_coef','spatial_curvature=0'],
        fixed_parameter_covariances=None,
        fixed_parameter_covariance_status='No uncertainty assigned in original BG1/S5 contract; do not infer measured zero uncertainty.',
        cross_covariance_H0DN_background=None,
        cross_covariance_status='UNAVAILABLE. Zero cross-block is an explicit conditional independence assumption for injections, not a measurement.',
        q0_j0_scope='H0DN upstream fixed q0,j0 are not re-fitted. Derived BG q0,j0 are diagnostics; no cross-block or estimator response is available to identify the two cosmologies.',
        fit_domain=dict(parameter_names=['H0','omega_b','omega_c'],lower=[60,.019,.08],upper=[80,.026,.16],
            scope='Historical least_squares support. Nonlinear draws outside support must be counted/rejected visibly, never silently clipped.'),
        primary_score=dict(t='hhat_local-log10Hbg',null_mean=0,alternative_mean=logK,
            variance='Var(hhat_local)+variance_h-2 Cov(hhat_local,log10Hbg)',
            conditional_independence_variance='Var(hhat_local)+variance_h',one_sided_cut_sigma=5,
            meaning='Detection against no shift. This does not establish specificity to TGL.'),
        tgl_consistency_score=dict(residual='hhat_local-log10Hbg-log10K',
            variance='Var(hhat_local)+variance_h_plus_k-2 Cov(hhat_local,log10Hbg+log10K)',
            meaning='Separate consistency check; do not use this denominator for primary null-zero detection.'),
        live_contract=dict(verified=bool(contract),deployment_id=contract.get('deployment_id') if contract else None,
            canonical_version=contract.get('canonical_version') if contract else None,
            receipt=str(contract_path) if contract else None),
        background_provider_current_pin_comparison=comparisons,
        all_background_provider_pins_equal_qualification=all(x['identical'] for x in comparisons),
        scope='Restored historical Planck compressed Chen+2019 plus DESI DR2 background, beta_background=0. Analytic covariance propagation re-executed. No local H0 centers, Motor constructor, API avaliar, optimization, um.py, Lean, installation or restart.',
        limitations=['Not an exact likelihood/posterior Hessian or a fresh BG fit.',
            'Statistical independence across local and background datasets is assumed only in synthetic injections; common systematics not quantified.',
            'Historical S5 fixes z_star and does not propagate recombination-redshift dependence.',
            'The E(z) prescription is the historical F9 approximation; this does not establish a self-consistent TGL background plus H0DN low-z model.'])
    save(ROOT/'BG1.json',out)
    checks=dict(status='PASS_WITH_SCOPE',cholesky_positive=True,background_rank=3,
        analytic_grad_lnE=grad_lnE.tolist(),numeric_grad_lnE=numeric_grad.tolist(),
        max_gradient_absolute_difference=float(np.max(np.abs(grad_lnE-numeric_grad))),
        S5_linear_Hlocal_variance=linear_P_variance,S5_expected_variance=expected['V_T_S5'],
        K_theta_difference=float(K_theta-expected['K_no_theta_do_fundo']),
        log_variance_joint_identity_residual=float(gp@C@gp-(gh@C@gh+gk@C@gk+2*gh@C@gk)),
        all_background_provider_pins_equal_qualification=out['all_background_provider_pins_equal_qualification'],
        live_contract_verified=bool(contract),local_H0_centers_used=False,new_background_fit=False)
    save(ROOT/'VALIDATION.json',checks)
    sources=[QPATH,SPATH,F9/'runner/f9v2_background.py',F9/'runner/f9v2_stats.py',
        BANCADA/'um_bancada.py',BANCADA/'bancada/evidencia.py',BANCADA/'canonical_contracts.json',Path(__file__)]
    if contract_path.exists(): sources.append(contract_path)
    save(ROOT/'SOURCE_PINS.json',dict(sources=[pin(p) for p in sources],
        qualified_background_provenance=comparisons,authority='Hashes identify bytes, not mathematical or empirical validation.'))
    print(json.dumps({k:out[k] for k in ['H0','sigma_H0','K','logK','gradient_h','gradient_k','variance_h','variance_h_plus_k','all_background_provider_pins_equal_qualification']},indent=2))

if __name__ == '__main__':
    main()
