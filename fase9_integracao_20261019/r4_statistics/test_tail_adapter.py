"""Deterministic analytic/synthetic qualification. No sampled or observed F9 data."""
import copy
import math
import unittest
import numpy as np
from tail_adapter import CalibrationError, qualify_gaussian_score as qualify, adjust_family


def contract(mu0=(0.,), mu1=(2.,), cov0=((1.,),), cov1=None, scenario='s1'):
    return dict(id='synthetic-simple', route_id='R4_SYNTHETIC', scenario_id=scenario,
                kind='SIMPLE_GAUSSIAN_KNOWN_SPD', parameters_fixed_independently_of_y=True,
                mu0=list(mu0), mu1=list(mu1), cov0=[list(r) for r in cov0],
                cov1=[list(r) for r in (cov0 if cov1 is None else cov1)])


def family(tests=None, scenarios=None, method='bonferroni'):
    return dict(id='synthetic-family', route_id='R4_SYNTHETIC', method=method,
                test_ids=tests or ['t1', 't2'], scenario_ids=scenarios or ['s1', 's2'],
                scope='SYNTHETIC_QUALIFICATION_ONLY')


def records():
    return [{'test_id': t, 'result': qualify(contract(scenario=s), [y])}
            for t in ['t1', 't2'] for s, y in [('s1', 3.), ('s2', 2.)]]


