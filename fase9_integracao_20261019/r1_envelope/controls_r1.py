"""Only new exact synthetic controls for the analytic envelope, no centers."""
from fractions import Fraction as F
from covariance_envelope_r1 import fixed_contrast_envelope as bound
from covariance_envelope_r1 import mean_minimax_design as design
from covariance_envelope_r1 import quadratic, EnvelopeError


def run():
    checks=[]
    def record(name, condition, **details):
        assert condition, name
        checks.append({"name":name,"passed":True,**details})
    for name,w,s,expected in [
        ("positive_weights_rank_one_sharp",[F(1,2),F(1,2)],[1,2],F(9,4)),
        ("negative_weights_rank_one_sharp",[2,-1],[1,2],F(16)),
        ("zero_contrast",[0,0],[1,2],F(0))]:
        r=bound(w,s)
        record(name,r['variance_bound']==expected==quadratic(w,r['attaining_covariance']),value=str(expected))
    r=design([1,2,3]); C=r['oracle_gls_worst_covariance']
    weights=[[1,0,0],[0,1,0],[0,0,1],[F(1,3)]*3,[2,-1,0],[F(1,2),F(1,2),0]]
    record("minimax_witness_factorization",all(
        quadratic(w,C)==F(1)+3*F(w[1])**2+8*F(w[2])**2>=1 for w in weights)
        and r['weights']==[1,0,0] and quadratic(r['weights'],C)==1)
    r=design([1,1,3])
    record("tied_minimum_singular_witness",r['selected_index']==0 and
        quadratic([F(1,2),F(1,2),0],r['oracle_gls_worst_covariance'])==1)
    w=[F(4,5),F(1,5)]
    record("stale_covariance_gls_is_not_oracle",quadratic(w,[[1,0],[0,4]])==F(4,5)
           and bound(w,[1,2])['variance_bound']==F(36,25)>1,
           meaning="Frozen weights from diagonal C can exceed sigma_min squared under another allowed C")
    allcorr=bound([1,-F(3,2)],[1,F(1,4)])['variance_bound']
    independent=F(1)+F(9,4)*F(1,16)
    record("background_cross_covariance_changes_bound",allcorr==F(121,64)>independent==F(73,64),
           joint=str(allcorr),independent_background=str(independent))
    # An understated diagonal falls outside the envelope assumptions.
    record("wrong_total_variance_invalidates_assumption",quadratic([1,0],[[4,0],[0,9]])>
           bound([1,0],[1,2])['variance_bound'],not_a_counterexample_within_hypotheses=True)
    # Both distributions can have variance one; a variance bound alone is not
    # a Gaussian 5-sigma tail. Synthetic three-point law, no data interpretation.
    record("variance_does_not_calibrate_tail",F(1,50)*25+F(1,50)*25==1 and F(1,50)*2==F(1,25),
           mass_at_minus5="1/50",mass_at_plus5="1/50",mass_at_zero="24/25")
    invalid=[("nan",[float('nan')],[1]),("bool",[True],[1]),
             ("zero_sigma",[1],[0]),("dimension",[1],[1,2])]
    for name,w,s in invalid:
        try:bound(w,s)
        except EnvelopeError as exc:record('refuse_'+name,True,message=str(exc))
        else:raise AssertionError('should refuse '+name)
    return {"passed":True,"checks":checks,"count":len(checks),
            "status":"EXACT_SYNTHETIC_ALGEBRA_CHECKED_ANALYTIC_PROOF_SEPARATE",
            "R1_physical_status":"OPEN","observed_centers_used":False,
            "beta_used_in_exact_controls":False,"observed_sigma_estimate":False}
