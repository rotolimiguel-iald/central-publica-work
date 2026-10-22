"""Focal regression for near-equal scalar covariance cancellation."""
import math
import unittest
from tail_adapter_r2 import qualify_gaussian_score
from test_tail_adapter import contract
from test_scalar_bridge import spec, C, Y
from scalar_bridge_r2 import qualify_scalar_synthetic


class StableRoots(unittest.TestCase):
    def test_requested_covariance_plus(self):
        r=qualify_gaussian_score(contract(mu1=(1.,),cov1=((1.+1e-12,),)),[3.])
        self.assertAlmostEqual(r['p_upper'],.5*math.erfc(3/math.sqrt(2)),delta=1e-14)
        self.assertAlmostEqual(r['roots'][1],3.,delta=2e-14)

    def test_covariance_minus(self):
        r=qualify_gaussian_score(contract(mu1=(1.,),cov1=((1.-1e-12,),)),[3.])
        self.assertAlmostEqual(r['p_upper'],.5*math.erfc(3/math.sqrt(2)),delta=1e-14)
        self.assertAlmostEqual(r['roots'][0],3.,delta=2e-14)

    def test_negative_mean_and_lower_root(self):
        r=qualify_gaussian_score(contract(mu1=(-1.,),cov1=((1.+1e-12,),)),[-3.])
        self.assertAlmostEqual(r['p_upper'],.5*math.erfc(3/math.sqrt(2)),delta=1e-14)
        self.assertAlmostEqual(r['roots'][0],-3.,delta=2e-14)

    def test_bridge_consumes_r2(self):
        r=qualify_scalar_synthetic(spec(),Y,C)
        self.assertEqual(r['score_quadratic_tail']['root_algorithm'],'SCALED_STABLE_Q_FORMULA')
        self.assertAlmostEqual(r['score_quadratic_tail']['p_upper'],r['score_with_logdet_tail']['p_upper'],delta=1e-13)


if __name__=='__main__':unittest.main(verbosity=2)
