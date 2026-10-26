"""Execution harness, NOT a source excerpt. No sealed answers enter the calculation.
Only numerical outputs leave this harness; historical verdict prose is never rendered.
"""
import json, math, time

def calculate(excerpt, scalar, progress=None):
 ns={'__name__':'film_numerical_excerpt','ONE':1}
 exec(compile(excerpt,'um_nucleo_filme.py','exec'),ns)
 exec(compile('if True:\n'+scalar,'um_scalar_excerpt.py','exec'),ns)
 calls=[('fractal_dephasing','fractal_dephasing_principle',(1,)),
 ('smatrix_closure','prove_smatrix_closure',(1,)),
 ('solder_4d','prove_solder_4d',(1,)),('local_breuer_gap','prove_local_breuer_gap',(1,)),
 ('minimal_solder','prove_minimal_solder',(1,)),('schwarzschild_step','prove_the_schwarzschild_step',(1,)),
 ('graviton_polarization','prove_graviton_polarization',(1,{})),
 ('the_TGL_identity_equation','prove_the_TGL_identity_equation',({},)),
 ('light_is_J','prove_light_is_J',(1,{})),('powers_ladder','prove_powers_ladder',(1,{}))]
 out={};timings={}
 def numeric_leaves(value,path):
  if isinstance(value,dict):
   for k,v in value.items(): numeric_leaves(v,path+'.'+k)
  elif isinstance(value,(int,float)) and not isinstance(value,bool):
   if not math.isfinite(float(value)): raise ValueError('Non-finite calculation: '+path)
   out[path]=float(value)
 for key,fn,args in calls:
  if progress: progress(key)
  start=time.perf_counter();result=ns[fn](*args);timings[key]=time.perf_counter()-start
  numeric_leaves(result,'core.'+key)
 for key,var in [('omega_I','omega_I'),('HALF','HALF'),('meia_nat_residual','mn_resid'),('S_boundary','S_boundary'),('SQRT_E','SQRT_E')]: out['core.'+key]=float(ns[var])
 beta=out['core.graviton_polarization.values.beta_runtime']
 out['core.theta_M_rad']=math.asin(math.sqrt(beta));out['core.theta_M_deg']=math.degrees(out['core.theta_M_rad'])
 return {'values':out,'timings_seconds':timings,'numpy_version':ns['np'].__version__}
