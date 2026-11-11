"""Independent covariance-only audit. Does not open blind injections or labels."""
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
BASE = HERE.parent

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def digest(data):
    return hashlib.sha256(data).hexdigest()

def pin(path):
    data = path.read_bytes()
    return {'path':str(path),'bytes':len(data),'sha256':digest(data)}

def write_new(path,value):
    data=(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    with path.open('xb') as stream:
        stream.write(data)
    assert path.read_bytes()==data

def main():
    design_path=BASE/'DESIGN_MARGINS.json'
    spec_path=BASE/'PROSPECTIVE_GEOMETRY.json'
    bg_path=HERE/'BG1.json'
    net_path=BASE/'network/network.npz'
    design,spec,bg=load(design_path),load(spec_path),load(bg_path)
    with np.load(net_path) as arrays:
        covariance=arrays['parameter_covariance_free_cepheid'].copy()
        h_index=int(arrays['h_index'])
    np.linalg.cholesky(covariance)
    vh,vc,hc=covariance[h_index,h_index],covariance[-1,-1],covariance[h_index,-1]
    d,vb=float(spec['logK']),float(spec['background_variance_logH'])
    assert d==bg['logK'] and vb==bg['variance_h']
    assert abs(hc-design['cov_h_cepheid_bias'])<1e-15
    precision=np.linalg.inv(covariance)
    base_sd=math.sqrt(vh)
    D=d/math.sqrt(vh+vb)
    minimum_vh=vh-hc*hc/vc
    rows=[]
    for target in design['targets']:
        power=float(target['target_power'])
        needed_D=5-float(norm.isf(1-power))
        # Independently use the quantile of the alternative-score exceedance.
        needed_D=5+float(norm.ppf(power))
        allowed_variance=(d/needed_D)**2-vb
        reduction=1-math.sqrt(allowed_variance)/base_sd
        assert abs(needed_D-target['target_D'])<1e-14
        assert abs(math.sqrt(allowed_variance)-target['maximum_sigma_logH_network'])<1e-14
        assert abs(reduction-target['sigma_reduction_from_free_cepheid_fraction'])<1e-14
        attainable=allowed_variance>=minimum_vh
        if allowed_variance>=vh:
            prior_sd=None
            updated_var=vh
            comparison='No additional independent constraint needed for this target.'
        else:
            assert attainable
            prior_var=hc*hc/(vh-allowed_variance)-vc
            assert prior_var>0
            prior_sd=math.sqrt(prior_var)
            augmented=precision.copy()
            augmented[-1,-1]+=1/prior_var
            # Full 65-parameter precision update, independent of scalar formula.
            updated=np.linalg.inv(augmented)
            updated_var=float(updated[h_index,h_index])
            assert abs(updated_var-allowed_variance)<1e-13
            assert abs(prior_sd-target['independent_external_cepheid_bias_constraint_sd_mag'])<1e-13
            comparison='Full precision update agrees with scalar Sherman-Morrison identity.'
        rows.append(dict(target_power=power,target_D=needed_D,attainable=bool(attainable),
            maximum_network_variance=allowed_variance,maximum_network_sigma=math.sqrt(allowed_variance),
            required_sigma_reduction_fraction=reduction,external_prior_sd_mag=prior_sd,
            full_precision_update_variance=float(updated_var),
            achieved_power=float(norm.sf(5-d/math.sqrt(updated_var+vb))),check=comparison))
    raw_margin=(d/5)**2-vh-vb
    assert raw_margin>0
    margin=math.sqrt(raw_margin)
    assert abs(margin-design['remaining_additive_common_logH_noise_sd_for_median_5sigma'])<1e-15
    assert abs(math.log(10)*margin-design['equivalent_fractional_H_noise'])<1e-15
    assert abs(bg['K']*bg['H0']*math.log(10)*margin-design['equivalent_H_noise_at_TGL_mean'])<1e-13
    sources=[design_path,BASE/'design_margins.py',spec_path,bg_path,net_path,Path(__file__)]
    report=dict(status='PASS_WITH_SCOPE',created_utc=datetime.now(timezone.utc).isoformat(),
        reviewer='parent-delegated ponte_formal; independent covariance reconstruction',
        inputs_read=[pin(path) for path in sources],blind_directories_read=False,blind_labels_read=False,
        equations=dict(prior='C_new = C - C[:,c] C[c,:] / (C[c,c]+tau^2)',
            variance='Vh_new = Vh - Cov(h,c)^2/(Vc+tau^2)',
            solved_prior='tau^2 = Cov(h,c)^2/(Vh-Vh_target)-Vc',
            power='P(Z>5|mean=D,variance=1)=Phi(D-5)',
            needed_D='5+Phi_inverse(power)',
            target_network_variance='(log10K/needed_D)^2 - Vbackground',
            additive_common_noise='sigma_extra^2=(log10K/5)^2-Vh-Vbackground'),
        covariance_shape=list(covariance.shape),base_D=float(D),base_power=float(norm.sf(5-D)),
        network_sigma=float(base_sd),minimum_network_variance_with_exact_c=float(minimum_vh),
        maximum_power_with_exact_c=float(norm.sf(5-d/math.sqrt(minimum_vh+vb))),
        targets=rows,remaining_additive_common_noise_variance=float(raw_margin),
        remaining_additive_common_noise_sd=float(margin),
        assumptions=['Local Gaussian linear model and fixed covariance.',
            'New Gaussian constraint on c is independent of all network/background information and has a correctly specified unbiased mean.',
            'Vbackground and log10K retain the frozen convention; cross-block zero is an explicit assumption.',
            'The extra common-noise margin is independent additive noise, not permission for an unmodelled bias.',
            'Fractional-H and km/s/Mpc equivalents use first-order log linearization.'],
        interpretation='90% and 95% require sigma reductions 16.9149345% and 22.0843546%; an external independent c constraint would need sd at most 0.01826515 and 0.008919802 mag respectively.',
        low_note='At 50%, negative sigma_reduction is allowable slack (~6.9% sigma increase), not a required improvement. Null external prior means no new constraint needed, not a zero-width prior.',
        empirical_scope='Prospective design calculations only. Does not validate H0DN data/model, common systematics, or observed five-sigma evidence.')
    write_new(HERE/'MARGINS_REVIEW.json',report)

    frozen=load(BASE/'FREEZE.json')
    frozen_rows={Path(row['path'].replace('\\\\','\\')).name:row for row in frozen['files']}
    backup=next(HERE.glob('BG1.json.bak_*'))
    old,new=load(backup),load(bg_path)
    changed=[key for key in old if old[key]!=new[key]]
    assert changed==['created_utc']
    assert digest(backup.read_bytes())==frozen_rows['BG1.json']['sha256']
    script=(HERE/'build_bg1.py').read_bytes()
    reconstructed=script.replace(b'import sys\n',b'',1).replace(b'\nsys.dont_write_bytecode = True\n',b'',1)
    reconstruction_matches=digest(reconstructed)==frozen_rows['build_bg1.py']['sha256']
    assert reconstruction_matches
    event=dict(status='VERIFIED_POST_FREEZE_BYTE_CHANGE_WITH_NUMERIC_IDENTITY',
        created_utc=datetime.now(timezone.utc).isoformat(),
        explanation='After the first build, added import sys and sys.dont_write_bytecode=True to prevent importlib from writing bytecode caches; reran build_bg1.py to pin the final script and regenerate receipts. Parent freeze occurred between those two builds; it was not synchronized with this finalization.',
        affected_frozen_files=['background/BG1.json','background/build_bg1.py'],
        bg1_changed_fields=[dict(field='created_utc',before=old['created_utc'],after=new['created_utc'])],
        other_bg1_fields_exactly_equal=True,
        script_exact_delta=['+ import sys','+ sys.dont_write_bytecode = True'],
        script_old_bytes_reconstructed_sha256=digest(reconstructed),
        reconstruction_matches_original_freeze=reconstruction_matches,
        old_bg1_source=pin(backup),current_bg1=pin(bg_path),current_script=pin(HERE/'build_bg1.py'),
        original_freeze=pin(BASE/'FREEZE.json'),
        additional_outputs_regenerated=['SOURCE_PINS.json (script pin changed)','VALIDATION.json (unchanged scientific values)'],
        no_blind_data_or_labels_accessed_by_this_agent=True,
        seed_or_injection_status='Parent and blind custodian reported no seed/injection generated before refusal; not independently inspected here.',
        recovery='Preserve original FREEZE and emit superseding FREEZE_R2 after parent review. This receipt does not modify any frozen input.',
        frozen_inputs_locked=True)
    write_new(HERE/'POST_FREEZE_CHANGE.json',event)
    print(json.dumps({'margins_review':report['status'],'base_D':D,'base_power':report['base_power'],
        'targets':rows,'post_freeze_change_verified':reconstruction_matches},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
