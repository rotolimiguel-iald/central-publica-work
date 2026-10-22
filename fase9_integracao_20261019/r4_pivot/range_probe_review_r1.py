"""One adversarial numerical range check; no observed input or old test rerun."""
from pathlib import Path
import hashlib,json,math,datetime,importlib.util
p=Path(__file__).resolve().parent
source=p/'fixed_background_pivot.py'
expected='3a596f022b03385a9a9218906079a5f66acb3a95db6391af02ec0d7a3dc73331'
assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
spec=importlib.util.spec_from_file_location('pivot_review',source)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
contract=dict(id='range-review',route_id='R4_RANGE_ONLY',scenario_id='finite_extreme',test_id='upper',mode='SYNTHETIC_ONLY',distribution='JOINT_GAUSSIAN_FIXED_UNKNOWN_H0_KNOWN_ERRORS',factor=1.,weights_rule='FIXED_GLS_C',C=[[1e-300]],background_variance=1e-300,cross_covariance=[0.],cross_covariance_source='SYNTHETIC_RANGE',fixed_before_centres=True,tail='upper',matrix_sha256=m.digest([[1e-300,0.],[0.,1e-300]]))
actual=m.design_power(contract,2.,1e150,5.,[[1e300,0.],[0.,1e300]])
# Same analytic law evaluated in unstandardized units; all intermediates finite.
threshold_original=5.*math.sqrt(2e-300)
expected_power=m.sf((threshold_original-1e150)/math.sqrt(2e300))
r={'status':'MATERIAL_NUMERICAL_RANGE_FINDING' if abs(actual['power']-expected_power)>1e-12 else 'NOT_REPRODUCED','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':expected,'probe_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'actual_power':actual['power'],'actual_sd_finite':math.isfinite(actual['alternative_sd_z']),'expected_stable_power':expected_power,'absolute_difference':abs(actual['power']-expected_power),'observed_data':False,'old_tests_repeated':False}
with (p/'RANGE_PROBE_RESULT_R1.json').open('x',encoding='utf-8') as f:json.dump(r,f,indent=2,allow_nan=False)
print(json.dumps(r))
