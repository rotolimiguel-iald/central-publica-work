from pathlib import Path
import hashlib,json,math,datetime
ROOT=Path(__file__).resolve().parent
x=0.0;total=0.0;values=[];means=[]
for n in range(4097):
 assert math.isfinite(x) and x==float(n)
 if n>0:
  mean=total/n
  assert math.isfinite(mean) and mean==(n-1)/2
  means.append(mean)
 values.append(x);total+=x
 nxt=x+1
 assert math.isfinite(nxt) and nxt-x==1
 x=nxt
assert values[-1]==4096 and means[-1]==2047.5
assert all(values[i+1]-values[i]==1 for i in range(len(values)-1))
assert all(means[i+1]-means[i]==0.5 for i in range(len(means)-1))
result={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASSA_CONTROLE_NEGATIVO','n_max':4096,'all_values_finite':True,'increment_exactly_one':True,'all_means_finite':True,'means_increment_exactly_half':True,'end_value':values[-1],'end_mean':means[-1],'A1_direct':'FALHA_ESPERADA','A1_cesaro':'FALHA_ESPERADA','proof':'Induction: x_0=0 and x_(n+1)=x_n+1 imply x_n=n for every n; arithmetic sum gives Cesaro_N=(N-1)/2. Both diverge, independently of finite samples. Equation x+1=x impossible.','scope':'Affine map on real line, outside linear/CPTP finite class.','R3_note':'Submitted runner fills affine labels by closed analytic formula and sets expected_outcomes_met=true; its all_ok does not consume an affine-control predicate. This independent artifact explicitly iterates and checks the recurrence.','probability_note':'Submitted probability_loss_per_step=0.0 is an expected mathematical identity, not a measured residual; measured trace-preservation residuals live in channel_checks.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
with (ROOT/'ADENDO_CONTROLE_AFIM_R1.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(result,f,indent=2,ensure_ascii=False,allow_nan=False)
print(json.dumps(result,indent=2,ensure_ascii=False))
