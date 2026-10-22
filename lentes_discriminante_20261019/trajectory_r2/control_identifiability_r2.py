"""Exact rational controls of thin-lens stationarity, not a TGL prediction."""
from fractions import Fraction as F
from pathlib import Path
import json, hashlib, datetime, time, traceback
P=Path(__file__).resolve().parent
def pin(path):return {'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
def new(name,obj):
 with (P/name).open('x',encoding='utf-8') as f:json.dump(obj,f,ensure_ascii=False,indent=2)
if __name__=='__main__':
 freeze=json.loads((P/'FREEZE_IDENTIFIABILITY_R2.json').read_text(encoding='utf-8'))
 for x in freeze['evidence']:
  assert pin(Path(x['path']))['sha256']==x['sha256'], 'Pin mismatch'
 if (P/'RESULT_IDENTIFIABILITY_R2.json').exists():raise RuntimeError('Result exists')
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();tick=time.perf_counter()
 new('START_IDENTIFIABILITY_R2.json',{'start_utc':start,'pins':freeze['evidence']})
 checks=[]; values={};exit_code=0
 def ck(name,yes):
  checks.append({'name':name,'passed':bool(yes)})
  if not yes:raise AssertionError(name)
 try:
  xp,xm,b,y=F(2),F(-1,2),F(1),F(3,2)
  e=F(-1,100); lam=F(7,5)
  for x in [xp,xm]:
   ck('point_mass_stationarity_'+str(x),x-y-b/x==0)
   dx=-x/(1+b/x**2)
   ck('quadratic_probe_linearized_image_'+str(x),(1+b/x**2)*dx+x==0)
   ck('envelope_derivative_'+str(x),(x-y-b/x)*dx+x*x/2==x*x/2)
  ck('displacements',-xp/(1+b/xp**2)==F(-8,5) and -xm/(1+b/xm**2)==F(1,10))
  ck('oriented_delay_derivative',xm*xm/2-xp*xp/2==F(-15,8))
  # MST identity coefficients: phi_lambda-lambda*phi is source-only.
  for x in [xp,xm,F(5,4)]:
   # Symbol of psi cancels identically; evaluate the polynomial remainder.
   remainder=(x-lam*y)**2/2-(1-lam)*x*x/2-lam*(x-y)**2/2
   ck('MST_source_constant_'+str(x),remainder==lam*(lam-1)*y*y/2)
   ck('MST_gradient_'+str(x), x-lam*y-(lam*b/x+(1-lam)*x)==lam*(x-y-b/x))
  # q(x)=x^4/4; refit source AND angular mass, not mass alone.
  db=(xp**3-xm**3)/(1/xp-1/xm);dy=xp**3-db/xp
  be=b+e*db;ye=y+e*dy
  ck('quartic_profile_derivatives',db==F(13,4) and dy==F(51,8))
  ck('positive_angular_mass',be>0)
  for x in [xp,xm]:
   ck('profiled_image_stationarity_'+str(x),x-ye-be/x+e*x**3==0)
   ck('negative_frozen_images_fail_'+str(x),x-y-b/x+e*x**3!=0)
  # Delay is A+B*log(4), with exact rational coefficients.
  A=(xm*xm-xp*xp)/2-(xm-xp)*ye+e*(xm**4-xp**4)/4
  B=be
  ck('quartic_delay_coefficient_A',A==F(15,8)+e*F(765,64))
  ck('quartic_delay_coefficient_B',B==1+e*F(13,4))
  ck('positive_delay_coefficients',A>0 and B>0)
  values={'quadratic_image_shifts':[str(F(-8,5)),str(F(1,10))],'quadratic_delay_derivative':str(F(-15,8)),'quartic_db':str(db),'quartic_dy':str(dy),'profiled_b':str(be),'profiled_y':str(ye),'profiled_delta_phi_A':str(A),'profiled_delta_phi_B':str(B),'basis':'A+B*log(4)','distance_formula':'D_e=D_0*(15/8+log(4))/(A+B*log(4)); exact cancellation, not independently constrained distance'}
 except Exception:
  exit_code=1;values['error']=traceback.format_exc()
 new('RESULT_IDENTIFIABILITY_R2.json',{'schema':'iald.lensing.exact_controls.r2','start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-tick,'exit_code':exit_code,'passed':exit_code==0,'checks':checks,'values':values,'statute':'REAL exact rational controls of a DERIVED generic model; not observed evidence','sources':freeze['evidence']})
 print(json.dumps({'exit_code':exit_code,'passed':exit_code==0,'checks':len(checks),'values':values}));raise SystemExit(exit_code)
