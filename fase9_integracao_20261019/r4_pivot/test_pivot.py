"""Deterministic synthetic laws and refusals; no observational centres or MC."""
import copy
import math
import unittest
from fixed_background_pivot import qualify,design_power,family_adjust,digest,PivotError


def model(factor=1.,cross=None):
    d=[0.,0.] if cross is None else cross
    C=[[1.,0.],[0.,1.]];s2=.5
    return dict(id='synthetic-contrast',route_id='R4_PIVOT_CANDIDATE',scenario_id='s1',test_id='lcdm_upper',
                mode='SYNTHETIC_ONLY',distribution='JOINT_GAUSSIAN_FIXED_UNKNOWN_H0_KNOWN_ERRORS',
                factor=factor,weights_rule='FIXED_GLS_C',C=C,background_variance=s2,cross_covariance=d,
                cross_covariance_source='EXPLICIT_SYNTHETIC_INPUT_NOT_MEASURED',fixed_before_centres=True,
                tail='upper',matrix_sha256=digest([C[0]+[d[0]],C[1]+[d[1]],d+[s2]]))


def repin(m):
    d=m['cross_covariance'];m['matrix_sha256']=digest([row+[d[i]] for i,row in enumerate(m['C'])]+[d+[m['background_variance']]])
    return m


def multiplicity():
    return dict(id='synthetic-two-tests',route_id='R4_PIVOT_CANDIDATE',method='bonferroni',
                test_ids=['lcdm_upper','tgl_compat'],scenario_ids=['s1'],scope='SYNTHETIC_CANDIDATE_NOT_ADOPTED_F9')