class Qualification(unittest.TestCase):
    def test_equal_normal_asimov(self):
        r = qualify(contract(), [2.])
        self.assertAlmostEqual(r['raw_score'], 4.)
        self.assertAlmostEqual(r['z_upper_normal_equivalent'], 2.)
        self.assertAlmostEqual(r['p_upper'], .5*math.erfc(math.sqrt(2)))

    def test_score_not_sqrt_score(self):
        r = qualify(contract(), [3.])
        self.assertAlmostEqual(r['z_upper_normal_equivalent'], 3.)
        self.assertGreater(abs(math.sqrt(r['raw_score'])-3), .1)

    def test_negative_score_valid_tail(self):
        r = qualify(contract(), [0.])
        self.assertEqual(r['raw_score'], -4.)
        self.assertAlmostEqual(r['p_upper'], .5)

    def test_five_sigma_and_half_power(self):
        r = qualify(contract(mu1=(5.,)), [5.])
        self.assertAlmostEqual(r['p_upper'], 2.866515718791946e-7, delta=1e-20)
        self.assertAlmostEqual(r['z_upper_normal_equivalent'], 5.)
        self.assertEqual(.5*math.erfc((5-5)/math.sqrt(2)), .5)

    def test_correlated_multivariate(self):
        r = qualify(contract(mu0=(0, 0), mu1=(1, 1), cov0=((2, 1), (1, 2))), [1, 1])
        self.assertAlmostEqual(r['design_D'], math.sqrt(2/3))

    def test_affine_change_of_coordinates(self):
        r1 = qualify(contract(), [3.])
        r2 = qualify(contract(mu0=(7.,), mu1=(13.,), cov0=((9.,),)), [16.])
        self.assertAlmostEqual(r1['p_upper'], r2['p_upper'])

    def test_unequal_scalar_positive_quadratic(self):
        r = qualify(contract(mu1=(0.,), cov1=((4.,),)), [2.])
        self.assertAlmostEqual(r['p_upper'], math.erfc(math.sqrt(2)))
        self.assertAlmostEqual(r['raw_score'], 3.)

    def test_unequal_scalar_negative_quadratic(self):
        r = qualify(contract(mu1=(0.,), cov1=((.25,),)), [1.])
        self.assertAlmostEqual(r['p_upper'], math.erf(1/math.sqrt(2)))

    def test_noncentral_scalar_roots(self):
        # T=.75*z²+z-1; at y=2 roots2 and-10/3.
        r = qualify(contract(mu1=(2.,), cov1=((4.,),)), [2.])
        p = .5*math.erfc(2/math.sqrt(2))+.5*math.erfc((10/3)/math.sqrt(2))
        self.assertAlmostEqual(r['p_upper'], p)

    def test_logdet_shift_preserves_tail_for_fixed_models(self):
        c = contract(mu1=(2.,), cov1=((4.,),))
        raw = qualify(c, [3.]); lr = qualify(c, [3.], 'normalized_log_likelihood_ratio')
        self.assertAlmostEqual(lr['raw_score']-raw['raw_score'], -math.log(4))
        self.assertAlmostEqual(lr['p_upper'], raw['p_upper'])

    def test_full_multivariate_unequal_refuses_tail(self):
        r = qualify(contract(mu0=(0, 0), mu1=(1, 1), cov0=((1, 0), (0, 1)), cov1=((2, 0), (0, 1))), [1, 1])
        self.assertEqual(r['calibration'], 'CALIBRATION_UNAVAILABLE')
        self.assertIsNone(r['p_upper'])
        self.assertEqual(r['null_quadratic_form']['A'], [[.5, 0.], [0., 0.]])

    def test_no_allclose_covariance_shortcut(self):
        r = qualify(contract(mu0=(0, 0), mu1=(1, 1), cov0=((1, 0), (0, 1)), cov1=((1+1e-12, 0), (0, 1))), [1, 1])
        self.assertEqual(r['calibration'], 'CALIBRATION_UNAVAILABLE')

    def test_missing_contract(self):
        for c in [None, {}, {'id':'x'}]:
            with self.subTest(c=c), self.assertRaises(CalibrationError): qualify(c, [0.])

    def test_estimated_or_composite_distribution_refused(self):
        for k,v in [('parameters_fixed_independently_of_y', False), ('kind', 'FITTED_OR_PROFILED')]:
            c=contract(); c[k]=v
            with self.subTest(k=k), self.assertRaises(CalibrationError): qualify(c, [0.])

    def test_no_bayes_or_sqrt_shortcut(self):
        for kind in ['lnB', 'sqrtDeltaQ', 'wilks']:
            with self.subTest(kind=kind), self.assertRaises(CalibrationError): qualify(contract(), [0.], kind)

    def test_nonfinite_or_bool_refused(self):
        for val in [True, float('nan'), float('inf'), -float('inf')]:
            for field in ['y','mu0','cov0']:
                c=contract(); y=[0.]
                if field=='y': y=[val]
                elif field=='mu0': c[field]=[val]
                else:c[field]=[[val]]
                with self.subTest(val=str(val),field=field), self.assertRaises(CalibrationError):qualify(c,y)

    def test_nonsymmetric_or_singular_refused(self):
        for cov in [((1, 1), (0, 1)), ((1, 1), (1, 1)), ((1, 0), (0, -1))]:
            with self.subTest(cov=cov), self.assertRaises(CalibrationError):qualify(contract(mu0=(0,0),mu1=(1,1),cov0=cov),[1,1])

    def test_identical_hypotheses_no_vacuous_claim(self):
        with self.assertRaises(CalibrationError):qualify(contract(mu1=(0.,)),[0.])

    def test_tail_underflow_refused(self):
        with self.assertRaises(CalibrationError):qualify(contract(),[50.])

    def test_numeric_overflow_refused(self):
        with self.assertRaises(CalibrationError):qualify(contract(),[1e308])

    def test_family_robust_max_not_min(self):
        r=adjust_family(family(),records())
        p=.5*math.erfc(math.sqrt(2))
        self.assertAlmostEqual(r['results']['t1']['p_robust'],p)
        self.assertAlmostEqual(r['results']['t1']['p_upper'],2*p)
        self.assertIsNone(r['observed_verdict'])

    def test_bonferroni_dependence_permitted_not_sidak(self):
        # Identical test outputs are perfectly dependent; Bonferroni still valid.
        self.assertEqual(adjust_family(family(),records())['results']['t1'],adjust_family(family(),records())['results']['t2'])
        with self.assertRaises(CalibrationError):adjust_family(family(method='sidak'),records())

    def test_missing_scenario_refused(self):
        with self.assertRaises(CalibrationError):adjust_family(family(),records()[:-1])

    def test_duplicate_scenario_refused(self):
        rr=records();rr[-1]=copy.deepcopy(rr[0])
        with self.assertRaises(CalibrationError):adjust_family(family(),rr)

    def test_cross_route_refused(self):
        rr=records();rr[0]['result']['route_id']='F9_JOINT'
        with self.assertRaises(CalibrationError):adjust_family(family(),rr)

    def test_unqualified_record_refused(self):
        rr=records();rr[0]['result']['calibration']='CALIBRATION_UNAVAILABLE'
        with self.assertRaises(CalibrationError):adjust_family(family(),rr)

    def test_invalid_tail_refused(self):
        for p in [None, True, float('nan'), 0, -1, 1.1]:
            rr=records();rr[0]['result']['p_upper']=p
            with self.subTest(p=str(p)),self.assertRaises(CalibrationError):adjust_family(family(),rr)

    def test_adoption_into_observed_route_refused(self):
        f=family();f['scope']='OBSERVED_F9_SCALAR'
        with self.assertRaises(CalibrationError):adjust_family(f,records())

    def test_no_correction_needs_single_test(self):
        with self.assertRaises(CalibrationError):adjust_family(family(method='none_single_test'),records())
        f=family(tests=['t1'],method='none_single_test')
        rr=[r for r in records() if r['test_id']=='t1']
        self.assertEqual(adjust_family(f,rr)['results']['t1']['multiplicity_factor'],1)

    def test_p_one_outputs_no_fake_finite_sigma(self):
        rr=records()
        for r in rr:r['result']['p_upper']=1.
        out=adjust_family(family(),rr)['results']['t1']
        self.assertIsNone(out['z_upper_normal_equivalent'])
        self.assertEqual(out['z_limit_if_p_one'],'-infinity')


if __name__ == '__main__':
    unittest.main(verbosity=2)
