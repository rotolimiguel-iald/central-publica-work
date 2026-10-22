"""GLS bridge checks against full matrices, fixed synthetic data only."""
import hashlib
import math
import unittest
import numpy as np
from scalar_bridge import qualify_scalar_synthetic
from tail_adapter import CalibrationError

C=np.array([[1., .2, .1], [.2, 2., .3], [.1, .3, 3.]])
Y=np.array([71.,74.,72.])  # Fabricated fixture, not reader centers.


def spec(c=C):
    # Same runtime rule; no literal beta. K computed from fixed synthetic cosmology.
    ALPHA_FINE_CODATA_2018=7.2973525693e-3
    beta=ALPHA_FINE_CODATA_2018*math.sqrt(math.e)
    e2=.3*(1+1089.95)**3+9e-5*(1+1089.95)**4+1-.3-9e-5
    return dict(id='scalar-synthetic-reduction',route_id='R4_SYNTHETIC',scenario_id='s1',
                mode='SYNTHETIC_ONLY',background_sampling='GAUSSIAN_DRAW_IN_SAMPLING_MODEL',
                parameters_fixed_independently_of_y=True,K=math.exp(beta*math.log(e2)/3),H_bg=68.,sigma_bg=.3,
                covariance_sha256=hashlib.sha256(c.astype('<f8').tobytes()).hexdigest())


class ScalarBridge(unittest.TestCase):
    def test_full_matrix_Q_and_logdet(self):
        s=spec(); r=qualify_scalar_synthetic(s,Y,C)
        qs=[]; lds=[]
        for f in [1.,s['K']]:
            mean=np.ones(3)*s['H_bg']*f
            cov=C+(s['sigma_bg']*f)**2*np.ones((3,3))
            rr=Y-mean
            qs.append(float(rr@np.linalg.solve(cov,rr)));lds.append(float(np.linalg.slogdet(cov)[1]))
        self.assertAlmostEqual(qs[0]-qs[1],r['score_quadratic_tail']['raw_score'],delta=1e-11)
        self.assertAlmostEqual(qs[0]-qs[1]+lds[0]-lds[1],r['score_with_logdet_tail']['raw_score'],delta=1e-11)
        self.assertAlmostEqual(r['score_quadratic_tail']['p_upper'],r['score_with_logdet_tail']['p_upper'],delta=1e-13)

    def test_orthogonal_displacement_cancels(self):
        s=spec(); one=np.ones(3); w=np.linalg.solve(C,one); v=np.array([1.,-w[0]/w[1],0.])
        r=qualify_scalar_synthetic(s,Y,C); shifted=qualify_scalar_synthetic(s,Y+10*v,C)
        self.assertAlmostEqual(r['score_quadratic_tail']['raw_score'],shifted['score_quadratic_tail']['raw_score'],delta=1e-11)
        self.assertGreater(abs(r['common_perpendicular_Q']-shifted['common_perpendicular_Q']),10)

    def test_zero_background_variance_reduces_normal(self):
        s=spec();s['sigma_bg']=0.
        self.assertEqual(qualify_scalar_synthetic(s,Y,C)['score_quadratic_tail']['calibration'],'ANALYTIC_SIMPLE_NORMAL')

    def test_matrix_pin_mutation_refused(self):
        changed=C.copy();changed[0,0]+=1e-6
        with self.assertRaises(CalibrationError):qualify_scalar_synthetic(spec(),Y,changed)

    def test_observed_and_composite_null_refused(self):
        for key,value in [('mode','OBSERVED'),('background_sampling','UNKNOWN_FIXED_H0'),('parameters_fixed_independently_of_y',False)]:
            s=spec();s[key]=value
            with self.subTest(key=key), self.assertRaises(CalibrationError):qualify_scalar_synthetic(s,Y,C)

    def test_identity_and_negative_K_refused(self):
        for k in [1.,-1.]:
            s=spec();s['K']=k
            with self.subTest(k=k),self.assertRaises(CalibrationError):qualify_scalar_synthetic(s,Y,C)

    def test_no_silent_shared_variance_repeated_per_reader(self):
        r=qualify_scalar_synthetic(spec(),Y,C);s=spec()
        wrong=C+s['sigma_bg']**2*np.eye(3)
        wrongvar=1/(np.ones(3)@np.linalg.solve(wrong,np.ones(3)))
        self.assertGreater(abs(wrongvar-r['null_variance']),.01)

    def test_three_reader_full_sampling_variance(self):
        s=spec();w=np.linalg.solve(C,np.ones(3));w=w/w.sum()
        cov=C+s['sigma_bg']**2*np.ones((3,3))
        r=qualify_scalar_synthetic(s,Y,C)
        self.assertAlmostEqual(float(w@cov@w),r['null_variance'],delta=1e-14)


if __name__=='__main__':unittest.main(verbosity=2)
