"""Read metadata/errors/covariances only; no observed centers or fits."""
from pathlib import Path
import json, hashlib, io, re
import numpy as np
import pandas as pd
from scipy import linalg

B = Path(__file__).resolve().parent
N = B.parent / 'network'
D = N / 'upstream/data'
PP = Path('C:/IALD/observaveis_tgl/tgl_data_cache/pantheon/Pantheon+SH0ES.dat')
PC = Path('C:/IALD/projetos_pyhton/acom/tgl_data_cache/pantheon_covariance.dat')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(name, obj):
    p = B / name
    temp = p.with_name(p.name + '.tmp')
    temp.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    temp.replace(p)

def stats(a):
    a = np.asarray(a)
    return dict(min=float(np.min(a)), median=float(np.median(a)), max=float(np.max(a)))

def envelope():
    z=np.load(N/'network.npz',allow_pickle=False)
    rows=json.loads((N/'rows.json').read_text('utf-8'))
    A,C,c,h=z['A'],z['C'],z['c_cepheid'],int(z['h_index'])
    ci=np.array([r['row'] for r in rows if r.get('kind')=='sn1a_calibrator'])
    hi=next(r['row'] for r in rows if r.get('kind')=='sn1a_hubble_flow')
    block=np.append(ci,hi)
    sigma=np.sqrt(C.diagonal()[block])
    out=[]
    precision=linalg.pinvh(C,atol=1e-10,rtol=0)
    for free_bias in [False,True]:
        design=np.column_stack([A,c]) if free_bias else A
        v=linalg.inv(design.T@precision@design)
        weight=v[h,:]@design.T@precision
        assert np.allclose(weight@design,np.eye(design.shape[1])[h,:],atol=1e-10)
        baseline=float(weight@C@weight)
        vcal=float(np.sum((weight[ci]*np.sqrt(C.diagonal()[ci]))**2))
        vhf=float(weight[hi]**2*C[hi,hi])
        outer=baseline-vcal-vhf
        coeff=np.abs(weight[block])*sigma
        max_b=float(coeff.sum()**2)
        min_b=float(max(2*coeff.max()-coeff.sum(),0)**2)
        record={'free_cepheid_bias':free_bias,'baseline_sigma_log10H0':baseline**.5,
                'variance_calibrators':vcal,'variance_HF_intercept':vhf,'variance_other_blocks':outer,
                'cross_only_sigma_min':float(np.sqrt(baseline-2*np.sqrt(vcal*vhf))),
                'cross_only_sigma_max':float(np.sqrt(baseline+2*np.sqrt(vcal*vhf))),
                'calibration_plus_cross_sigma_min':float(np.sqrt(outer+min_b)),
                'calibration_plus_cross_sigma_max':float(np.sqrt(outer+max_b)),
                'definition':'Exact bounds for unchanged baseline unbiased linear estimator; fixed block diagonals, all outside blocks preserved and independent. Not an estimated physical correlation or GLS minimax bound.',
                'scenarios':[]}
        signed=sigma*np.sign(weight[block])
        for rho in [0.,.1,.25,.5,.75,.95,.999]:
            trial=C.copy()
            trial[np.ix_(block,block)]=(1-rho)*np.diag(sigma**2)+rho*np.outer(signed,signed)
            evals,evecs=linalg.eigh(trial)
            assert evals[0]>-1e-10
            support=evals>1e-10
            assert np.max(np.abs(evecs[:,~support].T@design))<1e-9
            W=(evecs[:,support]/np.sqrt(evals[support])).T
            _,s,vt=linalg.svd(W@design,full_matrices=False)
            vnew=(vt.T/s**2)@vt
            record['scenarios'].append({'rho':rho,'fixed_estimator_sigma':float(np.sqrt(weight@trial@weight)),
                         'reoptimized_GLS_sigma':float(np.sqrt(vnew[h,h])), 'rank_C':int(support.sum()),
                         'min_eigenvalue':float(evals[0])})
        out.append(record)
    save('PSD_ENVELOPE.json',{'status':'DERIVED_SENSITIVITY_NOT_NEW_MEASURED_COVARIANCE','block_rows':block.tolist(),
          'block_definition':'55 SN Ia calibrators and one compressed SN Ia HF intercept; diagonal fixed',
          'formulas':{'cross_only':'Var=LCL +/- 2 sqrt(vcal*vhf), ||D_cal^(-1/2) X / sigma_hf||<=1',
                       'all_in_block_max':'Var_other + (sum_i |l_i| sigma_i)^2',
                       'all_in_block_min':'Var_other + max(2 max_i |l_i| sigma_i - sum_i |l_i| sigma_i,0)^2',
                       'scenario':'C_block(rho)=(1-rho)diag(sigma^2)+rho ss^T, s_i=sigma_i sign(l_i)'},
          'results':out})
    return out