class PivotTests(unittest.TestCase):
    def test_known_five_sigma_tail(self):
        r=qualify(model(),[8.,8.],3.)
        self.assertEqual(r['variance'],1.)
        self.assertEqual(r['z_pivot'],5.)
        self.assertAlmostEqual(r['p'],2.866515718791946e-7,delta=1e-20)

    def test_H0_fixed_unknown_cancels(self):
        for h in [-100.,0.,68.,1e12]:
            r=qualify(model(),[h+5,h+5],h)
            self.assertEqual(r['z_pivot'],5.)

    def test_TGL_factor_cancels_nuisance(self):
        for h in [0.,2.,1000.]:
            r=qualify(model(factor=1.25),[1.25*h+2,1.25*h+2],h)
            self.assertEqual(r['contrast'],2.)

    def test_cross_covariance_changes_variance(self):
        self.assertAlmostEqual(qualify(model(cross=[.1,.2]),[8.,8.],3.)['variance'],.7)
        self.assertAlmostEqual(qualify(model(cross=[-.1,-.2]),[8.,8.],3.)['variance'],1.3)

    def test_background_shift_not_nuisance_symmetry_when_y_unshifted(self):
        self.assertNotEqual(qualify(model(),[8.,8.],3.)['z_pivot'],qualify(model(),[8.,8.],4.)['z_pivot'])

    def test_gls_unequal_errors_weights_exact(self):
        m=model();m['C']=[[1.,0.],[0.,4.]];repin(m)
        r=qualify(m,[5.,5.],0.)
        self.assertEqual(r['weights_exact'],[[4,5],[1,5]])
        self.assertAlmostEqual(r['variance'],1.3)

    def test_explicit_rational_weights_and_negative_allowed(self):
        m=model();m['weights_rule']='EXPLICIT_NORMALIZED_RATIONAL';m['weights']=[[1,3],[2,3]]
        r=qualify(m,[3.,3.],0.);self.assertEqual(r['contrast'],3.)
        m['weights']=[[2,1],[-1,1]];r=qualify(m,[3.,3.],0.)
        self.assertEqual(r['variance'],5.5)

    def test_mean_and_variance_analytic_matrix(self):
        m=model(cross=[.1,.2]);r=qualify(m,[0.,0.],0.)
        # l=(.5,.5,-1), direct six cross/diagonal terms.
        direct=.25+.25+.5-2*.5*.1-2*.5*.2
        self.assertAlmostEqual(r['variance'],direct)
        self.assertEqual(.5*7+.5*7-7,0.)

    def test_two_sided_compatibility(self):
        m=model();m['tail']='two_sided';m['test_id']='tgl_compat'
        pos=qualify(m,[8.,8.],3.);neg=qualify(m,[-2.,-2.],3.)
        self.assertEqual(pos['p'],neg['p'])
        self.assertAlmostEqual(pos['p'],2*2.866515718791946e-7,delta=1e-20)
        self.assertLess(pos['z_equivalent_upper_tail'],5.)

    def test_runtime_beta_K_not_observed(self):
        ALPHA_FINE_CODATA_2018=7.2973525693e-3
        beta=ALPHA_FINE_CODATA_2018*math.sqrt(math.e)
        k=math.exp(beta*math.log(.3*(1+1089.95)**3+9e-5*(1+1089.95)**4+.69991)/3)
        r=qualify(model(factor=k),[70.,70.],60.)
        self.assertIsNone(r['observed_F9_verdict'])
        self.assertFalse(r['gate_moved'])

    def test_upper_power_at_D5_is_half(self):
        r=design_power(model(),6.,1.,5.,'SAME_AS_NULL')
        self.assertEqual(r['alternative_mean_z'],5.)
        self.assertEqual(r['power'],.5)

    def test_power_under_null_is_size_for_any_H0(self):
        for h in [0.,50.,1000.]:
            r=design_power(model(),1.,h,5.,'SAME_AS_NULL')
            self.assertAlmostEqual(r['power'],2.866515718791946e-7,delta=1e-20)

    def test_power_changed_alternative_covariance(self):
        r=design_power(model(),7.,1.,5.,[[4.,0.,0.],[0.,4.,0.],[0.,0.,2.]])
        self.assertEqual(r['alternative_sd_z'],2.)
        self.assertAlmostEqual(r['power'],.5*math.erfc(-.5/math.sqrt(2)))

    def test_two_sided_power_under_null(self):
        m=model();m['tail']='two_sided'
        r=design_power(m,1.,70.,5.,'SAME_AS_NULL')
        self.assertAlmostEqual(r['power'],math.erfc(5/math.sqrt(2)),delta=1e-20)

    def test_missing_cross_covariance_not_zero(self):
        for field in ['cross_covariance','cross_covariance_source']:
            m=model();del m[field]
            with self.subTest(field=field),self.assertRaises(PivotError):qualify(m,[1.,1.],0.)
        m=model();m['cross_covariance']=None
        with self.assertRaises(PivotError):qualify(m,[1.,1.],0.)

    def test_joint_covariance_invalid_despite_valid_C(self):
        with self.assertRaises(PivotError):qualify(model(cross=[.6,.6]),[1.,1.],0.)

    def test_exact_PSD_rejects_small_negative(self):
        m=model();m['C']=[[1.]];m['cross_covariance']=[1.];m['background_variance']=1.-1e-15;repin(m)
        with self.assertRaises(PivotError):qualify(m,[1.],0.)

    def test_zero_variance_singular_not_repaired(self):
        m=model();m['background_variance']=0.;repin(m)
        with self.assertRaises(PivotError):qualify(m,[1.,1.],0.)

    def test_missing_or_estimated_distribution_refused(self):
        for key,value in [('distribution','ESTIMATED'),('fixed_before_centres',False),('mode','OBSERVED')]:
            m=model();m[key]=value
            with self.subTest(key=key),self.assertRaises(PivotError):qualify(m,[1.,1.],0.)

    def test_not_normalized_weights_refused(self):
        m=model();m['weights_rule']='EXPLICIT_NORMALIZED_RATIONAL';m['weights']=[[1,3],[1,3]]
        with self.assertRaises(PivotError):qualify(m,[1.,1.],0.)

    def test_nonfinite_boolean(self):
        for x in [True,float('nan'),float('inf')]:
            with self.subTest(x=str(x)),self.assertRaises(PivotError):qualify(model(),[1.,x],0.)

    def test_pin_mutation(self):
        m=model();m['C'][0][0]=2.
        with self.assertRaises(PivotError):qualify(m,[1.,1.],0.)

    def test_extreme_tail_recuses_no_infinite_Z(self):
        with self.assertRaises(PivotError):qualify(model(),[100.,100.],0.)

    def test_family_two_tests_not_automatic_five(self):
        a=qualify(model(),[8.,8.],3.)
        m=model();m['test_id']='tgl_compat';m['tail']='two_sided';b=qualify(m,[8.,8.],3.)
        r=family_adjust(multiplicity(),[a,b])
        self.assertEqual(r['m'],2)
        self.assertEqual(r['results']['lcdm_upper']['p'],2*a['p'])

    def test_missing_scenario_and_Sidak_refused(self):
        with self.assertRaises(PivotError):family_adjust(multiplicity(),[])
        m=multiplicity();m['method']='sidak'
        with self.assertRaises(PivotError):family_adjust(m,[])

    def test_family_robust_uses_worst_and_no_cross_route(self):
        f=multiplicity();f['test_ids']=['lcdm_upper'];f['scenario_ids']=['s1','s2']
        a=qualify(model(),[8.,8.],3.);m=model();m['scenario_id']='s2';b=qualify(m,[6.,6.],3.)
        r=family_adjust(f,[a,b]);self.assertEqual(r['results']['lcdm_upper']['p_robust'],b['p'])
        b['route_id']='OTHER'
        with self.assertRaises(PivotError):family_adjust(f,[a,b])


if __name__=='__main__':unittest.main(verbosity=2)
