"""Four targeted range controls only; no repetition of the prior26 cases."""
import math,unittest
import fixed_background_pivot_r2 as m

def contract(v,tail='upper'):
 return dict(id='range-r2',route_id='R4_RANGE_R2',scenario_id='finite_extreme',test_id=tail,mode='SYNTHETIC_ONLY',distribution='JOINT_GAUSSIAN_FIXED_UNKNOWN_H0_KNOWN_ERRORS',factor=1.,weights_rule='FIXED_GLS_C',C=[[v]],background_variance=v,cross_covariance=[0.],cross_covariance_source='SYNTHETIC_RANGE',fixed_before_centres=True,tail=tail,matrix_sha256=m.digest([[v,0.],[0.,v]]))

class RangeTests(unittest.TestCase):
 def test_extreme_upper(self):
  r=m.design_power(contract(1e-300),2.,1e150,5.,[[1e300,0.],[0.,1e300]])
  expected=m.sf((5*math.sqrt(2e-300)-1e150)/math.sqrt(2e300))
  self.assertLessEqual(abs(r['power']-expected),1e-15)
  self.assertTrue(math.isfinite(r['alternative_sd_z']))
  self.assertTrue(math.isfinite(r['alternative_mean_z']))
 def test_extreme_two_sided(self):
  r=m.design_power(contract(1e-300,'two_sided'),2.,1e150,5.,[[1e300,0.],[0.,1e300]])
  a=5*math.sqrt(2e-300);s=math.sqrt(2e300)
  expected=m.sf((a-1e150)/s)+m.sf((a+1e150)/s)
  self.assertLessEqual(abs(r['power']-expected),1e-15)
  self.assertTrue(math.isfinite(r['alternative_sd_z']))
 def test_unrepresentable_sd_refuses(self):
  with self.assertRaises(m.PivotError):m.design_power(contract(5e-324),2.,1.,5.,[[5e307,0.],[0.,5e307]])
 def test_unrepresentable_mean_refuses(self):
  with self.assertRaises(m.PivotError):m.design_power(contract(1e-300),2.,1e308,5.,'SAME_AS_NULL')

if __name__=='__main__':unittest.main(verbosity=2)