def main():
    # Deliberate usecols excludes all magnitude/modulus centers.
    pp = pd.read_csv(PP, sep=r'\s+', usecols=['CID', 'IDSURVEY', 'zCMB', 'zHEL', 'VPEC', 'VPECERR',
          'IS_CALIBRATOR', 'USED_IN_SH0ES_HF', 'm_b_corr_err_DIAG', 'm_b_corr_err_RAW', 'm_b_corr_err_VPEC'], dtype={'CID':str})
    hf = pd.read_csv(D / 'sn1a_hf_pp.dat', sep=r'\s+', comment='#', header=None,
           usecols=[0, 2, 3, 4, 5, 6, 7, 8], names=['CID','err','zhel','zcmb','vp','vp_2mpp_sdss_6df','vp_2mrs','vp_2mpp'])
    cal = pd.read_csv(D / 'sn1a_calib.dat', sep=r'\s+', comment='#', header=None,
           usecols=[0,1,2,4], names=['number','host','CID','sigma'], dtype={'CID':str})
    local_hf = np.loadtxt(D / 'sn1a_covar_pp.dat')[1:].reshape(len(hf),len(hf))
    raw = np.loadtxt(PC)
    n = int(raw[0]); full = raw[1:].reshape(n,n)
    assert n == len(pp) == 1701
    full = .5 * (full + full.T)
    flag = pp.USED_IN_SH0ES_HF.to_numpy() == 1
    match = pp.loc[flag]
    ids_equal = list(hf.CID) == list(match.CID)
    comparison = {'same_HF_ID_order':ids_equal,'hf_rows':len(hf),'hf_unique':int(hf.CID.nunique()),'pp_hf_rows':int(flag.sum())}
    if ids_equal:
        ix = np.where(flag)[0]
        release_hf = full[np.ix_(ix,ix)]
        comparison.update(hf_cov_max_abs_difference=float(np.max(np.abs(local_hf-release_hf))),
               hf_cov_diagonal_ratio=stats(np.diag(local_hf)/np.diag(release_hf)),
               hf_err_DIAG_max_abs=float(np.max(np.abs(hf.err.to_numpy()-match.m_b_corr_err_DIAG.to_numpy()))),
               hf_err_RAW_max_abs=float(np.max(np.abs(hf.err.to_numpy()-match.m_b_corr_err_RAW.to_numpy()))),
               hf_zhel_max_abs=float(np.max(np.abs(hf.zhel.to_numpy()-match.zHEL.to_numpy()))),
               hf_zcmb_max_abs=float(np.max(np.abs(hf.zcmb.to_numpy()-match.zCMB.to_numpy()))),
               hf_vp_selected_vs_release_max_abs=float(np.max(np.abs(hf.vp_2mpp.to_numpy()-match.VPEC.to_numpy()))))
        # Covariance-only compression matching upstream, no magnitude input.
        c_light=299792.458
        zpec=np.sqrt((1+hf.vp_2mpp.to_numpy()/c_light)/(1-hf.vp_2mpp.to_numpy()/c_light))-1
        zcorr=(1+hf.zcmb.to_numpy())/(1+zpec)-1
        vcorr=c_light*((1+zcorr)**2-1)/((1+zcorr)**2+1)
        velocity_var=(np.log10(vcorr+240)-np.log10(vcorr))**2
        alpha_cov=local_hf/25+np.diag(velocity_var)
        numerator=linalg.solve(alpha_cov,np.ones(len(hf)),assume_a='pos')
        weights=numerator/numerator.sum()
        alpha_var=float(1/numerator.sum())
        # alpha = constant - 0.2 weights @ magnitude; this cross vector is
        # valid only for raw P+ light curves, NOT H0DN aggregate calibrators.
        raw_cross=-.2*full[:,ix]@weights
        np.savez_compressed(B/'raw_cross_diagnostic.npz',hf_pp_indices=ix,weights=weights,
                             raw_pp_to_alpha_covariance=raw_cross,alpha_variance=np.array(alpha_var))
        comparison['compressed_alpha_variance']=alpha_var
        comparison['H0DN_additional_velocity_variance_range']=stats(velocity_var)
        comparison['release_VPEC_error_mag_range']=stats(match.m_b_corr_err_VPEC.to_numpy())
    pp_norm = pp.CID.astype(str).str.lower()
    mapping=[]
    for row in cal.itertuples():
        indices=np.where(pp_norm.to_numpy() == row.CID.lower())[0]
        mapping.append({'host':row.host,'CID':row.CID,'cal_sigma':float(row.sigma),'pp_indices':indices.tolist(),
                        'pp_surveys':pp.iloc[indices].IDSURVEY.astype(int).tolist(),
                        'pp_IS_CALIBRATOR':pp.iloc[indices].IS_CALIBRATOR.astype(int).tolist(),
                        'pp_cov_diagonal_sigma':np.sqrt(np.diag(full)[indices]).tolist(),
                        'pp_DIAG_errors':pp.iloc[indices].m_b_corr_err_DIAG.to_numpy().tolist(),
                        'pp_RAW_errors':pp.iloc[indices].m_b_corr_err_RAW.to_numpy().tolist()})
    count={str(k):sum(len(x['pp_indices']) == k for x in mapping) for k in range(6)}
    singles=[x for x in mapping if len(x['pp_indices'])==1]
    matched_indices=np.array(sorted({i for x in mapping for i in x['pp_indices']}))
    raw_correlation=full[np.ix_(matched_indices,matched_indices)]/np.sqrt(np.outer(full.diagonal()[matched_indices],full.diagonal()[matched_indices]))
    raw_offdiag=raw_correlation[~np.eye(len(matched_indices),dtype=bool)]
    sensitivity=envelope()
    summary={'comparison':comparison, 'calibrators':{'count':len(cal),'unique':int(cal.CID.nunique()),
                'matching_multiplicity':count,'exact_matched_light_curves':len(matched_indices),
                'absent_IDs':[x['CID'] for x in mapping if not x['pp_indices']],
                'unverified_near_ID_candidates':{'2008fv':'2008fv_comb','1994D':'1994DRichmond'},
                'singletons_release_sigma_over_cal_sigma':stats([x['pp_cov_diagonal_sigma'][0]/x['cal_sigma'] for x in singles]),
                'matched_raw_light_curve_corr_offdiagonal':stats(raw_offdiag),
                'matched_raw_cross_alpha_corr':stats(raw_cross[matched_indices]/np.sqrt(full.diagonal()[matched_indices]*alpha_var))},
             'no_center_columns_read':True,'no_fit':True,
             'bridge_status':'OPEN_NO_TRANSPLANT: aggregate-to-lightcurve map/weights missing; unverified aliases and absent calibrators; split of Cepheid covariance from SN covariance missing',
             'covariance_complete_claim':'REJECTED: H0DN baseline is complete only for its published block-diagonal model; cross-rung and calibrator offdiagonals remain absent.',
             'additional_guard':'HF submatrix already derives from full P+ covariance; upstream adds its own velocity variance. A component-level audit is required before changing or adding velocity terms.',
             'envelope_sigma_max_with_calibrator_and_cross_correlations':[x['calibration_plus_cross_sigma_max'] for x in sensitivity],
             'sources':{str(p):sha(p) for p in [PP,PC,D/'sn1a_hf_pp.dat',D/'sn1a_covar_pp.dat',D/'sn1a_calib.dat',N/'network.npz',N/'MANIFEST.json',Path(__file__)]}}
    save('mapping.json',mapping)
    save('AUDIT.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
