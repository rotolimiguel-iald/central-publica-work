"""Frozen linear estimator of centered synthetic H0DN and BG1 vectors.
v411 amendment: evaluate() no longer raises data_outside_support; the projection on the
covariance null space is only reported (support_max_abs, support_l2). geometry() is unchanged.

Inputs contain known noise geometry, never an observed local H0 fit.
The baseline parameter vector is translated to zero without loss for GLS.
"""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
from scipy import linalg


def pin(path):
    path = Path(path)
    return {'path': str(path.resolve()), 'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def geometry(A, C, c, h_index):
    A, C, c = np.asarray(A, float), np.asarray(C, float), np.asarray(c, float)
    n, p = A.shape
    if C.shape != (n,n) or c.shape != (n,): raise ValueError('shape_mismatch')
    if not all(np.isfinite(x).all() for x in (A,C,c)): raise ValueError('nonfinite')
    if np.max(np.abs(C-C.T)) > 1e-12 * max(1., np.max(np.abs(C))):
        raise ValueError('asymmetric_covariance')
    vals, U = linalg.eigh((C+C.T)/2)
    tol = 64*np.finfo(float).eps*n*vals[-1]
    if vals[0] < -tol: raise ValueError('covariance_not_psd')
    keep=vals>tol
    if not keep.any(): raise ValueError('empty_support')
    if np.min(vals[keep]) < 100*tol: raise ValueError('ambiguous_rank')
    null=U[:,~keep]
    ext=np.column_stack([A,c])
    support_error=float(np.linalg.norm(null.T @ ext) / max(1.,np.linalg.norm(ext)))
    if support_error>1e-10: raise ValueError('deterministic_constraints_in_design_not_handled')
    W=U[:,keep].T/np.sqrt(vals[keep])[:,None]
    result={}
    for name, design in [('published_baseline',A),('free_cepheid_host_differential_bias',ext)]:
        Aw=W@design
        Ua, sv, Va = linalg.svd(Aw,full_matrices=False)
        if sv[-1] <= max(Aw.shape)*np.finfo(float).eps*sv[0]*64:
            raise ValueError('unidentified_design:'+name)
        invA=(Va.T/sv)@Ua.T
        influence=invA[h_index]@W
        expected=np.zeros(design.shape[1]);expected[h_index]=1
        err=float(np.max(np.abs(influence@design-expected)))
        if err>1e-9: raise ValueError('influence_unbiasedness_failed')
        variance=float(influence@C@influence)
        result[name]={'influence':influence,'variance_h':variance,
                      'response_cepheid':float(influence@c),'design_rank':len(sv),
                      'condition_design_whitened':float(sv[0]/sv[-1]),
                      'influence_identity_error':err}
    metadata={'n':n,'p':p,'cov_rank':int(keep.sum()),'cov_nullity':int((~keep).sum()),
              'eig_min':float(vals[0]),'eig_min_positive':float(vals[keep].min()),
              'eig_max':float(vals[-1]),'tolerance':float(tol),'support_design_error':support_error}
    return result,metadata,null


def evaluate(data, estimator):
    """No access to labels. data: local centered rows, BG centered parameters.
    v411: the null-space projection is a diagnostic only (no guard)."""
    local=np.asarray(data['local']);bg=np.asarray(data['background'])
    null=estimator['null_basis']; weights=estimator['weights']
    if local.ndim!=2 or bg.ndim!=2 or local.shape[0]!=bg.shape[0]: raise ValueError('shape')
    if weights.ndim!=2 or local.shape[1]!=weights.shape[1] or null.shape[0]!=local.shape[1]: raise ValueError('local_dimension')
    if bg.shape[1]!=len(estimator['gradient_h']) or estimator['gradient_k'].shape!=estimator['gradient_h'].shape: raise ValueError('background_dimension')
    if estimator['sd_null'].shape!=(weights.shape[0],) or estimator['sd_tgl'].shape!=(weights.shape[0],): raise ValueError('scale_dimension')
    if local.shape[0]==0: raise ValueError('empty_sample')
    numeric=[local,bg,null,weights,estimator['gradient_h'],estimator['gradient_k'],estimator['sd_null'],estimator['sd_tgl'],estimator['logK'],estimator['H0']]
    if not all(np.isfinite(x).all() for x in numeric): raise ValueError('nonfinite_input')
    if np.any(estimator['sd_null']<=0) or np.any(estimator['sd_tgl']<=0): raise ValueError('nonpositive_scale')
    support_error=float(np.max(np.abs(local@null))) if null.shape[1] else 0.
    support_l2=np.linalg.norm(local@null,axis=1) if null.shape[1] else np.zeros(local.shape[0])  # v411: diagnostic, no guard
    h = local@weights.T
    bh = bg@estimator['gradient_h']
    bk = bg@estimator['gradient_k']
    t = h-bh[:,None]
    z = t/estimator['sd_null']
    ztgl=(t-float(estimator['logK'])-bk[:,None])/estimator['sd_tgl']
    H0=float(estimator['H0'])
    if np.any(H0+bg[:,0]<=0): raise ValueError('nonpositive_background_H0')
    bh_exact=np.log10(H0+bg[:,0])-np.log10(H0)
    z_exact=(h-bh_exact[:,None])/estimator['sd_null']
    return {'t':t,'z_null':z,'z_tgl':ztgl,'z_null_exact_bg':z_exact,
            'support_max_abs':np.array(support_error),'support_l2':support_l2}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--estimator',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists(): raise FileExistsError(args.output)
    with np.load(args.input,allow_pickle=False) as data, np.load(args.estimator,allow_pickle=False) as est:
        out=evaluate(data,est)
    with args.output.open('xb') as f: np.savez_compressed(f,**out)
    print(json.dumps(pin(args.output)))


if __name__=='__main__': main()
